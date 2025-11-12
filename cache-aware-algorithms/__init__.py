"""
Cache-Aware Algorithms Package

A comprehensive collection of cache-optimized algorithm implementations.

Modules:
- search: Cache-efficient binary search variants
- matrix: Cache-blocked matrix multiplication
- trees: Cache-optimized B-trees
- sorting: Cache-oblivious sorting algorithms
- graph: Cache-optimized graph algorithms
- profiling: Cache profiling and analysis tools
- benchmarks: Performance benchmarking suite

Quick Start:
    from cache_aware_algorithms.search import CacheEfficientSearch
    from cache_aware_algorithms.profiling import CacheProfiler

For detailed documentation, see README.md
"""

__version__ = "1.0.0"
__author__ = "Algorithms Multiverse"

# Make key classes easily accessible
from .profiling.cache_profiler import CacheSimulator, CacheProfiler, AccessPatternAnalyzer

__all__ = [
    'CacheSimulator',
    'CacheProfiler',
    'AccessPatternAnalyzer',
]
