#!/usr/bin/env bash
# Install .opencode agents/commands (the `skills` CLI only installs skills/).
set -euo pipefail
MODE="--project"
[ "${1:-}" = "--global" ] && MODE="--global"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ "$MODE" = "--global" ]; then
  DEST="$HOME/.config/opencode"
else
  DEST="$PWD/.opencode"
fi
mkdir -p "$DEST/agents" "$DEST/commands"
cp -R "$ROOT/.opencode/agents/." "$DEST/agents/"
cp -R "$ROOT/.opencode/commands/." "$DEST/commands/"
printf 'installed agents+commands -> %s\n' "$DEST"
printf 'skills: npx -y skills@latest add <tu-usuario>/opencode-pstack --skill %s --agent opencode %s --yes\n' "'*'" "$([ "$MODE" = "--global" ] && echo --global || echo "")"
