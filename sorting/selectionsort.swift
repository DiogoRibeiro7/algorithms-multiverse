// Selection Sort Algorithm - Educational Implementation (Swift)
//
// ALGORITHM OVERVIEW:
// ==================
// Selection Sort works by repeatedly finding the minimum element from the unsorted
// portion of the array and placing it at the beginning. It divides the array into
// two parts: a sorted portion (left) and an unsorted portion (right).
//
// Time Complexity:
// - Best Case: O(n²) - Even if array is already sorted, still searches for minimum
// - Average Case: O(n²)
// - Worst Case: O(n²)
// - IMPORTANT: Unlike bubble sort and insertion sort, selection sort ALWAYS performs
//   O(n²) comparisons, regardless of input
//
// Space Complexity: O(1) - Sorts in-place with only constant extra space
//
// Stability: NOT stable by default (can be made stable with modifications)
// In-place: YES
//
// KEY ADVANTAGE: Makes MINIMUM number of swaps - only O(n) swaps!

import Foundation

// MARK: - Standard Selection Sort

/// Standard selection sort implementation.
///
/// ALGORITHM STEPS:
/// ===============
/// 1. Find the minimum element in the unsorted portion
/// 2. Swap it with the first element of the unsorted portion
/// 3. Move the boundary of sorted/unsorted portions one element to the right
/// 4. Repeat until the entire array is sorted
///
/// Visual Example:
/// ==============
/// Initial: [64, 25, 12, 22, 11]
///
/// Pass 1: Find min in [64, 25, 12, 22, 11] → 11
///         Swap 64 ↔ 11
///         Result: [11, 25, 12, 22, 64]
///                  ^^^ sorted portion
///
/// Pass 2: Find min in [25, 12, 22, 64] → 12
///         Swap 25 ↔ 12
///         Result: [11, 12, 25, 22, 64]
///                  ^^^^^^^ sorted portion
///
/// Time: O(n²), Space: O(n) for new array
func selectionSort<T: Comparable>(_ array: [T]) -> [T] {
    guard array.count > 1 else { return array }

    var result = array
    selectionSortInPlace(&result)
    return result
}

/// In-place selection sort implementation.
///
/// DETAILED STEP-BY-STEP:
/// ======================
/// For each position i from 0 to n-1:
///     - Assume arr[i] is the minimum
///     - Scan all elements from i+1 to n-1
///     - Track the index of the actual minimum element
///     - After scanning, swap arr[i] with the minimum element found
///
/// Time: O(n²), Space: O(1)
func selectionSortInPlace<T: Comparable>(_ array: inout [T]) {
    let n = array.count

    // Outer loop: Move boundary of unsorted subarray one by one
    for i in 0..<(n - 1) {
        // Find the minimum element in the remaining unsorted array
        // Start by assuming the first unsorted element is the minimum
        var minIdx = i

        // Inner loop: Search for the minimum in array[i+1...n-1]
        for j in (i + 1)..<n {
            // If we find a smaller element, update minIdx
            if array[j] < array[minIdx] {
                minIdx = j
            }
        }

        // Swap the found minimum element with the first element
        // of the unsorted portion
        if minIdx != i {
            array.swapAt(i, minIdx)
        }
    }
}

/// Selection sort with custom comparator.
func selectionSort<T>(_ array: [T], by comparator: (T, T) -> Bool) -> [T] {
    guard array.count > 1 else { return array }

    var result = array
    let n = result.count

    for i in 0..<(n - 1) {
        var minIdx = i

        for j in (i + 1)..<n {
            if comparator(result[j], result[minIdx]) {
                minIdx = j
            }
        }

        if minIdx != i {
            result.swapAt(i, minIdx)
        }
    }

    return result
}

// MARK: - Bidirectional Selection Sort

/// Bidirectional selection sort (also called "double selection sort").
///
/// OPTIMIZATION:
/// ============
/// Instead of finding just the minimum in each pass, we find BOTH the minimum
/// and maximum elements. We place the minimum at the beginning and the maximum
/// at the end, reducing the number of passes by approximately half.
///
/// Time: Still O(n²), but approximately 2x faster in practice
func bidirectionalSelectionSort<T: Comparable>(_ array: [T]) -> [T] {
    guard array.count > 1 else { return array }

    var result = array
    let n = result.count

    // Process from both ends toward the middle
    var left = 0
    var right = n - 1

    while left < right {
        // Find both minimum and maximum in the current range
        var minIdx = left
        var maxIdx = left

        for i in left...right {
            if result[i] < result[minIdx] {
                minIdx = i
            }
            if result[i] > result[maxIdx] {
                maxIdx = i
            }
        }

        // Handle special case: if min is at right position
        if minIdx == right {
            result.swapAt(left, right)
            if maxIdx == left {
                maxIdx = right
            }
        } else {
            // Swap minimum to the left boundary
            if minIdx != left {
                result.swapAt(left, minIdx)
            }

            // If maximum was at left position, it's now at minIdx
            if maxIdx == left {
                maxIdx = minIdx
            }

            // Swap maximum to the right boundary
            if maxIdx != right {
                result.swapAt(right, maxIdx)
            }
        }

        // Move boundaries inward
        left += 1
        right -= 1
    }

    return result
}

// MARK: - Recursive Selection Sort

/// Recursive implementation of selection sort.
///
/// RECURSIVE APPROACH:
/// ==================
/// Base case: Array of size 0 or 1 is already sorted
/// Recursive case:
///     1. Find the minimum element in the array
///     2. Swap it with the first element
///     3. Recursively sort the rest of the array (excluding the first element)
///
/// Time: O(n²), Space: O(n) for recursion stack
func selectionSortRecursive<T: Comparable>(_ array: [T]) -> [T] {
    guard array.count > 1 else { return array }

    var result = array
    selectionSortRecursiveHelper(&result, startIdx: 0)
    return result
}

private func selectionSortRecursiveHelper<T: Comparable>(_ array: inout [T], startIdx: Int) {
    // Base case: if we've reached the end, we're done
    guard startIdx < array.count - 1 else { return }

    // Find the minimum element in array[startIdx...n-1]
    var minIdx = startIdx
    for i in (startIdx + 1)..<array.count {
        if array[i] < array[minIdx] {
            minIdx = i
        }
    }

    // Swap the minimum with the element at startIdx
    if minIdx != startIdx {
        array.swapAt(startIdx, minIdx)
    }

    // Recursively sort the rest
    selectionSortRecursiveHelper(&array, startIdx: startIdx + 1)
}

// MARK: - Stable Selection Sort

/// Stable version of selection sort.
///
/// WHY STANDARD SELECTION SORT IS UNSTABLE:
/// ========================================
/// When we swap the minimum element with the first element of the unsorted
/// portion, we can change the relative order of equal elements.
///
/// MAKING IT STABLE:
/// ================
/// Instead of swapping, we shift all elements and insert the minimum
/// at the correct position. This preserves the relative order.
///
/// Time: O(n²) comparisons + O(n²) shifts
func stableSelectionSort<T: Comparable>(_ array: [T]) -> [T] {
    guard array.count > 1 else { return array }

    var result = array
    let n = result.count

    for i in 0..<(n - 1) {
        // Find minimum in unsorted portion
        var minIdx = i
        for j in (i + 1)..<n {
            if result[j] < result[minIdx] {
                minIdx = j
            }
        }

        // Instead of swapping, shift elements and insert
        if minIdx != i {
            let minValue = result[minIdx]
            // Shift all elements between i and minIdx one position right
            for k in stride(from: minIdx, to: i, by: -1) {
                result[k] = result[k - 1]
            }
            // Place minimum at position i
            result[i] = minValue
        }
    }

    return result
}

// MARK: - Visualization and Statistics

/// Tracks sorting operations
class SortStatistics {
    var comparisons = 0
    var swaps = 0
    var arrayAccesses = 0

    func reset() {
        comparisons = 0
        swaps = 0
        arrayAccesses = 0
    }

    var description: String {
        return "Comparisons: \(comparisons), Swaps: \(swaps), Array Accesses: \(arrayAccesses)"
    }
}

/// Selection sort with operation counting
func selectionSortWithStats<T: Comparable>(_ array: [T], stats: SortStatistics) -> [T] {
    stats.reset()
    guard array.count > 1 else { return array }

    var result = array
    let n = result.count

    for i in 0..<(n - 1) {
        var minIdx = i
        stats.arrayAccesses += 1

        for j in (i + 1)..<n {
            stats.comparisons += 1
            stats.arrayAccesses += 2  // Read result[j] and result[minIdx]
            if result[j] < result[minIdx] {
                minIdx = j
            }
        }

        if minIdx != i {
            stats.swaps += 1
            stats.arrayAccesses += 4  // Two reads, two writes
            result.swapAt(i, minIdx)
        }
    }

    return result
}

/// Creates a step-by-step visualization of selection sort
func visualizeSelectionSort(_ array: [Int]) -> [String] {
    var steps = [String]()
    var result = array

    steps.append(String(repeating: "=", count: 70))
    steps.append("SELECTION SORT VISUALIZATION")
    steps.append(String(repeating: "=", count: 70))
    steps.append("Initial array: \(result)")
    steps.append("")

    let n = result.count
    for i in 0..<(n - 1) {
        steps.append("Pass \(i + 1):")
        let unsorted = Array(result[i...])
        steps.append("  Looking for minimum in unsorted portion: \(unsorted)")

        var minIdx = i
        var minValue = result[i]

        // Show the search process
        for j in (i + 1)..<n {
            if result[j] < minValue {
                minIdx = j
                minValue = result[j]
                steps.append("    Found new minimum: \(minValue) at index \(minIdx)")
            }
        }

        // Show the swap
        if minIdx != i {
            steps.append("  Swapping \(result[i]) ↔ \(result[minIdx])")
            result.swapAt(i, minIdx)
        } else {
            steps.append("  No swap needed (minimum already in place)")
        }

        // Show current state
        let sorted = Array(result[0...i])
        let unsortedPart = i + 1 < n ? Array(result[(i + 1)...]) : []
        steps.append("  Sorted: \(sorted) | Unsorted: \(unsortedPart)")
        steps.append("")
    }

    steps.append("Final sorted array: \(result)")
    steps.append(String(repeating: "=", count: 70))

    return steps
}

// MARK: - Array Extension

extension Array where Element: Comparable {
    /// Returns a new array sorted using selection sort
    func selectionSorted() -> [Element] {
        return selectionSort(self)
    }

    /// Sorts the array in-place using selection sort
    mutating func selectionSort() {
        selectionSortInPlace(&self)
    }

    /// Returns true if the array is sorted in ascending order
    func isSorted() -> Bool {
        guard count > 1 else { return true }
        for i in 0..<(count - 1) {
            if self[i] > self[i + 1] {
                return false
            }
        }
        return true
    }
}

// MARK: - Demonstration and Testing

func demonstrateSelectionSort() {
    print("📚 SELECTION SORT - EDUCATIONAL DEMONSTRATION")
    print(String(repeating: "=", count: 80))

    // Test cases
    struct TestCase {
        let arr: [Int]
        let desc: String
    }

    let testCases = [
        TestCase(arr: [64, 25, 12, 22, 11], desc: "Random array"),
        TestCase(arr: [5, 2, 8, 6, 1, 9, 4], desc: "Small random array"),
        TestCase(arr: [1], desc: "Single element"),
        TestCase(arr: [], desc: "Empty array"),
        TestCase(arr: [3, 3, 3, 3, 3], desc: "All duplicates"),
        TestCase(arr: [9, 8, 7, 6, 5, 4, 3, 2, 1], desc: "Reverse sorted"),
        TestCase(arr: [1, 2, 3, 4, 5], desc: "Already sorted"),
        TestCase(arr: [1, 3, 2, 4, 5], desc: "Nearly sorted")
    ]

    print("\n📋 BASIC FUNCTIONALITY TESTS:")
    print(String(repeating: "-", count: 80))

    for tc in testCases {
        let original = tc.arr
        let standard = selectionSort(tc.arr)
        let bidirectional = bidirectionalSelectionSort(tc.arr)
        let recursive = selectionSortRecursive(tc.arr)
        let stable = stableSelectionSort(tc.arr)

        print("\nTest: \(tc.desc)")
        print("Original:      \(original)")
        print("Standard:      \(standard)")
        print("Bidirectional: \(bidirectional)")
        print("Recursive:     \(recursive)")
        print("Stable:        \(stable)")

        let allCorrect = standard.isSorted() && bidirectional.isSorted() &&
                        recursive.isSorted() && stable.isSorted()

        let status = allCorrect ? "✓" : "✗"
        print("All correct: \(status)")
    }

    // Visualization
    print("\n\n🎬 STEP-BY-STEP VISUALIZATION:")
    print(String(repeating: "-", count: 80))

    let demoArr = [64, 25, 12, 22, 11]
    let steps = visualizeSelectionSort(demoArr)
    for step in steps {
        print(step)
    }

    // Memory analysis
    print("\n\n💾 MEMORY USAGE ANALYSIS:")
    print(String(repeating: "-", count: 80))
    print("""

    Selection Sort Memory Characteristics:

    1. In-Place Sorting:
       - Space Complexity: O(1) auxiliary space
       - Only uses constant extra memory (minIdx, loop variables)
       - Original array is modified in-place

    2. Memory Writes:
       - Selection Sort: O(n) swaps (minimum writes)
       - Bubble Sort: O(n²) swaps in worst case
       - Insertion Sort: O(n²) shifts in worst case

       ⭐ This makes Selection Sort ideal when writing to memory is expensive!
          Examples: Flash memory, EEPROM, or distributed systems

    3. Swift-Specific:
       - Uses swapAt() method for efficient swapping
       - Copy-on-write semantics for arrays
       - Generic functions with Comparable protocol
    """)

    print("\n📌 WHEN TO USE SELECTION SORT:")
    print(String(repeating: "-", count: 80))
    print("""

    ✅ GOOD USE CASES:

    1. Minimal Memory Writes:
       - Flash memory or EEPROM (limited write cycles)
       - Distributed systems where network writes are expensive

    2. Small Datasets:
       - When simplicity matters more than efficiency
       - Educational purposes to understand sorting concepts

    3. Known Small Data:
       - Embedded systems with small, fixed-size arrays
       - When n is guaranteed to be small (< 20 elements)

    ❌ POOR USE CASES:

    1. Large Datasets:
       - Always O(n²) time, never adapts to input
       - Much slower than O(n log n) algorithms

    2. Nearly Sorted Data:
       - Unlike insertion sort, doesn't benefit from sorted input
       - Still performs all O(n²) comparisons

    3. Stable Sorting Required:
       - Standard selection sort is not stable
       - Making it stable adds overhead
    """)
}

func performanceBenchmark() {
    print("\n\n⚡ PERFORMANCE BENCHMARK")
    print(String(repeating: "=", count: 80))

    let sizes = [10, 20, 50, 100, 200]

    enum Pattern {
        case random
        case sorted
        case reversed

        func generate(_ n: Int) -> [Int] {
            switch self {
            case .random:
                return (0..<n).map { _ in Int.random(in: 1...1000) }
            case .sorted:
                return Array(0..<n)
            case .reversed:
                return Array((0..<n).reversed())
            }
        }
    }

    for pattern in [Pattern.random, .sorted, .reversed] {
        let patternName: String
        switch pattern {
        case .random: patternName = "Random"
        case .sorted: patternName = "Sorted"
        case .reversed: patternName = "Reversed"
        }

        print("\n\(patternName) Data:")
        print(String(format: "%-10s%15s%15s%15s", "Size", "Standard", "Bidirectional", "Recursive"))
        print(String(repeating: "-", count: 55))

        for size in sizes {
            let testData = pattern.generate(size)

            // Standard
            var start = Date()
            _ = selectionSort(testData)
            var elapsed = Date().timeIntervalSince(start)
            print(String(format: "%-10d%14.3fms", size, elapsed * 1000), terminator: "")

            // Bidirectional
            start = Date()
            _ = bidirectionalSelectionSort(testData)
            elapsed = Date().timeIntervalSince(start)
            print(String(format: "%14.3fms", elapsed * 1000), terminator: "")

            // Recursive
            start = Date()
            _ = selectionSortRecursive(testData)
            elapsed = Date().timeIntervalSince(start)
            print(String(format: "%14.3fms\n", elapsed * 1000), terminator: "")
        }
    }
}

// MARK: - Main

demonstrateSelectionSort()
performanceBenchmark()

print("\n✨ Selection Sort demonstration complete!")
