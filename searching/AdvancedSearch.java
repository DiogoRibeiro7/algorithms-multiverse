/**
 * Advanced Search Algorithms - Java Implementation
 * ================================================
 *
 * Comprehensive collection of advanced search algorithms including:
 * 1. Jump Search
 * 2. Fibonacci Search
 * 3. Interpolation Search
 * 4. Exponential Search
 * 5. Parallel Search
 * 6. Geometric Search (KD-Tree)
 * 7. Fuzzy Search (Levenshtein)
 *
 * Features:
 * - Generic implementations with Comparator support
 * - Cache-friendly algorithms
 * - Parallel implementations using Fork/Join
 * - Performance-optimized for JVM
 *
 * Compilation: javac AdvancedSearch.java
 * Usage: java AdvancedSearch
 */

import java.util.*;
import java.util.concurrent.*;
import java.util.function.*;
import java.util.stream.*;

public class AdvancedSearch {

    // =========================================================================
    // 1. JUMP SEARCH
    // =========================================================================

    /**
     * Jump Search - Block-based search algorithm
     *
     * Time: O(√n), Space: O(1)
     *
     * WHEN TO USE:
     * - Comparisons are expensive (complex objects)
     * - Sequential access patterns preferred
     * - Want fewer comparisons than binary search
     *
     * @param arr Sorted array
     * @param target Element to find
     * @return Index of target or -1
     */
    public static <T extends Comparable<T>> int jumpSearch(T[] arr, T target) {
        if (arr == null || arr.length == 0) return -1;

        int n = arr.length;
        int step = (int) Math.sqrt(n);  // Optimal step size
        int prev = 0;

        // Jump ahead to find block containing target
        while (prev < n && arr[Math.min(step, n) - 1].compareTo(target) < 0) {
            prev = step;
            step += (int) Math.sqrt(n);

            if (prev >= n) return -1;
        }

        // Linear search in the block
        while (prev < n && arr[prev].compareTo(target) < 0) {
            prev++;
            if (prev == Math.min(step, n)) return -1;
        }

        // Check if element found
        if (prev < n && arr[prev].compareTo(target) == 0) {
            return prev;
        }

        return -1;
    }

    // =========================================================================
    // 2. FIBONACCI SEARCH
    // =========================================================================

    /**
     * Fibonacci Search - Using Fibonacci numbers for division
     *
     * Time: O(log n), Space: O(1)
     *
     * ADVANTAGES:
     * - No division operations (only addition/subtraction)
     * - Good for systems where division is expensive
     * - Cache-friendly due to smaller jumps
     *
     * @param arr Sorted array
     * @param target Element to find
     * @return Index of target or -1
     */
    public static <T extends Comparable<T>> int fibonacciSearch(T[] arr, T target) {
        if (arr == null || arr.length == 0) return -1;

        int n = arr.length;

        // Initialize Fibonacci numbers
        int fibM2 = 0;  // (m-2)th Fibonacci number
        int fibM1 = 1;  // (m-1)th Fibonacci number
        int fibM = fibM2 + fibM1;  // mth Fibonacci number

        // Find smallest Fibonacci >= n
        while (fibM < n) {
            fibM2 = fibM1;
            fibM1 = fibM;
            fibM = fibM2 + fibM1;
        }

        int offset = -1;

        while (fibM > 1) {
            // Check if fibM2 is valid index
            int i = Math.min(offset + fibM2, n - 1);

            int cmp = arr[i].compareTo(target);

            if (cmp < 0) {
                // Move offset forward
                fibM = fibM1;
                fibM1 = fibM2;
                fibM2 = fibM - fibM1;
                offset = i;
            } else if (cmp > 0) {
                // Move Fibonacci numbers down
                fibM = fibM2;
                fibM1 = fibM1 - fibM2;
                fibM2 = fibM - fibM1;
            } else {
                return i;
            }
        }

        // Check last element
        if (fibM1 == 1 && offset + 1 < n && arr[offset + 1].compareTo(target) == 0) {
            return offset + 1;
        }

        return -1;
    }

    // =========================================================================
    // 3. INTERPOLATION SEARCH
    // =========================================================================

    /**
     * Interpolation Search - Value-based position estimation
     *
     * Time: O(log log n) average for uniform data, O(n) worst
     * Space: O(1)
     *
     * WHEN TO USE:
     * - Uniformly distributed numerical data
     * - Large sorted arrays
     * - Known data distribution
     *
     * @param arr Sorted integer array
     * @param target Element to find
     * @return Index of target or -1
     */
    public static int interpolationSearch(int[] arr, int target) {
        if (arr == null || arr.length == 0) return -1;

        int left = 0;
        int right = arr.length - 1;

        while (left <= right && target >= arr[left] && target <= arr[right]) {
            if (left == right) {
                return arr[left] == target ? left : -1;
            }

            // Interpolation formula
            int pos = left + ((target - arr[left]) * (right - left)) /
                             (arr[right] - arr[left]);

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

    // =========================================================================
    // 4. EXPONENTIAL SEARCH
    // =========================================================================

    /**
     * Exponential Search - Finds range then binary searches
     *
     * Time: O(log n), Space: O(1)
     *
     * WHEN TO USE:
     * - Unbounded/infinite arrays
     * - Target expected near beginning
     * - Unknown array size
     *
     * @param arr Sorted array
     * @param target Element to find
     * @return Index of target or -1
     */
    public static <T extends Comparable<T>> int exponentialSearch(T[] arr, T target) {
        if (arr == null || arr.length == 0) return -1;
        if (arr[0].compareTo(target) == 0) return 0;

        // Find range for binary search
        int i = 1;
        while (i < arr.length && arr[i].compareTo(target) <= 0) {
            i *= 2;
        }

        // Binary search in range [i/2, min(i, n-1)]
        return binarySearch(arr, target, i / 2, Math.min(i, arr.length - 1));
    }

    private static <T extends Comparable<T>> int binarySearch(
            T[] arr, T target, int left, int right) {
        while (left <= right) {
            int mid = left + (right - left) / 2;
            int cmp = arr[mid].compareTo(target);

            if (cmp == 0) return mid;
            else if (cmp < 0) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }

    // =========================================================================
    // 5. PARALLEL SEARCH
    // =========================================================================

    /**
     * Parallel Search using Fork/Join framework
     *
     * Time: O(n / cores) with parallelism
     * Space: O(cores)
     *
     * WHEN TO USE:
     * - Very large arrays (millions of elements)
     * - Multi-core CPUs available
     * - Can work on unsorted data
     *
     * @param arr Array to search (can be unsorted)
     * @param target Element to find
     * @return Index of target or -1
     */
    public static <T> int parallelSearch(T[] arr, T target) {
        if (arr == null || arr.length == 0) return -1;

        ForkJoinPool pool = ForkJoinPool.commonPool();
        return pool.invoke(new ParallelSearchTask<>(arr, target, 0, arr.length));
    }

    static class ParallelSearchTask<T> extends RecursiveTask<Integer> {
        private static final int THRESHOLD = 1000;
        private final T[] arr;
        private final T target;
        private final int start;
        private final int end;

        ParallelSearchTask(T[] arr, T target, int start, int end) {
            this.arr = arr;
            this.target = target;
            this.start = start;
            this.end = end;
        }

        @Override
        protected Integer compute() {
            int length = end - start;

            if (length <= THRESHOLD) {
                // Sequential search for small ranges
                for (int i = start; i < end; i++) {
                    if (Objects.equals(arr[i], target)) {
                        return i;
                    }
                }
                return -1;
            }

            // Split task
            int mid = start + length / 2;
            ParallelSearchTask<T> leftTask = new ParallelSearchTask<>(arr, target, start, mid);
            ParallelSearchTask<T> rightTask = new ParallelSearchTask<>(arr, target, mid, end);

            leftTask.fork();
            int rightResult = rightTask.compute();
            int leftResult = leftTask.join();

            // Return first found result
            if (leftResult != -1) return leftResult;
            return rightResult;
        }
    }

    // =========================================================================
    // 6. KD-TREE FOR GEOMETRIC SEARCH
    // =========================================================================

    /**
     * KD-Tree for multidimensional search
     *
     * Time:
     * - Build: O(n log n)
     * - Search: O(log n) average
     * - Nearest neighbor: O(log n) average
     *
     * WHEN TO USE:
     * - Nearest neighbor in multiple dimensions
     * - Range queries in 2D/3D space
     * - GIS applications
     * - Computer graphics
     */
    static class KDTree {
        private static class Node {
            double[] point;
            Node left, right;
            int axis;

            Node(double[] point, int axis) {
                this.point = point;
                this.axis = axis;
            }
        }

        private Node root;
        private int k;  // Number of dimensions

        public KDTree(double[][] points) {
            if (points.length == 0) return;
            this.k = points[0].length;
            this.root = build(points, 0);
        }

        private Node build(double[][] points, int depth) {
            if (points.length == 0) return null;

            int axis = depth % k;

            // Sort by current axis
            Arrays.sort(points, Comparator.comparingDouble(p -> p[axis]));
            int median = points.length / 2;

            Node node = new Node(points[median], axis);
            node.left = build(Arrays.copyOfRange(points, 0, median), depth + 1);
            node.right = build(Arrays.copyOfRange(points, median + 1, points.length), depth + 1);

            return node;
        }

        /**
         * Find nearest neighbor to query point
         */
        public NearestResult nearestNeighbor(double[] query) {
            if (root == null) return null;

            NearestResult best = new NearestResult(null, Double.MAX_VALUE);
            nearestSearch(root, query, best);
            return best;
        }

        private void nearestSearch(Node node, double[] query, NearestResult best) {
            if (node == null) return;

            double dist = distance(query, node.point);
            if (dist < best.distance) {
                best.point = node.point;
                best.distance = dist;
            }

            double diff = query[node.axis] - node.point[node.axis];
            Node near = diff < 0 ? node.left : node.right;
            Node far = diff < 0 ? node.right : node.left;

            nearestSearch(near, query, best);

            if (Math.abs(diff) < best.distance) {
                nearestSearch(far, query, best);
            }
        }

        private double distance(double[] p1, double[] p2) {
            double sum = 0;
            for (int i = 0; i < k; i++) {
                double diff = p1[i] - p2[i];
                sum += diff * diff;
            }
            return Math.sqrt(sum);
        }

        static class NearestResult {
            double[] point;
            double distance;

            NearestResult(double[] point, double distance) {
                this.point = point;
                this.distance = distance;
            }
        }
    }

    // =========================================================================
    // 7. FUZZY SEARCH (LEVENSHTEIN DISTANCE)
    // =========================================================================

    /**
     * Calculate Levenshtein (edit) distance between two strings
     *
     * Time: O(m * n), Space: O(min(m, n))
     */
    public static int levenshteinDistance(String s1, String s2) {
        if (s1.length() < s2.length()) {
            String temp = s1;
            s1 = s2;
            s2 = temp;
        }

        int m = s1.length();
        int n = s2.length();

        if (n == 0) return m;

        // Use two rows for space optimization
        int[] prevRow = new int[n + 1];
        int[] currRow = new int[n + 1];

        // Initialize first row
        for (int j = 0; j <= n; j++) {
            prevRow[j] = j;
        }

        for (int i = 1; i <= m; i++) {
            currRow[0] = i;

            for (int j = 1; j <= n; j++) {
                int cost = s1.charAt(i - 1) == s2.charAt(j - 1) ? 0 : 1;

                currRow[j] = Math.min(
                    Math.min(prevRow[j] + 1,      // Deletion
                            currRow[j - 1] + 1),  // Insertion
                    prevRow[j - 1] + cost         // Substitution
                );
            }

            // Swap rows
            int[] temp = prevRow;
            prevRow = currRow;
            currRow = temp;
        }

        return prevRow[n];
    }

    /**
     * Fuzzy search - Find approximate matches of pattern in text
     *
     * @param text Text to search in
     * @param pattern Pattern to find
     * @param maxDistance Maximum edit distance allowed
     * @return List of (start, end) positions
     */
    public static List<int[]> fuzzySearch(String text, String pattern, int maxDistance) {
        List<int[]> matches = new ArrayList<>();
        int textLen = text.length();
        int patternLen = pattern.length();

        for (int i = 0; i < textLen - patternLen + maxDistance + 1; i++) {
            for (int windowSize = Math.max(1, patternLen - maxDistance);
                 windowSize <= Math.min(textLen - i, patternLen + maxDistance);
                 windowSize++) {

                String window = text.substring(i, i + windowSize);
                int distance = levenshteinDistance(pattern, window);

                if (distance <= maxDistance) {
                    matches.add(new int[]{i, i + windowSize});
                    break;
                }
            }
        }

        return matches;
    }

    // =========================================================================
    // EXAMPLES AND TESTING
    // =========================================================================

    private static void printSeparator() {
        System.out.println("=".repeat(70));
    }

    private static void exampleJumpSearch() {
        printSeparator();
        System.out.println("EXAMPLE 1: Jump Search");
        printSeparator();

        Integer[] arr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
        System.out.println("Array: " + Arrays.toString(arr));
        System.out.println("Jump search for 11: index " + jumpSearch(arr, 11));
        System.out.println("Jump search for 20: index " + jumpSearch(arr, 20));
        System.out.println();
    }

    private static void exampleFibonacciSearch() {
        printSeparator();
        System.out.println("EXAMPLE 2: Fibonacci Search");
        printSeparator();

        Integer[] arr = {2, 3, 4, 10, 40, 50, 60, 70, 80, 90};
        System.out.println("Array: " + Arrays.toString(arr));
        System.out.println("Fibonacci search for 40: index " + fibonacciSearch(arr, 40));
        System.out.println("Fibonacci search for 100: index " + fibonacciSearch(arr, 100));
        System.out.println();
    }

    private static void exampleKDTree() {
        printSeparator();
        System.out.println("EXAMPLE 3: KD-Tree Geometric Search");
        printSeparator();

        double[][] points = {
            {2, 3}, {5, 4}, {9, 6}, {4, 7}, {8, 1}, {7, 2}
        };

        KDTree tree = new KDTree(points);
        double[] query = {6, 3};

        KDTree.NearestResult result = tree.nearestNeighbor(query);
        System.out.println("Query point: " + Arrays.toString(query));
        System.out.println("Nearest neighbor: " + Arrays.toString(result.point));
        System.out.printf("Distance: %.2f%n", result.distance);
        System.out.println();
    }

    private static void exampleFuzzySearch() {
        printSeparator();
        System.out.println("EXAMPLE 4: Fuzzy String Search");
        printSeparator();

        String text = "The quick brown fox jumps over the lazy dog";
        String pattern = "quik";

        System.out.println("Text: '" + text + "'");
        System.out.println("Pattern: '" + pattern + "' (max distance = 1)");

        List<int[]> matches = fuzzySearch(text, pattern, 1);
        System.out.println("Matches:");
        for (int[] match : matches) {
            System.out.printf("  [%d, %d]: '%s'%n",
                match[0], match[1], text.substring(match[0], match[1]));
        }
        System.out.println();
    }

    private static void exampleParallelSearch() {
        printSeparator();
        System.out.println("EXAMPLE 5: Parallel Search");
        printSeparator();

        // Create large array
        Integer[] arr = new Integer[10000];
        for (int i = 0; i < arr.length; i++) {
            arr[i] = i * 2;
        }

        int target = 5000;
        long start = System.nanoTime();
        int result = parallelSearch(arr, target);
        long time = (System.nanoTime() - start) / 1000;

        System.out.println("Array size: " + arr.length);
        System.out.println("Target: " + target);
        System.out.println("Found at index: " + result);
        System.out.printf("Time: %d microseconds%n", time);
        System.out.println();
    }

    public static void main(String[] args) {
        printSeparator();
        System.out.println("ADVANCED SEARCH ALGORITHMS - JAVA");
        printSeparator();
        System.out.println();

        exampleJumpSearch();
        exampleFibonacciSearch();
        exampleKDTree();
        exampleFuzzySearch();
        exampleParallelSearch();

        printSeparator();
        System.out.println("All examples completed!");
        printSeparator();
    }
}
