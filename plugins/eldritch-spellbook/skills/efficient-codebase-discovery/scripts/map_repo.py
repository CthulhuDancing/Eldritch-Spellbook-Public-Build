#!/usr/bin/env python3
"""Generate a concise structural map of a source repository.

Prefers Git-tracked files when available so generated/build/vendor content is
naturally excluded. Falls back to a conservative filesystem walk otherwise.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable


# Known filenames and directory names used to classify repository structure.
# These lists help the scanner recognize navigation docs, manifests, source roots,
# test folders, documentation folders, and common application entry points.
NAVIGATION_NAMES = {
    "AGENTS.md",
    "CONTRIBUTING",
    "CONTRIBUTING.md",
    "ARCHITECTURE.md",
    "CODEOWNERS",
    "CLAUDE.md",
}

MANIFEST_NAMES = {
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Pipfile",
    "poetry.lock",
    "uv.lock",
    "Cargo.toml",
    "go.mod",
    "go.work",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "Gemfile",
    "composer.json",
    "mix.exs",
    "deno.json",
    "deno.jsonc",
    "bun.lock",
    "bun.lockb",
    "pnpm-workspace.yaml",
    "Makefile",
    "CMakeLists.txt",
}

SOURCE_DIR_NAMES = {
    "src",
    "lib",
    "app",
    "apps",
    "packages",
    "services",
    "modules",
    "cmd",
    "internal",
}

TEST_DIR_NAMES = {
    "test",
    "tests",
    "spec",
    "specs",
    "__tests__",
}

DOC_DIR_NAMES = {
    "doc",
    "docs",
    "documentation",
}

ENTRYPOINT_BASENAMES = {
    "main.py",
    "app.py",
    "server.py",
    "manage.py",
    "main.ts",
    "main.tsx",
    "main.js",
    "main.jsx",
    "index.ts",
    "index.tsx",
    "index.js",
    "index.jsx",
    "Program.cs",
    "main.go",
    "main.rs",
}

CODE_EXTENSIONS = {
    ".c",
    ".cc",
    ".cjs",
    ".cpp",
    ".cs",
    ".go",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".mjs",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".swift",
    ".ts",
    ".tsx",
}

EXTENSION_ALIASES = {
    ".yml": ".yaml/.yml",
    ".yaml": ".yaml/.yml",
}
# =========


# Directories skipped during filesystem fallback scanning to avoid generated,
# vendored, cached, or otherwise noisy content.
IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    ".venv",
    "venv",
    "dist",
    "build",
    "coverage",
    ".next",
    ".cache",
    "target",
}
# =========


# Git helpers used to detect the repository root and retrieve the authoritative
# list of tracked files. This keeps the scanner focused on source-controlled
# content instead of generated, cached, or unrelated filesystem noise.
def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

def git_root(path: Path) -> Path | None:
    result = run_git(path, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        return None

    value = result.stdout.strip()
    return Path(value).resolve() if value else None

def git_files(root: Path) -> list[Path] | None:
    result = run_git(root, "ls-files", "-z")
    if result.returncode != 0:
        return None

    return [Path(path) for path in result.stdout.split("\0") if path]
# =========


# Filesystem fallback used when the target is not a Git repository. It walks
# the directory tree conservatively, skips common generated/vendor folders,
# and applies any requested depth limit to keep discovery proportional.
def filesystem_files(
    root: Path,
    max_depth: int | None,
) -> list[Path]:
    files: list[Path] = []

    for current, dirnames, filenames in os.walk(root):
        current_path = Path(current)

        try:
            relative = current_path.relative_to(root)
        except ValueError:
            continue

        current_depth = 0 if relative == Path(".") else len(relative.parts)

        dirnames[:] = sorted(
            directory
            for directory in dirnames
            if directory not in IGNORED_DIRS
        )

        if (
            max_depth is not None
            and current_depth >= max_depth
        ):
            dirnames[:] = []

        for filename in sorted(filenames):
            try:
                files.append(
                    (current_path / filename).relative_to(root)
                )
            except ValueError:
                continue

    return files

def within_depth(path: Path, max_depth: int | None) -> bool:
    if max_depth is None:
        return True

    return len(path.parts) - 1 <= max_depth
# =========


# File classification and manifest helpers used to recognize repository metadata,
# navigation files, and explicit structural hints declared by project manifests.
def is_readme(name: str) -> bool:
    upper = name.upper()
    return upper == "README" or upper.startswith("README.")

def is_manifest(path: Path) -> bool:
    name = path.name

    if name in MANIFEST_NAMES:
        return True

    lowered = name.lower()

    return (
        lowered.endswith(".sln")
        or lowered.endswith(".csproj")
        or lowered.startswith("dockerfile")
        or lowered.startswith("docker-compose")
        or lowered.startswith("compose.")
    )

def is_navigation(path: Path) -> bool:
    return is_readme(path.name) or path.name in NAVIGATION_NAMES

def read_json_file(
    root: Path,
    path: Path,
) -> dict:
    """Read a JSON object from the repository, returning an empty dict on failure."""
    try:
        with (root / path).open(
            "r",
            encoding="utf-8",
        ) as handle:
            value = json.load(handle)

        return value if isinstance(value, dict) else {}

    except (OSError, json.JSONDecodeError):
        return {}

def package_json_hints(
    root: Path,
    manifest: Path,
) -> dict[str, object]:
    """Extract structural repository hints from a package.json manifest."""
    data = read_json_file(root, manifest)
    hints: dict[str, object] = {}

    main = data.get("main")
    if isinstance(main, str):
        hints["main"] = main

    exports = data.get("exports")
    if isinstance(exports, (str, dict, list)):
        hints["exports"] = exports

    bin_value = data.get("bin")
    if isinstance(bin_value, (str, dict)):
        hints["bin"] = bin_value

    scripts = data.get("scripts")
    if isinstance(scripts, dict):
        start = scripts.get("start")

        if isinstance(start, str):
            hints["start"] = start

    workspaces = data.get("workspaces")
    if isinstance(workspaces, (list, dict)):
        hints["workspaces"] = workspaces

    return hints

def manifest_hints(
    root: Path,
    manifests: Iterable[Path],
) -> list[dict[str, object]]:
    """Extract supported structural hints from detected project manifests."""
    results: list[dict[str, object]] = []

    for manifest in manifests:
        if manifest.name != "package.json":
            continue

        hints = package_json_hints(
            root,
            manifest,
        )

        if not hints:
            continue

        results.append(
            {
                "manifest": manifest.as_posix(),
                "hints": hints,
            }
        )

    return results

def manifest_relative_path(
    manifest: Path,
    value: str,
) -> str:
    """Resolve a path declared by a manifest relative to that manifest."""
    cleaned = value.strip()

    if cleaned.startswith("./"):
        cleaned = cleaned[2:]

    parent = manifest.parent

    if str(parent) == ".":
        return Path(cleaned).as_posix()

    return (parent / cleaned).as_posix()

def direct_start_path(
    command: str,
) -> str | None:
    """Extract a directly executed source path from a simple start command."""
    parts = command.strip().split()

    if len(parts) < 2:
        return None

    if parts[0] in {"node", "bun"}:
        return parts[1]

    if (
        len(parts) >= 3
        and parts[0] == "deno"
        and parts[1] == "run"
    ):
        return parts[2]

    return None

def declared_entrypoints(
    manifest_metadata: Iterable[dict[str, object]],
) -> list[dict[str, str]]:
    """Convert supported manifest hints into explicit repository entry points."""
    found: list[dict[str, str]] = []

    for item in manifest_metadata:
        manifest = Path(str(item["manifest"]))
        hints = item["hints"]

        if not isinstance(hints, dict):
            continue

        main = hints.get("main")
        if isinstance(main, str):
            found.append(
                {
                    "path": manifest_relative_path(
                        manifest,
                        main,
                    ),
                    "source": f"{manifest.as_posix()}: main",
                }
            )

        exports = hints.get("exports")

        if isinstance(exports, str):
            found.append(
                {
                    "path": manifest_relative_path(
                        manifest,
                        exports,
                    ),
                    "source": f"{manifest.as_posix()}: exports",
                }
            )

        elif isinstance(exports, dict):
            root_export = exports.get(".")

            if isinstance(root_export, str):
                found.append(
                    {
                        "path": manifest_relative_path(
                            manifest,
                            root_export,
                        ),
                        "source": f"{manifest.as_posix()}: exports[.]",
                    }
                )

        bin_value = hints.get("bin")

        if isinstance(bin_value, str):
            found.append(
                {
                    "path": manifest_relative_path(
                        manifest,
                        bin_value,
                    ),
                    "source": f"{manifest.as_posix()}: bin",
                }
            )

        elif isinstance(bin_value, dict):
            for value in bin_value.values():
                if isinstance(value, str):
                    found.append(
                        {
                            "path": manifest_relative_path(
                                manifest,
                                value,
                            ),
                            "source": f"{manifest.as_posix()}: bin",
                        }
                    )

        start = hints.get("start")

        if isinstance(start, str):
            start_path = direct_start_path(start)

            if start_path:
                found.append(
                    {
                        "path": manifest_relative_path(
                            manifest,
                            start_path,
                        ),
                        "source": f"{manifest.as_posix()}: scripts.start",
                    }
                )

    unique: dict[str, dict[str, str]] = {}

    for item in found:
        unique.setdefault(item["path"], item)

    return sorted(
        unique.values(),
        key=lambda item: (
            item["path"].count("/"),
            item["path"].lower(),
        ),
    )
# =========


# Repository structure helpers used to summarize where files are concentrated,
# which file types are present, and where common source/test/doc roots appear.
def directory_counts(files: Iterable[Path]) -> Counter[str]:
    counts: Counter[str] = Counter()

    for path in files:
        top = path.parts[0] if len(path.parts) > 1 else "."
        counts[top] += 1

    return counts

def extension_label(
    path: Path,
) -> str:
    """Return a useful file-type label for repository summary output."""
    name = path.name

    if name.startswith("."):
        return "[dotfile/config]"

    extension = path.suffix.lower()

    if not extension:
        return "[no extension]"

    return EXTENSION_ALIASES.get(
        extension,
        extension,
    )

def extension_counts(
    files: Iterable[Path],
) -> Counter[str]:
    """Count repository files by normalized extension or special-file type."""
    counts: Counter[str] = Counter()

    for path in files:
        counts[extension_label(path)] += 1

    return counts

def is_under_named_dir(
    path: Path,
    names: set[str],
) -> bool:
    """Return True when any parent directory matches one of the given names."""
    return any(
        part.lower() in names
        for part in path.parts[:-1]
    )

def unique_dirs(
    files: Iterable[Path],
    names: set[str],
    excluded_ancestors: set[str] | None = None,
) -> list[str]:
    found: set[str] = set()

    for path in files:
        for index, part in enumerate(path.parts[:-1]):
            if part.lower() not in names:
                continue

            candidate = Path(*path.parts[: index + 1])

            if (
                excluded_ancestors
                and is_under_named_dir(
                    candidate,
                    excluded_ancestors,
                )
            ):
                continue

            found.add(candidate.as_posix() + "/")

    return sorted(
        found,
        key=lambda value: (
            value.count("/"),
            value.lower(),
        ),
    )

def code_surface_counts(
    files: Iterable[Path],
) -> Counter[str]:
    """Count implementation files by top-level repository area."""
    counts: Counter[str] = Counter()

    for path in files:
        if path.suffix.lower() not in CODE_EXTENSIONS:
            continue

        if is_under_named_dir(
            path,
            TEST_DIR_NAMES | DOC_DIR_NAMES,
        ):
            continue

        if len(path.parts) == 1:
            surface = "."
        else:
            surface = path.parts[0]

        if surface.startswith("."):
            continue

        counts[surface] += 1

    return counts

def surface_has_source_root(
    surface: str,
    source_roots: Iterable[str],
) -> bool:
    """Return True when a candidate surface already contains a known source root."""
    if surface == ".":
        return False

    prefix = surface.rstrip("/") + "/"

    return any(
        source_root.startswith(prefix)
        for source_root in source_roots
    )

def candidate_code_surfaces(
    files: Iterable[Path],
    source_roots: Iterable[str],
    minimum_files: int = 2,
) -> list[dict[str, object]]:
    """Find substantial code areas not already represented by known source roots."""
    counts = code_surface_counts(files)
    candidates: list[dict[str, object]] = []

    for surface, count in counts.items():
        if count < minimum_files:
            continue

        if surface_has_source_root(
            surface,
            source_roots,
        ):
            continue

        display_path = "./" if surface == "." else f"{surface}/"

        candidates.append(
            {
                "path": display_path,
                "files": count,
            }
        )

    return sorted(
        candidates,
        key=lambda item: (
            -int(item["files"]),
            str(item["path"]).lower(),
        ),
    )
# =========


# Candidate and path-list helpers used to surface conventional entry points
# and keep path output concise, unique, and consistently ordered.
def entrypoint_candidates(
    files: Iterable[Path],
) -> list[str]:
    candidates = [
        path.as_posix()
        for path in files
        if path.name in ENTRYPOINT_BASENAMES
    ]

    return sorted(
        candidates,
        key=lambda value: (
            value.count("/"),
            value.lower(),
        ),
    )

def compact_paths(
    paths: Iterable[Path],
    limit: int,
) -> list[str]:
    values = sorted(
        {path.as_posix() for path in paths},
        key=lambda value: (
            value.count("/"),
            value.lower(),
        ),
    )

    return values[:limit]
# =========


# Main repository mapping routine. It chooses Git or filesystem inventory,
# classifies the discovered files, and assembles the final structured summary.
#
# Args:
#   path: Repository or directory to scan.
#   max_depth: Optional directory-depth limit for the scan.
#   limit: Maximum number of entries returned per summary section.
def build_map(
    path: Path,
    max_depth: int | None,
    limit: int,
) -> dict[str, object]:
    requested = path.resolve()

    repo_root = git_root(requested)
    root = repo_root or requested

    tracked = git_files(root) if repo_root else None

    if tracked is not None:
        inventory_source = "git"
        files = tracked
    else:
        inventory_source = "filesystem"
        files = filesystem_files(
            root,
            max_depth,
        )

    files = [
        path
        for path in files
        if within_depth(path, max_depth)
    ]

    manifests = [
        path
        for path in files
        if is_manifest(path)
    ]

    manifest_metadata = manifest_hints(
        root,
        manifests,
    )

    declared_entries = declared_entrypoints(
        manifest_metadata,
    )

    navigation = [
        path
        for path in files
        if is_navigation(path)
    ]

    source_roots = unique_dirs(
        files,
        SOURCE_DIR_NAMES,
        TEST_DIR_NAMES | DOC_DIR_NAMES,
    )

    code_surfaces = candidate_code_surfaces(
        files,
        source_roots,
    )

    dir_counts = directory_counts(files)
    ext_counts = extension_counts(files)

    return {
        "root": str(root),
        "source": inventory_source,
        "file_count": len(files),
        "max_depth": max_depth,
        "manifests": compact_paths(manifests, limit),
        "manifest_metadata": manifest_metadata,
        "declared_entrypoints": declared_entries,
        "navigation_files": compact_paths(navigation, limit),
        "source_roots": source_roots[:limit],
        "candidate_code_surfaces": code_surfaces[:limit],
        "test_roots": unique_dirs(
            files,
            TEST_DIR_NAMES,
        )[:limit],
        "doc_roots": unique_dirs(
            files,
            DOC_DIR_NAMES,
        )[:limit],
        "entrypoint_candidates": entrypoint_candidates(
            files
        )[:limit],
        "top_directories": [
            {
                "path": name,
                "files": count,
            }
            for name, count in sorted(
                dir_counts.items(),
                key=lambda item: (
                    -item[1],
                    item[0].lower(),
                ),
            )[:limit]
        ],
        "extensions": [
            {
                "extension": extension,
                "files": count,
            }
            for extension, count in sorted(
                ext_counts.items(),
                key=lambda item: (
                    -item[1],
                    item[0],
                ),
            )[:limit]
        ],
    }
# =========


# Human-readable output formatter. Converts the structured repository map into
# the concise text report shown by default.
#
# Args:
#   data: Repository summary dictionary produced by build_map().
def render_text(
    data: dict[str, object],
) -> str:
    lines: list[str] = []

    lines.append(
        f"Repository root: {data['root']}"
    )
    lines.append(
        f"Inventory source: {data['source']}"
    )
    lines.append(
        f"Files considered: {data['file_count']}"
    )

    if data["max_depth"] is not None:
        lines.append(
            f"Maximum depth: {data['max_depth']}"
        )

    def section(
        title: str,
        values: list[str],
    ) -> None:
        lines.append("")
        lines.append(f"{title}:")

        if not values:
            lines.append("- none detected")
            return

        lines.extend(
            f"- {value}"
            for value in values
        )

    section(
        "Detected manifests",
        data["manifests"],
    )

    lines.append("")
    lines.append("Declared entry points:")

    declared_entries = data["declared_entrypoints"]

    if not declared_entries:
        lines.append("- none detected")
    else:
        for item in declared_entries:
            lines.append(
                f"- {item['path']} "
                f"({item['source']})"
        )

    section(
        "Navigation files",
        data["navigation_files"],
    )
    section(
        "Likely source roots",
        data["source_roots"],
    )

    lines.append("")
    lines.append("Candidate code surfaces:")

    code_surfaces = data["candidate_code_surfaces"]

    if not code_surfaces:
        lines.append("- none detected")
    else:
        for item in code_surfaces:
            lines.append(
                f"- {item['path']} "
                f"({item['files']} code files)"
            )

    section(
        "Likely test roots",
        data["test_roots"],
    )
    section(
        "Documentation roots",
        data["doc_roots"],
    )
    section(
        "Entry-point candidates",
        data["entrypoint_candidates"],
    )

    lines.append("")
    lines.append("Top-level file distribution:")

    top_directories = data["top_directories"]

    if not top_directories:
        lines.append("- none")
    else:
        for item in top_directories:
            lines.append(
                f"- {item['path']}: "
                f"{item['files']}"
            )

    lines.append("")
    lines.append("File types:")

    extensions = data["extensions"]

    if not extensions:
        lines.append("- none")
    else:
        for item in extensions:
            lines.append(
                f"- {item['extension']}: "
                f"{item['files']}"
            )

    return "\n".join(lines)
# =========


# JSON output formatter. Keeps the complete structured map, including raw
# manifest hints that are not displayed in the text summaries.
#
# Args:
#   data: Repository summary dictionary produced by build_map().
def render_json(
    data: dict[str, object],
) -> str:
    return json.dumps(
        data,
        indent=2,
        sort_keys=False,
    )
# =========


# Compact output formatter. Groups the same evidence as render_text() under
# short headings, without blank lines, bullets, or empty sections. This reduces
# repeated text for agent consumption while keeping the report readable.
#
# Args:
#   data: Repository summary dictionary produced by build_map().
def render_compact(
    data: dict[str, object],
) -> str:
    lines: list[str] = [
        f"root: {data['root']}",
        f"inventory: {data['source']}",
        f"files: {data['file_count']}",
    ]

    if data["max_depth"] is not None:
        lines.append(f"depth: {data['max_depth']}")

    # A heading applies to all following indented entries, so each entry
    # needs only its value. Missing sections mean there were no entries.
    def section(
        title: str,
        values: list[str],
    ) -> None:
        if not values:
            return

        lines.append(f"{title}:")
        lines.extend(f"  {value}" for value in values)

    section("manifests", data["manifests"])
    section(
        "declared entries",
        [
            f"{item['path']} <- {item['source']}"
            for item in data["declared_entrypoints"]
        ],
    )
    section("navigation", data["navigation_files"])
    section("likely source roots", data["source_roots"])
    section(
        "candidate code surfaces (code files)",
        [
            f"{item['path']}: {item['files']}"
            for item in data["candidate_code_surfaces"]
        ],
    )
    section("likely test roots", data["test_roots"])
    section("doc roots", data["doc_roots"])
    section("entry candidates", data["entrypoint_candidates"])
    section(
        "top directories (files)",
        [
            f"{item['path']}: {item['files']}"
            for item in data["top_directories"]
        ],
    )
    section(
        "file types (files)",
        [
            f"{item['extension']}: {item['files']}"
            for item in data["extensions"]
        ],
    )

    return "\n".join(lines)
# =========


# Command-line argument parser. Defines the supported script options and turns
# the user's CLI input into values the main routine can use.
#
# Supports:
#   path: Repository or directory to scan.
#   --format: Choose text, JSON, or compact output.
#   --json: Compatibility alias for --format json.
#   --max-depth: Limit how deep the scan considers files.
#   --limit: Limit summary sections, excluding declared entries and raw hints.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a concise, read-only structural "
            "map of a source repository."
        )
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help=(
            "Repository or directory to inspect "
            "(default: current directory)."
        ),
    )

    # Output selectors are mutually exclusive so conflicting choices produce
    # a clear error instead of silently overriding one another.
    output = parser.add_mutually_exclusive_group()
    output.add_argument(
        "--format",
        choices=("text", "json", "compact"),
        default="text",
        help="Output format (default: text).",
    )
    output.add_argument(
        "--json",
        dest="format",
        action="store_const",
        const="json",
        help="Alias for --format json.",
    )

    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help=(
            "Only consider files at or below this "
            "directory depth relative to the root."
        ),
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help=(
            "Maximum entries per summary section (default: 20); "
            "declared entry points and raw manifest hints are not limited."
        ),
    )

    return parser.parse_args()
# =========


# Program entry point. Validates user input, builds the repository map, selects
# text, JSON, or compact output, and returns an appropriate process exit code.
#
# Exit codes:
#   0: Successful scan.
#   2: Invalid path or command-line value.
def main() -> int:
    args = parse_args()

    path = Path(args.path).expanduser()

    if not path.exists():
        print(
            f"error: path does not exist: {path}",
            file=sys.stderr,
        )
        return 2

    if not path.is_dir():
        print(
            f"error: path is not a directory: {path}",
            file=sys.stderr,
        )
        return 2

    if (
        args.max_depth is not None
        and args.max_depth < 0
    ):
        print(
            "error: --max-depth must be >= 0",
            file=sys.stderr,
        )
        return 2

    if args.limit < 1:
        print(
            "error: --limit must be >= 1",
            file=sys.stderr,
        )
        return 2

    data = build_map(
        path,
        args.max_depth,
        args.limit,
    )

    if args.format == "json":
        print(render_json(data))
    elif args.format == "compact":
        print(render_compact(data))
    else:
        print(render_text(data))

    return 0
# ============

if __name__ == "__main__":
    raise SystemExit(main())
