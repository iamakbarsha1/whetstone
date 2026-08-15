#!/usr/bin/env python3
"""Validate whetstone skills and plugin manifests. Dependency-free (stdlib only).

Checks, per skill under skills/*/SKILL.md:
  - frontmatter block present (opening/closing ---)
  - `name` and `description` keys present and non-empty
  - directory name matches frontmatter `name`
  - `**Type:**` line and a pre-flight check section present
  - `## The core rule` section present
  - every `## Checks` bullet carries a `*(real case)*` marker
  - pre-flight has at least one checkbox per check (no ungated check)

Checks manifests:
  - .claude-plugin/marketplace.json and plugin.json parse as JSON
  - marketplace has a non-empty `plugins` array; each entry has name + source
  - plugin.json `name` is listed as a plugin in the marketplace

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


def main():
    check_skills()
    check_manifests()
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: skills + manifests valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
