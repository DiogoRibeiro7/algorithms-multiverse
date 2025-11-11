# String Processing and Analysis Utilities

Comprehensive collection of string processing, analysis, and natural language processing utilities implemented across multiple languages.

## 📚 Table of Contents

- [Overview](#overview)
- [Modules](#modules)
- [Algorithms Implemented](#algorithms-implemented)
- [Quick Start](#quick-start)
- [Detailed Documentation](#detailed-documentation)
- [Performance Characteristics](#performance-characteristics)
- [Use Cases](#use-cases)
- [Examples](#examples)

## 🎯 Overview

This collection provides production-ready implementations of advanced string processing algorithms and utilities, covering:

- **Pattern Matching** - 6 algorithms (KMP, Boyer-Moore, Rabin-Karp, Aho-Corasick, Z-algorithm, Manacher)
- **Suffix Structures** - Suffix arrays, LCP arrays, suffix trees
- **Edit Distance** - Hamming, Levenshtein, Damerau-Levenshtein, LCS
- **Compression** - RLE, LZ77, Huffman, Burrows-Wheeler Transform
- **Text Analysis** - Tokenization, n-grams, frequency analysis, TF-IDF
- **Fuzzy Matching** - Phonetic algorithms, approximate matching, similarity search
- **String Hashing** - Multiple hash functions, rolling hash

## 📦 Modules

### 1. Pattern Matching (`pattern_matching.py`)
Core pattern matching algorithms for finding substrings in text.

**Algorithms:**
- Knuth-Morris-Pratt (KMP)
- Boyer-Moore
- Rabin-Karp
- Aho-Corasick
- Z-algorithm
- Manacher's Algorithm

### 2. Suffix Array (`suffix_array.py`)
Suffix array construction and applications.

**Features:**
- Naive O(n² log n) construction
- Prefix doubling O(n log² n)
- Kasai's LCP algorithm O(n)
- Pattern searching
- Longest repeated substring
- Distinct substring counting
- Longest common substring

### 3. Edit Distance (`edit_distance.py`)
String similarity and edit distance metrics.

**Algorithms:**
- Hamming distance
- Levenshtein distance (space-optimized)
- Damerau-Levenshtein distance
- Longest Common Subsequence (LCS)
- Weighted edit distance
- Edit sequence reconstruction
- Jaro distance
- Jaro-Winkler distance

### 4. String Compression (`string_compression.py`)
Data compression algorithms for strings.

**Algorithms:**
- Run-Length Encoding (RLE)
- LZ77 (Lempel-Ziv)
- Huffman Coding
- Burrows-Wheeler Transform (BWT)
- Compression ratio analysis

### 5. Text Analysis (`text_analysis.py`)
Natural language processing and text analysis utilities.

**Features:**
- Tokenization (word, sentence, character, n-gram)
- Frequency analysis
- Text statistics (lexical diversity, readability scores)
- Stop words removal
- Simple stemming
- TF-IDF calculation
- Keyword extraction
- N-gram analysis

### 6. Fuzzy Matching (`fuzzy_matching.py`)
Approximate string matching and phonetic algorithms.

**Features:**
- String hashing (polynomial, FNV-1a, DJB2, MurmurHash3)
- Rolling hash
- Soundex algorithm
- Metaphone algorithm
- Fuzzy search
- Wildcard matching
- Simple regex engine
- Similarity search

## 🚀 Quick Start

### Pattern Matching

```python
from pattern_matching import KMP, BoyerMoore, AhoCorasick

text = "the quick brown fox jumps over the lazy dog"
pattern = "quick"

# Single pattern search
matches = KMP.search(text, pattern)
print(f"Pattern found at: {matches}")  # [4]

# Multiple pattern search
ac = AhoCorasick()
ac.add_pattern("quick")
ac.add_pattern("fox")
ac.add_pattern("dog")
ac.build_failure_links()
results = ac.search(text)
print(f"All matches: {results}")
```

### Suffix Array

```python
from suffix_array import SuffixArray, SuffixArrayApplications

text = "banana"

# Build suffix array and LCP
sa, lcp = SuffixArray.build_with_lcp(text)
print(f"Suffix array: {sa}")
print(f"LCP array: {lcp}")

# Find longest repeated substring
lrs = SuffixArrayApplications.longest_repeated_substring(text, sa, lcp)
print(f"Longest repeated substring: '{lrs}'")  # 'ana'
```

### Edit Distance

```python
from edit_distance import EditDistance, SimilarityMetrics

str1 = "kitten"
str2 = "sitting"

# Compute edit distance
distance = EditDistance.levenshtein(str1, str2)
print(f"Edit distance: {distance}")  # 3

# Compute similarity
similarity = SimilarityMetrics.normalized_levenshtein(str1, str2)
print(f"Similarity: {similarity:.2%}")  # 57.14%

# Get edit sequence
sequence = EditDistance.edit_sequence(str1, str2)
for op, pos, char in sequence:
    if op != 'match':
        print(f"{op} '{char}' at position {pos}")
```

### String Compression

```python
from string_compression import RunLengthEncoding, LZ77, HuffmanCoding

text = "aaabbbcccaaa"

# Run-Length Encoding
rle = RunLengthEncoding()
compressed = rle.compress(text)
print(f"RLE: '{text}' -> '{compressed}'")  # '3a3b3c3a'

# LZ77
lz77 = LZ77()
compressed = lz77.compress("abracadabra")
decompressed = lz77.decompress(compressed)
print(f"LZ77 works: {text == decompressed}")

# Huffman
huffman = HuffmanCoding()
compressed, codes = huffman.compress(text)
print(f"Huffman codes: {codes}")
```

### Text Analysis

```python
from text_analysis import Tokenizer, FrequencyAnalyzer, TFIDF, TextStatistics

text = "The quick brown fox jumps over the lazy dog. The dog was very lazy."

# Tokenization
words = Tokenizer.word_tokenize(text)
sentences = Tokenizer.sentence_tokenize(text)
bigrams = Tokenizer.n_gram_tokenize(text, 2)

# Frequency analysis
freq = FrequencyAnalyzer.word_frequency(text, top_k=5)
print(f"Top 5 words: {freq}")

# Text statistics
stats = TextStatistics.basic_stats(text)
readability = TextStatistics.flesch_reading_ease(text)
print(f"Readability score: {readability:.2f}")

# TF-IDF
tfidf = TFIDF()
tfidf.add_document("the cat sat on the mat")
tfidf.add_document("the dog sat on the log")
keywords = tfidf.extract_keywords("the cat and dog are friends", top_k=3)
print(f"Keywords: {keywords}")
```

### Fuzzy Matching

```python
from fuzzy_matching import PhoneticAlgorithms, FuzzyMatcher, SimilaritySearch

# Soundex - phonetic matching
name1, name2 = "Smith", "Smythe"
code1 = PhoneticAlgorithms.soundex(name1)
code2 = PhoneticAlgorithms.soundex(name2)
print(f"{name1} ({code1}) == {name2} ({code2}): {code1 == code2}")  # True

# Fuzzy search with errors
text = "the quick brown fox"
matches = FuzzyMatcher.fuzzy_search(text, "quik", max_errors=1)
print(f"Fuzzy matches: {matches}")  # [(4, 1)]

# Wildcard matching
result = FuzzyMatcher.wildcard_match("hello", "h*o")
print(f"Wildcard match: {result}")  # True

# Similarity search
names = ["Smith", "Johnson", "Williams", "Jones"]
search = SimilaritySearch(names)
similar = search.find_similar_soundex("Smythe")
print(f"Similar to 'Smythe': {similar}")  # ['Smith']
```

## 📊 Performance Characteristics

### Pattern Matching Algorithms

| Algorithm | Preprocessing | Searching | Best Case | Worst Case |
|-----------|--------------|-----------|-----------|------------|
| KMP | O(m) | O(n) | O(n) | O(n+m) |
| Boyer-Moore | O(m+\|Σ\|) | O(n/m) - O(nm) | O(n/m) | O(nm) |
| Rabin-Karp | O(m) | O(n) | O(n) | O(nm) |
| Aho-Corasick | O(Σm) | O(n+k) | O(n) | O(n+k) |
| Z-algorithm | O(n+m) | O(n+m) | O(n) | O(n+m) |
| Manacher | O(n) | O(n) | O(n) | O(n) |

### Suffix Array Operations

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Construction (naive) | O(n² log n) | O(n) |
| Construction (prefix doubling) | O(n log² n) | O(n) |
| LCP array (Kasai) | O(n) | O(n) |
| Pattern search | O(m log n) | O(1) |
| Longest repeated substring | O(n) | O(1) |

### Edit Distance Algorithms

| Algorithm | Time | Space | Space (optimized) |
|-----------|------|-------|-------------------|
| Hamming | O(n) | O(1) | O(1) |
| Levenshtein | O(nm) | O(nm) | O(min(n,m)) |
| Damerau-Levenshtein | O(nm) | O(nm) | - |
| LCS | O(nm) | O(nm) | O(min(n,m)) |
| Jaro | O(nm) | O(n+m) | - |

### Compression Algorithms

| Algorithm | Compression | Decompression | Space | Best For |
|-----------|-------------|---------------|-------|----------|
| RLE | O(n) | O(n) | O(n) | Repeated characters |
| LZ77 | O(n·w) | O(n) | O(w) | General purpose |
| Huffman | O(n log n) | O(n) | O(n) | Varied frequencies |
| BWT | O(n² log n) | O(n² log n) | O(n²) | Pre-processing |

*where n = text length, m = pattern length, w = window size, Σ = sum of pattern lengths, k = number of matches, |Σ| = alphabet size*

## 🎯 Use Cases

### Search Engines
- **Pattern Matching**: Fast text search with Boyer-Moore
- **Suffix Arrays**: Autocompletion, substring search
- **Text Analysis**: Keyword extraction, TF-IDF ranking
- **Fuzzy Matching**: Spell correction, "Did you mean?"

### Bioinformatics
- **Pattern Matching**: DNA sequence matching (KMP, Aho-Corasick)
- **Suffix Arrays**: Genome assembly, repeat finding
- **Edit Distance**: Sequence alignment
- **Compression**: Efficient storage of genomic data

### Data Deduplication
- **String Hashing**: Fast duplicate detection
- **Fuzzy Matching**: Near-duplicate detection
- **Edit Distance**: Record linkage
- **Phonetic Algorithms**: Name matching

### Text Processing
- **Tokenization**: Document processing
- **N-grams**: Language modeling
- **Frequency Analysis**: Text mining
- **Stemming**: Information retrieval

### Spell Checking
- **Edit Distance**: Suggest corrections
- **Phonetic Algorithms**: Sound-alike matches
- **Fuzzy Matching**: Typo tolerance
- **Text Analysis**: Context-aware suggestions

### Data Compression
- **RLE**: Image compression, simple text
- **LZ77**: General file compression (ZIP, gzip)
- **Huffman**: Optimal prefix codes
- **BWT**: bzip2 compression

## 📖 Detailed Documentation

### Pattern Matching

#### When to Use Each Algorithm

**Use KMP when:**
- Need guaranteed O(n) time
- Streaming text (no backtracking)
- Pattern is relatively short
- Predictable performance required

**Use Boyer-Moore when:**
- Large alphabet (ASCII, Unicode)
- Long patterns
- Best practical performance needed
- Text is in memory

**Use Rabin-Karp when:**
- Multiple pattern search
- Pattern matching with modifications
- Rolling hash applications
- Plagiarism detection

**Use Aho-Corasick when:**
- Searching for many patterns simultaneously
- Antivirus/IDS systems
- Content filtering
- Dictionary-based compression

**Use Z-algorithm when:**
- Simple linear-time solution needed
- Pattern preprocessing useful
- String processing tasks
- Educational purposes

**Use Manacher when:**
- Finding palindromes
- Longest palindromic substring
- DNA analysis
- String compression

### Suffix Arrays

**Applications:**
1. **Pattern Matching**: Binary search in O(m log n)
2. **Longest Repeated Substring**: Max value in LCP array
3. **Longest Common Substring**: Build combined suffix array
4. **Distinct Substrings**: n(n+1)/2 - sum(LCP)
5. **String Matching with Wildcards**: With preprocessing

**Construction Algorithms:**
- **Naive**: O(n² log n) - Simple but slow
- **Prefix Doubling**: O(n log² n) - Good balance
- **SA-IS**: O(n) - Fastest but complex

### Edit Distance

**Applications:**
1. **Spell Checking**: Find closest dictionary words
2. **DNA Alignment**: Compare genetic sequences
3. **Plagiarism Detection**: Document similarity
4. **Record Linkage**: Match database records
5. **Diff Tools**: File comparison

**Similarity Metrics:**
- **Normalized Levenshtein**: 1 - (distance / max_length)
- **Jaro**: Good for short strings (names)
- **Jaro-Winkler**: Better for names (prefix weight)
- **LCS Ratio**: 2·LCS / (len1 + len2)

### String Compression

**Choosing Compression:**

**RLE** (Run-Length Encoding):
- ✅ Very simple, fast
- ✅ Good for images, simple patterns
- ❌ Poor for natural text
- **Example**: "aaabbb" → "3a3b"

**LZ77** (Lempel-Ziv):
- ✅ Good general-purpose
- ✅ Used in ZIP, gzip, PNG
- ❌ Slow decompression
- **Example**: Replaces repeated sequences with references

**Huffman Coding**:
- ✅ Optimal prefix codes
- ✅ Good for varied frequencies
- ❌ Requires code table
- **Example**: Frequent chars get shorter codes

**BWT** (Burrows-Wheeler):
- ✅ Excellent pre-processing
- ✅ Used in bzip2
- ❌ Not compression itself
- **Example**: Rearranges to group similar chars

### Text Analysis

**Feature Extraction:**
1. **Bag of Words**: Word frequencies
2. **TF-IDF**: Important terms in documents
3. **N-grams**: Context and sequence
4. **Word Embeddings**: Semantic similarity

**Text Statistics:**
- **Lexical Diversity**: Vocabulary richness
- **Flesch Reading Ease**: Readability level
- **Zipf's Law**: Frequency-rank relationship
- **Entropy**: Information content

### Fuzzy Matching

**Phonetic Algorithms:**

**Soundex**:
- ✅ Simple, fast
- ✅ Good for names
- ❌ English-only
- ❌ Less accurate than Metaphone
- **Example**: "Smith" and "Smythe" → S530

**Metaphone**:
- ✅ More accurate than Soundex
- ✅ Better for general words
- ❌ English-only
- ❌ More complex
- **Example**: "knight" and "night" → same code

**String Hashing:**

**Polynomial Hash**:
- General purpose
- Good distribution
- Used in pattern matching

**FNV-1a / DJB2**:
- Fast, simple
- Good for hash tables
- Low collision rate

**MurmurHash**:
- Excellent distribution
- Very fast
- Good for general use

**Cryptographic (SHA, MD5)**:
- Secure
- Collision-resistant
- Slower

## 💻 Examples

### Example 1: Document Similarity

```python
from text_analysis import TFIDF, Tokenizer
from edit_distance import SimilarityMetrics

# Create corpus
tfidf = TFIDF()
docs = [
    "Machine learning is a subset of artificial intelligence",
    "Deep learning uses neural networks with multiple layers",
    "Natural language processing enables computers to understand text"
]

for doc in docs:
    tfidf.add_document(doc)

# Compare documents
doc1 = docs[0]
doc2 = docs[1]

# TF-IDF similarity
tfidf1 = tfidf.compute_tfidf(doc1)
tfidf2 = tfidf.compute_tfidf(doc2)

# Cosine similarity (simplified)
common_terms = set(tfidf1.keys()) & set(tfidf2.keys())
similarity = sum(tfidf1[t] * tfidf2[t] for t in common_terms)

print(f"TF-IDF similarity: {similarity:.4f}")

# Edit distance similarity
words1 = set(Tokenizer.word_tokenize(doc1))
words2 = set(Tokenizer.word_tokenize(doc2))
jaccard = len(words1 & words2) / len(words1 | words2)

print(f"Jaccard similarity: {jaccard:.4f}")
```

### Example 2: Spell Checker

```python
from edit_distance import EditDistance
from fuzzy_matching import PhoneticAlgorithms

class SpellChecker:
    def __init__(self, dictionary):
        self.dictionary = set(dictionary)
        self.soundex_index = {}

        for word in dictionary:
            code = PhoneticAlgorithms.soundex(word)
            if code not in self.soundex_index:
                self.soundex_index[code] = []
            self.soundex_index[code].append(word)

    def suggest(self, word, max_suggestions=5):
        # If correct, return empty
        if word in self.dictionary:
            return []

        # Get phonetically similar words
        code = PhoneticAlgorithms.soundex(word)
        candidates = self.soundex_index.get(code, list(self.dictionary))

        # Compute edit distances
        suggestions = []
        for candidate in candidates:
            dist = EditDistance.levenshtein(word, candidate)
            if dist <= 2:  # Max 2 edits
                suggestions.append((candidate, dist))

        # Sort by distance
        suggestions.sort(key=lambda x: x[1])

        return [word for word, _ in suggestions[:max_suggestions]]

# Usage
dictionary = ["hello", "world", "python", "programming", "algorithm"]
checker = SpellChecker(dictionary)

print(checker.suggest("helo"))  # ['hello']
print(checker.suggest("algoritm"))  # ['algorithm']
print(checker.suggest("wrld"))  # ['world']
```

### Example 3: Text Summarization (Keyword-Based)

```python
from text_analysis import TFIDF, Tokenizer, StopWords

def summarize(text, num_sentences=3):
    # Tokenize sentences
    sentences = Tokenizer.sentence_tokenize(text)

    # Build TF-IDF
    tfidf = TFIDF()
    for sent in sentences:
        tfidf.add_document(sent)

    # Score sentences
    scores = []
    for sent in sentences:
        sent_tfidf = tfidf.compute_tfidf(sent)
        score = sum(sent_tfidf.values())
        scores.append((sent, score))

    # Sort by score
    scores.sort(key=lambda x: x[1], reverse=True)

    # Return top sentences
    return [sent for sent, _ in scores[:num_sentences]]

# Usage
text = """
Natural language processing (NLP) is a subfield of artificial intelligence.
It focuses on the interaction between computers and human language.
NLP techniques are used in many applications.
These include machine translation, sentiment analysis, and chatbots.
The field combines linguistics, computer science, and machine learning.
"""

summary = summarize(text, num_sentences=2)
for sent in summary:
    print(f"- {sent}")
```

### Example 4: Plagiarism Detection

```python
from suffix_array import SuffixArrayApplications
from text_analysis import Tokenizer

def detect_plagiarism(doc1, doc2, min_length=10):
    # Normalize documents
    words1 = Tokenizer.word_tokenize(doc1)
    words2 = Tokenizer.word_tokenize(doc2)

    text1 = ' '.join(words1)
    text2 = ' '.join(words2)

    # Find longest common substring
    lcs = SuffixArrayApplications.longest_common_substring(text1, text2)

    # Calculate similarity
    similarity = len(lcs) / min(len(text1), len(text2))

    if len(lcs) >= min_length:
        return {
            'plagiarized': True,
            'similarity': similarity,
            'common_text': lcs,
            'length': len(lcs)
        }

    return {
        'plagiarized': False,
        'similarity': similarity
    }

# Usage
doc1 = "This is a sample document about natural language processing"
doc2 = "This is a sample document about machine learning techniques"

result = detect_plagiarism(doc1, doc2)
print(f"Plagiarized: {result['plagiarized']}")
print(f"Similarity: {result['similarity']:.2%}")
```

## 🔧 Advanced Topics

### Combining Algorithms

Many real-world applications benefit from combining multiple algorithms:

**Fuzzy Search Engine:**
```
1. Use Aho-Corasick for exact multi-pattern matching
2. Use Phonetic algorithms for sound-alike suggestions
3. Use Edit distance for typo correction
4. Use TF-IDF for relevance ranking
```

**DNA Sequence Analysis:**
```
1. Use Suffix arrays for finding repeats
2. Use Pattern matching for motif search
3. Use Edit distance for alignment
4. Use Compression for storage
```

**Document Clustering:**
```
1. Use Tokenization for feature extraction
2. Use N-grams for sequence features
3. Use TF-IDF for term weighting
4. Use Cosine similarity for clustering
```

## 📝 Best Practices

1. **Choose the Right Algorithm**: Match algorithm characteristics to your use case
2. **Consider Memory**: Use space-optimized versions for large data
3. **Preprocessing**: Amortize preprocessing cost across multiple queries
4. **Unicode Handling**: Be aware of multi-byte characters
5. **Benchmarking**: Test with real data before production
6. **Error Handling**: Validate inputs and handle edge cases
7. **Documentation**: Document assumptions and limitations

## 🎓 Learning Resources

### Books
- "Algorithms on Strings, Trees, and Sequences" by Dan Gusfield
- "Introduction to Information Retrieval" by Manning, Raghavan, and Schütze
- "Speech and Language Processing" by Jurafsky and Martin

### Papers
- Knuth-Morris-Pratt: "Fast Pattern Matching in Strings" (1977)
- Boyer-Moore: "A Fast String Searching Algorithm" (1977)
- Aho-Corasick: "Efficient String Matching" (1975)
- Manacher: "A New Linear-Time On-Line Algorithm" (1975)

### Online Resources
- CP-Algorithms: https://cp-algorithms.com/
- GeeksforGeeks String Algorithms
- TopCoder String Algorithm Tutorials

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional language implementations
- More advanced NLP features
- Performance optimizations
- Additional test cases
- Documentation improvements

## 📄 License

Part of the algorithms-multiverse repository. See main repository for license.

---

**Note**: All Python implementations are provided. Implementations in JavaScript, Java, C++, Go, and Rust are planned for future releases.
