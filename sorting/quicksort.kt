/**
 * QuickSort Algorithm Implementation in Kotlin
 * 
 * Time Complexity:
 * - Best Case: O(n log n)
 * - Average Case: O(n log n)
 * - Worst Case: O(n²)
 * 
 * Space Complexity: O(log n) due to recursion stack
 * 
 * Kotlin features:
 * - Extension functions
 * - Higher-order functions
 * - Null safety
 * - Data classes and sealed classes
 * - Coroutines support
 */

import kotlin.random.Random
import kotlin.system.measureTimeMillis
import kotlinx.coroutines.*

/**
 * QuickSort implementation with multiple variants
 */
class QuickSort {
    companion object {
        /**
         * Sort array using QuickSort algorithm (returns new array)
         */
        fun <T : Comparable<T>> sort(array: Array<T>): Array<T> {
            val result = array.copyOf()
            sortInPlace(result, 0, result.size - 1)
            return result
        }
        
        /**
         * Sort array in-place using QuickSort algorithm
         */
        fun <T : Comparable<T>> sortInPlace(array: Array<T>, low: Int = 0, high: Int = array.size - 1) {
            if (low < high) {
                val pivotIndex = partition(array, low, high)
                sortInPlace(array, low, pivotIndex - 1)
                sortInPlace(array, pivotIndex + 1, high)
            }
        }
        
        /**
         * Partition the array around a pivot element
         */
        private fun <T : Comparable<T>> partition(array: Array<T>, low: Int, high: Int): Int {
            val pivot = array[high]
            var i = low - 1
            
            for (j in low until high) {
                if (array[j] <= pivot) {
                    i++
                    array.swap(i, j)
                }
            }
            
            array.swap(i + 1, high)
            return i + 1
        }
        
        /**
         * Iterative implementation to avoid stack overflow
         */
        fun <T : Comparable<T>> sortIterative(array: Array<T>) {
            if (array.size <= 1) return
            
            val stack = mutableListOf<Pair<Int, Int>>()
            stack.add(0 to array.size - 1)
            
            while (stack.isNotEmpty()) {
                val (low, high) = stack.removeAt(stack.size - 1)
                
                if (low < high) {
                    val pivotIndex = partition(array, low, high)
                    stack.add(low to pivotIndex - 1)
                    stack.add(pivotIndex + 1 to high)
                }
            }
        }
        
        /**
         * Randomized QuickSort for better average performance
         */
        fun <T : Comparable<T>> sortRandomized(array: Array<T>, low: Int = 0, high: Int = array.size - 1) {
            if (low < high) {
                // Random pivot selection
                val randomIndex = Random.nextInt(low, high + 1)
                array.swap(randomIndex, high)
                
                val pivotIndex = partition(array, low, high)
                sortRandomized(array, low, pivotIndex - 1)
                sortRandomized(array, pivotIndex + 1, high)
            }
        }
        
        /**
         * Three-way partitioning for arrays with many duplicates
         */
        fun <T : Comparable<T>> sort3Way(array: Array<T>, low: Int = 0, high: Int = array.size - 1) {
            if (low >= high) return
            
            val pivot = array[low]
            var lt = low
            var gt = high
            var i = low
            
            while (i <= gt) {
                when {
                    array[i] < pivot -> {
                        array.swap(lt, i)
                        lt++
                        i++
                    }
                    array[i] > pivot -> {
                        array.swap(i, gt)
                        gt--
                    }
                    else -> i++
                }
            }
            
            sort3Way(array, low, lt - 1)
            sort3Way(array, gt + 1, high)
        }
        
        /**
         * Functional-style QuickSort implementation
         */
        fun <T : Comparable<T>> sortFunctional(list: List<T>): List<T> {
            if (list.size <= 1) return list
            
            val pivot = list[list.size / 2]
            val less = list.filter { it < pivot }
            val equal = list.filter { it == pivot }
            val greater = list.filter { it > pivot }
            
            return sortFunctional(less) + equal + sortFunctional(greater)
        }
        
        /**
         * Sort with custom comparator
         */
        fun <T> sortWithComparator(array: Array<T>, comparator: Comparator<T>): Array<T> {
            val result = array.copyOf()
            sortWithComparatorInPlace(result, 0, result.size - 1, comparator)
            return result
        }
        
        private fun <T> sortWithComparatorInPlace(
            array: Array<T>, 
            low: Int, 
            high: Int, 
            comparator: Comparator<T>
        ) {
            if (low < high) {
                val pivotIndex = partitionWithComparator(array, low, high, comparator)
                sortWithComparatorInPlace(array, low, pivotIndex - 1, comparator)
                sortWithComparatorInPlace(array, pivotIndex + 1, high, comparator)
            }
        }
        
        private fun <T> partitionWithComparator(
            array: Array<T>, 
            low: Int, 
            high: Int, 
            comparator: Comparator<T>
        ): Int {
            val pivot = array[high]
            var i = low - 1
            
            for (j in low until high) {
                if (comparator.compare(array[j], pivot) <= 0) {
                    i++
                    array.swap(i, j)
                }
            }
            
            array.swap(i + 1, high)
            return i + 1
        }
        
        /**
         * Parallel QuickSort using coroutines
         */
        suspend fun <T : Comparable<T>> sortParallel(
            array: Array<T>, 
            low: Int = 0, 
            high: Int = array.size - 1,
            threshold: Int = 1000
        ) {
            if (low < high) {
                val pivotIndex = partition(array, low, high)
                
                if (high - low > threshold) {
                    // Use parallel processing for large subarrays
                    coroutineScope {
                        launch { sortParallel(array, low, pivotIndex - 1, threshold) }
                        launch { sortParallel(array, pivotIndex + 1, high, threshold) }
                    }
                } else {
                    // Use sequential processing for small subarrays
                    sortInPlace(array, low, pivotIndex - 1)
                    sortInPlace(array, pivotIndex + 1, high)
                }
            }
        }
    }
}

/**
 * Extension functions for arrays and lists
 */
fun <T : Comparable<T>> Array<T>.quickSort(): Array<T> = QuickSort.sort(this)

fun <T : Comparable<T>> Array<T>.quickSortInPlace() = QuickSort.sortInPlace(this)

fun <T : Comparable<T>> List<T>.quickSort(): List<T> = QuickSort.sortFunctional(this)

fun <T : Comparable<T>> Array<T>.isSorted(): Boolean {
    for (i in 0 until size - 1) {
        if (this[i] > this[i + 1]) return false
    }
    return true
}

fun <T> Array<T>.swap(i: Int, j: Int) {
    if (i != j) {
        val temp = this[i]
        this[i] = this[j]
        this[j] = temp
    }
}

/**
 * Utility class for QuickSort operations
 */
object QuickSortUtils {
    /**
     * Generate random array for testing
     */
    fun generateRandomArray(size: Int, range: IntRange = 1..1000): Array<Int> {
        return Array(size) { Random.nextInt(range.first, range.last + 1) }
    }
    
    /**
     * Benchmark sorting performance
     */
    fun <T : Comparable<T>> benchmark(
        array: Array<T>, 
        method: String = "standard"
    ): Long {
        val testArray = array.copyOf()
        
        return measureTimeMillis {
            when (method.lowercase()) {
                "standard" -> QuickSort.sortInPlace(testArray)
                "iterative" -> QuickSort.sortIterative(testArray)
                "randomized" -> QuickSort.sortRandomized(testArray)
                "3way" -> QuickSort.sort3Way(testArray)
                else -> throw IllegalArgumentException("Unknown method: $method")
            }
        }
    }
    
    /**
     * Pretty print array
     */
    fun <T> printArray(array: Array<T>, label: String = "") {
        if (label.isNotEmpty()) {
            print("$label: ")
        }
        println(array.contentToString())
    }
}

/**
 * Data class for performance results
 */
data class BenchmarkResult(
    val method: String,
    val arraySize: Int,
    val timeMs: Long,
    val isCorrect: Boolean
)

/**
 * Sealed class for different sorting strategies
 */
sealed class SortingStrategy {
    object Standard : SortingStrategy()
    object Iterative : SortingStrategy()
    object Randomized : SortingStrategy()
    object ThreeWay : SortingStrategy()
    object Functional : SortingStrategy()
    
    fun <T : Comparable<T>> sort(array: Array<T>): Array<T> {
        return when (this) {
            is Standard -> QuickSort.sort(array)
            is Iterative -> array.copyOf().also { QuickSort.sortIterative(it) }
            is Randomized -> array.copyOf().also { QuickSort.sortRandomized(it) }
            is ThreeWay -> array.copyOf().also { QuickSort.sort3Way(it) }
            is Functional -> QuickSort.sortFunctional(array.toList()).toTypedArray()
        }
    }
    
    override fun toString(): String = this::class.simpleName ?: "Unknown"
}

/**
 * QuickSort analyzer class
 */
class QuickSortAnalyzer {
    fun analyzePerformance(sizes: List<Int>, iterations: Int = 5): List<BenchmarkResult> {
        val results = mutableListOf<BenchmarkResult>()
        val strategies = listOf(
            SortingStrategy.Standard,
            SortingStrategy.Iterative,
            SortingStrategy.Randomized,
            SortingStrategy.ThreeWay
        )
        
        for (size in sizes) {
            println("Testing with $size elements:")
            
            for (strategy in strategies) {
                val times = mutableListOf<Long>()
                var isCorrect = true
                
                repeat(iterations) {
                    val testArray = QuickSortUtils.generateRandomArray(size)
                    val originalArray = testArray.copyOf()
                    
                    val time = measureTimeMillis {
                        val sorted = strategy.sort(testArray)
                        if (!sorted.isSorted()) isCorrect = false
                    }
                    times.add(time)
                }
                
                val avgTime = times.average().toLong()
                results.add(BenchmarkResult(strategy.toString(), size, avgTime, isCorrect))
                
                println("  ${strategy.toString().padEnd(12)}: ${avgTime}ms avg ${if (isCorrect) "✓" else "✗"}")
            }
            println()
        }
        
        return results
    }
}

/**
 * Demonstration and testing functions
 */
fun demonstrateQuickSort() {
    println("🚀 Kotlin QuickSort Implementation")
    println("=".repeat(40))
    
    // Test arrays
    val testArrays = listOf(
        arrayOf(64, 34, 25, 12, 22, 11, 90),
        arrayOf(5, 2, 8, 6, 1, 9, 4),
        arrayOf(1),
        arrayOf<Int>(),
        arrayOf(3, 3, 3, 3, 3),
        arrayOf(9, 8, 7, 6, 5, 4, 3, 2, 1)
    )
    
    println("\n📋 Basic Sorting Tests:")
    println("-".repeat(30))
    
    testArrays.forEachIndexed { index, array ->
        val original = array.copyOf()
        val sorted = array.quickSort()
        val isCorrect = sorted.isSorted()
        
        println("Test ${index + 1}:")
        QuickSortUtils.printArray(original, "Original")
        QuickSortUtils.printArray(sorted, "Sorted  ")
        println("Correct: ${if (isCorrect) "✓" else "✗"}")
        println("-".repeat(25))
    }
    
    // Advanced features demonstration
    println("\n🎯 Advanced Features:")
    println("-".repeat(25))
    
    // String sorting
    val words = arrayOf("banana", "apple", "cherry", "date", "elderberry")
    val sortedWords = words.quickSort()
    QuickSortUtils.printArray(words, "Original words")
    QuickSortUtils.printArray(sortedWords, "Sorted words  ")
    
    // Custom comparator (reverse order)
    val numbers = arrayOf(64, 34, 25, 12, 22, 11, 90)
    val reverseSorted = QuickSort.sortWithComparator(numbers) { a, b -> b.compareTo(a) }
    QuickSortUtils.printArray(numbers, "Original  ")
    QuickSortUtils.printArray(reverseSorted, "Reverse   ")
    
    // Functional approach with lists
    val numberList = listOf(9, 3, 7, 1, 5)
    val functionalSorted = numberList.quickSort()
    println("Original list:   $numberList")
    println("Functional sort: $functionalSorted")
    
    // Using extension functions
    val extArray = arrayOf(42, 17, 89, 3, 56)
    println("\nExtension functions:")
    QuickSortUtils.printArray(extArray, "Before")
    extArray.quickSortInPlace()
    QuickSortUtils.printArray(extArray, "After ")
}

suspend fun demonstrateParallelSort() {
    println("\n🔄 Parallel Sorting Demonstration:")
    println("-".repeat(35))
    
    val largeArray = QuickSortUtils.generateRandomArray(100000)
    val testArray1 = largeArray.copyOf()
    val testArray2 = largeArray.copyOf()
    
    // Sequential sort
    val sequentialTime = measureTimeMillis {
        QuickSort.sortInPlace(testArray1)
    }
    
    // Parallel sort
    val parallelTime = measureTimeMillis {
        runBlocking {
            QuickSort.sortParallel(testArray2)
        }
    }
    
    println("Array size: ${largeArray.size}")
    println("Sequential time: ${sequentialTime}ms")
    println("Parallel time:   ${parallelTime}ms")
    println("Speedup: ${sequentialTime.toDouble() / parallelTime}x")
    println("Both correct: ${testArray1.isSorted() && testArray2.isSorted()}")
}

fun performanceBenchmark() {
    println("\n⚡ Performance Benchmark")
    println("=".repeat(30))
    
    val analyzer = QuickSortAnalyzer()
    val sizes = listOf(1000, 5000, 10000)
    analyzer.analyzePerformance(sizes, iterations = 3)
}

fun testEdgeCases() {
    println("🧩 Edge Cases Testing")
    println("=".repeat(25))
    
    val edgeCases = mapOf(
        "Empty array" to arrayOf<Int>(),
        "Single element" to arrayOf(42),
        "Two elements" to arrayOf(2, 1),
        "Already sorted" to arrayOf(1, 2, 3, 4, 5),
        "Reverse sorted" to arrayOf(5, 4, 3, 2, 1),
        "All duplicates" to arrayOf(5, 5, 5, 5, 5)
    )
    
    edgeCases.forEach { (name, array) ->
        val sorted = array.quickSort()
        val isCorrect = sorted.isSorted()
        println("$name: ${if (isCorrect) "✓" else "✗"}")
    }
}

/**
 * Main function
 */
suspend fun main() {
    demonstrateQuickSort()
    demonstrateParallelSort()
    performanceBenchmark()
    testEdgeCases()
    
    println("\n✨ QuickSort demonstration complete!")
}
