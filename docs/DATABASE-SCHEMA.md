# SourcingElf V2 — DATABASE-SCHEMA.md
更新时间：2026-05-19

---

# Purpose

This file summarizes the Supabase database schema for frontend development.

It is based on the SourcingElf V2 SQL schema.

Use this file to prevent Claude Code from guessing table names or fields.

---

# Database Overview

Total tables:
```text
19
```

Database type:
```text
Supabase PostgreSQL
```

RLS:
```text
Enabled
```

Frontend:
```text
Use anon key only
```

Admin:
```text
Requires Service Role Key / server-side admin method
```

---

# Tables

## 1. users

Purpose:
Basic user identity and role.

Fields:
- id
- email
- role: supplier / buyer / admin
- created_at

---

## 2. supplier_profiles

Purpose:
Supplier company profile.

Fields:
- id
- user_id
- company_name
- country
- city
- contact_name
- contact_phone
- website
- description
- status: pending / active / suspended
- created_at

---

## 3. supplier_factories

Purpose:
Supplier factory information.

Fields:
- id
- supplier_id
- factory_size
- workers_count
- production_lines
- annual_capacity
- created_at

---

## 4. supplier_moqs

Purpose:
Supplier MOQ information.

Fields:
- id
- supplier_id
- moq_value
- moq_unit
- created_at

---

## 5. supplier_certifications

Purpose:
Supplier certifications.

Fields:
- id
- supplier_id
- cert_name
- cert_number
- expires_at
- created_at

---

## 6. supplier_strengths

Purpose:
Supplier strengths / tags.

Fields:
- id
- supplier_id
- strength
- created_at

---

## 7. supplier_markets

Purpose:
Supplier target markets.

Fields:
- id
- supplier_id
- market
- created_at

---

## 8. buyer_profiles

Purpose:
Buyer company profile.

Fields:
- id
- user_id
- company_name
- country
- contact_name
- contact_phone
- website
- description
- status: active / suspended
- created_at

---

## 9. buyer_moqs

Purpose:
Buyer purchase quantity/MOQ data.

Fields:
- id
- buyer_id
- moq_value
- moq_unit
- created_at

---

## 10. buyer_markets

Purpose:
Buyer markets.

Fields:
- id
- buyer_id
- market
- created_at

---

## 11. buying_leads

Purpose:
Buyer sourcing task / buying lead.

Fields:
- id
- buyer_id
- title
- category
- description
- quantity
- quantity_unit
- target_price
- currency
- destination
- deadline
- status: open / closed / cancelled
- created_at

---

## 12. buying_lead_items

Purpose:
Line items/specs inside a buying lead.

Fields:
- id
- lead_id
- item_name
- quantity
- unit
- specs
- created_at

---

## 13. payments

Purpose:
Stripe payment records.

Fields:
- id
- supplier_id
- buyer_id
- connection_id
- lead_application_id
- stripe_payment_intent_id
- amount_usd
- is_promo_price
- status: pending / succeeded / failed / refunded
- paid_at
- created_at

---

## 14. connections

Purpose:
Unlocked buyer-supplier connection.

Fields:
- id
- supplier_id
- buyer_id
- lead_id
- payment_id
- status: active / closed
- unlocked_at
- created_at

---

## 15. lead_applications

Purpose:
Supplier applications to buying leads.

Fields:
- id
- lead_id
- supplier_id
- buyer_id
- status: pending / buyer_accepted / buyer_rejected / connected / cancelled
- payment_id
- payment_status: unpaid / paid / refunded
- message
- created_at

---

## 16. messages

Purpose:
IM chat messages.

Fields:
- id
- connection_id
- sender_id
- content
- read_at
- created_at

---

## 17. notifications

Purpose:
System notifications.

Fields:
- id
- user_id
- type
- title
- body
- is_read
- reference_id
- reference_type
- created_at

---

## 18. admin_notes

Purpose:
Internal admin notes.

Fields:
- id
- admin_id
- reference_id
- reference_type
- note
- created_at

---

## 19. pricing_config

Purpose:
Pricing and promo settings.

Fields:
- id
- standard_fee
- promo_fee
- promo_active
- promo_expires_at
- promo_description
- updated_at
- updated_by

---

# Key Status Values

## lead_applications.status

Allowed:
- pending
- buyer_accepted
- buyer_rejected
- connected
- cancelled

## lead_applications.payment_status

Allowed:
- unpaid
- paid
- refunded

## payments.status

Allowed:
- pending
- succeeded
- failed
- refunded

## connections.status

Allowed:
- active
- closed

---

# Page-to-Table Mapping

| Page | Tables |
|------|------|
| supplier-landing-v2.html | users, supplier_profiles |
| supplier-dashboard-v2.html | supplier_profiles, buying_leads, lead_applications, payments, connections |
| buyer-portal-v2.html | users, buyer_profiles, buying_leads, buying_lead_items, lead_applications |
| chat-v2.html | connections, messages, notifications |
| admin-v2.html | all tables |
| index.html | mostly static |
| supplier-features-v2.html | mostly static |

---

# Important Rule

Claude Code must not invent new tables or fields unless explicitly approved.

If a needed field is missing, report first.
Do not silently create schema changes.
