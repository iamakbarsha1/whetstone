---
name: verify-absence-claims
description: >
  Use when you're about to act on a "there is no X / none exists / not found /
  nothing handles this" claim — especially one from a delegated subagent,
  research handoff, or a teammate's summary. Positive file:line claims are
  citable and checkable; absence claims are only as good as the search pattern
  that produced them. Re-grep every "X does not exist" before building on it.
  Covers the other shapes the same weakness takes: a setting absent from one
  config layer while a higher-precedence layer supplies it at runtime, a sweep
  whose count came back suspiciously short, and a tracker with no matching
  issue at a destination that has since been archived or renamed. Triggers on
  "no existing", "none found", "there's no", "doesn't exist", "nothing does X",
  "nothing references this", "safe to delete", "unused", "it isn't configured",
  "the default applies", "only N results", "file this upstream",
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

The same weakness appears wherever a conclusion rests on something not being
there. A field missing from a config file, a sweep that came back short, a
tracker with no matching issue — each is the output of a search that could
have been scoped wrong, and each reads as a settled fact. Absence is always a
statement about where you looked.

This is about trusting a negative result someone already produced. Choosing
which direction a check *you* are writing should enumerate in — scrape
references and test each resolves, or list the real artifacts and test each is
referenced — is a different problem: use `enumerate-artifacts-not-references`.

## When this fires

**Where:** Acting on a negative finding you did not produce yourself — a
subagent's research handoff, a teammate's summary, a ticket claiming nothing
handles this, a "safe to delete".

**The case this came from.** Delegated research reported that no independent
implementation of a calculation existed, so the build started writing one.
Grepping the operation rather than the function name found six inline copies;
the task was extraction, not authoring. In a second case a cache directory
carrying an "orphaned at" timestamp was called dead weight, while the lease
directory beside it still named three running processes.

**Another shape it takes.** *(Illustrative: A migration is planned around "no
callers outside this service", proven by grepping the service's own repo. The
one consumer is a scheduled job in a sibling repo that was never searched —
the same grep, run one directory higher, returns it immediately.)*

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

- **An absent setting is evidence about one layer, not about the resolved
  value.** In layered configuration, a missing field at one rung says nothing
  about what a higher rung supplies at call time. Before reporting an absence
  as proof that a default took effect, enumerate the precedence chain and
  check every layer above the one you scanned — grep the dispatcher for the
  setting name, not only the definition files. "The file does not set it" and
  "the default therefore applies" are two claims, each needing its own
  evidence. *(An audit flagged every agent definition lacking a `model:` field
  as inheriting an expensive default; the largest group was routed correctly
  all along by a framework that resolved the value from a profile and passed
  it as a call-time parameter — the top rung of a four-rung chain, while the
  scanned field sat second from the bottom.)*
- **A test proves a layer only if no other layer could produce the same
  result.** When confirming that a specific precedence rung is applied, pick a
  case whose observed value is unique to that rung. If the rung under test and
  a lower one resolve to the same value, the result is consistent with both and
  discriminates nothing. Say which observation is load-bearing and which is
  merely consistent. *(Two agents were sampled to confirm frontmatter routing
  worked. One was pinned to the same value as the environment default, so its
  result was equally consistent with the frontmatter being read and with it
  being ignored; only the agent pinned to a value no other rung could produce
  was decisive.)*
- **A surprisingly small count is a search bug until proven otherwise.** Every
  enumeration states its count, and the count is checked against an
  independently-known expected magnitude before the result is used. Filter
  recursive-grep output on the content field only, never the whole line — the
  path prefix is not the data. Iterate from a file or an explicit array rather
  than an unquoted variable, and print the element count first. *(Two sweeps in
  one session under-reported for unrelated shell reasons: an exclude filter
  matched the file-path prefix instead of the content and dropped every shipped
  file, and a loop over an unquoted variable holding 33 names ran once under a
  shell that does not word-split, reporting "swept 1, failures: 0" — which
  reads as a pass.)*
- **Resolve the live destination before publishing to it.** For any outward-
  facing action aimed at a project you do not own, treat packaged metadata as a
  hint rather than an address. Confirm the target is not archived, renamed, or
  rehomed; follow a redirect in the README over a `repository` field; re-verify
  the finding against the successor's current source, because a rename is
  exactly the change that silently fixes path- and name-shaped bugs; then
  search the tracker for duplicates. When the checks invalidate the
  instruction, go back to the requester instead of filing an adapted version.
  *(Two bug reports were about to be filed against the repository named in a
  package's metadata. It had been archived five months earlier and redirected
  to a renamed successor under a different org; re-running the checks there
  invalidated both — one bug no longer existed, the other had been open for two
  months in a more thorough form.)*

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
- [ ] Any absent-setting claim names the full precedence chain and confirms no
      higher layer supplies the value at runtime.
- [ ] Any test of a precedence rung uses a value that rung alone could have
      produced, and you said which observation is load-bearing.
- [ ] Every sweep reported its count, and the count was compared against an
      expected magnitude before the result was used.
- [ ] Any outward-facing report resolved the project's live home, confirmed the
      finding still holds there, and checked the tracker for duplicates.

If any box is unchecked, you have a failed search, not a proven absence — go
grep it yourself.
