#!/usr/bin/env python3
"""Quick test: run exactly 10 slots through orchestrator to measure usage."""
import json, subprocess, re, time
from pathlib import Path

REPO = Path.home() / "curriculum-images"
MANIFEST = REPO / "manifest.json"
CLEANED = Path("/mnt/c/Users/Randk/Downloads/curriculum_processed")

def extract_context(html_path, slot_num):
    text = html_path.read_text(encoding="utf-8", errors="replace")
    pattern = rf'<!-- IMAGE REMOVED: \S+_(?:img|bg){int(slot_num):02d}\.\w+ \(alt: ([^)]+)\) -->'
    match = re.search(pattern, text)
    if not match:
        pattern = rf'<!-- IMAGE REMOVED: \S+_(?:img|bg){slot_num}\.\w+ \(alt: ([^)]+)\) -->'
        match = re.search(pattern, text)
    if not match:
        return None, None
    alt = match.group(1)
    start = max(0, match.start() - 500)
    end = min(len(text), match.end() + 500)
    ctx = re.sub(r'<[^>]+>', ' ', text[start:end])
    ctx = re.sub(r'\s+', ' ', ctx).strip()
    return alt, ctx

def build_prompt(subj, lesson, slot, alt, ctx, output):
    return f"""Generate ONE SVG diagram and save it to: {output}

Subject: {subj.upper()}
Lesson: {lesson.replace('_', ' ')}
Slot: {slot}
Section heading: {alt}

Surrounding lesson content:
---
{ctx}
---

INSTRUCTIONS:
1. Read ~/curriculum-images/generators/svg_base.py and ~/curriculum-images/generators/templates.py
2. Write a short Python script that imports from those files and generates the SVG
3. Use templates (comparison_diagram, process_flow, table_diagram, three_panel, cycle_diagram, labeled_diagram) when possible — most diagrams fit one of these
4. Only hand-code SVG coordinates if no template fits
5. Run your script to produce the SVG file
6. Do NOT modify any other files in the repo

STYLE: For ELL high school students. Max 15 words text. 800px wide. White background. 
Bold labels 14-16px. Color-coded. Clear arrows for flow/direction.
If concept needs a real photo, make a clean labeled placeholder diagram instead."""

manifest = json.loads(MANIFEST.read_text())

# Collect first 10 "needed" slots in bio priority order
tasks = []
for lesson_key in sorted(manifest["bio"].keys()):
    for slot_num, slot_data in sorted(manifest["bio"][lesson_key]["slots"].items()):
        if slot_data["status"] == "needed" and len(tasks) < 10:
            tasks.append(("bio", lesson_key, slot_num, slot_data))
    if len(tasks) >= 10:
        break

print(f"TEST RUN: {len(tasks)} slots")
print(f"Started: {time.strftime('%H:%M:%S')}")
print()

completed = 0
failed = 0

for i, (subj, lesson, slot, data) in enumerate(tasks):
    html = CLEANED / subj / "cleaned" / f"{lesson}.html"
    alt, ctx = extract_context(html, slot)
    if not ctx:
        print(f"  [{i+1}/10] SKIP {lesson} slot {slot} — no context")
        failed += 1
        continue
    
    output = REPO / subj / f"{lesson}_img{slot.zfill(2)}.svg"
    output.parent.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(subj, lesson, slot, alt, ctx, str(output))
    
    print(f"  [{i+1}/10] {lesson} slot {slot}: {alt[:50]}...", end=" ", flush=True)
    start_time = time.time()
    
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--print",
             "--dangerously-skip-permissions", "--model", "opus"],
            capture_output=True, text=True, timeout=300, cwd=str(REPO)
        )
        elapsed = time.time() - start_time
        
        if result.returncode == 0 and output.exists() and output.stat().st_size > 100:
            print(f"✓ ({elapsed:.0f}s, {output.stat().st_size} bytes)")
            completed += 1
            manifest["bio"][lesson]["slots"][slot]["status"] = "generated"
            MANIFEST.write_text(json.dumps(manifest, indent=2))
        else:
            print(f"✗ ({elapsed:.0f}s)")
            failed += 1
            if result.stderr:
                print(f"         stderr: {result.stderr[:150]}")
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"✗ TIMEOUT ({elapsed:.0f}s)")
        failed += 1
    
    time.sleep(5)

print(f"\nDONE: {completed} generated, {failed} failed")
print(f"Finished: {time.strftime('%H:%M:%S')}")
print(f"\nCheck your usage page now!")
