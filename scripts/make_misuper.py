"""Render the animated MiSUPER showcase (profile/misuper-{es,en}.svg) from the screenshots in assets/."""
import base64
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESKTOP = ROOT / "assets" / "misuper-desktop.jpg"
MOBILE = ROOT / "assets" / "misuper-mobile.jpg"

W, H = 920, 470
BG = "#0a0a0a"
DEVICE = "#1c1c1f"
DEVICE_EDGE = "#3f3f46"
ACCENT = "#f97316"
BRAND = "#e8a33a"
NAME = "#f5f5f5"
TEXT = "#c9c9d3"
MUTED = "#a1a1aa"
LIVE = "#22c55e"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif"

TEXTS = {
    "es": {
        "chip": "DESARROLLO PROPIO",
        "tagline": ["Punto de venta y gestión para", "kioscos y comercios minoristas"],
        "features": [
            "Cobro rápido con escáner y atajos de teclado",
            "Inventario y control de stock",
            "Caja, pedidos, clientes y reportes",
            "IA Insights y marketplace",
            "Web y mobile: un mismo sistema",
        ],
        "live": "demo en vivo",
        "cta": "Probalo en misuper.ar →",
        "aria": "MiSUPER, desarrollo propio: punto de venta y gestión para kioscos, mostrado en notebook y celular",
    },
    "en": {
        "chip": "PERSONAL PROJECT",
        "tagline": ["Point of sale and management for", "kiosks and small retailers"],
        "features": [
            "Fast checkout with scanner and shortcuts",
            "Inventory and stock control",
            "Cash register, orders, customers, reports",
            "AI insights and marketplace",
            "Desktop and mobile: one system",
        ],
        "live": "live demo",
        "cta": "Try it at misuper.ar →",
        "aria": "MiSUPER, personal project: point of sale and management for kiosks, shown on a laptop and a phone",
    },
}

LAP_X, LAP_Y = 372, 44
SCREEN_W, SCREEN_H = 432, 270
BEZEL = 12
PH_X, PH_Y = 752, 128
PH_SCREEN_W = 140
PH_SCREEN_H = round(PH_SCREEN_W * 649 / 300)
PH_BEZEL = 7


def data_uri(path):
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()


def render(t, desktop, mobile):
    t = {k: [escape(x) for x in v] if isinstance(v, list) else escape(v) for k, v in t.items()}
    sx, sy = LAP_X + BEZEL, LAP_Y + BEZEL
    lap_w, lap_h = SCREEN_W + 2 * BEZEL, SCREEN_H + 2 * BEZEL
    base_y = LAP_Y + lap_h
    base_l, base_r = LAP_X - 34, LAP_X + lap_w + 34
    px, py = PH_X + PH_BEZEL, PH_Y + PH_BEZEL
    ph_w, ph_h = PH_SCREEN_W + 2 * PH_BEZEL, PH_SCREEN_H + 2 * PH_BEZEL

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{t["aria"]}">',
        "<style>",
        f"text{{font-family:{FONT};}}",
        ".f{opacity:0;animation:up .7s cubic-bezier(.2,.8,.3,1) forwards;}",
        ".lap{opacity:0;animation:rise 1s cubic-bezier(.2,.8,.3,1) .2s forwards;}",
        ".ph{opacity:0;animation:slide 1s cubic-bezier(.2,.8,.3,1) .7s forwards;}",
        ".float{animation:float 5s ease-in-out 1.8s infinite;}",
        ".shine{animation:shine 1.6s ease-in-out 1.2s forwards;}",
        "@keyframes up{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:none;}}",
        "@keyframes rise{from{opacity:0;transform:translateY(24px) scale(.97);}to{opacity:1;transform:none;}}",
        "@keyframes slide{from{opacity:0;transform:translate(40px,20px);}to{opacity:1;transform:none;}}",
        "@keyframes float{50%{transform:translateY(-6px);}}",
        f"@keyframes shine{{from{{transform:translateX(-160px);}}to{{transform:translateX({SCREEN_W + 160}px);}}}}",
        "@media (prefers-reduced-motion:reduce){.f,.lap,.ph{animation:none;opacity:1;}.float,.shine{animation:none;}}",
        "</style>",
        "<defs>",
        f'<clipPath id="scr"><rect x="{sx}" y="{sy}" width="{SCREEN_W}" height="{SCREEN_H}" rx="3"/></clipPath>',
        f'<clipPath id="pscr"><rect x="{px}" y="{py}" width="{PH_SCREEN_W}" height="{PH_SCREEN_H}" rx="17"/></clipPath>',
        '<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
        f'<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{BRAND}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{BRAND}" stop-opacity="0"/></radialGradient>',
        '<filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">'
        '<feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#000" flood-opacity=".6"/></filter>',
        "</defs>",
        f'<rect width="{W}" height="{H}" rx="4.5" fill="{BG}"/>',
        f'<ellipse cx="{LAP_X + lap_w / 2 + 40}" cy="{LAP_Y + lap_h / 2 + 30}" rx="330" ry="210" fill="url(#glow)"/>',
    ]

    chip_w = len(unescape(t["chip"])) * 6.4 + 16
    feats_y = 196
    out += [
        '<g class="f" style="animation-delay:.1s">',
        f'<rect x="30" y="44" width="{chip_w:.0f}" height="18" rx="9" fill="none" stroke="{ACCENT}" stroke-opacity=".55"/>',
        f'<text x="{30 + chip_w / 2:.0f}" y="57" fill="{ACCENT}" font-size="9.5" font-weight="600" '
        f'letter-spacing=".6" text-anchor="middle">{t["chip"]}</text>',
        "</g>",
        '<g class="f" style="animation-delay:.25s">',
        f'<text x="28" y="112" fill="{NAME}" font-size="42" font-weight="700" letter-spacing="-1">Mi<tspan fill="{BRAND}">SUPER</tspan></text>',
        "</g>",
        '<g class="f" style="animation-delay:.4s">',
        f'<text x="30" y="142" fill="{TEXT}" font-size="14">{t["tagline"][0]}</text>',
        f'<text x="30" y="161" fill="{TEXT}" font-size="14">{t["tagline"][1]}</text>',
        "</g>",
    ]
    for i, feat in enumerate(t["features"]):
        y = feats_y + i * 27
        out += [
            f'<g class="f" style="animation-delay:{0.6 + i * 0.12:.2f}s">',
            f'<rect x="30" y="{y - 11}" width="14" height="14" rx="4" fill="{BRAND}" fill-opacity=".15" stroke="{BRAND}" stroke-opacity=".6"/>',
            f'<path d="M33.5,{y - 4} l2.6,2.6 l4.6,-5" fill="none" stroke="{BRAND}" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round"/>',
            f'<text x="54" y="{y}" fill="{TEXT}" font-size="12.5">{feat}</text>',
            "</g>",
        ]
    tail_y = feats_y + len(t["features"]) * 27 + 14
    out += [
        f'<g class="f" style="animation-delay:{0.6 + len(t["features"]) * 0.12 + 0.1:.2f}s">',
        f'<circle cx="34" cy="{tail_y - 4}" r="3" fill="{LIVE}"/>',
        f'<text x="43" y="{tail_y}" fill="{MUTED}" font-size="11">{t["live"]} · Next.js · TypeScript · Supabase</text>',
        f'<rect x="30" y="{tail_y + 18}" width="{len(unescape(t["cta"])) * 7.4 + 28:.0f}" height="34" rx="17" fill="{BRAND}"/>',
        f'<text x="{30 + (len(unescape(t["cta"])) * 7.4 + 28) / 2:.0f}" y="{tail_y + 40}" fill="#1a1204" font-size="13" '
        f'font-weight="700" text-anchor="middle">{t["cta"]}</text>',
        "</g>",
    ]

    out += [
        '<g class="lap"><g filter="url(#shadow)">',
        f'<rect x="{LAP_X}" y="{LAP_Y}" width="{lap_w}" height="{lap_h}" rx="12" fill="{DEVICE}" stroke="{DEVICE_EDGE}"/>',
        f'<circle cx="{LAP_X + lap_w / 2}" cy="{LAP_Y + 6}" r="1.8" fill="{DEVICE_EDGE}"/>',
        f'<path d="M{base_l},{base_y} H{base_r} L{base_r - 14},{base_y + 14} H{base_l + 14} Z" fill="#26262a" stroke="{DEVICE_EDGE}"/>',
        f'<rect x="{LAP_X + lap_w / 2 - 36}" y="{base_y}" width="72" height="5" rx="2.5" fill="#18181b"/>',
        "</g>",
        f'<image x="{sx}" y="{sy}" width="{SCREEN_W}" height="{SCREEN_H}" preserveAspectRatio="xMidYMid slice" '
        f'clip-path="url(#scr)" href="{desktop}" xlink:href="{desktop}"/>',
        f'<g clip-path="url(#scr)"><rect class="shine" x="{sx - 160}" y="{sy}" width="160" height="{SCREEN_H}" '
        'fill="url(#sh)" transform="translate(-160 0)"/></g>',
        "</g>",
        '<g class="ph"><g class="float"><g filter="url(#shadow)">',
        f'<rect x="{PH_X}" y="{PH_Y}" width="{ph_w}" height="{ph_h}" rx="24" fill="{DEVICE}" stroke="{DEVICE_EDGE}"/>',
        "</g>",
        f'<image x="{px}" y="{py}" width="{PH_SCREEN_W}" height="{PH_SCREEN_H}" preserveAspectRatio="xMidYMid slice" '
        f'clip-path="url(#pscr)" href="{mobile}" xlink:href="{mobile}"/>',
        f'<rect x="{PH_X + ph_w / 2 - 22}" y="{PH_Y + 12}" width="44" height="11" rx="5.5" fill="#050505"/>',
        "</g></g>",
        "</svg>",
    ]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    desktop, mobile = data_uri(DESKTOP), data_uri(MOBILE)
    for lang, t in TEXTS.items():
        path = ROOT / "profile" / f"misuper-{lang}.svg"
        path.write_text(render(t, desktop, mobile), encoding="utf-8")
        print(f"wrote {path} ({path.stat().st_size // 1024} KB)")
