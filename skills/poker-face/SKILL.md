---
name: "poker-face"
description: "Audit completed work against promised requirements and missed items."
---

# Poker Face

Completion gate for requirement truth, not behavioral correctness. Ask whether the implemented change satisfies the original promise — not whether the implementer's summary sounds complete.

Cold-reader miss discovery:

- reread the original plan, issue, delivery spec, acceptance criteria, or checkpoint target
- reconstruct a requirement checklist
- compare each item against actual repository state
- classify high, medium, and low misses
- return to implementation when material misses remain

Not a broad code review, architecture critique, or replacement for [$correctness](../correctness/SKILL.md).

## Role In The Stack

| Skill | Question |
| --- | --- |
| `delivery` | Is there an implementation-ready delivery spec? |
| `correctness` | Does the code behave correctly? |
| `poker-face` | Does the work satisfy every promised requirement? |
| factory review pass | Does the diff hold up as a read-only review (scope, boundaries, evidence honesty)? |
| `cleanliness` | Is complexity shaped into maintainable structure? |
| `factory` | Did the factory phase pass its checkpoint gate? |

## Factory Phase Use

Optional but preferred inside [factory](../factory/SKILL.md), and equally usable standalone. Inside factory it runs after implementation, **correctness**, and verification, and before review; see factory's phase loop for the full sequence.

Rules when used in a factory phase:

- Compare against: factory phase boundary, saved delivery spec, acceptance criteria, changed files, validation results, residual correctness risks.
- Any **high miss** → gate cannot pass; return to implementation.
- Any **medium miss** without explicit accepted deferral → gate cannot pass; return to implementation.
- **Unverified core requirement** → gate cannot pass until verified or downgraded with evidence.
- Only **low misses** or accepted follow-ups → continue toward checkpoint evaluation.
- **Completion estimate is secondary.** Miss classification blocks; percentage alone does not clear the gate.
- Skipping poker-face is allowed when delegation is unavailable, too costly, or not useful — record the skip reason in checkpoint evaluation.
- Poker-face does not replace correctness. A phase can satisfy requirements on paper and still be behaviorally wrong.

## When To Use

Use when:

- an implementation pass appears complete
- a written requirement, issue, plan, delivery spec, acceptance criteria, or checkpoint target exists
- a factory phase is about to enter checkpoint evaluation
- you need a cold audit of whether produced work meets the target

Do not use when:

- scope is still changing
- no concrete requirement or checkpoint exists
- implementation has not reached a plausible stopping point
- the user asked for correctness review, root-cause analysis, or architecture review instead

## Hard Rules

- Do not start until the original plan, issue, delivery spec, acceptance criteria, or checkpoint target is in hand.
- The original plan is source of truth. The implementer's summary, commit message, changed-file list, and validation notes are evidence, not authority.
- Reconstruct a checklist of every promised behavior, file, command, workflow, migration, test, documentation change, and explicit non-goal that matters to the slice.
- Inspect actual repository state for each item. Changed files are clues, not proof.
- Prefer direct evidence: code paths, tests, generated artifacts, command output, docs, configs, schemas, routes, APIs, CLI behavior, committed files.
- Mark every item: `SATISFIED`, `PARTIAL`, `MISSING`, `UNVERIFIED`, or `NOT APPLICABLE`.
- Classify every `PARTIAL`, `MISSING`, and `UNVERIFIED` item as `HIGH`, `MEDIUM`, or `LOW`.
- **HIGH** — core promised outcome absent, broken, unverified where verification was required, or in the wrong place.
- **MEDIUM** — supporting behavior, edge case, test, doc, integration, or cleanup absent enough that a fresh reviewer would call the slice incomplete.
- **LOW** — polish, wording, minor cleanup, or non-blocking gap.
- Any **HIGH** miss blocks completion.
- Any **MEDIUM** miss blocks completion unless explicitly moved to a named follow-up by the user or phase plan.
- Completion estimate is secondary. It must not clear the gate when high or medium misses exist.
- List every miss. Do not collapse into "largest missing requirement."
- Mark `UNVERIFIED` and classify the risk when evidence is insufficient.

## Audit Packet

Assemble before evaluation. A cold reader must be able to rerun the audit from this packet.

- `Original Target`: user request, issue, roadmap item, factory phase name
- `Delivery Spec`: saved artifact path, if one exists
- `Acceptance Criteria`: expected outputs and checkpoint target
- `Out Of Scope`: exclusions that should not count against completion
- `Requirement Checklist`: reconstructed before judging implementation
- `Repo State`: `git status`, relevant diff or commits, changed files
- `Validation`: commands run, results, skipped checks
- `Known Residual Risks`: risks from correctness or verification
- `Follow-Ups Already Accepted`: named deferrals that should not block this phase

If any field is unavailable, say so instead of inventing evidence.

## Procedure

Run the six steps in [$procedure](references/procedure.md):

1. Reconstruct the target cold
2. Build the requirement checklist
3. Inspect actual evidence
4. Run the independent audit
5. Score the result (miss classification authoritative)
6. Fix and rerun when required

## Output Format

1. **Poker Face** — evaluator mode; high/medium/low misses; unverified requirements; completion estimate (secondary)
2. **Verdict** — `CLEARED` or `NOT CLEARED`; blocking reason if not cleared
3. **Why** — one short paragraph on what drove the result
4. **Requirement Checklist** — compact checklist with status markers
5. **Missing Work** — every high and medium miss; low misses worth tracking
6. **Next Step** — checkpoint evaluation, return to implementation, or pause for blocking decision