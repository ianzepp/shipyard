# Auditor Procedure

Detailed mechanics for a rigorous, rerunnable code and integration audit. The
parent `SKILL.md` owns role boundaries and verdict authority.

## Contents

1. Freeze the review surface
2. Assemble the audit packet
3. Inventory and map the change
4. Review by lens
5. Validate by risk
6. Challenge findings
7. Derive and report the verdict

## 1. Freeze The Review Surface

Record the review identity before reading the implementation narrative deeply:

```text
assignment or request
repository and owning checkout
base SHA
head SHA, or WORKTREE with status snapshot
named paths and explicit exclusions
done-when, specification, issue, or user request
risk reason and expected validation
```

Use full SHAs in the final report. For a branch, derive the base using the
assignment's target branch and verify the merge-base is intended. For a landed
range, verify both endpoints exist on the expected history. For uncommitted
work, record `git status --short`, staged and unstaged surfaces separately, and
do not silently include later edits.

If the assignment does not identify a stable range, report the ambiguity to
the requester. Review may proceed for useful findings, but verdict cannot be
`clean_pass` until identity is stable.

Inspect uncommitted changes you did not make rather than normalizing them. If
they overlap the review surface, state whether the range can still be
reconstructed exactly. Never stash, restore, reset, clean, or overwrite them.

## 2. Assemble The Audit Packet

The packet must let another reviewer reproduce the audit:

| Field | Evidence |
| --- | --- |
| Original target | Assignment, issue, user request, delivery spec, done-when |
| Intended behavior | Requirement checklist reconstructed before trusting the completion summary |
| Non-goals | Explicit exclusions and accepted deferrals |
| Repository state | Base/head, status, commits, diff stat, changed paths |
| Risk profile | Auth, tenancy, persistence, money, migration, concurrency, ingress, deploy, compatibility |
| Claimed evidence | Implementer commands/results, test names, artifacts, status claims |
| Known context | Existing failures, incident or bug report, dependent changes, rollout constraints |

Mark unavailable fields as unknown. Do not infer acceptance criteria from the
implementation when an authoritative target exists.

When the target includes multiple requirements, mark each:

```text
SATISFIED | PARTIAL | MISSING | UNVERIFIED | NOT_APPLICABLE
```

Use [poker-face](../../poker-face/SKILL.md) when reconstructing a complex completion checklist. The
auditor still owns behavioral and integration correctness beyond that checklist.

## 3. Inventory And Map The Change

Start with commit and path inventory, then inspect content:

- commits in the exact range, including merges
- diff stat and every changed, added, deleted, renamed, generated, or vendored path
- submodule, lockfile, manifest, workflow, infrastructure, migration, fixture,
  snapshot, schema, public API, and documentation changes
- suspicious omissions: expected tests, migrations, generated outputs, config,
  callers, or cleanup absent from the diff

For each changed production symbol, trace enough surrounding behavior to know:

- who calls it and what assumptions callers make
- what it calls and which failures cross that boundary
- which state, schema, protocol, or configuration it reads and writes
- which tests cover the old defect, new behavior, negative path, and rollback
- which deployed component or external consumer observes the change

Use searches and structured tooling appropriate to the language. A diff is an
index of edits, not the boundary of behavioral impact.

Maintain a lightweight coverage ledger:

```text
path/symbol | lens applied | callers/consumers checked | validation | disposition
```

Every assigned changed path must end as reviewed, explicitly excluded, or a
blind spot that affects the verdict.

## 4. Review By Lens

Apply all applicable parent-skill lenses. Load the matching [correctness](../../correctness/SKILL.md)
language reference for substantive code changes.

### Behavior and error semantics

- Compare expected and actual behavior on success, empty, boundary, malformed,
  partial-failure, timeout, retry, and cancellation paths.
- Trace returned, swallowed, wrapped, logged, retried, and fallback errors.
- Look for permissive fallback where policy requires failure.
- Check numeric limits, ordering, time zones, encoding, parsing, and default values.

### Invariants, authorization, and trust

- Name the invariant before judging the implementation.
- Verify enforcement at the authoritative boundary, not only in UI or callers.
- Check tenant/resource ownership on reads and writes.
- Check idempotency keys, replay behavior, webhook authenticity, and TOCTOU gaps.
- Escalate deep adversarial work to a dedicated security review, naming the exact surface.

### Data and migration safety

- Check transaction boundaries, partial commits, retries, uniqueness, and ordering.
- Confirm migrations match runtime reads/writes and have a safe rollout order.
- Check downgrade/rollback assumptions when the deployment process supports them.
- Identify dual ledgers, destructive defaults, lossy conversion, and wipe-on-start behavior.

### Concurrency and lifecycle

- Trace ownership across tasks, threads, processes, callbacks, and shutdown.
- Check lock ordering, blocking in async contexts, double execution, cancellation,
  leaked resources, late callbacks, and retry storms.
- For plausible races, identify the interleaving needed; do not label generic
  concurrency as a defect without a failing schedule or broken invariant.

### Interfaces and compatibility

- Compare producers and consumers of APIs, CLI flags, events, schemas, files,
  serialization, feature flags, and environment variables.
- Check all internal callers after signature or semantic changes.
- Preserve compatibility only when the assignment or real external contract
  requires it; do not request speculative shims in projects that have chosen a clean break.
- Check version skew and rollout ordering across independently deployed components.

### Configuration, dependencies, and supply boundaries

- Check secure defaults, missing/empty values, precedence, environment drift,
  and configuration documentation when part of the contract.
- Inspect manifest and lockfile deltas together.
- Flag new lifecycle hooks, binaries, network behavior, build scripts, or licenses
  for explicit review; do not execute untrusted dependency code merely to test it.
- Distinguish dependency behavior from assumptions made by the changed code.

### Operations and observability

- Check build, startup, health, readiness, deploy, migration, and rollback order.
- Ensure material failures are observable without exposing secrets or tenant data.
- Check metrics/log labels for cardinality and audit usefulness when relevant.
- A passing unit suite is not deployment proof.

### Tests and evidence honesty

- Confirm the regression test would fail without the fix when feasible.
- Ensure mocks do not bypass the boundary being claimed as tested.
- Check negative, authorization, migration, concurrency, and integration paths
  proportional to risk.
- Treat status files, summaries, and commit messages as claims, not proof.

### Test-surface regression

Implementers under delivery pressure routinely delete, narrow, loosen, skip, or
rewrite tests that block their implementation. The auditor must verify the
test surface was not weakened without justification:

- Diff the test surface against the base: removed tests, weakened assertions,
  loosened mocks, narrowed scopes, deleted regression cases, and newly-gated
  entries (`#[ignore]`, `.skip()`, `xit`, `@pytest.mark.skip`, feature-flag
  gating, reduced iteration counts, relaxed tolerances).
- Every deletion or weakening requires explicit justification in the
  implementer's commit message, delivery spec, or review note. "Test was
  failing" or "blocked the change" is the signal of weakening, not the
  justification.
- Unjustified weakening is a finding. Severity is P1 when the affected test
  covered the changed behavior or would have caught the confirmed defect;
  otherwise P2.
- When a defect is confirmed, require the implementer to add a regression that
  fails without the fix, plus proportional coverage for the adjacent paths the
  defect touched (callers, error branches, concurrency, negative paths).
- The corrected behavior must be proven in the test framework, not inferred
  from a passing suite or a post-fix symptom check. Bias toward demanding
  additional coverage when a defect surfaces, not less.

### Performance and resource safety

- Report obvious availability failures: unbounded growth, blocking hot paths,
  deadlocks, retry amplification, or catastrophic complexity.
- Treat optimization opportunities without correctness impact as separate work, not findings.

## 5. Validate By Risk

Validation is non-editing, not necessarily filesystem read-only. Compilers and
tests may create cache/build artifacts. Do not run unsafe external code, use
credentials, contact production, mutate data, run migrations, or cross a trust
boundary merely because the repository documents a command.

| Risk | Minimum evidence when safe and available |
| --- | --- |
| Low | Diff/static inspection; focused existing tests for changed behavior |
| Medium | Focused tests plus typecheck/build or equivalent boundary validation |
| High | Regression and negative-path tests; affected integration suite; schema/config/deploy checks as applicable |
| Critical | High-risk evidence plus independent security/operational review; no clean pass from source inspection alone |

Select repo-native commands. Do not paste generic commands into an unfamiliar
toolchain. For each command record:

- exact command and working directory
- relevant environment assumptions
- exit status and concise result
- whether failure predates the range, is caused by it, or is unresolved
- skipped or blocked checks and why

If baseline is already red, compare against the base when safe or use history
and focused evidence. Never call an introduced failure "ambient" without proof.

## 6. Challenge Findings

Before promoting a candidate:

1. State expected behavior and its authority.
2. Trace the exact path from input/state to bad outcome.
3. Search for a guard, normalization, transaction, caller constraint, or test
   that disproves the issue.
4. Identify affected users, data, systems, or operational conditions.
5. Assign confidence based on evidence, not rhetorical certainty.
6. Describe the root-cause direction and observable done-when without writing a patch.

After confirming one blocker, continue the remaining coverage ledger. Distinct
root causes require distinct findings. Multiple symptoms of one root cause
should be consolidated with all material impact stated.

For a second-opinion audit, do not read the first report before completing this
step. Independence is evidence; duplicated phrasing is not.

## 7. Derive And Report The Verdict

Read `severity-and-verdicts.md`. Derive the verdict mechanically from:

1. highest supported severity and confidence
2. completeness of assigned coverage
3. required validation results
4. materiality of blind spots

Write findings first, ordered by severity and then confidence. Include a no-
findings statement only after coverage and validation are stated. Report what
was not proven: production behavior, global repository correctness, external
service behavior, or performance under load unless directly evidenced.

Return the report to the requester. If delivery fails, report the failure;
do not falsely claim the audit was delivered.
