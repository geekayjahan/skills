# Self-Improving Skills

How a skill gets better with use: evals gate every output, memory carries lessons
between uses, and a pruning pass keeps both from rotting. This file is the full
mechanics for steps 2, 5, and 6 of the build loop.

## Contents

- [Writing eval checks](#writing-eval-checks)
- [The grading loop](#the-grading-loop)
- [memory.md](#memorymd)
- [The pruning pass](#the-pruning-pass)
- [Templates](#templates)

## Writing eval checks

A good check names something every gold example does and a plausible bad output
would not, verifiable by pointing at the output. If two honest graders could
disagree on a verdict, split or sharpen the check until they could not.

Cap `evals.md` at ~12 checks. To add one past the cap, merge or retire a weaker one.

## The grading loop

The builder never grades its own work. A grader that watched the build inherits the
builder's reasoning and rationalizes the same flaws, so:

1. Launch a fresh agent whose context contains only three things: the output being
   graded, `evals.md`, and the source material the output was built from.
2. The grader returns a verdict per check — pass or fail, each with quoted evidence.
3. On any fail, the builder fixes the output and a **new** fresh agent re-grades.
   Reusing the previous grader contaminates it the same way reusing the builder would.
4. Stop when every check passes. Three to five rounds is typical for a first run;
   one round is typical once the skill has matured.

## memory.md

A lessons log for feedback that no binary check captures — style preferences, user
corrections, recurring pitfalls.

- One line per lesson, dated, newest first.
- Hard cap: ~12 entries. The cap is what forces distillation; an unbounded log
  becomes a second, worse skill body.
- Read it before building; append to it after any use that taught something.

## The pruning pass

Run after every use; do a deeper sweep every ~5 uses. The pass subtracts more often
than it adds — it exists to counter the slop-accumulation failure mode described in
[anti-patterns.md](anti-patterns.md):

- **Graduate**: a lesson that has held for 3+ uses moves into `references/` (if it
  is knowledge) or `evals.md` (if it is checkable), and is deleted from memory.
- **Merge**: two entries about the same behavior become one.
- **Retire**: entries about behavior the skill no longer exhibits get deleted.
- **Reread what changed**: in any file touched this cycle, delete every sentence
  whose removal loses nothing.

## Templates

`evals.md`:

```markdown
# Evals - <skill-name>

Binary checks, cap ~12. Grading loop: skill-creator references/self-improving.md.

1. [Question answerable yes/no by pointing at the output]
2. ...
```

`memory.md`:

```markdown
# Memory - <skill-name>

One line per lesson, newest first, cap ~12. Rules: skill-creator references/self-improving.md.

- YYYY-MM-DD: [lesson]
```
