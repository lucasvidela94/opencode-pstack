# PORT-NOTES

How this repo relates to upstream, and every deliberate deviation. Nothing here is invented: skill bodies are upstream's, translated mechanically by `scripts/adapt-upstream.py` (re-runnable). Host mappings cite official docs only (OpenCode V2 docs; Claude Code `skills` docs; Codex `skills`/plugin docs).

- Upstream: `cursor/plugins`, path `pstack/`, pinned in `UPSTREAM_COMMIT` (`fae2c6ed9582`). Upstream has 47 skills.
- Ported (35 skills): `poteto-mode`, `how`, `why`, `architect`, `arena`, `swarm`, `tdd`, `interrogate`, `blast-radius`, `unslop`, `no-comments`, `typescript-best-practices` + all 23 `principle-*` leaf skills (kept as skills, like upstream).
- Ported alongside: all 23 `poteto-mode` playbooks, `poteto-mode/references/bugbot-triage.md`, per-skill `references/` trees, agents `poteto-agent` + `comment-sicko`.
- `arena` + `swarm` are included (not deferred): `architect` Phase B runs the **arena** skill, and `poteto-mode`/autopilot fan-out routes through **swarm**.

## Host-neutral design

- Canonical frontmatter is open-standard only: `name` (== directory id) + `description`. No `user-invocable`, `disable-model-invocation`, `context`, `allowed-tools`, or other host keys (CI enforced).
- Bodies use capability verbs (`spawn a … subagent`, `ask the user`, `role-model configuration`) resolved via `skills/poteto-mode/references/hosts/` (`_contract.md` + one adapter per host). The contract also defines fallbacks: no subagents → lead runs inline and says so; no per-role models → one session model, panels give independent passes, not diversity.
- Known adapter gaps (stated in the adapters, not papered over): Codex docs name no subagent/user-prompt tool → native mechanism or inline fallback; Codex role-model control is advisory via Codex config; `poteto-mode/scripts/` omitted (Cursor-oriented).

## Mechanical translations (`BODY_RULES` in the script)

| Upstream (Cursor) | This repo (OpenCode) |
| --- | --- |
| `` `Task` `` / `Task tool` / `Task schema` / `Task subagent` | `` `subagent` `` tool |
| `` `subagent_type: "X"` `` | `` `subagent X (OpenCode subagent tool)` `` |
| `` `subagent_type`: `generalPurpose` `` | `` `subagent general (OpenCode subagent tool)` `` |
| `` `AskQuestion` `` / `AskUserQuestion` | `` `question` `` tool |
| `` `run_in_background: true` `` | `` `background: true` `` |
| `` `readonly`: `true`/`false` `` | `` `permissions` `` read-only / full tools |
| `` `/setup-pstack` ``, `` `pstack-models.mdc` `` | model configuration (`references/opencode-tools.md`) |
| `is_background: true` (agent) | `mode: subagent` |
| frontmatter `name: Poteto Mode` etc. | `name:` := directory id (lowercase kebab, required for portable installs) |
| frontmatter `disable-model-invocation`, `mode`, `icon`, `color`, `reminder` | dropped (Cursor-only). Hiding, when needed, is `slash: false` + `metadata.opencode/autoinvoke: false` |

## Known limits (per-file notes point here)

- No Cursor transcript store, no Cursor cloud agents (use `background: true` subagents on this machine), no `cursor-team-kit` (`deslop`, `control-ui`, `control-cli` — use native tools), no `orch` CLI (plain `ledger.tsv` via `shell`), `gh` is the forge CLI.
- `poteto-mode/scripts/` omitted (`bootstrap.ts`, `check-plan.mjs`, `orch`, `watch-pr`, `worktree-audit.sh`): Cursor-oriented. Revisit if a playbook needs one.
- Two transcript passages kept verbatim + allowlisted in `check.sh`: `playbooks/eval.md` (chain verification) and `playbooks/session-pickup.md` (prior-trail location). They degrade per the limits note.
- `why/references/synthesizer-prompt.md` keeps upstream's literal `(url)` template placeholder (allowlisted).
- Model slugs (`claude-opus-5-5`, `gpt-5.6-sol`, `grok-4.7-xhigh`, `*-max`) kept verbatim as upstream defaults. Map each role to a real `provider/model#variant` in your OpenCode config; a role set to `auto`/`inherit-parent` runs on the parent session model (omit `model`).

## Not yet ported (phase 2)

`reflect`, `figure-it-out`, `show-me-your-work`, `recall`, `teach`, `technical-writing`, `create-verification-skill`, `maintain-verification-skill`, `bro`, `automate-me`, `setup-pstack`, `make-bot-ui`. Router text may name them; treat as unavailable until ported.
