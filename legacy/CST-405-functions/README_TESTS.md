# C-Minus Compiler Test Files

This directory contains comprehensive test files for demonstrating the C-minus compiler with array support.

## Test Files

### 1. `test_complete_working.c` ✅
**Purpose:** Demonstrates all successful features of the compiler

**Features Tested:**
- ✓ Multiple global variables (3)
- ✓ Global arrays (sharedArray[10])
- ✓ Multiple functions (6 total: fillNumbers, readArray, sumFive, square, cube, main)
- ✓ Array declarations (local and global)
- ✓ Arithmetic operations with 5+ terms
- ✓ Arrays as function parameters
- ✓ Functions "returning" arrays (fill-parameter pattern)
- ✓ Array element access with constant indices
- ✓ Function calls with multiple parameters

**Compilation:**
```bash
./minicompiler test_complete_working.c output.s
# Result: COMPILATION SUCCESSFUL!
```

**Use Case:** Show students a complete, working C-minus program with arrays

---

### 2. `test_semantic_errors.c` ❌
**Purpose:** Demonstrates compiler's error detection and helpful error reporting

**Errors Included (11 total):**

| # | Line | Error Type | Description |
|---|------|------------|-------------|
| 1 | 11 | Duplicate Variable | Global variable 'globalC' declared twice |
| 2 | 14 | Invalid Array Size | Array 'zeroArray' has size 0 (must be > 0) |
| 3 | 20 | Duplicate Variable | Local variable 'x' declared twice in function |
| 4 | 23 | Undeclared Variable | Assignment to 'notDeclared' without declaration |
| 5 | 34 | Duplicate Function | Function 'square' defined twice |
| 6 | 43 | Undeclared Array | Array 'unknownArray' used without declaration |
| 7 | 46 | Undeclared Variable | Variable 'mystery' used without declaration |
| 8 | 49 | Wrong Arg Count | Function expects 2 args, got 1 |
| 9 | 52 | Wrong Arg Count | Function expects 2 args, got 3 |
| 10 | 55 | Undeclared Function | Call to 'unknownFunc' which doesn't exist |
| 11 | 58 | Undeclared Variable | Assignment to 'undeclaredVar' without declaration |

**Enhanced Error Messages Include:**
- 📍 **Precise location** (line number)
- ❌ **Clear error description** (what went wrong)
- 💡 **Helpful suggestions** (how to fix it)
- 📖 **Educational notes** (why it matters)
- ✓ **Examples** (correct usage patterns)

**Example Error Output:**
```
╔════════════════════════════════════════════════════════════╗
║ SEMANTIC ERROR - Undeclared Variable                      ║
╚════════════════════════════════════════════════════════════╝
  📍 Location: Line 46
  ❌ Error: Variable 'mystery' is used before being declared
  💡 Suggestion: Add a declaration before using this variable:
     → int mystery;  (add this before line 46)
  📖 Note: In C-minus, all variables must be declared before use
```

**Compilation:**
```bash
./minicompiler test_semantic_errors.c error_output.s
# Result: 11 errors detected with detailed explanations
```

**Use Case:** Teach students how to read and understand compiler error messages

---

## Compiler Features Demonstrated

### Array Support
- Array declarations: `int arr[10];`
- Array parameters: `int func(int arr[])`
- Array indexing: `arr[0] = value;`, `x = arr[i];`
- Multi-dimensional memory layout
- Proper MIPS code generation

### Function Support
- Multiple parameters (tested with 5 params)
- Function calls with arrays
- Return values
- Nested function calls
- Parameter passing via registers ($a0-$a3)

### Error Detection
- Comprehensive semantic analysis
- Helpful, educational error messages
- Suggestions for fixing errors
- "Customer service" oriented reporting

## For Students

Use `test_complete_working.c` to understand correct C-minus syntax and features.

Use `test_semantic_errors.c` to learn how the compiler detects and reports errors.

Compare the two files to understand the difference between valid and invalid code!
