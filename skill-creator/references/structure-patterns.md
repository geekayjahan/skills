# Structure Patterns

Recipes for the two things that decide whether a skill fires and reads well: the
description and the body layout. Read this while writing step 4 of the build loop.

## Contents

- [The description](#the-description)
- [Body layouts](#body-layouts)
- [Splitting content into references](#splitting-content-into-references)
- [Output formats](#output-formats)

## The description

The description carries the entire triggering decision (see the loading model in
SKILL.md's intro) — so a "When to Use" section in the body does nothing.

- Write in third person: the description is injected into a system prompt.
- State what the skill does AND when to use it, naming concrete triggers: file
  types, task names, phrases a user would actually say.
- Err on the pushy side ("Use whenever..."). Skills undertrigger far more often
  than they overtrigger.
- Describe triggering conditions, not the workflow. A description that summarizes
  the steps invites the agent to follow the summary and skip the body.

```yaml
# Bad - won't fire, no triggers
description: Helps with documents

# Bad - summarizes workflow; agent may follow this instead of reading the body
description: Edits posts by checking the hook, tightening prose, then grading against evals

# Good - what + when, concrete triggers, third person
description: Extract text and tables from PDF files, fill forms, merge documents.
  Use whenever the user mentions PDFs, forms, or document extraction.
```

Name the skill after the job it does (`processing-pdfs`, `brand-guidelines`),
never generically (`helper`, `utils`, `docs`). Format limits: SKILL.md's
frontmatter rules.

## Body layouts

Pick the one that matches the job; mix only when the job genuinely mixes:

- **Workflow** — sequential process. Overview, then numbered steps, each producing
  an artifact. Use when order matters.
- **Task** — independent operations. Quick start, then one section per operation.
  Use for tool collections (merge PDFs / split PDFs / extract text).
- **Reference** — standards and specifications. Guidelines, then specifics (colors,
  typography, schema). Use when the skill constrains rather than instructs.

## Splitting content into references

The body holds the workflow and the decisions; depth goes to `references/`. Two
rules make the split work:

1. **Link every reference directly from SKILL.md, with the condition for reading
   it** ("For form filling, see references/forms.md"). Chains of references get
   partially read and silently dropped.
2. **Organize by domain or variant so only the relevant file loads.** A BigQuery
   skill splits into `finance.md` / `sales.md` / `product.md`; a deploy skill into
   `aws.md` / `gcp.md` / `azure.md`. A sales question then costs only `sales.md`.

Give any reference file over 100 lines a table of contents, so a preview shows its
full scope.

## Output formats

When the skill's output must follow a shape, show the shape — a template beats a
paragraph describing one:

- **Strict**: "ALWAYS use this exact structure" + the skeleton, when downstream
  tooling or brand rules depend on it.
- **Flexible**: "Sensible default, adapt as needed" + the skeleton, when no
  downstream tool or brand rule depends on the shape.

For style rather than structure, give one input/output pair per output type from
the gold examples. One excellent pair calibrates better than several mediocre ones.
