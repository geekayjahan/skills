---
name: skill-creator
description: Guide for creating and improving skills - folders of instructions, scripts, and resources that extend Claude's capabilities with specialized knowledge or workflows. Use whenever the user wants to create a new skill, rewrite or audit an existing skill, add evals or memory to a skill, or package a skill for distribution.
license: Complete terms in LICENSE.txt
---

# Skill Creator

A skill is a folder that teaches Claude a repeatable job. It loads in three levels:
the frontmatter name and description are always in context (they are what triggers
the skill), the SKILL.md body loads only when the skill fires, and bundled files load
or execute only when a task needs them. Everything in this guide follows from that:
the description must trigger reliably, the body must stay lean, and depth belongs in
bundled files.

```
skill-name/
├── SKILL.md            # required: frontmatter + instructions
├── scripts/            # executable code
├── references/         # docs read into context when needed
├── assets/             # files used in output (templates, fonts, images)
├── examples/           # gold-standard outputs
├── evals.md            # binary quality checks
└── memory.md           # bounded lessons log
```

## The build loop

Build a skill the way a good team builds a product: examples first, spec before
build, minimal build, independent QA, bounded memory. Six steps; each produces a
named artifact.

### 1. Collect examples

Gather one to three concrete examples of the job: a real user request plus a
gold-standard output for each, covering the main variations. Ask the user for their
best existing samples; if they have none, draft candidates and get their approval.
Store them in `examples/`.

Skip only if the conversation already contains example requests with approved outputs.

### 2. Write the evals

Before writing any instructions, derive 5–10 checks from the examples: what must be
true of a good output? Each check is binary — pass or fail, never a score, because
a grader can't reliably tell a 3/5 from a 4/5, so scored rubrics measure noise.
Write the checks to `evals.md`. They serve as the design spec now and the quality
gate later; every instruction the skill ends up containing should exist to make
some check pass.

Check-writing method and template: [references/self-improving.md](references/self-improving.md).

### 3. Plan bundled resources

For each example, note what you would rebuild every time the job runs, then place it:

| Rebuilt every time            | Put it in     | How it loads                    |
|-------------------------------|---------------|---------------------------------|
| The same code                 | `scripts/`    | Executed; read only to patch    |
| The same knowledge (schemas, API docs, policies) | `references/` | Read into context when needed |
| The same output boilerplate (templates, fonts, logos) | `assets/` | Used in output; never read |

A resource earns its place by recurring across examples. Leave out any directory
with nothing to hold.

### 4. Build minimal

Scaffold the folder:

```bash
scripts/init_skill.py <skill-name> --path <output-dir>
```

Add `--no-self-improving` to skip the `evals.md` / `memory.md` / `examples/`
scaffolding for skills that produce no gradeable output (pure reference lookups,
one-shot utilities).

Then write, in order:

- **The description** — recipe and examples:
  [references/structure-patterns.md](references/structure-patterns.md).
- **The body** — just enough instruction to pass the evals from step 2, in
  imperative form ("Extract the text", not "You should extract the text"). Body
  layouts and how to split content into references:
  [references/structure-patterns.md](references/structure-patterns.md).
- **The resources** from step 3. Run every script once and fix what breaks before
  moving on.

Before grading, sweep the draft against
[references/anti-patterns.md](references/anti-patterns.md) and delete what it flags.

### 5. Grade with a clean-context agent

Run the grading loop in [references/self-improving.md](references/self-improving.md).
The step is done when every check in `evals.md` passes.

### 6. Maintain

After each real use, append what you learned to `memory.md` and run the pruning
pass. Memory rules, pruning mechanics, and templates:
[references/self-improving.md](references/self-improving.md).

## Frontmatter rules

`scripts/quick_validate.py <skill-dir>` enforces these; `package_skill.py` runs the
same validation before packaging.

- Allowed fields: `name`, `description`, `license`, `allowed-tools`, `metadata`,
  `compatibility`. Nothing else.
- `name`: required. Kebab-case (lowercase letters, digits, hyphens), max 64
  characters, no leading/trailing/double hyphens, matches the directory name.
- `description`: required. Max 1024 characters, no angle brackets.
- `compatibility`: optional, string, max 500 characters — only for environment
  requirements (target product, system packages). Most skills omit it.

## Packaging

```bash
scripts/package_skill.py <path/to/skill-folder> [output-dir]
```

Validates the skill, then zips it into a distributable `<skill-name>.skill` file.
Fix any reported validation errors and rerun.
