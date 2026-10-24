# whetstone

[![validate-skills](https://github.com/iamakbarsha1/whetstone/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/iamakbarsha1/whetstone/actions/workflows/validate-skills.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
[![skills](https://img.shields.io/badge/skills-30-brightgreen.svg)](#skills)

Agent skills honed on real work. Each skill is a short, self-contained rule set
distilled from **one concrete failure** — written so an AI coding agent (or a
human) can apply the lesson without the original context.

A whetstone sharpens a blade. These sharpen the agent.

## What makes a whetstone skill

Not general advice — a scar. Every skill here:

- comes from a **real failure** (each names the sanitized case it was distilled from),
- is **client-agnostic** — no project or company detail; the lesson generalizes,
- ends in a **pre-flight checklist** that fails loudly when a box is unchecked.

If it reads like a blog post, it doesn't belong. If it reads like a checklist a
tired engineer would thank you for at 3am, it does.

### Anatomy of a skill

Every `SKILL.md` follows the same shape:

```markdown
---
name: verify-through-the-real-path      # matches the folder name
description: >
  Use before claiming something works... Triggers on "verify",
  "confirm it works", "is it done", "benchmark", ...   # trigger phrases
---
# Verify Through the Real Path, Not a Proxy
**Type:** Open-source ...                # provenance, licence, feedback
## The core rule                         # one paragraph
## When this fires                       # Where + the distilled case + a second, illustrative one
## Checks                                # each rule + a grounding case (real, or *(Illustrative:)*)
## Pre-flight check                      # the checklist that gates "done"
```

The `description` carries the trigger phrases, so a skill-aware agent surfaces
the right skill when the situation matches. `## When this fires` is for the
reader who already has the skill open and needs to place it: one line on the
kind of work it belongs to, then the situation twice — once as the failure the
skill was distilled from, once in a different domain so the shape generalizes.
CI checks all three are present, in order, inside the section, and that the
second one carries its `*(Illustrative: …)*` marker.

## Skills

### Verify & prove

| Skill | Use it when | Example |
|-------|-------------|---------|
| [`verify-through-the-real-path`](skills/verify-through-the-real-path) | Before claiming something works, is done, safe, or fast — verify through the actual trigger, real data, and representative conditions, not a stand-in. | A direct-call check passed; the real hook ran from another working directory, never found the config, and silently never fired. |
| [`prove-the-test-can-fail`](skills/prove-the-test-can-fail) | After writing a test, or before trusting a green one — make it fail on purpose once, and confirm new branches are reachable by the mocks. | A green end-to-end test stayed green after a load-bearing step was disabled — it was asserting on the wrong layer. |
| [`spike-falsification`](skills/spike-falsification) | Validating a third-party dependency (API, SDK, contract, protocol) before building on it — execute against the real deployed artifact and try to falsify your design assumptions, don't just demo the happy path. | Research returned correct signatures; the deployed bytecode had 1-based indexing, and the "soulbound" token transferred. |
| [`measure-the-delta-not-the-absolute`](skills/measure-the-delta-not-the-absolute) | Judging whether your change is clean on a red or noisy baseline — prove it by stash-and-compare, not by which files appear in the failure list. | A red suite was about to be blamed on a diff; the identical command on the untouched base produced the same reds. |
| [`test-fixture-realism`](skills/test-fixture-realism) | Writing tests against a shared store or fabricated fixtures — make fixtures mirror data reality and assertions unable to pass trivially. | A fixture's hardcoded parent id made the join return nothing, and the test happily asserted on the empty result. |
| [`know-your-aggregate-command-scope`](skills/know-your-aggregate-command-scope) | Before citing a `test`/`lint`/`type-check`/`build` script as proof — confirm what it actually runs, how it forwards args, and whether it caches. | A `--testPathPattern` was dropped by the wrapper, so the green came from the whole suite, served from cache. |
| [`enumerate-artifacts-not-references`](skills/enumerate-artifacts-not-references) | Writing or reviewing a completeness gate — enumerate the real artifacts and check each is referenced, rather than scraping references out of prose and checking each resolves; keep a separate bounded pass for truncation. | A gate scraped nineteen illustrative paths out of a document's prose and reported each MISSING, burying the two real findings. |
| [`running-long-background-jobs`](skills/running-long-background-jobs) | Launching or verifying a long-running/detached job, or reconciling a batch against a corpus other processes also write to. | A backfill's residual of 151 was read as 151 failures; only 43 were real, the rest had arrived mid-run while a hook committed underneath it. |
| [`third-party-tool-onboarding`](skills/third-party-tool-onboarding) | Standing up a third-party tool on a host that fails one of its declared constraints — one probe that works proves one layer, not the rule; verify the artifact you received, and probe install, configure and run separately. | A pinned smoke test passed on an unsupported runtime, so the version floor was written off; the next unpinned install exited 0 with a build years out of date. |

### Plan & design

| Skill | Use it when | Example |
|-------|-------------|---------|
| [`plan-cross-encoding-review`](skills/plan-cross-encoding-review) | Reviewing an implementation plan or spec — catch the bug where one intent is encoded twice and the copies disagree. | The prose promised a rollback on failed retry; the pasted code skipped it, and the implementer transcribed the code. |
| [`confirm-the-premise-first`](skills/confirm-the-premise-first) | Designing when a choice depends on a technical property (local vs remote, reversible vs not) — state the ground truth before asking downstream questions. | A backend believed to run inference on-device was always remote — several data-exposure answers collapsed with the premise. |
| [`audit-before-you-build`](skills/audit-before-you-build) | Starting an implementation task from a ticket/checklist/spec — grep for what already exists first; trackers record conversations, not deliverables. | A milestone item was already ~90% shipped as a side effect; one grep for the route name turned "build" into gap-closing. |
| [`inject-ambient-inputs`](skills/inject-ambient-inputs) | Writing logic that reads the clock, randomness, env, or handles — pass them in as parameters so the pure core tests with no mocking machinery. | Rules calling the clock would have needed fake timers in every test; passing the date in gave ~30 tests with no mocks. |
| [`consistency-is-local-first`](skills/consistency-is-local-first) | Adding code to an existing module — match the nearest sibling's pattern; a repo-wide convention is the default only when the module has none. | Illustrative: applying the repo-wide convention would have made the new code the only outlier in a module that had settled on another way. |
| [`validate-the-users-proposed-mechanism`](skills/validate-the-users-proposed-mechanism) | A user names a platform/tool/library — treat it as a proposed mechanism; grep the artifact for disqualifiers before agreeing, separate intent from mechanism. | The requested serverless platform kills the long-lived `setInterval` workers the app depends on — one grep surfaced it. |
| [`harness-config-audit`](skills/harness-config-audit) | Applying an external write-up to a configuration you already run — produce a per-surface COVERED/PARTIAL/MISSING delta, and verify every name, version and command the guide cites against the installed build. | A guide was applied layer by layer; the audit found no permission rules defined at all, while the prompt gating unrestricted execution was switched off. |

### Change safely

| Skill | Use it when | Example |
|-------|-------------|---------|
| [`grep-the-blast-radius`](skills/grep-the-blast-radius) | Changing a shared contract (flag, column, type, endpoint) — the retired name is your consumer index; grep the whole workspace and run cross-boundary suites. | A shared union gained a member; a sibling package's exhaustive `switch` lost exhaustiveness while the editor's tests stayed green. |
| [`diff-each-side-against-merge-base`](skills/diff-each-side-against-merge-base) | Resolving a merge/rebase conflict — markers show where git gave up, not the full delta; auto-merge silently drops fields. | Auto-merge dropped struct fields present on both the base and one side, with nothing appearing between the conflict markers. |
| [`verify-absence-claims`](skills/verify-absence-claims) | Acting on a "none exists / not found" claim, especially from delegated research — re-grep it; absence is only as good as the search pattern. | Research said no shared implementation existed; grepping the operation instead of the function name found six inline copies. |
| [`negative-invariant-testing`](skills/negative-invariant-testing) | Protecting a "never does X" constraint — a behavioural test can't see an unused capability; assert structurally on the mechanism's existence. | A "never holds custody of funds" property had no test — nothing exercises custody, so nothing behavioural could go red. |
| [`safe-data-export`](skills/safe-data-export) | Exporting sensitive or large data into a path inside a git tree — make the destination uncommittable and verify it (gitignore first, then `git check-ignore` + `git status`) before the data exists on disk. | A memory dump carrying an email address, an org name and handles was aimed inside a public repo before any ignore rule existed. |

### Diagnose & review

| Skill | Use it when | Example |
|-------|-------------|---------|
| [`read-the-real-failing-call`](skills/read-the-real-failing-call) | Hardening against a failure mode — instrument the real failing call before and after, because a plausible hypothesis is not a diagnosis. | Timeout-and-retry was built for a two-thirds failure rate; the real cause was a context dump drowning the prompt. |
| [`manufacture-review-independence`](skills/manufacture-review-independence) | Reviewing your own work (author == reviewer) — replace lost independence with scoped parallel passes and adversarial re-reads of the source. | Two reviewers split High vs Low on the same fact; the deciding evidence sat in a module outside both their scopes. |
| [`findings-list-is-not-a-todo-list`](skills/findings-list-is-not-a-todo-list) | Acting on a review/audit/recommendation list — re-read each item's disposition and bucket them; some are marked no-fix, some need a human decision. | Illustrative: "fix the rest" nearly implemented several items the review had explicitly marked as requiring no change. |
| [`scan-generated-files-for-artifacts`](skills/scan-generated-files-for-artifacts) | Reviewing or signing off a file an agent wrote with a tool — grep its head and tail for leaked harness residue (stray tags, fence fragments, content past EOF); passing tests don't cover non-code bytes. | An approved markdown file compiled and tested clean, then shipped with a leaked tool-call closing tag in its tail. |
| [`macos-malware-triage`](skills/macos-malware-triage) | Checking a running macOS machine for compromise or unwanted persistence — walk fixed coverage axes instead of recall, hand back the checks your privileges can't reach, and separate malicious findings from stale and privacy-relevant ones. | A "scan my Mac" check improvised from recall reported clean — the two root-only checks it skipped were never named in the output. |

### Author & distill

| Skill | Use it when | Example |
|-------|-------------|---------|
| [`distill-the-scar`](skills/distill-the-scar) | Turning a real failure into a reusable skill — capture the scar, extract one transferable invariant, write it in the anatomy, and gate it with the validator. The method that forged every skill here, made repeatable. | Nineteen skills existed and the method behind them did not — a contributor handed only the log could not produce a twentieth. |
| [`name-the-boundary-between-siblings`](skills/name-the-boundary-between-siblings) | Adding or renaming a skill that will sit beside others — keyword coverage makes it findable, not pickable; grep your trigger words against the installed set and write a reciprocal boundary line into both files. | A whole-repo security-audit skill shipped beside a per-file one; both matched "security audit", neither named the other. |
| [`a-memory-is-not-a-trigger`](skills/a-memory-is-not-a-trigger) | Relying on a stored memory, a recalled note, a session-start banner, or a description-matched skill to make a required action fire every run. Passive context is read, not executed — gate must-dos with a deterministic hook or forced invocation, not a note you hope gets recalled. | A must-do named in both a recalled memory and a startup banner went undone all session — nothing in the loop executed it. |
| [`publish-oss-repo`](skills/publish-oss-repo) | Publishing a repo, or auditing one that has working code but still reads as neglected — signal maintenance with a canonical (machine-detected) license, tagged releases, topics, and CI that enforces the artifact's contract, each verified through the platform's own API. | A hand-written licence summary made GitHub display "Other", and several version bumps had no tag or release behind them. |

## Install

### As a Claude Code plugin (recommended)

Add the marketplace, then install the plugin — all skills come with it:

```sh
/plugin marketplace add iamakbarsha1/whetstone
/plugin install whetstone@whetstone-skills
```

Run these inside Claude Code. `whetstone@whetstone-skills` is
`plugin@marketplace` — the plugin is `whetstone`, the marketplace is
`whetstone-skills`.

### Manual copy

Each skill is a self-contained folder in the Claude Code skill layout
(`SKILL.md` with `name` + `description` frontmatter). Copy one:

```sh
cp -R skills/verify-through-the-real-path ~/.claude/skills/
```

Or all of them:

```sh
cp -R skills/* ~/.claude/skills/
```

The `description` frontmatter carries trigger phrases, so a skill-aware agent
surfaces each one when the situation matches.

### Other agents / plain reading

Every `SKILL.md` is plain Markdown — the rules and pre-flight checklists read
fine on their own. Any agent that can load a system prompt or reference file
can use them: paste the skill body in, or point your tool's context at the
file. Only the plugin auto-discovery above is Claude Code-specific.

## Contributing

New skills come from real failures, not general advice. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the bar and the skill format, and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Validate locally with
`python3 scripts/validate_skills.py` (CI runs the same check on every PR).

Changes are tracked in [CHANGELOG.md](CHANGELOG.md). Feedback on any skill's
methodology is welcome as a [repository issue](../../issues/new/choose).

## Licence

All skills are released under [CC BY 4.0](LICENSE) — share and adapt for any
purpose with credit to akbarsha (https://github.com/iamakbarsha1).
