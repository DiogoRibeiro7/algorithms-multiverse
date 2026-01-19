/**
 * Utility Functions Module
 * Common helper functions used across algorithm implementations
 */

// Comparison functions
export const defaultCompare = (a, b) => {
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
};

export const reverseCompare = (compareFunc = defaultCompare) => {
    return (a, b) => -compareFunc(a, b);
};

export const compareByProperty = (property, compareFunc = defaultCompare) => {
    return (a, b) => compareFunc(a[property], b[property]);
};

// Array utilities
export function swap(arr, i, j) {
    [arr[i], arr[j]] = [arr[j], arr[i]];
}

export function shuffle(arr) {
    const result = [...arr];
    for (let i = result.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        swap(result, i, j);
    }
    return result;
}

export function range(start, end, step = 1) {
    const result = [];
    if (step > 0) {
        for (let i = start; i < end; i += step) {
            result.push(i);
        }
    } else if (step < 0) {
        for (let i = start; i > end; i += step) {
            result.push(i);
        }
    }
    return result;
}

export function chunk(arr, size) {
    const chunks = [];
    for (let i = 0; i < arr.length; i += size) {
        chunks.push(arr.slice(i, i + size));
    }
    return chunks;
}

export function flatten(arr, depth = 1) {
    if (depth <= 0) return arr.slice();
    return arr.reduce((acc, val) => {
        if (Array.isArray(val)) {
            return acc.concat(flatten(val, depth - 1));
        }
        return acc.concat(val);
    }, []);
}

export function deepFlatten(arr) {
    return arr.reduce((acc, val) => {
        if (Array.isArray(val)) {
            return acc.concat(deepFlatten(val));
        }
        return acc.concat(val);
    }, []);
}

export function unique(arr, keyFunc = null) {
    if (keyFunc === null) {
        return [...new Set(arr)];
    }
    const seen = new Set();
    const result = [];
    for (const item of arr) {
        const key = keyFunc(item);
        if (!seen.has(key)) {
            seen.add(key);
            result.push(item);
        }
    }
    return result;
}

export function intersection(arr1, arr2) {
    const set2 = new Set(arr2);
    return arr1.filter(x => set2.has(x));
}

export function difference(arr1, arr2) {
    const set2 = new Set(arr2);
    return arr1.filter(x => !set2.has(x));
}

export function union(arr1, arr2) {
    return [...new Set([...arr1, ...arr2])];
}

export function zip(...arrays) {
    const minLength = Math.min(...arrays.map(arr => arr.length));
    const result = [];
    for (let i = 0; i < minLength; i++) {
        result.push(arrays.map(arr => arr[i]));
    }
    return result;
}

export function unzip(arr) {
    if (arr.length === 0) return [];
    const result = Array(arr[0].length).fill().map(() => []);
    for (let i = 0; i < arr.length; i++) {
        for (let j = 0; j < arr[i].length; j++) {
            result[j].push(arr[i][j]);
        }
    }
    return result;
}

// Mathematical utilities
export function gcd(a, b) {
    a = Math.abs(a);
    b = Math.abs(b);
    while (b !== 0) {
        const temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

export function lcm(a, b) {
    return Math.abs(a * b) / gcd(a, b);
}

export function factorial(n) {
    if (n < 0) throw new Error("Factorial is not defined for negative numbers");
    if (n <= 1) return 1;
    let result = 1;
    for (let i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

export function permutations(arr, r = null) {
    if (r === null) r = arr.length;
    if (r > arr.length) return [];
    if (r === 0) return [[]];

    const result = [];

    function backtrack(current, remaining) {
        if (current.length === r) {
            result.push([...current]);
            return;
        }
        for (let i = 0; i < remaining.length; i++) {
            current.push(remaining[i]);
            const newRemaining = [...remaining.slice(0, i), ...remaining.slice(i + 1)];
            backtrack(current, newRemaining);
            current.pop();
        }
    }

    backtrack([], arr);
    return result;
}

export function combinations(arr, r) {
    if (r > arr.length) return [];
    if (r === 0) return [[]];

    const result = [];

    function backtrack(start, current) {
        if (current.length === r) {
            result.push([...current]);
            return;
        }
        for (let i = start; i < arr.length; i++) {
            current.push(arr[i]);
            backtrack(i + 1, current);
            current.pop();
        }
    }

    backtrack(0, []);
    return result;
}

export function cartesianProduct(...arrays) {
    if (arrays.length === 0) return [];
    if (arrays.length === 1) return arrays[0].map(x => [x]);

    const result = [];

    function backtrack(index, current) {
        if (index === arrays.length) {
            result.push([...current]);
            return;
        }
        for (const item of arrays[index]) {
            current.push(item);
            backtrack(index + 1, current);
            current.pop();
        }
    }

    backtrack(0, []);
    return result;
}

export function isPrime(n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 === 0 || n % 3 === 0) return false;
    for (let i = 5; i * i <= n; i += 6) {
        if (n % i === 0 || n % (i + 2) === 0) return false;
    }
    return true;
}

export function primeFactors(n) {
    const factors = [];
    let divisor = 2;

    while (n > 1) {
        while (n % divisor === 0) {
            factors.push(divisor);
            n /= divisor;
        }
        divisor++;
        if (divisor * divisor > n && n > 1) {
            factors.push(n);
            break;
        }
    }

    return factors;
}

export function fibonacci(n) {
    if (n <= 0) return 0;
    if (n === 1) return 1;
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
        [a, b] = [b, a + b];
    }
    return b;
}

export function modularExponentiation(base, exp, mod) {
    let result = 1;
    base = base % mod;
    while (exp > 0) {
        if (exp % 2 === 1) {
            result = (result * base) % mod;
        }
        exp = Math.floor(exp / 2);
        base = (base * base) % mod;
    }
    return result;
}

// Random utilities
export function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

export function randomFloat(min, max) {
    return Math.random() * (max - min) + min;
}

export function randomChoice(arr) {
    if (arr.length === 0) return undefined;
    return arr[randomInt(0, arr.length - 1)];
}

export function randomSample(arr, k) {
    if (k > arr.length) {
        throw new Error("Sample size cannot exceed array length");
    }
    const result = [];
    const indices = new Set();
    while (indices.size < k) {
        const index = randomInt(0, arr.length - 1);
        if (!indices.has(index)) {
            indices.add(index);
            result.push(arr[index]);
        }
    }
    return result;
}

export function weightedRandomChoice(items, weights) {
    if (items.length !== weights.length) {
        throw new Error("Items and weights must have the same length");
    }
    const totalWeight = weights.reduce((sum, w) => sum + w, 0);
    let random = Math.random() * totalWeight;

    for (let i = 0; i < items.length; i++) {
        random -= weights[i];
        if (random <= 0) {
            return items[i];
        }
    }
    return items[items.length - 1];
}

// String utilities
export function isPalindrome(str) {
    const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
    let left = 0;
    let right = cleaned.length - 1;
    while (left < right) {
        if (cleaned[left] !== cleaned[right]) return false;
        left++;
        right--;
    }
    return true;
}

export function isAnagram(str1, str2) {
    const clean1 = str1.toLowerCase().replace(/[^a-z0-9]/g, '');
    const clean2 = str2.toLowerCase().replace(/[^a-z0-9]/g, '');

    if (clean1.length !== clean2.length) return false;

    const charCount = new Map();
    for (const char of clean1) {
        charCount.set(char, (charCount.get(char) || 0) + 1);
    }
    for (const char of clean2) {
        const count = charCount.get(char) || 0;
        if (count === 0) return false;
        charCount.set(char, count - 1);
    }
    return true;
}

export function longestCommonPrefix(strs) {
    if (strs.length === 0) return "";
    if (strs.length === 1) return strs[0];

    let prefix = strs[0];
    for (let i = 1; i < strs.length; i++) {
        while (!strs[i].startsWith(prefix)) {
            prefix = prefix.slice(0, -1);
            if (prefix === "") return "";
        }
    }
    return prefix;
}

// Validation utilities
export function isNumber(value) {
    return typeof value === 'number' && !isNaN(value) && isFinite(value);
}

export function isInteger(value) {
    return isNumber(value) && Number.isInteger(value);
}

export function isPositive(value) {
    return isNumber(value) && value > 0;
}

export function isNegative(value) {
    return isNumber(value) && value < 0;
}

export function inRange(value, min, max) {
    return isNumber(value) && value >= min && value <= max;
}

export function isArrayOf(arr, validator) {
    if (!Array.isArray(arr)) return false;
    return arr.every(validator);
}

// Functional utilities
export function compose(...fns) {
    return (x) => fns.reduceRight((acc, fn) => fn(acc), x);
}

export function pipe(...fns) {
    return (x) => fns.reduce((acc, fn) => fn(acc), x);
}

export function curry(fn) {
    return function curried(...args) {
        if (args.length >= fn.length) {
            return fn.apply(this, args);
        }
        return function(...nextArgs) {
            return curried.apply(this, args.concat(nextArgs));
        };
    };
}

export function memoize(fn, keyGenerator = (...args) => JSON.stringify(args)) {
    const cache = new Map();
    return function(...args) {
        const key = keyGenerator(...args);
        if (cache.has(key)) {
            return cache.get(key);
        }
        const result = fn.apply(this, args);
        cache.set(key, result);
        return result;
    };
}

export function debounce(fn, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
}

export function throttle(fn, delay) {
    let lastCall = 0;
    return function(...args) {
        const now = Date.now();
        if (now - lastCall >= delay) {
            lastCall = now;
            return fn.apply(this, args);
        }
    };
}

// Performance utilities
export function measureTime(fn, ...args) {
    const start = performance.now();
    const result = fn(...args);
    const end = performance.now();
    return {
        result,
        time: end - start
    };
}

export function benchmark(fn, iterations = 1000, ...args) {
    const times = [];
    for (let i = 0; i < iterations; i++) {
        const start = performance.now();
        fn(...args);
        const end = performance.now();
        times.push(end - start);
    }

    times.sort((a, b) => a - b);
    const avg = times.reduce((sum, t) => sum + t, 0) / times.length;
    const median = times[Math.floor(times.length / 2)];
    const min = times[0];
    const max = times[times.length - 1];

    return { avg, median, min, max, times };
}

// Matrix utilities (simple versions for quick use)
export function create2DArray(rows, cols, initialValue = 0) {
    return Array(rows).fill().map(() => Array(cols).fill(initialValue));
}

export function copy2DArray(arr) {
    return arr.map(row => [...row]);
}

export function transpose2DArray(arr) {
    if (arr.length === 0) return [];
    const rows = arr.length;
    const cols = arr[0].length;
    const result = create2DArray(cols, rows);
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            result[j][i] = arr[i][j];
        }
    }
    return result;
}

// Graph utilities (adjacency list helpers)
export function createAdjacencyList(n) {
    return Array(n).fill().map(() => []);
}

export function addEdge(adjList, from, to, directed = false) {
    adjList[from].push(to);
    if (!directed) {
        adjList[to].push(from);
    }
}

export function removeEdge(adjList, from, to, directed = false) {
    adjList[from] = adjList[from].filter(v => v !== to);
    if (!directed) {
        adjList[to] = adjList[to].filter(v => v !== from);
    }
}

// Bit manipulation utilities
export function getBit(num, position) {
    return (num >> position) & 1;
}

export function setBit(num, position) {
    return num | (1 << position);
}

export function clearBit(num, position) {
    return num & ~(1 << position);
}

export function toggleBit(num, position) {
    return num ^ (1 << position);
}

export function countBits(num) {
    let count = 0;
    while (num) {
        count += num & 1;
        num >>= 1;
    }
    return count;
}

export function isPowerOfTwo(num) {
    return num > 0 && (num & (num - 1)) === 0;
}

// Tree utilities (for binary tree arrays)
export function getParentIndex(i) {
    return Math.floor((i - 1) / 2);
}

export function getLeftChildIndex(i) {
    return 2 * i + 1;
}

export function getRightChildIndex(i) {
    return 2 * i + 2;
}

export function isLeaf(arr, i) {
    const left = getLeftChildIndex(i);
    return left >= arr.length;
}

// Error handling utilities
export function tryExecute(fn, defaultValue = null, ...args) {
    try {
        return fn(...args);
    } catch (error) {
        return defaultValue;
    }
}

export function retry(fn, maxAttempts = 3, delay = 0) {
    return async function(...args) {
        let lastError;
        for (let i = 0; i < maxAttempts; i++) {
            try {
                return await fn(...args);
            } catch (error) {
                lastError = error;
                if (i < maxAttempts - 1 && delay > 0) {
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            }
        }
        throw lastError;
    };
}

// Data structure helpers
export class PriorityQueue {
    constructor(compareFunc = (a, b) => a - b) {
        this.heap = [];
        this.compare = compareFunc;
    }

    push(item) {
        this.heap.push(item);
        this.bubbleUp(this.heap.length - 1);
    }

    pop() {
        if (this.isEmpty()) return undefined;
        const top = this.heap[0];
        const last = this.heap.pop();
        if (this.heap.length > 0) {
            this.heap[0] = last;
            this.bubbleDown(0);
        }
        return top;
    }

    peek() {
        return this.heap[0];
    }

    isEmpty() {
        return this.heap.length === 0;
    }

    size() {
        return this.heap.length;
    }

    bubbleUp(index) {
        while (index > 0) {
            const parentIndex = getParentIndex(index);
            if (this.compare(this.heap[index], this.heap[parentIndex]) < 0) {
                swap(this.heap, index, parentIndex);
                index = parentIndex;
            } else {
                break;
            }
        }
    }

    bubbleDown(index) {
        while (true) {
            let minIndex = index;
            const leftChild = getLeftChildIndex(index);
            const rightChild = getRightChildIndex(index);

            if (leftChild < this.heap.length &&
                this.compare(this.heap[leftChild], this.heap[minIndex]) < 0) {
                minIndex = leftChild;
            }

            if (rightChild < this.heap.length &&
                this.compare(this.heap[rightChild], this.heap[minIndex]) < 0) {
                minIndex = rightChild;
            }

            if (minIndex !== index) {
                swap(this.heap, index, minIndex);
                index = minIndex;
            } else {
                break;
            }
        }
    }
}

// Export all functions as a default object for convenience
export default {
    // Comparison
    defaultCompare,
    reverseCompare,
    compareByProperty,
    // Arrays
    swap,
    shuffle,
    range,
    chunk,
    flatten,
    deepFlatten,
    unique,
    intersection,
    difference,
    union,
    zip,
    unzip,
    // Math
    gcd,
    lcm,
    factorial,
    permutations,
    combinations,
    cartesianProduct,
    isPrime,
    primeFactors,
    fibonacci,
    modularExponentiation,
    // Random
    randomInt,
    randomFloat,
    randomChoice,
    randomSample,
    weightedRandomChoice,
    // Strings
    isPalindrome,
    isAnagram,
    longestCommonPrefix,
    // Validation
    isNumber,
    isInteger,
    isPositive,
    isNegative,
    inRange,
    isArrayOf,
    // Functional
    compose,
    pipe,
    curry,
    memoize,
    debounce,
    throttle,
    // Performance
    measureTime,
    benchmark,
    // Matrix
    create2DArray,
    copy2DArray,
    transpose2DArray,
    // Graph
    createAdjacencyList,
    addEdge,
    removeEdge,
    // Bits
    getBit,
    setBit,
    clearBit,
    toggleBit,
    countBits,
    isPowerOfTwo,
    // Tree
    getParentIndex,
    getLeftChildIndex,
    getRightChildIndex,
    isLeaf,
    // Error handling
    tryExecute,
    retry,
    // Data structures
    PriorityQueue
};