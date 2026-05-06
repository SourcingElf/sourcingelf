# SourcingElf 交接文档
**最后更新：2026-05-03 23:00**

---

## 启动步骤（每次开发前）

```
窗口1：cd C:\Projects\sourcingelf → uvicorn main:app --reload
窗口2：cd C:\Projects\sourcingelf-frontend → python -m http.server 3000
浏览器：http://localhost:3000/Supplier%20Dashboard%20-%20Connected.html
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

### client.js 关键规则
- `API_BASE_URL` = `http://localhost:8000` — **不要加 /api/v1**
- client.js 里所有函数路径已经带完整 `/api/v1/xxx`
- token 存在 localStorage 的 key 是 `token`（不是 `se_token`）
- **修改前必须先用 PowerShell Select-String 查清楚相关代码，确认无误才动手**

### 前端架构
- 22个 HTML 文件，原始备份在 `Claude Design Backup\standalone\`
- 修改页面逻辑：只改 inject_all.py，重新运行，不要直接编辑 HTML
- 运行 inject_all.py 会从备份重新生成所有页面，注入最新逻辑

---

## 重要业务决定记录

### Supplier Requests 页面的核心设计改动（2026-05-03）

**改动原因：**
原设计卡片上直接有 Connect Now 按钮，信息太少（只有4个字段），
供应商在不了解买家背景的情况下就要决定花 US$138，体验很差。

**新设计流程：**
1. 卡片显示基本信息（国家、买家类型、年采购量、目标市场、产品、过期日）
2. 卡片按钮改为：**View Profile**（主要）+ **Not Interested**
3. View Profile → 弹窗显示完整买家背景（遮码）
4. Connect Now 按钮移到弹窗里，看完资料再决定

**遮码规则（业务规则，不能改）：**
- 公司名：遮码 → 首字母 + ** + 最后一个字，例如 "A** Group"
- 姓名：完全隐藏
- Email / Phone / WhatsApp：完全隐藏
- 显示 "Revealed after connection" 提示
- 其他信息（业务性质、国家、年采购量、产品、定位、留言）：全部可见

**Connect Now 逻辑：**
- credits = 0 时：按钮禁用，显示 "Top up now →" 链接
- credits > 0 时：调用真实 API `POST /api/v1/suppliers/me/buyer-requests/{id}/connect`
- 成功后：卡片消失，显示 toast "Connected! Open chat →"

### MOQ 问题（待解决）
- buyer_requests 表没有 MOQ 字段
- 暂时不显示 MOQ，用 Target Market 替代第4格
- 未来方案：Lead Form 加 MOQ 填写栏 + buyer_requests 表加字段

### Supplier Connected 页面架构决定（2026-05-03 晚）

**问题：** GET /messages/connections 只返回 connection 记录（buyer_id 等 uuid），没有买家名字、公司、国家等显示信息。

**决定：新增专用端点（方案C），不改现有端点**
- 原因：改现有端点会影响买家端将来使用同一端点，风险高
- 新端点：`GET /api/v1/suppliers/me/connected-buyers`
- 位置：suppliers.py 末尾
- 返回：connection 记录 + buyer_profiles 信息合并，一次调用搞定
- client.js 新增：`SE.SupplierAPI.getConnectedBuyers()`

**Connected 页面功能：**
- 从真实 API 加载已连接买家列表
- 显示：买家姓名首字母头像、公司名、国家、买家类型、产品、连接日期
- 搜索功能：按公司、国家、类型、产品过滤
- Open Chat 按钮跳转到 IM Chat.html
- 无数据时显示 "No connections yet."

**注意：Connected 页面尚未用真实 connection 数据测试**
- 测试账号目前在 Supabase 没有 connection 记录
- 需要在 Supabase 手动插入一条 connection 记录才能验证卡片渲染
- 或等买家端完成后，走完整流程测试

---

## 后端端点测试结果

| 端点 | 状态 | 备注 |
|------|------|------|
| POST /auth/login | ✅ | 返回 JWT + role |
| GET /auth/me | ✅ | |
| GET /suppliers/me/profile | ✅ | |
| GET /suppliers/me/buyer-requests | ✅ | 2026-05-02 新增 |
| GET /suppliers/me/connected-buyers | ✅ | 2026-05-03 新增，返回空数组正常 |
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

## 前端对接进度（2026-05-03 23:00）

### ✅ 已完成
- 22/22 页面批量注入 client.js 完成
- 登录流程正常
- Dashboard Home — 三个数据卡片真实数据 ✅
- **Supplier Requests 页面 — 完整重做 ✅（2026-05-03）**
  - 真实 API 数据
  - View Profile 弹窗 + 买家信息遮码
  - Connect Now 移入弹窗 + Credits 余额检查
- **Supplier Connected 页面 — 真实 API 逻辑注入 ✅（2026-05-03 晚）**
  - 调用 SE.SupplierAPI.getConnectedBuyers()
  - 卡片渲染逻辑完整
  - 搜索过滤功能
  - ⚠️ 尚未用真实数据验证，需插入 Supabase 测试记录

### ⏳ 下一步（按优先级）

1. **验证 Connected 页面** — 在 Supabase connections 表插入一条测试记录，确认卡片正常渲染
   - 需要：supplier_id（f37d3e21-3ed8-4eed-a9b9-017746239e75）
   - 需要：一个 buyer_profiles 的 id（先查 Supabase）

2. **Buying Leads 页面** — 改成真实 API 数据
   - 目前是硬编码假数据
   - API 已有：`SE.LeadsAPI.browseLeads()`
   - 工作量较大

3. **IM Chat 页面对接**

4. **买家端**（需新建买家测试账号）

5. **部署到 Railway**

---

## 测试数据（Supabase 已插入）

| 表 | 数据 | 用途 |
|---|------|------|
| buyer_requests | Sarah Johnson / Anthropologie Group / US / Brand | 测试 Requests 页面 |

- supplier_id：`f37d3e21-3ed8-4eed-a9b9-017746239e75`
- status：pending
- expires_at：2026-06-02

---

## 已知 Bug 状态

| # | 问题 | 状态 |
|---|------|------|
| 6a | Buyer Applications Connect 确认弹窗 | ✅ 已修复 |
| 6b | 买家控台数据卡片宽度不等 | ⏳ 待修复 |
| 6c | 买家端导航缺少 Messages 入口 | ⏳ 待修复 |
| 6d | 供应商 Requests Connect Now 确认弹窗 | ✅ 已被新 View Profile 设计取代 |

---

## 今晚修改的文件（2026-05-03 晚）

| 文件 | 改动内容 |
|------|---------|
| C:\Projects\sourcingelf\routers\suppliers.py | 末尾新增 GET /me/connected-buyers 端点 |
| C:\Projects\sourcingelf-frontend\client.js | SupplierAPI 新增 getConnectedBuyers() 函数 |
| C:\Projects\sourcingelf-frontend\inject_all.py | Connected 页面 section 替换为真实 API 逻辑 |

**今晚产生的临时文件（可删可留，不影响系统）：**
- fix_connected_endpoint.py
- fix_client_connected.py
- fix_connected_page.py
- debug_connected.py
- connected_section.txt

---

## 备份位置

| 备份 | 内容 |
|------|------|
| C:\Projects\sourcingelf_backup_20260502 | 后端初始备份 |
| C:\Projects\sourcingelf_backup_jwt_fixed | JWT 修复后 |
| C:\Projects\更新-2026年5月2日 | 昨日 client.js + inject_all.py |
| C:\Projects\更新-2026年5月3日（下午） | Requests 页面重做版本 |
| C:\Projects\更新-2026年5月3日（晚） | Connected 页面版本（今晚） |
| C:\Projects\claude design backup\standalone\ | 所有原始 HTML 文件（勿动） |
