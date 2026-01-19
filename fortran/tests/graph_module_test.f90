! Test suite for graph algorithms module
program test_graph_module
    use iso_fortran_env, only: int32, real64
    use graph_module
    implicit none

    integer :: total_tests = 0, passed_tests = 0

    print '(A)', "========================================"
    print '(A)', "    Graph Module Test Suite"
    print '(A)', "========================================"

    call test_graph_creation()
    call test_bfs_dfs()
    call test_shortest_paths()
    call test_minimum_spanning_tree()
    call test_graph_properties()
    call test_flow_algorithms()

    print '(A)', ""
    print '(A)', "========================================"
    print '(A,I0,A,I0)', "Tests passed: ", passed_tests, "/", total_tests
    if (passed_tests == total_tests) then
        print '(A)', "STATUS: ALL TESTS PASSED ✓"
    else
        print '(A)', "STATUS: SOME TESTS FAILED ✗"
    end if
    print '(A)', "========================================"

contains

    subroutine test_graph_creation()
        type(graph_type) :: g
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Graph Creation..."

        ! Test undirected graph
        call graph_create(g, 5, .false.)
        call graph_add_edge(g, 1, 2, 1.0_real64)
        call graph_add_edge(g, 2, 3, 2.0_real64)
        call graph_add_edge(g, 3, 4, 1.5_real64)

        success = g%num_vertices == 5
        call report_test("Create undirected graph", success)

        ! Test directed graph
        call graph_create(g, 4, .true.)
        call graph_add_edge(g, 1, 2, 1.0_real64)
        call graph_add_edge(g, 2, 3, 1.0_real64)

        success = g%is_directed .and. g%num_vertices == 4
        call report_test("Create directed graph", success)

    end subroutine test_graph_creation

    subroutine test_bfs_dfs()
        type(graph_type) :: g
        integer, allocatable :: visited(:)
        integer :: path(10)
        integer :: path_length
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Graph Traversals..."

        ! Create test graph
        call graph_create(g, 6, .false.)
        call graph_add_edge(g, 1, 2, 1.0_real64)
        call graph_add_edge(g, 1, 3, 1.0_real64)
        call graph_add_edge(g, 2, 4, 1.0_real64)
        call graph_add_edge(g, 3, 4, 1.0_real64)
        call graph_add_edge(g, 4, 5, 1.0_real64)

        ! Test BFS
        allocate(visited(6))
        visited = 0
        call bfs(g, 1, visited)
        success = visited(1) > 0 .and. visited(5) > 0
        call report_test("Breadth-first search", success)

        ! Test DFS
        visited = 0
        call dfs(g, 1, visited)
        success = visited(1) > 0 .and. visited(5) > 0
        call report_test("Depth-first search", success)

        deallocate(visited)

    end subroutine test_bfs_dfs

    subroutine test_shortest_paths()
        type(graph_type) :: g
        real(real64), allocatable :: distances(:)
        integer, allocatable :: predecessors(:)
        real(real64) :: all_pairs(5,5)
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Shortest Path Algorithms..."

        ! Create weighted graph
        call graph_create(g, 5, .true.)
        call graph_add_edge(g, 1, 2, 4.0_real64)
        call graph_add_edge(g, 1, 3, 2.0_real64)
        call graph_add_edge(g, 2, 3, 1.0_real64)
        call graph_add_edge(g, 2, 4, 5.0_real64)
        call graph_add_edge(g, 3, 4, 8.0_real64)
        call graph_add_edge(g, 3, 5, 10.0_real64)
        call graph_add_edge(g, 4, 5, 2.0_real64)

        ! Test Dijkstra
        allocate(distances(5), predecessors(5))
        call dijkstra_shortest_path(g, 1, distances, predecessors)
        success = abs(distances(5) - 9.0_real64) < 1e-6
        call report_test("Dijkstra's shortest path", success)

        ! Test Bellman-Ford
        call bellman_ford(g, 1, distances, predecessors)
        success = abs(distances(5) - 9.0_real64) < 1e-6
        call report_test("Bellman-Ford shortest path", success)

        ! Test Floyd-Warshall
        call floyd_warshall(g, all_pairs)
        success = abs(all_pairs(1,5) - 9.0_real64) < 1e-6
        call report_test("Floyd-Warshall all pairs", success)

        deallocate(distances, predecessors)

    end subroutine test_shortest_paths

    subroutine test_minimum_spanning_tree()
        type(graph_type) :: g
        type(weighted_edge_type), allocatable :: mst(:)
        real(real64) :: total_weight
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Minimum Spanning Tree..."

        ! Create undirected weighted graph
        call graph_create(g, 5, .false.)
        call graph_add_edge(g, 1, 2, 2.0_real64)
        call graph_add_edge(g, 1, 3, 3.0_real64)
        call graph_add_edge(g, 2, 3, 1.0_real64)
        call graph_add_edge(g, 2, 4, 4.0_real64)
        call graph_add_edge(g, 3, 4, 2.0_real64)
        call graph_add_edge(g, 3, 5, 5.0_real64)
        call graph_add_edge(g, 4, 5, 3.0_real64)

        ! Test Kruskal's algorithm
        allocate(mst(4))
        call kruskal_mst(g, mst, total_weight)
        success = abs(total_weight - 8.0_real64) < 1e-6
        call report_test("Kruskal's MST", success)

        ! Test Prim's algorithm
        call prim_mst(g, mst, total_weight)
        success = abs(total_weight - 8.0_real64) < 1e-6
        call report_test("Prim's MST", success)

        deallocate(mst)

    end subroutine test_minimum_spanning_tree

    subroutine test_graph_properties()
        type(graph_type) :: g
        integer, allocatable :: order(:), components(:), colors(:)
        logical :: is_bipartite, success

        print '(A)', ""
        print '(A)', "Testing Graph Properties..."

        ! Test topological sort (DAG)
        call graph_create(g, 6, .true.)
        call graph_add_edge(g, 1, 2, 1.0_real64)
        call graph_add_edge(g, 1, 3, 1.0_real64)
        call graph_add_edge(g, 2, 4, 1.0_real64)
        call graph_add_edge(g, 3, 4, 1.0_real64)
        call graph_add_edge(g, 4, 5, 1.0_real64)
        call graph_add_edge(g, 5, 6, 1.0_real64)

        allocate(order(6))
        call topological_sort(g, order)
        success = order(1) == 1  ! First vertex should be 1 (no incoming edges)
        call report_test("Topological sort", success)

        ! Test strongly connected components
        allocate(components(6))
        call strongly_connected_components(g, components)
        success = maxval(components) >= 1
        call report_test("Strongly connected components", success)

        ! Test bipartite check
        call graph_create(g, 4, .false.)
        call graph_add_edge(g, 1, 2, 1.0_real64)
        call graph_add_edge(g, 2, 3, 1.0_real64)
        call graph_add_edge(g, 3, 4, 1.0_real64)
        call graph_add_edge(g, 4, 1, 1.0_real64)

        is_bipartite = bipartite_check(g)
        success = is_bipartite
        call report_test("Bipartite check", success)

        ! Test graph coloring
        allocate(colors(4))
        call graph_coloring(g, colors)
        success = maxval(colors) <= 2  ! Bipartite graph needs at most 2 colors
        call report_test("Graph coloring", success)

        deallocate(order, components, colors)

    end subroutine test_graph_properties

    subroutine test_flow_algorithms()
        type(graph_type) :: g
        real(real64) :: max_flow_value
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Flow Algorithms..."

        ! Create flow network
        call graph_create(g, 6, .true.)
        ! Source to intermediate nodes
        call graph_add_edge(g, 1, 2, 10.0_real64)
        call graph_add_edge(g, 1, 3, 10.0_real64)
        ! Intermediate edges
        call graph_add_edge(g, 2, 3, 2.0_real64)
        call graph_add_edge(g, 2, 4, 4.0_real64)
        call graph_add_edge(g, 2, 5, 8.0_real64)
        call graph_add_edge(g, 3, 5, 9.0_real64)
        ! To sink
        call graph_add_edge(g, 4, 6, 10.0_real64)
        call graph_add_edge(g, 5, 4, 6.0_real64)
        call graph_add_edge(g, 5, 6, 10.0_real64)

        max_flow_value = max_flow_ford_fulkerson(g, 1, 6)
        success = max_flow_value > 0.0_real64
        call report_test("Ford-Fulkerson max flow", success)

    end subroutine test_flow_algorithms

    subroutine report_test(test_name, success)
        character(len=*), intent(in) :: test_name
        logical, intent(in) :: success

        total_tests = total_tests + 1
        if (success) then
            passed_tests = passed_tests + 1
            print '(A,A,A)', "  ✓ ", test_name, " ... PASSED"
        else
            print '(A,A,A)', "  ✗ ", test_name, " ... FAILED"
        end if
    end subroutine report_test

end program test_graph_module