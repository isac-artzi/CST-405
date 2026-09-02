#!/usr/bin/env python3
"""
docgen.py — build the CST-405 course site from the content modules.

Every lecture-note page and class activity is described as data in
.tools/content/topicN.py.  This module turns that data into HTML, which means
all thirty-odd pages share one layout, one stylesheet and one set of
interactive components, and fixing the navigation once fixes it everywhere.

    python3 .tools/docgen.py

Output lands in docs/, which is what GitHub Pages serves.
"""

import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
sys.path.insert(0, os.path.join(HERE, "content"))

COURSE = "CST-405 · Principles of Compiler Design"

# ---------------------------------------------------------------------------
# GitHub Pages serves docs/ AS THE SITE ROOT, so a relative link from a page in
# here cannot reach student/ or instructor/ — they sit above it.  Set this to
# your repository URL and the starter-code cards become working links into the
# GitHub file browser.  Left empty, they render as plain paths, which is
# correct-but-unclickable rather than broken.
#
#   REPO_URL = "https://github.com/your-user/your-repo/tree/main"
# ---------------------------------------------------------------------------
REPO_URL = "https://github.com/isac-artzi/CST-405/tree/main"

# ---------------------------------------------------------------------------
# The six topics, in the order the syllabus runs them.
# ---------------------------------------------------------------------------
TOPICS = [
    dict(n=1, slug="topic-1-lexical-analysis",
         title="Compiler Design Phases",
         dates="Sep 8 – Sep 13, 2026", weeks="Week 1",
         project="Project 1 · Lexical Analyzer",
         due="Sep 13, 2026",
         code="lexer",
         blurb="What the six phases are, and the first one built for real."),
    dict(n=2, slug="topic-2-minimal-compiler",
         title="Compiler for a Starter Language",
         dates="Sep 14 – Oct 11, 2026", weeks="Weeks 2–5",
         project="Project 2 · Minimalist Language Compiler",
         due="Oct 11, 2026",
         code="compiler",
         blurb="A whole compiler, end to end, for the smallest language worth compiling."),
    dict(n=3, slug="topic-3-arrays-and-functions",
         title="Compiling Complex Variables and Functions",
         dates="Oct 12 – Nov 1, 2026", weeks="Weeks 6–8",
         project="Project 3 · Complex Variables and Functions",
         due="Nov 1, 2026",
         code="compiler",
         blurb="Arrays, functions, scope — and the activation record that makes calls possible."),
    dict(n=4, slug="topic-4-loops",
         title="Compiling Loops",
         dates="Nov 2 – Nov 22, 2026", weeks="Weeks 9–11",
         project="Project 4 · Loops and Optimization",
         due="Nov 22, 2026",
         code="compiler",
         blurb="Control flow becomes labels and jumps; then the optimizer earns its keep."),
    dict(n=5, slug="topic-5-decisions",
         title="Compiling Control Flow — Decisions",
         dates="Nov 23 – Dec 13, 2026", weeks="Weeks 12–14",
         project="Project 5 · Logic and Decisions",
         due="Dec 13, 2026",
         code="compiler",
         blurb="if, else, the dangling-else problem, Boolean operators, and switch."),
    dict(n=6, slug="topic-6-complete-compiler",
         title="Compiler Design and Implementation",
         dates="Dec 14 – Dec 20, 2026", weeks="Week 15",
         project="Project 6 · Complete Compiler (Benchmark)",
         due="Dec 20, 2026",
         code="compiler",
         blurb="Measure it, document it, defend it."),
]
BY_N = {t["n"]: t for t in TOPICS}

PHASES = [
    ("scanner.l",  "Lexical",    "chars → tokens"),
    ("parser.y",   "Syntax",     "tokens → AST"),
    ("semantic.c", "Semantic",   "AST → checked AST"),
    ("tac.c",      "IR",         "AST → TAC"),
    ("tac.c",      "Optimize",   "TAC → better TAC"),
    ("codegen.c",  "CodeGen",    "TAC → MIPS"),
]


# ===========================================================================
# Components
# ===========================================================================

def esc(s):
    return html.escape(s, quote=False)


def code(text, lang=""):
    """A code block.  Lines beginning >>> are highlighted."""
    out = []
    for line in text.rstrip("\n").split("\n"):
        if line.startswith(">>>"):
            out.append('<span class="hi">' + esc(line[3:]) + "</span>")
        else:
            out.append(esc(line))
    return '<pre><code class="lang-%s">%s</code></pre>\n' % (lang, "\n".join(out))


def pipeline(active=None, done=()):
    """The six-phase diagram, with the phase under discussion highlighted."""
    bw, gap, x0 = 148, 22, 6
    w = x0 * 2 + 6 * bw + 5 * gap          # exactly wide enough, so nothing clips
    parts = ['<div class="pipeline"><svg viewBox="0 0 %d 92" role="img" '
             'aria-label="The six phases of the compiler, left to right">' % w]
    for i, (f, name, sub) in enumerate(PHASES):
        x = x0 + i * (bw + gap)
        cls = "ph-box"
        if active is not None and i == active:
            cls += " on"
        elif i in done:
            cls += " done"
        parts.append('<rect class="%s" x="%d" y="20" width="%d" height="44" rx="6"/>' % (cls, x, bw))
        parts.append('<text class="ph-t" x="%d" y="39" text-anchor="middle">%d. %s</text>'
                     % (x + bw // 2, i + 1, name))
        parts.append('<text class="ph-s" x="%d" y="53" text-anchor="middle">%s</text>'
                     % (x + bw // 2, esc(sub)))
        parts.append('<text class="ph-lbl" x="%d" y="77" text-anchor="middle">%s</text>'
                     % (x + bw // 2, esc(f)))
        if i < len(PHASES) - 1:
            ax = x + bw + 3
            parts.append('<path class="ph-arrow" d="M%d 42 L%d 42 M%d 38 L%d 42 L%d 46"/>'
                         % (ax, ax + gap - 6, ax + gap - 11, ax + gap - 6, ax + gap - 11))
    parts.append("</svg></div>\n")
    return "".join(parts)


def tabs(pairs):
    """pairs: [(label, html_body), ...] — the same program in several forms."""
    bar = "".join('<button role="tab" aria-selected="false">%s</button>' % esc(l) for l, _ in pairs)
    panels = "".join('<div class="panel" hidden>%s</div>' % b for _, b in pairs)
    return '<div class="tabs"><div class="tabbar" role="tablist">%s</div>%s</div>\n' % (bar, panels)


def stepper(steps):
    """steps: [(caption, html_body), ...] — one transformation, one move at a time."""
    body = "".join('<div class="step" hidden><p class="caption">%s</p>%s</div>' % (c, b)
                   for c, b in steps)
    return ('<div class="stepper" tabindex="0">'
            '<div class="bar">'
            '<button data-act="prev">← back</button>'
            '<button data-act="next">next →</button>'
            '<button data-act="reset">restart</button>'
            '<span class="count"></span></div>'
            '<div class="body">%s</div></div>\n' % body)


def reveal(summary, body):
    return '<details class="reveal"><summary>%s</summary>%s</details>\n' % (esc(summary), body)


def quiz(question, options, feedback_default=""):
    """options: [(text, is_correct, feedback), ...]

    The question and option labels may contain inline HTML (they routinely
    contain <code>), so they are NOT escaped.  The feedback goes into an
    attribute and therefore is."""
    opts = "".join(
        '<button class="opt" data-correct="%d" data-feedback="%s">%s</button>'
        % (1 if ok else 0, html.escape(fb or feedback_default, quote=True), t)
        for t, ok, fb in options)
    return ('<div class="quiz"><p class="q">%s</p>%s<p class="fb"></p></div>\n'
            % (question, opts))


def note(kind, title, body):
    return '<div class="%s"><b>%s</b>%s</div>\n' % (kind, esc(title), body)


def table(headers, rows):
    h = "".join("<th>%s</th>" % esc(x) for x in headers)
    r = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % x for x in row) for row in rows)
    return '<div class="tablewrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>\n' % (h, r)


def steps_list(items):
    return '<ol class="steps">%s</ol>\n' % "".join("<li>%s</li>" % i for i in items)


def cards(items):
    """items: [(href, title, text), ...].  A href of None renders unlinked."""
    out = []
    for h, t, b in items:
        head = ('<a class="title" href="%s">%s</a>' % (h, esc(t))) if h else esc(t)
        out.append('<div class="card"><h3>%s</h3><p>%s</p></div>' % (head, b))
    return '<div class="grid">%s</div>\n' % "".join(out)


def p(*paras):
    return "".join("<p>%s</p>\n" % x for x in paras)


def h2(t): return "<h2>%s</h2>\n" % esc(t)
def h3(t): return "<h3>%s</h3>\n" % esc(t)
def h4(t): return "<h4>%s</h4>\n" % esc(t)
def ul(items): return "<ul>%s</ul>\n" % "".join("<li>%s</li>" % i for i in items)
def ol(items): return "<ol>%s</ol>\n" % "".join("<li>%s</li>" % i for i in items)


def meta(pairs):
    """The small fact bar at the top of a class activity."""
    return '<div class="meta">%s</div>\n' % "".join(
        "<span><b>%s</b> %s</span>" % (esc(k), esc(v)) for k, v in pairs)


def deliverable(body):
    return '<div class="deliverable"><h3>Deliverable</h3>%s</div>\n' % body


# ===========================================================================
# Page shell
# ===========================================================================

def page(path, title, eyebrow, lede, body, crumbs, depth=1):
    up = "../" * depth
    doc = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s · CST-405</title>
<link rel="stylesheet" href="%(up)sassets/cst405.css">
</head>
<body>
<header class="masthead">
  <div class="wrap">
    <p class="eyebrow">%(eyebrow)s</p>
    <h1>%(title)s</h1>
    <p class="lede">%(lede)s</p>
    <nav class="crumbs">%(crumbs)s</nav>
  </div>
</header>
<main class="wrap">
%(body)s
<footer class="pagefoot">
  <span>%(course)s · Grand Canyon University</span>
  <span><a href="%(up)sindex.html">All topics</a></span>
</footer>
</main>
<script src="%(up)sassets/cst405.js"></script>
</body>
</html>
""" % dict(title=esc(title), eyebrow=esc(eyebrow), lede=lede, body=body,
           crumbs=crumbs, up=up, course=COURSE)
    full = os.path.join(DOCS, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(doc)
    return path


def crumbs_for(t, extra=None):
    c = '<a href="../index.html">All topics</a> &nbsp;›&nbsp; '
    if extra:
        c += '<a href="index.html">Topic %d</a> &nbsp;›&nbsp; %s' % (t["n"], esc(extra))
    else:
        c += "Topic %d" % t["n"]
    return c


# ===========================================================================
# Build
# ===========================================================================

def build():
    import importlib
    written = []

    for t in TOPICS:
        mod = importlib.import_module("topic%d" % t["n"])

        # --- lecture notes -------------------------------------------------
        written.append(page(
            "%s/lecture-notes.html" % t["slug"],
            mod.LECTURE_TITLE,
            "Topic %d · Lecture notes · %s" % (t["n"], t["weeks"]),
            mod.LECTURE_LEDE,
            mod.lecture(),
            crumbs_for(t, "Lecture notes")))

        # --- activities ----------------------------------------------------
        acts = []
        for i, a in enumerate(mod.ACTIVITIES, 1):
            fn = "activity-%d-%s.html" % (i, a["slug"])
            written.append(page(
                "%s/%s" % (t["slug"], fn),
                a["title"],
                "Topic %d · Class activity %d · %s" % (t["n"], i, a["session"]),
                a["lede"],
                a["body"](),
                crumbs_for(t, "Activity %d" % i)))
            acts.append((fn, "Activity %d — %s" % (i, a["title"]), a["lede"]))

        # --- topic index ---------------------------------------------------
        docx = "CST-405-Topic-%d-%s.docx" % (t["n"], t["project"].split("·")[0].strip().replace(" ", "-"))
        body = (
            pipeline() +
            p("<b>%s</b> &nbsp;·&nbsp; %s &nbsp;·&nbsp; %s" % (esc(t["weeks"]), esc(t["dates"]), esc(t["blurb"]))) +
            h2("Start here") +
            cards([
                ("lecture-notes.html", "Lecture notes", esc(mod.LECTURE_LEDE)),
                (("%s/student/%s/" % (REPO_URL.rstrip("/"), t["slug"])) if REPO_URL else None,
                 "Your starter code",
                 "The %s you are extending this topic, with every TODO spelled out."
                 "<br><code>student/%s/</code>" % (t["code"], t["slug"])),
                (docx, "Assignment: %s" % esc(t["project"]),
                 "Full requirements and submission checklist. Due %s." % esc(t["due"])),
            ]) +
            h2("Class activities") +
            p("One per class meeting. Ungraded — they exist so that the assignment "
              "is not the first time you meet the idea.") +
            cards(acts))
        written.append(page("%s/index.html" % t["slug"],
                            "Topic %d — %s" % (t["n"], t["title"]),
                            "Topic %d · %s" % (t["n"], t["weeks"]),
                            esc(t["blurb"]),
                            body,
                            '<a href="../index.html">All topics</a> &nbsp;›&nbsp; Topic %d' % t["n"]))

    # --- site home ---------------------------------------------------------
    rows = []
    for t in TOPICS:
        rows.append([
            '<a href="%s/index.html"><b>Topic %d</b></a>' % (t["slug"], t["n"]),
            esc(t["title"]),
            esc(t["weeks"]),
            '<a href="%s/lecture-notes.html">notes</a>' % t["slug"],
            esc(t["project"].split("·")[0].strip()),
            esc(t["due"]),
        ])
    home = (
        p("This course does not build one compiler in six pieces. It builds "
          "<b>six compilers</b>, each one the previous one with a new language "
          "feature threaded through all six phases. By December you will have "
          "written the front end six times, and that repetition is the point: "
          "the second time you add a construct you will already know which "
          "files it touches.") +
        pipeline() +
        p("Every topic below has interactive lecture notes, one class activity "
          "per meeting, starter code with the work marked out, and the "
          "assignment description.") +
        table(["", "Topic", "When", "Notes", "Project", "Due"], rows) +
        h2("How the code is organised") +
        ul([
            "<code>student/topic-N/</code> — the compiler you start from, with "
            "this topic's work removed and replaced by numbered TODOs. It builds "
            "and runs before you touch it.",
            "<code>instructor/</code> — the complete milestone for each topic, "
            "kept on the instructor's machine and deliberately not published here.",
            "<code>docs/</code> — this site.",
        ]) +
        note("note", "Running the compiler",
             p("Every folder builds with <code>make</code> and self-tests with "
               "<code>make test</code>. You need <code>flex</code>, "
               "<code>bison</code>, <code>gcc</code>, and "
               "<a href='http://spimsimulator.sourceforge.net/'>SPIM</a> or QtSPIM "
               "to run the generated MIPS.")))
    written.append(page("index.html", "Principles of Compiler Design",
                        "CST-405 · Fall 2026 · Grand Canyon University",
                        "Six compilers in fifteen weeks.",
                        home,
                        "", depth=0))

    print("docgen: wrote %d pages" % len(written))
    for w in sorted(written):
        print("  docs/%s" % w)


if __name__ == "__main__":
    build()
