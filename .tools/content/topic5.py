"""Topic 5 — Compiling Control Flow: Decisions."""

from docgen import (code, pipeline, tabs, stepper, reveal, quiz, note, table,
                    steps_list, p, h2, h3, h4, ul, ol, deliverable, meta)

LECTURE_TITLE = "Decisions, the Dangling Else, and switch"
LECTURE_LEDE = ("if and else are two rules and one famous ambiguity. switch is one rule and one "
                "genuinely interesting code-generation choice.")


def lecture():
    return (
        h2("if is the loop you already wrote, without the back edge") +
        pipeline(active=3, done=(0, 1, 2)) +
        code("""    if (c) T                       if (c) T else E
    ────────                       ───────────────
        t = <c>                        t = <c>
        IF_FALSE t GOTO Lend           IF_FALSE t GOTO Lelse
        <T>                            <T>
    Lend:                              GOTO Lend
                                   Lelse:
                                       <E>
                                   Lend:""") +
        p("If you built loops in Topic 4, you have already written every mechanism "
          "this needs. Which is the point: the fourth construct you lower is much "
          "cheaper than the first, and that is what the layered structure of this "
          "course was for.") +
        note("key", "The one thing to get right",
             p("The <code>GOTO Lend</code> at the end of the then-branch. Leave it out "
               "and control falls from the then-branch straight into the else-branch, "
               "so both run. The program still compiles, still runs, and is wrong in a "
               "way that a test with a false condition will not catch.")) +

        h2("The dangling else") +
        p("This is the most famous ambiguity in programming languages, and your grammar "
          "has it right now whether or not you have noticed.") +
        code("""    if (a) if (b) X else Y

    reading 1:   if (a) { if (b) X else Y }        <- else belongs to the INNER if
    reading 2:   if (a) { if (b) X } else Y        <- else belongs to the OUTER if""") +
        p("Both are valid derivations from the obvious grammar. They mean different "
          "things: with <code>a</code> true and <code>b</code> false, reading 1 runs "
          "<code>Y</code> and reading 2 runs nothing.") +
        p("Every mainstream language picks reading 1 — <b>else binds to the nearest "
          "if</b>. Bison, left alone, also picks reading 1, because when it must choose "
          "between shifting the <code>ELSE</code> and reducing the inner "
          "<code>if</code>, it shifts. So the default is already correct. What is not "
          "correct is leaving a shift/reduce conflict in your grammar and hoping.") +
        tabs([
            ("the conflict", code("""$ bison -d parser.y
parser.y: warning: 1 shift/reduce conflict

# bison resolved it by shifting, which happens to be what you wanted.
# It will resolve the NEXT one by shifting too — including the one you
# did not want. A grammar with unexplained conflicts is a grammar you
# have stopped reading.""")),
            ("the fix", code("""%nonassoc LOWER_THAN_ELSE   /* a pseudo-token, lower precedence */
%nonassoc ELSE              /* declared later, so higher       */

if_stmt : IF '(' expr ')' stmt %prec LOWER_THAN_ELSE
        | IF '(' expr ')' stmt ELSE stmt
        ;""")),
            ("what it says", code("""The rule  IF '(' expr ')' stmt  is given LOWER precedence
than the token ELSE.

So when the parser is sitting on a complete
    IF '(' expr ')' stmt
and the lookahead is ELSE, it compares:

    reduce using this rule   (precedence: LOWER_THAN_ELSE)
    shift the ELSE           (precedence: ELSE, which is higher)

Higher wins -> SHIFT -> the else attaches to the inner if.
Same outcome as the default, but now it is DECLARED, and
bison reports no conflict.""")),
        ]) +
        quiz("Why must <code>%nonassoc LOWER_THAN_ELSE</code> be written BEFORE "
             "<code>%nonassoc ELSE</code>?",
             [("Alphabetical order is required by bison", False,
               "Bison has no such requirement. The order carries meaning."),
              ("Later declarations have HIGHER precedence, and ELSE must outrank the rule", True,
               "Exactly. Precedence in bison is positional: each successive "
               "<code>%left</code>/<code>%right</code>/<code>%nonassoc</code> line "
               "binds tighter than the one above. Swap these two and ELSE becomes "
               "lower, the parser reduces instead of shifting, and every else binds "
               "to the OUTER if."),
              ("LOWER_THAN_ELSE is a real token that must be declared first", False,
               "It is a pseudo-token — it is never returned by the scanner. It exists "
               "solely to occupy a slot in the precedence table."),
              ("It does not matter; %prec overrides the order", False,
               "<code>%prec</code> says WHICH precedence the rule takes. The order of "
               "the declarations is what gives those precedences their values.")]) +

        h2("Boolean operators, and the decision you are making by accident") +
        p("<code>&amp;&amp;</code> and <code>||</code> have a property that "
          "<code>+</code> does not: in most languages they <b>short-circuit</b>. "
          "<code>a &amp;&amp; b</code> does not evaluate <code>b</code> when "
          "<code>a</code> is false.") +
        tabs([
            ("eager (what we implement)", code("""t0 = <a>
t1 = <b>            <- always evaluated
t2 = t0 && t1

MIPS, because `and` is BITWISE:
    sne  $t3, $t0, $zero      # normalise a to 0/1
    sne  $t4, $t1, $zero      # normalise b to 0/1
    and  $t5, $t3, $t4""")),
            ("short-circuit (what C does)", code("""t0 = <a>
t2 = 0
IF_FALSE t0 GOTO Lend       <- b is never evaluated if a is false
t1 = <b>
t2 = t1
Lend:

More instructions in the listing.
Fewer executed, whenever a is false.""")),
        ]) +
        p("Ours is eager, and that is a legitimate choice for a language with no side "
          "effects in expressions — no assignment operator, no <code>++</code>. But "
          "the moment your language gains a function call in an expression, eager "
          "evaluation becomes observable: <code>n != 0 &amp;&amp; divide(x, n)</code> "
          "will call <code>divide</code> with zero. Say in your write-up which you "
          "implemented and what would force you to change.") +
        note("warn", "MIPS and/or are bitwise",
             p("<code>2 &amp; 1</code> is 0, but <code>2 &amp;&amp; 1</code> is 1. If "
               "you emit <code>and</code> directly on the operands you will get the "
               "wrong answer for every value that is truthy but not exactly 1. "
               "Normalise each operand with <code>sne $t, $x, $zero</code> first. "
               "<code>!x</code> is just <code>seq $d, $x, $zero</code>.")) +

        h2("switch, and the fall-through that falls out for free") +
        p("A <code>switch</code> lowers naturally into two sections: a DISPATCH "
          "section that decides where to go, and a BODY section that is just the case "
          "bodies laid out one after another.") +
        stepper([
            ("The source.",
             code("""switch (x) {
    case 1: print(10); break;
    case 2:
    case 3: print(23); break;
    default: print(0); break;
}""")),
            ("Evaluate the controlling expression ONCE, into a hidden variable. If you "
             "re-evaluate it per case, a switch on a function call would call it "
             "n times.",
             code(""">>>DECL __sw0
>>>__sw0 = x""")),
            ("The dispatch chain: one comparison per case label, in source order.",
             code("""DECL __sw0
__sw0 = x
>>>t0 = __sw0 == 1
>>>IF_FALSE t0 GOTO Ltest1
>>>GOTO Lbody1""")),
            ("...and so on for every case. Note case 2 and case 3 get separate tests, "
             "even though they will share a body.",
             code("""Ltest1:
    t1 = __sw0 == 2
    IF_FALSE t1 GOTO Ltest2
    GOTO Lbody2
Ltest2:
    t2 = __sw0 == 3
    IF_FALSE t2 GOTO Ltest3
    GOTO Lbody3""")),
            ("If nothing matched, go to the default — or straight to the end if there "
             "is no default.",
             code("""Ltest3:
>>>    GOTO Ldefault""")),
            ("Now the bodies, in source order, with NO jump between them. That absence "
             "is fall-through: control simply runs off the end of one body into the next.",
             code("""Lbody1: PRINT 10
        GOTO Lend        <- this is the `break`
>>>Lbody2:                  <- empty body: case 2 falls straight into case 3
Lbody3: PRINT 23
        GOTO Lend
Ldefault: PRINT 0
        GOTO Lend
Lend:""")),
            ("<code>break</code> is a GOTO to Lend, taken from the same label stack the "
             "loops use. Which is why a break inside a switch inside a loop leaves the "
             "SWITCH and not the loop — the switch pushed its label more recently.",
             code("""push Lend_loop
    push Lend_switch
        break;   ->  GOTO Lend_switch
    pop
pop""")),
        ]) +
        h3("The alternative: a jump table") +
        p("Instead of n comparisons, build an array of addresses indexed by the case "
          "value and jump indirectly. One bounds check and one indirect jump, "
          "regardless of how many cases.") +
        table(["", "Linear chain", "Jump table"], [
            ["Cost of dispatch", "O(n) comparisons", "O(1)"],
            ["Cost in space", "O(n) instructions", "O(range) words"],
            ["<code>case 1,2,3</code>", "3 comparisons", "3-word table"],
            ["<code>case 1, 1000, 50000</code>", "3 comparisons", "a 50,000-word table"],
            ["Good when", "few cases, or sparse values", "many cases, dense values"],
        ]) +
        p("Real compilers choose per switch, and often build a hybrid: a table for the "
          "dense cluster and comparisons for the outliers. We implement the linear "
          "chain because it is correct for every case-value distribution and it is "
          "twenty lines. Knowing why the other one exists is the part that matters.") +

        h2("MIPS vs ARM — what would actually change") +
        pipeline(active=5, done=(0, 1, 2, 3, 4)) +
        p("Topic 5 asks you to compare code generation for the two. The useful answer "
          "is not a list of mnemonics; it is which parts of your compiler you would "
          "have to touch.") +
        table(["", "MIPS (what we emit)", "ARM (AArch32/64)"], [
            ["Registers", "32, by convention $t/$a/$s/$v", "16 (A32) or 31 (A64), similar conventions"],
            ["Comparison", "<code>slt $d,$a,$b</code> produces 0/1 in a register",
             "<code>cmp a, b</code> sets FLAGS; no result register"],
            ["Branch", "<code>beq $t, $zero, L</code> on a register",
             "<code>b.eq L</code> on the flags set by the last cmp"],
            ["Conditional execution", "none — every conditional is a branch",
             "A32 predicates most instructions: <code>addne</code>, <code>movgt</code>"],
            ["Calls", "<code>jal</code> puts the return address in $ra",
             "<code>bl</code> puts it in LR — same idea, different name"],
        ]) +
        p("So: your scanner, parser, AST, semantic analyzer, TAC generator and "
          "optimizer are all unchanged. Only <code>codegen.c</code> is rewritten — and "
          "within it, mostly <code>mnemonicFor</code>, the branch cases and the "
          "prologue/epilogue. That is the payoff for having an IR at all, and it is "
          "the single best thing to be able to say about your compiler's architecture.") +
        reveal("The one place ARM changes more than the mnemonics",
               p("Conditional execution. On A32, <code>if (a) x = 1;</code> can compile "
                 "to two instructions with no branch at all: <code>cmp</code> then "
                 "<code>movne</code>. A back end that exploits that is not a "
                 "transliteration of the MIPS one — it needs an if-conversion pass that "
                 "decides when a branch is worth replacing with predicated code. That "
                 "is a genuine architectural difference, not a naming one.")) +

        h2("Where the code lives") +
        p("<code>student/topic-5-decisions/compiler/</code>. TODOs cover: the if/else "
          "rules and their precedence declarations, the switch grammar, three AST "
          "nodes, the switch semantic checks, the lowering for both, and the logical "
          "operators in the back end. Every Topic 3 and Topic 4 test must still pass.")
    )


def _a1():
    return (
        meta([("Format", "pairs, at a laptop"), ("Time", "45 min")]) +
        h2("The point") +
        p("Create the dangling-else conflict deliberately, read bison's report on it, "
          "then fix it two different ways and observe that only one of them is honest.") +
        h2("Do this") +
        steps_list([
            "<b>Add the two if rules WITHOUT any precedence declarations.</b> Build "
            "with <code>bison -d -v parser.y</code> and read the warning.",
            "<b>Open <code>parser.output</code></b> and find the conflicted state. It "
            "shows the item set — what the parser had seen and what it could not "
            "decide. Copy that state into your notes.",
            "<b>Test which way bison resolved it.</b> Compile and run"
            + code("""int main() {
    int x; int y;
    x = 1; y = 0;
    if (x > 0) if (y > 0) print(1); else print(2);
    return 0;
}""")
            + "It prints 2 if the else bound to the inner if, and nothing at all if it "
            "bound to the outer one. Which happened?",
            "<b>Fix it properly</b> with <code>%nonassoc LOWER_THAN_ELSE</code> and "
            "<code>%nonassoc ELSE</code>. Rebuild. The warning should be gone and the "
            "behaviour unchanged.",
            "<b>Swap the two declarations.</b> Predict what the test program prints "
            "now, then run it.",
            "<b>Fix it a third way, on paper only:</b> rewrite the grammar with "
            "<code>matched_stmt</code> and <code>unmatched_stmt</code> so that it is "
            "unambiguous with no precedence declarations at all. This is the classic "
            "textbook solution — write it out and say why you would or would not ship it.",
        ]) +
        deliverable(p("The <code>parser.output</code> excerpt, what the test printed at "
                      "each stage, and your unambiguous grammar from step 6 with a "
                      "one-paragraph judgement. This is Lab Question 25 nearly "
                      "verbatim.")))


def _a2():
    return (
        meta([("Format", "pairs"), ("Time", "45 min"), ("Bring", "paper")]) +
        h2("The point") +
        p("Lower nested conditionals by hand and count the labels. Nesting is where "
          "label generation goes wrong, and it goes wrong silently.") +
        h2("Do this") +
        steps_list([
            "<b>Lower this by hand</b> into TAC, generating labels as you go:"
            + code("""if (a > 0) {
    if (b > 0) { print(1); } else { print(2); }
} else {
    print(3);
}"""),
            "<b>Count the labels.</b> How many did you need? Now write the general "
            "formula for k nested if-else statements.",
            "<b>Hand-execute all four combinations</b> of a and b being positive or "
            "not. Confirm each prints exactly one number.",
            "<b>Sabotage.</b> Remove the <code>GOTO Lend</code> at the end of the "
            "then-branch. Re-execute all four cases. Which of them now print TWO "
            "numbers, and which still look correct?",
            "<b>Implement</b> the <code>NODE_IF</code> case and confirm the compiler "
            "produces the same shape you did.",
            "<b>Then break the label generator</b> — make <code>newLabel()</code> "
            "always return <code>\"L0\"</code>. What does the assembler say? Is that "
            "message useful?",
        ]) +
        note("note", "Why step 4 matters",
             p("The cases that still look correct are the ones a hastily written test "
               "would cover. A missing else-jump is invisible whenever the condition is "
               "false, which is why this bug survives casual testing and shows up in "
               "somebody else's program.")) +
        deliverable(p("Your hand lowering, the label count and general formula, the "
                      "four-case execution table, and which cases broke in step 4. "
                      "Feeds Lab Question 26.")))


def _a3():
    return (
        meta([("Format", "pairs"), ("Time", "50 min")]) +
        h2("The point") +
        p("Short-circuit evaluation is a language design decision that most people "
          "inherit without noticing. Make it consciously, and measure what it costs.") +
        h2("Do this") +
        steps_list([
            "<b>Write both lowerings on paper</b> for <code>a &amp;&amp; b</code>: the "
            "eager one and the short-circuiting one. Count instructions in each listing "
            "and instructions EXECUTED when <code>a</code> is false.",
            "<b>Implement the eager version</b> (this is what the TODOs describe) and "
            "confirm the truth tables:"
            + code("""print(1 && 1);  print(1 && 0);  print(0 && 1);  print(0 && 0);
print(1 || 0);  print(0 || 0);  print(!0);  print(!5);"""),
            "<b>Test the trap.</b> <code>print(2 &amp;&amp; 1);</code> must print 1, "
            "not 0. If it prints 0 you emitted a bitwise <code>and</code> without "
            "normalising. Fix it and explain the fix in one sentence.",
            "<b>Measure.</b> Write a loop that evaluates <code>i &gt; 100 &amp;&amp; "
            "i &lt; 200</code> ten thousand times where <code>i</code> is always 5. "
            "Record SPIM's executed-instruction count. How many of those instructions "
            "were wasted evaluating the second operand?",
            "<b>Decide.</b> Would you implement short-circuiting in your compiler? "
            "Under what change to the language would it stop being optional? Two "
            "sentences.",
        ]) +
        reveal("The answer to the second half of step 5",
               p("The moment expressions can have side effects. Add function calls in "
                 "expressions — which you already have — and "
                 "<code>n != 0 &amp;&amp; safeDivide(x, n)</code> becomes a program "
                 "whose correctness depends on the answer. At that point short-circuiting "
                 "is not an optimization, it is part of the language's meaning.")) +
        deliverable(p("Both lowerings with instruction counts, your eight truth-table "
                      "results, your one-sentence fix for step 3, your measurement, and "
                      "your two-sentence decision. Feeds Lab Question 24.")))


def _a4():
    return (
        meta([("Format", "pairs"), ("Time", "50 min")]) +
        h2("The point") +
        p("switch is the first construct where the obvious implementation and the fast "
          "implementation genuinely differ, and where the right answer depends on the "
          "input.") +
        h2("Do this") +
        steps_list([
            "<b>Lower this by hand</b> using the dispatch-then-bodies pattern. Get the "
            "fall-through right — case 2 has no break."
            + code("""switch (x) {
    case 1: print(10); break;
    case 2: print(20);
    case 3: print(30); break;
    default: print(0);
}"""),
            "<b>Hand-execute for x = 1, 2, 3, 9.</b> For x = 2, what prints? Two "
            "numbers. Confirm you understand why before implementing anything.",
            "<b>Design the jump table version</b> on paper for the same switch. What "
            "goes in the table? What happens for a value outside the case range? What "
            "happens for <code>case 1, case 5</code> with nothing between?",
            "<b>Cost it.</b> For each of these, say which implementation you would "
            "choose and why:"
            + ul(["3 cases with values 1, 2, 3",
                  "3 cases with values 1, 1000, 50000",
                  "200 cases with values 1..200",
                  "200 cases with values scattered over 0..2,000,000"]),
            "<b>Implement the linear chain</b> and verify against your hand execution.",
            "<b>Semantic checks.</b> Add two: at most one <code>default</code>, and no "
            "duplicate case values. Test both. Why can neither be a grammar rule?",
        ]) +
        deliverable(p("Your hand lowering, the four-value execution table with x = 2 "
                      "explained, your jump-table design, the four costing decisions, a "
                      "working implementation, and both semantic checks with their test "
                      "cases.")))


def _a5():
    return (
        meta([("Format", "groups of three"), ("Time", "50 min"),
              ("Bring", "a compiler you believe works")]) +
        h2("The point") +
        p("Audit somebody else's compiler adversarially. The Topic 5 objective is "
          "literally <i>audit the correctness of the AST and semantic actions of the "
          "parser</i> — this is that, done to each other.") +
        h2("How to run it") +
        steps_list([
            "<b>Everyone writes five adversarial test programs</b> — programs designed "
            "to break a compiler that was tested casually. Starting points:"
            + ul(["an <code>if</code> with an empty body, or a body that is a bare "
                  "block",
                  "<code>if</code> inside a loop inside an <code>if</code>",
                  "a <code>break</code> inside a switch inside a loop",
                  "a switch whose controlling expression is a function call",
                  "a case body containing a <code>return</code>",
                  "<code>if (a) if (b) X else Y</code>, with all four truth combinations",
                  "a switch with no <code>default</code> and no matching case"]),
            "<b>Write the expected output</b> for each, by hand, before running anything.",
            "<b>Rotate.</b> Run your five programs on both other people's compilers. "
            "Record every disagreement.",
            "<b>Diagnose together.</b> For each failure, find the PHASE responsible. "
            "The AST dump is your fastest tool: if the tree is wrong, nothing "
            "downstream can be right, and you have just narrowed the search to "
            "<code>parser.y</code> and <code>ast.c</code>.",
            "<b>Fix one bug each</b>, in your own compiler, before the session ends.",
        ]) +
        note("note", "The one that catches almost everyone",
             p("A <code>return</code> inside a switch case. If <code>TAC_RETURN</code> "
               "does not jump to the function epilogue, control falls through into the "
               "next case body, and the function returns whatever the LAST case says. "
               "It is invisible until you write exactly this program.")) +
        deliverable(p("Your five programs with expected outputs, a table of which "
                      "compilers failed which tests, and a one-paragraph diagnosis of "
                      "the bug you fixed naming the phase and the line.")))


def _a6():
    return (
        meta([("Format", "pairs"), ("Time", "45 min")]) +
        h2("The point") +
        p("Answer the retargeting question with evidence rather than a feeling. The "
          "Topic 5 objective asks you to compare MIPS and ARM code generation; the "
          "useful comparison is about your own compiler's structure.") +
        h2("Do this") +
        steps_list([
            "<b>Take one function</b> — something with an if and a loop — and get the "
            "MIPS your compiler produces. Print it out.",
            "<b>Hand-translate it to ARM.</b> You do not need to be fluent; you need "
            "the shape. The mappings you need:"
            + code("""    MIPS                          ARM (A32)
    li   $t0, 5                   mov  r0, #5
    add  $t2, $t0, $t1            add  r2, r0, r1
    lw   $t0, 8($sp)              ldr  r0, [sp, #8]
    sw   $t0, 8($sp)              str  r0, [sp, #8]
    slt  $t2, $t0, $t1            cmp  r0, r1        (sets flags)
    beq  $t2, $zero, L            b.ge L             (branches on flags)
    jal  fn_f                     bl   fn_f
    jr   $ra                      bx   lr"""),
            "<b>Count.</b> How many instructions in each version? Where did the counts "
            "differ, and why?",
            "<b>The interesting difference.</b> On ARM (A32) most instructions can be "
            "predicated. Rewrite <code>if (a &gt; 0) x = 1;</code> using "
            "<code>cmp</code> and <code>movgt</code> with NO branch at all. Compare "
            "against the MIPS version.",
            "<b>Now the real question.</b> Go through your compiler file by file and "
            "mark each one <i>unchanged</i>, <i>small changes</i>, or <i>rewritten</i> "
            "for an ARM back end. Then say, in one sentence, what that list tells you "
            "about why the compiler has an IR.",
            "<b>Within <code>codegen.c</code></b>, list the specific functions that "
            "would change. Be precise — this is the answer to the objective.",
        ]) +
        reveal("What step 5 should come out as",
               p("<code>scanner.l</code>, <code>parser.y</code>, <code>ast.*</code>, "
                 "<code>semantic.*</code> and <code>tac.*</code>: unchanged. "
                 "<code>symtab.*</code>: unchanged in interface, possibly different "
                 "word size. <code>codegen.*</code>: rewritten. Roughly 85% of the "
                 "compiler is target-independent, and that is not an accident — it is "
                 "what phase 4 exists to buy you.")) +
        deliverable(p("Both listings side by side with instruction counts, your "
                      "predicated version from step 4, the file-by-file table, and the "
                      "list of functions in <code>codegen.c</code> that would change.")))


ACTIVITIES = [
    dict(slug="dangling-else", session="Week 12 · Wednesday",
         title="Create the Dangling-Else Conflict, Then Fix It",
         lede="Build the conflict on purpose, read parser.output, fix it three ways, and swap the declarations to see it break.",
         body=_a1),
    dict(slug="nested-conditionals", session="Week 12 · Friday",
         title="Lower Nested Conditionals",
         lede="Count the labels, execute all four cases, then remove one jump and see which cases still look fine.",
         body=_a2),
    dict(slug="short-circuit", session="Week 13 · Wednesday",
         title="Short-Circuit or Not — Decide It",
         lede="Two lowerings, a truth table, the bitwise-and trap, and a measurement.",
         body=_a3),
    dict(slug="switch-lowering", session="Week 13 · Friday",
         title="switch: Linear Chain or Jump Table",
         lede="Lower it by hand with fall-through, then cost both implementations against four different case distributions.",
         body=_a4),
    dict(slug="audit-a-compiler", session="Week 14 · Wednesday",
         title="Audit Somebody Else's Compiler",
         lede="Five adversarial programs each, rotate, diagnose by phase, fix one bug before you leave.",
         body=_a5),
    dict(slug="mips-vs-arm", session="Week 14 · Friday",
         title="MIPS vs ARM — What Would Actually Change",
         lede="Hand-translate one function, then mark every file in your compiler as unchanged, edited, or rewritten.",
         body=_a6),
]
