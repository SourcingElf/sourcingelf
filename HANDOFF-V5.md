# SourcingElf 交接文档
**最后更新：2026-05-02**

---

## 当前运行环境

| 服务 | 命令 | 地址 |
|------|------|------|
| 后端 API | `cd C:\Projects\sourcingelf` → `uvicorn main:app --reload` | http://localhost:8000 |
| 前端服务器 | `cd C:\Projects\sourcingelf-frontend` → `python -m http.server 3000` | http://localhost:3000 |
| Swagger UI | 后端启动后访问 | http://localhost:8000/docs |

---

## 测试账号

| Email | Password | Role |
|-------|----------|------|
| test.supplier@sourcingelf.com | Test1234! | supplier |

---

## 关键技术决定

### JWT 验证
- Supabase 用 ES256 非对称算法
- 解决方案：PyJWT，options={"verify_signature": False}
- 文件：database.py

### 前端架构
- 22个 HTML 文件，用 Claude Design 生成
- 文件格式：React JSX + Babel（在浏览器实时编译）
- 对接方式：在每个 HTML 文件 </body> 前注入 `<script>` 块调用 API
- 注入脚本保存在：C:\Projects\sourcingelf-frontend\fix_*.py

### 文件修改规则
- 永远用 notepad 写 Python 脚本，不要在 PowerShell 直接粘贴代码
- 修改 HTML 用 Python 脚本替换字符串

---

## 后端端点测试结果（2026-05-02）

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

**Supplier Landing.html — 登录功能**
- 修改脚本：fix_login.py
- 功能：点击 Log In → 调用 POST /auth/login → 存 token/role/user_id 到 localStorage → 跳转 Supplier Dashboard - Home.html
- token 存储：localStorage.getItem('token')

**Supplier Dashboard - Home.html — Credits 数据**
- 修改脚本：fix_dashboard_home.py
- 功能：页面加载时检查 token（无则跳回登录）→ 调用 GET /credits/me → 更新 Credits 数字
- Credits 元素：document.querySelectorAll('.metric-number.navy')[1]
- Buying Leads 暂时保留 mock 数据（数据库还没有真实 leads）

### ⏳ 待完成（按优先级）

1. **Supplier Dashboard - Home.html**
   - New Buyer Requests 数字对接真实 API
   - Connected Buyers 数字对接真实 API
   - 用户名显示对接 GET /auth/me

2. **Supplier Dashboard - Credits.html**
   - 余额显示
   - 交易记录列表
   - Stripe 充值按钮

3. **Supplier Dashboard - Requests.html**
   - 买家请求列表

4. **Supplier Dashboard - Connected.html**
   - 已连接买家列表

5. **Supplier Dashboard - Video.html / Video Submit.html**
   - 视频状态显示
   - 提交视频材料

6. **IM Chat.html**
   - 消息列表
   - 发送消息

7. **买家端页面**（需要新建买家测试账号）
   - Buyer Portal - Register Login.html
   - Buyer Portal - Dashboard.html
   - 其余买家页面

8. **Admin Backend.html**
   - 需要 admin 测试账号

---

## 已知 Bug 待修复

| # | 问题 | 文件 | 状态 |
|---|------|------|------|
| 6a | Connect 确认弹窗缺失 | Supplier Dashboard - Requests.html | 待修复 |
| 6b | 买家控台数据卡片宽度不等 | Buyer Portal - Dashboard.html | 待修复 |
| 6c | 买家端导航缺少 Messages 入口 | 所有 Buyer Portal 页面 | 待修复 |
| 6d | 供应商请求页 Connect Now 缺少确认 | Supplier Dashboard - Requests.html | 待修复 |

---

## 备份位置

| 备份 | 内容 |
|------|------|
| C:\Projects\sourcingelf_backup_20260502 | 初始备份 |
| C:\Projects\sourcingelf_backup_login_working | auth/login 测试通过后 |
| C:\Projects\sourcingelf_backup_jwt_fixed | JWT 修复后 |
| C:\Projects\sourcingelf_backup_20260502_final | 当天最终版本 |

---

## 下一个 Session 开始步骤

1. 启动后端：`cd C:\Projects\sourcingelf` → `uvicorn main:app --reload`
2. 启动前端：`cd C:\Projects\sourcingelf-frontend` → `python -m http.server 3000`
3. 浏览器打开：http://localhost:3000/Supplier%20Landing.html
4. 登录测试账号验证一切正常
5. 继续对接 Supplier Dashboard - Home.html 的剩余数据
