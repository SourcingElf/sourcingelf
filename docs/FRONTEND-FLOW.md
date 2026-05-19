# SourcingElf V2 — FRONTEND-FLOW.md
更新时间：2026-05-19

---

# Purpose

This file defines the product workflow for SourcingElf V2 frontend development.

It prevents Claude Code from inventing new flows or reusing old V1 logic.

---

# Core MVP Flow

Buyer posts sourcing task
↓
Elfa/Admin matching
↓
Suppliers apply
↓
Buyer reviews suppliers
↓
Buyer accepts supplier / supplier is invited to connect
↓
Supplier pays per connection
↓
Connection is unlocked
↓
Buyer and supplier chat

---

# Buyer Flow

## 1. Buyer Entry

Buyer lands on:
```text
buyer-portal-v2.html
```

Buyer can:
- register/login
- create buyer profile
- create sourcing task
- use Elfa autofill/help where available

---

## 2. Create Sourcing Task

Buyer provides:
- product/category
- quantity/MOQ
- destination
- target price
- deadline
- specifications
- file upload if needed

Database:
- buying_leads
- buying_lead_items

---

## 3. Review Supplier Applications

Buyer can see suppliers that applied.

Before connection:
- buyer can see supplier basic profile
- supplier contact may remain hidden
- buyer can review details

Buyer actions:
- View Details
- Accept / shortlist supplier
- reject if needed

Database:
- lead_applications

---

## 4. Accept Supplier

When buyer accepts:

```text
lead_applications.status = buyer_accepted
```

Supplier is notified to pay.

---

## 5. Connection Unlock

After supplier payment succeeds:

- payment record becomes succeeded
- connection record is created
- lead_application becomes connected
- chat becomes available

Database:
- payments
- connections
- messages

---

# Supplier Flow

## 1. Supplier Entry

Supplier lands on:
```text
supplier-landing-v2.html
```

Supplier can:
- register/login
- submit profile
- paste official website / B2B profile link
- upload company file
- wait for review

Database:
- users
- supplier_profiles
- supplier_factories
- supplier_certifications
- supplier_strengths
- supplier_markets
- supplier_moqs

---

## 2. Supplier Dashboard

Supplier lands on:
```text
supplier-dashboard-v2.html
```

Supplier can:
- see relevant buying leads
- view details
- apply to leads
- track status
- pay when buyer accepts
- enter chat after connection unlock

---

## 3. Apply to Lead

Supplier actions:
- View Details
- Apply
- Send message/introduction

Database:
- lead_applications

Initial status:
```text
pending
```

---

## 4. Buyer Accepted

If buyer accepts:
```text
lead_applications.status = buyer_accepted
payment_status = unpaid
```

Supplier sees:
- Pay & Start Chatting
- connection fee
- early offer if active

---

## 5. Pay Per Connection

Supplier pays one-time fee.

No:
- wallet
- subscription
- credits top-up

---

## 6. Chat Unlock

After payment:
- chat becomes active
- buyer/supplier contact info unlocked
- IM conversation starts

---

# Chat Flow

Page:
```text
chat-v2.html
```

Chat is available only when:
```text
connections.status = active
```

MVP functions:
- send message
- show message history
- basic attachment/file selection UI
- prepare for Supabase Realtime later

Not MVP:
- public chat
- group chat
- community features
- CRM automation

---

# Admin Flow

Page:
```text
admin-v2.html
```

Admin manages:
- buyers
- suppliers
- leads
- applications
- connections
- payments
- messages
- pricing

Admin dashboard should show:
- monthly suppliers + total suppliers
- monthly buyers + total buyers
- monthly connections + total connections
- monthly revenue + total revenue

---

# Payment Flow

Current payment model:
```text
pay per connection
```

Default:
- Standard price: US$138
- Promo price: US$99 if active

Payment provider:
- Stripe

After successful payment:
1. update payments.status = succeeded
2. create/update connections record
3. update lead_applications.status = connected
4. update lead_applications.payment_status = paid
5. unlock chat
6. notify buyer and supplier

---

# Removed Flow

Do not reintroduce:

- supplier promotion video
- video upload
- supplier showcase
- wallet balance
- credits top-up
- subscription
- generic marketplace browsing
- complex bidding system
