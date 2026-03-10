# Curriculum Image Generation — Claude Code Instructions

## THE MISSION
Generate programmatic SVG diagrams for 529 image slots across 3 subjects.
These replace broken external image links in Mattie's ELL curriculum.

## REPO
~/curriculum-images/
- `manifest.json` — tracks every slot (status: needed/generated/approved/rejected)
- `generators/svg_base.py` — shared utilities (colors, shapes, text helpers)
- `generators/bio_13_cell_transport.py` — EXAMPLE: follow this pattern exactly
- `bio/`, `chem/`, `envbio/` — output SVG directories

## HOW TO GENERATE
1. Read manifest.json to find "needed" slots
2. For each lesson, create `generators/{subj}_{cp_num}_{short_name}.py`
3. Each slot = one function that returns an SVG string via make_svg()
4. Run the generator to produce SVGs in the subject folder
5. Update manifest status to "generated"
6. Git commit periodically

## THE PATTERN (read the example file first!)
```python
from svg_base import *

def img01_concept_name():
    content = ""
    content += text(400, 30, "Title", size=20, color=COLORS["blue"], bold=True)
    # ... build the diagram ...
    return make_svg(content, 800, 500)

if __name__ == "__main__":
    generators = {"01": img01_concept_name, ...}
    for slot, func in generators.items():
        svg = func()
        save_svg(svg, f"subject/Lesson_Name_img{slot}.svg")
        update_manifest("subject", "Lesson_Key", slot)
```

## STYLE RULES FOR ELL STUDENTS
- Max 15 words of text per diagram
- Labels: 14-16px, bold, high contrast
- Use color-coding over text where possible
- Arrows to show direction/flow
- Simple shapes — circles for molecules, rectangles for structures
- White background, clean lines
- Consistent color palette from COLORS dict
- Spanish cognates in parentheses where helpful: "cell (célula)"

## WHAT EACH IMAGE TYPE NEEDS

### Diagrams (most common):
- Labeled parts, clear arrows, color coding
- Examples: cell transport, DNA structure, chemical bonds

### Process/Cycle diagrams:
- Circular or linear flow with numbered steps
- Arrows showing direction
- Examples: cell cycle, carbon cycle, lytic cycle

### Comparison diagrams:
- Side-by-side with clear visual differences
- Shared color scheme for same concepts
- Examples: mitosis vs meiosis, ionic vs covalent

### Real-world connection images:
- Simple iconic representations (not photos — we can't generate photos)
- Examples: IV bag, wilting plant → use labeled simplified drawings

## PRIORITY ORDER
Work through subjects in this order (matches Mattie's teaching schedule):
1. **Bio** Checkpoints 13-38 (236 slots) — MCAS prep, most urgent
2. **Chem** Checkpoints 01-26 (143 slots)  
3. **EnvBio** Checkpoints 01-26 (150 slots)

Within Bio, prioritize in this order:
- CP 13-23 (Cell transport through Meiosis) — current unit
- CP 24-31 (Classification through Mutations) — upcoming
- CP 32-38 (Evolution through Homeostasis) — last unit

## GIT WORKFLOW
After every 2-3 lessons worth of generators:
```bash
cd ~/curriculum-images
git add -A
git commit -m "Generate: [subject] CP [numbers] - [brief description]"
git push
```

## QUALITY > SPEED
A simple, clear, correct diagram is better than a fancy broken one.
If a concept is too complex for one SVG, make it simpler rather than cramped.
When in doubt, use the two-panel comparison layout — it works for almost anything.
