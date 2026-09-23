"""Render the animated product-ecosystem diagram (profile/ecosystem-{es,en}.svg)."""
from html import escape, unescape
from pathlib import Path

PROFILE = Path(__file__).resolve().parent.parent / "profile"

W, H = 920, 562
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
        "legend_plan": "en desarrollo",
        "built": "DISEÑÉ Y CONSTRUÍ",
        "lead": "COORDINO",
        "contrib": "CONTRIBUYO",
        "head": "LIDERO PRODUCTO & OPS",
        "own": "DESARROLLO PROPIO",
        "tm": ["CRM inmobiliario multi-marca", "leads · propiedades · cobranzas", "en producción · 6 APIs externas"],
        "pr": ["Gestión de propiedades", "integración propia hacia Numinap", None],
        "nu": ["Planificación patrimonial", "patrimonio del inversionista", "integraciones en producción"],
        "orv": ["Sistema para inmobiliarias", "pagos · mensajería · postventa", "en producción"],
        "prop": ["Sistema para brokers inmobiliarios", "producto y operaciones del grupo", None],
        "ms": ["Gestión para kioscos y comercios minoristas: ventas, stock e inventario",
               "demo en vivo · Next.js · TypeScript · Supabase"],
        "edge_a": ("link de referido", "corredor → cliente"),
        "edge_b": ("flujo de caja", "propiedad → patrimonio"),
        "edge_e": ("etapa de inversión", "operaciones del cliente"),
        "plan_d": ("catálogos de inmobiliarias", "en desarrollo"),
        "plan_f": "catálogos compartidos · en desarrollo",
        "aria": "Diagrama del ecosistema Grupo Propital: TuMatch/Orkezto, Propirent y Propital envían datos a Numinap; "
                "Orvyt se integra con Numinap. En desarrollo: catálogos compartidos entre Propital, Orvyt y TuMatch/Orkezto. Aparte, MiSUPER, desarrollo propio",
    },
    "en": {
        "title": "Grupo Propital ecosystem",
        "subtitle": "How the products I build and lead connect",
        "legend_flow": "data flow",
        "legend_link": "integration",
        "legend_plan": "in progress",
        "built": "DESIGNED & BUILT",
        "lead": "LEAD",
        "contrib": "CONTRIBUTOR",
        "head": "HEAD OF PRODUCT & OPS",
        "own": "PERSONAL PROJECT",
        "tm": ["Multi-brand real-estate CRM", "leads · properties · billing", "in production · 6 external APIs"],
        "pr": ["Property management", "own integration into Numinap", None],
        "nu": ["Wealth planning", "investor net worth", "integrations in production"],
        "orv": ["Platform for real-estate agencies", "payments · messaging · after-sales", "in production"],
        "prop": ["Platform for real-estate brokers", "group-wide product & operations", None],
        "ms": ["Management system for kiosks and small retailers: sales, stock and inventory",
               "live demo · Next.js · TypeScript · Supabase"],
        "edge_a": ("referral link", "broker → client"),
        "edge_b": ("cash flow", "property → net worth"),
        "edge_e": ("investment stage", "client operations"),
        "plan_d": ("agency catalogs", "in progress"),
        "plan_f": "shared catalogs · in progress",
        "aria": "Grupo Propital ecosystem diagram: TuMatch/Orkezto, Propirent and Propital send data to Numinap; "
                "Orvyt integrates with Numinap. In progress: shared catalogs between Propital, Orvyt and TuMatch/Orkezto. Separately, MiSUPER, a personal project",
    },
}

NODES = {
    "pr": (30, 90, 220, 118),
    "tm": (30, 270, 220, 118),
    "nu": (360, 180, 200, 118),
    "orv": (670, 90, 220, 118),
    "prop": (670, 270, 220, 118),
}

EDGE_A = "M250,149 C305,149 305,225 360,225"
EDGE_B = "M250,329 C305,329 305,253 360,253"
LINK_C = "M670,149 C615,149 615,225 560,225"
PLAN_D = "M780,208 V270"
PLAN_F = "M140,388 V404 Q140,414 150,414 H770 Q780,414 780,404 V388"
EDGE_E = "M670,329 C615,329 615,253 560,253"

MS = (30, 462, 860, 80)


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


def flow(pid, d, label, sub, label_x, label_y, delay):
    return [
        f'<path id="{pid}" class="e" style="animation-delay:{delay}s" d="{d}" pathLength="1" '
        f'fill="none" stroke="{ACCENT}" stroke-opacity=".7" stroke-width="1.6"/>',
        f'<g class="n" style="animation-delay:{delay + 0.3}s">',
        f'<text x="{label_x}" y="{label_y}" fill="{TEXT}" font-size="11" font-weight="600" text-anchor="middle">{label}</text>',
        f'<text x="{label_x}" y="{label_y + 14}" fill="{MUTED}" font-size="10" text-anchor="middle">{sub}</text>',
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


def planned(d, delay):
    return [
        f'<g class="n" style="animation-delay:{delay}s">',
        f'<path class="p" d="{d}" fill="none" stroke="{ACCENT}" stroke-opacity=".55" '
        'stroke-width="1.6" stroke-dasharray="6 5"/>',
        "</g>",
    ]


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
        f'<path d="M{W - 380},34 h22" stroke="{ACCENT}" stroke-width="1.6"/>',
        f'<text x="{W - 352}" y="38">{t["legend_flow"]}</text>',
        f'<path d="M{W - 260},34 h22" stroke="{LINK}" stroke-width="1.6" stroke-dasharray="4 4"/>',
        f'<text x="{W - 232}" y="38">{t["legend_link"]}</text>',
        f'<path d="M{W - 150},34 h22" stroke="{ACCENT}" stroke-opacity=".55" stroke-width="1.6" stroke-dasharray="6 5"/>',
        f'<text x="{W - 122}" y="38">{t["legend_plan"]}</text>',
        "</g>",
    ]
    out += node("tm", "TuMatch / Orkezto", t["built"], t["tm"], 0.1)
    out += node("pr", "Propirent", t["contrib"], t["pr"], 0.2)
    out += node("nu", "Numinap", t["lead"], t["nu"], 0.3, hub=True)
    out += node("orv", "Orvyt", t["contrib"], t["orv"], 0.4)
    out += node("prop", "Propital", t["head"], t["prop"], 0.5)
    out += flow("eb", EDGE_A, *t["edge_b"], 305, 122, 0.8)
    out += flow("ea", EDGE_B, *t["edge_a"], 305, 356, 1.0)
    out += flow("ee", EDGE_E, *t["edge_e"], 615, 356, 1.2)
    out += link(LINK_C, 1.1, "lc")
    out += planned(PLAN_D, 1.4)
    out += [
        '<g class="n" style="animation-delay:1.6s">',
        f'<text x="770" y="236" fill="{TEXT}" font-size="11" font-weight="600" text-anchor="end">{t["plan_d"][0]}</text>',
        f'<text x="770" y="250" fill="{MUTED}" font-size="10" text-anchor="end">{t["plan_d"][1]}</text>',
        "</g>",
    ]
    out += planned(PLAN_F, 1.5)
    label_w = len(unescape(t["plan_f"])) * 5.6 + 24
    out += [
        '<g class="n" style="animation-delay:1.7s">',
        f'<rect x="{460 - label_w / 2:.0f}" y="405" width="{label_w:.0f}" height="18" fill="{BG}"/>',
        f'<text x="460" y="418" fill="{TEXT}" font-size="10.5" text-anchor="middle">{t["plan_f"]}</text>',
        "</g>",
    ]

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
