# Shipyard

Agent skills for the engineering process: the planning, delivery, and review
work that turns an idea into shipped code.

You bring a rough idea, or a large feature nobody has scoped yet. Shipyard
gives your coding agent (Claude Code, Codex, Cursor, or any harness that reads
skill files) a disciplined path from that idea to verified commits:

```text
idea → explore → goal → readiness check → campaign → spec → slices → build → audit → polish → shipped
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

Shipyard counters each of these with a stage that has a clear contract, a
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
                slicer ──▶ factory ──▶ auditor ──▶ polish ──▶ shipped
               (slices)   (commits)   (verdict)   (closeout)
                  ▲                       │
                  └──── rework ◀──────────┘
```

| Stage | Skill | Question it answers | Leaves behind |
| --- | --- | --- | --- |
| Explore | `big-bang` | What could this idea become, and which direction is strongest? | Branch records, decision ledger, handoff read |
| Define | `goal-forge` | What exactly are we building, in what architecture, and what proves it? | One goal document, usually `GOAL.md` |
| Check | `goal-check` | Can an implementer who wasn't in the conversation start from this goal? | `READY`, `NOT READY`, or `NEEDS FURTHER REVIEW` |
| Coordinate | `campaign` | How do several related goals, bugs, and features land as one contract? | Campaign artifact with ordered stages |
| Specify | `delivery` | What are the units, write scopes, dependencies, and gates for one outcome? | Repo-aware delivery spec |
| Slice | `slicer` | How do we cut the spec into small changes that can run independently? | Slice list (`<plan>.slices.md`) |
| Build | `factory` | How do we implement, verify, review, and commit, phase by phase? | Commits, a resumable ledger, status updates |
| Audit | `auditor` | Is the change correct, safe, integrated, and honestly evidenced? | Findings and a verdict |
| Close out | `polish` | Can each changed file be made smaller, clearer, and better tested? | Per-file polish commits |

The stages are entry points, not a strict chain. Skip what your work does not
need.

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
   criteria, and the first useful milestone.
3. **Check.** `goal-check` cold-reads `GOAL.md` as if it were a new
   implementer. If the store choice or the behavior over the limit is still
   open, the verdict is `NOT READY`, and it names exactly what to settle.
4. **Coordinate (when needed).** One goal needs no campaign. If rate limiting
   had to land together with quota billing and an admin UI, `campaign` would
   hold all three as one completion contract. It orders them into stages and
   tracks each to verified completion.
5. **Specify.** `delivery` resolves the goal against the live repo and saves a
   spec. The spec has units (limiter core, middleware wiring, configuration,
   metrics), each with a write scope, a named first edit, a done-when
   condition, and gates.
6. **Slice.** `slicer` re-reads the code and cuts the spec into slices. A
   foundation slice adds the shared types and the config entry. Then
   independent slices add the middleware, the metrics, and the tests, each
   with an exact list of files it may touch. Slices that share no files can
   run in parallel.
7. **Build.** `factory` runs the phase loop. It implements the slices, runs
   `correctness`, verifies with tests that fail before the change and pass
   after it, reviews the diff, and commits only a coherent, verified phase.
   Its ledger lets the work resume after a context reset.
8. **Audit.** `auditor` reviews the commit range. Suppose it returns
   `residual` with a P2 finding: the limiter's clock is not injectable in
   tests. `slicer`'s rework mode turns the finding into a repair slice, and
   factory runs it.
9. **Close out.** `polish` goes through the changed files one at a time. It
   removes what isn't needed, tightens names, and adds missing tests, with one
   commit per file.

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
  invariants, the first useful milestone, and open decisions.
- **Hands off to:** `goal-check` for a readiness verdict, `campaign` when the
  pressure test reveals several tracks, or `delivery` or `factory` to build.

#### `goal-check`: is the goal ready?

A pre-implementation readiness check with a stricter bar than goal-forge. It
asks whether an implementer who was not in the conversation could start
without inventing hidden scope, choosing the architecture, or guessing which
files to change. It is useful for second opinions, and for goals you haven't
looked at in a while, which it checks against today's code.

- **Use when:** before building from a goal document, especially one written
  by another person, agent, or model.
- **Produces:** a verdict: `READY`, `NOT READY` (with the specific gaps to
  fix), or `NEEDS FURTHER REVIEW` (when readiness depends on judgment it
  cannot verify). It escalates uncertainty rather than bluffing.
- **Hands off to:** `delivery` or `factory` when ready. Otherwise it goes back
  to `goal-forge`.

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
  stages with dependencies and gates, and closeout conditions.
- **Completes:** only when every admitted item is implemented and verified.
  A coherent document, a named next stage, or partially passing tests does
  not count.

#### `delivery`: compile one outcome into a spec

Turns one bounded but messy unit of work into a durable implementation
specification, grounded in the live repository. It runs six stages:
interpret, normalize, resolve against the repo, build a stage graph, assign
implementation units, and define checkpoints and gates. It plans only.

- **Use when:** one coherent outcome needs a concrete, repo-aware plan before
  anyone writes code.
- **Produces:** a saved spec with an interpreted unit, normalized spec,
  repo-aware baseline, stage graph, implementation work, checkpoints and
  gates, validation, review lenses, and open questions. Each unit has a write
  scope, a named edit, a done-when condition, and an optional sanity check.
- **Ready when:** an implementer can begin the named edit without
  rediscovering the architecture.
- **Hands off to:** `slicer`, then `factory`.

### Delivery

#### `slicer`: cut the plan into slices

Cuts an approved plan into **slices**: small changes an implementer can finish
from the brief alone. A slice is roughly 5 to 10 minutes of work, such as one
defect and its test or one mechanical edit across one or two files. Slicer
re-reads the code first, because plans go stale. It writes no code.

- **Use when:** between `delivery` and implementation, or whenever factory
  needs bounded worker assignments.
- **Modes:** *slice* (cut the whole plan), *rework* (turn audit findings or
  failing checks into repair slices), and *split* (replace a slice that ran
  far past its target).
- **Key rules:**
  - Slices that run at the same time never share a file.
  - A rename travels with all its call sites.
  - Shared foundations come first, then a wide fan-out.
  - Hot shared files are edited once or in a fixed order.
  - Tests travel with the code they test.
- **Produces:** `<plan>.slices.md`. Each slice has an id, title, write scope,
  dependencies, and a self-contained brief naming files, functions, the
  failing input, and the test to add.

#### `factory`: build it, phase by phase

Owns sustained implementation, from an execution-ready goal or campaign stage
to verified, coherent commits. It runs one phase at a time: select the phase,
compile it through delivery if needed, implement, verify, review, close out,
evaluate the checkpoint, and commit. It keeps a ledger so the work survives
context resets.

- **Use when:** a grounded goal or spec should be built end to end.
- **Lens order inside a phase:**
  `implement → correctness → verification → poker-face → review →
  cleanliness → housekeeping → polish → checkpoint → commit`.
  poker-face runs when completion must be reconstructed, and housekeeping
  runs at phase or lifecycle boundaries.
- **Gates:** new behavior normally needs a failing proof first and a passing
  proof afterward. A phase with failed correctness, verification, or
  checkpoint gates is not committed unless you explicitly accept the named
  risk.
- **Produces:** commits, goal and campaign status updates, a release decision
  (release now, prepare a release, defer, or not applicable), and a
  completion report.

#### `auditor`: independent review

A rigorous, read-only audit of a diff, branch, or commit range. It asks
whether the change is correct, safe, integrated, and honestly evidenced. It
checks behavior, invariants, data, concurrency, interfaces, configuration,
integration, tests and evidence (including any weakened tests), security, and
resources. It reports; you decide.

- **Use when:** after a change lands, before trusting a candidate branch, or
  for an independent second opinion.
- **Produces:** findings ranked by severity (P0 to P2) and a verdict:
  - `block_ship`: a confirmed or likely serious defect, failed validation, or
    an unreviewed critical surface;
  - `residual`: no ship blocker, but findings or bounded uncertainty remain;
  - `clean_pass`: complete coverage, validation passed, no actionable
    findings. This never means the whole repo is correct.
- **Hands off to:** `slicer` rework mode for repair slices.

#### `polish`: per-file closeout

A per-file improvement loop with a subtractive bias. Each changed file passes
through correctness, cleanliness, housekeeping, tests, and docs, and ends in
one commit. The first question is always what can leave: dead code, redundant
abstraction, and unused fields or helpers.

- **Use when:** after a phase or merge, or on any files that work but could
  be leaner, clearer, or better tested.
- **Produces:** one commit per changed file, marked with a `Polish-Primary:`
  trailer. Inspected files with no useful change are recorded and skipped.
- **Tools:** `scripts/suggest-polish-files.py` ranks candidate files, and
  `scripts/polish-inspected.py` records what was inspected.

### Review Lenses

Lenses are focused passes that factory, auditor, and polish call at set points.
Each one also works on its own.

| Lens | What it does | Notes |
| --- | --- | --- |
| `correctness` | Hunts real behavioral bugs, invariant breaks, races, and data-loss risks. Not general cleanup. | Language references for Go, Python, Rust, and TypeScript. Can split a large review by domain. |
| `poker-face` | Checks completed work against what was promised. It rebuilds the requirement checklist from the original plan and compares each item with the repo. | Classifies misses as high, medium, or low. Material misses send the work back to implementation. |
| `cleanliness` | Shapes code for managed complexity without changing behavior: boundaries, file and function size, dispatch, helpers, guard clauses, naming. | Has a read-only scanner mode and a Rust structure census script. |
| `housekeeping` | Full maintenance cycle at major inflection points. It runs a mechanical block (format, lint fix, build, never tests), then test-boundary hygiene, then a banned-pattern ratchet. | Hygiene ratchet templates for Go, Python, Rust, and TypeScript. Budgets only go down. |
| `consequences` | Traces forward from a proposed change: what else must move, what breaks, and what follow-on work is missing. Read-only. | Run before risky designs, migrations, or API and schema changes. |
| `red-green` | Testability and coverage work through red-green loops. It maps the test surface, removes testability blockers, and authors and verifies tests in two waves. | Broad and incremental modes. Ends at a clearance gate. |

## Principles

- **The repo is ground truth.** Goals, campaigns, and specs record intent.
  Code, tests, and history record what exists. When they disagree, the repo
  wins and the document is the defect.
- **Scope is a contract.** Admitted work stays mandatory until it is
  implemented and verified. Stages may sequence it. They may not quietly drop
  it.
- **Plans end in edits, not more discovery.** A spec is ready when an
  implementer can start a named edit without rediscovering the architecture.
- **Tests prove the target.** Never weaken a test or a gate to get a green run.
  Auditors check for exactly that.
- **Every stage leaves an artifact.** State lives in files, not chat, so the
  work survives context limits, handoffs, and restarts.
- **Uncertainty escalates.** A stage that cannot verify something says so and
  names the decision a person must make, rather than bluffing.
- **Subtract first.** Cleanup asks what can leave before it asks what to add.

## One Agent or Many

Every skill works with one agent in one repository.

If your harness supports subagents, some stages use them, but none require
them:

- `goal-check` and `auditor` prefer an independent reviewer for second
  opinions.
- `factory` can hand slices to parallel workers when slicer has given them
  disjoint write scopes.
- `correctness` can split a large review by domain.

Without subagents, the same work runs serially.

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
