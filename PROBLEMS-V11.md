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

## 6. 前端已知问题
- 6a. Buyer Applications Connect 确认弹窗 ✅ 已修复
- 6b. 买家控台数据卡片宽度不等 ⏳ 待修复
- 6c. 买家端导航缺少 Messages 入口 ⏳ 待修复
- 6d. 供应商 Requests Connect Now — ✅ 已被新的 View Profile 设计完全取代
- 6e. Dashboard Buying Leads 分页显示硬编码"Page 1 of 3" ⏳ 待修复
- 6f. Dashboard Buying Leads "Apply to this lead" 只是占位弹窗 ⏳ 待接入真实 API

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
- 解决方法：先用 debug 脚本打印 repr() 看真实内容，再写替换脚本
- 如果 ERROR，在脚本里加 print(repr(...)) 打印实际内容，对比差异
- 绝对不要猜测格式，必须先确认

## 18. inject_all.py 文件编码问题（2026-05-03）
- 问题：inject_all.py 里的中文注释和特殊字符（─）在 PowerShell 显示乱码
- 原因：文件编码与 PowerShell 显示编码不一致
- 影响：用字符串匹配替换会 ERROR（找不到目标字符串）
- 解决：用 Python 脚本读文件、print(repr(...)) 看真实内容，再用真实字符串做匹配
- 教训：永远不要靠 PowerShell 显示的内容来判断文件里的实际字符

## 19. Requests 页面重大设计升级（2026-05-03）
- 原设计：卡片直接有 Connect Now，信息太少，供应商无法充分判断买家
- 新设计：View Profile 弹窗 → 看完买家完整背景（遮码）→ 再决定 Connect
- 遮码规则：公司名首字母+**+最后一字，姓名/联系方式完全隐藏
- Connect Now 移入弹窗，credits=0时禁用并提示 Top up
- 详细业务逻辑见 HANDOFF.md「重要业务决定记录」章节

## 20. Connected 页面架构问题（2026-05-03 晚）
- 问题：GET /messages/connections 只返回 connection 的 uuid，没有买家显示信息
- 错误做法：改现有端点（会影响买家端）；前端多次调用（性能差）
- 正确做法：新增专用端点 GET /suppliers/me/connected-buyers，join buyer_profiles 返回
- 教训：改现有端点前必须想清楚所有使用这个端点的地方，避免影响其他功能

## 21. inject_all.py 替换脚本必须用 repr() 确认结束标记（2026-05-03 晚）
- 问题：用 PowerShell 看到的结束标记格式，和文件实际内容不一致
- 原因：PowerShell 显示有乱码，无法准确判断换行符和特殊字符
- 正确做法：先写 debug 脚本用 print(repr(content[idx:idx+600])) 打印真实内容
- 然后根据 repr() 输出的确切字符串写替换脚本，一次成功
- 教训：永远先 debug 再动手，不要猜

## 22. onclick 引号嵌套错误（2026-05-04，发生两次）
- 问题：HTML onclick 属性用双引号，里面的字符串不能用单引号，否则产生 SyntaxError
- 第一次：Connected 页面 Open Chat 按钮，onclick="...href='IM Chat.html'"
- 第二次：Buying Leads Apply 链接，onclick="alert('Apply feature coming soon')"
- 两次都产生：Uncaught SyntaxError: Unexpected identifier
- 正确写法：onclick="window.location.href=&quot;IM Chat.html&quot;"
- 正确写法：onclick="alert(&quot;Apply feature coming soon&quot;)"
- 规则：写任何 onclick 代码，写完必须先检查引号嵌套，再输出

## 23. 收工前必须在浏览器验证（2026-05-04 教训）
- 问题：上次对话写完代码没有打开浏览器验证，带着 JS 错误收工
- 今天花了大量时间才找到并修复这个本来一眼就能发现的错误
- 规则：每次改完代码，必须打开浏览器，看页面 + 看 Console，确认无红色报错才收工
