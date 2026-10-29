---
name: campaign
description: Coordinate several related goals, bugs, features, or delivery tracks through one durable routing artifact. Use when one goal, delivery spec, or factory run is too narrow.
---

# Campaign

A campaign is a completion contract and routing control plane for several
tracks. It orders campaign stages and lowers them into `delivery` or `factory`.
It does not implement product work directly.

Flow: `campaign → delivery → slicer → factory`.

## Modes

Choose and state the mode before substantive work.

- **Draft or maintain:** the user wants the campaign artifact created,
  reviewed, revised, or validated. Change only the artifact.
- **Run:** an existing campaign is the active goal and the user asks to run,
  continue, execute, or advance it. Use the artifact as the control plane and
  lower its next eligible stage.

An existing campaign with a bare execution objective normally means run mode.
A new or underspecified initiative normally means draft mode. A document name
containing `CAMPAIGN` does not decide the mode.

Local downstream execution is authorized in run mode unless the campaign,
repository rules, or user reserves an approval gate. Production changes,
deployments, payments, credential use, destructive data changes, and outbound
effects still require their stated authority.

State lives in files. The default campaign artifact is `CAMPAIGN.md` (or
`<name>.campaign.md`) at the repo root or the repo's docs directory; a repo's
own convention wins. Record the path used.
Commit the artifact when it is written or approved, as `docs(plan): <name>`,
following the user's commit unit (see factory
[Commits](../factory/SKILL.md#commits)). Factory keeps one ledger for the run
beside it (`<campaign-stem>.ledger.md`).

## Ground Truth

Read the campaign and its authoritative sources, then verify important status
claims against current code, tests, test output, ledgers, and Git history. Docs
describe intent unless current evidence proves implementation.

Identify:

- desired end state;
- every admitted item and required deliverable;
- current stage status and evidence;
- dependencies, gates, and stop conditions;
- the first incomplete, unblocked stage;
- production, migration, credential, and external-effect boundaries.

Missing or weak evidence means incomplete.

## Scope Closure

Every admitted item is mandatory through implementation and verification.
Sequencing may divide the work but may not discard, downgrade, or move admitted
scope outside the campaign. Work that is not part of the completion contract
belongs in separate intake, not an optional or deferred campaign stage.

The campaign remains incomplete while any admitted item or desired end-state
condition remains incomplete. Changing the contract requires an explicit
amendment stating what contract is replaced and what replaces it. A narrower
request for one turn does not silently narrow the campaign.

## Draft or Maintain

Produce one artifact that lets a later agent select the next stage without
rereading every source document. Use repository vocabulary, but include:

1. Summary and desired end state.
2. Scope and explicit exclusions.
3. Ground truth inspected and source authority.
4. Current track states and next actions.
5. Ordered campaign stages.
6. Dependencies, gates, and stop conditions.
7. Validation and closeout conditions.
8. Open routing decisions.

For each stage, record its status, source, dependency or gate, and whether it
lowers to `delivery`, `factory`, or both in sequence. Name the complete target
stage scope. For implementation-heavy work, state whether homogeneous successors
should batch, which concrete boundary permits splitting, or whether one
discovery unit must establish the pattern first.

Do not invent implementation acceptance criteria from conceptual prose or
embed factory tasks in the top-level artifact.

## Run Loop

1. Read the artifact and authoritative sources.
2. Reconstruct the admitted scope and desired end state.
3. Verify completed stages and gates from live evidence.
4. Select the first incomplete, unblocked stage.
5. Preserve the stage as one coherent outcome unless evidence identifies
   a real dependency, risk, ownership, validation, migration, or
   external-effect boundary.
6. If it needs a repo-aware spec, lower the whole stage through `delivery`
   (one spec per factory phase).
7. If it is execution-ready and authorized, lower it through `factory` or the
   named task-specific process.
8. Validate the stage with the strongest honest stage-scoped evidence.
9. Update the campaign and the owning goal's `## Status` section immediately
   with evidence, routing changes, blocked work, and the next stage. These
   status edits are bookkeeping: commit them with the stage's work or as
   `chore(ledger): <event>` under the user's commit unit.
10. Continue while the next stage is clear, safe, and authorized.

Research and documentation campaigns may produce artifacts and run gates
instead of changing code. They still obey the admitted scope and evidence
rules.

## Stop and Completion

Pause when authority is missing, sources conflict, a routing-changing decision
is unresolved, or the next effect crosses a reserved gate. State the exact
boundary and authoritative decision required.

Do not call the campaign complete because the artifact is coherent, a next
stage is named, a delivery spec exists, or partial tests pass. Complete only
when every admitted item is implemented and verified and the desired end state
and closeout gates are achieved, or the user explicitly amends the contract.
An audit is due at campaign completion (see factory
[After Audit](../factory/SKILL.md#after-audit)), and any open
independent-review item blocks closeout unless the user accepts it by name,
recorded in the ledger.

In draft mode, report whether the artifact has a stage ready for `delivery`, a
stage ready for `factory`, routing only, or missing discovery. In run mode,
lower the ready stage rather than stopping at that label.
