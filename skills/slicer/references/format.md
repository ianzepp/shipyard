# Slice List Format

One Markdown file per plan, saved next to it as `<plan-stem>.slices.md`.
The first section is the original cut. Each rework or split appends a new
section; landed slices are never rewritten.

## Layout

```markdown
# Slices: <plan subject>

- plan: <path to the plan>
- size target: 5–10 minutes

## Cut 1: slice

- answer: sliced
- longest chain: <ids, in order>

### <id>: <title>

- repo: <name>            (only when the plan spans repositories)
- write_scope: `<path>`, `<path>`
- deps: <ids> | none

<brief, as plain paragraphs>

### <id>: <title>

...

### Notes

<already delivered parts that were left out; assumptions. Omit when empty.>
```

Later sections are headed `## Cut <n>: rework` or `## Cut <n>: split`, with
the same fields. An escalation section carries `answer: escalate` and a
`reason:` line, and no slices.

Do not repeat the slice list in the notes.

## Example: slice

```markdown
## Cut 1: slice

- answer: sliced
- longest chain: retry-1, retry-2

### retry-1: Add the retry counter column

- write_scope: `src/store.rs`, `src/store_test.rs`
- deps: none

In src/store.rs, add the retry column to the steps table and its migration
(around line 120). Add a test in src/store_test.rs that asserts a new row
starts at zero.

Change only the files in write_scope. If the work needs any other path,
change nothing and report blocked-scope with the paths and the reason.

### retry-2: Stop a step after two attempts

- write_scope: `src/tick.rs`, `src/tick_test.rs`
- deps: retry-1

In src/tick.rs, read the counter and stop a step after two attempts. Test it
in src/tick_test.rs.

Change only the files in write_scope. ...

### Notes

Left out as already delivered: the CLI flag. Assumed: one attempt means one
job.
```

## Example: rework

A blocked-scope report: slice `flow-3` asked for `src/lib.rs` to add one
re-export. The rework gives that edit its own early slice and orders the
original work after it.

```markdown
## Cut 2: rework

- answer: sliced
- longest chain: flow-3.1, flow-3.2

### flow-3.1: Re-export the parser from the crate root

- write_scope: `src/lib.rs`, `src/lib_test.rs`
- deps: none

In src/lib.rs, add one pub use line that exports parse_flowchart from the
mermaid module. Add a test in src/lib_test.rs that calls it through the crate
root.

### flow-3.2: Load the flow definition

- write_scope: `src/flow/load.rs`, `src/flow/load_test.rs`
- deps: flow-3.1

The original brief of flow-3, unchanged: in src/flow/load.rs, parse the
shipped flow with the re-exported parser. Test it in src/flow/load_test.rs.

### Notes

flow-3 asked for src/lib.rs. No other slice owns that file, so the visibility
edit is its own slice and the original work follows it.
```

## Example: split

Slice `close-5` ran far past its size target. Its replacements take over its
deps.

```markdown
## Cut 3: split

- answer: sliced
- longest chain: retry-2, close-5.1, close-5.2

### close-5.1: Add the guard to the close path

- write_scope: `src/close.rs`, `src/close_test.rs`
- deps: retry-2

In src/close.rs, refuse a step on a closed run. Test it in
src/close_test.rs.

### close-5.2: Show the closed state on the board

- write_scope: `src/board.rs`, `src/board_test.rs`
- deps: retry-2, close-5.1

In src/board.rs, print closed for a closed run. Test it in
src/board_test.rs.

### Notes

Split along the two files; the board edit reads the guard, so it follows.
```

## Example: escalate

```markdown
## Cut 4: rework

- answer: escalate
- reason: The implementer asks for a new public interface on the store,
  which is a design change the plan did not settle.

The request, the plan section it conflicts with, and the choice a person must
make.
```
