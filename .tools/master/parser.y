%{
/* PHASE 2 — SYNTAX ANALYSIS
 *
 * The parser answers one question: do these tokens form a legal program?
 * Bison builds an LALR(1) bottom-up parser from the grammar below.  It reads
 * tokens left to right, shifts them onto a stack, and REDUCES whenever the
 * top of the stack matches the right-hand side of a rule.
 *
 * Answering "yes" is not enough, though — the rest of the compiler needs the
 * program's STRUCTURE.  So each rule carries a semantic action in { } that
 * builds one node of the abstract syntax tree.  $1, $2, ... are the values of
 * the symbols on the right-hand side; $$ is the value this rule hands back.
 *
 *      expr '+' expr   { $$ = createBinOp('+', $1, $3); }
 *       │        │                              │   └── right operand
 *       │        └── $3                         └────── left operand
 *       └── $1
 *
 * By the time yyparse() returns, the tree has been built bottom-up beneath us
 * and `root` points at the whole program.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ast.h"

/* External declarations for lexer interface */
extern int yylex();
extern int yyparse();
extern FILE* yyin;
extern int yylineno;  /* Line number from scanner */

void yyerror(const char* s);
ASTNode* root = NULL;
%}

/* SEMANTIC VALUES UNION */
%union {
    int num;
    char* str;
    struct ASTNode* node;
}

/* TOKEN DECLARATIONS */
%token <num> NUM
%token <str> ID
%token INT PRINT
/*#3*/
/*#todo Functions need one more keyword token: RETURN.*/
%token RETURN
/*#end*/
/*#4*/
/*#todo Declare the loop keywords: WHILE FOR BREAK.*/
%token WHILE FOR BREAK
/*#end*/
/*#4*/
/*#todo Declare the two-character relational operator tokens: LE GE EQ NE.*/
/*#todo (The single-character ones, < and >, arrive as character literals and*/
/*#todo  need no %token declaration.)*/
%token LE GE EQ NE
/*#end*/
/*#5*/
/*#todo Declare the decision keywords and logical operators:*/
/*#todo   IF ELSE SWITCH CASE DEFAULT AND OR*/
%token IF ELSE SWITCH CASE DEFAULT
%token AND OR
/*#end*/

/* NON-TERMINAL TYPES */
%type <node> program stmt_list stmt decl assign expr print_stmt
/*#3*/
/*#todo Declare the types of the new non-terminals, or bison will not know*/
/*#todo that their $$ is an ASTNode*:*/
/*#todo   decl_or_func_list decl_or_func func_def params param_list param*/
/*#todo   return_stmt block func_call arg_list args*/
%type <node> decl_or_func_list decl_or_func func_def params param_list param
%type <node> return_stmt block func_call arg_list args
/*#end*/
/*#4*/
/*#todo Every new non-terminal needs its type declared here, or bison will*/
/*#todo not know that $$ is an ASTNode*.  Add: while_stmt for_stmt*/
/*#todo for_init for_cond for_update break_stmt*/
%type <node> while_stmt for_stmt for_init for_cond for_update break_stmt
/*#end*/
/*#5*/
/*#todo Add the decision non-terminals: if_stmt switch_stmt case_list*/
/*#todo case_clause opt_stmt_list*/
%type <node> if_stmt switch_stmt case_list case_clause opt_stmt_list
/*#end*/

/* OPERATOR PRECEDENCE AND ASSOCIATIVITY
 * Listed from lowest to highest precedence.
 *
 * DANGLING-ELSE RESOLUTION:
 *   The grammar has an ambiguity: in  if (c) if (c) s  else s
 *   the "else" can bind to either "if".  The standard resolution
 *   is that else binds to the nearest (innermost) if.
 *
 *   We express this by giving the if-without-else rule a lower
 *   precedence (%prec LOWER_THAN_ELSE) than the ELSE token, so
 *   when bison sees ELSE it shifts (attaches it to the inner if)
 *   rather than reducing (closing the outer if first).
 */
/*#5*/
/*#todo Resolve the dangling-else ambiguity and give the logical operators*/
/*#todo their precedence.  Four lines, and their ORDER is the whole answer:*/
/*#todo   %nonassoc LOWER_THAN_ELSE*/
/*#todo   %nonassoc ELSE*/
/*#todo   %left OR*/
/*#todo   %left AND*/
/*#todo Ask yourself why OR must be listed BEFORE AND, and what would break*/
/*#todo if ELSE were listed before LOWER_THAN_ELSE.*/
%nonassoc LOWER_THAN_ELSE  /* pseudo-token: lower prec than ELSE */
%nonassoc ELSE             /* ELSE has higher prec → shifts over */
%left OR                   /* lowest: a || b || c groups left        */
%left AND                  /* && binds tighter than ||               */
/*#end*/
/*#4*/
/*#todo Give the relational operators their precedence.  They bind LOOSER*/
/*#todo than + - * /, which is what makes  a + 1 < b * 2  parse as*/
/*#todo   (a + 1) < (b * 2)  and not  a + (1 < b) * 2.*/
%left EQ NE
%left '<' '>' LE GE
/*#end*/
%left '+' '-'
%left '*' '/'
/*#3*/
%right UMINUS              /* unary minus                            */
/*#end*/
/*#5*/
/*#todo Unary ! binds at least as tightly as unary minus.  Declare it:*/
/*#todo   %right NOT*/
%right NOT                 /* highest: unary !                       */
/*#end*/

%%

/*#2!*/
/* PROGRAM RULE — in the starter language a program IS a list of statements.
 * Topic 3 replaces this rule the moment functions arrive. */
program:
    stmt_list { root = $1; }
    ;
/*#end*/
/*#3*/
/*#todo A program is no longer a flat list of statements.  It is a list of*/
/*#todo top-level DECLARATIONS and FUNCTION DEFINITIONS:*/
/*#todo   program           : decl_or_func_list*/
/*#todo   decl_or_func_list : decl_or_func | decl_or_func_list decl_or_func*/
/*#todo   decl_or_func      : func_def | decl*/
/*#todo Executable statements now live only inside a function body — which*/
/*#todo is why `main` suddenly matters.*/
/* PROGRAM RULE - Entry point */
program:
    decl_or_func_list {
        root = $1;
    }
    ;

/* Declaration or function list */
decl_or_func_list:
    decl_or_func {
        $$ = $1;
    }
    | decl_or_func_list decl_or_func {
        $$ = createStmtList($1, $2);
    }
    ;

/* Can be either a function definition or a variable declaration */
decl_or_func:
    func_def { $$ = $1; }
    | decl { $$ = $1; }
    ;

/*#end*/

/*#3*/
/*#todo FUNCTION DEFINITIONS, PARAMETERS and BLOCKS.*/
/*#todo   func_def   : INT ID '(' params ')' block  |  INT ID '(' ')' block*/
/*#todo   param_list : param | param_list ',' param*/
/*#todo   param      : INT ID           (a scalar parameter)*/
/*#todo              | INT ID '[' ']'   (an array parameter — note: no size)*/
/*#todo   block      : '{' stmt_list '}' | '{' '}'*/
/*#todo An array parameter carries no size because arrays are passed by*/
/*#todo REFERENCE: the callee receives an address, not a copy of the data.*/
/* FUNCTION DEFINITION - int name(params) { body } */
func_def:
    INT ID '(' params ')' block {
        $$ = createFuncDef($2, $4, $6);
        free($2);
    }
    | INT ID '(' ')' block {
        $$ = createFuncDef($2, NULL, $5);
        free($2);
    }
    ;

/* PARAMETERS */
params:
    param_list { $$ = $1; }
    ;

param_list:
    param {
        $$ = $1;
    }
    | param_list ',' param {
        $$ = createParamList($1, $3);
    }
    ;

param:
    INT ID {
        $$ = createParam($2);
        free($2);
    }
    | INT ID '[' ']' {
        $$ = createArrayParam($2);
        free($2);
    }
    ;

/* BLOCK STATEMENT */
block:
    '{' stmt_list '}' {
        $$ = createBlock($2);
    }
    | '{' '}' {
        $$ = createBlock(NULL);
    }
    ;

/*#end*/

/* STATEMENT LIST */
stmt_list:
    stmt {
        $$ = $1;
    }
    | stmt_list stmt {
        $$ = createStmtList($1, $2);
    }
    ;

/* STATEMENT TYPES */
stmt:
    decl
    | assign
    | print_stmt
/*#3*/
/*#todo A `return`, a `{ ... }` block, and a bare function call used for its*/
/*#todo effect are all statements now.  Add three alternatives:*/
/*#todo   | return_stmt      | block      | func_call ';'*/
    | return_stmt
/*#end*/
/*#4*/
/*#todo A loop and a `break` are statements too.  Add them as alternatives:*/
/*#todo   | while_stmt*/
/*#todo   | for_stmt*/
/*#todo   | break_stmt*/
    | while_stmt
    | for_stmt
    | break_stmt
/*#end*/
/*#5*/
/*#todo Add the decision statements: if_stmt and switch_stmt.*/
    | if_stmt
    | switch_stmt
/*#end*/
/*#3*/
    | block
    | func_call ';' { $$ = $1; }
/*#end*/
    ;

/*#5*/
/*#todo SWITCH STATEMENT.*/
/*#todo*/
/*#todo   switch_stmt : SWITCH '(' expr ')' '{' case_list '}'*/
/*#todo   case_list   : (empty) | case_list case_clause*/
/*#todo   case_clause : CASE NUM ':' opt_stmt_list | DEFAULT ':' opt_stmt_list*/
/*#todo   opt_stmt_list : (empty) | stmt_list*/
/*#todo*/
/*#todo case_list builds a LINKED LIST of clauses in source order — append to*/
/*#todo the tail, do not prepend, because fall-through depends on the order.*/
/*#todo A case body may be empty; that is how `case 4: case 5: ...` works.*/
/* SWITCH STATEMENT - switch (expr) { case_list } */
switch_stmt:
    SWITCH '(' expr ')' '{' case_list '}' {
        $$ = createSwitch($3, $6);
    }
    ;

/* CASE LIST - zero or more case/default clauses */
case_list:
    /* empty */ {
        $$ = NULL;
    }
    | case_list case_clause {
        /* Append case_clause to end of the linked list */
        if ($1 == NULL) {
            $$ = $2;
        } else {
            ASTNode* tail = $1;
            while (tail->data.case_clause.next)
                tail = tail->data.case_clause.next;
            tail->data.case_clause.next = $2;
            $$ = $1;
        }
    }
    ;

/* CASE CLAUSE - case N: stmts  or  default: stmts */
case_clause:
    CASE NUM ':' opt_stmt_list {
        $$ = createCase($2, 0, $4);
    }
    | DEFAULT ':' opt_stmt_list {
        $$ = createCase(0, 1, $3);
    }
    ;

/* OPTIONAL STATEMENT LIST - body of a case clause (may be empty) */
opt_stmt_list:
    /* empty */ {
        $$ = NULL;
    }
    | stmt_list {
        $$ = $1;
    }
    ;

/*#end*/

/*#4*/
/*#todo BREAK STATEMENT.  One rule, one action:*/
/*#todo   break_stmt: BREAK ';' { $$ = createBreak(); } ;*/
/* BREAK STATEMENT — leave the innermost loop (Topic 5: or switch) early */
break_stmt:
    BREAK ';' {
        $$ = createBreak();
    }
    ;
/*#end*/

/* DECLARATION - int x; or int arr[10]; */
decl:
    INT ID ';' {
        $$ = createDecl("int", $2);
        free($2);
    }
/*#3*/
/*#todo Array declaration:  int arr[10];*/
/*#todo The size is a NUM, not an expression — the compiler must know how many*/
/*#todo bytes to reserve, and it must know that at compile time.*/
    | INT ID '[' NUM ']' ';' {
        $$ = createArrayDecl($2, $4);
        free($2);
    }
/*#end*/
    ;

/* ASSIGNMENT - x = expr; or arr[i] = expr; */
assign:
    ID '=' expr ';' {
        $$ = createAssign($1, $3);
        free($1);
    }
/*#3*/
/*#todo Assignment to an array ELEMENT:  arr[i] = expr;*/
/*#todo The left-hand side is now a tree, not just a name, so the assignment node*/
/*#todo stores it in arrayLHS and leaves `var` NULL.*/
    | ID '[' expr ']' '=' expr ';' {
        ASTNode* lhs = createArrayIndex($1, $3);
        $$ = createAssign(NULL, $6);
        $$->data.assign.arrayLHS = lhs;
        free($1);
    }
/*#end*/
    ;

/*#3*/
/*#todo RETURN, in both forms:  return expr;  and  return;*/
/* RETURN STATEMENT */
return_stmt:
    RETURN expr ';' {
        $$ = createReturn($2);
    }
    | RETURN ';' {
        $$ = createReturn(NULL);
    }
    ;

/*#end*/
/*#5*/
/*#todo IF STATEMENT — two forms, and the dangling-else problem.*/
/*#todo*/
/*#todo   if_stmt : IF '(' expr ')' stmt %prec LOWER_THAN_ELSE*/
/*#todo           | IF '(' expr ')' stmt ELSE stmt*/
/*#todo*/
/*#todo Build them with createIf(cond, thenStmt, elseStmt); pass NULL for*/
/*#todo elseStmt in the first form.  The %prec marker is what tells bison to*/
/*#todo attach a trailing `else` to the NEAREST `if`.  Build it once without*/
/*#todo the marker and read the conflict report — that report is the lesson.*/
/* IF STATEMENT
 * Two forms:
 *   if (expr) stmt              - no else clause
 *   if (expr) stmt else stmt    - with else clause
 *
 * %prec LOWER_THAN_ELSE on the first rule tells bison that when
 * the lookahead is ELSE this rule has lower precedence, so bison
 * shifts the ELSE and attaches it to the innermost if (correct
 * dangling-else behaviour).  Without this marker bison still
 * resolves the conflict the same way but reports it as a warning.
 */
if_stmt:
    IF '(' expr ')' stmt %prec LOWER_THAN_ELSE {
        /* if-without-else: else_stmt is NULL */
        $$ = createIf($3, $5, NULL);
    }
    | IF '(' expr ')' stmt ELSE stmt {
        /* if-with-else: captures the else branch */
        $$ = createIf($3, $5, $7);
    }
    ;

/*#end*/

/*#4*/
/*#todo WHILE and FOR.*/
/*#todo*/
/*#todo   while_stmt : WHILE '(' expr ')' stmt          -> createWhile(cond, body)*/
/*#todo   for_stmt   : FOR '(' for_init ';' for_cond ';' for_update ')' stmt*/
/*#todo                                                  -> createFor(init,cond,update,body)*/
/*#todo*/
/*#todo All three parts of a for-header are OPTIONAL, so for_init, for_cond*/
/*#todo and for_update each need an empty alternative that yields NULL.*/
/*#todo Note what for_init is NOT: it is an assignment WITHOUT a semicolon,*/
/*#todo because the `;` belongs to the for-header, not to the assignment.*/
/* WHILE LOOP */
while_stmt:
    WHILE '(' expr ')' stmt {
        $$ = createWhile($3, $5);
    }
    ;

/* FOR LOOP - for (init; condition; update) body
 * All three header parts are optional (may be empty).
 * Syntax: for ( for_init ; for_cond ; for_update ) stmt
 */
for_stmt:
    FOR '(' for_init ';' for_cond ';' for_update ')' stmt {
        $$ = createFor($3, $5, $7, $9);
    }
    ;

/* FOR INIT - optional initialization (assignment without semicolon) */
for_init:
    /* empty - no initialization */  {
        $$ = NULL;
    }
    | ID '=' expr {
        /* Simple scalar assignment: e.g., i = 0 */
        $$ = createAssign($1, $3);
        free($1);
    }
    | ID '[' expr ']' '=' expr {
        /* Array element assignment: e.g., arr[0] = 0 */
        ASTNode* lhs = createArrayIndex($1, $3);
        $$ = createAssign(NULL, $6);
        $$->data.assign.arrayLHS = lhs;
        free($1);
    }
    ;

/* FOR CONDITION - optional loop condition expression */
for_cond:
    /* empty - no condition means loop forever (always true) */ {
        $$ = NULL;
    }
    | expr {
        /* Condition expression: e.g., i < 10 */
        $$ = $1;
    }
    ;

/* FOR UPDATE - optional per-iteration update (assignment without semicolon) */
for_update:
    /* empty - no update step */ {
        $$ = NULL;
    }
    | ID '=' expr {
        /* Simple scalar update: e.g., i = i + 1 */
        $$ = createAssign($1, $3);
        free($1);
    }
    | ID '[' expr ']' '=' expr {
        /* Array element update: e.g., arr[i] = arr[i] + 1 */
        ASTNode* lhs = createArrayIndex($1, $3);
        $$ = createAssign(NULL, $6);
        $$->data.assign.arrayLHS = lhs;
        free($1);
    }
    ;

/*#end*/

/* EXPRESSION RULES */
expr:
    NUM {
        $$ = createNum($1);
    }
    | ID {
        $$ = createVar($1);
        free($1);
    }
/*#3*/
/*#todo Two new kinds of primary expression: an array element  arr[i]  and a*/
/*#todo function call used for its value.*/
    | ID '[' expr ']' {
        $$ = createArrayIndex($1, $3);
        free($1);
    }
    | func_call {
        $$ = $1;
    }
/*#end*/
    | expr '+' expr {
        $$ = createBinOp('+', $1, $3);
    }
/*#3*/
/*#todo The rest of arithmetic.  Do NOT write precedence into these rules — the*/
/*#todo %left declarations above already did that.  Rewriting the grammar into*/
/*#todo term/factor layers to get precedence is the classic wrong turn here;*/
/*#todo it works, but it is the answer to a question bison already answered.*/
    | expr '-' expr {
        $$ = createBinOp('-', $1, $3);
    }
    | expr '*' expr {
        $$ = createBinOp('*', $1, $3);
    }
    | expr '/' expr {
        $$ = createBinOp('/', $1, $3);
    }
/*#end*/
/*#4*/
/*#todo The six relational operators, each producing a BINOP node.*/
/*#todo createBinOp packs the operator into ONE char, so the two-character*/
/*#todo operators get single-letter codes:  <= is 'l',  >= is 'g',*/
/*#todo == is 'e',  != is 'n'.  (See opText() in ast.c for the full table.)*/
/*#todo A comparison yields 1 or 0 — there is no separate boolean type.*/
    | expr '<' expr {
        $$ = createBinOp('<', $1, $3);
    }
    | expr '>' expr {
        $$ = createBinOp('>', $1, $3);
    }
    | expr LE expr {
        $$ = createBinOp('l', $1, $3);  /* 'l' for <= */
    }
    | expr GE expr {
        $$ = createBinOp('g', $1, $3);  /* 'g' for >= */
    }
    | expr EQ expr {
        $$ = createBinOp('e', $1, $3);  /* 'e' for == */
    }
    | expr NE expr {
        $$ = createBinOp('n', $1, $3);  /* 'n' for != */
    }
/*#end*/
/*#3*/
/*#todo Unary minus.  %prec UMINUS is what stops  -2 * 3  parsing as  -(2 * 3):*/
/*#todo without it the rule inherits the precedence of BINARY '-', which is*/
/*#todo lower than '*'.*/
    | '-' expr %prec UMINUS {
        $$ = createBinOp('u', $2, NULL);  /* 'u' for unary minus */
    }
/*#end*/
/*#5*/
/*#todo The three logical operators.  Codes: '&' for &&, '|' for ||, '!' for !.*/
/*#todo ! is unary, so pass NULL as the right operand — exactly like unary minus.*/
    | expr AND expr {
        $$ = createBinOp('&', $1, $3);    /* '&' for logical AND (&&) */
    }
    | expr OR expr {
        $$ = createBinOp('|', $1, $3);    /* '|' for logical OR (||)  */
    }
    | '!' expr %prec NOT {
        $$ = createBinOp('!', $2, NULL);  /* '!' for logical NOT      */
    }
/*#end*/
/*#3*/
/*#todo Parentheses.  Note there is no node for them: ( e ) just yields e.*/
/*#todo Parentheses exist to steer the PARSER; once the tree is built the*/
/*#todo grouping they asked for is recorded in its shape and they vanish.*/
    | '(' expr ')' {
        $$ = $2;
    }
/*#end*/
    ;

/*#3*/
/*#todo FUNCTION CALLS and their arguments.*/
/*#todo   func_call : ID '(' args ')' | ID '(' ')'*/
/*#todo   args      : (empty) | arg_list*/
/*#todo   arg_list  : expr | arg_list ',' expr*/
/*#todo Build the list with createArgList so tac.c can walk it in source*/
/*#todo order — argument order is part of the calling convention.*/
/* FUNCTION CALL */
func_call:
    ID '(' args ')' {
        $$ = createFuncCall($1, $3);
        free($1);
    }
    | ID '(' ')' {
        $$ = createFuncCall($1, NULL);
        free($1);
    }
    ;

/* ARGUMENTS */
args:
    arg_list { $$ = $1; }
    ;

arg_list:
    expr {
        $$ = $1;  /* Single argument becomes the arg node */
    }
    | arg_list ',' expr {
        $$ = createArgList($1, $3);
    }
    ;

/*#end*/

/* PRINT STATEMENT */
print_stmt:
    PRINT '(' expr ')' ';' {
        $$ = createPrint($3);
    }
    ;

%%

/* ERROR HANDLING */
void yyerror(const char* s) {
    fprintf(stderr, "Syntax Error at line %d: %s\n", yylineno, s);
}
