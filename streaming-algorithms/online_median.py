"""
Online Median Finding Algorithms

Efficient algorithms for finding the median in streaming data where elements
arrive one at a time and we have limited memory.

Key Algorithms:
- Two Heap Method (exact median)
- Reservoir Sampling Median (approximate)
- P-Square Algorithm (quantile estimation)
- Greenwald-Khanna Algorithm (space-efficient quantiles)
- T-Digest (approximate percentiles)
- Sliding Window Median

Author: Claude
Date: January 2026
"""

import heapq
import numpy as np
from typing import List, Optional, Tuple, Union, Deque
from collections import deque, defaultdict
from dataclasses import dataclass, field
import bisect
import math


class OnlineMedianFinder:
    """
    Exact online median finding using two heaps.

    Maintains the smaller half in a max heap and larger half in a min heap.
    Time: O(log n) per insertion, O(1) for median query
    Space: O(n)
    """

    def __init__(self):
        """Initialize the median finder."""
        self.max_heap = []  # Stores smaller half (negated for max heap)
        self.min_heap = []  # Stores larger half
        self.count = 0

    def add_number(self, num: float) -> None:
        """
        Add a number to the data stream.

        Args:
            num: Number to add
        """
        self.count += 1

        # Add to max heap first (smaller half)
        heapq.heappush(self.max_heap, -num)

        # Balance: move largest from max heap to min heap
        if self.max_heap:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)

        # Ensure max heap has same size or one more element
        if len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)

    def find_median(self) -> Optional[float]:
        """
        Find the median of all numbers seen so far.

        Returns:
            Current median or None if no numbers added
        """
        if self.count == 0:
            return None

        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        else:
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0

    def get_percentile(self, p: float) -> Optional[float]:
        """
        Approximate percentile (only exact for median).

        Args:
            p: Percentile (0-100)

        Returns:
            Approximate percentile value
        """
        if self.count == 0:
            return None

        if p == 50:
            return self.find_median()

        # For other percentiles, we'd need all data
        # This is just an approximation
        if p < 50 and self.max_heap:
            return -self.max_heap[0]
        elif p > 50 and self.min_heap:
            return self.min_heap[0]
        else:
            return self.find_median()


class SlidingWindowMedian:
    """
    Maintains median over a sliding window of fixed size.

    Uses balanced BST approach with sorted list.
    Time: O(log w) per update where w is window size
    Space: O(w)
    """

    def __init__(self, window_size: int):
        """
        Initialize sliding window median finder.

        Args:
            window_size: Size of the sliding window
        """
        self.window_size = window_size
        self.window = deque()
        self.sorted_window = []

    def add_number(self, num: float) -> Optional[float]:
        """
        Add number and return median of current window.

        Args:
            num: Number to add

        Returns:
            Median of current window
        """
        # Add new number
        self.window.append(num)
        bisect.insort(self.sorted_window, num)

        # Remove oldest if window full
        if len(self.window) > self.window_size:
            old = self.window.popleft()
            idx = bisect.bisect_left(self.sorted_window, old)
            self.sorted_window.pop(idx)

        return self.find_median()

    def find_median(self) -> Optional[float]:
        """Get median of current window."""
        if not self.sorted_window:
            return None

        n = len(self.sorted_window)
        if n % 2 == 1:
            return self.sorted_window[n // 2]
        else:
            return (self.sorted_window[n // 2 - 1] +
                   self.sorted_window[n // 2]) / 2.0


@dataclass
class PSquareMarker:
    """Marker for P-Square algorithm."""
    position: int  # Actual position
    desired: float  # Desired position
    value: float  # Marker value


class PSquareQuantile:
    """
    P-Square algorithm for dynamic quantile estimation.

    Maintains 5 markers that track quantiles without storing all data.
    Space: O(1), Time: O(1) per update
    """

    def __init__(self, p: float = 0.5):
        """
        Initialize P-Square for given quantile.

        Args:
            p: Quantile to track (0-1), default 0.5 for median
        """
        self.p = p
        self.markers = []
        self.init_values = []
        self.count = 0

    def add_number(self, num: float) -> None:
        """Add number to the stream."""
        self.count += 1

        if self.count <= 5:
            # Initial phase: collect first 5 values
            self.init_values.append(num)
            if self.count == 5:
                self._initialize_markers()
        else:
            # Update markers
            self._update_markers(num)

    def _initialize_markers(self):
        """Initialize the 5 markers."""
        self.init_values.sort()

        # Set up 5 markers at positions 1, 2, 3, 4, 5
        # with desired positions for quantiles 0, p/2, p, (1+p)/2, 1
        self.markers = [
            PSquareMarker(1, 1, self.init_values[0]),
            PSquareMarker(2, 1 + 2 * self.p, self.init_values[1]),
            PSquareMarker(3, 1 + 4 * self.p, self.init_values[2]),
            PSquareMarker(4, 3 + 2 * self.p, self.init_values[3]),
            PSquareMarker(5, 5, self.init_values[4])
        ]

    def _update_markers(self, num: float):
        """Update markers with new observation."""
        # Find cell k containing num
        k = 0
        for i in range(len(self.markers)):
            if num < self.markers[i].value:
                k = i
                break
        else:
            k = 4

        # Update marker positions
        for i in range(k, 5):
            self.markers[i].position += 1

        # Update desired positions
        self.markers[0].desired = 1
        self.markers[1].desired = 1 + 2 * self.p * self.count / 5
        self.markers[2].desired = 1 + 4 * self.p * self.count / 5
        self.markers[3].desired = 3 + 2 * self.p * self.count / 5
        self.markers[4].desired = self.count

        # Adjust marker values using P-square formula
        for i in range(1, 4):
            d = self.markers[i].desired - self.markers[i].position

            if (d >= 1 and self.markers[i + 1].position - self.markers[i].position > 1) or \
               (d <= -1 and self.markers[i - 1].position - self.markers[i].position < -1):

                d_sign = 1 if d > 0 else -1

                # Parabolic interpolation
                new_value = self._parabolic_interpolation(i, d_sign)

                # Check if interpolation maintains order
                if self.markers[i - 1].value < new_value < self.markers[i + 1].value:
                    self.markers[i].value = new_value
                else:
                    # Linear interpolation fallback
                    self.markers[i].value = self._linear_interpolation(i, d_sign)

                self.markers[i].position += d_sign

    def _parabolic_interpolation(self, i: int, d: int) -> float:
        """Parabolic interpolation for marker adjustment."""
        qi = self.markers[i].value
        qim1 = self.markers[i - 1].value
        qip1 = self.markers[i + 1].value
        ni = self.markers[i].position
        nim1 = self.markers[i - 1].position
        nip1 = self.markers[i + 1].position

        a = d / (nip1 - nim1)
        b = (ni - nim1 + d) * (qip1 - qi) / (nip1 - ni)
        c = (nip1 - ni - d) * (qi - qim1) / (ni - nim1)

        return qi + a * (b + c)

    def _linear_interpolation(self, i: int, d: int) -> float:
        """Linear interpolation for marker adjustment."""
        if d > 0:
            return self.markers[i].value + \
                   (self.markers[i + 1].value - self.markers[i].value) * \
                   (self.markers[i].position + d - self.markers[i].position) / \
                   (self.markers[i + 1].position - self.markers[i].position)
        else:
            return self.markers[i].value + \
                   (self.markers[i - 1].value - self.markers[i].value) * \
                   (self.markers[i].position + d - self.markers[i].position) / \
                   (self.markers[i - 1].position - self.markers[i].position)

    def get_quantile(self) -> Optional[float]:
        """Get the estimated quantile value."""
        if self.count < 5:
            if self.count == 0:
                return None
            # Use exact quantile for small samples
            sorted_vals = sorted(self.init_values)
            idx = int(self.p * (self.count - 1))
            return sorted_vals[idx]

        return self.markers[2].value  # Middle marker tracks p-quantile


class ReservoirMedian:
    """
    Approximate median using reservoir sampling.

    Maintains a fixed-size sample and computes median from it.
    Space: O(k) where k is reservoir size
    """

    def __init__(self, reservoir_size: int = 1000):
        """
        Initialize reservoir median finder.

        Args:
            reservoir_size: Size of the reservoir
        """
        self.reservoir_size = reservoir_size
        self.reservoir = []
        self.count = 0

    def add_number(self, num: float) -> None:
        """Add number to stream."""
        self.count += 1

        if len(self.reservoir) < self.reservoir_size:
            self.reservoir.append(num)
        else:
            # Reservoir sampling
            idx = np.random.randint(0, self.count)
            if idx < self.reservoir_size:
                self.reservoir[idx] = num

    def find_median(self) -> Optional[float]:
        """Find approximate median from reservoir."""
        if not self.reservoir:
            return None

        sorted_reservoir = sorted(self.reservoir)
        n = len(sorted_reservoir)

        if n % 2 == 1:
            return sorted_reservoir[n // 2]
        else:
            return (sorted_reservoir[n // 2 - 1] +
                   sorted_reservoir[n // 2]) / 2.0


class TDigest:
    """
    T-Digest algorithm for approximate percentiles.

    Adaptively maintains centroids with variable precision.
    Better accuracy at extremes (useful for percentiles).
    """

    @dataclass
    class Centroid:
        """Centroid in T-Digest."""
        mean: float
        count: int

        def __lt__(self, other):
            return self.mean < other.mean

    def __init__(self, compression: float = 100):
        """
        Initialize T-Digest.

        Args:
            compression: Compression parameter (higher = better accuracy, more memory)
        """
        self.compression = compression
        self.centroids = []
        self.total_count = 0

    def add(self, value: float, weight: int = 1) -> None:
        """Add value to the digest."""
        new_centroid = self.Centroid(value, weight)
        self.centroids.append(new_centroid)
        self.total_count += weight

        # Compress if too many centroids
        if len(self.centroids) > self.compression * 10:
            self._compress()

    def _compress(self):
        """Compress centroids by merging nearby ones."""
        if not self.centroids:
            return

        self.centroids.sort()

        merged = []
        current = self.centroids[0]

        for centroid in self.centroids[1:]:
            # Calculate scaling function k
            q = current.count / self.total_count
            k = 4 * self.compression * q * (1 - q)

            # Merge if close enough
            if current.count + centroid.count <= k:
                # Merge centroids
                total_count = current.count + centroid.count
                current = self.Centroid(
                    (current.mean * current.count +
                     centroid.mean * centroid.count) / total_count,
                    total_count
                )
            else:
                merged.append(current)
                current = centroid

        merged.append(current)
        self.centroids = merged

    def percentile(self, p: float) -> Optional[float]:
        """
        Get approximate percentile.

        Args:
            p: Percentile (0-100)

        Returns:
            Approximate percentile value
        """
        if not self.centroids:
            return None

        if len(self.centroids) == 1:
            return self.centroids[0].mean

        self.centroids.sort()

        target = p * self.total_count / 100.0
        accumulated = 0

        for i, centroid in enumerate(self.centroids):
            accumulated += centroid.count
            if accumulated >= target:
                if i == 0:
                    return centroid.mean

                # Interpolate between centroids
                prev_centroid = self.centroids[i - 1]
                excess = accumulated - target

                if centroid.count > 0:
                    fraction = 1 - (excess / centroid.count)
                    return prev_centroid.mean + \
                           fraction * (centroid.mean - prev_centroid.mean)
                else:
                    return centroid.mean

        return self.centroids[-1].mean

    def median(self) -> Optional[float]:
        """Get approximate median."""
        return self.percentile(50)


class GreenwaldKhanna:
    """
    Greenwald-Khanna algorithm for space-efficient quantile estimation.

    Provides epsilon-approximate quantiles with O(1/epsilon * log(epsilon*n)) space.
    """

    @dataclass
    class Tuple:
        """Element in GK summary."""
        value: float
        g: int  # Gap (rmin difference)
        delta: int  # Maximum possible error

    def __init__(self, epsilon: float = 0.01):
        """
        Initialize GK quantile estimator.

        Args:
            epsilon: Error bound (0-1)
        """
        self.epsilon = epsilon
        self.summary = []
        self.count = 0

    def add(self, value: float) -> None:
        """Add value to the stream."""
        self.count += 1

        # Find insertion position
        idx = bisect.bisect_left(self.summary, value,
                                 key=lambda t: t.value)

        # Calculate delta for new tuple
        if idx == 0:
            delta = 0
        elif idx == len(self.summary):
            delta = 0
        else:
            delta = int(2 * self.epsilon * self.count)

        # Insert new tuple
        new_tuple = self.Tuple(value, 1, delta)
        self.summary.insert(idx, new_tuple)

        # Compress if needed
        if len(self.summary) > 1 / (2 * self.epsilon):
            self._compress()

    def _compress(self):
        """Compress summary by merging tuples."""
        # Band compression based on GK algorithm
        for band_id in range(int(math.log2(self.count)) + 1):
            band_start = 2 ** band_id - 1
            band_end = 2 ** (band_id + 1) - 1

            threshold = int(2 * self.epsilon * band_end)

            i = 0
            while i < len(self.summary) - 1:
                if self.summary[i].g + self.summary[i + 1].g + \
                   self.summary[i + 1].delta <= threshold:
                    # Merge tuples i and i+1
                    self.summary[i].g += self.summary[i + 1].g
                    self.summary.pop(i + 1)
                else:
                    i += 1

    def quantile(self, phi: float) -> Optional[float]:
        """
        Get approximate quantile.

        Args:
            phi: Quantile (0-1)

        Returns:
            Approximate quantile value
        """
        if not self.summary:
            return None

        rank = int(phi * self.count)
        error = int(self.epsilon * self.count)

        rmin = 0
        for i, t in enumerate(self.summary):
            rmin += t.g
            rmax = rmin + t.delta

            if rank <= rmin + error:
                return t.value

        return self.summary[-1].value


# Example usage and demonstrations
def example_exact_median():
    """Demonstrate exact online median finding."""
    print("=== Exact Online Median (Two Heaps) ===\n")

    finder = OnlineMedianFinder()
    stream = [5, 15, 1, 3, 8, 7, 9, 10, 20, 12]

    print("Adding numbers to stream:")
    for num in stream:
        finder.add_number(num)
        print(f"  Added {num:2d}, median = {finder.find_median():.1f}")

    print(f"\nFinal median: {finder.find_median()}")


def example_sliding_window():
    """Demonstrate sliding window median."""
    print("=== Sliding Window Median ===\n")

    window_size = 5
    finder = SlidingWindowMedian(window_size)
    stream = list(range(1, 11))

    print(f"Window size: {window_size}")
    print("Stream and window medians:")

    for num in stream:
        median = finder.add_number(num)
        window_content = list(finder.window)
        print(f"  Added {num:2d}, window {window_content}, median = {median:.1f}")


def example_p_square():
    """Demonstrate P-Square algorithm for quantile estimation."""
    print("=== P-Square Quantile Estimation ===\n")

    # Track median (0.5 quantile) and 0.9 quantile
    median_tracker = PSquareQuantile(0.5)
    p90_tracker = PSquareQuantile(0.9)

    # Generate stream from normal distribution
    np.random.seed(42)
    stream_size = 10000
    stream = np.random.normal(100, 15, stream_size)

    for value in stream:
        median_tracker.add_number(value)
        p90_tracker.add_number(value)

    estimated_median = median_tracker.get_quantile()
    estimated_p90 = p90_tracker.get_quantile()

    # Compare with exact values
    exact_median = np.median(stream)
    exact_p90 = np.percentile(stream, 90)

    print(f"Stream size: {stream_size}")
    print(f"\nMedian estimation:")
    print(f"  P-Square estimate: {estimated_median:.2f}")
    print(f"  Exact median: {exact_median:.2f}")
    print(f"  Error: {abs(estimated_median - exact_median):.2f}")

    print(f"\n90th percentile estimation:")
    print(f"  P-Square estimate: {estimated_p90:.2f}")
    print(f"  Exact p90: {exact_p90:.2f}")
    print(f"  Error: {abs(estimated_p90 - exact_p90):.2f}")


def example_t_digest():
    """Demonstrate T-Digest for percentile estimation."""
    print("=== T-Digest Percentile Estimation ===\n")

    digest = TDigest(compression=100)

    # Add data from mixed distribution
    np.random.seed(42)

    # Normal data
    for _ in range(5000):
        digest.add(np.random.normal(50, 10))

    # Some outliers
    for _ in range(100):
        digest.add(np.random.uniform(100, 200))

    # Get various percentiles
    percentiles = [1, 5, 25, 50, 75, 95, 99]

    print("Percentile estimates:")
    for p in percentiles:
        value = digest.percentile(p)
        print(f"  P{p:2d}: {value:.2f}")

    print(f"\nMedian: {digest.median():.2f}")
    print(f"Total points: {digest.total_count}")
    print(f"Centroids used: {len(digest.centroids)}")


def example_comparison():
    """Compare different online median algorithms."""
    print("=== Algorithm Comparison ===\n")

    # Initialize algorithms
    exact = OnlineMedianFinder()
    reservoir = ReservoirMedian(reservoir_size=100)
    p_square = PSquareQuantile(0.5)
    t_digest = TDigest(compression=50)

    # Generate large stream
    np.random.seed(42)
    stream_size = 10000
    stream = np.random.exponential(scale=10, size=stream_size)

    # Process stream
    print(f"Processing {stream_size} values from exponential distribution...")

    for value in stream:
        exact.add_number(value)
        reservoir.add_number(value)
        p_square.add_number(value)
        t_digest.add(value)

    # Get results
    exact_median = exact.find_median()
    reservoir_median = reservoir.find_median()
    p_square_median = p_square.get_quantile()
    t_digest_median = t_digest.median()
    true_median = np.median(stream)

    # Compare results
    print("\nMedian estimates:")
    print(f"  True median:      {true_median:.3f}")
    print(f"  Exact (2-heap):   {exact_median:.3f} (error: {abs(exact_median - true_median):.3f})")
    print(f"  Reservoir (100):  {reservoir_median:.3f} (error: {abs(reservoir_median - true_median):.3f})")
    print(f"  P-Square:         {p_square_median:.3f} (error: {abs(p_square_median - true_median):.3f})")
    print(f"  T-Digest:         {t_digest_median:.3f} (error: {abs(t_digest_median - true_median):.3f})")

    print("\nSpace complexity:")
    print(f"  Exact: O(n) - stores all {stream_size} values in heaps")
    print(f"  Reservoir: O(k) - stores {len(reservoir.reservoir)} values")
    print(f"  P-Square: O(1) - stores 5 markers")
    print(f"  T-Digest: O(compression) - stores {len(t_digest.centroids)} centroids")


def example_streaming_statistics():
    """Demonstrate streaming median in data analysis context."""
    print("=== Streaming Statistics Application ===\n")

    # Simulate network latency monitoring
    print("Network Latency Monitoring Simulation")
    print("-" * 40)

    median_finder = OnlineMedianFinder()
    p50 = PSquareQuantile(0.50)
    p95 = PSquareQuantile(0.95)
    p99 = PSquareQuantile(0.99)

    # Simulate latency stream with occasional spikes
    np.random.seed(42)

    for minute in range(60):
        # Normal latency with occasional spikes
        if minute % 15 == 0 and minute > 0:
            # Spike
            latencies = np.random.normal(200, 50, 100)
        else:
            # Normal
            latencies = np.random.normal(20, 5, 100)

        for latency in latencies:
            latency = max(1, latency)  # Ensure positive
            median_finder.add_number(latency)
            p50.add_number(latency)
            p95.add_number(latency)
            p99.add_number(latency)

        if minute % 10 == 9:
            print(f"\nMinute {minute + 1} stats:")
            print(f"  Median (P50): {p50.get_quantile():.1f} ms")
            print(f"  P95: {p95.get_quantile():.1f} ms")
            print(f"  P99: {p99.get_quantile():.1f} ms")

    print("\n" + "=" * 40)
    print("Final statistics after 60 minutes:")
    print(f"  Total requests: {median_finder.count}")
    print(f"  Median latency: {median_finder.find_median():.1f} ms")
    print(f"  P95 latency: {p95.get_quantile():.1f} ms")
    print(f"  P99 latency: {p99.get_quantile():.1f} ms")


if __name__ == "__main__":
    # Run examples
    example_exact_median()
    print("\n" + "=" * 60 + "\n")

    example_sliding_window()
    print("\n" + "=" * 60 + "\n")

    example_p_square()
    print("\n" + "=" * 60 + "\n")

    example_t_digest()
    print("\n" + "=" * 60 + "\n")

    example_comparison()
    print("\n" + "=" * 60 + "\n")

    example_streaming_statistics()

    print("\n" + "=" * 60)
    print("Key Insights:")
    print("=" * 60)
    print("""
1. Two-heap method provides exact median but requires O(n) space,
   making it unsuitable for infinite streams.

2. P-Square algorithm uses only O(1) space (5 markers) and provides
   good approximations for any quantile, not just median.

3. T-Digest adaptively maintains precision, providing better accuracy
   at the extremes (useful for P99 latency monitoring).

4. Reservoir sampling gives unbiased samples but accuracy depends on
   reservoir size vs. stream size.

5. For sliding windows, maintaining sorted order allows O(log w)
   updates where w is window size.

6. Choice of algorithm depends on:
   - Exactness requirements
   - Memory constraints
   - Need for multiple quantiles
   - Stream characteristics (bounded vs unbounded)

7. In production systems, approximate algorithms like P-Square and
   T-Digest are preferred for their bounded memory usage.
    """)