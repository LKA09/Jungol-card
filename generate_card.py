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

# Matches the tier palette used by mazassumnida v2.
BACKGROUND_COLOR = {
    "Bronze": ("#F49347", "#984400", "#492000"),
    "Silver": ("#939195", "#6B7E91", "#1F354A"),
    "Gold": ("#FFC944", "#FFAF44", "#FF9632"),
    "Platinum": ("#8CC584", "#45B2D3", "#51A795"),
    "Diamond": ("#96B8DC", "#3EA5DB", "#4D6399"),
    "Ruby": ("#E45B62", "#E14476", "#CA0059"),
    "Unknown": ("#AAAAAA", "#666666", "#000000"),
}

# Current JUNGOL RV boundaries. Numeric tier 1..30 maps Bronze V .. Ruby I.
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


def make_svg(profile: dict[str, object]) -> str:
    handle = html_lib.escape(str(profile["handle"]))
    rank = html_lib.escape(str(profile["rank"]))
    tier_name = str(profile["tier_name"])
    tier_number = int(profile["tier_number"])
    rv = profile["rv"] if isinstance(profile["rv"], int) else None
    solved = profile["solved"] if isinstance(profile["solved"], int) else None

    tier_group, tier_level = tier_display(tier_number, tier_name)
    color1, color2, color3 = BACKGROUND_COLOR.get(tier_group, BACKGROUND_COLOR["Unknown"])
    percentage, current_rv, target_rv, bar_end = progress_info(tier_number, rv)

    solved_text = str(solved) if solved is not None else "-"
    rv_text = str(rv) if rv is not None else "-"
    progress_text = f"{current_rv} / {target_rv}" if rv is not None else "-"

    return f'''<svg height="170" width="350" viewBox="0 0 350 170"
    xmlns="http://www.w3.org/2000/svg" role="img"
    aria-label="JUNGOL {handle} {html_lib.escape(tier_name)}">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&amp;display=block');

    @keyframes fadeIn {{
      from {{ opacity: 0; }}
      to {{ opacity: 1; }}
    }}
    @keyframes delayFadeIn {{
      0%, 80% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
    }}
    @keyframes rateBarAnimation {{
      0%, 70% {{ stroke-dashoffset: {bar_end:.2f}; }}
      100% {{ stroke-dashoffset: 35; }}
    }}

    text {{
      fill: white;
      font-family: 'Noto Sans KR', sans-serif;
    }}
    .handle {{
      font-size: 1.30em;
      font-weight: 700;
      animation: fadeIn 1s ease-in-out forwards;
    }}
    .tier-title {{
      font-size: 1.35em;
      font-weight: 700;
      font-style: italic;
      opacity: 0;
      animation: delayFadeIn 2s ease-in-out forwards;
    }}
    .tier-number {{
      font-size: 3.1em;
      font-weight: 700;
      text-anchor: middle;
      opacity: 0;
      animation: delayFadeIn 2s ease-in-out forwards;
    }}
    .subtitle {{ font-weight: 500; font-size: 0.9em; }}
    .value {{ font-weight: 400; font-size: 0.9em; }}
    .percentage {{ font-weight: 300; font-size: 0.8em; }}
    .progress {{ font-size: 0.7em; }}
    .item {{
      opacity: 0;
      animation: delayFadeIn 2s ease-in-out forwards;
    }}
    .rate-bar {{
      stroke-dasharray: {bar_end:.2f};
      stroke-dashoffset: {bar_end:.2f};
      animation: rateBarAnimation 1.5s forwards ease-in-out;
    }}
  </style>

  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="35%">
      <stop offset="10%" stop-color="{color1}" stop-opacity="1">
        <animate attributeName="stop-opacity"
          values="0.7;0.73;0.9;0.97;1;0.97;0.9;0.73;0.7"
          dur="4s" repeatCount="indefinite"/>
      </stop>
      <stop offset="55%" stop-color="{color2}" stop-opacity="1">
        <animate attributeName="stop-opacity"
          values="1;0.95;0.93;0.95;1"
          dur="4s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="{color3}" stop-opacity="1">
        <animate attributeName="stop-opacity"
          values="1;0.97;0.9;0.83;0.8;0.83;0.9;0.97;1"
          dur="4s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
  </defs>

  <rect width="350" height="170" rx="10" ry="10" fill="url(#grad)"/>

  <!-- v2-style animated tier crest -->
  <line x1="34" y1="50" x2="34" y2="105" stroke-width="2" stroke="white">
    <animate attributeName="y2" dur="0.8s" fill="freeze"
      calcMode="spline" keyTimes="0;0.675;1" keySplines="0 0 1 1;0.5 0 0.5 1"
      values="50;50;105"/>
  </line>
  <line x1="34" y1="105" x2="67" y2="125" stroke-width="2" stroke="white">
    <animate attributeName="x2" dur="1s" fill="freeze" values="34;34;67" keyTimes="0;0.8;1"/>
    <animate attributeName="y2" dur="1s" fill="freeze" values="105;105;125" keyTimes="0;0.8;1"/>
  </line>
  <line x1="67" y1="125" x2="100" y2="105" stroke-width="2" stroke="white">
    <animate attributeName="x2" dur="1.2s" fill="freeze" values="67;67;100" keyTimes="0;0.833;1"/>
    <animate attributeName="y2" dur="1.2s" fill="freeze" values="125;125;105" keyTimes="0;0.833;1"/>
  </line>
  <line x1="100" y1="105" x2="100" y2="50" stroke-width="2" stroke="white">
    <animate attributeName="y2" dur="1.5s" fill="freeze" values="105;105;50" keyTimes="0;0.8;1"/>
  </line>
  <line x1="67" y1="130" x2="34" y2="110" stroke-width="2" stroke="white">
    <animate attributeName="x2" dur="1.9s" fill="freeze" values="67;67;34" keyTimes="0;0.789;1"/>
    <animate attributeName="y2" dur="1.9s" fill="freeze" values="130;130;110" keyTimes="0;0.789;1"/>
  </line>
  <line x1="67" y1="130" x2="100" y2="110" stroke-width="2" stroke="white">
    <animate attributeName="x2" dur="1.9s" fill="freeze" values="67;67;100" keyTimes="0;0.789;1"/>
    <animate attributeName="y2" dur="1.9s" fill="freeze" values="130;130;110" keyTimes="0;0.789;1"/>
  </line>

  <text x="67" y="42" class="tier-title" text-anchor="middle">{html_lib.escape(tier_group)}</text>
  <text x="67" y="100" class="tier-number">{html_lib.escape(tier_level)}</text>

  <text x="135" y="50" class="handle">{handle}</text>

  <g class="item" style="animation-delay:200ms">
    <text x="135" y="79" class="subtitle">rate</text>
    <text x="225" y="79" class="value">{rv_text}</text>
  </g>
  <g class="item" style="animation-delay:400ms">
    <text x="135" y="99" class="subtitle">solved</text>
    <text x="225" y="99" class="value">{solved_text}</text>
  </g>
  <g class="item" style="animation-delay:600ms">
    <text x="135" y="119" class="subtitle">rank</text>
    <text x="225" y="119" class="value">#{rank}</text>
  </g>

  <g class="rate-bar" style="animation-delay:800ms">
    <line x1="35" y1="142" x2="{bar_end:.2f}" y2="142"
      stroke-width="4" stroke="floralwhite" stroke-linecap="round"/>
  </g>
  <line x1="35" y1="142" x2="290" y2="142"
    stroke-width="4" stroke-opacity="40%" stroke="floralwhite" stroke-linecap="round"/>
  <text x="297" y="142" dominant-baseline="middle" class="percentage">{percentage}%</text>
  <text x="293" y="157" class="progress" text-anchor="end">{progress_text}</text>
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
