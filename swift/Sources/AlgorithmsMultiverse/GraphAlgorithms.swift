import Foundation
import Dispatch

// MARK: - Graph Algorithms

public struct GraphAlgorithms {

    // MARK: - Breadth-First Search

    /// BFS traversal from start vertex
    /// - Complexity: O(V + E)
    public static func bfs<T: Hashable>(
        graph: Graph<T>,
        start: T
    ) -> [T] {
        var visited: Set<T> = []
        var queue: Queue<T> = Queue()
        var result: [T] = []

        queue.enqueue(start)
        visited.insert(start)

        while let vertex = queue.dequeue() {
            result.append(vertex)

            for neighbor in graph.neighbors(of: vertex) {
                if !visited.contains(neighbor) {
                    visited.insert(neighbor)
                    queue.enqueue(neighbor)
                }
            }
        }

        return result
    }

    /// Find shortest path using BFS (unweighted graph)
    public static func shortestPath<T: Hashable>(
        graph: Graph<T>,
        from start: T,
        to end: T
    ) -> [T]? {
        var visited: Set<T> = []
        var queue: Queue<(vertex: T, path: [T])> = Queue()

        queue.enqueue((start, [start]))
        visited.insert(start)

        while let (vertex, path) = queue.dequeue() {
            if vertex == end {
                return path
            }

            for neighbor in graph.neighbors(of: vertex) {
                if !visited.contains(neighbor) {
                    visited.insert(neighbor)
                    queue.enqueue((neighbor, path + [neighbor]))
                }
            }
        }

        return nil
    }

    // MARK: - Depth-First Search

    /// DFS traversal (recursive)
    /// - Complexity: O(V + E)
    public static func dfs<T: Hashable>(
        graph: Graph<T>,
        start: T
    ) -> [T] {
        var visited: Set<T> = []
        var result: [T] = []

        dfsHelper(graph: graph, vertex: start, visited: &visited, result: &result)
        return result
    }

    private static func dfsHelper<T: Hashable>(
        graph: Graph<T>,
        vertex: T,
        visited: inout Set<T>,
        result: inout [T]
    ) {
        visited.insert(vertex)
        result.append(vertex)

        for neighbor in graph.neighbors(of: vertex) {
            if !visited.contains(neighbor) {
                dfsHelper(graph: graph, vertex: neighbor, visited: &visited, result: &result)
            }
        }
    }

    /// DFS traversal (iterative)
    public static func dfsIterative<T: Hashable>(
        graph: Graph<T>,
        start: T
    ) -> [T] {
        var visited: Set<T> = []
        var stack: Stack<T> = Stack()
        var result: [T] = []

        stack.push(start)

        while let vertex = stack.pop() {
            if !visited.contains(vertex) {
                visited.insert(vertex)
                result.append(vertex)

                for neighbor in graph.neighbors(of: vertex) {
                    if !visited.contains(neighbor) {
                        stack.push(neighbor)
                    }
                }
            }
        }

        return result
    }

    // MARK: - Dijkstra's Algorithm

    /// Dijkstra's shortest path algorithm
    /// - Complexity: O((V + E) log V) with binary heap
    public static func dijkstra<T: Hashable>(
        graph: WeightedGraph<T>,
        start: T
    ) -> [T: Double] {
        var distances: [T: Double] = [:]
        var visited: Set<T> = []
        var pq = PriorityQueue<(vertex: T, distance: Double)> { $0.distance < $1.distance }

        // Initialize distances
        for vertex in graph.vertices {
            distances[vertex] = vertex == start ? 0 : .infinity
        }

        pq.enqueue((start, 0))

        while let (current, currentDistance) = pq.dequeue() {
            if visited.contains(current) { continue }
            visited.insert(current)

            for (neighbor, weight) in graph.edges(from: current) {
                let newDistance = currentDistance + weight

                if newDistance < distances[neighbor]! {
                    distances[neighbor] = newDistance
                    pq.enqueue((neighbor, newDistance))
                }
            }
        }

        return distances
    }

    /// Dijkstra with path reconstruction
    public static func dijkstraWithPath<T: Hashable>(
        graph: WeightedGraph<T>,
        start: T,
        end: T
    ) -> (distance: Double, path: [T])? {
        var distances: [T: Double] = [:]
        var previous: [T: T] = [:]
        var visited: Set<T> = []
        var pq = PriorityQueue<(vertex: T, distance: Double)> { $0.distance < $1.distance }

        for vertex in graph.vertices {
            distances[vertex] = vertex == start ? 0 : .infinity
        }

        pq.enqueue((start, 0))

        while let (current, currentDistance) = pq.dequeue() {
            if visited.contains(current) { continue }
            visited.insert(current)

            if current == end { break }

            for (neighbor, weight) in graph.edges(from: current) {
                let newDistance = currentDistance + weight

                if newDistance < distances[neighbor]! {
                    distances[neighbor] = newDistance
                    previous[neighbor] = current
                    pq.enqueue((neighbor, newDistance))
                }
            }
        }

        // Reconstruct path
        guard distances[end]! < .infinity else { return nil }

        var path: [T] = []
        var current: T? = end

        while let vertex = current {
            path.append(vertex)
            current = previous[vertex]
        }

        path.reverse()
        return (distances[end]!, path)
    }

    // MARK: - A* Algorithm

    /// A* pathfinding algorithm
    public static func aStar<T: Hashable>(
        graph: WeightedGraph<T>,
        start: T,
        goal: T,
        heuristic: (T, T) -> Double
    ) -> [T]? {
        var gScore: [T: Double] = [start: 0]
        var fScore: [T: Double] = [start: heuristic(start, goal)]
        var cameFrom: [T: T] = [:]
        var openSet = PriorityQueue<(vertex: T, fScore: Double)> { $0.fScore < $1.fScore }
        var inOpenSet: Set<T> = [start]

        openSet.enqueue((start, fScore[start]!))

        while let (current, _) = openSet.dequeue() {
            inOpenSet.remove(current)

            if current == goal {
                // Reconstruct path
                var path: [T] = [current]
                var node = current

                while let prev = cameFrom[node] {
                    path.append(prev)
                    node = prev
                }

                return path.reversed()
            }

            for (neighbor, weight) in graph.edges(from: current) {
                let tentativeGScore = (gScore[current] ?? .infinity) + weight

                if tentativeGScore < (gScore[neighbor] ?? .infinity) {
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentativeGScore
                    fScore[neighbor] = tentativeGScore + heuristic(neighbor, goal)

                    if !inOpenSet.contains(neighbor) {
                        openSet.enqueue((neighbor, fScore[neighbor]!))
                        inOpenSet.insert(neighbor)
                    }
                }
            }
        }

        return nil
    }

    // MARK: - Bellman-Ford Algorithm

    /// Bellman-Ford shortest path (handles negative weights)
    /// - Complexity: O(VE)
    public static func bellmanFord<T: Hashable>(
        edges: [(from: T, to: T, weight: Double)],
        vertices: Set<T>,
        start: T
    ) -> (distances: [T: Double], hasNegativeCycle: Bool) {
        var distances: [T: Double] = [:]

        // Initialize distances
        for vertex in vertices {
            distances[vertex] = vertex == start ? 0 : .infinity
        }

        // Relax edges V-1 times
        for _ in 0..<vertices.count - 1 {
            for edge in edges {
                if distances[edge.from]! != .infinity {
                    let newDistance = distances[edge.from]! + edge.weight
                    if newDistance < distances[edge.to]! {
                        distances[edge.to] = newDistance
                    }
                }
            }
        }

        // Check for negative cycles
        for edge in edges {
            if distances[edge.from]! != .infinity {
                let newDistance = distances[edge.from]! + edge.weight
                if newDistance < distances[edge.to]! {
                    return (distances, true)
                }
            }
        }

        return (distances, false)
    }

    // MARK: - Floyd-Warshall Algorithm

    /// Floyd-Warshall all pairs shortest paths
    /// - Complexity: O(V³)
    public static func floydWarshall<T: Hashable>(
        graph: WeightedGraph<T>
    ) -> [T: [T: Double]] {
        var distances: [T: [T: Double]] = [:]
        let vertices = Array(graph.vertices)

        // Initialize distances
        for i in vertices {
            distances[i] = [:]
            for j in vertices {
                if i == j {
                    distances[i]![j] = 0
                } else {
                    distances[i]![j] = graph.weight(from: i, to: j) ?? .infinity
                }
            }
        }

        // Floyd-Warshall algorithm
        for k in vertices {
            for i in vertices {
                for j in vertices {
                    let throughK = distances[i]![k]! + distances[k]![j]!
                    if throughK < distances[i]![j]! {
                        distances[i]![j] = throughK
                    }
                }
            }
        }

        return distances
    }

    // MARK: - Minimum Spanning Tree

    /// Kruskal's MST algorithm
    /// - Complexity: O(E log E)
    public static func kruskal<T: Hashable>(
        edges: [(from: T, to: T, weight: Double)],
        vertices: Set<T>
    ) -> (edges: [(from: T, to: T, weight: Double)], totalWeight: Double) {
        let sortedEdges = edges.sorted { $0.weight < $1.weight }
        let disjointSet = DisjointSet<T>()
        var mst: [(from: T, to: T, weight: Double)] = []
        var totalWeight: Double = 0

        for edge in sortedEdges {
            if !disjointSet.isConnected(edge.from, edge.to) {
                disjointSet.union(edge.from, edge.to)
                mst.append(edge)
                totalWeight += edge.weight

                if mst.count == vertices.count - 1 {
                    break
                }
            }
        }

        return (mst, totalWeight)
    }

    /// Prim's MST algorithm
    /// - Complexity: O((V + E) log V) with binary heap
    public static func prim<T: Hashable>(
        graph: WeightedGraph<T>,
        start: T
    ) -> (edges: [(from: T, to: T, weight: Double)], totalWeight: Double) {
        var visited: Set<T> = []
        var mst: [(from: T, to: T, weight: Double)] = []
        var totalWeight: Double = 0
        var pq = PriorityQueue<(from: T, to: T, weight: Double)> { $0.weight < $1.weight }

        visited.insert(start)

        // Add all edges from start vertex
        for (neighbor, weight) in graph.edges(from: start) {
            pq.enqueue((start, neighbor, weight))
        }

        while let edge = pq.dequeue() {
            if visited.contains(edge.to) { continue }

            visited.insert(edge.to)
            mst.append(edge)
            totalWeight += edge.weight

            // Add all edges from newly visited vertex
            for (neighbor, weight) in graph.edges(from: edge.to) {
                if !visited.contains(neighbor) {
                    pq.enqueue((edge.to, neighbor, weight))
                }
            }
        }

        return (mst, totalWeight)
    }

    // MARK: - Topological Sort

    /// Topological sort using DFS
    /// - Complexity: O(V + E)
    public static func topologicalSort<T: Hashable>(
        graph: Graph<T>
    ) -> [T]? {
        guard graph.isDirected else { return nil }

        var visited: Set<T> = []
        var stack: [T] = []
        var visiting: Set<T> = []  // For cycle detection

        func dfs(_ vertex: T) -> Bool {
            if visiting.contains(vertex) {
                return false  // Cycle detected
            }
            if visited.contains(vertex) {
                return true
            }

            visiting.insert(vertex)

            for neighbor in graph.neighbors(of: vertex) {
                if !dfs(neighbor) {
                    return false
                }
            }

            visiting.remove(vertex)
            visited.insert(vertex)
            stack.append(vertex)

            return true
        }

        for vertex in graph.vertices {
            if !visited.contains(vertex) {
                if !dfs(vertex) {
                    return nil  // Graph has cycle
                }
            }
        }

        return stack.reversed()
    }

    /// Topological sort using Kahn's algorithm (BFS)
    public static func kahnsAlgorithm<T: Hashable>(
        graph: Graph<T>
    ) -> [T]? {
        guard graph.isDirected else { return nil }

        var inDegree: [T: Int] = [:]
        var queue: Queue<T> = Queue()
        var result: [T] = []

        // Calculate in-degrees
        for vertex in graph.vertices {
            inDegree[vertex] = graph.inDegree(of: vertex)
            if inDegree[vertex] == 0 {
                queue.enqueue(vertex)
            }
        }

        while let vertex = queue.dequeue() {
            result.append(vertex)

            for neighbor in graph.neighbors(of: vertex) {
                inDegree[neighbor]! -= 1
                if inDegree[neighbor] == 0 {
                    queue.enqueue(neighbor)
                }
            }
        }

        return result.count == graph.vertices.count ? result : nil
    }

    // MARK: - Strongly Connected Components

    /// Kosaraju's algorithm for SCCs
    /// - Complexity: O(V + E)
    public static func kosaraju<T: Hashable>(
        graph: Graph<T>
    ) -> [[T]] {
        guard graph.isDirected else { return [Array(graph.vertices)] }

        var visited: Set<T> = []
        var stack: [T] = []

        // First DFS to fill stack
        func dfs1(_ vertex: T) {
            visited.insert(vertex)
            for neighbor in graph.neighbors(of: vertex) {
                if !visited.contains(neighbor) {
                    dfs1(neighbor)
                }
            }
            stack.append(vertex)
        }

        // Create reversed graph
        let reversedGraph = Graph<T>(isDirected: true)
        for vertex in graph.vertices {
            reversedGraph.addVertex(vertex)
        }
        for vertex in graph.vertices {
            for neighbor in graph.neighbors(of: vertex) {
                reversedGraph.addEdge(from: neighbor, to: vertex)
            }
        }

        // First pass
        for vertex in graph.vertices {
            if !visited.contains(vertex) {
                dfs1(vertex)
            }
        }

        // Second DFS on reversed graph
        visited.removeAll()
        var components: [[T]] = []

        func dfs2(_ vertex: T, component: inout [T]) {
            visited.insert(vertex)
            component.append(vertex)
            for neighbor in reversedGraph.neighbors(of: vertex) {
                if !visited.contains(neighbor) {
                    dfs2(neighbor, component: &component)
                }
            }
        }

        // Process vertices in reverse finishing order
        while let vertex = stack.popLast() {
            if !visited.contains(vertex) {
                var component: [T] = []
                dfs2(vertex, component: &component)
                components.append(component)
            }
        }

        return components
    }

    // MARK: - Cycle Detection

    /// Detect cycle in directed graph
    public static func hasCycleDirected<T: Hashable>(
        graph: Graph<T>
    ) -> Bool {
        var visited: Set<T> = []
        var recursionStack: Set<T> = []

        func dfs(_ vertex: T) -> Bool {
            visited.insert(vertex)
            recursionStack.insert(vertex)

            for neighbor in graph.neighbors(of: vertex) {
                if !visited.contains(neighbor) {
                    if dfs(neighbor) {
                        return true
                    }
                } else if recursionStack.contains(neighbor) {
                    return true
                }
            }

            recursionStack.remove(vertex)
            return false
        }

        for vertex in graph.vertices {
            if !visited.contains(vertex) {
                if dfs(vertex) {
                    return true
                }
            }
        }

        return false
    }

    /// Detect cycle in undirected graph
    public static func hasCycleUndirected<T: Hashable>(
        graph: Graph<T>
    ) -> Bool {
        guard !graph.isDirected else { return hasCycleDirected(graph: graph) }

        var visited: Set<T> = []

        func dfs(_ vertex: T, parent: T?) -> Bool {
            visited.insert(vertex)

            for neighbor in graph.neighbors(of: vertex) {
                if !visited.contains(neighbor) {
                    if dfs(neighbor, parent: vertex) {
                        return true
                    }
                } else if neighbor != parent {
                    return true
                }
            }

            return false
        }

        for vertex in graph.vertices {
            if !visited.contains(vertex) {
                if dfs(vertex, parent: nil) {
                    return true
                }
            }
        }

        return false
    }

    // MARK: - Bipartite Check

    /// Check if graph is bipartite
    public static func isBipartite<T: Hashable>(
        graph: Graph<T>
    ) -> (isBipartite: Bool, coloring: [T: Int]?) {
        var color: [T: Int] = [:]
        var queue: Queue<T> = Queue()

        for start in graph.vertices {
            if color[start] != nil { continue }

            queue.enqueue(start)
            color[start] = 0

            while let vertex = queue.dequeue() {
                let currentColor = color[vertex]!

                for neighbor in graph.neighbors(of: vertex) {
                    if let neighborColor = color[neighbor] {
                        if neighborColor == currentColor {
                            return (false, nil)
                        }
                    } else {
                        color[neighbor] = 1 - currentColor
                        queue.enqueue(neighbor)
                    }
                }
            }
        }

        return (true, color)
    }

    // MARK: - Parallel Algorithms

    /// Parallel BFS using Grand Central Dispatch
    @available(iOS 13.0, macOS 10.15, *)
    public static func parallelBFS<T: Hashable>(
        graph: Graph<T>,
        start: T
    ) async -> [T] {
        var visited = Set<T>()
        var currentLevel = [start]
        var result = [T]()

        visited.insert(start)
        result.append(start)

        while !currentLevel.isEmpty {
            let nextLevel = await withTaskGroup(of: [T].self) { group in
                for vertex in currentLevel {
                    group.addTask {
                        var neighbors: [T] = []
                        for neighbor in graph.neighbors(of: vertex) {
                            neighbors.append(neighbor)
                        }
                        return neighbors
                    }
                }

                var allNeighbors: [T] = []
                for await neighbors in group {
                    allNeighbors.append(contentsOf: neighbors)
                }

                return allNeighbors.filter { !visited.contains($0) }
            }

            for vertex in nextLevel {
                visited.insert(vertex)
                result.append(vertex)
            }

            currentLevel = nextLevel
        }

        return result
    }
}

// MARK: - Weighted Graph

/// Weighted graph for algorithms requiring edge weights
public class WeightedGraph<T: Hashable> {
    private var adjacencyList: [T: [(vertex: T, weight: Double)]] = [:]
    public var isDirected: Bool

    public init(isDirected: Bool = false) {
        self.isDirected = isDirected
    }

    public var vertices: Set<T> {
        Set(adjacencyList.keys)
    }

    public func addVertex(_ vertex: T) {
        if adjacencyList[vertex] == nil {
            adjacencyList[vertex] = []
        }
    }

    public func addEdge(from: T, to: T, weight: Double) {
        addVertex(from)
        addVertex(to)

        adjacencyList[from]?.append((to, weight))
        if !isDirected {
            adjacencyList[to]?.append((from, weight))
        }
    }

    public func edges(from vertex: T) -> [(T, Double)] {
        adjacencyList[vertex] ?? []
    }

    public func weight(from: T, to: T) -> Double? {
        adjacencyList[from]?.first(where: { $0.vertex == to })?.weight
    }
}

// MARK: - Priority Queue with Custom Comparator

/// Priority queue that accepts custom comparator
public struct PriorityQueue<T> {
    private var heap: [T] = []
    private let comparator: (T, T) -> Bool

    public init(comparator: @escaping (T, T) -> Bool) {
        self.comparator = comparator
    }

    public var isEmpty: Bool { heap.isEmpty }
    public var count: Int { heap.count }

    public mutating func enqueue(_ element: T) {
        heap.append(element)
        siftUp(from: heap.count - 1)
    }

    @discardableResult
    public mutating func dequeue() -> T? {
        guard !heap.isEmpty else { return nil }

        if heap.count == 1 {
            return heap.removeFirst()
        }

        let value = heap[0]
        heap[0] = heap.removeLast()
        siftDown(from: 0)

        return value
    }

    private mutating func siftUp(from index: Int) {
        var child = index
        var parent = parentIndex(of: child)

        while child > 0 && comparator(heap[child], heap[parent]) {
            heap.swapAt(child, parent)
            child = parent
            parent = parentIndex(of: child)
        }
    }

    private mutating func siftDown(from index: Int) {
        var parent = index

        while true {
            let left = leftChildIndex(of: parent)
            let right = rightChildIndex(of: parent)
            var candidate = parent

            if left < heap.count && comparator(heap[left], heap[candidate]) {
                candidate = left
            }
            if right < heap.count && comparator(heap[right], heap[candidate]) {
                candidate = right
            }
            if candidate == parent {
                return
            }

            heap.swapAt(parent, candidate)
            parent = candidate
        }
    }

    private func parentIndex(of index: Int) -> Int {
        (index - 1) / 2
    }

    private func leftChildIndex(of index: Int) -> Int {
        2 * index + 1
    }

    private func rightChildIndex(of index: Int) -> Int {
        2 * index + 2
    }
}