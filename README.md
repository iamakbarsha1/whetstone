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

These follow the Claude Code skill layout (`SKILL.md` with `name` +
`description` frontmatter). To install one, copy its folder into your skills
directory:

```sh
cp -R skills/verify-through-the-real-path ~/.claude/skills/
```

Or copy them all:

```sh
cp -R skills/* ~/.claude/skills/
```

The `description` frontmatter carries trigger phrases, so a skill-aware agent
surfaces each one when the situation matches.

## Licence

All skills are released under [CC BY 4.0](LICENSE) — share and adapt for any
purpose with credit. Created by akbarsha (https://github.com/iamakbarsha1).

Feedback on any skill's methodology is welcome as a repository issue.
