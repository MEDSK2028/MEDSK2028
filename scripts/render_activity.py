#!/usr/bin/env python3
"""Render a verified full-year GitHub calendar with a decorative Python snake."""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "contribution-snapshot-2026.json"
DESKTOP_OUTPUT = ROOT / "assets" / "activity.svg"
MOBILE_OUTPUT = ROOT / "assets" / "activity-mobile.svg"
PALETTE = ["#161B22", "#033A16", "#196C2E", "#2EA043", "#56D364"]


def sunday_before(day: date) -> date:
    return day - timedelta(days=(day.weekday() + 1) % 7)


def snake_route(grid_x: int, grid_y: int, cell: int, gap: int) -> str:
    """Build a rounded vertical serpentine loop through all 53 calendar columns."""
    pitch = cell + gap
    left = grid_x + cell / 2
    right = grid_x + 52 * pitch + cell / 2
    top = grid_y + cell / 2
    bottom = grid_y + 6 * pitch + cell / 2
    commands = [f"M{left:g} {top:g}"]
    for week in range(53):
        x = left + week * pitch
        target_y = bottom if week % 2 == 0 else top
        commands.append(f"V{target_y:g}")
        if week < 52:
            next_x = x + pitch
            turn_y = target_y + (pitch * .92 if week % 2 == 0 else -pitch * .92)
            commands.append(
                f"C{x:g} {turn_y:g} {next_x:g} {turn_y:g} {next_x:g} {target_y:g}"
            )
    commands.extend(
        [
            f"C{right + pitch:g} {bottom:g} {right + pitch:g} {top - pitch * 1.8:g} {right:g} {top - pitch * 1.8:g}",
            f"H{left - pitch:g}",
            f"C{left - pitch * 1.8:g} {top - pitch * 1.8:g} {left - pitch * 1.8:g} {top:g} {left:g} {top:g}",
            f"H{left:g}",
        ]
    )
    return " ".join(commands)


def python_snake(route: str, *, mobile: bool) -> list[str]:
    """Return a small, non-data snake that follows the contribution cells."""
    scale = .72 if mobile else 1.0
    return [
        f'<path id="snake-route" d="{route}" fill="none" stroke="none"/>',
        f'<g class="python-snake" transform="scale({scale:g})" aria-hidden="true" filter="url(#snakeGlow)">',
        '<path d="M-25 0C-20-7-15 7-10 0S0-7 5 0" fill="none" stroke="url(#python)" stroke-width="6" stroke-linecap="round"/>',
        '<path d="M4-5C11-5 14-2 14 3C14 8 10 10 5 10H1V4H6C8 4 8 2 6 2H2C-1 2-3 0-3-3C-3-5-1-7 2-7H7" fill="#00E5FF" stroke="#EAF4FF" stroke-opacity=".55" stroke-width=".8"/>',
        '<circle cx="8.5" cy="-1.5" r="1.15" fill="#050816"/>',
        '<animateMotion dur="30s" repeatCount="indefinite" rotate="auto" calcMode="paced">',
        '<mpath href="#snake-route"/>',
        '</animateMotion>',
        '</g>',
    ]


def render(payload: dict[str, object], *, mobile: bool) -> str:
    owner_snapshot = payload.get("source_type") == "owner_authenticated_snapshot"
    days: dict[date, dict[str, int | None]] = {}
    if owner_snapshot:
        start_sunday = date.fromisoformat(str(payload.get("calendar_start")))
        last_day = date.fromisoformat(str(payload.get("calendar_end")))
        if start_sunday.weekday() != 6 or last_day < start_sunday:
            raise ValueError("Snapshot calendar bounds are invalid")
        for week in range(53):
            for row in range(7):
                current = start_sunday + timedelta(weeks=week, days=row)
                if current <= last_day:
                    days[current] = {"level": 0, "count": None}
        raw_levels = payload.get("levels")
        if not isinstance(raw_levels, list):
            raise ValueError("Snapshot contribution levels are missing")
        for entry in raw_levels:
            if not isinstance(entry, list) or len(entry) != 3:
                raise ValueError("Snapshot contribution level entry is invalid")
            week, row, level = (int(value) for value in entry)
            current = start_sunday + timedelta(weeks=week, days=row)
            if not 0 <= week < 53 or not 0 <= row < 7 or not 1 <= level <= 4:
                raise ValueError("Snapshot contribution level is out of range")
            if current not in days:
                raise ValueError("Snapshot contribution level is outside the captured calendar")
            days[current] = {"level": level, "count": None}
        end_saturday = start_sunday + timedelta(weeks=52, days=6)
    else:
        raw_days = payload.get("days")
        if not isinstance(raw_days, list) or len(raw_days) < 300:
            raise ValueError("Contribution JSON must contain at least 300 days")
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

    width, height = ((1000, 390) if not mobile else (560, 430))
    grid_x, grid_y = ((92, 148) if not mobile else (66, 170))
    cell, gap = ((11, 4) if not mobile else (6, 2))
    total = int(stats.get("total", 0))
    active = int(stats.get("active_days", 0))
    streak = int(stats.get("longest_streak", 0))
    route = snake_route(grid_x, grid_y, cell, gap)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{username} public GitHub activity</title>',
        f'<desc id="desc">A 53-week GitHub contribution calendar from an {"owner-provided authenticated snapshot" if owner_snapshot else "anonymous public calendar"}, with a decorative Python snake moving vertically through the squares.</desc>',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#101A32"/><stop offset=".55" stop-color="#080D1B"/><stop offset="1" stop-color="#050816"/></linearGradient><linearGradient id="brand" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#9D4EDD"/><stop offset=".5" stop-color="#FF4ECD"/><stop offset="1" stop-color="#00E5FF"/></linearGradient><linearGradient id="python" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#9D4EDD"/><stop offset=".5" stop-color="#00E5FF"/><stop offset="1" stop-color="#00FFA3"/></linearGradient><filter id="snakeGlow" x="-80%" y="-160%" width="260%" height="420%"><feGaussianBlur stdDeviation="1.8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
        "<style>",
        "text{font-family:'Geist Mono','IBM Plex Mono','SFMono-Regular',Consolas,monospace}",
        ".day{opacity:0;animation:cell .68s cubic-bezier(.22,1,.36,1) forwards}",
        ".meta{opacity:0;animation:meta .8s cubic-bezier(.22,1,.36,1) .95s forwards}",
        ".scan{animation:scan 5.8s cubic-bezier(.22,1,.36,1) infinite}",
        ".python-snake{opacity:.92}",
        "@keyframes cell{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}",
        "@keyframes meta{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}",
        "@keyframes scan{0%{opacity:0;transform:translateX(-120px)}18%{opacity:.7}68%,100%{opacity:0;transform:translateX(1020px)}}",
        "@media (prefers-reduced-motion:reduce){.day,.meta,.scan{animation:none!important;opacity:1!important;transform:none!important}.python-snake{display:none!important}}",
        "</style>",
        f'<rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="30" fill="#030510" stroke="#19254A"/>',
        f'<rect x="11" y="11" width="{width - 22}" height="{height - 22}" rx="24" fill="url(#bg)" stroke="#26365F"/>',
        '<circle cx="36" cy="36" r="5" fill="#FF5F57"/><circle cx="54" cy="36" r="5" fill="#FEBC2E"/><circle cx="72" cy="36" r="5" fill="#00FFA3"/>',
        f'<text x="96" y="41" fill="#91A4C5" font-size="12" letter-spacing="1.2">github-signal / {"authenticated snapshot" if owner_snapshot else "public audit"} / full-year</text>',
        f'<line x1="24" y1="58" x2="{width - 24}" y2="58" stroke="#223259"/>',
        '<rect class="scan" x="24" y="59" width="135" height="1" fill="url(#brand)" opacity="0"/>',
        f'<text class="meta" x="{34 if mobile else 42}" y="{91 if mobile else 89}" fill="#EAF4FF" font-size="{12 if mobile else 15}" font-weight="700">{total:,} CONTRIBUTIONS IN THE LAST YEAR</text>',
        f'<text class="meta" x="{34 if mobile else 42}" y="{116 if mobile else 111}" fill="#91A4C5" font-size="9">{username} · {"OWNER-PROVIDED GITHUB SNAPSHOT" if owner_snapshot else "VERIFIED PUBLIC CALENDAR"} · VERTICAL PYTHON SNAKE</text>',
        f'<rect x="{width - (92 if mobile else 110)}" y="76" width="{62 if mobile else 72}" height="28" rx="9" fill="#14244A" stroke="#314C80"/>',
        f'<text class="meta" x="{width - (76 if mobile else 91)}" y="95" fill="#00E5FF" font-size="10" font-weight="700">{last_day.year}</text>',
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
            record = days.get(current)
            if owner_snapshot and record is None:
                continue
            if record is None:
                record = {"level": 0, "count": 0}
            x = grid_x + week * (cell + gap)
            y = grid_y + row * (cell + gap)
            delay = min(.03 + (week + row) * .017, 1.02)
            tooltip = (
                f'GitHub activity on {current.isoformat()}; exact daily count is private in the supplied snapshot'
                if record["count"] is None
                else f'{record["count"]} contributions on {current.isoformat()}'
            )
            parts.append(
                f'<rect class="day" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="{2 if mobile else 3}" '
                f'fill="{PALETTE[int(record["level"])]}" style="animation-delay:{delay:.3f}s">'
                f'<title>{tooltip}</title></rect>'
            )

    parts.extend(python_snake(route, mobile=mobile))

    footer_y = 302 if not mobile else 292
    parts.append(f'<text class="meta" x="{34 if mobile else 42}" y="{footer_y}" fill="#00E5FF" font-size="{10 if mobile else 12}" font-weight="700">{total:,} CONTRIBUTIONS</text>')
    parts.append(f'<text class="meta" x="{230 if mobile else 270}" y="{footer_y}" fill="#91A4C5" font-size="{9 if mobile else 11}">{active} ACTIVE DAYS</text>')
    parts.append(f'<text class="meta" x="{390 if mobile else 430}" y="{footer_y}" fill="#91A4C5" font-size="{9 if mobile else 11}">{streak}D LONGEST STREAK</text>')
    fetched = escape(str(payload.get("captured_at" if owner_snapshot else "fetched_at", "unknown"))[:10])
    source_y = 376 if not mobile else 392
    source_name = "AUTHENTICATED GITHUB SNAPSHOT · OWNER PROVIDED" if owner_snapshot else "GITHUB PUBLIC CALENDAR"
    parts.append(f'<text class="meta" x="{34 if mobile else 42}" y="{source_y}" fill="#596B91" font-size="8">SOURCE: {source_name} · {fetched}</text>')
    legend_x = 392 if mobile else 790
    legend_y = 348 if not mobile else 350
    parts.append(f'<text class="meta" x="{legend_x}" y="{legend_y}" fill="#7184A9" font-size="8">LESS</text>')
    for index, color in enumerate(PALETTE):
        parts.append(f'<rect class="meta" x="{legend_x + 34 + index * 15}" y="{legend_y - 9}" width="10" height="10" rx="2" fill="{color}"/>')
    parts.append(f'<text class="meta" x="{legend_x + 112}" y="{legend_y}" fill="#7184A9" font-size="8">MORE</text>')
    parts.append(f'<text class="meta" x="{34 if mobile else 42}" y="{legend_y}" fill="#65769E" font-size="8">VERTICAL PYTHON SNAKE IS DECORATIVE · SNAPSHOT LEVELS ARE UNCHANGED</text>')
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
