# SourcingElf V2 — Claude 工作手册

## 项目基本信息

- 域名：sourcingelf.ai
- 类型：服装行业B2B撮合平台，连接供应商与全球买家
- AI助手名称：Elfa
- 创始人：无技术背景，依赖Claude.ai开发

---

## 绝对规则

- v1文件在main分支，**永远不要碰**
- **所有开发只在V2分支操作**
- 每次修改前确认当前在V2分支
- 改代码前必须先完整看代码，不猜测
- 一次只改一个地方，验证后再commit
- 不确定就说不确定

---

## 技术栈

- 前端：HTML/CSS/JS 静态页面（无框架）
- 数据库：Supabase（项目名：sourcingelf-v2）
- 部署：Cloudflare Pages（自动部署V2分支）
- 支付：Stripe JS
- 邮件：Resend
- 代码：GitHub仓库 sourcingelf，V2分支

---

## Supabase 配置

- Project URL：`https://btdrdozwndvdvzoqteol.supabase.co`
- Anon Key：`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0ZHJkb3p3bmR2ZHZ6b3F0ZW9sIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg2NzM5MTEsImV4cCI6MjA5NDI0OTkxMX0.7-Ar0JuwwkSpRzBxXuHWXZL6W8Q6Kh7RFgfR_spl0p8`

SDK引入（每个页面head加）：
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
```

初始化方式：
```js
const { createClient } = supabase
const db = createClient(
  'https://btdrdozwndvdvzoqteol.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0ZHJkb3p3bmR2ZHZ6b3F0ZW9sIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg2NzM5MTEsImV4cCI6MjA5NDI0OTkxMX0.7-Ar0JuwwkSpRzBxXuHWXZL6W8Q6Kh7RFgfR_spl0p8'
)
```

---

## Logo

- 路径：`/SourcingElf%20Logo%20-%20PNG%20-%20%E9%80%8F%E6%98%8E%E5%BA%95.png`
- 浅色背景：正常显示，无filter
- 深色背景必须加：`filter: brightness(0) invert(1)`

---

## 定价

- 正式价：US$138/次连接
- 促销价：US$99/次连接
- 读取 `pricing_config` 表，`promo_active=true` 时用 `promo_fee`

---

## 页面清单（V2分支，7个静态页面）

| 文件名 | 功能 |
|--------|------|
| index.html | 主页 |
| supplier-landing-v2.html | 供应商登录注册 |
| supplier-dashboard-v2.html | 供应商控台 |
| supplier-features-v2.html | 供应商功能页 |
| buyer-portal-v2.html | 买家端 |
| chat-v2.html | IM聊天 |
| admin-v2.html | 管理后台（写死密码登录）|

---

## 核心业务流程

```
买家发邀请
→ lead_applications.status = 'buyer_accepted'
→ 通知供应商付款
→ 供应商Stripe付款成功
→ connections记录创建
→ IM聊天解锁
→ 邮件通知双方
```

---

## 角色与权限

| 角色 | 登录方式 | 权限 |
|------|----------|------|
| supplier | Supabase Auth | 只能读写自己的数据 |
| buyer | Supabase Auth | 只能读写自己的数据 |
| admin | 写死密码 | 用Service Role Key绕过RLS |

---

## RLS状态

- ✅ 19张表全部启用RLS，policies已设置完毕
- admin操作必须用Service Role Key，不能用anon key
- 前端只用anon key

---

## 数据库（19张表）

### 用户相关
- `users`：id, email, role(supplier/buyer/admin), created_at
- `supplier_profiles`：id, user_id, company_name, country, city, contact_name, contact_phone, website, description, status(pending/active/suspended), created_at
- `buyer_profiles`：id, user_id, company_name, country, contact_name, contact_phone, website, description, status(active/suspended), created_at

### 供应商详情
- `supplier_factories`：id, supplier_id, factory_size, workers_count, production_lines, annual_capacity
- `supplier_moqs`：id, supplier_id, moq_value, moq_unit
- `supplier_certifications`：id, supplier_id, cert_name, cert_number, expires_at
- `supplier_strengths`：id, supplier_id, strength
- `supplier_markets`：id, supplier_id, market

### 买家详情
- `buyer_moqs`：id, buyer_id, moq_value, moq_unit
- `buyer_markets`：id, buyer_id, market

### 业务核心
- `buying_leads`：id, buyer_id, title, category, description, quantity, quantity_unit, target_price, currency, destination, deadline, status(open/closed/cancelled)
- `buying_lead_items`：id, lead_id, item_name, quantity, unit, specs
- `lead_applications`：id, lead_id, supplier_id, buyer_id, status(pending/buyer_accepted/buyer_rejected/connected/cancelled), payment_id, payment_status(unpaid/paid/refunded), message
- `connections`：id, supplier_id, buyer_id, lead_id, payment_id, status(active/closed), unlocked_at
- `payments`：id, supplier_id, buyer_id, connection_id, lead_application_id, stripe_payment_intent_id, amount_usd, is_promo_price, status(pending/succeeded/failed/refunded), paid_at
- `messages`：id, connection_id, sender_id, content, read_at, created_at
- `notifications`：id, user_id, type, title, body, is_read, reference_id, reference_type
- `admin_notes`：id, admin_id, reference_id, reference_type, note
- `pricing_config`：id, standard_fee, promo_fee, promo_active, promo_expires_at, promo_description

### 页面与数据库对应

| 页面 | 主要用表 |
|------|----------|
| supplier-landing-v2.html | users, supplier_profiles |
| supplier-dashboard-v2.html | supplier_profiles, buying_leads, lead_applications, connections |
| buyer-portal-v2.html | users, buyer_profiles, buying_leads, lead_applications |
| chat-v2.html | connections, messages, notifications |
| admin-v2.html | 所有表（Service Role Key）|
