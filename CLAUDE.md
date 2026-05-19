# SourcingElf V2 — Claude 工作手册

## 项目基本信息

- 域名：sourcingelf.ai
- 类型：服装行业AI辅助B2B撮合平台（全球服装供应链）
- AI助手名称：Elfa
- 当前阶段：V2 MVP
- 当前策略：静态HTML页面 + 最小工程化开发
- 创始人：非技术背景，采用 AI-assisted development workflow

---

# 当前开发原则（极其重要）

## V2 是全新前端工程

V1 不再作为开发基础。

V1 仅作为参考资料使用：

可参考：
- Supabase配置
- Stripe配置
- Resend配置
- GitHub/部署经验
- 部分Auth逻辑

禁止复用：
- V1页面结构
- Railway/FastAPI架构
- video showcase workflow
- wallet/top-up系统
- 旧supplier流程
- 旧routes/state逻辑

---

# 绝对规则

- v1文件在 main 分支，永远不要碰
- 所有开发只在 V2 分支操作
- 每次修改前确认当前在 V2 分支
- 改代码前必须先完整阅读代码
- 不允许猜测代码结构
- 一次只改一个地方
- 用户人工检查后再继续
- 不确定必须明确说不确定
- 不允许大规模重构 bundled HTML

---

# Product Philosophy

SourcingElf is not a complex marketplace.

It is a lightweight AI-assisted sourcing connection platform focused on high-quality business matching.

The product should remain:
- simple
- premium
- lightweight
- operationally efficient

Future intelligence should come mainly from:
- Elfa AI
- better matching
- workflow automation
- sourcing intelligence
- buyer/supplier quality scoring

NOT from:
- complex page structures
- marketplace clutter
- social/community features
- heavy supplier showcase systems

---

# 当前 MVP 核心逻辑

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

# 当前已确认移除功能

以下功能已从V2删除：

- Supplier promotion video
- Showcase video workflow
- Wallet / top-up balance system
- Complex supplier marketing pages
- Railway backend deployment
- FastAPI architecture
- Complex marketplace flow

---

# 技术栈（V2）

## 前端

- HTML / CSS / Vanilla JS
- 静态页面
- 无React
- 无Next.js
- 无复杂框架
- Cloudflare Pages部署

## Backend-as-a-Service

- Supabase
- Auth
- Database
- Storage
- Realtime（后期）

## Payments

- Stripe Checkout
- One-time payment only

## Email

- Resend

## Code Hosting

- GitHub（V2 branch）

---

# 当前7个正式页面（Source of Truth）

| 页面 | 文件 |
|------|------|
| Homepage | index.html |
| Buyer Portal | buyer-portal-v2.html |
| Supplier Landing | supplier-landing-v2.html |
| Supplier Dashboard | supplier-dashboard-v2.html |
| Supplier Features | supplier-features-v2.html |
| Chat | chat-v2.html |
| Admin | admin-v2.html |

以上页面已经：
- UI freeze
- wording统一
- logo统一
- footer统一
- Elfa icon统一
- MVP逻辑统一

不要重新设计。

---

# 前端开发策略

## 正确方向

Static HTML
↓
工程化整理
↓
Supabase integration
↓
Stripe integration
↓
Realtime/chat
↓
Deploy MVP

## 错误方向（禁止）

- React重构
- Next.js迁移
- Tailwind重构
- 大规模UI重写
- 无限优化动画
- 重新设计页面

---

# Claude.ai 工作方式

Claude.ai 负责：

- 任务拆分
- Prompt生成
- 架构建议
- 小步开发计划

不负责：
- 大规模代码生成
- 页面重构

---

# Claude Code 工作方式

Claude Code 只负责：

- 小任务执行
- 最小patch修改
- 精准代码修改

Claude Code 禁止：

- 自主重构
- redesign
- framework migration
- 大规模replace
- touching unrelated files
- long explanations
- long thinking

---

# Claude Code Prompt原则

始终强调：

- No redesign
- Minimal edits only
- Small tasks only
- Do not refactor
- Do not rewrite layouts
- Keep existing UI
- Do not touch unrelated files
- Wait for approval before major edits

---

# 当前开发阶段

## 当前阶段：

Frontend Engineering Setup

目标：
- 整理前端结构
- 稳定本地运行
- Cloudflare稳定部署
- 准备Supabase integration

当前不要开发：
- realtime
- advanced AI
- automation
- analytics

---

# 推荐开发顺序

1. Inspect current frontend structure
2. Organize assets/CSS/JS
3. Make all 7 pages stable
4. Setup navigation
5. Connect Supabase Auth
6. Connect database
7. Stripe payment
8. Chat/realtime
9. Final testing

---

# Supabase 配置

Project URL：
https://btdrdozwndvdvzoqteol.supabase.co

当前：
- 19张表
- RLS已完成
- Auth已开启

注意：
Admin 必须使用 Service Role Key
Frontend 只能使用 anon key

---

# 定价逻辑

标准价：
US$138 / connection

促销价：
US$99 / connection

当前MVP：
- pay per connection
- no wallet
- no subscription

---

# Logo 规则

统一使用：

SourcingElf-Logo.png

深色背景：
- 必须 invert/filter

浅色背景：
- 正常显示

禁止：
- 混用旧logo
- emoji logo
- 多种Elfa icon

---

# Chat 页面原则

Chat属于：
workspace/app interface

因此：
- 不使用marketing footer
- 不加入复杂导航
- 保持类似Slack/Intercom风格

---

# Admin 页面原则

Admin：
- lightweight
- operational
- SaaS dashboard feel

不要：
- marketing footer
- heavy navigation
- excessive branding

