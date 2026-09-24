"""Render the animated profile banner (assets/banner.svg)."""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "banner.svg"

W, H = 1280, 320
ACCENT = "#f97316"
PEACH = "#fdba74"
NAME = "#fafafa"
FONT = "Inter, 'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"

NAME_TEXT = "Matías Agüero Ventrice"
ROLE = "Head of Product &amp; Operations · Grupo Propital"
CHIPS = ["Next.js", "React", "TypeScript", "Supabase", "Python", "Claude API"]

DOTS = [(1120, 70, 3.2, 0.0), (1180, 150, 2.6, 1.1), (1060, 210, 2.4, 0.6), (1210, 250, 3.4, 1.7), (980, 60, 2.2, 2.3)]
SQUARES = [(1153, 43, 0.0), (1084, 124, 1.3), (1010, 262, 0.7)]


def render():
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        'role="img" aria-label="Matías Agüero Ventrice — Head of Product &amp; Operations">',
        "<style>",
        f"text{{font-family:{FONT};}}",
        f".mono{{font-family:{MONO};}}",
        ".in{opacity:0;animation:up .8s cubic-bezier(.2,.8,.3,1) forwards;}",
        ".dot{animation:float 6s ease-in-out infinite;}",
        ".sq{transform-box:fill-box;transform-origin:center;animation:spin 9s linear infinite;}",
        "@keyframes up{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:none;}}",
        "@keyframes float{50%{transform:translateY(-10px);opacity:.45;}}",
        "@keyframes spin{to{transform:rotate(360deg);}}",
        "@media (prefers-reduced-motion:reduce){.in{animation:none;opacity:1;}.dot,.sq{animation:none;}}",
        "</style>",
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0b0c"/>'
        '<stop offset="1" stop-color="#18181b"/></linearGradient>',
        f'<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".16"/>'
        f'<stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>',
        f'<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="-520" y1="0" x2="0" y2="0">'
        f'<stop offset="0" stop-color="{NAME}"/><stop offset=".35" stop-color="{ACCENT}"/>'
        f'<stop offset=".6" stop-color="{PEACH}"/><stop offset="1" stop-color="{NAME}"/>'
        '<animateTransform attributeName="gradientTransform" type="translate" from="160 0" to="1300 0" '
        'dur="4.5s" repeatCount="indefinite"/></linearGradient>',
        f'<clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
        "</defs>",
        '<g clip-path="url(#card)">',
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
        '<ellipse cx="180" cy="90" rx="320" ry="220" fill="url(#glow)"/>',
        '<g stroke="#ffffff" stroke-opacity=".05">',
    ]
    for i in range(7):
        y = -40 + i * 60
        out.append(f'<line x1="0" y1="{y + 70}" x2="{W}" y2="{y}"/>')
    out += [
        "</g>",
        f'<rect width="6" height="{H}" fill="{ACCENT}"/>',
        "</g>",
    ]

    for x, y, r, delay in DOTS:
        out.append(f'<circle class="dot" style="animation-delay:{delay}s" cx="{x}" cy="{y}" r="{r}" fill="{ACCENT}" fill-opacity=".85"/>')
    for x, y, delay in SQUARES:
        out.append(
            f'<rect class="sq" style="animation-delay:{delay}s" x="{x}" y="{y}" width="7" height="7" fill="none" '
            f'stroke="{ACCENT}" stroke-opacity=".8"/>'
        )

    out += [
        '<g class="in" style="animation-delay:.1s">',
        f'<rect x="80" y="90" width="140" height="140" rx="16" fill="#141416" stroke="{ACCENT}" stroke-width="1.5"/>',
        f'<text x="150" y="182" fill="{ACCENT}" font-size="64" font-weight="300" text-anchor="middle" '
        'letter-spacing="-2">MA</text>',
        "</g>",
        '<g class="in" style="animation-delay:.25s">',
        f'<text x="258" y="127" fill="url(#shine)" font-size="46" font-weight="700" letter-spacing="-.5">{NAME_TEXT}</text>',
        "</g>",
        '<g class="in" style="animation-delay:.4s">',
        f'<text x="260" y="167" fill="{ACCENT}" font-size="19">{ROLE}</text>',
        "</g>",
    ]

    x = 260
    for i, chip in enumerate(CHIPS):
        w = len(chip) * 8.4 + 28
        hot = chip == "Claude API"
        fill, stroke, color = ("#2a1206", ACCENT, ACCENT) if hot else ("#18181b", "#2e2e33", "#d4d4d8")
        out += [
            f'<g class="in" style="animation-delay:{0.55 + i * 0.08:.2f}s">',
            f'<rect x="{x}" y="205" width="{w:.0f}" height="34" rx="7" fill="{fill}" stroke="{stroke}" '
            f'stroke-opacity="{0.9 if hot else 1}"/>',
            f'<text x="{x + w / 2:.0f}" y="227" class="mono" fill="{color}" font-size="13.5" '
            f'text-anchor="middle">{chip}</text>',
            "</g>",
        ]
        x += w + 12

    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    OUT.write_text(render(), encoding="utf-8")
    print(f"wrote {OUT}")
