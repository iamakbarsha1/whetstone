# Changelog

All notable changes to whetstone are recorded here. Versions track the plugin
manifest (`.claude-plugin/plugin.json`) and follow [SemVer](https://semver.org):
new skills are a minor bump, rule changes to an existing skill are a patch.

## [1.4.0] — 2026-08-16

Added 1 skill (23 → 24).

- `scan-generated-files-for-artifacts` — grep an agent-written file's head and tail for leaked harness residue (stray tags, fence fragments, content past EOF); passing tests don't cover non-code bytes.

## [1.3.0] — 2026-08-16

Added 4 skills (19 → 23), promoted from field logs and repo work. (Backfilled: these shipped incrementally under the 1.3.0 manifest without their own changelog entry.)

- `distill-the-scar` — the meta-skill: turn a real failure into a gated, reusable skill.
- `a-memory-is-not-a-trigger` — passive context is read, not executed; gate must-dos with a deterministic hook or forced invocation.
- `publish-oss-repo` — signal maintenance with a canonical license, tagged releases, topics, and contract-enforcing CI.
- `safe-data-export` — make an export destination uncommittable and verify it before the data exists on disk.

## [1.2.0] — 2026-08-09

Added 5 skills (14 → 19), draining the last of the promotable field-log backlog.

- `test-fixture-realism` — fixtures must mirror data reality; assertions can't pass trivially.
- `consistency-is-local-first` — match the nearest sibling before the repo-wide convention.
- `findings-list-is-not-a-todo-list` — honor each finding's disposition; don't implement blessed no-ops.
- `validate-the-users-proposed-mechanism` — a user's tool choice is a proposed mechanism, not a spec.
- `know-your-aggregate-command-scope` — a wrapper's green means only what it actually ran.

## [1.1.0] — 2026-08-09

Added 9 skills (5 → 14), promoted from reviewer/task-observer field logs across real sessions.

- `grep-the-blast-radius`, `measure-the-delta-not-the-absolute`, `prove-the-test-can-fail`,
  `diff-each-side-against-merge-base`, `manufacture-review-independence`,
  `negative-invariant-testing`, `audit-before-you-build`, `verify-absence-claims`,
  `inject-ambient-inputs`.
- README regrouped into four themed tables.

## [1.0.0] — 2026-08-09

First distributable release.

- Packaged the 5 founding skills as a Claude Code plugin: `verify-through-the-real-path`,
  `plan-cross-encoding-review`, `read-the-real-failing-call`, `confirm-the-premise-first`,
  `running-long-background-jobs`.
- Added the plugin marketplace (`.claude-plugin/`), a dependency-free skill validator,
  CI, and contributor docs.

[1.4.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.4.0
[1.3.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.3.0
[1.2.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.2.0
[1.1.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.1.0
[1.0.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.0.0
