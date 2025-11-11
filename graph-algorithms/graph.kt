/**
 * Comprehensive Graph Data Structure Implementation
 * Supports multiple representations and core graph algorithms
 */

import java.util.*
import kotlin.math.max

enum class GraphType {
    DIRECTED, UNDIRECTED
}

enum class RepresentationType {
    ADJACENCY_LIST, ADJACENCY_MATRIX, EDGE_LIST, CSR
}

data class Edge(val src: Int, val dst: Int, val weight: Double)

data class Neighbor(val vertex: Int, val weight: Double)

class Graph(
    var numVertices: Int,
    private val graphType: GraphType = GraphType.UNDIRECTED,
    private val weighted: Boolean = false,
    private val representation: RepresentationType = RepresentationType.ADJACENCY_LIST
) {
    var numEdges: Int = 0
        private set

    // Different representations
    private val adjList: MutableMap<Int, MutableList<Neighbor>> = mutableMapOf()
    private var adjMatrix: Array<Array<Double?>> = Array(numVertices) { arrayOfNulls(numVertices) }
    private val edges: MutableList<Edge> = mutableListOf()
    private val csrValues: MutableList<Double> = mutableListOf()
    private val csrColIndices: MutableList<Int> = mutableListOf()
    private val csrRowPtr: MutableList<Int> = mutableListOf()

    init {
        // Initialize based on representation type
        when (representation) {
            RepresentationType.ADJACENCY_LIST -> {
                // adjList is already initialized
            }
            RepresentationType.ADJACENCY_MATRIX -> {
                // adjMatrix is already initialized
            }
            RepresentationType.EDGE_LIST -> {
                // edges is already initialized
            }
            RepresentationType.CSR -> {
                csrRowPtr.add(0)
            }
        }
    }

    /**
     * Add a new vertex and return its ID
     */
    fun addVertex(): Int {
        val vertexId = numVertices
        numVertices++

        if (representation == RepresentationType.ADJACENCY_MATRIX) {
            // Expand matrix
            val newMatrix = Array(numVertices) { arrayOfNulls<Double>(numVertices) }
            for (i in adjMatrix.indices) {
                for (j in adjMatrix[i].indices) {
                    newMatrix[i][j] = adjMatrix[i][j]
                }
            }
            adjMatrix = newMatrix
        }

        return vertexId
    }

    /**
     * Add an edge from u to v with optional weight
     */
    fun addEdge(u: Int, v: Int, weight: Double = 1.0) {
        require(u < numVertices && v < numVertices) {
            "Vertex out of range: $u or $v"
        }

        numEdges++

        when (representation) {
            RepresentationType.ADJACENCY_LIST -> {
                adjList.getOrPut(u) { mutableListOf() }.add(Neighbor(v, weight))
                if (graphType == GraphType.UNDIRECTED) {
                    adjList.getOrPut(v) { mutableListOf() }.add(Neighbor(u, weight))
                }
            }
            RepresentationType.ADJACENCY_MATRIX -> {
                adjMatrix[u][v] = weight
                if (graphType == GraphType.UNDIRECTED) {
                    adjMatrix[v][u] = weight
                }
            }
            RepresentationType.EDGE_LIST -> {
                edges.add(Edge(u, v, weight))
                if (graphType == GraphType.UNDIRECTED) {
                    edges.add(Edge(v, u, weight))
                }
            }
            RepresentationType.CSR -> {
                throw UnsupportedOperationException("CSR edges should be added via buildCSR()")
            }
        }
    }

    /**
     * Build CSR representation from edge list
     */
    fun buildCSR(edgeList: List<Edge>) {
        require(representation == RepresentationType.CSR) {
            "Graph must be CSR type"
        }

        // Sort edges by source vertex
        val sortedEdges = edgeList.sortedWith(compareBy({ it.src }, { it.dst }))

        csrValues.clear()
        csrColIndices.clear()
        csrRowPtr.clear()
        csrRowPtr.add(0)

        var currentRow = 0
        for (edge in sortedEdges) {
            // Fill gaps for vertices with no outgoing edges
            while (currentRow < edge.src) {
                csrRowPtr.add(csrColIndices.size)
                currentRow++
            }

            csrValues.add(edge.weight)
            csrColIndices.add(edge.dst)
        }

        // Complete row pointers
        while (currentRow < numVertices) {
            csrRowPtr.add(csrColIndices.size)
            currentRow++
        }

        numEdges = sortedEdges.size
    }

    /**
     * Get neighbors of vertex u with their edge weights
     */
    fun getNeighbors(u: Int): List<Neighbor> {
        return when (representation) {
            RepresentationType.ADJACENCY_LIST -> {
                adjList[u] ?: emptyList()
            }
            RepresentationType.ADJACENCY_MATRIX -> {
                val neighbors = mutableListOf<Neighbor>()
                for (v in 0 until numVertices) {
                    adjMatrix[u][v]?.let { weight ->
                        neighbors.add(Neighbor(v, weight))
                    }
                }
                neighbors
            }
            RepresentationType.EDGE_LIST -> {
                edges.filter { it.src == u }
                    .map { Neighbor(it.dst, it.weight) }
            }
            RepresentationType.CSR -> {
                val neighbors = mutableListOf<Neighbor>()
                val start = csrRowPtr[u]
                val end = csrRowPtr[u + 1]
                for (i in start until end) {
                    neighbors.add(Neighbor(csrColIndices[i], csrValues[i]))
                }
                neighbors
            }
        }
    }

    // === DEPTH-FIRST SEARCH ===

    /**
     * DFS traversal using recursion
     */
    fun dfsRecursive(start: Int): List<Int> {
        val visited = mutableSetOf<Int>()
        val traversal = mutableListOf<Int>()
        dfsHelper(start, visited, traversal)
        return traversal
    }

    private fun dfsHelper(v: Int, visited: MutableSet<Int>, traversal: MutableList<Int>) {
        visited.add(v)
        traversal.add(v)

        for (neighbor in getNeighbors(v)) {
            if (neighbor.vertex !in visited) {
                dfsHelper(neighbor.vertex, visited, traversal)
            }
        }
    }

    /**
     * DFS traversal using iteration with stack
     */
    fun dfsIterative(start: Int): List<Int> {
        val visited = mutableSetOf<Int>()
        val traversal = mutableListOf<Int>()
        val stack = Stack<Int>()
        stack.push(start)

        while (stack.isNotEmpty()) {
            val v = stack.pop()
            if (v !in visited) {
                visited.add(v)
                traversal.add(v)

                // Add neighbors in reverse order for consistent ordering
                val neighbors = getNeighbors(v)
                for (i in neighbors.indices.reversed()) {
                    val neighbor = neighbors[i]
                    if (neighbor.vertex !in visited) {
                        stack.push(neighbor.vertex)
                    }
                }
            }
        }

        return traversal
    }

    // === BREADTH-FIRST SEARCH ===

    /**
     * BFS traversal
     */
    fun bfs(start: Int): List<Int> {
        val visited = mutableSetOf(start)
        val traversal = mutableListOf<Int>()
        val queue: Queue<Int> = LinkedList()
        queue.offer(start)

        while (queue.isNotEmpty()) {
            val v = queue.poll()
            traversal.add(v)

            for (neighbor in getNeighbors(v)) {
                if (neighbor.vertex !in visited) {
                    visited.add(neighbor.vertex)
                    queue.offer(neighbor.vertex)
                }
            }
        }

        return traversal
    }

    // === TOPOLOGICAL SORTING ===

    /**
     * Topological sorting using Kahn's algorithm (BFS-based)
     * Returns null if graph contains a cycle
     */
    fun topologicalSort(): List<Int>? {
        require(graphType == GraphType.DIRECTED) {
            "Topological sort only works for directed graphs"
        }

        // Calculate in-degrees
        val inDegree = IntArray(numVertices)
        for (u in 0 until numVertices) {
            for (neighbor in getNeighbors(u)) {
                inDegree[neighbor.vertex]++
            }
        }

        // Queue with vertices having 0 in-degree
        val queue: Queue<Int> = LinkedList()
        for (v in 0 until numVertices) {
            if (inDegree[v] == 0) {
                queue.offer(v)
            }
        }

        val result = mutableListOf<Int>()

        while (queue.isNotEmpty()) {
            val u = queue.poll()
            result.add(u)

            for (neighbor in getNeighbors(u)) {
                inDegree[neighbor.vertex]--
                if (inDegree[neighbor.vertex] == 0) {
                    queue.offer(neighbor.vertex)
                }
            }
        }

        // Check if all vertices were processed (no cycle)
        return if (result.size == numVertices) result else null
    }

    /**
     * Topological sorting using DFS
     */
    fun topologicalSortDFS(): List<Int>? {
        require(graphType == GraphType.DIRECTED) {
            "Topological sort only works for directed graphs"
        }

        val visited = mutableSetOf<Int>()
        val recStack = mutableSetOf<Int>()
        val result = mutableListOf<Int>()

        fun dfsHelper(v: Int): Boolean {
            visited.add(v)
            recStack.add(v)

            for (neighbor in getNeighbors(v)) {
                if (neighbor.vertex !in visited) {
                    if (!dfsHelper(neighbor.vertex)) {
                        return false
                    }
                } else if (neighbor.vertex in recStack) {
                    return false  // Cycle detected
                }
            }

            recStack.remove(v)
            result.add(v)
            return true
        }

        for (v in 0 until numVertices) {
            if (v !in visited) {
                if (!dfsHelper(v)) {
                    return null  // Cycle detected
                }
            }
        }

        return result.reversed()
    }

    // === CONNECTED COMPONENTS ===

    /**
     * Find all connected components in the graph
     */
    fun findConnectedComponents(): List<List<Int>> {
        val visited = mutableSetOf<Int>()
        val components = mutableListOf<List<Int>>()

        for (v in 0 until numVertices) {
            if (v !in visited) {
                val component = mutableListOf<Int>()
                val stack = Stack<Int>()
                stack.push(v)

                while (stack.isNotEmpty()) {
                    val u = stack.pop()
                    if (u !in visited) {
                        visited.add(u)
                        component.add(u)

                        for (neighbor in getNeighbors(u)) {
                            if (neighbor.vertex !in visited) {
                                stack.push(neighbor.vertex)
                            }
                        }
                    }
                }

                components.add(component.sorted())
            }
        }

        return components
    }

    /**
     * Check if graph is connected
     */
    fun isConnected(): Boolean {
        if (numVertices == 0) return true
        return findConnectedComponents().size == 1
    }

    // === CYCLE DETECTION ===

    /**
     * Detect cycle in undirected graph using DFS
     */
    fun hasCycleUndirected(): Boolean {
        require(graphType == GraphType.UNDIRECTED) {
            "This method is for undirected graphs"
        }

        val visited = mutableSetOf<Int>()

        fun dfsHelper(v: Int, parent: Int): Boolean {
            visited.add(v)

            for (neighbor in getNeighbors(v)) {
                if (neighbor.vertex !in visited) {
                    if (dfsHelper(neighbor.vertex, v)) {
                        return true
                    }
                } else if (neighbor.vertex != parent) {
                    return true  // Cycle found
                }
            }

            return false
        }

        for (v in 0 until numVertices) {
            if (v !in visited) {
                if (dfsHelper(v, -1)) {
                    return true
                }
            }
        }

        return false
    }

    /**
     * Detect cycle in directed graph using DFS with recursion stack
     */
    fun hasCycleDirected(): Boolean {
        require(graphType == GraphType.DIRECTED) {
            "This method is for directed graphs"
        }

        val visited = mutableSetOf<Int>()
        val recStack = mutableSetOf<Int>()

        fun dfsHelper(v: Int): Boolean {
            visited.add(v)
            recStack.add(v)

            for (neighbor in getNeighbors(v)) {
                if (neighbor.vertex !in visited) {
                    if (dfsHelper(neighbor.vertex)) {
                        return true
                    }
                } else if (neighbor.vertex in recStack) {
                    return true  // Back edge found
                }
            }

            recStack.remove(v)
            return false
        }

        for (v in 0 until numVertices) {
            if (v !in visited) {
                if (dfsHelper(v)) {
                    return true
                }
            }
        }

        return false
    }

    /**
     * Detect cycle based on graph type
     */
    fun hasCycle(): Boolean {
        return when (graphType) {
            GraphType.DIRECTED -> hasCycleDirected()
            GraphType.UNDIRECTED -> hasCycleUndirected()
        }
    }

    // === GRAPH COLORING ===

    /**
     * Graph coloring using greedy algorithm
     * Returns mapping of vertex -> color
     */
    fun greedyColoring(): Map<Int, Int> {
        val colors = mutableMapOf<Int, Int>()

        for (v in 0 until numVertices) {
            // Get colors of neighbors
            val neighborColors = mutableSetOf<Int>()
            for (neighbor in getNeighbors(v)) {
                colors[neighbor.vertex]?.let { neighborColors.add(it) }
            }

            // Find first available color
            var color = 0
            while (color in neighborColors) {
                color++
            }

            colors[v] = color
        }

        return colors
    }

    /**
     * Get upper bound on chromatic number
     */
    fun chromaticNumberUpperBound(): Int {
        val coloring = greedyColoring()
        if (coloring.isEmpty()) return 0
        return (coloring.values.maxOrNull() ?: 0) + 1
    }

    // === VISUALIZATION ===

    /**
     * Generate ASCII art representation of the graph
     */
    fun toASCII(maxWidth: Int = 80): String {
        val sb = StringBuilder()

        sb.append("=".repeat(maxWidth)).append("\n")
        sb.append("Graph: $graphType, ${if (weighted) "weighted" else "unweighted"}\n")
        sb.append("Representation: $representation\n")
        sb.append("Vertices: $numVertices, Edges: $numEdges\n")
        sb.append("=".repeat(maxWidth)).append("\n\n")

        when (representation) {
            RepresentationType.ADJACENCY_LIST -> {
                sb.append("Adjacency List:\n")
                for (v in 0 until numVertices) {
                    val neighbors = getNeighbors(v)
                    sb.append("  $v -> [")
                    sb.append(neighbors.joinToString(", ") { neighbor ->
                        if (weighted) {
                            "${neighbor.vertex}(${String.format("%.1f", neighbor.weight)})"
                        } else {
                            "${neighbor.vertex}"
                        }
                    })
                    sb.append("]\n")
                }
            }
            RepresentationType.ADJACENCY_MATRIX -> {
                sb.append("Adjacency Matrix:\n")
                val displaySize = minOf(numVertices, 15)

                // Header
                sb.append("    ")
                for (i in 0 until displaySize) {
                    sb.append(String.format("%4d ", i))
                }
                sb.append("\n    ").append("-".repeat(5 * displaySize)).append("\n")

                for (i in 0 until displaySize) {
                    sb.append(String.format("%2d |", i))
                    for (j in 0 until displaySize) {
                        val weight = adjMatrix[i][j]
                        if (weight == null) {
                            sb.append("   . ")
                        } else {
                            sb.append(String.format("%4.0f ", weight))
                        }
                    }
                    sb.append("\n")
                }

                if (numVertices > 15) {
                    sb.append("  ... (truncated)\n")
                }
            }
            RepresentationType.EDGE_LIST -> {
                sb.append("Edge List:\n")
                val displayLimit = minOf(edges.size, 50)
                for (i in 0 until displayLimit) {
                    val edge = edges[i]
                    if (weighted) {
                        sb.append(String.format("  %d: %d -> %d (weight: %.1f)\n",
                            i, edge.src, edge.dst, edge.weight))
                    } else {
                        sb.append("  $i: ${edge.src} -> ${edge.dst}\n")
                    }
                }
                if (edges.size > 50) {
                    sb.append("  ... (${edges.size - 50} more edges)\n")
                }
            }
            RepresentationType.CSR -> {
                sb.append("CSR (Compressed Sparse Row):\n")
                val valLimit = minOf(csrValues.size, 20)
                sb.append("  Values: [")
                sb.append(csrValues.take(valLimit).joinToString(", ") { String.format("%.1f", it) })
                if (csrValues.size > 20) sb.append(", ...")
                sb.append("]\n")

                val colLimit = minOf(csrColIndices.size, 20)
                sb.append("  Col Indices: [")
                sb.append(csrColIndices.take(colLimit).joinToString(", "))
                if (csrColIndices.size > 20) sb.append(", ...")
                sb.append("]\n")

                val rowLimit = minOf(csrRowPtr.size, 20)
                sb.append("  Row Ptrs: [")
                sb.append(csrRowPtr.take(rowLimit).joinToString(", "))
                if (csrRowPtr.size > 20) sb.append(", ...")
                sb.append("]\n")
            }
        }

        sb.append("\n").append("=".repeat(maxWidth)).append("\n")
        return sb.toString()
    }

    override fun toString(): String = toASCII()
}

// === GRAPH GENERATORS ===

object GraphGenerator {
    /**
     * Generate a complete graph with n vertices
     */
    fun completeGraph(
        n: Int,
        graphType: GraphType = GraphType.UNDIRECTED,
        representation: RepresentationType = RepresentationType.ADJACENCY_LIST
    ): Graph {
        val g = Graph(n, graphType, false, representation)

        if (representation == RepresentationType.CSR) {
            val edges = mutableListOf<Edge>()
            for (i in 0 until n) {
                for (j in 0 until n) {
                    if (i != j) {
                        edges.add(Edge(i, j, 1.0))
                    }
                }
            }
            g.buildCSR(edges)
        } else {
            for (i in 0 until n) {
                for (j in i + 1 until n) {
                    g.addEdge(i, j)
                    if (graphType == GraphType.DIRECTED) {
                        g.addEdge(j, i)
                    }
                }
            }
        }

        return g
    }

    /**
     * Generate a cycle graph with n vertices
     */
    fun cycleGraph(
        n: Int,
        graphType: GraphType = GraphType.UNDIRECTED,
        representation: RepresentationType = RepresentationType.ADJACENCY_LIST
    ): Graph {
        val g = Graph(n, graphType, false, representation)

        if (representation == RepresentationType.CSR) {
            val edges = mutableListOf<Edge>()
            for (i in 0 until n) {
                edges.add(Edge(i, (i + 1) % n, 1.0))
                if (graphType == GraphType.UNDIRECTED) {
                    edges.add(Edge((i + 1) % n, i, 1.0))
                }
            }
            g.buildCSR(edges)
        } else {
            for (i in 0 until n) {
                g.addEdge(i, (i + 1) % n)
            }
        }

        return g
    }

    /**
     * Generate random graph with Erdős-Rényi model
     */
    fun randomGraph(
        n: Int,
        edgeProbability: Double,
        graphType: GraphType = GraphType.UNDIRECTED,
        weighted: Boolean = false,
        representation: RepresentationType = RepresentationType.ADJACENCY_LIST
    ): Graph {
        val g = Graph(n, graphType, weighted, representation)
        val edges = mutableListOf<Edge>()

        for (i in 0 until n) {
            val start = if (graphType == GraphType.UNDIRECTED) i + 1 else 0
            for (j in start until n) {
                if (i != j && Math.random() < edgeProbability) {
                    val weight = if (weighted) Math.random() * 9 + 1 else 1.0
                    edges.add(Edge(i, j, weight))
                }
            }
        }

        if (representation == RepresentationType.CSR) {
            if (graphType == GraphType.UNDIRECTED) {
                val reversed = edges.map { Edge(it.dst, it.src, it.weight) }
                edges.addAll(reversed)
            }
            g.buildCSR(edges.sortedWith(compareBy({ it.src }, { it.dst })))
        } else {
            for (edge in edges) {
                g.addEdge(edge.src, edge.dst, edge.weight)
            }
        }

        return g
    }

    /**
     * Generate a random Directed Acyclic Graph (DAG)
     */
    fun dag(
        n: Int,
        edgeProbability: Double,
        representation: RepresentationType = RepresentationType.ADJACENCY_LIST
    ): Graph {
        val g = Graph(n, GraphType.DIRECTED, false, representation)
        val edges = mutableListOf<Edge>()

        for (i in 0 until n) {
            for (j in i + 1 until n) {
                if (Math.random() < edgeProbability) {
                    edges.add(Edge(i, j, 1.0))
                }
            }
        }

        if (representation == RepresentationType.CSR) {
            g.buildCSR(edges)
        } else {
            for (edge in edges) {
                g.addEdge(edge.src, edge.dst, edge.weight)
            }
        }

        return g
    }
}

// === DEMO AND TESTING ===

fun demo() {
    println("=".repeat(80))
    println("GRAPH DATA STRUCTURES AND ALGORITHMS DEMO")
    println("=".repeat(80))
    println()

    // Demo 1: Adjacency List
    println("1. ADJACENCY LIST REPRESENTATION")
    println("-".repeat(80))
    val g1 = Graph(5, GraphType.UNDIRECTED, false, RepresentationType.ADJACENCY_LIST)
    g1.addEdge(0, 1)
    g1.addEdge(0, 4)
    g1.addEdge(1, 2)
    g1.addEdge(1, 3)
    g1.addEdge(1, 4)
    g1.addEdge(2, 3)
    g1.addEdge(3, 4)
    println(g1.toASCII())

    // Demo 2: DFS and BFS
    println("2. GRAPH TRAVERSAL")
    println("-".repeat(80))
    println("DFS Recursive from 0: ${g1.dfsRecursive(0)}")
    println("DFS Iterative from 0: ${g1.dfsIterative(0)}")
    println("BFS from 0: ${g1.bfs(0)}")
    println()

    // Demo 3: Connected Components
    println("3. CONNECTED COMPONENTS")
    println("-".repeat(80))
    val g2 = Graph(7, GraphType.UNDIRECTED)
    g2.addEdge(0, 1)
    g2.addEdge(1, 2)
    g2.addEdge(3, 4)
    g2.addEdge(5, 6)
    println("Components: ${g2.findConnectedComponents()}")
    println("Is connected: ${g2.isConnected()}")
    println()

    // Demo 4: Cycle Detection
    println("4. CYCLE DETECTION")
    println("-".repeat(80))
    println("Graph g1 has cycle: ${g1.hasCycle()}")
    val g3 = Graph(3, GraphType.UNDIRECTED)
    g3.addEdge(0, 1)
    g3.addEdge(1, 2)
    println("Linear graph has cycle: ${g3.hasCycle()}")
    println()

    // Demo 5: Topological Sort
    println("5. TOPOLOGICAL SORTING")
    println("-".repeat(80))
    val dag = GraphGenerator.dag(6, 0.3)
    println(dag.toASCII())
    println("Topological order: ${dag.topologicalSort()}")
    println("Topological order (DFS): ${dag.topologicalSortDFS()}")
    println()

    // Demo 6: Graph Coloring
    println("6. GRAPH COLORING")
    println("-".repeat(80))
    println("Greedy coloring: ${g1.greedyColoring()}")
    println("Chromatic number (upper bound): ${g1.chromaticNumberUpperBound()}")
    println()

    // Demo 7: Different Representations
    println("7. ADJACENCY MATRIX REPRESENTATION")
    println("-".repeat(80))
    val g4 = Graph(5, GraphType.DIRECTED, true, RepresentationType.ADJACENCY_MATRIX)
    g4.addEdge(0, 1, 2.5)
    g4.addEdge(0, 2, 1.0)
    g4.addEdge(1, 3, 3.0)
    g4.addEdge(2, 3, 1.5)
    g4.addEdge(3, 4, 2.0)
    println(g4.toASCII())

    // Demo 8: Graph Generators
    println("8. GRAPH GENERATORS")
    println("-".repeat(80))
    val complete = GraphGenerator.completeGraph(5)
    println("Complete graph K5:")
    println(complete.toASCII())

    val cycle = GraphGenerator.cycleGraph(6)
    println("Cycle graph C6:")
    println(cycle.toASCII())
}

fun main() {
    demo()
}
