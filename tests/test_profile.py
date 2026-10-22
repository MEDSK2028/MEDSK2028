from __future__ import annotations

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_profile_assets import (  # noqa: E402
    engineering_footprint,
    hero,
    info_card,
    projects,
    stack_card,
)


class SvgTests(unittest.TestCase):
    def test_generators_return_valid_accessible_svg(self) -> None:
        generated = (
            hero(True),
            hero(False),
            info_card(),
            stack_card(),
            projects(True),
            projects(False),
            engineering_footprint(True),
            engineering_footprint(False),
        )
        for source in generated:
            root = ET.fromstring(source)
            tags = {element.tag.rsplit("}", 1)[-1] for element in root.iter()}
            self.assertIn("title", tags)
            self.assertIn("desc", tags)
            self.assertNotIn("script", tags)

    def test_footprint_is_evidence_based(self) -> None:
        source = engineering_footprint(True)
        for label in (
            "APEX FUNDED BOT",
            "OPTIQ VISION FORGE",
            "WATIQA",
            "MPLS NETWORK LAB",
        ):
            self.assertIn(label, source)
        self.assertNotIn("contributions", source.lower())


if __name__ == "__main__":
    unittest.main()
