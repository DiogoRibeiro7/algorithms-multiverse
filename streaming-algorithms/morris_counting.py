"""
Morris Counting Algorithm Implementation

Probabilistic counting algorithm that uses logarithmic space to approximately
count large numbers. Also known as approximate counting or probabilistic counting.

Key Features:
- Uses O(log log n) bits to count up to n
- Morris Algorithm (1978)
- Morris+ with improved accuracy
- Morris++ with variance reduction
- Applications in streaming and space-constrained systems

Author: Claude
Date: January 2026
"""

import random
import numpy as np
from typing import List, Optional, Tuple, Union
from dataclasses import dataclass, field
import math
from collections import defaultdict


class MorrisCounter:
    """
    Basic Morris Counter for approximate counting.

    Uses probabilistic increments to count with logarithmic space.
    Counter value X represents approximately 2^X - 1 events.
    """

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize Morris counter.

        Args:
            seed: Random seed for reproducibility
        """
        self.counter = 0
        self.random = random.Random(seed)

    def increment(self) -> None:
        """Increment the counter probabilistically."""
        # Probability of increment is 1 / 2^counter
        if self.random.random() < (1.0 / (1 << self.counter)):
            self.counter += 1

    def get_count(self) -> int:
        """
        Get the estimated count.

        Returns:
            Estimated number of events
        """
        return (1 << self.counter) - 1

    def get_raw_value(self) -> int:
        """Get raw counter value (for debugging)."""
        return self.counter

    def reset(self) -> None:
        """Reset the counter to zero."""
        self.counter = 0

    def merge(self, other: 'MorrisCounter') -> 'MorrisCounter':
        """
        Merge two Morris counters (approximate sum).

        Args:
            other: Another Morris counter

        Returns:
            New counter with merged count
        """
        # Approximate merging: take the larger counter
        # and probabilistically increment based on smaller
        merged = MorrisCounter()
        merged.counter = max(self.counter, other.counter)

        # Probabilistic adjustment for smaller counter
        smaller = min(self.counter, other.counter)
        for _ in range(smaller):
            if merged.random.random() < 0.5:
                merged.counter += 1

        return merged


class MorrisPlusCounter:
    """
    Morris+ Counter with improved accuracy.

    Uses a more sophisticated estimation formula for better accuracy.
    """

    def __init__(self, base: float = 2.0, seed: Optional[int] = None):
        """
        Initialize Morris+ counter.

        Args:
            base: Base for exponential growth (typically 2.0)
            seed: Random seed
        """
        self.counter = 0
        self.base = base
        self.random = random.Random(seed)

    def increment(self) -> None:
        """Increment counter with base-dependent probability."""
        prob = 1.0 / (self.base ** self.counter)
        if self.random.random() < prob:
            self.counter += 1

    def get_count(self) -> float:
        """
        Get estimated count with improved formula.

        Returns:
            Estimated count as float
        """
        return (self.base ** self.counter - 1) / (self.base - 1)

    def get_variance(self) -> float:
        """
        Get theoretical variance of the estimate.

        Returns:
            Variance of the count estimate
        """
        n = self.get_count()
        return n * (n + 1) / 2


class MorrisPlusPlusCounter:
    """
    Morris++ Counter with multiple counters for variance reduction.

    Maintains k independent Morris counters and averages their estimates.
    """

    def __init__(self, k: int = 8, base: float = 2.0, seed: Optional[int] = None):
        """
        Initialize Morris++ with k counters.

        Args:
            k: Number of independent counters
            base: Base for exponential growth
            seed: Random seed
        """
        self.k = k
        self.base = base
        self.counters = []
        random_gen = random.Random(seed)

        for i in range(k):
            counter_seed = random_gen.randint(0, 2**32) if seed else None
            self.counters.append(MorrisPlusCounter(base, counter_seed))

    def increment(self) -> None:
        """Increment all counters."""
        for counter in self.counters:
            counter.increment()

    def get_count(self) -> float:
        """
        Get averaged count estimate.

        Returns:
            Mean of all counter estimates
        """
        estimates = [counter.get_count() for counter in self.counters]
        return np.mean(estimates)

    def get_count_with_confidence(self, confidence: float = 0.95) -> Tuple[float, float, float]:
        """
        Get count with confidence interval.

        Args:
            confidence: Confidence level (e.g., 0.95 for 95%)

        Returns:
            Tuple of (estimate, lower_bound, upper_bound)
        """
        estimates = [counter.get_count() for counter in self.counters]
        mean = np.mean(estimates)
        std = np.std(estimates)

        # Calculate confidence interval
        z_score = 1.96 if confidence == 0.95 else 2.58  # 95% or 99%
        margin = z_score * std / np.sqrt(self.k)

        return mean, max(0, mean - margin), mean + margin


class AdaptiveMorrisCounter:
    """
    Adaptive Morris counter that adjusts precision based on count magnitude.
    """

    def __init__(self, initial_bits: int = 8, max_bits: int = 32):
        """
        Initialize adaptive counter.

        Args:
            initial_bits: Initial bit width
            max_bits: Maximum bit width
        """
        self.bits = initial_bits
        self.max_bits = max_bits
        self.counter = 0
        self.exact_count = 0  # Track exact count initially
        self.mode = "exact"  # "exact" or "morris"
        self.threshold = (1 << initial_bits) - 1

    def increment(self) -> None:
        """Increment with adaptive precision."""
        if self.mode == "exact":
            self.exact_count += 1
            if self.exact_count > self.threshold:
                # Switch to Morris mode
                self.mode = "morris"
                self.counter = int(np.log2(self.exact_count + 1))
        else:
            # Morris mode
            if random.random() < (1.0 / (1 << self.counter)):
                self.counter += 1

                # Check if we should increase precision
                if self.counter > self.bits and self.bits < self.max_bits:
                    self.bits = min(self.bits * 2, self.max_bits)
                    self.threshold = (1 << self.bits) - 1

    def get_count(self) -> int:
        """Get estimated count."""
        if self.mode == "exact":
            return self.exact_count
        else:
            return (1 << self.counter) - 1

    def get_info(self) -> dict:
        """Get counter information."""
        return {
            "mode": self.mode,
            "bits": self.bits,
            "count": self.get_count(),
            "raw_counter": self.counter if self.mode == "morris" else self.exact_count
        }


class DistributedMorrisCounter:
    """
    Distributed Morris counting across multiple nodes.
    """

    def __init__(self, num_nodes: int = 4):
        """
        Initialize distributed counter.

        Args:
            num_nodes: Number of distributed nodes
        """
        self.num_nodes = num_nodes
        self.node_counters = [MorrisPlusCounter() for _ in range(num_nodes)]

    def increment_at_node(self, node_id: int) -> None:
        """
        Increment counter at specific node.

        Args:
            node_id: Node identifier (0 to num_nodes-1)
        """
        if 0 <= node_id < self.num_nodes:
            self.node_counters[node_id].increment()

    def get_global_count(self) -> float:
        """
        Get global count across all nodes.

        Returns:
            Sum of all node estimates
        """
        return sum(counter.get_count() for counter in self.node_counters)

    def get_node_counts(self) -> List[float]:
        """Get individual node counts."""
        return [counter.get_count() for counter in self.node_counters]


class StreamingWordCounter:
    """
    Count word frequencies in a stream using Morris counters.
    """

    def __init__(self, max_words: int = 10000):
        """
        Initialize streaming word counter.

        Args:
            max_words: Maximum unique words to track
        """
        self.max_words = max_words
        self.word_counters = {}
        self.total_words = MorrisPlusCounter()

    def add_word(self, word: str) -> None:
        """Add a word to the stream."""
        # Update total count
        self.total_words.increment()

        # Update word-specific counter
        if word not in self.word_counters:
            if len(self.word_counters) < self.max_words:
                self.word_counters[word] = MorrisPlusCounter()
            else:
                return  # Ignore new words after limit

        self.word_counters[word].increment()

    def get_word_count(self, word: str) -> float:
        """Get estimated count for a word."""
        if word in self.word_counters:
            return self.word_counters[word].get_count()
        return 0

    def get_top_words(self, k: int = 10) -> List[Tuple[str, float]]:
        """Get top k most frequent words."""
        word_counts = [(word, counter.get_count())
                      for word, counter in self.word_counters.items()]
        word_counts.sort(key=lambda x: x[1], reverse=True)
        return word_counts[:k]

    def get_total_count(self) -> float:
        """Get total word count."""
        return self.total_words.get_count()


# Example usage and demonstrations
def example_basic_morris():
    """Demonstrate basic Morris counting."""
    print("=== Basic Morris Counter ===\n")

    counter = MorrisCounter(seed=42)
    actual_count = 1000

    print(f"Counting to {actual_count}...")
    for _ in range(actual_count):
        counter.increment()

    estimated = counter.get_count()
    raw_value = counter.get_raw_value()

    print(f"Actual count: {actual_count}")
    print(f"Estimated count: {estimated}")
    print(f"Raw counter value: {raw_value}")
    print(f"Error: {abs(estimated - actual_count) / actual_count * 100:.1f}%")
    print(f"Space used: {raw_value.bit_length()} bits vs {actual_count.bit_length()} bits for exact")


def example_morris_plus():
    """Compare Morris and Morris+ accuracy."""
    print("=== Morris vs Morris+ Comparison ===\n")

    test_counts = [100, 1000, 10000, 100000]
    num_trials = 100

    for actual_count in test_counts:
        morris_errors = []
        morris_plus_errors = []

        for _ in range(num_trials):
            # Basic Morris
            morris = MorrisCounter()
            for _ in range(actual_count):
                morris.increment()
            morris_estimate = morris.get_count()
            morris_errors.append(abs(morris_estimate - actual_count) / actual_count)

            # Morris+
            morris_plus = MorrisPlusCounter()
            for _ in range(actual_count):
                morris_plus.increment()
            morris_plus_estimate = morris_plus.get_count()
            morris_plus_errors.append(abs(morris_plus_estimate - actual_count) / actual_count)

        print(f"Count = {actual_count:,}")
        print(f"  Morris avg error: {np.mean(morris_errors) * 100:.1f}%")
        print(f"  Morris+ avg error: {np.mean(morris_plus_errors) * 100:.1f}%")


def example_morris_plus_plus():
    """Demonstrate variance reduction with Morris++."""
    print("=== Morris++ Variance Reduction ===\n")

    actual_count = 10000
    k_values = [1, 4, 8, 16]

    print(f"Counting to {actual_count} with different k values:\n")

    for k in k_values:
        errors = []
        for _ in range(50):  # Multiple trials
            counter = MorrisPlusPlusCounter(k=k, seed=random.randint(0, 10000))
            for _ in range(actual_count):
                counter.increment()

            estimate = counter.get_count()
            error = abs(estimate - actual_count) / actual_count
            errors.append(error)

        print(f"k = {k:2d} counters:")
        print(f"  Mean error: {np.mean(errors) * 100:.2f}%")
        print(f"  Std dev: {np.std(errors) * 100:.2f}%")
        print(f"  Space: {k * 8} bits")


def example_adaptive_counter():
    """Demonstrate adaptive Morris counter."""
    print("=== Adaptive Morris Counter ===\n")

    counter = AdaptiveMorrisCounter(initial_bits=8)

    checkpoints = [10, 100, 255, 256, 1000, 10000, 100000]
    current = 0

    for checkpoint in checkpoints:
        for _ in range(checkpoint - current):
            counter.increment()
        current = checkpoint

        info = counter.get_info()
        print(f"After {checkpoint:,} increments:")
        print(f"  Mode: {info['mode']}")
        print(f"  Estimated count: {info['count']:,}")
        print(f"  Error: {abs(info['count'] - checkpoint) / checkpoint * 100:.1f}%")
        print(f"  Bits used: {info['bits']}")
        print()


def example_distributed_counting():
    """Demonstrate distributed Morris counting."""
    print("=== Distributed Morris Counting ===\n")

    num_nodes = 4
    counter = DistributedMorrisCounter(num_nodes)

    # Simulate events at different nodes
    events_per_node = [5000, 3000, 4000, 2000]
    total_events = sum(events_per_node)

    print(f"Distributing {total_events} events across {num_nodes} nodes:")
    print(f"Events per node: {events_per_node}\n")

    for node_id, num_events in enumerate(events_per_node):
        for _ in range(num_events):
            counter.increment_at_node(node_id)

    node_counts = counter.get_node_counts()
    global_count = counter.get_global_count()

    print("Node estimates:")
    for i, (actual, estimated) in enumerate(zip(events_per_node, node_counts)):
        error = abs(estimated - actual) / actual * 100 if actual > 0 else 0
        print(f"  Node {i}: {estimated:.0f} (actual: {actual}, error: {error:.1f}%)")

    print(f"\nGlobal estimate: {global_count:.0f}")
    print(f"Actual total: {total_events}")
    print(f"Global error: {abs(global_count - total_events) / total_events * 100:.1f}%")


def example_stream_word_counting():
    """Demonstrate word frequency counting in streams."""
    print("=== Stream Word Frequency Counting ===\n")

    counter = StreamingWordCounter(max_words=100)

    # Simulate text stream with Zipf distribution
    words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I',
             'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at']

    # Generate stream following Zipf's law
    stream = []
    for i, word in enumerate(words):
        frequency = int(10000 / (i + 1))  # Zipf distribution
        stream.extend([word] * frequency)

    random.shuffle(stream)

    print(f"Processing {len(stream)} words...")
    for word in stream:
        counter.add_word(word)

    print(f"\nTotal words processed: {counter.get_total_count():.0f}")
    print("\nTop 10 words by estimated frequency:")
    print(f"{'Word':<10} {'Estimated':<12} {'Actual':<10} {'Error %':<10}")
    print("-" * 45)

    top_words = counter.get_top_words(10)
    for word, estimated in top_words:
        actual = stream.count(word)
        error = abs(estimated - actual) / actual * 100 if actual > 0 else 0
        print(f"{word:<10} {estimated:<12.0f} {actual:<10} {error:<10.1f}")


def example_memory_comparison():
    """Compare memory usage of different counting methods."""
    print("=== Memory Usage Comparison ===\n")

    counts = [1000, 10000, 100000, 1000000]

    print(f"{'Count':<12} {'Exact (bits)':<15} {'Morris (bits)':<15} {'Savings':<10}")
    print("-" * 55)

    for count in counts:
        # Exact counter needs log2(count) bits
        exact_bits = count.bit_length()

        # Morris counter needs log2(log2(count)) bits
        morris_counter = MorrisCounter()
        for _ in range(count):
            morris_counter.increment()
        morris_bits = morris_counter.get_raw_value().bit_length()

        savings = exact_bits / morris_bits if morris_bits > 0 else float('inf')

        print(f"{count:<12,} {exact_bits:<15} {morris_bits:<15} {savings:<10.1f}x")


if __name__ == "__main__":
    # Run all examples
    example_basic_morris()
    print("\n" + "=" * 60 + "\n")

    example_morris_plus()
    print("\n" + "=" * 60 + "\n")

    example_morris_plus_plus()
    print("\n" + "=" * 60 + "\n")

    example_adaptive_counter()
    print("\n" + "=" * 60 + "\n")

    example_distributed_counting()
    print("\n" + "=" * 60 + "\n")

    example_stream_word_counting()
    print("\n" + "=" * 60 + "\n")

    example_memory_comparison()

    print("\n" + "=" * 60)
    print("Key Insights:")
    print("=" * 60)
    print("""
1. Morris counting uses O(log log n) bits to count up to n,
   achieving exponential space savings for large counts.

2. The algorithm trades accuracy for space: typical error is
   around 30-50% for basic Morris, improving to 10-20% with Morris+.

3. Morris++ uses multiple counters to reduce variance through
   averaging, achieving better accuracy at the cost of more space.

4. Adaptive Morris counters can provide exact counts for small
   numbers and switch to approximate mode for larger values.

5. The algorithm is inherently distributed-friendly since counters
   can be maintained independently and merged approximately.

6. Real-world applications include:
   - Network packet counting
   - Database query result size estimation
   - Stream processing systems
   - Memory-constrained embedded systems

7. Morris counting is particularly useful when:
   - Exact counts aren't critical
   - Space is extremely limited
   - Counts can grow very large
   - Multiple counters are needed
    """)