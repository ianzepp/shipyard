# Poker-Face Procedure

Detailed audit mechanics. The skill's `SKILL.md` owns gate rules, factory placement, and output format.

## 1. Reconstruct The Target Cold

Reread the original target material before reading the implementer's completion summary.

Write a short summary of what "done" means for this work. Use the delivery spec or checkpoint target when available. The target must be concrete enough that a second reader can compare it against the diff.

## 2. Build The Requirement Checklist

Convert the target into a checklist before scoring implementation.

Include:

- user-visible behavior promised by the plan
- internal behavior required to make that promise true
- files, modules, commands, docs, tests, configs, migrations, data, or generated artifacts explicitly named
- acceptance criteria and checkpoint conditions
- non-goals and accepted follow-ups

Do not omit checklist items because you believe they were probably handled. The checklist is the audit surface.

## 3. Inspect Actual Evidence

For each checklist item, inspect actual repository state.

Use direct reads and commands where practical:

- read the plan, delivery spec, and affected files
- inspect `git status` and the relevant diff or commits
- run or review validation evidence
- search for named APIs, routes, flags, files, tests, fixtures, docs, migrations, and examples
- verify generated artifacts or runtime behavior when the requirement depends on them

Do not accept "changed file X" as proof that requirement Y is satisfied. Point to the exact evidence.

## 4. Run The Independent Audit

Poker-face is mandatory at the phase gate when a goal, spec, or acceptance criteria exist. It is skipped only when none exist, with the reason recorded in the Checkpoint section of the [ledger](../../factory/references/loop.md#ledger-file). Delegation being unavailable or costly is not a reason to skip.

Use an independent evaluator agent when your tool supports subagents.

With no subagent, run a self-contained cold pass instead: write the requirement checklist from the plan and acceptance criteria before reading any summary, ledger, or commit message, then inspect the committed range against it. Report:

- `Evaluator mode: self-contained cold pass`
- why no subagent was used

The evaluator receives the audit packet and must return:

- `Checklist results`: every requirement marked `SATISFIED`, `PARTIAL`, `MISSING`, `UNVERIFIED`, or `NOT APPLICABLE`
- `Misses`: every high, medium, and low miss with evidence
- `Completion estimate: NN%`, as a secondary summary only
- `Reasoning: 2-4 sentences`

The evaluator judges completion against requirements only. Code style, architecture preference, and unrelated cleanup do not affect the score unless they block a stated requirement.

The evaluator acts like a fresh session given the original plan and asked whether the plan was implemented correctly.

### Evaluator prompt shape

1. Provide the original plan, delivery spec, checkpoint target, and acceptance criteria.
2. State out-of-scope items and already accepted follow-ups.
3. Provide repo state pointers: changed files, relevant diff or commits, validation, and known residual risks.
4. Ask for: reconstructed checklist; checklist result for every item; high, medium, and low misses; unverified requirements; `Completion estimate: NN%`; `Reasoning: 2-4 sentences`.
5. Instruct the evaluator to behave like a fresh session asked whether the original plan was implemented correctly.
6. Instruct the evaluator to judge requirement completion, not style or general architecture.

Keep the prompt factual. Do not argue that the implementation is complete.

## 5. Score The Result

Calculate:

- `High misses`
- `Medium misses`
- `Low misses`
- `Unverified requirements`
- `Completion estimate` (secondary)

Interpretation — **miss classification is authoritative**:

- any high miss → requirements missed; route to rework (see step 6)
- any medium miss without an approved deferral (the user's approval, or the plan already naming it as deferred, surfaced before the gate passes) → requirements missed; route to rework
- unverified requirement affecting a core promise → classify as high or medium; route to rework
- only low misses or approved deferrals → gate may clear
- completion estimate below `95%` with no high/medium misses → explain why the gate still clears, or route to rework

Do not clear the gate on percentage alone when high or medium misses exist.

## 6. Fix And Rerun When Required

If high or medium misses remain:

- identify missing requirements by checklist item
- inside factory, hand them to [slicer](../../slicer/SKILL.md) rework mode (a); the repair slices go through sign-off, and the affected gate parts (verification, poker-face, review) rerun. Standalone, implement the missing work directly
- update or rerun validation
- rerun poker-face from the original target, not from the fix summary
- continue until requirements clear, only low misses remain, or a real blocker requires user input; inside factory, its [phase gate](../../factory/references/loop.md#phase-gate) rules cap the rework cycles

Do not declare victory on a known miss.