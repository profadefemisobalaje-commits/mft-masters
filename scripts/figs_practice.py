"""Research, formulation and practice-management figures (28-40)."""
from figstyle import *
import math


def _pie(s, cx, cy, r, slices, colors):
    a = -90
    for frac, c in zip(slices, colors):
        b = a + frac * 360
        x1, y1 = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        x2, y2 = cx + r * math.cos(math.radians(b)), cy + r * math.sin(math.radians(b))
        large = 1 if (b - a) > 180 else 0
        s.path(f"M {cx} {cy} L {x1:.1f} {y1:.1f} A {r} {r} 0 {large} 1 {x2:.1f} {y2:.1f} Z",
               fill=c, stroke=WHITE, sw=2)
        a = b


def fig28():
    s = SVG(980, 660, "Choosing a Research Design",
            "Start with the question, not with the method you happen to like")
    s.rect(300, 92, 380, 62, fill=SLATE, stroke="none", rx=12)
    s.text(490, 120, "WHAT KIND OF QUESTION IS IT?", size=13, weight="700", fill=WHITE, spacing=0.7)
    s.text(490, 140, "and what can you feasibly access?", size=10.5, fill="#cbd5e1")
    branches = [
        (135, "HOW MUCH, HOW OFTEN,\nDOES X CAUSE Y?", TEAL, [
            "Survey / cross-sectional",
            "Longitudinal cohort",
            "Quasi-experiment",
            "Randomised trial",
            "Single-case (N=1) design"]),
        (390, "WHAT DOES IT MEAN,\nHOW IS IT LIVED?", PLUM, [
            "Phenomenology",
            "Grounded theory",
            "Ethnography",
            "Case study",
            "Narrative inquiry"]),
        (645, "BOTH, AND THE MIX\nMATTERS?", AMBER, [
            "Explanatory sequential",
            "Exploratory sequential",
            "Convergent parallel",
            "Embedded design",
            "Participatory action research"]),
    ]
    for x, head, c, items in branches:
        s.arrow(490, 156, x + 110, 196, color=c, sw=2)
        s.rect(x, 200, 220, 80, fill=WHITE, stroke=c, rx=10)
        for j, ln in enumerate(head.split("\n")):
            s.text(x + 110, 226 + j * 18, ln, size=10.5, weight="700", fill=c)
        y = 300
        for it in items:
            s.line(x + 110, y - 22, x + 110, y - 8, stroke=c, sw=1.2)
            s.rect(x, y, 220, 38, fill=PANEL, stroke="#dde4ec", rx=8)
            s.text(x + 110, y + 23, it, size=10.5, fill=INK)
            y += 48
    s.rect(895, 200, 62, 360, fill=SLATE_L, stroke="none", rx=8)
    s.text(926, 300, "ETHICS", size=10, weight="700", fill=SLATE, anchor="middle")
    s.text(926, 320, "approval", size=9, fill=MUTED, anchor="middle")
    s.text(926, 360, "consent", size=9, fill=MUTED, anchor="middle")
    s.text(926, 400, "risk plan", size=9, fill=MUTED, anchor="middle")
    s.text(926, 440, "data plan", size=9, fill=MUTED, anchor="middle")
    s.text(926, 480, "feedback", size=9, fill=MUTED, anchor="middle")
    s.note(40, 596, 900,
           "In MFT the unit of analysis is the relationship, not only the individual — which creates "
           "real statistical problems: partners are non-independent. Plan for it (dyadic data "
           "analysis, actor–partner models, or a design that samples one person per household).",
           size=11)
    return s


def fig29():
    s = SVG(980, 600, "Validity and Reliability: Four Targets, Three Kinds of Consistency",
            "A measure can be reliable without being valid; it cannot be valid without being reliable")
    # dartboards
    labels = [
        ("Internal validity", "did the intervention,\nnot something else,\nproduce the change?", TEAL),
        ("External validity", "can these findings\ntravel to other families,\nsettings, cultures?", BLUE),
        ("Construct validity", "are you really measuring\n'alliance' and not\n'social desirability'?", AMBER),
        ("Statistical validity", "is the effect large enough\nand the test powerful\nenough to trust?", PLUM),
    ]
    for i, (t, d, c) in enumerate(labels):
        x = 130 + i * 235
        for rr, cc in [(46, "#eef2f7"), (32, "#dde6f0"), (18, c)]:
            s.circle(x, 190, rr, fill=cc, stroke=WHITE, sw=1.4)
        # darts
        offs = [(6, -4), (-8, 5), (2, 10), (10, 6)][i]
        if i == 2:
            offs = (-26, 12)
        s.circle(x + offs[0], 190 + offs[1], 3.5, fill=ROSE, stroke="none")
        s.line(x + offs[0], 190 + offs[1], x + offs[0] + 22, 190 + offs[1] - 22, stroke=ROSE, sw=2)
        s.text(x, 262, t, size=12, weight="700", fill=c)
        for j, ln in enumerate(d.split("\n")):
            s.text(x, 284 + j * 15, ln, size=10, fill=MUTED)
    s.rect(60, 340, 860, 150, fill=PANEL, stroke=LINE, rx=12)
    s.text(86, 368, "THREE WAYS TO DEMONSTRATE RELIABILITY", size=11, weight="700", fill=SLATE,
           anchor="start", spacing=0.8)
    rel = [
        ("Test–retest", "same people, two occasions", "stability over time"),
        ("Inter-rater", "two coders, same material", "agreement between observers"),
        ("Internal consistency", "items within one scale", "Cronbach's alpha, ω"),
    ]
    for i, (a, b, c) in enumerate(rel):
        x = 90 + i * 285
        s.text(x, 400, a, size=11.5, weight="700", fill=TEAL, anchor="start")
        s.text(x, 420, b, size=10, fill=MUTED, anchor="start")
        s.text(x, 438, "→ " + c, size=9.5, fill=MUTED, anchor="start")
    s.note(40, 518, 900,
           "Practical caution with family measures: a couple's score is not the sum of two individual "
           "scores, and self-report is vulnerable to the 'halo' of a partner in the room. Prefer "
           "multi-informant, multi-method assessment (self-report + observation + collateral).",
           size=11)
    return s


def fig30():
    s = SVG(980, 620, "The Family Assessment Sequence",
            "Assessment is a relationship, not an interrogation: gather, observe, feed back, agree")
    steps = [
        ("Referral", "who is worried, and why now?", TEAL),
        ("Contracting", "consent, confidentiality limits, fees, goals", BLUE),
        ("Multi-informant intake", "each member's view; history; genogram", GREEN),
        ("Standardised measures", "functioning, satisfaction, symptoms, risk", AMBER),
        ("Interaction observation", "watch the family solve a real problem", PLUM),
        ("Formulation + feedback", "share a map, invite correction", ROSE),
        ("Plan + review", "measurable goals, review date", SLATE),
    ]
    for i, (t, d, c) in enumerate(steps):
        col, row = i % 4, i // 4
        x = 50 + col * 232
        y = 120 + row * 190
        s.rect(x, y, 210, 150, fill=WHITE, stroke=c, rx=12)
        s.rect(x, y, 210, 6, fill=c, stroke="none", rx=3)
        s.badge(x + 28, y + 40, i + 1, color=c)
        s.wrap(x + 105, y + 76, t, 19, 12, weight="700", fill=c, max_lines=2)
        s.wrap(x + 105, y + 112, d, 27, 9.8, fill=MUTED, max_lines=3)
        if col < 3:
            s.arrow(x + 212, y + 75, x + 228, y + 75, color=MUTED, sw=1.4)
    s.arrow(690, 280, 690, 300, color=MUTED, sw=1.4)
    s.arrow(600, 300, 575, 300, color=MUTED, sw=1.4)
    s.arrow(470, 300, 445, 300, color=MUTED, sw=1.4)
    s.arrow(350, 300, 325, 300, color=MUTED, sw=1.4)
    s.arrow(220, 300, 195, 300, color=MUTED, sw=1.4)
    s.rect(50, 430, 880, 130, fill=PANEL, stroke=LINE, rx=12)
    s.text(76, 458, "MINIMUM ASSESSMENT PACKAGE FOR A MASTER'S-LEVEL CLINIC", size=11, weight="700",
           fill=SLATE, anchor="start", spacing=0.6)
    packs = [
        "Presenting problem + onset + attempted solutions",
        "Genogram (3 generations) and migration history",
        "Risk screen: harm to self/others, abuse, IPV, safeguarding",
        "Functioning + relationship satisfaction measure",
        "Cultural, religious and language context; who holds power",
        "Client's own goals, in the client's own words",
    ]
    for i, p in enumerate(packs):
        col, row = i % 2, i // 2
        s.text(84 + col * 430, 486 + row * 24, "• " + p, size=10, fill=INK, anchor="start")
    s.note(40, 570, 900,
           "Feedback tip: present the formulation as a draft hypothesis with three parts — 'Here is "
           "what I think is happening; here is what I am less sure about; what have I got wrong?' "
           "Correction by the family increases buy-in and accuracy.", size=11)
    return s


def fig31():
    s = SVG(980, 620, "The 5-P Formulation Grid",
            "A transdiagnostic scaffold you can use with any presenting problem")
    cols = [
        ("PRESENTING", "What is happening now?", [
            "Amara, 16: school refusal for 6 weeks",
            "Parents in escalating conflict about discipline",
            "Weekly panic symptoms before school"], ROSE),
        ("PREDISPOSING", "What made this more likely?", [
            "Maternal history of depression",
            "Early separation during migration",
            "Family pattern of 'no feelings talk'"], TEAL),
        ("PRECIPITATING", "What tipped it over?", [
            "Father's job loss and increased drinking",
            "Best friend moved away",
            "Transition to senior secondary"], AMBER),
        ("PERPETUATING", "What keeps it going?", [
            "Parents' conflict cycle; mother–daughter coalition",
            "School avoidance rewarded by reduced anxiety",
            "Sleep disruption and phone use at night"], PLUM),
        ("PROTECTIVE", "What is already working?", [
            "Strong church community; aunt as ally",
            "Amara's engagement in art",
            "Parents both attend and want change"], GREEN),
    ]
    x = 45
    for t, q, items, c in cols:
        s.rect(x, 110, 172, 340, fill=WHITE, stroke=c, rx=12)
        s.rect(x, 110, 172, 6, fill=c, stroke="none", rx=3)
        s.text(x + 86, 142, t, size=11, weight="700", fill=c, spacing=0.8)
        s.text(x + 86, 164, q, size=9.5, fill=MUTED, italic=True)
        y = 190
        for it in items:
            s.wrap(x + 86, y, it, 20, 9.5, fill=INK, max_lines=3, leading=13)
            y += 60
        x += 181
    s.rect(45, 470, 890, 48, fill=SLATE, stroke="none", rx=10)
    s.text(490, 500, "Then write one sentence: 'Given ___, ___ and ___, the most useful focus now is ___ "
                     "because it is the most changeable.'", size=11, fill=WHITE)
    s.note(40, 532, 900,
           "The grid is a hypothesis, not a verdict. Share it, invite edits, and revisit it after "
           "four sessions. A formulation that never changes is usually a formulation nobody shared.",
           size=11)
    return s


def fig32():
    s = SVG(980, 640, "Supervision: The Triangle and Parallel Process",
            "What happens between therapist and client often reappears between supervisee and supervisor")
    # triangle
    s.path("M 250 430 L 420 140 L 590 430 Z", fill=PANEL, stroke=LINE, sw=1.6)
    s.rect(355, 96, 130, 54, fill=TEAL, stroke="none", rx=10)
    s.text(420, 128, "SUPERVISOR", size=11, weight="700", fill=WHITE, spacing=0.8)
    s.rect(180, 430, 140, 54, fill=BLUE, stroke="none", rx=10)
    s.text(250, 462, "THERAPIST", size=11, weight="700", fill=WHITE, spacing=0.8)
    s.rect(520, 430, 140, 54, fill=ROSE, stroke="none", rx=10)
    s.text(590, 462, "CLIENT / FAMILY", size=10, weight="700", fill=WHITE, spacing=0.6)
    s.text(300, 300, "evaluation", size=10, fill=MUTED)
    s.text(560, 300, "support", size=10, fill=MUTED)
    s.text(420, 520, "therapeutic relationship", size=10, fill=MUTED)
    s.arrow(340, 380, 250, 432, color=TEAL, sw=1.4, dash="4 3")
    s.arrow(500, 380, 590, 432, color=TEAL, sw=1.4, dash="4 3")
    # parallel process
    s.rect(660, 96, 280, 380, fill=WHITE, stroke=LINE, rx=12)
    s.text(800, 124, "PARALLEL PROCESS", size=10.5, weight="700", fill=SLATE, spacing=0.8)
    s.rect(690, 150, 220, 60, fill=PLUM_L, stroke=PLUM, rx=8)
    s.text(800, 174, "Client is helpless,", size=10, fill=INK)
    s.text(800, 190, "demands answers", size=10, fill=INK)
    s.rect(690, 250, 220, 60, fill=PLUM_L, stroke=PLUM, rx=8)
    s.text(800, 274, "Therapist feels stuck,", size=10, fill=INK)
    s.text(800, 290, "wants to be told what to do", size=10, fill=INK)
    s.rect(690, 350, 220, 60, fill=PLUM_L, stroke=PLUM, rx=8)
    s.text(800, 374, "Supervisee presents", size=10, fill=INK)
    s.text(800, 390, "'just tell me the technique'", size=10, fill=INK)
    s.arrow(800, 212, 800, 248, color=PLUM, sw=1.6)
    s.arrow(800, 312, 800, 348, color=PLUM, sw=1.6)
    s.text(800, 442, "Same shape, three rooms", size=10, fill=PLUM, italic=True)
    s.text(200, 560, "Four supervision tasks", size=11.5, weight="700", fill=SLATE)
    tasks = ["1  Monitor client welfare and safety", "2  Develop clinical skill and conceptualisation",
             "3  Ensure ethical and legal compliance", "4  Support the person of the therapist"]
    for i, t in enumerate(tasks):
        x = 60 + (i % 2) * 440
        y = 582 + (i // 2) * 26
        s.text(x, y, t, size=10.5, fill=INK, anchor="start")
    return s


def fig33():
    s = SVG(980, 660, "An Ethics Decision-Making Model",
            "Work the steps in order and write down what you decided and why")
    steps = [
        ("Identify the dilemma", "What exactly is the conflict? Facts, not assumptions.", TEAL),
        ("Check the codes", "Professional code, law, employer policy, cultural norms.", BLUE),
        ("Consult", "A trusted senior colleague, supervisor, ethics committee.", GREEN),
        ("Generate options", "At least three, including the uncomfortable one.", AMBER),
        ("Weigh consequences", "Who is affected? Harm, rights, duties, power.", PLUM),
        ("Decide and act", "Choose, document, and tell the client what you are doing.", ROSE),
        ("Evaluate", "What happened? Would you decide the same again?", SLATE),
    ]
    for i, (t, d, c) in enumerate(steps):
        x = 90 + i * 26
        y = 520 - i * 58
        s.rect(x, y, 640 - i * 20, 46, fill=WHITE, stroke=c, rx=8)
        s.rect(x, y, 7, 46, fill=c, stroke="none", rx=3)
        s.text(x + 22, y + 28, f"{i+1}. {t}", size=11.5, weight="700", fill=c, anchor="start",
               maxpx=200)
        s.text(x + 236, y + 28, d, size=9.6, fill=MUTED, anchor="start", maxpx=390)
    s.rect(740, 120, 210, 470, fill=PANEL, stroke=LINE, rx=12)
    s.text(845, 148, "WHEN IN DOUBT", size=10.5, weight="700", fill=SLATE, spacing=1)
    qs = ["Is the client safe?",
          "Would I be comfortable if this were published?",
          "Whose needs am I meeting?",
          "Have I documented it?",
          "Is this within my competence?",
          "Have I told the client what I am doing?"]
    y = 184
    for q in qs:
        s.wrap(845, y, "• " + q, 20, 10, fill=INK, leading=14, max_lines=3)
        y += 52
    s.note(40, 606, 900,
           "The most common real-world dilemmas in MFT are not dramatic: a dual relationship through "
           "church or family ties, a request to keep a secret from a spouse, an insurance form that "
           "does not fit the work, and a client who cannot pay. Each has a documented, defensible path.",
           size=11)
    return s


def fig34():
    s = SVG(980, 620, "Cultural Assessment: The ADDRESSING Framework (Hays)",
            "Culture is not a category you tick; it is a set of positions with power attached")
    items = [
        ("A", "Age & generational", "Who is young, who is elder, who must not be corrected?"),
        ("D", "Developmental / disability", "Visible and invisible; access needs; stigma"),
        ("D", "Disability acquired", "Onset, meaning, family role changes"),
        ("R", "Religion & spirituality", "Practice, obligation, authority, coping"),
        ("E", "Ethnic & racial identity", "Majority/minority status; discrimination history"),
        ("S", "Socioeconomic status", "Income, class, education, job security"),
        ("S", "Sexual orientation", "Disclosure, safety, family acceptance"),
        ("I", "Indigenous heritage", "Land, language, custom, historical loss"),
        ("N", "National origin", "Migration, citizenship, language, accent"),
        ("G", "Gender", "Roles, expectations, decision-making power"),
    ]
    for i, (l, t, d) in enumerate(items):
        col, row = i % 2, i // 2
        x = 60 + col * 455
        y = 104 + row * 92
        s.rect(x, y, 435, 78, fill=WHITE, stroke="#dde4ec", rx=10)
        s.circle(x + 36, y + 39, 20, fill=TEAL, stroke="none")
        s.text(x + 36, y + 45, l, size=14, weight="700", fill=WHITE)
        s.text(x + 68, y + 30, t, size=12, weight="700", fill=INK, anchor="start")
        s.wrap(x + 68, y + 52, d, 58, 9.8, fill=MUTED, anchor="start", max_lines=2)
    s.note(40, 572, 900,
           "Use it as an interview, not a checklist: 'In your family, who usually decides? Who is "
           "consulted? What does your faith say about this problem? What language do you argue in?' "
           "Then ask yourself where YOU sit on each line and how that shapes what you notice.",
           size=11)
    return s


def fig35():
    s = SVG(980, 600, "The Speaker–Listener Technique",
            "A structured conversation that slows down a fight enough for both people to be heard")
    s.rect(60, 100, 400, 210, fill=TEAL_L, stroke="#c8e3dd", rx=12)
    s.text(260, 130, "SPEAKER", size=12, weight="700", fill=TEAL, spacing=1)
    rules = ["Use 'I' statements about your own experience",
             "Keep it to one issue and one paragraph",
             "Pause; ask the listener to paraphrase",
             "No blame, no mind-reading, no 'always'"]
    for i, r in enumerate(rules):
        s.text(84, 162 + i * 34, "• " + r, size=10.5, fill=INK, anchor="start")
    s.rect(520, 100, 400, 210, fill=BLUE_L, stroke="#c7d6f4", rx=12)
    s.text(720, 130, "LISTENER", size=12, weight="700", fill=BLUE, spacing=1)
    rules2 = ["Paraphrase what you heard, without editing",
              "Check: 'Did I get that right?'",
              "No rebuttal, no advice, no face-pulling",
              "Ask one curious question, then swap"]
    for i, r in enumerate(rules2):
        s.text(544, 162 + i * 34, "• " + r, size=10.5, fill=INK, anchor="start")
    s.rect(400, 330, 180, 60, fill=AMBER, stroke="none", rx=10)
    s.text(490, 356, "THE FLOOR CARD", size=11, weight="700", fill=WHITE, spacing=0.8)
    s.text(490, 374, "whoever holds it speaks", size=9.5, fill="#fdf3e3")
    s.arrow(430, 316, 300, 314, color=AMBER, sw=1.6)
    s.arrow(550, 316, 680, 314, color=AMBER, sw=1.6)
    s.rect(60, 416, 860, 120, fill=PANEL, stroke=LINE, rx=12)
    s.text(86, 444, "WHY IT WORKS", size=11, weight="700", fill=SLATE, anchor="start", spacing=0.8)
    why = [
        ("Slows arousal", "paraphrasing forces a pause in the escalation cycle"),
        ("Interrupts punctuation", "each partner hears their own words returned"),
        ("Builds accuracy", "misattribution is corrected in real time"),
    ]
    for i, (a, b) in enumerate(why):
        x = 86 + i * 285
        s.text(x, 474, a, size=11, weight="700", fill=TEAL, anchor="start")
        s.wrap(x, 494, b, 40, 9.8, fill=MUTED, anchor="start", max_lines=2)
    s.note(40, 552, 900,
           "Assign it as homework with a 15-minute timer and one agreed topic. Expect it to feel "
           "artificial — that is the point; the structure is doing the regulating that the couple "
           "cannot yet do alone.", size=11)
    return s


def fig36():
    s = SVG(980, 660, "Eight Domains of Couple Intimacy",
            "Sex is one spoke, not the wheel; couples often argue about the spoke when the wheel is broken")
    cx, cy, R = 490, 350, 200
    s.circle(cx, cy, 74, fill=SLATE, stroke="none")
    s.text(cx, cy - 10, "Intimacy", size=15, weight="700", fill=WHITE)
    s.text(cx, cy + 14, "is plural", size=12, fill="#cbd5e1")
    doms = [
        ("Emotional", "being known and accepted", TEAL),
        ("Physical", "touch, affection, proximity", BLUE),
        ("Sexual", "desire, pleasure, consent", ROSE),
        ("Intellectual", "ideas, curiosity, play", PLUM),
        ("Spiritual", "shared meaning, prayer, values", GREEN),
        ("Social", "friends, family, community", AMBER),
        ("Recreational", "fun, adventure, rest", "#0891b2"),
        ("Financial", "money, security, decisions", "#7c2d12"),
    ]
    for i, (t, d, c) in enumerate(doms):
        ang = -math.pi / 2 + i * (2 * math.pi / 8)
        x, y = cx + (R + 10) * math.cos(ang), cy + (R + 10) * math.sin(ang)
        s.line(cx + 78 * math.cos(ang), cy + 78 * math.sin(ang),
               x - 62 * math.cos(ang), y - 30 * math.sin(ang), stroke=c, sw=2)
        s.rect(x - 88, y - 30, 176, 60, fill=WHITE, stroke=c, rx=10)
        s.text(x, y - 8, t, size=11.5, weight="700", fill=c)
        s.text(x, y + 12, d, size=9.5, fill=MUTED)
    s.note(40, 588, 900,
           "Assessment question: 'On a scale of 0–10, how satisfied are you with each of these eight?' "
           "Plot both partners' scores. Discrepancy is information, not betrayal — and the lowest "
           "spoke is rarely the one the couple complains about.", size=11)
    return s


def fig37():
    s = SVG(980, 600, "Therapist Self-Care: Eight Domains and a Weekly Audit",
            "Burnout is an occupational hazard of empathic work, not a personal failing")
    doms = [
        ("Physical", "sleep, movement, food, medical care", 3, TEAL),
        ("Emotional", "naming feelings, therapy, journaling", 2, ROSE),
        ("Social", "friends who are not clients", 3, BLUE),
        ("Cognitive", "boundaries on information, curiosity", 2, PLUM),
        ("Spiritual", "prayer, meditation, meaning, rest", 3, GREEN),
        ("Professional", "supervision, CPD, caseload limits", 2, AMBER),
        ("Financial", "fee policy, savings, debt plan", 1, "#7c2d12"),
        ("Environmental", "workspace, light, commute, safety", 3, "#0891b2"),
    ]
    for i, (t, d, level, c) in enumerate(doms):
        col, row = i % 2, i // 2
        x = 60 + col * 450
        y = 96 + row * 108
        s.rect(x, y, 430, 90, fill=WHITE, stroke="#dde4ec", rx=10)
        s.text(x + 20, y + 26, t, size=12, weight="700", fill=c, anchor="start")
        s.text(x + 20, y + 46, d, size=9.8, fill=MUTED, anchor="start")
        for b in range(5):
            fillc = c if b < level else "#e8edf3"
            s.rect(x + 20 + b * 48, y + 60, 40, 14, fill=fillc, stroke="none", rx=4)
        s.text(x + 260, y + 72, f"{level}/5 this week", size=9, fill=MUTED, anchor="start")
    s.rect(60, 540, 860, 40, fill=AMBER_L, stroke="#f0d9b5", rx=8)
    s.text(490, 566, "Warning signs: cynicism, dread before sessions, boundary erosion, "
                     "resentment of clients, 'I am the only one who can help'.", size=10.5, fill=AMBER)
    return s


def fig38():
    s = SVG(980, 620, "What Actually Accounts for Change? The Common-Factors View",
            "Wampold's approximate estimates — contested in detail, robust in direction")
    _pie(s, 290, 320, 165, [0.40, 0.30, 0.15, 0.15], ["#94a3b8", TEAL, AMBER, PLUM])
    s.circle(290, 320, 62, fill=WHITE, stroke=LINE)
    s.text(290, 314, "change", size=12, weight="700", fill=SLATE)
    s.text(290, 334, "in therapy", size=10, fill=MUTED)
    legend = [
        ("Extratherapeutic factors (client, context, events) — ~40%", "#94a3b8"),
        ("Alliance, empathy, goals and agreement — ~30%", TEAL),
        ("Expectancy, hope, placebo response — ~15%", AMBER),
        ("Specific model or technique — ~15%", PLUM),
    ]
    y = 170
    for label, c in legend:
        s.rect(560, y - 14, 16, 16, fill=c, stroke="none", rx=4)
        s.wrap(586, y, label, 40, 11, fill=INK, anchor="start", leading=16, max_lines=2)
        y += 58
    s.rect(560, 400, 380, 150, fill=TEAL_L, stroke="#c8e3dd", rx=12)
    s.text(586, 428, "IMPLICATION FOR A MASTER'S CLINICIAN", size=10, weight="700", fill=TEAL,
           anchor="start", spacing=0.6)
    s.wrap(586, 452, "Learn two or three models deeply rather than nine shallowly; invest in alliance "
                     "monitoring and rupture repair; expect the client's life to do a lot of the work.",
           44, 10.5, fill=INK, anchor="start", max_lines=4)
    s.note(40, 566, 900,
           "Critique to hold in mind: the percentages are illustrative, not measured constants, and "
           "the 'dodo bird' verdict (all bona fide therapies perform similarly) does not mean "
           "technique is irrelevant — it means technique without alliance is inert.", size=11)
    return s


def fig39():
    s = SVG(980, 640, "Marriage, Dissolution and the Law: A Nigerian Orientation Map",
            "Different marriage systems create different legal routes and different dilemmas for the therapist")
    s.rect(60, 96, 860, 118, fill=PANEL, stroke=LINE, rx=12)
    s.text(86, 122, "FOUR WAYS A MARRIAGE CAN EXIST", size=10.5, weight="700", fill=SLATE,
           anchor="start", spacing=0.8)
    types = [
        ("Statutory", "Marriage Act; one wife; court dissolution", TEAL),
        ("Customary", "bride price, kin consent; customary court", BLUE),
        ("Islamic", "four wives permitted; Sharia court in some states", GREEN),
        ("Cohabitation", "no legal marriage; limited statutory protection", AMBER),
    ]
    for i, (t, d, c) in enumerate(types):
        x = 86 + i * 210
        s.rect(x, 138, 196, 62, fill=WHITE, stroke=c, rx=8)
        s.text(x + 98, 160, t, size=11, weight="700", fill=c)
        s.wrap(x + 98, 178, d, 29, 8.8, fill=MUTED, max_lines=2, leading=12)
    s.text(490, 250, "when the marriage ends, four questions must be answered", size=11.5,
           fill=SLATE, italic=True)
    qs = [
        ("Children", "custody, access, maintenance, schooling, relocation", ROSE),
        ("Property", "title, contribution, customary vs statutory rights", PLUM),
        ("Maintenance", "spousal and child support; enforcement", AMBER),
        ("Status", "divorce, nullity, separation; religious and civil effects", TEAL),
    ]
    for i, (t, d, c) in enumerate(qs):
        x = 60 + i * 225
        s.rect(x, 272, 210, 100, fill=WHITE, stroke=c, rx=10)
        s.text(x + 105, 300, t, size=12, weight="700", fill=c)
        s.wrap(x + 105, 322, d, 26, 9.5, fill=MUTED, max_lines=3, leading=12)
    s.rect(60, 402, 860, 138, fill=WHITE, stroke=LINE, rx=12)
    s.text(86, 430, "THE THERAPIST'S POSITION", size=10.5, weight="700", fill=SLATE, anchor="start",
           spacing=0.8)
    notes = [
        ("Do", "explain the difference between therapy, mediation and legal advice; refer early; "
               "document risk; discuss what will be shared in court."),
        ("Do not", "give legal advice, draft agreements, or promise confidentiality you cannot keep "
                   "when a child is at risk or a subpoena arrives."),
        ("Watch", "power asymmetry, immigration status, economic dependence, threats, and any "
                  "pressure to reconcile 'for the family'."),
    ]
    y = 452
    for a, b in notes:
        s.text(86, y, a, size=10.5, weight="700", fill=TEAL, anchor="start")
        s.wrap(146, y, b, 88, 10, fill=MUTED, anchor="start", max_lines=2, leading=14)
        y += 32
    s.note(40, 558, 900,
           "This map is orientation, not legal authority: statutes, state practice and case law vary "
           "and change. Verify any specific question with a qualified lawyer in the relevant "
           "jurisdiction, and keep a referral list you have actually called.", size=11)
    return s


def fig40():
    s = SVG(980, 620, "Trauma-Informed Practice: The Four R's and Six Principles",
            "Trauma-informed is an organisational stance, not a technique you add to session two")
    four = [
        ("REALISE", "the widespread impact of trauma and the paths to recovery", TEAL),
        ("RECOGNISE", "the signs and symptoms in clients, families and staff", BLUE),
        ("RESPOND", "by integrating knowledge into policy, language and practice", GREEN),
        ("RESIST RE-TRAUMATISATION", "actively avoid practices that repeat the injury", ROSE),
    ]
    for i, (t, d, c) in enumerate(four):
        x = 45 + i * 228
        s.rect(x, 96, 212, 110, fill=WHITE, stroke=c, rx=12)
        s.rect(x, 96, 212, 6, fill=c, stroke="none", rx=3)
        s.text(x + 106, 128, t, size=10.5, weight="700", fill=c, spacing=0.5)
        s.wrap(x + 106, 152, d, 27, 9.5, fill=MUTED, max_lines=3, leading=13)
    s.text(490, 240, "SIX PRINCIPLES IN THE ROOM", size=11, weight="700", fill=SLATE, spacing=0.8)
    prin = [
        ("Safety", "predictable start and finish; explain the room; no surprises"),
        ("Trustworthiness", "do what you say; be on time; be honest about limits"),
        ("Peer support", "link to people who share the experience, not only professionals"),
        ("Collaboration", "shared power; the client helps set the agenda"),
        ("Empowerment", "build on strengths; offer choices at every step"),
        ("Cultural humility", "the family's meaning system is the treatment context"),
    ]
    for i, (t, d) in enumerate(prin):
        col, row = i % 2, i // 2
        x = 60 + col * 460
        y = 262 + row * 92
        s.rect(x, y, 440, 78, fill=PANEL, stroke="#dde4ec", rx=10)
        s.text(x + 20, y + 26, t, size=11.5, weight="700", fill=TEAL, anchor="start")
        s.wrap(x + 20, y + 46, d, 62, 9.6, fill=INK, anchor="start", max_lines=2, leading=13)
    s.note(40, 560, 900,
           "Re-traumatisation traps to avoid: forcing a detailed narrative too early, using a "
           "restraint or closed door without explanation, disclosing confidential material in a "
           "joint session, and interpreting 'non-compliance' as character.", size=11)
    return s
