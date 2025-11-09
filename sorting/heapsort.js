/**
 * Heap Sort Algorithm Implementation in JavaScript
 *
 * Time Complexity: O(n log n) - consistently across all cases
 * Space Complexity: O(1) for in-place sorting, O(n) for auxiliary heap
 *
 * Heap Sort is a comparison-based sorting algorithm that uses a binary heap data
 * structure. It divides its input into a sorted and an unsorted region, and it
 * iteratively shrinks the unsorted region by extracting the largest element and
 * inserting it into the sorted region.
 *
 * JavaScript features:
 * - ES6+ classes and syntax
 * - Generic heap implementation
 * - Priority queue
 * - Visual heap representation
 * - Comprehensive error handling
 */

/**
 * Maintain the max-heap property for a subtree rooted at index i.
 *
 * @template T
 * @param {T[]} arr - The array representing the heap
 * @param {number} n - Size of the heap
 * @param {number} i - Index of the root of the subtree
 *
 * Time Complexity: O(log n)
 */
function heapifyMax(arr, n, i) {
    let largest = i;
    const left = 2 * i + 1;
    const right = 2 * i + 2;

    // Check if left child exists and is greater than root
    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }

    // Check if right child exists and is greater than largest so far
    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }

    // If largest is not root, swap and recursively heapify
    if (largest !== i) {
        [arr[i], arr[largest]] = [arr[largest], arr[i]];
        heapifyMax(arr, n, largest);
    }
}

/**
 * Maintain the min-heap property for a subtree rooted at index i.
 *
 * @template T
 * @param {T[]} arr - The array representing the heap
 * @param {number} n - Size of the heap
 * @param {number} i - Index of the root of the subtree
 *
 * Time Complexity: O(log n)
 */
function heapifyMin(arr, n, i) {
    let smallest = i;
    const left = 2 * i + 1;
    const right = 2 * i + 2;

    // Check if left child exists and is smaller than root
    if (left < n && arr[left] < arr[smallest]) {
        smallest = left;
    }

    // Check if right child exists and is smaller than smallest so far
    if (right < n && arr[right] < arr[smallest]) {
        smallest = right;
    }

    // If smallest is not root, swap and recursively heapify
    if (smallest !== i) {
        [arr[i], arr[smallest]] = [arr[smallest], arr[i]];
        heapifyMin(arr, n, smallest);
    }
}

/**
 * Build a max-heap from an unordered array.
 *
 * @template T
 * @param {T[]} arr - Array to be converted into a max-heap
 *
 * Time Complexity: O(n)
 */
function buildMaxHeap(arr) {
    const n = arr.length;
    // Start from the last non-leaf node and heapify each node
    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
        heapifyMax(arr, n, i);
    }
}

/**
 * Build a min-heap from an unordered array.
 *
 * @template T
 * @param {T[]} arr - Array to be converted into a min-heap
 *
 * Time Complexity: O(n)
 */
function buildMinHeap(arr) {
    const n = arr.length;
    // Start from the last non-leaf node and heapify each node
    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
        heapifyMin(arr, n, i);
    }
}

/**
 * Sort an array using heap sort algorithm.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @returns {T[]} New sorted array
 *
 * Time Complexity: O(n log n)
 * Space Complexity: O(n) for the new array
 */
function heapSort(arr) {
    if (arr.length <= 1) {
        return [...arr];
    }

    const result = [...arr];
    heapSortInPlace(result);
    return result;
}

/**
 * Sort an array in-place using heap sort algorithm.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted in-place
 *
 * Time Complexity: O(n log n)
 * Space Complexity: O(1)
 */
function heapSortInPlace(arr) {
    const n = arr.length;

    // Build a max heap
    buildMaxHeap(arr);

    // Extract elements from heap one by one
    for (let i = n - 1; i > 0; i--) {
        // Move current root to end
        [arr[0], arr[i]] = [arr[i], arr[0]];
        // Call heapify on the reduced heap
        heapifyMax(arr, i, 0);
    }
}

/**
 * Sort an array in descending order using heap sort.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @returns {T[]} New sorted array in descending order
 *
 * Time Complexity: O(n log n)
 */
function heapSortDescending(arr) {
    if (arr.length <= 1) {
        return [...arr];
    }

    const result = [...arr];
    const n = result.length;

    // Build a min heap for descending order
    buildMinHeap(result);

    // Extract elements from heap one by one
    for (let i = n - 1; i > 0; i--) {
        [result[0], result[i]] = [result[i], result[0]];
        heapifyMin(result, i, 0);
    }

    return result;
}

/**
 * Max-Heap data structure implementation.
 *
 * A max-heap is a complete binary tree where each node is greater than or
 * equal to its children.
 *
 * @template T
 */
class MaxHeap {
    /**
     * Initialize the max-heap with optional initial data.
     * @param {T[]} [initialData] - Optional initial data
     */
    constructor(initialData = []) {
        this.heap = [...initialData];
        if (this.heap.length > 0) {
            buildMaxHeap(this.heap);
        }
    }

    /**
     * Get the parent index of node i.
     * @param {number} i - Node index
     * @returns {number} Parent index
     */
    parent(i) {
        return Math.floor((i - 1) / 2);
    }

    /**
     * Get the left child index of node i.
     * @param {number} i - Node index
     * @returns {number} Left child index
     */
    left(i) {
        return 2 * i + 1;
    }

    /**
     * Get the right child index of node i.
     * @param {number} i - Node index
     * @returns {number} Right child index
     */
    right(i) {
        return 2 * i + 2;
    }

    /**
     * Insert a new key into the heap.
     *
     * @param {T} key - Key to insert
     *
     * Time Complexity: O(log n)
     */
    insert(key) {
        // Add the new key at the end
        this.heap.push(key);
        // Fix the heap property if violated
        this._bubbleUp(this.heap.length - 1);
    }

    /**
     * Move the element at index i up to maintain heap property.
     * @private
     * @param {number} i - Index to bubble up
     */
    _bubbleUp(i) {
        while (i > 0 && this.heap[this.parent(i)] < this.heap[i]) {
            const parentIdx = this.parent(i);
            [this.heap[i], this.heap[parentIdx]] = [this.heap[parentIdx], this.heap[i]];
            i = parentIdx;
        }
    }

    /**
     * Remove and return the maximum element (root) from the heap.
     *
     * @returns {T} The maximum element
     * @throws {Error} If heap is empty
     *
     * Time Complexity: O(log n)
     */
    extractMax() {
        if (this.heap.length === 0) {
            throw new Error("extractMax from empty heap");
        }

        if (this.heap.length === 1) {
            return this.heap.pop();
        }

        // Store the maximum value
        const maxVal = this.heap[0];
        // Move the last element to root
        this.heap[0] = this.heap.pop();
        // Heapify the root
        heapifyMax(this.heap, this.heap.length, 0);

        return maxVal;
    }

    /**
     * Get the maximum element without removing it.
     *
     * @returns {T} The maximum element
     * @throws {Error} If heap is empty
     */
    getMax() {
        if (this.heap.length === 0) {
            throw new Error("getMax from empty heap");
        }
        return this.heap[0];
    }

    /**
     * Increase the value of a key at index i.
     *
     * @param {number} i - Index of the key to increase
     * @param {T} newKey - New value (must be greater than current value)
     * @throws {Error} If new key is smaller or index is invalid
     *
     * Time Complexity: O(log n)
     */
    increaseKey(i, newKey) {
        if (i < 0 || i >= this.heap.length) {
            throw new Error(`Index ${i} out of bounds`);
        }

        if (newKey < this.heap[i]) {
            throw new Error("New key is smaller than current key");
        }

        this.heap[i] = newKey;
        this._bubbleUp(i);
    }

    /**
     * Decrease the value of a key at index i.
     *
     * @param {number} i - Index of the key to decrease
     * @param {T} newKey - New value (must be smaller than current value)
     * @throws {Error} If new key is greater or index is invalid
     *
     * Time Complexity: O(log n)
     */
    decreaseKey(i, newKey) {
        if (i < 0 || i >= this.heap.length) {
            throw new Error(`Index ${i} out of bounds`);
        }

        if (newKey > this.heap[i]) {
            throw new Error("New key is greater than current key");
        }

        this.heap[i] = newKey;
        heapifyMax(this.heap, this.heap.length, i);
    }

    /**
     * Return the size of the heap.
     * @returns {number} Heap size
     */
    size() {
        return this.heap.length;
    }

    /**
     * Check if the heap is empty.
     * @returns {boolean} True if empty
     */
    isEmpty() {
        return this.heap.length === 0;
    }

    /**
     * Return a copy of the heap as an array.
     * @returns {T[]} Copy of the heap
     */
    toArray() {
        return [...this.heap];
    }

    /**
     * Create ASCII art visualization of the heap.
     *
     * @returns {string} String representation of the heap tree
     */
    visualize() {
        if (this.heap.length === 0) {
            return "Empty heap";
        }

        const lines = [];
        this._visualizeHelper(0, "", "", lines);
        return lines.join('\n');
    }

    /**
     * Helper method for visualizing the heap.
     * @private
     */
    _visualizeHelper(i, prefix, childPrefix, lines) {
        if (i >= this.heap.length) {
            return;
        }

        lines.push(prefix + this.heap[i]);

        const leftIdx = this.left(i);
        const rightIdx = this.right(i);

        if (leftIdx < this.heap.length || rightIdx < this.heap.length) {
            if (leftIdx < this.heap.length) {
                if (rightIdx < this.heap.length) {
                    this._visualizeHelper(leftIdx, childPrefix + "├── ", childPrefix + "│   ", lines);
                } else {
                    this._visualizeHelper(leftIdx, childPrefix + "└── ", childPrefix + "    ", lines);
                }
            }

            if (rightIdx < this.heap.length) {
                this._visualizeHelper(rightIdx, childPrefix + "└── ", childPrefix + "    ", lines);
            }
        }
    }
}

/**
 * Min-Heap data structure implementation.
 *
 * A min-heap is a complete binary tree where each node is less than or
 * equal to its children.
 *
 * @template T
 */
class MinHeap {
    /**
     * Initialize the min-heap with optional initial data.
     * @param {T[]} [initialData] - Optional initial data
     */
    constructor(initialData = []) {
        this.heap = [...initialData];
        if (this.heap.length > 0) {
            buildMinHeap(this.heap);
        }
    }

    parent(i) {
        return Math.floor((i - 1) / 2);
    }

    left(i) {
        return 2 * i + 1;
    }

    right(i) {
        return 2 * i + 2;
    }

    insert(key) {
        this.heap.push(key);
        this._bubbleUp(this.heap.length - 1);
    }

    _bubbleUp(i) {
        while (i > 0 && this.heap[this.parent(i)] > this.heap[i]) {
            const parentIdx = this.parent(i);
            [this.heap[i], this.heap[parentIdx]] = [this.heap[parentIdx], this.heap[i]];
            i = parentIdx;
        }
    }

    extractMin() {
        if (this.heap.length === 0) {
            throw new Error("extractMin from empty heap");
        }

        if (this.heap.length === 1) {
            return this.heap.pop();
        }

        const minVal = this.heap[0];
        this.heap[0] = this.heap.pop();
        heapifyMin(this.heap, this.heap.length, 0);

        return minVal;
    }

    getMin() {
        if (this.heap.length === 0) {
            throw new Error("getMin from empty heap");
        }
        return this.heap[0];
    }

    size() {
        return this.heap.length;
    }

    isEmpty() {
        return this.heap.length === 0;
    }

    visualize() {
        if (this.heap.length === 0) {
            return "Empty heap";
        }

        const lines = [];
        this._visualizeHelper(0, "", "", lines);
        return lines.join('\n');
    }

    _visualizeHelper(i, prefix, childPrefix, lines) {
        if (i >= this.heap.length) {
            return;
        }

        lines.push(prefix + this.heap[i]);

        const leftIdx = this.left(i);
        const rightIdx = this.right(i);

        if (leftIdx < this.heap.length || rightIdx < this.heap.length) {
            if (leftIdx < this.heap.length) {
                if (rightIdx < this.heap.length) {
                    this._visualizeHelper(leftIdx, childPrefix + "├── ", childPrefix + "│   ", lines);
                } else {
                    this._visualizeHelper(leftIdx, childPrefix + "└── ", childPrefix + "    ", lines);
                }
            }

            if (rightIdx < this.heap.length) {
                this._visualizeHelper(rightIdx, childPrefix + "└── ", childPrefix + "    ", lines);
            }
        }
    }
}

/**
 * Priority Queue implementation using a max-heap.
 *
 * Higher priority values are served first.
 *
 * @template T
 */
class PriorityQueue {
    constructor() {
        this.heap = new MaxHeap();
    }

    /**
     * Add an item to the priority queue.
     * @param {T} item - Item to add
     */
    enqueue(item) {
        this.heap.insert(item);
    }

    /**
     * Remove and return the highest priority item.
     * @returns {T} The highest priority item
     * @throws {Error} If queue is empty
     */
    dequeue() {
        return this.heap.extractMax();
    }

    /**
     * Get the highest priority item without removing it.
     * @returns {T} The highest priority item
     * @throws {Error} If queue is empty
     */
    peek() {
        return this.heap.getMax();
    }

    /**
     * Check if the priority queue is empty.
     * @returns {boolean} True if empty
     */
    isEmpty() {
        return this.heap.isEmpty();
    }

    /**
     * Return the size of the priority queue.
     * @returns {number} Queue size
     */
    size() {
        return this.heap.size();
    }
}

/**
 * Check if array is sorted in ascending order.
 * @template T
 * @param {T[]} arr - Array to check
 * @returns {boolean} True if sorted
 */
function isSorted(arr) {
    for (let i = 0; i < arr.length - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            return false;
        }
    }
    return true;
}

/**
 * Demonstrate heap sort and heap data structure.
 */
function demonstrateHeapSort() {
    console.log("🏔️  Heap Sort Implementation in JavaScript");
    console.log("=".repeat(60));

    // Test data
    const testArrays = [
        { arr: [64, 34, 25, 12, 22, 11, 90], desc: "Random array" },
        { arr: [5, 2, 8, 6, 1, 9, 4], desc: "Small random array" },
        { arr: [1], desc: "Single element" },
        { arr: [], desc: "Empty array" },
        { arr: [3, 3, 3, 3, 3], desc: "All duplicates" },
        { arr: [9, 8, 7, 6, 5, 4, 3, 2, 1], desc: "Reverse sorted" },
        { arr: [1, 2, 3, 4, 5], desc: "Already sorted" }
    ];

    console.log("\n📋 Basic Sorting Tests:");
    console.log("-".repeat(60));

    testArrays.forEach(({ arr, desc }) => {
        const original = [...arr];
        const sortedArr = heapSort(arr);

        console.log(`\nTest: ${desc}`);
        console.log(`Original: [${original.join(', ')}]`);
        console.log(`Sorted:   [${sortedArr.join(', ')}]`);
        console.log(`Correct:  ${isSorted(sortedArr) ? '✓' : '✗'}`);
    });

    console.log("\n" + "-".repeat(60));

    // Demonstrate heap visualization
    console.log("\n🌲 Heap Visualization:");
    console.log("-".repeat(60));

    const data = [64, 34, 25, 12, 22, 11, 90];
    const maxHeap = new MaxHeap(data);

    console.log(`\nMax-Heap built from: [${data.join(', ')}]`);
    console.log(maxHeap.visualize());

    console.log(`\nMin-Heap built from: [${data.join(', ')}]`);
    const minHeap = new MinHeap(data);
    console.log(minHeap.visualize());

    // Demonstrate heap operations
    console.log("\n🔧 Heap Operations:");
    console.log("-".repeat(60));

    const heap = new MaxHeap();
    const operations = [50, 30, 70, 20, 40, 60, 80];

    console.log(`\nInserting elements: [${operations.join(', ')}]`);
    operations.forEach(val => {
        heap.insert(val);
        console.log(`Inserted ${val}, Max: ${heap.getMax()}`);
    });

    console.log("\nHeap structure:");
    console.log(heap.visualize());

    console.log("\nExtracting elements:");
    const extracted = [];
    while (!heap.isEmpty()) {
        const val = heap.extractMax();
        extracted.push(val);
        console.log(`Extracted: ${val}`);
    }

    console.log(`Extraction order: [${extracted.join(', ')}]`);
    const expectedDesc = [...extracted].sort((a, b) => b - a);
    console.log(`Is descending: ${JSON.stringify(extracted) === JSON.stringify(expectedDesc) ? '✓' : '✗'}`);

    // Demonstrate priority queue
    console.log("\n📬 Priority Queue Demo:");
    console.log("-".repeat(60));

    const pq = new PriorityQueue();
    const tasks = [5, 1, 9, 3, 7];

    console.log(`\nEnqueuing tasks with priorities: [${tasks.join(', ')}]`);
    tasks.forEach(priority => {
        pq.enqueue(priority);
        console.log(`Enqueued priority ${priority}, Top priority: ${pq.peek()}`);
    });

    console.log("\nProcessing tasks by priority:");
    while (!pq.isEmpty()) {
        const priority = pq.dequeue();
        console.log(`Processing task with priority: ${priority}`);
    }
}

/**
 * Benchmark heap sort against other O(n log n) algorithms.
 */
function performanceBenchmark() {
    console.log("\n\n⚡ Performance Benchmark");
    console.log("=".repeat(80));

    const sizes = [100, 500, 1000, 5000, 10000];

    // Test different data patterns
    const patterns = {
        "Random": (n) => Array.from({ length: n }, () => Math.floor(Math.random() * 1000)),
        "Sorted": (n) => Array.from({ length: n }, (_, i) => i),
        "Reversed": (n) => Array.from({ length: n }, (_, i) => n - i),
        "Nearly Sorted": (n) => {
            const arr = Array.from({ length: n }, (_, i) => i);
            if (n >= 10) {
                for (let i = 0; i < Math.min(5, n / 10); i++) {
                    const idx1 = Math.floor(Math.random() * n);
                    const idx2 = Math.floor(Math.random() * n);
                    [arr[idx1], arr[idx2]] = [arr[idx2], arr[idx1]];
                }
            }
            return arr;
        }
    };

    const methods = {
        "Heap Sort": heapSort,
        "Built-in": (arr) => [...arr].sort((a, b) => a - b)
    };

    for (const [patternName, patternGen] of Object.entries(patterns)) {
        console.log(`\n${patternName} Data:`);

        // Header
        let header = "Size".padEnd(8);
        for (const method of Object.keys(methods)) {
            header += method.padStart(15);
        }
        console.log(header);
        console.log("-".repeat(8 + 15 * Object.keys(methods).length));

        for (const size of sizes) {
            const testData = patternGen(size);
            let row = size.toString().padEnd(8);

            for (const [methodName, methodFunc] of Object.entries(methods)) {
                // Warm-up
                methodFunc([...testData.slice(0, 100)]);

                // Benchmark
                const start = performance.now();
                const result = methodFunc([...testData]);
                const end = performance.now();

                const elapsedMs = end - start;
                row += `${elapsedMs.toFixed(2)}ms`.padStart(15);

                // Verify correctness
                if (!isSorted(result)) {
                    row += " ✗";
                }
            }

            console.log(row);
        }
    }
}

/**
 * Test edge cases and error handling.
 */
function testEdgeCases() {
    console.log("\n\n🧪 Edge Cases and Error Handling");
    console.log("=".repeat(60));

    console.log("\n1. Testing empty heap operations:");
    try {
        const heap = new MaxHeap();
        heap.extractMax();
        console.log("   ✗ Should have thrown Error");
    } catch (e) {
        console.log(`   ✓ Correctly threw: ${e.message}`);
    }

    console.log("\n2. Testing getMax on empty heap:");
    try {
        const heap = new MaxHeap();
        heap.getMax();
        console.log("   ✗ Should have thrown Error");
    } catch (e) {
        console.log(`   ✓ Correctly threw: ${e.message}`);
    }

    console.log("\n3. Testing increaseKey with smaller value:");
    try {
        const heap = new MaxHeap([10, 20, 30]);
        heap.increaseKey(0, 5);
        console.log("   ✗ Should have thrown Error");
    } catch (e) {
        console.log(`   ✓ Correctly threw: ${e.message}`);
    }

    console.log("\n4. Testing decreaseKey with larger value:");
    try {
        const heap = new MaxHeap([10, 20, 30]);
        heap.decreaseKey(0, 50);
        console.log("   ✗ Should have thrown Error");
    } catch (e) {
        console.log(`   ✓ Correctly threw: ${e.message}`);
    }

    console.log("\n5. Testing index out of bounds:");
    try {
        const heap = new MaxHeap([10, 20, 30]);
        heap.increaseKey(10, 50);
        console.log("   ✗ Should have thrown Error");
    } catch (e) {
        console.log(`   ✓ Correctly threw: ${e.message}`);
    }

    console.log("\n6. Testing with duplicates:");
    const arr = [5, 5, 5, 5, 5];
    const sortedArr = heapSort(arr);
    console.log(`   Original: [${arr.join(', ')}]`);
    console.log(`   Sorted:   [${sortedArr.join(', ')}]`);
    console.log(`   Correct:  ${JSON.stringify(sortedArr) === JSON.stringify(arr) ? '✓' : '✗'}`);

    console.log("\n7. Testing heap property after operations:");
    const heap = new MaxHeap([15, 10, 20, 8, 12, 25]);
    console.log(`   Initial heap: [${heap.toArray().join(', ')}]`);

    heap.insert(30);
    console.log(`   After insert(30): [${heap.toArray().join(', ')}]`);
    console.log(`   Max is 30: ${heap.getMax() === 30 ? '✓' : '✗'}`);

    const maxVal = heap.extractMax();
    console.log(`   Extracted: ${maxVal}`);
    console.log(`   New max is 25: ${heap.getMax() === 25 ? '✓' : '✗'}`);
}

// Main execution
if (typeof require !== 'undefined' && require.main === module) {
    demonstrateHeapSort();
    performanceBenchmark();
    testEdgeCases();

    console.log("\n✨ Heap Sort demonstration complete!");
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        heapSort,
        heapSortInPlace,
        heapSortDescending,
        heapifyMax,
        heapifyMin,
        buildMaxHeap,
        buildMinHeap,
        MaxHeap,
        MinHeap,
        PriorityQueue,
        isSorted,
        demonstrateHeapSort,
        performanceBenchmark,
        testEdgeCases
    };
}
