---
name: slicer
description: Cut an approved plan (a delivery spec, a factory phase, or a settled issue) into small self-contained implementation slices with exact write scopes and a dependency graph. Also re-cuts work after a failed review or check (rework) and replaces a slice that failed sign-off twice or proved larger than its brief (split). Use between delivery and implementation, or when factory needs bounded worker assignments. Planning only; writes no code.
---

# Slicer

Slicer cuts an approved plan into slices: small changes that an implementer
finishes from the brief alone, in parallel where the files allow it. It
re-reads the code, cuts the work, and saves a slice list. It does not plan,
judge the plan, or write code. One delivery spec is one factory phase, so it
gets one slice list; a goal with several phases has one spec and one slice
file per phase.

Flow: `campaign → delivery → slicer → factory → review → (rework via slicer)`.

Use `delivery` first when the outcome is not yet specified. Skip slicer when
the whole change is already one slice.

## Units, Phases, and Slices

- A **delivery unit** is one logical change.
- A **factory phase** is the unit of verification; commits follow the user's
  commit unit.
- A **slice** is the unit of implementation inside a phase. One unit becomes
  one slice or several.

Slices cut the plan; they never widen it. Factory integrates the slices and
owns phase verification, review, and commits.

A slice is **landed** when it is signed off and the slice file records it.
Committed is a separate fact that follows the commit unit the user chose for
the run (see factory's [commit rules](../factory/SKILL.md#commits)). Factory's
[slice sign-off](../factory/references/loop.md#running-a-slice-list) decides
when a slice has landed. The words "land", "landed", and "must land first"
below mean this, and `deps` wait for landed, not for a commit.

## Modes

Each request is one mode over one plan.

- **Slice.** Input: the plan, the repositories in scope, and the size target.
  Cut the whole remaining plan. The plan and your briefs are the only
  description of the work the implementers will have.
- **Rework.** The build did not pass, or an implementer could not stay inside
  its scope. The input is one or more of:
  - (a) review findings and failing check output, with the slices already
    landed. Cut slices that fix exactly those findings and failures.
  - (b) a blocked-scope report: the slice, the paths it asked for, its reason,
    and the current write scope of every slice in the run.
  - (c) one follow-up an implementer found outside its slice (its paths and
    need). Slice it inside this plan, or escalate it as new intake.

  Inputs (b) and (c) come from factory's
  [slice runner](../factory/references/loop.md#running-a-slice-list), which
  rejects any diff outside `write_scope` and passes the report on.

  Answer with replacement slices (ids `<old id>.<n>`, which take over the old
  slice's deps) or extra slices (ids `<prefix>-<n>`, new and unused). Do not
  re-cut work that already landed and passed. Do not widen the plan.
- **Split.** One slice failed sign-off twice, or its implementer reported that
  it is larger than its brief. The input holds that slice and what its
  attempts left behind. Replace it with two to four smaller slices
  that together do all of its work. They take over its deps, and anything that
  depended on the old slice now depends on the replacements. Ids are
  `<old id>.1`, `<old id>.2`. Keep the same repository.

## Check the Code First

Read the project's own agent instructions (`AGENTS.md`, `CLAUDE.md`,
`README.md`, whichever exist) once before you slice. Every brief must follow
them.

Re-read the code before you cut. The plan was written earlier, and line
numbers, file names, and function names in it may have moved. A brief must
name what is in the checkout now. If part of the plan is already delivered,
leave it out and say so in one line in the notes. If the plan and the code
disagree in a way the code cannot settle, escalate and say what disagrees.

## Scope Rules

- **One slice is one change a mid-level implementer can finish in the size
  target.** The default is 5 to 10 minutes of work; use the project's own
  target when it has one. A slice is one defect and its test, or one
  mechanical edit across one or two files. If in doubt, cut smaller and chain
  the pieces with `deps`.
- **Write scopes that run in parallel are disjoint.** Two slices may run at
  the same time only if their write scopes share no file. If two slices must
  touch the same file, chain them with `deps`, or move both edits into one
  slice.
- **A rename travels with its call sites.** The slice that renames a name (a
  function, type, constant, flag, or registry row) also updates every use, and
  its write scope covers them all. Never cut a rename into "add the new name"
  and "switch callers later", and never leave an alias or a second spelling.
  If the call sites are many, it is still one slice. When that slice is too
  large, make the rename its own early slice and chain the dependent work
  after it.
- **Foundation first, then a wide fan-out.** Put shared types, module
  skeletons, new files that others import, and registry rows in a first slice
  or a short chain. Everything that only builds on them depends on the
  foundation and runs in parallel with its siblings. Keep the longest chain as
  short as the plan allows.
- **Hot shared files go to the foundation or to ordered slices.** A file many
  slices would edit (a registry, dispatcher, command table, module list, or
  CLI definition) is edited once, in the foundation, with the hook points
  later slices need. Otherwise its edits are chained in a fixed order. Never
  let sibling slices race for it. A slice that needs one module line or one
  call site in a file it does not own means the foundation is missing that
  line.
- **Keep files under the project's size limit.** A slice that would push a
  file over a limit named in the project's instructions puts its logic in a
  new file inside its scope, and adds only the module line and the call to the
  old file.
- **Everything a slice calls must be reachable from its file.** Every
  function, type, or module a slice calls must be visible from the slice's
  file, including visibility and re-exports. If it is not, the visibility edit
  goes into that slice's write scope (when no sibling needs the same line), or
  into the foundation.
- **Tests travel with the code.** Each write scope includes the test files the
  slice adds or changes, placed where the project's instructions say tests
  live. A slice with no test says why in its brief; sign-off accepts that when
  the existing tests covering its `write_scope` pass (see factory's
  [slice sign-off](../factory/references/loop.md#running-a-slice-list)).
- **Every cut for a phase ends with a tidy slice.** See
  [The Tidy Slice](#the-tidy-slice).
- **No dependency crosses repositories.** A slice works in exactly one
  repository, and its write scope is relative to it. When the plan needs one
  repository's change to land before another can use it, escalate: that is a
  release step, not a slice edge.

## Slice Fields

Each slice has exactly these fields:

- `id`: unique and stable. `<prefix>-<n>`, where the prefix is a short stem of
  the plan's name. Rework and split use `<old id>.<n>`.
- `title`: under 100 characters.
- `repo`: the repository, only when the plan spans more than one.
- `write_scope`: the exact files the slice may change, tests included. A
  directory only when the files cannot be known. If a change regenerates a
  generated file, list that file and name the command in the brief.
- `deps`: ids of slices that must land first. Use it for real dependencies and
  to chain slices that share a file. No cycles. In rework, never name a slice
  that already landed.
- `red_first`: `yes` or `no`. `yes` for new behavior or a bug fix: the
  slice's test is written and seen failing before the change. `no` for
  mechanical edits, renames, docs, and the tidy slice.
- `brief`: self-contained. See below.
- `status`: one line in the slice file, kept current by factory's
  [slice runner](../factory/references/loop.md#running-a-slice-list): `pending`
  | `in-progress` | `landed <short hash>` | `landed (uncommitted)` |
  `blocked-scope` | `split into <ids>` | `reworked by <ids>`. Slicer writes
  `pending`. `landed (uncommitted)` is a signed-off slice whose commit does not
  exist yet, or whose own commit cannot record its hash (see
  [commits](../factory/SKILL.md#commits)); it becomes `landed <short hash>`
  once committed and recorded.

## The Tidy Slice

Every cut for a phase ends with a slice whose id is `<prefix>-tidy`. Factory
runs it like any slice, last.

- `deps`: every other slice in the cut.
- `red_first`: `no`.
- `write_scope`: the files the phase changes (the union of the other slices'
  write scopes), plus new files under the same directories, so extracted
  helpers have a home.
- `brief`: apply the [cleanliness](../cleanliness/SKILL.md) lens to those
  files with no behavior change. Name the narrow check and say the existing
  tests covering the scope must pass unchanged. A behavior change found while
  tidying is not made; the implementer reports it as a follow-up for rework.

Leave the tidy slice out only when the phase changes no source files (a
docs-only phase), and say so in the notes. A rework or split cut adds no tidy
slice of its own; if the tidy slice has not landed, the cut adds the repair
slices to its `deps` and says so in the notes.

## The Brief

The implementer has not seen the plan and will not. Every brief:

- names the files and functions, with line numbers from the current checkout;
- says what is wrong, with a concrete failing input, or what is missing;
- says what to change;
- names the test to add and what it asserts (a stable error type, code, or
  observable result, never message text);
- states `red_first`, and when it is `yes`, the reason the test must fail
  before the change, so the runner can confirm it fails for that reason
  (factory's [slice runner](../factory/references/loop.md#running-a-slice-list)
  records the failing output);
- quotes a decision's exact words when the slice implements one;
- lists the rules from the project's instructions that bind the edit;
- names the narrow check (a narrow build or one focused test). For the
  implementer it is advice, to run while working; factory's sign-off runs it
  as a gate before the slice is committed;
- ends with the scope rule: change only the files in `write_scope`. If the
  work needs any other path, change nothing and report `blocked-scope` with
  the paths and the reason. Report work found outside the slice as a
  follow-up instead of doing it. Never reset, restore, clean, stash, rebase,
  or amend, and never discard changes you did not make.

## Escalate

Stop and return the plan to its owner (the delivery spec, the campaign, or the
user) instead of slicing when:

- the plan and the code disagree and the code cannot settle it;
- a slice would need a dependency across repositories;
- the work cannot be cut into slices of the size target;
- a rework request is a design change the plan did not settle;
- in rework mode, nothing remains to cut.

An empty slice list is never a way to skip work. Escalation names what
disagrees and the choice a person must make.

## Output

Save the slice list as Markdown next to the plan it cuts, as
`<plan-stem>.slices.md` (the default; a repository's own convention wins).
One spec has one slice file. Record the path used in the slice file header;
factory creates the ledger at intake and copies that path into it.
Rework and split append a new section to the same file rather than rewriting
landed slices. The layout and worked examples are in
[references/format.md](references/format.md).

The slice file is a plan artifact: it is committed when written, as
`docs(plan): <name>`, following the user's commit unit (staged and reported in
user-commits mode); see factory's [commit rules](../factory/SKILL.md#commits).
Afterwards its `status` lines are bookkeeping paths, committed with each slice
rather than as separate plan commits.

## Ready

The slice list is ready only when:

- every remaining plan item is in exactly one slice, or is noted as already
  delivered;
- no two slices that can run at the same time share a file;
- the deps graph has no cycle and its longest chain is as short as the plan
  allows;
- every brief names code that exists in the checkout now;
- every slice carries a test or says why not, and sets `red_first`;
- a slice-mode cut ends with the tidy slice, or the notes say why not.

Finish with a short response: the path to the slice list, the slice count, the
longest chain, and any escalation. Do not paste the slice list into chat.
