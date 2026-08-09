---
name: audit-before-you-build
description: >
  Use as the FIRST step of any implementation task handed to you from a
  checklist, ticket, milestone, or spec — the first step is an existence
  check, not a design. Trackers record conversations, not deliverables, so
  grep for the item's key nouns and cross-check spec status before writing
  code, then pivot "build X" to "verify X and close the gaps" when it already
  exists. Triggers on "implement this ticket", "build feature X", "next
  milestone item", "from the checklist", "start this task", "add X".
---

# Audit Before You Build

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from cases where a checklist item was already ~90% shipped as a side
effect, and where "all issues closed" hid whole unbuilt layers — building from
the tracker text would have duplicated working code or missed real gaps.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A ticket, checklist, or spec line records a conversation about intent — it is
not a reliable record of what has or hasn't been built. Code drifts from the
tracker in both directions: features ship as side effects of other work
without their item being ticked, and closed items leave real layers unbuilt.
So the first step of "build X" is never design — it's an existence check. Grep
the codebase for the item's key nouns, cross-check the spec's own status
markers, and only then decide whether the task is "build", "finish", or
"verify and close".

## Checks

- **Grep for the item's key nouns before designing.** Take the concrete terms
  from the task — paths, function names, table/column names, endpoint routes,
  spec keywords — and grep for each. Existing hits mean the work is partly or
  wholly done. *(A milestone item was ~90% already implemented as a side
  effect of an earlier change; grepping the feature's route name surfaced it
  immediately, turning a "build" into a small gap-closing task.)*
- **Cross-check the tracker against code and spec status, both ways.** "Closed"
  does not mean "built" and "open" does not mean "absent". Read the spec's own
  Status headers and the code stubs together. *(An "all issues closed"
  milestone hid two entire layers that were never implemented — the tracker
  said done, the code said empty.)*
- **Pivot the verb when reality disagrees.** If the audit shows the thing
  exists, restate the task honestly — "verify the existing X and close gaps A
  and B" instead of "build X" — and say so before writing code. Duplicating
  working code is worse than a slow start.

## Pre-flight check — before you write implementation code from a task

- [ ] You grepped the codebase for the task's key nouns (paths, names, spec
      terms) and know what already exists.
- [ ] You cross-checked tracker status against actual code AND spec status
      markers, not just the ticket text.
- [ ] If the thing partly exists, you restated the task as verify/finish and
      said so before building.

If any box is unchecked, you're building on the tracker's word — go audit the
code first.
