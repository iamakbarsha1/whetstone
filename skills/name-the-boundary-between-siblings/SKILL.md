---
name: name-the-boundary-between-siblings
description: >
  Use when adding, renaming, or rewriting the description of a skill, command,
  or agent that will sit beside others in the same registry — the moment you
  pack a description with the keywords an agent would search for. Keyword
  coverage makes an entry discoverable; it does not make it selectable. If an
  installed sibling already claims those words, the router sees two
  descriptions that both fit and has nothing to choose on. Grep your primary
  keywords first, then write a reciprocal boundary line into both files naming
  the one axis that separates them. Triggers on "create a skill", "write a
  skill description", "rename this skill", "two skills overlap", "which skill
  should the router pick", "the agent picked the wrong skill", "skill
  discovery", "keyword coverage".
---

# Name the Boundary Between Siblings

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where a whole-repo security-audit skill shipped into a
library that already held a per-file one — both descriptions matched a bare
"security audit" request, and neither file mentioned the other.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

Discoverability and selectability are different properties. Packing a
description with every word an agent might search for makes the entry findable,
and in the same move maximises its overlap with everything already installed —
so an entry can satisfy every discoverability rule and still be unpickable,
because the router sees two descriptions that both fit the request and has
nothing to decide on. More keywords cannot fix this; only a stated boundary
can. Before writing the description, grep your primary keywords against the
installed set, and wherever a sibling already claims them, name the single axis
that separates the two — scope, perspective, or output shape — and write that
line into **both** files, not just the one open on screen.

Turning a single failure into a skill in the first place is a different job:
use `distill-the-scar` for producing the skill, this one for placing it beside
the skills already installed.

## Checks

- **Grep your primary keywords against the installed set before you write the
  description.** Take the two or three phrases a user would actually type and
  search every installed description for them (`grep -ril "security audit"
  ~/.claude/skills/*/SKILL.md`, widened to plugin or marketplace paths where
  relevant). Do this before drafting, not after: a description written first
  and checked later gets defended rather than changed. *(A whole-repo
  security-audit skill was written and shipped into a library that already held
  a per-file one; a single grep for "security audit" would have surfaced the
  collision before either description hardened.)*
- **Name the one axis that separates them, not a list of differences.** Two
  sibling entries always differ in many ways; the router can only act on one
  crisp distinction. Pick the axis that actually decides the request — scope
  (one file vs the whole repo), perspective (defender vs attacker), or output
  shape (report-only vs applies fixes) — and state it in the imperative form a
  reader can match against their own situation. *(Illustrative: two review
  skills were separated by a paragraph comparing their methodologies; requests
  kept landing on the wrong one until the line was rewritten to the single
  question "one file or the whole repo?")*
- **Write the boundary line into both bodies, never only the new one.** The
  one-way pointer is the default failure mode: the author knows the older entry
  exists, writes the cross-reference into the file already open on screen, and
  never opens the other. A request that lands on the older entry then has no
  route out — and that is exactly the half of the traffic the author never
  sees. Where the sibling is read-only (a plugin or system entry you cannot
  edit), put the line in the editable file and record the pairing in whatever
  delta or overlay file you do own. *(Two skills competing for "security audit"
  each needed the pointer; only the newer file got one, leaving every request
  that matched the older description with no way across.)*

## Pre-flight check — before you save a new or renamed skill

- [ ] The new entry's primary keywords were grepped against the installed
      descriptions **before** the description was drafted.
- [ ] Every sibling sharing a trigger word has a boundary line naming **one**
      distinguishing axis — scope, perspective, or output shape — not a list of
      differences.
- [ ] That boundary line exists in **both** bodies (or, for a read-only
      sibling, in the editable file plus the delta that owns the pairing).

If any box is unchecked, the router can still land on the wrong sibling with no
route back — go name the boundary.
