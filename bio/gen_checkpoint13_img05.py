#!/usr/bin/env python3
"""Generate facilitated diffusion diagram showing molecules passing through a transport protein."""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'generators'))
from svg_base import *

def generate():
    width, height = 800, 450
    c = ""

    # Title
    c += text(400, 35, "Facilitated Diffusion", size=22, color=COLORS["dark_gray"], bold=True)
    c += text(400, 58, "Molecules need a protein door to cross", size=13, color=COLORS["medium_gray"])

    # --- Outside / Inside labels ---
    c += text(130, 105, "OUTSIDE (High)", size=15, color=COLORS["blue"], bold=True)
    c += text(130, 380, "INSIDE (Low)", size=15, color=COLORS["teal"], bold=True)

    # --- Membrane bilayer (two horizontal bars with gap for protein) ---
    membrane_y = 200
    membrane_h = 60
    # Left section of membrane
    c += rect(60, membrane_y, 250, membrane_h, fill=COLORS["membrane"], stroke="#E69500", rx=8)
    # Right section of membrane
    c += rect(490, membrane_y, 250, membrane_h, fill=COLORS["membrane"], stroke="#E69500", rx=8)

    # Membrane label on left side
    c += text(185, membrane_y + 35, "Cell Membrane", size=12, color="#7A4A00", bold=True)
    # Membrane label on right side
    c += text(615, membrane_y + 35, "Cell Membrane", size=12, color="#7A4A00", bold=True)

    # Phospholipid pattern dots on membrane (decorative)
    for lx in range(80, 300, 30):
        c += circle(lx, membrane_y + 15, 5, fill="#FFE0B2", stroke="#E69500", sw=1)
        c += circle(lx, membrane_y + 45, 5, fill="#FFE0B2", stroke="#E69500", sw=1)
    for lx in range(510, 730, 30):
        c += circle(lx, membrane_y + 15, 5, fill="#FFE0B2", stroke="#E69500", sw=1)
        c += circle(lx, membrane_y + 45, 5, fill="#FFE0B2", stroke="#E69500", sw=1)

    # --- Transport Protein (channel in the gap) ---
    # Draw as a U-shaped channel protein spanning the membrane
    protein_color = COLORS["purple"]
    protein_light = "#E1BEE7"
    # Left wall of channel
    c += f'  <rect x="310" y="{membrane_y - 20}" width="30" height="{membrane_h + 40}" fill="{protein_light}" stroke="{protein_color}" stroke-width="2" rx="10" />\n'
    # Right wall of channel
    c += f'  <rect x="460" y="{membrane_y - 20}" width="30" height="{membrane_h + 40}" fill="{protein_light}" stroke="{protein_color}" stroke-width="2" rx="10" />\n'
    # Top lip left
    c += f'  <rect x="300" y="{membrane_y - 25}" width="50" height="15" fill="{protein_light}" stroke="{protein_color}" stroke-width="2" rx="6" />\n'
    # Top lip right
    c += f'  <rect x="450" y="{membrane_y - 25}" width="50" height="15" fill="{protein_light}" stroke="{protein_color}" stroke-width="2" rx="6" />\n'
    # Bottom lip left
    c += f'  <rect x="300" y="{membrane_y + membrane_h + 10}" width="50" height="15" fill="{protein_light}" stroke="{protein_color}" stroke-width="2" rx="6" />\n'
    # Bottom lip right
    c += f'  <rect x="450" y="{membrane_y + membrane_h + 10}" width="50" height="15" fill="{protein_light}" stroke="{protein_color}" stroke-width="2" rx="6" />\n'

    # Transport Protein label
    c += text(400, membrane_y + membrane_h + 50, "Transport Protein", size=14, color=COLORS["purple"], bold=True)
    c += text(400, membrane_y + membrane_h + 68, "(the door)", size=12, color=COLORS["medium_gray"])

    # --- Molecules (outside - many, clustered above membrane = HIGH) ---
    mol_color = COLORS["blue"]
    mol_light = "#BBDEFB"
    # Many molecules outside (high concentration)
    outside_molecules = [
        (340, 100), (370, 85), (410, 95), (440, 80), (460, 105),
        (380, 115), (420, 120), (355, 135), (445, 130),
        (390, 145), (430, 150), (370, 160),
        (500, 90), (530, 100), (550, 115),
        (280, 95), (260, 110), (300, 130),
    ]
    for mx, my in outside_molecules:
        c += circle(mx, my, 8, fill=mol_light, stroke=mol_color, sw=2)

    # --- Molecules passing through channel (mid-transit) ---
    c += circle(390, 210, 8, fill=mol_light, stroke=mol_color, sw=2)
    c += circle(410, 235, 8, fill=mol_light, stroke=mol_color, sw=2)

    # --- Molecules inside (few = LOW concentration) ---
    inside_molecules = [
        (370, 330), (430, 345), (400, 360),
    ]
    for mx, my in inside_molecules:
        c += circle(mx, my, 8, fill=mol_light, stroke=mol_color, sw=2)

    # --- Arrow showing direction of movement (high to low, downward through channel) ---
    c += arrow(400, 155, 400, 175, color=COLORS["red"], width=3)

    # Concentration gradient labels (right side)
    # Arrow showing HIGH -> LOW
    c += arrow(700, 110, 700, 370, color=COLORS["red"], width=3)
    c += text(700, 95, "HIGH", size=14, color=COLORS["red"], bold=True)
    c += text(700, 395, "LOW", size=14, color=COLORS["red"], bold=True)

    # Key insight box at bottom
    c += rect(150, 410, 500, 30, fill=COLORS["light_green"], stroke=COLORS["green"], rx=6)
    c += text(400, 430, "No energy needed — moves HIGH to LOW", size=13, color=COLORS["green"], bold=True)

    return make_svg(c, width, height)


if __name__ == "__main__":
    svg = generate()
    save_svg(svg, "bio/Checkpoint_13_Cell_Transport_img05.svg")
    print("Generated: bio/Checkpoint_13_Cell_Transport_img05.svg")
