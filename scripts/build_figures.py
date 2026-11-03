"""Generate every figure in assets/figures from the fig* modules."""
import importlib, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))

import figstyle, figs_theory, figs_clinical, figs_practice

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "figures")
os.makedirs(OUT, exist_ok=True)

CATALOGUE = [
    ("fig01", "two-cybernetics", figs_theory.fig01),
    ("fig02", "circular-causality", figs_theory.fig02),
    ("fig03", "genogram-symbols", figs_theory.fig03),
    ("fig04", "genogram-case", figs_theory.fig04),
    ("fig05", "structural-map", figs_theory.fig05),
    ("fig06", "bowen-concepts", figs_theory.fig06),
    ("fig07", "ecological-systems", figs_theory.fig07),
    ("fig08", "family-life-cycle", figs_theory.fig08),
    ("fig09", "stages-of-change", figs_theory.fig09),
    ("fig10", "feedback-loops", figs_theory.fig10),
    ("fig11", "communication-axioms", figs_theory.fig11),
    ("fig12", "eft-cycle", figs_clinical.fig12),
    ("fig13", "sound-relationship-house", figs_clinical.fig13),
    ("fig14", "four-horsemen", figs_clinical.fig14),
    ("fig15", "sfbt-moves", figs_clinical.fig15),
    ("fig16", "narrative-externalising", figs_clinical.fig16),
    ("fig17", "attachment-patterns", figs_clinical.fig17),
    ("fig18", "window-of-tolerance", figs_clinical.fig18),
    ("fig19", "polyvagal-ladder", figs_clinical.fig19),
    ("fig20", "hpa-axis", figs_clinical.fig20),
    ("fig21", "social-brain", figs_clinical.fig21),
    ("fig22", "dual-process-grief", figs_clinical.fig22),
    ("fig23", "developmental-milestones", figs_clinical.fig23),
    ("fig24", "playroom-plan", figs_clinical.fig24),
    ("fig25", "group-stages", figs_clinical.fig25),
    ("fig26", "crisis-stages", figs_clinical.fig26),
    ("fig27", "addiction-family-cycle", figs_clinical.fig27),
    ("fig28", "research-design-tree", figs_practice.fig28),
    ("fig29", "validity-reliability", figs_practice.fig29),
    ("fig30", "assessment-sequence", figs_practice.fig30),
    ("fig31", "five-p-formulation", figs_practice.fig31),
    ("fig32", "supervision-triangle", figs_practice.fig32),
    ("fig33", "ethics-decision-model", figs_practice.fig33),
    ("fig34", "addressing-framework", figs_practice.fig34),
    ("fig35", "speaker-listener", figs_practice.fig35),
    ("fig36", "intimacy-domains", figs_practice.fig36),
    ("fig37", "self-care-audit", figs_practice.fig37),
    ("fig38", "common-factors", figs_practice.fig38),
    ("fig39", "family-law-map", figs_practice.fig39),
    ("fig40", "trauma-informed", figs_practice.fig40),
]

if __name__ == "__main__":
    total = 0
    for fid, slug, fn in CATALOGUE:
        s = fn()
        p = os.path.join(OUT, f"{fid}-{slug}.svg")
        s.save(p)
        probs = s.lint()
        total += len(probs)
        if probs:
            print(f"\n[{fid}-{slug}] {len(probs)} problem(s)")
            for pr in probs[:12]:
                print("   ", pr)
        else:
            print(f"ok  {fid}-{slug}  ({s.w}x{s.h})")
    print(f"\n{total} layout problem(s) total")
