# Production

Use this reference inside `factory` after [vision](vision.md) has confirmed an
execution-ready goal boundary.

Production turns a roadmap, milestone list, campaign stage list, or epic set into
phase candidates: phase-sized outcomes, each compiled into one delivery spec
and run as one factory phase. It does not compile implementation work; that belongs to
[delivery](../../delivery/SKILL.md). It does not execute; that belongs to [loop](loop.md).

## Purpose

Production answers:

```text
What is the next phase candidate factory should compile and execute?
```

## Inputs

- vision readiness record
- roadmap docs, milestones, campaign stages, epics, issue sets, or prior plans
- repo ownership boundaries and current worktree state
- existing delivery specs and accepted work
- deferred findings from prior phases

## Ledger

Maintain a production ledger with:

- `Vision Source`
- `Roadmap Units`
- `Phase Candidates`
- `Generated Delivery Specs` (one per phase)
- `Current Candidate`
- `Completed Candidates`
- `Pending Candidates`
- `Blocked Candidates`
- `Dependency Notes`
- `Repo Boundaries`
- `Deferred Findings / Future Work`
- `User Decisions Needed`

This production section is part of the run's one ledger file
([loop](loop.md#ledger-file)); never keep it only in chat.

## Candidate Selection

Select one phase candidate at a time using this priority:

1. explicit user instruction
2. first unblocked roadmap unit
3. next dependency-unblocked milestone, stage, or epic
4. largest coherent batch that can produce a meaningful checkpoint without crossing a concrete split boundary

A phase candidate should have:

- a coherent outcome
- one primary repo or a clearly justified cross-repo boundary
- known inputs and expected outputs
- acceptance signals
- dependency notes
- a plausible validation path
- a clear reason it is not too large for one delivery compilation
- a clear reason it is not too small to justify a full factory loop

## Split Or Compile

Production should batch by default after the implementation pattern is known. If one phase has established the route, data model, API shape, test pattern, migration pattern, or doc pattern, group the remaining homogeneous requirements into the next phase candidate instead of creating a long sequence of tiny phases.

If a roadmap unit is too large for one phase, split it into several candidates before delivery. Splitting must be justified by a named boundary, not by the mere presence of multiple checklist items.

Split when the candidate:

- crosses unrelated repo or service boundaries
- mixes contracts, migrations, UI, operations, and docs without a convergence
  checkpoint
- has several unrelated acceptance targets
- cannot be validated as one coherent outcome
- would require broad speculative refactoring before useful progress
- has unresolved product or architecture decisions that would cause later work to be invented

Do not split when the candidate:

- repeats an already-proven implementation pattern across files, commands, variants, routes, fixtures, docs, tests, or cases
- is mostly mechanical propagation with local variations
- can be validated by one targeted command set plus repo-standard hygiene
- would make the factory loop mostly planning, closeout, and status text instead of implementation

Compile when the candidate is bounded enough for delivery to produce implementation-sized work and broad enough that execution does more work than process.

## Missing Specs

If a candidate lacks an executable delivery spec, invoke [$delivery](../../delivery/SKILL.md) to
create one. Do not ask the user to hand-write implementation planning when the
goal and roadmap evidence are sufficient.

Ask the user only when:

- product intent is materially ambiguous
- an authority, security, deployment, or data decision is required
- acceptance criteria would be invented rather than inferred
- repository evidence contradicts the roadmap source

## Handoff To Delivery

For each selected candidate, hand delivery one phase (one delivery spec per phase):

- `Phase Name`
- `Phase Goal`
- `Vision Boundary`
- `Source Evidence`
- `Target Repo(s)`
- `Expected Outputs`
- `Known Dependencies`
- `Out Of Scope`
- `Checkpoint Target`
- `Open Questions`

Record the generated delivery spec in the production section of the ledger
before loop execution begins.
