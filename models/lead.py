from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime
import uuid


class LeadStatus(str, Enum):
    draft = "draft"
    active = "active"
    expired = "expired"
    cancelled = "cancelled"


class ApplicationStatus(str, Enum):
    pending = "pending"
    viewed = "viewed"
    connected = "connected"
    rejected = "rejected"
    expired = "expired"


class CreditStatus(str, Enum):
    reserved = "reserved"
    deducted = "deducted"
    refunded = "refunded"


class ConnectionSource(str, Enum):
    request = "request"
    lead_application = "lead_application"


class LeadItemCreate(BaseModel):
    product_name: str
    description: Optional[str] = None
    quantity: Optional[int] = None
    price_range: Optional[str] = None
    oem_odm: Optional[str] = None
    reference_urls: Optional[List[str]] = None
    sort_order: int = 0


class LeadItemResponse(LeadItemCreate):
    id: uuid.UUID
    lead_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class BuyingLeadCreate(BaseModel):
    title: str
    notes: Optional[str] = None
    expires_at: datetime
    items: List[LeadItemCreate]


class BuyingLeadUpdate(BaseModel):
    title: Optional[str] = None
    notes: Optional[str] = None
    expires_at: Optional[datetime] = None
    status: Optional[LeadStatus] = None


class BuyingLeadResponse(BaseModel):
    id: uuid.UUID
    buyer_id: uuid.UUID
    title: str
    notes: Optional[str] = None
    status: LeadStatus
    expires_at: datetime
    created_at: datetime
    updated_at: datetime
    expired_at: Optional[datetime] = None
    items: Optional[List[LeadItemResponse]] = None
    buyer_company: Optional[str] = None
    buyer_country: Optional[str] = None
    buyer_positioning: Optional[List[str]] = None
    buyer_type: Optional[str] = None

    model_config = {"from_attributes": True}


class ApplicationCreate(BaseModel):
    message: Optional[str] = None
    reference_urls: Optional[List[str]] = None


class ApplicationResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID
    supplier_id: uuid.UUID
    message: Optional[str] = None
    reference_urls: Optional[List[str]] = None
    credit_transaction_id: Optional[uuid.UUID] = None
    credit_status: CreditStatus
    status: ApplicationStatus
    applied_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConnectionResponse(BaseModel):
    id: uuid.UUID
    supplier_id: uuid.UUID
    buyer_id: uuid.UUID
    source: ConnectionSource
    source_request_id: Optional[uuid.UUID] = None
    source_application_id: Optional[uuid.UUID] = None
    confirmed_by: Optional[str] = None
    confirmed_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    content: Optional[str] = None
    image_urls: Optional[List[str]] = None
    message_type: str = "text"


class MessageResponse(BaseModel):
    id: uuid.UUID
    connection_id: uuid.UUID
    sender_id: uuid.UUID
    content: Optional[str] = None
    image_urls: Optional[List[str]] = None
    message_type: str
    is_system: bool
    read_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}
