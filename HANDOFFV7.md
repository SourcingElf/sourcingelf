# SourcingElf 交接文档
**最后更新：2026-05-02**

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
| 后端 FastAPI | C:\Projects\sourcingelf\ |
| 前端 HTML（已注入） | C:\Projects\sourcingelf-frontend\ |
| 原始 HTML 备份 | C:\Projects\claude design backup\standalone\ |
| 设计规格 md 文件 | 随此文档一起保存 |

---

## 关键技术决定

### JWT 验证
- Supabase 用 ES256 非对称算法
- 解决方案：PyJWT，options={"verify_signature": False}
- 文件：database.py

### 前端架构
- 22个 HTML 文件，Claude Design 生成，格式为 React JSX + Babel（浏览器实时编译）
- API 对接方式：每个 HTML 注入 client.js + 页面专属脚本
- **登录方式：Supabase 直接登录**（signIn → 拿 JWT → 调 FastAPI /auth/me）
- Google/Apple 登录已在 client.js 准备好，上线配置域名后可用

### 关键文件
- `client.js` — 统一 API 客户端，放在 C:\Projects\sourcingelf-frontend\
- `inject_all.py` — 批量注入脚本，从备份重新生成所有 HTML
- 修改所有页面逻辑：只需更新 inject_all.py 里的 PAGE_SCRIPTS，重新运行即可

### 文件修改规则
- 永远用 notepad 写 Python 脚本
- 永远不要直接编辑输出的 HTML，要改就改 inject_all.py 再重跑
- 原始 HTML 备份不要动，永远从备份注入

---

## 后端端点测试结果（2026-05-02 全部通过）

| 端点 | 状态 | 备注 |
|------|------|------|
| POST /auth/login | ✅ | 返回 JWT + role |
| GET /auth/me | ✅ | |
| GET /suppliers/me/profile | ✅ | |
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

## 前端对接进度（2026-05-02）

### ✅ 已完成
- 22/22 页面批量注入 client.js 完成
- Supplier Landing.html — 登录功能正常（Supabase 直接登录）
- Supplier Dashboard - Home.html — Credits 真实数据显示（0）
- 所有页面路由守卫已配置（requireSupplier / requireBuyer / requireAdmin）
- Connect 确认弹窗已注入（Bug 6a/6d 修复）

### ⏳ 下一步（按优先级）

1. **验证登录完整流程**
   - 浏览器测试 Supplier Landing → 登录 → Dashboard
   - F12 Console 确认无报错
   - 确认 token 存入 localStorage 正确

2. **Supplier Dashboard - Home**
   - New Buyer Requests 数字对接 API
   - Connected Buyers 数字对接 API
   - 用户名对接 GET /auth/me

3. **Supplier Dashboard - Credits**
   - 余额显示、交易记录、Stripe Top Up

4. **Supplier Dashboard - Requests**
   - 买家请求列表从 API 加载

5. **Supplier Dashboard - Connected**
   - 已连接买家列表

6. **IM Chat**
   - 消息列表、发送消息

7. **买家端**（需新建买家测试账号）

8. **部署到 Railway**（上线后才能测试 Google/Apple 登录）

---

## 已知 Bug 状态

| # | 问题 | 状态 |
|---|------|------|
| 6a | Buyer Applications Connect 确认弹窗 | ✅ 已注入 |
| 6b | 买家控台数据卡片宽度不等 | ⏳ 待修复 |
| 6c | 买家端导航缺少 Messages 入口 | ⏳ 待修复 |
| 6d | 供应商 Requests Connect Now 确认弹窗 | ✅ 已注入 |

---

## 备份位置

| 备份 | 内容 |
|------|------|
| C:\Projects\sourcingelf_backup_20260502 | 后端初始备份 |
| C:\Projects\sourcingelf_backup_jwt_fixed | JWT 修复后 |
| C:\Projects\claude design backup\standalone\ | 所有原始 HTML 文件（勿动） |
