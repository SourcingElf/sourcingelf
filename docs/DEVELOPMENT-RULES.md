# SourcingElf V2 — DEVELOPMENT-RULES.md
更新时间：2026-05-19

---

# Purpose

This file defines how development should be done with Claude.ai and Claude Code.

The goal is to reduce token usage, prevent uncontrolled refactoring, and keep the MVP stable.

---

# Golden Rule

Claude Code executes.
It does not redesign.
It does not brainstorm.
It does not refactor unless explicitly approved.

---

# Development Mode

Use:
```text
small task → user checks → minimal fix → repeat
```

Do not use:
```text
big task → full rewrite → hope it works
```

---

# Before Every Claude Code Task

Claude Code must confirm:

1. current branch
2. files to be edited
3. exact task
4. no redesign
5. no unrelated changes

---

# Standard Claude Code Prompt Template

```text
Task:
[one small task only]

Files allowed to edit:
- [file name]

Rules:
- Do not redesign.
- Do not rewrite layout.
- Do not refactor unrelated code.
- Do not touch other files.
- Do not migrate framework.
- Keep existing UI.
- Minimal patch only.
- Before editing, list exact files you will change.
- After editing, summarize exact changes.

Acceptance:
- [clear test 1]
- [clear test 2]
- [clear test 3]
```

---

# Good Tasks

Examples:

```text
Fix logo path in admin-v2.html only.
```

```text
Connect supplier login form to Supabase Auth only.
```

```text
Add message insert logic to chat-v2.html only.
```

```text
Inspect project structure. Do not edit files.
```

---

# Bad Tasks

Avoid:

```text
Build the whole frontend.
```

```text
Refactor all pages.
```

```text
Make the app production ready.
```

```text
Improve the design.
```

```text
Optimize everything.
```

---

# Claude.ai Role

Claude.ai should:
- write precise prompts
- break work into small tasks
- review logic
- create implementation plans

Claude.ai should not:
- generate huge code rewrites
- create new designs
- make large architectural changes casually

---

# Claude Code Role

Claude Code should:
- inspect
- patch
- test
- report

Claude Code should not:
- decide new product logic
- invent new pages
- redesign
- migrate frameworks
- copy old V1 workflows

---

# User Review Role

After every change, user checks:
- screenshot
- Cloudflare deploy
- page visual
- console errors
- function behavior

Only after user approval:
- proceed to next task

---

# Stop Conditions

Stop and ask before continuing if:

- file is too large
- HTML is bundled/minified
- change requires touching many files
- schema seems missing
- old V1 logic appears
- unsure about workflow
- deployment config is unclear

---

# Commit Rules

Recommended after each successful task:

```text
git status
git add [changed files only]
git commit -m "Short clear message"
git push
```

Do not commit unrelated changes.

---

# Token Saving Rules

For Claude Code:
- concise output only
- no long explanation
- no brainstorming
- no alternative proposals unless requested
- report exact changes only

---

# Production Safety

Before touching live-facing behavior:
- backup file
- inspect first
- edit minimal section
- test locally
- deploy
- verify

---

# What Not To Reintroduce

Never reintroduce:
- supplier promotion video
- showcase video
- wallet/top-up
- Railway backend
- FastAPI backend
- old V1 route logic
- marketplace clutter
