# legacy — superseded course materials

Everything in this directory is the **previous** version of the CST-405 materials,
kept only for reference. Nothing current depends on it, and it is not regenerated.

| Folder | What it was | Superseded by |
|---|---|---|
| `CST-405-minimal/` | the minimal compiler | `instructor/topic-2-minimal-compiler/` |
| `CST-405-functions/` | functions and arrays | `instructor/topic-3-arrays-and-functions/` |
| `CST-405-if-loop/` | while loops | `instructor/topic-4-loops/` |
| `CST-405-for-loop/` | for loops | `instructor/topic-4-loops/` |
| `CST-405-if-statements/` | if statements | `instructor/topic-5-decisions/` |
| `CST-405-switch-statements/` | switch | `instructor/topic-5-decisions/` |
| `src/`, `include/`, `tests/`, `examples/` | a separate, parallel C-Minus compiler | the `.tools/master/` lineage |
| `compiler-extensions/` | six HTML extension write-ups | the optional-extension sections of the assignment `.docx` files |
| various `.html`, `.md`, `.pptx` | earlier activities and slides | `docs/` |

## Why it was replaced

The six `CST-405-*` folders were near-copies of one compiler maintained by hand, and
they had drifted. Consolidating them onto one generated master fixed several real
bugs that existed in some copies and not others:

- **The calling convention was broken.** `$ra` was never saved and `$sp` never moved
  between functions, so a callee's locals overwrote its caller's and recursion could
  not work.
- **`TAC_RETURN` emitted no jump.** A `return` in the middle of a function fell
  through into the code after it — which made `return` inside a `switch` case return
  whatever the *last* case said.
- **Global variables and arrays were unsupported** in the back end, despite being
  accepted by the grammar.
- **Array parameters were not passed by reference**, so passing an array to a
  function produced wrong addresses.
- **Global arrays were misaligned** in `.data`, raising an address-error exception in
  SPIM on every access.

These are fixed in `.tools/master/`, and `python3 .tools/stagegen.py --check` builds
and tests every milestone to keep them fixed.

## Deleting this

Nothing references it. `git rm -r legacy/` whenever you are confident you do not
want it — the history keeps it either way.
