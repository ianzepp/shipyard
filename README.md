# Shipyard

Agent skills for the engineering process: the planning, delivery, and review
work that turns an idea into shipped code.

You bring a rough idea, or a large feature nobody has scoped yet. Shipyard
gives your coding agent (Claude Code, Codex, Cursor, or any harness that reads
skill files) a disciplined path from that idea to verified, accepted changes:

```text
idea → explore → goal → readiness check → campaign → spec → slices → build → phase gate → polish → audit when due → closeout → shipped
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
                slicer ──▶ factory ──▶ phase gate ──▶ polish ──▶ auditor ──▶ closeout
               (slices)   (accepts)   (pass/fail)   (per file)  (when due)  (shipped)
                  ▲                       │                        │
                  └────── rework ◀────────┴────────────────────────┘
```

| Step | Skill | Question it answers | Leaves behind |
| --- | --- | --- | --- |
| Explore | `big-bang` | What could this idea become, and which direction is strongest? | Branch records, decision ledger, handoff read |
| Define | `goal-forge` | What exactly are we building, in what architecture, and what proves it? | One goal document, `GOAL.md` |
| Check | `goal-check` | Can an implementer who wasn't in the conversation start from this goal? | A verdict (`READY`, `NOT READY`, or `NEEDS FURTHER REVIEW`) recorded in the goal's `Status` section |
| Coordinate | `campaign` | How do several related goals, bugs, and features land as one contract? | Campaign artifact with ordered stages |
| Specify | `delivery` | What are the units, write scopes, dependencies, and gates for one phase? | Repo-aware delivery spec |
| Slice | `slicer` | How do we cut the spec into small changes that can run independently? | Slice list (`phase-<n>.slices.md`) |
| Build | `factory` | How do we implement, sign off, and gate the work, phase by phase, and close the goal out? | Accepted slices, a resumable ledger with per-phase checkpoints, status updates |
| Polish | `polish` | Can each changed file be made smaller, clearer, and better tested? | Per-file polish changes |
| Audit | `auditor` | Is the change correct, safe, integrated, and honestly evidenced? | Findings and a verdict |

The steps are entry points, not a strict chain. Skip what your work does not
need.

State lives in files. `goal-forge` picks a short kebab-case goal name (for
example `csv-export`), and everything for that goal lives in one directory.
These are the default locations; a repo's own convention wins, and each skill
records the path it used:

```text
docs/goals/<goal-name>/
  GOAL.md                  the goal
  ledger.md                factory's ledger: one per run, with a checkpoint per phase
  phase-<n>.md             delivery spec for phase n
  phase-<n>.slices.md      slice list for phase n
  repair-<n>.slices.md     slice list for a repair phase after a failed audit
  audit.md, audit-<n>.md   audit reports; a re-audit never overwrites
docs/campaigns/<campaign-name>/
  CAMPAIGN.md              the campaign
  ledger.md                when factory runs the campaign
```

An ad-hoc audit of a range with no goal can write `audits/<base>..<head>.md`.
`.polish-inspected.json` stays at the repo root.

One delivery spec is one factory phase, so a goal with several phases gets one
spec and one slice list per phase. These files, plus status edits and audit
reports, are bookkeeping: they are excluded from a slice's scope check and
travel with the work they document (through the same pull request), unless the
repo or you say otherwise.

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
| One small, clear change | just make it: a single small change can skip `factory`. Use `factory` when you want the full lifecycle (slices, gates, audit, closeout). |

## Workflow

Shipyard does not dictate your version control. It needs a **workflow**: how
changes are isolated, made durable, and integrated. The agent running `factory`
settles the details at intake and records them in the ledger's `Workflow`
section (its source, the branch layout if any, how a slice's changes are
isolated for sign-off, when work becomes durable, the integration points, and
who records changes), so a later agent can follow them.

**Precedence:** the repo's own instructions (AGENTS.md, CLAUDE.md,
CONTRIBUTING, branch protection, existing practice), then your stated
preference, then the agent's choice from the structures below.

**What the process needs from any workflow:**

1. Accepted work is durable (a commit, a merge, or a checkpoint, defined under
   structure C below) before anything that depends on it starts.
2. A slice's own changes can be isolated for sign-off, new untracked files
   included. If the workflow cannot do that, slices run one at a time and the
   agent records the changed paths at each start and acceptance.
3. A phase has a base and a reviewable change set, from where it started to
   the current accepted state, for the phase gate.
4. An audit gets a frozen ref or range that nobody changes during the audit.
5. Polish and housekeeping run only when no slice is in progress and the
   phase's work is accepted.

A slice is **accepted** when it passes sign-off and its changes are made
durable per the workflow. Whatever the workflow, never destroy or overwrite
work you did not make, never rewrite history that is accepted, integrated, or
shared, and never force-push a shared branch: fix forward. On a private
work-in-progress branch, history edits are a workflow choice.

If your repo uses its own words for these units ("task", "story", "unit"), the
agent maps them onto slice and phase and records the mapping in the ledger.

**Recommended structures** (suggestions; the agent may adapt them):

**A. Branch per slice** (recommended for multi-slice or multi-day work):

```text
main
└── <prefix>/main                         optional integration branch
    └── <prefix>/<feature>/main           feature branch; accepted slices merge here
        └── <prefix>/<feature>/<slice-id> one branch per slice (sibling of .../main)
```

Git cannot have a branch `a/b` and a branch `a/b/c` at the same time, so the
feature branch and its slice branches are siblings. A slice branch starts from
the feature branch. Sign-off diffs the slice branch against its base, and
acceptance merges it into the feature branch; the feature-branch tip after that
merge is the slice's ref. Slices with disjoint write scopes can run on parallel
branches. Commit freely inside a slice branch. When the feature is accepted, it
merges into the integration branch, and a pull request goes from the
integration branch (or from the feature branch when there is no integration
branch) to `main`.

**B. One feature branch, a commit per accepted slice** (small or medium work):
slices run one at a time, a slice's changes are the diff since the previous
accepted slice, and acceptance is the commit.

**C. The agent does not commit** (you integrate): the agent never waits for you
to commit. Instead it takes **checkpoints**. A checkpoint is an id for a saved
snapshot of the working tree. It touches no branch, no index, and no working
file, and it includes new untracked files (but not ignored ones). One way to
take one:

```bash
idx="$(git rev-parse --git-dir)/shipyard-index"
GIT_INDEX_FILE="$idx" git add -A && GIT_INDEX_FILE="$idx" git write-tree
```

That prints a tree id. The agent records it as the slice's ref
(`accepted tree:<id>`), and a slice's own changes are the diff between the
previous checkpoint and the new one. Audits use checkpoints as their base and
head. You can commit whenever you like, per slice, per phase, or at the end;
on resume, the checkpoint ids in the slice file and ledger are the authority.
Unreferenced tree objects can be garbage-collected after a few weeks, so
checkpoints are for the duration of the work, and the ledger also keeps each
slice's changed-path list as a fallback.

A suggested slice commit message in committing workflows is
`<type>(<scope>): <slice title>` with a `Slice: <id>` trailer, which lets a
later agent resume from the log.

Planning skills (`goal-forge`, `goal-check`, `campaign`, `delivery`, `slicer`)
only write their artifacts and leave them in place. `goal-forge` does not
create or switch branches. Factory intake records the artifacts per the
workflow (on the feature branch in A and B, in a checkpoint in C).

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
   writes `docs/goals/rate-limiting/GOAL.md`: the desired end state, the architecture direction (a
   token bucket in middleware with a shared store), non-goals, acceptance
   criteria, the first useful milestone, and where the first edit happens.
3. **Check.** `goal-check` cold-reads the goal as if it were a new
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
7. **Build.** `factory` settles the workflow at intake and records it, with
   the phase base, in the ledger. For a feature this size the agent might use a
   branch per slice under one feature branch (structure A). Each slice is
   implemented (for new behavior, test first: the failing run is recorded
   before the code is written), signed off (changes inside its write scope,
   formatter, linter, and narrow check passing, its test passing, a read-only
   `correctness` read of the diff), and accepted. A slice that fails sign-off
   goes back to its implementer, and after two failures it is split once; a
   split slice that fails again escalates to you. When the phase's slices are
   accepted, the phase gate runs over the phase's changes: verification,
   `poker-face`, review, checkpoint. A failed gate sends the findings to
   `slicer` rework, and the repairs are new slices; accepted work is never
   rewritten. After two failed gate cycles on the same finding the verdict is
   `NEEDS FURTHER REVIEW` and factory pauses. You can accept the named risk
   (recorded), amend the scope or plan, give direction for another rework
   attempt (which resets that finding's count), or stop. If you give
   direction, your recorded ruling counts as settling the design for that
   finding and becomes input to `slicer` rework; it is recorded once, in the
   phase's checkpoint in the ledger. The ledger, with a checkpoint per phase,
   lets the work resume after a context reset.
8. **Polish.** With the phase accepted and no slice in progress, `polish` goes
   through the changed files one at a time. It removes what isn't needed,
   tightens names, and adds missing tests (one commit per changed file is
   recommended where you commit). If it finds a real bug after the gate has
   passed, it pauses and first makes the polish edits already finished durable.
   Then `slicer` rework cuts a repair slice in the same phase and the
   checkpoint is marked reopened. Once the repair is accepted, the gate reruns:
   `poker-face` and review cover the repair slices' own changes, verification
   covers the whole phase change set, and the finished polish is listed as
   accepted polish, not re-reviewed as phase work. Then polish resumes.
9. **Audit.** Rate limiting is a security-sensitive surface, so an audit is due
   at the end of the goal. `auditor` reviews a frozen range. Suppose it
   returns `residual` with a P2 finding: the limiter counts rejected requests
   against the quota, so a client over the limit stays locked out longer than
   the window. The finding goes to the ledger's deferred findings with an
   owner and a done-when, or, if you want it fixed now, `slicer` rework turns
   it into a repair slice and factory runs it. Because the fix touches a
   security-sensitive surface, the original range plus the repair is audited
   again, and the new report is `audit-2.md`. A `block_ship` verdict starts a
   repair phase (its plan is the audit's findings, its slices in
   `repair-<n>.slices.md`) and the same re-audit. A residual you want fixed now
   runs as a repair phase too. Two `block_ship` verdicts on the same finding
   pause for you, as above.
10. **Closeout.** Factory is complete when, in order: (1) all phases are
    accepted; (2) housekeeping, if due, has run, scoped by default to the paths
    the goal changed; (3) the goal-completion audit is resolved (`clean_pass`,
    or residuals deferred with owner and done-when, and independent-review
    items closed or accepted by you by name); (4) the work is integrated per
    the workflow (merge, and a pull request only when the workflow says so or
    you ask); (5) the goal's `Status` says `complete <ref>`, the integrated
    ref (or the final checkpoint when the agent does not commit); (6) the
    ledger is closed with the integration state recorded, and the bookkeeping
    files are durable per the workflow. The audit that runs mid-goal is for
    risk signals; the goal-completion audit runs here, after housekeeping.

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
- **Produces:** a goal artifact, `docs/goals/<goal-name>/GOAL.md`. It covers the problem
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
  the audit due at campaign completion is resolved (see factory closeout), and
  no independent-review item is left open unless you accept it by name. A
  coherent document, a named next stage, or partially passing tests does not
  count.

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
  is larger than its brief; one level only, and a split slice that fails
  again escalates).
- **Key rules:**
  - Slices that run at the same time never share a file.
  - A rename travels with all its call sites.
  - Shared foundations come first, then a wide fan-out.
  - Hot shared files are edited once or in a fixed order.
  - Tests travel with the code they test.
  - Every cut for a phase ends with a tidy slice: the cleanliness lens on the
    files the phase changed, no behavior change (it may restructure tests
    without changing what they assert, and adds none). A repair phase has no
    tidy slice.
- **Produces:** `phase-<n>.slices.md`. Each slice has an id, title, write scope,
  dependencies, a `red_first` flag, and a self-contained brief naming files,
  functions, the failing input, and the test to add.

#### `factory`: build it, phase by phase

Owns sustained implementation, from an execution-ready goal or campaign stage
to verified, accepted changes. It runs one phase at a time: select the phase,
compile it through delivery and slicer if needed, run the slices, evaluate the
phase gate, and move on. It keeps a ledger so the work survives context
resets.

- **Use when:** a grounded goal or spec should be built end to end.
- **Workflow:** how changes are isolated, made durable, and integrated. The
  agent settles it at intake (repo instructions, then your preference, then
  its own choice) and records it in the ledger; see [Workflow](#workflow).
  Goals can take days, so accepted work is made durable before anything that
  depends on it starts. A phase's work is accepted before polish runs.
- **Order:** for each slice, `implement → sign-off → accept`. Then the phase
  gate over the phase's changes: `verification → poker-face → review →
  checkpoint`. A passing phase goes to `polish`, then an `auditor` pass when
  due. `housekeeping` runs only between phases, when no slice is in progress.
- **Slice sign-off:** the slice's changes (minus bookkeeping files) stay
  inside its write scope, the formatter, linter, and narrow check pass on
  those files, the slice's test exists and passes (and for new behavior or
  a bug fix a failing run was recorded first, per the brief's `red_first`
  flag), and a read-only `correctness` read of the diff finds nothing blocking.
- **Failures and caps:** a slice that fails sign-off goes back to its
  implementer, and after two failures to `slicer` split (one level only). A
  failed phase gate goes to `slicer` rework, and repairs are new slices;
  accepted work is never rewritten. Two failed gate cycles on the same
  finding, or two `block_ship` audits on it, give `NEEDS FURTHER REVIEW` and
  factory pauses for you: accept the named risk, amend the scope or plan, give
  direction for another attempt, or stop. The ruling is recorded in the ledger.
- **Closeout:** the goal is complete only when all phases are accepted,
  housekeeping (if due) and the goal-completion audit are done and resolved,
  the work is integrated per the workflow, the goal's `Status` is
  `complete <ref>`, and the ledger is closed; see factory
  [Closeout](skills/factory/SKILL.md#closeout).
- **Produces:** accepted slices, one ledger per run (`ledger.md` in the goal's
  directory) with a checkpoint per phase, goal and campaign status updates, a release
  decision (release now, prepare a release, defer, or not applicable), and a
  completion report.

#### `polish`: per-file improvement

A per-file improvement loop with a subtractive bias. Each changed file passes
through correctness, cleanliness, housekeeping, tests, and docs, and ends in
one commit where you commit (a recommendation), or a recorded change where the
agent does not. The first
question is always what can leave: dead code, redundant abstraction, and
unused fields or helpers.

- **Use when:** after a phase has been accepted, or on any files that work
  but could be leaner, clearer, or better tested. Polish runs on accepted
  work only, when no slice is in progress, and keeps its edits separate from
  slice work.
- **Produces:** in a committing workflow, one commit per changed file is
  recommended, marked with a `Polish-Primary:` trailer (needed only for
  `suggest-polish-files.py` ranking; without it, ranking falls back to
  `.polish-inspected.json`). The changed and inspected files are recorded in
  `.polish-inspected.json`, written at the end of the pass. Where the agent
  does not commit, that file's timestamps may go stale after you commit, so the
  analyzer re-suggests those files, which is harmless.
  Inspected files with no useful change are recorded and skipped. A bug found
  while polishing is not fixed by polish: it pauses and goes to `slicer`
  rework as a repair slice in the same phase (see the walkthrough).
- **Tools:** `scripts/suggest-polish-files.py` ranks candidate files, and
  `scripts/polish-inspected.py` records what was inspected. Run them as
  `python3 <skill-dir>/scripts/<script>.py --repo <repo-root>`, where
  `<skill-dir>` is where the skill is installed.

#### `auditor`: independent review

A rigorous, read-only audit of a frozen diff, branch, or commit range. It asks
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
- **After the audit:** `block_ship` goes to `slicer` rework, a repair phase
  (planned from the audit's findings, no new spec), and a re-audit of the
  original range plus the repairs; two `block_ship` verdicts on the same
  finding pause for you. `residual` findings go
  to the ledger's deferred findings, each with an owner and an observable
  done-when. A residual fixed now goes through rework, with a re-audit if the
  fix touches a risk-signal surface. `clean_pass` is recorded in the ledger.
  The auditor only writes its report file (a re-audit writes
  `audit-<n>.md`); the requester records it per the workflow. Goal
  closeout needs the due audit resolved; see factory [Closeout](skills/factory/SKILL.md#closeout).
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
| `housekeeping` | Full maintenance cycle at major inflection points. It runs a mechanical block (format, lint fix, build, never tests), then test-boundary hygiene, then a banned-pattern ratchet. | Hygiene ratchet templates for Go, Python, Rust, and TypeScript. Budgets only go down. Where you commit, a commit after each step (with `style:` or `chore:` subjects) is recommended, not required. |
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
- **Accepted work is durable.** Goals can take days, so each accepted slice is
  made durable per the workflow before anything depends on it, never held
  until the end of the goal. The workflow is the repo's, then yours, then the
  agent's, and it is recorded in the ledger.
- **Git safety.** Never destroy or overwrite work you did not make. Never
  rewrite history that is accepted, integrated, or shared, and never
  force-push a shared branch. Fix forward.
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
