import json
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path

LOGIN = "matias-aguero-ventrice"
OUT = Path(__file__).resolve().parent.parent / "profile" / "heatmap.svg"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""

LEVELS = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
PALETTE = ["#18181b", "#431407", "#9a3412", "#ea580c", "#fb923c"]
MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

BG = "#0a0a0a"
TITLE = "#f97316"
TEXT = "#c9c9d3"
MUTED = "#a1a1aa"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif"

CELL = 11
STEP = 14
LEFT = 58
TOP = 64
PAD = 30


def fetch(token):
    body = json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        sys.exit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def fmt(n):
    return f"{n:,}".replace(",", ".")


def render(calendar):
    weeks = [w["contributionDays"] for w in calendar["weeks"]]
    days = [d for w in weeks for d in w]
    total = calendar["totalContributions"]
    active = sum(1 for d in days if d["contributionCount"] > 0)
    best = max(days, key=lambda d: d["contributionCount"])
    best_date = date.fromisoformat(best["date"])

    grid_h = 7 * STEP
    grid_right = LEFT + len(weeks) * STEP - (STEP - CELL)
    width = grid_right + PAD
    height = TOP + grid_h + 58
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{total} contribuciones en el último año">',
        "<style>",
        f"text{{font-family:{FONT};}}",
        ".c{transform-box:fill-box;transform-origin:center;opacity:0;"
        "animation:pop .45s cubic-bezier(.2,.9,.3,1.3) forwards;}",
        ".f{opacity:0;animation:fade .6s ease-out forwards;}",
        "@keyframes pop{from{opacity:0;transform:translateY(-6px) scale(.4);}"
        "to{opacity:1;transform:none;}}",
        "@keyframes fade{to{opacity:1;}}",
        "@media (prefers-reduced-motion:reduce){.c,.f{animation:none;opacity:1;}}",
        "</style>",
        f'<rect width="{width}" height="{height}" rx="4.5" fill="{BG}"/>',
        f'<text x="{LEFT - 28}" y="32" fill="{TITLE}" font-size="18" font-weight="600">'
        f"Contribuciones · último año</text>",
    ]

    last_month = None
    last_label_col = -10
    for col, week in enumerate(weeks):
        month = date.fromisoformat(week[0]["date"]).month
        if month != last_month:
            if col - last_label_col >= 3 and col <= len(weeks) - 2:
                parts.append(
                    f'<text x="{LEFT + col * STEP}" y="{TOP - 10}" fill="{MUTED}" font-size="11">'
                    f"{MONTHS[month - 1]}</text>"
                )
                last_label_col = col
            last_month = month

    for row, label in ((1, "Lun"), (3, "Mié"), (5, "Vie")):
        parts.append(
            f'<text x="{LEFT - 28}" y="{TOP + row * STEP + CELL - 1}" fill="{MUTED}" font-size="11">'
            f"{label}</text>"
        )

    for col, week in enumerate(weeks):
        for d in week:
            row = date.fromisoformat(d["date"]).isoweekday() % 7
            color = PALETTE[LEVELS.index(d["contributionLevel"])]
            delay = (col + row) * 14
            n = d["contributionCount"]
            tip = f"{n} contribución" if n == 1 else f"{n} contribuciones"
            parts.append(
                f'<rect class="c" style="animation-delay:{delay}ms" x="{LEFT + col * STEP}" '
                f'y="{TOP + row * STEP}" width="{CELL}" height="{CELL}" rx="2.5" fill="{color}">'
                f'<title>{tip} el {d["date"]}</title></rect>'
            )

    footer_y = TOP + grid_h + 30
    reveal = (len(weeks) + 7) * 14
    summary = (
        f'<tspan fill="{TITLE}" font-weight="600">{fmt(total)}</tspan> contribuciones'
        f'  ·  mejor día: <tspan fill="{TITLE}" font-weight="600">{best["contributionCount"]}</tspan>'
        f" ({best_date.day} {MONTHS[best_date.month - 1]} {best_date.year})"
        f'  ·  días activos: <tspan fill="{TITLE}" font-weight="600">{active}</tspan>/{len(days)}'
    )
    parts.append(
        f'<text class="f" style="animation-delay:{reveal}ms" x="{LEFT - 28}" y="{footer_y}" '
        f'fill="{TEXT}" font-size="13">{summary}</text>'
    )

    legend_x = grid_right - 26 - len(PALETTE) * STEP
    legend = [
        f'<g class="f" style="animation-delay:{reveal}ms">',
        f'<text x="{legend_x - 6}" y="{footer_y}" fill="{MUTED}" font-size="11" text-anchor="end">Menos</text>',
    ]
    for i, color in enumerate(PALETTE):
        legend.append(
            f'<rect x="{legend_x + i * STEP}" y="{footer_y - CELL + 1}" width="{CELL}" height="{CELL}" '
            f'rx="2.5" fill="{color}"/>'
        )
    legend.append(
        f'<text x="{grid_right}" y="{footer_y}" fill="{MUTED}" font-size="11" text-anchor="end">Más</text>'
    )
    legend.append("</g>")
    parts.extend(legend)
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    token = os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("GH_TOKEN is required")
    OUT.write_text(render(fetch(token)), encoding="utf-8")
    print(f"wrote {OUT}")
