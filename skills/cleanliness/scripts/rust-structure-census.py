#!/usr/bin/env python3
"""Report structural review triggers in tracked Rust source.

This scanner is a routing aid, not a quality gate. It uses dependency-free
lexical analysis to rank files and symbols that deserve judgment: large files,
functions, closures, match arms, and deeply braced function bodies. Rust macros
and unusual syntax can produce approximate locations, so inspect source before
filing a cleanliness finding or changing code.
"""

from __future__ import annotations

import argparse
import bisect
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import median

SCHEMA_VERSION = 1
SKIP_PARTS = {
    ".git",
    "build",
    "cache",
    "dist",
    "generated",
    "node_modules",
    "target",
    "tmp",
    "vendor",
}
TEST_PARTS = {"benches", "examples", "fixture", "fixtures", "testdata", "tests"}
TEST_NAMES = {"test.rs", "tests.rs"}
TEST_SUFFIXES = ("_test.rs", "_tests.rs")
FUNCTION_RE = re.compile(r"\bfn\s+((?:r#)?[^\s(<{;]+)")
MATCH_ARM_RE = re.compile(r"=>\s*\{")


@dataclass(frozen=True)
class FileMetric:
    path: str
    lines: int
    starts_with_charter: bool
    functions: int
    closures: int
    match_arms: int
    max_function_nesting: int


@dataclass(frozen=True)
class FunctionMetric:
    path: str
    name: str
    start_line: int
    end_line: int
    lines: int
    nesting: int


@dataclass(frozen=True)
class BlockMetric:
    path: str
    start_line: int
    end_line: int
    lines: int


@dataclass(frozen=True)
class Analysis:
    file: FileMetric
    functions: tuple[FunctionMetric, ...]
    closures: tuple[BlockMetric, ...]
    match_arms: tuple[BlockMetric, ...]


def run_git(repo: Path, args: list[str]) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        message = result.stderr.decode(errors="replace").strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return result.stdout


def repo_root(path: Path) -> Path:
    return Path(run_git(path, ["rev-parse", "--show-toplevel"]).decode().strip())


def tracked_rust_files(repo: Path, pathspecs: list[str], include_tests: bool) -> list[str]:
    args = ["ls-files", "-z"]
    if pathspecs:
        args.extend(["--", *pathspecs])
    paths = run_git(repo, args).decode(errors="surrogateescape").split("\0")
    return [
        path
        for path in paths
        if path
        and path.endswith(".rs")
        and not should_skip(path)
        and (include_tests or not is_test_path(path))
    ]


def should_skip(path: str) -> bool:
    return bool(set(Path(path).parts) & SKIP_PARTS)


def is_test_path(path: str) -> bool:
    file_path = Path(path)
    return (
        bool(set(file_path.parts) & TEST_PARTS)
        or file_path.name in TEST_NAMES
        or file_path.name.endswith(TEST_SUFFIXES)
    )


def line_starts(text: str) -> list[int]:
    starts = [0]
    starts.extend(index + 1 for index, char in enumerate(text) if char == "\n")
    return starts


def line_number(starts: list[int], position: int) -> int:
    return bisect.bisect_right(starts, position)


def mask_non_code(source: str) -> str:
    """Replace comments and literals with spaces while preserving newlines."""
    chars = list(source)
    length = len(source)
    index = 0

    def mask(start: int, end: int) -> None:
        for offset in range(start, min(end, length)):
            if chars[offset] != "\n":
                chars[offset] = " "

    while index < length:
        if source.startswith("//", index):
            end = source.find("\n", index + 2)
            end = length if end == -1 else end
            mask(index, end)
            index = end
            continue

        if source.startswith("/*", index):
            depth = 1
            cursor = index + 2
            while cursor < length and depth:
                if source.startswith("/*", cursor):
                    depth += 1
                    cursor += 2
                elif source.startswith("*/", cursor):
                    depth -= 1
                    cursor += 2
                else:
                    cursor += 1
            mask(index, cursor)
            index = cursor
            continue

        raw = raw_string_end(source, index)
        if raw is not None:
            mask(index, raw)
            index = raw
            continue

        prefix = 1 if source[index:index + 1] in {'b', 'c'} else 0
        quote_at = index + prefix
        if quote_at < length and source[quote_at] == '"':
            end = quoted_end(source, quote_at, '"')
            mask(index, end)
            index = end
            continue

        char_end = char_literal_end(source, index)
        if char_end is not None:
            mask(index, char_end)
            index = char_end
            continue

        index += 1

    return "".join(chars)


def raw_string_end(source: str, start: int) -> int | None:
    index = start
    if source.startswith("br", index):
        index += 2
    elif source.startswith("r", index):
        index += 1
    else:
        return None

    hashes = 0
    while index < len(source) and source[index] == "#":
        hashes += 1
        index += 1
    if index >= len(source) or source[index] != '"':
        return None

    terminator = '"' + "#" * hashes
    end = source.find(terminator, index + 1)
    return len(source) if end == -1 else end + len(terminator)


def quoted_end(source: str, quote_at: int, quote: str) -> int:
    index = quote_at + 1
    while index < len(source):
        if source[index] == "\\":
            index += 2
            continue
        if source[index] == quote:
            return index + 1
        index += 1
    return len(source)


def char_literal_end(source: str, start: int) -> int | None:
    quote_at = start + 1 if source.startswith("b'", start) else start
    if quote_at >= len(source) or source[quote_at] != "'":
        return None

    index = quote_at + 1
    if index >= len(source) or source[index] in "\r\n'":
        return None
    if source[index] == "\\":
        index += 2
        if index < len(source) and source[index - 1] in {"u", "x"}:
            closing = source.find("'", index)
            if closing != -1 and "\n" not in source[index:closing]:
                return closing + 1
    else:
        index += 1
    return index + 1 if index < len(source) and source[index] == "'" else None


def matching_braces(code: str) -> dict[int, int]:
    stack: list[int] = []
    matches: dict[int, int] = {}
    for index, char in enumerate(code):
        if char == "{":
            stack.append(index)
        elif char == "}" and stack:
            start = stack.pop()
            matches[start] = index
    return matches


def find_function_body(code: str, signature_end: int, matches: dict[int, int]) -> int | None:
    """Find a function body after its name without selecting const-generic braces."""
    parens = 0
    brackets = 0
    angles = 0
    saw_parameters = False
    index = signature_end

    while index < len(code):
        char = code[index]
        if char == "(" and not saw_parameters and parens == brackets == angles == 0:
            saw_parameters = True
            parens = 1
        elif char == "(":
            parens += 1
        elif char == ")" and parens:
            parens -= 1
        elif char == "[":
            brackets += 1
        elif char == "]" and brackets:
            brackets -= 1
        elif char == "<" and not parens:
            angles += 1
        elif char == ">" and angles and code[index - 1:index] != "-":
            angles -= 1
        elif char == "{" and index in matches:
            if not saw_parameters or parens or brackets or angles or previous_nonspace(code, index) == "!":
                index = matches[index] + 1
                continue
            return index
        elif char == ";" and saw_parameters and parens == brackets == angles == 0:
            return None
        index += 1
    return None


def previous_nonspace(code: str, position: int) -> str:
    index = position - 1
    while index >= 0 and code[index].isspace():
        index -= 1
    return code[index] if index >= 0 else ""


def nested_brace_depth(code: str, start: int, end: int) -> int:
    depth = 0
    maximum = 0
    for char in code[start + 1:end]:
        if char == "{":
            depth += 1
            maximum = max(maximum, depth)
        elif char == "}" and depth:
            depth -= 1
    return maximum


def starts_with_module_charter(source: str) -> bool:
    stripped = source.lstrip("\ufeff \t\r\n")
    if stripped.startswith("#!") and not stripped.startswith("#!["):
        newline = stripped.find("\n")
        stripped = "" if newline == -1 else stripped[newline + 1:].lstrip()
    return stripped.startswith("//!") or stripped.startswith("/*!")


def valid_function_name(candidate: str) -> str | None:
    identifier = candidate[2:] if candidate.startswith("r#") else candidate
    return candidate if identifier.isidentifier() else None


def analyze_source(path: str, source: str) -> Analysis:
    code = mask_non_code(source)
    starts = line_starts(source)
    braces = matching_braces(code)

    functions: list[FunctionMetric] = []
    for match in FUNCTION_RE.finditer(code):
        name = valid_function_name(match.group(1))
        if name is None:
            continue
        body = find_function_body(code, match.end(), braces)
        if body is None:
            continue
        end = braces[body]
        start_line = line_number(starts, match.start())
        end_line = line_number(starts, end)
        functions.append(
            FunctionMetric(
                path=path,
                name=name,
                start_line=start_line,
                end_line=end_line,
                lines=end_line - start_line + 1,
                nesting=nested_brace_depth(code, body, end),
            )
        )

    closures = find_closure_metrics(path, code, starts, braces)
    match_arms = find_block_metrics(path, code, starts, braces, MATCH_ARM_RE)
    file_lines = len(source.splitlines())
    file_metric = FileMetric(
        path=path,
        lines=file_lines,
        starts_with_charter=starts_with_module_charter(source),
        functions=len(functions),
        closures=len(closures),
        match_arms=len(match_arms),
        max_function_nesting=max((item.nesting for item in functions), default=0),
    )
    return Analysis(file_metric, tuple(functions), tuple(closures), tuple(match_arms))


def find_closure_metrics(
    path: str,
    code: str,
    starts: list[int],
    braces: dict[int, int],
) -> list[BlockMetric]:
    metrics: list[BlockMetric] = []
    seen_bodies: set[int] = set()

    for opening, char in enumerate(code):
        if char != "|" or not is_closure_open(code, opening):
            continue
        closing = find_closure_bar(code, opening)
        if closing is None:
            continue
        body = find_closure_body(code, closing + 1, braces)
        if body is None or body in seen_bodies:
            continue
        seen_bodies.add(body)
        end = braces[body]
        start_line = line_number(starts, opening)
        end_line = line_number(starts, end)
        metrics.append(BlockMetric(path, start_line, end_line, end_line - start_line + 1))

    return metrics


def is_closure_open(code: str, position: int) -> bool:
    index = position - 1
    while index >= 0 and code[index].isspace():
        index -= 1
    if index < 0 or code[index] in "([{=,:;!>&":
        return True
    if not (code[index].isalnum() or code[index] == "_"):
        return False
    end = index + 1
    while index >= 0 and (code[index].isalnum() or code[index] == "_"):
        index -= 1
    return code[index + 1:end] in {"async", "break", "move", "return", "yield"}


def find_closure_bar(code: str, opening: int) -> int | None:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    index = opening + 1
    while index < len(code):
        char = code[index]
        if char in "([{":
            stack.append(char)
        elif char in pairs:
            if not stack or stack[-1] != pairs[char]:
                return None
            stack.pop()
        elif char == "|" and not stack:
            return index
        index += 1
    return None


def find_closure_body(code: str, position: int, braces: dict[int, int]) -> int | None:
    index = position
    while index < len(code) and code[index].isspace():
        index += 1
    if code.startswith("->", index):
        index += 2
    elif index < len(code) and code[index] == "{" and index in braces:
        return index
    else:
        return None

    parens = 0
    brackets = 0
    angles = 0
    while index < len(code):
        char = code[index]
        if char == "(":
            parens += 1
        elif char == ")" and parens:
            parens -= 1
        elif char == "[":
            brackets += 1
        elif char == "]" and brackets:
            brackets -= 1
        elif char == "<" and not parens:
            angles += 1
        elif char == ">" and angles and code[index - 1:index] != "-":
            angles -= 1
        elif char == "{" and index in braces:
            if parens or brackets or angles or previous_nonspace(code, index) == "!":
                index = braces[index] + 1
                continue
            return index
        elif char in ";=" and parens == brackets == angles == 0:
            return None
        index += 1
    return None


def find_block_metrics(
    path: str,
    code: str,
    starts: list[int],
    braces: dict[int, int],
    pattern: re.Pattern[str],
) -> list[BlockMetric]:
    metrics: list[BlockMetric] = []
    for match in pattern.finditer(code):
        body = code.rfind("{", match.start(), match.end())
        end = braces.get(body)
        if end is None:
            continue
        start_line = line_number(starts, match.start())
        end_line = line_number(starts, end)
        metrics.append(BlockMetric(path, start_line, end_line, end_line - start_line + 1))
    return metrics


def percentile(values: list[int], fraction: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, int(len(ordered) * fraction + 0.999999) - 1))
    return ordered[index]


def summarize(analyses: list[Analysis]) -> dict[str, object]:
    files = [item.file for item in analyses]
    functions = [metric for item in analyses for metric in item.functions]
    closures = [metric for item in analyses for metric in item.closures]
    match_arms = [metric for item in analyses for metric in item.match_arms]
    file_lines = [item.lines for item in files]
    function_lines = [item.lines for item in functions]
    return {
        "files": len(files),
        "lines": sum(file_lines),
        "files_starting_with_charters": sum(item.starts_with_charter for item in files),
        "file_lines_median": int(median(file_lines)) if file_lines else 0,
        "file_lines_p90": percentile(file_lines, 0.9),
        "functions": len(functions),
        "function_lines_median": int(median(function_lines)) if function_lines else 0,
        "function_lines_p90": percentile(function_lines, 0.9),
        "closures": len(closures),
        "match_arms": len(match_arms),
    }


def threshold_records(
    analyses: list[Analysis],
    file_lines: int,
    function_lines: int,
    nesting: int,
    closure_lines: int,
    match_arm_lines: int,
) -> dict[str, list[object]]:
    files = sorted(
        (item.file for item in analyses if item.file.lines >= file_lines),
        key=lambda item: (-item.lines, item.path),
    )
    not_starting_with_charters = sorted(
        (item.file for item in analyses if not item.file.starts_with_charter),
        key=lambda item: item.path,
    )
    functions = sorted(
        (
            metric
            for item in analyses
            for metric in item.functions
            if metric.lines >= function_lines
        ),
        key=lambda item: (-item.lines, -item.nesting, item.path, item.start_line),
    )
    deep_functions = sorted(
        (
            metric
            for item in analyses
            for metric in item.functions
            if metric.nesting >= nesting
        ),
        key=lambda item: (-item.nesting, -item.lines, item.path, item.start_line),
    )
    closures = sorted(
        (metric for item in analyses for metric in item.closures if metric.lines >= closure_lines),
        key=lambda item: (-item.lines, item.path, item.start_line),
    )
    match_arms = sorted(
        (metric for item in analyses for metric in item.match_arms if metric.lines >= match_arm_lines),
        key=lambda item: (-item.lines, item.path, item.start_line),
    )
    return {
        "files": files,
        "not_starting_with_charters": not_starting_with_charters,
        "functions": functions,
        "deep_functions": deep_functions,
        "closures": closures,
        "match_arms": match_arms,
    }


def output_document(
    repo: Path,
    args: argparse.Namespace,
    analyses: list[Analysis],
    records: dict[str, list[object]],
) -> dict[str, object]:
    limit = args.limit
    selected = {
        name: values[:limit] if limit > 0 else values
        for name, values in records.items()
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "notice": "Review triggers only; inspect source before treating a metric as structural debt.",
        "scope": {
            "repo": str(repo),
            "paths": args.path,
            "include_tests": args.include_tests,
        },
        "thresholds": {
            "file_lines": args.file_lines,
            "function_lines": args.function_lines,
            "nesting": args.nesting,
            "closure_lines": args.closure_lines,
            "match_arm_lines": args.match_arm_lines,
        },
        "summary": summarize(analyses),
        "trigger_counts": {name: len(values) for name, values in records.items()},
        "selection": {
            "limit": limit,
            "truncated": {
                name: len(selected[name]) < len(values)
                for name, values in records.items()
            },
        },
        "records": {
            name: [asdict(item) for item in values]
            for name, values in selected.items()
        },
    }


def print_table(document: dict[str, object]) -> None:
    summary = document["summary"]
    assert isinstance(summary, dict)
    print("Rust structural census (review triggers, not quality verdicts)")
    print(
        f"files={summary['files']} lines={summary['lines']} "
        f"starting_charters={summary['files_starting_with_charters']} functions={summary['functions']} "
        f"closures={summary['closures']} match_arms={summary['match_arms']}"
    )
    print(
        f"file lines: median={summary['file_lines_median']} p90={summary['file_lines_p90']} | "
        f"function lines: median={summary['function_lines_median']} p90={summary['function_lines_p90']}"
    )

    records = document["records"]
    counts = document["trigger_counts"]
    assert isinstance(records, dict) and isinstance(counts, dict)
    print_section("Large files", records["files"], counts["files"], file_row)
    print_section(
        "Files not starting with charters",
        records["not_starting_with_charters"],
        counts["not_starting_with_charters"],
        file_row,
    )
    print_section("Large functions", records["functions"], counts["functions"], function_row)
    print_section(
        "Deep functions",
        records["deep_functions"],
        counts["deep_functions"],
        function_row,
    )
    print_section("Large closures", records["closures"], counts["closures"], block_row)
    print_section("Large match arms", records["match_arms"], counts["match_arms"], block_row)


def print_section(name: str, rows: object, total: object, render: object) -> None:
    assert isinstance(rows, list) and isinstance(total, int) and callable(render)
    count = len(rows)
    label = f"showing {count} of {total} triggers" if count < total else f"{total} triggers"
    print(f"\n{name} ({label})")
    if not rows:
        print("  none")
        return
    for row in rows:
        assert isinstance(row, dict)
        print(f"  {render(row)}")


def file_row(row: dict[str, object]) -> str:
    charter = "starts-charter" if row["starts_with_charter"] else "no-start-charter"
    return f"{row['lines']:>5} lines  {charter:<16}  {row['path']}"


def function_row(row: dict[str, object]) -> str:
    return (
        f"{row['lines']:>5} lines  nest={row['nesting']:<2}  "
        f"{row['path']}:{row['start_line']}  {row['name']}"
    )


def block_row(row: dict[str, object]) -> str:
    return f"{row['lines']:>5} lines  {row['path']}:{row['start_line']}"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default=".", help="Git repository to inspect; default: current directory")
    parser.add_argument("--path", action="append", default=[], help="Restrict to a tracked pathspec; repeatable")
    parser.add_argument(
        "--include-tests",
        action="store_true",
        help="Include recognized test-file paths, fixtures, benches, and examples",
    )
    parser.add_argument("--limit", type=int, default=30, help="Rows per trigger category; 0 prints all")
    parser.add_argument("--file-lines", type=int, default=500, help="File-size review trigger")
    parser.add_argument("--function-lines", type=int, default=80, help="Function-size review trigger")
    parser.add_argument("--nesting", type=int, default=8, help="Nested-brace review trigger")
    parser.add_argument("--closure-lines", type=int, default=25, help="Closure-size review trigger")
    parser.add_argument("--match-arm-lines", type=int, default=20, help="Braced match-arm review trigger")
    parser.add_argument("--json", action="store_true", help="Emit stable JSON instead of a table")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        repo = repo_root(Path(args.repo).resolve())
        paths = tracked_rust_files(repo, args.path, args.include_tests)
        analyses = [
            analyze_source(path, (repo / path).read_text(encoding="utf-8"))
            for path in paths
        ]
    except (OSError, RuntimeError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    records = threshold_records(
        analyses,
        file_lines=args.file_lines,
        function_lines=args.function_lines,
        nesting=args.nesting,
        closure_lines=args.closure_lines,
        match_arm_lines=args.match_arm_lines,
    )
    document = output_document(repo, args, analyses, records)
    if args.json:
        print(json.dumps(document, indent=2, sort_keys=True))
    else:
        print_table(document)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
