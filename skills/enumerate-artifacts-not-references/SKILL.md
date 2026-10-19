---
name: enumerate-artifacts-not-references
description: >
  Use when writing or reviewing a check that pulls candidate paths, names, IDs,
  or links out of prose and then confirms each one resolves — a completeness
  gate, a link checker, a "did you ship every file you referenced" guard.
  Scraping by surface pattern has an unbounded input set, so any document whose
  subject is the thing being matched floods the gate with false failures, and a
  gate whose normal output on a correct run is a wall of errors gets read past.
  Invert it: enumerate the real artifacts and check each is referenced — and
  keep a second, separately bounded pass for whatever the original direction
  was actually catching. Triggers on "completeness check", "verification gate",
  "check every reference resolves", "link checker", "missing file check",
  "the gate is full of false positives", "pre-delivery check", "orphan check".
---

# Enumerate Artifacts, Not References

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a case where a pre-delivery completeness gate scraped path-shaped
strings out of a document's prose and examples and reported nineteen
non-existent files alongside two real ones — on a delivery that was correct.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening,
open an issue on the repository or contact the author at the profile link
above. If the problem is the agent not following a rule below rather than
the rule itself, that's an execution failure — acknowledge and correct it.

## The core rule

A check has two directions available, and they are not equivalent. Scraping
references out of prose and confirming each resolves takes an **unbounded**
input: free text, where every path-shaped substring in an example, a quote, or
a fenced block becomes a candidate, so any document *about* the thing being
matched mis-fires by construction. Enumerating the real artifacts on disk and
confirming each is referenced takes a **bounded, verifiable** input: a finite
set you can list. Prefer the second direction. But inverting is not a one-line
swap — the two directions answer different questions, and a naive inversion
silently drops whatever the original gate existed to catch, so split the gate
into two passes, each enumerating its own real set.

This is about the direction a check enumerates in, while you still control the
check. If instead you are handed someone else's finished "X does not exist"
and have to decide whether to trust it, use `verify-absence-claims`.

## When this fires

**Where:** Writing or reviewing a completeness gate — a link checker, a "did
we ship every file we referenced" guard, an orphan check, anything that
decides whether a delivery is whole.

**The case this came from.** A pre-delivery gate grepped a staged document for
`references/`-style paths and checked each against the staged set. Run against
a document that teaches how those directories are laid out, it scraped
nineteen illustrative paths and reported every one MISSING, burying the two
true findings. Inverting it to an orphan-only pass then went green on the
original truncation bug, because there was nothing staged to iterate.

**Another shape it takes.** *(Illustrative: A dependency audit greps every
`import` in the source and checks each one resolves in the lockfile. Imports
inside commented-out code and inside a docstring's example block are candidates
too, so it reports four packages as missing — while a package that sits in the
lockfile and is imported nowhere goes unmentioned, because nothing ever
enumerates the lockfile.)*

## Checks

- **Enumerate the real set; never scrape an unbounded one.** Before writing the
  check, name its input set out loud. "Every file under `references/`,
  `scripts/`, `assets/`" is finite and listable; "every path-shaped string in
  the body" is not, and will match examples, quotes, and code fences that were
  never claims about reality. A document whose subject matter *is* the thing
  being matched is the worst case, not an edge case. *(A pre-delivery gate
  grepped a staged document's body for `references/`-style paths and checked
  each against the staged set; run against a document that teaches how those
  directories are laid out, it scraped nineteen illustrative paths —
  `references/api_docs.md`, `assets/logo.png`, `scripts/rotate_pdf.py` — and
  reported every one as MISSING, burying the two true results.)*
- **Split, because inverting alone drops the bug the gate existed for.** The
  two directions answer different questions: "is every artifact referenced?"
  (orphans) and "is every expected artifact present?" (truncation). Keep both,
  each over its own enumerable set — the live or declared set for presence, the
  delivered set for orphans. *(Pure inversion to the orphan pass alone passed
  the original truncation bug green: with the main document delivered by itself
  and nothing staged under `references/`, there was nothing to iterate, so the
  gate reported clean. Adding the presence pass over the live file list emitted
  eleven MISSING lines on that same input.)*
- **Judge the gate by its output on a known-correct input, before you trust
  it.** Run the finished check once against a delivery you know is good. If a
  correct run is not silent, the gate's signal is noise and a reader will learn
  to skim past it — which is indistinguishable from never running it. Fix the
  gate, do not train yourself to ignore its output. *(The scraping gate's
  ordinary output on a correct delivery was twenty-one lines, nineteen of them
  false; the two real findings were read past.)*

## Pre-flight check — before you trust a completeness or reference check

- [ ] The check's input set is named and **bounded** — a listable set of real
      artifacts, not "whatever matches this pattern in the text".
- [ ] Both questions are covered by **separate** passes — every artifact is
      referenced (orphans) *and* every expected artifact is present
      (truncation) — rather than one direction standing in for both.
- [ ] The check was run once against a **known-correct** input and produced no
      findings; a noisy pass on a good run was fixed, not tolerated.

If any box is unchecked, you have a gate that either floods on correct input or
goes green on the failure it was written to catch — go bound its input set.
