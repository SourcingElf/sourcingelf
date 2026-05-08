"""Scan extensionless internal URLs in the Claude Design backup files."""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

BACKUP = r"C:\Projects\Claude Design Backup\standalone"

patterns = [
    re.compile(r"""href\s*=\s*\\?["']([^"'\\]+?)\\?["']""", re.IGNORECASE),
    re.compile(r"""window\.location(?:\.href)?\s*=\s*\\?["']([^"'\\]+?)\\?["']""", re.IGNORECASE),
    re.compile(r"""window\.open\s*\(\s*\\?["']([^"'\\]+?)\\?["']""", re.IGNORECASE),
]


def is_extless(u: str) -> bool:
    if not u.startswith("/"):
        return False
    if u.startswith("//") or u.startswith("/api/"):
        return False
    last = u.split("?")[0].split("#")[0].rstrip("/").rsplit("/", 1)[-1]
    return bool(last) and "." not in last


ext = {}
all_internal = {}
for f in sorted(os.listdir(BACKUP)):
    if not f.endswith(".html"):
        continue
    text = open(os.path.join(BACKUP, f), encoding="utf-8").read()
    for pat in patterns:
        for m in pat.finditer(text):
            u = m.group(1).strip()
            if u.startswith(("http://", "https://", "//", "mailto:", "tel:", "javascript:", "#", "data:", "blob:")):
                continue
            all_internal.setdefault(u, set()).add(f)
            if is_extless(u):
                ext.setdefault(u, []).append(f)

print(f"=== EXTENSIONLESS internal URLs in BACKUP files ===")
print(f"unique: {len(ext)}, total occurrences: {sum(len(v) for v in ext.values())}")
for u in sorted(ext):
    files = sorted(set(ext[u]))
    print(f"  {u!r}  ({len(ext[u])} times across {len(files)} file(s))")
    for fn in files:
        print(f"      - {fn}")

print(f"\n=== ALL non-external URLs in backup (top 30 by file count) ===")
top = sorted(all_internal.items(), key=lambda x: -len(x[1]))[:30]
for u, files in top:
    print(f"  {u!r:<55} {len(files):>3} file(s)")
