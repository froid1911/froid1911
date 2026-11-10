#!/usr/bin/env python3
"""Generate the light/dark SVGs used by README.md.

Run from the repo root:  python3 scripts/build.py
Edit the content below, re-run, commit the regenerated assets/.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "light": {"bg": "#ffffff", "fg": "#000000", "muted": "#6b6b6b", "line": "#dddddd", "accent": "#000000", "chip": "#f4f4f4"},
    "dark": {"bg": "#0d1117", "fg": "#f0f0f0", "muted": "#8b949e", "line": "#30363d", "accent": "#ffffff", "chip": "#161b22"},
}

MONO = "'Noto Sans Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

HEADER_LINES = [
    ("prompt", "froid@web3.berlin:~$ whoami"),
    ("title", "Frank"),
    ("body", "Founder of web3.berlin. Blockchain and AI systems that run in production."),
    ("body", "Peer-to-peer since Napster. Writing software professionally since 2010."),
    ("blank", ""),
    ("prompt", "froid@web3.berlin:~$ ls ~/now"),
    ("body", "powerhouse/   herdr+whistle/   local-ai-stack/   cortical-mirror/"),
]

TAGS = ["ethereum", "subgraphs", "p2p", "local ai", "agents", "k3s", "berlin"]

LINKS = [
    ("web3", "web3.berlin"),
    ("linkedin", "linkedin"),
    ("x", "x / twitter"),
    ("email", "email"),
]

CARDS = [
    ("whistle", "herdr + whistle", ["Android remote for herdr", "agent sessions. Approve,", "prompt, read agents as chat."], "Kotlin · Go"),
    ("local-ai", "local-ai-stack", ["3x RTX 3090, own C++/CUDA", "engine, vLLM, llama.cpp.", "No cloud API required."], "Shell · CUDA"),
    ("cortical", "cortical-mirror", ["A virtual cortex that learns", "to see with local rules.", "Live webcam demo."], "Python"),
]

WORK = [
    ("powerhouse", "Powerhouse", "2023 – today", ["Core team, Sky ecosystem.", "Document engine, Switchboard,", "Vetra Cloud, private doc AI."], "TypeScript · Rust · k3s"),
    ("aavegotchi", "Aavegotchi", "2021 – 2024", ["Lead subgraph developers.", "Core, Gotchiverse, Baazaar.", "176 merged PRs."], "The Graph · Polygon"),
    ("validators", "Ethereum", "since genesis", ["Validators since Beacon", "Chain genesis, 1 Dec 2020.", "Launchpad contributor."], "geth · Prysm"),
]


def svg(w, h, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{escape(label)}">\n{body}\n</svg>\n'
    )


def text(x, y, s, size, fill, weight=400, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>'
    )


def header(t):
    w, h = 1000, 350
    parts = [
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="{t["bg"]}" stroke="{t["line"]}"/>',
        f'<line x1="0" y1="40" x2="{w}" y2="40" stroke="{t["line"]}"/>',
    ]
    for i in range(3):
        parts.append(f'<circle cx="{24 + i * 18}" cy="20" r="5" fill="none" stroke="{t["muted"]}"/>')
    parts.append(text(w / 2, 25, "froid1911 — bash", 13, t["muted"], anchor="middle"))

    y = 82
    for kind, s in HEADER_LINES:
        if kind == "prompt":
            parts.append(text(32, y, s, 15, t["muted"]))
            y += 38
        elif kind == "title":
            parts.append(text(32, y + 6, s, 44, t["fg"], weight=700))
            y += 44
        elif kind == "body":
            parts.append(text(32, y, s, 16, t["fg"]))
            y += 26
        else:
            y += 10

    x = 32
    for tag in TAGS:
        tw = len(tag) * 8.4 + 22
        parts.append(f'<rect x="{x}" y="{h - 52}" width="{tw}" height="26" rx="13" fill="{t["chip"]}" stroke="{t["line"]}"/>')
        parts.append(text(x + tw / 2, h - 34, tag, 13, t["fg"], anchor="middle"))
        x += tw + 10
    parts.append(f'<rect x="{x}" y="{h - 49}" width="10" height="20" fill="{t["fg"]}"/>')
    return svg(w, h, "\n".join(parts), "Frank — founder of web3.berlin")


def link(t, label):
    w, h = 330, 56
    body = "\n".join([
        f'<rect x="4.5" y="4.5" width="{w - 9}" height="{h - 9}" rx="8" fill="{t["bg"]}" stroke="{t["fg"]}"/>',
        text(24, 36, ">", 22, t["muted"]),
        text(48, 36, label, 22, t["fg"], weight=600),
        text(w - 24, 36, "↗", 22, t["muted"], anchor="end"),
    ])
    return svg(w, h, body, label)


def card(t, title, lines, footer, meta=None):
    w, h = 330, 190
    parts = [
        f'<rect x="4.5" y="4.5" width="{w - 9}" height="{h - 9}" rx="10" fill="{t["bg"]}" stroke="{t["line"]}"/>',
        text(24, 42, title, 18, t["fg"], weight=700),
    ]
    if meta:
        parts.append(text(w - 24, 42, meta, 12, t["muted"], anchor="end"))
    parts.append(f'<line x1="24" y1="58" x2="{w - 24}" y2="58" stroke="{t["line"]}"/>')
    for i, s in enumerate(lines):
        parts.append(text(24, 86 + i * 22, s, 13.5, t["fg"]))
    parts.append(text(24, h - 24, footer, 12, t["muted"]))
    return svg(w, h, "\n".join(parts), title)


def main():
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"header_{name}.svg").write_text(header(t))
        for key, label in LINKS:
            (OUT / f"link_{key}_{name}.svg").write_text(link(t, label))
        for key, title, lines, footer in CARDS:
            (OUT / f"card_{key}_{name}.svg").write_text(card(t, title, lines, footer))
        for key, title, when, lines, footer in WORK:
            (OUT / f"work_{key}_{name}.svg").write_text(card(t, title, lines, footer, meta=when))


if __name__ == "__main__":
    main()
