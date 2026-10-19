#!/usr/bin/env python3
"""Validate whetstone skills and plugin manifests. Dependency-free (stdlib only).

Checks, per skill under skills/*/SKILL.md:
  - frontmatter block present (opening/closing ---)
  - `name` and `description` keys present and non-empty
  - directory name matches frontmatter `name`
  - `**Type:**` line and a pre-flight check section present
  - `## The core rule` section present
  - `## When this fires` section present, with its Where / case / illustrative
    lines
  - every `## Checks` bullet carries a `*(real case)*` marker
  - pre-flight has at least one checkbox per check (no ungated check)

Checks manifests:
  - .claude-plugin/marketplace.json and plugin.json parse as JSON
  - marketplace has a non-empty `plugins` array; each entry has name + source
  - plugin.json `name` is listed as a plugin in the marketplace
  - plugin.json `version` equals the marketplace entry's `version`

Checks cross-surface consistency (the skill count is encoded in ~8 places):
  - every skills/*/ directory has a README table row and a docs/index.html card
  - every README row and docs card points at a directory that exists
  - every README row carries a non-empty Example cell
  - every declared count (badges, meta tags, hero, section headers) equals the
    real directory count

Exit 0 = clean, 1 = one or more failures (printed). Run locally or in CI.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def err(msg):
    errors.append(msg)


def parse_frontmatter(text):
    """Return dict of top-level `key:` values from a leading --- fenced block.

    Only needs to see whether `name`/`description` exist and are non-empty, so
    it captures the scalar on the key line (folded `>`/`|` still count as
    non-empty because a value or block indicator follows the colon)."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None
    body = m.group(1)
    fields = {}
    for line in body.splitlines():
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if km:
            fields[km.group(1)] = km.group(2).strip()
    return fields


def check_bullets(text):
    """Return the top-level check bullets under the `## Checks` section.

    Each bullet starts `- **` and runs until the next such bullet or the next
    `## ` heading; indented sub-bullets stay attached to their parent. A skill
    that folds its single rule into `## The core rule` has no `## Checks` and
    returns []."""
    m = re.search(r"(?ms)^## Checks\b.*?(?=^## |\Z)", text)
    if not m:
        return []
    parts = re.split(r"(?m)^- \*\*", m.group(0))[1:]
    return ["- **" + p for p in parts]


def check_skills():
    skill_files = sorted(ROOT.glob("skills/*/SKILL.md"))
    if not skill_files:
        err("no skills found under skills/*/SKILL.md")
        return []
    names = []
    for f in skill_files:
        rel = f.relative_to(ROOT)
        dir_name = f.parent.name
        text = f.read_text()
        fm = parse_frontmatter(text)
        if fm is None:
            err(f"{rel}: missing frontmatter (--- block)")
            continue
        # Whetstone contract: every skill declares a Type and ends in a
        # pre-flight checklist. These are what make a skill actionable under
        # load; enforce them so a shapeless skill can't merge.
        if "**Type:**" not in text:
            err(f"{rel}: missing `**Type:**` line")
        if "pre-flight" not in text.lower():
            err(f"{rel}: missing a pre-flight check section")
        # A skill states one core rule, then either folds its single rule into
        # that paragraph (no `## Checks`) or lists checks — and then every check
        # must carry a `*(real case)*` and be gated by a pre-flight checkbox.
        # See CONTRIBUTING.md "Skill format".
        if "## The core rule" not in text:
            err(f"{rel}: missing `## The core rule` section")
        # A rule the reader cannot place is a rule they skip. `## When this
        # fires` is where the skill says what kind of work it belongs to and
        # shows the situation twice — once from the scar it was distilled
        # from, once from a different domain so the shape generalizes.
        if "## When this fires" not in text:
            err(f"{rel}: missing `## When this fires` section")
        else:
            for lead, label in (
                ("**Where:**", "a `**Where:**` line"),
                ("**The case this came from.**", "the distilled-case example"),
                ("**Another shape it takes.**", "the second, illustrative example"),
            ):
                if lead not in text:
                    err(f"{rel}: `## When this fires` missing {label}")
        bullets = check_bullets(text)
        for cb in bullets:
            if "*(" not in cb:
                head = cb.splitlines()[0].strip()[:70]
                err(f"{rel}: Check lacks a `*(real case)*` — {head}")
        if bullets:
            nbox = len(re.findall(r"(?m)^\s*- \[ \]", text))
            if nbox < len(bullets):
                err(
                    f"{rel}: {nbox} pre-flight checkbox(es) for {len(bullets)} "
                    f"checks — every check must be gated"
                )
        name = fm.get("name", "")
        if not name:
            err(f"{rel}: frontmatter missing non-empty `name`")
        elif name != dir_name:
            err(f"{rel}: `name: {name}` != directory `{dir_name}`")
        # description may be a folded scalar (`>`), so value on the key line is
        # empty but the block is non-empty; treat presence of the key as enough
        # only when it carries a value or a block indicator.
        if "description" not in fm:
            err(f"{rel}: frontmatter missing `description`")
        elif fm["description"] in ("", None):
            err(f"{rel}: `description` is empty")
        if name:
            names.append(name)
    return names


def load_json(rel):
    p = ROOT / rel
    if not p.exists():
        err(f"{rel}: missing")
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError as e:
        err(f"{rel}: invalid JSON — {e}")
        return None


def check_manifests():
    market = load_json(".claude-plugin/marketplace.json")
    plugin = load_json(".claude-plugin/plugin.json")
    market_plugin_names = []
    if market is not None:
        plugins = market.get("plugins")
        if not isinstance(plugins, list) or not plugins:
            err("marketplace.json: `plugins` must be a non-empty array")
        else:
            for i, pl in enumerate(plugins):
                if not pl.get("name"):
                    err(f"marketplace.json: plugins[{i}] missing `name`")
                if not pl.get("source"):
                    err(f"marketplace.json: plugins[{i}] missing `source`")
                if pl.get("name"):
                    market_plugin_names.append(pl["name"])
    if plugin is not None:
        pname = plugin.get("name")
        if not pname:
            err("plugin.json: missing `name`")
        elif market_plugin_names and pname not in market_plugin_names:
            err(f"plugin.json: `name: {pname}` not listed in marketplace plugins {market_plugin_names}")
        # The version is encoded twice; a release that bumps one and not the
        # other ships a manifest pair that disagrees about what it is.
        if market is not None and pname:
            entry = next((p for p in market.get("plugins", []) if p.get("name") == pname), None)
            if entry and entry.get("version") != plugin.get("version"):
                err(
                    f"version mismatch: plugin.json {plugin.get('version')!r} != "
                    f"marketplace.json {entry.get('version')!r}"
                )


# --- cross-surface consistency -------------------------------------------
# The skill count and the skill list are encoded across README.md and
# docs/index.html. Enumerate the real set (the directories) and check the
# surfaces against it — never scrape the prose for skill-shaped names and
# check those resolve, which has no bounded input set. Presence and orphans
# are separate questions, so they get separate passes: a single direction
# goes green on half the drift. See skills/enumerate-artifacts-not-references.

_ONES = (
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen"
).split()
_TENS = ("", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety")


def number_word(n):
    """Spell `n` in lowercase English. ponytail: 0-99 only — the site header is
    the sole caller and the library is nowhere near 100."""
    if n < 20:
        return _ONES[n]
    tens, ones = divmod(n, 10)
    return _TENS[tens] + (f"-{_ONES[ones]}" if ones else "")


def check_cross_surface():
    real = sorted(p.name for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file())
    total = len(real)
    readme = (ROOT / "README.md").read_text()
    site = (ROOT / "docs" / "index.html").read_text()

    # README catalogue rows: | [`name`](skills/name) | use it when | example |
    rows = re.findall(
        r"(?m)^\|\s*\[`([a-z0-9-]+)`\]\(skills/([a-z0-9-]+)\)\s*\|(.*)$", readme
    )
    for label, target, rest in rows:
        if label != target:
            err(f"README.md: row labelled `{label}` links to skills/{target}")
        # The catalogue carries the example too, so a row with an empty third
        # cell is a skill the reader can place only by opening its file.
        cells = [c.strip() for c in rest.split("|")]
        if len(cells) < 2 or not cells[1]:
            err(f"README.md: row for skills/{target} has an empty Example cell")
    readme_listed = {t for _, t, _ in rows}

    # docs cards: an anchor to the skill tree plus a matching slug line.
    cards = re.findall(
        r'<a class="skill" href="[^"]*/skills/([a-z0-9-]+)"[^>]*>\s*'
        r'<div class="slug">([a-z0-9-]+) ',
        site,
    )
    for href, slug in cards:
        if href != slug:
            err(f"docs/index.html: card slug `{slug}` links to skills/{href}")
    site_listed = {h for h, _ in cards}

    # Pass 1 — presence: every real skill reaches both catalogues.
    for name in real:
        if name not in readme_listed:
            err(f"README.md: no table row for skills/{name}")
        if name not in site_listed:
            err(f"docs/index.html: no card for skills/{name}")

    # Pass 2 — orphans: every catalogued skill is a directory that exists.
    for name in sorted(readme_listed - set(real)):
        err(f"README.md: row for skills/{name}, which does not exist")
    for name in sorted(site_listed - set(real)):
        err(f"docs/index.html: card for skills/{name}, which does not exist")

    # Pass 3 — declared counts: every surface agrees with the real total.
    surfaces = [
        ("README.md", "skills badge", readme, r"badge/skills-(\d+)-"),
        ("docs/index.html", "meta description", site, r'content="(\d+) agent skills,'),
        ("docs/index.html", "og/twitter description", site, r"scar\. (\d+) rule sets"),
        ("docs/index.html", "hero eyebrow", site, r"Whetstone · (\d+) skills ·"),
        ("docs/index.html", "hero stat", site,
         r'<div class="n">(\d+)</div><div class="l mono">Skills</div>'),
        ("docs/index.html", "install line", site, r"all (\d+) skills come with it"),
    ]
    for path, label, text, pattern in surfaces:
        found = re.findall(pattern, text)
        if not found:
            err(f"{path}: {label} count surface not found (pattern changed?)")
        for value in found:
            if int(value) != total:
                err(f"{path}: {label} says {value} skills, {total} directories exist")

    # The section header spells the count out.
    m = re.search(r"<h2>([A-Za-z-]+) edges,", site)
    if not m:
        err("docs/index.html: section header count surface not found (pattern changed?)")
    elif m.group(1).lower() != number_word(total):
        err(
            f"docs/index.html: section header says '{m.group(1)} edges', "
            f"{total} directories exist"
        )

    # Pass 4 — per-section counts match the cards in that section and sum to
    # the total. A skill added to the grid but not the header count, or filed
    # in no section at all, fails here.
    section_total = 0
    for block in re.split(r'<div class="cat">', site)[1:]:
        block = block.split("</section>")[0]
        head = re.search(r"<h3>(.*?)</h3>", block)
        declared = re.search(r'<span class="count mono">(\d+) skills</span>', block)
        if not head or not declared:
            continue
        actual = len(re.findall(r'<a class="skill"', block))
        if int(declared.group(1)) != actual:
            err(
                f"docs/index.html: section '{head.group(1)}' header says "
                f"{declared.group(1)} skills, {actual} cards present"
            )
        section_total += actual
    if section_total != total:
        err(f"docs/index.html: sections hold {section_total} cards, {total} directories exist")


def main():
    check_skills()
    check_manifests()
    check_cross_surface()
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: skills + manifests valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
