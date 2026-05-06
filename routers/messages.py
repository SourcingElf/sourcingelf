from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from datetime import datetime, timezone
from typing import List
import uuid

from database import get_db, get_current_user
from models.lead import MessageCreate, MessageResponse, ConnectionResponse

router = APIRouter()


def _get_connection_for_user(connection_id: str, user_id: str, db: Client) -> dict:
    """Fetch a connection and verify the requesting user is a participant."""
    conn = db.table("connections").select("*").eq("id", connection_id).maybe_single().execute()
    if not conn.data:
        raise HTTPException(status_code=404, detail="Connection not found")

    # Resolve supplier and buyer user IDs to check membership
    supplier = db.table("supplier_profiles").select("user_id").eq("id", conn.data["supplier_id"]).maybe_single().execute()
    buyer = db.table("buyer_profiles").select("user_id").eq("id", conn.data["buyer_id"]).maybe_single().execute()

    allowed = {
        supplier.data["user_id"] if supplier.data else None,
        buyer.data["user_id"] if buyer.data else None,
    }
    if user_id not in allowed:
        raise HTTPException(status_code=403, detail="Access denied")

    return conn.data


# ── Connections list ──────────────────────────────────────────────────────────

@router.get("/connections", response_model=List[ConnectionResponse])
async def list_my_connections(
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db),
):
    """Return all connections the current user participates in."""
    user_id = current_user["id"]
    role = current_user["role"]

    if role == "supplier":
        profile = db.table("supplier_profiles").select("id").eq("user_id", user_id).maybe_single().execute()
        if not profile.data:
            return []
        connections = db.table("connections").select("*").eq("supplier_id", profile.data["id"]).order("created_at", desc=True).execute().data

    elif role == "buyer":
        profile = db.table("buyer_profiles").select("id").eq("user_id", user_id).maybe_single().execute()
        if not profile.data:
            return []
        connections = db.table("connections").select("*").eq("buyer_id", profile.data["id"]).order("created_at", desc=True).execute().data

    else:
        connections = db.table("connections").select("*").order("created_at", desc=True).execute().data

    return connections


# ── Messages within a connection ─────────────────────────────────────────────

@router.get("/connections/{connection_id}", response_model=List[MessageResponse])
async def get_messages(
    connection_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db),
):
    _get_connection_for_user(str(connection_id), current_user["id"], db)

    messages = (
        db.table("messages")
        .select("*")
        .eq("connection_id", str(connection_id))
        .order("created_at")
        .execute().data
    )

    # Mark unread messages as read
    now = datetime.now(timezone.utc).isoformat()
    unread = [m["id"] for m in messages if m["sender_id"] != current_user["id"] and not m["read_at"]]
    if unread:
        db.table("messages").update({"read_at": now}).in_("id", unread).execute()

    return messages


@router.post("/connections/{connection_id}", response_model=MessageResponse, status_code=201)
async def send_message(
    connection_id: uuid.UUID,
    payload: MessageCreate,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db),
):
    _get_connection_for_user(str(connection_id), current_user["id"], db)

    if not payload.content and not payload.image_urls:
        raise HTTPException(status_code=400, detail="Message must have content or images")

    now = datetime.now(timezone.utc).isoformat()
    result = db.table("messages").insert({
        "connection_id": str(connection_id),
        "sender_id": current_user["id"],
        "content": payload.content,
        "image_urls": payload.image_urls,
        "message_type": payload.message_type,
        "is_system": False,
        "created_at": now,
    }).execute()

    # Notify the other participant
    conn = db.table("connections").select("supplier_id, buyer_id").eq("id", str(connection_id)).maybe_single().execute()
    if conn.data:
        supplier_user = db.table("supplier_profiles").select("user_id").eq("id", conn.data["supplier_id"]).maybe_single().execute()
        buyer_user = db.table("buyer_profiles").select("user_id").eq("id", conn.data["buyer_id"]).maybe_single().execute()

        recipient_user_id = None
        if supplier_user.data and supplier_user.data["user_id"] != current_user["id"]:
            recipient_user_id = supplier_user.data["user_id"]
        elif buyer_user.data and buyer_user.data["user_id"] != current_user["id"]:
            recipient_user_id = buyer_user.data["user_id"]

        if recipient_user_id:
            db.table("notifications").insert({
                "user_id": recipient_user_id,
                "type": "new_message",
                "title": "New message",
                "body": payload.content[:100] if payload.content else "Sent an image",
                "related_id": str(connection_id),
                "related_type": "connection",
                "created_at": now,
            }).execute()

    return result.data[0]


@router.put("/connections/{connection_id}/read", status_code=204)
async def mark_as_read(
    connection_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db),
):
    _get_connection_for_user(str(connection_id), current_user["id"], db)
    now = datetime.now(timezone.utc).isoformat()
    db.table("messages").update({"read_at": now}).eq("connection_id", str(connection_id)).neq("sender_id", current_user["id"]).is_("read_at", "null").execute()
