! ============================================================================
! Topological Sort Algorithms in Modern Fortran
!
! Implementations:
! - Kahn's Algorithm (BFS-based, using in-degree)
! - DFS-based Topological Sort
!
! Topological sorting orders vertices in a Directed Acyclic Graph (DAG)
! such that for every directed edge u→v, u comes before v in the ordering.
!
! Only possible for DAGs (Directed Acyclic Graphs).
! If graph has cycle, topological sort is not possible.
!
! Compile: gfortran -O3 -o topological_sort topological_sort.f90
! Run: ./topological_sort
!
! @author Algorithms Multiverse
! @version 1.0
! ============================================================================

module topological_sort_module
    implicit none
    private
    public :: kahns_algorithm, dfs_topological_sort
    public :: has_cycle_directed, print_order

contains

    ! ========================================================================
    ! KAHN'S ALGORITHM (BFS-based)
    ! ========================================================================

    subroutine kahns_algorithm(graph, n, order, order_size, has_cycle)
        ! Topological sort using Kahn's algorithm (BFS-based)
        !
        ! Time Complexity: O(V + E)
        ! Space Complexity: O(V)
        !
        ! Algorithm:
        ! 1. Compute in-degree for all vertices
        ! 2. Add all vertices with in-degree 0 to queue
        ! 3. While queue not empty:
        !    - Remove vertex, add to result
        !    - Decrease in-degree of neighbors
        !    - Add neighbors with in-degree 0 to queue
        ! 4. If all vertices processed, return order; else cycle exists
        !
        ! Applications:
        ! - Task scheduling with dependencies
        ! - Build systems (Makefile dependencies)
        ! - Course prerequisites
        ! - Spreadsheet formula evaluation
        implicit none
        integer, intent(in) :: graph(:,:), n
        integer, intent(out) :: order(:)
        integer, intent(out) :: order_size
        logical, intent(out) :: has_cycle
        integer :: in_degree(n), queue(n)
        integer :: front, rear, u, v, i

        ! Compute in-degree for each vertex
        in_degree = 0
        do u = 1, n
            do v = 1, n
                if (graph(u, v) /= 0) then
                    in_degree(v) = in_degree(v) + 1
                end if
            end do
        end do

        ! Initialize queue with vertices having in-degree 0
        front = 1
        rear = 0
        do i = 1, n
            if (in_degree(i) == 0) then
                rear = rear + 1
                queue(rear) = i
            end if
        end do

        order_size = 0

        ! Process vertices
        do while (front <= rear)
            u = queue(front)
            front = front + 1

            order_size = order_size + 1
            order(order_size) = u

            ! Reduce in-degree of neighbors
            do v = 1, n
                if (graph(u, v) /= 0) then
                    in_degree(v) = in_degree(v) - 1
                    if (in_degree(v) == 0) then
                        rear = rear + 1
                        queue(rear) = v
                    end if
                end if
            end do
        end do

        ! Check if all vertices were processed
        has_cycle = (order_size /= n)
    end subroutine kahns_algorithm

    ! ========================================================================
    ! DFS-BASED TOPOLOGICAL SORT
    ! ========================================================================

    subroutine dfs_topological_sort(graph, n, order, order_size, has_cycle)
        ! Topological sort using DFS
        !
        ! Time Complexity: O(V + E)
        ! Space Complexity: O(V)
        !
        ! Algorithm:
        ! 1. Perform DFS from each unvisited vertex
        ! 2. After visiting all descendants of a vertex, add it to result
        ! 3. Reverse the result to get topological order
        ! 4. Detect cycles using recursion stack
        !
        ! Applications: Same as Kahn's algorithm
        implicit none
        integer, intent(in) :: graph(:,:), n
        integer, intent(out) :: order(:)
        integer, intent(out) :: order_size
        logical, intent(out) :: has_cycle
        logical :: visited(n), rec_stack(n)
        integer :: stack(n), top
        integer :: i

        visited = .false.
        rec_stack = .false.
        top = 0
        has_cycle = .false.

        ! DFS from each unvisited vertex
        do i = 1, n
            if (.not. visited(i)) then
                call dfs_visit(graph, n, i, visited, rec_stack, stack, top, has_cycle)
                if (has_cycle) return
            end if
        end do

        ! Copy stack to order (already in reverse DFS finish order)
        order_size = top
        order(1:order_size) = stack(1:top)
    end subroutine dfs_topological_sort

    recursive subroutine dfs_visit(graph, n, u, visited, rec_stack, stack, top, has_cycle)
        ! DFS visit with cycle detection
        implicit none
        integer, intent(in) :: graph(:,:), n, u
        logical, intent(inout) :: visited(:), rec_stack(:)
        integer, intent(inout) :: stack(:), top
        logical, intent(inout) :: has_cycle
        integer :: v

        if (has_cycle) return

        visited(u) = .true.
        rec_stack(u) = .true.

        ! Visit all neighbors
        do v = 1, n
            if (graph(u, v) /= 0) then
                if (.not. visited(v)) then
                    call dfs_visit(graph, n, v, visited, rec_stack, stack, top, has_cycle)
                    if (has_cycle) return
                else if (rec_stack(v)) then
                    ! Back edge found - cycle detected
                    has_cycle = .true.
                    return
                end if
            end if
        end do

        rec_stack(u) = .false.

        ! Add to stack after visiting all descendants
        top = top + 1
        stack(top) = u
    end subroutine dfs_visit

    ! ========================================================================
    ! CYCLE DETECTION
    ! ========================================================================

    function has_cycle_directed(graph, n) result(has_cycle)
        ! Detect if directed graph has a cycle
        !
        ! Time Complexity: O(V + E)
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
                call detect_cycle_dfs(graph, n, i, visited, rec_stack, has_cycle)
                if (has_cycle) return
            end if
        end do
    end function has_cycle_directed

    recursive subroutine detect_cycle_dfs(graph, n, u, visited, rec_stack, has_cycle)
        ! DFS for cycle detection
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
                    call detect_cycle_dfs(graph, n, v, visited, rec_stack, has_cycle)
                else if (rec_stack(v)) then
                    has_cycle = .true.
                    return
                end if
            end if
        end do

        rec_stack(u) = .false.
    end subroutine detect_cycle_dfs

    ! ========================================================================
    ! UTILITY FUNCTIONS
    ! ========================================================================

    subroutine print_order(order, order_size, algorithm_name, has_cycle)
        ! Print topological order
        implicit none
        integer, intent(in) :: order(:), order_size
        character(len=*), intent(in) :: algorithm_name
        logical, intent(in) :: has_cycle
        integer :: i

        print *, ''
        print '(A)', trim(algorithm_name)
        print '(A)', repeat('-', 60)

        if (has_cycle) then
            print '(A)', 'ERROR: Graph contains a cycle!'
            print '(A)', 'Topological sort is only possible for DAGs (Directed Acyclic Graphs)'
        else
            write(*, '(A)', advance='no') 'Topological order: '
            do i = 1, order_size
                write(*, '(I0)', advance='no') order(i) - 1
                if (i < order_size) write(*, '(A)', advance='no') ' → '
            end do
            print *
            print '(A)', 'All dependencies are satisfied in this order.'
        end if
        print '(A)', repeat('-', 60)
    end subroutine print_order

end module topological_sort_module

! ============================================================================
! Main Program - Examples and Tests
! ============================================================================

program topological_sort_demo
    use topological_sort_module
    implicit none

    integer, parameter :: max_vertices = 10
    integer :: graph1(6, 6), graph2(6, 6)
    integer :: order(max_vertices), order_size
    logical :: has_cycle

    print '(A)', repeat('=', 70)
    print '(A)', '            TOPOLOGICAL SORT ALGORITHMS IN FORTRAN'
    print '(A)', repeat('=', 70)
    print *

    ! ========================================================================
    ! Example 1: DAG (course prerequisites)
    ! ========================================================================
    print '(A)', 'Example 1: Course Prerequisites (DAG)'
    print '(A)', repeat('=', 70)
    print *
    print '(A)', 'Courses (vertices):'
    print '(A)', '  0: Intro to Programming'
    print '(A)', '  1: Data Structures'
    print '(A)', '  2: Algorithms'
    print '(A)', '  3: Operating Systems'
    print '(A)', '  4: Database Systems'
    print '(A)', '  5: Compilers'
    print *
    print '(A)', 'Prerequisites (edges):'
    print '(A)', '  0 → 1: Need Intro before Data Structures'
    print '(A)', '  1 → 2: Need Data Structures before Algorithms'
    print '(A)', '  0 → 3: Need Intro before Operating Systems'
    print '(A)', '  1 → 4: Need Data Structures before Databases'
    print '(A)', '  2 → 5: Need Algorithms before Compilers'
    print '(A)', '  3 → 5: Need Operating Systems before Compilers'

    ! Build DAG
    graph1 = 0
    graph1(1, 2) = 1  ! 0 → 1
    graph1(2, 3) = 1  ! 1 → 2
    graph1(1, 4) = 1  ! 0 → 3
    graph1(2, 5) = 1  ! 1 → 4
    graph1(3, 6) = 1  ! 2 → 5
    graph1(4, 6) = 1  ! 3 → 5

    call print_graph(graph1, 6, 'Course Prerequisite Graph (Adjacency Matrix)')

    ! Test Kahn's algorithm
    print *
    print '(A)', 'Test 1: Kahns Algorithm (BFS-based)'
    call kahns_algorithm(graph1, 6, order, order_size, has_cycle)
    call print_order(order, order_size, "Kahn's Algorithm Result", has_cycle)

    ! Test DFS-based topological sort
    print *
    print '(A)', 'Test 2: DFS-based Topological Sort'
    call dfs_topological_sort(graph1, 6, order, order_size, has_cycle)
    call print_order(order, order_size, "DFS-based Topological Sort Result", has_cycle)

    ! ========================================================================
    ! Example 2: Graph with cycle
    ! ========================================================================
    print *
    print *
    print '(A)', 'Example 2: Graph with Cycle (Invalid for Topological Sort)'
    print '(A)', repeat('=', 70)
    print *
    print '(A)', 'This graph has a cycle: 0 → 1 → 2 → 0'

    graph2 = 0
    graph2(1, 2) = 1  ! 0 → 1
    graph2(2, 3) = 1  ! 1 → 2
    graph2(3, 1) = 1  ! 2 → 0 (creates cycle)
    graph2(2, 4) = 1  ! 1 → 3

    call print_graph(graph2, 4, 'Graph with Cycle (Adjacency Matrix)')

    print *
    print '(A)', 'Test 3: Kahns Algorithm on Cyclic Graph'
    call kahns_algorithm(graph2, 4, order, order_size, has_cycle)
    call print_order(order, order_size, "Kahn's Algorithm Result", has_cycle)

    print *
    print '(A)', 'Test 4: DFS-based Topological Sort on Cyclic Graph'
    call dfs_topological_sort(graph2, 4, order, order_size, has_cycle)
    call print_order(order, order_size, "DFS-based Topological Sort Result", has_cycle)

    ! Summary
    print *
    print '(A)', repeat('=', 70)
    print '(A)', 'Key Points:'
    print '(A)', '- Time Complexity: O(V + E) for both algorithms'
    print '(A)', '- Kahns: BFS-based, uses in-degree'
    print '(A)', '- DFS-based: Uses recursion and finish times'
    print '(A)', '- Both detect cycles in directed graphs'
    print '(A)', '- Topological sort only exists for DAGs'
    print '(A)', '- Applications: Task scheduling, build systems, course planning'
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

end program topological_sort_demo
