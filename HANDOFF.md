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

## 工作规则（11 条，违反过多次的坑）

完整规则见 `C:\Users\chean\.claude\projects\c--Projects-sourcingelf\memory\feedback_key_rules.md`。

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

---

## 已浏览器验证可用（7 个流程）

| # | 页面 | 验证状态 | 备注 |
|---|------|---------|------|
| 1 | Supplier Landing（登录） | ✅ | 注册 + 登录 |
| 2 | Supplier Dashboard - Home | ✅ | 数据卡片 + Apply 流程；`creditBalance` **还硬编码为 2**，未真接 `getMyCredits` |
| 3 | Supplier Dashboard - Requests | ✅ | View Profile + 遮码 + Connect Now |
| 4 | Supplier Dashboard - Connected | ✅ | |
| 5 | Buyer Portal - Register Login | ✅ | |
| 6 | Buyer Portal - Dashboard | ✅ | |
| 7 | Buyer Portal - Create Task | ✅ | |

---

## 今天部署但未验证（Day 0 必测）

| Commit | 内容 | 状态 |
|--------|------|------|
| `b6c6f37` | Home `buildLeadCard` 字段映射重写 | ⚠️ 待验证 |
| `a5feca5` | `main.py` 22 个显式路由 | ⚠️ 待验证 |
| `313eded` | 7 个无扩展名 alias | ⚠️ 待验证 |

**用户在生产无痕窗口测 3 件事**：

1. Home Buying Leads 卡片是否从 API 渲染真实数据
2. 点 Apply 按钮全流程是否走通
3. 点侧栏 Credits、Connected、Requests 是否正常跳转

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
