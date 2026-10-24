---
name: harness-config-audit
description: >
  Use when applying an external write-up — an article, a "here is my setup"
  post, a best-practice guide, a vendor doc — to a configuration you already
  run, and the ask is some form of "how do I apply this to mine". The
  deliverable is a per-surface delta, not a restatement of the guide: walk a
  FIXED list of configuration surfaces (always-loaded instructions,
  path-scoped rules, skills, subagents, permission allow/deny/ask rules, hooks
  by event, tool and MCP servers, model and effort settings, memory, recovery),
  give each a COVERED / PARTIAL / MISSING verdict with the command that proved
  it, and verify every product name, version, model id and command the write-up
  cites against the INSTALLED build before repeating it. Triggers on "how do I
  apply this to my setup", "audit my config", "what am I missing", "am I set up
  right", "review my harness config", "this article says to…", "should I add
  X", and any shared setup post you are handed to adopt.
---

# Harness Config Audit

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from an audit of a whole agent configuration against a third-party
article, improvised because no fixed surface list existed — it found a real
high-impact gap, and it also had to catch a model identifier the article named
that did not exist in the running environment.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

An external write-up describes someone else's finished configuration. Your
reader already has one. The deliverable is the difference between the two —
which layers are already covered, which are genuinely missing — and you cannot
state a difference you have not enumerated. So the audit has a fixed shape:
walk the same list of configuration surfaces every time, give each surface a
verdict, and attach to each verdict the command or file read that produced it.
A list assembled from memory is not an enumeration; it covers whatever the
agent happened to recall, and the surface nobody thought of is exactly where
the gap lives.

Two things come before the first verdict. Verify the write-up's factual claims
against the installed build — product names, version numbers, model
identifiers, command names — because an article is a snapshot of its author's
environment and routinely cites things that do not exist in the reader's;
repeating one unverified turns a configuration audit into a confident wrong
recommendation. Then, for each apparent gap, decide whether it is actually
covered by a different mechanism than the one the article names, so an existing
custom setup is not told to adopt a redundant pattern.

**Boundaries.** This skill audits an EXISTING whole configuration against an
EXTERNAL reference description and produces a per-surface delta.
`audit-before-you-build` is the same instinct aimed at code before implementing
a ticket: it asks whether the feature already exists, not which configuration
layers are covered. `verify-absence-claims` is what you run on each individual
MISSING verdict to prove the setting really is unset rather than supplied by a
higher-precedence layer — this skill decides which surfaces to look at, that
one proves each negative. `a-memory-is-not-a-trigger` picks the mechanism that
makes a required step fire reliably; reach for it after this audit names a gap,
not instead of it. `confirm-the-premise-first` establishes the ground truth of
a single asserted property a design choice rests on; here the premise under
test is a whole document's claims about an installed product.

## When this fires

**Where:** Someone hands you a write-up about how to configure a tool and asks
how it applies to the install they already have — an agent harness, a CI
pipeline, a linter stack, an editor setup.

**The case this came from.** A user shared a third-party article describing a
multi-layer configuration setup for an agent CLI and asked how to apply it to
their own install. No rule covered the shape, so the audit was improvised
surface by surface. Walking the layers turned up a gap that had been invisible
for a long time: no permission allow or deny rules defined at all, while the
prompt that gates unrestricted execution was switched off — each setting
unremarkable alone, dangerous as a pair. The article also named a model
identifier that did not exist in the running environment, and cited several
commands whose presence in the installed version had to be checked before any
of them could be recommended.

**Another shape it takes.** *(Illustrative: A team adopts a published
"hardened CI" guide and files a ticket for every control it lists. Three are
already enforced by a branch-protection rule rather than the workflow file the
guide names, so those tickets add redundant steps; a fourth references a runner
feature that landed two minor versions after the one the org pins, and the
pipeline breaks on first run.)*

## Checks

- **Walk a fixed surface list, and give every surface a verdict with its
  evidence.** Not the surfaces the article happens to organize itself around,
  and not the ones that come to mind — the same list, in the same order, every
  time:
  - always-loaded instruction files
  - path- or pattern-scoped rules
  - skills
  - subagents
  - permission allow / deny / ask rules
  - hooks, enumerated per event
  - tool and MCP servers
  - model and reasoning-effort settings
  - memory or persistent-state mechanism
  - recovery mechanism (resume, checkpoint, undo)

  Each gets COVERED, PARTIAL or MISSING, and each verdict names the command or
  file read that produced it and what that showed. A verdict without its
  evidence is a guess wearing a label. *(A whole-configuration audit was
  improvised because no fixed surface list existed, so its coverage depended
  entirely on what the agent recalled mid-task; the one high-impact gap it did
  surface was reached by the order the article happened to use, not by a list
  that guaranteed every surface was visited.)*
- **Verify every name, version, and command the write-up cites against the
  installed build, before repeating it.** Product names, model identifiers,
  flags, subcommands, config keys. Run the version query and the help output
  and check each one is really there; an article is a snapshot of its author's
  environment at its publication date. *(An article recommended a model
  identifier that did not exist in the running environment, and cited several
  commands whose presence in the installed version had to be confirmed one by
  one before any of them could be put in front of the user.)*
- **"Covered by a different mechanism" is COVERED, not MISSING.** Match the
  need the article's pattern serves, not the pattern's name. A setup that
  already solves the same problem through another surface is covered; reported
  against the article's vocabulary it reads as a gap, and the recommendation
  that follows is a redundant second implementation. Say which mechanism covers
  it. *(Most of the reference article's layers were already handled by
  mechanisms the existing setup implemented differently; scored against the
  article's own names rather than the need behind each one, every one of them
  would have been written up as missing.)*
- **Check the surfaces that only mean something in pairs.** Some gaps are
  invisible per-surface and obvious across two: a permission model read
  together with whatever prompts or gates it, a hook read together with the
  state it assumes, a recovery mechanism read together with what writes the
  state it restores. After the per-surface pass, re-read the verdicts for
  interactions. *(Zero permission rules is an ordinary preference when the
  confirmation prompt is on, and the prompt being off is ordinary when the
  rules are tight; the two settings together were the finding, and neither
  surface reported alone would have raised it.)*
- **Report the delta, not the guide.** The output is the per-surface table plus
  the gaps, ordered by what the gap actually exposes. No bullet-by-bullet recap
  of the source, no recommendation for something the reader already runs.
  *(Illustrative: An audit is returned as a section-by-section summary of the
  article with "you should consider this" under each heading; the reader cannot
  tell which items they already have, and the one genuine gap sits ninth in a
  list of twelve.)*

## Pre-flight check — before you hand back a configuration audit

- [ ] Every surface on the fixed list has a verdict (COVERED / PARTIAL /
      MISSING), including the ones the source write-up never mentions.
- [ ] Every verdict names the command or file read that produced it and what
      that showed.
- [ ] Every product name, version, model id, flag and command taken from the
      write-up was checked against the installed build before being repeated.
- [ ] Each apparent gap was tested against the need, not the pattern name, and
      anything already met by another mechanism says which one.
- [ ] You re-read the verdicts for cross-surface interactions, not just
      per-surface results.
- [ ] The deliverable is the delta and the gaps, not a walkthrough of the
      source write-up.

If any box is unchecked, you have a summary of someone else's setup, not an
audit of this one — go enumerate the surfaces.
