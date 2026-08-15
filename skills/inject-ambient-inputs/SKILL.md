---
name: inject-ambient-inputs
description: >
  Use when writing or refactoring logic that reads ambient state — the clock
  (now/today), randomness, environment variables, a DB/HTTP handle, the
  filesystem, the current user. Ambient reads are the main reason otherwise
  pure logic becomes un-unit-testable; pass them in as parameters and split
  the pure decision from the I/O so tests need no mocking machinery. Triggers
  on "Date.now", "new Date()", "hard to test", "mock the clock", "fake
  timers", "random in tests", "reads env", "make this testable", "pure
  function".
---

# Inject Ambient Inputs

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where business rules reading the clock directly would
have forced fake-timer mocking in every test; passing the current time in as a
value gave dozens of tests with zero mocks.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

Ambient inputs — the clock, randomness, environment, DB/HTTP handles, the
filesystem — are the main reason logic that is otherwise pure becomes painful
to unit-test: to test it you must intercept a global, which needs fake timers,
env stubbing, or a mocking framework in every test. Don't reach for the global
inside the decision logic. PASS ambient values in as parameters and keep a
thin I/O shell that reads them once at the edge. The pure core then tests with
plain inputs and plain assertions, no machinery.

## Checks

- **Take the value as an argument, don't read the global.** A function that
  branches on "today" should accept `today` as a parameter, not call the clock
  itself; one that needs a random pick should accept a seed or the chosen
  value. The caller at the edge reads the real clock/rng once and passes it
  down. *(Rules that called the clock directly would have needed fake-timer
  setup in every test; taking the date as a field turned that into ~30 tests
  with zero mocks.)*
- **Split the pure decision from the I/O.** Separate "decide what to do given
  these values" (pure, no ambient reads, no side effects) from "gather the
  values and apply the effect" (thin, ambient, barely tested). The pure half
  gets exhaustive cheap tests; the shell needs only a smoke test. *(A pricing
  function fetched the customer record and computed the discount in one call,
  so testing the discount math meant standing up a database; pulling the
  fetch out into a thin wrapper let the pricing rules run as plain
  input/output tests.)*
- **The edge reads ambient state exactly once.** Resolve now/env/handles at a
  single boundary and thread them through, rather than re-reading them deep in
  the call tree. Scattered ambient reads reintroduce the untestability you
  just removed and cause subtle drift. *(A billing job read the clock at the
  start of the run and again inside a nested helper; a run that crossed
  midnight between the two reads billed one day short.)*

## Pre-flight check — before you call ambient-dependent logic testable

- [ ] The decision logic takes clock/random/env/handles as PARAMETERS, not via
      global reads.
- [ ] Pure decision logic is separated from the ambient I/O shell.
- [ ] Ambient state is read once at the edge and threaded through, not
      re-read deep in the tree.
- [ ] The core's tests use plain inputs with no fake-timer/env-stub/mock
      machinery.

If any box is unchecked, the logic still depends on hidden globals — go inject
them.
