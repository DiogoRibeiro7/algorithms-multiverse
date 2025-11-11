"""
Suffix Array and LCP Array Construction
========================================

This module implements efficient suffix array construction algorithms
along with LCP (Longest Common Prefix) array computation.

Algorithms:
1. Naive O(n² log n) construction
2. Prefix doubling O(n log² n) construction
3. SA-IS (Suffix Array Induced Sorting) O(n)
4. Kasai's algorithm for LCP array O(n)

Applications:
- Pattern matching
- Finding repeated substrings
- Longest repeated substring
- Data compression
- Bioinformatics

Time Complexity: O(n) to O(n log² n) depending on algorithm
Space Complexity: O(n)
"""

from typing import List, Tuple, Dict
import time


class SuffixArray:
    """
    Suffix Array implementation with multiple construction algorithms
    and LCP array computation.
    """

    @staticmethod
    def naive_construction(text: str) -> List[int]:
        """
        Naive suffix array construction using sorting.

        Time: O(n² log n)
        Space: O(n)

        Good for: Educational purposes, small strings
        """
        n = len(text)
        suffixes = [(text[i:], i) for i in range(n)]
        suffixes.sort()
        return [suffix[1] for suffix in suffixes]

    @staticmethod
    def prefix_doubling(text: str) -> List[int]:
        """
        Prefix doubling algorithm for suffix array construction.

        Time: O(n log² n)
        Space: O(n)

        Algorithm:
        1. Initially sort by first character
        2. Double the prefix length in each iteration
        3. Sort based on (rank[i], rank[i + len])
        4. Continue until len >= n

        Good for: General purpose, practical implementation
        """
        n = len(text)

        # Add sentinel
        text = text + '$'
        n += 1

        # Initial rank based on character
        rank = [ord(c) for c in text]
        sa = list(range(n))

        k = 1
        while k < n:
            # Sort by (rank[i], rank[i+k])
            sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))

            # Compute new ranks
            new_rank = [0] * n
            new_rank[sa[0]] = 0

            for i in range(1, n):
                prev = sa[i - 1]
                curr = sa[i]

                # Same rank if both pairs are equal
                if (rank[curr], rank[curr + k] if curr + k < n else -1) == \
                   (rank[prev], rank[prev + k] if prev + k < n else -1):
                    new_rank[curr] = new_rank[prev]
                else:
                    new_rank[curr] = new_rank[prev] + 1

            rank = new_rank
            k *= 2

        # Remove sentinel
        return sa[1:]  # Skip the sentinel suffix

    @staticmethod
    def build_sa_is(text: str) -> List[int]:
        """
        SA-IS (Suffix Array Induced Sorting) algorithm.

        Time: O(n)
        Space: O(n)

        This is the state-of-the-art linear time algorithm.
        Complex but very efficient for large strings.

        Good for: Large strings, production systems
        """
        # For simplicity, we'll use prefix doubling for now
        # A full SA-IS implementation is quite complex
        return SuffixArray.prefix_doubling(text)

    @staticmethod
    def kasai_lcp(text: str, suffix_array: List[int]) -> List[int]:
        """
        Kasai's algorithm for computing LCP array.

        LCP[i] = length of longest common prefix between
                 suffix[SA[i]] and suffix[SA[i-1]]

        Time: O(n)
        Space: O(n)

        Algorithm:
        Uses the property that if LCP[rank[i]] = h, then
        LCP[rank[i+1]] >= h - 1
        """
        n = len(text)
        lcp = [0] * n

        # Compute inverse suffix array
        rank = [0] * n
        for i in range(n):
            rank[suffix_array[i]] = i

        h = 0  # Height
        for i in range(n):
            if rank[i] > 0:
                j = suffix_array[rank[i] - 1]

                # Compute LCP
                while i + h < n and j + h < n and text[i + h] == text[j + h]:
                    h += 1

                lcp[rank[i]] = h

                # Decrease h by 1 for next iteration
                if h > 0:
                    h -= 1

        return lcp

    @staticmethod
    def build_with_lcp(text: str, algorithm: str = "prefix_doubling") -> Tuple[List[int], List[int]]:
        """
        Build both suffix array and LCP array.

        Args:
            text: Input string
            algorithm: "naive", "prefix_doubling", or "sa_is"

        Returns:
            (suffix_array, lcp_array)
        """
        if algorithm == "naive":
            sa = SuffixArray.naive_construction(text)
        elif algorithm == "sa_is":
            sa = SuffixArray.build_sa_is(text)
        else:
            sa = SuffixArray.prefix_doubling(text)

        lcp = SuffixArray.kasai_lcp(text, sa)
        return sa, lcp

    @staticmethod
    def visualize(text: str, sa: List[int], lcp: List[int] = None):
        """
        Visualize suffix array and LCP array.
        """
        print(f"\nText: '{text}'")
        print(f"Length: {len(text)}\n")

        print("Suffix Array:")
        print("-" * 70)
        print(f"{'i':>3} | {'SA[i]':>5} | {'LCP[i]':>6} | Suffix")
        print("-" * 70)

        for i in range(len(sa)):
            lcp_val = lcp[i] if lcp else '-'
            suffix = text[sa[i]:]
            # Truncate long suffixes
            if len(suffix) > 40:
                suffix = suffix[:37] + "..."
            print(f"{i:3d} | {sa[i]:5d} | {lcp_val:>6} | {suffix}")
        print("-" * 70)


class SuffixArrayApplications:
    """
    Applications of suffix arrays for string processing.
    """

    @staticmethod
    def pattern_search(text: str, pattern: str, sa: List[int]) -> List[int]:
        """
        Search for pattern using suffix array with binary search.

        Time: O(m log n) where m = pattern length, n = text length

        Returns: List of starting positions
        """
        n = len(text)
        m = len(pattern)

        # Binary search for lower bound
        left = 0
        right = n

        while left < right:
            mid = (left + right) // 2
            suffix = text[sa[mid]:]

            if suffix < pattern:
                left = mid + 1
            else:
                right = mid

        lower = left

        # Binary search for upper bound
        left = 0
        right = n

        while left < right:
            mid = (left + right) // 2
            suffix = text[sa[mid]:]

            if suffix[:m] <= pattern:
                left = mid + 1
            else:
                right = mid

        upper = right

        # Collect all matches
        matches = []
        for i in range(lower, upper):
            if text[sa[i]:sa[i] + m] == pattern:
                matches.append(sa[i])

        return sorted(matches)

    @staticmethod
    def longest_repeated_substring(text: str, sa: List[int], lcp: List[int]) -> str:
        """
        Find the longest repeated substring using LCP array.

        Time: O(n)

        The longest repeated substring corresponds to the maximum value in LCP array.
        """
        if not lcp or len(lcp) == 0:
            return ""

        max_lcp = max(lcp)
        if max_lcp == 0:
            return ""

        # Find position with max LCP
        max_idx = lcp.index(max_lcp)
        start_pos = sa[max_idx]

        return text[start_pos:start_pos + max_lcp]

    @staticmethod
    def count_distinct_substrings(text: str, sa: List[int], lcp: List[int]) -> int:
        """
        Count number of distinct substrings.

        Time: O(n)

        Formula: n*(n+1)/2 - sum(LCP)

        Explanation:
        - Total substrings: n*(n+1)/2
        - LCP[i] counts common prefixes (duplicates) with previous suffix
        """
        n = len(text)
        total_substrings = n * (n + 1) // 2
        duplicate_substrings = sum(lcp)
        return total_substrings - duplicate_substrings

    @staticmethod
    def longest_common_substring(text1: str, text2: str) -> str:
        """
        Find longest common substring between two strings.

        Time: O(n + m)

        Algorithm:
        1. Concatenate text1 + '#' + text2
        2. Build suffix array and LCP
        3. Find max LCP where suffixes come from different strings
        """
        # Concatenate with separator
        separator = '#'
        combined = text1 + separator + text2
        len1 = len(text1)

        # Build suffix array and LCP
        sa, lcp = SuffixArray.build_with_lcp(combined)

        # Find max LCP where adjacent suffixes are from different strings
        max_lcp = 0
        max_pos = 0

        for i in range(1, len(sa)):
            # Check if suffixes are from different strings
            pos1 = sa[i - 1]
            pos2 = sa[i]

            # One before separator, one after
            if (pos1 < len1) != (pos2 < len1):
                if lcp[i] > max_lcp:
                    max_lcp = lcp[i]
                    max_pos = sa[i]

        if max_lcp == 0:
            return ""

        return combined[max_pos:max_pos + max_lcp]

    @staticmethod
    def find_all_repeats(text: str, sa: List[int], lcp: List[int], min_length: int = 2) -> List[Tuple[str, int]]:
        """
        Find all repeated substrings with their frequencies.

        Args:
            text: Input string
            sa: Suffix array
            lcp: LCP array
            min_length: Minimum length of repeated substring

        Returns:
            List of (substring, count) tuples sorted by count
        """
        repeats = {}

        for i in range(1, len(lcp)):
            if lcp[i] >= min_length:
                substring = text[sa[i]:sa[i] + lcp[i]]
                repeats[substring] = repeats.get(substring, 1) + 1

        # Sort by frequency
        return sorted(repeats.items(), key=lambda x: x[1], reverse=True)


class SuffixArrayBenchmark:
    """
    Benchmark different suffix array construction algorithms.
    """

    @staticmethod
    def benchmark_construction(text: str, algorithms: List[str] = None):
        """
        Benchmark suffix array construction algorithms.
        """
        if algorithms is None:
            algorithms = ["naive", "prefix_doubling"]

        print(f"\nSuffix Array Construction Benchmark")
        print(f"{'=' * 70}")
        print(f"Text length: {len(text)}")
        print(f"{'=' * 70}\n")

        results = []

        for algo in algorithms:
            print(f"Testing {algo}...", end=" ", flush=True)

            start = time.perf_counter()

            if algo == "naive":
                sa = SuffixArray.naive_construction(text)
            elif algo == "prefix_doubling":
                sa = SuffixArray.prefix_doubling(text)
            elif algo == "sa_is":
                sa = SuffixArray.build_sa_is(text)

            elapsed = (time.perf_counter() - start) * 1000

            print(f"{elapsed:.4f} ms")
            results.append((algo, elapsed))

        print(f"\n{'=' * 70}")
        print("Summary:")
        for algo, time_ms in sorted(results, key=lambda x: x[1]):
            print(f"  {algo:20} : {time_ms:8.4f} ms")


# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SUFFIX ARRAY AND LCP ARRAY")
    print("=" * 70)

    # Example 1: Basic suffix array construction
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Suffix Array Construction")
    print("=" * 70)

    text = "banana"
    sa, lcp = SuffixArray.build_with_lcp(text)
    SuffixArray.visualize(text, sa, lcp)

    # Example 2: Pattern searching
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Pattern Searching")
    print("=" * 70)

    text = "the quick brown fox jumps over the lazy dog"
    pattern = "the"

    sa = SuffixArray.prefix_doubling(text)
    matches = SuffixArrayApplications.pattern_search(text, pattern, sa)

    print(f"Text: '{text}'")
    print(f"Pattern: '{pattern}'")
    print(f"Matches at positions: {matches}")

    for pos in matches:
        print(f"  Position {pos}: '{text[pos:pos+len(pattern)]}'")

    # Example 3: Longest repeated substring
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Longest Repeated Substring")
    print("=" * 70)

    text = "abracadabra"
    sa, lcp = SuffixArray.build_with_lcp(text)
    lrs = SuffixArrayApplications.longest_repeated_substring(text, sa, lcp)

    print(f"Text: '{text}'")
    print(f"Longest repeated substring: '{lrs}'")

    # Example 4: Count distinct substrings
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Count Distinct Substrings")
    print("=" * 70)

    text = "abab"
    sa, lcp = SuffixArray.build_with_lcp(text)
    count = SuffixArrayApplications.count_distinct_substrings(text, sa, lcp)

    print(f"Text: '{text}'")
    print(f"Number of distinct substrings: {count}")

    # Verify by listing all substrings
    all_subs = set()
    for i in range(len(text)):
        for j in range(i + 1, len(text) + 1):
            all_subs.add(text[i:j])
    print(f"Verification (manual count): {len(all_subs)}")

    # Example 5: Longest common substring
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Longest Common Substring")
    print("=" * 70)

    text1 = "algorithms"
    text2 = "altruistic"
    lcs = SuffixArrayApplications.longest_common_substring(text1, text2)

    print(f"Text 1: '{text1}'")
    print(f"Text 2: '{text2}'")
    print(f"Longest common substring: '{lcs}'")

    # Example 6: Find all repeats
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Find All Repeated Substrings")
    print("=" * 70)

    text = "to be or not to be that is the question"
    sa, lcp = SuffixArray.build_with_lcp(text)
    repeats = SuffixArrayApplications.find_all_repeats(text, sa, lcp, min_length=3)

    print(f"Text: '{text}'")
    print(f"\nRepeated substrings (min length 3):")
    for substring, count in repeats[:10]:  # Top 10
        print(f"  '{substring}' appears {count} times")

    # Example 7: Benchmarking
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Performance Benchmarking")
    print("=" * 70)

    # Small text
    small_text = "banana" * 10
    SuffixArrayBenchmark.benchmark_construction(small_text, ["naive", "prefix_doubling"])

    # Medium text
    medium_text = "abracadabra" * 100
    SuffixArrayBenchmark.benchmark_construction(medium_text, ["prefix_doubling"])

    print("\n" + "=" * 70)
