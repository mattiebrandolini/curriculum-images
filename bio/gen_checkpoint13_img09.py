#!/usr/bin/env python3
"""Generate Checkpoint 13 img09: Bulk Transport — Moving Big Things."""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'generators'))
from templates import comparison_diagram

svg = comparison_diagram(
    "Bulk Transport",
    "Endocytosis", "Exocytosis",
    ["Into cell", "Wraps material in", "Ex: WBC eats bacteria"],
    ["Out of cell", "Vesicle releases out", "Ex: cell sends hormones"],
    left_color="blue", right_color="orange",
)

output = str(__import__('pathlib').Path(__file__).resolve().parent / "Checkpoint_13_Cell_Transport_img09.svg")
with open(output, "w") as f:
    f.write(svg)
print(f"Saved: {output}")
