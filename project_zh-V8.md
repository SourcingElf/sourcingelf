# SourcingElf — 项目文档
**最后更新：2026年4月28日**

---

## 项目概述

SourcingElf 是一个专业B2B服装采购撮合平台，通过精心策划的对接方式，连接经过审核的服装供应商与全球买家。平台由AI助手 **Elfa** 负责运营管理。

**域名：** sourcingelf.ai / sourcingelf.com
**AI助手：** Elfa（星球轨道图标，深蓝头像）

---

## 商业模式

### 核心收入
- 供应商每次与买家成功对接，支付 **US$138（1个credit）**
- 套餐优惠：3个credits US$368 / 5个credits US$498
- 申请采购任务时预扣credit；若任务到期未成功对接，则退还credit

### 两条对接路径
1. **Request路径**：Elfa推广供应商视频 → 买家发出请求 → 供应商查看买家背景 → 确认对接 → 扣减1个credit
2. **Task路径**：买家创建采购任务 → Elfa邀请匹配供应商 → 供应商申请（预扣credit）→ 买家审核 → 确认对接 → 正式扣减credit；若任务到期无对接 → 退还credit

### 买家验证机制
所有买家必须经Elfa验证（WhatsApp联系+背景核查）后，才能与供应商对接。已验证买家可自动被介绍给新供应商。

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | HTML / CSS / JS（静态文件，由Claude Design生成） |
| 后端 | Python FastAPI |
| 数据库 | PostgreSQL（via Supabase） |
| 文件存储 | Supabase Storage |
| 用户认证 | Supabase Auth |
| 支付 | Stripe |
| 邮件通知 | Resend |
| 服务器部署 | Railway |
| 代码仓库 | GitHub |
| 开发工具 | Claude Code |

---

## 项目文件结构

```
C:\Projects\sourcingelf\
├── main.py                  # FastAPI 应用入口
├── config.py                # 环境变量配置
├── database.py              # Supabase 数据库连接
├── requirements.txt         # Python 依赖包
├── .env                     # 环境变量（不提交到GitHub）
├── database.sql             # 完整数据库建表语句（24张表）
├── routers/
│   ├── __init__.py
│   ├── auth.py              # 注册 / 登录 / JWT
│   ├── suppliers.py         # 供应商资料与管理
│   ├── buyers.py            # 买家资料与管理
│   ├── videos.py            # 推广视频工作流
│   ├── leads.py             # 采购任务与申请
│   ├── credits.py           # Credits与Stripe支付
│   ├── messages.py          # IM聊天
│   └── admin.py             # 管理后台操作
└── models/
    ├── __init__.py
    ├── user.py
    ├── supplier.py
    ├── buyer.py
    ├── video.py
    ├── lead.py
    └── credit.py
```

---

## 数据库 — 24张表

| 表名 | 用途 |
|------|------|
| `users` | 所有账号（供应商/买家/Admin） |
| `supplier_profiles` | 供应商公司详细资料 |
| `supplier_factories` | 工厂信息（一个供应商可多个） |
| `supplier_moqs` | 按品类的最低起订量 |
| `supplier_certifications` | 认证证书（含文件URL） |
| `supplier_strengths` | 核心卖点 |
| `supplier_markets` | 目标市场（含份额百分比） |
| `buyer_profiles` | 买家公司详细资料 |
| `buyer_moqs` | 买家MOQ要求 |
| `buyer_markets` | 买家目标市场 |
| `videos` | 推广视频状态与文件信息 |
| `video_materials` | 供应商提交的视频制作素材 |
| `video_selling_points` | 每个视频的卖点条目 |
| `buying_leads` | 买家采购任务 |
| `buying_lead_items` | 采购任务明细 |
| `lead_applications` | 供应商申请采购任务 |
| `buyer_requests` | 买家向特定供应商发出的请求 |
| `connections` | 已确认的供应商-买家对接记录 |
| `messages` | IM聊天消息（永久保存） |
| `credits` | 供应商credit余额 |
| `credit_transactions` | 所有credit交易明细 |
| `payments` | Stripe支付记录 |
| `notifications` | 系统通知 |
| `admin_notes` | 管理员对用户的内部备注 |

### Credit交易类型说明
- `topup` — Stripe付款成功，充值
- `reserved` — 申请采购任务，预扣
- `deducted` — 对接确认，正式扣减
- `refunded` — 任务到期无对接，退还
- `manual_add` / `manual_deduct` — 管理员手动调整

---

## API端点（规划中）

### 认证
- `POST /auth/register` — 注册供应商或买家账号
- `POST /auth/login` — 登录，返回JWT令牌
- `POST /auth/logout` — 退出登录

### 供应商
- `GET /suppliers/me` — 获取自己的资料
- `PUT /suppliers/me` — 更新资料
- `GET /suppliers/{id}` — 获取指定供应商（买家/管理员用）

### 买家
- `GET /buyers/me` — 获取自己的资料
- `PUT /buyers/me` — 更新资料
- `POST /buyers/lead-form` — 提交Lead Form（无需登录）

### 推广视频
- `GET /videos/me` — 获取自己的视频状态
- `POST /videos/materials` — 提交制作素材
- `POST /videos/approve` — 批准草稿视频
- `POST /videos/revision` — 申请修改

### 采购任务
- `GET /leads` — 获取活跃任务列表（供应商）
- `POST /leads` — 创建采购任务（买家）
- `POST /leads/{id}/apply` — 申请采购任务（供应商，预扣credit）
- `GET /leads/{id}/applications` — 查看申请列表（买家）
- `POST /leads/{id}/connect/{application_id}` — 确认对接

### Credits
- `GET /credits/me` — 余额与交易记录
- `POST /credits/topup` — 发起Stripe支付
- `POST /credits/webhook` — Stripe Webhook回调

### 消息
- `GET /messages/{connection_id}` — 获取聊天记录
- `POST /messages/{connection_id}` — 发送消息

### 管理后台
- `GET /admin/suppliers` — 所有供应商列表
- `GET /admin/buyers` — 所有买家列表
- `PUT /admin/buyers/{id}/verify` — 标记买家为已验证
- `GET /admin/videos/pending` — 待审核视频列表
- `POST /admin/videos/{id}/approve` — 批准视频发布
- `POST /admin/credits/manual` — 手动调整credits

---

## 环境变量

```env
# Supabase
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_PUBLISHABLE_KEY=sb_publishable_xxxx
SUPABASE_SECRET_KEY=sb_secret_xxxx
DATABASE_URL=postgresql://postgres.[ref]:[password]@pooler.supabase.com:5432/postgres
DB_PASSWORD=xxxx

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_xxxx
STRIPE_SECRET_KEY=sk_test_xxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxx（部署时配置）

# Resend
RESEND_API_KEY=re_xxxx

# 应用
SECRET_KEY=xxxx（随机字符串，用于JWT签名）
ENVIRONMENT=development
```

---

## 账号与服务

| 服务 | 用途 | 网址 |
|------|------|------|
| Supabase | 数据库+存储+认证 | supabase.com |
| Stripe | 支付处理 | stripe.com |
| Railway | 后端服务器部署 | railway.app |
| Resend | 邮件通知 | resend.com |
| GitHub | 代码仓库 | github.com |
| Namecheap | 域名注册商 | namecheap.com |

**已拥有域名：** sourcingelf.ai / sourcingelf.com

---

## 设计资产

### Claude Design项目
**链接：** claude.ai/design/p/019dce81-2365-7044-9094-ceb31d7e2f1e

| 页面 | 状态 | 文件名 |
|------|------|--------|
| 主页 Homepage | ✅ 完成 | index.html |
| 供应商登录注册 | ✅ 完成 | supplier-landing |
| 供应商控台 | ✅ 完成 | supplier-dashboard |
| 供应商功能页 | ✅ 完成 | supplier-features |
| 买家端 Buyer Portal | ⏳ 5月5日 | — |
| IM聊天 | ⏳ 5月5日 | — |
| 管理后台 Admin | ⏳ 5月5日 | — |

### 品牌色彩
- 深蓝 Navy：`#1a2744`（供应商端主色）
- 深海蓝 Navy Deep：`#0f1a2e`（深色背景）
- 红色 Red：`#b91c1c`（买家端主色）
- 亮红 Red Bright：`#dc2626`（悬停状态）

### 字体
- 标题：Playfair Display（衬线体）
- 正文/UI：DM Sans（无衬线体）

### Logo
- 文件：`SourcingElf_Logo-20260404.png`
- 深色版（浅色背景）：原图
- 浅色版（深色背景）：CSS `filter: brightness(0) invert(1)`

---

## 核心业务逻辑规则

1. **Credit预扣**：供应商提交采购任务申请 → 预扣1个credit（锁定余额）
2. **Credit扣减**：买家确认对接 → 预扣转为正式扣减
3. **Credit退还**：采购任务到期无对接 → 预扣credit自动退还
4. **买家验证**：所有买家必须经Elfa验证后才能与供应商对接
5. **身份遮码**：对接确认前，买家公司名隐藏（显示为"A** Fashion Ltd"）
6. **防重复申请**：同一供应商对同一采购任务只能申请一次
7. **多次对接**：同一任务，买家可与多个供应商对接，不受限制
8. **视频修改**：每个视频最多允许供应商申请1次修改
9. **法律确认**：供应商发布视频前必须确认知识产权条款
10. **请求过期**：买家请求30天后自动过期
11. **任务过期**：采购任务在买家设定的日期过期（最长6个月）

---

## 定时任务（Cron Jobs）

| 任务 | 频率 | 执行内容 |
|------|------|---------|
| 任务过期处理 | 每天凌晨2:00 | 将过期任务标记expired，退还预扣credits |
| 请求过期处理 | 每天凌晨2:00 | 将30天未回应的买家请求标记expired |
| 到期提醒 | 每天上午9:00 | 通知买家7天内将过期的采购任务 |

---

## 当前项目状态（2026年4月28日）

### 已完成 ✅
- 业务逻辑与需求全面确认
- 数据库设计（24张表）
- Supabase建表完成
- Python FastAPI后端框架搭建（21个文件）
- 所有依赖包安装完毕
- 服务器成功启动
- API连接Supabase（注册接口可用）
- Claude Design完成4个页面
- 所有第三方账号注册完毕
- 所有API Keys保存完毕

### 进行中 ⏳
- 登录API测试
- 供应商Profile API
- 剩余设计页面（5月5日）

### 即将开始 🔜
- 完成所有API路由
- 前端HTML页面（来自Claude Design）
- 前端接API
- Stripe Webhook配置
- 部署到Railway
- 域名DNS配置
- 端到端测试
- 正式上线

---

## 注意事项

- Claude Design 5月5日重置，届时继续完成买家端、IM聊天、管理后台
- Stripe目前处于**测试模式**，上线前需切换为真实账户
- Railway目前有30天/US$5免费试用，正式部署后需升级
- Supabase免费额度适合MVP阶段，流量增长后升级Pro（US$25/月）
- 视频文件存储在Supabase Storage，数据库只存URL引用
- 管理后台V1仅桌面端，不需要手机端适配
- V1阶段：Elfa = 人工Admin操作 + 系统邮件通知（暂无AI自动化）
