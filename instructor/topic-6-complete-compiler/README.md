# CST-405 · Topic 6 — Compiler Design and Implementation · INSTRUCTOR

**Week 15 · Dec 14 – Dec 20, 2026** — complete implementation of this milestone.

> This is the working solution. `student/topic-6-complete-compiler/` is the same code with this
> topic's work removed and replaced by TODOs.

## Build and demonstrate

```bash
cd compiler
make
make test                              # every test, cumulative from Topic 2

./minicompiler tests/t6_07_benchmark.cm out.s          # full six-phase trace, for projecting
./minicompiler tests/t6_07_benchmark.cm out.s -q       # quiet
spim -file out.s
```

The unquiet trace prints the token stream, the AST, the scope stack, the symbol
table with storage assignments, both TAC listings, the optimization scorecard, the
register-allocation statistics and the phase timings. It is built to be projected.

## Teaching notes

- **Run the cold-start test for real.** Have teams swap repositories and build from the README with no verbal help. It finds every hole in twenty minutes, and no amount of telling them to write a good README achieves the same thing.
- **Push back on every number.** Compared to what? On what benchmark? How many runs? Most reported speedups do not survive the third question.
- **Ask for the limitations list before the demo.** A team that can list five real limits with reasons has understood their compiler; a team that says it does everything has not looked.
- **Lab Question 29 is a design review, not a confession.** Frame it that way or you get apologies instead of analysis.
- **The `--dot` / GraphViz extension is cheap and makes the videos much better.** Mention it in week 14 so teams have time.

## What goes wrong

- Wall-clock timings from SPIM. It is not a timing-accurate simulator; instruction counts are the honest metric.
- A performance section with no baseline.
- Build artefacts committed to the repository.
- A single 'final' commit, which says more about the team's process than they intend.

## Class activities for this topic

- **Week 15 · Wednesday** — Benchmark Your Compiler (`docs/topic-6-complete-compiler/activity-1-benchmark-your-compiler.html`)
- **Week 15 · Friday** — Cold-Start README Test and Demo Dry Run (`docs/topic-6-complete-compiler/activity-2-cold-start-and-demo.html`)

## Regenerating this folder

Both the student and instructor copies are generated from one annotated master:

```bash
python3 .tools/stagegen.py --check     # regenerate, then build and test everything
```

Edit `.tools/master/`, never this folder — changes here are overwritten on the next
run. See `.tools/README.md`.
