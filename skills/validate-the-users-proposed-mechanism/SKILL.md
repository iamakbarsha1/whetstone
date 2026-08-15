---
name: validate-the-users-proposed-mechanism
description: >
  Use when a user specifies a platform, tool, library, or approach as part of
  a request — their choice is a proposed MECHANISM, not a spec. Grep the built
  artifact for disqualifying signals before agreeing, separate their intent
  from the mechanism, and satisfy the intent with a feasible mechanism when the
  chosen one conflicts. Triggers on "deploy on X", "use library Y", "run it on
  Z", "switch to", "let's use", and any user-named tech that the existing code
  may not fit.
---

# Validate the User's Proposed Mechanism

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where a user's stated deployment stack was infeasible for
the built application, and implementing it verbatim would have discarded
working, tested code.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

When a user names a platform, tool, library, or approach, treat it as a
PROPOSED MECHANISM for an underlying INTENT — not as a fixed requirement.
Before implementing it, check the thing already built for signals that
disqualify the chosen mechanism. If it conflicts, separate the intent from the
mechanism, satisfy the intent with a feasible mechanism, and push back
explicitly on the conflict. Blindly implementing an infeasible choice throws
away working code and ships something that can't run.

## Checks

- **Grep the artifact for disqualifying signals first.** Before agreeing to a
  named platform/tool, search the codebase for constructs it can't support.
  *(A user asked to deploy on a serverless platform, but the app relied on
  long-lived `setInterval` background workers that serverless functions kill;
  and the named database was a different family than the data layer was written
  for, which would have meant a rewrite.)* One grep for the incompatible
  construct surfaces the conflict before you commit to it.
- **Separate intent from mechanism.** State what the user is actually trying to
  achieve ("cheap always-on hosting", "managed persistence") apart from the
  specific tool they named. The intent is the requirement; the tool is one way
  to meet it — and often not the only or best way given what's built.
  *(Illustrative: A user asked to move the job queue to a specific named message-broker
  service; restating the intent as "reliable retries under bursty load"
  showed the already-installed queue library met it without standing up a
  new service to operate.)*
- **Push back explicitly on a real conflict, with an alternative.** When the
  mechanism can't serve the intent without a rewrite, say so plainly and offer
  a feasible mechanism that does: "X kills the background workers this app
  needs; Y gives you the same always-on hosting without a rewrite." Don't
  silently implement the infeasible choice, and don't silently substitute your
  own without flagging it.
  *(Illustrative: A user asked to swap the app's ORM for a specific named alternative that
  dropped the transaction support the codebase relied on; the response named
  that gap directly and proposed a lighter driver that kept transactions and
  avoided a data-layer rewrite.)*

## Pre-flight check — before you implement a user-named tool/platform

- [ ] You grepped the existing artifact for constructs the named mechanism
      can't support.
- [ ] You separated the user's underlying intent from the specific mechanism
      they named.
- [ ] Any real conflict was raised explicitly, with a feasible alternative
      that serves the same intent.

If any box is unchecked, you may be building on an infeasible premise — check
the artifact against the mechanism first.
