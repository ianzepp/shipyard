---
name: factory
description: Execute multi-phase or correctness-heavy implementation work through scoped planning, implementation, verification, review, and commits.
---

# Factory

Factory owns sustained implementation from an execution-ready goal or campaign
stage through verified, coherent commits. Internal flow:

```text
confirm intent → select phase → compile delivery → implement → verify → review → commit → continue
```

Use `delivery` instead when the user wants planning without implementation. A
diagnosis request remains read-only unless the user also asks for repair. Use
`campaign` when several tracks still need a routing contract. A simple scoped
issue does not need Factory ceremony unless the user asks for the lifecycle.

## Authority and Scope

Establish the target repo, authoritative goal or campaign, phase frontier,
artifact location, and checkpoint. Infer these from current repo evidence and
prior instructions when safe. Ask only for a material decision that cannot be
resolved from those sources.

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
2. Select one delivery-sized outcome from the current frontier.
3. Compile it through the `delivery` contract when implementation boundaries,
   dependencies, or validation are not already explicit.
4. Save enough durable state to resume after compaction. Multi-agent,
   multi-repo, or multi-stage work requires a delivery artifact; a small
   already-specified phase may use the existing issue or goal plus a compact
   ledger.
5. Implement the complete phase outcome, using bounded workers when their
   write scopes and dependencies are disjoint. Cut those bounded assignments
   with `slicer` when the phase needs more than one.
6. Run the strongest honest phase-scoped verification. New behavior should
   normally have a failing proof first and a passing proof afterward.
7. Review the diff for behavioral correctness, scope completion, test
   weakening, boundary violations, and evidence honesty.
8. Perform one closeout quality pass over changed primary source files:
   simplify unnecessary complexity, address structural debt, format and lint
   within scope, and inspect the final diff. Generated, vendored, lock, cache,
   build, and third-party files are not cleanup targets unless intentionally
   changed.
9. Evaluate the checkpoint and update the owning goal or campaign status with
   exact evidence before beginning another phase.
10. Commit only the coherent completed phase.
11. Record whether the accumulated work requires a version bump, release prep,
    immediate release, or explicit deferral.
12. Continue to the next eligible phase while scope, authority, and gates are
    clear; otherwise pause at the exact boundary.

Lens order inside a phase. This is the one canonical sequence; other skills
point here rather than restating it:

```text
implement → correctness → verification → poker-face (when completion must be reconstructed) → review → cleanliness / closeout → housekeeping (at phase or lifecycle boundaries) → polish → checkpoint → commit
```

Each lens is its own skill (see References). Skip a lens only with a recorded
reason; return to implementation when a lens finds a blocking issue, then
rerun the affected checks.

Do not stop after producing a plan when implementation was requested. Do not
commit a phase with failed correctness, verification, or checkpoint gates
unless the user explicitly accepts the named risk.

## Decomposition

Batch homogeneous requirements after the first pattern is proven. Split only
at a named dependency, risk, ownership, validation, migration,
external-effect, shared-write, or unresolved-design boundary. If planning and
implementation can proceed independently, overlap them rather than serializing
on stage numbers.

Avoid both extremes:

- one mega-phase that mixes unrelated behavior families and gates;
- tiny phases whose planning and closeout cost exceeds the implementation.

Factory owns integration, phase validation, checkpoint evaluation, remaining
phase commits, and final reporting. Workers own only their bounded assignments.

## Review Modes

Use a correctness-focused pass when fixing bugs, hardening reliability, or
protecting security, persistence, ABI, or concurrency invariants. Use explicit
red-green work when testability or coverage is itself a deliverable or when a
missing proof makes implementation unsafe. These are targeted modes, not
ceremony for every phase.

An independent review should inspect settled specifications or frozen commit
ranges. Treat worker reports as evidence to challenge, not an invitation to
repeat every test. Blocking findings violate a stated acceptance criterion or
release invariant; residual findings become owned follow-up work without
stopping unrelated phases.

## Resumption and Failure

Maintain a compact ledger containing the current phase, delivery artifact or
authority, completed units and commits, validation evidence, deferred findings,
failed gates, and next eligible phase. Resume from repo and ledger truth rather
than chat history.

When a gate fails, preserve the evidence, route a bounded repair or decision,
and continue unaffected work. Use `slicer` rework mode to turn review findings
or failing checks into repair slices. Pause the factory only when the remaining
frontier requires missing authority, unavailable infrastructure, conflicting
contracts, or an unresolved decision that materially changes the result.

## Completion Report

Report:

- phases and delivery artifacts completed;
- behavior implemented;
- verification and review evidence;
- commits as count, short hash, and subject;
- goal or campaign status updates;
- release decision;
- separately recorded follow-up work;
- pending phases and exact blockers.

Point to durable artifacts rather than pasting them into chat. Factory is
complete only when its authorized phase set is implemented, verified,
reviewed, recorded, and committed.

## References

Load a reference only when its situation arises.

- [references/loop.md](references/loop.md): detailed execution model, ledger fields, phase granularity, checkpoint and commit rules; load when running the loop.
- [references/vision.md](references/vision.md): load when judging whether a goal is execution-ready.
- [references/production.md](references/production.md): load when selecting or sequencing delivery-sized units from the goal or campaign.
- [references/subagent.md](references/subagent.md): load when delegating bounded work to workers or independent reviewers.
- [references/correctness-mode.md](references/correctness-mode.md): load for bug fixes, reliability hardening, or security, persistence, ABI, and concurrency invariants.
- [references/red-green-mode.md](references/red-green-mode.md): load when testability or coverage is itself a deliverable.
- [poker-face](../poker-face/SKILL.md): load to audit a finished phase against its promised requirements.
- [red-green](../red-green/SKILL.md): load for the full test-first coverage loop behind red-green mode.
- [slicer](../slicer/SKILL.md): load to cut a phase into disjoint worker assignments, or to turn review findings into repair slices.
- [correctness](../correctness/SKILL.md): load for the behavioral-bug pass after implementation.
- [cleanliness](../cleanliness/SKILL.md): load for the structural pass over changed code at closeout.
- [housekeeping](../housekeeping/SKILL.md): load for the mechanical maintenance pass at phase or lifecycle boundaries.
- [polish](../polish/SKILL.md): load for the per-file second-pass review of phase-modified source files.
- [auditor](../auditor/SKILL.md): load for an independent read-only audit of a frozen commit range or release gate.
