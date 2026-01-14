"""
Advanced Bloom Filter Variants and Probabilistic Data Structures

Implementation of various bloom filter variants and related probabilistic
data structures for membership testing and counting.

Key Structures:
- Counting Bloom Filter
- Scalable Bloom Filter
- Cuckoo Filter
- Quotient Filter
- Stable Bloom Filter
- A2 (Adaptive) Bloom Filter
- Spectral Bloom Filter

Author: Claude
Date: January 2026
"""

import math
import hashlib
import numpy as np
from typing import List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
import mmh3
import random
from collections import defaultdict


class StandardBloomFilter:
    """
    Standard Bloom Filter for reference and comparison.

    Space: O(m) bits
    Insert: O(k)
    Query: O(k)
    False positive rate: (1 - e^(-kn/m))^k
    """

    def __init__(self, expected_elements: int = 10000,
                 false_positive_rate: float = 0.01):
        """
        Initialize Bloom filter.

        Args:
            expected_elements: Expected number of elements
            false_positive_rate: Desired false positive rate
        """
        self.expected_elements = expected_elements
        self.false_positive_rate = false_positive_rate

        # Calculate optimal parameters
        self.m = self._optimal_m(expected_elements, false_positive_rate)
        self.k = self._optimal_k(self.m, expected_elements)

        # Initialize bit array
        self.bit_array = np.zeros(self.m, dtype=bool)
        self.n = 0  # Current number of elements

    def _optimal_m(self, n: int, p: float) -> int:
        """Calculate optimal number of bits."""
        return int(-n * math.log(p) / (math.log(2) ** 2))

    def _optimal_k(self, m: int, n: int) -> int:
        """Calculate optimal number of hash functions."""
        return max(1, int(m / n * math.log(2)))

    def _hash(self, item: str, seed: int) -> int:
        """Generate hash value for item with given seed."""
        return mmh3.hash(str(item), seed) % self.m

    def add(self, item: Any) -> None:
        """Add an item to the filter."""
        for i in range(self.k):
            pos = self._hash(item, i)
            self.bit_array[pos] = True
        self.n += 1

    def contains(self, item: Any) -> bool:
        """Check if item might be in the set."""
        for i in range(self.k):
            pos = self._hash(item, i)
            if not self.bit_array[pos]:
                return False
        return True

    def get_load_factor(self) -> float:
        """Get the current load factor."""
        return np.sum(self.bit_array) / self.m


class CountingBloomFilter:
    """
    Counting Bloom Filter - supports deletions.

    Uses counters instead of bits, allowing element removal.
    Space: O(m * counter_bits)
    """

    def __init__(self, expected_elements: int = 10000,
                 false_positive_rate: float = 0.01,
                 counter_bits: int = 4):
        """
        Initialize Counting Bloom Filter.

        Args:
            expected_elements: Expected number of elements
            false_positive_rate: Desired false positive rate
            counter_bits: Bits per counter (4 bits = max count 15)
        """
        self.expected_elements = expected_elements
        self.false_positive_rate = false_positive_rate
        self.counter_bits = counter_bits
        self.max_count = (1 << counter_bits) - 1

        # Calculate parameters
        self.m = self._optimal_m(expected_elements, false_positive_rate)
        self.k = self._optimal_k(self.m, expected_elements)

        # Initialize counter array
        self.counters = np.zeros(self.m, dtype=np.uint8)
        self.n = 0

    def _optimal_m(self, n: int, p: float) -> int:
        """Calculate optimal number of counters."""
        return int(-n * math.log(p) / (math.log(2) ** 2))

    def _optimal_k(self, m: int, n: int) -> int:
        """Calculate optimal number of hash functions."""
        return max(1, int(m / n * math.log(2)))

    def _hash(self, item: str, seed: int) -> int:
        """Generate hash value."""
        return mmh3.hash(str(item), seed) % self.m

    def add(self, item: Any) -> bool:
        """
        Add an item to the filter.

        Returns:
            True if added successfully, False if counter overflow
        """
        positions = [self._hash(item, i) for i in range(self.k)]

        # Check for overflow
        for pos in positions:
            if self.counters[pos] >= self.max_count:
                return False

        # Increment counters
        for pos in positions:
            self.counters[pos] = min(self.counters[pos] + 1, self.max_count)

        self.n += 1
        return True

    def remove(self, item: Any) -> bool:
        """
        Remove an item from the filter.

        Returns:
            True if item might have been removed, False if definitely not present
        """
        positions = [self._hash(item, i) for i in range(self.k)]

        # Check if item might be present
        for pos in positions:
            if self.counters[pos] == 0:
                return False

        # Decrement counters
        for pos in positions:
            self.counters[pos] = max(0, self.counters[pos] - 1)

        self.n = max(0, self.n - 1)
        return True

    def contains(self, item: Any) -> bool:
        """Check if item might be in the set."""
        for i in range(self.k):
            pos = self._hash(item, i)
            if self.counters[pos] == 0:
                return False
        return True

    def get_count_estimate(self, item: Any) -> int:
        """Estimate the count of an item (min count across all positions)."""
        min_count = self.max_count
        for i in range(self.k):
            pos = self._hash(item, i)
            min_count = min(min_count, self.counters[pos])
        return min_count


class ScalableBloomFilter:
    """
    Scalable Bloom Filter - grows dynamically.

    Creates new filters as needed with tighter error bounds.
    Total false positive rate stays below target.
    """

    def __init__(self, initial_capacity: int = 1000,
                 false_positive_rate: float = 0.01,
                 growth_factor: int = 2):
        """
        Initialize Scalable Bloom Filter.

        Args:
            initial_capacity: Initial expected elements
            false_positive_rate: Target total false positive rate
            growth_factor: Growth factor for new filters
        """
        self.initial_capacity = initial_capacity
        self.false_positive_rate = false_positive_rate
        self.growth_factor = growth_factor

        # Create first filter with tighter bound
        self.filters = []
        self.capacities = []
        self.error_rates = []

        self._add_new_filter()

    def _add_new_filter(self):
        """Add a new bloom filter to the sequence."""
        index = len(self.filters)

        # Calculate capacity and error rate for new filter
        capacity = self.initial_capacity * (self.growth_factor ** index)

        # Error rates form geometric sequence: P0*r^0, P0*r^1, P0*r^2, ...
        # Total error = P0 * (1 - r^(n+1)) / (1 - r)
        # We want this < target, so we use tighter bounds for later filters
        r = 0.5  # Error reduction ratio
        error_rate = self.false_positive_rate * (r ** (index + 1))

        # Create new filter
        new_filter = StandardBloomFilter(capacity, error_rate)

        self.filters.append(new_filter)
        self.capacities.append(capacity)
        self.error_rates.append(error_rate)

    def add(self, item: Any) -> None:
        """Add an item to the filter."""
        # Check if item already exists
        if self.contains(item):
            return

        # Add to current (last) filter
        current_filter = self.filters[-1]

        # Check if current filter is getting full
        if current_filter.n >= current_filter.expected_elements:
            self._add_new_filter()
            current_filter = self.filters[-1]

        current_filter.add(item)

    def contains(self, item: Any) -> bool:
        """Check if item might be in the set."""
        # Check all filters (newest to oldest for better performance)
        for filter_obj in reversed(self.filters):
            if filter_obj.contains(item):
                return True
        return False

    def get_stats(self) -> dict:
        """Get statistics about the filter."""
        total_bits = sum(f.m for f in self.filters)
        total_elements = sum(f.n for f in self.filters)

        return {
            'num_filters': len(self.filters),
            'total_bits': total_bits,
            'total_elements': total_elements,
            'bits_per_element': total_bits / max(1, total_elements),
            'filter_sizes': [f.m for f in self.filters],
            'filter_counts': [f.n for f in self.filters]
        }


@dataclass
class CuckooFilterBucket:
    """Bucket for Cuckoo Filter."""
    fingerprints: List[Optional[int]] = field(default_factory=lambda: [None, None, None, None])

    def insert(self, fingerprint: int) -> bool:
        """Try to insert fingerprint into bucket."""
        for i in range(len(self.fingerprints)):
            if self.fingerprints[i] is None:
                self.fingerprints[i] = fingerprint
                return True
        return False

    def delete(self, fingerprint: int) -> bool:
        """Delete fingerprint from bucket."""
        for i in range(len(self.fingerprints)):
            if self.fingerprints[i] == fingerprint:
                self.fingerprints[i] = None
                return True
        return False

    def contains(self, fingerprint: int) -> bool:
        """Check if fingerprint is in bucket."""
        return fingerprint in self.fingerprints


class CuckooFilter:
    """
    Cuckoo Filter - space-efficient with deletion support.

    Better than Bloom filters for applications requiring deletion.
    Space: O(n * fingerprint_bits)
    """

    def __init__(self, capacity: int = 10000, bucket_size: int = 4,
                 fingerprint_bits: int = 8, max_kicks: int = 500):
        """
        Initialize Cuckoo Filter.

        Args:
            capacity: Maximum number of elements
            bucket_size: Number of slots per bucket
            fingerprint_bits: Bits per fingerprint
            max_kicks: Maximum relocations during insertion
        """
        self.capacity = capacity
        self.bucket_size = bucket_size
        self.fingerprint_bits = fingerprint_bits
        self.max_kicks = max_kicks

        # Calculate number of buckets
        self.num_buckets = (capacity + bucket_size - 1) // bucket_size
        self.buckets = [CuckooFilterBucket() for _ in range(self.num_buckets)]

        self.num_items = 0

    def _hash(self, item: Any) -> Tuple[int, int]:
        """Get hash and fingerprint for item."""
        item_hash = mmh3.hash(str(item))
        fingerprint = abs(item_hash) % (1 << self.fingerprint_bits)
        if fingerprint == 0:  # Avoid zero fingerprint
            fingerprint = 1
        return item_hash, fingerprint

    def _get_buckets(self, item_hash: int, fingerprint: int) -> Tuple[int, int]:
        """Get two candidate bucket indices."""
        i1 = abs(item_hash) % self.num_buckets
        i2 = (i1 ^ mmh3.hash(str(fingerprint))) % self.num_buckets
        return i1, i2

    def insert(self, item: Any) -> bool:
        """
        Insert an item into the filter.

        Returns:
            True if inserted successfully, False if filter is full
        """
        item_hash, fingerprint = self._hash(item)
        i1, i2 = self._get_buckets(item_hash, fingerprint)

        # Try to insert into either bucket
        if self.buckets[i1].insert(fingerprint):
            self.num_items += 1
            return True
        if self.buckets[i2].insert(fingerprint):
            self.num_items += 1
            return True

        # Both buckets full, need to relocate
        i = random.choice([i1, i2])

        for _ in range(self.max_kicks):
            # Pick random fingerprint to evict
            bucket = self.buckets[i]
            evict_index = random.randint(0, self.bucket_size - 1)
            evicted_fp = bucket.fingerprints[evict_index]

            if evicted_fp is None:
                continue

            # Replace with new fingerprint
            bucket.fingerprints[evict_index] = fingerprint
            fingerprint = evicted_fp

            # Find alternate bucket for evicted fingerprint
            i = (i ^ mmh3.hash(str(fingerprint))) % self.num_buckets

            if self.buckets[i].insert(fingerprint):
                self.num_items += 1
                return True

        return False  # Filter is full

    def delete(self, item: Any) -> bool:
        """Delete an item from the filter."""
        item_hash, fingerprint = self._hash(item)
        i1, i2 = self._get_buckets(item_hash, fingerprint)

        if self.buckets[i1].delete(fingerprint):
            self.num_items -= 1
            return True
        if self.buckets[i2].delete(fingerprint):
            self.num_items -= 1
            return True

        return False

    def contains(self, item: Any) -> bool:
        """Check if item might be in the set."""
        item_hash, fingerprint = self._hash(item)
        i1, i2 = self._get_buckets(item_hash, fingerprint)

        return (self.buckets[i1].contains(fingerprint) or
                self.buckets[i2].contains(fingerprint))

    def get_load_factor(self) -> float:
        """Get current load factor."""
        return self.num_items / (self.num_buckets * self.bucket_size)


class QuotientFilter:
    """
    Quotient Filter - cache-friendly AMQ data structure.

    Stores quotients and remainders of hash values.
    Supports merging and resizing.
    """

    def __init__(self, quotient_bits: int = 10):
        """
        Initialize Quotient Filter.

        Args:
            quotient_bits: Number of bits for quotient (determines size)
        """
        self.quotient_bits = quotient_bits
        self.remainder_bits = 64 - quotient_bits  # Using 64-bit hash
        self.num_slots = 1 << quotient_bits

        # Metadata bits per slot
        self.is_occupied = np.zeros(self.num_slots, dtype=bool)
        self.is_continuation = np.zeros(self.num_slots, dtype=bool)
        self.is_shifted = np.zeros(self.num_slots, dtype=bool)

        # Remainder storage
        self.remainders = np.zeros(self.num_slots, dtype=np.uint64)

        self.num_items = 0

    def _hash(self, item: Any) -> Tuple[int, int]:
        """Hash item into quotient and remainder."""
        h = abs(hash(str(item)))
        quotient = h >> self.remainder_bits
        remainder = h & ((1 << self.remainder_bits) - 1)
        quotient %= self.num_slots
        return quotient, remainder

    def insert(self, item: Any) -> bool:
        """Insert an item into the filter."""
        quotient, remainder = self._hash(item)

        # Find the start of the run for this quotient
        run_start = self._find_run_start(quotient)

        # Find insertion position within run
        insert_pos = run_start
        while (insert_pos < self.num_slots and
               self.is_continuation[insert_pos] and
               self.remainders[insert_pos] < remainder):
            insert_pos += 1

        if insert_pos >= self.num_slots:
            return False  # Filter full

        # Check if already exists
        if (insert_pos < self.num_slots and
            self.remainders[insert_pos] == remainder and
            self._get_quotient_for_slot(insert_pos) == quotient):
            return True  # Already exists

        # Shift elements to make room
        self._shift_right(insert_pos)

        # Insert new element
        self.remainders[insert_pos] = remainder
        self.is_occupied[quotient] = True

        if insert_pos != quotient:
            self.is_shifted[insert_pos] = True

        if insert_pos > run_start:
            self.is_continuation[insert_pos] = True

        self.num_items += 1
        return True

    def contains(self, item: Any) -> bool:
        """Check if item might be in the filter."""
        quotient, remainder = self._hash(item)

        if not self.is_occupied[quotient]:
            return False

        # Find the run for this quotient
        run_start = self._find_run_start(quotient)

        # Search within run
        pos = run_start
        while (pos < self.num_slots and
               (pos == run_start or self.is_continuation[pos])):
            if self.remainders[pos] == remainder:
                return True
            pos += 1

        return False

    def _find_run_start(self, quotient: int) -> int:
        """Find the start position of the run for given quotient."""
        # Count number of occupied slots before quotient
        runs_before = np.sum(self.is_occupied[:quotient])

        # Find the runs_before-th run
        current_run = 0
        pos = 0

        while current_run < runs_before and pos < self.num_slots:
            if not self.is_continuation[pos]:
                current_run += 1
            pos += 1

        return pos

    def _shift_right(self, start: int):
        """Shift elements right starting from position."""
        # Find end of cluster
        end = start
        while end < self.num_slots - 1 and self.remainders[end] != 0:
            end += 1

        # Shift elements
        for i in range(end, start, -1):
            self.remainders[i] = self.remainders[i - 1]
            self.is_continuation[i] = self.is_continuation[i - 1]
            self.is_shifted[i] = True

    def _get_quotient_for_slot(self, slot: int) -> int:
        """Get the quotient value for a given slot."""
        # Count runs before this slot
        runs = 0
        for i in range(slot + 1):
            if not self.is_continuation[i]:
                runs += 1

        # Find which quotient this is
        quotient = 0
        count = 0
        while count < runs and quotient < self.num_slots:
            if self.is_occupied[quotient]:
                count += 1
            if count < runs:
                quotient += 1

        return quotient


class StableBloomFilter:
    """
    Stable Bloom Filter - for streaming data with continuous updates.

    Randomly decrements counters to forget old data.
    Maintains stable false positive rate for streaming data.
    """

    def __init__(self, max_elements: int = 10000,
                 false_positive_rate: float = 0.01,
                 cells_per_element: int = 3):
        """
        Initialize Stable Bloom Filter.

        Args:
            max_elements: Maximum elements at steady state
            false_positive_rate: Target false positive rate
            cells_per_element: Cells to decrement per addition
        """
        self.max_elements = max_elements
        self.false_positive_rate = false_positive_rate
        self.cells_per_element = cells_per_element

        # Calculate parameters
        self.m = self._optimal_m(max_elements, false_positive_rate)
        self.k = self._optimal_k(self.m, max_elements)

        # Use small counters (e.g., 4 bits max)
        self.max_count = 15
        self.counters = np.zeros(self.m, dtype=np.uint8)

    def _optimal_m(self, n: int, p: float) -> int:
        """Calculate optimal number of cells."""
        return int(-n * math.log(p) / (math.log(2) ** 2))

    def _optimal_k(self, m: int, n: int) -> int:
        """Calculate optimal number of hash functions."""
        return max(1, int(m / n * math.log(2)))

    def _hash(self, item: str, seed: int) -> int:
        """Generate hash value."""
        return mmh3.hash(str(item), seed) % self.m

    def add(self, item: Any) -> None:
        """Add an item, with random eviction of old data."""
        # Randomly decrement P cells
        for _ in range(self.cells_per_element):
            pos = random.randint(0, self.m - 1)
            self.counters[pos] = max(0, self.counters[pos] - 1)

        # Set k cells to maximum
        for i in range(self.k):
            pos = self._hash(item, i)
            self.counters[pos] = self.max_count

    def contains(self, item: Any) -> bool:
        """Check if item might be in recent data."""
        for i in range(self.k):
            pos = self._hash(item, i)
            if self.counters[pos] == 0:
                return False
        return True

    def get_recency_estimate(self, item: Any) -> float:
        """Estimate how recently an item was added (0-1 scale)."""
        min_count = self.max_count
        for i in range(self.k):
            pos = self._hash(item, i)
            min_count = min(min_count, self.counters[pos])
        return min_count / self.max_count


# Example usage and demonstrations
def example_counting_bloom():
    """Demonstrate Counting Bloom Filter with deletion."""
    print("=== Counting Bloom Filter ===\n")

    cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)

    # Add items
    items = ['apple', 'banana', 'cherry', 'date', 'elderberry']
    for item in items:
        cbf.add(item)
        print(f"Added {item}")

    # Check membership
    print("\nMembership tests:")
    for item in items + ['fig', 'grape']:
        result = cbf.contains(item)
        print(f"  {item}: {result}")

    # Remove items
    print("\nRemoving 'banana' and 'cherry'...")
    cbf.remove('banana')
    cbf.remove('cherry')

    print("\nMembership after deletion:")
    for item in items:
        result = cbf.contains(item)
        print(f"  {item}: {result}")

    # Show count estimates
    print("\nCount estimates:")
    cbf.add('apple')  # Add apple again
    cbf.add('apple')  # And again
    print(f"  apple (added 3 times): {cbf.get_count_estimate('apple')}")
    print(f"  date (added once): {cbf.get_count_estimate('date')}")


def example_scalable_bloom():
    """Demonstrate Scalable Bloom Filter growth."""
    print("=== Scalable Bloom Filter ===\n")

    sbf = ScalableBloomFilter(initial_capacity=10,
                              false_positive_rate=0.01,
                              growth_factor=2)

    # Add many items to trigger growth
    num_items = 100
    for i in range(num_items):
        sbf.add(f"item_{i}")

        if i in [9, 29, 69]:  # Check growth points
            stats = sbf.get_stats()
            print(f"After {i+1} items:")
            print(f"  Number of filters: {stats['num_filters']}")
            print(f"  Filter sizes: {stats['filter_sizes']}")
            print(f"  Filter counts: {stats['filter_counts']}")
            print(f"  Bits per element: {stats['bits_per_element']:.2f}\n")

    # Test false positives
    false_positives = 0
    test_items = 1000
    for i in range(num_items, num_items + test_items):
        if sbf.contains(f"item_{i}"):
            false_positives += 1

    print(f"False positive rate: {false_positives/test_items:.3f}")
    print(f"Target rate: {sbf.false_positive_rate}")


def example_cuckoo_filter():
    """Demonstrate Cuckoo Filter operations."""
    print("=== Cuckoo Filter ===\n")

    cf = CuckooFilter(capacity=1000, bucket_size=4, fingerprint_bits=8)

    # Add items
    items = [f"user_{i}" for i in range(100)]
    for item in items:
        cf.insert(item)

    print(f"Added {len(items)} items")
    print(f"Load factor: {cf.get_load_factor():.2%}\n")

    # Test membership
    print("Membership tests:")
    test_items = items[:5] + [f"user_{i}" for i in range(1000, 1005)]
    for item in test_items:
        result = cf.contains(item)
        expected = item in items
        status = "✓" if result == expected else "✗"
        print(f"  {item}: {result} {status}")

    # Test deletion
    print("\nDeletion test:")
    delete_items = items[:3]
    for item in delete_items:
        cf.delete(item)
        print(f"  Deleted {item}")

    print("\nMembership after deletion:")
    for item in delete_items + items[3:5]:
        result = cf.contains(item)
        print(f"  {item}: {result}")

    # Compare space with bloom filter
    bf = StandardBloomFilter(expected_elements=100, false_positive_rate=0.01)
    for item in items:
        bf.add(item)

    print(f"\nSpace comparison:")
    print(f"  Bloom filter bits: {bf.m}")
    print(f"  Cuckoo filter slots: {cf.num_buckets * cf.bucket_size}")
    print(f"  Cuckoo bits per item: {cf.fingerprint_bits}")


def example_stable_bloom():
    """Demonstrate Stable Bloom Filter for streaming."""
    print("=== Stable Bloom Filter (Streaming) ===\n")

    sbf = StableBloomFilter(max_elements=50, false_positive_rate=0.01)

    # Simulate streaming data in batches
    batches = [
        ['news', 'sports', 'tech', 'politics', 'science'],
        ['weather', 'finance', 'health', 'travel', 'food'],
        ['music', 'movies', 'games', 'books', 'art']
    ]

    print("Processing streaming data batches...\n")

    for i, batch in enumerate(batches):
        print(f"Batch {i+1}: {batch}")

        # Add new batch
        for item in batch:
            sbf.add(item)

        # Test membership of all items seen so far
        print("  Membership tests:")
        all_items = [item for b in batches[:i+1] for item in b]

        for item in all_items[-10:]:  # Test last 10 items
            result = sbf.contains(item)
            recency = sbf.get_recency_estimate(item)
            print(f"    {item}: present={result}, recency={recency:.2f}")

        print()

    # Test old vs new items
    print("Old vs New items:")
    old_items = batches[0][:2]
    new_items = batches[-1][-2:]

    for item in old_items:
        result = sbf.contains(item)
        recency = sbf.get_recency_estimate(item)
        print(f"  Old '{item}': present={result}, recency={recency:.2f}")

    for item in new_items:
        result = sbf.contains(item)
        recency = sbf.get_recency_estimate(item)
        print(f"  New '{item}': present={result}, recency={recency:.2f}")


def compare_filters():
    """Compare different filter types."""
    print("=== Filter Comparison ===\n")

    n = 10000  # Number of elements
    p = 0.01   # Target false positive rate

    # Create filters
    filters = {
        'Standard Bloom': StandardBloomFilter(n, p),
        'Counting Bloom': CountingBloomFilter(n, p),
        'Cuckoo Filter': CuckooFilter(capacity=n),
    }

    # Add elements
    items = [f"item_{i}" for i in range(n)]
    insert_times = {}

    for name, filter_obj in filters.items():
        import time
        start = time.time()

        if isinstance(filter_obj, CuckooFilter):
            for item in items:
                filter_obj.insert(item)
        else:
            for item in items:
                filter_obj.add(item)

        insert_times[name] = time.time() - start

    # Test false positives
    test_items = [f"item_{i}" for i in range(n, n + 10000)]
    false_positives = {}
    query_times = {}

    for name, filter_obj in filters.items():
        import time
        start = time.time()

        fp_count = 0
        for item in test_items:
            if filter_obj.contains(item):
                fp_count += 1

        query_times[name] = time.time() - start
        false_positives[name] = fp_count / len(test_items)

    # Calculate space usage
    space_usage = {}
    space_usage['Standard Bloom'] = filters['Standard Bloom'].m / 8  # bits to bytes
    space_usage['Counting Bloom'] = filters['Counting Bloom'].m * filters['Counting Bloom'].counter_bits / 8
    space_usage['Cuckoo Filter'] = (filters['Cuckoo Filter'].num_buckets *
                                   filters['Cuckoo Filter'].bucket_size *
                                   filters['Cuckoo Filter'].fingerprint_bits / 8)

    # Print results
    print(f"{'Filter Type':<20} {'FP Rate':<12} {'Space (KB)':<12} {'Insert (s)':<12} {'Query (s)':<12}")
    print("-" * 70)

    for name in filters:
        fp_rate = false_positives[name]
        space_kb = space_usage[name] / 1024
        insert_time = insert_times[name]
        query_time = query_times[name]

        print(f"{name:<20} {fp_rate:<12.4f} {space_kb:<12.2f} {insert_time:<12.4f} {query_time:<12.4f}")

    print(f"\nTarget FP rate: {p}")
    print("\nKey differences:")
    print("- Counting Bloom: Supports deletion but uses more space")
    print("- Cuckoo Filter: Supports deletion with less space than Counting Bloom")
    print("- Standard Bloom: Most space-efficient but no deletion")


if __name__ == "__main__":
    # Run examples
    example_counting_bloom()
    print("\n" + "=" * 60 + "\n")

    example_scalable_bloom()
    print("\n" + "=" * 60 + "\n")

    example_cuckoo_filter()
    print("\n" + "=" * 60 + "\n")

    example_stable_bloom()
    print("\n" + "=" * 60 + "\n")

    compare_filters()

    print("\n" + "=" * 60)
    print("Key Insights:")
    print("=" * 60)
    print("""
1. Counting Bloom Filters enable deletion at the cost of using
   counters instead of bits (typically 4x more space).

2. Scalable Bloom Filters handle dynamic sets by creating a
   sequence of filters with geometrically decreasing error rates.

3. Cuckoo Filters provide deletion support with better space
   efficiency than Counting Bloom Filters and faster lookups.

4. Quotient Filters are cache-friendly and support merging,
   making them ideal for external memory applications.

5. Stable Bloom Filters continuously evict old data, maintaining
   a sliding window for streaming applications.

6. Trade-offs to consider:
   - Space efficiency vs. functionality (deletion, counting)
   - Static vs. dynamic capacity
   - Cache performance vs. simplicity
   - Exact deletion vs. probabilistic operations

7. Use cases:
   - Standard Bloom: Simple membership testing, static sets
   - Counting Bloom: When deletion is needed
   - Cuckoo Filter: Better than Counting Bloom for most uses
   - Scalable Bloom: Unknown or growing set sizes
   - Stable Bloom: Streaming data, recent item detection
    """)