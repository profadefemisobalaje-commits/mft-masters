# The teaching-week template

Every teaching week in every course book is written to a single standard: **not less than 8,000 words of
week content**, delivered through the same thirteen components so a student always knows where to find
what. The checker (`scripts/check_week_lengths.py`) measures each week from its heading to the next `##`
heading, and fails the build if any week falls short.

| # | Component | Target words | Purpose |
|---|---|---|---|
| 1 | Week at a glance — the 90-minute lecture plan | 250 | What happens in the session, minute by minute |
| 2 | Lecture notes — six to nine numbered sections | 2,800–3,200 | The substance: concepts, mechanisms, debates, numbers |
| 3 | Worked case study | 1,000–1,300 | One family, fully formulated, with the reasoning shown |
| 4 | Annotated transcript | 600–800 | What the therapist did, turn by turn, and why |
| 5 | Laboratory protocol + marking rubric | 600–800 | The assessed practice, with criteria and weights |
| 6 | Skills drill | 250–350 | A repeatable exercise for deliberate practice |
| 7 | Six common errors | 350–450 | What trainees actually get wrong, and the fix |
| 8 | Culture, faith and context note | 350–450 | Local application, with the caution attached |
| 9 | Evidence note or debate | 350–450 | What the literature supports, with hedges intact |
| 10 | Key terms table | 400–500 | 12–18 terms defined for the examination |
| 11 | Self-test — MCQs, short answers, model answers | 550–700 | Formative assessment with the key |
| 12 | Reflective task | 180–250 | The personal work that makes the week stick |
| 13 | Readings | 120–200 | Two core, four extension, with what to notice |

**House style for week content**

- Headings: `### 7.1`, `### 7.2` … under the week's `##` heading, so the PDF contents nests correctly.
- Callouts are blockquote panels, one per line start: `> **CASE** —`, `> **PRACTICAL** —`, `> **CAUTION** —`,
  `> **DEBATE** —`, `> **REFLECT** —`, `> **DRILL** —`, `> **TASK** —`, `> **AUDIT** —`. Dialogue is written
  as `> **Speaker:** …` lines.
- Cases are fictional composites. Names recur across the library so students meet the same families in
  different courses: the Adeyemi family, Mrs Okonkwo and Ebuka (9), Folake and Dele, Aisha and Sam.
- Every clinical claim that has an evidence base gets a hedge: *robust*, *plausible*, *popular but
  unsupported*. Students are being trained to read, not to believe.
- Currency: all figures cited as a percentage must be internally consistent within the book; where a figure
  is illustrative rather than sourced, say so.
- No week may end without a reflective task and a reading list.

**Word-count discipline.** Prose is not padded. The word count is met by covering the topic properly: the
history of the idea, the mechanism, the clinical procedure, the failure modes, the cultural application, the
evidence, the assessment. A week that reaches 8,000 words by repetition is a failed week; a week that reaches
8,000 words because the topic needed it is the standard.
