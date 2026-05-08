from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from datetime import datetime, timezone
from typing import List
import uuid

from database import get_db, require_role
from models.lead import (
    BuyingLeadCreate, BuyingLeadUpdate, BuyingLeadResponse,
    ApplicationCreate, ApplicationResponse,
    ConnectionResponse,
)

router = APIRouter()


def _require_buyer_profile(user_id: str, db: Client) -> dict:
    result = db.table("buyer_profiles").select("*").eq("user_id", user_id).maybe_single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Buyer profile not found")
    return result.data


def _require_supplier_profile(user_id: str, db: Client) -> dict:
    result = db.table("supplier_profiles").select("*").eq("user_id", user_id).maybe_single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Supplier profile not found")
    return result.data


def _mask_company(name: str) -> str:
    """Mask buyer company name until supplier connects.
    "Test Buyer Co" -> "T** Buyer Co". Privacy: full name is sent only after
    a paid connection is created (via /leads/{id}/applications/{app_id}/connect).
    """
    if not name:
        return ""
    parts = str(name).split()
    if not parts or len(parts[0]) <= 1:
        return name
    parts[0] = parts[0][0] + "**"
    return " ".join(parts)


def _get_lead_with_items(lead_id: str, db: Client) -> dict:
    result = db.table("buying_leads").select("*").eq("id", lead_id).maybe_single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead = result.data
    lead["items"] = db.table("buying_lead_items").select("*").eq("lead_id", lead_id).order("sort_order").execute().data
    return lead


# ── Buyer: manage leads ───────────────────────────────────────────────────────

@router.post("", response_model=BuyingLeadResponse, status_code=201)
async def create_lead(
    payload: BuyingLeadCreate,
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    now = datetime.now(timezone.utc).isoformat()

    lead_result = db.table("buying_leads").insert({
        "buyer_id": profile["id"],
        "title": payload.title,
        "notes": payload.notes,
        "status": "active",
        "expires_at": payload.expires_at.isoformat(),
        "created_at": now,
        "updated_at": now,
    }).execute()
    lead_id = lead_result.data[0]["id"]

    if payload.items:
        db.table("buying_lead_items").insert([
            {"lead_id": lead_id, **item.model_dump()} for item in payload.items
        ]).execute()

    return _get_lead_with_items(lead_id, db)


@router.get("/me", response_model=List[BuyingLeadResponse])
async def get_my_leads(
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    leads = (
        db.table("buying_leads")
        .select("*")
        .eq("buyer_id", profile["id"])
        .order("created_at", desc=True)
        .execute().data
    )
    for lead in leads:
        lead["items"] = db.table("buying_lead_items").select("*").eq("lead_id", lead["id"]).order("sort_order").execute().data
    return leads


@router.get("/browse", response_model=List[BuyingLeadResponse])
async def browse_active_leads(
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    """Suppliers browse open buying leads."""
    leads = (
        db.table("buying_leads")
        .select("*")
        .eq("status", "active")
        .order("created_at", desc=True)
        .execute().data
    )
    for lead in leads:
        lead["items"] = db.table("buying_lead_items").select("*").eq("lead_id", lead["id"]).order("sort_order").execute().data
        try:
            profile = db.table("buyer_profiles").select("company_name,country,positioning,business_nature").eq("id", lead["buyer_id"]).maybe_single().execute()
            if profile.data:
                lead["buyer_company"] = _mask_company(profile.data.get("company_name"))
                lead["buyer_country"] = profile.data.get("country")
                lead["buyer_positioning"] = profile.data.get("positioning") or []
                lead["buyer_type"] = profile.data.get("business_nature")
        except Exception:
            pass
    return leads


@router.get("/my-applications", response_model=List[str])
async def get_my_applied_lead_ids(
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    """Return lead_ids the current supplier has already applied to."""
    profile = _require_supplier_profile(current_user["id"], db)
    apps = db.table("lead_applications").select("lead_id").eq("supplier_id", profile["id"]).execute()
    return [str(a["lead_id"]) for a in (apps.data or [])]


@router.get("/{lead_id}", response_model=BuyingLeadResponse)
async def get_lead(
    lead_id: uuid.UUID,
    current_user: dict = Depends(require_role("buyer", "supplier", "admin")),
    db: Client = Depends(get_db),
):
    return _get_lead_with_items(str(lead_id), db)


@router.put("/{lead_id}", response_model=BuyingLeadResponse)
async def update_lead(
    lead_id: uuid.UUID,
    payload: BuyingLeadUpdate,
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    lead = _get_lead_with_items(str(lead_id), db)
    if lead["buyer_id"] != profile["id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    update_data = payload.model_dump(exclude_none=True)
    if "expires_at" in update_data:
        update_data["expires_at"] = update_data["expires_at"].isoformat()
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    db.table("buying_leads").update(update_data).eq("id", str(lead_id)).execute()
    return _get_lead_with_items(str(lead_id), db)


@router.delete("/{lead_id}", status_code=204)
async def cancel_lead(
    lead_id: uuid.UUID,
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    lead = _get_lead_with_items(str(lead_id), db)
    if lead["buyer_id"] != profile["id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    db.table("buying_leads").update({
        "status": "cancelled",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }).eq("id", str(lead_id)).execute()


# ── Supplier: apply to leads ──────────────────────────────────────────────────

@router.post("/{lead_id}/apply", response_model=ApplicationResponse, status_code=201)
async def apply_to_lead(
    lead_id: uuid.UUID,
    payload: ApplicationCreate,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    lead = _get_lead_with_items(str(lead_id), db)

    if lead["status"] != "active":
        raise HTTPException(status_code=400, detail="Lead is not active")

    # Prevent duplicate applications
    existing = (
        db.table("lead_applications")
        .select("id")
        .eq("lead_id", str(lead_id))
        .eq("supplier_id", profile["id"])
        .execute()
    )
    if existing.data:
        raise HTTPException(status_code=400, detail="Already applied to this lead")

    # Check available credits
    credits = db.table("credits").select("*").eq("supplier_id", profile["id"]).maybe_single().execute()
    if not credits.data or (credits.data["balance"] - credits.data["reserved"]) < 1:
        raise HTTPException(status_code=402, detail="Insufficient credits — please top up")

    now = datetime.now(timezone.utc).isoformat()

    # Insert credit_transactions (reserved)
    new_balance_after = credits.data["balance"] - credits.data["reserved"] - 1
    tx_result = db.table("credit_transactions").insert({
        "supplier_id": profile["id"],
        "type": "reserved",
        "amount": -1,
        "balance_after": new_balance_after,
        "notes": f"Reserved for lead {str(lead_id)}",
        "created_at": now,
    }).execute()
    tx_id = tx_result.data[0]["id"]

    # Update credits.reserved
    db.table("credits").update({
        "reserved": credits.data["reserved"] + 1,
        "updated_at": now,
    }).eq("supplier_id", profile["id"]).execute()

    # Insert application
    app_result = db.table("lead_applications").insert({
        "lead_id": str(lead_id),
        "supplier_id": profile["id"],
        "message": payload.message,
        "reference_urls": payload.reference_urls,
        "credit_transaction_id": tx_id,
        "credit_status": "reserved",
        "status": "pending",
        "applied_at": now,
        "updated_at": now,
    }).execute()

    # Back-link the application to the transaction
    db.table("credit_transactions").update({
        "lead_application_id": app_result.data[0]["id"]
    }).eq("id", tx_id).execute()

    return app_result.data[0]


# ── Buyer: view and accept applications ───────────────────────────────────────

@router.get("/{lead_id}/applications", response_model=List[ApplicationResponse])
async def get_lead_applications(
    lead_id: uuid.UUID,
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    lead = _get_lead_with_items(str(lead_id), db)
    if lead["buyer_id"] != profile["id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    applications = (
        db.table("lead_applications")
        .select("*")
        .eq("lead_id", str(lead_id))
        .order("applied_at")
        .execute().data
    )

    # Mark unviewed as viewed
    unviewed = [a["id"] for a in applications if a["status"] == "pending"]
    if unviewed:
        db.table("lead_applications").update({
            "status": "viewed",
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }).in_("id", unviewed).execute()

    return applications


@router.post("/{lead_id}/applications/{app_id}/connect", response_model=ConnectionResponse, status_code=201)
async def connect_with_supplier(
    lead_id: uuid.UUID,
    app_id: uuid.UUID,
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    """Buyer accepts an application → creates a connection and deducts the credit."""
    buyer_profile = _require_buyer_profile(current_user["id"], db)
    lead = _get_lead_with_items(str(lead_id), db)
    if lead["buyer_id"] != buyer_profile["id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    app = db.table("lead_applications").select("*").eq("id", str(app_id)).eq("lead_id", str(lead_id)).maybe_single().execute()
    if not app.data:
        raise HTTPException(status_code=404, detail="Application not found")
    if app.data["status"] in ("connected", "expired"):
        raise HTTPException(status_code=400, detail=f"Application is already {app.data['status']}")

    supplier_id = app.data["supplier_id"]
    now = datetime.now(timezone.utc).isoformat()

    # Check for existing connection
    existing_conn = (
        db.table("connections")
        .select("id")
        .eq("supplier_id", supplier_id)
        .eq("buyer_id", buyer_profile["id"])
        .execute()
    )
    if existing_conn.data:
        raise HTTPException(status_code=400, detail="Connection already exists")

    # Get credits to compute balance_after
    credits = db.table("credits").select("*").eq("supplier_id", supplier_id).maybe_single().execute()
    if not credits.data:
        raise HTTPException(status_code=400, detail="Supplier credits account not found")

    # Insert deducted credit_transactions record
    tx_result = db.table("credit_transactions").insert({
        "supplier_id": supplier_id,
        "type": "deducted",
        "amount": -1,
        "balance_after": credits.data["balance"] - 1,
        "lead_application_id": str(app_id),
        "notes": f"Connection confirmed for lead {str(lead_id)}",
        "created_at": now,
    }).execute()
    tx_id = tx_result.data[0]["id"]

    # Create connection
    conn_result = db.table("connections").insert({
        "supplier_id": supplier_id,
        "buyer_id": buyer_profile["id"],
        "source": "lead_application",
        "source_application_id": str(app_id),
        "credit_transaction_id": tx_id,
        "confirmed_by": "buyer",
        "confirmed_at": now,
        "created_at": now,
    }).execute()
    conn_id = conn_result.data[0]["id"]

    # Back-link connection to transaction
    db.table("credit_transactions").update({"connection_id": conn_id}).eq("id", tx_id).execute()

    # Update credits: reserved -1, balance -1, total_used +1
    db.table("credits").update({
        "balance": credits.data["balance"] - 1,
        "reserved": credits.data["reserved"] - 1,
        "total_used": credits.data["total_used"] + 1,
        "updated_at": now,
    }).eq("supplier_id", supplier_id).execute()

    # Update application status
    db.table("lead_applications").update({
        "status": "connected",
        "credit_status": "deducted",
        "updated_at": now,
    }).eq("id", str(app_id)).execute()

    # System message to kick off the chat
    db.table("messages").insert({
        "connection_id": conn_id,
        "sender_id": current_user["id"],
        "content": "You are now connected. Say hello!",
        "message_type": "system",
        "is_system": True,
        "created_at": now,
    }).execute()

    return conn_result.data[0]
