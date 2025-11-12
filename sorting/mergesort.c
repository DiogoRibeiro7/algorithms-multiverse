/*
 * MergeSort Implementation in C
 *
 * MergeSort is a divide-and-conquer sorting algorithm.
 * Time Complexity: O(n log n) - all cases
 * Space Complexity: O(n) - requires auxiliary array
 *
 * Features:
 * - Stable sorting algorithm
 * - Guaranteed O(n log n) performance
 * - Top-down and bottom-up implementations
 * - Natural merge sort variant
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Function prototypes
void mergesort(int arr[], int left, int right);
void mergesort_bottomup(int arr[], int n);
void merge(int arr[], int left, int mid, int right);
void print_array(const int arr[], int size);
int is_sorted(const int arr[], int size);

/*
 * Top-down MergeSort (recursive)
 */
void mergesort(int arr[], int left, int right) {
    if (left < right) {
        // Find middle point
        int mid = left + (right - left) / 2;

        // Sort first and second halves
        mergesort(arr, left, mid);
        mergesort(arr, mid + 1, right);

        // Merge the sorted halves
        merge(arr, left, mid, right);
    }
}

/*
 * Merge two sorted subarrays
 * arr[left..mid] and arr[mid+1..right]
 */
void merge(int arr[], int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    // Create temporary arrays
    int* L = (int*)malloc(n1 * sizeof(int));
    int* R = (int*)malloc(n2 * sizeof(int));

    // Copy data to temporary arrays
    for (int i = 0; i < n1; i++)
        L[i] = arr[left + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[mid + 1 + j];

    // Merge the temporary arrays back
    int i = 0, j = 0, k = left;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {  // <= ensures stability
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // Copy remaining elements
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }

    free(L);
    free(R);
}

/*
 * Bottom-up MergeSort (iterative)
 * Avoids recursion overhead
 */
void mergesort_bottomup(int arr[], int n) {
    // Start with merge subarrays of size 1, and merge to form size 2,
    // then merge subarrays of size 2 to form size 4, and so on
    for (int curr_size = 1; curr_size < n; curr_size *= 2) {
        // Pick starting index of left sub array to be merged
        for (int left_start = 0; left_start < n - 1; left_start += 2 * curr_size) {
            // Find ending point of left subarray
            // The starting point of right subarray is mid + 1
            int mid = left_start + curr_size - 1;

            // Find ending point of right subarray
            int right_end = (left_start + 2 * curr_size - 1 < n - 1) ?
                           (left_start + 2 * curr_size - 1) : (n - 1);

            // Merge subarrays arr[left_start...mid] & arr[mid+1...right_end]
            if (mid < right_end) {
                merge(arr, left_start, mid, right_end);
            }
        }
    }
}

/*
 * Print array
 */
void print_array(const int arr[], int size) {
    printf("[");
    for (int i = 0; i < size; i++) {
        printf("%d", arr[i]);
        if (i < size - 1) printf(", ");
    }
    printf("]\n");
}

/*
 * Check if array is sorted
 */
int is_sorted(const int arr[], int size) {
    for (int i = 0; i < size - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            return 0;
        }
    }
    return 1;
}

/*
 * Benchmark function
 */
double benchmark_sort(void (*sort_func)(int[], int, int), int arr[], int size, const char* name) {
    clock_t start = clock();
    sort_func(arr, 0, size - 1);
    clock_t end = clock();

    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("%s: ", name);
    if (is_sorted(arr, size)) {
        printf("✓ Sorted in %.6f seconds\n", time_taken);
    } else {
        printf("✗ Sort failed!\n");
    }

    return time_taken;
}

double benchmark_bottomup(int arr[], int size, const char* name) {
    clock_t start = clock();
    mergesort_bottomup(arr, size);
    clock_t end = clock();

    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("%s: ", name);
    if (is_sorted(arr, size)) {
        printf("✓ Sorted in %.6f seconds\n", time_taken);
    } else {
        printf("✗ Sort failed!\n");
    }

    return time_taken;
}

/*
 * Main function with tests and benchmarks
 */
int main() {
    srand(time(NULL));

    printf("=================================================================\n");
    printf("                    MERGESORT IN C\n");
    printf("=================================================================\n\n");

    // Test 1: Small array
    printf("Test 1: Small array (Top-Down)\n");
    printf("-----------------------------------------------------------------\n");
    int arr1[] = {64, 34, 25, 12, 22, 11, 90, 88, 45, 50};
    int n1 = sizeof(arr1) / sizeof(arr1[0]);

    printf("Original: ");
    print_array(arr1, n1);

    mergesort(arr1, 0, n1 - 1);

    printf("Sorted:   ");
    print_array(arr1, n1);
    printf("Stable: Yes (equal elements maintain relative order)\n\n");

    // Test 2: Array with duplicates (test stability)
    printf("Test 2: Testing stability with duplicates\n");
    printf("-----------------------------------------------------------------\n");
    int arr2[] = {5, 2, 8, 2, 9, 1, 5, 5, 2, 8};
    int n2 = sizeof(arr2) / sizeof(arr2[0]);

    printf("Original: ");
    print_array(arr2, n2);

    mergesort(arr2, 0, n2 - 1);

    printf("Sorted:   ");
    print_array(arr2, n2);
    printf("\n");

    // Test 3: Bottom-up MergeSort
    printf("Test 3: Bottom-Up MergeSort (Iterative)\n");
    printf("-----------------------------------------------------------------\n");
    int arr3[] = {38, 27, 43, 3, 9, 82, 10};
    int n3 = sizeof(arr3) / sizeof(arr3[0]);

    printf("Original: ");
    print_array(arr3, n3);

    mergesort_bottomup(arr3, n3);

    printf("Sorted:   ");
    print_array(arr3, n3);
    printf("\n");

    // Performance benchmarks
    printf("Performance Benchmarks\n");
    printf("=================================================================\n");

    int sizes[] = {1000, 5000, 10000, 50000};
    int num_sizes = sizeof(sizes) / sizeof(sizes[0]);

    for (int s = 0; s < num_sizes; s++) {
        int size = sizes[s];
        printf("\nArray size: %d elements\n", size);
        printf("-----------------------------------------------------------------\n");

        // Create random array
        int* arr = (int*)malloc(size * sizeof(int));
        for (int i = 0; i < size; i++) {
            arr[i] = rand() % 10000;
        }

        // Test top-down mergesort
        int* arr_copy1 = (int*)malloc(size * sizeof(int));
        memcpy(arr_copy1, arr, size * sizeof(int));
        benchmark_sort(mergesort, arr_copy1, size, "Top-Down MergeSort");
        free(arr_copy1);

        // Test bottom-up mergesort
        int* arr_copy2 = (int*)malloc(size * sizeof(int));
        memcpy(arr_copy2, arr, size * sizeof(int));
        benchmark_bottomup(arr_copy2, size, "Bottom-Up MergeSort");
        free(arr_copy2);

        free(arr);
    }

    printf("\n=================================================================\n");
    printf("Key Points:\n");
    printf("- Time Complexity: O(n log n) for all cases (best, average, worst)\n");
    printf("- Space Complexity: O(n) - requires auxiliary array\n");
    printf("- Stable: Yes - maintains relative order of equal elements\n");
    printf("- Top-Down: Recursive, conceptually simple\n");
    printf("- Bottom-Up: Iterative, avoids recursion overhead\n");
    printf("- Best for: Linked lists, external sorting, when stability needed\n");
    printf("=================================================================\n");

    return 0;
}
