---
name: scan-generated-files-for-artifacts
description: >
  Use when reviewing or signing off on a file an agent produced with a write
  tool — a doc, README, config, data file, or any non-code output. Passing
  tests prove nothing about stray harness framing: a leaked closing tag, an
  XML/markdown-fence fragment, or content past the intended EOF compiles and
  tests clean, then ships as visible garbage. Grep every agent-written file's
  head and tail for tool residue before you approve it. Triggers on "review my
  changes", "code review", "generated file", "wrote a doc", "wrote a README",
  "tool artifact", "stray tag", "harness residue", "content past EOF".
---

# Scan Generated Files for Artifacts

**Type:** Open-source — client-agnostic methodology, no project-specific detail.

**Created by akbarsha — https://github.com/iamakbarsha1**

Distilled from a review that approved a generated markdown file which compiled
and tested clean — its tail carried a leaked tool-call closing tag and shipped
as visible garbage.

**Licence:** Released under CC BY 4.0 — share and adapt for any purpose with
credit. Full text: `LICENSE` at the repository root.

**Feedback & Support:** If a rule here proves wrong or needs sharpening, open an
issue on the repository or contact the author at the profile link above. If the
problem is the agent not following a rule below rather than the rule itself,
that's an execution failure — acknowledge and correct it.

## The core rule

Tests exercise code behaviour; they say nothing about the bytes of a non-code
file. When an agent writes a file through a tool, the harness framing around
that write — a closing `</content>` or invoke/function tag, a stray markdown
fence, content past the point the spec said the file should end — can leak into
the file itself. It parses fine, compiles fine, tests green, and ships as
visible garbage a reader sees on the first or last screen. A review that runs
only the test suite misses this whole class. So for every file an agent produced
with a write tool, spend one cheap grep on its head and tail before sign-off,
and confirm it ends exactly where it should.

## Checks

- **Grep the head and tail of every agent-written file for harness residue.**
  Search the changed non-code files — especially the first and last few lines —
  for tool/harness tag fragments: `</content>`, closing invoke/function tags,
  orphaned markdown fences, or any framing that belongs to the write mechanism,
  not the content. A trivial `grep` catches what the test suite structurally
  cannot. *(A review approved a generated markdown doc that compiled and tested
  clean; its tail carried a leaked tool-call closing tag and shipped as visible
  garbage.)*
- **Confirm the file ends where the spec says it ends.** Content past the
  intended EOF — a duplicated section, a trailing fragment, a second copy of the
  closing block — reads as garbage but breaks no test. Check the last lines
  against what the file was supposed to contain, not just that it is non-empty.
  *(Illustrative: an agent-generated config had the intended body followed by a
  repeated tail block; every parser accepted it and the duplicate silently
  overrode the real values.)*
- **Never let a green test suite stand in for a byte-level check on non-code
  output.** Docs, configs, fixtures, and data files pass tests they were never
  the subject of. Treat "tests pass" and "the file is clean" as two separate
  claims, and prove the second one directly for anything an agent wrote.
  *(Illustrative: a README shipped with an XML fence fragment in its last
  paragraph; CI was green because no test reads the README.)*

## Pre-flight check — before you approve a review that includes generated files

- [ ] Every file an agent produced via a write tool was grepped at head and tail
      for harness/tool-framing residue (`</content>`, closing invoke/function
      tags, stray fences).
- [ ] Each such file ends exactly where its spec says it should — no content
      past the intended EOF, no duplicated tail block.
- [ ] "Tests pass" was not treated as proof the file's bytes are clean; the
      byte-level check was run separately for non-code output.

If any box is unchecked, a generated file may carry invisible artifacts that
test clean and ship as garbage — run the scan before approving.
