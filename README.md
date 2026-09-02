# CST-405 · Principles of Compiler Design

**Grand Canyon University · Fall 2026 · Sep 8 – Dec 20**

📖 **Course site — start here:** https://isac-artzi.github.io/CST-405/

Lecture notes, class activities, assignment descriptions and the language
reference all live on the site. This repository holds the starter code.

---

## What you are building

This course does not build one compiler in six pieces. It builds **six
compilers**, each one the previous one with a new language feature threaded
through all six phases. You will write the front end six times, and that
repetition is the point: the second time you add a construct, you already know
which files it touches.

```
scanner.l  ->  parser.y  ->  semantic.c  ->  tac.c  ->  tac.c  ->  codegen.c
 lexical       syntax        semantic        IR        optimize    codegen
```

| Topic | Milestone | The language gains | Weeks |
|---|---|---|---|
| 1 | Lexical analysis | the token set, error locations | 1 |
| 2 | A whole compiler | `int`, assignment, `+`, `print` | 2–5 |
| 3 | Variables and functions | arrays, `- * /`, functions, scope | 6–8 |
| 4 | Loops | `while`, `for`, `break`, relational operators | 9–11 |
| 5 | Decisions | `if`/`else`, `&& \|\| !`, `switch` | 12–14 |
| 6 | Complete compiler | no new syntax — measurement and documentation | 15 |

The target is MIPS32, run under [SPIM](http://spimsimulator.sourceforge.net/) or
QtSPIM.

## Layout

```
student/topic-1-lexical-analysis/      Topic 1 · Project 1
student/topic-2-minimal-compiler/      Topic 2 · Project 2
student/topic-3-arrays-and-functions/  Topic 3 · Project 3
student/topic-4-loops/                 Topic 4 · Project 4
student/topic-5-decisions/             Topic 5 · Project 5
student/topic-6-complete-compiler/     Topic 6 · Project 6

docs/                                  the course site
```

Each topic folder is **the previous milestone, complete and working**, with that
topic's work removed and replaced by numbered TODOs. It builds and runs as handed
to you — build it *before* you change anything, so that from then on any failure
is one you introduced.

Each folder has its own `README.md` saying what you are given, what you are
building, and how you know when you are done.

## Getting started

```bash
git clone https://github.com/isac-artzi/CST-405.git
cd CST-405/student/topic-1-lexical-analysis/lexer

make                      # build it
make test                 # run it over every program in tests/
```

From Topic 2 onward the executable is a compiler:

```bash
cd CST-405/student/topic-2-minimal-compiler/compiler
make
./minicompiler tests/t2_01_basics.cm out.s      # full trace of all six phases
./minicompiler tests/t2_01_basics.cm out.s -q   # quiet: errors and summary only
spim -file out.s                                # run the generated MIPS
```

Compiling also writes `out.tac` and `out.optimized.tac`. Reading those two side by
side is the fastest way to see what the optimizer did.

## Finding the work

Every place you need to write something is marked in the source with the topic
number and enough guidance to start:

```bash
grep -rn "TODO (Topic 3)" student/topic-3-arrays-and-functions/compiler
```

Work through them in the order they appear in each file — they are ordered
deliberately.

## The tests

`tests/` in each topic folder holds the programs your compiler must handle. Every
one states its expected output in a header comment, and a few are **supposed to
fail** — those check your error messages, and their comments say so.

The tests are **cumulative**. The Topic 5 folder still contains the Topic 3 tests,
and they must still pass. A milestone that breaks an earlier one is not a
milestone.

## What you need installed

- `flex` 2.6+
- `bison` 2.3+ (3.x also works)
- `gcc` or `clang`, and `make`
- SPIM or QtSPIM, to run the assembly your compiler produces

```bash
flex --version && bison --version && gcc --version && which spim
```

Project 1 asks for evidence that this toolchain is installed and working, so run
that check early.

## Submitting

Push your work to your **own private** repository and add the instructor as a
collaborator — not to this one. Each assignment description on the course site has
the full submission checklist, including the video requirement.
