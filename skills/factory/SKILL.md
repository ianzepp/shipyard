---
name: factory
description: Execute multi-phase or correctness-heavy implementation work through scoped planning, implementation, verification, review, and integration.
---

# Factory

Factory owns sustained implementation from an execution-ready goal or campaign
stage through verified, accepted changes. Internal flow:

```text
confirm intent → settle workflow → select phase → compile delivery → slice → implement and accept → phase gate → polish → audit when due → continue → closeout
```

Use `delivery` instead when the user wants planning without implementation. A
diagnosis request remains read-only unless the user also asks for repair. Use
`campaign` when several tracks still need a routing contract. A simple scoped
issue does not need Factory ceremony unless the user asks for the lifecycle.

## Authority and Scope

Establish the target repo, authoritative goal or campaign, phase frontier,
artifact location, [workflow](#workflow), and checkpoint. Infer these from
current repo evidence and prior instructions when safe. Ask only for a
material decision that cannot be resolved from those sources.

Campaign scope remains a completion contract. Every admitted item stays
mandatory until implemented and verified. A phase may sequence that work but
may not silently narrow it. Newly discovered out-of-scope work becomes
separate intake rather than expanding the active phase.

Keep edits within the selected phase. Preserve unrelated and foreign work.
Production effects, credentials, destructive data operations, deployments,
payments, and outbound actions remain subject to their explicit gates.

## Phase Loop

Run one coherent phase at a time:

1. Confirm the goal is grounded and execution-ready. At intake, create the
   run's one ledger file, settle the [workflow](#workflow) in its
   `## Workflow` section, and record the planning artifacts already written
   per that workflow ([loop](references/loop.md#factory-intake)).
2. Select one phase-sized outcome (a phase candidate) from the current
   frontier.
3. Compile it through the `delivery` contract when implementation boundaries,
   dependencies, or validation are not already explicit. One delivery spec is
   one factory phase by default; a multi-phase goal gets one spec and one
   slice file per phase.
4. Save enough durable state to resume after compaction. The ledger file is
   always required (default path and contents in
   [loop](references/loop.md#ledger-file)). Multi-agent, multi-repo, or
   multi-phase work also requires a saved delivery artifact; a small
   already-specified phase may use the existing issue or goal as its plan.
   Record the plan artifacts per the workflow.
5. Cut the phase with `slicer` when it needs more than one slice; the cut
   ends with a `<prefix>-tidy` slice unless the phase changes no source files
   (see Order). Once the plan and slice file are written, record the
   [phase base](#workflow) in the ledger. Implement the slices in `deps`
   order; sign off and accept each one per the workflow
   ([Running a Slice List](references/loop.md#running-a-slice-list)). Use
   bounded workers only when their write scopes are disjoint and the workflow
   isolates each slice's changes.
6. Run the phase gate over the phase change set
   ([loop](references/loop.md#phase-gate)): the strongest honest
   phase-scoped verification, then `poker-face`, then review of the diff for
   behavioral correctness, scope completion, test weakening, boundary
   violations, and evidence honesty, then the checkpoint. Red-first proof for
   new behavior and bug fixes is already checked at slice sign-off.
7. Confirm the phase's accepted work is durable per the workflow, and
   integrate at any point the workflow names for the end of a phase.
8. Run `polish` over the phase's accepted primary source files, with no slice
   in progress. Generated, vendored, lock, cache, build, and third-party files
   are not polish targets unless intentionally changed.
9. Run an audit when a mid-goal risk signal makes one due, and resolve it
   per [After Audit](#after-audit). The goal-completion audit runs in
   [Closeout](#closeout), after housekeeping, not here.
10. Update the owning goal or campaign status and the ledger with exact
    evidence, recorded per the workflow, before beginning another phase.
11. Record whether the accumulated work requires a version bump, release prep,
    immediate release, or explicit deferral.
12. Continue to the next eligible phase while scope, authority, and gates are
    clear; otherwise pause at the exact boundary. When every phase is
    accepted, run [Closeout](#closeout).

## Order

This is the one canonical order inside and around a phase; other skills point
here rather than restating it:

```text
for each slice (deps order): implement → slice sign-off → accept (durable per the workflow)
phase gate over the phase change set: verification → poker-face → review → checkpoint
phase passes → polish (no slice in progress; polish edits kept separate from slice work)
audit when a mid-goal risk signal makes one due (see After Audit)
housekeeping only between phases, at inflection points, on a clean tree
all phases accepted → closeout (housekeeping → goal-completion audit → integration)
```

- In-phase structural cleanup is not housekeeping. It is a final **tidy
  slice** in the phase, cut by `slicer` as `<prefix>-tidy`: the `cleanliness`
  lens on the phase's changed files, no behavior change, signed off and
  accepted like any slice ([loop](references/loop.md#tidy-slice)).
- `housekeeping` runs only between phases or at closeout, with no slice in
  progress, on a clean tree (bookkeeping files aside); its git steps follow
  the workflow.
- `polish` runs on accepted work only, when no slice is in progress. Its
  edits are kept separate from slice work.
- `poker-face` is mandatory at the phase gate whenever a goal, spec, or
  acceptance criteria exist. Skip it only when none exist, and record the
  reason. Without delegation, run it as a self-contained cold pass;
  "delegation unavailable" is not a skip reason.

Each lens is its own skill (see References). Skip a lens only with a recorded
reason. When a lens at the gate (poker-face, review, correctness) finds a
blocking issue, send it to `slicer` rework mode (a), run the repair slices
through sign-off, and rerun the affected gate checks. A bug polish finds after
the gate passed reopens the checkpoint
([loop](references/loop.md#polish)). After two failed gate cycles on the same
finding, the gate returns `NEEDS FURTHER REVIEW` and factory pauses for the
user ([Resumption and Failure](#resumption-and-failure)).

Do not stop after producing a plan when implementation was requested. Do not
mark a phase complete with a failed sign-off, verification, poker-face, or
checkpoint gate unless the user explicitly accepts the named risk.

## Workflow

The **workflow** is how changes are isolated, made durable, and integrated.
Factory does not impose one. The running agent settles it at factory intake
and records it in the ledger's `## Workflow` section
([loop](references/loop.md#ledger-file)):

- its source (repo instructions, the user, or the agent's choice);
- the branch layout, if any;
- how a slice's own changes are isolated for sign-off;
- when work becomes durable (a commit, a merge, or a
  [checkpoint](#checkpoints));
- integration points (merge, pull request);
- who records changes (the agent or the user);
- how the repo's own vocabulary maps onto factory's: when repo instructions
  use their own terms ("unit", "task", "story"), map them onto slice and
  phase and record the mapping here.

**Precedence.** The repo's own instructions (`AGENTS.md`, `CLAUDE.md`,
`CONTRIBUTING`, branch protection, existing practice) win over the user's
stated preference, which wins over the agent's choice from the
[recommended structures](references/loop.md#workflow-structures). The agent
decides the details and records them so a later agent can follow them.

**Requirements.** Whatever the workflow, the process needs:

1. **Accepted work is durable** before anything that depends on it starts:
   a commit, a merge, or a checkpoint (defined below).
2. **A slice's own changes are isolated** for sign-off, including new
   untracked files (`git status --porcelain -uall` or equivalent). If the
   workflow cannot isolate them, slices run one at a time and the agent
   records the changed paths when each slice starts and when it is accepted.
3. **A phase has a base and a reviewable change set** (from where the phase
   started to the current accepted state) for the phase gate.
4. **An audit gets a frozen ref or range**: a commit range, branch tip, pull
   request, or a pair of [checkpoints](#checkpoints), and nobody changes it
   during the audit.
5. **Polish and housekeeping run only when no slice is in progress** and the
   phase's work is accepted.

**Hard rule.** Never destroy or overwrite work you did not make (for example
with `reset --hard`, `checkout -- .`, `restore`, or `clean` over changes that
are not yours). Never rewrite history that is accepted, integrated, or shared.
Never force-push a shared branch. Fix forward. On a private work-in-progress
branch, history edits are a workflow choice.

**Accepted.** A slice is accepted when it passes
[sign-off](references/loop.md#running-a-slice-list) and its changes are made
durable per the workflow. Slice status lives only in the slice file; the
ledger points to that file:

```text
- status: pending | in-progress | accepted <ref> | blocked-scope | split into <ids> | reworked by <ids>
```

`<ref>` identifies the accepted state in the workflow (a commit, the
feature-branch tip after the slice's merge, or `tree:<id>` for a
[checkpoint](#checkpoints)), or is `-` when the workflow records none.
`deps` wait for `accepted`.

**Bookkeeping files** are the goal, the campaign, the delivery spec, the slice
file, the ledger, the audit report, and `.polish-inspected.json`. Their default
home is one directory per goal, `docs/goals/<goal-name>/`
([layout](references/loop.md#ledger-file)); `.polish-inspected.json` stays at
the repo root. They are excluded from the slice scope check and from
clean-tree checks. Bookkeeping is integrated with the work it documents (it
travels through the pull request) unless the repo or the user says
otherwise. Record it however the workflow records work; it must be durable
before [closeout](#closeout) ends.

**Clean tree.** No changes beyond accepted work and bookkeeping files. In a
committing workflow that means nothing uncommitted except bookkeeping; in a
workflow that uses [checkpoints](#checkpoints), it means no changes since the
latest accepted checkpoint. Housekeeping and polish check this before they
start.

**Phase base.** Where the phase started in the workflow (a commit, a branch
point, or a [checkpoint](#checkpoints)), recorded in the ledger after the
phase's plan artifacts are written. The **phase change set** runs from the
base to the current accepted state; the phase gate reviews it.

### Checkpoints

A **checkpoint** is an id for a saved snapshot of the working tree that
touches no branch, no index, and no working file. It is how a workflow where
the agent does not commit (structure C in
[Workflow Structures](references/loop.md#workflow-structures)) makes work
durable and reviewable. It is not the phase gate's checkpoint evaluation,
which is recorded in the phase's Checkpoint section of the ledger. A
suggested mechanism:

```bash
idx="$(git rev-parse --git-dir)/shipyard-index"
GIT_INDEX_FILE="$idx" git add -A && GIT_INDEX_FILE="$idx" git write-tree
```

This leaves the real index, the branches, and the working files untouched. It
prints a tree id that includes new untracked files (respecting `.gitignore`).
Record it as the slice's `<ref>`: `accepted tree:<id>`.

- **Phase base.** In this workflow the phase base is a checkpoint taken after
  the phase's plan artifacts are written.
- **Slice diff.** A slice's own changes are
  `git diff <previous checkpoint> <new checkpoint>`. While a slice is in
  progress, take a checkpoint and diff against the previous one.
- **The user commits whenever.** The user may commit per slice, per phase,
  or at the end. The agent never waits for a commit to continue.
- **Resume.** The checkpoint ids in the slice file and the ledger are the
  authority; commit trailers may be absent.
- **Audits.** An audit uses checkpoints as `base` and `head`. A re-audit
  after repairs reviews the original base to the new checkpoint.
- **Lifetime.** Unreferenced tree objects can be garbage-collected after a
  few weeks, so checkpoints serve for the duration of the work. The ledger
  keeps each slice's changed-path list as a fallback.

## Commits

How changes are recorded (commits, branches, merges, or no commits by the
agent at all) is the [workflow](#workflow)'s job. Factory sets no commit
granularity and no required message format; a repo's own convention wins.

In a workflow that commits, the suggested slice commit message is:

```text
<type>(<scope>): <slice title>

Slice: <id>
```

The `Slice:` trailer lets a later agent resume from `git log`.

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
are optional per phase otherwise. A risk-signal audit runs in the phase loop;
the goal-completion audit runs in [closeout](#closeout), after housekeeping.
An audit reviews a frozen ref or range ([workflow](#workflow) requirement 4).
The goal-level audit range starts at the first phase's base and ends at the
tip that holds all the goal's accepted work (for example the feature-branch
tip), or at the final checkpoint. The auditor writes its report file
(default `audit.md` in the goal directory;
[layout](references/loop.md#ledger-file)); factory records it per the
workflow. A re-audit writes `audit-<n>.md` (`n` counting from 2) and never
overwrites an earlier report.

- `block_ship` → `slicer` rework → a repair phase → re-audit the original
  range plus the repairs.
- `residual` → each finding goes to the ledger's Deferred Findings with an
  owner and an observable done-when; the user decides when. A residual fixed
  now runs as a repair phase, with the same rules as after `block_ship`; a
  re-audit is due when the fix touches a risk-signal surface.
- `clean_pass` → record it in the ledger.

A **repair phase** has these rules:

- Its plan is the audit report's findings (no new delivery spec).
- Its slice file is `repair-<n>.slices.md` in the goal directory, and its
  slice ids are `repair<n>-<k>`.
- It has no tidy slice. Polish runs only if the user asks.
- `poker-face` judges it against the findings' done-when.
- Two `block_ship` verdicts on the same finding return
  `NEEDS FURTHER REVIEW`, and factory pauses for the user.

## Closeout

A goal or campaign closes in this order:

1. Every phase is accepted.
2. `housekeeping` runs if due. By default its scope is the paths the goal
   changed, unless the user asks for more. It runs before the audit, so the
   audit covers it; after it, the audit range is frozen.
3. The goal-completion audit is resolved ([After Audit](#after-audit)):
   `clean_pass`, or every residual deferred with an owner and a done-when.
   Every independent-review item is closed, or accepted by the user by name
   and recorded in the ledger.
4. The work is integrated per the workflow (merge, pull request). The agent
   opens a pull request only when the workflow says so or the user asks.
5. The goal's `## Status` in its `GOAL.md` is set to `complete <ref>`, where
   `<ref>` is the integrated ref, or the final checkpoint in a workflow where
   the agent does not commit.
6. The ledger is closed with the integration state recorded, and the
   bookkeeping is made durable per the workflow.

Factory is complete when closeout is done.

## Decomposition

Batch homogeneous requirements after the first pattern is proven. Split only
at a named dependency, risk, ownership, validation, migration,
external-effect, shared-write, or unresolved-design boundary. If planning and
implementation can proceed independently, overlap them rather than serializing
on phase numbers.

Avoid both extremes:

- one mega-phase that mixes unrelated behavior families and gates;
- tiny phases whose planning and closeout cost exceeds the implementation.

Factory owns integration, phase validation, checkpoint evaluation, recording
accepted work per the workflow, and final reporting. Workers own only their
bounded assignments; they record changes only where the workflow lets them
(for example, inside their own slice branch).

## Review Modes

Use a correctness-focused pass when fixing bugs, hardening reliability, or
protecting security, persistence, ABI, or concurrency invariants. Use explicit
red-green work when testability or coverage is itself a deliverable or when a
missing proof makes implementation unsafe. These are targeted modes, not
ceremony for every phase. Inside factory both modes produce or feed slices:
their edits run as slices through sign-off, at the narrowest test scope,
widening at checkpoints.

An independent review should inspect settled specifications or a frozen ref
or range. Treat worker reports as evidence to challenge, not an invitation to
repeat every test. Blocking findings violate a stated acceptance criterion or
release invariant; residual findings become owned follow-up work without
stopping unrelated phases.

## Resumption and Failure

Keep one ledger per run as a file at its default path, never only in chat.
Its contents are listed in [loop](references/loop.md#ledger-file). Resume from
the ledger (including its `## Workflow` section), the slice file's status
lines, and the workflow's history (for example `git log` and its `Slice:`
trailers, when the workflow uses them), not from chat history. In a workflow
where the agent does not commit, the [checkpoint](#checkpoints) ids in the
slice file and the ledger are the authority.

When a gate fails, preserve the evidence, route a bounded repair or decision,
and continue unaffected work. Use `slicer` rework mode to turn review findings
or failing checks into repair slices; they are signed off and accepted like
any slice. After two failed gate cycles on the same finding, return
`NEEDS FURTHER REVIEW` and pause for the user. Split is one level only: a
slice cut by split mode that hits the split trigger again escalates to
`NEEDS FURTHER REVIEW` instead of splitting again. Otherwise pause the factory only when the
remaining frontier requires missing authority, unavailable infrastructure,
conflicting contracts, or an unresolved decision that materially changes the
result.

**Resuming after `NEEDS FURTHER REVIEW`.** Present the user with these
options. Record the ruling in one place: the phase's Checkpoint in the
ledger.

- accept the named risk (recorded by name);
- amend scope or plan (update the goal with `goal-forge` or the spec with
  `delivery`);
- give direction for another rework attempt (this resets that finding's cycle
  count). The recorded ruling is `slicer` rework input (d) and counts as
  settling the design for that finding;
- stop.

## Completion Report

Report:

- phases and delivery artifacts completed;
- behavior implemented;
- verification and review evidence;
- accepted work as the workflow records it (for commits: count, short hash,
  and subject);
- audit verdicts and their disposition;
- goal or campaign status updates;
- integration state (branch, merge, pull request);
- release decision;
- separately recorded follow-up work;
- pending phases and exact blockers.

Point to durable artifacts rather than pasting them into chat. Factory is
complete only when [closeout](#closeout) is done.

## References

Load a reference only when its situation arises.

- [references/loop.md](references/loop.md): detailed execution model, ledger file, recommended workflow structures, slice runner, phase granularity, and phase gate; load when running the loop.
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
- [housekeeping](../housekeeping/SKILL.md): load for the maintenance pass between phases, at inflection points, and before the closeout audit, on a clean tree.
- [polish](../polish/SKILL.md): load for the per-file second pass over the phase's accepted source files after the gate passes.
- [auditor](../auditor/SKILL.md): load for an independent read-only audit of a frozen ref or range, or a release gate.
