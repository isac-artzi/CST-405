# CST-405 · Topic 5 — Compiling Control Flow — Decisions · INSTRUCTOR

**Weeks 12–14 · Nov 23 – Dec 13, 2026** — complete implementation of this milestone.

> This is the working solution. `student/topic-5-decisions/` is the same code with this
> topic's work removed and replaced by TODOs.

## Build and demonstrate

```bash
cd compiler
make
make test                              # every test, cumulative from Topic 2

./minicompiler tests/t5_05_nested_switch.cm out.s          # full six-phase trace, for projecting
./minicompiler tests/t5_05_nested_switch.cm out.s -q       # quiet
spim -file out.s
```

The unquiet trace prints the token stream, the AST, the scope stack, the symbol
table with storage assignments, both TAC listings, the optimization scorecard, the
register-allocation statistics and the phase timings. It is built to be projected.

## Teaching notes

- **Build the conflict live, then read `parser.output` together.** This is the single best opportunity all term to show what an LALR parser is actually doing.
- **Then swap `%nonassoc LOWER_THAN_ELSE` and `%nonassoc ELSE`** and run the dangling-else test. It prints nothing instead of 2. Positional precedence stops being abstract.
- **`2 && 1` is the demo for logical operators.** Emit `and` directly, show it produce 0, then add the `sne` normalisation.
- **Lower `switch` on the board as dispatch-then-bodies.** Fall-through falls out of the layout with no extra machinery, and students find that genuinely surprising.
- **The jump-table comparison is worth ten minutes** even though nobody implements it. `case 1, 1000, 50000` makes the trade-off obvious.
- **The Week 14 audit activity is the best class of the term.** Adversarial testing of each other's compilers finds real bugs and the diagnosis practice is exactly what Project 6 needs.

## What goes wrong

- Leaving the shift/reduce conflict in and calling it resolved.
- Bitwise `and` on unnormalised operands.
- `return` inside a switch case, when `TAC_RETURN` does not jump to the epilogue. It is invisible until someone writes exactly that program.
- `break` inside a switch inside a loop leaving the loop. Check the label stack discipline.

## Class activities for this topic

- **Week 12 · Wednesday** — Create the Dangling-Else Conflict, Then Fix It (`docs/topic-5-decisions/activity-1-dangling-else.html`)
- **Week 12 · Friday** — Lower Nested Conditionals (`docs/topic-5-decisions/activity-2-nested-conditionals.html`)
- **Week 13 · Wednesday** — Short-Circuit or Not — Decide It (`docs/topic-5-decisions/activity-3-short-circuit.html`)
- **Week 13 · Friday** — switch: Linear Chain or Jump Table (`docs/topic-5-decisions/activity-4-switch-lowering.html`)
- **Week 14 · Wednesday** — Audit Somebody Else's Compiler (`docs/topic-5-decisions/activity-5-audit-a-compiler.html`)
- **Week 14 · Friday** — MIPS vs ARM — What Would Actually Change (`docs/topic-5-decisions/activity-6-mips-vs-arm.html`)

## Regenerating this folder

Both the student and instructor copies are generated from one annotated master:

```bash
python3 .tools/stagegen.py --check     # regenerate, then build and test everything
```

Edit `.tools/master/`, never this folder — changes here are overwritten on the next
run. See `.tools/README.md`.
