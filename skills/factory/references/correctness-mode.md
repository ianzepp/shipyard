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

Inside factory, this is normally an update-and-fix mode because the phase is already in execution. Its fixes run as slices: the analysis feeds [$slicer](../../slicer/SKILL.md) (or rework mode (a) for findings in an existing cut), and each fix is accepted through [slice sign-off](loop.md#running-a-slice-list), with `red_first: yes` for each bug fix. Do not make ad-hoc edits outside a slice. When the user clearly wants read-only diagnosis first, find the cause read-only before entering implementation.

This update mode is for correctness-mode phases only. The correctness read at slice sign-off stays read-only.

## Step 0: Orient

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

- all critical findings (≈ `P0`)
- all high findings (≈ `P1`)
- medium findings only when the fix is clearly correct and surgical

The severity mapping is in [factory's Verdicts and Severity](../SKILL.md#verdicts-and-severity).

Do not widen into cleanup, formatting theater, or architecture refactors unless they are required to make the correctness fix honest.

If a large design problem is the root cause, either:

- make the smallest safe corrective change now, or
- note that a later structural pass is needed

## Validate Hard

Run the strongest repo-native validation that matches the changed scope. Use the narrowest scope that proves the fix at slice sign-off, and widen at the phase gate and checkpoints (see [Verification scoping](loop.md#verification-scoping)).

Typical defaults, scoped to the touched package or module:

- Rust: `cargo test -p <crate>`, `cargo clippy -p <crate> --all-targets -- -D warnings`
- TypeScript / JavaScript: project test command on the touched files, typecheck, and lint when the fix touched typed or runtime boundaries
- Go: `go test ./<pkg>/...`, `go test -race ./<pkg>/...` when concurrency is in play, `go vet ./<pkg>/...`
- Python: project test command on the touched tests, plus configured type checker or lint when relevant

## Report Back Into Factory

Feed the results into the phase ledger:

- what was wrong
- what was fixed
- what was validated
- any remaining risks or deferred structural issues

If no actionable findings were found, say so plainly and note any residual blind spots.
