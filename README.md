# skills

Hand-picked and self-created skills for Claude. The one that matters here is **skill-creator**: it turns "write files agents can actually follow" into a repeatable job Claude runs for you.

If you got here from *Spend an hour on your agent files, save hours of token burn*, this is the skill the post points to. If you didn't, here's what it's for.

## What a skill is

A skill is a folder that teaches Claude a repeatable job. It loads in three levels:

- The name and description are always in context. They are what triggers the skill.
- The instructions (`SKILL.md`) load only when the skill fires.
- Bundled scripts and references load only when a task needs them.

That structure is the point. Claude carries almost nothing until the job comes up, then pulls in exactly what it needs.

## What skill-creator does

It builds and audits skills the way a good team ships a product: examples first, spec before build, minimal build, independent QA, bounded memory. Point Claude at it, describe the job you want to package, and it scaffolds the folder, writes the description so the skill triggers reliably, keeps the instructions lean, and validates the result.

Use it to:

- Create a new skill from scratch.
- Clean up procedure files or agent folders you already have.
- Add quality checks (evals) and a lessons log (memory) to a skill.
- Package a skill into a distributable file.

## How to use it

1. Download this repo, or just the `skill-creator/` folder.
2. Drop it into your skills directory: `~/.claude/skills/skill-creator/`.
3. Ask Claude to create or clean up a skill. It picks up skill-creator on its own.

To apply the article's framework to folders you already have, copy the post into a markdown file, then ask Claude to use both it and skill-creator to build a skill that audits and cleans up your procedure files.

## What's inside

| File | What it holds |
|---|---|
| `SKILL.md` | The six-step build loop and the frontmatter rules |
| `references/structure-patterns.md` | How to write the description and lay out the body |
| `references/self-improving.md` | Evals, grading, and the memory loop |
| `references/anti-patterns.md` | What to delete before you ship |
| `scripts/init_skill.py` | Scaffolds a new skill folder |
| `scripts/quick_validate.py` | Checks the frontmatter |
| `scripts/package_skill.py` | Zips a skill into a distributable file |

## Credit

skill-creator is built on Anthropic's guide to writing effective skills, upgraded with Peter Yang's approach to self-improving skills. I'd rather build on frontier guidance than recycle AI content back to you.
