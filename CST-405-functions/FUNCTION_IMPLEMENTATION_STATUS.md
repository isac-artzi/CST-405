# Function Support Implementation Status

## Overview
This document tracks the implementation of function support in the compiler. Function support is a **major feature** requiring changes across all compiler phases.

---

## ✅ COMPLETED PHASES

### 1. Lexical Analysis (scanner.l) ✅
**Status:** COMPLETE

**New Tokens Added:**
- Keywords: `return`, `if`, `else`, `while`
- Operators: `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `==`, `!=`
- Delimiters: `{`, `}`, `,`

**Testing:** ✅ Lex compiles successfully

---

### 2. Syntax Analysis (parser.y) ✅
**Status:** COMPLETE

**New Grammar Rules:**
- Function definitions: `int name(params) { body }`
- Function calls: `name(args)` (as statement and expression)
- Parameters: `int a, int b, int c`
- Return statements: `return expr;` and `return;`
- If statements: `if (cond) stmt` and `if (cond) stmt else stmt`
- While loops: `while (cond) stmt`
- Block statements: `{ stmt_list }`
- Enhanced expressions: arithmetic (`+`, `-`, `*`, `/`), comparison (`<`, `>`, `<=`, `>=`, `==`, `!=`), unary minus

**Testing:** ✅ Parser compiles with 1 shift/reduce conflict (expected for if-else)

---

### 3. Abstract Syntax Tree (ast.h/ast.c) ✅
**Status:** COMPLETE

**New Node Types:**
```c
NODE_FUNC_DEF     // Function definition
NODE_PARAM        // Parameter
NODE_PARAM_LIST   // Parameter list
NODE_FUNC_CALL    // Function call
NODE_ARG_LIST     // Argument list
NODE_RETURN       // Return statement
NODE_IF           // If statement
NODE_WHILE        // While loop
NODE_BLOCK        // Block statement
```

**New AST Creation Functions:**
- `createFuncDef(name, params, body)`
- `createParam(name)`
- `createParamList(param, next)`
- `createFuncCall(name, args)`
- `createArgList(expr, next)`
- `createReturn(expr)`
- `createIf(condition, then_stmt, else_stmt)`
- `createWhile(condition, body)`
- `createBlock(stmt_list)`

**Testing:** ✅ Successfully parses function code and builds AST
```
test_func_simple.c successfully parses and displays:
- Function definitions with parameters
- Function calls as expressions
- Return statements
- Block statements
```

---

## ⚠️ IN PROGRESS / TODO

### 4. Semantic Analysis (semantic.h/semantic.c) ⚠️
**Status:** NEEDS MAJOR UPDATES

**Required Additions:**

#### Function Symbol Table
```c
typedef struct {
    char* name;           // Function name
    int paramCount;       // Number of parameters
    char** paramNames;    // Parameter names
    int isDefined;        // Has body been seen?
    int isDeclared;       // Has prototype been seen?
} FunctionSymbol;
```

#### Checks Needed:
1. **Function Declaration Tracking**
   - Record function definitions
   - Track parameter names and counts
   - Detect duplicate function definitions

2. **Function Call Validation**
   - Verify function exists before calling
   - Check argument count matches parameter count
   - Built-in function handling (`print`)

3. **Return Statement Validation**
   - Ensure returns are inside functions
   - Check return value exists for int functions
   - Allow empty return for void (future feature)

4. **Scope Management**
   - Function parameters are local variables
   - Local variables shadow globals
   - Variables declared in blocks have block scope

5. **Variable Usage Validation**
   - Check variables declared before use (per scope)
   - Prevent use of variables from other function scopes

**Implementation Priority:** HIGH - Blocks TAC generation

---

### 5. Three-Address Code (tac.h/tac.c) ⚠️
**Status:** NEEDS MAJOR UPDATES

**New TAC Operations Needed:**

```c
typedef enum {
    // Existing
    TAC_ADD, TAC_ASSIGN, TAC_PRINT, TAC_DECL,

    // New for functions
    TAC_SUB,         // Subtraction
    TAC_MUL,         // Multiplication
    TAC_DIV,         // Division
    TAC_LT,          // Less than
    TAC_GT,          // Greater than
    TAC_LE,          // Less than or equal
    TAC_GE,          // Greater than or equal
    TAC_EQ,          // Equal
    TAC_NE,          // Not equal
    TAC_NEG,         // Unary negation

    TAC_LABEL,       // Label: L1:
    TAC_GOTO,        // Unconditional jump: goto L1
    TAC_IF_FALSE,    // Conditional jump: if_false expr goto L1
    TAC_IF_TRUE,     // Conditional jump: if_true expr goto L1

    TAC_FUNC_BEGIN,  // Mark start of function
    TAC_FUNC_END,    // Mark end of function
    TAC_PARAM,       // Function parameter declaration
    TAC_ARG,         // Push argument for call
    TAC_CALL,        // Call function: result = call func
    TAC_RETURN       // Return from function
} TACOp;
```

**Key Challenges:**

1. **Label Generation**
   - Generate unique labels for if/else/while
   - Control flow graph management

2. **Function Calls**
   - TAC for pushing arguments
   - TAC for calling function
   - TAC for retrieving return value

3. **Function Definitions**
   - Mark function boundaries
   - Handle parameter declarations
   - Manage local variable scope

4. **Control Flow**
   - If-else requires labels and conditional jumps
   - While loops require labels and backward jumps
   - Return statements exit function

**Example TAC for Function:**
```
FUNC_BEGIN add
PARAM a
PARAM b
DECL result
result = a + b
RETURN result
FUNC_END add

FUNC_BEGIN main
DECL x
DECL y
DECL z
x = 5
y = 10
ARG x
ARG y
z = CALL add
PRINT z
RETURN 0
FUNC_END main
```

**Implementation Priority:** CRITICAL - Required for code generation

---

### 6. Code Generation (codegen.h/codegen.c) ⚠️
**Status:** NEEDS MAJOR UPDATES

**MIPS Calling Convention Support:**

#### Stack Frame Layout:
```
High Memory
+------------------+
| Argument N       |  Caller's frame
| ...              |
| Argument 1       |
+------------------+
| Return Address   |  $ra
| Saved $fp        |  $fp (frame pointer)
+------------------+ <-- Current $fp
| Local Variable 1 |
| Local Variable 2 |
| ...              |
+------------------+
| Temporary Space  |
+------------------+ <-- Current $sp
Low Memory
```

#### Required MIPS Instructions:

**Function Prologue:**
```mips
function_name:
    # Save frame pointer
    addi $sp, $sp, -4
    sw $fp, 0($sp)

    # Set new frame pointer
    move $fp, $sp

    # Allocate space for locals
    addi $sp, $sp, -<local_size>
```

**Function Epilogue:**
```mips
    # Restore stack pointer
    move $sp, $fp

    # Restore frame pointer
    lw $fp, 0($sp)
    addi $sp, $sp, 4

    # Return
    jr $ra
```

**Function Call:**
```mips
    # Push arguments (right to left)
    addi $sp, $sp, -4
    sw <arg>, 0($sp)

    # Call function
    jal function_name

    # Clean up arguments
    addi $sp, $sp, <arg_count * 4>

    # Result in $v0
    move $t0, $v0
```

**Key Challenges:**

1. **Register Management**
   - Save/restore caller-saved registers ($t0-$t9)
   - Save/restore callee-saved registers ($s0-$s7)
   - Use $v0 for return values
   - Use $ra for return address

2. **Parameter Access**
   - Parameters accessed via frame pointer offset
   - First param at $fp + 8, second at $fp + 12, etc.

3. **Local Variables**
   - Locals accessed via frame pointer negative offset
   - Must track offset for each variable

4. **Control Flow**
   - Branch instructions for if/while
   - Label generation in assembly

**Implementation Priority:** CRITICAL - Final step

---

## 🧪 TESTING

### Test Files Created:
- ✅ `test_func_simple.c` - Basic function with parameters, call, return

### Test Files Needed:
- `test_func_recursive.c` - Recursive function (factorial, fibonacci)
- `test_func_multiple.c` - Multiple function definitions
- `test_func_control_flow.c` - If/else and while in functions
- `test_func_nested_calls.c` - Function calling other functions
- `test_func_no_params.c` - Functions without parameters
- `test_func_expressions.c` - Complex expressions with all operators

---

## 📋 IMPLEMENTATION CHECKLIST

### Semantic Analysis
- [ ] Add function symbol table
- [ ] Implement function registration
- [ ] Validate function calls (existence, argument count)
- [ ] Implement scope management (function scope, block scope)
- [ ] Validate variable declarations per scope
- [ ] Validate return statements
- [ ] Handle built-in functions (print)

### TAC Generation
- [ ] Add new TAC operation types
- [ ] Implement label generation
- [ ] Generate TAC for function definitions
- [ ] Generate TAC for function calls
- [ ] Generate TAC for return statements
- [ ] Generate TAC for if/else (labels, conditional jumps)
- [ ] Generate TAC for while loops (labels, jumps)
- [ ] Generate TAC for comparison operators
- [ ] Generate TAC for arithmetic operators (-, *, /)
- [ ] Update TAC optimization for new operations

### Code Generation
- [ ] Implement MIPS calling convention
- [ ] Generate function prologue
- [ ] Generate function epilogue
- [ ] Generate function calls (jal, argument passing)
- [ ] Implement frame pointer management
- [ ] Generate code for parameters
- [ ] Generate code for return statements
- [ ] Generate code for control flow (branches, labels)
- [ ] Generate code for comparison operators
- [ ] Generate code for arithmetic operators (-, *, /)
- [ ] Update register allocation for function calls

---

## 📝 NOTES

### Current Limitations:
1. Only `int` type supported (no void, no other types)
2. No arrays
3. No pointers
4. No structs
5. No global variable initialization
6. No function prototypes (functions must be defined before use)
7. No recursion limit checking

### Design Decisions:
1. All functions return `int` (main returns 0)
2. Parameters are pass-by-value only
3. No function overloading
4. `print` is a built-in statement, not a function
5. Simple one-pass compilation (no forward declarations)

---

## 🎯 NEXT STEPS

**Immediate Priority:**
1. Update semantic analyzer to track functions and validate calls
2. Extend TAC for function operations and control flow
3. Implement MIPS function calling convention in code generator
4. Test with simple function examples

**Estimated Effort:**
- Semantic Analysis: 2-4 hours
- TAC Generation: 4-6 hours
- Code Generation: 4-6 hours
- Testing & Debugging: 2-4 hours

**Total: 12-20 hours of implementation work**

---

## 📚 RESOURCES

### MIPS Calling Convention:
- [MIPS Assembly Programming Guide](https://courses.cs.washington.edu/courses/cse378/10sp/lectures/lec05.pdf)
- Registers: $a0-$a3 (arguments), $v0-$v1 (return), $ra (return address), $fp (frame pointer)

### Compiler Design:
- Dragon Book (Aho, Lam, Sethi, Ullman) - Chapter 7: Run-Time Environments
- Function call TAC intermediate representation
- Activation records and stack frames

---

**Last Updated:** 2026-01-22
**Status:** Parser and AST complete, semantic/TAC/codegen in progress
