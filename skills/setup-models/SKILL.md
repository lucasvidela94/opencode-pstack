---
name: setup-models
description: Configure which model fills each pstack role on your host. Use when role defaults don't match your providers, after installing, or when delegation warns about model slugs.
---

# Setup models (original to this repo, not upstream)

Upstream role lines name Cursor model slugs with `auto`/`inherit-parent` fallback. This skill maps each role to a model your host actually has. Resolve the `role model` verb through `../poteto-mode/references/hosts/` first.

## Roles to fill

| Role | Upstream default | Used by |
| --- | --- | --- |
| code delegates | `grok-4.7-xhigh-fast` | feature, refactoring, bug-fix, perf playbooks |
| hardest changes, judgment, prose | `claude-opus-5-5-max` | hardest tasks, synthesis, replies |
| arena runners / cross-judge | `claude-opus-5-5-max`, `gpt-5.6-sol-max`, `grok-4.7-xhigh-fast` | `arena` phases A and C |
| interrogate reviewers | reviewer table in `interrogate` | `interrogate` |
| explorers / explainers | `how`/`why` role lines | `how`, `why` |

## Workflow

1. Ask the user which provider and model fills each role. Keep it short: propose the closest match they have installed, accept `inherit-parent` (run on the session model) for any role.
2. Write the answers down in the user's own words, one line per role.
3. Apply per host:
   - OpenCode: set per-agent `model: provider/model#variant` in `opencode.jsonc` (one agent per panel member for diversity), or command `model` for single-shot overrides.
   - Claude Code: set `model` on the relevant skill/agent, or pick the session model with `/model`.
   - Codex: set models in Codex config; role defaults stay advisory (see `hosts/codex.md`).
4. Verify: name one role and where its model now lives. If a slug is rejected at delegation time, fall back to the closest same-family model and say so.
