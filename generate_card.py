from __future__ import annotations

import base64
import html as html_lib
import re
import urllib.request
from pathlib import Path

ACCOUNT_ID = "143157"
PROFILE_URL = f"https://jungol.co.kr/account/{ACCOUNT_ID}"
TIER_ICON_URL = "https://s.jungol.co.kr/solved/{tier}.svg"
OUTPUT = Path("jungol-card.svg")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=25) as response:
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


def tier_color(name: str) -> str:
    prefix = name.split()[0].lower() if name else ""
    return {
        "bronze": "#ad5600",
        "silver": "#435f7a",
        "gold": "#ec9a00",
        "platinum": "#27e2a4",
        "diamond": "#00b4fc",
        "ruby": "#ff0062",
    }.get(prefix, "#6e7681")


def parse_profile(page: str) -> dict[str, object]:
    title = meta(page, "og:title") or "@Lir09 · JUNGOL"
    description = meta(page, "og:description") or ""

    handle_match = re.search(r"@([^\s·]+)", title)
    handle = handle_match.group(1) if handle_match else "Lir09"
    tier_name = title.split("·", 1)[1].strip() if "·" in title else "JUNGOL"

    rank_match = re.search(r"rank\s+([\d,]+)", description, re.IGNORECASE)
    rank_text = rank_match.group(1) if rank_match else "-"

    # JUNGOL's SSR payload currently exposes rank, numeric tier and RV together.
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


def get_icon_data_uri(tier_number: int) -> str | None:
    if tier_number <= 0:
        return None
    try:
        icon = fetch(TIER_ICON_URL.format(tier=tier_number))
        encoded = base64.b64encode(icon).decode("ascii")
        return f"data:image/svg+xml;base64,{encoded}"
    except Exception as exc:
        print(f"warning: tier icon fetch failed: {exc}")
        return None


def make_svg(profile: dict[str, object], icon_uri: str | None) -> str:
    handle = html_lib.escape(str(profile["handle"]))
    tier_name = html_lib.escape(str(profile["tier_name"]))
    rank = html_lib.escape(str(profile["rank"]))
    rv = profile["rv"]
    solved = profile["solved"]
    accent = tier_color(str(profile["tier_name"]))

    solved_text = str(solved) if isinstance(solved, int) else "-"
    rv_text = str(rv) if isinstance(rv, int) else "-"

    if icon_uri:
        icon = f'<image href="{icon_uri}" x="22" y="35" width="98" height="98" preserveAspectRatio="xMidYMid meet"/>'
    else:
        short = html_lib.escape("".join(part[0] for part in str(profile["tier_name"]).split()[:2]).upper() or "J")
        icon = f'''<circle cx="71" cy="84" r="46" fill="{accent}" fill-opacity="0.14" stroke="{accent}" stroke-width="2"/>
        <text x="71" y="92" text-anchor="middle" class="fallback" fill="{accent}">{short}</text>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="380" height="170" viewBox="0 0 380 170" role="img" aria-label="JUNGOL profile badge for {handle}: {tier_name}">
  <style>
    .bg {{ fill: #ffffff; }}
    .border {{ fill: none; stroke: #d0d7de; }}
    .title {{ font: 700 15px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill: #57606a; letter-spacing: .8px; }}
    .handle {{ font: 600 16px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill: #24292f; }}
    .tier {{ font: 800 26px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    .value {{ font: 700 14px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill: #24292f; }}
    .label {{ font: 500 11px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill: #6e7781; }}
    .fallback {{ font: 800 23px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #0d1117; }}
      .border {{ stroke: #30363d; }}
      .title, .label {{ fill: #8b949e; }}
      .handle, .value {{ fill: #f0f6fc; }}
    }}
  </style>

  <rect class="bg" x="0.5" y="0.5" width="379" height="169" rx="12"/>
  <rect class="border" x="0.5" y="0.5" width="379" height="169" rx="12"/>
  <rect x="0" y="0" width="5" height="170" rx="2.5" fill="{accent}"/>

  {icon}

  <text x="140" y="36" class="title">JUNGOL PROFILE</text>
  <text x="140" y="62" class="handle">@{handle}</text>
  <text x="140" y="96" class="tier" fill="{accent}">{tier_name}</text>

  <text x="140" y="125" class="label">RANK</text>
  <text x="140" y="145" class="value">#{rank}</text>

  <text x="225" y="125" class="label">SOLVED</text>
  <text x="225" y="145" class="value">{solved_text}</text>

  <text x="318" y="125" class="label">RV</text>
  <text x="318" y="145" class="value">{rv_text}</text>
</svg>
'''


def main() -> None:
    page = fetch(PROFILE_URL).decode("utf-8", "replace")
    profile = parse_profile(page)
    print(profile)

    if profile["handle"] != "Lir09":
        raise RuntimeError(f"unexpected JUNGOL account: {profile['handle']}")

    icon_uri = get_icon_data_uri(int(profile["tier_number"]))
    OUTPUT.write_text(make_svg(profile, icon_uri), encoding="utf-8")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
