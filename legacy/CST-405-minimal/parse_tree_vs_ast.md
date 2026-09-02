# Parse Tree vs. Abstract Syntax Tree (AST) for `test.cm`

## Source Code

```c
int x;
int y;
int z;

x = 10;
y = 20;
z = x + y;
print(z);

x = z + 5;
print(x);

y = x + y + z;
print(y);
```

---

## Side-by-Side Comparison

### Key Differences

| Parse Tree (Concrete Syntax Tree)              | Abstract Syntax Tree (AST)                    |
|-------------------------------------------------|-----------------------------------------------|
| Includes **every** grammar symbol and token     | Only keeps **semantically meaningful** nodes   |
| Contains punctuation (`;`, `(`, `)`, `=`)       | Punctuation is **discarded**                   |
| Shows `program`, `stmt_list`, `stmt` wrappers   | Wrappers are **collapsed** into a flat list    |
| Reflects the exact grammar productions          | Reflects the **logical structure** of the code |
| Larger, more verbose                            | Smaller, more compact                          |

---

### Statement: `int x;`

```
       PARSE TREE                          AST
       ----------                          ---

         decl                        DECL: int x
        / | \
      INT  ID  ';'
           |
          "x"
```

- The parse tree retains the `INT` keyword token and `;` terminator as separate nodes.
- The AST collapses this into a single `DECL` node that preserves both the **type** (`int`)
  and the **name** (`x`) — the type is semantically meaningful (it determines storage size,
  valid operations, and enables type checking), so it belongs in the AST.

---

### Statement: `x = 10;`

```
       PARSE TREE                          AST
       ----------                          ---

          assign                        ASSIGN: x
        /  |  \  \                         |
      ID  '='  expr ';'                  NUM: 10
      |         |
     "x"       NUM
                |
               10
```

- The `=` operator and `;` terminator disappear in the AST.
- The assignment target (`x`) is stored directly in the node, and the value subtree is its child.

---

### Statement: `z = x + y;`

```
       PARSE TREE                              AST
       ----------                              ---

            assign                          ASSIGN: z
          /  |   \   \                         |
        ID  '='  expr  ';'                  BINOP: +
        |         |                          /     \
       "z"    expr '+' expr              VAR: x   VAR: y
               |         |
              ID         ID
              |          |
             "x"        "y"
```

- The parse tree shows the full derivation: `expr -> expr '+' expr`.
- The AST captures the same structure more concisely with a `BINOP` node
  whose children are the operands.

---

### Statement: `print(z);`

```
       PARSE TREE                              AST
       ----------                              ---

          print_stmt                         PRINT
       /  |   |   |  \                         |
   PRINT '('  expr ')' ';'                  VAR: z
                |
               ID
                |
               "z"
```

- Five tokens in the parse tree; the AST needs only two nodes.
- `PRINT`, `(`, `)`, and `;` all served purely syntactic roles.

---

### Statement: `y = x + y + z;`  (left-associative addition)

```
       PARSE TREE                                      AST
       ----------                                      ---

              assign                                ASSIGN: y
           /  |    \     \                             |
         ID  '='   expr   ';'                       BINOP: +
         |          |                                /     \
        "y"     expr '+' expr                   BINOP: +   VAR: z
                 |         |                     /     \
             expr '+' expr  ID                VAR: x   VAR: y
              |         |   |
             ID        ID  "z"
              |         |
             "x"       "y"
```

- Both trees encode left-associativity: `(x + y) + z`.
- The parse tree shows two `expr '+' expr` productions nested.
- The AST shows this as two nested `BINOP` nodes — same structure, less syntactic noise.

---

## Full Parse Tree (all 10 statements)

```
                                    program
                                      |
                                   stmt_list
                   ________________/    \
                  /                    stmt ─── print_stmt
               stmt_list                       / | |  |  \
            ___/    \                      PRINT '(' expr ')' ';'
           /       stmt ── assign                  |
        stmt_list        / |  \   \               ID
       ___/   \         ID '=' expr ';'            |
      /      stmt       |      |                  "y"
   stmt_list   |       "y"  expr '+' expr
   ___/ \    assign          |          |
  /     \   / | \ \       expr '+' expr  ID
 s.l.  stmt ID '=' expr ';' |       |   |
 /\     |   |      |       ID      ID  "z"
|  \  assign "x" expr '+' NUM |       |
|   \  /|\         |        |  "x"    "y"
| print_stmt      ID       5
| / | | | \        |
|PRINT(expr);     "z"
|      |
|     ID
|      |
|     "z"
|
stmt_list
___/ \
/     \
s.l.   stmt ── assign
/\       |     / | \ \
|  \   assign ID '=' expr ';'
|   \  /|\     |      |
|  print ID=expr; "y"  NUM
|  /||||  |   |        |
| P(expr); "x" NUM    20
|    |          |
|   ID         10
|    |
|   "x"
|
stmt_list
 /      \
stmt   stmt
 |       |
decl   decl
/|\    /|\
INT ID ; INT ID ;
    |       |
   "x"     "y"
             ...continued above...
```

*(The full parse tree is deeply nested and difficult to render in text —
this is precisely why compilers convert it to an AST!)*

---

## Full AST (actual compiler output)

This is the exact output produced by the minimal compiler's `printAST()` function:

```
DECL: int x
DECL: int y
DECL: int z
ASSIGN: x
  NUM: 10
ASSIGN: y
  NUM: 20
ASSIGN: z
  BINOP: +
    VAR: x
    VAR: y
PRINT
  VAR: z
ASSIGN: x
  BINOP: +
    VAR: z
    NUM: 5
PRINT
  VAR: x
ASSIGN: y
  BINOP: +
    BINOP: +
      VAR: x
      VAR: y
    VAR: z
PRINT
  VAR: y
```

### How `NODE_STMT_LIST` creates this flat output

The AST is internally a **right-leaning linked list** of `STMT_LIST` nodes:

```
STMT_LIST
 ├── stmt: DECL int x
 └── next: STMT_LIST
              ├── stmt: DECL int y
              └── next: STMT_LIST
                           ├── stmt: DECL int z
                           └── next: STMT_LIST
                                        ├── stmt: ASSIGN x ── NUM 10
                                        └── next: STMT_LIST
                                                     ├── stmt: ASSIGN y ── NUM 20
                                                     └── next: STMT_LIST
                                                                  ├── stmt: ASSIGN z ── BINOP +
                                                                  │                      ├── VAR x
                                                                  │                      └── VAR y
                                                                  └── next: STMT_LIST
                                                                               ├── stmt: PRINT ── VAR z
                                                                               └── next: ...
```

The `printAST` function hides the `STMT_LIST` scaffolding by printing each child
at the **same indentation level**, giving the clean flat output above.

---

## Discussion Points

1. **Why not just use the parse tree?**
   The parse tree is tightly coupled to the grammar. Changing a grammar rule
   (e.g., adding optional semicolons) would change the tree structure even though
   the program's meaning hasn't changed. The AST abstracts away these syntactic details.

2. **Information loss — is anything important discarded?**
   Semicolons, parentheses, and the `=` token carry no semantic information beyond
   what the AST node types already encode. However, the type keyword `int` *is*
   semantically meaningful — it determines storage size, valid operations, and enables
   type checking — so it is preserved in the `DECL` node's `varType` field and
   propagated into the symbol table.

3. **Left-associativity in `y = x + y + z`:**
   Both trees encode this as `(x + y) + z`. This is dictated by the `%left '+'`
   precedence declaration in `parser.y:42`. The parser builds the correct nesting
   automatically via the grammar rule `expr: expr '+' expr`.

4. **Where does the grammar end and the AST begin?**
   The parser's semantic actions (`{...}` blocks in `parser.y`) are the bridge.
   As each grammar production is reduced, the action creates an AST node — this is
   where the concrete parse tree is *selectively* captured into the abstract tree.
