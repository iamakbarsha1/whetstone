---
name: safe-data-export
description: >
  Use when a task's output is sensitive or large data and the destination is
  a path inside a version-controlled tree — writing the data is not the
  finish line, an unreviewed commit of it is the failure mode. Triggers on
  "export the data", "dump the DB", "extract observations", "write it to the
  repo", "save the logs", "migrate memory", and whenever the destination path
  resolves inside a git working tree.
---

# Safe Data Export

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where a memory export was pointed at a directory inside
a public repo before the ignore rule existed, one accidental `git add -A`
away from leaking personal data.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

When a task's output is sensitive or large data and its destination sits
inside a version-controlled tree, the ignore rule is a PRECONDITION of
writing, not a cleanup step performed after. Make the destination
uncommittable — and verify that it is — before the data exists on disk at
all. A `.gitignore` entry added after the write leaves a window, however
short, where any commit sweep (`git add -A`, an IDE auto-stage, a CI bot)
can pick the data up before you get back to it.

## Checks

- **`.gitignore` first, always.** Add the target directory or file path to
  `.gitignore` BEFORE writing a single byte of exported data. Writing first
  and ignoring later means there is a real window, between the write and the
  ignore-commit, where the data sits trackable. *(An agent exporting a
  project's persisted memory observations for migration was about to write
  the dump into a directory inside that project's — public — repo; writing
  first would have left the file trackable until the ignore rule landed.)*
- **Verify uncommittable before writing, not after.** Run
  `git check-ignore <path>` and confirm it matches, then run
  `git status --short` and confirm the target does NOT appear — both checks
  BEFORE the data exists on disk, not as a post-hoc sanity check. *(For that
  same export, `git check-ignore` against the target directory and
  `git status --short` showing it absent were both confirmed before the
  first observation was written, closing the gap a "write then verify"
  order would have left open.)*
- **One dedicated export directory, one ignore rule.** Write into a single
  `.<name>-export/`-style directory instead of scattering files across the
  tree — one line in `.gitignore` then covers the whole dump, and there's
  nothing left to hunt for path by path. *(The memory-observation export
  used one dedicated directory for the whole dump specifically so a single
  `.gitignore` entry, verified once, covered every file the migration
  produced.)*
- **Name the leak risk when the repo is public.** State explicitly, before
  writing, whether the destination repo is public and what the exported data
  contains — memory observations, DB rows, and logs routinely carry personal
  data (email addresses, org names, GitHub handles) that has no business in
  version control history. *(The observations being exported carried a
  personal email address, an organization name, and GitHub handles; the repo
  was public, so an accidental commit would have published all three.)*

## Pre-flight check — before you write exported data into a repo tree

- [ ] `.gitignore` already contains the target path, added before any data
      was written.
- [ ] `git check-ignore <path>` matches the target AND `git status --short`
      does not show it — both confirmed before the data exists on disk.
- [ ] The export lands in one dedicated directory (not scattered files), so
      a single ignore rule covers it.
- [ ] You stated whether the destination repo is public and what kind of
      personal data (emails, org names, handles) the export may contain.

If any box is unchecked, the destination is not proven uncommittable yet —
do not write the data.
