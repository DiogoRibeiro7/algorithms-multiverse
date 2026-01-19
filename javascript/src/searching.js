/**
 * @module searching
 * @description Searching algorithms implementation
 */

/**
 * Linear Search - O(n) time, O(1) space
 * @param {Array} arr - Array to search in
 * @param {*} target - Element to find
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Object} {found: boolean, index: number, comparisons: number}
 */
export function linearSearch(arr, target, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    let comparisons = 0;

    for (let i = 0; i < arr.length; i++) {
        comparisons++;
        if (compareFunc(arr[i], target) === 0) {
            return { found: true, index: i, comparisons };
        }
    }

    return { found: false, index: -1, comparisons };
}

/**
 * Binary Search - O(log n) time, O(1) space
 * Requires sorted array
 * @param {Array} arr - Sorted array to search in
 * @param {*} target - Element to find
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Object} {found: boolean, index: number, comparisons: number}
 */
export function binarySearch(arr, target, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    let left = 0;
    let right = arr.length - 1;
    let comparisons = 0;

    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        comparisons++;
        const cmp = compareFunc(arr[mid], target);

        if (cmp === 0) {
            return { found: true, index: mid, comparisons };
        } else if (cmp < 0) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return { found: false, index: -1, comparisons };
}

/**
 * Binary Search Recursive - O(log n) time, O(log n) space
 * @param {Array} arr - Sorted array
 * @param {*} target - Element to find
 * @param {number} [left=0] - Left boundary
 * @param {number} [right] - Right boundary
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Object} {found: boolean, index: number}
 */
export function binarySearchRecursive(arr, target, left = 0, right = arr.length - 1, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    if (left > right) {
        return { found: false, index: -1 };
    }

    const mid = Math.floor((left + right) / 2);
    const cmp = compareFunc(arr[mid], target);

    if (cmp === 0) {
        return { found: true, index: mid };
    } else if (cmp < 0) {
        return binarySearchRecursive(arr, target, mid + 1, right, compareFunc);
    } else {
        return binarySearchRecursive(arr, target, left, mid - 1, compareFunc);
    }
}

/**
 * Jump Search - O(√n) time, O(1) space
 * Requires sorted array
 * @param {Array} arr - Sorted array
 * @param {*} target - Element to find
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Object} {found: boolean, index: number, comparisons: number}
 */
export function jumpSearch(arr, target, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    const n = arr.length;
    const step = Math.floor(Math.sqrt(n));
    let prev = 0;
    let comparisons = 0;

    // Jump to find the block where element is present
    while (arr[Math.min(step, n) - 1] < target) {
        comparisons++;
        prev = step;
        step += Math.floor(Math.sqrt(n));
        if (prev >= n) {
            return { found: false, index: -1, comparisons };
        }
    }

    // Linear search in the block
    while (arr[prev] < target) {
        comparisons++;
        prev++;
        if (prev === Math.min(step, n)) {
            return { found: false, index: -1, comparisons };
        }
    }

    comparisons++;
    if (compareFunc(arr[prev], target) === 0) {
        return { found: true, index: prev, comparisons };
    }

    return { found: false, index: -1, comparisons };
}

/**
 * Interpolation Search - O(log log n) average, O(n) worst time
 * Best for uniformly distributed sorted arrays
 * @param {Array<number>} arr - Sorted array of numbers
 * @param {number} target - Number to find
 * @returns {Object} {found: boolean, index: number, comparisons: number}
 */
export function interpolationSearch(arr, target) {
    let left = 0;
    let right = arr.length - 1;
    let comparisons = 0;

    while (left <= right && target >= arr[left] && target <= arr[right]) {
        if (left === right) {
            comparisons++;
            if (arr[left] === target) {
                return { found: true, index: left, comparisons };
            }
            return { found: false, index: -1, comparisons };
        }

        // Estimate position
        const pos = left + Math.floor(
            ((target - arr[left]) / (arr[right] - arr[left])) * (right - left)
        );

        comparisons++;
        if (arr[pos] === target) {
            return { found: true, index: pos, comparisons };
        }

        if (arr[pos] < target) {
            left = pos + 1;
        } else {
            right = pos - 1;
        }
    }

    return { found: false, index: -1, comparisons };
}

/**
 * Exponential Search - O(log n) time, O(1) space
 * Good for unbounded or infinite arrays
 * @param {Array} arr - Sorted array
 * @param {*} target - Element to find
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Object} {found: boolean, index: number, comparisons: number}
 */
export function exponentialSearch(arr, target, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    const n = arr.length;
    let comparisons = 0;

    // If target is at first position
    comparisons++;
    if (compareFunc(arr[0], target) === 0) {
        return { found: true, index: 0, comparisons };
    }

    // Find range for binary search
    let i = 1;
    while (i < n && compareFunc(arr[i], target) <= 0) {
        comparisons++;
        if (compareFunc(arr[i], target) === 0) {
            return { found: true, index: i, comparisons };
        }
        i *= 2;
    }

    // Binary search in the range
    const result = binarySearch(
        arr.slice(Math.floor(i / 2), Math.min(i, n)),
        target,
        compareFunc
    );

    if (result.found) {
        result.index += Math.floor(i / 2);
    }
    result.comparisons += comparisons;

    return result;
}

/**
 * Fibonacci Search - O(log n) time, O(1) space
 * @param {Array} arr - Sorted array
 * @param {*} target - Element to find
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Object} {found: boolean, index: number, comparisons: number}
 */
export function fibonacciSearch(arr, target, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    const n = arr.length;
    let comparisons = 0;

    // Initialize Fibonacci numbers
    let fib2 = 0;  // (m-2)th Fibonacci number
    let fib1 = 1;  // (m-1)th Fibonacci number
    let fibM = fib2 + fib1;  // mth Fibonacci number

    // Find smallest Fibonacci number >= n
    while (fibM < n) {
        fib2 = fib1;
        fib1 = fibM;
        fibM = fib2 + fib1;
    }

    let offset = -1;

    while (fibM > 1) {
        const i = Math.min(offset + fib2, n - 1);
        comparisons++;

        const cmp = compareFunc(arr[i], target);
        if (cmp < 0) {
            fibM = fib1;
            fib1 = fib2;
            fib2 = fibM - fib1;
            offset = i;
        } else if (cmp > 0) {
            fibM = fib2;
            fib1 = fib1 - fib2;
            fib2 = fibM - fib1;
        } else {
            return { found: true, index: i, comparisons };
        }
    }

    // Check last element
    if (fib1 && offset + 1 < n) {
        comparisons++;
        if (compareFunc(arr[offset + 1], target) === 0) {
            return { found: true, index: offset + 1, comparisons };
        }
    }

    return { found: false, index: -1, comparisons };
}

/**
 * Ternary Search - O(log₃ n) time, O(1) space
 * @param {Array} arr - Sorted array
 * @param {*} target - Element to find
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Object} {found: boolean, index: number, comparisons: number}
 */
export function ternarySearch(arr, target, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    let left = 0;
    let right = arr.length - 1;
    let comparisons = 0;

    while (left <= right) {
        const mid1 = left + Math.floor((right - left) / 3);
        const mid2 = right - Math.floor((right - left) / 3);

        comparisons++;
        if (compareFunc(arr[mid1], target) === 0) {
            return { found: true, index: mid1, comparisons };
        }

        comparisons++;
        if (compareFunc(arr[mid2], target) === 0) {
            return { found: true, index: mid2, comparisons };
        }

        if (compareFunc(arr[mid1], target) > 0) {
            right = mid1 - 1;
        } else if (compareFunc(arr[mid2], target) < 0) {
            left = mid2 + 1;
        } else {
            left = mid1 + 1;
            right = mid2 - 1;
        }
    }

    return { found: false, index: -1, comparisons };
}

/**
 * Find minimum element in array
 * @param {Array} arr - Array to search
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Object} {value: *, index: number}
 */
export function findMin(arr, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    if (arr.length === 0) return { value: undefined, index: -1 };

    let minValue = arr[0];
    let minIndex = 0;

    for (let i = 1; i < arr.length; i++) {
        if (compareFunc(arr[i], minValue) < 0) {
            minValue = arr[i];
            minIndex = i;
        }
    }

    return { value: minValue, index: minIndex };
}

/**
 * Find maximum element in array
 * @param {Array} arr - Array to search
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Object} {value: *, index: number}
 */
export function findMax(arr, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    if (arr.length === 0) return { value: undefined, index: -1 };

    let maxValue = arr[0];
    let maxIndex = 0;

    for (let i = 1; i < arr.length; i++) {
        if (compareFunc(arr[i], maxValue) > 0) {
            maxValue = arr[i];
            maxIndex = i;
        }
    }

    return { value: maxValue, index: maxIndex };
}

/**
 * Find kth smallest element (Quick Select algorithm)
 * @param {Array} arr - Array to search
 * @param {number} k - k value (1-indexed)
 * @param {Function} [compareFunc] - Comparison function
 * @returns {*} kth smallest element
 */
export function findKthSmallest(arr, k, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    if (k <= 0 || k > arr.length) return undefined;

    const sorted = [...arr].sort(compareFunc);
    return sorted[k - 1];
}

/**
 * Find kth largest element
 * @param {Array} arr - Array to search
 * @param {number} k - k value (1-indexed)
 * @param {Function} [compareFunc] - Comparison function
 * @returns {*} kth largest element
 */
export function findKthLargest(arr, k, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    if (k <= 0 || k > arr.length) return undefined;

    const sorted = [...arr].sort((a, b) => -compareFunc(a, b));
    return sorted[k - 1];
}

/**
 * Two Sum Problem - Find two numbers that add up to target
 * @param {Array<number>} arr - Array of numbers
 * @param {number} target - Target sum
 * @returns {Object} {found: boolean, indices: [i, j], values: [a, b]}
 */
export function twoSum(arr, target) {
    const seen = new Map();

    for (let i = 0; i < arr.length; i++) {
        const complement = target - arr[i];
        if (seen.has(complement)) {
            return {
                found: true,
                indices: [seen.get(complement), i],
                values: [complement, arr[i]]
            };
        }
        seen.set(arr[i], i);
    }

    return { found: false, indices: [], values: [] };
}

/**
 * Three Sum Problem - Find three numbers that add up to target
 * @param {Array<number>} arr - Array of numbers
 * @param {number} target - Target sum
 * @returns {Array} Array of triplets
 */
export function threeSum(arr, target = 0) {
    const n = arr.length;
    const result = [];
    const sorted = [...arr].sort((a, b) => a - b);

    for (let i = 0; i < n - 2; i++) {
        // Skip duplicates
        if (i > 0 && sorted[i] === sorted[i - 1]) continue;

        let left = i + 1;
        let right = n - 1;

        while (left < right) {
            const sum = sorted[i] + sorted[left] + sorted[right];

            if (sum === target) {
                result.push([sorted[i], sorted[left], sorted[right]]);

                // Skip duplicates
                while (left < right && sorted[left] === sorted[left + 1]) left++;
                while (left < right && sorted[right] === sorted[right - 1]) right--;

                left++;
                right--;
            } else if (sum < target) {
                left++;
            } else {
                right--;
            }
        }
    }

    return result;
}

/**
 * Find peak element in array (element greater than neighbors)
 * @param {Array} arr - Array to search
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Object} {found: boolean, index: number, value: *}
 */
export function findPeak(arr, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    const n = arr.length;

    if (n === 0) return { found: false, index: -1, value: undefined };
    if (n === 1) return { found: true, index: 0, value: arr[0] };

    // Check first element
    if (compareFunc(arr[0], arr[1]) >= 0) {
        return { found: true, index: 0, value: arr[0] };
    }

    // Check last element
    if (compareFunc(arr[n - 1], arr[n - 2]) >= 0) {
        return { found: true, index: n - 1, value: arr[n - 1] };
    }

    // Binary search for peak
    let left = 1;
    let right = n - 2;

    while (left <= right) {
        const mid = Math.floor((left + right) / 2);

        if (compareFunc(arr[mid], arr[mid - 1]) >= 0 &&
            compareFunc(arr[mid], arr[mid + 1]) >= 0) {
            return { found: true, index: mid, value: arr[mid] };
        }

        if (compareFunc(arr[mid], arr[mid - 1]) < 0) {
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    }

    return { found: false, index: -1, value: undefined };
}

/**
 * Search in rotated sorted array
 * @param {Array} arr - Rotated sorted array
 * @param {*} target - Element to find
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Object} {found: boolean, index: number}
 */
export function searchRotated(arr, target, compareFunc = (a, b) => a === b ? 0 : (a < b ? -1 : 1)) {
    let left = 0;
    let right = arr.length - 1;

    while (left <= right) {
        const mid = Math.floor((left + right) / 2);

        if (compareFunc(arr[mid], target) === 0) {
            return { found: true, index: mid };
        }

        // Check which half is sorted
        if (compareFunc(arr[left], arr[mid]) <= 0) {
            // Left half is sorted
            if (compareFunc(arr[left], target) <= 0 && compareFunc(target, arr[mid]) < 0) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        } else {
            // Right half is sorted
            if (compareFunc(arr[mid], target) < 0 && compareFunc(target, arr[right]) <= 0) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
    }

    return { found: false, index: -1 };
}

// Export all searching algorithms
export default {
    linearSearch,
    binarySearch,
    binarySearchRecursive,
    jumpSearch,
    interpolationSearch,
    exponentialSearch,
    fibonacciSearch,
    ternarySearch,
    findMin,
    findMax,
    findKthSmallest,
    findKthLargest,
    twoSum,
    threeSum,
    findPeak,
    searchRotated
};