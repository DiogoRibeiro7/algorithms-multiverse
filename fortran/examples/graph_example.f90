! Example program demonstrating graph algorithms
program graph_example
    use iso_fortran_env, only: int32, real64
    use graph_module
    implicit none

    type(graph_type) :: g
    real(real64), allocatable :: distances(:)
    integer, allocatable :: predecessors(:), visited(:)
    type(weighted_edge_type), allocatable :: mst(:)
    real(real64) :: total_weight

    print '(A)', "========================================"
    print '(A)', "    Graph Algorithms Examples"
    print '(A)', "========================================"

    ! Example 1: Creating and traversing a graph
    print '(A)', ""
    print '(A)', "Example 1: Graph Creation and Traversal"
    print '(A)', "----------------------------------------"

    ! Create an undirected graph with 6 vertices
    call graph_create(g, 6, .false.)

    ! Add edges to form a connected graph
    call graph_add_edge(g, 1, 2, 1.0_real64)
    call graph_add_edge(g, 1, 3, 4.0_real64)
    call graph_add_edge(g, 2, 3, 2.0_real64)
    call graph_add_edge(g, 2, 4, 5.0_real64)
    call graph_add_edge(g, 3, 4, 1.0_real64)
    call graph_add_edge(g, 3, 5, 3.0_real64)
    call graph_add_edge(g, 4, 5, 2.0_real64)
    call graph_add_edge(g, 4, 6, 6.0_real64)
    call graph_add_edge(g, 5, 6, 1.0_real64)

    print '(A)', "Created graph with 6 vertices and 9 edges"

    ! Perform BFS from vertex 1
    allocate(visited(6))
    visited = 0
    call bfs(g, 1, visited)
    print '(A,6I3)', "BFS traversal order from vertex 1: ", visited

    ! Example 2: Shortest paths
    print '(A)', ""
    print '(A)', "Example 2: Shortest Path Algorithms"
    print '(A)', "------------------------------------"

    allocate(distances(6), predecessors(6))

    ! Find shortest paths from vertex 1 using Dijkstra
    call dijkstra_shortest_path(g, 1, distances, predecessors)

    print '(A)', "Shortest distances from vertex 1:"
    do i = 1, 6
        print '(A,I0,A,F6.2)', "  To vertex ", i, ": ", distances(i)
    end do

    ! Example 3: Minimum Spanning Tree
    print '(A)', ""
    print '(A)', "Example 3: Minimum Spanning Tree"
    print '(A)', "---------------------------------"

    allocate(mst(5))  ! MST will have n-1 edges

    ! Find MST using Kruskal's algorithm
    call kruskal_mst(g, mst, total_weight)

    print '(A,F6.2)', "MST total weight: ", total_weight
    print '(A)', "MST edges:"
    do i = 1, 5
        print '(A,I0,A,I0,A,F6.2)', "  Edge ", mst(i)%u, " - ", &
              mst(i)%v, ", weight: ", mst(i)%weight
    end do

    ! Example 4: Network flow
    print '(A)', ""
    print '(A)', "Example 4: Maximum Flow"
    print '(A)', "------------------------"

    ! Create a directed flow network
    call graph_create(g, 6, .true.)

    ! Add edges with capacities
    call graph_add_edge(g, 1, 2, 10.0_real64)  ! source to v2
    call graph_add_edge(g, 1, 3, 10.0_real64)  ! source to v3
    call graph_add_edge(g, 2, 3, 2.0_real64)
    call graph_add_edge(g, 2, 4, 4.0_real64)
    call graph_add_edge(g, 2, 5, 8.0_real64)
    call graph_add_edge(g, 3, 5, 9.0_real64)
    call graph_add_edge(g, 4, 6, 10.0_real64)  ! v4 to sink
    call graph_add_edge(g, 5, 4, 6.0_real64)
    call graph_add_edge(g, 5, 6, 10.0_real64)  ! v5 to sink

    total_weight = max_flow_ford_fulkerson(g, 1, 6)
    print '(A,F6.2)', "Maximum flow from vertex 1 to 6: ", total_weight

    ! Clean up
    deallocate(visited, distances, predecessors, mst)

    print '(A)', ""
    print '(A)', "========================================"
    print '(A)', "    Graph Examples Complete"
    print '(A)', "========================================"

contains
    integer :: i  ! Loop variable

end program graph_example