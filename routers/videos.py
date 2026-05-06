from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from datetime import datetime, timezone
from typing import List
import uuid

from database import get_db, require_role
from models.video import (
    VideoResponse, VideoMaterialCreate, VideoMaterialResponse,
    VideoRevisionRequest, AdminVideoUpdate,
)

router = APIRouter()


def _require_supplier_profile(user_id: str, db: Client) -> dict:
    result = db.table("supplier_profiles").select("*").eq("user_id", user_id).maybe_single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Supplier profile not found")
    return result.data


def _get_video_with_details(video_id: str, db: Client) -> dict:
    result = db.table("videos").select("*").eq("id", video_id).maybe_single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Video not found")
    video = result.data
    mat = db.table("video_materials").select("*").eq("video_id", video_id).maybe_single().execute()
    video["materials"] = mat.data
    pts = db.table("video_selling_points").select("*").eq("video_id", video_id).order("sort_order").execute()
    video["selling_points"] = pts.data
    return video


# ── Supplier ──────────────────────────────────────────────────────────────────

@router.get("/me", response_model=List[VideoResponse])
async def get_my_videos(
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    videos = db.table("videos").select("*").eq("supplier_id", profile["id"]).order("created_at", desc=True).execute().data
    for v in videos:
        mat = db.table("video_materials").select("*").eq("video_id", v["id"]).maybe_single().execute()
        v["materials"] = mat.data
        pts = db.table("video_selling_points").select("*").eq("video_id", v["id"]).order("sort_order").execute()
        v["selling_points"] = pts.data
    return videos


@router.post("/me/materials", response_model=VideoResponse, status_code=201)
async def submit_materials(
    payload: VideoMaterialCreate,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    """Submit production materials for a new video or resubmit for revision."""
    profile = _require_supplier_profile(current_user["id"], db)
    now = datetime.now(timezone.utc).isoformat()

    # Find an existing video in a submittable state, or create one
    existing = (
        db.table("videos")
        .select("*")
        .eq("supplier_id", profile["id"])
        .in_("status", ["none", "revision_requested"])
        .maybe_single()
        .execute()
    )

    if existing.data:
        video_id = existing.data["id"]
        db.table("videos").update({
            "status": "materials_submitted",
            "materials_submitted_at": now,
            "updated_at": now,
        }).eq("id", video_id).execute()
    else:
        video_result = db.table("videos").insert({
            "supplier_id": profile["id"],
            "status": "materials_submitted",
            "materials_submitted_at": now,
            "created_at": now,
            "updated_at": now,
        }).execute()
        video_id = video_result.data[0]["id"]

    selling_points = payload.selling_points or []
    mat_data = payload.model_dump(exclude={"selling_points"})
    mat_data.update({"video_id": video_id, "supplier_id": profile["id"], "submitted_at": now})

    # Replace existing material record if present
    db.table("video_materials").delete().eq("video_id", video_id).execute()
    db.table("video_materials").insert(mat_data).execute()

    # Replace selling points
    db.table("video_selling_points").delete().eq("video_id", video_id).execute()
    if selling_points:
        db.table("video_selling_points").insert([
            {"video_id": video_id, **sp.model_dump()} for sp in selling_points
        ]).execute()

    return _get_video_with_details(video_id, db)


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: uuid.UUID,
    current_user: dict = Depends(require_role("supplier", "admin")),
    db: Client = Depends(get_db),
):
    video = _get_video_with_details(str(video_id), db)

    # Suppliers can only view their own videos
    if current_user["role"] == "supplier":
        profile = _require_supplier_profile(current_user["id"], db)
        if video["supplier_id"] != profile["id"]:
            raise HTTPException(status_code=403, detail="Access denied")

    return video


@router.post("/{video_id}/approve", response_model=VideoResponse)
async def approve_draft(
    video_id: uuid.UUID,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    video = _get_video_with_details(str(video_id), db)

    if video["supplier_id"] != profile["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    if video["status"] != "draft_ready":
        raise HTTPException(status_code=400, detail="Video is not in draft_ready status")

    now = datetime.now(timezone.utc).isoformat()
    db.table("videos").update({
        "supplier_approved": True,
        "supplier_approved_at": now,
        "updated_at": now,
    }).eq("id", str(video_id)).execute()
    return _get_video_with_details(str(video_id), db)


@router.post("/{video_id}/revision", response_model=VideoResponse)
async def request_revision(
    video_id: uuid.UUID,
    payload: VideoRevisionRequest,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    video = _get_video_with_details(str(video_id), db)

    if video["supplier_id"] != profile["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    if video["status"] != "draft_ready":
        raise HTTPException(status_code=400, detail="Video is not in draft_ready status")
    if video["revision_count"] >= 1:
        raise HTTPException(status_code=400, detail="Revision limit reached (max 1)")

    now = datetime.now(timezone.utc).isoformat()
    db.table("videos").update({
        "status": "revision_requested",
        "revision_notes": payload.revision_notes,
        "revision_count": video["revision_count"] + 1,
        "updated_at": now,
    }).eq("id", str(video_id)).execute()
    return _get_video_with_details(str(video_id), db)


# ── Admin ─────────────────────────────────────────────────────────────────────

@router.get("/admin/all", response_model=List[VideoResponse])
async def admin_list_videos(
    status_filter: str = None,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    query = db.table("videos").select("*")
    if status_filter:
        query = query.eq("status", status_filter)
    videos = query.order("updated_at", desc=True).execute().data
    for v in videos:
        mat = db.table("video_materials").select("*").eq("video_id", v["id"]).maybe_single().execute()
        v["materials"] = mat.data
        pts = db.table("video_selling_points").select("*").eq("video_id", v["id"]).order("sort_order").execute()
        v["selling_points"] = pts.data
    return videos


@router.put("/admin/{video_id}", response_model=VideoResponse)
async def admin_update_video(
    video_id: uuid.UUID,
    payload: AdminVideoUpdate,
    current_user: dict = Depends(require_role("admin")),
    db: Client = Depends(get_db),
):
    now = datetime.now(timezone.utc).isoformat()
    update_data = payload.model_dump(exclude_none=True)
    update_data["updated_at"] = now

    if payload.status == "published":
        update_data.setdefault("published_at", now)
    elif payload.status == "draft_ready":
        update_data.setdefault("draft_ready_at", now)

    result = db.table("videos").update(update_data).eq("id", str(video_id)).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Video not found")
    return _get_video_with_details(str(video_id), db)
