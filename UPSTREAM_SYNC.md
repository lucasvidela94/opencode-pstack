# Upstream sync policy

- Upstream = `cursor/plugins`, path `pstack/`, at the commit pinned in `UPSTREAM_COMMIT`.
- Import only: `skills/**`, `agents/**` (docs), `docs/guide/**`. Never Cursor manifests, transcript paths, cloud-agent workflows, Graphite tooling.
- Adapt mechanically with `skills/poteto-mode/references/substitution-table.md`, then semantic review: capability verbs must describe the real job.
- Record the new commit in `UPSTREAM_COMMIT`, run `bash scripts/check.sh`, keep one shared `skills/` tree.
