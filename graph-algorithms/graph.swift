// Comprehensive Graph Data Structure Implementation
// Supports multiple representations and core graph algorithms

import Foundation

enum GraphType {
    case directed
    case undirected
}

enum RepresentationType {
    case adjacencyList
    case adjacencyMatrix
    case edgeList
    case csr  // Compressed Sparse Row
}

struct Edge {
    let src: Int
    let dst: Int
    let weight: Double
}

struct Neighbor {
    let vertex: Int
    let weight: Double
}

class Graph {
    private(set) var numVertices: Int
    private(set) var numEdges: Int
    private(set) var graphType: GraphType
    private(set) var weighted: Bool
    private(set) var representation: RepresentationType

    // Different representations
    private var adjList: [Int: [Neighbor]] = [:]
    private var adjMatrix: [[Double?]] = []
    private var edges: [Edge] = []
    private var csrValues: [Double] = []
    private var csrColIndices: [Int] = []
    private var csrRowPtr: [Int] = []

    init(numVertices: Int, graphType: GraphType = .undirected,
         weighted: Bool = false, representation: RepresentationType = .adjacencyList) {
        self.numVertices = numVertices
        self.numEdges = 0
        self.graphType = graphType
        self.weighted = weighted
        self.representation = representation

        // Initialize based on representation type
        switch representation {
        case .adjacencyList:
            break  // adjList is already initialized

        case .adjacencyMatrix:
            adjMatrix = Array(repeating: Array(repeating: nil, count: numVertices),
                            count: numVertices)

        case .edgeList:
            break  // edges is already initialized

        case .csr:
            csrRowPtr.append(0)
        }
    }

    // Add a new vertex and return its ID
    @discardableResult
    func addVertex() -> Int {
        let vertexId = numVertices
        numVertices += 1

        if representation == .adjacencyMatrix {
            // Expand matrix
            for i in 0..<adjMatrix.count {
                adjMatrix[i].append(nil)
            }
            adjMatrix.append(Array(repeating: nil, count: numVertices))
        }

        return vertexId
    }

    // Add an edge from u to v with optional weight
    func addEdge(_ u: Int, _ v: Int, weight: Double = 1.0) throws {
        guard u < numVertices && v < numVertices else {
            throw GraphError.vertexOutOfRange("Vertex out of range: \(u) or \(v)")
        }

        numEdges += 1

        switch representation {
        case .adjacencyList:
            adjList[u, default: []].append(Neighbor(vertex: v, weight: weight))
            if graphType == .undirected {
                adjList[v, default: []].append(Neighbor(vertex: u, weight: weight))
            }

        case .adjacencyMatrix:
            adjMatrix[u][v] = weight
            if graphType == .undirected {
                adjMatrix[v][u] = weight
            }

        case .edgeList:
            edges.append(Edge(src: u, dst: v, weight: weight))
            if graphType == .undirected {
                edges.append(Edge(src: v, dst: u, weight: weight))
            }

        case .csr:
            throw GraphError.invalidOperation("CSR edges should be added via buildCSR()")
        }
    }

    // Build CSR representation from edge list
    func buildCSR(edges edgeList: [Edge]) {
        guard representation == .csr else {
            fatalError("Graph must be CSR type")
        }

        // Sort edges by source vertex
        let sortedEdges = edgeList.sorted { ($0.src, $0.dst) < ($1.src, $1.dst) }

        csrValues = []
        csrColIndices = []
        csrRowPtr = [0]

        var currentRow = 0
        for edge in sortedEdges {
            // Fill gaps for vertices with no outgoing edges
            while currentRow < edge.src {
                csrRowPtr.append(csrColIndices.count)
                currentRow += 1
            }

            csrValues.append(edge.weight)
            csrColIndices.append(edge.dst)
        }

        // Complete row pointers
        while currentRow < numVertices {
            csrRowPtr.append(csrColIndices.count)
            currentRow += 1
        }

        numEdges = sortedEdges.count
    }

    // Get neighbors of vertex u with their edge weights
    func getNeighbors(_ u: Int) -> [Neighbor] {
        switch representation {
        case .adjacencyList:
            return adjList[u] ?? []

        case .adjacencyMatrix:
            var neighbors: [Neighbor] = []
            for (v, weightOpt) in adjMatrix[u].enumerated() {
                if let weight = weightOpt {
                    neighbors.append(Neighbor(vertex: v, weight: weight))
                }
            }
            return neighbors

        case .edgeList:
            return edges.filter { $0.src == u }
                .map { Neighbor(vertex: $0.dst, weight: $0.weight) }

        case .csr:
            var neighbors: [Neighbor] = []
            let start = csrRowPtr[u]
            let end = csrRowPtr[u + 1]
            for i in start..<end {
                neighbors.append(Neighbor(vertex: csrColIndices[i], weight: csrValues[i]))
            }
            return neighbors
        }
    }

    // === DEPTH-FIRST SEARCH ===

    // DFS traversal using recursion
    func dfsRecursive(start: Int) -> [Int] {
        var visited = Set<Int>()
        var traversal: [Int] = []
        dfsHelper(start, visited: &visited, traversal: &traversal)
        return traversal
    }

    private func dfsHelper(_ v: Int, visited: inout Set<Int>, traversal: inout [Int]) {
        visited.insert(v)
        traversal.append(v)

        for neighbor in getNeighbors(v) {
            if !visited.contains(neighbor.vertex) {
                dfsHelper(neighbor.vertex, visited: &visited, traversal: &traversal)
            }
        }
    }

    // DFS traversal using iteration with stack
    func dfsIterative(start: Int) -> [Int] {
        var visited = Set<Int>()
        var traversal: [Int] = []
        var stack = [start]

        while !stack.isEmpty {
            let v = stack.removeLast()
            if !visited.contains(v) {
                visited.insert(v)
                traversal.append(v)

                // Add neighbors in reverse order for consistent ordering
                let neighbors = getNeighbors(v)
                for neighbor in neighbors.reversed() {
                    if !visited.contains(neighbor.vertex) {
                        stack.append(neighbor.vertex)
                    }
                }
            }
        }

        return traversal
    }

    // === BREADTH-FIRST SEARCH ===

    // BFS traversal
    func bfs(start: Int) -> [Int] {
        var visited = Set<Int>([start])
        var traversal: [Int] = []
        var queue = [start]

        while !queue.isEmpty {
            let v = queue.removeFirst()
            traversal.append(v)

            for neighbor in getNeighbors(v) {
                if !visited.contains(neighbor.vertex) {
                    visited.insert(neighbor.vertex)
                    queue.append(neighbor.vertex)
                }
            }
        }

        return traversal
    }

    // === TOPOLOGICAL SORTING ===

    // Topological sorting using Kahn's algorithm (BFS-based)
    // Returns nil if graph contains a cycle
    func topologicalSort() -> [Int]? {
        guard graphType == .directed else {
            fatalError("Topological sort only works for directed graphs")
        }

        // Calculate in-degrees
        var inDegree = Array(repeating: 0, count: numVertices)
        for u in 0..<numVertices {
            for neighbor in getNeighbors(u) {
                inDegree[neighbor.vertex] += 1
            }
        }

        // Queue with vertices having 0 in-degree
        var queue = (0..<numVertices).filter { inDegree[$0] == 0 }
        var result: [Int] = []

        while !queue.isEmpty {
            let u = queue.removeFirst()
            result.append(u)

            for neighbor in getNeighbors(u) {
                inDegree[neighbor.vertex] -= 1
                if inDegree[neighbor.vertex] == 0 {
                    queue.append(neighbor.vertex)
                }
            }
        }

        // Check if all vertices were processed (no cycle)
        return result.count == numVertices ? result : nil
    }

    // Topological sorting using DFS
    func topologicalSortDFS() -> [Int]? {
        guard graphType == .directed else {
            fatalError("Topological sort only works for directed graphs")
        }

        var visited = Set<Int>()
        var recStack = Set<Int>()
        var result: [Int] = []

        func dfsHelper(_ v: Int) -> Bool {
            visited.insert(v)
            recStack.insert(v)

            for neighbor in getNeighbors(v) {
                if !visited.contains(neighbor.vertex) {
                    if !dfsHelper(neighbor.vertex) {
                        return false
                    }
                } else if recStack.contains(neighbor.vertex) {
                    return false  // Cycle detected
                }
            }

            recStack.remove(v)
            result.append(v)
            return true
        }

        for v in 0..<numVertices {
            if !visited.contains(v) {
                if !dfsHelper(v) {
                    return nil  // Cycle detected
                }
            }
        }

        return result.reversed()
    }

    // === CONNECTED COMPONENTS ===

    // Find all connected components in the graph
    func findConnectedComponents() -> [[Int]] {
        var visited = Set<Int>()
        var components: [[Int]] = []

        for v in 0..<numVertices {
            if !visited.contains(v) {
                var component: [Int] = []
                var stack = [v]

                while !stack.isEmpty {
                    let u = stack.removeLast()
                    if !visited.contains(u) {
                        visited.insert(u)
                        component.append(u)

                        for neighbor in getNeighbors(u) {
                            if !visited.contains(neighbor.vertex) {
                                stack.append(neighbor.vertex)
                            }
                        }
                    }
                }

                components.append(component.sorted())
            }
        }

        return components
    }

    // Check if graph is connected
    func isConnected() -> Bool {
        if numVertices == 0 { return true }
        return findConnectedComponents().count == 1
    }

    // === CYCLE DETECTION ===

    // Detect cycle in undirected graph using DFS
    func hasCycleUndirected() -> Bool {
        guard graphType == .undirected else {
            fatalError("This method is for undirected graphs")
        }

        var visited = Set<Int>()

        func dfsHelper(_ v: Int, parent: Int?) -> Bool {
            visited.insert(v)

            for neighbor in getNeighbors(v) {
                if !visited.contains(neighbor.vertex) {
                    if dfsHelper(neighbor.vertex, parent: v) {
                        return true
                    }
                } else if neighbor.vertex != parent {
                    return true  // Cycle found
                }
            }

            return false
        }

        for v in 0..<numVertices {
            if !visited.contains(v) {
                if dfsHelper(v, parent: nil) {
                    return true
                }
            }
        }

        return false
    }

    // Detect cycle in directed graph using DFS with recursion stack
    func hasCycleDirected() -> Bool {
        guard graphType == .directed else {
            fatalError("This method is for directed graphs")
        }

        var visited = Set<Int>()
        var recStack = Set<Int>()

        func dfsHelper(_ v: Int) -> Bool {
            visited.insert(v)
            recStack.insert(v)

            for neighbor in getNeighbors(v) {
                if !visited.contains(neighbor.vertex) {
                    if dfsHelper(neighbor.vertex) {
                        return true
                    }
                } else if recStack.contains(neighbor.vertex) {
                    return true  // Back edge found
                }
            }

            recStack.remove(v)
            return false
        }

        for v in 0..<numVertices {
            if !visited.contains(v) {
                if dfsHelper(v) {
                    return true
                }
            }
        }

        return false
    }

    // Detect cycle based on graph type
    func hasCycle() -> Bool {
        return graphType == .directed ? hasCycleDirected() : hasCycleUndirected()
    }

    // === GRAPH COLORING ===

    // Graph coloring using greedy algorithm
    // Returns mapping of vertex -> color
    func greedyColoring() -> [Int: Int] {
        var colors: [Int: Int] = [:]

        for v in 0..<numVertices {
            // Get colors of neighbors
            var neighborColors = Set<Int>()
            for neighbor in getNeighbors(v) {
                if let color = colors[neighbor.vertex] {
                    neighborColors.insert(color)
                }
            }

            // Find first available color
            var color = 0
            while neighborColors.contains(color) {
                color += 1
            }

            colors[v] = color
        }

        return colors
    }

    // Get upper bound on chromatic number
    func chromaticNumberUpperBound() -> Int {
        let coloring = greedyColoring()
        guard !coloring.isEmpty else { return 0 }
        return (coloring.values.max() ?? 0) + 1
    }

    // === VISUALIZATION ===

    // Generate ASCII art representation of the graph
    func toASCII(maxWidth: Int = 80) -> String {
        var output = ""

        output += String(repeating: "=", count: maxWidth) + "\n"
        output += "Graph: \(graphType), \(weighted ? "weighted" : "unweighted")\n"
        output += "Representation: \(representation)\n"
        output += "Vertices: \(numVertices), Edges: \(numEdges)\n"
        output += String(repeating: "=", count: maxWidth) + "\n\n"

        switch representation {
        case .adjacencyList:
            output += "Adjacency List:\n"
            for v in 0..<numVertices {
                let neighbors = getNeighbors(v)
                output += "  \(v) -> ["
                output += neighbors.enumerated().map { i, n in
                    let str = weighted ? "\(n.vertex)(\(String(format: "%.1f", n.weight)))" : "\(n.vertex)"
                    return str
                }.joined(separator: ", ")
                output += "]\n"
            }

        case .adjacencyMatrix:
            output += "Adjacency Matrix:\n"
            let displaySize = min(numVertices, 15)

            // Header
            output += "    "
            for i in 0..<displaySize {
                output += String(format: "%4d ", i)
            }
            output += "\n    " + String(repeating: "-", count: 5 * displaySize) + "\n"

            for i in 0..<displaySize {
                output += String(format: "%2d |", i)
                for j in 0..<displaySize {
                    if let weight = adjMatrix[i][j] {
                        output += String(format: "%4.0f ", weight)
                    } else {
                        output += "   . "
                    }
                }
                output += "\n"
            }

            if numVertices > 15 {
                output += "  ... (truncated)\n"
            }

        case .edgeList:
            output += "Edge List:\n"
            let displayLimit = min(edges.count, 50)
            for (i, edge) in edges.prefix(displayLimit).enumerated() {
                if weighted {
                    output += String(format: "  %d: %d -> %d (weight: %.1f)\n",
                                   i, edge.src, edge.dst, edge.weight)
                } else {
                    output += "  \(i): \(edge.src) -> \(edge.dst)\n"
                }
            }
            if edges.count > 50 {
                output += "  ... (\(edges.count - 50) more edges)\n"
            }

        case .csr:
            output += "CSR (Compressed Sparse Row):\n"
            let valLimit = min(csrValues.count, 20)
            output += "  Values: ["
            output += csrValues.prefix(valLimit).map { String(format: "%.1f", $0) }.joined(separator: ", ")
            if csrValues.count > 20 { output += ", ..." }
            output += "]\n"

            let colLimit = min(csrColIndices.count, 20)
            output += "  Col Indices: ["
            output += csrColIndices.prefix(colLimit).map { "\($0)" }.joined(separator: ", ")
            if csrColIndices.count > 20 { output += ", ..." }
            output += "]\n"

            let rowLimit = min(csrRowPtr.count, 20)
            output += "  Row Ptrs: ["
            output += csrRowPtr.prefix(rowLimit).map { "\($0)" }.joined(separator: ", ")
            if csrRowPtr.count > 20 { output += ", ..." }
            output += "]\n"
        }

        output += "\n" + String(repeating: "=", count: maxWidth) + "\n"
        return output
    }
}

// === GRAPH GENERATORS ===

class GraphGenerator {
    // Generate a complete graph with n vertices
    static func completeGraph(n: Int, graphType: GraphType = .undirected,
                            representation: RepresentationType = .adjacencyList) -> Graph {
        let g = Graph(numVertices: n, graphType: graphType, weighted: false,
                     representation: representation)

        if representation == .csr {
            var edges: [Edge] = []
            for i in 0..<n {
                for j in 0..<n where i != j {
                    edges.append(Edge(src: i, dst: j, weight: 1.0))
                }
            }
            g.buildCSR(edges: edges)
        } else {
            for i in 0..<n {
                for j in (i+1)..<n {
                    try? g.addEdge(i, j)
                    if graphType == .directed {
                        try? g.addEdge(j, i)
                    }
                }
            }
        }

        return g
    }

    // Generate a cycle graph with n vertices
    static func cycleGraph(n: Int, graphType: GraphType = .undirected,
                          representation: RepresentationType = .adjacencyList) -> Graph {
        let g = Graph(numVertices: n, graphType: graphType, weighted: false,
                     representation: representation)

        if representation == .csr {
            var edges: [Edge] = []
            for i in 0..<n {
                edges.append(Edge(src: i, dst: (i + 1) % n, weight: 1.0))
                if graphType == .undirected {
                    edges.append(Edge(src: (i + 1) % n, dst: i, weight: 1.0))
                }
            }
            g.buildCSR(edges: edges)
        } else {
            for i in 0..<n {
                try? g.addEdge(i, (i + 1) % n)
            }
        }

        return g
    }

    // Generate random graph with Erdős-Rényi model
    static func randomGraph(n: Int, edgeProbability: Double,
                          graphType: GraphType = .undirected,
                          weighted: Bool = false,
                          representation: RepresentationType = .adjacencyList) -> Graph {
        let g = Graph(numVertices: n, graphType: graphType, weighted: weighted,
                     representation: representation)
        var edgeList: [Edge] = []

        for i in 0..<n {
            let start = graphType == .undirected ? i + 1 : 0
            for j in start..<n where i != j {
                if Double.random(in: 0...1) < edgeProbability {
                    let weight = weighted ? Double.random(in: 1...10) : 1.0
                    edgeList.append(Edge(src: i, dst: j, weight: weight))
                }
            }
        }

        if representation == .csr {
            if graphType == .undirected {
                let reversed = edgeList.map { Edge(src: $0.dst, dst: $0.src, weight: $0.weight) }
                edgeList.append(contentsOf: reversed)
            }
            g.buildCSR(edges: edgeList)
        } else {
            for edge in edgeList {
                try? g.addEdge(edge.src, edge.dst, weight: edge.weight)
            }
        }

        return g
    }

    // Generate a random Directed Acyclic Graph (DAG)
    static func dag(n: Int, edgeProbability: Double,
                   representation: RepresentationType = .adjacencyList) -> Graph {
        let g = Graph(numVertices: n, graphType: .directed, weighted: false,
                     representation: representation)
        var edgeList: [Edge] = []

        for i in 0..<n {
            for j in (i+1)..<n {
                if Double.random(in: 0...1) < edgeProbability {
                    edgeList.append(Edge(src: i, dst: j, weight: 1.0))
                }
            }
        }

        if representation == .csr {
            g.buildCSR(edges: edgeList)
        } else {
            for edge in edgeList {
                try? g.addEdge(edge.src, edge.dst, weight: edge.weight)
            }
        }

        return g
    }
}

// === ERROR HANDLING ===

enum GraphError: Error {
    case vertexOutOfRange(String)
    case invalidOperation(String)
}

// === DEMO AND TESTING ===

func demo() {
    print(String(repeating: "=", count: 80))
    print("GRAPH DATA STRUCTURES AND ALGORITHMS DEMO")
    print(String(repeating: "=", count: 80))
    print()

    // Demo 1: Adjacency List
    print("1. ADJACENCY LIST REPRESENTATION")
    print(String(repeating: "-", count: 80))
    let g1 = Graph(numVertices: 5, graphType: .undirected, weighted: false,
                  representation: .adjacencyList)
    try? g1.addEdge(0, 1)
    try? g1.addEdge(0, 4)
    try? g1.addEdge(1, 2)
    try? g1.addEdge(1, 3)
    try? g1.addEdge(1, 4)
    try? g1.addEdge(2, 3)
    try? g1.addEdge(3, 4)
    print(g1.toASCII())

    // Demo 2: DFS and BFS
    print("2. GRAPH TRAVERSAL")
    print(String(repeating: "-", count: 80))
    print("DFS Recursive from 0: \(g1.dfsRecursive(start: 0))")
    print("DFS Iterative from 0: \(g1.dfsIterative(start: 0))")
    print("BFS from 0: \(g1.bfs(start: 0))")
    print()

    // Demo 3: Connected Components
    print("3. CONNECTED COMPONENTS")
    print(String(repeating: "-", count: 80))
    let g2 = Graph(numVertices: 7, graphType: .undirected)
    try? g2.addEdge(0, 1)
    try? g2.addEdge(1, 2)
    try? g2.addEdge(3, 4)
    try? g2.addEdge(5, 6)
    print("Components: \(g2.findConnectedComponents())")
    print("Is connected: \(g2.isConnected())")
    print()

    // Demo 4: Cycle Detection
    print("4. CYCLE DETECTION")
    print(String(repeating: "-", count: 80))
    print("Graph g1 has cycle: \(g1.hasCycle())")
    let g3 = Graph(numVertices: 3, graphType: .undirected)
    try? g3.addEdge(0, 1)
    try? g3.addEdge(1, 2)
    print("Linear graph has cycle: \(g3.hasCycle())")
    print()

    // Demo 5: Topological Sort
    print("5. TOPOLOGICAL SORTING")
    print(String(repeating: "-", count: 80))
    let dag = GraphGenerator.dag(n: 6, edgeProbability: 0.3)
    print(dag.toASCII())
    print("Topological order: \(dag.topologicalSort() ?? [])")
    print("Topological order (DFS): \(dag.topologicalSortDFS() ?? [])")
    print()

    // Demo 6: Graph Coloring
    print("6. GRAPH COLORING")
    print(String(repeating: "-", count: 80))
    print("Greedy coloring: \(g1.greedyColoring())")
    print("Chromatic number (upper bound): \(g1.chromaticNumberUpperBound())")
    print()

    // Demo 7: Different Representations
    print("7. ADJACENCY MATRIX REPRESENTATION")
    print(String(repeating: "-", count: 80))
    let g4 = Graph(numVertices: 5, graphType: .directed, weighted: true,
                  representation: .adjacencyMatrix)
    try? g4.addEdge(0, 1, weight: 2.5)
    try? g4.addEdge(0, 2, weight: 1.0)
    try? g4.addEdge(1, 3, weight: 3.0)
    try? g4.addEdge(2, 3, weight: 1.5)
    try? g4.addEdge(3, 4, weight: 2.0)
    print(g4.toASCII())

    // Demo 8: Graph Generators
    print("8. GRAPH GENERATORS")
    print(String(repeating: "-", count: 80))
    let complete = GraphGenerator.completeGraph(n: 5)
    print("Complete graph K5:")
    print(complete.toASCII())

    let cycle = GraphGenerator.cycleGraph(n: 6)
    print("Cycle graph C6:")
    print(cycle.toASCII())
}

// Run demo
demo()
