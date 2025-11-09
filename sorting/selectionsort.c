/**
 * Selection Sort Algorithm - Educational Implementation (C)
 *
 * ALGORITHM OVERVIEW:
 * ==================
 * Selection Sort works by repeatedly finding the minimum element from the unsorted
 * portion of the array and placing it at the beginning. It divides the array into
 * two parts: a sorted portion (left) and an unsorted portion (right).
 *
 * Time Complexity:
 * - Best Case: O(n²) - Even if array is already sorted, still searches for minimum
 * - Average Case: O(n²)
 * - Worst Case: O(n²)
 * - IMPORTANT: Unlike bubble sort and insertion sort, selection sort ALWAYS performs
 *   O(n²) comparisons, regardless of input
 *
 * Space Complexity: O(1) - Sorts in-place with only constant extra space
 *
 * Stability: NOT stable by default (can be made stable with modifications)
 * In-place: YES
 *
 * KEY ADVANTAGE: Makes MINIMUM number of swaps - only O(n) swaps!
 * This is critical when writing to memory is expensive (flash, EEPROM, etc.)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>

// ============================================================================
// UTILITY MACROS AND TYPES
// ============================================================================

#define SWAP(a, b, type) do { type temp = a; a = b; b = temp; } while(0)
#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define MAX(a, b) ((a) > (b) ? (a) : (b))

/**
 * Structure to track sorting operation statistics
 */
typedef struct {
    int comparisons;
    int swaps;
    int array_accesses;
} SortStatistics;

/**
 * Function pointer type for comparison function
 */
typedef int (*CompareFunc)(const void*, const void*);

// ============================================================================
// STANDARD SELECTION SORT
// ============================================================================

/**
 * Standard selection sort implementation for integer arrays.
 *
 * ALGORITHM STEPS:
 * ===============
 * 1. Find the minimum element in the unsorted portion
 * 2. Swap it with the first element of the unsorted portion
 * 3. Move the boundary of sorted/unsorted portions one element to the right
 * 4. Repeat until the entire array is sorted
 *
 * Visual Example:
 * ==============
 * Initial: [64, 25, 12, 22, 11]
 *
 * Pass 1: Find min in [64, 25, 12, 22, 11] → 11
 *         Swap 64 ↔ 11
 *         Result: [11, 25, 12, 22, 64]
 *                  ^^^ sorted portion
 *
 * Pass 2: Find min in [25, 12, 22, 64] → 12
 *         Swap 25 ↔ 12
 *         Result: [11, 12, 25, 22, 64]
 *                  ^^^^^^^ sorted portion
 *
 * Pass 3: Find min in [25, 22, 64] → 22
 *         Swap 25 ↔ 22
 *         Result: [11, 12, 22, 25, 64]
 *                  ^^^^^^^^^^^ sorted portion
 *
 * Pass 4: Find min in [25, 64] → 25
 *         No swap needed
 *         Result: [11, 12, 22, 25, 64]
 *                  ^^^^^^^^^^^^^^^ sorted portion
 *
 * @param arr Array to sort (modified in-place)
 * @param n Size of the array
 *
 * Time: O(n²), Space: O(1)
 */
void selection_sort(int arr[], int n) {
    /* Outer loop: Move boundary of unsorted subarray one by one */
    for (int i = 0; i < n - 1; i++) {
        /* Find the minimum element in the remaining unsorted array
         * Start by assuming the first unsorted element is the minimum */
        int min_idx = i;

        /* Inner loop: Search for the minimum in arr[i+1...n-1] */
        for (int j = i + 1; j < n; j++) {
            /* If we find a smaller element, update min_idx */
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }

        /* Swap the found minimum element with the first element
         * of the unsorted portion */
        if (min_idx != i) {
            SWAP(arr[i], arr[min_idx], int);
        }
    }
}

/**
 * Selection sort for an array that will be allocated and returned.
 * Original array is not modified.
 *
 * @param arr Original array
 * @param n Size of the array
 * @return Pointer to new sorted array (caller must free)
 */
int* selection_sort_copy(const int arr[], int n) {
    int* result = (int*)malloc(n * sizeof(int));
    if (result == NULL) {
        return NULL;
    }

    memcpy(result, arr, n * sizeof(int));
    selection_sort(result, n);
    return result;
}

// ============================================================================
// BIDIRECTIONAL SELECTION SORT
// ============================================================================

/**
 * Bidirectional selection sort (also called "double selection sort").
 *
 * OPTIMIZATION:
 * ============
 * Instead of finding just the minimum in each pass, we find BOTH the minimum
 * and maximum elements. We place the minimum at the beginning and the maximum
 * at the end, reducing the number of passes by approximately half.
 *
 * Algorithm:
 * - Find both min and max in the unsorted portion
 * - Place min at the left boundary
 * - Place max at the right boundary
 * - Move both boundaries inward
 *
 * Visual Example:
 * ==============
 * Initial: [64, 25, 12, 22, 11, 90, 88]
 *
 * Pass 1: Find min=11, max=90 in [64, 25, 12, 22, 11, 90, 88]
 *         Swap: 64 ↔ 11 (min to front), 90 stays
 *         Result: [11, 25, 12, 22, 64, 88, 90]
 *                  ^^                      ^^ sorted
 *
 * Pass 2: Find min=12, max=88 in [25, 12, 22, 64, 88]
 *         Swap: 25 ↔ 12 (min to front), 88 stays
 *         Result: [11, 12, 22, 25, 64, 88, 90]
 *                  ^^^^^^              ^^^^^^ sorted
 *
 * Time: Still O(n²), but approximately 2x faster in practice
 * Space: O(1)
 *
 * @param arr Array to sort (modified in-place)
 * @param n Size of the array
 */
void bidirectional_selection_sort(int arr[], int n) {
    int left = 0;
    int right = n - 1;

    while (left < right) {
        /* Find both minimum and maximum in the current range */
        int min_idx = left;
        int max_idx = left;

        for (int i = left; i <= right; i++) {
            if (arr[i] < arr[min_idx]) {
                min_idx = i;
            }
            if (arr[i] > arr[max_idx]) {
                max_idx = i;
            }
        }

        /* Handle special case: if min is at right position */
        if (min_idx == right) {
            SWAP(arr[left], arr[right], int);
            if (max_idx == left) {
                max_idx = right;
            }
        } else {
            /* Swap minimum to the left boundary */
            if (min_idx != left) {
                SWAP(arr[left], arr[min_idx], int);
            }

            /* If maximum was at left position, it's now at min_idx */
            if (max_idx == left) {
                max_idx = min_idx;
            }

            /* Swap maximum to the right boundary */
            if (max_idx != right) {
                SWAP(arr[right], arr[max_idx], int);
            }
        }

        /* Move boundaries inward */
        left++;
        right--;
    }
}

// ============================================================================
// RECURSIVE SELECTION SORT
// ============================================================================

/**
 * Helper function for recursive selection sort.
 *
 * @param arr Array to sort
 * @param start_idx Starting index for current recursion
 * @param n Size of the array
 */
static void selection_sort_recursive_helper(int arr[], int start_idx, int n) {
    /* Base case: if we've reached the end, we're done */
    if (start_idx >= n - 1) {
        return;
    }

    /* Find the minimum element in arr[start_idx...n-1] */
    int min_idx = start_idx;
    for (int i = start_idx + 1; i < n; i++) {
        if (arr[i] < arr[min_idx]) {
            min_idx = i;
        }
    }

    /* Swap the minimum with the element at start_idx */
    if (min_idx != start_idx) {
        SWAP(arr[start_idx], arr[min_idx], int);
    }

    /* Recursively sort the rest */
    selection_sort_recursive_helper(arr, start_idx + 1, n);
}

/**
 * Recursive implementation of selection sort.
 *
 * RECURSIVE APPROACH:
 * ==================
 * Base case: Array of size 0 or 1 is already sorted
 * Recursive case:
 *     1. Find the minimum element in the array
 *     2. Swap it with the first element
 *     3. Recursively sort the rest of the array (excluding the first element)
 *
 * Example:
 * ========
 * selection_sort_recursive([64, 25, 12, 22, 11])
 *     → Find min=11, swap with 64
 *     → [11] + selection_sort_recursive([25, 12, 22, 64])
 *         → Find min=12, swap with 25
 *         → [11, 12] + selection_sort_recursive([25, 22, 64])
 *             → ...continues recursively...
 *
 * Time: O(n²), Space: O(n) for recursion stack
 *
 * @param arr Array to sort (modified in-place)
 * @param n Size of the array
 */
void selection_sort_recursive(int arr[], int n) {
    selection_sort_recursive_helper(arr, 0, n);
}

// ============================================================================
// STABLE SELECTION SORT
// ============================================================================

/**
 * Stable version of selection sort.
 *
 * WHY STANDARD SELECTION SORT IS UNSTABLE:
 * ========================================
 * When we swap the minimum element with the first element of the unsorted
 * portion, we can change the relative order of equal elements.
 *
 * Example showing instability:
 * Input:  [4a, 5, 3, 2, 4b]  (a and b are just markers, both are 4)
 * Pass 1: Find min=2, swap with 4a → [2, 5, 3, 4a, 4b]
 * ...
 * Result might have 4b before 4a (unstable)
 *
 * MAKING IT STABLE:
 * ================
 * Instead of swapping, we shift all elements and insert the minimum
 * at the correct position. This preserves the relative order.
 *
 * Time: O(n²) comparisons + O(n²) shifts
 * Space: O(1)
 *
 * @param arr Array to sort (modified in-place)
 * @param n Size of the array
 */
void stable_selection_sort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        /* Find minimum in unsorted portion */
        int min_idx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }

        /* Instead of swapping, shift elements and insert */
        if (min_idx != i) {
            int min_value = arr[min_idx];

            /* Shift all elements between i and min_idx one position right */
            for (int k = min_idx; k > i; k--) {
                arr[k] = arr[k - 1];
            }

            /* Place minimum at position i */
            arr[i] = min_value;
        }
    }
}

// ============================================================================
// VISUALIZATION AND STATISTICS
// ============================================================================

/**
 * Reset sort statistics to zero.
 */
void reset_stats(SortStatistics* stats) {
    stats->comparisons = 0;
    stats->swaps = 0;
    stats->array_accesses = 0;
}

/**
 * Selection sort with operation counting.
 *
 * @param arr Array to sort (modified in-place)
 * @param n Size of the array
 * @param stats Pointer to statistics structure
 */
void selection_sort_with_stats(int arr[], int n, SortStatistics* stats) {
    reset_stats(stats);

    for (int i = 0; i < n - 1; i++) {
        int min_idx = i;
        stats->array_accesses++;

        for (int j = i + 1; j < n; j++) {
            stats->comparisons++;
            stats->array_accesses += 2;  /* Read arr[j] and arr[min_idx] */
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }

        if (min_idx != i) {
            stats->swaps++;
            stats->array_accesses += 4;  /* Two reads, two writes */
            SWAP(arr[i], arr[min_idx], int);
        }
    }
}

/**
 * Print array to console.
 */
void print_array(const int arr[], int n, const char* label) {
    printf("%s: [", label);
    for (int i = 0; i < n; i++) {
        printf("%d", arr[i]);
        if (i < n - 1) printf(", ");
    }
    printf("]\n");
}

/**
 * Create ASCII visualization of selection sort process.
 *
 * Shows each step with visual markers for:
 * - Sorted portion
 * - Current minimum being found
 * - Element being compared
 */
void visualize_selection_sort(const int arr[], int n) {
    /* Make a copy to sort */
    int* result = (int*)malloc(n * sizeof(int));
    memcpy(result, arr, n * sizeof(int));

    printf("======================================================================\n");
    printf("SELECTION SORT VISUALIZATION\n");
    printf("======================================================================\n");
    print_array(result, n, "Initial array");
    printf("\n");

    for (int i = 0; i < n - 1; i++) {
        printf("Pass %d:\n", i + 1);
        printf("  Looking for minimum in unsorted portion: [");
        for (int k = i; k < n; k++) {
            printf("%d", result[k]);
            if (k < n - 1) printf(", ");
        }
        printf("]\n");

        int min_idx = i;
        int min_value = result[i];

        /* Show the search process */
        for (int j = i + 1; j < n; j++) {
            if (result[j] < min_value) {
                min_idx = j;
                min_value = result[j];
                printf("    Found new minimum: %d at index %d\n", min_value, min_idx);
            }
        }

        /* Show the swap */
        if (min_idx != i) {
            printf("  Swapping %d ↔ %d\n", result[i], result[min_idx]);
            SWAP(result[i], result[min_idx], int);
        } else {
            printf("  No swap needed (minimum already in place)\n");
        }

        /* Show current state */
        printf("  Sorted: [");
        for (int k = 0; k <= i; k++) {
            printf("%d", result[k]);
            if (k < i) printf(", ");
        }
        printf("] | Unsorted: [");
        for (int k = i + 1; k < n; k++) {
            printf("%d", result[k]);
            if (k < n - 1) printf(", ");
        }
        printf("]\n\n");
    }

    print_array(result, n, "Final sorted array");
    printf("======================================================================\n");

    free(result);
}

/**
 * Check if an array is sorted in ascending order.
 */
bool is_sorted(const int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            return false;
        }
    }
    return true;
}

// ============================================================================
// COMPARISON WITH OTHER O(n²) ALGORITHMS
// ============================================================================

/**
 * Bubble sort with statistics (for comparison).
 */
void bubble_sort_with_stats(int arr[], int n, SortStatistics* stats) {
    reset_stats(stats);

    for (int i = 0; i < n; i++) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            stats->comparisons++;
            stats->array_accesses += 2;
            if (arr[j] > arr[j + 1]) {
                stats->swaps++;
                stats->array_accesses += 4;
                SWAP(arr[j], arr[j + 1], int);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

/**
 * Insertion sort with statistics (for comparison).
 */
void insertion_sort_with_stats(int arr[], int n, SortStatistics* stats) {
    reset_stats(stats);

    for (int i = 1; i < n; i++) {
        int key = arr[i];
        stats->array_accesses++;
        int j = i - 1;

        while (j >= 0) {
            stats->comparisons++;
            stats->array_accesses++;
            if (arr[j] > key) {
                stats->swaps++;
                stats->array_accesses += 2;
                arr[j + 1] = arr[j];
                j--;
            } else {
                break;
            }
        }
        arr[j + 1] = key;
        stats->array_accesses++;
    }
}

/**
 * Compare selection sort with other O(n²) algorithms.
 */
void compare_quadratic_sorts(const int arr[], int n) {
    printf("\n📊 ALGORITHM COMPARISON (O(n²) Algorithms):\n");
    printf("--------------------------------------------------------------------------------\n");

    /* Test cases */
    typedef struct {
        const char* name;
        int* data;
    } TestCase;

    const char* test_names[] = { "Random", "Already sorted", "Reverse sorted" };

    /* Create test data for each case */
    int* random_data = (int*)malloc(n * sizeof(int));
    int* sorted_data = (int*)malloc(n * sizeof(int));
    int* reversed_data = (int*)malloc(n * sizeof(int));

    memcpy(random_data, arr, n * sizeof(int));
    for (int i = 0; i < n; i++) sorted_data[i] = i;
    for (int i = 0; i < n; i++) reversed_data[i] = n - i - 1;

    int* test_arrays[] = { random_data, sorted_data, reversed_data };

    for (int t = 0; t < 3; t++) {
        printf("\n%s: ", test_names[t]);
        print_array(test_arrays[t], n, "");

        SortStatistics stats;

        /* Selection Sort */
        int* arr_sel = (int*)malloc(n * sizeof(int));
        memcpy(arr_sel, test_arrays[t], n * sizeof(int));
        selection_sort_with_stats(arr_sel, n, &stats);
        printf("  Selection Sort - Comparisons: %d, Swaps: %d, Array Accesses: %d\n",
               stats.comparisons, stats.swaps, stats.array_accesses);
        free(arr_sel);

        /* Bubble Sort */
        int* arr_bub = (int*)malloc(n * sizeof(int));
        memcpy(arr_bub, test_arrays[t], n * sizeof(int));
        bubble_sort_with_stats(arr_bub, n, &stats);
        printf("  Bubble Sort    - Comparisons: %d, Swaps: %d, Array Accesses: %d\n",
               stats.comparisons, stats.swaps, stats.array_accesses);
        free(arr_bub);

        /* Insertion Sort */
        int* arr_ins = (int*)malloc(n * sizeof(int));
        memcpy(arr_ins, test_arrays[t], n * sizeof(int));
        insertion_sort_with_stats(arr_ins, n, &stats);
        printf("  Insertion Sort - Comparisons: %d, Swaps: %d, Array Accesses: %d\n",
               stats.comparisons, stats.swaps, stats.array_accesses);
        free(arr_ins);
    }

    free(random_data);
    free(sorted_data);
    free(reversed_data);
}

// ============================================================================
// DEMONSTRATION AND TESTING
// ============================================================================

/**
 * Comprehensive demonstration of selection sort.
 */
void demonstrate_selection_sort() {
    printf("📚 SELECTION SORT - EDUCATIONAL DEMONSTRATION\n");
    printf("================================================================================\n");

    /* Test cases */
    int test1[] = {64, 25, 12, 22, 11};
    int test2[] = {5, 2, 8, 6, 1, 9, 4};
    int test3[] = {1};
    int test4[] = {3, 3, 3, 3, 3};
    int test5[] = {9, 8, 7, 6, 5, 4, 3, 2, 1};
    int test6[] = {1, 2, 3, 4, 5};

    int* tests[] = {test1, test2, test3, test4, test5, test6};
    int sizes[] = {5, 7, 1, 5, 9, 5};
    const char* descs[] = {
        "Random array",
        "Small random array",
        "Single element",
        "All duplicates",
        "Reverse sorted",
        "Already sorted"
    };

    printf("\n📋 BASIC FUNCTIONALITY TESTS:\n");
    printf("--------------------------------------------------------------------------------\n");

    for (int t = 0; t < 6; t++) {
        int n = sizes[t];
        int* arr = (int*)malloc(n * sizeof(int));

        printf("\nTest: %s\n", descs[t]);
        print_array(tests[t], n, "Original");

        /* Standard */
        memcpy(arr, tests[t], n * sizeof(int));
        selection_sort(arr, n);
        print_array(arr, n, "Standard      ");

        /* Bidirectional */
        memcpy(arr, tests[t], n * sizeof(int));
        bidirectional_selection_sort(arr, n);
        print_array(arr, n, "Bidirectional ");

        /* Recursive */
        memcpy(arr, tests[t], n * sizeof(int));
        selection_sort_recursive(arr, n);
        print_array(arr, n, "Recursive     ");

        /* Stable */
        memcpy(arr, tests[t], n * sizeof(int));
        stable_selection_sort(arr, n);
        print_array(arr, n, "Stable        ");

        printf("All correct: %s\n", is_sorted(arr, n) ? "✓" : "✗");

        free(arr);
    }

    /* Visualization */
    printf("\n\n🎬 STEP-BY-STEP VISUALIZATION:\n");
    printf("--------------------------------------------------------------------------------\n");
    int demo_arr[] = {64, 25, 12, 22, 11};
    visualize_selection_sort(demo_arr, 5);

    /* Comparison */
    compare_quadratic_sorts(test1, 5);

    /* Memory analysis */
    printf("\n\n💾 MEMORY USAGE ANALYSIS:\n");
    printf("--------------------------------------------------------------------------------\n");
    printf("Selection Sort Memory Characteristics:\n\n");
    printf("1. In-Place Sorting:\n");
    printf("   - Space Complexity: O(1) auxiliary space\n");
    printf("   - Only uses constant extra memory (min_idx, loop variables)\n");
    printf("   - Original array is modified in-place\n\n");
    printf("2. Memory Writes:\n");
    printf("   - Selection Sort: O(n) swaps (minimum writes)\n");
    printf("   - Bubble Sort: O(n²) swaps in worst case\n");
    printf("   - Insertion Sort: O(n²) shifts in worst case\n\n");
    printf("   ⭐ This makes Selection Sort ideal when writing to memory is expensive!\n");
    printf("      Examples: Flash memory, EEPROM, or distributed systems\n");
}

/**
 * Main function.
 */
int main(void) {
    demonstrate_selection_sort();
    printf("\n✨ Selection Sort demonstration complete!\n");
    return 0;
}
