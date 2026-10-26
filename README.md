# MSc Marriage and Family Therapy — Complete Lecture Library

A full, teachable postgraduate curriculum written as **28 standalone volumes** — the 27 taught courses
(Semesters One–Three plus all six electives) and the Master Thesis — supported by **40 original figures**
(genograms, systemic maps, neurobiology schematics, room layouts, decision models) that you can print,
project, or reuse in slides.

Each book is built to carry a **14–16 week semester**: a week-by-week teaching plan, lecture content, worked
cases, in-class practicals, assessment, glossary, and further reading. Nothing here is a summary — the books
are written to be taught from.

Every volume also exists as a **finished A4 PDF** — cover, imprint, contents with page numbers, running
heads, folios, embedded figures and bookmarks — in [`pdf/`](pdf/README.md), and the whole programme is
bound into one 449-page file.

---

## Start here

| If you are… | Open |
|---|---|
| A student | [Programme handbook](00-programme/00-programme-handbook.md) |
| A lecturer | [Teaching and assessment guide](00-programme/01-teaching-and-assessment-guide.md) |
| Looking for a diagram | [Figure index](00-programme/02-figure-index.md) or the visual [Figure gallery](00-programme/03-figure-gallery.md) |
| Wanting a printed book | [PDF print edition](pdf/README.md) — one A4 PDF per course, or the [complete library in one file](pdf/MFT-Library-Complete-28-volumes.pdf) |
| Wanting to browse everything | `python3 scripts/build_site.py`, then open `site/index.html` (or `python3 -m http.server`) |

---

## The programme

### Semester One
| Code | Course | Book |
|---|---|---|
| MFT 701 | Fundamentals of Marriage and Family Therapy | [open](01-semester-one/MFT-701-fundamentals-of-marriage-and-family-therapy.md) |
| MFT 702 | Theories of Family Therapy | [open](01-semester-one/MFT-702-theories-of-family-therapy.md) |
| MFT 703 | Human Development Across the Lifespan | [open](01-semester-one/MFT-703-human-development-across-the-lifespan.md) |
| MFT 704 | Ethical and Legal Issues in Therapy | [open](01-semester-one/MFT-704-ethical-and-legal-issues-in-therapy.md) |
| MFT 705 | Research Methods in Marriage and Family Therapy | [open](01-semester-one/MFT-705-research-methods-in-mft.md) |
| MFT 706 | Clinical Practice and Techniques | [open](01-semester-one/MFT-706-clinical-practice-and-techniques.md) |
| MFT 707 | Assessment and Diagnosis in Family Therapy | [open](01-semester-one/MFT-707-assessment-and-diagnosis-in-family-therapy.md) |
| MFT 708 | Cultural Competence in Therapy | [open](01-semester-one/MFT-708-cultural-competence-in-therapy.md) |

### Semester Two
| Code | Course | Book |
|---|---|---|
| MFT 709 | Group Therapy Techniques | [open](02-semester-two/MFT-709-group-therapy-techniques.md) |
| MFT 710 | Couples Therapy | [open](02-semester-two/MFT-710-couples-therapy.md) |
| MFT 711 | Child and Adolescent Therapy | [open](02-semester-two/MFT-711-child-and-adolescent-therapy.md) |
| MFT 712 | Crisis Intervention Strategies | [open](02-semester-two/MFT-712-crisis-intervention-strategies.md) |
| MFT 713 | Substance Abuse and Family Dynamics | [open](02-semester-two/MFT-713-substance-abuse-and-family-dynamics.md) |
| MFT 714 | Trauma-Informed Care | [open](02-semester-two/MFT-714-trauma-informed-care.md) |
| MFT 715 | Family Systems Theory | [open](02-semester-two/MFT-715-family-systems-theory.md) |

### Semester Three
| Code | Course | Book |
|---|---|---|
| MFT 716 | Communication Skills in Therapy | [open](03-semester-three/MFT-716-communication-skills-in-therapy.md) |
| MFT 717 | Psychopathology in Families | [open](03-semester-three/MFT-717-psychopathology-in-families.md) |
| MFT 718 | Intimacy and Relationship Dynamics | [open](03-semester-three/MFT-718-intimacy-and-relationship-dynamics.md) |
| MFT 719 | Family Life Cycle and Transitions | [open](03-semester-three/MFT-719-family-life-cycle-and-transitions.md) |
| MFT 720 | Supervision and Consultation in Therapy | [open](03-semester-three/MFT-720-supervision-and-consultation.md) |
| MFT 721 | Research Methodology | [open](03-semester-three/MFT-721-research-methodology.md) |
| MFT 770 | Master Thesis | [open](03-semester-three/MFT-770-master-thesis.md) |

### Electives
| Code | Course | Book |
|---|---|---|
| MFT 722 | Professional Development and Self-Care | [open](04-electives/MFT-722-professional-development-and-self-care.md) |
| MFT 723 | Special Populations in Therapy | [open](04-electives/MFT-723-special-populations-in-therapy.md) |
| MFT 724 | Family Law and Advocacy | [open](04-electives/MFT-724-family-law-and-advocacy.md) |
| MFT 725 | Integrative Approaches in Therapy | [open](04-electives/MFT-725-integrative-approaches-in-therapy.md) |
| MFT 726 | Neurobiology of Relationships | [open](04-electives/MFT-726-neurobiology-of-relationships.md) |
| MFT 727 | Play Therapy Techniques | [open](04-electives/MFT-727-play-therapy-techniques.md) |

---

## The print edition

There are two ways to read the library: as Markdown/HTML, or as a finished book. The `pdf/` folder holds
**29 PDFs** — one per course, plus the whole library in a single bookmarked volume.

| Edition | What it is | Where |
|---|---|---|
| Course PDFs | 28 files, A4, 11–27 pages each, 447 pages in total | [`pdf/`](pdf/README.md) |
| Complete library | all 28 volumes in programme order, 449 pages, nested bookmarks | [MFT-Library-Complete-28-volumes.pdf](pdf/MFT-Library-Complete-28-volumes.pdf) |

Each PDF opens with a cover carrying the course code, semester, unit value and prerequisite; an imprint
page with the citation, licence and the fictional-case statement; and a page listing every course in the
programme with the current volume marked. Then comes a two-level contents with real page numbers, the full
course text, and the back matter — integration chapter, glossary, self-assessment with model answers,
further reading.

The PDFs are **generated from the Markdown**, so the text has a single source of truth:

```bash
python3 scripts/build_pdfs.py              # 28 course PDFs -> pdf/
python3 scripts/build_pdfs.py --complete   # + the merged 449-page volume
python3 scripts/build_pdfs.py --only MFT-701
```

They need `reportlab`, `pillow`, `pypdf` and a `node` install of `@resvg/resvg-js` (used to turn the SVG
figures into print-resolution PNGs, so no reader ever has to render SVG). Type is DejaVu Serif and DejaVu
Sans throughout, embedded in every file, with italic faces synthesised by shearing so the output does not
change with the machine.

---

## How each book is structured

```
# MFT xxx — Course title
   Cover block: semester, units, prerequisites, lecturer-facing summary
## How to use this book
## Course description and rationale
## Learning outcomes (mapped to weeks)
## Assessment scheme
## The 14–16 week teaching plan           ← table: week, topic, activity, reading
## Week 1 … Week 16                        ← taught content, cases, practicals
## Integration chapter                    ← the whole course on two pages
## Glossary
## Self-assessment                        ← MCQs with key, short answers, essay questions
## Practical / clinical log requirements
## Further reading and references
```

Figures are embedded as `![Figure x.y — caption](../assets/figures/figNN-slug.svg)`. They are SVG, so they
stay sharp at any size, print cleanly, and can be recoloured or edited in any vector tool.

---

## Working with the repository

```bash
python3 scripts/build_figures.py       # regenerate all 40 figures + layout lint
python3 scripts/build_site.py          # build the HTML edition into site/
python3 scripts/build_site.py --serve  # build, then serve on :8000
python3 scripts/build_pdfs.py          # build the 28 A4 PDFs into pdf/
python3 scripts/build_pdfs.py --complete  # + the single 449-page library volume
```

* `scripts/figstyle.py` — a small SVG toolkit with real font metrics and a layout linter, so figures do not
  produce overlapping labels.
* `scripts/figs_*.py` — the figure definitions (theory, clinical, practice).
* `scripts/build_site.py` — Markdown → static HTML with sidebar, search and print CSS.
* `scripts/build_pdfs.py` — Markdown → A4 PDF: typesetting, tables, callouts, covers, contents, bookmarks.
* `scripts/svg2png.js` — figure rasteriser used by the PDF build (`@resvg/resvg-js`).
* `site/` — the generated HTML edition (safe to delete and rebuild; committed so it can be opened directly).
* `pdf/` — the generated print edition (also committed, so the books can be handed out as-is).

The figure scripts also **lint** each drawing: they report out-of-canvas text and overlapping labels, and the
build prints `0 layout problem(s)` when everything is clean.

---

## A note on scope, culture and safety

The books are written from an **integrative, systemic** stance and are deliberately grounded in Nigerian and
wider African clinical realities — extended family, faith communities, customary and statutory marriage,
migration, economic strain, and multilingual consulting rooms — while remaining faithful to the international
evidence base (AAMFT, IAMFC, EFTA, APA, WHO).

Three commitments run through every book:

1. **Safety first.** Risk assessment, safeguarding, intimate-partner violence screening and the limits of
   confidentiality are treated as core clinical skills, not footnotes.
2. **Cultural humility over cultural competence as a checklist.** Culture is interrogated as a set of
   positions with power attached, not a box to tick.
3. **Practise on yourself before you practise on clients.** Every week ends with a reflective task, because
   the therapist's own family of origin is the first instrument of the work.

These books are **educational materials**, not a substitute for supervised clinical practice, professional
registration, legal advice, or medical care. Case material throughout is fictional and composite; any
resemblance to real families is coincidental. Legal content is orientation only — verify all statutes and
procedure with a qualified lawyer in the relevant jurisdiction.

---

## Licence and reuse

Content and figures: **Creative Commons Attribution 4.0 (CC BY 4.0)**. Reuse, adapt and translate with
attribution. The figures are generated by the scripts in `scripts/` (no third-party images), so there is no
attribution stacking and no copyright risk in teaching materials.
