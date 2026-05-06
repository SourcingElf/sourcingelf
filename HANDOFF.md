# SourcingElf 交接文档
**最后更新：2026-05-06**

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

### ⚠️ 已知问题（待处理）
- **Dashboard 分页**："Page 1 of 3" 是假数据
- **Supplier Buying Leads "Apply to this lead"**：占位弹窗，未接 API
- **Buyer 控台数据卡片宽度不等**（Bug 6b）
- **Buyer 导航缺少 Messages 入口**（Bug 6c）

### ⏳ 下一步（按优先级）
1. **验证 Buyer Applications 页面** — 打开页面确认 Console 无报错，测试 Connect 流程
2. IM Chat 页面（需重写，不依赖原始备份）
3. Buying Leads Apply 接入真实 API（供应商端）
4. Dashboard 分页修复
5. 部署到 Railway

---

## 关键技术规则

### 修改 inject_all.py 前必须确认真实内容
用 repr() 看真实字符串，不靠 PowerShell 显示判断：
```
python -c "f=open('inject_all.py',encoding='utf-8').read(); i=f.find('目标字符串'); print(repr(f[i-20:i+100]))"
```

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

## 今天修改的文件（2026-05-06）

| 文件 | 改动 |
|------|------|
| inject_all.py | 买家登录：document capture 方案 |
| inject_all.py | Buyer Dashboard：接入 connections + active leads API |
| inject_all.py | Buyer Create Task：document capture 拦截 + createLead API |
| inject_all.py | Buyer Applications：加载申请 + Connect API（待验证） |
| routers/fix_buyer_uuid.py | 修正买家 UUID 不匹配（已执行，可删） |
