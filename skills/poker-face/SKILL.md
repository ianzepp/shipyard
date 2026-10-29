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
- route material misses to rework: inside factory, to [slicer](../slicer/SKILL.md) rework mode (a); standalone, back to implementation

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

Mandatory at the phase gate inside [factory](../factory/SKILL.md) whenever a goal, spec, or acceptance criteria exist; equally usable standalone. It runs over the [phase change set](../factory/references/loop.md#phase-gate) (committed, or signed off and staged, per the commit unit), after verification and before review; see factory's phase loop for the full sequence.

Rules when used in a factory phase:

- Compare against: factory phase boundary, saved delivery spec, acceptance criteria, the phase's commits and changed files, validation results, residual correctness risks.
- Any **high miss** → gate cannot pass; send the misses to slicer rework mode (a).
- Any **medium miss** → gate cannot pass unless deferring it has the user's approval or the plan already names it as deferred. Surface each medium miss to the user before the gate passes; on approval, record it in the ledger as a deferred finding (owner and done-when). A medium miss that breaks an acceptance criterion is never deferrable.
- **Unverified core requirement** → gate cannot pass until verified or downgraded with evidence.
- Only **low misses** or approved deferrals → continue toward the checkpoint.
- **Misses are repaired through rework.** Slicer cuts repair slices from the misses; the repair slices go through sign-off, and the affected gate parts (verification, poker-face, review) rerun. See factory's [phase gate](../factory/references/loop.md#phase-gate). Standalone use, outside factory, may simply return to implementation.
- **Completion estimate is secondary.** Miss classification blocks; percentage alone does not clear the gate.
- Skip poker-face only when no goal, spec, or acceptance criteria exist; record the skip reason, or the verdict and evaluator mode, in the Checkpoint section of the [ledger](../factory/references/loop.md#ledger-file). "Delegation unavailable" or "too costly" is not a skip reason: with no subagent, run a self-contained cold pass (procedure step 4) and report `Evaluator mode: self-contained cold pass`.
- Poker-face does not replace correctness. A phase can satisfy requirements on paper and still be behaviorally wrong.

## When To Use

Use when:

- an implementation pass appears complete
- a written requirement, issue, plan, delivery spec, acceptance criteria, or checkpoint target exists
- a factory phase is at its phase gate, before the checkpoint
- you need a cold audit of whether produced work meets the target

Do not use when:

- scope is still changing
- no concrete requirement or checkpoint exists
- implementation has not reached a plausible stopping point
- the user asked for correctness review, root-cause analysis, or architecture review instead

## Hard Rules

- Do not start until the original plan, issue, delivery spec, acceptance criteria, or checkpoint target is in hand.
- The original plan is source of truth. The implementer's summary, commit message, changed-file list, and validation notes are evidence, not authority.
- Reconstruct a checklist of every promised behavior, file, command, workflow, migration, test, documentation change, and explicit non-goal that matters to the work under audit.
- Inspect actual repository state for each item. Changed files are clues, not proof.
- Prefer direct evidence: code paths, tests, generated artifacts, command output, docs, configs, schemas, routes, APIs, CLI behavior, committed files.
- Mark every item: `SATISFIED`, `PARTIAL`, `MISSING`, `UNVERIFIED`, or `NOT APPLICABLE`.
- Classify every `PARTIAL`, `MISSING`, and `UNVERIFIED` item as `HIGH`, `MEDIUM`, or `LOW`.
- **HIGH** — core promised outcome absent, broken, unverified where verification was required, or in the wrong place.
- **MEDIUM** — supporting behavior, edge case, test, doc, integration, or cleanup absent enough that a fresh reviewer would call the work incomplete.
- **LOW** — polish, wording, minor cleanup, or non-blocking gap.
- Any **HIGH** miss blocks completion.
- Any **MEDIUM** miss blocks completion unless the user approved deferring it, or the plan already names it as deferred. Surface it before the gate passes, then record it as a deferred finding in the ledger (named follow-up with owner and done-when). A MEDIUM miss that breaks an acceptance criterion always blocks.
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
- `Follow-Ups Already Accepted`: deferrals the user approved or the plan names, which should not block this phase

If any field is unavailable, say so instead of inventing evidence.

## Procedure

Run the six steps in [procedure](references/procedure.md):

1. Reconstruct the target cold
2. Build the requirement checklist
3. Inspect actual evidence
4. Run the independent audit
5. Score the result (miss classification authoritative)
6. Fix and rerun when required

## Output Format

1. **Poker Face** — evaluator mode; high/medium/low misses; unverified requirements; completion estimate (secondary)
2. **Verdict** — `CLEARED` or `NOT CLEARED`; blocking reason if not cleared. Factory maps these to its gate results in its [verdict and severity table](../factory/SKILL.md).
3. **Why** — one short paragraph on what drove the result
4. **Requirement Checklist** — compact checklist with status markers
5. **Missing Work** — every high and medium miss; low misses worth tracking
6. **Next Step** — the checkpoint, rework (inside factory, slicer rework mode (a); standalone, return to implementation), or pause for a blocking decision