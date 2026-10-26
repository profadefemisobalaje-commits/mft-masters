#!/usr/bin/env python3
"""Build the print edition: one A4 PDF per course book.

The Markdown files are the source of truth. This script parses the same
Markdown dialect used by ``build_site.py`` and typesets each book as a
standalone, print-ready PDF with a cover, imprint page, contents with real
page numbers, running heads, folios, PDF bookmarks, styled tables, callout
panels and embedded figures.

    python3 scripts/build_pdfs.py                 # all course books
    python3 scripts/build_pdfs.py --only MFT-701  # one book
    python3 scripts/build_pdfs.py --programme     # include programme docs

Requirements: reportlab, pillow, and node with @resvg/resvg-js for the
SVG -> PNG conversion (NODE_PATH is probed automatically).
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "pdf"
CACHE = ROOT / ".build" / "figcache"
SVG2PNG = ROOT / "scripts" / "svg2png.js"

SECTIONS = [
    ("01-semester-one", "Semester One"),
    ("02-semester-two", "Semester Two"),
    ("03-semester-three", "Semester Three"),
    ("04-electives", "Electives"),
    ("00-programme", "Programme"),
]

# ------------------------------------------------------------------ palette

INK = colors.HexColor("#16232B")
BODY = colors.HexColor("#243139")
MUTED = colors.HexColor("#6C7A81")
TEAL = colors.HexColor("#0D4F4A")
TEAL_DEEP = colors.HexColor("#08322E")
GOLD = colors.HexColor("#A87C33")
GOLD_LIGHT = colors.HexColor("#D8B676")
RULE = colors.HexColor("#D7DEDD")
PANEL = colors.HexColor("#F4F6F5")
WHITE = colors.white

LIBRARY = []  # [(code, title, semester, units, filename)] filled in main()

KINDS = {
    "case": (colors.HexColor("#0D4F4A"), colors.HexColor("#EDF5F4")),
    "practical": (colors.HexColor("#1D4E89"), colors.HexColor("#EDF2FA")),
    "dialog": (colors.HexColor("#46545E"), colors.HexColor("#F3F5F7")),
    "caution": (colors.HexColor("#8E1F35"), colors.HexColor("#FBEEF0")),
    "reflect": (colors.HexColor("#5B3A8C"), colors.HexColor("#F4F0FB")),
    "debate": (colors.HexColor("#A87C33"), colors.HexColor("#FBF5E9")),
    "key": (colors.HexColor("#1D6B3A"), colors.HexColor("#EEF7F1")),
    "note": (colors.HexColor("#6C7A81"), colors.HexColor("#F5F7F7")),
}

LABEL_KIND = {
    "CASE": "case", "CASE PLAN": "case",
    "PRACTICAL": "practical", "TASK": "practical", "DRILL": "practical",
    "REHEARSAL": "practical", "ARTEFACT": "practical", "ASSESSED": "practical",
    "EXERCISE": "practical", "PRACTICE": "practical",
    "CAUTION": "caution", "WARNING": "caution", "RISK": "caution",
    "REFLECT": "reflect", "AUDIT": "reflect", "SUPERVISION": "reflect",
    "DEBATE": "debate", "DIALOGUE": "dialog", "KEY": "key", "NOTE": "note",
}

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

# ------------------------------------------------------------------ styles


def _oblique(src: Path, dst: Path, shear: float = 0.20) -> Path:
    """Synthesise an oblique face by shearing the outlines of the upright one."""
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.ttLib import TTFont as FTFont

    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    f = FTFont(str(src))
    glyf = f["glyf"]
    for name in f.getGlyphOrder():
        g = glyf[name]
        pen = TTGlyphPen(glyf)
        try:
            g.draw(TransformPen(pen, (1, 0, shear, 1, 0, 0)), glyf)
        except Exception:
            continue
        glyf[name] = pen.glyph()
    f.save(str(dst))
    return dst


def register_fonts():
    synth = ROOT / ".build" / "fonts"
    faces = {
        "Serif": "DejaVuSerif.ttf",
        "Serif-Bold": "DejaVuSerif-Bold.ttf",
        "Sans": "DejaVuSans.ttf",
        "Sans-Bold": "DejaVuSans-Bold.ttf",
        "Mono": "DejaVuSansMono.ttf",
    }
    for name, file in faces.items():
        pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / file)))
    # italics: use the shipped face if there is one, otherwise shear the upright
    for name, src_file, shipped_file, shear in (
            ("Serif-Italic", "DejaVuSerif.ttf", "DejaVuSerif-Italic.ttf", 0.20),
            ("Serif-BoldItalic", "DejaVuSerif-Bold.ttf", "DejaVuSerif-BoldItalic.ttf", 0.20),
            ("Sans-Oblique", "DejaVuSans.ttf", "DejaVuSans-Oblique.ttf", 0.18)):
        shipped = FONT_DIR / shipped_file
        path = shipped if shipped.exists() else _oblique(FONT_DIR / src_file, synth / f"{name}.ttf", shear)
        pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold",
                                  italic="Serif-Italic", boldItalic="Serif-BoldItalic")
    pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold",
                                  italic="Sans-Oblique", boldItalic="Sans-Bold")


def styles():
    s = {}
    s["body"] = ParagraphStyle(
        "body", fontName="Serif", fontSize=10.15, leading=15.1, textColor=BODY,
        alignment=TA_JUSTIFY, spaceAfter=7.2, splitLongWords=1, allowWidows=0, allowOrphans=0)
    s["h2"] = ParagraphStyle(
        "h2", fontName="Sans-Bold", fontSize=14, leading=18, textColor=TEAL,
        spaceBefore=4, spaceAfter=8, keepWithNext=1)
    s["h3"] = ParagraphStyle(
        "h3", fontName="Sans-Bold", fontSize=10.4, leading=13.6, textColor=INK,
        spaceBefore=13, spaceAfter=4.5, keepWithNext=1)
    s["h4"] = ParagraphStyle(
        "h4", fontName="Sans-Bold", fontSize=9.4, leading=12.5, textColor=colors.HexColor("#37505A"),
        spaceBefore=10, spaceAfter=3, keepWithNext=1)
    s["caption"] = ParagraphStyle(
        "caption", fontName="Serif-Italic", fontSize=8.1, leading=11.2, textColor=MUTED,
        spaceBefore=5, spaceAfter=12, alignment=TA_LEFT)
    s["quote"] = ParagraphStyle(
        "quote", fontName="Serif", fontSize=9.7, leading=14.4, textColor=BODY,
        alignment=TA_JUSTIFY, spaceAfter=0)
    s["quotelabel"] = ParagraphStyle(
        "quotelabel", fontName="Sans-Bold", fontSize=7.2, leading=9.5, textColor=MUTED,
        spaceAfter=3)
    s["cell"] = ParagraphStyle(
        "cell", fontName="Serif", fontSize=8.2, leading=11.1, textColor=BODY, alignment=TA_LEFT)
    s["cellhead"] = ParagraphStyle(
        "cellhead", fontName="Sans-Bold", fontSize=7.9, leading=10.6, textColor=colors.HexColor("#123B37"))
    s["bullet"] = ParagraphStyle(
        "bullet", parent=s["body"], leftIndent=15, bulletIndent=3, spaceAfter=3.4)
    s["toc0"] = ParagraphStyle(
        "toc0", fontName="Serif", fontSize=9.6, leading=17, textColor=INK, leftIndent=0)
    s["toc1"] = ParagraphStyle(
        "toc1", parent=s["toc0"], fontSize=9.0, leading=14.5, leftIndent=20,
        textColor=colors.HexColor("#3D4A51"))
    s["tocTitle"] = ParagraphStyle(
        "tocTitle", fontName="Sans-Bold", fontSize=20, leading=24, textColor=TEAL, spaceAfter=4)
    s["imprintTitle"] = ParagraphStyle(
        "imprintTitle", fontName="Serif-Bold", fontSize=19, leading=25, textColor=INK, spaceAfter=6)
    s["imprint"] = ParagraphStyle(
        "imprint", fontName="Serif", fontSize=9.4, leading=14.2, textColor=BODY, alignment=TA_JUSTIFY,
        spaceAfter=7)
    s["small"] = ParagraphStyle(
        "small", fontName="Serif", fontSize=8.4, leading=12.4, textColor=MUTED, spaceAfter=5)
    s["code"] = ParagraphStyle(
        "code", fontName="Mono", fontSize=7.8, leading=11, textColor=INK,
        backColor=PANEL, borderPadding=6, leftIndent=2, spaceBefore=4, spaceAfter=10)
    return s


# ------------------------------------------------------------------ figures


def _node_env():
    env = os.environ.copy()
    if not env.get("NODE_PATH"):
        for cand in ("/tmp/rend/node_modules", str(ROOT / "node_modules")):
            if Path(cand).is_dir():
                env["NODE_PATH"] = cand
                break
    return env


def ensure_png(svg: Path, width: int = 2000) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    stamp = f"{svg.name}:{svg.stat().st_mtime_ns}:{width}"
    key = hashlib.sha1(stamp.encode()).hexdigest()[:10]
    out = CACHE / f"{svg.stem}-{key}.png"
    if out.exists() and out.stat().st_size > 0:
        return out
    node = shutil.which("node")
    if not node:
        raise SystemExit("node is required to rasterise figures for the PDF edition")
    subprocess.run([node, str(SVG2PNG), str(svg), str(out), str(width)],
                   check=True, env=_node_env())
    return out


# ------------------------------------------------------------------ markdown


def inline(text: str) -> str:
    """Markdown inline -> ReportLab paragraph markup."""
    t = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"`([^`]+)`", r'<font name="Mono" size="8.2" color="#123B37">\1</font>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", t)

    def link(m):
        label, href = m.group(1), m.group(2)
        if href.startswith(("http://", "https://")):
            return f'<link href="{href}" color="#0D4F4A">{label}</link>'
        return label

    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, t)
    t = t.replace("&amp;lt;", "&lt;").replace("&amp;gt;", "&gt;")
    return t


def clean_len(cell: str) -> int:
    return len(re.sub(r"[*`\[\]()]", "", cell))


def parse_blocks(md: str):
    lines = md.split("\n")
    blocks, i = [], 0
    in_code = False
    while i < len(lines):
        ln = lines[i]
        st = ln.strip()

        if st.startswith("```"):
            if in_code:
                blocks.append({"t": "code", "text": "\n".join(buf)})
                in_code = False
            else:
                buf, in_code = [], True
            i += 1
            continue
        if in_code:
            buf.append(ln)
            i += 1
            continue
        if not st:
            i += 1
            continue

        mi = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", st)
        if mi:
            blocks.append({"t": "img", "alt": mi.group(1), "src": mi.group(2)})
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", st)
        if m:
            blocks.append({"t": "h", "lvl": len(m.group(1)), "text": m.group(2).strip()})
            i += 1
            continue
        if re.match(r"^(\*\*\*|---|___)$", st):
            blocks.append({"t": "hr"})
            i += 1
            continue

        if st.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            head = [c.strip() for c in st.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            blocks.append({"t": "table", "head": head, "rows": rows})
            continue

        if st.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            body = " ".join(x for x in buf if x).strip()
            label, kind = "", "note"
            m = re.match(r"^\*\*([^*]+?)\*\*\s*[—–\-:]\s*(.*)$", body, re.S)
            if not m:
                m = re.match(r"^\*\*([^*]+?)\*\*\s*(.*)$", body, re.S)
            if m:
                label, body = m.group(1).strip(), m.group(2).strip()
                key = re.sub(r"\s*\([^)]*\)\s*", "", label).upper().strip()
                kind = LABEL_KIND.get(key, "note")
                if label.endswith(":") and kind == "note":
                    kind = "dialog"
                elif kind == "note" and re.fullmatch(r"[A-Z][\w'’.\- ]{1,30}", label) and label.endswith(":"):
                    kind = "dialog"
            if body:
                blocks.append({"t": "quote", "kind": kind, "label": label, "text": body})
            continue

        if re.match(r"^([-*+]|\d+\.)\s+", st):
            ordered = bool(re.match(r"^\d+\.", st))
            items = []
            while i < len(lines) and re.match(r"^([-*+]|\d+\.)\s+", lines[i].strip()):
                item = re.sub(r"^([-*+]|\d+\.)\s+", "", lines[i].strip())
                i += 1
                while (i < len(lines) and lines[i].startswith("  ")
                       and not re.match(r"^([-*+]|\d+\.)\s+", lines[i].strip())):
                    item += " " + lines[i].strip()
                    i += 1
                items.append(item)
            blocks.append({"t": "ol" if ordered else "ul", "items": items})
            continue

        buf = [st]
        i += 1
        while (i < len(lines) and lines[i].strip()
               and not re.match(r"^(#{1,4}\s|>|\||```|!\[|([-*+]|\d+\.)\s)", lines[i].strip())):
            buf.append(lines[i].strip())
            i += 1
        blocks.append({"t": "p", "text": " ".join(buf)})
    return blocks


def merge_dialogue(blocks):
    """Consecutive speaker lines become one transcript panel."""
    out = []
    for b in blocks:
        if (b["t"] == "quote" and b["kind"] == "dialog" and out
                and out[-1]["t"] == "quote" and out[-1]["kind"] == "dialog"):
            prev = out[-1]
            prev.setdefault("lines", [(prev["label"], prev["text"])])
            prev["lines"].append((b["label"], b["text"]))
            continue
        out.append(b)
    return out


# ------------------------------------------------------------------ flowables


class Heading(Paragraph):
    """Paragraph that also feeds the contents and the PDF outline."""

    def __init__(self, text, style, toc_level=None, outline_level=0, key=None):
        Paragraph.__init__(self, text, style)
        self.toc_level = toc_level
        self.outline_level = outline_level
        self.key = key


def col_widths(rows, total):
    """Proportional widths, but never narrower than the longest word."""
    n = max(len(r) for r in rows)
    weights, mins = [], []
    for c in range(n):
        cells = [r[c] for r in rows if c < len(r)]
        lens = sorted(clean_len(x) for x in cells)
        p90 = lens[min(len(lens) - 1, int(len(lens) * 0.9))] if lens else 8
        weights.append(max(7, min(p90, 55)) ** 0.92)
        longest = 0.0
        for cell in cells:
            for word in re.sub(r"[*`]", "", cell).split():
                longest = max(longest, pdfmetrics.stringWidth(word, "Serif", 8.2))
        mins.append(longest + 13)
    s = sum(weights)
    widths = [total * w / s for w in weights]
    # lift any column below its floor, taking the room from the widest columns
    for _ in range(3):
        need = sum(max(0.0, mins[i] - widths[i]) for i in range(n))
        if need <= 0.5:
            break
        pool = [i for i in range(n) if widths[i] > mins[i] + 1]
        spare = sum(widths[i] - mins[i] for i in pool)
        if spare <= 0:
            break
        for i in pool:
            widths[i] -= need * (widths[i] - mins[i]) / spare
        for i in range(n):
            widths[i] = max(widths[i], mins[i])
    scale = total / sum(widths)
    return [w * scale for w in widths]


def table_flowable(block, S, avail):
    head, rows = block["head"], block["rows"]
    ncol = max([len(head)] + [len(r) for r in rows])
    head = head + [""] * (ncol - len(head))
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    data = [[Paragraph(inline(c), S["cellhead"]) for c in head]]
    data += [[Paragraph(inline(c), S["cell"]) for c in r] for r in rows]
    widths = col_widths([head] + rows, avail)
    t = Table(data, colWidths=widths, repeatRows=1, splitByRow=1, hAlign="LEFT")
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9F0EE")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, colors.HexColor("#A9BDB8")),
        ("GRID", (0, 1), (-1, -1), 0.4, RULE),
        ("LINEABOVE", (0, 1), (-1, 1), 0.4, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
    ]
    for r in range(1, len(data)):
        if r % 2 == 0:
            cmds.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#FAFCFB")))
    t.setStyle(TableStyle(cmds))
    return t


def callout(block, S, avail):
    bar, tint = KINDS.get(block["kind"], KINDS["note"])
    inner = []
    if block.get("lines"):
        parts = []
        for speaker, text in block["lines"]:
            parts.append(f'<b>{inline(speaker)}</b>&nbsp;&nbsp;{inline(text)}')
        inner.append(Paragraph("<br/>".join(parts), S["quote"]))
    else:
        if block["label"]:
            lab = block["label"]
            lab_style = ParagraphStyle(
                "lab", parent=S["quotelabel"], textColor=bar,
                fontName="Sans-Bold", fontSize=7.1, leading=9.4)
            inner.append(Paragraph(inline(lab.upper()), lab_style))
        inner.append(Paragraph(inline(block["text"]), S["quote"]))
    cell = inner
    t = Table([["", cell]], colWidths=[3.4, avail - 3.4], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), bar),
        ("BACKGROUND", (1, 0), (1, 0), tint),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 0), (0, 0), 0),
        ("BOTTOMPADDING", (0, 0), (0, 0), 0),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("RIGHTPADDING", (1, 0), (1, 0), 11),
        ("TOPPADDING", (1, 0), (1, 0), 7.5),
        ("BOTTOMPADDING", (1, 0), (1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return [Spacer(1, 3), t, Spacer(1, 9)]


def figure_flowable(block, md_dir, S, avail, frame_h):
    src = os.path.normpath(os.path.join(md_dir, block["src"]))
    p = Path(src)
    if not p.exists() or p.suffix.lower() != ".svg":
        return []
    png = ensure_png(p)
    from PIL import Image as PILImage
    with PILImage.open(png) as im:
        pw, ph = im.size
    aspect = ph / pw
    width = avail
    if width * aspect > frame_h * 0.58:
        width = (frame_h * 0.58) / aspect
    height = width * aspect
    cap = block.get("alt") or ""
    flow = [Spacer(1, 5), Image(str(png), width=width, height=height)]
    if cap:
        flow.append(Paragraph(inline(cap), S["caption"]))
    else:
        flow.append(Spacer(1, 12))
    return [KeepTogether(flow)]


# ------------------------------------------------------------------ document


class NumberedCanvas(pdfcanvas.Canvas):
    """Canvas that knows the total page count when it draws the last folio."""

    def __init__(self, *args, **kwargs):
        pdfcanvas.Canvas.__init__(self, *args, **kwargs)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved)
        for state in self._saved:
            self.__dict__.update(state)
            self._folio(total)
            pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)

    def _folio(self, total):
        n = self._pageNumber
        if n <= 2:  # cover and imprint carry no folio
            return
        W, H = A4
        self.saveState()
        self.setStrokeColor(RULE)
        self.setLineWidth(0.5)
        self.line(60, 46, W - 56, 46)
        self.setFont("Sans", 7.2)
        self.setFillColor(MUTED)
        self.drawString(60, 33, self.__dict__.get("_fol_left", ""))
        self.drawRightString(W - 56, 33, self.__dict__.get("_fol_right", ""))
        self.setFont("Sans-Bold", 8.2)
        self.setFillColor(GOLD)
        self.drawCentredString(W / 2, 32.4, f"{n} / {total}")
        self.restoreState()


class BookDoc(BaseDocTemplate):
    def __init__(self, filename, meta, **kw):
        self.meta = meta
        self._sec = 0
        self._outline = -1
        W, H = A4
        L, R, T, B = 60, 56, 70, 62
        BaseDocTemplate.__init__(
            self, str(filename), pagesize=A4,
            leftMargin=L, rightMargin=R, topMargin=T, bottomMargin=B,
            title=f"{meta['code']} — {meta['title']}",
            author="MSc Marriage and Family Therapy Lecture Library",
            subject=f"{meta['semester']} course book · {meta['units']} units",
            creator="build_pdfs.py (ReportLab)",
            **kw,
        )
        self.frame_w = W - L - R
        self.frame_h = H - T - B
        cover = Frame(0, 0, W, H, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="cover")
        front = Frame(L, 58, self.frame_w, H - 70 - 58, id="front")
        body = Frame(L, 62, self.frame_w, H - 78 - 62, id="body")
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[cover], onPage=self.draw_cover),
            PageTemplate(id="front", frames=[front], onPage=self.draw_front),
            PageTemplate(id="body", frames=[body], onPage=self.draw_body),
        ])

    # -- furniture ---------------------------------------------------------
    def draw_cover(self, canv, doc):
        m = self.meta
        W, H = A4
        canv.saveState()
        canv.setFillColor(colors.HexColor("#FBFAF7"))
        canv.rect(0, 0, W, H, fill=1, stroke=0)

        panel = 500
        canv.setFillColor(TEAL_DEEP)
        canv.rect(0, panel, W, H - panel, fill=1, stroke=0)
        canv.setFillColor(GOLD)
        canv.rect(0, panel, W, 3.0, fill=1, stroke=0)

        x = 60
        self._tracked(canv, x, 786, "MSC MARRIAGE AND FAMILY THERAPY", "Sans-Bold", 7.4, 2.1, GOLD_LIGHT)
        second = (f"LECTURE LIBRARY  ·  VOLUME {m['volume']} OF {m['total_volumes']}"
                  if m["volume"] else "PROGRAMME DOCUMENT  ·  LECTURE LIBRARY")
        self._tracked(canv, x, 768, second, "Sans", 6.9, 1.5, colors.HexColor("#9FB3AE"))
        canv.setStrokeColor(GOLD)
        canv.setLineWidth(0.9)
        canv.line(x, 750, x + 54, 750)

        canv.setFillColor(GOLD)
        if m["kind"] == "programme":
            self._tracked(canv, x, 706, m["code"], "Sans-Bold", 15, 2.4, GOLD)
            canv.setFillColor(colors.HexColor("#9FB3AE"))
            canv.setFont("Sans", 8.6)
            canv.drawString(x, 686, "Programme document")
        else:
            canv.setFont("Sans-Bold", 34)
            canv.drawString(x - 1, 706, m["code"].replace("MFT-", "MFT "))

        size, lead = (23.5, 30) if len(m["title"]) < 46 else (20.5, 26.5)
        y = 630 if m["kind"] == "programme" else 655
        for ln in self._wrap(m["title"], "Sans-Bold", size, W - 2 * x - 30)[:4]:
            canv.setFillColor(WHITE)
            canv.setFont("Sans-Bold", size)
            canv.drawString(x, y, ln)
            y -= lead

        if m["figures"] or m["practicals"] or m["cases"]:
            canv.setFillColor(colors.HexColor("#9FB3AE"))
            canv.setFont("Sans", 7.6)
            bits = [f"{m['practicals']} practicals", f"{m['cases']} worked cases",
                    f"{m['figures']} figures"]
            strip = f"{m['weeks']} teaching weeks" if m["kind"] == "course" else ""
            if strip:
                bits.insert(0, strip)
            canv.drawString(x, panel + 26, "   ·   ".join(bits))

        # lower half of the cover
        self._tracked(canv, x, 440, m["semester"].upper(), "Sans-Bold", 8.4, 1.9, TEAL)
        canv.setFillColor(MUTED)
        canv.setFont("Serif", 9.8)
        if m["kind"] == "programme":
            canv.drawString(x, 416, "For students and lecturers  ·  read before the semester")
        else:
            canv.drawString(x, 416, f"{m['units']} units  ·  {m['prereq']}")

        if m.get("epigraph"):
            lines = self._wrap(f"\u201c{m['epigraph']}\u201d", "Serif-Italic", 9.8, W - 2 * x - 24)[:4]
            canv.setFillColor(GOLD)
            canv.rect(x, 336 - (len(lines) - 1) * 14.6, 1.8, 18 + (len(lines) - 1) * 14.6, fill=1, stroke=0)
            canv.setFillColor(colors.HexColor("#3D4A51"))
            canv.setFont("Serif-Italic", 9.8)
            for i, ln in enumerate(lines):
                canv.drawString(x + 14, 344 - i * 14.6, ln)

        canv.setFont("Serif", 9.4)
        canv.setFillColor(BODY)
        if m["kind"] == "programme":
            for i, ln in enumerate([
                    "One of four programme documents that frame the 28-volume lecture library:",
                    "the student handbook, the lecturer's teaching and assessment guide, the",
                    "figure index and the visual figure gallery."]):
                canv.drawString(x, 240 - i * 14, ln)
        else:
            canv.drawString(x, 240, "One of 28 self-contained course books in the MSc Marriage and Family")
            canv.drawString(x, 226, "Therapy lecture library: a full taught semester per volume, with cases,")
            canv.drawString(x, 212, "practicals, assessment briefs, glossaries and model answers.")

        canv.setStrokeColor(RULE)
        canv.setLineWidth(0.6)
        canv.line(x, 120, W - 56, 120)
        canv.setFont("Sans", 7.2)
        canv.setFillColor(MUTED)
        canv.drawString(x, 104, "MSc Marriage and Family Therapy")
        canv.drawRightString(W - 56, 104, "CC BY 4.0  ·  2026 edition")
        canv.restoreState()

    @staticmethod
    def _tracked(canv, x, y, text, font, size, tracking, colour):
        canv.setFillColor(colour)
        canv.setFont(font, size)
        for ch in text:
            canv.drawString(x, y, ch)
            x += pdfmetrics.stringWidth(ch, font, size) + tracking

    @staticmethod
    def _wrap(text, font, size, maxw):
        out, cur = [], ""
        for word in text.split():
            trial = (cur + " " + word).strip()
            if pdfmetrics.stringWidth(trial, font, size) <= maxw or not cur:
                cur = trial
            else:
                out.append(cur)
                cur = word
        if cur:
            out.append(cur)
        return out

    def draw_front(self, canv, doc):
        if doc.page != 2:
            return
        W, H = A4
        m = self.meta
        canv.saveState()
        canv.setStrokeColor(RULE)
        canv.setLineWidth(0.5)
        canv.line(60, 100, W - 56, 100)
        canv.setFont("Sans", 6.9)
        canv.setFillColor(MUTED)
        canv.drawString(60, 86, "Set in DejaVu Serif and DejaVu Sans  ·  A4  ·  print-ready")
        canv.drawRightString(W - 56, 86, "28 volumes  ·  CC BY 4.0")
        canv.restoreState()

    def draw_body(self, canv, doc):
        m = self.meta
        W, H = A4
        canv.saveState()
        canv.setStrokeColor(RULE)
        canv.setLineWidth(0.5)
        canv.line(58, H - 52, W - 54, H - 52)
        canv.setFont("Sans", 7.1)
        canv.setFillColor(MUTED)
        canv.drawString(60, H - 45, f"{m['code']}  ·  {m['short']}")
        canv.drawRightString(W - 56, H - 45, "MSc Marriage and Family Therapy")
        canv.restoreState()
        canv._fol_left = "Lecture library  ·  CC BY 4.0"
        canv._fol_right = m["semester"]

    # -- indexing ----------------------------------------------------------
    def afterFlowable(self, flowable):
        if isinstance(flowable, Heading) and flowable.toc_level is not None:
            text = flowable.toc_text
            n = self.page
            key = f"sec{self._sec}"
            self._sec += 1
            self.canv.bookmarkPage(key)
            level = flowable.outline_level
            if level > self._outline + 1:  # never skip a level; readers reject the tree
                level = self._outline + 1
            try:
                self.canv.addOutlineEntry(text, key, level, 0)
            except ValueError:  # canvas outline was reset by a new build pass
                level = 0
                self.canv.addOutlineEntry(text, key, level, 0)
            self._outline = level
            self.notify("TOCEntry", (flowable.toc_level, text, n))


# ------------------------------------------------------------------ build


def read_meta(path: Path, volume: int, total: int):
    md = path.read_text(encoding="utf-8")
    m = re.search(r"^#\s+(.*)$", md, re.M)
    heading = re.sub(r"[*`]", "", m.group(1)).strip() if m else path.stem
    kind = "programme" if path.parent.name == "00-programme" else "course"
    if kind == "programme":
        num = re.match(r"(\d{2})-", path.name)
        code = f"PD {num.group(1)}" if num else "PD"
        title = re.sub(r"\s*[—–-]\s*MSc Marriage and Family Therapy$", "", heading).strip()
    else:
        mcode = re.match(r"(MFT-\d{3})", path.name)
        code = mcode.group(1) if mcode else path.stem.split("-")[0]
        title = re.sub(r"^MFT\s*\d{3}\s*[—–-]\s*", "", heading).strip()
    stand = ""
    sm = re.search(r"^>\s+\*\*MSc.*$", md, re.M)
    if sm:
        stand = sm.group(0).lstrip("> ").strip()
    units_m = re.search(r"([\d.]+)\s*Units?", stand, re.I)
    weeks_m = re.search(r"(\d+)\s+teaching weeks", stand, re.I)
    sem_m = re.search(r"(Semester \w+|Elective)", stand, re.I)
    folder = path.parent.name
    semester = {"01-semester-one": "Semester One", "02-semester-two": "Semester Two",
                "03-semester-three": "Semester Three", "04-electives": "Electives",
                "00-programme": "Programme"}.get(folder, sem_m.group(1) if sem_m else "")
    if sem_m and semester in ("Semester One", "Semester Two", "Semester Three"):
        semester = sem_m.group(1).title()
    summ = re.search(r"\*\*Course leader's summary\.\*\*\s*(.+?)(?:\n\s*\n|\Z)", md, re.S)
    if not summ:
        body = re.search(r"^#\s+.*?\n+(?:>.*?\n+)?(?:\*\*[^\n]*\*\*\s*)?(.{40,400}?)(?:\n\s*\n|\Z)",
                         md, re.S | re.M)
        if body:
            txt = re.sub(r"[*`]", "", re.sub(r"\s+", " ", body.group(1))).strip()
            first = re.split(r"(?<=[.?!])\s", txt)[0]
            if len(first) > 40:
                summ = type("S", (), {"group": lambda self, n: first})()
    epigraph = ""
    if summ:
        txt = re.sub(r"[*`]", "", re.sub(r"\s+", " ", summ.group(1))).strip()
        first = re.split(r"(?<=[.?!])\s", txt)[0]
        epigraph = first if len(first) <= 200 else first[:197].rsplit(" ", 1)[0] + "\u2026"
    prereq = "Prerequisite: none"
    pm = re.search(r"Prerequisite:\s*([^·|]+)", stand, re.I)
    if pm:
        prereq = "Prerequisite: " + pm.group(1).strip()
    meta = {
        "kind": kind,
        "code": code,
        "title": title,
        "heading": heading,
        "short": title if len(title) <= 62 else title[:59].rstrip() + "…",
        "semester": semester,
        "units": units_m.group(1) if units_m else "—",
        "weeks": weeks_m.group(1) if weeks_m else "14",
        "prereq": prereq,
        "stand": stand,
        "volume": volume,
        "total_volumes": total,
        "epigraph": epigraph,
        "practicals": len(re.findall(r"^>\s+\*\*(PRACTICAL|TASK|DRILL|REHEARSAL|ASSESSED)", md, re.M)),
        "cases": len(re.findall(r"^>\s+\*\*CASE", md, re.M)),
        "figures": len(re.findall(r"^!\[", md, re.M)),
        "path": path,
    }
    return md, meta


def series_page(meta, S, frame_w):
    """Front-matter page listing every volume in the library."""
    out = [Paragraph("The lecture library", S["imprintTitle"])]
    out.append(Spacer(1, 2))
    out.append(HRFlowable(width=90, thickness=2.4, color=GOLD, spaceBefore=0, spaceAfter=12, hAlign="LEFT"))
    out.append(Paragraph(
        "Twenty-eight self-contained course books carry the taught programme: eight in Semester One, "
        "seven in Semester Two, seven in Semester Three including the thesis, and six electives. "
        "The volume you are holding is marked in the margin.", S["small"]))
    out.append(Spacer(1, 8))
    data = [[Paragraph("Code", S["cellhead"]), Paragraph("Course", S["cellhead"]),
             Paragraph("Semester", S["cellhead"]), Paragraph("Units", S["cellhead"])]]
    cmds = []
    for i, (code, title, sem, units, _) in enumerate(LIBRARY, start=1):
        mine = code == meta["code"]
        style = ParagraphStyle("libcell", parent=S["cell"], fontSize=8.4, leading=11.4,
                               fontName="Sans-Bold" if mine else "Serif",
                               textColor=TEAL if mine else BODY)
        data.append([Paragraph(code.replace("MFT-", "MFT "), style),
                     Paragraph(inline(title), style),
                     Paragraph(sem.replace("Semester ", ""), S["cell"]),
                     Paragraph(units, S["cell"])])
        if mine:
            cmds.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#EDF5F4")))
            cmds.append(("LINEBEFORE", (0, i), (0, i), 2.2, TEAL))
    t = Table(data, colWidths=[frame_w * 0.14, frame_w * 0.63, frame_w * 0.13, frame_w * 0.10],
              repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9F0EE")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, colors.HexColor("#A9BDB8")),
        ("LINEBELOW", (0, 1), (-1, -1), 0.35, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
    ] + cmds))
    out.append(t)
    return out


def story_for(md, meta, S, frame_w, frame_h):
    blocks = parse_blocks(md)
    # drop the H1 (it becomes the cover) and the standfirst blockquote (imprint)
    if blocks and blocks[0]["t"] == "h" and blocks[0]["lvl"] == 1:
        blocks = blocks[1:]
    if blocks and blocks[0]["t"] == "quote" and (
            blocks[0].get("label", "").startswith("MSc")
            or "Units" in blocks[0].get("text", "")):
        blocks = blocks[1:]
    blocks = merge_dialogue(blocks)

    story = []
    # cover
    story += [Spacer(1, 2), NextPageTemplate("front"), PageBreak()]
    # imprint + library list
    story += imprint_page(meta, S)
    if LIBRARY:
        story += [PageBreak()]
        story += series_page(meta, S, frame_w)
    story += [PageBreak()]
    # contents
    story.append(Paragraph("Contents", S["tocTitle"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceBefore=2, spaceAfter=14))
    toc = TableOfContents()
    toc.levelStyles = [S["toc0"], S["toc1"]]
    toc.dotsMinLevel = 0
    story.append(toc)
    story += [NextPageTemplate("body"), PageBreak()]

    first_h2 = True
    prev_t = None
    for b in blocks:
        was_rule = prev_t == "hr"
        prev_t = b["t"]
        t = b["t"]
        if t == "h":
            lvl = b["lvl"]
            if lvl == 1:
                continue
            txt = b["text"]
            plain = re.sub(r"[*`]", "", txt)
            if lvl == 2:
                if not first_h2 and not was_rule:
                    story.append(HRFlowable(width="100%", thickness=0.6, color=RULE,
                                            spaceBefore=20, spaceAfter=6))
                first_h2 = False
                h = Heading(inline(txt), S["h2"], toc_level=0)
                h.toc_text = plain
                story.append(h)
            elif lvl == 3:
                h = Heading(inline(txt), S["h3"], toc_level=1, outline_level=1)
                h.toc_text = plain
                story.append(h)
            else:
                story.append(Paragraph(inline(txt), S["h4"]))
        elif t == "p":
            story.append(Paragraph(inline(b["text"]), S["body"]))
        elif t in ("ul", "ol"):
            for idx, item in enumerate(b["items"], 1):
                check = re.match(r"^\[( |x|X)\]\s+(.*)$", item)
                if check:
                    box = "☒" if check.group(1).lower() == "x" else "☐"
                    story.append(Paragraph(inline(check.group(2)), S["bullet"], bulletText=box))
                else:
                    bullet = "•" if t == "ul" else f"{idx}."
                    story.append(Paragraph(inline(item), S["bullet"], bulletText=bullet))
            story.append(Spacer(1, 5))
        elif t == "table":
            story.append(Spacer(1, 2))
            story.append(table_flowable(b, S, frame_w))
            story.append(Spacer(1, 12))
        elif t == "quote":
            story += callout(b, S, frame_w)
        elif t == "img":
            story += figure_flowable(b, str(meta["path"].parent), S, frame_w, frame_h)
        elif t == "hr":
            story.append(HRFlowable(width="100%", thickness=0.5, color=RULE,
                                    spaceBefore=12, spaceAfter=12))
        elif t == "code":
            story.append(Preformatted(b["text"], S["code"]))
    return story


def imprint_page(meta, S):
    out = [Spacer(1, 34)]
    out.append(Paragraph(meta["heading"], S["imprintTitle"]))
    out.append(Spacer(1, 2))
    out.append(HRFlowable(width=90, thickness=2.4, color=GOLD, spaceBefore=0, spaceAfter=14, hAlign="LEFT"))
    out.append(Paragraph(inline(meta["stand"]) if meta["stand"] else "", S["small"]))
    out.append(Spacer(1, 10))
    out.append(Paragraph(
        "This volume is one of 28 course books that together cover the whole MSc Marriage and Family "
        "Therapy taught programme. Each book is written to carry a 14&ndash;16 week semester on its own: "
        "every week pairs a core idea with the practice that follows from it, a worked case, and a "
        "reflective task, and each book closes with an integration chapter, a glossary and a "
        "self-assessment paper with model answers.", S["imprint"]))
    out.append(Paragraph(
        "The books are designed to be read straight through before the semester begins, revisited week "
        "by week, and used again in revision. Cross-references point to the other volumes where a topic "
        "is treated in more depth.", S["imprint"]))
    out.append(Spacer(1, 8))
    cite = (f"Lecture Library contributors (2026). <i>{meta['code'].replace('MFT-', 'MFT ')} — "
            f"{inline(meta['title'])}</i>. MSc Marriage and Family Therapy lecture library. CC BY 4.0.")
    out.append(Paragraph("How to cite this volume", ParagraphStyle(
        "citeHead", fontName="Sans-Bold", fontSize=7.4, leading=10, textColor=TEAL, spaceAfter=4)))
    out.append(Paragraph(cite, S["small"]))
    out.append(Spacer(1, 6))
    out.append(Paragraph("Licence", ParagraphStyle(
        "licHead", fontName="Sans-Bold", fontSize=7.4, leading=10, textColor=TEAL, spaceAfter=4)))
    out.append(Paragraph(
        "Creative Commons Attribution 4.0 International (CC BY 4.0). Share and adapt freely, including "
        "commercially, with attribution. Every figure in this volume was generated by the scripts in "
        "<font name='Mono' size='7.6'>scripts/</font>; there are no third-party images.", S["small"]))
    out.append(Spacer(1, 6))
    out.append(Paragraph("A note on the case material", ParagraphStyle(
        "caseHead", fontName="Sans-Bold", fontSize=7.4, leading=10, textColor=TEAL, spaceAfter=4)))
    out.append(Paragraph(
        "All families, couples and individuals in this book are fictional composites. They are written "
        "to teach pattern recognition, not to describe any real person. Nothing here replaces supervised "
        "clinical practice, professional registration, legal advice or medical care; legal content is "
        "orientation only and must be checked against the law of the relevant jurisdiction.", S["small"]))
    return out


def build_book(path: Path, S, volume: int, total: int, out_dir: Path):
    md, meta = read_meta(path, volume, total)
    doc_path = out_dir / f"{path.stem}.pdf"
    doc = BookDoc(doc_path, meta)
    story = story_for(md, meta, S, doc.frame_w, doc.frame_h)
    doc.multiBuild(story, maxPasses=4)
    return doc_path, doc.page


# ------------------------------------------------------------------ merged volume


def library_front_matter(S, frame_w):
    """Cover-style title page for the single-file edition of the whole library."""
    out = [Spacer(1, 76)]
    out.append(Paragraph("MSc Marriage and Family Therapy", ParagraphStyle(
        "libKicker", fontName="Sans-Bold", fontSize=9.6, leading=13, textColor=GOLD, spaceAfter=10)))
    out.append(Paragraph("The Lecture Library", ParagraphStyle(
        "libTitle", fontName="Serif-Bold", fontSize=30, leading=36, textColor=TEAL, spaceAfter=6)))
    out.append(Paragraph("Twenty-eight course books in one file", ParagraphStyle(
        "libSub", fontName="Serif", fontSize=13, leading=18, textColor=MUTED, spaceAfter=16)))
    out.append(HRFlowable(width=110, thickness=2.6, color=GOLD, spaceAfter=18, hAlign="LEFT"))
    out.append(Paragraph(
        "This single file contains every volume of the library, in programme order: eight courses in "
        "Semester One, seven in Semester Two, seven in Semester Three including the thesis, and six "
        "electives. Each course keeps its own cover, imprint, contents, running heads and folio, so the "
        "file can be printed whole or the individual volumes printed from the separate PDFs in "
        "<font name='Mono' size='8'>pdf/</font>.", S["imprint"]))
    out.append(Paragraph(
        "Use the bookmark panel of your PDF reader to jump to any course or to any chapter within a "
        "course. Every volume is also available as a standalone file, and the same text is published "
        "as a browsable site in <font name='Mono' size='8'>site/</font>.", S["imprint"]))
    out.append(PageBreak())
    out.append(Paragraph("Courses in this library", ParagraphStyle(
        "libTableTitle", fontName="Sans-Bold", fontSize=14, leading=18, textColor=TEAL, spaceAfter=2)))
    out.append(HRFlowable(width=74, thickness=2, color=GOLD, spaceBefore=2, spaceAfter=10, hAlign="LEFT"))
    rows = []
    for code, title, sem, units, _ in LIBRARY:
        rows.append((code.replace("MFT-", "MFT "), title, sem.replace("Semester ", ""), units))
    data = [[Paragraph(h, S["cellhead"]) for h in ("Code", "Course", "Semester", "Units")]]
    data += [[Paragraph(c, S["cell"]), Paragraph(inline(t), S["cell"]),
              Paragraph(s2, S["cell"]), Paragraph(u, S["cell"])] for c, t, s2, u in rows]
    t = Table(data, colWidths=[frame_w * 0.14, frame_w * 0.63, frame_w * 0.13, frame_w * 0.10],
              repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9F0EE")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, colors.HexColor("#A9BDB8")),
        ("LINEBELOW", (0, 1), (-1, -1), 0.35, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.6),
    ]))
    out.append(t)
    out.append(Spacer(1, 12))
    out.append(Paragraph(
        "Contents of each volume: how to use the book; course description and rationale; learning "
        "outcomes; assessment; the fourteen-week plan; fourteen teaching weeks; an integration "
        "chapter; a glossary; a self-assessment paper with model answers; and further reading.",
        S["small"]))
    return out


def build_complete(S, out_dir: Path):
    """Concatenate every course PDF behind a title page, keeping the bookmarks."""
    from pypdf import PdfReader, PdfWriter

    front = out_dir / ".front.pdf"

    class FrontDoc(BaseDocTemplate):
        def __init__(self, filename, **kw):
            W, H = A4
            BaseDocTemplate.__init__(self, str(filename), pagesize=A4, leftMargin=60, rightMargin=56,
                                     topMargin=70, bottomMargin=62,
                                     title="MSc Marriage and Family Therapy — Lecture Library",
                                     author="MSc Marriage and Family Therapy Lecture Library",
                                     subject="Complete 28-volume lecture library", **kw)
            self.frame_w = W - 60 - 56
            self.addPageTemplates([PageTemplate(id="front",
                                                frames=[Frame(60, 62, self.frame_w, H - 132)])])

    doc = FrontDoc(front)
    doc.build(library_front_matter(S, doc.frame_w))
    writer = PdfWriter()
    writer.append(str(front))
    page_offset = len(PdfReader(str(front)).pages)
    for code, title, sem, units, stem in LIBRARY:
        path = out_dir / f"{stem}.pdf"
        if not path.exists():
            continue
        reader = PdfReader(str(path))
        # outline_item wraps every imported bookmark under the course entry
        writer.append(str(path), outline_item=f"{code.replace('MFT-', 'MFT ')} — {title}")
        page_offset += len(reader.pages)
    target = out_dir / "MFT-Library-Complete-28-volumes.pdf"
    with open(target, "wb") as fh:
        writer.write(fh)
    front.unlink(missing_ok=True)
    return target, page_offset


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the A4 PDF edition")
    ap.add_argument("--only", help="build one course, e.g. MFT-701")
    ap.add_argument("--programme", action="store_true", help="also build the programme documents")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--complete", action="store_true",
                    help="also merge every volume into one bookmarked PDF")
    args = ap.parse_args(argv)

    register_fonts()
    S = styles()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    books = []
    for folder, label in SECTIONS:
        if folder == "00-programme" and not args.programme:
            continue
        d = ROOT / folder
        if not d.is_dir():
            continue
        books += sorted(d.glob("*.md"))

    total = len([b for b in books if b.parent.name != "00-programme"])

    if args.only:
        books = [b for b in books if args.only.lower() in b.name.lower()]

    for b in books:
        if b.parent.name == "00-programme":
            continue
        _, m = read_meta(b, 0, 0)
        LIBRARY.append((m["code"], m["title"], m["semester"], m["units"], b.stem))
    LIBRARY.sort(key=lambda r: r[0])

    print(f"building {len(books)} PDF(s)")
    for idx, path in enumerate(books, 1):
        vol = idx if path.parent.name != "00-programme" else 0
        out, pages = build_book(path, S, vol, total, out_dir)
        size = out.stat().st_size / 1024
        print(f"  {out.name:62s} {pages:3d} pages  {size:6.0f} KB")
    if args.complete:
        target, pages = build_complete(S, out_dir)
        print(f"merged  {target.name}  {pages} pages  {target.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"done → {out_dir}")


if __name__ == "__main__":
    main()
