# SourcingElf — 项目文档
**最后更新：2026-05-04（session 2）**

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
| 前端 | HTML / CSS / JS（静态页面） |
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
├── main.py
├── config.py
├── database.py
├── requirements.txt
├── .env
├── database.sql
├── routers\
│   ├── auth.py
│   ├── suppliers.py
│   ├── buyers.py
│   ├── videos.py
│   ├── leads.py
│   ├── credits.py
│   ├── messages.py
│   └── admin.py
└── models\
    ├── user.py
    ├── supplier.py
    ├── buyer.py
    ├── video.py
    ├── lead.py
    └── credit.py

C:\Projects\sourcingelf-frontend\
├── inject_all.py
├── client.js
├── fix_*.py
└── *.html（22个生成页面）

C:\Projects\claude design backup\standalone\
└── *.html（原始备份，绝不修改）
```

---

## 前端架构（重要）

- 22 个 HTML 页面，均由原始备份 + inject_all.py 生成
- **绝不直接编辑 HTML 文件**
- **所有逻辑改动写入 inject_all.py** → 运行 → 所有页面更新
- client.js 是共享 API 客户端，已注入每个页面
- **买家端原始 HTML 是打包压缩格式** — 不要用 PowerShell 读原始文件，用浏览器 F12 → 元素查看真实结构
- **拦截买家端链接必须用 document capture**：
  ```javascript
  document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (link && link.href && link.href.includes('dashboard.html')) {
      e.preventDefault();
      e.stopPropagation();
      doLogin();
    }
  }, true);
  ```
- **onclick 引号规则**：onclick 属性用双引号，里面字符串必须用 &quot; 不能用单引号

---

## 当前状态（2026-05-04 session 2）

### 已完成 ✅
- 业务逻辑与需求确定
- 数据库 Schema（24 张表）已在 Supabase 创建
- Python FastAPI 后端 — 全部 8 个路由文件完成
- 所有 22 个前端 HTML 页面完成 client.js 注入
- 供应商 Dashboard — 三个数据卡片显示真实 API 数据
- 供应商 Dashboard — Buying Leads 接入真实 API
- 供应商 Requests 页面 — View Profile 弹窗、买家信息遮码、Connect Now 在弹窗内
- **供应商 Connected 页面 — onclick 引号错误已修复（session 2）**

### ❌ 买家登录——未完成，下次第一优先
原始 HTML 里 Log In 按钮是 `<a href="dashboard.html">`，点击直接跳转，绕过我们的登录逻辑。
解决方案：用 `document.addEventListener('click', handler, true)` capture phase。
详见 HANDOFF.md。

### 待处理 ⏳
- 买家登录（第一优先）
- 买家 Dashboard
- 买家发布采购任务
- 买家查看供应商申请并确认连接
- IM Chat（需要完整重写）
- Buying Leads Apply 接入真实 API
- Dashboard 分页修复
- 部署到 Railway

### 测试账号
| Email | Password | Role |
|-------|----------|------|
| test.supplier@sourcingelf.com | Test1234! | supplier |
| test.buyer@sourcingelf.com | Test1234! | buyer |

### Supabase 测试数据
| 表 | ID / 记录 | 用途 |
|---|------|------|
| users（买家） | bae1599d-b815-4473-a248-52c76609a04d | 买家测试用户 |
| buyer_profiles | 8ea03203-0c55-44b6-acac-6f7085106aac | Test Buyer Co / US / Brand |
| buying_leads | 30837a3c-8b92-40bd-a817-b3334d06c599 | Women's Knitwear lead |
| buyer_requests | Sarah Johnson / Anthropologie Group | 测试 Requests 页面 |
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
