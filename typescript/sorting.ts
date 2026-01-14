/**
 * Sorting Algorithms in TypeScript
 * =================================
 *
 * Comprehensive implementation of sorting algorithms with TypeScript features:
 * - Strong typing and generics
 * - Custom comparator support
 * - Performance optimizations
 * - In-place and stable sorting variants
 *
 * @module sorting
 * @author Algorithms Multiverse
 */

/**
 * Comparator function type for comparing two elements
 */
type CompareFn<T> = (a: T, b: T) => number;

/**
 * Default comparator for primitive types
 */
const defaultCompare = <T>(a: T, b: T): number => {
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
};

/**
 * Sorting algorithm statistics
 */
interface SortingStats {
    comparisons: number;
    swaps: number;
    timeMs: number;
}

/**
 * Abstract base class for sorting algorithms
 */
abstract class SortingAlgorithm<T> {
    protected compareFn: CompareFn<T>;
    protected stats: SortingStats;

    constructor(compareFn: CompareFn<T> = defaultCompare) {
        this.compareFn = compareFn;
        this.stats = { comparisons: 0, swaps: 0, timeMs: 0 };
    }

    /**
     * Sort the array and return statistics
     */
    public sortWithStats(arr: T[]): SortingStats {
        this.resetStats();
        const start = performance.now();
        this.sort(arr);
        this.stats.timeMs = performance.now() - start;
        return { ...this.stats };
    }

    /**
     * Abstract sort method to be implemented by subclasses
     */
    public abstract sort(arr: T[]): void;

    /**
     * Check if array is sorted
     */
    public isSorted(arr: T[]): boolean {
        for (let i = 1; i < arr.length; i++) {
            if (this.compareFn(arr[i - 1], arr[i]) > 0) {
                return false;
            }
        }
        return true;
    }

    protected compare(a: T, b: T): number {
        this.stats.comparisons++;
        return this.compareFn(a, b);
    }

    protected swap(arr: T[], i: number, j: number): void {
        if (i !== j) {
            this.stats.swaps++;
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
    }

    private resetStats(): void {
        this.stats = { comparisons: 0, swaps: 0, timeMs: 0 };
    }
}

/**
 * Quick Sort Implementation
 * Time: O(n log n) average, O(n²) worst
 * Space: O(log n)
 */
export class QuickSort<T> extends SortingAlgorithm<T> {
    private randomPivot: boolean;

    constructor(compareFn: CompareFn<T> = defaultCompare, randomPivot = true) {
        super(compareFn);
        this.randomPivot = randomPivot;
    }

    public sort(arr: T[]): void {
        this.quickSort(arr, 0, arr.length - 1);
    }

    private quickSort(arr: T[], low: number, high: number): void {
        if (low < high) {
            const pivot = this.partition(arr, low, high);
            this.quickSort(arr, low, pivot - 1);
            this.quickSort(arr, pivot + 1, high);
        }
    }

    private partition(arr: T[], low: number, high: number): number {
        // Random pivot selection for better average case
        if (this.randomPivot) {
            const randomIdx = low + Math.floor(Math.random() * (high - low + 1));
            this.swap(arr, randomIdx, high);
        }

        const pivot = arr[high];
        let i = low - 1;

        for (let j = low; j < high; j++) {
            if (this.compare(arr[j], pivot) <= 0) {
                i++;
                this.swap(arr, i, j);
            }
        }

        this.swap(arr, i + 1, high);
        return i + 1;
    }
}

/**
 * Merge Sort Implementation (Stable)
 * Time: O(n log n) all cases
 * Space: O(n)
 */
export class MergeSort<T> extends SortingAlgorithm<T> {
    public sort(arr: T[]): void {
        if (arr.length <= 1) return;
        this.mergeSort(arr, 0, arr.length - 1);
    }

    private mergeSort(arr: T[], left: number, right: number): void {
        if (left < right) {
            const mid = Math.floor((left + right) / 2);
            this.mergeSort(arr, left, mid);
            this.mergeSort(arr, mid + 1, right);
            this.merge(arr, left, mid, right);
        }
    }

    private merge(arr: T[], left: number, mid: number, right: number): void {
        const leftArr = arr.slice(left, mid + 1);
        const rightArr = arr.slice(mid + 1, right + 1);

        let i = 0, j = 0, k = left;

        while (i < leftArr.length && j < rightArr.length) {
            if (this.compare(leftArr[i], rightArr[j]) <= 0) {
                arr[k++] = leftArr[i++];
            } else {
                arr[k++] = rightArr[j++];
            }
        }

        while (i < leftArr.length) {
            arr[k++] = leftArr[i++];
        }

        while (j < rightArr.length) {
            arr[k++] = rightArr[j++];
        }
    }
}

/**
 * Heap Sort Implementation
 * Time: O(n log n) all cases
 * Space: O(1)
 */
export class HeapSort<T> extends SortingAlgorithm<T> {
    public sort(arr: T[]): void {
        const n = arr.length;

        // Build max heap
        for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
            this.heapify(arr, n, i);
        }

        // Extract elements from heap
        for (let i = n - 1; i > 0; i--) {
            this.swap(arr, 0, i);
            this.heapify(arr, i, 0);
        }
    }

    private heapify(arr: T[], n: number, i: number): void {
        let largest = i;
        const left = 2 * i + 1;
        const right = 2 * i + 2;

        if (left < n && this.compare(arr[left], arr[largest]) > 0) {
            largest = left;
        }

        if (right < n && this.compare(arr[right], arr[largest]) > 0) {
            largest = right;
        }

        if (largest !== i) {
            this.swap(arr, i, largest);
            this.heapify(arr, n, largest);
        }
    }
}

/**
 * Tim Sort Implementation (Stable, Hybrid)
 * Time: O(n log n) all cases
 * Space: O(n)
 */
export class TimSort<T> extends SortingAlgorithm<T> {
    private readonly MIN_MERGE = 32;

    public sort(arr: T[]): void {
        const n = arr.length;

        // Sort individual runs using insertion sort
        for (let i = 0; i < n; i += this.MIN_MERGE) {
            this.insertionSort(arr, i, Math.min(i + this.MIN_MERGE - 1, n - 1));
        }

        // Merge the sorted runs
        for (let size = this.MIN_MERGE; size < n; size *= 2) {
            for (let start = 0; start < n; start += size * 2) {
                const mid = start + size - 1;
                const end = Math.min(start + size * 2 - 1, n - 1);

                if (mid < end) {
                    this.merge(arr, start, mid, end);
                }
            }
        }
    }

    private insertionSort(arr: T[], left: number, right: number): void {
        for (let i = left + 1; i <= right; i++) {
            const key = arr[i];
            let j = i - 1;

            while (j >= left && this.compare(arr[j], key) > 0) {
                arr[j + 1] = arr[j];
                j--;
            }

            arr[j + 1] = key;
        }
    }

    private merge(arr: T[], left: number, mid: number, right: number): void {
        const leftArr = arr.slice(left, mid + 1);
        const rightArr = arr.slice(mid + 1, right + 1);

        let i = 0, j = 0, k = left;

        while (i < leftArr.length && j < rightArr.length) {
            if (this.compare(leftArr[i], rightArr[j]) <= 0) {
                arr[k++] = leftArr[i++];
            } else {
                arr[k++] = rightArr[j++];
            }
        }

        while (i < leftArr.length) {
            arr[k++] = leftArr[i++];
        }

        while (j < rightArr.length) {
            arr[k++] = rightArr[j++];
        }
    }
}

/**
 * Radix Sort Implementation (for integers)
 * Time: O(nk) where k is the number of digits
 * Space: O(n)
 */
export class RadixSort {
    public sort(arr: number[]): void {
        if (arr.length <= 1) return;

        const max = Math.max(...arr);
        const maxDigits = Math.floor(Math.log10(max)) + 1;

        for (let digit = 0; digit < maxDigits; digit++) {
            this.countingSortByDigit(arr, digit);
        }
    }

    private countingSortByDigit(arr: number[], digit: number): void {
        const n = arr.length;
        const output = new Array(n);
        const count = new Array(10).fill(0);
        const exp = Math.pow(10, digit);

        // Count occurrences
        for (let i = 0; i < n; i++) {
            const index = Math.floor(arr[i] / exp) % 10;
            count[index]++;
        }

        // Cumulative count
        for (let i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }

        // Build output array
        for (let i = n - 1; i >= 0; i--) {
            const index = Math.floor(arr[i] / exp) % 10;
            output[count[index] - 1] = arr[i];
            count[index]--;
        }

        // Copy output to arr
        for (let i = 0; i < n; i++) {
            arr[i] = output[i];
        }
    }
}

/**
 * Intro Sort Implementation (Hybrid: Quick + Heap + Insertion)
 * Time: O(n log n) guaranteed
 * Space: O(log n)
 */
export class IntroSort<T> extends SortingAlgorithm<T> {
    private readonly INSERTION_THRESHOLD = 16;
    private heapSort: HeapSort<T>;

    constructor(compareFn: CompareFn<T> = defaultCompare) {
        super(compareFn);
        this.heapSort = new HeapSort(compareFn);
    }

    public sort(arr: T[]): void {
        if (arr.length <= 1) return;
        const maxDepth = Math.floor(Math.log2(arr.length)) * 2;
        this.introSort(arr, 0, arr.length - 1, maxDepth);
    }

    private introSort(arr: T[], low: number, high: number, depthLimit: number): void {
        if (high <= low) return;

        if (high - low + 1 <= this.INSERTION_THRESHOLD) {
            this.insertionSort(arr, low, high);
        } else if (depthLimit === 0) {
            // Switch to heap sort to avoid worst case
            const subArr = arr.slice(low, high + 1);
            this.heapSort.sort(subArr);
            for (let i = 0; i < subArr.length; i++) {
                arr[low + i] = subArr[i];
            }
        } else {
            const pivot = this.partition(arr, low, high);
            this.introSort(arr, low, pivot - 1, depthLimit - 1);
            this.introSort(arr, pivot + 1, high, depthLimit - 1);
        }
    }

    private partition(arr: T[], low: number, high: number): number {
        // Median of three pivot selection
        const mid = Math.floor((low + high) / 2);
        if (this.compare(arr[mid], arr[low]) < 0) this.swap(arr, mid, low);
        if (this.compare(arr[high], arr[low]) < 0) this.swap(arr, high, low);
        if (this.compare(arr[high], arr[mid]) < 0) this.swap(arr, high, mid);

        this.swap(arr, mid, high);
        const pivot = arr[high];
        let i = low - 1;

        for (let j = low; j < high; j++) {
            if (this.compare(arr[j], pivot) <= 0) {
                i++;
                this.swap(arr, i, j);
            }
        }

        this.swap(arr, i + 1, high);
        return i + 1;
    }

    private insertionSort(arr: T[], left: number, right: number): void {
        for (let i = left + 1; i <= right; i++) {
            const key = arr[i];
            let j = i - 1;

            while (j >= left && this.compare(arr[j], key) > 0) {
                arr[j + 1] = arr[j];
                j--;
            }

            arr[j + 1] = key;
        }
    }
}

/**
 * Utility class for sorting operations
 */
export class SortingUtils {
    /**
     * Check if an array is sorted
     */
    static isSorted<T>(arr: T[], compareFn: CompareFn<T> = defaultCompare): boolean {
        for (let i = 1; i < arr.length; i++) {
            if (compareFn(arr[i - 1], arr[i]) > 0) {
                return false;
            }
        }
        return true;
    }

    /**
     * Shuffle array using Fisher-Yates algorithm
     */
    static shuffle<T>(arr: T[]): void {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
    }

    /**
     * Generate test arrays
     */
    static generateTestArray(size: number, type: 'random' | 'sorted' | 'reverse' | 'nearly-sorted'): number[] {
        const arr = Array.from({ length: size }, (_, i) => i);

        switch (type) {
            case 'random':
                this.shuffle(arr);
                break;
            case 'reverse':
                arr.reverse();
                break;
            case 'nearly-sorted':
                // Swap a few random pairs
                for (let i = 0; i < Math.floor(size * 0.1); i++) {
                    const a = Math.floor(Math.random() * size);
                    const b = Math.floor(Math.random() * size);
                    [arr[a], arr[b]] = [arr[b], arr[a]];
                }
                break;
            // 'sorted' is default
        }

        return arr;
    }

    /**
     * Benchmark sorting algorithms
     */
    static benchmark<T>(
        algorithms: SortingAlgorithm<T>[],
        testData: T[][],
        names: string[]
    ): Map<string, SortingStats[]> {
        const results = new Map<string, SortingStats[]>();

        for (let i = 0; i < algorithms.length; i++) {
            const stats: SortingStats[] = [];

            for (const data of testData) {
                const arrCopy = [...data];
                const stat = algorithms[i].sortWithStats(arrCopy);
                stats.push(stat);
            }

            results.set(names[i], stats);
        }

        return results;
    }
}

// Example usage and demonstration
if (require.main === module) {
    console.log("TypeScript Sorting Algorithms Demonstration");
    console.log("=" .repeat(50));

    // Test with different data types
    const numbers = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 43, 24, 35, 31, 44, 65];
    const strings = ["apple", "zebra", "banana", "cherry", "date", "elderberry"];

    // Custom object type
    interface Person {
        name: string;
        age: number;
    }

    const people: Person[] = [
        { name: "Alice", age: 30 },
        { name: "Bob", age: 25 },
        { name: "Charlie", age: 35 },
        { name: "David", age: 20 }
    ];

    // Test different sorting algorithms
    const algorithms = [
        new QuickSort<number>(),
        new MergeSort<number>(),
        new HeapSort<number>(),
        new TimSort<number>(),
        new IntroSort<number>()
    ];

    const algorithmNames = ["QuickSort", "MergeSort", "HeapSort", "TimSort", "IntroSort"];

    console.log("\n1. Sorting Numbers:");
    console.log("Original:", numbers);

    algorithms.forEach((algo, i) => {
        const copy = [...numbers];
        const stats = algo.sortWithStats(copy);
        console.log(`${algorithmNames[i]}: ${copy}`);
        console.log(`  Stats: ${stats.comparisons} comparisons, ${stats.swaps} swaps, ${stats.timeMs.toFixed(3)}ms`);
    });

    console.log("\n2. Sorting Strings:");
    const stringSort = new QuickSort<string>();
    const stringCopy = [...strings];
    stringSort.sort(stringCopy);
    console.log("Sorted:", stringCopy);

    console.log("\n3. Sorting Objects:");
    const personSort = new MergeSort<Person>((a, b) => a.age - b.age);
    const peopleCopy = [...people];
    personSort.sort(peopleCopy);
    console.log("Sorted by age:", peopleCopy);

    console.log("\n4. Radix Sort (Integers only):");
    const radixNumbers = [170, 45, 75, 90, 2, 802, 24, 66];
    const radixSort = new RadixSort();
    const radixCopy = [...radixNumbers];
    radixSort.sort(radixCopy);
    console.log("Original:", radixNumbers);
    console.log("Sorted:", radixCopy);

    console.log("\n5. Performance Comparison:");
    const sizes = [100, 1000, 10000];

    sizes.forEach(size => {
        console.log(`\nArray size: ${size}`);
        const testArrays = [
            SortingUtils.generateTestArray(size, 'random'),
            SortingUtils.generateTestArray(size, 'sorted'),
            SortingUtils.generateTestArray(size, 'reverse'),
            SortingUtils.generateTestArray(size, 'nearly-sorted')
        ];

        const results = SortingUtils.benchmark(algorithms, testArrays, algorithmNames);

        results.forEach((stats, name) => {
            const avgTime = stats.reduce((sum, s) => sum + s.timeMs, 0) / stats.length;
            console.log(`  ${name}: ${avgTime.toFixed(3)}ms average`);
        });
    });
}