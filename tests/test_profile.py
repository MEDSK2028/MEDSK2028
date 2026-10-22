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
from generate_profile_assets import hero, info_card, projects, stack_card  # noqa: E402
from render_contributions import render  # noqa: E402


class ContributionParserTests(unittest.TestCase):
    def test_parser_extracts_full_calendar_and_tooltip_counts(self) -> None:
        start = date(2025, 1, 1)
        chunks = []
        for index in range(301):
            current = start + timedelta(days=index)
            count = 7 if index == 42 else 0
            level = 3 if count else 0
            label = f"{count} contributions" if count else "No contributions"
            chunks.append(
                f'<td id="day-{index}" data-date="{current.isoformat()}" '
                f'data-level="{level}"></td>'
                f'<tool-tip for="day-{index}">{label} on {current.isoformat()}.</tool-tip>'
            )
        days = parse_contributions("".join(chunks))
        self.assertEqual(len(days), 301)
        self.assertEqual(days[42].count, 7)
        self.assertEqual(days[42].level, 3)

    def test_stats_are_derived_from_counts(self) -> None:
        days = [
            Day("2026-01-01", 1, 1),
            Day("2026-01-02", 2, 2),
            Day("2026-01-03", 0, 0),
            Day("2026-01-04", 4, 9),
        ]
        stats = calculate_stats(days)
        self.assertEqual(stats["total"], 12)
        self.assertEqual(stats["active_days"], 3)
        self.assertEqual(stats["longest_streak"], 2)
        self.assertEqual(stats["best_day"], {"date": "2026-01-04", "count": 9})


class SvgTests(unittest.TestCase):
    def test_static_generators_return_valid_accessible_svg(self) -> None:
        for source in (hero(True), hero(False), info_card(), stack_card(), projects(True), projects(False)):
            root = ET.fromstring(source)
            tags = {element.tag.rsplit("}", 1)[-1] for element in root.iter()}
            self.assertIn("title", tags)
            self.assertIn("desc", tags)
            self.assertNotIn("script", tags)

    def test_contribution_renderer_outputs_53_week_grid(self) -> None:
        payload = json.loads((ROOT / "data/contributions.json").read_text(encoding="utf-8"))
        source = render(payload)
        ET.fromstring(source)
        self.assertEqual(source.count('class="day"'), 53 * 7)
        self.assertIn("MEDSK2028", source)


if __name__ == "__main__":
    unittest.main()
