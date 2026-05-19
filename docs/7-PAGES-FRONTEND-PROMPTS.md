# SourcingElf V2 — 7 Pages Frontend Development Prompts
版本：V2 Clean MVP
更新时间：2026-05-19

---

# 使用方式

这个文件不是设计 prompt。

用途：
- 给 Claude.ai / Claude Code 做前端开发参考
- 明确每个页面的职责
- 防止 Claude Code 重新设计页面
- 防止复用 V1 旧 video / wallet 逻辑
- 保持 7 个静态 HTML 页面作为 source of truth

开发原则：
- No redesign
- No layout rewrite
- No framework migration
- Minimal edits only
- Static HTML/CSS/JS first
- One task at a time
- User checks every change

---

# Global MVP Workflow

Buyer posts sourcing task
↓
Elfa/Admin matching
↓
Suppliers apply
↓
Buyer reviews suppliers
↓
Supplier pays connection fee
↓
Connection unlocked
↓
Chat unlocked

---

# Removed V1 Logic

Do NOT add back:

- supplier promotion video
- showcase video
- wallet/top-up
- membership/subscription
- Railway/FastAPI assumptions
- old supplier marketing flow
- complex marketplace discovery

---

# Page 1 — homepage / index.html

## Role

Public marketing homepage.

## Purpose

Explain SourcingElf positioning:
- AI-assisted sourcing connections
- premium apparel suppliers
- qualified global buyers
- curated introductions, not marketplace clutter

## Frontend Rules

- Keep current visual design
- Do not redesign hero
- Do not add new sections unless explicitly requested
- Keep footer unified
- Keep logo consistent

## Future Data Integration

Low priority.

Mostly static page.

Possible later:
- lead capture
- buyer/supplier CTA tracking

## Do Not Add

- supplier video showcase
- marketplace supplier grid
- heavy search/filtering
- public chat

---

# Page 2 — buyer-portal-v2.html

## Role

Buyer workspace.

## Purpose

Allow buyer to:
- create sourcing task
- let Elfa help organize request
- review matched suppliers/applications
- connect/pay/unlock chat

## Core Objects

- buyer_profiles
- buying_leads
- buying_lead_items
- lead_applications
- connections
- payments
- messages

## Required MVP Logic

Buyer can:
- view buyer profile
- create/edit sourcing task
- see supplier applications
- review supplier cards
- accept/select supplier
- proceed to connection/payment
- enter chat after connection unlocked

## UI Rules

- Keep existing UI
- Do not convert into marketplace browse page
- Keep buyer-task-led flow
- Keep Elfa assistive wording
- Keep View Details logic
- Hide sensitive supplier/contact data before connection where applicable

## Do Not Add

- generic supplier directory
- supplier video showcase
- wallet balance
- subscription plan

---

# Page 3 — supplier-landing-v2.html

## Role

Supplier entry page.

## Purpose

Supplier can:
- understand value proposition
- register/login
- build supplier profile
- let Elfa autofill profile from website/B2B showroom/profile link or upload

## Core Objects

- users
- supplier_profiles
- supplier_factories
- supplier_certifications
- supplier_strengths
- supplier_markets
- supplier_moqs

## Required MVP Logic

Supplier can:
- sign up
- log in
- reset password
- submit profile
- upload/paste business info source
- wait for review/approval

## UI Rules

- Keep registration/profile flow simple
- Keep Elfa autofill module
- Keep wording focused on buying leads and curated connections
- Keep optional website/B2B profile link wording

## Do Not Add

- video upload
- promotional showcase
- product catalog management
- complex seller storefront

---

# Page 4 — supplier-dashboard-v2.html

## Role

Supplier operational dashboard.

## Purpose

Supplier can:
- view relevant buying leads
- view full lead details
- apply to leads
- see application status
- pay when buyer accepts
- start chat after connection unlock

## Core Objects

- supplier_profiles
- buying_leads
- lead_applications
- payments
- connections
- messages

## Required MVP Logic

Each buying lead must have:
- View Details
- Apply
- status
- payment CTA if buyer accepted
- chat entry if connected

Before connection:
- supplier can see full buying requirement
- supplier can see basic buyer profile
- buyer identity/contact hidden where needed

After payment/connection:
- buyer company/contact/website/email/WhatsApp/IM unlocked

## UI Rules

- Keep dashboard simple
- Keep buying leads central
- Keep per-connection payment
- Keep early offer wording if needed
- Keep no wallet/top-up

## Do Not Add

- promotion video card
- upload video CTA
- supplier showcase analytics
- wallet balance

---

# Page 5 — supplier-features-v2.html

## Role

Supplier feature explanation / internal feature page.

## Purpose

Explain supplier-side benefits and workflow:
- build profile
- receive relevant buying opportunities
- apply/connect
- pay per connection
- chat after unlock

## Core Objects

Mostly static.

Possible later:
- supplier profile status
- CTA to dashboard/profile setup

## UI Rules

- Keep consistent sidebar/top nav/logo
- Keep no video workflow
- Keep SourcingElf/Elfa wording consistent
- Keep feature explanation lightweight

## Do Not Add

- video creation tools
- promotional campaign builder
- complex analytics

---

# Page 6 — chat-v2.html

## Role

Post-connection IM workspace.

## Purpose

Enable buyer and supplier to communicate after connection/payment is unlocked.

## Core Objects

- connections
- messages
- notifications
- attachments/storage later

## Required MVP Logic

Chat should:
- only unlock after valid connection
- show buyer/supplier conversation
- allow message sending
- support file/image selection UI
- prepare for Supabase Realtime later

## Current UI Rules

- No footer
- Workspace style
- Keep clean message layout
- Keep minimal attachment UI
- Do not add marketing navigation
- Do not add complex chat features yet

## Future Integration

- Supabase Realtime messages
- Supabase Storage attachments
- unread count
- notifications

## Do Not Add

- public chat
- social features
- group chat
- unrelated CRM complexity

---

# Page 7 — admin-v2.html

## Role

Internal operation dashboard.

## Purpose

Admin manages:
- buyers
- suppliers
- buying leads
- applications
- connections
- payments
- messages
- settings

## Core Objects

Admin can inspect all tables:
- users
- supplier_profiles
- buyer_profiles
- buying_leads
- lead_applications
- connections
- payments
- messages
- notifications
- pricing_config

## Required MVP Logic

Admin should:
- view monthly + total metrics
- verify buyers
- review suppliers
- view leads
- view connections
- view payments
- inspect messages
- manage pricing/settings later

## UI Rules

- Lightweight SaaS admin dashboard
- No marketing-heavy footer
- Use simple copyright footer only
- Keep action buttons aligned
- Keep metrics clear
- Keep sidebar logo consistent

## Do Not Add

- complex BI dashboard
- many charts
- marketplace moderation tools beyond MVP
- video moderation

---

# Recommended First Claude Code Prompt

Use this as the first execution prompt:

```text
You are working on SourcingElf V2 frontend in Windows PowerShell.

Read these files first:
- CLAUDE.md
- STATUS.md
- DESIGN-SYSTEM-V2.md
- 7-PAGES-FRONTEND-PROMPTS.md

Rules:
- Do not redesign.
- Do not rewrite layouts.
- Do not migrate to React/Next/Vite.
- Do not modify files yet.
- Do not touch V1/main branch.
- Use V2 branch only.
- Keep output concise.
- No long thinking.

Task:
Inspect the current project structure only.

Output only:
1. Current branch
2. HTML files found
3. Asset/logo files found
4. CSS/JS locations
5. package.json / deployment files found
6. Any mismatch vs the 7 expected pages
7. Recommended next smallest step

Do not edit files.
Wait for approval before making changes.
```

---

# Recommended Second Claude Code Prompt

Use only after inspection is complete:

```text
Task:
Create a minimal frontend development structure for the existing 7 static HTML pages.

Rules:
- No redesign
- No layout changes
- Do not rewrite HTML content
- Do not migrate frameworks
- Preserve existing visual output
- Only organize files if necessary
- Before editing, list exact files to be changed
- After editing, summarize exact changes

Acceptance:
- All 7 pages remain accessible
- Logo/assets load correctly
- Cloudflare Pages can still deploy
- No visual redesign
```

---

# Notes

These prompts should be used as product/engineering instructions, not design generation prompts.

The finalized HTML pages are the current source of truth.
