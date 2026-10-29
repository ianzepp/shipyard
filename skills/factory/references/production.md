# Production

Use this reference inside `factory` after [$vision](vision.md) has confirmed an
execution-ready goal boundary.

Production turns a roadmap, slice plan, milestone list, or epic set into
delivery-sized units. It does not compile implementation work; that belongs to
[$delivery](../../delivery/SKILL.md). It does not execute; that belongs to [$loop](loop.md).

## Purpose

Production answers:

```text
What is the next delivery-sized unit factory should compile and execute?
```

## Inputs

- vision readiness record
- roadmap docs, slices, milestones, epics, issue sets, or prior plans
- repo ownership boundaries and current worktree state
- existing delivery specs and completed commits
- deferred findings from prior phases

## Ledger

Maintain a production ledger with:

- `Vision Source`
- `Roadmap Units`
- `Delivery-Sized Units`
- `Generated Delivery Specs`
- `Current Unit`
- `Completed Units`
- `Pending Units`
- `Blocked Units`
- `Dependency Notes`
- `Repo Boundaries`
- `Deferred Findings / Future Work`
- `User Decisions Needed`

The ledger may live in chat during short runs, but long factory runs should use
a durable repo-local artifact when a convention is obvious.

## Unit Selection

Select one delivery-sized unit at a time using this priority:

1. explicit user instruction
2. first unblocked roadmap unit
3. next dependency-unblocked slice or epic
4. largest coherent batch that can produce a meaningful checkpoint without crossing a concrete split boundary

A delivery-sized unit should have:

- a coherent outcome
- one primary repo or a clearly justified cross-repo boundary
- known inputs and expected outputs
- acceptance signals
- dependency notes
- a plausible validation path
- a clear reason it is not too large for one delivery compilation
- a clear reason it is not too small to justify a full factory loop

## Split Or Compile

Production should batch by default after the implementation pattern is known. If one slice has established the route, data model, API shape, test pattern, migration pattern, or doc pattern, group the remaining homogeneous requirements into the next delivery-sized unit instead of creating a long sequence of tiny units.

If a roadmap unit is too large, split it before delivery. Splitting must be justified by a named boundary, not by the mere presence of multiple checklist items.

Split when the unit:

- crosses unrelated repo or service boundaries
- mixes contracts, migrations, UI, operations, and docs without a convergence
  checkpoint
- has several unrelated acceptance targets
- cannot be validated as one coherent outcome
- would require broad speculative refactoring before useful progress
- has unresolved product or architecture decisions that would cause later work to be invented

Do not split when the unit:

- repeats an already-proven implementation pattern across files, commands, variants, routes, fixtures, docs, tests, or cases
- is mostly mechanical propagation with local variations
- can be validated by one targeted command set plus repo-standard hygiene
- would make the factory loop mostly planning, closeout, and status text instead of implementation

Compile when the unit is bounded enough for delivery to produce implementation-sized work and broad enough that execution does more work than process.

## Missing Specs

If a unit lacks an executable delivery spec, invoke [$delivery](../../delivery/SKILL.md) to
create one. Do not ask the user to hand-write implementation planning when the
goal and roadmap evidence are sufficient.

Ask the user only when:

- product intent is materially ambiguous
- an authority, security, deployment, or data decision is required
- acceptance criteria would be invented rather than inferred
- repository evidence contradicts the roadmap source

## Handoff To Delivery

For each selected unit, hand delivery:

- `Unit Name`
- `Unit Goal`
- `Vision Boundary`
- `Source Evidence`
- `Target Repo(s)`
- `Expected Outputs`
- `Known Dependencies`
- `Out Of Scope`
- `Checkpoint Target`
- `Open Questions`

Record the generated delivery spec in the production ledger before loop
execution begins.
