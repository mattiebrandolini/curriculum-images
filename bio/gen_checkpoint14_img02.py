#!/usr/bin/env python3
"""Generate Checkpoint 14 img02: Why Viruses Are Different from Everything Else."""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent / 'generators'))
from templates import comparison_diagram
from svg_base import save_svg

svg = comparison_diagram(
    "Viruses vs. Living Cells",
    "Virus", "Living Cell",
    [
        "No cells",
        "No energy use",
        "Cannot reproduce alone",
        "DNA or RNA (not both)",
        "Not alive",
    ],
    [
        "Made of cells",
        "Uses energy (ATP)",
        "Reproduces on its own",
        "Has DNA and RNA",
        "Alive",
    ],
    left_color="purple",
    right_color="green",
)

save_svg(svg, "bio/Checkpoint_14_Viruses_Immune_Response_img02.svg")
print("Done: bio/Checkpoint_14_Viruses_Immune_Response_img02.svg")
