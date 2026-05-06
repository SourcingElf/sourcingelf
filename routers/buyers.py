from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from datetime import datetime, timezone
from typing import List
import uuid

from database import get_db, get_current_user, require_role
from models.buyer import (
    BuyerProfileCreate, BuyerProfileUpdate, BuyerProfileResponse,
    BuyerMOQCreate, BuyerMOQResponse,
    BuyerMarketCreate, BuyerMarketResponse,
    BuyerRequestCreate, BuyerRequestResponse,
)

router = APIRouter()


def _require_buyer_profile(user_id: str, db: Client) -> dict:
    result = db.table("buyer_profiles").select("*").eq("user_id", user_id).maybe_single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Buyer profile not found")
    return result.data


# ── Profile ──────────────────────────────────────────────────────────────────

@router.get("/me/profile", response_model=BuyerProfileResponse)
async def get_my_profile(
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    bid = profile["id"]
    profile["moqs"]    = db.table("buyer_moqs").select("*").eq("buyer_id", bid).execute().data
    profile["markets"] = db.table("buyer_markets").select("*").eq("buyer_id", bid).execute().data
    return profile


@router.post("/me/profile", response_model=BuyerProfileResponse, status_code=201)
async def create_my_profile(
    payload: BuyerProfileCreate,
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    if db.table("buyer_profiles").select("id").eq("user_id", current_user["id"]).execute().data:
        raise HTTPException(status_code=400, detail="Profile already exists")
    now = datetime.now(timezone.utc).isoformat()
    result = db.table("buyer_profiles").insert({
        **payload.model_dump(),
        "user_id": current_user["id"],
        "created_at": now,
        "updated_at": now,
    }).execute()
    return result.data[0]


@router.put("/me/profile", response_model=BuyerProfileResponse)
async def update_my_profile(
    payload: BuyerProfileUpdate,
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    update_data = payload.model_dump(exclude_none=True)
    if not update_data:
        return profile
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    result = db.table("buyer_profiles").update(update_data).eq("id", profile["id"]).execute()
    return result.data[0]


# ── MOQs ─────────────────────────────────────────────────────────────────────

@router.post("/me/moqs", response_model=BuyerMOQResponse, status_code=201)
async def add_moq(
    payload: BuyerMOQCreate,
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    result = db.table("buyer_moqs").insert({**payload.model_dump(), "buyer_id": profile["id"]}).execute()
    return result.data[0]


@router.put("/me/moqs/{moq_id}", response_model=BuyerMOQResponse)
async def update_moq(
    moq_id: uuid.UUID,
    payload: BuyerMOQCreate,
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    result = (
        db.table("buyer_moqs")
        .update(payload.model_dump())
        .eq("id", str(moq_id))
        .eq("buyer_id", profile["id"])
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="MOQ not found")
    return result.data[0]


@router.delete("/me/moqs/{moq_id}", status_code=204)
async def delete_moq(
    moq_id: uuid.UUID,
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    db.table("buyer_moqs").delete().eq("id", str(moq_id)).eq("buyer_id", profile["id"]).execute()


# ── Markets ──────────────────────────────────────────────────────────────────

@router.post("/me/markets", response_model=BuyerMarketResponse, status_code=201)
async def add_market(
    payload: BuyerMarketCreate,
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    result = db.table("buyer_markets").insert({**payload.model_dump(), "buyer_id": profile["id"]}).execute()
    return result.data[0]


@router.delete("/me/markets/{market_id}", status_code=204)
async def delete_market(
    market_id: uuid.UUID,
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    db.table("buyer_markets").delete().eq("id", str(market_id)).eq("buyer_id", profile["id"]).execute()


# ── Buyer Requests (Lead Form) ────────────────────────────────────────────────

@router.post("/requests", response_model=BuyerRequestResponse, status_code=201)
async def submit_buyer_request(
    payload: BuyerRequestCreate,
    db: Client = Depends(get_db),
):
    """
    Public endpoint — no auth required.
    Used by the lead form on a supplier's promo video page.
    """
    supplier_check = db.table("supplier_profiles").select("id").eq("id", str(payload.supplier_id)).execute()
    if not supplier_check.data:
        raise HTTPException(status_code=404, detail="Supplier not found")

    now = datetime.now(timezone.utc).isoformat()
    result = db.table("buyer_requests").insert({
        **payload.model_dump(),
        "supplier_id": str(payload.supplier_id),
        "status": "pending",
        "created_at": now,
        "updated_at": now,
    }).execute()
    return result.data[0]


@router.get("/me/requests", response_model=List[BuyerRequestResponse])
async def get_my_requests(
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    result = (
        db.table("buyer_requests")
        .select("*")
        .eq("buyer_id", profile["id"])
        .order("created_at", desc=True)
        .execute()
    )
    return result.data


@router.get("/me/connected-suppliers")
async def get_connected_suppliers(
    current_user: dict = Depends(require_role("buyer")),
    db: Client = Depends(get_db),
):
    profile = _require_buyer_profile(current_user["id"], db)
    connections = (
        db.table("connections")
        .select("*")
        .eq("buyer_id", profile["id"])
        .order("confirmed_at", desc=True)
        .execute().data
    )
    result = []
    for conn in connections:
        sp = db.table("supplier_profiles").select("*").eq("id", conn["supplier_id"]).maybe_single().execute()
        if sp.data:
            result.append({
                "connection_id": conn["id"],
                "confirmed_at": conn["confirmed_at"],
                "source": conn["source"],
                "supplier_id": sp.data["id"],
                "company_name": sp.data.get("company_name"),
                "country": sp.data.get("country"),
                "main_products": sp.data.get("main_products"),
                "given_name": sp.data.get("given_name"),
                "surname": sp.data.get("surname"),
            })
    return result
