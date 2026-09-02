"""Topic 1 — Compiler Design Phases.  Lecture notes and two class activities."""

from docgen import (code, pipeline, tabs, stepper, reveal, quiz, note, table,
                    steps_list, p, h2, h3, h4, ul, ol, deliverable, meta)

LECTURE_TITLE = "Six Phases, and the First One for Real"
LECTURE_LEDE = ("What a compiler is made of, why it is made of exactly those pieces, "
                "and how to build the first one so that it survives the next fourteen weeks.")


def lecture():
    return (
        h2("A compiler is a pipeline of small translations") +
        p("A compiler turns text into machine code. Said that way it sounds like one "
          "enormous problem. It is not. It is six small ones, arranged so that each "
          "hands the next a representation that is a little further from how people "
          "write and a little closer to how machines run.") +
        pipeline(active=0) +
        p("Read the diagram as a sequence of data structures, not a sequence of "
          "actions. That is the real content of the design:") +
        table(["Phase", "In", "Out", "The question it answers"], [
            ["1 · Lexical", "characters", "tokens", "Are these words in the language?"],
            ["2 · Syntax", "tokens", "syntax tree", "Do those words form a sentence?"],
            ["3 · Semantic", "syntax tree", "checked tree", "Does the sentence mean anything?"],
            ["4 · IR", "checked tree", "three-address code", "What steps compute it?"],
            ["5 · Optimize", "TAC", "smaller TAC", "Which steps are unnecessary?"],
            ["6 · CodeGen", "TAC", "MIPS assembly", "How does <i>this machine</i> do it?"],
        ]) +
        note("key", "Why six and not one",
             p("Because each boundary is a place you can change one side without "
               "touching the other. Retargeting this compiler from MIPS to ARM means "
               "rewriting phase 6 and nothing else. Adding a <code>while</code> loop "
               "means touching phases 1–4 and nothing in 5 or 6. You will do both of "
               "those things this semester, and you will only be able to do them "
               "quickly because the boundaries exist.")) +

        h2("Phase 1 in one picture") +
        p("The scanner reads characters and emits tokens. A token is three things: "
          "what KIND of thing it is, the exact TEXT that matched, and WHERE it was.") +
        code("""    source :   count  =  count + 1 ;

    tokens :   ID(count)   ASSIGN   ID(count)   PLUS   NUM(1)   SEMI
               │           │                                    │
               │           │                                    └─ line 4, col 19
               │           └─ kind only; the text "=" is not needed again
               └─ kind AND text: the parser will need the name "count\"""") +
        p("The KIND is what the parser makes decisions on. The TEXT matters only for "
          "identifiers and numbers — nobody ever needs to be reminded that "
          "<code>SEMI</code> was spelled <code>;</code>. The LOCATION is what turns "
          "<i>syntax error</i> into <i>line 12, column 7: missing semicolon</i>, and "
          "that difference is most of what people judge a compiler by.") +

        h2("Watch it happen") +
        stepper([
            ("The scanner starts at the first character. Nothing has been recognised yet.",
             code("int total;\n^\n\ntokens: (none)")),
            ("It matches the longest thing it can from here. Three characters spell a keyword.",
             code(">>>int total;\n^^^\n\ntokens: INT")),
            ("Whitespace matches a rule whose action is to produce no token at all — "
             "but it still has to advance the column counter.",
             code("int total;\n   ^\n\ntokens: INT")),
            ("Five letters. This matches the identifier pattern, and no keyword.",
             code("int >>>total;\n    ^^^^^\n\ntokens: INT  ID(total)")),
            ("One punctuation character, one token. The scanner is done; the file ends.",
             code("int total>>>;\n         ^\n\ntokens: INT  ID(total)  SEMI")),
        ]) +

        h2("The two rules that decide everything") +
        p("Flex builds a finite automaton from your rules and runs all of them at "
          "once. When several rules could match, two rules break the tie, in this order:") +
        h3("1. Longest match wins") +
        p("Given <code>&lt;=</code>, the rule for <code>&lt;=</code> beats the rule "
          "for <code>&lt;</code>, because it consumes two characters instead of one. "
          "Where those rules appear in the file makes no difference at all.") +
        code("""    input:  a <= b

    with a "<=" rule:      ID(a)  LE  ID(b)          3 tokens
    without a "<=" rule:   ID(a)  LT  ASSIGN  ID(b)  4 tokens  ← parser will choke""") +
        h3("2. On a tie, the earlier rule wins") +
        p("Given <code>int</code>, the keyword rule and the identifier rule both "
          "match exactly three characters. Now — and only now — order decides. This "
          "is the entire reason keyword rules must be written above the identifier "
          "rule, and it is worth proving to yourself by breaking it.") +
        quiz("A scanner has the identifier rule written ABOVE the keyword rules. "
             "What does it return for the input <code>while</code>?",
             [("WHILE — keywords are special-cased inside the identifier action", False,
               "That is one way to build a scanner, but not what these rules say. "
               "With no special-casing, the rules alone decide."),
              ("ID(while) — both rules match 5 characters, so the earlier rule wins", True,
               "Exactly. Longest match ties at 5, so first match decides, and the "
               "identifier rule was written first. The parser then sees an identifier "
               "where it expected a keyword and reports a syntax error on a line that "
               "looks perfectly correct."),
              ("An error — 'while' is reserved", False,
               "Nothing has told the scanner that 'while' is reserved except the order "
               "of the rules. Reverse the order and the reservation disappears."),
              ("WHILE — longest match prefers keywords", False,
               "Longest match compares LENGTHS, and both matches are 5 characters. It "
               "cannot break this tie; rule order does.")]) +

        h2("What the scanner deliberately does not do") +
        p("It is worth being precise about the boundary, because half the confusion in "
          "this course comes from expecting one phase to do another phase's work.") +
        table(["The scanner DOES", "The scanner does NOT"], [
            ["Recognise <code>while</code> as a keyword", "Know that a <code>while</code> needs a condition after it"],
            ["Recognise <code>)</code> as a delimiter", "Check that parentheses balance"],
            ["Recognise <code>total</code> as an identifier", "Know whether <code>total</code> was declared"],
            ["Report <code>@</code> as not being in the language", "Report <code>int int int;</code> as wrong"],
        ]) +
        p("Every entry in the right-hand column belongs to a later phase. "
          "<code>int int int;</code> is three perfectly good tokens; it is the "
          "<i>parser</i>, in Topic 2, that will object.") +

        h2("Errors are a feature, not an afterthought") +
        p("A scanner that stops at the first bad character makes the programmer "
          "recompile once per typo. Ours reports every lexical error in one run and "
          "keeps going. That costs about four lines:") +
        code("""    .   {
            fprintf(stderr,
              "  LEXICAL ERROR  line %d, col %d: "
              "character '%s' is not part of this language\\n",
              lineNo, colNo, yytext);
            lexErrorCount++;   /* count it   */
            colNo++;           /* step past it */
                               /* and CONTINUE */
        }""") +
        note("warn", "Column numbers are not free",
             p("Flex tracks lines for you with <code>%option yylineno</code>. It does "
               "not track columns. If you want a column number — and you do — you have "
               "to advance a counter yourself in every action, including the ones for "
               "whitespace and comments. Forget the comment case and every line number "
               "after your first multi-line comment will be wrong.")) +

        h2("The same input, four ways") +
        p("Here is what each phase will make of one line of source. You are building "
          "the first column this week; the rest arrive over the next four topics.") +
        tabs([
            ("source", code("int total;\ntotal = 2 + 3;\nprint(total);")),
            ("tokens", code("""INT  ID(total)  SEMI
ID(total)  ASSIGN  NUM(2)  PLUS  NUM(3)  SEMI
PRINT  LPAREN  ID(total)  RPAREN  SEMI""")),
            ("AST", code("""STMT_LIST
  DECL: int total
  ASSIGN: total
    BINOP: +
      NUM: 2
      NUM: 3
  PRINT
    VAR: total""")),
            ("TAC", code("""DECL int total
t0 = 2 + 3
total = t0
PRINT total""")),
            ("MIPS", code("""    li   $t0, 2
    li   $t1, 3
    add  $t2, $t0, $t1
    sw   $t2, 0($sp)      # total
    lw   $a0, 0($sp)
    li   $v0, 1
    syscall""")),
        ]) +
        reveal("Why is the TAC not just  total = 5 ?",
               p("It will be — but not yet. Constant folding happens in phase 5, and "
                 "phase 4's job is a faithful, unclever translation. Mixing the two is "
                 "how compilers get bugs that only appear when optimization is on.")) +

        h2("This week's project") +
        p("Project 1 asks for a lexical analyzer that recognises every token in the "
          "language, reports errors with their exact location, and certifies a file "
          "when it is clean. Four things are worth knowing before you start:") +
        ol([
            "<b>Scan the whole language now, not just Topic 2's part of it.</b> "
            "Recognising <code>switch</code> in week 1 costs one line and saves you "
            "editing this file in week 12.",
            "<b>The token KINDS you choose become bison's <code>%token</code> "
            "declarations in Topic 2.</b> Name them carefully; you will type them "
            "several hundred times.",
            "<b>Make the error messages good.</b> They are the part of this project "
            "you will still be using in December.",
            "<b>Exit non-zero on failure.</b> It is what lets <code>make</code> and a "
            "test script tell success from failure without reading your output.",
        ]) +
        note("note", "Where the code lives",
             p("<code>student/topic-1-lexical-analysis/lexer/</code> — build with "
               "<code>make</code>, self-test with <code>make test</code>. The six test "
               "files in <code>tests/</code> each state their expected result in a "
               "header comment; two of them are supposed to fail."))
    )


# ===========================================================================
# Class activities — one per class meeting (Wednesday and Friday)
# ===========================================================================

def _a1():
    return (
        meta([("Format", "pairs"), ("Time", "35–45 min"),
              ("Bring", "laptop, one sheet of paper")]) +
        h2("The point") +
        p("Before you let a tool tokenize for you, tokenize by hand. Every "
          "disagreement between your answer and the machine's is a rule you had not "
          "noticed you were assuming.") +
        h2("Do this") +
        steps_list([
            "<b>On paper, alone, five minutes.</b> Write the token stream for the "
            "line below. One token per line: KIND, then the text that matched. Do not "
            "run anything yet."
            + code("x=y<=z*2;  // done!"),
            "<b>Compare with your partner.</b> Where you differ, decide which of you "
            "is right and why <i>before</i> you look at any output. Write down each "
            "disagreement in one sentence.",
            "<b>Now run it.</b> Put that line in a file and run the instructor's "
            "lexer over it:"
            + code("cd instructor/topic-1-lexical-analysis/lexer\nmake\n./lexer yourfile.cm"),
            "<b>Account for every difference</b> between your hand answer and the "
            "machine's. For each one, name the rule that explains it: longest match, "
            "first match, or 'that is not the scanner's job'.",
            "<b>Then break it.</b> Add a second line containing a character the "
            "language does not have — <code>x = y @ z;</code> — and confirm the error "
            "names the right line AND the right column. Count the columns by hand to "
            "check.",
        ]) +
        h2("Questions worth arguing about") +
        ul([
            "Is <code>//&nbsp;done!</code> a token? If not, what happened to it, and "
            "which phase would have to care if it were?",
            "How many tokens is <code>&lt;=</code>? How would you find out without "
            "reading the scanner source?",
            "The line has no spaces around <code>=</code>. Did that change anything? "
            "Should it?",
        ]) +
        deliverable(
            p("One shared file, <code>activity1.md</code>, containing:") +
            ul(["your two hand-written token streams (before you ran anything),",
                "the machine's output,",
                "a numbered list of every disagreement, each with the one-sentence rule that explains it,",
                "the error message from step 5, with the column verified by hand."]) +
            p("Bring it to the next class. You will need the token-kind list for "
              "Project 1."))
    )


def _a2():
    return (
        meta([("Format", "pairs"), ("Time", "45 min"),
              ("Bring", "a working build of the Topic 1 lexer")]) +
        h2("The point") +
        p("Four experiments, each of which breaks the scanner in a specific way. "
          "Predict the outcome first, then run it. A prediction you got wrong teaches "
          "more than three that you got right, so write the prediction down before "
          "you run anything — otherwise you will remember having predicted correctly.") +
        note("note", "Work on a copy",
             p("<code>cp -r instructor/topic-1-lexical-analysis/lexer /tmp/broken</code> "
               "and vandalise that. You want the original intact for comparison.")) +
        h2("The experiments") +
        steps_list([
            "<b>Move the identifier rule above the keyword rules.</b> Predict what "
            "<code>tests/03_keywords_vs_ids.cm</code> will produce, then run it. Which "
            "of the two tie-breaking rules did you just change, and why did longest "
            "match not save you?",
            "<b>Delete the <code>&quot;&lt;=&quot;</code> rule.</b> Predict the token "
            "count for <code>tests/02_longest_match.cm</code>, then run it. You should "
            "be able to say the exact number before you look.",
            "<b>Move the <code>&quot;&lt;&quot;</code> rule above "
            "<code>&quot;&lt;=&quot;</code></b> (with both present). Predict, then run. "
            "This one surprises people — explain in one sentence why nothing changed.",
            "<b>Make the error action call <code>exit(1)</code> instead of counting "
            "and continuing.</b> Run <code>tests/05_lexical_errors.cm</code>, which "
            "contains four bad characters. How many did you find out about? Now imagine "
            "that file is 4,000 lines long.",
            "<b>Delete the <code>skip()</code> call from the block-comment rule</b> "
            "(leave the rule itself). Run <code>tests/04_comments.cm</code> and look at "
            "the line numbers. This is the bug the header comment in that test warns "
            "you about — now you have seen it.",
        ]) +
        h2("One design question, no experiment") +
        p("Our language has no string literals. Suppose you wanted to add them: "
          "<code>print(&quot;total = &quot;);</code>") +
        ul([
            "What pattern would match a string literal? Write it.",
            "What should happen if the closing quote is missing before end of line?",
            "Which phase should reject <code>&quot;abc&quot; + 1</code> — the scanner, "
            "the parser, or the semantic analyzer? Defend your answer in one sentence.",
        ]) +
        reveal("A hint on the third question",
               p("Ask what each phase can actually see. The scanner sees one token at "
                 "a time and has no idea what surrounds it. The parser sees the shape "
                 "of the expression but knows nothing about types. Only one phase in "
                 "this course is in a position to notice that a string and an integer "
                 "cannot be added.")) +
        deliverable(
            p("Extend <code>activity1.md</code> (or start <code>activity2.md</code>) with:") +
            ul(["for each of the five experiments: your written prediction, what "
                "actually happened, and one sentence reconciling them;",
                "your answers to the three string-literal questions;",
                "one sentence on which experiment surprised you most and why."]) +
            p("This material shows up directly in Lab Questions 1 and 2 and in your "
              "Project 1 video — the video asks you to explain design practices and "
              "implementation strategies, and 'here is what happens when you get rule "
              "order wrong' is exactly that."))
    )


ACTIVITIES = [
    dict(slug="tokenize-by-hand", session="Wednesday",
         title="Tokenize by Hand, Then by Machine",
         lede="Write the token stream yourself, then find out where you and flex disagree — "
              "and why.",
         body=_a1),
    dict(slug="break-the-scanner", session="Friday",
         title="Break the Scanner on Purpose",
         lede="Five experiments that each break the scanner in one specific way. "
              "Predict first, then run.",
         body=_a2),
]
