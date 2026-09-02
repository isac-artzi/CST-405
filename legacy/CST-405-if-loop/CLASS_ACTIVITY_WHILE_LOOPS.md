# Class Activity: Implementing WHILE Loops in a Compiler

**Course:** CST-405 Compiler Design
**Activity Type:** Hands-on Implementation
**Estimated Time:** 90-120 minutes
**Difficulty:** Intermediate

---

## Learning Objectives

By the end of this activity, students will be able to:
1. ✓ Extend a lexer to recognize loop keywords
2. ✓ Write grammar rules for while loop syntax
3. ✓ Create AST nodes to represent while loops
4. ✓ Generate Three-Address Code (TAC) for loops with proper control flow
5. ✓ Understand how loops are translated to assembly using labels and jumps

---

## Background

A **while loop** is a control flow statement that repeatedly executes code based on a condition:

```c
while (condition) {
    // body
}
```

**Control Flow Structure:**
```
START:
    evaluate condition
    if condition is false, jump to END
    execute body
    jump to START
END:
```

This requires:
- **Labels** for jump targets
- **Conditional jumps** (branch if false)
- **Unconditional jumps** (goto)

---

## Prerequisites

Students should have:
- ✓ Basic understanding of lexical analysis (Flex)
- ✓ Basic understanding of syntax analysis (Bison)
- ✓ Familiarity with AST (Abstract Syntax Trees)
- ✓ Understanding of Three-Address Code (TAC)
- ✓ Completed IF statement implementation (or similar)

---

## Part 1: Lexical Analysis (10 minutes)

### Task 1.1: Add WHILE Token

**File:** `scanner.l`

Add the `while` keyword to your lexer so it's recognized as a token.

**Instructions:**
1. Open `scanner.l`
2. Find the keyword section (where `if`, `else`, `return`, etc. are defined)
3. Add a rule for `while`

**Hint:**
```c
"if"        { return IF; }
"else"      { return ELSE; }
/* Add your WHILE token here */
```

**Question for Discussion:**
- Why do we need to recognize `while` as a separate token instead of treating it as a regular identifier?

---

## Part 2: Syntax Analysis (20 minutes)

### Task 2.1: Declare WHILE Token in Parser

**File:** `parser.y`

Add the token declaration in the `%token` section:

```c
%token IF ELSE WHILE RETURN PRINT
```

### Task 2.2: Write Grammar Rule for While Statement

Add a new grammar rule for while loops. A while loop has:
- The keyword `while`
- A condition in parentheses `(condition)`
- A statement body (could be a single statement or a block)

**Starter Code:**
```c
stmt:
      /* ... existing rules ... */
    | WHILE '(' expr ')' stmt
        {
            /* TODO: Create AST node for while loop */
            /* Hint: Use createWhileNode(condition, body) */
            $$ = NULL;  // Replace this!
        }
    ;
```

**Your Task:**
- Complete the action code to create a while loop AST node
- The condition is `$3` (third component)
- The body is `$5` (fifth component)

---

## Part 3: AST Representation (20 minutes)

### Task 3.1: Define AST Node Structure

**File:** `ast.h`

Add a new node type and structure for while loops:

```c
typedef enum {
    NODE_NUM,
    NODE_VAR,
    NODE_BINOP,
    NODE_ASSIGN,
    NODE_PRINT,
    NODE_IF,
    NODE_WHILE,     // Add this
    // ... other types
} NodeType;
```

Add the while loop structure to your AST node union:

```c
struct {
    ASTNode* condition;
    ASTNode* body;
} while_stmt;
```

### Task 3.2: Implement AST Creation Function

**File:** `ast.c`

Implement the function to create a while loop node:

```c
ASTNode* createWhileNode(ASTNode* condition, ASTNode* body) {
    // TODO: Allocate memory for new node
    // TODO: Set node type to NODE_WHILE
    // TODO: Set condition and body
    // TODO: Return the node

    return NULL;  // Replace this!
}
```

**Test Your Understanding:**
- What happens if condition is NULL?
- Should you validate inputs or trust the parser?

### Task 3.3: Add While Loop Printing

Update `printAST()` to handle while loops:

```c
case NODE_WHILE:
    printf("WHILE\n");
    printf("%sCONDITION:\n", indent);
    printAST(node->data.while_stmt.condition, depth + 1);
    printf("%sBODY:\n", indent);
    printAST(node->data.while_stmt.body, depth + 1);
    break;
```

---

## Part 4: Three-Address Code Generation (30 minutes)

### Task 4.1: Understand the TAC Pattern

A while loop translates to:

```
L_start:                    # Loop start label
    t0 = evaluate(condition)
    if_false t0 goto L_end  # Exit if condition is false
    [body code]             # Execute loop body
    goto L_start            # Jump back to start
L_end:                      # Loop exit label
```

### Task 4.2: Implement TAC Generation

**File:** `tac.c`

Add a case for `NODE_WHILE` in your TAC generation function:

```c
case NODE_WHILE: {
    /* TODO: Generate two unique labels */
    char* labelStart = newLabel();  // e.g., "L0"
    char* labelEnd = newLabel();    // e.g., "L1"

    /* Step 1: Emit start label */
    // appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelStart));

    /* Step 2: Evaluate condition */
    // char* cond = generateTACExpr(node->data.while_stmt.condition);

    /* Step 3: Jump to end if condition is false */
    // appendTAC(createTAC(TAC_IF_FALSE, cond, labelEnd, NULL));

    /* Step 4: Generate body code */
    // generateTACStmt(node->data.while_stmt.body);

    /* Step 5: Jump back to start */
    // appendTAC(createTAC(TAC_GOTO, labelStart, NULL, NULL));

    /* Step 6: Emit end label */
    // appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelEnd));

    break;
}
```

**Your Task:**
- Uncomment and complete the code above
- Make sure you understand what each step does
- Think about why the order matters!

---

## Part 5: Testing (20 minutes)

### Test Case 1: Simple Counter Loop

Create a file `test_while_simple.c`:

```c
int main() {
    int i;
    i = 1;

    while (i <= 5) {
        print(i);
        i = i + 1;
    }

    return 0;
}
```

**Expected Output:** (numbers 1 through 5)
```
1
2
3
4
5
```

**Expected TAC Structure:**
```
L0:                         # Loop start
    t0 = i <= 5            # Evaluate condition
    if_false t0 goto L1    # Exit if false
    print i                # Body
    t1 = i + 1
    i = t1
    goto L0                # Loop back
L1:                        # Loop end
```

### Test Case 2: Sum Accumulation

Create `test_while_sum.c`:

```c
int main() {
    int sum;
    int i;

    sum = 0;
    i = 1;

    while (i <= 10) {
        sum = sum + i;
        i = i + 1;
    }

    print(sum);  // Should print 55
    return 0;
}
```

**Expected Output:**
```
55
```

### Test Case 3: Nested While Loops

Create `test_while_nested.c`:

```c
int main() {
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

    return 0;
}
```

**Expected Output:** (multiplication table)
```
1
2
3
2
4
6
3
6
9
```

---

## Part 6: Code Generation (Optional - Advanced)

### Task 6.1: Generate MIPS Assembly

**File:** `codegen.c`

Translate TAC to MIPS assembly. The key instructions you'll need:

```assembly
L0:                         # Label
    lw $t0, i               # Load i
    li $t1, 5               # Load constant 5
    sle $t2, $t0, $t1       # Set if less or equal
    beqz $t2, L1            # Branch if equal to zero (false)
    # ... body code ...
    j L0                    # Jump to L0
L1:
```

**Your Task:**
- Implement the case for `TAC_LABEL`
- Implement the case for `TAC_GOTO`
- Implement the case for `TAC_IF_FALSE`

---

## Common Mistakes to Avoid

1. **Forgetting the jump back to start**
   - Without `goto L_start`, the loop only executes once!

2. **Wrong jump condition**
   - Use `IF_FALSE` to exit when condition fails
   - Don't use `IF_TRUE` (that's for different logic)

3. **Label confusion**
   - Make sure each label is unique
   - Use `newLabel()` to generate labels automatically

4. **Infinite loops in simple tests**
   - Check that your loop variable is actually incremented
   - Verify the condition can become false

5. **Not freeing temporaries**
   - Remember to free temporary registers after condition evaluation

---

## Bonus Challenges

### Challenge 1: DO-WHILE Loop
Implement a do-while loop that executes the body at least once:
```c
do {
    // body
} while (condition);
```

**Hint:** The condition check comes AFTER the body!

### Challenge 2: FOR Loop
Implement a for loop:
```c
for (init; condition; increment) {
    // body
}
```

**Hint:** This is syntactic sugar for a while loop!

### Challenge 3: BREAK Statement
Add support for breaking out of loops early:
```c
while (1) {
    if (i > 10) {
        break;
    }
    i = i + 1;
}
```

**Hint:** You'll need to track the current loop's end label!

---

## Deliverables

Submit the following:

1. **Modified source files:**
   - `scanner.l`
   - `parser.y`
   - `ast.h` and `ast.c`
   - `tac.c`

2. **Test files:**
   - All three test cases (simple, sum, nested)
   - Output showing successful compilation

3. **TAC output:**
   - Show the generated TAC for at least one test case
   - Annotate it to explain the control flow

4. **Reflection (1 paragraph each):**
   - What was the most challenging part?
   - How do while loops differ from if statements in code generation?
   - What did you learn about control flow in compilers?

---

## Grading Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| Lexer (scanner.l) | 10 | WHILE token correctly recognized |
| Parser (parser.y) | 15 | Grammar rule correctly implemented |
| AST | 20 | Node structure and creation function work |
| TAC Generation | 35 | Correct TAC with proper labels and jumps |
| Testing | 15 | All test cases pass and produce correct output |
| Code Quality | 5 | Clean, commented, well-structured code |
| **Total** | **100** | |

**Bonus:** +10 points for completing one or more bonus challenges

---

## Resources

- **Dragon Book:** Section 8.4 (Control Flow)
- **Lecture Slides:** Week 7 - Intermediate Code Generation
- **Office Hours:** Tuesday/Thursday 2-4 PM

---

## Submission Instructions

1. Create a directory: `lastname_firstname_while_loops/`
2. Include all modified source files
3. Include all test files
4. Include a `README.txt` with:
   - Compilation instructions
   - How to run tests
   - Any known issues
5. Zip the directory and submit to Canvas

**Due Date:** [To be filled in by instructor]

---

## Tips for Success

- **Start early!** Don't wait until the last minute
- **Test incrementally** - compile after each change
- **Use print statements** to debug TAC generation
- **Draw the control flow** on paper first
- **Ask questions** in class or during office hours
- **Work with a partner** (but submit individually)

Good luck! 🚀
