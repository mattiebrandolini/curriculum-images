#!/usr/bin/env python3
"""Generate osmosis diagram: water moving across a semi-permeable membrane."""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent / 'generators'))
from svg_base import *

def generate():
    c = ""
    W, H = 800, 420

    # Title
    c += text(400, 35, "Osmosis: Water Moves Across a Membrane", size=20, color=COLORS["dark_gray"], bold=True)

    # --- Left side: MORE water, FEWER solute ---
    c += rect(40, 60, 330, 300, fill="#E3F2FD", stroke="#90CAF9", rx=8)
    c += text(205, 90, "More Water", size=16, color=COLORS["blue"], bold=True)
    c += text(205, 110, "(less solute)", size=12, color=COLORS["medium_gray"])

    # Water molecules (small blue circles) - many on left
    water_left = [
        (90,160),(150,150),(100,210),(170,200),(130,260),(200,250),
        (80,280),(160,290),(240,170),(260,230),(220,300),(110,320),
        (180,340),(250,280),(280,310),(140,180),(210,140),(270,160),
    ]
    for wx, wy in water_left:
        c += circle(wx, wy, 10, fill="#64B5F6", stroke="#1565c0", sw=1.5)
        c += text(wx, wy + 4, "W", size=8, color="white", bold=True)

    # Solute on left (few)
    solute_left = [(120, 240), (250, 200)]
    for sx, sy in solute_left:
        c += circle(sx, sy, 13, fill="#FFCC80", stroke="#E65100", sw=2)
        c += text(sx, sy + 4, "S", size=9, color="#E65100", bold=True)

    # --- Right side: LESS water, MORE solute ---
    c += rect(430, 60, 330, 300, fill="#FFF3E0", stroke="#FFCC80", rx=8)
    c += text(595, 90, "Less Water", size=16, color=COLORS["orange"], bold=True)
    c += text(595, 110, "(more solute)", size=12, color=COLORS["medium_gray"])

    # Water molecules - fewer on right
    water_right = [
        (480,200),(540,260),(620,180),(570,320),(500,300),(660,270),
    ]
    for wx, wy in water_right:
        c += circle(wx, wy, 10, fill="#64B5F6", stroke="#1565c0", sw=1.5)
        c += text(wx, wy + 4, "W", size=8, color="white", bold=True)

    # Solute on right (many)
    solute_right = [
        (490,160),(560,170),(630,230),(700,200),(520,230),
        (650,300),(710,280),(470,270),(580,280),(700,150),
        (640,140),(530,140),
    ]
    for sx, sy in solute_right:
        c += circle(sx, sy, 13, fill="#FFCC80", stroke="#E65100", sw=2)
        c += text(sx, sy + 4, "S", size=9, color="#E65100", bold=True)

    # --- Membrane (vertical dashed bar in center) ---
    c += rect(370, 55, 60, 310, fill="#FFE0B2", stroke="#FF9800", rx=0)
    # Pore-like gaps showing semi-permeable nature
    for py in range(80, 340, 40):
        # Small gap (pore) in membrane
        c += rect(380, py, 40, 12, fill="white", stroke="#FFB74D", rx=3)
    c += text(400, 385, "Semi-Permeable Membrane", size=14, color="#E65100", bold=True)
    c += text(400, 403, "(only water can pass)", size=11, color=COLORS["medium_gray"])

    # --- Big arrows showing water movement LEFT → RIGHT ---
    # Three bold arrows going through the membrane
    c += arrow(280, 180, 450, 180, color=COLORS["blue"], width=3)
    c += arrow(290, 240, 460, 240, color=COLORS["blue"], width=3)
    c += arrow(270, 300, 440, 300, color=COLORS["blue"], width=3)

    # Arrow label
    c += text(340, 165, "H₂O", size=13, color=COLORS["blue"], bold=True)

    # Legend at bottom
    c += circle(180, 415, 8, fill="#64B5F6", stroke="#1565c0", sw=1.5)
    c += text(195, 419, "= Water", size=12, color=COLORS["dark_gray"], anchor="start")
    c += circle(320, 415, 10, fill="#FFCC80", stroke="#E65100", sw=2)
    c += text(337, 419, "= Solute (sugar/salt)", size=12, color=COLORS["dark_gray"], anchor="start")

    return make_svg(c, W, H)

svg = generate()
save_svg(svg, "bio/Checkpoint_13_Cell_Transport_img06.svg")
print("Done: bio/Checkpoint_13_Cell_Transport_img06.svg")
