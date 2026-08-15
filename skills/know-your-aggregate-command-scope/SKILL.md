---
name: know-your-aggregate-command-scope
description: >
  Use before trusting a named aggregate command — a `test`, `lint`,
  `type-check`, or `build` script that wraps a tool. Open it and confirm what
  it actually runs, how it forwards args, and whether it caches, because a
  green only means what the command covered. Triggers on "npm run test",
  "type-check passes", "lint is clean", "the build is green", "run the tests",
  "--testPathPattern", monorepo/workspace scripts, and citing a script's exit
  code as proof.
---

# Know Your Aggregate Command's Scope

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from cases where a wrapper script exited 0 while checking only part
of what was assumed, and where a test filter silently ran the whole cached
suite.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A named aggregate command (`npm run type-check`, `lint`, `test`, `build`) is a
wrapper, and its exit code means only "what this wrapper actually ran passed" —
which is often less, or more, than you assume. Before citing a green as proof,
open the script and confirm three things: WHICH targets it covers, HOW it
forwards your arguments, and WHETHER it caches. A pass over the wrong scope is
not evidence about the code you changed.

## Checks

- **Confirm which targets it covers.** In a monorepo/workspace, a top-level
  script may check only one project, or only the ones it lists, not everything
  you touched. *(Illustrative: A `type-check` script exited 0 but only ran against one of the
  three packages the change modified; the other two were never type-checked.)*
  Read the script and confirm it spans everything your change affects.
- **Confirm how it forwards your args.** Wrapper scripts mangle or drop
  arguments. A filter you pass may be ignored, applied to the wrong runner, or
  widened. *(A `--testPathPattern` passed through a wrapper was dropped, so the
  command silently ran the entire suite from cache instead of the one file
  intended.)* Verify the flag reached the underlying tool as intended.
- **Confirm whether it caches, and whether the cache is stale.** A cached
  runner can report a green that reflects a previous state, not your current
  code. *(Illustrative: A lint runner's incremental cache kept a file's previous clean
  result because its modification time hadn't changed after a rebase, so a
  newly introduced rule violation in that file was never re-linted and the
  run stayed green.)* Know if the command caches and force a clean run when
  the result must reflect the latest change.
- **Gate on new failures over a nonzero baseline.** If the aggregate already
  has errors, exit code is meaningless; gate on "zero new failures referencing
  the changed code" (see `measure-the-delta-not-the-absolute`), not on green.
  *(A test suite already had failing tests unrelated to the change; the run's
  exit code was nonzero before and after, so citing "the tests are red" said
  nothing until the failing test names were diffed and one new failure traced
  to the change turned up.)*

## Pre-flight check — before you cite an aggregate command as proof

- [ ] You confirmed the command covers ALL targets your change touched.
- [ ] You confirmed your args (filters/flags) reached the underlying tool as
      intended.
- [ ] You know whether it caches, and forced a clean run if the result must be
      current.
- [ ] On a nonzero baseline, you gated on new failures, not on exit code.

If any box is unchecked, the green describes the wrapper, not your change — go
read what the command runs.
