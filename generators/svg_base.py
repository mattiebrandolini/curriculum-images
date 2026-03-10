#!/usr/bin/env python3
"""
SVG Generator Framework for Curriculum Images.

Each generator function takes no arguments and returns an SVG string.
SVGs are designed for:
- WIDA Level 3 ELL students (clear labels, minimal text)
- Screen/tablet viewing (readable at 800px wide)
- Clean, professional style matching the curriculum aesthetic

Style guide:
- Background: white or very light gray
- Primary colors: #1565c0 (blue), #00695c (teal), #7b1fa2 (purple), #e65100 (orange)
- Text: 14-16px for labels, 12px for annotations, bold for key terms
- Arrows: clear direction indicators
- Labels: short English words, use color-coding over text where possible
- Font: sans-serif (Arial/Helvetica)
"""

import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MANIFEST = REPO_ROOT / "manifest.json"

# Style constants
COLORS = {
    "blue": "#1565c0",
    "teal": "#00695c", 
    "purple": "#7b1fa2",
    "orange": "#e65100",
    "red": "#c62828",
    "green": "#43a047",
    "light_blue": "#e3f2fd",
    "light_green": "#e8f5e9",
    "light_orange": "#fff3e0",
    "light_purple": "#f3e5f5",
    "light_gray": "#f5f5f5",
    "dark_gray": "#333333",
    "medium_gray": "#666666",
    "membrane": "#FFB74D",
    "water": "#64B5F6",
    "cell_bg": "#FFF9C4",
    "outside_bg": "#E3F2FD",
}

SVG_HEADER = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" 
     width="{width}" height="{height}" style="background: white; font-family: Arial, Helvetica, sans-serif;">
'''

SVG_FOOTER = '</svg>'


def make_svg(content, width=800, height=500):
    """Wrap content in SVG tags."""
    return SVG_HEADER.format(width=width, height=height) + content + SVG_FOOTER


def text(x, y, label, size=14, color="#333", bold=False, anchor="middle"):
    """Generate an SVG text element."""
    weight = "bold" if bold else "normal"
    return f'  <text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{label}</text>\n'


def rect(x, y, w, h, fill="#f5f5f5", stroke="#ccc", rx=4):
    """Generate a rounded rectangle."""
    return f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" rx="{rx}" />\n'


def circle(cx, cy, r, fill="#64B5F6", stroke="#1565c0", sw=2):
    """Generate a circle."""
    return f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" />\n'


def arrow(x1, y1, x2, y2, color="#333", width=2):
    """Generate a line with arrowhead."""
    mid = f"arrow_{x1}_{y1}_{x2}_{y2}"
    return (
        f'  <defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}" /></marker></defs>\n'
        f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{width}" marker-end="url(#{mid})" />\n'
    )


def label_box(x, y, w, h, label, bg="#e3f2fd", border="#1565c0", text_color="#1565c0"):
    """A labeled box - common for diagrams."""
    return (
        rect(x, y, w, h, fill=bg, stroke=border) +
        text(x + w/2, y + h/2 + 5, label, size=14, color=text_color, bold=True)
    )


def save_svg(content, filepath):
    """Save SVG string to file, creating directories as needed."""
    path = REPO_ROOT / filepath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


def update_manifest(subject, lesson_key, slot_num, status="generated"):
    """Update a slot's status in the manifest."""
    with open(MANIFEST) as f:
        data = json.load(f)
    
    if subject in data and lesson_key in data[subject]:
        if slot_num in data[subject][lesson_key]["slots"]:
            data[subject][lesson_key]["slots"][slot_num]["status"] = status
    
    with open(MANIFEST, "w") as f:
        json.dump(data, f, indent=2)
