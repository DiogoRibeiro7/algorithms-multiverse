"""
Online Statistics and Quantile Estimation Algorithms
====================================================

Implementations of streaming algorithms for computing statistics
(median, quantiles, mean, variance) on data streams with limited memory.

Includes:
- Online Median (Two Heaps)
- Running Median with Sliding Window
- Greenwald-Khanna Quantiles
- T-Digest for Quantile Estimation
- P-Square Algorithm for Quantiles
- Online Mean and Variance (Welford's Algorithm)
- Exponentially Weighted Statistics

Author: Claude
Date: January 2026
"""

import heapq
import bisect
import numpy as np
from typing import List, Optional, Tuple, Deque
from dataclasses import dataclass, field
from collections import deque
import math


class OnlineMedian:
    """
    Online Median Finder using Two Heaps.

    Maintains median of a stream using a max heap (for smaller half)
    and a min heap (for larger half).

    Time complexity: O(log n) per insertion, O(1) for median query
    Space complexity: O(n)
    """

    def __init__(self):
        """Initialize the median finder."""
        self.max_heap = []  # Smaller half (negated for max heap)
        self.min_heap = []  # Larger half

    def add(self, num: float):
        """
        Add a number to the stream.

        Args:
            num: Number to add
        """
        # Add to max heap first
        heapq.heappush(self.max_heap, -num)

        # Move largest from max heap to min heap
        max_top = -heapq.heappop(self.max_heap)
        heapq.heappush(self.min_heap, max_top)

        # Balance heaps (max heap can have at most 1 more element)
        if len(self.min_heap) > len(self.max_heap):
            min_top = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -min_top)

    def get_median(self) -> Optional[float]:
        """
        Get the current median.

        Returns:
            Current median or None if no elements
        """
        if not self.max_heap and not self.min_heap:
            return None

        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        else:
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0

    def size(self) -> int:
        """Get total number of elements."""
        return len(self.max_heap) + len(self.min_heap)


class SlidingWindowMedian:
    """
    Sliding Window Median using Balanced BST approach.

    Maintains median of last k elements in a stream.
    Uses two multisets (implemented with sorted lists) for simplicity.
    """

    def __init__(self, k: int):
        """
        Initialize sliding window median.

        Args:
            k: Window size
        """
        self.k = k
        self.window = deque(maxlen=k)
        self.sorted_window = []

    def add(self, num: float) -> Optional[float]:
        """
        Add number and return median of current window.

        Args:
            num: Number to add

        Returns:
            Median of current window
        """
        # Remove oldest if window is full
        if len(self.window) == self.k:
            old = self.window[0]
            idx = bisect.bisect_left(self.sorted_window, old)
            self.sorted_window.pop(idx)

        # Add new number
        self.window.append(num)
        bisect.insort(self.sorted_window, num)

        # Calculate median
        n = len(self.sorted_window)
        if n == 0:
            return None
        elif n % 2 == 1:
            return self.sorted_window[n // 2]
        else:
            return (self.sorted_window[n // 2 - 1] + self.sorted_window[n // 2]) / 2.0


@dataclass
class GKTuple:
    """Tuple for Greenwald-Khanna algorithm."""
    value: float
    gap: int
    delta: int


class GreenwaldKhannaQuantiles:
    """
    Greenwald-Khanna Algorithm for Quantile Estimation.

    Space-efficient algorithm for computing approximate quantiles
    with guaranteed error bounds.

    Error bound: epsilon * n
    Space complexity: O(1/epsilon * log(epsilon * n))
    """

    def __init__(self, epsilon: float = 0.01):
        """
        Initialize GK quantile estimator.

        Args:
            epsilon: Error bound (0 < epsilon < 1)
        """
        self.epsilon = epsilon
        self.summary = []  # List of GKTuples
        self.n = 0
        self.compress_threshold = int(1.0 / (2.0 * epsilon))

    def add(self, value: float):
        """Add value to stream."""
        self.n += 1

        # Find insertion position
        idx = bisect.bisect_left(self.summary, value, key=lambda x: x.value)

        # Calculate delta
        if idx == 0:
            delta = 0
        elif idx == len(self.summary):
            delta = 0
        else:
            delta = int(2 * self.epsilon * self.n)

        # Insert new tuple
        self.summary.insert(idx, GKTuple(value, 1, delta))

        # Compress if needed
        if self.n % self.compress_threshold == 0:
            self._compress()

    def _compress(self):
        """Compress summary by merging tuples."""
        if len(self.summary) <= 2:
            return

        new_summary = [self.summary[0]]  # Keep minimum

        for i in range(1, len(self.summary) - 1):
            current = self.summary[i]
            prev = new_summary[-1]

            # Check if we can merge
            if prev.gap + current.gap + current.delta <= int(2 * self.epsilon * self.n):
                # Merge by increasing gap of previous
                prev.gap += current.gap
            else:
                new_summary.append(current)

        new_summary.append(self.summary[-1])  # Keep maximum
        self.summary = new_summary

    def get_quantile(self, phi: float) -> Optional[float]:
        """
        Get approximate quantile.

        Args:
            phi: Quantile to compute (0 < phi < 1)

        Returns:
            Approximate quantile value
        """
        if not self.summary or not 0 <= phi <= 1:
            return None

        target_rank = int(phi * self.n)
        rank = 0

        for i, tuple_i in enumerate(self.summary):
            rank += tuple_i.gap

            if rank + tuple_i.gap > target_rank:
                return tuple_i.value

        return self.summary[-1].value if self.summary else None

    def get_rank(self, value: float) -> int:
        """Get approximate rank of a value."""
        rank = 0

        for tuple_i in self.summary:
            if tuple_i.value >= value:
                return rank
            rank += tuple_i.gap

        return self.n


@dataclass
class Centroid:
    """Centroid for T-Digest algorithm."""
    mean: float
    count: int


class TDigest:
    """
    T-Digest Algorithm for Quantile Estimation.

    Provides accurate quantile estimates especially for extreme quantiles
    (e.g., 99th, 99.9th percentile).

    Uses adaptive clustering with more clusters at the tails.
    """

    def __init__(self, delta: float = 100):
        """
        Initialize T-Digest.

        Args:
            delta: Compression parameter (higher = more accuracy, more memory)
        """
        self.delta = delta
        self.centroids = []
        self.n = 0

    def add(self, value: float, weight: int = 1):
        """
        Add value to digest.

        Args:
            value: Value to add
            weight: Weight/count of the value
        """
        # Add as new centroid
        new_centroid = Centroid(value, weight)
        self.centroids.append(new_centroid)
        self.n += weight

        # Compress if needed
        if len(self.centroids) > 20 * self.delta:
            self._compress()

    def _compress(self):
        """Compress centroids."""
        if not self.centroids:
            return

        # Sort centroids
        self.centroids.sort(key=lambda c: c.mean)

        # Merge adjacent centroids based on scale function
        merged = []
        current = self.centroids[0]
        cumulative_count = current.count

        for i in range(1, len(self.centroids)):
            next_centroid = self.centroids[i]

            # Calculate scale limit based on quantile
            q = cumulative_count / self.n
            scale_limit = self.delta * self._scale_function(q)

            if current.count + next_centroid.count <= scale_limit:
                # Merge centroids
                total_count = current.count + next_centroid.count
                current = Centroid(
                    mean=(current.mean * current.count + next_centroid.mean * next_centroid.count) / total_count,
                    count=total_count
                )
            else:
                merged.append(current)
                current = next_centroid

            cumulative_count += next_centroid.count

        merged.append(current)
        self.centroids = merged

    def _scale_function(self, q: float) -> float:
        """
        Scale function that determines cluster size.

        More clusters at the extremes (q near 0 or 1).
        """
        return 4 * self.n * q * (1 - q)

    def get_quantile(self, q: float) -> Optional[float]:
        """
        Get quantile estimate.

        Args:
            q: Quantile (0 <= q <= 1)

        Returns:
            Estimated quantile value
        """
        if not self.centroids or not 0 <= q <= 1:
            return None

        # Sort centroids
        sorted_centroids = sorted(self.centroids, key=lambda c: c.mean)

        # Find target rank
        target = q * self.n

        # Interpolate between centroids
        cumulative = 0
        prev_mean = sorted_centroids[0].mean
        prev_cumulative = 0

        for centroid in sorted_centroids:
            cumulative += centroid.count / 2.0  # Use centroid midpoint

            if cumulative >= target:
                # Interpolate
                if centroid.count > 0:
                    fraction = (target - prev_cumulative) / (cumulative - prev_cumulative)
                    return prev_mean + fraction * (centroid.mean - prev_mean)
                return centroid.mean

            prev_mean = centroid.mean
            prev_cumulative = cumulative
            cumulative += centroid.count / 2.0

        return sorted_centroids[-1].mean


class PSquareQuantile:
    """
    P-Square Algorithm for Dynamic Quantile Estimation.

    Maintains 5 markers to estimate a single quantile without storing data.
    Very memory efficient (O(1) space).
    """

    def __init__(self, p: float = 0.5):
        """
        Initialize P-Square for estimating p-th quantile.

        Args:
            p: Quantile to estimate (0 < p < 1)
        """
        self.p = p
        self.n = 0

        # Five markers
        self.positions = [1, 2, 3, 4, 5]  # Positions (ranks)
        self.heights = []  # Heights (values)
        self.desired_positions = [1, 1 + 2*p, 1 + 4*p, 3 + 2*p, 5]

        # Initialize with first 5 values
        self.initial_values = []

    def add(self, value: float):
        """Add value to stream."""
        self.n += 1

        if self.n <= 5:
            # Collect first 5 values
            self.initial_values.append(value)

            if self.n == 5:
                # Initialize markers
                self.heights = sorted(self.initial_values)
                self.positions = list(range(1, 6))
        else:
            # Update markers
            self._update_markers(value)

    def _update_markers(self, value: float):
        """Update marker positions and heights."""
        # Find cell k containing value
        k = 0
        for i in range(1, 5):
            if value < self.heights[i]:
                k = i - 1
                break
        else:
            k = 3

        # Increment positions of markers k+1 to 4
        for i in range(k + 1, 5):
            self.positions[i] += 1

        # Update desired positions
        for i in range(1, 4):
            self.desired_positions[i] += self._desired_increment(i)

        # Adjust heights of markers 1-3 if necessary
        for i in range(1, 4):
            delta = self.desired_positions[i] - self.positions[i]

            if (delta >= 1 and self.positions[i+1] - self.positions[i] > 1) or \
               (delta <= -1 and self.positions[i] - self.positions[i-1] > 1):
                # Use parabolic prediction
                d = 1 if delta > 0 else -1
                new_height = self._parabolic_predict(i, d)

                if self.heights[i-1] < new_height < self.heights[i+1]:
                    self.heights[i] = new_height
                else:
                    # Use linear prediction
                    self.heights[i] = self._linear_predict(i, d)

                self.positions[i] += d

    def _desired_increment(self, i: int) -> float:
        """Calculate desired position increment."""
        if i == 1:
            return self.p / 2
        elif i == 2:
            return self.p
        else:  # i == 3
            return (1 + self.p) / 2

    def _parabolic_predict(self, i: int, d: int) -> float:
        """Parabolic prediction for new height."""
        qi = self.heights[i]
        qim1 = self.heights[i-1]
        qip1 = self.heights[i+1]

        ni = self.positions[i]
        nim1 = self.positions[i-1]
        nip1 = self.positions[i+1]

        a = (ni - nim1 + d) * (qip1 - qi) / (nip1 - ni)
        b = (nip1 - ni - d) * (qi - qim1) / (ni - nim1)

        return qi + (d / (nip1 - nim1)) * (a + b)

    def _linear_predict(self, i: int, d: int) -> float:
        """Linear prediction for new height."""
        if d == 1:
            return self.heights[i] + (self.heights[i+1] - self.heights[i]) / (self.positions[i+1] - self.positions[i])
        else:
            return self.heights[i] - (self.heights[i] - self.heights[i-1]) / (self.positions[i] - self.positions[i-1])

    def get_quantile(self) -> Optional[float]:
        """Get current quantile estimate."""
        if self.n < 5:
            if not self.initial_values:
                return None
            sorted_vals = sorted(self.initial_values)
            idx = int(self.p * len(sorted_vals))
            return sorted_vals[min(idx, len(sorted_vals) - 1)]

        return self.heights[2]  # Middle marker estimates the quantile


class WelfordVariance:
    """
    Welford's Algorithm for Online Mean and Variance.

    Numerically stable single-pass algorithm for computing
    mean and variance of a stream.

    Space complexity: O(1)
    """

    def __init__(self):
        """Initialize Welford's algorithm."""
        self.n = 0
        self.mean = 0.0
        self.M2 = 0.0  # Sum of squared differences from mean

    def add(self, value: float):
        """Add value to stream."""
        self.n += 1
        delta = value - self.mean
        self.mean += delta / self.n
        delta2 = value - self.mean
        self.M2 += delta * delta2

    def get_mean(self) -> Optional[float]:
        """Get current mean."""
        return self.mean if self.n > 0 else None

    def get_variance(self) -> Optional[float]:
        """Get current variance."""
        if self.n < 2:
            return None
        return self.M2 / self.n  # Population variance

    def get_sample_variance(self) -> Optional[float]:
        """Get sample variance."""
        if self.n < 2:
            return None
        return self.M2 / (self.n - 1)

    def get_stddev(self) -> Optional[float]:
        """Get standard deviation."""
        var = self.get_variance()
        return math.sqrt(var) if var is not None else None

    def merge(self, other: 'WelfordVariance'):
        """Merge with another Welford instance."""
        if other.n == 0:
            return

        delta = other.mean - self.mean
        combined_n = self.n + other.n

        self.M2 = self.M2 + other.M2 + delta ** 2 * self.n * other.n / combined_n
        self.mean = (self.n * self.mean + other.n * other.mean) / combined_n
        self.n = combined_n


class ExponentiallyWeightedStats:
    """
    Exponentially Weighted Moving Average and Variance.

    Gives more weight to recent observations.
    Useful for time series with concept drift.
    """

    def __init__(self, alpha: float = 0.1):
        """
        Initialize EWMA.

        Args:
            alpha: Smoothing factor (0 < alpha <= 1)
                   Higher alpha = more weight on recent values
        """
        self.alpha = alpha
        self.mean = None
        self.variance = None
        self.n = 0

    def add(self, value: float):
        """Add value with exponential weighting."""
        self.n += 1

        if self.mean is None:
            self.mean = value
            self.variance = 0
        else:
            # Update mean
            delta = value - self.mean
            self.mean += self.alpha * delta

            # Update variance (EWMA of squared deviations)
            self.variance = (1 - self.alpha) * (self.variance + self.alpha * delta ** 2)

    def get_mean(self) -> Optional[float]:
        """Get exponentially weighted mean."""
        return self.mean

    def get_variance(self) -> Optional[float]:
        """Get exponentially weighted variance."""
        return self.variance

    def get_stddev(self) -> Optional[float]:
        """Get exponentially weighted standard deviation."""
        return math.sqrt(self.variance) if self.variance is not None else None


class OnlinePercentiles:
    """
    Complete online percentile tracker using multiple algorithms.

    Combines different approaches for comprehensive percentile tracking.
    """

    def __init__(self, percentiles: List[float] = None):
        """
        Initialize percentile tracker.

        Args:
            percentiles: List of percentiles to track (default: quartiles)
        """
        if percentiles is None:
            percentiles = [0.25, 0.5, 0.75, 0.90, 0.95, 0.99]

        self.percentiles = percentiles
        self.t_digest = TDigest(delta=100)
        self.gk = GreenwaldKhannaQuantiles(epsilon=0.01)
        self.median_finder = OnlineMedian()
        self.stats = WelfordVariance()
        self.n = 0

    def add(self, value: float):
        """Add value to all trackers."""
        self.n += 1
        self.t_digest.add(value)
        self.gk.add(value)
        self.median_finder.add(value)
        self.stats.add(value)

    def get_summary(self) -> dict:
        """Get complete statistical summary."""
        summary = {
            'count': self.n,
            'mean': self.stats.get_mean(),
            'stddev': self.stats.get_stddev(),
            'median': self.median_finder.get_median()
        }

        # Add percentiles from T-Digest
        for p in self.percentiles:
            summary[f'p{int(p*100)}'] = self.t_digest.get_quantile(p)

        return summary


def example_usage():
    """Demonstrate online statistics algorithms."""
    print("=" * 60)
    print("ONLINE STATISTICS AND QUANTILE ALGORITHMS")
    print("=" * 60)

    # Generate test stream
    np.random.seed(42)
    stream = np.concatenate([
        np.random.normal(0, 1, 1000),  # Normal distribution
        np.random.exponential(2, 500)  # Exponential tail
    ])
    np.random.shuffle(stream)

    # Example 1: Online Median
    print("\n1. Online Median Finder:")
    print("-" * 40)

    median_finder = OnlineMedian()
    for i, val in enumerate(stream[:100]):
        median_finder.add(val)

        if i % 20 == 19:
            print(f"  After {i+1} values: Median = {median_finder.get_median():.4f}")

    # Example 2: Sliding Window Median
    print("\n2. Sliding Window Median:")
    print("-" * 40)

    window_median = SlidingWindowMedian(k=50)
    medians = []

    for val in stream[:200]:
        med = window_median.add(val)
        if med is not None:
            medians.append(med)

    print(f"  Window size: 50")
    print(f"  Median range: [{min(medians):.4f}, {max(medians):.4f}]")
    print(f"  Final window median: {medians[-1]:.4f}")

    # Example 3: Greenwald-Khanna Quantiles
    print("\n3. Greenwald-Khanna Quantile Estimation:")
    print("-" * 40)

    gk = GreenwaldKhannaQuantiles(epsilon=0.01)
    for val in stream:
        gk.add(val)

    quantiles = [0.25, 0.5, 0.75, 0.90, 0.95, 0.99]
    print("  Approximate quantiles:")
    for q in quantiles:
        estimate = gk.get_quantile(q)
        actual = np.quantile(stream, q)
        error = abs(estimate - actual) / abs(actual) * 100 if actual != 0 else 0
        print(f"    {q:.2f}: Estimate = {estimate:.4f}, Actual = {actual:.4f}, Error = {error:.2f}%")

    # Example 4: T-Digest
    print("\n4. T-Digest Quantile Estimation:")
    print("-" * 40)

    tdigest = TDigest(delta=100)
    for val in stream:
        tdigest.add(val)

    print("  T-Digest quantiles (excellent for extremes):")
    for q in [0.5, 0.90, 0.95, 0.99, 0.999]:
        estimate = tdigest.get_quantile(q)
        actual = np.quantile(stream, q)
        error = abs(estimate - actual) / abs(actual) * 100 if actual != 0 else 0
        print(f"    {q:.3f}: Estimate = {estimate:.4f}, Actual = {actual:.4f}, Error = {error:.2f}%")

    # Example 5: P-Square for single quantile
    print("\n5. P-Square Algorithm (Single Quantile):")
    print("-" * 40)

    psquare_median = PSquareQuantile(p=0.5)
    psquare_90 = PSquareQuantile(p=0.90)

    for val in stream:
        psquare_median.add(val)
        psquare_90.add(val)

    print(f"  Median estimate: {psquare_median.get_quantile():.4f}")
    print(f"  Actual median: {np.median(stream):.4f}")
    print(f"  90th percentile estimate: {psquare_90.get_quantile():.4f}")
    print(f"  Actual 90th percentile: {np.quantile(stream, 0.90):.4f}")

    # Example 6: Welford's Algorithm
    print("\n6. Welford's Online Mean and Variance:")
    print("-" * 40)

    welford = WelfordVariance()
    for val in stream:
        welford.add(val)

    print(f"  Mean: {welford.get_mean():.4f} (actual: {np.mean(stream):.4f})")
    print(f"  Std Dev: {welford.get_stddev():.4f} (actual: {np.std(stream):.4f})")
    print(f"  Variance: {welford.get_variance():.4f} (actual: {np.var(stream):.4f})")

    # Example 7: Exponentially Weighted Stats
    print("\n7. Exponentially Weighted Statistics:")
    print("-" * 40)

    # Simulate concept drift
    drift_stream = np.concatenate([
        np.random.normal(0, 1, 500),  # Initial distribution
        np.random.normal(2, 1, 500)   # Shifted distribution
    ])

    ewma = ExponentiallyWeightedStats(alpha=0.1)
    batch_means = []

    for i, val in enumerate(drift_stream):
        ewma.add(val)

        if i % 100 == 99:
            batch_mean = np.mean(drift_stream[max(0, i-99):i+1])
            batch_means.append(batch_mean)
            print(f"  After {i+1} values: EWMA mean = {ewma.get_mean():.4f}, "
                  f"Batch mean = {batch_mean:.4f}")

    # Example 8: Complete Percentile Tracking
    print("\n8. Complete Online Statistics Summary:")
    print("-" * 40)

    tracker = OnlinePercentiles()
    for val in stream:
        tracker.add(val)

    summary = tracker.get_summary()
    print("  Statistical Summary:")
    for key, value in summary.items():
        if value is not None:
            print(f"    {key}: {value:.4f}")

    # Example 9: Performance Comparison
    print("\n9. Memory and Speed Comparison:")
    print("-" * 40)

    import time
    import sys

    test_size = 100000
    test_stream = np.random.normal(0, 1, test_size)

    # Memory comparison (approximate)
    algorithms = [
        ("Online Median (2 heaps)", OnlineMedian()),
        ("GK Quantiles", GreenwaldKhannaQuantiles(0.01)),
        ("T-Digest", TDigest(100)),
        ("P-Square (single)", PSquareQuantile(0.5)),
        ("Welford", WelfordVariance())
    ]

    print(f"  Stream size: {test_size:,}")
    print("  Algorithm performance:")

    for name, algo in algorithms:
        start = time.time()

        for val in test_stream:
            if hasattr(algo, 'add'):
                algo.add(val)

        elapsed = time.time() - start
        print(f"    {name:25s}: {elapsed*1000:.2f} ms")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Two-heap median: Exact but O(n) memory")
    print("- GK/T-Digest: Approximate but O(log n) memory")
    print("- P-Square: O(1) memory for single quantile")
    print("- Welford: Numerically stable variance computation")
    print("- EWMA: Adapts to changing distributions")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()