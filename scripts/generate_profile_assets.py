#!/usr/bin/env python3
"""Generate the premium animated SVG artwork used by the profile README."""

from __future__ import annotations

from html import escape
from math import cos, pi, sin
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

BG = "#080D1B"
DEEP = "#050816"
PANEL = "#0D1428"
PANEL_2 = "#101A32"
LINE = "#26365F"
VIOLET = "#9D4EDD"
CYAN = "#00E5FF"
MINT = "#00FFA3"
MAGENTA = "#FF4ECD"
TEXT = "#EAF4FF"
MUTED = "#91A4C5"
MONO = "'Geist Mono','IBM Plex Mono','SFMono-Regular',Consolas,monospace"
DISPLAY = "'Space Grotesk','Aptos Display','Segoe UI',sans-serif"


def svg_open(width: int, height: int, title: str, description: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{escape(description)}</desc>',
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0" stop-color="{PANEL_2}"/>',
        f'<stop offset=".52" stop-color="{BG}"/>',
        f'<stop offset="1" stop-color="{DEEP}"/>',
        "</linearGradient>",
        '<linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0" stop-color="{VIOLET}"/>',
        f'<stop offset=".5" stop-color="{MAGENTA}"/>',
        f'<stop offset="1" stop-color="{CYAN}"/>',
        "</linearGradient>",
        '<linearGradient id="neural" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0" stop-color="{MAGENTA}"/>',
        f'<stop offset=".5" stop-color="{VIOLET}"/>',
        f'<stop offset="1" stop-color="{CYAN}"/>',
        "</linearGradient>",
        '<radialGradient id="aura" cx=".78" cy=".18" r=".82">',
        f'<stop offset="0" stop-color="{VIOLET}" stop-opacity=".22"/>',
        f'<stop offset=".42" stop-color="{CYAN}" stop-opacity=".06"/>',
        f'<stop offset="1" stop-color="{BG}" stop-opacity="0"/>',
        "</radialGradient>",
        '<filter id="glow" x="-80%" y="-80%" width="260%" height="260%">',
        '<feGaussianBlur stdDeviation="3" result="blur"/>',
        '<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
        "</filter>",
        "</defs>",
        "<style>",
        f"text{{font-family:{MONO}}}",
        f".display{{font-family:{DISPLAY}}}",
        ".reveal{opacity:0;animation:reveal .82s cubic-bezier(.22,1,.36,1) forwards}",
        ".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.8s cubic-bezier(.22,1,.36,1) infinite}",
        ".blink{animation:blink 1.15s cubic-bezier(.22,1,.36,1) infinite}",
        ".scan{animation:scan 6.2s cubic-bezier(.22,1,.36,1) infinite}",
        ".flow{stroke-dasharray:7 11;animation:flow 5s cubic-bezier(.22,1,.36,1) infinite}",
        ".orbit-line{stroke-dasharray:8 13;animation:orbitFlow 10s linear infinite}",
        ".orbit-line.reverse{animation-direction:reverse;animation-duration:13s}",
        ".radar{transform-box:view-box;animation:radar 7.2s linear infinite}",
        ".role{opacity:0;animation:role 15s cubic-bezier(.22,1,.36,1) infinite}",
        ".r1{animation-delay:3s}.r2{animation-delay:6s}.r3{animation-delay:9s}.r4{animation-delay:12s}",
        "@keyframes reveal{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}",
        "@keyframes pulse{0%,100%{opacity:.35;transform:scale(.88)}50%{opacity:1;transform:scale(1.08)}}",
        "@keyframes blink{0%,42%{opacity:1}58%,100%{opacity:.08}}",
        "@keyframes scan{0%{opacity:0;transform:translateX(-160px)}14%{opacity:.7}62%,100%{opacity:0;transform:translateX(1050px)}}",
        "@keyframes flow{from{stroke-dashoffset:36}to{stroke-dashoffset:0}}",
        "@keyframes orbitFlow{from{stroke-dashoffset:84}to{stroke-dashoffset:0}}",
        "@keyframes radar{from{transform:rotate(0)}to{transform:rotate(360deg)}}",
        "@keyframes role{0%,14%{opacity:1;transform:translateY(0)}18%,92%{opacity:0;transform:translateY(-8px)}96%{opacity:0;transform:translateY(8px)}100%{opacity:1;transform:translateY(0)}}",
        "@media (prefers-reduced-motion:reduce){.reveal,.pulse,.blink,.scan,.flow,.orbit-line,.radar,.role{animation:none!important;opacity:1!important;transform:none!important}.r1,.r2,.r3,.r4{display:none!important}}",
        "</style>",
    ]


def shell(parts: list[str], width: int, height: int, label: str) -> None:
    parts.extend(
        [
            f'<rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="30" fill="#030510" stroke="#19254A"/>',
            f'<rect x="11" y="11" width="{width - 22}" height="{height - 22}" rx="24" fill="url(#bg)" stroke="{LINE}"/>',
            f'<rect x="12" y="12" width="{width - 24}" height="{height - 24}" rx="23" fill="url(#aura)"/>',
            '<circle cx="36" cy="36" r="5" fill="#FF5F57"/>',
            '<circle cx="54" cy="36" r="5" fill="#FEBC2E"/>',
            f'<circle cx="72" cy="36" r="5" fill="{MINT}"/>',
            f'<text x="96" y="41" fill="{MUTED}" font-size="12" letter-spacing="1.35">{escape(label)}</text>',
            f'<line x1="24" y1="58" x2="{width - 24}" y2="58" stroke="#223259"/>',
            f'<rect class="scan" x="24" y="59" width="150" height="1" fill="url(#brand)" opacity="0"/>',
        ]
    )


def text(
    x: float,
    y: float,
    value: str,
    *,
    size: int = 16,
    fill: str = TEXT,
    weight: int | None = None,
    spacing: float | None = None,
    css: str | None = None,
    delay: float | None = None,
) -> str:
    attrs = [f'x="{x:g}"', f'y="{y:g}"', f'fill="{fill}"', f'font-size="{size}"']
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
    fill: str = PANEL,
    stroke: str = LINE,
    radius: int = 18,
) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
        f'fill="{fill}" stroke="{stroke}"/>'
    )


NEURAL_NODES = [
    (32, 126), (63, 78), (96, 110), (124, 48), (154, 90), (186, 42),
    (214, 110), (246, 68), (276, 122), (306, 82), (340, 142), (296, 190),
    (254, 226), (204, 186), (172, 246), (126, 202), (82, 238), (48, 184),
]
NEURAL_EDGES = [
    (0, 1), (0, 17), (1, 2), (1, 3), (2, 4), (2, 15), (3, 4), (3, 5),
    (4, 6), (4, 13), (5, 6), (5, 7), (6, 7), (6, 8), (6, 13), (7, 9),
    (8, 9), (8, 10), (8, 11), (8, 13), (10, 11), (11, 12), (12, 13),
    (12, 14), (13, 14), (13, 15), (14, 16), (15, 16), (15, 17), (16, 17),
]


def neural_network(parts: list[str], x: int, y: int, scale: float = 1.0) -> None:
    parts.extend(
        [
            '<defs><clipPath id="sphereClip"><ellipse cx="184" cy="140" rx="158" ry="116"/></clipPath>',
            '<radialGradient id="sphereFace" cx="42%" cy="35%" r="72%"><stop offset="0" stop-color="#1A2851"/><stop offset=".52" stop-color="#0B132B"/><stop offset="1" stop-color="#050816"/></radialGradient></defs>',
        ]
    )
    parts.append(f'<g transform="translate({x} {y}) scale({scale})">')
    parts.append('<ellipse cx="184" cy="140" rx="158" ry="116" fill="url(#sphereFace)" stroke="#47598F" stroke-opacity=".9"/>')
    parts.append('<ellipse cx="184" cy="140" rx="158" ry="42" fill="none" stroke="#344C7D" stroke-opacity=".62"/>')
    parts.append('<ellipse cx="184" cy="140" rx="158" ry="82" fill="none" stroke="#263D6B" stroke-opacity=".58"/>')
    parts.append('<ellipse cx="184" cy="140" rx="58" ry="116" fill="none" stroke="#344C7D" stroke-opacity=".56"/>')
    parts.append('<ellipse cx="184" cy="140" rx="112" ry="116" fill="none" stroke="#263D6B" stroke-opacity=".5"/>')
    parts.append('<g transform="rotate(21 184 140)"><ellipse class="orbit-line" cx="184" cy="140" rx="176" ry="104" fill="none" stroke="#9D4EDD" stroke-opacity=".52" stroke-width="1.2"/></g>')
    parts.append('<g transform="rotate(-23 184 140)"><ellipse class="orbit-line reverse" cx="184" cy="140" rx="170" ry="92" fill="none" stroke="#00E5FF" stroke-opacity=".44" stroke-width="1.1"/></g>')
    parts.append('<g clip-path="url(#sphereClip)">')
    for index, (start, end) in enumerate(NEURAL_EDGES):
        x1, y1 = NEURAL_NODES[start]
        x2, y2 = NEURAL_NODES[end]
        bend = 18 if index % 2 else -18
        midx = (x1 + x2) / 2
        midy = (y1 + y2) / 2 + bend
        parts.append(
            f'<path class="flow" d="M{x1} {y1} Q{midx:g} {midy:g} {x2} {y2}" '
            'fill="none" stroke="url(#neural)" stroke-opacity=".55" stroke-width="1.25"/>'
        )
    for index, (node_x, node_y) in enumerate(NEURAL_NODES):
        color = (CYAN, VIOLET, MAGENTA, MINT)[index % 4]
        radius = 4.6 if index % 5 == 0 else 3.2
        parts.append(
            f'<circle class="pulse" cx="{node_x}" cy="{node_y}" r="{radius}" fill="{color}" '
            f'filter="url(#glow)" style="animation-delay:{index * .08:.2f}s"/>'
        )
    parts.append("</g>")
    parts.append('<circle cx="184" cy="140" r="31" fill="none" stroke="#00E5FF" stroke-opacity=".16"/>')
    parts.append(f'<circle cx="184" cy="140" r="18" fill="{BG}" stroke="{CYAN}" stroke-opacity=".75"/>')
    parts.append(f'<circle class="pulse" cx="184" cy="140" r="6" fill="{MINT}" filter="url(#glow)"/>')
    parts.append("</g>")


ROLES = [
    "AI-POWERED DEVELOPER",
    "VIBE CODING ENTHUSIAST",
    "AI AGENTS & AUTOMATION BUILDER",
    "CYBERSECURITY & NETWORK ENGINEER",
    "CREATIVE PROBLEM SOLVER",
]


def add_roles(parts: list[str], x: int, y: int, size: int) -> None:
    for index, role in enumerate(ROLES):
        css = "role" if index == 0 else f"role r{index}"
        parts.append(text(x, y, role, size=size, fill=CYAN, weight=700, spacing=.45, css=css))


def hero(desktop: bool) -> str:
    width, height = ((1000, 520) if desktop else (560, 780))
    parts = svg_open(
        width,
        height,
        "Mohamed Sarkouh — AI powered builder and cybersecurity minded developer",
        "Animated futuristic hero with Mohamed Sarkouh's name, rotating professional roles, and a neon neural network.",
    )
    shell(parts, width, height, "identity.sys / ai-cyber profile")
    if desktop:
        parts.append(text(52, 105, "AI × CYBERSECURITY / PROFILE 2026", size=11, fill=MINT, weight=700, spacing=1.8, css="reveal", delay=.10))
        parts.append('<text class="display reveal" x="52" y="177" fill="url(#brand)" font-size="48" font-weight="800" letter-spacing="-1" style="animation-delay:.22s">MOHAMED SARKOUH</text>')
        parts.append(text(55, 216, "AI-POWERED BUILDER. CREATIVE VIBE CODER.", size=15, fill=TEXT, weight=700, spacing=.55, css="reveal", delay=.38))
        parts.append(text(55, 242, "CYBERSECURITY MINDSET.", size=15, fill=MAGENTA, weight=700, spacing=.55, css="reveal", delay=.46))
        parts.append(rect(52, 274, 500, 62, fill="#0B1329", stroke="#354271", radius=16))
        parts.append(text(72, 299, "CURRENT ROLE /", size=9, fill=MUTED, weight=700, spacing=1.2, css="reveal", delay=.55))
        add_roles(parts, 72, 323, 14)
        parts.append(text(55, 382, "Turning ideas into intelligent, secure digital experiences.", size=14, fill=MUTED, css="reveal", delay=.72))
        parts.append(text(55, 432, "> build --creative --automate --secure", size=12, fill=VIOLET, css="reveal", delay=.90))
        parts.append(f'<rect class="blink" x="365" y="419" width="9" height="16" rx="2" fill="{CYAN}"/>')
        neural_network(parts, 602, 112, .98)
        parts.append(text(704, 451, "NEURAL BUILD GRAPH / LIVE MOTION", size=9, fill=MUTED, spacing=.8, css="reveal", delay=.85))
    else:
        parts.append(text(34, 100, "AI × CYBERSECURITY / PROFILE", size=10, fill=MINT, weight=700, spacing=1.35, css="reveal", delay=.10))
        parts.append('<text class="display reveal" x="34" y="156" fill="url(#brand)" font-size="35" font-weight="800" letter-spacing="-.6" style="animation-delay:.22s">MOHAMED SARKOUH</text>')
        parts.append(text(34, 194, "AI-POWERED BUILDER · VIBE CODER", size=13, fill=TEXT, weight=700, css="reveal", delay=.38))
        parts.append(text(34, 221, "CYBERSECURITY MINDSET", size=13, fill=MAGENTA, weight=700, css="reveal", delay=.46))
        parts.append(rect(28, 252, 504, 70, fill="#0B1329", stroke="#354271", radius=16))
        parts.append(text(48, 277, "CURRENT ROLE /", size=9, fill=MUTED, weight=700, spacing=1.1, css="reveal", delay=.55))
        add_roles(parts, 48, 304, 12)
        parts.append(text(34, 361, "Turning ideas into intelligent,", size=13, fill=MUTED, css="reveal", delay=.72))
        parts.append(text(34, 383, "secure digital experiences.", size=13, fill=MUTED, css="reveal", delay=.76))
        neural_network(parts, 98, 432, 1.0)
        parts.append(text(151, 733, "NEURAL BUILD GRAPH / LIVE MOTION", size=9, fill=MUTED, spacing=.55, css="reveal", delay=.85))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def terminal(desktop: bool) -> str:
    width, height = ((960, 470) if desktop else (560, 660))
    parts = svg_open(
        width,
        height,
        "Mohamed Sarkouh terminal introduction",
        "Animated Linux-style terminal showing Mohamed's identity, current focus, and mission, plus a decorative system status panel.",
    )
    shell(parts, width, height, "mohamed@lab:~ / zsh")
    commands = [
        ("whoami", ["AI Builder | Vibe Coder | Cybersecurity Mindset"]),
        ("current_focus", ["AI Agents · Intelligent Automation · Secure Applications"]),
        ("mission", ["Build smarter. Automate faster. Think securely."]),
    ]
    if desktop:
        x, y = 46, 105
        for index, (command, outputs) in enumerate(commands):
            parts.append(text(x, y, "$", size=15, fill=VIOLET, weight=700, css="reveal", delay=.12 + index * .24))
            parts.append(text(x + 22, y, command, size=14, fill=TEXT, weight=700, css="reveal", delay=.15 + index * .24))
            parts.append(text(x, y + 32, ">", size=14, fill=MINT, weight=700, css="reveal", delay=.22 + index * .24))
            parts.append(text(x + 22, y + 32, outputs[0], size=13, fill=MUTED, css="reveal", delay=.25 + index * .24))
            y += 92
        parts.append(f'<rect class="blink" x="47" y="382" width="9" height="17" rx="2" fill="{CYAN}"/>')
        parts.append(rect(674, 84, 244, 330, fill="#0A1227", stroke="#384575", radius=22))
        parts.append(text(698, 116, "DECORATIVE SYSTEM STATUS", size=9, fill=MAGENTA, weight=700, spacing=.75, css="reveal", delay=.2))
        status = [
            ("AI TOOLCHAIN", "ONLINE", CYAN),
            ("SECURITY MODE", "ACTIVE", MINT),
            ("NETWORK LAB", "READY", VIOLET),
            ("BUILD CHANNEL", "OPEN", MAGENTA),
        ]
        for index, (label, value, color) in enumerate(status):
            sy = 164 + index * 56
            parts.append(f'<circle class="pulse" cx="700" cy="{sy - 4}" r="4" fill="{color}"/>')
            parts.append(text(716, sy, label, size=10, fill=MUTED, spacing=.5, css="reveal", delay=.32 + index * .11))
            parts.append(text(872, sy, value, size=10, fill=color, weight=700, css="reveal", delay=.38 + index * .11))
        parts.append(text(698, 392, "visual indicator / not telemetry", size=8, fill="#63759B", css="reveal", delay=.85))
    else:
        x, y = 34, 104
        mobile_outputs = [
            ["AI Builder | Vibe Coder |", "Cybersecurity Mindset"],
            ["AI Agents · Intelligent Automation", "Secure Applications"],
            ["Build smarter. Automate faster.", "Think securely."],
        ]
        for index, ((command, _), outputs) in enumerate(zip(commands, mobile_outputs, strict=True)):
            parts.append(text(x, y, "$", size=14, fill=VIOLET, weight=700, css="reveal", delay=.12 + index * .24))
            parts.append(text(x + 22, y, command, size=13, fill=TEXT, weight=700, css="reveal", delay=.15 + index * .24))
            for line_index, output in enumerate(outputs):
                parts.append(text(x + (0 if line_index == 0 else 22), y + 30 + line_index * 22, ("> " if line_index == 0 else "") + output, size=12, fill=MINT if line_index == 0 else MUTED, css="reveal", delay=.22 + index * .24 + line_index * .04))
            y += 106
        parts.append(rect(28, 426, 504, 188, fill="#0A1227", stroke="#384575", radius=20))
        parts.append(text(50, 458, "DECORATIVE SYSTEM STATUS", size=9, fill=MAGENTA, weight=700, spacing=.7, css="reveal", delay=.5))
        status = [("AI TOOLCHAIN", "ONLINE", CYAN), ("SECURITY MODE", "ACTIVE", MINT), ("NETWORK LAB", "READY", VIOLET)]
        for index, (label, value, color) in enumerate(status):
            sy = 500 + index * 42
            parts.append(f'<circle class="pulse" cx="52" cy="{sy - 4}" r="4" fill="{color}"/>')
            parts.append(text(68, sy, label, size=10, fill=MUTED, css="reveal", delay=.62 + index * .10))
            parts.append(text(462, sy, value, size=10, fill=color, weight=700, css="reveal", delay=.67 + index * .10))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


SKILL_GROUPS = [
    ("01", "AI & AUTOMATION", CYAN, ["Python", "OpenAI API", "LLMs", "RAG", "MCP", "n8n", "LangChain", "LangGraph"]),
    ("02", "CYBERSECURITY", MAGENTA, ["Kali Linux", "Wazuh", "SIEM", "Wireshark", "Linux Security", "Network Security"]),
    ("03", "CREATIVE DEVELOPMENT", VIOLET, ["React", "Next.js", "JavaScript", "TypeScript", "Node.js", "REST APIs"]),
    ("04", "INFRASTRUCTURE", MINT, ["Docker", "Git", "GitHub Actions", "VMware", "GNS3", "Linux"]),
]


def skill_icon(parts: list[str], kind: str, x: int, y: int, color: str) -> None:
    parts.append(f'<g transform="translate({x} {y})" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" opacity=".9">')
    if kind == "01":
        parts.extend([
            '<circle cx="8" cy="15" r="3"/><circle cx="23" cy="7" r="3"/><circle cx="26" cy="23" r="3"/>',
            '<path d="M10.6 13.5L20.3 8.5M10.8 16.3L23.2 21.8M23.6 10L25.3 20"/>',
        ])
    elif kind == "02":
        parts.extend([
            '<path d="M16 3L28 8V15C28 22 23 27 16 30C9 27 4 22 4 15V8L16 3Z"/>',
            '<path d="M11 16L15 20L22 12"/>',
        ])
    elif kind == "03":
        parts.extend([
            '<path d="M11 8L3 16L11 24M21 8L29 16L21 24M18 5L14 27"/>',
        ])
    else:
        parts.extend([
            '<circle cx="16" cy="6" r="3"/><circle cx="6" cy="25" r="3"/><circle cx="26" cy="25" r="3"/>',
            '<path d="M14.5 8.7L7.5 22.3M17.5 8.7L24.5 22.3M9 25H23"/>',
        ])
    parts.append("</g>")


def skill_card(parts: list[str], group: tuple[str, str, str, list[str]], x: int, y: int, width: int, height: int, delay: float) -> None:
    index, title_value, color, items = group
    parts.append(rect(x, y, width, height, fill="#0A1227", stroke="#2D3B68", radius=22))
    parts.append(f'<rect x="{x + 1}" y="{y + 1}" width="4" height="{height - 2}" rx="2" fill="{color}" opacity=".85"/>')
    parts.append(text(x + 24, y + 35, index, size=9, fill=color, weight=700, spacing=1.2, css="reveal", delay=delay))
    parts.append(text(x + 60, y + 38, title_value, size=15, fill=TEXT, weight=700, spacing=.35, css="reveal", delay=delay + .05))
    skill_icon(parts, index, x + width - 60, y + 15, color)
    parts.append(f'<line x1="{x + 24}" y1="{y + 56}" x2="{x + width - 24}" y2="{y + 56}" stroke="#26365F"/>')
    columns = 2
    rows = (len(items) + 1) // columns
    for item_index, item in enumerate(items):
        column = item_index // rows
        row = item_index % rows
        item_x = x + 26 + column * ((width - 46) / 2)
        item_y = y + 88 + row * 31
        parts.append(f'<circle class="pulse" cx="{item_x:g}" cy="{item_y - 4:g}" r="3" fill="{color}" style="animation-delay:{delay + item_index * .05:.2f}s"/>')
        parts.append(text(item_x + 14, item_y, item, size=11, fill=MUTED, weight=700, css="reveal", delay=delay + .12 + item_index * .04))


def skills(desktop: bool) -> str:
    width, height = ((1000, 590) if desktop else (560, 1010))
    parts = svg_open(
        width,
        height,
        "Mohamed Sarkouh skills and technology map",
        "Four animated capability cards for AI and automation, cybersecurity, creative development, and infrastructure.",
    )
    shell(parts, width, height, "capabilities.map / evidence-led stack")
    if desktop:
        positions = [(30, 82, 540, 220), (592, 82, 378, 220), (30, 322, 378, 220), (430, 322, 540, 220)]
        for index, (group, (x, y, card_width, card_height)) in enumerate(zip(SKILL_GROUPS, positions, strict=True)):
            skill_card(parts, group, x, y, card_width, card_height, .12 + index * .12)
    else:
        for index, group in enumerate(SKILL_GROUPS):
            skill_card(parts, group, 28, 78 + index * 227, 504, 205, .12 + index * .12)
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


PROJECTS = [
    {
        "index": "01",
        "name": "OPTIQ VISION FORGE",
        "type": "COMPUTER-VISION COMMERCE",
        "summary": ["Optical commerce platform with MediaPipe face mesh,", "3D experiences, full-stack admin, and persistent data."],
        "stack": "REACT · MEDIAPIPE · THREE.JS · EXPRESS · POSTGRESQL",
        "color": CYAN,
        "status": "README PREVIEW · SOURCE PRIVATE",
    },
    {
        "index": "02",
        "name": "APEX FUNDED BOT",
        "type": "AI AUTOMATION WORKFLOW",
        "summary": ["Telegram-to-vision workflow with user confirmation,", "structured trade journaling, Notion, and Sheets sync."],
        "stack": "PYTHON · TELEGRAM · VISION MODELS · NOTION · SHEETS",
        "color": VIOLET,
        "status": "README PREVIEW · SOURCE PRIVATE",
    },
    {
        "index": "03",
        "name": "WATIQA",
        "type": "SECURE VERIFICATION SYSTEM",
        "summary": ["Audited bulk record verification with passkeys, queues,", "malware scanning, role controls, and private networking."],
        "stack": "FASTIFY · POSTGRESQL · REDIS · PRISMA · WEBAUTHN",
        "color": MAGENTA,
        "status": "README PREVIEW · SOURCE PRIVATE",
    },
    {
        "index": "04",
        "name": "MPLS NETWORK LAB",
        "type": "NETWORKING & SECURITY PROJECT",
        "summary": ["Hands-on MPLS and dynamic-routing lab focused on", "Linux infrastructure and security-aware network design."],
        "stack": "MPLS · OSPF · BGP · LINUX · NETWORK SECURITY",
        "color": MINT,
        "status": "README PREVIEW · LAB DETAILS PRIVATE",
    },
]


def project_card(parts: list[str], project: dict[str, object], x: int, y: int, width: int, height: int, delay: float) -> None:
    color = str(project["color"])
    parts.append(rect(x, y, width, height, fill="#0A1227", stroke="#2D3B68", radius=24))
    parts.append(f'<rect x="{x + 1}" y="{y + 1}" width="{width - 2}" height="4" rx="2" fill="{color}" opacity=".9"/>')
    parts.append(text(x + 24, y + 38, str(project["index"]), size=10, fill=color, weight=700, spacing=1.2, css="reveal", delay=delay))
    parts.append(text(x + 62, y + 40, str(project["name"]), size=18 if width < 400 else 21, fill=TEXT, weight=700, spacing=.2, css="reveal display", delay=delay + .05))
    parts.append(text(x + 24, y + 72, str(project["type"]), size=9, fill=color, weight=700, spacing=.8, css="reveal", delay=delay + .10))
    for line_index, line in enumerate(project["summary"]):
        parts.append(text(x + 24, y + 111 + line_index * 22, str(line), size=10 if width < 400 else 11, fill=MUTED, css="reveal", delay=delay + .16))
    parts.append(f'<line x1="{x + 24}" y1="{y + height - 70}" x2="{x + width - 24}" y2="{y + height - 70}" stroke="#26365F"/>')
    parts.append(text(x + 24, y + height - 43, str(project["stack"]), size=8 if width < 400 else 9, fill=TEXT, weight=700, spacing=.1, css="reveal", delay=delay + .22))
    parts.append(text(x + 24, y + height - 18, str(project["status"]), size=7 if width < 400 else 8, fill="#667AA5", weight=700, spacing=.35, css="reveal", delay=delay + .28))
    parts.append(text(x + width - (116 if width < 400 else 132), y + height - 18, "EMAIL FOR DETAILS >", size=7 if width < 400 else 8, fill=color, weight=700, spacing=.25, css="reveal", delay=delay + .32))
    parts.append(f'<circle class="pulse" cx="{x + width - 26}" cy="{y + 27}" r="4" fill="{color}"/>')


def projects(desktop: bool) -> str:
    width, height = ((1000, 650) if desktop else (560, 1165))
    parts = svg_open(
        width,
        height,
        "Selected projects by Mohamed Sarkouh",
        "Premium project showcase for OPTIQ Vision Forge, Apex Funded Bot, WATIQA, and MPLS Network Lab.",
    )
    shell(parts, width, height, "projects.showcase / verified / private-safe")
    if desktop:
        positions = [(30, 82, 550, 250), (602, 82, 368, 250), (30, 352, 368, 250), (420, 352, 550, 250)]
        for index, (project, (x, y, card_width, card_height)) in enumerate(zip(PROJECTS, positions, strict=True)):
            project_card(parts, project, x, y, card_width, card_height, .12 + index * .13)
    else:
        for index, project in enumerate(PROJECTS):
            project_card(parts, project, 28, 78 + index * 268, 504, 246, .12 + index * .13)
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def radar(parts: list[str], cx: int, cy: int, radius: int) -> None:
    for ratio in (.33, .66, 1.0):
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius * ratio:g}" fill="none" stroke="#33436F" stroke-opacity=".7"/>')
    parts.append(f'<line x1="{cx - radius}" y1="{cy}" x2="{cx + radius}" y2="{cy}" stroke="#27375F"/>')
    parts.append(f'<line x1="{cx}" y1="{cy - radius}" x2="{cx}" y2="{cy + radius}" stroke="#27375F"/>')
    for tick in range(24):
        angle = tick * 2 * pi / 24
        outer_x = cx + cos(angle) * radius
        outer_y = cy + sin(angle) * radius
        inner_radius = radius - (8 if tick % 3 == 0 else 4)
        inner_x = cx + cos(angle) * inner_radius
        inner_y = cy + sin(angle) * inner_radius
        parts.append(f'<line x1="{inner_x:g}" y1="{inner_y:g}" x2="{outer_x:g}" y2="{outer_y:g}" stroke="#526898" stroke-opacity="{.72 if tick % 3 == 0 else .38}"/>')
    sweep_angle = -36 * pi / 180
    sweep_x = cx + radius * cos(sweep_angle)
    sweep_y = cy + radius * sin(sweep_angle)
    parts.append(f'<g class="radar" style="transform-origin:{cx}px {cy}px">')
    parts.append(f'<path d="M{cx} {cy} L{cx} {cy - radius} A{radius} {radius} 0 0 1 {sweep_x:g} {sweep_y:g} Z" fill="{CYAN}" fill-opacity=".1" stroke="none"/>')
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{sweep_x:g}" y2="{sweep_y:g}" stroke="{CYAN}" stroke-opacity=".92" stroke-width="1.5" filter="url(#glow)"/>')
    parts.append(f'<path d="M{cx} {cy - radius * .68:g} A{radius * .68:g} {radius * .68:g} 0 0 1 {cx + radius * .68 * cos(sweep_angle):g} {cy + radius * .68 * sin(sweep_angle):g}" fill="none" stroke="{CYAN}" stroke-opacity=".22"/>')
    parts.append("</g>")
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="{BG}" stroke="{CYAN}" stroke-opacity=".8"/>')
    parts.append(f'<circle class="pulse" cx="{cx}" cy="{cy}" r="2.5" fill="{MINT}" filter="url(#glow)"/>')
    dots = [(-.48, -.25, "SIEM", MAGENTA), (.42, -.46, "NETWORK", CYAN), (.28, .42, "ENDPOINT", MINT)]
    for dx, dy, label, color in dots:
        dot_x = cx + radius * dx
        dot_y = cy + radius * dy
        parts.append(f'<circle class="pulse" cx="{dot_x:g}" cy="{dot_y:g}" r="5" fill="{color}" filter="url(#glow)"/>')
        parts.append(text(dot_x + 10, dot_y - 8, label, size=8, fill=color, weight=700, spacing=.45))


def system_status(desktop: bool) -> str:
    width, height = ((1000, 530) if desktop else (560, 860))
    parts = svg_open(
        width,
        height,
        "Mohamed Sarkouh currently building and decorative cybersecurity radar",
        "A decorative animated security radar beside a currently-building panel for AI applications, automation, and cybersecurity labs.",
    )
    shell(parts, width, height, "system.status / decorative visual")
    if desktop:
        parts.append(rect(30, 80, 420, 405, fill="#091126", stroke="#2D3B68", radius=24))
        parts.append(text(54, 112, "DECORATIVE / SECURITY RADAR", size=10, fill=MAGENTA, weight=700, spacing=.85, css="reveal", delay=.12))
        radar(parts, 240, 286, 146)
        parts.append(text(88, 464, "visual motif · not live security telemetry", size=9, fill="#65769E", css="reveal", delay=.7))
        parts.append(rect(474, 80, 496, 405, fill="#0A1227", stroke="#2D3B68", radius=24))
        parts.append(text(502, 119, "CURRENTLY BUILDING", size=11, fill=MINT, weight=700, spacing=1.3, css="reveal", delay=.15))
        items = [
            ("01", "SECURE AI-ASSISTED APPLICATIONS", "Fast prototypes with security-aware architecture.", CYAN),
            ("02", "AGENTIC AUTOMATION", "LLM workflows, MCP, n8n, and API orchestration.", VIOLET),
            ("03", "CYBERSECURITY PRACTICE", "SOC concepts, SIEM monitoring, and network labs.", MAGENTA),
        ]
        for index, (number, heading, detail, color) in enumerate(items):
            iy = 170 + index * 82
            parts.append(text(502, iy, number, size=10, fill=color, weight=700, css="reveal", delay=.28 + index * .12))
            parts.append(text(538, iy, heading, size=12, fill=TEXT, weight=700, css="reveal", delay=.32 + index * .12))
            parts.append(text(538, iy + 24, detail, size=10, fill=MUTED, css="reveal", delay=.37 + index * .12))
        parts.append(f'<line x1="502" y1="410" x2="940" y2="410" stroke="{LINE}"/>')
        parts.append(text(502, 446, "BUILD SMARTER.", size=12, fill=CYAN, weight=700, css="reveal", delay=.78))
        parts.append(text(627, 446, "AUTOMATE FASTER.", size=12, fill=VIOLET, weight=700, css="reveal", delay=.84))
        parts.append(text(788, 446, "THINK SECURELY.", size=12, fill=MINT, weight=700, css="reveal", delay=.90))
    else:
        parts.append(rect(28, 78, 504, 350, fill="#091126", stroke="#2D3B68", radius=22))
        parts.append(text(50, 110, "DECORATIVE / SECURITY RADAR", size=9, fill=MAGENTA, weight=700, spacing=.7, css="reveal", delay=.12))
        radar(parts, 280, 266, 125)
        parts.append(text(128, 407, "visual motif · not live telemetry", size=9, fill="#65769E", css="reveal", delay=.7))
        parts.append(rect(28, 448, 504, 362, fill="#0A1227", stroke="#2D3B68", radius=22))
        parts.append(text(50, 484, "CURRENTLY BUILDING", size=10, fill=MINT, weight=700, spacing=1.1, css="reveal", delay=.15))
        items = [
            ("01", "SECURE AI APPLICATIONS", "Security-aware rapid prototypes.", CYAN),
            ("02", "AGENTIC AUTOMATION", "LLMs, MCP, n8n, and APIs.", VIOLET),
            ("03", "CYBERSECURITY PRACTICE", "SIEM monitoring and network labs.", MAGENTA),
        ]
        for index, (number, heading, detail, color) in enumerate(items):
            iy = 535 + index * 72
            parts.append(text(50, iy, number, size=10, fill=color, weight=700, css="reveal", delay=.28 + index * .12))
            parts.append(text(88, iy, heading, size=12, fill=TEXT, weight=700, css="reveal", delay=.32 + index * .12))
            parts.append(text(88, iy + 23, detail, size=10, fill=MUTED, css="reveal", delay=.37 + index * .12))
        parts.append(text(50, 775, "BUILD SMARTER · AUTOMATE FASTER · THINK SECURELY", size=10, fill=CYAN, weight=700, css="reveal", delay=.82))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def footer(desktop: bool) -> str:
    width, height = ((1000, 190) if desktop else (560, 250))
    parts = svg_open(
        width,
        height,
        "Mohamed Sarkouh coding philosophy",
        "A minimal cyber-terminal footer with Mohamed's coding philosophy and availability status.",
    )
    shell(parts, width, height, "philosophy.sh / end-of-line")
    if desktop:
        parts.append(text(48, 103, ">", size=20, fill=VIOLET, weight=700, css="reveal", delay=.12))
        parts.append(text(78, 103, "BUILD SMARTER. AUTOMATE FASTER. THINK SECURELY.", size=17, fill=TEXT, weight=700, spacing=.5, css="reveal display", delay=.20))
        parts.append(text(78, 139, "AI innovation × creative building × practical security", size=11, fill=MUTED, css="reveal", delay=.32))
        parts.append(f'<circle class="pulse" cx="902" cy="101" r="5" fill="{MINT}"/>')
        parts.append(text(918, 106, "OPEN", size=10, fill=MINT, weight=700, css="reveal", delay=.4))
    else:
        parts.append(text(34, 102, ">", size=18, fill=VIOLET, weight=700, css="reveal", delay=.12))
        parts.append(text(62, 102, "BUILD SMARTER.", size=16, fill=TEXT, weight=700, css="reveal display", delay=.20))
        parts.append(text(62, 133, "AUTOMATE FASTER.", size=16, fill=TEXT, weight=700, css="reveal display", delay=.26))
        parts.append(text(62, 164, "THINK SECURELY.", size=16, fill=MINT, weight=700, css="reveal display", delay=.32))
        parts.append(text(62, 208, "AI innovation × creative building × practical security", size=9, fill=MUTED, css="reveal", delay=.42))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def write_assets() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    generated = {
        "hero.svg": hero(True),
        "hero-mobile.svg": hero(False),
        "projects.svg": projects(True),
        "projects-mobile.svg": projects(False),
        "terminal.svg": terminal(True),
        "terminal-mobile.svg": terminal(False),
        "skills.svg": skills(True),
        "skills-mobile.svg": skills(False),
        "system-status.svg": system_status(True),
        "system-status-mobile.svg": system_status(False),
        "footer.svg": footer(True),
        "footer-mobile.svg": footer(False),
    }
    for filename, content in generated.items():
        (ASSETS / filename).write_text(content, encoding="utf-8", newline="\n")
        print(f"wrote assets/{filename}")


if __name__ == "__main__":
    write_assets()
