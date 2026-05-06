from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel
import uuid

from database import get_db, require_role
from models.user import UserResponse
from models.supplier import SupplierProfileResponse
from models.buyer import BuyerProfileResponse, BuyerRequestResponse
from models.video import VideoResponse, AdminVideoUpdate
from models.credit import AdminCreditAdjust, CreditTransactionResponse

router = APIRouter()


# ── Users ─────────────────────────────────────────────────────────────────────

@router.get("/users", response_model=List[UserResponse])
async def list_users(
    role: Optional[str] = None,
    status: Optional[str] = None,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    query = db.table("users").select("*")
    if role:
        query = query.eq("role", role)
    if status:
        query = query.eq("status", status)
    return query.order("created_at", desc=True).execute().data


class UserStatusUpdate(BaseModel):
    status: str
    reason: Optional[str] = None


@router.put("/users/{user_id}/status", response_model=UserResponse)
async def update_user_status(
    user_id: uuid.UUID,
    payload: UserStatusUpdate,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    valid_statuses = {"active", "pending", "suspended"}
    if payload.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"status must be one of {valid_statuses}")

    now = datetime.now(timezone.utc).isoformat()
    result = db.table("users").update({
        "status": payload.status,
        "updated_at": now,
    }).eq("id", str(user_id)).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.reason:
        db.table("admin_notes").insert({
            "admin_id": current_user["id"],
            "target_user_id": str(user_id),
            "note": f"Status changed to '{payload.status}': {payload.reason}",
            "created_at": now,
        }).execute()

    return result.data[0]


# ── Suppliers ─────────────────────────────────────────────────────────────────

@router.get("/suppliers", response_model=List[SupplierProfileResponse])
async def list_suppliers(
    verified: Optional[bool] = None,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    query = db.table("supplier_profiles").select("*")
    if verified is not None:
        query = query.eq("verified", verified)
    return query.order("created_at", desc=True).execute().data


class SupplierVerifyPayload(BaseModel):
    verified: bool
    notes: Optional[str] = None


@router.put("/suppliers/{supplier_id}/verify", response_model=SupplierProfileResponse)
async def verify_supplier(
    supplier_id: uuid.UUID,
    payload: SupplierVerifyPayload,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    now = datetime.now(timezone.utc).isoformat()
    update_data: dict = {
        "verified": payload.verified,
        "updated_at": now,
    }
    if payload.verified:
        update_data["verified_at"] = now
        update_data["verified_by"] = current_user["id"]
    if payload.notes:
        update_data["admin_notes"] = payload.notes

    result = db.table("supplier_profiles").update(update_data).eq("id", str(supplier_id)).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Supplier not found")

    db.table("notifications").insert({
        "user_id": result.data[0]["user_id"],
        "type": "supplier_verified" if payload.verified else "supplier_unverified",
        "title": "Profile verified" if payload.verified else "Profile verification removed",
        "body": payload.notes,
        "related_id": str(supplier_id),
        "related_type": "supplier_profile",
        "created_at": now,
    }).execute()

    return result.data[0]


# ── Buyer requests ────────────────────────────────────────────────────────────

@router.get("/buyer-requests", response_model=List[BuyerRequestResponse])
async def list_buyer_requests(
    status: Optional[str] = None,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    query = db.table("buyer_requests").select("*")
    if status:
        query = query.eq("status", status)
    return query.order("created_at", desc=True).execute().data


class BuyerRequestStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None


@router.put("/buyer-requests/{request_id}/status", response_model=BuyerRequestResponse)
async def update_buyer_request_status(
    request_id: uuid.UUID,
    payload: BuyerRequestStatusUpdate,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    now = datetime.now(timezone.utc).isoformat()
    result = db.table("buyer_requests").update({
        "status": payload.status,
        "updated_at": now,
    }).eq("id", str(request_id)).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Request not found")
    return result.data[0]


# ── Buyers ────────────────────────────────────────────────────────────────────

@router.get("/buyers", response_model=List[BuyerProfileResponse])
async def list_buyers(
    elfa_verified: Optional[bool] = None,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    query = db.table("buyer_profiles").select("*")
    if elfa_verified is not None:
        query = query.eq("elfa_verified", elfa_verified)
    return query.order("created_at", desc=True).execute().data


class BuyerVerifyPayload(BaseModel):
    elfa_verified: bool
    notes: Optional[str] = None


@router.put("/buyers/{buyer_id}/verify", response_model=BuyerProfileResponse)
async def verify_buyer(
    buyer_id: uuid.UUID,
    payload: BuyerVerifyPayload,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    now = datetime.now(timezone.utc).isoformat()
    update_data: dict = {
        "elfa_verified": payload.elfa_verified,
        "updated_at": now,
    }
    if payload.elfa_verified:
        update_data["verified_at"] = now
        update_data["verified_by"] = current_user["id"]
    if payload.notes:
        update_data["verification_notes"] = payload.notes

    result = db.table("buyer_profiles").update(update_data).eq("id", str(buyer_id)).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return result.data[0]


# ── Credits ───────────────────────────────────────────────────────────────────

@router.post("/credits/adjust", response_model=CreditTransactionResponse, status_code=201)
async def adjust_credits(
    payload: AdminCreditAdjust,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    if payload.amount == 0:
        raise HTTPException(status_code=400, detail="Amount cannot be zero")

    credits = db.table("credits").select("*").eq("supplier_id", str(payload.supplier_id)).maybe_single().execute()
    if not credits.data:
        raise HTTPException(status_code=404, detail="Supplier credits account not found")

    new_balance = credits.data["balance"] + payload.amount
    if new_balance < 0:
        raise HTTPException(status_code=400, detail="Adjustment would result in negative balance")

    now = datetime.now(timezone.utc).isoformat()
    tx_type = "manual_add" if payload.amount > 0 else "manual_deduct"

    db.table("credits").update({
        "balance": new_balance,
        "updated_at": now,
    }).eq("supplier_id", str(payload.supplier_id)).execute()

    tx_result = db.table("credit_transactions").insert({
        "supplier_id": str(payload.supplier_id),
        "type": tx_type,
        "amount": payload.amount,
        "balance_after": new_balance,
        "notes": payload.notes,
        "created_by": current_user["id"],
        "created_at": now,
    }).execute()

    return tx_result.data[0]


# ── Admin notes ───────────────────────────────────────────────────────────────

class AdminNoteCreate(BaseModel):
    target_user_id: uuid.UUID
    note: str


class AdminNoteResponse(BaseModel):
    id: uuid.UUID
    admin_id: uuid.UUID
    target_user_id: uuid.UUID
    note: str
    created_at: datetime

    model_config = {"from_attributes": True}


@router.post("/notes", response_model=AdminNoteResponse, status_code=201)
async def create_admin_note(
    payload: AdminNoteCreate,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    now = datetime.now(timezone.utc).isoformat()
    result = db.table("admin_notes").insert({
        "admin_id": current_user["id"],
        "target_user_id": str(payload.target_user_id),
        "note": payload.note,
        "created_at": now,
    }).execute()
    return result.data[0]


@router.get("/notes/{user_id}", response_model=List[AdminNoteResponse])
async def get_admin_notes(
    user_id: uuid.UUID,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    return db.table("admin_notes").select("*").eq("target_user_id", str(user_id)).order("created_at", desc=True).execute().data
