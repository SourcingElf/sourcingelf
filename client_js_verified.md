# client.js 函数验证清单

**最后更新：2026-05-08（Day 0 基线）**
**client.js 路径**：`frontend/api/client.js`（547 行）
**全局暴露**：`window.SourcingElf.{CONFIG, AuthAPI, SupplierAPI, BuyerAPI, VideoAPI, LeadsAPI, CreditsAPI, MessagesAPI, AdminAPI, TokenManager, RouteGuard, FormHelper, NotificationHelper, apiFetch}`

---

## 维护规则

- **每完成一页验证**，把当页用到的 client.js 函数从"未验证"挪到"已验证"
- 标注**该函数被哪个页面验证**过（一个函数可被多个页面验证）
- 改 client.js 函数签名时，把所有调用过它的页面回归一遍

---

## 已验证（11 个核心 API + 6 个辅助）

通过 7 个已浏览器验证流程的实际调用得出。

### API 调用（11）

| 函数 | 验证页面 |
|------|---------|
| `AuthAPI.login` | Supplier Landing, Buyer Portal - Register Login |
| `AuthAPI.register` | Supplier Landing, Buyer Portal - Register Login |
| `LeadsAPI.browseLeads` | Supplier Dashboard - Home |
| `LeadsAPI.applyToLead` | Supplier Dashboard - Home |
| `LeadsAPI.getMyApplications` | Supplier Dashboard - Home (D0-2026-05-09 verified) |
| `LeadsAPI.createLead` | Buyer Portal - Create Task |
| `LeadsAPI.getMyLeads` | Buyer Portal - Dashboard |
| `CreditsAPI.getMyCredits` | Supplier Dashboard - Home (apply pre-check), Requests, **Credits (D1)** |
| `CreditsAPI.getMyTransactions` | Supplier Dashboard - Credits (D1) |
| `CreditsAPI.createCheckout` | Supplier Dashboard - Credits — Top Up button (D1, via redirectToCheckout) |
| `CreditsAPI.redirectToCheckout` | Supplier Dashboard - Credits — Top Up Stripe flow (D1) |
| `MessagesAPI.getMyConnections` | Buyer Portal - Dashboard |
| `SupplierAPI.getConnectedBuyers` | Supplier Dashboard - Connected (bundle 占位调用，D 阶段重写) |
| `SupplierAPI.getMyBuyerRequests` | Supplier Dashboard - Requests |
| `apiFetch`（底层） | Supplier Dashboard - Requests; 422 detail 数组解析已验证 |
| `VideoAPI.getMyVideos` | Supplier Dashboard - Video (D3) |
| `VideoAPI.submitMaterials` | Supplier Dashboard - Video Submit (D3) |
| `VideoAPI.approveVideo` | Supplier Dashboard - Video — Confirm Publish (D3) |
| `VideoAPI.requestRevision` | Supplier Dashboard - Video — Submit Revision (D3) |

### 辅助（6）

| 函数 | 验证页面 |
|------|---------|
| `NotificationHelper.error` | Supplier Landing, Requests, Connected, Buyer Register, Create Task |
| `NotificationHelper.success` | Supplier Landing, Buyer Register |
| `NotificationHelper.info` | Buyer Register |
| `RouteGuard.requireSupplier` | Supplier Dashboard - Requests, Connected |
| `RouteGuard.requireBuyer` | Buyer Portal - Dashboard, Create Task |
| `CONFIG.SUPPLIER_LOGIN_PAGE / BUYER_LOGIN_PAGE` | Supplier Landing, Buyer Register |

⚠️ **已知未真接 API**（后续处理）：
- Supplier Dashboard - Connected：connected buyers 列表 / View Profile / Chat 都是 bundle 占位（K2，D5-D7）
- Home Dashboard 顶部 3 个数据卡片（New Buyer Requests / Connected Buyers / Credits Balance）：可能仍是 bundle 占位（D2 验证）

---

## 未验证清单（待 14 天周期补齐）

### AuthAPI（剩 4）

- `logout`
- `updateMe`
- `getCurrentUser`
- `isLoggedIn`

### SupplierAPI（剩 15）

- `getProfile`, `createProfile`, `updateProfile`
- `addFactory`, `updateFactory`, `deleteFactory`
- `addMOQ`, `updateMOQ`, `deleteMOQ`
- `addCertification`, `deleteCertification`
- `addStrength`, `deleteStrength`
- `addMarket`, `deleteMarket`

### BuyerAPI（11，全部未验证）

- `getProfile`, `createProfile`, `updateProfile`
- `addMOQ`, `updateMOQ`, `deleteMOQ`
- `addMarket`, `deleteMarket`
- `submitRequest`, `getMyRequests`, `getConnectedSuppliers`

### VideoAPI（剩 1 — getVideo 单条查询，可选）

- `getVideo`（当前 Video.html 直接用 getMyVideos 列表里的第一条；如未来需要按 ID 看详情时再启用）

### LeadsAPI（剩 5）

- `getLead`, `updateLead`, `cancelLead`
- `getLeadApplications`, `connectWithSupplier`

### CreditsAPI（剩 1）

- `getMyPayments`（D2 时若需要单独看支付记录会接）

### MessagesAPI（剩 3 — D5-D7 验证）

- `getMessages`
- `sendMessage`
- `markAsRead`

### AdminAPI（13，全部未验证 — D14 验证）

- `listUsers`, `updateUserStatus`
- `listSuppliers`, `verifySupplier`
- `listBuyers`, `verifyBuyer`
- `listBuyerRequests`, `updateBuyerRequestStatus`
- `listVideos`, `updateVideo`
- `adjustCredits`, `addNote`, `getNotes`

### TokenManager（剩 7 — 通常不直接调用，验证算可选）

- `getSupabaseSession`, `setSupabaseSession`, `clearSupabaseSession`
- `getAccessToken`
- `getUser`, `setUser`, `clearUser`, `clearAll`

### RouteGuard（剩 3）

- `requireAuth`
- `requireAdmin`
- `requireGuest`

### FormHelper（3，全部未验证）

- `showError`, `clearError`, `setLoading`

### NotificationHelper（剩 1）

- `show`（底层，通常通过 success/error/info 间接调用）

---

## 验证标准

某个函数算"已验证"必须满足：

1. 在某个 HTML 页面里实际调用过
2. 该页面已通过浏览器 F12 测试，**Network 标签**看到该 API 返回 200 / 正确数据
3. 函数返回值被前端 JS 正确消费（不是 swallow 错误后忽略）

仅 grep 到调用代码不算——必须看到实际跑通。

---

## 统计

| 命名空间 | 总数 | 已验证 | 未验证 | 进度 |
|---------|------|-------|-------|------|
| AuthAPI | 6 | 2 | 4 | 33% |
| SupplierAPI | 17 | 2 | 15 | 12% |
| BuyerAPI | 11 | 0 | 11 | 0% |
| VideoAPI | 5 | 4 | 1 | 80% |
| LeadsAPI | 10 | 5 | 5 | 50% |
| CreditsAPI | 5 | 4 | 1 | 80% |
| MessagesAPI | 4 | 1 | 3 | 25% |
| AdminAPI | 13 | 0 | 13 | 0% |
| TokenManager | 8 | 0 | 8 | 0% |
| RouteGuard | 5 | 2 | 3 | 40% |
| FormHelper | 3 | 0 | 3 | 0% |
| NotificationHelper | 4 | 3 | 1 | 75% |
| **总计** | **91** | **23** | **68** | **25%** |
