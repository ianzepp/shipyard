---
name: "goal-check"
description: "Verify whether a goal document is defined enough to begin using as an implementation target."
---

# Goal Check

Pre-implementation readiness check for an **existing goal artifact**. Decide whether a goal is specific, grounded, bounded, architecturally decided, and testable enough that the next agent can start without inventing hidden scope.

Optional skill. Not a completion gate for work that has already been built — that is [`poker-face`](../poker-face/SKILL.md).

Goal-check uses a stricter handoff bar than goal-forge. A goal that only captures the desired architecture and rough implementation direction may be good goal-forge output, but it is not automatically ready for implementation. Goal-check judges the document against that bar and names every gap that keeps it from being deliverable to a competent implementer who was not in the conversation. It does not edit the goal's content: `NOT READY` lists the exact gaps, `goal-forge` (or the user) fills them, and goal-check runs again. It only records its verdict (see [Record The Verdict](#4-record-the-verdict)).

## Primary Use Cases

| Use case | When | How |
| --- | --- | --- |
| **Stale pickup** | User returns to a `GOAL.md` or handoff doc they have not read in a while | Time-boxed re-read; verify goal still matches current repo reality and intent |
| **Second opinion** | One model or agent drafted the goal; a different reviewer should cold-read it | Independent pass: judge the artifact and evidence, not the author's summary |

For second opinion: treat the goal document as source of truth. The drafter's chat summary, rationale, and "looks ready" claims are evidence only — not authority. Prefer a separate agent or model when delegation allows; otherwise perform an explicit cold pass and report `Evaluator mode: self-contained cold pass`.

## Vocabulary

| Term | Scope | Meaning |
| --- | --- | --- |
| **Goal artifact** | `goal-forge` output | Single focused goal document (`GOAL.md`, etc.). |
| **Campaign artifact** | `campaign` | Multi-track routing document — not what goal-check reviews unless the user points at a goal-shaped section. |
| **Delivery spec** | `delivery` | Implementation plan for one unit — checked by delivery/factory, not goal-check. |

**Rule:** Goal-check judges **implementation handoff readiness**. Poker-face judges **requirement completion** after implementation.

## Handoffs

| Verdict | Next step |
| --- | --- |
| `READY` + consumer is `factory` | Send to factory; [`vision`](../factory/references/vision.md) validates at entry |
| `READY` + consumer is `delivery` | Lower one stable unit into a delivery spec |
| `READY` + consumer is direct implementation | Begin scoped implementation |
| `READY` + consumer is `campaign` | User may need multi-track map before lowering |
| `NOT READY` | List the exact gaps. `goal-forge` (or the user) fills them, then run goal-check again; goal-check does not edit the goal's other sections |
| `NEEDS FURTHER REVIEW` | Escalate; do not bluff readiness |

| From | To | When |
| --- | --- | --- |
| `goal-forge` | `goal-check` | Goal drafted; readiness or second opinion needed |
| User | `goal-check` | Picking up stale goal doc; verifying before resuming work |
| `goal-check` | `goal-forge` | `NOT READY`: the listed gaps need a discovery conversation or an edit to the goal |
| `goal-check` | `campaign` | Review reveals multiple tracks needing coordination |

Do not use goal-check to: invent product scope; write or edit goals (beyond recording its verdict); execute; replace post-implementation review. It may require implementation-path detail inside the goal document (the `First Implementation Path` section, for the first milestone) when that detail is necessary for an unambiguous handoff, and it reports the absence as a gap rather than writing it.

## When To Use

Use when the user asks to:

- check whether a goal is ready to implement
- review a `GOAL.md`, goal section, handoff doc, or document packet
- decide if a goal can go to `factory`, `delivery`, or direct implementation
- find gaps that would make an agent wander, guess, or overreach
- verify architecture decisions, implementation path, acceptance criteria, validation, constraints, and stop conditions before work begins
- get a **second opinion** on a goal another agent drafted
- **re-validate** a goal document after time away from the project

Typical artifacts: `GOAL.md`, `goal.md`, PRD goal sections, handoff docs; supporting research, issues, design docs; acceptance criteria; constraints, non-goals, open questions, stop conditions.

Do not use for: writing goals from scratch (`goal-forge`); delivery planning (`delivery`); execution (`factory`); post-implementation review ([`poker-face`](../poker-face/SKILL.md), `correctness`); exhaustive repo-wide audits.

## Hard Constraints

Time-box the review. Decide whether the goal is usable as an implementation handoff.

- Spend limited time gathering context.
- Review against the goal's intended use as an implementation target.
- Focus on clarity, grounding, architecture decisions, implementation path, boundaries, acceptance criteria, validation, constraints, stop conditions.
- Supporting docs are evidence, not an invitation to redesign the goal.
- Do not require line-by-line edits, final code shapes, or exhaustive mechanical steps.
- Do require all material architecture decisions: canonical ownership, data/control flow, schema or API shape when relevant, integration boundaries, migration posture, compatibility stance, and the first milestone's implementation path through concrete files/modules/services when discoverable.
- Design choices may defer to `delivery` or `factory` only when the deferral is explicit, non-material to the starting architecture, and does not force the implementing model to choose between incompatible approaches.
- Do not pass a goal requiring guesswork on end state, architecture, success conditions, permissions, data shape, implementation order, or excluded scope.
- Do not fail a goal for non-material details deliberately deferred to delivery planning.
- Do not approve a goal you do not understand. Escalate.

Every review ends with: `READY`, `NOT READY`, or `NEEDS FURTHER REVIEW`.

## Goal Check Method

### 1. Reconstruct The Intended Target

Establish:

- what the goal should accomplish
- next consumer: `factory`, `delivery`, direct implementation, `campaign`, human review, or other planning layer
- authoritative documents vs supporting context
- in-scope and out-of-scope work
- intended architecture and the decisions already locked
- expected implementation path: concrete areas, files, modules, services, commands, migrations, generated artifacts, or manual flows the implementer should touch or inspect
- open questions and whether they block implementation

Unclear intended target → readiness signal.

For **stale pickup**, also check: repo state may have changed since the goal was written; flag stale claims against current code, tests, or docs.

For **second opinion**, read the goal artifact before the drafter's completion summary.

### 2. Check Goal Readiness

| Category | What to check |
| --- | --- |
| Desired end state | Concrete outcome named, not just activity |
| Grounding | Claims point to files, docs, data, commands, screenshots, or user statements |
| Architecture decisions | Canonical ownership, boundaries, data/control flow, API or schema posture, compatibility stance, and migration direction are decided where material |
| Boundaries | Goals, non-goals, constraints, stop conditions explicit |
| Acceptance criteria | Success judged without hidden chat context |
| Validation | Practical checks, commands, manual flows, or review steps named |
| Implementation handoff | Concrete starting path, expected touchpoints, sequencing, and deferred decisions are clear enough for a competent implementer who was not in the conversation to execute |
| Open questions | Listed; blocking only when they materially change implementation |
| Staleness | For stale pickup: material claims still true against current repo |

Prefer concrete blockers over broad improvement notes.

### 3. Make The Verdict

**`READY`** when:

- desired end state is clear
- material architecture decisions are explicit or intentionally deferred without blocking the starting path
- scope, non-goals, constraints, stop conditions suffice for the intended next process
- acceptance criteria and validation are specific enough to judge completion
- open questions absent, non-blocking, or correctly deferred
- an implementation agent can start without inventing hidden requirements, selecting the architecture, or guessing the first files/modules/services to change
- for stale pickup: no material stale claims block the goal

**`NOT READY`** when:

- desired end state ambiguous
- architecture direction or material design decisions are missing
- implementation path is too vague for a competent implementer who was not in the conversation to follow without choosing between plausible approaches
- material boundaries, constraints, permissions, data assumptions, or non-goals missing
- acceptance criteria subjective, absent, or disconnected
- validation absent for risky or user-visible outcomes
- blocking open questions not called out
- for stale pickup: goal contradicts current repo reality on material points

Be specific. Name each gap to fix before implementation begins; do not fix it yourself.

**`NEEDS FURTHER REVIEW`** when:

- goal not understandable after reasonable effort
- readiness depends on domain, security, architecture, data, or product judgment you cannot verify quickly
- document packet too large or contradictory for a bounded check
- approving would require pretending to know more than you do

Uncertainty escalates; do not bluff.

### 4. Record The Verdict

Write the verdict, evaluator mode, date, and any blocking gaps into the goal's `## Status` section, or into the run's ledger when one exists (see factory [Ledger File](../factory/references/loop.md#ledger-file)). This is the only edit goal-check makes, and it never touches the goal's other sections. Leave the edit in place; factory intake records it per the workflow (see factory [Workflow](../factory/SKILL.md#workflow)).

## Output Format

1. **Goal Check Summary** — artifact reviewed; evaluator mode (independent / self-contained cold pass); intended next consumer; handoff bar used; verdict
2. **Reasoning** — one short paragraph
3. **Key Points** — flat bullets for main readiness findings, including architecture and implementation-path clarity
4. **Blocking Gaps** — only when `NOT READY`
5. **Escalation Reason** — only when `NEEDS FURTHER REVIEW`
6. **Recorded in** — the goal's `Status` section or the ledger, with the path
7. **Recommended next step** — `factory`, `delivery`, `campaign`, `goal-forge` (fill the gaps, then re-run goal-check), or direct implementation

## Language To Use

Prefer: goal is ready / not ready; implementation handoff is ready / not ready; desired end state unclear; architecture decision missing; implementation path unclear; acceptance criteria insufficient; validation gap; hidden scope risk; non-goals missing; blocking open question; stale claim; ready for factory / delivery / campaign / direct implementation; needs deeper review.

Avoid vague "some concerns" when you can name the exact gap.
