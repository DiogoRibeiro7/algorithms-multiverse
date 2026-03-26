#!/usr/bin/env python3
"""Fail the build if docstring coverage drops below the configured threshold."""

from __future__ import annotations

import ast
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = [
    PROJECT_ROOT / "docs" / "site",
    PROJECT_ROOT / "docs" / "output",
    PROJECT_ROOT / "site",
]
SKIP_PARTS = {".git", "__pycache__"}
SKIP_FILES = {"setup.py"}
THRESHOLD = float(os.environ.get("DOCSTRING_COVERAGE_THRESHOLD", "1.0"))


def should_skip(path: Path) -> bool:
    """Return True when the file lives inside an ignored directory or name."""
    for skip_dir in SKIP_DIRS:
        try:
            path.relative_to(skip_dir)
            return True
        except ValueError:
            continue
    if any(part in SKIP_PARTS for part in path.parts):
        return True
    if path.name in SKIP_FILES:
        return True
    if path.name.startswith("test_") or path.name.endswith("_test.py"):
        return True
    if "tests" in path.parts:
        return True
    return False


def iter_python_files() -> list[Path]:
    """Return a list of Python sources inside the repository root."""
    return [path for path in PROJECT_ROOT.rglob("*.py") if not should_skip(path)]


def collect_counts() -> tuple[int, int, int, int]:
    """Return aggregated module/public docstring counts."""
    module_total = module_doc_total = 0
    public_total = public_doc_total = 0

    for path in iter_python_files():
        text = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue

        module_total += 1
        if ast.get_docstring(tree):
            module_doc_total += 1

        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("_"):
                    continue
                public_total += 1
                if ast.get_docstring(node):
                    public_doc_total += 1
            elif isinstance(node, ast.ClassDef):
                if node.name.startswith("_"):
                    continue
                public_total += 1
                if ast.get_docstring(node):
                    public_doc_total += 1
                for method in node.body:
                    if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)) and not method.name.startswith("_"):
                        public_total += 1
                        if ast.get_docstring(method):
                            public_doc_total += 1

    return module_total, module_doc_total, public_total, public_doc_total


def main() -> int:
    """Entrypoint for CLI usage."""
    module_total, module_doc_total, public_total, public_doc_total = collect_counts()

    def ratio(documented: int, total: int) -> float:
        return 1.0 if total == 0 else documented / total

    module_ratio = ratio(module_doc_total, module_total)
    public_ratio = ratio(public_doc_total, public_total)

    print(
        f"Docstring coverage: modules {module_doc_total}/{module_total}"
        f" ({module_ratio:.3%}), public objects {public_doc_total}/{public_total}"
        f" ({public_ratio:.3%})"
    )

    if module_ratio < THRESHOLD or public_ratio < THRESHOLD:
        print(
            f"Docstring coverage below threshold {THRESHOLD:.0%}."
            " Run tools/docstring_coverage.py locally before committing."
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
