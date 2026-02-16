/**
 * @file comprehensive_example.c
 * @brief Comprehensive example demonstrating the Algorithms Multiverse C library
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "algorithms_multiverse.h"

/* Function to print an array */
void print_array(const int* arr, size_t n, const char* label) {
    printf("%s: ", label);
    for (size_t i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

/* Sorting examples */
void sorting_examples(void) {
    printf("\n=== SORTING ALGORITHMS ===\n");

    int data[] = {64, 34, 25, 12, 22, 11, 90, 88, 45, 50};
    size_t n = sizeof(data) / sizeof(data[0]);

    /* Create copies for different sorting algorithms */
    int* arr1 = malloc(n * sizeof(int));
    int* arr2 = malloc(n * sizeof(int));
    int* arr3 = malloc(n * sizeof(int));

    memcpy(arr1, data, n * sizeof(int));
    memcpy(arr2, data, n * sizeof(int));
    memcpy(arr3, data, n * sizeof(int));

    print_array(data, n, "Original array");

    /* Quick Sort */
    quick_sort(arr1, n);
    print_array(arr1, n, "Quick Sort");

    /* Merge Sort */
    merge_sort(arr2, n);
    print_array(arr2, n, "Merge Sort");

    /* Heap Sort */
    heap_sort(arr3, n);
    print_array(arr3, n, "Heap Sort");

    /* Verify all sorts produced same result */
    printf("All sorts consistent: %s\n",
           memcmp(arr1, arr2, n * sizeof(int)) == 0 &&
           memcmp(arr2, arr3, n * sizeof(int)) == 0 ? "Yes" : "No");

    free(arr1);
    free(arr2);
    free(arr3);
}

/* Searching examples */
void searching_examples(void) {
    printf("\n=== SEARCHING ALGORITHMS ===\n");

    int arr[] = {2, 3, 4, 10, 20, 30, 40, 50, 60, 70};
    size_t n = sizeof(arr) / sizeof(arr[0]);
    int target = 30;

    print_array(arr, n, "Sorted array");
    printf("Target: %d\n", target);

    /* Linear Search */
    search_result_t result = linear_search(arr, n, target);
    printf("Linear Search: %s at index %zu (comparisons: %zu)\n",
           result.found ? "Found" : "Not found",
           result.index, result.comparisons);

    /* Binary Search */
    result = binary_search(arr, n, target);
    printf("Binary Search: %s at index %zu (comparisons: %zu)\n",
           result.found ? "Found" : "Not found",
           result.index, result.comparisons);

    /* Jump Search */
    result = jump_search(arr, n, target);
    printf("Jump Search: %s at index %zu (comparisons: %zu)\n",
           result.found ? "Found" : "Not found",
           result.index, result.comparisons);

    /* Interpolation Search */
    result = interpolation_search(arr, n, target);
    printf("Interpolation Search: %s at index %zu (comparisons: %zu)\n",
           result.found ? "Found" : "Not found",
           result.index, result.comparisons);
}

/* Data structure examples */
void data_structure_examples(void) {
    printf("\n=== DATA STRUCTURES ===\n");

    /* Stack example */
    printf("\nStack operations:\n");
    stack_t* stack = stack_create(5);
    stack_push(stack, (void*)(intptr_t)10);
    stack_push(stack, (void*)(intptr_t)20);
    stack_push(stack, (void*)(intptr_t)30);

    printf("Stack size: %zu\n", stack_size(stack));
    printf("Popped: %d\n", (int)(intptr_t)stack_pop(stack));
    printf("Top element: %d\n", (int)(intptr_t)stack_peek(stack));

    stack_destroy(stack);

    /* Queue example */
    printf("\nQueue operations:\n");
    queue_t* queue = queue_create(5);
    queue_enqueue(queue, (void*)(intptr_t)100);
    queue_enqueue(queue, (void*)(intptr_t)200);
    queue_enqueue(queue, (void*)(intptr_t)300);

    printf("Queue size: %zu\n", queue_size(queue));
    printf("Dequeued: %d\n", (int)(intptr_t)queue_dequeue(queue));
    printf("Front element: %d\n", (int)(intptr_t)queue_front(queue));

    queue_destroy(queue);

    /* Hash Table example */
    printf("\nHash Table operations:\n");
    hash_table_t* ht = ht_create(10, hash_string_djb2, compare_string);

    ht_insert(ht, "key1", "value1");
    ht_insert(ht, "key2", "value2");
    ht_insert(ht, "key3", "value3");

    printf("Hash table size: %zu\n", ht_size(ht));
    printf("Value for 'key2': %s\n", (char*)ht_get(ht, "key2"));
    printf("Contains 'key3': %s\n", ht_contains(ht, "key3") ? "Yes" : "No");

    ht_delete(ht, "key2");
    printf("After deleting 'key2', size: %zu\n", ht_size(ht));

    ht_destroy(ht);
}

/* String algorithm examples */
void string_examples(void) {
    printf("\n=== STRING ALGORITHMS ===\n");

    const char* text = "The quick brown fox jumps over the lazy dog";
    const char* pattern = "fox";

    printf("Text: \"%s\"\n", text);
    printf("Pattern: \"%s\"\n", pattern);

    /* Pattern matching */
    printf("\nPattern Matching:\n");

    pattern_match_result_t* matches = string_kmp_search(text, pattern);
    printf("KMP Search - Found %zu matches at positions: ", matches->count);
    for (size_t i = 0; i < matches->count; i++) {
        printf("%zu ", matches->positions[i]);
    }
    printf("\n");
    pattern_match_result_free(matches);

    matches = string_rabin_karp_search(text, pattern);
    printf("Rabin-Karp - Found %zu matches at positions: ", matches->count);
    for (size_t i = 0; i < matches->count; i++) {
        printf("%zu ", matches->positions[i]);
    }
    printf("\n");
    pattern_match_result_free(matches);

    /* String distances */
    printf("\nString Distances:\n");
    const char* s1 = "kitten";
    const char* s2 = "sitting";

    printf("Levenshtein distance between '%s' and '%s': %zu\n",
           s1, s2, string_levenshtein_distance(s1, s2));

    /* Palindrome check */
    printf("\nPalindrome Check:\n");
    const char* palindrome = "racecar";
    const char* not_palindrome = "hello";

    printf("'%s' is palindrome: %s\n",
           palindrome, string_is_palindrome(palindrome) ? "Yes" : "No");
    printf("'%s' is palindrome: %s\n",
           not_palindrome, string_is_palindrome(not_palindrome) ? "Yes" : "No");

    /* String hashing */
    printf("\nString Hashing:\n");
    const char* hash_str = "Hello, World!";
    printf("DJB2 hash of '%s': 0x%08X\n", hash_str, string_hash_djb2(hash_str));
    printf("FNV1a hash of '%s': 0x%08X\n", hash_str, string_hash_fnv1a(hash_str));
}

/* Numerical algorithm examples */
void numerical_examples(void) {
    printf("\n=== NUMERICAL ALGORITHMS ===\n");

    /* Basic arithmetic */
    printf("\nBasic Arithmetic:\n");
    printf("GCD(48, 18) = %lld\n", gcd(48, 18));
    printf("LCM(12, 15) = %lld\n", lcm(12, 15));
    printf("2^10 = %lld\n", fast_power(2, 10));
    printf("3^5 mod 7 = %lld\n", mod_exp(3, 5, 7));

    /* Prime numbers */
    printf("\nPrime Numbers:\n");
    printf("Is 97 prime? %s\n", is_prime(97) ? "Yes" : "No");
    printf("Is 100 prime? %s\n", is_prime(100) ? "Yes" : "No");

    /* Find first 20 primes */
    size_t count;
    size_t* primes = sieve_of_eratosthenes(100, &count);
    printf("First 20 primes: ");
    for (size_t i = 0; i < 20 && i < count; i++) {
        printf("%zu ", primes[i]);
    }
    printf("\n");
    free(primes);

    /* Prime factorization */
    int64_t* factors = prime_factorization(60, &count);
    printf("Prime factorization of 60: ");
    for (size_t i = 0; i < count; i++) {
        printf("%lld ", factors[i]);
    }
    printf("\n");
    free(factors);

    /* Combinatorics */
    printf("\nCombinatorics:\n");
    printf("10! = %lld\n", factorial(10));
    printf("C(10, 3) = %lld\n", binomial_coefficient(10, 3));
    printf("5th Catalan number = %lld\n", catalan_number(5));

    /* Number sequences */
    printf("\nNumber Sequences:\n");
    printf("First 10 Fibonacci numbers: ");
    for (int i = 0; i < 10; i++) {
        printf("%lld ", fibonacci(i));
    }
    printf("\n");

    /* Numerical integration example */
    printf("\nNumerical Integration:\n");
    /* Integrate x^2 from 0 to 1 (should be 1/3 ≈ 0.333) */
    double integral = trapezoidal_rule(
        [](double x) { return x * x; }, 0, 1, 100);
    printf("∫x² dx from 0 to 1 (Trapezoidal): %.6f\n", integral);

    integral = simpson_rule(
        [](double x) { return x * x; }, 0, 1, 100);
    printf("∫x² dx from 0 to 1 (Simpson): %.6f\n", integral);
}

/* Benchmark sorting algorithms */
void benchmark_sorting(void) {
    printf("\n=== SORTING BENCHMARKS ===\n");

    size_t sizes[] = {100, 1000, 10000};
    sort_algorithm_t algorithms[] = {
        SORT_BUBBLE, SORT_INSERTION, SORT_SELECTION,
        SORT_MERGE, SORT_QUICK, SORT_HEAP
    };
    const char* names[] = {
        "Bubble Sort", "Insertion Sort", "Selection Sort",
        "Merge Sort", "Quick Sort", "Heap Sort"
    };

    for (size_t s = 0; s < 3; s++) {
        size_t n = sizes[s];
        printf("\nArray size: %zu\n", n);

        /* Generate random array */
        int* arr = generate_random_array(n, 0, 1000);

        for (int a = 0; a < 6; a++) {
            /* Skip slow algorithms for large sizes */
            if (n > 1000 && a < 3) continue;

            sort_stats_t stats = benchmark_sort(algorithms[a], arr, n);
            printf("  %-15s: %.3f ms\n", names[a], stats.time_ms);
        }

        free(arr);
    }
}

int main(void) {
    printf("========================================\n");
    printf("   ALGORITHMS MULTIVERSE - C Library\n");
    printf("        Comprehensive Examples\n");
    printf("========================================\n");

    /* Initialize library */
    am_init();

    /* Set random seed for reproducible results */
    srand(time(NULL));

    /* Run examples */
    sorting_examples();
    searching_examples();
    data_structure_examples();
    string_examples();
    numerical_examples();
    benchmark_sorting();

    /* Clean up */
    am_cleanup();

    printf("\n========================================\n");
    printf("        Examples Complete!\n");
    printf("========================================\n");

    return 0;
}