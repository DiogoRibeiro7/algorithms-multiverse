"""
    GraphAlgorithms

Module containing graph algorithms implemented in Julia.
"""
module GraphAlgorithms

using DataStructures: PriorityQueue, enqueue!, dequeue!

export Graph, add_vertex!, add_edge!, dfs, bfs, dijkstra, bellman_ford,
       floyd_warshall, kruskal, prim, topological_sort, has_cycle,
       strongly_connected_components, is_bipartite

# Graph representation using adjacency list
mutable struct Graph
    directed::Bool
    vertices::Dict{Int, Vector{Tuple{Int, Float64}}}

    Graph(directed=false) = new(directed, Dict{Int, Vector{Tuple{Int, Float64}}}())
end

function add_vertex!(g::Graph, v::Int)
    if !haskey(g.vertices, v)
        g.vertices[v] = Vector{Tuple{Int, Float64}}()
    end
end

function add_edge!(g::Graph, from::Int, to::Int, weight::Float64=1.0)
    add_vertex!(g, from)
    add_vertex!(g, to)

    push!(g.vertices[from], (to, weight))
    if !g.directed
        push!(g.vertices[to], (from, weight))
    end
end

"""
    dfs(g::Graph, start::Int)

Perform depth-first search starting from vertex `start`.
"""
function dfs(g::Graph, start::Int)
    visited = Set{Int}()
    result = Int[]

    function dfs_visit(v::Int)
        push!(visited, v)
        push!(result, v)

        if haskey(g.vertices, v)
            for (neighbor, _) in g.vertices[v]
                if !(neighbor in visited)
                    dfs_visit(neighbor)
                end
            end
        end
    end

    dfs_visit(start)
    return result
end

"""
    bfs(g::Graph, start::Int)

Perform breadth-first search starting from vertex `start`.
"""
function bfs(g::Graph, start::Int)
    visited = Set{Int}()
    queue = [start]
    result = Int[]

    push!(visited, start)

    while !isempty(queue)
        v = popfirst!(queue)
        push!(result, v)

        if haskey(g.vertices, v)
            for (neighbor, _) in g.vertices[v]
                if !(neighbor in visited)
                    push!(visited, neighbor)
                    push!(queue, neighbor)
                end
            end
        end
    end

    return result
end

"""
    dijkstra(g::Graph, start::Int)

Find shortest paths from `start` to all other vertices using Dijkstra's algorithm.
"""
function dijkstra(g::Graph, start::Int)
    distances = Dict{Int, Float64}()
    previous = Dict{Int, Union{Int, Nothing}}()
    pq = PriorityQueue{Int, Float64}()

    for v in keys(g.vertices)
        distances[v] = Inf
        previous[v] = nothing
    end

    distances[start] = 0.0
    enqueue!(pq, start, 0.0)

    while !isempty(pq)
        current = dequeue!(pq)

        if haskey(g.vertices, current)
            for (neighbor, weight) in g.vertices[current]
                alt_dist = distances[current] + weight

                if alt_dist < distances[neighbor]
                    distances[neighbor] = alt_dist
                    previous[neighbor] = current
                    enqueue!(pq, neighbor, alt_dist)
                end
            end
        end
    end

    return distances, previous
end

"""
    bellman_ford(g::Graph, start::Int)

Find shortest paths using Bellman-Ford algorithm (handles negative weights).
"""
function bellman_ford(g::Graph, start::Int)
    distances = Dict{Int, Float64}()
    previous = Dict{Int, Union{Int, Nothing}}()

    for v in keys(g.vertices)
        distances[v] = Inf
        previous[v] = nothing
    end

    distances[start] = 0.0

    # Relax edges |V| - 1 times
    n_vertices = length(g.vertices)
    for _ in 1:n_vertices-1
        for v in keys(g.vertices)
            if distances[v] < Inf
                for (neighbor, weight) in g.vertices[v]
                    if distances[v] + weight < distances[neighbor]
                        distances[neighbor] = distances[v] + weight
                        previous[neighbor] = v
                    end
                end
            end
        end
    end

    # Check for negative cycles
    for v in keys(g.vertices)
        for (neighbor, weight) in g.vertices[v]
            if distances[v] + weight < distances[neighbor]
                error("Graph contains negative cycle")
            end
        end
    end

    return distances, previous
end

"""
    topological_sort(g::Graph)

Perform topological sort on a directed acyclic graph.
"""
function topological_sort(g::Graph)
    if !g.directed
        error("Topological sort requires a directed graph")
    end

    visited = Set{Int}()
    stack = Int[]

    function visit(v::Int)
        push!(visited, v)

        if haskey(g.vertices, v)
            for (neighbor, _) in g.vertices[v]
                if !(neighbor in visited)
                    visit(neighbor)
                end
            end
        end

        pushfirst!(stack, v)
    end

    for v in keys(g.vertices)
        if !(v in visited)
            visit(v)
        end
    end

    return stack
end

"""
    has_cycle(g::Graph)

Check if the graph contains a cycle.
"""
function has_cycle(g::Graph)
    visited = Set{Int}()
    rec_stack = Set{Int}()

    function has_cycle_util(v::Int, parent::Union{Int, Nothing}=nothing)
        push!(visited, v)
        push!(rec_stack, v)

        if haskey(g.vertices, v)
            for (neighbor, _) in g.vertices[v]
                if !(neighbor in visited)
                    if has_cycle_util(neighbor, v)
                        return true
                    end
                elseif g.directed
                    if neighbor in rec_stack
                        return true
                    end
                else
                    if neighbor != parent
                        return true
                    end
                end
            end
        end

        delete!(rec_stack, v)
        return false
    end

    for v in keys(g.vertices)
        if !(v in visited)
            if has_cycle_util(v)
                return true
            end
        end
    end

    return false
end

"""
    is_bipartite(g::Graph)

Check if the graph is bipartite (can be colored with two colors).
"""
function is_bipartite(g::Graph)
    colors = Dict{Int, Int}()

    for start in keys(g.vertices)
        if !haskey(colors, start)
            queue = [start]
            colors[start] = 0

            while !isempty(queue)
                v = popfirst!(queue)
                current_color = colors[v]

                if haskey(g.vertices, v)
                    for (neighbor, _) in g.vertices[v]
                        if haskey(colors, neighbor)
                            if colors[neighbor] == current_color
                                return false
                            end
                        else
                            colors[neighbor] = 1 - current_color
                            push!(queue, neighbor)
                        end
                    end
                end
            end
        end
    end

    return true
end

end # module GraphAlgorithms