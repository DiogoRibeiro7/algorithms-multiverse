/**
 * @file test_main.c
 * @brief Main test suite for Algorithms Multiverse C library
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <time.h>
#include "algorithms_multiverse.h"

/* Test result tracking */
static int tests_run = 0;
static int tests_passed = 0;
static int tests_failed = 0;

/* Macro for test assertions */
#define TEST_ASSERT(condition, message) do { \
    tests_run++; \
    if (condition) { \
        tests_passed++; \
        printf("  ✓ %s\n", message); \
    } else { \
        tests_failed++; \
        printf("  ✗ %s (line %d)\n", message, __LINE__); \
    } \
} while(0)

/* Test sorting algorithms */
void test_sorting(void) {
    printf("\n=== Testing Sorting Algorithms ===\n");

    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int expected[] = {11, 12, 22, 25, 34, 64, 90};
    size_t n = sizeof(arr) / sizeof(arr[0]);

    /* Test Bubble Sort */
    int* test_arr = malloc(n * sizeof(int));
    memcpy(test_arr, arr, n * sizeof(int));
    bubble_sort(test_arr, n);
    TEST_ASSERT(memcmp(test_arr, expected, n * sizeof(int)) == 0, "Bubble Sort");
    free(test_arr);

    /* Test Quick Sort */
    test_arr = malloc(n * sizeof(int));
    memcpy(test_arr, arr, n * sizeof(int));
    quick_sort(test_arr, n);
    TEST_ASSERT(memcmp(test_arr, expected, n * sizeof(int)) == 0, "Quick Sort");
    free(test_arr);

    /* Test Merge Sort */
    test_arr = malloc(n * sizeof(int));
    memcpy(test_arr, arr, n * sizeof(int));
    merge_sort(test_arr, n);
    TEST_ASSERT(memcmp(test_arr, expected, n * sizeof(int)) == 0, "Merge Sort");
    free(test_arr);

    /* Test Heap Sort */
    test_arr = malloc(n * sizeof(int));
    memcpy(test_arr, arr, n * sizeof(int));
    heap_sort(test_arr, n);
    TEST_ASSERT(memcmp(test_arr, expected, n * sizeof(int)) == 0, "Heap Sort");
    free(test_arr);

    /* Test is_sorted */
    TEST_ASSERT(is_sorted(expected, n), "is_sorted on sorted array");
    TEST_ASSERT(!is_sorted(arr, n), "is_sorted on unsorted array");
}

/* Test searching algorithms */
void test_searching(void) {
    printf("\n=== Testing Searching Algorithms ===\n");

    int arr[] = {10, 20, 30, 40, 50, 60, 70, 80, 90};
    size_t n = sizeof(arr) / sizeof(arr[0]);

    /* Test Binary Search */
    search_result_t result = binary_search(arr, n, 50);
    TEST_ASSERT(result.found && result.index == 4, "Binary Search - found");

    result = binary_search(arr, n, 55);
    TEST_ASSERT(!result.found, "Binary Search - not found");

    /* Test Linear Search */
    result = linear_search(arr, n, 30);
    TEST_ASSERT(result.found && result.index == 2, "Linear Search - found");

    result = linear_search(arr, n, 35);
    TEST_ASSERT(!result.found, "Linear Search - not found");

    /* Test Jump Search */
    result = jump_search(arr, n, 70);
    TEST_ASSERT(result.found && result.index == 6, "Jump Search");

    /* Test Interpolation Search */
    result = interpolation_search(arr, n, 40);
    TEST_ASSERT(result.found && result.index == 3, "Interpolation Search");

    /* Test finding min/max */
    int unsorted[] = {45, 23, 67, 12, 89, 34, 56};
    size_t m = sizeof(unsorted) / sizeof(unsorted[0]);
    TEST_ASSERT(find_min(unsorted, m) == 12, "Find minimum");
    TEST_ASSERT(find_max(unsorted, m) == 89, "Find maximum");

    /* Test finding kth element */
    TEST_ASSERT(find_kth_smallest(unsorted, m, 3) == 34, "Find 3rd smallest");
    TEST_ASSERT(find_kth_largest(unsorted, m, 2) == 67, "Find 2nd largest");
}

/* Test data structures */
void test_data_structures(void) {
    printf("\n=== Testing Data Structures ===\n");

    /* Test Stack */
    stack_t* stack = stack_create(5);
    TEST_ASSERT(stack != NULL, "Stack creation");
    TEST_ASSERT(stack_is_empty(stack), "Stack initially empty");

    stack_push(stack, (void*)10);
    stack_push(stack, (void*)20);
    stack_push(stack, (void*)30);
    TEST_ASSERT(stack_size(stack) == 3, "Stack size after push");
    TEST_ASSERT((intptr_t)stack_peek(stack) == 30, "Stack peek");
    TEST_ASSERT((intptr_t)stack_pop(stack) == 30, "Stack pop");
    TEST_ASSERT(stack_size(stack) == 2, "Stack size after pop");

    stack_destroy(stack);

    /* Test Queue */
    queue_t* queue = queue_create(5);
    TEST_ASSERT(queue != NULL, "Queue creation");
    TEST_ASSERT(queue_is_empty(queue), "Queue initially empty");

    queue_enqueue(queue, (void*)100);
    queue_enqueue(queue, (void*)200);
    queue_enqueue(queue, (void*)300);
    TEST_ASSERT(queue_size(queue) == 3, "Queue size after enqueue");
    TEST_ASSERT((intptr_t)queue_front(queue) == 100, "Queue front");
    TEST_ASSERT((intptr_t)queue_dequeue(queue) == 100, "Queue dequeue");
    TEST_ASSERT(queue_size(queue) == 2, "Queue size after dequeue");

    queue_destroy(queue);

    /* Test Hash Table */
    hash_table_t* ht = ht_create(10, hash_string_djb2, compare_string);
    TEST_ASSERT(ht != NULL, "Hash table creation");

    ht_insert(ht, "key1", "value1");
    ht_insert(ht, "key2", "value2");
    TEST_ASSERT(ht_size(ht) == 2, "Hash table size");
    TEST_ASSERT(strcmp(ht_get(ht, "key1"), "value1") == 0, "Hash table get");
    TEST_ASSERT(ht_contains(ht, "key2"), "Hash table contains");

    ht_delete(ht, "key1");
    TEST_ASSERT(!ht_contains(ht, "key1"), "Hash table delete");

    ht_destroy(ht);

    /* Test Priority Queue */
    priority_queue_t* pq = pq_create(10, compare_int);
    TEST_ASSERT(pq != NULL, "Priority queue creation");

    pq_insert(pq, (void*)30, 30);
    pq_insert(pq, (void*)10, 10);
    pq_insert(pq, (void*)20, 20);
    TEST_ASSERT(pq_size(pq) == 3, "Priority queue size");
    TEST_ASSERT((intptr_t)pq_extract(pq) == 10, "Priority queue extract min");

    pq_destroy(pq);
}

/* Test string algorithms */
void test_string_algorithms(void) {
    printf("\n=== Testing String Algorithms ===\n");

    /* Test pattern matching */
    const char* text = "ababcababa";
    const char* pattern = "aba";

    pattern_match_result_t* result = string_kmp_search(text, pattern);
    TEST_ASSERT(result != NULL && result->count == 3, "KMP pattern count");
    TEST_ASSERT(result->positions[0] == 0 && result->positions[1] == 5 &&
                result->positions[2] == 7, "KMP pattern positions");
    pattern_match_result_free(result);

    result = string_rabin_karp_search(text, pattern);
    TEST_ASSERT(result != NULL && result->count == 3, "Rabin-Karp pattern count");
    pattern_match_result_free(result);

    /* Test string distance */
    TEST_ASSERT(string_levenshtein_distance("kitten", "sitting") == 3,
                "Levenshtein distance");
    TEST_ASSERT(string_hamming_distance("abcd", "abxd") == 1,
                "Hamming distance");

    /* Test palindrome */
    TEST_ASSERT(string_is_palindrome("racecar"), "Palindrome positive");
    TEST_ASSERT(!string_is_palindrome("hello"), "Palindrome negative");

    /* Test string operations */
    char* reversed = string_reverse("hello");
    TEST_ASSERT(strcmp(reversed, "olleh") == 0, "String reverse");
    free(reversed);

    char* lower = string_to_lower("Hello World");
    TEST_ASSERT(strcmp(lower, "hello world") == 0, "String to lower");
    free(lower);

    char* upper = string_to_upper("Hello World");
    TEST_ASSERT(strcmp(upper, "HELLO WORLD") == 0, "String to upper");
    free(upper);

    char* trimmed = string_trim("  hello world  ");
    TEST_ASSERT(strcmp(trimmed, "hello world") == 0, "String trim");
    free(trimmed);

    /* Test string utilities */
    TEST_ASSERT(string_starts_with("hello world", "hello"), "String starts with");
    TEST_ASSERT(string_ends_with("hello world", "world"), "String ends with");
    TEST_ASSERT(string_count_words("hello world test") == 3, "Count words");
    TEST_ASSERT(string_is_anagram("listen", "silent"), "Is anagram");
}

/* Test numerical algorithms */
void test_numerical(void) {
    printf("\n=== Testing Numerical Algorithms ===\n");

    /* Test GCD/LCM */
    TEST_ASSERT(gcd(48, 18) == 6, "GCD(48, 18)");
    TEST_ASSERT(lcm(12, 15) == 60, "LCM(12, 15)");
    TEST_ASSERT(gcd(17, 19) == 1, "GCD of coprimes");

    /* Test modular arithmetic */
    TEST_ASSERT(mod_exp(3, 5, 7) == 5, "Modular exponentiation");
    TEST_ASSERT(mod_inverse(3, 7) == 5, "Modular inverse");

    /* Test prime functions */
    TEST_ASSERT(is_prime(17), "17 is prime");
    TEST_ASSERT(is_prime(97), "97 is prime");
    TEST_ASSERT(!is_prime(100), "100 is not prime");
    TEST_ASSERT(next_prime(14) == 17, "Next prime after 14");

    /* Test sieve of Eratosthenes */
    size_t count;
    size_t* primes = sieve_of_eratosthenes(30, &count);
    TEST_ASSERT(count == 10, "Number of primes <= 30");
    TEST_ASSERT(primes[0] == 2 && primes[1] == 3 && primes[9] == 29,
                "First and last primes");
    free(primes);

    /* Test factorization */
    int64_t* factors = prime_factorization(60, &count);
    TEST_ASSERT(count == 4, "Number of prime factors of 60");
    TEST_ASSERT(factors[0] == 2 && factors[1] == 2 &&
                factors[2] == 3 && factors[3] == 5,
                "Prime factors of 60");
    free(factors);

    /* Test combinatorics */
    TEST_ASSERT(factorial(5) == 120, "5! = 120");
    TEST_ASSERT(binomial_coefficient(10, 3) == 120, "C(10,3)");
    TEST_ASSERT(catalan_number(4) == 14, "4th Catalan number");

    /* Test Fibonacci */
    TEST_ASSERT(fibonacci(10) == 55, "10th Fibonacci number");
    TEST_ASSERT(lucas_number(5) == 11, "5th Lucas number");
    TEST_ASSERT(tribonacci(7) == 24, "7th Tribonacci number");

    /* Test Euler's totient */
    TEST_ASSERT(euler_totient(10) == 4, "φ(10) = 4");
    TEST_ASSERT(euler_totient(17) == 16, "φ(17) = 16 (prime)");
}

/* Summary of test results */
void print_summary(void) {
    printf("\n");
    printf("========================================\n");
    printf("           TEST SUMMARY\n");
    printf("========================================\n");
    printf("Tests run:    %d\n", tests_run);
    printf("Tests passed: %d\n", tests_passed);
    printf("Tests failed: %d\n", tests_failed);
    printf("Pass rate:    %.1f%%\n",
           tests_run > 0 ? (100.0 * tests_passed / tests_run) : 0.0);

    if (tests_failed == 0) {
        printf("\n✓✓✓ ALL TESTS PASSED ✓✓✓\n");
    } else {
        printf("\n✗✗✗ SOME TESTS FAILED ✗✗✗\n");
    }
    printf("========================================\n");
}

int main(void) {
    printf("========================================\n");
    printf("   ALGORITHMS MULTIVERSE - C Library\n");
    printf("           Test Suite\n");
    printf("========================================\n");

    /* Initialize library */
    am_init();

    /* Set seed for reproducible tests */
    am_set_random_seed(42);

    /* Run test suites */
    test_sorting();
    test_searching();
    test_data_structures();
    test_string_algorithms();
    test_numerical();

    /* Print summary */
    print_summary();

    /* Print memory stats */
    printf("\n");
    am_print_memory_stats();

    /* Clean up */
    am_cleanup();

    return tests_failed > 0 ? EXIT_FAILURE : EXIT_SUCCESS;
}