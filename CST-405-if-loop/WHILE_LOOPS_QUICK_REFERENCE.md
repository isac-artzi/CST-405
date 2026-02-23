# WHILE Loops Quick Reference Card

**CST-405 Compiler Design - Student Cheat Sheet**

---

## The Goal

Transform this:
```c
while (condition) {
    body;
}
```

Into this TAC:
```
L_start:
    t0 = evaluate(condition)
    if_false t0 goto L_end
    [body code]
    goto L_start
L_end:
```

---

## Step-by-Step Checklist

### ✓ Phase 1: Lexer (scanner.l)
```c
"while"     { return WHILE; }
```

### ✓ Phase 2: Parser (parser.y)
```c
%token WHILE

stmt: WHILE '(' expr ')' stmt
      { $$ = createWhileNode($3, $5); }
```

### ✓ Phase 3: AST (ast.h + ast.c)
```c
// ast.h
NODE_WHILE,
struct { ASTNode* condition; ASTNode* body; } while_stmt;

// ast.c
ASTNode* createWhileNode(ASTNode* condition, ASTNode* body) {
    ASTNode* node = malloc(sizeof(ASTNode));
    node->type = NODE_WHILE;
    node->data.while_stmt.condition = condition;
    node->data.while_stmt.body = body;
    return node;
}
```

### ✓ Phase 4: TAC Generation (tac.c)
```c
case NODE_WHILE: {
    char* labelStart = newLabel();
    char* labelEnd = newLabel();

    appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelStart));

    char* cond = generateTACExpr(node->data.while_stmt.condition);
    appendTAC(createTAC(TAC_IF_FALSE, cond, labelEnd, NULL));
    freeTemp(cond);

    generateTACStmt(node->data.while_stmt.body);

    appendTAC(createTAC(TAC_GOTO, labelStart, NULL, NULL));
    appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelEnd));
    break;
}
```

---

## Critical Components

### Labels
- **Start Label:** Where the loop begins (and jumps back to)
- **End Label:** Where the loop exits to
- Must be **unique** for each loop (nested loops!)

### Jump Instructions
- **IF_FALSE:** Exit loop when condition is false
- **GOTO:** Jump back to start of loop

### The Flow
1. **Check** condition
2. **Exit** if false (jump to end)
3. **Execute** body
4. **Loop** back (jump to start)
5. **Continue** after loop (at end label)

---

## TAC Instructions You'll Need

| Instruction | Format | Example | Purpose |
|-------------|--------|---------|---------|
| TAC_LABEL | `LABEL, NULL, NULL, labelName` | `L0:` | Mark a position |
| TAC_IF_FALSE | `IF_FALSE, cond, label, NULL` | `if_false t0 goto L1` | Conditional jump |
| TAC_GOTO | `GOTO, label, NULL, NULL` | `goto L0` | Unconditional jump |

---

## Common Mistakes

### ❌ Missing the goto back
```c
L0:
    if_false cond goto L1
    [body]
    // Missing: goto L0
L1:
```
**Result:** Loop only executes once!

### ❌ Wrong jump condition
```c
L0:
    if_true cond goto L1  // WRONG!
    [body]
    goto L0
L1:
```
**Result:** Inverted logic - exits when should continue!

### ❌ Reusing labels
```c
while (...) {
    while (...) {
        // Both loops use L0/L1
    }
}
```
**Result:** Label conflicts! Use `newLabel()` for each loop.

### ❌ Forgetting to free temps
```c
char* cond = generateTACExpr(...);
appendTAC(createTAC(TAC_IF_FALSE, cond, labelEnd, NULL));
// Missing: freeTemp(cond);
```
**Result:** Memory leaks and register pressure!

---

## Testing Your Implementation

### Minimal Test
```c
int i;
i = 1;
while (i <= 3) {
    print(i);
    i = i + 1;
}
```
**Expected:** 1, 2, 3

### Expected TAC Pattern
```
i = 1
L0:
    t0 = i <= 3
    if_false t0 goto L1
    print i
    t1 = i + 1
    i = t1
    goto L0
L1:
```

---

## Debugging Tips

### If loop never executes:
- Check condition evaluation
- Verify IF_FALSE jumps to end, not start
- Print initial values

### If loop never stops:
- Check loop variable is updated
- Verify condition can become false
- Check goto jumps to START, not end

### If compilation fails:
- Check all parentheses in parser rule
- Verify createWhileNode() is declared in ast.h
- Make sure NODE_WHILE is in enum
- Check TAC_WHILE is in switch statement

### Print TAC to debug:
```c
printTAC();  // Add this after generateTAC()
```

---

## Function Reference

### Utility Functions
```c
char* newLabel();                    // Generate unique label (L0, L1, ...)
char* newTemp();                     // Generate unique temp (t0, t1, ...)
void freeTemp(char* temp);           // Free temporary variable

TACInstr* createTAC(TACOp op, char* arg1, char* arg2, char* result);
void appendTAC(TACInstr* instr);    // Add TAC to list

char* generateTACExpr(ASTNode* expr);      // Generate TAC for expression
void generateTACStmt(ASTNode* stmt);       // Generate TAC for statement
```

### AST Functions (you implement)
```c
ASTNode* createWhileNode(ASTNode* condition, ASTNode* body);
```

---

## MIPS Reference (Advanced)

### MIPS Instructions for Loops
```assembly
L0:                         # Label
    lw $t0, offset($sp)     # Load variable
    li $t1, 5               # Load constant
    sle $t2, $t0, $t1       # Set if less or equal
    beqz $t2, L1            # Branch if equal zero (false)

    # ... body code ...

    j L0                    # Jump to L0
L1:                         # End label
```

### Key MIPS Instructions
- `beqz $reg, label` - Branch if equal to zero
- `bnez $reg, label` - Branch if not equal to zero
- `j label` - Unconditional jump

---

## Help & Resources

### Stuck? Check These:
1. ✓ Did you add WHILE to the token list?
2. ✓ Is your grammar rule in the `stmt:` section?
3. ✓ Did you include both condition AND body?
4. ✓ Are you generating TWO labels?
5. ✓ Do you have both IF_FALSE and GOTO?
6. ✓ Is the GOTO before the end label?

### Still Stuck?
- Look at how IF statements are implemented
- Draw the control flow on paper
- Print the TAC and verify structure
- Ask during office hours!

---

## Example Session

**Input:** `test_while_simple.c`
```c
int i;
i = 1;
while (i <= 5) {
    print(i);
    i = i + 1;
}
```

**Compile:**
```bash
make
./minicompiler test_while_simple.c output.s
```

**Generated TAC:**
```
DECL i
i = 1
L0:
    t0 = i <= 5
    IF_FALSE t0 GOTO L1
    PRINT i
    t1 = i + 1
    i = t1
    GOTO L0
L1:
```

**Run in MARS:**
```
Output:
1
2
3
4
5
```

---

## Pro Tips

💡 **Use descriptive labels in comments**
```c
appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelStart));  // Loop entry
```

💡 **Test incrementally**
- First: Make it compile
- Then: Check TAC structure
- Finally: Verify output

💡 **Nested loops? Draw it out!**
```
Outer_Start:
    [outer condition]
    Inner_Start:
        [inner condition]
        [inner body]
        goto Inner_Start
    Inner_End:
    [outer body]
    goto Outer_Start
Outer_End:
```

💡 **Compare with IF statements**
- IF: One direction, conditional jump, no goto back
- WHILE: Two directions, conditional jump OUT, goto back

---

**Good luck! 🚀**

*Remember: The compiler is just code. You can do this!*
