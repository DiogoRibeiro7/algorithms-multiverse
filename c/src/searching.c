/**
 * @file searching.c
 * @brief Implementation of searching algorithms
 */

#include "searching.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* Linear Search */
search_result_t linear_search(const int* arr, size_t n, int target) {
    search_result_t result = {false, 0, 0};

    if (!arr || n == 0) return result;

    for (size_t i = 0; i < n; i++) {
        result.comparisons++;
        if (arr[i] == target) {
            result.found = true;
            result.index = i;
            break;
        }
    }

    return result;
}

/* Generic Linear Search */
search_result_t linear_search_generic(const void* arr, size_t n, size_t elem_size,
                                      const void* target,
                                      int (*compare)(const void*, const void*)) {
    search_result_t result = {false, 0, 0};

    if (!arr || n == 0 || !target || !compare) return result;

    const char* array = (const char*)arr;

    for (size_t i = 0; i < n; i++) {
        result.comparisons++;
        if (compare(array + i * elem_size, target) == 0) {
            result.found = true;
            result.index = i;
            break;
        }
    }

    return result;
}

/* Binary Search (iterative) */
search_result_t binary_search(const int* arr, size_t n, int target) {
    search_result_t result = {false, 0, 0};

    if (!arr || n == 0) return result;

    size_t left = 0;
    size_t right = n - 1;

    while (left <= right) {
        size_t mid = left + (right - left) / 2;
        result.comparisons++;

        if (arr[mid] == target) {
            result.found = true;
            result.index = mid;
            break;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            if (mid == 0) break;  /* Prevent underflow */
            right = mid - 1;
        }
    }

    return result;
}

/* Binary Search (recursive helper) */
static search_result_t binary_search_recursive_helper(const int* arr, size_t left,
                                                      size_t right, int target,
                                                      size_t comparisons) {
    search_result_t result = {false, 0, comparisons};

    if (left > right) return result;

    size_t mid = left + (right - left) / 2;
    result.comparisons++;

    if (arr[mid] == target) {
        result.found = true;
        result.index = mid;
    } else if (arr[mid] < target) {
        return binary_search_recursive_helper(arr, mid + 1, right, target, result.comparisons);
    } else {
        if (mid == 0) return result;
        return binary_search_recursive_helper(arr, left, mid - 1, target, result.comparisons);
    }

    return result;
}

/* Binary Search (recursive) */
search_result_t binary_search_recursive(const int* arr, size_t n, int target) {
    if (!arr || n == 0) {
        search_result_t result = {false, 0, 0};
        return result;
    }

    return binary_search_recursive_helper(arr, 0, n - 1, target, 0);
}

/* Generic Binary Search */
search_result_t binary_search_generic(const void* arr, size_t n, size_t elem_size,
                                      const void* target,
                                      int (*compare)(const void*, const void*)) {
    search_result_t result = {false, 0, 0};

    if (!arr || n == 0 || !target || !compare) return result;

    const char* array = (const char*)arr;
    size_t left = 0;
    size_t right = n - 1;

    while (left <= right) {
        size_t mid = left + (right - left) / 2;
        result.comparisons++;

        int cmp = compare(array + mid * elem_size, target);

        if (cmp == 0) {
            result.found = true;
            result.index = mid;
            break;
        } else if (cmp < 0) {
            left = mid + 1;
        } else {
            if (mid == 0) break;
            right = mid - 1;
        }
    }

    return result;
}

/* Jump Search */
search_result_t jump_search(const int* arr, size_t n, int target) {
    search_result_t result = {false, 0, 0};

    if (!arr || n == 0) return result;

    size_t step = (size_t)sqrt(n);
    size_t prev = 0;

    /* Jump to find the block */
    while (arr[prev] < target) {
        result.comparisons++;
        size_t next = prev + step;

        if (next >= n) {
            next = n - 1;
        }

        if (arr[next] >= target) {
            break;
        }

        prev = next;
        if (prev >= n - 1) break;
    }

    /* Linear search in the block */
    for (size_t i = prev; i < n && i < prev + step; i++) {
        result.comparisons++;
        if (arr[i] == target) {
            result.found = true;
            result.index = i;
            break;
        }
        if (arr[i] > target) {
            break;
        }
    }

    return result;
}

/* Interpolation Search */
search_result_t interpolation_search(const int* arr, size_t n, int target) {
    search_result_t result = {false, 0, 0};

    if (!arr || n == 0) return result;

    size_t low = 0;
    size_t high = n - 1;

    while (low <= high && target >= arr[low] && target <= arr[high]) {
        result.comparisons++;

        if (low == high) {
            if (arr[low] == target) {
                result.found = true;
                result.index = low;
            }
            break;
        }

        /* Calculate position using interpolation formula */
        size_t pos = low + (((double)(high - low) / (arr[high] - arr[low])) *
                           (target - arr[low]));

        if (arr[pos] == target) {
            result.found = true;
            result.index = pos;
            break;
        } else if (arr[pos] < target) {
            low = pos + 1;
        } else {
            if (pos == 0) break;
            high = pos - 1;
        }
    }

    return result;
}

/* Exponential Search */
search_result_t exponential_search(const int* arr, size_t n, int target) {
    search_result_t result = {false, 0, 0};

    if (!arr || n == 0) return result;

    /* If target is at first position */
    result.comparisons++;
    if (arr[0] == target) {
        result.found = true;
        result.index = 0;
        return result;
    }

    /* Find range for binary search */
    size_t i = 1;
    while (i < n && arr[i] <= target) {
        result.comparisons++;
        if (arr[i] == target) {
            result.found = true;
            result.index = i;
            return result;
        }
        i *= 2;
    }

    /* Apply binary search on the range */
    size_t left = i / 2;
    size_t right = (i < n) ? i : n - 1;

    while (left <= right) {
        size_t mid = left + (right - left) / 2;
        result.comparisons++;

        if (arr[mid] == target) {
            result.found = true;
            result.index = mid;
            break;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            if (mid == 0) break;
            right = mid - 1;
        }
    }

    return result;
}

/* Fibonacci Search */
search_result_t fibonacci_search(const int* arr, size_t n, int target) {
    search_result_t result = {false, 0, 0};

    if (!arr || n == 0) return result;

    /* Initialize Fibonacci numbers */
    size_t fib2 = 0;  /* (m-2)'th Fibonacci number */
    size_t fib1 = 1;  /* (m-1)'th Fibonacci number */
    size_t fib = fib2 + fib1;  /* m'th Fibonacci number */

    /* Find the smallest Fibonacci number >= n */
    while (fib < n) {
        fib2 = fib1;
        fib1 = fib;
        fib = fib2 + fib1;
    }

    size_t offset = 0;

    while (fib > 1) {
        /* Check if fib2 is valid index */
        size_t i = (offset + fib2 < n - 1) ? offset + fib2 : n - 1;

        result.comparisons++;

        if (arr[i] < target) {
            fib = fib1;
            fib1 = fib2;
            fib2 = fib - fib1;
            offset = i;
        } else if (arr[i] > target) {
            fib = fib2;
            fib1 = fib1 - fib2;
            fib2 = fib - fib1;
        } else {
            result.found = true;
            result.index = i;
            return result;
        }
    }

    /* Check last element */
    if (offset < n) {
        result.comparisons++;
        if (arr[offset] == target) {
            result.found = true;
            result.index = offset;
        }
    }

    return result;
}

/* Ternary Search */
search_result_t ternary_search(const int* arr, size_t n, int target) {
    search_result_t result = {false, 0, 0};

    if (!arr || n == 0) return result;

    size_t left = 0;
    size_t right = n - 1;

    while (left <= right) {
        size_t mid1 = left + (right - left) / 3;
        size_t mid2 = right - (right - left) / 3;

        result.comparisons++;
        if (arr[mid1] == target) {
            result.found = true;
            result.index = mid1;
            return result;
        }

        result.comparisons++;
        if (arr[mid2] == target) {
            result.found = true;
            result.index = mid2;
            return result;
        }

        if (target < arr[mid1]) {
            if (mid1 == 0) break;
            right = mid1 - 1;
        } else if (target > arr[mid2]) {
            left = mid2 + 1;
        } else {
            left = mid1 + 1;
            if (mid2 == 0) break;
            right = mid2 - 1;
        }
    }

    return result;
}

/* Find minimum element */
int find_min(const int* arr, size_t n) {
    if (!arr || n == 0) return 0;

    int min = arr[0];
    for (size_t i = 1; i < n; i++) {
        if (arr[i] < min) {
            min = arr[i];
        }
    }
    return min;
}

/* Find maximum element */
int find_max(const int* arr, size_t n) {
    if (!arr || n == 0) return 0;

    int max = arr[0];
    for (size_t i = 1; i < n; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

/* Quick select algorithm for kth element */
static int partition_quickselect(int* arr, size_t low, size_t high) {
    int pivot = arr[high];
    size_t i = low;

    for (size_t j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
            i++;
        }
    }

    int temp = arr[i];
    arr[i] = arr[high];
    arr[high] = temp;

    return i;
}

static int quickselect(int* arr, size_t low, size_t high, size_t k) {
    if (low == high) {
        return arr[low];
    }

    size_t pivot_index = partition_quickselect(arr, low, high);

    if (k == pivot_index) {
        return arr[k];
    } else if (k < pivot_index) {
        return quickselect(arr, low, pivot_index - 1, k);
    } else {
        return quickselect(arr, pivot_index + 1, high, k);
    }
}

/* Find kth smallest element */
int find_kth_smallest(int* arr, size_t n, size_t k) {
    if (!arr || n == 0 || k == 0 || k > n) return 0;

    /* Create a copy to avoid modifying original array */
    int* temp = malloc(n * sizeof(int));
    memcpy(temp, arr, n * sizeof(int));

    int result = quickselect(temp, 0, n - 1, k - 1);

    free(temp);
    return result;
}

/* Find kth largest element */
int find_kth_largest(int* arr, size_t n, size_t k) {
    if (!arr || n == 0 || k == 0 || k > n) return 0;

    /* kth largest is (n - k + 1)th smallest */
    return find_kth_smallest(arr, n, n - k + 1);
}

/* Find median */
int find_median(int* arr, size_t n) {
    if (!arr || n == 0) return 0;

    if (n % 2 == 1) {
        /* Odd number of elements */
        return find_kth_smallest(arr, n, (n + 1) / 2);
    } else {
        /* Even number of elements - return lower median */
        return find_kth_smallest(arr, n, n / 2);
    }
}

/* Lower bound - first element >= value */
size_t lower_bound(const int* arr, size_t n, int value) {
    if (!arr || n == 0) return 0;

    size_t left = 0;
    size_t right = n;

    while (left < right) {
        size_t mid = left + (right - left) / 2;

        if (arr[mid] < value) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    return left;
}

/* Upper bound - first element > value */
size_t upper_bound(const int* arr, size_t n, int value) {
    if (!arr || n == 0) return 0;

    size_t left = 0;
    size_t right = n;

    while (left < right) {
        size_t mid = left + (right - left) / 2;

        if (arr[mid] <= value) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    return left;
}

/* Equal range - find range of elements equal to value */
void equal_range(const int* arr, size_t n, int value, size_t* lower, size_t* upper) {
    if (!arr || n == 0 || !lower || !upper) return;

    *lower = lower_bound(arr, n, value);
    *upper = upper_bound(arr, n, value);
}

/* Count occurrences of a value */
size_t count_occurrences(const int* arr, size_t n, int value) {
    if (!arr || n == 0) return 0;

    size_t lower, upper;
    equal_range(arr, n, value, &lower, &upper);

    return upper - lower;
}

/* Find peak element in 1D array */
size_t find_peak_1d(const int* arr, size_t n) {
    if (!arr || n == 0) return 0;
    if (n == 1) return 0;

    size_t left = 0;
    size_t right = n - 1;

    while (left <= right) {
        size_t mid = left + (right - left) / 2;

        /* Check if mid is a peak */
        bool left_ok = (mid == 0 || arr[mid] >= arr[mid - 1]);
        bool right_ok = (mid == n - 1 || arr[mid] >= arr[mid + 1]);

        if (left_ok && right_ok) {
            return mid;
        }

        /* Move to the side with larger neighbor */
        if (mid > 0 && arr[mid - 1] > arr[mid]) {
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    }

    return 0;
}

/* Find peak element in 2D matrix */
void find_peak_2d(const int** matrix, size_t rows, size_t cols,
                  size_t* peak_row, size_t* peak_col) {
    if (!matrix || rows == 0 || cols == 0 || !peak_row || !peak_col) return;

    *peak_row = 0;
    *peak_col = 0;

    size_t left = 0;
    size_t right = cols - 1;

    while (left <= right) {
        size_t mid_col = left + (right - left) / 2;

        /* Find maximum in mid column */
        size_t max_row = 0;
        for (size_t i = 1; i < rows; i++) {
            if (matrix[i][mid_col] > matrix[max_row][mid_col]) {
                max_row = i;
            }
        }

        /* Check if it's a peak */
        bool left_ok = (mid_col == 0 ||
                        matrix[max_row][mid_col] >= matrix[max_row][mid_col - 1]);
        bool right_ok = (mid_col == cols - 1 ||
                         matrix[max_row][mid_col] >= matrix[max_row][mid_col + 1]);

        if (left_ok && right_ok) {
            *peak_row = max_row;
            *peak_col = mid_col;
            return;
        }

        /* Move to the side with larger neighbor */
        if (mid_col > 0 && matrix[max_row][mid_col - 1] > matrix[max_row][mid_col]) {
            right = mid_col - 1;
        } else {
            left = mid_col + 1;
        }
    }
}

/* Find majority element (Boyer-Moore Voting Algorithm) */
int find_majority_element(const int* arr, size_t n, bool* has_majority) {
    if (!arr || n == 0 || !has_majority) {
        if (has_majority) *has_majority = false;
        return 0;
    }

    /* Find candidate */
    int candidate = arr[0];
    int count = 1;

    for (size_t i = 1; i < n; i++) {
        if (arr[i] == candidate) {
            count++;
        } else {
            count--;
            if (count == 0) {
                candidate = arr[i];
                count = 1;
            }
        }
    }

    /* Verify if candidate is majority */
    count = 0;
    for (size_t i = 0; i < n; i++) {
        if (arr[i] == candidate) {
            count++;
        }
    }

    *has_majority = (count > n / 2);
    return candidate;
}

/* Two Sum - find two indices that sum to target */
bool two_sum(const int* arr, size_t n, int target, size_t* idx1, size_t* idx2) {
    if (!arr || n < 2 || !idx1 || !idx2) return false;

    /* Create array of indices for sorting */
    size_t* indices = malloc(n * sizeof(size_t));
    int* sorted = malloc(n * sizeof(int));

    for (size_t i = 0; i < n; i++) {
        indices[i] = i;
        sorted[i] = arr[i];
    }

    /* Sort array and indices together */
    for (size_t i = 0; i < n - 1; i++) {
        for (size_t j = i + 1; j < n; j++) {
            if (sorted[i] > sorted[j]) {
                int temp = sorted[i];
                sorted[i] = sorted[j];
                sorted[j] = temp;

                size_t temp_idx = indices[i];
                indices[i] = indices[j];
                indices[j] = temp_idx;
            }
        }
    }

    /* Two pointer approach */
    size_t left = 0;
    size_t right = n - 1;
    bool found = false;

    while (left < right) {
        int sum = sorted[left] + sorted[right];

        if (sum == target) {
            *idx1 = indices[left];
            *idx2 = indices[right];
            found = true;
            break;
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
    }

    free(indices);
    free(sorted);
    return found;
}

/* Three Sum - find three indices that sum to target */
bool three_sum(const int* arr, size_t n, int target,
                size_t* idx1, size_t* idx2, size_t* idx3) {
    if (!arr || n < 3 || !idx1 || !idx2 || !idx3) return false;

    /* Try each element as first element */
    for (size_t i = 0; i < n - 2; i++) {
        /* Create reduced array without element i */
        int* reduced = malloc((n - 1) * sizeof(int));
        size_t* original_indices = malloc((n - 1) * sizeof(size_t));

        size_t k = 0;
        for (size_t j = 0; j < n; j++) {
            if (j != i) {
                reduced[k] = arr[j];
                original_indices[k] = j;
                k++;
            }
        }

        /* Find two sum in reduced array */
        size_t sub_idx1, sub_idx2;
        if (two_sum(reduced, n - 1, target - arr[i], &sub_idx1, &sub_idx2)) {
            *idx1 = i;
            *idx2 = original_indices[sub_idx1];
            *idx3 = original_indices[sub_idx2];

            free(reduced);
            free(original_indices);
            return true;
        }

        free(reduced);
        free(original_indices);
    }

    return false;
}