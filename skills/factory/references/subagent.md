# Subagent

Use this reference only for the parts of Factory execution that are specifically about using subagents. Factory already owns phase lifecycle, delivery specs, verification, gates, commits, correctness passes, and resumability.

## Core Principle

Subagents are bounded workers or reviewers with isolated context. The parent Factory run keeps global state, phase boundaries, ledgers, gates, and final verification authority.

Use subagents to reduce context pollution, parallelize independent investigation, and create independence between implementation and review. Do not use subagents as a replacement for Factory's lifecycle. Subagent use is an optional harness feature: if the tool has no subagents, run the same review and bounded work in the parent. When a phase needs more than one bounded worker assignment, cut the assignments with [$slicer](../../slicer/SKILL.md) so write scopes are disjoint.

## When To Use A Subagent

Use a subagent when the unit of work is:

- bounded enough to describe in a complete handoff packet
- separable from other active workstreams
- useful to isolate from the parent context
- reviewable from concrete outputs, files, commands, or findings
- unlikely to require unresolved product judgment from the user

Good subagent jobs:

- implement one narrow work item from the current Factory phase
- inspect a focused subsystem and report evidence
- run a contained bug investigation
- review a concrete diff against a specific spec
- review code quality, tests, or security for named files
- compare two possible implementation approaches and recommend one

Poor subagent jobs:

- own the whole Factory phase lifecycle
- decide phase boundaries or checkpoint policy
- make product calls that require user judgment
- edit overlapping files in parallel with another worker
- perform unbounded repo exploration without a clear question
- replace the parent agent's final verification

## Handoff Packet

Every subagent prompt should be self-contained. Include only the context needed for that bounded job.

Minimum handoff fields:

- `Role`: implementer, investigator, reviewer, verifier, researcher, etc.
- `Goal`: the exact bounded outcome expected
- `Phase Context`: the current Factory phase and why this job exists
- `Inputs`: relevant spec excerpts, file paths, failing commands, logs, constraints
- `Allowed Scope`: files, directories, commands, or behavior the subagent may touch
- `Out Of Scope`: explicit non-goals and boundaries
- `Expected Output`: patch, report, verdict, evidence list, command transcript, or questions
- `Verification`: commands or checks the subagent should run when applicable
- `Escalation`: what should make the subagent stop and report instead of guessing

Do not ask a subagent to infer the plan from the full repository when the parent already knows the relevant scope. Package it; for an implementer, the packet is the slice brief and its write scope.

## Role Patterns

### Implementer

Use for a concrete edit inside the current phase.

Required constraints:

- name the files or directories likely in scope
- provide acceptance criteria
- provide the relevant test or verification command
- when the brief says `red_first: yes`, require the new test to be run and seen failing before the change, with a summary of the failing output in the report (see [Running a Slice List](loop.md#running-a-slice-list))
- forbid unrelated cleanup
- forbid commits; the parent commits path-limited after sign-off
- require a concise summary of changed files and verification performed

### Investigator

Use for evidence gathering before a fix or design choice.

Required constraints:

- keep it read-only unless explicitly authorized
- ask for confirmed evidence separately from inference
- ask for exact files, symbols, commands, and observations
- require a short recommendation or next action

### Spec Reviewer

Use to check whether an implementation matches a specific spec.

Required constraints:

- provide the original spec excerpt directly
- ask for PASS or specific gaps
- separate missing requirements from optional improvements
- forbid style commentary unless it affects spec compliance

### Quality Reviewer

Use after the spec is satisfied to review implementation quality.

Required constraints:

- classify issues on the canonical `P0` / `P1` / `P2` scale ([factory's Verdicts and Severity](../SKILL.md#verdicts-and-severity))
- focus on bugs, maintainability, security, tests, and project conventions
- require concrete file/line evidence when possible
- produce `PASS` (no `P0` or `P1`; any `P2` becomes a deferred finding) or `FAIL` (any `P0` or `P1`)

### Verifier

Use to independently run or inspect validation evidence.

Required constraints:

- state the exact commands to run or checks to inspect
- report pass/fail and relevant excerpts
- call out skipped checks and why
- avoid implementing fixes unless explicitly asked

## Tool Scoping

Give subagents only the tools their role needs.

Examples:

- implementer: file + terminal
- reviewer: file, sometimes terminal
- investigator: file + terminal, optionally web if external facts matter
- documentation reviewer: file only
- researcher: web + file

A narrower toolset improves focus and reduces accidental side effects.

## Parallelism Rules

Parallelize only when workstreams are independent.

Safe parallelism:

- separate read-only investigations
- reviewers inspecting the same completed diff without writing
- implementation tasks touching disjoint files or modules
- research tasks that produce reports rather than edits

Unsafe parallelism:

- multiple implementers editing the same files
- parallel git index mutations or commits
- concurrent formatters over shared trees
- one worker changing APIs while another builds on the old shape
- workers that depend on each other's unmerged results

When in doubt, serialize implementers and parallelize reviewers.

## Verification Discipline

Subagent summaries are claims, not proof.

The parent Factory run should verify important outcomes before advancing gates or committing:

- inspect the actual diff or files when the change matters
- run or review the named verification commands
- confirm generated artifacts exist at the expected paths
- confirm the subagent made no commits
- re-run failed or ambiguous checks in the parent context when necessary

A reviewer subagent can inform a gate, but the parent owns the gate decision.

## Failure Handling

If a subagent fails, returns vague output, exceeds scope, or surfaces a blocker:

1. preserve the useful evidence
2. tighten the handoff packet
3. spawn a focused repair, investigation, or review subagent if useful
4. otherwise resume in the parent with the narrowed facts

Do not let a single subagent context sprawl indefinitely. If the job has changed, start a fresh bounded subagent.

## Prompt Template

```text
Role: <implementer | investigator | spec reviewer | quality reviewer | verifier>

Goal:
<one bounded outcome>

Factory Phase Context:
<current phase and why this job exists>

Inputs:
- <spec excerpt, paths, logs, commands, constraints>

Allowed Scope:
- <files/dirs/actions allowed>

Out Of Scope:
- <explicit exclusions>

Verification:
- <commands/checks to run or inspect>

Expected Output:
- <patch/report/verdict/evidence/questions>

Escalate Instead Of Guessing If:
- <conditions that should stop the subagent>
```

## Keep Out Of This Reference

Do not put Factory lifecycle rules here. The following belong in Factory's main loop or other references, not in Subagent:

- phase selection
- delivery spec generation
- checkpoint design
- correctness mode
- red-green mode
- polish closeout policy
- commit unit and bookkeeping commits
- compaction recovery
- final Factory reporting
