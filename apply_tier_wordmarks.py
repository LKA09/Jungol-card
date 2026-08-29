from __future__ import annotations

import base64
import re
import struct
import urllib.request
from functools import lru_cache
from pathlib import Path

WORDMARK_BASE = "https://raw.githubusercontent.com/mazassumnida/mazassumnida/master/api/image"
TARGETS = [
    Path("jungol-card.svg"),
    Path("designs/v2.svg"),
]
TARGETS.extend(sorted(Path("designs/tiers").glob("*.svg")))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (GitHub Actions; JUNGOL Card)",
    "Accept": "image/png,*/*;q=0.8",
}

TIER_RE = re.compile(
    r'<text\s+x="67"\s+y="42"\s+text-anchor="middle"\s+class="tier-title">'
    r'(Bronze|Silver|Gold|Platinum|Diamond|Ruby)</text>'
)

BOLD_FILTER = '''<filter id="tierWordmarkBold" x="-20%" y="-25%" width="140%" height="150%">
      <feMorphology in="SourceGraphic" operator="dilate" radius="0.55"/>
    </filter>'''


def png_size(data: bytes) -> tuple[int, int]:
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("invalid PNG wordmark")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


@lru_cache(maxsize=None)
def wordmark_image(tier: str) -> str:
    url = f"{WORDMARK_BASE}/{tier}.png"
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=25) as response:
        data = response.read()

    source_width, source_height = png_size(data)

    # Slightly larger than the original v2 wordmark so it reads clearly on GitHub.
    display_height = 33.0
    display_width = display_height * source_width / source_height
    if display_width > 96:
        display_width = 96.0
        display_height = display_width * source_height / source_width

    x = 67.0 - display_width / 2
    y = 11.5 + (33.0 - display_height) / 2
    encoded = base64.b64encode(data).decode("ascii")

    return (
        f'<image x="{x:.2f}" y="{y:.2f}" width="{display_width:.2f}" '
        f'height="{display_height:.2f}" class="tier-title" '
        f'filter="url(#tierWordmarkBold)" '
        f'preserveAspectRatio="xMidYMid meet" '
        f'href="data:image/png;base64,{encoded}"/>'
    )


def ensure_bold_filter(svg: str) -> str:
    if 'id="tierWordmarkBold"' in svg:
        return svg

    marker = "<defs>"
    if marker not in svg:
        return svg

    return svg.replace(marker, f"{marker}\n    {BOLD_FILTER}", 1)


def replace_wordmark(svg: str) -> str:
    def replacement(match: re.Match[str]) -> str:
        return wordmark_image(match.group(1))

    replaced = TIER_RE.sub(replacement, svg)
    if replaced != svg:
        replaced = ensure_bold_filter(replaced)
    return replaced


def main() -> None:
    changed = 0

    for path in TARGETS:
        if not path.exists():
            continue

        before = path.read_text(encoding="utf-8")
        after = replace_wordmark(before)

        if after != before:
            path.write_text(after, encoding="utf-8")
            changed += 1
            print(f"wordmark applied: {path}")

    print(f"updated {changed} SVG files")


if __name__ == "__main__":
    main()
