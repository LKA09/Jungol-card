from __future__ import annotations

import re
import urllib.parse
import urllib.request

BASE = "https://jungol.co.kr"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
    "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=25) as res:
        return res.read().decode("utf-8", "replace")


html = fetch(f"{BASE}/ranking")
print("=== HTML tail ===")
print(html[-7000:].replace("\n", " "))

raw_assets = sorted(set(re.findall(r'(?:\./|/)?_app/immutable/[A-Za-z0-9_./-]+\.js', html)))
print("\n=== JS assets from HTML ===")
for item in raw_assets:
    print(item)

urls = [urllib.parse.urljoin(BASE + "/", x.replace("./", "")) for x in raw_assets]
print("\n=== interesting JS snippets ===")
for url in urls:
    try:
        text = fetch(url)
    except Exception as exc:
        print("ERR", url, repr(exc))
        continue
    low = text.lower()
    if not any(x in low for x in ["ranking", "ranklist", "accountfind", "api.jungol", "$/account", "/rank"]):
        continue
    print("\nASSET", url, "LEN", len(text))
    for needle in ["api.jungol", "ranking", "RankList", "AccountFind", "$/account", "/rank", "rating", "tier"]:
        start = 0
        count = 0
        while count < 10:
            idx = low.find(needle.lower(), start)
            if idx == -1:
                break
            print("---", needle, "---")
            print(text[max(0, idx-900):idx+1800].replace("\n", " "))
            start = idx + len(needle)
            count += 1
