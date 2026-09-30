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
COMMIT = "2eb7ed4613cfc8f098dfe464a23680ea44d84c5e"

CORE_SKILLS = [
    "poteto-mode", "how", "why", "architect", "arena", "swarm", "tdd",
    "interrogate", "blast-radius", "unslop", "no-comments",
    "typescript-best-practices",
    # phase 2a: most-cited by the core (opening-a-pr, long/autonomous runs)
    "technical-writing", "show-me-your-work",
    # phase 2b: bespoke playbooks + project-local verification skills
    "figure-it-out", "create-verification-skill", "maintain-verification-skill",
]
# Skills whose scripts/ helpers are portable and referenced by the body.
# (poteto-mode/scripts stays omitted: Cursor-oriented tooling.)
SKILL_SCRIPTS = {"show-me-your-work"}
# principle-* discovered dynamically (23 upstream).
DROP_FRONTMATTER_KEYS = {
    "disable-model-invocation", "mode", "icon", "color", "reminder",
}

HEADER = (
    "> Adapted from `cursor/plugins` pstack@{commit}. Neutral host wording; "
    "no content invented. Resolve capability verbs via "
    "`skills/poteto-mode/references/hosts/`; deviations in `PORT-NOTES.md`.\n\n"
).format(commit=COMMIT[:12])

# Playbooks/skills that lean on Cursor-only runtime get an extra limits note.
LIMITS_NOTE = (
    "> Host limits for this file: it assumes Cursor transcripts "
    "(`agent-transcripts/`, `~/.cursor/projects/`), Cursor cloud agents, "
    "`cursor-team-kit` skills (`deslop`, `control-ui`, `control-cli`), or the "
    "`orch` CLI. Resolve each through the host adapter "
    "(`skills/poteto-mode/references/hosts/`); fallbacks in `hosts/_contract.md`. "
    "`gh` is the forge CLI; Graphite (`gt`) is never required.\n\n"
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
    "skills/show-me-your-work/SKILL.md",
}

HOSTS = "skills/poteto-mode/references/hosts/"

BODY_RULES = [
    # About to `AskQuestion` on a ... fork -> About to ask the user ...
    (re.compile(r"About to `AskQuestion`"), f"About to ask the user (see `{HOSTS}`)"),
    (re.compile(r"`?subagent_type:\s*\"([^\"]+)\"`?"), rf"spawn a `\1` subagent (see `{HOSTS}`)"),
    (re.compile(r"`subagent_type: generalPurpose`"), f"spawn a general-purpose subagent (see `{HOSTS}`)"),
    (re.compile(r"`subagent_type`:\s*`generalPurpose`"), f"spawn a general-purpose subagent (see `{HOSTS}`)"),
    (re.compile(r"`subagent_type`"), "subagent mechanism"),
    (re.compile(r"`Task`"), "subagent"),
    (re.compile(r"\bTask subagent\b"), "subagent"),
    (re.compile(r"AskUserQuestion"), "ask the user"),
    (re.compile(r"AskQuestion"), "ask the user"),
    (re.compile(r"`run_in_background:\s*true`"), "in the background"),
    (re.compile(r"run_in_background:\s*true"), "in the background"),
    (re.compile(r"`readonly`:\s*`true`"), "read-only"),
    (re.compile(r"`readonly`:\s*`false`"), "with full tools"),
    (re.compile(r"`/setup-pstack`"), f"`role-model configuration` (see `{HOSTS}`)"),
    (re.compile(r"/setup-pstack"), f"role-model configuration (see `{HOSTS}`)"),
    (re.compile(r"`~/.cursor/rules/pstack-models\.mdc`"), f"`role-model configuration` (see `{HOSTS}`)"),
    (re.compile(r"pstack-models\.mdc"), f"role-model configuration (see `{HOSTS}`)"),
    (re.compile(r"Task tool"), f"subagent mechanism (see `{HOSTS}`)"),
    (re.compile(r"Task schema"), f"subagent call format (see `{HOSTS}`)"),
    (re.compile(r"<Task as a verb phrase>"), "<subagent as a verb phrase>"),
    (re.compile(r"Substituting `generalPurpose`"), "Substituting another general-purpose subagent"),
    (re.compile(r"`?\.cursor/skills/([^\s`]+)`?"),
     r"`<host-skills>/\1` (OpenCode `.opencode/skills/`, Claude Code `.claude/skills/`, "
     r"Codex `.agents/skills/`; see `" + HOSTS + "`)"),
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
                            "Substituting another general-purpose subagent")
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
    WRITTEN.add(rel.as_posix())
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


# Repo-owned paths the sync never writes or deletes (our host-mapping docs).
OURS_EXACT = {"skills/poteto-mode/references/substitution-table.md"}
OURS_PREFIX = ("skills/poteto-mode/references/hosts/",)

# Upstream-owned paths written by the current run (for orphan cleanup).
WRITTEN = set()


def is_ours(rel):
    return rel in OURS_EXACT or rel.startswith(OURS_PREFIX)


def main():
    if not SRC.exists():
        sys.exit(f"upstream checkout missing: {SRC}")
    principle_dirs = sorted(p.name for p in (SRC / "skills").iterdir()
                            if p.is_dir() and p.name.startswith("principle-"))
    skill_dirs = CORE_SKILLS + principle_dirs

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
                        WRITTEN.add(rel.as_posix())
        scr = s / "scripts"
        if name in SKILL_SCRIPTS and scr.exists():
            for f in sorted(scr.rglob("*")):
                if f.is_file():
                    rel = Path("skills") / name / "scripts" / f.relative_to(scr)
                    (ROOT / rel.parent).mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, ROOT / rel)
                    WRITTEN.add(rel.as_posix())

    # poteto-mode playbooks + references (scripts/ intentionally omitted)
    pm, dst_pm = SRC / "skills" / "poteto-mode", ROOT / "skills" / "poteto-mode"
    for pb in sorted((pm / "playbooks").glob("*.md")):
        rel = Path("skills/poteto-mode/playbooks") / pb.name
        adapt_file(pb, dst_pm / "playbooks" / pb.name, rel)
    for f in sorted((pm / "references").glob("*.md")):
        rel = Path("skills/poteto-mode/references") / f.name
        if is_ours(rel.as_posix()):
            continue
        adapt_file(f, dst_pm / "references" / f.name, rel)

    # orphan cleanup: drop generated files upstream no longer ships.
    # Repo-owned paths are never touched.
    for base in (ROOT / "skills", ROOT / ".opencode" / "agents"):
        for f in sorted(base.rglob("*")):
            if f.is_file():
                rel = f.relative_to(ROOT).as_posix()
                if rel not in WRITTEN and not is_ours(rel):
                    f.unlink()
        for d in sorted((p for p in base.rglob("*") if p.is_dir()), reverse=True):
            try:
                d.rmdir()
            except OSError:
                pass

    # agents
    for a in ["poteto-agent.md", "comment-sicko.md"]:
        adapt_file(SRC / "agents" / a, ROOT / ".opencode" / "agents" / a,
                   Path(".opencode/agents") / a)

    (ROOT / "UPSTREAM_COMMIT").write_text(COMMIT + "\n")
    print(f"ported {len(skill_dirs)} skills + playbooks + 2 agents @ {COMMIT[:12]}")


if __name__ == "__main__":
    main()
