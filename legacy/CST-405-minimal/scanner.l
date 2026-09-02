%{
/* LEXICAL ANALYZER (SCANNER)
 * This is the first phase of compilation - breaking input into tokens
 * Flex generates a scanner from these rules that reads character by character
 */
#include <stdio.h>
#include <stdlib.h>
#include "parser.tab.h"  /* Token definitions from Bison */

/* Global flag to enable token display */
extern int displayTokens;
%}

/* Flex options to suppress warnings for unused functions */
%option nounput
%option noinput
%option yylineno

/* Exclusive start condition for multi-line comments */
%x COMMENT

%%

"//".*          {
    /* Single-line comment - ignore everything from // to end of line */
    if (displayTokens) printf("  (ignoring single-line comment)\n");
}

"/*"            {
    /* Start of multi-line comment - switch to COMMENT state */
    if (displayTokens) printf("  (start multi-line comment)\n");
    BEGIN(COMMENT);
}

<COMMENT>"*/"   {
    /* End of multi-line comment - return to normal scanning */
    if (displayTokens) printf("  (end multi-line comment)\n");
    BEGIN(INITIAL);
}

<COMMENT>\n     {
    /* Newline inside comment - ignore but continue in COMMENT state */
}

<COMMENT>.      {
    /* Any other character inside comment - ignore */
}

"int"           {
    if (displayTokens) printf("  TOKEN: INT keyword\n");
    return INT;
}

"print"         {
    if (displayTokens) printf("  TOKEN: PRINT keyword\n");
    return PRINT;
}

[a-zA-Z_][a-zA-Z0-9_]* {
    if (displayTokens) printf("  TOKEN: ID '%s'\n", yytext);
    yylval.str = strdup(yytext);
    return ID;
}

[0-9]+          {
    if (displayTokens) printf("  TOKEN: NUM %s\n", yytext);
    yylval.num = atoi(yytext);
    return NUM;
}

"+"             {
    if (displayTokens) printf("  TOKEN: '+'\n");
    return '+';
}

"="             {
    if (displayTokens) printf("  TOKEN: '='\n");
    return '=';
}

";"             {
    if (displayTokens) printf("  TOKEN: ';'\n");
    return ';';
}

"("             {
    if (displayTokens) printf("  TOKEN: '('\n");
    return '(';
}

")"             {
    if (displayTokens) printf("  TOKEN: ')'\n");
    return ')';
}

[ \t\n]         { }

.               {
    fprintf(stderr, "\n❌ Lexical Error at line %d:\n", yylineno);
    fprintf(stderr, "   Unknown character: '%c' (ASCII %d)\n", *yytext, *yytext);
    fprintf(stderr, "   💡 Suggestion: Remove this character or check for typos\n\n");
}

<<EOF>>         {
    if (YY_START == COMMENT) {
        fprintf(stderr, "\n❌ Lexical Error at line %d:\n", yylineno);
        fprintf(stderr, "   Unterminated multi-line comment\n");
        fprintf(stderr, "   💡 Suggestion: Add '*/' to close the comment\n\n");
        return 0;
    }
    yyterminate();
}

%%

/* Required by Flex - signals end of input */
int yywrap() {
    return 1;  /* 1 means no more input files */
}