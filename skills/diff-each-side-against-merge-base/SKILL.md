---
name: diff-each-side-against-merge-base
description: >
  Use when resolving a merge or rebase conflict, or reviewing a merge commit —
  conflict markers show where git gave up, not the full semantic delta, and
  3-way auto-merge silently drops fields outside the markers. Compare
  ours/theirs/base by symbol and field inventory before trusting the result.
  Triggers on "merge conflict", "resolve conflict", "rebase", "git merge",
  "auto-merge", "cherry-pick", and reviewing a large merge diff.
---

# Diff Each Side Against the Merge Base

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where 3-way auto-merge silently dropped fields outside
the conflict markers, and reading only the marked regions would have shipped a
file missing content.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

Conflict markers mark where git could not decide — not the full extent of what
changed. Git's 3-way merge auto-resolves every hunk it thinks is unambiguous,
and those silent auto-resolutions can drop or duplicate content when both
sides edited near the same region. Resolving a conflict by reading ONLY the
`<<<<<<<`/`>>>>>>>` regions is resolving a fraction of the delta. For any
non-trivial conflict, reconstruct the real change by comparing each side
against the merge base by symbol/field inventory.

## Checks

- **Inventory ours, theirs, and base — not just the markers.** For a
  conflicted file, list the symbols/fields/exports in the merge base, in
  "ours", and in "theirs". The correct resolution is the UNION of both sides'
  intended changes against the base. The markers only show you the overlap git
  couldn't auto-pick; everything auto-merged is still yours to verify.
  *(A 3-way merge auto-dropped several struct fields that existed on both the
  base and one side because the other side rewrote the surrounding block;
  nothing appeared between conflict markers.)*
- **Treat delete-vs-extend as a decision, not an auto-pick.** When one side
  deletes what the other extends (a field, a case, a param), auto-merge or a
  careless resolution will usually keep the delete and lose the extension —
  silently. Whenever the base had X, one side removed it, and the other built
  on it, stop and confirm intent explicitly. *(Illustrative: A base switch-case was removed
  on one branch while the other branch added new handling inside that same
  case; auto-merge kept the removal and silently discarded the added
  handling, with no conflict marker raised.)*
- **Verify the merged file's inventory against both parents.** After
  resolving, diff the result against BOTH parents and confirm every field/
  symbol that either parent intended to add is present, and every one either
  intended to remove is gone. A conflict "resolved" cleanly can still be
  missing content that never conflicted. *(Illustrative: After a conflict resolved with
  zero markers on a given function, diffing the merged file against both
  parent branches showed that function had existed in one parent and was
  silently missing from the merge output.)*

## Pre-flight check — before you commit a merge resolution

- [ ] For each conflicted file you compared ours/theirs/base by symbol/field
      inventory, not just the marked regions.
- [ ] Every delete-vs-extend case was resolved by an explicit decision, not an
      auto-pick.
- [ ] The final file's inventory was diffed against BOTH parents and accounts
      for every intended add and remove.

If any box is unchecked, you've resolved the markers, not the merge — go
inventory both sides.
