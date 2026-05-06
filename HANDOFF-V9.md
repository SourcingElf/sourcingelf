# SourcingElf 交接文档
**最后更新：2026-05-03 12:30**

---

## 启动步骤（每次开发前）

```
窗口1：cd C:\Projects\sourcingelf → uvicorn main:app --reload
窗口2：cd C:\Projects\sourcingelf-frontend → python -m http.server 3000
浏览器：http://localhost:3000/Supplier%20Dashboard%20-%20Requests.html
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

## 重要业务决定记录（2026-05-03 新增）

### Supplier Requests 页面的核心设计改动

**改动原因：**
原设计卡片上直接有 Connect Now 按钮，信息太少（只有4个字段），
供应商在不了解买家背景的情况下就要决定花 US$138，体验很差。
供应商在 connect 前需要充分了解买家背景，MOQ 是关键筛选条件之一。

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

**弹窗显示字段：**
- Company（遮码）、Buyer Type、Country、Target Market
- Annual Volume、Positioning
- Products Interested In
- Message from Buyer（如果有）
- Contact Details（隐藏提示）
- Credit 扣款提示 + 余额显示

**Connect Now 逻辑：**
- credits = 0 时：按钮禁用，显示 "Top up now →" 链接
- credits > 0 时：调用真实 API `POST /api/v1/suppliers/me/buyer-requests/{id}/connect`
- 成功后：卡片消失，显示 toast "Connected! Open chat →"

### MOQ 问题（待解决）
- buyer_requests 表没有 MOQ 字段
- buyer_profiles 有 buyer_moqs 表，但 Lead Form 买家可能没注册（buyer_id = null）
- 暂时不显示 MOQ，用 Target Market 替代第4格
- 未来方案：Lead Form 加 MOQ 填写栏 + buyer_requests 表加字段

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

## 前端对接进度（2026-05-03 12:30）

### ✅ 已完成
- 22/22 页面批量注入 client.js 完成
- 登录流程正常（Supabase登录 → JWT存入localStorage → 跳转Dashboard）
- Dashboard Home — Credits 真实数据 ✅
- Dashboard Home — Connected Buyers 真实数据 ✅
- Dashboard Home — New Buyer Requests 真实数据 ✅
- Dashboard Home — 侧边栏 nav-badge 同步更新 ✅
- 所有页面路由守卫已配置
- **Supplier Requests 页面 — 完整重做 ✅（2026-05-03）**
  - 真实 API 数据（替换硬编码假数据）
  - View Profile 弹窗（新增）
  - 买家信息遮码逻辑（新增）
  - Connect Now 移入弹窗，调真实 API（新增）
  - Credits 余额检查，0时禁用按钮（新增）
  - Not Interested 功能保留

### ⏳ 下一步（按优先级）

1. **Supplier Connected 页面** — 列表从 API 加载已连接买家
   - API 已有：`SE.MessagesAPI.getMyConnections()`
   - 需要先查清楚页面 HTML 结构（CSS class、容器 id），再写注入脚本

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
| buyer_requests | Sarah Johnson / Anthropologie Group（遮码：A** Group）/ US / Brand | 测试 Requests 页面 |

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

## 备份位置

| 备份 | 内容 |
|------|------|
| C:\Projects\sourcingelf_backup_20260502 | 后端初始备份 |
| C:\Projects\sourcingelf_backup_jwt_fixed | JWT 修复后 |
| C:\Projects\更新-2026年5月2日 | 昨日 client.js + inject_all.py |
| C:\Projects\更新-2026年5月3日 | 今日 inject_all.py（Requests 页面重做）|
| C:\Projects\claude design backup\standalone\ | 所有原始 HTML 文件（勿动） |
