"""
Reservoir Sampling and Stream Sampling Algorithms
=================================================

Implementations of algorithms for sampling from data streams of unknown
or very large size, using constant memory.

Includes:
- Simple Reservoir Sampling (Algorithm R)
- Weighted Reservoir Sampling
- Reservoir Sampling with Replacement
- Stratified Reservoir Sampling
- Sliding Window Sampling
- Priority Sampling

Author: Claude
Date: January 2026
"""

import random
import heapq
import numpy as np
from typing import Any, List, Optional, Tuple, Callable, Dict
from dataclasses import dataclass
from collections import defaultdict, deque
import math


@dataclass
class WeightedItem:
    """Item with associated weight for weighted sampling."""
    item: Any
    weight: float
    key: float = 0.0  # Random key for priority sampling


class ReservoirSampling:
    """
    Simple Reservoir Sampling (Algorithm R).

    Maintains a uniform random sample of k items from a stream
    of unknown size using O(k) memory.

    Each item has equal probability k/n of being in the final sample.
    """

    def __init__(self, k: int, seed: Optional[int] = None):
        """
        Initialize reservoir sampler.

        Args:
            k: Size of the reservoir (number of samples to maintain)
            seed: Random seed for reproducibility
        """
        self.k = k
        self.reservoir = []
        self.n = 0  # Number of items seen

        if seed is not None:
            random.seed(seed)

    def add(self, item: Any):
        """
        Add an item to the stream.

        Args:
            item: Item to potentially add to reservoir
        """
        self.n += 1

        if len(self.reservoir) < self.k:
            # Reservoir not full, add item
            self.reservoir.append(item)
        else:
            # Randomly decide whether to include this item
            # Probability of inclusion = k/n
            j = random.randint(1, self.n)
            if j <= self.k:
                # Replace random item in reservoir
                self.reservoir[j - 1] = item

    def get_sample(self) -> List[Any]:
        """
        Get the current reservoir sample.

        Returns:
            List of sampled items
        """
        return self.reservoir.copy()

    def reset(self):
        """Reset the reservoir."""
        self.reservoir = []
        self.n = 0


class OptimizedReservoirSampling(ReservoirSampling):
    """
    Optimized Reservoir Sampling (Algorithm L).

    Uses geometric distribution to skip items, reducing random number generation.
    More efficient for large streams.
    """

    def __init__(self, k: int, seed: Optional[int] = None):
        """Initialize optimized reservoir sampler."""
        super().__init__(k, seed)
        self.W = math.exp(math.log(random.random()) / k)  # Initial W
        self.next_record = self.k + 1 + math.floor(math.log(random.random()) / math.log(1 - self.W))

    def add(self, item: Any):
        """Add item using optimized algorithm."""
        self.n += 1

        if len(self.reservoir) < self.k:
            # Fill reservoir initially
            self.reservoir.append(item)
        elif self.n == self.next_record:
            # Include this item
            self.reservoir[random.randint(0, self.k - 1)] = item

            # Calculate next record to include
            self.W = self.W * math.exp(math.log(random.random()) / self.k)
            self.next_record = self.n + math.floor(math.log(random.random()) / math.log(1 - self.W)) + 1


class WeightedReservoirSampling:
    """
    Weighted Reservoir Sampling (Algorithm A-Res).

    Samples items with probability proportional to their weights.
    Uses the exponential random key method.
    """

    def __init__(self, k: int, seed: Optional[int] = None):
        """
        Initialize weighted reservoir sampler.

        Args:
            k: Size of reservoir
            seed: Random seed
        """
        self.k = k
        self.reservoir = []  # Min-heap of (key, item, weight)

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

    def add(self, item: Any, weight: float):
        """
        Add weighted item to stream.

        Args:
            item: Item to add
            weight: Weight of the item (must be positive)
        """
        if weight <= 0:
            raise ValueError("Weight must be positive")

        # Generate random key: k_i = u_i^(1/w_i) where u_i ~ U(0,1)
        key = random.random() ** (1.0 / weight)

        if len(self.reservoir) < self.k:
            # Reservoir not full, add item
            heapq.heappush(self.reservoir, (key, item, weight))
        elif key > self.reservoir[0][0]:
            # Replace item with smallest key
            heapq.heapreplace(self.reservoir, (key, item, weight))

    def get_sample(self) -> List[Tuple[Any, float]]:
        """
        Get weighted sample.

        Returns:
            List of (item, weight) tuples
        """
        return [(item, weight) for _, item, weight in self.reservoir]


class WeightedReservoirSamplingChao:
    """
    Weighted Reservoir Sampling using Chao's algorithm.

    Alternative weighted sampling method that's simpler but less efficient.
    """

    def __init__(self, k: int, seed: Optional[int] = None):
        """Initialize Chao's weighted sampler."""
        self.k = k
        self.reservoir = []
        self.weights = []
        self.weight_sum = 0.0

        if seed is not None:
            random.seed(seed)

    def add(self, item: Any, weight: float):
        """Add weighted item."""
        if weight <= 0:
            return

        self.weight_sum += weight

        if len(self.reservoir) < self.k:
            # Reservoir not full
            self.reservoir.append(item)
            self.weights.append(weight)
        else:
            # Probability of inclusion
            prob = weight / self.weight_sum

            if random.random() < prob:
                # Include this item, replace random existing item
                # Choose item to replace proportional to weight
                cumsum = 0
                threshold = random.random() * (self.weight_sum - weight)

                for i in range(self.k):
                    cumsum += self.weights[i]
                    if cumsum > threshold:
                        self.reservoir[i] = item
                        self.weights[i] = weight
                        break

    def get_sample(self) -> List[Any]:
        """Get sample."""
        return self.reservoir.copy()


class ReservoirSamplingWithReplacement:
    """
    Reservoir Sampling with Replacement.

    Allows the same item to appear multiple times in the reservoir.
    """

    def __init__(self, k: int, seed: Optional[int] = None):
        """Initialize sampler with replacement."""
        self.k = k
        self.stream = []  # Store all items (memory-intensive!)
        self.sample_indices = []

        if seed is not None:
            random.seed(seed)

    def add(self, item: Any):
        """Add item to stream."""
        self.stream.append(item)

        # Sample k items with replacement
        n = len(self.stream)
        if n == 1:
            self.sample_indices = [0] * self.k
        else:
            # Each position independently samples from [0, n-1]
            for i in range(self.k):
                if random.random() < 1.0 / n:
                    self.sample_indices[i] = n - 1

    def get_sample(self) -> List[Any]:
        """Get sample with replacement."""
        if not self.stream:
            return []

        if len(self.stream) < self.k:
            # Not enough items, sample with replacement
            return [random.choice(self.stream) for _ in range(self.k)]

        return [self.stream[i] for i in self.sample_indices]


class StratifiedReservoirSampling:
    """
    Stratified Reservoir Sampling.

    Maintains separate reservoirs for different strata/categories.
    Ensures balanced sampling across categories.
    """

    def __init__(self, k_per_stratum: int, seed: Optional[int] = None):
        """
        Initialize stratified sampler.

        Args:
            k_per_stratum: Number of samples per stratum
            seed: Random seed
        """
        self.k_per_stratum = k_per_stratum
        self.strata = defaultdict(lambda: ReservoirSampling(k_per_stratum, seed))

        if seed is not None:
            random.seed(seed)

    def add(self, item: Any, stratum: str):
        """
        Add item to specific stratum.

        Args:
            item: Item to add
            stratum: Category/stratum identifier
        """
        self.strata[stratum].add(item)

    def get_sample(self) -> Dict[str, List[Any]]:
        """
        Get stratified sample.

        Returns:
            Dictionary mapping stratum to list of samples
        """
        return {
            stratum: sampler.get_sample()
            for stratum, sampler in self.strata.items()
        }

    def get_flat_sample(self) -> List[Tuple[str, Any]]:
        """
        Get flattened sample.

        Returns:
            List of (stratum, item) tuples
        """
        result = []
        for stratum, sampler in self.strata.items():
            for item in sampler.get_sample():
                result.append((stratum, item))
        return result


class SlidingWindowSampling:
    """
    Sliding Window Reservoir Sampling.

    Maintains a sample from the last W items in the stream.
    Useful for time-sensitive sampling.
    """

    def __init__(self, k: int, window_size: int, seed: Optional[int] = None):
        """
        Initialize sliding window sampler.

        Args:
            k: Sample size
            window_size: Size of sliding window
            seed: Random seed
        """
        self.k = k
        self.window_size = window_size
        self.window = deque(maxlen=window_size)
        self.reservoir = []

        if seed is not None:
            random.seed(seed)

    def add(self, item: Any):
        """Add item to sliding window."""
        self.window.append(item)

        # Resample from current window
        if len(self.window) <= self.k:
            self.reservoir = list(self.window)
        else:
            # Sample k items from window
            self.reservoir = random.sample(list(self.window), self.k)

    def get_sample(self) -> List[Any]:
        """Get current sample from window."""
        return self.reservoir.copy()


class PrioritySampling:
    """
    Priority Sampling (VarOpt Sampling).

    Provides unbiased estimates of subset sums with minimal variance.
    Each item gets a priority and top-k priorities are kept.
    """

    def __init__(self, k: int, seed: Optional[int] = None):
        """
        Initialize priority sampler.

        Args:
            k: Sample size
            seed: Random seed
        """
        self.k = k
        self.items = []  # Min-heap of (-priority, item, weight)
        self.tau = 0  # Threshold

        if seed is not None:
            random.seed(seed)

    def add(self, item: Any, weight: float = 1.0):
        """
        Add item with weight/value.

        Args:
            item: Item to add
            weight: Weight/value of item
        """
        if weight <= 0:
            return

        # Generate priority: w_i / u_i where u_i ~ U(0,1)
        priority = weight / random.random()

        if len(self.items) < self.k:
            heapq.heappush(self.items, (-priority, item, weight))
            if len(self.items) == self.k:
                # Reservoir full, set threshold
                self.tau = -self.items[0][0]
        elif priority > self.tau:
            # Replace item with smallest priority
            heapq.heapreplace(self.items, (-priority, item, weight))
            self.tau = -self.items[0][0]

    def get_sample(self) -> List[Tuple[Any, float]]:
        """
        Get priority sample.

        Returns:
            List of (item, adjusted_weight) tuples
        """
        if len(self.items) < self.k:
            # Not enough items
            return [(item, weight) for _, item, weight in self.items]

        # Adjust weights for unbiased estimation
        result = []
        for neg_priority, item, weight in self.items:
            priority = -neg_priority
            adjusted_weight = max(weight, self.tau)
            result.append((item, adjusted_weight))

        return result

    def estimate_sum(self) -> float:
        """
        Estimate sum of all weights seen.

        Returns:
            Unbiased estimate of total weight
        """
        sample = self.get_sample()
        return sum(weight for _, weight in sample)


class BiasedReservoirSampling:
    """
    Biased Reservoir Sampling.

    Allows custom bias function to prefer certain items.
    """

    def __init__(self, k: int, bias_func: Callable[[Any], float], seed: Optional[int] = None):
        """
        Initialize biased sampler.

        Args:
            k: Sample size
            bias_func: Function that returns bias score for each item
            seed: Random seed
        """
        self.k = k
        self.bias_func = bias_func
        self.reservoir = []  # Stores (score, item)

        if seed is not None:
            random.seed(seed)

    def add(self, item: Any):
        """Add item with bias."""
        # Calculate biased score
        bias = self.bias_func(item)
        score = random.random() * bias

        if len(self.reservoir) < self.k:
            self.reservoir.append((score, item))
        else:
            # Find minimum score
            min_idx = min(range(len(self.reservoir)), key=lambda i: self.reservoir[i][0])

            if score > self.reservoir[min_idx][0]:
                self.reservoir[min_idx] = (score, item)

    def get_sample(self) -> List[Any]:
        """Get biased sample."""
        return [item for _, item in self.reservoir]


class DistributedReservoirSampling:
    """
    Distributed Reservoir Sampling.

    Combines samples from multiple parallel streams.
    """

    def __init__(self, k: int):
        """
        Initialize distributed sampler.

        Args:
            k: Total sample size
        """
        self.k = k
        self.partitions = []

    def add_partition(self, items: List[Any], count: int):
        """
        Add a partition's reservoir.

        Args:
            items: Sampled items from partition
            count: Total items seen in partition
        """
        self.partitions.append((items, count))

    def merge(self) -> List[Any]:
        """
        Merge partitions into final sample.

        Returns:
            Combined sample of size k
        """
        # Collect all items with their inclusion probabilities
        all_items = []
        total_count = sum(count for _, count in self.partitions)

        for items, count in self.partitions:
            # Weight of each item from this partition
            weight = count / len(items) if items else 1

            for item in items:
                # Generate priority
                priority = random.random() ** (1.0 / weight)
                all_items.append((priority, item))

        # Sort by priority and take top k
        all_items.sort(reverse=True)
        return [item for _, item in all_items[:self.k]]


def example_usage():
    """Demonstrate reservoir sampling algorithms."""
    print("=" * 60)
    print("RESERVOIR SAMPLING ALGORITHMS")
    print("=" * 60)

    # Generate stream data
    stream = list(range(1000))
    k = 10

    # Example 1: Simple Reservoir Sampling
    print("\n1. Simple Reservoir Sampling:")
    print("-" * 40)

    rs = ReservoirSampling(k, seed=42)
    for item in stream:
        rs.add(item)

    sample = rs.get_sample()
    print(f"Stream size: {len(stream)}")
    print(f"Sample size: {k}")
    print(f"Sample: {sorted(sample)}")

    # Verify uniform distribution
    print("\n2. Distribution Test (10000 runs):")
    counts = defaultdict(int)
    for run in range(10000):
        rs = ReservoirSampling(k=1, seed=run)
        for item in range(10):
            rs.add(item)
        counts[rs.get_sample()[0]] += 1

    print("Item frequencies (should be ~1000 each):")
    for item in range(10):
        print(f"  Item {item}: {counts[item]}")

    # Example 3: Weighted Reservoir Sampling
    print("\n3. Weighted Reservoir Sampling:")
    print("-" * 40)

    wrs = WeightedReservoirSampling(k=5, seed=42)

    # Add items with different weights
    items_weights = [
        ("A", 1.0), ("B", 2.0), ("C", 3.0), ("D", 4.0),
        ("E", 5.0), ("F", 1.0), ("G", 2.0), ("H", 3.0)
    ]

    for item, weight in items_weights:
        wrs.add(item, weight)

    sample = wrs.get_sample()
    print("Items with weights:")
    for item, weight in items_weights:
        print(f"  {item}: weight = {weight}")
    print(f"\nWeighted sample: {[item for item, _ in sample]}")

    # Example 4: Stratified Sampling
    print("\n4. Stratified Reservoir Sampling:")
    print("-" * 40)

    srs = StratifiedReservoirSampling(k_per_stratum=3, seed=42)

    # Add items from different categories
    categories = {
        "category_A": range(0, 100),
        "category_B": range(100, 200),
        "category_C": range(200, 300)
    }

    for category, items in categories.items():
        for item in items:
            srs.add(item, category)

    stratified_sample = srs.get_sample()
    for stratum, sample in stratified_sample.items():
        print(f"  {stratum}: {sample[:5]}...")  # Show first 5

    # Example 5: Sliding Window Sampling
    print("\n5. Sliding Window Sampling:")
    print("-" * 40)

    window_size = 50
    sws = SlidingWindowSampling(k=5, window_size=window_size, seed=42)

    # Simulate streaming with concept drift
    for i in range(200):
        sws.add(i)

        if i % 50 == 49:
            sample = sws.get_sample()
            print(f"  After {i+1} items, window sample: {sorted(sample)}")

    # Example 6: Priority Sampling
    print("\n6. Priority Sampling:")
    print("-" * 40)

    ps = PrioritySampling(k=5, seed=42)

    # Add items with values
    values = [10, 20, 30, 40, 50, 5, 15, 25, 35, 45]
    for i, val in enumerate(values):
        ps.add(f"item_{i}", val)

    priority_sample = ps.get_sample()
    print("Items with values:")
    for i, val in enumerate(values):
        print(f"  item_{i}: {val}")

    print("\nPriority sample (with adjusted weights):")
    for item, weight in priority_sample:
        print(f"  {item}: {weight:.2f}")

    estimated_sum = ps.estimate_sum()
    actual_sum = sum(values)
    print(f"\nEstimated sum: {estimated_sum:.2f}")
    print(f"Actual sum: {actual_sum}")

    # Example 7: Optimized vs Simple Performance
    print("\n7. Performance Comparison:")
    print("-" * 40)

    import time

    stream_size = 1000000
    k = 100

    # Simple reservoir sampling
    start = time.time()
    simple = ReservoirSampling(k, seed=42)
    for i in range(stream_size):
        simple.add(i)
    simple_time = time.time() - start

    # Optimized reservoir sampling
    start = time.time()
    optimized = OptimizedReservoirSampling(k, seed=42)
    for i in range(stream_size):
        optimized.add(i)
    optimized_time = time.time() - start

    print(f"Stream size: {stream_size:,}")
    print(f"Sample size: {k}")
    print(f"Simple Algorithm R: {simple_time*1000:.2f} ms")
    print(f"Optimized Algorithm L: {optimized_time*1000:.2f} ms")
    print(f"Speedup: {simple_time/optimized_time:.2f}x")

    # Example 8: Biased Sampling
    print("\n8. Biased Reservoir Sampling:")
    print("-" * 40)

    # Bias towards larger numbers
    bias_func = lambda x: x + 1 if isinstance(x, int) else 1

    brs = BiasedReservoirSampling(k=10, bias_func=bias_func, seed=42)

    for i in range(100):
        brs.add(i)

    biased_sample = sorted(brs.get_sample())
    print(f"Biased sample (prefers larger numbers):")
    print(f"  {biased_sample}")
    print(f"  Mean: {np.mean(biased_sample):.2f} (vs 49.5 for uniform)")

    # Example 9: Distributed Sampling
    print("\n9. Distributed Reservoir Sampling:")
    print("-" * 40)

    drs = DistributedReservoirSampling(k=10)

    # Simulate 3 partitions
    partitions = [
        (list(range(0, 333)), 333),
        (list(range(333, 666)), 333),
        (list(range(666, 1000)), 334)
    ]

    for partition_items, count in partitions:
        # Each partition does its own sampling
        rs_partition = ReservoirSampling(k=10, seed=42)
        for item in partition_items:
            rs_partition.add(item)

        drs.add_partition(rs_partition.get_sample(), count)

    merged_sample = sorted(drs.merge())
    print(f"Merged sample from 3 partitions:")
    print(f"  {merged_sample}")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Reservoir sampling maintains uniform random sample")
    print("- O(k) memory for any stream size")
    print("- Weighted sampling for non-uniform probabilities")
    print("- Stratified sampling ensures category balance")
    print("- Priority sampling provides unbiased sum estimates")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()