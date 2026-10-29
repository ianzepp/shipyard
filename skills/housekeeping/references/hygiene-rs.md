# Rust Hygiene Ratchet

Use this when a Rust repository does not already have a hygiene-budget test. Install a prebuild ratchet at `tests/hygiene.rs` and wire it into the normal `cargo test` flow.

## Requirements

- Scan production Rust source under `src/`.
- Exclude test companion files such as `*_test.rs` and `.test.rs`.
- Encode each smell as a budget constant.
- Budgets must be monotonic: initialize them to the current production-code count, then only lower them.
- The failure message must name the exceeded category and the observed count.

## Required baseline checks

- `.unwrap()`
- `.expect(`
- `panic!(`
- `unreachable!(`
- `todo!(`
- `unimplemented!(`

## Structural checks (test boundary)

See `test-boundary-hygiene.md`. These are required when the repo's convention is separate test files (or the user asks for it). In a repo that keeps idiomatic inline `#[cfg(test)] mod tests { ... }` modules, skip the structural checks below and instead scope the banned-pattern scan to non-test code (strip `#[cfg(test)]` blocks), recording that choice.

- `MAX_INLINE_TEST_MODULES = 0` — no `#[cfg(test)] mod tests { ... }` with inline bodies in `src/**/*.rs` (excluding `*_test.rs` / `*.test.rs`).
- `MAX_TEST_ATTR_IN_PRODUCTION = 0` — no `#[test]` or `#[tokio::test]` in production files.
- Allowed production wiring only:

```rust
#[cfg(test)]
#[path = "module_test.rs"]
mod tests;
```

When scanning banned-pattern budgets (`.unwrap()`, `panic!(`, etc.), count **production
code only**. Dedicated companion test files are excluded. Where the separate-files
convention applies, inline test blocks in production files are boundary violations
— move them out; do not exclude them from the structural ratchet or treat them as
acceptable production debt.

**Detection helper:**

```rust
fn production_violations(files: &[SourceFile]) -> Vec<String> {
    let mut hits = Vec::new();
    for file in files {
        if file.content.contains("#[test]") || file.content.contains("#[tokio::test]") {
            hits.push(format!("{}: contains #[test] in production file", file.path));
        }
        if file.content.contains("#[cfg(test)]") && file.content.contains("mod tests {") {
            hits.push(format!("{}: inline #[cfg(test)] mod tests {{", file.path));
        }
    }
    hits
}
```

**Remediation during housekeeping:** extract to `src/<module>_test.rs`, leave path-only
`mod tests;` in the production file, run `cargo test`, then lower unwrap/panic budgets.

## Optional extra budgets

Add these when the repo already treats them as debt:

- `let _ =` for silent discard
- `.ok()` for silent error dropping
- `#[allow(dead_code)]`

## Starter template

```rust
#![allow(clippy::absurd_extreme_comparisons)]

use std::fs;
use std::path::Path;

const MAX_UNWRAP: usize = 0;
const MAX_EXPECT: usize = 0;
const MAX_PANIC: usize = 0;
const MAX_UNREACHABLE: usize = 0;
const MAX_TODO: usize = 0;
const MAX_UNIMPLEMENTED: usize = 0;

struct SourceFile {
    path: String,
    content: String,
}

const MAX_INLINE_TEST_MODULES: usize = 0;
const MAX_TEST_ATTR_IN_PRODUCTION: usize = 0;

fn source_files() -> Vec<SourceFile> {
    let mut files = Vec::new();
    collect_rs_files(Path::new("src"), &mut files);
    files
}

fn collect_rs_files(dir: &Path, out: &mut Vec<SourceFile>) {
    let Ok(entries) = fs::read_dir(dir) else {
        return;
    };

    for entry in entries.flatten() {
        let path = entry.path();
        if path.is_dir() {
            collect_rs_files(&path, out);
        } else if path.extension().is_some_and(|ext| ext == "rs") {
            let name = path.file_name().unwrap_or_default().to_string_lossy();
            if name.ends_with("_test.rs") || name.ends_with(".test.rs") {
                continue;
            }
            if let Ok(content) = fs::read_to_string(&path) {
                out.push(SourceFile {
                    path: path.to_string_lossy().into_owned(),
                    content,
                });
            }
        }
    }
}

fn count_in_source(files: &[SourceFile], pattern: &str) -> usize {
    files.iter()
        .map(|file| file.content.lines().filter(|line| line.contains(pattern)).count())
        .sum()
}

#[test]
fn unwrap_budget() {
    let files = source_files();
    let count = count_in_source(&files, ".unwrap()");
    assert!(count <= MAX_UNWRAP, ".unwrap() budget exceeded: found {count}, max {MAX_UNWRAP}.");
}
```

Mirror that test shape for the other required categories.

## Installation notes

- If the repo already has debt, set each `MAX_*` to the current count rather than forcing zero on day one.
- Prefer exact substring counts over regex unless the repo needs more precision.
- Run `cargo test --test hygiene` immediately after adding the file.
