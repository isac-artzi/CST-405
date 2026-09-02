#ifndef AST_H
#define AST_H

/* ABSTRACT SYNTAX TREE (AST)
 * The AST is an intermediate representation of the program structure
 * It represents the hierarchical syntax of the source code
 * Each node represents a construct in the language
 */

/* NODE TYPES - Different kinds of AST nodes in our language */
typedef enum {
    NODE_NUM,         /* Numeric literal (e.g., 42) */
    NODE_VAR,         /* Variable reference (e.g., x) */
    NODE_BINOP,       /* Binary operation (e.g., x + y) */
    NODE_DECL,        /* Variable declaration (e.g., int x) */
    NODE_ASSIGN,      /* Assignment statement (e.g., x = 10) */
    NODE_PRINT,       /* Print statement (e.g., print(x)) */
    NODE_STMT_LIST,   /* List of statements (program structure) */
/*#3*/
/*#todo The node kinds functions need: FUNC_DEF, PARAM, PARAM_LIST, FUNC_CALL,*/
/*#todo ARG_LIST, RETURN.*/
    NODE_FUNC_DEF,    /* Function definition */
    NODE_PARAM,       /* Parameter (name only, type is always int) */
    NODE_PARAM_LIST,  /* Parameter list */
    NODE_FUNC_CALL,   /* Function call */
    NODE_ARG_LIST,    /* Argument list */
    NODE_RETURN,      /* Return statement */
/*#end*/
/*#4*/
/*#todo Add the loop node kinds to this enum:*/
/*#todo   NODE_WHILE, NODE_FOR, NODE_BREAK*/
    NODE_WHILE,       /* While loop */
    NODE_FOR,         /* For loop: for (init; condition; update) body */
    NODE_BREAK,       /* Break statement */

/*#end*/
/*#3*/
/*#todo And the node kinds blocks and arrays need: BLOCK, ARRAY_DECL, ARRAY_INDEX.*/
    NODE_BLOCK,       /* Block statement { ... } */
    NODE_ARRAY_DECL,  /* Array declaration (e.g., int arr[10] or int arr[]) */
    NODE_ARRAY_INDEX, /* Array indexing (e.g., arr[i]) */
/*#end*/
/*#5*/
/*#todo Add the decision node kinds:*/
/*#todo   NODE_IF, NODE_SWITCH, NODE_CASE*/
    NODE_IF,          /* If statement */
    NODE_SWITCH,      /* Switch statement */
    NODE_CASE         /* Case or default clause */
/*#end*/
} NodeType;

/* AST NODE STRUCTURE
 * Uses a union to efficiently store different node data
 * Only the relevant fields for each node type are used
 */
typedef struct ASTNode {
    NodeType type;  /* Identifies what kind of node this is */
    int lineno;     /* Line number in source code for error reporting */

    /* Union allows same memory to store different data types */
    union {
        /* Literal number value (NODE_NUM) */
        int num;
        
        /* Variable reference name (NODE_VAR) */
        char* name;

        /* Declaration structure (NODE_DECL) */
        struct {
            char* name;
            char* varType;
        } decl;


        /* Binary operation structure (NODE_BINOP) */
        struct {
            char op;                    /* Operator character ('+') */
            struct ASTNode* left;       /* Left operand */
            struct ASTNode* right;      /* Right operand */
        } binop;
        
        /* Assignment structure (NODE_ASSIGN) */
        struct {
            char* var;                  /* Variable being assigned to (NULL for array) */
            struct ASTNode* value;      /* Expression being assigned */
            struct ASTNode* arrayLHS;   /* Array index node (NULL for scalar) */  /*#3*/
        } assign;
        
        /* Print expression (NODE_PRINT) */
        struct ASTNode* expr;
        
        /* Statement list structure (NODE_STMT_LIST) */
        struct {
            struct ASTNode* stmt;       /* Current statement */
            struct ASTNode* next;       /* Rest of the list */
        } stmtlist;

/*#3*/
/*#todo Union members for the function-related node kinds.  Each records*/
/*#todo exactly what later phases will ask for and nothing more:*/
/*#todo   func_def  : name, params, body*/
/*#todo   param     : name          param_list : param, next*/
/*#todo   func_call : name, args    arg_list   : expr, next*/
/*#todo   ret       : expr (NULL for a bare `return;`)*/
        /* Function definition (NODE_FUNC_DEF) */
        struct {
            char* name;                 /* Function name */
            struct ASTNode* params;     /* Parameter list */
            struct ASTNode* body;       /* Function body (block or stmt_list) */
        } func_def;

        /* Parameter (NODE_PARAM) - just a name */
        struct {
            char* name;
        } param;

        /* Parameter list (NODE_PARAM_LIST) */
        struct {
            struct ASTNode* param;      /* Current parameter */
            struct ASTNode* next;       /* Rest of parameters */
        } param_list;

        /* Function call (NODE_FUNC_CALL) */
        struct {
            char* name;                 /* Function name */
            struct ASTNode* args;       /* Argument list */
        } func_call;

        /* Argument list (NODE_ARG_LIST) */
        struct {
            struct ASTNode* expr;       /* Current argument expression */
            struct ASTNode* next;       /* Rest of arguments */
        } arg_list;

        /* Return statement (NODE_RETURN) */
        struct {
            struct ASTNode* expr;       /* Expression to return (NULL for void) */
        } ret;

/*#end*/
/*#5*/
/*#todo A NODE_IF needs three children: condition, then-branch, else-branch.*/
/*#todo else_stmt is NULL when the source had no `else`.*/
        /* If statement (NODE_IF) */
        struct {
            struct ASTNode* condition;  /* Condition expression */
            struct ASTNode* then_stmt;  /* Then branch */
            struct ASTNode* else_stmt;  /* Else branch (NULL if no else) */
        } if_stmt;

/*#end*/
/*#4*/
/*#todo A NODE_WHILE needs a condition and a body.*/
        /* While loop (NODE_WHILE) */
        struct {
            struct ASTNode* condition;  /* Loop condition */
            struct ASTNode* body;       /* Loop body */
        } while_stmt;

/*#end*/
/*#4*/
/*#todo A NODE_FOR needs FOUR children: init, condition, update, body.*/
/*#todo Any of them may be NULL, because every part of a for-header is*/
/*#todo optional.  Decide now what "condition is NULL" should mean.*/
        /* For loop (NODE_FOR)
         * Represents: for (init; condition; update) body
         * Any part may be NULL:
         *   - init NULL   → no initialization
         *   - condition NULL → always true (infinite until break)
         *   - update NULL → no increment step
         */
        struct {
            struct ASTNode* init;       /* Initialization statement (assignment or NULL) */
            struct ASTNode* condition;  /* Loop condition expression (NULL = always true) */
            struct ASTNode* update;     /* Update statement executed after each iteration */
            struct ASTNode* body;       /* Loop body */
        } for_stmt;

/*#end*/
/*#3*/
/*#todo Union members for blocks and arrays:*/
/*#todo   block       : stmt_list*/
/*#todo   array_decl  : name, size, isParam*/
/*#todo   array_index : name, index*/
/*#todo isParam separates `int a[10];` (reserve 40 bytes of storage) from*/
/*#todo `int a[]` as a parameter (reserve 4 bytes for an address).*/
        /* Block statement (NODE_BLOCK) */
        struct {
            struct ASTNode* stmt_list;  /* Statements in block */
        } block;

        /* Array declaration (NODE_ARRAY_DECL) */
        struct {
            char* name;                 /* Array name */
            int size;                   /* Array size (0 for parameters) */
            int isParam;                /* 1 if this is a parameter, 0 otherwise */
        } array_decl;

        /* Array indexing (NODE_ARRAY_INDEX) */
        struct {
            char* name;                 /* Array name */
            struct ASTNode* index;      /* Index expression */
        } array_index;

/*#end*/
/*#5*/
/*#todo A NODE_SWITCH holds the controlling expression and a LINKED LIST of*/
/*#todo case clauses, in source order.*/
        /* Switch statement (NODE_SWITCH) */
        struct {
            struct ASTNode* expr;       /* Controlling expression (evaluated once) */
            struct ASTNode* cases;      /* Linked list of NODE_CASE nodes */
        } switch_stmt;

/*#end*/
/*#5*/
/*#todo A NODE_CASE is one clause of a switch.  It needs: the case constant,*/
/*#todo a flag saying whether it is the `default` clause, the body statement*/
/*#todo list (which may be NULL), and a `next` pointer to the following*/
/*#todo clause.  The `next` pointer is what preserves source order, and*/
/*#todo source order is what makes fall-through work.*/
        /* Case / default clause (NODE_CASE)
         * Linked list: each node's 'next' points to the following clause.
         * isDefault==1  → this is the default: clause (value is unused)
         * isDefault==0  → this is a case N: clause
         */
        struct {
            int value;                  /* Case constant value */
            int isDefault;             /* 1 if this is the default clause */
            struct ASTNode* body;       /* Statement list (may be NULL) */
            struct ASTNode* next;       /* Next case/default clause */
        } case_clause;
/*#end*/
    } data;
} ASTNode;

/* AST CONSTRUCTION FUNCTIONS
 * These functions are called by the parser to build the tree
 */
/* Basic nodes */
ASTNode* createNum(int value);                                   /* Create number node */
ASTNode* createVar(char* name);                                  /* Create variable node */
ASTNode* createBinOp(char op, ASTNode* left, ASTNode* right);   /* Create binary op node */
ASTNode* createDecl(char* type, char* name);                     /* Create declaration node */
ASTNode* createAssign(char* var, ASTNode* value);               /* Create assignment node */
ASTNode* createPrint(ASTNode* expr);                            /* Create print node */
ASTNode* createStmtList(ASTNode* stmt1, ASTNode* stmt2);        /* Create statement list */

/* Function-related nodes */
/*#3*/
/*#todo Declare the constructors for the function-related nodes.*/
ASTNode* createFuncDef(char* name, ASTNode* params, ASTNode* body);  /* Create function definition */
ASTNode* createParam(char* name);                               /* Create parameter */
ASTNode* createParamList(ASTNode* param, ASTNode* next);        /* Create parameter list */
ASTNode* createFuncCall(char* name, ASTNode* args);             /* Create function call */
ASTNode* createArgList(ASTNode* expr, ASTNode* next);           /* Create argument list */
ASTNode* createReturn(ASTNode* expr);                           /* Create return statement */
/*#end*/

/* Control flow nodes */
/*#3*/
/*#todo Declare createBlock.*/
ASTNode* createBlock(ASTNode* stmt_list);                       /* Create block statement */
/*#end*/
/*#4*/
/*#todo Declare the constructors for the loop nodes:*/
/*#todo   createWhile(condition, body)*/
/*#todo   createFor(init, condition, update, body)*/
/*#todo   createBreak()*/
ASTNode* createWhile(ASTNode* condition, ASTNode* body);
ASTNode* createFor(ASTNode* init, ASTNode* condition, ASTNode* update, ASTNode* body);
ASTNode* createBreak(void);
/*#end*/
/*#5*/
/*#todo Declare the constructors for the decision nodes:*/
/*#todo   createIf(condition, thenStmt, elseStmt)*/
/*#todo   createSwitch(expr, cases)*/
/*#todo   createCase(value, isDefault, body)*/
ASTNode* createIf(ASTNode* condition, ASTNode* then_stmt, ASTNode* else_stmt);
ASTNode* createSwitch(ASTNode* expr, ASTNode* cases);
ASTNode* createCase(int value, int isDefault, ASTNode* body);
/*#end*/

/*#3*/
/*#todo Declare the array constructors.  Note createArrayParam is separate from*/
/*#todo createArrayDecl: a parameter has no size and is a reference, not storage.*/
/* Array nodes */
ASTNode* createArrayDecl(char* name, int size);                 /* Create array declaration */
ASTNode* createArrayParam(char* name);                          /* Create array parameter */
ASTNode* createArrayIndex(char* name, ASTNode* index);          /* Create array indexing */
/*#end*/

/* Text form of a packed operator code (see createBinOp) */
const char* opText(char op);

/* AST DISPLAY FUNCTION */
void printAST(ASTNode* node, int level);                        /* Pretty-print the AST */

#endif