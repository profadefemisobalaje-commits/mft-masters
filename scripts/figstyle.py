"""Tiny SVG drawing toolkit used to generate the figure library.

Every figure in this repository is generated deterministically by these
scripts, so the artwork is original, licence-clean, resolution-independent,
and easy to revise (change the text, re-run, the figure updates).

Text is measured against a metric table (DejaVu Sans, the fallback that most
renderers use) so line wrapping and label fitting behave predictably.

Run:  python3 scripts/build_figures.py
"""

INK = "#1f2937"
MUTED = "#5b6675"
LINE = "#c7d0da"
PANEL = "#f8fafc"
WHITE = "#ffffff"
TEAL = "#0f766e"
TEAL_L = "#e6f4f1"
AMBER = "#b45309"
AMBER_L = "#fdf3e3"
ROSE = "#9f1239"
ROSE_L = "#fce8ee"
PLUM = "#6d28d9"
PLUM_L = "#f1ebfd"
BLUE = "#1d4ed8"
BLUE_L = "#e8eefc"
GREEN = "#15803d"
GREEN_L = "#e8f5ec"
SLATE = "#334155"
SLATE_L = "#eef2f7"

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

# width of ASCII 32..126 in em units (DejaVu Sans)
_W_REG = [0.32, 0.40, 0.46, 0.84, 0.64, 0.95, 0.78, 0.28, 0.39, 0.39, 0.50, 0.84,
          0.32, 0.36, 0.32, 0.34, 0.64, 0.64, 0.64, 0.64, 0.64, 0.64, 0.64, 0.64,
          0.64, 0.64, 0.34, 0.34, 0.84, 0.84, 0.84, 0.53, 1.00, 0.68, 0.69, 0.70,
          0.77, 0.63, 0.58, 0.78, 0.75, 0.30, 0.30, 0.66, 0.56, 0.86, 0.75, 0.79,
          0.60, 0.79, 0.70, 0.64, 0.61, 0.73, 0.68, 0.99, 0.68, 0.61, 0.68, 0.39,
          0.34, 0.39, 0.84, 0.50, 0.50, 0.61, 0.64, 0.55, 0.64, 0.62, 0.35, 0.64,
          0.63, 0.28, 0.28, 0.58, 0.28, 0.97, 0.63, 0.61, 0.64, 0.64, 0.41, 0.52,
          0.39, 0.63, 0.59, 0.82, 0.59, 0.59, 0.52, 0.64, 0.34, 0.64, 0.84]
_W_BOLD = [0.35, 0.46, 0.52, 0.84, 0.70, 1.00, 0.87, 0.31, 0.46, 0.46, 0.52, 0.84,
           0.38, 0.42, 0.38, 0.36, 0.70, 0.70, 0.70, 0.70, 0.70, 0.70, 0.70, 0.70,
           0.70, 0.70, 0.40, 0.40, 0.84, 0.84, 0.84, 0.58, 1.00, 0.77, 0.76, 0.73,
           0.83, 0.68, 0.68, 0.82, 0.84, 0.37, 0.37, 0.78, 0.64, 1.00, 0.84, 0.85,
           0.73, 0.85, 0.77, 0.72, 0.68, 0.81, 0.77, 1.10, 0.77, 0.72, 0.72, 0.46,
           0.36, 0.46, 0.84, 0.50, 0.50, 0.68, 0.72, 0.59, 0.72, 0.68, 0.44, 0.72,
           0.71, 0.34, 0.34, 0.66, 0.34, 1.04, 0.71, 0.69, 0.72, 0.72, 0.49, 0.60,
           0.48, 0.71, 0.65, 0.92, 0.64, 0.65, 0.58, 0.71, 0.36, 0.71, 0.84]

# characters outside ASCII that we use often
_EXTRA = {"—": 1.00, "–": 0.50, "‘": 0.32, "’": 0.32, "“": 0.50, "”": 0.50,
          "→": 0.84, "•": 0.35, "…": 1.00, "°": 0.50, "×": 0.84, "↑": 0.84,
          "↓": 0.84, "≈": 0.84, "±": 0.84, "½": 0.84, "·": 0.32, "&": 0.78}


def tw(s, size, weight="400"):
    """Estimated rendered width in pixels."""
    bold = weight in ("700", "600") or (isinstance(weight, str) and weight.isdigit()
                                        and int(weight) >= 600)
    table = _W_BOLD if bold else _W_REG
    total = 0.0
    for ch in s:
        o = ord(ch)
        if 32 <= o <= 126:
            total += table[o - 32]
        elif ch in _EXTRA:
            total += _EXTRA[ch]
        else:
            total += 0.62
    return total * size


def split_lines(s, maxpx, size, weight="400"):
    """Greedy word wrap driven by measured width."""
    words, lines, cur = s.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if tw(trial, size, weight) <= maxpx or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


class SVG:
    def __init__(self, w=980, h=640, title="", subtitle="", bg=WHITE):
        self.w, self.h = w, h
        self.parts = []
        self.defs = []
        self.labels = []  # (x0, y0, x1, y1, s) for the layout linter
        self.parts.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="{bg}"/>')
        for name, color in [("ar-ink", INK), ("ar-teal", TEAL), ("ar-rose", ROSE),
                            ("ar-amber", AMBER), ("ar-plum", PLUM), ("ar-blue", BLUE),
                            ("ar-green", GREEN), ("ar-muted", MUTED)]:
            self.defs.append(
                f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
                f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>'
            )
        if title:
            self.title(title, subtitle)

    # ------------------------------------------------------------------ text
    def text(self, x, y, s, size=15, weight="400", fill=INK, anchor="middle",
             italic=False, family=FONT, opacity=1.0, spacing=None, maxpx=None,
             min_size=8.0):
        """Draw text. If maxpx is given, shrink the size until it fits."""
        s = str(s)
        if maxpx:
            while size > min_size and tw(s, size, weight) > maxpx:
                size -= 0.25
        esc = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        style = f'font-family:{family};font-size:{size:g}px;font-weight:{weight};'
        if italic:
            style += 'font-style:italic;'
        if spacing:
            style += f'letter-spacing:{spacing}px;'
        if opacity != 1.0:
            style += f'opacity:{opacity};'
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" text-anchor="{anchor}" '
            f'style="{style}">{esc}</text>'
        )
        wpx_ = tw(s, size, weight)
        x0 = x - (wpx_ if anchor == "end" else wpx_ / 2 if anchor == "middle" else 0)
        self.labels.append((x0, y - size * 0.78, x0 + wpx_, y + size * 0.24, s, size))
        return size

    def wrap(self, x, y, s, width=30, size=14, leading=None, weight="400",
             fill=INK, anchor="middle", max_lines=None, italic=False, wpx=None):
        """Wrap text. `width` is a legacy character budget; `wpx` is exact pixels."""
        leading = leading or size * 1.35
        maxpx = wpx if wpx else width * size * 0.55
        lines = split_lines(s, maxpx, size, weight)
        if max_lines:
            lines = lines[:max_lines]
        for i, ln in enumerate(lines):
            self.text(x, y + i * leading, ln, size=size, weight=weight,
                      fill=fill, anchor=anchor, italic=italic)
        return y + len(lines) * leading

    # ------------------------------------------------------------------ title
    def title(self, s, subtitle="", y=48, x=None):
        x = self.w / 2 if x is None else x
        self.text(x, y, s, size=26, weight="700", fill=SLATE, maxpx=self.w - 80)
        if subtitle:
            self.text(x, y + 26, subtitle, size=14.5, fill=MUTED, maxpx=self.w - 100)

    # ------------------------------------------------------------------ shapes
    def rect(self, x, y, w, h, fill=WHITE, stroke=LINE, rx=12, sw=1.5,
             dash=None, opacity=1.0):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} opacity="{opacity}"/>')

    def circle(self, cx, cy, r, fill=WHITE, stroke=LINE, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def ellipse(self, cx, cy, rx, ry, fill=WHITE, stroke=LINE, sw=1.5,
                dash=None, opacity=1.0):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx}" ry="{ry}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d} opacity="{opacity}"/>')

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=1.6, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def path(self, d, stroke=LINE, fill="none", sw=1.6, dash=None, marker=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        ma = f' marker-end="url(#{marker})"' if marker else ""
        self.parts.append(
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da}{ma}/>')

    def arrow(self, x1, y1, x2, y2, color=TEAL, sw=2.0, dash=None,
              label=None, lsize=12.5, loff=(0, -8)):
        import math
        self.line(x1, y1, x2, y2, stroke=color, sw=sw, dash=dash)
        ang = math.atan2(y2 - y1, x2 - x1)
        L, W = 10, 5
        p1 = (x2 - L * math.cos(ang) + W * math.sin(ang),
              y2 - L * math.sin(ang) - W * math.cos(ang))
        p2 = (x2 - L * math.cos(ang) - W * math.sin(ang),
              y2 - L * math.sin(ang) + W * math.cos(ang))
        self.parts.append(
            f'<path d="M {p1[0]:.1f} {p1[1]:.1f} L {x2:.1f} {y2:.1f} '
            f'L {p2[0]:.1f} {p2[1]:.1f} z" fill="{color}"/>')
        if label:
            self.text((x1 + x2) / 2 + loff[0], (y1 + y2) / 2 + loff[1],
                      label, size=lsize, fill=color, weight="600")

    def card(self, x, y, w, h, title, body=(), fill=WHITE, stroke=LINE,
             tcolor=INK, tsize=15, bsize=13, lead=None, bar=None):
        self.rect(x, y, w, h, fill=fill, stroke=stroke)
        if bar:
            self.parts.append(f'<path d="M {x+12} {y} h {w-24}" stroke="{bar}" '
                              f'stroke-width="4" stroke-linecap="round"/>')
        cx = x + w / 2
        ty = y + 26
        if title:
            ty = self.wrap(cx, ty, title, size=tsize, weight="700", fill=tcolor,
                           wpx=w - 24, max_lines=2)
        for ln in body:
            self.wrap(cx, ty + 6, ln, size=bsize, fill=MUTED, wpx=w - 24,
                      max_lines=3, leading=lead or bsize * 1.3)
            ty += 6 + (lead or bsize * 1.3) * 1.05

    def chip(self, x, y, s, fill=TEAL_L, stroke=TEAL, color=TEAL, size=12.5,
             pad=12, h=26):
        w = tw(s, size, "600") + pad * 2
        self.rect(x, y, w, h, fill=fill, stroke=stroke, rx=13, sw=1.1)
        self.text(x + w / 2, y + h / 2 + size * 0.36, s, size=size, weight="600",
                  fill=color)
        return w

    def legend(self, items, x=40, y=None, size=12.5, gap=22, vertical=False):
        y = self.h - 30 if y is None else y
        cx = x
        for label, color in items:
            if vertical:
                self.rect(cx, y - 9, 14, 14, fill=color, stroke="none", rx=4)
                self.text(cx + 22, y + 2, label, size=size, fill=MUTED, anchor="start")
                y += gap
            else:
                w = tw(label, size) + 34
                self.rect(cx, y - 10, 14, 14, fill=color, stroke="none", rx=4)
                self.text(cx + 21, y + 1.5, label, size=size, fill=MUTED, anchor="start")
                cx += w

    def badge(self, x, y, n, color=TEAL):
        self.circle(x, y, 15, fill=color, stroke="none")
        self.text(x, y + 5, str(n), size=14, weight="700", fill=WHITE)

    def note(self, x, y, w, s, fill=AMBER_L, stroke="#f0d9b5", color=AMBER,
             size=13, h=None, label="NOTE"):
        lines = split_lines(s, w - 32, size)
        h = h or 30 + len(lines) * (size * 1.35) + 8
        self.rect(x, y, w, h, fill=fill, stroke=stroke, rx=10)
        self.text(x + 14, y + 19, label, size=10.5, weight="700", fill=color,
                  anchor="start", spacing=1.2)
        self.wrap(x + 14, y + 40, s, size=size, fill=color, anchor="start",
                  wpx=w - 32, leading=size * 1.35)
        return h

    def lint(self, tol=1.2):
        """Return a list of layout problems: text overlaps and out-of-canvas text."""
        problems = []
        for x0, y0, x1, y1, s, size in self.labels:
            if x0 < -1 or y0 < -1 or x1 > self.w + 1 or y1 > self.h + 1:
                problems.append(f"OUT OF CANVAS: {s[:46]!r} bbox=({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
        L = self.labels
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                a, b = L[i], L[j]
                ox = min(a[2], b[2]) - max(a[0], b[0])
                oy = min(a[3], b[3]) - max(a[1], b[1])
                if ox > tol and oy > tol * 2:
                    problems.append(
                        f"OVERLAP ({ox:.0f}x{oy:.0f}): {a[4][:34]!r} <> {b[4][:34]!r}")
        return problems

    def save(self, path, autofit=True):
        if autofit and self.labels:
            need = max(l[3] for l in self.labels) + 16
            if need > self.h:
                self.h = int(need) + 1
                self.parts[0] = (f'<rect x="0" y="0" width="{self.w}" '
                                 f'height="{self.h}" fill="{WHITE}"/>')
        body = "\n  ".join(self.parts)
        defs = "\n    ".join(self.defs)
        doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" '
               f'height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img">\n'
               f'  <defs>\n    {defs}\n  </defs>\n  {body}\n</svg>\n')
        with open(path, "w", encoding="utf-8") as f:
            f.write(doc)
        return path
