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

    # Larger handwritten tier wordmark for better readability on GitHub README.
    display_height = 38.0
    display_width = display_height * source_width / source_height
    if display_width > 106.0:
        display_width = 106.0
        display_height = display_width * source_height / source_width

    x = 67.0 - display_width / 2
    # Move the wordmark slightly lower so it sits closer to the crest.
    y = 11.0 + (39.0 - display_height) / 2
    encoded = base64.b64encode(data).decode("ascii")

    return (
        f'<image x="{x:.2f}" y="{y:.2f}" width="{display_width:.2f}" '
        f'height="{display_height:.2f}" class="tier-title" '
        f'preserveAspectRatio="xMidYMid meet" '
        f'href="data:image/png;base64,{encoded}"/>'
    )


def replace_wordmark(svg: str) -> str:
    def replacement(match: re.Match[str]) -> str:
        return wordmark_image(match.group(1))

    return TIER_RE.sub(replacement, svg)


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
