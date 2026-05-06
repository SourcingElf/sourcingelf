# SourcingElf — 项目文档
**最后更新：2026-05-04**

---

## 项目概述

SourcingElf 是一个高端 B2B 服装采购平台，通过精准配对，将经过验证的服装制造商（供应商）与全球买家连接起来。平台由 AI 助手 **Elfa** 运营。

**域名：** sourcingelf.ai / sourcingelf.com
**AI 助手：** Elfa（行星轨道图标，深蓝色头像）

---

## 商业模式

### 核心收入
- 供应商每次成功连接买家支付 **US$138**（1 个 credit）
- 套餐定价：3 个 credit US$368 / 5 个 credit US$498
- 供应商申请 Buying Lead 时预扣 credit；若任务到期未成功连接，则退还 credit

### 两种连接路径
1. **请求路径**：Elfa 推广供应商视频 → 买家发送请求 → 供应商查看买家资料 → 确认连接 → 扣除 1 个 credit
2. **任务路径**：买家发布采购任务 → Elfa 邀请匹配的供应商 → 供应商申请（预扣 credit）→ 买家审核 → 确认连接 → 扣除 credit；若任务到期未连接 → 退还 credit

### 买家验证
所有买家必须经过 Elfa 验证（WhatsApp 联系 + 背景调查）才能被介绍给供应商。已验证买家可自动与新供应商配对。

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | HTML / CSS / JS（静态页面，由 Claude Design 生成） |
| 后端 | Python FastAPI |
| 数据库 | PostgreSQL（通过 Supabase） |
| 文件存储 | Supabase Storage |
| 身份验证 | Supabase Auth |
| 支付 | Stripe |
| 邮件 | Resend |
| 服务器部署 | Railway |
| 代码仓库 | GitHub（尚未设置） |
| AI 助手 | Claude（开发中） |

---

## 项目结构

```
C:\Projects\sourcingelf\
├── main.py                  # FastAPI 应用入口
├── config.py                # 环境变量（pydantic-settings）
├── database.py              # Supabase 连接 + JWT 验证
├── requirements.txt
├── .env                     # 绝不提交到代码库
├── database.sql             # 完整数据库 Schema（24 张表）
├── routers\
│   ├── auth.py              # 注册 / 登录 / JWT
│   ├── suppliers.py         # 供应商资料与管理（完成）
│   ├── buyers.py            # 买家资料与管理（完成）
│   ├── videos.py            # 推广视频工作流（完成）
│   ├── leads.py             # 采购 Lead 与申请（完成）
│   ├── credits.py           # Credits 与 Stripe 支付（完成）
│   ├── messages.py          # IM 聊天（完成）
│   └── admin.py             # 管理员操作（完成）
└── models\
    ├── user.py
    ├── supplier.py
    ├── buyer.py
    ├── video.py
    ├── lead.py
    └── credit.py

C:\Projects\sourcingelf-frontend\
├── inject_all.py            # 批量注入脚本 — 所有前端改动在这里，不要直接编辑 HTML
├── client.js                # API 客户端 — 所有页面共用
├── fix_*.py                 # 一次性修复脚本（保留备查）
└── *.html                   # 22 个生成的 HTML 页面（不要直接编辑）

C:\Projects\claude design backup\standalone\
└── *.html                   # 原始 HTML 备份 — 绝对不要动
```

---

## 前端架构（重要）

- 22 个 HTML 页面，均由原始备份 + inject_all.py 生成
- **绝不直接编辑 HTML 文件** — 下次运行 inject_all.py 时改动会被覆盖
- **所有逻辑改动写入 inject_all.py** → 运行 inject_all.py → 所有页面更新
- client.js 是共享 API 客户端，已注入每个页面的 `<head>`
- fix_*.py 是用来安全修改 inject_all.py 的一次性脚本
- **修改 inject_all.py 前必须用 debug 脚本 print(repr(...)) 确认真实内容和结束标记** — 不能靠 PowerShell 显示判断，因为中文和特殊字符会显示乱码
- **onclick 引号规则（重要）**：onclick 属性用双引号，里面的字符串必须用 &quot; 不能用单引号。这个错误已经发生过两次，每次都产生 SyntaxError。

---

## API 路由参考

所有路由前缀：`/api/v1/`

### 身份验证
- `POST /auth/register` — 注册
- `POST /auth/login` — 登录，返回 JWT + role ✅ 已测试
- `GET /auth/me` — 获取当前用户信息
- `PUT /auth/me` — 更新用户信息
- `POST /auth/me/last-login` — 记录最后登录时间

### 供应商
- `GET /suppliers/me/profile` — 获取自己的资料（含工厂/MOQ/认证/优势/市场）
- `POST /suppliers/me/profile` — 创建资料
- `PUT /suppliers/me/profile` — 更新资料
- `GET /suppliers/me/buyer-requests` — 获取收到的买家请求 ✅ 已测试
- `POST /suppliers/me/buyer-requests/{id}/connect` — 确认与买家连接
- `GET /suppliers/me/connected-buyers` — 获取已连接买家完整信息 ✅ 2026-05-03 新增
- （工厂、MOQ、认证、优势、市场的增删改 CRUD）

### 买家
- `GET /buyers/me/profile` — 获取自己的资料
- `POST /buyers/me/profile` — 创建资料
- `PUT /buyers/me/profile` — 更新资料
- `POST /buyers/requests` — 提交 Lead Form（无需登录）
- `GET /buyers/me/requests` — 获取我发出的请求（仅买家可用）

### 采购 Lead
- `GET /leads/browse` — 供应商浏览活跃 Lead（买家名称已遮码）
- `POST /leads` — 买家创建采购任务
- `GET /leads/me` — 买家查看自己的 Lead
- `GET /leads/{id}` — 获取 Lead 详情
- `PUT /leads/{id}` — 更新 Lead
- `DELETE /leads/{id}` — 取消 Lead
- `POST /leads/{id}/apply` — 供应商申请（预扣 1 个 credit）
- `GET /leads/{id}/applications` — 买家查看申请列表
- `POST /leads/{id}/applications/{app_id}/connect` — 买家确认连接

### Credits
- `GET /credits/me` — 余额 + 账户信息 ✅ 已测试
- `GET /credits/me/transactions` — 交易记录 ✅ 已测试
- `POST /credits/checkout` — 创建 Stripe 结账会话
- `POST /credits/webhook` — Stripe Webhook
- `GET /credits/me/payments` — 支付记录

### 消息
- `GET /messages/connections` — 列出所有连接（聊天列表）✅ 已测试
- `GET /messages/connections/{id}` — 获取连接中的消息
- `POST /messages/connections/{id}` — 发送消息
- `PUT /messages/connections/{id}/read` — 标记为已读

### 视频
- `GET /videos/me` — 获取自己的视频 ✅ 已测试
- `POST /videos/me/materials` — 提交制作素材
- `GET /videos/{id}` — 获取视频详情
- `POST /videos/{id}/approve` — 供应商批准草稿
- `POST /videos/{id}/revision` — 供应商申请修改（最多 1 次）
- `GET /videos/admin/all` — 管理员：列出所有视频
- `PUT /videos/admin/{id}` — 管理员：更新视频状态

### 管理员
- `GET /admin/users` — 列出所有用户
- `PUT /admin/users/{id}/status` — 更新用户状态
- `GET /admin/suppliers` — 列出供应商资料
- `PUT /admin/suppliers/{id}/verify` — 验证供应商
- `GET /admin/buyer-requests` — 列出买家请求
- `PUT /admin/buyer-requests/{id}/status` — 更新请求状态
- `GET /admin/buyers` — 列出买家资料
- `PUT /admin/buyers/{id}/verify` — 验证买家
- `POST /admin/credits/adjust` — 手动调整 credit
- `POST /admin/notes` — 创建管理员备注
- `GET /admin/notes/{user_id}` — 获取用户的管理员备注

---

## 业务逻辑 — 核心规则

1. **Credit 预扣**：供应商申请 Lead → 预扣 1 个 credit
2. **Credit 扣除**：买家确认连接 → 预扣转为正式扣除
3. **Credit 退还**：Lead 到期未连接 → 退还预扣 credit
4. **买家验证**：所有买家经 Elfa 验证后才能被介绍
5. **身份遮码（核心业务规则，绝不能违反）**：
   - 连接确认前，买家公司全名、姓名、所有联系方式必须隐藏
   - 公司名遮码显示（如 "A** Group"）
   - 可显示：业务性质、国家、年采购量、产品、定位、目标市场、留言
6. **每个 Lead 每个供应商只能申请一次**
7. **一个任务可以连接多个供应商**
8. **视频修改**：每个视频最多修改 1 次
9. **法律确认**：供应商必须接受 IP 条款才能发布视频
10. **请求有效期**：30 天
11. **Lead 有效期**：买家自定（最长 6 个月），少于 7 天时显示橙色警告
12. **Credit 确认弹窗**：每次 Connect 操作前必须弹出确认
13. **供应商必须先查看买家资料再决定连接**：卡片只有 View Profile 按钮，Connect Now 在弹窗里

---

## 数据库 — 24 张表

| 表名 | 用途 |
|------|------|
| `users` | 所有账户（供应商 / 买家 / 管理员） |
| `supplier_profiles` | 供应商公司详情 |
| `supplier_factories` | 工厂信息 |
| `supplier_moqs` | 各品类 MOQ |
| `supplier_certifications` | 认证文件 |
| `supplier_strengths` | 核心优势 |
| `supplier_markets` | 目标市场 |
| `buyer_profiles` | 买家公司详情 |
| `buyer_moqs` | 买家 MOQ 要求 |
| `buyer_markets` | 买家目标市场 |
| `videos` | 推广视频状态 |
| `video_materials` | 提交的制作素材 |
| `video_selling_points` | 视频卖点 |
| `buying_leads` | 买家采购任务 |
| `buying_lead_items` | 任务产品明细 |
| `lead_applications` | 供应商申请记录 |
| `buyer_requests` | 买家请求（来自 Lead Form） |
| `connections` | 已确认的连接记录 |
| `messages` | IM 聊天消息 |
| `credits` | 供应商 credit 余额 |
| `credit_transactions` | 所有 credit 变动记录 |
| `payments` | Stripe 支付记录 |
| `notifications` | 系统通知 |
| `admin_notes` | 管理员内部备注 |

### 已知 Schema 缺陷 — buyer_requests 缺少 MOQ 字段
- buyer_requests 表没有 MOQ 字段
- 当前临时方案：用 Target Market 替代卡片第4格
- 待解决：Lead Form 加 MOQ 填写栏 + buyer_requests 表加字段

---

## 当前状态（2026-05-04）

### 已完成 ✅
- 业务逻辑与需求确定
- 数据库 Schema（24 张表）已在 Supabase 创建
- Python FastAPI 后端 — 全部 8 个路由文件完成
- 服务器正常运行，POST /auth/login 测试通过
- 所有 22 个前端 HTML 页面完成 client.js 注入
- Dashboard 首页 — 三个数据卡片显示真实 API 数据
- **Supplier Requests 页面 — 完整重做（2026-05-03）**
  - 真实 API 数据、View Profile 弹窗、买家信息遮码、Connect Now 在弹窗内
- **Supplier Connected 页面 — JS 错误修复（2026-05-04）**
  - 修复上次对话引入的 onclick 引号错误
  - API 正常调用，显示"0 connections"（正确）
  - 卡片渲染逻辑完整，但无真实 connection 数据验证过
- **Dashboard Buying Leads — 接入真实 API（2026-05-04）**
  - 替换硬编码假卡片，改为真实 API 渲染
  - 已用 Supabase 测试数据验证，卡片正常显示
  - ⚠️ 分页仍显示硬编码"Page 1 of 3"，未修复
  - ⚠️ "Apply to this lead" 只是占位弹窗，未接入真实 API

### 进行中 ⏳
- IM Chat 页面对接
- 买家端（0% 未开始）

### 待处理 🔜
- Buying Leads 分页修复
- Buying Leads Apply 功能接入真实 API
- Supplier Connected 卡片用真实数据验证
- Stripe Webhook 设置（Railway 部署后）
- 部署到 Railway
- 域名 DNS 配置
- 端到端测试
- 上线

### 测试账号
| Email | Password | Role |
|-------|----------|------|
| test.supplier@sourcingelf.com | Test1234! | supplier |
| test.buyer@sourcingelf.com | 未设密码 | buyer |

### Supabase 测试数据
| 表 | ID / 记录 | 用途 |
|---|------|------|
| users（买家） | bae1599d-b815-4473-a248-52c76609a04d | 买家测试用户 |
| buyer_profiles | 8ea03203-0c55-44b6-acac-6f7085106aac | Test Buyer Co / US / Brand |
| buying_leads | 30837a3c-8b92-40bd-a817-b3334d06c599 | Women's Knitwear lead |
| buying_lead_items | （自动生成） | 500 pcs / Mid-range / Premium |
| buyer_requests | Sarah Johnson / Anthropologie Group / US / Brand | 测试 Requests 页面 |
| supplier_profiles | f37d3e21-3ed8-4eed-a9b9-017746239e75 | 供应商测试账号 |

---

## 定时任务（Cron）— 尚未实现

| 任务 | 频率 | 操作 |
|------|------|------|
| 任务到期处理 | 每天凌晨 2:00 | 使 Lead 到期，退还预扣 credit |
| 请求到期处理 | 每天凌晨 2:00 | 使 30 天前的买家请求到期 |
| 到期提醒 | 每天上午 9:00 | 通知买家任务将在 7 天内到期 |

---

## 第三方账号

| 服务 | 用途 | 控制台 |
|------|------|--------|
| Supabase | 数据库 + 存储 + 身份验证 | supabase.com/dashboard |
| Stripe | 支付（测试模式） | dashboard.stripe.com |
| Railway | 后端部署 | railway.app |
| Resend | 邮件（尚未集成） | resend.com |
| Namecheap | 域名 | namecheap.com |
