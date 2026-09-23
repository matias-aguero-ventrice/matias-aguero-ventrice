"""Turn a photo into an animated ASCII-portrait SVG (profile/portrait.svg).

Usage: python scripts/make_portrait.py path/to/photo.jpg [head_frac]
head_frac: fraction of the subject's height to keep from the top (default 0.8).
Needs scripts/requirements-portrait.txt; only run when the photo changes.
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import new_session, remove

OUT = Path(__file__).resolve().parent.parent / "profile" / "portrait.svg"

RAMP = " .`:-=+*cs#%@"
COLS = 110
FONT_SIZE = 6.4
CHAR_W = 3.84
LINE_H = 6.72
PAD = 24
TOP = 46
GAMMA = 0.9

BG = "#0a0a0a"
INK = "#fde7d4"
ACCENT = "#f97316"
MUTED = "#a1a1aa"
USER_HOST = "matias@github"
PROMPT = " ~ $ whoami"


def prep(path, head_frac):
    rgba = remove(Image.open(path).convert("RGB"), session=new_session("u2net_human_seg"))
    rgba = np.array(rgba)
    alpha = rgba[:, :, 3].astype(np.float32) / 255

    ys, _ = np.where(alpha > 0.5)
    y0 = ys.min()
    y1 = int(y0 + (ys.max() - y0) * head_frac)
    xs = np.where(alpha[y0:y1].max(axis=0) > 0.5)[0]
    rgb = np.ascontiguousarray(rgba[y0:y1, xs.min():xs.max() + 1, :3])
    alpha = alpha[y0:y1, xs.min():xs.max() + 1]

    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    lab[:, :, 0] = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6, 6)).apply(lab[:, :, 0])
    gray = cv2.cvtColor(cv2.cvtColor(lab, cv2.COLOR_LAB2RGB), cv2.COLOR_RGB2GRAY)
    return gray.astype(np.float32), alpha


def to_ascii(gray, alpha):
    h, w = gray.shape
    rows = round(COLS * (h / w) * (CHAR_W / LINE_H))
    gray = cv2.resize(gray, (COLS, rows), interpolation=cv2.INTER_AREA)
    mask = cv2.resize(alpha, (COLS, rows), interpolation=cv2.INTER_AREA) > 0.5

    lo, hi = np.percentile(gray[mask], [2, 98])
    v = np.clip((gray - lo) / (hi - lo), 0, 1) ** GAMMA
    # bright -> dense; every subject cell gets at least RAMP[1] so the silhouette survives
    idx = np.where(mask, 1 + (v * (len(RAMP) - 2)).round().astype(int), 0)
    lines = ["".join(RAMP[i] for i in row).rstrip() for row in idx]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(lines):
    width = round(PAD * 2 + COLS * CHAR_W)
    height = round(TOP + len(lines) * LINE_H + PAD)
    row_dur = 0.28
    stagger = 0.045
    mono = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="Retrato ASCII de Matías Agüero Ventrice">',
        f"<style>text{{font-family:{mono};white-space:pre;}}</style>",
        f'<rect width="{width}" height="{height}" rx="4.5" fill="{BG}"/>',
        f'<text x="{PAD}" y="28" fill="{MUTED}" font-size="12">'
        f'<tspan fill="{ACCENT}">{USER_HOST}</tspan>{PROMPT}</text>',
        "<defs>",
    ]
    for i in range(len(lines)):
        begin = 0.3 + i * stagger
        y = TOP + i * LINE_H
        out.append(
            f'<clipPath id="r{i}"><rect x="{PAD}" y="{y}" width="0" height="{LINE_H}">'
            f'<animate attributeName="width" from="0" to="{COLS * CHAR_W}" begin="{begin:.3f}s" '
            f'dur="{row_dur}s" fill="freeze"/></rect></clipPath>'
        )
    out.append("</defs>")

    for i, line in enumerate(lines):
        if not line.strip():
            continue
        begin = 0.3 + i * stagger
        y = TOP + i * LINE_H
        out.append(
            f'<text clip-path="url(#r{i})" x="{PAD}" y="{y + LINE_H - 1.6:.1f}" fill="{INK}" '
            f'font-size="{FONT_SIZE}" textLength="{len(line) * CHAR_W:.1f}" lengthAdjust="spacing">'
            f"{esc(line)}</text>"
        )
        out.append(
            f'<rect x="{PAD}" y="{y}" width="{CHAR_W}" height="{LINE_H}" fill="{INK}" opacity="0">'
            f'<set attributeName="opacity" to="0.9" begin="{begin:.3f}s"/>'
            f'<animate attributeName="x" from="{PAD}" to="{PAD + COLS * CHAR_W}" begin="{begin:.3f}s" '
            f'dur="{row_dur}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0" begin="{begin + row_dur:.3f}s"/></rect>'
        )

    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    head_frac = float(sys.argv[2]) if len(sys.argv) == 3 else 0.8
    lines = to_ascii(*prep(sys.argv[1], head_frac))
    OUT.write_text(render(lines), encoding="utf-8")
    print(f"wrote {OUT} ({len(lines)} rows)")
