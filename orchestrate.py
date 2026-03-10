#!/usr/bin/env python3
"""
Orchestrator: Dispatches 529 individual Claude Code sessions,
one per image slot. Each session is fresh — zero context rot.

Usage:
    python3 orchestrate.py                  # Run all "needed" slots
    python3 orchestrate.py --subject bio    # Only bio
    python3 orchestrate.py --lesson Checkpoint_13_Cell_Transport  # Only one lesson
    python3 orchestrate.py --dry-run        # Show what would run, don't execute
    python3 orchestrate.py --resume         # Skip already-generated slots
"""

import json
import subprocess
import sys
import re
import time
import argparse
from pathlib import Path

REPO = Path.home() / "curriculum-images"
MANIFEST = REPO / "manifest.json"
CLEANED_BASE = Path("/mnt/c/Users/Randk/Downloads/curriculum_processed")
SVG_BASE = (REPO / "generators" / "svg_base.py").read_text()
TEMPLATES = (REPO / "generators" / "templates.py").read_text()

# How many slots between git commits
COMMIT_EVERY = 10


def extract_slot_context(html_path, slot_num):
    """Extract ~800 chars of HTML context around a specific IMAGE REMOVED comment."""
    text = html_path.read_text(encoding="utf-8", errors="replace")
    
    pattern = rf'<!-- IMAGE REMOVED: \S+_(?:img|bg){int(slot_num):02d}\.\w+ \(alt: ([^)]+)\) -->'
    match = re.search(pattern, text)
    
    if not match:
        # Try without zero-padding
        pattern = rf'<!-- IMAGE REMOVED: \S+_(?:img|bg){slot_num}\.\w+ \(alt: ([^)]+)\) -->'
        match = re.search(pattern, text)
    
    if not match:
        return None, None
    
    alt_text = match.group(1)
    start = max(0, match.start() - 400)
    end = min(len(text), match.end() + 400)
    context = text[start:end]
    
    # Clean HTML tags for readability but keep structure hints
    context = re.sub(r'<style[^>]*>.*?</style>', '', context, flags=re.DOTALL)
    context = re.sub(r'<[^>]+>', ' ', context)
    context = re.sub(r'\s+', ' ', context).strip()
    
    return alt_text, context


def build_prompt(subject, lesson_key, slot_num, alt_text, context, output_path):
    """Build the self-contained prompt for one Claude Code session."""
    
    return f"""You are generating ONE educational SVG diagram for a high school biology/chemistry curriculum.
The students are English Language Learners (WIDA Level 3 — intermediate English).

## YOUR TASK
Generate a single SVG file and save it to: {output_path}

## WHAT TO DRAW
Subject: {subject.upper()}
Lesson: {lesson_key.replace('_', ' ')}
Slot: {slot_num}
Alt text (section heading): {alt_text}

Here is the surrounding lesson content for context:
---
{context}
---

Based on this context, create a clear, labeled SVG diagram that helps ELL students understand this concept.

## TOOLS AVAILABLE
You have two Python files with SVG generation utilities. Read them first:
- ~/curriculum-images/generators/svg_base.py (colors, shapes, text helpers)  
- ~/curriculum-images/generators/templates.py (reusable layouts: comparison_diagram, process_flow, cycle_diagram, table_diagram, three_panel, labeled_diagram)

## HOW TO GENERATE
Write a short Python script that:
1. Imports from svg_base and templates
2. Calls the appropriate template (or builds custom SVG using helpers)
3. Writes the result to {output_path}

Then run it.

## STYLE RULES
- Max 15 words of text per diagram
- Labels: 14-16px, bold, high contrast  
- Use color-coding over text where possible
- White background, clean lines
- 800px wide, height as needed (300-500px typical)
- If the concept needs a photograph (microscope image, real organism), make a clean placeholder diagram with the key information as labeled text instead

## IMPORTANT
- Use templates from templates.py for 80%+ of diagrams — don't hand-code coordinates unless you must
- Read the lesson context carefully — the alt text is just a section heading, the context tells you what to actually draw
- Generate exactly ONE SVG file at the path specified above
- Do not modify any other files
"""


def run_claude_code(prompt, timeout=180, max_retries=3):
    """Run a single Claude Code session with retries and backoff."""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ["claude", "-p", prompt, "--print",
                 "--dangerously-skip-permissions",
                 "--model", "sonnet"],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(REPO)
            )
            # Check for rate limit in stderr
            if "rate" in result.stderr.lower() or "limit" in result.stderr.lower() or "429" in result.stderr:
                wait = 30 * (attempt + 1)
                print(f"
    Rate limited, waiting {wait}s (attempt {attempt+1}/{max_retries})...", end="", flush=True)
                time.sleep(wait)
                continue
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            if attempt < max_retries - 1:
                print(f"
    Timeout, retrying ({attempt+1}/{max_retries})...", end="", flush=True)
                time.sleep(10)
                continue
            return False, "", "TIMEOUT"
        except Exception as e:
            return False, "", str(e)
    return False, "", "MAX_RETRIES"


def git_commit(message):
    """Commit and push current changes."""
    subprocess.run(["git", "add", "-A"], cwd=str(REPO), capture_output=True)
    subprocess.run(["git", "commit", "-m", message], cwd=str(REPO), capture_output=True)
    subprocess.run(["git", "push"], cwd=str(REPO), capture_output=True)


def main():
    parser = argparse.ArgumentParser(description="Orchestrate SVG generation")
    parser.add_argument("--subject", help="Only process this subject (bio/chem/envbio)")
    parser.add_argument("--lesson", help="Only process this lesson key")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without executing")
    parser.add_argument("--resume", action="store_true", help="Skip already-generated slots")
    parser.add_argument("--timeout", type=int, default=120, help="Seconds per session")
    args = parser.parse_args()
    
    # Load manifest
    manifest = json.loads(MANIFEST.read_text())
    
    # Build task list
    tasks = []
    for subj, lessons in manifest.items():
        if args.subject and subj != args.subject:
            continue
        for lesson_key, lesson_data in lessons.items():
            if args.lesson and lesson_key != args.lesson:
                continue
            for slot_num, slot_data in lesson_data["slots"].items():
                if args.resume and slot_data["status"] != "needed":
                    continue
                tasks.append((subj, lesson_key, slot_num, slot_data))
    
    print(f"{'='*60}")
    print(f"CURRICULUM IMAGE ORCHESTRATOR")
    print(f"{'='*60}")
    print(f"Total tasks: {len(tasks)}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"Timeout per task: {args.timeout}s")
    print()
    
    if args.dry_run:
        for subj, lesson, slot, data in tasks:
            print(f"  [{subj}] {lesson} slot {slot}: {data['alt'][:60]}")
        return
    
    # Process
    completed = 0
    failed = 0
    skipped = 0
    since_commit = 0
    
    for i, (subj, lesson_key, slot_num, slot_data) in enumerate(tasks):
        # Find the HTML file
        cleaned_dir = CLEANED_BASE / subj / "cleaned"
        html_file = cleaned_dir / f"{lesson_key}.html"
        
        if not html_file.exists():
            print(f"  [{i+1}/{len(tasks)}] SKIP {subj}/{lesson_key} slot {slot_num} — HTML not found")
            skipped += 1
            continue
        
        # Extract context
        alt_text, context = extract_slot_context(html_file, slot_num)
        if not context:
            print(f"  [{i+1}/{len(tasks)}] SKIP {subj}/{lesson_key} slot {slot_num} — context not found")
            skipped += 1
            continue
        
        # Build output path
        output_path = REPO / subj / f"{lesson_key}_img{slot_num.zfill(2)}.svg"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build and run prompt
        prompt = build_prompt(subj, lesson_key, slot_num, alt_text, context, str(output_path))
        
        print(f"  [{i+1}/{len(tasks)}] {subj}/{lesson_key} slot {slot_num}: {alt_text[:50]}...", end=" ", flush=True)
        
        success, stdout, stderr = run_claude_code(prompt, timeout=args.timeout)
        
        # Verify output
        if success and output_path.exists() and output_path.stat().st_size > 100:
            print("✓")
            completed += 1
            since_commit += 1
            
            # Update manifest
            manifest[subj][lesson_key]["slots"][slot_num]["status"] = "generated"
            MANIFEST.write_text(json.dumps(manifest, indent=2))
        else:
            reason = "timeout" if "TIMEOUT" in stderr else "no output" if not output_path.exists() else "too small"
            print(f"✗ ({reason})")
            failed += 1
            
            # Log failure
            log = REPO / "generation_log.txt"
            with open(log, "a") as f:
                f.write(f"FAILED: {subj}/{lesson_key} slot {slot_num} — {reason}\n")
                if stderr and "TIMEOUT" not in stderr:
                    f.write(f"  stderr: {stderr[:200]}\n")
        
        # Git commit periodically
        if since_commit >= COMMIT_EVERY:
            git_commit(f"Generate: {subj} batch — {completed} images so far")
            since_commit = 0
            print(f"  [committed and pushed]")
        
        # Brief pause between sessions
        time.sleep(5)
    
    # Final commit
    if since_commit > 0:
        git_commit(f"Generate: final batch — {completed} total images")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"COMPLETE")
    print(f"  Generated: {completed}")
    print(f"  Failed: {failed}")
    print(f"  Skipped: {skipped}")
    print(f"  Total: {completed + failed + skipped}/{len(tasks)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
