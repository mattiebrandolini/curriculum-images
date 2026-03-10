#!/usr/bin/env python3
"""
Orchestrator: Dispatches individual Claude Code sessions for SVG generation.
Each session is fresh — zero context rot.

Usage:
    python3 orchestrate.py --resume                    # Run all remaining
    python3 orchestrate.py --resume --max-slots 60     # Tonight's batch
    python3 orchestrate.py --subject bio --resume      # Only bio
    python3 orchestrate.py --dry-run                   # Show plan
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
COMMIT_EVERY = 10


def extract_slot_context(html_path, slot_num):
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


def build_prompt(subj, lesson_key, slot_num, alt_text, context, output_path):
    return f"""Generate ONE SVG diagram and save it to: {output_path}

Subject: {subj.upper()}
Lesson: {lesson_key.replace('_', ' ')}
Slot: {slot_num}
Section heading: {alt_text}

Surrounding lesson content:
---
{context}
---

INSTRUCTIONS:
1. Read ~/curriculum-images/generators/svg_base.py and ~/curriculum-images/generators/templates.py
2. Write a short Python script that imports from those files and generates the SVG
3. Use templates (comparison_diagram, process_flow, table_diagram, three_panel, cycle_diagram, labeled_diagram) when possible
4. Only hand-code SVG coordinates if no template fits
5. Run your script to produce the SVG file
6. Do NOT modify any other files in the repo

STYLE: For ELL high school students (WIDA Level 3). Max 15 words text. 800px wide. White background.
Bold labels 14-16px. Color-coded. Clear arrows for flow/direction.
If concept needs a real photo, make a clean labeled placeholder diagram instead."""


def run_claude_code(prompt, timeout=180, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ["claude", "-p", prompt, "--print",
                 "--dangerously-skip-permissions", "--model", "opus"],
                capture_output=True, text=True, timeout=timeout, cwd=str(REPO)
            )
            stderr_lower = result.stderr.lower() if result.stderr else ""
            if "rate" in stderr_lower or "limit" in stderr_lower or "429" in stderr_lower:
                wait = 30 * (attempt + 1)
                print(f" [rate limited, waiting {wait}s]", end="", flush=True)
                time.sleep(wait)
                continue
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            if attempt < max_retries - 1:
                print(f" [timeout, retry {attempt+1}]", end="", flush=True)
                time.sleep(10)
                continue
            return False, "", "TIMEOUT"
        except Exception as e:
            return False, "", str(e)
    return False, "", "MAX_RETRIES"


def git_commit(message):
    subprocess.run(["git", "add", "-A"], cwd=str(REPO), capture_output=True)
    subprocess.run(["git", "commit", "-m", message], cwd=str(REPO), capture_output=True)
    subprocess.run(["git", "push"], cwd=str(REPO), capture_output=True)


def main():
    parser = argparse.ArgumentParser(description="Orchestrate SVG generation")
    parser.add_argument("--subject", help="Only process this subject (bio/chem/envbio)")
    parser.add_argument("--lesson", help="Only process this lesson key")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without executing")
    parser.add_argument("--resume", action="store_true", help="Skip already-generated slots")
    parser.add_argument("--max-slots", type=int, default=None, help="Max slots to process this run")
    parser.add_argument("--timeout", type=int, default=180, help="Seconds per session")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text())

    # Build task list sorted by checkpoint number across ALL subjects
    raw_tasks = []
    for subj, lessons in manifest.items():
        if args.subject and subj != args.subject:
            continue
        for lesson_key, lesson_data in lessons.items():
            if args.lesson and lesson_key != args.lesson:
                continue
            cp_match = re.search(r'Checkpoint_(\d+)', lesson_key)
            cp_num = int(cp_match.group(1)) if cp_match else 99
            for slot_num, slot_data in lesson_data["slots"].items():
                if args.resume and slot_data["status"] != "needed":
                    continue
                raw_tasks.append((cp_num, subj, lesson_key, slot_num, slot_data))

    raw_tasks.sort(key=lambda x: (x[0], x[1], int(x[3])))
    tasks = [(subj, lk, sn, sd) for (_, subj, lk, sn, sd) in raw_tasks]

    if args.max_slots and len(tasks) > args.max_slots:
        tasks = tasks[:args.max_slots]

    print("=" * 60)
    print("CURRICULUM IMAGE ORCHESTRATOR")
    print("=" * 60)
    print(f"Total tasks: {len(tasks)}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    if args.max_slots:
        print(f"Max slots: {args.max_slots}")
    print()

    if args.dry_run:
        for i, (subj, lesson, slot, data) in enumerate(tasks):
            print(f"  {i+1:3d}. [{subj:6s}] {lesson} slot {slot}: {data['alt'][:60]}")
        return

    completed = 0
    failed = 0
    skipped = 0
    since_commit = 0
    start_time = time.time()

    for i, (subj, lesson_key, slot_num, slot_data) in enumerate(tasks):
        html_file = CLEANED_BASE / subj / "cleaned" / f"{lesson_key}.html"
        if not html_file.exists():
            print(f"  [{i+1}/{len(tasks)}] SKIP {subj}/{lesson_key} slot {slot_num} - no HTML")
            skipped += 1
            continue

        alt_text, context = extract_slot_context(html_file, slot_num)
        if not context:
            print(f"  [{i+1}/{len(tasks)}] SKIP {subj}/{lesson_key} slot {slot_num} - no context")
            skipped += 1
            continue

        output_path = REPO / subj / f"{lesson_key}_img{slot_num.zfill(2)}.svg"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        prompt = build_prompt(subj, lesson_key, slot_num, alt_text, context, str(output_path))

        elapsed_total = time.time() - start_time
        rate = completed / (elapsed_total / 60) if elapsed_total > 60 else 0
        print(f"  [{i+1}/{len(tasks)}] {subj}/{lesson_key} s{slot_num}: {alt_text[:45]}...", end=" ", flush=True)

        success, stdout, stderr = run_claude_code(prompt, timeout=args.timeout)

        if success and output_path.exists() and output_path.stat().st_size > 100:
            size = output_path.stat().st_size
            print(f"OK ({size}B)")
            completed += 1
            since_commit += 1
            manifest[subj][lesson_key]["slots"][slot_num]["status"] = "generated"
            MANIFEST.write_text(json.dumps(manifest, indent=2))
        else:
            reason = "timeout" if "TIMEOUT" in str(stderr) else "no file" if not output_path.exists() else "too small"
            print(f"FAIL ({reason})")
            failed += 1
            log = REPO / "generation_log.txt"
            with open(log, "a") as f:
                f.write(f"FAILED: {subj}/{lesson_key} slot {slot_num} - {reason}\n")

        if since_commit >= COMMIT_EVERY:
            git_commit(f"Generate: batch {completed} images")
            since_commit = 0
            print(f"  [git push - {completed} total]")

        time.sleep(5)

    if since_commit > 0:
        git_commit(f"Generate: {completed} images total")

    elapsed = time.time() - start_time
    print(f"\n{'=' * 60}")
    print(f"DONE in {elapsed/60:.1f} minutes")
    print(f"  Generated: {completed}")
    print(f"  Failed: {failed}")
    print(f"  Skipped: {skipped}")
    print(f"  Rate: {completed/(elapsed/60):.1f} images/min" if elapsed > 60 else "")
    print("=" * 60)


if __name__ == "__main__":
    main()
