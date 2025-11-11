"""
Fuzzy String Matching Algorithms

Approximate string matching for handling typos, variations, and inexact matches.

ALGORITHMS IMPLEMENTED:
1. Levenshtein Distance (Edit Distance)
2. Hamming Distance
3. Jaro-Winkler Distance
4. Trigram Similarity
5. Fuzzy Search in Sorted Arrays

WHEN TO USE FUZZY MATCHING:
- Search with typo tolerance
- Autocomplete and suggestions
- Duplicate detection
- Name matching
- Spell checking
- DNA/protein sequence alignment

PERFORMANCE CHARACTERISTICS:
- Levenshtein: O(m*n) time, O(min(m,n)) space optimized
- Hamming: O(n) time, O(1) space
- Jaro-Winkler: O(m+n) time, O(1) space
- Trigram: O(m+n) time, O(m+n) space
"""

from typing import List, Tuple, Set
import re
from collections import defaultdict


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate Levenshtein (edit) distance between two strings.
    Counts minimum insertions, deletions, and substitutions.

    Time Complexity: O(m*n)
    Space Complexity: O(min(m,n)) with optimization

    Args:
        s1: First string
        s2: Second string

    Returns:
        Minimum number of edits to transform s1 into s2
    """
    m, n = len(s1), len(s2)

    # Optimize space by using shorter string for columns
    if m < n:
        s1, s2 = s2, s1
        m, n = n, m

    # Use only two rows instead of full matrix
    prev_row = list(range(n + 1))
    curr_row = [0] * (n + 1)

    for i in range(1, m + 1):
        curr_row[0] = i

        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr_row[j] = prev_row[j - 1]  # No operation needed
            else:
                # Min of: insert, delete, substitute
                curr_row[j] = 1 + min(
                    prev_row[j],      # Delete
                    curr_row[j - 1],  # Insert
                    prev_row[j - 1]   # Substitute
                )

        prev_row, curr_row = curr_row, prev_row

    return prev_row[n]


def hamming_distance(s1: str, s2: str) -> int:
    """
    Calculate Hamming distance - counts character mismatches.
    Only works for strings of equal length.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Args:
        s1: First string
        s2: Second string

    Returns:
        Number of positions with different characters
        Returns -1 if strings have different lengths
    """
    if len(s1) != len(s2):
        return -1

    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def jaro_winkler_distance(s1: str, s2: str, scaling_factor: float = 0.1) -> float:
    """
    Calculate Jaro-Winkler similarity (optimized for short strings).
    Returns value between 0 (no similarity) and 1 (identical).

    Time Complexity: O(m+n)
    Space Complexity: O(1)

    Best for: Names, short strings, prefix-heavy matching

    Args:
        s1: First string
        s2: Second string
        scaling_factor: Bonus for matching prefixes (default 0.1)

    Returns:
        Similarity score between 0 and 1
    """
    if s1 == s2:
        return 1.0

    len1, len2 = len(s1), len(s2)

    # Maximum allowed distance for matches
    match_distance = max(len1, len2) // 2 - 1
    match_distance = max(1, match_distance)

    s1_matches = [False] * len1
    s2_matches = [False] * len2

    matches = 0
    transpositions = 0

    # Find matches
    for i in range(len1):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, len2)

        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = s2_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    # Count transpositions
    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    # Calculate Jaro distance
    jaro = (matches / len1 + matches / len2 + (matches - transpositions / 2) / matches) / 3

    # Calculate common prefix length (up to 4 characters)
    prefix = 0
    for i in range(min(len1, len2, 4)):
        if s1[i] == s2[i]:
            prefix += 1
        else:
            break

    # Calculate Jaro-Winkler distance
    return jaro + prefix * scaling_factor * (1 - jaro)


def trigram_similarity(s1: str, s2: str) -> float:
    """
    Calculate similarity based on trigrams (3-character sequences).
    Good for longer strings and typo detection.

    Time Complexity: O(m+n)
    Space Complexity: O(m+n)

    Args:
        s1: First string
        s2: Second string

    Returns:
        Similarity score between 0 and 1
    """
    def get_trigrams(s: str) -> Set[str]:
        """Extract all trigrams from string"""
        s = f"  {s.lower()} "  # Pad for edge trigrams
        return set(s[i:i+3] for i in range(len(s) - 2))

    if not s1 or not s2:
        return 0.0

    trigrams1 = get_trigrams(s1)
    trigrams2 = get_trigrams(s2)

    if not trigrams1 and not trigrams2:
        return 1.0

    intersection = len(trigrams1 & trigrams2)
    union = len(trigrams1 | trigrams2)

    return intersection / union if union > 0 else 0.0


def fuzzy_search_in_array(arr: List[str], target: str, max_distance: int = 2) -> List[Tuple[int, str, int]]:
    """
    Fuzzy search in a sorted array of strings.
    Returns all strings within max_distance edits of target.

    Time Complexity: O(n * m * k) where k is average string length
    Space Complexity: O(n)

    Args:
        arr: Sorted array of strings
        target: Target string to search for
        max_distance: Maximum Levenshtein distance to consider a match

    Returns:
        List of (index, string, distance) tuples for all matches
    """
    results = []

    for i, s in enumerate(arr):
        # Early termination if strings are very different in length
        if abs(len(s) - len(target)) > max_distance:
            continue

        distance = levenshtein_distance(target, s)
        if distance <= max_distance:
            results.append((i, s, distance))

    # Sort by distance (closest matches first)
    results.sort(key=lambda x: x[2])

    return results


def fuzzy_search_autocomplete(dictionary: List[str], prefix: str, max_results: int = 10) -> List[Tuple[str, float]]:
    """
    Autocomplete with fuzzy matching.
    Returns suggestions even with typos in the prefix.

    Time Complexity: O(n * m)
    Space Complexity: O(n)

    Args:
        dictionary: List of possible words
        prefix: User's input (possibly with typos)
        max_results: Maximum number of suggestions to return

    Returns:
        List of (word, similarity_score) tuples
    """
    suggestions = []

    for word in dictionary:
        # Check if word starts with prefix (exact match bonus)
        if word.lower().startswith(prefix.lower()):
            suggestions.append((word, 1.0))
            continue

        # Check prefix similarity using Jaro-Winkler
        word_prefix = word[:len(prefix)]
        similarity = jaro_winkler_distance(prefix.lower(), word_prefix.lower())

        # Also consider full word similarity for very short prefixes
        if len(prefix) <= 3:
            full_similarity = jaro_winkler_distance(prefix.lower(), word.lower())
            similarity = max(similarity, full_similarity)

        if similarity > 0.7:  # Threshold for suggestions
            suggestions.append((word, similarity))

    # Sort by similarity (descending) and return top results
    suggestions.sort(key=lambda x: x[1], reverse=True)
    return suggestions[:max_results]


def phonetic_similarity(s1: str, s2: str) -> bool:
    """
    Simple phonetic similarity check using Soundex-like algorithm.
    Useful for name matching.

    Args:
        s1: First string
        s2: Second string

    Returns:
        True if strings sound similar
    """
    def soundex_code(s: str) -> str:
        """Generate simplified Soundex code"""
        if not s:
            return ""

        s = s.upper()
        # Keep first letter
        code = s[0]

        # Mapping of similar-sounding letters
        mapping = {
            'BFPV': '1', 'CGJKQSXZ': '2', 'DT': '3',
            'L': '4', 'MN': '5', 'R': '6'
        }

        for char in s[1:]:
            for group, digit in mapping.items():
                if char in group:
                    if code[-1] != digit:  # Avoid duplicates
                        code += digit
                    break

        return (code + '000')[:4]  # Pad to 4 characters

    return soundex_code(s1) == soundex_code(s2)


# Performance testing and demonstration
if __name__ == "__main__":
    print("=== Fuzzy String Matching Demonstrations ===\n")

    # 1. Levenshtein Distance
    print("1. Levenshtein Distance (Edit Distance)")
    pairs = [
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("algorithm", "algorythm"),
        ("python", "pithon")
    ]

    for s1, s2 in pairs:
        dist = levenshtein_distance(s1, s2)
        print(f"  '{s1}' -> '{s2}': {dist} edits")
    print()

    # 2. Jaro-Winkler Distance
    print("2. Jaro-Winkler Distance (Good for names)")
    name_pairs = [
        ("Martha", "Marhta"),
        ("Dwayne", "Duane"),
        ("DIXON", "DICKSON"),
        ("John", "Jon")
    ]

    for s1, s2 in name_pairs:
        similarity = jaro_winkler_distance(s1, s2)
        print(f"  '{s1}' vs '{s2}': {similarity:.3f} similarity")
    print()

    # 3. Trigram Similarity
    print("3. Trigram Similarity (Good for longer strings)")
    text_pairs = [
        ("algorithm", "algorythm"),
        ("information retrieval", "information retreival"),
        ("fuzzy matching", "fuzzzy matchng")
    ]

    for s1, s2 in text_pairs:
        similarity = trigram_similarity(s1, s2)
        print(f"  '{s1}' vs '{s2}': {similarity:.3f} similarity")
    print()

    # 4. Fuzzy Search in Array
    print("4. Fuzzy Search in Sorted Array")
    dictionary = sorted([
        "algorithm", "python", "search", "fuzzy", "matching",
        "binary", "linear", "interpolation", "fibonacci",
        "levenshtein", "jaro", "winkler", "trigram"
    ])

    search_terms = ["algoritm", "pyton", "fuzzi"]

    for term in search_terms:
        results = fuzzy_search_in_array(dictionary, term, max_distance=2)
        print(f"\n  Searching for '{term}':")
        for idx, word, dist in results[:3]:
            print(f"    Found '{word}' at index {idx}, distance {dist}")

    print()

    # 5. Autocomplete with Fuzzy Matching
    print("5. Autocomplete with Fuzzy Matching")
    words = [
        "algorithm", "align", "alien", "allegation", "allocate",
        "alternate", "aluminum", "always", "amazing", "ambiguous"
    ]

    prefixes = ["alg", "alein", "alo"]

    for prefix in prefixes:
        suggestions = fuzzy_search_autocomplete(words, prefix, max_results=3)
        print(f"\n  Prefix: '{prefix}'")
        for word, score in suggestions:
            print(f"    {word} (score: {score:.3f})")

    print()

    # 6. Phonetic Similarity
    print("6. Phonetic Similarity (Soundex-like)")
    phonetic_pairs = [
        ("Smith", "Smythe"),
        ("Johnson", "Jonson"),
        ("Catherine", "Katherine"),
        ("Robert", "Rupert")
    ]

    for s1, s2 in phonetic_pairs:
        similar = phonetic_similarity(s1, s2)
        print(f"  '{s1}' vs '{s2}': {'Similar' if similar else 'Different'}")

    print("\n=== Use Case Recommendations ===")
    print("• Levenshtein: General typo correction, spell checking")
    print("• Jaro-Winkler: Name matching, short strings with prefix importance")
    print("• Trigram: Longer texts, OCR errors, DNA sequences")
    print("• Hamming: Fixed-length codes, error detection")
    print("• Phonetic: Name search, pronunciation-based matching")
    print("\n• Choose based on:")
    print("  - String length (short: Jaro-Winkler, long: trigram)")
    print("  - Error type (typos: Levenshtein, phonetic: Soundex)")
    print("  - Performance needs (Hamming fastest, Levenshtein most accurate)")
