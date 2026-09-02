#!/usr/bin/env python3
"""
stagegen.py — build the per-topic compiler folders from one master source.

WHY THIS EXISTS
---------------
CST-405 hands students a compiler that grows across six topics.  Every topic
needs two copies of the same code base:

    instructor/topic-N/   the complete, working milestone (for lecturing)
    student/topic-N/      the same code with THIS topic's feature removed and
                          replaced by TODOs (the assignment)

Maintaining eight nearly-identical copies by hand guarantees they drift apart.
Instead there is ONE master (.tools/master/) annotated with stage markers, and
this script cuts every folder out of it.  Fix a bug once, regenerate, done.

MARKERS
-------
All markers are ordinary block comments, so the master itself still compiles
and can be tested directly.

    /*#4*/                     alone on a line: start a block introduced in
                               Topic 4
    /*#todo one line of text*/ (optional, repeated) the guidance students see
                               in place of the block
    /*#end*/                   end of the block

    some_code();     /*#4*/    a trailing marker gates that single line

GENERATION RULES for target topic S:

    block introduced at N > S   omitted entirely (feature not invented yet)
    block introduced at N < S   emitted in full (already-solved earlier work)
    block introduced at N == S  instructor: emitted in full
                                student:    replaced by a TODO comment

USAGE
    python3 .tools/stagegen.py            # regenerate everything
    python3 .tools/stagegen.py --check    # build + test every folder
"""

import os
import re
import shutil
import subprocess
import sys

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.dirname(HERE)
MASTER = os.path.join(HERE, "master")

# --------------------------------------------------------------------------
# The topics that are generated from the master.  Topics 1 and 2 have their
# own hand-written code bases (a scanner-only project and the minimal
# compiler), so they are not listed here.
# --------------------------------------------------------------------------
TOPICS = {
    2: dict(slug="topic-2-minimal-compiler",
            title="Compiler for a Starter Language",
            project="Project 2"),
    3: dict(slug="topic-3-arrays-and-functions",
            title="Compiling Complex Variables and Functions",
            project="Project 3"),
    4: dict(slug="topic-4-loops",
            title="Compiling Loops",
            project="Project 4"),
    5: dict(slug="topic-5-decisions",
            title="Compiling Control Flow — Decisions",
            project="Project 5"),
    6: dict(slug="topic-6-complete-compiler",
            title="Compiler Design and Implementation",
            project="Project 6"),
}

SOURCES = ["scanner.l", "parser.y", "ast.h", "ast.c", "symtab.h", "symtab.c",
           "semantic.h", "semantic.c", "tac.h", "tac.c", "codegen.h",
           "codegen.c", "trace.h", "main.c", "Makefile"]

# --------------------------------------------------------------------------
# PROGRESSION NOTES
# One entry per (file, topic).  These become the "what changed / what is next"
# banner at the top of every generated source file, so a student opening
# tac.c in Topic 4 can see at a glance how it differs from Topic 3 and where
# it is heading in Topic 5.
# --------------------------------------------------------------------------
PHASE_OF = {
    "scanner.l":  "Phase 1 — Lexical analysis",
    "parser.y":   "Phase 2 — Syntax analysis",
    "ast.h":      "Phase 2 — Syntax analysis (the tree it builds)",
    "ast.c":      "Phase 2 — Syntax analysis (the tree it builds)",
    "symtab.h":   "Phases 3 & 6 — Symbol table / storage map",
    "symtab.c":   "Phases 3 & 6 — Symbol table / storage map",
    "semantic.h": "Phase 3 — Semantic analysis",
    "semantic.c": "Phase 3 — Semantic analysis",
    "tac.h":      "Phases 4 & 5 — Intermediate code and optimization",
    "tac.c":      "Phases 4 & 5 — Intermediate code and optimization",
    "codegen.h":  "Phase 6 — MIPS code generation",
    "codegen.c":  "Phase 6 — MIPS code generation",
    "main.c":     "The driver — runs all six phases in order",
    "trace.h":    "Shared tracing helper",
    "Makefile":   "Build rules",
}

CHANGES = {
    2: {
        "scanner.l":  ["The starter token set: `int`, `print`, identifiers, numbers,",
                       "`+`, `=`, `;`, `(`, `)`, and both comment forms"],
        "parser.y":   ["The starter grammar: a program is a list of statements",
                       "Declaration, assignment, addition, and print",
                       "Error productions that name the mistake instead of just saying \"syntax error\""],
        "ast.h":      ["The node kinds the starter language needs: NUM, VAR, BINOP,",
                       "DECL, ASSIGN, PRINT, STMT_LIST"],
        "ast.c":      ["One constructor per node kind, plus a tree printer"],
        "symtab.h":   ["Name -> storage location, the map every later phase consults"],
        "symtab.c":   ["Four bytes per int, handed out in declaration order"],
        "semantic.c": ["Undeclared variables and duplicate declarations, reported with line numbers"],
        "tac.c":      ["AST -> three-address code, plus the optimizer skeleton"],
        "codegen.c":  ["TAC -> MIPS: a register cache over memory homes, and syscalls for print"],
        "main.c":     ["The six-phase driver every later milestone reuses unchanged"],
    },
    3: {
        "scanner.l":  ["Tokens for `[`, `]`, `,`, `{`, `}` and the arithmetic operators",
                       "`return` keyword for functions"],
        "parser.y":   ["A program is now a list of declarations AND function definitions",
                       "Array declaration `int a[10];`, indexing `a[i]`, and array parameters `int a[]`",
                       "Full arithmetic with precedence: + - * / , parentheses, unary minus",
                       "Function definitions, parameter lists, calls, and `return`"],
        "ast.h":      ["New nodes: FUNC_DEF, PARAM, PARAM_LIST, FUNC_CALL, ARG_LIST, RETURN",
                       "New nodes: ARRAY_DECL, ARRAY_INDEX, BLOCK"],
        "ast.c":      ["Constructors and printing for every new node type"],
        "symtab.h":   ["Split into a global table (.data) and a per-function table (the frame)",
                       "Arrays record their element count; array parameters record that the slot holds an address"],
        "symtab.c":   ["Storage is now assigned per function, not once for the whole program"],
        "semantic.c": ["A scope STACK replaces the single flat scope",
                       "Function signatures are collected first, so calls may appear before definitions",
                       "Argument count is checked against the declaration"],
        "tac.c":      ["FUNC_BEGIN / FUNC_END / PARAM / ARG / CALL / RETURN instructions",
                       "ARRAY_DECL / ARRAY_LOAD / ARRAY_STORE instructions"],
        "codegen.c":  ["Real activation records: prologue, epilogue, saved $ra",
                       "Globals emitted into .data; locals addressed off $sp",
                       "Arguments passed in $a0-$a3; arrays passed by reference"],
        "main.c":     ["Reports the storage map for each function as it is generated"],
    },
    4: {
        "scanner.l":  ["Relational operators `<  >  <=  >=  ==  !=`",
                       "Keywords `while`, `for`, `break`"],
        "parser.y":   ["Relational operators, slotted BELOW + - * / in the precedence table",
                       "`while (cond) stmt` and `for (init; cond; update) stmt`",
                       "`break;` to leave a loop early"],
        "ast.h":      ["New nodes: WHILE, FOR, BREAK"],
        "ast.c":      ["Constructors and printing for the loop nodes"],
        "semantic.c": ["`break` is rejected outside a loop, using a loop-depth counter"],
        "tac.c":      ["Labels and jumps: LABEL, GOTO, IF_FALSE, IF_TRUE",
                       "Loops are lowered to test-at-the-top label/jump patterns",
                       "A break-label stack so `break` knows which loop to leave",
                       "The optimizer now runs to a FIXED POINT and reports what each technique achieved"],
        "codegen.c":  ["Branch and label emission; registers are flushed at every control-flow join"],
        "main.c":     ["Per-phase timing, and an optimization scorecard for the write-up"],
    },
    5: {
        "scanner.l":  ["Keywords `if`, `else`, `switch`, `case`, `default`",
                       "Logical operators `&&`, `||`, `!` and the `:` delimiter"],
        "parser.y":   ["`if (cond) stmt` and `if (cond) stmt else stmt`",
                       "The dangling-else ambiguity resolved with %nonassoc precedence",
                       "`switch` with `case`, `default` and fall-through",
                       "Logical operators, placed at the BOTTOM of the precedence table"],
        "ast.h":      ["New nodes: IF, SWITCH, CASE"],
        "ast.c":      ["Constructors and printing for the decision nodes"],
        "semantic.c": ["`break` is now also valid inside a switch"],
        "tac.c":      ["if / if-else lowered with IF_FALSE and GOTO",
                       "switch lowered to a linear dispatch chain plus a body section, which is what makes fall-through fall out naturally"],
        "codegen.c":  ["Logical operators: operands normalised to 0/1 before the bitwise instruction"],
    },
    6: {
        "main.c":     ["The full metrics report: phase timings, optimization scorecard, spill counts"],
        "codegen.c":  ["No new language features — this is the milestone where the compiler is measured, documented and stress-tested"],
    },
}

NEXT = {
    2: "Topic 3 adds functions, arrays and the rest of arithmetic — and with them, real activation records.",
    3: "Topic 4 adds loops (while, for, break) and the label/jump machinery they need.",
    4: "Topic 5 adds decisions (if, if-else, switch) and the logical operators.",
    5: "Topic 6 adds no new syntax: it measures, documents and hardens what you have.",
    6: "This is the final milestone.",
}

MARK_BLOCK = re.compile(r"^\s*/\*#(\d)(!?)\*/\s*$")
MARK_TODO  = re.compile(r"^\s*/\*#todo ?(.*?)\*/\s*$")
MARK_END   = re.compile(r"^\s*/\*#end\*/\s*$")
MARK_LINE  = re.compile(r"^(.*?)\s*/\*#(\d)\*/\s*$")


def banner(fname, topic, mode):
    """The progression header stamped on top of every generated source file."""
    info = TOPICS[topic]
    changed = CHANGES.get(topic, {}).get(fname, [])
    prev = CHANGES.get(topic - 1, {}).get(fname, [])
    w = 76
    L = []
    L.append("/* " + "=" * (w - 3))
    L.append(" * CST-405  ·  TOPIC %d  ·  %s" % (topic, info["title"]))
    L.append(" * FILE: %s   —   %s" % (fname, PHASE_OF.get(fname, "")))
    L.append(" * " + "-" * (w - 3))
    L.append(" * THE PIPELINE, AND WHERE THIS FILE SITS IN IT")
    order = ["scanner.l", "parser.y", "ast.c", "semantic.c", "tac.c", "codegen.c"]
    lane = []
    for f in order:
        base = f.replace(".c", "").replace(".l", "").replace(".y", "")
        lane.append(base)
    L.append(" *   " + " -> ".join(lane))
    mine = fname.replace(".c", "").replace(".h", "").replace(".l", "").replace(".y", "")
    if mine in lane:
        pad = 0
        for b in lane:
            if b == mine:
                break
            pad += len(b) + 4
        L.append(" *   " + " " * pad + "^" * len(mine) + "  this file")
    L.append(" *")
    if changed:
        L.append(" * WHAT IS NEW IN TOPIC %d" % topic)
        for c in changed:
            L.append(" *   • " + c)
    else:
        L.append(" * UNCHANGED SINCE TOPIC %d — the interfaces held, which is the point" % (topic - 1))
        if prev:
            L.append(" * (last changed in Topic %d: %s)" % (topic - 1, prev[0]))
    L.append(" *")
    L.append(" * WHAT COMES NEXT")
    L.append(" *   " + NEXT[topic])
    if mode == "student":
        L.append(" *")
        L.append(" * YOUR TASK")
        L.append(" *   Everything below marked  TODO (Topic %d)  is yours to write." % topic)
        L.append(" *   Everything else already works — it is the Topic %d compiler you" % (topic - 1))
        L.append(" *   have already built and tested.  Do not rewrite it; extend it.")
    L.append(" * " + "=" * (w - 3) + " */")
    return "\n".join(L) + "\n"


def transform(text, topic, mode):
    """Apply the stage markers to one file's text."""
    out, todo, depth, keep = [], [], 0, True
    stage = 0
    indent = ""
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        m = MARK_BLOCK.match(line)
        if m and depth == 0:
            stage = int(m.group(1))
            only  = (m.group(2) == "!")   # /*#2!*/ = present ONLY at topic 2
            indent = line[:len(line) - len(line.lstrip())]
            depth = 1
            todo = []
            # collect the TODO text that immediately follows
            j = i + 1
            while j < len(lines) and MARK_TODO.match(lines[j]):
                todo.append(MARK_TODO.match(lines[j]).group(1).rstrip())
                j += 1
            if only:
                # An "only" block is scaffolding that a later milestone
                # replaces outright.  The instructor copy of Topic K keeps
                # Topic K's scaffolding.  The STUDENT copy of Topic K also
                # keeps Topic K-1's, because a student skeleton must be the
                # previous working milestone plus TODOs — it has to build and
                # run before they touch it, or they cannot tell their own
                # mistakes from ours.
                keep = (stage == topic) or (mode == "student" and stage == topic - 1)
            else:
                keep = (stage <= topic)
            # Scaffolding is never the answer to its own milestone, so it is
            # emitted verbatim rather than turned into a TODO.
            emit_todo = (not only) and stage == topic and mode == "student"
            body = []
            k = j
            while k < len(lines) and not MARK_END.match(lines[k]):
                if MARK_BLOCK.match(lines[k]):
                    raise SystemExit(
                        "stagegen: nested /*#N*/ block near line %d — a missing "
                        "/*#end*/ on its own line?  Offending text: %r"
                        % (k + 1, lines[k]))
                body.append(lines[k])
                k += 1
            if k >= len(lines):
                raise SystemExit(
                    "stagegen: unterminated /*#%d*/ block opened at line %d"
                    % (stage, i + 1))
            if emit_todo:
                out.append(indent + "/* " + "-" * 62)
                out.append(indent + " * TODO (Topic %d)" % topic)
                if todo:
                    for t in todo:
                        out.append((indent + " * " + t).rstrip())
                else:
                    out.append(indent + " * Implement this part of the milestone.")
                out.append(indent + " * " + "-" * 62 + " */")
            elif keep:
                out.extend(body)
            i = k + 1
            depth = 0
            continue

        if MARK_END.match(line) or MARK_TODO.match(line):
            i += 1
            continue

        # A trailing marker gates that one line.  It follows the same rule as
        # a block: already-solved work stays, the current milestone's work is
        # removed for students (silently — a one-line gate has no TODO text of
        # its own; the block that introduces the feature carries the guidance).
        m = MARK_LINE.match(line)
        if m and m.group(1).strip():
            n = int(m.group(2))
            if n < topic or (n == topic and mode != "student"):
                out.append(m.group(1).rstrip())
            i += 1
            continue

        out.append(line)
        i += 1

    text = "\n".join(out)
    # collapse the runs of blank lines that removals leave behind
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def copy_tests(topic, dest):
    """Tests are CUMULATIVE from Topic 3 on: Topic 5 must still pass every
    Topic 3 and 4 test.  A milestone that breaks an earlier one is not a
    milestone.  Topic 2's tests are the exception — its programs are bare
    statement lists, which stop being legal the moment Topic 3 requires
    everything to live inside a function."""
    tdir = os.path.join(dest, "tests")
    os.makedirs(tdir, exist_ok=True)
    first = 2 if topic == 2 else 3
    for t in range(first, topic + 1):
        src = os.path.join(HERE, "tests", "topic%d" % t)
        if not os.path.isdir(src):
            continue
        for f in sorted(os.listdir(src)):
            if f.endswith(".cm"):
                shutil.copy(os.path.join(src, f),
                            os.path.join(tdir, "t%d_%s" % (t, f)))


def build_folder(topic, mode, dest):
    os.makedirs(dest, exist_ok=True)
    copy_tests(topic, dest)
    for f in SOURCES:
        src = os.path.join(MASTER, f)
        if not os.path.exists(src):
            continue
        text = open(src).read()
        text = transform(text, topic, mode)
        if f.endswith((".c", ".h", ".y", ".l")):
            text = banner(f, topic, mode) + "\n" + text
        open(os.path.join(dest, f), "w").write(text)


def copy_topic1():
    """Topic 1 is a standalone scanner project with its own file set, so it is
    kept as hand-written source in .tools/topic1/ and copied verbatim."""
    for mode in ("instructor", "student"):
        src = os.path.join(HERE, "topic1", mode)
        dst = os.path.join(ROOT, mode, "topic-1-lexical-analysis", "lexer")
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        for junk in ("lexer", "lex.yy.c"):
            j = os.path.join(dst, junk)
            if os.path.exists(j):
                os.remove(j)
        for f in os.listdir(dst):
            if f.endswith(".o"):
                os.remove(os.path.join(dst, f))
        print("copied    %-11s topic 1 -> %s" % (mode, os.path.relpath(dst, ROOT)))


def main():
    check = "--check" in sys.argv
    made = []
    copy_topic1()
    for topic, info in TOPICS.items():
        for mode in ("instructor", "student"):
            dest = os.path.join(ROOT, mode, info["slug"], "compiler")
            if os.path.isdir(dest):
                shutil.rmtree(dest)
            build_folder(topic, mode, dest)
            made.append((topic, mode, dest))
            print("generated %-11s topic %d -> %s" % (mode, topic, os.path.relpath(dest, ROOT)))

    # Topic 2's student skeleton is not "the previous milestone plus TODOs" —
    # there is no previous milestone — so it is built by its own script.
    subprocess.run([sys.executable, os.path.join(HERE, "skeleton2.py")], check=True)

    if not check:
        return 0

    print("\nbuilding every instructor folder:")
    failed = 0

    # Topic 1 is copied rather than generated, but it still has to build.
    t1 = os.path.join(ROOT, "instructor", "topic-1-lexical-analysis", "lexer")
    r = subprocess.run(["make", "-s"], cwd=t1, capture_output=True, text=True)
    print("  topic 1 instructor: %s" % ("BUILD OK" if r.returncode == 0 else "BUILD FAILED"))
    if r.returncode:
        failed += 1
        print(r.stdout[-1500:], r.stderr[-1500:])
    else:
        r = subprocess.run(["make", "-s", "test"], cwd=t1, capture_output=True, text=True)
        for line in r.stdout.split("\n"):
            if line.strip():
                print("    " + line)
    for topic, mode, dest in made:
        if mode != "instructor":
            continue
        r = subprocess.run(["make", "-s"], cwd=dest, capture_output=True, text=True)
        ok = (r.returncode == 0)
        print("  topic %d instructor: %s" % (topic, "BUILD OK" if ok else "BUILD FAILED"))
        if not ok:
            failed += 1
            print(r.stdout[-2000:], r.stderr[-2000:])
            continue
        if r.stderr.strip():
            print("    (compiler warnings)\n" + r.stderr[-1500:])
        r = subprocess.run(["make", "-s", "test"], cwd=dest, capture_output=True, text=True)
        for line in r.stdout.split("\n"):
            print("    " + line)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
