# Guide: three real tasks

Copy-paste prompts. Give the goal and how you'll know it's done; let the router pick the playbook. Invocation per host: `Use the … skill` (OpenCode), `/…` (Claude Code), `$…` (Codex).

## 1. Bug fix, repro first (verified live on OpenCode, 2026-09-30)

```text
Use the poteto-mode skill. sumOfSquares in src/math.ts returns the wrong result
for negative numbers. Repro first, then fix and verify. Keep the diff minimal.
```

What happened: matched the **Bug fix** playbook, reproduced before touching code (negatives failed, positives passed), delegated the fix to one scoped `poteto-agent`, then verified the real module directly — 4 cases green — and named the principles that shaped each decision (`fix-root-causes`, `prove-it-works`, `laziness-protocol`, `guard-the-context-window`). Final diff: one reducer body.

## 2. Investigation with `how` (real upstream prompt, ran on Cursor)

From upstream's examples (mined from Lauren Tan's sessions):

```text
Use the how skill. How do we cancel runs? Do we have an n+1 when we look up
every run to cancel?
```

What to expect: the **Investigation** playbook — read-only, no edits. Explorers fan out over the subsystem (2–4 angles), a synthesizer merges findings, and the answer cites files, not impressions. Use it whenever you're tempted to ask "are we sure?".

## 3. Adversarial review with `interrogate` (real upstream prompt, ran on Cursor)

```text
Use the interrogate skill. Review this PR and try to break it.
```

What to expect: independent reviewers attack the diff (assumptions, edges, races, failure modes) and the lead aggregates to one severity-ranked verdict with file references. On hosts without per-role models you get independent passes instead of model diversity — the skill says so.
