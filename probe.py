from __future__ import annotations

import re
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://jungol.co.kr"
HANDLE = "Lir09"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
    "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}


def fetch(url: str) -> tuple[int, str, dict[str, str]]:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=25) as res:
        raw = res.read()
        return res.status, raw.decode("utf-8", "replace"), dict(res.headers.items())


print("=== ranking HTML discovery ===")
status, html, headers = fetch(f"{BASE}/ranking")
print("status", status, "length", len(html))

for pat in [r'https://[^"\'<> ]+', r'(?:src|href)="([^"]+)"']:
    vals = re.findall(pat, html)
    print("\npattern", pat)
    seen = set()
    for value in vals:
        value = value if isinstance(value, str) else value[0]
        if value in seen:
            continue
        seen.add(value)
        if "api." in value or value.endswith(".js") or "/_app/" in value:
            print(value)

api_hits = sorted(set(re.findall(r'https://api\.[A-Za-z0-9._/-]+', html)))
print("\napi hosts/urls:", api_hits)

assets = []
for src in re.findall(r'(?:src|href)="([^"]+\.js(?:\?[^"]*)?)"', html):
    assets.append(urllib.parse.urljoin(BASE, src))

print("\n=== JS bundle ranking/API snippets ===")
for url in assets:
    try:
        _, text, _ = fetch(url)
    except Exception as exc:
        print("asset error", url, repr(exc))
        continue
    low = text.lower()
    if "ranking" not in low and "api.jungol" not in low:
        continue
    print("\nASSET", url, "len", len(text))
    for needle in ["api.jungol", "ranking", "$/ranking", "/account/"]:
        start = 0
        shown = 0
        while shown < 6:
            idx = low.find(needle.lower(), start)
            if idx < 0:
                break
            print("needle", needle, "=>", text[max(0, idx-500):idx+1000].replace("\n", " "))
            start = idx + len(needle)
            shown += 1

print("\n=== likely API endpoints ===")
api_base = "https://api.jungol.co.kr"
paths = [
    "/ranking",
    f"/ranking?account={HANDLE}",
    f"/ranking?handle={HANDLE}",
    f"/account/{HANDLE}",
    f"/account?handle={HANDLE}",
    f"/account/search?handle={HANDLE}",
    f"/account/ranking?handle={HANDLE}",
]
for path in paths:
    url = api_base + path
    print("\n", url)
    try:
        status, text, hdr = fetch(url)
        print("status", status, "type", hdr.get("Content-Type"), "length", len(text))
        idx = text.lower().find(HANDLE.lower())
        if idx >= 0:
            print(text[max(0, idx-700):idx+2000].replace("\n", " "))
        else:
            print(text[:1800].replace("\n", " "))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        print("HTTP", exc.code, body[:1200].replace("\n", " "))
    except Exception as exc:
        print("ERROR", repr(exc))
