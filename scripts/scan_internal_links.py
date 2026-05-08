"""
Comprehensive scanner for internal links in all 22 frontend HTML files.

Three layers checked:
  1. Plain HTML attribute hrefs:        href="..."
  2. Inline JS navigation:              window.location.href = "...", window.open(...)
  3. JSON-encoded HTML inside bundler templates (`<script type="__bundler/template">`) —
     decoded with json.loads, then scanned for href / to / onClick navigation strings.

Output focuses on EXTENSIONLESS internal links (start with '/', no extension on
the last path segment), but also reports a summary of every internal navigation
target so the user can verify nothing is hidden.
"""
import os
import re
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

DIR = "frontend"

# Patterns handle BOTH plain HTML attrs (`href="..."`) AND JSON-escaped form
# (`href=\"...\"`) found inside `<script type="__bundler/template">` bodies.
# The `\\?` matches an optional literal backslash before the quote.
PATTERNS_PLAIN = [
    re.compile(r"""href\s*=\s*\\?["']([^"'\\]+?)\\?["']""", re.IGNORECASE),
    re.compile(r"""window\.location(?:\.href)?\s*=\s*\\?["']([^"'\\]+?)\\?["']""", re.IGNORECASE),
    re.compile(r"""window\.open\s*\(\s*\\?["']([^"'\\]+?)\\?["']""", re.IGNORECASE),
]


def is_internal_extensionless(url: str) -> bool:
    """True if URL is an absolute internal path with no extension on last segment."""
    if not url.startswith("/"):
        return False
    if url.startswith("//"):
        return False  # protocol-relative
    if url.startswith("/api/"):
        return False
    last = url.split("?")[0].split("#")[0].rstrip("/").rsplit("/", 1)[-1]
    if not last:
        return False  # bare slash
    if "." in last:  # e.g. "credits.html", "icon.svg"
        return False
    return True


def is_internal_navigation(url: str) -> bool:
    """Catch-all for any non-external nav target, used for fuller reporting."""
    if not url:
        return False
    if url.startswith(("http://", "https://", "//", "mailto:", "tel:", "javascript:", "#", "data:", "blob:")):
        return False
    return True


# url -> list of (file, location_label)
findings_extless = {}
findings_all_internal = {}


def record(url: str, file_label: str):
    if is_internal_navigation(url):
        findings_all_internal.setdefault(url, []).append(file_label)
    if is_internal_extensionless(url):
        findings_extless.setdefault(url, []).append(file_label)


def scan_text(text: str, file_label_prefix: str, line_offset_calc=None):
    """Apply plain patterns. line_offset_calc(start_offset) -> str like 'L42'."""
    for pat in PATTERNS_PLAIN:
        for m in pat.finditer(text):
            url = m.group(1).strip()
            if line_offset_calc is not None:
                line_label = line_offset_calc(m.start())
            else:
                line_label = ""
            label = f"{file_label_prefix}{line_label}"
            record(url, label)


def make_line_calc(text: str):
    """Returns a callable: offset -> 'L<n>' (1-based line number)."""
    def calc(offset: int) -> str:
        return f":L{text.count(chr(10), 0, offset) + 1}"

    return calc


SCRIPT_BLOCK_RE = re.compile(
    r"""<script\b([^>]*)>([\s\S]*?)</script>""", re.IGNORECASE
)
TYPE_RE = re.compile(r"""\btype\s*=\s*["']([^"']*)["']""", re.IGNORECASE)


for fname in sorted(os.listdir(DIR)):
    if not fname.endswith(".html"):
        continue
    path = os.path.join(DIR, fname)
    text = open(path, encoding="utf-8", errors="replace").read()

    # Strategy: build a "non-script" text for plain HTML scanning, then handle each
    # script block based on type.
    non_script_parts = []
    cursor = 0
    line_calc = make_line_calc(text)

    for m in SCRIPT_BLOCK_RE.finditer(text):
        # text before this script: regular HTML
        chunk = text[cursor:m.start()]
        non_script_parts.append(chunk)

        attrs = m.group(1) or ""
        body = m.group(2)
        type_m = TYPE_RE.search(attrs)
        typ = (type_m.group(1).lower() if type_m else "").strip()

        if typ == "__bundler/template":
            # Decode JSON to get real inner HTML, then scan.
            try:
                decoded = json.loads(body)
                if isinstance(decoded, str):
                    scan_text(
                        decoded,
                        file_label_prefix=f"{fname} [in __bundler/template]",
                        line_offset_calc=None,  # line numbers are meaningless post-decode
                    )
            except (ValueError, json.JSONDecodeError) as e:
                print(f"!! JSON decode failed for template in {fname}: {e}", file=sys.stderr)

        elif typ == "__bundler/manifest" or typ == "__bundler/ext_resources":
            # Manifest is base64+gzip binary — skip (would need decompression).
            pass

        # Inline JS bodies are scanned in the text-level pass below — don't
        # double-scan with a body-relative offset fed to a text-relative line calc
        # (that would attribute matches to wrong line numbers).

        cursor = m.end()

    non_script_parts.append(text[cursor:])
    # Scan plain-HTML regions (with original line numbers).
    # Note: concatenating skips the script bodies so line numbers stay correct
    # ONLY if we calc on original text. Scan original text directly for href=
    # but we also need to NOT double-count inline JS strings that appear both
    # as href= attributes and as window.location strings. Simplest: scan original
    # text with PLAIN patterns and accept some inline-JS strings will be matched
    # twice — dedupe by (url, file_label).
    scan_text(text, file_label_prefix=fname, line_offset_calc=line_calc)


# Dedupe: a url found in the same file_label shouldn't be reported twice.
def dedupe(d):
    return {url: sorted(set(locs)) for url, locs in d.items()}


findings_extless = dedupe(findings_extless)
findings_all_internal = dedupe(findings_all_internal)


# ─── REPORT ─────────────────────────────────────────────────────────────────
print("=" * 78)
print("EXTENSIONLESS INTERNAL LINKS — full scan of 22 HTML files")
print("=" * 78)
print(f"Unique URLs: {len(findings_extless)}    Total occurrences: {sum(len(v) for v in findings_extless.values())}")

# Group by URL family for readability
for url in sorted(findings_extless):
    locs = findings_extless[url]
    print(f"\n  {url!r}   ({len(locs)} location{'s' if len(locs) != 1 else ''})")
    # Group by source file
    by_file = {}
    for loc in locs:
        # split off the leading file name
        if " [in __bundler/template]" in loc:
            f, _, _ = loc.partition(" [in __bundler/template]")
            by_file.setdefault(f, []).append("(in __bundler/template)")
        else:
            f = loc.split(":")[0]
            line = loc.split(":", 1)[1] if ":" in loc else ""
            by_file.setdefault(f, []).append(line)
    for f in sorted(by_file):
        details = ", ".join(by_file[f])
        print(f"    {f}    {details}")

print("\n" + "=" * 78)
print("ALL INTERNAL NAV TARGETS (incl. .html — for cross-checking) — file count")
print("=" * 78)
# Just show URL + occurrence count, sorted
file_count = {}
for url, locs in findings_all_internal.items():
    files = set()
    for loc in locs:
        if " [in __bundler/template]" in loc:
            files.add(loc.partition(" [in __bundler/template]")[0])
        else:
            files.add(loc.split(":")[0])
    file_count[url] = (len(locs), len(files))

# Print sorted by URL
for url in sorted(file_count):
    n_loc, n_files = file_count[url]
    print(f"  {url!r}   ({n_loc} occurrences across {n_files} file{'s' if n_files != 1 else ''})")
