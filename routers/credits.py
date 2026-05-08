from fastapi import APIRouter, Depends, HTTPException, Request
from supabase import Client
from datetime import datetime, timezone
from typing import List
import stripe
import uuid

from config import settings
from database import get_db, require_role
from models.credit import (
    CreditsResponse, CreditTransactionResponse, PaymentResponse,
    CheckoutCreate, CheckoutResponse, PACKAGE_CONFIG,
)

stripe.api_key = settings.stripe_secret_key

router = APIRouter()


def _require_supplier_profile(user_id: str, db: Client) -> dict:
    result = db.table("supplier_profiles").select("*").eq("user_id", user_id).maybe_single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Supplier profile not found")
    return result.data


def _ensure_credits_account(supplier_id: str, db: Client) -> dict:
    """Get credits row, creating it if it doesn't exist yet."""
    result = db.table("credits").select("*").eq("supplier_id", supplier_id).maybe_single().execute()
    if result and result.data:
        return result.data
    now = datetime.now(timezone.utc).isoformat()
    created = db.table("credits").insert({
        "supplier_id": supplier_id,
        "balance": 0,
        "reserved": 0,
        "total_purchased": 0,
        "total_used": 0,
        "updated_at": now,
    }).execute()
    if created and created.data:
        return created.data[0]
    result2 = db.table("credits").select("*").eq("supplier_id", supplier_id).maybe_single().execute()
    return result2.data if result2 else {}


# ── Balance & history ─────────────────────────────────────────────────────────

@router.get("/me", response_model=CreditsResponse)
async def get_my_credits(
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    return _ensure_credits_account(profile["id"], db)


@router.get("/me/transactions", response_model=List[CreditTransactionResponse])
async def get_my_transactions(
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    result = (
        db.table("credit_transactions")
        .select("*")
        .eq("supplier_id", profile["id"])
        .order("created_at", desc=True)
        .execute()
    )
    return result.data


# ── Stripe checkout ───────────────────────────────────────────────────────────

@router.post("/checkout", response_model=CheckoutResponse, status_code=201)
async def create_checkout(
    payload: CheckoutCreate,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    pkg = PACKAGE_CONFIG[payload.package_type]
    now = datetime.now(timezone.utc).isoformat()

    # Create a pending payment record first so we have an ID for metadata
    payment_result = db.table("payments").insert({
        "supplier_id": profile["id"],
        "stripe_payment_id": "pending",  # updated after Stripe session is created
        "package_type": payload.package_type.value,
        "credits_purchased": pkg["credits"],
        "amount_usd": pkg["price_usd"],
        "status": "pending",
        "created_at": now,
    }).execute()
    payment_id = payment_result.data[0]["id"]

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": int(pkg["price_usd"] * 100),
                "product_data": {
                    "name": f"SourcingElf Credits - {payload.package_type.value.replace('_', ' ').title()}",
                    "description": f"{pkg['credits']} connection credit(s)",
                },
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"{settings.frontend_url}/credits/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{settings.frontend_url}/credits/cancelled",
        metadata={
            "payment_id": payment_id,
            "supplier_id": profile["id"],
            "package_type": payload.package_type.value,
            "credits": str(pkg["credits"]),
        },
    )

    # Store the real Stripe session ID
    db.table("payments").update({
        "stripe_payment_id": session.id,
    }).eq("id", payment_id).execute()

    return CheckoutResponse(checkout_url=session.url, payment_id=uuid.UUID(payment_id))


@router.post("/webhook", status_code=200)
async def stripe_webhook(request: Request, db: Client = Depends(get_db)):
    """
    Stripe sends POST here on payment events.
    Verify the signature, then credit the supplier on checkout.session.completed.
    """
    body = await request.body()
    sig = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(body, sig, settings.stripe_webhook_secret)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid Stripe signature")

    if event["type"] != "checkout.session.completed":
        return {"received": True}

    session = event["data"]["object"]
    meta = session.get("metadata", {})
    payment_id = meta.get("payment_id")
    supplier_id = meta.get("supplier_id")
    credits_to_add = int(meta.get("credits", 0))

    if not all([payment_id, supplier_id, credits_to_add]):
        raise HTTPException(status_code=400, detail="Missing metadata in Stripe session")

    # Guard against duplicate webhook deliveries
    payment = db.table("payments").select("*").eq("id", payment_id).maybe_single().execute()
    if not payment.data or payment.data["status"] == "succeeded":
        return {"received": True}

    now = datetime.now(timezone.utc).isoformat()

    db.table("payments").update({
        "status": "succeeded",
        "stripe_customer_id": session.get("customer"),
        "paid_at": now,
    }).eq("id", payment_id).execute()

    credits = _ensure_credits_account(supplier_id, db)
    new_balance = credits["balance"] + credits_to_add

    db.table("credits").update({
        "balance": new_balance,
        "total_purchased": credits["total_purchased"] + credits_to_add,
        "updated_at": now,
    }).eq("supplier_id", supplier_id).execute()

    db.table("credit_transactions").insert({
        "supplier_id": supplier_id,
        "type": "topup",
        "amount": credits_to_add,
        "balance_after": new_balance,
        "payment_id": payment_id,
        "notes": f"Stripe checkout {session['id']}",
        "created_at": now,
    }).execute()

    return {"received": True}


@router.get("/me/payments", response_model=List[PaymentResponse])
async def get_my_payments(
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    result = (
        db.table("payments")
        .select("*")
        .eq("supplier_id", profile["id"])
        .order("created_at", desc=True)
        .execute()
    )
    return result.data
