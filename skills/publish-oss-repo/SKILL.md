---
name: publish-oss-repo
description: >
  Use when preparing a repository for public release, or auditing one that
  already has working code but still reads as neglected to a stranger or to
  GitHub's own UI — "has the files" is not "reads as maintained". Triggers
  on "publish a repo", "open source this", "release", "make it look
  maintained", "license shows Other", "add topics", "GitHub release", "repo
  badges".
---

# Publish an OSS Repo That Reads as Maintained

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from reworking a skills repository from merely functional to
publish-ready and finding that working code and green CI still read as
abandoned to GitHub's own UI and to a stranger browsing it.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

"Has the files" is not "reads as maintained." A repo can have a LICENSE, a
changelog, and passing CI and still present as abandoned, because publishing
quality is signalled by machine-detectable facts — a canonical license the
platform's own detector recognizes, tagged releases per version, discoverable
topics, and CI that enforces the artifact's actual contract — and each of
those signals has to be verified through the platform's own API, not assumed
true because the file that's supposed to produce it exists.

## Checks

- **Fetch the canonical license text; never paraphrase it.** GitHub's license
  detector matches against the official legal text, not a legally-equivalent
  summary — a hand-written paraphrase makes GitHub display the license as
  "Other" and drops the repo out of license-filtered search. Pull the real
  text from the canonical source (creativecommons.org, choosealicense.com,
  the SPDX list) instead of transcribing it, and confirm detection through the
  platform's own API rather than eyeballing the file. *(A LICENSE file was a
  hand-written CC BY 4.0 summary; GitHub showed the license as "Other" until
  the canonical legal text replaced it, confirmed via `gh repo view --json
  licenseInfo` — fetching the canonical text also sidestepped a content-filter
  block that pasting the full 400-line legal text directly had tripped.)*
- **Cut a tag and a GitHub Release per version, not just a manifest bump.** A
  version bump that lives only in a manifest file is invisible outside the
  diff — no `git tag` output, no entry under Releases — and the repo reads as
  abandoned even when the code is current. Every version bump gets a matching
  git tag and release, not only the ones that feel significant. *(A plugin
  manifest had been bumped through several versions with zero git tags and
  zero GitHub Releases behind them; the repo looked unmaintained until a tag
  and release were cut for each version.)*
- **Set repo topics before anyone can find it by browsing.** GitHub's topic
  search and Explore surface only index repos with topics attached — zero
  topics means zero discoverability outside an exact-name search. Add topics
  for the domain, the language or framework, and the specific problem the
  repo solves. *(A skills repository had no GitHub topics set at all, so it
  never surfaced in topic-based discovery until topics were added.)*
- **Make CI enforce the artifact's contract, not just its metadata.** A
  validator that checks frontmatter presence but not the body's required
  shape lets a contribution merge with the right header and none of the
  substance underneath — the gate exists but gates nothing that matters.
  Enforce the structural contract itself (required sections, checklist
  parity, grounding markers) so a shapeless PR fails CI before a human has to
  catch it in review. *(A skills-repo validator checked only that frontmatter
  had `name` and `description`; it never checked for the required `## The
  core rule` section, checklist-to-check parity, or grounding markers, so a
  skill missing all three would still have passed CI.)*

## Pre-flight check — before you call a repo publish-ready

- [ ] The LICENSE file is the canonical legal text from the official source,
      and the platform's own API (e.g. `gh repo view --json licenseInfo`)
      confirms the license is detected, not shown as "Other".
- [ ] Every version bump in the manifest or changelog has a matching git tag
      and a platform release, not just a diff.
- [ ] The repo has topics set for its domain, language/framework, and the
      specific problem it solves — not zero.
- [ ] CI enforces the artifact's structural contract (required sections,
      checklist parity, grounding markers), not just frontmatter presence.

If any box is unchecked, the repo has the files but doesn't read as
maintained — go close the gap before calling it publish-ready.
