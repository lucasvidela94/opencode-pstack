#!/usr/bin/env bash
# Install the OpenCode host package (agents + commands).
# Skills travel via `npx skills add` (see README).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

DEST="$PWD/.opencode"
SCOPE="this project"
if [ "${1:-}" = "--global" ]; then
  DEST="$HOME/.config/opencode"
  SCOPE="your user config"
fi

mkdir -p "$DEST/agents" "$DEST/commands"
cp "$ROOT/.opencode/agents/"*.md "$DEST/agents/"
cp "$ROOT/.opencode/commands/"*.md "$DEST/commands/"
echo "installed agents+commands for $SCOPE -> $DEST"
