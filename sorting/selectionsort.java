/**
 * Selection Sort Algorithm - Educational Implementation (Java)
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
 */

import java.util.*;
import java.util.function.BiFunction;

public class SelectionSort {

    // ============================================================================
    // STANDARD SELECTION SORT
    // ============================================================================

    /**
     * Standard selection sort implementation for generic comparable types.
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
     * Time: O(n²), Space: O(n) for new array
     *
     * @param arr The array to sort
     * @param <T> The type of elements (must be Comparable)
     * @return A new sorted array
     */
    public static <T extends Comparable<T>> T[] sort(T[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();
        sortInPlace(result);
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
     * @param arr The array to sort (modified in-place)
     * @param <T> The type of elements (must be Comparable)
     */
    public static <T extends Comparable<T>> void sortInPlace(T[] arr) {
        int n = arr.length;

        // Outer loop: Move boundary of unsorted subarray one by one
        for (int i = 0; i < n - 1; i++) {
            // Find the minimum element in the remaining unsorted array
            // Start by assuming the first unsorted element is the minimum
            int minIdx = i;

            // Inner loop: Search for the minimum in arr[i+1...n-1]
            for (int j = i + 1; j < n; j++) {
                // If we find a smaller element, update minIdx
                if (arr[j].compareTo(arr[minIdx]) < 0) {
                    minIdx = j;
                }
            }

            // Swap the found minimum element with the first element
            // of the unsorted portion
            if (minIdx != i) {
                T temp = arr[i];
                arr[i] = arr[minIdx];
                arr[minIdx] = temp;
            }
        }
    }

    /**
     * Selection sort for primitive int arrays (more efficient).
     *
     * @param arr The array to sort
     * @return A new sorted array
     */
    public static int[] sort(int[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        int[] result = arr.clone();
        sortInPlace(result);
        return result;
    }

    /**
     * In-place selection sort for primitive int arrays.
     *
     * @param arr The array to sort (modified in-place)
     */
    public static void sortInPlace(int[] arr) {
        int n = arr.length;

        for (int i = 0; i < n - 1; i++) {
            int minIdx = i;

            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                }
            }

            if (minIdx != i) {
                int temp = arr[i];
                arr[i] = arr[minIdx];
                arr[minIdx] = temp;
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
     * Time: Still O(n²), but approximately 2x faster in practice
     *
     * @param arr The array to sort
     * @return A new sorted array
     */
    public static int[] bidirectionalSort(int[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        int[] result = arr.clone();
        int n = result.length;

        // Process from both ends toward the middle
        int left = 0;
        int right = n - 1;

        while (left < right) {
            // Find both minimum and maximum in the current range
            int minIdx = left;
            int maxIdx = left;

            for (int i = left; i <= right; i++) {
                if (result[i] < result[minIdx]) {
                    minIdx = i;
                }
                if (result[i] > result[maxIdx]) {
                    maxIdx = i;
                }
            }

            // Handle special case: if min is at right position
            if (minIdx == right) {
                swap(result, left, right);
                if (maxIdx == left) {
                    maxIdx = right;
                }
            } else {
                // Swap minimum to the left boundary
                if (minIdx != left) {
                    swap(result, left, minIdx);
                }

                // If maximum was at left position, it's now at minIdx
                if (maxIdx == left) {
                    maxIdx = minIdx;
                }

                // Swap maximum to the right boundary
                if (maxIdx != right) {
                    swap(result, right, maxIdx);
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
     * @param arr The array to sort
     * @return A new sorted array
     */
    public static int[] sortRecursive(int[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        int[] result = arr.clone();
        sortRecursiveHelper(result, 0);
        return result;
    }

    /**
     * Helper function for recursive selection sort.
     *
     * @param arr The array to sort
     * @param startIdx The starting index for the current recursion
     */
    private static void sortRecursiveHelper(int[] arr, int startIdx) {
        // Base case: if we've reached the end, we're done
        if (startIdx >= arr.length - 1) {
            return;
        }

        // Find the minimum element in arr[startIdx...n-1]
        int minIdx = startIdx;
        for (int i = startIdx + 1; i < arr.length; i++) {
            if (arr[i] < arr[minIdx]) {
                minIdx = i;
            }
        }

        // Swap the minimum with the element at startIdx
        if (minIdx != startIdx) {
            swap(arr, startIdx, minIdx);
        }

        // Recursively sort the rest
        sortRecursiveHelper(arr, startIdx + 1);
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
     * @param arr The array to sort
     * @return A new sorted array
     */
    public static int[] stableSort(int[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        int[] result = arr.clone();
        int n = result.length;

        for (int i = 0; i < n - 1; i++) {
            // Find minimum in unsorted portion
            int minIdx = i;
            for (int j = i + 1; j < n; j++) {
                if (result[j] < result[minIdx]) {
                    minIdx = j;
                }
            }

            // Instead of swapping, shift elements and insert
            if (minIdx != i) {
                int minValue = result[minIdx];
                // Shift all elements between i and minIdx one position right
                for (int k = minIdx; k > i; k--) {
                    result[k] = result[k - 1];
                }
                // Place minimum at position i
                result[i] = minValue;
            }
        }

        return result;
    }

    // ============================================================================
    // UTILITY METHODS
    // ============================================================================

    /**
     * Swap two elements in an array.
     */
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    /**
     * Check if an array is sorted.
     */
    public static boolean isSorted(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i] > arr[i + 1]) {
                return false;
            }
        }
        return true;
    }

    // ============================================================================
    // VISUALIZATION AND STATISTICS
    // ============================================================================

    /**
     * Class to track sorting operations for analysis.
     */
    public static class SortStatistics {
        public int comparisons = 0;
        public int swaps = 0;
        public int arrayAccesses = 0;

        public void reset() {
            comparisons = 0;
            swaps = 0;
            arrayAccesses = 0;
        }

        @Override
        public String toString() {
            return String.format("Comparisons: %d, Swaps: %d, Array Accesses: %d",
                    comparisons, swaps, arrayAccesses);
        }
    }

    /**
     * Selection sort with operation counting.
     */
    public static int[] sortWithStats(int[] arr, SortStatistics stats) {
        stats.reset();
        if (arr.length <= 1) {
            return arr.clone();
        }

        int[] result = arr.clone();
        int n = result.length;

        for (int i = 0; i < n - 1; i++) {
            int minIdx = i;
            stats.arrayAccesses++;

            for (int j = i + 1; j < n; j++) {
                stats.comparisons++;
                stats.arrayAccesses += 2;  // Read result[j] and result[minIdx]
                if (result[j] < result[minIdx]) {
                    minIdx = j;
                }
            }

            if (minIdx != i) {
                stats.swaps++;
                stats.arrayAccesses += 4;  // Two reads, two writes
                swap(result, i, minIdx);
            }
        }

        return result;
    }

    /**
     * Create ASCII visualization of selection sort process.
     */
    public static List<String> visualizeSelectionSort(int[] arr) {
        List<String> steps = new ArrayList<>();
        int[] result = arr.clone();
        int n = result.length;

        steps.add("=".repeat(70));
        steps.add("SELECTION SORT VISUALIZATION");
        steps.add("=".repeat(70));
        steps.add("Initial array: " + Arrays.toString(result));
        steps.add("");

        for (int i = 0; i < n - 1; i++) {
            steps.add(String.format("Pass %d:", i + 1));
            int[] unsorted = Arrays.copyOfRange(result, i, n);
            steps.add(String.format("  Looking for minimum in unsorted portion: %s",
                    Arrays.toString(unsorted)));

            int minIdx = i;
            int minValue = result[i];

            // Show the search process
            for (int j = i + 1; j < n; j++) {
                if (result[j] < minValue) {
                    minIdx = j;
                    minValue = result[j];
                    steps.add(String.format("    Found new minimum: %d at index %d",
                            minValue, minIdx));
                }
            }

            // Show the swap
            if (minIdx != i) {
                steps.add(String.format("  Swapping %d ↔ %d", result[i], result[minIdx]));
                swap(result, i, minIdx);
            } else {
                steps.add("  No swap needed (minimum already in place)");
            }

            // Show current state
            int[] sorted = Arrays.copyOfRange(result, 0, i + 1);
            int[] unsortedPart = Arrays.copyOfRange(result, i + 1, n);
            steps.add(String.format("  Sorted: %s | Unsorted: %s",
                    Arrays.toString(sorted), Arrays.toString(unsortedPart)));
            steps.add("");
        }

        steps.add("Final sorted array: " + Arrays.toString(result));
        steps.add("=".repeat(70));

        return steps;
    }

    // ============================================================================
    // DEMONSTRATIONS AND TESTING
    // ============================================================================

    /**
     * Comprehensive demonstration of selection sort.
     */
    public static void demonstrate() {
        System.out.println("📚 SELECTION SORT - EDUCATIONAL DEMONSTRATION");
        System.out.println("=".repeat(80));

        // Test cases
        int[][] testCases = {
                {64, 25, 12, 22, 11},
                {5, 2, 8, 6, 1, 9, 4},
                {1},
                {},
                {3, 3, 3, 3, 3},
                {9, 8, 7, 6, 5, 4, 3, 2, 1},
                {1, 2, 3, 4, 5},
                {1, 3, 2, 4, 5}
        };
        String[] descriptions = {
                "Random array",
                "Small random array",
                "Single element",
                "Empty array",
                "All duplicates",
                "Reverse sorted",
                "Already sorted",
                "Nearly sorted"
        };

        System.out.println("\n📋 BASIC FUNCTIONALITY TESTS:");
        System.out.println("-".repeat(80));

        for (int i = 0; i < testCases.length; i++) {
            int[] arr = testCases[i];
            int[] standard = sort(arr);
            int[] bidirectional = bidirectionalSort(arr);
            int[] recursive = sortRecursive(arr);
            int[] stable = stableSort(arr);

            System.out.println("\nTest: " + descriptions[i]);
            System.out.println("Original:      " + Arrays.toString(arr));
            System.out.println("Standard:      " + Arrays.toString(standard));
            System.out.println("Bidirectional: " + Arrays.toString(bidirectional));
            System.out.println("Recursive:     " + Arrays.toString(recursive));
            System.out.println("Stable:        " + Arrays.toString(stable));

            boolean allCorrect = isSorted(standard) && isSorted(bidirectional) &&
                    isSorted(recursive) && isSorted(stable);
            String status = allCorrect ? "✓" : "✗";
            System.out.println("All correct: " + status);
        }

        // Visualization
        System.out.println("\n\n🎬 STEP-BY-STEP VISUALIZATION:");
        System.out.println("-".repeat(80));
        int[] demoArr = {64, 25, 12, 22, 11};
        List<String> steps = visualizeSelectionSort(demoArr);
        for (String step : steps) {
            System.out.println(step);
        }

        // Memory analysis
        System.out.println("\n\n💾 MEMORY USAGE ANALYSIS:");
        System.out.println("-".repeat(80));
        System.out.println("""
                Selection Sort Memory Characteristics:

                1. In-Place Sorting:
                   - Space Complexity: O(1) auxiliary space
                   - Only uses a constant amount of extra memory (minIdx, loop variables)
                   - Original array is modified in-place

                2. Memory Writes:
                   - Selection Sort: O(n) swaps (minimum writes)
                   - Bubble Sort: O(n²) swaps in worst case
                   - Insertion Sort: O(n²) shifts in worst case

                   ⭐ This makes Selection Sort ideal when writing to memory is expensive!
                      Examples: Flash memory, EEPROM, or distributed systems
                """);
    }

    /**
     * Main method to run demonstration.
     */
    public static void main(String[] args) {
        demonstrate();
        System.out.println("\n✨ Selection Sort demonstration complete!");
    }
}
