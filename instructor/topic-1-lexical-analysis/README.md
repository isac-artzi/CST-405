# CST-405 · Topic 1 — Compiler Design Phases · INSTRUCTOR

**Week 1 · Sep 8 – Sep 13, 2026** — complete implementation of this milestone.

> This is the working solution. `student/topic-1-lexical-analysis/` is the same code with this
> topic's work removed and replaced by TODOs.

## Build and demonstrate

```bash
cd lexer
make
make test

./lexer tests/01_all_tokens.cm                # the token table, for projecting
./lexer tests/05_lexical_errors.cm     # four errors from one run
./lexer tests/06_unterminated_comment.cm
```

The token table is built to be projected: number, line, column, kind, lexeme, and
what the kind IS.

## Teaching notes

- **Open with the token table.** Run the instructor lexer on `tests/01_all_tokens.cm` before saying anything about theory. The table is the thing; the theory explains it.
- **The rule-order demo lands every time.** Move the identifier rule above the keywords, live, and run `tests/03_keywords_vs_ids.cm`. `int` comes back as an ID. Ten seconds, and it fixes first-match resolution permanently.
- **Then the longest-match demo.** Delete the `"<="` rule and run `tests/02_longest_match.cm`. Four tokens become eight.
- **Spend real time on columns.** Flex gives you lines free and columns not at all. Ask the class what `skip()` is for before telling them, then delete it from the block-comment rule and show `tests/04_comments.cm` reporting line 4 instead of line 6.
- **The boundary question is worth five minutes.** Why is `int int int;` not a lexical error? Most of the term's confusion is students expecting one phase to do another's work, and this is the cheapest place to head it off.

## What goes wrong

- Students who tokenize only what Topic 2 needs and have to reopen this file in week 12. Push hard on scanning the whole language now.
- `exit()` in the error action. Tests 05 then reports one error instead of four.
- Forgetting `yylval` — harmless this week, and a mystery in Topic 2 when every identifier turns out to be the same string.

## Class activities for this topic

- **Wednesday** — Tokenize by Hand, Then by Machine (`docs/topic-1-lexical-analysis/activity-1-tokenize-by-hand.html`)
- **Friday** — Break the Scanner on Purpose (`docs/topic-1-lexical-analysis/activity-2-break-the-scanner.html`)

## Regenerating this folder

Both the student and instructor copies are generated from one annotated master:

```bash
python3 .tools/stagegen.py --check     # regenerate, then build and test everything
```

Edit `.tools/master/`, never this folder — changes here are overwritten on the next
run. See `.tools/README.md`.
