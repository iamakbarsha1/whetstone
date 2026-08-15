# Contributing to whetstone

whetstone skills come from real failures, not general advice. A good skill
names a specific thing that went wrong and the rule that would have prevented
it — written so an agent (or human) can apply it without the original context.

## The bar

A skill belongs here if it is:

- **Distilled from a concrete failure** — not "best practices in general." Every
  skill states the real case it came from.
- **Client-agnostic** — no client/project/personal detail. The lesson
  generalizes; scrub identifying specifics.
- **Actionable under load** — a short rule set an agent can actually follow
  mid-task, ending in a pre-flight checklist that fails loudly if a box is
  unchecked.

If it reads like a blog post, it's not ready. If it reads like a checklist a
tired engineer would thank you for at 3am, it is.

## Skill format

One skill = one folder under `skills/<name>/` containing `SKILL.md`. Optional
supporting files (`references/*.md`, `scripts/*`) live in the same folder.

Frontmatter is a contract (CI enforces it):

```markdown
---
name: your-skill-name          # MUST equal the folder name
description: >                  # trigger phrases live here
  Use when <situation>. Triggers on "phrase a", "phrase b", ...
---
```

Match the structure of the existing skills:

1. Title + `**Type:**` line (open-source / internal)
2. `**Created by**` attribution
3. `**Licence:**` (CC BY 4.0) and `**Feedback & Support:**` lines
4. **The core rule** — one paragraph
5. **Checks** — the individual rules, each ending in a one-line sanitized real
   case in the form `*(what went wrong)*`. A single-rule skill may fold that one
   rule and its case into **The core rule** and omit the `## Checks` section
   (see `confirm-the-premise-first`).
6. **Pre-flight check** — a checklist that must all pass before claiming done.
   Every check above needs a matching checkbox; an ungated check is a silent
   hole in the "fail loudly" guarantee.

CI enforces the load-bearing parts of this contract (`scripts/validate_skills.py`):
`## The core rule` is present, every `## Checks` bullet carries a `*(real case)*`,
and the pre-flight has at least one checkbox per check. A skill that skips them
can't merge.

Copy an existing skill as a template — `verify-through-the-real-path` is a good
reference.

## Submitting

- **Suggest a skill first** (optional but faster): open a
  [new-skill suggestion](../../issues/new?template=new-skill-suggestion.yml).
- **Or open a PR** adding the skill folder. Before pushing, run the validator:

  ```sh
  python3 scripts/validate_skills.py
  ```

  It checks every `SKILL.md` has `name`+`description`, the folder name matches
  `name`, and the plugin manifests stay consistent. CI runs the same check.

- Feedback on an existing skill's methodology → open a
  [methodology-feedback issue](../../issues/new?template=methodology-feedback.yml).

By contributing you agree your contribution is licensed under CC BY 4.0.
