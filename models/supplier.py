from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class FactoryCreate(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    workers: Optional[int] = None
    monthly_capacity: Optional[str] = None
    sort_order: int = 0


class FactoryResponse(FactoryCreate):
    id: uuid.UUID
    supplier_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class MOQCreate(BaseModel):
    category: str
    quantity: Optional[int] = None
    unit: str = "pcs"


class MOQResponse(MOQCreate):
    id: uuid.UUID
    supplier_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class CertificationCreate(BaseModel):
    name: str
    file_url: Optional[str] = None


class CertificationResponse(CertificationCreate):
    id: uuid.UUID
    supplier_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class StrengthCreate(BaseModel):
    description: str
    sort_order: int = 0


class StrengthResponse(StrengthCreate):
    id: uuid.UUID
    supplier_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class MarketCreate(BaseModel):
    region: str
    share_pct: Optional[int] = None


class MarketResponse(MarketCreate):
    id: uuid.UUID
    supplier_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class SupplierProfileCreate(BaseModel):
    full_name: Optional[str] = None
    company_name: str
    website: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    office_address: Optional[str] = None
    br_file_url: Optional[str] = None
    main_products: Optional[str] = None
    positioning: Optional[List[str]] = None
    client_nature: Optional[List[str]] = None
    main_clients: Optional[str] = None


class SupplierProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    website: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    office_address: Optional[str] = None
    br_file_url: Optional[str] = None
    main_products: Optional[str] = None
    positioning: Optional[List[str]] = None
    client_nature: Optional[List[str]] = None
    main_clients: Optional[str] = None


class SupplierProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    full_name: Optional[str] = None
    company_name: str
    website: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    office_address: Optional[str] = None
    br_file_url: Optional[str] = None
    main_products: Optional[str] = None
    positioning: Optional[List[str]] = None
    client_nature: Optional[List[str]] = None
    main_clients: Optional[str] = None
    profile_complete: bool
    verified: bool
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    factories: Optional[List[FactoryResponse]] = None
    moqs: Optional[List[MOQResponse]] = None
    certifications: Optional[List[CertificationResponse]] = None
    strengths: Optional[List[StrengthResponse]] = None
    markets: Optional[List[MarketResponse]] = None

    model_config = {"from_attributes": True}
