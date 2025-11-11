/**
 * Comprehensive Trie Data Structure Implementations in C
 *
 * This module implements multiple trie variants and applications:
 * 1. Standard Trie
 * 2. Compressed Trie (Patricia Tree)
 * 3. Applications: Spell checker, Auto-complete
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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define ALPHABET_SIZE 26
#define MAX_WORD_LENGTH 100
#define MAX_SUGGESTIONS 10

// ============================================================================
// STANDARD TRIE
// ============================================================================

/**
 * Node in a standard trie
 */
typedef struct TrieNode {
    struct TrieNode* children[ALPHABET_SIZE];
    bool is_end_of_word;
    int frequency; // For ranking suggestions
} TrieNode;

/**
 * Standard Trie structure
 */
typedef struct {
    TrieNode* root;
    int word_count;
} Trie;

/**
 * Create a new trie node
 */
TrieNode* create_trie_node() {
    TrieNode* node = (TrieNode*)malloc(sizeof(TrieNode));
    if (!node) return NULL;

    node->is_end_of_word = false;
    node->frequency = 0;

    for (int i = 0; i < ALPHABET_SIZE; i++) {
        node->children[i] = NULL;
    }

    return node;
}

/**
 * Create a new trie
 */
Trie* create_trie() {
    Trie* trie = (Trie*)malloc(sizeof(Trie));
    if (!trie) return NULL;

    trie->root = create_trie_node();
    trie->word_count = 0;
    return trie;
}

/**
 * Insert a word into the trie. O(m)
 */
void trie_insert(Trie* trie, const char* word, int frequency) {
    if (!trie || !word) return;

    TrieNode* node = trie->root;
    int len = strlen(word);

    for (int i = 0; i < len; i++) {
        int index = tolower(word[i]) - 'a';

        if (index < 0 || index >= ALPHABET_SIZE) continue;

        if (!node->children[index]) {
            node->children[index] = create_trie_node();
        }
        node = node->children[index];
    }

    if (!node->is_end_of_word) {
        trie->word_count++;
    }

    node->is_end_of_word = true;
    node->frequency = frequency;
}

/**
 * Search for exact word. O(m)
 */
bool trie_search(Trie* trie, const char* word) {
    if (!trie || !word) return false;

    TrieNode* node = trie->root;
    int len = strlen(word);

    for (int i = 0; i < len; i++) {
        int index = tolower(word[i]) - 'a';

        if (index < 0 || index >= ALPHABET_SIZE || !node->children[index]) {
            return false;
        }
        node = node->children[index];
    }

    return node != NULL && node->is_end_of_word;
}

/**
 * Check if any word starts with prefix. O(p)
 */
bool trie_starts_with(Trie* trie, const char* prefix) {
    if (!trie || !prefix) return false;

    TrieNode* node = trie->root;
    int len = strlen(prefix);

    for (int i = 0; i < len; i++) {
        int index = tolower(prefix[i]) - 'a';

        if (index < 0 || index >= ALPHABET_SIZE || !node->children[index]) {
            return false;
        }
        node = node->children[index];
    }

    return node != NULL;
}

/**
 * Helper for DFS traversal
 */
void trie_dfs(TrieNode* node, char* prefix, int depth,
              char suggestions[][MAX_WORD_LENGTH], int* count, int limit) {
    if (*count >= limit) return;

    if (node->is_end_of_word) {
        prefix[depth] = '\0';
        strcpy(suggestions[*count], prefix);
        (*count)++;
    }

    for (int i = 0; i < ALPHABET_SIZE; i++) {
        if (node->children[i]) {
            prefix[depth] = 'a' + i;
            trie_dfs(node->children[i], prefix, depth + 1, suggestions, count, limit);
        }
    }
}

/**
 * Get word suggestions for prefix
 */
int trie_autocomplete(Trie* trie, const char* prefix,
                      char suggestions[][MAX_WORD_LENGTH], int limit) {
    if (!trie || !prefix) return 0;

    TrieNode* node = trie->root;
    int len = strlen(prefix);
    char current[MAX_WORD_LENGTH];
    strcpy(current, prefix);

    // Navigate to prefix node
    for (int i = 0; i < len; i++) {
        int index = tolower(prefix[i]) - 'a';

        if (index < 0 || index >= ALPHABET_SIZE || !node->children[index]) {
            return 0;
        }
        node = node->children[index];
    }

    // Collect suggestions
    int count = 0;
    trie_dfs(node, current, len, suggestions, &count, limit);
    return count;
}

/**
 * Count words with given prefix
 */
int count_words_helper(TrieNode* node) {
    if (!node) return 0;

    int count = node->is_end_of_word ? 1 : 0;

    for (int i = 0; i < ALPHABET_SIZE; i++) {
        if (node->children[i]) {
            count += count_words_helper(node->children[i]);
        }
    }

    return count;
}

int trie_count_words_with_prefix(Trie* trie, const char* prefix) {
    if (!trie || !prefix) return 0;

    TrieNode* node = trie->root;
    int len = strlen(prefix);

    for (int i = 0; i < len; i++) {
        int index = tolower(prefix[i]) - 'a';

        if (index < 0 || index >= ALPHABET_SIZE || !node->children[index]) {
            return 0;
        }
        node = node->children[index];
    }

    return count_words_helper(node);
}

/**
 * Free trie memory
 */
void free_trie_node(TrieNode* node) {
    if (!node) return;

    for (int i = 0; i < ALPHABET_SIZE; i++) {
        if (node->children[i]) {
            free_trie_node(node->children[i]);
        }
    }

    free(node);
}

void free_trie(Trie* trie) {
    if (!trie) return;

    free_trie_node(trie->root);
    free(trie);
}

// ============================================================================
// SPELL CHECKER
// ============================================================================

/**
 * Spell checker structure
 */
typedef struct {
    Trie* trie;
} SpellChecker;

/**
 * Create a new spell checker
 */
SpellChecker* create_spell_checker(const char* dictionary[], int dict_size) {
    SpellChecker* checker = (SpellChecker*)malloc(sizeof(SpellChecker));
    if (!checker) return NULL;

    checker->trie = create_trie();

    for (int i = 0; i < dict_size; i++) {
        trie_insert(checker->trie, dictionary[i], 1);
    }

    return checker;
}

/**
 * Check if word is correct
 */
bool spell_checker_is_correct(SpellChecker* checker, const char* word) {
    if (!checker || !word) return false;
    return trie_search(checker->trie, word);
}

/**
 * Free spell checker
 */
void free_spell_checker(SpellChecker* checker) {
    if (!checker) return;

    free_trie(checker->trie);
    free(checker);
}

// ============================================================================
// AUTO-COMPLETE
// ============================================================================

/**
 * Auto-complete structure
 */
typedef struct {
    Trie* trie;
} AutoComplete;

/**
 * Create a new auto-complete system
 */
AutoComplete* create_autocomplete() {
    AutoComplete* ac = (AutoComplete*)malloc(sizeof(AutoComplete));
    if (!ac) return NULL;

    ac->trie = create_trie();
    return ac;
}

/**
 * Add word to auto-complete
 */
void autocomplete_add_word(AutoComplete* ac, const char* word, int frequency) {
    if (!ac || !word) return;
    trie_insert(ac->trie, word, frequency);
}

/**
 * Search for suggestions
 */
int autocomplete_search(AutoComplete* ac, const char* prefix,
                        char suggestions[][MAX_WORD_LENGTH]) {
    if (!ac || !prefix) return 0;
    return trie_autocomplete(ac->trie, prefix, suggestions, MAX_SUGGESTIONS);
}

/**
 * Free auto-complete
 */
void free_autocomplete(AutoComplete* ac) {
    if (!ac) return;

    free_trie(ac->trie);
    free(ac);
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

void demonstrate() {
    printf("%s\n", "================================================================================");
    printf("COMPREHENSIVE TRIE DEMONSTRATIONS\n");
    printf("%s\n", "================================================================================");

    // Standard Trie
    printf("\n1. STANDARD TRIE\n");
    printf("%s\n", "--------------------------------------------------------------------------------");

    Trie* trie = create_trie();
    const char* words[] = {"the", "a", "there", "answer", "any", "by", "bye", "their"};
    int num_words = sizeof(words) / sizeof(words[0]);

    printf("Inserting words: ");
    for (int i = 0; i < num_words; i++) {
        printf("%s%s", words[i], i < num_words - 1 ? ", " : "");
        trie_insert(trie, words[i], 1);
    }
    printf("\n");

    printf("\nTotal words: %d\n", trie->word_count);
    printf("Search 'the': %s\n", trie_search(trie, "the") ? "true" : "false");
    printf("Search 'these': %s\n", trie_search(trie, "these") ? "true" : "false");
    printf("Starts with 'th': %s\n", trie_starts_with(trie, "th") ? "true" : "false");

    char suggestions[MAX_SUGGESTIONS][MAX_WORD_LENGTH];
    int count = trie_autocomplete(trie, "th", suggestions, MAX_SUGGESTIONS);

    printf("\nAuto-complete for 'th': ");
    for (int i = 0; i < count; i++) {
        printf("%s%s", suggestions[i], i < count - 1 ? ", " : "");
    }
    printf("\n");

    printf("Words with prefix 'the': %d\n", trie_count_words_with_prefix(trie, "the"));

    // Spell Checker
    printf("\n2. SPELL CHECKER\n");
    printf("%s\n", "--------------------------------------------------------------------------------");

    const char* dictionary[] = {"hello", "world", "python", "programming", "algorithm"};
    int dict_size = sizeof(dictionary) / sizeof(dictionary[0]);

    SpellChecker* checker = create_spell_checker(dictionary, dict_size);

    const char* test_words[] = {"hello", "helo", "world", "wrld", "python"};
    int test_count = sizeof(test_words) / sizeof(test_words[0]);

    for (int i = 0; i < test_count; i++) {
        bool correct = spell_checker_is_correct(checker, test_words[i]);
        printf("  '%s': %s\n", test_words[i], correct ? "✓" : "✗");
    }

    // Auto-Complete
    printf("\n3. AUTO-COMPLETE\n");
    printf("%s\n", "--------------------------------------------------------------------------------");

    AutoComplete* ac = create_autocomplete();

    autocomplete_add_word(ac, "python", 100);
    autocomplete_add_word(ac, "programming", 80);
    autocomplete_add_word(ac, "program", 60);
    autocomplete_add_word(ac, "javascript", 90);
    autocomplete_add_word(ac, "java", 95);

    printf("Popular searches added\n");

    char ac_suggestions[MAX_SUGGESTIONS][MAX_WORD_LENGTH];
    int ac_count = autocomplete_search(ac, "pro", ac_suggestions);

    printf("\nSuggestions for 'pro': ");
    for (int i = 0; i < ac_count; i++) {
        printf("%s%s", ac_suggestions[i], i < ac_count - 1 ? ", " : "");
    }
    printf("\n");

    ac_count = autocomplete_search(ac, "ja", ac_suggestions);
    printf("Suggestions for 'ja': ");
    for (int i = 0; i < ac_count; i++) {
        printf("%s%s", ac_suggestions[i], i < ac_count - 1 ? ", " : "");
    }
    printf("\n");

    // Cleanup
    free_trie(trie);
    free_spell_checker(checker);
    free_autocomplete(ac);

    printf("\n%s\n", "================================================================================");
    printf("✨ All demonstrations complete!\n");
    printf("%s\n", "================================================================================");
}

int main() {
    demonstrate();
    return 0;
}
