"""Topic 3 — Compiling Complex Variables and Functions."""

from docgen import (code, pipeline, tabs, stepper, reveal, quiz, note, table,
                    steps_list, p, h2, h3, h4, ul, ol, deliverable, meta)

LECTURE_TITLE = "Arrays, Functions, and the Activation Record"
LECTURE_LEDE = ("Three new language features, one new idea — and the new idea is where every "
                "call, every local variable and every recursion lives.")


def lecture():
    return (
        h2("What the language gains") +
        table(["New", "Looks like", "Costs you"], [
            ["Full arithmetic", "<code>a * b - c / 2</code>, parentheses, unary minus",
             "four grammar rules and a precedence table"],
            ["Arrays", "<code>int scores[10]; scores[i] = 3;</code>",
             "two AST nodes, address arithmetic in the back end"],
            ["Functions", "<code>int f(int a, int b[]) { return a; }</code>",
             "a second symbol table, and the activation record"],
            ["Scope", "parameters and locals shadow globals",
             "a scope STACK instead of one flat scope"],
        ]) +
        p("The first three are additive: new cases in switch statements you already "
          "wrote. The fourth is not. Scope changes what the symbol table <i>is</i>, "
          "and functions change what the code generator has to promise.") +

        h2("Precedence is a table, not a grammar rewrite") +
        pipeline(active=1, done=(0,)) +
        p("You could encode precedence by layering the grammar — "
          "<code>expr → term → factor</code>. Bison lets you keep one flat rule and "
          "declare the precedence instead. Both work; the declaration is shorter and "
          "keeps the grammar readable.") +
        code("""%left  '+' '-'      /* lowest  — and LEFT associative     */
%left  '*' '/'      /* higher                                */
%right UMINUS       /* highest — and RIGHT associative        */

expr : expr '+' expr | expr '-' expr
     | expr '*' expr | expr '/' expr
     | '-' expr %prec UMINUS
     | '(' expr ')'  | NUM | ID ;""") +
        p("Two things are being declared at once, and they are independent:") +
        ul(["<b>Precedence</b> — later lines bind tighter. This is what makes "
            "<code>2 + 3 * 4</code> parse as <code>2 + (3 * 4)</code>.",
            "<b>Associativity</b> — <code>%left</code> makes <code>17-5-3</code> group "
            "as <code>(17-5)-3</code>, which is 9. <code>%right</code> would give "
            "<code>17-(5-3)</code>, which is 15. Subtraction is not associative, so "
            "this choice is not cosmetic."]) +
        note("warn", "%prec UMINUS is not decoration",
             p("Without it, the rule <code>'-' expr</code> inherits the precedence of "
               "BINARY minus, which is lower than <code>*</code>. Then "
               "<code>-2 * 3</code> parses as <code>-(2 * 3)</code>. For multiplication "
               "the answer happens to be the same; for a function call with side "
               "effects, or for division, it is not. Try removing it and parsing "
               "<code>-8 / 2 / 2</code>.")) +
        quiz("Given <code>%left '+' '-'</code> then <code>%left '*' '/'</code>, how "
             "does <code>a - b * c - d</code> parse?",
             [("<code>((a - b) * c) - d</code>", False,
               "That would need <code>*</code> to bind LOOSER than <code>-</code>. It "
               "is declared later, so it binds tighter."),
              ("<code>(a - (b * c)) - d</code>", True,
               "Right on both counts: <code>*</code> binds tighter because it is "
               "declared later, and the two <code>-</code> operators group left "
               "because they are <code>%left</code>."),
              ("<code>a - ((b * c) - d)</code>", False,
               "That is right-associative subtraction. <code>%left</code> says "
               "otherwise — and this is exactly why the choice matters."),
              ("It is ambiguous; bison reports a conflict", False,
               "It would be, without the precedence declarations. That is what they "
               "are for: the grammar stays ambiguous and the declarations resolve it.")]) +

        h2("Arrays are address arithmetic") +
        pipeline(active=5, done=(0, 1, 2, 3, 4)) +
        p("An array is a block of consecutive words. <code>a[i]</code> means "
          "<i>the word at (base of a) + i×4</i>. That is the whole idea; everything "
          "else is bookkeeping about where the base is.") +
        code("""int scores[4];        scores lives at  8($sp)

   memory:      8($sp)   12($sp)   16($sp)   20($sp)
                ┌───────┬─────────┬─────────┬─────────┐
                │ [0]   │ [1]     │ [2]     │ [3]     │
                └───────┴─────────┴─────────┴─────────┘

   scores[i]  ->   addi $t0, $sp, 8      # base
                   sll  $t1, $ti, 2      # i * 4
                   add  $t0, $t0, $t1    # base + offset
                   lw   $t2, 0($t0)""") +
        p("The interesting part is that the base is found three different ways "
          "depending on what kind of array it is — and telling those apart is most of "
          "the array work in <code>codegen.c</code>:") +
        table(["Kind", "Where the elements are", "How to get the base"], [
            ["global <code>int g[4];</code>", "the <code>.data</code> section",
             "<code>la $t0, g_g</code>"],
            ["local <code>int a[4];</code>", "this function's frame",
             "<code>addi $t0, $sp, off</code>"],
            ["parameter <code>int a[]</code>", "somebody else's frame or .data",
             "<code>lw $t0, off($sp)</code>"],
        ]) +
        note("key", "Why an array parameter has no size",
             p("Arrays are passed by REFERENCE: the caller hands over the base "
               "address, one word, and the callee's slot holds that address rather "
               "than the data. That is why <code>int a[]</code> takes 4 bytes in the "
               "frame no matter how big the array is, and why the callee cannot know "
               "its length — which is why every function that takes an array in this "
               "language also takes a count.")) +

        h2("The activation record") +
        p("This is the one genuinely new idea in Topic 3. Every call needs somewhere "
          "to put its parameters, its locals, and the address to return to. That "
          "somewhere is a block of stack pushed on entry and popped on exit.") +
        code("""        high address
        ┌──────────────────────────────┐
        │ saved $ra                    │   frameSize-4($sp)
        ├──────────────────────────────┤
        │ (alignment)                  │
        ├──────────────────────────────┤
        │ parameters                   │
        │ locals and arrays            │   0($sp) .. localBytes-1
        │ compiler temporaries         │
        └──────────────────────────────┘   <- $sp
        low address""") +
        stepper([
            ("<code>main</code> is running. Its frame holds its own locals.",
             code("""$sp ──> ┌──────────────┐
        │ main's frame │
        └──────────────┘""")),
            ("<code>main</code> calls <code>sum(a, 4)</code>. First the arguments go "
             "into $a0-$a3, while the $t registers are still valid.",
             code("""    move $a0, $t3      # base address of a
    li   $a1, 4

$sp ──> ┌──────────────┐
        │ main's frame │
        └──────────────┘""")),
            ("Then everything live is written back to memory, because $t0-$t9 are "
             "caller-saved: the callee is free to clobber them all.",
             code("""    sw   $t2, 4($sp)   # write back before the call
    jal  fn_sum""")),
            ("The prologue of <code>sum</code> pushes a NEW frame and saves the return "
             "address into it. Now two frames are live.",
             code("""    addi $sp, $sp, -24
    sw   $ra, 20($sp)

$sp ──> ┌──────────────┐
        │ sum's frame  │   locals of sum
        ├──────────────┤
        │ main's frame │   untouched
        └──────────────┘""")),
            ("<code>sum</code> stores its parameters from $a0-$a3 into its own frame, "
             "because it will need $a0-$a3 again if it calls anything.",
             code(""">>>    sw   $a0, 0($sp)   # parameter a
>>>    sw   $a1, 4($sp)   # parameter n""")),
            ("On <code>return</code>: the value goes in $v0, then control jumps to the "
             "epilogue — it does not fall through.",
             code("""    move $v0, $t1
    j    fn_sum__epilogue""")),
            ("The epilogue restores $ra, pops the frame, and returns. main's frame is "
             "exactly as it was.",
             code("""fn_sum__epilogue:
    lw   $ra, 20($sp)
    addi $sp, $sp, 24
    jr   $ra

$sp ──> ┌──────────────┐
        │ main's frame │
        └──────────────┘""")),
        ]) +
        note("warn", "Three bugs that all look like 'my compiler is haunted'",
             ul(["<b>Not saving $ra.</b> Works for one call. Breaks the moment a "
                 "function calls another function, and breaks spectacularly on "
                 "recursion, because <code>jal</code> overwrites $ra every time.",
                 "<b>Not pushing a new frame.</b> The callee's locals land on top of "
                 "the caller's. Your variables change value across a call for no "
                 "visible reason.",
                 "<b>Falling through on <code>return</code> instead of jumping to the "
                 "epilogue.</b> A <code>return</code> in the middle of a function "
                 "silently continues into the code after it. Symptom: a function that "
                 "always returns whatever its LAST return statement says."])) +

        h2("Scope is a stack") +
        pipeline(active=2, done=(0, 1)) +
        p("Topic 2 had one flat set of names. Now a name can mean different things in "
          "different places, and the rule is: innermost wins.") +
        tabs([
            ("program", code("""int n;                 <- global

int show(int n) {      <- parameter shadows the global
    return n;
}

int main() {
    n = 1;
    print(n);          <- the global:    1
    print(show(2));    <- the parameter: 2
    print(n);          <- the global again, untouched: 1
    return 0;
}""")),
            ("scope stack while checking show()", code("""  [1] function show : n
  [0] global         : n, show, main

  lookup("n") searches [1] first, finds the parameter, stops.""")),
            ("scope stack while checking main()", code("""  [1] function main : (no locals)
  [0] global        : n, show, main

  lookup("n") searches [1], finds nothing, falls through to [0].""")),
        ]) +
        p("Two symbol tables now exist and they answer different questions. "
          "<code>semantic.c</code> keeps a scope stack that answers <i>is this name "
          "visible here?</i> and is thrown away when analysis finishes. "
          "<code>symtab.c</code> keeps a storage map that answers <i>what address is "
          "this name?</i> and is rebuilt per function during code generation. "
          "Confusing them is the single most common source of confusion in this topic.") +

        h2("Two passes, not one") +
        p("This program is legal, and it forces a design decision:") +
        code("""int main() {
    print(helper(3));       <- helper is used here...
    return 0;
}
int helper(int x) {         <- ...and defined here
    return x + 1;
}""") +
        p("A single pass over the AST would reach the call before it had ever seen the "
          "definition. So <code>performSemanticAnalysis</code> runs twice: pass 1 "
          "records every function signature, pass 2 checks every body. Collapse them "
          "into one pass and the program above stops compiling — which is a "
          "perfectly defensible language design (C required forward declarations for "
          "exactly this reason), but it should be a decision, not an accident.") +
        reveal("What pass 1 has to record, and what it does not",
               p("It needs the name, the parameter count, and which parameters are "
                 "arrays — everything needed to check a CALL. It does not need to look "
                 "inside the body at all. That asymmetry is why two cheap passes beat "
                 "one clever one.")) +

        h2("Interview questions this topic answers") +
        p("Topic 3 includes a technical interview, and these are the questions it is "
          "actually about. Practise saying the answers out loud.") +
        ul(["How does your parser tell a variable declaration from a function "
            "declaration? (Both start <code>int ID</code> — what is the deciding token?)",
            "Where do local variables live, and who allocates them?",
            "What exactly happens between <code>jal</code> and the first instruction "
            "of the callee?",
            "Why is <code>$ra</code> saved in the frame rather than kept in a register?",
            "Your language passes arrays by reference and integers by value. Why not "
            "both the same way?"]) +
        h2("Where the code lives") +
        p("<code>student/topic-3-arrays-and-functions/compiler/</code> — this is your "
          "working Topic 2 compiler with the new work marked. It builds and passes the "
          "Topic 2 tests before you start. <code>tests/</code> contains the five "
          "programs it must pass when you are done.")
    )


def _a1():
    return (
        meta([("Format", "pairs"), ("Time", "40 min"), ("Bring", "paper")]) +
        h2("The point") +
        p("Precedence and associativity are two separate decisions that people "
          "routinely conflate. Separate them by hand.") +
        h2("Do this") +
        steps_list([
            "<b>Draw the AST</b> for each of these, using the precedence table from "
            "the lecture notes. Do not run anything yet."
            + code("2 + 3 * 4\n(2 + 3) * 4\n17 - 5 - 3\n-2 * 3\n2 * -3\n-8 / 2 / 2"),
            "<b>Evaluate each tree</b> and write the number down.",
            "<b>Check</b> by compiling"
            + code("int main() { print(2 + 3 * 4); print(17 - 5 - 3); print(-8 / 2 / 2); return 0; }")
            + "and running it in SPIM. Any disagreement is worth ten minutes.",
            "<b>Change associativity.</b> In <code>parser.y</code>, change "
            "<code>%left '+' '-'</code> to <code>%right '+' '-'</code>. Predict which "
            "of your six expressions change value, then rebuild and check.",
            "<b>Remove <code>%prec UMINUS</code></b> from the unary-minus rule. "
            "Predict what happens to <code>-8 / 2 / 2</code>. Rebuild and check.",
            "<b>Put it back.</b>",
        ]) +
        h2("The question worth taking away") +
        p("Bison resolved an ambiguous grammar using declarations. The alternative was "
          "to rewrite the grammar into <code>expr → term → factor</code> layers. Write "
          "the layered version of just <code>+</code>, <code>*</code> and "
          "<code>NUM</code>, and say which you would ship in a compiler other people "
          "have to maintain.") +
        deliverable(p("Six trees with their values, the results of experiments 4 and "
                      "5, and your layered grammar with a one-paragraph argument. "
                      "Feeds Lab Question 3.")))


def _a2():
    return (
        meta([("Format", "pairs, at a laptop"), ("Time", "50 min")]) +
        h2("The point") +
        p("Do the address arithmetic by hand before you make the compiler do it. "
          "Off-by-four is a very cheap mistake to make and a very expensive one to "
          "find in generated assembly.") +
        h2("Do this") +
        steps_list([
            "<b>On paper.</b> <code>int a[5];</code> sits at offset 12 in the frame. "
            "Write the byte address of <code>a[0]</code>, <code>a[3]</code>, and "
            "<code>a[i]</code>. Then write the MIPS to load <code>a[i]</code> into "
            "<code>$t4</code>, assuming <code>i</code> is in <code>$t2</code>.",
            "<b>Why <code>sll $t, $t, 2</code> and not <code>mul $t, $t, 4</code>?</b> "
            "Both work. Time them if you like — SPIM will tell you the instruction "
            "count. Write down which is faster and why.",
            "<b>Implement</b> <code>createArrayDecl</code>, <code>createArrayIndex</code>, "
            "the two grammar rules, and the <code>TAC_ARRAY_LOAD</code> / "
            "<code>TAC_ARRAY_STORE</code> cases in <code>codegen.c</code>.",
            "<b>Test with a local array first</b>, then a global one. They take "
            "different paths through <code>arrayBaseReg</code>; make sure you know "
            "which path each one took by reading the generated <code>.s</code>.",
            "<b>Break it deliberately.</b> Read <code>a[99]</code> from a 5-element "
            "array. What happens? Nothing stops you — there is no bounds check in "
            "this language. Find out what memory you just read.",
        ]) +
        note("note", "Global arrays and .align",
             p("<code>.asciiz</code> leaves the assembler's location counter on an odd "
               "byte. If a <code>.space</code> or <code>.word</code> follows it "
               "without <code>.align 2</code>, every <code>lw</code> on that array "
               "raises an address-error exception in SPIM. It is a classic first bug "
               "and the error message does not obviously point at the cause.")) +
        deliverable(p("Your hand-written address arithmetic and MIPS from step 1, your "
                      "answer to step 2, a working array test, and one paragraph on "
                      "what step 5 produced. Feeds Lab Question 14.")))


def _a3():
    return (
        meta([("Format", "pairs"), ("Time", "50 min")]) +
        h2("The point") +
        p("Draw the stack frame you expect, then hold the generated assembly up "
          "against it. This is the activity that makes function calls stop being "
          "magic.") +
        h2("Do this") +
        steps_list([
            "<b>Draw the frame</b> you expect the compiler to build for"
            + code("""int addUp(int a, int b) {
    int t;
    t = a + b;
    return t;
}""")
            + "Label every slot with its offset from <code>$sp</code> and say how many "
            "bytes the whole frame is. Do not forget the temporaries.",
            "<b>Compile it</b> WITHOUT <code>-q</code> and find the line that says "
            "<code>Activation record for 'addUp': N bytes</code>, followed by the "
            "symbol table. Compare with your drawing.",
            "<b>Read the prologue and epilogue</b> in the generated <code>.s</code>. "
            "Account for every instruction. There should be no line you cannot explain.",
            "<b>Now sabotage the epilogue.</b> Comment out the <code>lw $ra</code> "
            "restore in <code>emitEpilogue</code>. Predict what happens, then rebuild "
            "and run. Where does control actually go?",
            "<b>Sabotage differently.</b> Restore that, and instead make "
            "<code>TAC_RETURN</code> NOT jump to the epilogue — just set <code>$v0</code> "
            "and fall through. Test with a function that has a return in the middle. "
            "Explain the result.",
        ]) +
        deliverable(p("Your predicted frame diagram next to the compiler's symbol "
                      "table, an annotated prologue/epilogue, and one paragraph for "
                      "each sabotage explaining the failure mode. Step 5 is exactly "
                      "the bug that broke <code>return</code> inside a switch in an earlier "
                      "version of this compiler.")))


def _a4():
    return (
        meta([("Format", "pairs, at a laptop"), ("Time", "50 min")]) +
        h2("The point") +
        p("Trace a call through the register conventions, including the case that "
          "breaks naive implementations: a call inside a call.") +
        h2("Do this") +
        steps_list([
            "<b>Predict the TAC</b> for <code>f(1, g(2))</code> — write the ARG and "
            "CALL instructions in order. Then compile and compare.",
            "<b>Explain the ordering.</b> Both calls emit ARG instructions into the "
            "same buffer. Why does the inner CALL take the right ones? (Read the "
            "<code>TAC_CALL</code> case in <code>codegen.c</code>.)",
            "<b>Write a recursive function</b> — factorial is fine — and run it for "
            "n = 5. Then draw the stack at the deepest point: how many frames, and "
            "what is in each <code>$ra</code> slot?",
            "<b>Find the register limit.</b> Write a function taking five parameters. "
            "What does the compiler say? Is that a good error message? Improve it if not.",
            "<b>Design.</b> Sketch how you WOULD pass a fifth argument. Real MIPS "
            "pushes it on the stack. Where exactly — above the caller's frame or below "
            "it? Who pops it? Write the two-line answer.",
        ]) +
        reveal("On step 2",
               p("A CALL consumes the LAST n buffered arguments, where n comes from "
                 "the CALL instruction itself. Work through <code>f(1, g(2))</code> "
                 "with that rule and watch it come out right — then work through "
                 "<code>f(g(1), 2)</code> and watch it come out right for a different "
                 "reason.")) +
        deliverable(p("Your predicted vs actual TAC, your answer to step 2, a stack "
                      "diagram for factorial(5) at maximum depth, and your two-line "
                      "answer to step 5. Feeds Lab Question 15.")))


def _a5():
    return (
        meta([("Format", "pairs"), ("Time", "40 min")]) +
        h2("The point") +
        p("Shadowing is easy to describe and easy to get wrong. Predict, then verify.") +
        h2("Do this") +
        steps_list([
            "<b>Predict the output</b> of this program, line by line, before running it."
            + code("""int n;
int twice(int n) { return n + n; }
int main() {
    int m;
    n = 10;
    m = twice(3);
    print(n);
    print(m);
    { int n; n = 99; print(n); }
    print(n);
    return 0;
}"""),
            "<b>Draw the scope stack</b> at each <code>print</code>. Which entry does "
            "the lookup find, and how many scopes did it search?",
            "<b>Run it</b> without <code>-q</code> and find the scope-stack traces in "
            "the semantic analyzer output. Reconcile.",
            "<b>Break it.</b> Make <code>exitScope()</code> a no-op. Predict what now "
            "goes wrong, then run and confirm. What error appears, and is it the "
            "error you predicted?",
            "<b>Break it the other way.</b> Restore <code>exitScope</code>, and change "
            "<code>isVarDeclaredInScope</code> to search only the OUTERMOST scope. "
            "Which of the two symbol tables did you just break — the visibility one or "
            "the storage one?",
        ]) +
        deliverable(p("Your line-by-line prediction, five scope-stack diagrams, and a "
                      "paragraph on each sabotage. Feeds Lab Questions 11 and 16.")))


def _a6():
    return (
        meta([("Format", "pairs, taking turns"), ("Time", "50 min"),
              ("Format note", "one whiteboard or shared doc per pair")]) +
        h2("The point") +
        p("Technical Interview Quiz 1 falls in this topic. The questions are not "
          "trivia — they are the design decisions you have already made, asked out "
          "loud. Rehearse saying them.") +
        h2("How to run it") +
        p("Ten minutes each way. One person asks, the other answers at the "
          "whiteboard — talking the whole time, the way you would in a real interview. "
          "The asker's job is to keep asking <i>why</i>.") +
        h2("The questions") +
        ol([
            "Walk me through what happens to <code>x = a + 1;</code> in your compiler, "
            "phase by phase. <i>(Follow-up: which phase would catch it if <code>a</code> "
            "were undeclared, and why can't an earlier one?)</i>",
            "Your parser sees <code>int total</code>. Is that a variable or a function? "
            "How does it decide, and how many tokens of lookahead does it need?",
            "Where do local variables live? Who decides the offsets, and when? "
            "<i>(Follow-up: why does <code>layoutFrame</code> walk the whole function "
            "before emitting anything?)</i>",
            "Draw the stack for <code>factorial(3)</code> at maximum depth.",
            "Your language passes integers by value and arrays by reference. Why the "
            "difference? What would change if arrays were by value?",
            "You have ten registers and a program with thirty live values. What do you "
            "do? <i>(Follow-up: how do you decide which one to evict?)</i>",
            "Name a program that your compiler accepts and should not. What would it "
            "take to catch it, and in which phase?",
        ]) +
        note("note", "What is actually being assessed",
             p("Not whether you memorised the answer. Whether you can reason out loud "
               "about a system you built, admit the parts you are unsure of, and say "
               "what you would do to find out. Answering 'I do not know, but here is "
               "how I would check' is a strong answer.")) +
        deliverable(p("Nothing to hand in. Note the two questions you answered worst "
                      "and go read the relevant code before the quiz.")))


ACTIVITIES = [
    dict(slug="precedence-lab", session="Week 6 · Wednesday",
         title="Precedence and Associativity Lab",
         lede="Six expressions, six trees, then break the precedence table and watch what changes.",
         body=_a1),
    dict(slug="array-addressing", session="Week 6 · Friday",
         title="Arrays Are Address Arithmetic",
         lede="Do base + index×4 by hand, then make the compiler do it — for local, global and parameter arrays.",
         body=_a2),
    dict(slug="draw-the-frame", session="Week 7 · Wednesday",
         title="Draw the Activation Record",
         lede="Predict the stack frame, check it against the generated assembly, then sabotage the epilogue.",
         body=_a3),
    dict(slug="calling-convention", session="Week 7 · Friday",
         title="Trace a Call, Including a Nested One",
         lede="$a0–$a3, $v0, $ra, and why f(1, g(2)) works at all.",
         body=_a4),
    dict(slug="scope-and-shadowing", session="Week 8 · Wednesday",
         title="Scope and Shadowing",
         lede="Predict the output, draw the scope stack, then break exitScope on purpose.",
         body=_a5),
    dict(slug="interview-rehearsal", session="Week 8 · Friday",
         title="Technical Interview Rehearsal",
         lede="Seven questions, ten minutes each way, at a whiteboard, out loud.",
         body=_a6),
]
