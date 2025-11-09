/**
 * Bubble Sort Algorithm Implementation in Java
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
 * Java features:
 * - Generic methods for type safety
 * - Multiple implementation patterns
 * - Overloaded methods
 * - Custom comparators
 * - Utility classes
 */

import java.util.*;
import java.util.function.BiFunction;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class BubbleSort {

    /**
     * Basic iterative bubble sort implementation.
     *
     * This is the standard bubble sort algorithm that compares and swaps
     * adjacent elements until the entire array is sorted.
     *
     * @param arr Array to be sorted
     * @param <T> Type of elements (must be Comparable)
     * @return New sorted array
     *
     * Time Complexity: O(n²) in all cases (no optimization)
     * Space Complexity: O(n) for the new array
     */
    public static <T extends Comparable<T>> T[] bubbleSortIterative(T[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();
        int n = result.length;

        // Outer loop for number of passes
        for (int i = 0; i < n; i++) {
            // Inner loop for comparisons
            // After each pass, the largest element "bubbles up" to its position
            for (int j = 0; j < n - i - 1; j++) {
                if (result[j].compareTo(result[j + 1]) > 0) {
                    // Swap adjacent elements
                    swap(result, j, j + 1);
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
     * @param arr Array to be sorted
     * @param <T> Type of elements (must be Comparable)
     * @return New sorted array
     *
     * Time Complexity:
     *   - Best Case: O(n) when already sorted
     *   - Average/Worst: O(n²)
     * Space Complexity: O(n) for the new array
     */
    public static <T extends Comparable<T>> T[] bubbleSortOptimized(T[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();
        int n = result.length;

        for (int i = 0; i < n; i++) {
            // Flag to optimize for already sorted arrays
            boolean swapped = false;

            for (int j = 0; j < n - i - 1; j++) {
                if (result[j].compareTo(result[j + 1]) > 0) {
                    swap(result, j, j + 1);
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
     * @param arr Array to be sorted in-place
     * @param <T> Type of elements (must be Comparable)
     *
     * Time Complexity: O(n) best case, O(n²) average/worst
     * Space Complexity: O(1)
     */
    public static <T extends Comparable<T>> void bubbleSortInPlace(T[] arr) {
        int n = arr.length;

        for (int i = 0; i < n; i++) {
            boolean swapped = false;

            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j].compareTo(arr[j + 1]) > 0) {
                    swap(arr, j, j + 1);
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
     * @param arr Array to be sorted
     * @param n Size of the array portion to sort
     * @param <T> Type of elements (must be Comparable)
     *
     * Time Complexity: O(n²)
     * Space Complexity: O(n) for recursion stack
     */
    public static <T extends Comparable<T>> void bubbleSortRecursive(T[] arr, int n) {
        // Base case: single element or empty
        if (n <= 1) {
            return;
        }

        // One pass of bubble sort
        // After this pass, the largest element will be at the end
        for (int i = 0; i < n - 1; i++) {
            if (arr[i].compareTo(arr[i + 1]) > 0) {
                swap(arr, i, i + 1);
            }
        }

        // Recursively sort the first n-1 elements
        bubbleSortRecursive(arr, n - 1);
    }

    /**
     * Recursive bubble sort with array cloning.
     *
     * @param arr Array to be sorted
     * @param <T> Type of elements (must be Comparable)
     * @return New sorted array
     */
    public static <T extends Comparable<T>> T[] bubbleSortRecursive(T[] arr) {
        T[] result = arr.clone();
        bubbleSortRecursive(result, result.length);
        return result;
    }

    /**
     * Functional-style bubble sort implementation using streams.
     *
     * @param arr Array to be sorted
     * @param <T> Type of elements (must be Comparable)
     * @return New sorted array
     *
     * Time Complexity: O(n²)
     * Space Complexity: O(n)
     */
    public static <T extends Comparable<T>> T[] bubbleSortFunctional(T[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();
        int n = result.length;

        // Functional approach with IntStream
        IntStream.range(0, n).forEach(i -> {
            boolean[] swapped = {false}; // Array to make it effectively final

            IntStream.range(0, n - i - 1).forEach(j -> {
                if (result[j].compareTo(result[j + 1]) > 0) {
                    swap(result, j, j + 1);
                    swapped[0] = true;
                }
            });
        });

        return result;
    }

    /**
     * Bubble sort with custom comparator.
     *
     * @param arr Array to be sorted
     * @param comparator Custom comparator
     * @param <T> Type of elements
     * @return New sorted array
     */
    public static <T> T[] bubbleSortWithComparator(T[] arr, Comparator<T> comparator) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();
        int n = result.length;

        for (int i = 0; i < n; i++) {
            boolean swapped = false;

            for (int j = 0; j < n - i - 1; j++) {
                if (comparator.compare(result[j], result[j + 1]) > 0) {
                    swap(result, j, j + 1);
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
     * @param arr Array to be sorted
     * @param <T> Type of elements (must be Comparable)
     * @return New sorted array
     *
     * Time Complexity: O(n²) worst case, but often faster than standard bubble sort
     * Space Complexity: O(n)
     */
    public static <T extends Comparable<T>> T[] cocktailSort(T[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();
        int start = 0;
        int end = result.length - 1;
        boolean swapped = true;

        while (swapped) {
            swapped = false;

            // Forward pass (like bubble sort)
            for (int i = start; i < end; i++) {
                if (result[i].compareTo(result[i + 1]) > 0) {
                    swap(result, i, i + 1);
                    swapped = true;
                }
            }

            if (!swapped) {
                break;
            }

            swapped = false;
            end--;

            // Backward pass
            for (int i = end - 1; i >= start; i--) {
                if (result[i].compareTo(result[i + 1]) > 0) {
                    swap(result, i, i + 1);
                    swapped = true;
                }
            }

            start++;
        }

        return result;
    }

    // Overloaded methods for primitive types

    /**
     * Optimized bubble sort for int arrays.
     */
    public static int[] bubbleSort(int[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        int[] result = arr.clone();
        int n = result.length;

        for (int i = 0; i < n; i++) {
            boolean swapped = false;

            for (int j = 0; j < n - i - 1; j++) {
                if (result[j] > result[j + 1]) {
                    int temp = result[j];
                    result[j] = result[j + 1];
                    result[j + 1] = temp;
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
     * Optimized bubble sort for double arrays.
     */
    public static double[] bubbleSort(double[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        double[] result = arr.clone();
        int n = result.length;

        for (int i = 0; i < n; i++) {
            boolean swapped = false;

            for (int j = 0; j < n - i - 1; j++) {
                if (result[j] > result[j + 1]) {
                    double temp = result[j];
                    result[j] = result[j + 1];
                    result[j + 1] = temp;
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
     * Swap two elements in an array.
     */
    private static <T> void swap(T[] arr, int i, int j) {
        T temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    /**
     * Check if array is sorted in ascending order.
     */
    public static <T extends Comparable<T>> boolean isSorted(T[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i].compareTo(arr[i + 1]) > 0) {
                return false;
            }
        }
        return true;
    }

    /**
     * Check if int array is sorted.
     */
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
        public int iterations = 0;

        @Override
        public String toString() {
            return String.format("Comparisons: %d, Swaps: %d, Iterations: %d",
                    comparisons, swaps, iterations);
        }
    }

    /**
     * Bubble sort with statistics tracking.
     */
    public static <T extends Comparable<T>> T[] bubbleSortWithStats(T[] arr, SortStatistics stats) {
        stats.comparisons = 0;
        stats.swaps = 0;
        stats.iterations = 0;

        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();
        int n = result.length;

        for (int i = 0; i < n; i++) {
            stats.iterations++;
            boolean swapped = false;

            for (int j = 0; j < n - i - 1; j++) {
                stats.comparisons++;
                if (result[j].compareTo(result[j + 1]) > 0) {
                    swap(result, j, j + 1);
                    stats.swaps++;
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
     * BubbleSorter class with state and statistics.
     */
    public static class BubbleSorter<T extends Comparable<T>> {
        private SortStatistics stats = new SortStatistics();

        public T[] sort(T[] arr) {
            return bubbleSortWithStats(arr, stats);
        }

        public SortStatistics getStats() {
            return stats;
        }

        public void resetStats() {
            stats = new SortStatistics();
        }
    }

    /**
     * Demonstrate various bubble sort implementations.
     */
    public static void demonstrateBubbleSort() {
        System.out.println("🫧 Bubble Sort Implementation in Java");
        System.out.println("=".repeat(50));

        // Test data - comprehensive edge cases
        Object[][] testCases = {
            {new Integer[]{64, 34, 25, 12, 22, 11, 90}, "Random array"},
            {new Integer[]{5, 2, 8, 6, 1, 9, 4}, "Small random array"},
            {new Integer[]{1}, "Single element"},
            {new Integer[]{}, "Empty array"},
            {new Integer[]{3, 3, 3, 3, 3}, "All duplicates"},
            {new Integer[]{9, 8, 7, 6, 5, 4, 3, 2, 1}, "Reverse sorted"},
            {new Integer[]{1, 2, 3, 4, 5}, "Already sorted"},
            {new Integer[]{5, 1, 4, 2, 3}, "Nearly sorted"}
        };

        System.out.println("\n📋 Basic Sorting Tests:");
        System.out.println("-".repeat(50));

        for (Object[] testCase : testCases) {
            Integer[] arr = (Integer[]) testCase[0];
            String desc = (String) testCase[1];

            Integer[] original = arr.clone();

            // Test different implementations
            Integer[] iterativeResult = bubbleSortIterative(arr);
            Integer[] optimizedResult = bubbleSortOptimized(arr);
            Integer[] recursiveResult = bubbleSortRecursive(arr);
            Integer[] cocktailResult = cocktailSort(arr);

            // Test in-place
            Integer[] inplaceResult = arr.clone();
            bubbleSortInPlace(inplaceResult);

            System.out.println("\nTest: " + desc);
            System.out.println("Original:  " + Arrays.toString(original));
            System.out.println("Sorted:    " + Arrays.toString(iterativeResult));

            // Verify all results are correct and equal
            boolean allCorrect = isSorted(iterativeResult) && isSorted(optimizedResult) &&
                                isSorted(recursiveResult) && isSorted(cocktailResult) &&
                                isSorted(inplaceResult);
            boolean allEqual = Arrays.equals(iterativeResult, optimizedResult) &&
                              Arrays.equals(iterativeResult, recursiveResult) &&
                              Arrays.equals(iterativeResult, cocktailResult) &&
                              Arrays.equals(iterativeResult, inplaceResult);

            String status = allCorrect && allEqual ? "✓" : "✗";
            System.out.println("All implementations match: " + status);
        }

        System.out.println("\n" + "-".repeat(50));

        // String sorting
        String[] words = {"banana", "apple", "cherry", "date", "elderberry"};
        String[] sortedWords = bubbleSortOptimized(words);

        System.out.println("\n🔤 Word sorting:");
        System.out.println("Original:     " + Arrays.toString(words));
        System.out.println("Alphabetical: " + Arrays.toString(sortedWords));

        // Custom comparison (descending)
        Integer[] numbers = {3, 1, 4, 1, 5, 9, 2, 6};
        Integer[] descSorted = bubbleSortWithComparator(numbers,
                (a, b) -> b.compareTo(a));

        System.out.println("\n🔢 Custom comparison (descending):");
        System.out.println("Original:   " + Arrays.toString(numbers));
        System.out.println("Descending: " + Arrays.toString(descSorted));

        // Primitive array
        int[] primitiveArr = {5, 2, 8, 1, 9};
        int[] sortedPrimitive = bubbleSort(primitiveArr);

        System.out.println("\n🔧 Primitive int array:");
        System.out.println("Original: " + Arrays.toString(primitiveArr));
        System.out.println("Sorted:   " + Arrays.toString(sortedPrimitive));
    }

    /**
     * Benchmark different bubble sort implementations.
     */
    public static void performanceBenchmark() {
        System.out.println("\n\n⚡ Performance Benchmark");
        System.out.println("=".repeat(70));

        int[] sizes = {100, 500, 1000, 2000};
        Random random = new Random(42); // Fixed seed for reproducibility

        // Test different data patterns
        Map<String, java.util.function.Function<Integer, Integer[]>> patterns = new LinkedHashMap<>();
        patterns.put("Random", n -> random.ints(n, 1, 1001).boxed().toArray(Integer[]::new));
        patterns.put("Sorted", n -> IntStream.range(0, n).boxed().toArray(Integer[]::new));
        patterns.put("Reversed", n -> IntStream.range(0, n).map(i -> n - i).boxed().toArray(Integer[]::new));
        patterns.put("Nearly Sorted", n -> {
            Integer[] arr = IntStream.range(0, n).boxed().toArray(Integer[]::new);
            for (int i = 0; i < Math.min(5, n / 10); i++) {
                int idx1 = random.nextInt(n);
                int idx2 = random.nextInt(n);
                Integer temp = arr[idx1];
                arr[idx1] = arr[idx2];
                arr[idx2] = temp;
            }
            return arr;
        });

        Map<String, java.util.function.Function<Integer[], Integer[]>> methods = new LinkedHashMap<>();
        methods.put("Iterative", BubbleSort::bubbleSortIterative);
        methods.put("Optimized", BubbleSort::bubbleSortOptimized);
        methods.put("Recursive", BubbleSort::bubbleSortRecursive);
        methods.put("Cocktail", BubbleSort::cocktailSort);
        methods.put("Arrays.sort", arr -> {
            Integer[] copy = arr.clone();
            Arrays.sort(copy);
            return copy;
        });

        for (Map.Entry<String, java.util.function.Function<Integer, Integer[]>> pattern : patterns.entrySet()) {
            System.out.println("\n" + pattern.getKey() + " Data:");

            // Header
            System.out.printf("%-8s", "Size");
            for (String method : methods.keySet()) {
                System.out.printf("%12s", method);
            }
            System.out.println();
            System.out.println("-".repeat(8 + 12 * methods.size()));

            for (int size : sizes) {
                Integer[] testData = pattern.getValue().apply(size);
                System.out.printf("%-8d", size);

                for (Map.Entry<String, java.util.function.Function<Integer[], Integer[]>> method : methods.entrySet()) {
                    // Skip recursive for large sizes
                    if (method.getKey().equals("Recursive") && size > 1000) {
                        System.out.printf("%12s", "N/A");
                        continue;
                    }

                    try {
                        // Warm-up
                        method.getValue().apply(testData.clone());

                        // Benchmark
                        long startTime = System.nanoTime();
                        Integer[] result = method.getValue().apply(testData.clone());
                        long endTime = System.nanoTime();

                        double elapsedMs = (endTime - startTime) / 1_000_000.0;
                        System.out.printf("%11.2fms", elapsedMs);

                        // Verify correctness
                        if (!isSorted(result)) {
                            System.out.print(" ✗");
                        }
                    } catch (StackOverflowError e) {
                        System.out.printf("%12s", "OVERFLOW");
                    }
                }

                System.out.println();
            }
        }
    }

    /**
     * Analyze bubble sort behavior with different inputs.
     */
    public static void analyzeAlgorithm() {
        System.out.println("\n\n🔍 Algorithm Analysis");
        System.out.println("=".repeat(50));

        Object[][] testCases = {
            {new Integer[]{5, 2, 8, 6, 1}, "Random"},
            {new Integer[]{1, 2, 3, 4, 5}, "Already sorted"},
            {new Integer[]{5, 4, 3, 2, 1}, "Reverse sorted"}
        };

        for (Object[] testCase : testCases) {
            Integer[] arr = (Integer[]) testCase[0];
            String desc = (String) testCase[1];

            SortStatistics stats = new SortStatistics();
            bubbleSortWithStats(arr, stats);

            int n = arr.length;
            int theoreticalMax = n * (n - 1) / 2;

            System.out.println("\n" + desc + ": " + Arrays.toString(arr));
            System.out.println("Array size (n): " + n);
            System.out.println("Comparisons: " + stats.comparisons +
                             " (theoretical max: " + theoreticalMax + ")");
            System.out.println("Swaps: " + stats.swaps);
            System.out.printf("Efficiency: %.1f%% (fewer swaps is better)%n",
                    (1 - stats.swaps / (double) Math.max(stats.comparisons, 1)) * 100);
        }
    }

    /**
     * Main method for demonstration.
     */
    public static void main(String[] args) {
        demonstrateBubbleSort();
        performanceBenchmark();
        analyzeAlgorithm();

        // Demonstrate OOP approach
        System.out.println("\n\n📊 Object-Oriented Approach");
        System.out.println("=".repeat(50));

        BubbleSorter<Integer> sorter = new BubbleSorter<>();
        Integer[] testArray = {64, 34, 25, 12, 22, 11, 90};

        Integer[] sortedArray = sorter.sort(testArray);
        SortStatistics stats = sorter.getStats();

        System.out.println("Original: " + Arrays.toString(testArray));
        System.out.println("Sorted:   " + Arrays.toString(sortedArray));
        System.out.println("Statistics: " + stats);

        System.out.println("\n✨ Bubble Sort demonstration complete!");
    }
}
