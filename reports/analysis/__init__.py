"""
Analysis modules for performance benchmarking and statistical analysis
"""

from .benchmark_runner import BenchmarkRunner
from .statistical_analyzer import StatisticalAnalyzer
from .trend_detector import TrendDetector
from .memory_profiler import MemoryProfiler
from .recommendation_engine import RecommendationEngine

__all__ = [
    'BenchmarkRunner',
    'StatisticalAnalyzer',
    'TrendDetector',
    'MemoryProfiler',
    'RecommendationEngine'
]
