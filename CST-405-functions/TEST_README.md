# Test Files Documentation

This document describes the test files included to verify the compiler's functionality.

## Test Files Overview

### 1. **test.c** - Comprehensive Test Suite
**Purpose:** Tests all major features and optimization scenarios

**Test Cases:**
1. **Basic Addition (Lines 14-15):**
   ```
   result = a + b;        // 5 + 10 = 15
   ```
   - Tests simple binary addition
   - Demonstrates constant propagation: `a=5, b=10` → `result=15`

2. **Multi-operand Addition (Lines 17-18):**
   ```
   result = a + b + c;    // 5 + 10 + 15 = 30
   ```
   - Tests chained additions
   - Shows TAC linearization with temporaries

3. **Large Constants (Lines 20-23):**
   ```
   d = 100; e = 200;
   result = d + e;        // 300
   ```
   - Tests larger numeric values
   - Verifies constant folding with bigger numbers

4. **Small Constants (Lines 25-28):**
   ```
   temp1 = 7; temp2 = 3;
   result = temp1 + temp2; // 10
   ```
   - Tests smaller values
   - Multiple temporary variables

5. **Pure Constant Expression (Lines 30-31):**
   ```
   result = 1 + 2;        // 3
   ```
   - **Key optimization test:** No variables, only constants
   - Should fold to `result = 3` at compile time
   - No runtime addition needed!

6. **Complex Multi-operand (Lines 33-34):**
   ```
   result = 5 + 10 + 15 + 20;  // 50
   ```
   - Tests maximum TAC optimization
   - Four constants → should become single constant `50`

7. **Copy Propagation Chain (Lines 36-40):**
   ```
   a = 1; b = a; c = b; d = c;  // All become 1
   ```
   - **Key optimization test:** Tests copy propagation
   - `d` should resolve to constant `1` through propagation chain

8. **Zero Arithmetic (Lines 42-43):**
   ```
   result = 0 + 0 + 0;    // 0
   ```
   - Edge case: operations with zero
   - Should optimize to `result = 0`

9. **Large Result (Lines 45-48):**
   ```
   a = 999; b = 1;
   result = a + b;        // 1000
   ```
   - Tests 4-digit results
   - Boundary value testing

10. **Duplicate Constants (Lines 50-53):**
    ```
    temp1 = 50; temp2 = 50;
    result = temp1 + temp2; // 100
    ```
    - Same values in different variables
    - Tests constant folding with duplicates

**Expected Output:**
```
15
30
300
10
3
50
1
0
1000
100
```

---

### 2. **test_simple.c** - Minimal Test
**Purpose:** Quick sanity check

**Test Case:**
```
x = 10; y = 20;
print(x + y);  // 30
```

**Expected Output:** `30`

**Use Case:** Fast compilation test during development

---

### 3. **test_constants.c** - Constant Folding Focus
**Purpose:** Stress test constant folding optimization

**Test Cases:**
1. **Five-operand addition:**
   ```
   result = 5 + 10 + 15 + 20 + 25;  // 75
   ```

2. **Three large constants:**
   ```
   result = 100 + 200 + 300;  // 600
   ```

3. **Ten operands:**
   ```
   result = 1+1+1+1+1+1+1+1+1+1;  // 10
   ```

**Expected Output:**
```
75
600
10
```

**What to Check:**
- Optimized TAC should show single constants, not chains of additions
- MIPS code should use `li` (load immediate) instead of `add` instructions

---

### 4. **test_propagation.c** - Copy Propagation Focus
**Purpose:** Verify copy propagation through variable chains

**Test Cases:**
1. **Five-level propagation:**
   ```
   a = 42;
   b = a;  c = b;  d = c;  e = d;
   print(e);  // Should propagate 42 through all variables
   ```

2. **Propagation with computation:**
   ```
   a = 10; b = 20;
   c = a + b;  // Should become c = 30
   ```

**Expected Output:**
```
42
30
```

**What to Check:**
- `e` should resolve to constant `42` in optimized TAC
- No unnecessary loads/stores in MIPS code

---

## How to Run Tests

### Run Specific Test:
```bash
./minicompiler test_simple.c output.s
```

### Run All Tests:
```bash
for test in test*.c; do
    echo "=== Testing $test ==="
    ./minicompiler "$test" "${test%.c}.s"
    echo
done
```

### Compare TAC Files:
```bash
# View optimization improvements
diff test.tac test.optimized.tac
```

---

## Optimization Verification Checklist

For each test, verify:

### ✅ TAC Generation
- [ ] Unoptimized TAC uses temporaries (t0, t1, t2...)
- [ ] TAC correctly represents expression trees
- [ ] Saved to `.tac` file

### ✅ Constant Folding
- [ ] Pure constant expressions evaluated at compile time
- [ ] Example: `1 + 2` becomes `3` in optimized TAC
- [ ] No `ADD` instructions for constant-only expressions

### ✅ Copy Propagation
- [ ] Variable chains resolve to source values
- [ ] Example: `a=5; b=a; c=b` → all become `5`
- [ ] Reduced variable dependencies

### ✅ Code Generation
- [ ] Optimized TAC used for MIPS generation (not AST)
- [ ] Constants loaded with `li` instructions
- [ ] Minimal register allocation
- [ ] Correct stack offsets for variables

---

## Understanding the Output

### TAC Files
- **test.tac** - Shows intermediate code before optimization
- **test.optimized.tac** - Shows code after constant folding & copy propagation

### MIPS Assembly
- **test.s** - Final assembly code
- Look for `li $tx, <constant>` for optimized constants
- Check for reduced `add` instructions

---

## Compiler Features Tested

| Feature | Tested By |
|---------|-----------|
| Variable declarations | All tests |
| Integer constants | All tests |
| Addition operator | All tests |
| Print statements | All tests |
| Multiple statements | test.c |
| Constant folding | test_constants.c |
| Copy propagation | test_propagation.c |
| Complex expressions | test.c (lines 33-34) |
| Register allocation | All tests (check MIPS output) |
| TAC generation | All tests |
| TAC optimization | All tests |

---

## Expected Behavior

### Unoptimized TAC Example:
```
12: t0 = a + b
13: result = t0
14: PRINT result
```

### Optimized TAC Example (with a=5, b=10):
```
12: t0 = 15           [constant: 15]
13: result = 15       [constant: 15]
14: PRINT 15          [constant: 15]
```

### Generated MIPS Example:
```mips
li $t0, 15         # Direct constant load
sw $t0, 20($sp)    # Store to result
li $t1, 15         # Load for print
move $a0, $t1
li $v0, 1
syscall
```

---

## Notes

- This compiler is **educational** and intentionally minimal
- Supports only: `int`, identifiers, numbers, `+`, `=`, `;`, `print()`
- Does **not** support: functions, control flow, other operators, types besides int
- Focus is on demonstrating compiler phases and optimizations
