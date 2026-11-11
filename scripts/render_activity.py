#!/usr/bin/env python3
"""Render public GitHub contribution data as responsive neon SVG artwork."""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "contributions.json"
DESKTOP_OUTPUT = ROOT / "assets" / "activity.svg"
MOBILE_OUTPUT = ROOT / "assets" / "activity-mobile.svg"
PALETTE = ["#111A35", "#34235F", "#62348E", "#9D4EDD", "#00E5FF"]


def sunday_before(day: date) -> date:
    return day - timedelta(days=(day.weekday() + 1) % 7)


def render(payload: dict[str, object], *, mobile: bool) -> str:
    raw_days = payload.get("days")
    if not isinstance(raw_days, list) or len(raw_days) < 300:
        raise ValueError("Contribution JSON must contain at least 300 days")
    days: dict[date, dict[str, int]] = {}
    for raw in raw_days:
        if not isinstance(raw, dict):
            continue
        current = date.fromisoformat(str(raw["date"]))
        level = int(raw["level"])
        count = int(raw["count"])
        if not 0 <= level <= 4 or count < 0:
            raise ValueError(f"Invalid contribution value for {current}")
        days[current] = {"level": level, "count": count}

    last_day = max(days)
    end_saturday = sunday_before(last_day) + timedelta(days=6)
    start_sunday = end_saturday - timedelta(weeks=52)
    username = escape(str(payload.get("username", "GitHub user")))
    stats = payload.get("stats") if isinstance(payload.get("stats"), dict) else {}

    width, height = ((1000, 360) if not mobile else (560, 395))
    grid_x, grid_y = ((92, 138) if not mobile else (66, 160))
    cell, gap = ((11, 4) if not mobile else (6, 2))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{username} public GitHub activity</title>',
        '<desc id="desc">A verified 53-week public GitHub contribution calendar rendered as a neon animated SVG.</desc>',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#101A32"/><stop offset=".55" stop-color="#080D1B"/><stop offset="1" stop-color="#050816"/></linearGradient><linearGradient id="brand" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#9D4EDD"/><stop offset=".5" stop-color="#FF4ECD"/><stop offset="1" stop-color="#00E5FF"/></linearGradient></defs>',
        "<style>",
        "text{font-family:'Geist Mono','IBM Plex Mono','SFMono-Regular',Consolas,monospace}",
        ".day{opacity:0;animation:cell .68s cubic-bezier(.22,1,.36,1) forwards}",
        ".meta{opacity:0;animation:meta .8s cubic-bezier(.22,1,.36,1) .95s forwards}",
        ".scan{animation:scan 5.8s cubic-bezier(.22,1,.36,1) infinite}",
        "@keyframes cell{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}",
        "@keyframes meta{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}",
        "@keyframes scan{0%{opacity:0;transform:translateX(-120px)}18%{opacity:.7}68%,100%{opacity:0;transform:translateX(1020px)}}",
        "@media (prefers-reduced-motion:reduce){.day,.meta,.scan{animation:none!important;opacity:1!important;transform:none!important}}",
        "</style>",
        f'<rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="30" fill="#030510" stroke="#19254A"/>',
        f'<rect x="11" y="11" width="{width - 22}" height="{height - 22}" rx="24" fill="url(#bg)" stroke="#26365F"/>',
        '<circle cx="36" cy="36" r="5" fill="#FF5F57"/><circle cx="54" cy="36" r="5" fill="#FEBC2E"/><circle cx="72" cy="36" r="5" fill="#00FFA3"/>',
        '<text x="96" y="41" fill="#91A4C5" font-size="12" letter-spacing="1.2">public-signal / verified / 53w</text>',
        f'<line x1="24" y1="58" x2="{width - 24}" y2="58" stroke="#223259"/>',
        '<rect class="scan" x="24" y="59" width="135" height="1" fill="url(#brand)" opacity="0"/>',
        f'<text class="meta" x="{34 if mobile else 42}" y="{91 if mobile else 89}" fill="#EAF4FF" font-size="{12 if mobile else 14}" font-weight="700">PUBLIC GITHUB SIGNAL / {username}</text>',
        f'<text class="meta" x="{34 if mobile else 42}" y="{112 if mobile else 106}" fill="#91A4C5" font-size="9">PUBLIC CALENDAR ONLY · NO FABRICATED ACTIVITY</text>',
    ]

    month_labels: list[tuple[int, str]] = []
    last_month = -1
    for week in range(53):
        marker = start_sunday + timedelta(weeks=week, days=3)
        if marker.month != last_month:
            month_labels.append((week, marker.strftime("%b").upper()))
            last_month = marker.month
    if len(month_labels) > 1 and month_labels[1][0] - month_labels[0][0] < 3:
        month_labels.pop(0)
    for week, label in month_labels:
        x = grid_x + week * (cell + gap)
        parts.append(f'<text x="{x}" y="{grid_y - 10}" fill="#7184A9" font-size="{7 if mobile else 9}">{label}</text>')

    for label, row in (("MON", 1), ("WED", 3), ("FRI", 5)):
        y = grid_y + row * (cell + gap) + cell - 1
        parts.append(f'<text x="{30 if mobile else 42}" y="{y}" fill="#5D6F95" font-size="{7 if mobile else 8}">{label}</text>')

    for week in range(53):
        for row in range(7):
            current = start_sunday + timedelta(weeks=week, days=row)
            record = days.get(current, {"level": 0, "count": 0})
            x = grid_x + week * (cell + gap)
            y = grid_y + row * (cell + gap)
            delay = min(.03 + (week + row) * .017, 1.02)
            parts.append(
                f'<rect class="day" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="{2 if mobile else 3}" '
                f'fill="{PALETTE[record["level"]]}" style="animation-delay:{delay:.3f}s">'
                f'<title>{record["count"]} contributions on {current.isoformat()}</title></rect>'
            )

    footer_y = 328 if not mobile else 346
    total = int(stats.get("total", 0))
    active = int(stats.get("active_days", 0))
    streak = int(stats.get("longest_streak", 0))
    parts.append(f'<text class="meta" x="{34 if mobile else 42}" y="{footer_y}" fill="#00E5FF" font-size="{10 if mobile else 12}" font-weight="700">{total:,} PUBLIC CONTRIBUTIONS</text>')
    parts.append(f'<text class="meta" x="{230 if mobile else 270}" y="{footer_y}" fill="#91A4C5" font-size="{9 if mobile else 11}">{active} ACTIVE DAYS</text>')
    parts.append(f'<text class="meta" x="{390 if mobile else 430}" y="{footer_y}" fill="#91A4C5" font-size="{9 if mobile else 11}">{streak}D LONGEST STREAK</text>')
    fetched = escape(str(payload.get("fetched_at", "unknown"))[:10])
    parts.append(f'<text class="meta" x="{34 if mobile else 42}" y="{footer_y + 25}" fill="#596B91" font-size="8">SOURCE: GITHUB PUBLIC CALENDAR · UPDATED {fetched}</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--desktop-output", type=Path, default=DESKTOP_OUTPUT)
    parser.add_argument("--mobile-output", type=Path, default=MOBILE_OUTPUT)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    args.desktop_output.parent.mkdir(parents=True, exist_ok=True)
    args.desktop_output.write_text(render(payload, mobile=False), encoding="utf-8", newline="\n")
    args.mobile_output.write_text(render(payload, mobile=True), encoding="utf-8", newline="\n")
    print(f"wrote {args.desktop_output}")
    print(f"wrote {args.mobile_output}")


if __name__ == "__main__":
    main()
