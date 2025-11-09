// Insertion Sort Algorithm Implementation in C#
//
// Time Complexity:
// - Best Case: O(n) - when array is already sorted
// - Average Case: O(n²)
// - Worst Case: O(n²) - when array is reverse sorted
// Space Complexity: O(1) for in-place, O(n) for functional approach
//
// Insertion Sort builds the final sorted array one item at a time.
//
// C# features:
// - Generic methods with IComparable<T> constraint
// - Extension methods on collections
// - LINQ for functional operations
// - Tuples for stability demonstration
// - Delegates and lambda expressions

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

namespace AlgorithmsMultiverse.Sorting
{
    public static class InsertionSort
    {
        // MARK: - Basic Insertion Sort

        /// <summary>
        /// Performs standard insertion sort.
        ///
        /// Time Complexity: O(n²) average and worst case, O(n) best case
        /// Space Complexity: O(n) for the new array
        ///
        /// Example visualization:
        ///   Initial: [5, 2, 8, 6, 1]
        ///   Step 1:  [2, 5, 8, 6, 1]  // Insert 2
        ///   Step 2:  [2, 5, 8, 6, 1]  // 8 already in place
        ///   Step 3:  [2, 5, 6, 8, 1]  // Insert 6
        ///   Step 4:  [1, 2, 5, 6, 8]  // Insert 1
        /// </summary>
        public static T[] Sort<T>(T[] arr) where T : IComparable<T>
        {
            if (arr.Length <= 1)
            {
                return (T[])arr.Clone();
            }

            T[] result = (T[])arr.Clone();
            SortInPlace(result);
            return result;
        }

        /// <summary>
        /// Sorts the array in-place using insertion sort.
        ///
        /// Time Complexity: O(n²) average and worst case, O(n) best case
        /// Space Complexity: O(1)
        /// </summary>
        public static void SortInPlace<T>(T[] arr) where T : IComparable<T>
        {
            for (int i = 1; i < arr.Length; i++)
            {
                T key = arr[i];
                int j = i - 1;

                // Move elements greater than key one position ahead
                while (j >= 0 && arr[j].CompareTo(key) > 0)
                {
                    arr[j + 1] = arr[j];
                    j--;
                }

                arr[j + 1] = key;
            }
        }

        /// <summary>
        /// Insertion sort with custom comparer.
        /// </summary>
        public static T[] Sort<T>(T[] arr, IComparer<T> comparer)
        {
            if (arr.Length <= 1)
            {
                return (T[])arr.Clone();
            }

            T[] result = (T[])arr.Clone();

            for (int i = 1; i < result.Length; i++)
            {
                T key = result[i];
                int j = i - 1;

                while (j >= 0 && comparer.Compare(key, result[j]) < 0)
                {
                    result[j + 1] = result[j];
                    j--;
                }

                result[j + 1] = key;
            }

            return result;
        }

        /// <summary>
        /// Insertion sort with custom comparison function.
        /// </summary>
        public static T[] Sort<T>(T[] arr, Comparison<T> comparison)
        {
            if (arr.Length <= 1)
            {
                return (T[])arr.Clone();
            }

            T[] result = (T[])arr.Clone();

            for (int i = 1; i < result.Length; i++)
            {
                T key = result[i];
                int j = i - 1;

                while (j >= 0 && comparison(key, result[j]) < 0)
                {
                    result[j + 1] = result[j];
                    j--;
                }

                result[j + 1] = key;
            }

            return result;
        }

        // MARK: - Recursive Insertion Sort

        /// <summary>
        /// Performs recursive insertion sort.
        ///
        /// Time Complexity: O(n²)
        /// Space Complexity: O(n) for recursion stack
        /// </summary>
        public static T[] SortRecursive<T>(T[] arr) where T : IComparable<T>
        {
            if (arr.Length <= 1)
            {
                return (T[])arr.Clone();
            }

            T[] result = (T[])arr.Clone();
            SortRecursiveHelper(result, result.Length);
            return result;
        }

        private static void SortRecursiveHelper<T>(T[] arr, int n) where T : IComparable<T>
        {
            // Base case
            if (n <= 1) return;

            // Sort first n-1 elements
            SortRecursiveHelper(arr, n - 1);

            // Insert last element at its correct position
            T key = arr[n - 1];
            int j = n - 2;

            while (j >= 0 && arr[j].CompareTo(key) > 0)
            {
                arr[j + 1] = arr[j];
                j--;
            }

            arr[j + 1] = key;
        }

        // MARK: - Binary Insertion Sort

        /// <summary>
        /// Uses binary search to find insertion position.
        ///
        /// Time Complexity: O(n²) for moves, O(n log n) for comparisons
        /// Space Complexity: O(n)
        /// </summary>
        public static T[] BinaryInsertionSort<T>(T[] arr) where T : IComparable<T>
        {
            if (arr.Length <= 1)
            {
                return (T[])arr.Clone();
            }

            T[] result = (T[])arr.Clone();

            for (int i = 1; i < result.Length; i++)
            {
                T key = result[i];

                // Find position using binary search
                int pos = BinarySearchPosition(result, 0, i - 1, key);

                // Shift elements to make space
                for (int j = i - 1; j >= pos; j--)
                {
                    result[j + 1] = result[j];
                }

                result[pos] = key;
            }

            return result;
        }

        private static int BinarySearchPosition<T>(T[] arr, int left, int right, T key)
            where T : IComparable<T>
        {
            if (right <= left)
            {
                return key.CompareTo(arr[left]) > 0 ? left + 1 : left;
            }

            int mid = (left + right) / 2;

            if (key.CompareTo(arr[mid]) == 0)
            {
                return mid + 1;
            }

            if (key.CompareTo(arr[mid]) > 0)
            {
                return BinarySearchPosition(arr, mid + 1, right, key);
            }

            return BinarySearchPosition(arr, left, mid - 1, key);
        }

        // MARK: - Shell Sort

        /// <summary>
        /// Performs shell sort (generalization of insertion sort).
        ///
        /// Time Complexity: Depends on gap sequence (O(n log²n) for good sequences)
        /// Space Complexity: O(n)
        /// </summary>
        public static T[] ShellSort<T>(T[] arr) where T : IComparable<T>
        {
            if (arr.Length <= 1)
            {
                return (T[])arr.Clone();
            }

            T[] result = (T[])arr.Clone();
            int n = result.Length;

            // Start with a large gap, then reduce (Knuth's sequence)
            int gap = 1;
            while (gap < n / 3)
            {
                gap = 3 * gap + 1;
            }

            // Perform gapped insertion sort
            while (gap > 0)
            {
                for (int i = gap; i < n; i++)
                {
                    T key = result[i];
                    int j = i;

                    // Insertion sort with gap
                    while (j >= gap && result[j - gap].CompareTo(key) > 0)
                    {
                        result[j] = result[j - gap];
                        j -= gap;
                    }

                    result[j] = key;
                }

                gap /= 3;
            }

            return result;
        }

        // MARK: - Sort Statistics

        /// <summary>
        /// Tracks sorting operations
        /// </summary>
        public class SortStatistics
        {
            public int Comparisons { get; set; }
            public int Swaps { get; set; }

            public void Reset()
            {
                Comparisons = 0;
                Swaps = 0;
            }

            public override string ToString()
            {
                return $"Comparisons: {Comparisons}, Swaps: {Swaps}";
            }
        }

        /// <summary>
        /// Insertion sort with statistics tracking
        /// </summary>
        public static T[] SortWithStats<T>(T[] arr, SortStatistics stats)
            where T : IComparable<T>
        {
            stats.Reset();
            if (arr.Length <= 1)
            {
                return (T[])arr.Clone();
            }

            T[] result = (T[])arr.Clone();

            for (int i = 1; i < result.Length; i++)
            {
                T key = result[i];
                int j = i - 1;

                while (j >= 0)
                {
                    stats.Comparisons++;
                    if (result[j].CompareTo(key) > 0)
                    {
                        result[j + 1] = result[j];
                        stats.Swaps++;
                        j--;
                    }
                    else
                    {
                        break;
                    }
                }

                result[j + 1] = key;
            }

            return result;
        }

        // MARK: - Visualization

        /// <summary>
        /// Creates a step-by-step visualization of insertion sort
        /// </summary>
        public static List<string> VisualizeInsertionSort(int[] arr)
        {
            var steps = new List<string>();
            var result = (int[])arr.Clone();

            steps.Add($"Initial: [{string.Join(", ", result)}]");

            for (int i = 1; i < result.Length; i++)
            {
                int key = result[i];
                int j = i - 1;

                steps.Add($"\nStep {i}: Inserting {key}");
                steps.Add($"  Before: [{string.Join(", ", result)}]");

                while (j >= 0 && result[j] > key)
                {
                    result[j + 1] = result[j];
                    j--;
                }

                result[j + 1] = key;
                steps.Add($"  After:  [{string.Join(", ", result)}]");
            }

            steps.Add($"\nFinal: [{string.Join(", ", result)}]");
            return steps;
        }

        // MARK: - Stability Demonstration

        /// <summary>
        /// Demonstrates that insertion sort is stable
        /// </summary>
        public static void DemonstrateStability()
        {
            var data = new List<(int value, int originalIndex)>
            {
                (3, 0),
                (1, 1),
                (3, 2),
                (2, 3),
                (3, 4)
            };

            // Sort by value only
            var sorted = Sort(data.ToArray(), (a, b) => a.value.CompareTo(b.value));

            Console.WriteLine("Stability Demonstration:");
            Console.Write("Original: ");
            foreach (var p in data)
            {
                Console.Write($"({p.value},{p.originalIndex}) ");
            }
            Console.WriteLine();

            Console.Write("Sorted:   ");
            foreach (var p in sorted)
            {
                Console.Write($"({p.value},{p.originalIndex}) ");
            }
            Console.WriteLine();

            // Check stability - all 3's should maintain original order
            var threeIndices = sorted.Where(p => p.value == 3).Select(p => p.originalIndex).ToList();
            bool isStable = threeIndices.SequenceEqual(new[] { 0, 2, 4 });
            Console.WriteLine($"Stable: {isStable} (indices of 3's: [{string.Join(", ", threeIndices)}])");
        }

        // MARK: - Extension Methods

        /// <summary>
        /// Extension method to check if an array is sorted
        /// </summary>
        public static bool IsSorted<T>(this T[] arr) where T : IComparable<T>
        {
            for (int i = 0; i < arr.Length - 1; i++)
            {
                if (arr[i].CompareTo(arr[i + 1]) > 0)
                {
                    return false;
                }
            }
            return true;
        }

        /// <summary>
        /// Extension method to sort an array using insertion sort
        /// </summary>
        public static T[] InsertionSorted<T>(this T[] arr) where T : IComparable<T>
        {
            return Sort(arr);
        }

        // MARK: - Demonstration and Testing

        public static void DemonstrateInsertionSort()
        {
            Console.WriteLine("📝 Insertion Sort Implementation in C#");
            Console.WriteLine(new string('=', 60));

            // Test data
            var testCases = new List<(int[] arr, string desc)>
            {
                (new[] {64, 34, 25, 12, 22, 11, 90}, "Random array"),
                (new[] {5, 2, 8, 6, 1, 9, 4}, "Small random array"),
                (new[] {1}, "Single element"),
                (Array.Empty<int>(), "Empty array"),
                (new[] {3, 3, 3, 3, 3}, "All duplicates"),
                (new[] {9, 8, 7, 6, 5, 4, 3, 2, 1}, "Reverse sorted"),
                (new[] {1, 2, 3, 4, 5}, "Already sorted"),
                (new[] {1, 3, 2, 4, 5}, "Nearly sorted")
            };

            Console.WriteLine("\n📋 Basic Sorting Tests:");
            Console.WriteLine(new string('-', 60));

            foreach (var tc in testCases)
            {
                var standardResult = Sort(tc.arr);
                var binaryResult = BinaryInsertionSort(tc.arr);
                var shellResult = ShellSort(tc.arr);
                var recursiveResult = SortRecursive(tc.arr);

                Console.WriteLine($"\nTest: {tc.desc}");
                Console.WriteLine($"Original: [{string.Join(", ", tc.arr)}]");
                Console.WriteLine($"Sorted:   [{string.Join(", ", standardResult)}]");

                bool allCorrect = standardResult.IsSorted() && binaryResult.IsSorted() &&
                                 shellResult.IsSorted() && recursiveResult.IsSorted();
                bool allEqual = standardResult.SequenceEqual(binaryResult) &&
                               standardResult.SequenceEqual(shellResult) &&
                               standardResult.SequenceEqual(recursiveResult);

                string status = (allCorrect && allEqual) ? "✓" : "✗";
                Console.WriteLine($"All implementations match: {status}");
            }

            // Visualization demo
            Console.WriteLine("\n\n🎬 Step-by-Step Visualization:");
            Console.WriteLine(new string('-', 60));

            var demoArr = new[] { 5, 2, 8, 6, 1 };
            var steps = VisualizeInsertionSort(demoArr);
            foreach (var step in steps)
            {
                Console.WriteLine(step);
            }

            // Stability demonstration
            Console.WriteLine("\n\n🔒 Stability Demonstration:");
            Console.WriteLine(new string('-', 60));
            DemonstrateStability();

            // Performance analysis
            Console.WriteLine("\n\n📊 Operation Counting:");
            Console.WriteLine(new string('-', 60));

            var statTestCases = new List<(int[] arr, string desc)>
            {
                (new[] {5, 2, 8, 6, 1}, "Random"),
                (new[] {1, 2, 3, 4, 5}, "Already sorted"),
                (new[] {5, 4, 3, 2, 1}, "Reverse sorted")
            };

            foreach (var tc in statTestCases)
            {
                var stats = new SortStatistics();
                SortWithStats(tc.arr, stats);

                int n = tc.arr.Length;
                Console.WriteLine($"\n{tc.desc}: [{string.Join(", ", tc.arr)}]");
                Console.WriteLine($"Array size (n): {n}");
                Console.WriteLine($"Comparisons: {stats.Comparisons}");
                Console.WriteLine($"Swaps: {stats.Swaps}");
                Console.WriteLine($"Best case comparisons: {n - 1}");
                Console.WriteLine($"Worst case comparisons: {n * (n - 1) / 2}");
            }
        }

        // MARK: - Performance Benchmark

        public static void PerformanceBenchmark()
        {
            Console.WriteLine("\n\n⚡ Performance Benchmark");
            Console.WriteLine(new string('=', 80));
            Console.WriteLine("\nInsertion sort is preferred for:");
            Console.WriteLine("  • Small arrays (typically n < 10-20)");
            Console.WriteLine("  • Nearly sorted arrays");
            Console.WriteLine("  • As part of hybrid sorting algorithms");
            Console.WriteLine();

            var sizes = new[] { 5, 10, 20, 50, 100, 500, 1000 };
            var random = new Random(42);

            var patterns = new Dictionary<string, Func<int, int[]>>
            {
                ["Random"] = n => Enumerable.Range(0, n).Select(_ => random.Next(1, 1001)).ToArray(),
                ["Nearly Sorted"] = n =>
                {
                    var arr = Enumerable.Range(0, n).ToArray();
                    for (int i = 0; i < Math.Min(5, n / 10); i++)
                    {
                        int idx1 = random.Next(n);
                        int idx2 = random.Next(n);
                        (arr[idx1], arr[idx2]) = (arr[idx2], arr[idx1]);
                    }
                    return arr;
                },
                ["Reversed"] = n => Enumerable.Range(0, n).Reverse().ToArray()
            };

            foreach (var pattern in patterns)
            {
                Console.WriteLine($"\n{pattern.Key} Data:");
                Console.WriteLine($"{"Size",-8}{"Insertion",15}{"Binary",15}{"Shell",15}{"Array.Sort",15}");
                Console.WriteLine(new string('-', 68));

                foreach (int size in sizes)
                {
                    var testData = pattern.Value(size);
                    Console.Write($"{size,-8}");

                    // Insertion Sort
                    var sw = Stopwatch.StartNew();
                    Sort(testData);
                    sw.Stop();
                    Console.Write($"{sw.Elapsed.TotalMilliseconds,14:F3}ms");

                    // Binary Insertion Sort
                    sw.Restart();
                    BinaryInsertionSort(testData);
                    sw.Stop();
                    Console.Write($"{sw.Elapsed.TotalMilliseconds,14:F3}ms");

                    // Shell Sort
                    sw.Restart();
                    ShellSort(testData);
                    sw.Stop();
                    Console.Write($"{sw.Elapsed.TotalMilliseconds,14:F3}ms");

                    // Array.Sort
                    var testData2 = (int[])testData.Clone();
                    sw.Restart();
                    Array.Sort(testData2);
                    sw.Stop();
                    Console.WriteLine($"{sw.Elapsed.TotalMilliseconds,14:F3}ms");
                }
            }
        }
    }

    // MARK: - Main Program

    public class Program
    {
        public static void Main(string[] args)
        {
            InsertionSort.DemonstrateInsertionSort();
            InsertionSort.PerformanceBenchmark();

            Console.WriteLine("\n✨ Insertion Sort demonstration complete!");
        }
    }
}
