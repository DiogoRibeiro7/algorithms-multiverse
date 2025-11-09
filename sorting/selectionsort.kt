// Selection Sort Algorithm - Educational Implementation (Kotlin)
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

package sorting

import kotlin.system.measureTimeMillis
import kotlin.random.Random

// ============================================================================
// STANDARD SELECTION SORT
// ============================================================================

/**
 * Standard selection sort implementation.
 *
 * ALGORITHM STEPS:
 * ===============
 * 1. Find the minimum element in the unsorted portion
 * 2. Swap it with the first element of the unsorted portion
 * 3. Move the boundary of sorted/unsorted portions one element to the right
 * 4. Repeat until the entire array is sorted
 *
 * Visual Example:
 * ==============
 * Initial: [64, 25, 12, 22, 11]
 *
 * Pass 1: Find min in [64, 25, 12, 22, 11] → 11
 *         Swap 64 ↔ 11
 *         Result: [11, 25, 12, 22, 64]
 *                  ^^^ sorted portion
 *
 * Pass 2: Find min in [25, 12, 22, 64] → 12
 *         Swap 25 ↔ 12
 *         Result: [11, 12, 25, 22, 64]
 *                  ^^^^^^^ sorted portion
 *
 * Time: O(n²), Space: O(n) for new list
 */
fun <T : Comparable<T>> selectionSort(arr: List<T>): List<T> {
    if (arr.size <= 1) return arr.toList()

    val result = arr.toMutableList()
    selectionSortInPlace(result)
    return result
}

/**
 * In-place selection sort implementation.
 *
 * DETAILED STEP-BY-STEP:
 * ======================
 * For each position i from 0 to n-1:
 *     - Assume arr[i] is the minimum
 *     - Scan all elements from i+1 to n-1
 *     - Track the index of the actual minimum element
 *     - After scanning, swap arr[i] with the minimum element found
 *
 * Time: O(n²), Space: O(1)
 */
fun <T : Comparable<T>> selectionSortInPlace(arr: MutableList<T>) {
    val n = arr.size

    // Outer loop: Move boundary of unsorted subarray one by one
    for (i in 0 until n - 1) {
        // Find the minimum element in the remaining unsorted array
        // Start by assuming the first unsorted element is the minimum
        var minIdx = i

        // Inner loop: Search for the minimum in arr[i+1...n-1]
        for (j in i + 1 until n) {
            // If we find a smaller element, update minIdx
            if (arr[j] < arr[minIdx]) {
                minIdx = j
            }
        }

        // Swap the found minimum element with the first element
        // of the unsorted portion
        if (minIdx != i) {
            val temp = arr[i]
            arr[i] = arr[minIdx]
            arr[minIdx] = temp
        }
    }
}

/**
 * Selection sort with custom comparator.
 */
fun <T> selectionSort(arr: List<T>, comparator: Comparator<T>): List<T> {
    if (arr.size <= 1) return arr.toList()

    val result = arr.toMutableList()
    val n = result.size

    for (i in 0 until n - 1) {
        var minIdx = i

        for (j in i + 1 until n) {
            if (comparator.compare(result[j], result[minIdx]) < 0) {
                minIdx = j
            }
        }

        if (minIdx != i) {
            val temp = result[i]
            result[i] = result[minIdx]
            result[minIdx] = temp
        }
    }

    return result
}

// ============================================================================
// BIDIRECTIONAL SELECTION SORT
// ============================================================================

/**
 * Bidirectional selection sort (also called "double selection sort").
 *
 * OPTIMIZATION:
 * ============
 * Instead of finding just the minimum in each pass, we find BOTH the minimum
 * and maximum elements. We place the minimum at the beginning and the maximum
 * at the end, reducing the number of passes by approximately half.
 *
 * Time: Still O(n²), but approximately 2x faster in practice
 */
fun <T : Comparable<T>> bidirectionalSelectionSort(arr: List<T>): List<T> {
    if (arr.size <= 1) return arr.toList()

    val result = arr.toMutableList()
    val n = result.size

    // Process from both ends toward the middle
    var left = 0
    var right = n - 1

    while (left < right) {
        // Find both minimum and maximum in the current range
        var minIdx = left
        var maxIdx = left

        for (i in left..right) {
            if (result[i] < result[minIdx]) {
                minIdx = i
            }
            if (result[i] > result[maxIdx]) {
                maxIdx = i
            }
        }

        // Handle special case: if min is at right position
        if (minIdx == right) {
            val temp = result[left]
            result[left] = result[right]
            result[right] = temp
            if (maxIdx == left) {
                maxIdx = right
            }
        } else {
            // Swap minimum to the left boundary
            if (minIdx != left) {
                val temp = result[left]
                result[left] = result[minIdx]
                result[minIdx] = temp
            }

            // If maximum was at left position, it's now at minIdx
            if (maxIdx == left) {
                maxIdx = minIdx
            }

            // Swap maximum to the right boundary
            if (maxIdx != right) {
                val temp = result[right]
                result[right] = result[maxIdx]
                result[maxIdx] = temp
            }
        }

        // Move boundaries inward
        left++
        right--
    }

    return result
}

// ============================================================================
// RECURSIVE SELECTION SORT
// ============================================================================

/**
 * Recursive implementation of selection sort.
 *
 * RECURSIVE APPROACH:
 * ==================
 * Base case: Array of size 0 or 1 is already sorted
 * Recursive case:
 *     1. Find the minimum element in the array
 *     2. Swap it with the first element
 *     3. Recursively sort the rest of the array (excluding the first element)
 *
 * Time: O(n²), Space: O(n) for recursion stack
 */
fun <T : Comparable<T>> selectionSortRecursive(arr: List<T>): List<T> {
    if (arr.size <= 1) return arr.toList()

    val result = arr.toMutableList()
    selectionSortRecursiveHelper(result, 0)
    return result
}

private fun <T : Comparable<T>> selectionSortRecursiveHelper(arr: MutableList<T>, startIdx: Int) {
    // Base case: if we've reached the end, we're done
    if (startIdx >= arr.size - 1) return

    // Find the minimum element in arr[startIdx...n-1]
    var minIdx = startIdx
    for (i in startIdx + 1 until arr.size) {
        if (arr[i] < arr[minIdx]) {
            minIdx = i
        }
    }

    // Swap the minimum with the element at startIdx
    if (minIdx != startIdx) {
        val temp = arr[startIdx]
        arr[startIdx] = arr[minIdx]
        arr[minIdx] = temp
    }

    // Recursively sort the rest
    selectionSortRecursiveHelper(arr, startIdx + 1)
}

// ============================================================================
// STABLE SELECTION SORT
// ============================================================================

/**
 * Stable version of selection sort.
 *
 * WHY STANDARD SELECTION SORT IS UNSTABLE:
 * ========================================
 * When we swap the minimum element with the first element of the unsorted
 * portion, we can change the relative order of equal elements.
 *
 * MAKING IT STABLE:
 * ================
 * Instead of swapping, we shift all elements and insert the minimum
 * at the correct position. This preserves the relative order.
 *
 * Time: O(n²) comparisons + O(n²) shifts
 */
fun <T : Comparable<T>> stableSelectionSort(arr: List<T>): List<T> {
    if (arr.size <= 1) return arr.toList()

    val result = arr.toMutableList()
    val n = result.size

    for (i in 0 until n - 1) {
        // Find minimum in unsorted portion
        var minIdx = i
        for (j in i + 1 until n) {
            if (result[j] < result[minIdx]) {
                minIdx = j
            }
        }

        // Instead of swapping, shift elements and insert
        if (minIdx != i) {
            val minValue = result[minIdx]
            // Shift all elements between i and minIdx one position right
            for (k in minIdx downTo i + 1) {
                result[k] = result[k - 1]
            }
            // Place minimum at position i
            result[i] = minValue
        }
    }

    return result
}

// ============================================================================
// VISUALIZATION AND STATISTICS
// ============================================================================

/**
 * Tracks sorting operations
 */
data class SortStatistics(
    var comparisons: Int = 0,
    var swaps: Int = 0,
    var arrayAccesses: Int = 0
) {
    fun reset() {
        comparisons = 0
        swaps = 0
        arrayAccesses = 0
    }

    override fun toString(): String {
        return "Comparisons: $comparisons, Swaps: $swaps, Array Accesses: $arrayAccesses"
    }
}

/**
 * Selection sort with operation counting
 */
fun <T : Comparable<T>> selectionSortWithStats(arr: List<T>, stats: SortStatistics): List<T> {
    stats.reset()
    if (arr.size <= 1) return arr.toList()

    val result = arr.toMutableList()
    val n = result.size

    for (i in 0 until n - 1) {
        var minIdx = i
        stats.arrayAccesses++

        for (j in i + 1 until n) {
            stats.comparisons++
            stats.arrayAccesses += 2  // Read result[j] and result[minIdx]
            if (result[j] < result[minIdx]) {
                minIdx = j
            }
        }

        if (minIdx != i) {
            stats.swaps++
            stats.arrayAccesses += 4  // Two reads, two writes
            val temp = result[i]
            result[i] = result[minIdx]
            result[minIdx] = temp
        }
    }

    return result
}

/**
 * Creates a step-by-step visualization of selection sort
 */
fun visualizeSelectionSort(arr: List<Int>): List<String> {
    val steps = mutableListOf<String>()
    val result = arr.toMutableList()

    steps.add("=".repeat(70))
    steps.add("SELECTION SORT VISUALIZATION")
    steps.add("=".repeat(70))
    steps.add("Initial array: $result")
    steps.add("")

    val n = result.size
    for (i in 0 until n - 1) {
        steps.add("Pass ${i + 1}:")
        val unsorted = result.subList(i, n)
        steps.add("  Looking for minimum in unsorted portion: $unsorted")

        var minIdx = i
        var minValue = result[i]

        // Show the search process
        for (j in i + 1 until n) {
            if (result[j] < minValue) {
                minIdx = j
                minValue = result[j]
                steps.add("    Found new minimum: $minValue at index $minIdx")
            }
        }

        // Show the swap
        if (minIdx != i) {
            steps.add("  Swapping ${result[i]} ↔ ${result[minIdx]}")
            val temp = result[i]
            result[i] = result[minIdx]
            result[minIdx] = temp
        } else {
            steps.add("  No swap needed (minimum already in place)")
        }

        // Show current state
        val sorted = result.subList(0, i + 1)
        val unsortedPart = if (i + 1 < n) result.subList(i + 1, n) else emptyList()
        steps.add("  Sorted: $sorted | Unsorted: $unsortedPart")
        steps.add("")
    }

    steps.add("Final sorted array: $result")
    steps.add("=".repeat(70))

    return steps
}

// ============================================================================
// EXTENSION FUNCTIONS
// ============================================================================

/**
 * Extension function to check if a list is sorted
 */
fun <T : Comparable<T>> List<T>.isSorted(): Boolean {
    for (i in 0 until size - 1) {
        if (this[i] > this[i + 1]) {
            return false
        }
    }
    return true
}

/**
 * Extension function to sort a list using selection sort
 */
fun <T : Comparable<T>> List<T>.selectionSorted(): List<T> {
    return selectionSort(this)
}

/**
 * Extension function to sort a mutable list in-place using selection sort
 */
fun <T : Comparable<T>> MutableList<T>.selectionSort() {
    selectionSortInPlace(this)
}

// ============================================================================
// DEMONSTRATION AND TESTING
// ============================================================================

fun demonstrateSelectionSort() {
    println("📚 SELECTION SORT - EDUCATIONAL DEMONSTRATION")
    println("=".repeat(80))

    // Test data
    data class TestCase(val arr: List<Int>, val desc: String)

    val testCases = listOf(
        TestCase(listOf(64, 25, 12, 22, 11), "Random array"),
        TestCase(listOf(5, 2, 8, 6, 1, 9, 4), "Small random array"),
        TestCase(listOf(1), "Single element"),
        TestCase(emptyList(), "Empty array"),
        TestCase(listOf(3, 3, 3, 3, 3), "All duplicates"),
        TestCase(listOf(9, 8, 7, 6, 5, 4, 3, 2, 1), "Reverse sorted"),
        TestCase(listOf(1, 2, 3, 4, 5), "Already sorted"),
        TestCase(listOf(1, 3, 2, 4, 5), "Nearly sorted")
    )

    println("\n📋 BASIC FUNCTIONALITY TESTS:")
    println("-".repeat(80))

    for (tc in testCases) {
        val standard = selectionSort(tc.arr)
        val bidirectional = bidirectionalSelectionSort(tc.arr)
        val recursive = selectionSortRecursive(tc.arr)
        val stable = stableSelectionSort(tc.arr)

        println("\nTest: ${tc.desc}")
        println("Original:      ${tc.arr}")
        println("Standard:      $standard")
        println("Bidirectional: $bidirectional")
        println("Recursive:     $recursive")
        println("Stable:        $stable")

        val allCorrect = standard.isSorted() && bidirectional.isSorted() &&
                recursive.isSorted() && stable.isSorted()

        val status = if (allCorrect) "✓" else "✗"
        println("All correct: $status")
    }

    // Visualization
    println("\n\n🎬 STEP-BY-STEP VISUALIZATION:")
    println("-".repeat(80))

    val demoArr = listOf(64, 25, 12, 22, 11)
    val steps = visualizeSelectionSort(demoArr)
    steps.forEach { println(it) }

    // Memory analysis
    println("\n\n💾 MEMORY USAGE ANALYSIS:")
    println("-".repeat(80))
    println("""

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

3. Kotlin-Specific:
   - Uses MutableList for in-place operations
   - toList() creates immutable copy
   - Extension functions for convenience
    """.trimIndent())

    println("\n📌 WHEN TO USE SELECTION SORT:")
    println("-".repeat(80))
    println("""

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
    """.trimIndent())
}

fun performanceBenchmark() {
    println("\n\n⚡ PERFORMANCE BENCHMARK")
    println("=".repeat(80))

    val sizes = listOf(10, 20, 50, 100, 200)

    val patterns = mapOf<String, (Int) -> List<Int>>(
        "Random" to { n -> List(n) { Random.nextInt(1, 1001) } },
        "Sorted" to { n -> (0 until n).toList() },
        "Reversed" to { n -> (0 until n).reversed() }
    )

    for ((patternName, patternGen) in patterns) {
        println("\n$patternName Data:")
        println("%-10s%15s%15s%15s".format("Size", "Standard", "Bidirectional", "Recursive"))
        println("-".repeat(55))

        for (size in sizes) {
            val testData = patternGen(size)
            print("%-10d".format(size))

            // Standard
            var elapsed = measureTimeMillis {
                selectionSort(testData)
            }
            print("%14.3fms".format(elapsed.toDouble()))

            // Bidirectional
            elapsed = measureTimeMillis {
                bidirectionalSelectionSort(testData)
            }
            print("%14.3fms".format(elapsed.toDouble()))

            // Recursive
            elapsed = measureTimeMillis {
                selectionSortRecursive(testData)
            }
            println("%14.3fms".format(elapsed.toDouble()))
        }
    }
}

// ============================================================================
// MAIN
// ============================================================================

fun main() {
    demonstrateSelectionSort()
    performanceBenchmark()

    println("\n✨ Selection Sort demonstration complete!")
}
