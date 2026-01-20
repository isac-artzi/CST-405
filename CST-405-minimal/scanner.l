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

%%

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

.               { printf("Lexical Error: Unknown character '%c'\n", *yytext); }

%%

/* Required by Flex - signals end of input */
int yywrap() {
    return 1;  /* 1 means no more input files */
}