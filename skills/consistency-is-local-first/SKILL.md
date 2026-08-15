---
name: consistency-is-local-first
description: >
  Use before writing new code in an existing module — match the nearest
  sibling's pattern first; a repo-wide convention is the default only when the
  local module has no established pattern of its own. A uniform module beats a
  globally-conformant outlier. Triggers on "follow the conventions", "match
  the style", "how do we do X here", "the standard is", "add a new
  component/form/endpoint", and starting new code beside existing code.
---

# Consistency Is Local First

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where applying a repo-wide convention would have made new
code the odd one out in a module that consistently did it another way.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

Consistency is local first. Before writing new code, read the nearest sibling
in the SAME module and match its pattern. A repo-wide convention (a style
guide, a "we always use X" doc) is the correct default only when the local
module has no established pattern of its own. A module that is internally
uniform — even in an "outdated" style — is more maintainable than one where a
new file conforms to the global rule while every sibling around it does
something else. Don't import a global convention into a module that has
locally settled on another. When the two genuinely conflict and the local
pattern is consistent, match local and note the divergence rather than
silently fragmenting the module.

## Checks

- **Read the nearest sibling before you write.** Open the file most like the
  one you're about to create, in the same directory/module, and copy its
  shape: its imports, its state approach, its error handling, its test layout.
  The closest existing analog outranks a remembered global rule. *(Illustrative: A module
  consistently used plain local state; applying the repo-wide
  form-library-plus-schema convention would have made the new form the single
  outlier in that module.)*
- **If you're deliberately breaking local consistency, say so.** Sometimes the
  right move IS to introduce the better pattern — but that's a migration
  decision, not a drive-by. Flag it: "this module uses X; I'm introducing Y
  here and the rest should follow or it'll be inconsistent," so it's a
  conscious choice, not an accidental outlier. *(Illustrative: A new file replaced a
  module's consistent callback-based error handling with promise chaining but
  didn't flag it as an intentional upgrade; the next contributor couldn't tell
  if it was deliberate and reverted it.)*

## Pre-flight check — before you add code to an existing module

- [ ] You read the nearest sibling in the same module and know its pattern.
- [ ] You matched the local pattern, OR the module had none and you fell back
      to the repo-wide convention.
- [ ] Any deliberate break from the local pattern is flagged as a migration
      choice, not left as a silent outlier.

If any box is unchecked, you may be fragmenting a uniform module — read the
sibling first.
