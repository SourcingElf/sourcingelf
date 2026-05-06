# SourcingElf 交接文档
**最后更新：2026-05-04**

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

## 最容易犯的错误（今天犯了两次，必须牢记）

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

**这个错误今天发生了两次：**
- 第一次：Connected 页面的 Open Chat 按钮（上次对话写错，今天才发现）
- 第二次：Buying Leads 的 Apply 链接（今天写新代码时又犯）

**每次写任何包含 onclick 的代码，写完必须立即检查引号，再给出文件。**

---

## 测试账号

| Email | Password | Role |
|-------|----------|------|
| test.supplier@sourcingelf.com | Test1234! | supplier |
| test.buyer@sourcingelf.com | 未设密码，仅数据库记录 | buyer |

---

## 测试数据（Supabase 已插入）

| 表 | ID | 内容 |
|---|------|------|
| users（买家） | bae1599d-b815-4473-a248-52c76609a04d | test.buyer@sourcingelf.com |
| buyer_profiles | 8ea03203-0c55-44b6-acac-6f7085106aac | Test Buyer Co / US / Brand |
| buying_leads | 30837a3c-8b92-40bd-a817-b3334d06c599 | Women's Knitwear lead |
| buyer_requests | （Sarah Johnson） | Anthropologie Group / US / Brand |
| supplier_profiles | f37d3e21-3ed8-4eed-a9b9-017746239e75 | 供应商测试账号 |

---

## 前端对接进度（2026-05-04）

### ✅ 已完成并在浏览器验证通过
- 22/22 页面注入 client.js
- 登录流程
- Dashboard — 三个数据卡片（真实数据）
- Dashboard — Buying Leads（真实 API，卡片正常渲染，有测试数据验证过）
- Supplier Requests — View Profile 弹窗 + 买家信息遮码 + Connect Now
- Supplier Connected — 无 JS 错误，API 正常调用，显示"0 connections"（正确）

### ⚠️ 已做但有已知问题，下次必须处理
- **Dashboard 分页**："Page 1 of 3" 是原始备份里的假数据，未换成真实数量
- **Apply to this lead**：点击只弹出占位提示，未接入真实 API（POST /leads/{id}/apply）
- **Supplier Connected 卡片**：渲染逻辑已写好，但没有真实 connection 记录验证过卡片样式

### ⏳ 下一步（按优先级）
1. IM Chat 页面接入真实 API
2. 买家端（注册登录、Dashboard、发布任务、查看申请、确认连接）
3. Buying Leads Apply 功能接入真实 API
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

## 今天修改的文件

| 文件 | 改动 |
|------|------|
| inject_all.py | 修复 Connected 页面 onclick 引号错误 |
| inject_all.py | Dashboard Buying Leads 接入真实 API |

