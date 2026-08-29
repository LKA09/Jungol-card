from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://jungol.co.kr"
CANDIDATES = ["Lir09", "lir09", "LIR09", "lka09", "LKA09"]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
    "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}


def fetch(url: str) -> tuple[int, str, str]:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=25) as res:
            return res.status, res.read().decode("utf-8", "replace"), res.geturl()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace"), exc.geturl()


def snippet(text: str, needle: str, before: int = 500, after: int = 1600) -> str:
    idx = text.lower().find(needle.lower())
    if idx < 0:
        return text[: min(len(text), 1800)].replace("\n", " ")
    return text[max(0, idx-before): idx+after].replace("\n", " ")


print("=== account __data variants ===")
for handle in CANDIDATES:
    url = f"{BASE}/account/{urllib.parse.quote(handle)}/__data.json"
    status, text, final = fetch(url)
    print("\n", handle, status, final, "len", len(text))
    print(snippet(text, handle))

print("\n=== direct internal-ish endpoints ===")
paths = []
for handle in CANDIDATES:
    q = urllib.parse.quote(handle)
    paths += [
        f"/$/account/{q}",
        f"/$/account/{q}/stat",
        f"/$/account/find?query={q}",
        f"/$/account/search?query={q}",
        f"/$/account?handle={q}",
    ]
paths += ["/$/ranking", "/$/rank", "/$/account/rank"]
for path in paths:
    status, text, final = fetch(BASE + path)
    print("\n", path, "=>", status, final, "len", len(text))
    print(snippet(text, "lir09", 300, 1200))

print("\n=== find ranking node ===")
_, html, _ = fetch(BASE + "/ranking")
app_match = re.search(r'import\("\./(_app/immutable/entry/app\.[^"]+\.js)"\)', html)
if not app_match:
    raise SystemExit("app manifest not found")
app_url = urllib.parse.urljoin(BASE + "/", app_match.group(1))
print("app:", app_url)
_, app, _ = fetch(app_url)

node_match = re.search(r'\.\./nodes/119\.([^"\\]+)\.js', app)
if not node_match:
    print("node 119 filename not found")
    print(snippet(app, '"/app/ranking"', 2000, 5000))
    raise SystemExit(0)
node_rel = "_app/immutable/nodes/119." + node_match.group(1) + ".js"
node_url = urllib.parse.urljoin(BASE + "/", node_rel)
print("node119:", node_url)
_, node, _ = fetch(node_url)
print("node119 len", len(node))
print(node[:12000].replace("\n", " "))

imports = sorted(set(re.findall(r'from"(\.\./chunks/[^\"]+\.js)"', node) + re.findall(r'import\("(\.\./chunks/[^\"]+\.js)"\)', node)))
print("\nnode119 chunks", imports)
for rel in imports:
    url = urllib.parse.urljoin(node_url, rel)
    _, text, _ = fetch(url)
    low = text.lower()
    if not any(k in low for k in ["rank", "rating", "tier", "account", "$/"]):
        continue
    print("\nCHUNK", url, "len", len(text))
    for key in ["$/", "ranking", "rank", "rating", "tier", "account"]:
        if key.lower() in low:
            print("--", key, "--")
            print(snippet(text, key, 700, 2200))
