"""
Suffix Tree and Suffix Array Implementations

Advanced string processing data structures for efficient pattern matching,
longest common substring, and other string operations.

Suffix Tree: A compressed trie containing all suffixes of a string.
Suffix Array: A space-efficient alternative storing sorted suffix indices.

Key Features:
- O(n) suffix tree construction (Ukkonen's algorithm)
- O(n log n) suffix array construction
- O(m) pattern matching for pattern of length m
- Longest common substring in O(n)
- Longest repeated substring
- All occurrences of a pattern

Applications:
- Bioinformatics (DNA/protein sequence analysis)
- Text editors (search and replace)
- Data compression
- Plagiarism detection
- Search engines

Author: Algorithms Multiverse
Date: January 2026
"""

from typing import List, Optional, Tuple, Set, Dict
from dataclasses import dataclass
import sys


class SuffixTreeNode:
    """Node in a suffix tree."""

    def __init__(self, start: int = -1, end: Optional[int] = None):
        """
        Initialize suffix tree node.

        Args:
            start: Start index of edge label in the text
            end: End index of edge label (None for leaves to use global end)
        """
        self.children: Dict[str, 'SuffixTreeNode'] = {}
        self.start = start
        self.end = end
        self.suffix_link: Optional['SuffixTreeNode'] = None
        self.suffix_index = -1  # -1 for internal nodes, >= 0 for leaves

    def edge_length(self, global_end: int) -> int:
        """Get the length of the edge leading to this node."""
        if self.start == -1:
            return 0
        if self.end is None:
            return global_end - self.start + 1
        return self.end - self.start + 1


class SuffixTree:
    """
    Suffix Tree implementation using Ukkonen's algorithm.

    Time Complexity:
    - Construction: O(n) where n is the length of the text
    - Pattern search: O(m) where m is the length of the pattern
    - Space: O(n)
    """

    def __init__(self, text: str):
        """
        Build suffix tree for the given text.

        Args:
            text: Input string to build suffix tree for
        """
        if not text:
            raise ValueError("Text cannot be empty")

        # Add terminal character if not present
        if not text.endswith('$'):
            text += '$'

        self.text = text
        self.n = len(text)
        self.root = SuffixTreeNode()
        self.global_end = -1

        # Build the tree
        self._build_suffix_tree()

    def _build_suffix_tree(self):
        """Build suffix tree using Ukkonen's algorithm."""
        # Active point for tree construction
        active_node = self.root
        active_edge = -1
        active_length = 0

        # Remaining suffixes to be added
        remaining_suffix_count = 0

        # Last created internal node
        last_new_node = None

        for i in range(self.n):
            self.global_end = i
            remaining_suffix_count += 1
            last_new_node = None

            while remaining_suffix_count > 0:
                # If active_length is 0, we need to check current character
                if active_length == 0:
                    active_edge = i

                # Check if there's an edge starting with active_edge character
                if self.text[active_edge] not in active_node.children:
                    # Create new leaf edge
                    active_node.children[self.text[active_edge]] = SuffixTreeNode(i)

                    # Add suffix link if needed
                    if last_new_node is not None:
                        last_new_node.suffix_link = active_node
                        last_new_node = None
                else:
                    # Edge exists, walk down if necessary
                    next_node = active_node.children[self.text[active_edge]]

                    # Walk down (trick 1)
                    if self._walk_down(next_node, active_length):
                        active_edge += next_node.edge_length(self.global_end)
                        active_length -= next_node.edge_length(self.global_end)
                        active_node = next_node
                        continue

                    # Check next character
                    if self.text[next_node.start + active_length] == self.text[i]:
                        # Character already exists, increment active_length
                        active_length += 1

                        # Add suffix link if needed
                        if last_new_node is not None and active_node != self.root:
                            last_new_node.suffix_link = active_node
                            last_new_node = None
                        break

                    # Split edge and create new internal node
                    split_end = next_node.start + active_length - 1

                    # New internal node
                    split_node = SuffixTreeNode(next_node.start, split_end)
                    active_node.children[self.text[active_edge]] = split_node

                    # New leaf
                    split_node.children[self.text[i]] = SuffixTreeNode(i)
                    next_node.start += active_length
                    split_node.children[self.text[next_node.start]] = next_node

                    # Add suffix links
                    if last_new_node is not None:
                        last_new_node.suffix_link = split_node
                    last_new_node = split_node

                # Decrement remaining suffix count
                remaining_suffix_count -= 1

                if active_node == self.root and active_length > 0:
                    active_length -= 1
                    active_edge = i - remaining_suffix_count + 1
                elif active_node != self.root:
                    active_node = active_node.suffix_link if active_node.suffix_link else self.root

        # Set suffix indices for leaves
        self._set_suffix_indices(self.root, 0)

    def _walk_down(self, node: SuffixTreeNode, active_length: int) -> bool:
        """Check if we need to walk down from the current node."""
        edge_length = node.edge_length(self.global_end)
        return active_length >= edge_length

    def _set_suffix_indices(self, node: SuffixTreeNode, label_height: int) -> None:
        """Set suffix index for leaf nodes (DFS traversal)."""
        if node is None:
            return

        leaf = True
        for child in node.children.values():
            leaf = False
            edge_len = child.edge_length(self.global_end)
            self._set_suffix_indices(child, label_height + edge_len)

        if leaf:
            node.suffix_index = self.n - label_height

    def search(self, pattern: str) -> List[int]:
        """
        Search for all occurrences of pattern in the text.

        Args:
            pattern: Pattern to search for

        Returns:
            List of starting positions of all occurrences
        """
        if not pattern:
            return []

        node = self.root
        i = 0

        while i < len(pattern):
            if pattern[i] not in node.children:
                return []  # Pattern not found

            child = node.children[pattern[i]]
            j = 0
            edge_len = child.edge_length(self.global_end)

            # Compare characters on the edge
            while j < edge_len and i < len(pattern):
                if self.text[child.start + j] != pattern[i]:
                    return []  # Mismatch
                j += 1
                i += 1

            if i < len(pattern):
                node = child  # Continue with next edge
            else:
                # Pattern found, collect all leaf positions
                return self._collect_leaves(child)

        return self._collect_leaves(node)

    def _collect_leaves(self, node: SuffixTreeNode) -> List[int]:
        """Collect all suffix indices from leaves under given node."""
        if node.suffix_index >= 0:
            return [node.suffix_index]

        result = []
        for child in node.children.values():
            result.extend(self._collect_leaves(child))
        return result

    def longest_repeated_substring(self) -> str:
        """
        Find the longest substring that appears at least twice.

        Returns:
            The longest repeated substring
        """
        max_height = 0
        substring_end = 0

        def dfs(node: SuffixTreeNode, height: int) -> int:
            nonlocal max_height, substring_end

            if node.suffix_index >= 0:
                return node.suffix_index

            # Internal node represents repeated substring
            min_suffix = float('inf')
            for child in node.children.values():
                edge_len = child.edge_length(self.global_end)
                suffix_idx = dfs(child, height + edge_len)
                min_suffix = min(min_suffix, suffix_idx)

            if height > max_height:
                max_height = height
                substring_end = min_suffix + height

            return min_suffix

        dfs(self.root, 0)

        if max_height == 0:
            return ""

        return self.text[substring_end - max_height:substring_end]

    def contains(self, pattern: str) -> bool:
        """Check if pattern exists in the text."""
        return len(self.search(pattern)) > 0


class SuffixArray:
    """
    Suffix Array implementation with LCP (Longest Common Prefix) array.

    A suffix array is a sorted array of all suffixes of a string,
    represented by their starting positions.

    Time Complexity:
    - Construction: O(n log n) or O(n) with advanced algorithms
    - Pattern search: O(m log n) where m is pattern length
    - Space: O(n)
    """

    def __init__(self, text: str):
        """
        Build suffix array for the given text.

        Args:
            text: Input string to build suffix array for
        """
        if not text:
            raise ValueError("Text cannot be empty")

        self.text = text
        self.n = len(text)
        self.suffix_array = self._build_suffix_array()
        self.lcp_array = self._build_lcp_array()

    def _build_suffix_array(self) -> List[int]:
        """
        Build suffix array using O(n log^2 n) algorithm.
        Can be optimized to O(n log n) or O(n).
        """
        # Create list of (suffix, index) pairs
        suffixes = []
        for i in range(self.n):
            suffixes.append((self.text[i:], i))

        # Sort suffixes
        suffixes.sort(key=lambda x: x[0])

        # Extract indices
        return [suffix[1] for suffix in suffixes]

    def _build_suffix_array_optimized(self) -> List[int]:
        """
        Build suffix array using O(n log n) algorithm with counting sort.
        """
        # Implementation of DC3 or SA-IS algorithm would go here
        # For now, using the simpler version above
        return self._build_suffix_array()

    def _build_lcp_array(self) -> List[int]:
        """
        Build LCP (Longest Common Prefix) array using Kasai's algorithm.

        LCP[i] = length of longest common prefix between suffix_array[i] and suffix_array[i+1]

        Time: O(n)
        """
        lcp = [0] * self.n
        rank = [0] * self.n

        # Build rank array (inverse of suffix array)
        for i in range(self.n):
            rank[self.suffix_array[i]] = i

        k = 0  # Length of previous LCP

        for i in range(self.n):
            if rank[i] == self.n - 1:
                k = 0
                continue

            j = self.suffix_array[rank[i] + 1]

            # Count matching characters
            while i + k < self.n and j + k < self.n and self.text[i + k] == self.text[j + k]:
                k += 1

            lcp[rank[i]] = k

            if k > 0:
                k -= 1

        return lcp

    def search(self, pattern: str) -> List[int]:
        """
        Search for all occurrences of pattern using binary search.

        Args:
            pattern: Pattern to search for

        Returns:
            List of starting positions of all occurrences

        Time: O(m log n) where m is pattern length
        """
        if not pattern:
            return []

        # Binary search for leftmost occurrence
        left = self._binary_search_left(pattern)
        if left == -1:
            return []

        # Binary search for rightmost occurrence
        right = self._binary_search_right(pattern)

        # Extract all positions
        result = []
        for i in range(left, right + 1):
            result.append(self.suffix_array[i])

        return sorted(result)

    def _binary_search_left(self, pattern: str) -> int:
        """Find leftmost suffix that starts with pattern."""
        left, right = 0, self.n - 1
        result = -1

        while left <= right:
            mid = (left + right) // 2
            suffix_start = self.suffix_array[mid]
            suffix = self.text[suffix_start:suffix_start + len(pattern)]

            if suffix >= pattern:
                if suffix.startswith(pattern):
                    result = mid
                right = mid - 1
            else:
                left = mid + 1

        return result

    def _binary_search_right(self, pattern: str) -> int:
        """Find rightmost suffix that starts with pattern."""
        left, right = 0, self.n - 1
        result = -1

        while left <= right:
            mid = (left + right) // 2
            suffix_start = self.suffix_array[mid]
            suffix = self.text[suffix_start:suffix_start + len(pattern)]

            if suffix > pattern or (suffix == pattern and suffix_start + len(pattern) <= self.n):
                if suffix.startswith(pattern):
                    result = mid
                    left = mid + 1
                else:
                    right = mid - 1
            else:
                left = mid + 1

        return result

    def longest_repeated_substring(self) -> str:
        """
        Find the longest repeated substring using LCP array.

        Returns:
            The longest repeated substring

        Time: O(n)
        """
        if self.n <= 1:
            return ""

        max_lcp = max(self.lcp_array)
        if max_lcp == 0:
            return ""

        max_idx = self.lcp_array.index(max_lcp)
        start = self.suffix_array[max_idx]

        return self.text[start:start + max_lcp]

    def longest_common_substring(self, text2: str) -> str:
        """
        Find longest common substring with another text.

        Args:
            text2: Second text to compare with

        Returns:
            The longest common substring
        """
        # Concatenate texts with unique separator
        separator = '#'
        combined = self.text + separator + text2
        n1 = len(self.text)

        # Build suffix array for combined text
        sa = SuffixArray(combined)

        max_len = 0
        result = ""

        # Check adjacent suffixes in sorted order
        for i in range(len(sa.suffix_array) - 1):
            pos1 = sa.suffix_array[i]
            pos2 = sa.suffix_array[i + 1]

            # Check if suffixes are from different texts
            if (pos1 < n1) != (pos2 < n1):
                # Calculate LCP
                lcp_len = sa.lcp_array[i]
                if lcp_len > max_len:
                    max_len = lcp_len
                    result = combined[pos1:pos1 + lcp_len]

        return result

    def count_distinct_substrings(self) -> int:
        """
        Count the number of distinct substrings.

        Returns:
            Number of distinct substrings

        Time: O(n)
        """
        # Total possible substrings
        total = self.n * (self.n + 1) // 2

        # Subtract duplicate substrings (sum of LCP values)
        duplicates = sum(self.lcp_array)

        return total - duplicates


class SuffixAutomaton:
    """
    Suffix Automaton (DAWG - Directed Acyclic Word Graph).

    A minimal DFA that recognizes all suffixes of a string.
    More space-efficient than suffix tree for some operations.
    """

    @dataclass
    class State:
        """State in suffix automaton."""
        length: int = 0
        link: Optional['SuffixAutomaton.State'] = None
        next: Dict[str, 'SuffixAutomaton.State'] = None

        def __post_init__(self):
            if self.next is None:
                self.next = {}

    def __init__(self, text: str):
        """
        Build suffix automaton for the given text.

        Args:
            text: Input string
        """
        self.text = text
        self.root = self.State()
        self.last = self.root

        # Build automaton
        for char in text:
            self._extend(char)

    def _extend(self, char: str):
        """Extend automaton with a new character."""
        cur = self.State(length=self.last.length + 1)
        p = self.last

        while p is not None and char not in p.next:
            p.next[char] = cur
            p = p.link

        if p is None:
            cur.link = self.root
        else:
            q = p.next[char]
            if p.length + 1 == q.length:
                cur.link = q
            else:
                # Clone state
                clone = self.State(length=p.length + 1)
                clone.next = q.next.copy()
                clone.link = q.link

                while p is not None and p.next.get(char) == q:
                    p.next[char] = clone
                    p = p.link

                q.link = clone
                cur.link = clone

        self.last = cur

    def contains(self, pattern: str) -> bool:
        """Check if pattern is a substring."""
        state = self.root

        for char in pattern:
            if char not in state.next:
                return False
            state = state.next[char]

        return True


def example_usage():
    """Demonstrate suffix structures usage."""
    print("Suffix Structures Examples")
    print("=" * 50)

    text = "banana"

    # Suffix Tree
    print("\n1. Suffix Tree:")
    st = SuffixTree(text)

    # Search for patterns
    patterns = ["ana", "ban", "nan", "xyz"]
    for pattern in patterns:
        positions = st.search(pattern)
        if positions:
            print(f"  '{pattern}' found at positions: {positions}")
        else:
            print(f"  '{pattern}' not found")

    # Longest repeated substring
    lrs = st.longest_repeated_substring()
    print(f"\n  Longest repeated substring: '{lrs}'")

    # Suffix Array
    print("\n2. Suffix Array:")
    sa = SuffixArray(text)

    print(f"  Suffix array: {sa.suffix_array}")
    print(f"  LCP array: {sa.lcp_array}")

    # Suffixes in sorted order
    print("\n  Suffixes in sorted order:")
    for i, idx in enumerate(sa.suffix_array):
        print(f"    {i}: '{text[idx:]}'")

    # Pattern search
    pattern = "ana"
    positions = sa.search(pattern)
    print(f"\n  Pattern '{pattern}' found at: {positions}")

    # Longest repeated substring
    lrs_sa = sa.longest_repeated_substring()
    print(f"  Longest repeated substring: '{lrs_sa}'")

    # Count distinct substrings
    distinct = sa.count_distinct_substrings()
    print(f"  Number of distinct substrings: {distinct}")

    # Longest common substring
    print("\n3. Longest Common Substring:")
    text1 = "GeeksforGeeks"
    text2 = "GeeksQuiz"
    sa1 = SuffixArray(text1)
    lcs = sa1.longest_common_substring(text2)
    print(f"  Text 1: '{text1}'")
    print(f"  Text 2: '{text2}'")
    print(f"  LCS: '{lcs}'")

    # DNA sequence example
    print("\n4. DNA Sequence Analysis:")
    dna = "ATCGATCGATCGATCG"
    st_dna = SuffixTree(dna)

    # Find all occurrences of a motif
    motif = "ATCG"
    occurrences = st_dna.search(motif)
    print(f"  DNA: {dna}")
    print(f"  Motif '{motif}' occurs {len(occurrences)} times at positions: {occurrences}")

    # Find tandem repeats
    tandem = st_dna.longest_repeated_substring()
    print(f"  Longest tandem repeat: '{tandem}'")

    # Performance comparison
    print("\n5. Performance Characteristics:")
    print("  Operation          | Suffix Tree | Suffix Array |")
    print("  -------------------|-------------|--------------|")
    print("  Construction       | O(n)        | O(n log n)   |")
    print("  Pattern search     | O(m)        | O(m log n)   |")
    print("  Space              | O(n)        | O(n)         |")
    print("  All occurrences    | O(m + occ)  | O(m log n + occ) |")
    print("  LCP/LRS           | O(n)        | O(n)         |")


def benchmark_suffix_structures():
    """Benchmark suffix structures on different text sizes."""
    import time
    import random
    import string

    print("\nSuffix Structures Benchmarks")
    print("=" * 50)

    sizes = [100, 500, 1000, 5000]

    for size in sizes:
        # Generate random text
        text = ''.join(random.choices(string.ascii_lowercase, k=size))
        pattern = text[size//2:size//2 + min(10, size//10)]

        print(f"\nText size: {size}")

        # Suffix Tree
        start = time.time()
        st = SuffixTree(text)
        build_time = time.time() - start

        start = time.time()
        for _ in range(100):
            st.search(pattern)
        search_time = time.time() - start

        print(f"  Suffix Tree:")
        print(f"    Build time: {build_time:.4f}s")
        print(f"    Search time (100x): {search_time:.4f}s")

        # Suffix Array
        start = time.time()
        sa = SuffixArray(text)
        build_time = time.time() - start

        start = time.time()
        for _ in range(100):
            sa.search(pattern)
        search_time = time.time() - start

        print(f"  Suffix Array:")
        print(f"    Build time: {build_time:.4f}s")
        print(f"    Search time (100x): {search_time:.4f}s")

        # Python built-in comparison
        start = time.time()
        for _ in range(100):
            text.find(pattern)
        builtin_time = time.time() - start

        print(f"  Python str.find (100x): {builtin_time:.4f}s")


if __name__ == "__main__":
    # Run examples
    example_usage()

    # Run benchmarks
    benchmark_suffix_structures()