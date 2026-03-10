#!/usr/bin/env python3
"""
Reusable layout templates for curriculum SVGs.
These handle positioning — generators just supply content.

Instead of hand-coding coordinates for every diagram, 
use these templates and just pass in labels/items.
"""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from svg_base import *


def comparison_diagram(title, left_title, right_title, left_items, right_items, 
                        left_color="blue", right_color="orange", width=800, height=None):
    """
    Side-by-side comparison. The most common layout.
    
    Args:
        title: Main heading
        left_title/right_title: Column headers
        left_items/right_items: List of strings for each side
        left_color/right_color: Color keys from COLORS dict
    
    Usage:
        svg = comparison_diagram(
            "Mitosis vs Meiosis",
            "Mitosis", "Meiosis",
            ["2 cells", "Identical", "Body cells", "1 division"],
            ["4 cells", "Different", "Sex cells", "2 divisions"],
        )
    """
    max_items = max(len(left_items), len(right_items))
    if height is None:
        height = 140 + max_items * 40
    
    c = ""
    c += text(400, 35, title, size=20, color=COLORS["dark_gray"], bold=True)
    
    # Left column
    lc = COLORS.get(left_color, left_color)
    lbg = COLORS.get(f"light_{left_color}", "#e3f2fd")
    c += rect(40, 60, 340, height - 80, fill=lbg, stroke=lc)
    c += rect(40, 60, 340, 40, fill=lc, stroke=lc)
    c += text(210, 87, left_title, size=16, color="white", bold=True)
    
    for i, item in enumerate(left_items):
        y = 130 + i * 40
        c += text(210, y, item, size=14, color=COLORS["dark_gray"])
    
    # Right column
    rc = COLORS.get(right_color, right_color)
    rbg = COLORS.get(f"light_{right_color}", "#fff3e0")
    c += rect(420, 60, 340, height - 80, fill=rbg, stroke=rc)
    c += rect(420, 60, 340, 40, fill=rc, stroke=rc)
    c += text(590, 87, right_title, size=16, color="white", bold=True)
    
    for i, item in enumerate(right_items):
        y = 130 + i * 40
        c += text(590, y, item, size=14, color=COLORS["dark_gray"])
    
    # VS divider
    c += circle(400, height // 2 + 20, 20, fill="white", stroke="#ccc")
    c += text(400, height // 2 + 26, "VS", size=12, color=COLORS["medium_gray"], bold=True)
    
    return make_svg(c, width, height)


def labeled_diagram(title, parts, connections=None, width=800, height=500):
    """
    Central diagram with labeled parts pointing to it.
    
    Args:
        title: Main heading
        parts: List of dicts: {"label": str, "x": int, "y": int, "desc": str (optional)}
        connections: List of tuples: (from_idx, to_idx) to draw lines between parts
    
    Usage:
        svg = labeled_diagram("Virus Structure", [
            {"label": "Capsid", "x": 400, "y": 150, "desc": "protein coat"},
            {"label": "DNA/RNA", "x": 400, "y": 250, "desc": "genetic material"},
        ])
    """
    c = ""
    c += text(400, 35, title, size=20, color=COLORS["dark_gray"], bold=True)
    
    for i, part in enumerate(parts):
        x, y = part["x"], part["y"]
        label = part["label"]
        desc = part.get("desc", "")
        color = part.get("color", COLORS["blue"])
        
        # Dot marker
        c += circle(x, y, 8, fill=color, stroke="white")
        
        # Label with optional description
        label_x = x + 20 if x < 400 else x - 20
        anchor = "start" if x < 400 else "end"
        c += text(label_x, y - 5, label, size=14, color=color, bold=True, anchor=anchor)
        if desc:
            c += text(label_x, y + 12, desc, size=11, color=COLORS["medium_gray"], anchor=anchor)
    
    if connections:
        for (i, j) in connections:
            p1, p2 = parts[i], parts[j]
            c += f'  <line x1="{p1["x"]}" y1="{p1["y"]}" x2="{p2["x"]}" y2="{p2["y"]}" stroke="#ccc" stroke-width="1" stroke-dasharray="4,4" />\n'
    
    return make_svg(c, width, height)


def process_flow(title, steps, direction="horizontal", width=800, height=None):
    """
    Linear process with numbered steps and arrows.
    
    Args:
        title: Main heading
        steps: List of dicts: {"label": str, "detail": str (optional), "color": str (optional)}
        direction: "horizontal" or "vertical"
    
    Usage:
        svg = process_flow("How DNA Replicates", [
            {"label": "Helicase unzips", "detail": "Breaks hydrogen bonds"},
            {"label": "Primase adds primer", "detail": "RNA starting point"},
            {"label": "DNA Polymerase builds", "detail": "Adds nucleotides 5'→3'"},
        ])
    """
    n = len(steps)
    
    if direction == "horizontal":
        if height is None:
            height = 200
        step_width = min(160, (width - 80) // n)
        start_x = (width - (step_width * n + 30 * (n - 1))) // 2
        
        c = ""
        c += text(400, 35, title, size=20, color=COLORS["dark_gray"], bold=True)
        
        for i, step in enumerate(steps):
            x = start_x + i * (step_width + 30)
            color = COLORS.get(step.get("color", "blue"), COLORS["blue"])
            light = COLORS.get(f"light_{step.get('color', 'blue')}", "#e3f2fd")
            
            # Step box
            c += rect(x, 60, step_width, 100, fill=light, stroke=color)
            
            # Step number circle
            c += circle(x + step_width // 2, 60, 14, fill=color, stroke="white")
            c += text(x + step_width // 2, 65, str(i + 1), size=12, color="white", bold=True)
            
            # Label
            c += text(x + step_width // 2, 105, step["label"], size=12, color=COLORS["dark_gray"], bold=True)
            
            if "detail" in step:
                c += text(x + step_width // 2, 125, step["detail"], size=10, color=COLORS["medium_gray"])
            
            # Arrow to next step
            if i < n - 1:
                ax = x + step_width + 3
                c += arrow(ax, 110, ax + 24, 110, color=COLORS["dark_gray"])
    
    else:  # vertical
        if height is None:
            height = 80 + n * 90
        
        c = ""
        c += text(400, 35, title, size=20, color=COLORS["dark_gray"], bold=True)
        
        for i, step in enumerate(steps):
            y = 70 + i * 90
            color = COLORS.get(step.get("color", "blue"), COLORS["blue"])
            light = COLORS.get(f"light_{step.get('color', 'blue')}", "#e3f2fd")
            
            c += rect(150, y, 500, 55, fill=light, stroke=color)
            c += circle(150, y + 27, 16, fill=color, stroke="white")
            c += text(150, y + 33, str(i + 1), size=13, color="white", bold=True)
            c += text(410, y + 25, step["label"], size=13, color=COLORS["dark_gray"], bold=True)
            
            if "detail" in step:
                c += text(410, y + 43, step["detail"], size=11, color=COLORS["medium_gray"])
            
            if i < n - 1:
                c += arrow(400, y + 58, 400, y + 85, color=COLORS["dark_gray"])
    
    return make_svg(c, width, height)


def cycle_diagram(title, steps, width=800, height=500, radius=160):
    """
    Circular cycle diagram with arrows between steps.
    
    Args:
        title: Main heading
        steps: List of dicts: {"label": str, "detail": str (optional), "color": str (optional)}
    
    Usage:
        svg = cycle_diagram("The Cell Cycle", [
            {"label": "G1 Phase", "detail": "Cell grows"},
            {"label": "S Phase", "detail": "DNA copied"},
            {"label": "G2 Phase", "detail": "Prepares"},
            {"label": "M Phase", "detail": "Division"},
        ])
    """
    import math
    n = len(steps)
    cx, cy = width // 2, height // 2 + 20
    
    c = ""
    c += text(cx, 35, title, size=20, color=COLORS["dark_gray"], bold=True)
    
    # Draw center circle (light)
    c += circle(cx, cy, radius + 40, fill="#fafafa", stroke="#eee")
    
    for i, step in enumerate(steps):
        angle = (2 * math.pi * i / n) - math.pi / 2  # Start from top
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        
        color = COLORS.get(step.get("color", "blue"), COLORS["blue"])
        light = COLORS.get(f"light_{step.get('color', 'blue')}", "#e3f2fd")
        
        # Step bubble
        c += circle(x, y, 35, fill=light, stroke=color)
        c += text(x, y - 3, step["label"], size=10, color=color, bold=True)
        
        if "detail" in step:
            c += text(x, y + 12, step["detail"], size=8, color=COLORS["medium_gray"])
        
        # Arrow to next step
        next_i = (i + 1) % n
        next_angle = (2 * math.pi * next_i / n) - math.pi / 2
        
        # Arrow start/end offset from circle edge
        ax1 = cx + (radius - 45) * math.cos((angle + next_angle) / 2)
        ay1 = cy + (radius - 45) * math.sin((angle + next_angle) / 2)
        ax2 = cx + (radius - 45) * math.cos((angle + next_angle) / 2 + 0.15)
        ay2 = cy + (radius - 45) * math.sin((angle + next_angle) / 2 + 0.15)
    
    return make_svg(c, width, height)


def table_diagram(title, headers, rows, col_colors=None, width=800, height=None):
    """
    Clean table layout for comparison data.
    
    Args:
        title: Main heading
        headers: List of column header strings
        rows: List of lists (each inner list = one row)
        col_colors: Optional list of color keys for headers
    
    Usage:
        svg = table_diagram("Tonicity Effects", 
            ["Solution", "Water moves", "Animal cell", "Plant cell"],
            [
                ["Hypertonic", "OUT of cell", "Shrinks", "Wilts"],
                ["Hypotonic", "INTO cell", "Bursts!", "Firm (turgor)"],
                ["Isotonic", "Equal", "Normal", "Normal"],
            ]
        )
    """
    n_cols = len(headers)
    n_rows = len(rows)
    col_width = (width - 80) // n_cols
    row_height = 45
    
    if height is None:
        height = 100 + (n_rows + 1) * row_height
    
    if col_colors is None:
        col_colors = ["blue"] * n_cols
    
    c = ""
    c += text(400, 35, title, size=20, color=COLORS["dark_gray"], bold=True)
    
    # Header row
    for j, header in enumerate(headers):
        x = 40 + j * col_width
        color = COLORS.get(col_colors[j % len(col_colors)], COLORS["blue"])
        c += rect(x, 55, col_width, row_height, fill=color, stroke="white")
        c += text(x + col_width // 2, 55 + row_height // 2 + 5, header, 
                  size=13, color="white", bold=True)
    
    # Data rows
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            x = 40 + j * col_width
            y = 55 + (i + 1) * row_height
            bg = "#f9f9f9" if i % 2 == 0 else "white"
            c += rect(x, y, col_width, row_height, fill=bg, stroke="#eee")
            c += text(x + col_width // 2, y + row_height // 2 + 5, cell,
                      size=12, color=COLORS["dark_gray"])
    
    return make_svg(c, width, height)


def three_panel(title, panels, width=800, height=350):
    """
    Three equal panels side by side — great for before/during/after, 
    three conditions, three types, etc.
    
    Args:
        title: Main heading
        panels: List of 3 dicts: {"title": str, "items": [str], "color": str}
    
    Usage:
        svg = three_panel("Three Types of Selection", [
            {"title": "Stabilizing", "items": ["Average wins", "Extremes removed"], "color": "blue"},
            {"title": "Directional", "items": ["One extreme wins", "Curve shifts"], "color": "orange"},
            {"title": "Disruptive", "items": ["Both extremes win", "Middle removed"], "color": "purple"},
        ])
    """
    c = ""
    c += text(400, 35, title, size=20, color=COLORS["dark_gray"], bold=True)
    
    panel_w = 220
    gap = 20
    start_x = (width - (3 * panel_w + 2 * gap)) // 2
    
    for i, panel in enumerate(panels[:3]):
        x = start_x + i * (panel_w + gap)
        color = COLORS.get(panel.get("color", "blue"), COLORS["blue"])
        light = COLORS.get(f"light_{panel.get('color', 'blue')}", "#e3f2fd")
        
        # Panel box
        c += rect(x, 55, panel_w, height - 75, fill=light, stroke=color)
        
        # Panel header
        c += rect(x, 55, panel_w, 40, fill=color, stroke=color)
        c += text(x + panel_w // 2, 82, panel["title"], size=14, color="white", bold=True)
        
        # Items
        for j, item in enumerate(panel.get("items", [])):
            y = 120 + j * 30
            c += text(x + panel_w // 2, y, item, size=12, color=COLORS["dark_gray"])
    
    return make_svg(c, width, height)
