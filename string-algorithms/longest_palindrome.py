"""
Longest Palindromic Substring Algorithms
========================================

Multiple algorithms for finding the longest palindromic substring in a string.

Algorithms included:
1. Manacher's Algorithm - O(n) time, O(n) space
2. Expand Around Center - O(n²) time, O(1) space
3. Dynamic Programming - O(n²) time, O(n²) space
4. Brute Force - O(n³) time, O(1) space (for comparison)

Applications:
- DNA sequence analysis
- Text processing
- Pattern recognition
- Data compression

References:
- Manacher, G. (1975). "A new linear-time on-line algorithm for finding
  the smallest initial palindrome of a string"
"""

from typing import List, Tuple
import time


class ManacherAlgorithm:
    """
    Manacher's algorithm for finding longest palindromic substring in O(n) time.

    This is the optimal algorithm for this problem.
    """

    @staticmethod
    def preprocess(text: str) -> str:
        """
        Transform string to handle even/odd length palindromes uniformly.

        Example: "aba" -> "#a#b#a#"

        Time: O(n)
        """
        if not text:
            return "#"

        result = "#"
        for char in text:
            result += char + "#"

        return result

    @staticmethod
    def longest_palindrome(text: str) -> str:
        """
        Find longest palindromic substring using Manacher's algorithm.

        Time: O(n)
        Space: O(n)

        Returns:
            Longest palindromic substring
        """
        if not text:
            return ""

        # Preprocess text
        s = ManacherAlgorithm.preprocess(text)
        n = len(s)

        # Array to store palindrome radius at each position
        p = [0] * n

        center = 0  # Center of rightmost palindrome
        right = 0   # Right boundary of rightmost palindrome

        max_len = 0
        max_center = 0

        for i in range(n):
            # Mirror of i with respect to center
            mirror = 2 * center - i

            # If i is within right boundary, use previously computed values
            if i < right:
                p[i] = min(right - i, p[mirror])

            # Try to expand palindrome centered at i
            try:
                while (i + p[i] + 1 < n and i - p[i] - 1 >= 0 and
                      s[i + p[i] + 1] == s[i - p[i] - 1]):
                    p[i] += 1
            except:
                pass

            # Update rightmost palindrome if needed
            if i + p[i] > right:
                center = i
                right = i + p[i]

            # Track longest palindrome
            if p[i] > max_len:
                max_len = p[i]
                max_center = i

        # Extract palindrome from original string
        start = (max_center - max_len) // 2
        return text[start:start + max_len]

    @staticmethod
    def find_all_palindromes(text: str, min_length: int = 1) -> List[Tuple[int, int, str]]:
        """
        Find all palindromic substrings using Manacher's algorithm.

        Time: O(n²) in worst case (all substrings are palindromes)

        Args:
            text: Input string
            min_length: Minimum palindrome length to return

        Returns:
            List of (start, end, palindrome_string) tuples
        """
        if not text:
            return []

        s = ManacherAlgorithm.preprocess(text)
        n = len(s)
        p = [0] * n

        center = 0
        right = 0

        for i in range(n):
            mirror = 2 * center - i

            if i < right:
                p[i] = min(right - i, p[mirror])

            try:
                while (i + p[i] + 1 < n and i - p[i] - 1 >= 0 and
                      s[i + p[i] + 1] == s[i - p[i] - 1]):
                    p[i] += 1
            except:
                pass

            if i + p[i] > right:
                center = i
                right = i + p[i]

        # Extract all palindromes
        palindromes = set()

        for i in range(n):
            for r in range(p[i], 0, -1):
                start = (i - r) // 2
                length = r
                if length >= min_length:
                    palindrome = text[start:start + length]
                    palindromes.add((start, start + length, palindrome))

        return sorted(list(palindromes))


class ExpandAroundCenter:
    """
    Expand around center algorithm - simple and intuitive.

    Time: O(n²)
    Space: O(1)
    """

    @staticmethod
    def expand(s: str, left: int, right: int) -> Tuple[int, int]:
        """
        Expand around center while characters match.

        Returns:
            (start, end) indices of palindrome
        """
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1

        return left + 1, right

    @staticmethod
    def longest_palindrome(text: str) -> str:
        """
        Find longest palindromic substring by expanding around centers.

        Time: O(n²)
        Space: O(1)
        """
        if not text:
            return ""

        max_start = 0
        max_len = 0

        for i in range(len(text)):
            # Check odd length palindromes (center is a character)
            left, right = ExpandAroundCenter.expand(text, i, i)
            if right - left > max_len:
                max_start = left
                max_len = right - left

            # Check even length palindromes (center is between characters)
            left, right = ExpandAroundCenter.expand(text, i, i + 1)
            if right - left > max_len:
                max_start = left
                max_len = right - left

        return text[max_start:max_start + max_len]

    @staticmethod
    def find_all_palindromes(text: str, min_length: int = 1) -> List[Tuple[int, int, str]]:
        """
        Find all palindromic substrings.

        Time: O(n²)
        """
        if not text:
            return []

        palindromes = set()

        for i in range(len(text)):
            # Odd length palindromes
            left, right = ExpandAroundCenter.expand(text, i, i)
            for start in range(left, i + 1):
                for end in range(i + 1, right + 1):
                    if end - start >= min_length and text[start:end] == text[start:end][::-1]:
                        palindromes.add((start, end, text[start:end]))

            # Even length palindromes
            left, right = ExpandAroundCenter.expand(text, i, i + 1)
            for start in range(left, i + 1):
                for end in range(i + 1, right + 1):
                    if end - start >= min_length and text[start:end] == text[start:end][::-1]:
                        palindromes.add((start, end, text[start:end]))

        return sorted(list(palindromes))


class DynamicProgramming:
    """
    Dynamic programming approach for longest palindromic substring.

    Time: O(n²)
    Space: O(n²)
    """

    @staticmethod
    def longest_palindrome(text: str) -> str:
        """
        Find longest palindromic substring using DP.

        Time: O(n²)
        Space: O(n²)

        DP formula:
        dp[i][j] = true if text[i:j+1] is palindrome
        dp[i][j] = (text[i] == text[j]) and dp[i+1][j-1]
        """
        if not text:
            return ""

        n = len(text)
        dp = [[False] * n for _ in range(n)]

        max_start = 0
        max_len = 1

        # All single characters are palindromes
        for i in range(n):
            dp[i][i] = True

        # Check for length 2
        for i in range(n - 1):
            if text[i] == text[i + 1]:
                dp[i][i + 1] = True
                max_start = i
                max_len = 2

        # Check for lengths greater than 2
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1

                if text[i] == text[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True

                    if length > max_len:
                        max_start = i
                        max_len = length

        return text[max_start:max_start + max_len]

    @staticmethod
    def find_all_palindromes(text: str, min_length: int = 1) -> List[Tuple[int, int, str]]:
        """
        Find all palindromic substrings using DP.

        Time: O(n²)
        Space: O(n²)
        """
        if not text:
            return []

        n = len(text)
        dp = [[False] * n for _ in range(n)]
        palindromes = []

        # Single characters
        for i in range(n):
            dp[i][i] = True
            if 1 >= min_length:
                palindromes.append((i, i + 1, text[i]))

        # Length 2
        for i in range(n - 1):
            if text[i] == text[i + 1]:
                dp[i][i + 1] = True
                if 2 >= min_length:
                    palindromes.append((i, i + 2, text[i:i + 2]))

        # Length 3 and above
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1

                if text[i] == text[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    if length >= min_length:
                        palindromes.append((i, j + 1, text[i:j + 1]))

        return palindromes


class BruteForce:
    """
    Brute force approach - check all substrings.

    Time: O(n³)
    Space: O(1)

    Only for educational purposes and small inputs.
    """

    @staticmethod
    def is_palindrome(s: str) -> bool:
        """Check if string is palindrome."""
        return s == s[::-1]

    @staticmethod
    def longest_palindrome(text: str) -> str:
        """
        Find longest palindromic substring by checking all substrings.

        Time: O(n³)
        """
        if not text:
            return ""

        max_palindrome = ""

        for i in range(len(text)):
            for j in range(i + 1, len(text) + 1):
                substring = text[i:j]
                if BruteForce.is_palindrome(substring):
                    if len(substring) > len(max_palindrome):
                        max_palindrome = substring

        return max_palindrome


# ============================================================================
# UTILITIES AND APPLICATIONS
# ============================================================================

def count_palindromic_substrings(text: str) -> int:
    """
    Count total number of palindromic substrings.

    Time: O(n²) using expand around center

    Returns:
        Count of palindromic substrings
    """
    count = 0

    for i in range(len(text)):
        # Odd length palindromes
        left = right = i
        while left >= 0 and right < len(text) and text[left] == text[right]:
            count += 1
            left -= 1
            right += 1

        # Even length palindromes
        left, right = i, i + 1
        while left >= 0 and right < len(text) and text[left] == text[right]:
            count += 1
            left -= 1
            right += 1

    return count


def longest_palindrome_by_removing_one(text: str) -> str:
    """
    Find longest palindrome that can be formed by removing at most one character.

    Time: O(n²)
    """
    def is_palindrome_range(s: str, left: int, right: int) -> bool:
        """Check if s[left:right+1] is palindrome."""
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    # First check if already palindrome
    if text == text[::-1]:
        return text

    # Try removing each character
    max_len = 0
    result = ""

    for i in range(len(text)):
        # Create string with character at i removed
        modified = text[:i] + text[i + 1:]

        # Check if it's palindrome
        if modified == modified[::-1] and len(modified) > max_len:
            max_len = len(modified)
            result = modified

    return result


# ============================================================================
# BENCHMARKING
# ============================================================================

def benchmark_algorithms():
    """Compare performance of different algorithms."""
    print("=" * 70)
    print("Algorithm Performance Comparison")
    print("=" * 70)

    test_cases = [
        ("babad", "Short"),
        ("cbbd", "Short even"),
        ("a" * 100 + "b" + "a" * 100, "Long palindrome"),
        ("abcdefghijklmnop" * 5, "Long non-palindrome"),
    ]

    algorithms = [
        ("Manacher", ManacherAlgorithm.longest_palindrome),
        ("Expand Around Center", ExpandAroundCenter.longest_palindrome),
        ("Dynamic Programming", DynamicProgramming.longest_palindrome),
    ]

    for text, description in test_cases:
        print(f"\n{description} (length {len(text)}):")
        print("-" * 50)

        for name, func in algorithms:
            start = time.perf_counter()
            result = func(text)
            elapsed = (time.perf_counter() - start) * 1000

            print(f"{name:25} : {elapsed:8.4f} ms -> '{result[:20]}...'")


# ============================================================================
# EXAMPLES
# ============================================================================

def example_compare_algorithms():
    """Show outputs from every palindrome solver on the same input text."""
    print("=" * 70)
    print("EXAMPLE 1: Compare Different Algorithms")
    print("=" * 70)

    text = "babad"

    print(f"Text: '{text}'\n")

    # Manacher's algorithm
    result = ManacherAlgorithm.longest_palindrome(text)
    print(f"Manacher's Algorithm:      '{result}'")

    # Expand around center
    result = ExpandAroundCenter.longest_palindrome(text)
    print(f"Expand Around Center:      '{result}'")

    # Dynamic programming
    result = DynamicProgramming.longest_palindrome(text)
    print(f"Dynamic Programming:       '{result}'")

    # Brute force (only for small strings)
    result = BruteForce.longest_palindrome(text)
    print(f"Brute Force:               '{result}'")

    print()


def example_find_all_palindromes():
    """Demonstrate enumerating palindromic substrings with metadata."""
    print("=" * 70)
    print("EXAMPLE 2: Find All Palindromic Substrings")
    print("=" * 70)

    text = "abba"

    palindromes = ManacherAlgorithm.find_all_palindromes(text, min_length=2)

    print(f"Text: '{text}'")
    print(f"Found {len(palindromes)} palindromes (length >= 2):\n")

    for start, end, pal in palindromes:
        print(f"  [{start}:{end}] = '{pal}'")

    print()


def example_count_palindromes():
    """Count palindromic substrings for several sample strings."""
    print("=" * 70)
    print("EXAMPLE 3: Count Palindromic Substrings")
    print("=" * 70)

    texts = ["abc", "aaa", "abba", "racecar"]

    for text in texts:
        count = count_palindromic_substrings(text)
        print(f"'{text}': {count} palindromic substrings")

    print()


def example_palindrome_variations():
    """Explore tolerant palindrome variants (e.g., remove-one heuristics)."""
    print("=" * 70)
    print("EXAMPLE 4: Palindrome Variations")
    print("=" * 70)

    text = "abcdef"

    result = longest_palindrome_by_removing_one(text)
    print(f"Text: '{text}'")
    print(f"Longest palindrome by removing one char: '{result}'")

    text = "racecar"
    result = longest_palindrome_by_removing_one(text)
    print(f"\nText: '{text}'")
    print(f"Longest palindrome by removing one char: '{result}'")

    print()


if __name__ == "__main__":
    print("=" * 70)
    print("LONGEST PALINDROMIC SUBSTRING ALGORITHMS")
    print("=" * 70)
    print()

    example_compare_algorithms()
    example_find_all_palindromes()
    example_count_palindromes()
    example_palindrome_variations()
    benchmark_algorithms()

    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
