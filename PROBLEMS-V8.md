# SourcingElf 踩坑记录

## 1. JWT 验证 Bug（已修复）
- 问题：jwt.decode 验证失败
- 原因：Supabase 用 ES256 非对称算法，不是 HS256
- 解决：改用 PyJWT，verify_signature=False
- 位置：database.py

## 2. 注册流程设计
- 正确流程：前端调用 supabase.auth.signUp()，然后前端调用 POST /auth/register
- 不要用后端单独创建 Supabase Auth 账号

## 3. Cloudflare 封锁本地请求
- 本地 PowerShell 直接调用 supabase.co 的 Auth API 会被封锁

## 4. Windows 环境注意
- PowerShell 不支持 Linux 命令（如 head）

## 5. 前端技术栈
- 纯 HTML/CSS/JS，不是 Next.js

## 6. 前端已知问题（API对接时修复）
- 6a. Connect 确认弹窗缺失 ✅ 已修复
- 6b. 买家控台数据卡片宽度不等 ⏳ 待修复
- 6c. 买家端导航缺少 Messages 入口 ⏳ 待修复
- 6d. 供应商请求页 Connect Now 缺少确认 ✅ 已修复

## 7. PowerShell 写入 Python 文件编码问题
- 永远用 notepad 或 Python 脚本写文件

## 8. auth.py login 端点 settings 引用问题
- 用 from config import settings as _s，函数内用 _s

## 9. Supabase JWT 算法是 ES256（2026-05-02）
- token header 显示 alg: ES256
- 最终解决：PyJWT verify_signature=False

## 10. credits.py _ensure_credits_account bug（2026-05-02）
- 问题：if result.data: 报 AttributeError
- 解决：改为 if result and result.data:

## 11. PowerShell 修改文件的正确方式
- 简单替换：(Get-Content "file.py") -replace 'old', 'new' | Set-Content "file.py"
- 复杂修改：用 notepad 写 fix_xxx.py，然后 python fix_xxx.py
- 绝对不要在 PowerShell 里逐行粘贴 Python 代码

## 12. Supabase login 速度慢
- 从新加坡连接，每次 login 需要 30-60 秒
- 加 -TimeoutSec 60 参数，偶尔超时重试即可

## 13. client.js token key 名称（2026-05-02 修复）
- 问题：client.js 读取 'se_token'，但登录脚本存的是 'token'
- 解决：用 fix_keys.py 把 client.js 里所有 'se_token' 改成 'token'
- localStorage 里的 keys：token, sb_session, user_id, role, se_user

## 14. API_BASE_URL 不能加 /api/v1（2026-05-02 确认）
- client.js 里所有函数路径已经带完整 /api/v1/xxx
- API_BASE_URL 必须保持 http://localhost:8000，不要加 /api/v1
- 如果加了会变成双重 /api/v1/api/v1/xxx，所有 API 调用 404

## 15. 修改代码前必须查清楚（2026-05-02 教训）
- 修改前必须先用 PowerShell Select-String 查清楚相关代码
- 确认函数名、路径、CSS class 都正确才动手
- 不允许边猜边改，猜测性修改会造成难以追踪的问题

## 16. 供应商没有查看收到的买家请求的 API（2026-05-02 发现并修复）
- 原问题：GET /buyers/me/requests 是买家查看自己发出的请求，供应商用会 403
- 解决：已在 suppliers.py 新增 GET /suppliers/me/buyer-requests
- 同时在 client.js 新增 SE.SupplierAPI.getMyBuyerRequests(status) 函数

## 17. Python 脚本替换文字时，搜索字符串必须与文件内容完全一致（2026-05-02）
- 问题：用 content.replace(old, new) 时，old 字符串里的换行、空格必须与文件完全匹配
- 解决方法：先用 Get-Content | Select-Object -Index 查看确切内容，再写脚本
- 如果 ERROR，在脚本里加 print(repr(...)) 打印实际内容，对比差异
- 绝对不要猜测格式，必须先确认
