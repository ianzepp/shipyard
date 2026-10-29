# TypeScript Hygiene Ratchet

Use this when a TypeScript or JavaScript repository does not already have a hygiene-budget test. Install a prebuild ratchet under the production source tree, usually `src/hygiene_test.ts` or `src/hygiene.spec.ts`, and use the repo's existing test runner.

## Requirements

- Scan production `.ts` or `.tsx` files under `src/`.
- Exclude test files such as `*_test.ts`, `*.test.ts`, `*.spec.ts`.
- Enforce test boundary hygiene (`test-boundary-hygiene.md`): no `describe(`, `it(`,
  or `test(` blocks in production `.ts`/`.tsx` files. Banned-pattern budgets apply
  to production files only; tests belong in dedicated test filenames.
- Encode each smell as a budget constant.
- Budgets must be monotonic: initialize to current totals, then only lower them.
- Failure output must list file:line hits for exceeded categories.
- Keep the implementation compatible with the repo's runner. Adapt imports for `node:test`, Bun, Vitest, or Jest as needed.

## Required baseline checks

- `: any`
- `as unknown as`
- `@ts-`
- `void ` statement fire-and-forget dispatches
- `JSON.parse`
- `console.`

## Optional extra budgets

Add these when they fit the codebase:

- Non-null assertions `!`
- `as any`
- `setTimeout(` without cleanup in frontend code

## Starter template

```ts
import * as fs from "node:fs";
import * as path from "node:path";
import assert from "node:assert/strict";
import test from "node:test";

const MAX_ANY_TYPE = 0;
const MAX_AS_UNKNOWN_AS = 0;
const MAX_TS_SUPPRESS = 0;
const MAX_VOID_DISPATCH = 0;
const MAX_JSON_PARSE = 0;
const MAX_CONSOLE = 0;

interface SourceFile {
  filePath: string;
  lines: string[];
}

function collectSourceFiles(dir: string): SourceFile[] {
  const results: SourceFile[] = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...collectSourceFiles(fullPath));
      continue;
    }
    if (!entry.name.endsWith(".ts") && !entry.name.endsWith(".tsx")) continue;
    if (entry.name.endsWith("_test.ts") || entry.name.endsWith(".test.ts") || entry.name.endsWith(".spec.ts")) continue;
    results.push({ filePath: fullPath, lines: fs.readFileSync(fullPath, "utf8").split("\n") });
  }
  return results;
}

function countMatches(files: SourceFile[], pattern: string): number {
  return files.reduce((total, file) => total + file.lines.filter((line) => line.includes(pattern)).length, 0);
}

const files = collectSourceFiles(path.resolve("src"));

test("any type budget", () => {
  const count = countMatches(files, ": any");
  assert.ok(count <= MAX_ANY_TYPE, `": any" budget exceeded (${count}/${MAX_ANY_TYPE})`);
});
```

Mirror that test shape for the other required categories, and for `void ` count only statement-form fire-and-forget calls, not return type annotations.

## Installation notes

- Put the ratchet where the repo's normal test command will discover it.
- If the codebase is JS-first, the same structure works in `.js`; keep the budgets and scan rules.
- Run the repo's standard test command immediately after adding the ratchet.
