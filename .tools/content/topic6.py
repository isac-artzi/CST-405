"""Topic 6 — Compiler Design and Implementation.  Measure it, document it, defend it."""

from docgen import (code, pipeline, tabs, stepper, reveal, quiz, note, table,
                    steps_list, p, h2, h3, h4, ul, ol, deliverable, meta)

LECTURE_TITLE = "Measure It, Document It, Defend It"
LECTURE_LEDE = ("No new syntax this week. The compiler is finished; the question is whether you "
                "can say anything true about it.")


def lecture():
    return (
        h2("What is left") +
        p("Every language feature is in. Topic 6 adds nothing to the grammar. What it "
          "adds is the three things that separate a project from a piece of "
          "engineering: <b>numbers</b>, <b>documentation</b>, and an honest account of "
          "the <b>limits</b>.") +
        pipeline(done=(0, 1, 2, 3, 4, 5)) +

        h2("Two different performance questions") +
        p("The Benchmark project asks for compilation time and execution time. They "
          "measure different things and they are answered with different tools.") +
        table(["Question", "What you measure", "How"], [
            ["How fast does the compiler run?", "wall-clock time per phase",
             "the timing table the driver already prints"],
            ["How fast does the compiled code run?", "instructions executed",
             "SPIM's instruction count, optimized vs unoptimized"],
            ["How big is the compiled code?", "TAC and MIPS instruction counts",
             "the optimizer's own scorecard"],
        ]) +
        h3("Compilation time") +
        p("The driver already reports it. Run it on inputs of several sizes and look "
          "at the SHAPE of the curve, not one number:") +
        code("""  Compilation time by phase
    1. Lexical + syntax analysis      0.07 ms
    2. AST construction               0.00 ms
    3. Semantic analysis              0.10 ms
    4. Intermediate code (TAC)        0.65 ms
    5. Optimization                   0.33 ms
    6. MIPS code generation           0.36 ms
    TOTAL                             1.55 ms""") +
        note("note", "The question worth asking about that table",
             p("Which phase grows fastest as the input grows? Compile a 10-line, a "
               "100-line and a 1000-line program and plot it. Most phases here are "
               "linear in program size. The optimizer is not — it runs to a fixed "
               "point, and <code>isReadLater()</code> scans forward from every "
               "instruction, which makes dead-code elimination quadratic. Finding that "
               "yourself, in your own compiler, is a much better write-up than "
               "repeating that optimization is expensive.")) +
        h3("Execution time") +
        p("Instruction count is the right metric here — it is deterministic, and SPIM "
          "is not a timing-accurate simulator, so wall-clock numbers from it mean very "
          "little.") +
        code("""  # optimized vs unoptimized, same source
  TAC instructions       48 -> 31       35.4% smaller
  MIPS instructions     112 -> 74       33.9% smaller
  Instructions executed  8,431 -> 5,102 39.5% fewer""") +
        p("Report all three. They will not agree, and the disagreement is informative: "
          "code size and work done diverge exactly in proportion to how much of the "
          "removed code was inside a loop.") +

        h2("Honest measurement") +
        p("Three rules that separate a number you can defend from a number you cannot:") +
        ol([
            "<b>Repeat the run.</b> Three times, minimum. If the spread is 8%, then a "
            "5% improvement is not a result.",
            "<b>Say what you compared.</b> 'Optimized vs unoptimized, same source, same "
            "machine, same simulator' — not 'my compiler is 30% faster', which is faster "
            "than what?",
            "<b>Report the benchmark.</b> A speedup on a program with a hot loop tells "
            "you about hot loops. Include the source you measured.",
        ]) +
        quiz("Your optimizer reports 35% fewer TAC instructions, but SPIM reports only "
             "4% fewer instructions executed. What is the most likely explanation?",
             [("The optimizer is broken", False,
               "Possible, but a broken optimizer usually produces wrong ANSWERS, not "
               "disappointing ratios. Check correctness separately."),
              ("Most of what it removed was setup code that runs once, while the hot "
               "loop was untouched", True,
               "Exactly. Code size counts each instruction once; execution counts it "
               "per iteration. Removing 17 instructions of straight-line setup saves 17 "
               "executions. Removing one instruction from a loop running 300 times "
               "saves 300. This is the single most important thing to understand about "
               "optimization measurement."),
              ("SPIM's instruction count is unreliable", False,
               "It is deterministic and exact. It is wall-clock time that SPIM cannot "
               "tell you anything useful about."),
              ("The MIPS back end undid the optimizations", False,
               "It cannot — it consumes the optimized TAC. Though it is worth checking "
               "that it really does; pointing it at the unoptimized list by mistake is "
               "a real bug people hit.")]) +

        h2("Knowing your own limits") +
        p("Every compiler has them. Being able to list your own — precisely, with the "
          "reason — is worth more in a viva than pretending there are none. Here are "
          "the ones this design has. Verify each on your own build; some of yours will "
          "differ.") +
        table(["Limit", "Why it exists", "What it would take to lift"], [
            ["At most 4 arguments per call",
             "arguments are passed only in $a0–$a3",
             "push the rest on the stack; decide who pops them"],
            ["No bounds checking on arrays",
             "no size information survives to run time",
             "pass a length with every array, or store it before element 0"],
            ["<code>int</code> is the only type",
             "the type is never recorded past the declaration",
             "a real type field in the symbol table, and type rules in phase 3"],
            ["Registers flushed at every branch",
             "the allocator does not track liveness across blocks",
             "a control-flow graph and live-variable analysis"],
            ["Optimizer forgets everything at a label",
             "no analysis across basic blocks",
             "the same CFG; then reaching-definitions"],
            ["Identifiers <code>t0</code>, <code>L0</code> are reserved",
             "they collide with generated names",
             "prefix generated names with a character the scanner cannot produce"],
        ]) +
        note("key", "This table is the answer to Lab Question 29",
             p("'Three things you would do differently' is not a confession, it is a "
               "design review. Pick one from the compiler's architecture, one from the "
               "language's features, and one from your implementation — and for each, "
               "say what it would have cost to do differently and why you did not.")) +

        h2("What a README has to contain") +
        p("Somebody who has never seen your compiler must be able to build and run it "
          "from your README alone. That is the whole test.") +
        tabs([
            ("required", code("""# <name> — a compiler for <language>

## What it does
One paragraph. What language it accepts, what it emits.

## Requirements
flex 2.6+, bison 2.3+ (or byacc), gcc, SPIM or QtSPIM
Tested on: <your OS and versions>

## Build
    make

## Run
    ./minicompiler input.cm output.s
    spim -file output.s

## The language
The grammar, in BNF. Every construct with one example.

## How it works
The six phases, one paragraph each, naming the file.

## Performance
The measurement table. Say what you compared and on what.

## Known limitations
The honest list. Each with a reason.

## Team
Who wrote which phase.""")),
            ("what makes one bad", code("""No exact build command       "just run make" is fine; "compile the
                             files" is not

No versions                  bison 2.3 and bison 3.x differ in ways
                             that break grammars. Say which you used.

No example input             a README with no runnable example cannot
                             be verified by the reader

Limitations section absent   the reader concludes you did not look

Performance with no baseline "30% faster" — than what?""")),
        ]) +

        h2("The video") +
        p("Each team member records their own. The rubric asks for the compiler "
          "working, plus decisions about language design and implementation approach. "
          "A structure that works:") +
        ol([
            "<b>Show it run</b> (60s). A non-trivial program, compiled, then executed "
            "in SPIM. Start here — everything after this is commentary on something the "
            "viewer has already seen work.",
            "<b>Follow one construct through all six phases</b> (3–4 min). Pick "
            "something with structure — a loop or a switch — and show it as source, "
            "tokens, AST, TAC, optimized TAC, and MIPS. This is the single most "
            "convincing thing you can do.",
            "<b>Your part</b> (2 min). Which phases you wrote, and one problem you had "
            "to solve, with the code on screen.",
            "<b>A decision you made</b> (2 min). Short-circuit or eager? Jump table or "
            "linear chain? Desugar <code>for</code> or lower it directly? Say what you "
            "chose and what would change your mind.",
            "<b>Numbers and limits</b> (1–2 min). The measurement table, and two "
            "limitations with reasons.",
        ]) +
        note("warn", "The failure mode to avoid",
             p("Reading the code aloud. The viewer can read. What they cannot get from "
               "the repository is WHY it is shaped that way — which alternatives you "
               "considered, what broke, what you would do differently. Ten minutes of "
               "that is worth an hour of narration.")) +

        h2("A last look back") +
        p("Fifteen weeks ago the scanner returned a token. Everything since has been "
          "the same move repeated: choose a representation, define what the phase "
          "before must hand you, and translate. The compiler is now about 3,000 lines. "
          "Roughly 85% of it does not know what machine it targets, and that is the "
          "part worth being proud of.") +
        reveal("If you want to keep going",
               ul(["<b>Types.</b> Add <code>bool</code> or <code>float</code>. The "
                   "work is almost entirely in phase 3, and it will show you why real "
                   "compilers have a type system rather than a type field.",
                   "<b>A control-flow graph.</b> Build one from the TAC. Then "
                   "liveness, then register allocation by graph colouring — the "
                   "textbook path, and each step is visibly better than what you have.",
                   "<b>An ARM back end.</b> You already know it is one file.",
                   "<b>LLVM IR instead of MIPS.</b> Emit textual LLVM from your TAC "
                   "and let <code>clang</code> do the rest. Two hundred lines, and "
                   "suddenly your language runs natively on any machine LLVM targets."])) +

        h2("Where the code lives") +
        p("<code>student/topic-6-complete-compiler/compiler/</code> — the same "
          "compiler, with the full test suite. Nothing is removed this topic; "
          "<code>tests/t6_06_everything.cm</code> exercises every feature at once, and "
          "<code>tests/t6_07_benchmark.cm</code> is a starting point for your "
          "measurements.")
    )


def _a1():
    return (
        meta([("Format", "pairs"), ("Time", "50 min"), ("Need", "SPIM and your compiler")]) +
        h2("The point") +
        p("Produce the performance section of your Benchmark submission, with numbers "
          "you could defend to somebody who wanted to disagree.") +
        h2("Do this") +
        steps_list([
            "<b>Pick three benchmarks</b> of different shapes: one straight-line "
            "arithmetic program, one with a hot nested loop, one heavy on function "
            "calls (recursion is good). Each should run long enough to give a "
            "six-figure instruction count.",
            "<b>Compilation time.</b> For each, record the per-phase timing table. "
            "Then make a 10×-longer version of one benchmark and record it again. Which "
            "phase grew fastest? Is anything super-linear?",
            "<b>Code size.</b> Record TAC instructions before and after optimization, "
            "and MIPS instruction count, for all three.",
            "<b>Work done.</b> Run each in SPIM, optimized and unoptimized, and record "
            "instructions executed. To get an unoptimized <code>.s</code>, temporarily "
            "point <code>generateMIPSFromTAC</code> at <code>getUnoptimizedTAC()</code>.",
            "<b>Repeat three times</b> and record the spread.",
            "<b>Build the table</b> and write three sentences: what you measured, what "
            "you compared it to, and what the numbers show. Then one more sentence on "
            "where they disagree and why.",
        ]) +
        note("note", "Where to look if a number surprises you",
             p("The register allocator reports spills and reloads. A benchmark with far "
               "more executed instructions than you expected usually has a spill inside "
               "the hot loop — which is a real finding, and a good thing to put in your "
               "write-up.")) +
        deliverable(p("A performance table covering all three benchmarks with all four "
                      "metrics, the repeated-run spread, the benchmark sources, and "
                      "your four sentences. This IS the performance section of Project "
                      "6 — write it once, well.")))


def _a2():
    return (
        meta([("Format", "groups of three"), ("Time", "50 min"),
              ("Bring", "a draft README and a laptop you can wipe")]) +
        h2("The point") +
        p("Two things get checked here, and both are checked by somebody who is not "
          "you: can a stranger build your compiler, and can you explain it out loud.") +
        h3("Part 1 — the cold-start README test (25 min)") +
        steps_list([
            "<b>Swap repositories.</b> Clone a group member's compiler into a fresh "
            "directory. Do not ask them anything.",
            "<b>Follow their README literally.</b> Every place you had to guess, "
            "improvise, or ask — write it down. Those are bugs in the README.",
            "<b>Score it.</b> Could you build it? Could you run it on your own input "
            "file? Could you find out what the language accepts without reading "
            "<code>parser.y</code>? Did the limitations section tell you anything you "
            "then confirmed?",
            "<b>Hand back your list.</b> Fix your own README before you leave.",
        ]) +
        h3("Part 2 — the demo dry run (25 min)") +
        p("Eight minutes each, to the other two, following the structure in the lecture "
          "notes. The audience's only job is to interrupt with <i>why</i>.") +
        steps_list([
            "<b>Show it run</b> before you explain anything.",
            "<b>Follow one construct through all six phases.</b> Have the files open "
            "already; do not spend demo time navigating.",
            "<b>Name a decision and defend it.</b> The audience should push back once.",
            "<b>Give two limitations with reasons.</b>",
            "<b>Audience feedback:</b> one thing that was convincing, one thing that "
            "was not, one question you would have asked if there were time.",
        ]) +
        note("note", "The most common demo mistake",
             p("Explaining for six minutes and demonstrating for one. Lead with the "
               "working program. Everything after it lands differently once the viewer "
               "has seen the thing actually work.")) +
        deliverable(p("The list of README problems you found in someone else's, the "
                      "list they found in yours, and your fixed README. Plus your "
                      "written notes from the demo feedback — those go straight into "
                      "your recorded video.")))


ACTIVITIES = [
    dict(slug="benchmark-your-compiler", session="Week 15 · Wednesday",
         title="Benchmark Your Compiler",
         lede="Three benchmarks, four metrics, three repeated runs — and a number you could defend to a sceptic.",
         body=_a1),
    dict(slug="cold-start-and-demo", session="Week 15 · Friday",
         title="Cold-Start README Test and Demo Dry Run",
         lede="Somebody who has never seen your compiler tries to build it. Then you explain it out loud and they interrupt.",
         body=_a2),
]
