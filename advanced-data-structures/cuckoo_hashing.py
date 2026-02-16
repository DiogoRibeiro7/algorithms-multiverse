"""
Cuckoo Hashing Implementation

A hash table with worst-case O(1) lookup time using two hash functions and two tables.
When a collision occurs, the existing element is "kicked out" and moved to its
alternative location, potentially triggering a chain of displacements.

Key Properties:
1. Worst-case O(1) lookup, delete
2. Expected O(1) insertion
3. Uses two hash functions and two tables (or one table with two positions)
4. Load factor typically kept below 50% for good performance
5. Rehashing when cycles detected during insertion

Advantages:
- Guaranteed constant-time lookup
- Simple lookup algorithm (check at most 2 locations)
- Good cache performance
- No clustering issues

Disadvantages:
- More complex insertion
- Lower space utilization (typically 50%)
- Possibility of insertion failure requiring rehash

Author: Algorithms Multiverse
Date: January 2026
"""

import random
import hashlib
from typing import Any, Optional, List, Tuple, Dict, Callable
from dataclasses import dataclass
from enum import Enum


class HashFunction:
    """Hash function generator for cuckoo hashing."""

    def __init__(self, seed: int, table_size: int):
        self.seed = seed
        self.table_size = table_size

    def __call__(self, key: Any) -> int:
        """Compute hash value for given key."""
        if isinstance(key, int):
            # For integers, use multiplication method
            hash_val = (key * 2654435761 + self.seed) % (2**32)
        elif isinstance(key, str):
            # For strings, use SHA256 with seed
            hash_input = f"{self.seed}:{key}".encode()
            hash_val = int(hashlib.sha256(hash_input).hexdigest(), 16)
        else:
            # For other types, use Python's hash with seed
            hash_val = hash(str(key) + str(self.seed))

        return hash_val % self.table_size


class CuckooHashTable:
    """
    Standard Cuckoo Hash Table with two hash functions.

    Uses a single array with two hash functions that map to different regions,
    or two separate arrays. This implementation uses a single array approach
    for better cache locality.

    Time Complexity:
    - Lookup: O(1) worst-case
    - Delete: O(1) worst-case
    - Insert: O(1) expected, O(n) worst-case (rehashing)

    Space Complexity: O(n) where n is the capacity
    """

    def __init__(self, initial_capacity: int = 16, max_iterations: int = 500):
        """
        Initialize Cuckoo Hash Table.

        Args:
            initial_capacity: Initial size of hash table
            max_iterations: Maximum displacements before rehashing
        """
        # Ensure capacity is even for two tables
        self.capacity = initial_capacity if initial_capacity % 2 == 0 else initial_capacity + 1
        self.size = 0
        self.max_iterations = max_iterations

        # Single array split into two logical tables
        self.keys: List[Optional[Any]] = [None] * self.capacity
        self.values: List[Optional[Any]] = [None] * self.capacity

        # Initialize hash functions
        self._init_hash_functions()

        # Statistics
        self.rehash_count = 0
        self.total_displacements = 0

    def _init_hash_functions(self):
        """Initialize two hash functions with random seeds."""
        half_size = self.capacity // 2
        seed1 = random.randint(0, 2**32 - 1)
        seed2 = random.randint(0, 2**32 - 1)

        # First hash maps to first half, second to second half
        self.hash1 = lambda key: HashFunction(seed1, half_size)(key)
        self.hash2 = lambda key: HashFunction(seed2, half_size)(key) + half_size

    def insert(self, key: Any, value: Any = None) -> bool:
        """
        Insert a key-value pair into the hash table.

        Args:
            key: Key to insert
            value: Value associated with key

        Returns:
            True if insertion successful, False if key already exists
        """
        if value is None:
            value = key

        # Check if key already exists
        if self.lookup(key) is not None:
            # Update existing key
            pos1, pos2 = self._get_positions(key)
            if self.keys[pos1] == key:
                self.values[pos1] = value
            elif self.keys[pos2] == key:
                self.values[pos2] = value
            return False

        # Try to insert using cuckoo process
        if self._insert_helper(key, value):
            return True

        # Insertion failed - need to rehash
        self._rehash()
        self._insert_helper(key, value)
        return True

    def _insert_helper(self, key: Any, value: Any) -> bool:
        """Helper method to insert without rehashing."""
        current_key = key
        current_value = value

        for _ in range(self.max_iterations):
            # Try position 1
            pos1 = self.hash1(current_key)
            if self.keys[pos1] is None:
                self.keys[pos1] = current_key
                self.values[pos1] = current_value
                self.size += 1
                return True

            # Kick out element at position 1
            current_key, self.keys[pos1] = self.keys[pos1], current_key
            current_value, self.values[pos1] = self.values[pos1], current_value
            self.total_displacements += 1

            # Try position 2 for kicked element
            pos2 = self.hash2(current_key)
            if self.keys[pos2] is None:
                self.keys[pos2] = current_key
                self.values[pos2] = current_value
                self.size += 1
                return True

            # Kick out element at position 2
            current_key, self.keys[pos2] = self.keys[pos2], current_key
            current_value, self.values[pos2] = self.values[pos2], current_value
            self.total_displacements += 1

        return False

    def lookup(self, key: Any) -> Optional[Any]:
        """
        Look up a key in the hash table.

        Args:
            key: Key to search for

        Returns:
            Value associated with key, or None if not found
        """
        pos1, pos2 = self._get_positions(key)

        if self.keys[pos1] == key:
            return self.values[pos1]
        elif self.keys[pos2] == key:
            return self.values[pos2]
        else:
            return None

    def delete(self, key: Any) -> bool:
        """
        Delete a key from the hash table.

        Args:
            key: Key to delete

        Returns:
            True if key was deleted, False if not found
        """
        pos1, pos2 = self._get_positions(key)

        if self.keys[pos1] == key:
            self.keys[pos1] = None
            self.values[pos1] = None
            self.size -= 1
            return True
        elif self.keys[pos2] == key:
            self.keys[pos2] = None
            self.values[pos2] = None
            self.size -= 1
            return True
        else:
            return False

    def _get_positions(self, key: Any) -> Tuple[int, int]:
        """Get the two possible positions for a key."""
        return self.hash1(key), self.hash2(key)

    def _rehash(self):
        """Rehash the table with new hash functions or larger size."""
        self.rehash_count += 1

        # Save old data
        old_keys = [(k, v) for k, v in zip(self.keys, self.values) if k is not None]

        # Increase capacity if load factor is high
        if self.size > self.capacity * 0.4:
            self.capacity *= 2

        # Reset table
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        old_size = self.size
        self.size = 0

        # Reinitialize hash functions
        self._init_hash_functions()

        # Reinsert all elements
        for key, value in old_keys:
            self._insert_helper(key, value)

    def get_load_factor(self) -> float:
        """Get the current load factor."""
        return self.size / self.capacity if self.capacity > 0 else 0

    def get_statistics(self) -> Dict[str, Any]:
        """Get hash table statistics."""
        return {
            'size': self.size,
            'capacity': self.capacity,
            'load_factor': self.get_load_factor(),
            'rehash_count': self.rehash_count,
            'total_displacements': self.total_displacements,
            'avg_displacements_per_insert': self.total_displacements / self.size if self.size > 0 else 0
        }

    def __contains__(self, key: Any) -> bool:
        """Check if key exists in hash table."""
        return self.lookup(key) is not None

    def __getitem__(self, key: Any) -> Any:
        """Get value for key."""
        value = self.lookup(key)
        if value is None:
            raise KeyError(f"Key '{key}' not found")
        return value

    def __setitem__(self, key: Any, value: Any):
        """Set value for key."""
        self.insert(key, value)

    def __delitem__(self, key: Any):
        """Delete key from hash table."""
        if not self.delete(key):
            raise KeyError(f"Key '{key}' not found")


class CuckooHashingWithStash(CuckooHashTable):
    """
    Cuckoo Hashing with a small stash to handle cycles.

    The stash is a small overflow area (typically 2-4 elements) that can
    store elements that couldn't be placed in the main table. This reduces
    the probability of rehashing significantly.
    """

    def __init__(self, initial_capacity: int = 16, max_iterations: int = 500, stash_size: int = 4):
        """
        Initialize Cuckoo Hash Table with stash.

        Args:
            initial_capacity: Initial size of hash table
            max_iterations: Maximum displacements before using stash
            stash_size: Size of stash for overflow elements
        """
        super().__init__(initial_capacity, max_iterations)
        self.stash_size = stash_size
        self.stash_keys: List[Optional[Any]] = [None] * stash_size
        self.stash_values: List[Optional[Any]] = [None] * stash_size

    def _insert_helper(self, key: Any, value: Any) -> bool:
        """Helper method to insert without rehashing, with stash support."""
        current_key = key
        current_value = value

        for _ in range(self.max_iterations):
            pos1 = self.hash1(current_key)
            if self.keys[pos1] is None:
                self.keys[pos1] = current_key
                self.values[pos1] = current_value
                self.size += 1
                return True

            current_key, self.keys[pos1] = self.keys[pos1], current_key
            current_value, self.values[pos1] = self.values[pos1], current_value
            self.total_displacements += 1

            pos2 = self.hash2(current_key)
            if self.keys[pos2] is None:
                self.keys[pos2] = current_key
                self.values[pos2] = current_value
                self.size += 1
                return True

            current_key, self.keys[pos2] = self.keys[pos2], current_key
            current_value, self.values[pos2] = self.values[pos2], current_value
            self.total_displacements += 1

        # Try to place in stash
        for i in range(self.stash_size):
            if self.stash_keys[i] is None:
                self.stash_keys[i] = current_key
                self.stash_values[i] = current_value
                self.size += 1
                return True

        return False

    def insert(self, key: Any, value: Any = None) -> bool:
        """Insert with stash support."""
        if value is None:
            value = key

        # Check if key exists in main table or stash
        existing_value = self.lookup(key)
        if existing_value is not None:
            # Update existing key
            pos1, pos2 = self._get_positions(key)
            if self.keys[pos1] == key:
                self.values[pos1] = value
            elif self.keys[pos2] == key:
                self.values[pos2] = value
            else:
                # Must be in stash
                for i in range(self.stash_size):
                    if self.stash_keys[i] == key:
                        self.stash_values[i] = value
                        break
            return False

        # Try to insert using helper
        if self._insert_helper(key, value):
            return True

        # Stash is full - need to rehash
        self._rehash()
        self._insert_helper(key, value)
        return True

    def lookup(self, key: Any) -> Optional[Any]:
        """Look up key in main table and stash."""
        # Check main table first
        value = super().lookup(key)
        if value is not None:
            return value

        # Check stash
        for i in range(self.stash_size):
            if self.stash_keys[i] == key:
                return self.stash_values[i]

        return None

    def delete(self, key: Any) -> bool:
        """Delete key from main table or stash."""
        # Try main table first
        if super().delete(key):
            return True

        # Check stash
        for i in range(self.stash_size):
            if self.stash_keys[i] == key:
                self.stash_keys[i] = None
                self.stash_values[i] = None
                self.size -= 1
                return True

        return False

    def _rehash(self):
        """Rehash including stash elements."""
        self.rehash_count += 1

        # Save old data including stash
        old_keys = [(k, v) for k, v in zip(self.keys, self.values) if k is not None]
        old_keys.extend([(k, v) for k, v in zip(self.stash_keys, self.stash_values) if k is not None])

        # Increase capacity if needed
        if self.size > self.capacity * 0.4:
            self.capacity *= 2

        # Reset everything
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.stash_keys = [None] * self.stash_size
        self.stash_values = [None] * self.stash_size
        old_size = self.size
        self.size = 0

        # Reinitialize hash functions
        self._init_hash_functions()

        # Reinsert all elements
        for key, value in old_keys:
            self._insert_helper(key, value)

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics including stash usage."""
        stats = super().get_statistics()
        stash_used = sum(1 for k in self.stash_keys if k is not None)
        stats.update({
            'stash_size': self.stash_size,
            'stash_used': stash_used,
            'stash_utilization': stash_used / self.stash_size if self.stash_size > 0 else 0
        })
        return stats


class CuckooFilter:
    """
    Cuckoo Filter - A space-efficient probabilistic data structure for membership testing.

    Similar to Bloom filters but supports deletion and has better lookup performance.
    Uses fingerprints instead of storing actual items.

    Properties:
    - False positive rate (configurable)
    - No false negatives
    - Supports deletion (unlike standard Bloom filters)
    - Better space efficiency than Bloom filters for low FPR
    """

    def __init__(self, capacity: int = 1000, fingerprint_size: int = 8, bucket_size: int = 4):
        """
        Initialize Cuckoo Filter.

        Args:
            capacity: Expected number of items
            fingerprint_size: Size of fingerprint in bits
            bucket_size: Number of entries per bucket
        """
        self.bucket_size = bucket_size
        self.fingerprint_size = fingerprint_size
        self.fingerprint_mask = (1 << fingerprint_size) - 1

        # Calculate number of buckets
        self.num_buckets = (capacity // bucket_size) + 1

        # Initialize buckets (each bucket holds multiple fingerprints)
        self.buckets = [[None for _ in range(bucket_size)] for _ in range(self.num_buckets)]

        self.size = 0
        self.max_kicks = 500

    def _fingerprint(self, item: Any) -> int:
        """Generate fingerprint for item."""
        hash_val = hash(str(item))
        return (hash_val & self.fingerprint_mask) or 1  # Ensure non-zero

    def _hash1(self, item: Any) -> int:
        """First hash function for bucket index."""
        return hash(str(item) + "h1") % self.num_buckets

    def _hash2(self, fp: int, i1: int) -> int:
        """Second hash function using fingerprint and first index."""
        hash_val = i1 ^ (hash(fp) * 0x9e3779b9)
        return hash_val % self.num_buckets

    def insert(self, item: Any) -> bool:
        """
        Insert an item into the filter.

        Returns:
            True if successful, False if filter is full
        """
        fp = self._fingerprint(item)
        i1 = self._hash1(item)
        i2 = self._hash2(fp, i1)

        # Try to insert in bucket 1
        for j in range(self.bucket_size):
            if self.buckets[i1][j] is None:
                self.buckets[i1][j] = fp
                self.size += 1
                return True

        # Try to insert in bucket 2
        for j in range(self.bucket_size):
            if self.buckets[i2][j] is None:
                self.buckets[i2][j] = fp
                self.size += 1
                return True

        # Both buckets full, need to kick out existing items
        i = i1 if random.random() < 0.5 else i2

        for _ in range(self.max_kicks):
            # Pick random entry to kick out
            j = random.randint(0, self.bucket_size - 1)
            fp, self.buckets[i][j] = self.buckets[i][j], fp

            # Calculate alternate location for kicked item
            i = self._hash2(fp, i)

            # Try to insert kicked item
            for j in range(self.bucket_size):
                if self.buckets[i][j] is None:
                    self.buckets[i][j] = fp
                    self.size += 1
                    return True

        # Filter is full
        return False

    def lookup(self, item: Any) -> bool:
        """Check if item might be in the filter."""
        fp = self._fingerprint(item)
        i1 = self._hash1(item)
        i2 = self._hash2(fp, i1)

        # Check both buckets
        return (fp in self.buckets[i1] or fp in self.buckets[i2])

    def delete(self, item: Any) -> bool:
        """
        Delete an item from the filter.

        Returns:
            True if item was deleted, False if not found
        """
        fp = self._fingerprint(item)
        i1 = self._hash1(item)
        i2 = self._hash2(fp, i1)

        # Try to delete from bucket 1
        for j in range(self.bucket_size):
            if self.buckets[i1][j] == fp:
                self.buckets[i1][j] = None
                self.size -= 1
                return True

        # Try to delete from bucket 2
        for j in range(self.bucket_size):
            if self.buckets[i2][j] == fp:
                self.buckets[i2][j] = None
                self.size -= 1
                return True

        return False

    def get_load_factor(self) -> float:
        """Get current load factor."""
        total_slots = self.num_buckets * self.bucket_size
        return self.size / total_slots if total_slots > 0 else 0

    def __contains__(self, item: Any) -> bool:
        """Check if item might be in filter."""
        return self.lookup(item)


def benchmark_cuckoo_hashing():
    """Benchmark different cuckoo hashing variants."""
    import time
    import random

    print("Cuckoo Hashing Benchmarks")
    print("=" * 50)

    sizes = [1000, 5000, 10000, 50000]

    for size in sizes:
        print(f"\nTesting with {size} items:")

        # Generate test data
        keys = list(range(size))
        random.shuffle(keys)
        values = [f"value_{k}" for k in keys]

        # Standard Cuckoo Hashing
        ch = CuckooHashTable(initial_capacity=size * 2)

        start = time.time()
        for k, v in zip(keys, values):
            ch.insert(k, v)
        insert_time = time.time() - start

        start = time.time()
        for k in keys[:1000]:
            _ = ch.lookup(k)
        lookup_time = (time.time() - start) * (size / 1000)

        stats = ch.get_statistics()
        print(f"\nStandard Cuckoo Hash:")
        print(f"  Insert time: {insert_time:.4f}s")
        print(f"  Lookup time: {lookup_time:.4f}s")
        print(f"  Load factor: {stats['load_factor']:.2%}")
        print(f"  Rehashes: {stats['rehash_count']}")
        print(f"  Avg displacements: {stats['avg_displacements_per_insert']:.2f}")

        # Cuckoo with Stash
        chs = CuckooHashingWithStash(initial_capacity=size * 2)

        start = time.time()
        for k, v in zip(keys, values):
            chs.insert(k, v)
        insert_time = time.time() - start

        start = time.time()
        for k in keys[:1000]:
            _ = chs.lookup(k)
        lookup_time = (time.time() - start) * (size / 1000)

        stats = chs.get_statistics()
        print(f"\nCuckoo Hash with Stash:")
        print(f"  Insert time: {insert_time:.4f}s")
        print(f"  Lookup time: {lookup_time:.4f}s")
        print(f"  Load factor: {stats['load_factor']:.2%}")
        print(f"  Rehashes: {stats['rehash_count']}")
        print(f"  Stash utilization: {stats['stash_utilization']:.2%}")

        # Python dict comparison
        d = {}
        start = time.time()
        for k, v in zip(keys, values):
            d[k] = v
        dict_insert = time.time() - start

        start = time.time()
        for k in keys[:1000]:
            _ = d[k]
        dict_lookup = (time.time() - start) * (size / 1000)

        print(f"\nPython dict (baseline):")
        print(f"  Insert time: {dict_insert:.4f}s")
        print(f"  Lookup time: {dict_lookup:.4f}s")

        # Cuckoo Filter
        cf = CuckooFilter(capacity=size)

        start = time.time()
        success = 0
        for k in keys:
            if cf.insert(k):
                success += 1
        filter_insert = time.time() - start

        start = time.time()
        for k in keys[:1000]:
            _ = k in cf
        filter_lookup = (time.time() - start) * (size / 1000)

        print(f"\nCuckoo Filter:")
        print(f"  Insert time: {filter_insert:.4f}s")
        print(f"  Lookup time: {filter_lookup:.4f}s")
        print(f"  Success rate: {success/size:.2%}")
        print(f"  Load factor: {cf.get_load_factor():.2%}")


def example_usage():
    """Demonstrate cuckoo hashing usage."""
    print("Cuckoo Hashing Examples")
    print("=" * 50)

    # Standard Cuckoo Hash Table
    print("\n1. Standard Cuckoo Hash Table:")
    ch = CuckooHashTable(initial_capacity=16)

    # Insert some items
    items = [("apple", 5), ("banana", 3), ("orange", 8),
             ("grape", 12), ("melon", 2), ("berry", 7)]

    for key, value in items:
        ch.insert(key, value)
        print(f"  Inserted: {key} -> {value}")

    # Lookup
    print("\nLookups:")
    for key in ["apple", "grape", "cherry"]:
        value = ch.lookup(key)
        print(f"  {key}: {value}")

    # Delete
    print("\nDelete 'banana':")
    ch.delete("banana")
    print(f"  After delete: {ch.lookup('banana')}")

    # Statistics
    print("\nStatistics:")
    stats = ch.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")

    # Cuckoo Hash with Stash
    print("\n2. Cuckoo Hash Table with Stash:")
    chs = CuckooHashingWithStash(initial_capacity=8, stash_size=2)

    # Insert more items to trigger stash usage
    for i in range(20):
        chs.insert(f"key_{i}", i * 10)

    stats = chs.get_statistics()
    print(f"  Items inserted: {stats['size']}")
    print(f"  Stash utilization: {stats['stash_utilization']:.0%}")
    print(f"  Rehash count: {stats['rehash_count']}")

    # Cuckoo Filter
    print("\n3. Cuckoo Filter (Probabilistic):")
    cf = CuckooFilter(capacity=100)

    # Insert items
    words = ["hello", "world", "cuckoo", "filter", "test"]
    for word in words:
        cf.insert(word)
        print(f"  Inserted: {word}")

    # Check membership
    print("\nMembership tests:")
    test_words = ["hello", "world", "python", "java"]
    for word in test_words:
        result = word in cf
        print(f"  '{word}' in filter: {result}")

    # Delete from filter
    print("\nDelete 'world':")
    cf.delete("world")
    print(f"  'world' in filter after delete: {'world' in cf}")

    print(f"\nFilter load factor: {cf.get_load_factor():.2%}")

    # Dictionary-style interface
    print("\n4. Dictionary-style Interface:")
    ch2 = CuckooHashTable()

    # Use like a dict
    ch2["name"] = "Alice"
    ch2["age"] = 30
    ch2["city"] = "New York"

    print(f"  Name: {ch2['name']}")
    print(f"  Age: {ch2['age']}")
    print(f"  'country' in table: {'country' in ch2}")

    del ch2["age"]
    print(f"  After deleting 'age': {'age' in ch2}")

    # Performance comparison
    print("\n5. Performance Characteristics:")
    print("  Operation     | Cuckoo Hash | Regular Hash | Chaining")
    print("  --------------|-------------|--------------|----------")
    print("  Lookup        | O(1) worst  | O(1) average | O(n) worst")
    print("  Insert        | O(1) amort. | O(1) average | O(1) average")
    print("  Delete        | O(1) worst  | O(1) average | O(n) worst")
    print("  Space         | ~50% load   | ~75% load    | >100% possible")
    print("  Cache misses  | ≤2          | 1 average    | Variable")


if __name__ == "__main__":
    # Run examples
    example_usage()

    # Run benchmarks
    print("\n" + "=" * 50)
    benchmark_cuckoo_hashing()