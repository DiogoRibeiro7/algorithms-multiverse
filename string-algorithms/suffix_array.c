/*
 * Suffix Array and LCP Array Construction in C
 * =============================================
 *
 * Algorithms implemented:
 * 1. Prefix doubling O(n log² n) for suffix array construction
 * 2. Kasai's algorithm O(n) for LCP array computation
 *
 * Applications:
 * - Pattern matching in O(m log n) time
 * - Finding longest repeated substring
 * - Counting distinct substrings
 * - Longest common substring between two strings
 *
 * Compilation: gcc -o suffix_array suffix_array.c -std=c11 -O2
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_TEXT_LENGTH 10000

/* Suffix structure for sorting */
typedef struct {
    int index;          /* Original index in text */
    int rank[2];        /* Rank pair for sorting */
} Suffix;

/* Comparison function for qsort */
int compare_suffixes(const void *a, const void *b) {
    Suffix *s1 = (Suffix *)a;
    Suffix *s2 = (Suffix *)b;

    if (s1->rank[0] != s2->rank[0])
        return s1->rank[0] - s2->rank[0];
    return s1->rank[1] - s2->rank[1];
}

/*
 * Build suffix array using prefix doubling algorithm
 * Time: O(n log² n)
 * Space: O(n)
 *
 * Algorithm:
 * 1. Initially rank suffixes by first character
 * 2. Double the comparison length in each iteration
 * 3. Sort by (rank[i], rank[i+len])
 * 4. Update ranks based on new ordering
 */
void build_suffix_array(const char *text, int n, int *sa) {
    Suffix *suffixes = (Suffix *)malloc(n * sizeof(Suffix));
    int *rank = (int *)malloc(n * sizeof(int));
    int *temp_rank = (int *)malloc(n * sizeof(int));

    /* Initialize ranks with character values */
    for (int i = 0; i < n; i++) {
        suffixes[i].index = i;
        suffixes[i].rank[0] = text[i];
        suffixes[i].rank[1] = (i + 1 < n) ? text[i + 1] : -1;
    }

    /* Sort by first two characters */
    qsort(suffixes, n, sizeof(Suffix), compare_suffixes);

    /* Build rank array */
    for (int i = 0; i < n; i++) {
        rank[suffixes[i].index] = i;
    }

    /* Prefix doubling */
    for (int k = 4; k < 2 * n; k *= 2) {
        /* Update ranks for sorting */
        for (int i = 0; i < n; i++) {
            int curr = suffixes[i].index;
            suffixes[i].rank[0] = rank[curr];
            suffixes[i].rank[1] = (curr + k / 2 < n) ? rank[curr + k / 2] : -1;
        }

        /* Sort suffixes */
        qsort(suffixes, n, sizeof(Suffix), compare_suffixes);

        /* Update ranks */
        temp_rank[suffixes[0].index] = 0;

        for (int i = 1; i < n; i++) {
            Suffix prev = suffixes[i - 1];
            Suffix curr = suffixes[i];

            /* Same rank if both pairs are equal */
            if (curr.rank[0] == prev.rank[0] && curr.rank[1] == prev.rank[1]) {
                temp_rank[curr.index] = temp_rank[prev.index];
            } else {
                temp_rank[curr.index] = temp_rank[prev.index] + 1;
            }
        }

        /* Copy temp ranks to rank array */
        memcpy(rank, temp_rank, n * sizeof(int));
    }

    /* Build suffix array from sorted suffixes */
    for (int i = 0; i < n; i++) {
        sa[i] = suffixes[i].index;
    }

    free(suffixes);
    free(rank);
    free(temp_rank);
}

/*
 * Build LCP array using Kasai's algorithm
 * Time: O(n)
 * Space: O(n)
 *
 * LCP[i] = length of longest common prefix between
 *          suffix[SA[i]] and suffix[SA[i-1]]
 *
 * Key property: If LCP[rank[i]] = h, then LCP[rank[i+1]] >= h - 1
 */
void build_lcp_array(const char *text, int n, const int *sa, int *lcp) {
    int *rank = (int *)malloc(n * sizeof(int));

    /* Compute inverse suffix array (rank) */
    for (int i = 0; i < n; i++) {
        rank[sa[i]] = i;
    }

    int h = 0;  /* Height of LCP */

    for (int i = 0; i < n; i++) {
        if (rank[i] > 0) {
            int j = sa[rank[i] - 1];

            /* Compute LCP */
            while (i + h < n && j + h < n && text[i + h] == text[j + h]) {
                h++;
            }

            lcp[rank[i]] = h;

            /* Decrease h for next iteration */
            if (h > 0) {
                h--;
            }
        }
    }

    free(rank);
}

/*
 * Pattern search using suffix array with binary search
 * Time: O(m log n)
 * Returns: Number of matches found
 */
int pattern_search(const char *text, int n, const int *sa,
                   const char *pattern, int m, int *matches) {
    int count = 0;

    /* Binary search for lower bound */
    int left = 0, right = n;
    while (left < right) {
        int mid = (left + right) / 2;
        int cmp = strncmp(text + sa[mid], pattern, m);

        if (cmp < 0) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    int lower = left;

    /* Binary search for upper bound */
    left = 0;
    right = n;
    while (left < right) {
        int mid = (left + right) / 2;
        int cmp = strncmp(text + sa[mid], pattern, m);

        if (cmp <= 0) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    int upper = right;

    /* Collect all matches */
    for (int i = lower; i < upper; i++) {
        if (strncmp(text + sa[i], pattern, m) == 0) {
            matches[count++] = sa[i];
        }
    }

    return count;
}

/*
 * Find longest repeated substring using LCP array
 * Time: O(n)
 */
int longest_repeated_substring(const char *text, int n,
                               const int *sa, const int *lcp,
                               char *result) {
    int max_lcp = 0;
    int max_idx = 0;

    /* Find maximum LCP value */
    for (int i = 1; i < n; i++) {
        if (lcp[i] > max_lcp) {
            max_lcp = lcp[i];
            max_idx = i;
        }
    }

    if (max_lcp == 0) {
        result[0] = '\0';
        return 0;
    }

    /* Copy the substring */
    strncpy(result, text + sa[max_idx], max_lcp);
    result[max_lcp] = '\0';

    return max_lcp;
}

/*
 * Count distinct substrings
 * Time: O(n)
 *
 * Formula: n*(n+1)/2 - sum(LCP)
 */
long long count_distinct_substrings(int n, const int *lcp) {
    long long total = (long long)n * (n + 1) / 2;
    long long duplicates = 0;

    for (int i = 1; i < n; i++) {
        duplicates += lcp[i];
    }

    return total - duplicates;
}

/*
 * Visualize suffix array and LCP array
 */
void visualize_suffix_array(const char *text, int n, const int *sa, const int *lcp) {
    printf("\nSuffix Array Visualization:\n");
    printf("Text: '%s'\n", text);
    printf("Length: %d\n\n", n);

    printf("%-4s | %-6s | %-6s | Suffix\n", "i", "SA[i]", "LCP[i]");
    printf("-----|--------|--------|");
    for (int i = 0; i < 40; i++) printf("-");
    printf("\n");

    for (int i = 0; i < n; i++) {
        printf("%-4d | %-6d | %-6d | ", i, sa[i], lcp[i]);

        /* Print suffix (truncate if too long) */
        const char *suffix = text + sa[i];
        int len = strlen(suffix);
        if (len > 40) {
            printf("%.37s...\n", suffix);
        } else {
            printf("%s\n", suffix);
        }
    }
    printf("\n");
}

/*
 * Benchmark suffix array construction
 */
double benchmark_construction(const char *text, int n) {
    int *sa = (int *)malloc(n * sizeof(int));

    clock_t start = clock();
    build_suffix_array(text, n, sa);
    clock_t end = clock();

    double time_ms = ((double)(end - start) / CLOCKS_PER_SEC) * 1000.0;

    free(sa);
    return time_ms;
}

/* ========================================================================= */
/* EXAMPLES AND TESTING                                                      */
/* ========================================================================= */

void example_basic_construction() {
    printf("=======================================================================\n");
    printf("EXAMPLE 1: Basic Suffix Array Construction\n");
    printf("=======================================================================\n");

    const char *text = "banana";
    int n = strlen(text);

    int *sa = (int *)malloc(n * sizeof(int));
    int *lcp = (int *)calloc(n, sizeof(int));

    build_suffix_array(text, n, sa);
    build_lcp_array(text, n, sa, lcp);

    visualize_suffix_array(text, n, sa, lcp);

    free(sa);
    free(lcp);
}

void example_pattern_search() {
    printf("=======================================================================\n");
    printf("EXAMPLE 2: Pattern Searching\n");
    printf("=======================================================================\n");

    const char *text = "the quick brown fox jumps over the lazy dog";
    const char *pattern = "the";
    int n = strlen(text);
    int m = strlen(pattern);

    int *sa = (int *)malloc(n * sizeof(int));
    int *matches = (int *)malloc(n * sizeof(int));

    build_suffix_array(text, n, sa);
    int count = pattern_search(text, n, sa, pattern, m, matches);

    printf("Text: '%s'\n", text);
    printf("Pattern: '%s'\n", pattern);
    printf("Matches at positions: ");

    for (int i = 0; i < count; i++) {
        printf("%d ", matches[i]);
    }
    printf("\n\n");

    for (int i = 0; i < count; i++) {
        printf("  Position %d: '", matches[i]);
        for (int j = 0; j < m; j++) {
            printf("%c", text[matches[i] + j]);
        }
        printf("'\n");
    }
    printf("\n");

    free(sa);
    free(matches);
}

void example_longest_repeated_substring() {
    printf("=======================================================================\n");
    printf("EXAMPLE 3: Longest Repeated Substring\n");
    printf("=======================================================================\n");

    const char *text = "abracadabra";
    int n = strlen(text);

    int *sa = (int *)malloc(n * sizeof(int));
    int *lcp = (int *)calloc(n, sizeof(int));
    char result[MAX_TEXT_LENGTH];

    build_suffix_array(text, n, sa);
    build_lcp_array(text, n, sa, lcp);

    longest_repeated_substring(text, n, sa, lcp, result);

    printf("Text: '%s'\n", text);
    printf("Longest repeated substring: '%s'\n\n", result);

    free(sa);
    free(lcp);
}

void example_count_distinct() {
    printf("=======================================================================\n");
    printf("EXAMPLE 4: Count Distinct Substrings\n");
    printf("=======================================================================\n");

    const char *text = "abab";
    int n = strlen(text);

    int *sa = (int *)malloc(n * sizeof(int));
    int *lcp = (int *)calloc(n, sizeof(int));

    build_suffix_array(text, n, sa);
    build_lcp_array(text, n, sa, lcp);

    long long count = count_distinct_substrings(n, lcp);

    printf("Text: '%s'\n", text);
    printf("Number of distinct substrings: %lld\n\n", count);

    free(sa);
    free(lcp);
}

void example_benchmark() {
    printf("=======================================================================\n");
    printf("EXAMPLE 5: Performance Benchmarking\n");
    printf("=======================================================================\n");

    /* Small text */
    char small_text[1000];
    strcpy(small_text, "");
    for (int i = 0; i < 10; i++) {
        strcat(small_text, "banana");
    }

    printf("Small text (length %zu): %.4f ms\n",
           strlen(small_text),
           benchmark_construction(small_text, strlen(small_text)));

    /* Medium text */
    char medium_text[2000];
    strcpy(medium_text, "");
    for (int i = 0; i < 100; i++) {
        strcat(medium_text, "abracadabra");
    }

    printf("Medium text (length %zu): %.4f ms\n\n",
           strlen(medium_text),
           benchmark_construction(medium_text, strlen(medium_text)));
}

int main() {
    printf("=======================================================================\n");
    printf("SUFFIX ARRAY AND LCP ARRAY IN C\n");
    printf("=======================================================================\n\n");

    example_basic_construction();
    example_pattern_search();
    example_longest_repeated_substring();
    example_count_distinct();
    example_benchmark();

    printf("=======================================================================\n");
    printf("All examples completed successfully!\n");
    printf("=======================================================================\n");

    return 0;
}
