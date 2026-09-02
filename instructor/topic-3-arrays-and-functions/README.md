# CST-405 · Topic 3 — Compiling Complex Variables and Functions · INSTRUCTOR

**Weeks 6–8 · Oct 12 – Nov 1, 2026** — complete implementation of this milestone.

> This is the working solution. `student/topic-3-arrays-and-functions/` is the same code with this
> topic's work removed and replaced by TODOs.

## Build and demonstrate

```bash
cd compiler
make
make test                              # every test, cumulative from Topic 2

./minicompiler tests/t3_05_scope.cm out.s          # full six-phase trace, for projecting
./minicompiler tests/t3_05_scope.cm out.s -q       # quiet
spim -file out.s
```

The unquiet trace prints the token stream, the AST, the scope stack, the symbol
table with storage assignments, both TAC listings, the optimization scorecard, the
register-allocation statistics and the phase timings. It is built to be projected.

## Teaching notes

- **The activation record is the whole topic.** Budget accordingly: arithmetic and arrays are one class between them; functions are two.
- **Draw the stack on the board and then show the generated `.s`.** The stepper in the lecture notes walks it frame by frame; project it and talk over it.
- **Demonstrate the three failure modes.** Comment out the `sw $ra` and run something recursive. Skip the frame push and watch a caller's locals change. Make `TAC_RETURN` fall through instead of jumping to the epilogue and show a function returning the wrong value. Each takes a minute and each is a bug half the class will otherwise write.
- **Be explicit about the two symbol tables.** `semantic.c` answers *is this name visible*; `symtab.c` answers *what address is it*. Students conflate them and then cannot debug either.
- **Array parameters by reference deserve their own five minutes.** Why does `int a[]` occupy four bytes? Ask before answering.

## What goes wrong

- Recursion that works for n=1 and fails for n=2: `$ra` is not being saved.
- A callee clobbering the caller's locals: no new frame is being pushed.
- `f(1, g(2))` wrong while `f(1, 2)` is right: argument buffering, or arguments materialised after the register flush rather than before it.
- Misaligned global arrays. Without `.align 2` after the newline string, every `lw` raises an address error in SPIM and the message does not point at the cause.

## Class activities for this topic

- **Week 6 · Wednesday** — Precedence and Associativity Lab (`docs/topic-3-arrays-and-functions/activity-1-precedence-lab.html`)
- **Week 6 · Friday** — Arrays Are Address Arithmetic (`docs/topic-3-arrays-and-functions/activity-2-array-addressing.html`)
- **Week 7 · Wednesday** — Draw the Activation Record (`docs/topic-3-arrays-and-functions/activity-3-draw-the-frame.html`)
- **Week 7 · Friday** — Trace a Call, Including a Nested One (`docs/topic-3-arrays-and-functions/activity-4-calling-convention.html`)
- **Week 8 · Wednesday** — Scope and Shadowing (`docs/topic-3-arrays-and-functions/activity-5-scope-and-shadowing.html`)
- **Week 8 · Friday** — Technical Interview Rehearsal (`docs/topic-3-arrays-and-functions/activity-6-interview-rehearsal.html`)

## Regenerating this folder

Both the student and instructor copies are generated from one annotated master:

```bash
python3 .tools/stagegen.py --check     # regenerate, then build and test everything
```

Edit `.tools/master/`, never this folder — changes here are overwritten on the next
run. See `.tools/README.md`.
