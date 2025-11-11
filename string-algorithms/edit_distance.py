"""
Edit Distance Algorithms
========================

This module implements various edit distance algorithms for measuring
string similarity.

Algorithms:
1. Hamming Distance - Simple substitution only
2. Levenshtein Distance - Insert, delete, substitute
3. Damerau-Levenshtein Distance - Adds transposition
4. Longest Common Subsequence (LCS)
5. Wagner-Fischer algorithm
6. Edit distance with custom costs

Applications:
- Spell checking
- DNA sequence alignment
- Plagiarism detection
- Fuzzy string matching
- Data deduplication

Time Complexity: O(nm) where n, m are string lengths
Space Complexity: O(nm) or O(min(n,m)) with optimization
"""

from typing import List, Tuple, Dict, Optional
import sys


class EditDistance:
    """
    Collection of edit distance algorithms.
    """

    @staticmethod
    def hamming(str1: str, str2: str) -> int:
        """
        Hamming Distance - Number of positions at which symbols differ.

        Time: O(n)
        Space: O(1)

        Requirements: Strings must have equal length

        Applications:
        - Error detection codes
        - Cryptography
        - Information theory
        """
        if len(str1) != len(str2):
            raise ValueError("Hamming distance requires equal length strings")

        return sum(c1 != c2 for c1, c2 in zip(str1, str2))

    @staticmethod
    def levenshtein(str1: str, str2: str, visualize: bool = False) -> int:
        """
        Levenshtein Distance - Minimum edits (insert, delete, substitute).

        Time: O(nm)
        Space: O(nm)

        Algorithm:
        dp[i][j] = min edit distance to transform str1[0:i] to str2[0:j]

        Recurrence:
        dp[i][j] = min(
            dp[i-1][j] + 1,      # delete from str1
            dp[i][j-1] + 1,      # insert into str1
            dp[i-1][j-1] + cost  # substitute (cost = 0 if match, 1 otherwise)
        )

        Applications:
        - Spell checking
        - DNA sequence alignment
        - Fuzzy matching
        """
        m, n = len(str1), len(str2)

        # Create DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Initialize base cases
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    cost = 0
                else:
                    cost = 1

                dp[i][j] = min(
                    dp[i - 1][j] + 1,      # deletion
                    dp[i][j - 1] + 1,      # insertion
                    dp[i - 1][j - 1] + cost  # substitution
                )

        if visualize:
            EditDistance._visualize_dp_table(str1, str2, dp)

        return dp[m][n]

    @staticmethod
    def levenshtein_optimized(str1: str, str2: str) -> int:
        """
        Space-optimized Levenshtein distance.

        Time: O(nm)
        Space: O(min(n, m))

        Uses only two rows of the DP table.
        """
        # Ensure str1 is shorter
        if len(str1) > len(str2):
            str1, str2 = str2, str1

        m, n = len(str1), len(str2)

        # Use two rows
        prev_row = list(range(n + 1))
        curr_row = [0] * (n + 1)

        for i in range(1, m + 1):
            curr_row[0] = i

            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    cost = 0
                else:
                    cost = 1

                curr_row[j] = min(
                    prev_row[j] + 1,          # deletion
                    curr_row[j - 1] + 1,      # insertion
                    prev_row[j - 1] + cost    # substitution
                )

            prev_row, curr_row = curr_row, prev_row

        return prev_row[n]

    @staticmethod
    def damerau_levenshtein(str1: str, str2: str) -> int:
        """
        Damerau-Levenshtein Distance - Adds transposition operation.

        Time: O(nm)
        Space: O(nm)

        Operations:
        1. Insertion
        2. Deletion
        3. Substitution
        4. Transposition (swap adjacent characters)

        More accurate for typos where characters are swapped.

        Applications:
        - Spell checking (catches "teh" -> "the")
        - OCR error correction
        - Keyboard typo detection
        """
        m, n = len(str1), len(str2)

        # Create DP table with extra row/column
        max_dist = m + n
        H = {}

        # Initialize
        H[-1, -1] = max_dist
        for i in range(0, m + 1):
            H[i, -1] = max_dist
            H[i, 0] = i
        for j in range(0, n + 1):
            H[-1, j] = max_dist
            H[0, j] = j

        for i in range(1, m + 1):
            DB = 0
            for j in range(1, n + 1):
                k = DB
                l = 0 if str1[i - 1] == str2[j - 1] else 1
                if str1[i - 1] == str2[j - 1]:
                    DB = j

                H[i, j] = min(
                    H[i - 1, j] + 1,           # deletion
                    H[i, j - 1] + 1,           # insertion
                    H[i - 1, j - 1] + l,       # substitution
                    H[k - 1, DB - 1] + (i - k - 1) + 1 + (j - DB - 1)  # transposition
                )

        return H[m, n]

    @staticmethod
    def lcs_length(str1: str, str2: str) -> int:
        """
        Longest Common Subsequence (LCS) length.

        Time: O(nm)
        Space: O(nm)

        Not a distance metric, but related.
        LCS can be used to compute edit distance.

        Note: Subsequence doesn't require consecutive characters.
        """
        m, n = len(str1), len(str2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]

    @staticmethod
    def lcs_string(str1: str, str2: str) -> str:
        """
        Return the actual Longest Common Subsequence.

        Time: O(nm)
        Space: O(nm)
        """
        m, n = len(str1), len(str2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Backtrack to find LCS
        lcs = []
        i, j = m, n

        while i > 0 and j > 0:
            if str1[i - 1] == str2[j - 1]:
                lcs.append(str1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return ''.join(reversed(lcs))

    @staticmethod
    def weighted_edit_distance(str1: str, str2: str,
                              insert_cost: int = 1,
                              delete_cost: int = 1,
                              substitute_cost: int = 1) -> int:
        """
        Edit distance with custom operation costs.

        Time: O(nm)
        Space: O(nm)

        Allows different costs for different operations.
        """
        m, n = len(str1), len(str2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i * delete_cost
        for j in range(n + 1):
            dp[0][j] = j * insert_cost

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    cost = 0
                else:
                    cost = substitute_cost

                dp[i][j] = min(
                    dp[i - 1][j] + delete_cost,
                    dp[i][j - 1] + insert_cost,
                    dp[i - 1][j - 1] + cost
                )

        return dp[m][n]

    @staticmethod
    def edit_sequence(str1: str, str2: str) -> List[Tuple[str, int, str]]:
        """
        Return the sequence of edit operations.

        Returns: List of (operation, position, character) tuples
        Operations: 'insert', 'delete', 'substitute', 'match'

        Time: O(nm)
        Space: O(nm)
        """
        m, n = len(str1), len(str2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]
        ops = [[None] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
            if i > 0:
                ops[i][0] = ('delete', i - 1, str1[i - 1])

        for j in range(n + 1):
            dp[0][j] = j
            if j > 0:
                ops[0][j] = ('insert', j - 1, str2[j - 1])

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                    ops[i][j] = ('match', i - 1, str1[i - 1])
                else:
                    costs = [
                        (dp[i - 1][j] + 1, 'delete', i - 1, str1[i - 1]),
                        (dp[i][j - 1] + 1, 'insert', j - 1, str2[j - 1]),
                        (dp[i - 1][j - 1] + 1, 'substitute', i - 1, str2[j - 1])
                    ]
                    min_cost = min(costs, key=lambda x: x[0])
                    dp[i][j] = min_cost[0]
                    ops[i][j] = min_cost[1:]

        # Backtrack to get sequence
        sequence = []
        i, j = m, n

        while i > 0 or j > 0:
            if ops[i][j]:
                sequence.append(ops[i][j])

            op = ops[i][j][0] if ops[i][j] else None

            if op == 'match' or op == 'substitute':
                i -= 1
                j -= 1
            elif op == 'delete':
                i -= 1
            elif op == 'insert':
                j -= 1

        return list(reversed(sequence))

    @staticmethod
    def _visualize_dp_table(str1: str, str2: str, dp: List[List[int]]):
        """
        Visualize the DP table for edit distance.
        """
        print("\nDP Table:")
        print("=" * 70)

        # Header
        print("       ", end="")
        for c in str2:
            print(f"{c:>4}", end="")
        print()

        # Rows
        for i, row in enumerate(dp):
            if i == 0:
                print("  ", end="")
            else:
                print(f"{str1[i-1]:>2}", end="")

            for val in row:
                print(f"{val:>4}", end="")
            print()


class SimilarityMetrics:
    """
    String similarity metrics derived from edit distances.
    """

    @staticmethod
    def normalized_levenshtein(str1: str, str2: str) -> float:
        """
        Normalized Levenshtein distance (0 to 1).

        Returns: 1 - (distance / max_length)

        1.0 = identical
        0.0 = completely different
        """
        if not str1 and not str2:
            return 1.0

        distance = EditDistance.levenshtein(str1, str2)
        max_len = max(len(str1), len(str2))

        return 1.0 - (distance / max_len)

    @staticmethod
    def similarity_ratio(str1: str, str2: str) -> float:
        """
        Similarity ratio based on LCS.

        Returns: 2 * LCS / (len(str1) + len(str2))

        1.0 = identical
        0.0 = no common subsequence
        """
        if not str1 and not str2:
            return 1.0

        lcs_len = EditDistance.lcs_length(str1, str2)
        total_len = len(str1) + len(str2)

        if total_len == 0:
            return 1.0

        return 2.0 * lcs_len / total_len

    @staticmethod
    def jaro_distance(str1: str, str2: str) -> float:
        """
        Jaro distance - Good for short strings like names.

        Time: O(nm)

        Returns value between 0 and 1:
        1.0 = identical
        0.0 = no similarity
        """
        if str1 == str2:
            return 1.0

        len1, len2 = len(str1), len(str2)

        if len1 == 0 or len2 == 0:
            return 0.0

        # Maximum allowed distance
        match_distance = max(len1, len2) // 2 - 1
        if match_distance < 1:
            match_distance = 1

        str1_matches = [False] * len1
        str2_matches = [False] * len2

        matches = 0
        transpositions = 0

        # Find matches
        for i in range(len1):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len2)

            for j in range(start, end):
                if str2_matches[j] or str1[i] != str2[j]:
                    continue
                str1_matches[i] = True
                str2_matches[j] = True
                matches += 1
                break

        if matches == 0:
            return 0.0

        # Find transpositions
        k = 0
        for i in range(len1):
            if not str1_matches[i]:
                continue
            while not str2_matches[k]:
                k += 1
            if str1[i] != str2[k]:
                transpositions += 1
            k += 1

        return (matches / len1 + matches / len2 +
                (matches - transpositions / 2) / matches) / 3.0

    @staticmethod
    def jaro_winkler_distance(str1: str, str2: str, prefix_scale: float = 0.1) -> float:
        """
        Jaro-Winkler distance - Gives more weight to common prefix.

        Time: O(nm)

        Better for names and short strings.

        Args:
            prefix_scale: Scaling factor for common prefix (default 0.1)

        Returns value between 0 and 1:
        1.0 = identical
        0.0 = no similarity
        """
        jaro = SimilarityMetrics.jaro_distance(str1, str2)

        # Find common prefix length (max 4)
        prefix = 0
        for i in range(min(len(str1), len(str2), 4)):
            if str1[i] == str2[i]:
                prefix += 1
            else:
                break

        return jaro + prefix * prefix_scale * (1 - jaro)


# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EDIT DISTANCE ALGORITHMS")
    print("=" * 70)

    # Example 1: Hamming distance
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Hamming Distance")
    print("=" * 70)

    str1 = "karolin"
    str2 = "kathrin"
    dist = EditDistance.hamming(str1, str2)

    print(f"String 1: '{str1}'")
    print(f"String 2: '{str2}'")
    print(f"Hamming distance: {dist}")

    # Example 2: Levenshtein distance
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Levenshtein Distance")
    print("=" * 70)

    str1 = "kitten"
    str2 = "sitting"
    dist = EditDistance.levenshtein(str1, str2, visualize=True)

    print(f"\nString 1: '{str1}'")
    print(f"String 2: '{str2}'")
    print(f"Levenshtein distance: {dist}")

    # Example 3: Damerau-Levenshtein distance
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Damerau-Levenshtein Distance (with transposition)")
    print("=" * 70)

    test_cases = [
        ("kitten", "sitting"),
        ("teh", "the"),
        ("abcd", "acbd"),
    ]

    for str1, str2 in test_cases:
        lev_dist = EditDistance.levenshtein(str1, str2)
        dam_lev_dist = EditDistance.damerau_levenshtein(str1, str2)

        print(f"\nString 1: '{str1}'")
        print(f"String 2: '{str2}'")
        print(f"  Levenshtein:         {lev_dist}")
        print(f"  Damerau-Levenshtein: {dam_lev_dist}")

    # Example 4: Longest Common Subsequence
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Longest Common Subsequence")
    print("=" * 70)

    str1 = "ABCDGH"
    str2 = "AEDFHR"
    lcs = EditDistance.lcs_string(str1, str2)

    print(f"String 1: '{str1}'")
    print(f"String 2: '{str2}'")
    print(f"LCS: '{lcs}' (length: {len(lcs)})")

    # Example 5: Edit sequence
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Edit Sequence")
    print("=" * 70)

    str1 = "saturday"
    str2 = "sunday"
    sequence = EditDistance.edit_sequence(str1, str2)

    print(f"String 1: '{str1}'")
    print(f"String 2: '{str2}'")
    print(f"\nEdit operations:")
    for op, pos, char in sequence:
        if op != 'match':
            print(f"  {op:12} at position {pos}: '{char}'")

    # Example 6: Similarity metrics
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Similarity Metrics")
    print("=" * 70)

    test_pairs = [
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("martha", "marhta"),
        ("dixon", "dicksonx"),
    ]

    for str1, str2 in test_pairs:
        norm_lev = SimilarityMetrics.normalized_levenshtein(str1, str2)
        sim_ratio = SimilarityMetrics.similarity_ratio(str1, str2)
        jaro = SimilarityMetrics.jaro_distance(str1, str2)
        jaro_winkler = SimilarityMetrics.jaro_winkler_distance(str1, str2)

        print(f"\n'{str1}' vs '{str2}':")
        print(f"  Normalized Levenshtein: {norm_lev:.4f}")
        print(f"  Similarity Ratio:       {sim_ratio:.4f}")
        print(f"  Jaro:                   {jaro:.4f}")
        print(f"  Jaro-Winkler:           {jaro_winkler:.4f}")

    # Example 7: Spell checking simulation
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Spell Checking Simulation")
    print("=" * 70)

    dictionary = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
    misspelled = "quikc"

    print(f"Misspelled word: '{misspelled}'")
    print(f"Dictionary: {dictionary}\n")

    suggestions = []
    for word in dictionary:
        dist = EditDistance.levenshtein(misspelled, word)
        suggestions.append((word, dist))

    suggestions.sort(key=lambda x: x[1])

    print("Suggestions (sorted by edit distance):")
    for word, dist in suggestions[:5]:
        print(f"  '{word}' (distance: {dist})")

    print("\n" + "=" * 70)
