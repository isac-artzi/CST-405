# CST-405 · Topic 2 — Compiler for a Starter Language · INSTRUCTOR

**Weeks 2–5 · Sep 14 – Oct 11, 2026** — complete implementation of this milestone.

> This is the working solution. `student/topic-2-minimal-compiler/` is the same code with this
> topic's work removed and replaced by TODOs.

## Build and demonstrate

```bash
cd compiler
make
make test                              # every test, cumulative from Topic 2

./minicompiler tests/t2_05_errors_syntax.cm out.s          # full six-phase trace, for projecting
./minicompiler tests/t2_05_errors_syntax.cm out.s -q       # quiet
spim -file out.s
```

The unquiet trace prints the token stream, the AST, the scope stack, the symbol
table with storage assignments, both TAC listings, the optimization scorecard, the
register-allocation statistics and the phase timings. It is built to be projected.

## Teaching notes

- **Four weeks is enough time to get this wrong slowly.** The single most useful intervention is insisting on an end-to-end spike in week 2: `print(1);` all the way to running MIPS, with everything else stubbed. Teams that do this finish; teams that build phase by phase discover in week 5 that their AST is the wrong shape.
- **Demo the tabs in the lecture notes.** One program, seven representations. It is the clearest single artefact in the course.
- **Live-build the grammar one rule at a time.** Start with `decl` alone and compile a file of declarations. Adding rules to a working parser is a completely different experience from writing the whole grammar and debugging it at once.
- **Create a conflict on purpose and open `parser.output`.** Nobody reads it until they are shown it once, and Topic 5 goes much better for the ones who have.
- **The `strdup` bug is worth demonstrating.** Remove it from `createAssign` and show the corrupted AST. It costs two minutes and saves several students an evening.

## What goes wrong

- Leaving code generation to week 5.
- `printAST` written badly or late. It is the debugging instrument for the rest of the term.
- Dividing the work by file rather than by phase, so nobody owns a boundary and nobody can explain one in their video.
- Forgetting `free($2)` on identifiers — invisible until valgrind in Topic 6.

## Class activities for this topic

- **Week 2 · Wednesday** — Derivations, Parse Trees, and Ambiguity (`docs/topic-2-minimal-compiler/activity-1-derivations-and-ambiguity.html`)
- **Week 2 · Friday** — First Contact with Bison (`docs/topic-2-minimal-compiler/activity-2-first-contact-with-bison.html`)
- **Week 3 · Wednesday** — Parse Tree vs AST (`docs/topic-2-minimal-compiler/activity-3-parse-tree-vs-ast.html`)
- **Week 3 · Friday** — Build the Tree, Then Print It (`docs/topic-2-minimal-compiler/activity-4-build-the-tree.html`)
- **Week 4 · Wednesday** — Predict the Symbol Table (`docs/topic-2-minimal-compiler/activity-5-symbol-table-and-scope.html`)
- **Week 4 · Friday** — Three-Address Code by Hand (`docs/topic-2-minimal-compiler/activity-6-tac-by-hand.html`)
- **Week 5 · Wednesday** — Your First Running Program (`docs/topic-2-minimal-compiler/activity-7-first-running-program.html`)
- **Week 5 · Friday** — Error Message Clinic (`docs/topic-2-minimal-compiler/activity-8-error-message-clinic.html`)

## Regenerating this folder

Both the student and instructor copies are generated from one annotated master:

```bash
python3 .tools/stagegen.py --check     # regenerate, then build and test everything
```

Edit `.tools/master/`, never this folder — changes here are overwritten on the next
run. See `.tools/README.md`.
