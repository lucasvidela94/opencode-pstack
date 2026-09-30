# poteto-mode for OpenCode, Claude Code & Codex

[![check](https://github.com/lucasvidela94/opencode-pstack/actions/workflows/check.yml/badge.svg)](https://github.com/lucasvidela94/opencode-pstack/actions/workflows/check.yml)
![skills](https://img.shields.io/badge/skills-45-blue.svg)
![license](https://img.shields.io/badge/license-MIT-green.svg)

> Also listed on [skills.sh](https://skills.sh/lucasvidela94/opencode-pstack/poteto-mode) — installs there rank the leaderboard.

A portable port of [Lauren Tan](https://github.com/poteto) (poteto)'s [pstack](https://github.com/cursor/plugins/tree/main/pstack).

> If you want to go fast, go deep first. Rigorous agent workflows you can parallelize with confidence.

## 30-second start

```bash
npx -y skills@latest add lucasvidela94/opencode-pstack --skill '*' --agent opencode --global --yes
```

Then say:

```text
Use the poteto-mode skill. The export writes duplicate rows when a retry lands mid-run. Repro first, then fix and verify.
```

`poteto-mode` matches a playbook (bug fix, feature, perf, investigation, plan, …), runs the supporting skills as steps need them, and shows evidence. You describe the goal and how you'll know it's done — no micromanaging.

## Install

| Host | Command |
| --- | --- |
| OpenCode | `npx -y skills@latest add lucasvidela94/opencode-pstack --skill '*' --agent opencode --global --yes` |
| Claude Code | `npx -y skills@latest add lucasvidela94/opencode-pstack --skill '*' --agent claude-code --global --yes` |
| Codex | `npx -y skills@latest add lucasvidela94/opencode-pstack --skill '*' --agent codex --global --yes` |

OpenCode also needs its agents/commands (the `skills` CLI only installs skills):

```bash
./scripts/setup-opencode.sh --global   # or --project
```

Verified with the `skills` CLI: it discovers all 45 skills and installs byte-identical copies to `~/.agents/skills` (OpenCode, Codex) and `~/.claude/skills` (Claude Code).

Alternatives: Claude Code plugin (`/plugin marketplace add lucasvidela94/opencode-pstack`, manifests in `.claude-plugin/`), Codex plugin (`.codex-plugin/` + `plugin.json`). Restart/reload the agent afterwards. If your Codex build doesn't scan `~/.agents/skills`, copy the skills to `~/.codex/skills`.

New here? [`docs/guide/`](docs/guide/) walks through three real tasks with copy-paste prompts.

## Why this exists

Agents fail in predictable ways. This repo answers three of them:

* **They declare victory without proof.** Every playbook ends in verification against the real artifact, and `principle-prove-it-works` forbids proxies. `create-verification-skill` gives your project a repeatable harness so proof isn't improvised each time.
* **They ship slop.** `unslop`, `no-comments`, and the laziness/subtraction principles keep diffs and prose small. `tdd` refuses bad tests instead of writing them to satisfy a workflow.
* **They balloon the diff.** `blast-radius` checks beyond the change, `architect` settles design before code, and `arena` compares candidates before committing to a shape.

## The skills

**Router:** [`poteto-mode`](skills/poteto-mode/SKILL.md) — picks the playbook and runs the rest as steps need them. 23 playbooks: investigation, bug fix, perf, hillclimb, forensics, feature, refactoring, prototype, visual parity, babysit, shipping, autopilot, orchestrate, and more.

| Skill | Use it when |
| --- | --- |
| [`how`](skills/how/SKILL.md) | you want to know how part of the system works |
| [`why`](skills/why/SKILL.md) | you want evidence for why it was built that way |
| [`architect`](skills/architect/SKILL.md) | the design must be settled before code (runs `arena` in Phase B) |
| [`arena`](skills/arena/SKILL.md) | N parallel candidates, pick a base, graft the best parts, verify |
| [`swarm`](skills/swarm/SKILL.md) | parallel fan-out: coverage, races, verification lanes |
| [`tdd`](skills/tdd/SKILL.md) | bug fix with a cheap failing test first (skipped when impractical — really) |
| [`interrogate`](skills/interrogate/SKILL.md) | adversarial review tries to break your design or diff |
| [`blast-radius`](skills/blast-radius/SKILL.md) | what could this change break beyond the diff |
| [`figure-it-out`](skills/figure-it-out/SKILL.md) | no playbook fits — designs a bespoke rigorous one |
| [`create-verification-skill`](skills/create-verification-skill/SKILL.md) | your project needs a repeatable way to prove real behavior |
| [`maintain-verification-skill`](skills/maintain-verification-skill/SKILL.md) | that verification skill drifted from the product |
| [`show-me-your-work`](skills/show-me-your-work/SKILL.md) | long/unattended work needs an auditable decision trail |
| [`technical-writing`](skills/technical-writing/SKILL.md) | docs, RFCs, PR descriptions, commit messages |
| [`setup-models`](skills/setup-models/SKILL.md) | map each pstack role to a model your host has (original to this repo) |
| [`reflect`](skills/reflect/SKILL.md) | mine the run for learnings, route each to a skill edit |
| [`recall`](skills/recall/SKILL.md) | pull the shared record: past symptoms, reverted fixes, firing errors |
| [`teach`](skills/teach/SKILL.md) | teach a concept over sessions in a stateful workspace |
| [`bro`](skills/bro/SKILL.md) | restate the last message in plain human language |
| [`unslop`](skills/unslop/SKILL.md) | strip AI slop from prose and code |
| [`no-comments`](skills/no-comments/SKILL.md) | delete comment noise, keep load-bearing whys |
| [`typescript-best-practices`](skills/typescript-best-practices/SKILL.md) | TS/React rules for this stack |

**Principles:** the 23 upstream `principle-*` leaf skills (prove it works, subtract before you add, laziness protocol, …). The agent names each principle that shaped a decision — and cites only the ones it actually read that session.

## What this never does

No binaries, no telemetry, no auto-hooks, no review gates on by default, no config replaces. Installing adds skill files (backing up anything it would overwrite); uninstalling is deleting those files. `scripts/doctor.sh` reports install health and changes nothing. Per-host behavior: [`docs/hosts.md`](docs/hosts.md).

## How the port works

One canonical `skills/` tree with open-standard frontmatter (`name` + `description` only). Skill bodies speak capability verbs — *spawn a subagent*, *ask the user*, *role model* — resolved per host through adapters in `skills/poteto-mode/references/hosts/` (`_contract.md` plus one page each for OpenCode, Claude Code, Codex, with honest fallbacks where a host lacks the capability).

Nothing is rewritten by hand: `scripts/adapt-upstream.py` ports `cursor/plugins` pstack at the commit pinned in `UPSTREAM_COMMIT` with mechanical substitutions only; `python3 scripts/check.py` gates every change. Every deviation is logged in `PORT-NOTES.md`.

## Credit

All engineering content is Lauren Tan's ([cursor/plugins `pstack`](https://github.com/cursor/plugins/tree/main/pstack), MIT). This repo tracks upstream and changes only what portability requires. If Cursor is your home, use her original.

## License

MIT — see `LICENSE`.
