with open('routers/credits.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 替换乱码钻石符号为普通问号或直接删掉
content = content.replace('\ufffd', '')  # replace错误字符
content = content.replace('◆', '')       # 如果是这个符号

with open('routers/credits.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. Line 105:")
lines = content.split('\n')
print(lines[104])