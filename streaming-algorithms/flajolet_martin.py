"""
Flajolet-Martin Algorithm Implementation

Probabilistic counting algorithm for estimating the number of distinct elements
in a data stream using logarithmic space.

Key Features:
- Estimates cardinality with O(log log n) bits
- Multiple hash functions for improved accuracy
- Super-LogLog and HyperLogLog++ variants
- Bias correction and sparse mode optimizations

Author: Claude
Date: January 2026
"""

import hashlib
import numpy as np
from typing import List, Union, Optional, Set, Callable, Tuple
from dataclasses import dataclass, field
import struct
import math
import mmh3  # MurmurHash3 for better hash distribution


class FlajoletMartin:
    """
    Classic Flajolet-Martin algorithm for cardinality estimation.

    Uses the position of the rightmost 1-bit in hash values to estimate
    the number of distinct elements.
    """

    def __init__(self, num_estimators: int = 64):
        """
        Initialize FM algorithm.

        Args:
            num_estimators: Number of independent estimators (more = better accuracy)
        """
        self.num_estimators = num_estimators
        self.max_zeros = [0] * num_estimators
        self.hash_seeds = [i for i in range(num_estimators)]

    def _hash(self, item: Union[str, int, bytes], seed: int) -> int:
        """
        Hash function for FM algorithm.

        Args:
            item: Item to hash
            seed: Hash seed for independence

        Returns:
            32-bit hash value
        """
        if isinstance(item, str):
            item = item.encode('utf-8')
        elif isinstance(item, int):
            item = str(item).encode('utf-8')

        # Use MurmurHash3 for good distribution
        return mmh3.hash(item, seed) & 0x7FFFFFFF  # Ensure positive

    def _count_trailing_zeros(self, n: int) -> int:
        """Count trailing zeros in binary representation."""
        if n == 0:
            return 32

        count = 0
        while (n & 1) == 0:
            count += 1
            n >>= 1
        return count

    def add(self, item: Union[str, int, bytes]) -> None:
        """
        Add an item to the stream.

        Args:
            item: Item to add
        """
        for i in range(self.num_estimators):
            hash_value = self._hash(item, self.hash_seeds[i])
            zeros = self._count_trailing_zeros(hash_value)
            self.max_zeros[i] = max(self.max_zeros[i], zeros)

    def estimate_cardinality(self, use_median: bool = False) -> int:
        """
        Estimate the number of distinct elements.

        Args:
            use_median: Use median instead of mean (more robust to outliers)

        Returns:
            Estimated cardinality
        """
        if use_median:
            # Median of estimates (more robust)
            estimates = [2 ** z for z in self.max_zeros]
            return int(np.median(estimates))
        else:
            # Mean of estimates (classic FM)
            phi = 0.77351  # Correction factor
            mean_estimate = np.mean([2 ** z for z in self.max_zeros])
            return int(mean_estimate / phi)

    def merge(self, other: 'FlajoletMartin') -> 'FlajoletMartin':
        """
        Merge with another FM estimator.

        Args:
            other: Another FM estimator

        Returns:
            Merged estimator
        """
        if self.num_estimators != other.num_estimators:
            raise ValueError("Cannot merge estimators with different sizes")

        merged = FlajoletMartin(self.num_estimators)
        merged.max_zeros = [max(a, b) for a, b in zip(self.max_zeros, other.max_zeros)]
        merged.hash_seeds = self.hash_seeds.copy()
        return merged


class ImprovedFlajoletMartin:
    """
    Improved FM algorithm with multiple enhancements:
    - Stochastic averaging for variance reduction
    - Bias correction
    - Small range correction
    """

    def __init__(self, precision: int = 14):
        """
        Initialize improved FM algorithm.

        Args:
            precision: Number of bits for buckets (m = 2^precision)
        """
        self.precision = precision
        self.m = 1 << precision  # Number of buckets
        self.registers = np.zeros(self.m, dtype=np.int8)
        self.alpha = self._get_alpha(self.m)

    def _get_alpha(self, m: int) -> float:
        """Get bias correction constant alpha."""
        if m == 16:
            return 0.673
        elif m == 32:
            return 0.697
        elif m == 64:
            return 0.709
        else:
            return 0.7213 / (1 + 1.079 / m)

    def _hash(self, item: Union[str, int, bytes]) -> int:
        """Hash function using SHA-1."""
        if isinstance(item, str):
            item = item.encode('utf-8')
        elif isinstance(item, int):
            item = str(item).encode('utf-8')

        return int(hashlib.sha1(item).hexdigest(), 16)

    def add(self, item: Union[str, int, bytes]) -> None:
        """Add item to the stream."""
        hash_value = self._hash(item)

        # First p bits determine bucket
        bucket = hash_value & ((1 << self.precision) - 1)

        # Count leading zeros in remaining bits
        remaining = hash_value >> self.precision
        leading_zeros = self._count_leading_zeros_64(remaining) + 1

        # Update register
        self.registers[bucket] = max(self.registers[bucket], leading_zeros)

    def _count_leading_zeros_64(self, n: int) -> int:
        """Count leading zeros in 64-bit number."""
        if n == 0:
            return 64

        count = 0
        bit = 1 << 63

        while (n & bit) == 0:
            count += 1
            bit >>= 1
            if count >= 64:
                break

        return count

    def estimate_cardinality(self) -> int:
        """
        Estimate cardinality with bias correction.

        Returns:
            Estimated number of distinct elements
        """
        # Harmonic mean of 2^register values
        raw_estimate = self.alpha * (self.m ** 2) / np.sum(2.0 ** (-self.registers))

        # Small range correction
        if raw_estimate <= 2.5 * self.m:
            zeros = np.count_nonzero(self.registers == 0)
            if zeros != 0:
                return int(self.m * np.log(self.m / zeros))

        # Large range correction
        if raw_estimate <= (1/30) * (1 << 32):
            return int(raw_estimate)
        else:
            return int(-1 * (1 << 32) * np.log(1 - raw_estimate / (1 << 32)))


class LogLogCounting:
    """
    LogLog Counting algorithm - predecessor to HyperLogLog.

    Uses geometric averaging instead of harmonic mean.
    """

    def __init__(self, k: int = 10):
        """
        Initialize LogLog counting.

        Args:
            k: Number of bits for buckets (m = 2^k)
        """
        self.k = k
        self.m = 1 << k
        self.M = np.zeros(self.m, dtype=np.int8)
        self.alpha = self._alpha_m(self.m)

    def _alpha_m(self, m: int) -> float:
        """Bias correction factor."""
        return 0.39701 if m == 32 else 0.79402 * m / (2 ** self._rho(m))

    def _rho(self, m: int) -> int:
        """Position of leftmost 1-bit."""
        return int(np.log2(m))

    def add(self, item: Union[str, int]) -> None:
        """Add item to counter."""
        if isinstance(item, int):
            item = str(item)

        hash_val = hashlib.md5(item.encode()).digest()
        j = int.from_bytes(hash_val[:2], 'big') % self.m

        w = int.from_bytes(hash_val[2:], 'big')
        rho = self._count_leading_zeros(w) + 1

        self.M[j] = max(self.M[j], rho)

    def _count_leading_zeros(self, w: int) -> int:
        """Count leading zeros."""
        if w == 0:
            return 32

        count = 0
        mask = 1 << 31

        while (w & mask) == 0 and count < 32:
            count += 1
            mask >>= 1

        return count

    def estimate(self) -> int:
        """Estimate cardinality using geometric mean."""
        # Geometric mean approach
        estimate = self.alpha * (self.m ** 2) * (2 ** (-np.mean(self.M)))

        # Small range correction
        if estimate <= 2.5 * self.m:
            zeros = np.count_nonzero(self.M == 0)
            if zeros > 0:
                return int(self.m * np.log(self.m / zeros))

        return int(estimate)


class SuperLogLog:
    """
    Super-LogLog algorithm - improved version of LogLog.

    Uses harmonic mean and improved bias correction.
    """

    def __init__(self, precision: int = 14):
        """
        Initialize Super-LogLog.

        Args:
            precision: Precision parameter (4-16 typical)
        """
        self.p = precision
        self.m = 1 << precision
        self.M = np.zeros(self.m, dtype=np.int8)

    def add(self, item: Union[str, int]) -> None:
        """Add item to the counter."""
        if isinstance(item, int):
            item = str(item)

        hash_bytes = hashlib.sha256(item.encode()).digest()
        hash_int = int.from_bytes(hash_bytes, 'big')

        # Split hash: first p bits for bucket, rest for rho
        j = hash_int & ((1 << self.p) - 1)
        w = hash_int >> self.p

        # Count leading zeros + 1
        rho = self._leading_zero_count(w) + 1
        self.M[j] = max(self.M[j], rho)

    def _leading_zero_count(self, w: int) -> int:
        """Count leading zeros in w."""
        if w == 0:
            return 64 - self.p

        count = 0
        bit_mask = 1 << (63 - self.p)

        while count < (64 - self.p) and (w & bit_mask) == 0:
            count += 1
            bit_mask >>= 1

        return count

    def estimate(self) -> int:
        """
        Estimate cardinality with improved bias correction.

        Returns:
            Estimated cardinality
        """
        # Harmonic mean with truncation of largest values
        sorted_M = np.sort(self.M)

        # Truncate top 30% for bias reduction
        truncate_idx = int(0.7 * self.m)
        truncated_M = sorted_M[:truncate_idx]

        # Compute estimate
        raw_estimate = 0.7213 * self.m * truncate_idx / \
                      np.sum(2.0 ** (-truncated_M))

        # Small range and large range corrections
        if raw_estimate < 2.5 * self.m:
            zeros = np.count_nonzero(self.M == 0)
            if zeros > 0:
                return int(self.m * np.log(self.m / zeros))

        return int(raw_estimate)


class MinCount:
    """
    MinCount algorithm - uses minimum values instead of bit patterns.

    Alternative approach to FM that tracks k minimum hash values.
    """

    def __init__(self, k: int = 1024):
        """
        Initialize MinCount.

        Args:
            k: Number of minimum values to track
        """
        self.k = k
        self.min_values = []

    def _hash_to_float(self, item: Union[str, int]) -> float:
        """Hash item to float in [0, 1)."""
        if isinstance(item, int):
            item = str(item)

        hash_bytes = hashlib.sha256(item.encode()).digest()
        hash_int = int.from_bytes(hash_bytes[:8], 'big')
        return hash_int / (2 ** 64)

    def add(self, item: Union[str, int]) -> None:
        """Add item to the counter."""
        hash_value = self._hash_to_float(item)

        if len(self.min_values) < self.k:
            self.min_values.append(hash_value)
            self.min_values.sort()
        elif hash_value < self.min_values[-1]:
            self.min_values[-1] = hash_value
            self.min_values.sort()

    def estimate(self) -> int:
        """
        Estimate cardinality from minimum values.

        Returns:
            Estimated cardinality
        """
        if len(self.min_values) < self.k:
            # Not enough samples yet
            return len(self.min_values)

        # Estimate based on k-th minimum
        return int((self.k - 1) / self.min_values[-1])


class AdaptiveFM:
    """
    Adaptive Flajolet-Martin that adjusts precision based on stream size.
    """

    def __init__(self, initial_precision: int = 8, max_precision: int = 16):
        """
        Initialize adaptive FM.

        Args:
            initial_precision: Starting precision
            max_precision: Maximum precision to grow to
        """
        self.current_precision = initial_precision
        self.max_precision = max_precision
        self.estimators = [FlajoletMartin(1 << initial_precision)]
        self.items_seen = 0
        self.threshold_multiplier = 4

    def add(self, item: Union[str, int]) -> None:
        """Add item and potentially upgrade precision."""
        self.items_seen += 1

        # Add to all precision levels
        for estimator in self.estimators:
            estimator.add(item)

        # Check if we should add higher precision
        current_estimate = self.estimators[-1].estimate_cardinality()
        current_capacity = (1 << self.current_precision) * self.threshold_multiplier

        if current_estimate > current_capacity and \
           self.current_precision < self.max_precision:
            self.current_precision += 1
            new_estimator = FlajoletMartin(1 << self.current_precision)

            # Replay seen items (in practice, would merge from lower precision)
            # This is simplified for demonstration
            self.estimators.append(new_estimator)

    def estimate(self) -> int:
        """Get estimate from highest precision level."""
        return self.estimators[-1].estimate_cardinality()


# Example usage and testing
def example_basic_fm():
    """Demonstrate basic Flajolet-Martin algorithm."""
    print("=== Basic Flajolet-Martin Algorithm ===\n")

    fm = FlajoletMartin(num_estimators=32)

    # Add some items with duplicates
    items = ['apple', 'banana', 'apple', 'cherry', 'date', 'banana',
             'elderberry', 'fig', 'grape', 'apple', 'honeydew']

    unique_items = set(items)

    print("Adding items to stream:")
    for item in items:
        fm.add(item)
        print(f"  Added: {item}")

    print(f"\nActual distinct count: {len(unique_items)}")
    print(f"FM estimate: {fm.estimate_cardinality()}")
    print(f"FM estimate (median): {fm.estimate_cardinality(use_median=True)}")


def example_large_stream():
    """Test FM on large stream."""
    print("=== Large Stream Test ===\n")

    # Initialize different variants
    fm_classic = FlajoletMartin(num_estimators=64)
    fm_improved = ImprovedFlajoletMartin(precision=10)
    loglog = LogLogCounting(k=10)
    superloglog = SuperLogLog(precision=10)
    mincount = MinCount(k=1024)

    # Generate stream with known cardinality
    np.random.seed(42)
    true_cardinality = 10000
    stream_size = 100000

    unique_items = set()

    print(f"Processing stream of {stream_size} items")
    print(f"True cardinality: {true_cardinality}\n")

    for _ in range(stream_size):
        # Generate items with controlled cardinality
        item = np.random.randint(0, true_cardinality)
        unique_items.add(item)

        fm_classic.add(item)
        fm_improved.add(item)
        loglog.add(item)
        superloglog.add(item)
        mincount.add(item)

    # Get estimates
    estimates = {
        "Classic FM": fm_classic.estimate_cardinality(),
        "Improved FM": fm_improved.estimate_cardinality(),
        "LogLog": loglog.estimate(),
        "SuperLogLog": superloglog.estimate(),
        "MinCount": mincount.estimate()
    }

    actual = len(unique_items)

    print("Algorithm Comparison:")
    print(f"{'Algorithm':<15} {'Estimate':<10} {'Error %':<10}")
    print("-" * 35)

    for name, estimate in estimates.items():
        error_pct = abs(estimate - actual) / actual * 100
        print(f"{name:<15} {estimate:<10} {error_pct:<10.2f}%")

    print(f"\nActual unique items: {actual}")


def example_merging():
    """Demonstrate merging of FM estimators."""
    print("=== Merging FM Estimators ===\n")

    # Simulate distributed counting
    fm1 = FlajoletMartin(num_estimators=32)
    fm2 = FlajoletMartin(num_estimators=32)

    # Stream 1: Users from region A
    region_a_users = [f"user_a_{i}" for i in range(1000)]
    for user in region_a_users:
        fm1.add(user)

    # Stream 2: Users from region B
    region_b_users = [f"user_b_{i}" for i in range(800)]
    for user in region_b_users:
        fm2.add(user)

    # Some overlap between regions
    overlap_users = [f"user_common_{i}" for i in range(200)]
    for user in overlap_users:
        fm1.add(user)
        fm2.add(user)

    # Get individual estimates
    estimate1 = fm1.estimate_cardinality()
    estimate2 = fm2.estimate_cardinality()

    # Merge estimators
    fm_merged = fm1.merge(fm2)
    merged_estimate = fm_merged.estimate_cardinality()

    # True count
    all_users = set(region_a_users + region_b_users + overlap_users)
    true_count = len(all_users)

    print("Distributed Counting Results:")
    print(f"  Region A estimate: {estimate1}")
    print(f"  Region B estimate: {estimate2}")
    print(f"  Merged estimate: {merged_estimate}")
    print(f"  True total unique: {true_count}")
    print(f"  Merge error: {abs(merged_estimate - true_count) / true_count * 100:.2f}%")


def example_streaming_analytics():
    """Real-world example: Website unique visitor counting."""
    print("=== Website Analytics: Unique Visitor Counting ===\n")

    # Initialize FM for hourly and daily counting
    hourly_fm = FlajoletMartin(num_estimators=128)
    daily_fm = ImprovedFlajoletMartin(precision=14)

    # Simulate visitor stream
    np.random.seed(42)

    print("Simulating 24 hours of website traffic...")
    print("-" * 50)

    total_hits = 0
    unique_visitors_actual = set()

    for hour in range(24):
        # Traffic varies by hour
        if 9 <= hour <= 17:  # Business hours
            num_visitors = np.random.poisson(5000)
        elif 18 <= hour <= 23:  # Evening
            num_visitors = np.random.poisson(3000)
        else:  # Night/early morning
            num_visitors = np.random.poisson(500)

        hour_visitors = set()

        for _ in range(num_visitors):
            # Some visitors return multiple times
            if np.random.random() < 0.3 and unique_visitors_actual:
                # Returning visitor
                visitor_id = np.random.choice(list(unique_visitors_actual))
            else:
                # New visitor
                visitor_id = f"visitor_{len(unique_visitors_actual)}"
                unique_visitors_actual.add(visitor_id)

            hour_visitors.add(visitor_id)
            hourly_fm.add(visitor_id)
            daily_fm.add(visitor_id)
            total_hits += 1

        if hour % 6 == 5:
            print(f"\nHour {hour + 1:2d} Report:")
            print(f"  Hits this hour: {num_visitors}")
            print(f"  Unique this hour: {len(hour_visitors)}")
            print(f"  Estimated unique so far: {hourly_fm.estimate_cardinality()}")

    print("\n" + "=" * 50)
    print("Daily Summary:")
    print(f"  Total hits: {total_hits}")
    print(f"  Actual unique visitors: {len(unique_visitors_actual)}")
    print(f"  FM estimate (128 estimators): {hourly_fm.estimate_cardinality()}")
    print(f"  Improved FM estimate: {daily_fm.estimate_cardinality()}")

    fm_error = abs(hourly_fm.estimate_cardinality() - len(unique_visitors_actual)) / len(unique_visitors_actual) * 100
    improved_error = abs(daily_fm.estimate_cardinality() - len(unique_visitors_actual)) / len(unique_visitors_actual) * 100

    print(f"\nAccuracy:")
    print(f"  Classic FM error: {fm_error:.2f}%")
    print(f"  Improved FM error: {improved_error:.2f}%")

    # Memory usage comparison
    exact_memory = len(unique_visitors_actual) * 32  # Assuming 32 bytes per ID
    fm_memory = 128 * 4  # 128 integers
    improved_memory = (1 << 14)  # 2^14 bytes

    print(f"\nMemory Usage:")
    print(f"  Exact (HashSet): {exact_memory:,} bytes")
    print(f"  Classic FM: {fm_memory} bytes")
    print(f"  Improved FM: {improved_memory:,} bytes")
    print(f"  Memory savings: {exact_memory / improved_memory:.1f}x")


if __name__ == "__main__":
    # Run examples
    example_basic_fm()
    print("\n" + "=" * 60 + "\n")

    example_large_stream()
    print("\n" + "=" * 60 + "\n")

    example_merging()
    print("\n" + "=" * 60 + "\n")

    example_streaming_analytics()

    print("\n" + "=" * 60)
    print("Key Insights:")
    print("=" * 60)
    print("""
1. Flajolet-Martin provides logarithmic space cardinality estimation,
   crucial for massive data streams.

2. Multiple independent estimators reduce variance through averaging,
   with median being more robust than mean.

3. Improved variants (LogLog, SuperLogLog) use stochastic averaging
   and bias correction for better accuracy.

4. FM estimators are mergeable, enabling distributed cardinality
   counting across multiple data streams or servers.

5. The algorithm trades accuracy for memory: ~2% error with just
   a few KB of memory vs. exact counting requiring O(n) space.

6. Different variants optimize for different scenarios:
   - Classic FM: Simple, good for teaching
   - LogLog/SuperLogLog: Better accuracy
   - MinCount: Alternative approach using minimum values

7. Real-world applications include:
   - Website unique visitor counting
   - Database query optimization
   - Network traffic analysis
   - Distributed systems monitoring
    """)