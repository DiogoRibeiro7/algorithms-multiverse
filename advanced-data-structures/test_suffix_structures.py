"""
Test suite for Suffix Tree and Suffix Array implementations.

Tests:
- Construction and basic operations
- Pattern matching
- Longest repeated substring
- Longest common substring
- Edge cases
- Performance characteristics

Author: Algorithms Multiverse
Date: January 2026
"""

import random
import string
import time
from typing import List
from suffix_structures import SuffixTree, SuffixArray, SuffixAutomaton


class TestSuffixStructures:
    """Test suite for suffix structures."""

    def test_suffix_tree_basic(self):
        """Test basic suffix tree operations."""
        print("Testing Suffix Tree - Basic Operations")
        print("-" * 40)

        text = "banana"
        st = SuffixTree(text)

        # Test pattern search
        test_cases = [
            ("ana", [1, 3]),  # "banana" has "ana" at positions 1 and 3
            ("ban", [0]),      # "ban" at position 0
            ("nan", [2]),      # "nan" at position 2
            ("a", [1, 3, 5]),  # "a" appears three times
            ("na", [2, 4]),    # "na" appears twice
            ("xyz", []),       # Not found
        ]

        passed = 0
        for pattern, expected in test_cases:
            result = sorted(st.search(pattern))
            if result == expected:
                passed += 1
                print(f"  Pattern '{pattern}': {result} [PASS]")
            else:
                print(f"  Pattern '{pattern}': Expected {expected}, got {result} [FAIL]")

        print(f"\nPassed {passed}/{len(test_cases)} tests")
        return passed == len(test_cases)

    def test_suffix_array_basic(self):
        """Test basic suffix array operations."""
        print("\nTesting Suffix Array - Basic Operations")
        print("-" * 40)

        text = "banana"
        sa = SuffixArray(text)

        # Check suffix array correctness
        print(f"  Text: '{text}'")
        print(f"  Suffix array: {sa.suffix_array}")

        # Verify suffixes are sorted
        suffixes = [text[i:] for i in sa.suffix_array]
        is_sorted = suffixes == sorted(suffixes)
        print(f"  Suffixes sorted correctly: {is_sorted}")

        # Test pattern search
        pattern = "ana"
        positions = sorted(sa.search(pattern))
        expected = [1, 3]
        search_correct = positions == expected
        print(f"  Search for '{pattern}': {positions} (correct: {search_correct})")

        # Test LCP array
        print(f"  LCP array: {sa.lcp_array}")

        return is_sorted and search_correct

    def test_longest_repeated_substring(self):
        """Test finding longest repeated substring."""
        print("\nTesting Longest Repeated Substring")
        print("-" * 40)

        test_cases = [
            ("banana", "ana"),
            ("abcdefg", ""),  # No repeated substring
            ("aaaaa", "aaaa"),
            ("abcabc", "abc"),
            ("mississippi", "issi"),
        ]

        passed = 0
        for text, expected in test_cases:
            # Test with Suffix Tree
            st = SuffixTree(text)
            lrs_st = st.longest_repeated_substring()

            # Test with Suffix Array
            sa = SuffixArray(text)
            lrs_sa = sa.longest_repeated_substring()

            if lrs_st == expected and lrs_sa == expected:
                passed += 1
                print(f"  '{text}' -> '{lrs_st}' [PASS]")
            else:
                print(f"  '{text}' -> ST: '{lrs_st}', SA: '{lrs_sa}' (expected: '{expected}') [FAIL]")

        print(f"\nPassed {passed}/{len(test_cases)} tests")
        return passed == len(test_cases)

    def test_longest_common_substring(self):
        """Test finding longest common substring between two strings."""
        print("\nTesting Longest Common Substring")
        print("-" * 40)

        test_cases = [
            ("GeeksforGeeks", "GeeksQuiz", "Geeks"),
            ("abcdxyz", "xyzabcd", "abcd"),
            ("zxabcdezy", "yzabcdezx", "abcdez"),
            ("ABC", "DEF", ""),  # No common substring
            ("ABABC", "BABCA", "BABC"),
        ]

        passed = 0
        for text1, text2, expected in test_cases:
            sa = SuffixArray(text1)
            lcs = sa.longest_common_substring(text2)

            # LCS might not be unique, check length
            if len(lcs) == len(expected):
                passed += 1
                print(f"  '{text1}' vs '{text2}' -> '{lcs}' [PASS]")
            else:
                print(f"  '{text1}' vs '{text2}' -> '{lcs}' (expected length: {len(expected)}) [FAIL]")

        print(f"\nPassed {passed}/{len(test_cases)} tests")
        return passed == len(test_cases)

    def test_count_distinct_substrings(self):
        """Test counting distinct substrings."""
        print("\nTesting Count Distinct Substrings")
        print("-" * 40)

        test_cases = [
            ("abc", 6),  # "", "a", "b", "c", "ab", "bc", "abc" (excluding empty)
            ("aaa", 3),  # "a", "aa", "aaa"
            ("ababa", 11),  # All distinct substrings
        ]

        passed = 0
        for text, expected in test_cases:
            sa = SuffixArray(text)
            count = sa.count_distinct_substrings()

            if count == expected:
                passed += 1
                print(f"  '{text}' has {count} distinct substrings [PASS]")
            else:
                print(f"  '{text}' has {count} distinct substrings (expected: {expected}) [FAIL]")

        print(f"\nPassed {passed}/{len(test_cases)} tests")
        return passed == len(test_cases)

    def test_suffix_automaton(self):
        """Test suffix automaton operations."""
        print("\nTesting Suffix Automaton")
        print("-" * 40)

        text = "banana"
        sa = SuffixAutomaton(text)

        test_cases = [
            ("ana", True),
            ("ban", True),
            ("nan", True),
            ("xyz", False),
            ("banana", True),
            ("ananan", False),
        ]

        passed = 0
        for pattern, expected in test_cases:
            result = sa.contains(pattern)
            if result == expected:
                passed += 1
                print(f"  Contains '{pattern}': {result} [PASS]")
            else:
                print(f"  Contains '{pattern}': {result} (expected: {expected}) [FAIL]")

        print(f"\nPassed {passed}/{len(test_cases)} tests")
        return passed == len(test_cases)

    def test_edge_cases(self):
        """Test edge cases."""
        print("\nTesting Edge Cases")
        print("-" * 40)

        # Empty pattern search
        st = SuffixTree("test")
        empty_search = st.search("")
        print(f"  Empty pattern search: {empty_search == []}")

        # Single character text
        st_single = SuffixTree("a")
        single_search = st_single.search("a")
        print(f"  Single char text: {single_search == [0]}")

        # Pattern longer than text
        long_pattern = st.search("testing")
        print(f"  Pattern longer than text: {long_pattern == []}")

        # All same characters
        st_same = SuffixTree("aaaa")
        same_search = sorted(st_same.search("aa"))
        print(f"  All same chars 'aa' in 'aaaa': {same_search == [0, 1, 2]}")

        # Special characters
        st_special = SuffixTree("a$b#c")
        special_search = st_special.search("#")
        print(f"  Special characters: found '#'")

        return True

    def test_dna_sequence_analysis(self):
        """Test with DNA sequences (real-world application)."""
        print("\nTesting DNA Sequence Analysis")
        print("-" * 40)

        # Simulated DNA sequence with repeating motifs
        dna = "ATCGATCGATCGTAGCTAGCTAGC"
        st = SuffixTree(dna)

        # Find motif occurrences
        motif = "ATCG"
        occurrences = st.search(motif)
        print(f"  DNA sequence: {dna}")
        print(f"  Motif '{motif}' found {len(occurrences)} times at: {occurrences}")

        # Find tandem repeats
        lrs = st.longest_repeated_substring()
        print(f"  Longest tandem repeat: '{lrs}' (length: {len(lrs)})")

        # Count unique k-mers (e.g., 3-mers)
        k = 3
        kmers = set()
        for i in range(len(dna) - k + 1):
            kmers.add(dna[i:i+k])
        print(f"  Unique {k}-mers: {len(kmers)}")

        return len(occurrences) > 0

    def test_text_processing(self):
        """Test with text processing scenarios."""
        print("\nTesting Text Processing")
        print("-" * 40)

        # Plagiarism detection simulation
        doc1 = "The quick brown fox jumps over the lazy dog"
        doc2 = "A quick brown fox jumped over a lazy dog"

        sa1 = SuffixArray(doc1)
        lcs = sa1.longest_common_substring(doc2)
        print(f"  Doc1: '{doc1}'")
        print(f"  Doc2: '{doc2}'")
        print(f"  Longest common phrase: '{lcs}'")

        # Find all word occurrences
        st = SuffixTree(doc1)
        word = "fox"
        positions = st.search(word)
        print(f"  Word '{word}' appears at positions: {positions}")

        return len(lcs) > 0

    def test_performance_comparison(self):
        """Compare performance of different implementations."""
        print("\nPerformance Comparison")
        print("-" * 40)

        sizes = [100, 500, 1000]

        for size in sizes:
            # Generate random text
            text = ''.join(random.choices(string.ascii_lowercase, k=size))
            pattern = text[size//2:size//2 + 5]

            print(f"\n  Text size: {size}")

            # Suffix Tree
            start = time.time()
            st = SuffixTree(text)
            st_build = time.time() - start

            start = time.time()
            st_result = st.search(pattern)
            st_search = time.time() - start

            # Suffix Array
            start = time.time()
            sa = SuffixArray(text)
            sa_build = time.time() - start

            start = time.time()
            sa_result = sa.search(pattern)
            sa_search = time.time() - start

            # Python built-in
            start = time.time()
            py_result = []
            idx = text.find(pattern)
            while idx != -1:
                py_result.append(idx)
                idx = text.find(pattern, idx + 1)
            py_search = time.time() - start

            print(f"    Build - ST: {st_build:.5f}s, SA: {sa_build:.5f}s")
            print(f"    Search - ST: {st_search:.5f}s, SA: {sa_search:.5f}s, Python: {py_search:.5f}s")

            # Verify all methods find same occurrences
            results_match = sorted(st_result) == sorted(sa_result) == sorted(py_result)
            print(f"    Results match: {results_match}")

    def test_large_alphabet(self):
        """Test with extended characters."""
        print("\nTesting Extended Characters")
        print("-" * 40)

        # Mixed case text
        text = "HelloWorldHello"
        st = SuffixTree(text)

        pattern = "Hello"
        positions = st.search(pattern)
        print(f"  Text: '{text}'")
        print(f"  Pattern '{pattern}' at positions: {positions}")

        # Numbers and letters
        mixed_text = "abc123abc456abc"
        st_mixed = SuffixTree(mixed_text)
        mixed_pattern = "abc"
        mixed_pos = st_mixed.search(mixed_pattern)
        print(f"  Pattern '{mixed_pattern}' found {len(mixed_pos)} times in mixed text")

        return len(positions) == 2

    def run_all_tests(self):
        """Run all tests."""
        print("=" * 50)
        print("SUFFIX STRUCTURES TEST SUITE")
        print("=" * 50)

        tests = [
            self.test_suffix_tree_basic,
            self.test_suffix_array_basic,
            self.test_longest_repeated_substring,
            self.test_longest_common_substring,
            self.test_count_distinct_substrings,
            self.test_suffix_automaton,
            self.test_edge_cases,
            self.test_dna_sequence_analysis,
            self.test_text_processing,
            self.test_large_alphabet,
            self.test_performance_comparison,
        ]

        passed = 0
        failed = 0

        for test in tests:
            try:
                result = test()
                if result is not False:
                    print(f"\n[PASS] {test.__name__}")
                    passed += 1
                else:
                    print(f"\n[FAIL] {test.__name__}")
                    failed += 1
            except Exception as e:
                print(f"\n[ERROR] {test.__name__}: {e}")
                failed += 1

        print("\n" + "=" * 50)
        print(f"TEST SUMMARY: {passed} passed, {failed} failed")
        print("=" * 50)


def application_examples():
    """Demonstrate real-world applications."""
    print("\nREAL-WORLD APPLICATIONS")
    print("=" * 50)

    # 1. Bioinformatics - Finding genes
    print("\n1. Gene Finding in DNA:")
    dna_sequence = "ATGCGATCGTAGCTAGCTGATCGATGCTAGC"
    start_codon = "ATG"  # Start codon in genetics

    st = SuffixTree(dna_sequence)
    starts = st.search(start_codon)
    print(f"  DNA: {dna_sequence}")
    print(f"  Start codon 'ATG' found at positions: {starts}")

    # 2. Data Compression - Finding repeated patterns
    print("\n2. Data Compression (LZ77-style):")
    text = "abcabcabcdefdefghi"
    sa = SuffixArray(text)
    lrs = sa.longest_repeated_substring()
    print(f"  Text: {text}")
    print(f"  Longest repeated: '{lrs}' (can be compressed)")

    # 3. Search Engine - Fast substring search
    print("\n3. Search Engine Indexing:")
    documents = [
        "The quick brown fox jumps",
        "Brown foxes are quick",
        "Jumping foxes are brown"
    ]

    # Build combined suffix structure
    combined = " | ".join(documents)
    st = SuffixTree(combined)

    query = "fox"
    positions = st.search(query)
    print(f"  Documents: {documents}")
    print(f"  Query '{query}' found at {len(positions)} positions")

    # Map positions back to documents
    doc_hits = []
    for pos in positions:
        doc_idx = combined[:pos].count(" | ")
        if doc_idx not in doc_hits:
            doc_hits.append(doc_idx)

    print(f"  Found in documents: {doc_hits}")

    # 4. Plagiarism Detection
    print("\n4. Plagiarism Detection:")
    original = "To be or not to be that is the question"
    suspected = "That is the question to be or not"

    sa_orig = SuffixArray(original.lower())
    lcs = sa_orig.longest_common_substring(suspected.lower())
    similarity = len(lcs) / min(len(original), len(suspected))

    print(f"  Original: '{original}'")
    print(f"  Suspected: '{suspected}'")
    print(f"  Longest common: '{lcs}'")
    print(f"  Similarity: {similarity:.1%}")

    # 5. Auto-complete / Type-ahead
    print("\n5. Auto-complete System:")
    dictionary = ["apple", "application", "apply", "appreciate", "banana", "band"]
    combined_dict = "$".join(dictionary) + "$"
    st_dict = SuffixTree(combined_dict)

    prefix = "app"
    positions = st_dict.search(prefix)
    suggestions = set()

    for pos in positions:
        # Find word boundaries
        start = combined_dict.rfind("$", 0, pos) + 1
        end = combined_dict.find("$", pos)
        if start == 0 or combined_dict[start-1] == "$":
            word = combined_dict[start:end]
            suggestions.add(word)

    print(f"  Dictionary: {dictionary}")
    print(f"  Prefix '{prefix}' suggestions: {sorted(suggestions)}")


if __name__ == "__main__":
    # Run test suite
    tester = TestSuffixStructures()
    tester.run_all_tests()

    # Show real-world applications
    print("\n")
    application_examples()