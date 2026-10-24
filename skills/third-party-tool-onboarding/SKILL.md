---
name: third-party-tool-onboarding
description: >
  Use when standing up a third-party tool you did not write — a CLI, an MCP
  server, a plugin, an SDK — on a host that does not satisfy one of its
  declared constraints: a runtime version range, an OS floor, an architecture,
  a licence tier. One probe appeared to work, so the constraint looks
  advisory. It is not: constraints are enforced per layer, and the dangerous
  layer is the one that exits 0 with the wrong artifact. Verify the installed
  version against the intended one rather than trusting the installer's exit
  status, probe install, configure and run as separate layers, and route
  around whichever layer enforces. Triggers on "unsupported version warning",
  "engines/requires floor not met", "it ran fine so the constraint must be
  advisory", "the install succeeded but the tool is the wrong version", "setup
  refused to run", "minimum version not met", "incompatible runtime",
  "onboarding a new CLI or MCP server".
---

# Third-Party Tool Onboarding — One Probe Proves One Layer

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from an onboarding where one declared version constraint produced
three different behaviours at three different layers, and a single successful
smoke test was read as proof the constraint did not apply anywhere.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A single successful probe disproves a universal blocker, never a selective
one. When a tool declares a constraint your host does not meet, one invocation
that works tells you that one path, at one layer, with those exact arguments,
did not enforce it — and nothing else. Constraints are enforced per layer, and
the most dangerous enforcement is not the refusal; it is the layer that
succeeds with the wrong result. An installer that cannot satisfy your
constraint may resolve *down* to an older version that can, exit 0, and leave
you holding an artifact years out of date with no error anywhere in the
output.

So the rule has two halves. After any install, verify the artifact you
received — compare installed version against intended version — rather than
trusting the installer's exit status. And when a declared constraint is unmet,
probe each layer you actually depend on separately: install, configure, run.
Record which layers enforce and which absorb, then route around the enforcing
ones instead of lifting the constraint everywhere.

This is about acquiring and wiring up a tool whose declared constraint you do
not satisfy. Whether a dependency you already have behaves the way its docs
claim once you build on it is a different question — use
`spike-falsification`. Whether the tool should be this tool at all, because
the user named a mechanism the existing code cannot support, is a third —
use `validate-the-users-proposed-mechanism`; here the choice is settled and
the work is finding the layer that permits it.

Two nearer neighbours. `verify-absence-claims` governs a negative finding
someone else handed you ("nothing enforces this"); this skill governs a
positive probe of your own over-generalised into a universal permission.
`diff-the-install-footprint` reads what an installer writes into config you
already run; this skill asks whether the installer delivered the artifact you
actually intended, rather than a version silently reselected to fit your host.

## When this fires

**Where:** Standing up a third-party tool on a host that fails one of its
declared constraints — the first install, the first config write, the first
real invocation — before anything downstream is built on the assumption that
it works here.

**The case this came from.** A tool declared a runtime version range the host
did not satisfy. One pinned smoke invocation succeeded, and that was taken as
evidence the range was advisory. The same constraint then bit twice more, each
at a different layer with a different signature: an *unpinned* global install
silently resolved to a years-old release instead of failing, because the
package manager does constraint-aware version selection — exit code 0, wrong
artifact, no error; and the tool's own `setup` command hard-refused with an
explicit remediation message. Meanwhile the server and the full analysis
pipeline ran correctly on the unsupported runtime. One declared constraint,
three behaviours across three layers.

**Another shape it takes.** *(Illustrative: A migration tool declares a
minimum database server version the staging server predates. A hand-run query
using the new syntax works, so the floor is written off. The migration
runner's own preflight then refuses outright, and the ORM's introspection
silently falls back to a legacy code path that does not read column defaults —
so the schema diff comes back clean while every inserted row lands null.)*

## Checks

- **One successful probe bounds nothing beyond itself.** A working invocation
  licenses the claim "this command, pinned this way, at this layer, did not
  enforce the constraint" — not "the constraint is advisory". Before
  generalising, name which layer the probe exercised and which layers you have
  not touched. *(A pinned smoke invocation succeeded on a runtime outside the
  tool's declared supported range, and the range was written off as advisory;
  it then blocked an install and a setup command at two other layers.)*
- **Verify the artifact you received, not the installer's exit status.** After
  every install, read back the installed version and compare it to the version
  you intended. Resolvers are constraint-aware: when the host cannot satisfy a
  package's declared floor, the resolver's success path may be to select an
  older release that fits, which is a silent downgrade wearing a zero exit
  code. *(An unpinned global install exited 0 on an unsupported runtime and
  left a release years out of date on disk; nothing in the output said the
  version had been reselected.)*
- **Pin the version on every install under an unmet constraint.** Pinning is
  what turns a silent reselection into a loud failure — an explicit version
  the host cannot support errors instead of degrading. Pin on the real install
  as well as on the throwaway probe, or the probe and the install are not
  testing the same thing. *(Same package, same host, two invocations: the
  pinned one fetched the current release and succeeded, the unpinned one
  installed a years-old build — the pin was the only difference.)*
- **Probe install, configure and run as separate layers, and record which
  enforce.** Walk every layer you actually depend on and try each one under
  the unmet constraint, rather than inferring the rest from whichever you
  tried first. Write down the verdict per layer — enforces, absorbs, degrades
  silently — because that table is what the next person needs and the
  constraint's own documentation will not give them. *(One constraint produced
  three behaviours: a silent install downgrade, a hard refusal from the tool's
  own setup command carrying a remediation message, and correct operation of
  the server and the full pipeline.)*
- **Route around the enforcing layer instead of lifting the constraint
  everywhere.** When one layer refuses and the layers you need do not, the fix
  is usually a narrower path to the same outcome, not a host-wide upgrade.
  Read the refusing command's remediation text for what it is — a description
  of that command's gate — then look for the smaller subcommand that does the
  one thing you need. *(A gated `setup` command was replaced by a narrower
  registration subcommand that performed the single required step and carried
  no version gate.)*

## Pre-flight check — before declaring a tool onboarded on an unsupported host

- [ ] Every "the constraint is advisory" claim names the one layer and the one
      invocation that proved it, and lists the layers still untested.
- [ ] After each install you read back the installed version and compared it
      to the intended version, rather than reading the exit code.
- [ ] Every install under an unmet constraint pins an explicit version, the
      real one as well as the probe.
- [ ] Install, configure and run were each exercised separately, with a
      per-layer verdict recorded (enforces / absorbs / degrades silently).
- [ ] Any enforcing layer was routed around with a narrower path, or the
      blocker was escalated — not assumed away because a deeper layer worked.
- [ ] The unsupported configuration is stated in the handoff, so the next
      reader knows which layers were proven and which were merely not hit.

If any box is unchecked, you have one data point and a guess about the rest —
probe the layer you skipped before building on it.
