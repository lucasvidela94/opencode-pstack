# Host adapter: Codex

Source: Codex docs (`skills`, skill-creator). Follows the open standard (`name` + `description` required).

- **Invoke skill**: `$skill-name` mention (CLI/IDE: `/skills` or `$`), or implicit via `description` match. `agents/openai.yaml` holds UI metadata (`display_name`, `short_description`, `default_prompt`); `allow_implicit_invocation: false` = explicit-only (this repo keeps the default `true`).
- **Spawn subagent**: the docs name no Codex subagent tool, so resolve delegation through Codex's native mechanism at run time. If spawning is unavailable or denied, collapse to the lead inline per `hosts/_contract.md` and state it. (Upstream `environment: "cloud"` / `run_in_background` have no Codex equivalent in the skill format.)
- **Ask the user**: no named prompt tool in the skill docs; ask in-conversation, or run non-interactive per the contract fallbacks.
- **Role models**: not controlled from skills; upstream role slugs are advisory here. Configure models in Codex config; panels give independent passes unless Codex offers per-agent models.
- **Skills discovery**: `.agents/skills` from cwd up to repo root, plus `$CODEX_HOME/skills` (`~/.codex/skills` default). Disable one via `[[skills.config]]` in `~/.codex/config.toml`.
- **Install**: `npx skills add <repo> --skill '*' --agent codex [--global]`, or package as plugin (`plugin.json` + `.codex-plugin/` compat, marketplaces via `codex plugin marketplace add`).
- **Routing**: `AGENTS.md`.
