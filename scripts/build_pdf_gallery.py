#!/usr/bin/env python3
"""Build the PDF cover gallery: `pdf/index.html` plus `pdf/thumbs/*.jpg`.

Reads the finished PDFs in `pdf/`, renders the cover of each one to a
thumbnail, and writes a single page from which any course can be opened in one
click. Run it after `build_pdfs.py`.

    python3 scripts/build_pdf_gallery.py
    python3 scripts/build_pdf_gallery.py --zip   # also rebuild the download bundle

Requires pypdfium2 and pillow.
"""
from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "pdf"
THUMBS = PDF / "thumbs"

SEMESTERS = [
    ("Semester One", {"701", "702", "703", "704", "705", "706", "707", "708"}),
    ("Semester Two", {"709", "710", "711", "712", "713", "714", "715"}),
    ("Semester Three", {"716", "717", "718", "719", "720", "721", "770"}),
    ("Electives", {"722", "723", "724", "725", "726", "727"}),
]

PROGRAMME = [
    ("PD 00", "Programme Handbook", "00-programme-handbook"),
    ("PD 01", "Teaching and Assessment Guide", "01-teaching-and-assessment-guide"),
    ("PD 02", "Figure Index", "02-figure-index"),
    ("PD 03", "Figure Gallery — all 40 diagrams", "03-figure-gallery"),
]


def titles():
    out = {}
    for md in ROOT.glob("0[1-4]*/*.md"):
        head = md.read_text(encoding="utf-8").splitlines()[0]
        m = re.match(r"#\s+MFT\s*(\d{3})\s*[—–-]\s*(.*)", head)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def thumb(pdf_path: Path) -> Path:
    THUMBS.mkdir(parents=True, exist_ok=True)
    out = THUMBS / (pdf_path.stem + ".jpg")
    doc = pdfium.PdfDocument(pdf_path)
    img = doc[0].render(scale=1.0).to_pil().convert("RGB")
    img.thumbnail((520, 736), Image.LANCZOS)
    img.save(out, quality=82, optimize=True)
    return out


def card(href: str, code: str, title: str, meta: str, image: str) -> str:
    return f'''<a class="card" href="{html.escape(href)}" target="_blank" rel="noopener">
  <img src="{html.escape(image)}" alt="Cover of {html.escape(code)}" loading="lazy">
  <div class="body">
    <div class="code">{html.escape(code)}</div>
    <div class="title">{html.escape(title)}</div>
    <div class="meta">{html.escape(meta)}</div>
  </div>
</a>'''


CSS = """
:root{--ink:#1b262c;--muted:#6c7a81;--teal:#0d4f4a;--gold:#a87c33;--line:#e2e7e6}
*{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI",-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif;
color:var(--ink);background:#fbfbf9;line-height:1.6}
header{background:#08322e;color:#fff;padding:56px 40px 44px}
header .kicker{color:#d8b676;font-size:12px;letter-spacing:2.4px;text-transform:uppercase;font-weight:700}
header h1{font-size:clamp(28px,4vw,42px);margin:10px 0 8px;letter-spacing:-.5px}
header p{margin:0;color:#9fb3ae;max-width:70ch}
.band{height:5px;background:var(--gold)}
main{max-width:1180px;margin:0 auto;padding:34px 24px 80px}
.lead{display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;
background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 22px;margin:0 0 26px}
.lead p{margin:0;font-size:15px}
.btn{display:inline-block;background:var(--teal);color:#fff;text-decoration:none;font-weight:600;
font-size:14px;padding:11px 18px;border-radius:9px;margin:3px 4px 3px 0}
.btn.alt{background:#fff;color:var(--teal);border:1.5px solid var(--teal)}
h2{font-size:13px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);
margin:38px 0 14px;padding-bottom:8px;border-bottom:1px solid var(--line)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(228px,1fr));gap:20px}
.card{background:#fff;border:1px solid var(--line);border-radius:13px;overflow:hidden;
text-decoration:none;color:inherit;display:flex;flex-direction:column;
transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease}
.card:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(8,50,46,.14);border-color:var(--teal)}
.card img{width:100%;display:block;border-bottom:1px solid var(--line);background:#eee}
.card .body{padding:13px 15px 16px}
.code{font-weight:700;color:var(--gold);font-size:12.5px;letter-spacing:.8px}
.title{font-weight:600;font-size:14.5px;line-height:1.35;margin:3px 0 7px}
.meta{font-size:11.5px;color:var(--muted)}
footer{border-top:1px solid var(--line);margin-top:46px;padding-top:18px;font-size:12.5px;color:var(--muted)}
footer a{color:var(--teal)}
@media print{header{background:#fff;color:#08322e;padding:0 0 18px}.band,.btn{display:none}
.card:hover{transform:none;box-shadow:none}.grid{grid-template-columns:repeat(3,1fr)}}
"""


def build(make_zip: bool = False) -> int:
    known = titles()
    groups = []
    total_pages = 0
    for label, codes in SEMESTERS:
        files = []
        for p in sorted(PDF.glob("MFT-*.pdf")):
            m = re.search(r"MFT-(\d{3})", p.name)
            if not m or "Library" in p.name or m.group(1) not in codes:
                continue
            doc = pdfium.PdfDocument(p)
            pages = len(doc)
            total_pages += pages
            files.append((m.group(1), p, pages))

        def order(item):
            return ("770" if item[0] == "770" else item[0])

        files.sort(key=order)
        cards = []
        for code, path, pages in files:
            thumb(path)
            cards.append(card(path.name, f"MFT {code}", known.get(code, path.stem),
                              f"{pages} pages · {path.stat().st_size / 1024:.0f} KB · A4 PDF",
                              f"thumbs/{path.stem}.jpg"))
        groups.append((label, cards))

    prog_cards = []
    for code, label, stem in PROGRAMME:
        path = PDF / f"{stem}.pdf"
        if not path.exists():
            continue
        thumb(path)
        prog_cards.append(card(path.name, code, label,
                               f"{len(pdfium.PdfDocument(path))} pages · A4 PDF",
                               f"thumbs/{path.stem}.jpg"))

    merged = PDF / "MFT-Library-Complete-28-volumes.pdf"
    merged_pages = len(pdfium.PdfDocument(merged)) if merged.exists() else 0
    n_books = sum(len(c) for _, c in groups)

    body = "".join(f"<h2>{html.escape(label)}</h2><div class=\"grid\">{''.join(cards)}</div>"
                   for label, cards in groups)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MSc Marriage and Family Therapy — print edition ({n_books} PDFs)</title>
<style>{CSS}</style></head>
<body>
<header>
  <div class="kicker">MSc Marriage and Family Therapy</div>
  <h1>Final PDFs — all {n_books} course subjects</h1>
  <p>Print-ready A4 books, one per course, plus the whole programme bound into a single file. Each opens
     with a cover, imprint, contents with page numbers, running heads, embedded figures and bookmarks.</p>
</header>
<div class="band"></div>
<main>
  <div class="lead">
    <p><b>{n_books} course PDFs · {total_pages} pages · 40 figures · CC BY 4.0</b><br>
       Click any cover to open that course's PDF.</p>
    <div>
      <a class="btn" href="{merged.name}" target="_blank" rel="noopener">Complete library — {merged_pages} pages, one file</a>
      <a class="btn alt" href="README.md">Print-edition notes</a>
      <a class="btn alt" href="../MFT-All-28-Course-PDFs.zip">Download all {n_books} (zip)</a>
    </div>
  </div>
  {body}
  <h2>Programme documents</h2>
  <div class="grid">{''.join(prog_cards)}</div>
  <footer>
    Generated from the Markdown source by <code>scripts/build_pdfs.py</code> and
    <code>scripts/build_pdf_gallery.py</code>. Typeset in DejaVu Serif and DejaVu Sans; every figure drawn by
    <code>scripts/</code>. Licence CC BY 4.0 —
    <a href="../README.md">library home</a> · <a href="../site/index.html">HTML edition</a>.
  </footer>
</main>
</body></html>'''
    (PDF / "index.html").write_text(page, encoding="utf-8")

    if make_zip:
        bundle = ROOT / "MFT-All-28-Course-PDFs.zip"
        bundle.unlink(missing_ok=True)
        subprocess.run(["zip", "-q", "-9", str(bundle)] + [p.name for p in sorted(PDF.glob("MFT-7*.pdf"))],
                       check=True, cwd=PDF)
        print(f"bundle  {bundle.name}  {bundle.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"gallery {PDF / 'index.html'}  ({n_books} books, {total_pages} pages, "
          f"{len(list(THUMBS.glob('*.jpg')))} covers)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--zip", action="store_true", help="also rebuild the all-courses download bundle")
    args = ap.parse_args()
    sys.exit(build(make_zip=args.zip))
