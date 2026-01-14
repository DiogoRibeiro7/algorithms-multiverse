// AlgorithmsMultiverse - Swift Implementation
// A comprehensive collection of algorithms and data structures

// MARK: - Module Exports

// Re-export all public APIs
public typealias AlgorithmsMultiverseSorting = Sorting
public typealias AlgorithmsMultiverseGraphAlgorithms = GraphAlgorithms
public typealias AlgorithmsMultiverseDynamicProgramming = DynamicProgramming

// MARK: - Version Info

public struct AlgorithmsMultiverse {
    public static let version = "1.0.0"
    public static let author = "Algorithms Multiverse"
    public static let license = "MIT"

    private init() {} // Prevent instantiation
}

// MARK: - Convenience Extensions

extension Array where Element: Comparable {
    /// Quick access to common sorting algorithms
    public enum SortMethod {
        case quick
        case merge
        case heap
        case tim
        case intro
    }

    /// Sort array using specified method
    public func sorted(by method: SortMethod) -> [Element] {
        switch method {
        case .quick:
            return sorted(using: .quickSort)
        case .merge:
            return sorted(using: .mergeSort)
        case .heap:
            return sorted(using: .heapSort)
        case .tim:
            return sorted(using: .timSort)
        case .intro:
            return sorted(using: .introSort)
        }
    }
}

// MARK: - Algorithm Categories

/// Categories of algorithms available in the library
public enum AlgorithmCategory: String, CaseIterable {
    case sorting = "Sorting Algorithms"
    case dataStructures = "Data Structures"
    case graphAlgorithms = "Graph Algorithms"
    case dynamicProgramming = "Dynamic Programming"

    public var description: String {
        rawValue
    }

    public var algorithms: [String] {
        switch self {
        case .sorting:
            return ["QuickSort", "MergeSort", "HeapSort", "TimSort", "RadixSort", "CountingSort"]
        case .dataStructures:
            return ["LinkedList", "Stack", "Queue", "PriorityQueue", "BinarySearchTree", "HashTable", "Trie", "Graph", "DisjointSet", "SegmentTree"]
        case .graphAlgorithms:
            return ["BFS", "DFS", "Dijkstra", "A*", "Bellman-Ford", "Floyd-Warshall", "Kruskal", "Prim", "Topological Sort", "Kosaraju"]
        case .dynamicProgramming:
            return ["Fibonacci", "LCS", "LIS", "Edit Distance", "Knapsack", "Coin Change", "Max Subarray", "Matrix Chain", "Palindrome", "Word Break"]
        }
    }
}