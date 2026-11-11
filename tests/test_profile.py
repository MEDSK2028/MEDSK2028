from __future__ import annotations

import json
import sys
import unittest
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fetch_contributions import Day, calculate_stats, parse_contributions  # noqa: E402
from generate_profile_assets import footer, hero, projects, skills, system_status, terminal  # noqa: E402
from render_activity import render  # noqa: E402


class ContributionTests(unittest.TestCase):
    def test_parser_extracts_counts_from_a_full_calendar(self) -> None:
        start = date(2025, 1, 1)
        chunks = []
        for index in range(301):
            current = start + timedelta(days=index)
            count = 9 if index == 42 else 0
            level = 4 if count else 0
            label = f"{count} contributions" if count else "No contributions"
            chunks.append(
                f'<td id="day-{index}" data-date="{current.isoformat()}" data-level="{level}"></td>'
                f'<tool-tip for="day-{index}">{label} on {current.isoformat()}.</tool-tip>'
            )
        days = parse_contributions("".join(chunks))
        self.assertEqual(len(days), 301)
        self.assertEqual(days[42], Day(days[42].date, 4, 9))

    def test_stats_are_derived_from_real_counts(self) -> None:
        stats = calculate_stats(
            [Day("2026-01-01", 1, 1), Day("2026-01-02", 2, 2), Day("2026-01-04", 4, 7)]
        )
        self.assertEqual(stats["total"], 10)
        self.assertEqual(stats["active_days"], 3)
        self.assertEqual(stats["longest_streak"], 2)


class SvgTests(unittest.TestCase):
    def test_static_generators_are_valid_accessible_svg(self) -> None:
        generated = (
            hero(True), hero(False), projects(True), projects(False),
            terminal(True), terminal(False), skills(True), skills(False),
            system_status(True), system_status(False), footer(True), footer(False),
        )
        for source in generated:
            root = ET.fromstring(source)
            tags = {element.tag.rsplit("}", 1)[-1] for element in root.iter()}
            self.assertIn("title", tags)
            self.assertIn("desc", tags)
            self.assertNotIn("script", tags)
            self.assertIn("prefers-reduced-motion", source)

    def test_brand_and_project_evidence_are_present(self) -> None:
        hero_source = hero(True)
        project_source = projects(True)
        self.assertIn("AI-POWERED BUILDER", hero_source)
        self.assertIn("CYBERSECURITY MINDSET", hero_source)
        for label in ("OPTIQ VISION FORGE", "APEX FUNDED BOT", "WATIQA", "MPLS NETWORK LAB"):
            self.assertIn(label, project_source)

    def test_activity_renderer_outputs_53_week_grid(self) -> None:
        payload = json.loads((ROOT / "data/contributions.json").read_text(encoding="utf-8"))
        for mobile in (False, True):
            source = render(payload, mobile=mobile)
            ET.fromstring(source)
            self.assertEqual(source.count('class="day"'), 53 * 7)
            self.assertIn("PUBLIC CONTRIBUTIONS IN THE LAST YEAR", source)
            self.assertIn('class="python-snake"', source)
            self.assertIn('repeatCount="indefinite"', source)
            self.assertIn("CONTRIBUTION DATA IS UNCHANGED", source)

    def test_project_previews_keep_source_private(self) -> None:
        source = projects(True)
        self.assertEqual(source.count("EMAIL FOR DETAILS &gt;"), 4)
        self.assertIn("README PREVIEW · SOURCE PRIVATE", source)
        self.assertNotIn("github.com/", source)

    def test_radar_uses_explicit_centered_origin(self) -> None:
        desktop = system_status(True)
        mobile = system_status(False)
        self.assertIn("transform-origin:240px 286px", desktop)
        self.assertIn("transform-origin:280px 266px", mobile)
        self.assertIn("animation:radar 7.2s linear infinite", desktop)


if __name__ == "__main__":
    unittest.main()
