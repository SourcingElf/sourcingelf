# SourcingElf V2 — ENVIRONMENT.md
更新时间：2026-05-19

---

# Purpose

This file defines environment variables, deployment settings, and local development notes.

Do not commit secret keys.

---

# Public Frontend Values

These can be used in frontend code:

```text
SUPABASE_URL
SUPABASE_ANON_KEY
STRIPE_PUBLISHABLE_KEY
```

---

# Secret Values

These must NOT be exposed in frontend HTML/JS:

```text
SUPABASE_SERVICE_ROLE_KEY
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
RESEND_API_KEY
```

Use secrets only in:
- Cloudflare Functions
- server-side endpoints
- Supabase Edge Functions
- secure backend environment

---

# Supabase

Project:
```text
sourcingelf-v2
```

Project URL:
```text
https://btdrdozwndvdvzoqteol.supabase.co
```

Frontend should use:
```text
anon key only
```

Admin operations requiring bypass of RLS:
```text
must not use anon key
```

---

# Stripe

Payment model:
```text
one-time payment per connection
```

Current pricing:
```text
Standard: US$138
Promo: US$99
```

Do not implement:
- wallet
- subscription
- credits balance
- top-up

---

# Resend

Used for:
- registration emails
- lead notifications
- payment/connection notifications
- buyer/supplier updates

API key must remain secret.

---

# Cloudflare Pages

Deployment:
```text
Cloudflare Pages
```

Domain:
```text
sourcingelf.ai
```

Branch:
```text
V2
```

Do not use:
```text
Railway
```

---

# Local Development

Recommended local folder:
```text
C:/projects/sourcingelf-V2/
```

Suggested local server:
```text
npx serve .
```

or:
```text
python -m http.server 3000
```

Local URL:
```text
http://localhost:3000
```

---

# Git Rules

Before any development:
```text
git status
git branch
```

Must confirm:
```text
V2 branch
```

Never modify:
```text
main branch / V1 files
```

---

# Security Rules

Never paste or expose:
- service role key
- Stripe secret key
- Resend API key
- webhook secrets

If Claude Code asks for secrets:
- refuse
- use placeholder env names only

---

# Env Variable Template

Use placeholders:

```env
SUPABASE_URL=
SUPABASE_ANON_KEY=
STRIPE_PUBLISHABLE_KEY=

# Server-side only
SUPABASE_SERVICE_ROLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
RESEND_API_KEY=
```
