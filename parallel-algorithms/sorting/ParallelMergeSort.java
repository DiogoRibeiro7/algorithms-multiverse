/*
 * Parallel Merge Sort Implementation in Java
 *
 * This implementation uses Java's ForkJoinPool framework for efficient parallel sorting.
 *
 * Features:
 * - ForkJoinPool work-stealing scheduler
 * - RecursiveTask for divide-and-conquer parallelism
 * - ExecutorService for alternative parallelism
 * - Thread-safe operations with AtomicLong
 * - Comprehensive performance metrics
 *
 * Time Complexity: O(n log n)
 * Space Complexity: O(n)
 *
 * To compile and run:
 *   javac ParallelMergeSort.java
 *   java ParallelMergeSort
 *
 * Author: Algorithms Multiverse
 */

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

/**
 * Result of a sorting operation with performance metrics
 */
class SortResult {
    int[] sortedArray;
    long timeTaken; // nanoseconds
    long comparisons;
    String method;
    int numThreads;

    public SortResult(int[] sortedArray, long timeTaken, long comparisons,
                      String method, int numThreads) {
        this.sortedArray = sortedArray;
        this.timeTaken = timeTaken;
        this.comparisons = comparisons;
        this.method = method;
        this.numThreads = numThreads;
    }

    public double getTimeInSeconds() {
        return timeTaken / 1_000_000_000.0;
    }
}

/**
 * RecursiveTask for ForkJoinPool-based parallel merge sort
 */
class MergeSortTask extends RecursiveTask<int[]> {
    private final int[] array;
    private final int threshold;
    private final AtomicLong comparisons;
    private final ParallelMergeSort sorter;

    public MergeSortTask(int[] array, int threshold, AtomicLong comparisons,
                        ParallelMergeSort sorter) {
        this.array = array;
        this.threshold = threshold;
        this.comparisons = comparisons;
        this.sorter = sorter;
    }

    @Override
    protected int[] compute() {
        // Base case: use sequential sort for small arrays
        if (array.length <= threshold) {
            return sorter.sequentialMergeSort(array, comparisons);
        }

        int mid = array.length / 2;
        int[] left = Arrays.copyOfRange(array, 0, mid);
        int[] right = Arrays.copyOfRange(array, mid, array.length);

        // Create subtasks
        MergeSortTask leftTask = new MergeSortTask(left, threshold, comparisons, sorter);
        MergeSortTask rightTask = new MergeSortTask(right, threshold, comparisons, sorter);

        // Fork both tasks
        leftTask.fork();
        rightTask.fork();

        // Wait for completion
        int[] leftResult = leftTask.join();
        int[] rightResult = rightTask.join();

        // Merge results
        return sorter.merge(leftResult, rightResult, comparisons, true);
    }
}

/**
 * Parallel Merge Sort implementation with multiple strategies
 */
public class ParallelMergeSort {
    private static final int SEQUENTIAL_THRESHOLD = 1000;
    private static final int PROCESS_THRESHOLD = 100000;

    private final int numThreads;
    private final ForkJoinPool forkJoinPool;

    public ParallelMergeSort(int numThreads) {
        this.numThreads = numThreads;
        this.forkJoinPool = new ForkJoinPool(numThreads);
    }

    /**
     * Merge two sorted arrays into one sorted array
     */
    public int[] merge(int[] left, int[] right, AtomicLong comparisons,
                      boolean countComparisons) {
        int[] result = new int[left.length + right.length];
        int i = 0, j = 0, k = 0;

        while (i < left.length && j < right.length) {
            if (countComparisons && comparisons != null) {
                comparisons.incrementAndGet();
            }

            if (left[i] <= right[j]) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }

        while (i < left.length) {
            result[k++] = left[i++];
        }

        while (j < right.length) {
            result[k++] = right[j++];
        }

        return result;
    }

    /**
     * Sequential merge sort for base cases
     */
    public int[] sequentialMergeSort(int[] array, AtomicLong comparisons) {
        if (array.length <= 1) {
            return array;
        }

        int mid = array.length / 2;
        int[] left = sequentialMergeSort(Arrays.copyOfRange(array, 0, mid), comparisons);
        int[] right = sequentialMergeSort(Arrays.copyOfRange(array, mid, array.length), comparisons);

        return merge(left, right, comparisons, true);
    }

    /**
     * Parallel merge sort using ForkJoinPool
     */
    public int[] parallelMergeSortForkJoin(int[] array) {
        AtomicLong comparisons = new AtomicLong(0);
        MergeSortTask task = new MergeSortTask(array, SEQUENTIAL_THRESHOLD, comparisons, this);
        return forkJoinPool.invoke(task);
    }

    /**
     * Parallel merge sort using ExecutorService
     */
    public int[] parallelMergeSortExecutor(int[] array) throws ExecutionException, InterruptedException {
        AtomicLong comparisons = new AtomicLong(0);

        if (array.length <= SEQUENTIAL_THRESHOLD) {
            return sequentialMergeSort(array, comparisons);
        }

        // Split into chunks
        int chunkSize = Math.max(array.length / numThreads, SEQUENTIAL_THRESHOLD);
        List<int[]> chunks = new ArrayList<>();

        for (int i = 0; i < array.length; i += chunkSize) {
            int end = Math.min(i + chunkSize, array.length);
            chunks.add(Arrays.copyOfRange(array, i, end));
        }

        // Sort chunks in parallel
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        List<Future<int[]>> futures = new ArrayList<>();

        for (int[] chunk : chunks) {
            futures.add(executor.submit(() -> sequentialMergeSort(chunk, comparisons)));
        }

        List<int[]> sortedChunks = new ArrayList<>();
        for (Future<int[]> future : futures) {
            sortedChunks.add(future.get());
        }

        executor.shutdown();

        // Merge sorted chunks
        while (sortedChunks.size() > 1) {
            List<int[]> merged = new ArrayList<>();
            for (int i = 0; i < sortedChunks.size(); i += 2) {
                if (i + 1 < sortedChunks.size()) {
                    merged.add(merge(sortedChunks.get(i), sortedChunks.get(i + 1),
                                   comparisons, false));
                } else {
                    merged.add(sortedChunks.get(i));
                }
            }
            sortedChunks = merged;
        }

        return sortedChunks.isEmpty() ? new int[0] : sortedChunks.get(0);
    }

    /**
     * Parallel merge sort using Java 8 Parallel Streams
     */
    public int[] parallelMergeSortStreams(int[] array) {
        if (array.length <= SEQUENTIAL_THRESHOLD) {
            AtomicLong comparisons = new AtomicLong(0);
            return sequentialMergeSort(array, comparisons);
        }

        // This is a simplified version using Arrays.parallelSort
        // For demonstration purposes
        int[] result = array.clone();
        Arrays.parallelSort(result);
        return result;
    }

    /**
     * Adaptive parallel merge sort
     */
    public int[] adaptiveParallelMergeSort(int[] array) throws ExecutionException, InterruptedException {
        int n = array.length;

        if (n <= SEQUENTIAL_THRESHOLD) {
            AtomicLong comparisons = new AtomicLong(0);
            return sequentialMergeSort(array, comparisons);
        } else if (n <= PROCESS_THRESHOLD) {
            return parallelMergeSortForkJoin(array);
        } else {
            return parallelMergeSortExecutor(array);
        }
    }

    /**
     * Sort with performance metrics
     */
    public SortResult sortWithMetrics(int[] array, String method) {
        AtomicLong comparisons = new AtomicLong(0);
        long startTime = System.nanoTime();

        int[] sorted;
        try {
            switch (method) {
                case "sequential":
                    sorted = sequentialMergeSort(array.clone(), comparisons);
                    break;
                case "forkjoin":
                    sorted = parallelMergeSortForkJoin(array.clone());
                    break;
                case "executor":
                    sorted = parallelMergeSortExecutor(array.clone());
                    break;
                case "streams":
                    sorted = parallelMergeSortStreams(array.clone());
                    break;
                case "adaptive":
                    sorted = adaptiveParallelMergeSort(array.clone());
                    break;
                default:
                    sorted = adaptiveParallelMergeSort(array.clone());
            }
        } catch (Exception e) {
            throw new RuntimeException("Error during sorting: " + e.getMessage(), e);
        }

        long timeTaken = System.nanoTime() - startTime;

        return new SortResult(sorted, timeTaken, comparisons.get(), method, numThreads);
    }

    /**
     * Check if array is sorted
     */
    public static boolean isSorted(int[] array) {
        for (int i = 1; i < array.length; i++) {
            if (array[i] < array[i - 1]) {
                return false;
            }
        }
        return true;
    }

    /**
     * Calculate speedup factor
     */
    public static double calculateSpeedup(long seqTime, long parallelTime) {
        return parallelTime == 0 ? 0 : (double) seqTime / parallelTime;
    }

    /**
     * Calculate parallel efficiency
     */
    public static double calculateEfficiency(double speedup, int numThreads) {
        return numThreads == 0 ? 0 : speedup / numThreads;
    }

    /**
     * Benchmark all methods
     */
    public static Map<String, SortResult> benchmarkAllMethods(int[] array, int numThreads) {
        Map<String, SortResult> results = new LinkedHashMap<>();
        String[] methods = {"sequential", "forkjoin", "executor", "adaptive"};

        ParallelMergeSort sorter = new ParallelMergeSort(numThreads);

        for (String method : methods) {
            try {
                results.put(method, sorter.sortWithMetrics(array, method));
            } catch (Exception e) {
                System.err.println("Error in " + method + ": " + e.getMessage());
            }
        }

        return results;
    }

    /**
     * Main demonstration
     */
    public static void main(String[] args) {
        System.out.println("=".repeat(80));
        System.out.println("PARALLEL MERGE SORT DEMONSTRATION (Java)");
        System.out.println("=".repeat(80));

        int numCores = Runtime.getRuntime().availableProcessors();
        System.out.println("Number of available processors: " + numCores);

        // Test with different sizes
        int[] sizes = {1000, 10000, 100000};

        for (int size : sizes) {
            System.out.println("\n" + "=".repeat(80));
            System.out.println(String.format("Testing with %,d elements", size));
            System.out.println("=".repeat(80));

            // Generate random array
            int[] array = new Random().ints(size, 0, 100000).toArray();

            // Benchmark all methods
            Map<String, SortResult> results = benchmarkAllMethods(array, numCores);

            // Display results
            System.out.println(String.format("\n%-15s %-15s %-20s %-10s",
                    "Method", "Time (s)", "Comparisons", "Verified"));
            System.out.println("-".repeat(80));

            long seqTime = results.containsKey("sequential") ?
                    results.get("sequential").timeTaken : 0;

            for (Map.Entry<String, SortResult> entry : results.entrySet()) {
                String method = entry.getKey();
                SortResult result = entry.getValue();

                String verified = isSorted(result.sortedArray) ? "✓" : "✗";

                System.out.println(String.format("%-15s %13.6f  %18,d  %-10s",
                        method, result.getTimeInSeconds(), result.comparisons, verified));

                if (!method.equals("sequential") && seqTime > 0) {
                    double speedup = calculateSpeedup(seqTime, result.timeTaken);
                    double efficiency = calculateEfficiency(speedup, result.numThreads);
                    System.out.println(String.format("%-15s Speedup: %.2fx  Efficiency: %.2f%%",
                            "", speedup, efficiency * 100));
                }
            }
        }

        System.out.println("\n" + "=".repeat(80));
        System.out.println("FORKJOIN POOL ANALYSIS");
        System.out.println("=".repeat(80));

        // Test scalability with different thread counts
        System.out.println("\nScalability test (50,000 elements):");
        int[] testArray = new Random().ints(50000, 0, 100000).toArray();

        System.out.println(String.format("\n%-10s %-15s %-10s", "Threads", "Time (s)", "Speedup"));
        System.out.println("-".repeat(40));

        long baselineTime = 0;
        for (int threads = 1; threads <= numCores; threads++) {
            ParallelMergeSort sorter = new ParallelMergeSort(threads);
            SortResult result = sorter.sortWithMetrics(testArray, "forkjoin");

            if (threads == 1) {
                baselineTime = result.timeTaken;
            }

            double speedup = calculateSpeedup(baselineTime, result.timeTaken);
            System.out.println(String.format("%-10d %13.6f  %.2fx",
                    threads, result.getTimeInSeconds(), speedup));
        }

        System.out.println("\n" + "=".repeat(80));
        System.out.println("WHEN TO USE PARALLEL MERGE SORT IN JAVA");
        System.out.println("=".repeat(80));
        System.out.println("""

Parallel merge sort with ForkJoinPool is beneficial when:

✓ Dataset size > 10,000 elements
✓ Multiple CPU cores available
✓ CPU-bound comparison operations
✓ Stable sorting required

Java-specific advantages:
✓ ForkJoinPool work-stealing scheduler
✓ RecursiveTask for divide-and-conquer
✓ Mature JVM optimizations
✓ Good tooling (JVisualVM, JFR)
✓ Platform-independent

Avoid parallel merge sort when:

✗ Small datasets (<1,000 elements)
✗ Single-core systems
✗ GC-sensitive applications
✗ Simple comparisons with low CPU cost

Strategy selection:
- Sequential: < 1,000 elements
- ForkJoin: 1,000 - 100,000 elements (best for recursive)
- Executor: > 100,000 elements (better chunking)
- Streams: Quick and easy (uses ForkJoin internally)
- Adaptive: Let the algorithm decide

Performance characteristics:
- Thread spawn: ~10-50μs overhead
- ForkJoin work stealing: Efficient load balancing
- Typical speedup: 3-3.5x on 4 cores
- Efficiency: 75-90% for optimal workload
- GC impact: Can affect performance

Best practices:
1. Use ForkJoinPool for recursive algorithms
2. Use ExecutorService for independent tasks
3. Configure pool size with parallelism parameter
4. Profile with JFR (Java Flight Recorder)
5. Warm up JVM for accurate benchmarks
6. Consider GC tuning for large datasets

ForkJoinPool features:
- Work-stealing scheduler (same as Go's)
- RecursiveTask/RecursiveAction abstractions
- Common pool for convenience
- Configurable parallelism level

Memory considerations:
- Heap allocations trigger GC
- Array copying overhead
- Consider using primitive arrays
- Monitor with JVisualVM

Comparison with other approaches:
- Arrays.parallelSort(): Built-in, uses ForkJoin
- Streams.parallel(): High-level, less control
- Custom ForkJoin: Full control, more code
- ExecutorService: Simple tasks, no recursion

JVM tuning:
- -XX:+UseParallelGC for throughput
- -XX:ParallelGCThreads=N for GC threads
- -XX:MaxGCPauseMillis=N for latency
- Xmx/Xms for heap size
        """);

        System.out.println("\nDemonstration complete!");
    }
}
