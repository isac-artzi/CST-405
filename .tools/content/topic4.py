"""Topic 4 — Compiling Loops (and making optimization pay)."""

from docgen import (code, pipeline, tabs, stepper, reveal, quiz, note, table,
                    steps_list, p, h2, h3, h4, ul, ol, deliverable, meta)

LECTURE_TITLE = "Loops, Labels, and What Optimization Is Actually Worth"
LECTURE_LEDE = ("Structured control flow becomes labels and jumps — and then the optimizer "
                "stops being a lecture topic and starts producing numbers you can quote.")


def lecture():
    return (
        h2("There are no loops in a machine") +
        p("A CPU has exactly two control-flow instructions: jump somewhere, and jump "
          "somewhere <i>if</i> a register is zero. Every <code>while</code>, "
          "<code>for</code>, <code>if</code> and <code>switch</code> in every language "
          "you have used is a pattern of those two. Building them is called "
          "<b>lowering</b>, and it happens in phase 4.") +
        pipeline(active=3, done=(0, 1, 2)) +
        code("""    while (c) B                    for (init; c; upd) B
    ───────────                    ────────────────────
                                     <init>
  Lstart:                          Lstart:
      t = <c>                          t = <c>
      IF_FALSE t GOTO Lend             IF_FALSE t GOTO Lend
      <B>                              <B>
      GOTO Lstart                      <upd>
  Lend:                                GOTO Lstart
                                   Lend:""") +
        p("Read those two side by side. A <code>for</code> loop is a <code>while</code> "
          "loop with two extra pieces bolted on, which is why many compilers desugar "
          "<code>for</code> into <code>while</code> in the front end and reuse one "
          "lowering. Either approach is fine; be able to say which you chose and why.") +

        h2("Watch a loop lower") +
        stepper([
            ("The source. Three lines that will become eleven instructions.",
             code("""i = 0;
while (i < 3) {
    print(i);
    i = i + 1;
}""")),
            ("Anything before the loop is emitted first, unchanged.",
             code(">>>i = 0")),
            ("A label marks the top. Every iteration will come back here.",
             code("""i = 0
>>>Lstart:""")),
            ("The condition is an ordinary expression, so it produces a temporary "
             "holding 1 or 0.",
             code("""i = 0
Lstart:
>>>    t0 = i < 3""")),
            ("The test. This is the ONLY thing that makes it a loop rather than a "
             "straight line.",
             code("""i = 0
Lstart:
    t0 = i < 3
>>>    IF_FALSE t0 GOTO Lend""")),
            ("The body, lowered normally. Nothing about it knows it is inside a loop.",
             code("""i = 0
Lstart:
    t0 = i < 3
    IF_FALSE t0 GOTO Lend
>>>    PRINT i
>>>    t1 = i + 1
>>>    i = t1""")),
            ("The jump back, and the exit label. Done.",
             code("""i = 0
Lstart:
    t0 = i < 3
    IF_FALSE t0 GOTO Lend
    PRINT i
    t1 = i + 1
    i = t1
>>>    GOTO Lstart
>>>Lend:""")),
        ]) +
        note("key", "Test at the top, not the bottom",
             p("The condition is evaluated BEFORE the body, so a loop whose condition "
               "is false initially executes zero times. That is what "
               "<code>while</code> means. Emit the test at the bottom instead and you "
               "have accidentally implemented <code>do-while</code> — a real language, "
               "but not the one you documented.")) +

        h2("break is a stack, and that is the whole implementation") +
        p("<code>break</code> means <i>jump to the exit label of the innermost thing I "
          "am inside</i>. The compiler does not need to analyse anything to work that "
          "out: when it starts lowering a loop it pushes that loop's exit label, and "
          "when it finishes it pops. A <code>break</code> anywhere in between emits a "
          "jump to whatever is on top.") +
        code("""    push Lend_outer
        push Lend_inner
            break;      ->   GOTO Lend_inner      (top of stack)
        pop
        break;          ->   GOTO Lend_outer      (top of stack now)
    pop""") +
        p("Nesting falls out for free. So does the error case: if the stack is empty "
          "when a <code>break</code> is lowered, the program had a <code>break</code> "
          "outside any loop — and the semantic analyzer should already have said so, "
          "with a line number, using the same idea as a depth counter.") +
        quiz("Where should 'break outside a loop' be reported?",
             [("The parser — it is a syntax error", False,
               "No grammar can express it. The grammar says <code>break_stmt : BREAK "
               "';'</code>, which is satisfied wherever the statement appears."),
              ("The semantic analyzer — it is context-sensitive", True,
               "Right, and it is the smallest possible example of a context-sensitive "
               "rule: whether the statement is legal depends entirely on what encloses "
               "it. That is precisely the territory no context-free grammar can reach."),
              ("The TAC generator — that is where the label stack lives", False,
               "It CAN detect it there, and ours does as a backstop. But by then you "
               "have lost the line number, and an error with no location is barely an "
               "error."),
              ("The code generator", False,
               "Far too late. By phase 6 the program has been through four "
               "transformations and the connection to source text is gone.")]) +

        h2("Now the optimizer earns its keep") +
        pipeline(active=4, done=(0, 1, 2, 3)) +
        p("Until this topic, optimization was a formality — straight-line code has "
          "little to remove. Loops change that, because an instruction inside a loop "
          "that runs 1,000 times costs 1,000 instructions.") +
        h3("The techniques, in the order a pass applies them") +
        table(["Technique", "Before", "After", "Why it is safe"], [
            ["Algebraic simplification", "<code>t = x + 0</code>", "<code>t = x</code>",
             "true for every integer x"],
            ["Constant folding", "<code>t = 2 * 3</code>", "<code>t = 6</code>",
             "both operands are literals"],
            ["Constant propagation", "<code>x = 5; y = x + 1</code>",
             "<code>x = 5; y = 5 + 1</code>", "x provably holds 5 at that point"],
            ["Copy propagation", "<code>t1 = x; y = t1</code>", "<code>y = x</code>",
             "t1 is only a copy"],
            ["Dead code elimination", "<code>t0 = a + b</code> (never read)", "—",
             "no later instruction reads t0"],
            ["Unreachable code", "code after <code>GOTO</code>", "—",
             "control can never arrive"],
            ["Branch simplification", "<code>IF_FALSE 0 GOTO L</code>",
             "<code>GOTO L</code>", "the condition is a known constant"],
        ]) +
        h3("Why one pass is not enough") +
        p("The techniques feed each other. Watch three passes turn six instructions "
          "into two:") +
        tabs([
            ("original", code("""t0 = 2 * 3
x  = t0
t1 = x + 0
y  = t1
t2 = y * 1
print t2""")),
            ("after pass 1", code(""">>>t0 = 6            folded
x  = 6            propagated
>>>t1 = x            algebraic (x + 0)
y  = x
t2 = y            algebraic (y * 1)
print t2""")),
            ("after pass 2", code("""x = 6
y = 6             propagated through the copies
t2 = 6
print 6           propagated into the print""")),
            ("after pass 3", code(""">>>print 6            everything else was dead

no changes on pass 4 — fixed point reached""")),
        ]) +
        p("This is why <code>optimizeTAC</code> loops until a pass reports zero "
          "changes. Running to a <b>fixed point</b> is how real optimizers are "
          "structured, and it is why the order of techniques within a pass matters "
          "less than you would expect.") +
        note("warn", "The safety rule you must not break",
             p("At a LABEL, forget every value you thought you knew. Control can arrive "
               "at a label from anywhere, so a fact established on one path is not a "
               "fact on another. Propagate a constant across a loop back-edge and you "
               "will produce a compiler that is correct on straight-line code and "
               "silently wrong on loops — the worst possible failure mode, because the "
               "tests you wrote in Topic 2 still pass.")) +

        h2("Measuring it") +
        p("Topic 4 asks you to <i>quantify</i> the gain. Two numbers are available and "
          "they measure different things:") +
        table(["Metric", "Where to get it", "What it tells you"], [
            ["TAC instruction count", "the optimizer's own report",
             "how much smaller the program got"],
            ["Executed instruction count", "SPIM's statistics after a run",
             "how much less work it actually does"],
        ]) +
        p("They can diverge sharply. Removing one instruction from inside a loop that "
          "runs 300 times shrinks the code by one and the execution by 300. Removing "
          "twenty instructions of setup code that runs once shrinks the code by twenty "
          "and the execution by twenty. Say which you measured.") +
        code("""    # code size, from the compiler's own report
    TAC instructions   48 -> 31  (17 removed, 35.4% smaller)

    # work done, from SPIM
    spim -file bench.s
    # (QtSPIM shows an instruction count; spim -exception_file ... likewise)""") +
        reveal("What counts as a significant gain?",
               p("Lab Question 22 asks you to say, with reference to your own machine. "
                 "Some anchors: a 5% reduction is inside the noise of most measurement "
                 "setups and you should not claim it without repeating the run. A 30% "
                 "reduction in executed instructions is a real result. A 10× result "
                 "usually means you removed something that should not have been "
                 "generated in the first place — which is a fine outcome, but the "
                 "honest report says so rather than crediting the optimizer.")) +
        h2("Two more techniques worth discussing (Lab Questions 21)") +
        h3("Loop unrolling") +
        code("""    for (i = 0; i < 4; i = i + 1)      s = s + a[0];
        s = s + a[i];              ->      s = s + a[1];
                                           s = s + a[2];
                                           s = s + a[3];""") +
        p("Removes four condition tests and four jumps, at the cost of four times the "
          "code. Worth it when the trip count is small and known; harmful when the "
          "loop body no longer fits in the instruction cache. Note that it requires "
          "knowing the trip count at compile time — which is why it pairs so naturally "
          "with constant propagation.") +
        h3("Strength reduction") +
        p("Replace an expensive operation with a cheap one that computes the same "
          "thing: <code>i * 4</code> becomes <code>i << 2</code>; a multiply inside a "
          "loop becomes an add on each iteration. Your array indexing already does the "
          "first one — find it in <code>elementAddrReg</code>.") +
        h2("Where the code lives") +
        p("<code>student/topic-4-loops/compiler/</code>. It is your working Topic 3 "
          "compiler; the TODOs cover the scanner, the grammar, two AST nodes, the "
          "break-depth check, the lowering, the branch codegen, and the branch "
          "simplification pass. The Topic 3 tests must still pass when you are done.")
    )


def _a1():
    return (
        meta([("Format", "pairs"), ("Time", "45 min"), ("Bring", "paper")]) +
        h2("The point") +
        p("Lower a loop by hand before you write the code that does it. The pattern is "
          "short enough to memorise and general enough to reuse for the rest of the "
          "course.") +
        h2("Do this") +
        steps_list([
            "<b>Lower this by hand</b> into TAC with labels and jumps:"
            + code("""i = 0;
s = 0;
while (i < 5) {
    s = s + i;
    i = i + 1;
}
print(s);"""),
            "<b>Hand-execute it.</b> Make a table with columns for <code>i</code>, "
            "<code>s</code>, and the instruction number. Step through until it "
            "terminates. What does it print?",
            "<b>Move the test to the bottom</b> — emit the body first, then the "
            "condition, then a conditional jump BACK to the top. Hand-execute again "
            "with <code>i = 5</code> initially. What changed? What language construct "
            "did you just implement?",
            "<b>Nest two loops</b> on paper. How many distinct labels do you need? "
            "What breaks if the label generator returns the same name twice?",
            "<b>Now implement it</b> — the <code>NODE_WHILE</code> case in "
            "<code>tac.c</code> — and compare the compiler's output with your "
            "handwritten listing.",
        ]) +
        deliverable(p("Your handwritten lowering, the execution trace table, your "
                      "answer to step 3 naming the construct, and the compiler's "
                      "<code>.tac</code> next to your version. Feeds Lab Question 17.")))


def _a2():
    return (
        meta([("Format", "pairs, at a laptop"), ("Time", "50 min")]) +
        h2("The point") +
        p("<code>for</code> is a design decision, not a feature. Make it deliberately.") +
        h2("Do this") +
        steps_list([
            "<b>Two implementations, on paper.</b> (a) Lower <code>for</code> directly, "
            "with its own case in <code>generateTACStmt</code>. (b) Desugar it in the "
            "parser: build a <code>NODE_WHILE</code> whose body is "
            "<code>{ B; upd; }</code>, preceded by <code>init</code>. Write the TAC "
            "each approach produces for the same loop.",
            "<b>Compare the two listings.</b> Are they identical? If not, which is "
            "shorter, and does the difference survive optimization?",
            "<b>Decide the awkward cases</b> before you code. What does your language "
            "do for each of these, and is it a parse error or a legal program?"
            + code("""for (; i < 5; i = i + 1) ...     no init
for (i = 0; ; i = i + 1) ...     no condition
for (i = 0; i < 5; ) ...         no update
for (;;) ...                     nothing at all"""),
            "<b>Implement your choice.</b> Then write a test file that exercises all "
            "four cases above and confirm each behaves as you decided.",
            "<b>Argue.</b> In two sentences: which implementation would you ship, and "
            "what would change your mind?",
        ]) +
        note("note", "There is no wrong answer to step 5",
             p("Desugaring keeps the back end smaller and guarantees the two loop forms "
               "cannot drift apart. A dedicated case keeps the TAC readable and lets "
               "you optimize <code>for</code> specifically later. Real compilers do "
               "both. What matters is that you can say which you did and why.")) +
        deliverable(p("Both TAC listings from step 1, your decision table for the four "
                      "degenerate forms, a working implementation, and your two-sentence "
                      "argument. Feeds Lab Question 18.")))


def _a3():
    return (
        meta([("Format", "pairs"), ("Time", "45 min")]) +
        h2("The point") +
        p("<code>break</code> looks trivial and is the first construct whose meaning "
          "depends on context rather than on its own text.") +
        h2("Do this") +
        steps_list([
            "<b>Predict the target</b> of each <code>break</code> below, then implement "
            "the break-label stack and check."
            + code("""while (a) {
    while (b) {
        break;        <- which loop does this leave?
    }
    break;            <- and this one?
}"""),
            "<b>Implement the semantic check.</b> A <code>break</code> outside any loop "
            "must be an error with a line number. Use a depth counter incremented "
            "around loop BODIES only — not around loop conditions. Explain why the "
            "condition is excluded.",
            "<b>Test the error.</b> Write a file with a top-level <code>break;</code> "
            "and confirm the message names the line.",
            "<b>Design <code>continue</code>.</b> You do not have to implement it. On "
            "paper: what label would it jump to in a <code>while</code>? In a "
            "<code>for</code>? The answers differ, and the difference is the reason "
            "<code>continue</code> in a <code>for</code> loop surprises people.",
            "<b>Design labelled break.</b> Java has <code>break outer;</code>. What "
            "would that require of your label stack? Two sentences.",
        ]) +
        reveal("On step 4",
               p("In a <code>while</code>, <code>continue</code> jumps to the top — the "
                 "same label the back-edge targets. In a <code>for</code>, it must jump "
                 "to the UPDATE, not the top, or the loop variable never advances and "
                 "you have written an infinite loop. This is why <code>for</code> needs "
                 "its own continue label even if you desugared it into a "
                 "<code>while</code>.")) +
        deliverable(p("Your predictions, a working break with a working error message, "
                      "and written answers to steps 4 and 5.")))


def _a4():
    return (
        meta([("Format", "pairs"), ("Time", "50 min"), ("Bring", "paper")]) +
        h2("The point") +
        p("Optimize a listing by hand, to a fixed point, before you trust a program to "
          "do it. You will find at least one transformation you would have got wrong.") +
        h2("Do this") +
        steps_list([
            "<b>By hand, pass by pass.</b> Optimize this listing. Write out each pass "
            "separately and label every change with the technique that made it."
            + code(""" 1: t0 = 4 * 5
 2: n  = t0
 3: t1 = n + 0
 4: m  = t1
 5: t2 = m * 1
 6: k  = t2
 7: t3 = 7 - 7
 8: IF_FALSE t3 GOTO L1
 9: PRINT 999
10: L1:
11: PRINT k"""),
            "<b>Keep going until nothing changes.</b> How many passes did it take? "
            "How many instructions are left?",
            "<b>Now the compiler.</b> Put an equivalent program through it and compare "
            "<code>out.tac</code> with <code>out.optimized.tac</code>. Read the "
            "technique scorecard the optimizer prints.",
            "<b>Find a disagreement</b> — either something you did that the compiler "
            "did not, or the reverse. Explain it. (There is at least one: the compiler "
            "will not eliminate a dead store to a user VARIABLE, only to a temporary. "
            "Why is that restriction there?)",
            "<b>Break the safety rule.</b> Remove the <code>clearFacts()</code> call at "
            "<code>TAC_LABEL</code>. Then compile a loop that changes a variable, and "
            "run it. Describe the wrong answer and explain precisely which assumption "
            "failed.",
        ]) +
        note("warn", "Step 5 is the important one",
             p("It produces a compiler that passes every straight-line test you have "
               "written and is silently wrong on loops. That failure mode — correct on "
               "the tests, wrong in reality — is the reason optimizer bugs have a "
               "reputation.")) +
        deliverable(p("Your pass-by-pass hand optimization with every change labelled, "
                      "the compiler's scorecard, your explanation of the disagreement, "
                      "and a description of the step-5 failure. Feeds Lab Questions 19 "
                      "and 20.")))


def _a5():
    return (
        meta([("Format", "pairs, at a laptop"), ("Time", "50 min"),
              ("Need", "SPIM, and your machine's specs")]) +
        h2("The point") +
        p("Produce a number you would be willing to defend. Most reported speedups do "
          "not survive the question <i>compared to what, measured how?</i>") +
        h2("Do this") +
        steps_list([
            "<b>Write a benchmark</b> with a hot loop — a nested loop running a few "
            "thousand iterations. <code>tests/t6_07_benchmark.cm</code> is a starting "
            "point if you want one.",
            "<b>Get the code-size numbers.</b> Compile it and record the TAC "
            "instruction count before and after optimization, plus the per-technique "
            "scorecard.",
            "<b>Get the work-done numbers.</b> Run both versions in SPIM and record "
            "the executed instruction count for each. To get an unoptimized "
            "<code>.s</code>, temporarily point <code>generateMIPSFromTAC</code> at "
            "<code>getUnoptimizedTAC()</code>.",
            "<b>Put the four numbers in a table</b> and compute both percentages. They "
            "will not match. Explain the gap in one sentence.",
            "<b>Repeat the run three times.</b> How much do the numbers move? Anything "
            "smaller than that spread is not a result.",
            "<b>State a threshold.</b> Given your machine and your measurement noise, "
            "what reduction would you call significant? Justify it with the numbers "
            "from step 5, not with a feeling.",
        ]) +
        deliverable(p("A results table with all four numbers and both percentages, "
                      "three repeated runs, your noise estimate, and a defended "
                      "threshold. This is Lab Question 22 and a large part of the "
                      "Project 6 performance section — do it properly now and reuse it "
                      "in December.")))


def _a6():
    return (
        meta([("Format", "pairs"), ("Time", "45 min")]) +
        h2("The point") +
        p("Two optimizations you will not implement, done by hand, so you can talk "
          "about them accurately.") +
        h2("Do this") +
        steps_list([
            "<b>Unroll by hand.</b> Take"
            + code("for (i = 0; i < 4; i = i + 1) { s = s + a[i]; }")
            + "and write both the normal lowering and a fully unrolled version. Count "
            "the instructions in each, and count how many EXECUTE in each.",
            "<b>Partial unrolling.</b> Now unroll by 2 rather than fully. Write it. "
            "What has to be true about the trip count for this to be correct, and what "
            "extra code is needed when it is not?",
            "<b>When does unrolling lose?</b> Change the loop to 10,000 iterations and "
            "reason about it. Name two costs.",
            "<b>Strength reduction.</b> The array index does "
            "<code>i * 4</code> every iteration. Rewrite the loop to keep a running "
            "address and add 4 each time instead. Count the instructions saved per "
            "iteration.",
            "<b>Find it in the compiler.</b> One strength reduction is already there: "
            "<code>sll $t, $t, 2</code> instead of a multiply. Locate it in "
            "<code>codegen.c</code> and say why the compiler can always do that one "
            "safely.",
        ]) +
        reveal("On step 3",
               p("Code size, and instruction-cache pressure. A loop body that fitted in "
                 "cache may not after unrolling, and a cache miss costs far more than "
                 "the compare-and-branch you removed. This is why unrolling decisions "
                 "in real compilers are driven by measured heuristics and not by a "
                 "rule.")) +
        deliverable(p("Both unrolled listings with instruction counts, your answer on "
                      "partial unrolling, two named costs, the strength-reduced loop, "
                      "and the line number of the existing strength reduction. Feeds "
                      "Lab Question 21.")))


ACTIVITIES = [
    dict(slug="lower-a-loop", session="Week 9 · Wednesday",
         title="Lower a Loop by Hand",
         lede="Labels and jumps on paper, then hand-execute it, then move the test to the bottom and see what you built.",
         body=_a1),
    dict(slug="for-vs-while", session="Week 9 · Friday",
         title="for vs while — a Design Decision",
         lede="Lower it directly or desugar it? Write both, decide the degenerate cases, then defend your choice.",
         body=_a2),
    dict(slug="break-and-continue", session="Week 10 · Wednesday",
         title="break, and the continue You Are Not Implementing",
         lede="A label stack, a depth counter, and why continue in a for loop surprises people.",
         body=_a3),
    dict(slug="optimize-by-hand", session="Week 10 · Friday",
         title="Optimize a Listing by Hand",
         lede="Pass by pass to a fixed point, then break the label safety rule and see the failure mode.",
         body=_a4),
    dict(slug="measure-it", session="Week 11 · Wednesday",
         title="Measure It, and Defend the Number",
         lede="Code size and work done are different numbers. Get both, repeat the run, and state a threshold you can justify.",
         body=_a5),
    dict(slug="unrolling-and-strength-reduction", session="Week 11 · Friday",
         title="Unrolling and Strength Reduction",
         lede="Two optimizations you will not implement, done by hand so you can talk about them accurately.",
         body=_a6),
]
