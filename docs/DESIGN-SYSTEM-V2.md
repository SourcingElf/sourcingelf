# SourcingElf V2 — Global Design System
版本：V2 Clean MVP
更新时间：2026-05-19

---

# Product Direction

SourcingElf is a lightweight AI-assisted sourcing connection platform for global apparel trade.

The platform focuses on:
- high-quality business matching
- operational simplicity
- premium B2B workflow
- curated buyer/supplier connections

The system is NOT intended to become:
- a cluttered marketplace
- a social platform
- a video-centric supplier showcase system

---

# Current MVP Workflow

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

# Design Philosophy

## Core Principles

- Premium
- Minimal
- Lightweight
- Operational
- SaaS-style workflow
- Clear hierarchy
- High trust feeling

Avoid:
- marketplace clutter
- excessive animations
- overloaded dashboards
- complicated navigation
- too many colors
- visual noise

---

# Brand Colors

| Name | Color | Usage |
|------|------|------|
| Navy Deep | #0f1a2e | Hero background / dark sections |
| Navy | #1a2744 | Main text / buttons / nav |
| Red | #b91c1c | CTA / buyer actions |
| Red Bright | #dc2626 | Hover / active |
| White | #ffffff | Background / cards |
| Gray 50 | #f8f7f5 | Section background |
| Gray 100 | #eeecea | Borders |
| Gray 400 | #9ca3af | Secondary text |
| Gray 600 | #4b5563 | Body text |
| Green | #16a34a | Success / connected |
| Amber | #d97706 | Pending / warning |

---

# Typography

## Fonts

Headings:
- Playfair Display

Body/UI:
- DM Sans

Google Fonts:
https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap

---

# Logo System

## Primary Logo

Current file:
SourcingElf-Logo.png

## Usage Rules

Light background:
- normal display

Dark background:
- use:
filter: brightness(0) invert(1)

## Recommended Sizes

| Usage | Height |
|------|------|
| Top navigation | 36px |
| Sidebar | 28px |
| Footer | 32px |
| Admin login | 34px |

---

# Elfa System

## Elfa Philosophy

Elfa is:
- an AI sourcing assistant
- operational guidance
- workflow assistance

Elfa is NOT:
- a chatbot-first experience
- a social AI companion
- an animated assistant

## Elfa Visual Rules

- Use one unified Elfa icon only
- Consistent navy background
- Consistent white symbol
- No emoji variants
- No mixed SVG styles

---

# Layout Principles

## General

- Large spacing
- Minimal borders
- Clean alignment
- Soft radius
- Clear typography hierarchy

## Radius

| Component | Radius |
|------|------|
| Cards | 12px–14px |
| Buttons | 6px–8px |
| Inputs | 6px–8px |
| Modals | 14px |

---

# Navigation Rules

## Marketing Pages

Pages:
- homepage
- supplier landing
- supplier features

Use:
- full footer
- branding
- navigation

## Workspace Pages

Pages:
- supplier dashboard
- buyer portal
- chat
- admin

Use:
- lightweight operational layout
- reduced marketing elements

---

# Footer Rules

## Marketing Footer

Use on:
- homepage
- supplier landing
- supplier features
- buyer portal

Footer copy:

AI-assisted sourcing connections for global apparel trade.

© 2026 SourcingElf.ai All rights reserved.

## Chat Footer

Chat pages should NOT use marketing footer.

Chat should feel like:
- Slack
- Intercom
- operational workspace

## Admin Footer

Admin uses lightweight copyright footer only.

No:
- social links
- legal clutter
- marketing sections

---

# Chat Design Rules

## Chat Philosophy

Chat is:
- post-payment communication
- business workflow
- operational communication

NOT:
- social messaging
- public community

## Chat UI

- Clean bubbles
- Minimal colors
- Lightweight toolbar
- Attachment support
- Workspace feeling

---

# Admin Design Rules

## Admin Philosophy

Admin should feel like:
- lightweight SaaS dashboard
- operational backend
- efficient workflow tool

Avoid:
- heavy enterprise complexity
- too many charts
- over-designed dashboards

## Admin Metrics

Preferred structure:
- large monthly metric
- small total cumulative metric

Example:

14
Connections This Month
186 total connections

---

# Buttons

## Primary Buttons

- Navy or Red
- Medium weight
- Clean spacing
- No oversized shadows

## Small Action Buttons

- Consistent width
- Center aligned
- No arrow icons

Preferred:
Verify
Review
View

Avoid:
Verify →
Review →
View →

---

# Current MVP Removed Features

The following features are intentionally removed from V2 MVP:

- promotion video workflow
- supplier showcase videos
- wallet/top-up system
- complex supplier marketing flows
- advanced marketplace discovery
- heavy analytics
- social/community features

---

# Payment System

## Current Payment Logic

- one-time payment
- pay per connection
- Stripe Checkout

## Pricing

Standard:
US$138

Promo:
US$99

---

# Frontend Engineering Principles

## Extremely Important

- Static HTML is source of truth
- No redesign during development
- Minimal patch workflow
- No uncontrolled refactor
- No framework migration
- Small iterative development only

---

# Claude Code Rules

Claude Code should:
- execute small tasks only
- avoid redesign
- avoid refactor
- avoid unrelated edits
- avoid long explanations

Workflow:
1. inspect
2. small edit
3. user checks
4. minimal fix
5. repeat

---

# Deployment

Frontend:
- Cloudflare Pages

Backend:
- Supabase

Payments:
- Stripe

Email:
- Resend

Code:
- GitHub V2 branch

