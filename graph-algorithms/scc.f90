! ============================================================================
! Strongly Connected Components (SCC) Algorithms in Modern Fortran
!
! Implementations:
! - Tarjan's Algorithm (single DFS pass)
! - Kosaraju's Algorithm (two DFS passes)
!
! A Strongly Connected Component is a maximal subgraph where every vertex
! is reachable from every other vertex in the subgraph.
!
! Compile: gfortran -O3 -o scc scc.f90
! Run: ./scc
!
! @author Algorithms Multiverse
! @version 1.0
! ============================================================================

module scc_module
    implicit none
    private
    public :: tarjans_scc, kosarajus_scc, print_sccs

contains

    ! ========================================================================
    ! TARJAN'S ALGORITHM
    ! ========================================================================

    subroutine tarjans_scc(graph, n, scc_ids, num_sccs)
        ! Find strongly connected components using Tarjan's algorithm
        !
        ! Time Complexity: O(V + E)
        ! Space Complexity: O(V)
        !
        ! Algorithm:
        ! 1. Perform DFS, maintaining discovery time and low-link value
        ! 2. Use a stack to track vertices in current SCC
        ! 3. When low[v] = disc[v], we found root of SCC
        ! 4. Pop stack until we reach v to get all vertices in SCC
        !
        ! Applications:
        ! - Finding cycles in directed graphs
        ! - Checking if graph is strongly connected
        ! - Decomposing graphs into components
        ! - Social network analysis
        implicit none
        integer, intent(in) :: graph(:,:), n
        integer, intent(out) :: scc_ids(:)
        integer, intent(out) :: num_sccs
        integer :: disc(n), low(n), stack(n), top
        logical :: visited(n), on_stack(n)
        integer :: time_counter, i

        ! Initialize
        visited = .false.
        on_stack = .false.
        disc = -1
        low = -1
        top = 0
        time_counter = 0
        num_sccs = 0

        ! Run DFS from each unvisited vertex
        do i = 1, n
            if (.not. visited(i)) then
                call tarjan_dfs(graph, n, i, visited, disc, low, stack, top, &
                               on_stack, time_counter, scc_ids, num_sccs)
            end if
        end do
    end subroutine tarjans_scc

    recursive subroutine tarjan_dfs(graph, n, u, visited, disc, low, stack, &
                                     top, on_stack, time_counter, scc_ids, num_sccs)
        ! DFS for Tarjan's algorithm
        implicit none
        integer, intent(in) :: graph(:,:), n, u
        logical, intent(inout) :: visited(:), on_stack(:)
        integer, intent(inout) :: disc(:), low(:), stack(:), top
        integer, intent(inout) :: time_counter, scc_ids(:), num_sccs
        integer :: v, w

        ! Initialize discovery time and low value
        visited(u) = .true.
        time_counter = time_counter + 1
        disc(u) = time_counter
        low(u) = time_counter

        ! Push to stack
        top = top + 1
        stack(top) = u
        on_stack(u) = .true.

        ! Visit all neighbors
        do v = 1, n
            if (graph(u, v) /= 0) then
                if (.not. visited(v)) then
                    ! Tree edge
                    call tarjan_dfs(graph, n, v, visited, disc, low, stack, &
                                   top, on_stack, time_counter, scc_ids, num_sccs)
                    low(u) = min(low(u), low(v))
                else if (on_stack(v)) then
                    ! Back edge to vertex in current SCC
                    low(u) = min(low(u), disc(v))
                end if
            end if
        end do

        ! If u is root of SCC
        if (low(u) == disc(u)) then
            num_sccs = num_sccs + 1

            ! Pop stack until we reach u
            do
                w = stack(top)
                top = top - 1
                on_stack(w) = .false.
                scc_ids(w) = num_sccs

                if (w == u) exit
            end do
        end if
    end subroutine tarjan_dfs

    ! ========================================================================
    ! KOSARAJU'S ALGORITHM
    ! ========================================================================

    subroutine kosarajus_scc(graph, n, scc_ids, num_sccs)
        ! Find strongly connected components using Kosaraju's algorithm
        !
        ! Time Complexity: O(V + E)
        ! Space Complexity: O(V + E)
        !
        ! Algorithm:
        ! 1. Perform DFS on original graph, record finish times
        ! 2. Transpose the graph (reverse all edges)
        ! 3. Perform DFS on transposed graph in decreasing finish time order
        ! 4. Each DFS tree in step 3 is an SCC
        !
        ! Applications: Same as Tarjan's algorithm
        implicit none
        integer, intent(in) :: graph(:,:), n
        integer, intent(out) :: scc_ids(:)
        integer, intent(out) :: num_sccs
        integer :: finish_order(n), finish_time
        integer :: transposed(n, n)
        logical :: visited(n)
        integer :: i, u

        ! Step 1: First DFS to get finish times
        visited = .false.
        finish_time = 0
        do i = 1, n
            if (.not. visited(i)) then
                call kosaraju_dfs1(graph, n, i, visited, finish_order, finish_time)
            end if
        end do

        ! Step 2: Transpose graph
        call transpose_graph(graph, transposed, n)

        ! Step 3: Second DFS on transposed graph in reverse finish order
        visited = .false.
        num_sccs = 0

        do i = n, 1, -1
            u = finish_order(i)
            if (.not. visited(u)) then
                num_sccs = num_sccs + 1
                call kosaraju_dfs2(transposed, n, u, visited, scc_ids, num_sccs)
            end if
        end do
    end subroutine kosarajus_scc

    recursive subroutine kosaraju_dfs1(graph, n, u, visited, finish_order, finish_time)
        ! First DFS for Kosaraju's algorithm - compute finish times
        implicit none
        integer, intent(in) :: graph(:,:), n, u
        logical, intent(inout) :: visited(:)
        integer, intent(inout) :: finish_order(:), finish_time
        integer :: v

        visited(u) = .true.

        ! Visit all neighbors
        do v = 1, n
            if (graph(u, v) /= 0 .and. .not. visited(v)) then
                call kosaraju_dfs1(graph, n, v, visited, finish_order, finish_time)
            end if
        end do

        ! Record finish time
        finish_time = finish_time + 1
        finish_order(finish_time) = u
    end subroutine kosaraju_dfs1

    recursive subroutine kosaraju_dfs2(graph, n, u, visited, scc_ids, scc_id)
        ! Second DFS for Kosaraju's algorithm - assign SCC IDs
        implicit none
        integer, intent(in) :: graph(:,:), n, u, scc_id
        logical, intent(inout) :: visited(:)
        integer, intent(inout) :: scc_ids(:)
        integer :: v

        visited(u) = .true.
        scc_ids(u) = scc_id

        ! Visit all neighbors
        do v = 1, n
            if (graph(u, v) /= 0 .and. .not. visited(v)) then
                call kosaraju_dfs2(graph, n, v, visited, scc_ids, scc_id)
            end if
        end do
    end subroutine kosaraju_dfs2

    ! ========================================================================
    ! UTILITY FUNCTIONS
    ! ========================================================================

    subroutine transpose_graph(graph, transposed, n)
        ! Transpose a directed graph (reverse all edges)
        implicit none
        integer, intent(in) :: graph(:,:), n
        integer, intent(out) :: transposed(:,:)
        integer :: i, j

        do i = 1, n
            do j = 1, n
                transposed(j, i) = graph(i, j)
            end do
        end do
    end subroutine transpose_graph

    subroutine print_sccs(scc_ids, n, num_sccs, algorithm_name)
        ! Print strongly connected components
        implicit none
        integer, intent(in) :: scc_ids(:), n, num_sccs
        character(len=*), intent(in) :: algorithm_name
        integer :: i, j
        logical :: printed

        print *, ''
        print '(A)', trim(algorithm_name)
        print '(A)', repeat('-', 60)
        print '(A, I0)', 'Number of SCCs: ', num_sccs
        print '(A)', repeat('-', 60)

        do i = 1, num_sccs
            write(*, '(A, I0, A)', advance='no') 'SCC #', i, ': {'
            printed = .false.

            do j = 1, n
                if (scc_ids(j) == i) then
                    if (printed) write(*, '(A)', advance='no') ', '
                    write(*, '(I0)', advance='no') j - 1
                    printed = .true.
                end if
            end do

            print '(A)', '}'
        end do

        print '(A)', repeat('-', 60)
    end subroutine print_sccs

end module scc_module

! ============================================================================
! Main Program - Examples and Tests
! ============================================================================

program scc_demo
    use scc_module
    implicit none

    integer, parameter :: max_vertices = 20
    integer :: graph1(8, 8), graph2(5, 5)
    integer :: scc_ids(max_vertices), num_sccs

    print '(A)', repeat('=', 70)
    print '(A)', '        STRONGLY CONNECTED COMPONENTS IN FORTRAN'
    print '(A)', repeat('=', 70)
    print *

    ! ========================================================================
    ! Example 1: Graph from CLRS textbook
    ! ========================================================================
    print '(A)', 'Example 1: Standard SCC Example'
    print '(A)', repeat('=', 70)
    print *
    print '(A)', 'Directed graph with multiple SCCs:'
    print *

    ! Initialize graph
    graph1 = 0

    ! SCC 1: {0, 1, 2}
    graph1(1, 2) = 1  ! 0 → 1
    graph1(2, 3) = 1  ! 1 → 2
    graph1(3, 1) = 1  ! 2 → 0

    ! SCC 2: {3, 4}
    graph1(4, 5) = 1  ! 3 → 4
    graph1(5, 4) = 1  ! 4 → 3

    ! SCC 3: {5}
    ! (singleton)

    ! SCC 4: {6, 7}
    graph1(7, 8) = 1  ! 6 → 7
    graph1(8, 7) = 1  ! 7 → 6

    ! Cross-component edges
    graph1(3, 4) = 1  ! 2 → 3
    graph1(2, 6) = 1  ! 1 → 5
    graph1(6, 7) = 1  ! 5 → 6
    graph1(5, 7) = 1  ! 4 → 6

    call print_graph(graph1, 8, 'Graph Adjacency Matrix')

    ! Test Tarjan's algorithm
    print *
    print '(A)', 'Test 1: Tarjans Algorithm'
    call tarjans_scc(graph1, 8, scc_ids, num_sccs)
    call print_sccs(scc_ids, 8, num_sccs, "Tarjan's Algorithm Result")

    ! Test Kosaraju's algorithm
    print *
    print '(A)', 'Test 2: Kosarajus Algorithm'
    call kosarajus_scc(graph1, 8, scc_ids, num_sccs)
    call print_sccs(scc_ids, 8, num_sccs, "Kosaraju's Algorithm Result")

    ! ========================================================================
    ! Example 2: Simple cycle graph
    ! ========================================================================
    print *
    print *
    print '(A)', 'Example 2: Simple Cycle Graph'
    print '(A)', repeat('=', 70)
    print *
    print '(A)', 'All vertices form one SCC: 0 → 1 → 2 → 3 → 4 → 0'

    graph2 = 0
    graph2(1, 2) = 1  ! 0 → 1
    graph2(2, 3) = 1  ! 1 → 2
    graph2(3, 4) = 1  ! 2 → 3
    graph2(4, 5) = 1  ! 3 → 4
    graph2(5, 1) = 1  ! 4 → 0

    call print_graph(graph2, 5, 'Cycle Graph Adjacency Matrix')

    print *
    print '(A)', 'Test 3: Tarjans Algorithm on Cycle Graph'
    call tarjans_scc(graph2, 5, scc_ids, num_sccs)
    call print_sccs(scc_ids, 5, num_sccs, "Tarjan's Algorithm Result")

    print *
    print '(A)', 'Test 4: Kosarajus Algorithm on Cycle Graph'
    call kosarajus_scc(graph2, 5, scc_ids, num_sccs)
    call print_sccs(scc_ids, 5, num_sccs, "Kosaraju's Algorithm Result")

    ! Summary
    print *
    print '(A)', repeat('=', 70)
    print '(A)', 'Key Points:'
    print '(A)', '- Time Complexity: O(V + E) for both algorithms'
    print '(A)', '- Tarjans: Single DFS pass, uses low-link values'
    print '(A)', '- Kosarajus: Two DFS passes, simpler but needs graph transpose'
    print '(A)', '- SCC is maximal subgraph where all vertices are mutually reachable'
    print '(A)', '- Applications: Social networks, web crawling, dependency analysis'
    print '(A)', '- Every vertex belongs to exactly one SCC'
    print '(A)', repeat('=', 70)

contains

    subroutine print_graph(graph, n, title)
        ! Print directed graph adjacency matrix
        implicit none
        integer, intent(in) :: graph(:,:), n
        character(len=*), intent(in) :: title
        integer :: i, j

        print *, ''
        print '(A)', trim(title)
        print *

        ! Print header
        write(*, '(A)', advance='no') '   '
        do j = 1, n
            write(*, '(I4)', advance='no') j-1
        end do
        print *

        ! Print matrix
        do i = 1, n
            write(*, '(I2, A)', advance='no') i-1, ': '
            do j = 1, n
                write(*, '(I4)', advance='no') graph(i, j)
            end do
            print *
        end do
    end subroutine print_graph

end program scc_demo
