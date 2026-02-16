/**
 * @file test_new_modules.c
 * @brief Test suite for dynamic programming, graph, and matrix modules
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <math.h>
#include "algorithms_multiverse.h"
#include "dynamic_programming.h"
#include "graph.h"
#include "matrix.h"

/* Test result tracking */
static int tests_run = 0;
static int tests_passed = 0;
static int tests_failed = 0;

/* Test assertion macro */
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

#define EPSILON 1e-6

/* =========================== */
/*  Dynamic Programming Tests  */
/* =========================== */

void test_dynamic_programming(void) {
    printf("\n=== Testing Dynamic Programming ===\n");

    /* Test Fibonacci */
    TEST_ASSERT(dp_fibonacci(0) == 0, "Fibonacci(0) = 0");
    TEST_ASSERT(dp_fibonacci(1) == 1, "Fibonacci(1) = 1");
    TEST_ASSERT(dp_fibonacci(10) == 55, "Fibonacci(10) = 55");
    TEST_ASSERT(dp_fibonacci_memoized(15) == 610, "Fibonacci memoized(15) = 610");

    /* Test Climbing Stairs */
    TEST_ASSERT(dp_climbing_stairs(3) == 3, "Climbing stairs(3) = 3");
    TEST_ASSERT(dp_climbing_stairs(5) == 8, "Climbing stairs(5) = 8");
    TEST_ASSERT(dp_climbing_stairs_k_steps(4, 2) == 5, "Climbing stairs k=2, n=4");

    /* Test Subset Sum */
    int arr1[] = {3, 34, 4, 12, 5, 2};
    TEST_ASSERT(dp_subset_sum(arr1, 6, 9) == true, "Subset sum exists for sum=9");
    TEST_ASSERT(dp_subset_sum(arr1, 6, 30) == false, "Subset sum doesn't exist for sum=30");

    /* Test Partition Equal Subset */
    int arr2[] = {1, 5, 11, 5};
    TEST_ASSERT(dp_partition_equal_subset(arr2, 4) == true, "Can partition [1,5,11,5]");

    int arr3[] = {1, 2, 3, 5};
    TEST_ASSERT(dp_partition_equal_subset(arr3, 4) == false, "Cannot partition [1,2,3,5]");

    /* Test 0/1 Knapsack */
    int weights[] = {10, 20, 30};
    int values[] = {60, 100, 120};
    knapsack_result_t* knap_result = dp_knapsack_01(weights, values, 3, 50);
    TEST_ASSERT(knap_result != NULL && knap_result->total_value == 220,
                "Knapsack 0/1 max value = 220");
    knapsack_result_free(knap_result);

    /* Test Coin Change */
    int coins[] = {1, 2, 5};
    TEST_ASSERT(dp_coin_change_min_coins(coins, 3, 11) == 3,
                "Min coins for amount 11 = 3");
    TEST_ASSERT(dp_coin_change_count_ways(coins, 3, 5) == 4,
                "Ways to make amount 5 = 4");

    /* Test Longest Common Subsequence */
    char* lcs = NULL;
    size_t lcs_len = dp_longest_common_subsequence("ABCDGH", "AEDFHR", &lcs);
    TEST_ASSERT(lcs_len == 3, "LCS length of 'ABCDGH' and 'AEDFHR' = 3");
    TEST_ASSERT(lcs != NULL && strcmp(lcs, "ADH") == 0, "LCS is 'ADH'");
    free(lcs);

    /* Test Longest Increasing Subsequence */
    int arr4[] = {10, 9, 2, 5, 3, 7, 101, 18};
    int* lis = NULL;
    size_t lis_len = dp_longest_increasing_subsequence(arr4, 8, &lis);
    TEST_ASSERT(lis_len == 4, "LIS length = 4");
    free(lis);

    /* Test Edit Distance */
    TEST_ASSERT(dp_edit_distance("kitten", "sitting") == 3,
                "Edit distance between 'kitten' and 'sitting' = 3");
    TEST_ASSERT(dp_edit_distance("saturday", "sunday") == 3,
                "Edit distance between 'saturday' and 'sunday' = 3");

    /* Test Matrix Chain Multiplication */
    int dims[] = {10, 30, 5, 60};
    TEST_ASSERT(dp_matrix_chain_multiplication(dims, 4) == 4500,
                "Matrix chain multiplication min cost = 4500");

    /* Test Maximum Subarray (Kadane's) */
    int arr5[] = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    TEST_ASSERT(dp_maximum_subarray(arr5, 9) == 6,
                "Maximum subarray sum = 6");

    /* Test House Robber */
    int houses[] = {2, 7, 9, 3, 1};
    TEST_ASSERT(dp_house_robber(houses, 5) == 12,
                "House robber max = 12");

    /* Test Stock Buy/Sell */
    int prices[] = {7, 1, 5, 3, 6, 4};
    TEST_ASSERT(dp_stock_buy_sell_one_transaction(prices, 6) == 5,
                "Max profit with one transaction = 5");
    TEST_ASSERT(dp_stock_buy_sell_unlimited(prices, 6) == 7,
                "Max profit with unlimited transactions = 7");

    /* Test Unique Paths */
    TEST_ASSERT(dp_unique_paths(3, 7) == 28, "Unique paths in 3x7 grid = 28");
    TEST_ASSERT(dp_unique_paths(3, 3) == 6, "Unique paths in 3x3 grid = 6");
}

/* =========================== */
/*      Graph Tests            */
/* =========================== */

void test_graph_algorithms(void) {
    printf("\n=== Testing Graph Algorithms ===\n");

    /* Test Graph Creation */
    graph_t* g = graph_create(5, GRAPH_UNDIRECTED, GRAPH_ADJ_LIST);
    TEST_ASSERT(g != NULL, "Graph creation");
    TEST_ASSERT(graph_num_vertices(g) == 5, "Graph has 5 vertices");

    /* Test Edge Addition */
    TEST_ASSERT(graph_add_edge(g, 0, 1, 1.0), "Add edge 0-1");
    TEST_ASSERT(graph_add_edge(g, 0, 2, 1.0), "Add edge 0-2");
    TEST_ASSERT(graph_add_edge(g, 1, 3, 1.0), "Add edge 1-3");
    TEST_ASSERT(graph_add_edge(g, 2, 4, 1.0), "Add edge 2-4");
    TEST_ASSERT(graph_num_edges(g) == 4, "Graph has 4 edges");

    /* Test Edge Existence */
    TEST_ASSERT(graph_has_edge(g, 0, 1), "Edge 0-1 exists");
    TEST_ASSERT(graph_has_edge(g, 1, 0), "Edge 1-0 exists (undirected)");
    TEST_ASSERT(!graph_has_edge(g, 0, 3), "Edge 0-3 doesn't exist");

    /* Test Graph Connectivity */
    TEST_ASSERT(graph_is_connected(g), "Graph is connected");

    graph_destroy(g);

    /* Test Directed Graph */
    g = graph_create(4, GRAPH_DIRECTED, GRAPH_ADJ_MATRIX);
    TEST_ASSERT(g != NULL, "Directed graph creation");

    graph_add_edge(g, 0, 1, 1.0);
    graph_add_edge(g, 1, 2, 1.0);
    graph_add_edge(g, 2, 3, 1.0);

    TEST_ASSERT(graph_has_edge(g, 0, 1), "Directed edge 0->1 exists");
    TEST_ASSERT(!graph_has_edge(g, 1, 0), "Directed edge 1->0 doesn't exist");

    /* Test Topological Sort */
    bool has_cycle = false;
    size_t* topo = graph_topological_sort(g, &has_cycle);
    TEST_ASSERT(!has_cycle, "DAG has no cycle");
    TEST_ASSERT(topo != NULL, "Topological sort successful");
    free(topo);

    graph_destroy(g);

    /* Test Weighted Graph and Dijkstra */
    g = graph_create(5, GRAPH_DIRECTED_WEIGHTED, GRAPH_ADJ_LIST);
    graph_add_edge(g, 0, 1, 4.0);
    graph_add_edge(g, 0, 2, 2.0);
    graph_add_edge(g, 1, 2, 1.0);
    graph_add_edge(g, 1, 3, 5.0);
    graph_add_edge(g, 2, 3, 8.0);
    graph_add_edge(g, 2, 4, 10.0);
    graph_add_edge(g, 3, 4, 2.0);

    double* distances = graph_dijkstra(g, 0, NULL);
    TEST_ASSERT(distances != NULL, "Dijkstra algorithm runs");
    TEST_ASSERT(fabs(distances[0] - 0.0) < EPSILON, "Distance to source = 0");
    TEST_ASSERT(fabs(distances[1] - 4.0) < EPSILON, "Shortest path to 1 = 4");
    TEST_ASSERT(fabs(distances[2] - 2.0) < EPSILON, "Shortest path to 2 = 2");
    TEST_ASSERT(fabs(distances[3] - 9.0) < EPSILON, "Shortest path to 3 = 9");
    TEST_ASSERT(fabs(distances[4] - 11.0) < EPSILON, "Shortest path to 4 = 11");
    free(distances);

    graph_destroy(g);

    /* Test Minimum Spanning Tree */
    g = graph_create(4, GRAPH_UNDIRECTED | GRAPH_WEIGHTED, GRAPH_EDGE_LIST);
    graph_add_edge(g, 0, 1, 10.0);
    graph_add_edge(g, 0, 2, 6.0);
    graph_add_edge(g, 0, 3, 5.0);
    graph_add_edge(g, 1, 3, 15.0);
    graph_add_edge(g, 2, 3, 4.0);

    size_t mst_edges;
    double total_weight;
    edge_t* mst = graph_kruskal_mst(g, &mst_edges, &total_weight);
    TEST_ASSERT(mst != NULL, "Kruskal's MST");
    TEST_ASSERT(mst_edges == 3, "MST has 3 edges");
    TEST_ASSERT(fabs(total_weight - 19.0) < EPSILON, "MST total weight = 19");
    free(mst);

    mst = graph_prim_mst(g, &mst_edges, &total_weight);
    TEST_ASSERT(mst != NULL, "Prim's MST");
    TEST_ASSERT(mst_edges == 3, "Prim MST has 3 edges");
    TEST_ASSERT(fabs(total_weight - 19.0) < EPSILON, "Prim MST total weight = 19");
    free(mst);

    graph_destroy(g);

    /* Test Graph Generation */
    g = graph_generate_complete(4);
    TEST_ASSERT(g != NULL, "Complete graph K4");
    TEST_ASSERT(graph_num_edges(g) == 6, "K4 has 6 edges");
    graph_destroy(g);

    g = graph_generate_cycle(5);
    TEST_ASSERT(g != NULL, "Cycle graph C5");
    TEST_ASSERT(graph_num_edges(g) == 5, "C5 has 5 edges");
    graph_destroy(g);

    g = graph_generate_path(4);
    TEST_ASSERT(g != NULL, "Path graph P4");
    TEST_ASSERT(graph_num_edges(g) == 3, "P4 has 3 edges");
    graph_destroy(g);
}

/* =========================== */
/*      Matrix Tests           */
/* =========================== */

void test_matrix_operations(void) {
    printf("\n=== Testing Matrix Operations ===\n");

    /* Test Matrix Creation */
    matrix_t* m1 = matrix_create(3, 3);
    TEST_ASSERT(m1 != NULL, "Matrix creation 3x3");
    TEST_ASSERT(m1->rows == 3 && m1->cols == 3, "Matrix dimensions");

    /* Test Identity Matrix */
    matrix_t* id = matrix_create_identity(3);
    TEST_ASSERT(id != NULL, "Identity matrix creation");
    TEST_ASSERT(matrix_get(id, 0, 0) == 1.0, "Identity[0][0] = 1");
    TEST_ASSERT(matrix_get(id, 0, 1) == 0.0, "Identity[0][1] = 0");
    TEST_ASSERT(matrix_get(id, 1, 1) == 1.0, "Identity[1][1] = 1");

    /* Test Matrix Arithmetic */
    double data1[] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    double data2[] = {9, 8, 7, 6, 5, 4, 3, 2, 1};
    matrix_t* a = matrix_create_from_array(data1, 3, 3);
    matrix_t* b = matrix_create_from_array(data2, 3, 3);

    matrix_t* sum = matrix_add(a, b);
    TEST_ASSERT(sum != NULL, "Matrix addition");
    TEST_ASSERT(matrix_get(sum, 0, 0) == 10.0, "Sum[0][0] = 10");
    TEST_ASSERT(matrix_get(sum, 1, 1) == 10.0, "Sum[1][1] = 10");

    matrix_t* diff = matrix_subtract(a, b);
    TEST_ASSERT(diff != NULL, "Matrix subtraction");
    TEST_ASSERT(matrix_get(diff, 0, 0) == -8.0, "Diff[0][0] = -8");

    matrix_t* prod = matrix_multiply(a, id);
    TEST_ASSERT(prod != NULL, "Matrix multiplication with identity");
    TEST_ASSERT(matrix_equals(prod, a, EPSILON), "A * I = A");

    /* Test Matrix Transpose */
    matrix_t* trans = matrix_transpose(a);
    TEST_ASSERT(trans != NULL, "Matrix transpose");
    TEST_ASSERT(matrix_get(trans, 0, 1) == 4.0, "Transpose[0][1] = 4");
    TEST_ASSERT(matrix_get(trans, 1, 0) == 2.0, "Transpose[1][0] = 2");

    /* Test Matrix Properties */
    double det = matrix_determinant(a);
    TEST_ASSERT(fabs(det - 0.0) < EPSILON, "Determinant of singular matrix ≈ 0");

    double trace = matrix_trace(a);
    TEST_ASSERT(fabs(trace - 15.0) < EPSILON, "Trace = 15");

    /* Test Symmetric Matrix */
    double sym_data[] = {1, 2, 3, 2, 5, 6, 3, 6, 9};
    matrix_t* sym = matrix_create_from_array(sym_data, 3, 3);
    TEST_ASSERT(matrix_is_symmetric(sym), "Matrix is symmetric");

    /* Test Matrix Norms */
    double norm_f = matrix_norm_frobenius(a);
    TEST_ASSERT(norm_f > 0, "Frobenius norm > 0");

    double norm_1 = matrix_norm_1(a);
    TEST_ASSERT(fabs(norm_1 - 18.0) < EPSILON, "1-norm = 18");

    double norm_inf = matrix_norm_inf(a);
    TEST_ASSERT(fabs(norm_inf - 24.0) < EPSILON, "Inf-norm = 24");

    /* Test Matrix Decompositions */
    matrix_t* L = NULL;
    matrix_t* U = NULL;
    double lu_data[] = {2, 1, 1, 4, 3, 3, 8, 7, 9};
    matrix_t* lu_mat = matrix_create_from_array(lu_data, 3, 3);
    bool lu_success = matrix_lu_decomposition(lu_mat, &L, &U);
    TEST_ASSERT(lu_success, "LU decomposition successful");
    TEST_ASSERT(L != NULL && U != NULL, "L and U matrices created");

    /* Verify LU decomposition */
    matrix_t* lu_prod = matrix_multiply(L, U);
    TEST_ASSERT(matrix_equals(lu_prod, lu_mat, EPSILON), "L * U = A");

    /* Test Linear System Solver */
    double A_data[] = {2, 1, -1, -3, -1, 2, -2, 1, 2};
    double b_vec[] = {8, -11, -3};
    matrix_t* A_sys = matrix_create_from_array(A_data, 3, 3);
    double* x = matrix_solve_linear_system(A_sys, b_vec);
    TEST_ASSERT(x != NULL, "Linear system solution");
    /* Solution should be approximately [2, 3, -1] */
    TEST_ASSERT(fabs(x[0] - 2.0) < EPSILON, "x[0] ≈ 2");
    TEST_ASSERT(fabs(x[1] - 3.0) < EPSILON, "x[1] ≈ 3");
    TEST_ASSERT(fabs(x[2] + 1.0) < EPSILON, "x[2] ≈ -1");

    /* Test Matrix Inverse */
    double inv_data[] = {1, 2, 0, 0, 1, 0, 0, 0, 1};
    matrix_t* inv_mat = matrix_create_from_array(inv_data, 3, 3);
    matrix_t* inv = matrix_inverse(inv_mat);
    TEST_ASSERT(inv != NULL, "Matrix inverse exists");

    matrix_t* inv_prod = matrix_multiply(inv_mat, inv);
    TEST_ASSERT(matrix_is_diagonal(inv_prod), "A * A^-1 is diagonal");
    TEST_ASSERT(fabs(matrix_get(inv_prod, 0, 0) - 1.0) < EPSILON,
                "A * A^-1 diagonal = 1");

    /* Test Vector Operations */
    double v1[] = {1, 2, 3};
    double v2[] = {4, 5, 6};
    double dot = vector_dot_product(v1, v2, 3);
    TEST_ASSERT(fabs(dot - 32.0) < EPSILON, "Dot product = 32");

    double* cross = vector_cross_product(v1, v2);
    TEST_ASSERT(cross != NULL, "Cross product computed");
    TEST_ASSERT(fabs(cross[0] + 3.0) < EPSILON, "Cross[0] = -3");
    TEST_ASSERT(fabs(cross[1] - 6.0) < EPSILON, "Cross[1] = 6");
    TEST_ASSERT(fabs(cross[2] + 3.0) < EPSILON, "Cross[2] = -3");

    double norm = vector_norm(v1, 3);
    TEST_ASSERT(fabs(norm - sqrt(14.0)) < EPSILON, "Vector norm");

    /* Test Special Matrices */
    matrix_t* hilbert = matrix_hilbert(3);
    TEST_ASSERT(hilbert != NULL, "Hilbert matrix creation");
    TEST_ASSERT(fabs(matrix_get(hilbert, 0, 0) - 1.0) < EPSILON,
                "Hilbert[0][0] = 1");
    TEST_ASSERT(fabs(matrix_get(hilbert, 0, 1) - 0.5) < EPSILON,
                "Hilbert[0][1] = 1/2");
    TEST_ASSERT(fabs(matrix_get(hilbert, 1, 1) - 1.0/3.0) < EPSILON,
                "Hilbert[1][1] = 1/3");

    /* Clean up */
    matrix_destroy(m1);
    matrix_destroy(id);
    matrix_destroy(a);
    matrix_destroy(b);
    matrix_destroy(sum);
    matrix_destroy(diff);
    matrix_destroy(prod);
    matrix_destroy(trans);
    matrix_destroy(sym);
    matrix_destroy(L);
    matrix_destroy(U);
    matrix_destroy(lu_mat);
    matrix_destroy(lu_prod);
    matrix_destroy(A_sys);
    free(x);
    matrix_destroy(inv_mat);
    matrix_destroy(inv);
    matrix_destroy(inv_prod);
    free(cross);
    matrix_destroy(hilbert);
}

/* Summary of test results */
void print_summary(void) {
    printf("\n");
    printf("========================================\n");
    printf("         TEST SUMMARY\n");
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
    printf("     Test Suite for New Modules\n");
    printf("========================================\n");

    /* Initialize library */
    am_init();

    /* Run test suites */
    test_dynamic_programming();
    test_graph_algorithms();
    test_matrix_operations();

    /* Print summary */
    print_summary();

    /* Clean up */
    am_cleanup();

    return tests_failed > 0 ? EXIT_FAILURE : EXIT_SUCCESS;
}