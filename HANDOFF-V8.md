# SourcingElf 交接文档
**最后更新：2026-05-02 23:00**

---

## 启动步骤（每次开发前）

```
窗口1：cd C:\Projects\sourcingelf → uvicorn main:app --reload
窗口2：cd C:\Projects\sourcingelf-frontend → python -m http.server 3000
浏览器：http://localhost:3000/Supplier%20Landing.html
```

---

## 测试账号

| Email | Password | Role |
|-------|----------|------|
| test.supplier@sourcingelf.com | Test1234! | supplier |

---

## 项目文件位置

| 内容 | 路径 |
|------|------|
| 后端 FastAPI | C:\Projects\sourcingelf\routers\ |
| 前端 HTML（已注入） | C:\Projects\sourcingelf-frontend\ |
| 原始 HTML 备份 | C:\Projects\claude design backup\standalone\ |

---

## 关键技术决定（已确认，不要改动）

### JWT 验证
- Supabase 用 ES256 非对称算法
- 解决方案：PyJWT，options={"verify_signature": False}
- 文件：database.py

### client.js 关键规则（2026-05-02 确认）
- `API_BASE_URL` = `http://localhost:8000` — **不要加 /api/v1**
- client.js 里所有函数路径已经带完整 `/api/v1/xxx`
- token 存在 localStorage 的 key 是 `token`（不是 `se_token`）
- **修改前必须先用 PowerShell Select-String 查清楚相关代码，确认无误才动手**

### 前端架构
- 22个 HTML 文件，React JSX + Babel（浏览器实时编译）
- 修改页面逻辑：只改 inject_all.py，重新运行，不要直接编辑 HTML
- 原始 HTML 备份不要动

---

## 后端端点测试结果（全部通过）

| 端点 | 状态 | 备注 |
|------|------|------|
| POST /auth/login | ✅ | 返回 JWT + role |
| GET /auth/me | ✅ | |
| GET /suppliers/me/profile | ✅ | |
| GET /suppliers/me/buyer-requests | ✅ | 2026-05-02 新增 |
| POST /suppliers/me/profile | ✅ | |
| GET /messages/connections | ✅ | |
| GET /leads/browse | ✅ | |
| GET /credits/me | ✅ | |
| GET /credits/me/transactions | ✅ | |
| GET /videos/me | ✅ | |
| GET /buyers/me/profile | ✅ 403 | supplier 无权，正确 |
| GET /leads/me | ✅ 403 | supplier 无权，正确 |
| GET /admin/users | ✅ 403 | supplier 无权，正确 |

---

## 前端对接进度（2026-05-02 23:00）

### ✅ 已完成
- 22/22 页面批量注入 client.js 完成
- 登录流程正常（Supabase登录 → JWT存入localStorage → 跳转Dashboard）
- Dashboard Home — Credits 真实数据 ✅
- Dashboard Home — Connected Buyers 真实数据 ✅（原假数据"14"）
- Dashboard Home — New Buyer Requests 真实数据 ✅（原假数据"3"）
- Dashboard Home — 侧边栏 nav-badge 同步更新 ✅
- 所有页面路由守卫已配置
- Connect 确认弹窗已注入（Bug 6a/6d）

### ⏳ 下一步（按优先级）

1. **Supplier Requests 页面** — 列表从 API 加载真实买家请求
   - API 已有：`SE.SupplierAPI.getMyBuyerRequests()`
   - 需要先查清楚页面 HTML 结构（CSS class、容器 id），再写注入脚本
   - 操作：Select-String 查 Supplier Dashboard - Requests.html，找卡片容器

2. **Supplier Connected 页面** — 列表从 API 加载已连接买家
   - API 已有：`SE.MessagesAPI.getMyConnections()`
   - 需要查清楚页面结构再动手

3. **Buying Leads — 改成真实 API 数据**
   - 目前是写死假数据（const leads = [...] 硬编码在 HTML 里）
   - 需要替换整个 leads 数组逻辑，改为调用 SE.LeadsAPI.browseLeads()
   - 工作量较大，放在 Requests 和 Connected 之后

4. **IM Chat 页面对接**

5. **买家端**（需新建买家测试账号）

6. **部署到 Railway**

---

## 已知 Bug 状态

| # | 问题 | 状态 |
|---|------|------|
| 6a | Buyer Applications Connect 确认弹窗 | ✅ 已修复 |
| 6b | 买家控台数据卡片宽度不等 | ⏳ 待修复 |
| 6c | 买家端导航缺少 Messages 入口 | ⏳ 待修复 |
| 6d | 供应商 Requests Connect Now 确认弹窗 | ✅ 已修复 |

---

## 备份位置

| 备份 | 内容 |
|------|------|
| C:\Projects\sourcingelf_backup_20260502 | 后端初始备份 |
| C:\Projects\sourcingelf_backup_jwt_fixed | JWT 修复后 |
| C:\Projects\更新-2026年5月2日 | 今日最新 client.js + inject_all.py |
| C:\Projects\claude design backup\standalone\ | 所有原始 HTML 文件（勿动） |
