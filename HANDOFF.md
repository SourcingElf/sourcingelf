# SourcingElf 交接文档

**最后更新：2026-05-08（Day 0 基建完成）**
**当前阶段：Direct HTML 14 天周期，Day 0 已完成**

---

## 项目背景

SourcingElf 是 B2B SaaS 平台，连接亚洲服装供应商和欧美买家。

- **后端**：FastAPI + Supabase + Stripe，部署在 Railway
- **前端**：22 个 HTML 文件（手写 Direct HTML）
- **生产 URL**：https://web-production-1875f.up.railway.app
- **GitHub repo**：SourcingElf/sourcingelf
- **角色**：用户是非技术创办人，Claude Code 担任 CTO 角色

---

## 启动步骤（每次开发前）

```
窗口1：cd C:\Projects\sourcingelf  → uvicorn main:app --reload
窗口2：cd C:\Projects\sourcingelf  → python -m http.server 3000 --directory frontend
浏览器：http://localhost:3000/Supplier%20Dashboard%20-%20Home.html
F12 Console 必须无红错才算可以开始
```

**测试账号**：

| 邮箱 | 密码 | 角色 |
|------|------|------|
| test.supplier@sourcingelf.com | Test1234! | supplier |
| test.buyer@sourcingelf.com | Test1234! | buyer |

---

## 技术方案：Direct HTML（已确定，不再讨论）

**决策依据**：

- Direct HTML 把握 75%，Next.js 把握仅 55%
- `Supplier Dashboard - Home.html`（49KB）已验证此模式可行
- 后端 70 个 API 路由完整不动
- `client.js`（547 行）drop-in 复用，全局暴露 `window.SourcingElf`

**架构**：

| 层 | 实现 |
|---|---|
| 前端 | 22 个手写 HTML，每个 `<head>` 引 `<script src="api/client.js">` |
| 静态服务 | FastAPI `main.py:42` 把 `frontend/` 挂载到 `/` |
| API | 所有路由都在 `/api/v1/*` 下，前端调用同源 |
| Auth | Supabase JWT（ES256，`verify_signature=False`），存 `localStorage.sb_session` |

---

## 已确定决策（不再讨论）

| 决策 | 选择 | 理由 |
|------|------|------|
| Q1: Day 0 基建 | 先做不跳过 | 减少重复踩坑 |
| Q2: Stripe webhook | 沙盒账号，webhook 暂跳过 | 等部署稳定后再配 |
| Q3: viewLead 详情 | 弹窗模态 | 不做独立详情页 |

---

## 工作规则（12 条，违反过多次的坑）

完整规则见 `C:\Users\chean\.claude\projects\c--Projects-sourcingelf\memory\feedback_key_rules.md` 和 `feedback_file_management.md`。

简版速查：

1. **onclick 引号嵌套** — 双引号外，里用 `&quot;` 不用单引号
2. **修代码前用 Python `repr()`** 确认真实字符（PowerShell 显示会乱码）
3. **收工前必须浏览器 F12 验证无红错**
4. **买家端 HTML 是打包格式** — 用 F12 看真实 DOM
5. **不要猜，先确认**（标识符/路径/CSS class）
6. **Python 写文件，绝不用 PowerShell** 粘贴代码
7. **全程中文沟通**
8. **重启服务前先 `ls` 确认文件存在**
9. **操作 DOM 前先解码 bundler template** 确认真实 element ID
10. **修死链/路由前必须先全局 grep** 摊清楚同类项
11. **CTO 模式工作** — 不给 A/B/C 菜单，给有信心的明确推荐
12. **每轮收工前同步 HANDOFF.md / client_js_verified.md / scripts/**，commit 写"为什么改"

---

## 已浏览器验证可用（9 个流程）

| # | 页面 | 验证状态 | 备注 |
|---|------|---------|------|
| 1 | Supplier Landing（登录） | ✅ | 注册 + 登录 |
| 2 | Supplier Dashboard - Home | ✅ | Buying Leads 接真实 API；Apply 流程含余额预检查；公司名**后端**打码（K4 done） |
| 3 | Supplier Dashboard - Requests | ✅ | 接真实 API；loading 占位防闪现；View Profile + Connect Now 流程 |
| 4 | Supplier Dashboard - Connected | ✅ (bundle 占位) | 页面能进，View Profile / Chat 按钮待 D 阶段接 API（K2） |
| 5 | Supplier Dashboard - Credits | ✅ D1 完成 | 真实余额 + 交易历史；Top Up 跳 Stripe Checkout（沙盒）；K3 done |
| 6 | Buyer Portal - Register Login | ✅ | |
| 7 | Buyer Portal - Dashboard | ✅ | |
| 8 | Buyer Portal - Create Task | ✅ | |
| 9 | 侧栏跳转（无扩展名 alias） | ✅ | /credits /connected /requests /dashboard 等全部 ok |

---

## D0 验证已完成（2026-05-09）

D0 浏览器验证轮跑完，下面 5 件事全部通过 ✓：

| # | 验证 | 状态 | 修复来源 commit |
|---|------|------|----------------|
| 1 | Home Buying Leads 卡片从 API 渲染真实数据 | ✅ | `c128f69` (字段映射 + buyer_type pill + 公司打码) |
| 2 | Apply 流程：余额足够正常扣 1 credit；余额不足按钮灰色禁用 | ✅ | `c128f69` (applyLead 预检查) + `762f9f6` (apiFetch 422 detail 解析) |
| 3 | Credits 侧栏跳转 → 页面正常 | ✅ | `e9beff3` (从 backup 恢复) |
| 4 | Connected 侧栏跳转 → 页面正常 | ✅ | `e9beff3` (从 backup 恢复) |
| 5 | Requests 占位卡片不再"几张 → 1 张"闪现 | ✅ | `fd38028` (loading 占位) |

D0 阻塞问题全部清除，**可以进 D1**。

---

## Known Backlog（待客户测试细化，D2+ 处理）

| # | 项 | 触发条件 | 计划处理时机 |
|---|----|---------|----|
| K1 | Buying Lead ID 改 `BL-YYYY-NNN` 格式（如 #BL-2026-047） | 设计稿要求；当前是 `BL-XXXXXXXX` 8 位 hex | 需要 `buying_leads` 表加 `sequence_number` 列 + DB migration，D2 单独议 |
| K2 | Supplier Connected 页面的 View Profile / Chat 按钮接 API | 当前是 bundle 占位，按钮无响应 | D5-D7 (IM Chat 重写时一起做 Chat 按钮) + D 阶段 (View Profile) |
| ~~K3~~ | ~~Credits 页面接真实 API~~ | **D1 已完成** (commits `5d1234`-`9d8765`) | ✅ |
| ~~K4~~ | ~~公司名打码移到后端~~ | **D1 已完成** (`_mask_company` in `routers/leads.py`) | ✅ |
| K5 | 17 个 mojibake 损坏的 HTML 文件批量恢复 | PowerShell 误读 UTF-8 留下的字符级损坏 | 等到对应 D 阶段重写整页时一起处理（不再批量） |
| K6 | Stripe webhook 接入（支付完自动同步余额） | Q2 决策暂跳过，D1 用前端 success 页面跳回 + 自动 refresh 替代 | D 阶段稳定后单独议 |
| K7 | Top Up modal 内 mock 卡片输入框 | 视觉装饰，实际跳 Stripe Hosted Checkout 填卡 | 客户测试后看是否需要去除装饰避免误导 |

---

## 待完成 15 个页面（按优先级）

| 阶段 | 页面 | 备注 |
|------|------|------|
| D1-D2 | Supplier Credits 全链路 | Stripe 沙盒 + 余额展示 + 历史 |
| D3-D4 | Supplier Video + Video Submit | |
| D5-D7 | IM Chat 完整重写 | v1 用 3 秒轮询，不上 WebSocket |
| D8-D9 | Buyer Tasks + Applications | |
| D10-D11 | Buyer Hub + Featured Suppliers + Lead Form | |
| D12-D13 | Buyer Profile + Connected + Requests + Landing | |
| D14 | Admin + Homepage + 整站回归 | |

---

## 关键参考路径

| 资源 | 路径 |
|------|------|
| 后端项目根 | `C:\Projects\sourcingelf` |
| 前端 HTML | `C:\Projects\sourcingelf\frontend\*.html` |
| client.js | `C:\Projects\sourcingelf\frontend\api\client.js` |
| API routers | `C:\Projects\sourcingelf\routers\*.py` |
| Models (pydantic) | `C:\Projects\sourcingelf\models\*.py` |
| backup 干净 HTML | `C:\Projects\Claude Design Backup\standalone\` |
| 一次性脚本归档 | `C:\Projects\sourcingelf\scripts\` |
| client.js 验证清单 | `C:\Projects\sourcingelf\client_js_verified.md` |
| 项目说明 | `C:\Projects\sourcingelf\CLAUDE.md` |

---

## Day 0 已完成清单（2026-05-08）

- [x] `.vscode/settings.json`：UTF-8 + LF + 去尾随空格
- [x] `.gitattributes`：所有源码 LF + UTF-8 强制
- [x] `scripts/` 目录建立 + 5 个一次性脚本归档（带 README）
- [x] `HANDOFF.md` 重写（本文件）
- [x] `client_js_verified.md` 创建（已验证 11 个函数 + 未验证清单）
- [x] 全部用 Python 写文件，UTF-8 验证通过

---

## 用户须知（每次新对话开始时）

1. 读 `CLAUDE.md`
2. 读 `memory/feedback_key_rules.md`（11 条规则）
3. 读本文件最新状态
4. 回复"准备就绪，确认按 X 步执行"
5. 等用户说"开始"再动手
