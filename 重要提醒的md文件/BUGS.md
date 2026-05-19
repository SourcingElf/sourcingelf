# SourcingElf V2 — Bugs & Issues

## Open Bugs

### 2026-05-14
- Claude Design bundle HTML causes huge Claude Code token usage
- supplier-landing-v2.html auth integration incomplete
- buyer-portal-v2.html logo display issue

## Fixed Bugs

### 2026-05-14
- chat-v2.html logo fixed
- supplier-features-v2.html logo fixed
- index.html footer logo fixed
- Cloudflare Pages connected to V2 branch

## Known Risks

- Bundle HTML files are difficult for Claude Code to patch safely
- Avoid large-scale refactor on bundled pages
- Avoid letting Claude Code read entire project context
- Prefer minimal patch modifications only

## Future Improvements

- Split bundle pages into modular JS/components
- Separate auth.js
- Separate supabase.js
- Reduce bundle size
- Reduce Claude Code token consumption
