#!/usr/bin/env python3
"""
readmegen.py — write the README for every student/ and instructor/ topic folder,
plus the repository README.

Kept next to the other generators so that a change to the topic list, the file
layout or the build commands is made in one place.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from docgen import TOPICS  # noqa: E402

BY_N = {t["n"]: t for t in TOPICS}

# ---------------------------------------------------------------------------
# Per-topic specifics
# ---------------------------------------------------------------------------
DETAIL = {
1: dict(
  dir="lexer", exe="lexer",
  given=["`tokens.h` — the token kinds, and the counters the scanner maintains",
         "`main.c` — the driver that prints the token table and the summary",
         "`Makefile`, and six test files under `tests/`"],
  build=["`scanner.l` — every rule, in the order the TODO comments give",
         "`tokenName()` and `tokenCategory()` in `main.c`"],
  done=["`make test` reports 0 errors for tests 01–04",
        "`./lexer tests/05_lexical_errors.cm` reports **four** errors and exits 1",
        "`./lexer tests/06_unterminated_comment.cm` reports one error and exits 1"],
  teach=[
    "**Open with the token table.** Run the instructor lexer on "
    "`tests/01_all_tokens.cm` before saying anything about theory. The table is the "
    "thing; the theory explains it.",
    "**The rule-order demo lands every time.** Move the identifier rule above the "
    "keywords, live, and run `tests/03_keywords_vs_ids.cm`. `int` comes back as an "
    "ID. Ten seconds, and it fixes first-match resolution permanently.",
    "**Then the longest-match demo.** Delete the `\"<=\"` rule and run "
    "`tests/02_longest_match.cm`. Four tokens become eight.",
    "**Spend real time on columns.** Flex gives you lines free and columns not at "
    "all. Ask the class what `skip()` is for before telling them, then delete it from "
    "the block-comment rule and show `tests/04_comments.cm` reporting line 4 instead "
    "of line 6.",
    "**The boundary question is worth five minutes.** Why is `int int int;` not a "
    "lexical error? Most of the term's confusion is students expecting one phase to "
    "do another's work, and this is the cheapest place to head it off."],
  pitfalls=[
    "Students who tokenize only what Topic 2 needs and have to reopen this file in "
    "week 12. Push hard on scanning the whole language now.",
    "`exit()` in the error action. Tests 05 then reports one error instead of four.",
    "Forgetting `yylval` — harmless this week, and a mystery in Topic 2 when every "
    "identifier turns out to be the same string."]),

2: dict(
  dir="compiler", exe="minicompiler",
  given=["`scanner.l` — a reference version of the Project 1 scanner, adapted to "
         "return bison token numbers",
         "every `.h` file — the data structures are the design",
         "`parser.y` prologue: `%union`, `%token`, the precedence table, `yyerror`",
         "`tac.c` machinery: temporary and label allocation, list handling",
         "`codegen.c` parts 1–3: the register cache, addressing, frame layout",
         "`main.c` — the six-phase driver"],
  build=["the grammar rules and their semantic actions (`parser.y`)",
         "the AST constructors and `printAST` (`ast.c`)",
         "symbol table insert and lookup (`symtab.c`)",
         "the semantic checks (`semantic.c`)",
         "AST → TAC (`tac.c`)",
         "one optimization pass (`tac.c`)",
         "TAC → MIPS instruction selection (`codegen.c`)"],
  done=["`make test` runs every program in `tests/`",
        "`t2_01`–`t2_03` produce the outputs in their header comments",
        "`t2_04` and `t2_05` are supposed to FAIL — check the messages name the "
        "right line"],
  teach=[
    "**Four weeks is enough time to get this wrong slowly.** The single most useful "
    "intervention is insisting on an end-to-end spike in week 2: `print(1);` all the "
    "way to running MIPS, with everything else stubbed. Teams that do this finish; "
    "teams that build phase by phase discover in week 5 that their AST is the wrong "
    "shape.",
    "**Demo the tabs in the lecture notes.** One program, seven representations. It "
    "is the clearest single artefact in the course.",
    "**Live-build the grammar one rule at a time.** Start with `decl` alone and "
    "compile a file of declarations. Adding rules to a working parser is a completely "
    "different experience from writing the whole grammar and debugging it at once.",
    "**Create a conflict on purpose and open `parser.output`.** Nobody reads it until "
    "they are shown it once, and Topic 5 goes much better for the ones who have.",
    "**The `strdup` bug is worth demonstrating.** Remove it from `createAssign` and "
    "show the corrupted AST. It costs two minutes and saves several students an "
    "evening."],
  pitfalls=[
    "Leaving code generation to week 5.",
    "`printAST` written badly or late. It is the debugging instrument for the rest "
    "of the term.",
    "Dividing the work by file rather than by phase, so nobody owns a boundary and "
    "nobody can explain one in their video.",
    "Forgetting `free($2)` on identifiers — invisible until valgrind in Topic 6."]),

3: dict(
  dir="compiler", exe="minicompiler",
  given=["the complete, working Topic 2 compiler — it builds and passes the Topic 2 "
         "tests before anything is written"],
  build=["arithmetic: `- * /`, parentheses, unary minus, and the precedence table",
         "arrays: declaration, indexing, array parameters",
         "functions: definitions, parameters, calls, `return`",
         "scope: a scope stack, and two-pass semantic analysis",
         "activation records: prologue, epilogue, saved `$ra`, arguments in "
         "`$a0`–`$a3`"],
  done=["all five `t3_*` tests produce the outputs in their header comments",
        "the Topic 2 tests still pass",
        "`fact(5)` returns 120 — if it does not, the calling convention is wrong"],
  teach=[
    "**The activation record is the whole topic.** Budget accordingly: arithmetic and "
    "arrays are one class between them; functions are two.",
    "**Draw the stack on the board and then show the generated `.s`.** The stepper in "
    "the lecture notes walks it frame by frame; project it and talk over it.",
    "**Demonstrate the three failure modes.** Comment out the `sw $ra` and run "
    "something recursive. Skip the frame push and watch a caller's locals change. Make "
    "`TAC_RETURN` fall through instead of jumping to the epilogue and show a function "
    "returning the wrong value. Each takes a minute and each is a bug half the class "
    "will otherwise write.",
    "**Be explicit about the two symbol tables.** `semantic.c` answers *is this name "
    "visible*; `symtab.c` answers *what address is it*. Students conflate them and "
    "then cannot debug either.",
    "**Array parameters by reference deserve their own five minutes.** Why does "
    "`int a[]` occupy four bytes? Ask before answering."],
  pitfalls=[
    "Recursion that works for n=1 and fails for n=2: `$ra` is not being saved.",
    "A callee clobbering the caller's locals: no new frame is being pushed.",
    "`f(1, g(2))` wrong while `f(1, 2)` is right: argument buffering, or arguments "
    "materialised after the register flush rather than before it.",
    "Misaligned global arrays. Without `.align 2` after the newline string, every "
    "`lw` raises an address error in SPIM and the message does not point at the "
    "cause."]),

4: dict(
  dir="compiler", exe="minicompiler",
  given=["the complete Topic 3 compiler"],
  build=["relational operators, and their place in the precedence table",
         "`while` and `for`, lowered to labels and jumps",
         "`break`, with the label stack and the depth check",
         "label and branch emission in the back end",
         "branch simplification in the optimizer"],
  done=["all six `t4_*` tests pass, plus everything from Topics 2 and 3",
        "the optimizer reports a scorecard and reaches a fixed point",
        "a benchmark has been measured optimized vs unoptimized"],
  teach=[
    "**Lower a loop on the board before showing any code.** The stepper in the "
    "lecture notes is built for exactly this; step through it and have the class call "
    "out the next instruction.",
    "**Test-at-top vs test-at-bottom.** Move the test and ask what construct they "
    "just built. It is the cleanest way to make `do-while` feel inevitable rather "
    "than arbitrary.",
    "**The fixed-point demo is the highlight of the topic.** Compile "
    "`t4_06_optimize.cm` and read the pass-by-pass output aloud: 14 changes, then 5, "
    "then 0. Then ask why one pass was not enough.",
    "**Then break the safety rule.** Remove `clearFacts()` at `TAC_LABEL` and compile "
    "a loop. The compiler still passes every Topic 2 and 3 test and is silently wrong "
    "on loops. It is the most instructive five minutes in the course.",
    "**Insist on the measurement distinction.** Code size and work done are different "
    "numbers. Students will conflate them in Project 6 unless it is nailed down here."],
  pitfalls=[
    "A single-pass optimizer, reported as if it were finished.",
    "Propagating constants across a label — correct on tests, wrong on loops.",
    "Reused labels from a broken label generator.",
    "Reporting a 4% speedup with 9% run-to-run variance. Make them repeat runs."]),

5: dict(
  dir="compiler", exe="minicompiler",
  given=["the complete Topic 4 compiler"],
  build=["`if` and `if`/`else`, with the dangling-else resolved by precedence",
         "logical `&&`, `||`, `!` — including the operand normalisation",
         "`switch`, `case`, `default`, fall-through and `break` (optional but "
         "recommended)",
         "the switch semantic checks: one `default`, no duplicate case values"],
  done=["all five `t5_*` tests pass, plus everything before them",
        "`bison -v parser.y` reports **no** conflicts",
        "`t5_02_dangling_else.cm` prints 2"],
  teach=[
    "**Build the conflict live, then read `parser.output` together.** This is the "
    "single best opportunity all term to show what an LALR parser is actually doing.",
    "**Then swap `%nonassoc LOWER_THAN_ELSE` and `%nonassoc ELSE`** and run the "
    "dangling-else test. It prints nothing instead of 2. Positional precedence stops "
    "being abstract.",
    "**`2 && 1` is the demo for logical operators.** Emit `and` directly, show it "
    "produce 0, then add the `sne` normalisation.",
    "**Lower `switch` on the board as dispatch-then-bodies.** Fall-through falls out "
    "of the layout with no extra machinery, and students find that genuinely "
    "surprising.",
    "**The jump-table comparison is worth ten minutes** even though nobody implements "
    "it. `case 1, 1000, 50000` makes the trade-off obvious.",
    "**The Week 14 audit activity is the best class of the term.** Adversarial "
    "testing of each other's compilers finds real bugs and the diagnosis practice is "
    "exactly what Project 6 needs."],
  pitfalls=[
    "Leaving the shift/reduce conflict in and calling it resolved.",
    "Bitwise `and` on unnormalised operands.",
    "`return` inside a switch case, when `TAC_RETURN` does not jump to the epilogue. "
    "It is invisible until someone writes exactly that program.",
    "`break` inside a switch inside a loop leaving the loop. Check the label stack "
    "discipline."]),

6: dict(
  dir="compiler", exe="minicompiler",
  given=["the complete compiler, and the full cumulative test suite"],
  build=["nothing new in the language",
         "a README a stranger can build from",
         "compilation-time and execution-time measurements",
         "an honest limitations section"],
  done=["every test from Topics 2–5 passes",
        "`t6_06_everything.cm` runs — that program exercises every feature at once",
        "someone outside the team has built it from the README alone"],
  teach=[
    "**Run the cold-start test for real.** Have teams swap repositories and build "
    "from the README with no verbal help. It finds every hole in twenty minutes, and "
    "no amount of telling them to write a good README achieves the same thing.",
    "**Push back on every number.** Compared to what? On what benchmark? How many "
    "runs? Most reported speedups do not survive the third question.",
    "**Ask for the limitations list before the demo.** A team that can list five real "
    "limits with reasons has understood their compiler; a team that says it does "
    "everything has not looked.",
    "**Lab Question 29 is a design review, not a confession.** Frame it that way or "
    "you get apologies instead of analysis.",
    "**The `--dot` / GraphViz extension is cheap and makes the videos much better.** "
    "Mention it in week 14 so teams have time."],
  pitfalls=[
    "Wall-clock timings from SPIM. It is not a timing-accurate simulator; instruction "
    "counts are the honest metric.",
    "A performance section with no baseline.",
    "Build artefacts committed to the repository.",
    "A single 'final' commit, which says more about the team's process than they "
    "intend."]),
}


STUDENT = """# CST-405 · Topic {n} — {title}

**{weeks} · {dates}**

{blurb}

---

## What you are given

This folder is a **working compiler**. Build it before you change anything:

```bash
cd {dir}
make
```

{given}

## What you are building

{build}

Every place you need to write something is marked `TODO (Topic {n})` in the source,
with the guidance you need at that spot. Work through them in the order they appear
in the file — they are ordered deliberately.

```bash
grep -rn "TODO (Topic {n})" {dir}
```

## Building and testing

{howto}

## You are done when

{done}

## The rest of this topic

- **Lecture notes** — `../../docs/{slug}/lecture-notes.html`
- **Class activities** — `../../docs/{slug}/` (one per class meeting)
- **The assignment** — `../../docs/{slug}/CST-405-Topic-{n}-Project-{n}.docx`
- **Grammar reference** — `../../docs/C-Minus-Grammar-Reference.md`

## Requirements

`flex`, `bison`, `gcc`, `make`, and [SPIM](http://spimsimulator.sourceforge.net/)
or QtSPIM to run the generated assembly.
"""

INSTRUCTOR = """# CST-405 · Topic {n} — {title} · INSTRUCTOR

**{weeks} · {dates}** — complete implementation of this milestone.

> This is the working solution. `student/{slug}/` is the same code with this
> topic's work removed and replaced by TODOs.

## Build and demonstrate

{howto_i}

## Teaching notes

{teach}

## What goes wrong

{pitfalls}

## Class activities for this topic

{acts}

## Regenerating this folder

Both the student and instructor copies are generated from one annotated master:

```bash
python3 .tools/stagegen.py --check     # regenerate, then build and test everything
```

Edit `.tools/master/`, never this folder — changes here are overwritten on the next
run. See `.tools/README.md`.
"""


HOWTO_LEXER = """```bash
cd {dir}
make                                   # build ./{exe}
make test                              # run the lexer over every tests/*.cm
make clean                             # remove everything make produced

./{exe} tests/{example}                # the full token table
./{exe} tests/{example} -c             # counts and summary only
echo $?                                # 0 = lexically clean, 1 = errors found
```

The exit status matters: it is what lets a script tell success from failure without
reading the output."""

HOWTO_LEXER_I = """```bash
cd {dir}
make
make test

./{exe} tests/{example}                # the token table, for projecting
./{exe} tests/05_lexical_errors.cm     # four errors from one run
./{exe} tests/06_unterminated_comment.cm
```

The token table is built to be projected: number, line, column, kind, lexeme, and
what the kind IS."""

HOWTO_COMPILER = """```bash
cd {dir}
make                                   # build ./{exe}
make test                              # compile and run every tests/*.cm
make clean                             # remove everything make produced

./{exe} tests/{example} out.s          # full trace of all six phases
./{exe} tests/{example} out.s -q       # quiet: errors and summary only
spim -file out.s                       # run the generated MIPS
```

Compiling also writes `out.tac` and `out.optimized.tac`. Reading those two side by
side is the fastest way to see what the optimizer did."""

HOWTO_COMPILER_I = """```bash
cd {dir}
make
make test                              # every test, cumulative from Topic 2

./{exe} tests/{example} out.s          # full six-phase trace, for projecting
./{exe} tests/{example} out.s -q       # quiet
spim -file out.s
```

The unquiet trace prints the token stream, the AST, the scope stack, the symbol
table with storage assignments, both TAC listings, the optimization scorecard, the
register-allocation statistics and the phase timings. It is built to be projected."""


def li(items):
    return "\n".join("- " + i for i in items)


def build():
    for t in TOPICS:
        n = t["n"]
        d = DETAIL[n]
        ext = "cm" if n > 1 else "cm"
        # an example test to name in the instructions
        tdir = os.path.join(ROOT, "instructor", t["slug"], d["dir"], "tests")
        example = "01_all_tokens.cm"
        if os.path.isdir(tdir):
            names = sorted(f for f in os.listdir(tdir) if f.endswith(".cm"))
            if names:
                example = names[-1] if n > 1 else names[0]

        if n == 1:
            howto = HOWTO_LEXER.format(dir=d["dir"], exe=d["exe"], example=example)
            howto_i = HOWTO_LEXER_I.format(dir=d["dir"], exe=d["exe"], example=example)
        else:
            howto = HOWTO_COMPILER.format(dir=d["dir"], exe=d["exe"], example=example)
            howto_i = HOWTO_COMPILER_I.format(dir=d["dir"], exe=d["exe"], example=example)

        common = dict(n=n, title=t["title"], weeks=t["weeks"], dates=t["dates"],
                      blurb=t["blurb"], slug=t["slug"], dir=d["dir"],
                      exe=d["exe"], ext=ext, example=example,
                      howto=howto, howto_i=howto_i)

        s = STUDENT.format(given=li(d["given"]), build=li(d["build"]),
                           done=li(d["done"]), **common)
        p = os.path.join(ROOT, "student", t["slug"], "README.md")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(s)

        # activity list, read from the content module
        sys.path.insert(0, os.path.join(HERE, "content"))
        mod = __import__("topic%d" % n)
        acts = li("**%s** — %s (`docs/%s/activity-%d-%s.html`)"
                  % (a["session"], a["title"], t["slug"], i, a["slug"])
                  for i, a in enumerate(mod.ACTIVITIES, 1))

        i = INSTRUCTOR.format(teach=li(d["teach"]), pitfalls=li(d["pitfalls"]),
                              acts=acts, **common)
        p = os.path.join(ROOT, "instructor", t["slug"], "README.md")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(i)

        print("wrote README for topic %d (student + instructor)" % n)


if __name__ == "__main__":
    build()
