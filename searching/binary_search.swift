/**
 * Binary Search Algorithm Collection in Swift
 *
 * Comprehensive implementation of binary search variants including:
 * 1. Classic binary search (iterative & recursive)
 * 2. First/last occurrence finding
 * 3. Rotated array search
 * 4. Exponential search
 * 5. Interpolation search
 * 6. Ternary search
 * 7. Binary search on answer (optimization)
 * 8. Advanced utilities
 *
 * Time Complexity: O(log n) for most variants
 * Space Complexity: O(1) iterative, O(log n) recursive
 *
 * Swift Features:
 * - Protocol-oriented programming
 * - Generics with constraints
 * - Optionals for safe unwrapping
 * - First-class functions and closures
 * - Value types and reference types
 */

import Foundation

// ==============================================================================
// 1. CLASSIC BINARY SEARCH
// ==============================================================================

/// Classic binary search - iterative implementation
///
/// Time Complexity: O(log n)
/// Space Complexity: O(1)
func binarySearchIterative<T: Comparable>(_ array: [T], target: T) -> Int? {
    guard !array.isEmpty else { return nil }

    var left = 0
    var right = array.count - 1

    while left <= right {
        let mid = left + (right - left) / 2  // Avoid overflow

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

/// Classic binary search - recursive implementation
///
/// Time Complexity: O(log n)
/// Space Complexity: O(log n) - recursion stack
func binarySearchRecursive<T: Comparable>(_ array: [T], target: T) -> Int? {
    guard !array.isEmpty else { return nil }
    return binarySearchRecursiveHelper(array, target: target, left: 0, right: array.count - 1)
}

private func binarySearchRecursiveHelper<T: Comparable>(
    _ array: [T],
    target: T,
    left: Int,
    right: Int
) -> Int? {
    guard left <= right else { return nil }

    let mid = left + (right - left) / 2

    if array[mid] == target {
        return mid
    } else if array[mid] < target {
        return binarySearchRecursiveHelper(array, target: target, left: mid + 1, right: right)
    } else {
        return binarySearchRecursiveHelper(array, target: target, left: left, right: mid - 1)
    }
}

/// Generic binary search with custom predicate
func binarySearch<T>(
    _ array: [T],
    predicate: (T) -> ComparisonResult
) -> Int? {
    guard !array.isEmpty else { return nil }

    var left = 0
    var right = array.count - 1

    while left <= right {
        let mid = left + (right - left) / 2

        switch predicate(array[mid]) {
        case .orderedSame:
            return mid
        case .orderedAscending:
            left = mid + 1
        case .orderedDescending:
            right = mid - 1
        }
    }

    return nil
}

// ==============================================================================
// 2. FIRST/LAST OCCURRENCE
// ==============================================================================

/// Find first (leftmost) occurrence of target
func findFirstOccurrence<T: Comparable>(_ array: [T], target: T) -> Int? {
    guard !array.isEmpty else { return nil }

    var left = 0
    var right = array.count - 1
    var result: Int? = nil

    while left <= right {
        let mid = left + (right - left) / 2

        if array[mid] == target {
            result = mid
            right = mid - 1  // Continue searching left
        } else if array[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }

    return result
}

/// Find last (rightmost) occurrence of target
func findLastOccurrence<T: Comparable>(_ array: [T], target: T) -> Int? {
    guard !array.isEmpty else { return nil }

    var left = 0
    var right = array.count - 1
    var result: Int? = nil

    while left <= right {
        let mid = left + (right - left) / 2

        if array[mid] == target {
            result = mid
            left = mid + 1  // Continue searching right
        } else if array[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }

    return result
}

/// Count total occurrences of target
func countOccurrences<T: Comparable>(_ array: [T], target: T) -> Int {
    guard let first = findFirstOccurrence(array, target: target) else {
        return 0
    }

    let last = findLastOccurrence(array, target: target)!
    return last - first + 1
}

/// Find range [start, end] of target
func searchRange<T: Comparable>(_ array: [T], target: T) -> (Int, Int)? {
    guard let first = findFirstOccurrence(array, target: target) else {
        return nil
    }

    let last = findLastOccurrence(array, target: target)!
    return (first, last)
}

// ==============================================================================
// 3. ROTATED SORTED ARRAY SEARCH
// ==============================================================================

/// Search in rotated sorted array
func searchRotatedArray(_ array: [Int], target: Int) -> Int? {
    guard !array.isEmpty else { return nil }

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

/// Find rotation point (minimum element)
func findRotationPoint(_ array: [Int]) -> Int? {
    guard !array.isEmpty else { return nil }

    var left = 0
    var right = array.count - 1

    while left < right {
        let mid = left + (right - left) / 2

        if array[mid] > array[right] {
            left = mid + 1
        } else {
            right = mid
        }
    }

    return left
}

// ==============================================================================
// 4. EXPONENTIAL SEARCH
// ==============================================================================

/// Exponential search - efficient for unbounded arrays
func exponentialSearch<T: Comparable>(_ array: [T], target: T) -> Int? {
    guard !array.isEmpty else { return nil }

    if array[0] == target {
        return 0
    }

    // Find range for binary search
    var i = 1
    while i < array.count && array[i] <= target {
        i *= 2
    }

    // Binary search in found range
    let left = i / 2
    let right = min(i, array.count - 1)

    return binarySearchRecursiveHelper(array, target: target, left: left, right: right)
}

// ==============================================================================
// 5. INTERPOLATION SEARCH
// ==============================================================================

/// Interpolation search - better for uniformly distributed data
///
/// Time Complexity: O(log log n) average, O(n) worst
func interpolationSearch(_ array: [Int], target: Int) -> Int? {
    guard !array.isEmpty else { return nil }

    var left = 0
    var right = array.count - 1

    while left <= right && target >= array[left] && target <= array[right] {
        if left == right {
            return array[left] == target ? left : nil
        }

        // Interpolation formula
        let pos = left + ((target - array[left]) * (right - left)) / (array[right] - array[left])

        // Ensure pos is within bounds
        let safePoz = max(left, min(pos, right))

        if array[safePoz] == target {
            return safePoz
        } else if array[safePoz] < target {
            left = safePoz + 1
        } else {
            right = safePoz - 1
        }
    }

    return nil
}

// ==============================================================================
// 6. TERNARY SEARCH
// ==============================================================================

/// Ternary search - divides array into three parts
func ternarySearch<T: Comparable>(_ array: [T], target: T) -> Int? {
    guard !array.isEmpty else { return nil }

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

/// Ternary search for finding maximum of unimodal function
func ternarySearchMaximum(
    function: (Double) -> Double,
    left: Double,
    right: Double,
    epsilon: Double = 1e-9
) -> Double {
    var l = left
    var r = right

    while r - l > epsilon {
        let mid1 = l + (r - l) / 3.0
        let mid2 = r - (r - l) / 3.0

        if function(mid1) < function(mid2) {
            l = mid1
        } else {
            r = mid2
        }
    }

    return (l + r) / 2.0
}

// ==============================================================================
// 7. BINARY SEARCH ON ANSWER
// ==============================================================================

/// Binary search on answer space for optimization problems
func binarySearchOnAnswer(
    predicate: (Int) -> Bool,
    low: Int,
    high: Int
) -> Int? {
    var l = low
    var h = high
    var result: Int? = nil

    while l <= h {
        let mid = l + (h - l) / 2

        if predicate(mid) {
            result = mid
            h = mid - 1  // Try to find smaller answer
        } else {
            l = mid + 1
        }
    }

    return result
}

/// Find integer square root using binary search
func integerSquareRoot(_ n: Int) -> Int? {
    guard n >= 0 else { return nil }

    if n == 0 || n == 1 {
        return n
    }

    var left = 0
    var right = n
    var result = 0

    while left <= right {
        let mid = left + (right - left) / 2
        let square = mid * mid

        if square == n {
            return mid
        } else if square < n {
            result = mid
            left = mid + 1
        } else {
            right = mid - 1
        }
    }

    return result
}

/// Find square root with decimal precision
func squareRoot(_ n: Double, precision: Int = 2) -> Double? {
    guard n >= 0 else { return nil }

    if n == 0.0 || n == 1.0 {
        return n
    }

    var left = 0.0
    var right = n
    let epsilon = pow(10.0, Double(-precision))

    while right - left > epsilon {
        let mid = left + (right - left) / 2.0
        let square = mid * mid

        if abs(square - n) < epsilon {
            return mid
        } else if square < n {
            left = mid
        } else {
            right = mid
        }
    }

    return (left + right) / 2.0
}

// ==============================================================================
// 8. ADVANCED UTILITIES
// ==============================================================================

/// Find insertion position to maintain sorted order
func searchInsertPosition<T: Comparable>(_ array: [T], target: T) -> Int {
    guard !array.isEmpty else { return 0 }

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

/// Find element closest to target
func findClosest(_ array: [Int], target: Int) -> Int? {
    guard !array.isEmpty else { return nil }

    if array.count == 1 {
        return 0
    }

    if target <= array[0] {
        return 0
    }
    if target >= array[array.count - 1] {
        return array.count - 1
    }

    var left = 0
    var right = array.count - 1

    while left < right {
        let mid = left + (right - left) / 2

        if array[mid] == target {
            return mid
        } else if array[mid] < target {
            left = mid + 1
        } else {
            right = mid
        }
    }

    if left > 0 && abs(array[left - 1] - target) < abs(array[left] - target) {
        return left - 1
    }

    return left
}

/// Find peak element (element greater than neighbors)
func findPeakElement(_ array: [Int]) -> Int? {
    guard !array.isEmpty else { return nil }

    if array.count == 1 {
        return 0
    }

    var left = 0
    var right = array.count - 1

    while left < right {
        let mid = left + (right - left) / 2

        if array[mid] < array[mid + 1] {
            left = mid + 1
        } else {
            right = mid
        }
    }

    return left
}

// ==============================================================================
// DEMONSTRATION AND TESTING
// ==============================================================================

func printSeparator(_ title: String) {
    print("\n\(title)")
    print(String(repeating: "-", count: 50))
}

func demonstrateClassicBinarySearch() {
    printSeparator("1. CLASSIC BINARY SEARCH")

    let array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    let targets = [7, 10, 1, 19]

    for target in targets {
        let idxIter = binarySearchIterative(array, target: target)
        let idxRec = binarySearchRecursive(array, target: target)
        print("Search \(String(format: "%2d", target)): Iterative=\(idxIter ?? -1), Recursive=\(idxRec ?? -1)")
    }
}

func demonstrateFirstLastOccurrence() {
    printSeparator("2. FIRST/LAST OCCURRENCE")

    let array = [1, 2, 2, 2, 3, 4, 4, 4, 4, 5]
    let targets = [2, 4, 6]

    for target in targets {
        let first = findFirstOccurrence(array, target: target)
        let last = findLastOccurrence(array, target: target)
        let count = countOccurrences(array, target: target)
        print("Target \(target): First=\(first ?? -1), Last=\(last ?? -1), Count=\(count)")
    }
}

func demonstrateRotatedArraySearch() {
    printSeparator("3. ROTATED ARRAY SEARCH")

    let rotated = [4, 5, 6, 7, 0, 1, 2]
    let rotationPoint = findRotationPoint(rotated)!

    print("Rotated array: \(rotated)")
    print("Rotation point: \(rotationPoint) (value: \(rotated[rotationPoint]))")

    let targets = [0, 3, 6]
    for target in targets {
        let idx = searchRotatedArray(rotated, target: target)
        print("Search \(target): Index=\(idx ?? -1)")
    }
}

func demonstrateExponentialSearch() {
    printSeparator("4. EXPONENTIAL SEARCH")

    let largeArray = (0..<50).map { $0 * 2 + 1 }
    let targets = [15, 51, 99]

    for target in targets {
        let idx = exponentialSearch(largeArray, target: target)
        print("Search \(String(format: "%2d", target)) in array of size 50: Index=\(idx ?? -1)")
    }
}

func demonstrateInterpolationSearch() {
    printSeparator("5. INTERPOLATION SEARCH")

    let uniformArray = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    let targets = [30, 75, 100]

    for target in targets {
        let idx = interpolationSearch(uniformArray, target: target)
        print("Search \(String(format: "%3d", target)): Index=\(idx ?? -1)")
    }
}

func demonstrateTernarySearch() {
    printSeparator("6. TERNARY SEARCH")

    let array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    let targets = [5, 1, 10, 11]

    for target in targets {
        let idx = ternarySearch(array, target: target)
        print("Search \(String(format: "%2d", target)): Index=\(idx ?? -1)")
    }

    // Unimodal function
    let function: (Double) -> Double = { x in -(x - 5) * (x - 5) + 25 }
    let maxX = ternarySearchMaximum(function: function, left: 0, right: 10)
    print(String(format: "Maximum of -(x-5)² + 25 at x ≈ %.6f", maxX))
}

func demonstrateBinarySearchOnAnswer() {
    printSeparator("7. BINARY SEARCH ON ANSWER")

    let testNumbers = [16, 25, 50, 100]
    for n in testNumbers {
        let sqrtInt = integerSquareRoot(n)!
        let sqrtPrecise = squareRoot(Double(n), precision: 2)!
        print(String(format: "√%3d = %d (integer), %.2f (precise)", n, sqrtInt, sqrtPrecise))
    }
}

func demonstrateAdvancedUtilities() {
    printSeparator("8. ADVANCED UTILITIES")

    let array = [1, 3, 5, 6, 8, 10]
    let targets = [2, 5, 11]

    for target in targets {
        let pos = searchInsertPosition(array, target: target)
        print("Insert position for \(String(format: "%2d", target)): \(pos)")
    }

    let arrayClosest = [1, 3, 5, 7, 9]
    let targetsClosest = [4, 6, 8]

    for target in targetsClosest {
        let idx = findClosest(arrayClosest, target: target)!
        print("Closest to \(target): Index=\(idx), Value=\(arrayClosest[idx])")
    }

    let peakArray = [1, 3, 20, 4, 1, 0]
    let peak = findPeakElement(peakArray)!
    print("Peak element in \(peakArray): Index=\(peak), Value=\(peakArray[peak])")
}

// Main execution
print("======================================================================")
print("BINARY SEARCH ALGORITHM COLLECTION - SWIFT")
print("======================================================================")

demonstrateClassicBinarySearch()
demonstrateFirstLastOccurrence()
demonstrateRotatedArraySearch()
demonstrateExponentialSearch()
demonstrateInterpolationSearch()
demonstrateTernarySearch()
demonstrateBinarySearchOnAnswer()
demonstrateAdvancedUtilities()

print("\n======================================================================")
print("DEMONSTRATION COMPLETE")
print("======================================================================")
