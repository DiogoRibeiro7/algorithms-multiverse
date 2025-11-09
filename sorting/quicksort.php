<?php
/**
 * QuickSort Algorithm Implementation in PHP
 * 
 * Time Complexity:
 * - Best Case: O(n log n)
 * - Average Case: O(n log n)
 * - Worst Case: O(n²)
 * 
 * Space Complexity: O(log n) due to recursion stack
 * 
 * PHP features:
 * - Object-oriented design
 * - Type declarations
 * - Anonymous functions
 * - Array functions
 */

class QuickSort 
{
    /**
     * Sort array using QuickSort algorithm (returns new array)
     */
    public static function sort(array $array): array 
    {
        $result = $array;
        self::sortInPlace($result, 0, count($result) - 1);
        return $result;
    }
    
    /**
     * Sort array in-place using QuickSort algorithm
     */
    public static function sortInPlace(array &$array, int $low = null, int $high = null): void 
    {
        if ($low === null) $low = 0;
        if ($high === null) $high = count($array) - 1;
        
        if ($low < $high) {
            $pivotIndex = self::partition($array, $low, $high);
            self::sortInPlace($array, $low, $pivotIndex - 1);
            self::sortInPlace($array, $pivotIndex + 1, $high);
        }
    }
    
    /**
     * Partition the array around a pivot element
     */
    private static function partition(array &$array, int $low, int $high): int 
    {
        $pivot = $array[$high];
        $i = $low - 1;
        
        for ($j = $low; $j < $high; $j++) {
            if ($array[$j] <= $pivot) {
                $i++;
                self::swap($array, $i, $j);
            }
        }
        
        self::swap($array, $i + 1, $high);
        return $i + 1;
    }
    
    /**
     * Swap two elements in the array
     */
    private static function swap(array &$array, int $i, int $j): void 
    {
        if ($i !== $j) {
            $temp = $array[$i];
            $array[$i] = $array[$j];
            $array[$j] = $temp;
        }
    }
    
    /**
     * Iterative implementation to avoid stack overflow
     */
    public static function sortIterative(array &$array): void 
    {
        $size = count($array);
        if ($size <= 1) return;
        
        $stack = [];
        array_push($stack, [$low = 0, $high = $size - 1]);
        
        while (!empty($stack)) {
            [$low, $high] = array_pop($stack);
            
            if ($low < $high) {
                $pivotIndex = self::partition($array, $low, $high);
                array_push($stack, [$low, $pivotIndex - 1]);
                array_push($stack, [$pivotIndex + 1, $high]);
            }
        }
    }
    
    /**
     * Randomized QuickSort for better average performance
     */
    public static function sortRandomized(array &$array, int $low = null, int $high = null): void 
    {
        if ($low === null) $low = 0;
        if ($high === null) $high = count($array) - 1;
        
        if ($low < $high) {
            // Random pivot selection
            $randomIndex = rand($low, $high);
            self::swap($array, $randomIndex, $high);
            
            $pivotIndex = self::partition($array, $low, $high);
            self::sortRandomized($array, $low, $pivotIndex - 1);
            self::sortRandomized($array, $pivotIndex + 1, $high);
        }
    }
    
    /**
     * Three-way partitioning for arrays with many duplicates
     */
    public static function sort3Way(array &$array, int $low = null, int $high = null): void 
    {
        if ($low === null) $low = 0;
        if ($high === null) $high = count($array) - 1;
        
        if ($low >= $high) return;
        
        $pivot = $array[$low];
        $lt = $low;
        $gt = $high;
        $i = $low;
        
        while ($i <= $gt) {
            if ($array[$i] < $pivot) {
                self::swap($array, $lt, $i);
                $lt++;
                $i++;
            } elseif ($array[$i] > $pivot) {
                self::swap($array, $i, $gt);
                $gt--;
            } else {
                $i++;
            }
        }
        
        self::sort3Way($array, $low, $lt - 1);
        self::sort3Way($array, $gt + 1, $high);
    }
    
    /**
     * Functional-style QuickSort implementation
     */
    public static function sortFunctional(array $array): array 
    {
        if (count($array) <= 1) {
            return $array;
        }
        
        $pivot = $array[array_rand($array)];
        
        $less = array_filter($array, fn($x) => $x < $pivot);
        $equal = array_filter($array, fn($x) => $x == $pivot);
        $greater = array_filter($array, fn($x) => $x > $pivot);
        
        return array_merge(
            self::sortFunctional($less),
            array_values($equal),
            self::sortFunctional($greater)
        );
    }
    
    /**
     * Sort with custom comparison function
     */
    public static function sortWithComparator(array $array, callable $comparator): array 
    {
        $result = $array;
        self::sortWithComparatorInPlace($result, 0, count($result) - 1, $comparator);
        return $result;
    }
    
    private static function sortWithComparatorInPlace(array &$array, int $low, int $high, callable $comparator): void 
    {
        if ($low < $high) {
            $pivotIndex = self::partitionWithComparator($array, $low, $high, $comparator);
            self::sortWithComparatorInPlace($array, $low, $pivotIndex - 1, $comparator);
            self::sortWithComparatorInPlace($array, $pivotIndex + 1, $high, $comparator);
        }
    }
    
    private static function partitionWithComparator(array &$array, int $low, int $high, callable $comparator): int 
    {
        $pivot = $array[$high];
        $i = $low - 1;
        
        for ($j = $low; $j < $high; $j++) {
            if ($comparator($array[$j], $pivot) <= 0) {
                $i++;
                self::swap($array, $i, $j);
            }
        }
        
        self::swap($array, $i + 1, $high);
        return $i + 1;
    }
}

/**
 * Utility class for QuickSort operations
 */
class QuickSortUtils 
{
    /**
     * Check if array is sorted
     */
    public static function isSorted(array $array): bool 
    {
        $count = count($array);
        for ($i = 0; $i < $count - 1; $i++) {
            if ($array[$i] > $array[$i + 1]) {
                return false;
            }
        }
        return true;
    }
    
    /**
     * Generate random array for testing
     */
    public static function generateRandomArray(int $size, int $min = 1, int $max = 1000): array 
    {
        $array = [];
        for ($i = 0; $i < $size; $i++) {
            $array[] = rand($min, $max);
        }
        return $array;
    }
    
    /**
     * Benchmark sorting performance
     */
    public static function benchmark(array $array, string $method = 'sort'): float 
    {
        $testArray = $array;
        $startTime = microtime(true);
        
        switch ($method) {
            case 'sort':
                QuickSort::sort($testArray);
                break;
            case 'iterative':
                QuickSort::sortIterative($testArray);
                break;
            case 'randomized':
                QuickSort::sortRandomized($testArray);
                break;
            case 'functional':
                QuickSort::sortFunctional($testArray);
                break;
            case '3way':
                QuickSort::sort3Way($testArray);
                break;
            default:
                throw new InvalidArgumentException("Unknown method: $method");
        }
        
        return (microtime(true) - $startTime) * 1000; // Return milliseconds
    }
    
    /**
     * Pretty print array
     */
    public static function printArray(array $array, string $label = ''): void 
    {
        if ($label) {
            echo "$label: ";
        }
        echo '[' . implode(', ', $array) . ']' . PHP_EOL;
    }
}

/**
 * Array extension trait (simulating extension methods)
 */
trait QuickSortArrayExtensions 
{
    public function quickSort(): array 
    {
        return QuickSort::sort($this);
    }
    
    public function quickSortInPlace(): void 
    {
        QuickSort::sortInPlace($this);
    }
    
    public function isSorted(): bool 
    {
        return QuickSortUtils::isSorted($this);
    }
}

/**
 * Enhanced array class with QuickSort methods
 */
class SortableArray extends ArrayObject 
{
    use QuickSortArrayExtensions;
    
    public function quickSort(): SortableArray 
    {
        $sorted = QuickSort::sort($this->getArrayCopy());
        return new self($sorted);
    }
    
    public function quickSortInPlace(): self 
    {
        $array = $this->getArrayCopy();
        QuickSort::sortInPlace($array);
        $this->exchangeArray($array);
        return $this;
    }
}

/**
 * Demonstration and testing function
 */
function demonstrateQuickSort(): void 
{
    echo "🚀 PHP QuickSort Implementation" . PHP_EOL;
    echo str_repeat('=', 40) . PHP_EOL;
    
    // Test arrays
    $testArrays = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 6, 1, 9, 4],
        [1],
        [],
        [3, 3, 3, 3, 3],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
    ];
    
    echo PHP_EOL . "📋 Basic Sorting Tests:" . PHP_EOL;
    echo str_repeat('-', 30) . PHP_EOL;
    
    foreach ($testArrays as $index => $array) {
        $original = $array;
        $sorted = QuickSort::sort($array);
        $isCorrect = QuickSortUtils::isSorted($sorted);
        
        echo "Test " . ($index + 1) . ":" . PHP_EOL;
        QuickSortUtils::printArray($original, "Original");
        QuickSortUtils::printArray($sorted, "Sorted  ");
        echo "Correct: " . ($isCorrect ? "✓" : "✗") . PHP_EOL;
        echo str_repeat("-", 25) . PHP_EOL;
    }
    
    // Advanced features demonstration
    echo PHP_EOL . "🎯 Advanced Features:" . PHP_EOL;
    echo str_repeat('-', 25) . PHP_EOL;
    
    // Custom comparator (reverse order)
    $numbers = [64, 34, 25, 12, 22, 11, 90];
    $reverseSorted = QuickSort::sortWithComparator(
        $numbers, 
        fn($a, $b) => $b <=> $a
    );
    
    QuickSortUtils::printArray($numbers, "Original");
    QuickSortUtils::printArray($reverseSorted, "Reverse ");
    
    // Functional approach
    $functionalSorted = QuickSort::sortFunctional($numbers);
    QuickSortUtils::printArray($functionalSorted, "Functional");
    
    // Using enhanced array class
    $sortableArray = new SortableArray([9, 3, 7, 1, 5]);
    echo PHP_EOL . "Enhanced Array Class:" . PHP_EOL;
    QuickSortUtils::printArray($sortableArray->getArrayCopy(), "Original");
    $sortableArray->quickSortInPlace();
    QuickSortUtils::printArray($sortableArray->getArrayCopy(), "Sorted  ");
    
    // String sorting
    $words = ['banana', 'apple', 'cherry', 'date'];
    $sortedWords = QuickSort::sort($words);
    QuickSortUtils::printArray($words, "Words Original");
    QuickSortUtils::printArray($sortedWords, "Words Sorted  ");
}

/**
 * Performance benchmarking function
 */
function performanceBenchmark(): void 
{
    echo PHP_EOL . "⚡ Performance Benchmark" . PHP_EOL;
    echo str_repeat('=', 30) . PHP_EOL;
    
    $sizes = [1000, 5000, 10000];
    
    foreach ($sizes as $size) {
        echo PHP_EOL . "Testing with $size elements:" . PHP_EOL;
        
        $testData = QuickSortUtils::generateRandomArray($size);
        $methods = ['sort', 'iterative', 'randomized', '3way', 'functional'];
        
        foreach ($methods as $method) {
            $time = QuickSortUtils::benchmark($testData, $method);
            printf("  %-12s: %8.2fms%s", 
                ucfirst($method), 
                $time, 
                PHP_EOL
            );
        }
    }
}

/**
 * Edge cases testing
 */
function testEdgeCases(): void 
{
    echo PHP_EOL . "🧩 Edge Cases Testing" . PHP_EOL;
    echo str_repeat('=', 25) . PHP_EOL;
    
    // Test edge cases
    $edgeCases = [
        'Empty array' => [],
        'Single element' => [42],
        'Two elements' => [2, 1],
        'Already sorted' => [1, 2, 3, 4, 5],
        'Reverse sorted' => [5, 4, 3, 2, 1],
        'All duplicates' => [5, 5, 5, 5, 5],
    ];
    
    foreach ($edgeCases as $name => $array) {
        $sorted = QuickSort::sort($array);
        $isCorrect = QuickSortUtils::isSorted($sorted);
        echo "$name: " . ($isCorrect ? "✓" : "✗") . PHP_EOL;
    }
}

// Main execution
if (php_sapi_name() === 'cli') {
    demonstrateQuickSort();
    performanceBenchmark();
    testEdgeCases();
    
    echo PHP_EOL . "✨ QuickSort demonstration complete!" . PHP_EOL;
}
?>
