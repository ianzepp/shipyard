# Poker-Face Procedure

Detailed audit mechanics. The skill's `SKILL.md` owns gate rules, factory placement, and output format.

## 1. Reconstruct The Target Cold

Reread the original target material before reading the implementer's completion summary.

Write a short summary of what "done" means for this slice. Use the delivery spec or checkpoint target when available. The target must be concrete enough that a second reader can compare it against the diff.

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

Use an independent evaluator agent when delegation is available and allowed.

If a subagent cannot be used, perform a separate evaluator pass and report:

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

- any high miss → requirements missed; return to implementation
- any medium miss without explicit accepted deferral → requirements missed; return to implementation
- unverified requirement affecting a core promise → classify as high or medium; return to implementation
- only low misses or accepted deferrals → gate may clear
- completion estimate below `95%` with no high/medium misses → explain why the gate still clears, or return to implementation

Do not clear the gate on percentage alone when high or medium misses exist.

## 6. Fix And Rerun When Required

If high or medium misses remain:

- identify missing requirements by checklist item
- implement the missing work
- update or rerun validation
- rerun poker-face from the original target, not from the fix summary
- continue until requirements clear, only low misses remain, or a real blocker requires user input

Do not declare victory on a known miss.