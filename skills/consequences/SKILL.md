---
name: "consequences"
description: Read-only forward trace of what a proposed design, refactor, migration, PR, or diff will affect before implementation. Use for blast radius, follow-on work, and compatibility risk — not for diagnosing existing failures or simplifying architecture from first principles.
---

# Consequences

Trace **forward** from a proposed change: what else must move, what breaks, what follow-on work is missing. Read-only. You are the oracle, not the implementer.

Focus: **pre-implementation blast radius and downstream pressure**. It does not simplify the design or review existing code; it traces what lands if the proposal ships.

## Role In The Stack

| Skill | Direction | Question |
| --- | --- | --- |
| `consequences` | Forward | If this change lands, what else moves or breaks? |
| diagnosing a failure | Backward | What caused the observed failure? Reproduce, trace, and find the cause read-only before any fix. |
| `correctness` | Present code | Does existing behavior fail? |
| `big-bang` | Futures | What paths and tradeoffs exist before choosing one? |

If repo context is fuzzy, orient in the repo (layout, conventions, entry points) before tracing. Do not guess architecture you have not oriented to.

## When To Use

Use when the user asks to:

- predict what a change will affect
- analyze blast radius before implementation
- review a refactor, migration, API/schema change, PR, diff, or design for downstream effects
- identify required follow-on work
- pressure-test a proposal for implementation gaps

Typical artifacts: PRs; design docs; refactor/migration plans; schema or API contract changes; feature proposals.

Do not use for:

- diagnosing an already observed failure → diagnose the failure read-only first (reproduce, trace, find the cause)
- implementing the change
- style, readability, or structural cleanup → `cleanliness`
- broad futures exploration → `big-bang`

## Hard Constraints

**Read everything. Change nothing.**

| Allowed | Forbidden |
| --- | --- |
| read files; `rg`; inspect diffs, commits, history | edit files |
| run tests/builds to understand current state | make the change under analysis |
| inspect config, schemas, interfaces | invent impact without code/contract trace |
| | treat speculation as certainty |

## Forward Trace

### 1. Understand the proposal

Establish: what is changing; why; proposal assumptions; whether the change is additive, breaking, behavioral, structural, or operational.

If the proposal is vague, say so before tracing.

**Exit:** change entrypoint identified (schema, API, module, data shape, workflow, contract).

### 2. Identify the impact zone

First-order areas touched:

| Area | Questions |
| --- | --- |
| Data | schema, migrations, backfills, indexes? |
| API / protocol | fields, compatibility, versioning? |
| Business logic | branches, invariants, validation, permissions? |
| UI | states, errors, loading, copy? |
| Tests | fixtures, assertions, baselines? |
| Dependencies | packages, providers, version conflicts? |
| Config / ops | env vars, flags, rollout, observability? |

**Exit:** first-order map complete.

### 3. Trace the consequence chain

For each impacted area:

- If this changes, what else must change?
- Which callers or consumers assume the old shape?
- What follow-on work is required for completeness?

Trace **2–3 concrete steps** outward. Go deeper only while the chain stays grounded.

**Exit:** numbered forward chain with evidence or explicit assumptions.

### 4. Surface risks and gaps

Look for: forgotten implementation steps; implied migrations/backfills; compatibility traps; rollout hazards; unhandled new states; misleading tests; cross-service coordination cost.

**Exit:** risks labeled; assumptions stated.

### 5. Separate required from optional

| Class | Meaning |
| --- | --- |
| Mandatory for correctness | Must happen or the change is wrong |
| Mandatory for compatibility | Must happen or consumers break |
| Recommended | Safety, observability, operability |
| Optional cleanup | Not a blocker unless it really is |

**Exit:** follow-on work classified.

## Evidence Rules

- Forward, not backward.
- Code and contracts are truth; docs are claims.
- Two or three solid steps beat a long speculative chain.
- State assumptions behind each consequence.
- Label unproven impact as **likely**, not certain.

## Output Format

1. **Summary** — proposal and overall impact in one short paragraph
2. **Consequence Chain** — numbered forward steps
3. **Impact Assessment** — bullets or compact table by area
4. **Required Follow-On Work** — must-happen changes
5. **Risks And Gaps** — underspecified or dangerous parts
6. **Questions** — what still needs clarification
7. **Recommendation** — ready, incomplete, or risky; one short paragraph

## Handoffs

| Finding | Next step |
| --- | --- |
| Proposal ready to implement | `delivery`, direct implementation, or `factory` |
| Fuzzy goal needs grounding | `goal-forge` |
| Multi-track coordination needed | `campaign` |
| Observed failure needs diagnosis | Diagnose the failure read-only first (reproduce, trace, find the cause) |
| Structural fix needed in existing code | `cleanliness` |
| Intentional compatibility removal | Remove the stale compatibility paths instead of keeping aliases |