/**
 * Comprehensive Trie Data Structure Implementations in JavaScript
 *
 * This module implements multiple trie variants and applications:
 * 1. Standard Trie
 * 2. Compressed Trie (Patricia Tree)
 * 3. Suffix Trie
 * 4. Applications: Spell checker, Auto-complete, Dictionary
 *
 * Time Complexity:
 * - Insert: O(m) where m is key length
 * - Search: O(m)
 * - Delete: O(m)
 * - Prefix Search: O(p + n) where p is prefix length, n is results
 * - Space: O(ALPHABET_SIZE * N * M) where N is number of keys
 *
 * Advantages over Hash Tables:
 * ✓ Prefix-based operations
 * ✓ Ordered traversal
 * ✓ No hash collisions
 * ✓ Memory efficient for common prefixes
 *
 * Use Cases:
 * - Auto-complete systems
 * - Spell checkers
 * - IP routing (longest prefix match)
 * - Dictionary implementations
 * - DNA sequence analysis
 * - Text prediction
 */

// ============================================================================
// STANDARD TRIE
// ============================================================================

/**
 * Node in a standard trie
 */
class TrieNode {
    constructor() {
        this.children = new Map();
        this.isEndOfWord = false;
        this.frequency = 0; // For ranking suggestions
    }
}

/**
 * Standard Trie implementation
 *
 * Features:
 * - Insert, search, delete operations
 * - Prefix search
 * - Auto-completion
 * - Word frequency tracking
 */
class Trie {
    constructor() {
        this.root = new TrieNode();
        this.wordCount = 0;
    }

    /**
     * Insert a word into the trie. O(m)
     * @param {string} word - The word to insert
     * @param {number} frequency - Frequency/weight of the word
     */
    insert(word, frequency = 1) {
        let node = this.root;

        for (const char of word) {
            if (!node.children.has(char)) {
                node.children.set(char, new TrieNode());
            }
            node = node.children.get(char);
        }

        if (!node.isEndOfWord) {
            this.wordCount++;
        }

        node.isEndOfWord = true;
        node.frequency = frequency;
    }

    /**
     * Search for exact word. O(m)
     * @param {string} word - The word to search for
     * @returns {boolean} - True if word exists
     */
    search(word) {
        const node = this._findNode(word);
        return node !== null && node.isEndOfWord;
    }

    /**
     * Check if any word starts with prefix. O(p)
     * @param {string} prefix - The prefix to check
     * @returns {boolean} - True if prefix exists
     */
    startsWith(prefix) {
        return this._findNode(prefix) !== null;
    }

    /**
     * Helper to find node for given prefix
     * @param {string} prefix - The prefix to find
     * @returns {TrieNode|null} - The node or null
     */
    _findNode(prefix) {
        let node = this.root;

        for (const char of prefix) {
            if (!node.children.has(char)) {
                return null;
            }
            node = node.children.get(char);
        }

        return node;
    }

    /**
     * Delete a word from trie. O(m)
     * @param {string} word - The word to delete
     * @returns {boolean} - True if word was deleted
     */
    delete(word) {
        const deleteHelper = (node, word, index) => {
            if (index === word.length) {
                if (!node.isEndOfWord) {
                    return false;
                }

                node.isEndOfWord = false;
                this.wordCount--;
                return node.children.size === 0;
            }

            const char = word[index];
            if (!node.children.has(char)) {
                return false;
            }

            const child = node.children.get(char);
            const shouldDeleteChild = deleteHelper(child, word, index + 1);

            if (shouldDeleteChild) {
                node.children.delete(char);
                return !node.isEndOfWord && node.children.size === 0;
            }

            return false;
        };

        return deleteHelper(this.root, word, 0);
    }

    /**
     * Get word suggestions for prefix
     * @param {string} prefix - The prefix to search for
     * @param {number} limit - Maximum number of suggestions
     * @returns {Array<{word: string, frequency: number}>} - List of suggestions
     */
    autocomplete(prefix, limit = 10) {
        const node = this._findNode(prefix);
        if (!node) {
            return [];
        }

        const suggestions = [];

        const dfs = (node, currentWord) => {
            if (node.isEndOfWord) {
                suggestions.push({ word: currentWord, frequency: node.frequency });
            }

            // Sort children for consistent ordering
            const sortedChildren = Array.from(node.children.entries()).sort();
            for (const [char, child] of sortedChildren) {
                dfs(child, currentWord + char);
            }
        };

        dfs(node, prefix);

        // Sort by frequency (descending) and then alphabetically
        suggestions.sort((a, b) => {
            if (b.frequency !== a.frequency) {
                return b.frequency - a.frequency;
            }
            return a.word.localeCompare(b.word);
        });

        return suggestions.slice(0, limit);
    }

    /**
     * Find longest common prefix of all words
     * @returns {string} - The longest common prefix
     */
    longestCommonPrefix() {
        if (this.root.children.size === 0) {
            return "";
        }

        const prefix = [];
        let node = this.root;

        while (node.children.size === 1 && !node.isEndOfWord) {
            const [char, child] = node.children.entries().next().value;
            prefix.push(char);
            node = child;
        }

        return prefix.join('');
    }

    /**
     * Get all words in trie
     * @returns {Array<string>} - All words sorted
     */
    getAllWords() {
        const words = [];

        const dfs = (node, current) => {
            if (node.isEndOfWord) {
                words.push(current);
            }
            for (const [char, child] of node.children.entries()) {
                dfs(child, current + char);
            }
        };

        dfs(this.root, "");
        return words.sort();
    }

    /**
     * Count how many words have given prefix
     * @param {string} prefix - The prefix to count
     * @returns {number} - Number of words with prefix
     */
    countWordsWithPrefix(prefix) {
        const node = this._findNode(prefix);
        if (!node) {
            return 0;
        }

        let count = 0;

        const dfs = (node) => {
            if (node.isEndOfWord) {
                count++;
            }
            for (const child of node.children.values()) {
                dfs(child);
            }
        };

        dfs(node);
        return count;
    }

    /**
     * Serialize trie to JSON string
     * @returns {string} - JSON representation
     */
    serialize() {
        const nodeToObject = (node) => {
            const obj = {
                isEnd: node.isEndOfWord,
                freq: node.frequency,
                children: {}
            };

            for (const [char, child] of node.children.entries()) {
                obj.children[char] = nodeToObject(child);
            }

            return obj;
        };

        return JSON.stringify(nodeToObject(this.root));
    }

    /**
     * Deserialize trie from JSON string
     * @param {string} data - JSON string
     * @returns {Trie} - Deserialized trie
     */
    static deserialize(data) {
        const trie = new Trie();

        const objectToNode = (obj) => {
            const node = new TrieNode();
            node.isEndOfWord = obj.isEnd;
            node.frequency = obj.freq;

            for (const [char, childObj] of Object.entries(obj.children)) {
                node.children.set(char, objectToNode(childObj));
            }

            return node;
        };

        const rootObj = JSON.parse(data);
        trie.root = objectToNode(rootObj);

        // Recount words
        const countWords = (node) => {
            let count = node.isEndOfWord ? 1 : 0;
            for (const child of node.children.values()) {
                count += countWords(child);
            }
            return count;
        };

        trie.wordCount = countWords(trie.root);
        return trie;
    }
}

// ============================================================================
// COMPRESSED TRIE (PATRICIA TREE)
// ============================================================================

/**
 * Node in Patricia trie (compressed trie)
 */
class PatriciaNode {
    constructor(key = "") {
        this.key = key; // Edge label (can be multiple characters)
        this.children = new Map();
        this.isEndOfWord = false;
        this.value = null;
    }
}

/**
 * Compressed Trie (Patricia Tree)
 *
 * More space-efficient than standard trie by compressing
 * chains of single-child nodes into single edges.
 *
 * Used in:
 * - IP routing tables (CIDR)
 * - Radix trees
 * - Suffix trees
 */
class PatriciaTrie {
    constructor() {
        this.root = new PatriciaNode();
    }

    /**
     * Insert word into Patricia trie
     * @param {string} word - The word to insert
     * @param {*} value - Associated value
     */
    insert(word, value = null) {
        if (!word) return;

        let node = this.root;
        let remaining = word;

        while (remaining) {
            const matchedChar = remaining[0];

            if (!node.children.has(matchedChar)) {
                // No matching child, create new node
                const newNode = new PatriciaNode(remaining);
                newNode.isEndOfWord = true;
                newNode.value = value !== null ? value : word;
                node.children.set(matchedChar, newNode);
                return;
            }

            const child = node.children.get(matchedChar);

            // Find common prefix between remaining and child.key
            let i = 0;
            while (i < remaining.length && i < child.key.length &&
                   remaining[i] === child.key[i]) {
                i++;
            }

            if (i === child.key.length) {
                // Child key is prefix of remaining
                node = child;
                remaining = remaining.slice(i);
            } else {
                // Need to split the edge
                const common = child.key.slice(0, i);

                // Create new intermediate node
                const newNode = new PatriciaNode(common);

                // Update child key (remove common prefix)
                const oldSuffix = child.key.slice(i);
                child.key = oldSuffix;

                // Add old child to new node
                newNode.children.set(oldSuffix[0], child);

                // Add new node to parent
                node.children.set(matchedChar, newNode);

                // Add new leaf if there's remaining text
                remaining = remaining.slice(i);
                if (remaining) {
                    const leaf = new PatriciaNode(remaining);
                    leaf.isEndOfWord = true;
                    leaf.value = value !== null ? value : word;
                    newNode.children.set(remaining[0], leaf);
                } else {
                    newNode.isEndOfWord = true;
                    newNode.value = value !== null ? value : word;
                }
                return;
            }
        }

        node.isEndOfWord = true;
        node.value = value !== null ? value : word;
    }

    /**
     * Search for exact word
     * @param {string} word - The word to search for
     * @returns {boolean} - True if word exists
     */
    search(word) {
        const [node, remaining] = this._findNode(word);
        return node !== null && remaining === "" && node.isEndOfWord;
    }

    /**
     * Find node and return remaining unmatched string
     * @param {string} word - The word to find
     * @returns {[PatriciaNode|null, string]} - Node and remaining string
     */
    _findNode(word) {
        let node = this.root;
        let remaining = word;

        while (remaining) {
            const matchedChar = remaining[0];
            if (!node.children.has(matchedChar)) {
                return [null, remaining];
            }

            const child = node.children.get(matchedChar);

            // Check if remaining matches child.key
            if (!remaining.startsWith(child.key)) {
                return [null, remaining];
            }

            remaining = remaining.slice(child.key.length);
            node = child;
        }

        return [node, remaining];
    }
}

// ============================================================================
// SUFFIX TRIE
// ============================================================================

/**
 * Suffix Trie for pattern matching
 *
 * Stores all suffixes of a text for efficient pattern search.
 *
 * Applications:
 * - Substring search
 * - Pattern matching
 * - DNA sequence analysis
 */
class SuffixTrie {
    constructor(text) {
        this.trie = new Trie();
        this.text = text;

        // Insert all suffixes
        for (let i = 0; i < text.length; i++) {
            this.trie.insert(text.slice(i));
        }
    }

    /**
     * Check if pattern exists as substring
     * @param {string} pattern - The pattern to search for
     * @returns {boolean} - True if pattern exists
     */
    containsSubstring(pattern) {
        return this.trie.startsWith(pattern);
    }

    /**
     * Find all starting positions of pattern in text
     * @param {string} pattern - The pattern to find
     * @returns {Array<number>} - Starting positions
     */
    findAllOccurrences(pattern) {
        const positions = [];

        for (let i = 0; i < this.text.length; i++) {
            if (this.text.slice(i).startsWith(pattern)) {
                positions.push(i);
            }
        }

        return positions;
    }
}

// ============================================================================
// APPLICATIONS
// ============================================================================

/**
 * Spell checker using trie
 *
 * Features:
 * - Dictionary lookup
 * - Suggestions for misspelled words
 * - Edit distance calculations
 */
class SpellChecker {
    constructor(dictionary) {
        this.trie = new Trie();
        for (const word of dictionary) {
            this.trie.insert(word.toLowerCase());
        }
    }

    /**
     * Check if word is spelled correctly
     * @param {string} word - The word to check
     * @returns {boolean} - True if correct
     */
    isCorrect(word) {
        return this.trie.search(word.toLowerCase());
    }

    /**
     * Suggest corrections for misspelled word
     * @param {string} word - The word to correct
     * @param {number} maxDistance - Maximum edit distance
     * @returns {Array<string>} - Suggestions
     */
    suggest(word, maxDistance = 2) {
        word = word.toLowerCase();

        if (this.isCorrect(word)) {
            return [word];
        }

        const suggestions = new Set();
        const candidates = this._generateCandidates(word, maxDistance);

        for (const candidate of candidates) {
            if (this.trie.search(candidate)) {
                suggestions.add(candidate);
            }
        }

        return Array.from(suggestions).sort().slice(0, 10);
    }

    /**
     * Generate candidate words within edit distance
     * @param {string} word - The word
     * @param {number} maxDistance - Maximum distance
     * @returns {Set<string>} - Candidates
     */
    _generateCandidates(word, maxDistance) {
        if (maxDistance === 0) {
            return new Set([word]);
        }

        const candidates = new Set([word]);
        const alphabet = 'abcdefghijklmnopqrstuvwxyz';

        // Deletions
        for (let i = 0; i < word.length; i++) {
            candidates.add(word.slice(0, i) + word.slice(i + 1));
        }

        // Transpositions
        for (let i = 0; i < word.length - 1; i++) {
            candidates.add(word.slice(0, i) + word[i + 1] + word[i] + word.slice(i + 2));
        }

        // Replacements
        for (let i = 0; i < word.length; i++) {
            for (const c of alphabet) {
                candidates.add(word.slice(0, i) + c + word.slice(i + 1));
            }
        }

        // Insertions
        for (let i = 0; i <= word.length; i++) {
            for (const c of alphabet) {
                candidates.add(word.slice(0, i) + c + word.slice(i));
            }
        }

        if (maxDistance > 1) {
            const newCandidates = new Set();
            for (const candidate of candidates) {
                const recursiveCandidates = this._generateCandidates(candidate, maxDistance - 1);
                for (const rc of recursiveCandidates) {
                    newCandidates.add(rc);
                }
            }
            for (const nc of newCandidates) {
                candidates.add(nc);
            }
        }

        return candidates;
    }
}

/**
 * Auto-complete system using trie
 *
 * Features:
 * - Prefix-based suggestions
 * - Frequency-based ranking
 * - Recent searches boost
 */
class AutoComplete {
    constructor() {
        this.trie = new Trie();
        this.recentSearches = [];
        this.maxRecent = 100;
    }

    /**
     * Add word to auto-complete dictionary
     * @param {string} word - The word to add
     * @param {number} frequency - Word frequency
     */
    addWord(word, frequency = 1) {
        this.trie.insert(word.toLowerCase(), frequency);
    }

    /**
     * Get auto-complete suggestions
     * @param {string} prefix - The prefix to search for
     * @returns {Array<string>} - Suggestions
     */
    search(prefix) {
        prefix = prefix.toLowerCase();
        const suggestions = this.trie.autocomplete(prefix, 10);

        // Boost recent searches
        const recentSet = new Set(this.recentSearches);
        const boosted = suggestions.map(({ word, frequency }) => ({
            word,
            frequency: frequency * (recentSet.has(word) ? 2 : 1)
        }));

        boosted.sort((a, b) => {
            if (b.frequency !== a.frequency) {
                return b.frequency - a.frequency;
            }
            return a.word.localeCompare(b.word);
        });

        return boosted.map(({ word }) => word);
    }

    /**
     * Record user search for boosting
     * @param {string} query - The search query
     */
    recordSearch(query) {
        this.recentSearches.push(query.toLowerCase());
        if (this.recentSearches.length > this.maxRecent) {
            this.recentSearches.shift();
        }
    }
}

/**
 * Dictionary implementation using trie
 *
 * Features:
 * - Fast lookup
 * - Prefix search
 * - Range queries
 */
class Dictionary {
    constructor() {
        this.trie = new PatriciaTrie();
    }

    /**
     * Add word with definition
     * @param {string} word - The word
     * @param {string} definition - The definition
     */
    add(word, definition) {
        this.trie.insert(word.toLowerCase(), definition);
    }

    /**
     * Get definition for word
     * @param {string} word - The word to lookup
     * @returns {string|null} - The definition or null
     */
    lookup(word) {
        const [node, remaining] = this.trie._findNode(word.toLowerCase());
        if (node && remaining === "" && node.isEndOfWord) {
            return node.value;
        }
        return null;
    }
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

function demonstrate() {
    console.log("=".repeat(80));
    console.log("COMPREHENSIVE TRIE DEMONSTRATIONS");
    console.log("=".repeat(80));

    // Standard Trie
    console.log("\n1. STANDARD TRIE");
    console.log("-".repeat(80));
    const trie = new Trie();

    const words = ["the", "a", "there", "answer", "any", "by", "bye", "their"];
    console.log("Inserting words:", words.join(", "));
    for (const word of words) {
        trie.insert(word);
    }

    console.log(`\nTotal words: ${trie.wordCount}`);
    console.log(`Search 'the': ${trie.search('the')}`);
    console.log(`Search 'these': ${trie.search('these')}`);
    console.log(`Starts with 'th': ${trie.startsWith('th')}`);

    const autocomplete = trie.autocomplete('th');
    console.log(`\nAuto-complete for 'th': ${autocomplete.map(x => x.word).join(", ")}`);
    console.log(`Longest common prefix: '${trie.longestCommonPrefix()}'`);
    console.log(`Words with prefix 'the': ${trie.countWordsWithPrefix('the')}`);

    // Patricia Trie
    console.log("\n2. PATRICIA TRIE (Compressed)");
    console.log("-".repeat(80));
    const ptrie = new PatriciaTrie();

    const routes = [
        ["192.168.1.0", "Router A"],
        ["192.168.2.0", "Router B"],
        ["192.168.1.1", "Host 1"],
        ["10.0.0.0", "Network B"]
    ];

    for (const [ip, dest] of routes) {
        ptrie.insert(ip, dest);
        console.log(`  Added route: ${ip} -> ${dest}`);
    }

    console.log(`\nSearch '192.168.1.0': ${ptrie.search('192.168.1.0')}`);
    console.log(`Search '192.168.1.1': ${ptrie.search('192.168.1.1')}`);

    // Suffix Trie
    console.log("\n3. SUFFIX TRIE");
    console.log("-".repeat(80));
    const text = "banana";
    const suffixTrie = new SuffixTrie(text);

    console.log(`Text: '${text}'`);
    console.log(`Contains 'ana': ${suffixTrie.containsSubstring('ana')}`);
    console.log(`Contains 'nan': ${suffixTrie.containsSubstring('nan')}`);
    console.log(`Occurrences of 'ana': [${suffixTrie.findAllOccurrences('ana').join(", ")}]`);

    // Spell Checker
    console.log("\n4. SPELL CHECKER");
    console.log("-".repeat(80));
    const dictionary = ["hello", "world", "python", "programming", "algorithm"];
    const checker = new SpellChecker(dictionary);

    const testWords = ["hello", "helo", "wrld", "python", "pyton"];
    for (const word of testWords) {
        const correct = checker.isCorrect(word);
        const suggestions = !correct ? checker.suggest(word) : [];
        console.log(`  '${word}': ${correct ? '✓' : '✗'}${suggestions.length ? ` → Suggestions: ${suggestions.slice(0, 3).join(", ")}` : ''}`);
    }

    // Auto-Complete
    console.log("\n5. AUTO-COMPLETE");
    console.log("-".repeat(80));
    const autoComplete = new AutoComplete();

    const searches = [
        ["python", 100],
        ["programming", 80],
        ["program", 60],
        ["javascript", 90],
        ["java", 95]
    ];

    for (const [word, freq] of searches) {
        autoComplete.addWord(word, freq);
    }

    console.log("Popular searches added");
    console.log(`\nSuggestions for 'pro': ${autoComplete.search('pro').join(", ")}`);
    console.log(`Suggestions for 'ja': ${autoComplete.search('ja').join(", ")}`);

    // Dictionary
    console.log("\n6. DICTIONARY");
    console.log("-".repeat(80));
    const dict = new Dictionary();

    dict.add("algorithm", "A step-by-step procedure for solving a problem");
    dict.add("data structure", "A way of organizing data");
    dict.add("trie", "A tree-like data structure for storing strings");

    console.log(`Lookup 'trie': ${dict.lookup('trie')}`);
    console.log(`Lookup 'algorithm': ${dict.lookup('algorithm')}`);

    console.log("\n" + "=".repeat(80));
    console.log("✨ All demonstrations complete!");
    console.log("=".repeat(80));
}

// Export for use in Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        Trie,
        TrieNode,
        PatriciaTrie,
        PatriciaNode,
        SuffixTrie,
        SpellChecker,
        AutoComplete,
        Dictionary,
        demonstrate
    };
}

// Run demonstration if executed directly
if (typeof require !== 'undefined' && require.main === module) {
    demonstrate();
}
