# SourcingElf — Project Documentation
**Last Updated: 2026-05-04 (session 2)**

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
├── main.py
├── config.py
├── database.py
├── requirements.txt
├── .env
├── database.sql
├── routers\
│   ├── auth.py
│   ├── suppliers.py
│   ├── buyers.py
│   ├── videos.py
│   ├── leads.py
│   ├── credits.py
│   ├── messages.py
│   └── admin.py
└── models\
    ├── user.py
    ├── supplier.py
    ├── buyer.py
    ├── video.py
    ├── lead.py
    └── credit.py

C:\Projects\sourcingelf-frontend\
├── inject_all.py
├── client.js
├── fix_*.py
└── *.html  (22 generated pages)

C:\Projects\claude design backup\standalone\
└── *.html  (original backups — NEVER touch)
```

---

## Frontend Architecture (Important)

- 22 HTML pages, all generated from original backups + inject_all.py
- **Never edit HTML files directly**
- **All logic changes go into inject_all.py** → run it → all pages updated
- client.js is the shared API client, included in every page
- **Buyer-side original HTML is in bundled/compressed format** — cannot be read with PowerShell debug scripts. Use browser F12 → Elements to inspect rendered structure.
- **To intercept links in buyer pages, use document capture:**
  ```javascript
  document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (link && link.href && link.href.includes('dashboard.html')) {
      e.preventDefault();
      e.stopPropagation();
      doLogin();
    }
  }, true);
  ```
- **onclick quote rule**: onclick attributes use double quotes — strings inside must use &quot; not single quotes.

---

## API Routes Reference

All routes prefixed with `/api/v1/`

### Auth
- `POST /auth/register`
- `POST /auth/login` ✅ TESTED
- `GET /auth/me`
- `PUT /auth/me`
- `POST /auth/me/last-login`

### Suppliers
- `GET /suppliers/me/profile`
- `POST /suppliers/me/profile`
- `PUT /suppliers/me/profile`
- `GET /suppliers/me/buyer-requests` ✅ TESTED
- `POST /suppliers/me/buyer-requests/{id}/connect`
- `GET /suppliers/me/connected-buyers` ✅ ADDED 2026-05-03
- (CRUD for factories, moqs, certifications, strengths, markets)

### Buyers
- `GET /buyers/me/profile`
- `POST /buyers/me/profile`
- `PUT /buyers/me/profile`
- `POST /buyers/requests`
- `GET /buyers/me/requests`

### Buying Leads
- `GET /leads/browse`
- `POST /leads`
- `GET /leads/me`
- `GET /leads/{id}`
- `PUT /leads/{id}`
- `DELETE /leads/{id}`
- `POST /leads/{id}/apply`
- `GET /leads/{id}/applications`
- `POST /leads/{id}/applications/{app_id}/connect`

### Credits
- `GET /credits/me` ✅ TESTED
- `GET /credits/me/transactions` ✅ TESTED
- `POST /credits/checkout`
- `POST /credits/webhook`
- `GET /credits/me/payments`

### Messages
- `GET /messages/connections` ✅ TESTED
- `GET /messages/connections/{id}`
- `POST /messages/connections/{id}`
- `PUT /messages/connections/{id}/read`

### Videos
- `GET /videos/me` ✅ TESTED
- `POST /videos/me/materials`
- `GET /videos/{id}`
- `POST /videos/{id}/approve`
- `POST /videos/{id}/revision`
- `GET /videos/admin/all`
- `PUT /videos/admin/{id}`

### Admin
- `GET /admin/users`
- `PUT /admin/users/{id}/status`
- `GET /admin/suppliers`
- `PUT /admin/suppliers/{id}/verify`
- `GET /admin/buyer-requests`
- `PUT /admin/buyer-requests/{id}/status`
- `GET /admin/buyers`
- `PUT /admin/buyers/{id}/verify`
- `POST /admin/credits/adjust`
- `POST /admin/notes`
- `GET /admin/notes/{user_id}`

---

## Business Logic — Key Rules

1. Credit reservation: Supplier applies to lead → 1 credit reserved
2. Credit deduction: Buyer confirms → reserved credit becomes deducted
3. Credit refund: Lead expires → reserved credit returned
4. Buyer verification: All buyers verified by Elfa before introduction
5. **Identity masking: Buyer company name, full name, and all contact details ALWAYS hidden until connection confirmed.**
6. One application per lead per supplier
7. Multiple connections per task allowed
8. Video revision: Max 1 revision per video
9. Legal confirmation: Supplier must accept IP terms before video published
10. Request expiry: 30 days
11. Lead expiry: Buyer-set date (max 6 months), amber warning if <7 days
12. Credit confirmation modal: Required before every Connect action
13. **Supplier must view buyer profile BEFORE connecting — View Profile opens modal, Connect Now is inside the modal**

---

## Current Status (2026-05-04 session 2)

### Completed ✅
- Business logic & requirements finalised
- Database schema (24 tables) created in Supabase
- Python FastAPI backend — all 8 router files complete
- All 22 frontend HTML pages — client.js injected
- Supplier Dashboard — all 3 metric cards showing real API data
- Supplier Dashboard — Buying Leads feed showing real API data
- Supplier Requests page — View Profile modal, masked buyer info, Connect Now inside modal
- **Supplier Connected page — onclick quote bug fixed (session 2)**

### ❌ Buyer Login — NOT complete, top priority next session
Original HTML has `<a href="dashboard.html">` as the Log In button — it jumps directly, bypassing our login logic. Solution: use `document.addEventListener('click', handler, true)` capture phase. See HANDOFF.md for exact code.

### Pending ⏳
- Buyer login (top priority)
- Buyer Dashboard
- Buyer create task
- Buyer view applications & confirm connection
- IM Chat (needs full rewrite, not using original backup)
- Buying Leads Apply → real API
- Dashboard pagination fix
- Deploy to Railway

### Test Accounts
| Email | Password | Role |
|-------|----------|------|
| test.supplier@sourcingelf.com | Test1234! | supplier |
| test.buyer@sourcingelf.com | Test1234! | buyer |

### Test Data in Supabase
| Table | Record | Purpose |
|-------|--------|---------|
| users (buyer) | bae1599d-b815-4473-a248-52c76609a04d | Buyer test user |
| buyer_profiles | 8ea03203-0c55-44b6-acac-6f7085106aac | Test Buyer Co / US / Brand |
| buying_leads | 30837a3c-8b92-40bd-a817-b3334d06c599 | Women's Knitwear lead |
| buyer_requests | Sarah Johnson / Anthropologie Group | Test Requests page |
| supplier_profiles | f37d3e21-3ed8-4eed-a9b9-017746239e75 | Supplier test account |

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
