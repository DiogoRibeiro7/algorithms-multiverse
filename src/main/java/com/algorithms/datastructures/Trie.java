package com.algorithms.datastructures;

/**
 * Comprehensive Trie Data Structure Implementations in Java
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

import java.util.*;
import java.util.stream.*;

// ============================================================================
// STANDARD TRIE
// ============================================================================

/**
 * Node in a standard trie
 */
class TrieNode {
    Map<Character, TrieNode> children;
    boolean isEndOfWord;
    int frequency; // For ranking suggestions

    public TrieNode() {
        this.children = new HashMap<>();
        this.isEndOfWord = false;
        this.frequency = 0;
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
    private TrieNode root;
    private int wordCount;

    public Trie() {
        this.root = new TrieNode();
        this.wordCount = 0;
    }

    /**
     * Insert a word into the trie. O(m)
     * @param word The word to insert
     * @param frequency Frequency/weight of the word
     */
    public void insert(String word, int frequency) {
        TrieNode node = root;

        for (char c : word.toCharArray()) {
            node.children.putIfAbsent(c, new TrieNode());
            node = node.children.get(c);
        }

        if (!node.isEndOfWord) {
            wordCount++;
        }

        node.isEndOfWord = true;
        node.frequency = frequency;
    }

    public void insert(String word) {
        insert(word, 1);
    }

    /**
     * Search for exact word. O(m)
     * @param word The word to search for
     * @return True if word exists
     */
    public boolean search(String word) {
        TrieNode node = findNode(word);
        return node != null && node.isEndOfWord;
    }

    /**
     * Check if any word starts with prefix. O(p)
     * @param prefix The prefix to check
     * @return True if prefix exists
     */
    public boolean startsWith(String prefix) {
        return findNode(prefix) != null;
    }

    /**
     * Helper to find node for given prefix
     * @param prefix The prefix to find
     * @return The node or null
     */
    private TrieNode findNode(String prefix) {
        TrieNode node = root;

        for (char c : prefix.toCharArray()) {
            if (!node.children.containsKey(c)) {
                return null;
            }
            node = node.children.get(c);
        }

        return node;
    }

    /**
     * Delete a word from trie. O(m)
     * @param word The word to delete
     * @return True if word was deleted
     */
    public boolean delete(String word) {
        return deleteHelper(root, word, 0);
    }

    private boolean deleteHelper(TrieNode node, String word, int index) {
        if (index == word.length()) {
            if (!node.isEndOfWord) {
                return false;
            }

            node.isEndOfWord = false;
            wordCount--;
            return node.children.isEmpty();
        }

        char c = word.charAt(index);
        if (!node.children.containsKey(c)) {
            return false;
        }

        TrieNode child = node.children.get(c);
        boolean shouldDeleteChild = deleteHelper(child, word, index + 1);

        if (shouldDeleteChild) {
            node.children.remove(c);
            return !node.isEndOfWord && node.children.isEmpty();
        }

        return false;
    }

    /**
     * Suggestion class for autocomplete
     */
    public static class Suggestion implements Comparable<Suggestion> {
        String word;
        int frequency;

        public Suggestion(String word, int frequency) {
            this.word = word;
            this.frequency = frequency;
        }

        @Override
        public int compareTo(Suggestion other) {
            if (this.frequency != other.frequency) {
                return Integer.compare(other.frequency, this.frequency);
            }
            return this.word.compareTo(other.word);
        }
    }

    /**
     * Get word suggestions for prefix
     * @param prefix The prefix to search for
     * @param limit Maximum number of suggestions
     * @return List of suggestions
     */
    public List<Suggestion> autocomplete(String prefix, int limit) {
        TrieNode node = findNode(prefix);
        if (node == null) {
            return new ArrayList<>();
        }

        List<Suggestion> suggestions = new ArrayList<>();
        dfsCollectWords(node, new StringBuilder(prefix), suggestions);

        Collections.sort(suggestions);
        return suggestions.stream()
                .limit(limit)
                .collect(Collectors.toList());
    }

    private void dfsCollectWords(TrieNode node, StringBuilder current, List<Suggestion> suggestions) {
        if (node.isEndOfWord) {
            suggestions.add(new Suggestion(current.toString(), node.frequency));
        }

        // Sort children for consistent ordering
        List<Character> sortedKeys = new ArrayList<>(node.children.keySet());
        Collections.sort(sortedKeys);

        for (char c : sortedKeys) {
            current.append(c);
            dfsCollectWords(node.children.get(c), current, suggestions);
            current.deleteCharAt(current.length() - 1);
        }
    }

    /**
     * Find longest common prefix of all words
     * @return The longest common prefix
     */
    public String longestCommonPrefix() {
        if (root.children.isEmpty()) {
            return "";
        }

        StringBuilder prefix = new StringBuilder();
        TrieNode node = root;

        while (node.children.size() == 1 && !node.isEndOfWord) {
            Map.Entry<Character, TrieNode> entry = node.children.entrySet().iterator().next();
            prefix.append(entry.getKey());
            node = entry.getValue();
        }

        return prefix.toString();
    }

    /**
     * Get all words in trie
     * @return All words sorted
     */
    public List<String> getAllWords() {
        List<String> words = new ArrayList<>();
        dfsCollectAllWords(root, new StringBuilder(), words);
        Collections.sort(words);
        return words;
    }

    private void dfsCollectAllWords(TrieNode node, StringBuilder current, List<String> words) {
        if (node.isEndOfWord) {
            words.add(current.toString());
        }

        for (Map.Entry<Character, TrieNode> entry : node.children.entrySet()) {
            current.append(entry.getKey());
            dfsCollectAllWords(entry.getValue(), current, words);
            current.deleteCharAt(current.length() - 1);
        }
    }

    /**
     * Count how many words have given prefix
     * @param prefix The prefix to count
     * @return Number of words with prefix
     */
    public int countWordsWithPrefix(String prefix) {
        TrieNode node = findNode(prefix);
        if (node == null) {
            return 0;
        }

        return countWordsHelper(node);
    }

    private int countWordsHelper(TrieNode node) {
        int count = node.isEndOfWord ? 1 : 0;

        for (TrieNode child : node.children.values()) {
            count += countWordsHelper(child);
        }

        return count;
    }

    public int getWordCount() {
        return wordCount;
    }
}

// ============================================================================
// COMPRESSED TRIE (PATRICIA TREE)
// ============================================================================

/**
 * Node in Patricia trie (compressed trie)
 */
class PatriciaNode {
    String key; // Edge label (can be multiple characters)
    Map<Character, PatriciaNode> children;
    boolean isEndOfWord;
    String value;

    public PatriciaNode(String key) {
        this.key = key;
        this.children = new HashMap<>();
        this.isEndOfWord = false;
        this.value = null;
    }

    public PatriciaNode() {
        this("");
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
    private PatriciaNode root;

    public PatriciaTrie() {
        this.root = new PatriciaNode();
    }

    /**
     * Insert word into Patricia trie
     * @param word The word to insert
     * @param value Associated value
     */
    public void insert(String word, String value) {
        if (word == null || word.isEmpty()) return;

        PatriciaNode node = root;
        String remaining = word;

        while (!remaining.isEmpty()) {
            char matchedChar = remaining.charAt(0);

            if (!node.children.containsKey(matchedChar)) {
                // No matching child, create new node
                PatriciaNode newNode = new PatriciaNode(remaining);
                newNode.isEndOfWord = true;
                newNode.value = value != null ? value : word;
                node.children.put(matchedChar, newNode);
                return;
            }

            PatriciaNode child = node.children.get(matchedChar);

            // Find common prefix between remaining and child.key
            int i = 0;
            while (i < remaining.length() && i < child.key.length() &&
                   remaining.charAt(i) == child.key.charAt(i)) {
                i++;
            }

            if (i == child.key.length()) {
                // Child key is prefix of remaining
                node = child;
                remaining = remaining.substring(i);
            } else {
                // Need to split the edge
                String common = child.key.substring(0, i);

                // Create new intermediate node
                PatriciaNode newNode = new PatriciaNode(common);

                // Update child key (remove common prefix)
                String oldSuffix = child.key.substring(i);
                child.key = oldSuffix;

                // Add old child to new node
                newNode.children.put(oldSuffix.charAt(0), child);

                // Add new node to parent
                node.children.put(matchedChar, newNode);

                // Add new leaf if there's remaining text
                remaining = remaining.substring(i);
                if (!remaining.isEmpty()) {
                    PatriciaNode leaf = new PatriciaNode(remaining);
                    leaf.isEndOfWord = true;
                    leaf.value = value != null ? value : word;
                    newNode.children.put(remaining.charAt(0), leaf);
                } else {
                    newNode.isEndOfWord = true;
                    newNode.value = value != null ? value : word;
                }
                return;
            }
        }

        node.isEndOfWord = true;
        node.value = value != null ? value : word;
    }

    public void insert(String word) {
        insert(word, null);
    }

    /**
     * Search for exact word
     * @param word The word to search for
     * @return True if word exists
     */
    public boolean search(String word) {
        PatriciaNode node = findNode(word);
        return node != null && node.isEndOfWord;
    }

    /**
     * Find node for given word
     * @param word The word to find
     * @return The node or null
     */
    private PatriciaNode findNode(String word) {
        PatriciaNode node = root;
        String remaining = word;

        while (!remaining.isEmpty()) {
            char matchedChar = remaining.charAt(0);
            if (!node.children.containsKey(matchedChar)) {
                return null;
            }

            PatriciaNode child = node.children.get(matchedChar);

            // Check if remaining matches child.key
            if (!remaining.startsWith(child.key)) {
                return null;
            }

            remaining = remaining.substring(child.key.length());
            node = child;
        }

        return remaining.isEmpty() ? node : null;
    }

    /**
     * Get value for word
     * @param word The word to lookup
     * @return The value or null
     */
    public String getValue(String word) {
        PatriciaNode node = findNode(word);
        if (node != null && node.isEndOfWord) {
            return node.value;
        }
        return null;
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
    private Trie trie;
    private String text;

    public SuffixTrie(String text) {
        this.trie = new Trie();
        this.text = text;

        // Insert all suffixes
        for (int i = 0; i < text.length(); i++) {
            trie.insert(text.substring(i));
        }
    }

    /**
     * Check if pattern exists as substring
     * @param pattern The pattern to search for
     * @return True if pattern exists
     */
    public boolean containsSubstring(String pattern) {
        return trie.startsWith(pattern);
    }

    /**
     * Find all starting positions of pattern in text
     * @param pattern The pattern to find
     * @return List of starting positions
     */
    public List<Integer> findAllOccurrences(String pattern) {
        List<Integer> positions = new ArrayList<>();

        for (int i = 0; i < text.length(); i++) {
            if (text.substring(i).startsWith(pattern)) {
                positions.add(i);
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
    private Trie trie;

    public SpellChecker(List<String> dictionary) {
        this.trie = new Trie();
        for (String word : dictionary) {
            trie.insert(word.toLowerCase());
        }
    }

    /**
     * Check if word is spelled correctly
     * @param word The word to check
     * @return True if correct
     */
    public boolean isCorrect(String word) {
        return trie.search(word.toLowerCase());
    }

    /**
     * Suggest corrections for misspelled word
     * @param word The word to correct
     * @param maxDistance Maximum edit distance
     * @return List of suggestions
     */
    public List<String> suggest(String word, int maxDistance) {
        word = word.toLowerCase();

        if (isCorrect(word)) {
            return Arrays.asList(word);
        }

        Set<String> suggestions = new HashSet<>();
        Set<String> candidates = generateCandidates(word, maxDistance);

        for (String candidate : candidates) {
            if (trie.search(candidate)) {
                suggestions.add(candidate);
            }
        }

        List<String> result = new ArrayList<>(suggestions);
        Collections.sort(result);
        return result.stream().limit(10).collect(Collectors.toList());
    }

    public List<String> suggest(String word) {
        return suggest(word, 2);
    }

    /**
     * Generate candidate words within edit distance
     * @param word The word
     * @param maxDistance Maximum distance
     * @return Set of candidates
     */
    private Set<String> generateCandidates(String word, int maxDistance) {
        if (maxDistance == 0) {
            return new HashSet<>(Arrays.asList(word));
        }

        Set<String> candidates = new HashSet<>();
        candidates.add(word);
        String alphabet = "abcdefghijklmnopqrstuvwxyz";

        // Deletions
        for (int i = 0; i < word.length(); i++) {
            candidates.add(word.substring(0, i) + word.substring(i + 1));
        }

        // Transpositions
        for (int i = 0; i < word.length() - 1; i++) {
            candidates.add(word.substring(0, i) + word.charAt(i + 1) +
                          word.charAt(i) + word.substring(i + 2));
        }

        // Replacements
        for (int i = 0; i < word.length(); i++) {
            for (char c : alphabet.toCharArray()) {
                candidates.add(word.substring(0, i) + c + word.substring(i + 1));
            }
        }

        // Insertions
        for (int i = 0; i <= word.length(); i++) {
            for (char c : alphabet.toCharArray()) {
                candidates.add(word.substring(0, i) + c + word.substring(i));
            }
        }

        if (maxDistance > 1) {
            Set<String> newCandidates = new HashSet<>();
            for (String candidate : candidates) {
                newCandidates.addAll(generateCandidates(candidate, maxDistance - 1));
            }
            candidates.addAll(newCandidates);
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
    private Trie trie;
    private Deque<String> recentSearches;
    private static final int MAX_RECENT = 100;

    public AutoComplete() {
        this.trie = new Trie();
        this.recentSearches = new ArrayDeque<>();
    }

    /**
     * Add word to auto-complete dictionary
     * @param word The word to add
     * @param frequency Word frequency
     */
    public void addWord(String word, int frequency) {
        trie.insert(word.toLowerCase(), frequency);
    }

    public void addWord(String word) {
        addWord(word, 1);
    }

    /**
     * Get auto-complete suggestions
     * @param prefix The prefix to search for
     * @return List of suggestions
     */
    public List<String> search(String prefix) {
        prefix = prefix.toLowerCase();
        List<Trie.Suggestion> suggestions = trie.autocomplete(prefix, 10);

        // Boost recent searches
        Set<String> recentSet = new HashSet<>(recentSearches);
        List<Trie.Suggestion> boosted = new ArrayList<>();

        for (Trie.Suggestion s : suggestions) {
            int freq = s.frequency * (recentSet.contains(s.word) ? 2 : 1);
            boosted.add(new Trie.Suggestion(s.word, freq));
        }

        Collections.sort(boosted);
        return boosted.stream()
                .map(s -> s.word)
                .collect(Collectors.toList());
    }

    /**
     * Record user search for boosting
     * @param query The search query
     */
    public void recordSearch(String query) {
        recentSearches.addLast(query.toLowerCase());
        if (recentSearches.size() > MAX_RECENT) {
            recentSearches.removeFirst();
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
    private PatriciaTrie trie;

    public Dictionary() {
        this.trie = new PatriciaTrie();
    }

    /**
     * Add word with definition
     * @param word The word
     * @param definition The definition
     */
    public void add(String word, String definition) {
        trie.insert(word.toLowerCase(), definition);
    }

    /**
     * Get definition for word
     * @param word The word to lookup
     * @return The definition or null
     */
    public String lookup(String word) {
        return trie.getValue(word.toLowerCase());
    }
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

class TrieDemo {
    public static void main(String[] args) {
        System.out.println("=".repeat(80));
        System.out.println("COMPREHENSIVE TRIE DEMONSTRATIONS");
        System.out.println("=".repeat(80));

        // Standard Trie
        System.out.println("\n1. STANDARD TRIE");
        System.out.println("-".repeat(80));
        Trie trie = new Trie();

        String[] words = {"the", "a", "there", "answer", "any", "by", "bye", "their"};
        System.out.println("Inserting words: " + String.join(", ", words));
        for (String word : words) {
            trie.insert(word);
        }

        System.out.println("\nTotal words: " + trie.getWordCount());
        System.out.println("Search 'the': " + trie.search("the"));
        System.out.println("Search 'these': " + trie.search("these"));
        System.out.println("Starts with 'th': " + trie.startsWith("th"));

        List<Trie.Suggestion> autocomplete = trie.autocomplete("th", 10);
        String autocompleteWords = autocomplete.stream()
                .map(s -> s.word)
                .collect(Collectors.joining(", "));
        System.out.println("\nAuto-complete for 'th': " + autocompleteWords);
        System.out.println("Longest common prefix: '" + trie.longestCommonPrefix() + "'");
        System.out.println("Words with prefix 'the': " + trie.countWordsWithPrefix("the"));

        // Patricia Trie
        System.out.println("\n2. PATRICIA TRIE (Compressed)");
        System.out.println("-".repeat(80));
        PatriciaTrie ptrie = new PatriciaTrie();

        String[][] routes = {
            {"192.168.1.0", "Router A"},
            {"192.168.2.0", "Router B"},
            {"192.168.1.1", "Host 1"},
            {"10.0.0.0", "Network B"}
        };

        for (String[] route : routes) {
            ptrie.insert(route[0], route[1]);
            System.out.println("  Added route: " + route[0] + " -> " + route[1]);
        }

        System.out.println("\nSearch '192.168.1.0': " + ptrie.search("192.168.1.0"));
        System.out.println("Search '192.168.1.1': " + ptrie.search("192.168.1.1"));

        // Suffix Trie
        System.out.println("\n3. SUFFIX TRIE");
        System.out.println("-".repeat(80));
        String text = "banana";
        SuffixTrie suffixTrie = new SuffixTrie(text);

        System.out.println("Text: '" + text + "'");
        System.out.println("Contains 'ana': " + suffixTrie.containsSubstring("ana"));
        System.out.println("Contains 'nan': " + suffixTrie.containsSubstring("nan"));
        System.out.println("Occurrences of 'ana': " + suffixTrie.findAllOccurrences("ana"));

        // Spell Checker
        System.out.println("\n4. SPELL CHECKER");
        System.out.println("-".repeat(80));
        List<String> dictionary = Arrays.asList("hello", "world", "python", "programming", "algorithm");
        SpellChecker checker = new SpellChecker(dictionary);

        String[] testWords = {"hello", "helo", "wrld", "python", "pyton"};
        for (String word : testWords) {
            boolean correct = checker.isCorrect(word);
            List<String> suggestions = !correct ? checker.suggest(word) : new ArrayList<>();
            System.out.print("  '" + word + "': " + (correct ? "✓" : "✗"));
            if (!suggestions.isEmpty()) {
                System.out.print(" → Suggestions: " +
                    suggestions.stream().limit(3).collect(Collectors.joining(", ")));
            }
            System.out.println();
        }

        // Auto-Complete
        System.out.println("\n5. AUTO-COMPLETE");
        System.out.println("-".repeat(80));
        AutoComplete autoComplete = new AutoComplete();

        Object[][] searches = {
            {"python", 100},
            {"programming", 80},
            {"program", 60},
            {"javascript", 90},
            {"java", 95}
        };

        for (Object[] search : searches) {
            autoComplete.addWord((String) search[0], (Integer) search[1]);
        }

        System.out.println("Popular searches added");
        System.out.println("\nSuggestions for 'pro': " + String.join(", ", autoComplete.search("pro")));
        System.out.println("Suggestions for 'ja': " + String.join(", ", autoComplete.search("ja")));

        // Dictionary
        System.out.println("\n6. DICTIONARY");
        System.out.println("-".repeat(80));
        Dictionary dict = new Dictionary();

        dict.add("algorithm", "A step-by-step procedure for solving a problem");
        dict.add("data structure", "A way of organizing data");
        dict.add("trie", "A tree-like data structure for storing strings");

        System.out.println("Lookup 'trie': " + dict.lookup("trie"));
        System.out.println("Lookup 'algorithm': " + dict.lookup("algorithm"));

        System.out.println("\n" + "=".repeat(80));
        System.out.println("✨ All demonstrations complete!");
        System.out.println("=".repeat(80));
    }
}

