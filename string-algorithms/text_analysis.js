/**
 * Text Analysis and NLP Utilities - JavaScript Implementation
 * ===========================================================
 *
 * Features:
 * - Tokenization (word, sentence, character, n-gram)
 * - Frequency analysis
 * - Text statistics
 * - TF-IDF calculation
 * - Keyword extraction
 *
 * Run: node text_analysis.js
 */

/**
 * Text tokenization utilities
 */
class Tokenizer {
    /**
     * Split text into words
     */
    static wordTokenize(text, lowercase = true) {
        if (lowercase) {
            text = text.toLowerCase();
        }

        // Simple word tokenization
        const words = text.match(/\b\w+\b/g) || [];
        return words;
    }

    /**
     * Split text into sentences
     */
    static sentenceTokenize(text) {
        // Simple sentence splitting on . ! ?
        const sentences = text.split(/[.!?]+/);
        // Remove empty sentences and strip whitespace
        return sentences
            .map(s => s.trim())
            .filter(s => s.length > 0);
    }

    /**
     * Split text into characters
     */
    static characterTokenize(text, includeSpaces = false) {
        if (includeSpaces) {
            return [...text];
        }
        return [...text].filter(c => !/\s/.test(c));
    }

    /**
     * Generate n-grams from text
     */
    static nGramTokenize(text, n, wordLevel = true) {
        let tokens;

        if (wordLevel) {
            tokens = Tokenizer.wordTokenize(text);
        } else {
            tokens = [...text];
        }

        if (tokens.length < n) {
            return [];
        }

        const ngrams = [];
        for (let i = 0; i <= tokens.length - n; i++) {
            if (wordLevel) {
                ngrams.push(tokens.slice(i, i + n).join(' '));
            } else {
                ngrams.push(tokens.slice(i, i + n).join(''));
            }
        }

        return ngrams;
    }
}

/**
 * N-gram analysis and generation
 */
class NGramAnalyzer {
    /**
     * Generate n-grams with frequencies
     */
    static generateNGrams(text, n, wordLevel = true) {
        const ngrams = Tokenizer.nGramTokenize(text, n, wordLevel);
        const counts = {};

        for (const ngram of ngrams) {
            counts[ngram] = (counts[ngram] || 0) + 1;
        }

        return counts;
    }

    /**
     * Get most common n-grams
     */
    static mostCommonNGrams(text, n, topK = 10, wordLevel = true) {
        const ngrams = NGramAnalyzer.generateNGrams(text, n, wordLevel);

        return Object.entries(ngrams)
            .sort((a, b) => b[1] - a[1])
            .slice(0, topK);
    }

    /**
     * Calculate n-gram probabilities
     */
    static ngramProbability(text, n) {
        const ngrams = Tokenizer.nGramTokenize(text, n);
        const total = ngrams.length;

        if (total === 0) {
            return {};
        }

        const counts = {};
        for (const ngram of ngrams) {
            counts[ngram] = (counts[ngram] || 0) + 1;
        }

        const probs = {};
        for (const [ngram, count] of Object.entries(counts)) {
            probs[ngram] = count / total;
        }

        return probs;
    }
}

/**
 * Text frequency analysis
 */
class FrequencyAnalyzer {
    /**
     * Count word frequencies
     */
    static wordFrequency(text, topK = null) {
        const words = Tokenizer.wordTokenize(text);
        const counter = {};

        for (const word of words) {
            counter[word] = (counter[word] || 0) + 1;
        }

        if (topK) {
            return Object.fromEntries(
                Object.entries(counter)
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, topK)
            );
        }

        return counter;
    }

    /**
     * Count character frequencies
     */
    static characterFrequency(text) {
        const counter = {};

        for (const char of text) {
            counter[char] = (counter[char] || 0) + 1;
        }

        return counter;
    }

    /**
     * Count letter frequencies (alphabetic only)
     */
    static letterFrequency(text) {
        const letters = [...text]
            .filter(c => /[a-zA-Z]/.test(c))
            .map(c => c.toLowerCase());

        const counter = {};
        for (const letter of letters) {
            counter[letter] = (counter[letter] || 0) + 1;
        }

        return counter;
    }

    /**
     * Analyze text according to Zipf's law
     */
    static zipfAnalysis(text) {
        const words = Tokenizer.wordTokenize(text);
        const counter = {};

        for (const word of words) {
            counter[word] = (counter[word] || 0) + 1;
        }

        const ranked = Object.entries(counter)
            .sort((a, b) => b[1] - a[1]);

        return ranked.map(([word, freq], index) => ({
            word,
            rank: index + 1,
            frequency: freq
        }));
    }
}

/**
 * Text statistics
 */
class TextStatistics {
    /**
     * Compute basic text statistics
     */
    static basicStats(text) {
        const words = Tokenizer.wordTokenize(text);
        const sentences = Tokenizer.sentenceTokenize(text);
        const characters = Tokenizer.characterTokenize(text);

        const avgWordLength = words.length > 0
            ? words.reduce((sum, w) => sum + w.length, 0) / words.length
            : 0;

        const avgSentenceLength = sentences.length > 0
            ? words.length / sentences.length
            : 0;

        return {
            characters: text.length,
            charactersNoSpaces: characters.length,
            words: words.length,
            sentences: sentences.length,
            uniqueWords: new Set(words).size,
            avgWordLength,
            avgSentenceLength
        };
    }

    /**
     * Calculate lexical diversity (type-token ratio)
     */
    static lexicalDiversity(text) {
        const words = Tokenizer.wordTokenize(text);

        if (words.length === 0) {
            return 0.0;
        }

        const unique = new Set(words).size;
        return unique / words.length;
    }

    /**
     * Calculate Flesch Reading Ease score
     * Score interpretation:
     * 90-100: Very easy (5th grade)
     * 80-90:  Easy (6th grade)
     * 70-80:  Fairly easy (7th grade)
     * 60-70:  Standard (8th-9th grade)
     * 50-60:  Fairly difficult (10th-12th grade)
     * 30-50:  Difficult (College)
     * 0-30:   Very difficult (College graduate)
     */
    static fleschReadingEase(text) {
        const words = Tokenizer.wordTokenize(text);
        const sentences = Tokenizer.sentenceTokenize(text);

        if (words.length === 0 || sentences.length === 0) {
            return 0.0;
        }

        const totalWords = words.length;
        const totalSentences = sentences.length;
        const totalSyllables = words.reduce((sum, w) => sum + TextStatistics._countSyllables(w), 0);

        const score = 206.835 - 1.015 * (totalWords / totalSentences) - 84.6 * (totalSyllables / totalWords);

        return Math.max(0, Math.min(100, score));
    }

    /**
     * Estimate syllable count (simple heuristic)
     * @private
     */
    static _countSyllables(word) {
        word = word.toLowerCase();
        let count = 0;
        const vowels = 'aeiouy';
        let prevWasVowel = false;

        for (const char of word) {
            const isVowel = vowels.includes(char);
            if (isVowel && !prevWasVowel) {
                count++;
            }
            prevWasVowel = isVowel;
        }

        // Adjust for silent e
        if (word.endsWith('e')) {
            count--;
        }

        // At least one syllable
        return Math.max(1, count);
    }
}

/**
 * Stop words management
 */
class StopWords {
    static ENGLISH_STOP_WORDS = new Set([
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'will', 'with', 'this', 'but', 'they', 'have',
        'had', 'what', 'when', 'where', 'who', 'which', 'why', 'how'
    ]);

    /**
     * Remove stop words from text
     */
    static removeStopWords(text, customStopWords = null) {
        const stopWords = customStopWords || StopWords.ENGLISH_STOP_WORDS;
        const words = Tokenizer.wordTokenize(text);

        const filtered = words.filter(w => !stopWords.has(w.toLowerCase()));
        return filtered.join(' ');
    }

    /**
     * Filter stop words from word list
     */
    static filterWords(words, customStopWords = null) {
        const stopWords = customStopWords || StopWords.ENGLISH_STOP_WORDS;
        return words.filter(w => !stopWords.has(w.toLowerCase()));
    }
}

/**
 * Simple stemmer (Porter Stemmer simplified)
 */
class SimpleStemmer {
    /**
     * Apply simple stemming rules
     */
    static stem(word) {
        word = word.toLowerCase();

        // Remove common suffixes
        const suffixes = [
            ['sses', 'ss'], ['ies', 'i'], ['ss', 'ss'], ['s', ''],
            ['eed', 'ee'], ['ed', ''], ['ing', ''],
            ['ational', 'ate'], ['tional', 'tion'], ['ful', ''],
            ['ness', ''], ['ous', ''], ['ive', ''], ['ize', '']
        ];

        for (const [suffix, replacement] of suffixes) {
            if (word.endsWith(suffix)) {
                word = word.slice(0, -suffix.length) + replacement;
                break;
            }
        }

        return word;
    }

    /**
     * Stem a list of words
     */
    static stemWords(words) {
        return words.map(w => SimpleStemmer.stem(w));
    }
}

/**
 * TF-IDF (Term Frequency-Inverse Document Frequency)
 */
class TFIDF {
    constructor() {
        this.documents = [];
        this.vocab = new Set();
        this.idf = {};
    }

    /**
     * Add a document to the corpus
     */
    addDocument(text) {
        const words = Tokenizer.wordTokenize(text);
        this.documents.push(words);
        words.forEach(w => this.vocab.add(w));
    }

    /**
     * Compute IDF for all terms
     */
    computeIDF() {
        const nDocs = this.documents.length;

        for (const term of this.vocab) {
            // Count documents containing term
            const docCount = this.documents.filter(doc => doc.includes(term)).length;
            this.idf[term] = docCount > 0 ? Math.log(nDocs / docCount) : 0;
        }
    }

    /**
     * Compute TF for a document
     */
    computeTF(document) {
        const total = document.length;

        if (total === 0) {
            return {};
        }

        const counts = {};
        for (const term of document) {
            counts[term] = (counts[term] || 0) + 1;
        }

        const tf = {};
        for (const [term, count] of Object.entries(counts)) {
            tf[term] = count / total;
        }

        return tf;
    }

    /**
     * Compute TF-IDF scores for a document
     */
    computeTFIDF(text) {
        if (Object.keys(this.idf).length === 0) {
            this.computeIDF();
        }

        const words = Tokenizer.wordTokenize(text);
        const tf = this.computeTF(words);

        const tfidf = {};
        for (const [term, tfScore] of Object.entries(tf)) {
            const idfScore = this.idf[term] || 0;
            tfidf[term] = tfScore * idfScore;
        }

        return tfidf;
    }

    /**
     * Extract top keywords using TF-IDF
     */
    extractKeywords(text, topK = 10) {
        const tfidf = this.computeTFIDF(text);

        return Object.entries(tfidf)
            .sort((a, b) => b[1] - a[1])
            .slice(0, topK);
    }
}

/**
 * Keyword extraction utilities
 */
class KeywordExtractor {
    /**
     * Extract keywords by frequency
     */
    static extractByFrequency(text, topK = 10, removeStopWords = true) {
        let words = Tokenizer.wordTokenize(text);

        if (removeStopWords) {
            words = StopWords.filterWords(words);
        }

        const counter = {};
        for (const word of words) {
            counter[word] = (counter[word] || 0) + 1;
        }

        return Object.entries(counter)
            .sort((a, b) => b[1] - a[1])
            .slice(0, topK);
    }
}

// ============================================================================
// EXAMPLE USAGE AND TESTING
// ============================================================================

if (require.main === module) {
    console.log('='.repeat(70));
    console.log('TEXT ANALYSIS AND NLP UTILITIES - JAVASCRIPT');
    console.log('='.repeat(70));

    const sampleText = `
    Natural language processing (NLP) is a subfield of linguistics, computer science,
    and artificial intelligence concerned with the interactions between computers and
    human language. In particular, how to program computers to process and analyze
    large amounts of natural language data. The goal is a computer capable of
    understanding the contents of documents, including the contextual nuances of the
    language within them. The technology can then accurately extract information and
    insights contained in the documents as well as categorize and organize the
    documents themselves.
    `;

    // Example 1: Tokenization
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 1: Tokenization');
    console.log('='.repeat(70));

    const words = Tokenizer.wordTokenize(sampleText);
    const sentences = Tokenizer.sentenceTokenize(sampleText);

    console.log(`Number of words: ${words.length}`);
    console.log(`Number of sentences: ${sentences.length}`);
    console.log(`\nFirst 10 words: ${words.slice(0, 10).join(', ')}`);
    console.log(`\nFirst sentence: ${sentences[0]}`);

    // Example 2: N-grams
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 2: N-gram Analysis');
    console.log('='.repeat(70));

    const bigrams = NGramAnalyzer.mostCommonNGrams(sampleText, 2, 5);
    const trigrams = NGramAnalyzer.mostCommonNGrams(sampleText, 3, 5);

    console.log('Top 5 bigrams:');
    for (const [ngram, count] of bigrams) {
        console.log(`  '${ngram}': ${count}`);
    }

    console.log('\nTop 5 trigrams:');
    for (const [ngram, count] of trigrams) {
        console.log(`  '${ngram}': ${count}`);
    }

    // Example 3: Frequency Analysis
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 3: Frequency Analysis');
    console.log('='.repeat(70));

    const wordFreq = FrequencyAnalyzer.wordFrequency(sampleText, 10);
    console.log('Top 10 words by frequency:');
    for (const [word, count] of Object.entries(wordFreq).sort((a, b) => b[1] - a[1])) {
        console.log(`  '${word}': ${count}`);
    }

    // Example 4: Text Statistics
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 4: Text Statistics');
    console.log('='.repeat(70));

    const stats = TextStatistics.basicStats(sampleText);
    console.log('Basic statistics:');
    for (const [key, value] of Object.entries(stats)) {
        const displayValue = Number.isInteger(value) ? value : value.toFixed(2);
        console.log(`  ${key}: ${displayValue}`);
    }

    const diversity = TextStatistics.lexicalDiversity(sampleText);
    const readingEase = TextStatistics.fleschReadingEase(sampleText);

    console.log(`\nLexical diversity: ${diversity.toFixed(4)}`);
    console.log(`Flesch Reading Ease: ${readingEase.toFixed(2)}`);

    // Example 5: Stop Words Removal
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 5: Stop Words Removal');
    console.log('='.repeat(70));

    const testSentence = 'the quick brown fox jumps over the lazy dog';
    const filtered = StopWords.removeStopWords(testSentence);

    console.log(`Original:  '${testSentence}'`);
    console.log(`Filtered:  '${filtered}'`);

    // Example 6: TF-IDF
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 6: TF-IDF Analysis');
    console.log('='.repeat(70));

    const tfidf = new TFIDF();
    const docs = [
        'the cat sat on the mat',
        'the dog sat on the log',
        'cats and dogs are enemies',
        'the cat and dog played together'
    ];

    for (const doc of docs) {
        tfidf.addDocument(doc);
    }

    const testDoc = 'the cat and dog are friends';
    const keywords = tfidf.extractKeywords(testDoc, 5);

    console.log(`Test document: '${testDoc}'`);
    console.log('\nTop keywords by TF-IDF:');
    for (const [word, score] of keywords) {
        console.log(`  '${word}': ${score.toFixed(4)}`);
    }

    console.log('\n' + '='.repeat(70));
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        Tokenizer,
        NGramAnalyzer,
        FrequencyAnalyzer,
        TextStatistics,
        StopWords,
        SimpleStemmer,
        TFIDF,
        KeywordExtractor
    };
}
