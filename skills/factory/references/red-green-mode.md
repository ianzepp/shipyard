# Red-Green Mode

Use this reference when `factory` is already active and the selected phase needs serious testability improvement or coverage expansion.

This is not just "add some tests." Its purpose is to tighten the code honestly:

- map the real current test surface
- identify where state, side effects, and coupling make testing harder than they should be
- expand tests aggressively
- run the tests after the writing passes
- loop until failures are correctly assigned to the implementation or the tests

## When To Use

Use this mode when:

- the user wants broader or deeper automated test coverage
- the code is hard to test because logic is entangled with state or side effects
- you want happy, sad, and edge case unit tests written aggressively
- the goal is to end with real failing-or-green test results, not unverified patches

Do not use it when:

- the user only wants one targeted test added
- the work is primarily integration, UI, or end-to-end coverage instead of unit-testability
- the repository is too unstable to distinguish test failures from ambient breakage

## Hard Rules

- Choose Broad mode or Incremental mode (see [red-green](../../red-green/SKILL.md)) before starting the audit.
- Step order matters. Do not skip ahead to writing tests before the coverage and decomposition audits are done.
- When delegation is available, use independent passes rather than treating the first draft of tests as final.
- Do not declare success on added tests that were never executed.
- Preserve the baseline. Separate ambient failures from failures introduced by the testing effort.

## Entry Conditions

Before starting, establish:

- the named `Target Surface`
- the intended behavior contract, or the limits of what is actually known
- the test runner and at least one relevant test command
- the baseline status of the target surface

Stop or mark the effort blocked if:

- intended behavior is too ambiguous to write honest tests
- the target surface cannot be named
- the environment is too broken to classify failures meaningfully
- the test runner cannot be identified

## Workflow

### 1. Audit Current Test Coverage

Build a factual baseline before changing code.

Record:

- current test surface
- likely blind spots
- candidate modules for aggressive unit coverage
- baseline failures or ambient uncertainty

### 2. Audit Decomposition And Testability

Inspect the implementation for structure that prevents clean unit testing.

Look for:

- hidden mutable state
- singleton or global dependencies
- time, randomness, I/O, process, or network calls embedded in core logic
- oversized functions mixing orchestration and decision logic
- constructors or setup paths that do too much work

This step should produce a concrete decomposition plan, not generic advice.

### 3. First Pass: Author Aggressive Unit Tests

Prefer disjoint ownership if using agents.

Bias toward:

- expected success paths
- invalid inputs
- boundary values
- null or nil handling
- empty collections and degenerate states
- ordering sensitivity
- error propagation
- retry, timeout, or fallback logic when locally unit-testable

### 4. Second Pass: Verify The First Pass

Review the newly added tests independently when possible.

Check for:

- invented behavior
- brittle assertions
- unreachable setup
- shallow assertions
- tests that only look comprehensive

### 5. Run The Tests And Classify Failures

After both writing passes are complete, run the relevant tests.

Preferred order:

1. targeted tests for the newly changed surfaces
2. adjacent package or module tests if cheap
3. the broader relevant suite

Record:

- what command was run
- what passed
- what failed
- whether failures were pre-existing, newly introduced, or ambiguous

## Clearance Decision

At the end of the loop, decide whether:

- the surface is now sufficiently hardened
- the implementation needs additional decomposition
- a failing test exposed a real product bug that must be fixed before the phase can pass

Feed that decision back into the main factory phase ledger.
