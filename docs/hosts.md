# Host capability matrix

What each skill group does per host. `full` = as upstream designed.
`degraded` = works with a stated fallback (see `skills/poteto-mode/references/hosts/`).
Install rows describe the recommended path.

| Group | OpenCode | Claude Code | Codex |
| --- | --- | --- | --- |
| router + 23 playbooks | full | full | full |
| workflow skills (`how`, `why`, `tdd`, `architect`, …) | full | full | full |
| panels (`arena`, `swarm`, `interrogate`) | full (per-agent `model`) | full (skill/agent `model`) | degraded: independent passes, model control is advisory |
| principles (23) | full | full | full |
| verification skills | full (generate into `<host-skills>`) | full | full |
| `reflect`, `recall` | degraded: session history + trails instead of transcript files | degraded: same | degraded: same |
| `setup-models` | full (writes `opencode.jsonc` values) | full (skill/agent `model`, `/model`) | degraded: advisory, via Codex config |
| agents (`poteto-agent`, `comment-sicko`) | native (`.opencode/agents`) | `.claude/agents` + `Task subagent_type` | via plugin manifests |
| commands (`/poteto-mode`) | native (`.opencode/commands`) | merged into skills (`/poteto-mode` skill) | `$poteto-mode` skill mention |
| install | `npx skills add` + `setup-opencode.sh` | `npx skills add` or plugin marketplace | `npx skills add` or plugin marketplace |
| uninstall | delete the installed files; nothing else was touched | same | same |
