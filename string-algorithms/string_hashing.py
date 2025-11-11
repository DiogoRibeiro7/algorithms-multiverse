"""
String Hashing Functions and Utilities
======================================

Comprehensive collection of string hashing algorithms for pattern matching,
similarity detection, and data structures.

Algorithms included:
1. Polynomial Rolling Hash (Rabin-Karp)
2. Multiple Hash Functions (for collision reduction)
3. Double Hashing
4. Zobrist Hashing for strings
5. Custom hash functions with different bases and moduli

Applications:
- Fast substring matching (Rabin-Karp algorithm)
- String comparison in O(1) after O(n) preprocessing
- Hash tables for strings
- Bloom filters
- String deduplication

Time Complexity:
- Single hash: O(n) to compute, O(1) to compare
- Rolling hash: O(1) per character update
- Multiple hashes: O(k) where k = number of hash functions

Space Complexity: O(1) per hash value
"""

import random
from typing import List, Tuple, Optional
import time


class StringHash:
    """
    Base class for string hashing algorithms.
    """

    @staticmethod
    def hash_string(s: str) -> int:
        """
        Simple polynomial hash function.

        Time: O(n)
        """
        hash_val = 0
        base = 31
        mod = 10**9 + 9

        for char in s:
            hash_val = (hash_val * base + ord(char)) % mod

        return hash_val

    @staticmethod
    def hash_substring(s: str, start: int, end: int) -> int:
        """
        Hash a substring s[start:end].

        Time: O(end - start)
        """
        hash_val = 0
        base = 31
        mod = 10**9 + 9

        for i in range(start, end):
            hash_val = (hash_val * base + ord(s[i])) % mod

        return hash_val


class RollingHash:
    """
    Rolling hash (Rabin-Karp) for efficient substring hashing.

    Allows O(1) hash updates when sliding a window through text.
    """

    def __init__(self, base: int = 31, mod: int = 10**9 + 9):
        """
        Initialize rolling hash parameters.

        Args:
            base: Base for polynomial hash
            mod: Modulus for hash values
        """
        self.base = base
        self.mod = mod
        self.base_pow = {}  # Cache for base powers

    def _get_base_pow(self, n: int) -> int:
        """Get base^n mod mod with caching."""
        if n not in self.base_pow:
            self.base_pow[n] = pow(self.base, n, self.mod)
        return self.base_pow[n]

    def hash_string(self, s: str) -> int:
        """
        Compute hash of entire string.

        Time: O(n)
        """
        hash_val = 0
        for char in s:
            hash_val = (hash_val * self.base + ord(char)) % self.mod
        return hash_val

    def roll_forward(self, old_hash: int, old_char: str, new_char: str,
                    window_size: int) -> int:
        """
        Update hash when sliding window forward.

        Remove old_char from left, add new_char to right.

        Time: O(1)
        """
        # Remove contribution of old_char
        hash_val = (old_hash - ord(old_char) * \
                   self._get_base_pow(window_size - 1)) % self.mod

        # Add new_char
        hash_val = (hash_val * self.base + ord(new_char)) % self.mod

        return hash_val

    def search_pattern(self, text: str, pattern: str) -> List[int]:
        """
        Search for pattern in text using rolling hash.

        Time: O(n + m) average, O(nm) worst case (with verification)

        Returns:
            List of starting positions where pattern occurs
        """
        n = len(text)
        m = len(pattern)

        if m > n:
            return []

        matches = []

        # Compute pattern hash
        pattern_hash = self.hash_string(pattern)

        # Compute hash of first window
        window_hash = self.hash_string(text[:m])

        # Check first window
        if window_hash == pattern_hash and text[:m] == pattern:
            matches.append(0)

        # Roll through text
        for i in range(1, n - m + 1):
            window_hash = self.roll_forward(
                window_hash,
                text[i - 1],
                text[i + m - 1],
                m
            )

            # Check if hashes match
            if window_hash == pattern_hash:
                # Verify actual substring to handle collisions
                if text[i:i + m] == pattern:
                    matches.append(i)

        return matches


class MultiHash:
    """
    Multiple hash functions to reduce collision probability.

    Uses k different hash functions with different bases.
    """

    def __init__(self, k: int = 3,
                bases: Optional[List[int]] = None,
                mods: Optional[List[int]] = None):
        """
        Initialize with k hash functions.

        Args:
            k: Number of hash functions
            bases: List of bases (generated if None)
            mods: List of moduli (generated if None)
        """
        self.k = k

        if bases is None:
            self.bases = [31, 37, 41, 43, 47, 53, 59, 61][:k]
        else:
            self.bases = bases

        if mods is None:
            self.mods = [
                10**9 + 7,
                10**9 + 9,
                10**9 + 21,
                10**9 + 33,
                10**9 + 87,
                10**9 + 93,
            ][:k]
        else:
            self.mods = mods

    def hash_string(self, s: str) -> List[int]:
        """
        Compute k hash values for string.

        Time: O(kn)

        Returns:
            List of k hash values
        """
        hashes = []

        for i in range(self.k):
            hash_val = 0
            base = self.bases[i]
            mod = self.mods[i]

            for char in s:
                hash_val = (hash_val * base + ord(char)) % mod

            hashes.append(hash_val)

        return hashes

    def compare(self, hashes1: List[int], hashes2: List[int]) -> bool:
        """
        Compare two sets of hash values.

        Time: O(k)

        Returns:
            True if all hashes match
        """
        return hashes1 == hashes2


class DoubleHash:
    """
    Double hashing for even better collision resistance.

    Uses two independent hash functions.
    """

    def __init__(self):
        self.base1 = 31
        self.mod1 = 10**9 + 7
        self.base2 = 37
        self.mod2 = 10**9 + 9

    def hash_string(self, s: str) -> Tuple[int, int]:
        """
        Compute both hash values.

        Time: O(n)

        Returns:
            Tuple of (hash1, hash2)
        """
        hash1 = 0
        hash2 = 0

        for char in s:
            hash1 = (hash1 * self.base1 + ord(char)) % self.mod1
            hash2 = (hash2 * self.base2 + ord(char)) % self.mod2

        return (hash1, hash2)

    def compare(self, h1: Tuple[int, int], h2: Tuple[int, int]) -> bool:
        """
        Compare two double hash values.

        Time: O(1)
        """
        return h1 == h2


class ZobristHash:
    """
    Zobrist hashing for strings (adapted from chess).

    Uses precomputed random values for each character at each position.
    """

    def __init__(self, max_length: int = 100, seed: Optional[int] = None):
        """
        Initialize Zobrist hash tables.

        Args:
            max_length: Maximum string length to support
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)

        self.max_length = max_length
        self.zobrist_table = {}

        # Generate random values for each (position, character) pair
        for pos in range(max_length):
            for c in range(256):  # ASCII characters
                self.zobrist_table[(pos, c)] = random.getrandbits(64)

    def hash_string(self, s: str) -> int:
        """
        Compute Zobrist hash.

        Time: O(n)
        """
        hash_val = 0

        for i, char in enumerate(s):
            if i >= self.max_length:
                break
            hash_val ^= self.zobrist_table[(i, ord(char))]

        return hash_val

    def update_character(self, old_hash: int, pos: int,
                        old_char: str, new_char: str) -> int:
        """
        Update hash when changing a character.

        Time: O(1)
        """
        # XOR out old character
        hash_val = old_hash ^ self.zobrist_table[(pos, ord(old_char))]

        # XOR in new character
        hash_val ^= self.zobrist_table[(pos, ord(new_char))]

        return hash_val


class PrecomputedHash:
    """
    Precompute all substring hashes for O(1) queries.

    Uses prefix hash array and base powers.
    """

    def __init__(self, text: str, base: int = 31, mod: int = 10**9 + 9):
        """
        Precompute hash values.

        Time: O(n)
        """
        self.text = text
        self.n = len(text)
        self.base = base
        self.mod = mod

        # Precompute prefix hashes
        self.prefix_hash = [0] * (self.n + 1)
        for i in range(self.n):
            self.prefix_hash[i + 1] = \
                (self.prefix_hash[i] * base + ord(text[i])) % mod

        # Precompute base powers
        self.base_pow = [1] * (self.n + 1)
        for i in range(self.n):
            self.base_pow[i + 1] = (self.base_pow[i] * base) % mod

    def substring_hash(self, start: int, end: int) -> int:
        """
        Get hash of substring text[start:end] in O(1).

        Time: O(1)
        """
        hash_val = (self.prefix_hash[end] -
                   self.prefix_hash[start] * self.base_pow[end - start]) % \
                   self.mod

        return hash_val

    def compare_substrings(self, start1: int, end1: int,
                          start2: int, end2: int) -> bool:
        """
        Compare two substrings in O(1).

        Time: O(1)

        Returns:
            True if substrings are equal
        """
        if end1 - start1 != end2 - start2:
            return False

        return self.substring_hash(start1, end1) == \
               self.substring_hash(start2, end2)


# ============================================================================
# APPLICATIONS AND UTILITIES
# ============================================================================

def find_duplicate_substrings(text: str, length: int) -> List[str]:
    """
    Find all duplicate substrings of given length using hashing.

    Time: O(n) average

    Args:
        text: Input text
        length: Substring length

    Returns:
        List of duplicate substrings
    """
    if length > len(text):
        return []

    seen = {}
    duplicates = set()
    rh = RollingHash()

    # Process all substrings
    for i in range(len(text) - length + 1):
        substring = text[i:i + length]
        hash_val = rh.hash_string(substring)

        if hash_val in seen:
            duplicates.add(substring)
        else:
            seen[hash_val] = substring

    return list(duplicates)


def longest_common_prefix_hash(s1: str, s2: str) -> int:
    """
    Find length of longest common prefix using binary search and hashing.

    Time: O(log n * log n) = O(log² n)

    Returns:
        Length of longest common prefix
    """
    n = min(len(s1), len(s2))

    if n == 0:
        return 0

    # Binary search on length
    left, right = 0, n

    rh = RollingHash()

    while left < right:
        mid = (left + right + 1) // 2

        hash1 = rh.hash_string(s1[:mid])
        hash2 = rh.hash_string(s2[:mid])

        if hash1 == hash2 and s1[:mid] == s2[:mid]:
            left = mid
        else:
            right = mid - 1

    return left


# ============================================================================
# BENCHMARKING AND TESTING
# ============================================================================

def benchmark_hash_functions():
    """Benchmark different hash functions."""
    print("=" * 70)
    print("Hash Function Performance Comparison")
    print("=" * 70)

    texts = [
        "short",
        "medium length text for testing",
        "a" * 1000,  # Long repetitive
        "The quick brown fox jumps over the lazy dog" * 20
    ]

    for text in texts:
        print(f"\nText length: {len(text)}")
        print("-" * 50)

        # Simple hash
        start = time.perf_counter()
        for _ in range(1000):
            StringHash.hash_string(text)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"Simple hash:    {elapsed:8.4f} ms (1000 iterations)")

        # Rolling hash
        rh = RollingHash()
        start = time.perf_counter()
        for _ in range(1000):
            rh.hash_string(text)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"Rolling hash:   {elapsed:8.4f} ms (1000 iterations)")

        # Multi-hash
        mh = MultiHash(k=3)
        start = time.perf_counter()
        for _ in range(1000):
            mh.hash_string(text)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"Multi-hash (3): {elapsed:8.4f} ms (1000 iterations)")

    print()


# ============================================================================
# EXAMPLES
# ============================================================================

def example_rolling_hash():
    print("=" * 70)
    print("EXAMPLE 1: Rolling Hash Pattern Matching")
    print("=" * 70)

    text = "the quick brown fox jumps over the lazy dog"
    pattern = "the"

    rh = RollingHash()
    matches = rh.search_pattern(text, pattern)

    print(f"Text: '{text}'")
    print(f"Pattern: '{pattern}'")
    print(f"Matches at positions: {matches}")

    for pos in matches:
        print(f"  Position {pos}: '{text[pos:pos+len(pattern)]}'")

    print()


def example_multi_hash():
    print("=" * 70)
    print("EXAMPLE 2: Multi-Hash Comparison")
    print("=" * 70)

    strings = ["hello", "hello", "world", "hello!", "helo"]

    mh = MultiHash(k=3)

    print("Computing hashes for strings:")
    hashes = {}
    for s in strings:
        h = mh.hash_string(s)
        hashes[s] = h
        print(f"  '{s}': {h}")

    print("\nComparing strings:")
    print(f"  'hello' == 'hello': {mh.compare(hashes['hello'], hashes['hello'])}")
    print(f"  'hello' == 'world': {mh.compare(hashes['hello'], hashes['world'])}")
    print(f"  'hello' == 'hello!': {mh.compare(hashes['hello'], hashes['hello!'])}")

    print()


def example_precomputed_hash():
    print("=" * 70)
    print("EXAMPLE 3: Precomputed Hash for Substring Queries")
    print("=" * 70)

    text = "abracadabra"
    ph = PrecomputedHash(text)

    print(f"Text: '{text}'")
    print("\nSubstring hashes (O(1) queries):")

    substrings = [(0, 4), (4, 7), (7, 11), (0, 3), (7, 10)]

    for start, end in substrings:
        hash_val = ph.substring_hash(start, end)
        print(f"  text[{start}:{end}] = '{text[start:end]}' -> {hash_val}")

    print("\nComparing substrings:")
    print(f"  text[0:3] == text[7:10]: {ph.compare_substrings(0, 3, 7, 10)}")

    print()


def example_find_duplicates():
    print("=" * 70)
    print("EXAMPLE 4: Find Duplicate Substrings")
    print("=" * 70)

    text = "banana republic banana split"
    length = 3

    duplicates = find_duplicate_substrings(text, length)

    print(f"Text: '{text}'")
    print(f"Looking for duplicates of length {length}")
    print(f"Found {len(duplicates)} duplicate substrings:")

    for dup in sorted(duplicates):
        print(f"  '{dup}'")

    print()


if __name__ == "__main__":
    print("=" * 70)
    print("STRING HASHING UTILITIES")
    print("=" * 70)
    print()

    example_rolling_hash()
    example_multi_hash()
    example_precomputed_hash()
    example_find_duplicates()
    benchmark_hash_functions()

    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
