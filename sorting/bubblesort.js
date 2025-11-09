/**
 * Bubble Sort Algorithm Implementation in JavaScript
 *
 * Time Complexity:
 * - Best Case: O(n) - when array is already sorted (optimized version)
 * - Average Case: O(n²)
 * - Worst Case: O(n²) - when array is reverse sorted
 * Space Complexity: O(1) for in-place, O(n) for functional approach
 *
 * Bubble Sort works by repeatedly stepping through the list, comparing adjacent
 * elements and swapping them if they are in the wrong order. The pass through
 * the list is repeated until the list is sorted.
 *
 * JavaScript features:
 * - ES6+ syntax (arrow functions, destructuring, spread operator)
 * - Array extension methods
 * - Functional programming patterns
 * - Performance measurement using performance.now()
 */

/**
 * Basic iterative bubble sort implementation.
 *
 * This is the standard bubble sort algorithm that compares and swaps
 * adjacent elements until the entire array is sorted.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @returns {T[]} New sorted array
 *
 * Time Complexity: O(n²) in all cases (no optimization)
 * Space Complexity: O(n) for the new array
 */
function bubbleSortIterative(arr) {
    if (arr.length <= 1) {
        return [...arr];
    }

    const result = [...arr];
    const n = result.length;

    // Outer loop for number of passes
    for (let i = 0; i < n; i++) {
        // Inner loop for comparisons
        // After each pass, the largest element "bubbles up" to its position
        for (let j = 0; j < n - i - 1; j++) {
            if (result[j] > result[j + 1]) {
                // Swap adjacent elements using destructuring
                [result[j], result[j + 1]] = [result[j + 1], result[j]];
            }
        }
    }

    return result;
}

/**
 * Optimized bubble sort with early termination.
 *
 * This version includes a flag to detect if any swaps were made during a pass.
 * If no swaps occur, the array is already sorted and we can terminate early.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @returns {T[]} New sorted array
 *
 * Time Complexity:
 *   - Best Case: O(n) when already sorted
 *   - Average/Worst: O(n²)
 * Space Complexity: O(n) for the new array
 */
function bubbleSortOptimized(arr) {
    if (arr.length <= 1) {
        return [...arr];
    }

    const result = [...arr];
    const n = result.length;

    for (let i = 0; i < n; i++) {
        // Flag to optimize for already sorted arrays
        let swapped = false;

        for (let j = 0; j < n - i - 1; j++) {
            if (result[j] > result[j + 1]) {
                [result[j], result[j + 1]] = [result[j + 1], result[j]];
                swapped = true;
            }
        }

        // If no swaps occurred, array is sorted
        if (!swapped) {
            break;
        }
    }

    return result;
}

/**
 * In-place bubble sort implementation (optimized).
 *
 * Sorts the array in-place without creating a new array,
 * minimizing space complexity.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted in-place
 * @returns {void}
 *
 * Time Complexity: O(n) best case, O(n²) average/worst
 * Space Complexity: O(1)
 */
function bubbleSortInPlace(arr) {
    const n = arr.length;

    for (let i = 0; i < n; i++) {
        let swapped = false;

        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
                swapped = true;
            }
        }

        if (!swapped) {
            break;
        }
    }
}

/**
 * Recursive bubble sort implementation.
 *
 * Each recursive call performs one pass through the array,
 * bubbling the largest element to the end.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @param {number} [n=arr.length] - Size of the array portion to sort
 * @returns {T[]} The same array (sorted in-place for recursion efficiency)
 *
 * Time Complexity: O(n²)
 * Space Complexity: O(n) for recursion stack
 */
function bubbleSortRecursive(arr, n = null) {
    // Initialize on first call
    if (n === null) {
        const result = [...arr];
        return bubbleSortRecursive(result, result.length);
    }

    // Base case: single element or empty
    if (n <= 1) {
        return arr;
    }

    // One pass of bubble sort
    // After this pass, the largest element will be at the end
    for (let i = 0; i < n - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            [arr[i], arr[i + 1]] = [arr[i + 1], arr[i]];
        }
    }

    // Recursively sort the first n-1 elements
    return bubbleSortRecursive(arr, n - 1);
}

/**
 * Functional-style bubble sort implementation.
 *
 * This implementation uses functional programming principles,
 * creating new arrays for immutability.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @returns {T[]} New sorted array
 *
 * Time Complexity: O(n²)
 * Space Complexity: O(n)
 */
function bubbleSortFunctional(arr) {
    if (arr.length <= 1) {
        return [...arr];
    }

    const performPass = (array) => {
        let swapped = false;
        const newArray = [...array];

        for (let i = 0; i < newArray.length - 1; i++) {
            if (newArray[i] > newArray[i + 1]) {
                [newArray[i], newArray[i + 1]] = [newArray[i + 1], newArray[i]];
                swapped = true;
            }
        }

        return { array: newArray, swapped };
    };

    let result = [...arr];
    let continueSort = true;

    while (continueSort) {
        const { array, swapped } = performPass(result);
        result = array;
        continueSort = swapped;
    }

    return result;
}

/**
 * Bubble sort with custom comparison function.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @param {(a: T, b: T) => number} [compareFn] - Comparison function
 * @returns {T[]} New sorted array
 *
 * Example:
 *   bubbleSortWithComparator([3, 1, 4], (a, b) => b - a) // Descending order
 */
function bubbleSortWithComparator(arr, compareFn = (a, b) => a > b ? 1 : a < b ? -1 : 0) {
    if (arr.length <= 1) {
        return [...arr];
    }

    const result = [...arr];
    const n = result.length;

    for (let i = 0; i < n; i++) {
        let swapped = false;

        for (let j = 0; j < n - i - 1; j++) {
            if (compareFn(result[j], result[j + 1]) > 0) {
                [result[j], result[j + 1]] = [result[j + 1], result[j]];
                swapped = true;
            }
        }

        if (!swapped) {
            break;
        }
    }

    return result;
}

/**
 * Cocktail Shaker Sort (bidirectional bubble sort).
 *
 * An optimized version of bubble sort that sorts in both directions
 * alternately, which can be more efficient for certain data patterns.
 *
 * @template T
 * @param {T[]} arr - Array to be sorted
 * @returns {T[]} New sorted array
 *
 * Time Complexity: O(n²) worst case, but often faster than standard bubble sort
 * Space Complexity: O(n)
 */
function cocktailSort(arr) {
    if (arr.length <= 1) {
        return [...arr];
    }

    const result = [...arr];
    let start = 0;
    let end = result.length - 1;
    let swapped = true;

    while (swapped) {
        swapped = false;

        // Forward pass (like bubble sort)
        for (let i = start; i < end; i++) {
            if (result[i] > result[i + 1]) {
                [result[i], result[i + 1]] = [result[i + 1], result[i]];
                swapped = true;
            }
        }

        if (!swapped) {
            break;
        }

        swapped = false;
        end--;

        // Backward pass
        for (let i = end - 1; i >= start; i--) {
            if (result[i] > result[i + 1]) {
                [result[i], result[i + 1]] = [result[i + 1], result[i]];
                swapped = true;
            }
        }

        start++;
    }

    return result;
}

/**
 * Check if array is sorted in ascending order.
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
 * Count comparisons and swaps during bubble sort.
 *
 * @template T
 * @param {T[]} arr - Array to analyze
 * @returns {{ comparisons: number, swaps: number }}
 */
function countComparisonsAndSwaps(arr) {
    const result = [...arr];
    const n = result.length;
    let comparisons = 0;
    let swaps = 0;

    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            comparisons++;
            if (result[j] > result[j + 1]) {
                [result[j], result[j + 1]] = [result[j + 1], result[j]];
                swaps++;
            }
        }
    }

    return { comparisons, swaps };
}

/**
 * Array extension methods for convenient sorting.
 */
if (typeof Array.prototype.bubbleSort === 'undefined') {
    /**
     * Extension method to sort array using bubble sort.
     * @returns {Array} New sorted array
     */
    Array.prototype.bubbleSort = function() {
        return bubbleSortOptimized(this);
    };

    /**
     * Extension method to sort array in-place using bubble sort.
     * @returns {Array} The same array (sorted)
     */
    Array.prototype.bubbleSortInPlace = function() {
        bubbleSortInPlace(this);
        return this;
    };
}

/**
 * BubbleSorter class with statistics tracking.
 */
class BubbleSorter {
    constructor() {
        this.comparisons = 0;
        this.swaps = 0;
        this.iterations = 0;
    }

    /**
     * Sort array and track statistics.
     * @template T
     * @param {T[]} arr - Array to sort
     * @returns {T[]} Sorted array
     */
    sort(arr) {
        this.resetStats();
        const result = [...arr];
        const n = result.length;

        for (let i = 0; i < n; i++) {
            this.iterations++;
            let swapped = false;

            for (let j = 0; j < n - i - 1; j++) {
                this.comparisons++;
                if (result[j] > result[j + 1]) {
                    [result[j], result[j + 1]] = [result[j + 1], result[j]];
                    this.swaps++;
                    swapped = true;
                }
            }

            if (!swapped) {
                break;
            }
        }

        return result;
    }

    resetStats() {
        this.comparisons = 0;
        this.swaps = 0;
        this.iterations = 0;
    }

    getStats() {
        return {
            comparisons: this.comparisons,
            swaps: this.swaps,
            iterations: this.iterations
        };
    }
}

/**
 * Demonstrate various bubble sort implementations.
 */
function demonstrateBubbleSort() {
    console.log("🫧 Bubble Sort Implementation in JavaScript");
    console.log("=".repeat(50));

    // Test data - comprehensive edge cases
    const testArrays = [
        { arr: [64, 34, 25, 12, 22, 11, 90], desc: "Random array" },
        { arr: [5, 2, 8, 6, 1, 9, 4], desc: "Small random array" },
        { arr: [1], desc: "Single element" },
        { arr: [], desc: "Empty array" },
        { arr: [3, 3, 3, 3, 3], desc: "All duplicates" },
        { arr: [9, 8, 7, 6, 5, 4, 3, 2, 1], desc: "Reverse sorted" },
        { arr: [1, 2, 3, 4, 5], desc: "Already sorted" },
        { arr: [5, 1, 4, 2, 3], desc: "Nearly sorted" }
    ];

    console.log("\n📋 Basic Sorting Tests:");
    console.log("-".repeat(50));

    testArrays.forEach(({ arr, desc }) => {
        const original = [...arr];

        // Test different implementations
        const iterativeResult = bubbleSortIterative(arr);
        const optimizedResult = bubbleSortOptimized(arr);
        const recursiveResult = bubbleSortRecursive(arr);
        const cocktailResult = cocktailSort(arr);

        // Test in-place
        const inplaceResult = [...arr];
        bubbleSortInPlace(inplaceResult);

        console.log(`\nTest: ${desc}`);
        console.log(`Original:  [${original.join(', ')}]`);
        console.log(`Sorted:    [${iterativeResult.join(', ')}]`);

        // Verify all results are correct and equal
        const results = [iterativeResult, optimizedResult, recursiveResult,
                        cocktailResult, inplaceResult];
        const allCorrect = results.every(result => isSorted(result));
        const allEqual = results.every(result =>
            JSON.stringify(result) === JSON.stringify(iterativeResult));

        const status = allCorrect && allEqual ? "✓" : "✗";
        console.log(`All implementations match: ${status}`);
    });

    console.log("\n" + "-".repeat(50));

    // String sorting
    const words = ["banana", "apple", "cherry", "date", "elderberry"];
    const sortedWords = bubbleSortOptimized(words);

    console.log("\n🔤 Word sorting:");
    console.log(`Original:     [${words.join(', ')}]`);
    console.log(`Alphabetical: [${sortedWords.join(', ')}]`);

    // Custom comparison
    const numbers = [3, 1, 4, 1, 5, 9, 2, 6];
    const descSorted = bubbleSortWithComparator(numbers, (a, b) => b - a);

    console.log("\n🔢 Custom comparison (descending):");
    console.log(`Original:   [${numbers.join(', ')}]`);
    console.log(`Descending: [${descSorted.join(', ')}]`);

    // Array extension methods
    console.log("\n🔧 Extension Methods:");
    const testExt = [5, 2, 8, 1, 9];
    console.log(`Original: [${testExt.join(', ')}]`);
    console.log(`Using .bubbleSort(): [${testExt.bubbleSort().join(', ')}]`);
}

/**
 * Benchmark different bubble sort implementations.
 */
function performanceBenchmark() {
    console.log("\n\n⚡ Performance Benchmark");
    console.log("=".repeat(70));

    const sizes = [100, 500, 1000, 2000];

    // Test different data patterns
    const patterns = {
        "Random": (n) => Array.from({ length: n }, () => Math.floor(Math.random() * 1000)),
        "Sorted": (n) => Array.from({ length: n }, (_, i) => i),
        "Reversed": (n) => Array.from({ length: n }, (_, i) => n - i),
        "Nearly Sorted": (n) => {
            const arr = Array.from({ length: n }, (_, i) => i);
            if (n >= 10) {
                // Swap a few elements
                for (let i = 0; i < Math.min(5, n / 10); i++) {
                    const idx = Math.floor(Math.random() * n);
                    const idx2 = Math.floor(Math.random() * n);
                    [arr[idx], arr[idx2]] = [arr[idx2], arr[idx]];
                }
            }
            return arr;
        }
    };

    const methods = {
        "Iterative": bubbleSortIterative,
        "Optimized": bubbleSortOptimized,
        "Recursive": bubbleSortRecursive,
        "Cocktail": cocktailSort,
        "Built-in": (arr) => [...arr].sort((a, b) => a - b)
    };

    for (const [patternName, patternGen] of Object.entries(patterns)) {
        console.log(`\n${patternName} Data:`);

        // Header
        let header = "Size".padEnd(8);
        for (const method of Object.keys(methods)) {
            header += method.padStart(12);
        }
        console.log(header);
        console.log("-".repeat(8 + 12 * Object.keys(methods).length));

        for (const size of sizes) {
            const testData = patternGen(size);
            let row = size.toString().padEnd(8);

            for (const [methodName, methodFunc] of Object.entries(methods)) {
                // Skip recursive for large sizes
                if (methodName === "Recursive" && size > 1000) {
                    row += "N/A".padStart(12);
                    continue;
                }

                try {
                    const start = performance.now();
                    const result = methodFunc([...testData]);
                    const end = performance.now();

                    const elapsedMs = end - start;
                    row += `${elapsedMs.toFixed(2)}ms`.padStart(12);

                    // Verify correctness
                    if (!isSorted(result)) {
                        row += " ✗";
                    }
                } catch (error) {
                    row += "ERROR".padStart(12);
                }
            }

            console.log(row);
        }
    }
}

/**
 * Analyze bubble sort behavior with different inputs.
 */
function analyzeAlgorithm() {
    console.log("\n\n🔍 Algorithm Analysis");
    console.log("=".repeat(50));

    const testCases = [
        { arr: [5, 2, 8, 6, 1], desc: "Random" },
        { arr: [1, 2, 3, 4, 5], desc: "Already sorted" },
        { arr: [5, 4, 3, 2, 1], desc: "Reverse sorted" }
    ];

    testCases.forEach(({ arr, desc }) => {
        const { comparisons, swaps } = countComparisonsAndSwaps(arr);
        const n = arr.length;
        const theoreticalMax = n * (n - 1) / 2;

        console.log(`\n${desc}: [${arr.join(', ')}]`);
        console.log(`Array size (n): ${n}`);
        console.log(`Comparisons: ${comparisons} (theoretical max: ${theoreticalMax})`);
        console.log(`Swaps: ${swaps}`);
        console.log(`Efficiency: ${((1 - swaps / Math.max(comparisons, 1)) * 100).toFixed(1)}% (fewer swaps is better)`);
    });
}

// Main execution
if (typeof require !== 'undefined' && require.main === module) {
    demonstrateBubbleSort();
    performanceBenchmark();
    analyzeAlgorithm();

    // Demonstrate OOP approach
    console.log("\n\n📊 Object-Oriented Approach");
    console.log("=".repeat(50));

    const sorter = new BubbleSorter();
    const testArray = [64, 34, 25, 12, 22, 11, 90];

    const sortedArray = sorter.sort(testArray);
    const stats = sorter.getStats();

    console.log(`Original: [${testArray.join(', ')}]`);
    console.log(`Sorted:   [${sortedArray.join(', ')}]`);
    console.log(`Statistics:`, stats);

    console.log("\n✨ Bubble Sort demonstration complete!");
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        bubbleSortIterative,
        bubbleSortOptimized,
        bubbleSortInPlace,
        bubbleSortRecursive,
        bubbleSortFunctional,
        bubbleSortWithComparator,
        cocktailSort,
        isSorted,
        BubbleSorter,
        demonstrateBubbleSort,
        performanceBenchmark,
        analyzeAlgorithm
    };
}
