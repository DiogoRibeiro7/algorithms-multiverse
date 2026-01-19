! Algorithms Multiverse - Fortran Implementation
! Main module that exports all algorithm implementations
! Uses modern Fortran 2008/2018 features

module algorithms_multiverse
    use iso_fortran_env, only: int32, int64, real32, real64
    use sorting_module
    use searching_module
    use numerical_module
    use matrix_module
    use dynamic_programming_module
    use graph_module
    use string_module
    use crypto_module
    use geometry_module
    use data_structures_module
    use statistics_module
    use optimization_module
    use streaming_module
    implicit none
    private

    ! Module version information
    character(len=*), parameter, public :: VERSION = "1.0.0"
    character(len=*), parameter, public :: AUTHOR = "Algorithms Multiverse"

    ! Re-export all public interfaces
    ! Sorting algorithms
    public :: quick_sort, merge_sort, heap_sort, insertion_sort, bubble_sort
    public :: shell_sort, radix_sort, counting_sort, bucket_sort

    ! Searching algorithms
    public :: binary_search, linear_search, jump_search, interpolation_search
    public :: fibonacci_search, exponential_search, ternary_search

    ! Numerical algorithms
    public :: gcd, lcm, is_prime, sieve_of_eratosthenes, prime_factorization
    public :: factorial, binomial_coefficient, fast_power, modular_exponentiation

    ! Matrix operations
    public :: matrix_multiply, matrix_transpose, matrix_inverse, lu_decomposition
    public :: gaussian_elimination, jacobi_iteration, gauss_seidel

    ! Dynamic programming
    public :: fibonacci_dp, knapsack, longest_common_subsequence, edit_distance
    public :: matrix_chain_multiplication, coin_change

    ! Graph algorithms
    public :: graph_type, weighted_edge_type
    public :: graph_create, graph_add_edge, graph_add_vertex
    public :: bfs, dfs, dijkstra_shortest_path, bellman_ford
    public :: floyd_warshall, kruskal_mst, prim_mst, topological_sort
    public :: strongly_connected_components, articulation_points
    public :: bipartite_check, graph_coloring, max_flow_ford_fulkerson

    ! String algorithms
    public :: kmp_search, rabin_karp_search, boyer_moore_search
    public :: longest_common_substring, longest_palindromic_substring
    public :: is_palindrome, levenshtein_distance, string_permutations
    public :: string_combinations, z_algorithm, manacher_algorithm
    public :: suffix_array_build, lcp_array_build, aho_corasick_search

    ! Cryptographic algorithms
    public :: caesar_cipher_encrypt, caesar_cipher_decrypt
    public :: vigenere_encrypt, vigenere_decrypt
    public :: xor_cipher, substitution_cipher_encrypt, substitution_cipher_decrypt
    public :: simple_hash, djb2_hash, generate_rsa_keys, rsa_encrypt, rsa_decrypt

    ! Geometry algorithms
    public :: point_2d_type, point_3d_type, line_2d_type, circle_type, polygon_type
    public :: distance_2d, distance_3d, cross_product_2d, dot_product_2d
    public :: point_in_polygon, convex_hull_graham_scan, convex_hull_jarvis_march
    public :: line_intersection, circle_intersection, closest_pair_of_points
    public :: polygon_area, polygon_perimeter, segment_intersection
    public :: kd_tree_type, kd_tree_build, kd_tree_nearest_neighbor
    public :: quad_tree_type, quad_tree_insert, quad_tree_query_range

    ! Data structures
    public :: stack_type, queue_type, priority_queue_type, deque_type
    public :: linked_list_type, doubly_linked_list_type
    public :: binary_tree_type, bst_type, avl_tree_type
    public :: trie_type, hash_table_type, disjoint_set_type
    public :: segment_tree_type, fenwick_tree_type

    ! Statistics algorithms
    public :: mean, median, mode, variance, std_dev, covariance
    public :: correlation, percentile, z_score, t_test_one_sample
    public :: t_test_two_sample, chi_square_test, anova_one_way
    public :: linear_regression, polynomial_regression, exponential_regression
    public :: moving_average, exponential_smoothing, autocorrelation
    public :: k_means_clustering, hierarchical_clustering, dbscan_clustering
    public :: pca_transform, hypothesis_test_result

    ! Optimization algorithms
    public :: golden_section_search, gradient_descent, newton_method_optimization
    public :: conjugate_gradient_minimize, bfgs_minimize
    public :: linear_programming_simplex, nelder_mead_simplex
    public :: differential_evolution, particle_swarm_optimization
    public :: genetic_algorithm, simulated_annealing, tabu_search
    public :: ant_colony_optimization, branch_and_bound

    ! Streaming algorithms
    public :: reservoir_sample, weighted_reservoir_sample
    public :: count_min_sketch_type, hyperloglog_type, streaming_stats_type
    public :: sliding_window_type, tdigest_type, space_saving_type
    public :: cms_create, cms_update, cms_query
    public :: hll_create, hll_add, hll_estimate_cardinality
    public :: streaming_mean, streaming_variance, streaming_median_approximate
    public :: frequent_items_misra_gries

    ! Public types
    public :: matrix_type, sparse_matrix_type

contains

    ! Utility function to print algorithm statistics
    subroutine print_statistics()
        implicit none

        print '(A)', "========================================="
        print '(A)', "  Algorithms Multiverse - Fortran"
        print '(A)', "========================================="
        print '(A,A)', "Version: ", VERSION
        print '(A,A)', "Author: ", AUTHOR
        print '(A)', ""
        print '(A)', "Available Modules:"
        print '(A)', "  - Sorting Algorithms (10+ implementations)"
        print '(A)', "  - Searching Algorithms (7+ implementations)"
        print '(A)', "  - Numerical Algorithms (15+ implementations)"
        print '(A)', "  - Matrix Operations (10+ implementations)"
        print '(A)', "  - Dynamic Programming (8+ implementations)"
        print '(A)', "  - Graph Algorithms (15+ implementations)"
        print '(A)', "  - String Algorithms (12+ implementations)"
        print '(A)', "  - Cryptographic Algorithms (10+ implementations)"
        print '(A)', "  - Geometry Algorithms (15+ implementations)"
        print '(A)', "  - Data Structures (14+ implementations)"
        print '(A)', "  - Statistics Algorithms (20+ implementations)"
        print '(A)', "  - Optimization Algorithms (14+ implementations)"
        print '(A)', "  - Streaming Algorithms (10+ implementations)"
        print '(A)', "========================================="

    end subroutine print_statistics

    ! Benchmark utility for timing algorithms
    subroutine benchmark_algorithm(algorithm_name, start_time, end_time, n)
        implicit none
        character(len=*), intent(in) :: algorithm_name
        real(real64), intent(in) :: start_time, end_time
        integer(int32), intent(in) :: n
        real(real64) :: elapsed_time

        elapsed_time = end_time - start_time

        print '(A,A,A)', "Algorithm: ", algorithm_name
        print '(A,I0)', "  Input size: ", n
        print '(A,F12.9,A)', "  Time: ", elapsed_time, " seconds"
        print '(A,F12.3,A)', "  Rate: ", real(n, real64) / elapsed_time / 1e6, " million ops/sec"

    end subroutine benchmark_algorithm

end module algorithms_multiverse