# Host contract (capability verbs)

Skills in this repo never name host tools. They use these verbs; the lead resolves each through the adapter for the active host (`opencode.md`, `claude-code.md`, `codex.md`) **before** delegating.

| Verb | Meaning |
| --- | --- |
| spawn a `<agent>` subagent | run the named agent in a child session with a complete brief; report back evidence |
| spawn N subagents in one message / in parallel | fan out; background when the host supports it |
| in the background | don't block the lead; notify on completion |
| read-only / with full tools | child session with restricted / full capabilities |
| ask the user | pause and ask; free-form answer always allowed; only for calls no experiment can settle |
| load skill `<id>` | read that skill's full instructions into this run |
| role model (`<role>` line, default `<slug>`) | model configured for that role; `auto`/`inherit-parent` = run on the parent session model |
| `<host-skills>` | the active host's project skills directory (OpenCode `.opencode/skills/`, Claude Code `.claude/skills/`, Codex `.agents/skills/`) |
| `<host-session-store>` | where the host keeps session history on disk, if anywhere (Cursor: transcript files; other hosts: conversation history plus decision trails — never another project's sessions) |

## Fallbacks (all hosts)

- No subagent mechanism, or spawning denied: the lead executes inline and states the limitation. Parallelism collapses to sequential steps.
- No user-prompt mechanism (non-interactive run): decide reversible calls under the autonomy grant, record defaults for operator-only calls with the one word that reverses each.
- No per-role model control: everything runs on the session model; panels give independent passes, not model diversity. Say so when asked.
- The lead always owns synthesis, final patch judgment, and verification on the narrowest meaningful real surface.
