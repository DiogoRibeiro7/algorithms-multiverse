"""
Natural Language Processing Utilities
=====================================

Basic NLP utilities for text processing, including tokenization, stemming,
and text analysis.

Features:
1. Tokenization (word, sentence, character)
2. Porter Stemmer algorithm
3. Stop word removal
4. Text normalization
5. Basic POS tagging patterns
6. Simple parsing utilities
7. Text statistics

Applications:
- Text preprocessing for ML/NLP
- Information retrieval
- Search engines
- Text mining
- Document classification
"""

import re
from typing import List, Set, Dict, Tuple
from collections import Counter, defaultdict
import string


# ============================================================================
# TOKENIZATION
# ============================================================================

class Tokenizer:
    """
    Text tokenization utilities.
    """

    @staticmethod
    def word_tokenize(text: str, lowercase: bool = True) -> List[str]:
        """
        Tokenize text into words.

        Time: O(n)

        Args:
            text: Input text
            lowercase: Convert to lowercase

        Returns:
            List of word tokens
        """
        if lowercase:
            text = text.lower()

        # Split on whitespace and punctuation
        words = re.findall(r'\b\w+\b', text)
        return words

    @staticmethod
    def sentence_tokenize(text: str) -> List[str]:
        """
        Tokenize text into sentences.

        Time: O(n)

        Returns:
            List of sentences
        """
        # Simple sentence boundary detection
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def character_tokenize(text: str, include_spaces: bool = False) -> List[str]:
        """
        Tokenize text into characters.

        Time: O(n)
        """
        if include_spaces:
            return list(text)
        return [c for c in text if not c.isspace()]

    @staticmethod
    def ngram_tokenize(text: str, n: int = 2,
                      char_level: bool = False) -> List[str]:
        """
        Generate n-grams from text.

        Time: O(n)

        Args:
            text: Input text
            n: N-gram size
            char_level: Character-level or word-level

        Returns:
            List of n-grams
        """
        if char_level:
            tokens = list(text)
        else:
            tokens = Tokenizer.word_tokenize(text)

        if len(tokens) < n:
            return []

        return [' '.join(tokens[i:i+n]) if not char_level
                else ''.join(tokens[i:i+n])
                for i in range(len(tokens) - n + 1)]


# ============================================================================
# STEMMING
# ============================================================================

class PorterStemmer:
    """
    Porter Stemmer algorithm for English.

    Reduces words to their root form.
    Example: "running" -> "run", "flies" -> "fli"
    """

    def __init__(self):
        self.vowels = set('aeiou')

    def _is_consonant(self, word: str, i: int) -> bool:
        """Check if character at position i is a consonant."""
        if i < 0 or i >= len(word):
            return False

        if word[i] in self.vowels:
            return False

        if word[i] == 'y':
            if i == 0:
                return True
            return not self._is_consonant(word, i - 1)

        return True

    def _measure(self, word: str) -> int:
        """
        Calculate measure of a word.

        Measure is the number of VC sequences.
        Example: "tr" = 0, "tree" = 0, "trouble" = 1
        """
        measure = 0
        i = 0
        length = len(word)

        # Skip initial consonants
        while i < length and self._is_consonant(word, i):
            i += 1

        while i < length:
            # Skip vowels
            while i < length and not self._is_consonant(word, i):
                i += 1

            if i >= length:
                break

            measure += 1

            # Skip consonants
            while i < length and self._is_consonant(word, i):
                i += 1

        return measure

    def _contains_vowel(self, word: str) -> bool:
        """Check if word contains a vowel."""
        for i in range(len(word)):
            if not self._is_consonant(word, i):
                return True
        return False

    def _ends_double_consonant(self, word: str) -> bool:
        """Check if word ends with double consonant."""
        if len(word) < 2:
            return False

        return (word[-1] == word[-2] and
                self._is_consonant(word, len(word) - 1))

    def _ends_cvc(self, word: str) -> bool:
        """Check if word ends with consonant-vowel-consonant."""
        if len(word) < 3:
            return False

        i = len(word) - 1
        return (self._is_consonant(word, i) and
                not self._is_consonant(word, i - 1) and
                self._is_consonant(word, i - 2) and
                word[-1] not in 'wxy')

    def stem(self, word: str) -> str:
        """
        Apply Porter stemming algorithm.

        Time: O(n) where n is word length

        Args:
            word: Word to stem

        Returns:
            Stemmed word
        """
        if len(word) <= 2:
            return word

        word = word.lower()
        original_word = word

        # Step 1a
        if word.endswith('sses'):
            word = word[:-2]
        elif word.endswith('ies'):
            word = word[:-2]
        elif word.endswith('ss'):
            pass
        elif word.endswith('s'):
            word = word[:-1]

        # Step 1b
        if word.endswith('eed'):
            if self._measure(word[:-3]) > 0:
                word = word[:-1]
        elif word.endswith('ed'):
            stem = word[:-2]
            if self._contains_vowel(stem):
                word = stem
                if word.endswith('at') or word.endswith('bl') or \
                   word.endswith('iz'):
                    word += 'e'
                elif self._ends_double_consonant(word) and \
                     word[-1] not in 'lsz':
                    word = word[:-1]
                elif self._measure(word) == 1 and self._ends_cvc(word):
                    word += 'e'
        elif word.endswith('ing'):
            stem = word[:-3]
            if self._contains_vowel(stem):
                word = stem
                if word.endswith('at') or word.endswith('bl') or \
                   word.endswith('iz'):
                    word += 'e'
                elif self._ends_double_consonant(word) and \
                     word[-1] not in 'lsz':
                    word = word[:-1]
                elif self._measure(word) == 1 and self._ends_cvc(word):
                    word += 'e'

        # Step 1c
        if word.endswith('y') and self._contains_vowel(word[:-1]):
            word = word[:-1] + 'i'

        # Simplified - full Porter stemmer has more steps
        return word


# ============================================================================
# TEXT NORMALIZATION
# ============================================================================

class TextNormalizer:
    """
    Text normalization utilities.
    """

    # Common English stop words
    STOP_WORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have',
        'had', 'what', 'when', 'where', 'who', 'which', 'why', 'how'
    }

    @staticmethod
    def remove_punctuation(text: str) -> str:
        """Remove punctuation from text."""
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    @staticmethod
    def remove_numbers(text: str) -> str:
        """Remove numbers from text."""
        return re.sub(r'\d+', '', text)

    @staticmethod
    def remove_extra_whitespace(text: str) -> str:
        """Remove extra whitespace."""
        return ' '.join(text.split())

    @staticmethod
    def remove_stop_words(tokens: List[str]) -> List[str]:
        """
        Remove stop words from token list.

        Time: O(n)
        """
        return [token for token in tokens
                if token.lower() not in TextNormalizer.STOP_WORDS]

    @staticmethod
    def normalize(text: str, lowercase: bool = True,
                 remove_punct: bool = True,
                 remove_nums: bool = False,
                 remove_stops: bool = False) -> str:
        """
        Apply all normalization steps.

        Args:
            text: Input text
            lowercase: Convert to lowercase
            remove_punct: Remove punctuation
            remove_nums: Remove numbers
            remove_stops: Remove stop words

        Returns:
            Normalized text
        """
        if lowercase:
            text = text.lower()

        if remove_punct:
            text = TextNormalizer.remove_punctuation(text)

        if remove_nums:
            text = TextNormalizer.remove_numbers(text)

        text = TextNormalizer.remove_extra_whitespace(text)

        if remove_stops:
            tokens = text.split()
            tokens = TextNormalizer.remove_stop_words(tokens)
            text = ' '.join(tokens)

        return text


# ============================================================================
# TEXT STATISTICS
# ============================================================================

class TextStatistics:
    """
    Compute various text statistics.
    """

    @staticmethod
    def word_frequency(text: str, top_n: int = None) -> List[Tuple[str, int]]:
        """
        Compute word frequencies.

        Time: O(n log n)

        Args:
            text: Input text
            top_n: Return only top N words

        Returns:
            List of (word, frequency) tuples
        """
        words = Tokenizer.word_tokenize(text)
        freq = Counter(words)

        if top_n:
            return freq.most_common(top_n)
        return freq.most_common()

    @staticmethod
    def character_frequency(text: str) -> Dict[str, int]:
        """
        Compute character frequencies.

        Time: O(n)
        """
        return dict(Counter(text))

    @staticmethod
    def lexical_diversity(text: str) -> float:
        """
        Calculate lexical diversity (unique words / total words).

        Time: O(n)

        Returns:
            Diversity score in [0, 1]
        """
        words = Tokenizer.word_tokenize(text)
        if not words:
            return 0.0

        return len(set(words)) / len(words)

    @staticmethod
    def average_word_length(text: str) -> float:
        """
        Calculate average word length.

        Time: O(n)
        """
        words = Tokenizer.word_tokenize(text)
        if not words:
            return 0.0

        return sum(len(word) for word in words) / len(words)

    @staticmethod
    def readability_score(text: str) -> float:
        """
        Simple readability score (Flesch Reading Ease approximation).

        Higher score = easier to read

        Time: O(n)
        """
        sentences = Tokenizer.sentence_tokenize(text)
        words = Tokenizer.word_tokenize(text)

        if not sentences or not words:
            return 0.0

        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = TextStatistics.average_word_length(text)

        # Simplified Flesch score
        score = 206.835 - 1.015 * avg_sentence_length - \
                84.6 * avg_word_length / 5

        return max(0, min(100, score))


# ============================================================================
# SIMPLE POS TAGGING
# ============================================================================

class SimplePOSTagger:
    """
    Very simple rule-based POS tagger (educational purposes).
    """

    def __init__(self):
        # Common word patterns
        self.patterns = {
            r'.*ing$': 'VBG',  # Gerund
            r'.*ed$': 'VBD',   # Past tense verb
            r'.*ly$': 'RB',    # Adverb
            r'.*s$': 'NNS',    # Plural noun
            r'.*ion$': 'NN',   # Noun
            r'.*ment$': 'NN',  # Noun
        }

        # Common words
        self.lexicon = {
            'the': 'DT', 'a': 'DT', 'an': 'DT',
            'is': 'VBZ', 'are': 'VBP', 'was': 'VBD', 'were': 'VBD',
            'and': 'CC', 'or': 'CC', 'but': 'CC',
            'in': 'IN', 'on': 'IN', 'at': 'IN', 'to': 'TO',
            'I': 'PRP', 'you': 'PRP', 'he': 'PRP', 'she': 'PRP',
        }

    def tag(self, text: str) -> List[Tuple[str, str]]:
        """
        Tag words with parts of speech.

        Returns:
            List of (word, tag) tuples
        """
        words = Tokenizer.word_tokenize(text, lowercase=False)
        tagged = []

        for word in words:
            word_lower = word.lower()

            # Check lexicon
            if word_lower in self.lexicon:
                tagged.append((word, self.lexicon[word_lower]))
                continue

            # Check patterns
            found = False
            for pattern, tag in self.patterns.items():
                if re.match(pattern, word_lower):
                    tagged.append((word, tag))
                    found = True
                    break

            if not found:
                # Default to noun
                tagged.append((word, 'NN'))

        return tagged


# ============================================================================
# EXAMPLES
# ============================================================================

def example_tokenization():
    """Walk through tokenization utilities with sample output."""
    print("=" * 70)
    print("EXAMPLE 1: Tokenization")
    print("=" * 70)

    text = "The quick brown fox jumps over the lazy dog. What a fox!"

    print(f"Text: '{text}'\n")

    # Word tokenization
    words = Tokenizer.word_tokenize(text)
    print(f"Words: {words}\n")

    # Sentence tokenization
    sentences = Tokenizer.sentence_tokenize(text)
    print(f"Sentences: {sentences}\n")

    # N-grams
    bigrams = Tokenizer.ngram_tokenize(text, n=2)
    print(f"Bigrams: {bigrams[:5]}...\n")

    trigrams = Tokenizer.ngram_tokenize(text, n=3)
    print(f"Trigrams: {trigrams[:3]}...\n")


def example_stemming():
    """Showcase the toy Porter stemmer on representative words."""
    print("=" * 70)
    print("EXAMPLE 2: Porter Stemmer")
    print("=" * 70)

    stemmer = PorterStemmer()

    words = ["running", "runs", "ran", "runner", "flies", "flying",
             "happily", "happiness", "connection", "connected"]

    print("Word -> Stem:")
    for word in words:
        stem = stemmer.stem(word)
        print(f"  {word:15} -> {stem}")

    print()


def example_normalization():
    """Demonstrate successive normalization toggles on the same text."""
    print("=" * 70)
    print("EXAMPLE 3: Text Normalization")
    print("=" * 70)

    text = "The Quick BROWN Fox!!! Jumps over the 123 lazy dogs."

    print(f"Original: '{text}'\n")

    # Different normalization levels
    norm1 = TextNormalizer.normalize(text, lowercase=True,
                                    remove_punct=False)
    print(f"Lowercase: '{norm1}'")

    norm2 = TextNormalizer.normalize(text, remove_punct=True)
    print(f"No punctuation: '{norm2}'")

    norm3 = TextNormalizer.normalize(text, remove_nums=True)
    print(f"No numbers: '{norm3}'")

    norm4 = TextNormalizer.normalize(text, remove_stops=True)
    print(f"No stop words: '{norm4}'")

    print()


def example_statistics():
    """Highlight word frequency, diversity, length, and readability stats."""
    print("=" * 70)
    print("EXAMPLE 4: Text Statistics")
    print("=" * 70)

    text = """
    The quick brown fox jumps over the lazy dog. The dog was really lazy.
    Meanwhile, the fox was very quick and brown.
    """

    print(f"Text: {text.strip()}\n")

    # Word frequency
    freq = TextStatistics.word_frequency(text, top_n=5)
    print("Top 5 words:")
    for word, count in freq:
        print(f"  '{word}': {count}")

    # Statistics
    print(f"\nLexical diversity: {TextStatistics.lexical_diversity(text):.3f}")
    print(f"Average word length: " \
          f"{TextStatistics.average_word_length(text):.2f}")
    print(f"Readability score: " \
          f"{TextStatistics.readability_score(text):.1f}")

    print()


def example_pos_tagging():
    """Illustrate the rule-based POS tagger on a tiny sentence."""
    print("=" * 70)
    print("EXAMPLE 5: Simple POS Tagging")
    print("=" * 70)

    tagger = SimplePOSTagger()

    text = "The quick fox is running quickly"

    tagged = tagger.tag(text)

    print(f"Text: '{text}'\n")
    print("Tagged:")
    for word, tag in tagged:
        print(f"  {word:10} -> {tag}")

    print()


if __name__ == "__main__":
    print("=" * 70)
    print("NLP UTILITIES")
    print("=" * 70)
    print()

    example_tokenization()
    example_stemming()
    example_normalization()
    example_statistics()
    example_pos_tagging()

    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
