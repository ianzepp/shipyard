---
name: "goal-forge"
description: "Converge fuzzy intent into a grounded, agent-ready goal document for one focused target."
---

# Goal Forge

Conversational convergence for **one focused problem** before execution. Lock the problem shape, desired architecture, and rough implementation direction, gather evidence, then write a single **goal artifact** (`GOAL.md`, in its own directory). Does not implement the goal.

Optional upstream skill. Run when intent is fuzzy and the outcome should be one bounded target — not when several tracks already need a coordination map (use `campaign` instead).

Goal-forge operates at the **architecture and milestone** level. It should answer what needs to exist, which architecture direction is intended, what first useful milestone proves the direction, and what decisions remain open. It should not try to become a task-by-task implementation playbook; that stricter handoff belongs to `goal-check`, `delivery`, or `factory`.

## Vocabulary

| Term | Scope | Meaning |
| --- | --- | --- |
| **Goal artifact** | `goal-forge` | Single focused document (`GOAL.md`) defining one problem boundary and desired end state. |
| **Campaign artifact** | `campaign` | Multi-track routing document coordinating several goals, bugs, features, or cleanup families. |
| **Delivery spec** | `delivery` | Repo-aware plan for one phase (one coherent outcome). Lower from goal or campaign — not produced here. |
| **Factory phase** | `factory` | Execution cycle for one phase: a group of slices whose phase gate is evaluated together. |

**Rule:** Goal-forge forges **one goal**. Campaign maps **many tracks**. Delivery compiles **units** into **specs**. Factory executes **phases**.

## Goal-Forge vs Campaign

| | `goal-forge` | `campaign` |
| --- | --- | --- |
| **Scope** | One focused target | Broader sweep across related work |
| **Artifact** | Goal document | Campaign routing document |
| **Typical input** | Fuzzy idea, one problem, one `GOAL.md` to refine | Pile of goals, bugs, tracks, overlapping source docs |
| **Output** | Grounded architecture-direction goal ready for goal-check, factory, delivery, or direct work | Stage map lowering into delivery/factory loops |

Choose **goal-forge** when the user needs to talk through and lock **one** problem. Choose **campaign** when several grounded or partially grounded items need **one top-level map** before lowering.

Both are optional. Factory or campaign can start from an already-grounded artifact without goal-forge.

## Handoffs

| From | To | When |
| --- | --- | --- |
| User | `goal-forge` | Intent is fuzzy; one focused goal artifact is needed |
| `goal-forge` | `goal-check` | Goal drafted; need readiness verdict or second opinion |
| `goal-forge` | `campaign` | Pressure test reveals multiple tracks that need coordination |
| `goal-forge` | `factory` | Goal artifact is grounded; user authorizes multi-phase execution |
| `goal-forge` | `delivery` | One stable unit needs a delivery spec without full factory |
| `goal-forge` | direct implementation | Scope is small enough to implement without delivery planning |

Factory [`vision`](../factory/references/vision.md) validates goal readiness at factory entry. Goal-forge produces the artifact; vision checks execution readiness.

## Core Rules

- Do not implement code, migrations, UI, scripts, docs, or product changes — except writing or updating the goal artifact.
- Write the goal artifact and leave it in place. Factory intake records it per the workflow (see factory [Workflow](../factory/SKILL.md#workflow)).
- Do not create a harness-native goal or task object (if your tool has one) unless the user explicitly asks for one.
- When the user asks for `GOAL.md`, handoff, or PRD goal section, write the artifact — not a harness-native goal.
- Do not generate the final goal document until the problem shape is locked or the user explicitly asks for a rough draft.
- Treat conversation as intent, not ground truth. Verify against files, code, data, logs, docs, screenshots, transcripts, PRs, or explicit user statements.
- Target detail level: nail down the desired architecture, key invariants, rough implementation shape, and first useful milestone. Write a First Implementation Path for the first milestone only: the modules, files, or services where the first edit happens, enough for an implementer to start. Leave full file-by-file sequencing, exact edits, and mechanical task order to `delivery` and `slicer` unless the user explicitly wants them in the goal.
- Ask when the answer is a preference, authorization decision, or material ambiguity that cannot be discovered locally.
- Ask one question at a time unless a small related batch is clearly better.
- Do not create or switch branches; factory does that at intake (see factory [Workflow](../factory/SKILL.md#workflow)).

## When To Use

Use when the user asks to:

- talk through a problem before handing it to a process
- create, refine, split, or sanity-check a `GOAL.md`
- define a long-running implementation objective for **one** target
- turn a rough idea, PRD, branch, issue, bug narrative, or broad desire into an agent-ready goal
- decide whether a goal is grounded enough for `factory`, `delivery`, or direct implementation
- identify the first useful milestone without committing to a delivery plan

Do not use when:

- several tracks need one coordination map → `campaign`
- tiny one-command tasks
- direct implementation of an already-scoped issue
- delivery planning for an already-stable goal → `delivery`
- autonomous multi-phase execution → `factory`
- second opinion on an existing goal only → `goal-check`
- post-implementation completion gates → [`poker-face`](../poker-face/SKILL.md), `correctness`

## Inputs

Accept: raw idea; feeling the goal is not yet definable; existing `GOAL.md`, PRD, design doc, issue, branch, PR, transcript; bug narrative; broad implementation desire needing scope.

**Destination rules:**

- User provides a path → inspect before overwriting.
- User references an existing goal → update in place unless they ask for a separate draft.
- No path → pick a short kebab-case `<goal-name>` (for example `csv-export`) and write `docs/goals/<goal-name>/GOAL.md`, unless the repo has its own convention for where such documents live. Factory keeps the ledger, phase specs, slice files, and audit reports in the same directory. Record the path used.
- Multiple plausible roots → inspect layout; choose the most local root for the work.
- Full goal in chat only when the user asks for inline draft or filesystem writes are blocked.

## Workflow

### 1. Discovery Conversation

Reconstruct intent in the user's terms. Collect: pain/opportunity/failure; proposed solution; explicit non-wants; named repos, files, docs, branches, PRs, screenshots, transcripts, logs; constraints and taste notes; likely consumer (human, `factory`, direct agent, harness-native goal, PRD).

If still exploring, stay conversational. Do not force the artifact early.

**Exit:** restate desired outcome without inventing new scope.

### 2. Evidence Gathering

Research before asking for discoverable facts. Use a dedicated skill or tool for each item when you have one; when an evidence source is unavailable, record the substitution you used instead. Cover:

- orientation: read the repo layout, conventions, and validation paths before asking the user anything discoverable
- simplification: first-principles check of whether the requested solution is the simplest one
- gap analysis: the milestone versus the current implementation
- bug or regression starting point: reproduce and trace the failure read-only to find its cause, when the goal is a fix
- stale docs or PRDs: verify their claims against live code before trusting them
- blast radius: run `consequences` for API, schema, migration, security

Inspect authorized real data when available. Treat docs as claims; verify against code, schemas, tests, logs, runtime state, or user statements.

**Exit:** every major future claim points to an artifact, command, query, or explicit user statement.

### 3. Problem Lock

Produce a concise problem lock; ask the user to confirm or correct.

Include: `Actual problem`; `Desired end state`; `Architecture direction`; `Current evidence`; `Real constraints`; `Non-goals`; `First useful milestone`; `Open decisions`; `Exit strategy` (kill switch, rollback, removal, opt-out, monitoring).

`Architecture direction` should state the intended boundary shape, data/control flow, canonical module or service ownership, and any clean-break choices the user has made. Keep it high enough to guide implementers, but do not expand it into a full delivery spec during goal-forge.

Do not continue to the final document until the user accepts the lock, unless they ask for a rough draft.

**Exit:** user confirms or corrects the lock.

### 4. Pressure Test

Pressure-test before drafting. Use [references/pressure-test-checklist.md](references/pressure-test-checklist.md) when complex.

Check: missing acceptance criteria; undefined terms; unstated workflows; hidden data dependencies; migration assumptions; unresolved architecture choices; security boundaries; validation gaps; rollout/rollback needs; version or release checkpoint needs; first milestone size; whether an agent could declare victory while the user cannot test the result.

If multiple independent tracks emerge, note whether `campaign` is the better next step.

**Exit:** ambiguities resolved, recorded as open questions, or converted to user questions.

### 5. Draft The Goal

Write only after problem lock and pressure test are complete enough. Use [references/goal-template.md](references/goal-template.md).

Required sections: `Summary`; `Problem`; `Goals`; `Non-goals`; `Ground truth researched`; `Reference packet`; `Constraints and invariants`; `Architecture direction`; `Supporting skills`; `Implementation shape` (milestones in rough order — not a delivery plan); `First implementation path` (first milestone only: where the first edit happens); `Release posture` when user-visible or package-facing work is likely; `Exit strategy` when relevant; `Acceptance criteria`; `Validation`; `Open questions`; `Stop conditions`; `Status` (starts as `not started`; goal-check, factory, and campaign update it with verdicts and evidence).

Do not lower into epics, workstreams, merge waves, full file-by-file task lists, or delivery specs — that belongs to `delivery` and `slicer`. `goal-check` only verifies that the goal is ready for that step; it does not write it.

**Exit:** a future agent understands problem, intended architecture, boundaries, first milestone, evidence, and stop conditions without hidden chat context.

### 6. Handoff Readiness

Run a completion check against the user request, problem lock, evidence, and draft.

Use [goal-check](../goal-check/SKILL.md) when available — especially for second-opinion review after drafting. If it returns NOT READY, fill the gaps it lists (here or with the user), then run it again; goal-check records its verdict in the goal's `Status` section but never edits the goal's other sections. Use [`poker-face`](../poker-face/SKILL.md) adapted to the goal document only when a broader promise-versus-artifact audit is needed.

Do not report completion on a goal with material readiness gaps. Revise or record blockers explicitly.

Report one of:

| Label | Meaning |
| --- | --- |
| **Ready for factory** | Grounded goal boundary; factory `vision` can admit the roadmap or milestone into [production](../factory/references/production.md) |
| **Ready for delivery** | One stable unit can lower into a delivery spec |
| **Ready for campaign** | Goal is clear but work should route through a multi-track map first |
| **Ready for direct implementation** | Small enough that architecture and rough path are sufficient without delivery planning |
| **Needs more discovery** | Material problem, permission, evidence, or scope question remains |

## Output Patterns

**In progress:** `Problem Lock Draft`; `Evidence Used`; `Missing Context`; `Next Question`.

**Completed:** artifact path; ground truth sources; exit strategy decision; unresolved user questions; handoff readiness label; goal-check verdict if run.

**Blocked:** exact blocker; what was inspected; one next question or permission; what gets added after the answer.

## Anti-Rationalization

| Rationalization | Rebuttal |
| --- | --- |
| "The user already explained it, so I can skip research." | Conversation is intent, not ground truth. Verify against code and data. |
| "The docs say how it works." | Docs are claims. Prove them against implementation and current data. |
| "The goal can be broad because the agent will figure it out." | Broad goals wander. Define the first useful milestone — or route to `campaign`. |
| "We can add rollback later." | Ask about exit strategy now or record it as out of scope. |
| "This is just planning, so validation can wait." | A goal without validation teaches agents to declare victory without evidence. |
| "Factory can clean this up later." | Factory executes phases. It should not rediscover what problem the user meant. |
| "I should create the harness-native goal now because the draft looks good." | Harness-native goals only when the user explicitly asked and the goal is grounded. |
