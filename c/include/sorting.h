/**
 * @file sorting.h
 * @brief Sorting algorithms interface
 */

#ifndef AM_SORTING_H
#define AM_SORTING_H

#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Sorting algorithm types */
typedef enum {
    SORT_BUBBLE,
    SORT_INSERTION,
    SORT_SELECTION,
    SORT_MERGE,
    SORT_QUICK,
    SORT_HEAP,
    SORT_SHELL,
    SORT_RADIX,
    SORT_COUNTING,
    SORT_BUCKET,
    SORT_TIM,
    SORT_INTRO,
    SORT_COMB,
    SORT_GNOME,
    SORT_COCKTAIL
} sort_algorithm_t;

/* Sorting functions for integer arrays */

void bubble_sort(int* arr, size_t n);
void insertion_sort(int* arr, size_t n);
void selection_sort(int* arr, size_t n);
void merge_sort(int* arr, size_t n);
void quick_sort(int* arr, size_t n);
void heap_sort(int* arr, size_t n);
void shell_sort(int* arr, size_t n);
void radix_sort(int* arr, size_t n);
void counting_sort(int* arr, size_t n, int max_val);
void bucket_sort(int* arr, size_t n);
void tim_sort(int* arr, size_t n);
void intro_sort(int* arr, size_t n);
void comb_sort(int* arr, size_t n);
void gnome_sort(int* arr, size_t n);
void cocktail_sort(int* arr, size_t n);

/* Generic sorting with comparator */
void bubble_sort_generic(void* arr, size_t n, size_t elem_size,
                         int (*compare)(const void*, const void*));
void merge_sort_generic(void* arr, size_t n, size_t elem_size,
                        int (*compare)(const void*, const void*));
void quick_sort_generic(void* arr, size_t n, size_t elem_size,
                        int (*compare)(const void*, const void*));

/* Parallel sorting (requires OpenMP) */
void parallel_merge_sort(int* arr, size_t n);
void parallel_quick_sort(int* arr, size_t n);

/* Utility functions */
bool is_sorted(const int* arr, size_t n);
bool is_sorted_generic(const void* arr, size_t n, size_t elem_size,
                       int (*compare)(const void*, const void*));
void shuffle_array(int* arr, size_t n);
int* generate_random_array(size_t n, int min_val, int max_val);

/* Benchmark functions */
typedef struct {
    double time_ms;
    size_t comparisons;
    size_t swaps;
    size_t memory_used;
} sort_stats_t;

sort_stats_t benchmark_sort(sort_algorithm_t algo, int* arr, size_t n);
void print_sort_stats(const sort_stats_t* stats);

#ifdef __cplusplus
}
#endif

#endif /* AM_SORTING_H */