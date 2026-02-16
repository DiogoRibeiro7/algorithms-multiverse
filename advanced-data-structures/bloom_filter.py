#!/usr/bin/env python3
"""
Bloom Filter Implementation

A Bloom Filter is a space-efficient probabilistic data structure designed to test
whether an element is a member of a set. It can have false positives but never
false negatives - if it says an element is NOT in the set, it definitely isn't.

Key Properties:
- Space-efficient: Uses bit array instead of storing actual elements
- Fast operations: O(k) for both insert and lookup (k = number of hash functions)
- No false negatives: If element not found, it's definitely not in the set
- Possible false positives: May say element exists when it doesn't
- No deletion: Standard bloom filter doesn't support removal

Time Complexity:
- Insert: O(k) where k is number of hash functions
- Query: O(k)
- Space: O(m) bits where m is filter size

Applications:
- Web crawlers (checking if URL already visited)
- Database systems (reducing disk lookups)
- Network routers (packet routing)
- Spell checkers (checking if word exists)
- Distributed systems (cache sharing)
- Bitcoin and blockchain (transaction validation)

Author: Algorithms Multiverse
License: MIT
"""

import hashlib
import math
import mmh3  # MurmurHash3 for better distribution
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional, Union, Tuple
from bitarray import bitarray


class BloomFilter:
    """
    Bloom Filter for probabilistic membership testing

    Uses multiple hash functions to map elements to bit positions.
    Provides configurable false positive rate.

    Attributes:
        size: Size of bit array
        num_hashes: Number of hash functions
        bit_array: Internal bit array
        count: Number of elements added
        expected_elements: Expected number of elements
        false_positive_rate: Target false positive probability
    """

    def __init__(self, expected_elements: int = 10000,
                 false_positive_rate: float = 0.01):
        """
        Initialize Bloom Filter with optimal parameters

        Args:
            expected_elements: Expected number of elements to store
            false_positive_rate: Desired false positive probability (0-1)
        """
        self.expected_elements = expected_elements
        self.false_positive_rate = false_positive_rate

        # Calculate optimal size and number of hash functions
        self.size = self._optimal_size(expected_elements, false_positive_rate)
        self.num_hashes = self._optimal_num_hashes(self.size, expected_elements)

        # Initialize bit array
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

        self.count = 0

        print(f"Bloom Filter initialized:")
        print(f"  Expected elements: {expected_elements}")
        print(f"  False positive rate: {false_positive_rate:.2%}")
        print(f"  Bit array size: {self.size} bits ({self.size/8:.1f} bytes)")
        print(f"  Number of hash functions: {self.num_hashes}")
        print(f"  Bits per element: {self.size/expected_elements:.1f}")

    @staticmethod
    def _optimal_size(n: int, p: float) -> int:
        """
        Calculate optimal bit array size

        Formula: m = -n * ln(p) / (ln(2)^2)

        Args:
            n: Expected number of elements
            p: Desired false positive probability

        Returns:
            Optimal size in bits
        """
        m = -n * math.log(p) / (math.log(2) ** 2)
        return int(m)

    @staticmethod
    def _optimal_num_hashes(m: int, n: int) -> int:
        """
        Calculate optimal number of hash functions

        Formula: k = (m/n) * ln(2)

        Args:
            m: Size of bit array
            n: Expected number of elements

        Returns:
            Optimal number of hash functions
        """
        k = (m / n) * math.log(2)
        return max(1, int(k))

    def _hash(self, item: Union[str, int, bytes], seed: int) -> int:
        """
        Generate hash value for item with given seed

        Args:
            item: Item to hash
            seed: Seed for hash function

        Returns:
            Hash value modulo filter size
        """
        # Convert to bytes if necessary
        if isinstance(item, str):
            item = item.encode('utf-8')
        elif isinstance(item, int):
            item = str(item).encode('utf-8')

        # Use MurmurHash3 for better distribution
        hash_value = mmh3.hash(item, seed, signed=False)
        return hash_value % self.size

    def _get_hash_positions(self, item: Union[str, int, bytes]) -> List[int]:
        """
        Get all hash positions for an item

        Args:
            item: Item to hash

        Returns:
            List of bit positions
        """
        positions = []
        for i in range(self.num_hashes):
            pos = self._hash(item, i)
            positions.append(pos)
        return positions

    def add(self, item: Union[str, int, bytes]) -> None:
        """
        Add an item to the Bloom filter

        Args:
            item: Item to add
        """
        positions = self._get_hash_positions(item)
        for pos in positions:
            self.bit_array[pos] = 1
        self.count += 1

    def contains(self, item: Union[str, int, bytes]) -> bool:
        """
        Check if an item might be in the set

        Args:
            item: Item to check

        Returns:
            True if item might be in set (possible false positive)
            False if item definitely not in set (no false negatives)
        """
        positions = self._get_hash_positions(item)
        return all(self.bit_array[pos] for pos in positions)

    def __contains__(self, item: Union[str, int, bytes]) -> bool:
        """Support 'in' operator"""
        return self.contains(item)

    def get_load_factor(self) -> float:
        """
        Calculate the load factor (proportion of bits set to 1)

        Returns:
            Load factor between 0 and 1
        """
        return self.bit_array.count(1) / self.size

    def estimate_false_positive_rate(self) -> float:
        """
        Estimate current false positive rate based on load

        Formula: (1 - e^(-kn/m))^k

        Returns:
            Estimated false positive probability
        """
        k = self.num_hashes
        n = self.count
        m = self.size

        if n == 0:
            return 0

        # Formula: (1 - e^(-kn/m))^k
        fp_rate = (1 - math.exp(-k * n / m)) ** k
        return fp_rate

    def estimate_num_elements(self) -> int:
        """
        Estimate number of elements based on bit array state

        Formula: n ≈ -(m/k) * ln(1 - X/m)
        where X is number of set bits

        Returns:
            Estimated number of elements
        """
        X = self.bit_array.count(1)
        if X == 0:
            return 0
        if X == self.size:
            return self.expected_elements  # Saturated

        # Formula: n = -(m/k) * ln(1 - X/m)
        n = -(self.size / self.num_hashes) * math.log(1 - X / self.size)
        return int(n)

    def clear(self) -> None:
        """Clear the Bloom filter"""
        self.bit_array.setall(0)
        self.count = 0

    def union(self, other: 'BloomFilter') -> 'BloomFilter':
        """
        Create union of two Bloom filters (OR operation)

        Args:
            other: Another Bloom filter with same parameters

        Returns:
            New Bloom filter containing union
        """
        if self.size != other.size or self.num_hashes != other.num_hashes:
            raise ValueError("Bloom filters must have same parameters")

        result = BloomFilter.__new__(BloomFilter)
        result.size = self.size
        result.num_hashes = self.num_hashes
        result.expected_elements = self.expected_elements
        result.false_positive_rate = self.false_positive_rate
        result.bit_array = self.bit_array | other.bit_array
        result.count = self.count + other.count  # Approximate
        return result

    def intersection(self, other: 'BloomFilter') -> 'BloomFilter':
        """
        Create intersection of two Bloom filters (AND operation)

        Note: This gives approximate intersection with higher false positive rate

        Args:
            other: Another Bloom filter with same parameters

        Returns:
            New Bloom filter containing intersection
        """
        if self.size != other.size or self.num_hashes != other.num_hashes:
            raise ValueError("Bloom filters must have same parameters")

        result = BloomFilter.__new__(BloomFilter)
        result.size = self.size
        result.num_hashes = self.num_hashes
        result.expected_elements = self.expected_elements
        result.false_positive_rate = self.false_positive_rate
        result.bit_array = self.bit_array & other.bit_array
        result.count = min(self.count, other.count)  # Approximate
        return result

    def visualize(self, sample_size: int = 1000):
        """
        Visualize the bit array and statistics

        Args:
            sample_size: Size of visualization sample
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # 1. Bit array visualization
        ax1 = axes[0, 0]
        sample = min(sample_size, self.size)
        bits = [self.bit_array[i] for i in range(sample)]
        bit_matrix = np.array(bits).reshape(-1, min(100, sample))

        im1 = ax1.imshow(bit_matrix, cmap='RdYlGn_r', aspect='auto')
        ax1.set_title(f'Bit Array Visualization (first {sample} bits)')
        ax1.set_xlabel('Bit Position')
        ax1.set_ylabel('Row')
        plt.colorbar(im1, ax=ax1)

        # 2. Load distribution
        ax2 = axes[0, 1]
        chunk_size = self.size // 100
        chunks = []
        for i in range(0, self.size, chunk_size):
            chunk_load = self.bit_array[i:i+chunk_size].count(1) / min(chunk_size, self.size - i)
            chunks.append(chunk_load)

        ax2.bar(range(len(chunks)), chunks, color='steelblue')
        ax2.set_title('Load Distribution Across Filter')
        ax2.set_xlabel('Chunk Index')
        ax2.set_ylabel('Load Factor')
        ax2.axhline(y=0.5, color='r', linestyle='--', label='50% load')
        ax2.legend()

        # 3. Hash distribution
        ax3 = axes[1, 0]
        test_items = [f"test_{i}" for i in range(100)]
        all_positions = []
        for item in test_items:
            positions = self._get_hash_positions(item)
            all_positions.extend(positions)

        ax3.hist(all_positions, bins=50, color='green', alpha=0.7)
        ax3.set_title('Hash Function Distribution (100 test items)')
        ax3.set_xlabel('Bit Position')
        ax3.set_ylabel('Frequency')

        # 4. Statistics
        ax4 = axes[1, 1]
        ax4.axis('off')

        stats_text = f"""
        Bloom Filter Statistics:

        Size: {self.size} bits ({self.size/8:.1f} bytes)
        Hash Functions: {self.num_hashes}
        Elements Added: {self.count}
        Expected Elements: {self.expected_elements}

        Load Factor: {self.get_load_factor():.2%}
        Bits Set: {self.bit_array.count(1)} / {self.size}

        Target FP Rate: {self.false_positive_rate:.4%}
        Current FP Rate: {self.estimate_false_positive_rate():.4%}
        Estimated Elements: {self.estimate_num_elements()}
        """

        ax4.text(0.1, 0.5, stats_text, fontsize=10, verticalalignment='center',
                fontfamily='monospace')

        plt.suptitle('Bloom Filter Analysis', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()


class CountingBloomFilter:
    """
    Counting Bloom Filter - supports deletion

    Uses counters instead of bits, allowing removal of elements
    at the cost of more space.
    """

    def __init__(self, expected_elements: int = 10000,
                 false_positive_rate: float = 0.01,
                 counter_bits: int = 4):
        """
        Initialize Counting Bloom Filter

        Args:
            expected_elements: Expected number of elements
            false_positive_rate: Target false positive rate
            counter_bits: Bits per counter (4 bits = max count 15)
        """
        self.expected_elements = expected_elements
        self.false_positive_rate = false_positive_rate
        self.counter_bits = counter_bits
        self.max_count = (1 << counter_bits) - 1

        # Calculate optimal parameters
        self.size = BloomFilter._optimal_size(expected_elements, false_positive_rate)
        self.num_hashes = BloomFilter._optimal_num_hashes(self.size, expected_elements)

        # Initialize counter array
        self.counters = np.zeros(self.size, dtype=np.uint8)
        self.count = 0

        print(f"\nCounting Bloom Filter initialized:")
        print(f"  Counter bits: {counter_bits} (max count: {self.max_count})")
        print(f"  Memory usage: {self.size * counter_bits / 8:.1f} bytes")

    def _hash(self, item: Union[str, int, bytes], seed: int) -> int:
        """Generate hash value"""
        if isinstance(item, str):
            item = item.encode('utf-8')
        elif isinstance(item, int):
            item = str(item).encode('utf-8')

        hash_value = mmh3.hash(item, seed, signed=False)
        return hash_value % self.size

    def add(self, item: Union[str, int, bytes]) -> None:
        """Add item to filter"""
        for i in range(self.num_hashes):
            pos = self._hash(item, i)
            if self.counters[pos] < self.max_count:
                self.counters[pos] += 1
        self.count += 1

    def remove(self, item: Union[str, int, bytes]) -> bool:
        """
        Remove item from filter

        Args:
            item: Item to remove

        Returns:
            True if item was possibly in filter, False if definitely not
        """
        # Check if item might be in filter
        positions = []
        for i in range(self.num_hashes):
            pos = self._hash(item, i)
            positions.append(pos)
            if self.counters[pos] == 0:
                return False  # Item definitely not in filter

        # Decrement counters
        for pos in positions:
            if self.counters[pos] > 0:
                self.counters[pos] -= 1

        self.count = max(0, self.count - 1)
        return True

    def contains(self, item: Union[str, int, bytes]) -> bool:
        """Check if item might be in filter"""
        for i in range(self.num_hashes):
            pos = self._hash(item, i)
            if self.counters[pos] == 0:
                return False
        return True


def demonstrate_bloom_filter():
    """Demonstrate Bloom filter operations"""
    print("=" * 60)
    print("Bloom Filter Demonstration")
    print("=" * 60)

    # Create Bloom filter
    bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)

    # Add some elements
    words = ["apple", "banana", "cherry", "date", "elderberry",
             "fig", "grape", "honeydew", "kiwi", "lemon"]

    print(f"\nAdding {len(words)} fruits to the filter...")
    for word in words:
        bf.add(word)

    # Test membership
    print("\nMembership tests:")
    test_words = ["apple", "banana", "orange", "mango", "kiwi", "watermelon"]
    for word in test_words:
        result = word in bf
        actual = word in words
        status = "✓" if result == actual else "FP" if result else "FN"
        print(f"  '{word}': {result} (actual: {actual}) [{status}]")

    # Statistics
    print(f"\nFilter statistics:")
    print(f"  Load factor: {bf.get_load_factor():.2%}")
    print(f"  Estimated FP rate: {bf.estimate_false_positive_rate():.4%}")
    print(f"  Estimated elements: {bf.estimate_num_elements()}")

    # Visualize
    bf.visualize()


def test_false_positive_rate():
    """Test actual vs theoretical false positive rate"""
    print("\n" + "=" * 60)
    print("False Positive Rate Analysis")
    print("=" * 60)

    target_rates = [0.001, 0.01, 0.05, 0.1]
    n_elements = 1000
    n_tests = 10000

    results = []

    for target_rate in target_rates:
        bf = BloomFilter(expected_elements=n_elements,
                        false_positive_rate=target_rate)

        # Add elements
        for i in range(n_elements):
            bf.add(f"element_{i}")

        # Test for false positives
        false_positives = 0
        for i in range(n_elements, n_elements + n_tests):
            if bf.contains(f"test_{i}"):
                false_positives += 1

        actual_rate = false_positives / n_tests
        results.append((target_rate, actual_rate))

        print(f"\nTarget FP rate: {target_rate:.1%}")
        print(f"  Actual FP rate: {actual_rate:.1%}")
        print(f"  Difference: {abs(actual_rate - target_rate):.1%}")

    # Visualize results
    plt.figure(figsize=(10, 6))
    target_rates_plot, actual_rates = zip(*results)

    x_pos = np.arange(len(target_rates_plot))
    width = 0.35

    plt.bar(x_pos - width/2, target_rates_plot, width, label='Target', alpha=0.8)
    plt.bar(x_pos + width/2, actual_rates, width, label='Actual', alpha=0.8)

    plt.xlabel('Configuration')
    plt.ylabel('False Positive Rate')
    plt.title('Target vs Actual False Positive Rates')
    plt.xticks(x_pos, [f"{r:.1%}" for r in target_rates_plot])
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def demonstrate_counting_bloom_filter():
    """Demonstrate counting Bloom filter with deletion"""
    print("\n" + "=" * 60)
    print("Counting Bloom Filter Demonstration")
    print("=" * 60)

    cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)

    # Add elements
    elements = ["alpha", "beta", "gamma", "delta", "epsilon"]
    print(f"\nAdding elements: {elements}")
    for elem in elements:
        cbf.add(elem)

    # Check membership
    print("\nInitial membership:")
    for elem in elements[:3]:
        print(f"  {elem}: {cbf.contains(elem)}")

    # Remove elements
    print(f"\nRemoving 'beta'...")
    cbf.remove("beta")

    print("\nMembership after removal:")
    for elem in elements[:3]:
        print(f"  {elem}: {cbf.contains(elem)}")

    # Add duplicate
    print(f"\nAdding 'alpha' again (duplicate)...")
    cbf.add("alpha")

    print(f"Removing 'alpha' once...")
    cbf.remove("alpha")

    print(f"'alpha' still in filter: {cbf.contains('alpha')}")

    print(f"Removing 'alpha' again...")
    cbf.remove("alpha")

    print(f"'alpha' still in filter: {cbf.contains('alpha')}")


def application_example_url_deduplication():
    """Example: URL deduplication in web crawler"""
    print("\n" + "=" * 60)
    print("Application: Web Crawler URL Deduplication")
    print("=" * 60)

    # Simulate web crawler
    bf = BloomFilter(expected_elements=1000000, false_positive_rate=0.001)

    # URLs to crawl
    urls = [
        "https://example.com",
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.org",
        "https://example.com",  # Duplicate
        "https://example.com/page3",
        "https://example.com/page1",  # Duplicate
    ]

    crawled = []
    skipped = []

    print("\nCrawling URLs:")
    for url in urls:
        if url not in bf:
            print(f"  Crawling: {url}")
            bf.add(url)
            crawled.append(url)
        else:
            print(f"  Skipping (already seen): {url}")
            skipped.append(url)

    print(f"\nResults:")
    print(f"  URLs crawled: {len(crawled)}")
    print(f"  URLs skipped: {len(skipped)}")
    print(f"  Memory used: {bf.size / 8:.1f} bytes")
    print(f"  (vs ~{sum(len(url) for url in crawled):.0f} bytes for storing URLs)")


if __name__ == "__main__":
    # Install required package if not available
    try:
        import mmh3
        import bitarray
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call(["pip", "install", "mmh3", "bitarray"])
        import mmh3
        from bitarray import bitarray

    # Run demonstrations
    demonstrate_bloom_filter()
    test_false_positive_rate()
    demonstrate_counting_bloom_filter()
    application_example_url_deduplication()

    print("\n" + "=" * 60)
    print("Bloom Filter Implementation Complete!")
    print("=" * 60)