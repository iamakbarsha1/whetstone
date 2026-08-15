---
name: measure-the-delta-not-the-absolute
description: >
  Use when judging whether your change is clean against a red or noisy
  baseline — failing tests you didn't touch, pre-existing lint/typecheck
  errors, flaky CI. Innocence is a claim about a delta, so prove it by
  stash-and-compare or head-vs-base under an identical harness, never by
  reading which files appear in the failure list. Triggers on "is this
  failure mine", "pre-existing failures", "red baseline", "did my change
  break this", "CI was already failing", "flaky", and before blaming or
  clearing a diff on a noisy suite.
---

# Measure the Delta, Not the Absolute

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from cases where a red or ambiguous test/lint/typecheck result was
nearly (mis)attributed to the current change when it was pre-existing or
environmental.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

On a red or noisy baseline, "my change is clean" and "this failure is mine"
are both claims about a DELTA, not an absolute. Prove them differentially:
run the same check against the code WITHOUT your change under an identical
harness, and compare. Never infer innocence (or guilt) from which files
happen to appear in a failure list — a failure can reference a file you
touched for a reason that predates you, and a failure in a file you never
opened can still be yours.

## Checks

- **Stash-and-compare, or head-vs-base.** To decide whether a failure is
  yours, capture the check's output with your change, then again without it
  (`git stash`, or run against the merge base / a clean worktree) using the
  SAME command and environment. The difference is your delta. Same failures
  before and after → not yours. New failures → yours. *(A red suite was about
  to be blamed on a diff; running the identical command on the untouched base
  showed the same reds — the change had added zero failures.)*
- **Identical harness, including untracked env.** A differential comparison
  is only valid if both runs use the same config, env vars, DB state, and
  flags. A fresh worktree or clean checkout often DROPS untracked files
  (`.env`, local fixtures) that the check depends on, producing fake new
  failures. Copy the ambient inputs into the comparison run, or the delta is
  noise. *(Illustrative: A head-vs-base run in a new worktree "found" failures that were
  really just a missing untracked `.env` the base run never had.)*
- **On a nonzero baseline, gate on NEW, not on green.** When the suite/lint/
  typecheck already has errors, exit code and total count are useless gates.
  Gate on "zero new errors that reference the changed code" — diff the error
  sets, don't compare pass/fail. A build that goes from 40 errors to 41 is
  regressing even though it was never green. *(Illustrative: A typecheck baseline held at
  62 errors for weeks; a change was cleared because the total stayed at 62,
  but diffing the error sets showed it had introduced three new errors while
  incidentally fixing three unrelated ones.)*

## Pre-flight check — before you attribute (or clear) a failure

- [ ] You ran the SAME check with and without your change (stash-and-compare
      or head-vs-base), not just once.
- [ ] Both runs used an identical harness, including untracked env/config the
      check depends on.
- [ ] On a nonzero baseline, you compared error SETS and gated on new errors,
      not on exit code or total count.

If any box is unchecked, you're reading an absolute, not a delta — go measure
the difference.
