"""
Convenience package exposing a stable import path for key Algorithms Multiverse modules.

The original repository organizes source files in directories that are not valid Python
package names (for example ``graph-algorithms``).  This package dynamically loads those
modules so tooling such as MkDocs + mkdocstrings can import them without renaming files.
"""

from __future__ import annotations

import importlib.util
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path
from types import ModuleType
from typing import Dict

_REPO_ROOT = Path(__file__).resolve().parent.parent

_MODULE_MAP: Dict[str, Path] = {
    "graph_generators_extended": _REPO_ROOT / "graph-algorithms" / "graph_generators_extended.py",
    "graph_advanced": _REPO_ROOT / "graph-algorithms" / "graph_advanced.py",
    "mst_algorithms": _REPO_ROOT / "graph-algorithms" / "mst_algorithms.py",
    "mst_network_applications": _REPO_ROOT / "graph-algorithms" / "mst_network_applications.py",
    "mst_visualization": _REPO_ROOT / "graph-algorithms" / "mst_visualization.py",
    "aggregate_results": _REPO_ROOT / "graph-algorithms" / "aggregate_results.py",
    "benchmark_py": _REPO_ROOT / "graph-algorithms" / "benchmark_py.py",
}

__all__ = ["graph", "mst_benchmark"] + sorted(_MODULE_MAP)


def _load_module(name: str, path: Path) -> ModuleType:
    """Dynamically load the requested module and register it under this package."""
    module_name = f"{__name__}.{name}"
    if module_name in sys.modules:
        return sys.modules[module_name]

    if not path.exists():
        raise ModuleNotFoundError(f"Module '{module_name}' file not found at {path}")

    loader = SourceFileLoader(module_name, str(path))
    module_dir = str(path.parent)
    if module_dir not in sys.path:
        sys.path.append(module_dir)
    spec = importlib.util.spec_from_loader(module_name, loader)
    if spec is None:
        raise ImportError(f"Unable to create spec for {module_name}")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    sys.modules[module_name] = module
    # Expose as attribute so `from algorithms_multiverse import graph` works.
    setattr(sys.modules[__name__], name, module)
    return module


def __getattr__(name: str) -> ModuleType:
    """Load modules on first attribute access to keep import overhead low."""
    if name in _MODULE_MAP:
        return _load_module(name, _MODULE_MAP[name])
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
