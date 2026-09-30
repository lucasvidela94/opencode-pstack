# opencode-pstack

Host-neutral adaptation of [Cursor pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (poteto) for **OpenCode, Claude Code, and Codex**. Rigorous, small, verifiable engineering workflows as Agent Skills.

One canonical `skills/` tree (open standard frontmatter: `name` + `description` only). Skills speak capability verbs; each host resolves them through an adapter in `skills/poteto-mode/references/hosts/`.

## Install (via `npx skills`)

```bash
# OpenCode (global)
npx -y skills@latest add <tu-usuario>/opencode-pstack --skill '*' --agent opencode --global --yes
# Claude Code
npx -y skills@latest add <tu-usuario>/opencode-pstack --skill '*' --agent claude-code --global --yes
# Codex
npx -y skills@latest add <tu-usuario>/opencode-pstack --skill '*' --agent codex --global --yes
```

Verified with the `skills` CLI: it discovers all 37 skills and installs byte-identical copies to `~/.agents/skills` (OpenCode, Codex) and `~/.claude/skills` (Claude Code). If your Codex build doesn't pick up `~/.agents/skills`, copy the skills to `~/.codex/skills` (`$CODEX_HOME/skills`), which Codex always scans.

OpenCode also needs its agents/commands (the `skills` CLI only installs skills):

```bash
./scripts/setup-opencode.sh --global   # or --project
```

Claude Code plugin alternative: `/plugin marketplace add <tu-usuario>/opencode-pstack`, then install from the marketplace (see `.claude-plugin/`). Codex plugin alternative: manifests in `.codex-plugin/` + `plugin.json`.

Restart/reload the agent so it rescans skills.

## Use

Ask for the router skill by name for non-trivial work:

```text
Use the poteto-mode skill. <goal + how you will check it>
```

(`$poteto-mode` on Codex, `/poteto-mode` on Claude Code.) Casual turns: just talk normally, no skill needed. The repo's own routing line lives in `AGENTS.md`; Claude Code users add the same line to `CLAUDE.md`:

```text
Non-trivial engineering work: use the `poteto-mode` skill. Casual turns: don't.
```

## What is included

37 skills: `poteto-mode`, `how`, `why`, `architect`, `arena`, `swarm`, `tdd`, `interrogate`, `blast-radius`, `unslop`, `no-comments`, `technical-writing`, `show-me-your-work`, `typescript-best-practices` + the 23 upstream `principle-*` leaf skills (kept as skills: the router names them, the agent reads the leaf `SKILL.md` before applying one). `show-me-your-work` ships its portable `scripts/log.sh` helper verbatim.

23 playbooks under `skills/poteto-mode/playbooks/`. Agents `poteto-agent` + `comment-sicko` (OpenCode: `.opencode/agents/`; other hosts: resolve via the host adapter).

## Layout

```text
skills/<name>/SKILL.md        # canonical, host-neutral, npx-installable
skills/poteto-mode/playbooks/ # 23 playbooks
skills/poteto-mode/references/# substitution-table.md, bugbot-triage.md, hosts/
skills/poteto-mode/references/hosts/  # _contract.md, opencode.md, claude-code.md, codex.md
.opencode/agents|commands/    # OpenCode host package
.claude-plugin/               # Claude Code plugin + marketplace manifests
.codex-plugin/plugin.json     # Codex compat manifest (+ portable plugin.json)
opencode.jsonc                # self-registers ./skills (no committed mirror)
scripts/                      # adapt-upstream.py, check.py, setup-opencode.sh
```

## Sync upstream

`UPSTREAM_COMMIT` pins the reviewed `cursor/plugins` revision. Re-run `python3 scripts/adapt-upstream.py`, review the diff, run the gate. Policy and deviations in `PORT-NOTES.md`.

## Verify

```bash
python3 scripts/check.py
```

Gate: frontmatter (`name` == directory, `description` present, no host-specific keys), relative links resolve, no usable Cursor-only tokens, manifests are valid JSON.

## License

MIT. Original pstack work by Lauren Tan; see `LICENSE` and `PORT-NOTES.md` for attribution.
