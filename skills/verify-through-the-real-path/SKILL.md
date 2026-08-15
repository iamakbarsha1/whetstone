---
name: verify-through-the-real-path
description: >
  Use before claiming something works, is done, is safe, or is fast — verify
  through the actual trigger, real data, and representative conditions, not a
  convenient stand-in. Triggers on "verify", "confirm it works", "is it done",
  "benchmark", "ETA for a long run", "is this edge case reachable", "test the
  hook", "smoke test", and before declaring a fix complete.
---

# Verify Through the Real Path, Not a Proxy

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from repeated cases where a check passed against a convenient
stand-in while the real thing was broken.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A convenient stand-in is not the thing you claimed works. Verify through the
actual trigger, real data, and representative conditions — not a shortcut
that inherits your ambient context or hides the tail.

## Checks

- **Real trigger, not a direct call.** A feature fired by a hook, cron, or
  detached/background process is only verified by exercising the ACTUAL
  trigger — invoke the real hook/script with a representative payload, from a
  representative working directory, with the real environment — and observe
  the end effect (the commit, the file, the side effect). A direct call to
  the underlying function is a unit test: it inherits your ambient
  cwd/env/resolved paths that the real trigger never has. *(A sync-triggered
  feature passed a direct-call check, but the real event hook that fires it
  ran from a different working directory, never found the relative config, and
  silently never fired.)*
- **Smoke test = throughput floor, not an ETA.** A smoke test proves the
  pipeline works and gives a throughput FLOOR — not a wall-clock estimate.
  For multi-hour jobs, wall time is governed by tail effects a short sample
  can't see (host sleep/power throttling, item-size variance, throttling
  windows). Re-measure the instantaneous completion rate over time; don't
  trust smoke-rate × N. *(A short smoke run extrapolated to a few hours; the
  real run took roughly three times as long.)*
- **Micro-benchmark = upper bound.** A speedup that removes a FIXED cost
  (process startup, connection, allocation) is only as large as that cost's
  share of total time. A trivial input inflates that share — benchmark on a
  REPRESENTATIVE workload, and if you cite a micro-benchmark, label it an
  upper bound. *(A startup-strip showed a ~3.5x speedup on trivial input but
  only ~25% on the real workload, where a variable cost the micro-benchmark
  omitted dominates.)*
- **"Unreachable / safe / cosmetic" is only as strong as its invariant.**
  Name the invariant the verdict rests on, then check whether it is enforced
  LOCALLY (a guard in code you own) or merely assumed of an upstream. If
  merely assumed, verify it against live data and state it as an EMPIRICAL
  ceiling, not a structural one — and note the one-line local guard that
  would make it structural. *(A divert guard called "effectively unreachable"
  actually self-disabled when an upstream field was null; it was safe only
  because that upstream always populated the field — confirmed against tens
  of thousands of live rows, zero nulls — which is empirical, not
  guaranteed.)*
- **`--help` can execute.** Before running an unfamiliar CLI subcommand "just
  to see the flags", confirm the arg parser's unknown-flag behaviour first
  (read the dispatch code or grep for `--help`/usage). A parser that ignores
  unknown flags runs the subcommand with defaults — on a mutating/
  side-effecting subcommand, `--help` triggers a real execution. Prefer a
  guaranteed-safe probe: `--version`, a confirmed dry-run, or reading source.
  *(A `--help` probe on an unfamiliar mutating subcommand executed a real run
  — live side effects on dozens of records — before printing anything.)*

## Pre-flight check — before you claim it works

Re-read the checks above against what actually happened, not what you
intended:

- [ ] The claim was verified through the real trigger/path, not a convenient
      direct call that inherits favorable ambient context.
- [ ] Any timing claim from a smoke test is labeled a floor, and the live
      rate was checked on a representative run.
- [ ] Any benchmark cited is on a representative workload, or labeled an
      upper bound.
- [ ] Any "safe/unreachable/cosmetic" verdict names its invariant and states
      whether that invariant is locally enforced or only empirically true.
- [ ] Any unfamiliar CLI probed for its flags used a guaranteed-safe route
      (`--version`, a confirmed dry-run, or reading source), never `--help` on a
      mutating subcommand whose arg parser might execute it.

If any box is unchecked, the claim is not verified — go back and check it.
