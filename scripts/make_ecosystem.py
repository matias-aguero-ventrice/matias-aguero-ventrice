"""Render the animated product-ecosystem diagram (profile/ecosystem-{es,en}.svg)."""
from html import escape, unescape
from pathlib import Path

PROFILE = Path(__file__).resolve().parent.parent / "profile"

W, H = 900, 392
BG = "#0a0a0a"
CARD = "#111113"
BORDER = "#27272a"
ACCENT = "#f97316"
NAME = "#f5f5f5"
TEXT = "#c9c9d3"
MUTED = "#a1a1aa"
LIVE = "#22c55e"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif"

TEXTS = {
    "es": {
        "title": "Ecosistema de producto",
        "subtitle": "Cómo se conectan los productos que construyo y coordino",
        "built": "DISEÑÉ Y CONSTRUÍ",
        "lead": "COORDINO",
        "contrib": "CONTRIBUYO",
        "tm": ["CRM inmobiliario multi-marca", "leads · propiedades · cobranzas", "en producción · 6 APIs externas"],
        "pr": ["Gestión de propiedades", "integración propia hacia Numinap", None],
        "nu": ["Planificación patrimonial", "patrimonio del inversionista", "integraciones en producción"],
        "orv": ["Plataforma inmobiliaria", "multi-tenant · LatAm", "en producción"],
        "pills": ["MercadoPago · Stripe", "Twilio · WhatsApp/SMS", "Módulo de postventa"],
        "edge_a": ("link de referido", "corredor → cliente"),
        "edge_b": ("flujo de caja", "propiedad → patrimonio"),
        "aria": "Diagrama del ecosistema de producto: TuMatch/Orkezto y Propirent se integran con Numinap; Orvyt integra pagos, mensajería y postventa",
    },
    "en": {
        "title": "Product ecosystem",
        "subtitle": "How the products I build and lead connect",
        "built": "DESIGNED & BUILT",
        "lead": "LEAD",
        "contrib": "CONTRIBUTOR",
        "tm": ["Multi-brand real-estate CRM", "leads · properties · billing", "in production · 6 external APIs"],
        "pr": ["Property management", "own integration into Numinap", None],
        "nu": ["Wealth planning", "investor net worth", "integrations in production"],
        "orv": ["Real-estate platform", "multi-tenant · LatAm", "in production"],
        "pills": ["MercadoPago · Stripe", "Twilio · WhatsApp/SMS", "After-sales module"],
        "edge_a": ("referral link", "broker → client"),
        "edge_b": ("cash flow", "property → net worth"),
        "aria": "Product ecosystem diagram: TuMatch/Orkezto and Propirent integrate into Numinap; Orvyt integrates payments, messaging and after-sales",
    },
}

NODES = {
    "tm": (30, 90, 230, 118),
    "pr": (30, 250, 230, 118),
    "nu": (400, 170, 240, 118),
    "orv": (690, 90, 180, 118),
}

EDGE_A = "M260,149 C330,149 330,215 400,215"
EDGE_B = "M260,309 C330,309 330,243 400,243"

SPINE_X = 708
PILL_X, PILL_W, PILL_H = 722, 148, 26
PILL_YS = (236, 276, 316)


def escape_all(v):
    if isinstance(v, str):
        return escape(v)
    if v is None:
        return None
    return type(v)(escape_all(x) for x in v)


def node(key, name, chip, lines, delay, hub=False):
    x, y, w, h = NODES[key]
    chip_w = len(unescape(chip)) * 6.4 + 16
    stroke = ACCENT if hub else BORDER
    out = [
        f'<g class="n" style="animation-delay:{delay}s">',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{CARD}" stroke="{stroke}"'
        + (' filter="url(#glow)"' if hub else "") + "/>",
        f'<rect x="{x + 14}" y="{y + 12}" width="{chip_w:.0f}" height="18" rx="9" fill="none" '
        f'stroke="{ACCENT}" stroke-opacity=".55"/>',
        f'<text x="{x + 14 + chip_w / 2:.0f}" y="{y + 25}" fill="{ACCENT}" font-size="9.5" '
        f'font-weight="600" letter-spacing=".6" text-anchor="middle">{chip}</text>',
        f'<text x="{x + 14}" y="{y + 54}" fill="{NAME}" font-size="16" font-weight="600">{name}</text>',
        f'<text x="{x + 14}" y="{y + 75}" fill="{TEXT}" font-size="11.5">{lines[0]}</text>',
        f'<text x="{x + 14}" y="{y + 92}" fill="{MUTED}" font-size="11">{lines[1]}</text>',
    ]
    if lines[2]:
        out += [
            f'<circle cx="{x + 18}" cy="{y + 105}" r="3" fill="{LIVE}"/>',
            f'<text x="{x + 27}" y="{y + 109}" fill="{MUTED}" font-size="10.5">{lines[2]}</text>',
        ]
    out.append("</g>")
    return out


def edge(pid, d, label, sub, label_y, delay):
    return [
        f'<path id="{pid}" class="e" style="animation-delay:{delay}s" d="{d}" pathLength="1" '
        f'fill="none" stroke="{ACCENT}" stroke-opacity=".7" stroke-width="1.6"/>',
        f'<g class="n" style="animation-delay:{delay + 0.3}s">',
        f'<text x="330" y="{label_y}" fill="{TEXT}" font-size="11" font-weight="600" text-anchor="middle">{label}</text>',
        f'<text x="330" y="{label_y + 14}" fill="{MUTED}" font-size="10" text-anchor="middle">{sub}</text>',
        "</g>",
    ] + [
        f'<circle r="3.2" fill="{ACCENT}" opacity="0">'
        f'<set attributeName="opacity" to="1" begin="{delay + 0.9 + i * 1.1:.1f}s"/>'
        f'<animateMotion dur="2.2s" repeatCount="indefinite" begin="{delay + 0.9 + i * 1.1:.1f}s">'
        f'<mpath href="#{pid}" xlink:href="#{pid}"/></animateMotion></circle>'
        for i in range(2)
    ]


def render(t):
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{t["aria"]}">',
        "<style>",
        f"text{{font-family:{FONT};}}",
        ".n{opacity:0;animation:up .6s cubic-bezier(.2,.8,.3,1) forwards;}",
        ".e{stroke-dasharray:1;stroke-dashoffset:1;animation:draw .8s ease-out forwards;}",
        "@keyframes up{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:none;}}",
        "@keyframes draw{to{stroke-dashoffset:0;}}",
        "@media (prefers-reduced-motion:reduce){.n,.e{animation:none;opacity:1;stroke-dashoffset:0;}}",
        "</style>",
        "<defs>",
        '<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">'
        f'<feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="{ACCENT}" flood-opacity=".35"/></filter>',
        "</defs>",
        f'<rect width="{W}" height="{H}" rx="4.5" fill="{BG}"/>',
        f'<text x="30" y="38" fill="{ACCENT}" font-size="18" font-weight="600">{t["title"]}</text>',
        f'<text x="30" y="60" fill="{MUTED}" font-size="12">{t["subtitle"]}</text>',
    ]
    out += node("tm", "TuMatch / Orkezto", t["built"], t["tm"], 0.1)
    out += node("pr", "Propirent", t["contrib"], t["pr"], 0.25)
    out += node("nu", "Numinap", t["lead"], t["nu"], 0.4, hub=True)
    out += node("orv", "Orvyt", t["contrib"], t["orv"], 0.55)
    out += edge("ea", EDGE_A, *t["edge_a"], 133, 0.8)
    out += edge("eb", EDGE_B, *t["edge_b"], 334, 1.0)

    spine_end = PILL_YS[-1] + PILL_H / 2
    out.append(
        f'<path class="e" style="animation-delay:1.1s" d="M{SPINE_X},208 V{spine_end}" pathLength="1" '
        f'fill="none" stroke="{BORDER}" stroke-width="1.4"/>'
    )
    for i, (py, label) in enumerate(zip(PILL_YS, t["pills"])):
        mid = py + PILL_H / 2
        out += [
            f'<g class="n" style="animation-delay:{1.3 + i * 0.15:.2f}s">',
            f'<path d="M{SPINE_X},{mid} H{PILL_X}" stroke="{BORDER}" stroke-width="1.4"/>',
            f'<rect x="{PILL_X}" y="{py}" width="{PILL_W}" height="{PILL_H}" rx="13" fill="{CARD}" stroke="{BORDER}"/>',
            f'<text x="{PILL_X + PILL_W / 2}" y="{py + 17}" fill="{TEXT}" font-size="10.5" text-anchor="middle">{label}</text>',
            "</g>",
        ]
    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for lang, t in TEXTS.items():
        t = {k: escape_all(v) for k, v in t.items()}
        path = PROFILE / f"ecosystem-{lang}.svg"
        path.write_text(render(t), encoding="utf-8")
        print(f"wrote {path}")
