#!/usr/bin/env python3
"""Release gate: frontmatter, links, name==directory, no usable Cursor-only
tokens, host-neutral canonical frontmatter, valid manifests. Exit 1 on failure.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures = []


def fail(msg):
    failures.append(msg)
    print(f"FAIL: {msg}")


# Upstream-verbatim passages that name Cursor concepts to disclaim or locate.
# Documented in PORT-NOTES.md; everything else must be clean.
ALLOWLIST_RESIDUE = [
    ("playbooks/eval.md", "agent-transcripts"),
    ("playbooks/session-pickup.md", "agent-transcripts"),
    ("skills/show-me-your-work/SKILL.md", "agent-transcripts"),
    ("skills/reflect/SKILL.md", "agent-transcripts"),
    ("skills/reflect/SKILL.md", "~/.cursor"),
    ("skills/recall/SKILL.md", "agent-transcripts"),
    ("skills/recall/SKILL.md", "~/.cursor"),
]
ALLOWLIST_LINK = {"url"}  # upstream-verbatim template placeholder (why/references)

RESIDUE = re.compile(
    r"subagent_type|AskUserQuestion|`AskQuestion`|disable-model-invocation"
    r"|\.cursor-plugin|is_background|/setup-pstack|generalPurpose|`Task`"
    r"|Task subagent|`readonly`|pstack-models|Task tool|Task schema|~/\.cursor|<Task"
    r"|user-invocable|context: fork"
)
HOST_KEYS = re.compile(
    r"^(user-invocable|disable-model-invocation|context|allowed-tools|"
    r"disallowed-tools|effort|argument-hint|arguments|model):"
)
LINK = re.compile(r"\]\(([^)]+)\)")


def frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[: end + 4]
    return ""


# 1. skill frontmatter
for skill_dir in sorted((ROOT / "skills").iterdir()):
    if not skill_dir.is_dir():
        continue
    name = skill_dir.name
    f = skill_dir / "SKILL.md"
    if not f.exists():
        fail(f"missing SKILL.md in skills/{name}")
        continue
    fm = frontmatter(f.read_text())
    m = re.search(r"^name:\s*(.+)$", fm, re.M)
    if not m or m.group(1).strip() != name:
        fail(f"skills/{name}: frontmatter name != directory")
    if not re.search(r"^description:\s*\S", fm, re.M):
        fail(f"skills/{name}: empty description (undiscoverable)")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        fail(f"skills/{name}: id not kebab-case")
    if HOST_KEYS.search(fm):
        fail(f"skills/{name}: host-specific frontmatter key")

# 2. relative links
for f in sorted((ROOT / "skills").rglob("*.md")):
    for link in LINK.findall(f.read_text()):
        if link.startswith(("http", "https", "mailto:", "#")):
            continue
        target = link.split("#")[0]
        if target in ALLOWLIST_LINK:
            continue
        if not (f.parent / target).exists():
            fail(f"broken link in {f.relative_to(ROOT)}: {link}")

# 3. Cursor-only residue (mapping docs exempt by design)
exempt_dirs = {"skills/poteto-mode/references/hosts"}
exempt_files = {"skills/poteto-mode/references/substitution-table.md"}
scan_roots = [ROOT / "skills", ROOT / ".opencode"]
for base in scan_roots:
    for f in sorted(base.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(ROOT).as_posix()
        if rel in exempt_files or any(rel.startswith(d) for d in exempt_dirs):
            continue
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if line.startswith(">"):
                continue  # port-note blockquotes may name concepts to disclaim
            if not RESIDUE.search(line):
                continue
            if any(a in rel and b in line for a, b in ALLOWLIST_RESIDUE):
                continue
            fail(f"Cursor-only residue {rel}:{i}: {line.strip()[:100]}")

# 4. agents shape
for a in sorted((ROOT / ".opencode" / "agents").glob("*.md")):
    if not re.search(r"^mode:", a.read_text(), re.M):
        fail(f"agent {a.relative_to(ROOT)} missing mode:")

# 5. manifests
for m in [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
          ".codex-plugin/plugin.json"]:
    try:
        json.loads((ROOT / m).read_text())
    except (OSError, ValueError):
        fail(f"invalid JSON: {m}")

if failures:
    print(f"GATE FAILED ({len(failures)})")
    sys.exit(1)
print("PASS: check.py")
