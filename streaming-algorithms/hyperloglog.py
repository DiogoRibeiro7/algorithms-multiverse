"""
HyperLogLog and Cardinality Estimation Algorithms
=================================================

Implementations of probabilistic algorithms for estimating the number of
distinct elements in large data streams using minimal memory.

Includes:
- HyperLogLog (HLL) - Standard implementation
- HyperLogLog++ - Enhanced version with bias correction
- Linear Counting
- LogLog algorithm
- Flajolet-Martin algorithm

Author: Claude
Date: January 2026
"""

import hashlib
import numpy as np
from typing import Any, List, Optional, Union
import struct
import math


class HyperLogLog:
    """
    HyperLogLog algorithm for cardinality estimation.

    Uses probabilistic counting to estimate the number of unique elements
    in a dataset using only O(m) memory where m is the number of buckets.

    Standard error: ~1.04/sqrt(m)
    """

    def __init__(self, precision: int = 14):
        """
        Initialize HyperLogLog.

        Args:
            precision: Number of bits to use for bucket addressing (4-16).
                      Higher precision = more accuracy but more memory.
                      Memory usage = 2^precision bytes
        """
        if not 4 <= precision <= 16:
            raise ValueError("Precision must be between 4 and 16")

        self.precision = precision
        self.m = 1 << precision  # Number of buckets (2^precision)
        self.buckets = np.zeros(self.m, dtype=np.uint8)

        # Alpha constant for bias correction
        if self.m == 16:
            self.alpha = 0.673
        elif self.m == 32:
            self.alpha = 0.697
        elif self.m == 64:
            self.alpha = 0.709
        else:
            self.alpha = 0.7213 / (1 + 1.079 / self.m)

    def _hash(self, item: Any) -> int:
        """
        Hash an item to a 64-bit integer.

        Args:
            item: Item to hash

        Returns:
            64-bit hash value
        """
        # Convert item to bytes
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')

        # Use SHA-256 and take first 8 bytes
        hash_bytes = hashlib.sha256(data).digest()[:8]
        return struct.unpack('>Q', hash_bytes)[0]

    def _leading_zeros(self, bits: int, start_bit: int = 0) -> int:
        """
        Count leading zeros in binary representation.

        Args:
            bits: Integer to count zeros in
            start_bit: Bit position to start counting from

        Returns:
            Number of leading zeros plus one
        """
        # Mask to ignore the bucket bits
        mask = (1 << (64 - self.precision)) - 1
        bits = (bits & mask) << self.precision

        if bits == 0:
            return 64 - self.precision + 1

        # Count leading zeros
        leading_zeros = 0
        for i in range(64 - self.precision):
            if bits & (1 << (63 - i)):
                break
            leading_zeros += 1

        return leading_zeros + 1

    def add(self, item: Any):
        """
        Add an item to the HyperLogLog.

        Args:
            item: Item to add
        """
        # Hash the item
        hash_value = self._hash(item)

        # Use first 'precision' bits for bucket index
        bucket_idx = hash_value >> (64 - self.precision)

        # Count leading zeros in remaining bits
        leading_zeros = self._leading_zeros(hash_value)

        # Update bucket with maximum leading zeros seen
        self.buckets[bucket_idx] = max(self.buckets[bucket_idx], leading_zeros)

    def count(self) -> int:
        """
        Estimate the cardinality.

        Returns:
            Estimated number of unique elements
        """
        # Calculate raw estimate
        raw_estimate = self.alpha * self.m ** 2 / np.sum(2.0 ** (-self.buckets))

        # Apply bias correction for small and large cardinalities
        if raw_estimate <= 2.5 * self.m:
            # Small range correction
            zeros = np.count_nonzero(self.buckets == 0)
            if zeros != 0:
                return int(self.m * np.log(self.m / float(zeros)))

        if raw_estimate <= (1.0/30.0) * (1 << 32):
            # No correction
            return int(raw_estimate)
        else:
            # Large range correction
            return int(-1 * (1 << 32) * np.log(1 - raw_estimate / (1 << 32)))

    def merge(self, other: 'HyperLogLog'):
        """
        Merge another HyperLogLog into this one.

        Args:
            other: Another HyperLogLog with same precision
        """
        if self.precision != other.precision:
            raise ValueError("Cannot merge HyperLogLogs with different precisions")

        # Take maximum of each bucket
        self.buckets = np.maximum(self.buckets, other.buckets)

    def relative_error(self) -> float:
        """
        Calculate the expected relative standard error.

        Returns:
            Expected relative error
        """
        return 1.04 / math.sqrt(self.m)


class HyperLogLogPlusPlus(HyperLogLog):
    """
    HyperLogLog++ algorithm with enhanced bias correction.

    Improvements over standard HLL:
    - Better bias correction for small cardinalities
    - Sparse representation for better accuracy with small sets
    - 64-bit hash for better accuracy
    """

    def __init__(self, precision: int = 14, sparse_precision: int = 25):
        """
        Initialize HyperLogLog++.

        Args:
            precision: Normal precision (p)
            sparse_precision: Precision for sparse mode (p')
        """
        super().__init__(precision)
        self.sparse_precision = sparse_precision
        self.sparse = True
        self.sparse_list = []

        # Threshold for switching from sparse to normal
        self.sparse_threshold = self.m * 6

    def add(self, item: Any):
        """Add an item to HyperLogLog++."""
        hash_value = self._hash(item)

        if self.sparse:
            # Sparse mode
            self._add_sparse(hash_value)

            # Check if we should switch to normal mode
            if len(self.sparse_list) > self.sparse_threshold:
                self._switch_to_normal()
        else:
            # Normal mode
            bucket_idx = hash_value >> (64 - self.precision)
            leading_zeros = self._leading_zeros(hash_value)
            self.buckets[bucket_idx] = max(self.buckets[bucket_idx], leading_zeros)

    def _add_sparse(self, hash_value: int):
        """Add to sparse representation."""
        # Encode as (index, rho) pair
        idx = hash_value >> (64 - self.sparse_precision)
        rho = self._leading_zeros(hash_value << self.sparse_precision) + self.sparse_precision - self.precision

        # Store in sparse list (could be optimized with better data structure)
        self.sparse_list.append((idx, rho))

    def _switch_to_normal(self):
        """Convert from sparse to normal representation."""
        self.sparse = False

        # Convert sparse list to buckets
        for idx, rho in self.sparse_list:
            # Map sparse index to normal bucket
            bucket_idx = idx >> (self.sparse_precision - self.precision)
            self.buckets[bucket_idx] = max(self.buckets[bucket_idx], rho)

        self.sparse_list = []

    def count(self) -> int:
        """Estimate cardinality with improved bias correction."""
        if self.sparse:
            # Estimate from sparse representation
            return self._count_sparse()

        # Use enhanced bias correction
        raw_estimate = self.alpha * self.m ** 2 / np.sum(2.0 ** (-self.buckets))

        # Enhanced bias correction
        if raw_estimate <= 5 * self.m:
            return self._bias_correction(raw_estimate)

        return int(raw_estimate)

    def _count_sparse(self) -> int:
        """Count from sparse representation."""
        # Simple approximation for sparse mode
        # In practice, would use more sophisticated estimation
        return len(set(idx for idx, _ in self.sparse_list))

    def _bias_correction(self, raw_estimate: float) -> int:
        """Apply bias correction for small cardinalities."""
        # Simplified bias correction
        # Real implementation would use empirically derived bias data
        zeros = np.count_nonzero(self.buckets == 0)
        if zeros != 0:
            return int(self.m * np.log(self.m / float(zeros)))
        return int(raw_estimate)


class LinearCounting:
    """
    Linear Counting algorithm for cardinality estimation.

    Simpler than HyperLogLog but uses more memory.
    Good for smaller cardinalities.
    """

    def __init__(self, max_cardinality: int = 100000):
        """
        Initialize Linear Counting.

        Args:
            max_cardinality: Expected maximum cardinality
        """
        # Size of bit map (use ~10 bits per expected unique element)
        self.m = max(1024, int(max_cardinality * 10))
        self.bitmap = np.zeros(self.m, dtype=bool)
        self.modified = False

    def _hash(self, item: Any) -> int:
        """Hash an item to an integer."""
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')

        # Use simple hash for speed
        return hash(data) & 0x7FFFFFFF

    def add(self, item: Any):
        """Add an item."""
        hash_value = self._hash(item)
        bit_index = hash_value % self.m

        if not self.bitmap[bit_index]:
            self.bitmap[bit_index] = True
            self.modified = True

    def count(self) -> int:
        """Estimate cardinality."""
        # Count empty bits
        empty_bits = np.count_nonzero(~self.bitmap)

        if empty_bits == 0:
            # Bitmap is full
            return self.m  # Lower bound

        # Linear counting formula
        return int(self.m * np.log(self.m / float(empty_bits)))

    def merge(self, other: 'LinearCounting'):
        """Merge another LinearCounting instance."""
        if self.m != other.m:
            raise ValueError("Cannot merge LinearCounting with different sizes")

        self.bitmap |= other.bitmap
        self.modified = True


class FlajoletMartin:
    """
    Flajolet-Martin algorithm for cardinality estimation.

    One of the earliest streaming algorithms for distinct counting.
    Uses the position of the rightmost 1-bit in hash values.
    """

    def __init__(self, num_hashes: int = 32):
        """
        Initialize Flajolet-Martin.

        Args:
            num_hashes: Number of hash functions to use (reduces variance)
        """
        self.num_hashes = num_hashes
        self.max_zeros = np.zeros(num_hashes, dtype=int)

    def _hash(self, item: Any, seed: int) -> int:
        """Hash with seed."""
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')

        # Add seed to data
        data = data + str(seed).encode('utf-8')

        # Use SHA-256
        hash_bytes = hashlib.sha256(data).digest()[:4]
        return struct.unpack('>I', hash_bytes)[0]

    def _trailing_zeros(self, n: int) -> int:
        """Count trailing zeros in binary representation."""
        if n == 0:
            return 32

        count = 0
        while n & 1 == 0:
            count += 1
            n >>= 1
        return count

    def add(self, item: Any):
        """Add an item."""
        for i in range(self.num_hashes):
            hash_value = self._hash(item, i)
            trailing = self._trailing_zeros(hash_value)
            self.max_zeros[i] = max(self.max_zeros[i], trailing)

    def count(self) -> int:
        """Estimate cardinality."""
        # Use median of estimates to reduce variance
        estimates = 2 ** self.max_zeros

        # Different averaging methods
        # Method 1: Median (more robust to outliers)
        median_estimate = np.median(estimates)

        # Method 2: Mean of middle values
        sorted_estimates = np.sort(estimates)
        start = self.num_hashes // 4
        end = 3 * self.num_hashes // 4
        mean_estimate = np.mean(sorted_estimates[start:end])

        # Apply correction factor (phi ≈ 0.77351)
        phi = 0.77351

        return int(mean_estimate / phi)


class MorrisCounting:
    """
    Morris Counting algorithm for approximate counting.

    Uses probabilistic increment to count large numbers with logarithmic space.
    Different from cardinality estimation - this counts total items, not unique.
    """

    def __init__(self, delta: float = 0.1):
        """
        Initialize Morris Counter.

        Args:
            delta: Error parameter (smaller = more accurate but slower)
        """
        self.delta = delta
        self.X = 0  # Counter value
        self.a = 1 + delta  # Base for exponential

    def increment(self):
        """Increment the counter probabilistically."""
        # Increment with probability 1/a^X
        if np.random.random() < 1.0 / (self.a ** self.X):
            self.X += 1

    def count(self) -> int:
        """Get estimated count."""
        return int(self.a ** self.X - 1)

    def merge(self, other: 'MorrisCounting'):
        """Merge another Morris counter."""
        # Approximate merge
        total_estimate = self.count() + other.count()

        # Reset and set to approximate combined value
        self.X = int(np.log(total_estimate + 1) / np.log(self.a))


class CountingBloomFilter:
    """
    Counting Bloom Filter for frequency estimation.

    Extension of Bloom filter that can count occurrences and support deletions.
    """

    def __init__(self, expected_elements: int = 10000, false_positive_rate: float = 0.01):
        """
        Initialize Counting Bloom Filter.

        Args:
            expected_elements: Expected number of elements
            false_positive_rate: Desired false positive rate
        """
        # Calculate optimal size and hash functions
        self.m = int(-expected_elements * np.log(false_positive_rate) / (np.log(2) ** 2))
        self.k = int(self.m * np.log(2) / expected_elements)

        # Use 4-bit counters (max count = 15)
        self.counters = np.zeros(self.m, dtype=np.uint8)

    def _hash(self, item: Any, seed: int) -> int:
        """Generate hash with seed."""
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')

        # Add seed
        data = data + str(seed).encode('utf-8')

        # Hash and map to counter index
        hash_value = hash(data) & 0x7FFFFFFF
        return hash_value % self.m

    def add(self, item: Any):
        """Add an item (increment counters)."""
        for i in range(self.k):
            idx = self._hash(item, i)
            if self.counters[idx] < 15:  # Prevent overflow
                self.counters[idx] += 1

    def remove(self, item: Any):
        """Remove an item (decrement counters)."""
        # First check if item might be present
        if not self.contains(item):
            return False

        for i in range(self.k):
            idx = self._hash(item, i)
            if self.counters[idx] > 0:
                self.counters[idx] -= 1

        return True

    def contains(self, item: Any) -> bool:
        """Check if item might be in the filter."""
        for i in range(self.k):
            idx = self._hash(item, i)
            if self.counters[idx] == 0:
                return False
        return True

    def frequency(self, item: Any) -> int:
        """Estimate frequency of an item."""
        min_count = float('inf')

        for i in range(self.k):
            idx = self._hash(item, i)
            min_count = min(min_count, self.counters[idx])

        return int(min_count)


def example_usage():
    """Demonstrate cardinality estimation algorithms."""
    print("=" * 60)
    print("CARDINALITY ESTIMATION ALGORITHMS")
    print("=" * 60)

    # Generate test data
    np.random.seed(42)

    # Create dataset with known cardinality
    unique_items = [f"item_{i}" for i in range(10000)]
    # Add duplicates
    dataset = []
    for item in unique_items:
        count = np.random.geometric(0.3)  # Geometric distribution for counts
        dataset.extend([item] * count)

    np.random.shuffle(dataset)
    actual_cardinality = len(unique_items)

    print(f"\nDataset: {len(dataset)} total items, {actual_cardinality} unique items")
    print("-" * 40)

    # Test HyperLogLog
    print("\n1. HyperLogLog:")
    for precision in [8, 10, 12, 14]:
        hll = HyperLogLog(precision)
        for item in dataset:
            hll.add(item)

        estimate = hll.count()
        error = abs(estimate - actual_cardinality) / actual_cardinality * 100
        memory = 2 ** precision

        print(f"  Precision {precision:2d}: Estimate = {estimate:5d}, "
              f"Error = {error:5.2f}%, Memory = {memory:6d} bytes")

    # Test HyperLogLog++
    print("\n2. HyperLogLog++:")
    hll_pp = HyperLogLogPlusPlus(precision=14)
    for item in dataset:
        hll_pp.add(item)

    estimate = hll_pp.count()
    error = abs(estimate - actual_cardinality) / actual_cardinality * 100
    print(f"  Estimate = {estimate}, Error = {error:.2f}%")

    # Test Linear Counting
    print("\n3. Linear Counting:")
    lc = LinearCounting(max_cardinality=20000)
    for item in dataset:
        lc.add(item)

    estimate = lc.count()
    error = abs(estimate - actual_cardinality) / actual_cardinality * 100
    print(f"  Estimate = {estimate}, Error = {error:.2f}%")

    # Test Flajolet-Martin
    print("\n4. Flajolet-Martin:")
    fm = FlajoletMartin(num_hashes=32)
    for item in dataset:
        fm.add(item)

    estimate = fm.count()
    error = abs(estimate - actual_cardinality) / actual_cardinality * 100
    print(f"  Estimate = {estimate}, Error = {error:.2f}%")

    # Test merging
    print("\n5. Merging HyperLogLogs:")
    hll1 = HyperLogLog(12)
    hll2 = HyperLogLog(12)

    # Split data
    mid = len(unique_items) // 2
    for item in unique_items[:mid]:
        hll1.add(item)
    for item in unique_items[mid:]:
        hll2.add(item)

    print(f"  HLL1 estimate: {hll1.count()}")
    print(f"  HLL2 estimate: {hll2.count()}")

    hll1.merge(hll2)
    merged_estimate = hll1.count()
    error = abs(merged_estimate - actual_cardinality) / actual_cardinality * 100
    print(f"  Merged estimate: {merged_estimate}, Error = {error:.2f}%")

    # Test Morris Counting
    print("\n6. Morris Counting (Approximate Counting):")
    morris = MorrisCounting(delta=0.1)

    true_count = 100000
    for _ in range(true_count):
        morris.increment()

    estimate = morris.count()
    error = abs(estimate - true_count) / true_count * 100
    print(f"  True count: {true_count}")
    print(f"  Morris estimate: {estimate}, Error = {error:.2f}%")
    print(f"  Space used: X = {morris.X} (vs {len(str(true_count))} digits for exact)")

    # Test Counting Bloom Filter
    print("\n7. Counting Bloom Filter (Frequency Estimation):")
    cbf = CountingBloomFilter(expected_elements=1000, false_positive_rate=0.01)

    # Add items with frequencies
    test_items = {"apple": 5, "banana": 3, "orange": 7}
    for item, count in test_items.items():
        for _ in range(count):
            cbf.add(item)

    print("  Frequency estimates:")
    for item, true_count in test_items.items():
        est_freq = cbf.frequency(item)
        print(f"    {item}: True = {true_count}, Estimate = {est_freq}")

    # Performance comparison
    print("\n8. Performance Comparison:")
    print("-" * 40)

    import time

    test_size = 50000
    test_data = [f"item_{i % 10000}" for i in range(test_size)]

    algorithms = [
        ("HyperLogLog(10)", HyperLogLog(10)),
        ("HyperLogLog(14)", HyperLogLog(14)),
        ("LinearCounting", LinearCounting()),
        ("FlajoletMartin", FlajoletMartin(16))
    ]

    for name, algo in algorithms:
        start = time.time()
        for item in test_data:
            algo.add(item)
        estimate = algo.count()
        elapsed = time.time() - start

        print(f"  {name:20s}: {elapsed*1000:6.2f} ms, Estimate = {estimate}")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- HyperLogLog provides excellent accuracy/memory trade-off")
    print("- Higher precision = better accuracy but more memory")
    print("- Linear Counting is simpler but uses more memory")
    print("- Flajolet-Martin is historically important but less accurate")
    print("- Morris Counting approximates counts, not cardinality")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()