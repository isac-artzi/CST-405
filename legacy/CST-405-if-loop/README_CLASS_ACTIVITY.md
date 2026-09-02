# WHILE Loops Class Activity - Package Contents

This directory contains a complete educational package for teaching students how to implement WHILE loops in a compiler.

---

## 📚 Materials Overview

### For Students

| File | Purpose | When to Use |
|------|---------|-------------|
| **CLASS_ACTIVITY_WHILE_LOOPS.md** | Main assignment handout | Give at start of activity |
| **WHILE_LOOPS_QUICK_REFERENCE.md** | Quick reference card | Keep open during coding |
| **test_while_simple.c** | Basic test case | First test to verify implementation |
| **test_while_sum.c** | Accumulation test | Second test for correctness |
| **test_while_nested.c** | Nested loops test | Advanced test for nested loops |

### For Instructors

| File | Purpose | When to Use |
|------|---------|-------------|
| **SOLUTION_GUIDE_WHILE_LOOPS.md** | Complete solutions | Grading reference, answer key |
| **WHILE_LOOP_IMPLEMENTATION.md** | Implementation notes | Background reading |

### Test Files

All test files are ready to use and include:
- ✓ Clear comments explaining what they test
- ✓ Expected output documented
- ✓ Progressive difficulty (simple → complex)

---

## 🎯 Recommended Class Schedule

### Total Time: 90-120 minutes

```
[10 min] Introduction & Background
         - Explain while loop control flow
         - Show TAC structure on board
         - Distribute CLASS_ACTIVITY_WHILE_LOOPS.md

[15 min] Part 1-2: Lexer & Parser (Guided)
         - Walk through together as a class
         - Students modify scanner.l and parser.y
         - Verify compilation works

[30 min] Part 3: AST Implementation (Independent)
         - Students work on ast.h and ast.c
         - Instructor circulates to help
         - Students verify with printAST()

[35 min] Part 4: TAC Generation (Critical Section)
         - Brief review of control flow
         - Students implement TAC generation
         - This is the hardest part - allow time!

[20 min] Part 5: Testing & Debugging
         - Students run test cases
         - Debug issues
         - Compare TAC output

[10 min] Wrap-up & Discussion
         - Discuss common mistakes
         - Preview next topic (code generation)
```

---

## 📖 Learning Progression

### Phase 1: Recognition (Easy)
Students learn to recognize and parse `while` syntax.
- **Files Modified:** scanner.l, parser.y
- **Difficulty:** ⭐☆☆☆☆
- **Expected Errors:** Token not defined, syntax errors

### Phase 2: Representation (Medium)
Students create AST nodes to represent while loops.
- **Files Modified:** ast.h, ast.c
- **Difficulty:** ⭐⭐⭐☆☆
- **Expected Errors:** Struct definition errors, malloc issues

### Phase 3: Translation (Hard)
Students generate TAC with proper control flow.
- **Files Modified:** tac.c
- **Difficulty:** ⭐⭐⭐⭐☆
- **Expected Errors:** Label confusion, missing goto, wrong jump condition

---

## 🧪 Test Cases Explained

### Test 1: Simple Counter (`test_while_simple.c`)
**Purpose:** Verify basic loop functionality
**Key Concepts:**
- Loop counter initialization
- Condition checking
- Variable increment
- Loop termination

**Common Issues:**
- Loop executes forever (forgot increment)
- Loop doesn't execute (condition wrong)
- Off-by-one errors

### Test 2: Sum Accumulation (`test_while_sum.c`)
**Purpose:** Test loop variable accumulation
**Key Concepts:**
- Accumulator pattern
- Multiple variable updates in loop
- Correct final result (55)

**Common Issues:**
- Wrong sum (logic error in TAC)
- Temporary variables not freed

### Test 3: Nested Loops (`test_while_nested.c`)
**Purpose:** Verify nested loop control flow
**Key Concepts:**
- Label uniqueness
- Inner/outer loop independence
- Multiple loop variables

**Common Issues:**
- Label conflicts
- Inner loop affects outer loop variable
- Wrong nesting order

---

## 🎓 Teaching Tips

### Before Class
1. ✓ Test the solution yourself
2. ✓ Print quick reference cards for students
3. ✓ Have solution guide ready for questions
4. ✓ Set up projector to show TAC examples

### During Class
1. **Draw on board:** Show control flow diagram
2. **Live demo:** Compile and show TAC for simple example
3. **Pair programming:** Students work in pairs
4. **Checkpoint:** Check everyone's progress after each phase
5. **Common errors:** Share solutions to frequent mistakes

### After Class
1. Collect submissions
2. Run test cases to verify correctness
3. Grade using rubric in CLASS_ACTIVITY_WHILE_LOOPS.md
4. Provide feedback on common issues

---

## 🐛 Common Student Mistakes & Solutions

### Mistake 1: "My loop only executes once"
**Cause:** Missing `goto` back to start
**Fix:** Check Step 5 in TAC generation
```c
appendTAC(createTAC(TAC_GOTO, labelStart, NULL, NULL));
```

### Mistake 2: "My loop never exits"
**Cause:** Loop variable not updated, or wrong condition
**Fix:** Verify body updates the loop counter
```c
i = i + 1;  // Make sure this is in the loop body!
```

### Mistake 3: "Nested loops don't work"
**Cause:** Reusing same labels
**Fix:** Each loop needs unique labels from `newLabel()`
```c
// WRONG: Hardcoded labels
appendTAC(createTAC(TAC_LABEL, NULL, NULL, "L0"));

// RIGHT: Generated unique labels
char* labelStart = newLabel();
appendTAC(createTAC(TAC_LABEL, NULL, NULL, labelStart));
```

### Mistake 4: "Compiler crashes on while loop"
**Cause:** NULL pointer, memory error
**Fix:** Check malloc returns in createWhileNode()

### Mistake 5: "TAC shows wrong jump direction"
**Cause:** Used IF_TRUE instead of IF_FALSE
**Fix:** Use IF_FALSE to exit loop
```c
// WRONG: Exits when condition is TRUE
appendTAC(createTAC(TAC_IF_TRUE, cond, labelEnd, NULL));

// RIGHT: Exits when condition is FALSE
appendTAC(createTAC(TAC_IF_FALSE, cond, labelEnd, NULL));
```

---

## ✅ Grading Checklist

Use this when grading student submissions:

### Functionality (70 points)
- [ ] Scanner recognizes `while` keyword (10 pts)
- [ ] Parser rule correctly parses while syntax (15 pts)
- [ ] AST node created with condition and body (15 pts)
- [ ] TAC generates correct structure (30 pts)
  - [ ] Start label emitted
  - [ ] Condition evaluated
  - [ ] IF_FALSE jumps to end
  - [ ] Body code generated
  - [ ] GOTO jumps to start
  - [ ] End label emitted

### Testing (20 points)
- [ ] test_while_simple.c works (5 pts)
- [ ] test_while_sum.c works (10 pts)
- [ ] test_while_nested.c works (5 pts)

### Code Quality (10 points)
- [ ] Code compiles without warnings (3 pts)
- [ ] Appropriate comments (3 pts)
- [ ] Proper memory management (2 pts)
- [ ] Clean, readable code (2 pts)

**Bonus:**
- [ ] DO-WHILE implementation (+5 pts)
- [ ] FOR loop implementation (+5 pts)
- [ ] BREAK statement (+10 pts)

---

## 📊 Assessment Rubric

### Excellent (90-100)
- All tests pass
- TAC is correct and efficient
- Code is clean and well-documented
- Shows deep understanding of control flow

### Good (80-89)
- All or most tests pass
- TAC is mostly correct with minor issues
- Code works but may have style issues
- Demonstrates solid understanding

### Satisfactory (70-79)
- Basic tests pass
- TAC has some logical errors
- Code works but has significant issues
- Shows basic understanding

### Needs Improvement (60-69)
- Only simple test passes
- TAC structure incomplete
- Code has major bugs
- Limited understanding

### Unsatisfactory (<60)
- Tests fail
- TAC incorrect or missing
- Code doesn't compile
- Fundamental misunderstandings

---

## 🔧 Setup Instructions

### For Students
1. Download all files from this directory
2. Place test files in your project directory
3. Follow CLASS_ACTIVITY_WHILE_LOOPS.md step by step
4. Use WHILE_LOOPS_QUICK_REFERENCE.md as a guide
5. Test with provided .c files

### For Instructors
1. Review SOLUTION_GUIDE_WHILE_LOOPS.md
2. Print student handouts:
   - CLASS_ACTIVITY_WHILE_LOOPS.md
   - WHILE_LOOPS_QUICK_REFERENCE.md
3. Set up example compiler project
4. Prepare to demo TAC generation
5. Have debugging environment ready

---

## 📝 Files Summary

```
CLASS_ACTIVITY_WHILE_LOOPS.md      - Main student handout (8 pages)
SOLUTION_GUIDE_WHILE_LOOPS.md      - Instructor solutions (15 pages)
WHILE_LOOPS_QUICK_REFERENCE.md     - Student cheat sheet (4 pages)
test_while_simple.c                - Basic test case
test_while_sum.c                   - Accumulation test case
test_while_nested.c                - Nested loops test case
README_CLASS_ACTIVITY.md           - This file
```

---

## 🚀 Extensions & Future Work

After students complete this activity, they can:

1. **Implement FOR loops**
   - Desugar into while loops
   - Practice syntactic sugar concepts

2. **Add BREAK and CONTINUE**
   - Teach about jump targets
   - Loop label stack management

3. **Optimize loops**
   - Constant condition elimination
   - Loop unrolling
   - Loop invariant code motion

4. **Add DO-WHILE**
   - Different control flow pattern
   - Condition at end instead of start

---

## 📧 Support

For questions or issues:
- **Instructor Office Hours:** [Fill in]
- **Discussion Board:** [Fill in]
- **Email:** [Fill in]

---

## 📜 License & Usage

These materials are provided for educational use in CST-405 Compiler Design.

**Instructors:** Feel free to modify for your class needs
**Students:** Use for learning, not for plagiarism

---

**Last Updated:** February 2026
**Version:** 1.0
**Course:** CST-405 Compiler Design
