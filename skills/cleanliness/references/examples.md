# Cleanliness Examples

Use this reference for concrete structural patterns. The examples are in Rust
and TypeScript, but the rules are intentionally portable.

## Boundary Comments

Do write module comments that define ownership:

```rust
//! Order domain layer.
//!
//! `orders` owns order behavior used by the HTTP API. HTTP route
//! families belong above this module; storage adapters and transaction details
//! belong below it.
```

Why it works:

- states the boundary
- names what belongs elsewhere
- gives future agents a filing rule before they add code

Do not write comments that only decorate:

```rust
//! Utilities.
//! This file has helper functions.
```

That gives no boundary, no exclusion rule, and no architecture signal.

## Thin Entrypoints

Favor route or command handlers that parse, authorize, and delegate:

```ts
export default withAuth(async ({ db, params, query }) => {
    const filter = orderFilterFromQuery(query);
    return db.orders.stream(params.customerId, filter);
});
```

Keep the domain work elsewhere:

```ts
function orderFilterFromQuery(query: QueryParams): OrderFilter {
    return {
        ...(query.where ? { where: parseJson(query.where, 'where') } : {}),
        ...(query.order ? { order: parseJson(query.order, 'order') } : {}),
        ...(query.limit !== undefined ? { limit: parseLimit(query.limit) } : {}),
    };
}
```

Avoid handlers that also implement validation policy, SQL, response shaping,
authorization decisions, and logging in one body.

## Dispatch Shape

A large dispatch is acceptable when arms delegate immediately:

```rust
match (resource, op) {
    ("job", "create") => one(store::job::create(caller, from_data(&req.data)?).await?),
    ("job", "status") => one(job_status::status(caller, id_from(req)?).await?),
    ("invoice", "check") => one(store::invoice::check(caller, from_data(&req.data)?).await?),
    _ => Err(Error::UnknownCommand(req.command.clone())),
}
```

It becomes a cleanliness problem when each arm grows its own inline workflow:

```rust
match call.as_str() {
    "orders:create" => {
        let context = context_from_data(&req.data)?;
        let customer = required_str(&req.data, "customer")?;
        let body = required_object(&req.data, "body")?;
        validate_customer(customer)?;
        authorize(&context, customer)?;
        let tx = open_tx(&context).await?;
        // dozens more lines...
    }
    // repeated for many calls
}
```

Clean options:

- move each resource to `dispatch_orders`, `dispatch_invoices`, `dispatch_users`
- create a typed command enum and lower once
- use a static route/operation table when the language and framework make that
  clearer than a large `match`
- keep arms scan-friendly by calling named helpers instead of embedding
  multi-line closures

## Function Length

Use approximate triggers:

- under 40 lines: usually fine
- 40-80 lines: check for visible phases
- 80-150 lines: require a strong reason or helper extraction
- over 150 lines: treat as a design smell unless it is generated code, a dense
  declarative table, or a deliberately flat parser/emitter with clear sections

Do not split just to satisfy a counter. Split when the extracted piece has a
name that improves the parent:

```rust
async fn handle_checkout(...) {
    let req = parse_checkout_request(&req, sender).await?;
    let plan = plan_for(config, &req)?;
    let cart = load_cart(caller, store, req.cart_id).await;
    let charge = build_charge(&req, &cart);
    let result = payments.charge(charge).await;
    send_checkout_result(sender, req, result).await;
}
```

Avoid:

```rust
fn handle_checkout_part_1(...) { ... }
fn handle_checkout_part_2(...) { ... }
fn handle_checkout_part_3(...) { ... }
```

Those helpers hide length but do not reveal concepts.

## Early Return And Guard Clauses

Prefer guard clauses for invalid, empty, unauthorized, or already-complete
cases. The main path should stay flat and easy to scan.

Good:

```ts
function renderProject(project: Project | null, user: User): View {
    if (!project) return missingProjectView();
    if (!user.canView(project)) return unauthorizedView();
    if (project.archived) return archivedProjectView(project);

    const summary = buildProjectSummary(project);
    const actions = actionsForProject(project, user);
    return projectView(summary, actions);
}
```

Questionable:

```ts
function renderProject(project: Project | null, user: User): View {
    if (project) {
        if (user.canView(project)) {
            if (!project.archived) {
                const summary = buildProjectSummary(project);
                const actions = actionsForProject(project, user);
                return projectView(summary, actions);
            } else {
                return archivedProjectView(project);
            }
        } else {
            return unauthorizedView();
        }
    } else {
        return missingProjectView();
    }
}
```

Do not flatten every conditional mechanically. Keep structured branching when
both sides are meaningful peer workflows, when cleanup/defer semantics require
one exit shape, or when the language/framework convention favors an explicit
result expression. Treat deeply nested conditionals as a cleanliness issue when
guard clauses would make preconditions and the primary path clearer.

## Closure Weight

Keep closures light in iterator chains, framework builders, transaction
wrappers, and spawned async tasks.

Closures inside `match` arms deserve extra suspicion. A match is often a table
of cases; a long closure inside an arm makes the table stop being scannable.

Good:

```rust
match op {
    Op::Create(input) => run_create(system, caller, input).await,
    Op::Delete(input) => run_delete(system, caller, input).await,
}
```

Questionable:

```rust
match op {
    Op::Create(input) => {
        with_retry(|| async {
            let validated = validate_create(&input)?;
            let tx = system.store.begin().await?;
            let record = insert_record(&tx, validated).await?;
            publish_created(system, &record).await?;
            tx.commit().await?;
            Ok(record)
        })
        .await
    }
    Op::Delete(input) => run_delete(system, caller, input).await,
}
```

Prefer:

```rust
match op {
    Op::Create(input) => create_with_retry(system, caller, input).await,
    Op::Delete(input) => run_delete(system, caller, input).await,
}
```

Then put the retry closure inside `create_with_retry` or a smaller helper whose
name explains the operation. A closure longer than a few lines should usually
be extracted unless it is a tiny adapter around a framework API and the body
stays obvious at the callsite.

Good:

```rust
transaction::write(db, move |tx| {
    Box::pin(async move { create_orders_in_tx(tx, init, orders).await })
})
```

Bad:

```rust
transaction::write(db, move |tx| {
    Box::pin(async move {
        // validation, branching, SQL, response shaping, logging, and cleanup
        // all inline for 80 lines
    })
})
```

Extract heavy closure bodies into named helpers. The callsite should reveal the
transactional shape, not bury the operation.

## Naming

Names should spend length where it buys precision.

Good:

- `ready_to_ship`
- `refund_window_open`
- `payment_matches_invoice`
- `record_not_found_or_not_trashed`
- `load_invoice_template_context`

Questionable:

- `scan_expr_for_go_unsupported_errors`
- `scan_block_for_rust_unsupported_errors`
- `scan_if_body_for_go_unsupported_errors`

Those names may be accurate, but repeated long prefixes suggest a missing
module, trait, visitor, or target-specific policy object. Consider moving them
under `go::unsupported` or `rust::unsupported`, then naming them `scan_expr`,
`scan_block`, and `scan_if_body`.

## Identifier Strings

Strings that behave like fixed identifiers should usually be named constants.
This includes route names, command names, event names, provider keys, modes,
feature flags, telemetry labels, protocol values, field names, and dispatch
keys.

Good:

```rust
const COMMAND_ORDERS_CREATE: &str = "orders:create";
const FIELD_CUSTOMER: &str = "customer";
const FIELD_BODY: &str = "body";

match call.as_str() {
    COMMAND_ORDERS_CREATE => create_order(
        required_str(&req.data, FIELD_CUSTOMER)?,
        required_object(&req.data, FIELD_BODY)?,
    ),
    _ => Err(Error::UnknownCommand(call)),
}
```

Questionable:

```rust
match call.as_str() {
    "orders:create" => create_order(
        required_str(&req.data, "customer")?,
        required_object(&req.data, "body")?,
    ),
    _ => Err(Error::UnknownCommand(call)),
}
```

The strings are not prose; they are part of a machine contract. Constants make
renames searchable, reduce typo risk, and give the identifier a domain name.

Do not extract every string mechanically. Inline text is usually fine for
one-off human-facing copy, test scenario descriptions, short log messages, or
error text whose wording is the value. Extract when the string is used as an
identifier, compared in logic, shared across callsites, or part of an external
contract.

## Argument Consistency

Related functions should present the same conceptual inputs in the same order
unless the domain gives a clear reason not to. This matters most for route
families, storage helpers, provider adapters, compiler lowering passes,
builder-style utilities, and sibling operations such as `create`, `update`,
`delete`, `load`, and `list`.

Good:

```rust
fn create_run(caller: &Caller, store: &Store, request: CreateRun) -> Result<Run> { ... }
fn update_run(caller: &Caller, store: &Store, run_id: RunId, request: UpdateRun) -> Result<Run> { ... }
fn delete_run(caller: &Caller, store: &Store, run_id: RunId) -> Result<()> { ... }
```

The family keeps actor/context first, stable infrastructure next, resource
identity before the operation payload, and operation-specific data last.

Questionable:

```rust
fn create_run(store: &Store, request: CreateRun, caller: &Caller) -> Result<Run> { ... }
fn update_run(caller: &Caller, run_id: RunId, request: UpdateRun, store: &Store) -> Result<Run> { ... }
fn delete_run(run_id: RunId, store: &Store, caller: &Caller) -> Result<()> { ... }
```

Each function may be understandable alone, but the family forces readers to
relearn the signature every time.

When cleaning this up:

- prefer the repo's existing convention over inventing one
- keep receiver/context/auth/session arguments consistently first
- keep stable dependencies before operation data when that matches local style
- keep IDs before payload/options when the operation is resource-scoped
- use a small request/context struct when the same long argument bundle appears
  across several functions

Do not hunt the whole repo for every possible ordering mismatch. Treat it as
cleanliness work when the related family is already in scope and one signature
is clearly out of sync with its siblings.

## Comment Quality

Good comments explain the decision:

```rust
// WHY private enum over trait object: the provider set is closed and compile
// time known. Exhaustive matching makes new providers update construction and
// dispatch together.
```

Weak comments restate the code:

```rust
// Increment the counter.
counter += 1;
```

Use comments for:

- module boundaries
- lifecycle phases
- concurrency or transaction invariants
- target-specific tradeoffs
- compatibility constraints
- why a simpler-looking approach is wrong

Do not use comments as a substitute for extraction. A 700-line function with
phase banners is still a 700-line function.

## Review Output

For read-only cleanliness reviews, use concise findings:

```text
phase-blocking: `src/api/auth/routes.rs::register` mixes request parsing,
tenant creation, key provisioning, and response shaping in one 180-line handler.
The current phase adds new auth behavior here, so split provisioning into a
domain helper before the phase gate.

deferred: `src/service.rs` is a 600-line facade. The touched method stayed thin,
so this is not phase-blocking. Consider grouping methods by route family in a
future API cleanup phase.
```

Do not report vague taste:

```text
This file is ugly and should be cleaner.
```
