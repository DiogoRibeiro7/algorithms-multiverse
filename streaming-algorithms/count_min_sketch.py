"""
Count-Min Sketch Implementation
===============================

A probabilistic data structure for frequency estimation in data streams.
The Count-Min Sketch provides approximate frequency counts with guaranteed
error bounds using sub-linear space.

Key Features:
- Space-efficient frequency counting
- Guaranteed overestimation (never underestimates)
- Configurable accuracy vs space trade-off
- Support for heavy hitters detection
- Mergeable sketches for distributed systems

Applications:
- Network traffic monitoring
- Database query optimization
- Frequent itemset mining
- Real-time analytics
- DDoS attack detection

Author: Claude
Date: January 2026
"""

import numpy as np
import hashlib
from typing import Any, List, Tuple, Optional, Dict, Set
from dataclasses import dataclass, field
import mmh3  # MurmurHash3 for better hash distribution
import math
from collections import defaultdict


@dataclass
class SketchConfig:
    """Configuration for Count-Min Sketch."""
    width: int  # Number of counters per row
    depth: int  # Number of hash functions
    seed: int = 42

    @classmethod
    def from_error_prob(cls, epsilon: float, delta: float, seed: int = 42) -> 'SketchConfig':
        """
        Create config from error probability parameters.

        Args:
            epsilon: Error factor (relative error bound)
            delta: Failure probability
            seed: Random seed

        Returns:
            SketchConfig with optimal dimensions
        """
        width = math.ceil(math.e / epsilon)
        depth = math.ceil(math.log(1 / delta))
        return cls(width=width, depth=depth, seed=seed)


class CountMinSketch:
    """
    Count-Min Sketch for frequency estimation.

    Provides approximate frequency counts with error bounds:
    - Estimate >= True Count (never underestimates)
    - P(Estimate <= True Count + ε * ||a||₁) >= 1 - δ
    """

    def __init__(self, config: Optional[SketchConfig] = None):
        """
        Initialize Count-Min Sketch.

        Args:
            config: Sketch configuration
        """
        if config is None:
            # Default: 0.1% error rate with 99.9% confidence
            config = SketchConfig.from_error_prob(0.001, 0.001)

        self.config = config
        self.table = np.zeros((config.depth, config.width), dtype=np.int64)
        self.total_count = 0

    def _hash(self, item: Any, i: int) -> int:
        """
        Compute hash for item with i-th hash function.

        Args:
            item: Item to hash
            i: Hash function index

        Returns:
            Hash value in range [0, width)
        """
        # Convert item to bytes if needed
        if isinstance(item, str):
            item_bytes = item.encode('utf-8')
        elif isinstance(item, (int, float)):
            item_bytes = str(item).encode('utf-8')
        else:
            item_bytes = str(item).encode('utf-8')

        # Use MurmurHash3 with different seeds
        hash_value = mmh3.hash(item_bytes, self.config.seed + i, signed=False)
        return hash_value % self.config.width

    def update(self, item: Any, count: int = 1):
        """
        Add item to sketch with given count.

        Args:
            item: Item to add
            count: Count to add (default 1)
        """
        for i in range(self.config.depth):
            j = self._hash(item, i)
            self.table[i, j] += count
        self.total_count += count

    def query(self, item: Any) -> int:
        """
        Query frequency estimate for item.

        Args:
            item: Item to query

        Returns:
            Estimated frequency count
        """
        min_count = float('inf')
        for i in range(self.config.depth):
            j = self._hash(item, i)
            min_count = min(min_count, self.table[i, j])
        return int(min_count)

    def merge(self, other: 'CountMinSketch') -> 'CountMinSketch':
        """
        Merge two sketches (for distributed computing).

        Args:
            other: Another sketch to merge

        Returns:
            New merged sketch
        """
        if (self.config.width != other.config.width or
            self.config.depth != other.config.depth):
            raise ValueError("Sketches must have same dimensions to merge")

        merged = CountMinSketch(self.config)
        merged.table = self.table + other.table
        merged.total_count = self.total_count + other.total_count
        return merged

    def inner_product(self, other: 'CountMinSketch') -> int:
        """
        Estimate inner product of two frequency vectors.

        Args:
            other: Another sketch

        Returns:
            Estimated inner product
        """
        if (self.config.width != other.config.width or
            self.config.depth != other.config.depth):
            raise ValueError("Sketches must have same dimensions")

        min_product = float('inf')
        for i in range(self.config.depth):
            row_product = np.sum(self.table[i] * other.table[i])
            min_product = min(min_product, row_product)
        return int(min_product)

    def heavy_hitters(self, threshold: float) -> List[Tuple[Any, int]]:
        """
        Find heavy hitters (frequent items).

        Note: This requires storing seen items separately,
        as the sketch itself doesn't store items.

        Args:
            threshold: Frequency threshold (fraction of total)

        Returns:
            List of (item, count) for heavy hitters
        """
        # In practice, you'd track items separately
        # This is a placeholder showing the concept
        min_count = int(threshold * self.total_count)
        # Would return items with query(item) >= min_count
        return []

    def __add__(self, other: 'CountMinSketch') -> 'CountMinSketch':
        """Operator overload for merging sketches."""
        return self.merge(other)


class CountMinSketchWithHeap:
    """
    Count-Min Sketch with min-heap for heavy hitters tracking.

    Maintains a heap of frequent items alongside the sketch.
    """

    def __init__(self, config: Optional[SketchConfig] = None, k: int = 100):
        """
        Initialize sketch with heavy hitters tracking.

        Args:
            config: Sketch configuration
            k: Number of heavy hitters to track
        """
        self.sketch = CountMinSketch(config)
        self.k = k
        self.heap: List[Tuple[int, Any]] = []  # Min-heap of (count, item)
        self.heap_items: Set[Any] = set()  # Items currently in heap

    def update(self, item: Any, count: int = 1):
        """Update sketch and heavy hitters."""
        self.sketch.update(item, count)
        estimated_count = self.sketch.query(item)

        # Update heap for heavy hitters
        if item in self.heap_items:
            # Update existing item in heap (rebuild for simplicity)
            self.heap = [(self.sketch.query(it), it)
                        for _, it in self.heap if it != item]
            self.heap.append((estimated_count, item))
            self.heap.sort()
        elif len(self.heap) < self.k:
            # Add to heap if not full
            self.heap.append((estimated_count, item))
            self.heap_items.add(item)
            self.heap.sort()
        elif estimated_count > self.heap[0][0]:
            # Replace minimum if new item is larger
            _, removed_item = self.heap[0]
            self.heap_items.remove(removed_item)
            self.heap[0] = (estimated_count, item)
            self.heap_items.add(item)
            self.heap.sort()

    def get_heavy_hitters(self) -> List[Tuple[Any, int]]:
        """Get current heavy hitters."""
        return [(item, count) for count, item in reversed(self.heap)]


class CountSketch:
    """
    Count Sketch - Alternative to Count-Min with unbiased estimates.

    Unlike Count-Min, Count Sketch can both over and underestimate,
    but provides unbiased estimates with bounded variance.
    """

    def __init__(self, width: int = 1000, depth: int = 5, seed: int = 42):
        """
        Initialize Count Sketch.

        Args:
            width: Number of counters per row
            depth: Number of hash functions
            seed: Random seed
        """
        self.width = width
        self.depth = depth
        self.seed = seed
        self.table = np.zeros((depth, width), dtype=np.int64)

    def _hash(self, item: Any, i: int) -> Tuple[int, int]:
        """
        Compute hash and sign for item.

        Returns:
            (position, sign) where sign is +1 or -1
        """
        if isinstance(item, str):
            item_bytes = item.encode('utf-8')
        else:
            item_bytes = str(item).encode('utf-8')

        # Position hash
        pos = mmh3.hash(item_bytes, self.seed + i, signed=False) % self.width
        # Sign hash
        sign = 1 if mmh3.hash(item_bytes, self.seed + i + self.depth) % 2 == 0 else -1

        return pos, sign

    def update(self, item: Any, count: int = 1):
        """Add item to sketch."""
        for i in range(self.depth):
            pos, sign = self._hash(item, i)
            self.table[i, pos] += sign * count

    def query(self, item: Any) -> int:
        """Query frequency estimate (median of estimates)."""
        estimates = []
        for i in range(self.depth):
            pos, sign = self._hash(item, i)
            estimates.append(sign * self.table[i, pos])
        return int(np.median(estimates))


def streaming_example():
    """Example: Real-time frequency counting in data streams."""
    print("=" * 60)
    print("COUNT-MIN SKETCH - STREAMING FREQUENCY COUNTING")
    print("=" * 60)

    # Create sketch with specific error bounds
    # 0.1% error rate with 99.9% confidence
    config = SketchConfig.from_error_prob(epsilon=0.001, delta=0.001)
    sketch = CountMinSketch(config)

    print(f"Sketch Configuration:")
    print(f"  Width: {config.width} counters per row")
    print(f"  Depth: {config.depth} hash functions")
    print(f"  Memory: ~{config.width * config.depth * 8 / 1024:.1f} KB")

    # Simulate data stream
    stream = ['apple'] * 100 + ['banana'] * 75 + ['cherry'] * 50 + \
             ['date'] * 25 + ['elderberry'] * 10 + \
             ['fig'] * 5 + ['grape'] * 3 + ['honeydew'] * 1

    import random
    random.shuffle(stream)

    print(f"\nProcessing stream of {len(stream)} items...")
    for item in stream:
        sketch.update(item)

    # Query frequencies
    items = ['apple', 'banana', 'cherry', 'date', 'elderberry',
             'fig', 'grape', 'honeydew', 'kiwi']

    print("\nFrequency Estimates:")
    print(f"{'Item':<12} {'True':<8} {'Estimated':<12} {'Error':<8}")
    print("-" * 40)

    true_counts = {'apple': 100, 'banana': 75, 'cherry': 50,
                  'date': 25, 'elderberry': 10, 'fig': 5,
                  'grape': 3, 'honeydew': 1, 'kiwi': 0}

    for item in items:
        estimated = sketch.query(item)
        true_count = true_counts.get(item, 0)
        error = estimated - true_count
        print(f"{item:<12} {true_count:<8} {estimated:<12} {error:<8}")


def network_monitoring_example():
    """Example: Network traffic monitoring."""
    print("\n" + "=" * 60)
    print("NETWORK TRAFFIC MONITORING")
    print("=" * 60)

    # Track heavy hitters (top IPs by packet count)
    sketch = CountMinSketchWithHeap(
        config=SketchConfig.from_error_prob(0.001, 0.001),
        k=5  # Track top 5 IPs
    )

    # Simulate network traffic
    print("Simulating network traffic...")

    # Some IPs are more active (simulating DDoS or heavy users)
    traffic_distribution = {
        '192.168.1.1': 5000,    # Heavy user
        '10.0.0.1': 3000,       # Heavy user
        '172.16.0.1': 2000,     # Moderate
        '192.168.1.2': 1000,    # Moderate
        '10.0.0.2': 500,        # Light
    }

    # Add many more IPs with light traffic
    for i in range(3, 100):
        traffic_distribution[f'192.168.1.{i}'] = random.randint(1, 100)

    # Process packets
    total_packets = 0
    for ip, count in traffic_distribution.items():
        for _ in range(count):
            sketch.update(ip)
            total_packets += 1

    print(f"Total packets processed: {total_packets}")

    # Get heavy hitters
    print("\nTop 5 IPs by traffic volume:")
    print(f"{'Rank':<6} {'IP Address':<15} {'Packets':<10} {'% Traffic':<10}")
    print("-" * 45)

    for rank, (ip, count) in enumerate(sketch.get_heavy_hitters()[:5], 1):
        percentage = (count / total_packets) * 100
        print(f"{rank:<6} {ip:<15} {count:<10} {percentage:.1f}%")


def database_optimization_example():
    """Example: Database query optimization."""
    print("\n" + "=" * 60)
    print("DATABASE QUERY OPTIMIZATION")
    print("=" * 60)

    # Track frequency of query predicates
    sketch = CountMinSketch()

    # Simulate query log
    queries = [
        "user_id=123",
        "product_id=456",
        "user_id=123",
        "category='electronics'",
        "user_id=789",
        "product_id=456",
        "user_id=123",
        "date>'2024-01-01'",
        "product_id=456",
        "user_id=123",
    ] * 100  # Repeat pattern

    print("Processing query log...")
    for predicate in queries:
        sketch.update(predicate)

    # Identify candidates for indexing
    print("\nPredicate frequencies (for index selection):")
    unique_predicates = set(queries)

    frequencies = []
    for predicate in unique_predicates:
        freq = sketch.query(predicate)
        frequencies.append((freq, predicate))

    frequencies.sort(reverse=True)

    print(f"{'Predicate':<25} {'Frequency':<10} {'Index?':<10}")
    print("-" * 45)

    for freq, predicate in frequencies[:5]:
        should_index = "Yes" if freq > 100 else "No"
        print(f"{predicate:<25} {freq:<10} {should_index:<10}")


def distributed_counting_example():
    """Example: Distributed counting with sketch merging."""
    print("\n" + "=" * 60)
    print("DISTRIBUTED COUNTING")
    print("=" * 60)

    # Create sketches for different nodes
    config = SketchConfig.from_error_prob(0.01, 0.01)

    node1 = CountMinSketch(config)
    node2 = CountMinSketch(config)
    node3 = CountMinSketch(config)

    print("Simulating distributed word counting...")

    # Each node processes different parts of data
    node1_data = ['hello'] * 10 + ['world'] * 5 + ['foo'] * 3
    node2_data = ['hello'] * 8 + ['world'] * 12 + ['bar'] * 7
    node3_data = ['hello'] * 5 + ['foo'] * 9 + ['baz'] * 4

    for word in node1_data:
        node1.update(word)
    for word in node2_data:
        node2.update(word)
    for word in node3_data:
        node3.update(word)

    # Merge sketches
    merged = node1 + node2 + node3

    print("\nGlobal word frequencies:")
    words = ['hello', 'world', 'foo', 'bar', 'baz', 'missing']
    true_counts = {'hello': 23, 'world': 17, 'foo': 12, 'bar': 7, 'baz': 4, 'missing': 0}

    print(f"{'Word':<10} {'True':<8} {'Estimated':<12} {'Error':<8}")
    print("-" * 40)

    for word in words:
        estimated = merged.query(word)
        true = true_counts[word]
        error = estimated - true
        print(f"{word:<10} {true:<8} {estimated:<12} {error:<8}")


def count_sketch_comparison():
    """Compare Count-Min Sketch vs Count Sketch."""
    print("\n" + "=" * 60)
    print("COUNT-MIN vs COUNT SKETCH COMPARISON")
    print("=" * 60)

    # Same configuration for both
    width, depth = 1000, 5

    cm_sketch = CountMinSketch(SketchConfig(width=width, depth=depth))
    c_sketch = CountSketch(width=width, depth=depth)

    # Add items with varying frequencies
    items = {
        'common': 1000,
        'frequent': 500,
        'moderate': 100,
        'rare': 10,
        'very_rare': 1
    }

    for item, count in items.items():
        for _ in range(count):
            cm_sketch.update(item)
            c_sketch.update(item)

    print(f"{'Item':<12} {'True':<8} {'Count-Min':<12} {'Count Sketch':<12}")
    print("-" * 50)

    for item, true_count in items.items():
        cm_estimate = cm_sketch.query(item)
        c_estimate = c_sketch.query(item)
        print(f"{item:<12} {true_count:<8} {cm_estimate:<12} {c_estimate:<12}")

    # Test non-existent item
    print(f"{'never_seen':<12} {0:<8} {cm_sketch.query('never_seen'):<12} "
          f"{c_sketch.query('never_seen'):<12}")

    print("\nObservations:")
    print("- Count-Min always overestimates (one-sided error)")
    print("- Count Sketch can under/overestimate (two-sided error)")
    print("- Count Sketch gives unbiased estimates")


def memory_comparison():
    """Compare memory usage vs accuracy."""
    print("\n" + "=" * 60)
    print("MEMORY VS ACCURACY TRADE-OFF")
    print("=" * 60)

    # Different configurations
    configs = [
        (0.1, 0.1, "Low accuracy"),      # 10% error, 90% confidence
        (0.01, 0.01, "Medium accuracy"),  # 1% error, 99% confidence
        (0.001, 0.001, "High accuracy"),  # 0.1% error, 99.9% confidence
    ]

    print(f"{'Config':<20} {'Width':<10} {'Depth':<10} {'Memory (KB)':<15}")
    print("-" * 55)

    for epsilon, delta, name in configs:
        config = SketchConfig.from_error_prob(epsilon, delta)
        memory_kb = (config.width * config.depth * 8) / 1024
        print(f"{name:<20} {config.width:<10} {config.depth:<10} {memory_kb:<15.1f}")

    # Test accuracy with different configs
    print("\nAccuracy test with 1000 items:")

    test_data = ['item' + str(i % 100) for i in range(10000)]
    true_counts = defaultdict(int)
    for item in test_data:
        true_counts[item] += 1

    for epsilon, delta, name in configs:
        config = SketchConfig.from_error_prob(epsilon, delta)
        sketch = CountMinSketch(config)

        for item in test_data:
            sketch.update(item)

        # Calculate average error
        errors = []
        for item, true_count in true_counts.items():
            estimated = sketch.query(item)
            error_rate = (estimated - true_count) / true_count if true_count > 0 else 0
            errors.append(error_rate)

        avg_error = np.mean(errors) * 100
        max_error = np.max(errors) * 100

        print(f"\n{name}:")
        print(f"  Average error: {avg_error:.2f}%")
        print(f"  Max error: {max_error:.2f}%")


if __name__ == "__main__":
    # Run examples
    streaming_example()
    network_monitoring_example()
    database_optimization_example()
    distributed_counting_example()
    count_sketch_comparison()
    memory_comparison()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Count-Min Sketch provides space-efficient frequency estimation")
    print("- Always overestimates, never underestimates")
    print("- Error bounds: ε * total_count with probability 1-δ")
    print("- Mergeable for distributed systems")
    print("- Trade-off: accuracy vs memory usage")
    print("=" * 60)