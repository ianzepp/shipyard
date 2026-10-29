# Shipyard

Agent skills for the engineering process: the planning, delivery, and review
work that turns an idea into shipped code.

You bring a rough idea, or a large feature nobody has scoped yet. Shipyard
gives your coding agent (Claude Code, Codex, Cursor, or any harness that reads
skill files) a disciplined path from that idea to verified commits:

```text
idea → explore → goal → readiness check → campaign → spec → slices → build and commit → phase gate → polish → audit when due → shipped
```

Each step is a skill. Each skill does one kind of work, reads what the step
before it left in your repository, and writes its own artifact for the next.
You can start at any step that fits where your work is today.

## Why

Coding agents are good at writing code and bad at the work around it. Left
alone, they tend to:

- start coding before anyone has decided what "done" means;
- keep the plan in chat, where it is lost when the context window fills;
- quietly drop the hard parts of the scope and report success anyway;
- trust a document that says something works without checking the code;
- weaken a test to get a green run;
- declare victory because the summary sounds complete.

Shipyard counters each of these with a step that has a clear contract, a
saved artifact, and an honest gate. Plans live in files. Scope is a contract
that only an explicit amendment can change. Every status claim is checked
against code, tests, and history. Review lenses look for bugs, missed
requirements, and structural debt before anything is called done.

## The Pipeline

```text
                  ┌──────────────────────── planning ────────────────────────┐
  rough idea ──▶  big-bang ──▶ goal-forge ──▶ goal-check ──▶ campaign ──▶ delivery
                  (options)    (GOAL.md)      (READY?)       (many goals)  (spec)
                                                                              │
                  ┌──────────────────────── delivery ────────────────────────┘
                  ▼
                slicer ──▶ factory ──▶ phase gate ──▶ polish ──▶ auditor ──▶ shipped
               (slices)   (commits)   (pass/fail)   (closeout)  (when due)
                  ▲                       │                        │
                  └────── rework ◀────────┴────────────────────────┘
```

| Step | Skill | Question it answers | Leaves behind |
| --- | --- | --- | --- |
| Explore | `big-bang` | What could this idea become, and which direction is strongest? | Branch records, decision ledger, handoff read |
| Define | `goal-forge` | What exactly are we building, in what architecture, and what proves it? | One goal document, usually `GOAL.md` |
| Check | `goal-check` | Can an implementer who wasn't in the conversation start from this goal? | A verdict (`READY`, `NOT READY`, or `NEEDS FURTHER REVIEW`) recorded in the goal's `Status` section |
| Coordinate | `campaign` | How do several related goals, bugs, and features land as one contract? | Campaign artifact with ordered stages |
| Specify | `delivery` | What are the units, write scopes, dependencies, and gates for one phase? | Repo-aware delivery spec |
| Slice | `slicer` | How do we cut the spec into small changes that can run independently? | Slice list (`<plan>.slices.md`) |
| Build | `factory` | How do we implement, sign off, commit, and gate the work, phase by phase? | Commits, a resumable ledger with per-phase checkpoints, status updates |
| Close out | `polish` | Can each changed file be made smaller, clearer, and better tested? | Per-file polish commits |
| Audit | `auditor` | Is the change correct, safe, integrated, and honestly evidenced? | Findings and a verdict |

The steps are entry points, not a strict chain. Skip what your work does not
need.

State lives in files. These are the default locations; a repo's own convention
wins, and each skill records the path it used:

| Artifact | Default location |
| --- | --- |
| Goal | `GOAL.md` (repo root or the repo's docs directory) |
| Campaign | `CAMPAIGN.md`, or `<name>.campaign.md` |
| Delivery spec | the repo's plans directory, for example `docs/plans/<name>.md` |
| Slice list | `<spec-stem>.slices.md`, next to the spec |
| Ledger | `<goal-stem>.ledger.md` (or `<campaign-stem>.ledger.md`), next to the goal or campaign: one per run, with a checkpoint per phase |
| Audit report | `<goal-or-campaign-stem>.audit.md`, else `audits/<base>..<head>.md` for an ad-hoc range |

One delivery spec is one factory phase, so a goal with several phases gets one
spec and one slice list per phase. Plan artifacts (goal, campaign, spec, slice
list) are committed when written or approved, as `docs(plan): <name>`. Ledger
and status edits are bookkeeping that ride along in slice commits or land as
`chore(ledger): <phase> <event>`.
## Where to Start

| Your situation | Start with |
| --- | --- |
| A vague idea with several possible directions | `big-bang` |
| One problem you can describe but haven't pinned down | `goal-forge` |
| A `GOAL.md` (yours or someone else's) you want to trust before building | `goal-check` |
| A pile of related goals, bugs, and features that must all land | `campaign` |
| One clear outcome that needs a concrete implementation plan | `delivery` |
| An approved plan you want cut into parallel, reviewable work | `slicer` |
| A grounded goal or spec you want built end to end | `factory` |
| A branch, diff, or commit range you want reviewed before you trust it | `auditor` |
| Files that work but could be leaner, clearer, or better tested | `polish` |
| A proposed change whose blast radius you want to know first | `consequences` |

## A Walkthrough

Here is one feature moving through the pipeline: *add per-tenant rate limiting
to an HTTP API.*

1. **Explore (optional).** If it is unclear whether you want rate limiting,
   quotas, or billing tiers, `big-bang` maps the options, pressure-tests the
   assumptions, and recommends a branch. Here the idea is already clear, so
   skip it.
2. **Define.** `goal-forge` talks the problem through with you, one question at
   a time. It checks the claims against the code, for example how the
   middleware is wired today and where tenant identity comes from. Then it
   writes `GOAL.md`: the desired end state, the architecture direction (a
   token bucket in middleware with a shared store), non-goals, acceptance
   criteria, the first useful milestone, and where the first edit happens.
3. **Check.** `goal-check` cold-reads `GOAL.md` as if it were a new
   implementer. If the store choice or the behavior over the limit is still
   open, the verdict is `NOT READY`, and it lists exactly what to settle.
   It records the verdict, evaluator mode, date, and gaps in the goal's
   `Status` section and edits nothing else: `goal-forge` (or you) settles
   those points, and `goal-check` runs again.
4. **Coordinate (when needed).** One goal needs no campaign. If rate limiting
   had to land together with quota billing and an admin UI, `campaign` would
   hold all three as one completion contract. It orders them into stages and
   tracks each to verified completion.
5. **Specify.** `delivery` resolves the goal against the live repo and saves a
   spec. The spec has units (limiter core, middleware wiring, configuration,
   metrics), each with a write scope, a named first edit, a done-when
   condition, and gates. This goal fits in one phase, so it gets one spec; a
   larger goal would get one spec per phase.
6. **Slice.** `slicer` re-reads the code and cuts the spec into slices. A
   foundation slice adds the shared types and the config entry. Then
   independent slices add the middleware, the metrics, and the tests, each
   with an exact list of files it may touch, and a final tidy slice cleans up
   the files the phase changed. Slices that share no files can run in
   parallel.
7. **Build.** `factory` asks (or infers) your commit unit, by default one
   commit per slice, and records it, with the phase base, in the ledger. Each
   slice is implemented (for new behavior, test first: the failing run is
   recorded before the code is written), signed off (diff inside its write
   scope, formatter, linter, and narrow check passing, its test passing, a
   read-only `correctness` read of the diff), and committed. A slice that fails
   sign-off goes back to its implementer, and after two failures it is split.
   When the phase's slices have landed, the phase gate runs over the phase's
   changes: verification, `poker-face`, review, checkpoint. A failed gate sends
   the findings to `slicer` rework, and the repairs land as new commits. After
   two failed gate cycles on the same finding, factory pauses for you. The
   ledger, with a checkpoint per phase, lets the work resume after a context
   reset.
8. **Close out.** With the phase committed, `polish` goes through the changed
   files one at a time. It removes what isn't needed, tightens names, and adds
   missing tests, with one commit per file.
9. **Audit.** Rate limiting is a security-sensitive surface, so an audit is due
   at the end of the goal. `auditor` reviews the committed range. Suppose it
   returns `residual` with a P2 finding: the limiter counts rejected requests
   against the quota, so a client over the limit stays locked out longer than
   the window. The finding goes to the ledger's deferred findings with an
   owner and a done-when, or, if you want it fixed now, `slicer` rework turns
   it into a repair slice and factory runs it. Because the fix touches a
   security-sensitive surface, the original range plus the repair is audited
   again. A `block_ship` verdict always goes through rework and the same
   re-audit.

Every step left a file in the repo. Any agent, or you next week, can pick up
from any point.

## The Skills

### Planning

#### `big-bang`: expand a rough idea

A planning and ideation skill for ideas that are still taking shape. It widens
the idea into named branches and pressure-tests the load-bearing assumptions.
At each branch point it makes a provisional choice and keeps exploring until
the strongest directions are ready for deeper planning. It writes no code.

- **Use when:** the center of the idea is still moving, or several directions
  are plausible.
- **Produces:** a design corpus of branch records, research briefs, risk
  registers, and a decision ledger. Each turn ends with a compact read:
  current read, branches, decision read, pressure test, artifacts, next
  redirects, and handoff read.
- **Hands off to:** `goal-forge` for one grounded goal, `delivery` for an
  implementation plan, or `factory` once a branch, phase set, and checkpoint
  policy exist.

#### `goal-forge`: converge on one goal

A guided conversation that locks the shape of **one** problem before any
execution. It gathers evidence from code, data, logs, and docs, and treats
conversation as intent rather than truth. It pressure-tests the problem, then
writes a single goal document. It works at the architecture and milestone
level, not file by file.

- **Use when:** intent is fuzzy and the outcome should be one bounded target.
- **Produces:** a goal artifact, usually `GOAL.md`. It covers the problem
  boundary, the desired end state, the architecture direction, key
  invariants, the first useful milestone and where its first edit happens, open
  decisions, and a `Status` section that goal-check, factory, and campaign update.
- **Hands off to:** `goal-check` for a readiness verdict, `campaign` when the
  pressure test reveals several tracks, or `delivery` or `factory` to build.

#### `goal-check`: is the goal ready?

A pre-implementation readiness check with a stricter bar than goal-forge. It
judges the goal and never edits its content. It asks whether an implementer
who was not in the conversation could start without inventing hidden scope, choosing the architecture, or guessing which
files to change. It is useful for second opinions, and for goals you haven't
looked at in a while, which it checks against today's code.

- **Use when:** before building from a goal document, especially one written
  by another person, agent, or model.
- **Produces:** a verdict: `READY`, `NOT READY` (with the specific gaps to
  fix), or `NEEDS FURTHER REVIEW` (when readiness depends on judgment it
  cannot verify). The verdict, evaluator mode, date, and gaps are recorded in
  the goal's `Status` section (or the ledger when one exists). It escalates
  uncertainty rather than bluffing.
- **Hands off to:** `delivery` or `factory` when ready. On `NOT READY` it
  lists the gaps, `goal-forge` (or you) fills them, and goal-check runs
  again.

#### `campaign`: one contract for many tracks

A completion contract and routing plan for several related goals, bugs,
features, or cleanup families. Every admitted item stays mandatory until it is
implemented and verified. Sequencing may split the work, but only an explicit
amendment can narrow it. Campaigns don't implement anything themselves. They
lower each stage into `delivery` or `factory`.

- **Use when:** one goal, spec, or factory run is too narrow for the work.
- **Modes:** *draft or maintain* (write or revise the artifact only) and
  *run* (verify progress from live evidence, then lower the next unblocked
  stage).
- **Produces:** a campaign artifact. It holds the desired end state, the
  scope and exclusions, the ground truth inspected, track states, ordered
  stages with dependencies and gates, and closeout conditions. As stages
  complete, it records evidence in the owning goal's `Status` section.
- **Completes:** only when every admitted item is implemented and verified,
  the audit due at campaign completion has run, and no independent-review item
  is left open. A coherent document, a named next stage, or partially passing
  tests does not count.

#### `delivery`: compile one outcome into a spec

Turns one bounded but messy unit of work, from a campaign stage or a goal
document, into a durable implementation specification, grounded in the live
repository. It runs six steps:
interpret, normalize, resolve against the repo, build a unit graph, assign
implementation units, and define checkpoints and gates. It plans only. One
spec covers one factory phase; a multi-phase goal gets one spec per phase.

- **Use when:** one coherent outcome needs a concrete, repo-aware plan before
  anyone writes code.
- **Produces:** a saved spec with an interpreted unit, normalized spec,
  repo-aware baseline, unit graph, implementation work, checkpoints and
  gates, validation, review lenses, and open questions. Each unit has a write
  scope, a named edit, a done-when condition, and an optional sanity check.
- **Ready when:** an implementer can begin the named edit without
  rediscovering the architecture.
- **Hands off to:** `slicer`, then `factory`.

### Build and Review

#### `slicer`: cut the plan into slices

Cuts an approved plan into **slices**: small changes an implementer can finish
from the brief alone. A slice is roughly 5 to 10 minutes of work, such as one
defect and its test or one mechanical edit across one or two files. Slicer
re-reads the code first, because plans go stale. It writes no code. "Slice"
means exactly this unit: larger chunks are called milestones (in a goal),
stages (in a campaign), units (in a delivery spec), and phases (in factory).

- **Use when:** between `delivery` and implementation, or whenever factory
  needs bounded worker assignments.
- **Modes:** *slice* (cut the whole plan), *rework* (turn audit findings,
  failed phase gates, or failing checks into repair slices), and *split*
  (replace a slice that fails sign-off twice, or that the implementer reports
  is larger than its brief).
- **Key rules:**
  - Slices that run at the same time never share a file.
  - A rename travels with all its call sites.
  - Shared foundations come first, then a wide fan-out.
  - Hot shared files are edited once or in a fixed order.
  - Tests travel with the code they test.
  - Every cut for a phase ends with a tidy slice: the cleanliness lens on the
    files the phase changed, no behavior change.
- **Produces:** `<plan>.slices.md`. Each slice has an id, title, write scope,
  dependencies, a `red_first` flag, and a self-contained brief naming files,
  functions, the failing input, and the test to add.

#### `factory`: build it, phase by phase

Owns sustained implementation, from an execution-ready goal or campaign stage
to verified, coherent commits. It runs one phase at a time: select the phase,
compile it through delivery and slicer if needed, run the slices, evaluate the
phase gate, and move on. It keeps a ledger so the work survives context
resets.

- **Use when:** a grounded goal or spec should be built end to end.
- **Commit unit:** your choice, recorded in the ledger at the start of a run.
  `per-slice` is the default: each slice is committed after sign-off, so
  nothing waits for the end of a goal that may take days. `per-phase` commits
  once when the phase gate passes. `user-commits` stages and reports, and you
  commit. A phase always has its work committed before polish runs. A slice
  is *landed* when it is signed off; it is *committed* separately, so in
  `per-phase` and `user-commits` modes a slice can be landed before its commit
  exists.
- **Order:** for each slice, `implement → sign-off → commit`. Then the phase
  gate over the phase's commits: `verification → poker-face → review →
  checkpoint`. A passing phase goes to `polish`, then an `auditor` pass when
  due. `housekeeping` runs only between phases, on a clean tree.
- **Slice sign-off:** the diff (minus ledger and slice-file bookkeeping) stays
  inside the slice's write scope, the formatter, linter, and narrow check pass
  on those files, the slice's test exists and passes (and for new behavior or
  a bug fix a failing run was recorded first, per the brief's `red_first`
  flag), and a read-only `correctness` read of the diff finds nothing blocking.
- **Bookkeeping:** slice commits carry the slice's files plus the status line
  and ledger entry they updated. Gate results are committed as
  `chore(ledger): <phase> <event>`, plan artifacts as `docs(plan): <name>`, and
  the audit report as `docs(audit): <range>`.
- **Failures:** a slice that fails sign-off goes back to its implementer, and
  after two failures to `slicer` split. A failed phase gate goes to `slicer`
  rework, and repairs land as new commits; landed commits are never rewritten.
  After two failed gate cycles on the same finding, factory pauses for you.
- **Produces:** commits, one ledger per run (`<goal-stem>.ledger.md`) with a
  checkpoint per phase, goal and campaign status updates, a release decision
  (release now, prepare a release, defer, or not applicable), and a
  completion report.

#### `polish`: per-file closeout

A per-file improvement loop with a subtractive bias. Each changed file passes
through correctness, cleanliness, housekeeping, tests, and docs, and ends in
one commit. The first question is always what can leave: dead code, redundant
abstraction, and unused fields or helpers.

- **Use when:** after a phase has been committed, or on any files that work
  but could be leaner, clearer, or better tested. Polish runs on committed
  work only, and its commits contain only polish.
- **Produces:** one commit per changed file, marked with a `Polish-Primary:`
  trailer. Inspected files with no useful change are recorded and skipped;
  that record is committed as `polish: record inspected files` when a pass
  makes no other polish commit. A bug found while polishing is not fixed in a
  polish commit: it goes to `slicer` rework as a repair slice.
- **Tools:** `scripts/suggest-polish-files.py` ranks candidate files, and
  `scripts/polish-inspected.py` records what was inspected. Run them as
  `python3 <skill-dir>/scripts/<script>.py --repo <repo-root>`, where
  `<skill-dir>` is where the skill is installed.

#### `auditor`: independent review

A rigorous, read-only audit of a diff, branch, or commit range. It asks
whether the change is correct, safe, integrated, and honestly evidenced. It
checks behavior, invariants, data, concurrency, interfaces, configuration,
integration, tests and evidence (including any weakened tests), security, and
resources. It reports; you decide.

- **Use when:** an audit is due: at goal or campaign completion, at release
  gates, on risk signals (auth, permissions, data migration, persistence,
  concurrency, public API or schema changes, security-sensitive input), or when
  you ask. It is optional per phase otherwise. It also works on a candidate
  branch or as an independent second opinion.
- **Produces:** findings ranked by severity (P0 to P2) and a verdict:
  - `block_ship`: a confirmed or likely serious defect, failed validation, or
    an unreviewed critical surface;
  - `residual`: no ship blocker, but findings or bounded uncertainty remain;
  - `clean_pass`: complete coverage, validation passed, no actionable
    findings. This never means the whole repo is correct.
- **After the audit:** `block_ship` goes to `slicer` rework, a repair phase,
  and a re-audit of the original range plus the repairs. `residual` findings go
  to the ledger's deferred findings, each with an owner and an observable
  done-when. A residual fixed now goes through rework, with a re-audit if the
  fix touches a risk-signal surface. `clean_pass` is recorded in the ledger.
  The auditor only writes its report file; factory commits it.
- **Single agent:** when the auditor also wrote the change, it reports
  `Evaluator mode: self-audit` and rebuilds the requirements from the plan and
  diff before reading any summary. For auth, permissions, tenancy, data
  migration, persistence formats, or security-sensitive input, a self-audit
  cannot return `clean_pass`: the best result is `residual` with an
  "independent review required" item. Such items stay open as `blocking-later`
  for release gates and goal or campaign closeout, and closeout waits until a
  separate reviewer signs off or you accept the item by name.

### Review Lenses

Lenses are focused passes that factory, auditor, and polish call at set points.
Each one also works on its own.

| Lens | What it does | Notes |
| --- | --- | --- |
| `correctness` | Hunts real behavioral bugs, invariant breaks, races, and data-loss risks. Not general cleanup. | Language references for Go, Python, Rust, and TypeScript. Can split a large review by domain. |
| `poker-face` | Checks completed work against what was promised. It rebuilds the requirement checklist from the original plan and compares each item with the repo. | Skipped only when no goal, spec, or acceptance criteria exist. High misses block. A medium miss is deferred only with your approval (or when the plan already names it as deferred), and a medium that breaks an acceptance criterion always blocks. Low ones are noted. |
| `cleanliness` | Shapes code for managed complexity without changing behavior: boundaries, file and function size, dispatch, helpers, guard clauses, naming. | Has a read-only scanner mode and a Rust structure census script. |
| `housekeeping` | Full maintenance cycle at major inflection points. It runs a mechanical block (format, lint fix, build, never tests), then test-boundary hygiene, then a banned-pattern ratchet. | Hygiene ratchet templates for Go, Python, Rust, and TypeScript. Budgets only go down. |
| `consequences` | Traces forward from a proposed change: what else must move, what breaks, and what follow-on work is missing. Read-only. | Run before risky designs, migrations, or API and schema changes. |
| `red-green` | Testability and coverage work through red-green loops. It maps the test surface, removes testability blockers, and authors and verifies tests in two waves. New behavior and bug fixes need a test seen failing first. | Broad and incremental modes. Ends at a clearance gate. |

## Principles

- **The repo is ground truth.** Goals, campaigns, and specs record intent.
  Code, tests, and history record what exists. When they disagree, the repo
  wins and the document is the defect.
- **Scope is a contract.** Admitted work stays mandatory until it is
  implemented and verified. Campaign stages may sequence it. They may not
  quietly drop it.
- **Plans end in edits, not more discovery.** A spec is ready when an
  implementer can start a named edit without rediscovering the architecture.
- **Tests prove the target.** Never weaken a test or a gate to get a green run.
  Auditors check for exactly that. New behavior and bug fixes need a test seen
  failing before the change.
- **Commit early, at the unit you choose.** Goals can take days, so work is
  committed per slice by default (or per phase, or by you), never held until
  the end. A phase is committed before polish runs. Plans and bookkeeping are
  committed too, so the repo shows where the run stands.
- **Git safety.** Never `reset --hard`, `checkout -- .`, `restore` over
  others' work, `clean`, `stash`, `rebase`, amend a landed commit, or
  force-push. Never discard changes you did not make. Fix forward with new
  commits.
- **Every step leaves an artifact.** State lives in files, not chat: the goal
  and its `Status` section, the spec, the slice list, the ledger's per-phase
  checkpoints. The work survives context limits, handoffs, and restarts.
- **Uncertainty escalates.** A step that cannot verify something says so and
  names the decision a person must make, rather than bluffing.
- **Subtract first.** Cleanup asks what can leave before it asks what to add.

## One Agent or Many

Every skill works with one agent in one repository.

If your harness supports subagents, some steps use them, but none require
them:

- `goal-check` and `auditor` prefer an independent reviewer for second
  opinions.
- `factory` can hand slices to parallel workers when slicer has given them
  disjoint write scopes.
- `correctness` can split a large review by domain.

Without subagents, the same work runs serially, and independence is kept
honestly rather than skipped:

- `auditor` reports `Evaluator mode: self-audit` when the agent that wrote the
  change audits it, rebuilds requirements before reading summaries, and cannot
  return `clean_pass` on auth, permissions, tenancy, data migration,
  persistence, or security-sensitive changes without an independent reviewer
  (another agent or model, or you).
- `goal-check`, `poker-face`, and `red-green` Wave 2 run a self-contained cold
  pass and report `Evaluator mode: self-contained cold pass`. At the phase gate
  `poker-face` is skipped only when no goal, spec, or acceptance criteria
  exist; lack of delegation is not a reason to skip it.

## Install

### Claude Code

Add this repository as a plugin marketplace, then install the plugin:

```text
/plugin marketplace add ianzepp/shipyard
/plugin install shipyard@shipyard
```

Claude loads a skill when your request matches it. You can also name one, for
example *"use goal-forge to pin down this feature"*.

### Codex and other harnesses

Clone the repository and link each skill folder into your harness's skill
directory. For Codex:

```bash
git clone https://github.com/ianzepp/shipyard ~/shipyard
for s in ~/shipyard/skills/*/; do ln -s "$s" ~/.codex/skills/; done
```

Then invoke a skill by name, for example `$goal-forge` or `$factory`.

## Repository Layout

```text
skills/
  <name>/
    SKILL.md            name, description, and the procedure the agent follows
    references/         detail loaded only when needed
    scripts/            deterministic helpers (polish, cleanliness)
    agents/openai.yaml  display metadata for harnesses that use it
.claude-plugin/         Claude Code plugin and marketplace manifests
```

## License

MIT
