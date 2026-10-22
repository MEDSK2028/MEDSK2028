#!/usr/bin/env python3
"""Fetch a public GitHub contribution calendar without credentials."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "contributions.json"
USERNAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
COUNT_RE = re.compile(r"([0-9][0-9,]*) contributions?")


@dataclass
class Day:
    date: str
    level: int
    count: int = 0


class ContributionParser(HTMLParser):
    """Extract calendar cells and their associated tooltip counts."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.days_by_id: dict[str, Day] = {}
        self.tooltip_target: str | None = None
        self.tooltip_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        day_date = values.get("data-date")
        day_id = values.get("id")
        level = values.get("data-level")
        if day_date and day_id and level is not None:
            try:
                parsed_level = int(level)
                date.fromisoformat(day_date)
            except (TypeError, ValueError):
                return
            if 0 <= parsed_level <= 4:
                self.days_by_id[day_id] = Day(day_date, parsed_level)

        if tag == "tool-tip" and values.get("for") in self.days_by_id:
            self.tooltip_target = values["for"]
            self.tooltip_text = []

    def handle_data(self, data: str) -> None:
        if self.tooltip_target:
            self.tooltip_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "tool-tip" or not self.tooltip_target:
            return
        value = " ".join(self.tooltip_text)
        match = COUNT_RE.search(value)
        self.days_by_id[self.tooltip_target].count = (
            int(match.group(1).replace(",", "")) if match else 0
        )
        self.tooltip_target = None
        self.tooltip_text = []


def parse_contributions(html: str) -> list[Day]:
    parser = ContributionParser()
    parser.feed(html)
    days = sorted(parser.days_by_id.values(), key=lambda item: item.date)
    if len(days) < 300:
        raise ValueError(
            f"GitHub contribution response contained only {len(days)} calendar days; "
            "refusing to replace known-good data."
        )
    return days


def calculate_stats(days: list[Day]) -> dict[str, object]:
    parsed = [(date.fromisoformat(day.date), day.count) for day in days]
    active = {day for day, count in parsed if count > 0}
    longest = 0
    run = 0
    previous: date | None = None
    for day in sorted(active):
        run = run + 1 if previous and day == previous + timedelta(days=1) else 1
        longest = max(longest, run)
        previous = day

    by_count = sorted(days, key=lambda item: (item.count, item.date), reverse=True)
    best = by_count[0] if by_count else Day("", 0, 0)
    return {
        "total": sum(day.count for day in days),
        "active_days": len(active),
        "longest_streak": longest,
        "best_day": {"date": best.date, "count": best.count},
    }


def fetch(username: str, timeout: int = 20) -> str:
    if not USERNAME_RE.fullmatch(username):
        raise ValueError("Invalid GitHub username")
    request = Request(
        f"https://github.com/users/{username}/contributions",
        headers={
            "Accept": "text/html,application/xhtml+xml",
            "User-Agent": f"{username}-profile-contribution-generator/1.0",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed host
            if response.status != 200:
                raise RuntimeError(f"GitHub returned HTTP {response.status}")
            return response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Unable to fetch GitHub contributions: {exc}") from exc


def build_payload(username: str, html: str) -> dict[str, object]:
    days = parse_contributions(html)
    return {
        "username": username,
        "fetched_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "source": f"https://github.com/users/{username}/contributions",
        "stats": calculate_stats(days),
        "days": [day.__dict__ for day in days],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="MEDSK2028")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--input-html", type=Path, help="Parse a saved response for testing")
    args = parser.parse_args()

    html = (
        args.input_html.read_text(encoding="utf-8")
        if args.input_html
        else fetch(args.username)
    )
    payload = build_payload(args.username, html)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"wrote {args.output} ({len(payload['days'])} days, "
        f"{payload['stats']['total']} contributions)"
    )


if __name__ == "__main__":
    main()
