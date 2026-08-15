---
name: plan-cross-encoding-review
description: >
  Use when reviewing an implementation plan, spec, or task breakdown before
  handing it to an implementer — catches the class of bug where one intent is
  encoded twice and the two encodings silently disagree. Triggers on "review
  this plan", "check this spec", "self-review the plan", "before I implement",
  "fixture values", "edge case in the plan", and writing task breakdowns with
  hardcoded fixtures or guards.
---

# Plan Cross-Encoding Review

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from plan-review failures where one intent was written down twice
and the two copies drifted apart.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

When a plan encodes one intent two ways, diff the two encodings against each
other before shipping the plan. Divergence between two representations of the
same intent is a latent bug that the implementer will resolve in the wrong
direction.

## Checks

- **Redundant-value agreement.** Any two hardcoded values related by a pure
  function (epoch↔date, hash↔slug, size↔count) are a latent contradiction
  unless one is computed from the other or the pair is explicitly verified.
  Reused magic pairs multiply the blast radius across tasks. *(A test fixture
  hardcoded a Unix epoch and its human date as an unchecked pair; the date was
  wrong, and the same pair reused across tasks would have multiplied the bug —
  a failing test caught it just before it shipped.)*
- **Prose-vs-code agreement.** When a task gives both a prose description of
  an edge case and the code, and they disagree, the implementer transcribes
  the code and silently ignores the prose. For every edge-case behaviour you
  describe in prose, point to the exact code line that implements it; if the
  code doesn't, fix the code or delete the prose claim. Never ship a plan
  whose prose promises behaviour the code block doesn't deliver — especially
  on data-loss or security edges. *(A task's prose promised a failed retry
  would roll back its partial write, but the pasted code skipped that step;
  the implementer copied the code as written, and partial writes silently
  landed on every retried failure.)*
- **Guard shape and ordering.** When a plan specifies a guard over
  machine-generated text that embeds user data, match the forbidden
  STRUCTURE (e.g. a specific trailer line), not bare keywords that also occur
  legitimately as data (e.g. reserved words appearing inside user-supplied
  names). And order side-effecting steps so the validating/throwing step runs
  BEFORE any durable state advance (validate → act → commit state last), so a
  failure is a safe retry rather than corruption. *(A guard blocked the bare
  word "reserved" meant to catch one trailer line, and also rejected a
  legitimate user name containing it; the check ran after the record was
  already committed, so the false rejection surfaced only after durable
  state had already changed.)*

## Pre-flight check — before you ship the plan

- [ ] Every pair of related hardcoded values is computed or explicitly
      verified against each other.
- [ ] Every prose edge-case claim names the code line that implements it.
- [ ] Every guard matches a structure, not bare keywords, and validates
      before advancing durable state.

If any box is unchecked, the plan is not review-clean — fix it inline.
