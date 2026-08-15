---
name: distill-the-scar
description: >
  Use when you just hit a real failure worth keeping — a bug, a wrong fix, a
  wasted hour — and want to turn it into a reusable skill instead of a private
  lesson. Turns one concrete failure into a Whetstone-shaped SKILL.md: extract
  the transferable invariant, write it so an agent can apply it without the
  original context, and gate it with the validator. Triggers on "make this a
  skill", "turn this into a rule", "capture this lesson", "distill this
  failure", "add a skill for this", "postmortem into a skill", and any moment
  you catch yourself saying "I'll remember this next time."
---

# Distill the Scar

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where the skill-making method itself lived only in one
person's head — every existing skill was forged the same way, but the way was
never written down, so it couldn't be handed to an agent or a contributor.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A skill is a scar with the pain removed and the lesson kept. It comes from
**one concrete failure**, not from general advice. If you cannot name the
single case that produced it — what broke, what the plausible-but-wrong move
was, and how you know the real cause — you are writing advice, not a skill,
and it will not survive contact with a real agent under load.

Distill in five moves. Do them in order; skipping the first two is how you
get shapeless "best practice" that reads well and changes nothing:

1. **Capture the raw scar.** Write down the actual failure before you
   generalize: the real command, the real output/error, the wrong hypothesis
   that felt right, and the evidence that finally located the true cause.
   Sanitize names and secrets, keep the mechanics exact. Vague memory here
   produces vague skills.
2. **Extract the one transferable invariant.** Ask: what rule, applied at the
   moment of the failure, would have prevented it — stated so it holds in
   codebases that share nothing with this one? One failure yields one
   invariant. If you find two, that is two skills.
3. **Write it in the anatomy.** Mirror an existing skill exactly — do not
   invent a new shape:
   - Frontmatter `name` (kebab-case, matches the directory) and a folded
     `description` that opens with **"Use when …"** and ends with a concrete
     **"Triggers on …"** list of the phrases and situations that should fire
     it. The description is the whole retrieval surface; a skill that never
     triggers is dead weight.
   - `**Type:**`, author, "Distilled from a case where …", licence, and
     feedback lines.
   - `## The core rule` — the invariant, in one paragraph.
   - `## Checks` — for a multi-rule skill, each rule as a bullet ending in a
     one-line sanitized **`*(real case)*`** grounding it in an actual scar. A
     single-rule skill may instead fold that one rule and its case into `## The
     core rule` (as a **"Real case (sanitized):"** paragraph) and omit
     `## Checks`.
   - `## Pre-flight check` — a checklist the agent runs *before* it claims the
     work is done, with one checkbox per check, phrased so an unchecked box
     means "not finished."
4. **Name it for the invariant, not the story.** A plain imperative that
   states the rule — `verify-absence-claims`, `measure-the-delta-not-the-
   absolute` — beats a clever title. The name is a handle the agent greps for
   under pressure; match the local convention of the skills already present.
5. **Gate it.** Run `python3 scripts/validate_skills.py`. It enforces the
   frontmatter, the `**Type:**` line, `## The core rule`, the pre-flight
   section, the directory-name match, and — when a `## Checks` section is
   present — that every check carries a `*(real case)*` and the pre-flight has a
   checkbox for each. A skill that fails the validator does not merge — the
   shape is not decoration, it is what makes the skill usable under load.

**Real case (sanitized):** A skills repository grew to nineteen entries, each
genuinely distilled from a real failure. But the distilling itself was tacit —
captured live by an observer step, then hand-shaped by whoever was at the
keyboard. The plausible-but-wrong move was to trust that the observer log already
*was* the method; that it wasn't became provable the moment a new contributor,
handed only that log, could not produce a twentieth skill that matched the first
nineteen. The method was never a written artifact, so the founder was the single
point of failure for the repo's whole premise.
Writing the method down as this skill — capture, extract, shape, name, gate —
turned "how we make skills" from tribal knowledge into a step anyone can run,
and made the repository self-hosting: the skill that forges the skills now
lives beside the ones it forged.

## Pre-flight check — before you call a skill distilled

- [ ] You can name the **single concrete failure** it came from — what broke,
      the plausible wrong move, and how the real cause was proven.
- [ ] The skill states **one transferable invariant**, not a bundle of advice;
      a second invariant became a second skill.
- [ ] The `description` opens with "Use when …" and carries a concrete
      "Triggers on …" list — it will actually fire when the situation recurs.
- [ ] Every check carries a sanitized real case (or, for a single-rule skill,
      the core rule does), and there is a **pre-flight checklist**; names and
      secrets are sanitized, mechanics kept exact.
- [ ] `python3 scripts/validate_skills.py` prints `OK` — the skill passes the
      same gate as every other skill in the repository.

If any box is unchecked, you have a lesson, not a skill — go finish the
distillation.
