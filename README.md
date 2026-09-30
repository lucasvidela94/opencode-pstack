# opencode-pstack — poteto-mode for OpenCode, Claude Code & Codex

[![check](https://github.com/lucasvidela94/opencode-pstack/actions/workflows/check.yml/badge.svg)](https://github.com/lucasvidela94/opencode-pstack/actions/workflows/check.yml)
![skills](https://img.shields.io/badge/skills-40-blue.svg)
![license](https://img.shields.io/badge/license-MIT-green.svg)

[Lauren Tan](https://github.com/poteto) (poteto) shipped 1,000 PRs in a month by making her agents work the way she does: route every non-trivial task through a playbook, verify against the real thing, keep diffs small. That system is **pstack** — and its router is **poteto-mode**. This repo ports it, faithfully and host-neutrally, to OpenCode, Claude Code, and Codex.

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

Alternatives: Claude Code plugin (`/plugin marketplace add lucasvidela94/opencode-pstack`, manifests in `.claude-plugin/`), Codex plugin (`.codex-plugin/` + `plugin.json`). Restart/reload the agent afterwards. If your Codex build doesn't scan `~/.agents/skills`, copy the skills to `~/.codex/skills`.

New here? [`docs/guide/`](docs/guide/) walks through three real tasks with copy-paste prompts.

## The skills

**Router:** `poteto-mode` — picks the playbook and runs the rest as steps need them. 23 playbooks: investigation, bug fix, perf, hillclimb, forensics, feature, refactoring, prototype, visual parity, babysit, shipping, autopilot, orchestrate, and more.

| Skill | Use it when |
| --- | --- |
| `how` | you want to know how part of the system works |
| `why` | you want evidence for why it was built that way |
| `architect` | the design must be settled before code (runs `arena` in Phase B) |
| `arena` | N parallel candidates, pick a base, graft the best parts, verify |
| `swarm` | parallel fan-out: coverage, races, verification lanes |
| `tdd` | bug fix with a cheap failing test first (skipped when impractical — really) |
| `interrogate` | adversarial review tries to break your design or diff |
| `blast-radius` | what could this change break beyond the diff |
| `figure-it-out` | no playbook fits — designs a bespoke rigorous one |
| `create-verification-skill` | your project needs a repeatable way to prove real behavior |
| `maintain-verification-skill` | that verification skill drifted from the product |
| `show-me-your-work` | long/unattended work needs an auditable decision trail |
| `technical-writing` | docs, RFCs, PR descriptions, commit messages |
| `unslop` | strip AI slop from prose and code |
| `no-comments` | delete comment noise, keep load-bearing whys |
| `typescript-best-practices` | TS/React rules for this stack |

**Principles:** the 23 upstream `principle-*` leaf skills (prove it works, subtract before you add, laziness protocol, …). The agent names each principle that shaped a decision — and cites only the ones it actually read that session.

## How the port works

One canonical `skills/` tree with open-standard frontmatter (`name` + `description` only). Skill bodies speak capability verbs — *spawn a subagent*, *ask the user*, *role model* — resolved per host through adapters in `skills/poteto-mode/references/hosts/` (`_contract.md` plus one page each for OpenCode, Claude Code, Codex, with honest fallbacks where a host lacks the capability).

Nothing is rewritten by hand: `scripts/adapt-upstream.py` ports `cursor/plugins` pstack at the commit pinned in `UPSTREAM_COMMIT` with mechanical substitutions only; `python3 scripts/check.py` gates every change. Every deviation is logged in `PORT-NOTES.md`.

## Credit

All engineering content is Lauren Tan's ([cursor/plugins `pstack`](https://github.com/cursor/plugins/tree/main/pstack), MIT). This repo tracks upstream and changes only what portability requires. If Cursor is your home, use her original.

## License

MIT — see `LICENSE`.
