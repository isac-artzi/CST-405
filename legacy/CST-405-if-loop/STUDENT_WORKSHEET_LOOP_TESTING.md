# Student Worksheet: Loop Testing & Optimization

**Name:** _________________________ **Date:** _____________

**CST-405 Compiler Design - Lab Session**

---

## 📋 Instructions

This worksheet accompanies the interactive class activity. Complete each section as we progress through the material. You may work in pairs, but submit individually.

---

## Part 1: Execution Trace (10 points)

### Exercise 1A: Complete the Trace Table

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

Fill in the execution table:

| Step | i | j | Output | Next Action |
|------|---|---|--------|-------------|
| 1 | 1 | 1 | 1 | j++ |
| 2 | 1 | 2 | ___ | ___ |
| 3 | 1 | 3 | ___ | ___ |
| 4 | 2 | ___ | ___ | ___ |
| 5 | ___ | ___ | ___ | ___ |
| 6 | ___ | ___ | ___ | ___ |

**Total iterations:** ______

**Pattern observed:** _______________________________________________

---

### Exercise 1B: Label Identification

For the same code above, identify the TAC labels:

```assembly
i = 1

_______:                    # ← Outer loop start label: ___________
    t0 = i <= 2
    if_false t0 goto _______  # ← Outer loop end label: ___________

    j = 1

    _______:                # ← Inner loop start label: ___________
        t1 = j <= 3
        if_false t1 goto _______  # ← Inner loop end label: ___________

        t2 = i * j
        print t2
        t3 = j + 1
        j = t3
        goto _______        # ← This jumps to: ___________

    _______:

    t4 = i + 1
    i = t4
    goto _______            # ← This jumps to: ___________

_______:
```

**Total labels needed:** ______

**Why must labels be unique?** ________________________________________

_____________________________________________________________________

---

## Part 2: Test Case Design (20 points)

### Exercise 2A: Boundary Testing

Design a test case for each scenario:

**Test 1: Loop executes exactly 0 times**
```c
int i;
i = ______;               // Initial value

while (i _____ ______) {  // Condition that's false
    print(999);
}

print(1);                 // This should print
```

**Expected output:** ________________


**Test 2: Loop executes exactly 1 time**
```c
int i;
i = ______;               // Initial value

while (i _____ ______) {  // Condition
    print(i);
    i = i + 1;
}
```

**Expected output:** ________________


**Test 3: Loop with boundary condition (off-by-one test)**
```c
int i;
i = 1;

while (i _____ 5) {       // Should this be < or <= ?
    print(i);
    i = i + 1;
}

// Goal: Print exactly 1,2,3,4,5
```

**Correct condition:** ______________

**Why?** ____________________________________________________________

---

### Exercise 2B: Accumulator Testing

Complete this test for calculating sum of 1 to N:

```c
int sum;
int i;
int n;

n = ______;              // Choose a value
sum = ______;            // Initial sum
i = ______;              // Initial counter

while (i _____ n) {      // Condition
    sum = ____________;  // Update sum
    i = ______________;  // Update counter
}

print(sum);
```

**Expected output:** ________________

**Verification formula:** n(n+1)/2 = ________________

**Does your output match?** Yes / No

---

## Part 3: Control Flow Analysis (15 points)

### Exercise 3A: Draw the CFG

Draw the Control Flow Graph for this code:

```c
int i;
i = 0;
while (i < 3) {
    if (i > 0) {
        print(100);
    }
    i = i + 1;
}
```

**Your CFG Drawing:**
```
     Entry
       |
       v
   [ i = 0 ]
       |
       v



   (Draw CFG here using boxes and arrows)




       |
       v
     Exit
```

**How many decision points?** ______

**How many possible paths?** ______

---

### Exercise 3B: Path Coverage

List all unique paths through the CFG you drew:

**Path 1:** ________________________________________________________

**Path 2:** ________________________________________________________

**Path 3:** ________________________________________________________

**Path 4:** ________________________________________________________

**Which paths test the TRUE branch of the if?** ____________________

**Which paths test the FALSE branch of the if?** ___________________

---

## Part 4: Optimization Analysis (25 points)

### Exercise 4A: Identify Loop-Invariant Code

Mark ALL loop-invariant expressions in this code with ✓:

```c
int i;
int result;
int a;
int b;
int c;

a = 10;
b = 20;
c = 5;
i = 0;

while (i < 100) {
    result = a + b;        [ ]  Loop-invariant?
    result = result * c;   [ ]  Loop-invariant?
    print(result);         [ ]  Loop-invariant?
    i = i + 1;            [ ]  Loop-invariant?
}
```

**Expressions to move out:** _______________________________________

**Why can these be moved?** ________________________________________

_____________________________________________________________________

---

### Exercise 4B: Apply Optimization

Rewrite the code above with optimizations applied:

```c
int i;
int result;
int a;
int b;
int c;

a = 10;
b = 20;
c = 5;
i = 0;

// YOUR OPTIMIZATIONS HERE:




while (i < 100) {
    // MODIFIED LOOP BODY:




}
```

**How many operations saved?** ______

**Calculation:** ____________________________________________________

---

### Exercise 4C: Constant Folding

Apply constant folding to this TAC:

**Before:**
```assembly
L0:
    t0 = 5 + 3              # ← Can fold to: ____________
    t1 = i < t0
    if_false t1 goto L1
    print i
    t2 = i + 1
    i = t2
    goto L0
L1:
```

**After (optimized):**
```assembly
L0:
    t0 = i < ______         # ← Folded constant here
    if_false t0 goto L1
    print i
    t1 = i + 1
    i = t1
    goto L0
L1:
```

**Operation eliminated:** ___________________________________________

---

## Part 5: Debugging Practice (15 points)

### Exercise 5A: Find the Bug

This test should print the sum of even numbers 2 through 10, but it's wrong:

```c
int sum;
int i;

sum = 0;
i = 2;

while (i < 10) {          // ← Bug somewhere near here?
    sum = sum + i;
    i = i + 2;
}

print(sum);
// Expected: 30 (2+4+6+8+10)
// Actually prints: 20
```

**What's the bug?** ________________________________________________

**How to fix it?** _________________________________________________

**Corrected condition:** ___________________________________________

---

### Exercise 5B: TAC Debugging

This TAC has a bug that causes wrong label jumps:

```assembly
DECL i
DECL j
i = 1
L0:
    t0 = i <= 2
    IF_FALSE t0 GOTO L1

    j = 1
    L0:                      # ← Something wrong here?
        t1 = j <= 2
        IF_FALSE t1 GOTO L1  # ← And here?
        PRINT j
        j = j + 1
        GOTO L0
    L1:

    i = i + 1
    GOTO L0
L1:
```

**Problem identified:** ____________________________________________

**Fix:** ___________________________________________________________

**Corrected labels:**

- Outer loop start: ___________
- Outer loop end: ___________
- Inner loop start: ___________
- Inner loop end: ___________

---

## Part 6: Lab Exercises (15 points)

### Exercise 6A: Design Test Suite

For this function, write 3 test cases:

```c
int countDivisible(int limit, int divisor) {
    int count;
    int i;

    count = 0;
    i = 1;

    while (i <= limit) {
        if (i % divisor == 0) {  // Note: % is modulo (remainder)
            count = count + 1;
        }
        i = i + 1;
    }

    return count;
}
```

**Test Case 1:**
```c
result = countDivisible(______, ______);
// Expected: ______
// Rationale: _________________________________________________
```

**Test Case 2:**
```c
result = countDivisible(______, ______);
// Expected: ______
// Rationale: _________________________________________________
```

**Test Case 3:**
```c
result = countDivisible(______, ______);
// Expected: ______
// Rationale: _________________________________________________
```

---

### Exercise 6B: Optimization Challenge

Optimize this code (hint: multiple optimizations possible):

**Original:**
```c
int i;
int j;
int result;
int x;
int y;

x = 7;
y = 3;
i = 0;

while (i < 50) {
    j = 0;
    while (j < 20) {
        result = x * y;      // ← Optimize this
        print(result);
        j = j + 1;
    }
    i = i + 1;
}
```

**Your Optimized Version:**
```c
int i;
int j;
int result;
int x;
int y;

x = 7;
y = 3;

// YOUR OPTIMIZATIONS:







while (i < 50) {




}
```

**Operations saved:** _______________

**Percentage improvement:** _______________

---

## Reflection Questions (Bonus +5 points)

Answer in complete sentences:

**1. What was the most challenging concept in this lab?**

_____________________________________________________________________

_____________________________________________________________________

_____________________________________________________________________


**2. How does understanding TAC help you write better optimizations?**

_____________________________________________________________________

_____________________________________________________________________

_____________________________________________________________________


**3. If you had to explain nested loops to a classmate, what analogy would you use?**

_____________________________________________________________________

_____________________________________________________________________

_____________________________________________________________________


**4. What optimization surprised you the most in terms of performance impact?**

_____________________________________________________________________

_____________________________________________________________________

_____________________________________________________________________

---

## Summary Checklist

Before submitting, verify you've completed:

- [ ] Part 1: Execution trace table
- [ ] Part 1: Label identification
- [ ] Part 2: All 3 boundary tests
- [ ] Part 2: Accumulator test
- [ ] Part 3: CFG drawing
- [ ] Part 3: Path coverage analysis
- [ ] Part 4: Loop-invariant identification
- [ ] Part 4: Optimization implementation
- [ ] Part 4: Constant folding
- [ ] Part 5: Both debugging exercises
- [ ] Part 6: Test suite design
- [ ] Part 6: Optimization challenge
- [ ] Reflection questions (bonus)

---

## Grading Rubric

| Section | Points | Your Score |
|---------|--------|------------|
| Part 1: Execution Trace | 10 | _____ |
| Part 2: Test Design | 20 | _____ |
| Part 3: Control Flow | 15 | _____ |
| Part 4: Optimization | 25 | _____ |
| Part 5: Debugging | 15 | _____ |
| Part 6: Lab Exercises | 15 | _____ |
| **Total** | **100** | _____ |
| Bonus: Reflection | +5 | _____ |
| **Final Score** | **105** | _____ |

---

## Submission

**Submit this worksheet plus:**
1. `test_comprehensive.c` - Your test file from Exercise 6A
2. `optimized_code.c` - Your optimized code from Exercise 6B
3. `analysis.txt` - Written answers to reflection questions

**Due:** ________________

**Submit to:** Canvas Assignment "Loop Testing & Optimization Lab"

---

**Notes & Observations:**

(Use this space for any additional notes, observations, or questions)

_____________________________________________________________________

_____________________________________________________________________

_____________________________________________________________________

_____________________________________________________________________

_____________________________________________________________________
