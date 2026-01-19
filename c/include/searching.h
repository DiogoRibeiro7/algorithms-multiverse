/**
 * @file searching.h
 * @brief Searching algorithms interface
 */

#ifndef AM_SEARCHING_H
#define AM_SEARCHING_H

#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Search result structure */
typedef struct {
    bool found;
    size_t index;
    size_t comparisons;
} search_result_t;

/* Linear search algorithms */
search_result_t linear_search(const int* arr, size_t n, int target);
search_result_t linear_search_generic(const void* arr, size_t n, size_t elem_size,
                                      const void* target,
                                      int (*compare)(const void*, const void*));

/* Binary search algorithms */
search_result_t binary_search(const int* arr, size_t n, int target);
search_result_t binary_search_recursive(const int* arr, size_t n, int target);
search_result_t binary_search_generic(const void* arr, size_t n, size_t elem_size,
                                      const void* target,
                                      int (*compare)(const void*, const void*));

/* Advanced search algorithms */
search_result_t jump_search(const int* arr, size_t n, int target);
search_result_t interpolation_search(const int* arr, size_t n, int target);
search_result_t exponential_search(const int* arr, size_t n, int target);
search_result_t fibonacci_search(const int* arr, size_t n, int target);
search_result_t ternary_search(const int* arr, size_t n, int target);

/* Finding specific elements */
int find_min(const int* arr, size_t n);
int find_max(const int* arr, size_t n);
int find_kth_smallest(int* arr, size_t n, size_t k);
int find_kth_largest(int* arr, size_t n, size_t k);
int find_median(int* arr, size_t n);

/* Range queries */
size_t lower_bound(const int* arr, size_t n, int value);
size_t upper_bound(const int* arr, size_t n, int value);
void equal_range(const int* arr, size_t n, int value, size_t* lower, size_t* upper);
size_t count_occurrences(const int* arr, size_t n, int value);

/* Peak finding */
size_t find_peak_1d(const int* arr, size_t n);
void find_peak_2d(const int** matrix, size_t rows, size_t cols,
                  size_t* peak_row, size_t* peak_col);

/* Majority element */
int find_majority_element(const int* arr, size_t n, bool* has_majority);

/* Two-pointer techniques */
bool two_sum(const int* arr, size_t n, int target, size_t* idx1, size_t* idx2);
bool three_sum(const int* arr, size_t n, int target,
                size_t* idx1, size_t* idx2, size_t* idx3);

#ifdef __cplusplus
}
#endif

#endif /* AM_SEARCHING_H */