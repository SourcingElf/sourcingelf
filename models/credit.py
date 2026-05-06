from pydantic import BaseModel, computed_field
from typing import Optional
from enum import Enum
from datetime import datetime
import uuid


class PackageType(str, Enum):
    single = "single"
    triple = "triple"
    five_pack = "five_pack"


PACKAGE_CONFIG: dict[PackageType, dict] = {
    PackageType.single:    {"credits": 1, "price_usd": 138.00},
    PackageType.triple:    {"credits": 3, "price_usd": 368.00},
    PackageType.five_pack: {"credits": 5, "price_usd": 498.00},
}


class TransactionType(str, Enum):
    topup = "topup"
    reserved = "reserved"
    deducted = "deducted"
    refunded = "refunded"
    manual_add = "manual_add"
    manual_deduct = "manual_deduct"


class CreditsResponse(BaseModel):
    id: uuid.UUID
    supplier_id: uuid.UUID
    balance: int
    reserved: int
    total_purchased: int
    total_used: int
    updated_at: datetime

    @computed_field
    @property
    def available(self) -> int:
        return self.balance - self.reserved

    model_config = {"from_attributes": True}


class CreditTransactionResponse(BaseModel):
    id: uuid.UUID
    supplier_id: uuid.UUID
    type: TransactionType
    amount: int
    balance_after: int
    payment_id: Optional[uuid.UUID] = None
    connection_id: Optional[uuid.UUID] = None
    lead_application_id: Optional[uuid.UUID] = None
    notes: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PaymentResponse(BaseModel):
    id: uuid.UUID
    supplier_id: uuid.UUID
    stripe_payment_id: str
    package_type: PackageType
    credits_purchased: int
    amount_usd: float
    status: str
    paid_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class CheckoutCreate(BaseModel):
    package_type: PackageType


class CheckoutResponse(BaseModel):
    checkout_url: str
    payment_id: uuid.UUID


class AdminCreditAdjust(BaseModel):
    supplier_id: uuid.UUID
    amount: int  # positive = add, negative = deduct
    notes: str
