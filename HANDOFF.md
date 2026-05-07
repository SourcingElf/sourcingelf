# SourcingElf 交接文档
**最后更新：2026-05-07**

---

## 启动步骤（每次开发前）

```
窗口1：cd C:\Projects\sourcingelf → uvicorn main:app --reload
窗口2：cd C:\Projects\sourcingelf-frontend → python -m http.server 3000
浏览器验证：http://localhost:3000/Supplier%20Dashboard%20-%20Home.html
```

---

## 给新对话的第一件事

**不要假设上次收工时一切正常。**
每次开始工作，必须先打开浏览器，打开 F12 Console，确认没有红色报错，才能开始。
上次对话就是因为没有做这步，带着错误收工，浪费了今天大量时间。

---

## 最容易犯的错误（必须牢记）

### 引号嵌套错误
在 JavaScript 的 onclick 属性里，外层是双引号，里面绝对不能用单引号。

```
❌ 错误（会产生 SyntaxError: Unexpected identifier）：
onclick="window.location.href='IM Chat.html'"
onclick="alert('Apply feature coming soon')"

✅ 正确（用 &quot; 代替单引号）：
onclick="window.location.href=&quot;IM Chat.html&quot;"
onclick="alert(&quot;Apply feature coming soon&quot;)"
```

**每次写任何包含 onclick 的代码，写完必须立即检查引号，再给出文件。**

### 买家端原始 HTML 是打包格式
- 无法用 PowerShell debug 脚本读取元素结构
- 必须用浏览器 F12 → 元素标签查看渲染后的真实结构
- 拦截链接必须用 document capture（见下方买家登录说明）

---

## 测试账号

| Email | Password | Role |
|-------|----------|------|
| test.supplier@sourcingelf.com | Test1234! | supplier |
| test.buyer@sourcingelf.com | Test1234! | buyer |

---

## 测试数据（Supabase 已插入）

| 表 | ID | 内容 |
|---|------|------|
| users（买家） | **dcc3f777-c350-4286-9436-af2081118958** | test.buyer@sourcingelf.com（UUID 已修正） |
| buyer_profiles | 8ea03203-0c55-44b6-acac-6f7085106aac | Test Buyer Co / US / Brand |
| buying_leads | 30837a3c-8b92-40bd-a817-b3334d06c599 | Women's Knitwear lead（+ 用户今天新增了几条） |
| buying_lead_items | （自动生成） | 500 pcs / Mid-range / Premium |
| buyer_requests | Sarah Johnson | Anthropologie Group / US / Brand |
| supplier_profiles | f37d3e21-3ed8-4eed-a9b9-017746239e75 | 供应商测试账号 |

---

## 前端对接进度（2026-05-06）

### ✅ 已完成并在浏览器验证通过
- 22/22 页面注入 client.js
- 供应商登录流程
- Supplier Dashboard — 三个数据卡片（真实数据）+ Buying Leads 卡片
- Supplier Requests — View Profile 弹窗 + 买家信息遮码 + Connect Now
- Supplier Connected — API 正常
- **买家登录** — document capture phase 方案，验证通过 ✅
- **买家 Dashboard** — 接入真实 API（connections + active leads 计数）✅
- **买家 Create Task** — document capture 拦截 tasks.html 链接，表单提交接入 createLead API ✅

### ⚠️ 已做但未在浏览器验证（下次必须先验证）
- **Buyer Applications** — 脚本已注入，逻辑：加载所有 lead 的申请，绑定 Connect 到真实 API，待验证

### ✅ 2026-05-07 新增完成
- **Bug 6c（Buyer 导航加 Messages 入口）** — injectBuyerMessagesNav 改为三次重试 [300,800,1500]ms，验证通过 ✅
- **Bug 6b（Buyer Dashboard 数据卡片等宽等高）** — 删除 metrics-row 幽灵 `<a>` 元素 + inline style，验证通过 ✅
- **Supplier Apply to Lead 接入真实 API** — 弹窗 + `POST /api/v1/leads/{id}/apply` 全链路打通；修复 bundle renderer 在 DOMContentLoaded 覆盖 `window.applyToLead` 的竞争问题（改为在 `renderLeadsPage()` 之后赋值）✅
- **Apply 后卡片状态更新** — 申请成功/400 重复申请均调用 `markCardApplied`，按钮变灰色 "Applied ✓"，NEW 标签消失 ✅
- **Buying Leads 卡片 UI 统一** — `buildLeadCard` 改为与 bundled template 一致的富结构：`detail-item`、日历 SVG、`view-details-btn`、`lead-id` footer、`pill pill-red`，`appliedLeadIds` Set 保持翻页后申请状态 ✅
- **inject_all.py 停用** — 所有修改直接在 `sourcingelf/frontend/*.html` 进行；`Copy-Item *.html` 已同步所有页面到部署目录 ✅

### ⚠️ 已知问题（待处理）
- **Dashboard 分页**："Page 1 of 3" 是假数据
- **IM Chat** 需完整重写

### ⏳ 下一步（按优先级）
1. IM Chat 页面重写
2. Dashboard 分页修复（真实分页逻辑）

---

## 关键技术规则

### inject_all.py 已停用
不再运行 inject_all.py。所有修改直接编辑 `C:\Projects\sourcingelf\frontend\*.html`，同时同步更新 `C:\Projects\sourcingelf-frontend\*.html`（如有需要）。

### JWT
Supabase 用 ES256，PyJWT verify_signature=False，不要改 database.py。

### client.js
- API_BASE_URL = http://localhost:8000（不加 /api/v1）
- token 存在 localStorage，key 是 'token'

### 工作方式
- 一次只做一件事
- 做完立即浏览器验证（页面 + Console）
- 确认没问题才进行下一步
- 不要在没有验证的情况下收工

---

## 重要技术记录

### 买家端所有链接用 document capture 拦截
买家端 HTML 是打包格式，按钮都是 `<a href="xxx.html">` 直接跳转。
**必须用 `document.addEventListener('click', handler, true)` 拦截**，不要用 MutationObserver 或 setInterval。
判断条件：`link.href.includes('xxx.html')`，然后 `e.preventDefault() + e.stopPropagation()`。

### test.buyer UUID 已修正（2026-05-06）
- 原 users 表 id（手动插入错误）: bae1599d-b815-4473-a248-52c76609a04d
- 正确 Supabase Auth UUID: dcc3f777-c350-4286-9436-af2081118958
- fix_buyer_uuid.py 已执行：删旧记录 → 用新 UUID 重建 → buyer_profiles.user_id 同步更新

## 修改文件记录

### 2026-05-06
| 文件 | 改动 |
|------|------|
| inject_all.py | 买家登录：document capture 方案 |
| inject_all.py | Buyer Dashboard：接入 connections + active leads API |
| inject_all.py | Buyer Create Task：document capture 拦截 + createLead API |
| inject_all.py | Buyer Applications：加载申请 + Connect API（待验证） |
| routers/fix_buyer_uuid.py | 修正买家 UUID 不匹配（已执行，可删） |

### 2026-05-07
| 文件 | 改动 |
|------|------|
| frontend/Buyer Portal - Dashboard.html | Bug 6b：删幽灵 `<a>`，加 inline style 等高等宽；Bug 6c：Messages 导航入口 |
| frontend/Supplier Dashboard - Home.html | Apply to Lead 全链路：弹窗+API+卡片状态；buildLeadCard 富结构；bundle renderer 竞争修复 |
| frontend/*.html | Copy-Item 从 sourcingelf-frontend 同步所有页面 |
| requirements.txt | 加 email-validator（修复 Railway 启动崩溃） |
