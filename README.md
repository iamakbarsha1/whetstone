# whetstone

Agent skills honed on real work. Each skill here is a short, self-contained
rule set distilled from a concrete failure or hard-won lesson during real
engineering sessions, written so an AI coding agent (or a human) can apply it
without the original context.

A whetstone sharpens a blade. These sharpen the agent.

## Skills

### Verify & prove

| Skill | Use it when |
|-------|-------------|
| [`verify-through-the-real-path`](skills/verify-through-the-real-path) | Before claiming something works, is done, safe, or fast — verify through the actual trigger, real data, and representative conditions, not a stand-in. |
| [`prove-the-test-can-fail`](skills/prove-the-test-can-fail) | After writing a test, or before trusting a green one — make it fail on purpose once, and confirm new branches are reachable by the mocks. |
| [`measure-the-delta-not-the-absolute`](skills/measure-the-delta-not-the-absolute) | Judging whether your change is clean on a red or noisy baseline — prove it by stash-and-compare, not by which files appear in the failure list. |
| [`test-fixture-realism`](skills/test-fixture-realism) | Writing tests against a shared store or fabricated fixtures — make fixtures mirror data reality and assertions unable to pass trivially. |
| [`know-your-aggregate-command-scope`](skills/know-your-aggregate-command-scope) | Before citing a `test`/`lint`/`type-check`/`build` script as proof — confirm what it actually runs, how it forwards args, and whether it caches. |
| [`running-long-background-jobs`](skills/running-long-background-jobs) | Launching or verifying a long-running/detached job, or reconciling a batch against a corpus other processes also write to. |

### Plan & design

| Skill | Use it when |
|-------|-------------|
| [`plan-cross-encoding-review`](skills/plan-cross-encoding-review) | Reviewing an implementation plan or spec — catch the bug where one intent is encoded twice and the copies disagree. |
| [`confirm-the-premise-first`](skills/confirm-the-premise-first) | Designing when a choice depends on a technical property (local vs remote, reversible vs not) — state the ground truth before asking downstream questions. |
| [`audit-before-you-build`](skills/audit-before-you-build) | Starting an implementation task from a ticket/checklist/spec — grep for what already exists first; trackers record conversations, not deliverables. |
| [`inject-ambient-inputs`](skills/inject-ambient-inputs) | Writing logic that reads the clock, randomness, env, or handles — pass them in as parameters so the pure core tests with no mocking machinery. |
| [`consistency-is-local-first`](skills/consistency-is-local-first) | Adding code to an existing module — match the nearest sibling's pattern; a repo-wide convention is the default only when the module has none. |
| [`validate-the-users-proposed-mechanism`](skills/validate-the-users-proposed-mechanism) | A user names a platform/tool/library — treat it as a proposed mechanism; grep the artifact for disqualifiers before agreeing, separate intent from mechanism. |

### Change safely

| Skill | Use it when |
|-------|-------------|
| [`grep-the-blast-radius`](skills/grep-the-blast-radius) | Changing a shared contract (flag, column, type, endpoint) — the retired name is your consumer index; grep the whole workspace and run cross-boundary suites. |
| [`diff-each-side-against-merge-base`](skills/diff-each-side-against-merge-base) | Resolving a merge/rebase conflict — markers show where git gave up, not the full delta; auto-merge silently drops fields. |
| [`verify-absence-claims`](skills/verify-absence-claims) | Acting on a "none exists / not found" claim, especially from delegated research — re-grep it; absence is only as good as the search pattern. |
| [`negative-invariant-testing`](skills/negative-invariant-testing) | Protecting a "never does X" constraint — a behavioural test can't see an unused capability; assert structurally on the mechanism's existence. |

### Diagnose & review

| Skill | Use it when |
|-------|-------------|
| [`read-the-real-failing-call`](skills/read-the-real-failing-call) | Hardening against a failure mode — instrument the real failing call before and after, because a plausible hypothesis is not a diagnosis. |
| [`manufacture-review-independence`](skills/manufacture-review-independence) | Reviewing your own work (author == reviewer) — replace lost independence with scoped parallel passes and adversarial re-reads of the source. |
| [`findings-list-is-not-a-todo-list`](skills/findings-list-is-not-a-todo-list) | Acting on a review/audit/recommendation list — re-read each item's disposition and bucket them; some are marked no-fix, some need a human decision. |

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
`python3 scripts/validate_skills.py` (CI runs the same check).

## Licence

All skills are released under [CC BY 4.0](LICENSE) — share and adapt for any
purpose with credit. Created by akbarsha (https://github.com/iamakbarsha1).

Feedback on any skill's methodology is welcome as a repository issue.
