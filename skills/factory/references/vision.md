# Vision

Use this reference inside `factory` before production begins.

Vision imports and checks the goal boundary that factory will execute. It does
not replace [$goal-forge](../../goal-forge/SKILL.md). If the
goal is still fuzzy, route back to goal-forge instead of inventing missing
intent.

## Purpose

Vision answers one question:

```text
Is this goal, roadmap, or vision packet grounded enough for factory execution?
```

Inputs can include:

- `GOAL.md`, PRDs, design docs, roadmap docs, milestone lists, issues, transcripts,
  or explicit user instructions
- repo state, tests, generated docs, schemas, logs, or other evidence
- prior delivery specs or factory ledgers

## Readiness Check

Extract and record:

- `Goal Boundary`: what outcome factory is allowed to pursue
- `Non-goals`: tempting adjacent work to exclude
- `Ground Truth`: files, docs, commands, data, or explicit user statements used
- `Invariants`: architecture, product, security, data, compatibility, or ops
  rules that must remain true
- `Acceptance Signals`: how completion can be recognized
- `Stop Conditions`: what should force factory to pause
- `Initial Production Inputs`: roadmap units, milestones, campaign stages,
  epics, or first useful implementation targets

Classify gaps:

- `Inferable`: can be resolved from repo evidence or source docs
- `Blocking`: material product, authority, permission, or acceptance ambiguity
- `Deferred`: real future work but not needed to begin production

## Gate

Proceed to [production](production.md) only when:

- the goal boundary is clear enough to prevent hidden scope invention
- at least one production input or first useful milestone exists
- acceptance signals and stop conditions are concrete enough for review
- every blocking gap is resolved, or the user has explicitly accepted
  proceeding with each one named (record them in the ledger)

If the goal is not ready, pause and recommend goal-forge with the exact missing
problem-lock fields. Do not use factory to discover the user's real goal while
also implementing it.
