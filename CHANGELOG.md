# Changelog

All notable changes to whetstone are recorded here. Versions track the plugin
manifest (`.claude-plugin/plugin.json`) and follow [SemVer](https://semver.org):
new skills are a minor bump, rule changes to an existing skill are a patch, and
repo tooling or docs that ship with the plugin are a patch. A change to the
skill format contract itself — a new required section, a new CI gate a
contributor must satisfy — is a minor bump, because work written against the
previous version no longer merges.

## [1.7.0] — 2026-10-19

No new skills (still 27). Adds a required `## When this fires` section to the
skill format, and backfills it across all 27.

- Every `SKILL.md` gained `## When this fires`: a `**Where:**` line naming the
  kind of work the skill belongs to, then the situation twice — `**The case
  this came from.**`, retold from the failure the skill was distilled from, and
  `**Another shape it takes.**`, a different domain marked
  `*(Illustrative: …)*`. The frontmatter `description` tells a router when to
  surface a skill; this tells a reader who already has it open where it applies.
- `scripts/validate_skills.py` enforces the section: the three lead-ins appear
  in order *inside* the section body, each followed by text, the section sits
  between the core rule and the pre-flight, and the second example carries its
  `*(Illustrative: …)*` marker. Heading lookups are anchored to line starts,
  because skills quote their own anatomy in prose and an unanchored search
  finds the mention instead of the heading.
- All three catalogue surfaces now carry the example and CI requires it on each:
  a non-empty Example cell per README row, and a `<p class="eg">` line per
  `docs/index.html` card.
- `CONTRIBUTING.md` and the README's "Anatomy of a skill" block record the new
  section; the site's own anatomy list and code sample, which had been
  describing the 1.6.1 shape, were updated to match.
- `CONTRIBUTING.md` states the provenance rule outright: a case is lived or it
  is marked `*(Illustrative: …)*`, and a file may not claim both of the same
  case.

Known limitation, narrowed: the example lives in three hand-maintained places —
the `SKILL.md` section, the README row, and the site card. The README cell and
the card are the same condensed sentence, so CI requires them to match exactly.
The `SKILL.md` section is a longer retelling and cannot be compared
mechanically; keeping that one honest is still on the author.

Fixed while writing this release: five skills had a header calling a case lived
while their own `## Checks` bullet marked the same case `*(Illustrative: …)*`.
The first drafts of the new section inherited the header's side and restated it
on two more surfaces. The sections now draw only on material the file treats as
lived. The underlying header-vs-bullet contradiction in
`findings-list-is-not-a-todo-list` and `consistency-is-local-first` is older
than this release and still open — those two have no unmarked case to stand on.

## [1.6.1] — 2026-10-19

No skill changes. Ships the cross-surface consistency checks that landed after 1.6.0.

- `scripts/validate_skills.py` gained `check_cross_surface()`: the skill count in
  `README.md`, the card count in `docs/index.html`, and that file's per-section
  counts must agree with the number of directories under `skills/`, and every skill
  directory must appear in both the README table and the docs catalogue. Checked
  against all four drift modes before merge.
- `CONTRIBUTING.md` records what the checks enforce, so a contributor adding a skill
  knows which surfaces move together.

Background: 1.5.0 shipped with `docs/index.html` a skill behind the repo, and the gap
went unnoticed until the 1.6.0 review. These checks make that break CI instead.

## [1.6.0] — 2026-10-17

Added 2 skills (25 → 27), promoted from a weekly skill review.

- `enumerate-artifacts-not-references` — a completeness gate that scrapes references out of prose has an unbounded input set and floods on any document about the thing it matches; enumerate the real artifacts instead, and keep a separate bounded pass for truncation.
- `name-the-boundary-between-siblings` — keyword coverage makes a skill discoverable, not selectable; grep your trigger words against the installed set and write a reciprocal boundary line into both files.

Also: added reciprocal boundary lines to `verify-absence-claims` and `distill-the-scar` (the siblings the new skills compete with), and brought `docs/index.html` back in sync — it was still showing 24 skills and missing the `spike-falsification` card from 1.5.0.

## [1.5.0] — 2026-09-08

Added 1 skill (24 → 25).

- `spike-falsification` — validate a third-party dependency by executing against the real deployed artifact and trying to falsify design assumptions, not demoing the happy path. (Onchain origin; gotchas marked as the pattern, not universal rules.)

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

[1.7.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.7.0
[1.6.1]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.6.1
[1.6.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.6.0
[1.5.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.5.0
[1.4.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.4.0
[1.3.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.3.0
[1.2.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.2.0
[1.1.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.1.0
[1.0.0]: https://github.com/iamakbarsha1/whetstone/releases/tag/v1.0.0
