#!/usr/bin/env python3
"""Generate: Bacteriophage T4 infecting a bacterium."""
import sys, math
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'generators'))
from svg_base import *

def generate():
    width, height = 800, 520
    c = ""

    # Title
    c += text(400, 35, "Bacteriophage T4 Infecting a Bacterium", size=20, color=COLORS["dark_gray"], bold=True)

    # === Bacterium (rod-shaped, bottom) ===
    bx, by, bw, bh = 200, 370, 400, 120
    br = 60  # rounded ends
    c += f'  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="{br}" ry="{br}" fill="#FFF9C4" stroke="#F9A825" stroke-width="3" />\n'
    # Bacterial DNA squiggles inside
    c += f'  <path d="M 300 410 Q 330 395 360 410 Q 390 425 420 410 Q 450 395 480 410" fill="none" stroke="#E65100" stroke-width="2" opacity="0.5" />\n'
    c += f'  <path d="M 280 435 Q 310 420 340 435 Q 370 450 400 435 Q 430 420 460 435" fill="none" stroke="#E65100" stroke-width="2" opacity="0.5" />\n'
    c += text(400, 500, "Bacterium", size=16, color="#F9A825", bold=True)

    # === Phage T4 structure ===
    # Center X for the phage
    px = 400

    # --- Head (icosahedral = hexagon shape) ---
    head_cy = 140
    head_r = 55
    # Draw hexagon
    hex_points = []
    for i in range(6):
        angle = math.pi / 6 + i * math.pi / 3
        hx = px + head_r * math.cos(angle)
        hy = head_cy + head_r * math.sin(angle)
        hex_points.append(f"{hx:.1f},{hy:.1f}")
    pts = " ".join(hex_points)
    c += f'  <polygon points="{pts}" fill="#E3F2FD" stroke="#1565C0" stroke-width="3" />\n'

    # DNA inside head (wavy lines)
    c += f'  <path d="M 380 115 Q 390 105 400 115 Q 410 125 420 115" fill="none" stroke="#C62828" stroke-width="2" />\n'
    c += f'  <path d="M 375 135 Q 385 125 395 135 Q 405 145 415 135 Q 425 125 430 135" fill="none" stroke="#C62828" stroke-width="2" />\n'
    c += f'  <path d="M 380 155 Q 390 145 400 155 Q 410 165 420 155" fill="none" stroke="#C62828" stroke-width="2" />\n'

    # --- Collar (small rectangle below head) ---
    c += rect(385, 195, 30, 12, fill="#1565C0", stroke="#0D47A1", rx=2)

    # --- Tail sheath (long tube) ---
    c += rect(390, 207, 20, 100, fill="#90CAF9", stroke="#1565C0", rx=2)
    # Inner tube (darker, thinner)
    c += rect(396, 207, 8, 100, fill="#1565C0", stroke="none", rx=1)

    # --- Baseplate (wider hexagonal plate) ---
    bp_y = 310
    bp_points = f"{px-30},{bp_y} {px-20},{bp_y-10} {px+20},{bp_y-10} {px+30},{bp_y} {px+20},{bp_y+10} {px-20},{bp_y+10}"
    c += f'  <polygon points="{bp_points}" fill="#1565C0" stroke="#0D47A1" stroke-width="2" />\n'

    # --- Tail fibers (6 legs, 3 each side) ---
    fiber_color = "#7B1FA2"
    # Left fibers
    c += f'  <path d="M {px-20} {bp_y} Q {px-80} {bp_y+20} {px-120} {bp_y+55}" fill="none" stroke="{fiber_color}" stroke-width="2" />\n'
    c += f'  <path d="M {px-25} {bp_y+5} Q {px-75} {bp_y+35} {px-100} {bp_y+60}" fill="none" stroke="{fiber_color}" stroke-width="2" />\n'
    c += f'  <path d="M {px-15} {bp_y+5} Q {px-60} {bp_y+40} {px-80} {bp_y+60}" fill="none" stroke="{fiber_color}" stroke-width="2" />\n'
    # Right fibers
    c += f'  <path d="M {px+20} {bp_y} Q {px+80} {bp_y+20} {px+120} {bp_y+55}" fill="none" stroke="{fiber_color}" stroke-width="2" />\n'
    c += f'  <path d="M {px+25} {bp_y+5} Q {px+75} {bp_y+35} {px+100} {bp_y+60}" fill="none" stroke="{fiber_color}" stroke-width="2" />\n'
    c += f'  <path d="M {px+15} {bp_y+5} Q {px+60} {bp_y+40} {px+80} {bp_y+60}" fill="none" stroke="{fiber_color}" stroke-width="2" />\n'

    # --- DNA injection arrow (from tail into bacterium) ---
    c += f'  <line x1="{px}" y1="320" x2="{px}" y2="370" stroke="#C62828" stroke-width="3" stroke-dasharray="6,3" />\n'
    c += f'  <polygon points="{px-6},365 {px+6},365 {px},378" fill="#C62828" />\n'

    # === Labels with leader lines ===
    # Head label (left)
    c += f'  <line x1="340" y1="120" x2="170" y2="100" stroke="#999" stroke-width="1" />\n'
    c += text(160, 95, "Head (capsid)", size=14, color=COLORS["blue"], bold=True, anchor="end")

    # DNA label (left)
    c += f'  <line x1="370" y1="145" x2="170" y2="145" stroke="#999" stroke-width="1" />\n'
    c += text(160, 141, "DNA", size=14, color=COLORS["red"], bold=True, anchor="end")

    # Tail label (right)
    c += f'  <line x1="415" y1="255" x2="600" y2="255" stroke="#999" stroke-width="1" />\n'
    c += text(610, 251, "Tail sheath", size=14, color=COLORS["blue"], bold=True, anchor="start")

    # Baseplate label (right)
    c += f'  <line x1="435" y1="310" x2="600" y2="310" stroke="#999" stroke-width="1" />\n'
    c += text(610, 306, "Baseplate", size=14, color=COLORS["blue"], bold=True, anchor="start")

    # Tail fibers label (right)
    c += f'  <line x1="525" y1="360" x2="620" y2="345" stroke="#999" stroke-width="1" />\n'
    c += text(630, 341, "Tail fibers", size=14, color=COLORS["purple"], bold=True, anchor="start")

    # Injection label
    c += text(400, 355, "DNA injected", size=12, color=COLORS["red"], bold=True)

    return make_svg(c, width, height)

if __name__ == "__main__":
    svg = generate()
    out = str(__import__('pathlib').Path(__file__).resolve().parent / "Checkpoint_14_Viruses_Immune_Response_img01.svg")
    with open(out, "w") as f:
        f.write(svg)
    print(f"Saved: {out}")
