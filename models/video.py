from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime
import uuid


class VideoStatus(str, Enum):
    none = "none"
    materials_submitted = "materials_submitted"
    in_production = "in_production"
    draft_ready = "draft_ready"
    revision_requested = "revision_requested"
    published = "published"
    unpublished = "unpublished"


class SellingPointCreate(BaseModel):
    description: str
    sort_order: int = 0


class SellingPointResponse(SellingPointCreate):
    id: uuid.UUID
    video_id: uuid.UUID

    model_config = {"from_attributes": True}


class VideoMaterialCreate(BaseModel):
    main_products_desc: Optional[str] = None
    additional_notes: Optional[str] = None
    target_positioning: Optional[List[str]] = None
    target_buyer_nature: Optional[List[str]] = None
    min_order_qty: Optional[int] = None
    min_order_unit: str = "pcs"
    photo_urls: Optional[List[str]] = None
    video_urls: Optional[List[str]] = None
    selling_points: Optional[List[SellingPointCreate]] = None


class VideoMaterialResponse(BaseModel):
    id: uuid.UUID
    video_id: uuid.UUID
    supplier_id: uuid.UUID
    main_products_desc: Optional[str] = None
    additional_notes: Optional[str] = None
    target_positioning: Optional[List[str]] = None
    target_buyer_nature: Optional[List[str]] = None
    min_order_qty: Optional[int] = None
    min_order_unit: str
    photo_urls: Optional[List[str]] = None
    video_urls: Optional[List[str]] = None
    submitted_at: datetime

    model_config = {"from_attributes": True}


class VideoResponse(BaseModel):
    id: uuid.UUID
    supplier_id: uuid.UUID
    file_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_sec: Optional[int] = None
    file_size_mb: Optional[float] = None
    status: VideoStatus
    materials_submitted_at: Optional[datetime] = None
    draft_ready_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    revision_count: int
    revision_notes: Optional[str] = None
    supplier_approved: bool
    supplier_approved_at: Optional[datetime] = None
    admin_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    materials: Optional[VideoMaterialResponse] = None
    selling_points: Optional[List[SellingPointResponse]] = None

    model_config = {"from_attributes": True}


class VideoRevisionRequest(BaseModel):
    revision_notes: str


class AdminVideoUpdate(BaseModel):
    status: VideoStatus
    file_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_sec: Optional[int] = None
    file_size_mb: Optional[float] = None
    admin_notes: Optional[str] = None
