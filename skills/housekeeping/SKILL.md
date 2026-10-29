---
name: "housekeeping"
description: "Full repository maintenance cycle at major inflection points: mechanical block (fmt, lint --fix, build/check — never tests), then test-boundary hygiene (move inline tests out of production code), then banned-pattern ratchet."
---

# Housekeeping

Full maintenance cycle for **major inflection points**. Run phases in order.
Commit after each successful phase that changes the tree. Stop and ask the user
if a failure is ambiguous or a fix needs product judgment.

| Related | Relationship |
|---|---|
| When to run | Run full housekeeping only at **major inflection points** (goal or campaign complete, large merge spanning several features, stage closeout, user ask). Not after every change — cost is about that of a large implementation unit. Prefer **one phase per task** when possible. A mechanical-only pass is Phase 1. |
| `$polish` | Deeper per-file quality (test decomposition, missing tests, docs) is `$polish`, not this skill. Housekeeping enforces test **boundaries**; polish improves test **quality**. |
| Docs | README / documentation truth passes are their own tasks, not phases here. Verify doc claims against live code. |

Dependency and lockfile policy: [$dependency-policy](references/dependency-policy.md).

## Pipeline Order

| Order | Phase | Notes |
|---|---|---|
| 1 | **Mechanical block** | fmt → lint `--fix` → build/check → generate (if named) → report. **Never tests.** |
| 2 | **Test boundary hygiene** | Move inline tests out of production files; thin wiring only; structural check |
| 3 | **Banned-pattern ratchet** | Run hygiene against non-test code; reduce or lower budgets, never raise |
| 4 | **Completion report** | Aggregate mechanical + hygiene results |

**Order matters.** Test boundary hygiene runs **before** the banned-pattern
ratchet. The hygiene script scopes bans to non-test code; tests living inline
in production files surface as `expect`/`panic` violations that look like "fix
these" when the real fix is "move these tests." Never count or ratchet over
unmigrated inline tests.

| Gate | Rule |
|---|---|
| Mechanical stops (dirty tree / judgment / out-of-scope dirt) | Resolve with the user and re-run, or abort the cycle — **do not skip to hygiene on a red build** |
| Hygiene fails | Narrow hygiene tests only; fix or stop — never weaken the ratchet |

## Phase Summary

| # | Phase | Action | Commit |
|---|---|---|---|
| **1** | Mechanical block | 1.1 Refresh → 1.2 Orient → 1.3 Verify env → 1.4 Lint `--fix` → 1.5 Build → 1.6 Format → 1.7 Generated → 1.8 Report | `style: format` / `chore: lint --fix` / `chore: regenerate` |
| **2** | Test boundary hygiene | Extract inline tests to dedicated test files; verify thin wiring only | `test: extract inline tests to dedicated files` |
| **3** | Banned-pattern ratchet | Run hygiene; reduce violations; lower budgets (never raise) | `chore: reduce hygiene debt` / `test: add hygiene ratchet` |

A large lint backlog is its own project, not a housekeeping phase.

## Global Rules

| # | Rule | Do | Never |
|---|---|---|---|
| 1 | Tooling | Prefer **local** fmt/lint/build commands for the frozen root (from manifests + short AGENTS notes for *those* commands only) | CI archaeology; inventing suite runs from CI matrices |
| 2 | Foreign changes | Report and stop | Overwrite, revert, stash, or ignore unrelated local changes |
| 3 | Staleness | Rely on the 1.1 refresh first; re-check before judgment edits | — |
| 4 | Monorepos | One named root per task | Cross-repo freestyle |
| 5 | Caches | — | Delete or mutate caches or environments outside the repo unless the user asks |
| 6 | Blockers | Stop and ask when: local changes/untracked/merge/rebase in progress; unrelated edits interfere; step unusually expensive/disruptive/ambiguous | Stash automatically; merge or rebase without asking |
| 7 | Skips | No test harness → skip Phases 2–3 and say so; mechanical already skipped build → do not invent one | Skip the mechanical block and still claim full housekeeping |
| 8 | Mechanical boundary | Hygiene phases may edit beyond the mechanical freeze only with explicit full-HK scope | Use housekeeping to sneak product refactors |

## Phase 1: Mechanical Block

Mechanical verify / fix / format for a **frozen scope**. Be literal. Do not design products.

**Invariant.** Success is **command-defined**. If a fix needs product or
architecture judgment → **stop**, report, do not freestyle.

**The mechanical block never runs tests.** Not full suites, not filters, not
"cheap default `cargo test`," not CI test jobs. Tests belong to the implementer's
closeout, Phases 2–3 when they choose, auditors, or CI — not the mechanical
block. Large repos (thousands of tests) make accidental suite runs especially
costly.

### Scope Contract (task must freeze)

| Field | Required |
|---|---|
| **Repo root** | Exact path (monorepo: one package or sibling repo, not the whole container unless asked) |
| **Allowed paths** | Exact paths or "whole clean repo" |
| **Generators** | Optional explicit script path |

Outside freeze → inventory and **stop** (uncommitted changes you did not make: never erase them).

There is **no** test-filter field. Do not accept or invent one.

### Mechanical steps

| # | Step | Action | Commit |
|---|---|---|---|
| 1.1 | Refresh | Status + optional ff-only pull | — |
| 1.2 | Orient | Toolchain + HEAD | — |
| 1.3 | Verify env | Build/check **commands** only (not tests) | — |
| 1.4 | Lint auto | Repo linter `--fix` only | `chore: lint --fix` if tree changed |
| 1.5 | Build | Repo build/check command | — |
| 1.6 | Format | Repo formatter | `style: format` if tree changed |
| 1.7 | Generated | Named repo-native generator only | with related work or `chore: regenerate` |
| 1.8 | Report | Commands, pass/fail, SHAs, files | — |

**There is no tests step.** Do not add one.

### 1.1 Repository Refresh

| # | Step | Action | Gate |
|---|---|---|---|
| 1 | Worktree | `git rev-parse --show-toplevel` | Exists; matches task root |
| 2 | Status | `git status --short --branch` | — |
| 3 | Dirty outside freeze | List paths; **stop** | User decision |
| 4 | Dirty inside freeze only | Continue (task owns that dirt) | — |
| 5 | Clean + upstream | `git fetch` → `git pull --ff-only` | Fast-forward OK |
| 6 | Diverged / pull fails | **Stop**, report | — |
| 7 | Record | `git log --oneline -1` | HEAD captured |

### 1.2 Orient

| # | Step | Action | Gate |
|---|---|---|---|
| 1 | Detect | Read manifests (`Cargo.toml`, `package.json`, `go.mod`, `pyproject.toml`) | Toolchain known |
| 2 | Commands | List **fmt / lint --fix / build-or-check** only for this root | Commands listed |
| 3 | Record | Start HEAD hash | Captured |

No long planning essay. One short toolchain line is enough.
Do **not** inventory `.github/workflows` or decide which CI jobs apply.

### 1.3 Verify Environment

Run **verify** only (per language), from the frozen root — **compile/check, not test**:

| Language | Prefer |
|---|---|
| Rust | Repo-standard `cargo check` / `cargo build` (or narrow `-p` if the freeze says so). **Never `cargo test`.** |
| TS/JS | Lockfile-strict install only if the task requires; then project **build** (not test) |
| Go | `go build` (not `go test`) |
| Python | Project env sync only if already standard; then project **check/build** (not pytest) |

Follow [$dependency-policy](references/dependency-policy.md) **clean-environment
command table** only.
**Never:** upgrade packages for freshness; weaken locks; invent release-age
config; run tests "to verify env."

Fail → capture log → **stop** (unless a one-line mechanical fix under the freeze
— see Tiny Fix Rule).

### 1.4 Lint Auto-Fix Only

Run (existing tools only):

| Language | Command |
|---|---|
| Rust | `cargo clippy --fix --allow-dirty -- -D warnings` **or** the repo's documented local clippy one-liner; if clippy fails policy-only, report — do not rewrite APIs |
| TS/JS | Project lint with `--fix` if supported |
| Go | `golangci-lint run --fix` if present; else skip |
| Python | `ruff check --fix .` if present |

If no linter configured → **skip** (do not bootstrap).
If auto-fix rewrites files → inspect diff → commit `chore: lint --fix` only if
purely mechanical.

**Never:** add eslint/prettier/ruff config; "fix remaining warnings" by redesign.

### 1.5 Build Verification

| Language | Command |
|---|---|
| Rust | `cargo build` / `cargo check` or repo variant (not test) |
| TS/JS | Project build script |
| Go | `go build ./...` or narrower task path |
| Python | Configured build or skip |

Green → continue. Red → Tiny Fix Rule or stop + report.

### 1.6 Format

| Language | Command |
|---|---|
| Rust | `cargo fmt` |
| TS/JS | Project formatter, else skip if none |
| Go | `gofmt -w` on allowed paths |
| Python | `ruff format` if present |

Inspect formatter diff. Huge unrelated churn → **stop**, do not commit.
Else commit `style: format` when files changed.

### 1.7 Generated Outputs

| Rule | Detail |
|---|---|
| When | The task **names** the generator script |
| Scope | Only outputs that script already owns and the repo tracks |
| Never | New artifact types; surprise lockfile edits |

### Tiny Fix Rule

Allowed **only** when all hold:

1. Error points inside **frozen** paths
2. Fix is mechanical (fmt artifact, missing import the compiler names, clippy
   auto-fix leftover)
3. **≤ ~15 lines** total
4. Re-run the failing **build/lint** command → green

Otherwise: **stop**, report the residual to the user.

### 1.8 Report

| Category | Content |
|---|---|
| Scope | Repo, freeze, HEAD before/after |
| Commands | Exact commands + pass/fail |
| Commits | Count + short hash + subject each |
| Files | Touched paths |
| Residuals | Failures, out-of-scope dirt, judgment needed |
| Not claimed | Product correctness, **any test results**, full suite, public claim truth |
| Tests | Always: **not run** (the mechanical block does not run tests) |

### Mechanical-only task shape

A task scoped to Phase 1 only is a mechanical-only pass:

```text
Repo: <absolute root>
Freeze: paths | whole clean repo
Commands (optional overrides): fmt / lint / build-or-check / generator
Done when: format + lint --fix + build/check green, or fail report with logs
Never: tests
Commit: style:/chore: only on allowed paths
```

## Phase 2: Test Boundary Hygiene

Read [$test-boundary-hygiene](references/test-boundary-hygiene.md) before
counting or moving anything. The hygiene script scopes bans to non-test code;
inline tests in production files are a **boundary violation**, not a budget line.

| Rule | Do | Never |
|---|---|---|
| Embedded tests | Scan production trees → **move** every inline test to a dedicated test file | Raise budgets; delete tests; swap `unwrap` for silent drops; defer extraction |
| Wiring | Leave only thin wiring (Rust: `#[cfg(test)] #[path = "foo_test.rs"] mod tests;` with **no inline body**) | Leave partial inlines |
| Re-test | Re-run the relevant test suite after each extraction batch | Assume moved tests pass |
| Structural ratchet | Add/extend the structural inline-test check so inline tests cannot return | Skip the structural guard |

Move test bodies verbatim into the dedicated test file (see the remediation
steps in the reference) — mechanical relocation beats retyping. Proof: test
count before == test count after.

Per-language detection commands: see
[$test-boundary-hygiene](references/test-boundary-hygiene.md).

Commit: `test: extract inline tests to dedicated files`.

## Phase 3: Banned-Pattern Ratchet

| State | Sequence |
|---|---|
| **No ratchet** | (1) Test boundary hygiene must be complete → (2) Set each budget to current production-only totals (not arbitrary zero) → (3) Scope scans to production files; exclude dedicated test filenames → (4) Include the required structural inline-test check → (5) Run the new hygiene test → (6) Commit: `test: add hygiene ratchet` |
| **Ratchet exists** | (1) Run → (2) If tests in production → back to Phase 2, re-run → (3) Reduce production violations; never raise budget → (4) Lower the budget constant when code beats it → (5) Commit: `chore: reduce hygiene debt` or `test: extract inline tests to dedicated files` |

Use bundled references: Rust: [$hygiene-rs](references/hygiene-rs.md), TS/JS:
[$hygiene-ts](references/hygiene-ts.md), Go: [$hygiene-go](references/hygiene-go.md),
Python: [$hygiene-py](references/hygiene-py.md).

**Source file size:** flag production files ~1000+ lines when a natural split
helps. Not test files. Not intentional dispatcher/orchestrator files.

Skip when there is no practical test harness or the language is unsupported.

## Phase 4: Completion Report

| Category | Content |
|---|---|
| Mechanical | 1.8 report summary (commands, style/chore commits, pass/fail) |
| Hygiene | Test boundary: inline tests extracted; structural ratchet status. Ratchet: budget before→after |
| Commits | Count + short hashes |
| Build + tests | Final status (tests: which narrow suites ran) |
| Changes | By category: lint, correctness, tests, formatting, docs |
| Dependencies | Cooldown/lock notes; advisories |
| Deferred | Manual follow-up |

## Anti-Patterns

**Workspace:** stashing uncommitted changes you did not make; merging/rebasing through divergence;
skipping the 1.1 refresh before judgment edits; raising hygiene budgets;
deleting tests instead of extracting them.

**Composition:** running Phases 2–3 on a red mechanical build; using full
housekeeping for routine post-unit fmt (use a Phase 1-only task); treating
housekeeping as a license for README research, test-quality passes, or docs
(those are separate docs tasks or `polish`).

**Phases:** running the banned-pattern ratchet over unmigrated inline tests;
skipping the structural inline-test ratchet after extraction; repo-wide bug
hunts; over-engineering decomposition.
