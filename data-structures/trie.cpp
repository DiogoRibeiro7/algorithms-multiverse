/**
 * Comprehensive Trie Data Structure Implementations in C++
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

#include <iostream>
#include <unordered_map>
#include <map>
#include <vector>
#include <string>
#include <algorithm>
#include <memory>
#include <queue>
#include <set>
#include <deque>

using namespace std;

// ============================================================================
// STANDARD TRIE
// ============================================================================

/**
 * Node in a standard trie
 */
class TrieNode {
public:
    unordered_map<char, shared_ptr<TrieNode>> children;
    bool isEndOfWord;
    int frequency; // For ranking suggestions

    TrieNode() : isEndOfWord(false), frequency(0) {}
};

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
private:
    shared_ptr<TrieNode> root;
    int wordCount;

    shared_ptr<TrieNode> findNode(const string& prefix) {
        auto node = root;

        for (char c : prefix) {
            if (node->children.find(c) == node->children.end()) {
                return nullptr;
            }
            node = node->children[c];
        }

        return node;
    }

    bool deleteHelper(shared_ptr<TrieNode> node, const string& word, size_t index) {
        if (index == word.length()) {
            if (!node->isEndOfWord) {
                return false;
            }

            node->isEndOfWord = false;
            wordCount--;
            return node->children.empty();
        }

        char c = word[index];
        if (node->children.find(c) == node->children.end()) {
            return false;
        }

        auto child = node->children[c];
        bool shouldDeleteChild = deleteHelper(child, word, index + 1);

        if (shouldDeleteChild) {
            node->children.erase(c);
            return !node->isEndOfWord && node->children.empty();
        }

        return false;
    }

    void dfsCollectWords(shared_ptr<TrieNode> node, string current,
                        vector<pair<string, int>>& suggestions) {
        if (node->isEndOfWord) {
            suggestions.push_back({current, node->frequency});
        }

        // Sort children for consistent ordering
        map<char, shared_ptr<TrieNode>> sortedChildren(
            node->children.begin(), node->children.end());

        for (const auto& [c, child] : sortedChildren) {
            dfsCollectWords(child, current + c, suggestions);
        }
    }

    void dfsCollectAllWords(shared_ptr<TrieNode> node, string current,
                           vector<string>& words) {
        if (node->isEndOfWord) {
            words.push_back(current);
        }

        for (const auto& [c, child] : node->children) {
            dfsCollectAllWords(child, current + c, words);
        }
    }

    int countWordsHelper(shared_ptr<TrieNode> node) {
        int count = node->isEndOfWord ? 1 : 0;

        for (const auto& [c, child] : node->children) {
            count += countWordsHelper(child);
        }

        return count;
    }

public:
    Trie() : root(make_shared<TrieNode>()), wordCount(0) {}

    /**
     * Insert a word into the trie. O(m)
     */
    void insert(const string& word, int frequency = 1) {
        auto node = root;

        for (char c : word) {
            if (node->children.find(c) == node->children.end()) {
                node->children[c] = make_shared<TrieNode>();
            }
            node = node->children[c];
        }

        if (!node->isEndOfWord) {
            wordCount++;
        }

        node->isEndOfWord = true;
        node->frequency = frequency;
    }

    /**
     * Search for exact word. O(m)
     */
    bool search(const string& word) {
        auto node = findNode(word);
        return node != nullptr && node->isEndOfWord;
    }

    /**
     * Check if any word starts with prefix. O(p)
     */
    bool startsWith(const string& prefix) {
        return findNode(prefix) != nullptr;
    }

    /**
     * Delete a word from trie. O(m)
     */
    bool remove(const string& word) {
        return deleteHelper(root, word, 0);
    }

    /**
     * Get word suggestions for prefix
     */
    vector<pair<string, int>> autocomplete(const string& prefix, int limit = 10) {
        auto node = findNode(prefix);
        if (!node) {
            return {};
        }

        vector<pair<string, int>> suggestions;
        dfsCollectWords(node, prefix, suggestions);

        // Sort by frequency (descending) and then alphabetically
        sort(suggestions.begin(), suggestions.end(),
             [](const auto& a, const auto& b) {
                 if (a.second != b.second) {
                     return a.second > b.second;
                 }
                 return a.first < b.first;
             });

        if (suggestions.size() > static_cast<size_t>(limit)) {
            suggestions.resize(limit);
        }

        return suggestions;
    }

    /**
     * Find longest common prefix of all words
     */
    string longestCommonPrefix() {
        if (root->children.empty()) {
            return "";
        }

        string prefix;
        auto node = root;

        while (node->children.size() == 1 && !node->isEndOfWord) {
            auto it = node->children.begin();
            prefix += it->first;
            node = it->second;
        }

        return prefix;
    }

    /**
     * Get all words in trie
     */
    vector<string> getAllWords() {
        vector<string> words;
        dfsCollectAllWords(root, "", words);
        sort(words.begin(), words.end());
        return words;
    }

    /**
     * Count how many words have given prefix
     */
    int countWordsWithPrefix(const string& prefix) {
        auto node = findNode(prefix);
        if (!node) {
            return 0;
        }

        return countWordsHelper(node);
    }

    int getWordCount() const {
        return wordCount;
    }
};

// ============================================================================
// COMPRESSED TRIE (PATRICIA TREE)
// ============================================================================

/**
 * Node in Patricia trie (compressed trie)
 */
class PatriciaNode {
public:
    string key; // Edge label (can be multiple characters)
    unordered_map<char, shared_ptr<PatriciaNode>> children;
    bool isEndOfWord;
    string value;

    PatriciaNode(const string& k = "")
        : key(k), isEndOfWord(false) {}
};

/**
 * Compressed Trie (Patricia Tree)
 *
 * More space-efficient than standard trie by compressing
 * chains of single-child nodes into single edges.
 */
class PatriciaTrie {
private:
    shared_ptr<PatriciaNode> root;

    shared_ptr<PatriciaNode> findNode(const string& word) {
        auto node = root;
        string remaining = word;

        while (!remaining.empty()) {
            char matchedChar = remaining[0];
            if (node->children.find(matchedChar) == node->children.end()) {
                return nullptr;
            }

            auto child = node->children[matchedChar];

            // Check if remaining matches child.key
            if (remaining.substr(0, child->key.length()) != child->key) {
                return nullptr;
            }

            remaining = remaining.substr(child->key.length());
            node = child;
        }

        return remaining.empty() ? node : nullptr;
    }

public:
    PatriciaTrie() : root(make_shared<PatriciaNode>()) {}

    /**
     * Insert word into Patricia trie
     */
    void insert(const string& word, const string& value = "") {
        if (word.empty()) return;

        auto node = root;
        string remaining = word;

        while (!remaining.empty()) {
            char matchedChar = remaining[0];

            if (node->children.find(matchedChar) == node->children.end()) {
                // No matching child, create new node
                auto newNode = make_shared<PatriciaNode>(remaining);
                newNode->isEndOfWord = true;
                newNode->value = value.empty() ? word : value;
                node->children[matchedChar] = newNode;
                return;
            }

            auto child = node->children[matchedChar];

            // Find common prefix between remaining and child.key
            size_t i = 0;
            while (i < remaining.length() && i < child->key.length() &&
                   remaining[i] == child->key[i]) {
                i++;
            }

            if (i == child->key.length()) {
                // Child key is prefix of remaining
                node = child;
                remaining = remaining.substr(i);
            } else {
                // Need to split the edge
                string common = child->key.substr(0, i);

                // Create new intermediate node
                auto newNode = make_shared<PatriciaNode>(common);

                // Update child key (remove common prefix)
                string oldSuffix = child->key.substr(i);
                child->key = oldSuffix;

                // Add old child to new node
                newNode->children[oldSuffix[0]] = child;

                // Add new node to parent
                node->children[matchedChar] = newNode;

                // Add new leaf if there's remaining text
                remaining = remaining.substr(i);
                if (!remaining.empty()) {
                    auto leaf = make_shared<PatriciaNode>(remaining);
                    leaf->isEndOfWord = true;
                    leaf->value = value.empty() ? word : value;
                    newNode->children[remaining[0]] = leaf;
                } else {
                    newNode->isEndOfWord = true;
                    newNode->value = value.empty() ? word : value;
                }
                return;
            }
        }

        node->isEndOfWord = true;
        node->value = value.empty() ? word : value;
    }

    /**
     * Search for exact word
     */
    bool search(const string& word) {
        auto node = findNode(word);
        return node != nullptr && node->isEndOfWord;
    }

    /**
     * Get value for word
     */
    string getValue(const string& word) {
        auto node = findNode(word);
        if (node && node->isEndOfWord) {
            return node->value;
        }
        return "";
    }
};

// ============================================================================
// SUFFIX TRIE
// ============================================================================

/**
 * Suffix Trie for pattern matching
 */
class SuffixTrie {
private:
    Trie trie;
    string text;

public:
    SuffixTrie(const string& t) : text(t) {
        // Insert all suffixes
        for (size_t i = 0; i < text.length(); i++) {
            trie.insert(text.substr(i));
        }
    }

    /**
     * Check if pattern exists as substring
     */
    bool containsSubstring(const string& pattern) {
        return trie.startsWith(pattern);
    }

    /**
     * Find all starting positions of pattern in text
     */
    vector<int> findAllOccurrences(const string& pattern) {
        vector<int> positions;

        for (size_t i = 0; i < text.length(); i++) {
            if (text.substr(i, pattern.length()) == pattern) {
                positions.push_back(i);
            }
        }

        return positions;
    }
};

// ============================================================================
// APPLICATIONS
// ============================================================================

/**
 * Spell checker using trie
 */
class SpellChecker {
private:
    Trie trie;

    set<string> generateCandidates(const string& word, int maxDistance) {
        if (maxDistance == 0) {
            return {word};
        }

        set<string> candidates;
        candidates.insert(word);
        string alphabet = "abcdefghijklmnopqrstuvwxyz";

        // Deletions
        for (size_t i = 0; i < word.length(); i++) {
            candidates.insert(word.substr(0, i) + word.substr(i + 1));
        }

        // Transpositions
        for (size_t i = 0; i < word.length() - 1; i++) {
            string transposed = word.substr(0, i) +
                              word[i + 1] + word[i] +
                              word.substr(i + 2);
            candidates.insert(transposed);
        }

        // Replacements
        for (size_t i = 0; i < word.length(); i++) {
            for (char c : alphabet) {
                candidates.insert(word.substr(0, i) + c + word.substr(i + 1));
            }
        }

        // Insertions
        for (size_t i = 0; i <= word.length(); i++) {
            for (char c : alphabet) {
                candidates.insert(word.substr(0, i) + c + word.substr(i));
            }
        }

        if (maxDistance > 1) {
            set<string> newCandidates;
            for (const auto& candidate : candidates) {
                auto recursive = generateCandidates(candidate, maxDistance - 1);
                newCandidates.insert(recursive.begin(), recursive.end());
            }
            candidates.insert(newCandidates.begin(), newCandidates.end());
        }

        return candidates;
    }

public:
    SpellChecker(const vector<string>& dictionary) {
        for (const auto& word : dictionary) {
            string lower = word;
            transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
            trie.insert(lower);
        }
    }

    /**
     * Check if word is spelled correctly
     */
    bool isCorrect(const string& word) {
        string lower = word;
        transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
        return trie.search(lower);
    }

    /**
     * Suggest corrections for misspelled word
     */
    vector<string> suggest(const string& word, int maxDistance = 2) {
        string lower = word;
        transform(lower.begin(), lower.end(), lower.begin(), ::tolower);

        if (isCorrect(lower)) {
            return {lower};
        }

        set<string> suggestions;
        auto candidates = generateCandidates(lower, maxDistance);

        for (const auto& candidate : candidates) {
            if (trie.search(candidate)) {
                suggestions.insert(candidate);
            }
        }

        vector<string> result(suggestions.begin(), suggestions.end());
        if (result.size() > 10) {
            result.resize(10);
        }

        return result;
    }
};

/**
 * Auto-complete system using trie
 */
class AutoComplete {
private:
    Trie trie;
    deque<string> recentSearches;
    static const int MAX_RECENT = 100;

public:
    /**
     * Add word to auto-complete dictionary
     */
    void addWord(const string& word, int frequency = 1) {
        string lower = word;
        transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
        trie.insert(lower, frequency);
    }

    /**
     * Get auto-complete suggestions
     */
    vector<string> search(const string& prefix) {
        string lower = prefix;
        transform(lower.begin(), lower.end(), lower.begin(), ::tolower);

        auto suggestions = trie.autocomplete(lower, 10);

        // Boost recent searches
        set<string> recentSet(recentSearches.begin(), recentSearches.end());
        vector<pair<string, int>> boosted;

        for (const auto& [word, freq] : suggestions) {
            int newFreq = freq * (recentSet.count(word) ? 2 : 1);
            boosted.push_back({word, newFreq});
        }

        sort(boosted.begin(), boosted.end(),
             [](const auto& a, const auto& b) {
                 if (a.second != b.second) {
                     return a.second > b.second;
                 }
                 return a.first < b.first;
             });

        vector<string> result;
        for (const auto& [word, freq] : boosted) {
            result.push_back(word);
        }

        return result;
    }

    /**
     * Record user search for boosting
     */
    void recordSearch(const string& query) {
        string lower = query;
        transform(lower.begin(), lower.end(), lower.begin(), ::tolower);

        recentSearches.push_back(lower);
        if (recentSearches.size() > MAX_RECENT) {
            recentSearches.pop_front();
        }
    }
};

/**
 * Dictionary implementation using trie
 */
class Dictionary {
private:
    PatriciaTrie trie;

public:
    /**
     * Add word with definition
     */
    void add(const string& word, const string& definition) {
        string lower = word;
        transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
        trie.insert(lower, definition);
    }

    /**
     * Get definition for word
     */
    string lookup(const string& word) {
        string lower = word;
        transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
        return trie.getValue(lower);
    }
};

// ============================================================================
// DEMONSTRATION
// ============================================================================

void demonstrate() {
    cout << string(80, '=') << endl;
    cout << "COMPREHENSIVE TRIE DEMONSTRATIONS" << endl;
    cout << string(80, '=') << endl;

    // Standard Trie
    cout << "\n1. STANDARD TRIE" << endl;
    cout << string(80, '-') << endl;
    Trie trie;

    vector<string> words = {"the", "a", "there", "answer", "any", "by", "bye", "their"};
    cout << "Inserting words: ";
    for (size_t i = 0; i < words.size(); i++) {
        cout << words[i];
        if (i < words.size() - 1) cout << ", ";
        trie.insert(words[i]);
    }
    cout << endl;

    cout << "\nTotal words: " << trie.getWordCount() << endl;
    cout << "Search 'the': " << (trie.search("the") ? "true" : "false") << endl;
    cout << "Search 'these': " << (trie.search("these") ? "true" : "false") << endl;
    cout << "Starts with 'th': " << (trie.startsWith("th") ? "true" : "false") << endl;

    auto autocomplete = trie.autocomplete("th");
    cout << "\nAuto-complete for 'th': ";
    for (size_t i = 0; i < autocomplete.size(); i++) {
        cout << autocomplete[i].first;
        if (i < autocomplete.size() - 1) cout << ", ";
    }
    cout << endl;
    cout << "Longest common prefix: '" << trie.longestCommonPrefix() << "'" << endl;
    cout << "Words with prefix 'the': " << trie.countWordsWithPrefix("the") << endl;

    // Patricia Trie
    cout << "\n2. PATRICIA TRIE (Compressed)" << endl;
    cout << string(80, '-') << endl;
    PatriciaTrie ptrie;

    vector<pair<string, string>> routes = {
        {"192.168.1.0", "Router A"},
        {"192.168.2.0", "Router B"},
        {"192.168.1.1", "Host 1"},
        {"10.0.0.0", "Network B"}
    };

    for (const auto& [ip, dest] : routes) {
        ptrie.insert(ip, dest);
        cout << "  Added route: " << ip << " -> " << dest << endl;
    }

    cout << "\nSearch '192.168.1.0': " << (ptrie.search("192.168.1.0") ? "true" : "false") << endl;
    cout << "Search '192.168.1.1': " << (ptrie.search("192.168.1.1") ? "true" : "false") << endl;

    // Suffix Trie
    cout << "\n3. SUFFIX TRIE" << endl;
    cout << string(80, '-') << endl;
    string text = "banana";
    SuffixTrie suffixTrie(text);

    cout << "Text: '" << text << "'" << endl;
    cout << "Contains 'ana': " << (suffixTrie.containsSubstring("ana") ? "true" : "false") << endl;
    cout << "Contains 'nan': " << (suffixTrie.containsSubstring("nan") ? "true" : "false") << endl;

    auto occurrences = suffixTrie.findAllOccurrences("ana");
    cout << "Occurrences of 'ana': [";
    for (size_t i = 0; i < occurrences.size(); i++) {
        cout << occurrences[i];
        if (i < occurrences.size() - 1) cout << ", ";
    }
    cout << "]" << endl;

    // Spell Checker
    cout << "\n4. SPELL CHECKER" << endl;
    cout << string(80, '-') << endl;
    vector<string> dictionary = {"hello", "world", "python", "programming", "algorithm"};
    SpellChecker checker(dictionary);

    vector<string> testWords = {"hello", "helo", "wrld", "python", "pyton"};
    for (const auto& word : testWords) {
        bool correct = checker.isCorrect(word);
        auto suggestions = !correct ? checker.suggest(word) : vector<string>();
        cout << "  '" << word << "': " << (correct ? "✓" : "✗");
        if (!suggestions.empty()) {
            cout << " → Suggestions: ";
            for (size_t i = 0; i < min(size_t(3), suggestions.size()); i++) {
                cout << suggestions[i];
                if (i < min(size_t(3), suggestions.size()) - 1) cout << ", ";
            }
        }
        cout << endl;
    }

    // Auto-Complete
    cout << "\n5. AUTO-COMPLETE" << endl;
    cout << string(80, '-') << endl;
    AutoComplete autoComplete;

    vector<pair<string, int>> searches = {
        {"python", 100},
        {"programming", 80},
        {"program", 60},
        {"javascript", 90},
        {"java", 95}
    };

    for (const auto& [word, freq] : searches) {
        autoComplete.addWord(word, freq);
    }

    cout << "Popular searches added" << endl;

    auto proSuggestions = autoComplete.search("pro");
    cout << "\nSuggestions for 'pro': ";
    for (size_t i = 0; i < proSuggestions.size(); i++) {
        cout << proSuggestions[i];
        if (i < proSuggestions.size() - 1) cout << ", ";
    }
    cout << endl;

    auto jaSuggestions = autoComplete.search("ja");
    cout << "Suggestions for 'ja': ";
    for (size_t i = 0; i < jaSuggestions.size(); i++) {
        cout << jaSuggestions[i];
        if (i < jaSuggestions.size() - 1) cout << ", ";
    }
    cout << endl;

    // Dictionary
    cout << "\n6. DICTIONARY" << endl;
    cout << string(80, '-') << endl;
    Dictionary dict;

    dict.add("algorithm", "A step-by-step procedure for solving a problem");
    dict.add("data structure", "A way of organizing data");
    dict.add("trie", "A tree-like data structure for storing strings");

    cout << "Lookup 'trie': " << dict.lookup("trie") << endl;
    cout << "Lookup 'algorithm': " << dict.lookup("algorithm") << endl;

    cout << "\n" << string(80, '=') << endl;
    cout << "✨ All demonstrations complete!" << endl;
    cout << string(80, '=') << endl;
}

int main() {
    demonstrate();
    return 0;
}
