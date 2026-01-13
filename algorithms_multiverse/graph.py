"""Compatibility wrapper that exposes graph algorithms as a regular Python package."""

from __future__ import annotations

import importlib.util
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path

_GRAPH_DIR = Path(__file__).resolve().parent.parent / "graph-algorithms"
_GRAPH_STR = str(_GRAPH_DIR)
if _GRAPH_STR not in sys.path:
    sys.path.append(_GRAPH_STR)

_SOURCE_PATH = _GRAPH_DIR / "graph.py"
_LOADER = SourceFileLoader(__name__, str(_SOURCE_PATH))
_SPEC = importlib.util.spec_from_loader(__name__, _LOADER)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Unable to create spec for {_SOURCE_PATH}")
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[__name__] = _MODULE
_SPEC.loader.exec_module(_MODULE)
