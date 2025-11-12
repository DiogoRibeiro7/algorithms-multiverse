"""
Comprehensive Benchmarking Suite for Parallel Algorithms

This module provides tools for benchmarking and analyzing parallel algorithms:
- Performance measurement
- Scalability analysis (strong and weak scaling)
- Speedup and efficiency calculation
- Amdahl's and Gustafson's law verification
- Visualization and reporting

Features:
- Automated testing across different sizes
- Thread scaling analysis
- Comparison across algorithms
- Statistical analysis (mean, stddev, confidence intervals)
- Export to CSV and JSON

Author: Algorithms Multiverse
"""

import sys
import os
import time
import statistics
import json
import csv
from typing import List, Dict, Tuple, Callable, Any
from dataclasses import dataclass, asdict
import multiprocessing as mp

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@dataclass
class BenchmarkResult:
    """Single benchmark result"""
    algorithm: str
    method: str
    size: int
    num_workers: int
    time_taken: float
    speedup: float
    efficiency: float
    operations: int = 0


@dataclass
class ScalingAnalysis:
    """Scaling analysis results"""
    algorithm: str
    size: int
    worker_counts: List[int]
    times: List[float]
    speedups: List[float]
    efficiencies: List[float]
    scaling_type: str  # "strong" or "weak"


class PerformanceAnalyzer:
    """
    Comprehensive performance analysis for parallel algorithms.
    """

    def __init__(self):
        self.results: List[BenchmarkResult] = []

    def benchmark_function(self,
                          func: Callable,
                          args: tuple = (),
                          runs: int = 3) -> Tuple[float, float]:
        """
        Benchmark a function with multiple runs.

        Args:
            func: Function to benchmark
            args: Arguments to pass to function
            runs: Number of runs for averaging

        Returns:
            Tuple of (mean_time, stddev_time)
        """
        times = []

        for _ in range(runs):
            start = time.perf_counter()
            func(*args)
            elapsed = time.perf_counter() - start
            times.append(elapsed)

        return statistics.mean(times), statistics.stdev(times) if len(times) > 1 else 0

    def strong_scaling_analysis(self,
                                algorithm_func: Callable,
                                size: int,
                                max_workers: int = None,
                                runs: int = 3) -> ScalingAnalysis:
        """
        Strong scaling analysis: Fixed problem size, varying workers.

        Measures how execution time decreases as workers increase
        for a fixed problem size.

        Args:
            algorithm_func: Function(size, num_workers) -> result
            size: Problem size (fixed)
            max_workers: Maximum number of workers
            runs: Number of runs per configuration

        Returns:
            ScalingAnalysis results
        """
        if max_workers is None:
            max_workers = mp.cpu_count()

        worker_counts = list(range(1, max_workers + 1))
        times = []
        speedups = []
        efficiencies = []

        # Baseline (sequential or 1 worker)
        baseline_time, _ = self.benchmark_function(
            algorithm_func, args=(size, 1), runs=runs
        )

        for workers in worker_counts:
            mean_time, _ = self.benchmark_function(
                algorithm_func, args=(size, workers), runs=runs
            )

            speedup = baseline_time / mean_time if mean_time > 0 else 0
            efficiency = speedup / workers if workers > 0 else 0

            times.append(mean_time)
            speedups.append(speedup)
            efficiencies.append(efficiency)

        return ScalingAnalysis(
            algorithm="strong_scaling",
            size=size,
            worker_counts=worker_counts,
            times=times,
            speedups=speedups,
            efficiencies=efficiencies,
            scaling_type="strong"
        )

    def weak_scaling_analysis(self,
                              algorithm_func: Callable,
                              base_size: int,
                              max_workers: int = None,
                              runs: int = 3) -> ScalingAnalysis:
        """
        Weak scaling analysis: Problem size scales with workers.

        Measures how execution time changes when both problem size
        and workers increase proportionally.

        Args:
            algorithm_func: Function(size, num_workers) -> result
            base_size: Base problem size per worker
            max_workers: Maximum number of workers
            runs: Number of runs per configuration

        Returns:
            ScalingAnalysis results
        """
        if max_workers is None:
            max_workers = mp.cpu_count()

        worker_counts = list(range(1, max_workers + 1))
        times = []
        speedups = []
        efficiencies = []

        # Baseline (1 worker with base size)
        baseline_time, _ = self.benchmark_function(
            algorithm_func, args=(base_size, 1), runs=runs
        )

        for workers in worker_counts:
            # Scale problem size with workers
            size = base_size * workers

            mean_time, _ = self.benchmark_function(
                algorithm_func, args=(size, workers), runs=runs
            )

            # For weak scaling, ideal time should remain constant
            speedup = baseline_time / mean_time if mean_time > 0 else 0
            efficiency = speedup / workers if workers > 0 else 0

            times.append(mean_time)
            speedups.append(speedup)
            efficiencies.append(efficiency)

        return ScalingAnalysis(
            algorithm="weak_scaling",
            size=base_size,
            worker_counts=worker_counts,
            times=times,
            speedups=speedups,
            efficiencies=efficiencies,
            scaling_type="weak"
        )

    def calculate_speedup(self, sequential_time: float, parallel_time: float) -> float:
        """Calculate speedup: S = T_sequential / T_parallel"""
        return sequential_time / parallel_time if parallel_time > 0 else 0

    def calculate_efficiency(self, speedup: float, num_workers: int) -> float:
        """Calculate efficiency: E = Speedup / NumWorkers"""
        return speedup / num_workers if num_workers > 0 else 0

    def amdahls_law(self, parallel_fraction: float, num_workers: int) -> float:
        """
        Amdahl's Law: Maximum speedup with fixed problem size.

        S(n) = 1 / ((1 - p) + p/n)

        where:
        - p is the parallel fraction
        - n is the number of workers

        Args:
            parallel_fraction: Fraction of code that can be parallelized (0-1)
            num_workers: Number of workers

        Returns:
            Maximum theoretical speedup
        """
        if parallel_fraction < 0 or parallel_fraction > 1:
            raise ValueError("Parallel fraction must be between 0 and 1")

        serial_fraction = 1 - parallel_fraction
        return 1 / (serial_fraction + parallel_fraction / num_workers)

    def gustafson_law(self, parallel_fraction: float, num_workers: int) -> float:
        """
        Gustafson's Law: Speedup with scaled problem size.

        S(n) = (1 - p) + p * n

        where:
        - p is the parallel fraction
        - n is the number of workers

        Args:
            parallel_fraction: Fraction of code that can be parallelized (0-1)
            num_workers: Number of workers

        Returns:
            Maximum theoretical speedup with scaled workload
        """
        if parallel_fraction < 0 or parallel_fraction > 1:
            raise ValueError("Parallel fraction must be between 0 and 1")

        serial_fraction = 1 - parallel_fraction
        return serial_fraction + parallel_fraction * num_workers

    def add_result(self, result: BenchmarkResult):
        """Add a benchmark result"""
        self.results.append(result)

    def export_csv(self, filename: str):
        """Export results to CSV file"""
        if not self.results:
            print("No results to export")
            return

        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=asdict(self.results[0]).keys())
            writer.writeheader()
            for result in self.results:
                writer.writerow(asdict(result))

        print(f"Results exported to {filename}")

    def export_json(self, filename: str):
        """Export results to JSON file"""
        if not self.results:
            print("No results to export")
            return

        data = [asdict(result) for result in self.results]

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Results exported to {filename}")

    def print_summary(self):
        """Print summary of benchmark results"""
        if not self.results:
            print("No results available")
            return

        print("\n" + "=" * 80)
        print("BENCHMARK SUMMARY")
        print("=" * 80)

        # Group by algorithm
        by_algorithm = {}
        for result in self.results:
            key = (result.algorithm, result.method)
            if key not in by_algorithm:
                by_algorithm[key] = []
            by_algorithm[key].append(result)

        for (algorithm, method), results in by_algorithm.items():
            print(f"\n{algorithm} - {method}")
            print("-" * 80)
            print(f"{'Size':<12} {'Workers':<10} {'Time (s)':<12} {'Speedup':<10} {'Efficiency':<12}")
            print("-" * 80)

            for result in results:
                print(f"{result.size:<12,} {result.num_workers:<10} "
                      f"{result.time_taken:>10.6f}  "
                      f"{result.speedup:>8.2f}x  "
                      f"{result.efficiency:>10.2%}")


def print_scaling_analysis(analysis: ScalingAnalysis):
    """Print scaling analysis results"""
    print(f"\n{analysis.scaling_type.upper()} SCALING ANALYSIS")
    print(f"Algorithm: {analysis.algorithm}")
    print(f"Size: {analysis.size:,}")
    print("-" * 80)
    print(f"{'Workers':<10} {'Time (s)':<12} {'Speedup':<10} {'Efficiency':<12}")
    print("-" * 80)

    for i, workers in enumerate(analysis.worker_counts):
        print(f"{workers:<10} {analysis.times[i]:>10.6f}  "
              f"{analysis.speedups[i]:>8.2f}x  "
              f"{analysis.efficiencies[i]:>10.2%}")


def demonstrate_theoretical_limits():
    """Demonstrate Amdahl's and Gustafson's laws"""
    print("\n" + "=" * 80)
    print("THEORETICAL SPEEDUP LIMITS")
    print("=" * 80)

    analyzer = PerformanceAnalyzer()

    parallel_fractions = [0.5, 0.75, 0.9, 0.95, 0.99]
    worker_counts = [1, 2, 4, 8, 16, 32]

    # Amdahl's Law
    print("\nAMDAHL'S LAW (Fixed Problem Size)")
    print("-" * 80)
    print(f"{'Parallel %':<12} ", end="")
    for workers in worker_counts:
        print(f"{workers:>8}w ", end="")
    print()
    print("-" * 80)

    for p in parallel_fractions:
        print(f"{p*100:>10.0f}%  ", end="")
        for workers in worker_counts:
            speedup = analyzer.amdahls_law(p, workers)
            print(f"{speedup:>8.2f}x ", end="")
        print()

    # Gustafson's Law
    print("\nGUSTAFSON'S LAW (Scaled Problem Size)")
    print("-" * 80)
    print(f"{'Parallel %':<12} ", end="")
    for workers in worker_counts:
        print(f"{workers:>8}w ", end="")
    print()
    print("-" * 80)

    for p in parallel_fractions:
        print(f"{p*100:>10.0f}%  ", end="")
        for workers in worker_counts:
            speedup = analyzer.gustafson_law(p, workers)
            print(f"{speedup:>8.2f}x ", end="")
        print()


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("COMPREHENSIVE PARALLEL ALGORITHMS BENCHMARK SUITE")
    print("=" * 80)

    analyzer = PerformanceAnalyzer()

    # Demonstrate theoretical limits
    demonstrate_theoretical_limits()

    print("\n" + "=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    print("""
AMDAHL'S LAW (Strong Scaling):
- Fixed problem size
- Maximum speedup limited by serial fraction
- Even 5% serial code limits speedup to 20x
- Diminishing returns with more workers

GUSTAFSON'S LAW (Weak Scaling):
- Scaled problem size (more data per worker)
- Better scalability than Amdahl's law
- Assumes parallel portion can scale
- More realistic for big data applications

PRACTICAL CONSIDERATIONS:
1. Overhead: Thread creation, synchronization, communication
2. Load imbalance: Irregular workloads, dynamic partitioning
3. Memory bandwidth: Cache effects, NUMA effects
4. Contention: Locks, atomic operations, shared resources

OPTIMIZATION STRATEGIES:
1. Minimize serial portions (Amdahl's law)
2. Reduce synchronization overhead
3. Improve load balancing (work stealing)
4. Optimize cache locality (blocking, tiling)
5. Use appropriate granularity (not too fine/coarse)

MEASURING PERFORMANCE:
✓ Speedup: T_sequential / T_parallel
✓ Efficiency: Speedup / NumWorkers
✓ Strong scaling: Fixed size, varying workers
✓ Weak scaling: Proportional size and workers
✓ Profile: Identify bottlenecks

EXPECTED PERFORMANCE:
- Embarrassingly parallel: Near-linear speedup
- Moderate dependencies: 50-80% efficiency
- High dependencies: <50% efficiency
- I/O bound: Limited speedup
- Memory bound: Depends on bandwidth

BEST PRACTICES:
1. Profile before optimizing
2. Measure actual speedup, not assumptions
3. Test with realistic data sizes
4. Consider overhead at small sizes
5. Validate correctness first
6. Compare with sequential baseline
7. Use statistical analysis (multiple runs)
8. Monitor system resources (CPU, memory, I/O)
    """)

    print("\n" + "=" * 80)
    print("BENCHMARKING GUIDELINES")
    print("=" * 80)
    print("""
1. SETUP:
   - Warm up JIT compilers
   - Close unnecessary applications
   - Disable frequency scaling (if possible)
   - Pin threads to cores (for consistency)
   - Use dedicated hardware (for accuracy)

2. METHODOLOGY:
   - Multiple runs (3-10 for statistics)
   - Exclude outliers (>2 standard deviations)
   - Report mean and standard deviation
   - Test multiple input sizes
   - Test multiple thread counts

3. METRICS:
   - Wall-clock time (total elapsed)
   - CPU time (actual CPU usage)
   - Throughput (operations/second)
   - Latency (time per operation)
   - Speedup and efficiency

4. ANALYSIS:
   - Plot scaling curves
   - Identify bottlenecks
   - Compare to theoretical limits
   - Check for regressions
   - Validate correctness

5. REPORTING:
   - Algorithm and implementation
   - Hardware specifications
   - Software versions
   - Input characteristics
   - Statistical measures
   - Visualization (graphs)
    """)

    print("\nBenchmark suite ready for use!")
