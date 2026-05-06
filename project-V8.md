# SourcingElf — Project Documentation
**Last Updated: 2026-05-02**

---

## Project Overview

SourcingElf is a premium B2B apparel sourcing platform that connects verified apparel manufacturers (suppliers) with global buyers through curated introductions. The platform is operated by an AI assistant called **Elfa**.

**Domains:** sourcingelf.ai / sourcingelf.com  
**AI Assistant:** Elfa (planet-orbit icon, navy avatar)

---

## Business Model

### Core Revenue
- Suppliers pay **US$138 per confirmed buyer connection** (1 credit)
- Bundle pricing: 3 credits US$368 / 5 credits US$498
- Credits are pre-deducted when applying to Buying Leads; refunded if task expires without connection

### Two Connection Paths
1. **Request Path**: Elfa promotes supplier video → buyer sends request → supplier reviews buyer → confirms connection → 1 credit deducted
2. **Task Path**: Buyer creates sourcing task → Elfa invites matched suppliers → supplier applies (credit reserved) → buyer reviews → confirms connection → credit deducted; if task expires without connection → credit refunded

### Buyer Verification
All buyers must be verified by Elfa (WhatsApp contact + background check) before being introduced to suppliers. Verified buyers can be automatically introduced to new suppliers.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML / CSS / JS (static, from Claude Design) |
| Backend | Python FastAPI |
| Database | PostgreSQL via Supabase |
| File Storage | Supabase Storage |
| Authentication | Supabase Auth |
| Payments | Stripe |
| Email | Resend |
| Server Deployment | Railway |
| Code Repository | GitHub (not yet set up) |
| AI Assistant | Claude (development) |

---

## Project Structure

```
C:\Projects\sourcingelf\
├── main.py                  # FastAPI app entry point
├── config.py                # Environment variables (pydantic-settings)
├── database.py              # Supabase connection + JWT verification
├── requirements.txt
├── .env                     # Never commit
├── database.sql             # Full database schema (24 tables)
├── HANDOFF.md               # Session handoff notes (NEW)
├── routers/
│   ├── auth.py              # Register / Login / JWT
│   ├── suppliers.py         # Supplier profile & management (COMPLETE)
│   ├── buyers.py            # Buyer profile & management (COMPLETE)
│   ├── videos.py            # Promotion video workflow (COMPLETE)
│   ├── leads.py             # Buying leads & applications (COMPLETE)
│   ├── credits.py           # Credits & Stripe payments (COMPLETE)
│   ├── messages.py          # IM chat (COMPLETE)
│   └── admin.py             # Admin operations (COMPLETE)
└── models/
    ├── user.py
    ├── supplier.py
    ├── buyer.py
    ├── video.py
    ├── lead.py
    └── credit.py
```

---

## API Routes Reference

All routes prefixed with `/api/v1/`

### Auth
- `POST /auth/register` — Register (frontend calls Supabase signUp first, then this)
- `POST /auth/login` — Login, returns JWT + role ✅ TESTED
- `GET /auth/me` — Get current user info
- `PUT /auth/me` — Update user info
- `POST /auth/me/last-login` — Record last login timestamp

### Suppliers
- `GET /suppliers/me/profile` — Get own profile (+ factories/moqs/certs/strengths/markets)
- `POST /suppliers/me/profile` — Create profile
- `PUT /suppliers/me/profile` — Update profile
- `POST /suppliers/me/factories` — Add factory
- `PUT /suppliers/me/factories/{id}` — Update factory
- `DELETE /suppliers/me/factories/{id}` — Delete factory
- (similar CRUD for moqs, certifications, strengths, markets)

### Buyers
- `GET /buyers/me/profile` — Get own profile
- `POST /buyers/me/profile` — Create profile
- `PUT /buyers/me/profile` — Update profile
- `POST /buyers/requests` — Submit lead form (unauthenticated, from supplier video page)
- `GET /buyers/me/requests` — Get my buyer requests

### Buying Leads
- `GET /leads/browse` — Supplier browses active leads (buyer names MASKED)
- `POST /leads` — Buyer creates sourcing task
- `GET /leads/me` — Buyer sees own leads
- `GET /leads/{id}` — Get lead detail
- `PUT /leads/{id}` — Update lead
- `DELETE /leads/{id}` — Cancel lead
- `POST /leads/{id}/apply` — Supplier applies (reserves 1 credit)
- `GET /leads/{id}/applications` — Buyer views applications
- `POST /leads/{id}/applications/{app_id}/connect` — Buyer confirms connection (deducts credit)

### Credits
- `GET /credits/me` — Balance + credit account
- `GET /credits/me/transactions` — Transaction history
- `POST /credits/checkout` — Create Stripe checkout session
- `POST /credits/webhook` — Stripe webhook (no auth, signature verified)
- `GET /credits/me/payments` — Payment history

### Messages
- `GET /messages/connections` — List all connections (chat list)
- `GET /messages/connections/{id}` — Get messages in connection
- `POST /messages/connections/{id}` — Send message
- `PUT /messages/connections/{id}/read` — Mark as read

### Videos
- `GET /videos/me` — Get own video(s)
- `POST /videos/me/materials` — Submit production materials
- `GET /videos/{id}` — Get video detail
- `POST /videos/{id}/approve` — Supplier approves draft
- `POST /videos/{id}/revision` — Supplier requests revision (max 1)
- `GET /videos/admin/all` — Admin: list all videos
- `PUT /videos/admin/{id}` — Admin: update video status

### Admin
- `GET /admin/users` — List all users (filter by role/status)
- `PUT /admin/users/{id}/status` — Update user status
- `GET /admin/suppliers` — List supplier profiles
- `PUT /admin/suppliers/{id}/verify` — Verify supplier
- `GET /admin/buyer-requests` — List buyer requests
- `PUT /admin/buyer-requests/{id}/status` — Update request status
- `GET /admin/buyers` — List buyer profiles
- `PUT /admin/buyers/{id}/verify` — Verify buyer (elfa_verified=true)
- `POST /admin/credits/adjust` — Manual credit adjustment
- `POST /admin/notes` — Create admin note
- `GET /admin/notes/{user_id}` — Get admin notes for user

---

## Database — 24 Tables

| Table | Purpose |
|-------|---------|
| `users` | All accounts (supplier / buyer / admin) |
| `supplier_profiles` | Supplier company details |
| `supplier_factories` | Factory info |
| `supplier_moqs` | MOQ by category |
| `supplier_certifications` | Certifications |
| `supplier_strengths` | Key selling points |
| `supplier_markets` | Target markets |
| `buyer_profiles` | Buyer company details |
| `buyer_moqs` | MOQ requirements |
| `buyer_markets` | Target markets |
| `videos` | Promo video status |
| `video_materials` | Submitted materials |
| `video_selling_points` | Selling points per video |
| `buying_leads` | Buyer sourcing tasks |
| `buying_lead_items` | Line items per task |
| `lead_applications` | Supplier applications |
| `buyer_requests` | Buyer requests to suppliers |
| `connections` | Confirmed connections |
| `messages` | IM chat messages |
| `credits` | Supplier credit balance (balance + reserved + total_purchased + total_used) |
| `credit_transactions` | All credit movements |
| `payments` | Stripe payment records |
| `notifications` | System notifications |
| `admin_notes` | Internal admin notes |

### Credit Transaction Types
- `topup` — Stripe payment received
- `reserved` — Applied to buying lead (pre-deducted, balance locked)
- `deducted` — Connection confirmed (finalised, reserved→deducted)
- `refunded` — Task expired without connection
- `manual_add` / `manual_deduct` — Admin adjustment

---

## config.py Fields

```python
# Supabase
supabase_url: str
supabase_anon_key: str        # Public/anon key
supabase_service_key: str     # Service role key (bypasses RLS)
supabase_jwt_secret: str      # Base64-encoded — ALWAYS decode before use

# Stripe
stripe_secret_key: str
stripe_webhook_secret: str

# Resend
resend_api_key: str
from_email: str = "noreply@sourcingelf.com"

# App
app_env: str = "development"
app_url: str = "http://localhost:8000"
frontend_url: str = "http://localhost:3000"

# Credit pricing
credits_single_price_usd: float = 138.00
credits_triple_price_usd: float = 368.00
credits_five_pack_price_usd: float = 498.00
```

---

## Environment Variables (.env)

```
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_KEY=...
SUPABASE_JWT_SECRET=...  (base64 encoded)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_... (set after Railway deployment)
RESEND_API_KEY=re_...
APP_ENV=development
FRONTEND_URL=http://localhost:3000
```

---

## Notes & Gotchas

- **Frontend stack is plain HTML/CSS/JS** — do NOT suggest Next.js
- **Supabase Auth**: frontend calls `supabase.auth.signUp()` first, then `POST /auth/register`
- **JWT verification**: Supabase JWT Secret is base64-encoded → `base64.b64decode()` before use
- **Cloudflare blocks PowerShell** calls to supabase.co — test Auth via browser only
- **Windows environment**: PowerShell only, no Linux commands
- **PowerShell encoding**: Never use PowerShell to write Python code directly — use notepad or Python scripts
- **database.py pattern**: `get_db()` returns `supabase_admin` (service role), `get_current_user()` verifies JWT via `jose` library
- **Stripe**: TEST mode currently — switch to live before launch
- **Buyer name masking**: ALWAYS mask buyer company name until connection confirmed (business rule #5)

---

## Business Logic — Key Rules

1. Credit reservation: Supplier applies to lead → 1 credit reserved (credits.reserved +1, balance unchanged... wait, actual implementation: balance-1, reserved+1 — check leads.py)
2. Credit deduction: Buyer confirms → reserved credit becomes deducted (balance-1, reserved-1, total_used+1)
3. Credit refund: Lead expires → reserved credit returned (balance+1, reserved-1)
4. Buyer verification: All buyers verified by Elfa before introduction
5. Identity masking: Buyer company name ALWAYS hidden until connection confirmed
6. One application per lead per supplier
7. Multiple connections per task allowed (buyer can connect with many suppliers)
8. Video revision: Max 1 revision per video
9. Legal confirmation: Supplier must accept IP terms before video published
10. Request expiry: 30 days
11. Lead expiry: Buyer-set date (max 6 months), amber warning if <7 days
12. Credit confirmation modal: Required before every Connect action

---

## Current Status (2026-05-02)

### Completed ✅
- Business logic & requirements finalised
- Database schema designed (24 tables) and created in Supabase
- Python FastAPI backend — all 8 router files complete
- All dependencies installed (fastapi, uvicorn, httpx, stripe, pyjwt/jose, supabase)
- Server running successfully (`uvicorn main:app --reload`)
- **POST /auth/login tested and working** — returns JWT + role
- All 22 frontend HTML pages designed (Claude Design)

### In Progress ⏳
- **401 error on authenticated endpoints** — GET /suppliers/me/profile returns "Invalid token"
  - JWT decode uses `jose` library with `options={"verify_aud": False}`
  - Need to debug in new session

### Upcoming 🔜
- Fix 401 JWT issue
- Test all remaining endpoints via Swagger UI
- Connect frontend HTML to backend API (fix 4 known issues during integration)
- Stripe webhook setup (after Railway deployment)
- Deploy to Railway
- Domain DNS configuration
- End-to-end testing
- Launch

### Test Accounts
| Email | Password | Role | In users table |
|-------|----------|------|----------------|
| test.supplier@sourcingelf.com | Test1234! | supplier | YES |
| test3@sourcingelf.com | unknown | supplier | YES |

### Backups
- `C:\Projects\sourcingelf_backup_20260502` — before login fix
- `C:\Projects\sourcingelf_backup_login_working` — after login working

---

## Scheduled Jobs (Cron) — Not Yet Implemented

| Job | Frequency | Action |
|-----|-----------|--------|
| Task expiry processor | Daily 2:00 AM | Expire leads, refund reserved credits |
| Request expiry | Daily 2:00 AM | Expire 30-day-old buyer requests |
| Expiry reminder | Daily 9:00 AM | Notify buyers of tasks expiring in 7 days |

---

## Third-Party Accounts

| Service | Purpose | Console |
|---------|---------|---------|
| Supabase | Database + Storage + Auth | supabase.com/dashboard |
| Stripe | Payment (TEST mode) | dashboard.stripe.com |
| Railway | Backend deployment | railway.app |
| Resend | Email (not yet integrated) | resend.com |
| Namecheap | Domain | namecheap.com |

**Domains:** sourcingelf.ai / sourcingelf.com
