#!/usr/bin/env python3
"""Port cursor/plugins pstack content to this repo for OpenCode.

Mechanical translations only (see substitution-table.md + PORT-NOTES.md).
Re-run after bumping UPSTREAM_COMMIT's pinned revision, then review the diff.

Usage: python3 scripts/adapt-upstream.py
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path("/tmp/opencode/plugins/pstack")
COMMIT = "fae2c6ed95821bd85f614a73e4842e13229fa5e5"

CORE_SKILLS = [
    "poteto-mode", "how", "why", "architect", "arena", "swarm", "tdd",
    "interrogate", "blast-radius", "unslop", "no-comments",
    "typescript-best-practices",
]
# principle-* discovered dynamically (23 upstream).
DROP_FRONTMATTER_KEYS = {
    "disable-model-invocation", "mode", "icon", "color", "reminder",
}

HEADER = (
    "> Adapted from `cursor/plugins` pstack@{commit} for OpenCode. "
    "Mechanical translations only, no content invented; see `PORT-NOTES.md`.\n\n"
).format(commit=COMMIT[:12])

# Playbooks/skills that lean on Cursor-only runtime get an extra limits note.
LIMITS_NOTE = (
    "> OpenCode limits for this file: no Cursor transcript store "
    "(`agent-transcripts/`, `~/.cursor/projects/`), no Cursor cloud agents "
    "(use OpenCode `background: true` subagents on this machine), no "
    "`cursor-team-kit` skills (`deslop`, `control-ui`, `control-cli` — use "
    "native `read`/`edit`/`shell`/browser instead), no `orch` CLI (keep a "
    "plain `ledger.tsv` via `shell`). `gh` is the forge CLI; Graphite (`gt`) "
    "is never required.\n\n"
)
LIMITS_FILES = {
    "skills/poteto-mode/playbooks/session-pickup.md",
    "skills/poteto-mode/playbooks/autopilot-full.md",
    "skills/poteto-mode/playbooks/autopilot-stack.md",
    "skills/poteto-mode/playbooks/orchestrate.md",
    "skills/poteto-mode/playbooks/shipping.md",
    "skills/poteto-mode/playbooks/eval.md",
    "skills/poteto-mode/playbooks/worktree-cleanup.md",
    "skills/poteto-mode/playbooks/babysit.md",
    "skills/poteto-mode/playbooks/multi-phase-plan.md",
    "skills/poteto-mode/playbooks/opening-a-pr.md",
    "skills/poteto-mode/SKILL.md",
    "skills/arena/SKILL.md",
    "skills/swarm/SKILL.md",
}

BODY_RULES = [
    # About to `AskQuestion` on a ... fork -> About to ask the user ...
    (re.compile(r"About to `AskQuestion`"), "About to ask the user (the `question` tool)"),
    (re.compile(r"`?subagent_type:\s*\"([^\"]+)\"`?"), r"`subagent \1 (OpenCode subagent tool)`"),
    (re.compile(r"`subagent_type: generalPurpose`"), "`subagent general (OpenCode subagent tool)`"),
    (re.compile(r"`subagent_type`:\s*`generalPurpose`"), "`subagent general (OpenCode subagent tool)`"),
    (re.compile(r"`subagent_type`"), "`subagent`"),
    (re.compile(r"Substituting `generalPurpose`"), "Substituting the `general` subagent"),
    (re.compile(r"`Task`"), "`subagent`"),
    (re.compile(r"\bTask subagent\b"), "subagent"),
    (re.compile(r"AskUserQuestion"), "`question`"),
    (re.compile(r"AskQuestion"), "`question`"),
    (re.compile(r"`run_in_background:\s*true`"), "`background: true`"),
    (re.compile(r"run_in_background:\s*true"), "background: `true`"),
    (re.compile(r"`readonly`:\s*`true`"), "`permissions`: read-only (deny `edit` and `shell`)"),
    (re.compile(r"`readonly`:\s*`false`"), "`permissions`: full tool access"),
    (re.compile(r"`/setup-pstack`"), "`model configuration` (references/opencode-tools.md)"),
    (re.compile(r"/setup-pstack"), "model configuration (references/opencode-tools.md)"),
    (re.compile(r"`~/.cursor/rules/pstack-models\.mdc`"), "`model configuration` (references/opencode-tools.md)"),
    (re.compile(r"pstack-models\.mdc"), "model configuration (references/opencode-tools.md)"),
    (re.compile(r"Task tool"), "`subagent` tool"),
    (re.compile(r"Task schema"), "`subagent` schema"),
    (re.compile(r"<Task as a verb phrase>"), "<subagent as a verb phrase>"),
]


def split_frontmatter(text):
    if text.startswith("---\n") or text.startswith("---\r\n"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[: end + 4], text[end + 4 :]
    return None, text


def adapt_frontmatter(fm, rel):
    """Rewrite frontmatter: name := directory/skill id, drop Cursor-only keys."""
    lines = fm.split("\n")
    out = [lines[0]]
    has_mode = False
    if rel.parts[0] == "skills":
        skill_id = rel.parts[1]
        # agents keep their own names; poteto-agent/comment-sicko already match files
    for line in lines[1:]:
        m = re.match(r"^([A-Za-z0-9_/\.-]+):", line)
        if m and m.group(1) in DROP_FRONTMATTER_KEYS:
            continue
        if re.match(r"^mode:", line):
            has_mode = True
        if rel.parts[0] == "skills" and re.match(r"^name:", line):
            line = f"name: {skill_id}"
        if rel.parts[0] == ".opencode" and re.match(r"^is_background:", line):
            line = "mode: subagent"
            has_mode = True
        line = line.replace("Substituting `generalPurpose`",
                            "Substituting the `general` subagent")
        out.append(line)
    text = "\n".join(out)
    if rel.parts[0] == ".opencode" and not has_mode:
        text = text.replace("\n---", "\nmode: subagent\n---", 1)
    return text


def adapt_body(body):
    for rx, repl in BODY_RULES:
        body = rx.sub(repl, body)
    return body


def adapt_file(src, dst, rel):
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text()
    fm, body = split_frontmatter(text)
    if fm is not None:
        fm = adapt_frontmatter(fm, rel)
        body = adapt_body(body)
        note = LIMITS_NOTE if rel.as_posix() in LIMITS_FILES else ""
        dst.write_text(fm + "\n\n" + HEADER + note + body.lstrip("\n"))
    else:
        body = adapt_body(text)
        note = LIMITS_NOTE if rel.as_posix() in LIMITS_FILES else ""
        dst.write_text(HEADER + note + body)


def main():
    if not SRC.exists():
        sys.exit(f"upstream checkout missing: {SRC}")
    principle_dirs = sorted(p.name for p in (SRC / "skills").iterdir()
                            if p.is_dir() and p.name.startswith("principle-"))
    skill_dirs = CORE_SKILLS + principle_dirs

    # our own host-mapping files live inside poteto-mode/references: preserve them
    keep = {}
    for ours in ["references/opencode-tools.md", "references/substitution-table.md"]:
        p = ROOT / "skills" / "poteto-mode" / ours
        if p.exists():
            keep[ours] = p.read_text()

    # clean previously generated skill trees (keep our own references/*.md)
    for name in skill_dirs:
        d = ROOT / "skills" / name
        if d.exists():
            shutil.rmtree(d)

    for name in skill_dirs:
        s = SRC / "skills" / name
        adapt_file(s / "SKILL.md", ROOT / "skills" / name / "SKILL.md",
                   Path("skills") / name / "SKILL.md")
        ref = s / "references"
        if ref.exists():
            for f in sorted(ref.rglob("*")):
                if f.is_file():
                    rel = Path("skills") / name / "references" / f.relative_to(ref)
                    (ROOT / rel.parent).mkdir(parents=True, exist_ok=True)
                    if f.suffix == ".md":
                        adapt_file(f, ROOT / rel, rel)
                    else:
                        shutil.copy2(f, ROOT / rel)

    # poteto-mode playbooks + references (scripts/ intentionally omitted)
    pm, dst_pm = SRC / "skills" / "poteto-mode", ROOT / "skills" / "poteto-mode"
    for pb in sorted((pm / "playbooks").glob("*.md")):
        rel = Path("skills/poteto-mode/playbooks") / pb.name
        adapt_file(pb, dst_pm / "playbooks" / pb.name, rel)
    for f in sorted((pm / "references").glob("*.md")):
        rel = Path("skills/poteto-mode/references") / f.name
        if (dst_pm / "references" / f.name).exists():
            continue  # keep our opencode-tools.md / substitution-table.md
        adapt_file(f, dst_pm / "references" / f.name, rel)

    for ours, text in keep.items():
        p = ROOT / "skills" / "poteto-mode" / ours
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)

    # agents
    for a in ["poteto-agent.md", "comment-sicko.md"]:
        adapt_file(SRC / "agents" / a, ROOT / ".opencode" / "agents" / a,
                   Path(".opencode/agents") / a)

    (ROOT / "UPSTREAM_COMMIT").write_text(COMMIT + "\n")
    print(f"ported {len(skill_dirs)} skills + playbooks + 2 agents @ {COMMIT[:12]}")


if __name__ == "__main__":
    main()
