# Rust And Generated-Code Cleanliness

Use this reference for Rust repositories, especially LLM-generated compiler,
backend, API, service, and orchestration code.

## Calibration

Useful guideposts for a well-structured Rust codebase: many small files (a
median around 70 lines), no function over roughly 150 lines, module comments
that state ownership, and clear domain layering with route/domain separation.
Comments and phase labels do not erase oversized-function risk.

Do not blindly impose these numbers. Use them to calibrate suspicion, then
respect the target repo's own conventions.

## Rust Module Shape

Prefer:

```text
src/billing/
  mod.rs              public actor/dispatch boundary
  types/              shared request/record/error types
  store/              thin persistence adapters
  ops/                compound operations
  orchestrate.rs      lifecycle state machine
  invoice_status.rs   read-side aggregate view
```

This shape helps future work find the right file. It also keeps generated code
from appending every new operation to `mod.rs`.

Avoid:

```text
src/billing/mod.rs    actor, all types, persistence, orchestration, validation,
                      tests, event fanout, and response shaping
```

If a module root grows beyond wiring and public shape, move behavior down.

## Visitor, Parser, And Emitter Functions

Compiler-like code often has large `match` statements. Cleanliness does not
forbid that. It asks whether the function still has one responsibility.

Acceptable:

```rust
fn emit_expr(ctx: &Ctx, expr: &Expr, out: &mut Writer) -> Result<()> {
    match &expr.kind {
        ExprKind::Literal(lit) => emit_literal(lit, out),
        ExprKind::Call(call) => emit_call(ctx, call, out),
        ExprKind::Block(block) => emit_block_expr(ctx, block, out),
    }
}
```

Problematic:

```rust
fn emit_expr(...) -> Result<()> {
    match &expr.kind {
        ExprKind::Call(call) => {
            // resolve intrinsic
            // infer receiver collection type
            // translate standard library method
            // emit fallback call
            // special-case text indexing
            // all inline
        }
        // many branches with similar inline sub-work
    }
}
```

Also problematic:

```rust
fn emit_expr(...) -> Result<()> {
    match &expr.kind {
        ExprKind::Call(call) => with_emit_context(|ctx| {
            // resolve intrinsic
            // infer receiver collection type
            // translate standard library method
            // emit fallback call
            // special-case text indexing
            // all inline
        }),
        _ => emit_simple_expr(expr),
    }
}
```

The closure hides the same complexity as a long arm body and makes the match
harder to scan. Extract the operation behind a named helper:

```rust
fn emit_expr(...) -> Result<()> {
    match &expr.kind {
        ExprKind::Call(call) => emit_call_expr(ctx, call, out),
        _ => emit_simple_expr(expr),
    }
}
```

Clean extraction targets:

- `emit_call`
- `emit_method_call`
- `emit_optional_chain`
- `emit_target_intrinsic`
- `emit_collection_method`
- `emit_statement_like_expr`

Use submodules when the helper names all share a prefix:

```text
codegen/ts/
  expr.rs
  expr/call.rs
  expr/chain.rs
  expr/intrinsic.rs
```

## Target-Specific Duplication

When code repeats the same scanner for Go, Rust, TypeScript, or another target,
look for a target policy object or module split.

Before:

```rust
fn scan_expr_for_go_unsupported_errors(...)
fn scan_block_for_go_unsupported_errors(...)
fn scan_if_body_for_go_unsupported_errors(...)
fn scan_expr_for_rust_unsupported_errors(...)
fn scan_block_for_rust_unsupported_errors(...)
fn scan_if_body_for_rust_unsupported_errors(...)
```

Better options:

```rust
mod unsupported {
    pub mod go {
        pub fn scan_expr(...) { ... }
        pub fn scan_block(...) { ... }
    }

    pub mod rust {
        pub fn scan_expr(...) { ... }
        pub fn scan_block(...) { ... }
    }
}
```

Or:

```rust
trait TargetPolicy {
    fn target_name(&self) -> &'static str;
    fn diagnose_expr(&self, expr: &Expr, diagnostics: &mut Vec<Diagnostic>);
}
```

Do not introduce a trait just for fashion. Use it only when multiple targets
share traversal and differ in policy.

## Async And Transaction Closures

Rust LLM output often hides large workflows inside async closures:

```rust
tokio::spawn(async move {
    match handle(&caller, &req).await {
        Ok(items) => { /* send every item inline */ }
        Err(err) => { /* send error inline */ }
    }
});
```

This can be fine when the body is short. If it grows, extract:

```rust
tokio::spawn(async move {
    respond_to_order_request(caller, req, sender).await;
});
```

Then make the helper own the full response lifecycle.

Apply the same rule inside `match` arms. If an arm needs a closure longer than a
few lines, keep the arm as a call to a domain-named helper and move the closure
behind that helper. The match should show which case maps to which operation,
not contain the operation itself.

For transactions, prefer helper boundaries that name the operation:

```rust
transaction::write_sqlite(db, move |tx| {
    sqlite_create_orders_tx(&mut tx.connection, &init, orders)
})
```

If the closure contains validation, branching, SQL construction, and response
shaping, it is hiding a module.

## Test Cleanliness

Long integration tests are sometimes justified, but they should have readable
scenario phases and reusable setup helpers.

Favor:

```rust
#[test]
fn shipping_both_items_marks_order_shipped() {
    let harness = OrderHarness::new();
    let order = harness.create_order_with_two_items();

    harness.ship_item(order.item_a);
    harness.ship_item(order.item_b);

    harness.assert_order_shipped(order.id);
}
```

Avoid one test that creates config, writes fixtures, starts services, advances
state, asserts every intermediate row, and checks logs all inline.

If a test name exceeds normal length because it encodes the full scenario,
consider whether the module path and helper names can carry some context.

## Reporting Rust Cleanliness Findings

Use structural evidence:

```text
phase-blocking: `src/codegen/ts/expr.rs::generate_expr`
handles target intrinsics, method translation, optional chains, statement-like
IIFEs, literal emission, and collection semantics in one long match. The current
phase modifies method translation, so extract `generate_method_call` and
`try_generate_collection_method` before adding more branches.
```

Distinguish deferred debt:

```text
deferred: `src/command_handler.rs::dispatch_command` is a large string dispatch,
but this phase only touched one thin service method. Record a future split into
resource-specific dispatch helpers; do not broaden the current diff.
```

Escalate to correctness only when shape hides a concrete failure mode:

```text
correctness handoff: the mixed transaction and cleanup logic in
`provision_account` can leak external resources on malformed payment-provider responses.
This is not merely cleanliness; inspect failure paths and compensation behavior.
```
