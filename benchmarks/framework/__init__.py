"""
Benchmark Framework for Algorithms Multiverse

Cross-language performance testing and analysis framework.
"""

__version__ = "1.0.0"
__author__ = "Algorithms Multiverse"

from .runner import BenchmarkRunner, BenchmarkResult
from .analyzer import BenchmarkAnalyzer, PerformanceMetrics, RegressionAlert

__all__ = [
    'BenchmarkRunner',
    'BenchmarkResult',
    'BenchmarkAnalyzer',
    'PerformanceMetrics',
    'RegressionAlert'
]
