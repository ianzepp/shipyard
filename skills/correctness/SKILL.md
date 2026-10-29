---
name: "correctness"
description: "Hunt behavioral bugs, invariant breaks, races, and data-loss risks."
---

# Correctness

Deep correctness work: find or fix real behavioral bugs and correctness risks. Not general cleanup.

Also a factory internal mode. Factory reference: [correctness-mode](../factory/references/correctness-mode.md).

## Role In The Stack

| Skill | Question |
| --- | --- |
| `correctness` | Does the code behave correctly? |
| [`poker-face`](../poker-face/SKILL.md) | Does the work satisfy every promised requirement? |
| Read-only diagnosis | What caused the failure before any fix? |

A factory phase can satisfy requirements (`poker-face`) and still be behaviorally wrong (`correctness`). Both must clear before checkpoint.

## Factory Phase Use

Inside [factory](../factory/SKILL.md), correctness runs twice: as the correctness read of each slice's own changes at slice sign-off (isolated per the [workflow](../factory/SKILL.md#workflow)), and in the phase gate's review over the phase change set. Factory's [order](../factory/SKILL.md#order) is the canonical sequence.

- **Sign-off read is read-only.** Report findings by severity; make no edits. Any CRITICAL or HIGH finding (P0/P1, see [verdicts and severity](../factory/SKILL.md#verdicts-and-severity)) sends the slice back to its implementer; MEDIUM and LOW go to the ledger as notes.
- **Gate review is read-only too.** Its findings go to [slicer](../slicer/SKILL.md#modes) rework mode (a); the repair slices run through sign-off, then the affected gate checks are rerun (see the [phase gate](../factory/references/loop.md#phase-gate)).
- **Update mode is for correctness-mode phases** (a phase that is primarily bug-fixing or reliability hardening). Even there, the fixes run as slices with sign-off, not as ad-hoc edits. When the user clearly wants read-only diagnosis first, diagnose read-only first (find the cause before any fix).

Scope to the active **factory phase** change set (everything since the phase base) and its delivery spec. Feed results into the phase ledger: what was wrong, fixed, validated, and any deferred structural issues.

Use **Correctness Mode** inside factory when the phase is primarily bug-fixing, reliability hardening, or a user-requested correctness pass with fixes.

## Global Rules

- Focus on correctness, not style.
- Prioritize real failure modes: wrong output, silent loss, corruption, races, hangs, API misuse, broken invariants.
- Fix root causes, not symptoms.
- Severity-driven: critical and high first; medium only when clearly surgical.
- Use repo conventions and tests to validate fixes.
- If the repo has a hygiene ratchet, account for it when removing tracked debt patterns.

## Mode Selection

| Mode | Use when | Do |
| --- | --- | --- |
| **Read-only** | Review, audit, bug hunt, assessment, report, or "correctness pass" without explicit fix request | Report findings by severity; no file edits; non-mutating validation only |
| **Update** | Fix, patch, address, implement, repair, or scoped failing tests | Analyze first; fix critical/high by default; medium only when surgical; validate |

If wording is ambiguous: read-only for broad audits; update for scoped bug reports or failing tests.

## Domain Split

For a broad pass over a whole project, split it into logical domains and review one domain at a time. If your tool supports subagents, you may run one per domain; otherwise work through the domains serially and say so in the report.

Suggested domains:

- API boundaries, routing, auth, input validation
- Persistence, migrations, transactions, data integrity
- Concurrency, background jobs, lifecycle, cancellation, resource cleanup
- Domain invariants, state transitions, business rules
- Serialization, parsing, protocol compatibility, external integrations
- Tests, fixtures, mocks, validation gaps hiding regressions

Per domain: bounded scope; correctness findings only; mode-appropriate write scope; severity, file/line, reproduction reasoning, recommended fix; distinguish confirmed bugs from plausible risks.

Overall: deduplicate by root cause; promote only concrete source-grounded issues; apply fixes in priority order in update mode; report domain coverage.

## Workflow

### Step 0: Orient

1. Detect language and toolchain from manifests.
2. Read `AGENTS.md`, `CLAUDE.md`, `README.md`, and repo tooling docs.
3. Inspect dirty state. Do not trample unrelated local changes.
4. Identify scope: changed files, named subsystem, or failing area from tests/reports.
5. State language, scope, selected mode, and validation plan before editing.

### Step 1: Load The Language Lens

- Rust: [correctness-rs](references/correctness-rs.md)
- TypeScript / JavaScript: [correctness-ts](references/correctness-ts.md)
- Go: [correctness-go](references/correctness-go.md)
- Python: [correctness-py](references/correctness-py.md)

Multi-language repos: apply per component. Unsupported language: narrower manual pass.

### Step 2: Analyze Before Editing

Prioritize: silent data loss; incorrect fallbacks; invariant violations; races and async ordering; cancellation/lifecycle bugs; bad error propagation; unsafe boundaries; logic disagreeing with tests, docs, or intent.

Establish expected behavior from tests, grep, and nearby modules before changing anything.

### Step 3: Fix The Real Bugs

Skip in read-only mode.

Fix: all critical; all high; medium only when clearly surgical.

Do not widen into cleanup, formatting, or architecture refactors unless required for an honest fix.

Large design root cause: smallest safe corrective change now, or recommend `consequences` if structural redesign exceeds scope.

### Step 4: Validate Hard

Read-only: non-mutating reproduction and inspection. Update: strongest repo-native validation matching scope.

Typical defaults (inside factory, run the narrowest scope that proves the change and widen at checkpoints):

- Rust: the narrowest `cargo test` scope that proves the change (`cargo test -p <crate>`; widen when the change crosses crates), `cargo clippy --all-targets -- -D warnings`
- TypeScript / JavaScript: project test, typecheck, lint on touched boundaries
- Go: `go test` on the touched packages (`./...` at checkpoints), `go test -race ./...` when concurrency matters, `go vet ./...`
- Python: project tests plus type checker or lint when relevant

Lower hygiene ratchet budgets when tracked debt was reduced.

### Step 5: Report Clearly

Report: selected mode; domain split used (serial or subagents); what was wrong; what was fixed; what was validated; remaining risks or deferred structural issues.

If no actionable findings, say so plainly and note residual blind spots.