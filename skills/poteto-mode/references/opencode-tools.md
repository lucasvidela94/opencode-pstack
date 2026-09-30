# opencode-tools (single host mapping)

Source of truth for how capability verbs execute on OpenCode V2. Skills use verbs; only this file names tools.

| Verb | OpenCode |
| --- | --- |
| launch a subagent | `subagent` tool: `agentID` + short `description` + complete `prompt`. Parallel = multiple calls with `background: true`. Only agents with `mode: subagent`/`all`. Permission: `subagent` with resource = agent ID. |
| load a skill | `skill` tool with the exact case-sensitive ID. Permission: `skill` with resource = skill ID. |
| ask the user | `question` tool (header, question, options; free-form always available). Permission: `question` resource `*`. Requires interactive client. |
| explore files | `glob` (paths), `grep` (contents), `read` (file/dir page). |
| edit files | `edit` for focused replacement, `write` to create/replace whole file, `patch` for multi-file (mostly GPT models). |
| run commands | `shell` with `workdir`; `timeout` in ms for long runs; `background: true` for servers. |
| web | `webfetch` (one URL), `websearch` (query). |
| parallel tool calls | `execute` (Code Mode) to combine catalog calls without flooding context. |
| panels / model diversity | per-agent `model: provider/model#variant` (see `models`). Subagent uses its configured model, else inherits the parent session model. One agent per panel member. Upstream role lines (`model: the <role> line, default <slug>`) map to this: set each role's model in OpenCode config; `auto`/`inherit-parent` = omit `model`. Upstream default slugs are kept verbatim in the skills as reference data, not as working config. |
| slash commands | `.opencode/commands/*.md`; `$ARGUMENTS`, `$1..$n`, `!`code`` shell blocks. Body = prompt template. |

Paths inside a skill are relative to its `SKILL.md` directory. Supporting files are not auto-loaded; read them when the skill says so.
