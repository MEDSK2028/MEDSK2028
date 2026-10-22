#!/usr/bin/env python3
"""Validate README references, SVG safety, contribution data, and workflow guards."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = [
    "assets/hero.svg",
    "assets/hero-mobile.svg",
    "assets/info-card.svg",
    "assets/stack.svg",
    "assets/projects.svg",
    "assets/projects-mobile.svg",
    "assets/contribution-graph.svg",
]
REQUIRED = [
    "README.md",
    "data/contributions.json",
    "scripts/generate_profile_assets.py",
    "scripts/fetch_contributions.py",
    "scripts/render_contributions.py",
    ".github/workflows/update-contributions.yml",
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
        fail("README contains no local asset references")
    missing = [ref for ref in refs if not (ROOT / ref.removeprefix("./")).is_file()]
    if missing:
        fail("README has broken local references: " + ", ".join(missing))


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def validate_svg(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    if "<script" in source.lower():
        fail(f"{path.name} contains a script element")
    if re.search(r'(?:href|xlink:href)="https?://', source, flags=re.I):
        fail(f"{path.name} contains an external asset reference")
    root = ET.fromstring(source)
    if local_name(root.tag) != "svg":
        fail(f"{path.name} does not have an SVG root")
    if not root.get("viewBox"):
        fail(f"{path.name} is missing a viewBox")
    names = {local_name(element.tag) for element in root.iter()}
    if "title" not in names or "desc" not in names:
        fail(f"{path.name} requires accessible title and desc elements")


def validate_contributions() -> None:
    payload = json.loads((ROOT / "data/contributions.json").read_text(encoding="utf-8"))
    if payload.get("username") != "MEDSK2028":
        fail("Contribution data belongs to the wrong account")
    days = payload.get("days")
    if not isinstance(days, list) or len(days) < 300:
        fail("Contribution data is incomplete")
    if any(not 0 <= int(day["level"]) <= 4 or int(day["count"]) < 0 for day in days):
        fail("Contribution data contains an invalid level or count")


def validate_workflow() -> None:
    path = ROOT / ".github/workflows/update-contributions.yml"
    source = path.read_text(encoding="utf-8")
    required_fragments = [
        "schedule:",
        "workflow_dispatch:",
        "contents: write",
        "python scripts/fetch_contributions.py",
        "python scripts/render_contributions.py",
        "python scripts/validate_profile.py",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in source]
    if missing:
        fail("Workflow is missing: " + ", ".join(missing))
    action_refs = re.findall(r"uses:\s*([^\s#]+)", source)
    if not action_refs or any(not re.search(r"@[0-9a-f]{40}$", ref) for ref in action_refs):
        fail("Every workflow action must be pinned to a full commit SHA")
    if "secrets." in source:
        fail("Contribution workflow must not require repository secrets")


def main() -> None:
    checks = [
        validate_required_files,
        validate_readme_links,
        validate_contributions,
        validate_workflow,
    ]
    try:
        for check in checks:
            check()
        for asset in ASSETS:
            validate_svg(ROOT / asset)
    except (ET.ParseError, KeyError, TypeError, ValueError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print(f"profile validation passed ({len(REQUIRED)} required files, {len(ASSETS)} SVGs)")


if __name__ == "__main__":
    main()
