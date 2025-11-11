/**
 * Binary Search Algorithm Collection in Java
 *
 * Comprehensive implementation of binary search variants including:
 * 1. Classic binary search (iterative & recursive)
 * 2. First/last occurrence finding
 * 3. Rotated array search
 * 4. Exponential search
 * 5. Interpolation search
 * 6. Ternary search
 * 7. Binary search on answer (optimization)
 * 8. Advanced utilities
 *
 * Time Complexity: O(log n) for most variants
 * Space Complexity: O(1) iterative, O(log n) recursive
 *
 * Java Features:
 * - Generic types with bounded wildcards
 * - Comparator interface for custom comparisons
 * - Functional interfaces and lambda expressions
 * - Exception handling
 * - Comprehensive documentation
 */

import java.util.*;
import java.util.function.*;

public class BinarySearch {

    // ==========================================================================
    // 1. CLASSIC BINARY SEARCH
    // ==========================================================================

    /**
     * Classic binary search - iterative implementation.
     *
     * @param arr Sorted array of comparable elements
     * @param target Element to search for
     * @return Index of target if found, -1 otherwise
     * @param <T> Type that implements Comparable
     *
     * Time Complexity: O(log n)
     * Space Complexity: O(1)
     */
    public static <T extends Comparable<T>> int binarySearchIterative(T[] arr, T target) {
        if (arr == null || arr.length == 0) {
            return -1;
        }

        int left = 0;
        int right = arr.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;  // Avoid overflow

            int comparison = arr[mid].compareTo(target);

            if (comparison == 0) {
                return mid;
            } else if (comparison < 0) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return -1;
    }

    /**
     * Classic binary search - recursive implementation.
     *
     * @param arr Sorted array
     * @param target Element to search for
     * @return Index of target if found, -1 otherwise
     *
     * Time Complexity: O(log n)
     * Space Complexity: O(log n) - recursion stack
     */
    public static <T extends Comparable<T>> int binarySearchRecursive(T[] arr, T target) {
        if (arr == null || arr.length == 0) {
            return -1;
        }
        return binarySearchRecursiveHelper(arr, target, 0, arr.length - 1);
    }

    private static <T extends Comparable<T>> int binarySearchRecursiveHelper(
            T[] arr, T target, int left, int right) {

        if (left > right) {
            return -1;
        }

        int mid = left + (right - left) / 2;
        int comparison = arr[mid].compareTo(target);

        if (comparison == 0) {
            return mid;
        } else if (comparison < 0) {
            return binarySearchRecursiveHelper(arr, target, mid + 1, right);
        } else {
            return binarySearchRecursiveHelper(arr, target, left, mid - 1);
        }
    }

    /**
     * Generic binary search with custom comparator.
     *
     * @param arr Sorted array
     * @param target Element to search for
     * @param comparator Custom comparator
     * @return Index of target if found, -1 otherwise
     */
    public static <T> int binarySearchWithComparator(
            T[] arr, T target, Comparator<T> comparator) {

        if (arr == null || arr.length == 0) {
            return -1;
        }

        int left = 0;
        int right = arr.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            int comparison = comparator.compare(arr[mid], target);

            if (comparison == 0) {
                return mid;
            } else if (comparison < 0) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return -1;
    }

    // ==========================================================================
    // 2. FIRST/LAST OCCURRENCE
    // ==========================================================================

    /**
     * Find first (leftmost) occurrence of target in sorted array.
     *
     * @param arr Sorted array (may contain duplicates)
     * @param target Element to search for
     * @return Index of first occurrence, -1 if not found
     */
    public static <T extends Comparable<T>> int findFirstOccurrence(T[] arr, T target) {
        if (arr == null || arr.length == 0) {
            return -1;
        }

        int left = 0;
        int right = arr.length - 1;
        int result = -1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            int comparison = arr[mid].compareTo(target);

            if (comparison == 0) {
                result = mid;
                right = mid - 1;  // Continue searching left
            } else if (comparison < 0) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return result;
    }

    /**
     * Find last (rightmost) occurrence of target in sorted array.
     *
     * @param arr Sorted array (may contain duplicates)
     * @param target Element to search for
     * @return Index of last occurrence, -1 if not found
     */
    public static <T extends Comparable<T>> int findLastOccurrence(T[] arr, T target) {
        if (arr == null || arr.length == 0) {
            return -1;
        }

        int left = 0;
        int right = arr.length - 1;
        int result = -1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            int comparison = arr[mid].compareTo(target);

            if (comparison == 0) {
                result = mid;
                left = mid + 1;  // Continue searching right
            } else if (comparison < 0) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return result;
    }

    /**
     * Count total occurrences of target in sorted array.
     *
     * @param arr Sorted array
     * @param target Element to count
     * @return Number of occurrences
     */
    public static <T extends Comparable<T>> int countOccurrences(T[] arr, T target) {
        int first = findFirstOccurrence(arr, target);
        if (first == -1) {
            return 0;
        }

        int last = findLastOccurrence(arr, target);
        return last - first + 1;
    }

    /**
     * Find range [start, end] of target in sorted array.
     *
     * @param arr Sorted array
     * @param target Element to search for
     * @return Array of [first, last] indices, [-1, -1] if not found
     */
    public static <T extends Comparable<T>> int[] searchRange(T[] arr, T target) {
        int first = findFirstOccurrence(arr, target);
        if (first == -1) {
            return new int[]{-1, -1};
        }

        int last = findLastOccurrence(arr, target);
        return new int[]{first, last};
    }

    // ==========================================================================
    // 3. ROTATED SORTED ARRAY SEARCH
    // ==========================================================================

    /**
     * Search in rotated sorted array.
     *
     * @param arr Rotated sorted array (no duplicates)
     * @param target Element to search for
     * @return Index of target if found, -1 otherwise
     */
    public static <T extends Comparable<T>> int searchRotatedArray(T[] arr, T target) {
        if (arr == null || arr.length == 0) {
            return -1;
        }

        int left = 0;
        int right = arr.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (arr[mid].compareTo(target) == 0) {
                return mid;
            }

            // Determine which half is sorted
            if (arr[left].compareTo(arr[mid]) <= 0) {
                // Left half is sorted
                if (arr[left].compareTo(target) <= 0 && target.compareTo(arr[mid]) < 0) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } else {
                // Right half is sorted
                if (arr[mid].compareTo(target) < 0 && target.compareTo(arr[right]) <= 0) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
        }

        return -1;
    }

    /**
     * Find rotation point (minimum element) in rotated sorted array.
     *
     * @param arr Rotated sorted array
     * @return Index of minimum element
     */
    public static <T extends Comparable<T>> int findRotationPoint(T[] arr) {
        if (arr == null || arr.length == 0) {
            return -1;
        }

        int left = 0;
        int right = arr.length - 1;

        while (left < right) {
            int mid = left + (right - left) / 2;

            if (arr[mid].compareTo(arr[right]) > 0) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        return left;
    }

    // ==========================================================================
    // 4. EXPONENTIAL SEARCH
    // ==========================================================================

    /**
     * Exponential search - efficient for unbounded arrays.
     *
     * @param arr Sorted array
     * @param target Element to search for
     * @return Index of target if found, -1 otherwise
     */
    public static <T extends Comparable<T>> int exponentialSearch(T[] arr, T target) {
        if (arr == null || arr.length == 0) {
            return -1;
        }

        if (arr[0].compareTo(target) == 0) {
            return 0;
        }

        // Find range for binary search
        int i = 1;
        while (i < arr.length && arr[i].compareTo(target) <= 0) {
            i *= 2;
        }

        // Binary search in found range
        int left = i / 2;
        int right = Math.min(i, arr.length - 1);

        return binarySearchRecursiveHelper(arr, target, left, right);
    }

    // ==========================================================================
    // 5. INTERPOLATION SEARCH
    // ==========================================================================

    /**
     * Interpolation search - better for uniformly distributed data.
     *
     * @param arr Sorted array of integers
     * @param target Integer to search for
     * @return Index of target if found, -1 otherwise
     *
     * Time Complexity: O(log log n) average, O(n) worst
     */
    public static int interpolationSearch(int[] arr, int target) {
        if (arr == null || arr.length == 0) {
            return -1;
        }

        int left = 0;
        int right = arr.length - 1;

        while (left <= right && target >= arr[left] && target <= arr[right]) {
            if (left == right) {
                return arr[left] == target ? left : -1;
            }

            // Interpolation formula
            int pos = left + ((target - arr[left]) * (right - left)) /
                            (arr[right] - arr[left]);

            // Ensure pos is within bounds
            pos = Math.max(left, Math.min(pos, right));

            if (arr[pos] == target) {
                return pos;
            } else if (arr[pos] < target) {
                left = pos + 1;
            } else {
                right = pos - 1;
            }
        }

        return -1;
    }

    // ==========================================================================
    // 6. TERNARY SEARCH
    // ==========================================================================

    /**
     * Ternary search - divides array into three parts.
     *
     * @param arr Sorted array
     * @param target Element to search for
     * @return Index of target if found, -1 otherwise
     */
    public static <T extends Comparable<T>> int ternarySearch(T[] arr, T target) {
        if (arr == null || arr.length == 0) {
            return -1;
        }

        int left = 0;
        int right = arr.length - 1;

        while (left <= right) {
            int mid1 = left + (right - left) / 3;
            int mid2 = right - (right - left) / 3;

            if (arr[mid1].compareTo(target) == 0) {
                return mid1;
            }
            if (arr[mid2].compareTo(target) == 0) {
                return mid2;
            }

            if (target.compareTo(arr[mid1]) < 0) {
                right = mid1 - 1;
            } else if (target.compareTo(arr[mid2]) > 0) {
                left = mid2 + 1;
            } else {
                left = mid1 + 1;
                right = mid2 - 1;
            }
        }

        return -1;
    }

    /**
     * Ternary search for finding maximum of unimodal function.
     *
     * @param function Unimodal function
     * @param left Left boundary
     * @param right Right boundary
     * @param epsilon Precision threshold
     * @return x value where function reaches maximum
     */
    public static double ternarySearchMaximum(
            DoubleUnaryOperator function, double left, double right, double epsilon) {

        while (right - left > epsilon) {
            double mid1 = left + (right - left) / 3.0;
            double mid2 = right - (right - left) / 3.0;

            if (function.applyAsDouble(mid1) < function.applyAsDouble(mid2)) {
                left = mid1;
            } else {
                right = mid2;
            }
        }

        return (left + right) / 2.0;
    }

    // ==========================================================================
    // 7. BINARY SEARCH ON ANSWER
    // ==========================================================================

    /**
     * Binary search on answer space for optimization problems.
     *
     * @param predicate Function returning true if answer is feasible
     * @param low Minimum possible answer
     * @param high Maximum possible answer
     * @return Minimum value where predicate is true, -1 if no solution
     */
    public static int binarySearchOnAnswer(
            IntPredicate predicate, int low, int high) {

        int result = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (predicate.test(mid)) {
                result = mid;
                high = mid - 1;  // Try to find smaller answer
            } else {
                low = mid + 1;
            }
        }

        return result;
    }

    /**
     * Find integer square root using binary search.
     *
     * @param n Number to find square root of (non-negative)
     * @return Integer square root of n
     * @throws IllegalArgumentException if n is negative
     */
    public static int integerSquareRoot(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("Cannot compute square root of negative number");
        }

        if (n == 0 || n == 1) {
            return n;
        }

        int left = 0;
        int right = n;
        int result = 0;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            // Use long to avoid overflow
            long square = (long) mid * mid;

            if (square == n) {
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
     * Find square root with decimal precision using binary search.
     *
     * @param n Number to find square root of
     * @param precision Number of decimal places
     * @return Square root of n
     */
    public static double squareRoot(double n, int precision) {
        if (n < 0) {
            throw new IllegalArgumentException("Cannot compute square root of negative number");
        }

        if (n == 0.0 || n == 1.0) {
            return n;
        }

        // Find integer part
        double left = 0.0;
        double right = n;
        double result = 0.0;

        // Binary search for decimal precision
        double epsilon = Math.pow(10, -precision);

        while (right - left > epsilon) {
            double mid = left + (right - left) / 2.0;
            double square = mid * mid;

            if (Math.abs(square - n) < epsilon) {
                return mid;
            } else if (square < n) {
                result = mid;
                left = mid;
            } else {
                right = mid;
            }
        }

        return result;
    }

    // ==========================================================================
    // 8. ADVANCED UTILITIES
    // ==========================================================================

    /**
     * Find insertion position to maintain sorted order.
     *
     * @param arr Sorted array
     * @param target Element to insert
     * @return Index where target should be inserted
     */
    public static <T extends Comparable<T>> int searchInsertPosition(T[] arr, T target) {
        if (arr == null || arr.length == 0) {
            return 0;
        }

        int left = 0;
        int right = arr.length;

        while (left < right) {
            int mid = left + (right - left) / 2;

            if (arr[mid].compareTo(target) < 0) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        return left;
    }

    /**
     * Find element closest to target.
     *
     * @param arr Sorted array of integers
     * @param target Target value
     * @return Index of closest element
     */
    public static int findClosest(int[] arr, int target) {
        if (arr == null || arr.length == 0) {
            return -1;
        }

        if (arr.length == 1) {
            return 0;
        }

        int left = 0;
        int right = arr.length - 1;

        if (target <= arr[left]) {
            return left;
        }
        if (target >= arr[right]) {
            return right;
        }

        while (left < right) {
            int mid = left + (right - left) / 2;

            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        if (left > 0 && Math.abs(arr[left - 1] - target) < Math.abs(arr[left] - target)) {
            return left - 1;
        }

        return left;
    }

    /**
     * Find peak element in array (element greater than neighbors).
     *
     * @param arr Array of integers
     * @return Index of a peak element
     */
    public static int findPeakElement(int[] arr) {
        if (arr == null || arr.length == 0) {
            return -1;
        }

        if (arr.length == 1) {
            return 0;
        }

        int left = 0;
        int right = arr.length - 1;

        while (left < right) {
            int mid = left + (right - left) / 2;

            if (arr[mid] < arr[mid + 1]) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        return left;
    }

    // ==========================================================================
    // DEMONSTRATION AND TESTING
    // ==========================================================================

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("BINARY SEARCH ALGORITHM COLLECTION - JAVA");
        System.out.println("=".repeat(70));

        demonstrateClassicBinarySearch();
        demonstrateFirstLastOccurrence();
        demonstrateRotatedArraySearch();
        demonstrateExponentialSearch();
        demonstrateInterpolationSearch();
        demonstrateTernarySearch();
        demonstrateBinarySearchOnAnswer();
        demonstrateAdvancedUtilities();
        runPerformanceTests();

        System.out.println("\n" + "=".repeat(70));
        System.out.println("DEMONSTRATION COMPLETE");
        System.out.println("=".repeat(70));
    }

    private static void demonstrateClassicBinarySearch() {
        System.out.println("\n1. CLASSIC BINARY SEARCH");
        System.out.println("-".repeat(50));

        Integer[] arr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
        int[] targets = {7, 10, 1, 19};

        for (int target : targets) {
            int idxIter = binarySearchIterative(arr, target);
            int idxRec = binarySearchRecursive(arr, target);
            System.out.printf("Search %2d: Iterative=%2d, Recursive=%2d%n",
                            target, idxIter, idxRec);
        }

        // Custom comparator (case-insensitive)
        String[] strings = {"Apple", "banana", "Cherry", "date"};
        Comparator<String> caseInsensitive = String.CASE_INSENSITIVE_ORDER;
        int idx = binarySearchWithComparator(strings, "cherry", caseInsensitive);
        System.out.printf("Case-insensitive search for 'cherry': %d%n", idx);
    }

    private static void demonstrateFirstLastOccurrence() {
        System.out.println("\n2. FIRST/LAST OCCURRENCE");
        System.out.println("-".repeat(50));

        Integer[] arr = {1, 2, 2, 2, 3, 4, 4, 4, 4, 5};
        int[] targets = {2, 4, 6};

        for (int target : targets) {
            int first = findFirstOccurrence(arr, target);
            int last = findLastOccurrence(arr, target);
            int count = countOccurrences(arr, target);
            System.out.printf("Target %d: First=%2d, Last=%2d, Count=%d%n",
                            target, first, last, count);
        }
    }

    private static void demonstrateRotatedArraySearch() {
        System.out.println("\n3. ROTATED ARRAY SEARCH");
        System.out.println("-".repeat(50));

        Integer[] rotated = {4, 5, 6, 7, 0, 1, 2};
        int rotationPoint = findRotationPoint(rotated);

        System.out.println("Rotated array: " + Arrays.toString(rotated));
        System.out.printf("Rotation point: %d (value: %d)%n",
                        rotationPoint, rotated[rotationPoint]);

        int[] targets = {0, 3, 6};
        for (int target : targets) {
            int idx = searchRotatedArray(rotated, target);
            System.out.printf("Search %d: Index=%d%n", target, idx);
        }
    }

    private static void demonstrateExponentialSearch() {
        System.out.println("\n4. EXPONENTIAL SEARCH");
        System.out.println("-".repeat(50));

        Integer[] largeArr = new Integer[50];
        for (int i = 0; i < 50; i++) {
            largeArr[i] = i * 2 + 1;
        }

        int[] targets = {15, 51, 99};
        for (int target : targets) {
            int idx = exponentialSearch(largeArr, target);
            System.out.printf("Search %2d in array of size %d: Index=%d%n",
                            target, largeArr.length, idx);
        }
    }

    private static void demonstrateInterpolationSearch() {
        System.out.println("\n5. INTERPOLATION SEARCH");
        System.out.println("-".repeat(50));

        int[] uniformArr = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
        int[] targets = {30, 75, 100};

        for (int target : targets) {
            int idx = interpolationSearch(uniformArr, target);
            System.out.printf("Search %3d: Index=%d%n", target, idx);
        }
    }

    private static void demonstrateTernarySearch() {
        System.out.println("\n6. TERNARY SEARCH");
        System.out.println("-".repeat(50));

        Integer[] arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        int[] targets = {5, 1, 10, 11};

        for (int target : targets) {
            int idx = ternarySearch(arr, target);
            System.out.printf("Search %2d: Index=%d%n", target, idx);
        }

        // Unimodal function: -(x-5)^2 + 25 (peak at x=5)
        DoubleUnaryOperator func = x -> -(x - 5) * (x - 5) + 25;
        double maxX = ternarySearchMaximum(func, 0, 10, 1e-9);
        System.out.printf("Maximum of -(x-5)² + 25 at x ≈ %.6f%n", maxX);
    }

    private static void demonstrateBinarySearchOnAnswer() {
        System.out.println("\n7. BINARY SEARCH ON ANSWER");
        System.out.println("-".repeat(50));

        int[] testNumbers = {16, 25, 50, 100};
        for (int n : testNumbers) {
            int sqrt = integerSquareRoot(n);
            double preciseSqrt = squareRoot(n, 2);
            System.out.printf("√%3d = %d (integer), %.2f (precise)%n",
                            n, sqrt, preciseSqrt);
        }
    }

    private static void demonstrateAdvancedUtilities() {
        System.out.println("\n8. ADVANCED UTILITIES");
        System.out.println("-".repeat(50));

        Integer[] arr = {1, 3, 5, 6, 8, 10};
        int[] targets = {2, 5, 11};

        for (int target : targets) {
            int pos = searchInsertPosition(arr, target);
            System.out.printf("Insert position for %2d: %d%n", target, pos);
        }

        int[] arrClosest = {1, 3, 5, 7, 9};
        int[] targetsClosest = {4, 6, 8};

        for (int target : targetsClosest) {
            int idx = findClosest(arrClosest, target);
            System.out.printf("Closest to %d: Index=%d, Value=%d%n",
                            target, idx, arrClosest[idx]);
        }

        int[] peakArr = {1, 3, 20, 4, 1, 0};
        int peak = findPeakElement(peakArr);
        System.out.printf("Peak element in %s: Index=%d, Value=%d%n",
                        Arrays.toString(peakArr), peak, peakArr[peak]);
    }

    private static void runPerformanceTests() {
        System.out.println("\n" + "=".repeat(70));
        System.out.println("PERFORMANCE BENCHMARKS");
        System.out.println("=".repeat(70));

        int[] sizes = {1000, 10000, 100000};
        Random random = new Random(42);

        for (int size : sizes) {
            System.out.printf("%nArray size: %,d%n", size);
            System.out.println("-".repeat(50));

            // Generate sorted array
            Integer[] arr = new Integer[size];
            for (int i = 0; i < size; i++) {
                arr[i] = i * 2;
            }

            int[] targets = new int[100];
            for (int i = 0; i < 100; i++) {
                targets[i] = random.nextInt(size) * 2;
            }

            // Binary Search (Iterative)
            long start = System.nanoTime();
            for (int target : targets) {
                binarySearchIterative(arr, target);
            }
            double timeBinaryIter = (System.nanoTime() - start) / 1_000_000.0;

            // Binary Search (Recursive)
            start = System.nanoTime();
            for (int target : targets) {
                binarySearchRecursive(arr, target);
            }
            double timeBinaryRec = (System.nanoTime() - start) / 1_000_000.0;

            // Exponential Search
            start = System.nanoTime();
            for (int target : targets) {
                exponentialSearch(arr, target);
            }
            double timeExponential = (System.nanoTime() - start) / 1_000_000.0;

            // Convert to int array for interpolation search
            int[] intArr = new int[size];
            for (int i = 0; i < size; i++) {
                intArr[i] = arr[i];
            }

            start = System.nanoTime();
            for (int target : targets) {
                interpolationSearch(intArr, target);
            }
            double timeInterpolation = (System.nanoTime() - start) / 1_000_000.0;

            // Ternary Search
            start = System.nanoTime();
            for (int target : targets) {
                ternarySearch(arr, target);
            }
            double timeTernary = (System.nanoTime() - start) / 1_000_000.0;

            System.out.printf("Binary (Iterative):    %8.3f ms%n", timeBinaryIter);
            System.out.printf("Binary (Recursive):    %8.3f ms%n", timeBinaryRec);
            System.out.printf("Exponential Search:    %8.3f ms%n", timeExponential);
            System.out.printf("Interpolation Search:  %8.3f ms%n", timeInterpolation);
            System.out.printf("Ternary Search:        %8.3f ms%n", timeTernary);
        }
    }
}
