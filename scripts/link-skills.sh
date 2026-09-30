#!/usr/bin/env bash
# Link this repo's skills into the local harness skill dirs (symlinks, so a
# `git pull` keeps installed skills current). Re-run after adding skills.
# Alternative to `npx skills add` (which copies). Idempotent.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

link_all() {
  local dest="$1"
  mkdir -p "$dest"
  for d in "$ROOT"/skills/*/; do
    local name
    name="$(basename "$d")"
    ln -sfn "$d" "$dest/$name"
  done
  echo "linked $(ls "$ROOT/skills" | wc -l) skills -> $dest"
}

link_all "$HOME/.agents/skills"   # OpenCode (compat) + Codex
link_all "$HOME/.claude/skills"   # Claude Code
