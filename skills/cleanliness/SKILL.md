---
name: cleanliness
description: "Shape implementation code for managed complexity and run read-only cleanliness scans: module boundaries, function and file size, dispatch structure, helper extraction, guard clauses, naming consistency, and control-flow complexity. Use when refactoring code structure for maintainability without changing behavior, especially after LLM-generated work, before the work is accepted, or as a factory tidy slice."
---

# Cleanliness

Shape code for structural maintainability without changing behavior.

## Role In The Stack

| Skill | Question |
| --- | --- |
| `correctness` | Does behavior fail? |
| `cleanliness` | Is complexity shaped into clear modules, functions, boundaries, control flow, names, and comments? |
| `housekeeping` | Is the repo hygienic and validated? |

Local readability and aesthetic polish belong to `polish`. `cleanliness` is architectural and structural. In factory, cleanliness edits behavior-preserving structure in the phase's tidy slice (see factory's [order](../factory/SKILL.md#order)).

## Scanner Mode

Use scanner mode for a read-only pass over existing code when no implementation
diff is authorized. The scanner discovers structural opportunities, classifies
their architectural owner, and files durable findings for later work. It does
not refactor code, create a new campaign, or treat every large file as debt.

Classify each finding by the area that owns it (for example a layer, module
family, or subsystem of the repo), plus `CROSS` for a finding that genuinely
spans two areas and cannot be assigned to one owner.

Classify by the invariant or responsibility at risk, not only by the file path.
If an existing campaign already owns the surface, route the finding there rather
than creating competing work.

### Scanner workflow

1. Read the active campaign or planning documents and identify current work,
   ownership, and protected or dirty surfaces.
2. Scan a bounded module or responsibility family. Prefer concrete structural
   evidence over size-only suspicion: mixed responsibilities, opaque dispatch,
   repeated policy, oversized orchestration, boundary leakage, or control flow
   that actively impedes change.
3. Classify each finding by owning area (or `CROSS`), and identify the owning
   campaign or mark the routing decision unresolved.
4. Deduplicate against existing deferred records and tracker issues using a stable
   fingerprint such as area + repository + path + symbol + finding type.
5. File only bounded, evidence-backed findings. Keep implementation proposals
   optional and preserve uncertainty when the correct boundary is not known.
6. Stop after the scan budget, on ownership ambiguity, or when the path is under
   active conflicting work. Record the observation for later rather than
   competing with the active implementation.

### Rust structural census

Use `scripts/rust-structure-census.py` to rank tracked Rust source before a
bounded scanner pass. `<skill-dir>` is where this skill is installed (for the Claude Code plugin, `${CLAUDE_PLUGIN_ROOT}/skills/cleanliness`); `<repo-root>` is the repository; point `--path` at the source root, e.g. `src` or `crates`:

```bash
python3 <skill-dir>/scripts/rust-structure-census.py \
  --repo <repo-root> --path <source-root> --limit 30
python3 <skill-dir>/scripts/rust-structure-census.py \
  --repo <repo-root> --path <source-root> --json --limit 100
```

The dependency-free scanner reports file and function size, nested-brace depth,
large block closures, large braced match arms, and initial module-charter
coverage. Recognized test-file paths, fixtures, benches, and examples are
excluded unless `--include-tests` is passed; inline `#[cfg(test)]` modules remain
part of their owning source file. Thresholds select review candidates; they are
not quality budgets, findings, or permission to refactor. Its Rust parsing is
lexical and approximate, especially around macros and unusual syntax, so inspect
each ranked symbol before filing work. Keep its current-shape signals separate
from churn or polish-history scores.

### Finding record

Every filed finding should include:

```text
Area: <owning area> | CROSS
Owner campaign: <campaign or unresolved>
Repository: <repo>
Path / symbols: <exact locations>
Finding type: <structural category>
Evidence: <specific observations>
Why it matters: <maintainability or boundary risk>
Suggested boundary: <optional>
Done when: <observable closure condition>
Validation: <focused checks expected later>
Fingerprint: <stable deduplication key>
```

Use subjects that expose routing immediately, for example:

```text
[CLEAN][parser] Mixed expression grammar responsibilities
[CLEAN][validate] Separate layout validation from program traversal
```

### Filing and lifecycle

Route findings by output kind:

| Output | Use for |
|---|---|
| Campaign deferred register | valid findings not ready for execution |
| Task / issue | concrete bounded cleanup package |
| Question for the owner | ownership or scope decision required |
| Note / summary | advisory context, scan summaries, notifications |

Use whatever tracker the repo already has; this skill only defines the cleanliness finding content and routing vocabulary.

Track findings as:

```text
discovered → deferred → queued → in progress → resolved
                         ↘ invalidated / superseded
```

The scanner is read-only with respect to source code. Filing must remain
idempotent, must not weaken campaign gates, and must not silently accept or
implement its own findings.

## Factory Phase Use

Inside [factory](../factory/SKILL.md), cleanliness runs as the phase's final tidy slice, cut by [slicer](../slicer/SKILL.md) as `<prefix>-tidy` (depends on every other slice, `red_first: no`); factory's [order](../factory/SKILL.md#order) is the canonical sequence. In a tidy slice cleanliness never changes behavior.

Default scope: the **factory phase's change set** (everything changed since the phase base, per the [workflow](../factory/SKILL.md#workflow)); immediate local modules needed for coherent boundaries; tests only when test shape is a maintainability risk.

Cleanliness may reshape (behavior-preserving): split along repo boundaries; extract domain-named helpers; move logic out of routes, facades, closures, or dispatch arms; add boundary and `WHY` comments; rename phase-introduced symbols.

Cleanliness must not:

- change public behavior (standalone use may do so only after rerunning correctness and verification; in a tidy slice never: a behavior change found is a finding for slicer rework, not an edit)
- broaden into unrelated pre-existing architecture debt
- perform aesthetic-only churn (aesthetics belong to `polish`, which applies this lens to one file at a time)
- remove compatibility paths or deprecated aliases (record each as a deferred finding, or propose a separate slice, to remove the compatibility path)
- treat every long untouched function as phase-blocking

Structural debt outside the active phase → record under `Deferred Findings / Future Work` with `Type: cleanliness` unless it blocks the checkpoint.

## Default Workflow

1. **Inspect conventions** — nearby files, module roots, route/service layers, related function families, tests, repo docs; prefer repo decomposition style.
2. **Map responsibilities** — boundary each touched file owns; flag mixed routing, orchestration, validation, storage, transformation, rendering, provider calls, persistence.
3. **Check complexity pressure** — oversized files; functions over ~80 lines (review trigger); over ~150 lines (strong trigger); deep nesting; avoidable `if`/`else` chains; repetitive dispatch; match arms with heavy inline closures; long inconsistent names; helpers with no domain identity. Repo-defined metrics win over these defaults.
4. **Check identifier literals** — hard-coded strings that represent stable identifiers, routes, event names, modes, provider keys, field names, labels, or protocol values should usually be named constants. Do not extract ordinary user-facing prose just because it is a string.
5. **Check signature consistency** — in clearly related function groups, notice arguments that are named, grouped, or ordered differently without a domain reason. Standardize obvious local drift, especially receiver/context/auth/id/options/data ordering, but do not launch a broad API migration just to make every callsite aesthetically uniform.
6. **Reshape when it helps** — extract around domain concepts; split modules on real ownership boundaries; keep thin facades thin; preserve useful visual repetition when abstraction would hide the pattern.
7. **Add boundary comments** — module comments stating what belongs here and elsewhere; short `WHY` for non-obvious tradeoffs; no line-by-line narration.
8. **Verify unchanged behavior** — format and run relevant tests. A behavior change found: in a tidy slice, record it as a finding for slicer rework; standalone, hand it to `correctness` and rerun checks after.

## Use Modes

| Mode | Use when |
| --- | --- |
| **Read-only** | Review, audit, assessment — report `phase-blocking` or `deferred` with paths, symbols, structural reason |
| **Scanner** | Bounded repository scan — classify findings by owning area and route deferred/task/question/note outputs without editing code |
| **Update** | Clean, reshape, refactor, split — behavior-preserving unless user authorizes semantic changes |

## What To Favor

- Module roots stating ownership boundaries
- Route/handler/facade code that delegates quickly
- Domain helpers named after the concept they own
- Small functions with visible phases: validate, prepare, execute, report
- Guard clauses and early returns for invalid, empty, unauthorized, or already-complete cases
- Related function families with stable argument order, names, and grouping
- Match arms that delegate to named helpers instead of hiding workflows in closures
- Named constants for stable strings used as identifiers, protocol values, or dispatch keys
- Private context objects shortening noisy signatures
- Dispatch tables or resource-specific modules when `match` grows repetitive
- Comments explaining architecture, invariants, phase ordering, tradeoffs
- Tests near protected behavior; large fixtures in helpers when readable

## What To Avoid

- Giant orchestration functions justified only by phase comments
- Long `match` bodies with inline business logic in every branch
- Nested `if`/`else` pyramids where guard clauses would make the main path obvious
- Heavy closures in match arms, builder chains, async spawns, iterators, or transaction wrappers
- Files mixing routing, domain decisions, storage, response formatting
- Helper soup with names that do not clarify the parent
- Names repeating a whole story because code has no enclosing module
- Repeated or semantically important identifier strings embedded directly in logic
- Related methods that shuffle the same arguments without a clear semantic reason
- Comments paraphrasing the next line
- Broad refactors outside touched scope unless cleanliness is the primary objective

## References

- [examples](references/examples.md) — do/don't patterns, review language, before/after shapes
- [rust-generated-code](references/rust-generated-code.md) — Rust and LLM-generated compiler, backend, service, route, or orchestration code
- [`rust-structure-census.py`](scripts/rust-structure-census.py) — dependency-free Rust structural review-trigger census with table and JSON output
