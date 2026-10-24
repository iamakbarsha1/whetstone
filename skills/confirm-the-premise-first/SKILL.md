---
name: confirm-the-premise-first
description: >
  Use during design or brainstorming when a user's choice depends on a
  technical property they assert or imply — state the ground truth of that
  property before asking downstream questions built on it. Triggers on
  "should we use X or Y", design trade-off discussions, privacy/data-egress
  decisions, and any choice that hinges on local-vs-remote, free-vs-paid,
  sync-vs-async, or reversible-vs-not. Also use before calling a generated
  artifact broken — a symlink, lockfile, build output, compiled config, or
  migration — since "this points at the wrong thing" is a premise about intent
  that only the declaration can confirm. Triggers on "this is wired wrong",
  "the install is broken", "that symlink points at the wrong target", and any
  bug report written from derived state.
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

The same holds when the load-bearing premise is a claim about history rather
than a property of the system. What an earlier version shipped, what a past
decision settled, what a previous section of the same document says — each is
a claim about a record, and the record is almost always within reach: the
entry directly below the one you are writing, the git log, the section above.
Read it instead of recalling it. Recall feels most authoritative for exactly
the facts that have been compressed, and when the claim lands in prose there
is no validator downstream to catch it.

"Should we use X or Y" also reaches `diff-the-install-footprint`, and one axis
separates them: this skill establishes the ground truth a choice hinges on
before the choice is debated; that one reads what a specific tool's installer
writes into config you already run, once a candidate is on the table.

**Real case (sanitized):** A user chose a local-looking CLI backend believing
it ran inference on-device; it was always remote. Several downstream
data-exposure answers collapsed once that single premise was corrected — the
questions asked before the correction were wasted.

**Real case (sanitized):** A changelog entry justified a new check by stating
that the previous release had shipped a docs page one version behind. The
entry immediately below it recorded the opposite: that release was the one
that caught and fixed the lag, which had been introduced two releases earlier.
The history was recalled rather than read, and the file holding the correction
was already open.

This establishes the ground truth of a single asserted property a choice rests
on; verifying a whole external write-up's product names, versions and commands
against an installed build, as part of a per-surface configuration audit, is
`harness-config-audit`.

## When this fires

**Where:** Early in a design or brainstorming exchange, the moment a user's
choice rests on a property of the system they asserted rather than checked —
or on a claim about what an earlier version or decision actually did.

**The case this came from.** A user chose a local-looking CLI backend
believing it ran inference on-device. It was always remote, and several
downstream data-exposure answers collapsed the moment that one premise was
corrected. The historical variant is above: a changelog entry justified a new
check with a claim the entry directly below it contradicted.

**Another shape it takes.** *(Illustrative: A team debates retention policy
for a queue on the premise that messages are deleted on acknowledgement. The
broker is configured for replay and holds them seven days, so every retention
question asked before that is checked is answered about a system that does not
exist.)*

## Checks

- **Read the declaration, not the artifact it generated.** When a derived
  thing looks wrong — a symlink, a lockfile, a build output, a compiled config,
  a migration — read the declaration that produced it before calling it a
  defect, and specifically check whether the target you believe it *should*
  point at exists at all. "This is wired to the wrong thing" is a claim about
  intent, and intent lives in the manifest, not in the output. If declaration
  and artifact agree, what you have is at most a naming or ergonomics
  complaint, which is a different and much weaker report. *(A package's
  installed binary symlinked to a different entry point than its name
  suggested, and that was written up as a mis-wired install naming the "real"
  target it should have used. The manifest showed the mapping was explicit and
  deliberate, the supposed correct target was not shipped at all, and the alias
  worked when invoked properly — the wrong conclusion had already reached a
  written report bound for an upstream tracker.)*

## Pre-flight check — before asking downstream policy questions

- [ ] You identified the technical property the user's choice depends on.
- [ ] You stated its ground truth in one line before asking questions built
      on it.
- [ ] For any privacy/egress decision, you confirmed the transport reality
      (where the data actually goes) before asking the policy question.
- [ ] Any claim about prior state — an earlier version, a past decision, a
      previous section — was read from the record, not recalled.
- [ ] Before calling any generated artifact a defect, you read the declaration
      that produced it and confirmed the target you expected actually exists.

If any box is unchecked, you may be spending questions on a wrong premise —
anchor it first.
