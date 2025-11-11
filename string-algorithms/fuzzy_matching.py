"""
String Hashing and Fuzzy Matching
==================================

This module implements various string hashing functions and fuzzy
matching algorithms.

Features:
1. Multiple hash functions (polynomial, MurmurHash, etc.)
2. Rolling hash for substring matching
3. Fuzzy string matching algorithms
4. Phonetic algorithms (Soundex, Metaphone)
5. Approximate string matching
6. String similarity search

Applications:
- Duplicate detection
- Spell checking
- Record linkage
- Search with typos
- Data deduplication
"""

import hashlib
from typing import List, Tuple, Set, Dict, Optional
import re


class StringHash:
    """
    Various string hashing functions.
    """

    @staticmethod
    def polynomial_hash(s: str, base: int = 31, mod: int = 10**9 + 9) -> int:
        """
        Polynomial rolling hash.

        hash = (s[0] * base^(n-1) + s[1] * base^(n-2) + ... + s[n-1]) mod mod

        Time: O(n)

        Good for: Pattern matching, substring search
        """
        hash_value = 0
        power = 1

        for char in s:
            hash_value = (hash_value + ord(char) * power) % mod
            power = (power * base) % mod

        return hash_value

    @staticmethod
    def fnv1a_hash(s: str) -> int:
        """
        FNV-1a hash (Fowler-Noll-Vo).

        Fast, good distribution.

        Time: O(n)
        """
        FNV_prime = 0x01000193
        FNV_offset_basis = 0x811c9dc5

        hash_value = FNV_offset_basis

        for char in s:
            hash_value ^= ord(char)
            hash_value = (hash_value * FNV_prime) & 0xFFFFFFFF

        return hash_value

    @staticmethod
    def djb2_hash(s: str) -> int:
        """
        DJB2 hash by Dan Bernstein.

        Simple and effective.

        Time: O(n)
        """
        hash_value = 5381

        for char in s:
            hash_value = ((hash_value << 5) + hash_value) + ord(char)

        return hash_value & 0xFFFFFFFF

    @staticmethod
    def murmur_hash3_32(s: str, seed: int = 0) -> int:
        """
        Simplified MurmurHash3 (32-bit).

        Very good distribution and speed.

        Time: O(n)
        """
        data = s.encode('utf-8')
        c1 = 0xcc9e2d51
        c2 = 0x1b873593
        r1 = 15
        r2 = 13
        m = 5
        n = 0xe6546b64

        hash_value = seed

        # Process data in 4-byte chunks
        for i in range(0, len(data) - 3, 4):
            k = int.from_bytes(data[i:i+4], 'little')

            k = (k * c1) & 0xFFFFFFFF
            k = ((k << r1) | (k >> (32 - r1))) & 0xFFFFFFFF
            k = (k * c2) & 0xFFFFFFFF

            hash_value ^= k
            hash_value = ((hash_value << r2) | (hash_value >> (32 - r2))) & 0xFFFFFFFF
            hash_value = (hash_value * m + n) & 0xFFFFFFFF

        # Process remaining bytes
        remaining = len(data) % 4
        if remaining > 0:
            k = 0
            for i in range(remaining):
                k |= data[len(data) - remaining + i] << (8 * i)

            k = (k * c1) & 0xFFFFFFFF
            k = ((k << r1) | (k >> (32 - r1))) & 0xFFFFFFFF
            k = (k * c2) & 0xFFFFFFFF

            hash_value ^= k

        # Finalization
        hash_value ^= len(data)
        hash_value ^= (hash_value >> 16)
        hash_value = (hash_value * 0x85ebca6b) & 0xFFFFFFFF
        hash_value ^= (hash_value >> 13)
        hash_value = (hash_value * 0xc2b2ae35) & 0xFFFFFFFF
        hash_value ^= (hash_value >> 16)

        return hash_value

    @staticmethod
    def cryptographic_hash(s: str, algorithm: str = 'sha256') -> str:
        """
        Cryptographic hash functions.

        Args:
            s: Input string
            algorithm: 'md5', 'sha1', 'sha256', 'sha512'

        Returns: Hex digest
        """
        data = s.encode('utf-8')

        if algorithm == 'md5':
            return hashlib.md5(data).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(data).hexdigest()
        elif algorithm == 'sha256':
            return hashlib.sha256(data).hexdigest()
        elif algorithm == 'sha512':
            return hashlib.sha512(data).hexdigest()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")


class RollingHash:
    """
    Rolling hash for efficient substring operations.
    """

    def __init__(self, base: int = 31, mod: int = 10**9 + 9):
        self.base = base
        self.mod = mod

    def compute(self, s: str) -> int:
        """
        Compute initial hash.
        """
        hash_value = 0
        power = 1

        for char in s:
            hash_value = (hash_value + ord(char) * power) % self.mod
            power = (power * self.base) % self.mod

        return hash_value

    def roll(self, old_hash: int, old_char: str, new_char: str, window_size: int) -> int:
        """
        Update hash by rolling window.

        Remove old_char from left, add new_char to right.

        Time: O(1)
        """
        # Remove old character
        old_hash = (old_hash - ord(old_char)) % self.mod
        if old_hash < 0:
            old_hash += self.mod

        # Divide by base
        old_hash = (old_hash * pow(self.base, self.mod - 2, self.mod)) % self.mod

        # Add new character
        power = pow(self.base, window_size - 1, self.mod)
        new_hash = (old_hash + ord(new_char) * power) % self.mod

        return new_hash


class PhoneticAlgorithms:
    """
    Phonetic algorithms for fuzzy matching.
    """

    @staticmethod
    def soundex(name: str) -> str:
        """
        Soundex algorithm - encodes names phonetically.

        Time: O(n)

        Rules:
        1. Keep first letter
        2. Replace consonants with digits:
           - b,f,p,v -> 1
           - c,g,j,k,q,s,x,z -> 2
           - d,t -> 3
           - l -> 4
           - m,n -> 5
           - r -> 6
        3. Remove vowels (a,e,i,o,u,h,w,y)
        4. Remove duplicate adjacent digits
        5. Pad with zeros to length 4

        Good for: Name matching, handling misspellings
        """
        if not name:
            return "0000"

        name = name.upper()

        # Soundex mapping
        soundex_mapping = {
            'B': '1', 'F': '1', 'P': '1', 'V': '1',
            'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
            'D': '3', 'T': '3',
            'L': '4',
            'M': '5', 'N': '5',
            'R': '6'
        }

        # Keep first letter
        result = name[0]

        # Process rest of name
        prev_code = soundex_mapping.get(name[0], '0')

        for char in name[1:]:
            code = soundex_mapping.get(char, '0')

            # Skip vowels and duplicates
            if code != '0' and code != prev_code:
                result += code
                prev_code = code

            # Only 4 characters
            if len(result) == 4:
                break

        # Pad with zeros
        result += '0' * (4 - len(result))

        return result[:4]

    @staticmethod
    def metaphone(word: str, max_length: int = 4) -> str:
        """
        Simplified Metaphone algorithm.

        More accurate than Soundex for English words.

        Time: O(n)

        Note: This is a simplified version. For production,
        use a full implementation or library.

        Good for: English word matching, spell checking
        """
        if not word:
            return ""

        word = word.upper()

        # Remove non-alphabetic characters
        word = ''.join(c for c in word if c.isalpha())

        if not word:
            return ""

        result = []

        # Simplified rules
        i = 0
        while i < len(word) and len(result) < max_length:
            char = word[i]

            if char in 'AEIOU':
                if i == 0:
                    result.append(char)
            elif char == 'B':
                if i + 1 < len(word) and word[i + 1] != 'B':
                    result.append('B')
            elif char in 'FVWJZ':
                result.append(char)
            elif char in 'KCQ':
                result.append('K')
            elif char in 'GJ':
                result.append('J')
            elif char in 'SXZ':
                result.append('S')
            elif char in 'DT':
                result.append('T')
            elif char == 'L':
                result.append('L')
            elif char in 'MN':
                result.append('N')
            elif char == 'R':
                result.append('R')

            i += 1

        return ''.join(result)[:max_length]


class FuzzyMatcher:
    """
    Fuzzy string matching utilities.
    """

    @staticmethod
    def hamming_distance(s1: str, s2: str) -> int:
        """
        Hamming distance - number of differing positions.

        Requires equal length strings.
        """
        if len(s1) != len(s2):
            raise ValueError("Hamming distance requires equal length strings")

        return sum(c1 != c2 for c1, c2 in zip(s1, s2))

    @staticmethod
    def fuzzy_search(text: str, pattern: str, max_errors: int = 2) -> List[Tuple[int, int]]:
        """
        Approximate string matching with bounded errors.

        Find all occurrences of pattern in text with at most max_errors mismatches.

        Time: O(nm) where n=len(text), m=len(pattern)

        Returns: List of (position, errors) tuples
        """
        results = []
        n = len(text)
        m = len(pattern)

        for i in range(n - m + 1):
            substring = text[i:i + m]
            errors = sum(c1 != c2 for c1, c2 in zip(substring, pattern))

            if errors <= max_errors:
                results.append((i, errors))

        return results

    @staticmethod
    def wildcard_match(text: str, pattern: str) -> bool:
        """
        Match text against pattern with wildcards.

        Wildcards:
        - '?' matches any single character
        - '*' matches any sequence of characters

        Time: O(nm) worst case

        Returns: True if pattern matches text
        """
        m, n = len(text), len(pattern)

        # DP table
        dp = [[False] * (n + 1) for _ in range(m + 1)]

        # Empty pattern matches empty text
        dp[0][0] = True

        # Handle leading '*'
        for j in range(1, n + 1):
            if pattern[j - 1] == '*':
                dp[0][j] = dp[0][j - 1]

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if pattern[j - 1] == '*':
                    # * matches empty or one+ characters
                    dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
                elif pattern[j - 1] == '?' or text[i - 1] == pattern[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]

        return dp[m][n]

    @staticmethod
    def regex_match_simple(text: str, pattern: str) -> bool:
        """
        Very simple regex matcher (educational).

        Supports:
        - . (any character)
        - * (zero or more of previous)
        - Character literals

        Time: O(2^n) worst case (backtracking)

        Note: This is for educational purposes only.
        Use Python's re module for production.
        """
        def match_helper(t_idx: int, p_idx: int) -> bool:
            # Base cases
            if p_idx == len(pattern):
                return t_idx == len(text)

            # Check if next character is *
            has_star = p_idx + 1 < len(pattern) and pattern[p_idx + 1] == '*'

            if has_star:
                # Try matching zero occurrences
                if match_helper(t_idx, p_idx + 2):
                    return True

                # Try matching one or more occurrences
                if t_idx < len(text):
                    if pattern[p_idx] == '.' or pattern[p_idx] == text[t_idx]:
                        return match_helper(t_idx + 1, p_idx)

                return False
            else:
                # No star, must match current character
                if t_idx < len(text):
                    if pattern[p_idx] == '.' or pattern[p_idx] == text[t_idx]:
                        return match_helper(t_idx + 1, p_idx + 1)

                return False

        return match_helper(0, 0)


class SimilaritySearch:
    """
    Find similar strings in a collection.
    """

    def __init__(self, strings: List[str]):
        """
        Initialize with a collection of strings.
        """
        self.strings = strings
        self.soundex_index = {}
        self.metaphone_index = {}

        # Build phonetic indices
        for s in strings:
            soundex = PhoneticAlgorithms.soundex(s)
            metaphone = PhoneticAlgorithms.metaphone(s)

            if soundex not in self.soundex_index:
                self.soundex_index[soundex] = []
            self.soundex_index[soundex].append(s)

            if metaphone not in self.metaphone_index:
                self.metaphone_index[metaphone] = []
            self.metaphone_index[metaphone].append(s)

    def find_similar_soundex(self, query: str) -> List[str]:
        """
        Find strings with same Soundex encoding.
        """
        soundex = PhoneticAlgorithms.soundex(query)
        return self.soundex_index.get(soundex, [])

    def find_similar_metaphone(self, query: str) -> List[str]:
        """
        Find strings with same Metaphone encoding.
        """
        metaphone = PhoneticAlgorithms.metaphone(query)
        return self.metaphone_index.get(metaphone, [])

    def find_similar_edit_distance(self, query: str, max_distance: int = 2) -> List[Tuple[str, int]]:
        """
        Find strings within edit distance.

        Returns: List of (string, distance) tuples
        """
        from edit_distance import EditDistance

        results = []
        for s in self.strings:
            distance = EditDistance.levenshtein(query, s)
            if distance <= max_distance:
                results.append((s, distance))

        return sorted(results, key=lambda x: x[1])


# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("STRING HASHING AND FUZZY MATCHING")
    print("=" * 70)

    # Example 1: String Hashing
    print("\n" + "=" * 70)
    print("EXAMPLE 1: String Hashing")
    print("=" * 70)

    test_string = "hello world"

    print(f"String: '{test_string}'\n")
    print("Hash functions:")
    print(f"  Polynomial: {StringHash.polynomial_hash(test_string)}")
    print(f"  FNV-1a:     {StringHash.fnv1a_hash(test_string)}")
    print(f"  DJB2:       {StringHash.djb2_hash(test_string)}")
    print(f"  MurmurHash3:{StringHash.murmur_hash3_32(test_string)}")
    print(f"  SHA-256:    {StringHash.cryptographic_hash(test_string, 'sha256')[:32]}...")

    # Example 2: Rolling Hash
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Rolling Hash")
    print("=" * 70)

    text = "abcdefgh"
    window_size = 3

    roller = RollingHash()

    print(f"Text: '{text}'")
    print(f"Window size: {window_size}\n")

    # Compute initial hash
    window = text[:window_size]
    hash_val = roller.compute(window)
    print(f"Window '{window}': hash = {hash_val}")

    # Roll through text
    for i in range(window_size, len(text)):
        old_char = text[i - window_size]
        new_char = text[i]
        window = text[i - window_size + 1:i + 1]

        hash_val = roller.roll(hash_val, old_char, new_char, window_size)
        print(f"Window '{window}': hash = {hash_val}")

    # Example 3: Soundex
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Soundex Algorithm")
    print("=" * 70)

    names = [
        ("Smith", "Smythe"),
        ("Johnson", "Jonson"),
        ("Williams", "Wiliams"),
        ("Robert", "Rupert"),
        ("Jackson", "Jacson")
    ]

    print("Name pairs and their Soundex codes:")
    for name1, name2 in names:
        code1 = PhoneticAlgorithms.soundex(name1)
        code2 = PhoneticAlgorithms.soundex(name2)
        match = "✓" if code1 == code2 else "✗"

        print(f"  {name1:12} ({code1}) vs {name2:12} ({code2}) {match}")

    # Example 4: Metaphone
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Metaphone Algorithm")
    print("=" * 70)

    words = [
        ("knight", "night"),
        ("phone", "fone"),
        ("write", "right"),
        ("their", "there"),
    ]

    print("Word pairs and their Metaphone codes:")
    for word1, word2 in words:
        code1 = PhoneticAlgorithms.metaphone(word1)
        code2 = PhoneticAlgorithms.metaphone(word2)
        match = "✓" if code1 == code2 else "✗"

        print(f"  {word1:10} ({code1:4}) vs {word2:10} ({code2:4}) {match}")

    # Example 5: Fuzzy Search
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Fuzzy Search (Approximate Matching)")
    print("=" * 70)

    text = "the quick brown fox jumps over the lazy dog"
    pattern = "quik"
    max_errors = 1

    matches = FuzzyMatcher.fuzzy_search(text, pattern, max_errors)

    print(f"Text: '{text}'")
    print(f"Pattern: '{pattern}' (max errors: {max_errors})")
    print(f"\nMatches:")
    for pos, errors in matches:
        matched = text[pos:pos + len(pattern)]
        print(f"  Position {pos}: '{matched}' ({errors} errors)")

    # Example 6: Wildcard Matching
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Wildcard Matching")
    print("=" * 70)

    test_cases = [
        ("hello", "h*o", True),
        ("hello", "h?llo", True),
        ("hello", "h?l*", True),
        ("hello", "h*l*o", True),
        ("hello", "world", False),
    ]

    print("Pattern matching with wildcards:")
    for text, pattern, expected in test_cases:
        result = FuzzyMatcher.wildcard_match(text, pattern)
        status = "✓" if result == expected else "✗"
        print(f"  '{text}' matches '{pattern}': {result} {status}")

    # Example 7: Simple Regex
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Simple Regex Matcher")
    print("=" * 70)

    test_cases = [
        ("abc", "a.c", True),
        ("abc", "a*bc", True),
        ("aaa", "a*", True),
        ("ab", ".*", True),
        ("mississippi", "mis*is*p*.", True),
    ]

    print("Simple regex matching:")
    for text, pattern, expected in test_cases:
        result = FuzzyMatcher.regex_match_simple(text, pattern)
        status = "✓" if result == expected else "✗"
        print(f"  '{text}' matches '{pattern}': {result} {status}")

    # Example 8: Similarity Search
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Similarity Search")
    print("=" * 70)

    # Dictionary of names
    names_dict = [
        "Smith", "Johnson", "Williams", "Jones", "Brown",
        "Davis", "Miller", "Wilson", "Moore", "Taylor",
        "Anderson", "Thomas", "Jackson", "White", "Harris"
    ]

    search = SimilaritySearch(names_dict)

    # Search for similar names
    queries = ["Smythe", "Jonson", "Wiliams"]

    for query in queries:
        print(f"\nQuery: '{query}'")

        soundex_matches = search.find_similar_soundex(query)
        print(f"  Soundex matches: {soundex_matches}")

        metaphone_matches = search.find_similar_metaphone(query)
        print(f"  Metaphone matches: {metaphone_matches}")

    print("\n" + "=" * 70)
