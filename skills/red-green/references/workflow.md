# Red-Green Workflow

Detailed mechanics for the red-green loop. Load when executing a run; the skill's `SKILL.md` owns mode selection, hard rules, and clearance.

## 1. Audit Current Test Coverage

Build a factual baseline before changing code.

| Mode | Scope |
| --- | --- |
| Broad | Map the subsystem or package; identify broad blind spots |
| Incremental | Map the changed surface and immediate neighboring tests and modules |

Check: test runners and coverage tooling; which packages/modules/directories have tests; untested or weak critical paths; whether existing coverage data is current enough to trust.

If no reliable coverage report exists, infer the baseline from repo structure and existing tests. Name important untested surfaces plainly.

Record as `Coverage Baseline`: current test surface, blind spots, candidate modules, baseline failures or ambient uncertainty.

## 2. Audit Decomposition And Testability

Before writing tests, inspect structure that blocks clean unit testing.

Look for: hidden mutable state; singleton or global dependencies; time, randomness, I/O, process, or network in core logic; oversized functions mixing orchestration and decision logic; constructors that do too much; branches reachable only through awkward setup.

Decide where code needs decomposition to: separate pure logic from effects; inject dependencies; isolate state transitions; make branches unit-testable without heroic fixtures.

Produce a concrete decomposition plan, not generic advice. Record as `Testability Findings`.

## 3. Wave 1: Author Aggressive Unit Tests

Spawn one or more worker agents with disjoint ownership.

Ownership rules:

- define `Wave 1 Ownership Map` before spawning
- each owned surface has a clear file or module boundary
- do not split work so finely that multiple agents edit the same seam
- in Incremental mode, use the smallest agent count that preserves independence

Each worker must:

- own a clear module, package, or file set
- add aggressive unit coverage for happy, sad, and edge cases
- prefer small deterministic fixtures over broad integration setup
- note assumptions inline when behavior is ambiguous
- not run tests (standalone; inside factory the tests are run at slice sign-off, see `SKILL.md`)

Target cases: success paths; invalid inputs; boundary values; nil/null handling; empty collections; ordering sensitivity; error propagation; retry, timeout, or fallback logic when locally unit-testable.

## 4. Wave 2: Verify Wave 1

Spawn independent agents to review newly added tests.

Rules:

- Wave 2 agents must not verify their own authored surface
- verify against implementation contract and stated target surface
- in Incremental mode, keep verification local unless drift was introduced
- record findings and repairs as `Wave 2 Audit Notes`
- do not run tests (standalone; inside factory see `SKILL.md`)

These agents must: verify tests match the implementation contract; catch invented behavior, brittle assertions, unreachable setup; tighten naming and case structure; fix obviously wrong or malformed tests.

## 5. Run Tests And Record Failures

After both writing passes, run relevant tests. Inside factory, authored tests are accepted as slices per the [workflow](../../factory/SKILL.md#workflow), and each slice's tests are run at its sign-off instead, with the `red_first` record kept in the ledger ([slice runner](../../factory/references/loop.md#running-a-slice-list)). For new behavior or a bug fix, run the new test first against the unfixed code (on a brand-new module, stub the interface first so the test fails on behavior, not on a missing import) and record that it fails for the right reason (the missing behavior or the bug itself). If it passes, or fails for another reason, the test is wrong: fix the test before touching the implementation. Then apply the fix and run in this order:

1. targeted tests for newly changed surfaces
2. adjacent package or module tests if cheap
3. broader relevant suite

| Mode | Widen scope |
| --- | --- |
| Broad | From targeted runs to broader subsystem or suite |
| Incremental | Only as far as risk profile justifies |

Record as `Failure Ledger`: command run; the red result observed before the fix and why it failed; pass/fail; whether failures were pre-existing, newly introduced, or ambiguous. Do not collapse failures into one bucket.

## 6. Loop Until Honestly Resolved

Classify each failure:

- test is wrong
- implementation is wrong
- structure blocks honest tests and needs decomposition
- environment is broken or baseline was already red

Act accordingly: fix test; fix implementation; decompose; rerun affected tests, then broader suite.

Stop when: relevant suite is green; remaining failures are clearly pre-existing and documented; work is blocked by scope boundary.

Every iteration updates `Failure Ledger` with: failing test or suite; classification; action taken; rerun scope; outcome.

## Delegation Pattern

| Wave | Role |
| --- | --- |
| 1 | Worker agents write tests for disjoint owned surfaces |
| 2 | Separate agents verify Wave 1 outputs and repair tests without executing them |

Do not use the same agent for authorship and verification of the same surface unless delegation is unavailable. Without delegation, run Wave 2 as a self-contained cold pass: set aside your authoring notes, re-read the tests against the implementation contract and target surface only, and report `Evaluator mode: self-contained cold pass` in `Wave 2 Audit Notes`. Scale delegation to the mode and ownership map.

## Triage Standard

- Test contradicts intended behavior → fix the test.
- Implementation contradicts intended behavior → fix the implementation.
- Intended behavior cannot be tested cleanly → fix the design seam first.
- Intended behavior unknown → say so explicitly; mark ambiguity.

Truth over momentum. Wrong green tests are worse than red ones.

## Output Format

Report in this order:

1. **Mode And Target Surface** — broad or incremental; named surface
2. **Coverage Audit** — current surface; blind spots; target modules; baseline status
3. **Decomposition Audit** — testability blockers; seams to extract or isolate
4. **Wave 1** — agents; owned surfaces; tests added
5. **Wave 2** — agents; verification findings; test fixes
6. **Test Run** — commands; pass/fail summary; notable failures
7. **Loop Result** — implementation fixes; test fixes; remaining blockers
8. **Clearance Decision** — cleared, not cleared, or blocked; short reason

## Vocabulary

Prefer: broad mode; incremental mode; target surface; coverage audit; blind spots; baseline status; decomposition seam; state leakage; owned surface; wave 1 authorship; wave 2 verification; honest failure; failure ledger; test bug; implementation bug; design-for-testability blocker; clearance gate.