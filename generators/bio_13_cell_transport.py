#!/usr/bin/env python3
"""
EXAMPLE: Bio Checkpoint 13 — Cell Transport
Shows the pattern for generating curriculum SVGs.

Each lesson gets its own generator file.
Each slot gets its own function.
All functions called at bottom to generate all SVGs for the lesson.
"""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from svg_base import *


SUBJECT = "bio"
LESSON = "Checkpoint_13_Cell_Transport"


def img01_cell_membrane_overview():
    """SLOT 1: Cell Membrane Osmosis Biology — overview of transport across membrane."""
    content = ""
    
    # Title
    content += text(400, 30, "Cell Membrane Transport", size=20, color=COLORS["blue"], bold=True)
    
    # Membrane (horizontal bilayer)
    content += '  <rect x="50" y="200" width="700" height="40" fill="#FFB74D" rx="20" opacity="0.8" />\n'
    content += text(400, 225, "Cell Membrane (phospholipid bilayer)", size=12, color="#5D4037")
    
    # Outside label
    content += text(400, 170, "OUTSIDE the cell", size=16, color=COLORS["blue"], bold=True)
    content += text(400, 188, "(high concentration)", size=11, color=COLORS["medium_gray"])
    
    # Inside label  
    content += text(400, 275, "INSIDE the cell", size=16, color=COLORS["teal"], bold=True)
    content += text(400, 293, "(low concentration)", size=11, color=COLORS["medium_gray"])
    
    # Passive transport section (left)
    content += rect(60, 310, 220, 140, fill=COLORS["light_blue"], stroke=COLORS["blue"])
    content += text(170, 335, "PASSIVE Transport", size=14, color=COLORS["blue"], bold=True)
    content += text(170, 355, "No energy needed", size=11, color=COLORS["medium_gray"])
    content += text(170, 380, "• Simple diffusion", size=12, color=COLORS["dark_gray"])
    content += text(170, 400, "• Facilitated diffusion", size=12, color=COLORS["dark_gray"])
    content += text(170, 420, "• Osmosis (water)", size=12, color=COLORS["dark_gray"])
    
    # Arrow down through membrane (passive)
    content += arrow(170, 160, 170, 260, color=COLORS["blue"], width=3)
    content += text(130, 155, "HIGH → LOW", size=10, color=COLORS["blue"], bold=True)
    
    # Active transport section (right)
    content += rect(520, 310, 220, 140, fill=COLORS["light_orange"], stroke=COLORS["orange"])
    content += text(630, 335, "ACTIVE Transport", size=14, color=COLORS["orange"], bold=True)
    content += text(630, 355, "Needs ATP energy", size=11, color=COLORS["medium_gray"])
    content += text(630, 380, "• Protein pumps", size=12, color=COLORS["dark_gray"])
    content += text(630, 400, "• Endocytosis (in)", size=12, color=COLORS["dark_gray"])
    content += text(630, 420, "• Exocytosis (out)", size=12, color=COLORS["dark_gray"])
    
    # Arrow up through membrane (active — against gradient)
    content += arrow(630, 260, 630, 160, color=COLORS["orange"], width=3)
    content += text(670, 155, "LOW → HIGH", size=10, color=COLORS["orange"], bold=True)
    
    # ATP symbol
    content += circle(580, 160, 15, fill="#FFF3E0", stroke=COLORS["orange"])
    content += text(580, 165, "ATP", size=10, color=COLORS["orange"], bold=True)
    
    return make_svg(content, 800, 470)


def img02_concentration_gradient():
    """SLOT 2: Diffusion Concentration Gradient — molecules moving high to low."""
    content = ""
    
    content += text(400, 30, "Concentration Gradient", size=20, color=COLORS["blue"], bold=True)
    content += text(400, 52, "Molecules move from HIGH to LOW concentration", size=13, color=COLORS["medium_gray"])
    
    # Three stages left to right
    stages = [
        ("Before", "All on one side", 80),
        ("During", "Spreading out", 310),
        ("After", "Equal everywhere", 540),
    ]
    
    for label, desc, x in stages:
        # Container box
        content += rect(x, 70, 200, 200, fill="white", stroke="#ccc")
        content += text(x + 100, 95, label, size=14, color=COLORS["blue"], bold=True)
        
        # Divider line (membrane)
        content += f'  <line x1="{x+100}" y1="110" x2="{x+100}" y2="250" stroke="{COLORS["membrane"]}" stroke-width="3" stroke-dasharray="8,4" />\n'
    
    # Stage 1: dots clustered left
    for i in range(12):
        cx = 100 + (i % 4) * 15
        cy = 140 + (i // 4) * 25
        content += circle(cx, cy, 6, fill=COLORS["blue"], stroke="none", sw=0)
    
    # Stage 2: dots spreading
    positions = [(330,140),(350,160),(370,150),(390,180),(340,200),(420,140),(440,170),(460,200),(380,220),(330,230),(450,230),(410,160)]
    for cx, cy in positions:
        content += circle(cx, cy, 6, fill=COLORS["blue"], stroke="none", sw=0)
    
    # Stage 3: dots evenly spread
    for i in range(12):
        cx = 560 + (i % 4) * 40
        cy = 130 + (i // 4) * 35
        content += circle(cx, cy, 6, fill=COLORS["blue"], stroke="none", sw=0)
    
    # Arrows between stages
    content += arrow(290, 170, 305, 170, color=COLORS["dark_gray"])
    content += arrow(520, 170, 535, 170, color=COLORS["dark_gray"])
    
    # Bottom label
    content += text(400, 310, "This happens naturally — no energy needed!", size=14, color=COLORS["green"], bold=True)
    content += text(400, 335, "equilibrium = equal concentration on both sides", size=12, color=COLORS["medium_gray"])
    
    return make_svg(content, 800, 360)


# ============================================================
# Generate all SVGs for this lesson
# ============================================================
if __name__ == "__main__":
    generators = {
        "01": img01_cell_membrane_overview,
        "02": img02_concentration_gradient,
        # Remaining slots to be implemented:
        # "03": img03_simple_diffusion,
        # "04": img04_facilitated_diffusion,
        # "05": img05_osmosis,
        # "06": img06_tonicity,
        # "07": img07_active_transport,
        # "08": img08_sodium_potassium_pump,
        # "09": img09_endocytosis_exocytosis,
        # "10": img10_real_world,
    }
    
    for slot_num, gen_func in generators.items():
        svg = gen_func()
        filepath = f"{SUBJECT}/{LESSON}_img{slot_num}.svg"
        saved = save_svg(svg, filepath)
        update_manifest(SUBJECT, LESSON, slot_num)
        print(f"  ✓ Slot {slot_num}: {filepath}")
    
    print(f"\nGenerated {len(generators)}/{10} slots for {LESSON}")
