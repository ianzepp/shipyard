#!/usr/bin/env python3
"""Record files inspected during a polish pass so the suggest-polish-files
analyzer can skip them without requiring a commit.

Usage:
  # Mark files as inspected (records current timestamp)
  polish-inspected.py --repo . --files src/foo.rs src/bar.py

  # Read file list from stdin
  echo "src/foo.rs" | polish-inspected.py --repo . --stdin

  # List currently recorded inspected files
  polish-inspected.py --repo . --list

  # Prune entries where the file on disk has been modified since inspection
  polish-inspected.py --repo . --prune

  # Custom output path
  polish-inspected.py --repo . --output docs/polish/inspected.json --files src/foo.rs
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_INSPECTED_FILE = ".polish-inspected.json"


def repo_root(path: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=path,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "not a git repository")
    return Path(result.stdout.strip())


def load_inspected(inspected_path: Path) -> dict[str, str]:
    """Return {path: iso_timestamp} or empty dict if file missing/corrupt."""
    if not inspected_path.exists():
        return {}
    try:
        with open(inspected_path) as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            return {}
        return {k: v for k, v in data.items() if isinstance(k, str) and isinstance(v, str)}
    except (json.JSONDecodeError, OSError):
        return {}


def save_inspected(inspected_path: Path, data: dict[str, str]) -> None:
    inspected_path.parent.mkdir(parents=True, exist_ok=True)
    with open(inspected_path, "w") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
        fh.write("\n")


def file_last_modified_epoch(repo: Path, file_path: str) -> int | None:
    """Return the epoch timestamp of the last commit that touched the file."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "--", file_path],
        cwd=repo,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    output = result.stdout.strip()
    if not output:
        return None
    try:
        return int(output)
    except ValueError:
        return None


def file_exists_in_worktree(repo: Path, file_path: str) -> bool:
    """Check whether the file still exists on disk (not deleted)."""
    return (repo / file_path).exists()


def record_files(
    repo: Path,
    inspected_path: Path,
    files: list[str],
) -> int:
    """Add or update inspection entries for the given files.  Returns count of
    files recorded (excluding those that don't exist)."""
    data = load_inspected(inspected_path)
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    count = 0

    for file_path in files:
        file_path = file_path.strip()
        if not file_path:
            continue
        if not file_exists_in_worktree(repo, file_path):
            print(f"warning: skipping {file_path} — file does not exist in worktree", file=sys.stderr)
            continue
        data[file_path] = now
        count += 1

    if count > 0:
        save_inspected(inspected_path, data)
        print(f"Recorded {count} file(s) in {inspected_path}")
    return count


def list_files(data: dict[str, str]) -> None:
    if not data:
        print("No inspected files recorded.")
        return
    for path, ts in sorted(data.items()):
        print(f"{ts[:19]:<19}  {path}")


def prune_files(repo: Path, data: dict[str, str]) -> dict[str, str]:
    """Remove entries where the file on disk has been modified since
    the inspection timestamp.  Also removes entries for deleted files."""
    pruned: dict[str, str] = {}
    removed = 0
    now_epoch = int(dt.datetime.now(dt.timezone.utc).timestamp())

    for path, ts_str in sorted(data.items()):
        try:
            inspected_epoch = int(dt.datetime.fromisoformat(ts_str).timestamp())
        except (ValueError, OSError):
            removed += 1
            continue

        if not file_exists_in_worktree(repo, path):
            print(f"pruned (deleted): {path}")
            removed += 1
            continue

        last_mod = file_last_modified_epoch(repo, path)
        if last_mod is not None and last_mod > inspected_epoch:
            print(f"pruned (modified after inspection): {path}")
            removed += 1
            continue

        pruned[path] = ts_str

    if removed > 0:
        print(f"Pruned {removed} stale entr{'y' if removed == 1 else 'ies'}.")
    return pruned


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", "-r", default=".", help="Git repository root; default: current directory")
    parser.add_argument(
        "--output", "-o",
        default=None,
        help=f"Inspection data file path relative to repo root; default: {DEFAULT_INSPECTED_FILE}",
    )
    parser.add_argument("--files", "-f", nargs="*", default=[], help="File paths to mark as inspected")
    parser.add_argument("--stdin", action="store_true", help="Read file paths from stdin (one per line)")
    parser.add_argument("--list", "-l", action="store_true", help="List currently inspected files")
    parser.add_argument("--prune", "-p", action="store_true", help="Remove entries for files modified since inspection")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        repo = repo_root(Path(args.repo).resolve())
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    output_rel = args.output or DEFAULT_INSPECTED_FILE
    inspected_path = repo / output_rel

    # Collect files from --files and optionally --stdin
    file_list = list(args.files)
    if args.stdin:
        file_list.extend(line.rstrip("\n") for line in sys.stdin)

    action_taken = False

    if args.list:
        data = load_inspected(inspected_path)
        list_files(data)
        action_taken = True

    if args.prune:
        data = load_inspected(inspected_path)
        pruned = prune_files(repo, data)
        if pruned != data:
            save_inspected(inspected_path, pruned)
        action_taken = True

    if file_list:
        record_files(repo, inspected_path, file_list)
        action_taken = True

    if not action_taken:
        print("Nothing to do. Use --files, --stdin, --list, or --prune.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
