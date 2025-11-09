<?php
// Insertion Sort Algorithm Implementation in PHP
//
// Time Complexity:
// - Best Case: O(n) - when array is already sorted
// - Average Case: O(n²)
// - Worst Case: O(n²) - when array is reverse sorted
// Space Complexity: O(1) for in-place, O(n) for functional approach
//
// Insertion Sort builds the final sorted array one item at a time.
//
// PHP features:
// - Type declarations (PHP 7+)
// - Static methods in classes
// - Array functions and functional programming
// - Callable comparators
// - Namespace organization

namespace AlgorithmsMultiverse\Sorting;

/**
 * Insertion Sort implementation with multiple variants
 */
class InsertionSort
{
    // MARK: - Basic Insertion Sort

    /**
     * Performs standard insertion sort.
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
     *
     * @param array $arr The array to sort
     * @return array The sorted array
     */
    public static function sort(array $arr): array
    {
        if (count($arr) <= 1) {
            return $arr;
        }

        $result = $arr;
        self::sortInPlace($result);
        return $result;
    }

    /**
     * Sorts the array in-place using insertion sort.
     *
     * Time Complexity: O(n²) average and worst case, O(n) best case
     * Space Complexity: O(1)
     *
     * @param array &$arr The array to sort (passed by reference)
     */
    public static function sortInPlace(array &$arr): void
    {
        $n = count($arr);

        for ($i = 1; $i < $n; $i++) {
            $key = $arr[$i];
            $j = $i - 1;

            // Move elements greater than key one position ahead
            while ($j >= 0 && $arr[$j] > $key) {
                $arr[$j + 1] = $arr[$j];
                $j--;
            }

            $arr[$j + 1] = $key;
        }
    }

    /**
     * Insertion sort with custom comparator.
     *
     * @param array $arr The array to sort
     * @param callable $comparator Comparison function
     * @return array The sorted array
     */
    public static function sortWithComparator(array $arr, callable $comparator): array
    {
        if (count($arr) <= 1) {
            return $arr;
        }

        $result = $arr;
        $n = count($result);

        for ($i = 1; $i < $n; $i++) {
            $key = $result[$i];
            $j = $i - 1;

            while ($j >= 0 && $comparator($key, $result[$j]) < 0) {
                $result[$j + 1] = $result[$j];
                $j--;
            }

            $result[$j + 1] = $key;
        }

        return $result;
    }

    // MARK: - Recursive Insertion Sort

    /**
     * Performs recursive insertion sort.
     *
     * Time Complexity: O(n²)
     * Space Complexity: O(n) for recursion stack
     *
     * @param array $arr The array to sort
     * @return array The sorted array
     */
    public static function sortRecursive(array $arr): array
    {
        if (count($arr) <= 1) {
            return $arr;
        }

        $result = $arr;
        self::sortRecursiveHelper($result, count($result));
        return $result;
    }

    /**
     * Helper function for recursive insertion sort.
     *
     * @param array &$arr The array to sort
     * @param int $n The number of elements to sort
     */
    private static function sortRecursiveHelper(array &$arr, int $n): void
    {
        // Base case
        if ($n <= 1) {
            return;
        }

        // Sort first n-1 elements
        self::sortRecursiveHelper($arr, $n - 1);

        // Insert last element at its correct position
        $key = $arr[$n - 1];
        $j = $n - 2;

        while ($j >= 0 && $arr[$j] > $key) {
            $arr[$j + 1] = $arr[$j];
            $j--;
        }

        $arr[$j + 1] = $key;
    }

    // MARK: - Binary Insertion Sort

    /**
     * Uses binary search to find insertion position.
     *
     * Time Complexity: O(n²) for moves, O(n log n) for comparisons
     * Space Complexity: O(n)
     *
     * @param array $arr The array to sort
     * @return array The sorted array
     */
    public static function binaryInsertionSort(array $arr): array
    {
        if (count($arr) <= 1) {
            return $arr;
        }

        $result = $arr;
        $n = count($result);

        for ($i = 1; $i < $n; $i++) {
            $key = $result[$i];

            // Find position using binary search
            $pos = self::binarySearchPosition($result, 0, $i - 1, $key);

            // Shift elements to make space
            for ($j = $i - 1; $j >= $pos; $j--) {
                $result[$j + 1] = $result[$j];
            }

            $result[$pos] = $key;
        }

        return $result;
    }

    /**
     * Binary search to find the correct insertion position.
     *
     * @param array $arr The array
     * @param int $left Left boundary
     * @param int $right Right boundary
     * @param mixed $key The key to insert
     * @return int The position to insert
     */
    private static function binarySearchPosition(array $arr, int $left, int $right, $key): int
    {
        if ($right <= $left) {
            return ($key > $arr[$left]) ? $left + 1 : $left;
        }

        $mid = intdiv($left + $right, 2);

        if ($key == $arr[$mid]) {
            return $mid + 1;
        }

        if ($key > $arr[$mid]) {
            return self::binarySearchPosition($arr, $mid + 1, $right, $key);
        }

        return self::binarySearchPosition($arr, $left, $mid - 1, $key);
    }

    // MARK: - Shell Sort

    /**
     * Performs shell sort (generalization of insertion sort).
     *
     * Time Complexity: Depends on gap sequence (O(n log²n) for good sequences)
     * Space Complexity: O(n)
     *
     * @param array $arr The array to sort
     * @return array The sorted array
     */
    public static function shellSort(array $arr): array
    {
        if (count($arr) <= 1) {
            return $arr;
        }

        $result = $arr;
        $n = count($result);

        // Start with a large gap, then reduce (Knuth's sequence)
        $gap = 1;
        while ($gap < intdiv($n, 3)) {
            $gap = 3 * $gap + 1;
        }

        // Perform gapped insertion sort
        while ($gap > 0) {
            for ($i = $gap; $i < $n; $i++) {
                $key = $result[$i];
                $j = $i;

                // Insertion sort with gap
                while ($j >= $gap && $result[$j - $gap] > $key) {
                    $result[$j] = $result[$j - $gap];
                    $j -= $gap;
                }

                $result[$j] = $key;
            }

            $gap = intdiv($gap, 3);
        }

        return $result;
    }

    // MARK: - Sort Statistics

    /**
     * Insertion sort with statistics tracking
     *
     * @param array $arr The array to sort
     * @param SortStatistics $stats Statistics object to track operations
     * @return array The sorted array
     */
    public static function sortWithStats(array $arr, SortStatistics $stats): array
    {
        $stats->reset();
        if (count($arr) <= 1) {
            return $arr;
        }

        $result = $arr;
        $n = count($result);

        for ($i = 1; $i < $n; $i++) {
            $key = $result[$i];
            $j = $i - 1;

            while ($j >= 0) {
                $stats->comparisons++;
                if ($result[$j] > $key) {
                    $result[$j + 1] = $result[$j];
                    $stats->swaps++;
                    $j--;
                } else {
                    break;
                }
            }

            $result[$j + 1] = $key;
        }

        return $result;
    }

    // MARK: - Visualization

    /**
     * Creates a step-by-step visualization of insertion sort
     *
     * @param array $arr The array to visualize
     * @return array Array of strings showing each step
     */
    public static function visualizeInsertionSort(array $arr): array
    {
        $steps = [];
        $result = $arr;

        $steps[] = "Initial: [" . implode(", ", $result) . "]";

        $n = count($result);
        for ($i = 1; $i < $n; $i++) {
            $key = $result[$i];
            $j = $i - 1;

            $steps[] = "\nStep $i: Inserting $key";
            $steps[] = "  Before: [" . implode(", ", $result) . "]";

            while ($j >= 0 && $result[$j] > $key) {
                $result[$j + 1] = $result[$j];
                $j--;
            }

            $result[$j + 1] = $key;
            $steps[] = "  After:  [" . implode(", ", $result) . "]";
        }

        $steps[] = "\nFinal: [" . implode(", ", $result) . "]";
        return $steps;
    }

    // MARK: - Stability Demonstration

    /**
     * Demonstrates that insertion sort is stable
     */
    public static function demonstrateStability(): void
    {
        $data = [
            ['value' => 3, 'originalIndex' => 0],
            ['value' => 1, 'originalIndex' => 1],
            ['value' => 3, 'originalIndex' => 2],
            ['value' => 2, 'originalIndex' => 3],
            ['value' => 3, 'originalIndex' => 4],
        ];

        // Sort by value only
        $sorted = self::sortWithComparator($data, function($a, $b) {
            return $a['value'] <=> $b['value'];
        });

        echo "Stability Demonstration:\n";
        echo "Original: ";
        foreach ($data as $p) {
            echo "({$p['value']},{$p['originalIndex']}) ";
        }
        echo "\n";

        echo "Sorted:   ";
        foreach ($sorted as $p) {
            echo "({$p['value']},{$p['originalIndex']}) ";
        }
        echo "\n";

        // Check stability - all 3's should maintain original order
        $threeIndices = array_map(
            fn($p) => $p['originalIndex'],
            array_filter($sorted, fn($p) => $p['value'] === 3)
        );
        $isStable = $threeIndices == [0, 2, 4];
        echo "Stable: " . ($isStable ? "true" : "false") .
             " (indices of 3's: [" . implode(", ", $threeIndices) . "])\n";
    }

    // MARK: - Helper Functions

    /**
     * Check if an array is sorted in ascending order
     *
     * @param array $arr The array to check
     * @return bool True if sorted, false otherwise
     */
    public static function isSorted(array $arr): bool
    {
        $n = count($arr);
        for ($i = 0; $i < $n - 1; $i++) {
            if ($arr[$i] > $arr[$i + 1]) {
                return false;
            }
        }
        return true;
    }
}

/**
 * Tracks sorting operations
 */
class SortStatistics
{
    public int $comparisons = 0;
    public int $swaps = 0;

    public function reset(): void
    {
        $this->comparisons = 0;
        $this->swaps = 0;
    }

    public function __toString(): string
    {
        return "Comparisons: {$this->comparisons}, Swaps: {$this->swaps}";
    }
}

// MARK: - Demonstration and Testing

function demonstrateInsertionSort(): void
{
    echo "📝 Insertion Sort Implementation in PHP\n";
    echo str_repeat("=", 60) . "\n";

    // Test data
    $testCases = [
        ['arr' => [64, 34, 25, 12, 22, 11, 90], 'desc' => 'Random array'],
        ['arr' => [5, 2, 8, 6, 1, 9, 4], 'desc' => 'Small random array'],
        ['arr' => [1], 'desc' => 'Single element'],
        ['arr' => [], 'desc' => 'Empty array'],
        ['arr' => [3, 3, 3, 3, 3], 'desc' => 'All duplicates'],
        ['arr' => [9, 8, 7, 6, 5, 4, 3, 2, 1], 'desc' => 'Reverse sorted'],
        ['arr' => [1, 2, 3, 4, 5], 'desc' => 'Already sorted'],
        ['arr' => [1, 3, 2, 4, 5], 'desc' => 'Nearly sorted'],
    ];

    echo "\n📋 Basic Sorting Tests:\n";
    echo str_repeat("-", 60) . "\n";

    foreach ($testCases as $tc) {
        $standardResult = InsertionSort::sort($tc['arr']);
        $binaryResult = InsertionSort::binaryInsertionSort($tc['arr']);
        $shellResult = InsertionSort::shellSort($tc['arr']);
        $recursiveResult = InsertionSort::sortRecursive($tc['arr']);

        echo "\nTest: {$tc['desc']}\n";
        echo "Original: [" . implode(", ", $tc['arr']) . "]\n";
        echo "Sorted:   [" . implode(", ", $standardResult) . "]\n";

        $allCorrect = InsertionSort::isSorted($standardResult) &&
                     InsertionSort::isSorted($binaryResult) &&
                     InsertionSort::isSorted($shellResult) &&
                     InsertionSort::isSorted($recursiveResult);
        $allEqual = ($standardResult == $binaryResult) &&
                   ($standardResult == $shellResult) &&
                   ($standardResult == $recursiveResult);

        $status = ($allCorrect && $allEqual) ? "✓" : "✗";
        echo "All implementations match: $status\n";
    }

    // Visualization demo
    echo "\n\n🎬 Step-by-Step Visualization:\n";
    echo str_repeat("-", 60) . "\n";

    $demoArr = [5, 2, 8, 6, 1];
    $steps = InsertionSort::visualizeInsertionSort($demoArr);
    foreach ($steps as $step) {
        echo "$step\n";
    }

    // Stability demonstration
    echo "\n\n🔒 Stability Demonstration:\n";
    echo str_repeat("-", 60) . "\n";
    InsertionSort::demonstrateStability();

    // Performance analysis
    echo "\n\n📊 Operation Counting:\n";
    echo str_repeat("-", 60) . "\n";

    $statTestCases = [
        ['arr' => [5, 2, 8, 6, 1], 'desc' => 'Random'],
        ['arr' => [1, 2, 3, 4, 5], 'desc' => 'Already sorted'],
        ['arr' => [5, 4, 3, 2, 1], 'desc' => 'Reverse sorted'],
    ];

    foreach ($statTestCases as $tc) {
        $stats = new SortStatistics();
        InsertionSort::sortWithStats($tc['arr'], $stats);

        $n = count($tc['arr']);
        echo "\n{$tc['desc']}: [" . implode(", ", $tc['arr']) . "]\n";
        echo "Array size (n): $n\n";
        echo "Comparisons: {$stats->comparisons}\n";
        echo "Swaps: {$stats->swaps}\n";
        echo "Best case comparisons: " . ($n - 1) . "\n";
        echo "Worst case comparisons: " . ($n * ($n - 1) / 2) . "\n";
    }
}

// MARK: - Performance Benchmark

function performanceBenchmark(): void
{
    echo "\n\n⚡ Performance Benchmark\n";
    echo str_repeat("=", 80) . "\n";
    echo "\nInsertion sort is preferred for:\n";
    echo "  • Small arrays (typically n < 10-20)\n";
    echo "  • Nearly sorted arrays\n";
    echo "  • As part of hybrid sorting algorithms\n";
    echo "\n";

    $sizes = [5, 10, 20, 50, 100, 500, 1000];

    $patterns = [
        'Random' => function($n) {
            $arr = [];
            for ($i = 0; $i < $n; $i++) {
                $arr[] = rand(1, 1000);
            }
            return $arr;
        },
        'Nearly Sorted' => function($n) {
            $arr = range(0, $n - 1);
            for ($i = 0; $i < min(5, intdiv($n, 10)); $i++) {
                $idx1 = rand(0, $n - 1);
                $idx2 = rand(0, $n - 1);
                $temp = $arr[$idx1];
                $arr[$idx1] = $arr[$idx2];
                $arr[$idx2] = $temp;
            }
            return $arr;
        },
        'Reversed' => function($n) {
            return range($n - 1, 0);
        },
    ];

    foreach ($patterns as $patternName => $patternGen) {
        echo "\n$patternName Data:\n";
        printf("%-8s%15s%15s%15s%15s\n", "Size", "Insertion", "Binary", "Shell", "sort()");
        echo str_repeat("-", 68) . "\n";

        foreach ($sizes as $size) {
            $testData = $patternGen($size);
            printf("%-8d", $size);

            // Insertion Sort
            $start = microtime(true);
            InsertionSort::sort($testData);
            $elapsed = (microtime(true) - $start) * 1000;
            printf("%14.3fms", $elapsed);

            // Binary Insertion Sort
            $start = microtime(true);
            InsertionSort::binaryInsertionSort($testData);
            $elapsed = (microtime(true) - $start) * 1000;
            printf("%14.3fms", $elapsed);

            // Shell Sort
            $start = microtime(true);
            InsertionSort::shellSort($testData);
            $elapsed = (microtime(true) - $start) * 1000;
            printf("%14.3fms", $elapsed);

            // PHP sort()
            $testData2 = $testData;
            $start = microtime(true);
            sort($testData2);
            $elapsed = (microtime(true) - $start) * 1000;
            printf("%14.3fms\n", $elapsed);
        }
    }
}

// MARK: - Main

if (php_sapi_name() === 'cli') {
    demonstrateInsertionSort();
    performanceBenchmark();

    echo "\n✨ Insertion Sort demonstration complete!\n";
}
