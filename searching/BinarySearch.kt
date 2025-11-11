/**
 * Comprehensive Binary Search Algorithm Collection - Kotlin
 * ==========================================================
 *
 * A complete collection of binary search algorithms implemented
 * in Kotlin with language-specific features and extensions.
 *
 * Algorithms included:
 * 1. Classic Binary Search (iterative & recursive)
 * 2. First/Last Occurrence
 * 3. Rotated Sorted Array Search
 * 4. Exponential Search
 * 5. Interpolation Search
 * 6. Ternary Search
 * 7. Binary Search on Answer (optimization problems)
 * 8. Advanced Utilities
 *
 * Compilation: kotlinc BinarySearch.kt -include-runtime -d BinarySearch.jar
 * Usage: kotlin BinarySearch.jar
 * Or: kotlinc -script BinarySearch.kt
 */

// ============================================================================
// 1. CLASSIC BINARY SEARCH
// ============================================================================

/**
 * Classic binary search - Iterative implementation
 *
 * @param arr Sorted array/list
 * @param target Element to search for
 * @return Index of target, or -1 if not found
 *
 * Time: O(log n), Space: O(1)
 */
fun <T : Comparable<T>> binarySearchIterative(arr: List<T>, target: T): Int {
    var left = 0
    var right = arr.size - 1

    while (left <= right) {
        val mid = left + (right - left) / 2

        when {
            arr[mid] == target -> return mid
            arr[mid] < target -> left = mid + 1
            else -> right = mid - 1
        }
    }

    return -1
}

/**
 * Classic binary search - Recursive implementation
 *
 * Time: O(log n), Space: O(log n) due to recursion
 */
fun <T : Comparable<T>> binarySearchRecursive(
    arr: List<T>,
    target: T,
    left: Int = 0,
    right: Int = arr.size - 1
): Int {
    if (left > right) return -1

    val mid = left + (right - left) / 2

    return when {
        arr[mid] == target -> mid
        arr[mid] < target -> binarySearchRecursive(arr, target, mid + 1, right)
        else -> binarySearchRecursive(arr, target, left, mid - 1)
    }
}

/**
 * Binary search with custom comparator
 *
 * @param arr Sorted array/list
 * @param target Element to search for
 * @param comparator Custom comparison function
 * @return Index of target, or -1 if not found
 */
fun <T> binarySearchWithComparator(
    arr: List<T>,
    target: T,
    comparator: Comparator<T>
): Int {
    var left = 0
    var right = arr.size - 1

    while (left <= right) {
        val mid = left + (right - left) / 2
        val cmp = comparator.compare(arr[mid], target)

        when {
            cmp == 0 -> return mid
            cmp < 0 -> left = mid + 1
            else -> right = mid - 1
        }
    }

    return -1
}

// ============================================================================
// 2. FIRST/LAST OCCURRENCE (for arrays with duplicates)
// ============================================================================

/**
 * Find first occurrence of target in sorted array
 *
 * Time: O(log n), Space: O(1)
 */
fun <T : Comparable<T>> findFirstOccurrence(arr: List<T>, target: T): Int {
    var left = 0
    var right = arr.size - 1
    var result = -1

    while (left <= right) {
        val mid = left + (right - left) / 2

        when {
            arr[mid] == target -> {
                result = mid
                right = mid - 1  // Continue searching left
            }
            arr[mid] < target -> left = mid + 1
            else -> right = mid - 1
        }
    }

    return result
}

/**
 * Find last occurrence of target in sorted array
 *
 * Time: O(log n), Space: O(1)
 */
fun <T : Comparable<T>> findLastOccurrence(arr: List<T>, target: T): Int {
    var left = 0
    var right = arr.size - 1
    var result = -1

    while (left <= right) {
        val mid = left + (right - left) / 2

        when {
            arr[mid] == target -> {
                result = mid
                left = mid + 1  // Continue searching right
            }
            arr[mid] < target -> left = mid + 1
            else -> right = mid - 1
        }
    }

    return result
}

/**
 * Count occurrences of target in sorted array
 *
 * Time: O(log n), Space: O(1)
 */
fun <T : Comparable<T>> countOccurrences(arr: List<T>, target: T): Int {
    val first = findFirstOccurrence(arr, target)
    if (first == -1) return 0

    val last = findLastOccurrence(arr, target)
    return last - first + 1
}

/**
 * Find range [first, last] of target occurrences
 *
 * @return Pair of (first, last) indices, or (-1, -1) if not found
 */
fun <T : Comparable<T>> findRange(arr: List<T>, target: T): Pair<Int, Int> {
    val first = findFirstOccurrence(arr, target)
    if (first == -1) return Pair(-1, -1)

    val last = findLastOccurrence(arr, target)
    return Pair(first, last)
}

// ============================================================================
// 3. ROTATED SORTED ARRAY SEARCH
// ============================================================================

/**
 * Search in rotated sorted array
 *
 * Example: [4, 5, 6, 7, 0, 1, 2] (rotated from [0, 1, 2, 4, 5, 6, 7])
 *
 * Time: O(log n), Space: O(1)
 */
fun <T : Comparable<T>> searchRotatedArray(arr: List<T>, target: T): Int {
    var left = 0
    var right = arr.size - 1

    while (left <= right) {
        val mid = left + (right - left) / 2

        if (arr[mid] == target) {
            return mid
        }

        // Determine which half is sorted
        if (arr[left] <= arr[mid]) {
            // Left half is sorted
            if (arr[left] <= target && target < arr[mid]) {
                right = mid - 1
            } else {
                left = mid + 1
            }
        } else {
            // Right half is sorted
            if (arr[mid] < target && target <= arr[right]) {
                left = mid + 1
            } else {
                right = mid - 1
            }
        }
    }

    return -1
}

/**
 * Find rotation point (minimum element) in rotated sorted array
 *
 * Time: O(log n), Space: O(1)
 */
fun <T : Comparable<T>> findRotationPoint(arr: List<T>): Int {
    var left = 0
    var right = arr.size - 1

    while (left < right) {
        val mid = left + (right - left) / 2

        if (arr[mid] > arr[right]) {
            // Minimum is in right half
            left = mid + 1
        } else {
            // Minimum is in left half (or mid)
            right = mid
        }
    }

    return left
}

// ============================================================================
// 4. EXPONENTIAL SEARCH
// ============================================================================

/**
 * Exponential search - finds range then applies binary search
 *
 * Time: O(log n), Space: O(1)
 */
fun <T : Comparable<T>> exponentialSearch(arr: List<T>, target: T): Int {
    val n = arr.size

    if (n == 0) return -1
    if (arr[0] == target) return 0

    // Find range for binary search
    var i = 1
    while (i < n && arr[i] <= target) {
        i *= 2
    }

    // Binary search in range [i/2, min(i, n-1)]
    var left = i / 2
    var right = minOf(i, n - 1)

    while (left <= right) {
        val mid = left + (right - left) / 2

        when {
            arr[mid] == target -> return mid
            arr[mid] < target -> left = mid + 1
            else -> right = mid - 1
        }
    }

    return -1
}

// ============================================================================
// 5. INTERPOLATION SEARCH
// ============================================================================

/**
 * Interpolation search for uniformly distributed numerical data
 *
 * Time: O(log log n) average, O(n) worst
 * Space: O(1)
 */
fun interpolationSearch(arr: List<Int>, target: Int): Int {
    var left = 0
    var right = arr.size - 1

    while (left <= right && target >= arr[left] && target <= arr[right]) {
        if (left == right) {
            return if (arr[left] == target) left else -1
        }

        // Interpolation formula
        val pos = left + ((target - arr[left]) * (right - left)) /
                (arr[right] - arr[left])

        when {
            arr[pos] == target -> return pos
            arr[pos] < target -> left = pos + 1
            else -> right = pos - 1
        }
    }

    return -1
}

// ============================================================================
// 6. TERNARY SEARCH
// ============================================================================

/**
 * Ternary search on sorted array
 *
 * Time: O(log₃ n) ≈ O(log n)
 * Space: O(1)
 */
fun <T : Comparable<T>> ternarySearch(arr: List<T>, target: T): Int {
    var left = 0
    var right = arr.size - 1

    while (left <= right) {
        val mid1 = left + (right - left) / 3
        val mid2 = right - (right - left) / 3

        when {
            arr[mid1] == target -> return mid1
            arr[mid2] == target -> return mid2
            target < arr[mid1] -> right = mid1 - 1
            target > arr[mid2] -> left = mid2 + 1
            else -> {
                left = mid1 + 1
                right = mid2 - 1
            }
        }
    }

    return -1
}

/**
 * Ternary search for finding maximum of unimodal function
 *
 * @param fn Unimodal function
 * @param left Left boundary
 * @param right Right boundary
 * @param precision Precision for convergence
 * @return x value where f(x) is maximum
 */
fun ternarySearchMaximum(
    fn: (Double) -> Double,
    leftBound: Double,
    rightBound: Double,
    precision: Double = 1e-6
): Double {
    var left = leftBound
    var right = rightBound

    while (right - left > precision) {
        val mid1 = left + (right - left) / 3.0
        val mid2 = right - (right - left) / 3.0

        if (fn(mid1) < fn(mid2)) {
            left = mid1
        } else {
            right = mid2
        }
    }

    return (left + right) / 2.0
}

// ============================================================================
// 7. BINARY SEARCH ON ANSWER (Optimization Problems)
// ============================================================================

/**
 * Binary search on answer space with predicate function
 *
 * Finds smallest value in range where predicate returns true
 *
 * Time: O(log(range) * T) where T is predicate evaluation time
 */
fun binarySearchOnAnswer(
    predicate: (Int) -> Boolean,
    left: Int,
    right: Int
): Int {
    var l = left
    var r = right
    var result = right + 1

    while (l <= r) {
        val mid = l + (r - l) / 2

        if (predicate(mid)) {
            result = mid
            r = mid - 1  // Try to find smaller answer
        } else {
            l = mid + 1
        }
    }

    return result
}

/**
 * Find integer square root using binary search
 *
 * Time: O(log n), Space: O(1)
 */
fun findSquareRoot(n: Int): Int {
    require(n >= 0) { "Square root of negative number" }
    if (n <= 1) return n

    var left = 1
    var right = n / 2
    var result = 1

    while (left <= right) {
        val mid = left + (right - left) / 2
        val square = mid.toLong() * mid

        when {
            square == n.toLong() -> return mid
            square < n -> {
                result = mid
                left = mid + 1
            }
            else -> right = mid - 1
        }
    }

    return result
}

/**
 * Find square root with decimal precision
 *
 * Time: O(log(n/precision))
 */
fun findSquareRootDecimal(n: Double, precision: Double = 0.01): Double {
    require(n >= 0) { "Square root of negative number" }
    if (n <= 1) return n

    var left = 0.0
    var right = n

    while (right - left > precision) {
        val mid = (left + right) / 2.0
        val square = mid * mid

        when {
            kotlin.math.abs(square - n) < precision -> return mid
            square < n -> left = mid
            else -> right = mid
        }
    }

    return (left + right) / 2.0
}

// ============================================================================
// 8. ADVANCED UTILITIES
// ============================================================================

/**
 * Find insertion position for element in sorted array
 *
 * Time: O(log n), Space: O(1)
 */
fun <T : Comparable<T>> findInsertPosition(arr: List<T>, target: T): Int {
    var left = 0
    var right = arr.size

    while (left < right) {
        val mid = left + (right - left) / 2

        if (arr[mid] < target) {
            left = mid + 1
        } else {
            right = mid
        }
    }

    return left
}

/**
 * Find closest element to target in sorted array
 *
 * Time: O(log n), Space: O(1)
 */
fun findClosest(arr: List<Int>, target: Int): Int {
    if (arr.isEmpty()) return -1
    if (arr.size == 1) return 0

    var left = 0
    var right = arr.size - 1

    while (left < right - 1) {
        val mid = left + (right - left) / 2

        when {
            arr[mid] == target -> return mid
            arr[mid] < target -> left = mid
            else -> right = mid
        }
    }

    // Compare distances
    val leftDist = kotlin.math.abs(arr[left] - target)
    val rightDist = kotlin.math.abs(arr[right] - target)

    return if (leftDist <= rightDist) left else right
}

/**
 * Find peak element in array
 *
 * Time: O(log n), Space: O(1)
 */
fun <T : Comparable<T>> findPeakElement(arr: List<T>): Int {
    if (arr.isEmpty()) return -1
    if (arr.size == 1) return 0

    var left = 0
    var right = arr.size - 1

    while (left < right) {
        val mid = left + (right - left) / 2

        if (arr[mid] < arr[mid + 1]) {
            // Peak is on right
            left = mid + 1
        } else {
            // Peak is on left or mid
            right = mid
        }
    }

    return left
}

// ============================================================================
// EXAMPLES AND TESTING
// ============================================================================

fun printSeparator() {
    println("=".repeat(70))
}

fun main() {
    printSeparator()
    println("BINARY SEARCH ALGORITHM COLLECTION - KOTLIN")
    printSeparator()
    println()

    // Example 1: Classic Binary Search
    printSeparator()
    println("EXAMPLE 1: Classic Binary Search")
    printSeparator()

    val arr = listOf(1, 3, 5, 7, 9, 11, 13, 15, 17, 19)
    println("Array: $arr")
    println("Search for 7: index ${binarySearchIterative(arr, 7)}")
    println("Search for 11: index ${binarySearchRecursive(arr, 11)}")
    println("Search for 20: index ${binarySearchIterative(arr, 20)}")
    println()

    // Example 2: First/Last Occurrence
    printSeparator()
    println("EXAMPLE 2: First/Last Occurrence (Duplicates)")
    printSeparator()

    val arrDup = listOf(1, 2, 2, 2, 3, 4, 4, 5, 5, 5, 5)
    println("Array: $arrDup")
    println("First occurrence of 2: index ${findFirstOccurrence(arrDup, 2)}")
    println("Last occurrence of 2: index ${findLastOccurrence(arrDup, 2)}")
    println("Count of 5: ${countOccurrences(arrDup, 5)}")

    val (first, last) = findRange(arrDup, 4)
    println("Range of 4: [$first, $last]")
    println()

    // Example 3: Rotated Sorted Array
    printSeparator()
    println("EXAMPLE 3: Rotated Sorted Array")
    printSeparator()

    val rotated = listOf(4, 5, 6, 7, 0, 1, 2)
    println("Array: $rotated")
    println("Search for 0: index ${searchRotatedArray(rotated, 0)}")
    println("Search for 5: index ${searchRotatedArray(rotated, 5)}")
    println("Rotation point: index ${findRotationPoint(rotated)}")
    println()

    // Example 4: Square Root
    printSeparator()
    println("EXAMPLE 4: Square Root using Binary Search")
    printSeparator()

    println("√50 (integer): ${findSquareRoot(50)}")
    println("√50 (decimal): ${"%.2f".format(findSquareRootDecimal(50.0, 0.01))}")
    println("√100: ${findSquareRoot(100)}")
    println()

    // Example 5: Binary Search on Answer
    printSeparator()
    println("EXAMPLE 5: Binary Search on Answer - Ship Packages")
    printSeparator()

    val weights = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    val days = 5

    val canShip = { capacity: Int ->
        var dayCount = 1
        var currentWeight = 0

        for (w in weights) {
            if (currentWeight + w > capacity) {
                dayCount++
                currentWeight = w
            } else {
                currentWeight += w
            }
        }

        dayCount <= days
    }

    val minCapacity = binarySearchOnAnswer(canShip, 1, 55)

    println("Weights: $weights")
    println("Days: $days")
    println("Minimum ship capacity: $minCapacity")
    println()

    // Example 6: Peak Element
    printSeparator()
    println("EXAMPLE 6: Find Peak Element")
    printSeparator()

    val peaks = listOf(1, 3, 20, 4, 1, 0)
    val peakIdx = findPeakElement(peaks)

    println("Array: $peaks")
    println("Peak at index $peakIdx, value: ${peaks[peakIdx]}")
    println()

    printSeparator()
    println("All examples completed!")
    printSeparator()
}
