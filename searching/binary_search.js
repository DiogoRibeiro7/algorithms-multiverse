/**
 * Comprehensive Binary Search Algorithm Collection - JavaScript
 * =============================================================
 *
 * A complete collection of binary search algorithms and variants
 * implemented in modern JavaScript (ES6+).
 *
 * Algorithms included:
 * 1. Classic Binary Search (iterative & recursive)
 * 2. First/Last Occurrence
 * 3. Rotated Sorted Array Search
 * 4. Exponential Search
 * 5. Interpolation Search
 * 6. Ternary Search
 * 7. Binary Search on Answer (optimization problems)
 * 8. Advanced Utilities (peak finding, insertion position, etc.)
 *
 * Time Complexity: O(log n) for most variants
 * Space Complexity: O(1) iterative, O(log n) recursive
 *
 * Usage: node binary_search.js
 */

// ============================================================================
// 1. CLASSIC BINARY SEARCH
// ============================================================================

/**
 * Classic binary search - Iterative implementation
 *
 * @param {number[]} arr - Sorted array
 * @param {number} target - Element to search for
 * @returns {number} Index of target, or -1 if not found
 *
 * Time: O(log n), Space: O(1)
 */
function binarySearchIterative(arr, target) {
    let left = 0;
    let right = arr.length - 1;

    while (left <= right) {
        // Avoid integer overflow
        const mid = left + Math.floor((right - left) / 2);

        if (arr[mid] === target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}

/**
 * Classic binary search - Recursive implementation
 *
 * @param {number[]} arr - Sorted array
 * @param {number} target - Element to search for
 * @param {number} left - Left boundary (default 0)
 * @param {number} right - Right boundary (default arr.length - 1)
 * @returns {number} Index of target, or -1 if not found
 *
 * Time: O(log n), Space: O(log n) due to recursion
 */
function binarySearchRecursive(arr, target, left = 0, right = arr.length - 1) {
    if (left > right) {
        return -1;
    }

    const mid = left + Math.floor((right - left) / 2);

    if (arr[mid] === target) {
        return mid;
    } else if (arr[mid] < target) {
        return binarySearchRecursive(arr, target, mid + 1, right);
    } else {
        return binarySearchRecursive(arr, target, left, mid - 1);
    }
}

/**
 * Generic binary search with custom comparator
 *
 * @param {Array} arr - Sorted array
 * @param {*} target - Element to search for
 * @param {Function} compareFn - Comparator function (a, b) => number
 * @returns {number} Index of target, or -1 if not found
 */
function binarySearchWithComparator(arr, target, compareFn) {
    let left = 0;
    let right = arr.length - 1;

    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2);
        const cmp = compareFn(arr[mid], target);

        if (cmp === 0) {
            return mid;
        } else if (cmp < 0) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}

// ============================================================================
// 2. FIRST/LAST OCCURRENCE (for arrays with duplicates)
// ============================================================================

/**
 * Find first occurrence of target in sorted array
 *
 * @param {number[]} arr - Sorted array (may contain duplicates)
 * @param {number} target - Element to search for
 * @returns {number} Index of first occurrence, or -1 if not found
 *
 * Time: O(log n), Space: O(1)
 */
function findFirstOccurrence(arr, target) {
    let left = 0;
    let right = arr.length - 1;
    let result = -1;

    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2);

        if (arr[mid] === target) {
            result = mid;
            right = mid - 1;  // Continue searching left
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return result;
}

/**
 * Find last occurrence of target in sorted array
 *
 * @param {number[]} arr - Sorted array (may contain duplicates)
 * @param {number} target - Element to search for
 * @returns {number} Index of last occurrence, or -1 if not found
 *
 * Time: O(log n), Space: O(1)
 */
function findLastOccurrence(arr, target) {
    let left = 0;
    let right = arr.length - 1;
    let result = -1;

    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2);

        if (arr[mid] === target) {
            result = mid;
            left = mid + 1;  // Continue searching right
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return result;
}

/**
 * Count occurrences of target in sorted array
 *
 * @param {number[]} arr - Sorted array
 * @param {number} target - Element to count
 * @returns {number} Count of occurrences
 *
 * Time: O(log n), Space: O(1)
 */
function countOccurrences(arr, target) {
    const first = findFirstOccurrence(arr, target);
    if (first === -1) return 0;

    const last = findLastOccurrence(arr, target);
    return last - first + 1;
}

/**
 * Find range [first, last] of target occurrences
 *
 * @param {number[]} arr - Sorted array
 * @param {number} target - Element to search for
 * @returns {number[]} [first, last] indices, or [-1, -1] if not found
 */
function findRange(arr, target) {
    const first = findFirstOccurrence(arr, target);
    if (first === -1) return [-1, -1];

    const last = findLastOccurrence(arr, target);
    return [first, last];
}

// ============================================================================
// 3. ROTATED SORTED ARRAY SEARCH
// ============================================================================

/**
 * Search in rotated sorted array
 *
 * Example: [4, 5, 6, 7, 0, 1, 2] (rotated from [0, 1, 2, 4, 5, 6, 7])
 *
 * @param {number[]} arr - Rotated sorted array
 * @param {number} target - Element to search for
 * @returns {number} Index of target, or -1 if not found
 *
 * Time: O(log n), Space: O(1)
 */
function searchRotatedArray(arr, target) {
    let left = 0;
    let right = arr.length - 1;

    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2);

        if (arr[mid] === target) {
            return mid;
        }

        // Determine which half is sorted
        if (arr[left] <= arr[mid]) {
            // Left half is sorted
            if (arr[left] <= target && target < arr[mid]) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        } else {
            // Right half is sorted
            if (arr[mid] < target && target <= arr[right]) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
    }

    return -1;
}

/**
 * Find rotation point (minimum element) in rotated sorted array
 *
 * @param {number[]} arr - Rotated sorted array
 * @returns {number} Index of minimum element (rotation point)
 *
 * Time: O(log n), Space: O(1)
 */
function findRotationPoint(arr) {
    let left = 0;
    let right = arr.length - 1;

    while (left < right) {
        const mid = left + Math.floor((right - left) / 2);

        if (arr[mid] > arr[right]) {
            // Minimum is in right half
            left = mid + 1;
        } else {
            // Minimum is in left half (or mid)
            right = mid;
        }
    }

    return left;
}

// ============================================================================
// 4. EXPONENTIAL SEARCH
// ============================================================================

/**
 * Exponential search - finds range then applies binary search
 *
 * Good for unbounded/infinite arrays and when target is near beginning
 *
 * @param {number[]} arr - Sorted array
 * @param {number} target - Element to search for
 * @returns {number} Index of target, or -1 if not found
 *
 * Time: O(log n), Space: O(1)
 */
function exponentialSearch(arr, target) {
    const n = arr.length;

    if (n === 0) return -1;
    if (arr[0] === target) return 0;

    // Find range for binary search
    let i = 1;
    while (i < n && arr[i] <= target) {
        i *= 2;
    }

    // Binary search in range [i/2, min(i, n-1)]
    let left = Math.floor(i / 2);
    let right = Math.min(i, n - 1);

    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2);

        if (arr[mid] === target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}

// ============================================================================
// 5. INTERPOLATION SEARCH
// ============================================================================

/**
 * Interpolation search - uses value information to estimate position
 *
 * Best for uniformly distributed numerical data
 * O(log log n) average, O(n) worst case
 *
 * @param {number[]} arr - Sorted array of numbers
 * @param {number} target - Element to search for
 * @returns {number} Index of target, or -1 if not found
 *
 * Time: O(log log n) average, O(n) worst
 * Space: O(1)
 */
function interpolationSearch(arr, target) {
    let left = 0;
    let right = arr.length - 1;

    while (left <= right && target >= arr[left] && target <= arr[right]) {
        if (left === right) {
            return arr[left] === target ? left : -1;
        }

        // Interpolation formula
        const pos = left + Math.floor(
            ((target - arr[left]) * (right - left)) /
            (arr[right] - arr[left])
        );

        if (arr[pos] === target) {
            return pos;
        } else if (arr[pos] < target) {
            left = pos + 1;
        } else {
            right = pos - 1;
        }
    }

    return -1;
}

// ============================================================================
// 6. TERNARY SEARCH
// ============================================================================

/**
 * Ternary search on sorted array (3-way division)
 *
 * @param {number[]} arr - Sorted array
 * @param {number} target - Element to search for
 * @returns {number} Index of target, or -1 if not found
 *
 * Time: O(log₃ n) ≈ O(log n)
 * Space: O(1)
 */
function ternarySearch(arr, target) {
    let left = 0;
    let right = arr.length - 1;

    while (left <= right) {
        const mid1 = left + Math.floor((right - left) / 3);
        const mid2 = right - Math.floor((right - left) / 3);

        if (arr[mid1] === target) return mid1;
        if (arr[mid2] === target) return mid2;

        if (target < arr[mid1]) {
            right = mid1 - 1;
        } else if (target > arr[mid2]) {
            left = mid2 + 1;
        } else {
            left = mid1 + 1;
            right = mid2 - 1;
        }
    }

    return -1;
}

/**
 * Ternary search for finding maximum of unimodal function
 *
 * @param {Function} fn - Unimodal function
 * @param {number} left - Left boundary
 * @param {number} right - Right boundary
 * @param {number} precision - Precision for convergence
 * @returns {number} x value where f(x) is maximum
 *
 * Time: O(log₃(range/precision))
 */
function ternarySearchMaximum(fn, left, right, precision = 1e-6) {
    while (right - left > precision) {
        const mid1 = left + (right - left) / 3;
        const mid2 = right - (right - left) / 3;

        if (fn(mid1) < fn(mid2)) {
            left = mid1;
        } else {
            right = mid2;
        }
    }

    return (left + right) / 2;
}

// ============================================================================
// 7. BINARY SEARCH ON ANSWER (Optimization Problems)
// ============================================================================

/**
 * Binary search on answer space with predicate function
 *
 * Finds smallest value in range where predicate returns true
 *
 * @param {Function} predicate - Function that returns boolean
 * @param {number} left - Minimum possible answer
 * @param {number} right - Maximum possible answer
 * @returns {number} Smallest value where predicate is true
 *
 * Time: O(log(range) * T) where T is predicate evaluation time
 */
function binarySearchOnAnswer(predicate, left, right) {
    let result = right + 1;

    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2);

        if (predicate(mid)) {
            result = mid;
            right = mid - 1;  // Try to find smaller answer
        } else {
            left = mid + 1;
        }
    }

    return result;
}

/**
 * Find integer square root using binary search
 *
 * @param {number} n - Number to find square root of
 * @returns {number} Floor of square root
 *
 * Time: O(log n), Space: O(1)
 */
function findSquareRoot(n) {
    if (n < 0) throw new Error("Square root of negative number");
    if (n <= 1) return n;

    let left = 1;
    let right = Math.floor(n / 2);
    let result = 1;

    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2);
        const square = mid * mid;

        if (square === n) {
            return mid;
        } else if (square < n) {
            result = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return result;
}

/**
 * Find square root with decimal precision
 *
 * @param {number} n - Number to find square root of
 * @param {number} precision - Decimal places of precision
 * @returns {number} Square root with specified precision
 */
function findSquareRootDecimal(n, precision = 2) {
    if (n < 0) throw new Error("Square root of negative number");
    if (n <= 1) return n;

    let left = 0;
    let right = n;
    const epsilon = Math.pow(10, -precision);

    while (right - left > epsilon) {
        const mid = (left + right) / 2;
        const square = mid * mid;

        if (Math.abs(square - n) < epsilon) {
            return parseFloat(mid.toFixed(precision));
        } else if (square < n) {
            left = mid;
        } else {
            right = mid;
        }
    }

    return parseFloat(((left + right) / 2).toFixed(precision));
}

/**
 * Find nth root using binary search
 *
 * @param {number} x - Number
 * @param {number} n - Root degree
 * @param {number} precision - Decimal precision
 * @returns {number} nth root of x
 */
function findNthRoot(x, n, precision = 2) {
    if (x < 0 && n % 2 === 0) {
        throw new Error("Even root of negative number");
    }

    let left = 0;
    let right = Math.max(1, x);
    const epsilon = Math.pow(10, -precision);

    while (right - left > epsilon) {
        const mid = (left + right) / 2;
        const power = Math.pow(mid, n);

        if (Math.abs(power - x) < epsilon) {
            return parseFloat(mid.toFixed(precision));
        } else if (power < x) {
            left = mid;
        } else {
            right = mid;
        }
    }

    return parseFloat(((left + right) / 2).toFixed(precision));
}

// ============================================================================
// 8. ADVANCED UTILITIES
// ============================================================================

/**
 * Find insertion position for element in sorted array
 *
 * @param {number[]} arr - Sorted array
 * @param {number} target - Element to insert
 * @returns {number} Index where target should be inserted
 *
 * Time: O(log n), Space: O(1)
 */
function findInsertPosition(arr, target) {
    let left = 0;
    let right = arr.length;

    while (left < right) {
        const mid = left + Math.floor((right - left) / 2);

        if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    return left;
}

/**
 * Find closest element to target in sorted array
 *
 * @param {number[]} arr - Sorted array
 * @param {number} target - Target value
 * @returns {number} Index of closest element
 *
 * Time: O(log n), Space: O(1)
 */
function findClosest(arr, target) {
    if (arr.length === 0) return -1;
    if (arr.length === 1) return 0;

    let left = 0;
    let right = arr.length - 1;

    while (left < right - 1) {
        const mid = left + Math.floor((right - left) / 2);

        if (arr[mid] === target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid;
        } else {
            right = mid;
        }
    }

    // Compare distances
    const leftDist = Math.abs(arr[left] - target);
    const rightDist = Math.abs(arr[right] - target);

    return leftDist <= rightDist ? left : right;
}

/**
 * Find peak element in array (element greater than neighbors)
 *
 * @param {number[]} arr - Array (not necessarily sorted)
 * @returns {number} Index of a peak element
 *
 * Time: O(log n), Space: O(1)
 */
function findPeakElement(arr) {
    if (arr.length === 0) return -1;
    if (arr.length === 1) return 0;

    let left = 0;
    let right = arr.length - 1;

    while (left < right) {
        const mid = left + Math.floor((right - left) / 2);

        if (arr[mid] < arr[mid + 1]) {
            // Peak is on right
            left = mid + 1;
        } else {
            // Peak is on left or mid
            right = mid;
        }
    }

    return left;
}

// ============================================================================
// EXAMPLES AND TESTING
// ============================================================================

function runExamples() {
    console.log("=".repeat(70));
    console.log("BINARY SEARCH ALGORITHM COLLECTION - JAVASCRIPT");
    console.log("=".repeat(70));
    console.log();

    // Example 1: Classic Binary Search
    console.log("=".repeat(70));
    console.log("EXAMPLE 1: Classic Binary Search");
    console.log("=".repeat(70));

    const arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
    console.log(`Array: [${arr.join(", ")}]`);
    console.log(`Search for 7: index ${binarySearchIterative(arr, 7)}`);
    console.log(`Search for 11: index ${binarySearchRecursive(arr, 11)}`);
    console.log(`Search for 20: index ${binarySearchIterative(arr, 20)}`);
    console.log();

    // Example 2: First/Last Occurrence
    console.log("=".repeat(70));
    console.log("EXAMPLE 2: First/Last Occurrence (Duplicates)");
    console.log("=".repeat(70));

    const arrDup = [1, 2, 2, 2, 3, 4, 4, 5, 5, 5, 5];
    console.log(`Array: [${arrDup.join(", ")}]`);
    console.log(`First occurrence of 2: index ${findFirstOccurrence(arrDup, 2)}`);
    console.log(`Last occurrence of 2: index ${findLastOccurrence(arrDup, 2)}`);
    console.log(`Count of 5: ${countOccurrences(arrDup, 5)}`);
    console.log(`Range of 4: [${findRange(arrDup, 4).join(", ")}]`);
    console.log();

    // Example 3: Rotated Sorted Array
    console.log("=".repeat(70));
    console.log("EXAMPLE 3: Rotated Sorted Array");
    console.log("=".repeat(70));

    const rotated = [4, 5, 6, 7, 0, 1, 2];
    console.log(`Array: [${rotated.join(", ")}]`);
    console.log(`Search for 0: index ${searchRotatedArray(rotated, 0)}`);
    console.log(`Search for 5: index ${searchRotatedArray(rotated, 5)}`);
    console.log(`Rotation point: index ${findRotationPoint(rotated)}`);
    console.log();

    // Example 4: Square Root
    console.log("=".repeat(70));
    console.log("EXAMPLE 4: Square Root using Binary Search");
    console.log("=".repeat(70));

    console.log(`√50 (integer): ${findSquareRoot(50)}`);
    console.log(`√50 (decimal): ${findSquareRootDecimal(50, 2)}`);
    console.log(`∛27: ${findNthRoot(27, 3, 2)}`);
    console.log();

    // Example 5: Binary Search on Answer
    console.log("=".repeat(70));
    console.log("EXAMPLE 5: Binary Search on Answer - Ship Packages");
    console.log("=".repeat(70));

    const weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    const days = 5;

    function canShip(capacity) {
        let dayCount = 1;
        let currentWeight = 0;

        for (const w of weights) {
            if (currentWeight + w > capacity) {
                dayCount++;
                currentWeight = w;
            } else {
                currentWeight += w;
            }
        }

        return dayCount <= days;
    }

    const minCapacity = binarySearchOnAnswer(canShip, 1, 55);
    console.log(`Weights: [${weights.join(", ")}]`);
    console.log(`Days: ${days}`);
    console.log(`Minimum ship capacity: ${minCapacity}`);
    console.log();

    // Example 6: Peak Element
    console.log("=".repeat(70));
    console.log("EXAMPLE 6: Find Peak Element");
    console.log("=".repeat(70));

    const peaks = [1, 3, 20, 4, 1, 0];
    const peakIdx = findPeakElement(peaks);
    console.log(`Array: [${peaks.join(", ")}]`);
    console.log(`Peak at index ${peakIdx}, value: ${peaks[peakIdx]}`);
    console.log();

    console.log("=".repeat(70));
    console.log("All examples completed!");
    console.log("=".repeat(70));
}

// Run examples if executed directly
if (typeof require !== 'undefined' && require.main === module) {
    runExamples();
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        binarySearchIterative,
        binarySearchRecursive,
        binarySearchWithComparator,
        findFirstOccurrence,
        findLastOccurrence,
        countOccurrences,
        findRange,
        searchRotatedArray,
        findRotationPoint,
        exponentialSearch,
        interpolationSearch,
        ternarySearch,
        ternarySearchMaximum,
        binarySearchOnAnswer,
        findSquareRoot,
        findSquareRootDecimal,
        findNthRoot,
        findInsertPosition,
        findClosest,
        findPeakElement
    };
}
