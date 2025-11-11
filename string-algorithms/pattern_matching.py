"""
Comprehensive String Pattern Matching Algorithms
=================================================

This module implements six major pattern matching algorithms with detailed
explanations, preprocessing steps, performance analysis, and benchmarking.

Algorithms:
1. Knuth-Morris-Pratt (KMP)
2. Boyer-Moore
3. Rabin-Karp
4. Aho-Corasick (multiple pattern matching)
5. Z-algorithm
6. Manacher's algorithm (palindrome detection)

Features:
- All occurrences detection
- Unicode support
- Edge case handling
- Performance benchmarking
- Visualization of algorithm progress
"""

from typing import List, Tuple, Dict, Set
import time
from collections import deque, defaultdict


# ============================================================================
# 1. KNUTH-MORRIS-PRATT (KMP) ALGORITHM
# ============================================================================

class KMP:
    """
    Knuth-Morris-Pratt (KMP) Pattern Matching Algorithm
    ===================================================

    Time Complexity:
    - Preprocessing: O(m) where m = pattern length
    - Searching: O(n) where n = text length
    - Total: O(n + m)

    Space Complexity: O(m) for failure function table

    Real-world applications:
    - Text editors (Find functionality)
    - DNA sequence matching
    - Network packet inspection
    - Log file analysis

    Key Concept:
    Uses failure function to avoid re-examining text characters.
    When mismatch occurs, uses precomputed information to skip
    unnecessary comparisons.
    """

    @staticmethod
    def compute_lps(pattern: str) -> List[int]:
        """
        Compute Longest Proper Prefix which is also Suffix (LPS) array.

        LPS[i] = length of longest proper prefix of pattern[0:i+1]
                 that is also a suffix

        Example: pattern = "ABABC"
        LPS = [0, 0, 1, 2, 0]
        - "A" -> 0 (no proper prefix)
        - "AB" -> 0
        - "ABA" -> 1 ("A" is both prefix and suffix)
        - "ABAB" -> 2 ("AB" is both prefix and suffix)
        - "ABABC" -> 0

        Time: O(m), Space: O(m)
        """
        m = len(pattern)
        lps = [0] * m
        length = 0  # Length of previous longest prefix suffix
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    # Try shorter prefix
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        return lps

    @staticmethod
    def search(text: str, pattern: str, visualize: bool = False) -> List[int]:
        """
        Find all occurrences of pattern in text.

        Returns: List of starting indices where pattern is found

        Time: O(n + m), Space: O(m)
        """
        if not pattern or not text:
            return []

        n = len(text)
        m = len(pattern)

        if m > n:
            return []

        # Preprocessing
        lps = KMP.compute_lps(pattern)

        matches = []
        i = 0  # Index for text
        j = 0  # Index for pattern

        if visualize:
            print(f"\nKMP Algorithm Visualization:")
            print(f"Text:    {text}")
            print(f"Pattern: {pattern}")
            print(f"LPS:     {lps}\n")

        while i < n:
            if visualize and j == 0:
                print(f"Comparing at position {i}: '{text[i:i+m] if i+m <= n else text[i:]}'")

            if pattern[j] == text[i]:
                i += 1
                j += 1

            if j == m:
                # Pattern found
                matches.append(i - j)
                if visualize:
                    print(f"✓ Match found at index {i - j}")
                j = lps[j - 1]
            elif i < n and pattern[j] != text[i]:
                # Mismatch after j matches
                if j != 0:
                    if visualize:
                        print(f"  Mismatch at position {i}, using LPS to skip to j={lps[j-1]}")
                    j = lps[j - 1]
                else:
                    i += 1

        return matches


# ============================================================================
# 2. BOYER-MOORE ALGORITHM
# ============================================================================

class BoyerMoore:
    """
    Boyer-Moore Pattern Matching Algorithm
    ======================================

    Time Complexity:
    - Best case: O(n/m) - sublinear!
    - Worst case: O(n*m)
    - Average case: O(n)

    Space Complexity: O(|Σ|) where Σ is alphabet size

    Real-world applications:
    - GNU grep utility
    - Text editors with fast search
    - Antivirus signature matching

    Key Concepts:
    1. Bad Character Rule: Skip alignments based on mismatched character
    2. Good Suffix Rule: Skip based on matched suffix
    3. Searches from right to left in pattern
    """

    @staticmethod
    def bad_character_table(pattern: str) -> Dict[str, int]:
        """
        Build bad character table.

        For each character, stores rightmost occurrence in pattern.
        Used to shift pattern when mismatch occurs.

        Time: O(m + |Σ|), Space: O(|Σ|)
        """
        table = {}
        m = len(pattern)

        for i in range(m):
            table[pattern[i]] = i

        return table

    @staticmethod
    def good_suffix_table(pattern: str) -> List[int]:
        """
        Build good suffix table.

        For each position, stores how far to shift when
        suffix match fails at that position.

        Time: O(m), Space: O(m)
        """
        m = len(pattern)
        shift = [0] * (m + 1)
        border = [0] * (m + 1)

        # Preprocessing
        i = m
        j = m + 1
        border[i] = j

        while i > 0:
            while j <= m and pattern[i - 1] != pattern[j - 1]:
                if shift[j] == 0:
                    shift[j] = j - i
                j = border[j]

            i -= 1
            j -= 1
            border[i] = j

        # Case 2: Pattern suffix is prefix
        j = border[0]
        for i in range(m + 1):
            if shift[i] == 0:
                shift[i] = j
            if i == j:
                j = border[j]

        return shift

    @staticmethod
    def search(text: str, pattern: str, visualize: bool = False) -> List[int]:
        """
        Find all occurrences using Boyer-Moore algorithm.

        Time: O(n) average, O(n*m) worst case
        """
        if not pattern or not text:
            return []

        n = len(text)
        m = len(pattern)

        if m > n:
            return []

        # Preprocessing
        bad_char = BoyerMoore.bad_character_table(pattern)
        good_suffix = BoyerMoore.good_suffix_table(pattern)

        matches = []
        s = 0  # Shift of pattern with respect to text

        if visualize:
            print(f"\nBoyer-Moore Algorithm Visualization:")
            print(f"Text:    {text}")
            print(f"Pattern: {pattern}\n")

        while s <= n - m:
            j = m - 1

            if visualize:
                print(f"Checking at position {s}: '{text[s:s+m]}'")

            # Match from right to left
            while j >= 0 and pattern[j] == text[s + j]:
                j -= 1

            if j < 0:
                # Pattern found
                matches.append(s)
                if visualize:
                    print(f"✓ Match found at index {s}")
                s += good_suffix[0] if s + m < n else 1
            else:
                # Mismatch occurred
                bad_char_shift = j - bad_char.get(text[s + j], -1)
                good_suffix_shift = good_suffix[j + 1]
                shift = max(bad_char_shift, good_suffix_shift)

                if visualize:
                    print(f"  Mismatch at j={j}, shifting by {shift}")

                s += shift

        return matches


# ============================================================================
# 3. RABIN-KARP ALGORITHM
# ============================================================================

class RabinKarp:
    """
    Rabin-Karp Rolling Hash Algorithm
    ==================================

    Time Complexity:
    - Average case: O(n + m)
    - Worst case: O(n*m) when many hash collisions

    Space Complexity: O(1)

    Real-world applications:
    - Plagiarism detection
    - Multiple pattern matching
    - DNA sequence analysis
    - Document similarity

    Key Concept:
    Uses rolling hash to quickly compute hash values of
    all substrings of length m. Compares hashes first,
    then verifies with character comparison.
    """

    def __init__(self, base: int = 256, prime: int = 101):
        """
        Initialize with base for hashing and prime modulo.

        base: Base for polynomial rolling hash (usually 256 for ASCII)
        prime: Prime number for modulo to reduce collisions
        """
        self.base = base
        self.prime = prime

    def hash(self, s: str, length: int) -> int:
        """
        Compute hash value for string s[0:length].

        Hash = (s[0] * base^(length-1) + s[1] * base^(length-2) + ... + s[length-1]) % prime
        """
        h = 0
        for i in range(length):
            h = (h * self.base + ord(s[i])) % self.prime
        return h

    def search(self, text: str, pattern: str, visualize: bool = False) -> List[int]:
        """
        Find all occurrences using Rabin-Karp algorithm.

        Time: O(n + m) average, O(n*m) worst case
        """
        if not pattern or not text:
            return []

        n = len(text)
        m = len(pattern)

        if m > n:
            return []

        # Preprocessing
        pattern_hash = self.hash(pattern, m)
        text_hash = self.hash(text, m)

        # Highest power of base for rolling hash
        h = pow(self.base, m - 1, self.prime)

        matches = []

        if visualize:
            print(f"\nRabin-Karp Algorithm Visualization:")
            print(f"Text:    {text}")
            print(f"Pattern: {pattern}")
            print(f"Pattern hash: {pattern_hash}\n")

        for i in range(n - m + 1):
            if visualize:
                print(f"Position {i}: hash={text_hash}, substring='{text[i:i+m]}'")

            # Check hash match
            if pattern_hash == text_hash:
                # Verify character by character (handle hash collision)
                if text[i:i+m] == pattern:
                    matches.append(i)
                    if visualize:
                        print(f"  ✓ Match found at index {i}")
                elif visualize:
                    print(f"  ✗ Hash collision, not a real match")

            # Compute rolling hash for next window
            if i < n - m:
                # Remove leading character, add trailing character
                text_hash = (self.base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % self.prime

                # Handle negative hash
                if text_hash < 0:
                    text_hash += self.prime

        return matches


# ============================================================================
# 4. AHO-CORASICK ALGORITHM (MULTIPLE PATTERN MATCHING)
# ============================================================================

class AhoCorasick:
    """
    Aho-Corasick Multiple Pattern Matching Algorithm
    ================================================

    Time Complexity:
    - Preprocessing: O(sum of pattern lengths)
    - Searching: O(n + k) where k = number of matches

    Space Complexity: O(sum of pattern lengths)

    Real-world applications:
    - Antivirus scanning (multiple virus signatures)
    - Network intrusion detection
    - Content filtering
    - Bioinformatics (multiple gene sequences)

    Key Concept:
    Builds trie of patterns with failure links (similar to KMP).
    Can find all patterns in single pass through text.
    """

    class TrieNode:
        def __init__(self):
            self.children = {}
            self.output = []  # Patterns ending at this node
            self.fail = None  # Failure link

    def __init__(self):
        self.root = self.TrieNode()
        self.patterns = []

    def add_pattern(self, pattern: str, pattern_id: int = None):
        """
        Add pattern to trie.

        Time: O(m) where m = pattern length
        """
        if pattern_id is None:
            pattern_id = len(self.patterns)

        self.patterns.append(pattern)

        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = self.TrieNode()
            node = node.children[char]

        node.output.append(pattern_id)

    def build_failure_links(self):
        """
        Build failure links using BFS.

        Failure link points to longest proper suffix that is
        also a prefix of some pattern.

        Time: O(total pattern length)
        """
        queue = deque()

        # Set failure link for depth 1 nodes to root
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)

        # BFS to set failure links
        while queue:
            current = queue.popleft()

            for char, child in current.children.items():
                queue.append(child)

                # Find failure link
                fail_node = current.fail
                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail

                child.fail = fail_node.children[char] if fail_node else self.root

                # Add output from failure link
                child.output.extend(child.fail.output)

    def search(self, text: str, visualize: bool = False) -> Dict[int, List[int]]:
        """
        Find all occurrences of all patterns in text.

        Returns: Dict mapping pattern_id to list of starting indices

        Time: O(n + k) where k = number of matches
        """
        if not text:
            return {}

        # Ensure failure links are built
        if self.root.children and list(self.root.children.values())[0].fail is None:
            self.build_failure_links()

        results = defaultdict(list)
        current = self.root

        if visualize:
            print(f"\nAho-Corasick Algorithm Visualization:")
            print(f"Text: {text}")
            print(f"Patterns: {self.patterns}\n")

        for i, char in enumerate(text):
            # Follow failure links until we find match or reach root
            while current is not None and char not in current.children:
                current = current.fail

            if current is None:
                current = self.root
                continue

            current = current.children[char]

            # Check for pattern matches
            if current.output:
                for pattern_id in current.output:
                    pattern_len = len(self.patterns[pattern_id])
                    start_idx = i - pattern_len + 1
                    results[pattern_id].append(start_idx)

                    if visualize:
                        print(f"✓ Found pattern '{self.patterns[pattern_id]}' at index {start_idx}")

        return dict(results)


# ============================================================================
# 5. Z-ALGORITHM
# ============================================================================

class ZAlgorithm:
    """
    Z-Algorithm for Pattern Matching
    =================================

    Time Complexity: O(n + m)
    Space Complexity: O(n + m)

    Real-world applications:
    - Pattern matching (alternative to KMP)
    - String processing
    - Compression algorithms

    Key Concept:
    Z[i] = length of longest substring starting at i that is also
    a prefix of the string.

    Creates concatenation: pattern + "$" + text
    Then Z-values equal to pattern length indicate matches.
    """

    @staticmethod
    def compute_z_array(s: str) -> List[int]:
        """
        Compute Z-array for string s.

        Z[i] = length of longest substring starting from s[i]
               which is also a prefix of s

        Example: s = "aabcaabxaaz"
        Z = [11, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]

        Time: O(n), Space: O(n)
        """
        n = len(s)
        z = [0] * n
        z[0] = n

        # [l, r] is window where s[l:r+1] matches prefix
        l, r = 0, 0

        for i in range(1, n):
            if i > r:
                # Outside window, compute naively
                l, r = i, i
                while r < n and s[r - l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
            else:
                # Inside window, use previously computed values
                k = i - l
                if z[k] < r - i + 1:
                    z[i] = z[k]
                else:
                    l = i
                    while r < n and s[r - l] == s[r]:
                        r += 1
                    z[i] = r - l
                    r -= 1

        return z

    @staticmethod
    def search(text: str, pattern: str, visualize: bool = False) -> List[int]:
        """
        Find all occurrences using Z-algorithm.

        Time: O(n + m)
        """
        if not pattern or not text:
            return []

        n = len(text)
        m = len(pattern)

        if m > n:
            return []

        # Create concatenation with separator
        concat = pattern + "$" + text
        z = ZAlgorithm.compute_z_array(concat)

        matches = []

        if visualize:
            print(f"\nZ-Algorithm Visualization:")
            print(f"Text:    {text}")
            print(f"Pattern: {pattern}")
            print(f"Concatenation: {concat}")
            print(f"Z-array: {z}\n")

        # Find positions where Z-value equals pattern length
        for i in range(m + 1, len(concat)):
            if z[i] == m:
                match_pos = i - m - 1
                matches.append(match_pos)
                if visualize:
                    print(f"✓ Match found at index {match_pos} (Z[{i}] = {m})")

        return matches


# ============================================================================
# 6. MANACHER'S ALGORITHM (PALINDROME DETECTION)
# ============================================================================

class Manacher:
    """
    Manacher's Algorithm for Finding Palindromes
    ============================================

    Time Complexity: O(n)
    Space Complexity: O(n)

    Real-world applications:
    - DNA sequence analysis
    - Text compression
    - Finding repeated structures
    - Natural language processing

    Key Concept:
    Finds all palindromes in linear time using:
    1. Transform string to handle even/odd length palindromes uniformly
    2. Use previously computed palindrome information to avoid redundant checks
    """

    @staticmethod
    def preprocess(s: str) -> str:
        """
        Transform string to handle even/odd palindromes uniformly.

        Example: "aba" -> "#a#b#a#"

        This allows treating all palindromes as odd-length.
        """
        if not s:
            return "#"

        result = "#"
        for char in s:
            result += char + "#"
        return result

    @staticmethod
    def find_all_palindromes(s: str, visualize: bool = False) -> List[Tuple[int, int, str]]:
        """
        Find all palindromes in string.

        Returns: List of (start, end, palindrome_string) tuples

        Time: O(n)
        """
        if not s:
            return []

        # Preprocess string
        t = Manacher.preprocess(s)
        n = len(t)

        # p[i] = radius of palindrome centered at i
        p = [0] * n
        center = 0  # Center of rightmost palindrome
        right = 0   # Right boundary of rightmost palindrome

        if visualize:
            print(f"\nManacher's Algorithm Visualization:")
            print(f"Original: {s}")
            print(f"Transformed: {t}\n")

        for i in range(n):
            # Mirror of i with respect to center
            mirror = 2 * center - i

            if i < right:
                # Use previously computed information
                p[i] = min(right - i, p[mirror])

            # Try to expand palindrome centered at i
            try:
                while (i + p[i] + 1 < n and i - p[i] - 1 >= 0 and
                       t[i + p[i] + 1] == t[i - p[i] - 1]):
                    p[i] += 1
            except:
                pass

            # Update rightmost palindrome if necessary
            if i + p[i] > right:
                center = i
                right = i + p[i]

        # Extract palindromes
        palindromes = []
        for i in range(n):
            if p[i] > 0:
                # Convert back to original string indices
                start = (i - p[i]) // 2
                end = (i + p[i]) // 2
                if start < end:  # Skip single characters
                    palindrome_str = s[start:end]
                    palindromes.append((start, end, palindrome_str))

        if visualize:
            print("Palindromes found:")
            for start, end, pal in palindromes:
                print(f"  [{start}:{end}] = '{pal}'")

        return palindromes

    @staticmethod
    def longest_palindrome(s: str) -> str:
        """
        Find the longest palindromic substring.

        Time: O(n)
        """
        if not s:
            return ""

        t = Manacher.preprocess(s)
        n = len(t)
        p = [0] * n
        center = 0
        right = 0

        for i in range(n):
            mirror = 2 * center - i

            if i < right:
                p[i] = min(right - i, p[mirror])

            try:
                while (i + p[i] + 1 < n and i - p[i] - 1 >= 0 and
                       t[i + p[i] + 1] == t[i - p[i] - 1]):
                    p[i] += 1
            except:
                pass

            if i + p[i] > right:
                center = i
                right = i + p[i]

        # Find longest palindrome
        max_len = 0
        center_index = 0
        for i in range(n):
            if p[i] > max_len:
                max_len = p[i]
                center_index = i

        start = (center_index - max_len) // 2
        return s[start:start + max_len]


# ============================================================================
# BENCHMARKING AND PERFORMANCE COMPARISON
# ============================================================================

class PerformanceBenchmark:
    """
    Benchmark suite for comparing algorithm performance.
    """

    @staticmethod
    def benchmark_single_pattern(text: str, pattern: str, iterations: int = 100):
        """
        Benchmark all single-pattern algorithms.
        """
        print(f"\n{'='*70}")
        print(f"PERFORMANCE BENCHMARK")
        print(f"{'='*70}")
        print(f"Text length: {len(text)}")
        print(f"Pattern length: {len(pattern)}")
        print(f"Iterations: {iterations}\n")

        algorithms = [
            ("KMP", lambda: KMP.search(text, pattern)),
            ("Boyer-Moore", lambda: BoyerMoore.search(text, pattern)),
            ("Rabin-Karp", lambda: RabinKarp().search(text, pattern)),
            ("Z-Algorithm", lambda: ZAlgorithm.search(text, pattern)),
        ]

        results = []

        for name, func in algorithms:
            start = time.perf_counter()
            for _ in range(iterations):
                matches = func()
            end = time.perf_counter()

            avg_time = (end - start) / iterations * 1000  # milliseconds
            results.append((name, avg_time, len(matches)))

            print(f"{name:15} | {avg_time:8.4f} ms | {len(matches)} matches")

        # Find best performer
        best = min(results, key=lambda x: x[1])
        print(f"\n✓ Fastest: {best[0]} ({best[1]:.4f} ms)")

        return results

    @staticmethod
    def benchmark_varying_sizes():
        """
        Benchmark with varying text and pattern sizes.
        """
        print(f"\n{'='*70}")
        print(f"SCALING PERFORMANCE TEST")
        print(f"{'='*70}\n")

        test_cases = [
            (100, 5),
            (1000, 10),
            (10000, 20),
            (100000, 50),
        ]

        for text_len, pattern_len in test_cases:
            # Generate test data
            text = "ABCABCABC" * (text_len // 9 + 1)
            text = text[:text_len]
            pattern = "ABC" * (pattern_len // 3 + 1)
            pattern = pattern[:pattern_len]

            print(f"Text: {text_len} chars, Pattern: {pattern_len} chars")

            # Test KMP and Boyer-Moore (fastest typically)
            start = time.perf_counter()
            kmp_matches = KMP.search(text, pattern)
            kmp_time = (time.perf_counter() - start) * 1000

            start = time.perf_counter()
            bm_matches = BoyerMoore.search(text, pattern)
            bm_time = (time.perf_counter() - start) * 1000

            print(f"  KMP: {kmp_time:.4f} ms ({len(kmp_matches)} matches)")
            print(f"  Boyer-Moore: {bm_time:.4f} ms ({len(bm_matches)} matches)")
            print()


# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("STRING PATTERN MATCHING ALGORITHMS")
    print("="*70)

    # Test text and patterns
    text = "ABABCABABABCABAB"
    pattern = "ABAB"

    print(f"\nTest Text: {text}")
    print(f"Pattern: {pattern}\n")

    # 1. KMP Algorithm
    print("\n" + "="*70)
    print("1. KMP ALGORITHM")
    print("="*70)
    matches = KMP.search(text, pattern, visualize=True)
    print(f"\nMatches found: {matches}")

    # 2. Boyer-Moore Algorithm
    print("\n" + "="*70)
    print("2. BOYER-MOORE ALGORITHM")
    print("="*70)
    matches = BoyerMoore.search(text, pattern, visualize=True)
    print(f"\nMatches found: {matches}")

    # 3. Rabin-Karp Algorithm
    print("\n" + "="*70)
    print("3. RABIN-KARP ALGORITHM")
    print("="*70)
    rk = RabinKarp()
    matches = rk.search(text, pattern, visualize=True)
    print(f"\nMatches found: {matches}")

    # 4. Aho-Corasick Algorithm (Multiple Patterns)
    print("\n" + "="*70)
    print("4. AHO-CORASICK ALGORITHM (Multiple Patterns)")
    print("="*70)
    ac = AhoCorasick()
    patterns = ["ABAB", "ABC", "CAB"]
    for i, p in enumerate(patterns):
        ac.add_pattern(p, i)
    ac.build_failure_links()
    results = ac.search(text, visualize=True)
    print(f"\nAll matches: {dict(results)}")

    # 5. Z-Algorithm
    print("\n" + "="*70)
    print("5. Z-ALGORITHM")
    print("="*70)
    matches = ZAlgorithm.search(text, pattern, visualize=True)
    print(f"\nMatches found: {matches}")

    # 6. Manacher's Algorithm (Palindromes)
    print("\n" + "="*70)
    print("6. MANACHER'S ALGORITHM")
    print("="*70)
    palindrome_text = "babad"
    longest = Manacher.longest_palindrome(palindrome_text)
    print(f"Text: {palindrome_text}")
    print(f"Longest palindrome: '{longest}'")

    palindromes = Manacher.find_all_palindromes(palindrome_text, visualize=True)

    # Performance Benchmarking
    print("\n" + "="*70)
    print("PERFORMANCE BENCHMARKING")
    print("="*70)

    benchmark_text = "ABC" * 1000
    benchmark_pattern = "ABCABC"

    PerformanceBenchmark.benchmark_single_pattern(benchmark_text, benchmark_pattern, iterations=100)
    PerformanceBenchmark.benchmark_varying_sizes()

    print("\n" + "="*70)
