from __future__ import annotations

import html as html_lib
import re
import urllib.request
from pathlib import Path

ACCOUNT_ID = "143157"
PROFILE_URL = f"https://jungol.co.kr/account/{ACCOUNT_ID}"
OUTPUT_DEFAULT = Path("jungol-card.svg")
OUTPUT_V1 = Path("designs/v1.svg")
OUTPUT_V2 = Path("designs/v2.svg")
OUTPUT_COMPACT = Path("designs/compact.svg")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}

TIER_GROUPS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby"]

# Palette follows the visual language of mazassumnida v2, adapted for JUNGOL.
BACKGROUND_COLOR = {
    "Bronze": ("#F49347", "#984400", "#492000"),
    "Silver": ("#939195", "#6B7E91", "#1F354A"),
    "Gold": ("#FFC944", "#FFAF44", "#FF9632"),
    "Platinum": ("#8CC584", "#45B2D3", "#51A795"),
    "Diamond": ("#96B8DC", "#3EA5DB", "#4D6399"),
    "Ruby": ("#E45B62", "#E14476", "#CA0059"),
    "Unknown": ("#AAAAAA", "#666666", "#000000"),
}

# JUNGOL numeric tier 1..30 = Bronze V .. Ruby I.
TIER_BOUNDS = {
    1: (30, 60), 2: (60, 90), 3: (90, 120), 4: (120, 150), 5: (150, 200),
    6: (200, 300), 7: (300, 400), 8: (400, 500), 9: (500, 650), 10: (650, 800),
    11: (800, 950), 12: (950, 1100), 13: (1100, 1250), 14: (1250, 1400), 15: (1400, 1600),
    16: (1600, 1750), 17: (1750, 1900), 18: (1900, 2000), 19: (2000, 2100), 20: (2100, 2200),
    21: (2200, 2300), 22: (2300, 2400), 23: (2400, 2500), 24: (2500, 2600), 25: (2600, 2700),
    26: (2700, 2800), 27: (2800, 2850), 28: (2850, 2900), 29: (2900, 2950), 30: (2950, 3000),
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
    tier_name = title.split("·", 1)[1].strip() if "·" in title else "Unknown"

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
        group = TIER_GROUPS[(tier_number - 1) // 5]
        level = 5 - ((tier_number - 1) % 5)
        return group, str(level)

    parts = fallback_name.split()
    return (parts[0] if parts else "Unknown", parts[-1] if len(parts) > 1 else "")


def progress_info(tier_number: int, rv: int | None) -> tuple[int, int, int, float]:
    if rv is None or tier_number not in TIER_BOUNDS:
        return 0, 0, 0, 35.0

    minimum, target = TIER_BOUNDS[tier_number]
    span = max(1, target - minimum)
    current = max(minimum, min(rv, target))
    percentage = round((current - minimum) * 100 / span)
    bar_end = 35 + 2.55 * percentage
    return percentage, rv, target, bar_end


def profile_values(profile: dict[str, object]) -> dict[str, object]:
    handle = html_lib.escape(str(profile["handle"]))
    rank = html_lib.escape(str(profile["rank"]))
    tier_name = str(profile["tier_name"])
    tier_number = int(profile["tier_number"])
    rv = profile["rv"] if isinstance(profile["rv"], int) else None
    solved = profile["solved"] if isinstance(profile["solved"], int) else None
    tier_group, tier_level = tier_display(tier_number, tier_name)
    percentage, current_rv, target_rv, bar_end = progress_info(tier_number, rv)
    color1, color2, color3 = BACKGROUND_COLOR.get(tier_group, BACKGROUND_COLOR["Unknown"])

    return {
        "handle": handle,
        "rank": rank,
        "tier_name": html_lib.escape(tier_name),
        "tier_group": html_lib.escape(tier_group),
        "tier_level": html_lib.escape(tier_level),
        "rv": str(rv) if rv is not None else "-",
        "solved": str(solved) if solved is not None else "-",
        "percentage": percentage,
        "progress": f"{current_rv} / {target_rv}" if rv is not None else "-",
        "bar_end": bar_end,
        "color1": color1,
        "color2": color2,
        "color3": color3,
    }


def render_v1(profile: dict[str, object]) -> str:
    p = profile_values(profile)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="350" height="170" viewBox="0 0 350 170" role="img" aria-label="JUNGOL {p['handle']} {p['tier_name']}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{p['color1']}"/>
      <stop offset="55%" stop-color="{p['color2']}"/>
      <stop offset="100%" stop-color="{p['color3']}"/>
    </linearGradient>
  </defs>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&amp;display=block');
    text {{ fill:#fff; font-family:'Noto Sans KR',sans-serif; }}
    .handle {{ font-size:21px; font-weight:700; }}
    .tier {{ font-size:20px; font-weight:700; opacity:.72; }}
    .label {{ font-size:14px; font-weight:500; }}
    .value {{ font-size:14px; font-weight:400; }}
    .small {{ font-size:11px; font-weight:400; }}
  </style>
  <rect width="350" height="170" rx="10" fill="url(#bg)"/>
  <text x="35" y="48" class="handle">{p['handle']}</text>
  <text x="315" y="48" text-anchor="end" class="tier">{p['tier_group']} {p['tier_level']}</text>
  <text x="35" y="79" class="label">rate</text><text x="145" y="79" class="value">{p['rv']}</text>
  <text x="35" y="100" class="label">solved</text><text x="145" y="100" class="value">{p['solved']}</text>
  <text x="35" y="121" class="label">rank</text><text x="145" y="121" class="value">#{p['rank']}</text>
  <line x1="35" y1="142" x2="290" y2="142" stroke="floralwhite" stroke-opacity=".4" stroke-width="4" stroke-linecap="round"/>
  <line x1="35" y1="142" x2="{p['bar_end']:.2f}" y2="142" stroke="floralwhite" stroke-width="4" stroke-linecap="round"/>
  <text x="297" y="145" class="small">{p['percentage']}%</text>
  <text x="293" y="158" text-anchor="end" class="small">{p['progress']}</text>
</svg>
'''


def render_v2(profile: dict[str, object]) -> str:
    p = profile_values(profile)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="350" height="170" viewBox="0 0 350 170" role="img" aria-label="JUNGOL {p['handle']} {p['tier_name']}">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&amp;display=block');
    @keyframes fadeIn {{ from {{ opacity:0; }} to {{ opacity:1; }} }}
    @keyframes delayed {{ 0%,80% {{ opacity:0; }} 100% {{ opacity:1; }} }}
    @keyframes barIn {{ 0%,70% {{ stroke-dashoffset:{p['bar_end']:.2f}; }} 100% {{ stroke-dashoffset:35; }} }}
    text {{ fill:white; font-family:'Noto Sans KR',sans-serif; text-rendering:geometricPrecision; }}
    .handle {{ font-size:1.30em; font-weight:700; letter-spacing:-.02em; animation:fadeIn 1s ease-in-out forwards; }}
    .tier-title {{ font-size:1.38em; font-weight:700; font-style:italic; letter-spacing:-.055em; opacity:0; animation:delayed 2s ease-in-out forwards; }}
    .tier-number {{ font-size:3.12em; font-weight:900; letter-spacing:-.055em; text-anchor:middle; opacity:0; animation:delayed 2s ease-in-out forwards; }}
    .subtitle {{ font-size:.90em; font-weight:500; letter-spacing:-.01em; }}
    .value {{ font-size:.90em; font-weight:400; letter-spacing:-.005em; }}
    .percentage {{ font-size:.80em; font-weight:300; }}
    .progress {{ font-size:.70em; font-weight:400; }}
    .item {{ opacity:0; animation:delayed 2s ease-in-out forwards; }}
    .rate-bar {{ stroke-dasharray:{p['bar_end']:.2f}; stroke-dashoffset:{p['bar_end']:.2f}; animation:barIn 1.5s ease-in-out forwards; }}
  </style>
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="35%">
      <stop offset="10%" stop-color="{p['color1']}" stop-opacity="1"><animate attributeName="stop-opacity" values=".7;.73;.9;.97;1;.97;.9;.73;.7" dur="4s" repeatCount="indefinite"/></stop>
      <stop offset="55%" stop-color="{p['color2']}" stop-opacity="1"><animate attributeName="stop-opacity" values="1;.95;.93;.95;1" dur="4s" repeatCount="indefinite"/></stop>
      <stop offset="100%" stop-color="{p['color3']}" stop-opacity="1"><animate attributeName="stop-opacity" values="1;.97;.9;.83;.8;.83;.9;.97;1" dur="4s" repeatCount="indefinite"/></stop>
    </linearGradient>
  </defs>
  <rect width="350" height="170" rx="10" fill="url(#grad)"/>

  <line x1="34" y1="50" x2="34" y2="105" stroke="white" stroke-width="2"><animate attributeName="y2" dur=".8s" fill="freeze" values="50;50;105" keyTimes="0;.675;1"/></line>
  <line x1="34" y1="105" x2="67" y2="125" stroke="white" stroke-width="2"><animate attributeName="x2" dur="1s" fill="freeze" values="34;34;67" keyTimes="0;.8;1"/><animate attributeName="y2" dur="1s" fill="freeze" values="105;105;125" keyTimes="0;.8;1"/></line>
  <line x1="67" y1="125" x2="100" y2="105" stroke="white" stroke-width="2"><animate attributeName="x2" dur="1.2s" fill="freeze" values="67;67;100" keyTimes="0;.833;1"/><animate attributeName="y2" dur="1.2s" fill="freeze" values="125;125;105" keyTimes="0;.833;1"/></line>
  <line x1="100" y1="105" x2="100" y2="50" stroke="white" stroke-width="2"><animate attributeName="y2" dur="1.5s" fill="freeze" values="105;105;50" keyTimes="0;.8;1"/></line>
  <line x1="67" y1="130" x2="34" y2="110" stroke="white" stroke-width="2"><animate attributeName="x2" dur="1.9s" fill="freeze" values="67;67;34" keyTimes="0;.789;1"/><animate attributeName="y2" dur="1.9s" fill="freeze" values="130;130;110" keyTimes="0;.789;1"/></line>
  <line x1="67" y1="130" x2="100" y2="110" stroke="white" stroke-width="2"><animate attributeName="x2" dur="1.9s" fill="freeze" values="67;67;100" keyTimes="0;.789;1"/><animate attributeName="y2" dur="1.9s" fill="freeze" values="130;130;110" keyTimes="0;.789;1"/></line>

  <text x="67" y="42" text-anchor="middle" class="tier-title">{p['tier_group']}</text>
  <text x="67" y="100" class="tier-number">{p['tier_level']}</text>
  <text x="135" y="50" class="handle">{p['handle']}</text>

  <g class="item" style="animation-delay:200ms"><text x="135" y="79" class="subtitle">rate</text><text x="225" y="79" class="value">{p['rv']}</text></g>
  <g class="item" style="animation-delay:400ms"><text x="135" y="99" class="subtitle">solved</text><text x="225" y="99" class="value">{p['solved']}</text></g>
  <g class="item" style="animation-delay:600ms"><text x="135" y="119" class="subtitle">rank</text><text x="225" y="119" class="value">#{p['rank']}</text></g>

  <g class="rate-bar" style="animation-delay:800ms"><line x1="35" y1="142" x2="{p['bar_end']:.2f}" y2="142" stroke="floralwhite" stroke-width="4" stroke-linecap="round"/></g>
  <line x1="35" y1="142" x2="290" y2="142" stroke="floralwhite" stroke-opacity=".4" stroke-width="4" stroke-linecap="round"/>
  <text x="297" y="142" dominant-baseline="middle" class="percentage">{p['percentage']}%</text>
  <text x="293" y="157" text-anchor="end" class="progress">{p['progress']}</text>
</svg>
'''


def render_compact(profile: dict[str, object]) -> str:
    p = profile_values(profile)
    short_tier = f"{p['tier_group'][0]}{p['tier_level']}" if p['tier_level'] else p['tier_group']
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="250" height="32" viewBox="0 0 250 32" role="img" aria-label="JUNGOL {p['handle']} {p['tier_name']}">
  <defs>
    <linearGradient id="tier" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="{p['color1']}"/><stop offset="55%" stop-color="{p['color2']}"/><stop offset="100%" stop-color="{p['color3']}"/></linearGradient>
  </defs>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&amp;display=block');
    text {{ fill:white; font-family:'Noto Sans KR',sans-serif; }}
  </style>
  <rect width="250" height="32" rx="6" fill="#343a40"/>
  <path d="M0 6a6 6 0 0 1 6-6h74v32H6a6 6 0 0 1-6-6z" fill="#24292f"/>
  <path d="M80 0h54v32H80z" fill="url(#tier)"/>
  <text x="40" y="21" text-anchor="middle" font-size="12" font-weight="700">JUNGOL</text>
  <text x="107" y="21" text-anchor="middle" font-size="13" font-weight="700">{short_tier}</text>
  <text x="144" y="20" font-size="12" font-weight="500">{p['handle']}</text>
  <text x="235" y="20" text-anchor="end" font-size="11" font-weight="400">{p['rv']} RV</text>
</svg>
'''


def main() -> None:
    page = fetch(PROFILE_URL).decode("utf-8", "replace")
    profile = parse_profile(page)
    print(profile)

    if profile["handle"] != "Lir09":
        raise RuntimeError(f"unexpected JUNGOL account: {profile['handle']}")

    OUTPUT_V1.parent.mkdir(parents=True, exist_ok=True)
    v1 = render_v1(profile)
    v2 = render_v2(profile)
    compact = render_compact(profile)

    OUTPUT_V1.write_text(v1, encoding="utf-8")
    OUTPUT_V2.write_text(v2, encoding="utf-8")
    OUTPUT_COMPACT.write_text(compact, encoding="utf-8")
    OUTPUT_DEFAULT.write_text(v2, encoding="utf-8")

    print(f"wrote {OUTPUT_DEFAULT}, {OUTPUT_V1}, {OUTPUT_V2}, {OUTPUT_COMPACT}")


if __name__ == "__main__":
    main()
