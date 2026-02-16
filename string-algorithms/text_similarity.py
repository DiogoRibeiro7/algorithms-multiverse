"""
Text Similarity Metrics
=======================

Comprehensive collection of text similarity and distance metrics for comparing strings.

Metrics included:
1. **Set-based metrics:**
   - Jaccard similarity
   - Sørensen-Dice coefficient
   - Overlap coefficient

2. **Sequence-based metrics:**
   - Levenshtein distance & similarity
   - Hamming distance
   - Jaro similarity
   - Jaro-Winkler similarity

3. **Vector-based metrics:**
   - Cosine similarity
   - Euclidean distance

4. **Token-based metrics:**
   - Token Jaccard
   - Token cosine similarity

5. **N-gram based metrics:**
   - N-gram Jaccard
   - N-gram cosine

Applications:
- Fuzzy string matching
- Duplicate detection
- Spell checking
- Information retrieval
- Recommendation systems
"""

from typing import Set, List, Counter as CounterType
from collections import Counter
import math


# ============================================================================
# SET-BASED SIMILARITY METRICS
# ============================================================================

def jaccard_similarity(s1: str, s2: str) -> float:
    """
    Jaccard similarity coefficient for character sets.

    Formula: |A ∩ B| / |A ∪ B|

    Time: O(n + m)

    Returns:
        Similarity score in [0, 1]
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    set1 = set(s1)
    set2 = set(s2)

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    return intersection / union if union > 0 else 0.0


def sorensen_dice_coefficient(s1: str, s2: str) -> float:
    """
    Sørensen-Dice coefficient (also known as Dice coefficient).

    Formula: 2 * |A ∩ B| / (|A| + |B|)

    Time: O(n + m)

    Returns:
        Similarity score in [0, 1]
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    set1 = set(s1)
    set2 = set(s2)

    intersection = len(set1 & set2)

    return 2.0 * intersection / (len(set1) + len(set2))


def overlap_coefficient(s1: str, s2: str) -> float:
    """
    Overlap coefficient (Szymkiewicz-Simpson coefficient).

    Formula: |A ∩ B| / min(|A|, |B|)

    Time: O(n + m)

    Returns:
        Similarity score in [0, 1]
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    set1 = set(s1)
    set2 = set(s2)

    intersection = len(set1 & set2)
    min_size = min(len(set1), len(set2))

    return intersection / min_size if min_size > 0 else 0.0


# ============================================================================
# SEQUENCE-BASED METRICS
# ============================================================================

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Levenshtein edit distance.

    Minimum number of single-character edits (insertions, deletions, substitutions).

    Time: O(n * m)
    Space: O(min(n, m))

    Returns:
        Edit distance
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    if not s2:
        return len(s1)

    # Use two rows for space optimization
    previous_row = list(range(len(s2) + 1))
    current_row = [0] * (len(s2) + 1)

    for i, c1 in enumerate(s1):
        current_row[0] = i + 1

        for j, c2 in enumerate(s2):
            # Cost of substitution
            cost = 0 if c1 == c2 else 1

            current_row[j + 1] = min(
                previous_row[j + 1] + 1,      # Deletion
                current_row[j] + 1,           # Insertion
                previous_row[j] + cost        # Substitution
            )

        previous_row, current_row = current_row, previous_row

    return previous_row[-1]


def levenshtein_similarity(s1: str, s2: str) -> float:
    """
    Normalized Levenshtein similarity.

    Formula: 1 - (distance / max_length)

    Returns:
        Similarity score in [0, 1]
    """
    if not s1 and not s2:
        return 1.0

    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))

    return 1.0 - (distance / max_len) if max_len > 0 else 1.0


def hamming_distance(s1: str, s2: str) -> int:
    """
    Hamming distance (for strings of equal length).

    Number of positions at which corresponding characters differ.

    Time: O(n)

    Returns:
        Hamming distance, or -1 if lengths differ
    """
    if len(s1) != len(s2):
        return -1

    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def jaro_similarity(s1: str, s2: str) -> float:
    """
    Jaro similarity measure.

    Accounts for character matches and transpositions.

    Time: O(n * m)

    Returns:
        Similarity score in [0, 1]
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    len1, len2 = len(s1), len(s2)

    # Maximum allowed distance for matching
    max_dist = max(len1, len2) // 2 - 1
    if max_dist < 0:
        max_dist = 0

    # Track which characters matched
    s1_matches = [False] * len1
    s2_matches = [False] * len2

    matches = 0
    transpositions = 0

    # Find matches
    for i in range(len1):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len2)

        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue

            s1_matches[i] = True
            s2_matches[j] = True
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

    return (matches / len1 +
            matches / len2 +
            (matches - transpositions / 2) / matches) / 3.0


def jaro_winkler_similarity(s1: str, s2: str, prefix_scale: float = 0.1) -> float:
    """
    Jaro-Winkler similarity (variant of Jaro with prefix bonus).

    Time: O(n * m)

    Args:
        s1, s2: Strings to compare
        prefix_scale: Scaling factor for prefix bonus (default 0.1)

    Returns:
        Similarity score in [0, 1]
    """
    jaro_sim = jaro_similarity(s1, s2)

    # Find common prefix length (up to 4 characters)
    prefix_len = 0
    for i in range(min(len(s1), len(s2), 4)):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break

    return jaro_sim + (prefix_len * prefix_scale * (1 - jaro_sim))


# ============================================================================
# VECTOR-BASED METRICS
# ============================================================================

def cosine_similarity(s1: str, s2: str) -> float:
    """
    Cosine similarity based on character frequencies.

    Time: O(n + m)

    Returns:
        Similarity score in [0, 1]
    """
    if not s1 or not s2:
        return 0.0

    # Count character frequencies
    vec1 = Counter(s1)
    vec2 = Counter(s2)

    # Get all unique characters
    all_chars = set(vec1.keys()) | set(vec2.keys())

    # Compute dot product
    dot_product = sum(vec1.get(char, 0) * vec2.get(char, 0)
                     for char in all_chars)

    # Compute magnitudes
    magnitude1 = math.sqrt(sum(count ** 2 for count in vec1.values()))
    magnitude2 = math.sqrt(sum(count ** 2 for count in vec2.values()))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def euclidean_distance(s1: str, s2: str) -> float:
    """
    Euclidean distance based on character frequencies.

    Time: O(n + m)

    Returns:
        Distance value (lower is more similar)
    """
    vec1 = Counter(s1)
    vec2 = Counter(s2)

    all_chars = set(vec1.keys()) | set(vec2.keys())

    distance_sq = sum((vec1.get(char, 0) - vec2.get(char, 0)) ** 2
                      for char in all_chars)

    return math.sqrt(distance_sq)


# ============================================================================
# TOKEN-BASED METRICS
# ============================================================================

def tokenize(text: str) -> List[str]:
    """Simple whitespace tokenization."""
    return text.lower().split()


def token_jaccard(s1: str, s2: str) -> float:
    """
    Jaccard similarity on word tokens.

    Time: O(n + m)
    """
    tokens1 = set(tokenize(s1))
    tokens2 = set(tokenize(s2))

    if not tokens1 and not tokens2:
        return 1.0

    intersection = len(tokens1 & tokens2)
    union = len(tokens1 | tokens2)

    return intersection / union if union > 0 else 0.0


def token_cosine_similarity(s1: str, s2: str) -> float:
    """
    Cosine similarity on word token frequencies.

    Time: O(n + m)
    """
    tokens1 = tokenize(s1)
    tokens2 = tokenize(s2)

    if not tokens1 or not tokens2:
        return 0.0

    vec1 = Counter(tokens1)
    vec2 = Counter(tokens2)

    all_tokens = set(vec1.keys()) | set(vec2.keys())

    dot_product = sum(vec1.get(token, 0) * vec2.get(token, 0)
                     for token in all_tokens)

    magnitude1 = math.sqrt(sum(count ** 2 for count in vec1.values()))
    magnitude2 = math.sqrt(sum(count ** 2 for count in vec2.values()))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


# ============================================================================
# N-GRAM BASED METRICS
# ============================================================================

def get_ngrams(text: str, n: int) -> Set[str]:
    """
    Extract all n-grams from text.

    Time: O(len(text) * n)
    """
    if len(text) < n:
        return set()

    return set(text[i:i + n] for i in range(len(text) - n + 1))


def ngram_jaccard(s1: str, s2: str, n: int = 2) -> float:
    """
    Jaccard similarity on n-grams.

    Time: O(n + m)

    Args:
        s1, s2: Strings to compare
        n: N-gram size (default 2 for bigrams)
    """
    ngrams1 = get_ngrams(s1, n)
    ngrams2 = get_ngrams(s2, n)

    if not ngrams1 and not ngrams2:
        return 1.0

    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)

    return intersection / union if union > 0 else 0.0


def ngram_cosine_similarity(s1: str, s2: str, n: int = 2) -> float:
    """
    Cosine similarity on n-gram frequencies.

    Time: O(n + m)
    """
    ngrams1 = [s1[i:i + n] for i in range(len(s1) - n + 1)]
    ngrams2 = [s2[i:i + n] for i in range(len(s2) - n + 1)]

    if not ngrams1 or not ngrams2:
        return 0.0

    vec1 = Counter(ngrams1)
    vec2 = Counter(ngrams2)

    all_ngrams = set(vec1.keys()) | set(vec2.keys())

    dot_product = sum(vec1.get(ng, 0) * vec2.get(ng, 0)
                     for ng in all_ngrams)

    magnitude1 = math.sqrt(sum(count ** 2 for count in vec1.values()))
    magnitude2 = math.sqrt(sum(count ** 2 for count in vec2.values()))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


# ============================================================================
# UTILITY FUNCTION: COMPARE ALL METRICS
# ============================================================================

def compare_all_metrics(s1: str, s2: str) -> dict:
    """
    Compute all similarity metrics between two strings.

    Returns:
        Dictionary mapping metric name to similarity score
    """
    return {
        "Jaccard (char)": jaccard_similarity(s1, s2),
        "Sørensen-Dice": sorensen_dice_coefficient(s1, s2),
        "Overlap": overlap_coefficient(s1, s2),
        "Levenshtein": levenshtein_similarity(s1, s2),
        "Jaro": jaro_similarity(s1, s2),
        "Jaro-Winkler": jaro_winkler_similarity(s1, s2),
        "Cosine (char)": cosine_similarity(s1, s2),
        "Token Jaccard": token_jaccard(s1, s2),
        "Token Cosine": token_cosine_similarity(s1, s2),
        "2-gram Jaccard": ngram_jaccard(s1, s2, 2),
        "2-gram Cosine": ngram_cosine_similarity(s1, s2, 2),
    }


# ============================================================================
# EXAMPLES AND TESTING
# ============================================================================

def example_set_based_metrics():
    """Compare classic set-based similarity metrics on sample pairs."""
    print("=" * 70)
    print("EXAMPLE 1: Set-Based Similarity Metrics")
    print("=" * 70)

    pairs = [
        ("kitten", "sitting"),
        ("hello", "hallo"),
        ("algorithm", "logarithm"),
    ]

    for s1, s2 in pairs:
        print(f"\nComparing '{s1}' and '{s2}':")
        print(f"  Jaccard:       {jaccard_similarity(s1, s2):.4f}")
        print(f"  Sørensen-Dice: {sorensen_dice_coefficient(s1, s2):.4f}")
        print(f"  Overlap:       {overlap_coefficient(s1, s2):.4f}")

    print()


def example_sequence_based_metrics():
    """Demonstrate edit-distance and character-alignment metrics."""
    print("=" * 70)
    print("EXAMPLE 2: Sequence-Based Metrics")
    print("=" * 70)

    pairs = [
        ("kitten", "sitting"),
        ("hello", "hallo"),
        ("algorithm", "logarithm"),
    ]

    for s1, s2 in pairs:
        print(f"\nComparing '{s1}' and '{s2}':")
        print(f"  Levenshtein distance:   {levenshtein_distance(s1, s2)}")
        print(f"  Levenshtein similarity: {levenshtein_similarity(s1, s2):.4f}")
        print(f"  Jaro:                   {jaro_similarity(s1, s2):.4f}")
        print(f"  Jaro-Winkler:           {jaro_winkler_similarity(s1, s2):.4f}")

    print()


def example_vector_based_metrics():
    """Highlight cosine/Euclidean scores using vectorized character counts."""
    print("=" * 70)
    print("EXAMPLE 3: Vector-Based Metrics")
    print("=" * 70)

    pairs = [
        ("hello", "hallo"),
        ("information", "reformation"),
        ("abc", "xyz"),
    ]

    for s1, s2 in pairs:
        print(f"\nComparing '{s1}' and '{s2}':")
        print(f"  Cosine similarity:   {cosine_similarity(s1, s2):.4f}")
        print(f"  Euclidean distance:  {euclidean_distance(s1, s2):.4f}")

    print()


def example_token_based_metrics():
    """Compare token-level Jaccard and cosine similarity for sentences."""
    print("=" * 70)
    print("EXAMPLE 4: Token-Based Metrics")
    print("=" * 70)

    pairs = [
        ("the quick brown fox", "the lazy brown dog"),
        ("hello world", "world hello"),
        ("machine learning algorithms", "deep learning algorithms"),
    ]

    for s1, s2 in pairs:
        print(f"\nComparing:")
        print(f"  '{s1}'")
        print(f"  '{s2}'")
        print(f"  Token Jaccard: {token_jaccard(s1, s2):.4f}")
        print(f"  Token Cosine:  {token_cosine_similarity(s1, s2):.4f}")

    print()


def example_ngram_metrics():
    """Evaluate bigram/trigram overlaps via Jaccard and cosine metrics."""
    print("=" * 70)
    print("EXAMPLE 5: N-gram Based Metrics")
    print("=" * 70)

    pairs = [
        ("hello", "hallo"),
        ("algorithm", "logarithm"),
    ]

    for s1, s2 in pairs:
        print(f"\nComparing '{s1}' and '{s2}':")
        print(f"  2-gram Jaccard: {ngram_jaccard(s1, s2, 2):.4f}")
        print(f"  3-gram Jaccard: {ngram_jaccard(s1, s2, 3):.4f}")
        print(f"  2-gram Cosine:  {ngram_cosine_similarity(s1, s2, 2):.4f}")

    print()


def example_comprehensive_comparison():
    """Print every implemented metric for a single string pair."""
    print("=" * 70)
    print("EXAMPLE 6: Comprehensive Comparison")
    print("=" * 70)

    s1 = "the quick brown fox"
    s2 = "the lazy brown dog"

    print(f"String 1: '{s1}'")
    print(f"String 2: '{s2}'\n")

    metrics = compare_all_metrics(s1, s2)

    print("All similarity metrics:")
    for metric_name, score in sorted(metrics.items(), key=lambda x: -x[1]):
        print(f"  {metric_name:20} : {score:.4f}")

    print()


if __name__ == "__main__":
    print("=" * 70)
    print("TEXT SIMILARITY METRICS")
    print("=" * 70)
    print()

    example_set_based_metrics()
    example_sequence_based_metrics()
    example_vector_based_metrics()
    example_token_based_metrics()
    example_ngram_metrics()
    example_comprehensive_comparison()

    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
