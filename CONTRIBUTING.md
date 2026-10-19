# Contributing to whetstone

whetstone skills come from real failures, not general advice. A good skill
names a specific thing that went wrong and the rule that would have prevented
it — written so an agent (or human) can apply it without the original context.

One rule outranks the rest: a case is lived or it is marked
`*(Illustrative: …)*`, and nothing in the file may claim otherwise. A skill
whose header calls a case lived while its own bullet marks the same case
illustrative is a contradiction to fix, not a style choice — CI can check the
marker is present, never that it is honest.

## The bar

A skill belongs here if it is:

- **Distilled from a concrete failure** — not "best practices in general." Every
  skill names the real case it came from; where a check adds an example not
  drawn from a logged incident, it is marked `*(Illustrative: …)*` rather than
  dressed up as a lived one.
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
5. **When this fires** — a `**Where:**` line naming the kind of work the skill
   belongs to, then the same situation twice: `**The case this came from.**`
   (retold from the failure the skill was distilled from) and `**Another shape
   it takes.**` (a different domain, marked `*(Illustrative: …)*`). Two
   examples, because one case reads as a story about someone else's stack and
   two read as a shape. Three rules CI enforces: the three lead-ins appear in
   that order inside the section, each with text after it; the section sits
   between the core rule and the pre-flight; and the second example carries the
   `*(Illustrative: …)*` marker. Draw the first example only from material the
   file treats as lived — if the matching `## Checks` bullet is marked
   `*(Illustrative: …)*`, that case is not available to you here, and a second
   example that is the first one with the nouns swapped is not a second
   example.
6. **Checks** — the individual rules, each ending in a one-line sanitized real
   case in the form `*(what went wrong)*`. A single-rule skill may fold that one
   rule and its case into **The core rule** and omit the `## Checks` section
   (see `confirm-the-premise-first`).
7. **Pre-flight check** — a checklist that must all pass before claiming done.
   Every check above needs a matching checkbox; an ungated check is a silent
   hole in the "fail loudly" guarantee.

CI enforces the load-bearing parts of this contract (`scripts/validate_skills.py`):
`## The core rule` is present, `## When this fires` is present with all three of
its lines, every `## Checks` bullet carries a grounding case `*(…)*` — a real
one, or one marked `*(Illustrative: …)*` — and the pre-flight
has at least one checkbox per check. A skill that skips them can't merge. (CI
checks the marker is present; it cannot tell a real case from a fabricated one,
so honesty about which is which is on the author — see `distill-the-scar`.)

It also checks that a new skill actually reaches the catalogue: every
`skills/*/` directory needs a README table row — with a non-empty Example cell —
and a card in `docs/index.html` carrying a `<p class="eg">` example line,
every row and card must point at a directory that exists, and every declared
skill count — the README badge, the site's meta tags, hero, spelled-out section
header and per-section counts — must equal the number of directories. The count
lives in eight places, so adding a skill without propagating it is a drift the
validator now fails on rather than a release catching it later.

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
