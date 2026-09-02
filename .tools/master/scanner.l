%{
/* PHASE 1 — LEXICAL ANALYSIS
 *
 * The scanner turns a stream of CHARACTERS into a stream of TOKENS.
 * It is the only part of the compiler that ever sees whitespace or comments.
 *
 *      int  sum  =  a + 10 ;
 *      └─┬┘ └─┬┘ │  │ │ └┬┘ │
 *       INT  ID  '=' ID '+' NUM ';'
 *
 * Flex turns the rules below into a finite automaton.  Two rules decide
 * everything you need to know about how it behaves:
 *
 *   LONGEST MATCH   "<=" wins over "<" because it matches more characters.
 *                   This is why "<=" must exist as a rule at all, and why
 *                   its position in the file does not matter.
 *   FIRST MATCH     when two rules match the SAME length, the one written
 *                   first wins.  This is why the keyword rules sit above
 *                   the identifier rule: without that order, "int" would
 *                   come back as an ID.
 */
#include <stdio.h>
#include <stdlib.h>
#include "parser.tab.h"  /* Token definitions from Bison */
%}

/* Flex options to suppress warnings for unused functions */
%option nounput
%option noinput
%option yylineno

%%

"int"           { return INT; }
"print"         { return PRINT; }
    /*#3*/
    /*#todo Return RETURN for the `return` keyword.*/
"return"        { return RETURN; }
    /*#end*/
    /*#5*/
    /*#todo Return the IF and ELSE tokens for the `if` and `else` keywords.*/
    /*#todo One line each, exactly like the `int` and `print` rules above.*/
"if"            { return IF; }
"else"          { return ELSE; }
    /*#end*/
    /*#4*/
    /*#todo Return WHILE and FOR for the loop keywords.*/
"while"         { return WHILE; }
"for"           { return FOR; }
    /*#end*/
    /*#5*/
    /*#todo Return SWITCH, CASE and DEFAULT for the switch keywords.*/
"switch"        { return SWITCH; }
"case"          { return CASE; }
"default"       { return DEFAULT; }
    /*#end*/
    /*#4*/
    /*#todo Return BREAK for the `break` keyword.*/
"break"         { return BREAK; }
    /*#end*/

[a-zA-Z_][a-zA-Z0-9_]* {
    yylval.str = strdup(yytext);
    return ID;
}

[0-9]+          {
    yylval.num = atoi(yytext);
    return NUM;
}

    /*#5*/
    /*#todo Return AND and OR for the logical operators && and ||.*/
    /*#todo Think about longest match: does `&&` need its own rule to beat anything?*/
"&&"            { return AND; }
"||"            { return OR; }
    /*#end*/

    /*#4*/
    /*#todo Return LE, GE, EQ and NE for the two-character relational operators.*/
    /*#todo These MUST exist as their own rules: without a `<=` rule, flex would*/
    /*#todo match `<` and then `=` and your parser would see two tokens, not one.*/
"<="            { return LE; }
">="            { return GE; }
"=="            { return EQ; }
"!="            { return NE; }
    /*#end*/

"+"             { return '+'; }
    /*#3*/
    /*#todo The rest of arithmetic: return '-', '*' and '/'.*/
    /*#todo Careful: the '/' rule must not swallow the start of a comment.*/
    /*#todo Longest match settles it — check that it really does.*/
"-"             { return '-'; }
"*"             { return '*'; }
"/"             { return '/'; }
    /*#end*/

    /*#4*/
    /*#todo Return the single-character relational operators.*/
"<"             { return '<'; }
">"             { return '>'; }
    /*#end*/
    /*#5*/
    /*#todo Return the logical-not operator.*/
"!"             { return '!'; }
    /*#end*/

"="             { return '='; }

";"             { return ';'; }
    /*#5*/
    /*#todo Return ':' — needed to write `case 3:` and `default:`.*/
":"             { return ':'; }
    /*#end*/
"("             { return '('; }
")"             { return ')'; }
    /*#3*/
    /*#todo Braces for blocks, brackets for arrays, comma for parameter lists.*/
"{"             { return '{'; }
"}"             { return '}'; }
"["             { return '['; }
"]"             { return ']'; }
","             { return ','; }
    /*#end*/

"//".*          { /* Skip single-line comments */ }
"/*"([^*]|\*+[^*/])*\*+"/"  { /* Skip multi-line comments */ }

[ \t\n]         { }

.               { printf("Lexical Error: Unknown character '%c'\n", *yytext); }

%%

int yywrap() {
    return 1;
}
