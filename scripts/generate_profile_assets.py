#!/usr/bin/env python3
"""Generate the static animated SVG artwork used by the profile README."""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

BG = "#050b09"
PANEL = "#07110e"
PANEL_ALT = "#091814"
LINE = "#174c3b"
MUTED = "#77998c"
TEXT = "#d7f7e9"
EMERALD = "#35f2a1"
CYAN = "#43d9ff"
AMBER = "#f5c76b"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',monospace"


def svg_open(width: int, height: int, title: str, description: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f"<title id=\"title\">{escape(title)}</title>",
        f"<desc id=\"desc\">{escape(description)}</desc>",
        "<defs>",
        '<linearGradient id="shell" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0" stop-color="{PANEL_ALT}"/>',
        f'<stop offset="0.55" stop-color="{BG}"/>',
        '<stop offset="1" stop-color="#061510"/>',
        "</linearGradient>",
        '<radialGradient id="signal" cx="0.18" cy="0.1" r="0.85">',
        f'<stop offset="0" stop-color="{EMERALD}" stop-opacity=".13"/>',
        f'<stop offset=".48" stop-color="{CYAN}" stop-opacity=".025"/>',
        '<stop offset="1" stop-color="#000" stop-opacity="0"/>',
        "</radialGradient>",
        "</defs>",
        "<style>",
        f"text{{font-family:{MONO}}}",
        ".reveal{opacity:0;animation:reveal .82s cubic-bezier(.22,1,.36,1) forwards}",
        ".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.6s cubic-bezier(.22,1,.36,1) infinite}",
        ".scan{animation:scan 5.5s cubic-bezier(.22,1,.36,1) infinite}",
        ".flow{stroke-dasharray:7 10;animation:flow 4.8s cubic-bezier(.22,1,.36,1) infinite}",
        "@keyframes reveal{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}",
        "@keyframes pulse{0%,100%{opacity:.35;transform:scale(.88)}50%{opacity:1;transform:scale(1)}}",
        "@keyframes scan{0%{opacity:0;transform:translateX(-180px)}15%{opacity:.55}60%,100%{opacity:0;transform:translateX(980px)}}",
        "@keyframes flow{from{stroke-dashoffset:34}to{stroke-dashoffset:0}}",
        "@media (prefers-reduced-motion:reduce){.reveal,.pulse,.scan,.flow{animation:none!important;opacity:1!important;transform:none!important}}",
        "</style>",
    ]


def shell(parts: list[str], width: int, height: int, label: str) -> None:
    parts.extend(
        [
            f'<rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="28" fill="#030806" stroke="#0d2b22"/>',
            f'<rect x="11" y="11" width="{width - 22}" height="{height - 22}" rx="22" fill="url(#shell)" stroke="{LINE}"/>',
            f'<rect x="12" y="12" width="{width - 24}" height="{height - 24}" rx="21" fill="url(#signal)"/>',
            '<circle cx="36" cy="36" r="5" fill="#ff6b6b"/>',
            '<circle cx="54" cy="36" r="5" fill="#f5c76b"/>',
            f'<circle cx="72" cy="36" r="5" fill="{EMERALD}"/>',
            f'<text x="96" y="41" fill="{MUTED}" font-size="13" letter-spacing="1.2">{escape(label)}</text>',
            f'<line x1="24" y1="58" x2="{width - 24}" y2="58" stroke="#103529"/>',
            f'<rect class="scan" x="24" y="59" width="120" height="1" fill="{CYAN}" opacity="0"/>',
        ]
    )


def text(
    x: int,
    y: int,
    value: str,
    *,
    size: int = 16,
    fill: str = TEXT,
    weight: int | None = None,
    spacing: float | None = None,
    css: str | None = None,
    delay: float | None = None,
) -> str:
    attrs = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"', f'font-size="{size}"']
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if spacing is not None:
        attrs.append(f'letter-spacing="{spacing}"')
    if css:
        attrs.append(f'class="{css}"')
    if delay is not None:
        attrs.append(f'style="animation-delay:{delay:.2f}s"')
    return f"<text {' '.join(attrs)}>{escape(value)}</text>"


def rect(
    x: int,
    y: int,
    width: int,
    height: int,
    *,
    fill: str = PANEL_ALT,
    stroke: str = LINE,
    radius: int = 16,
) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
        f'fill="{fill}" stroke="{stroke}"/>'
    )


MONOGRAM = [
    "##    ##   #######",
    "###  ###  ##      ",
    "## ## ##   ###### ",
    "##    ##        ##",
    "##    ##  ####### ",
]


def add_monogram(parts: list[str], x: int, y: int, *, font_size: int, step: int) -> None:
    for index, row in enumerate(MONOGRAM):
        parts.append(
            text(
                x,
                y + index * step,
                row,
                size=font_size,
                fill=EMERALD if index < 3 else CYAN,
                weight=700,
                spacing=1.4,
                css="reveal",
                delay=0.12 + index * 0.09,
            )
        )


def hero(desktop: bool) -> str:
    width, height = ((960, 390) if desktop else (560, 610))
    parts = svg_open(
        width,
        height,
        "Mohamed Sarkouh — AI engineer terminal introduction",
        "Animated terminal card with an ASCII MS monogram and an introduction to Mohamed's AI engineering work.",
    )
    shell(parts, width, height, "mohamed@github: ~/profile")
    if desktop:
        parts.append(rect(34, 78, 344, 278, fill="#06110d", stroke="#123c2f", radius=20))
        add_monogram(parts, 62, 142, font_size=20, step=31)
        parts.append(text(62, 325, "MS:// BUILDING INTELLIGENT SYSTEMS", size=12, fill=MUTED, spacing=0.7, css="reveal", delay=.75))
        divider_x = 408
        parts.append(f'<line x1="{divider_x}" y1="90" x2="{divider_x}" y2="340" stroke="#123c2f"/>')
        x = 444
        parts.append(text(x, 112, "> boot --profile mohamed.sarkouh", size=14, fill=CYAN, css="reveal", delay=.20))
        parts.append(text(x, 164, "MOHAMED SARKOUH", size=32, fill=TEXT, weight=700, spacing=1.2, css="reveal", delay=.46))
        parts.append(text(x, 200, "AI ENGINEER  /  CREATIVE DEVELOPER", size=15, fill=EMERALD, weight=700, spacing=.7, css="reveal", delay=.70))
        lines = [
            "agents · RAG · MCP · LLM applications",
            "Python · n8n · APIs · full-stack systems",
            "Linux · networking · secure infrastructure",
        ]
        for index, line in enumerate(lines):
            parts.append(text(x, 246 + index * 31, f"0{index + 1}  {line}", size=14, fill=MUTED, css="reveal", delay=.92 + index * .13))
        parts.append(f'<circle class="pulse" cx="446" cy="337" r="4" fill="{EMERALD}"/>')
        parts.append(text(460, 342, "SYSTEM STATUS: OPEN TO BUILD", size=12, fill=EMERALD, spacing=.8, css="reveal", delay=1.35))
    else:
        parts.append(rect(28, 78, 504, 228, fill="#06110d", stroke="#123c2f", radius=20))
        add_monogram(parts, 68, 130, font_size=20, step=30)
        parts.append(text(68, 283, "MS:// INTELLIGENT SYSTEMS", size=13, fill=MUTED, spacing=.8, css="reveal", delay=.75))
        x = 42
        parts.append(text(x, 352, "> boot mohamed.sarkouh", size=14, fill=CYAN, css="reveal", delay=.25))
        parts.append(text(x, 402, "MOHAMED SARKOUH", size=30, fill=TEXT, weight=700, spacing=.8, css="reveal", delay=.48))
        parts.append(text(x, 436, "AI ENGINEER / CREATIVE DEVELOPER", size=14, fill=EMERALD, weight=700, css="reveal", delay=.70))
        for index, line in enumerate(("agents · RAG · MCP · LLM apps", "Python · n8n · APIs · full-stack", "Linux · networking · infrastructure")):
            parts.append(text(x, 482 + index * 31, f"0{index + 1}  {line}", size=14, fill=MUTED, css="reveal", delay=.90 + index * .13))
        parts.append(f'<circle class="pulse" cx="44" cy="580" r="4" fill="{EMERALD}"/>')
        parts.append(text(58, 585, "SYSTEM STATUS: OPEN TO BUILD", size=12, fill=EMERALD, css="reveal", delay=1.34))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def info_card() -> str:
    width, height = 840, 390
    parts = svg_open(
        width,
        height,
        "Mohamed Sarkouh developer information card",
        "An animated information card listing Mohamed's professional focus across AI, automation, software, and infrastructure.",
    )
    shell(parts, width, height, "whoami --verbose")
    parts.append(text(40, 96, "IDENTITY", size=11, fill=CYAN, weight=700, spacing=1.8, css="reveal", delay=.1))
    parts.append(text(40, 133, "Mohamed Sarkouh", size=26, fill=TEXT, weight=700, css="reveal", delay=.2))
    parts.append(text(40, 161, "AI engineer · systems-minded builder", size=14, fill=MUTED, css="reveal", delay=.3))
    rows = [
        ("INTELLIGENCE", "LLM applications · AI agents · RAG systems · MCP integrations", EMERALD),
        ("AUTOMATION", "n8n workflows · API integrations · event-driven operations", CYAN),
        ("SOFTWARE", "Python · TypeScript · React · Node.js · Fastify", EMERALD),
        ("PLATFORM", "PostgreSQL · Redis · Docker · Linux · secure deployment", CYAN),
        ("FOUNDATION", "Networking · infrastructure · cybersecurity", AMBER),
    ]
    for index, (key, value, color) in enumerate(rows):
        y = 218 + index * 31
        parts.append(text(40, y, key, size=11, fill=color, weight=700, spacing=1.0, css="reveal", delay=.42 + index * .11))
        parts.append(text(174, y, value, size=13, fill=TEXT, css="reveal", delay=.48 + index * .11))
    parts.append(rect(638, 84, 164, 86, fill="#061510", stroke="#1a5e47", radius=18))
    parts.append(text(660, 112, "OPERATING MODE", size=10, fill=MUTED, spacing=1.2, css="reveal", delay=.3))
    parts.append(text(660, 141, "SHIP / LEARN", size=16, fill=EMERALD, weight=700, css="reveal", delay=.46))
    parts.append(f'<circle class="pulse" cx="779" cy="136" r="5" fill="{EMERALD}"/>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def stack_card() -> str:
    width, height = 840, 430
    parts = svg_open(
        width,
        height,
        "Mohamed Sarkouh technology stack",
        "Animated capability matrix for AI engineering, full-stack development, automation, and infrastructure.",
    )
    shell(parts, width, height, "stack --capability-matrix")
    columns = [
        (42, "01 / INTELLIGENCE", EMERALD, ["LLM APPLICATIONS", "AI AGENTS", "RAG SYSTEMS", "MCP INTEGRATIONS"]),
        (304, "02 / BUILD", CYAN, ["PYTHON", "TYPESCRIPT", "REACT + NODE", "FASTIFY + APIs"]),
        (566, "03 / SYSTEMS", AMBER, ["N8N AUTOMATION", "POSTGRES + REDIS", "DOCKER + LINUX", "NETWORK + SECURITY"]),
    ]
    for column_index, (x, heading, color, items) in enumerate(columns):
        parts.append(rect(x, 84, 232, 306, fill="#06110e", stroke="#123c2f", radius=20))
        parts.append(text(x + 20, 119, heading, size=11, fill=color, weight=700, spacing=1.1, css="reveal", delay=.14 + column_index * .12))
        parts.append(f'<line x1="{x + 20}" y1="136" x2="{x + 212}" y2="136" stroke="#123c2f"/>')
        for item_index, item in enumerate(items):
            y = 180 + item_index * 51
            delay = .32 + column_index * .10 + item_index * .09
            parts.append(f'<circle class="pulse" cx="{x + 28}" cy="{y - 5}" r="3.5" fill="{color}" style="animation-delay:{delay:.2f}s"/>')
            parts.append(text(x + 43, y, item, size=13, fill=TEXT, weight=700, spacing=.3, css="reveal", delay=delay))
            parts.append(text(x + 43, y + 18, "ready", size=10, fill=MUTED, css="reveal", delay=delay + .05))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


PROJECTS = [
    {
        "index": "01",
        "name": "WATIQA",
        "type": "SECURE VERIFICATION INFRASTRUCTURE",
        "summary": "Audited identification-record verification with bulk jobs,",
        "summary2": "role controls, passkeys, malware scanning, and private networking.",
        "stack": "FASTIFY · POSTGRESQL · REDIS/BULLMQ · PRISMA · WEBAUTHN",
        "color": EMERALD,
    },
    {
        "index": "02",
        "name": "APEX FUNDED BOT",
        "type": "VISION-TO-JOURNAL AI WORKFLOW",
        "summary": "Telegram workflow that interprets chart screenshots, confirms",
        "summary2": "trade context, and synchronizes Notion and Sheets analytics.",
        "stack": "PYTHON · TELEGRAM · VISION MODELS · NOTION · GOOGLE SHEETS",
        "color": CYAN,
    },
    {
        "index": "03",
        "name": "OPTIQ VISION FORGE",
        "type": "COMPUTER-VISION COMMERCE",
        "summary": "Full-stack optical storefront with face-mesh experiences, 3D,",
        "summary2": "admin workflows, persistent data, and production media storage.",
        "stack": "REACT · MEDIAPIPE · THREE.JS · EXPRESS · POSTGRESQL",
        "color": EMERALD,
    },
    {
        "index": "04",
        "name": "MPLS NETWORK LAB",
        "type": "NETWORK INFRASTRUCTURE PROJECT",
        "summary": "Hands-on networking project focused on MPLS, dynamic routing,",
        "summary2": "Linux-based infrastructure, and secure network operations.",
        "stack": "MPLS · OSPF · BGP · LINUX · NETWORK SECURITY",
        "color": AMBER,
    },
]


FOOTPRINT_DOMAINS = [
    {
        "index": "01",
        "title": "AI / AGENTS",
        "evidence": "APEX FUNDED BOT",
        "stack": "PYTHON · VISION MODELS · TELEGRAM · N8N",
        "color": CYAN,
    },
    {
        "index": "02",
        "title": "APPLICATION SYSTEMS",
        "evidence": "OPTIQ VISION FORGE",
        "stack": "REACT · TYPESCRIPT · NODE.JS · EXPRESS",
        "color": EMERALD,
    },
    {
        "index": "03",
        "title": "DATA / RELIABILITY",
        "evidence": "WATIQA",
        "stack": "POSTGRESQL · REDIS · PRISMA · QUEUES",
        "color": EMERALD,
    },
    {
        "index": "04",
        "title": "NETWORK / SECURITY",
        "evidence": "MPLS NETWORK LAB",
        "stack": "MPLS · OSPF · BGP · LINUX · WEBAUTHN",
        "color": AMBER,
    },
]


def footprint_domain(
    parts: list[str], domain: dict[str, str], x: int, y: int, width: int, delay: float
) -> None:
    parts.append(rect(x, y, width, 132, fill="#06110e", stroke="#123c2f", radius=20))
    parts.append(text(x + 20, y + 31, domain["index"], size=10, fill=domain["color"], weight=700, spacing=1.1, css="reveal", delay=delay))
    parts.append(text(x + 54, y + 33, domain["title"], size=16, fill=TEXT, weight=700, spacing=.25, css="reveal", delay=delay + .05))
    parts.append(text(x + 20, y + 67, f'EVIDENCE / {domain["evidence"]}', size=9, fill=domain["color"], weight=700, spacing=.65, css="reveal", delay=delay + .10))
    parts.append(f'<line x1="{x + 20}" y1="{y + 83}" x2="{x + width - 20}" y2="{y + 83}" stroke="#123c2f"/>')
    parts.append(text(x + 20, y + 110, domain["stack"], size=9, fill=MUTED, weight=700, spacing=.15, css="reveal", delay=delay + .16))
    parts.append(f'<circle class="pulse" cx="{x + width - 24}" cy="{y + 26}" r="4" fill="{domain["color"]}"/>')


def engineering_footprint(desktop: bool) -> str:
    width, height = ((960, 540) if desktop else (560, 820))
    parts = svg_open(
        width,
        height,
        "Mohamed Sarkouh engineering footprint",
        "A verified map connecting AI agents, application systems, data reliability, and network security to selected projects.",
    )
    shell(parts, width, height, "engineering-footprint --verified")
    if desktop:
        paths = [
            "M365 245 C345 230 350 175 340 154",
            "M595 245 C615 230 610 175 620 154",
            "M365 305 C345 320 350 405 340 426",
            "M595 305 C615 320 610 405 620 426",
        ]
        for index, path in enumerate(paths):
            color = FOOTPRINT_DOMAINS[index]["color"]
            parts.append(f'<path class="flow" d="{path}" fill="none" stroke="{color}" stroke-opacity=".65" stroke-width="1.5"/>')
        parts.append(rect(365, 210, 230, 130, fill="#071813", stroke="#1a5e47", radius=24))
        parts.append(text(395, 246, "MOHAMED SARKOUH", size=11, fill=CYAN, weight=700, spacing=1.2, css="reveal", delay=.12))
        parts.append(text(395, 278, "SYSTEMS BUILDER", size=21, fill=TEXT, weight=700, spacing=.4, css="reveal", delay=.22))
        parts.append(text(395, 307, "4 PROJECTS / 4 DOMAINS", size=10, fill=EMERALD, weight=700, spacing=.7, css="reveal", delay=.32))
        parts.append(f'<circle class="pulse" cx="566" cy="242" r="5" fill="{EMERALD}"/>')
        positions = [(40, 86), (620, 86), (40, 362), (620, 362)]
        for index, (domain, (x, y)) in enumerate(zip(FOOTPRINT_DOMAINS, positions, strict=True)):
            footprint_domain(parts, domain, x, y, 300, .18 + index * .12)
    else:
        parts.append(f'<line class="flow" x1="52" y1="176" x2="52" y2="742" stroke="{EMERALD}" stroke-opacity=".55" stroke-width="1.5"/>')
        parts.append(rect(28, 78, 504, 112, fill="#071813", stroke="#1a5e47", radius=22))
        parts.append(text(52, 111, "MOHAMED SARKOUH", size=10, fill=CYAN, weight=700, spacing=1.1, css="reveal", delay=.10))
        parts.append(text(52, 143, "ENGINEERING FOOTPRINT", size=22, fill=TEXT, weight=700, spacing=.25, css="reveal", delay=.20))
        parts.append(text(52, 169, "4 PROJECTS / 4 VERIFIED DOMAINS", size=10, fill=EMERALD, weight=700, spacing=.55, css="reveal", delay=.30))
        for index, domain in enumerate(FOOTPRINT_DOMAINS):
            footprint_domain(parts, domain, 28, 210 + index * 145, 504, .18 + index * .12)
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def project_card(parts: list[str], project: dict[str, str], x: int, y: int, width: int, delay: float) -> None:
    parts.append(rect(x, y, width, 198, fill="#06110e", stroke="#123c2f", radius=20))
    parts.append(text(x + 22, y + 34, project["index"], size=11, fill=project["color"], weight=700, spacing=1.2, css="reveal", delay=delay))
    parts.append(text(x + 58, y + 36, project["name"], size=19, fill=TEXT, weight=700, spacing=.3, css="reveal", delay=delay + .06))
    parts.append(text(x + 22, y + 67, project["type"], size=10, fill=project["color"], weight=700, spacing=.8, css="reveal", delay=delay + .12))
    parts.append(text(x + 22, y + 103, project["summary"], size=12, fill=MUTED, css="reveal", delay=delay + .18))
    parts.append(text(x + 22, y + 124, project["summary2"], size=12, fill=MUTED, css="reveal", delay=delay + .18))
    parts.append(f'<line x1="{x + 22}" y1="{y + 148}" x2="{x + width - 22}" y2="{y + 148}" stroke="#123c2f"/>')
    parts.append(text(x + 22, y + 178, project["stack"], size=10, fill=TEXT, weight=700, spacing=.15, css="reveal", delay=delay + .24))
    parts.append(f'<circle class="pulse" cx="{x + width - 28}" cy="{y + 28}" r="4" fill="{project["color"]}"/>')


def projects(desktop: bool) -> str:
    width, height = ((960, 530) if desktop else (560, 930))
    parts = svg_open(
        width,
        height,
        "Selected projects by Mohamed Sarkouh",
        "Four selected projects: WATIQA, Apex Funded Bot, OPTIQ Vision Forge, and MPLS Network Lab.",
    )
    shell(parts, width, height, "projects --selected --private-safe")
    if desktop:
        positions = [(28, 82), (494, 82), (28, 294), (494, 294)]
        for index, (project, (x, y)) in enumerate(zip(PROJECTS, positions, strict=True)):
            project_card(parts, project, x, y, 438, .14 + index * .12)
    else:
        for index, project in enumerate(PROJECTS):
            project_card(parts, project, 28, 78 + index * 210, 504, .14 + index * .12)
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def write_assets() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    generated = {
        "hero.svg": hero(desktop=True),
        "hero-mobile.svg": hero(desktop=False),
        "info-card.svg": info_card(),
        "stack.svg": stack_card(),
        "projects.svg": projects(desktop=True),
        "projects-mobile.svg": projects(desktop=False),
        "engineering-footprint.svg": engineering_footprint(desktop=True),
        "engineering-footprint-mobile.svg": engineering_footprint(desktop=False),
    }
    for filename, content in generated.items():
        (ASSETS / filename).write_text(content, encoding="utf-8", newline="\n")
        print(f"wrote assets/{filename}")


if __name__ == "__main__":
    write_assets()
