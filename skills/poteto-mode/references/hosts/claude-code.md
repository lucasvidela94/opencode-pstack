# Host adapter: Claude Code

Source: Claude Code docs (`skills`, Agent Skills standard). Follows the open standard; repo frontmatter stays spec-only (`name`, `description`).

- **Spawn subagent**: `Task` tool with `subagent_type` (builtin `Explore`, `Plan`, `general-purpose`, or custom from `.claude/agents/`). `poteto-agent` for full-style delegates.
- **Ask the user**: `AskUserQuestion` tool.
- **Role models**: skill frontmatter `model` (same values as `/model`, or `inherit`) + `effort` (`low`…`max`); subagent model per agent config. `auto`/`inherit-parent` roles = `inherit` / omit.
- **Skills**: `~/.claude/skills/`, `.claude/skills/`; `/skill-name` invocation; `description` drives auto-load. `user-invocable: false` = Claude-only (hidden from `/` menu). `disable-model-invocation: true` = user-only trigger. Commands merged into skills (`.claude/commands/` still works).
- **Install**: `npx skills add <repo> --skill '*' --agent claude-code [--global]`, or `/plugin marketplace add <owner>/<repo>` + `/plugin install <name>@<marketplace>` (see `.claude-plugin/`).
- **Routing**: `CLAUDE.md` (this repo ships the same routing line as `AGENTS.md`).
