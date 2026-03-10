#!/usr/bin/env python3
"""Generate concentration gradient diagram for Checkpoint 13 Cell Transport."""
import sys, random, math
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'generators'))
from svg_base import *

random.seed(42)

width, height = 800, 420
c = ""

# Title
c += text(400, 35, "The Concentration Gradient", size=20, color=COLORS["dark_gray"], bold=True)

# Background container
c += rect(40, 55, 720, 310, fill="#fafafa", stroke="#ddd", rx=12)

# Dividing dashed line (gradient boundary visual)
c += f'  <line x1="400" y1="75" x2="400" y2="345" stroke="#bbb" stroke-width="1.5" stroke-dasharray="6,4" />\n'

# LEFT SIDE — HIGH concentration
c += rect(50, 60, 340, 50, fill=COLORS["orange"], stroke=COLORS["orange"], rx=8)
c += text(220, 92, "HIGH Concentration", size=16, color="white", bold=True)

# RIGHT SIDE — LOW concentration
c += rect(410, 60, 340, 50, fill=COLORS["teal"], stroke=COLORS["teal"], rx=8)
c += text(580, 92, "LOW Concentration", size=16, color="white", bold=True)

# Draw molecules as colored circles
# Left side: many molecules clustered (high concentration)
left_molecules = []
for i in range(40):
    mx = random.uniform(70, 370)
    my = random.uniform(130, 330)
    # Bias toward left side (more dense on left)
    mx = 70 + (mx - 70) * 0.7
    left_molecules.append((mx, my))

for mx, my in left_molecules:
    c += circle(mx, my, 8, fill="#FF8A65", stroke=COLORS["orange"], sw=1.5)

# Right side: fewer molecules spread out (low concentration)
right_molecules = []
for i in range(12):
    mx = random.uniform(430, 730)
    my = random.uniform(130, 330)
    right_molecules.append((mx, my))

for mx, my in right_molecules:
    c += circle(mx, my, 8, fill="#80CBC4", stroke=COLORS["teal"], sw=1.5)

# Big arrow showing direction of movement
# Arrow from high to low
arrow_y = 380
c += f'  <defs><marker id="bigArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{COLORS["blue"]}" /></marker></defs>\n'
c += f'  <line x1="200" y1="{arrow_y}" x2="600" y2="{arrow_y}" stroke="{COLORS["blue"]}" stroke-width="4" marker-end="url(#bigArrow)" />\n'

c += text(400, arrow_y + 28, "Molecules move HIGH → LOW", size=14, color=COLORS["blue"], bold=True)

svg = make_svg(c, width, height + 30)

out = "/home/mattie/curriculum-images/bio/Checkpoint_13_Cell_Transport_img03.svg"
__import__('pathlib').Path(out).parent.mkdir(parents=True, exist_ok=True)
__import__('pathlib').Path(out).write_text(svg, encoding="utf-8")
print(f"Saved: {out}")
