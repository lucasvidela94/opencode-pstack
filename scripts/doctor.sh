#!/usr/bin/env bash
# doctor: read-only health report of a pstack install. Changes nothing.
# Exit 0 when poteto-mode resolves on at least one host, 1 otherwise.
ok=0
hit()  { printf 'FOUND  : %s\n' "$*"; ok=1; }
miss() { printf 'MISSING: %s\n' "$*"; }
info() { printf 'INFO   : %s\n' "$*"; }

for d in "$HOME/.agents/skills/poteto-mode" \
         "$HOME/.config/opencode/skills/poteto-mode" \
         "$HOME/.claude/skills/poteto-mode" \
         "$HOME/.codex/skills/poteto-mode"; do
  if [ -f "$d/SKILL.md" ]; then hit "skill poteto-mode in $d"; else miss "skill poteto-mode in $d"; fi
done

for d in "$HOME/.config/opencode/agents" "$PWD/.opencode/agents"; do
  if [ -f "$d/poteto-agent.md" ]; then
    if [ "$d" = "$PWD/.opencode/agents" ]; then info "agent poteto-agent in $d (current project)"; else hit "agent poteto-agent in $d"; fi
  else
    miss "agent poteto-agent in $d"
  fi
done

if [ "$ok" = "1" ]; then echo "doctor: poteto-mode resolves somewhere"; else echo "doctor: nothing installed (see README)"; fi
exit $((1 - ok))
