# CST-405 · Topic 4 — Compiling Loops · INSTRUCTOR

**Weeks 9–11 · Nov 2 – Nov 22, 2026** — complete implementation of this milestone.

> This is the working solution. `student/topic-4-loops/` is the same code with this
> topic's work removed and replaced by TODOs.

## Build and demonstrate

```bash
cd compiler
make
make test                              # every test, cumulative from Topic 2

./minicompiler tests/t4_06_optimize.cm out.s          # full six-phase trace, for projecting
./minicompiler tests/t4_06_optimize.cm out.s -q       # quiet
spim -file out.s
```

The unquiet trace prints the token stream, the AST, the scope stack, the symbol
table with storage assignments, both TAC listings, the optimization scorecard, the
register-allocation statistics and the phase timings. It is built to be projected.

## Teaching notes

- **Lower a loop on the board before showing any code.** The stepper in the lecture notes is built for exactly this; step through it and have the class call out the next instruction.
- **Test-at-top vs test-at-bottom.** Move the test and ask what construct they just built. It is the cleanest way to make `do-while` feel inevitable rather than arbitrary.
- **The fixed-point demo is the highlight of the topic.** Compile `t4_06_optimize.cm` and read the pass-by-pass output aloud: 14 changes, then 5, then 0. Then ask why one pass was not enough.
- **Then break the safety rule.** Remove `clearFacts()` at `TAC_LABEL` and compile a loop. The compiler still passes every Topic 2 and 3 test and is silently wrong on loops. It is the most instructive five minutes in the course.
- **Insist on the measurement distinction.** Code size and work done are different numbers. Students will conflate them in Project 6 unless it is nailed down here.

## What goes wrong

- A single-pass optimizer, reported as if it were finished.
- Propagating constants across a label — correct on tests, wrong on loops.
- Reused labels from a broken label generator.
- Reporting a 4% speedup with 9% run-to-run variance. Make them repeat runs.

## Class activities for this topic

- **Week 9 · Wednesday** — Lower a Loop by Hand (`docs/topic-4-loops/activity-1-lower-a-loop.html`)
- **Week 9 · Friday** — for vs while — a Design Decision (`docs/topic-4-loops/activity-2-for-vs-while.html`)
- **Week 10 · Wednesday** — break, and the continue You Are Not Implementing (`docs/topic-4-loops/activity-3-break-and-continue.html`)
- **Week 10 · Friday** — Optimize a Listing by Hand (`docs/topic-4-loops/activity-4-optimize-by-hand.html`)
- **Week 11 · Wednesday** — Measure It, and Defend the Number (`docs/topic-4-loops/activity-5-measure-it.html`)
- **Week 11 · Friday** — Unrolling and Strength Reduction (`docs/topic-4-loops/activity-6-unrolling-and-strength-reduction.html`)

## Regenerating this folder

Both the student and instructor copies are generated from one annotated master:

```bash
python3 .tools/stagegen.py --check     # regenerate, then build and test everything
```

Edit `.tools/master/`, never this folder — changes here are overwritten on the next
run. See `.tools/README.md`.
