/**
 * @file string_algorithms.h
 * @brief String algorithms interface
 */

#ifndef AM_STRING_ALGORITHMS_H
#define AM_STRING_ALGORITHMS_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Pattern matching result */
typedef struct {
    size_t* positions;
    size_t count;
    size_t capacity;
} pattern_match_result_t;

/* Pattern matching algorithms */
pattern_match_result_t* string_naive_search(const char* text, const char* pattern);
pattern_match_result_t* string_kmp_search(const char* text, const char* pattern);
pattern_match_result_t* string_rabin_karp_search(const char* text, const char* pattern);
pattern_match_result_t* string_boyer_moore_search(const char* text, const char* pattern);
pattern_match_result_t* string_boyer_moore_horspool(const char* text, const char* pattern);
pattern_match_result_t* string_z_algorithm(const char* text, const char* pattern);
pattern_match_result_t* string_aho_corasick(const char* text,
                                            const char** patterns, size_t num_patterns);
void pattern_match_result_free(pattern_match_result_t* result);

/* String distance algorithms */
size_t string_levenshtein_distance(const char* s1, const char* s2);
size_t string_hamming_distance(const char* s1, const char* s2);
size_t string_damerau_levenshtein_distance(const char* s1, const char* s2);
double string_jaro_distance(const char* s1, const char* s2);
double string_jaro_winkler_distance(const char* s1, const char* s2);
size_t string_longest_common_subsequence(const char* s1, const char* s2, char** lcs);
size_t string_longest_common_substring(const char* s1, const char* s2, char** lcs);

/* Palindrome algorithms */
bool string_is_palindrome(const char* str);
char* string_longest_palindrome(const char* str);
char* string_longest_palindrome_manacher(const char* str);
size_t string_count_palindromic_substrings(const char* str);
char** string_all_palindromic_substrings(const char* str, size_t* count);

/* String transformation */
char* string_reverse(const char* str);
char* string_rotate_left(const char* str, size_t k);
char* string_rotate_right(const char* str, size_t k);
char* string_to_lower(const char* str);
char* string_to_upper(const char* str);
char* string_trim(const char* str);
char* string_replace(const char* str, const char* old_substr, const char* new_substr);
char* string_remove_duplicates(const char* str);

/* String generation */
char** string_permutations(const char* str, size_t* count);
char** string_combinations(const char* str, size_t k, size_t* count);
char** string_power_set(const char* str, size_t* count);

/* Suffix structures */
typedef struct suffix_array suffix_array_t;
typedef struct suffix_tree suffix_tree_t;

suffix_array_t* suffix_array_build(const char* text);
void suffix_array_destroy(suffix_array_t* sa);
size_t* suffix_array_get_array(const suffix_array_t* sa);
size_t* suffix_array_lcp(const suffix_array_t* sa);
pattern_match_result_t* suffix_array_search(const suffix_array_t* sa, const char* pattern);

suffix_tree_t* suffix_tree_build(const char* text);
void suffix_tree_destroy(suffix_tree_t* tree);
bool suffix_tree_contains(const suffix_tree_t* tree, const char* pattern);
size_t suffix_tree_count_occurrences(const suffix_tree_t* tree, const char* pattern);
char* suffix_tree_longest_repeated_substring(const suffix_tree_t* tree);

/* String compression */
char* string_run_length_encode(const char* str);
char* string_run_length_decode(const char* str);
char* string_huffman_encode(const char* str, uint8_t** encoded, size_t* encoded_len);
char* string_huffman_decode(const uint8_t* encoded, size_t encoded_len);
char* string_lz77_compress(const char* str, uint8_t** compressed, size_t* compressed_len);
char* string_lz77_decompress(const uint8_t* compressed, size_t compressed_len);

/* Regular expression matching */
bool string_regex_match(const char* str, const char* pattern);
bool string_wildcard_match(const char* str, const char* pattern);

/* String hashing */
uint32_t string_hash_djb2(const char* str);
uint32_t string_hash_fnv1a(const char* str);
uint64_t string_hash_murmur3(const char* str);
uint64_t string_rolling_hash(const char* str, size_t len);

/* String utilities */
char** string_split(const char* str, const char* delimiter, size_t* count);
char* string_join(const char** strings, size_t count, const char* delimiter);
bool string_starts_with(const char* str, const char* prefix);
bool string_ends_with(const char* str, const char* suffix);
size_t string_count_words(const char* str);
bool string_is_anagram(const char* s1, const char* s2);
bool string_is_rotation(const char* s1, const char* s2);

/* String parsing */
bool string_is_numeric(const char* str);
bool string_is_alpha(const char* str);
bool string_is_alphanumeric(const char* str);
bool string_is_valid_ipv4(const char* str);
bool string_is_valid_ipv6(const char* str);
bool string_is_valid_email(const char* str);

#ifdef __cplusplus
}
#endif

#endif /* AM_STRING_ALGORITHMS_H */