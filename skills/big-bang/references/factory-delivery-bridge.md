# Factory And Delivery Bridge

Big Bang should learn from `goal-forge`, `delivery`, and `factory` without becoming any of them.

`goal-forge` converges one chosen branch into a grounded goal document. `delivery` is the compiler for a selected branch. `factory` is the long-running
supervisor for a selected phase set. Big Bang is the discovery engine that
creates enough structured material for either handoff to work.

Big Bang does not implement. For software projects, it may explore architecture
futures, product surfaces, operational consequences, sequencing, risk, and
planning paths, but it should not generate application code, scaffold a
repository, install dependencies, or begin execution. Use Big Bang to decide
where the project should go; use `goal-forge`, `delivery`, or `factory` after a branch is ready
to become implementation work.

Big Bang should not require the user to select every branch before exploration
can continue. A branch can be selected provisionally for exploration without
becoming the final delivery branch. Record provisional branch choices in a
decision ledger, explore the best one or two branches, and promote only when a
branch has enough evidence, artifacts, and acceptance shape to justify handoff.

## Use Delivery Patterns Inside Big Bang

Borrow these patterns before any implementation handoff:

- `interpreted problem`: restate the rough idea's real center
- `normalized spec`: split facts, assumptions, constraints, and open questions
- `artifact flow`: name what each artifact consumes and produces
- `milestone graph`: sketch how a branch would unfold if selected
- `checkpoint target`: describe what would prove a branch is ready to promote
- `gate criteria`: state what would make the branch pass, fail, or need review
- `decision ledger`: record provisional branch choices, parked branches, and
  evidence that would reverse a choice

Do not over-compile too early. A speculative branch can have a lightweight stage
graph without pretending to be ready for implementation.

## Use Factory Patterns Inside Big Bang

Borrow these patterns when the idea starts spanning many turns:

- keep a `Big Bang Ledger`
- select one branch or artifact question at a time
- preserve completed, active, and pending branches
- continue down a provisional lead branch rather than waiting at every fork
- define checkpoint policies for branch promotion
- record what would trigger delivery or factory handoff
- keep recovery state in a repo-local artifact, not only in chat

The factory-like behavior here is supervision, not execution. Big Bang supervises
idea expansion until the work becomes executable.

## Goal-Forge Handoff Packet

Create this when one branch is chosen but the problem still needs to be locked
and grounded in the repo before any plan. `goal-forge` takes it as its starting
input, then verifies the evidence itself.

```markdown
## Goal-Forge Handoff

Chosen branch:

Why this branch:

Evidence for it (artifacts, files, data, user statements):

Rejected or parked branches:

Known constraints and non-goals:

Open decisions:
```

## Delivery Handoff Packet

Create this when one branch should become a concrete plan:

```markdown
## Delivery Handoff

Selected branch:

Why this branch:

Interpreted problem:

Normalized spec:

Known constraints:

Required repo or workspace context:

Suggested milestone graph:

Checkpoint targets:

Gate criteria:

Open questions:
```

## Factory Handoff Packet

Create this when the selected branch has a phase set that should be executed
autonomously:

```markdown
## Factory Handoff

Phase Set Source:

Selected Branch:

Target Workspace:

Delivery Spec Directory:

Checkpoint Policy:

Workflow (how changes are isolated, made durable, integrated):

Agent Policy:

Completed Big Bang Artifacts:

Pending Phases:

Open Questions:

Stop Or Escalation Conditions:
```

## Promotion Rules

Promote from Big Bang to goal-forge when:

- the user has chosen a branch, or a provisional branch is ready for approval
- the problem is still fuzzy in the repo's terms: architecture, first milestone,
  and acceptance criteria are not yet written down
- the next useful artifact is one grounded goal document, not yet a plan

Promote from Big Bang to delivery when:

- the user has chosen a branch, or the agent has clearly marked a provisional
  branch as ready for the user's approval
- acceptance criteria can be described
- the next useful artifact is an executable delivery plan
- implementation details are becoming concrete enough that staying in Big Bang
  would invite accidental code generation or scaffolding

Promote from Big Bang to factory when:

- the user wants autonomous multi-phase execution
- the phase list is durable enough to survive compaction
- checkpoints are clear and the workflow is chosen or left for factory intake (see factory [Workflow](../../factory/SKILL.md#workflow))
- the work is no longer primarily about discovering the idea

Stay in Big Bang when:

- branch choice is still unclear
- pressure tests are missing
- the next step is research, inventory, narrative, or artifact shaping
- a handoff would create fake certainty
- the branch point can be responsibly played out with provisional choices
  instead of pausing for human input
- the project may eventually involve software, but the current need is still
  possible futures, consequences, judgment calls, or planning direction
