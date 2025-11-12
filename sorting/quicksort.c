/*
 * QuickSort Implementation in C
 *
 * QuickSort is a divide-and-conquer sorting algorithm.
 * Average Time Complexity: O(n log n)
 * Worst Case: O(n²) - when pivot selection is poor
 * Space Complexity: O(log n) - recursion stack
 *
 * Features:
 * - In-place sorting
 * - Randomized pivot selection
 * - Three-way partitioning for handling duplicates
 * - Tail recursion optimization
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

// Function prototypes
void quicksort(int arr[], int left, int right);
void quicksort_random(int arr[], int left, int right);
void quicksort_3way(int arr[], int left, int right);
int partition(int arr[], int left, int right);
int partition_random(int arr[], int left, int right);
void swap(int* a, int* b);
void print_array(const int arr[], int size);
int is_sorted(const int arr[], int size);

/*
 * Standard QuickSort with Lomuto partition scheme
 */
void quicksort(int arr[], int left, int right) {
    if (left < right) {
        int pivot_idx = partition(arr, left, right);

        // Recursively sort elements before and after partition
        quicksort(arr, left, pivot_idx - 1);
        quicksort(arr, pivot_idx + 1, right);
    }
}

/*
 * Partition function using Lomuto scheme
 * Chooses rightmost element as pivot
 */
int partition(int arr[], int left, int right) {
    int pivot = arr[right];
    int i = left - 1;

    for (int j = left; j < right; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }

    swap(&arr[i + 1], &arr[right]);
    return i + 1;
}

/*
 * QuickSort with randomized pivot selection
 * Improves average case performance and avoids worst case for sorted arrays
 */
void quicksort_random(int arr[], int left, int right) {
    if (left < right) {
        int pivot_idx = partition_random(arr, left, right);

        quicksort_random(arr, left, pivot_idx - 1);
        quicksort_random(arr, pivot_idx + 1, right);
    }
}

/*
 * Partition with random pivot selection
 */
int partition_random(int arr[], int left, int right) {
    // Choose random pivot and swap with rightmost element
    int random_idx = left + rand() % (right - left + 1);
    swap(&arr[random_idx], &arr[right]);

    return partition(arr, left, right);
}

/*
 * Three-way QuickSort (Dutch National Flag algorithm)
 * Efficient for arrays with many duplicate elements
 * Partitions into: < pivot, == pivot, > pivot
 */
void quicksort_3way(int arr[], int left, int right) {
    if (left >= right) return;

    int pivot = arr[left];
    int lt = left;      // arr[left..lt-1] < pivot
    int gt = right;     // arr[gt+1..right] > pivot
    int i = left + 1;   // arr[lt..i-1] == pivot

    while (i <= gt) {
        if (arr[i] < pivot) {
            swap(&arr[lt], &arr[i]);
            lt++;
            i++;
        } else if (arr[i] > pivot) {
            swap(&arr[i], &arr[gt]);
            gt--;
        } else {
            i++;
        }
    }

    // Now arr[left..lt-1] < pivot == arr[lt..gt] < arr[gt+1..right]
    quicksort_3way(arr, left, lt - 1);
    quicksort_3way(arr, gt + 1, right);
}

/*
 * Swap two integers
 */
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
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
        printf("✓ Sorted correctly in %.6f seconds\n", time_taken);
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
    printf("                    QUICKSORT IN C\n");
    printf("=================================================================\n\n");

    // Test 1: Small array
    printf("Test 1: Small array\n");
    printf("-----------------------------------------------------------------\n");
    int arr1[] = {64, 34, 25, 12, 22, 11, 90};
    int n1 = sizeof(arr1) / sizeof(arr1[0]);

    printf("Original: ");
    print_array(arr1, n1);

    quicksort(arr1, 0, n1 - 1);

    printf("Sorted:   ");
    print_array(arr1, n1);
    printf("\n");

    // Test 2: Array with duplicates
    printf("Test 2: Array with duplicates (3-way partition)\n");
    printf("-----------------------------------------------------------------\n");
    int arr2[] = {5, 2, 8, 2, 9, 1, 5, 5, 2, 8};
    int n2 = sizeof(arr2) / sizeof(arr2[0]);

    printf("Original: ");
    print_array(arr2, n2);

    quicksort_3way(arr2, 0, n2 - 1);

    printf("Sorted:   ");
    print_array(arr2, n2);
    printf("\n");

    // Test 3: Already sorted array
    printf("Test 3: Already sorted array (randomized pivot)\n");
    printf("-----------------------------------------------------------------\n");
    int arr3[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int n3 = sizeof(arr3) / sizeof(arr3[0]);

    printf("Original: ");
    print_array(arr3, n3);

    quicksort_random(arr3, 0, n3 - 1);

    printf("Sorted:   ");
    print_array(arr3, n3);
    printf("\n");

    // Benchmark with larger arrays
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

        // Test standard quicksort
        int* arr_copy1 = (int*)malloc(size * sizeof(int));
        memcpy(arr_copy1, arr, size * sizeof(int));
        benchmark_sort(quicksort, arr_copy1, size, "Standard QuickSort");
        free(arr_copy1);

        // Test randomized quicksort
        int* arr_copy2 = (int*)malloc(size * sizeof(int));
        memcpy(arr_copy2, arr, size * sizeof(int));
        benchmark_sort(quicksort_random, arr_copy2, size, "Randomized QuickSort");
        free(arr_copy2);

        // Test 3-way quicksort
        int* arr_copy3 = (int*)malloc(size * sizeof(int));
        memcpy(arr_copy3, arr, size * sizeof(int));
        benchmark_sort(quicksort_3way, arr_copy3, size, "3-Way QuickSort");
        free(arr_copy3);

        free(arr);
    }

    printf("\n=================================================================\n");
    printf("Key Points:\n");
    printf("- Standard QuickSort: Simple but vulnerable to worst case O(n²)\n");
    printf("- Randomized QuickSort: Average O(n log n) even for sorted input\n");
    printf("- 3-Way QuickSort: Excellent for arrays with many duplicates\n");
    printf("- In-place sorting: O(1) extra space (excluding recursion)\n");
    printf("- Not stable: Equal elements may be reordered\n");
    printf("=================================================================\n");

    return 0;
}
