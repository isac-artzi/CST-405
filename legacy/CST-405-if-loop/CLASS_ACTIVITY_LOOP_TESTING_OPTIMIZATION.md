# Interactive Class Activity: Loop Testing & Optimization

**CST-405 Compiler Design**
**Topic:** Advanced Loop Testing, Verification, and Optimization
**Format:** Interactive Presentation + Hands-on Lab
**Duration:** 120 minutes

---

## 📋 Table of Contents

1. [Introduction & Objectives](#introduction)
2. [Part 1: Understanding Nested Loops](#part-1-nested-loops)
3. [Part 2: Testing Strategies](#part-2-testing-strategies)
4. [Part 3: Control Flow Analysis](#part-3-control-flow)
5. [Part 4: Loop Optimizations](#part-4-optimizations)
6. [Part 5: Hands-on Lab](#part-5-lab)
7. [Part 6: Advanced Challenges](#part-6-challenges)

---

<a name="introduction"></a>
## 🎯 Introduction & Learning Objectives

### What We'll Learn Today

By the end of this session, you will:
- ✓ Understand how nested loops create complex control flow
- ✓ Design comprehensive test cases for loop implementations
- ✓ Analyze TAC output to verify correct behavior
- ✓ Identify optimization opportunities in loop code
- ✓ Implement basic loop optimizations

### Prerequisites
- ✅ Completed basic WHILE loop implementation
- ✅ Understand TAC (Three-Address Code)
- ✅ Familiar with control flow concepts
- ✅ Know how to read AST structures

---

<a name="part-1-nested-loops"></a>
## 📚 Part 1: Understanding Nested Loops (20 minutes)

### 1.1 Visual Model: Loop Nesting

Let's visualize how nested loops work:

```
┌─────────────────────────────────────────────────────────────┐
│                      OUTER LOOP                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Outer: Initialize i = 1                               │  │
│  │                                                        │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │            INNER LOOP                        │    │  │
│  │  │  ┌────────────────────────────────────────┐  │    │  │
│  │  │  │ Inner: Initialize j = 1                │  │    │  │
│  │  │  │                                         │  │    │  │
│  │  │  │ ┌─────────────────────────────────┐   │  │    │  │
│  │  │  │ │  Execute: print(i * j)          │   │  │    │  │
│  │  │  │ └─────────────────────────────────┘   │  │    │  │
│  │  │  │                                         │  │    │  │
│  │  │  │ Inner: Increment j                     │  │    │  │
│  │  │  │ Inner: Check j <= 3                    │  │    │  │
│  │  │  │        ↓ false                         │  │    │  │
│  │  │  └────────────────────────────────────────┘  │    │  │
│  │  │                                               │    │  │
│  │  │  Inner loop complete, return to outer       │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  │                                                        │  │
│  │  Outer: Increment i                                   │  │
│  │  Outer: Check i <= 2                                  │  │
│  │         ↓ false                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  All loops complete                                         │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Execution Flow Diagram

```
START
  │
  ├─→ [Outer Init: i=1]
  │
  ├─→ [Outer Condition: i<=2?] ──No──→ END
  │         │
  │        Yes
  │         ↓
  │   [Inner Init: j=1]
  │         │
  │   [Inner Condition: j<=3?] ──No──→ [i++] ──┐
  │         │                                    │
  │        Yes                                   │
  │         ↓                                    │
  │   [Execute Body: print(i*j)]                │
  │         │                                    │
  │   [j++] ─┘                                   │
  │         │                                    │
  │         └────────────────────────────────────┘
  │
  └─→ LOOP BACK
```

### 1.3 TAC Structure for Nested Loops

```assembly
# Outer loop structure
L_outer_start:
    t0 = i <= 2                    # Outer condition
    if_false t0 goto L_outer_end   # Exit outer if false

    # Inner loop structure (NESTED)
    L_inner_start:
        t1 = j <= 3                # Inner condition
        if_false t1 goto L_inner_end  # Exit inner if false

        # Inner body
        t2 = i * j
        print t2

        # Inner increment
        t3 = j + 1
        j = t3

        goto L_inner_start         # Loop inner
    L_inner_end:

    # Outer increment
    t4 = i + 1
    i = t4

    goto L_outer_start             # Loop outer
L_outer_end:
```

### 🎓 Discussion Question 1
> **How many labels are needed for nested loops?**
>
> Answer: Each loop needs 2 labels (start + end).
> For N nested loops: 2 × N labels needed.

---

### 1.4 Interactive Exercise: Trace the Execution

Given this code:
```c
int i;
int j;
i = 1;
while (i <= 2) {
    j = 1;
    while (j <= 3) {
        print(i * j);
        j = j + 1;
    }
    i = i + 1;
}
```

**✏️ YOUR TURN:** Fill in the execution table

| Iteration | i | j | i*j | Action |
|-----------|---|---|-----|--------|
| 1 | 1 | 1 | 1 | print(1) |
| 2 | 1 | 2 | ? | ? |
| 3 | 1 | 3 | ? | ? |
| 4 | 2 | 1 | ? | ? |
| 5 | 2 | 2 | ? | ? |
| 6 | 2 | 3 | ? | ? |

<details>
<summary>🔍 Click to reveal answer</summary>

| Iteration | i | j | i*j | Action |
|-----------|---|---|-----|--------|
| 1 | 1 | 1 | 1 | print(1) |
| 2 | 1 | 2 | 2 | print(2) |
| 3 | 1 | 3 | 3 | print(3) |
| 4 | 2 | 1 | 2 | print(2) |
| 5 | 2 | 2 | 4 | print(4) |
| 6 | 2 | 3 | 6 | print(6) |

**Total iterations:** 6 (outer: 2, inner: 3, total: 2×3)
</details>

---

<a name="part-2-testing-strategies"></a>
## 🧪 Part 2: Testing Strategies (25 minutes)

### 2.1 The Testing Pyramid for Loops

```
                    ┌─────────────────┐
                    │  Edge Cases     │  ← Complex scenarios
                    │  (Nested, etc)  │
                    ├─────────────────┤
                    │   Integration   │  ← Multiple loops
                    │     Tests       │
                    ├─────────────────┤
                    │  Functionality  │  ← Basic loop behavior
                    │     Tests       │
                    ├─────────────────┤
                    │     Unit        │  ← Individual components
                    │     Tests       │
                    └─────────────────┘
```

### 2.2 Test Categories

#### Category 1: Boundary Tests
Testing loop boundaries to catch off-by-one errors

```c
/* Test: Loop executes exactly N times */
int count;
count = 0;

while (count < 5) {    // Should execute 5 times
    print(count);       // 0, 1, 2, 3, 4
    count = count + 1;
}

// Expected output: 0, 1, 2, 3, 4
// Common error: Prints 0-5 (6 times) if using <=
```

**✏️ YOUR TURN:** Write a test where the loop should execute exactly 10 times

<details>
<summary>🔍 Example solution</summary>

```c
int i;
i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
// Output: 0 through 9 (10 numbers)
```
</details>

---

#### Category 2: Zero Iterations Test
Loops that should never execute

```c
/* Test: Loop with false condition should not execute */
int i;
i = 10;

while (i < 5) {        // Condition is false from start
    print(999);        // This should NEVER print
    i = i + 1;
}

print(100);            // This SHOULD print

// Expected output: 100 (only)
// TAC should jump over loop body
```

**Expected TAC Pattern:**
```assembly
i = 10
L0:
    t0 = i < 5              # t0 = false (0)
    if_false t0 goto L1     # Immediately jumps to L1
    # Body never executes
    print 999
    goto L0
L1:
    print 100               # Executes here
```

---

#### Category 3: Accumulator Pattern Tests
Testing loops that accumulate values

```c
/* Test: Sum of 1 to N */
int sum;
int i;
int n;

n = 10;
sum = 0;
i = 1;

while (i <= n) {
    sum = sum + i;
    i = i + 1;
}

print(sum);  // Expected: 55

// Formula verification: n(n+1)/2 = 10(11)/2 = 55
```

**✏️ YOUR TURN:** Design a test for calculating factorial of 5

<details>
<summary>🔍 Example solution</summary>

```c
int factorial;
int i;

factorial = 1;
i = 1;

while (i <= 5) {
    factorial = factorial * i;
    i = i + 1;
}

print(factorial);  // Expected: 120 (5! = 5×4×3×2×1)
```
</details>

---

#### Category 4: Nested Loop Tests

##### Test 4A: Simple 2D Grid
```c
/* Test: Print a 3x3 grid of coordinates */
int row;
int col;

row = 0;
while (row < 3) {
    col = 0;
    while (col < 3) {
        print(row * 10 + col);  // Print as two-digit number
        col = col + 1;
    }
    row = row + 1;
}

/* Expected output:
   00, 01, 02,
   10, 11, 12,
   20, 21, 22
*/
```

##### Test 4B: Triple Nesting
```c
/* Test: Three levels of nesting */
int i;
int j;
int k;

i = 1;
while (i <= 2) {
    j = 1;
    while (j <= 2) {
        k = 1;
        while (k <= 2) {
            print(i * 100 + j * 10 + k);
            k = k + 1;
        }
        j = j + 1;
    }
    i = i + 1;
}

/* Expected output: 111, 112, 121, 122, 211, 212, 221, 222
   Total iterations: 2 × 2 × 2 = 8
*/
```

---

### 2.3 Test Case Design Checklist

Use this checklist when designing loop tests:

```
┌─────────────────────────────────────────────────────────────┐
│                  LOOP TEST CHECKLIST                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [ ] Test 0 iterations (condition false from start)        │
│  [ ] Test 1 iteration (minimal case)                       │
│  [ ] Test N iterations (normal case)                       │
│  [ ] Test boundary conditions (off-by-one)                 │
│  [ ] Test accumulation correctness                         │
│  [ ] Test variable updates                                 │
│  [ ] Test nested loops (if applicable)                     │
│  [ ] Test with arrays (if applicable)                      │
│  [ ] Test with function calls (if applicable)              │
│  [ ] Verify TAC structure is correct                       │
│  [ ] Verify label uniqueness                               │
│  [ ] Verify no memory leaks                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 2.4 Interactive Exercise: Debug This Test

**Problem:** Student submitted this test, but it fails. Find the bug!

```c
/* Test: Sum of even numbers from 2 to 10 */
int sum;
int i;

sum = 0;
i = 2;

while (i < 10) {        // BUG HERE!
    sum = sum + i;
    i = i + 2;
}

print(sum);
// Student expects: 30 (2+4+6+8+10)
// Actually prints: 20 (2+4+6+8)
```

**✏️ YOUR TURN:** What's wrong? How do you fix it?

<details>
<summary>🔍 Answer</summary>

**Bug:** Condition should be `i <= 10`, not `i < 10`

**Reason:** Loop exits when i=10, missing the last value

**Fix:**
```c
while (i <= 10) {  // Include 10
    sum = sum + i;
    i = i + 2;
}
// Now prints: 30 ✓
```
</details>

---

<a name="part-3-control-flow"></a>
## 🔄 Part 3: Control Flow Analysis (20 minutes)

### 3.1 Control Flow Graphs (CFG)

A **Control Flow Graph** visualizes all possible execution paths.

#### Example: Simple While Loop CFG

```c
while (i < 5) {
    print(i);
    i = i + 1;
}
```

**CFG Representation:**
```
     ┌──────────┐
     │  Entry   │
     └────┬─────┘
          │
          ↓
     ┌──────────┐
  ┌──│ i < 5 ?  │──┐
  │  └──────────┘  │
  │                │
  │ true       false│
  ↓                ↓
┌──────────┐  ┌──────────┐
│ print(i) │  │   Exit   │
└────┬─────┘  └──────────┘
     │
     ↓
┌──────────┐
│ i = i+1  │
└────┬─────┘
     │
     │
     └───────┐
             ↓
         (back to condition)
```

---

### 3.2 Nested Loop CFG

```c
while (i < 2) {
    while (j < 3) {
        print(j);
        j = j + 1;
    }
    i = i + 1;
}
```

**CFG with Two Loops:**
```
        ┌──────────────┐
        │    Entry     │
        └──────┬───────┘
               │
               ↓
        ┌──────────────┐
     ┌──│  i < 2 ?     │──┐
     │  └──────────────┘  │
     │                    │
  true│                   │false
     ↓                    ↓
┌─────────────┐      ┌──────────┐
│ j = 1       │      │   Exit   │
└─────┬───────┘      └──────────┘
      │
      ↓
┌─────────────┐
│  j < 3 ?    │←──────┐
└─────┬───────┘       │
      │               │
   true│              │
      ↓               │
┌─────────────┐       │
│ print(j)    │       │
└─────┬───────┘       │
      ↓               │
┌─────────────┐       │
│ j = j + 1   │───────┘
└─────────────┘
      │
  false│
      ↓
┌─────────────┐
│ i = i + 1   │
└─────┬───────┘
      │
      └──────────┐
                 ↓
            (back to outer condition)
```

---

### 3.3 Path Coverage Analysis

**Goal:** Every possible path through the code should be tested.

#### Coverage Types:

1. **Statement Coverage:** Every line executes at least once
2. **Branch Coverage:** Every true/false decision tested
3. **Path Coverage:** Every unique path through CFG tested

**Example Analysis:**
```c
while (i < 3) {
    if (i == 1) {
        print(100);
    } else {
        print(200);
    }
    i = i + 1;
}
```

**Paths to Test:**
- Path 1: i=0 → false condition (0 iterations)
- Path 2: i=1 → enter loop → if true → print 100
- Path 3: i=0,2 → enter loop → if false → print 200
- Path 4: Multiple iterations testing both branches

---

### 3.4 Interactive Exercise: Draw the CFG

**✏️ YOUR TURN:** Draw the CFG for this code

```c
int i;
int sum;
i = 1;
sum = 0;

while (i <= 3) {
    if (i > 1) {
        sum = sum + i;
    }
    i = i + 1;
}

print(sum);
```

**Template:**
```
     Entry
       ↓
     i = 1
       ↓
    sum = 0
       ↓
    [Your CFG here]
       ↓
   print(sum)
       ↓
     Exit
```

<details>
<summary>🔍 Solution</summary>

```
     ┌──────────┐
     │  Entry   │
     └────┬─────┘
          ↓
     ┌──────────┐
     │  i = 1   │
     └────┬─────┘
          ↓
     ┌──────────┐
     │ sum = 0  │
     └────┬─────┘
          ↓
     ┌──────────┐
  ┌──│ i <= 3?  │──┐
  │  └──────────┘  │
  │                │
true│           false│
  ↓                ↓
┌──────────┐  ┌──────────┐
│ i > 1?   │  │print(sum)│
└──┬───┬───┘  └──────────┘
   │   │           ↓
T  │   │F      ┌──────────┐
   │   │       │   Exit   │
   ↓   ↓       └──────────┘
┌────┐ │
│+sum│ │
└─┬──┘ │
  │    │
  └──┬─┘
     ↓
┌──────────┐
│ i = i+1  │
└────┬─────┘
     │
     └──┐
        ↓
   (back to i<=3?)
```
</details>

---

<a name="part-4-optimizations"></a>
## ⚡ Part 4: Loop Optimizations (30 minutes)

### 4.1 Why Optimize Loops?

Loops often account for **90%+ of execution time** in programs!

```
┌───────────────────────────────────────────────────────────┐
│         PROGRAM EXECUTION TIME DISTRIBUTION               │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  Loops: ████████████████████████████████████████  90%    │
│  Other: ████                                       10%    │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

**Impact:** Optimizing loops by 10% → 9% total speedup!

---

### 4.2 Optimization 1: Constant Folding in Conditions

#### Before Optimization:
```c
while (i < 2 + 3) {    // Constant expression
    print(i);
    i = i + 1;
}
```

**TAC (Unoptimized):**
```assembly
L0:
    t0 = 2 + 3           # Computed EVERY iteration!
    t1 = i < t0
    if_false t1 goto L1
    print i
    t2 = i + 1
    i = t2
    goto L0
L1:
```

#### After Optimization:
**TAC (Optimized):**
```assembly
L0:
    t0 = i < 5           # Constant folded: 2+3 = 5
    if_false t0 goto L1
    print i
    t1 = i + 1
    i = t1
    goto L0
L1:
```

**Savings:** One ADD operation per iteration eliminated!

---

### 4.3 Optimization 2: Loop-Invariant Code Motion (LICM)

**Principle:** Move code that doesn't change out of the loop

#### Before Optimization:
```c
int i;
int result;
int a;
int b;

a = 10;
b = 20;
i = 0;

while (i < 100) {
    result = a + b;      // Same value every iteration!
    print(result);
    i = i + 1;
}
```

**TAC (Unoptimized):**
```assembly
a = 10
b = 20
i = 0
L0:
    t0 = i < 100
    if_false t0 goto L1
    t1 = a + b           # Computed 100 times!
    result = t1
    print result
    t2 = i + 1
    i = t2
    goto L0
L1:
```

#### After Optimization:
**TAC (Optimized):**
```assembly
a = 10
b = 20
i = 0
t1 = a + b               # Computed ONCE before loop!
result = t1
L0:
    t0 = i < 100
    if_false t0 goto L1
    print result         # Just use the value
    t2 = i + 1
    i = t2
    goto L0
L1:
```

**Savings:** 99 ADD operations eliminated!

---

### 4.4 Optimization 3: Dead Loop Elimination

**Principle:** Remove loops that never execute

#### Example 1: Condition Always False
```c
while (0) {              // Constant false
    print(100);
}
```

**TAC (Unoptimized):**
```assembly
L0:
    if_false 0 goto L1   # Always jumps
    print 100
    goto L0
L1:
```

**TAC (Optimized):**
```assembly
# Entire loop removed - dead code!
```

---

#### Example 2: Unreachable Loop
```c
int i;
i = 10;

while (i < 5) {          // 10 < 5 is always false
    print(i);
    i = i + 1;
}
```

**Optimized:** If compiler can prove `i = 10` and condition is `i < 5`, entire loop removed.

---

### 4.5 Optimization 4: Strength Reduction

**Principle:** Replace expensive operations with cheaper ones

#### Example: Multiplication to Addition
```c
int i;
int result;
i = 0;

while (i < 10) {
    result = i * 5;      // Multiplication
    print(result);
    i = i + 1;
}
```

**Before (Expensive MUL):**
```assembly
i = 0
L0:
    t0 = i < 10
    if_false t0 goto L1
    t1 = i * 5           # Multiplication (slow)
    result = t1
    print result
    t2 = i + 1
    i = t2
    goto L0
L1:
```

**After (Cheap ADD):**
```assembly
i = 0
result = 0               # Initialize result
L0:
    t0 = i < 10
    if_false t0 goto L1
    print result
    result = result + 5  # Addition (fast)
    i = i + 1
    goto L0
L1:
```

**Key Insight:** `i * 5` can be computed incrementally as `0, 5, 10, 15, ...` using addition!

---

### 4.6 Optimization Summary Table

| Optimization | When Applicable | Benefit | Difficulty |
|--------------|----------------|---------|------------|
| **Constant Folding** | Constants in loop | Reduce computations | Easy ⭐ |
| **LICM** | Loop-invariant expressions | Move out of loop | Medium ⭐⭐ |
| **Dead Loop Elimination** | Always false condition | Remove entire loop | Easy ⭐ |
| **Strength Reduction** | Multiplication by constant | Replace with addition | Hard ⭐⭐⭐ |
| **Loop Unrolling** | Small known bounds | Reduce branching | Medium ⭐⭐ |

---

### 4.7 Interactive Exercise: Identify Optimizations

**✏️ YOUR TURN:** What optimizations can be applied to this code?

```c
int i;
int j;
int x;
int y;
int result;

x = 5;
y = 10;
i = 0;

while (i < 100) {
    j = 0;
    while (j < 50) {
        result = x + y;      // Hint 1: Check this
        print(result);
        j = j + 1;
    }
    i = i + 1;
}
```

**Questions:**
1. Is there loop-invariant code?
2. Can we do constant folding?
3. What's the total number of `x + y` computations?

<details>
<summary>🔍 Answers</summary>

1. **Loop-Invariant Code:** YES!
   - `result = x + y` is invariant (x and y never change)
   - Can be moved outside BOTH loops

2. **Constant Folding:** NO
   - x and y are variables (even though they're constant values)
   - Would need interprocedural analysis

3. **Computations:** 100 × 50 = 5,000 times!
   - After LICM: Only 1 time!

**Optimized Version:**
```c
x = 5;
y = 10;
result = x + y;          // Compute once
i = 0;

while (i < 100) {
    j = 0;
    while (j < 50) {
        print(result);    // Just use it
        j = j + 1;
    }
    i = i + 1;
}
```

**Savings:** 4,999 ADD operations eliminated! ⚡
</details>

---

<a name="part-5-lab"></a>
## 🔬 Part 5: Hands-on Lab (30 minutes)

### Lab Setup

You'll work on three exercises:
1. **Testing:** Design comprehensive test cases
2. **Analysis:** Analyze TAC output for correctness
3. **Optimization:** Implement a simple optimization

---

### Exercise 1: Design Test Suite (10 minutes)

**Task:** Create a comprehensive test suite for this function:

```c
/* Function: Count multiples of 'divisor' up to 'limit' */
int countMultiples(int limit, int divisor) {
    int count;
    int i;

    count = 0;
    i = divisor;

    while (i <= limit) {
        count = count + 1;
        i = i + divisor;
    }

    return count;
}
```

**✏️ YOUR TASK:** Write at least 5 test cases covering:
- Normal case
- Edge cases (limit=0, divisor=1, etc.)
- Boundary conditions

**Template:**
```c
int main() {
    int result;

    /* Test 1: Normal case */
    result = countMultiples(10, 2);
    print(result);  // Expected: ?

    /* Test 2: Your test here */

    /* Test 3: Your test here */

    /* Test 4: Your test here */

    /* Test 5: Your test here */

    return 0;
}
```

<details>
<summary>🔍 Sample Solution</summary>

```c
int main() {
    int result;

    /* Test 1: Multiples of 2 up to 10 (2,4,6,8,10) */
    result = countMultiples(10, 2);
    print(result);  // Expected: 5

    /* Test 2: Multiples of 1 up to 5 (all numbers) */
    result = countMultiples(5, 1);
    print(result);  // Expected: 5

    /* Test 3: Multiples of 10 up to 100 (10,20,...,100) */
    result = countMultiples(100, 10);
    print(result);  // Expected: 10

    /* Test 4: Limit less than divisor (no multiples) */
    result = countMultiples(3, 5);
    print(result);  // Expected: 0

    /* Test 5: Exact multiple (20 / 5 = 4) */
    result = countMultiples(20, 5);
    print(result);  // Expected: 4

    return 0;
}
```
</details>

---

### Exercise 2: TAC Analysis (10 minutes)

**Task:** Analyze this TAC output and answer questions

**Given TAC:**
```assembly
  1: FUNC_BEGIN main
  2: DECL i
  3: DECL sum
  4: sum = 0
  5: i = 1
  6: L0:
  7: t0 = i <= 5
  8: IF_FALSE t0 GOTO L1
  9: t1 = sum + i
 10: sum = t1
 11: t2 = i + 1
 12: i = t2
 13: GOTO L0
 14: L1:
 15: PRINT sum
 16: FUNC_END main
```

**✏️ QUESTIONS:**

1. **How many times does line 9 execute?**
   - [ ] 4 times
   - [ ] 5 times
   - [ ] 6 times
   - [ ] Infinite

2. **What is the final value of sum?**
   - [ ] 10
   - [ ] 15
   - [ ] 20
   - [ ] 25

3. **Which line contains the loop exit condition?**
   - [ ] Line 6
   - [ ] Line 7
   - [ ] Line 8
   - [ ] Line 13

4. **What optimization could be applied?**
   - [ ] Constant folding on line 7
   - [ ] Dead code elimination
   - [ ] Loop-invariant code motion
   - [ ] None possible

5. **Draw the control flow:** Which lines form the loop body?

<details>
<summary>🔍 Answers</summary>

1. **5 times** - Loop runs for i=1,2,3,4,5
2. **15** - Sum = 1+2+3+4+5 = 15
3. **Line 8** - `IF_FALSE t0 GOTO L1` exits the loop
4. **None possible** - All code is necessary for this loop
5. **Loop body: Lines 9-12**
   - Line 9-10: sum += i
   - Line 11-12: i++
   - Line 13: Jump back

**Control Flow:**
```
5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → (back to 6)
                ↓
               14 → 15
```
</details>

---

### Exercise 3: Implement Loop-Invariant Code Motion (10 minutes)

**Task:** Manually optimize this code by moving invariant code out of the loop

**Given Code:**
```c
int i;
int area;
int width;
int height;

width = 10;
height = 20;
i = 0;

while (i < 1000) {
    area = width * height;     // Invariant!
    print(area);
    i = i + 1;
}
```

**✏️ YOUR TASK:**
1. Identify the loop-invariant expression
2. Rewrite the code with the optimization applied
3. Calculate how many MUL operations you saved

**Template:**
```c
int i;
int area;
int width;
int height;

width = 10;
height = 20;
i = 0;

// YOUR OPTIMIZATION HERE

while (i < 1000) {
    // MODIFIED LOOP BODY HERE
}
```

<details>
<summary>🔍 Solution</summary>

**Optimized Code:**
```c
int i;
int area;
int width;
int height;

width = 10;
height = 20;
area = width * height;    // ← Moved OUTSIDE loop
i = 0;

while (i < 1000) {
    print(area);          // ← Just use the result
    i = i + 1;
}
```

**Analysis:**
- **Invariant expression:** `width * height`
- **Operations saved:** 999 multiplications
  - Before: 1000 MUL operations
  - After: 1 MUL operation
  - Savings: 999 MUL ops! ⚡

**Why it works:**
- `width` and `height` never change inside the loop
- `area` calculation produces the same result every iteration
- Computing once and reusing is more efficient
</details>

---

<a name="part-6-challenges"></a>
## 🏆 Part 6: Advanced Challenges (Bonus)

### Challenge 1: Optimize This Code ⭐⭐

```c
int i;
int j;
int result;
int a;
int b;
int c;

a = 5;
b = 10;
c = 3;
i = 0;

while (i < 100) {
    j = 0;
    while (j < 50) {
        result = (a + b) * c;    // Multiple optimizations possible!
        print(result);
        j = j + 1;
    }
    i = i + 1;
}
```

**Questions:**
1. How many times is `(a + b) * c` computed?
2. What optimizations can be applied?
3. Rewrite with all optimizations applied

<details>
<summary>🔍 Solution</summary>

1. **Computed:** 100 × 50 = 5,000 times!

2. **Optimizations possible:**
   - Constant folding: `a + b` = 15
   - Constant folding: `15 * c` = 45
   - Loop-invariant code motion: Move entire calculation out

3. **Fully optimized:**
```c
int i;
int j;
int result;
int a;
int b;
int c;

a = 5;
b = 10;
c = 3;
result = (a + b) * c;    // Compute once: 45
i = 0;

while (i < 100) {
    j = 0;
    while (j < 50) {
        print(result);    // Just print the constant
        j = j + 1;
    }
    i = i + 1;
}
```

**Even better:** If compiler knows this prints 45 exactly 5,000 times, could unroll or optimize further!
</details>

---

### Challenge 2: Find the Bug ⭐⭐⭐

This TAC was generated for nested loops, but there's a subtle bug:

```assembly
FUNC_BEGIN main
DECL i
DECL j
i = 1
L0:
    t0 = i <= 2
    IF_FALSE t0 GOTO L1
    j = 1
    L0:                      # ← Bug is here!
        t1 = j <= 3
        IF_FALSE t1 GOTO L1  # ← And here!
        PRINT j
        t2 = j + 1
        j = t2
        GOTO L0
    L1:
    t3 = i + 1
    i = t3
    GOTO L0
L1:
FUNC_END main
```

**✏️ YOUR TASK:** Find and fix the bug!

<details>
<summary>🔍 Solution</summary>

**Bug:** Label reuse! Both loops use L0 and L1.

**Problem:**
- Inner loop's `GOTO L0` jumps to outer loop's start!
- Inner loop's `L1` is unreachable (outer loop's L1 comes first)

**Fixed Version:**
```assembly
FUNC_BEGIN main
DECL i
DECL j
i = 1
L0:                          # Outer start
    t0 = i <= 2
    IF_FALSE t0 GOTO L1      # Outer end
    j = 1
    L2:                      # Inner start (unique!)
        t1 = j <= 3
        IF_FALSE t1 GOTO L3  # Inner end (unique!)
        PRINT j
        t2 = j + 1
        j = t2
        GOTO L2              # Jump to inner start
    L3:                      # Inner end
    t3 = i + 1
    i = t3
    GOTO L0                  # Jump to outer start
L1:                          # Outer end
FUNC_END main
```

**Lesson:** Each loop MUST have unique labels!
</details>

---

### Challenge 3: Design a Stress Test ⭐⭐⭐⭐

**Task:** Create a test that:
- Uses 4 levels of nesting
- Exercises at least 10,000 iterations total
- Tests all optimization categories we discussed
- Includes expected output

**Bonus points for:**
- Creative use of arrays
- Function calls within loops
- Complex conditions

---

## 📊 Summary & Key Takeaways

### What We Learned

```
┌───────────────────────────────────────────────────────────┐
│                    KEY CONCEPTS                           │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ✓ Nested loops create complex control flow              │
│  ✓ Comprehensive testing requires multiple categories    │
│  ✓ CFG visualization helps understand execution paths    │
│  ✓ Loop optimizations can dramatically improve speed     │
│  ✓ TAC analysis reveals optimization opportunities       │
│  ✓ Label management is critical for nested structures    │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Optimization Impact

```
                PERFORMANCE GAINS

Constant Folding:     ████░░░░░░  ~10-20%
LICM:                 ██████████  ~50-90%
Dead Code Elim:       ████████░░  ~40-80%
Strength Reduction:   ██████░░░░  ~30-50%
```

### Testing Checklist

- ✅ Boundary conditions tested
- ✅ Zero iteration case tested
- ✅ Normal cases tested
- ✅ Nested loops tested
- ✅ TAC structure verified
- ✅ Optimizations identified

---

## 📝 Lab Submission

### What to Submit

1. **test_comprehensive.c** - Your comprehensive test suite
2. **analysis.txt** - TAC analysis answers
3. **optimized_code.c** - Your optimized version from Exercise 3
4. **reflection.md** - Short reflection (see below)

### Reflection Questions

Answer in 2-3 sentences each:

1. What was the most challenging part of testing nested loops?
2. Which optimization technique do you think is most impactful? Why?
3. How would you approach debugging a complex nested loop?
4. What tools or techniques would help automate loop testing?

---

## 📚 Additional Resources

- **Dragon Book:** Chapter 9 (Code Optimization)
- **Engineering a Compiler:** Section 8.5 (Loop Optimizations)
- **Online CFG Tool:** https://dreampuf.github.io/GraphvizOnline/
- **TAC Visualizer:** (Check course website)

---

## 🎯 Next Session Preview

**Coming Up:** Code Generation for Loops in MIPS Assembly
- Translating TAC to assembly
- Register allocation for loop variables
- Branch optimization in assembly
- Practical MIPS loop patterns

---

**End of Interactive Activity**

**Total Time:** ~120 minutes
**Difficulty:** Intermediate to Advanced
**Prerequisites:** Basic loop implementation complete

*Questions? Ask during office hours or post to the discussion board!*
