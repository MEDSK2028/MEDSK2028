#!/usr/bin/env python3
"""Render contribution data as an animated, GitHub-compatible SVG."""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "contributions.json"
DEFAULT_OUTPUT = ROOT / "assets" / "contribution-graph.svg"
PALETTE = ["#10231c", "#0b5d3b", "#0e8f5a", "#22c77a", "#43f0a4"]


def sunday_before(day: date) -> date:
    return day - timedelta(days=(day.weekday() + 1) % 7)


def render(payload: dict[str, object]) -> str:
    raw_days = payload.get("days")
    if not isinstance(raw_days, list) or len(raw_days) < 300:
        raise ValueError("Contribution JSON must contain at least 300 days")

    days: dict[date, dict[str, object]] = {}
    for raw in raw_days:
        if not isinstance(raw, dict):
            continue
        parsed_date = date.fromisoformat(str(raw["date"]))
        level = int(raw["level"])
        count = int(raw["count"])
        if not 0 <= level <= 4 or count < 0:
            raise ValueError(f"Invalid contribution value for {parsed_date}")
        days[parsed_date] = {"level": level, "count": count}

    last_day = max(days)
    end_saturday = sunday_before(last_day) + timedelta(days=6)
    start_sunday = end_saturday - timedelta(weeks=52)
    username = escape(str(payload.get("username", "GitHub user")))
    stats = payload.get("stats") if isinstance(payload.get("stats"), dict) else {}

    width, height = 900, 268
    grid_x, grid_y = 72, 104
    cell, gap = 10, 3
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{username} GitHub contribution activity</title>',
        '<desc id="desc">A real 53-week GitHub contribution calendar generated from public profile data.</desc>',
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#091814"/><stop offset=".6" stop-color="#050b09"/><stop offset="1" stop-color="#061510"/></linearGradient>',
        "</defs>",
        "<style>",
        "text{font-family:'SFMono-Regular',Consolas,'Liberation Mono',monospace}",
        ".day{opacity:0;animation:cell .68s cubic-bezier(.22,1,.36,1) forwards}",
        ".meta{opacity:0;animation:meta .8s cubic-bezier(.22,1,.36,1) 1.05s forwards}",
        "@keyframes cell{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}",
        "@keyframes meta{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}",
        "@media (prefers-reduced-motion:reduce){.day,.meta{animation:none!important;opacity:1!important;transform:none!important}}",
        "</style>",
        f'<rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="28" fill="#030806" stroke="#0d2b22"/>',
        f'<rect x="11" y="11" width="{width - 22}" height="{height - 22}" rx="22" fill="url(#bg)" stroke="#174c3b"/>',
        '<circle cx="36" cy="36" r="5" fill="#ff6b6b"/><circle cx="54" cy="36" r="5" fill="#f5c76b"/><circle cx="72" cy="36" r="5" fill="#35f2a1"/>',
        '<text x="96" y="41" fill="#77998c" font-size="13" letter-spacing="1.2">contributions --live --53w</text>',
        '<line x1="24" y1="58" x2="876" y2="58" stroke="#103529"/>',
        f'<text class="meta" x="34" y="84" fill="#d7f7e9" font-size="13" font-weight="700">{username} / public activity</text>',
    ]

    month_labels: list[tuple[int, str]] = []
    last_month = -1
    for week in range(53):
        current = start_sunday + timedelta(weeks=week)
        marker = current + timedelta(days=3)
        if marker.month != last_month:
            month_labels.append((week, marker.strftime("%b").upper()))
            last_month = marker.month
    if len(month_labels) > 1 and month_labels[1][0] - month_labels[0][0] < 3:
        month_labels.pop(0)
    for week, label in month_labels:
        x = grid_x + week * (cell + gap)
        parts.append(f'<text x="{x}" y="97" fill="#77998c" font-size="9">{label}</text>')

    for label, row in (("MON", 1), ("WED", 3), ("FRI", 5)):
        y = grid_y + row * (cell + gap) + 8
        parts.append(f'<text x="34" y="{y}" fill="#58796d" font-size="8">{label}</text>')

    for week in range(53):
        for row in range(7):
            current = start_sunday + timedelta(weeks=week, days=row)
            record = days.get(current, {"level": 0, "count": 0})
            level = int(record["level"])
            x = grid_x + week * (cell + gap)
            y = grid_y + row * (cell + gap)
            delay = min(0.04 + (week + row) * 0.018, 1.08)
            parts.append(
                f'<rect class="day" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" '
                f'fill="{PALETTE[level]}" style="animation-delay:{delay:.3f}s">'
                f'<title>{record["count"]} contributions on {current.isoformat()}</title></rect>'
            )

    footer_y = 232
    total = int(stats.get("total", 0))
    active_days = int(stats.get("active_days", 0))
    longest = int(stats.get("longest_streak", 0))
    parts.extend(
        [
            f'<text class="meta" x="34" y="{footer_y}" fill="#35f2a1" font-size="12" font-weight="700">{total:,} CONTRIBUTIONS</text>',
            f'<text class="meta" x="212" y="{footer_y}" fill="#77998c" font-size="12">{active_days} ACTIVE DAYS</text>',
            f'<text class="meta" x="364" y="{footer_y}" fill="#77998c" font-size="12">{longest}D LONGEST STREAK</text>',
            f'<text class="meta" x="670" y="{footer_y}" fill="#77998c" font-size="10">LESS</text>',
        ]
    )
    for index, color in enumerate(PALETTE):
        parts.append(f'<rect class="meta" x="{710 + index * 16}" y="{footer_y - 10}" width="10" height="10" rx="2" fill="{color}"/>')
    parts.append(f'<text class="meta" x="796" y="{footer_y}" fill="#77998c" font-size="10">MORE</text>')
    fetched_at = escape(str(payload.get("fetched_at", "unknown"))[:10])
    parts.append(f'<text class="meta" x="34" y="253" fill="#426458" font-size="9">SOURCE: GITHUB PUBLIC CALENDAR · UPDATED {fetched_at}</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(payload), encoding="utf-8", newline="\n")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
