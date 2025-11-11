/**
 * Binary Search Algorithm Collection in C
 *
 * Comprehensive implementation of binary search variants including:
 * 1. Classic binary search (iterative & recursive)
 * 2. First/last occurrence finding
 * 3. Rotated array search
 * 4. Exponential search
 * 5. Interpolation search
 * 6. Ternary search
 * 7. Binary search on answer (optimization)
 * 8. Advanced utilities
 *
 * Time Complexity: O(log n) for most variants
 * Space Complexity: O(1) iterative, O(log n) recursive
 *
 * C Features:
 * - Function pointers for custom comparators
 * - Macro-based generic implementations
 * - Efficient pointer arithmetic
 * - Comprehensive error handling
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>

/* ========================================================================== */
/* TYPE DEFINITIONS AND COMPARATORS                                          */
/* ========================================================================== */

typedef int (*CompareFunc)(const void*, const void*);
typedef bool (*Predicate)(int);
typedef double (*UnaryFunction)(double);

/* Standard comparators */
int compare_int(const void* a, const void* b) {
    int arg1 = *(const int*)a;
    int arg2 = *(const int*)b;
    return (arg1 > arg2) - (arg1 < arg2);
}

int compare_double(const void* a, const void* b) {
    double arg1 = *(const double*)a;
    double arg2 = *(const double*)b;
    return (arg1 > arg2) - (arg1 < arg2);
}

/* ========================================================================== */
/* 1. CLASSIC BINARY SEARCH                                                  */
/* ========================================================================== */

/**
 * Classic binary search - iterative implementation for integers.
 *
 * Time Complexity: O(log n)
 * Space Complexity: O(1)
 *
 * @param arr Sorted array
 * @param size Array size
 * @param target Element to search for
 * @return Index of target if found, -1 otherwise
 */
int binary_search_iterative(const int arr[], int size, int target) {
    if (arr == NULL || size <= 0) {
        return -1;
    }

    int left = 0;
    int right = size - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;  /* Avoid overflow */

        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}

/**
 * Classic binary search - recursive implementation.
 *
 * Time Complexity: O(log n)
 * Space Complexity: O(log n) - recursion stack
 */
int binary_search_recursive_helper(const int arr[], int target, int left, int right) {
    if (left > right) {
        return -1;
    }

    int mid = left + (right - left) / 2;

    if (arr[mid] == target) {
        return mid;
    } else if (arr[mid] < target) {
        return binary_search_recursive_helper(arr, target, mid + 1, right);
    } else {
        return binary_search_recursive_helper(arr, target, left, mid - 1);
    }
}

int binary_search_recursive(const int arr[], int size, int target) {
    if (arr == NULL || size <= 0) {
        return -1;
    }
    return binary_search_recursive_helper(arr, target, 0, size - 1);
}

/**
 * Generic binary search with custom comparator.
 *
 * @param arr Sorted array
 * @param size Number of elements
 * @param elem_size Size of each element
 * @param target Pointer to target element
 * @param compare Comparison function
 * @return Index of target if found, -1 otherwise
 */
int binary_search_generic(const void* arr, int size, size_t elem_size,
                         const void* target, CompareFunc compare) {
    if (arr == NULL || size <= 0 || compare == NULL) {
        return -1;
    }

    int left = 0;
    int right = size - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        const void* mid_elem = (const char*)arr + mid * elem_size;

        int cmp = compare(mid_elem, target);

        if (cmp == 0) {
            return mid;
        } else if (cmp < 0) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}

/* ========================================================================== */
/* 2. FIRST/LAST OCCURRENCE                                                  */
/* ========================================================================== */

/**
 * Find first (leftmost) occurrence of target.
 *
 * @param arr Sorted array (may contain duplicates)
 * @param size Array size
 * @param target Element to search for
 * @return Index of first occurrence, -1 if not found
 */
int find_first_occurrence(const int arr[], int size, int target) {
    if (arr == NULL || size <= 0) {
        return -1;
    }

    int left = 0;
    int right = size - 1;
    int result = -1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            result = mid;
            right = mid - 1;  /* Continue searching left */
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return result;
}

/**
 * Find last (rightmost) occurrence of target.
 *
 * @param arr Sorted array (may contain duplicates)
 * @param size Array size
 * @param target Element to search for
 * @return Index of last occurrence, -1 if not found
 */
int find_last_occurrence(const int arr[], int size, int target) {
    if (arr == NULL || size <= 0) {
        return -1;
    }

    int left = 0;
    int right = size - 1;
    int result = -1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            result = mid;
            left = mid + 1;  /* Continue searching right */
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return result;
}

/**
 * Count total occurrences of target.
 *
 * @param arr Sorted array
 * @param size Array size
 * @param target Element to count
 * @return Number of occurrences
 */
int count_occurrences(const int arr[], int size, int target) {
    int first = find_first_occurrence(arr, size, target);
    if (first == -1) {
        return 0;
    }

    int last = find_last_occurrence(arr, size, target);
    return last - first + 1;
}

/**
 * Find range [start, end] of target.
 *
 * @param arr Sorted array
 * @param size Array size
 * @param target Element to search for
 * @param range Output array [first, last]
 */
void search_range(const int arr[], int size, int target, int range[2]) {
    int first = find_first_occurrence(arr, size, target);
    if (first == -1) {
        range[0] = range[1] = -1;
        return;
    }

    int last = find_last_occurrence(arr, size, target);
    range[0] = first;
    range[1] = last;
}

/* ========================================================================== */
/* 3. ROTATED SORTED ARRAY SEARCH                                            */
/* ========================================================================== */

/**
 * Search in rotated sorted array.
 *
 * @param arr Rotated sorted array (no duplicates)
 * @param size Array size
 * @param target Element to search for
 * @return Index of target if found, -1 otherwise
 */
int search_rotated_array(const int arr[], int size, int target) {
    if (arr == NULL || size <= 0) {
        return -1;
    }

    int left = 0;
    int right = size - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            return mid;
        }

        /* Determine which half is sorted */
        if (arr[left] <= arr[mid]) {
            /* Left half is sorted */
            if (arr[left] <= target && target < arr[mid]) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        } else {
            /* Right half is sorted */
            if (arr[mid] < target && target <= arr[right]) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
    }

    return -1;
}

/**
 * Find rotation point (minimum element).
 *
 * @param arr Rotated sorted array
 * @param size Array size
 * @return Index of minimum element
 */
int find_rotation_point(const int arr[], int size) {
    if (arr == NULL || size <= 0) {
        return -1;
    }

    int left = 0;
    int right = size - 1;

    while (left < right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] > arr[right]) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    return left;
}

/* ========================================================================== */
/* 4. EXPONENTIAL SEARCH                                                     */
/* ========================================================================== */

/**
 * Exponential search - efficient for unbounded arrays.
 *
 * @param arr Sorted array
 * @param size Array size
 * @param target Element to search for
 * @return Index of target if found, -1 otherwise
 */
int exponential_search(const int arr[], int size, int target) {
    if (arr == NULL || size <= 0) {
        return -1;
    }

    if (arr[0] == target) {
        return 0;
    }

    /* Find range for binary search */
    int i = 1;
    while (i < size && arr[i] <= target) {
        i *= 2;
    }

    /* Binary search in found range */
    int left = i / 2;
    int right = (i < size) ? i : size - 1;

    return binary_search_recursive_helper(arr, target, left, right);
}

/* ========================================================================== */
/* 5. INTERPOLATION SEARCH                                                   */
/* ========================================================================== */

/**
 * Interpolation search - better for uniformly distributed data.
 *
 * Time Complexity: O(log log n) average, O(n) worst
 *
 * @param arr Sorted array of integers
 * @param size Array size
 * @param target Integer to search for
 * @return Index of target if found, -1 otherwise
 */
int interpolation_search(const int arr[], int size, int target) {
    if (arr == NULL || size <= 0) {
        return -1;
    }

    int left = 0;
    int right = size - 1;

    while (left <= right && target >= arr[left] && target <= arr[right]) {
        if (left == right) {
            return (arr[left] == target) ? left : -1;
        }

        /* Interpolation formula */
        int pos = left + ((double)(target - arr[left]) / (arr[right] - arr[left])) *
                        (right - left);

        /* Ensure pos is within bounds */
        if (pos < left) pos = left;
        if (pos > right) pos = right;

        if (arr[pos] == target) {
            return pos;
        } else if (arr[pos] < target) {
            left = pos + 1;
        } else {
            right = pos - 1;
        }
    }

    return -1;
}

/* ========================================================================== */
/* 6. TERNARY SEARCH                                                         */
/* ========================================================================== */

/**
 * Ternary search - divides array into three parts.
 *
 * @param arr Sorted array
 * @param size Array size
 * @param target Element to search for
 * @return Index of target if found, -1 otherwise
 */
int ternary_search(const int arr[], int size, int target) {
    if (arr == NULL || size <= 0) {
        return -1;
    }

    int left = 0;
    int right = size - 1;

    while (left <= right) {
        int mid1 = left + (right - left) / 3;
        int mid2 = right - (right - left) / 3;

        if (arr[mid1] == target) {
            return mid1;
        }
        if (arr[mid2] == target) {
            return mid2;
        }

        if (target < arr[mid1]) {
            right = mid1 - 1;
        } else if (target > arr[mid2]) {
            left = mid2 + 1;
        } else {
            left = mid1 + 1;
            right = mid2 - 1;
        }
    }

    return -1;
}

/**
 * Ternary search for finding maximum of unimodal function.
 *
 * @param function Unimodal function
 * @param left Left boundary
 * @param right Right boundary
 * @param epsilon Precision threshold
 * @return x value where function reaches maximum
 */
double ternary_search_maximum(UnaryFunction function, double left, double right,
                              double epsilon) {
    while (right - left > epsilon) {
        double mid1 = left + (right - left) / 3.0;
        double mid2 = right - (right - left) / 3.0;

        if (function(mid1) < function(mid2)) {
            left = mid1;
        } else {
            right = mid2;
        }
    }

    return (left + right) / 2.0;
}

/* ========================================================================== */
/* 7. BINARY SEARCH ON ANSWER                                                */
/* ========================================================================== */

/**
 * Binary search on answer space for optimization problems.
 *
 * @param predicate Function returning true if answer is feasible
 * @param low Minimum possible answer
 * @param high Maximum possible answer
 * @return Minimum value where predicate is true, -1 if no solution
 */
int binary_search_on_answer(Predicate predicate, int low, int high) {
    if (predicate == NULL) {
        return -1;
    }

    int result = -1;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (predicate(mid)) {
            result = mid;
            high = mid - 1;  /* Try to find smaller answer */
        } else {
            low = mid + 1;
        }
    }

    return result;
}

/**
 * Find integer square root using binary search.
 *
 * @param n Number to find square root of (non-negative)
 * @return Integer square root of n, -1 on error
 */
int integer_square_root(int n) {
    if (n < 0) {
        return -1;
    }

    if (n == 0 || n == 1) {
        return n;
    }

    int left = 0;
    int right = n;
    int result = 0;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        /* Use long long to avoid overflow */
        long long square = (long long)mid * mid;

        if (square == n) {
            return mid;
        } else if (square < n) {
            result = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return result;
}

/**
 * Find square root with decimal precision.
 *
 * @param n Number to find square root of
 * @param precision Number of decimal places
 * @return Square root of n
 */
double square_root(double n, int precision) {
    if (n < 0.0) {
        return -1.0;
    }

    if (n == 0.0 || n == 1.0) {
        return n;
    }

    double left = 0.0;
    double right = n;
    double epsilon = pow(10, -precision);

    while (right - left > epsilon) {
        double mid = left + (right - left) / 2.0;
        double square = mid * mid;

        if (fabs(square - n) < epsilon) {
            return mid;
        } else if (square < n) {
            left = mid;
        } else {
            right = mid;
        }
    }

    return (left + right) / 2.0;
}

/* ========================================================================== */
/* 8. ADVANCED UTILITIES                                                     */
/* ========================================================================== */

/**
 * Find insertion position to maintain sorted order.
 *
 * @param arr Sorted array
 * @param size Array size
 * @param target Element to insert
 * @return Index where target should be inserted
 */
int search_insert_position(const int arr[], int size, int target) {
    if (arr == NULL || size <= 0) {
        return 0;
    }

    int left = 0;
    int right = size;

    while (left < right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    return left;
}

/**
 * Find element closest to target.
 *
 * @param arr Sorted array
 * @param size Array size
 * @param target Target value
 * @return Index of closest element
 */
int find_closest(const int arr[], int size, int target) {
    if (arr == NULL || size <= 0) {
        return -1;
    }

    if (size == 1) {
        return 0;
    }

    if (target <= arr[0]) {
        return 0;
    }
    if (target >= arr[size - 1]) {
        return size - 1;
    }

    int left = 0;
    int right = size - 1;

    while (left < right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    if (left > 0 && abs(arr[left - 1] - target) < abs(arr[left] - target)) {
        return left - 1;
    }

    return left;
}

/**
 * Find peak element (element greater than neighbors).
 *
 * @param arr Array
 * @param size Array size
 * @return Index of a peak element
 */
int find_peak_element(const int arr[], int size) {
    if (arr == NULL || size <= 0) {
        return -1;
    }

    if (size == 1) {
        return 0;
    }

    int left = 0;
    int right = size - 1;

    while (left < right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] < arr[mid + 1]) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    return left;
}

/* ========================================================================== */
/* DEMONSTRATION AND TESTING                                                 */
/* ========================================================================== */

void print_separator(const char* title) {
    printf("\n%s\n", title);
    for (int i = 0; i < 50; i++) printf("-");
    printf("\n");
}

void demonstrate_classic_binary_search() {
    print_separator("1. CLASSIC BINARY SEARCH");

    int arr[] = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
    int size = sizeof(arr) / sizeof(arr[0]);
    int targets[] = {7, 10, 1, 19};

    for (int i = 0; i < 4; i++) {
        int target = targets[i];
        int idx_iter = binary_search_iterative(arr, size, target);
        int idx_rec = binary_search_recursive(arr, size, target);
        printf("Search %2d: Iterative=%2d, Recursive=%2d\n",
               target, idx_iter, idx_rec);
    }

    /* Generic search */
    int target = 7;
    int idx = binary_search_generic(arr, size, sizeof(int), &target, compare_int);
    printf("Generic search for %d: %d\n", target, idx);
}

void demonstrate_first_last_occurrence() {
    print_separator("2. FIRST/LAST OCCURRENCE");

    int arr[] = {1, 2, 2, 2, 3, 4, 4, 4, 4, 5};
    int size = sizeof(arr) / sizeof(arr[0]);
    int targets[] = {2, 4, 6};

    for (int i = 0; i < 3; i++) {
        int target = targets[i];
        int first = find_first_occurrence(arr, size, target);
        int last = find_last_occurrence(arr, size, target);
        int count = count_occurrences(arr, size, target);
        printf("Target %d: First=%2d, Last=%2d, Count=%d\n",
               target, first, last, count);
    }
}

void demonstrate_rotated_array_search() {
    print_separator("3. ROTATED ARRAY SEARCH");

    int rotated[] = {4, 5, 6, 7, 0, 1, 2};
    int size = sizeof(rotated) / sizeof(rotated[0]);
    int rotation_point = find_rotation_point(rotated, size);

    printf("Rotated array: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", rotated[i]);
    }
    printf("\nRotation point: %d (value: %d)\n",
           rotation_point, rotated[rotation_point]);

    int targets[] = {0, 3, 6};
    for (int i = 0; i < 3; i++) {
        int target = targets[i];
        int idx = search_rotated_array(rotated, size, target);
        printf("Search %d: Index=%d\n", target, idx);
    }
}

void demonstrate_exponential_search() {
    print_separator("4. EXPONENTIAL SEARCH");

    int large_arr[50];
    for (int i = 0; i < 50; i++) {
        large_arr[i] = i * 2 + 1;
    }

    int targets[] = {15, 51, 99};
    for (int i = 0; i < 3; i++) {
        int target = targets[i];
        int idx = exponential_search(large_arr, 50, target);
        printf("Search %2d in array of size 50: Index=%d\n", target, idx);
    }
}

void demonstrate_interpolation_search() {
    print_separator("5. INTERPOLATION SEARCH");

    int uniform_arr[] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
    int size = sizeof(uniform_arr) / sizeof(uniform_arr[0]);
    int targets[] = {30, 75, 100};

    for (int i = 0; i < 3; i++) {
        int target = targets[i];
        int idx = interpolation_search(uniform_arr, size, target);
        printf("Search %3d: Index=%d\n", target, idx);
    }
}

void demonstrate_ternary_search() {
    print_separator("6. TERNARY SEARCH");

    int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int size = sizeof(arr) / sizeof(arr[0]);
    int targets[] = {5, 1, 10, 11};

    for (int i = 0; i < 4; i++) {
        int target = targets[i];
        int idx = ternary_search(arr, size, target);
        printf("Search %2d: Index=%d\n", target, idx);
    }

    /* Unimodal function: -(x-5)^2 + 25 */
    double max_x = ternary_search_maximum(
        [](double x) { return -(x - 5) * (x - 5) + 25; },
        0.0, 10.0, 1e-9
    );
    printf("Maximum of -(x-5)² + 25 at x ≈ %.6f\n", max_x);
}

void demonstrate_binary_search_on_answer() {
    print_separator("7. BINARY SEARCH ON ANSWER");

    int test_numbers[] = {16, 25, 50, 100};
    for (int i = 0; i < 4; i++) {
        int n = test_numbers[i];
        int sqrt_int = integer_square_root(n);
        double sqrt_precise = square_root((double)n, 2);
        printf("√%3d = %d (integer), %.2f (precise)\n",
               n, sqrt_int, sqrt_precise);
    }
}

void demonstrate_advanced_utilities() {
    print_separator("8. ADVANCED UTILITIES");

    int arr[] = {1, 3, 5, 6, 8, 10};
    int size = sizeof(arr) / sizeof(arr[0]);
    int targets[] = {2, 5, 11};

    for (int i = 0; i < 3; i++) {
        int target = targets[i];
        int pos = search_insert_position(arr, size, target);
        printf("Insert position for %2d: %d\n", target, pos);
    }

    int arr_closest[] = {1, 3, 5, 7, 9};
    int size_closest = sizeof(arr_closest) / sizeof(arr_closest[0]);
    int targets_closest[] = {4, 6, 8};

    for (int i = 0; i < 3; i++) {
        int target = targets_closest[i];
        int idx = find_closest(arr_closest, size_closest, target);
        printf("Closest to %d: Index=%d, Value=%d\n",
               target, idx, arr_closest[idx]);
    }

    int peak_arr[] = {1, 3, 20, 4, 1, 0};
    int peak_size = sizeof(peak_arr) / sizeof(peak_arr[0]);
    int peak = find_peak_element(peak_arr, peak_size);
    printf("Peak element: Index=%d, Value=%d\n", peak, peak_arr[peak]);
}

int main() {
    printf("======================================================================\n");
    printf("BINARY SEARCH ALGORITHM COLLECTION - C\n");
    printf("======================================================================\n");

    demonstrate_classic_binary_search();
    demonstrate_first_last_occurrence();
    demonstrate_rotated_array_search();
    demonstrate_exponential_search();
    demonstrate_interpolation_search();
    demonstrate_ternary_search();
    demonstrate_binary_search_on_answer();
    demonstrate_advanced_utilities();

    printf("\n======================================================================\n");
    printf("DEMONSTRATION COMPLETE\n");
    printf("======================================================================\n");

    return 0;
}
