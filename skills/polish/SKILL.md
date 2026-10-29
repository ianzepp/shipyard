---
name: polish
description: Disciplined per-file improvement loop with a subtractive bias — correctness → cleanliness → housekeeping → tests → docs → commit. Use for polish, polish pass, polish loop, or polishing specific files.
---

# Polish

One primary source file per iteration. Supporting edits only when directly coupled: tests, fixtures, helpers, technical docs. Source comments and file-level documentation belong to the primary file, not the supporting-doc allowance. If work escapes this boundary → stop, report.

**Polish runs on committed work only.** Run it after a [factory](../factory/SKILL.md) phase gate passes (see its [order](../factory/SKILL.md#order)), or on files the user names. Its commits contain only polish. If a target file has uncommitted changes that you did not make (the user or another process), stop and report; never fold them into a polish commit. In `user-commits` mode, run polish only after the user has committed the phase; polish then stages one file at a time and reports, and the user commits.

**Git safety.** Never `reset --hard`, `checkout -- .`, `restore` over others' work, `clean`, `stash`, `rebase`, amend a landed commit, or force-push. Never discard changes you did not make. Fix forward with new commits.

## File list

| Rule | Action |
|---|---|
| Explicit list | Use user-provided files |
| Repo/package/dir | Derive via repo conventions |
| Exclude | Generated, vendored, lock, build, cache, fixture-only, third-party |
| Ordering | Stable sort; serial traversal |

## Unit of work

| Scope | Allowed | Forbidden |
|---|---|---|
| **Primary** | One source file per loop | — |
| **Supporting** | Matching unit/integration tests; fixtures/helpers for those tests; technical docs describing the file or its test coverage; caller/callee adjustments preserving contract | Unrelated neighboring cleanup; broad refactors; repo-wide hygiene; general-concept docs |

## Per-file loop

| # | Step | Gate |
|---|---|---|
| 0 | Confirm the file's changes are committed and none are foreign | Clean target; else stop and report |
| 1 | Read file + nearby tests + related docs + surrounding context | Understand contract |
| 2 | `correctness` → behavioral bugs, invariant breaks, race risks, data-loss risks | No silent regressions |
| 3 | `cleanliness` lens applied to this one file → **subtractive first**: what can leave (dead code, redundant abstraction, fields/imports/helpers with no user)? Then naming, structure, complexity. No behavior change; aesthetic-only churn is not a reason to edit | Local maintainability ↑; every survivor defended |
| 4 | `housekeeping` lens → stale patterns, test/production boundary (per the repo's convention), repo convention drift | Hygiene aligned |
| 5 | Create/update directly matching tests | Useful coverage for changed behavior |
| 6 | Review source presentation under repository policy; update directly related technical docs | Charter/rationale/contract not stale or invented |
| 7 | Targeted validation only: file + related tests | Short explicit timeout; no full suite |
| 8 | Review diff for scope; keep only this unit's changes | No leak to other files |
| 9 | Commit cohesive change (polish only) | Continue to next file |

No useful change → record inspected, skip. No forced commit.

**A bug found in step 2 is not a polish edit.** Stop work on that file, record the finding, and route it to [slicer](../slicer/SKILL.md#modes) rework mode (a) as a repair slice. When polish runs inside [factory](../factory/SKILL.md), factory runs that repair slice through sign-off and the phase gate (see its [phase gate](../factory/references/loop.md#phase-gate)); standalone, report the finding to the user. Polish commits stay polish-only; never mix a fix into one.

## Design taste

Polish defaults to **removal**. This skill treats absence as the default and makes every survivor defend itself. Apply that bias inside the per-file boundary:

| Principle | Per-file application |
|---|---|
| **Subtractive first** | Before improving, ask what can leave: dead code, redundant abstraction, fields/imports/helpers that exist without a user. Default answer to "add X" is "no, unless." |
| **Defended survivors** | Every retained dependency, field, public symbol, and abstraction needs evidence of a caller, contract, or invariant. This is an analysis gate, not a demand for a source comment. No evidence → removal candidate. |
| **Don't unify different masters** | Within the file, split types/helpers that serve different constraints (request vs. response, wire vs. in-memory, config vs. runtime). **Cross-file** false unifications (e.g. one struct doing wire + routing jobs): flag in the report, do not fix — that exceeds the file boundary. |
| **Make bad states unconstructable** | Where a runtime check catches an invalid state, prefer a type or constructor that prevents it — only when no behavior change. Validate-after is a smell; construct-correct is the target. |
| **Comments preserve grounded rationale** | A comment that restates the code is noise. Keep comments for non-obvious constraints, rejected alternatives, invariants, safety, recovery, or supported history. Delete comments that only paraphrase the next line. Never invent a rationale merely because the code looks unusual. |
| **Leave a ratchet** | When polish establishes or hardens a rule (no bare `.unwrap`, no `json!` macro, no silent `let _ =`), leave a **shrink-only budget test** behind where the repo's test runner allows it. Budgets only decrease, never grow. Ratchets make polish compound across passes; prose rules decay. |

**Load-bearing guard:** before deleting code whose purpose is not obvious, classify it — *load-bearing absence* (correctly absent, e.g. no transport in a pure library) vs. *deferred dirt* (a missing layer someone still has to build). Defensive synchronization, fallback branches, and validation often look incidental and carry hidden load. When evidence is insufficient, preserve the code and report the candidate. Add a rationale comment only when callers, tests, canonical docs, history, or an explicit invariant support it.

## Source presentation

Polish follows the owning repository's source-documentation policy. A project may
define stricter documentation rules; follow them.

Review source presentation after correctness and structure are settled:

- keep or refine an existing file charter when it still describes stable ownership
- add a charter when repository policy requires one and inspected evidence supports it
- use conceptual section headings only when they improve navigation
- preserve comments for constraints, rejected alternatives, invariants, safety,
  recovery, algorithms, or supported history
- remove narration, name paraphrase, volatile inventories, and movable numbering
- update directly related external docs only when the primary-file change makes
  their contract stale

Claim strength must not exceed inspected evidence. Declarations and tests can
support visible behavior; architectural ownership requires neighboring modules
and canonical docs; rejected alternatives and history require explicit records.
A smaller or mechanically assigned agent may maintain accepted charters and
obvious local comments, but must escalate ambiguous ownership or rationale
rather than writing plausible prose.

A documentation-only improvement to the primary source file is a valid polish
change. A repository-wide documentation retrofit, cross-module ownership rewrite,
or general-concept document remains outside the one-file boundary.

## Test discipline

| Rule | Do | Never |
|---|---|---|
| Frequency | Targeted per-file checks; broader validation once after all files or at batch boundary | Full suite after every file |
| Scope | Exact test filter, single-package test, linter on touched file, focused typecheck | Unbounded runs |
| Timeout | Explicit short timeout via repo wrapper or shell tool | Hung suites |
| Exception | Shared infrastructure where targeted checks give no signal → broaden, report why | Silent broadening |

## Commit rule

Commit after each changed primary file. Include: primary + supporting tests, fixtures, helpers, docs. In `user-commits` mode, stage the primary and supporting files for that one file, report, and let the user commit before moving to the next file.

| Element | Format |
|---|---|
| Subject | `polish(scope): concise improvement` |
| Scope | Crate, module, package, or primary subsystem |
| Primary trailer | `Polish-Primary: src/parser/nodes.rs` (exactly one) |
| Supporting trailer | `Polish-Supporting: path/to/file` (optional) |

Path-limited staging: stage only the primary file and its supporting files. Lock-producing git: serialize within the repo.

## Reporting candidates

`scripts/suggest-polish-files.py` ranks tracked files by churn since last recognized polish commit. `<skill-dir>` is where this skill is installed (for the Claude Code plugin, `${CLAUDE_PLUGIN_ROOT}/skills/polish`); `<repo-root>` is the repository being polished:

```bash
python3 <skill-dir>/scripts/suggest-polish-files.py --repo <repo-root>
python3 <skill-dir>/scripts/suggest-polish-files.py --repo <repo-root> --json --limit 15
```

Recognized: `polish(scope):…`, legacy `Polish …`, reversed `<scope>: polish …`, any commit with `Polish-Primary:` trailer. Score = routing suggestion, not quality verdict.

Exclude generated or unpolishable files with a repo-root `.polishignore` (gitignore-style globs, `#` comments, blank lines) or repeatable `--exclude <glob>` flags. Excluded files are dropped from candidates entirely and counted in the stderr summary.

For Rust repositories, the cleanliness-owned structural census is an optional
companion (`<skills-root>` is the directory holding the installed skills; point `--path` at the source root):

```bash
python3 <skills-root>/cleanliness/scripts/rust-structure-census.py \
  --repo <repo-root> --path <source-root> --limit 30
```

Keep the signals separate. `suggest-polish-files.py` measures churn since
polish; the census measures current structural review pressure. High churn plus
structural pressure is a strong per-file candidate. High pressure with little
churn usually belongs in a deliberate cleanliness package rather than an
incidental polish edit. Census thresholds are review triggers, not quality
verdicts.

Run the analyzer after a large merge to pick candidates, then polish them one file at a time.

### Recording inspected files

When a file is inspected through the full per-file loop and found clean (no changes needed, no commit), record it so the analyzer does not flag it again:

```bash
python3 <skill-dir>/scripts/polish-inspected.py \
  --repo <repo-root> --files src/foo.rs src/bar.py
```

This creates or updates `.polish-inspected.json` in the repo root. `suggest-polish-files.py` auto-detects this file and suppresses entries whose inspection timestamp is newer than the file's last git modification.

**Prune stale entries** (removes files modified after inspection):
```bash
python3 <skill-dir>/scripts/polish-inspected.py --repo <repo-root> --prune
```

**List current inspections:**
```bash
python3 <skill-dir>/scripts/polish-inspected.py --repo <repo-root> --list
```

Whoever runs the pass **must** record every file it inspects and finds clean during a polish pass. `.polish-inspected.json` is a polish artifact, so it stays within the polish-only rule. Commit it with the pass's last polish commit; when the pass makes no other polish commit, commit it alone as `polish: record inspected files` (no `Polish-Primary:` trailer). In `user-commits` mode, stage it and report.

## Progress reporting

| When | Report |
|---|---|
| After each file | Primary file completed; supporting files changed; validation: ran/deferred/broadened with reason; commit hash+subject or skip reason; boundary issues |
| End of cycle | Run broader validation once; summarize: completed files, inspected-unchanged, skipped, validation coverage, all commits |

## Anti-patterns

**Loop:** skip correctness for cleanliness, defer tests past commit, run full suite per file, force commit on unchanged file, polish files outside the bounded list, scope leak to unrelated files, silent test broadening, delete code whose load-bearing purpose is unconfirmed.
**Source presentation:** narrate code, demand comments for every survivor, invent rationale or history, copy changing inventories into prose, rewrite cross-module charters inside one file's loop.
**Commit:** omit `Polish-Primary:` trailer on a primary-file commit, fold a bug fix into a polish commit, `polish` type on non-polish commits, parallel git during file loop, mixed-scope commits spanning multiple primary files.
**Reporting:** skip per-file progress, treat `suggest-polish-files.py` score as quality gate.
