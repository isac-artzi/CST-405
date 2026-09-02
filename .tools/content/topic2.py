"""Topic 2 — Compiler for a Starter Language.  Four weeks, eight activities."""

from docgen import (code, pipeline, tabs, stepper, reveal, quiz, note, table,
                    steps_list, p, h2, h3, h4, ul, ol, deliverable, meta)

LECTURE_TITLE = "A Whole Compiler, for the Smallest Language Worth Compiling"
LECTURE_LEDE = ("Four weeks, six phases, one very small language — and by the end, a .s file "
                "that runs.")


def lecture():
    return (
        h2("The language") +
        p("This is the entire starter language. Three kinds of statement, one "
          "operator, one type.") +
        code("""program    ->  stmt_list
stmt_list  ->  stmt  |  stmt_list stmt
stmt       ->  decl  |  assign  |  print_stmt
decl       ->  'int' ID ';'
assign     ->  ID '=' expr ';'
expr       ->  NUM  |  ID  |  expr '+' expr
print_stmt ->  'print' '(' expr ')' ';'""") +
        p("It looks trivial, and as a language it is. As a <i>compiler project</i> "
          "it is not, because a working compiler for this language needs every one of "
          "the six phases, complete. Adding <code>*</code> later costs one grammar "
          "rule. Adding the first phase costs four weeks.") +
        note("key", "What you are really building",
             p("The scaffolding. Everything in Topics 3–6 is a new <i>case</i> in "
               "switch statements you write this month. Get the shape right now and "
               "the rest of the semester is additive; get it wrong and you will "
               "rewrite it in November under deadline.")) +

        h2("One program, six representations") +
        p("Here is the same three-line program as each phase sees it. Flip through "
          "the tabs — the whole course is in this one widget.") +
        tabs([
            ("1 source", code("int total;\ntotal = 2 + 3;\nprint(total);")),
            ("2 tokens", code("""INT   ID(total)  SEMI
ID(total)  ASSIGN  NUM(2)  PLUS  NUM(3)  SEMI
PRINT  LPAREN  ID(total)  RPAREN  SEMI""")),
            ("3 AST", code("""STMT_LIST
  DECL: int total
  ASSIGN: total
    BINOP: +
      NUM: 2
      NUM: 3
  PRINT
    VAR: total""")),
            ("4 symbols", code("""LOCALS (activation record, 4 bytes)
    total        int      0($sp)""")),
            ("5 TAC", code("""FUNC_BEGIN main
    DECL int total
    t0 = 2 + 3
    total = t0
    PRINT total
    RETURN 0
FUNC_END main""")),
            ("6 optimized", code("""FUNC_BEGIN main
    DECL int total
>>>    total = 5          <- folded, and t0 was then dead
    PRINT total
    RETURN 0
FUNC_END main""")),
            ("7 MIPS", code(""".data
__nl: .asciiz "\\n"

.text
.globl main
main:
    addi $sp, $sp, -16
    sw   $ra, 12($sp)
    li   $t0, 5
    sw   $t0, 0($sp)      # total
    lw   $t1, 0($sp)
    move $a0, $t1
    li   $v0, 1
    syscall
    la   $a0, __nl
    li   $v0, 4
    syscall
main__epilogue:
    lw   $ra, 12($sp)
    addi $sp, $sp, 16
    li   $v0, 10
    syscall""")),
        ]) +

        h2("Phase 2 — the parser, and what a semantic action really is") +
        pipeline(active=1, done=(0,)) +
        p("Bison builds a bottom-up parser. It shifts tokens onto a stack and, "
          "whenever the top of the stack matches the right-hand side of a rule, "
          "REDUCES: pops those symbols and pushes the left-hand side. The action in "
          "braces runs at the moment of the reduction, and that is when your AST node "
          "gets built.") +
        code("""expr : expr '+' expr   { $$ = createBinOp('+', $1, $3); }
       ─┬─  ─┬─  ─┬─           ─┬─              ─┬─  ─┬─
        │    │    │             │                │    └── $3, the right subtree
        │    │    └── $3        │                └─────── $1, the left subtree
        │    └── $2 (unused)    └── the value THIS rule hands back
        └── $1""") +
        p("Because reductions happen innermost-first, the children are already built "
          "by the time the parent's action runs. You never write tree-building code "
          "that walks anything; you only ever assemble one node from pieces that "
          "already exist.") +
        stepper([
            ("Input: <code>total = 2 + 3 ;</code> — the parser starts with an empty stack.",
             code("stack: (empty)                 remaining: ID = NUM + NUM ;")),
            ("Shift ID, then '=' , then NUM.",
             code("stack: ID  =  NUM              remaining: + NUM ;")),
            ("NUM can be reduced to expr. The action runs: <code>$$ = createNum(2)</code>.",
             code(">>>stack: ID  =  expr             remaining: + NUM ;\n\n       expr ─ NUM: 2")),
            ("Shift '+' and NUM; reduce that NUM to expr as well.",
             code("stack: ID  =  expr  +  expr    remaining: ;\n\n       expr ─ NUM: 2      expr ─ NUM: 3")),
            ("Now the top three symbols match <code>expr '+' expr</code>. Reduce, and "
             "the action builds the BINOP node from two subtrees that already exist.",
             code(""">>>stack: ID  =  expr             remaining: ;

       expr ─ BINOP: +
                ├─ NUM: 2
                └─ NUM: 3""")),
            ("Shift ';' and reduce the whole thing to <code>assign</code>. "
             "One statement, one tree.",
             code(""">>>stack: assign                  remaining: (none)

       ASSIGN: total
         └─ BINOP: +
              ├─ NUM: 2
              └─ NUM: 3""")),
        ]) +

        h2("Parse tree vs AST — the difference that matters") +
        p("The parse tree records every reduction the parser made, including the ones "
          "that exist only to encode precedence. The AST records what the program "
          "MEANS. Compare, for <code>total = 2 + 3;</code>:") +
        tabs([
            ("parse tree", code("""assign
├─ ID(total)
├─ '='
├─ expr
│  ├─ expr
│  │  └─ NUM(2)
│  ├─ '+'
│  └─ expr
│     └─ NUM(3)
└─ ';'""")),
            ("AST", code("""ASSIGN: total
└─ BINOP: +
   ├─ NUM: 2
   └─ NUM: 3""")),
        ]) +
        p("The AST threw away the semicolon, the equals sign, and the chain of "
          "single-child <code>expr</code> nodes. Nothing downstream needs them. Every "
          "later phase walks the AST, so every node you keep is a node five phases "
          "have to handle.") +
        quiz("Why does the AST have no node for parentheses?",
             [("Because the scanner discards them", False,
               "The scanner returns them as tokens; the parser uses them. Something "
               "else explains why they leave no trace."),
              ("Because <code>( e )</code> yields <code>e</code>: the grouping is "
               "already recorded in the tree's SHAPE", True,
               "Right. Parentheses exist to steer the parser. Once the tree is built, "
               "the shape they produced IS the grouping, and a node saying "
               "'these were parenthesised' would add nothing any later phase could use."),
              ("Because our language has no parentheses in expressions", False,
               "It gets them in Topic 3 — and still has no AST node for them."),
              ("Because they are handled by precedence declarations", False,
               "Precedence resolves ambiguity between operators. Parentheses override "
               "it explicitly. Both end up expressed the same way: as tree shape.")]) +

        h2("Phase 3 — semantic analysis is where 'it parses' stops being enough") +
        pipeline(active=2, done=(0, 1)) +
        p("These two programs are equally legal as SENTENCES. Only one of them means "
          "anything.") +
        code("""int x;              int x;
x = 1;              x = ghost;      <- parses fine: ID '=' expr ';'
print(x);           print(x);       <- but `ghost` was never declared"""),
        p("No context-free grammar can express 'declared before use', because the "
          "declaration can be arbitrarily far away. That is precisely the boundary "
          "between phase 2 and phase 3, and it is worth being able to state crisply "
          "in a technical interview.") +
        p("The symbol table is what closes the gap. Walk the AST; on a declaration, "
          "insert; on a use, look up.") +

        h2("Phase 4 — three-address code, and why bother") +
        pipeline(active=3, done=(0, 1, 2)) +
        p("You could generate MIPS straight from the AST. People do. But every "
          "optimization you will write in Topic 4 wants a flat list of simple "
          "instructions, not a tree — and every new target machine you might add "
          "wants to start from something that is not the source language.") +
        code("""AST                            TAC
                               t0 = 2 + 3
ASSIGN: total          ->      total = t0
  BINOP: +
    NUM: 2                     one operator per instruction,
    NUM: 3                     at most three operands""") +
        note("note", "The rule that makes the recursion work",
             p("<code>generateTACExpr()</code> returns the NAME of the place holding "
               "the result. Sometimes that is a literal (<code>\"5\"</code>), "
               "sometimes a variable (<code>\"total\"</code>), sometimes a temporary "
               "(<code>\"t0\"</code>). The caller does not care which — it just uses "
               "the name. One return convention, and the whole tree walk falls out.")) +

        h2("Phase 6 — registers are a cache over memory") +
        pipeline(active=5, done=(0, 1, 2, 3, 4)) +
        p("TAC pretends it has unlimited named locations. MIPS has 32 registers. The "
          "resolution is simple and it is the same one CPUs use for main memory: give "
          "every name a permanent HOME in the stack frame, and treat "
          "<code>$t0</code>–<code>$t9</code> as a cache over those homes.") +
        table(["Situation", "What the allocator does"], [
            ["Need a value that is already in a register", "use it; no instruction emitted"],
            ["Need a value that is not", "<code>lw</code> from its home slot"],
            ["About to overwrite a name", "take a register, mark it dirty, do NOT load"],
            ["No free registers", "evict the least recently used one, <code>sw</code> it first if dirty"],
            ["About to call a function", "write back everything dirty; the callee owns $t0-$t9"],
        ]) +
        p("Because every name has a home, any value can be written back at any "
          "moment. That one guarantee is what makes spilling safe, and it is why "
          "<code>layoutFrame()</code> walks the whole function before a single "
          "instruction is emitted.") +

        h2("What good error messages are worth") +
        p("Both of these are correct. Only one of them is useful.") +
        tabs([
            ("what bison gives you", code("syntax error")),
            ("what you can give instead", code("""❌ Syntax Error at line 4:
   Missing semicolon after assignment
   💡 Suggestion: add ';' after 'total = 2 + 3'""")),
        ]) +
        p("The second costs one <code>error</code> production per statement form. "
          "Lab Question 5 asks you to write a program with three deliberate syntax "
          "errors and demonstrate that you detect all three with their exact "
          "locations — so this is not optional polish, it is the assignment.") +
        reveal("How an error production works",
               p("Bison has a magic token, <code>error</code>. Writing "
                 "<code>| ID '=' expr error</code> tells it: if you were parsing an "
                 "assignment and hit something unexpected where the semicolon should "
                 "be, take this rule instead, run its action, and then call "
                 "<code>yyerrok</code> to resume normal parsing. The action is where "
                 "you print a message that names the statement you were in.") +
               code("""assign:
    ID '=' expr ';'      { $$ = createAssign($1, $3); free($1); }
  | ID '=' expr error    { fprintf(stderr,
                             "line %d: missing ';' after assignment to '%s'\\n",
                             yylineno, $1);
                           free($1); $$ = NULL; yyerrok; }
  ;""")) +

        h2("A four-week plan") +
        table(["Week", "Build", "Done when"], [
            ["2", "Grammar + AST (phases 1–2)",
             "<code>printAST</code> shows a correct tree for a 5-line program"],
            ["3", "Symbol table + semantic checks (phase 3)",
             "undeclared and duplicate variables are both caught, with line numbers"],
            ["4", "TAC generation (phase 4)",
             "the .tac file is readable and you can hand-execute it"],
            ["5", "Optimizer + MIPS (phases 5–6)",
             "<code>spim -file out.s</code> prints the right numbers"],
        ]) +
        note("warn", "The single most common way this goes wrong",
             p("Leaving code generation until week 5. Phases 4 and 6 are where the "
               "design decisions you made in week 2 come due, and if the AST is the "
               "wrong shape you want to find out in week 3, not the night before the "
               "deadline. Get one statement — <code>print(1);</code> — all the way "
               "through to running MIPS in the first week. Then widen.")) +
        h2("Where the code lives") +
        p("<code>student/topic-2-minimal-compiler/compiler/</code>. It builds before "
          "you touch it: the scanner, the headers, the driver and the register "
          "allocator are given. Sections marked <code>TODO (Topic 2)</code> are yours. "
          "<code>make test</code> runs <code>tests/*.cm</code>; two of those tests are "
          "supposed to fail, and their header comments say why.")
    )


# ===========================================================================
# Eight class activities — two per week for four weeks
# ===========================================================================

def _a1():
    return (
        meta([("Format", "pairs"), ("Time", "45 min"), ("Bring", "paper")]) +
        h2("The point") +
        p("Before touching bison, derive some sentences by hand. Ambiguity is easy to "
          "define and hard to recognise, and the only reliable way to recognise it is "
          "to have once found two different trees for the same string.") +
        h2("Do this") +
        steps_list([
            "<b>Derive.</b> Using the starter grammar, write a leftmost derivation for"
            + code("int x;\nx = 1 + 2;")
            + "Show every step: <code>program ⇒ stmt_list ⇒ ...</code>",
            "<b>Draw the parse tree</b> for that derivation.",
            "<b>Now the interesting one.</b> Take this grammar fragment, which has no "
            "precedence declarations at all:"
            + code("expr -> expr '+' expr | expr '*' expr | NUM")
            + "Draw <b>two different parse trees</b> for <code>1 + 2 * 3</code>. "
            "Evaluate both. You should get two different numbers.",
            "<b>Fix it two ways.</b> (a) By rewriting the grammar into layers "
            "(<code>expr → term → factor</code>). (b) By keeping the ambiguous grammar "
            "and adding <code>%left</code> declarations. Write both.",
            "<b>Argue.</b> Which fix would you ship, and why? There is a real answer "
            "here and it is not obvious — write down the trade-off you actually "
            "believe, not the one you think is expected.",
        ]) +
        reveal("If you are stuck on step 5",
               p("Layering is portable: it works with any parser generator, and the "
                 "grammar itself documents the precedence. Precedence declarations are "
                 "shorter, easier to change, and keep the grammar readable — but they "
                 "are a bison feature, and they hide the precedence somewhere other "
                 "than the rules. Both arguments are good. Pick one and mean it.")) +
        deliverable(p("A photo or scan of your worked pages, plus a short paragraph "
                      "answering step 5. This is most of Lab Question 3.")))


def _a2():
    return (
        meta([("Format", "pairs, at a laptop"), ("Time", "50 min")]) +
        h2("The point") +
        p("Get bison to talk to you. Its conflict reports are the most useful and "
          "least read output in this course.") +
        h2("Do this") +
        steps_list([
            "<b>Build the given skeleton</b> and confirm it compiles:"
            + code("cd student/topic-2-minimal-compiler/compiler\nmake\n./minicompiler tests/t2_01_basics.cm out.s")
            + "It will fail — the grammar is a placeholder. Read the message.",
            "<b>Write ONE rule:</b> <code>program : stmt_list { root = $1; }</code> "
            "and <code>stmt_list : stmt | stmt_list stmt</code>, with "
            "<code>stmt : decl</code> and <code>decl : INT ID ';'</code>. "
            "Nothing else. Build.",
            "<b>Feed it a file containing only declarations.</b> Confirm it parses.",
            "<b>Now deliberately create a conflict.</b> Add a second rule "
            "<code>stmt : INT ID ';'</code> alongside <code>stmt : decl</code>. "
            "Rebuild and read what bison says.",
            "<b>Get the full report.</b> Run <code>bison -d -v parser.y</code> and open "
            "<code>parser.output</code>. Find the state with the conflict. It shows you "
            "the exact item set — which symbols it had seen and what it could not "
            "decide between.",
            "<b>Remove the conflict</b> and add the remaining rules for "
            "<code>assign</code> and <code>print_stmt</code>.",
        ]) +
        note("note", "parser.output is a gift",
             p("Nearly everyone in this course will, at some point, have a grammar "
               "with a conflict they do not understand. The answer is always in "
               "<code>parser.output</code>. Learning to read it today costs 15 minutes "
               "and saves an evening in Topic 5, where the dangling-else conflict "
               "arrives on schedule.")) +
        deliverable(p("Your <code>parser.y</code> with all four statement forms "
                      "parsing, plus the excerpt from <code>parser.output</code> "
                      "showing the conflict you created in step 4 and one sentence "
                      "explaining what bison could not decide.")))


def _a3():
    return (
        meta([("Format", "individual, then compare"), ("Time", "40 min")]) +
        h2("The point") +
        p("You are about to design a data structure that five later phases have to "
          "live with. Design it on paper first.") +
        h2("Do this") +
        steps_list([
            "<b>Draw the parse tree AND the AST</b> for"
            + code("int a;\nint b;\na = 1 + 2;\nb = a + a;\nprint(b);"),
            "<b>Count the nodes in each.</b> Write both numbers down.",
            "<b>For every node in the parse tree that is NOT in the AST</b>, say in "
            "one phrase what it was for and why nothing downstream needs it.",
            "<b>Design decision.</b> Our <code>NODE_STMT_LIST</code> holds two "
            "children — a statement and 'the rest'. An alternative is a single node "
            "holding an array of statements. Sketch both for the five-statement "
            "program above.",
            "<b>Argue it.</b> Which is easier to build in a bison action? Which is "
            "easier to WALK in <code>generateTAC</code>? They may not be the same "
            "answer, and noticing that is the point.",
        ]) +
        reveal("A nudge on step 5",
               p("A left-recursive rule reduces one statement at a time, so an action "
                 "naturally builds a linked structure — the array version has to grow "
                 "and copy. But walking a linked list of lists means every visitor "
                 "needs a special case for 'the child is itself a list', which is "
                 "exactly the bug that will make your compiler silently skip "
                 "statements. Look at how <code>checkStmtList</code> and "
                 "<code>generateTACStmtList</code> handle it in the given code.")) +
        deliverable(p("Both trees, both node counts, your list from step 3, and a "
                      "short paragraph on step 5. This is Lab Question 6 nearly "
                      "verbatim.")))


def _a4():
    return (
        meta([("Format", "pairs, at a laptop"), ("Time", "50 min")]) +
        h2("The point") +
        p("Make the tree real, and make it visible. <code>printAST</code> is the "
          "instrument you will use to debug everything else this semester.") +
        h2("Do this") +
        steps_list([
            "<b>Write the AST constructors</b> in <code>ast.c</code>. Follow the "
            "pattern of <code>createNum</code>, which is given. Five functions, three "
            "lines each.",
            "<b>Wire them into the grammar actions</b> in <code>parser.y</code>.",
            "<b>Write <code>printAST</code>.</b> Two spaces of indent per level. "
            "Recurse into children at <code>level + 1</code> — except for "
            "<code>NODE_STMT_LIST</code>, whose two children print at the SAME level, "
            "because a sequence is not a nesting.",
            "<b>Test it against your paper answer from Activity 3.</b> If the printed "
            "tree does not match what you drew, one of the two is wrong; find out "
            "which before moving on.",
            "<b>Deliberately break it.</b> In <code>createAssign</code>, store the "
            "name without <code>strdup</code>: <code>node->data.assign.var = var;</code>. "
            "Rebuild and run. Describe what you see and explain why.",
        ]) +
        note("warn", "Step 5 is the most valuable five minutes of the week",
             p("The scanner reuses its buffer for the next token. A name you merely "
               "point at will have changed by the time the semantic analyzer reads it. "
               "The symptom is an AST that looks randomly corrupted, and it is one of "
               "the hardest bugs to find in this course — unless you have seen it once, "
               "on purpose, when you knew what you had just done.")) +
        deliverable(p("A working <code>printAST</code>, its output for the Activity 3 "
                      "program, and one paragraph describing what step 5 produced and "
                      "why.")))


def _a5():
    return (
        meta([("Format", "pairs"), ("Time", "45 min")]) +
        h2("The point") +
        p("Predict what the symbol table will contain before you look. Being able to "
          "do that reliably is the difference between debugging and guessing.") +
        h2("Do this") +
        steps_list([
            "<b>Predict.</b> For the program below, write down what the symbol table "
            "holds after each line: names, and the stack offset each one gets."
            + code("int a;\nint b;\nint sum;\na = 3;\nb = 4;\nsum = a + b;\nprint(sum);"),
            "<b>Check.</b> Compile it WITHOUT <code>-q</code> and find the symbol "
            "table trace in the output. Reconcile any differences.",
            "<b>Now break it three ways</b>, and for each one predict the message "
            "before you run it:"
            + ul(["<code>int a; int a;</code> — duplicate declaration",
                  "<code>x = 1;</code> with no declaration of <code>x</code>",
                  "<code>print(y);</code> with no declaration of <code>y</code>"]),
            "<b>Grade your own error messages.</b> For each, ask: does it give the "
            "LINE? does it name the IDENTIFIER? does it say what would fix it? Rewrite "
            "any that fail all three.",
            "<b>Design question.</b> Our table is a flat array searched linearly. "
            "Sketch what changes if it becomes a hash table. Which functions change? "
            "Which do not? Why does that answer matter?",
        ]) +
        deliverable(p("Your predictions and the actual traces side by side; your three "
                      "improved error messages; a short answer to step 5. Steps 3–4 "
                      "feed Lab Question 5 directly.")))


def _a6():
    return (
        meta([("Format", "pairs"), ("Time", "50 min")]) +
        h2("The point") +
        p("Translate an AST to three-address code by hand, then make the compiler "
          "agree with you. If it does not, one of you is wrong and it is worth knowing "
          "which.") +
        h2("Do this") +
        steps_list([
            "<b>By hand.</b> Write the TAC for"
            + code("int a; int b; int c;\na = 1 + 2;\nb = a + a;\nc = a + b + 3;\nprint(c);")
            + "Use <code>t0, t1, ...</code> for temporaries. Number every instruction.",
            "<b>Count your temporaries.</b> How many did you use? How many were live "
            "at once? Those are different numbers, and the second one is what a "
            "register allocator cares about.",
            "<b>Compare with a partner.</b> If your instruction counts differ, you "
            "made different choices — find out what they were.",
            "<b>Now the compiler.</b> Implement <code>generateTACExpr</code> and "
            "<code>generateTACStmt</code>, compile that program, and read "
            "<code>out.tac</code>.",
            "<b>Reconcile.</b> Any difference between your listing and the "
            "compiler's is either your mistake or a design choice you did not know "
            "you had made. Which is it?",
            "<b>Hand-execute the TAC.</b> With a table of variable values, step "
            "through your listing and confirm it prints what the source program "
            "should. This is how you will debug phase 6 next week.",
        ]) +
        deliverable(p("Your handwritten TAC, the compiler's <code>out.tac</code>, and "
                      "a numbered list of the differences with an explanation for "
                      "each. This is Lab Question 8.")))


def _a7():
    return (
        meta([("Format", "pairs, at a laptop"), ("Time", "55 min"),
              ("Need", "SPIM or QtSPIM installed")]) +
        h2("The point") +
        p("Get one program all the way to a running executable. Nothing in this course "
          "feels real until that happens.") +
        h2("Do this") +
        steps_list([
            "<b>By hand first.</b> Take three TAC instructions —"
            + code("t0 = 2 + 3\ntotal = t0\nPRINT total")
            + "— and write the MIPS yourself. Assume <code>total</code> lives at "
            "<code>0($sp)</code>. You need <code>li</code>, <code>add</code>, "
            "<code>sw</code>, <code>lw</code>, and the two syscalls.",
            "<b>Assemble and run YOUR hand-written version.</b> Wrap it in a "
            "<code>.text / .globl main / main:</code> skeleton and run "
            "<code>spim -file yours.s</code>. Fix it until it prints 5.",
            "<b>Now implement the code generator</b> for those three TAC opcodes: "
            "<code>TAC_ASSIGN</code>, <code>TAC_ADD</code>, <code>TAC_PRINT</code>.",
            "<b>Diff.</b> Compare the compiler's output with your hand-written "
            "version. Where the compiler emitted more instructions than you did, say "
            "why — and whether the extra ones are actually necessary.",
            "<b>Finish the phase.</b> Add <code>TAC_DECL</code> and "
            "<code>TAC_RETURN</code>, then run every test in <code>tests/</code>.",
        ]) +
        note("note", "The two syscalls you need",
             code("""    li   $v0, 1        # print integer, value in $a0
    syscall

    li   $v0, 10       # exit
    syscall""")) +
        deliverable(p("Your hand-written <code>.s</code> file, the compiler's, a "
                      "screenshot of both running in SPIM, and your answer to step 4. "
                      "This is Lab Questions 9 and 10.")))


def _a8():
    return (
        meta([("Format", "groups of three"), ("Time", "45 min")]) +
        h2("The point") +
        p("A compiler is a user interface. Its users are programmers, and they meet it "
          "almost exclusively through its error messages.") +
        h2("Do this") +
        steps_list([
            "<b>Collect real ones.</b> Each person writes three broken programs — one "
            "lexical error, one syntax error, one semantic error — and runs them "
            "through their own compiler. Paste the actual output.",
            "<b>Score every message</b> against four questions: Does it give the LINE? "
            "Does it name the OFFENDING THING? Does it say what was EXPECTED? Does it "
            "suggest a FIX? Most first drafts score one out of four.",
            "<b>Rewrite the worst three.</b> Aim for four out of four."
            + code("""before:  syntax error

after:   ❌ Syntax Error at line 7:
            Missing semicolon after assignment
            💡 Suggestion: add ';' after 'total = 2 + 3'"""),
            "<b>Implement one of them</b> as a bison error production. See the lecture "
            "notes for the shape.",
            "<b>Swap compilers.</b> Run your broken programs through a group member's "
            "compiler. Whose messages would you rather receive at 2am?",
        ]) +
        h2("A harder question, if you have time") +
        p("What should the compiler do AFTER reporting an error — stop, or keep going? "
          "Try both. Feed a file with five errors to each. There is a real trade-off "
          "here: keeping going can cascade one mistake into twenty spurious ones, and "
          "stopping makes the programmer recompile five times.") +
        deliverable(p("A table of your before/after messages with their four-point "
                      "scores, at least one implemented error production, and a "
                      "paragraph on the stop-or-continue question. This material is "
                      "the strongest thing you can put in your Project 2 video.")))


ACTIVITIES = [
    dict(slug="derivations-and-ambiguity", session="Week 2 · Wednesday",
         title="Derivations, Parse Trees, and Ambiguity",
         lede="Derive by hand, then find two trees for one string — and fix it two different ways.",
         body=_a1),
    dict(slug="first-contact-with-bison", session="Week 2 · Friday",
         title="First Contact with Bison",
         lede="One rule at a time, and a deliberate conflict so you learn to read parser.output.",
         body=_a2),
    dict(slug="parse-tree-vs-ast", session="Week 3 · Wednesday",
         title="Parse Tree vs AST",
         lede="Draw both, count the difference, and decide what your statement list should look like.",
         body=_a3),
    dict(slug="build-the-tree", session="Week 3 · Friday",
         title="Build the Tree, Then Print It",
         lede="Semantic actions, AST constructors, and a deliberate strdup bug that will save you a week.",
         body=_a4),
    dict(slug="symbol-table-and-scope", session="Week 4 · Wednesday",
         title="Predict the Symbol Table",
         lede="Write down what the table will hold before you run anything, then grade your own error messages.",
         body=_a5),
    dict(slug="tac-by-hand", session="Week 4 · Friday",
         title="Three-Address Code by Hand",
         lede="Translate an AST yourself, then make the compiler agree with you.",
         body=_a6),
    dict(slug="first-running-program", session="Week 5 · Wednesday",
         title="Your First Running Program",
         lede="Hand-write the MIPS, run it in SPIM, then make the compiler produce it.",
         body=_a7),
    dict(slug="error-message-clinic", session="Week 5 · Friday",
         title="Error Message Clinic",
         lede="Score your diagnostics out of four, rewrite the worst, and swap compilers.",
         body=_a8),
]
