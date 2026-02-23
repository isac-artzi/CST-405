# Minimal C Compiler - Educational Version with Functions

A fully functional compiler demonstrating all phases of compilation with extensive educational features. Now supports **functions, parameters, return values, and control flow** - making it a truly realistic compiler architecture!

## 🎯 Purpose

This compiler strips away complexity to show the **essential components** of compilation:
- **Realistic Language**: Functions, parameters, control flow - real compiler features!
- **Clear Phases**: Each compilation phase is visible and well-documented
- **Real Output**: Generates actual MIPS assembly that runs on simulators
- **Educational Focus**: Extensive comments, explanatory output, and visual tracing
- **Dual Symbol Tables**: Demonstrates separation of semantic checking vs code generation

## 📚 Language Features

Our C-like language now supports:

### ✅ Data Types
- **Integer variables**: `int x;`

### ✅ Operations
- **Arithmetic**: `+`, `-`, `*`, `/`, unary `-`
- **Comparisons**: `<`, `>`, `<=`, `>=`, `==`, `!=`
- **Assignment**: `x = expression;`

### ✅ Functions
- **Function definitions**: `int add(int a, int b) { ... }`
- **Parameters**: Pass values to functions
- **Return statements**: `return expr;`
- **Function calls**: `result = add(5, 10);`

### ✅ Control Flow
- **If statements**: `if (x < 10) { ... } else { ... }`
- **While loops**: `while (x > 0) { ... }`
- **Code blocks**: `{ statement; statement; }`

### ✅ I/O
- **Print statement**: `print(x);`

## 🔧 Compiler Architecture

### TWO SYMBOL TABLES: A Key Design Decision

This compiler uses **two separate symbol tables** for different purposes - a clean architectural separation found in many production compilers:

```
┌─────────────────────────────────────────────────────┐
│  SEMANTIC SYMBOL TABLE (semantic.c)                 │
│  Purpose: Validate program correctness              │
│  Data: Variable names + scope hierarchy             │
│  Lifetime: Created during Phase 3, then discarded   │
│                                                      │
│  typedef struct {                                   │
│      char* names[MAX_VARS];  // Just names          │
│      int count;                                     │
│  } Scope;                                           │
│                                                      │
│  static Scope scopes[MAX_SCOPE_DEPTH];              │
│  static int scopeDepth;                             │
└─────────────────────────────────────────────────────┘
                         ↓
                  (Discarded after Phase 3)
                         ↓
┌─────────────────────────────────────────────────────┐
│  CODEGEN SYMBOL TABLE (symtab.c)                    │
│  Purpose: Assign memory locations                   │
│  Data: Variable names + stack offsets               │
│  Lifetime: Created during Phase 6                   │
│                                                      │
│  typedef struct {                                   │
│      char* name;      // Variable name              │
│      int offset;      // Stack memory offset        │
│  } Symbol;                                          │
│                                                      │
│  SymbolTable symtab;  // Single flat table          │
└─────────────────────────────────────────────────────┘
```

**Why Two Tables?**

1. **Different Purposes**: Semantic checking vs memory layout
2. **Different Structures**: Nested scopes vs flat table
3. **Phase Independence**: TAC doesn't need any symbol table
4. **Clean Design**: Each phase uses only what it needs

### Complete Compilation Pipeline

```
Source Code (.c)
      ↓
┌──────────────────────────────┐
│ PHASE 1: LEXICAL ANALYSIS    │ → Tokens (INT, ID, NUM, +, =, etc.)
│      (scanner.l)             │   Now with line number tracking!
│  • Tokenizes input           │
│  • Tracks line numbers       │
└──────────────────────────────┘
      ↓
┌──────────────────────────────┐
│ PHASE 2: SYNTAX ANALYSIS     │ → Abstract Syntax Tree (AST)
│      (parser.y)              │
│  • Parses grammar rules      │
│  • Builds hierarchical AST   │
│  • Reports syntax errors     │
│    with line numbers         │
└──────────────────────────────┘
      ↓
┌──────────────────────────────┐
│ PHASE 3: SEMANTIC ANALYSIS   │ → Validation Complete
│     (semantic.c)             │
│  ┌────────────────────────┐  │
│  │ SEMANTIC SYMBOL TABLE  │  │ ← First symbol table!
│  │ • Scope-based lookup   │  │
│  │ • Function signatures  │  │
│  │ • Parameter tracking   │  │
│  │ • Variable validation  │  │
│  └────────────────────────┘  │
│  • Checks declarations       │
│  • Validates scope           │
│  • Verifies function calls   │
│  • Visual scope stack trace  │
└──────────────────────────────┘
      ↓ (Semantic table DISCARDED)
      ↓
┌──────────────────────────────┐
│ PHASE 4: TAC GENERATION      │ → Three-Address Code
│       (tac.c)                │
│  • Linearizes AST            │
│  • Generates temporaries     │
│  • Function markers          │
│  • No symbol table needed!   │
└──────────────────────────────┘
      ↓
┌──────────────────────────────┐
│ PHASE 5: OPTIMIZATION        │ → Optimized TAC
│       (tac.c)                │
│  • Constant folding          │
│  • Copy propagation          │
│  • Dead code elimination     │
└──────────────────────────────┘
      ↓
┌──────────────────────────────┐
│ PHASE 6: CODE GENERATION     │ → MIPS Assembly (.s)
│      (codegen.c)             │
│  ┌────────────────────────┐  │
│  │  CODEGEN SYMBOL TABLE  │  │ ← Second symbol table!
│  │ • Built from TAC       │  │
│  │ • Flat structure       │  │
│  │ • Memory offsets       │  │
│  │ • Stack layout         │  │
│  └────────────────────────┘  │
│  • Instruction selection     │
│  • Register allocation       │
│  • MIPS code emission        │
└──────────────────────────────┘
      ↓
MIPS Assembly (.s) + TAC files
```

## 💾 Understanding Symbol Tables

### Semantic Symbol Table (Phase 3)

**Location**: `semantic.c:23-115`

**Purpose**: Validate that the program makes semantic sense

**Data Structure**:
```c
/* Scope for variables */
typedef struct {
    char* names[MAX_VARS];  // Just variable NAMES
    int count;
} Scope;

static Scope scopes[MAX_SCOPE_DEPTH];  // Stack of scopes
static int scopeDepth = 0;
static char* currentFunction = NULL;
```

**Features**:
- ✅ Nested scopes (global, function, block)
- ✅ Shadowing support (inner scope hides outer)
- ✅ Function parameter tracking
- ✅ Visual scope stack printing
- ✅ Destroyed after semantic checking completes

**Example Output**:
```
┌─────────────────────────────────────────────────────────┐
│ SEMANTIC SCOPE STACK (Depth: 2)
├─────────────────────────────────────────────────────────┤
│ Scope[0] GLOBAL (0 variables)
│   (empty)
│ Scope[1] Function 'add' (2 variables)
│   Variables: a, b
└─────────────────────────────────────────────────────────┘
```

### Codegen Symbol Table (Phase 6)

**Location**: `symtab.c:14-76`

**Purpose**: Map variables to memory locations for code generation

**Data Structure**:
```c
typedef struct {
    char* name;     // Variable identifier
    int offset;     // Stack offset in bytes
} Symbol;

typedef struct {
    Symbol vars[MAX_VARS];  // Flat array
    int count;
    int nextOffset;         // Next available offset
} SymbolTable;

SymbolTable symtab;  // Single global instance
```

**Features**:
- ✅ Flat structure (no nesting)
- ✅ Memory offset tracking
- ✅ Built fresh from TAC instructions
- ✅ Stack layout management
- ✅ Debug tracing output

**Example Output**:
```
=== SYMBOL TABLE STATE ===
Count: 3, Next Offset: 12
Variables:
  [0] a -> offset 0
  [1] b -> offset 4
  [2] result -> offset 8
==========================
```

### Why This Design?

```
┌─────────────────────────────────────────────────────────┐
│ PHASE 3: Semantic Analysis                              │
│                                                          │
│ Question: "Is variable 'a' declared in visible scope?"  │
│ Answer:   Uses semantic table with nested scopes        │
│                                                          │
│ Example:                                                 │
│   int add(int a, int b) {                               │
│       return a + b;  // ✓ 'a' and 'b' are in scope     │
│   }                                                      │
└─────────────────────────────────────────────────────────┘
                         ↓
              [Semantic table discarded]
                         ↓
┌─────────────────────────────────────────────────────────┐
│ PHASE 6: Code Generation                                │
│                                                          │
│ Question: "Where is variable 'a' stored in memory?"     │
│ Answer:   Uses codegen table with stack offsets         │
│                                                          │
│ Example:                                                 │
│   lw $t0, 0($sp)    # Load 'a' from offset 0           │
│   lw $t1, 4($sp)    # Load 'b' from offset 4           │
│   add $t2, $t0, $t1                                     │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Build & Run

### Prerequisites
- `flex` (lexical analyzer generator)
- `bison` (parser generator)
- `gcc` (C compiler)
- MIPS simulator (MARS, SPIM, or QtSPIM) for running output

### Compilation
```bash
# Build the compiler
make

# Compile a source file
./minicompiler input.c output.s

# Clean build files
make clean
```

### Example Session
```bash
$ ./minicompiler test_func_simple.c test.s

╔════════════════════════════════════════════════════════════╗
║          MINIMAL C COMPILER - EDUCATIONAL VERSION         ║
╚════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────┐
│ PHASE 1: LEXICAL & SYNTAX ANALYSIS                       │
├──────────────────────────────────────────────────────────┤
│ • Reading source file: test_func_simple.c
│ • Tokenizing input (scanner.l)
│ • Parsing grammar rules (parser.y)
│ • Building Abstract Syntax Tree
└──────────────────────────────────────────────────────────┘
✓ Parse successful - program is syntactically correct!

┌──────────────────────────────────────────────────────────┐
│ PHASE 3: SEMANTIC ANALYSIS                               │
├──────────────────────────────────────────────────────────┤

Entered global scope

┌─────────────────────────────────────────────────────────┐
│ SEMANTIC SCOPE STACK (Depth: 1)
├─────────────────────────────────────────────────────────┤
│ Scope[0] GLOBAL (0 variables)
│   (empty)
└─────────────────────────────────────────────────────────┘

─── Checking function: add ───
  Entered function 'add' scope

┌─────────────────────────────────────────────────────────┐
│ SEMANTIC SCOPE STACK (Depth: 2)
├─────────────────────────────────────────────────────────┤
│ Scope[0] GLOBAL (0 variables)
│   (empty)
│ Scope[1] Function 'add' (2 variables)
│   Variables: a, b
└─────────────────────────────────────────────────────────┘

[... TAC generation, optimization, and code generation ...]

✓ COMPILATION SUCCESSFUL!
```

## 📝 Example Programs

### Simple Function
```c
int add(int a, int b) {
    int result;
    result = a + b;
    return result;
}

int main() {
    int x;
    int y;
    int z;

    x = 5;
    y = 10;
    z = add(x, y);
    print(z);    // Output: 15

    return 0;
}
```

### Control Flow Example
```c
int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

int main() {
    int result;
    result = max(10, 20);
    print(result);  // Output: 20
    return 0;
}
```

### Loop Example
```c
int factorial(int n) {
    int result;
    result = 1;

    while (n > 1) {
        result = result * n;
        n = n - 1;
    }

    return result;
}

int main() {
    int fact;
    fact = factorial(5);
    print(fact);  // Output: 120
    return 0;
}
```

## 🔄 Three-Address Code (TAC) Generation

### Why TAC?

TAC is the **bridge** between high-level code and machine code:

1. **Platform Independent**: Same TAC works for MIPS, x86, ARM, etc.
2. **Easy to Optimize**: Simple structure makes transformations straightforward
3. **No Symbol Table Needed**: All variable names are embedded in TAC
4. **Linearized Control Flow**: Makes code generation simpler

### TAC for Functions

**Source Code:**
```c
int add(int a, int b) {
    int result;
    result = a + b;
    return result;
}
```

**Generated TAC:**
```
1: FUNC_BEGIN add
2: PARAM a           ← Parameter declarations
3: PARAM b
4: DECL result
5: t0 = a + b
6: result = t0
7: RETURN result
8: FUNC_END add
```

**Why TAC Doesn't Need a Symbol Table:**
- Variable names ('a', 'b', 'result') are directly embedded
- TAC is self-contained
- Can be saved to file and loaded independently
- Code generator rebuilds symbol table from TAC

### TAC Instruction Types

```c
typedef enum {
    /* Arithmetic */
    TAC_ADD, TAC_SUB, TAC_MUL, TAC_DIV, TAC_NEG,

    /* Comparison */
    TAC_LT, TAC_GT, TAC_LE, TAC_GE, TAC_EQ, TAC_NE,

    /* Assignment & I/O */
    TAC_ASSIGN, TAC_PRINT, TAC_DECL,

    /* Control Flow */
    TAC_LABEL, TAC_GOTO, TAC_IF_FALSE, TAC_IF_TRUE,

    /* Functions */
    TAC_FUNC_BEGIN,   // Mark function start
    TAC_FUNC_END,     // Mark function end
    TAC_PARAM,        // Declare parameter
    TAC_ARG,          // Pass argument
    TAC_CALL,         // Call function
    TAC_RETURN        // Return from function
} TACOp;
```

## 🎓 Educational Features

### 1. Visual Scope Tracking

The semantic analyzer now prints the scope stack as it evolves:

```
Entered function 'add' scope

┌─────────────────────────────────────────────────────────┐
│ SEMANTIC SCOPE STACK (Depth: 2)
├─────────────────────────────────────────────────────────┤
│ Scope[0] GLOBAL (0 variables)
│   (empty)
│ Scope[1] Function 'add' (2 variables)
│   Variables: a, b
└─────────────────────────────────────────────────────────┘
```

This helps students understand:
- How scopes are nested
- When variables come into scope
- How parameters are treated as local variables
- When scopes are destroyed

### 2. Dual Symbol Table Visualization

Students can see both symbol tables in action:

**Phase 3 - Semantic Table:**
```
Scope[1] Function 'add' (2 variables)
  Variables: a, b
```

**Phase 6 - Codegen Table:**
```
=== SYMBOL TABLE STATE ===
Variables:
  [0] a -> offset 0
  [1] b -> offset 4
==========================
```

### 3. Line Number Error Reporting

Syntax errors now show exact line numbers:
```
Syntax Error at line 4: syntax error
```

### 4. Complete Compilation Trace

Every phase shows detailed output:
- ✅ Token stream (if verbose mode enabled)
- ✅ Abstract Syntax Tree structure
- ✅ Semantic scope evolution
- ✅ Unoptimized TAC
- ✅ Optimized TAC (saved to `.optimized.tac`)
- ✅ Symbol table states
- ✅ Generated MIPS assembly

## 📁 File Structure

```
CST-405-functions/
├── scanner.l              # Lexical analyzer (Flex)
│                          # Now with line number tracking
├── parser.y               # Grammar rules (Bison)
│                          # Supports functions, control flow
├── ast.h/c                # Abstract Syntax Tree
│                          # Nodes for functions, params, returns
├── semantic.h/c           # Semantic analysis
│                          # SEMANTIC SYMBOL TABLE (scope-based)
│                          # Function signature tracking
├── symtab.h/c             # Code generation symbol table
│                          # CODEGEN SYMBOL TABLE (flat, memory-based)
├── tac.h/c                # Three-address code generation
│                          # Function support, control flow
├── codegen.h/c            # MIPS code generator
│                          # Function prologues/epilogues
├── main.c                 # Compiler driver
├── Makefile               # Build configuration
├── test_*.c               # Example programs
├── COMPILER_AUDIT_REPORT.md  # Detailed audit findings
└── README.md              # This file
```

## 🔍 Deep Dive: Why Two Symbol Tables?

This is a **fundamental compiler architecture decision** that demonstrates clean phase separation:

### Information Flow Without Symbol Tables

```
Source → AST → Semantic Check → TAC → Optimize → Code Gen
         ↓           ↓            ↓                  ↓
         |      Semantic Table    |           Codegen Table
         |      (validates)       |           (allocates)
         |      DISCARDED ────────┘           REBUILT
         |
         └──────────────────────────────────────→ Names preserved
```

### The Genius of This Design

1. **TAC is Self-Contained**
   - Can save TAC to file
   - Can load TAC later
   - Can compile with different backends
   - No symbol table dependency

2. **Phase Independence**
   - Semantic analysis can change without affecting codegen
   - Codegen can change without affecting semantic analysis
   - Different memory layouts possible (stack, heap, registers)

3. **Educational Clarity**
   - Students see checking vs allocation as separate concerns
   - Demonstrates single responsibility principle
   - Shows how information transforms through phases

4. **Real-World Pattern**
   - LLVM uses similar approach
   - GCC has multiple intermediate representations
   - Production compilers separate concerns this way

### What Gets Lost? What Gets Preserved?

**Lost After Semantic Phase:**
- ❌ Scope hierarchy (nested structures)
- ❌ Which scope each variable belongs to
- ❌ Shadowing relationships

**Preserved in TAC:**
- ✅ Variable names
- ✅ Function names
- ✅ Parameter names
- ✅ All operations and control flow

**Rebuilt in Codegen:**
- ✅ Variable locations (stack offsets)
- ✅ Flat symbol table (all visible variables)
- ✅ Memory layout

## 🎯 Learning Objectives

After studying this compiler, students will understand:

1. **Lexical Analysis**: Pattern matching, token generation, line tracking
2. **Parsing**: Context-free grammars, AST construction, error recovery
3. **Semantic Analysis**:
   - Scope management
   - Symbol table design
   - Type checking
   - Function signature validation
4. **Intermediate Representation**:
   - Three-address code
   - Why IR is platform-independent
   - How TAC simplifies optimization
5. **Symbol Tables**:
   - When to use nested scopes vs flat tables
   - Semantic checking vs code generation needs
   - How information flows through compilation
6. **Optimization**: Constant folding, copy propagation
7. **Code Generation**:
   - Instruction selection
   - Register allocation
   - Stack frame management
   - Function calling conventions
8. **Software Architecture**:
   - Phase separation
   - Single responsibility principle
   - Clean interfaces between components

## 🔬 Advanced Topics Demonstrated

### Function Calling (Partial Implementation)

The compiler generates function prologue/epilogue markers:

```mips
# Function: add
add:
    # Parameter 'a' at offset 0
    # Parameter 'b' at offset 4
    # Declared 'result' at offset 8
    lw $t0, 0($sp)     # Load a
    lw $t1, 4($sp)     # Load b
    add $t2, $t0, $t1  # Compute a + b
    sw $t2, 8($sp)     # Store to result
    move $v0, $t2      # Return value
    jr $ra             # Return to caller
```

**Note**: Full activation record management and parameter passing via registers would be the next enhancement.

---

## 🏗️ Deep Dive: Two Symbol Tables Architecture

### The Fundamental Design Decision

This compiler implements a **clean separation of concerns** through two distinct symbol tables - a pattern found in production compilers like LLVM and GCC.

### Symbol Table #1: Semantic Analysis (semantic.c)

**Location**: `semantic.c:23-115`

**Purpose**: Validate program correctness

**Data Structure**:
```c
typedef struct {
    char* names[MAX_VARS];  // Variable names only
    int count;
} Scope;

static Scope scopes[MAX_SCOPE_DEPTH];  // Stack of nested scopes
static int scopeDepth = 0;
static char* currentFunction = NULL;
```

**Key Features**:
1. **Nested Scopes**: Maintains a stack of scopes (global → function → block)
2. **Shadowing Support**: Inner scopes can hide outer scope variables
3. **Function Context**: Tracks current function for return validation
4. **Scope Hierarchy**: Proper lexical scoping rules

**Questions This Table Answers**:
- ✅ Is variable 'x' declared before use?
- ✅ Is variable 'x' declared in a visible scope?
- ✅ Is there a redeclaration in the same scope?
- ✅ Are function parameters accessible in the function body?
- ✅ Does a function call match the signature?

**Lifetime**: Created at Phase 3 start → Destroyed after Phase 3 completes

**Example**:
```c
int main() {
    int x;           // Scope[1] depth 1
    {
        int y;       // Scope[2] depth 2
        int x;       // ✓ Shadows outer x - legal!
    }
    int y;           // ✓ y from inner scope destroyed
}
```

### Symbol Table #2: Code Generation (symtab.c)

**Location**: `symtab.c:14-76`

**Purpose**: Assign memory locations for variables

**Data Structure**:
```c
typedef struct {
    char* name;     // Variable name
    int offset;     // Stack offset in bytes
} Symbol;

typedef struct {
    Symbol vars[MAX_VARS];
    int count;
    int nextOffset;
} SymbolTable;

SymbolTable symtab;  // Single global flat table
```

**Key Features**:
1. **Flat Structure**: No nesting - all variables in one list
2. **Memory Offsets**: Maps variables to stack locations
3. **Built from TAC**: Reconstructed from TAC instructions
4. **Stack Layout**: Determines variable memory addresses

**Questions This Table Answers**:
- ✅ What stack offset does variable 'x' have?
- ✅ How much stack space do we need?
- ✅ Where should this load/store instruction access?

**Lifetime**: Created at Phase 6 start → Used throughout code generation

**Example**:
```c
int add(int a, int b) {
    int result;
    ...
}

Symbol Table:
  a      → offset 0   (4 bytes)
  b      → offset 4   (4 bytes)
  result → offset 8   (4 bytes)
Total stack: 12 bytes
```

### Why Two Tables? The Information Flow

```
┌──────────────────────────────────────────────────────┐
│ PHASE 3: Semantic Analysis                           │
│                                                       │
│ Input:  AST (tree structure)                         │
│ Tool:   Semantic Symbol Table (nested scopes)        │
│ Output: Validation (errors or success)               │
│                                                       │
│ Question: "Is this code semantically correct?"       │
│ Answer:   Check scopes, declarations, types          │
└──────────────────────────────────────────────────────┘
                         ↓
              [Semantic Table DISCARDED]
              [Information preserved in TAC]
                         ↓
┌──────────────────────────────────────────────────────┐
│ PHASE 4: TAC Generation                              │
│                                                       │
│ Input:  AST                                          │
│ Tool:   NONE - No symbol table needed!               │
│ Output: TAC with embedded variable names             │
│                                                       │
│ TAC Example:                                         │
│   PARAM a                                            │
│   PARAM b                                            │
│   DECL result                                        │
│   t0 = a + b       ← Variable names preserved!      │
│   result = t0                                        │
└──────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────┐
│ PHASE 6: Code Generation                             │
│                                                       │
│ Input:  Optimized TAC                                │
│ Tool:   Codegen Symbol Table (flat, memory-focused)  │
│ Output: MIPS assembly                                │
│                                                       │
│ Question: "Where is variable 'a' in memory?"        │
│ Answer:   Look up offset, generate lw/sw            │
│                                                       │
│ Assembly Example:                                    │
│   lw $t0, 0($sp)    # Load 'a' from offset 0        │
│   lw $t1, 4($sp)    # Load 'b' from offset 4        │
└──────────────────────────────────────────────────────┘
```

### The Genius of This Design

**1. TAC as the Bridge**

TAC doesn't need a symbol table because variable names are **embedded** in the instructions:
```
t0 = a + b    ← Variable names 'a', 'b', 't0' are in the TAC
```

This means:
- ✅ TAC can be saved to a file
- ✅ TAC can be loaded and compiled independently
- ✅ Different back-ends can use different memory layouts
- ✅ Optimization can happen without symbol table coordination

**2. Phase Independence**

Each phase has exactly the data structure it needs:
- **Semantic**: Needs nesting, scoping rules → Nested scope stack
- **Codegen**: Needs memory locations → Flat offset table

Changes to one don't affect the other!

**3. Real-World Pattern**

**LLVM IR** (Intermediate Representation):
```llvm
define i32 @add(i32 %a, i32 %b) {
entry:
  %result = alloca i32       ; Variable names preserved
  %0 = add i32 %a, %b        ; Self-contained
  store i32 %0, i32* %result
  ret i32 %result
}
```

LLVM IR is self-contained (like our TAC), allowing:
- Multiple optimization passes
- Different target architectures (x86, ARM, MIPS)
- Separate compilation units

**GCC's RTL** (Register Transfer Language):
- Also self-contained intermediate form
- Variables referenced by name/number
- Symbol table rebuilt for each target architecture

### What Gets Lost vs Preserved

**❌ Lost After Semantic Phase:**
- Scope nesting structure
- Which scope each variable belongs to
- Shadowing relationships
- Block boundaries

**✅ Preserved in TAC:**
- All variable names
- All function names
- All parameters
- Complete program logic
- Control flow structure

**✅ Rebuilt in Codegen:**
- Variable memory locations
- Stack layout
- Register assignments

### Educational Value

Students learn:
1. **Separation of Concerns**: Different phases need different data
2. **Interface Design**: TAC is the clean interface between phases
3. **Real Compiler Patterns**: This is how LLVM, GCC, and others work
4. **Trade-offs**: Nested vs flat, validation vs allocation

---

## 🎯 Deep Dive: Register Allocation

### Overview

Register allocation is the process of mapping **unlimited virtual registers** (TAC temporaries and variables) to the **limited physical registers** available on the CPU.

**The Problem**:
- TAC generates temporaries: t0, t1, t2, t3, ..., t99, ... (unlimited)
- MIPS has only 10 temp registers: $t0-$t9 (10 registers)
- **How do we map unlimited to limited?**

### Our Implementation

**Location**: `codegen.c:26-162`

**Strategy**: Linear scan with LRU (Least Recently Used) spilling

### Data Structures

```c
#define NUM_TEMP_REGS 10   // $t0 through $t9

typedef struct {
    char varName[MAX_VAR_NAME];  // Which variable/temp is in this register
    int inUse;                   // Is this register currently allocated?
    int isDirty;                 // Has value been modified (needs writeback)?
    int lastUsed;                // Timestamp of last use (for LRU)
} RegisterDescriptor;

typedef struct {
    RegisterDescriptor regs[NUM_TEMP_REGS];
    int timestamp;               // Global timestamp counter
    int spillCount;              // Statistics: how many spills occurred
} RegisterAllocator;

RegisterAllocator regAlloc;  // Global allocator instance
```

### Core Algorithm

**1. Register Lookup** (codegen.c:40)
```c
int findVarReg(const char* varName) {
    for (int i = 0; i < NUM_TEMP_REGS; i++) {
        if (regAlloc.regs[i].inUse &&
            strcmp(regAlloc.regs[i].varName, varName) == 0) {
            regAlloc.regs[i].lastUsed = regAlloc.timestamp++;  // Update LRU
            return i;  // Found! Return $ti
        }
    }
    return -1;  // Not in any register
}
```

**2. Register Allocation** (codegen.c:90)
```c
int allocReg(const char* varName) {
    // Check if already allocated
    int existing = findVarReg(varName);
    if (existing != -1) return existing;

    // Find free register
    for (int i = 0; i < NUM_TEMP_REGS; i++) {
        if (!regAlloc.regs[i].inUse) {
            regAlloc.regs[i].inUse = 1;
            strcpy(regAlloc.regs[i].varName, varName);
            regAlloc.regs[i].isDirty = 0;
            regAlloc.regs[i].lastUsed = regAlloc.timestamp++;
            return i;  // Allocated $ti
        }
    }

    // No free registers - must spill!
    int victim = selectVictimReg();  // LRU selection
    spillReg(victim);

    // Use freed register
    regAlloc.regs[victim].inUse = 1;
    strcpy(regAlloc.regs[victim].varName, varName);
    regAlloc.regs[victim].isDirty = 0;
    regAlloc.regs[victim].lastUsed = regAlloc.timestamp++;
    return victim;
}
```

**3. LRU Victim Selection** (codegen.c:52)
```c
int selectVictimReg() {
    int victim = 0;
    int oldestTime = regAlloc.regs[0].lastUsed;

    // Find register with oldest timestamp
    for (int i = 1; i < NUM_TEMP_REGS; i++) {
        if (regAlloc.regs[i].lastUsed < oldestTime) {
            oldestTime = regAlloc.regs[i].lastUsed;
            victim = i;
        }
    }

    return victim;  // Return index of LRU register
}
```

**4. Register Spilling** (codegen.c:67)
```c
void spillReg(int regNum) {
    if (!regAlloc.regs[regNum].inUse) return;

    // Only spill if value was modified (dirty)
    if (regAlloc.regs[regNum].isDirty) {
        int offset = getVarOffset(regAlloc.regs[regNum].varName);
        if (offset != -1) {
            // Generate store instruction
            fprintf(output, "    # Spilling $t%d (%s) to memory\n",
                    regNum, regAlloc.regs[regNum].varName);
            fprintf(output, "    sw $t%d, %d($sp)\n", regNum, offset);
            regAlloc.spillCount++;
        }
    }

    // Mark register as free
    regAlloc.regs[regNum].inUse = 0;
    regAlloc.regs[regNum].isDirty = 0;
}
```

### Complete Example

**TAC Input**:
```
t0 = a + b
t1 = c + d
t2 = e + f
t3 = t0 + t1
t4 = t2 + t3
...
t15 = ...  ← More temporaries than registers!
```

**Register Allocation Trace**:
```
Instruction: t0 = a + b
  [ALLOC] $t0 ← a      (timestamp 0)
  [ALLOC] $t1 ← b      (timestamp 1)
  [ALLOC] $t2 ← t0     (timestamp 2)

Instruction: t1 = c + d
  [ALLOC] $t3 ← c      (timestamp 3)
  [ALLOC] $t4 ← d      (timestamp 4)
  [ALLOC] $t5 ← t1     (timestamp 5)

... continues ...

Instruction: t10 = x + y  (all 10 registers in use!)
  [ALLOC] Need register for x
  [NO FREE REGISTERS]
  [LRU] Oldest is $t0 (timestamp 0)
  [SPILL] sw $t0, offset($sp)  ← Write back to memory
  [ALLOC] $t0 ← x      (timestamp 10, reused)
```

### Dirty Bit Optimization

**The Dirty Bit** tracks whether a register value has been modified:

```c
// Case 1: Load-only (not dirty)
lw $t0, 0($sp)        # Load 'a' into $t0
                      # isDirty = 0 (just loaded, not modified)
// If we need to spill $t0 now:
//   → Skip the store! Value in memory is same as register

// Case 2: Modified (dirty)
li $t1, 10            # Load constant
add $t0, $t0, $t1     # Modify $t0
                      # isDirty = 1 (value changed)
// If we need to spill $t0 now:
//   → Must store! sw $t0, offset($sp)
```

**Why This Matters**:
- Saves memory bandwidth
- Reduces generated code size
- Common optimization in real compilers

### Handling TAC Temporaries

TAC temporaries (t0, t1, t2, ...) vs MIPS registers ($t0, $t1, ...):

```
TAC: t0 = a + b       ← t0 is a TAC temporary (virtual)
     t1 = t0 + c
     x = t1

MIPS: lw $t3, offset_a($sp)    # 'a' → $t3
      lw $t4, offset_b($sp)    # 'b' → $t4
      add $t5, $t3, $t4        # t0 → $t5 (TAC t0 mapped to MIPS $t5)
      lw $t6, offset_c($sp)    # 'c' → $t6
      add $t7, $t5, $t6        # t1 → $t7 (TAC t1 mapped to MIPS $t7)
      sw $t7, offset_x($sp)    # Store to 'x'
```

**Key Insight**: TAC temporaries are treated just like variables:
- Allocated to MIPS registers
- Can be spilled if needed
- Tracked by the register allocator

### Register Allocation Strategies (Advanced)

Our compiler uses **linear scan with LRU**. Production compilers use:

**1. Graph Coloring** (optimal but expensive):
```
Variables as nodes, conflicts as edges
Colors = registers, goal: minimize colors used

 a ------- b         a and b can't be in same register
  \       /          (used simultaneously)
   \     /
     c

Solution: a→$t0, b→$t1, c→$t0 (c can reuse a's register)
```

**2. Linear Scan** (fast, good enough):
```
Sort variables by live range
Scan left to right, allocate registers
Spill when out of registers

Our implementation is this approach!
```

**3. SSA-based** (modern approach):
```
Static Single Assignment form
Each variable assigned exactly once
Enables better optimization
Used by LLVM
```

### Statistics and Debugging

```c
void printRegAllocStats() {
    printf("Total registers spilled:     %3d\n", regAlloc.spillCount);
    printf("Final register usage:\n");

    for (int i = 0; i < NUM_TEMP_REGS; i++) {
        if (regAlloc.regs[i].inUse) {
            printf("  $t%-2d: %-20s%s\n",
                   i, regAlloc.regs[i].varName,
                   regAlloc.regs[i].isDirty ? " (dirty)" : "");
        }
    }
}
```

**Example Output**:
```
┌──────────────────────────────────────────────────────────┐
│ REGISTER ALLOCATION STATISTICS                           │
├──────────────────────────────────────────────────────────┤
│ Total registers spilled:       5                         │
│ Final register usage:                                    │
│   $t0 : x                                         │
│   $t1 : y                                         │
│   $t2 : t0                                        │
└──────────────────────────────────────────────────────────┘
```

---

## ⚡ Deep Dive: Optimization Tracking

### Overview

The compiler now tracks and reports every optimization applied during the optimization phase, making the transformation process transparent to students.

**Location**: `tac.c:477-585`

### Optimization Techniques Implemented

**1. Constant Folding**

Evaluates compile-time constant expressions:

```c
// Before optimization:
x = 5 + 3;        →  TAC: t0 = 5 + 3
                      x = t0

// After optimization:
x = 8;            →  TAC: t0 = 8
                      x = t0

Optimization logged:
  [8] CONSTANT FOLDING: t0 = 5 + 3 → t0 = 8
```

**Supported Operations**:
- Arithmetic: `+`, `-`, `*`, `/`
- Comparisons: `<`, `>`, `<=`, `>=`, `==`, `!=`

**Implementation** (tac.c:492):
```c
static char* foldConstants(TACOp op, const char* arg1, const char* arg2, int* folded) {
    if (!isConstantNumber(arg1) || !isConstantNumber(arg2)) {
        return NULL;  // Can't fold non-constants
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
        // ... more operations
    }

    if (*folded) {
        char* resultStr = malloc(20);
        sprintf(resultStr, "%d", result);
        return resultStr;
    }
    return NULL;
}
```

**2. Copy Propagation**

Tracks constant assignments:

```c
// TAC:
x = 10           ← x now known to be constant 10
y = x            → Can propagate: y = 10

Optimization logged:
  [15] COPY PROPAGATION: x = 10 (constant)
```

### Visual Optimization Tracking

**Output Format**:
```
┌──────────────────────────────────────────────────────────┐
│ OPTIMIZATION PASS - Tracking Changes                    │
├──────────────────────────────────────────────────────────┤
│ [  8] CONSTANT FOLDING: t0 = 10 + 5 → t0 = 15
│ [ 10] CONSTANT FOLDING: t0 = 20 - 8 → t0 = 12
│ [ 16] CONSTANT FOLDING: t0 = 3 * 4 → t0 = 12
│ [ 22] CONSTANT FOLDING: t0 = 5 + 3 → t0 = 8
│ [ 24] CONSTANT FOLDING: t0 = 10 * 2 → t0 = 20
│ [ 31] CONSTANT FOLDING: t0 = 2 * 3 → t0 = 6
├──────────────────────────────────────────────────────────┤
│ Total optimizations applied:   6                         │
└──────────────────────────────────────────────────────────┘
```

### Complete Example

**Source Code**:
```c
int main() {
    int x;
    int y;

    x = 10 + 5;     // Optimization opportunity!
    y = 20 - 8;     // Optimization opportunity!

    print(x + y);
    return 0;
}
```

**Unoptimized TAC**:
```
 1: FUNC_BEGIN main
 2: DECL x
 3: DECL y
 4: t0 = 10 + 5        ← 10 + 5 are constants!
 5: x = t0
 6: t0 = 20 - 8        ← 20 - 8 are constants!
 7: y = t0
 8: t0 = x + y
 9: PRINT t0
10: RETURN 0
11: FUNC_END main
```

**Optimization Process**:
```
Processing instruction 4: t0 = 10 + 5
  → Both operands are constants
  → Fold: 10 + 5 = 15
  → Log: [4] CONSTANT FOLDING: t0 = 10 + 5 → t0 = 15

Processing instruction 6: t0 = 20 - 8
  → Both operands are constants
  → Fold: 20 - 8 = 12
  → Log: [6] CONSTANT FOLDING: t0 = 20 - 8 → t0 = 12
```

**Optimized TAC**:
```
 1: FUNC_BEGIN main
 2: DECL x
 3: DECL y
 4: t0 = 15            ← Folded from 10 + 5
 5: x = t0
 6: t0 = 12            ← Folded from 20 - 8
 7: y = t0
 8: t0 = x + y
 9: PRINT t0
10: RETURN 0
11: FUNC_END main
```

### Educational Value

Students can:
1. **See transformations**: Each optimization is logged with before/after
2. **Count optimizations**: Total count shows optimization impact
3. **Trace changes**: Line numbers show where optimizations occur
4. **Compare output**: Side-by-side unoptimized vs optimized TAC
5. **Understand trade-offs**: More optimization passes = better code but longer compile time

### Future Optimizations

The infrastructure supports adding:
- **Dead Code Elimination**: Remove unused variables
- **Common Subexpression Elimination**: Reuse computed values
- **Strength Reduction**: Replace expensive ops (multiply → shift)
- **Loop Optimizations**: Unrolling, invariant code motion

---

## 🤝 Contributing

This is an educational project. Suggestions for:
- Clearer explanations
- Better visual output
- Additional example programs
- Documentation improvements

...are always welcome!

## 📜 License

Educational use - free to use and modify for teaching purposes.

## 🙏 Acknowledgments

This compiler demonstrates real compiler architecture principles while remaining accessible to students. The dual symbol table design, phase separation, and extensive tracing make it an excellent teaching tool for understanding how compilers really work.
