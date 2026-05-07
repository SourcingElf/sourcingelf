# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
# Backend (window 1)
uvicorn main:app --reload

# Frontend file server (window 2)
python -m http.server 3000 --directory frontend

# API docs (development only)
http://localhost:8000/docs
```

Deploy target is Railway (`Procfile`: `uvicorn main:app --host 0.0.0.0 --port $PORT`). To redeploy: Railway dashboard → manual Redeploy.

## Architecture

**Backend**: FastAPI + Supabase (PostgreSQL). No ORM — all DB access uses the Supabase Python client directly (`supabase_admin` with the service key). Auth is Supabase Auth (JWT ES256); the backend decodes tokens with `verify_signature=False` and looks up the user in the `users` table.

**Frontend**: Pure HTML/CSS/JS files in `frontend/`. No build step. All pages include `<script src="client.js"></script>`, which provides `SourcingElf.AuthAPI`, `SourcingElf.SupplierAPI`, `SourcingElf.BuyerAPI`, `SourcingElf.LeadsAPI`, `SourcingElf.CreditsAPI`, `SourcingElf.MessagesAPI`. The client auto-selects `API_BASE_URL`: `http://localhost:8000` on port 3000, otherwise same-origin (production).

**Static file serving**: `main.py` mounts `frontend/` at `/` after all API routes, so `/api/v1/...` always wins.

## Auth Flow

Two-step registration: `supabase.auth.signUp()` → then `POST /api/v1/auth/register` with the resulting JWT as Bearer. The `users` table ID must match the Supabase Auth UUID — mismatches cause 401/404 errors everywhere.

Token stored in `localStorage` as `sb_session` (full Supabase session object); `TokenManager.getAccessToken()` extracts `access_token` from it.

`require_role("supplier")` / `require_role("buyer")` are FastAPI dependency factories — use them on any route that needs RBAC.

## Key Architectural Rules

**Supabase client**: `get_db()` always returns `supabase_admin` (service key). Never use the anon client for backend DB writes.

**Profile indirection**: Routes never work directly with `user_id`. They call `_require_supplier_profile(user_id, db)` or `_require_buyer_profile(user_id, db)` to get the profile row, then use `profile["id"]` (the profile UUID) for all subsequent queries. This is the pattern in every router.

**Credits lifecycle**: Apply → credit `reserved +1`; buyer accepts → credit `balance -1, reserved -1, total_used +1`. The `credits` table tracks `balance`, `reserved`, `total_purchased`, `total_used`. Available credits = `balance - reserved`. HTTP 402 means insufficient credits.

**Connections**: Created only when a buyer accepts a supplier's lead application (`POST /api/v1/leads/{lead_id}/applications/{app_id}/connect`). A system message is auto-inserted into `messages` at connection time. The `messages` router uses `connection_id` (not user IDs directly) for all chat operations.

## Frontend Patterns

**Buyer-portal HTML files are pre-bundled** — they have internal renderers that run on `DOMContentLoaded`. To prevent bundle placeholders from flashing before real API data:
- Use `Object.defineProperty` on the target container's `innerHTML` setter, set up synchronously inside the `<script>` block before any `DOMContentLoaded` handlers register.
- Use a flag (`_blocked = true` by default) that only our render function can toggle via a `Element.prototype.__allowOurRender` setter.

**onclick in HTML attributes**: Never use single quotes inside `onclick="..."`. Use `&quot;` if string literals are needed inside the attribute value.

**Buyer-portal navigation**: Links are `<a href="PageName.html">` inside the bundle. Intercept with `document.addEventListener('click', handler, true)` (capture phase) — do **not** use MutationObserver or setInterval.

## Database Schema Summary

Core tables: `users` → `supplier_profiles` / `buyer_profiles` → `connections` → `messages`. Credits flow: `credits` (balance sheet) + `credit_transactions` (ledger) + `payments` (Stripe). Leads flow: `buying_leads` + `buying_lead_items` → `lead_applications` → `connections`. Reference: `database.sql`.

## Environment Variables (`.env`)

| Key | Purpose |
|-----|---------|
| `SUPABASE_URL` / `SUPABASE_ANON_KEY` / `SUPABASE_SERVICE_KEY` | Supabase project |
| `SUPABASE_JWT_SECRET` | Present but JWT verification is currently disabled (`verify_signature=False`) |
| `STRIPE_SECRET_KEY` / `STRIPE_WEBHOOK_SECRET` | Stripe payments |
| `RESEND_API_KEY` / `FROM_EMAIL` | Transactional email |
| `APP_ENV` | `development` enables `/docs` and `/redoc` |
| `FRONTEND_URL` | Used in Stripe redirect URLs and CORS |

## Test Accounts

| Email | Password | Role |
|-------|----------|------|
| test.supplier@sourcingelf.com | Test1234! | supplier |
| test.buyer@sourcingelf.com | Test1234! | buyer |
