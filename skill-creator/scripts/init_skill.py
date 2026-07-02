#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path> [--no-self-improving]

Examples:
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private --no-self-improving
"""

import sys
from pathlib import Path

# Make emoji-laden prints safe on Windows consoles (cp1252) without PYTHONUTF8.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: What the skill does AND when to use it. This is the skill's only trigger - recipe in skill-creator references/structure-patterns.md.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences on what this skill enables.]

## [TODO: First main section]

[TODO: Instructions. Body layouts: skill-creator references/structure-patterns.md.]

## Resources

[TODO: Link each bundled file with the condition for using it, e.g.
"For form filling, see references/forms.md". Delete unused directories.]
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""Example helper script for {skill_name}. Replace or delete."""


def main():
    print("Example script for {skill_name}")


if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference for {skill_title}

Placeholder for knowledge the model lacks: schemas, API docs, policies,
detailed procedures. Replace or delete. Structure rules: skill-creator
references/structure-patterns.md.
"""

EXAMPLE_ASSET = """Placeholder for files used in the skill's output (templates, fonts,
images, boilerplate). Assets are never read into context. Replace or delete.
"""

EVALS_TEMPLATE = """# Evals - {skill_name}

Binary checks, cap ~12. Grading loop: skill-creator references/self-improving.md.

1. [TODO: question answerable yes/no by pointing at the output]
2. [TODO: ...]
3. [TODO: ...]
"""

MEMORY_TEMPLATE = """# Memory - {skill_name}

One line per lesson, newest first, cap ~12. Rules: skill-creator references/self-improving.md.

- [TODO: YYYY-MM-DD: lesson]
"""

EXAMPLE_OUTPUT = """# Example: [TODO: name a gold-standard output]

Replace with a best-in-class output for {skill_name}. Keep 1-3.
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path, self_improving=True):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created
        self_improving: Also scaffold evals.md, memory.md, and examples/

    Returns:
        Path to created skill directory, or None if error
    """
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content, encoding="utf-8")
        print("✅ Created SKILL.md")
    except Exception as e:
        print(f"❌ Error creating SKILL.md: {e}")
        return None

    try:
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name), encoding="utf-8")
        example_script.chmod(0o755)
        print("✅ Created scripts/example.py")

        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title), encoding="utf-8")
        print("✅ Created references/api_reference.md")

        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET, encoding="utf-8")
        print("✅ Created assets/example_asset.txt")

        if self_improving:
            evals_path = skill_dir / 'evals.md'
            evals_path.write_text(EVALS_TEMPLATE.format(skill_name=skill_name), encoding="utf-8")
            print("✅ Created evals.md")

            memory_path = skill_dir / 'memory.md'
            memory_path.write_text(MEMORY_TEMPLATE.format(skill_name=skill_name), encoding="utf-8")
            print("✅ Created memory.md")

            examples_dir = skill_dir / 'examples'
            examples_dir.mkdir(exist_ok=True)
            example_output = examples_dir / 'example.md'
            example_output.write_text(EXAMPLE_OUTPUT.format(skill_name=skill_name), encoding="utf-8")
            print("✅ Created examples/example.md")
    except Exception as e:
        print(f"❌ Error creating resource directories: {e}")
        return None

    print(f"\n✅ Skill '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Complete the TODO items in SKILL.md (description first - it is the trigger)")
    print("2. Customize or delete the example files in scripts/, references/, and assets/")
    if self_improving:
        print("3. Fill evals.md, add a gold-standard output to examples/, keep memory.md current")
        print("4. Run quick_validate.py to check the skill structure")
    else:
        print("3. Run quick_validate.py to check the skill structure")

    return skill_dir


def main():
    args = [a for a in sys.argv[1:] if a != '--no-self-improving']
    self_improving = '--no-self-improving' not in sys.argv[1:]

    if len(args) != 3 or args[1] != '--path':
        print("Usage: init_skill.py <skill-name> --path <path> [--no-self-improving]")
        print("\nSkill name must satisfy quick_validate.py's naming rules")
        print("(e.g., 'my-data-analyzer').")
        print("\nOptions:")
        print("  --no-self-improving   Skip evals.md/memory.md/examples/ scaffolding")
        print("                        (for skills with no gradeable output)")
        print("\nExamples:")
        print("  init_skill.py my-new-skill --path skills/public")
        print("  init_skill.py my-api-helper --path skills/private --no-self-improving")
        sys.exit(1)

    skill_name = args[0]
    path = args[2]

    print(f"🚀 Initializing skill: {skill_name}")
    print(f"   Location: {path}")
    print()

    result = init_skill(skill_name, path, self_improving=self_improving)

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
