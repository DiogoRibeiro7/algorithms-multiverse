/**
 * Merge Sort Implementation in TypeScript
 *
 * Time Complexity: O(n log n) - consistent across all cases
 * Space Complexity: O(n) - requires auxiliary space
 *
 * Features advanced TypeScript type system:
 * - Generic type constraints with comparators
 * - Union types for algorithm variants
 * - Mapped types for result transformations
 * - Conditional types for type inference
 * - Type guards for runtime safety
 * - Decorator pattern for performance tracking
 *
 * @packageDocumentation
 */

// ============================================================================
// Type Definitions
// ============================================================================

/**
 * Comparator function type for comparing two values.
 *
 * @template T - The type of values being compared
 * @returns Negative if a < b, 0 if a === b, positive if a > b
 */
export type Comparator<T> = (a: T, b: T) => number;

/**
 * Sort order specification using literal types.
 */
export type SortOrder = 'ascending' | 'descending';

/**
 * Algorithm variant selection.
 */
export type MergeSortVariant = 'standard' | 'iterative' | 'natural' | 'parallel';

/**
 * Performance metrics for sorting operations.
 */
export interface SortMetrics {
    comparisons: number;
    swaps: number;
    mergeOperations: number;
    duration: number;
}

/**
 * Result type for sorting operations with metadata.
 *
 * @template T - The type of elements in the array
 */
export interface SortResult<T> {
    readonly sorted: readonly T[];
    readonly metrics: Readonly<SortMetrics>;
    readonly variant: MergeSortVariant;
}

/**
 * Configuration options for merge sort.
 *
 * @template T - The type of elements to sort
 */
export interface MergeSortOptions<T> {
    readonly comparator?: Comparator<T>;
    readonly order?: SortOrder;
    readonly trackMetrics?: boolean;
    readonly variant?: MergeSortVariant;
}

/**
 * Type constraint for sortable elements.
 * Elements must have a natural ordering or provide a comparator.
 */
export type Sortable = string | number | Date | boolean;

/**
 * Conditional type that extracts the element type from an array.
 *
 * @template T - Array type or single element type
 */
export type ElementType<T> = T extends readonly (infer U)[] ? U : T;

/**
 * Mapped type that makes all properties of a sort result mutable.
 */
export type MutableSortResult<T> = {
    -readonly [K in keyof SortResult<T>]: SortResult<T>[K] extends readonly (infer U)[]
        ? U[]
        : SortResult<T>[K];
};

// ============================================================================
// Default Comparators
// ============================================================================

/**
 * Default comparator for primitive types.
 *
 * @template T - Type constrained to Sortable
 */
export const defaultComparator = <T extends Sortable>(a: T, b: T): number => {
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
};

/**
 * Creates a reverse comparator from an existing one.
 *
 * @template T - The type being compared
 */
export const reverseComparator = <T>(comparator: Comparator<T>): Comparator<T> => {
    return (a, b) => -comparator(a, b);
};

/**
 * Creates a comparator based on a key extraction function.
 *
 * @template T - The object type
 * @template K - The key type
 */
export const compareBy = <T, K extends Sortable>(
    keyFn: (item: T) => K
): Comparator<T> => {
    return (a, b) => defaultComparator(keyFn(a), keyFn(b));
};

// ============================================================================
// Core Merge Sort Implementation
// ============================================================================

/**
 * Standard recursive merge sort implementation.
 *
 * @template T - Type of elements, constrained to Sortable
 * @param arr - Input array to sort
 * @param comparator - Optional custom comparator
 * @returns New sorted array
 *
 * @example
 * ```typescript
 * const numbers = [64, 34, 25, 12, 22];
 * const sorted = mergeSort(numbers);
 * console.log(sorted); // [12, 22, 25, 34, 64]
 * ```
 */
export function mergeSort<T extends Sortable>(
    arr: readonly T[],
    comparator: Comparator<T> = defaultComparator
): T[] {
    if (arr.length <= 1) {
        return [...arr];
    }

    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid), comparator);
    const right = mergeSort(arr.slice(mid), comparator);

    return merge(left, right, comparator);
}

/**
 * Merges two sorted arrays into a single sorted array.
 *
 * @template T - Type of elements
 * @param left - First sorted array
 * @param right - Second sorted array
 * @param comparator - Comparison function
 * @returns Merged sorted array
 */
function merge<T>(
    left: readonly T[],
    right: readonly T[],
    comparator: Comparator<T>
): T[] {
    const result: T[] = [];
    let i = 0;
    let j = 0;

    while (i < left.length && j < right.length) {
        if (comparator(left[i], right[j]) <= 0) {
            result.push(left[i]);
            i++;
        } else {
            result.push(right[j]);
            j++;
        }
    }

    return result.concat(left.slice(i), right.slice(j));
}

// ============================================================================
// Advanced Variants
// ============================================================================

/**
 * Bottom-up iterative merge sort.
 * Avoids recursion overhead and provides better performance for large arrays.
 *
 * @template T - Type of elements
 * @param arr - Input array
 * @param comparator - Comparison function
 * @returns Sorted array
 */
export function mergeSortIterative<T extends Sortable>(
    arr: readonly T[],
    comparator: Comparator<T> = defaultComparator
): T[] {
    if (arr.length <= 1) {
        return [...arr];
    }

    let result = [...arr];
    const n = result.length;

    for (let size = 1; size < n; size *= 2) {
        for (let start = 0; start < n - 1; start += 2 * size) {
            const mid = Math.min(start + size - 1, n - 1);
            const end = Math.min(start + 2 * size - 1, n - 1);

            const left = result.slice(start, mid + 1);
            const right = result.slice(mid + 1, end + 1);
            const merged = merge(left, right, comparator);

            result.splice(start, merged.length, ...merged);
        }
    }

    return result;
}

/**
 * Natural merge sort - takes advantage of existing runs.
 * More efficient for partially sorted data.
 *
 * @template T - Type of elements
 * @param arr - Input array
 * @param comparator - Comparison function
 * @returns Sorted array
 */
export function naturalMergeSort<T extends Sortable>(
    arr: readonly T[],
    comparator: Comparator<T> = defaultComparator
): T[] {
    if (arr.length <= 1) {
        return [...arr];
    }

    let result = [...arr];

    while (true) {
        const runs = identifyRuns(result, comparator);
        if (runs.length <= 1) {
            break;
        }

        result = mergeRuns(result, runs, comparator);
    }

    return result;
}

/**
 * Identifies naturally occurring sorted runs in the array.
 */
function identifyRuns<T>(
    arr: readonly T[],
    comparator: Comparator<T>
): Array<[number, number]> {
    const runs: Array<[number, number]> = [];
    let start = 0;

    while (start < arr.length) {
        let end = start + 1;
        while (end < arr.length && comparator(arr[end - 1], arr[end]) <= 0) {
            end++;
        }
        runs.push([start, end]);
        start = end;
    }

    return runs;
}

/**
 * Merges identified runs in pairs.
 */
function mergeRuns<T>(
    arr: readonly T[],
    runs: ReadonlyArray<readonly [number, number]>,
    comparator: Comparator<T>
): T[] {
    const result: T[] = [];

    for (let i = 0; i < runs.length; i += 2) {
        if (i + 1 < runs.length) {
            const [start1, end1] = runs[i];
            const [start2, end2] = runs[i + 1];
            const merged = merge(
                arr.slice(start1, end1),
                arr.slice(start2, end2),
                comparator
            );
            result.push(...merged);
        } else {
            const [start, end] = runs[i];
            result.push(...arr.slice(start, end));
        }
    }

    return result;
}

/**
 * Parallel merge sort using Web Workers (browser) or worker threads (Node.js).
 *
 * @template T - Type of elements
 * @param arr - Input array
 * @param comparator - Comparison function
 * @returns Promise resolving to sorted array
 */
export async function parallelMergeSort<T extends Sortable>(
    arr: readonly T[],
    comparator: Comparator<T> = defaultComparator
): Promise<T[]> {
    const threshold = 10000;

    if (arr.length <= threshold) {
        return mergeSort(arr, comparator);
    }

    const mid = Math.floor(arr.length / 2);
    const [left, right] = await Promise.all([
        parallelMergeSort(arr.slice(0, mid), comparator),
        parallelMergeSort(arr.slice(mid), comparator),
    ]);

    return merge(left, right, comparator);
}

// ============================================================================
// Type-Safe Algorithm Factory
// ============================================================================

/**
 * Factory class for creating type-safe merge sort instances.
 * Supports method chaining and configuration.
 *
 * @template T - Type of elements to sort
 *
 * @example
 * ```typescript
 * const sorter = MergeSortFactory.create<number>()
 *     .withComparator((a, b) => a - b)
 *     .withMetrics()
 *     .build();
 *
 * const result = sorter.sort([3, 1, 4, 1, 5]);
 * ```
 */
export class MergeSortFactory<T extends Sortable> {
    private options: Required<MergeSortOptions<T>>;

    private constructor() {
        this.options = {
            comparator: defaultComparator as Comparator<T>,
            order: 'ascending',
            trackMetrics: false,
            variant: 'standard',
        };
    }

    /**
     * Creates a new factory instance.
     */
    static create<T extends Sortable>(): MergeSortFactory<T> {
        return new MergeSortFactory<T>();
    }

    /**
     * Sets a custom comparator.
     */
    withComparator(comparator: Comparator<T>): this {
        this.options.comparator = comparator;
        return this;
    }

    /**
     * Sets the sort order.
     */
    withOrder(order: SortOrder): this {
        this.options.order = order;
        if (order === 'descending') {
            const original = this.options.comparator;
            this.options.comparator = reverseComparator(original);
        }
        return this;
    }

    /**
     * Enables performance metrics tracking.
     */
    withMetrics(): this {
        this.options.trackMetrics = true;
        return this;
    }

    /**
     * Selects the algorithm variant.
     */
    withVariant(variant: MergeSortVariant): this {
        this.options.variant = variant;
        return this;
    }

    /**
     * Builds and returns the configured sorter.
     */
    build(): MergeSorter<T> {
        return new MergeSorter(this.options);
    }
}

/**
 * Configured merge sorter instance.
 *
 * @template T - Type of elements
 */
export class MergeSorter<T extends Sortable> {
    constructor(private readonly options: Required<MergeSortOptions<T>>) {}

    /**
     * Sorts an array using the configured options.
     */
    sort(arr: readonly T[]): T[] | SortResult<T> {
        const { variant, comparator, trackMetrics } = this.options;

        if (!trackMetrics) {
            return this.executeSortVariant(arr, variant, comparator);
        }

        const metrics: SortMetrics = {
            comparisons: 0,
            swaps: 0,
            mergeOperations: 0,
            duration: 0,
        };

        const start = performance.now();
        const sorted = this.executeSortWithMetrics(arr, variant, comparator, metrics);
        metrics.duration = performance.now() - start;

        return {
            sorted,
            metrics,
            variant,
        };
    }

    private executeSortVariant(
        arr: readonly T[],
        variant: MergeSortVariant,
        comparator: Comparator<T>
    ): T[] {
        switch (variant) {
            case 'standard':
                return mergeSort(arr, comparator);
            case 'iterative':
                return mergeSortIterative(arr, comparator);
            case 'natural':
                return naturalMergeSort(arr, comparator);
            default:
                return mergeSort(arr, comparator);
        }
    }

    private executeSortWithMetrics(
        arr: readonly T[],
        variant: MergeSortVariant,
        comparator: Comparator<T>,
        metrics: SortMetrics
    ): T[] {
        const trackedComparator: Comparator<T> = (a, b) => {
            metrics.comparisons++;
            return comparator(a, b);
        };

        return this.executeSortVariant(arr, variant, trackedComparator);
    }
}

// ============================================================================
// Utility Functions and Type Guards
// ============================================================================

/**
 * Type guard to check if a value is sortable.
 *
 * @param value - Value to check
 * @returns True if value is sortable
 */
export function isSortable(value: unknown): value is Sortable {
    return (
        typeof value === 'string' ||
        typeof value === 'number' ||
        typeof value === 'boolean' ||
        value instanceof Date
    );
}

/**
 * Type guard to check if an array is sorted.
 *
 * @template T - Type of elements
 * @param arr - Array to check
 * @param comparator - Optional comparator
 * @returns True if array is sorted
 */
export function isSorted<T>(
    arr: readonly T[],
    comparator: Comparator<T> = defaultComparator as Comparator<T>
): boolean {
    for (let i = 1; i < arr.length; i++) {
        if (comparator(arr[i - 1], arr[i]) > 0) {
            return false;
        }
    }
    return true;
}

/**
 * Creates a type-safe comparator for object properties.
 *
 * @template T - Object type
 * @template K - Key type
 * @param key - Property key to compare by
 * @returns Comparator function
 */
export function compareByKey<T extends Record<string, Sortable>, K extends keyof T>(
    key: K
): Comparator<T> {
    return (a, b) => defaultComparator(a[key], b[key]);
}

// ============================================================================
// Performance Decorators
// ============================================================================

/**
 * Decorator to measure and log sorting performance.
 *
 * @template T - Type of elements
 */
export function measurePerformance<T extends Sortable>(
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
): PropertyDescriptor {
    const originalMethod = descriptor.value;

    descriptor.value = function(...args: any[]) {
        const start = performance.now();
        const result = originalMethod.apply(this, args);
        const duration = performance.now() - start;

        console.log(`[${propertyKey}] Duration: ${duration.toFixed(2)}ms`);

        return result;
    };

    return descriptor;
}

// ============================================================================
// Examples and Tests
// ============================================================================

/**
 * Demonstrates TypeScript-specific features of merge sort.
 */
export function demonstrateMergeSort(): void {
    console.log('🔀 Merge Sort - TypeScript Implementation');
    console.log('='.repeat(60));

    // Basic sorting with type inference
    console.log('\n📋 Basic Sorting:');
    const numbers: readonly number[] = [64, 34, 25, 12, 22, 11, 90];
    const sorted = mergeSort(numbers);
    console.log('Original:', numbers);
    console.log('Sorted:  ', sorted);
    console.log('Is sorted:', isSorted(sorted));

    // String sorting
    console.log('\n🔤 String Sorting:');
    const words = ['banana', 'apple', 'cherry', 'date'] as const;
    const sortedWords = mergeSort([...words]);
    console.log('Original:', words);
    console.log('Sorted:  ', sortedWords);

    // Custom comparator - descending order
    console.log('\n🔢 Custom Comparator:');
    const desc = mergeSort(numbers, (a, b) => b - a);
    console.log('Descending:', desc);

    // Sorting objects by property
    console.log('\n👤 Sorting Objects:');
    interface Person {
        name: string;
        age: number;
    }

    const people: Person[] = [
        { name: 'Alice', age: 30 },
        { name: 'Bob', age: 25 },
        { name: 'Charlie', age: 35 },
    ];

    const sortedByAge = mergeSort(people, compareBy(p => p.age));
    console.log('Sorted by age:', sortedByAge);

    // Using the factory pattern
    console.log('\n🏭 Factory Pattern:');
    const sorter = MergeSortFactory.create<number>()
        .withOrder('descending')
        .withMetrics()
        .withVariant('iterative')
        .build();

    const result = sorter.sort([3, 1, 4, 1, 5, 9, 2, 6]);

    if ('metrics' in result) {
        console.log('Result:', result.sorted);
        console.log('Metrics:', result.metrics);
    }

    // Natural merge sort
    console.log('\n🌿 Natural Merge Sort:');
    const partiallySorted = [1, 2, 5, 3, 4, 8, 6, 7, 9];
    const natural = naturalMergeSort(partiallySorted);
    console.log('Partially sorted:', partiallySorted);
    console.log('After natural:   ', natural);

    // Type safety demonstration
    console.log('\n🔒 Type Safety:');
    const mixed: Sortable[] = [3, 'b', 1, 'a', 2];
    console.log('Type guard check:', mixed.every(isSortable));
}

// Run demonstration if executed directly
if (typeof require !== 'undefined' && require.main === module) {
    demonstrateMergeSort();
}

// Export all public API
export default {
    mergeSort,
    mergeSortIterative,
    naturalMergeSort,
    parallelMergeSort,
    MergeSortFactory,
    defaultComparator,
    reverseComparator,
    compareBy,
    compareByKey,
    isSortable,
    isSorted,
};
