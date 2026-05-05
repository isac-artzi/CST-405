# C-Minus Language Grammar Reference

## CST-405 Compiler Design

This document presents the grammar of the C-Minus language as it evolves across the course. Each section corresponds to one iteration of the compiler, building incrementally from a minimal base to a full-featured language. Grammar rules are written in BNF notation. Terminal symbols appear in `'single quotes'` and non-terminals are plain text.

Each iteration shows only the **new and changed** rules introduced in that phase. Rules carried forward unchanged from previous iterations are omitted for brevity.

---

## Lexical Conventions (All Iterations)

The following lexical rules apply throughout every iteration of the grammar:

| Element | Pattern | Examples |
|---------|---------|----------|
| Identifier (ID) | Letter or underscore, followed by letters, digits, or underscores | `x`, `count`, `my_var` |
| Integer Literal (NUM) | One or more digits | `0`, `42`, `100` |
| Single-line comment | `//` to end of line | `// this is a comment` |
| Multi-line comment | `/*` ... `*/` | `/* block comment */` |
| Whitespace | Spaces, tabs, newlines | (ignored) |

---

## Iteration 1: Minimal Compiler

**Folder:** `CST-405-minimal/`

**What students build:** A compiler that handles integer variable declarations, assignment with addition, and a built-in `print` statement. This is the simplest possible program that demonstrates all six compiler phases (lexing, parsing, semantic analysis, TAC generation, optimization, and MIPS code generation).

### Keywords and Tokens

```
Keywords:    int   print
Operators:   +   =
Delimiters:  ;   (   )
```

### Grammar

```
program
    → stmt_list

stmt_list
    → stmt
    | stmt_list  stmt

stmt
    → decl
    | assign
    | print_stmt

decl
    → 'int'  ID  ';'

assign
    → ID  '='  expr  ';'

expr
    → NUM
    | ID
    | expr  '+'  expr

print_stmt
    → 'print'  '('  expr  ')'  ';'
```

### Operator Precedence

| Precedence | Operator | Associativity |
|------------|----------|---------------|
| 1          | `+`      | Left          |

### Example Program

```c
int x;
int y;
x = 5;
y = x + 3;
print(y);
```

---

## Iteration 2: Functions, Arrays, and Arithmetic

**Folder:** `CST-405-functions/`

**What is added:** Programs are now organized into function definitions. Arrays, return statements, the remaining arithmetic operators (`-`, `*`, `/`), unary minus, function calls, and block statements are introduced. The program structure changes from a flat statement list to a list of top-level declarations and function definitions.

Note: Comparison operators are not yet needed because the language has no conditional or looping constructs at this stage.

### New Keywords and Tokens

```
New Keywords:    return
New Operators:   -   *   /
New Delimiters:  {   }   [   ]   ,
```

### Grammar (new and changed rules only)

```
program
    → decl_or_func_list                                       [CHANGED]

decl_or_func_list                                             [NEW]
    → decl_or_func
    | decl_or_func_list  decl_or_func

decl_or_func                                                  [NEW]
    → func_def
    | decl

func_def                                                      [NEW]
    → 'int'  ID  '('  params  ')'  block
    | 'int'  ID  '('  ')'  block

params                                                        [NEW]
    → param_list

param_list                                                    [NEW]
    → param
    | param_list  ','  param

param                                                         [NEW]
    → 'int'  ID
    | 'int'  ID  '['  ']'

block                                                         [NEW]
    → '{'  stmt_list  '}'
    | '{'  '}'

stmt                                                          [CHANGED]
    → decl
    | assign
    | print_stmt
    | return_stmt
    | block
    | func_call  ';'

decl                                                          [CHANGED]
    → 'int'  ID  ';'
    | 'int'  ID  '['  NUM  ']'  ';'

assign                                                        [CHANGED]
    → ID  '='  expr  ';'
    | ID  '['  expr  ']'  '='  expr  ';'

return_stmt                                                   [NEW]
    → 'return'  expr  ';'
    | 'return'  ';'

expr                                                          [CHANGED]
    → NUM
    | ID
    | ID  '['  expr  ']'
    | func_call
    | expr  '+'  expr
    | expr  '-'  expr
    | expr  '*'  expr
    | expr  '/'  expr
    | '-'  expr                                  (unary minus)
    | '('  expr  ')'

func_call                                                     [NEW]
    → ID  '('  args  ')'
    | ID  '('  ')'

args                                                          [NEW]
    → arg_list

arg_list                                                      [NEW]
    → expr
    | arg_list  ','  expr
```

### Operator Precedence

Listed from lowest to highest:

| Precedence | Operators    | Associativity |
|------------|-------------|---------------|
| 1 (lowest) | `+`  `-`    | Left          |
| 2          | `*`  `/`    | Left          |
| 3 (highest)| unary `-`   | Right         |

### Example Program

```c
int add(int a, int b) {
    return a + b;
}

int main() {
    int nums[5];
    int result;
    nums[0] = 10;
    result = add(nums[0], 20);
    print(result);
    return 0;
}
```

---

## Iteration 3: While Loops

**Folder:** `CST-405-if-loop/`

**What is added:** The `while` loop -- the first control-flow construct in the language. Because loops require conditions, the comparison operators (`<`, `>`, `<=`, `>=`, `==`, `!=`) are also introduced in this iteration.

### New Keywords and Tokens

```
New Keywords:    while
New Operators:   <   >   <=   >=   ==   !=
```

### Grammar (new and changed rules only)

```
stmt                                                          [CHANGED]
    → ...                                   (all previous forms)
    | while_stmt

while_stmt                                                    [NEW]
    → 'while'  '('  expr  ')'  stmt

expr                                                          [CHANGED]
    → ...                                   (all previous forms)
    | expr  '<'   expr
    | expr  '>'   expr
    | expr  '<='  expr
    | expr  '>='  expr
    | expr  '=='  expr
    | expr  '!='  expr
```

### Operator Precedence

The comparison operators slot in below the arithmetic operators:

| Precedence | Operators              | Associativity |
|------------|------------------------|---------------|
| 1 (lowest) | `==`  `!=`             | Left          |
| 2          | `<`  `>`  `<=`  `>=`   | Left          |
| 3          | `+`  `-`               | Left          |
| 4          | `*`  `/`               | Left          |
| 5 (highest)| unary `-`              | Right         |

### Design Notes

- The body of `while` is a single *stmt*, which can be a block (`{ ... }`), giving the familiar braced form.
- Any expression can serve as the loop condition. A value of zero is false; any non-zero value is true.

### Example Program

```c
int main() {
    int x;
    x = 10;

    while (x > 0) {
        print(x);
        x = x - 1;
    }

    return 0;
}
```

---

## Iteration 4: For Loops

**Folder:** `CST-405-for-loop/`

**What is added:** The `for` loop construct. All three parts of the for-loop header (initialization, condition, update) are optional, following C conventions.

### New Keywords and Tokens

```
New Keywords:    for
```

### Grammar (new and changed rules only)

```
stmt                                                          [CHANGED]
    → ...                                   (all previous forms)
    | for_stmt

for_stmt                                                      [NEW]
    → 'for'  '('  for_init  ';'  for_cond  ';'  for_update  ')'  stmt

for_init                                                      [NEW]
    → (* empty *)
    | ID  '='  expr
    | ID  '['  expr  ']'  '='  expr

for_cond                                                      [NEW]
    → (* empty *)
    | expr

for_update                                                    [NEW]
    → (* empty *)
    | ID  '='  expr
    | ID  '['  expr  ']'  '='  expr
```

### Design Notes

- When *for_init* is empty, no initialization is performed.
- When *for_cond* is empty, the loop runs indefinitely (always true).
- When *for_update* is empty, no per-iteration update occurs.
- The init and update clauses support both scalar and array-element assignments.
- Note that init and update are **assignment expressions without a trailing semicolon** -- the semicolons in `for (init ; cond ; update)` are part of the `for_stmt` rule itself.

### Example Program

```c
int main() {
    int sum;
    int i;
    sum = 0;
    for (i = 1; i <= 10; i = i + 1) {
        sum = sum + i;
    }
    print(sum);
    return 0;
}
```

---

## Iteration 5: If-Statements

**Folder:** `CST-405-if-statements/`

**What is added:** Conditional branching with `if` and the optional `else` clause. This iteration also addresses the **dangling-else ambiguity** -- a classic problem in language design -- using Bison's precedence mechanism.

### New Keywords and Tokens

```
New Keywords:    if   else
```

### Grammar (new and changed rules only)

```
stmt                                                          [CHANGED]
    → ...                                   (all previous forms)
    | if_stmt

if_stmt                                                       [NEW]
    → 'if'  '('  expr  ')'  stmt
    | 'if'  '('  expr  ')'  stmt  'else'  stmt
```

### The Dangling-Else Problem

When `if` statements are nested, an `else` clause is ambiguous:

```c
if (a)
    if (b)
        x = 1;
    else
        x = 2;
```

Which `if` does the `else` belong to? There are two valid parse trees:

```
Interpretation A:                Interpretation B:
if (a)                           if (a)
    if (b)                           if (b)
        x = 1;                          x = 1;
    else            <-- inner    else                <-- outer
        x = 2;                       x = 2;
```

The standard C convention (Interpretation A) is that `else` binds to the **nearest** unmatched `if`.

### Solution: Precedence-Based Disambiguation

The resolution uses Bison's precedence mechanism with a pseudo-token:

```
%nonassoc  LOWER_THAN_ELSE      (* pseudo-token with lower precedence *)
%nonassoc  ELSE                 (* ELSE token with higher precedence  *)
```

The if-without-else rule is annotated: `%prec LOWER_THAN_ELSE`.

When the parser sees `else` after an if-without-else, it must choose:
- **Reduce** (close the outer `if`) -- precedence of `LOWER_THAN_ELSE`
- **Shift** (attach `else` to the inner `if`) -- precedence of `ELSE`

Since `ELSE` has higher precedence, the parser **shifts**, binding `else` to the nearest `if`. This eliminates the shift/reduce conflict warning entirely.

### Example Program

```c
int main() {
    int x;
    x = 10;

    if (x > 5) {
        print(1);
    } else {
        print(0);
    }

    return 0;
}
```

---

## Iteration 6: Switch Statements

**Folder:** `CST-405-switch-statements/`

**What is added:** The `switch`, `case`, `default`, and `break` statements, providing multi-way branching on integer values.

### New Keywords and Tokens

```
New Keywords:    switch   case   default   break
New Delimiters:  :
```

### Grammar (new and changed rules only)

```
stmt                                                          [CHANGED]
    → ...                                   (all previous forms)
    | switch_stmt
    | break_stmt

switch_stmt                                                   [NEW]
    → 'switch'  '('  expr  ')'  '{'  case_list  '}'

case_list                                                     [NEW]
    → (* empty *)
    | case_list  case_clause

case_clause                                                   [NEW]
    → 'case'  NUM  ':'  opt_stmt_list
    | 'default'  ':'  opt_stmt_list

opt_stmt_list                                                 [NEW]
    → (* empty *)
    | stmt_list

break_stmt                                                    [NEW]
    → 'break'  ';'
```

### Design Notes

- Case labels must be integer literals (not expressions).
- Fall-through occurs if `break` is omitted (same as C).
- The `default` clause is optional and handles any unmatched value.
- `break` can appear in any statement context, but semantic analysis restricts it to loops and switch bodies.

### Example Program

```c
int main() {
    int day;
    day = 3;
    switch (day) {
        case 1:
            print(10);
            break;
        case 2:
            print(20);
            break;
        case 3:
            print(30);
            break;
        default:
            print(0);
            break;
    }
    return 0;
}
```

---

## Complete Grammar Summary

The final C-Minus grammar after all six iterations, collected into one reference:

### Tokens

```
Keywords:    int  print  return  if  else  while  for  switch  case  default  break
Operators:   +  -  *  /  <  >  <=  >=  ==  !=  =
Delimiters:  ;  ,  :  (  )  {  }  [  ]
Literals:    NUM (integer)
Identifiers: ID
```

### Complete Grammar

```
program
    → decl_or_func_list

decl_or_func_list
    → decl_or_func
    | decl_or_func_list  decl_or_func

decl_or_func
    → func_def
    | decl

func_def
    → 'int'  ID  '('  params  ')'  block
    | 'int'  ID  '('  ')'  block

params
    → param_list

param_list
    → param
    | param_list  ','  param

param
    → 'int'  ID
    | 'int'  ID  '['  ']'

block
    → '{'  stmt_list  '}'
    | '{'  '}'

stmt_list
    → stmt
    | stmt_list  stmt

stmt
    → decl
    | assign
    | print_stmt
    | return_stmt
    | if_stmt
    | while_stmt
    | for_stmt
    | switch_stmt
    | break_stmt
    | block
    | func_call  ';'

decl
    → 'int'  ID  ';'
    | 'int'  ID  '['  NUM  ']'  ';'

assign
    → ID  '='  expr  ';'
    | ID  '['  expr  ']'  '='  expr  ';'

return_stmt
    → 'return'  expr  ';'
    | 'return'  ';'

if_stmt
    → 'if'  '('  expr  ')'  stmt
    | 'if'  '('  expr  ')'  stmt  'else'  stmt

while_stmt
    → 'while'  '('  expr  ')'  stmt

for_stmt
    → 'for'  '('  for_init  ';'  for_cond  ';'  for_update  ')'  stmt

for_init
    → (* empty *)
    | ID  '='  expr
    | ID  '['  expr  ']'  '='  expr

for_cond
    → (* empty *)
    | expr

for_update
    → (* empty *)
    | ID  '='  expr
    | ID  '['  expr  ']'  '='  expr

switch_stmt
    → 'switch'  '('  expr  ')'  '{'  case_list  '}'

case_list
    → (* empty *)
    | case_list  case_clause

case_clause
    → 'case'  NUM  ':'  opt_stmt_list
    | 'default'  ':'  opt_stmt_list

opt_stmt_list
    → (* empty *)
    | stmt_list

break_stmt
    → 'break'  ';'

print_stmt
    → 'print'  '('  expr  ')'  ';'

expr
    → NUM
    | ID
    | ID  '['  expr  ']'
    | func_call
    | expr  '+'  expr
    | expr  '-'  expr
    | expr  '*'  expr
    | expr  '/'  expr
    | expr  '<'  expr
    | expr  '>'  expr
    | expr  '<='  expr
    | expr  '>='  expr
    | expr  '=='  expr
    | expr  '!='  expr
    | '-'  expr
    | '('  expr  ')'

func_call
    → ID  '('  args  ')'
    | ID  '('  ')'

args
    → arg_list

arg_list
    → expr
    | arg_list  ','  expr
```

### Operator Precedence (lowest to highest)

| Precedence | Operators        | Associativity |
|------------|-----------------|---------------|
| 1 (lowest) | `==`  `!=`      | Left          |
| 2          | `<`  `>`  `<=`  `>=` | Left     |
| 3          | `+`  `-`        | Left          |
| 4          | `*`  `/`        | Left          |
| 5 (highest)| unary `-`       | Right         |

---

## Differences from Standard C

C-Minus is intentionally simplified compared to full C:

| Feature | C-Minus | Standard C |
|---------|---------|------------|
| Types | `int` only | `int`, `char`, `float`, `double`, `void`, structs, unions, enums, pointers |
| Functions | Return `int`, no `void` return type | Multiple return types, `void` |
| I/O | Built-in `print()` | Library functions (`printf`, `scanf`) via `#include` |
| Strings | Not supported | Character arrays with null terminator |
| Preprocessor | None | `#include`, `#define`, `#ifdef`, etc. |
| Pointers | Not supported | Full pointer arithmetic |
| Logical operators | Not supported | `&&`, `\|\|`, `!` |
| Bitwise operators | Not supported | `&`, `\|`, `^`, `~`, `<<`, `>>` |
| Increment/Decrement | Not supported | `++`, `--` |
| Compound assignment | Not supported | `+=`, `-=`, `*=`, `/=` |
| Type casting | Not supported | Explicit and implicit casts |
| `do-while` | Not supported | `do { ... } while (expr);` |
| Ternary operator | Not supported | `expr ? expr : expr` |
| `for` loop declarations | Not supported | `for (int i = 0; ...)` |

These simplifications keep the compiler implementable in a single semester while still exercising every phase of compilation.
