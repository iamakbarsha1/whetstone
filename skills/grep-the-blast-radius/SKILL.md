---
name: grep-the-blast-radius
description: >
  Use when changing a shared contract — a flag, column, enum/union member,
  shared type, exported symbol, endpoint shape, or config key. The retired
  name is the cheapest complete index of consumers: grep the whole workspace
  and run every suite that crosses the boundary, not just the package you
  edited. Triggers on "rename", "change this type", "add/remove a field",
  "change the API shape", "update shared config", "who uses this", "will this
  break anything", and editing any code imported by more than one module.
---

# Grep the Blast Radius of a Contract Change

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from repeated cases where a shared contract changed, the edited
package's tests stayed green, and sibling consumers broke silently.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

Verification scope follows the contract, not the diff. When you change
something shared, the OLD name (the field you renamed, the enum member you
removed, the flag you retired) is the most complete index of its consumers
that exists. Grep for it across the ENTIRE workspace — source, tests, e2e
scripts, other apps, generated code, docs that assert behaviour — before you
call the change done, and run every suite that crosses the changed boundary.
A green suite in the package you edited proves nothing about the package that
imports it.

## Checks

- **Grep the retired name across everything, then delete it last.** Before
  removing or renaming a shared symbol, `grep -r` the old name over the whole
  repo (not just `src/` of the current package). Each hit is a consumer you
  must update or consciously leave. Do the rename everywhere, THEN delete the
  old definition — deleting first turns the compiler/grep index you need into
  a pile of unrelated errors. *(A shared union gained a member; an exhaustive
  `switch` and a `Record<Union, ...>` in a sibling package silently lost
  exhaustiveness, and the editing package's tests never touched them.)*
- **Run the suites that cross the boundary, not the one you touched.** A
  contract change is verified by the consumers' tests, not the definer's. If
  the shared thing is used by three apps and an e2e script, a passing unit
  test in the shared library is the least informative signal available. Run
  the cross-boundary suites, or state explicitly which you could not run.
  *(A shared function's failure mode changed from throwing to returning
  null; the library's own suite passed, but the one consumer app's e2e
  suite, which depended on the throw, was never run before merge, and the
  null passed through unnoticed.)*
- **Mirrored and duplicated encodings count as consumers.** If the same
  intent is written in more than one place — an array whose order mirrors an
  enum, a hardcoded list that must match a DB column set, a client copy of a
  server type — the grep must find all copies. A contract with N copies has N
  consumers even when only one is imported. *(An endpoint's field list was
  mirrored in a hand-maintained client array; adding a field server-side left
  the client array one short, with no type error to catch it.)*

## Pre-flight check — before you call a shared change done

- [ ] You grepped the retired/old name across the WHOLE workspace (src +
      tests + e2e + other apps + generated), not just the edited package.
- [ ] Every consumer the grep found is updated, or consciously left with a
      reason.
- [ ] You ran the suites of the CONSUMERS that cross the changed boundary, or
      named the ones you couldn't run.
- [ ] Any mirrored/duplicated encoding of the same intent was found and
      reconciled.

If any box is unchecked, the blast radius is unmeasured — go grep it.
