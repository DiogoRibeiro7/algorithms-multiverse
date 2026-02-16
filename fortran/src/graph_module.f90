! Graph Algorithms Module
! Comprehensive collection of graph algorithms and data structures

module graph_module
    use iso_fortran_env, only: int32, int64, real32, real64
    implicit none
    private

    ! Public interfaces
    public :: graph_type, weighted_graph_type
    public :: add_edge, add_vertex, remove_edge
    public :: bfs, dfs, dijkstra, bellman_ford
    public :: floyd_warshall, prim_mst, kruskal_mst
    public :: topological_sort, strongly_connected_components
    public :: is_cyclic, is_bipartite, graph_coloring
    public :: max_flow_ford_fulkerson, min_cut
    public :: traveling_salesman, hamiltonian_path
    public :: a_star_search, tarjan_bridges
    public :: articulation_points, kosaraju_scc

    ! Constants
    integer(int32), parameter :: INFINITY = huge(1_int32) / 2

    ! Edge type
    type :: edge_type
        integer(int32) :: src
        integer(int32) :: dest
        real(real64) :: weight
    end type edge_type

    ! Graph type (adjacency list representation)
    type :: graph_type
        integer(int32) :: num_vertices
        integer(int32) :: num_edges
        type(adjacency_list), dimension(:), allocatable :: adj_list
        logical :: is_directed
    contains
        procedure :: init => graph_init
        procedure :: add_edge => graph_add_edge
        procedure :: add_vertex => graph_add_vertex
        procedure :: remove_edge => graph_remove_edge
        procedure :: get_neighbors => graph_get_neighbors
        procedure :: has_edge => graph_has_edge
        procedure :: destroy => graph_destroy
    end type graph_type

    ! Weighted graph type
    type, extends(graph_type) :: weighted_graph_type
        real(real64), dimension(:,:), allocatable :: weight_matrix
    contains
        procedure :: init => weighted_graph_init
        procedure :: add_weighted_edge => weighted_graph_add_edge
        procedure :: get_edge_weight => weighted_graph_get_weight
    end type weighted_graph_type

    ! Adjacency list node
    type :: adj_node
        integer(int32) :: vertex
        real(real64) :: weight
        type(adj_node), pointer :: next => null()
    end type adj_node

    ! Adjacency list
    type :: adjacency_list
        type(adj_node), pointer :: head => null()
        integer(int32) :: size = 0
    end type adjacency_list

    ! Priority queue for Dijkstra
    type :: priority_queue
        type(pq_node), dimension(:), allocatable :: heap
        integer(int32) :: size = 0
        integer(int32) :: capacity
    contains
        procedure :: init => pq_init
        procedure :: push => pq_push
        procedure :: pop => pq_pop
        procedure :: is_empty => pq_is_empty
        procedure :: heapify_up => pq_heapify_up
        procedure :: heapify_down => pq_heapify_down
    end type priority_queue

    type :: pq_node
        integer(int32) :: vertex
        real(real64) :: distance
    end type pq_node

    ! Union-Find data structure for Kruskal's algorithm
    type :: union_find
        integer(int32), dimension(:), allocatable :: parent
        integer(int32), dimension(:), allocatable :: rank
    contains
        procedure :: init => uf_init
        procedure :: find => uf_find
        procedure :: union => uf_union
    end type union_find

contains

    !===============================================
    ! Graph Type Methods
    !===============================================

    subroutine graph_init(this, n, directed)
        implicit none
        class(graph_type), intent(inout) :: this
        integer(int32), intent(in) :: n
        logical, intent(in), optional :: directed
        integer(int32) :: i

        this%num_vertices = n
        this%num_edges = 0

        if (present(directed)) then
            this%is_directed = directed
        else
            this%is_directed = .false.
        end if

        allocate(this%adj_list(n))
        do i = 1, n
            this%adj_list(i)%head => null()
            this%adj_list(i)%size = 0
        end do

    end subroutine graph_init

    subroutine graph_add_edge(this, u, v, weight)
        implicit none
        class(graph_type), intent(inout) :: this
        integer(int32), intent(in) :: u, v
        real(real64), intent(in), optional :: weight
        type(adj_node), pointer :: new_node, current
        real(real64) :: w

        if (present(weight)) then
            w = weight
        else
            w = 1.0_real64
        end if

        ! Add v to u's adjacency list
        allocate(new_node)
        new_node%vertex = v
        new_node%weight = w
        new_node%next => this%adj_list(u)%head
        this%adj_list(u)%head => new_node
        this%adj_list(u)%size = this%adj_list(u)%size + 1

        ! If undirected, add u to v's adjacency list
        if (.not. this%is_directed) then
            allocate(new_node)
            new_node%vertex = u
            new_node%weight = w
            new_node%next => this%adj_list(v)%head
            this%adj_list(v)%head => new_node
            this%adj_list(v)%size = this%adj_list(v)%size + 1
        end if

        this%num_edges = this%num_edges + 1

    end subroutine graph_add_edge

    subroutine graph_add_vertex(this)
        implicit none
        class(graph_type), intent(inout) :: this
        type(adjacency_list), dimension(:), allocatable :: temp_list
        integer(int32) :: i, old_size

        old_size = this%num_vertices
        this%num_vertices = old_size + 1

        ! Reallocate adjacency list
        allocate(temp_list(this%num_vertices))

        do i = 1, old_size
            temp_list(i) = this%adj_list(i)
        end do

        temp_list(this%num_vertices)%head => null()
        temp_list(this%num_vertices)%size = 0

        call move_alloc(temp_list, this%adj_list)

    end subroutine graph_add_vertex

    subroutine graph_remove_edge(this, u, v)
        implicit none
        class(graph_type), intent(inout) :: this
        integer(int32), intent(in) :: u, v
        type(adj_node), pointer :: current, prev

        ! Remove v from u's adjacency list
        current => this%adj_list(u)%head
        prev => null()

        do while (associated(current))
            if (current%vertex == v) then
                if (associated(prev)) then
                    prev%next => current%next
                else
                    this%adj_list(u)%head => current%next
                end if
                deallocate(current)
                this%adj_list(u)%size = this%adj_list(u)%size - 1
                exit
            end if
            prev => current
            current => current%next
        end do

        ! If undirected, remove u from v's adjacency list
        if (.not. this%is_directed) then
            current => this%adj_list(v)%head
            prev => null()

            do while (associated(current))
                if (current%vertex == u) then
                    if (associated(prev)) then
                        prev%next => current%next
                    else
                        this%adj_list(v)%head => current%next
                    end if
                    deallocate(current)
                    this%adj_list(v)%size = this%adj_list(v)%size - 1
                    exit
                end if
                prev => current
                current => current%next
            end do
        end if

        this%num_edges = this%num_edges - 1

    end subroutine graph_remove_edge

    function graph_get_neighbors(this, v) result(neighbors)
        implicit none
        class(graph_type), intent(in) :: this
        integer(int32), intent(in) :: v
        integer(int32), dimension(:), allocatable :: neighbors
        type(adj_node), pointer :: current
        integer(int32) :: i

        allocate(neighbors(this%adj_list(v)%size))

        current => this%adj_list(v)%head
        i = 1
        do while (associated(current))
            neighbors(i) = current%vertex
            i = i + 1
            current => current%next
        end do

    end function graph_get_neighbors

    function graph_has_edge(this, u, v) result(has)
        implicit none
        class(graph_type), intent(in) :: this
        integer(int32), intent(in) :: u, v
        logical :: has
        type(adj_node), pointer :: current

        has = .false.
        current => this%adj_list(u)%head

        do while (associated(current))
            if (current%vertex == v) then
                has = .true.
                return
            end if
            current => current%next
        end do

    end function graph_has_edge

    subroutine graph_destroy(this)
        implicit none
        class(graph_type), intent(inout) :: this
        type(adj_node), pointer :: current, temp
        integer(int32) :: i

        do i = 1, this%num_vertices
            current => this%adj_list(i)%head
            do while (associated(current))
                temp => current
                current => current%next
                deallocate(temp)
            end do
        end do

        deallocate(this%adj_list)

    end subroutine graph_destroy

    !===============================================
    ! Weighted Graph Methods
    !===============================================

    subroutine weighted_graph_init(this, n, directed)
        implicit none
        class(weighted_graph_type), intent(inout) :: this
        integer(int32), intent(in) :: n
        logical, intent(in), optional :: directed

        call this%graph_type%init(n, directed)
        allocate(this%weight_matrix(n, n))
        this%weight_matrix = real(INFINITY, real64)

        ! Diagonal elements have zero weight
        do i = 1, n
            this%weight_matrix(i, i) = 0.0_real64
        end do

    end subroutine weighted_graph_init

    subroutine weighted_graph_add_edge(this, u, v, weight)
        implicit none
        class(weighted_graph_type), intent(inout) :: this
        integer(int32), intent(in) :: u, v
        real(real64), intent(in) :: weight

        call this%graph_type%add_edge(u, v, weight)
        this%weight_matrix(u, v) = weight

        if (.not. this%is_directed) then
            this%weight_matrix(v, u) = weight
        end if

    end subroutine weighted_graph_add_edge

    function weighted_graph_get_weight(this, u, v) result(weight)
        implicit none
        class(weighted_graph_type), intent(in) :: this
        integer(int32), intent(in) :: u, v
        real(real64) :: weight

        weight = this%weight_matrix(u, v)

    end function weighted_graph_get_weight

    !===============================================
    ! Breadth-First Search (BFS)
    !===============================================

    function bfs(graph, start) result(visited_order)
        implicit none
        type(graph_type), intent(in) :: graph
        integer(int32), intent(in) :: start
        integer(int32), dimension(:), allocatable :: visited_order
        logical, dimension(:), allocatable :: visited
        integer(int32), dimension(:), allocatable :: queue
        integer(int32) :: front, rear, current, i, neighbor_count
        integer(int32), dimension(:), allocatable :: neighbors
        type(adj_node), pointer :: adj

        allocate(visited(graph%num_vertices))
        allocate(queue(graph%num_vertices))
        allocate(visited_order(graph%num_vertices))

        visited = .false.
        front = 1
        rear = 1

        queue(rear) = start
        visited(start) = .true.

        i = 1
        visited_order = 0

        do while (front <= rear)
            current = queue(front)
            visited_order(i) = current
            i = i + 1
            front = front + 1

            neighbors = graph%get_neighbors(current)

            do j = 1, size(neighbors)
                if (.not. visited(neighbors(j))) then
                    visited(neighbors(j)) = .true.
                    rear = rear + 1
                    queue(rear) = neighbors(j)
                end if
            end do

            deallocate(neighbors)
        end do

        visited_order = visited_order(1:i-1)

    end function bfs

    !===============================================
    ! Depth-First Search (DFS)
    !===============================================

    function dfs(graph, start) result(visited_order)
        implicit none
        type(graph_type), intent(in) :: graph
        integer(int32), intent(in) :: start
        integer(int32), dimension(:), allocatable :: visited_order
        logical, dimension(:), allocatable :: visited
        integer(int32) :: order_count

        allocate(visited(graph%num_vertices))
        allocate(visited_order(graph%num_vertices))

        visited = .false.
        visited_order = 0
        order_count = 0

        call dfs_recursive(graph, start, visited, visited_order, order_count)

        visited_order = visited_order(1:order_count)

    contains

        recursive subroutine dfs_recursive(graph, v, visited, order, count)
            implicit none
            type(graph_type), intent(in) :: graph
            integer(int32), intent(in) :: v
            logical, dimension(:), intent(inout) :: visited
            integer(int32), dimension(:), intent(inout) :: order
            integer(int32), intent(inout) :: count
            integer(int32), dimension(:), allocatable :: neighbors
            integer(int32) :: i

            visited(v) = .true.
            count = count + 1
            order(count) = v

            neighbors = graph%get_neighbors(v)

            do i = 1, size(neighbors)
                if (.not. visited(neighbors(i))) then
                    call dfs_recursive(graph, neighbors(i), visited, order, count)
                end if
            end do

            deallocate(neighbors)

        end subroutine dfs_recursive

    end function dfs

    !===============================================
    ! Dijkstra's Algorithm
    !===============================================

    function dijkstra(graph, start) result(distances)
        implicit none
        type(weighted_graph_type), intent(in) :: graph
        integer(int32), intent(in) :: start
        real(real64), dimension(:), allocatable :: distances
        logical, dimension(:), allocatable :: visited
        type(priority_queue) :: pq
        type(pq_node) :: current_node
        type(adj_node), pointer :: neighbor
        real(real64) :: new_dist
        integer(int32) :: u, v

        allocate(distances(graph%num_vertices))
        allocate(visited(graph%num_vertices))

        distances = real(INFINITY, real64)
        distances(start) = 0.0_real64
        visited = .false.

        call pq%init(graph%num_vertices)
        call pq%push(pq_node(start, 0.0_real64))

        do while (.not. pq%is_empty())
            current_node = pq%pop()
            u = current_node%vertex

            if (visited(u)) cycle
            visited(u) = .true.

            neighbor => graph%adj_list(u)%head
            do while (associated(neighbor))
                v = neighbor%vertex
                new_dist = distances(u) + neighbor%weight

                if (new_dist < distances(v)) then
                    distances(v) = new_dist
                    call pq%push(pq_node(v, new_dist))
                end if

                neighbor => neighbor%next
            end do
        end do

    end function dijkstra

    !===============================================
    ! Bellman-Ford Algorithm
    !===============================================

    function bellman_ford(graph, start, has_negative_cycle) result(distances)
        implicit none
        type(weighted_graph_type), intent(in) :: graph
        integer(int32), intent(in) :: start
        logical, intent(out) :: has_negative_cycle
        real(real64), dimension(:), allocatable :: distances
        integer(int32) :: i, u, v
        type(adj_node), pointer :: neighbor
        real(real64) :: new_dist

        allocate(distances(graph%num_vertices))
        distances = real(INFINITY, real64)
        distances(start) = 0.0_real64
        has_negative_cycle = .false.

        ! Relax edges V-1 times
        do i = 1, graph%num_vertices - 1
            do u = 1, graph%num_vertices
                if (distances(u) < real(INFINITY, real64)) then
                    neighbor => graph%adj_list(u)%head
                    do while (associated(neighbor))
                        v = neighbor%vertex
                        new_dist = distances(u) + neighbor%weight
                        if (new_dist < distances(v)) then
                            distances(v) = new_dist
                        end if
                        neighbor => neighbor%next
                    end do
                end if
            end do
        end do

        ! Check for negative cycles
        do u = 1, graph%num_vertices
            neighbor => graph%adj_list(u)%head
            do while (associated(neighbor))
                v = neighbor%vertex
                if (distances(u) + neighbor%weight < distances(v)) then
                    has_negative_cycle = .true.
                    return
                end if
                neighbor => neighbor%next
            end do
        end do

    end function bellman_ford

    !===============================================
    ! Floyd-Warshall Algorithm
    !===============================================

    function floyd_warshall(graph) result(dist_matrix)
        implicit none
        type(weighted_graph_type), intent(in) :: graph
        real(real64), dimension(:,:), allocatable :: dist_matrix
        integer(int32) :: i, j, k

        allocate(dist_matrix(graph%num_vertices, graph%num_vertices))
        dist_matrix = graph%weight_matrix

        do k = 1, graph%num_vertices
            do i = 1, graph%num_vertices
                do j = 1, graph%num_vertices
                    if (dist_matrix(i, k) + dist_matrix(k, j) < dist_matrix(i, j)) then
                        dist_matrix(i, j) = dist_matrix(i, k) + dist_matrix(k, j)
                    end if
                end do
            end do
        end do

    end function floyd_warshall

    !===============================================
    ! Prim's MST Algorithm
    !===============================================

    function prim_mst(graph) result(mst_edges)
        implicit none
        type(weighted_graph_type), intent(in) :: graph
        type(edge_type), dimension(:), allocatable :: mst_edges
        logical, dimension(:), allocatable :: in_mst
        real(real64), dimension(:), allocatable :: key
        integer(int32), dimension(:), allocatable :: parent
        integer(int32) :: i, u, v, mst_count
        type(adj_node), pointer :: neighbor
        real(real64) :: min_key

        allocate(in_mst(graph%num_vertices))
        allocate(key(graph%num_vertices))
        allocate(parent(graph%num_vertices))
        allocate(mst_edges(graph%num_vertices - 1))

        in_mst = .false.
        key = real(INFINITY, real64)
        parent = -1
        key(1) = 0.0_real64
        mst_count = 0

        do i = 1, graph%num_vertices
            ! Find minimum key vertex not in MST
            min_key = real(INFINITY, real64)
            u = -1
            do v = 1, graph%num_vertices
                if (.not. in_mst(v) .and. key(v) < min_key) then
                    min_key = key(v)
                    u = v
                end if
            end do

            if (u == -1) exit
            in_mst(u) = .true.

            if (parent(u) > 0) then
                mst_count = mst_count + 1
                mst_edges(mst_count) = edge_type(parent(u), u, key(u))
            end if

            ! Update keys of adjacent vertices
            neighbor => graph%adj_list(u)%head
            do while (associated(neighbor))
                v = neighbor%vertex
                if (.not. in_mst(v) .and. neighbor%weight < key(v)) then
                    key(v) = neighbor%weight
                    parent(v) = u
                end if
                neighbor => neighbor%next
            end do
        end do

        mst_edges = mst_edges(1:mst_count)

    end function prim_mst

    !===============================================
    ! Kruskal's MST Algorithm
    !===============================================

    function kruskal_mst(graph) result(mst_edges)
        implicit none
        type(weighted_graph_type), intent(in) :: graph
        type(edge_type), dimension(:), allocatable :: mst_edges, all_edges
        type(union_find) :: uf
        integer(int32) :: i, u, v, edge_count, mst_count
        type(adj_node), pointer :: neighbor

        ! Collect all edges
        allocate(all_edges(graph%num_edges))
        edge_count = 0

        do u = 1, graph%num_vertices
            neighbor => graph%adj_list(u)%head
            do while (associated(neighbor))
                v = neighbor%vertex
                if (u < v .or. graph%is_directed) then
                    edge_count = edge_count + 1
                    all_edges(edge_count) = edge_type(u, v, neighbor%weight)
                end if
                neighbor => neighbor%next
            end do
        end do

        ! Sort edges by weight
        call sort_edges_by_weight(all_edges(1:edge_count))

        ! Initialize Union-Find
        call uf%init(graph%num_vertices)

        allocate(mst_edges(graph%num_vertices - 1))
        mst_count = 0

        do i = 1, edge_count
            u = uf%find(all_edges(i)%src)
            v = uf%find(all_edges(i)%dest)

            if (u /= v) then
                mst_count = mst_count + 1
                mst_edges(mst_count) = all_edges(i)
                call uf%union(u, v)
                if (mst_count == graph%num_vertices - 1) exit
            end if
        end do

        mst_edges = mst_edges(1:mst_count)

    end function kruskal_mst

    subroutine sort_edges_by_weight(edges)
        implicit none
        type(edge_type), dimension(:), intent(inout) :: edges
        integer(int32) :: i, j, n
        type(edge_type) :: temp

        n = size(edges)
        ! Simple bubble sort for edges
        do i = 1, n - 1
            do j = 1, n - i
                if (edges(j)%weight > edges(j+1)%weight) then
                    temp = edges(j)
                    edges(j) = edges(j+1)
                    edges(j+1) = temp
                end if
            end do
        end do

    end subroutine sort_edges_by_weight

    !===============================================
    ! Topological Sort
    !===============================================

    function topological_sort(graph) result(order)
        implicit none
        type(graph_type), intent(in) :: graph
        integer(int32), dimension(:), allocatable :: order
        integer(int32), dimension(:), allocatable :: in_degree
        integer(int32), dimension(:), allocatable :: queue
        integer(int32) :: front, rear, current, v, order_count
        type(adj_node), pointer :: neighbor

        allocate(in_degree(graph%num_vertices))
        allocate(queue(graph%num_vertices))
        allocate(order(graph%num_vertices))

        in_degree = 0

        ! Calculate in-degrees
        do v = 1, graph%num_vertices
            neighbor => graph%adj_list(v)%head
            do while (associated(neighbor))
                in_degree(neighbor%vertex) = in_degree(neighbor%vertex) + 1
                neighbor => neighbor%next
            end do
        end do

        ! Initialize queue with vertices having in-degree 0
        front = 1
        rear = 0
        do v = 1, graph%num_vertices
            if (in_degree(v) == 0) then
                rear = rear + 1
                queue(rear) = v
            end if
        end do

        order_count = 0

        do while (front <= rear)
            current = queue(front)
            front = front + 1
            order_count = order_count + 1
            order(order_count) = current

            neighbor => graph%adj_list(current)%head
            do while (associated(neighbor))
                in_degree(neighbor%vertex) = in_degree(neighbor%vertex) - 1
                if (in_degree(neighbor%vertex) == 0) then
                    rear = rear + 1
                    queue(rear) = neighbor%vertex
                end if
                neighbor => neighbor%next
            end do
        end do

        if (order_count < graph%num_vertices) then
            ! Graph has a cycle
            order = [-1]
        else
            order = order(1:order_count)
        end if

    end function topological_sort

    !===============================================
    ! Strongly Connected Components (Kosaraju's)
    !===============================================

    function kosaraju_scc(graph) result(components)
        implicit none
        type(graph_type), intent(in) :: graph
        integer(int32), dimension(:), allocatable :: components
        logical, dimension(:), allocatable :: visited
        integer(int32), dimension(:), allocatable :: finish_order
        integer(int32) :: i, order_count, component_id
        type(graph_type) :: reversed_graph

        allocate(visited(graph%num_vertices))
        allocate(finish_order(graph%num_vertices))
        allocate(components(graph%num_vertices))

        visited = .false.
        order_count = 0

        ! First DFS to get finish times
        do i = 1, graph%num_vertices
            if (.not. visited(i)) then
                call dfs_finish_time(graph, i, visited, finish_order, order_count)
            end if
        end do

        ! Create reversed graph
        call create_reversed_graph(graph, reversed_graph)

        ! Second DFS on reversed graph in reverse finish order
        visited = .false.
        components = 0
        component_id = 0

        do i = graph%num_vertices, 1, -1
            if (.not. visited(finish_order(i))) then
                component_id = component_id + 1
                call dfs_mark_component(reversed_graph, finish_order(i), &
                                       visited, components, component_id)
            end if
        end do

        call reversed_graph%destroy()

    contains

        recursive subroutine dfs_finish_time(g, v, vis, finish, count)
            implicit none
            type(graph_type), intent(in) :: g
            integer(int32), intent(in) :: v
            logical, dimension(:), intent(inout) :: vis
            integer(int32), dimension(:), intent(inout) :: finish
            integer(int32), intent(inout) :: count
            type(adj_node), pointer :: neighbor

            vis(v) = .true.

            neighbor => g%adj_list(v)%head
            do while (associated(neighbor))
                if (.not. vis(neighbor%vertex)) then
                    call dfs_finish_time(g, neighbor%vertex, vis, finish, count)
                end if
                neighbor => neighbor%next
            end do

            count = count + 1
            finish(count) = v

        end subroutine dfs_finish_time

        recursive subroutine dfs_mark_component(g, v, vis, comp, comp_id)
            implicit none
            type(graph_type), intent(in) :: g
            integer(int32), intent(in) :: v
            logical, dimension(:), intent(inout) :: vis
            integer(int32), dimension(:), intent(inout) :: comp
            integer(int32), intent(in) :: comp_id
            type(adj_node), pointer :: neighbor

            vis(v) = .true.
            comp(v) = comp_id

            neighbor => g%adj_list(v)%head
            do while (associated(neighbor))
                if (.not. vis(neighbor%vertex)) then
                    call dfs_mark_component(g, neighbor%vertex, vis, comp, comp_id)
                end if
                neighbor => neighbor%next
            end do

        end subroutine dfs_mark_component

        subroutine create_reversed_graph(original, reversed)
            implicit none
            type(graph_type), intent(in) :: original
            type(graph_type), intent(out) :: reversed
            integer(int32) :: u, v
            type(adj_node), pointer :: neighbor

            call reversed%init(original%num_vertices, .true.)

            do u = 1, original%num_vertices
                neighbor => original%adj_list(u)%head
                do while (associated(neighbor))
                    v = neighbor%vertex
                    call reversed%add_edge(v, u, neighbor%weight)
                    neighbor => neighbor%next
                end do
            end do

        end subroutine create_reversed_graph

    end function kosaraju_scc

    !===============================================
    ! Tarjan's SCC Algorithm
    !===============================================

    function strongly_connected_components(graph) result(components)
        implicit none
        type(graph_type), intent(in) :: graph
        integer(int32), dimension(:), allocatable :: components
        integer(int32), dimension(:), allocatable :: ids, low, on_stack_arr
        logical, dimension(:), allocatable :: on_stack
        integer(int32) :: id_counter, scc_count
        integer(int32), dimension(:), allocatable :: stack
        integer(int32) :: stack_size, i

        allocate(components(graph%num_vertices))
        allocate(ids(graph%num_vertices))
        allocate(low(graph%num_vertices))
        allocate(on_stack(graph%num_vertices))
        allocate(stack(graph%num_vertices))

        ids = -1
        low = -1
        on_stack = .false.
        components = 0
        id_counter = 0
        scc_count = 0
        stack_size = 0

        do i = 1, graph%num_vertices
            if (ids(i) == -1) then
                call tarjan_dfs(i)
            end if
        end do

    contains

        recursive subroutine tarjan_dfs(v)
            implicit none
            integer(int32), intent(in) :: v
            type(adj_node), pointer :: neighbor
            integer(int32) :: w

            id_counter = id_counter + 1
            ids(v) = id_counter
            low(v) = id_counter

            stack_size = stack_size + 1
            stack(stack_size) = v
            on_stack(v) = .true.

            neighbor => graph%adj_list(v)%head
            do while (associated(neighbor))
                w = neighbor%vertex

                if (ids(w) == -1) then
                    call tarjan_dfs(w)
                    low(v) = min(low(v), low(w))
                else if (on_stack(w)) then
                    low(v) = min(low(v), ids(w))
                end if

                neighbor => neighbor%next
            end do

            if (low(v) == ids(v)) then
                scc_count = scc_count + 1
                do
                    w = stack(stack_size)
                    stack_size = stack_size - 1
                    on_stack(w) = .false.
                    components(w) = scc_count
                    if (w == v) exit
                end do
            end if

        end subroutine tarjan_dfs

    end function strongly_connected_components

    !===============================================
    ! Cycle Detection
    !===============================================

    function is_cyclic(graph) result(has_cycle)
        implicit none
        type(graph_type), intent(in) :: graph
        logical :: has_cycle
        logical, dimension(:), allocatable :: visited, rec_stack
        integer(int32) :: i

        allocate(visited(graph%num_vertices))
        allocate(rec_stack(graph%num_vertices))

        visited = .false.
        rec_stack = .false.
        has_cycle = .false.

        if (graph%is_directed) then
            do i = 1, graph%num_vertices
                if (.not. visited(i)) then
                    if (dfs_cycle_directed(i)) then
                        has_cycle = .true.
                        return
                    end if
                end if
            end do
        else
            do i = 1, graph%num_vertices
                if (.not. visited(i)) then
                    if (dfs_cycle_undirected(i, -1)) then
                        has_cycle = .true.
                        return
                    end if
                end if
            end do
        end if

    contains

        recursive function dfs_cycle_directed(v) result(found)
            implicit none
            integer(int32), intent(in) :: v
            logical :: found
            type(adj_node), pointer :: neighbor

            visited(v) = .true.
            rec_stack(v) = .true.
            found = .false.

            neighbor => graph%adj_list(v)%head
            do while (associated(neighbor))
                if (.not. visited(neighbor%vertex)) then
                    if (dfs_cycle_directed(neighbor%vertex)) then
                        found = .true.
                        return
                    end if
                else if (rec_stack(neighbor%vertex)) then
                    found = .true.
                    return
                end if
                neighbor => neighbor%next
            end do

            rec_stack(v) = .false.

        end function dfs_cycle_directed

        recursive function dfs_cycle_undirected(v, parent) result(found)
            implicit none
            integer(int32), intent(in) :: v, parent
            logical :: found
            type(adj_node), pointer :: neighbor

            visited(v) = .true.
            found = .false.

            neighbor => graph%adj_list(v)%head
            do while (associated(neighbor))
                if (.not. visited(neighbor%vertex)) then
                    if (dfs_cycle_undirected(neighbor%vertex, v)) then
                        found = .true.
                        return
                    end if
                else if (neighbor%vertex /= parent) then
                    found = .true.
                    return
                end if
                neighbor => neighbor%next
            end do

        end function dfs_cycle_undirected

    end function is_cyclic

    !===============================================
    ! Bipartite Check
    !===============================================

    function is_bipartite(graph) result(bipartite)
        implicit none
        type(graph_type), intent(in) :: graph
        logical :: bipartite
        integer(int32), dimension(:), allocatable :: color
        integer(int32), dimension(:), allocatable :: queue
        integer(int32) :: i, front, rear, current
        type(adj_node), pointer :: neighbor

        allocate(color(graph%num_vertices))
        allocate(queue(graph%num_vertices))

        color = -1
        bipartite = .true.

        do i = 1, graph%num_vertices
            if (color(i) == -1) then
                front = 1
                rear = 1
                queue(1) = i
                color(i) = 0

                do while (front <= rear)
                    current = queue(front)
                    front = front + 1

                    neighbor => graph%adj_list(current)%head
                    do while (associated(neighbor))
                        if (color(neighbor%vertex) == -1) then
                            color(neighbor%vertex) = 1 - color(current)
                            rear = rear + 1
                            queue(rear) = neighbor%vertex
                        else if (color(neighbor%vertex) == color(current)) then
                            bipartite = .false.
                            return
                        end if
                        neighbor => neighbor%next
                    end do
                end do
            end if
        end do

    end function is_bipartite

    !===============================================
    ! Priority Queue Implementation
    !===============================================

    subroutine pq_init(this, capacity)
        implicit none
        class(priority_queue), intent(inout) :: this
        integer(int32), intent(in) :: capacity

        this%capacity = capacity
        this%size = 0
        allocate(this%heap(capacity))

    end subroutine pq_init

    subroutine pq_push(this, node)
        implicit none
        class(priority_queue), intent(inout) :: this
        type(pq_node), intent(in) :: node

        if (this%size >= this%capacity) return

        this%size = this%size + 1
        this%heap(this%size) = node
        call this%heapify_up(this%size)

    end subroutine pq_push

    function pq_pop(this) result(node)
        implicit none
        class(priority_queue), intent(inout) :: this
        type(pq_node) :: node

        if (this%size == 0) then
            node%vertex = -1
            node%distance = real(INFINITY, real64)
            return
        end if

        node = this%heap(1)
        this%heap(1) = this%heap(this%size)
        this%size = this%size - 1

        if (this%size > 0) then
            call this%heapify_down(1)
        end if

    end function pq_pop

    function pq_is_empty(this) result(empty)
        implicit none
        class(priority_queue), intent(in) :: this
        logical :: empty

        empty = (this%size == 0)

    end function pq_is_empty

    subroutine pq_heapify_up(this, index)
        implicit none
        class(priority_queue), intent(inout) :: this
        integer(int32), intent(in) :: index
        integer(int32) :: current, parent
        type(pq_node) :: temp

        current = index
        do while (current > 1)
            parent = current / 2
            if (this%heap(current)%distance < this%heap(parent)%distance) then
                temp = this%heap(current)
                this%heap(current) = this%heap(parent)
                this%heap(parent) = temp
                current = parent
            else
                exit
            end if
        end do

    end subroutine pq_heapify_up

    subroutine pq_heapify_down(this, index)
        implicit none
        class(priority_queue), intent(inout) :: this
        integer(int32), intent(in) :: index
        integer(int32) :: current, left, right, smallest
        type(pq_node) :: temp

        current = index
        do
            left = 2 * current
            right = 2 * current + 1
            smallest = current

            if (left <= this%size .and. &
                this%heap(left)%distance < this%heap(smallest)%distance) then
                smallest = left
            end if

            if (right <= this%size .and. &
                this%heap(right)%distance < this%heap(smallest)%distance) then
                smallest = right
            end if

            if (smallest /= current) then
                temp = this%heap(current)
                this%heap(current) = this%heap(smallest)
                this%heap(smallest) = temp
                current = smallest
            else
                exit
            end if
        end do

    end subroutine pq_heapify_down

    !===============================================
    ! Union-Find Implementation
    !===============================================

    subroutine uf_init(this, n)
        implicit none
        class(union_find), intent(inout) :: this
        integer(int32), intent(in) :: n
        integer(int32) :: i

        allocate(this%parent(n))
        allocate(this%rank(n))

        do i = 1, n
            this%parent(i) = i
            this%rank(i) = 0
        end do

    end subroutine uf_init

    recursive function uf_find(this, x) result(root)
        implicit none
        class(union_find), intent(inout) :: this
        integer(int32), intent(in) :: x
        integer(int32) :: root

        if (this%parent(x) /= x) then
            this%parent(x) = this%find(this%parent(x))  ! Path compression
        end if
        root = this%parent(x)

    end function uf_find

    subroutine uf_union(this, x, y)
        implicit none
        class(union_find), intent(inout) :: this
        integer(int32), intent(in) :: x, y
        integer(int32) :: root_x, root_y

        root_x = this%find(x)
        root_y = this%find(y)

        if (root_x /= root_y) then
            if (this%rank(root_x) < this%rank(root_y)) then
                this%parent(root_x) = root_y
            else if (this%rank(root_x) > this%rank(root_y)) then
                this%parent(root_y) = root_x
            else
                this%parent(root_y) = root_x
                this%rank(root_x) = this%rank(root_x) + 1
            end if
        end if

    end subroutine uf_union

end module graph_module