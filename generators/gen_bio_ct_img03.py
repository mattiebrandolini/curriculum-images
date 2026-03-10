#!/usr/bin/env python3
"""
Generator: Bio Checkpoint 13 - Cell Transport - Image 03
Concept: Concentration Gradient — molecules move from HIGH to LOW
Three stages: Clustered → Spreading → Equal (equilibrium)
"""

import sys, itertools, random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from svg_base import *


def gen():
    width, height = 800, 445
    c = ""

    # ── Title ──────────────────────────────────────────────────────────
    c += text(400, 32, "Concentration Gradient", size=20,
              color=COLORS["dark_gray"], bold=True)
    c += text(400, 52, "Molecules always move: HIGH → LOW",
              size=13, color=COLORS["medium_gray"])

    # ── Layout ─────────────────────────────────────────────────────────
    panel_w = 218
    panel_h = 300
    gap     = 23
    pxs     = [50, 50 + panel_w + gap, 50 + 2 * (panel_w + gap)]
    py      = 68
    mol_r   = 7
    mol_fill = "#7b1fa2"
    mol_line = "#4a148c"

    panel_defs = [
        {"title": "1. Clustered",  "color": "orange"},
        {"title": "2. Spreading",  "color": "teal"},
        {"title": "3. Equal",      "color": "blue"},
    ]

    # ── Panel shells ────────────────────────────────────────────────────
    for i, cfg in enumerate(panel_defs):
        x  = pxs[i]
        cl = COLORS.get(cfg["color"], COLORS["blue"])
        bg = COLORS.get(f"light_{cfg['color']}", "#e3f2fd")
        c += rect(x, py, panel_w, panel_h, fill=bg, stroke=cl, rx=8)
        # header bar — draw with rx then cover rounded bottom
        c += f'  <rect x="{x}" y="{py}" width="{panel_w}" height="40" fill="{cl}" rx="8"/>\n'
        c += f'  <rect x="{x}" y="{py+26}" width="{panel_w}" height="14" fill="{cl}" rx="0"/>\n'
        c += text(x + panel_w // 2, py + 27, cfg["title"],
                  size=14, color="white", bold=True)

    # ══════════════════════════════════════════════════════════════════
    # PANEL 1 — Clustered  (many left, few right)
    # ══════════════════════════════════════════════════════════════════
    x1  = pxs[0]
    mid = x1 + panel_w // 2

    # dashed divider
    c += (f'  <line x1="{mid}" y1="{py+40}" x2="{mid}" y2="{py+panel_h-28}"'
          f' stroke="#bbb" stroke-width="1.5" stroke-dasharray="5,4"/>\n')

    # HIGH side — 17 molecules
    high = [
        (x1+22, py+68),  (x1+52, py+55),  (x1+82, py+70),
        (x1+28, py+103), (x1+60, py+92),  (x1+90, py+108),
        (x1+20, py+140), (x1+55, py+130), (x1+88, py+145),
        (x1+32, py+175), (x1+65, py+165), (x1+95, py+180),
        (x1+25, py+210), (x1+58, py+200), (x1+92, py+215),
        (x1+38, py+245), (x1+70, py+238),
    ]
    for mx, my in high:
        c += circle(mx, my, mol_r, fill=mol_fill, stroke=mol_line, sw=1)

    # LOW side — 3 molecules
    for mx, my in [(x1+138, py+80), (x1+172, py+165), (x1+150, py+242)]:
        c += circle(mx, my, mol_r, fill=mol_fill, stroke=mol_line, sw=1)

    # Tiny perfume bottle (source icon)
    bx, by = x1 + 154, py + 44
    c += rect(bx, by, 16, 22, fill="#e0e0e0", stroke="#999", rx=3)
    c += f'  <line x1="{bx+16}" y1="{by+5}" x2="{bx+26}" y2="{by+5}" stroke="#999" stroke-width="2"/>\n'
    c += f'  <line x1="{bx+26}" y1="{by+5}" x2="{bx+26}" y2="{by+15}" stroke="#999" stroke-width="2"/>\n'
    for sdx, sdy in [(30,43),(35,48),(30,53),(39,45),(39,51)]:
        c += f'  <circle cx="{bx+sdx}" cy="{py+sdy}" r="2" fill="{mol_fill}" opacity="0.5"/>\n'

    c += text(mid - 50, py + panel_h - 12, "HIGH", size=12,
              color=COLORS["orange"], bold=True)
    c += text(mid + 50, py + panel_h - 12, "LOW",  size=12,
              color=COLORS["blue"], bold=True)

    # ══════════════════════════════════════════════════════════════════
    # PANEL 2 — Spreading  (molecules in motion, arrows)
    # ══════════════════════════════════════════════════════════════════
    x2 = pxs[1]
    spread = [
        (x2+18, py+65),  (x2+45, py+55),  (x2+30, py+100),
        (x2+80, py+82),  (x2+105, py+115), (x2+92, py+150),
        (x2+72, py+175), (x2+115, py+182),
        (x2+148, py+95),  (x2+172, py+135), (x2+155, py+180),
        (x2+175, py+210),
        (x2+22, py+195),  (x2+58, py+215),  (x2+130, py+232),
        (x2+165, py+248),
    ]
    for mx, my in spread:
        c += circle(mx, my, mol_r, fill=mol_fill, stroke=mol_line, sw=1)

    for ay in [py + 265, py + 280]:
        c += arrow(x2 + 18, ay, x2 + 196, ay, color=COLORS["teal"], width=2)
    c += text(x2 + panel_w // 2, py + panel_h - 12, "Moving →",
              size=12, color=COLORS["teal"], bold=True)

    # ══════════════════════════════════════════════════════════════════
    # PANEL 3 — Equilibrium  (evenly distributed)
    # ══════════════════════════════════════════════════════════════════
    x3 = pxs[2]
    random.seed(42)
    cols = [x3+22, x3+58, x3+96, x3+135, x3+172, x3+206]
    rows = [py+65, py+105, py+145, py+185, py+225, py+262]
    for r, col in itertools.product(rows, cols):
        jx = random.randint(-6, 6)
        jy = random.randint(-5, 5)
        mx, my = col + jx, r + jy
        if x3 + mol_r < mx < x3 + panel_w - mol_r and py + 42 < my < py + panel_h - 22:
            c += circle(mx, my, mol_r, fill=mol_fill, stroke=mol_line, sw=1)

    c += text(x3 + panel_w // 2, py + panel_h - 12, "Equilibrium",
              size=12, color=COLORS["blue"], bold=True)

    # ── "Time passes" bottom arrow ─────────────────────────────────────
    arr_y = py + panel_h + 22
    c += text(400, arr_y + 2, "Time passes", size=12, color=COLORS["medium_gray"])
    c += arrow(pxs[0] + 18, arr_y + 16, pxs[2] + panel_w - 18, arr_y + 16,
               color=COLORS["dark_gray"], width=2)

    # ── Footer ────────────────────────────────────────────────────────
    c += text(400, height - 10,
              "Like perfume spreading across a room",
              size=11, color=COLORS["medium_gray"])

    return make_svg(c, width, height)


if __name__ == "__main__":
    svg = gen()
    out = save_svg(svg, "bio/Checkpoint_13_Cell_Transport_img03.svg")
    print(f"Saved: {out}  ({len(svg):,} bytes)")
