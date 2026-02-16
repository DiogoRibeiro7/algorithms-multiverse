// AlgorithmsMultiverse - Swift Implementation
// A comprehensive collection of algorithms and data structures

// MARK: - Module Exports

// Re-export all public APIs
public typealias AlgorithmsMultiverseSorting = Sorting
public typealias AlgorithmsMultiverseGraphAlgorithms = GraphAlgorithms
public typealias AlgorithmsMultiverseDynamicProgramming = DynamicProgramming
public typealias AlgorithmsMultiverseSearching = Searching
public typealias AlgorithmsMultiverseStringAlgorithms = StringAlgorithms
public typealias AlgorithmsMultiverseNumericalAlgorithms = NumericalAlgorithms
public typealias AlgorithmsMultiverseAdvancedAlgorithms = AdvancedAlgorithms

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
    case searching = "Searching Algorithms"
    case dataStructures = "Data Structures"
    case graphAlgorithms = "Graph Algorithms"
    case dynamicProgramming = "Dynamic Programming"
    case stringAlgorithms = "String Algorithms"
    case numericalAlgorithms = "Numerical Algorithms"
    case advancedAlgorithms = "Advanced Algorithms"

    public var description: String {
        rawValue
    }

    public var algorithms: [String] {
        switch self {
        case .sorting:
            return ["QuickSort", "MergeSort", "HeapSort", "TimSort", "RadixSort", "CountingSort", "IntroSort", "ShellSort"]
        case .searching:
            return ["Binary Search", "Linear Search", "Jump Search", "Interpolation Search", "Exponential Search", "Ternary Search", "Fibonacci Search", "Two-Pointer"]
        case .dataStructures:
            return ["LinkedList", "Stack", "Queue", "PriorityQueue", "BinarySearchTree", "HashTable", "Trie", "Graph", "DisjointSet", "SegmentTree"]
        case .graphAlgorithms:
            return ["BFS", "DFS", "Dijkstra", "A*", "Bellman-Ford", "Floyd-Warshall", "Kruskal", "Prim", "Topological Sort", "Kosaraju"]
        case .dynamicProgramming:
            return ["Fibonacci", "LCS", "LIS", "Edit Distance", "Knapsack", "Coin Change", "Max Subarray", "Matrix Chain", "Palindrome", "Word Break"]
        case .stringAlgorithms:
            return ["KMP", "Rabin-Karp", "Boyer-Moore", "Z-Algorithm", "Manacher", "Longest Palindrome", "Edit Distance", "Anagram Check"]
        case .numericalAlgorithms:
            return ["GCD", "LCM", "Prime Check", "Sieve of Eratosthenes", "Newton-Raphson", "FFT", "Matrix Operations", "Modular Arithmetic"]
        case .advancedAlgorithms:
            return ["Huffman Coding", "LZW", "Bloom Filter", "Skip List", "Convex Hull", "Closest Pair", "Reservoir Sampling"]
        }
    }
}