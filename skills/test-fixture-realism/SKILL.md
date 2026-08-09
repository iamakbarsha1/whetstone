---
name: test-fixture-realism
description: >
  Use when writing tests against a shared store or with fabricated fixtures —
  a test only proves something if its fixtures mirror data reality and its
  assertions can't pass trivially. Covers asserting on rows you created (not
  aggregate counts), real referential integrity, seeded randomness and pinned
  time, fail-closed guard fixtures, and mocks that quietly load the real
  module. Triggers on "test fixtures", "seed data", "test DB", "factory",
  "mock returns", "flaky test", "assert count", "foreign key in test",
  "automock", and building any non-trivial test's setup.
---

# Test-Fixture Realism

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a recurring cluster of test failures where the fixtures didn't
match data reality or the assertion could pass without the code working.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A test proves something only if two things hold: its fixtures resemble the
data the code meets in production, and its assertions cannot pass unless the
code actually worked. Fabricated fixtures that skip referential integrity,
aggregate assertions over a shared store, unseeded randomness, and mocks that
echo the input all produce green tests that verify nothing. Build fixtures that
are real enough to exercise the code, and assertions specific enough to fail
when it breaks.

## Checks

- **Assert on the rows YOU created, not aggregates.** Against a shared DB or
  store, other data and parallel tests pollute any `count(*)` or "all rows"
  assertion. Tag the rows your test inserts (a marker, a returned id) and
  assert on exactly those. *(A test asserted a total row count; another test's
  seed data made it flap between pass and fail.)*
- **Fixtures need real referential integrity.** A foreign key must point to a
  parent row that actually exists — create the parent, use its RETURNED id.
  A made-up id either errors or silently matches nothing, and the test then
  exercises an empty join. *(A fixture used a hardcoded parent id; the join
  returned zero rows and the test asserted on emptiness without noticing.)*
- **Kill nondeterminism: seed randomness, pin the clock.** Random fixture
  values and time-derived keys make tests flaky and can collide across runs.
  Seed the RNG and pass a fixed time in (see the `inject-ambient-inputs`
  skill), so the same inputs produce the same fixtures every run. *(Fixtures
  keyed on the current time occasionally collided, producing an
  order-dependent failure.)*
- **A guard's fixture must fail closed.** When testing a validation/guard, the
  fixture that VIOLATES it must actually trip the failure path — an omitted or
  malformed field should make the assertion fail, not pass by default. This is
  the fixture side of `prove-the-test-can-fail`. *(A "reject when field
  missing" test used a fixture that still had the field, so it never exercised
  the rejection.)*
- **Watch mocks that load the real module or echo the input.** Automock and
  partial mocks can pull in the real module and run its side effects; and a
  test whose expected value is computed from the same call it's testing (a
  search that echoes its own query) passes trivially. Assert against an
  INDEPENDENT expectation, and confirm the mock isn't executing real code.

## Pre-flight check — before you trust a fixture-backed test

- [ ] Assertions target the specific rows/records the test created, not
      aggregates over a shared store.
- [ ] Every foreign key / reference points to a real parent the test created,
      using its returned id.
- [ ] Randomness is seeded and time is pinned, so fixtures are deterministic.
- [ ] Any guard test's violating fixture actually trips the failure path.
- [ ] Mocks don't secretly load the real module, and no assertion is satisfied
      by echoing the input.

If any box is unchecked, the fixture doesn't mirror reality — the green is
uninformative.
