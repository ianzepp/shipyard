# Test Boundary Hygiene

**Applies when the repo adopts this convention** (separate test files, stated in its instructions or evident from its existing layout) or the user asks for it. Idiomatic inline tests, such as Rust `#[cfg(test)] mod tests { ... }`, are not a violation in a repo that uses them; skip this reference there, record the reason, and scope banned-pattern scans to non-test code by other means. Go and Python test-file naming is already the language convention.

Production source files and test source files serve different quality bars. Hygiene
ratchets ban patterns such as `.unwrap()`, `panic!(`, `.ok()`, and `let _ =` in
**production** code. Those same patterns are normal and acceptable in **dedicated
test files**.

When tests live inside production files — inline `#[cfg(test)] mod tests { ... }`,
`#[test]` functions at the bottom of a module, or test helpers mixed into prod
modules — housekeeping and hygiene passes miss the boundary:

- Agents run hygiene on `src/` and count banned patterns that actually belong to
  tests, forcing bogus production "fixes" or inflated budgets.
- Other sessions discover tests embedded in production files and must manually
  extract them even after a recent housekeeping pass.

**Where the convention applies, housekeeping enforces test boundaries in Step 2
(Test Boundary Hygiene), before Step 3 (Banned-Pattern Ratchet) ever counts budgets.**

## Rules by language

### Rust

**Production file** — any `src/**/*.rs` except companion test files
(`*_test.rs`, `*.test.rs`).

**Allowed wiring in a production file (declaration only):**

```rust
#[cfg(test)]
#[path = "module_test.rs"]
mod tests;
```

**Forbidden in production files (when this convention applies):**

- `#[cfg(test)] mod tests { ... }` with inline test bodies
- `#[test]`, `#[tokio::test]`, or `#[rstest]` functions defined in the production file
- Test-only helpers, fixtures, or mock types that are only used from tests

**Dedicated test file locations:**

- Colocated companion: `src/module_test.rs` or `src/module.test.rs`
- Crate integration: `tests/*.rs`

**Detection:**

```sh
rg -n '#\[cfg\(test\)\]' src --glob '*.rs' --glob '!*_test.rs' --glob '!*.test.rs'
rg -n '#\[test\]' src --glob '*.rs' --glob '!*_test.rs' --glob '!*.test.rs'
rg -n 'mod tests\s*\{' src --glob '*.rs' --glob '!*_test.rs'
```

**Remediation:**

1. Move test bodies into `*_test.rs` / `*.test.rs` beside the module (or `tests/`).
2. Replace inline modules with `#[cfg(test)] #[path = "..."] mod tests;` only.
3. Re-run `cargo test` and `cargo test --test hygiene`.
4. Lower hygiene budgets if production-only counts dropped.

### TypeScript / JavaScript

**Production:** `src/**/*.ts(x)` excluding `*_test.ts`, `*.test.ts`, `*.spec.ts`.

**Forbidden:** `describe(`, `it(`, `test(`, `expect(` blocks in non-test files.

**Dedicated test files:** colocated `*_test.ts` / `*.test.ts` / `*.spec.ts`, or
`tests/` / `__tests__/`.

**Detection:**

```sh
rg -n '\b(describe|it|test)\s*\(' src --glob '*.ts' --glob '!*test*' --glob '!*spec*'
```

### Go

**Production:** `*.go` excluding `*_test.go`.

**Forbidden:** `func Test` and `testing.T` usage outside `*_test.go`.

**Detection:**

```sh
rg -n 'func Test' --glob '*.go' --glob '!*_test.go'
```

### Python

**Production:** `*.py` excluding `test_*.py` and `*_test.py`.

**Forbidden:** test functions/classes in production modules (`def test_`,
`pytest`, heavy `assert` blocks in non-test modules).

**Detection:**

```sh
rg -n '^def test_|^async def test_' --glob '*.py' --glob '!test_*.py' --glob '!*_test.py'
```

## Hygiene ratchet integration

When scanning production code for banned-pattern budgets:

1. **Exclude** dedicated test filenames (`*_test.rs`, `*.test.ts`, `*_test.go`, etc.).
2. **Do not** treat inline `#[cfg(test)] { ... }` blocks as exempt — they are a
   boundary violation; move them out, then count.
3. Add a **structural** ratchet test (see language hygiene references) with budget
   `MAX_INLINE_TEST_MODULES = 0` or equivalent.

## Housekeeping completion gate

Before finishing Step 3, in a repo where this convention applies, confirm:

- [ ] No `#[test]` / `describe` / `func Test` / `def test_` in production files
- [ ] Rust `#[cfg(test)]` in production files is path-only (`#[path = "..."] mod tests;`)
- [ ] Hygiene budgets reflect production code only
- [ ] Full test suite still passes after extractions

Report moved modules in the final housekeeping summary.