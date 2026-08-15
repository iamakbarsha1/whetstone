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

Distilled from a case where a detached backfill resolved a relative config path
against a working directory it never inherited, silently ran for hours on
default settings, and then reported success against a start-time target a
concurrent hook had already moved.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose
with credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If the methodology produces a wrong call, or a rule
here needs sharpening, open an issue on the repository or contact the author
at the profile link above with what happened and what you expected. If the problem is the agent not
following a rule below rather than the rule itself, that's an execution
failure — acknowledge and correct it, don't file it as methodology feedback.

## The core rule

A detached job does not inherit the session that launched it — not its working
directory, not its environment, not its wakefulness — and the moment anything
else writes the same corpus, `remaining = target − done` stops being true.
Launch with every input absolute and the host kept awake, confirm the config is
live from the running process's behaviour (not the file on disk), and verify
completion against the corpus's current per-item state, not the job's own
counters.

## Checks

- **Make every path absolute at launch.** A backgrounded or detached process is
  not guaranteed the launcher's cwd, env, or shell state; a relative input
  (`./config.json`, `../data`) can silently fall back to a built-in default when
  the inherited cwd differs. Pass every path-like flag absolute at the command
  line, not by "run it from the right directory". If a scheduler sets its own
  cwd you can't control, log the resolved absolute path of every input at
  process start so a wrong fallback shows up in the log instead of silently.
  *(A detached run resolved `./config` against a cwd it never inherited, used
  defaults with no error, and ran ~6 hours on the wrong settings — found only
  later by degraded throughput.)*
- **Keep the host awake for unattended runs.** Sleep and power throttling
  (macOS App Nap, laptop suspend) can pause or slow a detached process for hours
  without killing it, indistinguishable from "still running" if you aren't
  watching. Wrap any multi-hour unattended run in the platform keep-awake —
  `caffeinate`, `systemd-inhibit`, `powercfg /requestsoverride`. *(A ~17h
  unattended run lost roughly 40% of its wall time — about 7 hours — to host
  sleep the process couldn't prevent; a keep-awake wrapper would have cut it to
  ~6–7h.)*
- **Confirm the config is live at runtime, not correct on disk.** A correct file
  proves nothing about what the running process loaded. Confirm the intended
  setting is ACTIVE from an early runtime signal — a logged effective-config
  line, a worker count matching the setting, an observed rate consistent with
  it. *(A run whose config was fixed on disk kept using the old value the
  already-started process had loaded; the file check passed while behaviour
  didn't.)*
- **A smoke test is a throughput floor, not an ETA.** A short sample can't see
  host sleep, per-item size variance, or time-of-day throttling — all of which
  dominate a multi-hour wall time and can multiply a naive `smoke_rate × N`
  estimate several times over. Report the extrapolation as "at least this long"
  and re-measure the live rate mid-run. (Overlaps `verify-through-the-real-path`'s
  smoke check; kept here for the background-job flow.) *(A 17-item smoke at
  ~6s/item projected ~6h; the real ~4,300-item run took ~17h once host sleep,
  per-item variance, and rate-limit windows were in play.)*
- **Reconcile a shared corpus in three buckets, not by subtraction.** If
  anything else can add, remove, or change items mid-run, `remaining = target −
  done` is false: the residual is real failures PLUS items that arrived or
  changed during the run. Split it into **processed-ok** / **failed** (with
  reasons) / **arrived-during-run**, and expect an external committer — a hook
  watching the corpus — to commit the job's partial output as a side effect, so
  the job's own final count reads low with no data loss. (If nothing else writes
  the corpus, this collapses to two buckets — still verify by per-item state,
  not arithmetic.) *(A backfill's residual of 151 was first read as 151
  failures, but only 43 were real — the other ~108 items had arrived mid-run,
  and a Stop-hook's 16 incremental commits had obscured the job's true
  processed count.)*
- **Verify completeness by per-item state, not job arithmetic.** Confirm against
  the corpus's CURRENT state, not the start-time snapshot: the working
  tree/output location is clean AND every item's live state (a hash, a status
  field, a timestamp) matches its expected post-processing state — checked live,
  not assumed from the job's self-reported counters. *(Completion was confirmed
  per-item by a content hash, not the job's counter — items the counter called
  done carried no hash and were caught only by the live state check.)*
- **Schedule the mop-up before calling it done.** Everything in the
  arrived/changed-during-run bucket needs its own follow-up pass. Don't fold it
  into "failed", and don't call the job complete until that pass is run or
  scheduled. *(A mop-up pass over all 151 residuals — not just the 43 real
  failures — cleared them to zero; folding the ~108 mid-run arrivals into
  "failed" would have miscounted them permanently.)*

## Pre-flight check — before declaring the job done

Re-read the checks above against what actually happened, not what was intended:

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
