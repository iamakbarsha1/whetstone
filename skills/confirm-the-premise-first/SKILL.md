---
name: confirm-the-premise-first
description: >
  Use during design or brainstorming when a user's choice depends on a
  technical property they assert or imply — state the ground truth of that
  property before asking downstream questions built on it. Triggers on
  "should we use X or Y", design trade-off discussions, privacy/data-egress
  decisions, and any choice that hinges on local-vs-remote, free-vs-paid,
  sync-vs-async, or reversible-vs-not.
---

# Confirm the Premise First

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a design dialogue that advanced several questions deep on a
load-bearing wrong assumption before it surfaced by accident.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

When a user's choice hinges on a technical property they assert or imply
(local vs remote, free vs paid, sync vs async, reversible vs not, on-device
vs egress), state the ground truth of that property explicitly BEFORE asking
any downstream questions that depend on it — a one-line "here's what actually
happens" anchor. Questions built on an unverified, load-bearing wrong
assumption are wasted, and the assumption often only surfaces by accident.
For privacy or data-egress decisions especially, confirm the transport
reality first, then ask the policy question.

**Real case (sanitized):** A user chose a local-looking CLI backend believing
it ran inference on-device; it was always remote. Several downstream
data-exposure answers collapsed once that single premise was corrected — the
questions asked before the correction were wasted.

## Pre-flight check — before asking downstream policy questions

- [ ] You identified the technical property the user's choice depends on.
- [ ] You stated its ground truth in one line before asking questions built
      on it.
- [ ] For any privacy/egress decision, you confirmed the transport reality
      (where the data actually goes) before asking the policy question.

If any box is unchecked, you may be spending questions on a wrong premise —
anchor it first.
