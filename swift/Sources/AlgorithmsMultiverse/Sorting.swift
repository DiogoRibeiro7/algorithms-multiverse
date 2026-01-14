import Foundation
import Dispatch

/// Protocol for sortable collections
public protocol SortableCollection {
    associatedtype Element: Comparable
    func sorted(by algorithm: SortingAlgorithm) -> [Element]
}

/// Enum representing different sorting algorithms
public enum SortingAlgorithm {
    case quickSort
    case mergeSort
    case heapSort
    case timSort
    case radixSort
    case introSort
}

/// Sorting algorithms implementation with iOS optimizations
public struct Sorting {

    // MARK: - Quick Sort

    /// Quick Sort with in-place sorting
    /// - Complexity: O(n log n) average case, O(n²) worst case
    public static func quickSort<T: Comparable>(_ array: inout [T]) {
        quickSort(&array, low: 0, high: array.count - 1)
    }

    private static func quickSort<T: Comparable>(_ array: inout [T], low: Int, high: Int) {
        guard low < high else { return }

        let pivot = partition(&array, low: low, high: high)
        quickSort(&array, low: low, high: pivot - 1)
        quickSort(&array, low: pivot + 1, high: high)
    }

    private static func partition<T: Comparable>(_ array: inout [T], low: Int, high: Int) -> Int {
        // Three-way partitioning for better performance with duplicates
        let pivot = array[high]
        var i = low - 1

        for j in low..<high {
            if array[j] <= pivot {
                i += 1
                array.swapAt(i, j)
            }
        }

        array.swapAt(i + 1, high)
        return i + 1
    }

    /// Parallel Quick Sort using Grand Central Dispatch
    @available(iOS 13.0, macOS 10.15, *)
    public static func parallelQuickSort<T: Comparable>(_ array: [T]) async -> [T] {
        guard array.count > 1 else { return array }

        return await withTaskGroup(of: [T].self) { group in
            await parallelQuickSortHelper(array, group: &group)
        }
    }

    @available(iOS 13.0, macOS 10.15, *)
    private static func parallelQuickSortHelper<T: Comparable>(
        _ array: [T],
        group: inout TaskGroup<[T]>
    ) async -> [T] {
        guard array.count > 1 else { return array }

        let pivot = array[array.count / 2]
        let less = array.filter { $0 < pivot }
        let equal = array.filter { $0 == pivot }
        let greater = array.filter { $0 > pivot }

        if array.count > 1000 {
            // Parallel execution for large arrays
            group.addTask { await parallelQuickSortHelper(less, group: &group) }
            group.addTask { await parallelQuickSortHelper(greater, group: &group) }

            var results: [[T]] = []
            for await result in group {
                results.append(result)
            }

            return results[0] + equal + results[1]
        } else {
            // Sequential for small arrays
            let sortedLess = await parallelQuickSortHelper(less, group: &group)
            let sortedGreater = await parallelQuickSortHelper(greater, group: &group)
            return sortedLess + equal + sortedGreater
        }
    }

    // MARK: - Merge Sort

    /// Merge Sort implementation
    /// - Complexity: O(n log n) all cases
    public static func mergeSort<T: Comparable>(_ array: [T]) -> [T] {
        guard array.count > 1 else { return array }

        let middle = array.count / 2
        let left = mergeSort(Array(array[..<middle]))
        let right = mergeSort(Array(array[middle...]))

        return merge(left, right)
    }

    private static func merge<T: Comparable>(_ left: [T], _ right: [T]) -> [T] {
        var result: [T] = []
        result.reserveCapacity(left.count + right.count)

        var leftIndex = 0
        var rightIndex = 0

        while leftIndex < left.count && rightIndex < right.count {
            if left[leftIndex] <= right[rightIndex] {
                result.append(left[leftIndex])
                leftIndex += 1
            } else {
                result.append(right[rightIndex])
                rightIndex += 1
            }
        }

        result.append(contentsOf: left[leftIndex...])
        result.append(contentsOf: right[rightIndex...])

        return result
    }

    // MARK: - Heap Sort

    /// Heap Sort implementation
    /// - Complexity: O(n log n) all cases
    public static func heapSort<T: Comparable>(_ array: inout [T]) {
        let n = array.count

        // Build max heap
        for i in stride(from: n/2 - 1, through: 0, by: -1) {
            heapify(&array, n: n, i: i)
        }

        // Extract elements from heap
        for i in stride(from: n - 1, through: 1, by: -1) {
            array.swapAt(0, i)
            heapify(&array, n: i, i: 0)
        }
    }

    private static func heapify<T: Comparable>(_ array: inout [T], n: Int, i: Int) {
        var largest = i
        let left = 2 * i + 1
        let right = 2 * i + 2

        if left < n && array[left] > array[largest] {
            largest = left
        }

        if right < n && array[right] > array[largest] {
            largest = right
        }

        if largest != i {
            array.swapAt(i, largest)
            heapify(&array, n: n, i: largest)
        }
    }

    // MARK: - Tim Sort

    /// Tim Sort - Hybrid stable sorting algorithm
    /// - Complexity: O(n log n) all cases
    public static func timSort<T: Comparable>(_ array: [T]) -> [T] {
        let minMerge = 32
        var result = array
        let n = result.count

        // Sort individual runs using insertion sort
        for start in stride(from: 0, to: n, by: minMerge) {
            let end = min(start + minMerge - 1, n - 1)
            insertionSort(&result, left: start, right: end)
        }

        // Merge sorted runs
        var size = minMerge
        while size < n {
            for start in stride(from: 0, to: n, by: size * 2) {
                let mid = start + size - 1
                let end = min(start + size * 2 - 1, n - 1)

                if mid < end {
                    mergeInPlace(&result, left: start, mid: mid, right: end)
                }
            }
            size *= 2
        }

        return result
    }

    private static func insertionSort<T: Comparable>(_ array: inout [T], left: Int, right: Int) {
        for i in (left + 1)...right {
            let key = array[i]
            var j = i - 1

            while j >= left && array[j] > key {
                array[j + 1] = array[j]
                j -= 1
            }

            array[j + 1] = key
        }
    }

    private static func mergeInPlace<T: Comparable>(_ array: inout [T], left: Int, mid: Int, right: Int) {
        let leftArray = Array(array[left...mid])
        let rightArray = Array(array[(mid + 1)...right])

        var i = 0, j = 0, k = left

        while i < leftArray.count && j < rightArray.count {
            if leftArray[i] <= rightArray[j] {
                array[k] = leftArray[i]
                i += 1
            } else {
                array[k] = rightArray[j]
                j += 1
            }
            k += 1
        }

        while i < leftArray.count {
            array[k] = leftArray[i]
            i += 1
            k += 1
        }

        while j < rightArray.count {
            array[k] = rightArray[j]
            j += 1
            k += 1
        }
    }

    // MARK: - Radix Sort

    /// Radix Sort for integers
    /// - Complexity: O(nk) where k is the number of digits
    public static func radixSort(_ array: inout [Int]) {
        guard !array.isEmpty else { return }

        let maxElement = array.max()!
        var exp = 1

        while maxElement / exp > 0 {
            countingSortByDigit(&array, exp: exp)
            exp *= 10
        }
    }

    private static func countingSortByDigit(_ array: inout [Int], exp: Int) {
        let n = array.count
        var output = Array(repeating: 0, count: n)
        var count = Array(repeating: 0, count: 10)

        // Count occurrences
        for i in 0..<n {
            let index = (array[i] / exp) % 10
            count[index] += 1
        }

        // Cumulative count
        for i in 1..<10 {
            count[i] += count[i - 1]
        }

        // Build output array
        for i in stride(from: n - 1, through: 0, by: -1) {
            let index = (array[i] / exp) % 10
            output[count[index] - 1] = array[i]
            count[index] -= 1
        }

        // Copy output to array
        array = output
    }

    // MARK: - Counting Sort

    /// Counting Sort for small range integers
    /// - Complexity: O(n + k) where k is the range
    public static func countingSort(_ array: [Int], maxValue: Int) -> [Int] {
        var count = Array(repeating: 0, count: maxValue + 1)
        var output = Array(repeating: 0, count: array.count)

        // Count occurrences
        for num in array {
            count[num] += 1
        }

        // Cumulative count
        for i in 1...maxValue {
            count[i] += count[i - 1]
        }

        // Build output array
        for i in stride(from: array.count - 1, through: 0, by: -1) {
            output[count[array[i]] - 1] = array[i]
            count[array[i]] -= 1
        }

        return output
    }

    // MARK: - Utility Functions

    /// Check if array is sorted
    public static func isSorted<T: Comparable>(_ array: [T]) -> Bool {
        for i in 1..<array.count {
            if array[i - 1] > array[i] {
                return false
            }
        }
        return true
    }

    /// Shuffle array using Fisher-Yates algorithm
    public static func shuffle<T>(_ array: inout [T]) {
        for i in stride(from: array.count - 1, through: 1, by: -1) {
            let j = Int.random(in: 0...i)
            array.swapAt(i, j)
        }
    }

    /// Find k-th smallest element using QuickSelect
    /// - Complexity: O(n) average case
    public static func quickSelect<T: Comparable>(_ array: [T], k: Int) -> T? {
        guard k >= 0 && k < array.count else { return nil }

        var arr = array
        return quickSelectHelper(&arr, k: k, low: 0, high: array.count - 1)
    }

    private static func quickSelectHelper<T: Comparable>(
        _ array: inout [T],
        k: Int,
        low: Int,
        high: Int
    ) -> T {
        if low == high {
            return array[low]
        }

        let pivotIndex = partition(&array, low: low, high: high)

        if k == pivotIndex {
            return array[k]
        } else if k < pivotIndex {
            return quickSelectHelper(&array, k: k, low: low, high: pivotIndex - 1)
        } else {
            return quickSelectHelper(&array, k: k, low: pivotIndex + 1, high: high)
        }
    }
}

// MARK: - Array Extensions

extension Array where Element: Comparable {
    /// Sort array using specified algorithm
    public func sorted(using algorithm: SortingAlgorithm) -> [Element] {
        switch algorithm {
        case .quickSort:
            var copy = self
            Sorting.quickSort(&copy)
            return copy
        case .mergeSort:
            return Sorting.mergeSort(self)
        case .heapSort:
            var copy = self
            Sorting.heapSort(&copy)
            return copy
        case .timSort:
            return Sorting.timSort(self)
        case .radixSort:
            guard Element.self == Int.self else {
                return self.sorted()
            }
            var copy = self as! [Int]
            Sorting.radixSort(&copy)
            return copy as! [Element]
        case .introSort:
            return self.sorted() // Use Swift's built-in introsort
        }
    }

    /// Check if array is sorted
    public var isSorted: Bool {
        Sorting.isSorted(self)
    }

    /// Shuffle array in place
    public mutating func shuffle() {
        Sorting.shuffle(&self)
    }

    /// Find k-th smallest element
    public func kthSmallest(_ k: Int) -> Element? {
        Sorting.quickSelect(self, k: k)
    }
}

// MARK: - Performance Measurement

/// Measure sorting performance
public struct SortingBenchmark {
    public let algorithm: String
    public let elementCount: Int
    public let executionTime: TimeInterval
    public let isSorted: Bool

    public static func measure<T: Comparable>(
        _ array: [T],
        algorithm: SortingAlgorithm
    ) -> SortingBenchmark {
        let start = CFAbsoluteTimeGetCurrent()
        let sorted = array.sorted(using: algorithm)
        let end = CFAbsoluteTimeGetCurrent()

        return SortingBenchmark(
            algorithm: "\(algorithm)",
            elementCount: array.count,
            executionTime: end - start,
            isSorted: Sorting.isSorted(sorted)
        )
    }
}