#!/usr/bin/env python3
"""
Count-Min Sketch Implementation

A probabilistic data structure for frequency estimation in data streams.
Provides approximate frequency counts with guaranteed error bounds using
sublinear space. Particularly useful for streaming algorithms and
finding heavy hitters in large datasets.

Key Features:
- Space-efficient frequency counting
- Guaranteed overestimation (never underestimates)
- Sublinear space complexity O(epsilon * delta)
- Constant time updates and queries O(d)

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
import hashlib
from typing import List, Tuple, Any, Optional, Dict, Set
from collections import defaultdict
import math
import mmh3  # MurmurHash3 for better hash distribution


class CountMinSketch:
    """
    Count-Min Sketch for frequency estimation.

    A probabilistic data structure that uses multiple hash functions
    and a 2D array to estimate item frequencies with bounded error.

    Parameters:
        width: Number of counters per row (affects accuracy)
        depth: Number of hash functions/rows (affects confidence)
        epsilon: Error factor (optional, calculates width)
        delta: Failure probability (optional, calculates depth)
    """

    def __init__(self, width: int = None, depth: int = None,
                 epsilon: float = None, delta: float = None):
        """
        Initialize Count-Min Sketch.

        Can specify either width/depth directly or epsilon/delta for automatic sizing.

        Args:
            width: Number of counters per row
            depth: Number of hash functions
            epsilon: Relative error bound (e.g., 0.01 for 1% error)
            delta: Failure probability (e.g., 0.01 for 99% confidence)
        """
        if epsilon and delta:
            # Calculate dimensions from error parameters
            self.width = int(np.ceil(np.e / epsilon))
            self.depth = int(np.ceil(np.log(1.0 / delta)))
            self.epsilon = epsilon
            self.delta = delta
        elif width and depth:
            self.width = width
            self.depth = depth
            # Calculate error parameters
            self.epsilon = np.e / width
            self.delta = np.exp(-depth)
        else:
            # Default parameters for reasonable accuracy
            self.width = 2000
            self.depth = 5
            self.epsilon = np.e / self.width
            self.delta = np.exp(-self.depth)

        # Initialize the sketch table
        self.table = np.zeros((self.depth, self.width), dtype=np.int64)

        # Random seeds for hash functions
        self.hash_seeds = [i * 17 + 31 for i in range(self.depth)]

        # Track total items counted
        self.total_count = 0

        print(f"Count-Min Sketch initialized:")
        print(f"  Width: {self.width}, Depth: {self.depth}")
        print(f"  Error rate (epsilon): {self.epsilon:.4f}")
        print(f"  Failure probability (delta): {self.delta:.4f}")
        print(f"  Memory usage: {self.table.nbytes / 1024:.1f} KB")

    def _hash(self, item: Any, seed: int) -> int:
        """
        Hash an item to a position in the table.

        Args:
            item: The item to hash
            seed: Seed for the hash function

        Returns:
            Hash value modulo width
        """
        if isinstance(item, str):
            item_bytes = item.encode('utf-8')
        else:
            item_bytes = str(item).encode('utf-8')

        # Use MurmurHash3 for good distribution
        hash_value = mmh3.hash(item_bytes, seed, signed=False)
        return hash_value % self.width

    def add(self, item: Any, count: int = 1) -> None:
        """
        Add an item to the sketch with given count.

        Args:
            item: The item to add
            count: The count to add (default: 1)
        """
        for i in range(self.depth):
            j = self._hash(item, self.hash_seeds[i])
            self.table[i, j] += count

        self.total_count += count

    def update(self, item: Any, count: int = 1) -> None:
        """Alias for add method"""
        self.add(item, count)

    def query(self, item: Any) -> int:
        """
        Query the estimated frequency of an item.

        Returns the minimum count across all hash functions,
        which gives the best estimate with guaranteed overestimation.

        Args:
            item: The item to query

        Returns:
            Estimated frequency count
        """
        min_count = float('inf')

        for i in range(self.depth):
            j = self._hash(item, self.hash_seeds[i])
            min_count = min(min_count, self.table[i, j])

        return int(min_count)

    def estimate(self, item: Any) -> int:
        """Alias for query method"""
        return self.query(item)

    def merge(self, other: 'CountMinSketch') -> 'CountMinSketch':
        """
        Merge another Count-Min Sketch into this one.

        Both sketches must have the same dimensions.

        Args:
            other: Another Count-Min Sketch to merge

        Returns:
            Self for method chaining

        Raises:
            ValueError: If dimensions don't match
        """
        if self.width != other.width or self.depth != other.depth:
            raise ValueError("Cannot merge sketches with different dimensions")

        self.table += other.table
        self.total_count += other.total_count
        return self

    def clear(self) -> None:
        """Clear all counts in the sketch"""
        self.table.fill(0)
        self.total_count = 0

    def get_heavy_hitters(self, threshold: float = 0.01) -> List[Tuple[Any, int]]:
        """
        Find heavy hitters (frequent items) in the sketch.

        Note: This requires tracking items separately as the sketch
        itself doesn't store actual items, only counts.

        Args:
            threshold: Fraction of total count (e.g., 0.01 for 1%)

        Returns:
            List of (item, count) tuples for heavy hitters
        """
        # This is a limitation of pure Count-Min Sketch
        # In practice, you'd maintain a separate structure
        print("Note: Heavy hitters require tracking items separately")
        return []

    def error_bound(self) -> float:
        """
        Calculate the error bound for frequency estimates.

        With probability 1-delta, the error is at most epsilon * total_count

        Returns:
            Maximum expected error in frequency estimates
        """
        return self.epsilon * self.total_count

    def __getitem__(self, item: Any) -> int:
        """Allow dictionary-style access"""
        return self.query(item)

    def __str__(self) -> str:
        """String representation"""
        return (f"CountMinSketch(width={self.width}, depth={self.depth}, "
                f"epsilon={self.epsilon:.4f}, delta={self.delta:.4f}, "
                f"total_count={self.total_count})")

    def __repr__(self) -> str:
        return self.__str__()


class CountMinSketchWithHeap:
    """
    Enhanced Count-Min Sketch that tracks heavy hitters using a min-heap.

    Maintains a heap of the top-k frequent items for efficient
    heavy hitter queries.
    """

    def __init__(self, width: int = 2000, depth: int = 5, k: int = 100):
        """
        Initialize Count-Min Sketch with heavy hitter tracking.

        Args:
            width: Number of counters per row
            depth: Number of hash functions
            k: Number of top items to track
        """
        self.sketch = CountMinSketch(width=width, depth=depth)
        self.k = k
        self.heavy_hitters = {}  # item -> estimated count
        self.min_heap_threshold = 0

    def add(self, item: Any, count: int = 1) -> None:
        """Add an item and update heavy hitters"""
        self.sketch.add(item, count)
        estimated = self.sketch.query(item)

        # Update heavy hitters
        if estimated > self.min_heap_threshold:
            self.heavy_hitters[item] = estimated

            # Maintain top-k
            if len(self.heavy_hitters) > self.k:
                # Remove item with minimum count
                min_item = min(self.heavy_hitters, key=self.heavy_hitters.get)
                self.min_heap_threshold = self.heavy_hitters[min_item]
                del self.heavy_hitters[min_item]

    def get_top_k(self) -> List[Tuple[Any, int]]:
        """
        Get the top-k frequent items.

        Returns:
            List of (item, estimated_count) tuples sorted by frequency
        """
        return sorted(self.heavy_hitters.items(),
                     key=lambda x: x[1], reverse=True)

    def query(self, item: Any) -> int:
        """Query frequency of an item"""
        return self.sketch.query(item)


class ConservativeUpdateSketch(CountMinSketch):
    """
    Conservative Update variant of Count-Min Sketch.

    Only increments the minimum counters, reducing overestimation
    compared to standard Count-Min Sketch.
    """

    def add(self, item: Any, count: int = 1) -> None:
        """
        Conservative add - only update minimum counters.

        Args:
            item: The item to add
            count: The count to add
        """
        # Find current minimum estimate
        min_count = self.query(item)

        # Only update counters that have the minimum value
        for i in range(self.depth):
            j = self._hash(item, self.hash_seeds[i])
            if self.table[i, j] == min_count:
                self.table[i, j] += count

        self.total_count += count


class CountSketch:
    """
    Count Sketch - a variant that can handle negative updates.

    Uses random +1/-1 signs to allow for deletions and provides
    unbiased estimates with bounded variance.
    """

    def __init__(self, width: int = 2000, depth: int = 5):
        """
        Initialize Count Sketch.

        Args:
            width: Number of counters per row
            depth: Number of hash functions
        """
        self.width = width
        self.depth = depth
        self.table = np.zeros((depth, width), dtype=np.int64)

        # Hash seeds for position and sign
        self.hash_seeds = [i * 31 + 17 for i in range(depth)]
        self.sign_seeds = [i * 37 + 23 for i in range(depth)]

    def _hash_position(self, item: Any, seed: int) -> int:
        """Hash to position"""
        item_bytes = str(item).encode('utf-8')
        return mmh3.hash(item_bytes, seed, signed=False) % self.width

    def _hash_sign(self, item: Any, seed: int) -> int:
        """Hash to +1 or -1"""
        item_bytes = str(item).encode('utf-8')
        return 1 if mmh3.hash(item_bytes, seed) % 2 == 0 else -1

    def add(self, item: Any, count: int = 1) -> None:
        """Add an item with count (can be negative for deletion)"""
        for i in range(self.depth):
            j = self._hash_position(item, self.hash_seeds[i])
            g = self._hash_sign(item, self.sign_seeds[i])
            self.table[i, j] += g * count

    def query(self, item: Any) -> int:
        """
        Query using median estimate for robustness.

        Returns:
            Median of estimates from all rows
        """
        estimates = []
        for i in range(self.depth):
            j = self._hash_position(item, self.hash_seeds[i])
            g = self._hash_sign(item, self.sign_seeds[i])
            estimates.append(g * self.table[i, j])

        # Return median for robustness
        return int(np.median(estimates))


def demo_count_min_sketch():
    """Demonstrate Count-Min Sketch usage"""
    print("Count-Min Sketch Demo")
    print("=" * 50)

    # Create a sketch with 1% error and 99% confidence
    cms = CountMinSketch(epsilon=0.01, delta=0.01)

    # Simulate a data stream
    stream = ['apple'] * 100 + ['banana'] * 50 + ['orange'] * 30
    stream += ['grape'] * 10 + ['peach'] * 5
    np.random.shuffle(stream)

    # Add items to sketch
    for item in stream:
        cms.add(item)

    # Query frequencies
    print("\nFrequency Estimates:")
    for item in ['apple', 'banana', 'orange', 'grape', 'peach', 'mango']:
        estimated = cms.query(item)
        print(f"  {item}: {estimated}")

    print(f"\nError bound: <= {cms.error_bound():.1f}")
    print(f"Total items: {cms.total_count}")

    # Test heavy hitters tracking
    print("\n" + "=" * 50)
    print("Heavy Hitters Demo")

    cms_hh = CountMinSketchWithHeap(width=1000, depth=4, k=5)

    # Add same stream
    for item in stream:
        cms_hh.add(item)

    print("\nTop-5 frequent items:")
    for item, count in cms_hh.get_top_k():
        print(f"  {item}: {count}")

    # Test conservative update
    print("\n" + "=" * 50)
    print("Conservative Update Comparison")

    standard = CountMinSketch(width=100, depth=3)
    conservative = ConservativeUpdateSketch(width=100, depth=3)

    test_stream = ['a'] * 10 + ['b'] * 5 + ['c'] * 3

    for item in test_stream:
        standard.add(item)
        conservative.add(item)

    print("\nEstimates for 'a':")
    print(f"  Standard CMS: {standard.query('a')}")
    print(f"  Conservative: {conservative.query('a')}")


if __name__ == "__main__":
    demo_count_min_sketch()