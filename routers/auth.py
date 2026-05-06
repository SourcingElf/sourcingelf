from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from datetime import datetime, timezone

from database import get_db, get_current_user
from models.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: Client = Depends(get_db)):
    """
    Create a user record after Supabase Auth sign-up.
    Call this from the client immediately after auth.signUp() succeeds.
    The JWT from the sign-up response should be passed as the Bearer token
    so the user_id in the token matches the record we create here.
    """
    existing = db.table("users").select("id").eq("email", payload.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    now = datetime.now(timezone.utc).isoformat()
    result = db.table("users").insert({
        **payload.model_dump(),
        "status": "active",
        "auth_provider": "email",
        "created_at": now,
        "updated_at": now,
    }).execute()
    return result.data[0]


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_me(
    payload: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db),
):
    update_data = payload.model_dump(exclude_none=True)
    if not update_data:
        return current_user
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    result = db.table("users").update(update_data).eq("id", current_user["id"]).execute()
    return result.data[0]


@router.post("/me/last-login", status_code=status.HTTP_204_NO_CONTENT)
async def record_last_login(
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db),
):
    db.table("users").update({
        "last_login_at": datetime.now(timezone.utc).isoformat()
    }).eq("id", current_user["id"]).execute()


# 



from pydantic import BaseModel as _BM
from config import settings as _s

class LoginRequest(_BM):
    email: str
    password: str

@router.post("/login")
async def login(payload: LoginRequest, db: Client = Depends(get_db)):
    import httpx
    from datetime import datetime, timezone
    async with httpx.AsyncClient() as c:
        resp = await c.post(
            f"{_s.supabase_url}/auth/v1/token?grant_type=password",
            headers={"apikey": _s.supabase_anon_key, "Content-Type": "application/json"},
            json={"email": payload.email, "password": payload.password},
            timeout=10,
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail=resp.json().get("error_description", "Invalid credentials"))
    auth_data = resp.json()
    result = db.table("users").select("*").eq("id", auth_data["user"]["id"]).maybe_single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user = result.data
    if user["status"] == "suspended":
        raise HTTPException(status_code=403, detail="Account suspended")
    db.table("users").update({"last_login_at": datetime.now(timezone.utc).isoformat()}).eq("id", user["id"]).execute()
    return {"access_token": auth_data["access_token"], "token_type": "bearer", "user_id": user["id"], "role": user["role"], "email": user["email"]}
