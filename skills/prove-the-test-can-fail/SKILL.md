---
name: prove-the-test-can-fail
description: >
  Use after writing a test, or before trusting one that passed — a test that
  has never failed is unverified. Do one sabotage run (break the thing under
  test, confirm the right assertion fails) and confirm each new branch is
  actually reachable by the mocks/fixtures. Triggers on "test passes", "added
  a test", "green on first run", "after-the-fact test", "is this test real",
  "mock", "coverage", and before claiming a behaviour is tested.
---

# Prove the Test Can Fail

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from cases where a test passed on the first run and proved nothing —
hardcoded-success mocks left new failure branches unexercised.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A test that has never been observed to fail is unverified — a green pass is
consistent with a test that asserts nothing, mocks away the code path, or
never reaches the branch it claims to cover. Before trusting it, make it fail
ON PURPOSE once: break the thing under test and confirm the SPECIFIC assertion
you care about is the one that goes red. Then confirm the failure branches you
added are actually reachable given the fixtures.

## Checks

- **One sabotage run per assertion that matters.** Temporarily break the
  behaviour (flip a return, remove the guard, corrupt the input) and confirm
  the intended assertion fails with a message about the right thing — not some
  unrelated setup error. Revert. A test you've only ever seen pass is a test
  you've never seen work. *(An after-the-fact e2e passed on the first run;
  disabling a load-bearing step showed the test still passed — it was
  asserting on the wrong layer entirely.)*
- **Confirm new branches are reachable by the mocks.** Adding a failure
  branch (a row-count guard, an error path, a retry) is worthless if the
  fixtures can never trigger it. For each new branch, point to the fixture
  that trips it — e.g. a `mockResolvedValueOnce(0)` that makes the row-count
  guard fire — or the branch is dead in the test. *(A guard for "zero rows
  affected" was added and "tested", but every mock returned a positive count,
  so the guard's branch was never executed.)*
- **Hardcoded-success mocks hide the code under test.** A mock that always
  returns the happy value turns the test into a check of the mock. If the
  mock's return can't vary across cases, the test can't distinguish working
  code from broken code. Vary the mock per case, or assert on a real effect.
  *(Illustrative: A payment-gateway client mock always returned `{status: "success"}`
  regardless of the request payload, so tests for a valid charge and a
  malformed one passed identically — the test verified the mock, not the
  validation logic.)*
- **Pick the fixture that forces the risky path, not the one that's easy to
  build.** When a project has a safe/native path and a custom/failure-prone one
  (a merge, a mutation, a parser), the obvious first example often routes
  through the native path and never runs your code at all — it proves the
  platform works, not your logic. Confirm at least one fixture drives the custom
  path end to end; if the natural demo bypasses it, add a minimal one that
  doesn't. *(A plan's single seed bundle turned out to be pure external-plugin
  installs the platform handles natively, so it never touched the custom
  settings/config merge-installer — the code most likely to break would have
  shipped with no end-to-end test exercising it.)*

## Pre-flight check — before you call a behaviour tested

- [ ] You saw the test FAIL at least once by deliberately breaking the thing
      under test, and the right assertion was the one that failed.
- [ ] Every new failure/edge branch has a fixture that actually reaches it.
- [ ] No assertion is satisfied purely by a hardcoded-success mock.
- [ ] At least one fixture drives the custom/failure-prone path end to end, not
      just the safe/native path the platform handles for you.

If any box is unchecked, you have a green light of unknown wiring — go make it
fail on purpose.
