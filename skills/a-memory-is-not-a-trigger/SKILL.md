---
name: a-memory-is-not-a-trigger
description: >
  Use when you're relying on a stored memory, a recalled note, an injected
  session-start banner, or a description-matched skill to make a required
  action happen every session or run — especially a recurring logging,
  bookkeeping, or guardrail step. Passive context is advisory: the agent reads
  it and can still skip the action. If it must happen every time, gate it with
  a deterministic mechanism (a hook that executes it, an always-loaded forced
  invocation), not a note you hope gets recalled. Triggers on "remember to do
  X every session", "add a memory so it always…", "why didn't it log / run /
  update", "it was in the instructions but didn't happen", mandatory recurring
  steps, and any moment you catch yourself trusting recall to fire a must-do.
---

# A Memory Is Not a Trigger

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where a required per-session action was named in both a
recalled memory and a session-start reminder, yet still didn't happen for a
whole session — the reminders were read and never acted on.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

Passively-recalled context is advisory, not control flow. A stored memory, a
note surfaced into the prompt, a banner a startup hook printed, a skill matched
by its description — every one of them is something the agent *reads*. Reading
is not executing. If nothing in the loop forces the step, a required recurring
action can be present in context, acknowledged, and skipped anyway. So writing
the rule down does not make it fire: storage is not enforcement. For anything
that must happen every session or run, gate it with a deterministic mechanism —
a hook that performs the action, or an always-loaded instruction that forces an
invocation — and treat any reminder-only path as "may not happen."

**Real case (sanitized):** A required per-session bookkeeping step was wired two
passive ways at once — a memory that got surfaced into context, and a
session-start hook that printed a reminder about it. Both fired every session.
The step still went undone for the entire session: the reminder was read and
not acted on, because nothing in the loop actually executed it. The fix was not
"remember harder" — it was converting the must-do into enforcement: an
always-loaded, mandatory-activation instruction that forces the skill to run,
plus a hook that performs the deterministic half instead of merely mentioning
it. The lesson generalizes to any recurring guardrail, log, or cleanup an agent
is "supposed to remember."

## Checks

- **Separate advisory context from control flow.** A memory, a recalled note,
  an injected startup banner, a description-matched skill — all are inputs the
  agent reads; none of them run anything. If no hook or forced invocation sits
  in the path, classify the action as "may not happen" and design accordingly.
  *(A per-session logging step named in both a recalled memory and a startup
  banner was read every session and skipped anyway.)*
- **Gate must-dos deterministically.** For an action that must happen every
  time, put it where execution isn't optional: a hook that runs the action, or
  an always-loaded config instruction that forces a skill invocation — not a
  note filed in passive memory that depends on recall plus goodwill to fire.
- **Split "remind" from "perform".** A hook that only injects a reminder is
  still advisory. If the mechanism can execute the deterministic half of the
  work itself, execute it there and leave only the judgment to the agent — a
  reminder to do X is weaker than a step that does X.
- **Don't upgrade "I stored it" to "it'll happen".** Writing the rule down —
  into memory, a doc, a skill description — feels like closure, but the write
  is the easy half. The firing is unproven until a mechanism guarantees it;
  confirm the action actually happened, don't infer it from the note existing.

## Pre-flight check — before you trust a recurring action to fire

- [ ] Every action that must happen each session/run has a **deterministic
      trigger** (a hook or a forced invocation), not only a passively-recalled
      memory, note, or banner.
- [ ] Any reminder-only mechanism is treated as **advisory**; each true must-do
      has an executor, not just a mention.
- [ ] The **deterministic half** of the work is performed by the mechanism,
      with only judgment left to the agent.
- [ ] You **verified the action actually fired** at least once — not merely
      that the instruction or memory exists.

If any box is unchecked, you have a note you hope gets read, not an action that
happens — go put a real trigger in the loop.
