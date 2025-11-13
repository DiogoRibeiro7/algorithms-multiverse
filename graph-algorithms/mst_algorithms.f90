! ============================================================================
! Minimum Spanning Tree Algorithms in Modern Fortran
!
! Implementations of fundamental MST algorithms:
! - Kruskal's Algorithm (using Union-Find)
! - Prim's Algorithm (using priority queue)
!
! A Minimum Spanning Tree connects all vertices in a weighted graph
! with minimum total edge weight, without cycles.
!
! Compile: gfortran -O3 -o mst_algorithms mst_algorithms.f90
! Run: ./mst_algorithms
!
! @author Algorithms Multiverse
! @version 1.0
! ============================================================================

module mst_module
    implicit none
    private
    public :: kruskals_mst, prims_mst, print_mst
    public :: Edge

    ! Edge structure for Kruskal's algorithm
    type :: Edge
        integer :: u, v      ! vertices
        real(8) :: weight    ! edge weight
    end type Edge

contains

    ! ========================================================================
    ! KRUSKAL'S ALGORITHM
    ! ========================================================================

    subroutine kruskals_mst(edges, n_edges, n_vertices, mst, mst_size, mst_weight)
        ! Kruskal's MST algorithm using Union-Find
        !
        ! Time Complexity: O(E log E) for sorting edges
        ! Space Complexity: O(V + E)
        !
        ! Algorithm:
        ! 1. Sort all edges by weight
        ! 2. Initialize Union-Find structure
        ! 3. For each edge in sorted order:
        !    - If edge connects two different components, add to MST
        ! 4. Stop when MST has V-1 edges
        !
        ! Applications:
        ! - Network design (minimum cable length)
        ! - Clustering algorithms
        ! - Image segmentation
        implicit none
        type(Edge), intent(inout) :: edges(:)
        integer, intent(in) :: n_edges, n_vertices
        type(Edge), intent(out) :: mst(:)
        integer, intent(out) :: mst_size
        real(8), intent(out) :: mst_weight
        integer :: parent(n_vertices), rank(n_vertices)
        integer :: i, u_root, v_root

        ! Initialize Union-Find
        do i = 1, n_vertices
            parent(i) = i
            rank(i) = 0
        end do

        ! Sort edges by weight (simple bubble sort for clarity)
        call sort_edges(edges, n_edges)

        mst_size = 0
        mst_weight = 0.0d0

        ! Process edges in increasing order of weight
        do i = 1, n_edges
            u_root = find_set(parent, edges(i)%u)
            v_root = find_set(parent, edges(i)%v)

            ! If vertices are in different components
            if (u_root /= v_root) then
                mst_size = mst_size + 1
                mst(mst_size) = edges(i)
                mst_weight = mst_weight + edges(i)%weight
                call union_sets(parent, rank, u_root, v_root)

                ! MST complete when we have V-1 edges
                if (mst_size == n_vertices - 1) exit
            end if
        end do
    end subroutine kruskals_mst

    ! ========================================================================
    ! PRIM'S ALGORITHM
    ! ========================================================================

    subroutine prims_mst(graph, n_vertices, start, mst_edges, mst_size, mst_weight)
        ! Prim's MST algorithm
        !
        ! Time Complexity: O(V²) with adjacency matrix
        ! Space Complexity: O(V)
        !
        ! Algorithm:
        ! 1. Start with arbitrary vertex
        ! 2. Maintain set of vertices in MST
        ! 3. Repeatedly add minimum weight edge connecting
        !    MST to a vertex outside MST
        !
        ! Applications:
        ! - Network routing protocols
        ! - Approximation algorithms for TSP
        ! - Maze generation
        implicit none
        real(8), intent(in) :: graph(:,:)
        integer, intent(in) :: n_vertices, start
        type(Edge), intent(out) :: mst_edges(:)
        integer, intent(out) :: mst_size
        real(8), intent(out) :: mst_weight
        logical :: in_mst(n_vertices)
        real(8) :: key(n_vertices)
        integer :: parent(n_vertices)
        integer :: i, u, v, min_idx
        real(8) :: min_key
        real(8), parameter :: INF = 1.0d10

        ! Initialize
        in_mst = .false.
        key = INF
        parent = -1
        key(start) = 0.0d0

        mst_size = 0
        mst_weight = 0.0d0

        do i = 1, n_vertices
            ! Find minimum key vertex not in MST
            min_key = INF
            min_idx = -1

            do v = 1, n_vertices
                if (.not. in_mst(v) .and. key(v) < min_key) then
                    min_key = key(v)
                    min_idx = v
                end if
            end do

            if (min_idx == -1) exit  ! No more reachable vertices

            u = min_idx
            in_mst(u) = .true.

            ! Add edge to MST (except for first vertex)
            if (parent(u) /= -1) then
                mst_size = mst_size + 1
                mst_edges(mst_size)%u = parent(u)
                mst_edges(mst_size)%v = u
                mst_edges(mst_size)%weight = key(u)
                mst_weight = mst_weight + key(u)
            end if

            ! Update keys of adjacent vertices
            do v = 1, n_vertices
                if (.not. in_mst(v) .and. graph(u, v) > 0.0d0 .and. &
                    graph(u, v) < INF .and. graph(u, v) < key(v)) then
                    key(v) = graph(u, v)
                    parent(v) = u
                end if
            end do
        end do
    end subroutine prims_mst

    ! ========================================================================
    ! UNION-FIND DATA STRUCTURE (for Kruskal's algorithm)
    ! ========================================================================

    recursive function find_set(parent, x) result(root)
        ! Find operation with path compression
        !
        ! Time Complexity: O(α(n)) - inverse Ackermann function
        implicit none
        integer, intent(inout) :: parent(:)
        integer, intent(in) :: x
        integer :: root

        if (parent(x) /= x) then
            parent(x) = find_set(parent, parent(x))  ! Path compression
        end if
        root = parent(x)
    end function find_set

    subroutine union_sets(parent, rank, x, y)
        ! Union operation with union by rank
        !
        ! Time Complexity: O(α(n))
        implicit none
        integer, intent(inout) :: parent(:), rank(:)
        integer, intent(in) :: x, y

        ! Union by rank heuristic
        if (rank(x) < rank(y)) then
            parent(x) = y
        else if (rank(x) > rank(y)) then
            parent(y) = x
        else
            parent(y) = x
            rank(x) = rank(x) + 1
        end if
    end subroutine union_sets

    ! ========================================================================
    ! UTILITY FUNCTIONS
    ! ========================================================================

    subroutine sort_edges(edges, n)
        ! Simple bubble sort for edges by weight
        ! (Can be replaced with quicksort for large graphs)
        implicit none
        type(Edge), intent(inout) :: edges(:)
        integer, intent(in) :: n
        integer :: i, j
        type(Edge) :: temp

        do i = 1, n-1
            do j = 1, n-i
                if (edges(j)%weight > edges(j+1)%weight) then
                    temp = edges(j)
                    edges(j) = edges(j+1)
                    edges(j+1) = temp
                end if
            end do
        end do
    end subroutine sort_edges

    subroutine print_mst(mst, mst_size, mst_weight, algorithm_name)
        ! Print MST edges and total weight
        implicit none
        type(Edge), intent(in) :: mst(:)
        integer, intent(in) :: mst_size
        real(8), intent(in) :: mst_weight
        character(len=*), intent(in) :: algorithm_name
        integer :: i

        print *, ''
        print '(A)', trim(algorithm_name)
        print '(A)', repeat('-', 50)
        print '(A)', 'Edge       Weight'
        print '(A)', repeat('-', 50)

        do i = 1, mst_size
            write(*, '(I2, A, I2, 5X, F8.2)') &
                mst(i)%u-1, ' - ', mst(i)%v-1, mst(i)%weight
        end do

        print '(A)', repeat('-', 50)
        print '(A, F8.2)', 'Total MST Weight: ', mst_weight
    end subroutine print_mst

end module mst_module

! ============================================================================
! Main Program - Examples and Tests
! ============================================================================

program mst_demo
    use mst_module
    implicit none

    integer, parameter :: n_vertices = 9
    integer, parameter :: max_edges = 100
    real(8) :: graph(n_vertices, n_vertices)
    type(Edge) :: edges(max_edges), mst(n_vertices-1)
    integer :: n_edges, mst_size
    real(8) :: mst_weight
    integer :: i, j

    print '(A)', repeat('=', 70)
    print '(A)', '          MINIMUM SPANNING TREE ALGORITHMS IN FORTRAN'
    print '(A)', repeat('=', 70)
    print *

    ! Initialize graph
    graph = 0.0d0

    ! Build example graph (from CLRS textbook)
    ! Edge list for Kruskal's algorithm
    n_edges = 0

    ! Add edges (undirected graph)
    call add_edge(graph, edges, n_edges, 1, 2, 4.0d0)
    call add_edge(graph, edges, n_edges, 1, 8, 8.0d0)
    call add_edge(graph, edges, n_edges, 2, 3, 8.0d0)
    call add_edge(graph, edges, n_edges, 2, 8, 11.0d0)
    call add_edge(graph, edges, n_edges, 3, 4, 7.0d0)
    call add_edge(graph, edges, n_edges, 3, 6, 4.0d0)
    call add_edge(graph, edges, n_edges, 3, 9, 2.0d0)
    call add_edge(graph, edges, n_edges, 4, 5, 9.0d0)
    call add_edge(graph, edges, n_edges, 4, 6, 14.0d0)
    call add_edge(graph, edges, n_edges, 5, 6, 10.0d0)
    call add_edge(graph, edges, n_edges, 6, 7, 2.0d0)
    call add_edge(graph, edges, n_edges, 7, 8, 1.0d0)
    call add_edge(graph, edges, n_edges, 7, 9, 6.0d0)
    call add_edge(graph, edges, n_edges, 8, 9, 7.0d0)

    ! Print graph
    call print_graph(graph, n_vertices)

    ! Test Kruskal's algorithm
    print *
    print '(A)', 'Test 1: Kruskals MST Algorithm'
    call kruskals_mst(edges, n_edges, n_vertices, mst, mst_size, mst_weight)
    call print_mst(mst, mst_size, mst_weight, "Kruskal's Algorithm Result")

    ! Test Prim's algorithm
    print *
    print '(A)', 'Test 2: Prims MST Algorithm'
    call prims_mst(graph, n_vertices, 1, mst, mst_size, mst_weight)
    call print_mst(mst, mst_size, mst_weight, "Prim's Algorithm Result")

    print *
    print '(A)', repeat('=', 70)
    print '(A)', 'Key Points:'
    print '(A)', '- Kruskals: O(E log E), greedy edge-based approach'
    print '(A)', '- Prims: O(V²) with array, O((V+E)logV) with heap'
    print '(A)', '- Both produce same total weight (MST is unique for distinct weights)'
    print '(A)', '- Union-Find: Nearly O(1) amortized time per operation'
    print '(A)', '- Applications: Network design, clustering, approximation algorithms'
    print '(A)', repeat('=', 70)

contains

    subroutine add_edge(graph, edges, n_edges, u, v, weight)
        ! Add undirected edge to graph and edge list
        implicit none
        real(8), intent(inout) :: graph(:,:)
        type(Edge), intent(inout) :: edges(:)
        integer, intent(inout) :: n_edges
        integer, intent(in) :: u, v
        real(8), intent(in) :: weight

        graph(u, v) = weight
        graph(v, u) = weight

        n_edges = n_edges + 1
        edges(n_edges)%u = u
        edges(n_edges)%v = v
        edges(n_edges)%weight = weight
    end subroutine add_edge

    subroutine print_graph(graph, n)
        ! Print graph adjacency matrix
        implicit none
        real(8), intent(in) :: graph(:,:)
        integer, intent(in) :: n
        integer :: i, j

        print '(A)', 'Graph adjacency matrix (0 = no edge):'
        print *

        ! Print header
        write(*, '(A)', advance='no') '   '
        do j = 1, n
            write(*, '(I6)', advance='no') j-1
        end do
        print *

        ! Print matrix
        do i = 1, n
            write(*, '(I2, A)', advance='no') i-1, ': '
            do j = 1, n
                if (graph(i, j) == 0.0d0) then
                    write(*, '(A6)', advance='no') '  -  '
                else
                    write(*, '(F6.1)', advance='no') graph(i, j)
                end if
            end do
            print *
        end do
    end subroutine print_graph

end program mst_demo
