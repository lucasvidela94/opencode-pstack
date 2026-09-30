#!/usr/bin/env bash
# Release gate: frontmatter, links, name==directory, no Cursor-only tokens.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAIL_FILE="$(mktemp)"
fail() { printf 'FAIL: %s\n' "$*" | tee -a "$FAIL_FILE"; }

for d in "$ROOT"/skills/*/; do
  [ -f "$d/SKILL.md" ] || { fail "missing SKILL.md in $d"; continue; }
  name="$(basename "$d")"
  fm_name="$(sed -n '/^---$/,/^---$/p' "$d/SKILL.md" | grep -E '^name:' | head -1 | sed 's/^name:[[:space:]]*//')"
  desc="$(sed -n '/^---$/,/^---$/p' "$d/SKILL.md" | grep -E '^description:' | head -1 | sed 's/^description:[[:space:]]*//')"
  [ "$fm_name" = "$name" ] || fail "skills/$name: frontmatter name '$fm_name' != directory '$name'"
  [ -n "$desc" ] || fail "skills/$name: empty description (undiscoverable)"
  echo "$name" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$' || fail "skills/$name: id not kebab-case"
done

# relative links resolve (allowlist: upstream-verbatim template placeholder + documented deferrals)
while IFS= read -r f; do
  dir="$(dirname "$f")"
  { grep -Eo '\]\([^)]+\)' "$f" || true; } | sed 's/^](//;s/)$//' | while IFS= read -r link; do
    case "$link" in
      http*|https*|mailto:*|"#"*) continue;;
      "url") continue;; # upstream-verbatim template placeholder, see PORT-NOTES.md
    esac
    link="${link%%#*}"
    [ -e "$dir/$link" ] || fail "broken link in ${f#$ROOT/}: $link"
  done
done < <(find "$ROOT/skills" -name '*.md')

# Cursor-only tokens: blockquote port-notes may name them to disclaim them;
# mapping docs (hosts/, substitution-table) name them by design;
# two upstream-verbatim transcript passages are allowlisted (see PORT-NOTES.md).
grep -rnE 'subagent_type|AskUserQuestion|disable-model-invocation|\.cursor-plugin|is_background|/setup-pstack|generalPurpose|`Task`|Task subagent|`readonly`|pstack-models|Task tool|Task schema|~/.cursor|<Task|user-invocable|context: fork' \
  "$ROOT/skills" "$ROOT/.opencode" "$ROOT/.claude-plugin" "$ROOT/.codex-plugin" 2>/dev/null \
  | grep -v '^[^:]*:[0-9]*:>' \
  | grep -v 'poteto-mode/references/hosts/' \
  | grep -v 'poteto-mode/references/substitution-table.md' \
  | grep -v 'playbooks/eval.md:.*agent-transcripts' \
  | grep -v 'playbooks/session-pickup.md:.*agent-transcripts' \
  | while IFS= read -r line; do fail "Cursor-only residue: $line"; done || true

# agents shape
for a in "$ROOT"/.opencode/agents/*.md; do
  grep -qE '^mode:' "$a" || fail "agent ${a#$ROOT/} missing mode:"
done

# canonical frontmatter stays host-neutral (open standard only: name + description)
while IFS= read -r f; do
  if sed -n '/^---$/,/^---$/p' "$f" | head -20 | grep -qE '^(user-invocable|disable-model-invocation|context|allowed-tools|disallowed-tools|effort|argument-hint|arguments|model):'; then
    fail "host-specific frontmatter in ${f#$ROOT/}"
  fi
done < <(find "$ROOT/skills" -name 'SKILL.md')

# manifests are valid JSON
for m in "$ROOT"/.claude-plugin/plugin.json "$ROOT"/.claude-plugin/marketplace.json "$ROOT"/.codex-plugin/plugin.json; do
  python3 -m json.tool "$m" >/dev/null 2>&1 || fail "invalid JSON: ${m#$ROOT/}"
done

# .opencode/skills mirror stays identical to canonical skills/
if [ ! -d "$ROOT/.opencode/skills" ]; then
  fail "missing .opencode/skills mirror (run scripts/adapt-upstream.py)"
elif ! diff -r -q "$ROOT/skills" "$ROOT/.opencode/skills" >/dev/null 2>&1; then
  fail ".opencode/skills mirror out of sync (run scripts/adapt-upstream.py)"
  diff -r -q "$ROOT/skills" "$ROOT/.opencode/skills" 2>&1 | head -5 | while IFS= read -r line; do fail "mirror: $line"; done || true
fi

if [ -s "$FAIL_FILE" ]; then
  printf 'GATE FAILED\n'; rm -f "$FAIL_FILE"; exit 1
fi
rm -f "$FAIL_FILE"
echo "PASS: check.sh"
