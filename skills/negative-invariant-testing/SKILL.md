---
name: negative-invariant-testing
description: >
  Use when a system has a load-bearing "never" constraint — never holds funds,
  never logs secrets, never calls a forbidden API, never writes to a table,
  never blocks the event loop. Behavioural tests can't observe a capability
  that isn't exercised yet, so write a STRUCTURAL test that trips on the mere
  existence of the forbidden mechanism. Triggers on "never does X", "must
  not", "forbidden", "invariant", "safety constraint", "guardrail", "should
  not be possible", and hardening a property a future edit could quietly
  violate.
---

# Negative-Invariant Testing

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where a load-bearing "the system never does X" constraint
had no test, so a future edit adding the forbidden construct would break it
invisibly.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A constraint of the form "the system NEVER does X" can't be protected by a
behavioural test, because a behavioural test can only observe behaviour that
is exercised — and the whole point is that X is never exercised today. The
danger is a future edit that ADDS the forbidden capability; nothing runs it,
so nothing goes red. Protect a negative invariant with a STRUCTURAL test that
fails on the mere existence of the mechanism — introspect the schema, the AST,
the exports, the dependency list — so the guard trips the moment someone
introduces X, before it's ever called.

## Checks

- **Assert on existence, not on execution.** Write the test against the
  structure that would have to exist for X to be possible: a forbidden import
  or export, a schema column that would let the system hold state it shouldn't,
  a function signature, a config key, a dependency. The test passes because
  the mechanism is absent and fails the instant it appears. *(A "never holds
  custody of funds" property had no test; a structural check that fails if a
  balance-holding field or transfer-out capability is ever added would trip on
  the first line of the violation, not the first execution.)*
- **Name the invariant in the failure message.** A structural test that fires
  is cryptic without context ("unexpected export found"). State the invariant
  it protects and why, so the engineer who tripped it understands they've
  crossed a designed line, not hit a lint quirk. *(A guard against
  reintroducing a banned network call fired with only "forbidden pattern
  matched"; the engineer read it as flaky lint noise, silenced the check, and
  the banned call shipped on the next release.)*
- **Prefer the narrowest structural signal.** Trip on the specific forbidden
  construct (this import, this column, this capability), not a broad proxy
  that also flags legitimate code. A negative-invariant test that cries wolf
  gets deleted, and then the invariant is unprotected again. *(A "never opens
  a raw socket" guard matched any file containing the word "socket"; it
  flagged a legitimate client-library import, got dismissed as noise, and was
  deleted, leaving the real invariant unprotected.)*

## Pre-flight check — before you rely on a "never" constraint

- [ ] The invariant has a STRUCTURAL test (schema/AST/exports/deps), not only
      a behavioural one.
- [ ] The test fails on the EXISTENCE of the forbidden mechanism, before it is
      ever executed.
- [ ] The failure message names the invariant and why it matters.
- [ ] The structural signal is narrow enough not to flag legitimate code.

If any box is unchecked, the "never" is a comment, not a guard — go make it
structural.
