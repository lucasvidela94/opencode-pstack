# opencode-pstack

Portable adaptation of [Cursor pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (poteto) for OpenCode. Rigorous, small, verifiable engineering workflows as Agent Skills.

## Install (normal way, via `npx skills`)

```bash
# global
npx -y skills@latest add <tu-usuario>/opencode-pstack --skill '*' --agent opencode --global --yes

# or project-local
npx -y skills@latest add <tu-usuario>/opencode-pstack --skill '*' --agent opencode --yes
```

Then install the OpenCode agents/commands (the `skills` CLI only installs skills):

```bash
./scripts/setup-opencode.sh --global   # or --project
```

Restart/reload OpenCode so it rescans skills.

## Use

Ask for the router skill by name for non-trivial work:

```text
Use the poteto-mode skill. <goal + how you will check it>
```

Casual turns: just talk normally, no skill needed (see `AGENTS.md`).

## What is included

Core only (on purpose). `arena`/`swarm` (token-heavy panels) come later.

| Skill | Use when |
| --- | --- |
| `poteto-mode` | router: non-trivial coding, investigation, review, migration, verification |
| `how` | explain how part of the system works |
| `why` | evidence for why it was built that way |
| `architect` | design must be settled before code (runs **arena** in Phase B) |
| `arena` | N parallel candidates, pick a base, graft strengths, verify |
| `swarm` | parallel fan-out: coverage matrices, races, verification lanes |
| `tdd` | bug fix / feature with repro-first discipline |
| `interrogate` | adversarial review of a design or diff |
| `blast-radius` | what could this change break beyond the diff |
| `unslop` | de-slop prose/code, say less |
| `no-comments` | remove comment noise, keep only load-bearing ones |
| `typescript-best-practices` | TS/React rules for this stack |

Principles are the 23 upstream `principle-*` leaf skills, kept as skills (like upstream): `poteto-mode` names them, the agent reads the leaf `SKILL.md` in full before applying one. Host mapping lives in one file: `skills/poteto-mode/references/opencode-tools.md`. Deviations from upstream are logged in `PORT-NOTES.md`.

## Layout

```text
skills/<name>/SKILL.md        # canonical source, npx-installable (35: 12 workflow + 23 principle-*)
skills/poteto-mode/playbooks/ # 23 playbooks, copied verbatim from the matched router step
skills/poteto-mode/references/# opencode-tools.md, substitution-table.md, bugbot-triage.md
.opencode/agents/             # poteto-agent, comment-sicko (mode: subagent)
.opencode/commands/           # /poteto-mode
scripts/                      # adapt-upstream.py, check.sh, setup-opencode.sh
```

## Sync upstream

`UPSTREAM_COMMIT` pins the reviewed `cursor/plugins` revision. Procedure in `UPSTREAM_SYNC.md`. After any sync: `./scripts/sync-check` = `bash scripts/check.sh`.

## Verify

```bash
bash scripts/check.sh
```

Gate: frontmatter (`name` == directory, non-empty `description`), relative links resolve, no Cursor-only tokens, agents/commands shape.

## License

MIT. Original pstack work by Lauren Tan; see `LICENSE` and `UPSTREAM_SYNC.md` for attribution.
