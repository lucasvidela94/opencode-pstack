# Substitution table: Cursor pstack -> host-neutral skills

Checklist for every ported file (applied by `scripts/adapt-upstream.py`). Translate, don't copy.

| Upstream (Cursor) | This repo (neutral verb → host adapter) |
| --- | --- |
| `Task` tool / `subagent_type:` | spawn a subagent (see `skills/poteto-mode/references/hosts/`) |
| `AskQuestion` / `AskUserQuestion` | ask the user (see hosts) |
| `generalPurpose` subagent | a general-purpose subagent (see hosts) |
| `readonly: true/false` (Task param) | read-only / with full tools (see hosts) |
| `run_in_background: true` | in the background (see hosts) |
| transcript paths, cloud agents, background-task API | per-file host-limits note + `hosts/_contract.md` fallbacks. Two transcript passages kept verbatim + allowlisted (see below) |
| model slugs + `/setup-pstack` + `pstack-models.mdc` | role-model configuration (see hosts); OpenCode: `provider/model#variant` per agent/command; Claude Code: `model`/`effort` + agent config; Codex: advisory, via Codex config |
| `SessionStart` hook forcing poteto-mode | routing line in `AGENTS.md` / `CLAUDE.md`, no auto-hook |
| `disable-model-invocation: true` | dropped from canonical frontmatter (host-specific; each host resolves hiding via its adapter) |
| `is_background` flag | dropped; background-ness is a call-time host concern |
| `.cursor-plugin/`, Cursor manifests/commands | `skills/<name>/SKILL.md` (canonical) + host packages (`.opencode/`, `.claude-plugin/`, `.codex-plugin/`) |
| `tools/upstream.json` pin | `UPSTREAM_COMMIT` + `UPSTREAM_SYNC.md` + `scripts/adapt-upstream.py` |

Forbidden-as-usable tokens in canonical skill bodies (checked in CI): `subagent_type`, `AskUserQuestion`, `disable-model-invocation`, `.cursor-plugin`, `is_background`, `/setup-pstack`, `pstack-models.mdc`, `` `Task` ``, `generalPurpose`, `user-invocable`, `context: fork`. Mapping docs (`hosts/`, this table) name them by design and are exempt.
