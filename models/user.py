from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime
import uuid


class UserRole(str, Enum):
    supplier = "supplier"
    buyer = "buyer"
    admin = "admin"


class UserStatus(str, Enum):
    active = "active"
    pending = "pending"
    suspended = "suspended"


class AuthProvider(str, Enum):
    email = "email"
    google = "google"
    apple = "apple"


class UserBase(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    role: UserRole
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    id: uuid.UUID
    status: UserStatus
    auth_provider: AuthProvider
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
