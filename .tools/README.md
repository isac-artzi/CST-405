# .tools — how the course materials are generated

Nothing in `student/`, `instructor/` or `docs/` is edited by hand. All of it is cut
from sources in this directory. That is deliberate: there are twelve nearly
identical copies of one compiler in this repository, and hand-maintaining twelve
copies guarantees they drift apart. Fix a bug in the master, regenerate, and every
milestone gets the fix.

```
.tools/
  master/           ONE annotated compiler. Every topic folder is cut from this.
  topic1/           Topic 1 is a scanner-only project with a different file set,
                    so it is hand-written here and copied verbatim.
  tests/topicN/     the test programs each milestone must pass
  content/topicN.py the lecture notes and class activities, as data

  stagegen.py       master  ->  student/ and instructor/ code folders
  skeleton2.py      instructor topic 2  ->  student topic 2 skeleton
  docgen.py         content/  ->  docs/  (43 HTML pages)
  readmegen.py      ->  a README in every topic folder
  docxgen.py        ->  the six assignment .docx files
```

## Regenerate everything

```bash
python3 .tools/stagegen.py --check    # code: 12 folders, then build and test them
python3 .tools/docgen.py              # the course site
python3 .tools/readmegen.py           # the topic READMEs
python3 .tools/docxgen.py             # the assignment documents
```

`stagegen.py --check` builds every instructor folder and runs its cumulative test
suite. If a milestone breaks an earlier milestone's tests, you find out here.

`docxgen.py` needs `pip install python-docx`; nothing else has dependencies.

Set `REPO_URL` at the top of `docgen.py` to your GitHub repository so that the
"your starter code" cards link into the file browser. GitHub Pages serves `docs/`
as the site root, so those paths cannot be reached relatively.

---

## How the staging works

`master/` is a complete, working compiler with the *last* milestone's feature set.
Anything introduced after Topic 2 is wrapped in a stage marker saying which topic
introduces it. The markers are ordinary block comments, so nothing needs escaping
and the sources stay readable.

```c
/*#4*/
/*#todo Lower NODE_WHILE to labels and jumps.*/
/*#todo   Lstart:  t = cond ;  IF_FALSE t GOTO Lend ;  body ;  GOTO Lstart ;  Lend:*/
        case NODE_WHILE: {
            ... the working implementation ...
        }
/*#end*/
```

Generating topic **S** applies one rule to every block:

| Block introduced at | instructor(S) | student(S) |
|---|---|---|
| N &gt; S | omitted — the feature does not exist yet | omitted |
| N &lt; S | emitted in full — already-solved earlier work | emitted in full |
| N = S | emitted in full | **replaced by the TODO text** |

So `student/topic-4/` is exactly `instructor/topic-3/` plus TODOs — which means a
student skeleton always builds and runs before it is touched. That matters: a
skeleton that does not compile makes it impossible to tell your own mistakes from
ours.

### The other two marker forms

A trailing marker gates a single line:

```c
static int breakDepth = 0;   /*#4*/
```

A `!` marks scaffolding that a later milestone *replaces* rather than extends:

```c
/*#2!*/
    /* The starter language has no functions, so the whole program becomes
     * the body of an implicit main(). Topic 3 replaces this. */
    appendTAC(createTAC(TAC_FUNC_BEGIN, NULL, NULL, "main"));
/*#end*/
```

An `only` block appears in instructor(N) and — because a student skeleton is the
*previous* working milestone — also in student(N+1), where the TODO next to it says
to replace it.

### Rules for editing the master

- A marker must be **alone on its line**, except the trailing single-line form.
  `stagegen.py` refuses to run if it finds a nested or unterminated block.
- `/*#todo` text must not contain `*/`. `skeleton2.py` asserts this; in the master
  it would close the comment early and produce a wall of errors in a file nobody
  has touched.
- In `scanner.l`, markers must be **indented**. Flex treats an unindented line in
  the rules section as a pattern.
- The master no longer compiles on its own — it contains `/*#2!*/` scaffolding
  alongside the code that replaces it. Test through the generated folders:
  `python3 .tools/stagegen.py --check`.

### Progression comments

`stagegen.py` stamps a header on every generated source file: where the file sits
in the pipeline, what changed in this topic, and what the next topic will change.
That text lives in the `PHASE_OF`, `CHANGES` and `NEXT` tables at the top of
`stagegen.py` — add a feature there when you add one to the master, or the banners
go stale while the code stays correct.

---

## Topic 1 and Topic 2 are special

**Topic 1** is a scanner with its own driver and no parser, so it is hand-written
in `topic1/instructor/` and `topic1/student/` and copied verbatim.

**Topic 2** has no previous milestone to be "plus TODOs" of — Project 2 asks
students to build a whole compiler for the first time. So its student skeleton is
produced by `skeleton2.py`, which takes the generated instructor folder and removes
specific implementations. What is removed and what is given is a pedagogical
decision, and it is documented at the top of that file rather than left implicit.

---

## Adding a language feature

1. Implement it in `master/`, wrapped in `/*#N*/ … /*#end*/` with a `/*#todo`
   explaining what a student has to write.
2. Add a test to `tests/topicN/` with its expected output in a header comment.
3. Add a line to `CHANGES[N]` in `stagegen.py` so the file banners mention it.
4. `python3 .tools/stagegen.py --check` — it builds and tests all twelve folders.
5. Mention it in `content/topicN.py` (lecture notes) and `docxgen.py` (the
   assignment), then regenerate those.

## Adding or editing a class activity

Activities live in `content/topicN.py` as entries in the `ACTIVITIES` list. Each is
a dict with `slug`, `session`, `title`, `lede` and a `body` function returning HTML
built from the helpers in `docgen.py` (`steps_list`, `meta`, `deliverable`,
`reveal`, `quiz`, `code`, `note`, `table`). Run `docgen.py`; the topic index page
picks up the new activity automatically.
