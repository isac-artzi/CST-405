# Instructor Guide: Loop Testing & Optimization

**CST-405 Compiler Design**
**Session Duration:** 120 minutes
**Format:** Interactive Lecture + Lab

---

## 📋 Session Overview

### Learning Outcomes
Students will be able to:
1. Trace execution of nested loops manually
2. Design comprehensive test suites for loop implementations
3. Analyze TAC for correctness and optimization opportunities
4. Identify and apply common loop optimizations
5. Debug complex control flow issues

### Materials Needed
- [ ] Projector for presentation
- [ ] Whiteboard/markers for diagrams
- [ ] Student worksheets (printed)
- [ ] Sample code files (on shared drive)
- [ ] TAC examples (handout or projected)
- [ ] Access to compiler environment

### Pre-Class Setup
1. Test all code examples compile correctly
2. Prepare TAC output files for examples
3. Load presentation slides
4. Set up live coding environment
5. Prepare polling/quiz questions (if using clickers)

---

## ⏱️ Detailed Lesson Plan

### Introduction (10 minutes)

#### Opening Hook
> "Last week you implemented while loops. Today, we stress-test them and make them faster. By the end of class, you'll find optimizations that eliminate 99% of computations in some loops!"

#### Learning Objectives Review
Project and read aloud:
- Understanding nested loops
- Testing strategies
- Control flow analysis
- Loop optimizations

#### Pre-Assessment Question
**Show on screen:** "How many labels are needed for 3 nested while loops?"
- Take votes (show of hands)
- Answer: 6 (each loop needs start + end)
- Use this to gauge understanding

**Transition:** "Let's see why..."

---

### Part 1: Understanding Nested Loops (20 minutes)

#### 1.1 Visual Model (5 minutes)

**SHOW:** Box diagram of nested loops from slide 1
- Walk through outer → inner → back to outer flow
- **Point:** Use pointer to trace execution path

**Interactive element:**
> "Everyone, put your finger on 'Outer: Initialize i=1' and trace with me..."

**Live Demo:**
```c
int i = 1;
while (i <= 2) {
    int j = 1;
    while (j <= 3) {
        printf("%d ", i*j);
        j++;
    }
    i++;
}
```

- Compile and run in real-time
- Show output: `1 2 3 2 4 6`
- **Ask:** "Why 6 numbers?"

#### 1.2 TAC Structure (8 minutes)

**SHOW:** TAC slide for nested loops

**Teaching Tip:** Use different colors for each loop level
- Green highlight: Outer loop (L0, L1)
- Blue highlight: Inner loop (L2, L3)

**Live TAC Generation:**
- Run compiler on example
- Project TAC output
- **Point out:**
  - 4 distinct labels
  - 2 IF_FALSE instructions
  - 2 GOTO instructions
  - Nesting structure

**Common Student Question:**
> "Why can't we reuse labels?"

**Answer with example:** Show what happens with duplicate labels (infinite loop or crash)

#### 1.3 Student Exercise (7 minutes)

**DISTRIBUTE:** Worksheet Part 1
- Students fill in execution trace table
- **Walk around:** Check progress, answer questions

**After 5 minutes:**
- Show solution on projector
- **Ask:** "Who got 6 iterations?" (show of hands)
- Discuss any confusion

**Key Teaching Points:**
- Inner loop completes fully before outer continues
- Loop variables must be independent
- Total iterations = outer × inner

---

### Part 2: Testing Strategies (25 minutes)

#### 2.1 The Testing Pyramid (3 minutes)

**SHOW:** Pyramid diagram

**Analogy:**
> "Testing is like building security. You need multiple layers. If one test misses a bug, another catches it."

**Real-world example:**
> "Mars Climate Orbiter crashed due to unit conversion bug. Proper testing pyramid would have caught it!"

#### 2.2 Boundary Tests (8 minutes)

**SHOW:** Code for 0-iteration test

**Think-Pair-Share:**
1. **Think (1 min):** "What should this output?"
2. **Pair (2 min):** Discuss with neighbor
3. **Share:** Call on 2-3 students

**Live Demo:**
- Run the code
- Show it prints only 100, not 999
- **Explain:** Condition false from start

**Interactive Coding:**
> "Now let's create a bug. What if I change `<` to `<=`?"
- Make change live
- Run again
- **Discuss:** How did output change? Why?

#### 2.3 Accumulator Tests (7 minutes)

**SHOW:** Sum 1 to N code

**Math Connection:**
> "This is Gauss's formula: n(n+1)/2. At age 7, Gauss summed 1 to 100 in seconds using this!"

**Verification Strategy:**
- Show formula: 10(11)/2 = 55
- Run code, verify output matches
- **Teaching moment:** Always have independent verification

**Challenge Question:**
> "What if the loop had `i = i + 2` instead?"
- Answer: Only odd numbers, different formula needed

#### 2.4 Nested Loop Tests (7 minutes)

**SHOW:** 3x3 grid example

**Visual Aid:** Draw grid on whiteboard
```
00  01  02
10  11  12
20  21  22
```

**Pattern Recognition:**
> "Notice the pattern? First digit is row, second is column."

**Student Activity:**
- Project triple-nested loop code
- **Ask:** "How many outputs?"
- Give 30 seconds to calculate
- Answer: 2×2×2 = 8

**Live Run:** Execute and count together

---

### Part 3: Control Flow Analysis (20 minutes)

#### 3.1 CFG Introduction (5 minutes)

**SHOW:** Simple while loop CFG

**Drawing Technique:**
> "CFGs are roadmaps of your code. Boxes are actions, arrows are decisions."

**Components:**
- Boxes = statements
- Diamonds = conditions
- Arrows = control flow

**Real-world analogy:**
> "Like GPS navigation: you start, check conditions at each turn, follow paths."

#### 3.2 Nested Loop CFG (7 minutes)

**SHOW:** Nested loop CFG slide

**Interactive Tracing:**
- Use laser pointer to trace one complete execution
- **Ask student to come up:** Trace a different path
- Class verifies correctness

**Complexity Discussion:**
> "Notice how quickly CFGs get complex. Imagine 4 nested loops!"

#### 3.3 Path Coverage (8 minutes)

**SHOW:** Code with if inside while

**Worksheet Time:**
- Students draw CFG (Part 3A)
- **Time:** 5 minutes
- Circulate to help

**Solution Review:**
- Project correct CFG
- Count decision points together
- List all paths as a class

**Discussion:**
> "Why can't we test every path in large programs?"
- Answer: Exponential growth
- Need smart testing strategies

---

### BREAK (10 minutes)

Announce: "10-minute break. Back at [TIME]"

---

### Part 4: Loop Optimizations (30 minutes)

#### 4.1 Why Optimize? (5 minutes)

**SHOW:** Pie chart of execution time

**Dramatic Statement:**
> "90% of your program's time is in loops. Optimize loops, optimize everything!"

**Real Example:**
> "Google saves millions in server costs through loop optimization. Each 1% improvement = $millions saved."

**Interactive Poll:**
> "Raise hand if you think optimizations matter only for huge programs?"
- Address misconception: Optimizations matter at all scales

#### 4.2 Constant Folding (7 minutes)

**SHOW:** Before/after TAC for constant folding

**Live Optimization:**
1. Start with unoptimized TAC
2. Circle the `2 + 3` in red
3. **Ask:** "What's 2 + 3?"
4. Replace with 5 in optimized version

**Impact Calculation:**
```
Before: N iterations × 1 ADD = N operations
After:  1 ADD (compile time) = 1 operation
Savings: N - 1 operations
```

**For N=1000:** 999 operations saved!

**Student Misconception Alert:**
> "But addition is fast!"

**Response:**
> "Yes, but happens 1000 times. Also, enables other optimizations."

#### 4.3 Loop-Invariant Code Motion (10 minutes)

**SHOW:** LICM example code

**Discovery Learning:**
- **Ask:** "What values change inside the loop?"
  - i changes
  - result changes (assigned)
- **Ask:** "What values DON'T change?"
  - a, b don't change
  - a + b always same!

**Eureka Moment:**
> "We're computing the same thing 100 times! Move it out!"

**Show Optimized Version:**
- Highlight moved code
- Count operations saved: 99 ADDs + 99 MULs = 198 ops!

**CRITICAL TEACHING POINT:**
> "LICM is the most impactful optimization you'll learn. Remember it!"

**Common Student Error:**
> "Can I move `i = i + 1` out?"

**Answer:** No! It changes each iteration (not invariant).

#### 4.4 Dead Loop Elimination (5 minutes)

**SHOW:** `while (0)` example

**Obvious Question:**
> "Why would anyone write this?"

**Real Scenario:**
- Debugging (commented out)
- Conditional compilation
- Code generation errors
- After other optimizations

**Show Transformation:**
- Cross out entire loop in red
- "Compiler deletes this at compile time"

#### 4.5 Strength Reduction (3 minutes)

**SHOW:** Multiplication to addition example

**Key Insight:**
> "Multiplication: ~5-10 cycles. Addition: 1 cycle. Big difference in tight loops!"

**Pattern:**
```
i * 5 becomes:
0, 5, 10, 15, 20, ... (just add 5 each time!)
```

**Advanced Note:**
> "Modern compilers do this automatically. But you should know WHY."

---

### Part 5: Hands-on Lab (30 minutes)

#### Setup (2 minutes)

**Instructions:**
1. Open worksheet Part 5
2. Open code editor
3. Access sample files on shared drive
4. Work individually or in pairs

**Remind:** "Pairs discuss, but submit individually"

#### Exercise 1: Test Suite Design (10 minutes)

**Circulate:** Help students who are stuck

**Common Issues to Watch For:**
- Not covering edge cases (limit=0, divisor=1)
- Off-by-one errors in expected output
- Not explaining rationale

**Checkpoint at 5 minutes:**
> "Everyone should have at least 2 test cases by now."

**Early Finishers:**
> "Try to break the function. What inputs cause problems?"

#### Exercise 2: TAC Analysis (8 minutes)

**Show TAC on projector**

**Guided Analysis:**
- Read together as a class
- **Ask:** "What's the first instruction that executes?"
- Trace through one iteration together

**Questions:**
- Poll class on multiple choice questions
- Discuss common wrong answers

**Teaching Moment:**
> "Notice how TAC makes control flow explicit. No hidden jumps!"

#### Exercise 3: LICM Implementation (10 minutes)

**Before Students Start:**
> "Look for code that gives same result every iteration."

**Hint Progression:**
- After 2 minutes: "What variables never change?"
- After 4 minutes: "Can width × height move?"
- After 6 minutes: Show first step

**Solution Review:**
- Project corrected code
- Calculate savings together
- **Emphasize:** 999 operations saved = 99.9% improvement!

**Extension Question:**
> "What if width and height could change between loop runs? Can we still optimize?"

---

### Part 6: Advanced Challenges (10 minutes)

**For Early Finishers:**

**Challenge 1:** Project on screen
- Students work independently
- Circulate to see approaches

**Challenge 2:** Debugging exercise
- Hint: "Look at label names"
- Give students time to discover

**Share Solutions:**
- If time permits, have student present their solution
- Or project solution and explain

---

### Wrap-Up & Summary (5 minutes)

#### Key Takeaways

**Ask Students:**
> "What's the most important thing you learned today?"
- Call on 3-4 students
- Synthesize responses

#### Concept Review

**Quick Quiz (optional):**
1. How many labels for 2 nested loops? (4)
2. Best optimization for invariant expressions? (LICM)
3. What does CFG stand for? (Control Flow Graph)

#### Preview Next Session

> "Next class: We translate these optimized loops to MIPS assembly. You'll see how TAC makes code generation easier!"

#### Assignment Reminder

**Show on screen:**
- Worksheet due: [DATE]
- Test files due: [DATE]
- Submit to Canvas
- Office hours: [TIMES]

#### Questions?

Leave 2-3 minutes for questions.

---

## 📊 Assessment Notes

### Formative Assessment Checkpoints

Throughout class, gauge understanding:

| Time | Check | Method | If Struggling |
|------|-------|--------|---------------|
| 15 min | Nested loop concept | Show of hands | Re-explain with simpler example |
| 35 min | Testing categories | Quick quiz | Review pyramid |
| 55 min | CFG reading | Student draws | Pair with strong student |
| 75 min | LICM concept | Poll | Show more examples |

### Common Misconceptions

**Misconception 1:** "Nested loops share labels"
- **Correction:** Each loop needs unique labels
- **Evidence:** Show broken TAC

**Misconception 2:** "All code in loop can be moved out"
- **Correction:** Only invariant expressions
- **Evidence:** Counter-example with i++

**Misconception 3:** "Optimizations don't matter for small programs"
- **Correction:** Good habits + understanding matters
- **Evidence:** Real-world performance data

**Misconception 4:** "More nesting = more efficient"
- **Correction:** More nesting = more complex, not more efficient
- **Evidence:** Complexity analysis

### Individual Student Tracking

Watch for students who:
- ✓ Finish quickly (give extensions)
- ✗ Struggle with traces (offer 1-on-1 help)
- ⚠ Get stuck on CFGs (pair them up)
- 🌟 Show exceptional understanding (recommend advanced reading)

---

## 🎯 Solutions to All Exercises

### Student Worksheet Solutions

#### Part 1: Execution Trace

| Step | i | j | Output | Next Action |
|------|---|---|--------|-------------|
| 1 | 1 | 1 | 1 | j++ |
| 2 | 1 | 2 | 2 | j++ |
| 3 | 1 | 3 | 3 | j=4, exit inner, i++ |
| 4 | 2 | 1 | 2 | j++ |
| 5 | 2 | 2 | 4 | j++ |
| 6 | 2 | 3 | 6 | j=4, exit inner, i++ |

Labels: L0, L1 (outer), L2, L3 (inner) - Total: 4 labels

---

#### Part 2A: Boundary Tests

**Test 1:** Zero iterations
```c
int i;
i = 10;
while (i < 5) {
    print(999);
}
print(1);
```
Output: 1

**Test 2:** One iteration
```c
int i;
i = 1;
while (i <= 1) {
    print(i);
    i = i + 1;
}
```
Output: 1

**Test 3:** Boundary
```c
int i;
i = 1;
while (i <= 5) {  // Must use <=
    print(i);
    i = i + 1;
}
```
Output: 1 2 3 4 5

---

#### Part 2B: Accumulator

```c
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

print(sum);
```
Output: 55
Verification: 10(11)/2 = 55 ✓

---

#### Part 3A: CFG

```
     ┌──────────┐
     │  Entry   │
     └────┬─────┘
          ↓
     ┌──────────┐
     │  i = 0   │
     └────┬─────┘
          ↓
     ┌──────────┐
  ┌──│ i < 3?   │──┐
  │  └──────────┘  │
  │                │
true│           false│
  ↓                ↓
┌──────────┐  ┌──────────┐
│ i > 0?   │  │   Exit   │
└─┬───┬────┘  └──────────┘
  │   │
T │   │ F
  ↓   ↓
┌─────┐│
│print││
│100  ││
└─┬───┘│
  │    │
  └──┬─┘
     ↓
┌──────────┐
│ i = i+1  │
└────┬─────┘
     │
     └──┐
        ↓
   (back to i<3?)
```

Decision points: 2 (i < 3, i > 0)
Possible paths: 4

---

#### Part 4A: Loop-Invariant Identification

```c
result = a + b;        [✓]  Invariant - a,b don't change
result = result * c;   [✓]  Invariant - uses previous invariant
print(result);         [✗]  Not code (it's I/O)
i = i + 1;            [✗]  Not invariant - i changes
```

---

#### Part 4B: Optimized Code

```c
int i;
int result;
int a;
int b;
int c;

a = 10;
b = 20;
c = 5;
result = (a + b) * c;  // = 150, computed once
i = 0;

while (i < 100) {
    print(result);      // Just use the value
    i = i + 1;
}
```

Operations saved:
- Before: 100 ADD + 100 MUL = 200 operations
- After: 1 ADD + 1 MUL = 2 operations
- Saved: 198 operations (99% reduction!)

---

#### Part 4C: Constant Folding

After optimization:
```assembly
L0:
    t0 = i < 8          # Folded: 5+3=8
    if_false t0 goto L1
    print i
    t1 = i + 1
    i = t1
    goto L0
L1:
```

Operation eliminated: ADD (5+3) inside loop

---

#### Part 5A: Bug Fix

Bug: Condition should be `i <= 10` not `i < 10`
Fix: Change to `while (i <= 10)`
Reason: Need to include 10 in the sum

---

#### Part 5B: TAC Debugging

Problem: Duplicate labels L0 and L1
Fix:
```assembly
L0:    # Outer start
L1:    # Outer end
L2:    # Inner start
L3:    # Inner end
```

---

### Advanced Challenge Solutions

#### Challenge 1: Nested Optimization

Computed: 100 × 50 = 5,000 times

Optimizations:
1. Constant folding: a=5, b=10, c=3
2. LICM: Move (a+b)*c out of loops
3. Result: Constant 45

```c
result = (a + b) * c;  // = 45
while (i < 100) {
    while (j < 50) {
        print(result);
        j++;
    }
    i++;
}
```

---

#### Challenge 2: Label Bug

Fixed TAC uses unique labels:
- Outer: L0, L1
- Inner: L2, L3

Each goto/if_false references correct label.

---

## 📝 Grading Guidelines

### Worksheet Grading

**Full Credit Criteria:**
- All calculations correct
- Shows work/reasoning
- Tests are comprehensive
- Optimizations correctly applied

**Partial Credit:**
- Minor arithmetic errors: -1 per error
- Incomplete reasoning: -2 points
- Missing test case: -3 points
- Wrong optimization but right idea: -2 points

### Code Submissions

**Test Files:**
- Compiles without errors: 5 pts
- Tests cover all categories: 10 pts
- Expected outputs documented: 5 pts

**Optimized Code:**
- Correctly optimized: 10 pts
- Compiles and runs: 5 pts
- Savings calculated correctly: 5 pts

---

## 🔧 Troubleshooting

### Common Technical Issues

**Issue:** Compiler errors when running examples
- **Fix:** Check compiler flags, ensure up-to-date

**Issue:** TAC output not displaying
- **Fix:** Redirect to file, then display: `./compiler input.c > tac.txt`

**Issue:** Students can't access shared files
- **Fix:** Upload to Canvas as backup

### Classroom Management

**Issue:** Students finish too quickly
- **Solution:** Have extension challenges ready

**Issue:** Students fall behind
- **Solution:** Pair with stronger student or offer office hours

**Issue:** Technical difficulties with projector
- **Solution:** Have printed handouts as backup

---

## 📚 Additional Resources for Students

### Recommended Reading
- Dragon Book: Chapter 9, Sections 9.1-9.4
- Engineering a Compiler: Section 8.5

### Online Resources
- CFG Visualizer: https://dreampuf.github.io/GraphvizOnline/
- TAC Tutorial: (course website)
- Loop Optimization Examples: (course repository)

### Practice Problems
- Additional worksheets on Canvas
- Past exam questions
- Online coding challenges (link on syllabus)

---

## 📅 Post-Class Follow-Up

### Office Hours Topics
Be prepared to discuss:
- CFG drawing techniques
- LICM edge cases
- Complex nested loop debugging
- Optimization tradeoffs

### Next Session Prep
- Review MIPS assembly basics
- Prepare code generation examples
- Set up MARS simulator
- Create register allocation visuals

### Student Feedback
After class, note:
- Which concepts need more time?
- Which examples worked well?
- What questions came up repeatedly?
- How to improve for next semester?

---

**End of Instructor Guide**

---

## Quick Reference: Timing Summary

```
┌─────────────────────────────────────────────────────┐
│  0:00 - 0:10  │  Introduction                       │
│  0:10 - 0:30  │  Part 1: Nested Loops              │
│  0:30 - 0:55  │  Part 2: Testing Strategies        │
│  0:55 - 1:15  │  Part 3: Control Flow              │
│  1:15 - 1:25  │  BREAK                             │
│  1:25 - 1:55  │  Part 4: Optimizations             │
│  1:55 - 2:25  │  Part 5: Lab Exercises             │
│  2:25 - 2:35  │  Part 6: Advanced Challenges       │
│  2:35 - 2:40  │  Wrap-up & Questions               │
└─────────────────────────────────────────────────────┘
Total: 2 hours 40 minutes (includes 10-min break)
```

**Adjust timing based on class pace and engagement!**
