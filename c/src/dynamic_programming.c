/**
 * @file dynamic_programming.c
 * @brief Implementation of dynamic programming algorithms
 */

#include "dynamic_programming.h"
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <math.h>
#include <stdio.h>

#define MIN(a,b) ((a) < (b) ? (a) : (b))
#define MAX(a,b) ((a) > (b) ? (a) : (b))
#define MIN3(a,b,c) MIN(MIN(a,b),c)

/* =========================== */
/*    Fibonacci & Sequences    */
/* =========================== */

int64_t dp_fibonacci(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;

    int64_t prev2 = 0, prev1 = 1, current = 0;
    for (int i = 2; i <= n; i++) {
        current = prev1 + prev2;
        prev2 = prev1;
        prev1 = current;
    }
    return current;
}

int64_t dp_fibonacci_memoized(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;

    int64_t* memo = calloc(n + 1, sizeof(int64_t));
    memo[0] = 0;
    memo[1] = 1;

    for (int i = 2; i <= n; i++) {
        if (memo[i] == 0) {
            memo[i] = memo[i-1] + memo[i-2];
        }
    }

    int64_t result = memo[n];
    free(memo);
    return result;
}

int64_t dp_fibonacci_bottom_up(int n) {
    return dp_fibonacci(n);  /* Already implemented as bottom-up */
}

int64_t dp_tribonacci(int n) {
    if (n == 0) return 0;
    if (n == 1 || n == 2) return 1;

    int64_t t0 = 0, t1 = 1, t2 = 1, tn = 0;
    for (int i = 3; i <= n; i++) {
        tn = t0 + t1 + t2;
        t0 = t1;
        t1 = t2;
        t2 = tn;
    }
    return tn;
}

int64_t dp_climbing_stairs(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    if (n == 2) return 2;

    int64_t prev2 = 1, prev1 = 2, current = 0;
    for (int i = 3; i <= n; i++) {
        current = prev1 + prev2;
        prev2 = prev1;
        prev1 = current;
    }
    return current;
}

int64_t dp_climbing_stairs_k_steps(int n, int k) {
    if (n <= 0 || k <= 0) return 0;

    int64_t* dp = calloc(n + 1, sizeof(int64_t));
    dp[0] = 1;

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= k && j <= i; j++) {
            dp[i] += dp[i - j];
        }
    }

    int64_t result = dp[n];
    free(dp);
    return result;
}

/* =========================== */
/*      Subset Problems        */
/* =========================== */

bool dp_subset_sum(const int* arr, size_t n, int target) {
    if (target == 0) return true;
    if (n == 0) return false;

    /* Create DP table */
    bool** dp = malloc((n + 1) * sizeof(bool*));
    for (size_t i = 0; i <= n; i++) {
        dp[i] = calloc(abs(target) + 1, sizeof(bool));
    }

    /* Base case: empty subset sums to 0 */
    for (size_t i = 0; i <= n; i++) {
        dp[i][0] = true;
    }

    /* Fill the DP table */
    for (size_t i = 1; i <= n; i++) {
        for (int j = 1; j <= abs(target); j++) {
            dp[i][j] = dp[i-1][j];  /* Exclude current element */
            if (j >= arr[i-1]) {
                dp[i][j] = dp[i][j] || dp[i-1][j - arr[i-1]];  /* Include current element */
            }
        }
    }

    bool result = dp[n][abs(target)];

    /* Free memory */
    for (size_t i = 0; i <= n; i++) {
        free(dp[i]);
    }
    free(dp);

    return result;
}

subset_result_t* dp_subset_sum_solution(const int* arr, size_t n, int target) {
    subset_result_t* result = malloc(sizeof(subset_result_t));
    result->subset = NULL;
    result->size = 0;
    result->found = false;

    if (target == 0) {
        result->found = true;
        return result;
    }
    if (n == 0) return result;

    /* Create DP table */
    bool** dp = malloc((n + 1) * sizeof(bool*));
    for (size_t i = 0; i <= n; i++) {
        dp[i] = calloc(abs(target) + 1, sizeof(bool));
    }

    /* Base case */
    for (size_t i = 0; i <= n; i++) {
        dp[i][0] = true;
    }

    /* Fill DP table */
    for (size_t i = 1; i <= n; i++) {
        for (int j = 1; j <= abs(target); j++) {
            dp[i][j] = dp[i-1][j];
            if (j >= arr[i-1]) {
                dp[i][j] = dp[i][j] || dp[i-1][j - arr[i-1]];
            }
        }
    }

    if (dp[n][abs(target)]) {
        result->found = true;
        result->subset = malloc(n * sizeof(size_t));

        /* Backtrack to find the subset */
        int j = abs(target);
        size_t count = 0;
        for (size_t i = n; i > 0 && j > 0; i--) {
            if (!dp[i-1][j]) {
                result->subset[count++] = i - 1;
                j -= arr[i-1];
            }
        }
        result->size = count;
    }

    /* Free DP table */
    for (size_t i = 0; i <= n; i++) {
        free(dp[i]);
    }
    free(dp);

    return result;
}

void subset_result_free(subset_result_t* result) {
    if (result) {
        free(result->subset);
        free(result);
    }
}

bool dp_partition_equal_subset(const int* arr, size_t n) {
    int sum = 0;
    for (size_t i = 0; i < n; i++) {
        sum += arr[i];
    }

    /* If sum is odd, can't partition equally */
    if (sum % 2 != 0) return false;

    return dp_subset_sum(arr, n, sum / 2);
}

int dp_minimum_subset_sum_difference(const int* arr, size_t n) {
    int sum = 0;
    for (size_t i = 0; i < n; i++) {
        sum += arr[i];
    }

    /* Find subset with sum closest to sum/2 */
    int target = sum / 2;

    bool** dp = malloc((n + 1) * sizeof(bool*));
    for (size_t i = 0; i <= n; i++) {
        dp[i] = calloc(target + 1, sizeof(bool));
    }

    for (size_t i = 0; i <= n; i++) {
        dp[i][0] = true;
    }

    for (size_t i = 1; i <= n; i++) {
        for (int j = 1; j <= target; j++) {
            dp[i][j] = dp[i-1][j];
            if (j >= arr[i-1]) {
                dp[i][j] = dp[i][j] || dp[i-1][j - arr[i-1]];
            }
        }
    }

    /* Find the largest j <= target for which dp[n][j] is true */
    int max_sum = 0;
    for (int j = target; j >= 0; j--) {
        if (dp[n][j]) {
            max_sum = j;
            break;
        }
    }

    /* Free memory */
    for (size_t i = 0; i <= n; i++) {
        free(dp[i]);
    }
    free(dp);

    return abs(sum - 2 * max_sum);
}

size_t dp_count_subsets_with_sum(const int* arr, size_t n, int target) {
    if (target < 0) return 0;

    /* Create DP table */
    size_t** dp = malloc((n + 1) * sizeof(size_t*));
    for (size_t i = 0; i <= n; i++) {
        dp[i] = calloc(target + 1, sizeof(size_t));
    }

    /* Base case: empty subset sums to 0 */
    for (size_t i = 0; i <= n; i++) {
        dp[i][0] = 1;
    }

    /* Fill the DP table */
    for (size_t i = 1; i <= n; i++) {
        for (int j = 0; j <= target; j++) {
            dp[i][j] = dp[i-1][j];  /* Exclude current element */
            if (j >= arr[i-1]) {
                dp[i][j] += dp[i-1][j - arr[i-1]];  /* Include current element */
            }
        }
    }

    size_t result = dp[n][target];

    /* Free memory */
    for (size_t i = 0; i <= n; i++) {
        free(dp[i]);
    }
    free(dp);

    return result;
}

/* =========================== */
/*     Knapsack Problems       */
/* =========================== */

knapsack_result_t* dp_knapsack_01(const int* weights, const int* values, size_t n, int capacity) {
    knapsack_result_t* result = malloc(sizeof(knapsack_result_t));
    result->items = NULL;
    result->count = 0;
    result->total_value = 0;
    result->total_weight = 0;

    if (n == 0 || capacity <= 0) return result;

    /* Create DP table */
    int** dp = malloc((n + 1) * sizeof(int*));
    for (size_t i = 0; i <= n; i++) {
        dp[i] = calloc(capacity + 1, sizeof(int));
    }

    /* Fill DP table */
    for (size_t i = 1; i <= n; i++) {
        for (int w = 1; w <= capacity; w++) {
            if (weights[i-1] <= w) {
                dp[i][w] = MAX(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1]);
            } else {
                dp[i][w] = dp[i-1][w];
            }
        }
    }

    result->total_value = dp[n][capacity];

    /* Backtrack to find selected items */
    result->items = malloc(n * sizeof(size_t));
    int w = capacity;
    size_t count = 0;

    for (size_t i = n; i > 0 && w > 0; i--) {
        if (dp[i][w] != dp[i-1][w]) {
            result->items[count++] = i - 1;
            result->total_weight += weights[i-1];
            w -= weights[i-1];
        }
    }
    result->count = count;

    /* Free DP table */
    for (size_t i = 0; i <= n; i++) {
        free(dp[i]);
    }
    free(dp);

    return result;
}

void knapsack_result_free(knapsack_result_t* result) {
    if (result) {
        free(result->items);
        free(result);
    }
}

int dp_knapsack_unbounded(const int* weights, const int* values, size_t n, int capacity) {
    if (n == 0 || capacity <= 0) return 0;

    int* dp = calloc(capacity + 1, sizeof(int));

    for (int w = 1; w <= capacity; w++) {
        for (size_t i = 0; i < n; i++) {
            if (weights[i] <= w) {
                dp[w] = MAX(dp[w], dp[w - weights[i]] + values[i]);
            }
        }
    }

    int result = dp[capacity];
    free(dp);
    return result;
}

int dp_knapsack_bounded(const int* weights, const int* values,
                        const int* quantities, size_t n, int capacity) {
    if (n == 0 || capacity <= 0) return 0;

    int* dp = calloc(capacity + 1, sizeof(int));

    for (size_t i = 0; i < n; i++) {
        for (int w = capacity; w >= weights[i]; w--) {
            for (int k = 1; k <= quantities[i] && k * weights[i] <= w; k++) {
                dp[w] = MAX(dp[w], dp[w - k * weights[i]] + k * values[i]);
            }
        }
    }

    int result = dp[capacity];
    free(dp);
    return result;
}

double dp_fractional_knapsack(const double* weights, const double* values,
                               size_t n, double capacity) {
    if (n == 0 || capacity <= 0) return 0;

    /* Create array of items with value/weight ratio */
    typedef struct {
        double weight;
        double value;
        double ratio;
        size_t index;
    } item_t;

    item_t* items = malloc(n * sizeof(item_t));
    for (size_t i = 0; i < n; i++) {
        items[i].weight = weights[i];
        items[i].value = values[i];
        items[i].ratio = values[i] / weights[i];
        items[i].index = i;
    }

    /* Sort by ratio in descending order */
    for (size_t i = 0; i < n - 1; i++) {
        for (size_t j = 0; j < n - i - 1; j++) {
            if (items[j].ratio < items[j + 1].ratio) {
                item_t temp = items[j];
                items[j] = items[j + 1];
                items[j + 1] = temp;
            }
        }
    }

    double total_value = 0;
    double remaining_capacity = capacity;

    for (size_t i = 0; i < n && remaining_capacity > 0; i++) {
        if (items[i].weight <= remaining_capacity) {
            total_value += items[i].value;
            remaining_capacity -= items[i].weight;
        } else {
            total_value += (remaining_capacity / items[i].weight) * items[i].value;
            remaining_capacity = 0;
        }
    }

    free(items);
    return total_value;
}

/* =========================== */
/*  Longest Common Subsequence */
/* =========================== */

size_t dp_longest_common_subsequence(const char* s1, const char* s2, char** lcs) {
    if (!s1 || !s2) return 0;

    size_t m = strlen(s1);
    size_t n = strlen(s2);

    /* Create DP table */
    int** dp = malloc((m + 1) * sizeof(int*));
    for (size_t i = 0; i <= m; i++) {
        dp[i] = calloc(n + 1, sizeof(int));
    }

    /* Fill DP table */
    for (size_t i = 1; i <= m; i++) {
        for (size_t j = 1; j <= n; j++) {
            if (s1[i-1] == s2[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = MAX(dp[i-1][j], dp[i][j-1]);
            }
        }
    }

    size_t lcs_length = dp[m][n];

    /* Reconstruct LCS if requested */
    if (lcs && lcs_length > 0) {
        *lcs = malloc(lcs_length + 1);
        (*lcs)[lcs_length] = '\0';

        size_t i = m, j = n, index = lcs_length;
        while (i > 0 && j > 0) {
            if (s1[i-1] == s2[j-1]) {
                (*lcs)[--index] = s1[i-1];
                i--;
                j--;
            } else if (dp[i-1][j] > dp[i][j-1]) {
                i--;
            } else {
                j--;
            }
        }
    }

    /* Free DP table */
    for (size_t i = 0; i <= m; i++) {
        free(dp[i]);
    }
    free(dp);

    return lcs_length;
}

void lcs_result_free(lcs_result_t* result) {
    if (result) {
        free(result->sequence);
        free(result);
    }
}

/* =========================== */
/*  Longest Increasing Subseq */
/* =========================== */

size_t dp_longest_increasing_subsequence(const int* arr, size_t n, int** lis) {
    if (!arr || n == 0) return 0;

    size_t* dp = malloc(n * sizeof(size_t));
    size_t* parent = malloc(n * sizeof(size_t));

    for (size_t i = 0; i < n; i++) {
        dp[i] = 1;
        parent[i] = i;
    }

    size_t max_length = 1;
    size_t max_index = 0;

    for (size_t i = 1; i < n; i++) {
        for (size_t j = 0; j < i; j++) {
            if (arr[j] < arr[i] && dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
                parent[i] = j;
            }
        }
        if (dp[i] > max_length) {
            max_length = dp[i];
            max_index = i;
        }
    }

    /* Reconstruct LIS if requested */
    if (lis) {
        *lis = malloc(max_length * sizeof(int));
        size_t index = max_index;
        for (int i = max_length - 1; i >= 0; i--) {
            (*lis)[i] = arr[index];
            if (index == parent[index]) break;
            index = parent[index];
        }
    }

    free(dp);
    free(parent);
    return max_length;
}

size_t dp_longest_decreasing_subsequence(const int* arr, size_t n, int** lds) {
    if (!arr || n == 0) return 0;

    size_t* dp = malloc(n * sizeof(size_t));
    size_t* parent = malloc(n * sizeof(size_t));

    for (size_t i = 0; i < n; i++) {
        dp[i] = 1;
        parent[i] = i;
    }

    size_t max_length = 1;
    size_t max_index = 0;

    for (size_t i = 1; i < n; i++) {
        for (size_t j = 0; j < i; j++) {
            if (arr[j] > arr[i] && dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
                parent[i] = j;
            }
        }
        if (dp[i] > max_length) {
            max_length = dp[i];
            max_index = i;
        }
    }

    /* Reconstruct LDS if requested */
    if (lds) {
        *lds = malloc(max_length * sizeof(int));
        size_t index = max_index;
        for (int i = max_length - 1; i >= 0; i--) {
            (*lds)[i] = arr[index];
            if (index == parent[index]) break;
            index = parent[index];
        }
    }

    free(dp);
    free(parent);
    return max_length;
}

size_t dp_longest_bitonic_subsequence(const int* arr, size_t n) {
    if (!arr || n == 0) return 0;

    /* LIS from left to right */
    size_t* lis = malloc(n * sizeof(size_t));
    for (size_t i = 0; i < n; i++) {
        lis[i] = 1;
        for (size_t j = 0; j < i; j++) {
            if (arr[j] < arr[i] && lis[j] + 1 > lis[i]) {
                lis[i] = lis[j] + 1;
            }
        }
    }

    /* LDS from right to left */
    size_t* lds = malloc(n * sizeof(size_t));
    for (int i = n - 1; i >= 0; i--) {
        lds[i] = 1;
        for (size_t j = n - 1; j > i; j--) {
            if (arr[j] < arr[i] && lds[j] + 1 > lds[i]) {
                lds[i] = lds[j] + 1;
            }
        }
    }

    /* Find maximum bitonic length */
    size_t max_length = 0;
    for (size_t i = 0; i < n; i++) {
        size_t bitonic_length = lis[i] + lds[i] - 1;
        if (bitonic_length > max_length) {
            max_length = bitonic_length;
        }
    }

    free(lis);
    free(lds);
    return max_length;
}

size_t dp_longest_palindromic_subsequence(const char* str, char** lps) {
    if (!str) return 0;

    size_t n = strlen(str);
    if (n == 0) return 0;

    /* Reverse the string and find LCS with original */
    char* rev = malloc(n + 1);
    for (size_t i = 0; i < n; i++) {
        rev[i] = str[n - 1 - i];
    }
    rev[n] = '\0';

    size_t result = dp_longest_common_subsequence(str, rev, lps);
    free(rev);
    return result;
}

size_t dp_longest_repeating_subsequence(const char* str, char** lrs) {
    if (!str) return 0;

    size_t n = strlen(str);
    if (n == 0) return 0;

    /* Create DP table */
    int** dp = malloc((n + 1) * sizeof(int*));
    for (size_t i = 0; i <= n; i++) {
        dp[i] = calloc(n + 1, sizeof(int));
    }

    /* Fill DP table - similar to LCS but with constraint i != j */
    for (size_t i = 1; i <= n; i++) {
        for (size_t j = 1; j <= n; j++) {
            if (str[i-1] == str[j-1] && i != j) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = MAX(dp[i-1][j], dp[i][j-1]);
            }
        }
    }

    size_t lrs_length = dp[n][n];

    /* Reconstruct LRS if requested */
    if (lrs && lrs_length > 0) {
        *lrs = malloc(lrs_length + 1);
        (*lrs)[lrs_length] = '\0';

        size_t i = n, j = n, index = lrs_length;
        while (i > 0 && j > 0) {
            if (dp[i][j] == dp[i-1][j-1] + 1) {
                (*lrs)[--index] = str[i-1];
                i--;
                j--;
            } else if (dp[i-1][j] > dp[i][j-1]) {
                i--;
            } else {
                j--;
            }
        }
    }

    /* Free DP table */
    for (size_t i = 0; i <= n; i++) {
        free(dp[i]);
    }
    free(dp);

    return lrs_length;
}

/* =========================== */
/*      Edit Distance          */
/* =========================== */

size_t dp_edit_distance(const char* s1, const char* s2) {
    if (!s1) s1 = "";
    if (!s2) s2 = "";

    size_t m = strlen(s1);
    size_t n = strlen(s2);

    /* Create DP table */
    size_t** dp = malloc((m + 1) * sizeof(size_t*));
    for (size_t i = 0; i <= m; i++) {
        dp[i] = malloc((n + 1) * sizeof(size_t));
    }

    /* Initialize base cases */
    for (size_t i = 0; i <= m; i++) dp[i][0] = i;
    for (size_t j = 0; j <= n; j++) dp[0][j] = j;

    /* Fill DP table */
    for (size_t i = 1; i <= m; i++) {
        for (size_t j = 1; j <= n; j++) {
            if (s1[i-1] == s2[j-1]) {
                dp[i][j] = dp[i-1][j-1];
            } else {
                dp[i][j] = 1 + MIN3(dp[i-1][j],    /* delete */
                                    dp[i][j-1],    /* insert */
                                    dp[i-1][j-1]); /* replace */
            }
        }
    }

    size_t result = dp[m][n];

    /* Free DP table */
    for (size_t i = 0; i <= m; i++) {
        free(dp[i]);
    }
    free(dp);

    return result;
}

size_t dp_edit_distance_weighted(const char* s1, const char* s2,
                                  size_t insert_cost, size_t delete_cost,
                                  size_t replace_cost) {
    if (!s1) s1 = "";
    if (!s2) s2 = "";

    size_t m = strlen(s1);
    size_t n = strlen(s2);

    /* Create DP table */
    size_t** dp = malloc((m + 1) * sizeof(size_t*));
    for (size_t i = 0; i <= m; i++) {
        dp[i] = malloc((n + 1) * sizeof(size_t));
    }

    /* Initialize base cases */
    dp[0][0] = 0;
    for (size_t i = 1; i <= m; i++) dp[i][0] = i * delete_cost;
    for (size_t j = 1; j <= n; j++) dp[0][j] = j * insert_cost;

    /* Fill DP table */
    for (size_t i = 1; i <= m; i++) {
        for (size_t j = 1; j <= n; j++) {
            if (s1[i-1] == s2[j-1]) {
                dp[i][j] = dp[i-1][j-1];
            } else {
                dp[i][j] = MIN3(dp[i-1][j] + delete_cost,
                                dp[i][j-1] + insert_cost,
                                dp[i-1][j-1] + replace_cost);
            }
        }
    }

    size_t result = dp[m][n];

    /* Free DP table */
    for (size_t i = 0; i <= m; i++) {
        free(dp[i]);
    }
    free(dp);

    return result;
}

size_t dp_min_insertions_palindrome(const char* str) {
    if (!str) return 0;

    size_t n = strlen(str);
    if (n <= 1) return 0;

    /* LPS length tells us how many chars are already in palindrome order */
    size_t lps_length = dp_longest_palindromic_subsequence(str, NULL);

    /* Minimum insertions = string length - LPS length */
    return n - lps_length;
}

size_t dp_min_deletions_palindrome(const char* str) {
    /* Same as minimum insertions */
    return dp_min_insertions_palindrome(str);
}

/* Continue with remaining functions... */

/* =========================== */
/*      Coin Change            */
/* =========================== */

int dp_coin_change_min_coins(const int* coins, size_t n, int amount) {
    if (amount == 0) return 0;
    if (n == 0 || amount < 0) return -1;

    int* dp = malloc((amount + 1) * sizeof(int));
    for (int i = 0; i <= amount; i++) {
        dp[i] = INT_MAX;
    }
    dp[0] = 0;

    for (int i = 1; i <= amount; i++) {
        for (size_t j = 0; j < n; j++) {
            if (coins[j] <= i && dp[i - coins[j]] != INT_MAX) {
                dp[i] = MIN(dp[i], dp[i - coins[j]] + 1);
            }
        }
    }

    int result = (dp[amount] == INT_MAX) ? -1 : dp[amount];
    free(dp);
    return result;
}

int dp_coin_change_count_ways(const int* coins, size_t n, int amount) {
    if (amount == 0) return 1;
    if (n == 0 || amount < 0) return 0;

    int* dp = calloc(amount + 1, sizeof(int));
    dp[0] = 1;

    for (size_t i = 0; i < n; i++) {
        for (int j = coins[i]; j <= amount; j++) {
            dp[j] += dp[j - coins[i]];
        }
    }

    int result = dp[amount];
    free(dp);
    return result;
}

/* =========================== */
/*    Matrix Chain Multiply    */
/* =========================== */

int dp_matrix_chain_multiplication(const int* dimensions, size_t n) {
    if (n < 2) return 0;

    size_t num_matrices = n - 1;

    /* Create DP table */
    int** dp = malloc(num_matrices * sizeof(int*));
    for (size_t i = 0; i < num_matrices; i++) {
        dp[i] = calloc(num_matrices, sizeof(int));
    }

    /* Fill DP table */
    for (size_t len = 2; len <= num_matrices; len++) {
        for (size_t i = 0; i <= num_matrices - len; i++) {
            size_t j = i + len - 1;
            dp[i][j] = INT_MAX;

            for (size_t k = i; k < j; k++) {
                int cost = dp[i][k] + dp[k+1][j] +
                          dimensions[i] * dimensions[k+1] * dimensions[j+1];
                dp[i][j] = MIN(dp[i][j], cost);
            }
        }
    }

    int result = dp[0][num_matrices - 1];

    /* Free DP table */
    for (size_t i = 0; i < num_matrices; i++) {
        free(dp[i]);
    }
    free(dp);

    return result;
}

/* =========================== */
/*     Grid Path Problems      */
/* =========================== */

int dp_unique_paths(int m, int n) {
    if (m <= 0 || n <= 0) return 0;

    int* dp = calloc(n, sizeof(int));
    dp[0] = 1;

    for (int i = 0; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[j] += dp[j-1];
        }
    }

    int result = dp[n-1];
    free(dp);
    return result;
}

int dp_unique_paths_with_obstacles(int** grid, int m, int n) {
    if (!grid || m <= 0 || n <= 0 || grid[0][0] == 1) return 0;

    int* dp = calloc(n, sizeof(int));
    dp[0] = 1;

    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == 1) {
                dp[j] = 0;
            } else if (j > 0) {
                dp[j] += dp[j-1];
            }
        }
    }

    int result = dp[n-1];
    free(dp);
    return result;
}

int dp_min_path_sum(int** grid, int m, int n) {
    if (!grid || m <= 0 || n <= 0) return 0;

    int** dp = malloc(m * sizeof(int*));
    for (int i = 0; i < m; i++) {
        dp[i] = malloc(n * sizeof(int));
    }

    dp[0][0] = grid[0][0];

    /* Initialize first row */
    for (int j = 1; j < n; j++) {
        dp[0][j] = dp[0][j-1] + grid[0][j];
    }

    /* Initialize first column */
    for (int i = 1; i < m; i++) {
        dp[i][0] = dp[i-1][0] + grid[i][0];
    }

    /* Fill rest of the table */
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = grid[i][j] + MIN(dp[i-1][j], dp[i][j-1]);
        }
    }

    int result = dp[m-1][n-1];

    /* Free DP table */
    for (int i = 0; i < m; i++) {
        free(dp[i]);
    }
    free(dp);

    return result;
}

/* =========================== */
/*      Stock Problems         */
/* =========================== */

int dp_stock_buy_sell_one_transaction(const int* prices, size_t n) {
    if (!prices || n < 2) return 0;

    int min_price = prices[0];
    int max_profit = 0;

    for (size_t i = 1; i < n; i++) {
        max_profit = MAX(max_profit, prices[i] - min_price);
        min_price = MIN(min_price, prices[i]);
    }

    return max_profit;
}

int dp_stock_buy_sell_unlimited(const int* prices, size_t n) {
    if (!prices || n < 2) return 0;

    int total_profit = 0;

    for (size_t i = 1; i < n; i++) {
        if (prices[i] > prices[i-1]) {
            total_profit += prices[i] - prices[i-1];
        }
    }

    return total_profit;
}

int dp_stock_buy_sell_k_transactions(const int* prices, size_t n, int k) {
    if (!prices || n < 2 || k <= 0) return 0;

    /* If k >= n/2, we can make as many transactions as we want */
    if (k >= n / 2) {
        return dp_stock_buy_sell_unlimited(prices, n);
    }

    /* Create DP tables for buy and sell states */
    int* buy = malloc((k + 1) * sizeof(int));
    int* sell = malloc((k + 1) * sizeof(int));

    for (int i = 0; i <= k; i++) {
        buy[i] = -prices[0];
        sell[i] = 0;
    }

    for (size_t i = 1; i < n; i++) {
        for (int j = k; j >= 1; j--) {
            sell[j] = MAX(sell[j], buy[j] + prices[i]);
            buy[j] = MAX(buy[j], sell[j-1] - prices[i]);
        }
    }

    int result = sell[k];
    free(buy);
    free(sell);
    return result;
}

int dp_stock_buy_sell_with_cooldown(const int* prices, size_t n) {
    if (!prices || n < 2) return 0;

    int hold = -prices[0];  /* Max profit when holding a stock */
    int sold = 0;           /* Max profit on day we sold */
    int rest = 0;           /* Max profit when resting */

    for (size_t i = 1; i < n; i++) {
        int prev_sold = sold;
        sold = hold + prices[i];
        hold = MAX(hold, rest - prices[i]);
        rest = MAX(rest, prev_sold);
    }

    return MAX(sold, rest);
}

int dp_stock_buy_sell_with_fee(const int* prices, size_t n, int fee) {
    if (!prices || n < 2) return 0;

    int cash = 0;           /* Max profit without stock */
    int hold = -prices[0];  /* Max profit with stock */

    for (size_t i = 1; i < n; i++) {
        int prev_cash = cash;
        cash = MAX(cash, hold + prices[i] - fee);
        hold = MAX(hold, prev_cash - prices[i]);
    }

    return cash;
}

/* =========================== */
/*        Palindromes          */
/* =========================== */

int dp_palindrome_partitioning_min_cuts(const char* str) {
    if (!str) return 0;

    size_t n = strlen(str);
    if (n <= 1) return 0;

    /* Create palindrome table */
    bool** is_palindrome = malloc(n * sizeof(bool*));
    for (size_t i = 0; i < n; i++) {
        is_palindrome[i] = calloc(n, sizeof(bool));
        is_palindrome[i][i] = true;
    }

    /* Fill palindrome table */
    for (size_t len = 2; len <= n; len++) {
        for (size_t i = 0; i <= n - len; i++) {
            size_t j = i + len - 1;
            if (len == 2) {
                is_palindrome[i][j] = (str[i] == str[j]);
            } else {
                is_palindrome[i][j] = (str[i] == str[j]) && is_palindrome[i+1][j-1];
            }
        }
    }

    /* DP for minimum cuts */
    int* cuts = malloc(n * sizeof(int));

    for (size_t i = 0; i < n; i++) {
        if (is_palindrome[0][i]) {
            cuts[i] = 0;
        } else {
            cuts[i] = i;  /* Maximum cuts needed */
            for (size_t j = 1; j <= i; j++) {
                if (is_palindrome[j][i]) {
                    cuts[i] = MIN(cuts[i], cuts[j-1] + 1);
                }
            }
        }
    }

    int result = cuts[n-1];

    /* Free memory */
    for (size_t i = 0; i < n; i++) {
        free(is_palindrome[i]);
    }
    free(is_palindrome);
    free(cuts);

    return result;
}

/* =========================== */
/*    Optimization Problems    */
/* =========================== */

int dp_maximum_subarray(const int* arr, size_t n) {
    if (!arr || n == 0) return 0;

    int max_ending_here = arr[0];
    int max_so_far = arr[0];

    for (size_t i = 1; i < n; i++) {
        max_ending_here = MAX(arr[i], max_ending_here + arr[i]);
        max_so_far = MAX(max_so_far, max_ending_here);
    }

    return max_so_far;
}

int dp_maximum_product_subarray(const int* arr, size_t n) {
    if (!arr || n == 0) return 0;

    int max_product = arr[0];
    int min_ending = arr[0];
    int max_ending = arr[0];

    for (size_t i = 1; i < n; i++) {
        int temp = max_ending;
        max_ending = MAX(arr[i], MAX(max_ending * arr[i], min_ending * arr[i]));
        min_ending = MIN(arr[i], MIN(temp * arr[i], min_ending * arr[i]));
        max_product = MAX(max_product, max_ending);
    }

    return max_product;
}

int dp_house_robber(const int* nums, size_t n) {
    if (!nums || n == 0) return 0;
    if (n == 1) return nums[0];

    int prev2 = nums[0];
    int prev1 = MAX(nums[0], nums[1]);

    for (size_t i = 2; i < n; i++) {
        int current = MAX(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = current;
    }

    return prev1;
}

int dp_house_robber_circular(const int* nums, size_t n) {
    if (!nums || n == 0) return 0;
    if (n == 1) return nums[0];
    if (n == 2) return MAX(nums[0], nums[1]);

    /* Rob houses 0 to n-2 */
    int max1 = 0;
    int prev2 = nums[0];
    int prev1 = MAX(nums[0], nums[1]);

    for (size_t i = 2; i < n - 1; i++) {
        int current = MAX(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = current;
    }
    max1 = prev1;

    /* Rob houses 1 to n-1 */
    prev2 = nums[1];
    prev1 = MAX(nums[1], nums[2]);

    for (size_t i = 3; i < n; i++) {
        int current = MAX(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = current;
    }

    return MAX(max1, prev1);
}

/* =========================== */
/*      Utility Functions      */
/* =========================== */

void dp_result_free(dp_result_t* result) {
    if (result) {
        free(result->path);
        free(result);
    }
}

void dp_print_solution(const dp_result_t* result) {
    if (!result) {
        printf("No solution\n");
        return;
    }

    printf("Value: %lld\n", result->value);
    if (result->path && result->path_length > 0) {
        printf("Path: ");
        for (size_t i = 0; i < result->path_length; i++) {
            printf("%zu ", result->path[i]);
        }
        printf("\n");
    }
}

void dp_print_table(int** table, int rows, int cols) {
    if (!table) return;

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%4d ", table[i][j]);
        }
        printf("\n");
    }
}