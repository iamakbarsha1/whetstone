---
name: manufacture-review-independence
description: >
  Use when reviewing your own work, or when the author-equals-reviewer guard
  is deliberately overridden — real independence is gone, so manufacture it:
  parallel independently-scoped sub-reviews plus an adversarial re-read of
  source for every high-severity claim, and treat cross-reviewer disagreement
  as a pointer to the boundary file that settles it. Triggers on "self-review",
  "review my own PR", "author is the reviewer", "no one else can review",
  "code review my changes", and conflicting review findings.
---

# Manufacture Review Independence

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from self-review situations where the author was also the reviewer,
and from parallel reviewers giving conflicting severities because the deciding
file sat outside both their scopes.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A review's value comes from independence. When author and reviewer are the
same (or the same model, same context, same session), that independence is
gone and leniency creeps in. Don't pretend the review is independent —
MANUFACTURE independence structurally: split the work into independently-
scoped sub-reviews, run an adversarial pass whose job is to refute each
high-severity claim by re-reading the source, and when two views disagree,
resolve it by reading the file that decides — never by averaging.

## Checks

- **Split into independently-scoped sub-reviews.** Instead of one lenient pass
  over everything, review in separate scoped passes (security, correctness,
  contract-boundaries, tests) each blind to the others' conclusions, then
  merge. Different scopes surface what a single sympathetic read glosses over.
  *(Illustrative: A combined pass over a multi-tenant export feature missed a missing
  tenant-scoping check; rerunning the same diff as a dedicated security-only
  pass caught it immediately, because that pass wasn't also weighing style.)*
- **Adversarially re-read source for every high-severity claim.** For each
  High/Critical finding, run a pass whose explicit goal is to REFUTE it by
  reading the actual code, and default to "not real" if the source doesn't
  confirm it. This kills both the author's blind spots and plausible-but-false
  findings. A claim that survives a genuine refutation attempt is worth
  acting on. *(Illustrative: A finding claimed a race condition from the diff alone; an
  adversarial re-read of the full function showed a mutex already guarded
  the section, and the finding was dropped.)*
- **Disagreement points to the boundary file — go read it.** When two
  reviewers (or two passes) assign conflicting severity to the same fact, that
  gap is not noise to average away; it means the deciding evidence lives in a
  file NEITHER of them fully read. Identify that boundary file, read it, and
  let it settle the call. *(Two parallel reviewers rated the same issue High
  and Low; the truth lived in a shared module outside both their assigned
  scopes — reading it resolved the conflict decisively.)*
- **For security/correctness-critical code, iterate adversaries until they
  converge.** After your own tests pass, run independent adversarial passes —
  each a distinct attack lens (encoding, casing, framing, boundary) — and
  require each to EMPIRICALLY confirm a bypass by running the code, not
  theorize one. Feed every confirmed bypass back as a regression test and
  re-run; the stop condition is convergence — rounds that surface only ceilings
  you've consciously accepted — not a single clean round. *(A fail-closed secret
  scrubber passed all its author-written tests, but four rounds of parallel
  adversaries each found real high-severity bypasses the tests never imagined —
  UUID-shaped tokens, uppercase/short hex, narrow-wrapped PEM bodies — until the
  rounds converged on documented, accepted ceilings.)*

## Pre-flight check — before you trust a self-review

- [ ] The review ran as multiple independently-scoped passes, not one
      sympathetic read.
- [ ] Every High/Critical finding survived an adversarial re-read of the
      actual source (or was dropped).
- [ ] Any cross-reviewer disagreement was resolved by reading the deciding
      boundary file, not by averaging severities.
- [ ] For security/correctness-critical code, adversarial passes ran until they
      converged on accepted ceilings — not stopped at the first clean round —
      and each confirmed bypass became a regression test.

If any box is unchecked, the review inherited the author's blind spots — go
manufacture the independence.
