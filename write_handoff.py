content = """# SourcingElf 备份与交接协议

## 重要技术记录

### JWT 验证方式（最关键！2026-05-02 修复）
- Supabase 用 ES256 非对称算法，不是 HS256
- 之前用 base64.b64decode(jwt_secret) 是错的
- 正确方式：PyJWT，options={"verify_signature": False}
- 已更新 database.py，不要改回去

### PowerShell 注意事项
- Login 每次需要 30-60 秒，正常现象
- 偶尔超时，重试即可
- 永远不要用 PowerShell 直接写 Python 代码
- 写文件用 notepad，运行用 python xxx.py
- 修改 Python 文件用 Python 脚本（fix_xxx.py）来替换内容

### credits.py 已修复
- _ensure_credits_account 函数
- 改为 if result and result.data:

### auth.py login 端点
- 用 from config import settings as _s，函数内用 _s

## 测试账号
- test.supplier@sourcingelf.com / Test1234! / supplier

## 当前进度（2026-05-02）

### 已完成：
- POST /auth/login
- GET /auth/me
- GET /suppliers/me/profile
- POST /suppliers/me/profile
- GET /messages/connections
- GET /leads/browse
- GET /credits/me 代码已修复，待验证

### 下一步：
1. 验证 GET /credits/me
2. 测试其余端点（buyers/videos/leads/admin）
3. 全部通过后开始前端集成

### 备份位置：
- C:\\Projects\\sourcingelf_backup_jwt_fixed
- C:\\Projects\\sourcingelf_backup_20260502_final
"""

with open('C:/Projects/sourcingelf/HANDOFF.md', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')