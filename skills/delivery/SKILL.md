---
name: delivery
description: Turn one bounded but messy unit of work into a durable, repo-aware implementation specification. Use for planning only; use factory when implementation is requested.
---

# Delivery

Delivery compiles one coherent outcome into a specification that `factory` can
execute. It inspects and plans, but does not implement, verify product behavior,
change product code, or run the factory lifecycle. It writes only its own spec
artifact and leaves it in place. Factory intake records it per the workflow
(see factory [Workflow](../factory/SKILL.md#workflow)).

Use `campaign` first when several tracks need one routing contract. Skip
delivery when the work is already implementation-ready and the user wants a
simple scoped change rather than a planned factory run.

## Contract

A delivery specification must:

- preserve all scope admitted by its input: a campaign stage or a goal
  artifact (`goal-forge` output, ideally `READY` from `goal-check`);
- resolve requirements against the live repository;
- separate evidence, inference, and unresolved decisions;
- identify implementation units that start with a named edit rather than more
  architectural discovery;
- name dependencies, write scopes, validation, integration gates, and stop
  conditions;
- remain useful across compaction and handoff.

Delivery may sequence or split work at a concrete logical-change boundary. It
may not narrow the campaign contract. If the target is too broad or unstable
to lower honestly, return it for campaign amendment or define a mandatory
discovery unit followed by explicit successors.

## Planning Pipeline

Run these steps in order and preserve each step's output for the next:

1. **Interpret.** Identify the intended outcome, explicit requirements,
   constraints, non-goals, contradictions, and unresolved decisions.
2. **Normalize.** Produce one stable unit description and concrete completion
   conditions.
3. **Resolve against the repo.** Inspect current code, tests, configuration,
   history, ownership boundaries, migrations, deployment shape, and relevant
   conventions. Treat docs as claims until corroborated.
4. **Lower to a unit graph.** Define implementation units, dependencies, and
   integration points.
5. **Assign implementation work.** Give each unit a bounded write scope,
   named edit, done-when condition, and narrow sanity check when useful.
6. **Define checkpoints and gates.** Separate unit sanity from integration,
   suite, migration, release, or external-effect gates.

Record later revisions explicitly instead of silently rewriting earlier
decisions.

## Unit Sizing

Keep one specification for one coherent outcome, and by default one
specification for one factory phase. That outcome may require many
implementation units. A goal that needs several phases gets one spec (and one
slice file) per phase.

One implementation unit is one logical change:

- one behavior family on one primary surface, with matching tests when useful;
- small enough to implement and verify without owning project-wide gates;
- large enough that its process overhead does not exceed the change;
- independently integrable, or paired with an explicit merge gate when atomic
  landing is required.

Do not put a clean break, all callers, all documentation, and the full suite on
one implementer. Do not create five-line units whose task descriptions are
larger than their code. Batch homogeneous work into the same specification, not
automatically into the same worker.

Prefer parallel work only when write surfaces and dependencies are genuinely
disjoint. Shared hot modules, migrations, generated artifacts, and atomic
authority changes need an explicit serialization or integration plan.

## Artifact

Save the result before implementation. Use the repo's own plans or docs
convention. By default, for a goal, write `docs/goals/<goal-name>/phase-<n>.md`
next to its `GOAL.md` (one spec per phase). For a standalone unit with no goal,
pick a short kebab-case name and use `docs/goals/<name>/phase-1.md`. Record the
path used. Ask only when destination choice would be material.

Include:

1. `Interpreted Unit`
2. `Normalized Spec`
3. `Repo-Aware Baseline`
4. `Unit Graph`
5. `Implementation Work`
6. `Checkpoints And Gates`
7. `Validation`
8. `Review Lenses`
9. `Open Questions`

`Review Lenses` names which lens skills the work should run and when:
[`correctness`](../correctness/SKILL.md), [`cleanliness`](../cleanliness/SKILL.md),
[`housekeeping`](../housekeeping/SKILL.md) (between phases only),
[`consequences`](../consequences/SKILL.md) (before risky design or migration
changes), [`red-green`](../red-green/SKILL.md) (for testability and coverage programs;
failing-test-first proof for ordinary behavior changes is already enforced at
slice sign-off), and [`poker-face`](../poker-face/SKILL.md)
(after implementation, against the promised outcome). Factory's
[order](../factory/SKILL.md#order) sets the order in which they run.

Each implementation assignment should be expressible as a short pointer:

```text
delivery: <spec path>
unit: <id>
write_scope: <paths>
edit: <named seam or behavior>
done_when: <unit outcome>
sanity: <optional narrow check>
```

Name whether completion implies `release-now`, `release-prep`,
`defer-release`, or `not-applicable`, with the evidence or repository
convention behind that decision.

## Ready

The specification is implementation-ready only when a worker can begin the
named edit without rediscovering the architecture, every admitted requirement
remains represented in a mandatory unit or gate, dependencies are explicit,
and validation honestly proves the intended outcome.

Units stay at the logical-change level. The next step is
[`slicer`](../slicer/SKILL.md): it cuts each unit into small self-contained
slices against the current code, just before implementation.

Finish with a short response pointing to the saved artifact and naming only
blocking open questions. Do not paste the full specification into chat.
