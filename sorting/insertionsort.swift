// Insertion Sort Algorithm Implementation in Swift
//
// Time Complexity:
// - Best Case: O(n) - when array is already sorted
// - Average Case: O(n²)
// - Worst Case: O(n²) - when array is reverse sorted
// Space Complexity: O(1) for in-place, O(n) for functional approach
//
// Insertion Sort builds the final sorted array one item at a time.
//
// Swift features:
// - Generic functions with Comparable protocol
// - Protocol extensions on Array
// - Value semantics and copy-on-write
// - Tuple-based stability demonstration
// - Custom operators and closures

import Foundation

// MARK: - Basic Insertion Sort

/// Performs standard insertion sort.
///
/// Time Complexity: O(n²) average and worst case, O(n) best case
/// Space Complexity: O(n) for the new array
///
/// Example visualization:
///   Initial: [5, 2, 8, 6, 1]
///   Step 1:  [2, 5, 8, 6, 1]  // Insert 2
///   Step 2:  [2, 5, 8, 6, 1]  // 8 already in place
///   Step 3:  [2, 5, 6, 8, 1]  // Insert 6
///   Step 4:  [1, 2, 5, 6, 8]  // Insert 1
func insertionSort<T: Comparable>(_ array: [T]) -> [T] {
    guard array.count > 1 else { return array }
    var result = array
    insertionSortInPlace(&result)
    return result
}

/// Sorts the array in-place using insertion sort.
///
/// Time Complexity: O(n²) average and worst case, O(n) best case
/// Space Complexity: O(1)
func insertionSortInPlace<T: Comparable>(_ array: inout [T]) {
    for i in 1..<array.count {
        let key = array[i]
        var j = i - 1

        // Move elements greater than key one position ahead
        while j >= 0 && array[j] > key {
            array[j + 1] = array[j]
            j -= 1
        }

        array[j + 1] = key
    }
}

/// Insertion sort with custom comparator.
///
/// - Parameters:
///   - array: The array to sort
///   - comparator: A closure that returns true if first element should come before second
/// - Returns: A new sorted array
func insertionSort<T>(_ array: [T], by comparator: (T, T) -> Bool) -> [T] {
    guard array.count > 1 else { return array }
    var result = array

    for i in 1..<result.count {
        let key = result[i]
        var j = i - 1

        while j >= 0 && comparator(key, result[j]) {
            result[j + 1] = result[j]
            j -= 1
        }

        result[j + 1] = key
    }

    return result
}

// MARK: - Recursive Insertion Sort

/// Performs recursive insertion sort.
///
/// Time Complexity: O(n²)
/// Space Complexity: O(n) for recursion stack
func insertionSortRecursive<T: Comparable>(_ array: [T]) -> [T] {
    guard array.count > 1 else { return array }
    var result = array
    insertionSortRecursiveHelper(&result, array.count)
    return result
}

private func insertionSortRecursiveHelper<T: Comparable>(_ array: inout [T], _ n: Int) {
    // Base case
    guard n > 1 else { return }

    // Sort first n-1 elements
    insertionSortRecursiveHelper(&array, n - 1)

    // Insert last element at its correct position
    let key = array[n - 1]
    var j = n - 2

    while j >= 0 && array[j] > key {
        array[j + 1] = array[j]
        j -= 1
    }

    array[j + 1] = key
}

// MARK: - Binary Insertion Sort

/// Uses binary search to find insertion position.
///
/// Time Complexity: O(n²) for moves, O(n log n) for comparisons
/// Space Complexity: O(n)
func binaryInsertionSort<T: Comparable>(_ array: [T]) -> [T] {
    guard array.count > 1 else { return array }
    var result = array

    for i in 1..<result.count {
        let key = result[i]

        // Find position using binary search
        let pos = binarySearchPosition(in: result, left: 0, right: i - 1, key: key)

        // Shift elements to make space
        for j in stride(from: i - 1, through: pos, by: -1) {
            result[j + 1] = result[j]
        }

        result[pos] = key
    }

    return result
}

private func binarySearchPosition<T: Comparable>(in array: [T], left: Int, right: Int, key: T) -> Int {
    guard right >= left else {
        return key > array[left] ? left + 1 : left
    }

    let mid = (left + right) / 2

    if key == array[mid] {
        return mid + 1
    }

    if key > array[mid] {
        return binarySearchPosition(in: array, left: mid + 1, right: right, key: key)
    }

    return binarySearchPosition(in: array, left: left, right: mid - 1, key: key)
}

// MARK: - Shell Sort

/// Performs shell sort (generalization of insertion sort).
///
/// Time Complexity: Depends on gap sequence (O(n log²n) for good sequences)
/// Space Complexity: O(n)
func shellSort<T: Comparable>(_ array: [T]) -> [T] {
    guard array.count > 1 else { return array }
    var result = array
    let n = result.count

    // Start with a large gap, then reduce (Knuth's sequence)
    var gap = 1
    while gap < n / 3 {
        gap = 3 * gap + 1
    }

    // Perform gapped insertion sort
    while gap > 0 {
        for i in gap..<n {
            let key = result[i]
            var j = i

            // Insertion sort with gap
            while j >= gap && result[j - gap] > key {
                result[j] = result[j - gap]
                j -= gap
            }

            result[j] = key
        }

        gap /= 3
    }

    return result
}

// MARK: - Sort Statistics

/// Tracks sorting operations
class SortStatistics {
    var comparisons = 0
    var swaps = 0

    func reset() {
        comparisons = 0
        swaps = 0
    }

    var description: String {
        return "Comparisons: \(comparisons), Swaps: \(swaps)"
    }
}

/// Insertion sort with statistics tracking
func insertionSortWithStats<T: Comparable>(_ array: [T], stats: SortStatistics) -> [T] {
    stats.reset()
    guard array.count > 1 else { return array }
    var result = array

    for i in 1..<result.count {
        let key = result[i]
        var j = i - 1

        while j >= 0 {
            stats.comparisons += 1
            if result[j] > key {
                result[j + 1] = result[j]
                stats.swaps += 1
                j -= 1
            } else {
                break
            }
        }

        result[j + 1] = key
    }

    return result
}

// MARK: - Visualization

/// Creates a step-by-step visualization of insertion sort
func visualizeInsertionSort(_ array: [Int]) -> [String] {
    var steps = [String]()
    var result = array

    steps.append("Initial: \(result)")

    for i in 1..<result.count {
        let key = result[i]
        var j = i - 1

        steps.append("\nStep \(i): Inserting \(key)")
        steps.append("  Before: \(result)")

        while j >= 0 && result[j] > key {
            result[j + 1] = result[j]
            j -= 1
        }

        result[j + 1] = key
        steps.append("  After:  \(result)")
    }

    steps.append("\nFinal: \(result)")
    return steps
}

// MARK: - Stability Demonstration

/// Demonstrates that insertion sort is stable
func demonstrateStability() {
    struct Pair {
        let value: Int
        let originalIndex: Int
    }

    let data = [
        Pair(value: 3, originalIndex: 0),
        Pair(value: 1, originalIndex: 1),
        Pair(value: 3, originalIndex: 2),
        Pair(value: 2, originalIndex: 3),
        Pair(value: 3, originalIndex: 4)
    ]

    // Sort by value only
    let sorted = insertionSort(data) { $0.value < $1.value }

    print("Stability Demonstration:")
    print("Original: ", terminator: "")
    for p in data {
        print("(\(p.value),\(p.originalIndex)) ", terminator: "")
    }
    print()

    print("Sorted:   ", terminator: "")
    for p in sorted {
        print("(\(p.value),\(p.originalIndex)) ", terminator: "")
    }
    print()

    // Check stability - all 3's should maintain original order
    let threeIndices = sorted.filter { $0.value == 3 }.map { $0.originalIndex }
    let isStable = threeIndices == [0, 2, 4]
    print("Stable: \(isStable) (indices of 3's: \(threeIndices))")
}

// MARK: - Array Extension

extension Array where Element: Comparable {
    /// Returns a new array sorted using insertion sort
    func insertionSorted() -> [Element] {
        return insertionSort(self)
    }

    /// Sorts the array in-place using insertion sort
    mutating func insertionSort() {
        insertionSortInPlace(&self)
    }

    /// Returns true if the array is sorted in ascending order
    func isSorted() -> Bool {
        for i in 0..<(count - 1) {
            if self[i] > self[i + 1] {
                return false
            }
        }
        return true
    }
}

// MARK: - Demonstration and Testing

func demonstrateInsertionSort() {
    print("📝 Insertion Sort Implementation in Swift")
    print(String(repeating: "=", count: 60))

    // Test data
    struct TestCase {
        let arr: [Int]
        let desc: String
    }

    let testCases = [
        TestCase(arr: [64, 34, 25, 12, 22, 11, 90], desc: "Random array"),
        TestCase(arr: [5, 2, 8, 6, 1, 9, 4], desc: "Small random array"),
        TestCase(arr: [1], desc: "Single element"),
        TestCase(arr: [], desc: "Empty array"),
        TestCase(arr: [3, 3, 3, 3, 3], desc: "All duplicates"),
        TestCase(arr: [9, 8, 7, 6, 5, 4, 3, 2, 1], desc: "Reverse sorted"),
        TestCase(arr: [1, 2, 3, 4, 5], desc: "Already sorted"),
        TestCase(arr: [1, 3, 2, 4, 5], desc: "Nearly sorted")
    ]

    print("\n📋 Basic Sorting Tests:")
    print(String(repeating: "-", count: 60))

    for tc in testCases {
        let standardResult = insertionSort(tc.arr)
        let binaryResult = binaryInsertionSort(tc.arr)
        let shellResult = shellSort(tc.arr)
        let recursiveResult = insertionSortRecursive(tc.arr)

        print("\nTest: \(tc.desc)")
        print("Original: \(tc.arr)")
        print("Sorted:   \(standardResult)")

        let allCorrect = standardResult.isSorted() && binaryResult.isSorted() &&
                        shellResult.isSorted() && recursiveResult.isSorted()
        let allEqual = standardResult == binaryResult && standardResult == shellResult &&
                      standardResult == recursiveResult

        let status = (allCorrect && allEqual) ? "✓" : "✗"
        print("All implementations match: \(status)")
    }

    // Visualization demo
    print("\n\n🎬 Step-by-Step Visualization:")
    print(String(repeating: "-", count: 60))

    let demoArr = [5, 2, 8, 6, 1]
    let steps = visualizeInsertionSort(demoArr)
    for step in steps {
        print(step)
    }

    // Stability demonstration
    print("\n\n🔒 Stability Demonstration:")
    print(String(repeating: "-", count: 60))
    demonstrateStability()

    // Performance analysis
    print("\n\n📊 Operation Counting:")
    print(String(repeating: "-", count: 60))

    let statTestCases = [
        TestCase(arr: [5, 2, 8, 6, 1], desc: "Random"),
        TestCase(arr: [1, 2, 3, 4, 5], desc: "Already sorted"),
        TestCase(arr: [5, 4, 3, 2, 1], desc: "Reverse sorted")
    ]

    for tc in statTestCases {
        let stats = SortStatistics()
        _ = insertionSortWithStats(tc.arr, stats: stats)

        let n = tc.arr.count
        print("\n\(tc.desc): \(tc.arr)")
        print("Array size (n): \(n)")
        print("Comparisons: \(stats.comparisons)")
        print("Swaps: \(stats.swaps)")
        print("Best case comparisons: \(n - 1)")
        print("Worst case comparisons: \(n * (n - 1) / 2)")
    }
}

// MARK: - Performance Benchmark

func performanceBenchmark() {
    print("\n\n⚡ Performance Benchmark")
    print(String(repeating: "=", count: 80))
    print("\nInsertion sort is preferred for:")
    print("  • Small arrays (typically n < 10-20)")
    print("  • Nearly sorted arrays")
    print("  • As part of hybrid sorting algorithms")
    print()

    let sizes = [5, 10, 20, 50, 100, 500, 1000]

    enum Pattern {
        case random
        case nearlySorted
        case reversed

        func generate(_ n: Int) -> [Int] {
            switch self {
            case .random:
                return (0..<n).map { _ in Int.random(in: 1...1000) }
            case .nearlySorted:
                var arr = Array(0..<n)
                for _ in 0..<min(5, n / 10) {
                    let idx1 = Int.random(in: 0..<n)
                    let idx2 = Int.random(in: 0..<n)
                    arr.swapAt(idx1, idx2)
                }
                return arr
            case .reversed:
                return Array((0..<n).reversed())
            }
        }
    }

    for pattern in [Pattern.random, .nearlySorted, .reversed] {
        let patternName: String
        switch pattern {
        case .random: patternName = "Random"
        case .nearlySorted: patternName = "Nearly Sorted"
        case .reversed: patternName = "Reversed"
        }

        print("\n\(patternName) Data:")
        print(String(format: "%-8s%15s%15s%15s%15s", "Size", "Insertion", "Binary", "Shell", "sorted()"))
        print(String(repeating: "-", count: 68))

        for size in sizes {
            let testData = pattern.generate(size)
            print(String(format: "%-8d", size), terminator: "")

            // Insertion Sort
            var start = Date()
            _ = insertionSort(testData)
            var elapsed = Date().timeIntervalSince(start)
            print(String(format: "%14.3fms", elapsed * 1000), terminator: "")

            // Binary Insertion Sort
            start = Date()
            _ = binaryInsertionSort(testData)
            elapsed = Date().timeIntervalSince(start)
            print(String(format: "%14.3fms", elapsed * 1000), terminator: "")

            // Shell Sort
            start = Date()
            _ = shellSort(testData)
            elapsed = Date().timeIntervalSince(start)
            print(String(format: "%14.3fms", elapsed * 1000), terminator: "")

            // Swift sorted()
            start = Date()
            _ = testData.sorted()
            elapsed = Date().timeIntervalSince(start)
            print(String(format: "%14.3fms\n", elapsed * 1000), terminator: "")
        }
    }
}

// MARK: - Main

demonstrateInsertionSort()
performanceBenchmark()

print("\n✨ Insertion Sort demonstration complete!")
