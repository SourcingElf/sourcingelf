from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from datetime import datetime, timezone
from typing import List
import uuid

from database import get_db, require_role
from models.supplier import (
    SupplierProfileCreate, SupplierProfileUpdate, SupplierProfileResponse,
    FactoryCreate, FactoryResponse,
    MOQCreate, MOQResponse,
    CertificationCreate, CertificationResponse,
    StrengthCreate, StrengthResponse,
    MarketCreate, MarketResponse,
)

router = APIRouter()


def _require_supplier_profile(user_id: str, db: Client) -> dict:
    result = db.table("supplier_profiles").select("*").eq("user_id", user_id).maybe_single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Supplier profile not found")
    return result.data


# ── Profile ──────────────────────────────────────────────────────────────────

@router.get("/me/profile", response_model=SupplierProfileResponse)
async def get_my_profile(
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    sid = profile["id"]
    profile["factories"]     = db.table("supplier_factories").select("*").eq("supplier_id", sid).order("sort_order").execute().data
    profile["moqs"]          = db.table("supplier_moqs").select("*").eq("supplier_id", sid).execute().data
    profile["certifications"] = db.table("supplier_certifications").select("*").eq("supplier_id", sid).execute().data
    profile["strengths"]     = db.table("supplier_strengths").select("*").eq("supplier_id", sid).order("sort_order").execute().data
    profile["markets"]       = db.table("supplier_markets").select("*").eq("supplier_id", sid).execute().data
    return profile


@router.post("/me/profile", response_model=SupplierProfileResponse, status_code=201)
async def create_my_profile(
    payload: SupplierProfileCreate,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    if db.table("supplier_profiles").select("id").eq("user_id", current_user["id"]).execute().data:
        raise HTTPException(status_code=400, detail="Profile already exists")
    now = datetime.now(timezone.utc).isoformat()
    result = db.table("supplier_profiles").insert({
        **payload.model_dump(),
        "user_id": current_user["id"],
        "created_at": now,
        "updated_at": now,
    }).execute()
    return result.data[0]


@router.put("/me/profile", response_model=SupplierProfileResponse)
async def update_my_profile(
    payload: SupplierProfileUpdate,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    update_data = payload.model_dump(exclude_none=True)
    if not update_data:
        return profile
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    result = db.table("supplier_profiles").update(update_data).eq("id", profile["id"]).execute()
    return result.data[0]


# ── Factories ────────────────────────────────────────────────────────────────

@router.post("/me/factories", response_model=FactoryResponse, status_code=201)
async def add_factory(
    payload: FactoryCreate,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    result = db.table("supplier_factories").insert({**payload.model_dump(), "supplier_id": profile["id"]}).execute()
    return result.data[0]


@router.put("/me/factories/{factory_id}", response_model=FactoryResponse)
async def update_factory(
    factory_id: uuid.UUID,
    payload: FactoryCreate,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    result = (
        db.table("supplier_factories")
        .update(payload.model_dump())
        .eq("id", str(factory_id))
        .eq("supplier_id", profile["id"])
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Factory not found")
    return result.data[0]


@router.delete("/me/factories/{factory_id}", status_code=204)
async def delete_factory(
    factory_id: uuid.UUID,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    db.table("supplier_factories").delete().eq("id", str(factory_id)).eq("supplier_id", profile["id"]).execute()


# ── MOQs ─────────────────────────────────────────────────────────────────────

@router.post("/me/moqs", response_model=MOQResponse, status_code=201)
async def add_moq(
    payload: MOQCreate,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    result = db.table("supplier_moqs").insert({**payload.model_dump(), "supplier_id": profile["id"]}).execute()
    return result.data[0]


@router.put("/me/moqs/{moq_id}", response_model=MOQResponse)
async def update_moq(
    moq_id: uuid.UUID,
    payload: MOQCreate,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    result = (
        db.table("supplier_moqs")
        .update(payload.model_dump())
        .eq("id", str(moq_id))
        .eq("supplier_id", profile["id"])
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="MOQ not found")
    return result.data[0]


@router.delete("/me/moqs/{moq_id}", status_code=204)
async def delete_moq(
    moq_id: uuid.UUID,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    db.table("supplier_moqs").delete().eq("id", str(moq_id)).eq("supplier_id", profile["id"]).execute()


# ── Certifications ───────────────────────────────────────────────────────────

@router.post("/me/certifications", response_model=CertificationResponse, status_code=201)
async def add_certification(
    payload: CertificationCreate,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    result = db.table("supplier_certifications").insert({**payload.model_dump(), "supplier_id": profile["id"]}).execute()
    return result.data[0]


@router.delete("/me/certifications/{cert_id}", status_code=204)
async def delete_certification(
    cert_id: uuid.UUID,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    db.table("supplier_certifications").delete().eq("id", str(cert_id)).eq("supplier_id", profile["id"]).execute()


# ── Strengths ────────────────────────────────────────────────────────────────

@router.post("/me/strengths", response_model=StrengthResponse, status_code=201)
async def add_strength(
    payload: StrengthCreate,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    result = db.table("supplier_strengths").insert({**payload.model_dump(), "supplier_id": profile["id"]}).execute()
    return result.data[0]


@router.delete("/me/strengths/{strength_id}", status_code=204)
async def delete_strength(
    strength_id: uuid.UUID,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    db.table("supplier_strengths").delete().eq("id", str(strength_id)).eq("supplier_id", profile["id"]).execute()


# ── Markets ──────────────────────────────────────────────────────────────────

@router.post("/me/markets", response_model=MarketResponse, status_code=201)
async def add_market(
    payload: MarketCreate,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    result = db.table("supplier_markets").insert({**payload.model_dump(), "supplier_id": profile["id"]}).execute()
    return result.data[0]


@router.delete("/me/markets/{market_id}", status_code=204)
async def delete_market(
    market_id: uuid.UUID,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    db.table("supplier_markets").delete().eq("id", str(market_id)).eq("supplier_id", profile["id"]).execute()


# ── Buyer Requests received by this supplier ─────────────────────────────────

@router.get("/me/buyer-requests")
async def get_my_buyer_requests(
    status: str = None,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    """Supplier views buyer requests they have received."""
    profile = _require_supplier_profile(current_user["id"], db)
    query = db.table("buyer_requests").select("*").eq("supplier_id", profile["id"])
    if status:
        query = query.eq("status", status)
    result = query.order("created_at", desc=True).execute()
    return result.data


# ── Connected Buyers ─────────────────────────────────────────────────────────

@router.get("/me/connected-buyers")
async def get_connected_buyers(
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    connections = (
        db.table("connections")
        .select("*")
        .eq("supplier_id", profile["id"])
        .order("confirmed_at", desc=True)
        .execute().data
    )
    result = []
    for conn in connections:
        buyer = db.table("buyer_profiles").select("*").eq("id", conn["buyer_id"]).maybe_single().execute()
        if buyer.data:
            bp = buyer.data
            result.append({
                "connection_id": conn["id"],
                "confirmed_at": conn["confirmed_at"],
                "source": conn["source"],
                "buyer_id": bp["id"],
                "company_name": bp["company_name"],
                "business_nature": bp["business_nature"],
                "country": bp["country"],
                "main_products": bp["main_products"],
                "annual_volume": bp["annual_volume"],
                "given_name": bp["given_name"],
                "surname": bp["surname"],
            })
    return result
