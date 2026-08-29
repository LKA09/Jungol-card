from __future__ import annotations

import html as html_lib
import re
import urllib.request
from pathlib import Path

ACCOUNT_ID = "143157"
PROFILE_URL = f"https://jungol.co.kr/account/{ACCOUNT_ID}"
OUTPUT = Path("jungol-card.svg")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}

TIER_GROUPS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby"]

# JUNGOL RV boundaries used for the progress-to-next-tier bar.
# key = numeric JUNGOL tier, value = (current tier minimum RV, next tier RV)
TIER_BOUNDS = {
    1: (0, 30),
    2: (30, 60),
    3: (60, 90),
    4: (120, 150),
    5: (150, 200),
    6: (200, 300),
    7: (300, 400),
    8: (400, 500),
    9: (500, 650),
    10: (650, 800),
    11: (800, 950),
    12: (950, 1100),
    13: (1100, 1250),
    14: (1250, 1400),
    15: (1400, 1600),
    16: (1600, 1750),
    17: (1750, 1900),
    18: (1900, 2050),
    19: (2050, 2200),
    20: (2200, 2350),
    21: (2350, 2500),
    22: (2500, 2650),
    23: (2650, 2800),
    24: (2800, 2950),
    25: (2950, 3100),
    26: (3100, 3250),
    27: (3250, 3400),
    28: (3400, 3550),
    29: (3550, 3700),
    30: (3700, 4000),
}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=25) as response:
        return response.read()


def meta(page: str, prop: str) -> str | None:
    patterns = [
        rf'<meta\s+property=["\']{re.escape(prop)}["\']\s+content=["\']([^"\']*)["\']',
        rf'<meta\s+content=["\']([^"\']*)["\']\s+property=["\']{re.escape(prop)}["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, page, re.IGNORECASE)
        if match:
            return html_lib.unescape(match.group(1))
    return None


def parse_profile(page: str) -> dict[str, object]:
    title = meta(page, "og:title") or "@Lir09 · JUNGOL"
    description = meta(page, "og:description") or ""

    handle_match = re.search(r"@([^\s·]+)", title)
    handle = handle_match.group(1) if handle_match else "Lir09"
    tier_name = title.split("·", 1)[1].strip() if "·" in title else "JUNGOL"

    rank_match = re.search(r"rank\s+([\d,]+)", description, re.IGNORECASE)
    rank_text = rank_match.group(1) if rank_match else "-"

    stats_match = re.search(r"rank:(\d+),tier:(\d+),rv:(\d+),rankBaseRv:", page)
    if stats_match:
        rank_text = f"{int(stats_match.group(1)):,}"
        tier_number = int(stats_match.group(2))
        rv = int(stats_match.group(3))
    else:
        tier_number = 0
        rv = None

    solved_count = None
    solved_match = re.search(r"solved:\[(.*?)\],wrong:\[", page, re.DOTALL)
    if solved_match:
        solved_count = len(re.findall(r"\{id:\d+,tier:\{", solved_match.group(1)))

    return {
        "handle": handle,
        "tier_name": tier_name,
        "tier_number": tier_number,
        "rank": rank_text,
        "rv": rv,
        "solved": solved_count,
    }


def tier_display(tier_number: int, fallback_name: str) -> tuple[str, str]:
    if 1 <= tier_number <= 30:
        group_index = (tier_number - 1) // 5
        level = 5 - ((tier_number - 1) % 5)
        return TIER_GROUPS[group_index], str(level)

    parts = fallback_name.split()
    return (parts[0] if parts else "JUNGOL", parts[-1] if len(parts) > 1 else "-")


def progress_info(tier_number: int, rv: int | None) -> tuple[int, int, int]:
    if rv is None or tier_number not in TIER_BOUNDS:
        return 0, 100, 0

    minimum, target = TIER_BOUNDS[tier_number]
    span = max(1, target - minimum)
    gained = max(0, min(rv - minimum, span))
    percent = round(gained / span * 100)
    return percent, rv, target


def make_svg(profile: dict[str, object]) -> str:
    handle = html_lib.escape(str(profile["handle"]))
    rank = html_lib.escape(str(profile["rank"]))
    tier_name = str(profile["tier_name"])
    tier_number = int(profile["tier_number"])
    rv = profile["rv"] if isinstance(profile["rv"], int) else None
    solved = profile["solved"] if isinstance(profile["solved"], int) else None

    tier_group, tier_level = tier_display(tier_number, tier_name)
    tier_group = html_lib.escape(tier_group)
    tier_level = html_lib.escape(tier_level)

    percent, current_rv, target_rv = progress_info(tier_number, rv)
    track_x = 34
    track_width = 258
    fill_width = round(track_width * percent / 100)

    rv_text = str(rv) if rv is not None else "-"
    solved_text = str(solved) if solved is not None else "-"
    progress_text = f"{current_rv} / {target_rv}" if rv is not None else "-"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="350" height="170" viewBox="0 0 350 170" role="img" aria-label="JUNGOL {handle} {html_lib.escape(tier_name)}">
  <defs>
    <linearGradient id="card" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8f939a"/>
      <stop offset="34%" stop-color="#617489"/>
      <stop offset="100%" stop-color="#17304b"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="350" height="170" rx="11" fill="url(#card)"/>

  <!-- tier emblem -->
  <text x="38" y="47" fill="#fff" font-family="Segoe Print, Bradley Hand, cursive" font-size="24" font-style="italic">{tier_group}</text>
  <path d="M34 51 V108 L68 127 L102 108 V51" fill="none" stroke="#fff" stroke-width="2" opacity=".95"/>
  <path d="M34 108 L68 132 L102 108" fill="none" stroke="#fff" stroke-width="2" opacity=".95"/>
  <text x="68" y="101" text-anchor="middle" fill="#fff" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="700">{tier_level}</text>

  <!-- profile -->
  <text x="136" y="51" fill="#fff" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="700">{handle}</text>

  <g fill="#fff" font-family="Arial, Helvetica, sans-serif" font-size="15">
    <text x="136" y="80" font-weight="700">rate</text>
    <text x="226" y="80">{rv_text}</text>

    <text x="136" y="101" font-weight="700">solved</text>
    <text x="226" y="101">{solved_text}</text>

    <text x="136" y="122" font-weight="700">rank</text>
    <text x="226" y="122">#{rank}</text>
  </g>

  <!-- progress -->
  <rect x="{track_x}" y="141" width="{track_width}" height="4" rx="2" fill="#fff" opacity=".38"/>
  <rect x="{track_x}" y="141" width="{fill_width}" height="4" rx="2" fill="#fff"/>
  <text x="299" y="145" fill="#fff" font-family="Arial, Helvetica, sans-serif" font-size="12">{percent}%</text>
  <text x="292" y="158" text-anchor="end" fill="#fff" font-family="Arial, Helvetica, sans-serif" font-size="12" font-weight="700">{progress_text}</text>
</svg>
'''


def main() -> None:
    page = fetch(PROFILE_URL).decode("utf-8", "replace")
    profile = parse_profile(page)
    print(profile)

    if profile["handle"] != "Lir09":
        raise RuntimeError(f"unexpected JUNGOL account: {profile['handle']}")

    OUTPUT.write_text(make_svg(profile), encoding="utf-8")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
