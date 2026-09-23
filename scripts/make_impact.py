"""Render the animated impact card (profile/impact-{es,en}.svg). Figures are the ones already public on matiasaguero.dev."""
from html import escape
from pathlib import Path

PROFILE = Path(__file__).resolve().parent.parent / "profile"

W, H = 920, 196
BG = "#0a0a0a"
CARD = "#111113"
BORDER = "#27272a"
ACCENT = "#f97316"
TEXT = "#c9c9d3"
MUTED = "#a1a1aa"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif"
FRAMES = 14
STEP = 0.07

# (prefix, final value, decimals, suffix)
METRICS = [
    ("+", 150, 0, ""),
    ("$", 6.3, 1, "M"),
    ("+", 40, 0, "%"),
    ("+$", 1.8, 1, "M"),
]

TEXTS = {
    "es": {
        "title": "Impacto en Grupo Propital",
        "subtitle": "Resultados de la operación y del CRM TuMatch/Orkezto",
        "labels": [
            ("corredores activos", "en la red"),
            ("CLP recaudados", "récord histórico"),
            ("ventas de", "membresías"),
            ("CLP de ahorro", "operativo"),
        ],
        "aria": "Impacto: más de 150 corredores activos, récord de recaudación de 6,3 millones de CLP, "
                "40% más en ventas de membresías y más de 1,8 millones de CLP de ahorro operativo",
    },
    "en": {
        "title": "Impact at Grupo Propital",
        "subtitle": "Results from operations and the TuMatch/Orkezto CRM",
        "labels": [
            ("active brokers", "in the network"),
            ("CLP collected", "all-time record"),
            ("membership", "sales growth"),
            ("CLP in operating", "savings"),
        ],
        "aria": "Impact: 150+ active brokers, all-time collection record of 6.3M CLP, "
                "40% membership sales growth and 1.8M+ CLP in operating savings",
    },
}


def ease(p):
    return 1 - (1 - p) ** 3


def counter(x, y, prefix, value, decimals, suffix, delay):
    out = []
    for i in range(1, FRAMES + 1):
        v = value * ease(i / FRAMES)
        label = f"{prefix}{v:.{decimals}f}{suffix}"
        cls = "k last" if i == FRAMES else "k"
        out.append(
            f'<text class="{cls}" style="animation-delay:{delay + (i - 1) * STEP:.2f}s" x="{x}" y="{y}" '
            f'fill="{ACCENT}" font-size="34" font-weight="700" text-anchor="middle">{label}</text>'
        )
    return out


def render(t):
    col_w = (W - 60 - 3 * 16) / 4
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{escape(t["aria"])}">',
        "<style>",
        f"text{{font-family:{FONT};}}",
        ".n{opacity:0;animation:up .6s cubic-bezier(.2,.8,.3,1) forwards;}",
        ".bar{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:grow 1s ease-out forwards;}",
        f".k{{opacity:0;animation:flash {STEP}s linear;}}",
        ".k.last{animation:hold .01s linear forwards;}",
        "@keyframes flash{from,to{opacity:1;}}",
        "@keyframes hold{to{opacity:1;}}",
        "@keyframes up{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:none;}}",
        "@keyframes grow{to{transform:scaleX(1);}}",
        "@media (prefers-reduced-motion:reduce){.n,.k.last{animation:none;opacity:1;}.k{animation:none;}.bar{animation:none;transform:none;}}",
        "</style>",
        f'<rect width="{W}" height="{H}" rx="4.5" fill="{BG}"/>',
        f'<text x="30" y="38" fill="{ACCENT}" font-size="18" font-weight="600">{escape(t["title"])}</text>',
        f'<text x="30" y="60" fill="{MUTED}" font-size="12">{escape(t["subtitle"])}</text>',
    ]
    for i, ((prefix, value, decimals, suffix), (l1, l2)) in enumerate(zip(METRICS, t["labels"])):
        x = 30 + i * (col_w + 16)
        cx = x + col_w / 2
        delay = 0.3 + i * 0.15
        out += [
            f'<g class="n" style="animation-delay:{delay:.2f}s">',
            f'<rect x="{x:.1f}" y="80" width="{col_w:.1f}" height="96" rx="8" fill="{CARD}" stroke="{BORDER}"/>',
            f'<rect class="bar" style="animation-delay:{delay + 0.2:.2f}s" x="{x + 16:.1f}" y="80" '
            f'width="{col_w - 32:.1f}" height="2" rx="1" fill="{ACCENT}"/>',
            f'<text x="{cx:.1f}" y="146" fill="{TEXT}" font-size="11.5" text-anchor="middle">{escape(l1)}</text>',
            f'<text x="{cx:.1f}" y="162" fill="{MUTED}" font-size="11" text-anchor="middle">{escape(l2)}</text>',
            "</g>",
        ]
        out += counter(round(cx, 1), 124, prefix, value, decimals, suffix, delay + 0.2)
    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for lang, t in TEXTS.items():
        path = PROFILE / f"impact-{lang}.svg"
        path.write_text(render(t), encoding="utf-8")
        print(f"wrote {path}")
