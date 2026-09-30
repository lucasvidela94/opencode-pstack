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

# Back up anything we are about to replace. We add; we never silently destroy.
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP="$DEST/.backup-$STAMP"
backed_up=0
for f in "$ROOT/.opencode/agents/"*.md "$ROOT/.opencode/commands/"*.md; do
  dir="agents"
  case "$f" in
    */commands/*) dir="commands";;
  esac
  base="$(basename "$f")"
  if [ -e "$DEST/$dir/$base" ] && ! cmp -s "$f" "$DEST/$dir/$base"; then
    mkdir -p "$BACKUP/$dir"
    cp "$DEST/$dir/$base" "$BACKUP/$dir/"
    backed_up=1
  fi
done

cp "$ROOT/.opencode/agents/"*.md "$DEST/agents/"
cp "$ROOT/.opencode/commands/"*.md "$DEST/commands/"
echo "installed agents+commands for $SCOPE -> $DEST"
if [ "$backed_up" = "1" ]; then
  echo "replaced files backed up in $BACKUP (delete it when happy)"
fi
