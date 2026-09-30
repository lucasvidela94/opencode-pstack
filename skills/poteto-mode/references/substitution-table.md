# Substitution table: Cursor pstack -> OpenCode

Checklist for every ported file (applied by `scripts/adapt-upstream.py`). Translate, don't copy.

| Upstream (Cursor) | OpenCode |
| --- | --- |
| `Task` tool / `subagent_type:` | `subagent` tool + agent ID in `.opencode/agents/*.md` (`mode: subagent`) |
| `AskQuestion` / `AskUserQuestion` | `question` tool |
| `generalPurpose` subagent | `general` builtin subagent (read-only variants: `explore`) |
| `readonly: true/false` (Task param) | agent `permissions` (deny vs allow `edit`/`shell`) |
| `run_in_background: true` | `background: true` |
| transcript paths, cloud agents, background-task API | drop; use sessions (foreground or `background: true` subagents). Two transcript passages kept verbatim + allowlisted (see `PORT-NOTES.md`) |
| model slugs (`claude-*`, `gpt-*`, `grok-*`) + `/setup-pstack` + `pstack-models.mdc` | `provider/model#variant` per agent/command or root `model`; roles configured in OpenCode config |
| `SessionStart` hook forcing poteto-mode | routing line in `AGENTS.md`, no auto-hook |
| `disable-model-invocation: true` | dropped; hide with `slash: false` + `metadata.opencode/autoinvoke: false` when needed |
| `is_background` flag | `mode: subagent` + `background: true` at call time |
| `.cursor-plugin/`, Cursor manifests/commands | `skills/<name>/SKILL.md` (canonical) + `.opencode/agents/`, `.opencode/commands/` |
| `tools/upstream.json` pin | `UPSTREAM_COMMIT` + `UPSTREAM_SYNC.md` + `scripts/adapt-upstream.py` |

Forbidden-as-usable tokens in this repo (checked in CI): `subagent_type`, `AskUserQuestion`, `disable-model-invocation`, `.cursor-plugin`, `is_background`, `/setup-pstack`, `pstack-models.mdc`, `` `Task` ``, `generalPurpose`. Port-note blockquotes may name them to disclaim them.
