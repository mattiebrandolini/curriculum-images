# Curriculum Image Generation — Claude Code Instructions

## THE MISSION
Generate programmatic SVG diagrams for 529 image slots across 3 subjects.
These replace broken external image links in Mattie's ELL curriculum.

## REPO LAYOUT
~/curriculum-images/
- `manifest.json` — tracks every slot (status: needed/generated/approved/rejected)
- `generators/svg_base.py` — shared utilities (colors, shapes, text helpers)
- `generators/templates.py` — REUSABLE LAYOUT TEMPLATES (comparison, process_flow, cycle, table, etc.)
- `generators/bio_13_cell_transport.py` — EXAMPLE: follow this pattern
- `bio/`, `chem/`, `envbio/` — output SVG directories

## CRITICAL: READ THE LESSON BEFORE GENERATING

The alt texts in manifest.json are SECTION HEADINGS, not image descriptions.
"Bulk Transport — Moving Big Things" could be anything without context.

**BEFORE writing any generator file:**
1. Read the cleaned HTML file for that lesson:
   `/mnt/c/Users/Randk/Downloads/curriculum_processed/{subj}/cleaned/{filename}.html`
2. Find each `<!-- IMAGE REMOVED: ... -->` comment in context
3. Read the surrounding section to understand what concept is being taught
4. THEN decide what to draw

This is the difference between a useful diagram and a random shape.

## WORKFLOW PER LESSON
```
1. Read the cleaned HTML for context
2. For each IMAGE REMOVED comment, note:
   - What section is it in?
   - What concept is being taught?
   - What would help an ELL student understand this?
3. Choose the best template from templates.py for each slot
4. Write the generator file, mostly calling templates
5. Run it, check the SVGs render (open in browser or cat the file)
6. Update manifest, commit
```

## USE TEMPLATES — DON'T HAND-CODE COORDINATES

`generators/templates.py` has ready-made layouts. Use them for 80%+ of diagrams:

### comparison_diagram(title, left_title, right_title, left_items, right_items)
- Mitosis vs Meiosis, Ionic vs Covalent, Prokaryote vs Eukaryote
- Any "compare two things" slot

### process_flow(title, steps, direction="horizontal"|"vertical")
- DNA replication steps, lytic cycle, translation
- Any "here's how this works step by step" slot

### cycle_diagram(title, steps)
- Cell cycle, carbon cycle, water cycle, Krebs cycle
- Any circular process

### table_diagram(title, headers, rows)
- Tonicity effects table, transport type comparison, bond properties
- Any "fill in this table" or "compare these properties" slot

### three_panel(title, panels)
- Three types of selection, three bacterial shapes, three domains
- Any "here are three categories" slot

### labeled_diagram(title, parts, connections)
- Virus structure, cell organelles, chloroplast parts
- Any "label the parts of this thing" slot

### Custom SVG (use svg_base.py helpers)
- Only for unique diagrams that don't fit any template
- Punnett squares, pedigree charts, DNA double helix, etc.
- Use the helpers: text(), rect(), circle(), arrow(), label_box()

**MOST SLOTS WILL BE 5-15 LINES OF CODE using templates.**
Only write custom SVG when no template fits.

## EXAMPLE: Template-based generator
```python
from svg_base import *
from templates import *

SUBJECT = "bio"
LESSON = "Checkpoint_19_Mitosis_vs_Meiosis"

def img03_two_jobs():
    return comparison_diagram(
        "Two Types of Cell Division",
        "Mitosis", "Meiosis",
        ["For growth & repair", "2 identical cells", "Body cells (somatic)", "1 division", "46 → 46 chromosomes"],
        ["For reproduction", "4 different cells", "Sex cells (gametes)", "2 divisions", "46 → 23 chromosomes"],
        left_color="blue", right_color="purple"
    )

def img07_side_by_side():
    return table_diagram("Mitosis vs Meiosis Comparison",
        ["Feature", "Mitosis", "Meiosis"],
        [
            ["# of divisions", "1", "2"],
            ["# of cells made", "2", "4"],
            ["Chromosome #", "Same (diploid)", "Half (haploid)"],
            ["Cells identical?", "Yes", "No — unique"],
            ["Purpose", "Growth/repair", "Sex cells"],
        ],
        col_colors=["teal", "blue", "purple"]
    )
```

**See how much shorter that is than hand-coding coordinates?**

## STYLE RULES FOR ELL STUDENTS
- Max 15 words of text per diagram
- Labels: 14-16px, bold, high contrast
- Use color-coding over text where possible
- Spanish cognates in parentheses where helpful: "cell (célula)"
- Simple is better — if a diagram looks cluttered, split into two simpler ones

## PRIORITY ORDER (matches Mattie's teaching schedule)
1. **Bio** Checkpoints 13-23 (current unit, MCAS prep) — DO THESE FIRST
2. **Bio** Checkpoints 24-31 (upcoming)
3. **Bio** Checkpoints 32-38 (last unit)
4. **Chem** Checkpoints 01-26
5. **EnvBio** Checkpoints 01-26

## GIT WORKFLOW
After every 3-5 lessons:
```bash
cd ~/curriculum-images
git add -A
git commit -m "Generate: [subject] CP [numbers] - [brief description]"
git push
```

## QUALITY > SPEED
A simple, correct diagram is better than a fancy broken one.
When in doubt, use comparison_diagram or table_diagram — they work for almost anything.
If a concept is genuinely too visual for programmatic SVG (e.g., "microscope photo of bacteria"),
generate a simple labeled placeholder with the key information as text and mark it in manifest
as "generated" with a note like "placeholder — needs photo".
