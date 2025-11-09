/**
 * Selection Sort Algorithm - Educational Implementation (JavaScript/ES6+)
 *
 * ALGORITHM OVERVIEW:
 * ==================
 * Selection Sort works by repeatedly finding the minimum element from the unsorted
 * portion of the array and placing it at the beginning. It divides the array into
 * two parts: a sorted portion (left) and an unsorted portion (right).
 *
 * Time Complexity:
 * - Best Case: O(n²) - Even if array is already sorted, still searches for minimum
 * - Average Case: O(n²)
 * - Worst Case: O(n²)
 * - IMPORTANT: Unlike bubble sort and insertion sort, selection sort ALWAYS performs
 *   O(n²) comparisons, regardless of input
 *
 * Space Complexity: O(1) - Sorts in-place with only constant extra space
 *
 * Stability: NOT stable by default (can be made stable with modifications)
 * In-place: YES
 *
 * KEY ADVANTAGE: Makes MINIMUM number of swaps - only O(n) swaps!
 * This is important when writing to memory is expensive.
 */

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
 * Pass 3: Find min in [25, 22, 64] → 22
 *         Swap 25 ↔ 22
 *         Result: [11, 12, 22, 25, 64]
 *                  ^^^^^^^^^^^ sorted portion
 *
 * Pass 4: Find min in [25, 64] → 25
 *         No swap needed
 *         Result: [11, 12, 22, 25, 64]
 *                  ^^^^^^^^^^^^^^^ sorted portion
 *
 * @param {Array} arr - The array to sort
 * @param {Function} [comparator] - Optional comparison function
 * @returns {Array} A new sorted array
 */
function selectionSort(arr, comparator = (a, b) => a - b) {
    if (arr.length <= 1) return [...arr];

    const result = [...arr];
    selectionSortInPlace(result, comparator);
    return result;
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
 * @param {Array} arr - The array to sort (modified in-place)
 * @param {Function} [comparator] - Optional comparison function
 */
function selectionSortInPlace(arr, comparator = (a, b) => a - b) {
    const n = arr.length;

    // Outer loop: Move boundary of unsorted subarray one by one
    for (let i = 0; i < n - 1; i++) {
        // Find the minimum element in the remaining unsorted array
        // Start by assuming the first unsorted element is the minimum
        let minIdx = i;

        // Inner loop: Search for the minimum in arr[i+1...n-1]
        for (let j = i + 1; j < n; j++) {
            // If we find a smaller element, update minIdx
            if (comparator(arr[j], arr[minIdx]) < 0) {
                minIdx = j;
            }
        }

        // Swap the found minimum element with the first element
        // of the unsorted portion
        if (minIdx !== i) {
            [arr[i], arr[minIdx]] = [arr[minIdx], arr[i]];
        }
    }
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
 * Algorithm:
 * - Find both min and max in the unsorted portion
 * - Place min at the left boundary
 * - Place max at the right boundary
 * - Move both boundaries inward
 *
 * Time: Still O(n²), but approximately 2x faster in practice
 *
 * @param {Array} arr - The array to sort
 * @param {Function} [comparator] - Optional comparison function
 * @returns {Array} A new sorted array
 */
function bidirectionalSelectionSort(arr, comparator = (a, b) => a - b) {
    if (arr.length <= 1) return [...arr];

    const result = [...arr];
    const n = result.length;

    // Process from both ends toward the middle
    let left = 0;
    let right = n - 1;

    while (left < right) {
        // Find both minimum and maximum in the current range
        let minIdx = left;
        let maxIdx = left;

        for (let i = left; i <= right; i++) {
            if (comparator(result[i], result[minIdx]) < 0) {
                minIdx = i;
            }
            if (comparator(result[i], result[maxIdx]) > 0) {
                maxIdx = i;
            }
        }

        // Handle special case: if min is at right position
        if (minIdx === right) {
            [result[left], result[right]] = [result[right], result[left]];
            if (maxIdx === left) {
                maxIdx = right;
            }
        } else {
            // Swap minimum to the left boundary
            if (minIdx !== left) {
                [result[left], result[minIdx]] = [result[minIdx], result[left]];
            }

            // If maximum was at left position, it's now at minIdx
            if (maxIdx === left) {
                maxIdx = minIdx;
            }

            // Swap maximum to the right boundary
            if (maxIdx !== right) {
                [result[right], result[maxIdx]] = [result[maxIdx], result[right]];
            }
        }

        // Move boundaries inward
        left++;
        right--;
    }

    return result;
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
 * @param {Array} arr - The array to sort
 * @param {Function} [comparator] - Optional comparison function
 * @returns {Array} A new sorted array
 */
function selectionSortRecursive(arr, comparator = (a, b) => a - b) {
    if (arr.length <= 1) return [...arr];

    const result = [...arr];
    selectionSortRecursiveHelper(result, 0, comparator);
    return result;
}

/**
 * Helper function for recursive selection sort.
 * @private
 */
function selectionSortRecursiveHelper(arr, startIdx, comparator) {
    // Base case: if we've reached the end, we're done
    if (startIdx >= arr.length - 1) return;

    // Find the minimum element in arr[startIdx...n-1]
    let minIdx = startIdx;
    for (let i = startIdx + 1; i < arr.length; i++) {
        if (comparator(arr[i], arr[minIdx]) < 0) {
            minIdx = i;
        }
    }

    // Swap the minimum with the element at startIdx
    if (minIdx !== startIdx) {
        [arr[startIdx], arr[minIdx]] = [arr[minIdx], arr[startIdx]];
    }

    // Recursively sort the rest
    selectionSortRecursiveHelper(arr, startIdx + 1, comparator);
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
 * @param {Array} arr - The array to sort
 * @param {Function} [comparator] - Optional comparison function
 * @returns {Array} A new sorted array
 */
function stableSelectionSort(arr, comparator = (a, b) => a - b) {
    if (arr.length <= 1) return [...arr];

    const result = [...arr];
    const n = result.length;

    for (let i = 0; i < n - 1; i++) {
        // Find minimum in unsorted portion
        let minIdx = i;
        for (let j = i + 1; j < n; j++) {
            if (comparator(result[j], result[minIdx]) < 0) {
                minIdx = j;
            }
        }

        // Instead of swapping, shift elements and insert
        if (minIdx !== i) {
            const minValue = result[minIdx];
            // Shift all elements between i and minIdx one position right
            for (let k = minIdx; k > i; k--) {
                result[k] = result[k - 1];
            }
            // Place minimum at position i
            result[i] = minValue;
        }
    }

    return result;
}

// ============================================================================
// VISUALIZATION AND STATISTICS
// ============================================================================

/**
 * Class to track sorting operations for analysis.
 */
class SortStatistics {
    constructor() {
        this.comparisons = 0;
        this.swaps = 0;
        this.arrayAccesses = 0;
    }

    reset() {
        this.comparisons = 0;
        this.swaps = 0;
        this.arrayAccesses = 0;
    }

    toString() {
        return `Comparisons: ${this.comparisons}, Swaps: ${this.swaps}, Array Accesses: ${this.arrayAccesses}`;
    }
}

/**
 * Selection sort with operation counting.
 */
function selectionSortWithStats(arr, stats) {
    stats.reset();
    if (arr.length <= 1) return [...arr];

    const result = [...arr];
    const n = result.length;

    for (let i = 0; i < n - 1; i++) {
        let minIdx = i;
        stats.arrayAccesses++;

        for (let j = i + 1; j < n; j++) {
            stats.comparisons++;
            stats.arrayAccesses += 2;  // Read result[j] and result[minIdx]
            if (result[j] < result[minIdx]) {
                minIdx = j;
            }
        }

        if (minIdx !== i) {
            stats.swaps++;
            stats.arrayAccesses += 4;  // Two reads, two writes
            [result[i], result[minIdx]] = [result[minIdx], result[i]];
        }
    }

    return result;
}

/**
 * Create ASCII visualization of selection sort process.
 */
function visualizeSelectionSort(arr) {
    const steps = [];
    const result = [...arr];
    const n = result.length;

    steps.push('='.repeat(70));
    steps.push('SELECTION SORT VISUALIZATION');
    steps.push('='.repeat(70));
    steps.push(`Initial array: [${result.join(', ')}]`);
    steps.push('');

    for (let i = 0; i < n - 1; i++) {
        steps.push(`Pass ${i + 1}:`);
        const unsortedPortion = result.slice(i);
        steps.push(`  Looking for minimum in unsorted portion: [${unsortedPortion.join(', ')}]`);

        let minIdx = i;
        let minValue = result[i];

        // Show the search process
        for (let j = i + 1; j < n; j++) {
            if (result[j] < minValue) {
                minIdx = j;
                minValue = result[j];
                steps.push(`    Found new minimum: ${minValue} at index ${minIdx}`);
            }
        }

        // Show the swap
        if (minIdx !== i) {
            steps.push(`  Swapping ${result[i]} ↔ ${result[minIdx]}`);
            [result[i], result[minIdx]] = [result[minIdx], result[i]];
        } else {
            steps.push(`  No swap needed (minimum already in place)`);
        }

        // Show current state
        const sortedPart = result.slice(0, i + 1);
        const unsortedPart = result.slice(i + 1);
        steps.push(`  Sorted: [${sortedPart.join(', ')}] | Unsorted: [${unsortedPart.join(', ')}]`);
        steps.push('');
    }

    steps.push(`Final sorted array: [${result.join(', ')}]`);
    steps.push('='.repeat(70));

    return steps;
}

// ============================================================================
// ARRAY PROTOTYPE EXTENSIONS
// ============================================================================

/**
 * Extend Array prototype with selection sort methods
 */
Array.prototype.selectionSort = function(comparator) {
    return selectionSort(this, comparator);
};

Array.prototype.selectionSortInPlace = function(comparator) {
    selectionSortInPlace(this, comparator);
    return this;
};

// ============================================================================
// COMPARISON WITH OTHER O(n²) ALGORITHMS
// ============================================================================

/**
 * Compare selection sort with other O(n²) algorithms.
 */
function compareQuadraticSorts(arr) {
    const results = {};

    // Selection Sort
    const statsSelection = new SortStatistics();
    selectionSortWithStats(arr, statsSelection);
    results['Selection Sort'] = {
        comparisons: statsSelection.comparisons,
        swaps: statsSelection.swaps,
        arrayAccesses: statsSelection.arrayAccesses
    };

    // Bubble Sort (for comparison)
    const statsBubble = new SortStatistics();
    const bubbleSort = (arr, stats) => {
        stats.reset();
        const result = [...arr];
        const n = result.length;
        for (let i = 0; i < n; i++) {
            let swapped = false;
            for (let j = 0; j < n - i - 1; j++) {
                stats.comparisons++;
                stats.arrayAccesses += 2;
                if (result[j] > result[j + 1]) {
                    stats.swaps++;
                    stats.arrayAccesses += 4;
                    [result[j], result[j + 1]] = [result[j + 1], result[j]];
                    swapped = true;
                }
            }
            if (!swapped) break;
        }
        return result;
    };
    bubbleSort(arr, statsBubble);
    results['Bubble Sort'] = {
        comparisons: statsBubble.comparisons,
        swaps: statsBubble.swaps,
        arrayAccesses: statsBubble.arrayAccesses
    };

    // Insertion Sort (for comparison)
    const statsInsertion = new SortStatistics();
    const insertionSort = (arr, stats) => {
        stats.reset();
        const result = [...arr];
        const n = result.length;
        for (let i = 1; i < n; i++) {
            const key = result[i];
            stats.arrayAccesses++;
            let j = i - 1;
            while (j >= 0) {
                stats.comparisons++;
                stats.arrayAccesses++;
                if (result[j] > key) {
                    stats.swaps++;
                    stats.arrayAccesses += 2;
                    result[j + 1] = result[j];
                    j--;
                } else {
                    break;
                }
            }
            result[j + 1] = key;
            stats.arrayAccesses++;
        }
        return result;
    };
    insertionSort(arr, statsInsertion);
    results['Insertion Sort'] = {
        comparisons: statsInsertion.comparisons,
        swaps: statsInsertion.swaps,
        arrayAccesses: statsInsertion.arrayAccesses
    };

    return results;
}

// ============================================================================
// DEMONSTRATIONS AND TESTING
// ============================================================================

function demonstrateSelectionSort() {
    console.log('📚 SELECTION SORT - EDUCATIONAL DEMONSTRATION');
    console.log('='.repeat(80));

    // Test cases
    const testCases = [
        { arr: [64, 25, 12, 22, 11], desc: 'Random array' },
        { arr: [5, 2, 8, 6, 1, 9, 4], desc: 'Small random array' },
        { arr: [1], desc: 'Single element' },
        { arr: [], desc: 'Empty array' },
        { arr: [3, 3, 3, 3, 3], desc: 'All duplicates' },
        { arr: [9, 8, 7, 6, 5, 4, 3, 2, 1], desc: 'Reverse sorted' },
        { arr: [1, 2, 3, 4, 5], desc: 'Already sorted' },
        { arr: [1, 3, 2, 4, 5], desc: 'Nearly sorted' }
    ];

    console.log('\n📋 BASIC FUNCTIONALITY TESTS:');
    console.log('-'.repeat(80));

    testCases.forEach(({ arr, desc }) => {
        const original = [...arr];
        const standard = selectionSort(arr);
        const bidirectional = bidirectionalSelectionSort(arr);
        const recursive = selectionSortRecursive(arr);
        const stable = stableSelectionSort(arr);

        console.log(`\nTest: ${desc}`);
        console.log(`Original:      [${original.join(', ')}]`);
        console.log(`Standard:      [${standard.join(', ')}]`);
        console.log(`Bidirectional: [${bidirectional.join(', ')}]`);
        console.log(`Recursive:     [${recursive.join(', ')}]`);
        console.log(`Stable:        [${stable.join(', ')}]`);

        const allEqual = JSON.stringify(standard) === JSON.stringify([...arr].sort((a, b) => a - b));
        const status = allEqual ? '✓' : '✗';
        console.log(`All correct: ${status}`);
    });

    // Visualization
    console.log('\n\n🎬 STEP-BY-STEP VISUALIZATION:');
    console.log('-'.repeat(80));
    const demoArr = [64, 25, 12, 22, 11];
    const steps = visualizeSelectionSort(demoArr);
    steps.forEach(step => console.log(step));

    // Statistics comparison
    console.log('\n\n📊 ALGORITHM COMPARISON (O(n²) Algorithms):');
    console.log('-'.repeat(80));

    const comparisonCases = [
        { arr: [5, 2, 8, 6, 1], desc: 'Random' },
        { arr: [1, 2, 3, 4, 5], desc: 'Already sorted' },
        { arr: [5, 4, 3, 2, 1], desc: 'Reverse sorted' }
    ];

    comparisonCases.forEach(({ arr, desc }) => {
        console.log(`\n${desc}: [${arr.join(', ')}]`);
        const results = compareQuadraticSorts(arr);

        console.log(`${'Algorithm'.padEnd(20)} ${'Comparisons'.padEnd(15)} ${'Swaps'.padEnd(15)} ${'Array Accesses'.padEnd(15)}`);
        console.log('-'.repeat(65));
        Object.entries(results).forEach(([algo, stats]) => {
            console.log(`${algo.padEnd(20)} ${String(stats.comparisons).padEnd(15)} ${String(stats.swaps).padEnd(15)} ${String(stats.arrayAccesses).padEnd(15)}`);
        });

        // Analysis
        const selSwaps = results['Selection Sort'].swaps;
        const bubSwaps = results['Bubble Sort'].swaps;
        const insSwaps = results['Insertion Sort'].swaps;

        console.log(`\n  Key Observation:`);
        console.log(`  - Selection Sort made ${selSwaps} swaps (minimum among all)`);
        console.log(`  - Bubble Sort made ${bubSwaps} swaps`);
        console.log(`  - Insertion Sort made ${insSwaps} swaps`);
    });
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        selectionSort,
        selectionSortInPlace,
        bidirectionalSelectionSort,
        selectionSortRecursive,
        stableSelectionSort,
        visualizeSelectionSort,
        compareQuadraticSorts,
        demonstrateSelectionSort,
        SortStatistics
    };
}

// Run demonstration if executed directly
if (typeof require !== 'undefined' && require.main === module) {
    demonstrateSelectionSort();
}
