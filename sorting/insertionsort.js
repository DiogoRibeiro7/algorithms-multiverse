/**
 * Insertion Sort Algorithm Implementation in JavaScript
 *
 * Time Complexity:
 * - Best Case: O(n) - when array is already sorted
 * - Average Case: O(n²)
 * - Worst Case: O(n²) - when array is reverse sorted
 * Space Complexity: O(1) for in-place, O(n) for functional approach
 *
 * Insertion Sort builds the final sorted array one item at a time. It is much less
 * efficient on large lists than more advanced algorithms like quicksort or merge sort.
 * However, it has several advantages:
 * - Simple implementation
 * - Efficient for small data sets
 * - Adaptive (efficient for nearly sorted data)
 * - Stable (preserves relative order of equal elements)
 * - In-place (only requires O(1) additional memory)
 * - Online (can sort a list as it receives it)
 *
 * JavaScript features:
 * - ES6+ syntax (arrow functions, destructuring, spread operator)
 * - Array extension methods
 * - Functional programming patterns
 * - Performance measurement using performance.now()
 */

/**
 * Standard insertion sort implementation.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @returns {T[]} New sorted array
 *
 * Time Complexity: O(n²) average and worst case, O(n) best case
 * Space Complexity: O(n) for the new array
 *
 * Example visualization:
 *   Initial: [5, 2, 8, 6, 1]
 *   Step 1:  [2, 5, 8, 6, 1]  // Insert 2
 *   Step 2:  [2, 5, 8, 6, 1]  // 8 already in place
 *   Step 3:  [2, 5, 6, 8, 1]  // Insert 6
 *   Step 4:  [1, 2, 5, 6, 8]  // Insert 1
 */
function insertionSort(arr) {
    if (arr.length <= 1) {
        return [...arr];
    }

    const result = [...arr];
    insertionSortInPlace(result);
    return result;
}

/**
 * In-place insertion sort implementation.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted in-place
 *
 * Time Complexity: O(n²) average and worst case, O(n) best case
 * Space Complexity: O(1)
 */
function insertionSortInPlace(arr) {
    for (let i = 1; i < arr.length; i++) {
        const key = arr[i];
        let j = i - 1;

        // Move elements greater than key one position ahead
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }

        arr[j + 1] = key;
    }
}

/**
 * Recursive insertion sort implementation.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @param {number} [n] - Number of elements to sort (used in recursion)
 * @returns {T[]} The same array (sorted in-place for recursion efficiency)
 *
 * Time Complexity: O(n²)
 * Space Complexity: O(n) for recursion stack
 */
function insertionSortRecursive(arr, n = null) {
    // Initialize on first call
    if (n === null) {
        const result = [...arr];
        return insertionSortRecursive(result, result.length);
    }

    // Base case
    if (n <= 1) {
        return arr;
    }

    // Sort first n-1 elements
    insertionSortRecursive(arr, n - 1);

    // Insert last element at its correct position
    const key = arr[n - 1];
    let j = n - 2;

    while (j >= 0 && arr[j] > key) {
        arr[j + 1] = arr[j];
        j--;
    }

    arr[j + 1] = key;
    return arr;
}

/**
 * Binary insertion sort - uses binary search to find insertion position.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @returns {T[]} New sorted array
 *
 * Time Complexity: O(n²) for moves, O(n log n) for comparisons
 * Space Complexity: O(n)
 */
function binaryInsertionSort(arr) {
    if (arr.length <= 1) {
        return [...arr];
    }

    const result = [...arr];

    for (let i = 1; i < result.length; i++) {
        const key = result[i];

        // Find position using binary search
        const pos = binarySearchPosition(result, 0, i - 1, key);

        // Shift elements to make space
        for (let j = i - 1; j >= pos; j--) {
            result[j + 1] = result[j];
        }

        result[pos] = key;
    }

    return result;
}

/**
 * Find the position where key should be inserted.
 *
 * @template T
 * @param {T[]} arr - Sorted array
 * @param {number} left - Left boundary
 * @param {number} right - Right boundary
 * @param {T} key - Element to insert
 * @returns {number} Position where key should be inserted
 */
function binarySearchPosition(arr, left, right, key) {
    if (right <= left) {
        return key > arr[left] ? left + 1 : left;
    }

    const mid = Math.floor((left + right) / 2);

    if (key === arr[mid]) {
        return mid + 1;
    }

    if (key > arr[mid]) {
        return binarySearchPosition(arr, mid + 1, right, key);
    }

    return binarySearchPosition(arr, left, mid - 1, key);
}

/**
 * Shell sort - a generalization of insertion sort.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @returns {T[]} New sorted array
 *
 * Time Complexity: Depends on gap sequence (O(n log²n) for good sequences)
 * Space Complexity: O(n)
 */
function shellSort(arr) {
    if (arr.length <= 1) {
        return [...arr];
    }

    const result = [...arr];
    const n = result.length;

    // Start with a large gap, then reduce (Knuth's sequence)
    let gap = 1;
    while (gap < Math.floor(n / 3)) {
        gap = 3 * gap + 1;
    }

    // Perform gapped insertion sort
    while (gap > 0) {
        for (let i = gap; i < n; i++) {
            const key = result[i];
            let j = i;

            // Insertion sort with gap
            while (j >= gap && result[j - gap] > key) {
                result[j] = result[j - gap];
                j -= gap;
            }

            result[j] = key;
        }

        gap = Math.floor(gap / 3);
    }

    return result;
}

/**
 * Hybrid sort that uses insertion sort for small subarrays.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @param {number} [threshold=10] - Size below which to use insertion sort
 * @returns {T[]} New sorted array
 */
function hybridInsertionSort(arr, threshold = 10) {
    if (arr.length <= threshold) {
        return insertionSort(arr);
    }

    // For demonstration; in practice, this would call quicksort or mergesort
    return insertionSort(arr);
}

/**
 * Insertion sort with custom comparator.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @param {(a: T, b: T) => number} compareFn - Comparison function
 * @returns {T[]} New sorted array
 */
function insertionSortWithComparator(arr, compareFn = (a, b) => a > b ? 1 : a < b ? -1 : 0) {
    if (arr.length <= 1) {
        return [...arr];
    }

    const result = [...arr];

    for (let i = 1; i < result.length; i++) {
        const key = result[i];
        let j = i - 1;

        while (j >= 0 && compareFn(result[j], key) > 0) {
            result[j + 1] = result[j];
            j--;
        }

        result[j + 1] = key;
    }

    return result;
}

/**
 * Create a step-by-step visualization of the insertion sort process.
 *
 * @param {number[]} arr - Array to sort
 * @returns {string[]} Array of strings showing each step
 */
function visualizeInsertionSort(arr) {
    const steps = [];
    const result = [...arr];
    steps.push(`Initial: [${result.join(', ')}]`);

    for (let i = 1; i < result.length; i++) {
        const key = result[i];
        let j = i - 1;

        steps.push(`\nStep ${i}: Inserting ${key}`);
        steps.push(`  Before: [${result.join(', ')}]`);

        while (j >= 0 && result[j] > key) {
            result[j + 1] = result[j];
            j--;
        }

        result[j + 1] = key;
        steps.push(`  After:  [${result.join(', ')}]`);
    }

    steps.push(`\nFinal: [${result.join(', ')}]`);
    return steps;
}

/**
 * Count comparisons and swaps during insertion sort.
 *
 * @template T
 * @param {T[]} arr - Array to sort
 * @returns {{ comparisons: number, swaps: number }}
 */
function countOperations(arr) {
    const result = [...arr];
    let comparisons = 0;
    let swaps = 0;

    for (let i = 1; i < result.length; i++) {
        const key = result[i];
        let j = i - 1;

        while (j >= 0) {
            comparisons++;
            if (result[j] > key) {
                result[j + 1] = result[j];
                swaps++;
                j--;
            } else {
                break;
            }
        }

        result[j + 1] = key;
    }

    return { comparisons, swaps };
}

/**
 * Demonstrate that insertion sort is stable.
 */
function isStableDemo() {
    // Using objects with value and original index to track stability
    const data = [
        { val: 3, idx: 0 },
        { val: 1, idx: 1 },
        { val: 3, idx: 2 },
        { val: 2, idx: 3 },
        { val: 3, idx: 4 }
    ];

    console.log("Stability Demonstration:");
    console.log("Original:", data.map(d => `(${d.val},${d.idx})`).join(' '));

    const sorted = insertionSortWithComparator(data, (a, b) => a.val - b.val);
    console.log("Sorted:  ", sorted.map(d => `(${d.val},${d.idx})`).join(' '));

    // Check if elements with same value maintain their relative order
    const threeIndices = sorted.filter(d => d.val === 3).map(d => d.idx);
    const isStable = JSON.stringify(threeIndices) === JSON.stringify([0, 2, 4]);

    console.log(`Stable: ${isStable} (indices of 3's: [${threeIndices.join(', ')}])`);
}

/**
 * Check if array is sorted.
 *
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
 * Array extension methods for convenient sorting.
 */
if (typeof Array.prototype.insertionSort === 'undefined') {
    Array.prototype.insertionSort = function() {
        return insertionSort(this);
    };

    Array.prototype.insertionSortInPlace = function() {
        insertionSortInPlace(this);
        return this;
    };
}

/**
 * Demonstrate various insertion sort implementations.
 */
function demonstrateInsertionSort() {
    console.log("📝 Insertion Sort Implementation in JavaScript");
    console.log("=".repeat(60));

    // Test data
    const testArrays = [
        { arr: [64, 34, 25, 12, 22, 11, 90], desc: "Random array" },
        { arr: [5, 2, 8, 6, 1, 9, 4], desc: "Small random array" },
        { arr: [1], desc: "Single element" },
        { arr: [], desc: "Empty array" },
        { arr: [3, 3, 3, 3, 3], desc: "All duplicates" },
        { arr: [9, 8, 7, 6, 5, 4, 3, 2, 1], desc: "Reverse sorted" },
        { arr: [1, 2, 3, 4, 5], desc: "Already sorted" },
        { arr: [1, 3, 2, 4, 5], desc: "Nearly sorted" }
    ];

    console.log("\n📋 Basic Sorting Tests:");
    console.log("-".repeat(60));

    testArrays.forEach(({ arr, desc }) => {
        const original = [...arr];

        // Test different implementations
        const standardResult = insertionSort(arr);
        const binaryResult = binaryInsertionSort(arr);
        const shellResult = shellSort(arr);
        const recursiveResult = insertionSortRecursive(arr);

        console.log(`\nTest: ${desc}`);
        console.log(`Original:  [${original.join(', ')}]`);
        console.log(`Sorted:    [${standardResult.join(', ')}]`);

        // Verify all results
        const results = [standardResult, binaryResult, shellResult, recursiveResult];
        const allCorrect = results.every(result => isSorted(result));
        const allEqual = results.every(result =>
            JSON.stringify(result) === JSON.stringify(standardResult));

        const status = allCorrect && allEqual ? "✓" : "✗";
        console.log(`All implementations match: ${status}`);
    });

    // Visualization demo
    console.log("\n\n🎬 Step-by-Step Visualization:");
    console.log("-".repeat(60));

    const demoArr = [5, 2, 8, 6, 1];
    const steps = visualizeInsertionSort(demoArr);
    steps.forEach(step => console.log(step));

    // Stability demonstration
    console.log("\n\n🔒 Stability Demonstration:");
    console.log("-".repeat(60));
    isStableDemo();

    // Performance analysis
    console.log("\n\n📊 Operation Counting:");
    console.log("-".repeat(60));

    const testCases = [
        { arr: [5, 2, 8, 6, 1], desc: "Random" },
        { arr: [1, 2, 3, 4, 5], desc: "Already sorted" },
        { arr: [5, 4, 3, 2, 1], desc: "Reverse sorted" }
    ];

    testCases.forEach(({ arr, desc }) => {
        const { comparisons, swaps } = countOperations(arr);
        const n = arr.length;

        console.log(`\n${desc}: [${arr.join(', ')}]`);
        console.log(`Array size (n): ${n}`);
        console.log(`Comparisons: ${comparisons}`);
        console.log(`Swaps: ${swaps}`);
        console.log(`Best case comparisons: ${n - 1}`);
        console.log(`Worst case comparisons: ${n * (n - 1) / 2}`);
    });
}

/**
 * Benchmark insertion sort and show when it's preferred.
 */
function performanceBenchmark() {
    console.log("\n\n⚡ Performance Benchmark");
    console.log("=".repeat(80));
    console.log("\nInsertion sort is preferred for:");
    console.log("  • Small arrays (typically n < 10-20)");
    console.log("  • Nearly sorted arrays");
    console.log("  • As part of hybrid sorting algorithms");
    console.log();

    const sizes = [5, 10, 20, 50, 100, 500, 1000];

    // Test different data patterns
    const patterns = {
        "Random": (n) => Array.from({ length: n }, () => Math.floor(Math.random() * 1000)),
        "Nearly Sorted": (n) => {
            const arr = Array.from({ length: n }, (_, i) => i);
            // Swap a few elements
            for (let i = 0; i < Math.min(5, n / 10); i++) {
                const idx1 = Math.floor(Math.random() * n);
                const idx2 = Math.floor(Math.random() * n);
                [arr[idx1], arr[idx2]] = [arr[idx2], arr[idx1]];
            }
            return arr;
        },
        "Reversed": (n) => Array.from({ length: n }, (_, i) => n - i)
    };

    const methods = {
        "Insertion": insertionSort,
        "Binary Insert": binaryInsertionSort,
        "Shell Sort": shellSort,
        "Built-in": (arr) => [...arr].sort((a, b) => a - b)
    };

    for (const [patternName, patternGen] of Object.entries(patterns)) {
        console.log(`\n${patternName} Data:`);

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
                const start = performance.now();
                const result = methodFunc([...testData]);
                const end = performance.now();

                const elapsedMs = end - start;
                row += `${elapsedMs.toFixed(3)}ms`.padStart(15);

                if (!isSorted(result)) {
                    row += " ✗";
                }
            }

            console.log(row);
        }
    }
}

// Main execution
if (typeof require !== 'undefined' && require.main === module) {
    demonstrateInsertionSort();
    performanceBenchmark();

    console.log("\n✨ Insertion Sort demonstration complete!");
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        insertionSort,
        insertionSortInPlace,
        insertionSortRecursive,
        binaryInsertionSort,
        shellSort,
        hybridInsertionSort,
        insertionSortWithComparator,
        visualizeInsertionSort,
        countOperations,
        isSorted,
        demonstrateInsertionSort,
        performanceBenchmark
    };
}
