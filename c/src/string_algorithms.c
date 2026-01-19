/**
 * @file string_algorithms.c
 * @brief Implementation of string algorithms
 */

#include "string_algorithms.h"
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

/* Pattern matching result functions */
static pattern_match_result_t* create_result(size_t initial_capacity) {
    pattern_match_result_t* result = malloc(sizeof(pattern_match_result_t));
    if (!result) return NULL;

    result->positions = malloc(initial_capacity * sizeof(size_t));
    if (!result->positions) {
        free(result);
        return NULL;
    }

    result->count = 0;
    result->capacity = initial_capacity;
    return result;
}

static bool add_match(pattern_match_result_t* result, size_t position) {
    if (result->count >= result->capacity) {
        size_t new_capacity = result->capacity * 2;
        size_t* new_positions = realloc(result->positions,
                                        new_capacity * sizeof(size_t));
        if (!new_positions) return false;

        result->positions = new_positions;
        result->capacity = new_capacity;
    }

    result->positions[result->count++] = position;
    return true;
}

void pattern_match_result_free(pattern_match_result_t* result) {
    if (result) {
        free(result->positions);
        free(result);
    }
}

/* Naive pattern matching */
pattern_match_result_t* string_naive_search(const char* text, const char* pattern) {
    if (!text || !pattern) return NULL;

    size_t text_len = strlen(text);
    size_t pattern_len = strlen(pattern);

    if (pattern_len > text_len) return create_result(0);

    pattern_match_result_t* result = create_result(10);
    if (!result) return NULL;

    for (size_t i = 0; i <= text_len - pattern_len; i++) {
        size_t j = 0;
        while (j < pattern_len && text[i + j] == pattern[j]) {
            j++;
        }

        if (j == pattern_len) {
            add_match(result, i);
        }
    }

    return result;
}

/* KMP (Knuth-Morris-Pratt) pattern matching */
static size_t* compute_lps_array(const char* pattern, size_t pattern_len) {
    size_t* lps = calloc(pattern_len, sizeof(size_t));
    if (!lps) return NULL;

    size_t len = 0;
    size_t i = 1;

    while (i < pattern_len) {
        if (pattern[i] == pattern[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }

    return lps;
}

pattern_match_result_t* string_kmp_search(const char* text, const char* pattern) {
    if (!text || !pattern) return NULL;

    size_t text_len = strlen(text);
    size_t pattern_len = strlen(pattern);

    if (pattern_len > text_len) return create_result(0);

    size_t* lps = compute_lps_array(pattern, pattern_len);
    if (!lps) return NULL;

    pattern_match_result_t* result = create_result(10);
    if (!result) {
        free(lps);
        return NULL;
    }

    size_t i = 0;  /* index for text */
    size_t j = 0;  /* index for pattern */

    while (i < text_len) {
        if (pattern[j] == text[i]) {
            i++;
            j++;
        }

        if (j == pattern_len) {
            add_match(result, i - j);
            j = lps[j - 1];
        } else if (i < text_len && pattern[j] != text[i]) {
            if (j != 0) {
                j = lps[j - 1];
            } else {
                i++;
            }
        }
    }

    free(lps);
    return result;
}

/* Rabin-Karp pattern matching */
pattern_match_result_t* string_rabin_karp_search(const char* text, const char* pattern) {
    if (!text || !pattern) return NULL;

    size_t text_len = strlen(text);
    size_t pattern_len = strlen(pattern);

    if (pattern_len > text_len) return create_result(0);

    const int PRIME = 101;
    const int BASE = 256;

    pattern_match_result_t* result = create_result(10);
    if (!result) return NULL;

    /* Calculate hash value of pattern and first window */
    int pattern_hash = 0;
    int text_hash = 0;
    int h = 1;

    /* Calculate h = BASE^(pattern_len - 1) % PRIME */
    for (size_t i = 0; i < pattern_len - 1; i++) {
        h = (h * BASE) % PRIME;
    }

    /* Calculate initial hash values */
    for (size_t i = 0; i < pattern_len; i++) {
        pattern_hash = (BASE * pattern_hash + pattern[i]) % PRIME;
        text_hash = (BASE * text_hash + text[i]) % PRIME;
    }

    /* Slide pattern over text */
    for (size_t i = 0; i <= text_len - pattern_len; i++) {
        /* Check if hash values match */
        if (pattern_hash == text_hash) {
            /* Verify character by character */
            size_t j = 0;
            while (j < pattern_len && text[i + j] == pattern[j]) {
                j++;
            }

            if (j == pattern_len) {
                add_match(result, i);
            }
        }

        /* Calculate hash for next window */
        if (i < text_len - pattern_len) {
            text_hash = (BASE * (text_hash - text[i] * h) + text[i + pattern_len]) % PRIME;

            if (text_hash < 0) {
                text_hash += PRIME;
            }
        }
    }

    return result;
}

/* Boyer-Moore pattern matching */
static void compute_bad_char_table(const char* pattern, size_t pattern_len,
                                   int bad_char[256]) {
    for (int i = 0; i < 256; i++) {
        bad_char[i] = -1;
    }

    for (size_t i = 0; i < pattern_len; i++) {
        bad_char[(unsigned char)pattern[i]] = i;
    }
}

pattern_match_result_t* string_boyer_moore_search(const char* text, const char* pattern) {
    if (!text || !pattern) return NULL;

    size_t text_len = strlen(text);
    size_t pattern_len = strlen(pattern);

    if (pattern_len > text_len) return create_result(0);

    pattern_match_result_t* result = create_result(10);
    if (!result) return NULL;

    int bad_char[256];
    compute_bad_char_table(pattern, pattern_len, bad_char);

    size_t shift = 0;

    while (shift <= text_len - pattern_len) {
        int j = pattern_len - 1;

        while (j >= 0 && pattern[j] == text[shift + j]) {
            j--;
        }

        if (j < 0) {
            add_match(result, shift);
            shift += (shift + pattern_len < text_len) ?
                     pattern_len - bad_char[(unsigned char)text[shift + pattern_len]] : 1;
        } else {
            int bc_shift = bad_char[(unsigned char)text[shift + j]];
            shift += (j - bc_shift > 1) ? j - bc_shift : 1;
        }
    }

    return result;
}

/* String distance algorithms */

/* Levenshtein distance (edit distance) */
size_t string_levenshtein_distance(const char* s1, const char* s2) {
    if (!s1 || !s2) return 0;

    size_t len1 = strlen(s1);
    size_t len2 = strlen(s2);

    if (len1 == 0) return len2;
    if (len2 == 0) return len1;

    /* Create DP table */
    size_t** dp = malloc((len1 + 1) * sizeof(size_t*));
    for (size_t i = 0; i <= len1; i++) {
        dp[i] = malloc((len2 + 1) * sizeof(size_t));
    }

    /* Initialize first row and column */
    for (size_t i = 0; i <= len1; i++) {
        dp[i][0] = i;
    }
    for (size_t j = 0; j <= len2; j++) {
        dp[0][j] = j;
    }

    /* Fill the DP table */
    for (size_t i = 1; i <= len1; i++) {
        for (size_t j = 1; j <= len2; j++) {
            size_t cost = (s1[i - 1] == s2[j - 1]) ? 0 : 1;

            size_t deletion = dp[i - 1][j] + 1;
            size_t insertion = dp[i][j - 1] + 1;
            size_t substitution = dp[i - 1][j - 1] + cost;

            dp[i][j] = deletion < insertion ? deletion : insertion;
            if (substitution < dp[i][j]) {
                dp[i][j] = substitution;
            }
        }
    }

    size_t distance = dp[len1][len2];

    /* Free memory */
    for (size_t i = 0; i <= len1; i++) {
        free(dp[i]);
    }
    free(dp);

    return distance;
}

/* Hamming distance */
size_t string_hamming_distance(const char* s1, const char* s2) {
    if (!s1 || !s2) return 0;

    size_t len1 = strlen(s1);
    size_t len2 = strlen(s2);

    if (len1 != len2) return SIZE_MAX;  /* Undefined for different lengths */

    size_t distance = 0;
    for (size_t i = 0; i < len1; i++) {
        if (s1[i] != s2[i]) {
            distance++;
        }
    }

    return distance;
}

/* Longest common subsequence */
size_t string_longest_common_subsequence(const char* s1, const char* s2, char** lcs) {
    if (!s1 || !s2) return 0;

    size_t len1 = strlen(s1);
    size_t len2 = strlen(s2);

    /* Create DP table */
    size_t** dp = malloc((len1 + 1) * sizeof(size_t*));
    for (size_t i = 0; i <= len1; i++) {
        dp[i] = calloc(len2 + 1, sizeof(size_t));
    }

    /* Fill DP table */
    for (size_t i = 1; i <= len1; i++) {
        for (size_t j = 1; j <= len2; j++) {
            if (s1[i - 1] == s2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = (dp[i - 1][j] > dp[i][j - 1]) ?
                           dp[i - 1][j] : dp[i][j - 1];
            }
        }
    }

    size_t lcs_len = dp[len1][len2];

    /* Reconstruct LCS if requested */
    if (lcs && lcs_len > 0) {
        *lcs = malloc(lcs_len + 1);
        (*lcs)[lcs_len] = '\0';

        size_t i = len1, j = len2, k = lcs_len;

        while (i > 0 && j > 0) {
            if (s1[i - 1] == s2[j - 1]) {
                (*lcs)[--k] = s1[i - 1];
                i--;
                j--;
            } else if (dp[i - 1][j] > dp[i][j - 1]) {
                i--;
            } else {
                j--;
            }
        }
    }

    /* Free DP table */
    for (size_t i = 0; i <= len1; i++) {
        free(dp[i]);
    }
    free(dp);

    return lcs_len;
}

/* Longest common substring */
size_t string_longest_common_substring(const char* s1, const char* s2, char** lcs) {
    if (!s1 || !s2) return 0;

    size_t len1 = strlen(s1);
    size_t len2 = strlen(s2);

    /* Create DP table */
    size_t** dp = malloc((len1 + 1) * sizeof(size_t*));
    for (size_t i = 0; i <= len1; i++) {
        dp[i] = calloc(len2 + 1, sizeof(size_t));
    }

    size_t max_len = 0;
    size_t end_pos = 0;

    /* Fill DP table */
    for (size_t i = 1; i <= len1; i++) {
        for (size_t j = 1; j <= len2; j++) {
            if (s1[i - 1] == s2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                if (dp[i][j] > max_len) {
                    max_len = dp[i][j];
                    end_pos = i;
                }
            }
        }
    }

    /* Extract the substring if requested */
    if (lcs && max_len > 0) {
        *lcs = malloc(max_len + 1);
        memcpy(*lcs, s1 + end_pos - max_len, max_len);
        (*lcs)[max_len] = '\0';
    }

    /* Free DP table */
    for (size_t i = 0; i <= len1; i++) {
        free(dp[i]);
    }
    free(dp);

    return max_len;
}

/* Palindrome functions */

/* Check if string is palindrome */
bool string_is_palindrome(const char* str) {
    if (!str) return false;

    size_t len = strlen(str);
    if (len <= 1) return true;

    size_t left = 0;
    size_t right = len - 1;

    while (left < right) {
        if (str[left] != str[right]) {
            return false;
        }
        left++;
        right--;
    }

    return true;
}

/* Find longest palindrome (simple O(n^3) algorithm) */
char* string_longest_palindrome(const char* str) {
    if (!str) return NULL;

    size_t len = strlen(str);
    if (len == 0) return strdup("");

    size_t max_len = 1;
    size_t start = 0;

    for (size_t i = 0; i < len; i++) {
        for (size_t j = i; j < len; j++) {
            /* Check if substring is palindrome */
            bool is_palindrome = true;
            size_t left = i, right = j;

            while (left < right) {
                if (str[left] != str[right]) {
                    is_palindrome = false;
                    break;
                }
                left++;
                right--;
            }

            if (is_palindrome && (j - i + 1) > max_len) {
                max_len = j - i + 1;
                start = i;
            }
        }
    }

    char* result = malloc(max_len + 1);
    memcpy(result, str + start, max_len);
    result[max_len] = '\0';

    return result;
}

/* String transformation functions */

/* Reverse string */
char* string_reverse(const char* str) {
    if (!str) return NULL;

    size_t len = strlen(str);
    char* result = malloc(len + 1);

    for (size_t i = 0; i < len; i++) {
        result[i] = str[len - 1 - i];
    }
    result[len] = '\0';

    return result;
}

/* Convert to lowercase */
char* string_to_lower(const char* str) {
    if (!str) return NULL;

    size_t len = strlen(str);
    char* result = malloc(len + 1);

    for (size_t i = 0; i < len; i++) {
        result[i] = tolower(str[i]);
    }
    result[len] = '\0';

    return result;
}

/* Convert to uppercase */
char* string_to_upper(const char* str) {
    if (!str) return NULL;

    size_t len = strlen(str);
    char* result = malloc(len + 1);

    for (size_t i = 0; i < len; i++) {
        result[i] = toupper(str[i]);
    }
    result[len] = '\0';

    return result;
}

/* Trim whitespace */
char* string_trim(const char* str) {
    if (!str) return NULL;

    /* Find first non-whitespace */
    const char* start = str;
    while (*start && isspace(*start)) {
        start++;
    }

    /* Find last non-whitespace */
    const char* end = str + strlen(str) - 1;
    while (end > start && isspace(*end)) {
        end--;
    }

    size_t len = end - start + 1;
    char* result = malloc(len + 1);
    memcpy(result, start, len);
    result[len] = '\0';

    return result;
}

/* String hashing functions */

/* DJB2 hash */
uint32_t string_hash_djb2(const char* str) {
    if (!str) return 0;

    uint32_t hash = 5381;
    int c;

    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c;  /* hash * 33 + c */
    }

    return hash;
}

/* FNV-1a hash */
uint32_t string_hash_fnv1a(const char* str) {
    if (!str) return 0;

    uint32_t hash = 2166136261u;

    while (*str) {
        hash ^= (uint8_t)*str++;
        hash *= 16777619u;
    }

    return hash;
}

/* MurmurHash3 (32-bit) */
uint64_t string_hash_murmur3(const char* str) {
    if (!str) return 0;

    const uint32_t c1 = 0xcc9e2d51;
    const uint32_t c2 = 0x1b873593;
    const uint32_t r1 = 15;
    const uint32_t r2 = 13;
    const uint32_t m = 5;
    const uint32_t n = 0xe6546b64;

    uint32_t hash = 0;
    size_t len = strlen(str);
    const int nblocks = len / 4;
    const uint32_t* blocks = (const uint32_t*)str;

    for (int i = 0; i < nblocks; i++) {
        uint32_t k = blocks[i];
        k *= c1;
        k = (k << r1) | (k >> (32 - r1));
        k *= c2;

        hash ^= k;
        hash = ((hash << r2) | (hash >> (32 - r2))) * m + n;
    }

    const uint8_t* tail = (const uint8_t*)(str + nblocks * 4);
    uint32_t k1 = 0;

    switch (len & 3) {
        case 3: k1 ^= tail[2] << 16;
        case 2: k1 ^= tail[1] << 8;
        case 1: k1 ^= tail[0];
                k1 *= c1;
                k1 = (k1 << r1) | (k1 >> (32 - r1));
                k1 *= c2;
                hash ^= k1;
    }

    hash ^= len;
    hash ^= (hash >> 16);
    hash *= 0x85ebca6b;
    hash ^= (hash >> 13);
    hash *= 0xc2b2ae35;
    hash ^= (hash >> 16);

    return hash;
}

/* String utilities */

/* Check if string starts with prefix */
bool string_starts_with(const char* str, const char* prefix) {
    if (!str || !prefix) return false;

    size_t str_len = strlen(str);
    size_t prefix_len = strlen(prefix);

    if (prefix_len > str_len) return false;

    return strncmp(str, prefix, prefix_len) == 0;
}

/* Check if string ends with suffix */
bool string_ends_with(const char* str, const char* suffix) {
    if (!str || !suffix) return false;

    size_t str_len = strlen(str);
    size_t suffix_len = strlen(suffix);

    if (suffix_len > str_len) return false;

    return strcmp(str + str_len - suffix_len, suffix) == 0;
}

/* Count words in string */
size_t string_count_words(const char* str) {
    if (!str) return 0;

    size_t count = 0;
    bool in_word = false;

    while (*str) {
        if (isspace(*str)) {
            in_word = false;
        } else if (!in_word) {
            in_word = true;
            count++;
        }
        str++;
    }

    return count;
}

/* Check if two strings are anagrams */
bool string_is_anagram(const char* s1, const char* s2) {
    if (!s1 || !s2) return false;

    size_t len1 = strlen(s1);
    size_t len2 = strlen(s2);

    if (len1 != len2) return false;

    int char_count[256] = {0};

    /* Count characters in s1 */
    for (size_t i = 0; i < len1; i++) {
        char_count[(unsigned char)s1[i]]++;
    }

    /* Subtract characters in s2 */
    for (size_t i = 0; i < len2; i++) {
        char_count[(unsigned char)s2[i]]--;
        if (char_count[(unsigned char)s2[i]] < 0) {
            return false;
        }
    }

    return true;
}

/* Check if s2 is rotation of s1 */
bool string_is_rotation(const char* s1, const char* s2) {
    if (!s1 || !s2) return false;

    size_t len1 = strlen(s1);
    size_t len2 = strlen(s2);

    if (len1 != len2) return false;
    if (len1 == 0) return true;

    /* Create s1 + s1 and check if s2 is substring */
    char* doubled = malloc(len1 * 2 + 1);
    strcpy(doubled, s1);
    strcat(doubled, s1);

    bool result = strstr(doubled, s2) != NULL;

    free(doubled);
    return result;
}