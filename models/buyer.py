from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class BuyerMOQCreate(BaseModel):
    category: str
    quantity: Optional[int] = None
    unit: str = "pcs"


class BuyerMOQResponse(BuyerMOQCreate):
    id: uuid.UUID
    buyer_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class BuyerMarketCreate(BaseModel):
    region: str


class BuyerMarketResponse(BuyerMarketCreate):
    id: uuid.UUID
    buyer_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class BuyerProfileCreate(BaseModel):
    title: Optional[str] = None
    given_name: Optional[str] = None
    surname: Optional[str] = None
    company_name: Optional[str] = None
    business_nature: Optional[str] = None
    website: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    office_address: Optional[str] = None
    annual_volume: Optional[str] = None
    main_products: Optional[str] = None
    positioning: Optional[List[str]] = None


class BuyerProfileUpdate(BuyerProfileCreate):
    pass


class BuyerProfileResponse(BuyerProfileCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    elfa_verified: bool
    verified_at: Optional[datetime] = None
    from_lead_form: bool
    profile_complete: bool
    created_at: datetime
    updated_at: datetime
    moqs: Optional[List[BuyerMOQResponse]] = None
    markets: Optional[List[BuyerMarketResponse]] = None

    model_config = {"from_attributes": True}


class BuyerRequestCreate(BaseModel):
    supplier_id: uuid.UUID
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    business_nature: Optional[str] = None
    country: Optional[str] = None
    target_market: Optional[str] = None
    email: str
    phone: str
    whatsapp: str
    website: Optional[str] = None
    annual_volume: Optional[str] = None
    main_products: Optional[str] = None
    positioning: Optional[List[str]] = None
    message: Optional[str] = None
    source: str = "lead_form"


class BuyerRequestResponse(BaseModel):
    id: uuid.UUID
    buyer_id: Optional[uuid.UUID] = None
    supplier_id: uuid.UUID
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    business_nature: Optional[str] = None
    country: Optional[str] = None
    target_market: Optional[str] = None
    email: str
    phone: str
    whatsapp: str
    website: Optional[str] = None
    annual_volume: Optional[str] = None
    main_products: Optional[str] = None
    positioning: Optional[List[str]] = None
    message: Optional[str] = None
    source: str
    status: str
    created_at: datetime
    updated_at: datetime
    expires_at: datetime

    model_config = {"from_attributes": True}
