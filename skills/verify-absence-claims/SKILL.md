---
name: verify-absence-claims
description: >
  Use when you're about to act on a "there is no X / none exists / not found /
  nothing handles this" claim — especially one from a delegated subagent,
  research handoff, or a teammate's summary. Positive file:line claims are
  citable and checkable; absence claims are only as good as the search pattern
  that produced them. Re-grep every "X does not exist" before building on it.
  Triggers on "no existing", "none found", "there's no", "doesn't exist",
  "nothing does X", research/subagent handoffs, and any negative finding you
  didn't verify yourself.
---

# Verify Absence Claims

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where delegated research reported "no independent
implementation of X exists" and the build then found several inline
duplicates — the negative claim was simply wrong.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A positive claim ("X is at file:line") carries its own proof — you can open
the file. A negative claim ("there is no X") carries none; it's only as strong
as the search that failed to find X, and a search that used the wrong term,
scope, or spelling produces a confident false "none". Never build on an
absence claim you didn't verify. Treat every "X doesn't exist" as "X was not
found by <specific search>", and re-run a broader search before you rely on it —
especially when the claim came from a delegated agent whose search you can't
see.

## Checks

- **Re-grep every load-bearing "none exists".** Before you act on an absence
  claim (build the thing that "doesn't exist yet", skip a case that "never
  happens"), run your own search with SEVERAL phrasings — the canonical name,
  likely synonyms, partial tokens, the inline pattern as well as a named
  helper. Absence found by one narrow query is not absence. *(Delegated
  research concluded no shared implementation of a calculation existed;
  grepping the operation instead of the function name found six inline copies.)*
- **Distinguish "not found" from "not present".** A subagent or teammate can
  only report what their search covered. Rephrase their "X does not exist" as
  "X not found by <their method>" and check whether their scope even included
  where X would live (other packages, generated code, inline copies, tests).
  *(Illustrative: A subagent reported no rate limiter existed after searching the
  application code only; the limiter lived in a shared middleware package
  outside its search path.)*
- **Label unverified absences as such.** When you must pass an absence claim
  onward without re-checking, mark it "verify: none found" rather than stating
  it as fact, so the next reader knows it's a search result, not a guarantee.
  *(Illustrative: A handoff note stated "no retry logic exists" as settled fact instead of
  as unverified; the next engineer wrapped calls in a new retry layer around
  code that already retried internally, doubling the delay.)*

## Pre-flight check — before you build on "X doesn't exist"

- [ ] You re-ran the search yourself with multiple phrasings (name, synonyms,
      inline pattern), not just trusted the report.
- [ ] The search scope actually covered where X would live (all packages,
      generated code, tests, inline copies).
- [ ] Any absence you pass onward unverified is labeled "verify: none found",
      not stated as fact.

If any box is unchecked, you have a failed search, not a proven absence — go
grep it yourself.
