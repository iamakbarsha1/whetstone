#!/usr/bin/env python3
"""Validate whetstone skills and plugin manifests. Dependency-free (stdlib only).

Checks, per skill under skills/*/SKILL.md:
  - frontmatter block present (opening/closing ---)
  - `name` and `description` keys present and non-empty
  - directory name matches frontmatter `name`

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


def check_skills():
    skill_files = sorted(ROOT.glob("skills/*/SKILL.md"))
    if not skill_files:
        err("no skills found under skills/*/SKILL.md")
        return []
    names = []
    for f in skill_files:
        dir_name = f.parent.name
        text = f.read_text()
        fm = parse_frontmatter(text)
        if fm is None:
            err(f"{f.relative_to(ROOT)}: missing frontmatter (--- block)")
            continue
        # Whetstone contract: every skill declares a Type and ends in a
        # pre-flight checklist. These are what make a skill actionable under
        # load; enforce them so a shapeless skill can't merge.
        if "**Type:**" not in text:
            err(f"{f.relative_to(ROOT)}: missing `**Type:**` line")
        if "pre-flight" not in text.lower():
            err(f"{f.relative_to(ROOT)}: missing a pre-flight check section")
        name = fm.get("name", "")
        if not name:
            err(f"{f.relative_to(ROOT)}: frontmatter missing non-empty `name`")
        elif name != dir_name:
            err(f"{f.relative_to(ROOT)}: `name: {name}` != directory `{dir_name}`")
        # description may be a folded scalar (`>`), so value on the key line is
        # empty but the block is non-empty; treat presence of the key as enough
        # only when it carries a value or a block indicator.
        if "description" not in fm:
            err(f"{f.relative_to(ROOT)}: frontmatter missing `description`")
        elif fm["description"] in ("", None):
            err(f"{f.relative_to(ROOT)}: `description` is empty")
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
