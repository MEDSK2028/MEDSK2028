#!/usr/bin/env python3
"""Validate README references, SVG safety, activity data, and workflow guards."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = [
    "assets/hero.svg",
    "assets/hero-mobile.svg",
    "assets/projects.svg",
    "assets/projects-mobile.svg",
    "assets/terminal.svg",
    "assets/terminal-mobile.svg",
    "assets/skills.svg",
    "assets/skills-mobile.svg",
    "assets/system-status.svg",
    "assets/system-status-mobile.svg",
    "assets/activity.svg",
    "assets/activity-mobile.svg",
    "assets/footer.svg",
    "assets/footer-mobile.svg",
]
REQUIRED = [
    "README.md",
    "docs/maintenance.md",
    "data/contributions.json",
    "data/contribution-snapshot-2026.json",
    "scripts/generate_profile_assets.py",
    "scripts/fetch_contributions.py",
    "scripts/render_activity.py",
    ".github/workflows/update-activity.yml",
    *ASSETS,
]


def fail(message: str) -> None:
    raise ValueError(message)


def validate_required_files() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail("Missing required files: " + ", ".join(missing))


def validate_readme_links() -> None:
    source = (ROOT / "README.md").read_text(encoding="utf-8")
    html_refs = re.findall(r'(?:src|srcset|href)="(\./[^"#?]+)', source)
    markdown_refs = re.findall(r"\]\((\./[^)#?]+)", source)
    refs = sorted(set(html_refs + markdown_refs))
    if not refs:
        fail("README contains no local references")
    missing = [ref for ref in refs if not (ROOT / ref.removeprefix("./")).is_file()]
    if missing:
        fail("README has broken local references: " + ", ".join(missing))


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def validate_svg(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    lowered = source.lower()
    if "<script" in lowered or "javascript:" in lowered:
        fail(f"{path.name} contains executable script content")
    if re.search(r'(?:href|xlink:href)="https?://', source, flags=re.I):
        fail(f"{path.name} contains an external asset reference")
    root = ET.fromstring(source)
    if local_name(root.tag) != "svg" or not root.get("viewBox"):
        fail(f"{path.name} requires an SVG root and viewBox")
    names = {local_name(element.tag) for element in root.iter()}
    if "title" not in names or "desc" not in names:
        fail(f"{path.name} requires accessible title and desc elements")
    if "prefers-reduced-motion" not in source:
        fail(f"{path.name} requires a reduced-motion fallback")


def validate_activity() -> None:
    payload = json.loads((ROOT / "data/contributions.json").read_text(encoding="utf-8"))
    if payload.get("username") != "MEDSK2028":
        fail("Activity data belongs to the wrong account")
    days = payload.get("days")
    if not isinstance(days, list) or len(days) < 300:
        fail("Activity data is incomplete")
    if any(not 0 <= int(day["level"]) <= 4 or int(day["count"]) < 0 for day in days):
        fail("Activity data contains an invalid value")
    snapshot = json.loads((ROOT / "data/contribution-snapshot-2026.json").read_text(encoding="utf-8"))
    if snapshot.get("username") != "MEDSK2028" or snapshot.get("source_type") != "owner_authenticated_snapshot":
        fail("Contribution snapshot provenance is invalid")
    levels = snapshot.get("levels")
    stats = snapshot.get("stats")
    if not isinstance(levels, list) or not isinstance(stats, dict):
        fail("Contribution snapshot structure is invalid")
    if len(levels) != 42 or int(stats.get("total", 0)) != 487:
        fail("Contribution snapshot no longer matches the owner-provided 2026 calendar")
    if any(
        not isinstance(entry, list)
        or len(entry) != 3
        or not 0 <= int(entry[0]) < 53
        or not 0 <= int(entry[1]) < 7
        or not 1 <= int(entry[2]) <= 4
        for entry in levels
    ):
        fail("Contribution snapshot contains an invalid level entry")
    coordinates = {(int(entry[0]), int(entry[1])) for entry in levels}
    if len(coordinates) != len(levels):
        fail("Contribution snapshot contains duplicate calendar cells")
    start = date.fromisoformat(str(snapshot.get("calendar_start")))
    end = date.fromisoformat(str(snapshot.get("calendar_end")))
    active_dates = sorted(start + timedelta(weeks=week, days=row) for week, row in coordinates)
    if active_dates[-1] > end or int(stats.get("active_days", 0)) != len(active_dates):
        fail("Contribution snapshot active-day count is invalid")
    longest = run = 0
    previous: date | None = None
    for current in active_dates:
        run = run + 1 if previous and current == previous + timedelta(days=1) else 1
        longest = max(longest, run)
        previous = current
    if int(stats.get("longest_streak", 0)) != longest:
        fail("Contribution snapshot longest streak is invalid")
    for asset in ("assets/activity.svg", "assets/activity-mobile.svg"):
        source = (ROOT / asset).read_text(encoding="utf-8")
        if source.count('class="day"') != 368:
            fail(f"{asset} must contain the complete captured 53-week calendar")
        if 'class="python-snake"' not in source or 'repeatCount="indefinite"' not in source:
            fail(f"{asset} is missing the looping decorative Python snake")
        if "487 CONTRIBUTIONS IN THE LAST YEAR" not in source:
            fail(f"{asset} is not rendering the owner-provided contribution snapshot")


def validate_workflow() -> None:
    source = (ROOT / ".github/workflows/update-activity.yml").read_text(encoding="utf-8")
    required = [
        "schedule:",
        "workflow_dispatch:",
        "contents: write",
        "python scripts/fetch_contributions.py",
        "python scripts/render_activity.py",
        "python scripts/validate_profile.py",
    ]
    missing = [fragment for fragment in required if fragment not in source]
    if missing:
        fail("Workflow is missing: " + ", ".join(missing))
    action_refs = re.findall(r"uses:\s*([^\s#]+)", source)
    if not action_refs or any(not re.search(r"@[0-9a-f]{40}$", ref) for ref in action_refs):
        fail("Every workflow action must be pinned to a full commit SHA")
    if "secrets." in source:
        fail("The public activity workflow must not require repository secrets")


def main() -> None:
    try:
        validate_required_files()
        validate_readme_links()
        validate_activity()
        validate_workflow()
        for asset in ASSETS:
            validate_svg(ROOT / asset)
    except (ET.ParseError, KeyError, TypeError, ValueError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print(f"profile validation passed ({len(REQUIRED)} required files, {len(ASSETS)} SVGs)")


if __name__ == "__main__":
    main()
