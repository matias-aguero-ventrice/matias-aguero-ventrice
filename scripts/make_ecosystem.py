"""Render the animated product-ecosystem diagram (profile/ecosystem-{es,en}.svg)."""
from html import escape, unescape
from pathlib import Path

PROFILE = Path(__file__).resolve().parent.parent / "profile"

W, H = 900, 548
BG = "#0a0a0a"
CARD = "#111113"
BORDER = "#27272a"
ACCENT = "#f97316"
LINK = "#71717a"
NAME = "#f5f5f5"
TEXT = "#c9c9d3"
MUTED = "#a1a1aa"
LIVE = "#22c55e"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif"

TEXTS = {
    "es": {
        "title": "Ecosistema Grupo Propital",
        "subtitle": "Cómo se conectan los productos que construyo y coordino",
        "legend_flow": "flujo de datos",
        "legend_link": "integración",
        "built": "DISEÑÉ Y CONSTRUÍ",
        "lead": "COORDINO",
        "contrib": "CONTRIBUYO",
        "head": "LIDERO PRODUCTO & OPS",
        "own": "DESARROLLO PROPIO",
        "tm": ["CRM inmobiliario multi-marca", "leads · propiedades · cobranzas", "en producción · 6 APIs externas"],
        "pr": ["Gestión de propiedades", "integración propia hacia Numinap", None],
        "nu": ["Planificación patrimonial", "patrimonio del inversionista", "integraciones en producción"],
        "orv": ["Plataforma multi-tenant", "pagos · mensajería · postventa", "en producción"],
        "prop": ["Grupo proptech · Chile", "producto y operaciones del grupo", None],
        "ms": ["Gestión para kioscos y comercios minoristas: ventas, stock e inventario",
               "demo en vivo · Next.js · TypeScript · Supabase"],
        "edge_a": ("link de referido", "corredor → cliente"),
        "edge_b": ("flujo de caja", "propiedad → patrimonio"),
        "aria": "Diagrama del ecosistema Grupo Propital: TuMatch/Orkezto y Propirent envían datos a Numinap; "
                "Orvyt y Propital se integran con Numinap, y entre sí. Aparte, MiSUPER, desarrollo propio",
    },
    "en": {
        "title": "Grupo Propital ecosystem",
        "subtitle": "How the products I build and lead connect",
        "legend_flow": "data flow",
        "legend_link": "integration",
        "built": "DESIGNED & BUILT",
        "lead": "LEAD",
        "contrib": "CONTRIBUTOR",
        "head": "HEAD OF PRODUCT & OPS",
        "own": "PERSONAL PROJECT",
        "tm": ["Multi-brand real-estate CRM", "leads · properties · billing", "in production · 6 external APIs"],
        "pr": ["Property management", "own integration into Numinap", None],
        "nu": ["Wealth planning", "investor net worth", "integrations in production"],
        "orv": ["Multi-tenant platform", "payments · messaging · after-sales", "in production"],
        "prop": ["Proptech group · Chile", "group-wide product & operations", None],
        "ms": ["Management system for kiosks and small retailers: sales, stock and inventory",
               "live demo · Next.js · TypeScript · Supabase"],
        "edge_a": ("referral link", "broker → client"),
        "edge_b": ("cash flow", "property → net worth"),
        "aria": "Grupo Propital ecosystem diagram: TuMatch/Orkezto and Propirent send data to Numinap; "
                "Orvyt and Propital integrate with Numinap and with each other. Separately, MiSUPER, a personal project",
    },
}

NODES = {
    "tm": (30, 90, 230, 118),
    "pr": (30, 270, 230, 118),
    "nu": (380, 180, 220, 118),
    "orv": (670, 90, 200, 118),
    "prop": (670, 270, 200, 118),
}

EDGE_A = "M260,149 C320,149 320,225 380,225"
EDGE_B = "M260,329 C320,329 320,253 380,253"
LINK_C = "M670,149 C635,149 635,225 600,225"
LINK_D = "M770,208 V270"
LINK_E = "M670,329 C635,329 635,253 600,253"

MS = (30, 444, 840, 80)


def escape_all(v):
    if isinstance(v, str):
        return escape(v)
    if v is None:
        return None
    return type(v)(escape_all(x) for x in v)


def chip(x, y, label):
    w = len(unescape(label)) * 6.4 + 16
    return [
        f'<rect x="{x}" y="{y}" width="{w:.0f}" height="18" rx="9" fill="none" stroke="{ACCENT}" stroke-opacity=".55"/>',
        f'<text x="{x + w / 2:.0f}" y="{y + 13}" fill="{ACCENT}" font-size="9.5" font-weight="600" '
        f'letter-spacing=".6" text-anchor="middle">{label}</text>',
    ]


def live(x, y, label):
    return [
        f'<circle cx="{x + 4}" cy="{y - 4}" r="3" fill="{LIVE}"/>',
        f'<text x="{x + 13}" y="{y}" fill="{MUTED}" font-size="10.5">{label}</text>',
    ]


def node(key, name, role, lines, delay, hub=False):
    x, y, w, h = NODES[key]
    stroke = ACCENT if hub else BORDER
    out = [
        f'<g class="n" style="animation-delay:{delay}s">',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{CARD}" stroke="{stroke}"'
        + (' filter="url(#glow)"' if hub else "") + "/>",
        *chip(x + 14, y + 12, role),
        f'<text x="{x + 14}" y="{y + 54}" fill="{NAME}" font-size="16" font-weight="600">{name}</text>',
        f'<text x="{x + 14}" y="{y + 75}" fill="{TEXT}" font-size="11.5">{lines[0]}</text>',
        f'<text x="{x + 14}" y="{y + 92}" fill="{MUTED}" font-size="11">{lines[1]}</text>',
    ]
    if lines[2]:
        out += live(x + 14, y + 109, lines[2])
    out.append("</g>")
    return out


def flow(pid, d, label, sub, label_y, delay):
    return [
        f'<path id="{pid}" class="e" style="animation-delay:{delay}s" d="{d}" pathLength="1" '
        f'fill="none" stroke="{ACCENT}" stroke-opacity=".7" stroke-width="1.6"/>',
        f'<g class="n" style="animation-delay:{delay + 0.3}s">',
        f'<text x="320" y="{label_y}" fill="{TEXT}" font-size="11" font-weight="600" text-anchor="middle">{label}</text>',
        f'<text x="320" y="{label_y + 14}" fill="{MUTED}" font-size="10" text-anchor="middle">{sub}</text>',
        "</g>",
    ] + [
        f'<circle r="3.2" fill="{ACCENT}" opacity="0">'
        f'<set attributeName="opacity" to="1" begin="{delay + 0.9 + i * 1.1:.1f}s"/>'
        f'<animateMotion dur="2.2s" repeatCount="indefinite" begin="{delay + 0.9 + i * 1.1:.1f}s">'
        f'<mpath href="#{pid}" xlink:href="#{pid}"/></animateMotion></circle>'
        for i in range(2)
    ]


def link(d, delay, pid=None):
    id_attr = f' id="{pid}"' if pid else ""
    out = [
        f'<g class="n" style="animation-delay:{delay}s">',
        f'<path class="p"{id_attr} d="{d}" fill="none" stroke="{LINK}" '
        'stroke-width="1.6" stroke-dasharray="4 4"/>',
        "</g>",
    ]
    if pid:
        begin = delay + 0.9
        out.append(
            f'<circle r="2.6" fill="{MUTED}" opacity="0">'
            f'<set attributeName="opacity" to=".9" begin="{begin:.1f}s"/>'
            f'<animateMotion dur="2.6s" repeatCount="indefinite" begin="{begin:.1f}s">'
            f'<mpath href="#{pid}" xlink:href="#{pid}"/></animateMotion></circle>'
        )
    return out


def render(t):
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{t["aria"]}">',
        "<style>",
        f"text{{font-family:{FONT};}}",
        ".n{opacity:0;animation:up .6s cubic-bezier(.2,.8,.3,1) forwards;}",
        ".e{stroke-dasharray:1;stroke-dashoffset:1;animation:draw .8s ease-out forwards;}",
        ".p{animation:pulse 2.4s ease-in-out 2s infinite;}",
        "@keyframes up{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:none;}}",
        "@keyframes draw{to{stroke-dashoffset:0;}}",
        "@keyframes pulse{50%{stroke-opacity:.35;}}",
        "@media (prefers-reduced-motion:reduce){.n,.e,.p{animation:none;opacity:1;stroke-dashoffset:0;}}",
        "</style>",
        "<defs>",
        '<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">'
        f'<feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="{ACCENT}" flood-opacity=".35"/></filter>',
        "</defs>",
        f'<rect width="{W}" height="{H}" rx="4.5" fill="{BG}"/>',
        f'<text x="30" y="38" fill="{ACCENT}" font-size="18" font-weight="600">{t["title"]}</text>',
        f'<text x="30" y="60" fill="{MUTED}" font-size="12">{t["subtitle"]}</text>',
        f'<g fill="{MUTED}" font-size="10.5">',
        f'<path d="M{W - 250},34 h22" stroke="{ACCENT}" stroke-width="1.6"/>',
        f'<text x="{W - 222}" y="38">{t["legend_flow"]}</text>',
        f'<path d="M{W - 130},34 h22" stroke="{LINK}" stroke-width="1.6" stroke-dasharray="4 4"/>',
        f'<text x="{W - 102}" y="38">{t["legend_link"]}</text>',
        "</g>",
    ]
    out += node("tm", "TuMatch / Orkezto", t["built"], t["tm"], 0.1)
    out += node("pr", "Propirent", t["contrib"], t["pr"], 0.2)
    out += node("nu", "Numinap", t["lead"], t["nu"], 0.3, hub=True)
    out += node("orv", "Orvyt", t["contrib"], t["orv"], 0.4)
    out += node("prop", "Propital", t["head"], t["prop"], 0.5)
    out += flow("ea", EDGE_A, *t["edge_a"], 122, 0.8)
    out += flow("eb", EDGE_B, *t["edge_b"], 356, 1.0)
    out += link(LINK_C, 1.1, "lc")
    out += link(LINK_E, 1.2, "le")
    out += link(LINK_D, 1.3)

    x, y, w, h = MS
    out += [
        '<g class="n" style="animation-delay:1.4s">',
        f'<path d="M30,{y - 22} H{W - 30}" stroke="{BORDER}" stroke-dasharray="2 5"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{CARD}" stroke="{BORDER}"/>',
        *chip(x + 14, y + 14, t["own"]),
        f'<text x="{x + 14}" y="{y + 60}" fill="{NAME}" font-size="16" font-weight="600">MiSUPER</text>',
        f'<text x="{x + 200}" y="{y + 36}" fill="{TEXT}" font-size="11.5">{t["ms"][0]}</text>',
        *live(x + 200, y + 58, t["ms"][1]),
        "</g>",
        "</svg>",
    ]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for lang, t in TEXTS.items():
        t = {k: escape_all(v) for k, v in t.items()}
        path = PROFILE / f"ecosystem-{lang}.svg"
        path.write_text(render(t), encoding="utf-8")
        print(f"wrote {path}")
