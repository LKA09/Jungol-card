from pathlib import Path

from generate_card import TIER_BOUNDS, render_v2, tier_display

OUTPUT_DIR = Path("designs/tiers")
ROMAN = {"5": "v", "4": "iv", "3": "iii", "2": "ii", "1": "i"}


def preview_profile(tier_number: int) -> dict[str, object]:
    minimum, target = TIER_BOUNDS[tier_number]
    rv = (minimum + target) // 2
    tier_group, tier_level = tier_display(tier_number, "Unknown")

    return {
        "handle": "Preview",
        "tier_name": f"{tier_group} {tier_level}",
        "tier_number": tier_number,
        "rank": "1,000",
        "rv": rv,
        "solved": 100,
    }


def file_name(tier_number: int) -> str:
    tier_group, tier_level = tier_display(tier_number, "Unknown")
    return f"{tier_number:02d}-{tier_group.lower()}-{ROMAN[tier_level]}.svg"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for tier_number in range(1, 31):
        path = OUTPUT_DIR / file_name(tier_number)
        path.write_text(render_v2(preview_profile(tier_number)), encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
