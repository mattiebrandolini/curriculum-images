#!/usr/bin/env python3
"""Generate Active Transport diagram - molecules moving against concentration gradient."""
import sys, math
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'generators'))
from svg_base import *

def generate():
    c = ""
    W, H = 800, 420

    # Title
    c += text(400, 35, "Active Transport", size=22, color=COLORS["dark_gray"], bold=True)
    c += text(400, 58, "Moves molecules from LOW to HIGH concentration", size=13, color=COLORS["medium_gray"])

    # --- Background zones ---
    # Left zone (LOW concentration)
    c += rect(40, 80, 310, 280, fill="#E8F5E9", stroke="#A5D6A7", rx=10)
    c += text(195, 105, "LOW Concentration", size=15, color=COLORS["green"], bold=True)

    # Right zone (HIGH concentration)
    c += rect(450, 80, 310, 280, fill="#FFEBEE", stroke="#EF9A9A", rx=10)
    c += text(605, 105, "HIGH Concentration", size=15, color=COLORS["red"], bold=True)

    # --- Membrane (center bar) ---
    c += rect(350, 80, 100, 280, fill=COLORS["membrane"], stroke="#F57C00", rx=0)
    c += text(400, 230, "Cell", size=11, color="#5D4037", bold=True)
    c += text(400, 248, "Membrane", size=11, color="#5D4037", bold=True)

    # Protein channel in membrane
    c += f'  <rect x="375" y="150" width="50" height="80" fill="#7E57C2" stroke="#4527A0" rx="8" />\n'
    c += text(400, 185, "Protein", size=9, color="white", bold=True)
    c += text(400, 198, "Pump", size=9, color="white", bold=True)

    # --- Molecules (dots) ---
    # Few dots on left (LOW)
    low_dots = [(120, 180), (200, 250), (100, 300), (250, 170), (160, 320)]
    for (dx, dy) in low_dots:
        c += circle(dx, dy, 10, fill="#66BB6A", stroke="#388E3C", sw=2)

    # Many dots on right (HIGH)
    high_dots = [
        (490, 150), (540, 180), (600, 140), (680, 170), (720, 200),
        (500, 240), (560, 260), (640, 230), (700, 260), (480, 310),
        (550, 330), (620, 300), (690, 320), (530, 150), (660, 290),
    ]
    for (dx, dy) in high_dots:
        c += circle(dx, dy, 10, fill="#EF5350", stroke="#C62828", sw=2)

    # --- Arrow: molecule moving from LOW → HIGH through pump ---
    # Molecule being transported
    c += circle(310, 190, 10, fill="#66BB6A", stroke="#388E3C", sw=2)
    # Curved arrow path from left side through pump to right side
    c += (
        f'  <defs><marker id="arrowAT" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="#4527A0" /></marker></defs>\n'
        f'  <path d="M 310 190 Q 340 160 400 160 Q 460 160 460 190" '
        f'stroke="#4527A0" stroke-width="3" fill="none" '
        f'stroke-dasharray="6,3" marker-end="url(#arrowAT)" />\n'
    )
    # Arriving molecule on right
    c += circle(465, 190, 10, fill="#66BB6A", stroke="#388E3C", sw=2)
    c += f'  <circle cx="465" cy="190" r="10" fill="#66BB6A" stroke="#FDD835" stroke-width="3" />\n'

    # --- ATP Energy burst ---
    # Star/burst shape for ATP energy
    c += f'  <polygon points="400,265 407,280 425,283 412,295 415,313 400,304 385,313 388,295 375,283 393,280" fill="#FDD835" stroke="#F9A825" stroke-width="1.5" />\n'
    c += text(400, 296, "ATP", size=10, color="#E65100", bold=True)
    c += text(400, 340, "Energy needed!", size=13, color=COLORS["orange"], bold=True)

    # --- Bottom analogy ---
    c += f'  <line x1="100" y1="390" x2="700" y2="390" stroke="#BDBDBD" stroke-width="1" />\n'
    # Hill analogy
    c += f'  <path d="M 200 405 Q 400 370 600 405" stroke="#9E9E9E" stroke-width="2" fill="none" />\n'
    # Ball on slope
    c += circle(280, 400, 8, fill="#66BB6A", stroke="#388E3C", sw=2)
    c += arrow(290, 395, 400, 380, color=COLORS["orange"], width=2)
    c += text(500, 415, "Like pushing a ball uphill", size=12, color=COLORS["medium_gray"])

    return make_svg(c, W, H)

if __name__ == "__main__":
    svg = generate()
    save_svg(svg, "bio/Checkpoint_13_Cell_Transport_img08.svg")
    print("Generated bio/Checkpoint_13_Cell_Transport_img08.svg")
