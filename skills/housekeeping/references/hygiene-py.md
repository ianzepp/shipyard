# Python Hygiene Ratchet

Use this when a Python repository does not already have a hygiene-budget test. Install a prebuild ratchet at `tests/test_hygiene.py` so it runs with the normal `pytest` flow.

## Requirements

- Scan production `.py` files only.
- Exclude test files such as `test_*.py` and `*_test.py`.
- Enforce test boundary hygiene (`test-boundary-hygiene.md`): no `def test_` / pytest
  blocks in production modules. Banned-pattern budgets apply to production `.py` only.
- Encode each smell as a budget constant.
- Budgets must be monotonic: initialize to current totals, then only lower them.
- Failure output must list file:line hits for exceeded categories.

## Required baseline checks

- `print(`
- `# type: ignore`
- `# noqa`
- `except Exception:`

## Optional extra budgets

Add these when they fit the repo:

- `except:`
- `typing.Any`
- `eval(` or `exec(`

## Starter template

```python
from __future__ import annotations

import re
from pathlib import Path

MAX_PRINT = 0
MAX_TYPE_IGNORE = 0
MAX_NOQA = 0
MAX_EXCEPT_EXCEPTION = 0

def _source_files() -> list[Path]:
    root = Path(__file__).parent.parent
    return [
        p
        for p in root.rglob("*.py")
        if not p.name.startswith("test_") and not p.name.endswith("_test.py")
    ]

def _lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()

def _count(files: list[Path], pattern: str) -> int:
    return sum(1 for p in files for line in _lines(p) if pattern in line)

def _count_regex(files: list[Path], rx: re.Pattern[str]) -> int:
    return sum(1 for p in files for line in _lines(p) if rx.search(line))

SOURCE_FILES = _source_files()

def test_print_budget() -> None:
    count = _count_regex(SOURCE_FILES, re.compile(r"\bprint\("))
    assert count <= MAX_PRINT, f"print() budget exceeded ({count}/{MAX_PRINT})"
```

Mirror that test shape for the other required categories and include file:line hit lists in the assertion message.

## Installation notes

- Narrow the root directory if the repo contains tooling scripts or vendored code that should not count toward budgets.
- Keep `# noqa` handling pragmatic. If the repo has intentional framework-specific suppressions, set the initial budget to the current count and document the allowed cases inline.
- Run `pytest tests/test_hygiene.py` first, then the full test suite.
