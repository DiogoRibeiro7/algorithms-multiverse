/**
 * @module sorting
 * @description Sorting algorithms implementation
 */

/**
 * Swap two elements in an array
 * @private
 */
function swap(arr, i, j) {
    [arr[i], arr[j]] = [arr[j], arr[i]];
}

/**
 * Default comparison function
 * @private
 */
function defaultCompare(a, b) {
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
}

/**
 * Bubble Sort - O(n²) time, O(1) space
 * @param {Array} arr - Array to sort
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Array} Sorted array
 */
export function bubbleSort(arr, compareFunc = defaultCompare) {
    const n = arr.length;
    const result = [...arr];

    for (let i = 0; i < n - 1; i++) {
        let swapped = false;
        for (let j = 0; j < n - i - 1; j++) {
            if (compareFunc(result[j], result[j + 1]) > 0) {
                swap(result, j, j + 1);
                swapped = true;
            }
        }
        if (!swapped) break;
    }

    return result;
}

/**
 * Insertion Sort - O(n²) time, O(1) space
 * @param {Array} arr - Array to sort
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Array} Sorted array
 */
export function insertionSort(arr, compareFunc = defaultCompare) {
    const result = [...arr];
    const n = result.length;

    for (let i = 1; i < n; i++) {
        const key = result[i];
        let j = i - 1;

        while (j >= 0 && compareFunc(result[j], key) > 0) {
            result[j + 1] = result[j];
            j--;
        }
        result[j + 1] = key;
    }

    return result;
}

/**
 * Selection Sort - O(n²) time, O(1) space
 * @param {Array} arr - Array to sort
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Array} Sorted array
 */
export function selectionSort(arr, compareFunc = defaultCompare) {
    const result = [...arr];
    const n = result.length;

    for (let i = 0; i < n - 1; i++) {
        let minIdx = i;
        for (let j = i + 1; j < n; j++) {
            if (compareFunc(result[j], result[minIdx]) < 0) {
                minIdx = j;
            }
        }
        if (minIdx !== i) {
            swap(result, i, minIdx);
        }
    }

    return result;
}

/**
 * Merge Sort - O(n log n) time, O(n) space
 * @param {Array} arr - Array to sort
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Array} Sorted array
 */
export function mergeSort(arr, compareFunc = defaultCompare) {
    if (arr.length <= 1) return [...arr];

    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid), compareFunc);
    const right = mergeSort(arr.slice(mid), compareFunc);

    return merge(left, right, compareFunc);
}

function merge(left, right, compareFunc) {
    const result = [];
    let i = 0, j = 0;

    while (i < left.length && j < right.length) {
        if (compareFunc(left[i], right[j]) <= 0) {
            result.push(left[i++]);
        } else {
            result.push(right[j++]);
        }
    }

    return result.concat(left.slice(i)).concat(right.slice(j));
}

/**
 * Quick Sort - O(n log n) average, O(n²) worst time, O(log n) space
 * @param {Array} arr - Array to sort
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Array} Sorted array
 */
export function quickSort(arr, compareFunc = defaultCompare) {
    if (arr.length <= 1) return [...arr];

    const result = [...arr];
    quickSortHelper(result, 0, result.length - 1, compareFunc);
    return result;
}

function quickSortHelper(arr, low, high, compareFunc) {
    if (low < high) {
        const pivotIdx = partition(arr, low, high, compareFunc);
        quickSortHelper(arr, low, pivotIdx - 1, compareFunc);
        quickSortHelper(arr, pivotIdx + 1, high, compareFunc);
    }
}

function partition(arr, low, high, compareFunc) {
    const pivot = arr[high];
    let i = low - 1;

    for (let j = low; j < high; j++) {
        if (compareFunc(arr[j], pivot) <= 0) {
            i++;
            swap(arr, i, j);
        }
    }

    swap(arr, i + 1, high);
    return i + 1;
}

/**
 * Heap Sort - O(n log n) time, O(1) space
 * @param {Array} arr - Array to sort
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Array} Sorted array
 */
export function heapSort(arr, compareFunc = defaultCompare) {
    const result = [...arr];
    const n = result.length;

    // Build heap
    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
        heapify(result, n, i, compareFunc);
    }

    // Extract elements from heap
    for (let i = n - 1; i > 0; i--) {
        swap(result, 0, i);
        heapify(result, i, 0, compareFunc);
    }

    return result;
}

function heapify(arr, n, i, compareFunc) {
    let largest = i;
    const left = 2 * i + 1;
    const right = 2 * i + 2;

    if (left < n && compareFunc(arr[left], arr[largest]) > 0) {
        largest = left;
    }

    if (right < n && compareFunc(arr[right], arr[largest]) > 0) {
        largest = right;
    }

    if (largest !== i) {
        swap(arr, i, largest);
        heapify(arr, n, largest, compareFunc);
    }
}

/**
 * Radix Sort - O(nk) time, O(n+k) space (for integers)
 * @param {Array<number>} arr - Array of non-negative integers
 * @returns {Array<number>} Sorted array
 */
export function radixSort(arr) {
    if (arr.length === 0) return [];

    const result = [...arr];
    const max = Math.max(...result);

    for (let exp = 1; Math.floor(max / exp) > 0; exp *= 10) {
        countingSortByDigit(result, exp);
    }

    return result;
}

function countingSortByDigit(arr, exp) {
    const n = arr.length;
    const output = new Array(n);
    const count = new Array(10).fill(0);

    // Count occurrences of each digit
    for (let i = 0; i < n; i++) {
        const digit = Math.floor(arr[i] / exp) % 10;
        count[digit]++;
    }

    // Calculate cumulative count
    for (let i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }

    // Build output array
    for (let i = n - 1; i >= 0; i--) {
        const digit = Math.floor(arr[i] / exp) % 10;
        output[count[digit] - 1] = arr[i];
        count[digit]--;
    }

    // Copy output to arr
    for (let i = 0; i < n; i++) {
        arr[i] = output[i];
    }
}

/**
 * Counting Sort - O(n+k) time, O(k) space
 * @param {Array<number>} arr - Array of non-negative integers
 * @param {number} [maxValue] - Maximum value in array
 * @returns {Array<number>} Sorted array
 */
export function countingSort(arr, maxValue = null) {
    if (arr.length === 0) return [];

    const max = maxValue ?? Math.max(...arr);
    const min = Math.min(...arr);
    const range = max - min + 1;
    const count = new Array(range).fill(0);
    const result = new Array(arr.length);

    // Count occurrences
    for (const num of arr) {
        count[num - min]++;
    }

    // Calculate cumulative count
    for (let i = 1; i < range; i++) {
        count[i] += count[i - 1];
    }

    // Build output array
    for (let i = arr.length - 1; i >= 0; i--) {
        result[count[arr[i] - min] - 1] = arr[i];
        count[arr[i] - min]--;
    }

    return result;
}

/**
 * Bucket Sort - O(n+k) average time, O(n) space
 * @param {Array<number>} arr - Array of numbers in range [0,1)
 * @param {number} [bucketSize] - Number of buckets
 * @returns {Array<number>} Sorted array
 */
export function bucketSort(arr, bucketSize = 10) {
    if (arr.length === 0) return [];

    // Find range
    const min = Math.min(...arr);
    const max = Math.max(...arr);
    const range = max - min;

    // Create buckets
    const bucketCount = Math.floor(range / bucketSize) + 1;
    const buckets = Array.from({ length: bucketCount }, () => []);

    // Distribute elements into buckets
    for (const num of arr) {
        const bucketIdx = Math.floor((num - min) / bucketSize);
        buckets[bucketIdx].push(num);
    }

    // Sort each bucket and concatenate
    const result = [];
    for (const bucket of buckets) {
        if (bucket.length > 0) {
            result.push(...insertionSort(bucket));
        }
    }

    return result;
}

/**
 * Tim Sort - Hybrid stable sort (merge + insertion)
 * O(n log n) time, O(n) space
 * @param {Array} arr - Array to sort
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Array} Sorted array
 */
export function timSort(arr, compareFunc = defaultCompare) {
    const MIN_MERGE = 32;
    const n = arr.length;
    const result = [...arr];

    // Sort individual runs using insertion sort
    for (let i = 0; i < n; i += MIN_MERGE) {
        const end = Math.min(i + MIN_MERGE, n);
        insertionSortRange(result, i, end, compareFunc);
    }

    // Merge runs
    let size = MIN_MERGE;
    while (size < n) {
        for (let start = 0; start < n; start += size * 2) {
            const mid = start + size;
            const end = Math.min(start + size * 2, n);
            if (mid < end) {
                mergeRange(result, start, mid, end, compareFunc);
            }
        }
        size *= 2;
    }

    return result;
}

function insertionSortRange(arr, left, right, compareFunc) {
    for (let i = left + 1; i < right; i++) {
        const key = arr[i];
        let j = i - 1;
        while (j >= left && compareFunc(arr[j], key) > 0) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

function mergeRange(arr, left, mid, right, compareFunc) {
    const leftPart = arr.slice(left, mid);
    const rightPart = arr.slice(mid, right);
    let i = 0, j = 0, k = left;

    while (i < leftPart.length && j < rightPart.length) {
        if (compareFunc(leftPart[i], rightPart[j]) <= 0) {
            arr[k++] = leftPart[i++];
        } else {
            arr[k++] = rightPart[j++];
        }
    }

    while (i < leftPart.length) {
        arr[k++] = leftPart[i++];
    }

    while (j < rightPart.length) {
        arr[k++] = rightPart[j++];
    }
}

/**
 * Shell Sort - O(n log n) to O(n²) time, O(1) space
 * @param {Array} arr - Array to sort
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Array} Sorted array
 */
export function shellSort(arr, compareFunc = defaultCompare) {
    const result = [...arr];
    const n = result.length;

    // Start with large gap, reduce by half each iteration
    for (let gap = Math.floor(n / 2); gap > 0; gap = Math.floor(gap / 2)) {
        for (let i = gap; i < n; i++) {
            const temp = result[i];
            let j = i;

            while (j >= gap && compareFunc(result[j - gap], temp) > 0) {
                result[j] = result[j - gap];
                j -= gap;
            }

            result[j] = temp;
        }
    }

    return result;
}

/**
 * Comb Sort - O(n²) worst case, better average than bubble sort
 * @param {Array} arr - Array to sort
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Array} Sorted array
 */
export function combSort(arr, compareFunc = defaultCompare) {
    const result = [...arr];
    const n = result.length;
    let gap = n;
    const shrink = 1.3;
    let sorted = false;

    while (gap > 1 || !sorted) {
        gap = Math.floor(gap / shrink);
        if (gap < 1) gap = 1;

        sorted = true;
        for (let i = 0; i + gap < n; i++) {
            if (compareFunc(result[i], result[i + gap]) > 0) {
                swap(result, i, i + gap);
                sorted = false;
            }
        }
    }

    return result;
}

/**
 * Gnome Sort - O(n²) time, O(1) space
 * @param {Array} arr - Array to sort
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Array} Sorted array
 */
export function gnomeSort(arr, compareFunc = defaultCompare) {
    const result = [...arr];
    const n = result.length;
    let i = 0;

    while (i < n) {
        if (i === 0 || compareFunc(result[i], result[i - 1]) >= 0) {
            i++;
        } else {
            swap(result, i, i - 1);
            i--;
        }
    }

    return result;
}

/**
 * Cocktail Sort (Bidirectional Bubble Sort) - O(n²) time, O(1) space
 * @param {Array} arr - Array to sort
 * @param {Function} [compareFunc] - Comparison function
 * @returns {Array} Sorted array
 */
export function cocktailSort(arr, compareFunc = defaultCompare) {
    const result = [...arr];
    const n = result.length;
    let left = 0;
    let right = n - 1;
    let swapped = true;

    while (swapped && left < right) {
        swapped = false;

        // Left to right
        for (let i = left; i < right; i++) {
            if (compareFunc(result[i], result[i + 1]) > 0) {
                swap(result, i, i + 1);
                swapped = true;
            }
        }
        right--;

        if (!swapped) break;

        swapped = false;

        // Right to left
        for (let i = right; i > left; i--) {
            if (compareFunc(result[i], result[i - 1]) < 0) {
                swap(result, i, i - 1);
                swapped = true;
            }
        }
        left++;
    }

    return result;
}

/**
 * Check if an array is sorted
 * @param {Array} arr - Array to check
 * @param {Function} [compareFunc] - Comparison function
 * @returns {boolean} True if sorted
 */
export function isSorted(arr, compareFunc = defaultCompare) {
    for (let i = 1; i < arr.length; i++) {
        if (compareFunc(arr[i - 1], arr[i]) > 0) {
            return false;
        }
    }
    return true;
}

/**
 * Shuffle an array using Fisher-Yates algorithm
 * @param {Array} arr - Array to shuffle
 * @returns {Array} Shuffled array
 */
export function shuffle(arr) {
    const result = [...arr];
    const n = result.length;

    for (let i = n - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        swap(result, i, j);
    }

    return result;
}

/**
 * Benchmark a sorting algorithm
 * @param {Function} sortFunc - Sorting function to benchmark
 * @param {Array} arr - Array to sort
 * @returns {Object} Benchmark results
 */
export function benchmarkSort(sortFunc, arr) {
    const startTime = performance.now();
    const sorted = sortFunc([...arr]);
    const endTime = performance.now();

    return {
        algorithm: sortFunc.name,
        inputSize: arr.length,
        timeMs: endTime - startTime,
        isSorted: isSorted(sorted)
    };
}

/**
 * Compare multiple sorting algorithms
 * @param {Array} algorithms - Array of sorting functions
 * @param {Array} arr - Test array
 * @returns {Array} Comparison results
 */
export function compareSorts(algorithms, arr) {
    return algorithms.map(algo => benchmarkSort(algo, arr))
        .sort((a, b) => a.timeMs - b.timeMs);
}

// Export all sorting algorithms
export default {
    bubbleSort,
    insertionSort,
    selectionSort,
    mergeSort,
    quickSort,
    heapSort,
    radixSort,
    countingSort,
    bucketSort,
    timSort,
    shellSort,
    combSort,
    gnomeSort,
    cocktailSort,
    isSorted,
    shuffle,
    benchmarkSort,
    compareSorts
};