/**
 * @file dynamic_programming.h
 * @brief Dynamic Programming algorithms and solutions
 */

#ifndef AM_DYNAMIC_PROGRAMMING_H
#define AM_DYNAMIC_PROGRAMMING_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Result structures */
typedef struct {
    int64_t value;
    size_t* path;
    size_t path_length;
} dp_result_t;

typedef struct {
    char* sequence;
    size_t length;
} lcs_result_t;

typedef struct {
    size_t* subset;
    size_t size;
    bool found;
} subset_result_t;

typedef struct {
    size_t* items;
    size_t count;
    int64_t total_value;
    int64_t total_weight;
} knapsack_result_t;

/* Classic DP problems */

/* Fibonacci and sequences */
int64_t dp_fibonacci(int n);
int64_t dp_fibonacci_memoized(int n);
int64_t dp_fibonacci_bottom_up(int n);
int64_t dp_tribonacci(int n);
int64_t dp_climbing_stairs(int n);
int64_t dp_climbing_stairs_k_steps(int n, int k);

/* Subset problems */
bool dp_subset_sum(const int* arr, size_t n, int target);
subset_result_t* dp_subset_sum_solution(const int* arr, size_t n, int target);
size_t dp_count_subsets_with_sum(const int* arr, size_t n, int target);
bool dp_partition_equal_subset(const int* arr, size_t n);
int dp_minimum_subset_sum_difference(const int* arr, size_t n);
void subset_result_free(subset_result_t* result);

/* Knapsack problems */
knapsack_result_t* dp_knapsack_01(const int* weights, const int* values, size_t n, int capacity);
int dp_knapsack_unbounded(const int* weights, const int* values, size_t n, int capacity);
int dp_knapsack_bounded(const int* weights, const int* values,
                        const int* quantities, size_t n, int capacity);
double dp_fractional_knapsack(const double* weights, const double* values,
                               size_t n, double capacity);
void knapsack_result_free(knapsack_result_t* result);

/* Longest subsequence problems */
size_t dp_longest_increasing_subsequence(const int* arr, size_t n, int** lis);
size_t dp_longest_decreasing_subsequence(const int* arr, size_t n, int** lds);
size_t dp_longest_bitonic_subsequence(const int* arr, size_t n);
size_t dp_longest_common_subsequence(const char* s1, const char* s2, char** lcs);
size_t dp_longest_palindromic_subsequence(const char* str, char** lps);
size_t dp_longest_repeating_subsequence(const char* str, char** lrs);
dp_result_t* dp_lis_nlogn(const int* arr, size_t n);

/* String DP problems */
size_t dp_edit_distance(const char* s1, const char* s2);
size_t dp_edit_distance_weighted(const char* s1, const char* s2,
                                  size_t insert_cost, size_t delete_cost,
                                  size_t replace_cost);
size_t dp_min_insertions_palindrome(const char* str);
size_t dp_min_deletions_palindrome(const char* str);
bool dp_string_interleaving(const char* s1, const char* s2, const char* s3);
size_t dp_distinct_subsequences(const char* str, const char* pattern);
bool dp_wildcard_matching(const char* str, const char* pattern);
bool dp_regular_expression_matching(const char* str, const char* pattern);

/* Coin change problems */
int dp_coin_change_min_coins(const int* coins, size_t n, int amount);
int dp_coin_change_count_ways(const int* coins, size_t n, int amount);
dp_result_t* dp_coin_change_solution(const int* coins, size_t n, int amount);

/* Matrix chain multiplication */
int dp_matrix_chain_multiplication(const int* dimensions, size_t n);
void dp_matrix_chain_order(const int* dimensions, size_t n,
                           int** optimal_order);

/* Tree DP problems */
int dp_max_path_sum_tree(void* root);
int dp_diameter_of_tree(void* root);
size_t dp_count_subtrees_with_sum(void* root, int target);
int dp_house_robber_tree(void* root);

/* Grid/Path DP problems */
int dp_unique_paths(int m, int n);
int dp_unique_paths_with_obstacles(int** grid, int m, int n);
int dp_min_path_sum(int** grid, int m, int n);
int dp_max_path_sum_triangle(int** triangle, int rows);
int dp_dungeon_game(int** dungeon, int m, int n);
int dp_cherry_pickup(int** grid, int n);
int dp_min_falling_path_sum(int** matrix, int m, int n);

/* Interval DP problems */
int dp_burst_balloons(const int* nums, size_t n);
int dp_palindrome_partitioning_min_cuts(const char* str);
bool dp_palindrome_partitioning_possible(const char* str, int k);
int dp_minimum_score_triangulation(const int* values, size_t n);

/* Stock problems */
int dp_stock_buy_sell_one_transaction(const int* prices, size_t n);
int dp_stock_buy_sell_unlimited(const int* prices, size_t n);
int dp_stock_buy_sell_k_transactions(const int* prices, size_t n, int k);
int dp_stock_buy_sell_with_cooldown(const int* prices, size_t n);
int dp_stock_buy_sell_with_fee(const int* prices, size_t n, int fee);

/* Game theory DP */
bool dp_can_win_nim(int n);
int dp_stone_game(const int* piles, size_t n);
bool dp_predict_the_winner(const int* nums, size_t n);

/* Digit DP */
int dp_count_digit_one(int n);
int dp_numbers_with_unique_digits(int n);
int dp_count_numbers_with_digit(int n, int digit);
int dp_sum_of_digits_in_range(int a, int b);

/* Probability DP */
double dp_knight_probability(int n, int k, int row, int col);
double dp_new_21_game(int n, int k, int max_pts);

/* Optimization DP */
int dp_maximum_subarray(const int* arr, size_t n);
int dp_maximum_product_subarray(const int* arr, size_t n);
int dp_house_robber(const int* nums, size_t n);
int dp_house_robber_circular(const int* nums, size_t n);
int dp_egg_drop(int eggs, int floors);
int dp_super_egg_drop(int eggs, int floors);
int dp_minimum_cost_tickets(const int* days, size_t n,
                             const int* costs, size_t cost_count);

/* Utility Functions */
void dp_result_free(dp_result_t* result);
void lcs_result_free(lcs_result_t* result);
void dp_print_solution(const dp_result_t* result);
void dp_print_table(int** table, int rows, int cols);

/* Memory optimization techniques */
int64_t dp_space_optimized_lcs(const char* s1, const char* s2);
int dp_space_optimized_knapsack(const int* weights, const int* values,
                                 size_t n, int capacity);

/* Memoization utilities */
typedef struct memo_table memo_table_t;

memo_table_t* memo_create(size_t dimensions, ...);
void memo_destroy(memo_table_t* table);
bool memo_has(memo_table_t* table, ...);
int64_t memo_get(memo_table_t* table, ...);
void memo_set(memo_table_t* table, int64_t value, ...);

#ifdef __cplusplus
}
#endif

#endif /* AM_DYNAMIC_PROGRAMMING_H */