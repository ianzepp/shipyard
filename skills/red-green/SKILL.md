---
name: "red-green"
description: "Drive serious testability and coverage work through red-green loops."
---

# Red Green

Push a codebase through an honest test-first tightening cycle: map the test surface, find testability blockers, run a two-wave agent authoring and verification pass, execute tests only after both passes, and loop until failures are correctly assigned.

Used inside [factory](../factory/SKILL.md) or standalone. Detailed step mechanics: [workflow](references/workflow.md).

## When To Use

Use when:

- the user wants broader or deeper automated unit coverage
- logic is entangled with state or side effects
- you want aggressive happy/sad/edge unit tests with a two-pass agent workflow
- the goal is a real failing-or-green result, not an unverified patch

Do not use when:

- the user only wants one targeted test, or the change is a single new behavior or bug fix (factory's red-first sign-off already covers that; red-green is for testability and coverage programs)
- work is primarily integration, UI, or end-to-end coverage
- the code cannot be exercised without environment setup outside scope
- the repo is too unstable to separate test failures from ambient breakage

## Modes

Choose one before the audit:

| Mode | Use when | Boundary |
| --- | --- | --- |
| **Broad** | Broad coverage push across a subsystem, package, or part of the repo | Subsystem or package boundary is known |
| **Incremental** | Bounded change, issue, PR, or local failing surface | Changed files, issue scope, PR diff, or failing surface is known |

## Hard Rules

- Complete coverage and decomposition audits before writing tests.
- When delegation is available: Wave 1 authors tests; Wave 2 verifies; they must not be the same agent for the same surface.
- Standalone: do not run tests during Wave 1 or Wave 2. Inside factory the waves still decide who authors and who verifies, but the authored tests land as slices and are run at sign-off (see Inside Factory).
- Red first: for new behavior or a bug fix, run the new test before the fix and record that it fails for the right reason (the missing behavior or the bug, not a typo or broken setup). A test never seen failing proves nothing. Inside factory this is the slice brief's `red_first: yes` field (see Inside Factory).
- Without delegation, Wave 2 is a self-contained cold pass: re-read the Wave 1 tests against the implementation contract only, not your authoring notes, and report `Evaluator mode: self-contained cold pass`.
- Keep agent ownership boundaries explicit so parallel workers do not collide in the same files.
- Treat decomposition findings as implementation work when they block testability.
- On failure, classify test bug vs implementation bug vs design blocker. Do not guess.
- Do not declare success on tests that were never executed.
- Separate ambient failures from failures introduced by this effort.

## Inside Factory

Red-green inside [factory](../factory/SKILL.md) produces or feeds slices (see [red-green-mode](../factory/references/red-green-mode.md)):

- Authored tests and any testability refactors run as slices through [slice sign-off](../factory/references/loop.md#running-a-slice-list), not as ad-hoc edits.
- Tests are run at sign-off, never left unexecuted. For a slice whose brief says `red_first: yes`, the runner writes the test, runs it, confirms it fails for the stated reason, records a summary of the failing output in the [ledger](../factory/references/loop.md#ledger-file), and only then lets the implementation change land. Sign-off checks that record.
- Run the narrowest scope that proves the slice; widen at the phase gate and checkpoints, not per slice.
- Wave 2 without delegation is the same self-contained cold pass, with the `Evaluator mode` line above.

## Entry Conditions

Establish before starting:

- named `Target Surface`
- intended behavior contract, or limits of what is known
- test runner and at least one relevant test command
- baseline status of the target surface (including "unknown because environment is broken")

Stop or mark blocked if: intended behavior is too ambiguous; target surface cannot be named; environment too broken to classify failures; test runner cannot be identified.

## Required Artifacts

Maintain explicitly:

1. `Target Surface`
2. `Coverage Baseline`
3. `Testability Findings`
4. `Wave 1 Ownership Map`
5. `Wave 2 Audit Notes`
6. `Failure Ledger`
7. `Clearance Decision`

## Workflow

Run the steps in [workflow](references/workflow.md):

1. Audit current test coverage → `Coverage Baseline`
2. Audit decomposition and testability → `Testability Findings`
3. Wave 1: author aggressive unit tests
4. Wave 2: verify and repair tests (no test execution)
5. Run tests → `Failure Ledger`
6. Loop until honestly resolved

## Clearance Gate

End every run with `Clearance Decision`:

| Decision | Meaning |
| --- | --- |
| `CLEARED` | Target surface is honestly covered; new failures resolved or classified |
| `NOT CLEARED` | Unresolved test, implementation, or testability defects remain in scope |
| `BLOCKED` | Ambiguity, environment failure, or boundary constraints prevent honest completion |

Mode-specific bar:

- **Broad**: named subsystem or package has materially improved honest coverage; remaining failures classified
- **Incremental**: changed or failing surface is honestly covered; no unexplained adjacent regression