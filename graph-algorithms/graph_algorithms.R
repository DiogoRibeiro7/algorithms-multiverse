# Graph Algorithms in R
#
# Implementations of fundamental graph algorithms:
# - Breadth-First Search (BFS)
# - Depth-First Search (DFS)
# - Dijkstra's Shortest Path
#
# Graph representation: Adjacency List (efficient for sparse graphs)

#' Create an empty graph
#'
#' @param num_vertices Number of vertices
#' @return Graph as a list of adjacency lists
create_graph <- function(num_vertices) {
    graph <- vector("list", num_vertices)
    for (i in 1:num_vertices) {
        graph[[i]] <- list()
    }
    return(graph)
}

#' Add edge to graph
#'
#' @param graph Graph structure
#' @param from Source vertex (1-indexed)
#' @param to Destination vertex (1-indexed)
#' @param weight Edge weight
#' @param directed Whether graph is directed
add_edge <- function(graph, from, to, weight = 1, directed = FALSE) {
    # Add edge from -> to
    graph[[from]] <- c(graph[[from]], list(list(vertex = to, weight = weight)))

    # For undirected graph, add edge to -> from
    if (!directed) {
        graph[[to]] <- c(graph[[to]], list(list(vertex = from, weight = weight)))
    }

    return(graph)
}

#' Print graph structure
print_graph <- function(graph) {
    cat("Graph adjacency list:\n")
    for (v in 1:length(graph)) {
        cat(sprintf("Vertex %d:", v - 1))
        for (neighbor in graph[[v]]) {
            cat(sprintf(" -> %d(w:%d)", neighbor$vertex - 1, neighbor$weight))
        }
        cat("\n")
    }
}

# ===================================================================
# BREADTH-FIRST SEARCH (BFS)
# ===================================================================

#' Breadth-First Search
#'
#' @param graph Graph structure
#' @param start Starting vertex (1-indexed)
#' @return Vector of visited vertices in BFS order
bfs <- function(graph, start) {
    num_vertices <- length(graph)
    visited <- rep(FALSE, num_vertices)
    queue <- c()
    result <- c()

    # Enqueue start vertex
    visited[start] <- TRUE
    queue <- c(queue, start)

    while (length(queue) > 0) {
        # Dequeue
        current <- queue[1]
        queue <- queue[-1]

        result <- c(result, current - 1)  # Store 0-indexed

        # Visit all adjacent vertices
        for (neighbor in graph[[current]]) {
            adj_vertex <- neighbor$vertex
            if (!visited[adj_vertex]) {
                visited[adj_vertex] <- TRUE
                queue <- c(queue, adj_vertex)
            }
        }
    }

    return(result)
}

# ===================================================================
# DEPTH-FIRST SEARCH (DFS)
# ===================================================================

#' Depth-First Search (recursive)
#'
#' @param graph Graph structure
#' @param start Starting vertex (1-indexed)
#' @return Vector of visited vertices in DFS order
dfs <- function(graph, start) {
    num_vertices <- length(graph)
    visited <- rep(FALSE, num_vertices)
    result <- c()

    dfs_util <- function(vertex) {
        visited[vertex] <<- TRUE
        result <<- c(result, vertex - 1)  # Store 0-indexed

        # Visit all adjacent vertices
        for (neighbor in graph[[vertex]]) {
            adj_vertex <- neighbor$vertex
            if (!visited[adj_vertex]) {
                dfs_util(adj_vertex)
            }
        }
    }

    dfs_util(start)
    return(result)
}

# ===================================================================
# DIJKSTRA'S SHORTEST PATH
# ===================================================================

#' Dijkstra's Shortest Path Algorithm
#'
#' @param graph Graph structure
#' @param src Source vertex (1-indexed)
#' @return Vector of shortest distances from source
dijkstra <- function(graph, src) {
    num_vertices <- length(graph)
    dist <- rep(Inf, num_vertices)
    visited <- rep(FALSE, num_vertices)

    dist[src] <- 0

    for (count in 1:num_vertices) {
        # Find minimum distance vertex not yet visited
        min_dist <- Inf
        u <- -1

        for (v in 1:num_vertices) {
            if (!visited[v] && dist[v] < min_dist) {
                min_dist <- dist[v]
                u <- v
            }
        }

        if (u == -1 || dist[u] == Inf) break  # All reachable vertices processed

        visited[u] <- TRUE

        # Update distances of adjacent vertices
        for (neighbor in graph[[u]]) {
            v <- neighbor$vertex
            weight <- neighbor$weight

            if (!visited[v] && dist[u] + weight < dist[v]) {
                dist[v] <- dist[u] + weight
            }
        }
    }

    return(dist)
}

# ===================================================================
# MAIN DEMONSTRATION
# ===================================================================

cat(rep('=', 70), '\n')
cat('                    GRAPH ALGORITHMS IN R\n')
cat(rep('=', 70), '\n\n')

# Create a graph with 6 vertices
num_vertices <- 6
graph <- create_graph(num_vertices)

# Add edges (undirected graph with weights)
# Using 1-indexed vertices in R
graph <- add_edge(graph, 1, 2, weight = 4)
graph <- add_edge(graph, 1, 3, weight = 3)
graph <- add_edge(graph, 2, 3, weight = 1)
graph <- add_edge(graph, 2, 4, weight = 2)
graph <- add_edge(graph, 3, 4, weight = 4)
graph <- add_edge(graph, 4, 5, weight = 2)
graph <- add_edge(graph, 5, 6, weight = 6)

# Print graph structure
print_graph(graph)
cat('\n')

# Test BFS
cat('Test 1: Breadth-First Search (BFS)\n')
cat(rep('-', 70), '\n')
bfs_result <- bfs(graph, 1)  # Start from vertex 0 (index 1 in R)
cat(sprintf('BFS traversal from vertex 0: %s\n', paste(bfs_result, collapse = ' ')))
cat('\n')

# Test DFS
cat('Test 2: Depth-First Search (DFS)\n')
cat(rep('-', 70), '\n')
dfs_result <- dfs(graph, 1)  # Start from vertex 0 (index 1 in R)
cat(sprintf('DFS traversal from vertex 0: %s\n', paste(dfs_result, collapse = ' ')))
cat('\n')

# Test Dijkstra
cat('Test 3: Dijkstra\'s Shortest Path Algorithm\n')
cat(rep('-', 70), '\n')
distances <- dijkstra(graph, 1)  # Start from vertex 0 (index 1 in R)

cat('\nDijkstra\'s shortest paths from vertex 0:\n')
cat('Vertex\tDistance from Source\n')
cat(rep('-', 40), '\n')

for (i in 1:num_vertices) {
    if (is.infinite(distances[i])) {
        cat(sprintf('%d\t\tINF\n', i - 1))
    } else {
        cat(sprintf('%d\t\t%d\n', i - 1, distances[i]))
    }
}

cat('\n', rep('=', 70), '\n')
cat('Key Points:\n')
cat('- BFS: O(V + E) time, explores level by level\n')
cat('  * Shortest path in unweighted graphs\n')
cat('  * Uses queue data structure\n')
cat('- DFS: O(V + E) time, explores depth-first\n')
cat('  * Good for detecting cycles, connectivity\n')
cat('  * Uses recursion/stack\n')
cat('- Dijkstra: O((V + E) log V) with heap, O(V²) with array\n')
cat('  * Shortest path in weighted graphs (non-negative weights)\n')
cat('  * Uses priority queue/min-heap\n')
cat('- Adjacency list: O(V + E) space, efficient for sparse graphs\n')
cat(rep('=', 70), '\n')

# Visualize paths (simple text representation)
cat('\nPath visualization:\n')
cat('Graph structure (vertex -> neighbors):\n')
cat('0 -> 1(4), 2(3)\n')
cat('1 -> 0(4), 2(1), 3(2)\n')
cat('2 -> 0(3), 1(1), 3(4)\n')
cat('3 -> 1(2), 2(4), 4(2)\n')
cat('4 -> 3(2), 5(6)\n')
cat('5 -> 4(6)\n')
cat('\nShortest paths from vertex 0:\n')
cat('0 -> 0: 0 (self)\n')
cat('0 -> 1: 4 (direct)\n')
cat('0 -> 2: 3 (direct)\n')
cat('0 -> 3: 6 (via 1 or 2)\n')
cat('0 -> 4: 8 (via 3)\n')
cat('0 -> 5: 14 (via 4)\n')
