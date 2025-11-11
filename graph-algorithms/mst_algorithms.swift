/**
 * Comprehensive Minimum Spanning Tree (MST) Algorithms
 * =====================================================
 *
 * Implements three classic MST algorithms with various optimizations:
 * 1. Kruskal's Algorithm with Union-Find (path compression + union by rank)
 * 2. Prim's Algorithm with priority queue
 * 3. Borůvka's Algorithm (parallel-friendly)
 *
 * Features:
 * - Support for disconnected graphs (Minimum Spanning Forest)
 * - Swift-optimized implementations
 * - Performance comparison
 *
 * Time Complexities:
 * - Kruskal's: O(E log E) or O(E log V)
 * - Prim's (Binary Heap): O((V+E) log V)
 * - Borůvka's: O(E log V)
 *
 * @author Claude Code
 * @version 2025
 */

import Foundation

// ========================================================================
// UNION-FIND DATA STRUCTURE
// ========================================================================

/// Union-Find (Disjoint Set Union) data structure
///
/// Implements path compression and union by rank for near O(1) operations.
class UnionFind {
    private var parent: [Int]
    private var rank: [Int]
    private var componentCount: Int

    init(_ n: Int) {
        parent = Array(0..<n)
        rank = Array(repeating: 0, count: n)
        componentCount = n
    }

    /// Find the representative (root) of the set containing x
    /// Uses path compression for optimization
    func find(_ x: Int) -> Int {
        if parent[x] != x {
            parent[x] = find(parent[x]) // Path compression
        }
        return parent[x]
    }

    /// Union the sets containing x and y
    /// Uses union by rank for optimization
    func union(_ x: Int, _ y: Int) -> Bool {
        var px = find(x)
        var py = find(y)

        if px == py {
            return false // Already in same set
        }

        // Union by rank
        if rank[px] < rank[py] {
            swap(&px, &py)
        }

        parent[py] = px
        if rank[px] == rank[py] {
            rank[px] += 1
        }

        componentCount -= 1
        return true
    }

    func connected(_ x: Int, _ y: Int) -> Bool {
        return find(x) == find(y)
    }

    func getComponentCount() -> Int {
        return componentCount
    }
}

// ========================================================================
// EDGE STRUCTURE
// ========================================================================

/// Represents a weighted edge in a graph
struct Edge: Comparable {
    let u: Int
    let v: Int
    let weight: Double

    init(_ u: Int, _ v: Int, _ weight: Double) {
        self.u = u
        self.v = v
        self.weight = weight
    }

    static func < (lhs: Edge, rhs: Edge) -> Bool {
        return lhs.weight < rhs.weight
    }

    static func == (lhs: Edge, rhs: Edge) -> Bool {
        return lhs.weight == rhs.weight
    }
}

extension Edge: CustomStringConvertible {
    var description: String {
        return "Edge(\(u), \(v), \(weight))"
    }
}

// ========================================================================
// PRIORITY QUEUE (MIN-HEAP)
// ========================================================================

/// Min-heap priority queue for Prim's algorithm
struct PriorityQueue<T: Comparable> {
    private var heap: [T] = []

    var isEmpty: Bool {
        return heap.isEmpty
    }

    var count: Int {
        return heap.count
    }

    mutating func push(_ element: T) {
        heap.append(element)
        bubbleUp(heap.count - 1)
    }

    mutating func pop() -> T? {
        guard !heap.isEmpty else { return nil }

        if heap.count == 1 {
            return heap.removeLast()
        }

        let min = heap[0]
        heap[0] = heap.removeLast()
        bubbleDown(0)
        return min
    }

    private mutating func bubbleUp(_ index: Int) {
        var child = index
        var parent = (child - 1) / 2

        while child > 0 && heap[child] < heap[parent] {
            heap.swapAt(child, parent)
            child = parent
            parent = (child - 1) / 2
        }
    }

    private mutating func bubbleDown(_ index: Int) {
        var parent = index

        while true {
            let leftChild = 2 * parent + 1
            let rightChild = 2 * parent + 2
            var smallest = parent

            if leftChild < heap.count && heap[leftChild] < heap[smallest] {
                smallest = leftChild
            }

            if rightChild < heap.count && heap[rightChild] < heap[smallest] {
                smallest = rightChild
            }

            if smallest == parent {
                break
            }

            heap.swapAt(parent, smallest)
            parent = smallest
        }
    }
}

// ========================================================================
// MST RESULT
// ========================================================================

/// Result of MST computation
struct MSTResult {
    var mstEdges: [Edge]
    var totalWeight: Double
    var forest: [[Edge]]

    init(mstEdges: [Edge] = [], totalWeight: Double = 0.0, forest: [[Edge]] = []) {
        self.mstEdges = mstEdges
        self.totalWeight = totalWeight
        self.forest = forest
    }
}

// ========================================================================
// MST ALGORITHMS
// ========================================================================

/// Collection of Minimum Spanning Tree algorithms
class MSTAlgorithms {
    private let numVertices: Int
    private let edges: [Edge]
    private var adjList: [[Edge]]

    init(numVertices: Int, edges: [Edge]) {
        self.numVertices = numVertices
        self.edges = edges
        self.adjList = Array(repeating: [], count: numVertices)
        buildAdjacencyList()
    }

    private func buildAdjacencyList() {
        for edge in edges {
            adjList[edge.u].append(edge)
            adjList[edge.v].append(Edge(edge.v, edge.u, edge.weight))
        }
    }

    // ========================================================================
    // KRUSKAL'S ALGORITHM
    // ========================================================================

    /// Kruskal's Algorithm for MST/MSF
    ///
    /// Strategy: Sort edges by weight, add edges that don't create cycles
    /// Uses Union-Find to efficiently detect cycles
    ///
    /// Time Complexity: O(E log E) or O(E log V)
    /// Space Complexity: O(V + E)
    func kruskal(returnForest: Bool = false) -> MSTResult {
        // Sort edges by weight - O(E log E)
        let sortedEdges = edges.sorted()

        let uf = UnionFind(numVertices)
        var result = MSTResult()

        for edge in sortedEdges {
            if uf.union(edge.u, edge.v) {
                result.mstEdges.append(edge)
                result.totalWeight += edge.weight

                // Early termination for connected graph
                if !returnForest && result.mstEdges.count == numVertices - 1 {
                    break
                }
            }
        }

        if returnForest {
            result.forest = buildForest(edges: result.mstEdges)
        }

        return result
    }

    // ========================================================================
    // PRIM'S ALGORITHM
    // ========================================================================

    /// Prim's Algorithm for MST
    ///
    /// Strategy: Grow tree from starting vertex, always add minimum weight edge
    /// that connects tree to non-tree vertex
    ///
    /// Time Complexity: O((V+E) log V)
    /// Space Complexity: O(V + E)
    func prim(start: Int = 0) -> MSTResult {
        var result = MSTResult()
        var visited = Set<Int>([start])
        var pq = PriorityQueue<Edge>()

        // Add edges from start vertex
        for edge in adjList[start] {
            pq.push(edge)
        }

        while !pq.isEmpty && visited.count < numVertices {
            guard let edge = pq.pop() else { break }

            if visited.contains(edge.v) {
                continue
            }

            // Add edge to MST
            visited.insert(edge.v)
            result.mstEdges.append(edge)
            result.totalWeight += edge.weight

            // Add edges from newly added vertex
            for nextEdge in adjList[edge.v] {
                if !visited.contains(nextEdge.v) {
                    pq.push(nextEdge)
                }
            }
        }

        return result
    }

    /// Prim's algorithm using simple array (O(V²) for dense graphs)
    func primSimpleArray(start: Int = 0) -> MSTResult {
        var result = MSTResult()
        var visited = Array(repeating: false, count: numVertices)
        var minWeight = Array(repeating: Double.infinity, count: numVertices)
        var parent = Array(repeating: -1, count: numVertices)

        minWeight[start] = 0

        for _ in 0..<numVertices {
            // Find minimum weight unvisited vertex - O(V)
            var u = -1
            var minVal = Double.infinity
            for v in 0..<numVertices {
                if !visited[v] && minWeight[v] < minVal {
                    minVal = minWeight[v]
                    u = v
                }
            }

            guard u != -1 else { break }

            if minWeight[u] == Double.infinity {
                break // Disconnected graph
            }

            visited[u] = true

            // Add edge to MST (skip first vertex)
            if parent[u] != -1 {
                result.mstEdges.append(Edge(parent[u], u, minWeight[u]))
                result.totalWeight += minWeight[u]
            }

            // Update neighbors
            for edge in adjList[u] {
                let v = edge.v
                if !visited[v] && edge.weight < minWeight[v] {
                    minWeight[v] = edge.weight
                    parent[v] = u
                }
            }
        }

        return result
    }

    // ========================================================================
    // BORŮVKA'S ALGORITHM
    // ========================================================================

    /// Borůvka's (Sollin's) Algorithm for MST
    ///
    /// Strategy: In each phase, find minimum weight edge for each component,
    /// add all such edges simultaneously (parallel-friendly)
    ///
    /// Time Complexity: O(E log V)
    /// Space Complexity: O(V + E)
    func boruvka() -> MSTResult {
        let uf = UnionFind(numVertices)
        var result = MSTResult()
        var numComponents = numVertices

        while numComponents > 1 {
            var cheapest = Array(repeating: -1, count: numVertices)

            // Find cheapest edge from each component
            for (i, edge) in edges.enumerated() {
                let uRoot = uf.find(edge.u)
                let vRoot = uf.find(edge.v)

                if uRoot == vRoot {
                    continue // Same component
                }

                // Check if this is cheapest for component of u
                if cheapest[uRoot] == -1 || edge.weight < edges[cheapest[uRoot]].weight {
                    cheapest[uRoot] = i
                }

                // Check if this is cheapest for component of v
                if cheapest[vRoot] == -1 || edge.weight < edges[cheapest[vRoot]].weight {
                    cheapest[vRoot] = i
                }
            }

            // Add all cheapest edges
            var addedAny = false
            for i in 0..<numVertices {
                if cheapest[i] != -1 {
                    let edge = edges[cheapest[i]]
                    if uf.union(edge.u, edge.v) {
                        result.mstEdges.append(edge)
                        result.totalWeight += edge.weight
                        numComponents -= 1
                        addedAny = true
                    }
                }
            }

            if !addedAny {
                break // Disconnected graph or done
            }
        }

        return result
    }

    // ========================================================================
    // UTILITY METHODS
    // ========================================================================

    private func buildForest(edges: [Edge]) -> [[Edge]] {
        guard !edges.isEmpty else { return [] }

        let uf = UnionFind(numVertices)
        for edge in edges {
            _ = uf.union(edge.u, edge.v)
        }

        var componentEdges: [Int: [Edge]] = [:]
        for edge in edges {
            let root = uf.find(edge.u)
            componentEdges[root, default: []].append(edge)
        }

        return Array(componentEdges.values)
    }

    /// Find Minimum Spanning Forest for potentially disconnected graph
    func minimumSpanningForest(algorithm: String = "kruskal") -> MSTResult {
        switch algorithm {
        case "kruskal":
            return kruskal(returnForest: true)
        case "prim":
            var visitedGlobal = Set<Int>()
            var result = MSTResult()

            for start in 0..<numVertices {
                if !visitedGlobal.contains(start) {
                    let tree = prim(start: start)

                    // Mark vertices in this tree as visited
                    for edge in tree.mstEdges {
                        visitedGlobal.insert(edge.u)
                        visitedGlobal.insert(edge.v)
                    }

                    if !tree.mstEdges.isEmpty {
                        result.forest.append(tree.mstEdges)
                        result.totalWeight += tree.totalWeight
                        result.mstEdges.append(contentsOf: tree.mstEdges)
                    }
                }
            }

            return result
        case "boruvka":
            var result = boruvka()
            result.forest = buildForest(edges: result.mstEdges)
            return result
        default:
            fatalError("Unknown algorithm: \(algorithm)")
        }
    }

    /// Compare performance of all MST algorithms
    func compareAlgorithms(numRuns: Int = 10) -> [String: [String: Double]] {
        var results: [String: [String: Double]] = [:]

        // Kruskal's
        var kruskalTimes: [Double] = []
        var kResult: MSTResult!
        for _ in 0..<numRuns {
            let start = Date()
            kResult = kruskal()
            kruskalTimes.append(Date().timeIntervalSince(start) * 1000)
        }

        results["kruskal"] = [
            "meanTime": kruskalTimes.reduce(0, +) / Double(kruskalTimes.count),
            "minTime": kruskalTimes.min() ?? 0,
            "maxTime": kruskalTimes.max() ?? 0,
            "weight": kResult.totalWeight,
            "numEdges": Double(kResult.mstEdges.count)
        ]

        // Prim's
        var primTimes: [Double] = []
        var pResult: MSTResult!
        for _ in 0..<numRuns {
            let start = Date()
            pResult = prim()
            primTimes.append(Date().timeIntervalSince(start) * 1000)
        }

        results["prim"] = [
            "meanTime": primTimes.reduce(0, +) / Double(primTimes.count),
            "minTime": primTimes.min() ?? 0,
            "maxTime": primTimes.max() ?? 0,
            "weight": pResult.totalWeight,
            "numEdges": Double(pResult.mstEdges.count)
        ]

        // Borůvka's
        var boruvkaTimes: [Double] = []
        var bResult: MSTResult!
        for _ in 0..<numRuns {
            let start = Date()
            bResult = boruvka()
            boruvkaTimes.append(Date().timeIntervalSince(start) * 1000)
        }

        results["boruvka"] = [
            "meanTime": boruvkaTimes.reduce(0, +) / Double(boruvkaTimes.count),
            "minTime": boruvkaTimes.min() ?? 0,
            "maxTime": boruvkaTimes.max() ?? 0,
            "weight": bResult.totalWeight,
            "numEdges": Double(bResult.mstEdges.count)
        ]

        return results
    }
}

// ========================================================================
// DEMO
// ========================================================================

func demoMSTAlgorithms() {
    print(String(repeating: "=", count: 80))
    print("MINIMUM SPANNING TREE ALGORITHMS DEMO")
    print(String(repeating: "=", count: 80))
    print()

    let edges = [
        Edge(0, 1, 4),
        Edge(0, 7, 8),
        Edge(1, 2, 8),
        Edge(1, 7, 11),
        Edge(2, 3, 7),
        Edge(2, 5, 4),
        Edge(2, 8, 2),
        Edge(3, 4, 9),
        Edge(3, 5, 14),
        Edge(4, 5, 10),
        Edge(5, 6, 2),
        Edge(6, 7, 1),
        Edge(6, 8, 6),
        Edge(7, 8, 7)
    ]

    let mst = MSTAlgorithms(numVertices: 9, edges: edges)

    // Kruskal's
    print("1. KRUSKAL'S ALGORITHM")
    print(String(repeating: "-", count: 80))
    let kResult = mst.kruskal()
    print("MST Weight: \(kResult.totalWeight)")
    print("Edges: ", terminator: "")
    for e in kResult.mstEdges {
        print("(\(e.u),\(e.v),\(Int(e.weight))) ", terminator: "")
    }
    print("\n")

    // Prim's
    print("2. PRIM'S ALGORITHM")
    print(String(repeating: "-", count: 80))
    let pResult = mst.prim()
    print("MST Weight: \(pResult.totalWeight)")
    print("Edges: ", terminator: "")
    for e in pResult.mstEdges {
        print("(\(e.u),\(e.v),\(Int(e.weight))) ", terminator: "")
    }
    print("\n")

    // Borůvka's
    print("3. BORŮVKA'S ALGORITHM")
    print(String(repeating: "-", count: 80))
    let bResult = mst.boruvka()
    print("MST Weight: \(bResult.totalWeight)")
    print("Edges: ", terminator: "")
    for e in bResult.mstEdges {
        print("(\(e.u),\(e.v),\(Int(e.weight))) ", terminator: "")
    }
    print("\n")

    // Performance
    print("4. PERFORMANCE COMPARISON")
    print(String(repeating: "-", count: 80))
    let results = mst.compareAlgorithms(numRuns: 100)

    for (algo, metrics) in results {
        print("\n\(algo.uppercased())")
        print(String(format: "  Mean time: %.4f ms", metrics["meanTime"]!))
        print(String(format: "  Min time:  %.4f ms", metrics["minTime"]!))
        print(String(format: "  Max time:  %.4f ms", metrics["maxTime"]!))
        print(String(format: "  Weight:    %.2f", metrics["weight"]!))
    }
    print()

    // Disconnected graph
    print("5. MINIMUM SPANNING FOREST (Disconnected Graph)")
    print(String(repeating: "-", count: 80))
    let disconnectedEdges = [
        Edge(0, 1, 1),
        Edge(1, 2, 2),
        Edge(3, 4, 3),
        Edge(4, 5, 4)
    ]

    let mstForest = MSTAlgorithms(numVertices: 6, edges: disconnectedEdges)
    let forestResult = mstForest.minimumSpanningForest()

    print("Number of trees: \(forestResult.forest.count)")
    print("Total weight: \(forestResult.totalWeight)")
    for (i, tree) in forestResult.forest.enumerated() {
        print("\nTree \(i + 1):")
        print("  Edges: ", terminator: "")
        for e in tree {
            print("(\(e.u),\(e.v),\(Int(e.weight))) ", terminator: "")
        }
        print()
    }
}

// Run demo
demoMSTAlgorithms()
