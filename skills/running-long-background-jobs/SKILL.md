---
name: running-long-background-jobs
description: >
  Use before launching any long-running, backgrounded, detached, or nohup'd
  process (backfills, batch migrations, bulk data processing, multi-hour scrapes,
  crawls), and again when verifying it finished correctly. Also use when
  reconciling a batch job against a corpus (files, DB rows, records) that
  other processes — event hooks, cron, other agents — also write to during
  the run. Triggers on "background job", "long-running job", "detached
  process", "backfill", "batch job", "nohup", "disown", "unattended run",
  "overnight job".
---

# Running Long Background Jobs

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from field lessons about launching and verifying long-running,
detached, and background jobs against corpora that other processes also
write to.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose
with credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If the methodology produces a wrong call, or a rule
here needs sharpening, open an issue on the repository or contact the author
at the profile link above with what happened and what you expected. If the problem is the agent not
following a rule below rather than the rule itself, that's an execution
failure — acknowledge and correct it, don't file it as methodology feedback.

## Trigger

Before backgrounding or detaching any job expected to run unattended for
more than a few minutes. Before declaring such a job "done." Before trusting
a smoke test's timing. Before reconciling a batch job's results against a
corpus other processes can also modify.

## Inputs Required

- The command being launched, and every config/input/output path it reads —
  know which of these are relative vs. absolute.
- Whether anything else (a hook, cron, another agent, a scheduler) reads or
  writes the same corpus/output location during the run.
- The target count or completion criterion for the job, and how it's
  currently measured (a counter, a file count, a commit, a log line).

## Process

### Step 1 — Make every input absolute at launch time

A backgrounded or detached process is not guaranteed to inherit the cwd, env,
or shell state of the session that launched it. If the job resolves any
input from a relative path (`./config.json`, `../data`), it can silently
fall back to a built-in default when the inherited cwd differs — with no
error, discovered only much later via wrong behavior or degraded throughput.

Convert every cwd-relative input to an absolute path explicitly at the
command line (e.g. `--config /abs/path/to/config.json`, not reliance on
"run it from the right directory"). Do this for every path-like flag, not
just the one you're actively changing.

### Step 2 — Keep the host awake for unattended multi-hour runs

Host sleep or power-saving throttling (macOS App Nap, laptop suspend) can
pause or slow a detached process for hours without killing it, and this
looks identical to the job "just running" if you're not watching. For any
run expected to span an unattended stretch (overnight, multi-hour), wrap it
in the platform's keep-awake mechanism — `caffeinate` on macOS,
`systemd-inhibit` on Linux, `powercfg /requestsoverride` on Windows — rather
than trusting the machine to stay responsive on its own.

### Step 3 — Verify the config is live at runtime, not just correct on disk

A correct config file proves nothing about what the running process actually
loaded. Before walking away, confirm the intended setting is ACTIVE via an
early runtime signal: a logged effective-config line, a process/worker count
matching the setting, or an observed throughput consistent with it. Checking
the file is not verification; checking the process's observed behavior is.

### Step 4 — Treat any smoke test as a throughput floor, not an ETA

A short smoke run only measures steady-state throughput on a small,
unrepresentative sample. It does not see host sleep, per-item size variance,
or time-of-day throttling — all of which dominate wall time on a real
multi-hour run and can multiply the naive `smoke_rate × N` estimate several
times over. Report smoke-test extrapolations as a floor ("at least this
long"), not a deadline, and re-measure the instantaneous completion rate
periodically during the real run instead of trusting the initial estimate.

### Step 5 — Reconcile completion by three buckets, not by subtraction

If the job's corpus is shared — anything else can add, remove, or modify
items in it while the job runs — then `remaining = target − done` stops
being true partway through. The residual is genuine failures PLUS items
that arrived (or changed) during the run. Reconcile explicitly into three
buckets: **processed-ok**, **failed** (with reasons), and **arrived/changed
during run**. Don't report or act on a raw subtraction against the
job's start-time target.

Also expect external committers: a hook or scheduled process watching the
same corpus may commit the job's own partial output incrementally as a
side effect of its normal behavior. When that happens, the job's own final
commit or log will show fewer items than were actually processed — that's
the external committer's doing, not a sign of data loss.

### Step 6 — Verify completeness by per-item state, not job-time arithmetic

Confirm completion against the CURRENT state of the corpus, not the
snapshot the job started with. A reliable invariant: working tree / output
location is clean (no uncommitted or unprocessed diffs) AND every item's
current state matches its expected post-processing state (a hash, a status
field, a timestamp) — checked live, not assumed from the job's self-reported
counters.

### Step 7 — Plan a mop-up pass

Anything landing in the "arrived/changed during run" bucket from Step 5
needs its own follow-up pass. Don't fold it silently into "failed," and
don't consider the job complete until it's scheduled or run.

### Pre-flight check — before declaring the job done

Re-read Steps 1–6 against what actually happened, not what was intended:

- [ ] Every path-like input was passed absolute, not relied on via cwd.
- [ ] The effective config was confirmed live at runtime (not just read
      from disk).
- [ ] Host keep-awake was used if the run was unattended and multi-hour.
- [ ] Any smoke-test timing claim is labeled a floor, and the actual live
      rate was checked at least once mid-run.
- [ ] Completion is reported as three buckets (processed-ok / failed /
      arrived-during-run), not a single "done" count from subtraction.
- [ ] Completeness was verified against the corpus's CURRENT per-item state,
      not the job's start-time counters.
- [ ] A mop-up pass exists (scheduled or already run) for anything in the
      arrived-during-run bucket.

If any box is unchecked, the job is not verified — go back and check it
before reporting success.

## Output Format

A completion report with:

1. **Processed-ok** — count, with the verification evidence used (per-item
   state check, not a job-reported counter alone).
2. **Failed** — count and reasons, if any.
3. **Arrived/changed during run** — count, and whether they're covered by
   an already-run or scheduled mop-up pass.
4. **Runtime evidence** — the early signal that confirmed the intended
   config was actually active (not just present on disk).
5. **Timing note** — if a pre-run smoke-test estimate was given, whether
   actual wall time matched, exceeded, or was flagged mid-run as running
   long.

## Tools Used

Whatever backgrounding mechanism the platform provides (`nohup`, `disown`,
`tmux`/`screen`, a job scheduler, or a managed background-task API); a
host keep-awake utility for unattended runs; access to the corpus's
per-item state (file hashes, DB rows, status fields) to reconcile against.
No specific vendor or product is required — the methodology applies to any
detached/background execution mechanism.

## Notes

- **Closed corpus (no other writers):** the three-bucket reconciliation in
  Step 5 collapses to two (processed-ok, failed). Still verify by per-item
  state rather than arithmetic — a stale or off-by-one target count is just
  as easy to hide behind subtraction as a concurrent writer is.
- **cwd cannot be controlled** (e.g., a managed scheduler that sets its own
  working directory): add an explicit debug/print step that logs the
  resolved absolute path for every input at process start, so a wrong
  fallback is visible in logs rather than silent.
- This skill governs launching and verifying background jobs specifically.
  General claims-need-evidence discipline for any completion claim (tests,
  builds, PRs) belongs to a broader verification skill if the environment
  has one — this skill only adds the parts specific to detached/background
  execution and shared-corpus reconciliation.
