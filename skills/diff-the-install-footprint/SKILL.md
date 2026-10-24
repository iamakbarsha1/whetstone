---
name: diff-the-install-footprint
description: >
  Use when deciding whether to adopt a tool that installs into a shared
  environment — a plugin, framework, agent harness, shell or editor config,
  starter template, or anything with an init wizard that writes files you did
  not review. Its installer claims slots that already have an occupant: named
  locations a shared config reserves for one writer — a hook or lifecycle
  event, an always-loaded instruction or rc file, a permission entry, a budget.
  Fetch the config the installer actually writes, map every slot it claims onto
  whatever holds it today, and subtract capability you already run before
  counting what is left. Triggers on "should we adopt X", "should we install
  X", "how do we add X to our workflow", "is this worth installing", "evaluate
  this repo for our stack", "run the init wizard", "add the marketplace".
---

# Diff the Install Footprint

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where a popular agent framework was evaluated for
adoption and the config its init wizard writes — nine hooks, four of them on
events already occupied, a wildcard package-runner permission, an always-loaded
instruction file — turned a feature list that read as additive into a
replacement for the whole setup.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A README describes capability; the installer describes consequence. Anything
installed into a shared environment claims slots — named locations a shared
config reserves for a single writer — and most of them already have an
occupant. In an agent harness the slots are hook events, an instruction file
loaded every session, a permission allow-list, a tool budget; elsewhere they
are rc files, git hooks, lint rule names, a `PATH` entry, a port. Two writers
on one slot is a collision,
not an addition, and capability you already run is not a gain. So before
installing: fetch the config the installer actually writes, enumerate every
slot it claims, and map each onto what holds it today. Judge the tool on that
residue — what is genuinely new after subtraction, minus what it displaces —
never on the feature list.

Five siblings share trigger words with this one, and a single axis separates
each. `spike-falsification` asks whether a dependency your code *calls* behaves
as documented; this asks what its installer *writes* into config your other
tools read. `validate-the-users-proposed-mechanism` asks whether the code you
already have can run on a named platform; this asks that of your configuration
rather than your code. `confirm-the-premise-first` establishes the ground truth
a choice hinges on before the choice is debated; this reads what one specific
installer lands on disk.

The other two sit on the install itself. This is about what an installer
writes into config you already run; whether the installer delivered the
artifact you actually intended, rather than a version silently reselected to
fit your host, is `third-party-tool-onboarding`. This asks what one tool's
installer wrote into config you already run; taking an inventory of every
configuration surface against an external reference description and reporting
a per-surface delta is `harness-config-audit`.

## When this fires

**Where:** The window between "look at this tool" and running its installer —
adopting a plugin, framework, agent harness, shared preset, or any package
whose setup step writes into config that everything else you run also reads.

**The case this came from.** A request to work out how to use a heavily-starred
agent-orchestration framework. The README read as additive. The config its init
wizard writes did not: nine hooks across six event types, four of them on
events already owned by installed tooling that rewrote the same prompts and the
same shell commands; a 71 KB instruction file loaded into every session
alongside the existing one; a setting capping the skill listing at six percent
of a budget, against roughly two hundred skills already installed; and an
allow-list granting unprompted
execution of any package from the registry against a three-entry deny list.
Subtracting capability already running left three genuinely new things out of a
page of features. Nothing had broken yet — the install had not been run.

**Another shape it takes.** *(Illustrative: A team adopts an all-in-one lint
preset for the rules it advertises. Its postinstall writes the same git hook
file their own pre-commit script owns, silently replacing it, and sets
conflicting severities for rules the existing config already defines — so the
gain is a handful of new rules and the cost is a check that stopped running.)*

## Checks

- **Fetch the config the installer writes, not the README — and diff it.**
  Where setup is a wizard that generates config from answers, reading the
  project's source does not tell you what lands. Snapshot a scratch directory
  (`git init && git commit --allow-empty -m base`), run the installer inside
  it, then read `git status` and `git diff` for the exact file set and
  contents. That diff is the input to every check below. Marketing describes
  intent; those files describe what you will be running. *(A project README
  read as a purely additive capability layer; the `settings.json` its init
  wizard writes declares nine hooks, a tool-listing budget cap, and a wildcard
  package-runner permission, none of which the README mentions.)*
- **Map every claimed slot onto its current occupant.** Enumerate the shared,
  effectively single-occupant slots it takes — each hook event, the
  always-loaded instruction file, the permission set, the tool budget, memory
  or state directories — and name what already holds each one. A slot with two
  writers is a collision to resolve before install, not a feature to enjoy.
  *(Four of the nine registered hooks landed on events already held by
  installed tooling — two of them rewriting the same prompt and the same shell
  command the incoming hooks rewrote.)*
- **Read the vendored permission list literally.** An allow-list inside a
  config you install is a standing grant to whatever runs under it, not a
  convenience default. Read each entry as the worst thing it permits, and treat
  a wildcard over a package runner or a network tool as arbitrary code
  execution with no prompt. *(An installed permission block allowed any package
  from the public registry to be executed unprompted, plus unattended pushes,
  against a deny list of three entries.)*
- **Subtract duplicated capability before counting value.** List what the tool
  offers, strike every item already covered by something installed, and read
  what survives. A long feature list that nets to two or three items — arriving
  with worse integration than the tools already wired together — is a sideways
  move being read as an upgrade. *(A feature page's worth of orchestration,
  memory, review, and codegen capability netted to three items not already
  running; the rest duplicated installed tooling.)*
- **Take the additive path, in a throwaway directory, one piece at a time.**
  Where a project ships both an all-in-one installer and a narrower path —
  single plugin, single command, config-free import — trial the narrow one in a
  scratch directory first and promote only what earns its place. *(Illustrative:
  A toolkit is trialled by running its full bootstrap in the main repo; backing
  out later means hand-reverting edits to four shared config files, while the
  one subcommand that was actually wanted needed none of them.)*

## Pre-flight check — before you install anything into a shared environment

- [ ] You have the installer's real output in front of you — the file set and
      contents it writes, captured by diffing a scratch directory where it ran,
      not the README or the docs site.
- [ ] Every shared slot it claims is listed next to the thing that already
      holds it, and each collision has a decision.
- [ ] Each permission it vendors was read as the worst action it allows, with
      wildcards over execution or network treated as unprompted arbitrary code.
- [ ] You subtracted capability you already run and can state the residue —
      what is genuinely new — in a sentence.
- [ ] If a narrower install path exists, it was trialled in a throwaway
      directory before anything touched the real configuration.

If any box is unchecked, you are adopting on the strength of a feature list, or
installing into live config you have not read — go get the installer's real
output first.
