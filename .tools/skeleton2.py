#!/usr/bin/env python3
"""
skeleton2.py — build the Topic 2 STUDENT skeleton from the Topic 2 instructor
compiler.

Topic 2 is the odd one out.  Every other student folder is "the previous
milestone plus TODOs", which stagegen.py produces from the stage markers.
Topic 2 has no previous milestone: Project 2 asks students to build a whole
compiler for the first time, so almost everything has to come out.

What is GIVEN and what is REMOVED is a pedagogical decision, not a mechanical
one, so it is spelled out here rather than inferred:

  GIVEN   scanner.l           they wrote this in Project 1; a common reference
                              version keeps everyone on the same footing
          all .h files        the data structures ARE the design; handing them
                              over is what makes the six phases fit together
          parser.y prologue   %union, %token, precedence, yyerror
          tac.c machinery     temp/label allocation, list handling
          codegen.c PARTS 1-3 register cache, addressing, frame layout
          main.c              the driver, so they can see the phase order

  REMOVED grammar rules and their semantic actions      (Phase 2)
          AST constructors and the tree printer         (Phase 2)
          symbol table insert/lookup                    (Phase 3)
          the semantic checks                           (Phase 3)
          AST -> TAC translation                        (Phase 4)
          the optimizer                                 (Phase 5)
          TAC -> MIPS instruction selection             (Phase 6)

Run by stagegen.py; also runnable on its own.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC  = os.path.join(ROOT, "instructor", "topic-2-minimal-compiler", "compiler")
DST  = os.path.join(ROOT, "student",    "topic-2-minimal-compiler", "compiler")


def todo(title, lines, indent=""):
    # A "*/" inside the body would close the comment early and produce a wall
    # of nonsense errors in a file the student has not touched yet.
    for l in lines:
        assert "*/" not in l, "TODO text would close its own comment: " + l
    w = 68 - len(indent)
    out = [indent + "/* " + "-" * w,
           indent + " * TODO (Topic 2) — " + title]
    for l in lines:
        out.append((indent + " * " + l).rstrip())
    out.append(indent + " * " + "-" * w + " */")
    return "\n".join(out) + "\n"


def cut(text, start, end, replacement, keep_end=True):
    """Replace text[start_anchor : end_anchor) with `replacement`."""
    i = text.index(start)
    j = text.index(end, i)
    return text[:i] + replacement + (text[j:] if keep_end else "")


# ---------------------------------------------------------------------------
def build_parser(text):
    # Bison rejects a %type for a non-terminal with no rules, so the skeleton
    # declares only `program` (which has a placeholder rule) and leaves the
    # rest in the TODO for students to restore as they write each rule.
    text = text.replace(
        "%type <node> program stmt_list stmt decl assign expr print_stmt",
        "/* Every non-terminal that yields an AST node must be declared here.\n"
        " * Add to this line as you add rules:\n"
        " *   %type <node> program stmt_list stmt decl assign expr print_stmt\n"
        " * (bison rejects a %type for a non-terminal that has no rules yet,\n"
        " *  which is why only `program` is listed to begin with) */\n"
        "%type <node> program")
    return cut(text, "%%\n\n", "\n%%\n", """%%

""" + todo("THE GRAMMAR", [
 "Everything above this line is given: the token declarations, the",
 "precedence table, and the union that lets a rule hand back an ASTNode*.",
 "Below it, write the rules.  Each rule needs a semantic action in { }",
 "that builds one AST node and assigns it to $$.",
 "",
 "THE GRAMMAR YOU ARE IMPLEMENTING",
 "",
 "    program     ->  stmt_list",
 "    stmt_list   ->  stmt  |  stmt_list stmt",
 "    stmt        ->  decl  |  assign  |  print_stmt",
 "    decl        ->  'int' ID ';'",
 "    assign      ->  ID '=' expr ';'",
 "    expr        ->  NUM  |  ID  |  expr '+' expr",
 "    print_stmt  ->  'print' '(' expr ')' ';'",
 "",
 "THE ACTIONS YOU NEED",
 "",
 "    program    : stmt_list          { root = $1; }",
 "    stmt_list  : stmt_list stmt     { $$ = createStmtList($1, $2); }",
 "    decl       : INT ID ';'         { $$ = createDecl(\"int\", $2); free($2); }",
 "    assign     : ID '=' expr ';'    { $$ = createAssign($1, $3); free($1); }",
 "    expr       : expr '+' expr      { $$ = createBinOp('+', $1, $3); }",
 "    print_stmt : PRINT '(' expr ')' ';'  { $$ = createPrint($3); }",
 "",
 "TWO THINGS THAT WILL BITE YOU",
 "",
 "  free($2) on an ID.  The scanner strdup'd the identifier text; the AST",
 "  constructor strdup's it again.  Whoever received it from the scanner",
 "  has to free it, and that is this rule.  Skip it and the compiler",
 "  leaks — small here, embarrassing under valgrind in Topic 6.",
 "",
 "  `root` is a global declared in the prologue above.  The `program` rule",
 "  is the ONLY place that assigns it.  If root stays NULL after a",
 "  successful parse, that assignment is missing and every later phase",
 "  will silently do nothing.",
 "",
 "GOING FURTHER (worth doing, and worth talking about in your video)",
 "",
 "  Add ERROR PRODUCTIONS so that a missing semicolon produces",
 "    \"line 4: missing ';' after assignment to x\"",
 "  instead of \"syntax error\".  The shape is:",
 "    | ID '=' expr error  { report it; $$ = NULL; yyerrok; }",
 "  Error messages are most of what people judge a compiler by.",
]) + """
/* A placeholder so that `make` succeeds before you have written anything.
 * It accepts exactly one program — the empty one — and builds no tree.
 * Delete it as soon as you have a real `program` rule. */
program:
    /* empty */ { root = NULL; }
    ;

/* TODO: write your grammar rules here. */

""", keep_end=True)


def build_ast(text):
    # keep createNum and createVar as worked examples; blank the rest
    text = cut(text, "/* Create a binary operation node", "/* Display the AST structure",
        todo("THE REMAINING AST CONSTRUCTORS", [
 "createNum and createVar above are the pattern.  Every constructor does",
 "the same four things:",
 "",
 "    ASTNode* node = malloc(sizeof(ASTNode));",
 "    node->type   = NODE_XXX;          <- which kind of node this is",
 "    node->lineno = yylineno;          <- where it came from, for errors",
 "    ... store the children ...",
 "    return node;",
 "",
 "Write: createBinOp, createDecl, createAssign, createPrint, createStmtList.",
 "",
 "strdup every char* you store.  The scanner's buffer is reused for the",
 "next token, so a name you merely point at will have changed by the time",
 "the semantic analyzer reads it.  That bug looks like the AST being",
 "randomly corrupted, and it is one of the hardest to find in this course.",
 "",
 "createStmtList is the one worth thinking about: it links two statements",
 "into a list, and the grammar is LEFT recursive, so $1 is the list so far",
 "and $2 is the new statement.  Draw the tree for a three-statement",
 "program before you write it.",
]) + "\n\n")
    # printAST is the last function in the file, so cut to the end
    i = text.index("void printAST(ASTNode* node, int level)")
    text = text[:i] + "void printAST(ASTNode* node, int level) {\n" + (
        todo("THE TREE PRINTER", [
 "Print the tree, one node per line, indented two spaces per level.",
 "",
 "    if (!node) return;",
 "    for (int i = 0; i < level; i++) printf(\"  \");",
 "    switch (node->type) { ... one case per node kind ... }",
 "",
 "Recurse into children with level + 1 so the indentation shows the shape.",
 "NODE_STMT_LIST is the exception: print its two children at the SAME",
 "level, because a list of statements is a sequence, not a nesting.",
 "",
 "This function is not decoration.  It is the only window you have into",
 "Phase 2, and every bug you hit for the rest of the semester gets",
 "diagnosed by staring at its output.  Write it early and make it good.",
], "    ") + "}\n")
    return text


def build_symtab(text):
    text = cut(text, "int addVar(char* name, char* type) {", "int addArray(char* name, int size) {",
        "int addVar(char* name, char* type) {\n" +
        todo("DECLARE A VARIABLE", [
 "Add `name` to the local table and give it a home in the frame.",
 "Return the byte offset you assigned, or -1 if the name is already",
 "declared — the caller uses -1 to report a duplicate declaration.",
 "",
 "Each int takes 4 bytes, and offsets run upward from 0.  So the first",
 "variable lives at 0($sp), the second at 4($sp), and nextOffset is",
 "simply the running total.",
 "",
 "findIn() and appendTo() above do the searching and the allocation.",
], "    ") + "    return -1;\n}\n\n")
    text = cut(text, "Symbol* lookupSymbol(const char* name) {", "int getVarOffset(char* name) {",
        "Symbol* lookupSymbol(const char* name) {\n" +
        todo("RESOLVE A NAME", [
 "Return the symbol for `name`, or NULL if it is not declared.",
 "Search the LOCAL table first and the GLOBAL table second: that order is",
 "what makes an inner declaration shadow an outer one, and it is the",
 "entire implementation of scoping at this milestone.",
], "    ") + "    (void)name;\n    return NULL;\n}\n\n")
    return text


def build_semantic(text):
    text = cut(text, "static void checkExpr(ASTNode* node) {", "/* Check statement */",
        "static void checkExpr(ASTNode* node) {\n" +
        todo("CHECK AN EXPRESSION", [
 "Walk the expression and report anything that cannot mean what it says.",
 "",
 "    NODE_NUM    always fine",
 "    NODE_VAR    the name must be declared and VISIBLE here",
 "                -> isVarDeclaredInScope(node->data.name)",
 "    NODE_BINOP  nothing to check about the operator itself; recurse into",
 "                both operands",
 "",
 "When you report an error: give the LINE NUMBER (node->lineno), name the",
 "identifier, and say what would fix it.  Compare these two messages and",
 "decide which one you would rather receive:",
 "",
 "    error: undeclared identifier",
 "    line 7: 'totl' is not declared — did you mean 'total'?",
 "",
 "Increment semInfo.errorCount for each error.  Do NOT stop at the first",
 "one: report everything you can find in a single run.",
], "    ") + "    (void)node;\n}\n\n")
    text = cut(text, "static void checkStmt(ASTNode* node) {", "/* Check statement list */",
        "static void checkStmt(ASTNode* node) {\n" +
        todo("CHECK A STATEMENT", [
 "    NODE_DECL    the name must NOT already be declared in this scope.",
 "                 On success, add it: addVarToScope(name).",
 "    NODE_ASSIGN  the target must already be declared; then check the",
 "                 expression on the right with checkExpr.",
 "    NODE_PRINT   check the expression.",
 "    NODE_STMT_LIST  recurse into both halves via checkStmtList.",
 "",
 "Order matters in NODE_ASSIGN and it is easy to get backwards.  For",
 "    int x;  x = x + 1;",
 "checking the right-hand side must happen with x already in scope.  For",
 "    int x = x + 1;",
 "(a form this language does not have — but think about it) it should not.",
 "Languages differ here, and this is where that decision gets made.",
], "    ") + "    (void)node;\n}\n\n")
    return text


def build_tac(text):
    text = cut(text, "char* generateTACExpr(ASTNode* node) {", "/* Generate TAC for statement list */",
        "char* generateTACExpr(ASTNode* node) {\n" +
        todo("EXPRESSION -> THREE-ADDRESS CODE", [
 "Return the NAME of the location holding this expression's value.  That",
 "return value is the whole contract, and it is what makes the recursion",
 "work: a caller does not care whether it gets back a literal, a variable",
 "or a temporary, only that it can name the value.",
 "",
 "    NODE_NUM    return a string holding the literal, e.g. \"42\"",
 "    NODE_VAR    return a copy of the variable's name",
 "    NODE_BINOP  t = allocTemp();",
 "                left  = generateTACExpr(left child)",
 "                right = generateTACExpr(right child)",
 "                emit  t = left + right",
 "                freeTemp(left); freeTemp(right);",
 "                return t",
 "",
 "Free the operand temporaries AFTER emitting, never before: freeing t1",
 "and then using it in the instruction you are about to emit is how you",
 "end up with two live values in the same temporary.",
 "",
 "For  a + b + c  you should get exactly three instructions.  If you get",
 "four, or if a temporary number is reused while still live, print the",
 "TAC and walk it by hand — that listing is the point of this phase.",
], "    ") + "    (void)node;\n    return NULL;\n}\n\n")
    text = cut(text, "static void generateTACStmt(ASTNode* node) {\n    if", "void generateTAC(ASTNode* node) {",
        "static void generateTACStmt(ASTNode* node) {\n" +
        todo("STATEMENT -> THREE-ADDRESS CODE", [
 "    NODE_DECL    emit TAC_DECL — no code runs, but the back end needs to",
 "                 know the variable exists so it can reserve a slot",
 "    NODE_ASSIGN  evaluate the expression, then emit TAC_ASSIGN",
 "    NODE_PRINT   evaluate the expression, then emit TAC_PRINT",
 "    NODE_STMT_LIST  recurse",
 "",
 "Use appendTAC(createTAC(op, arg1, arg2, result)) to emit.",
], "    ") + "    (void)node;\n}\n\n")
    text = cut(text, "static TACList optimizePass(TACList* in) {", "void optimizeTAC(void) {",
        "static TACList optimizePass(TACList* in) {\n" +
        todo("ONE OPTIMIZATION PASS", [
 "Copy `in` to `out`, rewriting what you can along the way.  Start with",
 "the two transformations that pay off immediately on this language:",
 "",
 "  CONSTANT FOLDING     t0 = 2 + 3      ->   t0 = 5",
 "                       Both operands are literals, so do the arithmetic",
 "                       now instead of at run time.  foldConstants() is",
 "                       already written for you.",
 "",
 "  CONSTANT PROPAGATION x = 5 ; y = x + 1   ->   y = 5 + 1",
 "                       Remember that x holds 5, and substitute it into",
 "                       later operands.  Then folding turns that into 6,",
 "                       which is why these two techniques belong together.",
 "",
 "  THE RULE YOU MUST NOT BREAK: forget every remembered value at a LABEL.",
 "  Control can arrive at a label from anywhere, so nothing you learned",
 "  before it is still guaranteed.  Topic 2 has no labels yet — but write",
 "  the code as if it did, because Topic 4 will add them and you will not",
 "  remember this warning then.",
 "",
 "Count every rewrite in changesThisPass so optimizeTAC() knows whether to",
 "run again, and in the matching optStats field so main.c can report it.",
], "    ") + "    TACList out = { NULL, NULL, in->tempCount, in->labelCount };\n"
   "    for (TACInstr* c = in->head; c; c = c->next) {\n"
   "        TACInstr* n = createTAC(c->op, c->arg1, c->arg2, c->result);\n"
   "        if (!out.head) out.head = out.tail = n;\n"
   "        else { out.tail->next = n; out.tail = n; }\n"
   "    }\n    return out;\n}\n\n")
    return text


def build_codegen(text):
    i = text.index("        for (TACInstr* i = c->next; i && i->op != TAC_FUNC_END; i = i->next) {")
    j = text.index("        flushRegisters(\"end of function body\");")
    return text[:i] + """        for (TACInstr* i = c->next; i && i->op != TAC_FUNC_END; i = i->next) {
""" + todo("TAC -> MIPS", [
 "One case per TAC opcode.  Everything you need is already written above:",
 "",
 "    operandReg(name)   register holding that value (loads it, or does",
 "                       `li` if it is a literal)",
 "    defReg(name)       register to WRITE a new value of `name` into",
 "    flushRegisters()   write every dirty register back to memory",
 "",
 "  TAC_DECL     no instruction — the slot was reserved by layoutFrame().",
 "               Emit a comment saying where it lives; you will be glad of",
 "               it the first time you read your own assembly.",
 "",
 "  TAC_ASSIGN   result = arg1",
 "                   int a = operandReg(i->arg1);",
 "                   int d = defReg(i->result);",
 "                   move $td, $ta",
 "",
 "  TAC_ADD      result = arg1 + arg2   ->   add $td, $ta, $tb",
 "",
 "  TAC_PRINT    print arg1, using the SPIM syscalls:",
 "                   move $a0, $t<arg>",
 "                   li   $v0, 1        # 1 = print integer",
 "                   syscall",
 "                   la   $a0, __nl     # then a newline",
 "                   li   $v0, 4        # 4 = print string",
 "                   syscall",
 "",
 "  TAC_RETURN   put the value in $v0, then jump to the epilogue label.",
 "               Do NOT just fall through.",
 "",
 "WHY defReg AND operandReg ARE DIFFERENT",
 "  operandReg must LOAD the value from memory if it is not already in a",
 "  register.  defReg must not: the register is about to be overwritten,",
 "  so loading first is a wasted instruction.  Use the wrong one and your",
 "  code still works — just with an extra `lw` everywhere.  Reading your",
 "  own output and spotting that is a genuinely good exercise.",
], "            ") + """        }

""" + text[j:]


BUILDERS = {
    "parser.y":   build_parser,
    "ast.c":      build_ast,
    "symtab.c":   build_symtab,
    "semantic.c": build_semantic,
    "tac.c":      build_tac,
    "codegen.c":  build_codegen,
}

BANNER_TASK = """ *
 * YOUR TASK
 *   This is Project 2: the first compiler you build end to end.  Sections
 *   marked  TODO (Topic 2)  are yours.  Everything else — the headers, the
 *   scanner, the driver, the register allocator — is given, because the
 *   point of this project is the six PHASES, not the plumbing between them.
"""


def main():
    if not os.path.isdir(SRC):
        print("skeleton2: run stagegen first (no %s)" % SRC)
        return 1
    if os.path.isdir(DST):
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)
    for name in os.listdir(DST):
        p = os.path.join(DST, name)
        if not os.path.isfile(p):
            continue
        if name in ("minicompiler",) or name.endswith(".o"):
            os.remove(p)
            continue
        text = open(p).read()
        if name in BUILDERS:
            text = BUILDERS[name](text)
        if name.endswith((".c", ".h", ".y", ".l")):
            text = text.replace(" * ==========", BANNER_TASK + " * ==========", 1)
        open(p, "w").write(text)
    print("generated student    topic 2 -> %s" % os.path.relpath(DST, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
