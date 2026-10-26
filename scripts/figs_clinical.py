"""Clinical model figures (12-27)."""
from figstyle import *
import math


def fig12():
    s = SVG(980, 640, "The EFT Cycle: Secondary Emotion Hides Primary Attachment Need",
            "Emotionally Focused Therapy (Sue Johnson) maps the loop beneath the argument")
    s.rect(40, 96, 400, 250, fill=ROSE_L, stroke="#f0c9d5", rx=14)
    s.text(240, 122, "PURSUER  (Aisha)", size=12.5, weight="700", fill=ROSE, spacing=0.8)
    s.text(240, 152, "Action tendency", size=10.5, fill=MUTED, italic=True)
    s.text(240, 174, "protest, criticise, chase", size=13, weight="600", fill=INK)
    s.text(240, 204, "Secondary emotion (on the surface)", size=10.5, fill=MUTED, italic=True)
    s.text(240, 226, "anger · frustration · resentment", size=13, weight="600", fill=ROSE)
    s.text(240, 256, "Primary emotion (underneath)", size=10.5, fill=MUTED, italic=True)
    s.text(240, 278, "fear of abandonment · loneliness", size=13, weight="600", fill=PLUM)
    s.text(240, 312, "Attachment cry: 'Are you there for me?'", size=12, fill=SLATE, italic=True)
    s.rect(540, 96, 400, 250, fill=BLUE_L, stroke="#c7d6f4", rx=14)
    s.text(740, 122, "WITHDRAWER  (Sam)", size=12.5, weight="700", fill=BLUE, spacing=0.8)
    s.text(740, 152, "Action tendency", size=10.5, fill=MUTED, italic=True)
    s.text(740, 174, "shut down, avoid, go quiet", size=13, weight="600", fill=INK)
    s.text(740, 204, "Secondary emotion (on the surface)", size=10.5, fill=MUTED, italic=True)
    s.text(740, 226, "numbness · irritation · distance", size=13, weight="600", fill=BLUE)
    s.text(740, 256, "Primary emotion (underneath)", size=10.5, fill=MUTED, italic=True)
    s.text(740, 278, "shame · fear of failure · helplessness", size=13, weight="600", fill=PLUM)
    s.text(740, 312, "Attachment cry: 'I can never get it right.'", size=12, fill=SLATE, italic=True)
    # loop arrows
    s.arrow(300, 366, 620, 430, color=ROSE, sw=2.6)
    s.text(410, 388, "pursue to get a response", size=11.5, fill=ROSE, weight="600")
    s.arrow(700, 470, 360, 512, color=BLUE, sw=2.6)
    s.text(540, 500, "withdraw to keep the peace", size=11.5, fill=BLUE, weight="600")
    s.rect(230, 520, 520, 86, fill=SLATE, stroke="none", rx=14)
    s.text(490, 548, "THE NEGATIVE CYCLE IS THE ENEMY — NOT YOUR PARTNER", size=14,
           weight="700", fill=WHITE, spacing=0.6)
    s.text(490, 574, "EFT moves: de-escalate → restructure the bond → consolidate", size=11.5,
           fill="#cbd5e1")
    s.note(40, 620, 900,
           "In session you do not argue with the anger. You slow the film: 'When she sounds angry, "
           "what happens inside you?' — and then, to the other: 'Can you hear that he disappears "
           "because he is afraid of failing you?'", size=12)
    return s


def fig13():
    s = SVG(980, 680, "The Sound Relationship House (Gottman)",
            "Seven storeys supported by two pillars: trust and commitment")
    levels = [
        ("Create shared meaning", "rituals, roles, goals, symbols", PLUM),
        ("Make life dreams come true", "honour each other's aspirations", AMBER),
        ("Manage conflict", "dialogue, repair, compromise, 'two yeses'", ROSE),
        ("The positive perspective", "positive sentiment override", GREEN),
        ("Turn towards", "bids, small moments, emotional bank account", TEAL),
        ("Share fondness and admiration", "express respect out loud", BLUE),
        ("Build love maps", "know each other's inner world", SLATE),
    ]
    y = 116
    for i, (t, sub, c) in enumerate(levels):
        s.rect(230, y, 520, 62, fill=WHITE, stroke=c, rx=8)
        s.rect(230, y, 8, 62, fill=c, stroke="none", rx=4)
        s.text(258, y + 26, t, size=13.5, weight="700", fill=c, anchor="start")
        s.text(258, y + 47, sub, size=11, fill=MUTED, anchor="start")
        y += 68
    # roof
    s.path("M 210 112 L 490 66 L 770 112", stroke=SLATE, sw=3, fill="none")
    # pillars
    s.rect(150, 116, 52, 466, fill=TEAL_L, stroke=TEAL, rx=8)
    s.text(176, 360, "T", size=22, weight="700", fill=TEAL)
    s.rect(778, 116, 52, 466, fill=TEAL_L, stroke=TEAL, rx=8)
    s.text(804, 360, "C", size=22, weight="700", fill=TEAL)
    s.text(176, 600, "Trust", size=12, weight="600", fill=TEAL)
    s.text(804, 600, "Commitment", size=12, weight="600", fill=TEAL)
    s.text(490, 612, "friendship is the foundation of romance", size=11, fill=MUTED, italic=True)
    s.text(490, 634, "5:1 positive-to-negative interaction ratio during conflict (the 'magic ratio')",
           size=11.5, fill=SLATE, weight="600", maxpx=880)
    s.note(40, 656, 900,
           "Adaptation caution: Gottman's norms were derived largely from U.S. samples. Use the "
           "structure of the house as a clinical map; do not treat the 5:1 ratio as a universal law.",
           size=12)
    return s


def fig14():
    s = SVG(980, 580, "The Four Horsemen and Their Antidotes",
            "Noticing the horseman is the skill; the antidote is the intervention")
    pairs = [
        ("Criticism", "Attacking the person, not the behaviour", "\"You always leave the place a mess.\"",
         "Gentle start-up", "\"I feel overwhelmed at 8 p.m. when the kitchen is full. Could we reset after dinner?\"", ROSE),
        ("Contempt", "Mockery, eye-rolls, name-calling, superiority", "\"You're hopeless, just like your father.\"",
         "Build a culture of appreciation", "Name one specific thing done well this week — out loud, daily.", PLUM),
        ("Defensiveness", "Counter-attack or innocent victim stance", "\"Me? You're the one who never listens.\"",
         "Accept some responsibility", "\"I did forget. That's on me. Let me fix it now.\"", AMBER),
        ("Stonewalling", "Shutting down, going blank, leaving", "Silence, phone scrolling, walking out.",
         "Self-soothe and return", "\"I'm flooded. I need 30 minutes, then I'll come back to this.\"", BLUE),
    ]
    y = 106
    for name, desc, ex, anti, anti_ex, c in pairs:
        s.rect(40, y, 445, 104, fill=WHITE, stroke=c, rx=10)
        s.rect(495, y, 445, 104, fill=GREEN_L, stroke="#bcdcc6", rx=10)
        s.text(60, y + 26, name.upper(), size=12, weight="700", fill=c, anchor="start", spacing=1)
        s.text(60, y + 48, desc, size=11, fill=MUTED, anchor="start")
        s.text(60, y + 70, ex, size=11.5, fill=INK, anchor="start", italic=True)
        s.text(60, y + 90, "secondary emotion on display", size=10, fill=MUTED, anchor="start")
        s.text(515, y + 26, "ANTIDOTE: " + anti.upper(), size=11.5, weight="700", fill=GREEN,
               anchor="start", spacing=0.6, maxpx=406)
        s.wrap(515, y + 52, anti_ex, size=11, fill=INK, anchor="start", wpx=406,
               italic=True, max_lines=2)
        s.text(515, y + 90, "name the primary need, then make one request", size=10, fill=MUTED,
               anchor="start")
        y += 114
    s.note(40, 552, 900,
           "Frequency matters more than intensity: contempt is the single strongest predictor of "
           "relationship dissolution in Gottman's longitudinal work, and it is also the horseman most "
           "treatable — because it lives in tone, not in facts.", size=11.5)
    return s


def fig15():
    s = SVG(980, 600, "Solution-Focused Brief Therapy: The Session in Five Moves",
            "Assume competence; study the exceptions; keep the next step small")
    steps = [
        ("1", "Listen for strengths", "What is already working? Who in the family has kept this from being worse?"),
        ("2", "The miracle question", "\"Suppose tonight, while you sleep, a miracle happens and the problem is solved. What will you notice first tomorrow?\""),
        ("3", "Scale the present", "\"On 0–10, where are you today? What would move you one point up — not to 10?\""),
        ("4", "Explore exceptions", "Tell me about a time the argument stayed small. What were you each doing differently?"),
        ("5", "End with a task", "Notice and repeat what worked. Invite the family to do more of it before the next session."),
    ]
    y = 108
    for n, t, body in steps:
        s.rect(60, y, 860, 86, fill=WHITE, stroke=LINE, rx=10)
        s.circle(104, y + 43, 20, fill=TEAL, stroke="none")
        s.text(104, y + 49, n, size=15, weight="700", fill=WHITE)
        s.text(140, y + 34, t, size=14, weight="700", fill=TEAL, anchor="start")
        s.wrap(140, y + 58, body, width=88, size=11.5, fill=MUTED, anchor="start", max_lines=2)
        y += 94
    s.note(40, 570, 900,
           "Nigerian clinical note: the miracle question can feel counter-cultural to families who "
           "expect expert direction. Follow it with a very concrete 'one small step' so the family "
           "leaves with something to do, not just something to imagine.", size=11.5)
    return s


def fig16():
    s = SVG(980, 560, "Narrative Therapy: Externalising the Problem, Re-authoring the Story",
            "The person is never the problem; the problem is the problem")
    s.rect(40, 100, 210, 300, fill=ROSE_L, stroke="#f0c9d5", rx=12)
    s.text(145, 128, "PROBLEM-SATURATED", size=11, weight="700", fill=ROSE, spacing=0.8)
    s.text(145, 146, "STORY", size=11, weight="700", fill=ROSE, spacing=0.8)
    s.wrap(145, 180, "\"I am a bad mother.\"", 20, 12.5, fill=INK, italic=True)
    s.wrap(145, 214, "Thin description; the person is fused with the problem.", 20, 11.5, fill=MUTED)
    s.rect(280, 100, 210, 300, fill=AMBER_L, stroke="#f0d9b5", rx=12)
    s.text(385, 128, "EXTERNALISE", size=11, weight="700", fill=AMBER, spacing=1)
    s.wrap(385, 162, "\"When did 'the guilt' first arrive? What does it tell you to do?\"", 21, 12,
           fill=INK, italic=True)
    s.wrap(385, 230, "Name it. Map its influence. Separate identity from problem.", 21, 11.5, fill=MUTED)
    s.rect(520, 100, 200, 300, fill=TEAL_L, stroke="#c8e3dd", rx=12)
    s.text(620, 128, "UNIQUE OUTCOMES", size=11, weight="700", fill=TEAL, spacing=0.8)
    s.wrap(620, 162, "\"Tell me about a moment the guilt was quieter — what were you doing?\"", 21, 12,
           fill=INK, italic=True)
    s.wrap(620, 234, "Find exceptions the dominant story cannot explain.", 21, 11.5, fill=MUTED)
    s.rect(750, 100, 190, 300, fill=PLUM_L, stroke="#ddd0f7", rx=12)
    s.text(845, 128, "RE-AUTHOR", size=11, weight="700", fill=PLUM, spacing=0.8)
    s.wrap(845, 162, "\"Who would recognise this version of you? What would they name it?\"", 21, 12,
           fill=INK, italic=True)
    s.wrap(845, 240, "Thicken the preferred story; recruit an audience.", 21, 11.5, fill=MUTED)
    for x in (250, 490, 720):
        s.arrow(x, 250, x + 28, 250, color=SLATE, sw=2)
    s.text(490, 440, "Therapy is a re-writing, not a repair: the family leaves with a story it can live in.",
           size=12.5, fill=SLATE, italic=True)
    s.note(40, 470, 900,
           "Practical: write the externalised name on a card and put it on the table between you. "
           "Ask the family to speak to the problem, not to each other, and to describe its tactics, "
           "size, and times of day. Children often join this immediately.", size=11.5)
    return s


def fig17():
    s = SVG(980, 640, "Adult Attachment: Two Dimensions, Four Patterns",
            "Anxiety about abandonment and avoidance of closeness combine into recognisable strategies")
    # axes
    x0, y0, w, h = 250, 130, 480, 400
    s.rect(x0, y0, w, h, fill=PANEL, stroke=LINE, rx=10)
    s.line(x0 + w / 2, y0, x0 + w / 2, y0 + h, stroke="#b8c4d2", sw=1.4)
    s.line(x0, y0 + h / 2, x0 + w, y0 + h / 2, stroke="#b8c4d2", sw=1.4)
    s.text(x0 + w / 2, y0 + h + 34, "AVOIDANCE OF INTIMACY  →", size=11.5, weight="700", fill=MUTED)
    s.text(x0 - 34, y0 + h / 2, "ANXIETY", size=11.5, weight="700", fill=MUTED, anchor="middle")
    s.text(x0 - 34, y0 + h / 2 - 100, "high", size=10, fill=MUTED)
    s.text(x0 - 34, y0 + h / 2 + 104, "low", size=10, fill=MUTED)
    quads = [
        (x0 + w * 0.26, y0 + h * 0.24, "SECURE", "comfortable with closeness\nand with separateness",
         "I am worthy; others are reliable.", GREEN),
        (x0 + w * 0.74, y0 + h * 0.24, "DISMISSIVE-AVOIDANT", "compulsively self-reliant;\nminimises need",
         "Closeness is unsafe; I need no one.", BLUE),
        (x0 + w * 0.24, y0 + h * 0.74, "ANXIOUS-PREOCCUPIED", "hypervigilant to withdrawal;\nclinging or protesting",
         "I must hold on or I will be left.", ROSE),
        (x0 + w * 0.76, y0 + h * 0.74, "FEARFUL-AVOIDANT", "wants closeness and fears it;\napproach–avoidance",
         "I need you and you are dangerous.", PLUM),
    ]
    for x, y, name, desc, belief, c in quads:
        s.rect(x - 100, y - 44, 200, 96, fill=WHITE, stroke=c, rx=12)
        s.text(x, y - 18, name, size=11, weight="700", fill=c)
        for j, ln in enumerate(desc.split("\n")):
            s.text(x, y + 2 + j * 15, ln, size=10, fill=MUTED)
        s.text(x, y + 42, belief, size=9.5, fill=c, italic=True)
    s.note(40, 596, 900,
           "Attachment is a pattern, not a personality type. The same person can be secure with a "
           "sibling and anxious with a partner, and patterns shift with context, therapy and a "
           "safe relationship. Assess the pattern, then ask what it protects.", size=11.5)
    return s


def fig18():
    s = SVG(980, 600, "The Window of Tolerance",
            "Trauma narrows the band in which a person can think, feel and stay relational")
    s.rect(70, 110, 620, 130, fill=ROSE_L, stroke="#f0c9d5", rx=10)
    s.text(96, 140, "HYPERAROUSAL", size=13, weight="700", fill=ROSE, anchor="start", spacing=0.8)
    s.text(96, 166, "fight / flight: panic, rage, hypervigilance, intrusive images, restlessness",
           size=11.5, fill=MUTED, anchor="start")
    s.rect(70, 240, 620, 160, fill=GREEN_L, stroke="#bcdcc6", rx=10)
    s.text(96, 272, "WINDOW OF TOLERANCE", size=13, weight="700", fill=GREEN, anchor="start", spacing=0.8)
    s.text(96, 298, "regulated: can think, feel, choose, connect, learn", size=11.5, fill=MUTED,
           anchor="start")
    s.rect(70, 400, 620, 130, fill=BLUE_L, stroke="#c7d6f4", rx=10)
    s.text(96, 430, "HYPOAROUSAL", size=13, weight="700", fill=BLUE, anchor="start", spacing=0.8)
    s.text(96, 456, "freeze / collapse: numbness, dissociation, shutdown, shame, exhaustion",
           size=11.5, fill=MUTED, anchor="start")
    # arrow band narrowing
    s.path("M 730 130 C 700 240, 700 400, 730 510", stroke=SLATE, sw=2, fill="none", dash="5 4")
    s.text(790, 300, "Trauma and chronic stress", size=12, weight="600", fill=SLATE)
    s.text(790, 322, "narrow the window", size=12, fill=MUTED)
    s.arrow(770, 360, 700, 330, color=SLATE, sw=1.5)
    s.text(790, 380, "Safety, co-regulation and", size=11.5, fill=MUTED)
    s.text(790, 400, "skills widen it again", size=11.5, fill=MUTED)
    s.arrow(770, 424, 700, 400, color=GREEN, sw=1.5)
    s.note(40, 552, 900,
           "In-session signal: watch for breath-holding, flushing, freezing, gaze change or sudden "
           "compliance. Those are not 'resistance' — they are the nervous system leaving the room. "
           "Slow down, orient to the present, and offer choice.", size=11.5)
    return s


def fig19():
    s = SVG(980, 620, "The Polyvagal Ladder (Porges)",
            "Three survival states, each with its own felt sense and social signal")
    rungs = [
        ("VENTRAL VAGAL", "SAFE & SOCIAL", "calm, curious, connected, flexible",
         "warm voice, open posture, eye contact", GREEN, 0),
        ("SYMPATHETIC", "MOBILISED", "anxious, angry, panicked, driven",
         "fast speech, agitation, urgency", AMBER, 1),
        ("DORSAL VAGAL", "SHUT DOWN", "numb, flat, hopeless, dissociated",
         "low voice, still face, collapse", BLUE, 2),
    ]
    y = 120
    for name, state, felt, cue, c, i in rungs:
        indent = i * 70
        s.rect(90 + indent, y, 640 - indent, 118, fill=WHITE, stroke=c, rx=10)
        s.rect(90 + indent, y, 7, 118, fill=c, stroke="none", rx=3)
        s.text(116 + indent, y + 30, name, size=12.5, weight="700", fill=c, anchor="start", spacing=0.8)
        s.text(116 + indent, y + 52, state, size=11, fill=MUTED, anchor="start", spacing=1)
        s.text(116 + indent, y + 78, felt, size=12, fill=INK, anchor="start")
        s.text(116 + indent, y + 100, "cues: " + cue, size=10.5, fill=MUTED, anchor="start")
        y += 136
    s.arrow(830, 470, 830, 150, color=GREEN, sw=2.4)
    s.text(785, 300, "co-regulation", size=10.5, weight="600", fill=GREEN)
    s.text(785, 316, "moves you up", size=10.5, weight="600", fill=GREEN)
    s.text(918, 288, "SAFETY", size=10, weight="700", fill=GREEN, anchor="start")
    s.text(918, 306, "is the", size=9.5, fill=MUTED, anchor="start")
    s.text(918, 322, "intervention", size=9.5, fill=MUTED, anchor="start")
    s.note(40, 560, 900,
           "Clinically: the ladder is not a hierarchy of worth. A 'shut down' adolescent is not lazy; "
           "a 'mobilised' parent is not abusive by nature. Ask 'what did your body do to keep you "
           "safe?' before asking 'what should you do differently?'", size=11.5)
    return s


def fig20():
    s = SVG(980, 660, "The Stress Response: HPA Axis and the Family",
            "Chronic family conflict is a physiological dose, not only an emotional experience")
    s.card(90, 130, 200, 96, "HYPOTHALAMUS", ["detects threat,", "releases CRH"], fill=TEAL_L,
           stroke=TEAL, tcolor=TEAL, tsize=13, bsize=11)
    s.card(390, 110, 200, 96, "PITUITARY", ["releases ACTH into", "the bloodstream"], fill=BLUE_L,
           stroke=BLUE, tcolor=BLUE, tsize=13, bsize=11)
    s.card(700, 130, 200, 96, "ADRENAL GLANDS", ["cortisol + adrenaline", "into circulation"],
           fill=AMBER_L, stroke=AMBER, tcolor=AMBER, tsize=13, bsize=11)
    s.arrow(292, 178, 388, 158, color=TEAL, sw=2, label="CRH", loff=(-4, -18))
    s.arrow(592, 158, 698, 178, color=BLUE, sw=2, label="ACTH", loff=(4, -18))
    # target organs
    targets = [("heart rate and blood pressure \u2191", "palpitations, tension"),
               ("sleep \u2193", "night waking, early rising"),
               ("digestion \u2193", "nausea, appetite change"),
               ("immune function \u2193", "colds, slow healing")]
    for i, (t, d) in enumerate(targets):
        x = 62 + i * 218
        s.rect(x, 288, 196, 76, fill=WHITE, stroke=AMBER, rx=10)
        s.text(x + 98, 312, t, size=10.5, weight="600", fill=AMBER, maxpx=176)
        s.text(x + 98, 332, d, size=9.5, fill=MUTED, maxpx=176)
        s.line(300 + i * 200, 228, x + 98, 286, stroke=AMBER, sw=1.1, dash="3 3")
    # feedback loop
    s.path("M 160 286 C 120 330, 120 250, 150 228", stroke=ROSE, sw=1.8, fill="none", dash="6 4")
    s.text(490, 404, "negative feedback: cortisol signals the brain to switch the response off — "
                     "unless the threat keeps returning", size=10.5, fill=ROSE)
    # chronic stress panel
    s.rect(60, 424, 860, 140, fill=PANEL, stroke=LINE, rx=12)
    s.text(84, 452, "WHEN THE STRESSOR IS THE RELATIONSHIP ITSELF", size=11, weight="700",
           fill=SLATE, anchor="start", spacing=0.8)
    items = [("Allostatic load", "the system never fully powers down"),
             ("Sensitised amygdala", "smaller triggers, bigger reactions"),
             ("Weaker prefrontal control", "harder to inhibit the sharp reply"),
             ("Child cortisol patterns", "linked to anxiety and sleep problems")]
    for i, (a, b) in enumerate(items):
        x = 84 + (i % 2) * 425
        yy = 482 + (i // 2) * 42
        s.text(x, yy, a, size=10.5, weight="700", fill=TEAL, anchor="start")
        s.text(x + 168, yy, b, size=9.8, fill=MUTED, anchor="start", maxpx=230)
    s.note(40, 586, 900,
           "This is why 'just calm down' fails: the body is running a script that predates the "
           "argument. Regulate first (breath, movement, safety), then reason. Couple sessions that "
           "begin with 90 seconds of paced breathing look visibly different.", size=11)
    return s


def fig21():
    s = SVG(980, 640, "The Social Brain: Where Connection Hurts and Heals",
            "A simplified lateral schematic — the labels name functions, not precise anatomy")
    s.ellipse(500, 330, 205, 180, fill="#f7f2ea", stroke="#d8cbb8", sw=2)
    s.path("M 380 175 C 300 185 265 240 272 305 C 278 355 315 385 360 392 "
           "C 382 428 448 434 480 406 C 540 416 596 380 600 332 "
           "C 604 285 572 248 540 236 C 516 193 448 166 380 175 Z",
           fill="#fdf6ee", stroke="#c9b49a", sw=2)
    s.path("M 380 175 C 320 182 268 228 268 296 C 296 276 336 262 380 264 Z",
           fill=TEAL_L, stroke=TEAL, sw=1.4)
    s.text(322, 246, "PFC", size=11.5, weight="700", fill=TEAL)
    s.circle(432, 344, 24, fill=ROSE, stroke="none")
    s.text(432, 349, "Amy", size=9.5, weight="700", fill=WHITE)
    s.ellipse(498, 344, 38, 17, fill=PLUM_L, stroke=PLUM, sw=1.4)
    s.text(498, 348, "hippocampus", size=8.5, fill=PLUM)
    s.ellipse(392, 276, 34, 24, fill=AMBER_L, stroke=AMBER, sw=1.4)
    s.text(392, 281, "insula", size=9, fill=AMBER)
    s.ellipse(366, 310, 26, 13, fill=BLUE_L, stroke=BLUE, sw=1.4)
    s.text(366, 314, "ACC", size=8.5, fill=BLUE)
    s.circle(566, 404, 40, fill="#efe6da", stroke="#c9b49a")
    s.text(566, 409, "cerebellum", size=8.5, fill=MUTED)
    s.rect(520, 396, 24, 86, fill="#efe6da", stroke="#c9b49a", rx=6)

    labels = [
        (322, 246, "Prefrontal cortex", "perspective-taking, inhibition, reappraisal",
         252, 140, "end", TEAL),
        (392, 276, "Insula", "visceral feeling; the 'gut sense' of another person",
         720, 150, "start", AMBER),
        (366, 310, "Anterior cingulate", "social pain and exclusion; fires like physical pain",
         720, 246, "start", BLUE),
        (432, 344, "Amygdala", "fast, pre-verbal threat detection",
         720, 342, "start", ROSE),
        (498, 344, "Hippocampus", "context and memory; shrinks under chronic stress",
         720, 438, "start", PLUM),
    ]
    for x, y, name, desc, tx, ty, anchor, c in labels:
        lx = tx + 6 if anchor == "end" else tx - 6
        s.line(x, y, lx, ty - 4, stroke=c, sw=1.1, dash="3 3")
        s.text(tx, ty, name, size=11, weight="700", fill=c, anchor=anchor)
        s.wrap(tx, ty + 17, desc, size=9.5, fill=MUTED, anchor=anchor,
               wpx=240 if anchor == "start" else 230, max_lines=2, leading=13)
    s.note(40, 512, 900,
           "Translation into practice: rejection activates pain circuitry (Eisenberger's social-pain "
           "findings), which is why contempt lands physically. A stressed hippocampus also files the "
           "argument as a general rule rather than a single event — so reframing is not politeness, "
           "it changes what gets encoded.", size=11)
    return s


def fig22():
    s = SVG(980, 560, "The Dual-Process Model of Grieving (Stroebe & Schut)",
            "Healthy grieving oscillates between loss and restoration; neither track is 'the right one'")
    s.rect(60, 100, 860, 300, fill=WHITE, stroke=LINE, rx=12)
    # tracks
    s.line(100, 170, 880, 170, stroke=ROSE, sw=1.2, dash="4 4")
    s.line(100, 330, 880, 330, stroke=TEAL, sw=1.2, dash="4 4")
    s.text(110, 158, "LOSS-ORIENTED", size=11, weight="700", fill=ROSE, anchor="start", spacing=0.8)
    s.text(110, 350, "RESTORATION-ORIENTED", size=11, weight="700", fill=TEAL, anchor="start", spacing=0.8)
    s.text(120, 200, "grief work, crying, yearning,", size=10.5, fill=MUTED, anchor="start")
    s.text(120, 216, "reviewing the relationship", size=10.5, fill=MUTED, anchor="start")
    s.text(120, 380, "new roles, routines, identity,", size=10.5, fill=MUTED, anchor="start")
    s.text(120, 396, "attending to life and the living", size=10.5, fill=MUTED, anchor="start")
    # oscillation
    pts = [(130, 300), (200, 175), (280, 320), (350, 185), (430, 330), (500, 180),
           (580, 315), (650, 180), (730, 330), (810, 190), (870, 300)]
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
    s.path(d, stroke=SLATE, sw=2.6, fill="none")
    s.text(490, 128, "oscillation: moving back and forth is the adaptive process", size=11,
           fill=SLATE, italic=True)
    s.text(490, 428, "time →", size=10.5, fill=MUTED)
    # stressors
    boxes = [
        ("Loss stressors", "anniversary, photographs, an empty chair at Eid", ROSE),
        ("Restoration stressors", "school run alone, finances, 'who am I now?'", TEAL),
        ("Overdose risk", "staying on one track too long: avoidance or endless immersion", AMBER),
    ]
    x = 60
    for t, b, c in boxes:
        s.rect(x, 440, 280, 86, fill=WHITE, stroke=c, rx=10)
        s.text(x + 16, 466, t, size=11.5, weight="700", fill=c, anchor="start")
        s.wrap(x + 16, 488, b, 42, 10.5, fill=MUTED, anchor="start", max_lines=2)
        x += 295
    s.note(40, 540, 900,
           "Cultural note: in many Nigerian families, mourning is collective and public, with "
           "prescribed rites. The dual-process lens is useful only if it respects those rites as "
           "restoration work rather than as 'avoidance'. Ask what the family's tradition requires.",
           size=11)
    return s


def fig23():
    s = SVG(980, 660, "Developmental Milestones Across Childhood",
            "A screening map — not a diagnostic instrument. Variation is normal; regression is a flag")
    ages = ["0–1", "1–3", "3–6", "6–11", "11–14", "14–18"]
    domains = [
        ("Physical", [TEAL, "sits, crawls, walks", "runs, climbs, feeds self",
                      "hops, draws, toilet trained", "refines motor skills",
                      "puberty begins", "growth spurt, sexual maturity"], 0),
        ("Cognitive", [BLUE, "object permanence", "symbolic play, words combine",
                       "magical thinking, theory of mind", "concrete operations",
                       "abstract reasoning begins", "hypothetical + moral reasoning"], 1),
        ("Language", [GREEN, "cooing, babbling", "first words, 2-word phrases",
                      "sentences, 1,000+ words", "reading, narrative",
                      "complex sentences, slang", "abstract, peer register"], 2),
        ("Social-emotional", [PLUM, "attachment, social smile", "self-recognition, tantrums",
                              "play with peers, initiative", "industry, rule-based play",
                              "identity, autonomy", "intimacy, independence"], 3),
    ]
    x0 = 150
    s.text(x0 - 18, 118, "AGE (years)", size=10, weight="700", fill=MUTED, anchor="end")
    for i, a in enumerate(ages):
        s.text(x0 + i * 136 + 62, 118, a, size=11, weight="700", fill=SLATE)
    s.line(x0, 130, x0 + 816, 130, stroke=LINE, sw=1.5)
    for name, row, r in domains:
        c = row[0]
        y = 150 + r * 116
        s.text(x0 - 18, y + 40, name, size=11, weight="700", fill=c, anchor="end")
        for i in range(6):
            s.rect(x0 + i * 136 + 4, y, 128, 82, fill=WHITE, stroke="#e2e8f0", rx=8)
            s.wrap(x0 + i * 136 + 68, y + 26, row[i + 1], 17, 9.8, fill=INK, max_lines=4)
    s.note(40, 620, 900,
           "Clinical use: milestone knowledge helps you distinguish a child's behaviour that is "
           "'age-appropriate and infuriating' from a developmental delay. Always ask about "
           "regression (loss of words, toileting, motor skills) — that is a referral trigger.", size=11)
    return s


def fig24():
    s = SVG(980, 640, "Play Therapy Room: A Practical Floor Plan",
            "A predictable room is a therapeutic instrument: same place, same rules, same limits")
    s.rect(70, 100, 840, 460, fill="#fbfcfd", stroke=SLATE, sw=2.2)
    # door
    s.rect(70, 400, 10, 90, fill=WHITE, stroke=WHITE)
    s.path("M 70 400 A 90 90 0 0 1 160 490", stroke=SLATE, sw=1.6, dash="4 3", fill="none")
    s.text(120, 520, "door", size=10, fill=MUTED)
    # furniture
    s.rect(120, 130, 200, 120, fill=AMBER_L, stroke=AMBER, rx=6)
    s.text(220, 178, "SAND TRAY", size=11, weight="700", fill=AMBER)
    s.text(220, 196, "wet + dry, miniatures", size=9.5, fill=MUTED)
    s.rect(360, 130, 160, 120, fill=PLUM_L, stroke=PLUM, rx=6)
    s.text(440, 172, "DOLLHOUSE", size=11, weight="700", fill=PLUM)
    s.text(440, 190, "& family figures", size=9.5, fill=MUTED)
    s.rect(560, 130, 160, 120, fill=TEAL_L, stroke=TEAL, rx=6)
    s.text(640, 172, "ART TABLE", size=11, weight="700", fill=TEAL)
    s.text(640, 190, "paper, crayons, clay", size=9.5, fill=MUTED)
    s.rect(750, 130, 120, 120, fill=BLUE_L, stroke=BLUE, rx=6)
    s.text(810, 172, "PUPPETS", size=11, weight="700", fill=BLUE)
    s.text(810, 190, "stage + basket", size=9.5, fill=MUTED)
    s.circle(190, 340, 58, fill=WHITE, stroke=GREEN, sw=1.6)
    s.text(190, 336, "BEAN BAGS", size=10, weight="700", fill=GREEN)
    s.text(190, 352, "circle time", size=9, fill=MUTED)
    s.rect(300, 300, 150, 90, fill=WHITE, stroke=SLATE, rx=6)
    s.text(375, 330, "CHILD CHAIR", size=9.5, weight="700", fill=SLATE)
    s.text(375, 346, "child height", size=9, fill=MUTED)
    s.rect(480, 300, 150, 90, fill=WHITE, stroke=SLATE, rx=6)
    s.text(555, 330, "THERAPIST CHAIR", size=9, weight="700", fill=SLATE)
    s.text(555, 346, "90° angle, not opposite", size=8.5, fill=MUTED)
    s.rect(660, 300, 200, 90, fill=GREEN_L, stroke=GREEN, rx=6)
    s.text(760, 330, "BOOKS & FEELINGS", size=10, weight="700", fill=GREEN)
    s.text(760, 346, "faces, stories, cards", size=9, fill=MUTED)
    s.rect(300, 420, 300, 100, fill=PANEL, stroke=LINE, rx=6, dash="5 4")
    s.text(450, 452, "OPEN FLOOR SPACE", size=10.5, weight="700", fill=MUTED)
    s.text(450, 470, "for role-play, movement,", size=9, fill=MUTED)
    s.text(450, 484, "and family sessions", size=9, fill=MUTED)
    s.rect(690, 430, 200, 100, fill=ROSE_L, stroke=ROSE, rx=6)
    s.text(790, 458, "STORAGE", size=10, weight="700", fill=ROSE)
    s.text(790, 476, "labelled boxes;", size=9, fill=MUTED)
    s.text(790, 490, "child can reach", size=9, fill=MUTED)
    # observation
    s.rect(860, 100, 40, 460, fill=SLATE_L, stroke=SLATE)
    s.text(880, 340, "mirror", size=9, fill=MUTED, anchor="middle")
    s.note(40, 588, 900,
           "Limit-setting script: 'You can be as angry as you want in here, and you may not hurt "
           "yourself, me, or the room.' State the limit, offer an acceptable alternative, and name "
           "the feeling. Consistency is the intervention.", size=11)
    return s


def fig25():
    s = SVG(980, 600, "Stages of Group Development and the Therapeutic Factors",
            "Groups change shape over time; your leadership must change with them")
    stages = [
        ("FORMING", "orientation, anxiety,\ndependence on leader", TEAL),
        ("STORMING", "conflict, roles contested,\nresistance", ROSE),
        ("NORMING", "cohesion, shared rules,\ntrust", AMBER),
        ("PERFORMING", "work, mutual aid,\nrisk-taking", GREEN),
        ("ADJOURNING", "separation, consolidation,\nforward plan", PLUM),
    ]
    x = 55
    for i, (n, d, c) in enumerate(stages):
        s.rect(x, 110, 168, 130, fill=WHITE, stroke=c, rx=12)
        s.rect(x, 110, 168, 6, fill=c, stroke="none", rx=3)
        s.text(x + 84, 140, n, size=11.5, weight="700", fill=c, spacing=0.8)
        for j, ln in enumerate(d.split("\n")):
            s.text(x + 84, 166 + j * 16, ln, size=10, fill=MUTED)
        if i < 4:
            s.arrow(x + 170, 175, x + 194, 175, color=SLATE, sw=1.8)
        x += 178
    s.rect(55, 268, 420, 280, fill=PANEL, stroke=LINE, rx=12)
    s.text(80, 296, "YALOM'S THERAPEUTIC FACTORS", size=11, weight="700", fill=SLATE,
           anchor="start", spacing=0.8)
    factors = ["Instillation of hope", "Universality", "Imparting information",
               "Altruism", "Corrective recapitulation", "Socialising techniques",
               "Imitative behaviour", "Interpersonal learning", "Group cohesiveness",
               "Catharsis", "Existential factors"]
    for i, f in enumerate(factors):
        col, row = i % 2, i // 2
        s.circle(84 + col * 205, 326 + row * 34, 4, fill=TEAL, stroke="none")
        s.text(96 + col * 205, 330 + row * 34, f, size=10.5, fill=INK, anchor="start")
    s.rect(495, 268, 430, 280, fill=WHITE, stroke=LINE, rx=12)
    s.text(520, 296, "WHAT THE LEADER DOES", size=11, weight="700", fill=SLATE, anchor="start",
           spacing=0.8)
    actions = [
        ("Forming", "structure, safety, names, purpose"),
        ("Storming", "stay steady; name the process"),
        ("Norming", "make the rules explicit"),
        ("Performing", "step back; let mutual aid work"),
        ("Adjourning", "review gains; plan for relapse"),
    ]
    for i, (a, b) in enumerate(actions):
        s.text(520, 330 + i * 42, a, size=11, weight="700", fill=TEAL, anchor="start")
        s.text(600, 330 + i * 42, b, size=10.5, fill=MUTED, anchor="start")
    s.note(40, 566, 900,
           "Open versus closed groups: closed groups build cohesion but lose members to attrition; "
           "open groups tolerate drop-out but must re-form repeatedly. Choose according to setting, "
           "not preference.", size=11)
    return s


def fig26():
    s = SVG(980, 620, "Crisis Intervention: Roberts' Seven-Stage Model",
            "The first task is always safety, not insight")
    stages = [
        ("1", "Assess lethality", "risk to self or others; means, plan, intent", ROSE),
        ("2", "Establish rapport", "calm, non-judgemental contact; 'I'm here with you'", AMBER),
        ("3", "Identify the problem", "the precipitating event and its meaning", TEAL),
        ("4", "Explore feelings", "name and normalise; allow the story", BLUE),
        ("5", "Generate alternatives", "options, not yet decisions", GREEN),
        ("6", "Implement a plan", "concrete, timed, written down", PLUM),
        ("7", "Follow up", "check adherence, revise, link to care", SLATE),
    ]
    for i, (n, t, d, c) in enumerate(stages):
        col, row = i % 2, i // 2
        x = 60 + col * 450
        y = 110 + row * 118
        s.rect(x, y, 420, 100, fill=WHITE, stroke=c, rx=10)
        s.circle(x + 40, y + 50, 20, fill=c, stroke="none")
        s.text(x + 40, y + 56, n, size=14, weight="700", fill=WHITE)
        s.text(x + 74, y + 40, t, size=13, weight="700", fill=c, anchor="start")
        s.wrap(x + 74, y + 64, d, 52, 10.5, fill=MUTED, anchor="start", max_lines=2)
    s.note(40, 500, 900,
           "Do not skip stage 1 to get to stage 3. A thorough lethality assessment (ideation, plan, "
           "intent, means, protective factors, previous attempts) is both a clinical and a legal "
           "duty. Document what you asked and what you did.", size=11.5)
    s.text(490, 566, "In family crises, sequence matters: stabilise the most vulnerable member first, "
                     "then convene the system.", size=11.5, fill=SLATE, italic=True)
    return s


def fig27():
    s = SVG(980, 620, "Addiction and the Family: The Maintenance Cycle",
            "Substance use is a family-organising behaviour, not a private habit")
    cx, cy, R = 470, 320, 175
    s.circle(cx, cy, R, fill=PANEL, stroke=LINE)
    nodes = [
        ("Use", "relief, ritual, escape", ROSE),
        ("Secrecy", "lies, hiding, double life", PLUM),
        ("Enabling", "covering, paying, excusing", AMBER),
        ("Crisis", "health, money, law, violence", ROSE),
        ("Shame", "blame, silence, isolation", BLUE),
        ("Promise", "'this is the last time'", TEAL),
    ]
    for i, (t, sub, c) in enumerate(nodes):
        ang = -math.pi / 2 + i * (2 * math.pi / 6)
        x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
        s.rect(x - 74, y - 32, 148, 64, fill=WHITE, stroke=c, rx=10)
        s.text(x, y - 6, t, size=12, weight="700", fill=c)
        s.text(x, y + 14, sub, size=9.5, fill=MUTED)
    for i in range(6):
        a1 = -math.pi / 2 + i * (2 * math.pi / 6) + 0.30
        a2 = a1 + 0.62
        s.arrow(cx + (R - 56) * math.cos(a1), cy + (R - 56) * math.sin(a1),
                cx + (R - 56) * math.cos(a2), cy + (R - 56) * math.sin(a2), color=MUTED, sw=1.4)
    s.circle(cx, cy, 66, fill=SLATE, stroke="none")
    s.text(cx, cy - 4, "The family", size=12.5, weight="700", fill=WHITE)
    s.text(cx, cy + 16, "adapts around it", size=10.5, fill="#cbd5e1")
    # roles
    s.rect(700, 96, 240, 440, fill=WHITE, stroke=LINE, rx=12)
    s.text(820, 124, "COMMON FAMILY ROLES", size=10.5, weight="700", fill=SLATE, spacing=0.8)
    roles = [("The enabler", "removes consequences"), ("The hero", "over-achieves, distracts"),
             ("The scapegoat", "carries the anger"), ("The lost child", "disappears quietly"),
             ("The mascot", "uses humour to defuse")]
    for i, (a, b) in enumerate(roles):
        y = 158 + i * 74
        s.text(720, y, a, size=11.5, weight="700", fill=TEAL, anchor="start")
        s.text(720, y + 18, b, size=10, fill=MUTED, anchor="start")
    s.note(40, 540, 900,
           "Evidence-informed options: motivational interviewing, CBT-based relapse prevention, "
           "family-inclusive approaches (e.g. behavioural couples therapy, CRAFT for concerned "
           "relatives), peer recovery support, and medication-assisted treatment where indicated. "
           "Confrontational 'interventions' have weak evidence and high drop-out.", size=11)
    return s
