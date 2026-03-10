#!/usr/bin/env python3
"""Generate Tonicity: The Three Solutions diagram with visual cells and water arrows."""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'generators'))
from svg_base import *

def generate():
    W, H = 800, 420
    c = ""

    # Title
    c += text(400, 32, "Tonicity: The Three Solutions", size=20, color=COLORS["dark_gray"], bold=True)

    panels = [
        {
            "name": "Hypertonic",
            "subtitle": "More solute outside",
            "water_dir": "out",
            "cell_label": "Cell shrinks",
            "color": COLORS["red"],
            "light": "#ffebee",
            "cell_rx": 48,  # slightly smaller cell
            "cell_ry": 48,
        },
        {
            "name": "Hypotonic",
            "subtitle": "Less solute outside",
            "water_dir": "in",
            "cell_label": "Cell swells",
            "color": COLORS["blue"],
            "light": COLORS["light_blue"],
            "cell_rx": 62,  # slightly bigger cell
            "cell_ry": 58,
        },
        {
            "name": "Isotonic",
            "subtitle": "Equal solute",
            "water_dir": "both",
            "cell_label": "Cell stays same",
            "color": COLORS["green"],
            "light": COLORS["light_green"],
            "cell_rx": 55,
            "cell_ry": 55,
        },
    ]

    panel_w = 230
    gap = 18
    start_x = (W - (3 * panel_w + 2 * gap)) // 2

    for i, p in enumerate(panels):
        px = start_x + i * (panel_w + gap)
        cx = px + panel_w // 2
        cy = 210

        # Panel background
        c += rect(px, 50, panel_w, 355, fill=p["light"], stroke=p["color"], rx=8)

        # Header bar
        c += f'  <rect x="{px}" y="50" width="{panel_w}" height="44" fill="{p["color"]}" rx="8" />\n'
        # Square off bottom corners of header
        c += f'  <rect x="{px}" y="72" width="{panel_w}" height="22" fill="{p["color"]}" />\n'
        c += text(cx, 79, p["name"], size=16, color="white", bold=True)

        # Subtitle
        c += text(cx, 112, p["subtitle"], size=12, color=COLORS["medium_gray"])

        # Outside area with dots (solute particles)
        c += f'  <rect x="{px + 15}" y="125" width="{panel_w - 30}" height="185" fill="#f0f7ff" stroke="#ccc" rx="6" stroke-dasharray="4,2" />\n'
        c += text(cx, 142, "Outside", size=10, color=COLORS["medium_gray"])

        # Cell (ellipse) in center
        c += f'  <ellipse cx="{cx}" cy="{cy}" rx="{p["cell_rx"]}" ry="{p["cell_ry"]}" fill="{COLORS["cell_bg"]}" stroke="{COLORS["membrane"]}" stroke-width="3" />\n'
        c += text(cx, cy + 4, "Cell", size=11, color=COLORS["dark_gray"], bold=True)

        # Solute dots outside cell
        import math
        if p["water_dir"] == "out":
            # Many dots outside (hypertonic: more solute outside)
            outside_dots = [(px+30, 165), (px+60, 155), (px+panel_w-30, 165),
                           (px+panel_w-60, 155), (px+35, 275), (px+panel_w-35, 275),
                           (px+55, 290), (px+panel_w-55, 290),
                           (px+40, 230), (px+panel_w-40, 230)]
            inside_dots = [(cx-10, cy-12), (cx+12, cy+10)]
        elif p["water_dir"] == "in":
            # Few dots outside (hypotonic: less solute outside)
            outside_dots = [(px+40, 170), (px+panel_w-40, 280)]
            inside_dots = [(cx-15, cy-15), (cx+10, cy-8), (cx-5, cy+15),
                          (cx+18, cy+10), (cx-12, cy+5), (cx+5, cy-18)]
        else:
            # Equal dots (isotonic)
            outside_dots = [(px+35, 170), (px+panel_w-35, 170),
                           (px+35, 280), (px+panel_w-35, 280)]
            inside_dots = [(cx-12, cy-10), (cx+12, cy-10),
                          (cx-12, cy+12), (cx+12, cy+12)]

        for dx, dy in outside_dots:
            c += circle(dx, dy, 4, fill=p["color"], stroke="none", sw=0)
        for dx, dy in inside_dots:
            c += circle(dx, dy, 4, fill="#e65100", stroke="none", sw=0)

        # Water arrows
        arrow_color = COLORS["water"]
        if p["water_dir"] == "out":
            # Arrows pointing OUT from cell
            c += arrow(cx - p["cell_rx"] - 2, cy, cx - p["cell_rx"] - 28, cy, color=arrow_color, width=3)
            c += arrow(cx + p["cell_rx"] + 2, cy, cx + p["cell_rx"] + 28, cy, color=arrow_color, width=3)
        elif p["water_dir"] == "in":
            # Arrows pointing IN to cell
            c += arrow(cx - p["cell_rx"] - 28, cy, cx - p["cell_rx"] - 2, cy, color=arrow_color, width=3)
            c += arrow(cx + p["cell_rx"] + 28, cy, cx + p["cell_rx"] + 2, cy, color=arrow_color, width=3)
        else:
            # Arrows both ways
            c += arrow(cx - p["cell_rx"] - 2, cy - 10, cx - p["cell_rx"] - 24, cy - 10, color=arrow_color, width=2)
            c += arrow(cx - p["cell_rx"] - 24, cy + 10, cx - p["cell_rx"] - 2, cy + 10, color=arrow_color, width=2)
            c += arrow(cx + p["cell_rx"] + 2, cy - 10, cx + p["cell_rx"] + 24, cy - 10, color=arrow_color, width=2)
            c += arrow(cx + p["cell_rx"] + 24, cy + 10, cx + p["cell_rx"] + 2, cy + 10, color=arrow_color, width=2)

        # Water label on arrows
        if p["water_dir"] != "both":
            c += text(cx, cy + p["cell_ry"] + 18, "H₂O", size=11, color=arrow_color, bold=True)
        else:
            c += text(cx, cy + p["cell_ry"] + 18, "H₂O equal", size=11, color=arrow_color, bold=True)

        # Result label at bottom
        c += text(cx, 340, p["cell_label"], size=14, color=p["color"], bold=True)

    # Legend at very bottom
    c += circle(240, 395, 4, fill=COLORS["blue"], stroke="none", sw=0)
    c += text(260, 399, "= solute", size=10, color=COLORS["medium_gray"], anchor="start")
    c += f'  <line x1="330" y1="395" x2="360" y2="395" stroke="{COLORS["water"]}" stroke-width="3" />\n'
    c += text(370, 399, "= water movement", size=10, color=COLORS["medium_gray"], anchor="start")

    return make_svg(c, W, H)

if __name__ == "__main__":
    svg = generate()
    out = str(__import__('pathlib').Path(__file__).resolve().parent / "Checkpoint_13_Cell_Transport_img07.svg")
    with open(out, "w") as f:
        f.write(svg)
    print(f"Saved: {out}")
