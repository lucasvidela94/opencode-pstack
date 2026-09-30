# Host adapter: OpenCode (V2)

Source: OpenCode V2 docs (`skills`, `agents`, `commands`, `models`, `tools`).

- **Spawn subagent**: `subagent` tool with agent ID + short `description` + complete `prompt`. `background: true` for parallel/long runs. Only agents with `mode: subagent`/`all` (see `.opencode/agents/`). Permission: `subagent` with resource = agent ID.
- **General-purpose / read-only**: builtins `general` (broad) and `explore` (read-only, no edits). `poteto-agent` for full-style delegates.
- **Ask the user**: `question` tool (header, question, options). Permission: `question` resource `*`. Needs an interactive client.
- **Load skill**: `skill` tool with the exact case-sensitive ID. Permission: `skill` with resource = skill ID.
- **Files/commands/web**: `glob`/`grep`/`read`; `edit` (focused) / `write` (create/replace) / `patch` (multi-file, mostly GPT models); `shell` with `workdir`/`timeout`/`background`; `webfetch`/`websearch`; `execute` (Code Mode) for parallel calls.
- **Role models**: per-agent/command `model: provider/model#variant`, e.g. `anthropic/claude-sonnet-4-5#high`. One agent per panel member for model diversity. Session stores its own model; selecting a primary agent does not change it.
- **Skills discovery**: `.opencode/skills`, `.agents/skills`, `.claude/skills` (project, cwd → root) + `~/.config/opencode/skills`, `~/.agents/skills`, `~/.claude/skills`. ID = path-derived, case-sensitive; frontmatter `name` is display-only.
- **Hiding**: `slash: false` + `metadata.opencode/autoinvoke: false` (stays loadable by ID). There is no `user-invocable` field.
- **Slash commands**: `.opencode/commands/*.md` with `$ARGUMENTS`, `$1..$n`, `!`code`` shell blocks.
- **Routing**: `AGENTS.md` (no auto-hook; no `instructions` config resolution in V2).
