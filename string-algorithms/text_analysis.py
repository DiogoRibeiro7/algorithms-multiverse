"""
Text Analysis and NLP Utilities
================================

This module implements various text analysis and natural language processing utilities.

Features:
1. Tokenization (word, sentence, character)
2. N-gram generation
3. Frequency analysis
4. Text statistics
5. Basic stemming and lemmatization
6. Stop words removal
7. TF-IDF calculation
8. Text similarity metrics
9. Keyword extraction
10. Readability scores

Applications:
- Search engines
- Text mining
- Information retrieval
- Document classification
- Content analysis
"""

import re
import math
from typing import List, Dict, Tuple, Set, Optional
from collections import Counter, defaultdict
import string


class Tokenizer:
    """
    Text tokenization utilities.
    """

    @staticmethod
    def word_tokenize(text: str, lowercase: bool = True) -> List[str]:
        """
        Split text into words.

        Args:
            text: Input text
            lowercase: Convert to lowercase

        Returns: List of words
        """
        if lowercase:
            text = text.lower()

        # Simple word tokenization
        words = re.findall(r'\b\w+\b', text)
        return words

    @staticmethod
    def sentence_tokenize(text: str) -> List[str]:
        """
        Split text into sentences.

        Returns: List of sentences
        """
        # Simple sentence splitting on . ! ?
        sentences = re.split(r'[.!?]+', text)
        # Remove empty sentences and strip whitespace
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    @staticmethod
    def character_tokenize(text: str, include_spaces: bool = False) -> List[str]:
        """
        Split text into characters.

        Args:
            text: Input text
            include_spaces: Include whitespace characters

        Returns: List of characters
        """
        if include_spaces:
            return list(text)
        return [c for c in text if not c.isspace()]

    @staticmethod
    def n_gram_tokenize(text: str, n: int, word_level: bool = True) -> List[str]:
        """
        Generate n-grams from text.

        Args:
            text: Input text
            n: N-gram size
            word_level: True for word n-grams, False for character n-grams

        Returns: List of n-grams as strings
        """
        if word_level:
            tokens = Tokenizer.word_tokenize(text)
        else:
            tokens = list(text)

        if len(tokens) < n:
            return []

        ngrams = []
        for i in range(len(tokens) - n + 1):
            if word_level:
                ngram = ' '.join(tokens[i:i + n])
            else:
                ngram = ''.join(tokens[i:i + n])
            ngrams.append(ngram)

        return ngrams


class NGramAnalyzer:
    """
    N-gram analysis and generation.
    """

    @staticmethod
    def generate_ngrams(text: str, n: int, word_level: bool = True) -> Dict[str, int]:
        """
        Generate n-grams with frequencies.

        Returns: Dictionary mapping n-gram to count
        """
        ngrams = Tokenizer.n_gram_tokenize(text, n, word_level)
        return Counter(ngrams)

    @staticmethod
    def most_common_ngrams(text: str, n: int, top_k: int = 10, word_level: bool = True) -> List[Tuple[str, int]]:
        """
        Get most common n-grams.

        Args:
            text: Input text
            n: N-gram size
            top_k: Number of top n-grams to return
            word_level: Word or character n-grams

        Returns: List of (ngram, count) tuples
        """
        ngrams = NGramAnalyzer.generate_ngrams(text, n, word_level)
        return Counter(ngrams).most_common(top_k)

    @staticmethod
    def ngram_probability(text: str, n: int) -> Dict[str, float]:
        """
        Calculate n-gram probabilities.

        Returns: Dictionary mapping n-gram to probability
        """
        ngrams = Tokenizer.n_gram_tokenize(text, n)
        total = len(ngrams)

        if total == 0:
            return {}

        counts = Counter(ngrams)
        return {ngram: count / total for ngram, count in counts.items()}


class FrequencyAnalyzer:
    """
    Text frequency analysis.
    """

    @staticmethod
    def word_frequency(text: str, top_k: Optional[int] = None) -> Dict[str, int]:
        """
        Count word frequencies.

        Args:
            text: Input text
            top_k: Return only top k words (None for all)

        Returns: Dictionary or list of (word, count) tuples
        """
        words = Tokenizer.word_tokenize(text)
        counter = Counter(words)

        if top_k:
            return dict(counter.most_common(top_k))
        return dict(counter)

    @staticmethod
    def character_frequency(text: str) -> Dict[str, int]:
        """
        Count character frequencies.

        Returns: Dictionary mapping character to count
        """
        return dict(Counter(text))

    @staticmethod
    def letter_frequency(text: str) -> Dict[str, int]:
        """
        Count letter frequencies (alphabetic only).

        Returns: Dictionary mapping letter to count
        """
        letters = [c.lower() for c in text if c.isalpha()]
        return dict(Counter(letters))

    @staticmethod
    def zipf_analysis(text: str) -> List[Tuple[str, int, int]]:
        """
        Analyze text according to Zipf's law.

        Zipf's law: frequency × rank ≈ constant

        Returns: List of (word, rank, frequency) tuples
        """
        words = Tokenizer.word_tokenize(text)
        counter = Counter(words)
        ranked = counter.most_common()

        result = []
        for rank, (word, freq) in enumerate(ranked, 1):
            result.append((word, rank, freq))

        return result


class TextStatistics:
    """
    Compute various text statistics.
    """

    @staticmethod
    def basic_stats(text: str) -> Dict[str, int]:
        """
        Compute basic text statistics.

        Returns: Dictionary with various counts
        """
        words = Tokenizer.word_tokenize(text)
        sentences = Tokenizer.sentence_tokenize(text)
        characters = Tokenizer.character_tokenize(text)

        return {
            'characters': len(text),
            'characters_no_spaces': len(characters),
            'words': len(words),
            'sentences': len(sentences),
            'unique_words': len(set(words)),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
        }

    @staticmethod
    def lexical_diversity(text: str) -> float:
        """
        Calculate lexical diversity (type-token ratio).

        Returns: unique_words / total_words

        Higher values indicate more diverse vocabulary.
        """
        words = Tokenizer.word_tokenize(text)
        if not words:
            return 0.0

        unique = len(set(words))
        total = len(words)

        return unique / total

    @staticmethod
    def flesch_reading_ease(text: str) -> float:
        """
        Calculate Flesch Reading Ease score.

        Formula: 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)

        Score interpretation:
        90-100: Very easy (5th grade)
        80-90:  Easy (6th grade)
        70-80:  Fairly easy (7th grade)
        60-70:  Standard (8th-9th grade)
        50-60:  Fairly difficult (10th-12th grade)
        30-50:  Difficult (College)
        0-30:   Very difficult (College graduate)

        Returns: Reading ease score (0-100)
        """
        words = Tokenizer.word_tokenize(text)
        sentences = Tokenizer.sentence_tokenize(text)

        if not words or not sentences:
            return 0.0

        total_words = len(words)
        total_sentences = len(sentences)
        total_syllables = sum(TextStatistics._count_syllables(w) for w in words)

        score = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)

        return max(0, min(100, score))  # Clamp to 0-100

    @staticmethod
    def _count_syllables(word: str) -> int:
        """
        Estimate syllable count (simple heuristic).
        """
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        prev_was_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                count += 1
            prev_was_vowel = is_vowel

        # Adjust for silent e
        if word.endswith('e'):
            count -= 1

        # At least one syllable
        return max(1, count)


class StopWords:
    """
    Stop words management.
    """

    # Common English stop words
    ENGLISH_STOP_WORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have',
        'had', 'what', 'when', 'where', 'who', 'which', 'why', 'how'
    }

    @staticmethod
    def remove_stop_words(text: str, custom_stop_words: Optional[Set[str]] = None) -> str:
        """
        Remove stop words from text.

        Args:
            text: Input text
            custom_stop_words: Custom set of stop words (uses default if None)

        Returns: Text with stop words removed
        """
        stop_words = custom_stop_words if custom_stop_words else StopWords.ENGLISH_STOP_WORDS

        words = Tokenizer.word_tokenize(text)
        filtered = [w for w in words if w.lower() not in stop_words]

        return ' '.join(filtered)

    @staticmethod
    def filter_words(words: List[str], custom_stop_words: Optional[Set[str]] = None) -> List[str]:
        """
        Filter stop words from word list.
        """
        stop_words = custom_stop_words if custom_stop_words else StopWords.ENGLISH_STOP_WORDS
        return [w for w in words if w.lower() not in stop_words]


class SimpleStemmer:
    """
    Simple rule-based stemmer (Porter Stemmer simplified).
    """

    @staticmethod
    def stem(word: str) -> str:
        """
        Apply simple stemming rules.

        Note: This is a simplified stemmer. For production use,
        consider NLTK's Porter or Snowball stemmers.
        """
        word = word.lower()

        # Remove common suffixes
        suffixes = [
            ('sses', 'ss'), ('ies', 'i'), ('ss', 'ss'), ('s', ''),
            ('eed', 'ee'), ('ed', ''), ('ing', ''),
            ('ational', 'ate'), ('tional', 'tion'), ('ful', ''),
            ('ness', ''), ('ous', ''), ('ive', ''), ('ize', ''),
        ]

        for suffix, replacement in suffixes:
            if word.endswith(suffix):
                word = word[:-len(suffix)] + replacement
                break

        return word

    @staticmethod
    def stem_words(words: List[str]) -> List[str]:
        """
        Stem a list of words.
        """
        return [SimpleStemmer.stem(w) for w in words]


class TFIDF:
    """
    TF-IDF (Term Frequency-Inverse Document Frequency) calculator.
    """

    def __init__(self):
        self.documents = []
        self.vocab = set()
        self.idf = {}

    def add_document(self, text: str):
        """
        Add a document to the corpus.
        """
        words = Tokenizer.word_tokenize(text)
        self.documents.append(words)
        self.vocab.update(words)

    def compute_idf(self):
        """
        Compute IDF for all terms.

        IDF(term) = log(total_docs / docs_containing_term)
        """
        n_docs = len(self.documents)

        for term in self.vocab:
            # Count documents containing term
            doc_count = sum(1 for doc in self.documents if term in doc)
            self.idf[term] = math.log(n_docs / doc_count) if doc_count > 0 else 0

    def compute_tf(self, document: List[str]) -> Dict[str, float]:
        """
        Compute TF for a document.

        TF(term) = count(term) / total_terms
        """
        total = len(document)
        if total == 0:
            return {}

        tf = Counter(document)
        return {term: count / total for term, count in tf.items()}

    def compute_tfidf(self, text: str) -> Dict[str, float]:
        """
        Compute TF-IDF scores for a document.

        Returns: Dictionary mapping term to TF-IDF score
        """
        if not self.idf:
            self.compute_idf()

        words = Tokenizer.word_tokenize(text)
        tf = self.compute_tf(words)

        tfidf = {}
        for term, tf_score in tf.items():
            idf_score = self.idf.get(term, 0)
            tfidf[term] = tf_score * idf_score

        return tfidf

    def extract_keywords(self, text: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Extract top keywords using TF-IDF.

        Args:
            text: Input text
            top_k: Number of top keywords

        Returns: List of (keyword, score) tuples
        """
        tfidf = self.compute_tfidf(text)
        return sorted(tfidf.items(), key=lambda x: x[1], reverse=True)[:top_k]


class KeywordExtractor:
    """
    Keyword extraction utilities.
    """

    @staticmethod
    def extract_by_frequency(text: str, top_k: int = 10, remove_stop_words: bool = True) -> List[Tuple[str, int]]:
        """
        Extract keywords by frequency.

        Args:
            text: Input text
            top_k: Number of keywords
            remove_stop_words: Remove stop words

        Returns: List of (keyword, frequency) tuples
        """
        words = Tokenizer.word_tokenize(text)

        if remove_stop_words:
            words = StopWords.filter_words(words)

        counter = Counter(words)
        return counter.most_common(top_k)

    @staticmethod
    def extract_noun_phrases(text: str) -> List[str]:
        """
        Extract simple noun phrases (very basic).

        Note: This is a simplified version. For production,
        use proper POS tagging with NLTK or spaCy.

        Returns: List of potential noun phrases
        """
        # Simple pattern: adjective* noun+
        # This is very simplified and won't work well for real NLP
        words = Tokenizer.word_tokenize(text, lowercase=False)

        phrases = []
        current_phrase = []

        for word in words:
            # Very simple heuristic: capitalized words might be nouns
            if word[0].isupper() and len(word) > 2:
                current_phrase.append(word)
            else:
                if len(current_phrase) > 1:
                    phrases.append(' '.join(current_phrase))
                current_phrase = []

        if len(current_phrase) > 1:
            phrases.append(' '.join(current_phrase))

        return phrases


# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TEXT ANALYSIS AND NLP UTILITIES")
    print("=" * 70)

    # Sample text
    sample_text = """
    Natural language processing (NLP) is a subfield of linguistics, computer science,
    and artificial intelligence concerned with the interactions between computers and
    human language. In particular, how to program computers to process and analyze
    large amounts of natural language data. The goal is a computer capable of
    understanding the contents of documents, including the contextual nuances of the
    language within them. The technology can then accurately extract information and
    insights contained in the documents as well as categorize and organize the
    documents themselves.
    """

    # Example 1: Tokenization
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Tokenization")
    print("=" * 70)

    words = Tokenizer.word_tokenize(sample_text)
    sentences = Tokenizer.sentence_tokenize(sample_text)

    print(f"Number of words: {len(words)}")
    print(f"Number of sentences: {len(sentences)}")
    print(f"\nFirst 10 words: {words[:10]}")
    print(f"\nFirst sentence: {sentences[0]}")

    # Example 2: N-grams
    print("\n" + "=" * 70)
    print("EXAMPLE 2: N-gram Analysis")
    print("=" * 70)

    bigrams = NGramAnalyzer.most_common_ngrams(sample_text, 2, top_k=5)
    trigrams = NGramAnalyzer.most_common_ngrams(sample_text, 3, top_k=5)

    print("Top 5 bigrams:")
    for ngram, count in bigrams:
        print(f"  '{ngram}': {count}")

    print("\nTop 5 trigrams:")
    for ngram, count in trigrams:
        print(f"  '{ngram}': {count}")

    # Character n-grams
    char_trigrams = NGramAnalyzer.most_common_ngrams(sample_text, 3, top_k=5, word_level=False)
    print("\nTop 5 character trigrams:")
    for ngram, count in char_trigrams:
        print(f"  '{ngram}': {count}")

    # Example 3: Frequency Analysis
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Frequency Analysis")
    print("=" * 70)

    word_freq = FrequencyAnalyzer.word_frequency(sample_text, top_k=10)
    print("Top 10 words by frequency:")
    for word, count in sorted(word_freq.items(), key=lambda x: x[1], reverse=True):
        print(f"  '{word}': {count}")

    # Zipf's law analysis
    zipf = FrequencyAnalyzer.zipf_analysis(sample_text)[:5]
    print("\nZipf's law analysis (top 5):")
    for word, rank, freq in zipf:
        print(f"  Rank {rank}: '{word}' (freq={freq}, rank×freq={rank * freq})")

    # Example 4: Text Statistics
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Text Statistics")
    print("=" * 70)

    stats = TextStatistics.basic_stats(sample_text)
    print("Basic statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value if isinstance(value, int) else f'{value:.2f}'}")

    diversity = TextStatistics.lexical_diversity(sample_text)
    reading_ease = TextStatistics.flesch_reading_ease(sample_text)

    print(f"\nLexical diversity: {diversity:.4f}")
    print(f"Flesch Reading Ease: {reading_ease:.2f}")

    # Example 5: Stop Words Removal
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Stop Words Removal")
    print("=" * 70)

    test_sentence = "the quick brown fox jumps over the lazy dog"
    filtered = StopWords.remove_stop_words(test_sentence)

    print(f"Original:  '{test_sentence}'")
    print(f"Filtered:  '{filtered}'")

    # Example 6: Simple Stemming
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Simple Stemming")
    print("=" * 70)

    test_words = ["running", "runs", "ran", "easily", "fairly", "nationalization"]
    stemmed = SimpleStemmer.stem_words(test_words)

    print("Word stemming:")
    for original, stem in zip(test_words, stemmed):
        print(f"  {original:20} -> {stem}")

    # Example 7: TF-IDF
    print("\n" + "=" * 70)
    print("EXAMPLE 7: TF-IDF Analysis")
    print("=" * 70)

    # Create a small corpus
    tfidf = TFIDF()
    docs = [
        "the cat sat on the mat",
        "the dog sat on the log",
        "cats and dogs are enemies",
        "the cat and dog played together"
    ]

    for doc in docs:
        tfidf.add_document(doc)

    # Extract keywords from a new document
    test_doc = "the cat and dog are friends"
    keywords = tfidf.extract_keywords(test_doc, top_k=5)

    print(f"Test document: '{test_doc}'")
    print("\nTop keywords by TF-IDF:")
    for word, score in keywords:
        print(f"  '{word}': {score:.4f}")

    # Example 8: Keyword Extraction
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Keyword Extraction")
    print("=" * 70)

    keywords = KeywordExtractor.extract_by_frequency(sample_text, top_k=10, remove_stop_words=True)

    print("Top keywords (by frequency, stop words removed):")
    for word, freq in keywords:
        print(f"  '{word}': {freq}")

    print("\n" + "=" * 70)
