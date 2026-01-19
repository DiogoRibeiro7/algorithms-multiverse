/**
 * @file sorting.c
 * @brief Implementation of sorting algorithms
 */

#include "sorting.h"
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <omp.h>

/* Helper function to swap two integers */
static inline void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

/* Helper function for generic swap */
static void swap_generic(void* a, void* b, size_t size) {
    char* temp = malloc(size);
    memcpy(temp, a, size);
    memcpy(a, b, size);
    memcpy(b, temp, size);
    free(temp);
}

/* Bubble Sort */
void bubble_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    for (size_t i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (size_t j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(&arr[j], &arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

/* Insertion Sort */
void insertion_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    for (size_t i = 1; i < n; i++) {
        int key = arr[i];
        size_t j = i;
        while (j > 0 && arr[j - 1] > key) {
            arr[j] = arr[j - 1];
            j--;
        }
        arr[j] = key;
    }
}

/* Selection Sort */
void selection_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    for (size_t i = 0; i < n - 1; i++) {
        size_t min_idx = i;
        for (size_t j = i + 1; j < n; j++) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }
        if (min_idx != i) {
            swap(&arr[i], &arr[min_idx]);
        }
    }
}

/* Merge Sort helper - merge two sorted subarrays */
static void merge(int* arr, size_t left, size_t mid, size_t right) {
    size_t n1 = mid - left + 1;
    size_t n2 = right - mid;

    int* L = malloc(n1 * sizeof(int));
    int* R = malloc(n2 * sizeof(int));

    for (size_t i = 0; i < n1; i++) {
        L[i] = arr[left + i];
    }
    for (size_t j = 0; j < n2; j++) {
        R[j] = arr[mid + 1 + j];
    }

    size_t i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
        }
    }

    while (i < n1) {
        arr[k++] = L[i++];
    }
    while (j < n2) {
        arr[k++] = R[j++];
    }

    free(L);
    free(R);
}

/* Merge Sort recursive helper */
static void merge_sort_recursive(int* arr, size_t left, size_t right) {
    if (left < right) {
        size_t mid = left + (right - left) / 2;
        merge_sort_recursive(arr, left, mid);
        merge_sort_recursive(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

/* Merge Sort */
void merge_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;
    merge_sort_recursive(arr, 0, n - 1);
}

/* Quick Sort partition */
static size_t partition(int* arr, size_t low, size_t high) {
    int pivot = arr[high];
    size_t i = low;

    for (size_t j = low; j < high; j++) {
        if (arr[j] < pivot) {
            swap(&arr[i], &arr[j]);
            i++;
        }
    }
    swap(&arr[i], &arr[high]);
    return i;
}

/* Quick Sort recursive helper */
static void quick_sort_recursive(int* arr, size_t low, size_t high) {
    if (low < high) {
        size_t pi = partition(arr, low, high);
        if (pi > 0) {
            quick_sort_recursive(arr, low, pi - 1);
        }
        quick_sort_recursive(arr, pi + 1, high);
    }
}

/* Quick Sort */
void quick_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;
    quick_sort_recursive(arr, 0, n - 1);
}

/* Heap Sort helper - heapify */
static void heapify(int* arr, size_t n, size_t i) {
    size_t largest = i;
    size_t left = 2 * i + 1;
    size_t right = 2 * i + 2;

    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }
    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }

    if (largest != i) {
        swap(&arr[i], &arr[largest]);
        heapify(arr, n, largest);
    }
}

/* Heap Sort */
void heap_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    /* Build heap */
    for (size_t i = n / 2; i > 0; i--) {
        heapify(arr, n, i - 1);
    }

    /* Extract elements from heap */
    for (size_t i = n - 1; i > 0; i--) {
        swap(&arr[0], &arr[i]);
        heapify(arr, i, 0);
    }
}

/* Shell Sort */
void shell_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    /* Start with large gap, reduce by half each iteration */
    for (size_t gap = n / 2; gap > 0; gap /= 2) {
        /* Do gapped insertion sort */
        for (size_t i = gap; i < n; i++) {
            int temp = arr[i];
            size_t j = i;
            while (j >= gap && arr[j - gap] > temp) {
                arr[j] = arr[j - gap];
                j -= gap;
            }
            arr[j] = temp;
        }
    }
}

/* Radix Sort helper - get max value */
static int get_max(int* arr, size_t n) {
    int max = arr[0];
    for (size_t i = 1; i < n; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

/* Radix Sort helper - counting sort for specific digit */
static void counting_sort_radix(int* arr, size_t n, int exp) {
    int* output = malloc(n * sizeof(int));
    int count[10] = {0};

    /* Count occurrences */
    for (size_t i = 0; i < n; i++) {
        count[(arr[i] / exp) % 10]++;
    }

    /* Cumulative count */
    for (int i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }

    /* Build output array */
    for (size_t i = n; i > 0; i--) {
        int digit = (arr[i - 1] / exp) % 10;
        output[count[digit] - 1] = arr[i - 1];
        count[digit]--;
    }

    /* Copy output to arr */
    memcpy(arr, output, n * sizeof(int));
    free(output);
}

/* Radix Sort */
void radix_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    int max = get_max(arr, n);

    /* Do counting sort for every digit */
    for (int exp = 1; max / exp > 0; exp *= 10) {
        counting_sort_radix(arr, n, exp);
    }
}

/* Counting Sort */
void counting_sort(int* arr, size_t n, int max_val) {
    if (!arr || n <= 1 || max_val < 0) return;

    int* count = calloc(max_val + 1, sizeof(int));
    int* output = malloc(n * sizeof(int));

    /* Count occurrences */
    for (size_t i = 0; i < n; i++) {
        if (arr[i] >= 0 && arr[i] <= max_val) {
            count[arr[i]]++;
        }
    }

    /* Cumulative count */
    for (int i = 1; i <= max_val; i++) {
        count[i] += count[i - 1];
    }

    /* Build output array */
    for (size_t i = n; i > 0; i--) {
        if (arr[i - 1] >= 0 && arr[i - 1] <= max_val) {
            output[count[arr[i - 1]] - 1] = arr[i - 1];
            count[arr[i - 1]]--;
        }
    }

    /* Copy output to arr */
    memcpy(arr, output, n * sizeof(int));

    free(count);
    free(output);
}

/* Bucket Sort */
void bucket_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    /* Find min and max */
    int min = arr[0], max = arr[0];
    for (size_t i = 1; i < n; i++) {
        if (arr[i] < min) min = arr[i];
        if (arr[i] > max) max = arr[i];
    }

    /* Number of buckets */
    size_t bucket_count = n;
    int range = max - min + 1;

    /* Create buckets */
    int** buckets = calloc(bucket_count, sizeof(int*));
    size_t* bucket_sizes = calloc(bucket_count, sizeof(size_t));
    size_t* bucket_capacities = calloc(bucket_count, sizeof(size_t));

    /* Initialize buckets */
    for (size_t i = 0; i < bucket_count; i++) {
        bucket_capacities[i] = 10;
        buckets[i] = malloc(bucket_capacities[i] * sizeof(int));
    }

    /* Distribute elements into buckets */
    for (size_t i = 0; i < n; i++) {
        size_t bucket_idx = (size_t)((arr[i] - min) * bucket_count / range);
        if (bucket_idx >= bucket_count) bucket_idx = bucket_count - 1;

        /* Expand bucket if needed */
        if (bucket_sizes[bucket_idx] == bucket_capacities[bucket_idx]) {
            bucket_capacities[bucket_idx] *= 2;
            buckets[bucket_idx] = realloc(buckets[bucket_idx],
                                         bucket_capacities[bucket_idx] * sizeof(int));
        }

        buckets[bucket_idx][bucket_sizes[bucket_idx]++] = arr[i];
    }

    /* Sort individual buckets and concatenate */
    size_t index = 0;
    for (size_t i = 0; i < bucket_count; i++) {
        if (bucket_sizes[i] > 0) {
            insertion_sort(buckets[i], bucket_sizes[i]);
            for (size_t j = 0; j < bucket_sizes[i]; j++) {
                arr[index++] = buckets[i][j];
            }
        }
        free(buckets[i]);
    }

    free(buckets);
    free(bucket_sizes);
    free(bucket_capacities);
}

/* Tim Sort - simplified implementation */
static const size_t MIN_MERGE = 32;

static void insertion_sort_tim(int* arr, size_t left, size_t right) {
    for (size_t i = left + 1; i <= right; i++) {
        int key = arr[i];
        size_t j = i;
        while (j > left && arr[j - 1] > key) {
            arr[j] = arr[j - 1];
            j--;
        }
        arr[j] = key;
    }
}

void tim_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    /* Sort individual runs using insertion sort */
    for (size_t i = 0; i < n; i += MIN_MERGE) {
        size_t end = (i + MIN_MERGE - 1 < n - 1) ? i + MIN_MERGE - 1 : n - 1;
        insertion_sort_tim(arr, i, end);
    }

    /* Merge runs */
    for (size_t size = MIN_MERGE; size < n; size *= 2) {
        for (size_t left = 0; left < n; left += size * 2) {
            size_t mid = left + size - 1;
            size_t right = (left + size * 2 - 1 < n - 1) ? left + size * 2 - 1 : n - 1;

            if (mid < right) {
                merge(arr, left, mid, right);
            }
        }
    }
}

/* Intro Sort - combination of quicksort, heapsort, and insertion sort */
static void intro_sort_recursive(int* arr, size_t low, size_t high, size_t depth_limit) {
    size_t size = high - low + 1;

    if (size <= 16) {
        /* Use insertion sort for small arrays */
        insertion_sort_tim(arr, low, high);
        return;
    }

    if (depth_limit == 0) {
        /* Use heapsort if recursion depth is too high */
        heap_sort(arr + low, size);
        return;
    }

    /* Use quicksort */
    size_t pivot = partition(arr, low, high);
    if (pivot > 0 && pivot > low) {
        intro_sort_recursive(arr, low, pivot - 1, depth_limit - 1);
    }
    intro_sort_recursive(arr, pivot + 1, high, depth_limit - 1);
}

void intro_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    /* Calculate depth limit (2 * log2(n)) */
    size_t depth_limit = 0;
    size_t temp = n;
    while (temp > 0) {
        depth_limit++;
        temp >>= 1;
    }
    depth_limit *= 2;

    intro_sort_recursive(arr, 0, n - 1, depth_limit);
}

/* Comb Sort */
void comb_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    size_t gap = n;
    const double shrink = 1.3;
    bool swapped = true;

    while (gap > 1 || swapped) {
        gap = (size_t)(gap / shrink);
        if (gap < 1) gap = 1;

        swapped = false;
        for (size_t i = 0; i + gap < n; i++) {
            if (arr[i] > arr[i + gap]) {
                swap(&arr[i], &arr[i + gap]);
                swapped = true;
            }
        }
    }
}

/* Gnome Sort */
void gnome_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    size_t index = 0;
    while (index < n) {
        if (index == 0 || arr[index] >= arr[index - 1]) {
            index++;
        } else {
            swap(&arr[index], &arr[index - 1]);
            index--;
        }
    }
}

/* Cocktail Sort (Bidirectional Bubble Sort) */
void cocktail_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    bool swapped = true;
    size_t start = 0;
    size_t end = n - 1;

    while (swapped) {
        swapped = false;

        /* Forward pass */
        for (size_t i = start; i < end; i++) {
            if (arr[i] > arr[i + 1]) {
                swap(&arr[i], &arr[i + 1]);
                swapped = true;
            }
        }

        if (!swapped) break;

        end--;
        swapped = false;

        /* Backward pass */
        for (size_t i = end; i > start; i--) {
            if (arr[i] < arr[i - 1]) {
                swap(&arr[i], &arr[i - 1]);
                swapped = true;
            }
        }

        start++;
    }
}

/* Generic sorting with comparator */
void bubble_sort_generic(void* arr, size_t n, size_t elem_size,
                         int (*compare)(const void*, const void*)) {
    if (!arr || n <= 1 || !compare) return;

    char* array = (char*)arr;
    for (size_t i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (size_t j = 0; j < n - i - 1; j++) {
            if (compare(array + j * elem_size, array + (j + 1) * elem_size) > 0) {
                swap_generic(array + j * elem_size, array + (j + 1) * elem_size, elem_size);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

/* Parallel merge sort using OpenMP */
void parallel_merge_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    #ifdef _OPENMP
    #pragma omp parallel
    {
        #pragma omp single nowait
        {
            merge_sort_recursive(arr, 0, n - 1);
        }
    }
    #else
    merge_sort(arr, n);
    #endif
}

/* Parallel quick sort using OpenMP */
static void parallel_quick_sort_recursive(int* arr, size_t low, size_t high, int depth) {
    if (low < high) {
        size_t pi = partition(arr, low, high);

        #ifdef _OPENMP
        if (depth > 0) {
            #pragma omp task
            {
                if (pi > 0) {
                    parallel_quick_sort_recursive(arr, low, pi - 1, depth - 1);
                }
            }
            #pragma omp task
            {
                parallel_quick_sort_recursive(arr, pi + 1, high, depth - 1);
            }
        } else {
            if (pi > 0) {
                quick_sort_recursive(arr, low, pi - 1);
            }
            quick_sort_recursive(arr, pi + 1, high);
        }
        #else
        if (pi > 0) {
            quick_sort_recursive(arr, low, pi - 1);
        }
        quick_sort_recursive(arr, pi + 1, high);
        #endif
    }
}

void parallel_quick_sort(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    #ifdef _OPENMP
    int depth = 4;  /* Limit parallel depth */
    #pragma omp parallel
    {
        #pragma omp single nowait
        {
            parallel_quick_sort_recursive(arr, 0, n - 1, depth);
        }
    }
    #else
    quick_sort(arr, n);
    #endif
}

/* Utility functions */
bool is_sorted(const int* arr, size_t n) {
    if (!arr || n <= 1) return true;

    for (size_t i = 1; i < n; i++) {
        if (arr[i] < arr[i - 1]) {
            return false;
        }
    }
    return true;
}

bool is_sorted_generic(const void* arr, size_t n, size_t elem_size,
                       int (*compare)(const void*, const void*)) {
    if (!arr || n <= 1 || !compare) return true;

    const char* array = (const char*)arr;
    for (size_t i = 1; i < n; i++) {
        if (compare(array + i * elem_size, array + (i - 1) * elem_size) < 0) {
            return false;
        }
    }
    return true;
}

void shuffle_array(int* arr, size_t n) {
    if (!arr || n <= 1) return;

    srand(time(NULL));
    for (size_t i = n - 1; i > 0; i--) {
        size_t j = rand() % (i + 1);
        swap(&arr[i], &arr[j]);
    }
}

int* generate_random_array(size_t n, int min_val, int max_val) {
    if (n == 0 || max_val < min_val) return NULL;

    int* arr = malloc(n * sizeof(int));
    if (!arr) return NULL;

    srand(time(NULL));
    int range = max_val - min_val + 1;

    for (size_t i = 0; i < n; i++) {
        arr[i] = min_val + (rand() % range);
    }

    return arr;
}

/* Benchmark function */
sort_stats_t benchmark_sort(sort_algorithm_t algo, int* arr, size_t n) {
    sort_stats_t stats = {0};
    if (!arr || n == 0) return stats;

    /* Create a copy for sorting */
    int* temp = malloc(n * sizeof(int));
    memcpy(temp, arr, n * sizeof(int));

    /* Start timing */
    clock_t start = clock();

    /* Run the selected algorithm */
    switch (algo) {
        case SORT_BUBBLE:
            bubble_sort(temp, n);
            break;
        case SORT_INSERTION:
            insertion_sort(temp, n);
            break;
        case SORT_SELECTION:
            selection_sort(temp, n);
            break;
        case SORT_MERGE:
            merge_sort(temp, n);
            break;
        case SORT_QUICK:
            quick_sort(temp, n);
            break;
        case SORT_HEAP:
            heap_sort(temp, n);
            break;
        case SORT_SHELL:
            shell_sort(temp, n);
            break;
        case SORT_RADIX:
            radix_sort(temp, n);
            break;
        case SORT_COUNTING:
            counting_sort(temp, n, get_max(temp, n));
            break;
        case SORT_BUCKET:
            bucket_sort(temp, n);
            break;
        case SORT_TIM:
            tim_sort(temp, n);
            break;
        case SORT_INTRO:
            intro_sort(temp, n);
            break;
        case SORT_COMB:
            comb_sort(temp, n);
            break;
        case SORT_GNOME:
            gnome_sort(temp, n);
            break;
        case SORT_COCKTAIL:
            cocktail_sort(temp, n);
            break;
    }

    /* End timing */
    clock_t end = clock();
    stats.time_ms = ((double)(end - start) / CLOCKS_PER_SEC) * 1000.0;
    stats.memory_used = n * sizeof(int);

    free(temp);
    return stats;
}