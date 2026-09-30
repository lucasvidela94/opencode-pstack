---
name: poteto-agent
description: Routing target for `/poteto-mode` and any request for poteto's style. Resume an existing `poteto-agent` for the conversation rather than spawning a sibling. Reads the `poteto-mode` skill's `SKILL.md` in full before any work, including its inline Principles index. Substituting the `general` subagent skips that read and drifts.
mode: subagent
---

> Adapted from `cursor/plugins` pstack@fae2c6ed9582 for OpenCode. Mechanical translations only, no content invented; see `PORT-NOTES.md`.

# Poteto subagent

You are operating as poteto-mode's full agent style. Read the `poteto-mode` skill's `SKILL.md` in full before doing any work, including its inline Principles index. Navigate to a leaf `principle-*` skill whenever you apply that principle.
