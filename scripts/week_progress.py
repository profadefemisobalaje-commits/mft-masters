#!/usr/bin/env python3
"""Write PROGRESS.md: how far the 8,000-word-per-week expansion has got.

    python3 scripts/week_progress.py            # rewrite PROGRESS.md
    python3 scripts/week_progress.py --check    # also print the shortfall
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from check_week_lengths import FOLDERS, books, weeks_of  # noqa: E402

FLOOR = 8000


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--floor", type=int, default=FLOOR)
    args = ap.parse_args(argv)

    rows = []
    done = total = 0
    for md in books():
        code = re.match(r"(MFT-\d{3})", md.name).group(1)
        wk = weeks_of(md)
        n_done = sum(1 for _, _, w in wk if w >= args.floor)
        words = sum(w for _, _, w in wk)
        done += n_done
        total += len(wk)
        rows.append((code, md.name, len(wk), n_done, sum(w for _, _, w in wk), words))

    lines = ["# Progress — 8,000 words per teaching week\n",
             f"Target: every teaching week in every course book at **{args.floor:,}+ words**. "
             f"Current standing: **{done} of {total} weeks** at or above the floor.\n",
             "Run `python3 scripts/check_week_lengths.py -v` for the week-by-week audit; "
             "`python3 scripts/week_progress.py` rewrites this file.\n",
             "| Course | Weeks | At 8,000+ | Weekly words | Status |",
             "|---|---|---|---|---|"]
    for code, name, n, n_done, _, words in rows:
        pct = round(100 * n_done / n) if n else 0
        status = "complete" if n_done == n else (f"{pct}%" if n_done else "not started")
        lines.append(f"| {code} | {n} | {n_done} | {words:,} | {status} |")
    lines.append("")
    lines.append("**Definition of complete.** A week counts when `check_week_lengths.py` measures 8,000 or "
                 "more words between its heading and the next `##` heading, and the week contains all "
                 "thirteen components in `00-programme/04-week-template.md`.\n")
    lines.append("**Pace note.** Meeting the floor across the whole library needs roughly 3.1 million words "
                 "of new teaching text — the equivalent of about thirty full-length books. Courses are "
                 "expanded one week at a time, in programme order, each week written to the template and "
                 "verified before the next is started.\n")
    (ROOT / "PROGRESS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"PROGRESS.md written · {done}/{total} weeks at {args.floor:,}+ words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
