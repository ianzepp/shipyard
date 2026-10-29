# Goal Template

Use this template for `GOAL.md`, handoff goals, PRD goal sections, or harness-native goal prep notes.

```markdown
# Goal: <short name>

## Summary

<One short paragraph describing the desired end state.>

## Problem

- <Concrete problem 1.>
- <Concrete problem 2, if any.>

## Goals

- <Required outcome.>
- <Required behavior or artifact.>
- <Required verification or user-facing capability.>

## Non-goals

- <Explicitly excluded work.>
- <Tempting adjacent work the agent should not do.>

## Ground Truth Researched

- `<path or source>`: <what was learned>
- `<command or query>`: <what was learned>
- `<database/read-only data source>`: <what was learned>
- `<conversation/session/source>`: <what the user clarified>

## Reference Packet

Before editing, inspect:

- `<path>`: <why it matters>
- `<path>`: <why it matters>
- `<command>`: <what it verifies>
- `<read-only query or data source>`: <what assumption it grounds>

## Constraints And Invariants

- <Security, data, product, UX, architecture, compatibility, or permission rule.>
- <Any current repo convention the implementation must preserve.>

## Architecture Direction

- Boundary shape: <the modules, services, or layers involved and where the boundaries sit.>
- Data and control flow: <how data and control move through them.>
- Ownership: <which module or service is canonical for each responsibility.>
- Clean-break choices: <what is removed or replaced rather than kept for compatibility.>

## Supporting Skills

- `<skill>`: <when the implementing agent should use it>
- `<skill>`: <when the validating agent should use it>

## Implementation Shape

- Milestone 1: <smallest useful milestone>
- Milestone 2: <follow-up milestone, if known>
- Later: <deferred work, if useful>

## First Implementation Path

For the first milestone only. Full sequencing belongs to delivery and slicer.

- `<module, file, or service>`: <what changes there first>
- `<module, file, or service>`: <what follows, if needed to make the first edit>

## Release Posture

Decision: <release checkpoint required / release prep only / defer release / not applicable>

- <Version bump, changelog, release notes, tag, deployment, migration, or operator notice expected at a checkpoint.>
- <Authorization gate for publication/deployment, if any.>

## Exit Strategy

Decision: <included / not included / ask user before implementation>

- <Kill switch, rollback, removal plan, opt-out path, monitoring threshold, or other approved escape path.>

## Acceptance Criteria

- <Objective done check.>
- <Objective done check.>
- <Objective done check.>

## Validation

- `<command>` should <expected result>.
- Manual flow: <exact local/user-facing test path>.
- Review check: <what to inspect before calling it done>.

## Open Questions

- <Question that can materially change implementation.>

## Stop Conditions

- Stop if <assumption/evidence gap/permission boundary>.
- Stop if <destructive action or production write would be needed>.
- Stop if <exit strategy decision becomes necessary and was not approved>.

## Status

not started

<Updated by goal-check (readiness verdicts: verdict, evaluator mode, date, gaps), and by factory or campaign as work lands: milestone, commits, validation evidence.>
```

Keep the template specific. Delete empty sections only when they genuinely do not apply.
