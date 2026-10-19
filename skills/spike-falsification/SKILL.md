---
name: spike-falsification
description: >
  Use when validating a third-party dependency — an API, SDK, contract, or
  protocol — before designing on top of it, especially onchain/smart-contract
  dependencies. Triggers on "spike this integration", "validate this
  contract/SDK before we build on it", "is this really soulbound /
  non-transferable / read-only", "prove the API behaves like the docs say",
  "fork the network and test against the deployed contract", or any request to
  de-risk a dependency before committing to a design.
---

# Spike to Falsify, Not to Demo

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from an onchain spike where web research returned correct contract
signatures, but the behaviours that actually shaped the design were only caught
by executing against the deployed bytecode.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening, open an
issue on the repository or contact the author at the profile link above. If the
problem is the agent not following a rule below rather than the rule itself,
that's an execution failure — acknowledge and correct it.

## The core rule

Docs and research tell you the API *shape*; only executing against the
production artifact tells you its *behaviour*. A spike exists to try to
**falsify** your design assumptions — run the operation you believe is
impossible, forbidden, or already handled — not to demo the happy path. A spike
that only shows the thing working has tested nothing you were worried about.

## When this fires

**Where:** Evaluating a third-party dependency — an API, SDK, published
package, or deployed contract — in the window before a design hardens around
its assumed behaviour.

**The case this came from.** Web research returned correct contract
signatures, so the design proceeded on them. Executing against the deployed
bytecode on a fork surfaced 1-based indexing and a mandatory filter argument
that no document mentioned, and a token the design assumed was soulbound
turned out to be transferable.

**Another shape it takes.** *(Illustrative: A vendor API is documented as
idempotent on a client-supplied key, and the spike demos one successful
create. Replaying the same key against the real endpoint would have shown the
second call creating a duplicate — which the billing design had already
written off as impossible.)*

## Checks

- **Execute against the real deployed artifact, not a mock or a local
  redeploy.** Run against the live network (fork it), the real API endpoint, or
  the actual published package version — a local reimplementation inherits your
  assumptions instead of exposing the vendor's. *(Web research returned correct
  contract signatures, but 1-based indexing and mandatory filter arguments only
  surfaced when calling the deployed bytecode on an anvil fork of the testnet.)*
- **Run at least one deliberate falsification.** Name the property your design
  depends on (immutable, soulbound, idempotent, read-only) and attempt the
  operation that would violate it; observe what actually happens rather than
  what the docs imply. *(A token assumed soulbound was in fact transferable —
  caught only by attempting the transfer, before a whole access model was built
  on the false assumption.)*
- **Keep an honest friction log.** Record every surprise, gotcha, and dead end
  in the findings doc, not just the path that worked — the friction is the
  reusable output of a spike. *(anvil's well-known default accounts carry
  contract code on public testnets, which silently breaks `_safeMint`'s
  onReceived callback; the fix — fund fresh EOAs with `anvil_setBalance` — is
  worthless to the next spike unless it's written down.)*

## Pre-flight check — before you trust a spike's conclusions

- [ ] The spike ran against the real deployed artifact (forked live network for
      onchain), not a mock, stub, or local redeploy.
- [ ] You attempted at least one operation your design assumes cannot happen,
      and recorded the actual result — not the documented one.
- [ ] The findings doc logs every surprise and gotcha hit, not only the
      happy-path result.
- [ ] Any check whose grounding case is domain-specific (e.g. anvil/EVM) was
      applied as an example of the pattern, not copied verbatim to an unrelated
      stack.

If any box is unchecked, you have a demo, not a spike — go try to break the
assumption you're about to build on.
