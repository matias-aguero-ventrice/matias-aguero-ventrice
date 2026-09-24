"""Render the animated profile banner (assets/banner.svg)."""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "banner.svg"

W, H = 1280, 320
ACCENT = "#f97316"
PEACH = "#fdba74"
NAME = "#fafafa"
MUTED = "#a1a1aa"
FONT = "Inter, 'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"

NAME_TEXT = "Matías Agüero Ventrice"
ROLE = "Head of Product &amp; Operations · Grupo Propital"
LOCATION = "San Juan, Argentina · Remoto"
CHIPS = ["Next.js", "React", "TypeScript", "Supabase", "Python", "Claude API"]

TERM_X, TERM_Y, TERM_W, TERM_H = 930, 60, 310, 200
TERMINAL = [
    ("cmd", "whoami"),
    ("out", "matías — product &amp; ops builder"),
    ("cmd", "ls proyectos/"),
    ("hi", "misuper/  made-in-3d/  portfolio/"),
    ("cmd", "cat foco.txt"),
    ("out", "producto · operaciones · IA aplicada"),
]


def render():
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        'aria-label="Matías Agüero Ventrice — Head of Product &amp; Operations · Grupo Propital">',
        "<style>",
        f"text{{font-family:{FONT};}}",
        f".mono{{font-family:{MONO};white-space:pre;}}",
        ".in{opacity:0;animation:up .8s cubic-bezier(.2,.8,.3,1) forwards;}",
        ".drift1{animation:drift 14s ease-in-out infinite alternate;}",
        ".drift2{animation:drift 18s ease-in-out -6s infinite alternate-reverse;}",
        f".cursor{{opacity:0;animation:blink 1s steps(1) {0.9 + len(TERMINAL) * 0.3:.2f}s infinite;}}",
        "@keyframes up{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:none;}}",
        "@keyframes drift{to{transform:translate(60px,20px);}}",
        "@keyframes blink{0%{opacity:1;}50%{opacity:0;}}",
        "@media (prefers-reduced-motion:reduce){.in,.cursor{animation:none;opacity:1;}.drift1,.drift2{animation:none;}}",
        "</style>",
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#09090b"/>'
        '<stop offset="1" stop-color="#151518"/></linearGradient>',
        '<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">'
        '<path d="M32 0H0V32" fill="none" stroke="#ffffff" stroke-opacity=".045"/></pattern>',
        '<radialGradient id="fade" cx=".45" cy=".45" r=".7"><stop offset="0" stop-color="#fff"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>',
        f'<mask id="gridmask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>',
        '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="55"/></filter>',
        f'<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACCENT}"/>'
        f'<stop offset="1" stop-color="{ACCENT}" stop-opacity=".15"/></linearGradient>',
        f'<linearGradient id="ring" gradientUnits="userSpaceOnUse" x1="80" y1="90" x2="220" y2="230">'
        f'<stop offset="0" stop-color="{ACCENT}"/><stop offset=".5" stop-color="{PEACH}"/>'
        f'<stop offset="1" stop-color="{ACCENT}" stop-opacity=".15"/>'
        '<animateTransform attributeName="gradientTransform" type="rotate" from="0 150 160" to="360 150 160" '
        'dur="6s" repeatCount="indefinite"/></linearGradient>',
        f'<linearGradient id="mark" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{PEACH}"/>'
        f'<stop offset="1" stop-color="{ACCENT}"/></linearGradient>',
        f'<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="-520" y1="0" x2="0" y2="0">'
        f'<stop offset="0" stop-color="{NAME}"/><stop offset=".4" stop-color="{ACCENT}"/>'
        f'<stop offset=".6" stop-color="{PEACH}"/><stop offset="1" stop-color="{NAME}"/>'
        '<animateTransform attributeName="gradientTransform" type="translate" from="160 0" to="1300 0" '
        'begin="1s" dur="5s" repeatCount="indefinite"/></linearGradient>',
        '<clipPath id="type"><rect x="258" y="140" width="0" height="36">'
        '<animate attributeName="width" from="0" to="520" begin=".6s" dur="1.4s" fill="freeze" '
        'calcMode="spline" keyTimes="0;1" keySplines=".4 0 .2 1"/></rect></clipPath>',
        f'<clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
        "</defs>",
        '<g clip-path="url(#card)">',
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
        f'<g class="drift1"><ellipse cx="200" cy="80" rx="240" ry="150" fill="{ACCENT}" fill-opacity=".20" filter="url(#blur)"/></g>',
        f'<g class="drift2"><ellipse cx="1060" cy="250" rx="260" ry="130" fill="{ACCENT}" fill-opacity=".10" filter="url(#blur)"/></g>',
        f'<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridmask)"/>',
        f'<rect width="5" height="{H}" fill="url(#bar)"/>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="#ffffff" stroke-opacity=".06"/>',
        "</g>",
    ]

    tx, ty = TERM_X, TERM_Y
    out += [
        '<g class="in" style="animation-delay:.5s">',
        f'<rect x="{tx}" y="{ty}" width="{TERM_W}" height="{TERM_H}" rx="10" fill="#0e0e10" fill-opacity=".92" stroke="#2e2e33"/>',
        f'<path d="M{tx},{ty + 28} H{tx + TERM_W}" stroke="#2e2e33"/>',
        *[f'<circle cx="{tx + 16 + i * 14}" cy="{ty + 14}" r="4.5" fill="{c}" fill-opacity=".85"/>'
          for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840"))],
        f'<text class="mono" x="{tx + TERM_W / 2}" y="{ty + 18}" fill="#71717a" font-size="11" text-anchor="middle">~/matias</text>',
        "</g>",
    ]
    colors = {"out": "#e4e4e7", "hi": PEACH}
    y = ty + 50
    for i, (kind, text) in enumerate(TERMINAL):
        body = (f'<tspan fill="{ACCENT}">$</tspan> <tspan fill="#d4d4d8">{text}</tspan>' if kind == "cmd"
                else f'<tspan fill="{colors[kind]}">{text}</tspan>')
        out.append(
            f'<text class="mono in" style="animation-delay:{0.9 + i * 0.3:.2f}s" x="{tx + 16}" y="{y}" font-size="12">{body}</text>'
        )
        y += 22
    out += [
        f'<text class="mono in" style="animation-delay:{0.9 + len(TERMINAL) * 0.3:.2f}s" x="{tx + 16}" y="{y}" '
        f'font-size="12" fill="{ACCENT}">$</text>',
        f'<rect class="cursor" x="{tx + 30}" y="{y - 11}" width="7" height="14" fill="{PEACH}"/>',
    ]

    out += [
        '<g class="in" style="animation-delay:.1s">',
        f'<rect x="80" y="90" width="140" height="140" rx="18" fill="#121214"/>',
        f'<rect x="80" y="90" width="140" height="140" rx="18" fill="none" stroke="url(#ring)" stroke-width="2"/>',
        '<text x="150" y="182" fill="url(#mark)" font-size="64" font-weight="300" text-anchor="middle" '
        'letter-spacing="-2">MA</text>',
        "</g>",
        '<g class="in" style="animation-delay:.25s">',
        f'<text x="258" y="127" fill="url(#shine)" font-size="46" font-weight="700" letter-spacing="-.5">{NAME_TEXT}</text>',
        "</g>",
        f'<text clip-path="url(#type)" x="260" y="167" fill="{ACCENT}" font-size="19">{ROLE}</text>',
    ]

    x = 260
    for i, chip in enumerate(CHIPS):
        w = len(chip) * 8.4 + 28
        hot = chip == "Claude API"
        fill, stroke, color = ("#2a1206", ACCENT, ACCENT) if hot else ("#18181b", "#2e2e33", "#d4d4d8")
        out += [
            f'<g class="in" style="animation-delay:{1.0 + i * 0.08:.2f}s">',
            f'<rect x="{x}" y="200" width="{w:.0f}" height="34" rx="7" fill="{fill}" fill-opacity=".9" stroke="{stroke}"/>',
            f'<text x="{x + w / 2:.0f}" y="222" class="mono" fill="{color}" font-size="13.5" text-anchor="middle">{chip}</text>',
            "</g>",
        ]
        x += w + 12

    out += [
        '<g class="in" style="animation-delay:1.6s">',
        f'<circle cx="266" cy="263" r="3.5" fill="#22c55e"/>',
        f'<circle cx="266" cy="263" r="3.5" fill="none" stroke="#22c55e"><animate attributeName="r" from="3.5" to="9" '
        'begin="2s" dur="2s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" from=".7" to="0" '
        'begin="2s" dur="2s" repeatCount="indefinite"/></circle>',
        f'<text x="278" y="268" fill="{MUTED}" font-size="13.5">{LOCATION}</text>',
        "</g>",
        "</svg>",
    ]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    OUT.write_text(render(), encoding="utf-8")
    print(f"wrote {OUT}")
