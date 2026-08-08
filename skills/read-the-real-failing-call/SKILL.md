---
name: read-the-real-failing-call
description: >
  Use when hardening against a failure mode or fixing an intermittent/partial
  failure — instrument the real failing invocation before and after, because
  a plausible hypothesis is not a diagnosis. Triggers on "why is this
  failing", "flaky", "intermittent failures", "high failure rate", "harden
  this", "add retries", "it times out sometimes", and diagnosing a fix that
  didn't move the failure rate.
---

# Read the Real Failing Call

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where a plausible, well-tested fix left the real cause
completely untouched.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A plausible failure hypothesis is not a diagnosis. When hardening against a
hypothesized failure mode, capture the ACTUAL raw output/error of a real
failing invocation both BEFORE and AFTER the fix. Don't infer the cause from
symptoms or a plausible upstream theory. A fix that targets the hypothesized
cause can pass all unit tests and still leave the real cause untouched; only
a before/after on the live failing call proves which cause dominated.

**Real case (sanitized):** A failure rate around two-thirds on an LLM CLI was
pre-diagnosed as timeout plus missing retry. Building configurable timeout,
retry, and concurrency barely moved it. Instrumenting one real failing call
showed the prompt was drowning the actual input in a tens-of-thousands-of-
character context dump; the model was responding to the dump, not the task.
Capping the dump dropped the failure rate from roughly two-thirds to about
5% — a cause the timeout/retry theory never touched.

## Pre-flight check — before you call the failure fixed

- [ ] You captured the raw output/error of a real failing invocation BEFORE
      the fix (not just symptoms or a theory).
- [ ] You re-ran the same real invocation AFTER the fix and compared.
- [ ] The measured failure rate on real inputs actually moved — green unit
      tests alone do not prove the dominant cause was addressed.

If any box is unchecked, you have a hypothesis, not a diagnosis — go read the
real call.
