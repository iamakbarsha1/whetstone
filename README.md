# whetstone

Agent skills honed on real work. Each skill here is a short, self-contained
rule set distilled from a concrete failure or hard-won lesson during real
engineering sessions, written so an AI coding agent (or a human) can apply it
without the original context.

A whetstone sharpens a blade. These sharpen the agent.

## Skills

| Skill | Use it when |
|-------|-------------|
| [`verify-through-the-real-path`](skills/verify-through-the-real-path) | Before claiming something works, is done, safe, or fast — verify through the actual trigger, real data, and representative conditions, not a stand-in. |
| [`plan-cross-encoding-review`](skills/plan-cross-encoding-review) | Reviewing an implementation plan or spec — catch the bug where one intent is encoded twice and the copies disagree. |
| [`read-the-real-failing-call`](skills/read-the-real-failing-call) | Hardening against a failure mode — instrument the real failing call before and after, because a plausible hypothesis is not a diagnosis. |
| [`confirm-the-premise-first`](skills/confirm-the-premise-first) | Designing when a choice depends on a technical property (local vs remote, reversible vs not) — state the ground truth before asking downstream questions. |
| [`running-long-background-jobs`](skills/running-long-background-jobs) | Launching or verifying a long-running/detached job, or reconciling a batch against a corpus other processes also write to. |

## Install

### As a Claude Code plugin (recommended)

Add the marketplace, then install the plugin — all skills come with it:

```sh
/plugin marketplace add iamakbarsha1/whetstone
/plugin install whetstone@whetstone-skills
```

Run these inside Claude Code. `whetstone@whetstone-skills` is
`plugin@marketplace` — the plugin is `whetstone`, the marketplace is
`whetstone-skills`.

### Manual copy

Each skill is a self-contained folder in the Claude Code skill layout
(`SKILL.md` with `name` + `description` frontmatter). Copy one:

```sh
cp -R skills/verify-through-the-real-path ~/.claude/skills/
```

Or all of them:

```sh
cp -R skills/* ~/.claude/skills/
```

The `description` frontmatter carries trigger phrases, so a skill-aware agent
surfaces each one when the situation matches.

### Other agents / plain reading

Every `SKILL.md` is plain Markdown — the rules and pre-flight checklists read
fine on their own. Any agent that can load a system prompt or reference file
can use them: paste the skill body in, or point your tool's context at the
file. Only the plugin auto-discovery above is Claude Code-specific.

## Contributing

New skills come from real failures, not general advice. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the bar and the skill format, and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Validate locally with
`python3 scripts/validate_skills.py` (CI runs the same check).

## Licence

All skills are released under [CC BY 4.0](LICENSE) — share and adapt for any
purpose with credit. Created by akbarsha (https://github.com/iamakbarsha1).

Feedback on any skill's methodology is welcome as a repository issue.
