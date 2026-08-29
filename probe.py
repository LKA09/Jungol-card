from __future__ import annotations

import urllib.error
import urllib.request

HANDLE = "Lir09"
BASE = "https://jungol.co.kr"
URLS = [
    f"{BASE}/ranking",
    f"{BASE}/ranking?account={HANDLE}",
    f"{BASE}/ranking?handle={HANDLE}",
    f"{BASE}/ranking?query={HANDLE}",
    f"{BASE}/ranking?search={HANDLE}",
    f"{BASE}/ranking/__data.json",
    f"{BASE}/ranking/__data.json?account={HANDLE}",
    f"{BASE}/ranking/__data.json?handle={HANDLE}",
    f"{BASE}/ranking/__data.json?query={HANDLE}",
    f"{BASE}/ranking/__data.json?search={HANDLE}",
    f"{BASE}/account/{HANDLE}",
    f"{BASE}/account/{HANDLE}/__data.json",
    f"{BASE}/account?handle={HANDLE}",
    f"{BASE}/account/__data.json?handle={HANDLE}",
    f"{BASE}/user/{HANDLE}",
    f"{BASE}/user/{HANDLE}/__data.json",
    f"{BASE}/profile/{HANDLE}",
    f"{BASE}/profile/{HANDLE}/__data.json",
]

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
    "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}

for url in URLS:
    print("\n" + "=" * 100)
    print(url)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            raw = res.read()
            text = raw.decode("utf-8", "replace")
            print("status:", res.status)
            print("final url:", res.geturl())
            print("type:", res.headers.get("content-type"))
            print("length:", len(raw))
            idx = text.lower().find(HANDLE.lower())
            print("contains handle:", idx >= 0, "index:", idx)
            if idx >= 0:
                print("around handle:", text[max(0, idx-800):idx+1800].replace("\n", " "))
            else:
                print("head:", text[:1500].replace("\n", " "))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        print("HTTP ERROR", e.code, body[:1200].replace("\n", " "))
    except Exception as e:
        print("ERROR", repr(e))
