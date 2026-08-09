---
name: findings-list-is-not-a-todo-list
description: >
  Use when re-engaged to "act on" or "fix the rest of" a review, audit, or
  recommendation list — the list is not a to-do list. Re-read each item's own
  disposition first and bucket them; some are explicitly marked no-fix, some
  need a human decision, some are scale-gated. Triggers on "fix the findings",
  "address the review", "do the rest of the recommendations", "apply the audit",
  "action these items", and acting on any list you or someone else produced
  earlier.
---

# A Findings List Is Not a To-Do List

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where "fix the rest of the findings" was nearly satisfied
by implementing every item — including ones the review itself had marked "no
fix required."

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A review, audit, or recommendation list records findings with DISPOSITIONS —
not a flat queue of tasks to execute. "Fix the rest" does not mean "implement
every remaining item." Some items are explicitly marked no-fix or accepted;
some need a decision only a human can make; some are gated on a scale you don't
have yet. Before acting, re-read each item's own verdict and bucket the list;
then do the actionable ones, skip the blessed no-ops, and surface the
decisions — and say which bucket each landed in.

## Checks

- **Re-read each item's disposition before touching anything.** Findings often
  carry their own verdict ("no fix required", "acceptable", "won't fix",
  "needs product decision", "revisit at scale"). Implementing an item the
  review deliberately closed is actively wrong, not just wasted work. *(A
  request to "fix the remaining findings" would have implemented several items
  the review had explicitly marked as requiring no change.)*
- **Bucket, don't queue.** Sort the list into: actionable-now, review-blessed
  no-op (skip), needs-a-human-decision (surface, don't guess), and scale/
  condition-gated (defer with the trigger). Only the first bucket is work.
- **State the buckets back.** Report what you're doing as the buckets, not as
  "done all findings": "3 fixed, 2 were marked no-fix so skipped, 1 needs your
  call on X, 1 deferred until Y." This prevents both over-implementing and
  silently dropping items.

## Pre-flight check — before you act on a findings list

- [ ] You re-read each item's own disposition, not just its title.
- [ ] Items are bucketed (actionable / blessed no-op / needs-decision /
      gated), not treated as one flat queue.
- [ ] No item marked no-fix/accepted was implemented.
- [ ] Decisions were surfaced to the human rather than guessed, and you stated
      the buckets back.

If any box is unchecked, you're running a queue, not honoring a review — go
re-read the dispositions.
