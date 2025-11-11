"""
Advanced Text Analysis Tools
============================

Comprehensive text analysis utilities including frequency analysis,
n-gram generation, TF-IDF, and document similarity.

Features:
1. Character and word frequency analysis
2. N-gram generation (unigrams, bigrams, trigrams, etc.)
3. TF-IDF (Term Frequency-Inverse Document Frequency)
4. Document vectorization
5. Collocations and co-occurrence
6. Keyword extraction
7. Text summarization metrics

Applications:
- Information retrieval
- Document classification
- Text mining
- Search engine optimization
- Content analysis
"""

import math
from typing import List, Dict, Tuple, Set
from collections import Counter, defaultdict
import re


# ============================================================================
# FREQUENCY ANALYSIS
# ============================================================================

class FrequencyAnalysis:
    """
    Analyze character and word frequencies in text.
    """

    @staticmethod
    def character_frequency(text: str, normalize: bool = False) -> Dict[str, float]:
        """
        Compute character frequency distribution.

        Time: O(n)

        Args:
            text: Input text
            normalize: Return probabilities instead of counts

        Returns:
            Dictionary mapping characters to frequencies
        """
        freq = Counter(text)

        if normalize:
            total = len(text)
            return {char: count / total for char, count in freq.items()}

        return dict(freq)

    @staticmethod
    def word_frequency(text: str, normalize: bool = False,
                      case_sensitive: bool = False) -> Dict[str, float]:
        """
        Compute word frequency distribution.

        Time: O(n)
        """
        if not case_sensitive:
            text = text.lower()

        words = re.findall(r'\b\w+\b', text)
        freq = Counter(words)

        if normalize:
            total = len(words)
            return {word: count / total for word, count in freq.items()}

        return dict(freq)

    @staticmethod
    def letter_frequency(text: str, normalize: bool = True) -> Dict[str, float]:
        """
        Compute letter frequency (alphabetic characters only).

        Useful for cryptanalysis, language detection, etc.

        Time: O(n)
        """
        letters = [c.lower() for c in text if c.isalpha()]
        freq = Counter(letters)

        if normalize and letters:
            total = len(letters)
            return {letter: count / total for letter, count in freq.items()}

        return dict(freq)

    @staticmethod
    def zipf_analysis(text: str, top_n: int = 50) -> List[Tuple[str, int, float]]:
        """
        Analyze word frequency according to Zipf's law.

        Zipf's law: frequency of word is inversely proportional to its rank.

        Returns:
            List of (word, frequency, expected_frequency) tuples
        """
        words = re.findall(r'\b\w+\b', text.lower())
        freq = Counter(words)

        most_common = freq.most_common(top_n)

        if not most_common:
            return []

        # Zipf's law: f(r) = f(1) / r
        max_freq = most_common[0][1]

        results = []
        for rank, (word, count) in enumerate(most_common, 1):
            expected = max_freq / rank
            results.append((word, count, expected))

        return results


# ============================================================================
# N-GRAM GENERATION AND ANALYSIS
# ============================================================================

class NGramAnalyzer:
    """
    N-gram generation and analysis.
    """

    @staticmethod
    def generate_ngrams(tokens: List[str], n: int) -> List[Tuple[str, ...]]:
        """
        Generate n-grams from token list.

        Time: O(n * k) where k is n-gram size

        Args:
            tokens: List of tokens
            n: N-gram size

        Returns:
            List of n-gram tuples
        """
        if n < 1 or len(tokens) < n:
            return []

        return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

    @staticmethod
    def ngram_frequency(text: str, n: int = 2,
                       char_level: bool = False) -> Dict[Tuple, int]:
        """
        Compute n-gram frequencies.

        Time: O(n)

        Args:
            text: Input text
            n: N-gram size
            char_level: Character-level or word-level

        Returns:
            Dictionary mapping n-grams to frequencies
        """
        if char_level:
            tokens = list(text)
        else:
            tokens = re.findall(r'\b\w+\b', text.lower())

        ngrams = NGramAnalyzer.generate_ngrams(tokens, n)
        return dict(Counter(ngrams))

    @staticmethod
    def most_common_ngrams(text: str, n: int = 2, top_k: int = 10,
                          char_level: bool = False) -> List[Tuple[Tuple, int]]:
        """
        Find most common n-grams.

        Time: O(n log k)
        """
        freq = NGramAnalyzer.ngram_frequency(text, n, char_level)
        return Counter(freq).most_common(top_k)

    @staticmethod
    def conditional_frequency(text: str, n: int = 2) -> Dict[Tuple, Dict[str, float]]:
        """
        Compute conditional probabilities for n-grams.

        P(word_n | word_1, ..., word_{n-1})

        Time: O(n)
        """
        words = re.findall(r'\b\w+\b', text.lower())
        ngrams = NGramAnalyzer.generate_ngrams(words, n)

        # Count context and full n-gram occurrences
        context_counts = Counter()
        ngram_counts = Counter()

        for ngram in ngrams:
            context = ngram[:-1]
            context_counts[context] += 1
            ngram_counts[ngram] += 1

        # Compute conditional probabilities
        conditional = defaultdict(dict)
        for ngram, count in ngram_counts.items():
            context = ngram[:-1]
            word = ngram[-1]
            conditional[context][word] = count / context_counts[context]

        return dict(conditional)


# ============================================================================
# TF-IDF (Term Frequency-Inverse Document Frequency)
# ============================================================================

class TFIDF:
    """
    TF-IDF vectorization for document analysis.
    """

    def __init__(self, documents: List[str]):
        """
        Initialize with document collection.

        Args:
            documents: List of document strings
        """
        self.documents = documents
        self.vocabulary: Set[str] = set()
        self.idf: Dict[str, float] = {}
        self.tf: List[Dict[str, int]] = []

        self._compute()

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        return re.findall(r'\b\w+\b', text.lower())

    def _compute_tf(self) -> None:
        """Compute term frequency for each document."""
        for doc in self.documents:
            words = self._tokenize(doc)
            self.vocabulary.update(words)
            self.tf.append(dict(Counter(words)))

    def _compute_idf(self) -> None:
        """
        Compute inverse document frequency.

        IDF(term) = log(N / df(term))
        where N = total documents, df = document frequency
        """
        n_docs = len(self.documents)

        # Count document frequency for each term
        df = defaultdict(int)
        for tf_dict in self.tf:
            for term in tf_dict.keys():
                df[term] += 1

        # Compute IDF
        for term in self.vocabulary:
            self.idf[term] = math.log(n_docs / df[term])

    def _compute(self) -> None:
        """Compute TF and IDF."""
        self._compute_tf()
        self._compute_idf()

    def vectorize(self, doc_idx: int) -> Dict[str, float]:
        """
        Get TF-IDF vector for document.

        Args:
            doc_idx: Document index

        Returns:
            Dictionary mapping terms to TF-IDF scores
        """
        if doc_idx < 0 or doc_idx >= len(self.documents):
            return {}

        tf_dict = self.tf[doc_idx]
        tfidf = {}

        for term, tf_value in tf_dict.items():
            tfidf[term] = tf_value * self.idf[term]

        return tfidf

    def top_terms(self, doc_idx: int, k: int = 10) -> List[Tuple[str, float]]:
        """
        Get top k terms by TF-IDF score for a document.

        Args:
            doc_idx: Document index
            k: Number of top terms

        Returns:
            List of (term, score) tuples
        """
        tfidf = self.vectorize(doc_idx)
        return sorted(tfidf.items(), key=lambda x: -x[1])[:k]


# ============================================================================
# COLLOCATION AND CO-OCCURRENCE
# ============================================================================

class CollocationFinder:
    """
    Find collocations (words that frequently appear together).
    """

    @staticmethod
    def find_bigram_collocations(text: str, min_freq: int = 2,
                                 top_k: int = 10) -> List[Tuple[Tuple[str, str], float]]:
        """
        Find bigram collocations using pointwise mutual information (PMI).

        PMI(w1, w2) = log(P(w1, w2) / (P(w1) * P(w2)))

        Time: O(n)
        """
        words = re.findall(r'\b\w+\b', text.lower())
        n = len(words)

        if n < 2:
            return []

        # Count unigrams and bigrams
        unigram_counts = Counter(words)
        bigrams = [(words[i], words[i+1]) for i in range(n - 1)]
        bigram_counts = Counter(bigrams)

        # Calculate PMI for each bigram
        pmi_scores = {}

        for bigram, count in bigram_counts.items():
            if count < min_freq:
                continue

            w1, w2 = bigram
            p_bigram = count / (n - 1)
            p_w1 = unigram_counts[w1] / n
            p_w2 = unigram_counts[w2] / n

            pmi = math.log(p_bigram / (p_w1 * p_w2))
            pmi_scores[bigram] = pmi

        # Return top k collocations
        return sorted(pmi_scores.items(), key=lambda x: -x[1])[:top_k]

    @staticmethod
    def cooccurrence_matrix(text: str, window_size: int = 5) -> Dict[Tuple[str, str], int]:
        """
        Build word co-occurrence matrix.

        Counts how often words appear within a window.

        Time: O(n * w) where w is window size
        """
        words = re.findall(r'\b\w+\b', text.lower())
        cooccur = defaultdict(int)

        for i, word1 in enumerate(words):
            # Look at words within window
            start = max(0, i - window_size)
            end = min(len(words), i + window_size + 1)

            for j in range(start, end):
                if i != j:
                    word2 = words[j]
                    # Use sorted pair to avoid duplicates
                    pair = tuple(sorted([word1, word2]))
                    cooccur[pair] += 1

        return dict(cooccur)


# ============================================================================
# KEYWORD EXTRACTION
# ============================================================================

class KeywordExtractor:
    """
    Extract keywords from text.
    """

    @staticmethod
    def extract_by_frequency(text: str, top_k: int = 10,
                            stop_words: Set[str] = None) -> List[Tuple[str, int]]:
        """
        Extract keywords by word frequency.

        Simple but effective baseline.

        Time: O(n log k)
        """
        if stop_words is None:
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on',
                         'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is',
                         'was', 'are', 'were', 'be', 'been', 'being', 'have',
                         'has', 'had', 'do', 'does', 'did', 'will', 'would',
                         'should', 'could', 'may', 'might', 'can', 'must'}

        words = re.findall(r'\b\w+\b', text.lower())
        filtered_words = [w for w in words if w not in stop_words]

        freq = Counter(filtered_words)
        return freq.most_common(top_k)

    @staticmethod
    def extract_by_tfidf(documents: List[str], doc_idx: int,
                        top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Extract keywords using TF-IDF.

        More sophisticated than pure frequency.

        Time: O(n * m) where n = docs, m = vocab size
        """
        tfidf = TFIDF(documents)
        return tfidf.top_terms(doc_idx, k=top_k)


# ============================================================================
# EXAMPLES
# ============================================================================

def example_frequency_analysis():
    print("=" * 70)
    print("EXAMPLE 1: Frequency Analysis")
    print("=" * 70)

    text = "The quick brown fox jumps over the lazy dog. The dog barks."

    # Character frequency
    char_freq = FrequencyAnalysis.character_frequency(text, normalize=True)
    print("Top 5 characters:")
    for char, freq in sorted(char_freq.items(), key=lambda x: -x[1])[:5]:
        if char != ' ':
            print(f"  '{char}': {freq:.3f}")

    # Word frequency
    word_freq = FrequencyAnalysis.word_frequency(text)
    print("\nWord frequencies:")
    for word, count in sorted(word_freq.items(), key=lambda x: -x[1]):
        print(f"  '{word}': {count}")

    print()


def example_ngrams():
    print("=" * 70)
    print("EXAMPLE 2: N-gram Analysis")
    print("=" * 70)

    text = "to be or not to be that is the question"

    # Bigrams
    bigrams = NGramAnalyzer.most_common_ngrams(text, n=2, top_k=5)
    print("Most common bigrams:")
    for ngram, count in bigrams:
        print(f"  {' '.join(ngram)}: {count}")

    # Trigrams
    trigrams = NGramAnalyzer.most_common_ngrams(text, n=3, top_k=3)
    print("\nMost common trigrams:")
    for ngram, count in trigrams:
        print(f"  {' '.join(ngram)}: {count}")

    # Character bigrams
    char_bigrams = NGramAnalyzer.most_common_ngrams(text, n=2,
                                                    char_level=True, top_k=5)
    print("\nMost common character bigrams:")
    for ngram, count in char_bigrams:
        print(f"  '{''.join(ngram)}': {count}")

    print()


def example_tfidf():
    print("=" * 70)
    print("EXAMPLE 3: TF-IDF Analysis")
    print("=" * 70)

    documents = [
        "The cat sat on the mat",
        "The dog played in the park",
        "The cat and dog are friends"
    ]

    tfidf = TFIDF(documents)

    for i, doc in enumerate(documents):
        print(f"\nDocument {i}: '{doc}'")
        print("Top TF-IDF terms:")
        for term, score in tfidf.top_terms(i, k=3):
            print(f"  {term}: {score:.3f}")

    print()


def example_collocations():
    print("=" * 70)
    print("EXAMPLE 4: Collocation Finding")
    print("=" * 70)

    text = """
    Machine learning is a subset of artificial intelligence. Deep learning
    is a subset of machine learning. Neural networks are used in deep learning.
    """

    collocations = CollocationFinder.find_bigram_collocations(text, min_freq=1,
                                                               top_k=5)

    print("Top collocations (by PMI):")
    for (w1, w2), pmi in collocations:
        print(f"  '{w1} {w2}': {pmi:.3f}")

    print()


def example_keyword_extraction():
    print("=" * 70)
    print("EXAMPLE 5: Keyword Extraction")
    print("=" * 70)

    text = """
    Python is a high-level programming language. Python supports multiple
    programming paradigms. Python is widely used in data science and machine
    learning applications.
    """

    # By frequency
    keywords_freq = KeywordExtractor.extract_by_frequency(text, top_k=5)
    print("Keywords by frequency:")
    for word, count in keywords_freq:
        print(f"  {word}: {count}")

    # By TF-IDF
    documents = [
        text,
        "Java is an object-oriented programming language",
        "JavaScript is used for web development"
    ]

    keywords_tfidf = KeywordExtractor.extract_by_tfidf(documents, 0, top_k=5)
    print("\nKeywords by TF-IDF:")
    for word, score in keywords_tfidf:
        print(f"  {word}: {score:.3f}")

    print()


if __name__ == "__main__":
    print("=" * 70)
    print("ADVANCED TEXT ANALYSIS TOOLS")
    print("=" * 70)
    print()

    example_frequency_analysis()
    example_ngrams()
    example_tfidf()
    example_collocations()
    example_keyword_extraction()

    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
