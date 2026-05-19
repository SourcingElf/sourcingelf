# SourcingElf V2 — HOW-TO-USE-DOCS.md
更新时间：2026-05-19

---

# Purpose

This file explains how to use the SourcingElf V2 documentation set during development.

---

# Current Docs Set

Use these files together:

| File | Purpose |
|------|------|
| CLAUDE.md | Main project rulebook for Claude |
| STATUS.md | Current project state |
| DESIGN-SYSTEM-V2.md | UI/product design rules |
| 7-PAGES-FRONTEND-PROMPTS.md | Page-by-page frontend responsibilities |
| PROJECT-STRUCTURE.md | Folder and file organization |
| FRONTEND-FLOW.md | Buyer/supplier/admin/chat workflow |
| DATABASE-SCHEMA.md | Supabase table/field reference |
| ENVIRONMENT.md | Env variables and deployment notes |
| DEVELOPMENT-RULES.md | Claude.ai / Claude Code working rules |

---

# When Starting a New Claude.ai Chat

Paste or upload:

1. CLAUDE.md
2. STATUS.md
3. DESIGN-SYSTEM-V2.md
4. 7-PAGES-FRONTEND-PROMPTS.md
5. DEVELOPMENT-RULES.md

Then say:

```text
Use these as project rules. Do not redesign. Help me create the next smallest Claude Code prompt only.
```

---

# When Starting Claude Code

Give Claude Code:

1. CLAUDE.md
2. STATUS.md
3. PROJECT-STRUCTURE.md
4. DEVELOPMENT-RULES.md

For database tasks, also give:
```text
DATABASE-SCHEMA.md
```

For workflow tasks, also give:
```text
FRONTEND-FLOW.md
```

For UI tasks, also give:
```text
DESIGN-SYSTEM-V2.md
```

---

# First Claude Code Task

Recommended:

```text
Read:
- CLAUDE.md
- STATUS.md
- PROJECT-STRUCTURE.md
- DEVELOPMENT-RULES.md

Task:
Inspect current project structure only.

Rules:
- Do not edit files.
- Do not redesign.
- Do not refactor.
- Do not migrate framework.
- Keep output concise.

Output:
1. current branch
2. HTML files found
3. assets found
4. CSS/JS locations
5. deployment files found
6. mismatch vs expected 7 pages
7. next smallest step
```

---

# Which File To Use For Which Task

## UI bug / visual alignment

Use:
- DESIGN-SYSTEM-V2.md
- DEVELOPMENT-RULES.md

## Auth

Use:
- CLAUDE.md
- DATABASE-SCHEMA.md
- ENVIRONMENT.md
- FRONTEND-FLOW.md

## Buyer portal

Use:
- 7-PAGES-FRONTEND-PROMPTS.md
- FRONTEND-FLOW.md
- DATABASE-SCHEMA.md

## Supplier dashboard

Use:
- 7-PAGES-FRONTEND-PROMPTS.md
- FRONTEND-FLOW.md
- DATABASE-SCHEMA.md

## Payment

Use:
- FRONTEND-FLOW.md
- DATABASE-SCHEMA.md
- ENVIRONMENT.md

## Chat

Use:
- 7-PAGES-FRONTEND-PROMPTS.md
- FRONTEND-FLOW.md
- DATABASE-SCHEMA.md

## Admin

Use:
- 7-PAGES-FRONTEND-PROMPTS.md
- DATABASE-SCHEMA.md
- DEVELOPMENT-RULES.md

---

# Important Reminder

Do not upload everything for every task if token usage is high.

Use only the relevant files.

For example:
- UI fix: DESIGN + DEVELOPMENT only
- Database integration: DATABASE + FLOW + ENV
- Project setup: STRUCTURE + STATUS + CLAUDE

---

# Recommended Development Order

1. Project structure inspection
2. Asset/logo path stabilization
3. Local running
4. Supabase Auth
5. Supplier profile
6. Buyer profile
7. Buying leads
8. Applications
9. Stripe payment
10. Connections
11. Chat messages
12. Admin real data
13. Final testing
