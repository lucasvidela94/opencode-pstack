# Changelog

Brief, per shipped change. Upstream content versions live in `UPSTREAM_COMMIT`.

## Unreleased

- `reflect`, `recall`, `teach`, `bro`: router now cites only ported skills.
- `<host-skills>` / `<host-session-store>` conventions for Cursor path schemes.
- `setup-models`: original skill mapping pstack roles to host models.
- `scripts/link-skills.sh`: symlink installs for contributors.
- `CLAUDE.md` restored as pointer to `AGENTS.md`.
- README: problem framing + per-skill links.

## 2026-09-30 — host-neutral + phase 2

- 41 skills: 18 workflow (`poteto-mode`, `how`, `why`, `architect`, `arena`,
  `swarm`, `tdd`, `interrogate`, `blast-radius`, `unslop`, `no-comments`,
  `technical-writing`, `show-me-your-work`, `figure-it-out`,
  `create-verification-skill`, `maintain-verification-skill`,
  `typescript-best-practices`, `setup-models`) + 23 `principle-*`.
- Host-neutral core with `hosts/` adapters (OpenCode, Claude Code, Codex).
- `setup-models` is original to this repo (role-model configuration per host).
- `docs/guide/` with three real task examples.
- Upstream pin `2eb7ed4` (pstack untouched since `fae2c6e`).

## 2026-09-30 — initial port

- 35 skills + 23 playbooks + 2 agents from `cursor/plugins` pstack@`fae2c6e`.
- Mechanical port script + CI gate + plugin manifests.
