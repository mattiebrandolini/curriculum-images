#!/usr/bin/env python3
"""Generate img10: Why This Matters — Your Cells Right Now.
Shows three real examples of cell transport happening in the body."""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent / 'generators'))
from templates import three_panel

svg = three_panel(
    "Transport in Your Body Now",
    [
        {
            "title": "Lungs",
            "items": ["O\u2082 diffuses in", "(diffusion)"],
            "color": "blue",
        },
        {
            "title": "Kidneys",
            "items": ["Water moves out", "(osmosis)"],
            "color": "teal",
        },
        {
            "title": "Intestines",
            "items": ["Nutrients absorbed", "(active transport)"],
            "color": "orange",
        },
    ],
    height=280,
)

out = __import__('pathlib').Path(__file__).parent / "Checkpoint_13_Cell_Transport_img10.svg"
out.write_text(svg, encoding="utf-8")
print(f"Saved: {out}")
