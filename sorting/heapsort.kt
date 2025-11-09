/**
 * Heap Sort Algorithm Implementation in Kotlin
 *
 * Time Complexity: O(n log n) - consistently across all cases
 * Space Complexity: O(1) for in-place sorting, O(n) for auxiliary heap
 *
 * Heap Sort is a comparison-based sorting algorithm that uses a binary heap data
 * structure. It divides its input into a sorted and an unsorted region, and it
 * iteratively shrinks the unsorted region by extracting the largest element and
 * inserting it into the sorted region.
 *
 * Kotlin features:
 * - Generic functions and classes
 * - Data classes
 * - Extension functions
 * - Null safety
 * - Functional programming
 */

import kotlin.system.measureTimeMillis
import kotlin.random.Random

/**
 * Maintain the max-heap property for a subtree rooted at index i.
 *
 * Time Complexity: O(log n)
 */
fun <T : Comparable<T>> heapifyMax(arr: MutableList<T>, n: Int, i: Int) {
    var largest = i
    val left = 2 * i + 1
    val right = 2 * i + 2

    // Check if left child exists and is greater than root
    if (left < n && arr[left] > arr[largest]) {
        largest = left
    }

    // Check if right child exists and is greater than largest so far
    if (right < n && arr[right] > arr[largest]) {
        largest = right
    }

    // If largest is not root, swap and recursively heapify
    if (largest != i) {
        arr[i] = arr[largest].also { arr[largest] = arr[i] }
        heapifyMax(arr, n, largest)
    }
}

/**
 * Maintain the min-heap property for a subtree rooted at index i.
 *
 * Time Complexity: O(log n)
 */
fun <T : Comparable<T>> heapifyMin(arr: MutableList<T>, n: Int, i: Int) {
    var smallest = i
    val left = 2 * i + 1
    val right = 2 * i + 2

    if (left < n && arr[left] < arr[smallest]) {
        smallest = left
    }

    if (right < n && arr[right] < arr[smallest]) {
        smallest = right
    }

    if (smallest != i) {
        arr[i] = arr[smallest].also { arr[smallest] = arr[i] }
        heapifyMin(arr, n, smallest)
    }
}

/**
 * Build a max-heap from an unordered array.
 *
 * Time Complexity: O(n)
 */
fun <T : Comparable<T>> buildMaxHeap(arr: MutableList<T>) {
    val n = arr.size
    // Start from the last non-leaf node and heapify each node
    for (i in n / 2 - 1 downTo 0) {
        heapifyMax(arr, n, i)
    }
}

/**
 * Build a min-heap from an unordered array.
 *
 * Time Complexity: O(n)
 */
fun <T : Comparable<T>> buildMinHeap(arr: MutableList<T>) {
    val n = arr.size
    for (i in n / 2 - 1 downTo 0) {
        heapifyMin(arr, n, i)
    }
}

/**
 * Sort a list using heap sort algorithm.
 *
 * Time Complexity: O(n log n)
 */
fun <T : Comparable<T>> heapSort(arr: List<T>): List<T> {
    if (arr.size <= 1) {
        return arr.toList()
    }

    val result = arr.toMutableList()
    heapSortInPlace(result)
    return result
}

/**
 * Sort a list in-place using heap sort algorithm.
 *
 * Time Complexity: O(n log n)
 * Space Complexity: O(1)
 */
fun <T : Comparable<T>> heapSortInPlace(arr: MutableList<T>) {
    val n = arr.size

    // Build a max heap
    buildMaxHeap(arr)

    // Extract elements from heap one by one
    for (i in n - 1 downTo 1) {
        // Move current root to end
        arr[0] = arr[i].also { arr[i] = arr[0] }
        // Call heapify on the reduced heap
        heapifyMax(arr, i, 0)
    }
}

/**
 * Check if list is sorted in ascending order.
 */
fun <T : Comparable<T>> isSorted(arr: List<T>): Boolean {
    for (i in 0 until arr.size - 1) {
        if (arr[i] > arr[i + 1]) {
            return false
        }
    }
    return true
}

/**
 * Max-Heap data structure implementation.
 */
class MaxHeap<T : Comparable<T>>(initialData: List<T> = emptyList()) {
    private val heap: MutableList<T> = initialData.toMutableList()

    init {
        if (heap.isNotEmpty()) {
            buildHeap()
        }
    }

    private fun parent(i: Int) = (i - 1) / 2
    private fun left(i: Int) = 2 * i + 1
    private fun right(i: Int) = 2 * i + 2

    private fun buildHeap() {
        val n = heap.size
        for (i in n / 2 - 1 downTo 0) {
            heapifyDown(i)
        }
    }

    private fun bubbleUp(i: Int) {
        var index = i
        while (index > 0 && heap[parent(index)] < heap[index]) {
            val parentIndex = parent(index)
            heap[index] = heap[parentIndex].also { heap[parentIndex] = heap[index] }
            index = parentIndex
        }
    }

    private fun heapifyDown(i: Int) {
        var largest = i
        val left = left(i)
        val right = right(i)

        if (left < heap.size && heap[left] > heap[largest]) {
            largest = left
        }

        if (right < heap.size && heap[right] > heap[largest]) {
            largest = right
        }

        if (largest != i) {
            heap[i] = heap[largest].also { heap[largest] = heap[i] }
            heapifyDown(largest)
        }
    }

    /**
     * Insert a new key into the heap.
     *
     * Time Complexity: O(log n)
     */
    fun insert(key: T) {
        heap.add(key)
        bubbleUp(heap.size - 1)
    }

    /**
     * Remove and return the maximum element (root) from the heap.
     *
     * Time Complexity: O(log n)
     */
    fun extractMax(): T {
        require(heap.isNotEmpty()) { "extractMax from empty heap" }

        if (heap.size == 1) {
            return heap.removeAt(0)
        }

        val max = heap[0]
        heap[0] = heap.removeAt(heap.size - 1)
        heapifyDown(0)

        return max
    }

    /**
     * Get the maximum element without removing it.
     */
    fun getMax(): T {
        require(heap.isNotEmpty()) { "getMax from empty heap" }
        return heap[0]
    }

    /**
     * Increase the value of a key at index i.
     *
     * Time Complexity: O(log n)
     */
    fun increaseKey(i: Int, newKey: T) {
        require(i in heap.indices) { "Index $i out of bounds" }
        require(newKey >= heap[i]) { "New key is smaller than current key" }

        heap[i] = newKey
        bubbleUp(i)
    }

    /**
     * Decrease the value of a key at index i.
     *
     * Time Complexity: O(log n)
     */
    fun decreaseKey(i: Int, newKey: T) {
        require(i in heap.indices) { "Index $i out of bounds" }
        require(newKey <= heap[i]) { "New key is greater than current key" }

        heap[i] = newKey
        heapifyDown(i)
    }

    val size: Int
        get() = heap.size

    fun isEmpty(): Boolean = heap.isEmpty()

    fun toList(): List<T> = heap.toList()

    /**
     * Create ASCII art visualization of the heap.
     */
    fun visualize(): String {
        if (heap.isEmpty()) {
            return "Empty heap"
        }

        val lines = mutableListOf<String>()
        visualizeHelper(0, "", "", lines)
        return lines.joinToString("\n")
    }

    private fun visualizeHelper(i: Int, prefix: String, childPrefix: String, lines: MutableList<String>) {
        if (i >= heap.size) {
            return
        }

        lines.add("$prefix${heap[i]}")

        val leftIdx = left(i)
        val rightIdx = right(i)

        if (leftIdx < heap.size || rightIdx < heap.size) {
            if (leftIdx < heap.size) {
                if (rightIdx < heap.size) {
                    visualizeHelper(leftIdx, "$childPrefix├── ", "$childPrefix│   ", lines)
                } else {
                    visualizeHelper(leftIdx, "$childPrefix└── ", "$childPrefix    ", lines)
                }
            }

            if (rightIdx < heap.size) {
                visualizeHelper(rightIdx, "$childPrefix└── ", "$childPrefix    ", lines)
            }
        }
    }
}

/**
 * Min-Heap data structure implementation.
 */
class MinHeap<T : Comparable<T>>(initialData: List<T> = emptyList()) {
    private val heap: MutableList<T> = initialData.toMutableList()

    init {
        if (heap.isNotEmpty()) {
            buildHeap()
        }
    }

    private fun parent(i: Int) = (i - 1) / 2
    private fun left(i: Int) = 2 * i + 1
    private fun right(i: Int) = 2 * i + 2

    private fun buildHeap() {
        val n = heap.size
        for (i in n / 2 - 1 downTo 0) {
            heapifyDown(i)
        }
    }

    private fun bubbleUp(i: Int) {
        var index = i
        while (index > 0 && heap[parent(index)] > heap[index]) {
            val parentIndex = parent(index)
            heap[index] = heap[parentIndex].also { heap[parentIndex] = heap[index] }
            index = parentIndex
        }
    }

    private fun heapifyDown(i: Int) {
        var smallest = i
        val left = left(i)
        val right = right(i)

        if (left < heap.size && heap[left] < heap[smallest]) {
            smallest = left
        }

        if (right < heap.size && heap[right] < heap[smallest]) {
            smallest = right
        }

        if (smallest != i) {
            heap[i] = heap[smallest].also { heap[smallest] = heap[i] }
            heapifyDown(smallest)
        }
    }

    fun insert(key: T) {
        heap.add(key)
        bubbleUp(heap.size - 1)
    }

    fun extractMin(): T {
        require(heap.isNotEmpty()) { "extractMin from empty heap" }

        if (heap.size == 1) {
            return heap.removeAt(0)
        }

        val min = heap[0]
        heap[0] = heap.removeAt(heap.size - 1)
        heapifyDown(0)

        return min
    }

    fun getMin(): T {
        require(heap.isNotEmpty()) { "getMin from empty heap" }
        return heap[0]
    }

    val size: Int
        get() = heap.size

    fun isEmpty(): Boolean = heap.isEmpty()

    fun visualize(): String {
        if (heap.isEmpty()) {
            return "Empty heap"
        }

        val lines = mutableListOf<String>()
        visualizeHelper(0, "", "", lines)
        return lines.joinToString("\n")
    }

    private fun visualizeHelper(i: Int, prefix: String, childPrefix: String, lines: MutableList<String>) {
        if (i >= heap.size) {
            return
        }

        lines.add("$prefix${heap[i]}")

        val leftIdx = left(i)
        val rightIdx = right(i)

        if (leftIdx < heap.size || rightIdx < heap.size) {
            if (leftIdx < heap.size) {
                if (rightIdx < heap.size) {
                    visualizeHelper(leftIdx, "$childPrefix├── ", "$childPrefix│   ", lines)
                } else {
                    visualizeHelper(leftIdx, "$childPrefix└── ", "$childPrefix    ", lines)
                }
            }

            if (rightIdx < heap.size) {
                visualizeHelper(rightIdx, "$childPrefix└── ", "$childPrefix    ", lines)
            }
        }
    }
}

/**
 * Priority Queue implementation using a max-heap.
 */
class PriorityQueue<T : Comparable<T>> {
    private val heap = MaxHeap<T>()

    fun enqueue(item: T) {
        heap.insert(item)
    }

    fun dequeue(): T = heap.extractMax()

    fun peek(): T = heap.getMax()

    fun isEmpty(): Boolean = heap.isEmpty()

    val size: Int
        get() = heap.size
}

/**
 * Extension function to sort list using heap sort.
 */
fun <T : Comparable<T>> List<T>.heapSorted(): List<T> = heapSort(this)

/**
 * Demonstrate heap sort and heap data structure.
 */
fun demonstrateHeapSort() {
    println("🏔️  Heap Sort Implementation in Kotlin")
    println("=".repeat(60))

    // Test data
    val testCases = listOf(
        listOf(64, 34, 25, 12, 22, 11, 90) to "Random array",
        listOf(5, 2, 8, 6, 1, 9, 4) to "Small random array",
        listOf(1) to "Single element",
        emptyList<Int>() to "Empty array",
        listOf(3, 3, 3, 3, 3) to "All duplicates",
        listOf(9, 8, 7, 6, 5, 4, 3, 2, 1) to "Reverse sorted",
        listOf(1, 2, 3, 4, 5) to "Already sorted"
    )

    println("\n📋 Basic Sorting Tests:")
    println("-".repeat(60))

    for ((arr, desc) in testCases) {
        val original = arr
        val sortedArr = heapSort(arr)

        println("\nTest: $desc")
        println("Original: $original")
        println("Sorted:   $sortedArr")
        println("Correct:  ${if (isSorted(sortedArr)) "✓" else "✗"}")
    }

    println("\n" + "-".repeat(60))

    // Demonstrate heap visualization
    println("\n🌲 Heap Visualization:")
    println("-".repeat(60))

    val data = listOf(64, 34, 25, 12, 22, 11, 90)
    val maxHeap = MaxHeap(data)

    println("\nMax-Heap built from: $data")
    println(maxHeap.visualize())

    println("\nMin-Heap built from: $data")
    val minHeap = MinHeap(data)
    println(minHeap.visualize())

    // Demonstrate heap operations
    println("\n🔧 Heap Operations:")
    println("-".repeat(60))

    val heap = MaxHeap<Int>()
    val operations = listOf(50, 30, 70, 20, 40, 60, 80)

    println("\nInserting elements: $operations")
    for (val_ in operations) {
        heap.insert(val_)
        println("Inserted $val_, Max: ${heap.getMax()}")
    }

    println("\nHeap structure:")
    println(heap.visualize())

    println("\nExtracting elements:")
    val extracted = mutableListOf<Int>()
    while (!heap.isEmpty()) {
        val val_ = heap.extractMax()
        extracted.add(val_)
        println("Extracted: $val_")
    }

    println("Extraction order: $extracted")

    // Demonstrate priority queue
    println("\n📬 Priority Queue Demo:")
    println("-".repeat(60))

    val pq = PriorityQueue<Int>()
    val tasks = listOf(5, 1, 9, 3, 7)

    println("\nEnqueuing tasks with priorities: $tasks")
    for (priority in tasks) {
        pq.enqueue(priority)
        println("Enqueued priority $priority, Top priority: ${pq.peek()}")
    }

    println("\nProcessing tasks by priority:")
    while (!pq.isEmpty()) {
        val priority = pq.dequeue()
        println("Processing task with priority: $priority")
    }

    // Demonstrate extension function
    println("\n🔧 Extension Function:")
    println("-".repeat(60))
    val testList = listOf(5, 2, 8, 1, 9)
    println("Original: $testList")
    println("Sorted:   ${testList.heapSorted()}")
}

/**
 * Benchmark heap sort.
 */
fun performanceBenchmark() {
    println("\n\n⚡ Performance Benchmark")
    println("=".repeat(80))

    val sizes = listOf(100, 500, 1000, 5000, 10000)

    val patterns = mapOf(
        "Random" to { n: Int -> List(n) { Random.nextInt(1, 1001) } },
        "Sorted" to { n: Int -> List(n) { it } },
        "Reversed" to { n: Int -> List(n) { n - it } }
    )

    for ((patternName, patternGen) in patterns) {
        println("\n$patternName Data:")
        println("%-8s%15s%15s".format("Size", "Heap Sort", "sorted()"))
        println("-".repeat(38))

        for (size in sizes) {
            val testData = patternGen(size)
            print("%-8d".format(size))

            // Heap Sort
            var result: List<Int>
            val heapTime = measureTimeMillis {
                result = heapSort(testData)
            }
            print("%14.2fms".format(heapTime.toDouble()))

            // Kotlin sorted()
            val sortedTime = measureTimeMillis {
                testData.sorted()
            }
            println("%14.2fms".format(sortedTime.toDouble()))
        }
    }
}

/**
 * Test edge cases and error handling.
 */
fun testEdgeCases() {
    println("\n\n🧪 Edge Cases and Error Handling")
    println("=".repeat(60))

    println("\n1. Testing empty heap operations:")
    val heap1 = MaxHeap<Int>()
    try {
        heap1.extractMax()
        println("   ✗ Should have thrown exception")
    } catch (e: IllegalArgumentException) {
        println("   ✓ Correctly threw: ${e.message}")
    }

    println("\n2. Testing increaseKey with smaller value:")
    val heap2 = MaxHeap(listOf(10, 20, 30))
    try {
        heap2.increaseKey(0, 5)
        println("   ✗ Should have thrown exception")
    } catch (e: IllegalArgumentException) {
        println("   ✓ Correctly threw: ${e.message}")
    }

    println("\n3. Testing with duplicates:")
    val arr = listOf(5, 5, 5, 5, 5)
    val sorted = heapSort(arr)
    println("   Original: $arr")
    println("   Sorted:   $sorted")
    println("   Correct:  ${if (sorted == arr) "✓" else "✗"}")
}

fun main() {
    demonstrateHeapSort()
    performanceBenchmark()
    testEdgeCases()

    println("\n✨ Heap Sort demonstration complete!")
}
