import json
import os
import sys
import urllib.request
from collections import Counter
from html import escape
from pathlib import Path

LOGIN = "matias-aguero-ventrice"
OUT = Path(__file__).resolve().parent.parent / "profile" / "langs.svg"
TOP = 6

QUERY = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    repositories(first: 100, after: $cursor, ownerAffiliations: OWNER, isFork: false) {
      pageInfo { hasNextPage endCursor }
      nodes {
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""

W, H = 350, 195
BG = "#0a0a0a"
TITLE = "#f97316"
TEXT = "#c9c9d3"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif"


def fetch(token):
    sizes, colors, cursor = Counter(), {}, None
    while True:
        body = json.dumps({"query": QUERY, "variables": {"login": LOGIN, "cursor": cursor}}).encode()
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=body,
            headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
        if "errors" in payload:
            sys.exit(f"GraphQL error: {payload['errors']}")
        repos = payload["data"]["user"]["repositories"]
        for repo in repos["nodes"]:
            for edge in repo["languages"]["edges"]:
                name = edge["node"]["name"]
                sizes[name] += edge["size"]
                colors[name] = edge["node"]["color"] or "#71717a"
        if not repos["pageInfo"]["hasNextPage"]:
            return sizes, colors
        cursor = repos["pageInfo"]["endCursor"]


def render(sizes, colors):
    total = sum(sizes.values())
    top = sizes.most_common(TOP)
    bar_x, bar_w = 25, W - 50
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        'role="img" aria-label="Most used languages">',
        "<style>",
        f"text{{font-family:{FONT};}}",
        ".n{opacity:0;animation:up .5s ease-out forwards;}",
        ".bar{transform-box:view-box;transform-origin:25px 0;transform:scaleX(0);animation:grow 1s ease-out .2s forwards;}",
        "@keyframes up{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:none;}}",
        "@keyframes grow{to{transform:scaleX(1);}}",
        "@media (prefers-reduced-motion:reduce){.n{animation:none;opacity:1;}.bar{animation:none;transform:none;}}",
        "</style>",
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="4.5" fill="{BG}"/>',
        f'<text x="25" y="35" fill="{TITLE}" font-size="18" font-weight="600">Most Used Languages</text>',
        f'<clipPath id="bar"><rect x="{bar_x}" y="55" width="{bar_w}" height="8" rx="4"/></clipPath>',
        '<g class="bar" clip-path="url(#bar)">',
    ]
    x = bar_x
    for name, size in top:
        w = bar_w * size / total
        out.append(f'<rect x="{x:.2f}" y="55" width="{w + 0.5:.2f}" height="8" fill="{colors[name]}"/>')
        x += w
    out.append(f'<rect x="{x:.2f}" y="55" width="{bar_x + bar_w - x:.2f}" height="8" fill="#3f3f46"/>')
    out.append("</g>")
    for i, (name, size) in enumerate(top):
        col, row = i % 2, i // 2
        lx, ly = 25 + col * 160, 95 + row * 30
        out += [
            f'<g class="n" style="animation-delay:{0.4 + i * 0.08:.2f}s">',
            f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{colors[name]}"/>',
            f'<text x="{lx + 16}" y="{ly}" fill="{TEXT}" font-size="12">{escape(name)} {100 * size / total:.2f}%</text>',
            "</g>",
        ]
    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    token = os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("GH_TOKEN is required")
    OUT.write_text(render(*fetch(token)), encoding="utf-8")
    print(f"wrote {OUT}")
