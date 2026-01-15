// Searching Algorithms - Swift Implementation
// Comprehensive collection of search algorithms with iOS optimizations

import Foundation

/// Namespace for searching algorithms
public enum Searching {

    // MARK: - Binary Search Variants

    /// Standard binary search for sorted arrays
    /// - Parameters:
    ///   - array: Sorted array to search
    ///   - target: Element to find
    /// - Returns: Index of target or nil if not found
    /// - Complexity: O(log n) time, O(1) space
    public static func binarySearch<T: Comparable>(_ array: [T], target: T) -> Int? {
        var left = 0
        var right = array.count - 1

        while left <= right {
            let mid = left + (right - left) / 2

            if array[mid] == target {
                return mid
            } else if array[mid] < target {
                left = mid + 1
            } else {
                right = mid - 1
            }
        }

        return nil
    }

    /// Binary search with custom comparator
    public static func binarySearch<T>(
        _ array: [T],
        target: T,
        comparator: (T, T) -> ComparisonResult
    ) -> Int? {
        var left = 0
        var right = array.count - 1

        while left <= right {
            let mid = left + (right - left) / 2
            let result = comparator(array[mid], target)

            if result == .orderedSame {
                return mid
            } else if result == .orderedAscending {
                left = mid + 1
            } else {
                right = mid - 1
            }
        }

        return nil
    }

    /// Find first occurrence of target in sorted array
    /// - Complexity: O(log n) time, O(1) space
    public static func lowerBound<T: Comparable>(_ array: [T], target: T) -> Int {
        var left = 0
        var right = array.count

        while left < right {
            let mid = left + (right - left) / 2

            if array[mid] < target {
                left = mid + 1
            } else {
                right = mid
            }
        }

        return left
    }

    /// Find first position where target could be inserted
    /// - Complexity: O(log n) time, O(1) space
    public static func upperBound<T: Comparable>(_ array: [T], target: T) -> Int {
        var left = 0
        var right = array.count

        while left < right {
            let mid = left + (right - left) / 2

            if array[mid] <= target {
                left = mid + 1
            } else {
                right = mid
            }
        }

        return left
    }

    /// Count occurrences of target in sorted array
    /// - Complexity: O(log n) time, O(1) space
    public static func countOccurrences<T: Comparable>(_ array: [T], target: T) -> Int {
        let lower = lowerBound(array, target: target)

        if lower == array.count || array[lower] != target {
            return 0
        }

        let upper = upperBound(array, target: target)
        return upper - lower
    }

    // MARK: - Linear Search Variants

    /// Standard linear search
    /// - Complexity: O(n) time, O(1) space
    public static func linearSearch<T: Equatable>(_ array: [T], target: T) -> Int? {
        for (index, element) in array.enumerated() {
            if element == target {
                return index
            }
        }
        return nil
    }

    /// Find all occurrences of target
    /// - Complexity: O(n) time, O(k) space where k is number of occurrences
    public static func findAll<T: Equatable>(_ array: [T], target: T) -> [Int] {
        return array.enumerated().compactMap { index, element in
            element == target ? index : nil
        }
    }

    /// Sentinel linear search (faster for arrays that can be modified)
    /// - Complexity: O(n) time, O(1) space
    public static func sentinelSearch<T: Equatable>(_ array: inout [T], target: T) -> Int? {
        let lastElement = array.last
        array[array.count - 1] = target

        var i = 0
        while array[i] != target {
            i += 1
        }

        // Restore original value
        if let last = lastElement {
            array[array.count - 1] = last
        }

        if i < array.count - 1 || lastElement == target {
            return i
        }

        return nil
    }

    // MARK: - Advanced Search Algorithms

    /// Jump search for sorted arrays
    /// - Complexity: O(√n) time, O(1) space
    public static func jumpSearch<T: Comparable>(_ array: [T], target: T) -> Int? {
        let n = array.count
        let step = Int(sqrt(Double(n)))

        var prev = 0
        var current = 0

        // Jump to find block containing target
        while current < n && array[min(step, n) - 1] < target {
            prev = current
            current += step
            if prev >= n {
                return nil
            }
        }

        // Linear search in block
        while array[prev] < target {
            prev += 1
            if prev == min(current, n) {
                return nil
            }
        }

        if array[prev] == target {
            return prev
        }

        return nil
    }

    /// Interpolation search for uniformly distributed sorted arrays
    /// - Complexity: O(log log n) average, O(n) worst case
    public static func interpolationSearch(_ array: [Int], target: Int) -> Int? {
        var low = 0
        var high = array.count - 1

        while low <= high && target >= array[low] && target <= array[high] {
            if low == high {
                return array[low] == target ? low : nil
            }

            // Interpolation formula
            let pos = low + ((target - array[low]) * (high - low)) / (array[high] - array[low])

            if array[pos] == target {
                return pos
            } else if array[pos] < target {
                low = pos + 1
            } else {
                high = pos - 1
            }
        }

        return nil
    }

    /// Exponential search for unbounded arrays
    /// - Complexity: O(log n) time, O(1) space
    public static func exponentialSearch<T: Comparable>(_ array: [T], target: T) -> Int? {
        if array.isEmpty {
            return nil
        }

        if array[0] == target {
            return 0
        }

        // Find range for binary search
        var bound = 1
        while bound < array.count && array[bound] <= target {
            bound *= 2
        }

        // Binary search in found range
        let left = bound / 2
        let right = min(bound, array.count - 1)
        let subArray = Array(array[left...right])

        if let index = binarySearch(subArray, target: target) {
            return left + index
        }

        return nil
    }

    /// Ternary search for sorted arrays
    /// - Complexity: O(log₃ n) time, O(1) space
    public static func ternarySearch<T: Comparable>(_ array: [T], target: T) -> Int? {
        var left = 0
        var right = array.count - 1

        while left <= right {
            let mid1 = left + (right - left) / 3
            let mid2 = right - (right - left) / 3

            if array[mid1] == target {
                return mid1
            }
            if array[mid2] == target {
                return mid2
            }

            if target < array[mid1] {
                right = mid1 - 1
            } else if target > array[mid2] {
                left = mid2 + 1
            } else {
                left = mid1 + 1
                right = mid2 - 1
            }
        }

        return nil
    }

    /// Fibonacci search for sorted arrays
    /// - Complexity: O(log n) time, O(1) space
    public static func fibonacciSearch<T: Comparable>(_ array: [T], target: T) -> Int? {
        let n = array.count

        // Initialize Fibonacci numbers
        var fib2 = 0  // (m-2)th Fibonacci number
        var fib1 = 1  // (m-1)th Fibonacci number
        var fibM = fib2 + fib1  // mth Fibonacci number

        // Find smallest Fibonacci number >= n
        while fibM < n {
            fib2 = fib1
            fib1 = fibM
            fibM = fib2 + fib1
        }

        var offset = -1

        while fibM > 1 {
            let i = min(offset + fib2, n - 1)

            if array[i] < target {
                fibM = fib1
                fib1 = fib2
                fib2 = fibM - fib1
                offset = i
            } else if array[i] > target {
                fibM = fib2
                fib1 = fib1 - fib2
                fib2 = fibM - fib1
            } else {
                return i
            }
        }

        // Check last element
        if fib1 == 1 && offset + 1 < n && array[offset + 1] == target {
            return offset + 1
        }

        return nil
    }

    // MARK: - Specialized Search Algorithms

    /// Search in rotated sorted array
    /// - Complexity: O(log n) time, O(1) space
    public static func searchRotated<T: Comparable>(_ array: [T], target: T) -> Int? {
        var left = 0
        var right = array.count - 1

        while left <= right {
            let mid = left + (right - left) / 2

            if array[mid] == target {
                return mid
            }

            // Determine which half is sorted
            if array[left] <= array[mid] {
                // Left half is sorted
                if array[left] <= target && target < array[mid] {
                    right = mid - 1
                } else {
                    left = mid + 1
                }
            } else {
                // Right half is sorted
                if array[mid] < target && target <= array[right] {
                    left = mid + 1
                } else {
                    right = mid - 1
                }
            }
        }

        return nil
    }

    /// Find peak element in array (local maximum)
    /// - Complexity: O(log n) time, O(1) space
    public static func findPeak<T: Comparable>(_ array: [T]) -> Int? {
        guard !array.isEmpty else { return nil }

        var left = 0
        var right = array.count - 1

        while left < right {
            let mid = left + (right - left) / 2

            if array[mid] > array[mid + 1] {
                right = mid
            } else {
                left = mid + 1
            }
        }

        return left
    }

    /// Two-pointer search for pair with given sum
    /// - Complexity: O(n) time for sorted array, O(1) space
    public static func twoSum(_ array: [Int], target: Int) -> (Int, Int)? {
        var left = 0
        var right = array.count - 1

        while left < right {
            let sum = array[left] + array[right]

            if sum == target {
                return (left, right)
            } else if sum < target {
                left += 1
            } else {
                right -= 1
            }
        }

        return nil
    }

    /// Three-pointer search for triplet with given sum
    /// - Complexity: O(n²) time, O(1) space
    public static func threeSum(_ array: [Int], target: Int) -> [(Int, Int, Int)] {
        var result: [(Int, Int, Int)] = []
        let sortedArray = array.sorted()

        for i in 0..<sortedArray.count - 2 {
            // Skip duplicates
            if i > 0 && sortedArray[i] == sortedArray[i - 1] {
                continue
            }

            var left = i + 1
            var right = sortedArray.count - 1

            while left < right {
                let sum = sortedArray[i] + sortedArray[left] + sortedArray[right]

                if sum == target {
                    result.append((i, left, right))

                    // Skip duplicates
                    while left < right && sortedArray[left] == sortedArray[left + 1] {
                        left += 1
                    }
                    while left < right && sortedArray[right] == sortedArray[right - 1] {
                        right -= 1
                    }

                    left += 1
                    right -= 1
                } else if sum < target {
                    left += 1
                } else {
                    right -= 1
                }
            }
        }

        return result
    }

    // MARK: - K-th Element Algorithms

    /// Quick select to find k-th smallest element
    /// - Complexity: O(n) average, O(n²) worst case
    public static func quickSelect<T: Comparable>(_ array: inout [T], k: Int) -> T? {
        guard k > 0 && k <= array.count else { return nil }
        return quickSelectHelper(&array, k - 1, 0, array.count - 1)
    }

    private static func quickSelectHelper<T: Comparable>(
        _ array: inout [T],
        _ k: Int,
        _ left: Int,
        _ right: Int
    ) -> T? {
        if left == right {
            return array[left]
        }

        let pivotIndex = partition(&array, left, right)

        if k == pivotIndex {
            return array[k]
        } else if k < pivotIndex {
            return quickSelectHelper(&array, k, left, pivotIndex - 1)
        } else {
            return quickSelectHelper(&array, k, pivotIndex + 1, right)
        }
    }

    private static func partition<T: Comparable>(_ array: inout [T], _ left: Int, _ right: Int) -> Int {
        let pivot = array[right]
        var i = left

        for j in left..<right {
            if array[j] <= pivot {
                array.swapAt(i, j)
                i += 1
            }
        }

        array.swapAt(i, right)
        return i
    }

    // MARK: - Pattern Searching

    /// Naive pattern search in string
    /// - Complexity: O(nm) time where n is text length, m is pattern length
    public static func naivePatternSearch(_ text: String, pattern: String) -> [Int] {
        var result: [Int] = []
        let textArray = Array(text)
        let patternArray = Array(pattern)
        let n = textArray.count
        let m = patternArray.count

        for i in 0...(n - m) {
            var j = 0

            while j < m && textArray[i + j] == patternArray[j] {
                j += 1
            }

            if j == m {
                result.append(i)
            }
        }

        return result
    }

    // MARK: - Parallel Search (iOS Optimized)

    /// Parallel search using GCD for large datasets
    @available(iOS 13.0, macOS 10.15, *)
    public static func parallelSearch<T: Equatable>(
        _ array: [T],
        target: T
    ) async -> [Int] {
        let chunkSize = max(1, array.count / ProcessInfo.processInfo.activeProcessorCount)

        return await withTaskGroup(of: [Int].self) { group in
            for (offset, chunk) in array.chunked(into: chunkSize).enumerated() {
                group.addTask {
                    var indices: [Int] = []
                    for (index, element) in chunk.enumerated() {
                        if element == target {
                            indices.append(offset * chunkSize + index)
                        }
                    }
                    return indices
                }
            }

            var allIndices: [Int] = []
            for await indices in group {
                allIndices.append(contentsOf: indices)
            }

            return allIndices.sorted()
        }
    }
}

// MARK: - Helper Extensions

private extension Array {
    /// Split array into chunks of specified size
    func chunked(into size: Int) -> [[Element]] {
        return stride(from: 0, to: count, by: size).map {
            Array(self[$0..<Swift.min($0 + size, count)])
        }
    }
}

// MARK: - Search Result Type

/// Result type for detailed search operations
public struct SearchResult<T> {
    public let index: Int?
    public let element: T?
    public let comparisons: Int
    public let timeElapsed: TimeInterval

    public var found: Bool {
        return index != nil
    }
}

// MARK: - Performance Measurement

/// Utility for measuring search performance
public struct SearchBenchmark {
    /// Measure search algorithm performance
    public static func measure<T: Comparable>(
        _ array: [T],
        target: T,
        algorithm: (([T], T) -> Int?)
    ) -> SearchResult<T> {
        let startTime = CFAbsoluteTimeGetCurrent()
        var comparisons = 0

        // Hook for counting comparisons (simplified for example)
        let index = algorithm(array, target)

        let timeElapsed = CFAbsoluteTimeGetCurrent() - startTime

        return SearchResult(
            index: index,
            element: index.map { array[$0] },
            comparisons: comparisons,
            timeElapsed: timeElapsed
        )
    }

    /// Compare multiple search algorithms
    public static func compare<T: Comparable>(
        _ array: [T],
        target: T,
        algorithms: [(name: String, function: ([T], T) -> Int?)]
    ) -> [(name: String, result: SearchResult<T>)] {
        return algorithms.map { (name, function) in
            (name, measure(array, target: target, algorithm: function))
        }
    }
}