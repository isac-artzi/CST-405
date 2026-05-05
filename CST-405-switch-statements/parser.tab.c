/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton implementation for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "2.3"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Using locations.  */
#define YYLSP_NEEDED 0



/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     NUM = 258,
     ID = 259,
     INT = 260,
     PRINT = 261,
     RETURN = 262,
     IF = 263,
     ELSE = 264,
     WHILE = 265,
     FOR = 266,
     SWITCH = 267,
     CASE = 268,
     DEFAULT = 269,
     BREAK = 270,
     LE = 271,
     GE = 272,
     EQ = 273,
     NE = 274,
     LOWER_THAN_ELSE = 275,
     UMINUS = 276
   };
#endif
/* Tokens.  */
#define NUM 258
#define ID 259
#define INT 260
#define PRINT 261
#define RETURN 262
#define IF 263
#define ELSE 264
#define WHILE 265
#define FOR 266
#define SWITCH 267
#define CASE 268
#define DEFAULT 269
#define BREAK 270
#define LE 271
#define GE 272
#define EQ 273
#define NE 274
#define LOWER_THAN_ELSE 275
#define UMINUS 276




/* Copy the first part of user declarations.  */
#line 1 "parser.y"

/* SYNTAX ANALYZER (PARSER) - WITH FUNCTION SUPPORT
 * This is the second phase of compilation - checking grammar rules
 * Bison generates a parser that builds an Abstract Syntax Tree (AST)
 * Now supports functions, control flow, and more operators
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


/* Enabling traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 0
#endif

/* Enabling the token table.  */
#ifndef YYTOKEN_TABLE
# define YYTOKEN_TABLE 0
#endif

#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
#line 23 "parser.y"
{
    int num;
    char* str;
    struct ASTNode* node;
}
/* Line 193 of yacc.c.  */
#line 165 "parser.tab.c"
	YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif



/* Copy the second part of user declarations.  */


/* Line 216 of yacc.c.  */
#line 178 "parser.tab.c"

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#elif (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
typedef signed char yytype_int8;
#else
typedef short int yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(e) ((void) (e))
#else
# define YYUSE(e) /* empty */
#endif

/* Identity function, used to suppress warnings about constant conditions.  */
#ifndef lint
# define YYID(n) (n)
#else
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static int
YYID (int i)
#else
static int
YYID (i)
    int i;
#endif
{
  return i;
}
#endif

#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#     ifndef _STDLIB_H
#      define _STDLIB_H 1
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's `empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (YYID (0))
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined _STDLIB_H \
       && ! ((defined YYMALLOC || defined malloc) \
	     && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef _STDLIB_H
#    define _STDLIB_H 1
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
	 || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss;
  YYSTYPE yyvs;
  };

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

/* Copy COUNT objects from FROM to TO.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(To, From, Count) \
      __builtin_memcpy (To, From, (Count) * sizeof (*(From)))
#  else
#   define YYCOPY(To, From, Count)		\
      do					\
	{					\
	  YYSIZE_T yyi;				\
	  for (yyi = 0; yyi < (Count); yyi++)	\
	    (To)[yyi] = (From)[yyi];		\
	}					\
      while (YYID (0))
#  endif
# endif

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack)					\
    do									\
      {									\
	YYSIZE_T yynewbytes;						\
	YYCOPY (&yyptr->Stack, Stack, yysize);				\
	Stack = &yyptr->Stack;						\
	yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
	yyptr += yynewbytes / sizeof (*yyptr);				\
      }									\
    while (YYID (0))

#endif

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  8
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   315

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  38
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  30
/* YYNRULES -- Number of rules.  */
#define YYNRULES  76
/* YYNRULES -- Number of states.  */
#define YYNSTATES  163

/* YYTRANSLATE(YYLEX) -- Bison symbol number corresponding to YYLEX.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   276

#define YYTRANSLATE(YYX)						\
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[YYLEX] -- Bison symbol number corresponding to YYLEX.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      28,    29,    25,    23,    30,    24,     2,    26,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    36,    35,
      21,    37,    22,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    31,     2,    32,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,    33,     2,    34,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    27
};

#if YYDEBUG
/* YYPRHS[YYN] -- Index of the first RHS symbol of rule number YYN in
   YYRHS.  */
static const yytype_uint16 yyprhs[] =
{
       0,     0,     3,     5,     7,    10,    12,    14,    21,    27,
      29,    31,    35,    38,    43,    47,    50,    52,    55,    57,
      59,    61,    63,    65,    67,    69,    71,    73,    75,    78,
      86,    87,    90,    95,    99,   100,   102,   105,   109,   116,
     121,   129,   133,   136,   142,   150,   156,   166,   167,   171,
     178,   179,   181,   182,   186,   193,   195,   197,   202,   204,
     208,   212,   216,   220,   224,   228,   232,   236,   240,   244,
     247,   251,   256,   260,   262,   264,   268
};

/* YYRHS -- A `-1'-separated list of the rules' RHS.  */
static const yytype_int8 yyrhs[] =
{
      39,     0,    -1,    40,    -1,    41,    -1,    40,    41,    -1,
      42,    -1,    54,    -1,     5,     4,    28,    43,    29,    46,
      -1,     5,     4,    28,    29,    46,    -1,    44,    -1,    45,
      -1,    44,    30,    45,    -1,     5,     4,    -1,     5,     4,
      31,    32,    -1,    33,    47,    34,    -1,    33,    34,    -1,
      48,    -1,    47,    48,    -1,    54,    -1,    55,    -1,    67,
      -1,    56,    -1,    57,    -1,    58,    -1,    59,    -1,    49,
      -1,    53,    -1,    46,    -1,    64,    35,    -1,    12,    28,
      63,    29,    33,    50,    34,    -1,    -1,    50,    51,    -1,
      13,     3,    36,    52,    -1,    14,    36,    52,    -1,    -1,
      47,    -1,    15,    35,    -1,     5,     4,    35,    -1,     5,
       4,    31,     3,    32,    35,    -1,     4,    37,    63,    35,
      -1,     4,    31,    63,    32,    37,    63,    35,    -1,     7,
      63,    35,    -1,     7,    35,    -1,     8,    28,    63,    29,
      48,    -1,     8,    28,    63,    29,    48,     9,    48,    -1,
      10,    28,    63,    29,    48,    -1,    11,    28,    60,    35,
      61,    35,    62,    29,    48,    -1,    -1,     4,    37,    63,
      -1,     4,    31,    63,    32,    37,    63,    -1,    -1,    63,
      -1,    -1,     4,    37,    63,    -1,     4,    31,    63,    32,
      37,    63,    -1,     3,    -1,     4,    -1,     4,    31,    63,
      32,    -1,    64,    -1,    63,    23,    63,    -1,    63,    24,
      63,    -1,    63,    25,    63,    -1,    63,    26,    63,    -1,
      63,    21,    63,    -1,    63,    22,    63,    -1,    63,    16,
      63,    -1,    63,    17,    63,    -1,    63,    18,    63,    -1,
      63,    19,    63,    -1,    24,    63,    -1,    28,    63,    29,
      -1,     4,    28,    65,    29,    -1,     4,    28,    29,    -1,
      66,    -1,    63,    -1,    66,    30,    63,    -1,     6,    28,
      63,    29,    35,    -1
};

/* YYRLINE[YYN] -- source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,    69,    69,    76,    79,    86,    87,    92,    96,   104,
     108,   111,   117,   121,   129,   132,   139,   142,   149,   150,
     151,   152,   153,   154,   155,   156,   157,   158,   159,   164,
     171,   174,   190,   193,   200,   203,   210,   217,   221,   229,
     233,   243,   246,   263,   267,   275,   285,   292,   295,   300,
     311,   314,   322,   325,   330,   341,   344,   348,   352,   355,
     358,   361,   364,   367,   370,   373,   376,   379,   382,   385,
     388,   395,   399,   407,   411,   414,   421
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || YYTOKEN_TABLE
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "NUM", "ID", "INT", "PRINT", "RETURN",
  "IF", "ELSE", "WHILE", "FOR", "SWITCH", "CASE", "DEFAULT", "BREAK", "LE",
  "GE", "EQ", "NE", "LOWER_THAN_ELSE", "'<'", "'>'", "'+'", "'-'", "'*'",
  "'/'", "UMINUS", "'('", "')'", "','", "'['", "']'", "'{'", "'}'", "';'",
  "':'", "'='", "$accept", "program", "decl_or_func_list", "decl_or_func",
  "func_def", "params", "param_list", "param", "block", "stmt_list",
  "stmt", "switch_stmt", "case_list", "case_clause", "opt_stmt_list",
  "break_stmt", "decl", "assign", "return_stmt", "if_stmt", "while_stmt",
  "for_stmt", "for_init", "for_cond", "for_update", "expr", "func_call",
  "args", "arg_list", "print_stmt", 0
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[YYLEX-NUM] -- Internal token number corresponding to
   token YYLEX-NUM.  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,    60,    62,    43,    45,    42,    47,   276,    40,    41,
      44,    91,    93,   123,   125,    59,    58,    61
};
# endif

/* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,    38,    39,    40,    40,    41,    41,    42,    42,    43,
      44,    44,    45,    45,    46,    46,    47,    47,    48,    48,
      48,    48,    48,    48,    48,    48,    48,    48,    48,    49,
      50,    50,    51,    51,    52,    52,    53,    54,    54,    55,
      55,    56,    56,    57,    57,    58,    59,    60,    60,    60,
      61,    61,    62,    62,    62,    63,    63,    63,    63,    63,
      63,    63,    63,    63,    63,    63,    63,    63,    63,    63,
      63,    64,    64,    65,    66,    66,    67
};

/* YYR2[YYN] -- Number of symbols composing right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     1,     1,     2,     1,     1,     6,     5,     1,
       1,     3,     2,     4,     3,     2,     1,     2,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     2,     7,
       0,     2,     4,     3,     0,     1,     2,     3,     6,     4,
       7,     3,     2,     5,     7,     5,     9,     0,     3,     6,
       0,     1,     0,     3,     6,     1,     1,     4,     1,     3,
       3,     3,     3,     3,     3,     3,     3,     3,     3,     2,
       3,     4,     3,     1,     1,     3,     5
};

/* YYDEFACT[STATE-NAME] -- Default rule to reduce with in state
   STATE-NUM when YYTABLE doesn't specify something else to do.  Zero
   means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       0,     0,     0,     2,     3,     5,     6,     0,     1,     4,
       0,     0,    37,     0,     0,     0,     9,    10,     0,    12,
       0,     8,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,    15,    27,     0,    16,    25,
      26,    18,    19,    21,    22,    23,    24,     0,    20,     7,
      11,    38,    13,     0,     0,     0,     0,     0,    55,    56,
       0,     0,    42,     0,    58,     0,     0,    47,     0,    36,
      14,    17,    28,    72,    74,     0,    73,     0,     0,     0,
       0,    69,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,    41,     0,     0,     0,     0,     0,    71,
       0,     0,    39,     0,     0,    70,    65,    66,    67,    68,
      63,    64,    59,    60,    61,    62,     0,     0,     0,     0,
      50,     0,    75,     0,    76,    57,    43,    45,     0,    48,
       0,    51,    30,     0,     0,     0,    52,     0,    40,    44,
       0,     0,     0,     0,     0,    29,    31,    49,     0,     0,
       0,     0,    34,     0,    53,    46,    34,    35,    33,     0,
      32,     0,    54
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,     2,     3,     4,     5,    15,    16,    17,    36,   157,
      38,    39,   137,   146,   158,    40,    41,    42,    43,    44,
      45,    46,    97,   130,   142,    63,    64,    75,    76,    48
};

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
#define YYPACT_NINF -46
static const yytype_int16 yypact[] =
{
      -4,    10,    34,    -4,   -46,   -46,   -46,    31,   -46,   -46,
       8,    30,   -46,    61,    38,    43,    63,   -46,    66,    71,
      46,   -46,    38,   106,    91,    95,    -9,   125,   105,     1,
     107,   127,   128,   140,   118,   -46,   -46,    79,   -46,   -46,
     -46,   -46,   -46,   -46,   -46,   -46,   -46,   119,   -46,   -46,
     -46,   -46,   -46,     3,    64,    64,    -5,    64,   -46,    32,
      64,    64,   -46,   126,   -46,    64,    64,   165,    64,   -46,
     -46,   -46,   -46,   -46,   289,   142,   153,   171,   141,   219,
      64,   -46,   233,    64,    64,    64,    64,    64,    64,    64,
      64,    64,    64,   -46,   247,   261,   -13,   135,   275,   -46,
      64,   147,   -46,   150,   183,   -46,   115,   115,    84,    84,
     115,   115,    51,    51,   -46,   -46,   113,   113,    64,    64,
      64,   177,   289,    64,   -46,   -46,   189,   -46,   195,   289,
     151,   289,   -46,   156,   113,   185,   230,    35,   -46,   -46,
      64,    33,   217,   244,   224,   -46,   -46,   289,    64,    64,
     113,   225,   113,   207,   289,   -46,   113,   113,   -46,   216,
     -46,    64,   289
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
     -46,   -46,   -46,   264,   -46,   -46,   -46,   251,   -11,   255,
     -35,   -46,   -46,   -46,   132,   -46,   131,   -46,   -46,   -46,
     -46,   -46,   -46,   -46,   -46,   -45,   -20,   -46,   -46,   -46
};

/* YYTABLE[YYPACT[STATE-NUM]].  What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule which
   number is the opposite.  If zero, do what YYDEFACT says.
   If YYTABLE_NINF, syntax error.  */
#define YYTABLE_NINF -1
static const yytype_uint8 yytable[] =
{
      47,     1,    71,    21,    58,    59,    58,    59,    74,    77,
      78,    49,    79,    13,     7,    81,    82,    47,   118,    53,
      94,    95,    54,    98,   119,    60,    11,    60,    55,    61,
      12,    61,    73,    18,     8,   104,    62,    14,   106,   107,
     108,   109,   110,   111,   112,   113,   114,   115,   143,   144,
      26,    27,    28,    29,    30,   122,    31,    32,    33,    10,
      53,    34,    11,    80,   148,    19,    12,    58,    59,   145,
     149,    20,    22,   128,   129,   131,    91,    92,   133,    20,
      35,   126,   127,    26,    27,    28,    29,    30,    60,    31,
      32,    33,    61,    23,    34,   147,    47,    47,    24,   139,
      83,    84,    25,   153,   154,    87,    88,    89,    90,    91,
      92,    13,    20,    70,    47,   155,   162,    26,    27,    28,
      29,    30,    71,    31,    32,    33,    51,    52,    34,    56,
      47,     6,    47,    57,     6,    65,    47,    47,    89,    90,
      91,    92,    83,    84,    85,    86,    20,    87,    88,    89,
      90,    91,    92,    69,    72,    66,    67,    83,    84,    85,
      86,    93,    87,    88,    89,    90,    91,    92,    68,    96,
     120,    99,    83,    84,    85,    86,   102,    87,    88,    89,
      90,    91,    92,   100,   123,   124,   136,    83,    84,    85,
      86,   138,    87,    88,    89,    90,    91,    92,   134,    83,
      84,    85,    86,   101,    87,    88,    89,    90,    91,    92,
     132,    83,    84,    85,    86,   125,    87,    88,    89,    90,
      91,    92,   140,    83,    84,    85,    86,   135,    87,    88,
      89,    90,    91,    92,   141,    83,    84,    85,    86,   159,
      87,    88,    89,    90,    91,    92,   150,   151,   103,    83,
      84,    85,    86,   161,    87,    88,    89,    90,    91,    92,
     152,   156,   105,    83,    84,    85,    86,     9,    87,    88,
      89,    90,    91,    92,    50,    37,   116,    83,    84,    85,
      86,     0,    87,    88,    89,    90,    91,    92,   160,     0,
     117,    83,    84,    85,    86,     0,    87,    88,    89,    90,
      91,    92,     0,     0,   121,    83,    84,    85,    86,     0,
      87,    88,    89,    90,    91,    92
};

static const yytype_int16 yycheck[] =
{
      20,     5,    37,    14,     3,     4,     3,     4,    53,    54,
      55,    22,    57,     5,     4,    60,    61,    37,    31,    28,
      65,    66,    31,    68,    37,    24,    31,    24,    37,    28,
      35,    28,    29,     3,     0,    80,    35,    29,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,    13,    14,
       4,     5,     6,     7,     8,   100,    10,    11,    12,    28,
      28,    15,    31,    31,    31,     4,    35,     3,     4,    34,
      37,    33,    29,   118,   119,   120,    25,    26,   123,    33,
      34,   116,   117,     4,     5,     6,     7,     8,    24,    10,
      11,    12,    28,    30,    15,   140,   116,   117,    32,   134,
      16,    17,    31,   148,   149,    21,    22,    23,    24,    25,
      26,     5,    33,    34,   134,   150,   161,     4,     5,     6,
       7,     8,   157,    10,    11,    12,    35,    32,    15,     4,
     150,     0,   152,    28,     3,    28,   156,   157,    23,    24,
      25,    26,    16,    17,    18,    19,    33,    21,    22,    23,
      24,    25,    26,    35,    35,    28,    28,    16,    17,    18,
      19,    35,    21,    22,    23,    24,    25,    26,    28,     4,
      35,    29,    16,    17,    18,    19,    35,    21,    22,    23,
      24,    25,    26,    30,    37,    35,    35,    16,    17,    18,
      19,    35,    21,    22,    23,    24,    25,    26,     9,    16,
      17,    18,    19,    32,    21,    22,    23,    24,    25,    26,
      33,    16,    17,    18,    19,    32,    21,    22,    23,    24,
      25,    26,    37,    16,    17,    18,    19,    32,    21,    22,
      23,    24,    25,    26,     4,    16,    17,    18,    19,    32,
      21,    22,    23,    24,    25,    26,    29,     3,    29,    16,
      17,    18,    19,    37,    21,    22,    23,    24,    25,    26,
      36,    36,    29,    16,    17,    18,    19,     3,    21,    22,
      23,    24,    25,    26,    23,    20,    29,    16,    17,    18,
      19,    -1,    21,    22,    23,    24,    25,    26,   156,    -1,
      29,    16,    17,    18,    19,    -1,    21,    22,    23,    24,
      25,    26,    -1,    -1,    29,    16,    17,    18,    19,    -1,
      21,    22,    23,    24,    25,    26
};

/* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
   symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,     5,    39,    40,    41,    42,    54,     4,     0,    41,
      28,    31,    35,     5,    29,    43,    44,    45,     3,     4,
      33,    46,    29,    30,    32,    31,     4,     5,     6,     7,
       8,    10,    11,    12,    15,    34,    46,    47,    48,    49,
      53,    54,    55,    56,    57,    58,    59,    64,    67,    46,
      45,    35,    32,    28,    31,    37,     4,    28,     3,     4,
      24,    28,    35,    63,    64,    28,    28,    28,    28,    35,
      34,    48,    35,    29,    63,    65,    66,    63,    63,    63,
      31,    63,    63,    16,    17,    18,    19,    21,    22,    23,
      24,    25,    26,    35,    63,    63,     4,    60,    63,    29,
      30,    32,    35,    29,    63,    29,    63,    63,    63,    63,
      63,    63,    63,    63,    63,    63,    29,    29,    31,    37,
      35,    29,    63,    37,    35,    32,    48,    48,    63,    63,
      61,    63,    33,    63,     9,    32,    35,    50,    35,    48,
      37,     4,    62,    13,    14,    34,    51,    63,    31,    37,
      29,     3,    36,    63,    63,    48,    36,    47,    52,    32,
      52,    37,    63
};

#define yyerrok		(yyerrstatus = 0)
#define yyclearin	(yychar = YYEMPTY)
#define YYEMPTY		(-2)
#define YYEOF		0

#define YYACCEPT	goto yyacceptlab
#define YYABORT		goto yyabortlab
#define YYERROR		goto yyerrorlab


/* Like YYERROR except do call yyerror.  This remains here temporarily
   to ease the transition to the new meaning of YYERROR, for GCC.
   Once GCC version 2 has supplanted version 1, this can go.  */

#define YYFAIL		goto yyerrlab

#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)					\
do								\
  if (yychar == YYEMPTY && yylen == 1)				\
    {								\
      yychar = (Token);						\
      yylval = (Value);						\
      yytoken = YYTRANSLATE (yychar);				\
      YYPOPSTACK (1);						\
      goto yybackup;						\
    }								\
  else								\
    {								\
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;							\
    }								\
while (YYID (0))


#define YYTERROR	1
#define YYERRCODE	256


/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

#define YYRHSLOC(Rhs, K) ((Rhs)[K])
#ifndef YYLLOC_DEFAULT
# define YYLLOC_DEFAULT(Current, Rhs, N)				\
    do									\
      if (YYID (N))                                                    \
	{								\
	  (Current).first_line   = YYRHSLOC (Rhs, 1).first_line;	\
	  (Current).first_column = YYRHSLOC (Rhs, 1).first_column;	\
	  (Current).last_line    = YYRHSLOC (Rhs, N).last_line;		\
	  (Current).last_column  = YYRHSLOC (Rhs, N).last_column;	\
	}								\
      else								\
	{								\
	  (Current).first_line   = (Current).last_line   =		\
	    YYRHSLOC (Rhs, 0).last_line;				\
	  (Current).first_column = (Current).last_column =		\
	    YYRHSLOC (Rhs, 0).last_column;				\
	}								\
    while (YYID (0))
#endif


/* YY_LOCATION_PRINT -- Print the location on the stream.
   This macro was not mandated originally: define only if we know
   we won't break user code: when these are the locations we know.  */

#ifndef YY_LOCATION_PRINT
# if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL
#  define YY_LOCATION_PRINT(File, Loc)			\
     fprintf (File, "%d.%d-%d.%d",			\
	      (Loc).first_line, (Loc).first_column,	\
	      (Loc).last_line,  (Loc).last_column)
# else
#  define YY_LOCATION_PRINT(File, Loc) ((void) 0)
# endif
#endif


/* YYLEX -- calling `yylex' with the right arguments.  */

#ifdef YYLEX_PARAM
# define YYLEX yylex (YYLEX_PARAM)
#else
# define YYLEX yylex ()
#endif

/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)			\
do {						\
  if (yydebug)					\
    YYFPRINTF Args;				\
} while (YYID (0))

# define YY_SYMBOL_PRINT(Title, Type, Value, Location)			  \
do {									  \
  if (yydebug)								  \
    {									  \
      YYFPRINTF (stderr, "%s ", Title);					  \
      yy_symbol_print (stderr,						  \
		  Type, Value); \
      YYFPRINTF (stderr, "\n");						  \
    }									  \
} while (YYID (0))


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_value_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# else
  YYUSE (yyoutput);
# endif
  switch (yytype)
    {
      default:
	break;
    }
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (yytype < YYNTOKENS)
    YYFPRINTF (yyoutput, "token %s (", yytname[yytype]);
  else
    YYFPRINTF (yyoutput, "nterm %s (", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_stack_print (yytype_int16 *bottom, yytype_int16 *top)
#else
static void
yy_stack_print (bottom, top)
    yytype_int16 *bottom;
    yytype_int16 *top;
#endif
{
  YYFPRINTF (stderr, "Stack now");
  for (; bottom <= top; ++bottom)
    YYFPRINTF (stderr, " %d", *bottom);
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)				\
do {								\
  if (yydebug)							\
    yy_stack_print ((Bottom), (Top));				\
} while (YYID (0))


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_reduce_print (YYSTYPE *yyvsp, int yyrule)
#else
static void
yy_reduce_print (yyvsp, yyrule)
    YYSTYPE *yyvsp;
    int yyrule;
#endif
{
  int yynrhs = yyr2[yyrule];
  int yyi;
  unsigned long int yylno = yyrline[yyrule];
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
	     yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      fprintf (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr, yyrhs[yyprhs[yyrule] + yyi],
		       &(yyvsp[(yyi + 1) - (yynrhs)])
		       		       );
      fprintf (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)		\
do {					\
  if (yydebug)				\
    yy_reduce_print (yyvsp, Rule); \
} while (YYID (0))

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef	YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif



#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static YYSIZE_T
yystrlen (const char *yystr)
#else
static YYSIZE_T
yystrlen (yystr)
    const char *yystr;
#endif
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static char *
yystpcpy (char *yydest, const char *yysrc)
#else
static char *
yystpcpy (yydest, yysrc)
    char *yydest;
    const char *yysrc;
#endif
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
	switch (*++yyp)
	  {
	  case '\'':
	  case ',':
	    goto do_not_strip_quotes;

	  case '\\':
	    if (*++yyp != '\\')
	      goto do_not_strip_quotes;
	    /* Fall through.  */
	  default:
	    if (yyres)
	      yyres[yyn] = *yyp;
	    yyn++;
	    break;

	  case '"':
	    if (yyres)
	      yyres[yyn] = '\0';
	    return yyn;
	  }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into YYRESULT an error message about the unexpected token
   YYCHAR while in state YYSTATE.  Return the number of bytes copied,
   including the terminating null byte.  If YYRESULT is null, do not
   copy anything; just return the number of bytes that would be
   copied.  As a special case, return 0 if an ordinary "syntax error"
   message will do.  Return YYSIZE_MAXIMUM if overflow occurs during
   size calculation.  */
static YYSIZE_T
yysyntax_error (char *yyresult, int yystate, int yychar)
{
  int yyn = yypact[yystate];

  if (! (YYPACT_NINF < yyn && yyn <= YYLAST))
    return 0;
  else
    {
      int yytype = YYTRANSLATE (yychar);
      YYSIZE_T yysize0 = yytnamerr (0, yytname[yytype]);
      YYSIZE_T yysize = yysize0;
      YYSIZE_T yysize1;
      int yysize_overflow = 0;
      enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
      char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
      int yyx;

# if 0
      /* This is so xgettext sees the translatable formats that are
	 constructed on the fly.  */
      YY_("syntax error, unexpected %s");
      YY_("syntax error, unexpected %s, expecting %s");
      YY_("syntax error, unexpected %s, expecting %s or %s");
      YY_("syntax error, unexpected %s, expecting %s or %s or %s");
      YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s");
# endif
      char *yyfmt;
      char const *yyf;
      static char const yyunexpected[] = "syntax error, unexpected %s";
      static char const yyexpecting[] = ", expecting %s";
      static char const yyor[] = " or %s";
      char yyformat[sizeof yyunexpected
		    + sizeof yyexpecting - 1
		    + ((YYERROR_VERBOSE_ARGS_MAXIMUM - 2)
		       * (sizeof yyor - 1))];
      char const *yyprefix = yyexpecting;

      /* Start YYX at -YYN if negative to avoid negative indexes in
	 YYCHECK.  */
      int yyxbegin = yyn < 0 ? -yyn : 0;

      /* Stay within bounds of both yycheck and yytname.  */
      int yychecklim = YYLAST - yyn + 1;
      int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
      int yycount = 1;

      yyarg[0] = yytname[yytype];
      yyfmt = yystpcpy (yyformat, yyunexpected);

      for (yyx = yyxbegin; yyx < yyxend; ++yyx)
	if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR)
	  {
	    if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
	      {
		yycount = 1;
		yysize = yysize0;
		yyformat[sizeof yyunexpected - 1] = '\0';
		break;
	      }
	    yyarg[yycount++] = yytname[yyx];
	    yysize1 = yysize + yytnamerr (0, yytname[yyx]);
	    yysize_overflow |= (yysize1 < yysize);
	    yysize = yysize1;
	    yyfmt = yystpcpy (yyfmt, yyprefix);
	    yyprefix = yyor;
	  }

      yyf = YY_(yyformat);
      yysize1 = yysize + yystrlen (yyf);
      yysize_overflow |= (yysize1 < yysize);
      yysize = yysize1;

      if (yysize_overflow)
	return YYSIZE_MAXIMUM;

      if (yyresult)
	{
	  /* Avoid sprintf, as that infringes on the user's name space.
	     Don't have undefined behavior even if the translation
	     produced a string with the wrong number of "%s"s.  */
	  char *yyp = yyresult;
	  int yyi = 0;
	  while ((*yyp = *yyf) != '\0')
	    {
	      if (*yyp == '%' && yyf[1] == 's' && yyi < yycount)
		{
		  yyp += yytnamerr (yyp, yyarg[yyi++]);
		  yyf += 2;
		}
	      else
		{
		  yyp++;
		  yyf++;
		}
	    }
	}
      return yysize;
    }
}
#endif /* YYERROR_VERBOSE */


/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
#else
static void
yydestruct (yymsg, yytype, yyvaluep)
    const char *yymsg;
    int yytype;
    YYSTYPE *yyvaluep;
#endif
{
  YYUSE (yyvaluep);

  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  switch (yytype)
    {

      default:
	break;
    }
}


/* Prevent warnings from -Wmissing-prototypes.  */

#ifdef YYPARSE_PARAM
#if defined __STDC__ || defined __cplusplus
int yyparse (void *YYPARSE_PARAM);
#else
int yyparse ();
#endif
#else /* ! YYPARSE_PARAM */
#if defined __STDC__ || defined __cplusplus
int yyparse (void);
#else
int yyparse ();
#endif
#endif /* ! YYPARSE_PARAM */



/* The look-ahead symbol.  */
int yychar;

/* The semantic value of the look-ahead symbol.  */
YYSTYPE yylval;

/* Number of syntax errors so far.  */
int yynerrs;



/*----------.
| yyparse.  |
`----------*/

#ifdef YYPARSE_PARAM
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void *YYPARSE_PARAM)
#else
int
yyparse (YYPARSE_PARAM)
    void *YYPARSE_PARAM;
#endif
#else /* ! YYPARSE_PARAM */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void)
#else
int
yyparse ()

#endif
#endif
{
  
  int yystate;
  int yyn;
  int yyresult;
  /* Number of tokens to shift before error messages enabled.  */
  int yyerrstatus;
  /* Look-ahead token as an internal (translated) token number.  */
  int yytoken = 0;
#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

  /* Three stacks and their tools:
     `yyss': related to states,
     `yyvs': related to semantic values,
     `yyls': related to locations.

     Refer to the stacks thru separate pointers, to allow yyoverflow
     to reallocate them elsewhere.  */

  /* The state stack.  */
  yytype_int16 yyssa[YYINITDEPTH];
  yytype_int16 *yyss = yyssa;
  yytype_int16 *yyssp;

  /* The semantic value stack.  */
  YYSTYPE yyvsa[YYINITDEPTH];
  YYSTYPE *yyvs = yyvsa;
  YYSTYPE *yyvsp;



#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  YYSIZE_T yystacksize = YYINITDEPTH;

  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;


  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY;		/* Cause a token to be read.  */

  /* Initialize stack pointers.
     Waste one element of value and location stack
     so that they stay on the same level as the state stack.
     The wasted elements are never initialized.  */

  yyssp = yyss;
  yyvsp = yyvs;

  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
	/* Give user a chance to reallocate the stack.  Use copies of
	   these so that the &'s don't force the real ones into
	   memory.  */
	YYSTYPE *yyvs1 = yyvs;
	yytype_int16 *yyss1 = yyss;


	/* Each stack pointer address is followed by the size of the
	   data in use in that stack, in bytes.  This used to be a
	   conditional around just the two extra args, but that might
	   be undefined if yyoverflow is a macro.  */
	yyoverflow (YY_("memory exhausted"),
		    &yyss1, yysize * sizeof (*yyssp),
		    &yyvs1, yysize * sizeof (*yyvsp),

		    &yystacksize);

	yyss = yyss1;
	yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
	goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
	yystacksize = YYMAXDEPTH;

      {
	yytype_int16 *yyss1 = yyss;
	union yyalloc *yyptr =
	  (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
	if (! yyptr)
	  goto yyexhaustedlab;
	YYSTACK_RELOCATE (yyss);
	YYSTACK_RELOCATE (yyvs);

#  undef YYSTACK_RELOCATE
	if (yyss1 != yyssa)
	  YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;


      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
		  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
	YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     look-ahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to look-ahead token.  */
  yyn = yypact[yystate];
  if (yyn == YYPACT_NINF)
    goto yydefault;

  /* Not known => get a look-ahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid look-ahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = YYLEX;
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yyn == 0 || yyn == YYTABLE_NINF)
	goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  if (yyn == YYFINAL)
    YYACCEPT;

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the look-ahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token unless it is eof.  */
  if (yychar != YYEOF)
    yychar = YYEMPTY;

  yystate = yyn;
  *++yyvsp = yylval;

  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     `$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 2:
#line 69 "parser.y"
    {
        root = (yyvsp[(1) - (1)].node);
    ;}
    break;

  case 3:
#line 76 "parser.y"
    {
        (yyval.node) = (yyvsp[(1) - (1)].node);
    ;}
    break;

  case 4:
#line 79 "parser.y"
    {
        (yyval.node) = createStmtList((yyvsp[(1) - (2)].node), (yyvsp[(2) - (2)].node));
    ;}
    break;

  case 5:
#line 86 "parser.y"
    { (yyval.node) = (yyvsp[(1) - (1)].node); ;}
    break;

  case 6:
#line 87 "parser.y"
    { (yyval.node) = (yyvsp[(1) - (1)].node); ;}
    break;

  case 7:
#line 92 "parser.y"
    {
        (yyval.node) = createFuncDef((yyvsp[(2) - (6)].str), (yyvsp[(4) - (6)].node), (yyvsp[(6) - (6)].node));
        free((yyvsp[(2) - (6)].str));
    ;}
    break;

  case 8:
#line 96 "parser.y"
    {
        (yyval.node) = createFuncDef((yyvsp[(2) - (5)].str), NULL, (yyvsp[(5) - (5)].node));
        free((yyvsp[(2) - (5)].str));
    ;}
    break;

  case 9:
#line 104 "parser.y"
    { (yyval.node) = (yyvsp[(1) - (1)].node); ;}
    break;

  case 10:
#line 108 "parser.y"
    {
        (yyval.node) = (yyvsp[(1) - (1)].node);
    ;}
    break;

  case 11:
#line 111 "parser.y"
    {
        (yyval.node) = createParamList((yyvsp[(1) - (3)].node), (yyvsp[(3) - (3)].node));
    ;}
    break;

  case 12:
#line 117 "parser.y"
    {
        (yyval.node) = createParam((yyvsp[(2) - (2)].str));
        free((yyvsp[(2) - (2)].str));
    ;}
    break;

  case 13:
#line 121 "parser.y"
    {
        (yyval.node) = createArrayParam((yyvsp[(2) - (4)].str));
        free((yyvsp[(2) - (4)].str));
    ;}
    break;

  case 14:
#line 129 "parser.y"
    {
        (yyval.node) = createBlock((yyvsp[(2) - (3)].node));
    ;}
    break;

  case 15:
#line 132 "parser.y"
    {
        (yyval.node) = createBlock(NULL);
    ;}
    break;

  case 16:
#line 139 "parser.y"
    {
        (yyval.node) = (yyvsp[(1) - (1)].node);
    ;}
    break;

  case 17:
#line 142 "parser.y"
    {
        (yyval.node) = createStmtList((yyvsp[(1) - (2)].node), (yyvsp[(2) - (2)].node));
    ;}
    break;

  case 28:
#line 159 "parser.y"
    { (yyval.node) = (yyvsp[(1) - (2)].node); ;}
    break;

  case 29:
#line 164 "parser.y"
    {
        (yyval.node) = createSwitch((yyvsp[(3) - (7)].node), (yyvsp[(6) - (7)].node));
    ;}
    break;

  case 30:
#line 171 "parser.y"
    {
        (yyval.node) = NULL;
    ;}
    break;

  case 31:
#line 174 "parser.y"
    {
        /* Append case_clause to end of the linked list */
        if ((yyvsp[(1) - (2)].node) == NULL) {
            (yyval.node) = (yyvsp[(2) - (2)].node);
        } else {
            ASTNode* tail = (yyvsp[(1) - (2)].node);
            while (tail->data.case_clause.next)
                tail = tail->data.case_clause.next;
            tail->data.case_clause.next = (yyvsp[(2) - (2)].node);
            (yyval.node) = (yyvsp[(1) - (2)].node);
        }
    ;}
    break;

  case 32:
#line 190 "parser.y"
    {
        (yyval.node) = createCase((yyvsp[(2) - (4)].num), 0, (yyvsp[(4) - (4)].node));
    ;}
    break;

  case 33:
#line 193 "parser.y"
    {
        (yyval.node) = createCase(0, 1, (yyvsp[(3) - (3)].node));
    ;}
    break;

  case 34:
#line 200 "parser.y"
    {
        (yyval.node) = NULL;
    ;}
    break;

  case 35:
#line 203 "parser.y"
    {
        (yyval.node) = (yyvsp[(1) - (1)].node);
    ;}
    break;

  case 36:
#line 210 "parser.y"
    {
        (yyval.node) = createBreak();
    ;}
    break;

  case 37:
#line 217 "parser.y"
    {
        (yyval.node) = createDecl((yyvsp[(2) - (3)].str));
        free((yyvsp[(2) - (3)].str));
    ;}
    break;

  case 38:
#line 221 "parser.y"
    {
        (yyval.node) = createArrayDecl((yyvsp[(2) - (6)].str), (yyvsp[(4) - (6)].num));
        free((yyvsp[(2) - (6)].str));
    ;}
    break;

  case 39:
#line 229 "parser.y"
    {
        (yyval.node) = createAssign((yyvsp[(1) - (4)].str), (yyvsp[(3) - (4)].node));
        free((yyvsp[(1) - (4)].str));
    ;}
    break;

  case 40:
#line 233 "parser.y"
    {
        ASTNode* lhs = createArrayIndex((yyvsp[(1) - (7)].str), (yyvsp[(3) - (7)].node));
        (yyval.node) = createAssign(NULL, (yyvsp[(6) - (7)].node));
        (yyval.node)->data.assign.arrayLHS = lhs;
        free((yyvsp[(1) - (7)].str));
    ;}
    break;

  case 41:
#line 243 "parser.y"
    {
        (yyval.node) = createReturn((yyvsp[(2) - (3)].node));
    ;}
    break;

  case 42:
#line 246 "parser.y"
    {
        (yyval.node) = createReturn(NULL);
    ;}
    break;

  case 43:
#line 263 "parser.y"
    {
        /* if-without-else: else_stmt is NULL */
        (yyval.node) = createIf((yyvsp[(3) - (5)].node), (yyvsp[(5) - (5)].node), NULL);
    ;}
    break;

  case 44:
#line 267 "parser.y"
    {
        /* if-with-else: captures the else branch */
        (yyval.node) = createIf((yyvsp[(3) - (7)].node), (yyvsp[(5) - (7)].node), (yyvsp[(7) - (7)].node));
    ;}
    break;

  case 45:
#line 275 "parser.y"
    {
        (yyval.node) = createWhile((yyvsp[(3) - (5)].node), (yyvsp[(5) - (5)].node));
    ;}
    break;

  case 46:
#line 285 "parser.y"
    {
        (yyval.node) = createFor((yyvsp[(3) - (9)].node), (yyvsp[(5) - (9)].node), (yyvsp[(7) - (9)].node), (yyvsp[(9) - (9)].node));
    ;}
    break;

  case 47:
#line 292 "parser.y"
    {
        (yyval.node) = NULL;
    ;}
    break;

  case 48:
#line 295 "parser.y"
    {
        /* Simple scalar assignment: e.g., i = 0 */
        (yyval.node) = createAssign((yyvsp[(1) - (3)].str), (yyvsp[(3) - (3)].node));
        free((yyvsp[(1) - (3)].str));
    ;}
    break;

  case 49:
#line 300 "parser.y"
    {
        /* Array element assignment: e.g., arr[0] = 0 */
        ASTNode* lhs = createArrayIndex((yyvsp[(1) - (6)].str), (yyvsp[(3) - (6)].node));
        (yyval.node) = createAssign(NULL, (yyvsp[(6) - (6)].node));
        (yyval.node)->data.assign.arrayLHS = lhs;
        free((yyvsp[(1) - (6)].str));
    ;}
    break;

  case 50:
#line 311 "parser.y"
    {
        (yyval.node) = NULL;
    ;}
    break;

  case 51:
#line 314 "parser.y"
    {
        /* Condition expression: e.g., i < 10 */
        (yyval.node) = (yyvsp[(1) - (1)].node);
    ;}
    break;

  case 52:
#line 322 "parser.y"
    {
        (yyval.node) = NULL;
    ;}
    break;

  case 53:
#line 325 "parser.y"
    {
        /* Simple scalar update: e.g., i = i + 1 */
        (yyval.node) = createAssign((yyvsp[(1) - (3)].str), (yyvsp[(3) - (3)].node));
        free((yyvsp[(1) - (3)].str));
    ;}
    break;

  case 54:
#line 330 "parser.y"
    {
        /* Array element update: e.g., arr[i] = arr[i] + 1 */
        ASTNode* lhs = createArrayIndex((yyvsp[(1) - (6)].str), (yyvsp[(3) - (6)].node));
        (yyval.node) = createAssign(NULL, (yyvsp[(6) - (6)].node));
        (yyval.node)->data.assign.arrayLHS = lhs;
        free((yyvsp[(1) - (6)].str));
    ;}
    break;

  case 55:
#line 341 "parser.y"
    {
        (yyval.node) = createNum((yyvsp[(1) - (1)].num));
    ;}
    break;

  case 56:
#line 344 "parser.y"
    {
        (yyval.node) = createVar((yyvsp[(1) - (1)].str));
        free((yyvsp[(1) - (1)].str));
    ;}
    break;

  case 57:
#line 348 "parser.y"
    {
        (yyval.node) = createArrayIndex((yyvsp[(1) - (4)].str), (yyvsp[(3) - (4)].node));
        free((yyvsp[(1) - (4)].str));
    ;}
    break;

  case 58:
#line 352 "parser.y"
    {
        (yyval.node) = (yyvsp[(1) - (1)].node);
    ;}
    break;

  case 59:
#line 355 "parser.y"
    {
        (yyval.node) = createBinOp('+', (yyvsp[(1) - (3)].node), (yyvsp[(3) - (3)].node));
    ;}
    break;

  case 60:
#line 358 "parser.y"
    {
        (yyval.node) = createBinOp('-', (yyvsp[(1) - (3)].node), (yyvsp[(3) - (3)].node));
    ;}
    break;

  case 61:
#line 361 "parser.y"
    {
        (yyval.node) = createBinOp('*', (yyvsp[(1) - (3)].node), (yyvsp[(3) - (3)].node));
    ;}
    break;

  case 62:
#line 364 "parser.y"
    {
        (yyval.node) = createBinOp('/', (yyvsp[(1) - (3)].node), (yyvsp[(3) - (3)].node));
    ;}
    break;

  case 63:
#line 367 "parser.y"
    {
        (yyval.node) = createBinOp('<', (yyvsp[(1) - (3)].node), (yyvsp[(3) - (3)].node));
    ;}
    break;

  case 64:
#line 370 "parser.y"
    {
        (yyval.node) = createBinOp('>', (yyvsp[(1) - (3)].node), (yyvsp[(3) - (3)].node));
    ;}
    break;

  case 65:
#line 373 "parser.y"
    {
        (yyval.node) = createBinOp('l', (yyvsp[(1) - (3)].node), (yyvsp[(3) - (3)].node));  /* 'l' for <= */
    ;}
    break;

  case 66:
#line 376 "parser.y"
    {
        (yyval.node) = createBinOp('g', (yyvsp[(1) - (3)].node), (yyvsp[(3) - (3)].node));  /* 'g' for >= */
    ;}
    break;

  case 67:
#line 379 "parser.y"
    {
        (yyval.node) = createBinOp('e', (yyvsp[(1) - (3)].node), (yyvsp[(3) - (3)].node));  /* 'e' for == */
    ;}
    break;

  case 68:
#line 382 "parser.y"
    {
        (yyval.node) = createBinOp('n', (yyvsp[(1) - (3)].node), (yyvsp[(3) - (3)].node));  /* 'n' for != */
    ;}
    break;

  case 69:
#line 385 "parser.y"
    {
        (yyval.node) = createBinOp('u', (yyvsp[(2) - (2)].node), NULL);  /* 'u' for unary minus */
    ;}
    break;

  case 70:
#line 388 "parser.y"
    {
        (yyval.node) = (yyvsp[(2) - (3)].node);
    ;}
    break;

  case 71:
#line 395 "parser.y"
    {
        (yyval.node) = createFuncCall((yyvsp[(1) - (4)].str), (yyvsp[(3) - (4)].node));
        free((yyvsp[(1) - (4)].str));
    ;}
    break;

  case 72:
#line 399 "parser.y"
    {
        (yyval.node) = createFuncCall((yyvsp[(1) - (3)].str), NULL);
        free((yyvsp[(1) - (3)].str));
    ;}
    break;

  case 73:
#line 407 "parser.y"
    { (yyval.node) = (yyvsp[(1) - (1)].node); ;}
    break;

  case 74:
#line 411 "parser.y"
    {
        (yyval.node) = (yyvsp[(1) - (1)].node);  /* Single argument becomes the arg node */
    ;}
    break;

  case 75:
#line 414 "parser.y"
    {
        (yyval.node) = createArgList((yyvsp[(1) - (3)].node), (yyvsp[(3) - (3)].node));
    ;}
    break;

  case 76:
#line 421 "parser.y"
    {
        (yyval.node) = createPrint((yyvsp[(3) - (5)].node));
    ;}
    break;


/* Line 1267 of yacc.c.  */
#line 2022 "parser.tab.c"
      default: break;
    }
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;


  /* Now `shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*------------------------------------.
| yyerrlab -- here on detecting error |
`------------------------------------*/
yyerrlab:
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
      {
	YYSIZE_T yysize = yysyntax_error (0, yystate, yychar);
	if (yymsg_alloc < yysize && yymsg_alloc < YYSTACK_ALLOC_MAXIMUM)
	  {
	    YYSIZE_T yyalloc = 2 * yysize;
	    if (! (yysize <= yyalloc && yyalloc <= YYSTACK_ALLOC_MAXIMUM))
	      yyalloc = YYSTACK_ALLOC_MAXIMUM;
	    if (yymsg != yymsgbuf)
	      YYSTACK_FREE (yymsg);
	    yymsg = (char *) YYSTACK_ALLOC (yyalloc);
	    if (yymsg)
	      yymsg_alloc = yyalloc;
	    else
	      {
		yymsg = yymsgbuf;
		yymsg_alloc = sizeof yymsgbuf;
	      }
	  }

	if (0 < yysize && yysize <= yymsg_alloc)
	  {
	    (void) yysyntax_error (yymsg, yystate, yychar);
	    yyerror (yymsg);
	  }
	else
	  {
	    yyerror (YY_("syntax error"));
	    if (yysize != 0)
	      goto yyexhaustedlab;
	  }
      }
#endif
    }



  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse look-ahead token after an
	 error, discard it.  */

      if (yychar <= YYEOF)
	{
	  /* Return failure if at end of input.  */
	  if (yychar == YYEOF)
	    YYABORT;
	}
      else
	{
	  yydestruct ("Error: discarding",
		      yytoken, &yylval);
	  yychar = YYEMPTY;
	}
    }

  /* Else will try to reuse look-ahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  /* Do not reclaim the symbols of the rule which action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;	/* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (yyn != YYPACT_NINF)
	{
	  yyn += YYTERROR;
	  if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
	    {
	      yyn = yytable[yyn];
	      if (0 < yyn)
		break;
	    }
	}

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
	YYABORT;


      yydestruct ("Error: popping",
		  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  if (yyn == YYFINAL)
    YYACCEPT;

  *++yyvsp = yylval;


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#ifndef yyoverflow
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEOF && yychar != YYEMPTY)
     yydestruct ("Cleanup: discarding lookahead",
		 yytoken, &yylval);
  /* Do not reclaim the symbols of the rule which action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
		  yystos[*yyssp], yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  /* Make sure YYID is used.  */
  return YYID (yyresult);
}


#line 426 "parser.y"


/* ERROR HANDLING */
void yyerror(const char* s) {
    fprintf(stderr, "Syntax Error at line %d: %s\n", yylineno, s);
}

