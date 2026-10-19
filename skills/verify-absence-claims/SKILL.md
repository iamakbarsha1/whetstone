---
name: verify-absence-claims
description: >
  Use when you're about to act on a "there is no X / none exists / not found /
  nothing handles this" claim — especially one from a delegated subagent,
  research handoff, or a teammate's summary. Positive file:line claims are
  citable and checkable; absence claims are only as good as the search pattern
  that produced them. Re-grep every "X does not exist" before building on it.
  Triggers on "no existing", "none found", "there's no", "doesn't exist",
  "nothing does X", "nothing references this", "safe to delete", "unused",
  research/subagent handoffs, and any negative finding you didn't verify
  yourself.
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

This is about trusting a negative result someone already produced. Choosing
which direction a check *you* are writing should enumerate in — scrape
references and test each resolves, or list the real artifacts and test each is
referenced — is a different problem: use `enumerate-artifacts-not-references`.

## Checks

- **Re-grep every load-bearing "none exists".** Before you act on an absence
  claim (build the thing that "doesn't exist yet", skip a case that "never
  happens"), run your own search with SEVERAL phrasings — the canonical name,
  likely synonyms, partial tokens, the inline pattern as well as a named
  helper. Absence found by one narrow query is not absence. *(Delegated
  research concluded no shared implementation of a calculation existed;
  grepping the operation instead of the function name found six inline copies.)*
- **Prove the probe could have found it.** A malformed query and a true absence
  return the same silence: a path that doesn't exist, a typo'd flag, a command
  erroring to empty stdout. Before an empty result counts as evidence, run the
  same probe against something you know is present, or inspect the level you're
  querying. *(A versioned install tree was checked for skills at
  `<cache>/<plugin>/skills`, came back empty, and was reported as an empty
  install; the tree nests by version, so nothing was ever at that level and the
  install was in fact complete.)*
- **Distinguish "not found" from "not present".** A subagent or teammate can
  only report what their search covered. Rephrase their "X does not exist" as
  "X not found by <their method>" and check whether their scope even included
  where X would live (other packages, generated code, inline copies, tests).
  *(Illustrative: A subagent reported no rate limiter existed after searching the
  application code only; the limiter lived in a shared middleware package
  outside its search path.)*
- **Before deleting, check holders, not tombstones.** A status marker records
  how something reached its current state (superseded, deprecated, orphaned at
  a timestamp); it says nothing about who is holding the thing right now. Those
  are different questions, and a well-formed query of the wrong evidence class
  answers neither. Enumerate the real holders — lease files, open handles, lock
  entries, live process IDs — and say which ones you checked and how you
  established each was gone. *(A cache directory carried an "orphaned at"
  timestamp and was reported as dead weight, safe to delete; the lease
  directory beside it held four entries, three of them naming processes that
  were still running.)*
- **Label unverified absences as such.** When you must pass an absence claim
  onward without re-checking, mark it "verify: none found" rather than stating
  it as fact, so the next reader knows it's a search result, not a guarantee.
  *(Illustrative: A handoff note stated "no retry logic exists" as settled fact instead of
  as unverified; the next engineer wrapped calls in a new retry layer around
  code that already retried internally, doubling the delay.)*

## Pre-flight check — before you build on "X doesn't exist"

- [ ] You re-ran the search yourself with multiple phrasings (name, synonyms,
      inline pattern), not just trusted the report.
- [ ] The probe itself is known to work — you ran it against a known-present
      instance, or confirmed the path and level you queried actually exist.
- [ ] The search scope actually covered where X would live (all packages,
      generated code, tests, inline copies).
- [ ] Before any deletion, you enumerated the live holders and named which you
      checked, rather than trusting a marker describing how it got there.
- [ ] Any absence you pass onward unverified is labeled "verify: none found",
      not stated as fact.

If any box is unchecked, you have a failed search, not a proven absence — go
grep it yourself.
