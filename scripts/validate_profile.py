#!/usr/bin/env python3
"""Validate README references and SVG accessibility and safety."""

from __future__ import annotations

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
    "assets/engineering-footprint.svg",
    "assets/engineering-footprint-mobile.svg",
]
REQUIRED = [
    "README.md",
    "scripts/generate_profile_assets.py",
    "docs/maintenance.md",
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


def main() -> None:
    try:
        validate_required_files()
        validate_readme_links()
        for asset in ASSETS:
            validate_svg(ROOT / asset)
    except (ET.ParseError, TypeError, ValueError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print(f"profile validation passed ({len(REQUIRED)} required files, {len(ASSETS)} SVGs)")


if __name__ == "__main__":
    main()
