# Correctness Mode

Use this reference when `factory` is already active and the selected phase is primarily bug-fixing, safety hardening, or reliability work.

This mode is for deep correctness work, not general cleanup.

## Focus

Prioritize:

- wrong output
- silent data loss
- invariant violations
- race conditions and async ordering bugs
- cancellation and lifecycle inconsistencies
- bad error propagation
- unsafe or unsound boundary handling
- logic that disagrees with tests, docs, or repository intent

Global rules:

- focus on correctness, not style
- fix root causes, not symptoms
- keep findings severity-driven
- use the project's own conventions and tests to validate fixes

## Mode Selection

Inside factory, this is normally an update-and-fix mode because the phase is already in execution. When the user clearly wants read-only diagnosis first, prefer the delivery-level root-cause behavior before entering implementation.

## Phase 0: Orient

1. Detect the primary language and toolchain from repository files.
2. Read repository guidance files first.
3. Inspect the dirty state before making fixes.
4. Identify the exact scope of the selected phase.
5. State the detected language, scope, and validation plan before editing.

## Analyze Before Editing

Perform a focused correctness review of the scoped area before changing code.

Use tests, grep, and nearby modules to establish how the code is supposed to behave before changing anything.

## Fix The Real Bugs

Fix:

- all critical findings
- all high findings
- medium findings only when the fix is clearly correct and surgical

Do not widen into cleanup, formatting theater, or architecture refactors unless they are required to make the correctness fix honest.

If a large design problem is the root cause, either:

- make the smallest safe corrective change now, or
- note that a later structural pass is needed

## Validate Hard

Run the strongest repo-native validation that matches the changed scope.

Typical defaults:

- Rust: `cargo test`, `cargo clippy --all-targets -- -D warnings`
- TypeScript / JavaScript: project test command, typecheck, and lint when the fix touched typed or runtime boundaries
- Go: `go test ./...`, `go test -race ./...` when concurrency is in play, `go vet ./...`
- Python: project test command plus configured type checker or lint when relevant

## Report Back Into Factory

Feed the results into the phase ledger:

- what was wrong
- what was fixed
- what was validated
- any remaining risks or deferred structural issues

If no actionable findings were found, say so plainly and note any residual blind spots.
