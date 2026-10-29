# Auditor Severity And Verdicts

Use this taxonomy for every auditor report. Severity describes consequence;
confidence describes evidence. Do not raise severity to compensate for weak
evidence or lower it because a fix seems easy.

## Severity

| Level | Definition | Typical examples | Disposition |
| --- | --- | --- | --- |
| **P0** | Active or immediately exploitable catastrophic failure with broad or irreversible impact | Cross-tenant disclosure in a live path, destructive migration/data wipe, credential compromise, systemic outage trigger | `block_ship`; immediate escalation to the requester and security/ops owners |
| **P1** | Ship-blocking correctness, security, data, availability, or contract failure under realistic conditions | Auth bypass, corruption, broken primary workflow, unsafe migration, deadlock, incompatible API/schema rollout, silent material loss | `block_ship`; repair owned by the implementer or a specialist |
| **P2** | Real bounded defect or material evidence gap that does not make the reviewed change unsafe to merge under current conditions | Incorrect edge case, missing noncritical negative test, bounded cleanup leak, misleading operational signal, incomplete supporting integration | `residual`; named owner and observable done-when |

Do not report style, naming preference, speculative architecture, or generic
best practice as P2. Route maintainability to [cleanliness](../../cleanliness/SKILL.md), and treat
performance opportunities without correctness impact as separate work.

## Confidence

| Confidence | Evidence |
| --- | --- |
| **confirmed** | Reproduced failure, failing test, deterministic trace, or direct invariant contradiction with no applicable guard |
| **likely** | Complete source/data-flow reasoning and realistic trigger, but execution is unavailable or unsafe |
| **plausible** | Credible risk with missing facts or an unresolved interaction; requires targeted validation before promotion |

Plausible concerns normally belong in `blind_spots`, not findings. Promote a
plausible concern to a finding only when the uncertainty itself violates a
required evidence or safety contract. Explain what fact would confirm or dismiss it.

## Verdict Derivation

### `block_ship`

Required when any of these is true:

- confirmed P0 or P1
- likely P1 that cannot be safely disproved before disposition
- required validation fails because of the reviewed change
- a critical changed surface is unreviewed or cannot be identified
- base/head identity is unstable for a high- or critical-risk audit
- a migration, auth, tenancy, money, or destructive-data path lacks the minimum
  evidence needed to establish its central invariant

P2 findings may accompany `block_ship` but do not cause it by themselves.

### `residual`

Allowed only when there is no ship blocker and at least one of these remains:

- confirmed or likely P2
- skipped noncritical validation with bounded effect
- immaterial or bounded blind spot
- accepted follow-up that the requester must preserve
- a plausible concern requiring later measurement or environment access

Every residual needs an owner or `unresolved`, a done-when, and its effect on
the reviewed change.

An "independent review required" or "independent security review required"
item is `blocking-later` for release gates and goal or campaign closeout (see
factory's [Verdicts and Severity](../../factory/SKILL.md#verdicts-and-severity)).
A residual the requester fixes now goes through rework, and a re-audit is due
if the fix touches a risk-signal surface.

### `clean_pass`

Allowed only when all are true:

- repository and exact range are frozen
- every assigned changed path is reviewed or explicitly excluded by assignment
- affected callers, consumers, tests, and operational boundaries are accounted for
- every applicable lens is completed
- minimum risk-based validation passes
- there are no P0, P1, or P2 findings
- blind spots are empty or demonstrably immaterial and disclosed
- the report states what was not claimed
- for a self-audit (`Evaluator mode: self-audit`) of a change touching auth,
  permissions, tenancy, data migration, persistence formats, or
  security-sensitive input: a separate reviewer has signed off. Otherwise the
  verdict is `residual` with an "independent review required" item
- for a critical-risk audit: any required independent security review has
  been done; otherwise the verdict is `residual` with an "independent
  security review required" item naming the surfaces

A clean pass can coexist with pre-existing failures only when evidence proves
they predate the range and do not prevent validation of the changed behavior.
Record them in validation or blind spots.

## Calibration Rules

- Judge impact at the actual trust and deployment boundary.
- Use realistic triggering conditions, not theoretical possibility alone.
- A one-line fix can close a P1; fix size does not determine severity.
- Missing tests are P1 only when a required high-risk invariant is otherwise
  unverified. A routine missing regression is usually P2.
- Removed or weakened tests in the reviewed range are worse than missing tests:
  they represent coverage that existed and was discarded. Treat unjustified
  weakening as P1 when the affected test covered the changed behavior or would
  have caught the confirmed defect; otherwise P2. Deletion that masks a
  confirmed defect is P1 regardless of routine missing-test calibration.
- Backward incompatibility is a defect only when a real contract requires
  compatibility. Internal callers must instead move to the canonical path.
- Security findings need a concrete trust-boundary failure or escalation target.
- Performance findings become P1 when they plausibly cause outage, deadlock,
  unbounded resource exhaustion, or violation of an explicit service contract.
- If severity depends on an unknown fact, state both branches and assign the
  confidence supported by current evidence.

## Finding Quality Gate

A finding is ready to report only when it contains:

```text
severity + confidence
exact location or boundary
authoritative expected behavior
observed or traced actual behavior
concrete impact and trigger
evidence or reproduction limitation
root-cause fix direction
suggested owner
observable done-when
```

If one of these is unavailable, explain why. Unsupported certainty is a report
defect; hidden doubt is worse than an explicitly bounded blind spot.
