# SourcingElf — Project Documentation
**Last Updated: 2026-05-03**

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
1. **Request Path**: Elfa promotes supplier video → buyer sends request → supplier reviews buyer profile → confirms connection → 1 credit deducted
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

C:\Projects\sourcingelf-frontend\
├── inject_all.py            # Master injection script — edit this, not the HTML files
├── client.js                # API client — shared across all pages
├── fix_*.py                 # One-time fix scripts (keep for reference)
└── *.html                   # 22 generated HTML pages (do not edit directly)

C:\Projects\claude design backup\standalone\
└── *.html                   # Original HTML backups — NEVER touch these
```

---

## Frontend Architecture (Important)

- 22 HTML pages, all generated from original backups + inject_all.py
- **Never edit HTML files directly** — changes will be overwritten next time inject_all.py runs
- **All logic changes go into inject_all.py** → run it → all pages updated
- client.js is the shared API client, included in every page's `<head>`
- Fix scripts (fix_*.py) are one-time scripts used to update inject_all.py safely
- **Before modifying inject_all.py**: always use a debug script with `print(repr(...))` to confirm exact content and end markers — do NOT rely on PowerShell display which may show garbled characters

---

## API Routes Reference

All routes prefixed with `/api/v1/`

### Auth
- `POST /auth/register` — Register
- `POST /auth/login` — Login, returns JWT + role ✅ TESTED
- `GET /auth/me` — Get current user info
- `PUT /auth/me` — Update user info
- `POST /auth/me/last-login` — Record last login timestamp

### Suppliers
- `GET /suppliers/me/profile` — Get own profile (+ factories/moqs/certs/strengths/markets)
- `POST /suppliers/me/profile` — Create profile
- `PUT /suppliers/me/profile` — Update profile
- `GET /suppliers/me/buyer-requests` — Get buyer requests received by this supplier ✅ TESTED
- `POST /suppliers/me/buyer-requests/{id}/connect` — Supplier confirms connection from request
- `GET /suppliers/me/connected-buyers` — Get connected buyers with full profile info ✅ ADDED 2026-05-03
- (CRUD for factories, moqs, certifications, strengths, markets)

### Buyers
- `GET /buyers/me/profile` — Get own profile
- `POST /buyers/me/profile` — Create profile
- `PUT /buyers/me/profile` — Update profile
- `POST /buyers/requests` — Submit lead form (unauthenticated)
- `GET /buyers/me/requests` — Get my buyer requests (buyer use only)

### Buying Leads
- `GET /leads/browse` — Supplier browses active leads (buyer names MASKED)
- `POST /leads` — Buyer creates sourcing task
- `GET /leads/me` — Buyer sees own leads
- `GET /leads/{id}` — Get lead detail
- `PUT /leads/{id}` — Update lead
- `DELETE /leads/{id}` — Cancel lead
- `POST /leads/{id}/apply` — Supplier applies (reserves 1 credit)
- `GET /leads/{id}/applications` — Buyer views applications
- `POST /leads/{id}/applications/{app_id}/connect` — Buyer confirms connection

### Credits
- `GET /credits/me` — Balance + credit account ✅ TESTED
- `GET /credits/me/transactions` — Transaction history ✅ TESTED
- `POST /credits/checkout` — Create Stripe checkout session
- `POST /credits/webhook` — Stripe webhook
- `GET /credits/me/payments` — Payment history

### Messages
- `GET /messages/connections` — List all connections ✅ TESTED
- `GET /messages/connections/{id}` — Get messages in connection
- `POST /messages/connections/{id}` — Send message
- `PUT /messages/connections/{id}/read` — Mark as read

### Videos
- `GET /videos/me` — Get own videos ✅ TESTED
- `POST /videos/me/materials` — Submit production materials
- `GET /videos/{id}` — Get video detail
- `POST /videos/{id}/approve` — Supplier approves draft
- `POST /videos/{id}/revision` — Supplier requests revision (max 1)
- `GET /videos/admin/all` — Admin: list all videos
- `PUT /videos/admin/{id}` — Admin: update video status

### Admin
- `GET /admin/users` — List all users
- `PUT /admin/users/{id}/status` — Update user status
- `GET /admin/suppliers` — List supplier profiles
- `PUT /admin/suppliers/{id}/verify` — Verify supplier
- `GET /admin/buyer-requests` — List buyer requests
- `PUT /admin/buyer-requests/{id}/status` — Update request status
- `GET /admin/buyers` — List buyer profiles
- `PUT /admin/buyers/{id}/verify` — Verify buyer
- `POST /admin/credits/adjust` — Manual credit adjustment
- `POST /admin/notes` — Create admin note
- `GET /admin/notes/{user_id}` — Get admin notes for user

---

## Business Logic — Key Rules

1. Credit reservation: Supplier applies to lead → 1 credit reserved
2. Credit deduction: Buyer confirms → reserved credit becomes deducted
3. Credit refund: Lead expires → reserved credit returned
4. Buyer verification: All buyers verified by Elfa before introduction
5. **Identity masking: Buyer company name, full name, and all contact details ALWAYS hidden until connection confirmed. Show only: masked company name (e.g. "A** Group"), business nature, country, annual volume, products, positioning, target market, message.**
6. One application per lead per supplier
7. Multiple connections per task allowed
8. Video revision: Max 1 revision per video
9. Legal confirmation: Supplier must accept IP terms before video published
10. Request expiry: 30 days
11. Lead expiry: Buyer-set date (max 6 months), amber warning if <7 days
12. Credit confirmation modal: Required before every Connect action
13. **Supplier must be able to view buyer profile BEFORE connecting — View Profile button opens a modal with masked buyer info, Connect Now is inside the modal (not on the card directly)**

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
| `buyer_requests` | Buyer requests to suppliers (from Lead Form) |
| `connections` | Confirmed connections |
| `messages` | IM chat messages |
| `credits` | Supplier credit balance |
| `credit_transactions` | All credit movements |
| `payments` | Stripe payment records |
| `notifications` | System notifications |
| `admin_notes` | Internal admin notes |

### Known Schema Gap — buyer_requests MOQ
- buyer_requests table has no MOQ field
- buyer_moqs table exists in buyer_profiles but Lead Form buyers may not be registered (buyer_id = null)
- Current workaround: show Target Market in place of MOQ on request cards
- Future fix needed: add MOQ field to Lead Form + buyer_requests table

---

## Current Status (2026-05-03)

### Completed ✅
- Business logic & requirements finalised
- Database schema (24 tables) created in Supabase
- Python FastAPI backend — all 8 router files complete
- Server running successfully
- POST /auth/login tested and working
- All 22 frontend HTML pages — client.js injected
- Dashboard Home — all 3 metric cards showing real API data
- **Supplier Requests page — fully rebuilt (2026-05-03)**
  - Real API data (replaced hardcoded fake data)
  - View Profile modal with masked buyer info
  - Connect Now inside modal with credit check
  - Not Interested flow retained
- **Supplier Connected page — real API logic injected (2026-05-03 evening)**
  - New dedicated endpoint GET /suppliers/me/connected-buyers added to suppliers.py
  - Returns connection records joined with buyer_profiles info
  - client.js: SE.SupplierAPI.getConnectedBuyers() added
  - Card rendering, search filter, Open Chat button all implemented
  - ⚠️ Not yet tested with real data — test account has no connections in Supabase

### In Progress ⏳
- Supplier Connected page — needs real connection test data in Supabase to verify card rendering
- Buying Leads page — needs real API data (currently hardcoded)
- IM Chat page integration

### Upcoming 🔜
- Buyer portal pages
- Stripe webhook setup (after Railway deployment)
- Deploy to Railway
- Domain DNS configuration
- End-to-end testing
- Launch

### Test Accounts
| Email | Password | Role |
|-------|----------|------|
| test.supplier@sourcingelf.com | Test1234! | supplier |

### Test Data in Supabase
| Table | Record | Purpose |
|-------|--------|---------|
| buyer_requests | Sarah Johnson / Anthropologie Group / US / Brand | Test Requests page |

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
