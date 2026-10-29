---
name: factory
description: Execute multi-phase or correctness-heavy implementation work through scoped planning, implementation, verification, review, and commits.
---

# Factory

Factory owns sustained implementation from an execution-ready goal or campaign
stage through verified, coherent commits. Internal flow:

```text
confirm intent → select phase → compile delivery → slice → implement and commit → phase gate → polish → audit when due → continue
```

Use `delivery` instead when the user wants planning without implementation. A
diagnosis request remains read-only unless the user also asks for repair. Use
`campaign` when several tracks still need a routing contract. A simple scoped
issue does not need Factory ceremony unless the user asks for the lifecycle.

## Authority and Scope

Establish the target repo, authoritative goal or campaign, phase frontier,
artifact location, commit unit, and checkpoint. Infer these from current repo
evidence and prior instructions when safe. Ask only for a material decision
that cannot be resolved from those sources.

Campaign scope remains a completion contract. Every admitted item stays
mandatory until implemented and verified. A phase may sequence that work but
may not silently narrow it. Newly discovered out-of-scope work becomes
separate intake rather than expanding the active phase.

Keep edits within the selected phase. Preserve unrelated and foreign work.
Production effects, credentials, destructive data operations, deployments,
payments, and outbound actions remain subject to their explicit gates.

## Phase Loop

Run one coherent phase at a time:

1. Confirm the goal is grounded and execution-ready.
2. Select one phase-sized outcome (a phase candidate) from the current
   frontier, and record the phase base in the ledger.
3. Compile it through the `delivery` contract when implementation boundaries,
   dependencies, or validation are not already explicit. One delivery spec is
   one factory phase by default; a multi-phase goal gets one spec and one
   slice file per phase.
4. Save enough durable state to resume after compaction. The run's one ledger
   file is always required (default path and contents in
   [loop](references/loop.md#ledger-file)). Multi-agent, multi-repo, or
   multi-phase work also requires a saved delivery artifact; a small
   already-specified phase may use the existing issue or goal as its plan.
   Commit plan artifacts not already committed as `docs(plan): <name>`
   (see [Commits](#commits)).
5. Cut the phase with `slicer` when it needs more than one slice; the cut
   ends with a `<prefix>-tidy` slice unless the phase changes no source files
   (see Order). Implement the slices in
   `deps` order; sign off and commit each one per the commit unit
   ([Running a Slice List](references/loop.md#running-a-slice-list)). Use
   bounded workers only when their write scopes are disjoint.
6. Run the phase gate over the phase change set
   ([loop](references/loop.md#phase-gate)): the strongest honest
   phase-scoped verification, then `poker-face`, then review of the diff for
   behavioral correctness, scope completion, test weakening, boundary
   violations, and evidence honesty, then the checkpoint. Red-first proof for
   new behavior and bug fixes is already checked at slice sign-off.
7. Commit per the commit unit: per-slice commits already exist; per-phase
   mode makes its one commit when the gate passes; in user-commits mode
   factory has staged each signed-off slice and reported it, and the user
   commits. The phase's work is committed before polish runs.
8. Run `polish` over the phase's committed primary source files. Generated,
   vendored, lock, cache, build, and third-party files are not polish targets
   unless intentionally changed.
9. Run an audit when one is due, and resolve it per [After Audit](#after-audit).
10. Update the owning goal or campaign status and the ledger with exact
    evidence, committed as bookkeeping (see [Commits](#commits)), before
    beginning another phase.
11. Record whether the accumulated work requires a version bump, release prep,
    immediate release, or explicit deferral.
12. Continue to the next eligible phase while scope, authority, and gates are
    clear; otherwise pause at the exact boundary.

## Order

This is the one canonical order inside and around a phase; other skills point
here rather than restating it:

```text
for each slice (deps order): implement → slice sign-off → commit (per commit unit)
phase gate over the phase change set: verification → poker-face → review → checkpoint
phase passes → polish (own per-file commits, polish-only)
audit when due (see After Audit)
housekeeping only between phases, at inflection points, on a clean tree
```

- In-phase structural cleanup is not housekeeping. It is a final **tidy
  slice** in the phase, cut by `slicer` as `<prefix>-tidy`: the `cleanliness`
  lens on the phase's changed files, no behavior change, signed off and
  committed like any slice ([loop](references/loop.md#tidy-slice)).
- `housekeeping` runs only between phases or at goal or campaign closeout, on
  a clean tree, where its pull and its own commits are safe.
- `polish` runs on committed work only; its commits contain only polish.
- `poker-face` is mandatory at the phase gate whenever a goal, spec, or
  acceptance criteria exist. Skip it only when none exist, and record the
  reason. Without delegation, run it as a self-contained cold pass;
  "delegation unavailable" is not a skip reason.

Each lens is its own skill (see References). Skip a lens only with a recorded
reason. When a lens at the gate (poker-face, review, correctness) or polish
finds a blocking issue, send it to `slicer` rework mode (a), run the repair
slices through sign-off, and rerun the affected gate checks. After two failed
gate cycles on the same finding, the gate returns `NEEDS FURTHER REVIEW` and
factory pauses for the user.

Do not stop after producing a plan when implementation was requested. Do not
mark a phase complete with a failed sign-off, verification, poker-face, or
checkpoint gate unless the user explicitly accepts the named risk.

## Commits

Commit granularity is the user's choice. Record it in the ledger as the
**commit unit** at the start of a factory run; ask, or infer it from repo rules
and history:

- `per-slice` (default): commit each slice after its sign-off. The commit
  holds the slice's `write_scope` plus the bookkeeping paths it updated.
- `per-phase`: one commit when the phase gate passes, holding the phase
  change set and its bookkeeping.
- `user-commits`: factory stages each signed-off slice and reports it; the
  user commits when they choose. Polish waits until the user has committed
  the phase, then stages one file at a time and reports.

Goals can take days. Never hold work uncommitted until the end of a goal. A
phase always has its work committed before polish runs.

A slice is **landed** when it is signed off and recorded in the slice file.
Committed is separate: the status line reads `landed (uncommitted)` until a
commit holds the work, then `landed <short hash>`. `deps` wait for landed, not
committed.

**Phase base and change set.** The phase base is the commit the phase started
from, recorded in the ledger. The phase change set is everything since the
base: the range `<base>..HEAD` in per-slice mode, or the commits plus the
working-tree diff against the base in per-phase and user-commits modes. The
phase gate runs over the change set.

**Bookkeeping paths** of a run are the ledger, the current slice file, edits
to the goal's `## Status` section, and status edits to the campaign artifact.
They are not part of any slice's diff, and they ride along with the commit
that updates them.

Commit messages (a repo's stronger convention wins; keep the `Slice:`
trailer):

| Commit | Message |
| --- | --- |
| Slice | `<type>(<scope>): <slice title>` with a trailer `Slice: <id>` |
| Plan artifact (goal, campaign, delivery spec, slice file) when written or approved | `docs(plan): <name>` |
| Gate results and other ledger updates | `chore(ledger): <phase> <event>` |
| Audit report | `docs(audit): <range>` |

Every commit is path-limited: stage only the paths that commit owns. In
user-commits mode each of these is staged and reported instead. A failed phase gate goes to `slicer`
rework; its repair slices land as new commits.

**Git safety.** Never `reset --hard`, `checkout -- .`, `restore` over others'
work, `clean`, `stash`, `rebase`, amend a landed commit, or force-push. Never
discard changes you did not make. Fix forward with new commits.

## Verdicts and Severity

Lens skills report in their own words. This table is how each maps to the
factory gate (`PASS`, `FAIL`, `NEEDS FURTHER REVIEW`):

| Skill | Verdicts | Maps to factory gate |
| --- | --- | --- |
| goal-check | `READY` / `NOT READY` / `NEEDS FURTHER REVIEW` | `PASS` / `FAIL` / `NEEDS FURTHER REVIEW` |
| poker-face | `CLEARED` / `NOT CLEARED` | `PASS` / `FAIL` |
| red-green | clearance: `CLEARED` / `NOT CLEARED` / `BLOCKED` | `PASS` / `FAIL` / `NEEDS FURTHER REVIEW` |
| auditor | `clean_pass` / `residual` / `block_ship` | `PASS` / `PASS` with deferred findings / `FAIL` |

Severity: the auditor's `P0` / `P1` / `P2` is the canonical scale.
`correctness` `CRITICAL` ≈ `P0`, `HIGH` ≈ `P1`, `MEDIUM` and `LOW` ≈ `P2`.
At slice sign-off, a `correctness` `CRITICAL` or `HIGH` finding sends the
slice back to its implementer; `MEDIUM` and `LOW` go to the ledger as notes.

For `poker-face`, a `HIGH` miss blocks. A `MEDIUM` miss that breaks an
acceptance criterion always blocks. Any other `MEDIUM` miss blocks unless the
user approves deferring it, or the plan already names it as deferred; surface
it before the gate passes, then record it as a named deferred finding. A `LOW`
miss is noted.

Deferred findings carry a factory priority
([loop](references/loop.md#phase-gate)). Severities feed it like this:

- `P0` and `P1` are never deferred: they fail the gate and go to rework,
  unless the user explicitly accepts the named risk.
- `P2` is `important` by default, and `blocking-later` when a named later
  phase, release, or goal closeout cannot pass without it.
- Noted-only findings (poker-face `LOW`, a `P2` the reviewer calls cosmetic)
  are `opportunistic`.
- Independent-review items (an auditor's "independent review required" item
  from a self-audit, or a critical-risk security review) are always
  `blocking-later` for release gates and goal or campaign closeout. Closeout
  cannot happen with one open unless the user explicitly accepts it by name;
  record that acceptance in the ledger.

## After Audit

Audits are due at goal or campaign completion, at release gates, on risk
signals (auth, permissions, data migration, persistence, concurrency, public
API or schema change, security-sensitive input), or when the user asks. They
are optional per phase otherwise. An audit reviews a committed range. Factory
commits the audit report file as `docs(audit): <range>`.

- `block_ship` → `slicer` rework → a repair phase → re-audit the original
  range plus the repairs.
- `residual` → each finding goes to the ledger's Deferred Findings with an
  owner and an observable done-when; the user decides when. A residual fixed
  now goes through `slicer` rework like any repair; a re-audit is due when
  the fix touches a risk-signal surface.
- `clean_pass` → record it in the ledger.

## Decomposition

Batch homogeneous requirements after the first pattern is proven. Split only
at a named dependency, risk, ownership, validation, migration,
external-effect, shared-write, or unresolved-design boundary. If planning and
implementation can proceed independently, overlap them rather than serializing
on phase numbers.

Avoid both extremes:

- one mega-phase that mixes unrelated behavior families and gates;
- tiny phases whose planning and closeout cost exceeds the implementation.

Factory owns integration, phase validation, checkpoint evaluation, commits,
and final reporting. Workers own only their bounded assignments and do not
commit.

## Review Modes

Use a correctness-focused pass when fixing bugs, hardening reliability, or
protecting security, persistence, ABI, or concurrency invariants. Use explicit
red-green work when testability or coverage is itself a deliverable or when a
missing proof makes implementation unsafe. These are targeted modes, not
ceremony for every phase. Inside factory both modes produce or feed slices:
their edits run as slices through sign-off, at the narrowest test scope,
widening at checkpoints.

An independent review should inspect settled specifications or frozen commit
ranges. Treat worker reports as evidence to challenge, not an invitation to
repeat every test. Blocking findings violate a stated acceptance criterion or
release invariant; residual findings become owned follow-up work without
stopping unrelated phases.

## Resumption and Failure

Keep one ledger per run as a file at its default path, never only in chat.
Its contents are listed in [loop](references/loop.md#ledger-file). Resume from the
ledger, the slice file's status lines, and `git log` (the `Slice:` trailers),
not from chat history.

When a gate fails, preserve the evidence, route a bounded repair or decision,
and continue unaffected work. Use `slicer` rework mode to turn review findings
or failing checks into repair slices, and land them as new commits. After two
failed gate cycles on the same finding, return `NEEDS FURTHER REVIEW` and
pause for the user. Otherwise pause the factory only when the remaining frontier requires missing authority,
unavailable infrastructure, conflicting contracts, or an unresolved decision
that materially changes the result.

## Completion Report

Report:

- phases and delivery artifacts completed;
- behavior implemented;
- verification and review evidence;
- commits as count, short hash, and subject;
- audit verdicts and their disposition;
- goal or campaign status updates;
- release decision;
- separately recorded follow-up work;
- pending phases and exact blockers.

Point to durable artifacts rather than pasting them into chat. Factory is
complete only when its authorized phases are implemented, verified, reviewed,
recorded, and committed, and any due audit is resolved.

## References

Load a reference only when its situation arises.

- [references/loop.md](references/loop.md): detailed execution model, ledger file, slice runner, phase granularity, phase gate and commit rules; load when running the loop.
- [references/vision.md](references/vision.md): load when judging whether a goal is execution-ready.
- [references/production.md](references/production.md): load when selecting or sequencing phase candidates from the goal or campaign.
- [references/subagent.md](references/subagent.md): load when delegating bounded work to workers or independent reviewers.
- [references/correctness-mode.md](references/correctness-mode.md): load for bug fixes, reliability hardening, or security, persistence, ABI, and concurrency invariants.
- [references/red-green-mode.md](references/red-green-mode.md): load when testability or coverage is itself a deliverable.
- [poker-face](../poker-face/SKILL.md): load to audit a finished phase against its promised requirements at the phase gate.
- [red-green](../red-green/SKILL.md): load for the full test-first coverage loop behind red-green mode.
- [slicer](../slicer/SKILL.md): load to cut a phase into slices, to turn review findings into repair slices, or to split a slice that failed sign-off twice or proved larger than its brief.
- [correctness](../correctness/SKILL.md): load for the read-only correctness read at slice sign-off and for correctness mode.
- [cleanliness](../cleanliness/SKILL.md): load for the `<prefix>-tidy` slice at the end of a phase.
- [housekeeping](../housekeeping/SKILL.md): load for the maintenance pass between phases, at inflection points, on a clean tree.
- [polish](../polish/SKILL.md): load for the per-file second pass over the phase's committed source files after the gate passes.
- [auditor](../auditor/SKILL.md): load for an independent read-only audit of a committed range or release gate.
