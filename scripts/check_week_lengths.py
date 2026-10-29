#!/usr/bin/env python3
"""Audit the length of every teaching week in the library.

Two editorial standards are enforced here:

  * every teaching week in every course book must run to at least
    ``--floor`` words (default 8,000);
  * the weekly content is counted from the week heading to the next
    heading at the same level, so the running count maps to what a reader
    actually gets in one week.

    python3 scripts/check_week_lengths.py              # table + summary
    python3 scripts/check_week_lengths.py --course MFT-701
    python3 scripts/check_week_lengths.py --fail-under # exit 1 if any week is short
    python3 scripts/check_week_lengths.py --csv report.csv
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDERS = ["01-semester-one", "02-semester-two", "03-semester-three", "04-electives"]
WEEK_RE = re.compile(r"^##\s+Week\s+(\d+)\b[^\n]*$", re.M)


def words(text: str) -> int:
    """Count words the way a reader would: prose, tables and captions."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)      # figure embeds are not prose
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)   # keep link text
    text = re.sub(r"[|#>*_`-]+", " ", text)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-.]*", text))


def weeks_of(md: Path):
    """[(week number, heading, word count)] for one book."""
    text = md.read_text(encoding="utf-8")
    marks = list(WEEK_RE.finditer(text))
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        # stop at the next top-level section if one comes first
        tail = text[m.end():end]
        nxt = re.search(r"^##\s+(?!Week\s)(.{0,80})$", tail, re.M)
        if nxt:
            tail = tail[:nxt.start()]
        out.append((int(m.group(1)), m.group(0).lstrip("# ").strip(), words(tail)))
    return out


def books(course: str | None = None):
    for folder in FOLDERS:
        for md in sorted((ROOT / folder).glob("*.md")):
            if course and course.lower() not in md.name.lower():
                continue
            yield md


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--floor", type=int, default=8000)
    ap.add_argument("--course", help="limit to one course, e.g. MFT-701")
    ap.add_argument("--fail-under", action="store_true", help="exit 1 if any week is short")
    ap.add_argument("--csv", help="also write a CSV report")
    ap.add_argument("--verbose", "-v", action="store_true", help="print every week")
    args = ap.parse_args(argv)

    rows, short = [], 0
    total_words = total_needed = 0
    for md in books(args.course):
        code = re.match(r"(MFT-\d{3})", md.name)
        code = code.group(1) if code else md.stem
        wk = weeks_of(md)
        if not wk:
            continue
        counts = [w for _, _, w in wk]
        deficits = [max(0, args.floor - c) for c in counts]
        short += sum(1 for d in deficits if d)
        total_words += sum(counts)
        total_needed += sum(deficits)
        rows.append({
            "course": code,
            "file": md.name,
            "weeks": len(wk),
            "min": min(counts),
            "mean": round(sum(counts) / len(counts)),
            "max": max(counts),
            "short": sum(1 for d in deficits if d),
            "deficit": sum(deficits),
            "per_week": counts,
        })

    head = f"{'course':9s} {'weeks':>5s} {'min':>6s} {'mean':>6s} {'max':>6s} {'short':>5s} {'words to add':>12s}"
    print(head)
    print("-" * len(head))
    for r in rows:
        print(f"{r['course']:9s} {r['weeks']:5d} {r['min']:6d} {r['mean']:6d} {r['max']:6d} "
              f"{r['short']:5d} {r['deficit']:12,d}")
        if args.verbose:
            for (n, title, c) in weeks_of(ROOT / next(
                    p for p in sorted((ROOT).glob(f"0*/{r['file']}")))):
                flag = "" if c >= args.floor else f"  (+{args.floor - c:,} to go)"
                print(f"    week {n:2d}  {c:6,d}{flag}   {title[10:60]}")

    print("-" * len(head))
    print(f"{len(rows)} course books · {sum(r['weeks'] for r in rows)} teaching weeks · "
          f"{total_words:,} words in weekly content · {short} weeks under {args.floor:,}")
    print(f"words needed to meet the {args.floor:,}-word floor in every week: {total_needed:,}")

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["course", "file", "weeks", "min", "mean", "max", "short", "deficit", "per_week"])
            for r in rows:
                w.writerow([r["course"], r["file"], r["weeks"], r["min"], r["mean"], r["max"],
                            r["short"], r["deficit"], " ".join(map(str, r["per_week"]))])
        print(f"report → {args.csv}")

    if args.fail_under and short:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
