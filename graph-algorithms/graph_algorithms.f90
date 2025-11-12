! Graph Algorithms in Modern Fortran
!
! Implementations of fundamental graph algorithms:
! - Breadth-First Search (BFS)
! - Depth-First Search (DFS)
! - Dijkstra's Shortest Path
!
! Graph representation: Adjacency Matrix (simpler for Fortran)

program graph_algorithms
    implicit none

    integer, parameter :: MAX_V = 100
    integer, parameter :: INF = 999999

    ! Test graph
    integer, parameter :: n_vertices = 6
    integer :: graph(n_vertices, n_vertices)
    integer :: i, j

    print '(A)', repeat('=', 70)
    print '(A)', '                GRAPH ALGORITHMS IN FORTRAN'
    print '(A)', repeat('=', 70)
    print *

    ! Initialize graph with INF (no edges)
    graph = INF
    do i = 1, n_vertices
        graph(i, i) = 0  ! Distance to self is 0
    end do

    ! Add edges (undirected graph with weights)
    ! Edge (0,1) weight 4
    graph(1, 2) = 4
    graph(2, 1) = 4

    ! Edge (0,2) weight 3
    graph(1, 3) = 3
    graph(3, 1) = 3

    ! Edge (1,2) weight 1
    graph(2, 3) = 1
    graph(3, 2) = 1

    ! Edge (1,3) weight 2
    graph(2, 4) = 2
    graph(4, 2) = 2

    ! Edge (2,3) weight 4
    graph(3, 4) = 4
    graph(4, 3) = 4

    ! Edge (3,4) weight 2
    graph(4, 5) = 2
    graph(5, 4) = 2

    ! Edge (4,5) weight 6
    graph(5, 6) = 6
    graph(6, 5) = 6

    ! Print graph
    call print_graph(graph, n_vertices)
    print *

    ! Test BFS
    print '(A)', 'Test 1: Breadth-First Search (BFS)'
    print '(A)', repeat('-', 70)
    call bfs(graph, n_vertices, 1)  ! Start from vertex 1 (0-indexed as 1 in Fortran)
    print *

    ! Test DFS
    print '(A)', 'Test 2: Depth-First Search (DFS)'
    print '(A)', repeat('-', 70)
    call dfs(graph, n_vertices, 1)
    print *

    ! Test Dijkstra
    print '(A)', 'Test 3: Dijkstras Shortest Path Algorithm'
    print '(A)', repeat('-', 70)
    call dijkstra(graph, n_vertices, 1)

    print *
    print '(A)', repeat('=', 70)
    print '(A)', 'Key Points:'
    print '(A)', '- BFS: O(V + E) time, explores level by level'
    print '(A)', '- DFS: O(V + E) time, explores depth-first'
    print '(A)', '- Dijkstra: O(V²) time with array, O((V+E)logV) with heap'
    print '(A)', '- Adjacency matrix: O(V²) space, O(1) edge lookup'
    print '(A)', repeat('=', 70)

contains

    ! ===================================================================
    ! GRAPH UTILITIES
    ! ===================================================================

    subroutine print_graph(graph, n)
        integer, intent(in) :: graph(:,:), n
        integer :: i, j

        print '(A)', 'Graph adjacency matrix:'
        print '(A)', '(INF = no edge)'
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
                if (graph(i, j) == INF) then
                    write(*, '(A6)', advance='no') 'INF'
                else
                    write(*, '(I6)', advance='no') graph(i, j)
                end if
            end do
            print *
        end do
    end subroutine print_graph

    ! ===================================================================
    ! BREADTH-FIRST SEARCH (BFS)
    ! ===================================================================

    subroutine bfs(graph, n, start)
        integer, intent(in) :: graph(:,:), n, start
        logical :: visited(n)
        integer :: queue(n), front, rear
        integer :: current, i

        visited = .false.
        front = 1
        rear = 1
        queue(rear) = start

        visited(start) = .true.

        write(*, '(A, I0, A)', advance='no') 'BFS traversal from vertex ', start-1, ': '

        do while (front <= rear)
            current = queue(front)
            front = front + 1

            write(*, '(I0, A)', advance='no') current-1, ' '

            ! Visit all adjacent vertices
            do i = 1, n
                if (graph(current, i) /= INF .and. graph(current, i) /= 0 &
                    .and. .not. visited(i)) then
                    visited(i) = .true.
                    rear = rear + 1
                    queue(rear) = i
                end if
            end do
        end do

        print *
    end subroutine bfs

    ! ===================================================================
    ! DEPTH-FIRST SEARCH (DFS)
    ! ===================================================================

    subroutine dfs(graph, n, start)
        integer, intent(in) :: graph(:,:), n, start
        logical :: visited(n)

        visited = .false.

        write(*, '(A, I0, A)', advance='no') 'DFS traversal from vertex ', start-1, ': '
        call dfs_util(graph, n, start, visited)
        print *
    end subroutine dfs

    recursive subroutine dfs_util(graph, n, vertex, visited)
        integer, intent(in) :: graph(:,:), n, vertex
        logical, intent(inout) :: visited(:)
        integer :: i

        visited(vertex) = .true.
        write(*, '(I0, A)', advance='no') vertex-1, ' '

        ! Visit all adjacent vertices
        do i = 1, n
            if (graph(vertex, i) /= INF .and. graph(vertex, i) /= 0 &
                .and. .not. visited(i)) then
                call dfs_util(graph, n, i, visited)
            end if
        end do
    end subroutine dfs_util

    ! ===================================================================
    ! DIJKSTRA'S SHORTEST PATH
    ! ===================================================================

    subroutine dijkstra(graph, n, src)
        integer, intent(in) :: graph(:,:), n, src
        integer :: dist(n)
        logical :: visited(n)
        integer :: i, count, min_dist, u, v

        ! Initialize
        dist = INF
        dist(src) = 0
        visited = .false.

        do count = 1, n
            ! Find minimum distance vertex not yet visited
            min_dist = INF
            u = -1

            do i = 1, n
                if (.not. visited(i) .and. dist(i) < min_dist) then
                    min_dist = dist(i)
                    u = i
                end if
            end do

            if (u == -1) exit  ! All remaining vertices are unreachable

            visited(u) = .true.

            ! Update distances of adjacent vertices
            do v = 1, n
                if (.not. visited(v) .and. graph(u, v) /= INF &
                    .and. dist(u) /= INF &
                    .and. dist(u) + graph(u, v) < dist(v)) then
                    dist(v) = dist(u) + graph(u, v)
                end if
            end do
        end do

        ! Print results
        print *
        print '(A, I0)', 'Dijkstras shortest paths from vertex ', src-1
        print '(A)', 'Vertex    Distance from Source'
        print '(A)', repeat('-', 40)

        do i = 1, n
            write(*, '(I4, A)', advance='no') i-1, '         '
            if (dist(i) == INF) then
                print '(A)', 'INF'
            else
                print '(I0)', dist(i)
            end if
        end do
    end subroutine dijkstra

end program graph_algorithms
