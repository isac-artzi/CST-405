# CST-405 · Principles of Compiler Design

**Grand Canyon University · Fall 2026 · Sep 8 – Dec 20**

Course materials for CST-405: six compiler milestones, interactive lecture notes,
thirty class activities, and the assignment descriptions.

📖 **Course site:** https://isac-artzi.github.io/CST-405/
(GitHub Pages, served from `/docs` — see [Publishing](#publishing-the-course-site))

---

## The idea

This course does not build one compiler in six pieces. It builds **six compilers**,
each one the previous one with a new language feature threaded through all six
phases. Students write the front end six times, and that repetition is the point:
the second time you add a construct, you already know which files it touches.

```
scanner.l  ->  parser.y  ->  semantic.c  ->  tac.c  ->  tac.c  ->  codegen.c
 lexical       syntax        semantic        IR        optimize    codegen
```

| Topic | Milestone | Language gains | Weeks | Project |
|---|---|---|---|---|
| 1 | Lexical analysis | the token set, error locations | 1 | Project 1 |
| 2 | A whole compiler | `int`, assignment, `+`, `print` | 2–5 | Project 2 |
| 3 | Variables and functions | arrays, `- * /`, functions, scope | 6–8 | Project 3 |
| 4 | Loops | `while`, `for`, `break`, relational ops, real optimization | 9–11 | Project 4 |
| 5 | Decisions | `if`/`else`, `&& \|\| !`, `switch` | 12–14 | Project 5 |
| 6 | Complete compiler | no new syntax — measurement and documentation | 15 | Project 6 |

The target is MIPS32, run under [SPIM](http://spimsimulator.sourceforge.net/) or
QtSPIM.

## Layout

```
student/topic-N-.../       the compiler students start from:
                           the previous milestone, with this topic's work
                           removed and replaced by numbered TODOs.
                           It builds and runs before they touch it.

docs/                      the course site: lecture notes, 30 class activities,
                           the six assignment .docx files, and the grammar
                           reference. This is what GitHub Pages serves.

.tools/                    the generators. One annotated master compiler that
                           every topic folder is cut from. See below.

instructor/                NOT IN THIS REPOSITORY. The complete milestone for
                           each topic, plus teaching notes. It lives on the
                           instructor's machine and is regenerated on demand
                           with `python3 .tools/stagegen.py --check`.
```

## Quick start

```bash
# requirements
flex --version && bison --version && gcc --version && which spim

# build and test every milestone
python3 .tools/stagegen.py --check

# or build one by hand
cd instructor/topic-4-loops/compiler
make
make test
./minicompiler tests/t4_02_for.cm out.s     # full six-phase trace
spim -file out.s
```

Passing `-q` silences the trace and prints only errors and the summary.

## Regenerating everything

All twelve code folders — the six published `student/` ones and the six local
`instructor/` ones — come from **one** annotated master, so a bug is fixed once and
propagates everywhere:

```bash
python3 .tools/stagegen.py --check    # 12 code folders; builds and tests them
python3 .tools/docgen.py              # 43 pages of lecture notes and activities
python3 .tools/readmegen.py           # every topic README
python3 .tools/docxgen.py             # the six assignment .docx  (needs python-docx)
```

Edit `.tools/master/` — never the generated folders. Full explanation in
[`.tools/README.md`](.tools/README.md).

## Publishing the course site

The `docs/` directory is a complete static site with no build step.

1. Push to GitHub.
2. **Settings → Pages → Source: Deploy from a branch**, branch `main`, folder
   `/docs`.
3. The site appears at https://isac-artzi.github.io/CST-405/

Everything is relative-linked, so it also works by opening `docs/index.html`
straight off disk.

Nothing else to configure. (`REPO_URL` in `.tools/docgen.py` is already set to this
repository; it is what makes the "your starter code" cards link into the GitHub file
browser. GitHub Pages serves `docs/` as the site root, so those folders cannot be
reached with a relative link — they sit above it.)

## What the compiler can and cannot do

Worth knowing before you assign it. Each limit is deliberate and is discussed in
the topic where it bites.

| Limit | Why |
|---|---|
| `int` is the only type | no type system; the type is not tracked past declaration |
| at most 4 arguments per call | arguments are passed only in `$a0`–`$a3` |
| no array bounds checking | no length information survives to run time |
| registers flushed at every branch | the allocator does not track liveness across blocks |
| optimizer forgets facts at a label | no analysis across basic blocks |
| `t0`, `L0` … are reserved identifiers | they would collide with generated names; the semantic analyzer rejects them with an explanation |

Lifting any of these is a good optional extension, and each is named as one in the
relevant assignment description.

## Requirements

- `flex` 2.6+
- `bison` 2.3+ (also builds with 3.x)
- `gcc` or `clang`
- `make`
- SPIM or QtSPIM
- Python 3.8+ to run the generators; `python-docx` only for the `.docx` files
