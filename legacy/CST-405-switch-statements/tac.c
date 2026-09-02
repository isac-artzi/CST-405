#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "tac.h"

TACList tacList;
TACList optimizedList;
TempAllocator tempAlloc;

void initTAC() {
    tacList.head = NULL;
    tacList.tail = NULL;
    tacList.tempCount = 0;
    tacList.labelCount = 0;
    optimizedList.head = NULL;
    optimizedList.tail = NULL;

    /* Initialize temporary allocator */
    for (int i = 0; i < MAX_TEMPS; i++) {
        tempAlloc.allocated[i] = 0;
    }
    tempAlloc.maxUsed = 0;
    tempAlloc.freeCount = 0;
    printf("TAC: Temporary allocator initialized\n");
}

char* newTemp() {
    char* temp = malloc(10);
    sprintf(temp, "t%d", tacList.tempCount++);
    return temp;
}

char* allocTemp() {
    int tempNum;

    if (tempAlloc.freeCount > 0) {
        tempNum = tempAlloc.freeList[--tempAlloc.freeCount];
        printf("    [TAC ALLOC] Reusing temporary t%d\n", tempNum);
    } else {
        tempNum = tempAlloc.maxUsed++;
        if (tempNum >= MAX_TEMPS) {
            fprintf(stderr, "ERROR: Exceeded maximum temporaries\n");
            exit(1);
        }
        printf("    [TAC ALLOC] Allocating new temporary t%d\n", tempNum);
    }

    tempAlloc.allocated[tempNum] = 1;
    char* temp = malloc(10);
    sprintf(temp, "t%d", tempNum);
    return temp;
}

void freeTemp(char* temp) {
    if (!temp || temp[0] != 't') return;

    int tempNum = atoi(temp + 1);
    if (!tempAlloc.allocated[tempNum]) return;

    tempAlloc.allocated[tempNum] = 0;
    if (tempAlloc.freeCount < MAX_TEMPS) {
        tempAlloc.freeList[tempAlloc.freeCount++] = tempNum;
        printf("    [TAC FREE] Released temporary %s\n", temp);
    }
}

char* newLabel() {
    char* label = malloc(10);
    sprintf(label, "L%d", tacList.labelCount++);
    return label;
}

void printTempAllocatorState() {
    printf("\n┌──────────────────────────────────────────────────────────┐\n");
    printf("│ TEMPORARY ALLOCATOR STATISTICS                           │\n");
    printf("├──────────────────────────────────────────────────────────┤\n");
    printf("│ Total temporaries used:      %3d                         │\n", tempAlloc.maxUsed);
    printf("│ Currently allocated:         %3d                         │\n",
           tempAlloc.maxUsed - tempAlloc.freeCount);
    printf("│ Available for reuse:         %3d                         │\n", tempAlloc.freeCount);
    printf("└──────────────────────────────────────────────────────────┘\n\n");
}

TACInstr* createTAC(TACOp op, char* arg1, char* arg2, char* result) {
    TACInstr* instr = malloc(sizeof(TACInstr));
    instr->op = op;
    instr->arg1 = arg1 ? strdup(arg1) : NULL;
    instr->arg2 = arg2 ? strdup(arg2) : NULL;
    instr->result = result ? strdup(result) : NULL;
    instr->next = NULL;
    return instr;
}

void appendTAC(TACInstr* instr) {
    if (!tacList.head) {
        tacList.head = tacList.tail = instr;
    } else {
        tacList.tail->next = instr;
        tacList.tail = instr;
    }
}

void appendOptimizedTAC(TACInstr* instr) {
    if (!optimizedList.head) {
        optimizedList.head = optimizedList.tail = instr;
    } else {
        optimizedList.tail->next = instr;
        optimizedList.tail = instr;
    }
}

/* ── BREAK LABEL STACK ──────────────────────────────────────────────────────
 * When entering a switch, for, or while, push the "end" label so that any
 * nested NODE_BREAK can emit GOTO to the right exit point.
 */
#define MAX_BREAK_DEPTH 64
static char* breakLabelStack[MAX_BREAK_DEPTH];
static int   breakLabelTop = 0;

static void pushBreakLabel(char* label) {
    if (breakLabelTop < MAX_BREAK_DEPTH)
        breakLabelStack[breakLabelTop++] = label;
    else
        fprintf(stderr, "TAC Error: break label stack overflow\n");
}

static char* peekBreakLabel() {
    return (breakLabelTop > 0) ? breakLabelStack[breakLabelTop - 1] : NULL;
}

static void popBreakLabel() {
    if (breakLabelTop > 0) breakLabelTop--;
}

/* Forward declarations */
static void generateTACStmt(ASTNode* node);
static int generateArgTAC(ASTNode* arg);

/* Recursively generate TAC for function call arguments, returns count */
static int generateArgTAC(ASTNode* arg) {
    if (!arg) return 0;

    if (arg->type == NODE_ARG_LIST) {
        // Check if expr is nested ARG_LIST
        if (arg->data.arg_list.expr && arg->data.arg_list.expr->type == NODE_ARG_LIST) {
            // Recursively process nested list
            return generateArgTAC(arg->data.arg_list.expr) + generateArgTAC(arg->data.arg_list.next);
        } else {
            // Process this argument
            char* argTemp = generateTACExpr(arg->data.arg_list.expr);
            appendTAC(createTAC(TAC_ARG, argTemp, NULL, NULL));
            // Process remaining arguments
            return 1 + generateArgTAC(arg->data.arg_list.next);
        }
    } else {
        // Single argument
        char* argTemp = generateTACExpr(arg);
        appendTAC(createTAC(TAC_ARG, argTemp, NULL, NULL));
        return 1;
    }
}

/* Generate TAC for expression - returns the temp/var holding result */
char* generateTACExpr(ASTNode* node) {
    if (!node) return NULL;

    switch(node->type) {
        case NODE_NUM: {
            char* temp = malloc(20);
            sprintf(temp, "%d", node->data.num);
            return temp;
        }

        case NODE_VAR:
            return strdup(node->data.name);

        case NODE_BINOP: {
            char* left = generateTACExpr(node->data.binop.left);
            char* right = NULL;

            /* Unary minus has no right operand */
            if (node->data.binop.op != 'u') {
                right = generateTACExpr(node->data.binop.right);
            }

            char* temp = allocTemp();

            /* Select operation type */
            TACOp op;
            switch(node->data.binop.op) {
                case '+': op = TAC_ADD; break;
                case '-': op = TAC_SUB; break;
                case '*': op = TAC_MUL; break;
                case '/': op = TAC_DIV; break;
                case '<': op = TAC_LT; break;
                case '>': op = TAC_GT; break;
                case 'l': op = TAC_LE; break;  /* <= */
                case 'g': op = TAC_GE; break;  /* >= */
                case 'e': op = TAC_EQ; break;  /* == */
                case 'n': op = TAC_NE; break;  /* != */
                case 'u': op = TAC_NEG; break; /* unary - */
                default:  op = TAC_ADD; break;
            }

            appendTAC(createTAC(op, left, right, temp));

            freeTemp(left);
            if (right) freeTemp(right);

            return temp;
        }

        case NODE_FUNC_CALL: {
            /* Generate TAC for arguments and count them */
            int argCount = generateArgTAC(node->data.func_call.args);

            /* Generate call instruction */
            char* result = allocTemp();
            char argCountStr[10];
            sprintf(argCountStr, "%d", argCount);
            appendTAC(createTAC(TAC_CALL, node->data.func_call.name, argCountStr, result));

            return result;
        }

        case NODE_ARRAY_INDEX: {
            /* Generate index expression */
            char* indexTemp = generateTACExpr(node->data.array_index.index);

            /* Allocate temporary for result */
            char* resultTemp = allocTemp();

            /* Generate TAC_ARRAY_LOAD: result = array[index] */
            appendTAC(createTAC(TAC_ARRAY_LOAD, node->data.array_index.name, indexTemp, resultTemp));

            freeTemp(indexTemp);
            return resultTemp;
        }

        default:
            return NULL;
    }
}

/* Generate TAC for statement list */
static void generateTACStmtList(ASTNode* node) {
    if (!node) return;

    if (node->type == NODE_STMT_LIST) {
        generateTACStmt(node->data.stmtlist.stmt);
        generateTACStmtList(node->data.stmtlist.next);
    } else {
        generateTACStmt(node);
    }
}

/* Generate TAC for a statement */
static void generateTACStmt(ASTNode* node) {
    if (!node) return;

    switch(node->type) {
        case NODE_DECL:
            appendTAC(createTAC(TAC_DECL, node->data.decl.varType, NULL, node->data.decl.name));
            break;

        case NODE_ASSIGN: {
            char* expr = generateTACExpr(node->data.assign.value);

            if (node->data.assign.arrayLHS) {
                /* Array element assignment: arr[index] = expr */
                ASTNode* arrayIndex = node->data.assign.arrayLHS;
                char* indexTemp = generateTACExpr(arrayIndex->data.array_index.index);

                /* Generate TAC_ARRAY_STORE: array[index] = value */
                appendTAC(createTAC(TAC_ARRAY_STORE, arrayIndex->data.array_index.name, indexTemp, expr));

                freeTemp(indexTemp);
            } else {
                /* Regular assignment */
                appendTAC(createTAC(TAC_ASSIGN, expr, NULL, node->data.assign.var));
            }
            freeTemp(expr);
            break;
        }

        case NODE_PRINT: {
            char* expr = generateTACExpr(node->data.expr);
            appendTAC(createTAC(TAC_PRINT, expr, NULL, NULL));
            freeTemp(expr);
            break;
        }

        case NODE_RETURN: {
            if (node->data.ret.expr) {
                char* expr = generateTACExpr(node->data.ret.expr);
                appendTAC(createTAC(TAC_RETURN, expr, NULL, NULL));
                freeTemp(expr);
            } else {
                appendTAC(createTAC(TAC_RETURN, NULL, NULL, NULL));
            }
            break;
        }

        case NODE_IF: {
            /* Generate labels */
            char* labelElse = newLabel();
            char* labelEnd = newLabel();

            /* Evaluate condition */
            char* cond = generateTACExpr(node->data.if_stmt.condition);

            /* If condition is false, jump to else (or end) */
            if (node->data.if_stmt.else_stmt) {
                appendTAC(createTAC(TAC_IF_FALSE, cond, labelElse, NULL));
            } else {
                appendTAC(createTAC(TAC_IF_FALSE, cond, labelEnd, NULL));
            }
            freeTemp(cond);

            /* Generate then branch */
            generateTACStmt(node->data.if_stmt.then_stmt);

            if (node->data.if_stmt.else_stmt) {
                /* Jump over else branch */
                appendTAC(createTAC(TAC_GOTO, labelEnd, NULL, NULL));

                /* Else label */
                appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelElse));

                /* Generate else branch */
                generateTACStmt(node->data.if_stmt.else_stmt);
            }

            /* End label */
            appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelEnd));
            break;
        }

        case NODE_WHILE: {
            /* Generate labels */
            char* labelStart = newLabel();
            char* labelEnd = newLabel();

            /* Start label */
            appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelStart));

            /* Evaluate condition */
            char* cond = generateTACExpr(node->data.while_stmt.condition);

            /* If condition is false, jump to end */
            appendTAC(createTAC(TAC_IF_FALSE, cond, labelEnd, NULL));
            freeTemp(cond);

            /* Generate body — break exits to labelEnd */
            pushBreakLabel(labelEnd);
            generateTACStmt(node->data.while_stmt.body);
            popBreakLabel();

            /* Jump back to start */
            appendTAC(createTAC(TAC_GOTO, labelStart, NULL, NULL));

            /* End label */
            appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelEnd));
            break;
        }

        case NODE_FOR: {
            /* FOR LOOP TAC GENERATION
             * A for loop: for (init; cond; update) body
             * Is lowered to:
             *   [init]
             * L_start:
             *   t = [cond]          ← only if condition present
             *   IF_FALSE t GOTO L_end
             *   [body]
             * L_update:             ← jump target for conceptual "continue"
             *   [update]
             *   GOTO L_start
             * L_end:
             */
            char* labelStart  = newLabel();  /* Top of loop – condition check */
            char* labelUpdate = newLabel();  /* Update step label */
            char* labelEnd    = newLabel();  /* Past the loop */

            /* 1. Execute initialization once before the loop begins */
            if (node->data.for_stmt.init) {
                generateTACStmt(node->data.for_stmt.init);
            }

            /* 2. Emit the loop-start label – condition is tested here */
            appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelStart));

            /* 3. Evaluate condition (if present); if false, exit loop */
            if (node->data.for_stmt.condition) {
                char* cond = generateTACExpr(node->data.for_stmt.condition);
                appendTAC(createTAC(TAC_IF_FALSE, cond, labelEnd, NULL));
                freeTemp(cond);
            }
            /* No condition means the loop runs unconditionally (infinite) */

            /* 4. Generate loop body — break exits to labelEnd */
            pushBreakLabel(labelEnd);
            generateTACStmt(node->data.for_stmt.body);
            popBreakLabel();

            /* 5. Emit the update label then execute the update expression */
            appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelUpdate));
            if (node->data.for_stmt.update) {
                generateTACStmt(node->data.for_stmt.update);
            }

            /* 6. Jump back to the top to re-check the condition */
            appendTAC(createTAC(TAC_GOTO, labelStart, NULL, NULL));

            /* 7. End-of-loop label – execution resumes here when condition fails */
            appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelEnd));
            break;
        }

        case NODE_BLOCK:
            generateTACStmtList(node->data.block.stmt_list);
            break;

        case NODE_FUNC_CALL:
            /* Function call as statement (result discarded) */
            generateTACExpr(node);
            break;

        case NODE_STMT_LIST:
            generateTACStmtList(node);
            break;

        case NODE_ARRAY_DECL: {
            /* Generate array declaration */
            if (!node->data.array_decl.isParam) {
                char sizeStr[20];
                sprintf(sizeStr, "%d", node->data.array_decl.size);
                appendTAC(createTAC(TAC_ARRAY_DECL, sizeStr, NULL, node->data.array_decl.name));
            } else {
                /* Array parameter - handled by TAC_PARAM */
                appendTAC(createTAC(TAC_PARAM, NULL, NULL, node->data.array_decl.name));
            }
            break;
        }

        case NODE_SWITCH: {
            /* SWITCH STATEMENT TAC GENERATION
             *
             * Strategy: linear-scan dispatch + separate body section.
             *
             * Structure emitted:
             *   DECL  __swN            ; hidden variable for controlling expr
             *   ASSIGN expr -> __swN   ; evaluate controlling expression once
             *
             *   ; --- dispatch table ---
             *   tCmp = __swN == c0
             *   IF_FALSE tCmp GOTO L_test1
             *   GOTO L_body0
             * L_test1:
             *   tCmp = __swN == c1
             *   IF_FALSE tCmp GOTO L_dispatch_done
             *   GOTO L_body1
             * L_dispatch_done:
             *   GOTO L_default   (or GOTO L_end if no default)
             *
             *   ; --- case bodies (fall-through between them is intentional) ---
             * L_body0:
             *   <body0>
             *   GOTO L_end        ; only if body contains break
             * L_body1:
             *   <body1>
             *   GOTO L_end
             * L_default:
             *   <default body>
             * L_end:
             */

            /* Step 1: Evaluate controlling expression into a hidden named variable
             * so it survives label-induced register invalidations. */
            char switchVar[32];
            sprintf(switchVar, "__sw%d", tacList.labelCount);
            appendTAC(createTAC(TAC_DECL, NULL, NULL, switchVar));

            char* switchVal = generateTACExpr(node->data.switch_stmt.expr);
            appendTAC(createTAC(TAC_ASSIGN, switchVal, NULL, switchVar));
            freeTemp(switchVal);

            /* Step 2: Count cases and pre-allocate body labels */
            int caseCount = 0;
            ASTNode* c = node->data.switch_stmt.cases;
            while (c) { caseCount++; c = c->data.case_clause.next; }

            if (caseCount == 0) {
                /* Empty switch — nothing to emit */
                break;
            }

            char** bodyLabels = (char**)malloc(sizeof(char*) * caseCount);
            ASTNode** caseArr  = (ASTNode**)malloc(sizeof(ASTNode*) * caseCount);

            int defaultIdx    = -1;   /* index of the default clause (-1 = none) */
            int nonDefCount   = 0;    /* number of non-default cases */
            int* nonDefIdx    = (int*)malloc(sizeof(int) * caseCount);

            c = node->data.switch_stmt.cases;
            for (int i = 0; i < caseCount; i++) {
                bodyLabels[i] = newLabel();
                caseArr[i]    = c;
                if (c->data.case_clause.isDefault) {
                    defaultIdx = i;
                } else {
                    nonDefIdx[nonDefCount++] = i;
                }
                c = c->data.case_clause.next;
            }

            char* labelDispatchDone = newLabel();
            char* labelEnd          = newLabel();

            /* Step 3: Emit dispatch table */
            for (int ni = 0; ni < nonDefCount; ni++) {
                int   i         = nonDefIdx[ni];
                ASTNode* cas    = caseArr[i];

                /* Compare switch variable to case constant */
                char caseConst[32];
                sprintf(caseConst, "%d", cas->data.case_clause.value);
                char* cmpTemp = allocTemp();
                appendTAC(createTAC(TAC_EQ, switchVar, caseConst, cmpTemp));

                /* If not equal: skip to next test (or dispatch_done if last) */
                char* failTarget;
                if (ni < nonDefCount - 1) {
                    failTarget = newLabel();   /* will be emitted below */
                } else {
                    failTarget = labelDispatchDone;
                }
                appendTAC(createTAC(TAC_IF_FALSE, cmpTemp, failTarget, NULL));
                freeTemp(cmpTemp);

                /* If equal: jump to this case's body */
                appendTAC(createTAC(TAC_GOTO, bodyLabels[i], NULL, NULL));

                /* Emit the fail-target label for next iteration (except last) */
                if (ni < nonDefCount - 1) {
                    appendTAC(createTAC(TAC_LABEL, NULL, NULL, failTarget));
                }
            }

            /* Dispatch done: no case matched → jump to default or end */
            appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelDispatchDone));
            if (defaultIdx >= 0) {
                appendTAC(createTAC(TAC_GOTO, bodyLabels[defaultIdx], NULL, NULL));
            } else {
                appendTAC(createTAC(TAC_GOTO, labelEnd, NULL, NULL));
            }

            /* Step 4: Emit case bodies (order: non-default first, then default
             * at its original position to preserve fall-through semantics) */
            pushBreakLabel(labelEnd);
            for (int i = 0; i < caseCount; i++) {
                appendTAC(createTAC(TAC_LABEL, NULL, NULL, bodyLabels[i]));
                if (caseArr[i]->data.case_clause.body) {
                    generateTACStmt(caseArr[i]->data.case_clause.body);
                }
            }
            popBreakLabel();

            /* End of switch */
            appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelEnd));

            free(bodyLabels);
            free(caseArr);
            free(nonDefIdx);
            break;
        }

        case NODE_BREAK: {
            /* BREAK STATEMENT TAC GENERATION
             * Emit an unconditional jump to the innermost enclosing switch/loop
             * end label (top of the break label stack).
             */
            char* breakTarget = peekBreakLabel();
            if (breakTarget) {
                appendTAC(createTAC(TAC_GOTO, breakTarget, NULL, NULL));
            } else {
                fprintf(stderr, "TAC Error: break statement outside any switch/loop\n");
            }
            break;
        }

        default:
            break;
    }
}

/* Recursively generate TAC for function parameters */
static void generateParamTAC(ASTNode* param) {
    if (!param) return;

    if (param->type == NODE_PARAM) {
        appendTAC(createTAC(TAC_PARAM, NULL, NULL, param->data.param.name));
    } else if (param->type == NODE_ARRAY_DECL && param->data.array_decl.isParam) {
        appendTAC(createTAC(TAC_PARAM, NULL, NULL, param->data.array_decl.name));
    } else if (param->type == NODE_PARAM_LIST) {
        // Recursively process nested param lists
        generateParamTAC(param->data.param_list.param);
        generateParamTAC(param->data.param_list.next);
    }
}

/* Generate TAC for function definition */
static void generateTACFuncDef(ASTNode* node) {
    if (!node || node->type != NODE_FUNC_DEF) return;

    /* Function begin marker */
    appendTAC(createTAC(TAC_FUNC_BEGIN, NULL, NULL, node->data.func_def.name));

    /* Generate parameter declarations */
    generateParamTAC(node->data.func_def.params);

    /* Generate function body */
    generateTACStmt(node->data.func_def.body);

    /* Function end marker */
    appendTAC(createTAC(TAC_FUNC_END, NULL, NULL, node->data.func_def.name));
}

/* Recursive helper to generate TAC for declarations/functions list */
static void generateTACList(ASTNode* node) {
    if (!node) return;

    if (node->type == NODE_STMT_LIST) {
        /* The stmt field might itself be a STMT_LIST (left-recursive grammar) */
        generateTACList(node->data.stmtlist.stmt);
        /* The next field contains the last item */
        generateTACList(node->data.stmtlist.next);
    } else if (node->type == NODE_FUNC_DEF) {
        generateTACFuncDef(node);
    } else {
        generateTACStmt(node);
    }
}

/* Main TAC generation entry point */
void generateTAC(ASTNode* node) {
    if (!node) return;
    generateTACList(node);
}

/* Get operation name for printing */
static const char* getOpName(TACOp op) {
    switch(op) {
        case TAC_ADD: return "+";
        case TAC_SUB: return "-";
        case TAC_MUL: return "*";
        case TAC_DIV: return "/";
        case TAC_NEG: return "NEG";
        case TAC_LT: return "<";
        case TAC_GT: return ">";
        case TAC_LE: return "<=";
        case TAC_GE: return ">=";
        case TAC_EQ: return "==";
        case TAC_NE: return "!=";
        default: return "?";
    }
}

void printTAC() {
    printf("Unoptimized TAC Instructions:\n");
    printf("─────────────────────────────\n");
    TACInstr* curr = tacList.head;
    int lineNum = 1;
    while (curr) {
        printf("%3d: ", lineNum++);
        switch(curr->op) {
            case TAC_FUNC_BEGIN:
                printf("FUNC_BEGIN %s\n", curr->result);
                break;
            case TAC_FUNC_END:
                printf("FUNC_END %s\n", curr->result);
                break;
            case TAC_PARAM:
                printf("PARAM %s\n", curr->result);
                break;
            case TAC_DECL:
                printf("DECL %s\n", curr->result);
                break;
            case TAC_ADD:
            case TAC_SUB:
            case TAC_MUL:
            case TAC_DIV:
            case TAC_LT:
            case TAC_GT:
            case TAC_LE:
            case TAC_GE:
            case TAC_EQ:
            case TAC_NE:
                printf("%s = %s %s %s\n", curr->result, curr->arg1,
                       getOpName(curr->op), curr->arg2);
                break;
            case TAC_NEG:
                printf("%s = -%s\n", curr->result, curr->arg1);
                break;
            case TAC_ASSIGN:
                printf("%s = %s\n", curr->result, curr->arg1);
                break;
            case TAC_PRINT:
                printf("PRINT %s\n", curr->arg1);
                break;
            case TAC_ARG:
                printf("ARG %s\n", curr->arg1);
                break;
            case TAC_CALL:
                printf("%s = CALL %s, %s\n", curr->result, curr->arg1, curr->arg2);
                break;
            case TAC_RETURN:
                if (curr->arg1) {
                    printf("RETURN %s\n", curr->arg1);
                } else {
                    printf("RETURN\n");
                }
                break;
            case TAC_LABEL:
                printf("%s:\n", curr->result);
                break;
            case TAC_GOTO:
                printf("GOTO %s\n", curr->arg1);
                break;
            case TAC_IF_FALSE:
                printf("IF_FALSE %s GOTO %s\n", curr->arg1, curr->arg2);
                break;
            case TAC_IF_TRUE:
                printf("IF_TRUE %s GOTO %s\n", curr->arg1, curr->arg2);
                break;
            case TAC_ARRAY_DECL:
                printf("ARRAY_DECL %s[%s]\n", curr->result, curr->arg1);
                break;
            case TAC_ARRAY_LOAD:
                printf("%s = %s[%s]\n", curr->result, curr->arg1, curr->arg2);
                break;
            case TAC_ARRAY_STORE:
                printf("%s[%s] = %s\n", curr->arg1, curr->arg2, curr->result);
                break;
            default:
                printf("UNKNOWN\n");
                break;
        }
        curr = curr->next;
    }
}

/* Helper: Check if string is a constant number */
static int isConstantNumber(const char* str) {
    if (!str || str[0] == '\0') return 0;
    int i = 0;
    if (str[i] == '-' || str[i] == '+') i++;
    if (str[i] == '\0') return 0;
    while (str[i] != '\0') {
        if (str[i] < '0' || str[i] > '9') return 0;
        i++;
    }
    return 1;
}

/* Helper: Perform constant folding on binary operation */
static char* foldConstants(TACOp op, const char* arg1, const char* arg2, int* folded) {
    *folded = 0;

    if (!isConstantNumber(arg1) || !isConstantNumber(arg2)) {
        return NULL;
    }

    int val1 = atoi(arg1);
    int val2 = atoi(arg2);
    int result = 0;

    switch(op) {
        case TAC_ADD: result = val1 + val2; *folded = 1; break;
        case TAC_SUB: result = val1 - val2; *folded = 1; break;
        case TAC_MUL: result = val1 * val2; *folded = 1; break;
        case TAC_DIV:
            if (val2 != 0) {
                result = val1 / val2;
                *folded = 1;
            }
            break;
        case TAC_LT: result = (val1 < val2) ? 1 : 0; *folded = 1; break;
        case TAC_GT: result = (val1 > val2) ? 1 : 0; *folded = 1; break;
        case TAC_LE: result = (val1 <= val2) ? 1 : 0; *folded = 1; break;
        case TAC_GE: result = (val1 >= val2) ? 1 : 0; *folded = 1; break;
        case TAC_EQ: result = (val1 == val2) ? 1 : 0; *folded = 1; break;
        case TAC_NE: result = (val1 != val2) ? 1 : 0; *folded = 1; break;
        default: break;
    }

    if (*folded) {
        char* resultStr = malloc(20);
        sprintf(resultStr, "%d", result);
        return resultStr;
    }
    return NULL;
}

/* TAC Optimization with tracking */
void optimizeTAC() {
    int optimizationCount = 0;

    printf("\n┌──────────────────────────────────────────────────────────┐\n");
    printf("│ OPTIMIZATION PASS - Tracking Changes                    │\n");
    printf("├──────────────────────────────────────────────────────────┤\n");
    printf("│ Analyzing each instruction for optimization opportunities│\n");
    printf("├──────────────────────────────────────────────────────────┤\n");

    TACInstr* curr = tacList.head;
    int instrNum = 1;

    while (curr) {
        int optimized = 0;
        TACInstr* newInstr = NULL;

        /* Constant Folding for binary operations */
        if (curr->op == TAC_ADD || curr->op == TAC_SUB ||
            curr->op == TAC_MUL || curr->op == TAC_DIV ||
            curr->op == TAC_LT || curr->op == TAC_GT ||
            curr->op == TAC_LE || curr->op == TAC_GE ||
            curr->op == TAC_EQ || curr->op == TAC_NE) {

            int folded = 0;
            char* foldedValue = foldConstants(curr->op, curr->arg1, curr->arg2, &folded);

            if (folded) {
                /* Replace operation with assignment of constant */
                newInstr = createTAC(TAC_ASSIGN, foldedValue, NULL, curr->result);
                printf("│ [%3d] ✓ CONSTANT FOLDING: %s = %s %s %s\n",
                       instrNum, curr->result, curr->arg1, getOpName(curr->op), curr->arg2);
                printf("│       → Evaluating: %s %s %s = %s\n",
                       curr->arg1, getOpName(curr->op), curr->arg2, foldedValue);
                printf("│       → Simplified to: %s = %s\n", curr->result, foldedValue);
                optimizationCount++;
                optimized = 1;
                free(foldedValue);
            }
        }

        /* Copy Propagation for assignments of constants */
        if (!optimized && curr->op == TAC_ASSIGN && isConstantNumber(curr->arg1)) {
            newInstr = createTAC(curr->op, curr->arg1, curr->arg2, curr->result);
            printf("│ [%3d] COPY PROPAGATION: %s = %s (constant)\n",
                   instrNum, curr->result, curr->arg1);
            optimizationCount++;
            optimized = 1;
        }

        /* Dead Loop Elimination: Optimize IF_FALSE with constant condition */
        if (!optimized && curr->op == TAC_IF_FALSE && isConstantNumber(curr->arg1)) {
            int condValue = atoi(curr->arg1);
            if (condValue == 0) {
                /* Condition is always false - always jump */
                newInstr = createTAC(TAC_GOTO, curr->arg2, NULL, NULL);
                printf("│ [%3d] ✓ DEAD LOOP ELIMINATION: if_false %s goto %s\n",
                       instrNum, curr->arg1, curr->arg2);
                printf("│       → Condition always false, converted to: goto %s\n", curr->arg2);
                optimizationCount++;
                optimized = 1;
            } else {
                /* Condition is always true - never jump (dead branch) */
                /* We skip this instruction by not creating newInstr */
                printf("│ [%3d] ✓ DEAD BRANCH ELIMINATION: if_false %s goto %s\n",
                       instrNum, curr->arg1, curr->arg2);
                printf("│       → Condition always true, branch removed\n");
                optimizationCount++;
                optimized = 1;
                /* Don't append anything - effectively removes the instruction */
                curr = curr->next;
                instrNum++;
                continue;
            }
        }

        /* Infinite Loop Detection: Optimize IF_TRUE with constant condition */
        if (!optimized && curr->op == TAC_IF_TRUE && isConstantNumber(curr->arg1)) {
            int condValue = atoi(curr->arg1);
            if (condValue != 0) {
                /* Condition is always true - always jump */
                newInstr = createTAC(TAC_GOTO, curr->arg2, NULL, NULL);
                printf("│ [%3d] ✓ CONSTANT BRANCH: if_true %s goto %s\n",
                       instrNum, curr->arg1, curr->arg2);
                printf("│       → Condition always true, converted to: goto %s\n", curr->arg2);
                optimizationCount++;
                optimized = 1;
            } else {
                /* Condition is always false - never jump (dead branch) */
                printf("│ [%3d] ✓ DEAD BRANCH ELIMINATION: if_true %s goto %s\n",
                       instrNum, curr->arg1, curr->arg2);
                printf("│       → Condition always false, branch removed\n");
                optimizationCount++;
                optimized = 1;
                /* Don't append anything - effectively removes the instruction */
                curr = curr->next;
                instrNum++;
                continue;
            }
        }

        /* If no optimization applied, copy instruction as-is */
        if (!newInstr) {
            newInstr = createTAC(curr->op, curr->arg1, curr->arg2, curr->result);
        }

        appendOptimizedTAC(newInstr);
        curr = curr->next;
        instrNum++;
    }

    printf("├──────────────────────────────────────────────────────────┤\n");
    printf("│ Total optimizations applied: %3d                         │\n", optimizationCount);
    printf("└──────────────────────────────────────────────────────────┘\n\n");
}

void printOptimizedTAC() {
    printf("Optimized TAC Instructions:\n");
    printf("─────────────────────────────\n");
    TACInstr* curr = optimizedList.head;
    int lineNum = 1;
    while (curr) {
        printf("%3d: ", lineNum++);
        switch(curr->op) {
            case TAC_FUNC_BEGIN:
                printf("FUNC_BEGIN %s\n", curr->result);
                break;
            case TAC_FUNC_END:
                printf("FUNC_END %s\n", curr->result);
                break;
            case TAC_PARAM:
                printf("PARAM %s\n", curr->result);
                break;
            case TAC_DECL:
                printf("DECL %s\n", curr->result);
                break;
            case TAC_ADD:
            case TAC_SUB:
            case TAC_MUL:
            case TAC_DIV:
            case TAC_LT:
            case TAC_GT:
            case TAC_LE:
            case TAC_GE:
            case TAC_EQ:
            case TAC_NE:
                printf("%s = %s %s %s\n", curr->result, curr->arg1,
                       getOpName(curr->op), curr->arg2);
                break;
            case TAC_NEG:
                printf("%s = -%s\n", curr->result, curr->arg1);
                break;
            case TAC_ASSIGN:
                printf("%s = %s\n", curr->result, curr->arg1);
                break;
            case TAC_PRINT:
                printf("PRINT %s\n", curr->arg1);
                break;
            case TAC_ARG:
                printf("ARG %s\n", curr->arg1);
                break;
            case TAC_CALL:
                printf("%s = CALL %s, %s\n", curr->result, curr->arg1, curr->arg2);
                break;
            case TAC_RETURN:
                if (curr->arg1) {
                    printf("RETURN %s\n", curr->arg1);
                } else {
                    printf("RETURN\n");
                }
                break;
            case TAC_LABEL:
                printf("%s:\n", curr->result);
                break;
            case TAC_GOTO:
                printf("GOTO %s\n", curr->arg1);
                break;
            case TAC_IF_FALSE:
                printf("IF_FALSE %s GOTO %s\n", curr->arg1, curr->arg2);
                break;
            case TAC_IF_TRUE:
                printf("IF_TRUE %s GOTO %s\n", curr->arg1, curr->arg2);
                break;
            case TAC_ARRAY_DECL:
                printf("ARRAY_DECL %s[%s]\n", curr->result, curr->arg1);
                break;
            case TAC_ARRAY_LOAD:
                printf("%s = %s[%s]\n", curr->result, curr->arg1, curr->arg2);
                break;
            case TAC_ARRAY_STORE:
                printf("%s[%s] = %s\n", curr->arg1, curr->arg2, curr->result);
                break;
            default:
                printf("UNKNOWN\n");
                break;
        }
        curr = curr->next;
    }
}

TACList* getOptimizedTAC() {
    return &optimizedList;
}

void saveTACToFile(const char* filename) {
    FILE* file = fopen(filename, "w");
    if (!file) {
        fprintf(stderr, "Error: Cannot open file '%s' for writing\n", filename);
        return;
    }

    fprintf(file, "Unoptimized Three-Address Code (TAC)\n");
    fprintf(file, "=====================================\n");
    fprintf(file, "Intermediate representation with functions\n\n");

    TACInstr* curr = tacList.head;
    int lineNum = 1;
    while (curr) {
        fprintf(file, "%3d: ", lineNum++);
        switch(curr->op) {
            case TAC_FUNC_BEGIN:
                fprintf(file, "FUNC_BEGIN %s\n", curr->result);
                break;
            case TAC_FUNC_END:
                fprintf(file, "FUNC_END %s\n", curr->result);
                break;
            case TAC_PARAM:
                fprintf(file, "PARAM %s\n", curr->result);
                break;
            case TAC_DECL:
                fprintf(file, "DECL %s\n", curr->result);
                break;
            case TAC_ADD:
            case TAC_SUB:
            case TAC_MUL:
            case TAC_DIV:
            case TAC_LT:
            case TAC_GT:
            case TAC_LE:
            case TAC_GE:
            case TAC_EQ:
            case TAC_NE:
                fprintf(file, "%s = %s %s %s\n", curr->result, curr->arg1,
                       getOpName(curr->op), curr->arg2);
                break;
            case TAC_NEG:
                fprintf(file, "%s = -%s\n", curr->result, curr->arg1);
                break;
            case TAC_ASSIGN:
                fprintf(file, "%s = %s\n", curr->result, curr->arg1);
                break;
            case TAC_PRINT:
                fprintf(file, "PRINT %s\n", curr->arg1);
                break;
            case TAC_ARG:
                fprintf(file, "ARG %s\n", curr->arg1);
                break;
            case TAC_CALL:
                fprintf(file, "%s = CALL %s, %s\n", curr->result, curr->arg1, curr->arg2);
                break;
            case TAC_RETURN:
                if (curr->arg1) {
                    fprintf(file, "RETURN %s\n", curr->arg1);
                } else {
                    fprintf(file, "RETURN\n");
                }
                break;
            case TAC_LABEL:
                fprintf(file, "%s:\n", curr->result);
                break;
            case TAC_GOTO:
                fprintf(file, "GOTO %s\n", curr->arg1);
                break;
            case TAC_IF_FALSE:
                fprintf(file, "IF_FALSE %s GOTO %s\n", curr->arg1, curr->arg2);
                break;
            case TAC_IF_TRUE:
                fprintf(file, "IF_TRUE %s GOTO %s\n", curr->arg1, curr->arg2);
                break;
            case TAC_ARRAY_DECL:
                fprintf(file, "ARRAY_DECL %s[%s]\n", curr->result, curr->arg1);
                break;
            case TAC_ARRAY_LOAD:
                fprintf(file, "%s = %s[%s]\n", curr->result, curr->arg1, curr->arg2);
                break;
            case TAC_ARRAY_STORE:
                fprintf(file, "%s[%s] = %s\n", curr->arg1, curr->arg2, curr->result);
                break;
            default:
                fprintf(file, "UNKNOWN\n");
                break;
        }
        curr = curr->next;
    }

    fclose(file);
    printf("✓ Unoptimized TAC saved to: %s\n", filename);
}

void saveOptimizedTACToFile(const char* filename) {
    FILE* file = fopen(filename, "w");
    if (!file) {
        fprintf(stderr, "Error: Cannot open file '%s' for writing\n", filename);
        return;
    }

    fprintf(file, "Optimized Three-Address Code (TAC)\n");
    fprintf(file, "===================================\n");
    fprintf(file, "With function support and control flow\n\n");

    TACInstr* curr = optimizedList.head;
    int lineNum = 1;
    while (curr) {
        fprintf(file, "%3d: ", lineNum++);
        switch(curr->op) {
            case TAC_FUNC_BEGIN:
                fprintf(file, "FUNC_BEGIN %s\n", curr->result);
                break;
            case TAC_FUNC_END:
                fprintf(file, "FUNC_END %s\n", curr->result);
                break;
            case TAC_PARAM:
                fprintf(file, "PARAM %s\n", curr->result);
                break;
            case TAC_DECL:
                fprintf(file, "DECL %s\n", curr->result);
                break;
            case TAC_ADD:
            case TAC_SUB:
            case TAC_MUL:
            case TAC_DIV:
            case TAC_LT:
            case TAC_GT:
            case TAC_LE:
            case TAC_GE:
            case TAC_EQ:
            case TAC_NE:
                fprintf(file, "%s = %s %s %s\n", curr->result, curr->arg1,
                       getOpName(curr->op), curr->arg2);
                break;
            case TAC_NEG:
                fprintf(file, "%s = -%s\n", curr->result, curr->arg1);
                break;
            case TAC_ASSIGN:
                fprintf(file, "%s = %s\n", curr->result, curr->arg1);
                break;
            case TAC_PRINT:
                fprintf(file, "PRINT %s\n", curr->arg1);
                break;
            case TAC_ARG:
                fprintf(file, "ARG %s\n", curr->arg1);
                break;
            case TAC_CALL:
                fprintf(file, "%s = CALL %s, %s\n", curr->result, curr->arg1, curr->arg2);
                break;
            case TAC_RETURN:
                if (curr->arg1) {
                    fprintf(file, "RETURN %s\n", curr->arg1);
                } else {
                    fprintf(file, "RETURN\n");
                }
                break;
            case TAC_LABEL:
                fprintf(file, "%s:\n", curr->result);
                break;
            case TAC_GOTO:
                fprintf(file, "GOTO %s\n", curr->arg1);
                break;
            case TAC_IF_FALSE:
                fprintf(file, "IF_FALSE %s GOTO %s\n", curr->arg1, curr->arg2);
                break;
            case TAC_IF_TRUE:
                fprintf(file, "IF_TRUE %s GOTO %s\n", curr->arg1, curr->arg2);
                break;
            case TAC_ARRAY_DECL:
                fprintf(file, "ARRAY_DECL %s[%s]\n", curr->result, curr->arg1);
                break;
            case TAC_ARRAY_LOAD:
                fprintf(file, "%s = %s[%s]\n", curr->result, curr->arg1, curr->arg2);
                break;
            case TAC_ARRAY_STORE:
                fprintf(file, "%s[%s] = %s\n", curr->arg1, curr->arg2, curr->result);
                break;
            default:
                fprintf(file, "UNKNOWN\n");
                break;
        }
        curr = curr->next;
    }

    fclose(file);
    printf("✓ Optimized TAC saved to: %s\n", filename);
}
