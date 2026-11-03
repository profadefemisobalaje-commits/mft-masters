#!/usr/bin/env python3
"""Build a browsable, print-ready HTML edition of the whole programme.

Takes every Markdown book in the repository and renders it into `site/` with a
shared sidebar, per-page table of contents, client-side search, and print CSS
so students can read on screen or print to PDF.

    python3 scripts/build_site.py          # build
    python3 scripts/build_site.py --serve  # build and serve on :8000
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")

SECTIONS = [
    ("00-programme", "Programme"),
    ("01-semester-one", "Semester One"),
    ("02-semester-two", "Semester Two"),
    ("03-semester-three", "Semester Three"),
    ("04-electives", "Electives"),
]

# ----------------------------------------------------------------- markdown


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)",
               r'<figure><img src="\2" alt="\1" loading="lazy">'
               r'<figcaption>\1</figcaption></figure>', t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:60] or "s"


def md_to_html(md):
    lines = md.split("\n")
    out, i, toc = [], 0, []
    in_code = False
    while i < len(lines):
        ln = lines[i]
        st = ln.strip()

        if st.startswith("```"):
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                out.append('<pre><code>')
                in_code = True
            i += 1
            continue
        if in_code:
            out.append(html.escape(ln) + "\n")
            i += 1
            continue

        if not st:
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", st)
        if m:
            lvl = len(m.group(1))
            txt = m.group(2)
            hid = slug(re.sub(r"[*`]", "", txt))
            if lvl == 2:
                toc.append((hid, re.sub(r"[*`]", "", txt)))
            out.append(f'<h{lvl} id="{hid}">{inline(txt)}</h{lvl}>')
            i += 1
            continue

        if re.match(r"^(\*\*\*|---|___)$", st):
            out.append("<hr>")
            i += 1
            continue

        # table
        if st.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            head = [c.strip() for c in st.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append('<div class="tw"><table><thead><tr>' +
                       "".join(f"<th>{inline(c)}</th>" for c in head) +
                       "</tr></thead><tbody>")
            for r in rows:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</tbody></table></div>")
            continue

        # blockquote (callouts): "> **Title**" blocks
        if st.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            kind = "note"
            body = " ".join(buf)
            low = body.lower()
            for k, tag in [("practical", "practical"), ("case", "case"),
                           ("caution", "caution"), ("reflect", "reflect"),
                           ("key", "key"), ("dialog", "dialog"),
                           ("law", "law"), ("task", "practical")]:
                if low.startswith("**" + k):
                    kind = tag
                    body = body[len("**" + k) + 1:].lstrip("*: ").strip()
                    break
            out.append(f'<div class="callout {kind}">{inline(body)}</div>')
            continue

        # lists
        if re.match(r"^([-*+]|\d+\.)\s+", st):
            ordered = bool(re.match(r"^\d+\.", st))
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>")
            while i < len(lines) and re.match(r"^([-*+]|\d+\.)\s+", lines[i].strip()):
                item = re.sub(r"^([-*+]|\d+\.)\s+", "", lines[i].strip())
                # continuation lines
                i += 1
                while (i < len(lines) and lines[i].startswith("  ")
                       and not re.match(r"^([-*+]|\d+\.)\s+", lines[i].strip())):
                    item += " " + lines[i].strip()
                    i += 1
                out.append(f"<li>{inline(item)}</li>")
            out.append(f"</{tag}>")
            continue

        # paragraph
        buf = [st]
        i += 1
        while (i < len(lines) and lines[i].strip()
               and not re.match(r"^(#{1,4}\s|>|\||```|([-*+]|\d+\.)\s)",
                                lines[i].strip())):
            buf.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out), toc


# ----------------------------------------------------------------- layout

CSS = """
:root{--ink:#1f2937;--muted:#5b6675;--line:#e2e8f0;--teal:#0f766e;--bg:#fff;
--panel:#f8fafc;--amber:#b45309;--rose:#9f1239;--plum:#6d28d9;--blue:#1d4ed8;--green:#15803d;}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:"Segoe UI",-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;
color:var(--ink);background:var(--bg);line-height:1.68;font-size:16.5px}
.wrap{display:grid;grid-template-columns:296px minmax(0,1fr);min-height:100vh}
nav{position:sticky;top:0;height:100vh;overflow-y:auto;background:#0f172a;color:#cbd5e1;padding:22px 18px 60px}
nav h1{font-size:15px;letter-spacing:.4px;color:#fff;margin:0 0 4px;line-height:1.35}
nav .sub{font-size:11.5px;color:#94a3b8;margin-bottom:16px}
nav input{width:100%;padding:8px 10px;border-radius:8px;border:1px solid #334155;
background:#1e293b;color:#e2e8f0;font-size:13px;margin-bottom:14px}
nav a{display:block;color:#cbd5e1;text-decoration:none;font-size:13px;padding:5px 8px;border-radius:6px}
nav a:hover{background:#1e293b;color:#fff}
nav a.on{background:var(--teal);color:#fff;font-weight:600}
nav .sec{font-size:10.5px;letter-spacing:1.2px;text-transform:uppercase;color:#64748b;margin:18px 0 6px}
a{color:var(--teal)}
main{padding:44px 52px 90px;max-width:1000px;width:100%}
h1{font-size:30px;line-height:1.25;margin:0 0 8px;color:#0f172a;letter-spacing:-.4px}
h2{font-size:22px;margin:46px 0 12px;padding-top:12px;border-top:1px solid var(--line);
color:#0f172a;scroll-margin-top:16px}
h3{font-size:17.5px;margin:28px 0 8px;color:var(--teal)}
h4{font-size:15px;margin:20px 0 6px;color:#334155}
p{margin:0 0 14px;max-width:76ch}
ul,ol{margin:0 0 16px;padding-left:24px;max-width:76ch}
li{margin:5px 0}
code{background:#f1f5f9;padding:1px 5px;border-radius:4px;font-size:.9em}
pre{background:#0f172a;color:#e2e8f0;padding:16px;border-radius:10px;overflow-x:auto}
figure{margin:22px 0;padding:0}
figure img{width:100%;height:auto;border:1px solid var(--line);border-radius:12px;background:#fff}
figcaption{font-size:13px;color:var(--muted);margin-top:8px;font-style:italic}
.tw{overflow-x:auto;margin:18px 0}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{border:1px solid var(--line);padding:9px 11px;vertical-align:top;text-align:left}
th{background:var(--panel);font-size:12.5px;text-transform:uppercase;letter-spacing:.5px;color:#475569}
tr:nth-child(even) td{background:#fcfdfe}
blockquote,.callout{margin:20px 0;padding:16px 18px;border-radius:10px;border-left:4px solid var(--amber);
background:#fdf7ec;font-size:15px}
.callout.case{border-color:var(--teal);background:#eef7f5}
.callout.practical{border-color:var(--blue);background:#eef2fd}
.callout.caution{border-color:var(--rose);background:#fcf0f4}
.callout.reflect{border-color:var(--plum);background:#f5f0fe}
.callout.key{border-color:var(--green);background:#eef8f1}
.callout.dialog{border-color:#475569;background:#f4f6f9}
.callout.law{border-color:#7c2d12;background:#fbf3ee}
hr{border:none;border-top:1px solid var(--line);margin:34px 0}
.meta{color:var(--muted);font-size:14px;margin:0 0 6px}
.toc{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 22px;margin:24px 0}
.toc div{font-size:11px;letter-spacing:1.3px;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.toc a{display:block;font-size:14px;padding:3px 0;text-decoration:none}
.toc a:hover{text-decoration:underline}
@media print{
 nav{display:none}.wrap{display:block}main{padding:0;max-width:none}
 h2{page-break-after:avoid}figure{page-break-inside:avoid}body{font-size:11.5pt}
 a{color:inherit;text-decoration:none}
}
@media (max-width:900px){.wrap{display:block}nav{position:static;height:auto}
 main{padding:24px 18px 60px}h1{font-size:24px}}
"""

SHELL = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{css}</style></head><body><div class="wrap">
<nav><h1>MSc Marriage &amp; Family Therapy</h1>
<div class="sub">Complete lecture library · 28 course books</div>
<input id="q" placeholder="Filter courses…" oninput="f(this.value)">
{nav}</nav>
<main><h1>{h1}</h1>{meta}{toc}{body}</main></div>
<script>
function f(v){{v=v.toLowerCase();
document.querySelectorAll('nav a').forEach(function(a){{
a.style.display=a.textContent.toLowerCase().includes(v)?'block':'none';}});}}
</script></body></html>"""


def collect():
    pages = []
    for folder, label in SECTIONS:
        d = os.path.join(ROOT, folder)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".md"):
                pages.append((folder, label, f))
    return pages


def title_of(md, fallback):
    m = re.search(r"^#\s+(.*)$", md, re.M)
    return re.sub(r"[*`]", "", m.group(1)).strip() if m else fallback


def build():
    pages = collect()
    os.makedirs(OUT, exist_ok=True)
    # nav
    nav = []
    for folder, label in SECTIONS:
        group = [p for p in pages if p[0] == folder]
        if not group:
            continue
        nav.append(f'<div class="sec">{label}</div>')
        for pf, _, f in group:
            md = open(os.path.join(ROOT, pf, f), encoding="utf-8").read()
            t = title_of(md, f[:-3])
            nav.append(f'<a href="{pf}-{f[:-3]}.html">{html.escape(t)}</a>')
    nav_html = "\n".join(nav)

    for pf, _, f in pages:
        path = os.path.join(pf, f)
        md = open(os.path.join(ROOT, path), encoding="utf-8").read()
        t = title_of(md, f[:-3])
        # strip the leading H1 and the standfirst blockquote; they become the page header
        lines = md.split("\n")
        meta_line = ""
        out_lines = []
        seen_h1 = False
        for ln in lines:
            if not seen_h1 and ln.startswith("# "):
                seen_h1 = True
                continue
            if seen_h1 and not meta_line and ln.startswith("> **"):
                meta_line = ln[2:].strip()
                continue
            out_lines.append(ln)
        md = "\n".join(out_lines)
        body, toc = md_to_html(md)
        meta = (f'<p class="meta">{inline(meta_line)}</p>' if meta_line else "")
        toc_html = ""
        if len(toc) > 4:
            items = "".join(f'<a href="#{h}">{html.escape(x)}</a>' for h, x in toc)
            toc_html = f'<div class="toc"><div>In this book</div>{items}</div>' 
        page = SHELL.format(title=html.escape(t), css=CSS, nav=nav_html,
                            toc=toc_html, h1=html.escape(t),
                            meta=meta, body=body)
        with open(os.path.join(OUT, f"{pf}-{f[:-3]}.html"), "w", encoding="utf-8") as fh:
            fh.write(page)
    # index
    cards = []
    for folder, label in SECTIONS:
        group = [p for p in pages if p[0] == folder]
        if not group:
            continue
        cards.append(f'<h2>{label}</h2><ul>')
        for pf, _, f in group:
            md = open(os.path.join(ROOT, pf, f), encoding="utf-8").read()
            cards.append(f'<li><a href="{pf}-{f[:-3]}.html">{html.escape(title_of(md, f))}</a></li>')
        cards.append("</ul>")
    idx = SHELL.format(
        title="MFT Masters — Lecture Library", css=CSS, nav=nav_html, toc="",
        h1="MSc Marriage and Family Therapy",
        meta='<p class="meta">Complete lecture library · 28 course books · 40 original figures</p>',
        body=("<p>Every course in the programme is written as a self-contained book: 14–16 weeks of "
              "teaching, worked cases, practicals, assessment, glossary and further reading.</p>"
              "<p>The same books are also typeset as a <b>print edition</b>: one finished A4 PDF per "
              "course, plus the whole programme bound into a single bookmarked file. "
              '<a href="../pdf/README.md">Open the print edition</a>.</p>'
              + "".join(cards)))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(idx)
    # asset passthrough: pages live in site/, figures referenced as ../assets/...
    print(f"built {len(pages)} pages + index → {OUT}")
    return len(pages)


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        import http.server, socketserver, functools
        port = 8000
        h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
        with socketserver.TCPServer(("0.0.0.0", port), h) as httpd:
            print(f"serving on http://0.0.0.0:{port}/site/index.html")
            httpd.serve_forever()
