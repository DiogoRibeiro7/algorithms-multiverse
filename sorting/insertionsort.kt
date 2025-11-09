// Insertion Sort Algorithm Implementation in Kotlin
//
// Time Complexity:
// - Best Case: O(n) - when array is already sorted
// - Average Case: O(n²)
// - Worst Case: O(n²) - when array is reverse sorted
// Space Complexity: O(1) for in-place, O(n) for functional approach
//
// Insertion Sort builds the final sorted array one item at a time.
//
// Kotlin features:
// - Generic functions with reified type parameters
// - Extension functions on collections
// - Data classes and destructuring
// - Higher-order functions and lambdas
// - Null safety

package sorting

import kotlin.system.measureTimeMillis
import kotlin.random.Random

// MARK: - Basic Insertion Sort

/**
 * Performs standard insertion sort.
 *
 * Time Complexity: O(n²) average and worst case, O(n) best case
 * Space Complexity: O(n) for the new list
 *
 * Example visualization:
 *   Initial: [5, 2, 8, 6, 1]
 *   Step 1:  [2, 5, 8, 6, 1]  // Insert 2
 *   Step 2:  [2, 5, 8, 6, 1]  // 8 already in place
 *   Step 3:  [2, 5, 6, 8, 1]  // Insert 6
 *   Step 4:  [1, 2, 5, 6, 8]  // Insert 1
 */
fun <T : Comparable<T>> insertionSort(arr: List<T>): List<T> {
    if (arr.size <= 1) return arr.toList()
    val result = arr.toMutableList()
    insertionSortInPlace(result)
    return result
}

/**
 * Sorts the list in-place using insertion sort.
 *
 * Time Complexity: O(n²) average and worst case, O(n) best case
 * Space Complexity: O(1)
 */
fun <T : Comparable<T>> insertionSortInPlace(arr: MutableList<T>) {
    for (i in 1 until arr.size) {
        val key = arr[i]
        var j = i - 1

        // Move elements greater than key one position ahead
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j]
            j--
        }

        arr[j + 1] = key
    }
}

/**
 * Insertion sort with custom comparator.
 */
fun <T> insertionSort(arr: List<T>, comparator: Comparator<T>): List<T> {
    if (arr.size <= 1) return arr.toList()
    val result = arr.toMutableList()

    for (i in 1 until result.size) {
        val key = result[i]
        var j = i - 1

        while (j >= 0 && comparator.compare(key, result[j]) < 0) {
            result[j + 1] = result[j]
            j--
        }

        result[j + 1] = key
    }

    return result
}

// MARK: - Recursive Insertion Sort

/**
 * Performs recursive insertion sort.
 *
 * Time Complexity: O(n²)
 * Space Complexity: O(n) for recursion stack
 */
fun <T : Comparable<T>> insertionSortRecursive(arr: List<T>): List<T> {
    if (arr.size <= 1) return arr.toList()
    val result = arr.toMutableList()
    insertionSortRecursiveHelper(result, result.size)
    return result
}

private fun <T : Comparable<T>> insertionSortRecursiveHelper(arr: MutableList<T>, n: Int) {
    // Base case
    if (n <= 1) return

    // Sort first n-1 elements
    insertionSortRecursiveHelper(arr, n - 1)

    // Insert last element at its correct position
    val key = arr[n - 1]
    var j = n - 2

    while (j >= 0 && arr[j] > key) {
        arr[j + 1] = arr[j]
        j--
    }

    arr[j + 1] = key
}

// MARK: - Binary Insertion Sort

/**
 * Uses binary search to find insertion position.
 *
 * Time Complexity: O(n²) for moves, O(n log n) for comparisons
 * Space Complexity: O(n)
 */
fun <T : Comparable<T>> binaryInsertionSort(arr: List<T>): List<T> {
    if (arr.size <= 1) return arr.toList()
    val result = arr.toMutableList()

    for (i in 1 until result.size) {
        val key = result[i]

        // Find position using binary search
        val pos = binarySearchPosition(result, 0, i - 1, key)

        // Shift elements to make space
        for (j in i - 1 downTo pos) {
            result[j + 1] = result[j]
        }

        result[pos] = key
    }

    return result
}

private fun <T : Comparable<T>> binarySearchPosition(
    arr: List<T>,
    left: Int,
    right: Int,
    key: T
): Int {
    if (right <= left) {
        return if (key > arr[left]) left + 1 else left
    }

    val mid = (left + right) / 2

    return when {
        key == arr[mid] -> mid + 1
        key > arr[mid] -> binarySearchPosition(arr, mid + 1, right, key)
        else -> binarySearchPosition(arr, left, mid - 1, key)
    }
}

// MARK: - Shell Sort

/**
 * Performs shell sort (generalization of insertion sort).
 *
 * Time Complexity: Depends on gap sequence (O(n log²n) for good sequences)
 * Space Complexity: O(n)
 */
fun <T : Comparable<T>> shellSort(arr: List<T>): List<T> {
    if (arr.size <= 1) return arr.toList()
    val result = arr.toMutableList()
    val n = result.size

    // Start with a large gap, then reduce (Knuth's sequence)
    var gap = 1
    while (gap < n / 3) {
        gap = 3 * gap + 1
    }

    // Perform gapped insertion sort
    while (gap > 0) {
        for (i in gap until n) {
            val key = result[i]
            var j = i

            // Insertion sort with gap
            while (j >= gap && result[j - gap] > key) {
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

/**
 * Tracks sorting operations
 */
data class SortStatistics(
    var comparisons: Int = 0,
    var swaps: Int = 0
) {
    fun reset() {
        comparisons = 0
        swaps = 0
    }

    override fun toString(): String {
        return "Comparisons: $comparisons, Swaps: $swaps"
    }
}

/**
 * Insertion sort with statistics tracking
 */
fun <T : Comparable<T>> insertionSortWithStats(arr: List<T>, stats: SortStatistics): List<T> {
    stats.reset()
    if (arr.size <= 1) return arr.toList()
    val result = arr.toMutableList()

    for (i in 1 until result.size) {
        val key = result[i]
        var j = i - 1

        while (j >= 0) {
            stats.comparisons++
            if (result[j] > key) {
                result[j + 1] = result[j]
                stats.swaps++
                j--
            } else {
                break
            }
        }

        result[j + 1] = key
    }

    return result
}

// MARK: - Visualization

/**
 * Creates a step-by-step visualization of insertion sort
 */
fun visualizeInsertionSort(arr: List<Int>): List<String> {
    val steps = mutableListOf<String>()
    val result = arr.toMutableList()

    steps.add("Initial: $result")

    for (i in 1 until result.size) {
        val key = result[i]
        var j = i - 1

        steps.add("\nStep $i: Inserting $key")
        steps.add("  Before: $result")

        while (j >= 0 && result[j] > key) {
            result[j + 1] = result[j]
            j--
        }

        result[j + 1] = key
        steps.add("  After:  $result")
    }

    steps.add("\nFinal: $result")
    return steps
}

// MARK: - Stability Demonstration

/**
 * Demonstrates that insertion sort is stable
 */
fun demonstrateStability() {
    data class Pair(val value: Int, val originalIndex: Int)

    val data = listOf(
        Pair(3, 0),
        Pair(1, 1),
        Pair(3, 2),
        Pair(2, 3),
        Pair(3, 4)
    )

    // Sort by value only
    val sorted = insertionSort(data, compareBy { it.value })

    println("Stability Demonstration:")
    print("Original: ")
    data.forEach { print("(${it.value},${it.originalIndex}) ") }
    println()

    print("Sorted:   ")
    sorted.forEach { print("(${it.value},${it.originalIndex}) ") }
    println()

    // Check stability - all 3's should maintain original order
    val threeIndices = sorted.filter { it.value == 3 }.map { it.originalIndex }
    val isStable = threeIndices == listOf(0, 2, 4)
    println("Stable: $isStable (indices of 3's: $threeIndices)")
}

// MARK: - Extension Functions

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
 * Extension function to sort a list using insertion sort
 */
fun <T : Comparable<T>> List<T>.insertionSorted(): List<T> {
    return insertionSort(this)
}

/**
 * Extension function to sort a mutable list in-place using insertion sort
 */
fun <T : Comparable<T>> MutableList<T>.insertionSort() {
    insertionSortInPlace(this)
}

// MARK: - Demonstration and Testing

fun demonstrateInsertionSort() {
    println("📝 Insertion Sort Implementation in Kotlin")
    println("=".repeat(60))

    // Test data
    data class TestCase(val arr: List<Int>, val desc: String)

    val testCases = listOf(
        TestCase(listOf(64, 34, 25, 12, 22, 11, 90), "Random array"),
        TestCase(listOf(5, 2, 8, 6, 1, 9, 4), "Small random array"),
        TestCase(listOf(1), "Single element"),
        TestCase(emptyList(), "Empty array"),
        TestCase(listOf(3, 3, 3, 3, 3), "All duplicates"),
        TestCase(listOf(9, 8, 7, 6, 5, 4, 3, 2, 1), "Reverse sorted"),
        TestCase(listOf(1, 2, 3, 4, 5), "Already sorted"),
        TestCase(listOf(1, 3, 2, 4, 5), "Nearly sorted")
    )

    println("\n📋 Basic Sorting Tests:")
    println("-".repeat(60))

    for (tc in testCases) {
        val standardResult = insertionSort(tc.arr)
        val binaryResult = binaryInsertionSort(tc.arr)
        val shellResult = shellSort(tc.arr)
        val recursiveResult = insertionSortRecursive(tc.arr)

        println("\nTest: ${tc.desc}")
        println("Original: ${tc.arr}")
        println("Sorted:   $standardResult")

        val allCorrect = standardResult.isSorted() && binaryResult.isSorted() &&
                shellResult.isSorted() && recursiveResult.isSorted()
        val allEqual = standardResult == binaryResult && standardResult == shellResult &&
                standardResult == recursiveResult

        val status = if (allCorrect && allEqual) "✓" else "✗"
        println("All implementations match: $status")
    }

    // Visualization demo
    println("\n\n🎬 Step-by-Step Visualization:")
    println("-".repeat(60))

    val demoArr = listOf(5, 2, 8, 6, 1)
    val steps = visualizeInsertionSort(demoArr)
    steps.forEach { println(it) }

    // Stability demonstration
    println("\n\n🔒 Stability Demonstration:")
    println("-".repeat(60))
    demonstrateStability()

    // Performance analysis
    println("\n\n📊 Operation Counting:")
    println("-".repeat(60))

    val statTestCases = listOf(
        TestCase(listOf(5, 2, 8, 6, 1), "Random"),
        TestCase(listOf(1, 2, 3, 4, 5), "Already sorted"),
        TestCase(listOf(5, 4, 3, 2, 1), "Reverse sorted")
    )

    for (tc in statTestCases) {
        val stats = SortStatistics()
        insertionSortWithStats(tc.arr, stats)

        val n = tc.arr.size
        println("\n${tc.desc}: ${tc.arr}")
        println("Array size (n): $n")
        println("Comparisons: ${stats.comparisons}")
        println("Swaps: ${stats.swaps}")
        println("Best case comparisons: ${n - 1}")
        println("Worst case comparisons: ${n * (n - 1) / 2}")
    }
}

// MARK: - Performance Benchmark

fun performanceBenchmark() {
    println("\n\n⚡ Performance Benchmark")
    println("=".repeat(80))
    println("\nInsertion sort is preferred for:")
    println("  • Small arrays (typically n < 10-20)")
    println("  • Nearly sorted arrays")
    println("  • As part of hybrid sorting algorithms")
    println()

    val sizes = listOf(5, 10, 20, 50, 100, 500, 1000)

    val patterns = mapOf<String, (Int) -> List<Int>>(
        "Random" to { n ->
            List(n) { Random.nextInt(1, 1001) }
        },
        "Nearly Sorted" to { n ->
            val arr = (0 until n).toMutableList()
            repeat(minOf(5, n / 10)) {
                val idx1 = Random.nextInt(n)
                val idx2 = Random.nextInt(n)
                val temp = arr[idx1]
                arr[idx1] = arr[idx2]
                arr[idx2] = temp
            }
            arr
        },
        "Reversed" to { n ->
            (0 until n).reversed()
        }
    )

    for ((patternName, patternGen) in patterns) {
        println("\n$patternName Data:")
        println("%-8s%15s%15s%15s%15s".format("Size", "Insertion", "Binary", "Shell", "sorted()"))
        println("-".repeat(68))

        for (size in sizes) {
            val testData = patternGen(size)
            print("%-8d".format(size))

            // Insertion Sort
            var elapsed = measureTimeMillis {
                insertionSort(testData)
            }
            print("%14.3fms".format(elapsed.toDouble()))

            // Binary Insertion Sort
            elapsed = measureTimeMillis {
                binaryInsertionSort(testData)
            }
            print("%14.3fms".format(elapsed.toDouble()))

            // Shell Sort
            elapsed = measureTimeMillis {
                shellSort(testData)
            }
            print("%14.3fms".format(elapsed.toDouble()))

            // Kotlin sorted()
            elapsed = measureTimeMillis {
                testData.sorted()
            }
            println("%14.3fms".format(elapsed.toDouble()))
        }
    }
}

// MARK: - Main

fun main() {
    demonstrateInsertionSort()
    performanceBenchmark()

    println("\n✨ Insertion Sort demonstration complete!")
}
