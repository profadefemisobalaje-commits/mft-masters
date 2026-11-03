"""Theory & systems figures (01-11)."""
from figstyle import *


def fig01():
    s = SVG(980, 560, "Two Cybernetics of Family Therapy",
            "How the therapist's position changed the whole field")
    # panel 1
    s.rect(40, 100, 430, 380, fill=SLATE_L, stroke="#dbe3ec")
    s.text(255, 132, "FIRST-ORDER CYBERNETICS", size=15, weight="700", fill=SLATE, spacing=1)
    s.text(255, 154, "Observing a system from outside", size=13, fill=MUTED, italic=True)
    s.circle(255, 235, 34, fill=WHITE, stroke=TEAL, sw=2)
    s.text(255, 241, "Family", size=14, weight="700", fill=TEAL)
    s.arrow(150, 235, 205, 235, color=TEAL, label="input", loff=(0, -40))
    s.arrow(305, 235, 365, 235, color=TEAL, label="output", loff=(0, -40))
    s.rect(60, 200, 90, 70, fill=WHITE, stroke=LINE)
    s.wrap(105, 226, "Stimulus", 10, 12.5)
    s.rect(365, 200, 90, 70, fill=WHITE, stroke=LINE)
    s.wrap(410, 226, "Behaviour", 11, 12.5)
    s.circle(255, 372, 30, fill=AMBER_L, stroke=AMBER, sw=2)
    s.text(255, 370, "Therapist", size=12, weight="700", fill=AMBER)
    s.text(255, 384, "outside", size=10.5, fill=AMBER)
    s.arrow(255, 342, 255, 290, color=AMBER, dash="5 4")
    s.text(255, 440, "The observer stands apart, changes the", size=12.5, fill=MUTED)
    s.text(255, 458, "family, and measures the result.", size=12.5, fill=MUTED)
    # panel 2
    s.rect(510, 100, 430, 380, fill=TEAL_L, stroke="#c8e3dd")
    s.text(725, 132, "SECOND-ORDER CYBERNETICS", size=15, weight="700", fill=TEAL, spacing=1)
    s.text(725, 154, "The observer is part of the observed system", size=13, fill=MUTED, italic=True)
    s.circle(725, 258, 102, fill=WHITE, stroke=TEAL, sw=2)
    s.text(725, 202, "Family", size=15, weight="700", fill=TEAL)
    s.text(725, 222, "+ therapist + culture", size=11.5, fill=MUTED)
    s.circle(725, 300, 32, fill=AMBER, stroke="none")
    s.text(725, 296, "You", size=13, weight="700", fill=WHITE)
    s.text(725, 313, "inside", size=9.5, fill="#fdf3e3")
    s.arrow(690, 240, 690, 268, color=ROSE, sw=1.6, dash="4 3")
    s.arrow(762, 268, 762, 240, color=ROSE, sw=1.6, dash="4 3")
    s.text(725, 372, "Every intervention is also feedback:", size=12.5, fill=MUTED)
    s.text(725, 390, "the family adapts to being watched.", size=12.5, fill=MUTED)
    s.note(60, 500, 860,
           "Clinical use: knowing which cybernetics you are operating from tells you whether to "
           "aim at 'fixing' a family (first-order) or at co-creating new meanings and staying "
           "curious about your own effect on the system (second-order).", size=12.5)
    return s


def fig02():
    s = SVG(980, 660, "Circular Causality: The Pursue–Withdraw Loop",
            "No single villain: each response is the cause and consequence of the other")
    boxes = [
        (60, 110, "Aisha feels unheard", "tracks Sam's distance; asks\n'why are you so quiet?'", TEAL, "1"),
        (540, 110, "Aisha protests", "criticism, pursuit:\n'we never talk any more'", ROSE, "2"),
        (540, 350, "Sam withdraws", "TV, phone, late nights,\n'here we go again'", PLUM, "3"),
        (60, 350, "Sam feels criticised", "shuts down to keep the peace\nand avoid a fight", BLUE, "4"),
    ]
    for x, y, t, d, c, n in boxes:
        s.rect(x, y, 380, 120, fill=WHITE, stroke=c, rx=14)
        s.rect(x, y, 380, 5, fill=c, stroke="none", rx=3)
        s.badge(x + 34, y + 42, n, color=c)
        s.text(x + 60, y + 40, t, size=14, weight="700", fill=c, anchor="start", maxpx=300)
        for j, ln in enumerate(d.split("\n")):
            s.text(x + 60, y + 64 + j * 19, ln, size=10.5, fill=MUTED, anchor="start")
    # center
    s.circle(490, 290, 72, fill=SLATE, stroke="none")
    s.text(490, 282, "The loop", size=14, weight="700", fill=WHITE)
    s.text(490, 302, "is the client", size=11.5, fill="#cbd5e1")
    # arrows clockwise
    s.arrow(444, 170, 536, 170, color=ROSE, sw=2.4)
    s.arrow(730, 234, 730, 346, color=PLUM, sw=2.4)
    s.arrow(536, 410, 444, 410, color=BLUE, sw=2.4)
    s.arrow(250, 346, 250, 234, color=TEAL, sw=2.4)
    s.text(490, 148, "pursuit", size=10.5, weight="600", fill=ROSE)
    s.text(756, 292, "withdrawal", size=10.5, weight="600", fill=PLUM, anchor="start")
    s.text(490, 436, "protection", size=10.5, weight="600", fill=BLUE)
    s.text(222, 292, "renewed", size=10.5, weight="600", fill=TEAL, anchor="end")
    s.text(222, 308, "pursuit", size=10.5, weight="600", fill=TEAL, anchor="end")
    s.note(40, 500, 900,
           "Reframe in session: 'So the more you reach for him, the more he steps back; and the more "
           "he steps back, the more you reach. Neither of you invented this alone.' The reframe "
           "converts a character complaint into a pattern that both partners can change.", size=11.5)
    s.text(490, 596, "Each arrow is also a cause: your response is the trigger for my next move.",
           size=11.5, fill=SLATE, italic=True)
    return s


def fig03():
    s = SVG(980, 600, "Reading a Genogram: Standard Symbols",
            "Use the same visual grammar every time so three generations can be read at a glance")
    items = [
        ("male", "square"), ("female", "circle"), ("index client", "double"),
        ("deceased", "cross"), ("pregnancy loss", "triangle"), ("adopted", "bracket"),
        ("married", "marriage"), ("divorced", "divorce"), ("cohabiting", "cohabit"),
        ("twins", "twins"), ("conflict", "conflict"), ("cutoff", "cutoff"),
        ("close", "close"), ("enmeshed", "enmesh"), ("foster", "foster"),
    ]
    x0, y0, dx, dy = 90, 155, 190, 135
    for i, (label, kind) in enumerate(items):
        col, row = i % 5, i // 5
        x, y = x0 + col * dx, y0 + row * dy
        if kind == "male":
            s.rect(x - 20, y - 20, 40, 40, fill=WHITE, stroke=INK, rx=2)
        elif kind == "female":
            s.circle(x, y, 21, fill=WHITE, stroke=INK)
        elif kind == "double":
            s.rect(x - 24, y - 24, 48, 48, fill=WHITE, stroke=TEAL, rx=2, sw=2)
            s.rect(x - 17, y - 17, 34, 34, fill=WHITE, stroke=TEAL, rx=2, sw=2)
        elif kind == "cross":
            s.rect(x - 20, y - 20, 40, 40, fill=SLATE_L, stroke=INK, rx=2)
            s.line(x - 20, y - 20, x + 20, y + 20, stroke=ROSE, sw=2.4)
            s.line(x + 20, y - 20, x - 20, y + 20, stroke=ROSE, sw=2.4)
        elif kind == "triangle":
            s.path(f"M {x} {y-22} L {x+20} {y+16} L {x-20} {y+16} z",
                   stroke=INK, fill=WHITE, sw=1.5)
        elif kind == "bracket":
            s.line(x - 20, y + 22, x - 20, y - 6, stroke=INK, sw=1.8)
            s.line(x - 20, y - 6, x - 8, y - 6, stroke=INK, sw=1.8)
            s.circle(x + 8, y, 18, fill=WHITE, stroke=INK, dash="4 3")
        elif kind == "marriage":
            s.line(x - 45, y, x + 45, y, stroke=INK, sw=2)
            s.text(x, y - 10, "m. 2009", size=10.5, fill=MUTED)
        elif kind == "divorce":
            s.line(x - 45, y, x - 12, y, stroke=INK, sw=2)
            s.line(x + 12, y, x + 45, y, stroke=INK, sw=2)
            s.line(x - 10, y - 11, x + 8, y + 11, stroke=ROSE, sw=2)
            s.line(x + 8, y - 11, x - 10, y + 11, stroke=ROSE, sw=2)
        elif kind == "cohabit":
            s.line(x - 45, y, x + 45, y, stroke=INK, sw=2, dash="5 5")
        elif kind == "twins":
            s.line(x, y - 45, x, y - 26, stroke=INK, sw=2)
            s.line(x - 22, y - 26, x + 22, y - 26, stroke=INK, sw=2)
            s.line(x - 22, y - 26, x - 34, y - 8, stroke=INK, sw=2)
            s.line(x + 22, y - 26, x + 34, y - 8, stroke=INK, sw=2)
        elif kind == "conflict":
            s.path(f"M {x-40} {y} l 8 -9 l 8 18 l 8 -18 l 8 18 l 8 -18 l 8 18 l 8 -9",
                   stroke=ROSE, sw=2.2)
        elif kind == "cutoff":
            s.line(x - 42, y, x - 14, y, stroke=INK, sw=2)
            s.line(x + 14, y, x + 42, y, stroke=INK, sw=2)
            s.path(f"M {x-14} {y} l 6 -6 l -12 12 M {x+14} {y} l -6 -6 l 12 12",
                   stroke=ROSE, sw=2.2)
        elif kind == "close":
            s.line(x - 42, y, x + 42, y, stroke=INK, sw=2)
            s.line(x - 42, y + 6, x + 42, y + 6, stroke=INK, sw=2)
        elif kind == "enmesh":
            s.line(x - 42, y + 2, x + 42, y + 2, stroke=INK, sw=2)
            for k in range(3):
                s.line(x - 42 + k * 22, y + 2, x - 42 + k * 22 + 12, y + 12, stroke=INK, sw=1.4)
        elif kind == "foster":
            s.rect(x - 20, y - 20, 40, 40, fill=WHITE, stroke=INK, rx=2, dash="4 3")
            s.text(x, y + 5, "F", size=13, weight="700", fill=MUTED)
        s.text(x, y + 52, label, size=12.5, fill=MUTED)
    s.note(40, 540, 900,
           "Also record: ages or year of birth inside the symbol, date and cause of death above it, "
           "occupation, migration, religion, and significant secrets (affairs, incarceration, "
           "abuse) using a key that you explain to the family before you draw.", size=12.5)
    return s


def fig04():
    s = SVG(980, 720, "Three-Generation Genogram: The Adeyemi Family",
            "Presenting problem: 'Our 16-year-old daughter is out of control' — the map shows a wider story")
    for y, lab in [(166, "GENERATION 1"), (336, "GENERATION 2"), (516, "GENERATION 3")]:
        s.text(44, y, lab, size=10, weight="700", fill=MUTED, anchor="start", spacing=1.1)

    # ---------------- generation 1
    s.rect(228, 120, 44, 44, fill=SLATE_L, stroke=INK, rx=2)
    s.line(226, 118, 274, 166, stroke=ROSE, sw=2.2)
    s.line(274, 118, 226, 166, stroke=ROSE, sw=2.2)
    s.text(250, 148, "78", size=11.5, fill=MUTED)
    s.circle(360, 142, 22, fill=WHITE, stroke=INK)
    s.text(360, 147, "74", size=11.5, fill=MUTED)
    s.line(272, 142, 338, 142, stroke=INK, sw=2)
    s.text(305, 132, "1958", size=9.5, fill=MUTED)
    s.text(250, 186, "paternal grandsire", size=10.5, fill=MUTED)
    s.text(250, 201, "d. 1998, stroke", size=10, fill=ROSE)
    s.text(360, 186, "grandmother", size=10.5, fill=MUTED)
    s.text(360, 201, "the family's memory-keeper", size=9.5, fill=MUTED, italic=True)

    # ---------------- generation 2
    s.line(309, 142, 309, 258, stroke=INK, sw=1.8)
    s.line(196, 258, 400, 258, stroke=INK, sw=1.8)
    s.line(196, 258, 196, 276, stroke=INK, sw=1.8)
    s.line(400, 258, 400, 276, stroke=INK, sw=1.8)
    s.rect(174, 278, 44, 44, fill=WHITE, stroke=INK, rx=2)
    s.text(196, 306, "52", size=11.5, fill=MUTED)
    s.text(196, 344, "Uncle Emeka", size=10.5, fill=MUTED)
    s.text(196, 359, "cut off since 2011", size=10, fill=ROSE)
    s.rect(378, 278, 44, 44, fill=SLATE_L, stroke=INK, rx=2)
    s.text(400, 306, "49", size=11.5, fill=MUTED)
    s.text(400, 344, "Tunde (father)", size=10.5, fill=MUTED)
    s.text(400, 359, "alcohol misuse", size=10, fill=ROSE)
    s.circle(520, 300, 22, fill=SLATE_L, stroke=INK)
    s.text(520, 305, "46", size=11.5, fill=MUTED)
    s.text(560, 344, "Bisi (mother)", size=10.5, fill=MUTED)
    s.text(560, 359, "recurrent depression", size=10, fill=ROSE)
    s.line(422, 300, 498, 300, stroke=INK, sw=2)
    s.text(460, 291, "m. 2003", size=9.5, fill=MUTED)

    # cutoff between the brothers
    s.line(222, 300, 372, 300, stroke=INK, sw=1.8)
    s.path("M 292 300 l 7 -7 l -14 14 M 312 300 l -7 -7 l 14 14", stroke=ROSE, sw=2)
    s.text(302, 286, "cutoff", size=9.5, fill=ROSE)

    # conflict between parents
    s.path("M 432 312 l 7 -7 l 7 14 l 7 -14 l 7 14 l 7 -7", stroke=ROSE, sw=2)
    s.text(460, 332, "marital conflict", size=9, fill=ROSE)

    # ---------------- generation 3
    s.line(466, 300, 466, 468, stroke=INK, sw=1.8)
    s.line(400, 468, 560, 468, stroke=INK, sw=1.8)
    for x in (400, 500, 560):
        s.line(x, 468, x, 494, stroke=INK, sw=1.8)
    s.rect(378, 494, 44, 44, fill=WHITE, stroke=INK, rx=2)
    s.text(400, 522, "16", size=11.5, fill=MUTED)
    s.text(400, 560, "Amara (IP)", size=10.5, fill=MUTED)
    s.text(400, 575, "school refusal", size=10, fill=ROSE)
    s.circle(500, 516, 22, fill=WHITE, stroke=INK)
    s.text(500, 521, "13", size=11.5, fill=MUTED)
    s.text(500, 560, "Chidi", size=10.5, fill=MUTED)
    s.rect(538, 494, 44, 44, fill=WHITE, stroke=INK, rx=2)
    s.text(560, 522, "9", size=11.5, fill=MUTED)
    s.text(560, 560, "Dayo", size=10.5, fill=MUTED)

    # enmeshed mother-daughter
    s.line(506, 324, 428, 492, stroke=PLUM, sw=2, dash="3 4")
    s.text(432, 424, "enmeshed", size=9.5, fill=PLUM)

    # ---------------- hypotheses
    s.rect(620, 120, 330, 420, fill=PANEL, stroke=LINE, rx=12)
    s.text(785, 150, "Working hypotheses", size=13.5, weight="700", fill=SLATE)
    hyps = [
        ("Amara's symptoms regulate", "the parents' distance."),
        ("Bisi and Amara form a", "cross-generational coalition."),
        ("Tunde's drinking tracks the", "marital conflict cycle."),
        ("The paternal cutoff removed", "a source of practical support."),
        ("Migration and bereavement", "thinned the kin network."),
    ]
    y = 190
    for i, (a, b) in enumerate(hyps):
        s.badge(650, y + 2, i + 1, color=TEAL)
        s.text(672, y, a, size=10.5, fill=INK, anchor="start", maxpx=258)
        s.text(672, y + 17, b, size=10.5, fill=INK, anchor="start", maxpx=258)
        y += 64
    s.note(40, 636, 900,
           "Notice what the map does NOT tell you: the meaning the family gives to father's drinking, "
           "the voice of the absent uncle, and the resources (church, neighbours, income) that are "
           "not drawn. A genogram is a hypothesis generator, not a verdict.", size=11.5)
    return s


def fig05():
    s = SVG(980, 620, "Structural Mapping: Boundaries, Subsystems and Coalitions",
            "Minuchin's map: who is inside which boundary, and who stands with whom against whom")
    # panel A enmeshed
    s.rect(40, 96, 285, 400, fill=ROSE_L, stroke="#f2cbd6")
    s.text(182, 122, "ENMESHED", size=13, weight="700", fill=ROSE, spacing=1)
    s.ellipse(182, 250, 120, 96, fill=WHITE, stroke=ROSE, sw=2, dash="3 5")
    s.rect(118, 214, 34, 34, fill=WHITE, stroke=INK, rx=2)
    s.circle(206, 231, 17, fill=WHITE, stroke=INK)
    s.rect(160, 268, 30, 30, fill=WHITE, stroke=INK, rx=2)
    s.circle(212, 283, 15, fill=WHITE, stroke=INK)
    s.text(182, 372, "Diffuse boundaries", size=11.5, fill=ROSE)
    s.text(182, 390, "thoughts and feelings are", size=11, fill=MUTED)
    s.text(182, 406, "shared before they are owned", size=11, fill=MUTED)
    # panel B disengaged
    s.rect(345, 96, 285, 400, fill=BLUE_L, stroke="#cbd8f5")
    s.text(487, 122, "DISENGAGED", size=13, weight="700", fill=BLUE, spacing=1)
    for i, (x, y) in enumerate([(400, 210), (555, 210), (430, 300), (540, 300)]):
        if i in (0, 2):
            s.rect(x, y, 32, 32, fill=WHITE, stroke=INK, rx=2)
        else:
            s.circle(x + 16, y + 16, 16, fill=WHITE, stroke=INK)
    s.ellipse(487, 260, 145, 130, fill="none", stroke=BLUE, sw=2, dash="2 6")
    s.text(487, 372, "Rigid boundaries", size=11.5, fill=BLUE)
    s.text(487, 390, "little contact, low belonging,", size=11, fill=MUTED)
    s.text(487, 406, "autonomy without connection", size=11, fill=MUTED)
    # panel C coalition
    s.rect(650, 96, 290, 400, fill=PLUM_L, stroke="#ddd0f7")
    s.text(795, 122, "CROSS-GENERATIONAL", size=12, weight="700", fill=PLUM, spacing=0.8)
    s.text(795, 140, "COALITION", size=12, weight="700", fill=PLUM, spacing=0.8)
    s.rect(700, 176, 44, 44, fill=WHITE, stroke=INK, rx=2)
    s.text(722, 204, "F", size=13, weight="700", fill=MUTED)
    s.circle(860, 198, 22, fill=WHITE, stroke=INK)
    s.text(860, 203, "M", size=13, weight="700", fill=MUTED)
    s.line(744, 198, 838, 198, stroke=ROSE, sw=2.2)
    s.path("M 770 198 l 8 -7 l 8 14 l 8 -14 l 8 14 l 8 -7", stroke=ROSE, sw=2)
    s.text(791, 186, "conflict", size=9.5, fill=ROSE)
    s.rect(820, 290, 38, 38, fill=WHITE, stroke=INK, rx=2)
    s.text(839, 315, "C", size=13, weight="700", fill=MUTED)
    s.line(860, 220, 843, 288, stroke=PLUM, sw=3.2)
    s.line(722, 220, 780, 300, stroke=INK, sw=1.5, dash="5 5")
    s.text(795, 372, "Two against one; the child", size=11, fill=MUTED)
    s.text(795, 388, "carries the marital tension", size=11, fill=MUTED)
    s.text(795, 404, "and gains power by doing so", size=11, fill=MUTED)
    s.note(40, 518, 900,
           "Healthy structure is not 'no boundaries' or 'strong boundaries' — it is boundaries that "
           "are clear enough for hierarchy and close enough for belonging, and that flex when the "
           "family faces a normal transition.", size=12.5)
    return s


def fig06():
    s = SVG(980, 700, "Bowen's Eight Interlocking Concepts",
            "Differentiation of self is the anchor; the other seven describe what happens when it is low")
    cx, cy = 490, 340
    s.circle(cx, cy, 92, fill=SLATE, stroke="none")
    s.text(cx, cy - 10, "Differentiation", size=14, weight="700", fill=WHITE, maxpx=160)
    s.text(cx, cy + 8, "of self", size=14, weight="700", fill=WHITE)
    s.text(cx, cy + 34, "the anchor", size=10.5, fill="#cbd5e1")
    left = [
        ("Triangles", "two insiders, one outsider; anxiety moves to a third"),
        ("Nuclear family emotional process", "stress is absorbed by one member, the couple, or a child"),
        ("Family projection process", "parental anxiety lands on the most vulnerable child"),
        ("Multigenerational transmission", "patterns repeat across three or more generations"),
    ]
    right = [
        ("Emotional cutoff", "distance used as a solution; attachment stays unresolved"),
        ("Sibling position", "birth order and role shape adult expectations"),
        ("Societal emotional process", "culture, class, race and religion enter the system"),
        ("Chronic anxiety", "the fuel: reactivity to perceived threat"),
    ]
    for i, (t, b) in enumerate(left):
        y = 104 + i * 126
        s.rect(40, y, 260, 88, fill=WHITE, stroke=TEAL, rx=12)
        s.text(60, y + 24, t, size=11.5, weight="700", fill=TEAL, anchor="start", maxpx=232)
        s.wrap(60, y + 44, b, size=10, fill=MUTED, anchor="start", wpx=222, max_lines=3)
        s.line(302, y + 44, cx - 86, cy - 40 + i * 28, stroke=TEAL, sw=1.3, dash="3 3")
    for i, (t, b) in enumerate(right):
        y = 104 + i * 126
        s.rect(680, y, 260, 88, fill=WHITE, stroke=PLUM, rx=12)
        s.text(700, y + 24, t, size=11.5, weight="700", fill=PLUM, anchor="start", maxpx=232)
        s.wrap(700, y + 44, b, size=10, fill=MUTED, anchor="start", wpx=222, max_lines=3)
        s.line(678, y + 44, cx + 86, cy - 40 + i * 28, stroke=PLUM, sw=1.3, dash="3 3")
    s.note(40, 620, 900,
           "Differentiation is not independence or emotional coldness. It is the capacity to stay "
           "emotionally connected while holding your own convictions — 'I love you, and I still "
           "think this.'", size=11.5)
    return s


def fig07():
    s = SVG(980, 660, "The Family in Its Ecological Nested Systems",
            "Bronfenbrenner's bioecological model adapted for family therapy assessment")
    s.rect(30, 96, 920, 470, fill="#f4f7fb", stroke="#d5dfea", rx=16)
    s.text(56, 122, "MACROSYSTEM  culture · policy · religion · economy", size=11, weight="700",
           fill=MUTED, anchor="start", spacing=0.6)
    s.rect(90, 140, 800, 400, fill="#eaf0f8", stroke="#c9d6e6", rx=14)
    s.text(112, 166, "EXOSYSTEM  school board · workplace · health system · mass media", size=11,
           weight="700", fill=MUTED, anchor="start", spacing=0.5)
    s.rect(150, 184, 680, 330, fill="#e4ece0", stroke="#c3d3bd", rx=14)
    s.text(172, 210, "MESOSYSTEM  links between microsystems (home–school, home–clinic)", size=11,
           weight="700", fill=MUTED, anchor="start", spacing=0.4)
    s.rect(215, 230, 550, 258, fill=WHITE, stroke="#cbd5e1", rx=14)
    s.text(238, 256, "MICROSYSTEM  the family's daily settings", size=11, weight="700",
           fill=MUTED, anchor="start", spacing=0.5)
    # family core
    s.rect(300, 286, 44, 44, fill=WHITE, stroke=INK, rx=2)
    s.circle(408, 308, 22, fill=WHITE, stroke=INK)
    s.rect(486, 288, 40, 40, fill=WHITE, stroke=INK, rx=2)
    s.circle(548, 308, 20, fill=WHITE, stroke=INK)
    s.line(344, 308, 386, 308, stroke=INK, sw=2)
    s.line(430, 308, 486, 308, stroke=INK, sw=2)
    s.line(526, 308, 528, 308, stroke=INK, sw=2)
    s.text(428, 360, "the family", size=11.5, fill=MUTED, italic=True)
    s.rect(250, 392, 130, 62, fill=TEAL_L, stroke=TEAL, rx=8)
    s.text(315, 416, "church / mosque", size=11, fill=TEAL, weight="600")
    s.text(315, 434, "extended kin", size=11, fill=TEAL, weight="600")
    s.rect(400, 392, 120, 62, fill=AMBER_L, stroke=AMBER, rx=8)
    s.text(460, 416, "school", size=11, fill=AMBER, weight="600")
    s.text(460, 434, "health clinic", size=11, fill=AMBER, weight="600")
    s.rect(545, 392, 130, 62, fill=BLUE_L, stroke=BLUE, rx=8)
    s.text(610, 416, "peers", size=11, fill=BLUE, weight="600")
    s.text(610, 434, "social media", size=11, fill=BLUE, weight="600")
    s.text(300, 490, "CHRONOSYSTEM  time: migration, bereavement, policy change, family stage",
           size=11, weight="700", fill=MUTED, anchor="start")
    s.arrow(920, 470, 905, 470, color=MUTED, sw=1.2)
    s.note(40, 584, 900,
           "Assessment prompt: 'What outside this room is holding the problem in place — rent, "
           "school fees, a shift pattern, a hostile in-law, a visa application?' Therapy that stays "
           "inside the consulting room misses most of the system.", size=12.5)
    return s


def fig08():
    s = SVG(980, 660, "The Family Life Cycle: Six Stages and Their Tasks",
            "Symptom often appears at a stage transition, not inside a stage")
    stages = [
        ("1", "Leaving home", "Single young adults", "Differentiate from family of origin", TEAL),
        ("2", "Joinings", "New couple", "Commit to a new system; renegotiate with families", BLUE),
        ("3", "Young children", "Families with young children", "Make room for children; realign", GREEN),
        ("4", "Adolescents", "Families with teenagers", "Flex boundaries; shift to independence", AMBER),
        ("5", "Launching", "Children leaving", "Renegotiate the couple; accept new members", PLUM),
        ("6", "Later life", "Families in later life", "Accept generational roles; face loss", ROSE),
    ]
    for i, (n, name, who, task, c) in enumerate(stages):
        col, row = i % 3, i // 3
        x = 45 + col * 305
        y = 130 + row * 235
        s.rect(x, y, 285, 200, fill=WHITE, stroke=c, rx=14)
        s.rect(x, y, 285, 6, fill=c, stroke="none", rx=3)
        s.circle(x + 34, y + 44, 18, fill=c, stroke="none")
        s.text(x + 34, y + 50, n, size=15, weight="700", fill=WHITE)
        s.text(x + 62, y + 50, name, size=16, weight="700", fill=c, anchor="start")
        s.text(x + 22, y + 90, who, size=11.5, fill=MUTED, anchor="start", italic=True)
        s.wrap(x + 22, y + 122, task, width=38, size=12.5, fill=INK, anchor="start")
        s.text(x + 22, y + 182, "Risk: transition without renegotiation", size=10.5,
               fill=MUTED, anchor="start")
    s.note(40, 606, 900,
           "Carter and McGoldrick's framework is descriptive, not prescriptive: in many Nigerian and "
           "other African households, stages overlap (a grandparent fostering a child, an adult "
           "sibling living in), and 'launching' may be cyclical rather than linear. Treat the stages "
           "as questions to ask, not a timetable to enforce.", size=12.5)
    return s


def fig09():
    s = SVG(980, 620, "The Stages of Change (Transtheoretical Model)",
            "Match your intervention to the stage — advice given too early produces resistance")
    cx, cy, R = 490, 330, 195
    s.circle(cx, cy, R, fill=PANEL, stroke=LINE, sw=1.4)
    s.circle(cx, cy, 78, fill=WHITE, stroke=LINE)
    s.text(cx, cy - 6, "Relapse", size=14, weight="700", fill=ROSE)
    s.text(cx, cy + 14, "is data, not failure", size=10.5, fill=MUTED)
    import math
    nodes = [
        ("Pre-contemplation", "not thinking about it", TEAL),
        ("Contemplation", "ambivalent, weighing it up", BLUE),
        ("Preparation", "planning a change", GREEN),
        ("Action", "doing it, first 6 months", AMBER),
        ("Maintenance", "sustaining, 6 months+", PLUM),
    ]
    for i, (n, sub, c) in enumerate(nodes):
        ang = -math.pi / 2 + i * (2 * math.pi / 5)
        x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
        s.rect(x - 82, y - 34, 164, 68, fill=WHITE, stroke=c, rx=12)
        s.text(x, y - 6, n, size=12.5, weight="700", fill=c)
        s.text(x, y + 15, sub, size=10.5, fill=MUTED)
    # rotation arrows
    for i in range(5):
        a1 = -math.pi / 2 + i * (2 * math.pi / 5) + 0.34
        a2 = a1 + 0.52
        x1, y1 = cx + (R - 62) * math.cos(a1), cy + (R - 62) * math.sin(a1)
        x2, y2 = cx + (R - 62) * math.cos(a2), cy + (R - 62) * math.sin(a2)
        s.arrow(x1, y1, x2, y2, color=MUTED, sw=1.5)
    s.note(40, 530, 900,
           "In family work, 'the client' is plural: a wife may sit in action while her husband sits "
           "in pre-contemplation. Interventions must be staged for each member, or the more "
           "motivated partner becomes the identified enforcer.", size=12.5)
    return s


def fig10():
    s = SVG(980, 540, "Positive and Negative Feedback in a Family System",
            "A thermostat and a household used to illustrate the same logic")
    s.rect(40, 100, 430, 300, fill=PANEL, stroke=LINE, rx=12)
    s.text(255, 124, "MECHANICAL EXAMPLE", size=11.5, weight="700", fill=MUTED, spacing=1)
    s.rect(205, 150, 100, 46, fill=WHITE, stroke=TEAL, rx=8)
    s.text(255, 178, "thermostat 18°C", size=11.5, fill=TEAL, weight="600")
    s.circle(255, 280, 34, fill=AMBER_L, stroke=AMBER)
    s.text(255, 276, "heater", size=11.5, fill=AMBER, weight="600")
    s.text(255, 292, "ON", size=10, fill=AMBER)
    s.arrow(215, 200, 230, 250, color=TEAL, sw=1.8, label="too cold", loff=(-34, -6))
    s.arrow(290, 250, 292, 200, color=ROSE, sw=1.8, label="heat", loff=(26, 22))
    s.text(255, 356, "Negative feedback (corrective): deviation is reduced.", size=11.5, fill=MUTED)
    s.rect(500, 100, 440, 300, fill=TEAL_L, stroke="#c8e3dd", rx=12)
    s.text(720, 124, "FAMILY EXAMPLE", size=11.5, weight="700", fill=TEAL, spacing=1)
    s.rect(560, 150, 145, 60, fill=WHITE, stroke=ROSE, rx=8)
    s.text(632, 174, "Ade fails an exam", size=11.5, fill=ROSE, weight="600")
    s.text(632, 192, "tension rises", size=10, fill=MUTED)
    s.rect(755, 150, 145, 60, fill=WHITE, stroke=BLUE, rx=8)
    s.text(827, 174, "Parents argue", size=11.5, fill=BLUE, weight="600")
    s.text(827, 192, "about discipline", size=10, fill=MUTED)
    s.rect(755, 268, 145, 60, fill=WHITE, stroke=AMBER, rx=8)
    s.text(827, 292, "Ade's behaviour", size=11.5, fill=AMBER, weight="600")
    s.text(827, 310, "worsens", size=10, fill=MUTED)
    s.rect(560, 268, 145, 60, fill=WHITE, stroke=PLUM, rx=8)
    s.text(632, 292, "More monitoring", size=11.5, fill=PLUM, weight="600")
    s.text(632, 310, "and blame", size=10, fill=MUTED)
    s.arrow(705, 180, 753, 180, color=ROSE, sw=1.8)
    s.arrow(827, 210, 827, 266, color=BLUE, sw=1.8)
    s.arrow(753, 298, 707, 298, color=AMBER, sw=1.8)
    s.arrow(632, 266, 632, 212, color=PLUM, sw=1.8)
    s.text(720, 356, "Positive feedback (amplifying): deviation is increased.", size=11.5, fill=MUTED)
    s.note(40, 424, 900,
           "Both types are always present. Therapy usually adds a negative-feedback loop where an "
           "amplifying one is running — for example, a bedtime routine that interrupts the "
           "'he won't sleep → we argue → he is anxious → he won't sleep' spiral.", size=12.5)
    return s


def fig11():
    s = SVG(980, 620, "Watzlawick's Five Axioms of Communication",
            "Every message has a report and a command; every relationship is a punctuation of events")
    items = [
        ("1", "One cannot not communicate", "Silence, lateness and a turned back are messages.",
         "A husband's silence at dinner is read as punishment — and is communication either way.", TEAL),
        ("2", "Every message has content and relationship levels",
         "The report carries information; the command defines the relationship.",
         "'The bin is full' can mean information, or 'you are lazy'.", BLUE),
        ("3", "Punctuation organises the sequence of events",
         "Each partner believes the other started it.",
         "She says he withdraws; he says she nags. Both are describing the same loop from opposite ends.", GREEN),
        ("4", "Humans communicate digitally and analogically",
         "Words are digital; tone, posture and timing are analogical.",
         "A text saying 'fine' with a three-hour delay carries two different messages.", AMBER),
        ("5", "Relationships are symmetrical or complementary",
         "Equal/competitive versus unequal/one-up–one-down.",
         "Two high achievers escalate (symmetrical); a 'strong' parent and a 'weak' child lock in (complementary).", PLUM),
    ]
    y = 108
    for n, t, expl, ex, c in items:
        s.rect(40, y, 900, 88, fill=WHITE, stroke="#dde4ec", rx=10)
        s.rect(40, y, 6, 88, fill=c, stroke="none", rx=3)
        s.circle(78, y + 44, 17, fill=c, stroke="none")
        s.text(78, y + 50, n, size=14, weight="700", fill=WHITE)
        s.text(108, y + 34, t, size=14, weight="700", fill=c, anchor="start")
        s.text(108, y + 56, expl, size=11.5, fill=MUTED, anchor="start")
        s.text(108, y + 76, "e.g. " + ex, size=11, fill=INK, anchor="start", italic=True)
        y += 98
    s.note(40, 572, 900,
           "Axiom 3 is the therapist's most useful tool: asking each member to punctuate the same "
           "sequence aloud makes the loop visible without assigning blame.", size=12.5)
    return s
