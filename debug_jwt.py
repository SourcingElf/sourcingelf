import base64
import sys
sys.path.insert(0, '.')
from config import settings
from jose import jwt, JWTError

TOKEN = "eyJhbGciOiJFUzI1NiIsImtpZCI6ImIyNDUyZDVkLThhZmItNDA0Mi1hNTcxLTExNTE2ZjQ0NjE0MyIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2d4dXF5a2Fvd3FxY3p6YW5weHBiLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI0ZjUzNTg3Yi0zNDA2LTQ4MTktYTE2YS1iMTQ0N2FkM2QxYTkiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzc3NzA0OTU5LCJpYXQiOjE3Nzc3MDEzNTksImVtYWlsIjoidGVzdC5zdXBwbGllckBzb3VyY2luZ2VsZi5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsX3ZlcmlmaWVkIjp0cnVlfSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTc3NzcwMTM1OX1dLCJzZXNzaW9uX2lkIjoiYzg5MzhlNDAtMDI1OS00MmE4LWJlZWMtNTgzMDgxMDJhZjZiIiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.BnWWsl5KEEgTbaEQYdSCgFSzJV2A0Xd3azHU5wYm6lMNPWdHEBq7G5ltszdjbmExkH7qQacqYIqXCM5lZL7v0g"

print("=== Step 1: base64 decode ===")
raw = settings.supabase_jwt_secret
print("原始 secret 长度:", len(raw))
print("前20字符:", raw[:20])

try:
    decoded = base64.b64decode(raw)
    print("decode 成功，字节数:", len(decoded))
except Exception as e:
    print("decode 失败:", e)
    padding = 4 - len(raw) % 4
    if padding != 4:
        decoded = base64.b64decode(raw + '=' * padding)
        print("补 padding 后成功，字节数:", len(decoded))

print("\n=== Step 2: jose decode (with b64decode) ===")
try:
    payload = jwt.decode(TOKEN, decoded, algorithms=["HS256"], options={"verify_aud": False})
    print("成功！sub =", payload.get("sub"))
    print("完整 payload:", payload)
except JWTError as e:
    print("JWTError:", e)
except Exception as e:
    print("其他错误:", e)

print("\n=== Step 3: jose decode (raw string, no decode) ===")
try:
    payload2 = jwt.decode(TOKEN, raw, algorithms=["HS256"], options={"verify_aud": False})
    print("成功！sub =", payload2.get("sub"))
    print("完整 payload:", payload2)
except JWTError as e:
    print("JWTError:", e)
except Exception as e:
    print("其他错误:", e)