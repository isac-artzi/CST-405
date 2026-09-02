# Solution Guide: Implementing WHILE Loops

**For Instructors Only**

This document contains complete solutions for the WHILE loop class activity.

---

## Part 1: Lexical Analysis - SOLUTION

**File:** `scanner.l`

```c
/* Keywords */
"int"       { return INT; }
"if"        { return IF; }
"else"      { return ELSE; }
"while"     { return WHILE; }    // Solution: Add this line
"return"    { return RETURN; }
"print"     { return PRINT; }
```

**Key Points:**
- Must come BEFORE the identifier rule
- Case-sensitive (lowercase 'while')
- Returns the WHILE token defined in parser

---

## Part 2: Syntax Analysis - SOLUTION

**File:** `parser.y`

### Token Declaration:
```c
%token INT IF ELSE WHILE RETURN PRINT
```

### Grammar Rule:
```c
stmt:
      /* ... existing rules ... */
    | WHILE '(' expr ')' stmt
        {
            $$ = createWhileNode($3, $5);
        }
    ;
```

**Explanation:**
- `$3` is the expression (condition) between parentheses
- `$5` is the statement (body) after the closing parenthesis
- The parentheses and WHILE keyword don't need to be captured

**Common Student Errors:**
- Using `$1` and `$2` (forgetting to count terminals)
- Not handling compound statements (blocks)
- Mixing up condition and body order

---

## Part 3: AST Representation - SOLUTION

**File:** `ast.h`

### Node Type Enum:
```c
typedef enum {
    NODE_NUM,
    NODE_VAR,
    NODE_BINOP,
    NODE_ASSIGN,
    NODE_PRINT,
    NODE_IF,
    NODE_WHILE,        // Add this
    NODE_RETURN,
    NODE_BLOCK,
    NODE_STMT_LIST,
    // ... other types
} NodeType;
```

### AST Node Structure:
```c
typedef struct ASTNode {
    NodeType type;
    union {
        // ... other node types ...

        struct {
            struct ASTNode* condition;
            struct ASTNode* body;
        } while_stmt;

        // ... other node types ...
    } data;
} ASTNode;
```

**File:** `ast.c`

### Creation Function:
```c
ASTNode* createWhileNode(ASTNode* condition, ASTNode* body) {
    ASTNode* node = malloc(sizeof(ASTNode));
    if (!node) {
        fprintf(stderr, "Error: Memory allocation failed for WHILE node\n");
        exit(1);
    }

    node->type = NODE_WHILE;
    node->data.while_stmt.condition = condition;
    node->data.while_stmt.body = body;

    return node;
}
```

**Important Notes:**
- Always check malloc() return value in production code
- Condition and body can be NULL (though parser should prevent this)
- Memory is freed when the entire AST is freed

### Print Function:
```c
void printAST(ASTNode* node, int depth) {
    if (!node) return;

    char indent[100];
    for (int i = 0; i < depth * 2; i++) {
        indent[i] = ' ';
    }
    indent[depth * 2] = '\0';

    switch(node->type) {
        // ... other cases ...

        case NODE_WHILE:
            printf("%sWHILE\n", indent);
            printf("%s  CONDITION:\n", indent);
            printAST(node->data.while_stmt.condition, depth + 2);
            printf("%s  BODY:\n", indent);
            printAST(node->data.while_stmt.body, depth + 2);
            break;

        // ... other cases ...
    }
}
```

---

## Part 4: TAC Generation - SOLUTION

**File:** `tac.c`

### Complete Implementation:
```c
case NODE_WHILE: {
    /* Generate unique labels for loop control */
    char* labelStart = newLabel();  // e.g., "L0"
    char* labelEnd = newLabel();    // e.g., "L1"

    /* Step 1: Emit start label - this is the loop entry point */
    appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelStart));

    /* Step 2: Evaluate condition expression */
    char* cond = generateTACExpr(node->data.while_stmt.condition);

    /* Step 3: Conditional jump - exit loop if condition is false */
    appendTAC(createTAC(TAC_IF_FALSE, cond, labelEnd, NULL));
    freeTemp(cond);  // Free the temporary holding condition result

    /* Step 4: Generate code for loop body */
    generateTACStmt(node->data.while_stmt.body);

    /* Step 5: Unconditional jump back to loop start */
    appendTAC(createTAC(TAC_GOTO, labelStart, NULL, NULL));

    /* Step 6: Emit end label - this is the loop exit point */
    appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelEnd));

    break;
}
```

**Detailed Explanation:**

1. **Label Generation:**
   - `newLabel()` generates unique labels (L0, L1, L2, ...)
   - Each while loop needs two labels: start and end
   - Labels must be unique to avoid conflicts with nested loops

2. **Loop Structure:**
   ```
   L_start:                    ← Loop begins here
       evaluate condition      ← Check if we should continue
       if_false goto L_end     ← Exit if condition is false
       [body code]             ← Execute loop body
       goto L_start            ← Jump back to start
   L_end:                      ← Loop exits here
   ```

3. **Why IF_FALSE instead of IF_TRUE?**
   - We want to exit when condition is FALSE
   - If condition is TRUE, we fall through to execute the body
   - More efficient than jumping when true

4. **Memory Management:**
   - `freeTemp(cond)` releases the temporary variable
   - Important for register allocation in later stages

**Common Student Errors:**

❌ **Forgetting goto back to start:**
```c
// This only executes once!
L0:
    if_false cond goto L1
    [body]
L1:  // Missing: goto L0
```

❌ **Using IF_TRUE instead of IF_FALSE:**
```c
// This inverts the logic!
if_true cond goto L1  // Wrong: jumps when should continue
[body]
goto L0
L1:
```

❌ **Wrong label order:**
```c
// End label comes before start!
L1:  // Wrong position
L0:
    if_false cond goto L1
    [body]
    goto L0
```

---

## Part 5: Expected TAC Output

### Test Case 1 (Simple Counter):
```c
int i;
i = 1;
while (i <= 5) {
    print(i);
    i = i + 1;
}
```

**Expected TAC:**
```
DECL i
i = 1

L0:                         # Loop start
    t0 = i <= 5            # Evaluate: i <= 5
    IF_FALSE t0 GOTO L1    # Exit if i > 5
    PRINT i                # Print current value
    t1 = i + 1             # Calculate i + 1
    i = t1                 # Update i
    GOTO L0                # Loop back to start
L1:                        # Loop end
```

### Test Case 2 (Sum Accumulation):
```c
int sum;
int i;
sum = 0;
i = 1;
while (i <= 10) {
    sum = sum + i;
    i = i + 1;
}
print(sum);
```

**Expected TAC:**
```
DECL sum
DECL i
sum = 0
i = 1

L0:                         # Loop start
    t0 = i <= 10           # Check condition
    IF_FALSE t0 GOTO L1    # Exit when i > 10
    t1 = sum + i           # Calculate sum + i
    sum = t1               # Update sum
    t2 = i + 1             # Calculate i + 1
    i = t2                 # Update i
    GOTO L0                # Loop back
L1:                        # Loop end

PRINT sum                  # Output final sum
```

### Test Case 3 (Nested Loops):
```c
int i;
int j;
i = 1;
while (i <= 3) {
    j = 1;
    while (j <= 3) {
        print(i * j);
        j = j + 1;
    }
    i = i + 1;
}
```

**Expected TAC:**
```
DECL i
DECL j
i = 1

L0:                         # Outer loop start
    t0 = i <= 3
    IF_FALSE t0 GOTO L1    # Exit outer loop
    j = 1

    L2:                     # Inner loop start (nested)
        t1 = j <= 3
        IF_FALSE t1 GOTO L3 # Exit inner loop
        t2 = i * j
        PRINT t2
        t3 = j + 1
        j = t3
        GOTO L2             # Inner loop back
    L3:                     # Inner loop end

    t4 = i + 1
    i = t4
    GOTO L0                # Outer loop back
L1:                        # Outer loop end
```

**Note on Nested Loops:**
- Each loop gets its own unique pair of labels
- Inner loop labels (L2, L3) are different from outer loop (L0, L1)
- `newLabel()` ensures uniqueness automatically

---

## Part 6: Code Generation - SOLUTION

**File:** `codegen.c`

### TAC_LABEL:
```c
case TAC_LABEL:
    printf("[TAC %3d] LABEL: %s\n", tacLineNum, curr->result);
    fprintf(output, "%s:                    # Label\n", curr->result);
    break;
```

### TAC_GOTO:
```c
case TAC_GOTO:
    printf("[TAC %3d] GOTO: %s\n", tacLineNum, curr->arg1);
    fprintf(output, "    j %s              # Unconditional jump\n", curr->arg1);
    break;
```

### TAC_IF_FALSE:
```c
case TAC_IF_FALSE: {
    printf("[TAC %3d] IF_FALSE: if !%s goto %s\n", tacLineNum, curr->arg1, curr->arg2);

    // Load condition value into register
    int condReg;
    if (isConstant(curr->arg1)) {
        condReg = allocReg("const_cond");
        fprintf(output, "    li $t%d, %s         # Load condition\n", condReg, curr->arg1);
    } else {
        condReg = findVarReg(curr->arg1);
        if (condReg == -1) {
            // Not in register, load from memory
            if (isTACTemp(curr->arg1)) {
                fprintf(stderr, "Error: TAC temporary '%s' not in register\n", curr->arg1);
                exit(1);
            }
            int offset = getVarOffset(curr->arg1);
            if (offset == -1) {
                fprintf(stderr, "Error: Condition variable '%s' not found\n", curr->arg1);
                exit(1);
            }
            condReg = allocReg(curr->arg1);
            fprintf(output, "    lw $t%d, %d($sp)     # Load condition\n", condReg, offset);
        }
    }

    // Branch if zero (false)
    fprintf(output, "    beqz $t%d, %s       # Jump if false\n", condReg, curr->arg2);

    freeReg(condReg);
    break;
}
```

**Generated MIPS Example:**
```assembly
main_start:
    # i = 1
    li $t0, 1
    sw $t0, 0($sp)

L0:                         # Loop start
    lw $t0, 0($sp)          # Load i
    li $t1, 5               # Load constant 5
    sle $t2, $t0, $t1       # i <= 5 ? 1 : 0
    beqz $t2, L1            # Branch to L1 if false

    # Print i
    lw $t0, 0($sp)
    move $a0, $t0
    li $v0, 1
    syscall

    # i = i + 1
    lw $t0, 0($sp)
    li $t1, 1
    add $t2, $t0, $t1
    sw $t2, 0($sp)

    j L0                    # Jump back to start

L1:                         # Loop end
```

---

## Assessment & Grading Notes

### Full Credit (100/100):
- ✅ WHILE token recognized in lexer
- ✅ Grammar rule correctly parses while statements
- ✅ AST node properly created with condition and body
- ✅ TAC generates correct control flow (labels + jumps)
- ✅ All three test cases compile and run correctly
- ✅ Code is clean and commented

### Partial Credit Scenarios:

**80-90 points:**
- Minor syntax errors that are easily fixable
- Missing comments or documentation
- Test cases work but have minor output formatting issues

**60-80 points:**
- TAC structure correct but missing free or label management
- Nested loops don't work correctly
- One or two test cases fail

**40-60 points:**
- Basic structure present but significant logical errors
- Only simple test case works
- Missing key components (like goto back to start)

**Below 40 points:**
- Incomplete implementation
- Major conceptual misunderstandings
- Code doesn't compile

### Bonus Points:

**DO-WHILE (+5 points):**
```c
case NODE_DO_WHILE: {
    char* labelStart = newLabel();
    char* labelEnd = newLabel();

    appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelStart));

    // Body comes FIRST (always executes once)
    generateTACStmt(node->data.do_while_stmt.body);

    // THEN check condition
    char* cond = generateTACExpr(node->data.do_while_stmt.condition);
    appendTAC(createTAC(TAC_IF_TRUE, cond, labelStart, NULL));  // Note: IF_TRUE

    appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelEnd));
    break;
}
```

**FOR Loop (+5 points):**
```c
// Desugar: for(init; cond; incr) body
// Into: init; while(cond) { body; incr; }
```

**BREAK Statement (+10 points):**
- Requires maintaining a stack of loop end labels
- Jump to current loop's end label

---

## Discussion Questions for Class

1. **Why do we need labels in TAC for while loops?**
   - Answer: Labels provide jump targets for control flow

2. **What's the difference between IF_FALSE and IF_TRUE?**
   - Answer: IF_FALSE jumps when condition is 0, IF_TRUE jumps when non-zero

3. **Why does the goto come before the end label?**
   - Answer: We need to jump back before exiting; if goto came after, it would never execute

4. **How does the compiler handle nested loops?**
   - Answer: Each loop gets unique labels via newLabel()

5. **What happens if we forget to increment the loop variable?**
   - Answer: Infinite loop! Condition never becomes false

6. **Can a while loop body be empty?**
   - Answer: Yes, syntactically valid but produces no body code

7. **How would you optimize `while(1)`?**
   - Answer: Remove condition check, just loop forever (until break)

---

## Extended Activities

### Activity 1: Loop Optimization
Have students identify and optimize these patterns:
- `while(0)` → Remove entire loop (dead code)
- `while(1)` → Remove condition check (infinite loop)
- Loop invariant code motion

### Activity 2: Control Flow Graphs
Draw CFGs for:
- Simple while loop
- Nested while loops
- While loop with early return

### Activity 3: Comparison with Other Loops
Compare TAC for:
- while loop
- do-while loop
- for loop
- Show they're all similar!

---

## Common Student Questions

**Q: Why does my nested loop use 4 labels instead of 2?**
A: Each loop needs its own start and end label. 2 loops = 4 labels.

**Q: My loop executes one extra time. Why?**
A: Check your condition operator. `i < 5` vs `i <= 5` makes a difference!

**Q: I get "undefined label" errors in MIPS.**
A: Make sure you're emitting TAC_LABEL instructions for both start and end labels.

**Q: Can I use numbers instead of label names?**
A: No! Numbers are constants. Use L0, L1, etc. as label identifiers.

**Q: How do I debug TAC generation?**
A: Print the TAC before and after each step. Use `printTAC()` liberally!

---

## Additional Resources

- **Visualization Tool:** Use online CFG tools to visualize control flow
- **MIPS Simulator:** MARS or SPIM for testing generated assembly
- **Sample Implementation:** Available in course repository

---

**End of Solution Guide**
