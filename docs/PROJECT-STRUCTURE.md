# SourcingElf V2 — PROJECT-STRUCTURE.md
更新时间：2026-05-19

---

# Purpose

This file defines the recommended frontend project structure for SourcingElf V2.

It is used to guide Claude.ai and Claude Code during frontend engineering.

Important:
- This is NOT a redesign instruction.
- This is NOT a framework migration instruction.
- Existing 7 static HTML pages remain the source of truth.

---

# Current Strategy

SourcingElf V2 uses:

- Static HTML
- CSS
- Vanilla JavaScript
- Cloudflare Pages
- Supabase
- Stripe
- Resend

No React / Next.js / Vite migration at this stage.

---

# Expected 7 Pages

| Page | File |
|------|------|
| Homepage | index.html |
| Buyer Portal | buyer-portal-v2.html |
| Supplier Landing | supplier-landing-v2.html |
| Supplier Dashboard | supplier-dashboard-v2.html |
| Supplier Features | supplier-features-v2.html |
| Chat | chat-v2.html |
| Admin | admin-v2.html |

---

# Recommended Project Structure

```text
sourcingelf-v2/
│
├─ index.html
├─ buyer-portal-v2.html
├─ supplier-landing-v2.html
├─ supplier-dashboard-v2.html
├─ supplier-features-v2.html
├─ chat-v2.html
├─ admin-v2.html
│
├─ assets/
│  ├─ SourcingElf-Logo.png
│  └─ other-images/
│
├─ styles/
│  ├─ global.css
│  ├─ homepage.css
│  ├─ buyer-portal.css
│  ├─ supplier-landing.css
│  ├─ supplier-dashboard.css
│  ├─ supplier-features.css
│  ├─ chat.css
│  └─ admin.css
│
├─ scripts/
│  ├─ supabase-client.js
│  ├─ auth.js
│  ├─ buyer.js
│  ├─ supplier.js
│  ├─ chat.js
│  ├─ payments.js
│  └─ admin.js
│
├─ docs/
│  ├─ CLAUDE.md
│  ├─ STATUS.md
│  ├─ DESIGN-SYSTEM-V2.md
│  ├─ 7-PAGES-FRONTEND-PROMPTS.md
│  ├─ PROJECT-STRUCTURE.md
│  ├─ FRONTEND-FLOW.md
│  ├─ DATABASE-SCHEMA.md
│  ├─ ENVIRONMENT.md
│  └─ DEVELOPMENT-RULES.md
│
└─ README.md
```

---

# Important Notes

## HTML files

The existing 7 HTML files should not be rewritten.

If CSS/JS are currently inline inside bundled HTML:
- Do not extract everything immediately.
- Only extract when needed and safe.
- Avoid large risky refactors.

## CSS

Preferred long-term direction:
- shared global design styles in `styles/global.css`
- page-specific styles in separate files

But during MVP:
- keep existing inline styles if extraction creates risk
- use minimal patch workflow

## JavaScript

Preferred long-term direction:
- shared Supabase client in `scripts/supabase-client.js`
- auth helpers in `scripts/auth.js`
- page-specific logic in page JS files

But during MVP:
- do not move working JS unless necessary
- avoid breaking static pages

---

# Asset Rules

## Logo

Preferred file:
```text
assets/SourcingElf-Logo.png
```

If current pages use root-level:
```text
SourcingElf-Logo.png
```

Do not change all paths at once.

Fix page by page only.

## Dark Background Logo

Use:
```css
filter: brightness(0) invert(1);
```

---

# Cloudflare Pages Rules

Cloudflare should deploy from V2 branch.

Do not reintroduce Railway.

Do not require server runtime for static frontend.

---

# Claude Code Usage

## First task

Claude Code should inspect only:

```text
Do not edit files.
List current structure.
Compare against expected 7 pages.
Report mismatches.
```

## Do not allow Claude Code to

- redesign UI
- migrate framework
- rewrite all HTML
- reorganize everything at once
- touch V1/main branch
- change deployment architecture without approval

---

# Acceptance Criteria

Project structure is acceptable when:

- all 7 pages exist
- all pages load locally
- logo/assets load correctly
- Cloudflare Pages deploys successfully
- no visual redesign occurred
- no V1 video/wallet workflow returned
