#!/usr/bin/env python3
"""Generate Simple Diffusion diagram — molecules passing through the membrane."""

import sys, math
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'generators'))
from svg_base import *

def generate():
    width, height = 800, 460
    c = ""

    # Title
    c += text(400, 32, "Simple Diffusion", size=20, color=COLORS["dark_gray"], bold=True)
    c += text(400, 54, "Small, nonpolar molecules pass straight through", size=13, color=COLORS["medium_gray"])

    # --- Concentration labels ---
    c += rect(30, 75, 200, 36, fill=COLORS["light_blue"], stroke=COLORS["blue"], rx=8)
    c += text(130, 99, "HIGH concentration", size=13, color=COLORS["blue"], bold=True)

    c += rect(570, 75, 200, 36, fill=COLORS["light_blue"], stroke=COLORS["blue"], rx=8)
    c += text(670, 99, "LOW concentration", size=13, color=COLORS["blue"], bold=True)

    # Big direction arrow behind membrane
    c += arrow(200, 98, 560, 98, color="#90CAF9", width=3)

    # === PHOSPHOLIPID BILAYER (vertical, center of diagram) ===
    mem_x = 400          # center x of membrane
    mem_w = 60           # total membrane thickness
    mem_top = 120
    mem_bot = 420

    # Membrane background band
    c += rect(mem_x - mem_w//2, mem_top, mem_w, mem_bot - mem_top,
              fill="#FFF3E0", stroke=COLORS["membrane"], rx=0)

    # Draw phospholipid symbols along the two leaflets
    def phospholipid(cx, cy, facing_right=True):
        """Draw a single phospholipid: circle head + two wavy tails."""
        # Head (hydrophilic)
        s = ""
        s += circle(cx, cy, 7, fill=COLORS["membrane"], stroke="#E65100", sw=1)
        # Tails (hydrophobic) — two short lines
        dx = 18 if facing_right else -18
        s += f'  <line x1="{cx}" y1="{cy-3}" x2="{cx+dx}" y2="{cy-5}" stroke="#FFB74D" stroke-width="2" stroke-linecap="round"/>\n'
        s += f'  <line x1="{cx}" y1="{cy+3}" x2="{cx+dx}" y2="{cy+5}" stroke="#FFB74D" stroke-width="2" stroke-linecap="round"/>\n'
        return s

    # Left leaflet (heads face left, tails face right)
    for i in range(10):
        y = mem_top + 15 + i * 30
        c += phospholipid(mem_x - mem_w//2 + 7, y, facing_right=True)

    # Right leaflet (heads face right, tails face left)
    for i in range(10):
        y = mem_top + 15 + i * 30
        c += phospholipid(mem_x + mem_w//2 - 7, y, facing_right=False)

    # Membrane label
    c += text(400, mem_bot + 18, "Cell Membrane", size=13, color="#E65100", bold=True)
    c += text(400, mem_bot + 34, "(phospholipid bilayer)", size=11, color=COLORS["medium_gray"])

    # === MOLECULES PASSING THROUGH ===
    # Each molecule: (label, y_center, color, left_x, right_x)
    molecules = [
        ("O₂",  185, "#43a047"),
        ("CO₂", 270, "#1565c0"),
        ("N₂",  355, "#7b1fa2"),
    ]

    for label, y, col in molecules:
        # Molecule on left (high conc side) — multiple dots to show many
        for dx in [80, 140, 200]:
            c += circle(dx, y, 12, fill=col, stroke="white", sw=2)
            c += text(dx, y + 5, label, size=9, color="white", bold=True)

        # Arrow through membrane
        c += arrow(240, y, 370, y, color=col, width=3)
        # Dashed continuation through membrane
        c += f'  <line x1="{370}" y1="{y}" x2="{430}" y2="{y}" stroke="{col}" stroke-width="2" stroke-dasharray="5,4" />\n'
        # Arrow emerging on right side
        c += arrow(430, y, 560, y, color=col, width=3)

        # Molecule on right (low conc side) — fewer dots
        c += circle(600, y, 12, fill=col, stroke="white", sw=2)
        c += text(600, y + 5, label, size=9, color="white", bold=True)

    # === LEGEND BOX (bottom-left) ===
    c += rect(30, 380, 220, 55, fill="#FAFAFA", stroke="#ddd", rx=6)
    c += text(40, 400, "No energy needed", size=12, color=COLORS["green"], bold=True, anchor="start")
    c += text(40, 420, "No protein channel needed", size=12, color=COLORS["green"], bold=True, anchor="start")

    # Key label bottom-right
    c += rect(550, 380, 220, 55, fill="#FAFAFA", stroke="#ddd", rx=6)
    c += text(560, 400, "= passive transport", size=12, color=COLORS["blue"], bold=True, anchor="start")
    c += text(560, 420, "High → Low concentration", size=12, color=COLORS["blue"], bold=True, anchor="start")

    return make_svg(c, width, height)


if __name__ == "__main__":
    svg = generate()
    out = REPO_ROOT / "bio" / "Checkpoint_13_Cell_Transport_img04.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"Saved: {out}")
