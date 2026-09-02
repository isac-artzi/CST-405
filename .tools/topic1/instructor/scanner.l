%{
/* ============================================================================
 * CST-405  ·  TOPIC 1  ·  Compiler Design Phases
 * FILE: scanner.l   —   Phase 1: Lexical analysis
 * ----------------------------------------------------------------------------
 * Flex reads the rules below and writes a finite automaton that recognises
 * all of them at once.  You never write the automaton; you write the
 * vocabulary, and two rules decide everything about how it behaves:
 *
 *   LONGEST MATCH   "<=" beats "<" because it consumes more characters.
 *                   Position in the file is irrelevant for this.
 *   FIRST MATCH     when two rules match the SAME number of characters, the
 *                   one written EARLIER wins.  This is the only reason the
 *                   keyword rules must appear above the identifier rule:
 *                   "int" matches both, both match three characters, and
 *                   whichever is written first decides the outcome.
 *
 * Delete a keyword rule and watch that keyword come back as an ID.  That one
 * experiment explains rule order better than any paragraph can.
 *
 * WHAT COMES NEXT
 *   In Topic 2 this same file feeds bison instead of main.c.  The actions
 *   change from "record a token for printing" to "return a token number";
 *   the patterns do not change at all.
 * ==========================================================================*/
#include <stdio.h>
#include <string.h>
#include "tokens.h"

int lexErrorCount = 0;
int tokenCount    = 0;
int lineNo        = 1;
int colNo         = 1;

char lastLexeme[256];
int  lastLine;
int  lastCol;

/* Record where the token that is being returned started, then advance the
 * column past it.  Flex tracks lines for us (%option yylineno) but not
 * columns, so we keep the column by hand — and a column number is half of
 * what makes an error message actually findable. */
static int tok(TokenKind k) {
    lastLine = lineNo;
    lastCol  = colNo;
    snprintf(lastLexeme, sizeof lastLexeme, "%s", yytext);
    colNo += (int)yyleng;
    tokenCount++;
    return (int)k;
}

/* Advance the position counters over text that produces no token at all:
 * whitespace, newlines, and the insides of comments. */
static void skip(const char* s, int n) {
    for (int i = 0; i < n; i++) {
        if (s[i] == '\n') { lineNo++; colNo = 1; }
        else if (s[i] == '\t') colNo += 4;
        else colNo++;
    }
}
%}

%option noyywrap
%option nounput
%option noinput

/* Named patterns keep the rules below readable.  A definition is pure
 * substitution — {digit}+ literally becomes [0-9]+ before flex sees it. */
digit   [0-9]
letter  [a-zA-Z_]
ident   {letter}({letter}|{digit})*
number  {digit}+

%%

 /* ── Comments and whitespace produce no tokens ─────────────────────────
  * They still have to be COUNTED, or every line number after the first
  * multi-line comment is wrong.  Note the pattern for a block comment:
  * "/*"([^*]|\*+[^*\/])*\*+"/"  —  it is fiddly precisely because it must
  * not stop at the first '*' it meets. */
"//".*                          { skip(yytext, (int)yyleng); }
"/*"([^*]|\*+[^*/])*\*+"/"      { skip(yytext, (int)yyleng); }
"/*"([^*]|\*+[^*/])*            {
                                  /* Reached end of file inside a comment */
                                  fprintf(stderr,
                                    "  LEXICAL ERROR  line %d, col %d: "
                                    "unterminated block comment\n"
                                    "                 the /* opened here is never closed by */\n",
                                    lineNo, colNo);
                                  lexErrorCount++;
                                  skip(yytext, (int)yyleng);
                                }
[ \t\r\n]+                      { skip(yytext, (int)yyleng); }

 /* ── Keywords.  These MUST precede the identifier rule. ─────────────── */
"int"       { return tok(TOK_INT);     }
"print"     { return tok(TOK_PRINT);   }
"return"    { return tok(TOK_RETURN);  }
"if"        { return tok(TOK_IF);      }
"else"      { return tok(TOK_ELSE);    }
"while"     { return tok(TOK_WHILE);   }
"for"       { return tok(TOK_FOR);     }
"switch"    { return tok(TOK_SWITCH);  }
"case"      { return tok(TOK_CASE);    }
"default"   { return tok(TOK_DEFAULT); }
"break"     { return tok(TOK_BREAK);   }

 /* ── Identifiers and numbers ────────────────────────────────────────── */
{ident}     { return tok(TOK_ID);  }
{number}    { return tok(TOK_NUM); }

 /* ── Two-character operators BEFORE their one-character prefixes ─────
  * Longest match already handles this, so the order here is for the human
  * reader, not for flex.  Prove it to yourself: move "<" above "<=" and
  * confirm that "<=" still comes back as one token. */
"<="        { return tok(TOK_LE);  }
">="        { return tok(TOK_GE);  }
"=="        { return tok(TOK_EQ);  }
"!="        { return tok(TOK_NE);  }
"&&"        { return tok(TOK_AND); }
"||"        { return tok(TOK_OR);  }

 /* ── One-character operators ────────────────────────────────────────── */
"+"         { return tok(TOK_PLUS);   }
"-"         { return tok(TOK_MINUS);  }
"*"         { return tok(TOK_STAR);   }
"/"         { return tok(TOK_SLASH);  }
"<"         { return tok(TOK_LT);     }
">"         { return tok(TOK_GT);     }
"!"         { return tok(TOK_NOT);    }
"="         { return tok(TOK_ASSIGN); }

 /* ── Delimiters ─────────────────────────────────────────────────────── */
";"         { return tok(TOK_SEMI);      }
":"         { return tok(TOK_COLON);     }
","         { return tok(TOK_COMMA);     }
"("         { return tok(TOK_LPAREN);    }
")"         { return tok(TOK_RPAREN);    }
"{"         { return tok(TOK_LBRACE);    }
"}"         { return tok(TOK_RBRACE);    }
"["         { return tok(TOK_LBRACKET);  }
"]"         { return tok(TOK_RBRACKET);  }

 /* ── Anything else is a lexical error ────────────────────────────────
  * Report it, count it, and KEEP GOING.  A scanner that stops at the first
  * bad character makes the programmer fix one typo per compile.  Recovering
  * and reporting all of them in one run is worth the few lines it costs. */
.           {
              fprintf(stderr,
                "  LEXICAL ERROR  line %d, col %d: "
                "character '%s' is not part of this language\n",
                lineNo, colNo, yytext);
              if (yytext[0] == '\'' || yytext[0] == '"')
                  fprintf(stderr,
                "                 (this language has no character or string literals)\n");
              else if (yytext[0] == '@' || yytext[0] == '$' || yytext[0] == '#')
                  fprintf(stderr,
                "                 (identifiers may contain only letters, digits and _)\n");
              lexErrorCount++;
              colNo++;
            }

%%
