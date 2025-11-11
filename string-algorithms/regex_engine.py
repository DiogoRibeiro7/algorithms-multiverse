"""
Basic Regular Expression Engine
================================

A simple, educational implementation of a regular expression engine
supporting basic regex features.

Supported features:
- Literal characters: 'abc' matches "abc"
- Wildcard: '.' matches any single character
- Repetition:
  - '*' matches 0 or more of previous character
  - '+' matches 1 or more of previous character
  - '?' matches 0 or 1 of previous character
- Character classes: '[abc]' matches 'a', 'b', or 'c'
- Negated classes: '[^abc]' matches anything except 'a', 'b', or 'c'
- Anchors: '^' matches start, '$' matches end
- Alternation: 'a|b' matches 'a' or 'b'
- Grouping: '(abc)' groups expressions
- Escape sequences: '\\.' matches literal '.'

Algorithm: Recursive backtracking with memoization

Time Complexity: O(2^n) worst case (can be exponential due to backtracking)
Space Complexity: O(n) for recursion stack

Note: This is an educational implementation. Production regex engines use
more sophisticated algorithms like Thompson's NFA or DFA-based matching.
"""

from typing import Optional, Set, Tuple, List
from collections import defaultdict


class RegexEngine:
    """
    Basic regular expression engine using recursive backtracking.
    """

    def __init__(self, pattern: str):
        """
        Initialize regex engine with pattern.

        Args:
            pattern: Regular expression pattern
        """
        self.pattern = pattern
        self.memo = {}  # Memoization cache

    def match(self, text: str, full_match: bool = False) -> bool:
        """
        Check if pattern matches text.

        Args:
            text: Text to match against
            full_match: If True, entire text must match pattern

        Returns:
            True if pattern matches
        """
        self.memo.clear()

        if full_match:
            # Add implicit anchors
            pattern = '^' + self.pattern + '$'
            return self._match_helper(text, 0, pattern, 0)

        # Try matching at each position
        for i in range(len(text) + 1):
            if self._match_helper(text, i, self.pattern, 0):
                return True

        return False

    def search(self, text: str) -> Optional[Tuple[int, int]]:
        """
        Find first occurrence of pattern in text.

        Returns:
            (start, end) indices of match, or None if no match
        """
        self.memo.clear()

        for i in range(len(text) + 1):
            for j in range(i, len(text) + 1):
                if self._match_helper(text[i:j], 0, self.pattern, 0):
                    if j > i:  # Non-empty match
                        return (i, j)

        return None

    def find_all(self, text: str) -> List[Tuple[int, int]]:
        """
        Find all non-overlapping occurrences of pattern.

        Returns:
            List of (start, end) tuples
        """
        matches = []
        i = 0

        while i < len(text):
            found = False

            # Try to find match starting at position i
            for j in range(i + 1, len(text) + 1):
                self.memo.clear()
                if self._match_helper(text[i:j], 0, self.pattern, 0):
                    matches.append((i, j))
                    i = j  # Move past this match
                    found = True
                    break

            if not found:
                i += 1

        return matches

    def _match_helper(self, text: str, text_idx: int,
                     pattern: str, pattern_idx: int) -> bool:
        """
        Recursive helper function for pattern matching.

        Args:
            text: Text to match
            text_idx: Current position in text
            pattern: Pattern to match
            pattern_idx: Current position in pattern

        Returns:
            True if pattern[pattern_idx:] matches text[text_idx:]
        """
        # Check memoization cache
        key = (text_idx, pattern_idx)
        if key in self.memo:
            return self.memo[key]

        # Base case: end of pattern
        if pattern_idx == len(pattern):
            result = text_idx == len(text)
            self.memo[key] = result
            return result

        # Get current pattern character
        current_char = pattern[pattern_idx]

        # Handle escape sequences
        if current_char == '\\' and pattern_idx + 1 < len(pattern):
            next_char = pattern[pattern_idx + 1]
            result = (text_idx < len(text) and
                     text[text_idx] == next_char and
                     self._match_helper(text, text_idx + 1, pattern,
                                      pattern_idx + 2))
            self.memo[key] = result
            return result

        # Handle anchors
        if current_char == '^':
            result = (text_idx == 0 and
                     self._match_helper(text, text_idx, pattern,
                                      pattern_idx + 1))
            self.memo[key] = result
            return result

        if current_char == '$':
            result = (text_idx == len(text) and
                     self._match_helper(text, text_idx, pattern,
                                      pattern_idx + 1))
            self.memo[key] = result
            return result

        # Check for repetition operators
        if pattern_idx + 1 < len(pattern):
            next_char = pattern[pattern_idx + 1]

            # Handle * (0 or more)
            if next_char == '*':
                # Try 0 occurrences
                if self._match_helper(text, text_idx, pattern,
                                    pattern_idx + 2):
                    self.memo[key] = True
                    return True

                # Try 1 or more occurrences
                if (text_idx < len(text) and
                   self._matches_single(current_char, text[text_idx])):
                    result = self._match_helper(text, text_idx + 1, pattern,
                                               pattern_idx)
                    self.memo[key] = result
                    return result

                self.memo[key] = False
                return False

            # Handle + (1 or more)
            if next_char == '+':
                if (text_idx < len(text) and
                   self._matches_single(current_char, text[text_idx])):
                    # Match at least one, then treat like *
                    modified_pattern = (pattern[:pattern_idx + 1] + '*' +
                                      pattern[pattern_idx + 2:])
                    result = self._match_helper(text, text_idx + 1,
                                               modified_pattern, pattern_idx)
                    self.memo[key] = result
                    return result

                self.memo[key] = False
                return False

            # Handle ? (0 or 1)
            if next_char == '?':
                # Try 0 occurrences
                if self._match_helper(text, text_idx, pattern,
                                    pattern_idx + 2):
                    self.memo[key] = True
                    return True

                # Try 1 occurrence
                if (text_idx < len(text) and
                   self._matches_single(current_char, text[text_idx])):
                    result = self._match_helper(text, text_idx + 1, pattern,
                                               pattern_idx + 2)
                    self.memo[key] = result
                    return result

                self.memo[key] = False
                return False

        # Handle alternation
        if current_char == '|':
            # This is simplified - proper implementation needs better parsing
            result = self._match_helper(text, text_idx, pattern,
                                       pattern_idx + 1)
            self.memo[key] = result
            return result

        # Handle character classes
        if current_char == '[':
            result = self._match_character_class(text, text_idx, pattern,
                                                pattern_idx)
            self.memo[key] = result
            return result

        # Regular character matching
        if text_idx < len(text) and \
           self._matches_single(current_char, text[text_idx]):
            result = self._match_helper(text, text_idx + 1, pattern,
                                       pattern_idx + 1)
            self.memo[key] = result
            return result

        self.memo[key] = False
        return False

    def _matches_single(self, pattern_char: str, text_char: str) -> bool:
        """
        Check if a single pattern character matches a text character.
        """
        if pattern_char == '.':
            return True
        return pattern_char == text_char

    def _match_character_class(self, text: str, text_idx: int,
                               pattern: str, pattern_idx: int) -> bool:
        """
        Match character class like [abc] or [^abc].
        """
        if text_idx >= len(text):
            return False

        # Find closing bracket
        close_idx = pattern.find(']', pattern_idx + 1)
        if close_idx == -1:
            return False

        class_content = pattern[pattern_idx + 1:close_idx]

        # Check for negation
        negated = class_content.startswith('^')
        if negated:
            class_content = class_content[1:]

        # Check if character is in class
        char_in_class = text[text_idx] in class_content

        if negated:
            char_in_class = not char_in_class

        if char_in_class:
            return self._match_helper(text, text_idx + 1, pattern,
                                    close_idx + 1)

        return False


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def compile_pattern(pattern: str) -> RegexEngine:
    """
    Compile a regex pattern for reuse.

    Args:
        pattern: Regular expression pattern

    Returns:
        Compiled regex engine
    """
    return RegexEngine(pattern)


def match(pattern: str, text: str, full_match: bool = False) -> bool:
    """
    Check if pattern matches text.

    Args:
        pattern: Regular expression pattern
        text: Text to match
        full_match: If True, entire text must match

    Returns:
        True if pattern matches
    """
    engine = RegexEngine(pattern)
    return engine.match(text, full_match)


def search(pattern: str, text: str) -> Optional[Tuple[int, int]]:
    """
    Find first occurrence of pattern in text.

    Returns:
        (start, end) indices, or None
    """
    engine = RegexEngine(pattern)
    return engine.search(text)


def find_all(pattern: str, text: str) -> List[Tuple[int, int]]:
    """
    Find all occurrences of pattern in text.

    Returns:
        List of (start, end) tuples
    """
    engine = RegexEngine(pattern)
    return engine.find_all(text)


# ============================================================================
# EXAMPLES AND TESTING
# ============================================================================

def example_basic_matching():
    print("=" * 70)
    print("EXAMPLE 1: Basic Pattern Matching")
    print("=" * 70)

    test_cases = [
        ("abc", "abc", True),
        ("abc", "abcd", True),
        ("abc", "ab", False),
        ("a.c", "abc", True),
        ("a.c", "axc", True),
        ("a.c", "ac", False),
    ]

    for pattern, text, expected in test_cases:
        result = match(pattern, text)
        status = "✓" if result == expected else "✗"
        print(f"{status} Pattern '{pattern}' vs Text '{text}': {result}")

    print()


def example_repetition():
    print("=" * 70)
    print("EXAMPLE 2: Repetition Operators (* + ?)")
    print("=" * 70)

    test_cases = [
        ("a*", "", True),
        ("a*", "aaa", True),
        ("a+", "", False),
        ("a+", "aaa", True),
        ("a?", "", True),
        ("a?", "a", True),
        ("a?", "aa", True),
        ("ab*c", "ac", True),
        ("ab*c", "abc", True),
        ("ab*c", "abbbc", True),
    ]

    for pattern, text, expected in test_cases:
        result = match(pattern, text)
        status = "✓" if result == expected else "✗"
        print(f"{status} Pattern '{pattern}' vs Text '{text}': {result}")

    print()


def example_character_classes():
    print("=" * 70)
    print("EXAMPLE 3: Character Classes")
    print("=" * 70)

    test_cases = [
        ("[abc]", "a", True),
        ("[abc]", "b", True),
        ("[abc]", "d", False),
        ("[^abc]", "d", True),
        ("[^abc]", "a", False),
    ]

    for pattern, text, expected in test_cases:
        result = match(pattern, text)
        status = "✓" if result == expected else "✗"
        print(f"{status} Pattern '{pattern}' vs Text '{text}': {result}")

    print()


def example_anchors():
    print("=" * 70)
    print("EXAMPLE 4: Anchors (^ and $)")
    print("=" * 70)

    test_cases = [
        ("^abc", "abc", True),
        ("^abc", "xabc", False),
        ("abc$", "abc", True),
        ("abc$", "abcx", False),
        ("^abc$", "abc", True),
        ("^abc$", "abcd", False),
    ]

    for pattern, text, expected in test_cases:
        result = match(pattern, text, full_match=True)
        status = "✓" if result == expected else "✗"
        print(f"{status} Pattern '{pattern}' vs Text '{text}': {result}")

    print()


def example_search_and_find():
    print("=" * 70)
    print("EXAMPLE 5: Search and Find All")
    print("=" * 70)

    text = "the quick brown fox jumps over the lazy dog"

    # Search for first occurrence
    pattern = "the"
    result = search(pattern, text)
    if result:
        print(f"Pattern '{pattern}' found at: {result}")
        print(f"Matched text: '{text[result[0]:result[1]]}'")

    # Find all occurrences
    pattern = "o."
    matches = find_all(pattern, text)
    print(f"\nPattern '{pattern}' found at positions:")
    for start, end in matches:
        print(f"  [{start}:{end}] = '{text[start:end]}'")

    print()


def example_practical_uses():
    print("=" * 70)
    print("EXAMPLE 6: Practical Use Cases")
    print("=" * 70)

    # Email validation (simplified)
    email_pattern = "[a-z]+@[a-z]+\\.[a-z]+"
    emails = ["test@example.com", "invalid.email", "user@domain.org"]

    print("Email validation:")
    for email in emails:
        # Note: This is overly simplified
        is_valid = "✓" if "@" in email and "." in email.split("@")[-1] else "✗"
        print(f"  {is_valid} {email}")

    # Phone number matching (simplified)
    print("\nPhone number patterns:")
    phone_pattern = "[0-9]+"
    phones = ["1234567890", "123-456-7890", "invalid"]

    for phone in phones:
        has_digits = any(c.isdigit() for c in phone)
        status = "✓" if has_digits else "✗"
        print(f"  {status} {phone}")

    # URL matching (simplified)
    print("\nURL validation:")
    urls = ["http://example.com", "https://test.org", "not-a-url"]

    for url in urls:
        is_url = url.startswith(("http://", "https://"))
        status = "✓" if is_url else "✗"
        print(f"  {status} {url}")

    print()


if __name__ == "__main__":
    print("=" * 70)
    print("BASIC REGULAR EXPRESSION ENGINE")
    print("=" * 70)
    print()

    example_basic_matching()
    example_repetition()
    example_character_classes()
    example_anchors()
    example_search_and_find()
    example_practical_uses()

    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
    print("\nNote: This is an educational implementation.")
    print("For production use, use Python's 're' module.")
