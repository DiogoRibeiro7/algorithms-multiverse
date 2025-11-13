! ============================================================================
! Cycle Detection Algorithms in Modern Fortran
!
! Implementations:
! - DFS-based cycle detection for directed graphs
! - DFS-based cycle detection for undirected graphs
! - Floyd's Cycle Detection (for linked lists/functional graphs)
!
! Cycle: A path that starts and ends at the same vertex.
!
! Compile: gfortran -O3 -o cycle_detection cycle_detection.f90
! Run: ./cycle_detection
!
! @author Algorithms Multiverse
! @version 1.0
! ============================================================================

module cycle_detection_module
    implicit none
    private
    public :: has_cycle_directed, has_cycle_undirected
    public :: floyds_cycle_detection, find_cycle_directed

contains

    ! ========================================================================
    ! DIRECTED GRAPH CYCLE DETECTION
    ! ========================================================================

    function has_cycle_directed(graph, n) result(has_cycle)
        ! Detect cycle in directed graph using DFS with recursion stack
        !
        ! Time Complexity: O(V + E)
        ! Space Complexity: O(V)
        !
        ! Algorithm:
        ! - Use DFS with a recursion stack
        ! - If we encounter a vertex in the recursion stack, cycle exists
        ! - Recursion stack tracks vertices in current DFS path
        !
        ! Applications:
        ! - Deadlock detection
        ! - Dependency cycle detection
        ! - Topological sort validation
        implicit none
        integer, intent(in) :: graph(:,:), n
        logical :: has_cycle
        logical :: visited(n), rec_stack(n)
        integer :: i

        visited = .false.
        rec_stack = .false.
        has_cycle = .false.

        do i = 1, n
            if (.not. visited(i)) then
                call dfs_directed(graph, n, i, visited, rec_stack, has_cycle)
                if (has_cycle) return
            end if
        end do
    end function has_cycle_directed

    recursive subroutine dfs_directed(graph, n, u, visited, rec_stack, has_cycle)
        ! DFS for directed graph cycle detection
        implicit none
        integer, intent(in) :: graph(:,:), n, u
        logical, intent(inout) :: visited(:), rec_stack(:), has_cycle
        integer :: v

        if (has_cycle) return

        visited(u) = .true.
        rec_stack(u) = .true.

        do v = 1, n
            if (graph(u, v) /= 0) then
                if (.not. visited(v)) then
                    call dfs_directed(graph, n, v, visited, rec_stack, has_cycle)
                else if (rec_stack(v)) then
                    ! Back edge to vertex in current path - cycle found
                    has_cycle = .true.
                    return
                end if
            end if
        end do

        rec_stack(u) = .false.
    end subroutine dfs_directed

    ! ========================================================================
    ! DIRECTED GRAPH - FIND ACTUAL CYCLE
    ! ========================================================================

    subroutine find_cycle_directed(graph, n, cycle, cycle_size, has_cycle)
        ! Find an actual cycle in directed graph and return the vertices
        !
        ! Time Complexity: O(V + E)
        ! Space Complexity: O(V)
        implicit none
        integer, intent(in) :: graph(:,:), n
        integer, intent(out) :: cycle(:), cycle_size
        logical, intent(out) :: has_cycle
        logical :: visited(n), rec_stack(n)
        integer :: parent(n), cycle_start, cycle_end
        integer :: i

        visited = .false.
        rec_stack = .false.
        parent = -1
        has_cycle = .false.
        cycle_start = -1
        cycle_end = -1

        do i = 1, n
            if (.not. visited(i)) then
                call dfs_find_cycle(graph, n, i, visited, rec_stack, parent, &
                                   has_cycle, cycle_start, cycle_end)
                if (has_cycle) exit
            end if
        end do

        if (has_cycle) then
            ! Reconstruct cycle
            cycle_size = 0
            i = cycle_end
            do
                cycle_size = cycle_size + 1
                cycle(cycle_size) = i
                if (i == cycle_start) exit
                i = parent(i)
            end do

            ! Reverse cycle to get correct order
            call reverse_array(cycle, cycle_size)
        else
            cycle_size = 0
        end if
    end subroutine find_cycle_directed

    recursive subroutine dfs_find_cycle(graph, n, u, visited, rec_stack, parent, &
                                       has_cycle, cycle_start, cycle_end)
        ! DFS to find actual cycle in directed graph
        implicit none
        integer, intent(in) :: graph(:,:), n, u
        logical, intent(inout) :: visited(:), rec_stack(:), has_cycle
        integer, intent(inout) :: parent(:), cycle_start, cycle_end
        integer :: v

        if (has_cycle) return

        visited(u) = .true.
        rec_stack(u) = .true.

        do v = 1, n
            if (graph(u, v) /= 0) then
                if (.not. visited(v)) then
                    parent(v) = u
                    call dfs_find_cycle(graph, n, v, visited, rec_stack, parent, &
                                       has_cycle, cycle_start, cycle_end)
                else if (rec_stack(v)) then
                    ! Found cycle
                    has_cycle = .true.
                    cycle_start = v
                    cycle_end = u
                    return
                end if
            end if
        end do

        rec_stack(u) = .false.
    end subroutine dfs_find_cycle

    ! ========================================================================
    ! UNDIRECTED GRAPH CYCLE DETECTION
    ! ========================================================================

    function has_cycle_undirected(graph, n) result(has_cycle)
        ! Detect cycle in undirected graph using DFS
        !
        ! Time Complexity: O(V + E)
        ! Space Complexity: O(V)
        !
        ! Algorithm:
        ! - Use DFS with parent tracking
        ! - If we encounter a visited vertex that's not the parent, cycle exists
        !
        ! Applications:
        ! - Checking if graph is a tree
        ! - Network loop detection
        ! - Forest validation
        implicit none
        integer, intent(in) :: graph(:,:), n
        logical :: has_cycle
        logical :: visited(n)
        integer :: i

        visited = .false.
        has_cycle = .false.

        do i = 1, n
            if (.not. visited(i)) then
                call dfs_undirected(graph, n, i, -1, visited, has_cycle)
                if (has_cycle) return
            end if
        end do
    end function has_cycle_undirected

    recursive subroutine dfs_undirected(graph, n, u, parent, visited, has_cycle)
        ! DFS for undirected graph cycle detection
        implicit none
        integer, intent(in) :: graph(:,:), n, u, parent
        logical, intent(inout) :: visited(:), has_cycle
        integer :: v

        if (has_cycle) return

        visited(u) = .true.

        do v = 1, n
            if (graph(u, v) /= 0) then
                if (.not. visited(v)) then
                    call dfs_undirected(graph, n, v, u, visited, has_cycle)
                else if (v /= parent) then
                    ! Found edge to visited vertex that's not parent - cycle found
                    has_cycle = .true.
                    return
                end if
            end if
        end do
    end subroutine dfs_undirected

    ! ========================================================================
    ! FLOYD'S CYCLE DETECTION (Tortoise and Hare)
    ! ========================================================================

    function floyds_cycle_detection(next, start, n) result(has_cycle)
        ! Floyd's cycle detection algorithm (for functional graphs)
        !
        ! Time Complexity: O(n) where n is cycle length + distance to cycle
        ! Space Complexity: O(1)
        !
        ! Algorithm:
        ! - Use two pointers: slow (moves 1 step) and fast (moves 2 steps)
        ! - If they meet, cycle exists
        ! - This is the "tortoise and hare" algorithm
        !
        ! Applications:
        ! - Linked list cycle detection
        ! - Functional graph cycle detection
        ! - Sequence period finding
        implicit none
        integer, intent(in) :: next(:)  ! next(i) = next vertex from i
        integer, intent(in) :: start, n
        logical :: has_cycle
        integer :: slow, fast, steps

        slow = start
        fast = start
        has_cycle = .false.
        steps = 0

        ! Move pointers until they meet or reach end
        do while (steps < n * 2)  ! Safety limit
            ! Slow moves 1 step
            if (next(slow) == -1) return  ! Reached end, no cycle
            slow = next(slow)

            ! Fast moves 2 steps
            if (next(fast) == -1) return
            fast = next(fast)
            if (next(fast) == -1) return
            fast = next(fast)

            steps = steps + 1

            ! If they meet, cycle exists
            if (slow == fast) then
                has_cycle = .true.
                return
            end if
        end do
    end function floyds_cycle_detection

    ! ========================================================================
    ! UTILITY FUNCTIONS
    ! ========================================================================

    subroutine reverse_array(arr, n)
        ! Reverse an array
        implicit none
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: n
        integer :: i, temp

        do i = 1, n / 2
            temp = arr(i)
            arr(i) = arr(n - i + 1)
            arr(n - i + 1) = temp
        end do
    end subroutine reverse_array

end module cycle_detection_module

! ============================================================================
! Main Program - Examples and Tests
! ============================================================================

program cycle_detection_demo
    use cycle_detection_module
    implicit none

    integer, parameter :: max_vertices = 20
    integer :: graph_dir1(4, 4), graph_dir2(4, 4)
    integer :: graph_undir1(5, 5), graph_undir2(5, 5)
    integer :: next(10), cycle(max_vertices), cycle_size
    logical :: has_cycle

    print '(A)', repeat('=', 70)
    print '(A)', '            CYCLE DETECTION ALGORITHMS IN FORTRAN'
    print '(A)', repeat('=', 70)
    print *

    ! ========================================================================
    ! Example 1: Directed Graph with Cycle
    ! ========================================================================
    print '(A)', 'Example 1: Directed Graph WITH Cycle'
    print '(A)', repeat('=', 70)
    print *
    print '(A)', 'Graph has cycle: 0 → 1 → 2 → 0'

    graph_dir1 = 0
    graph_dir1(1, 2) = 1  ! 0 → 1
    graph_dir1(2, 3) = 1  ! 1 → 2
    graph_dir1(3, 1) = 1  ! 2 → 0 (creates cycle)
    graph_dir1(2, 4) = 1  ! 1 → 3

    call print_graph(graph_dir1, 4, 'Directed Graph (Adjacency Matrix)')

    has_cycle = has_cycle_directed(graph_dir1, 4)
    print *
    print '(A, L1)', 'Has cycle: ', has_cycle

    call find_cycle_directed(graph_dir1, 4, cycle, cycle_size, has_cycle)
    if (has_cycle) then
        call print_cycle(cycle, cycle_size)
    end if

    ! ========================================================================
    ! Example 2: Directed Graph without Cycle (DAG)
    ! ========================================================================
    print *
    print *
    print '(A)', 'Example 2: Directed Graph WITHOUT Cycle (DAG)'
    print '(A)', repeat('=', 70)
    print *
    print '(A)', 'This is a DAG (Directed Acyclic Graph)'

    graph_dir2 = 0
    graph_dir2(1, 2) = 1  ! 0 → 1
    graph_dir2(1, 3) = 1  ! 0 → 2
    graph_dir2(2, 4) = 1  ! 1 → 3
    graph_dir2(3, 4) = 1  ! 2 → 3

    call print_graph(graph_dir2, 4, 'Directed Graph (Adjacency Matrix)')

    has_cycle = has_cycle_directed(graph_dir2, 4)
    print *
    print '(A, L1)', 'Has cycle: ', has_cycle

    ! ========================================================================
    ! Example 3: Undirected Graph with Cycle
    ! ========================================================================
    print *
    print *
    print '(A)', 'Example 3: Undirected Graph WITH Cycle'
    print '(A)', repeat('=', 70)
    print *
    print '(A)', 'Graph has cycle: 0 - 1 - 2 - 0'

    graph_undir1 = 0
    ! Add undirected edges
    graph_undir1(1, 2) = 1
    graph_undir1(2, 1) = 1  ! 0 - 1

    graph_undir1(2, 3) = 1
    graph_undir1(3, 2) = 1  ! 1 - 2

    graph_undir1(3, 1) = 1
    graph_undir1(1, 3) = 1  ! 2 - 0 (creates cycle)

    graph_undir1(2, 4) = 1
    graph_undir1(4, 2) = 1  ! 1 - 3

    call print_graph(graph_undir1, 4, 'Undirected Graph (Adjacency Matrix)')

    has_cycle = has_cycle_undirected(graph_undir1, 4)
    print *
    print '(A, L1)', 'Has cycle: ', has_cycle

    ! ========================================================================
    ! Example 4: Undirected Graph without Cycle (Tree)
    ! ========================================================================
    print *
    print *
    print '(A)', 'Example 4: Undirected Graph WITHOUT Cycle (Tree)'
    print '(A)', repeat('=', 70)
    print *
    print '(A)', 'This is a tree (connected acyclic graph)'

    graph_undir2 = 0
    ! Tree structure
    graph_undir2(1, 2) = 1
    graph_undir2(2, 1) = 1  ! 0 - 1

    graph_undir2(1, 3) = 1
    graph_undir2(3, 1) = 1  ! 0 - 2

    graph_undir2(2, 4) = 1
    graph_undir2(4, 2) = 1  ! 1 - 3

    graph_undir2(2, 5) = 1
    graph_undir2(5, 2) = 1  ! 1 - 4

    call print_graph(graph_undir2, 5, 'Undirected Graph (Adjacency Matrix)')

    has_cycle = has_cycle_undirected(graph_undir2, 5)
    print *
    print '(A, L1)', 'Has cycle: ', has_cycle

    ! ========================================================================
    ! Example 5: Floyd's Cycle Detection
    ! ========================================================================
    print *
    print *
    print '(A)', 'Example 5: Floyds Cycle Detection (Tortoise and Hare)'
    print '(A)', repeat('=', 70)
    print *
    print '(A)', 'Functional graph: 0→1→2→3→4→2 (cycle: 2→3→4→2)'

    ! -1 means no next vertex
    next = -1
    next(1) = 2  ! 0 → 1
    next(2) = 3  ! 1 → 2
    next(3) = 4  ! 2 → 3
    next(4) = 5  ! 3 → 4
    next(5) = 3  ! 4 → 2 (creates cycle)

    has_cycle = floyds_cycle_detection(next, 1, 10)
    print *
    print '(A, L1)', 'Has cycle: ', has_cycle

    ! Summary
    print *
    print '(A)', repeat('=', 70)
    print '(A)', 'Key Points:'
    print '(A)', '- Directed graphs: Use recursion stack for cycle detection'
    print '(A)', '- Undirected graphs: Use parent tracking for cycle detection'
    print '(A)', '- Floyds algorithm: O(1) space, O(n) time for functional graphs'
    print '(A)', '- Time complexity: O(V + E) for graph-based methods'
    print '(A)', '- Applications: Deadlock detection, dependency validation, tree check'
    print '(A)', repeat('=', 70)

contains

    subroutine print_graph(graph, n, title)
        ! Print graph adjacency matrix
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

    subroutine print_cycle(cycle, cycle_size)
        ! Print cycle vertices
        implicit none
        integer, intent(in) :: cycle(:), cycle_size
        integer :: i

        print *
        write(*, '(A)', advance='no') 'Cycle found: '
        do i = 1, cycle_size
            write(*, '(I0)', advance='no') cycle(i) - 1
            if (i < cycle_size) write(*, '(A)', advance='no') ' → '
        end do
        print *
    end subroutine print_cycle

end program cycle_detection_demo
