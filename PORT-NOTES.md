# PORT-NOTES

How this repo relates to upstream, and every deliberate deviation. Nothing here is invented: skill bodies are upstream's, translated mechanically by `scripts/adapt-upstream.py` (re-runnable). Host mappings cite official docs only (OpenCode V2 docs; Claude Code `skills` docs; Codex `skills`/plugin docs).

- Upstream: `cursor/plugins`, path `pstack/`, pinned in `UPSTREAM_COMMIT` (`fae2c6ed9582`). Upstream has 47 skills.
- Ported (45 skills): `poteto-mode`, `how`, `why`, `architect`, `arena`, `swarm`, `tdd`, `interrogate`, `blast-radius`, `unslop`, `no-comments`, `technical-writing`, `show-me-your-work`, `figure-it-out`, `create-verification-skill`, `maintain-verification-skill`, `typescript-best-practices`, `setup-models`, `reflect`, `recall`, `teach`, `bro` + all 23 `principle-*` leaf skills (kept as skills, like upstream). `setup-models` is original to this repo.
- Ported alongside: all 23 `poteto-mode` playbooks, `poteto-mode/references/bugbot-triage.md`, per-skill `references/` trees, agents `poteto-agent` + `comment-sicko`.
- `arena` + `swarm` are included (not deferred): `architect` Phase B runs the **arena** skill, and `poteto-mode`/autopilot fan-out routes through **swarm**.
- This repo self-registers its skills for OpenCode via `opencode.jsonc` (`skills: ["./skills"]`) instead of a committed `.opencode/skills` mirror: one source of truth, no duplication to drift. Distribution to other projects is `npx skills add` or the host manifests.

## Host-neutral design

- Canonical frontmatter is open-standard only: `name` (== directory id) + `description`. No `user-invocable`, `disable-model-invocation`, `context`, `allowed-tools`, or other host keys (CI enforced).
- Bodies use capability verbs (`spawn a … subagent`, `ask the user`, `role-model configuration`) resolved via `skills/poteto-mode/references/hosts/` (`_contract.md` + one adapter per host). The contract also defines fallbacks: no subagents → lead runs inline and says so; no per-role models → one session model, panels give independent passes, not diversity.
- Known adapter gaps (stated in the adapters, not papered over): Codex docs name no subagent/user-prompt tool → native mechanism or inline fallback; Codex role-model control is advisory via Codex config; `poteto-mode/scripts/` omitted (Cursor-oriented).

## Mechanical translations (`BODY_RULES` in the script)

| Upstream (Cursor) | This repo (neutral verb → host adapter) |
| --- | --- |
| `` `Task` `` / `Task tool` / `Task schema` / `Task subagent` | subagent / subagent mechanism / subagent call format (see `skills/poteto-mode/references/hosts/`) |
| `` `subagent_type: "X"` `` | spawn a `X` subagent (see hosts) |
| `` `subagent_type`: `generalPurpose` `` | spawn a general-purpose subagent (see hosts) |
| `` `AskQuestion` `` / `AskUserQuestion` | ask the user (see hosts) |
| `` `run_in_background: true` `` | in the background (see hosts) |
| `` `readonly`: `true`/`false` `` | read-only / with full tools (see hosts) |
| `` `/setup-pstack` ``, `` `pstack-models.mdc` `` | role-model configuration (see `skills/poteto-mode/references/hosts/`) |
| `` `.cursor/skills/<path>` `` | `` `<host-skills>/<path>` `` + per-host legend (OpenCode `.opencode/skills/`, Claude Code `.claude/skills/`, Codex `.agents/skills/`; `<host-skills>` defined in `hosts/_contract.md`) |
| Cursor path schemes (transcript store, slug scheme) | `` `<host-session-store>` `` (+ contract row); the slug-scheme clause is dropped as inapplicable |
| `is_background: true` (agent) | `mode: subagent` (OpenCode host package only) |
| frontmatter `name: Poteto Mode` etc. | `name:` := directory id (lowercase kebab, required for portable installs) |
| frontmatter `disable-model-invocation`, `mode`, `icon`, `color`, `reminder` | dropped (Cursor-only; canonical frontmatter is open-standard only) |

## Known limits (per-file notes point here)

- No Cursor transcript store, no Cursor cloud agents, no `cursor-team-kit` (`deslop`, `control-ui`, `control-cli`), no `orch` CLI. Each file resolves these through its host adapter; fallbacks in `hosts/_contract.md`. `gh` is the forge CLI.
- `poteto-mode/scripts/` omitted (`bootstrap.ts`, `check-plan.mjs`, `orch`, `watch-pr`, `worktree-audit.sh`): Cursor-oriented. Revisit if a playbook needs one.
- Two transcript passages kept verbatim + allowlisted in `check.py`: `playbooks/eval.md` (chain verification) and `playbooks/session-pickup.md` (prior-trail location). They degrade per the limits note.
- `why/references/synthesizer-prompt.md` keeps upstream's literal `(url)` template placeholder (allowlisted).
- Model slugs kept verbatim as upstream defaults. Map each role per the host adapter (OpenCode: `provider/model#variant`; Claude Code: `model`/`effort`; Codex: advisory). `auto`/`inherit-parent` = run on the parent session model.

## Sync policy

- Upstream = `cursor/plugins`, path `pstack/`, at the commit pinned in `UPSTREAM_COMMIT`.
- Import only: `skills/**` (in scope), `agents/**`, `docs/guide/**`. Never Cursor manifests, transcript paths, cloud-agent workflows, Graphite tooling, or `poteto-mode/scripts/`.
- `scripts/adapt-upstream.py` applies `substitution-table.md` mechanically, then semantic review: capability verbs must describe the real job. It writes only upstream-owned paths and deletes orphans; repo-owned paths (`hosts/`, `substitution-table.md`) are never touched.
- Record the new commit in `UPSTREAM_COMMIT`, run the gate, keep one shared `skills/` tree.

## Not yet ported (phase 2)

`automate-me`, `setup-pstack`, `make-bot-ui`. Router text may name them; treat as unavailable until ported.
