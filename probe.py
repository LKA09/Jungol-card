from __future__ import annotations

import urllib.error
import urllib.request

BASE = "https://jungol.co.kr"
ACCOUNT_ID = "143157"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
    "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}


def fetch(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=25) as res:
            return res.status, res.read().decode("utf-8", "replace"), res.geturl(), dict(res.headers.items())
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace"), exc.geturl(), dict(exc.headers.items())


for path in [
    f"/account/{ACCOUNT_ID}",
    f"/account/{ACCOUNT_ID}/__data.json",
    f"/$/account/{ACCOUNT_ID}",
    f"/$/account/{ACCOUNT_ID}/stat",
]:
    status, text, final, headers = fetch(BASE + path)
    print("\n" + "=" * 120)
    print(path, "=>", status, final, headers.get("Content-Type"), "len", len(text))
    for needle in ["Lir09", '"tier"', '"rating"', '"rank"', '"solved"', '"handle"', '"aid"']:
        idx = text.lower().find(needle.lower())
        if idx >= 0:
            print("\nNEEDLE", needle)
            print(text[max(0, idx-1000):idx+3500].replace("\n", " "))
    print("\nHEAD")
    print(text[:4500].replace("\n", " "))
