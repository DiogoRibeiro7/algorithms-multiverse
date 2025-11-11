package com.algorithms.sorting;

/**
 * Insertion Sort Algorithm Implementation in Java
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
 * Java features:
 * - Generic methods for type safety
 * - Multiple implementation patterns
 * - Overloaded methods for primitives
 * - Custom comparators
 */

import java.util.*;
import java.util.function.BiFunction;

public class InsertionSort {

    /**
     * Standard insertion sort implementation.
     *
     * @param arr Array to be sorted
     * @param <T> Type of elements (must be Comparable)
     * @return New sorted array
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
    public static <T extends Comparable<T>> T[] insertionSort(T[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();
        insertionSortInPlace(result);
        return result;
    }

    /**
     * In-place insertion sort implementation.
     *
     * @param arr Array to be sorted in-place
     * @param <T> Type of elements (must be Comparable)
     *
     * Time Complexity: O(n²) average and worst case, O(n) best case
     * Space Complexity: O(1)
     */
    public static <T extends Comparable<T>> void insertionSortInPlace(T[] arr) {
        for (int i = 1; i < arr.length; i++) {
            T key = arr[i];
            int j = i - 1;

            // Move elements greater than key one position ahead
            while (j >= 0 && arr[j].compareTo(key) > 0) {
                arr[j + 1] = arr[j];
                j--;
            }

            arr[j + 1] = key;
        }
    }

    /**
     * Recursive insertion sort implementation.
     *
     * @param arr Array to be sorted
     * @param n Number of elements to sort
     * @param <T> Type of elements
     */
    public static <T extends Comparable<T>> void insertionSortRecursive(T[] arr, int n) {
        // Base case
        if (n <= 1) {
            return;
        }

        // Sort first n-1 elements
        insertionSortRecursive(arr, n - 1);

        // Insert last element at its correct position
        T key = arr[n - 1];
        int j = n - 2;

        while (j >= 0 && arr[j].compareTo(key) > 0) {
            arr[j + 1] = arr[j];
            j--;
        }

        arr[j + 1] = key;
    }

    /**
     * Recursive insertion sort with array cloning.
     *
     * @param arr Array to be sorted
     * @param <T> Type of elements
     * @return New sorted array
     */
    public static <T extends Comparable<T>> T[] insertionSortRecursive(T[] arr) {
        T[] result = arr.clone();
        insertionSortRecursive(result, result.length);
        return result;
    }

    /**
     * Binary insertion sort - uses binary search to find insertion position.
     *
     * @param arr Array to be sorted
     * @param <T> Type of elements
     * @return New sorted array
     *
     * Time Complexity: O(n²) for moves, O(n log n) for comparisons
     * Space Complexity: O(n)
     */
    public static <T extends Comparable<T>> T[] binaryInsertionSort(T[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();

        for (int i = 1; i < result.length; i++) {
            T key = result[i];

            // Find position using binary search
            int pos = binarySearchPosition(result, 0, i - 1, key);

            // Shift elements to make space
            for (int j = i - 1; j >= pos; j--) {
                result[j + 1] = result[j];
            }

            result[pos] = key;
        }

        return result;
    }

    /**
     * Find the position where key should be inserted.
     */
    private static <T extends Comparable<T>> int binarySearchPosition(T[] arr, int left, int right, T key) {
        if (right <= left) {
            return key.compareTo(arr[left]) > 0 ? left + 1 : left;
        }

        int mid = (left + right) / 2;

        if (key.compareTo(arr[mid]) == 0) {
            return mid + 1;
        }

        if (key.compareTo(arr[mid]) > 0) {
            return binarySearchPosition(arr, mid + 1, right, key);
        }

        return binarySearchPosition(arr, left, mid - 1, key);
    }

    /**
     * Shell sort - a generalization of insertion sort.
     *
     * @param arr Array to be sorted
     * @param <T> Type of elements
     * @return New sorted array
     *
     * Time Complexity: Depends on gap sequence (O(n log²n) for good sequences)
     */
    public static <T extends Comparable<T>> T[] shellSort(T[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();
        int n = result.length;

        // Start with a large gap, then reduce (Knuth's sequence)
        int gap = 1;
        while (gap < n / 3) {
            gap = 3 * gap + 1;
        }

        // Perform gapped insertion sort
        while (gap > 0) {
            for (int i = gap; i < n; i++) {
                T key = result[i];
                int j = i;

                // Insertion sort with gap
                while (j >= gap && result[j - gap].compareTo(key) > 0) {
                    result[j] = result[j - gap];
                    j -= gap;
                }

                result[j] = key;
            }

            gap /= 3;
        }

        return result;
    }

    /**
     * Insertion sort with custom comparator.
     *
     * @param arr Array to be sorted
     * @param comparator Custom comparator
     * @param <T> Type of elements
     * @return New sorted array
     */
    public static <T> T[] insertionSortWithComparator(T[] arr, Comparator<T> comparator) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();

        for (int i = 1; i < result.length; i++) {
            T key = result[i];
            int j = i - 1;

            while (j >= 0 && comparator.compare(result[j], key) > 0) {
                result[j + 1] = result[j];
                j--;
            }

            result[j + 1] = key;
        }

        return result;
    }

    // Overloaded methods for primitive types

    /**
     * Insertion sort for int arrays.
     */
    public static int[] insertionSort(int[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        int[] result = arr.clone();
        insertionSortInPlace(result);
        return result;
    }

    /**
     * In-place insertion sort for int arrays.
     */
    public static void insertionSortInPlace(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int key = arr[i];
            int j = i - 1;

            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }

            arr[j + 1] = key;
        }
    }

    /**
     * Check if array is sorted.
     */
    public static <T extends Comparable<T>> boolean isSorted(T[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i].compareTo(arr[i + 1]) > 0) {
                return false;
            }
        }
        return true;
    }

    public static boolean isSorted(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i] > arr[i + 1]) {
                return false;
            }
        }
        return true;
    }

    /**
     * Statistics class for tracking sort operations.
     */
    public static class SortStatistics {
        public int comparisons = 0;
        public int swaps = 0;

        public void reset() {
            comparisons = 0;
            swaps = 0;
        }

        @Override
        public String toString() {
            return String.format("Comparisons: %d, Swaps: %d", comparisons, swaps);
        }
    }

    /**
     * Insertion sort with statistics tracking.
     */
    public static <T extends Comparable<T>> T[] insertionSortWithStats(T[] arr, SortStatistics stats) {
        stats.reset();

        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();

        for (int i = 1; i < result.length; i++) {
            T key = result[i];
            int j = i - 1;

            while (j >= 0) {
                stats.comparisons++;
                if (result[j].compareTo(key) > 0) {
                    result[j + 1] = result[j];
                    stats.swaps++;
                    j--;
                } else {
                    break;
                }
            }

            result[j + 1] = key;
        }

        return result;
    }

    /**
     * Visualize insertion sort steps.
     */
    public static String[] visualizeInsertionSort(int[] arr) {
        List<String> steps = new ArrayList<>();
        int[] result = arr.clone();
        steps.add("Initial: " + Arrays.toString(result));

        for (int i = 1; i < result.length; i++) {
            int key = result[i];
            int j = i - 1;

            steps.add("\nStep " + i + ": Inserting " + key);
            steps.add("  Before: " + Arrays.toString(result));

            while (j >= 0 && result[j] > key) {
                result[j + 1] = result[j];
                j--;
            }

            result[j + 1] = key;
            steps.add("  After:  " + Arrays.toString(result));
        }

        steps.add("\nFinal: " + Arrays.toString(result));
        return steps.toArray(new String[0]);
    }

    /**
     * Demonstrate stability of insertion sort.
     */
    public static void demonstrateStability() {
        // Using arrays of Pairs to track stability
        class Pair implements Comparable<Pair> {
            int value;
            int originalIndex;

            Pair(int value, int originalIndex) {
                this.value = value;
                this.originalIndex = originalIndex;
            }

            @Override
            public int compareTo(Pair other) {
                return Integer.compare(this.value, other.value);
            }

            @Override
            public String toString() {
                return "(" + value + "," + originalIndex + ")";
            }
        }

        Pair[] data = {
            new Pair(3, 0),
            new Pair(1, 1),
            new Pair(3, 2),
            new Pair(2, 3),
            new Pair(3, 4)
        };

        System.out.println("Stability Demonstration:");
        System.out.print("Original: ");
        for (Pair p : data) System.out.print(p + " ");
        System.out.println();

        Pair[] sorted = insertionSort(data);
        System.out.print("Sorted:   ");
        for (Pair p : sorted) System.out.print(p + " ");
        System.out.println();

        // Check stability - elements with value 3 should maintain order
        List<Integer> threeIndices = new ArrayList<>();
        for (Pair p : sorted) {
            if (p.value == 3) {
                threeIndices.add(p.originalIndex);
            }
        }

        boolean isStable = threeIndices.equals(Arrays.asList(0, 2, 4));
        System.out.println("Stable: " + isStable + " (indices of 3's: " + threeIndices + ")");
    }

    /**
     * Demonstrate various insertion sort implementations.
     */
    public static void demonstrateInsertionSort() {
        System.out.println("📝 Insertion Sort Implementation in Java");
        System.out.println("=".repeat(60));

        // Test data
        Object[][] testCases = {
            {new Integer[]{64, 34, 25, 12, 22, 11, 90}, "Random array"},
            {new Integer[]{5, 2, 8, 6, 1, 9, 4}, "Small random array"},
            {new Integer[]{1}, "Single element"},
            {new Integer[]{}, "Empty array"},
            {new Integer[]{3, 3, 3, 3, 3}, "All duplicates"},
            {new Integer[]{9, 8, 7, 6, 5, 4, 3, 2, 1}, "Reverse sorted"},
            {new Integer[]{1, 2, 3, 4, 5}, "Already sorted"},
            {new Integer[]{1, 3, 2, 4, 5}, "Nearly sorted"}
        };

        System.out.println("\n📋 Basic Sorting Tests:");
        System.out.println("-".repeat(60));

        for (Object[] testCase : testCases) {
            Integer[] arr = (Integer[]) testCase[0];
            String desc = (String) testCase[1];

            Integer[] original = arr.clone();
            Integer[] standardResult = insertionSort(arr);
            Integer[] binaryResult = binaryInsertionSort(arr);
            Integer[] shellResult = shellSort(arr);
            Integer[] recursiveResult = insertionSortRecursive(arr);

            System.out.println("\nTest: " + desc);
            System.out.println("Original:  " + Arrays.toString(original));
            System.out.println("Sorted:    " + Arrays.toString(standardResult));

            boolean allCorrect = isSorted(standardResult) && isSorted(binaryResult) &&
                                isSorted(shellResult) && isSorted(recursiveResult);
            boolean allEqual = Arrays.equals(standardResult, binaryResult) &&
                              Arrays.equals(standardResult, shellResult) &&
                              Arrays.equals(standardResult, recursiveResult);

            String status = allCorrect && allEqual ? "✓" : "✗";
            System.out.println("All implementations match: " + status);
        }

        // Visualization demo
        System.out.println("\n\n🎬 Step-by-Step Visualization:");
        System.out.println("-".repeat(60));

        int[] demoArr = {5, 2, 8, 6, 1};
        String[] steps = visualizeInsertionSort(demoArr);
        for (String step : steps) {
            System.out.println(step);
        }

        // Stability demonstration
        System.out.println("\n\n🔒 Stability Demonstration:");
        System.out.println("-".repeat(60));
        demonstrateStability();

        // Performance analysis
        System.out.println("\n\n📊 Operation Counting:");
        System.out.println("-".repeat(60));

        Integer[][] statTestCases = {
            {5, 2, 8, 6, 1},
            {1, 2, 3, 4, 5},
            {5, 4, 3, 2, 1}
        };
        String[] descriptions = {"Random", "Already sorted", "Reverse sorted"};

        for (int i = 0; i < statTestCases.length; i++) {
            Integer[] arr = statTestCases[i];
            String desc = descriptions[i];

            SortStatistics stats = new SortStatistics();
            insertionSortWithStats(arr, stats);

            int n = arr.length;
            System.out.println("\n" + desc + ": " + Arrays.toString(arr));
            System.out.println("Array size (n): " + n);
            System.out.println("Comparisons: " + stats.comparisons);
            System.out.println("Swaps: " + stats.swaps);
            System.out.println("Best case comparisons: " + (n - 1));
            System.out.println("Worst case comparisons: " + (n * (n - 1) / 2));
        }
    }

    /**
     * Benchmark insertion sort.
     */
    public static void performanceBenchmark() {
        System.out.println("\n\n⚡ Performance Benchmark");
        System.out.println("=".repeat(80));
        System.out.println("\nInsertion sort is preferred for:");
        System.out.println("  • Small arrays (typically n < 10-20)");
        System.out.println("  • Nearly sorted arrays");
        System.out.println("  • As part of hybrid sorting algorithms");
        System.out.println();

        int[] sizes = {5, 10, 20, 50, 100, 500, 1000};
        Random random = new Random(42);

        Map<String, java.util.function.Function<Integer, int[]>> patterns = new LinkedHashMap<>();
        patterns.put("Random", n -> random.ints(n, 1, 1001).toArray());
        patterns.put("Nearly Sorted", n -> {
            int[] arr = java.util.stream.IntStream.range(0, n).toArray();
            for (int i = 0; i < Math.min(5, n / 10); i++) {
                int idx1 = random.nextInt(n);
                int idx2 = random.nextInt(n);
                int temp = arr[idx1];
                arr[idx1] = arr[idx2];
                arr[idx2] = temp;
            }
            return arr;
        });
        patterns.put("Reversed", n -> java.util.stream.IntStream.range(0, n).map(i -> n - i).toArray());

        for (Map.Entry<String, java.util.function.Function<Integer, int[]>> pattern : patterns.entrySet()) {
            System.out.println("\n" + pattern.getKey() + " Data:");
            System.out.printf("%-8s%15s%15s%15s%15s%n", "Size", "Insertion", "Binary", "Shell", "Arrays.sort");
            System.out.println("-".repeat(68));

            for (int size : sizes) {
                int[] testData = pattern.getValue().apply(size);
                System.out.printf("%-8d", size);

                // Insertion Sort
                long start = System.nanoTime();
                insertionSort(testData.clone());
                long end = System.nanoTime();
                System.out.printf("%14.3fms", (end - start) / 1_000_000.0);

                // Binary Insertion Sort
                Integer[] testDataObj = Arrays.stream(testData).boxed().toArray(Integer[]::new);
                start = System.nanoTime();
                binaryInsertionSort(testDataObj);
                end = System.nanoTime();
                System.out.printf("%14.3fms", (end - start) / 1_000_000.0);

                // Shell Sort
                start = System.nanoTime();
                shellSort(testDataObj);
                end = System.nanoTime();
                System.out.printf("%14.3fms", (end - start) / 1_000_000.0);

                // Arrays.sort
                int[] testData2 = testData.clone();
                start = System.nanoTime();
                Arrays.sort(testData2);
                end = System.nanoTime();
                System.out.printf("%14.3fms%n", (end - start) / 1_000_000.0);
            }
        }
    }

    public static void main(String[] args) {
        demonstrateInsertionSort();
        performanceBenchmark();

        System.out.println("\n✨ Insertion Sort demonstration complete!");
    }
}

