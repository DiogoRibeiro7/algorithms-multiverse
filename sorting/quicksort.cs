/*
 * QuickSort Algorithm Implementation in C#
 * 
 * Time Complexity:
 * - Best Case: O(n log n)
 * - Average Case: O(n log n)
 * - Worst Case: O(n²)
 * 
 * Space Complexity: O(log n) due to recursion stack
 * 
 * C# features:
 * - Generic types and constraints
 * - Extension methods
 * - LINQ integration
 * - Performance optimizations
 */

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

namespace AlgorithmsMultiverse.Sorting
{
    /// <summary>
    /// QuickSort implementation with multiple variants and optimizations
    /// </summary>
    public static class QuickSort
    {
        /// <summary>
        /// Sorts an array using QuickSort algorithm (creates new array)
        /// </summary>
        public static T[] Sort<T>(T[] array) where T : IComparable<T>
        {
            if (array == null) throw new ArgumentNullException(nameof(array));
            
            var result = new T[array.Length];
            Array.Copy(array, result, array.Length);
            SortInPlace(result, 0, result.Length - 1);
            return result;
        }
        
        /// <summary>
        /// Sorts an array in-place using QuickSort algorithm
        /// </summary>
        public static void SortInPlace<T>(T[] array) where T : IComparable<T>
        {
            if (array == null) throw new ArgumentNullException(nameof(array));
            if (array.Length <= 1) return;
            
            SortInPlace(array, 0, array.Length - 1);
        }
        
        /// <summary>
        /// Internal recursive QuickSort implementation
        /// </summary>
        private static void SortInPlace<T>(T[] array, int low, int high) where T : IComparable<T>
        {
            if (low < high)
            {
                int pivotIndex = Partition(array, low, high);
                SortInPlace(array, low, pivotIndex - 1);
                SortInPlace(array, pivotIndex + 1, high);
            }
        }
        
        /// <summary>
        /// Partitions the array around a pivot element
        /// </summary>
        private static int Partition<T>(T[] array, int low, int high) where T : IComparable<T>
        {
            T pivot = array[high];
            int i = low - 1;
            
            for (int j = low; j < high; j++)
            {
                if (array[j].CompareTo(pivot) <= 0)
                {
                    i++;
                    Swap(array, i, j);
                }
            }
            
            Swap(array, i + 1, high);
            return i + 1;
        }
        
        /// <summary>
        /// Iterative implementation to avoid stack overflow on large arrays
        /// </summary>
        public static void SortIterative<T>(T[] array) where T : IComparable<T>
        {
            if (array == null) throw new ArgumentNullException(nameof(array));
            if (array.Length <= 1) return;
            
            var stack = new Stack<(int low, int high)>();
            stack.Push((0, array.Length - 1));
            
            while (stack.Count > 0)
            {
                var (low, high) = stack.Pop();
                
                if (low < high)
                {
                    int pivotIndex = Partition(array, low, high);
                    stack.Push((low, pivotIndex - 1));
                    stack.Push((pivotIndex + 1, high));
                }
            }
        }
        
        /// <summary>
        /// Randomized QuickSort for better average case performance
        /// </summary>
        public static void SortRandomized<T>(T[] array) where T : IComparable<T>
        {
            if (array == null) throw new ArgumentNullException(nameof(array));
            if (array.Length <= 1) return;
            
            var random = new Random();
            SortRandomizedHelper(array, 0, array.Length - 1, random);
        }
        
        private static void SortRandomizedHelper<T>(T[] array, int low, int high, Random random) 
            where T : IComparable<T>
        {
            if (low < high)
            {
                // Random pivot selection
                int randomIndex = random.Next(low, high + 1);
                Swap(array, randomIndex, high);
                
                int pivotIndex = Partition(array, low, high);
                SortRandomizedHelper(array, low, pivotIndex - 1, random);
                SortRandomizedHelper(array, pivotIndex + 1, high, random);
            }
        }
        
        /// <summary>
        /// Three-way partitioning QuickSort for arrays with many duplicates
        /// </summary>
        public static void Sort3Way<T>(T[] array) where T : IComparable<T>
        {
            if (array == null) throw new ArgumentNullException(nameof(array));
            if (array.Length <= 1) return;
            
            Sort3WayHelper(array, 0, array.Length - 1);
        }
        
        private static void Sort3WayHelper<T>(T[] array, int low, int high) where T : IComparable<T>
        {
            if (low >= high) return;
            
            T pivot = array[low];
            int lt = low, gt = high, i = low;
            
            while (i <= gt)
            {
                int cmp = array[i].CompareTo(pivot);
                if (cmp < 0) Swap(array, lt++, i++);
                else if (cmp > 0) Swap(array, i, gt--);
                else i++;
            }
            
            Sort3WayHelper(array, low, lt - 1);
            Sort3WayHelper(array, gt + 1, high);
        }
        
        /// <summary>
        /// QuickSort with custom comparer
        /// </summary>
        public static void Sort<T>(T[] array, IComparer<T> comparer)
        {
            if (array == null) throw new ArgumentNullException(nameof(array));
            if (comparer == null) throw new ArgumentNullException(nameof(comparer));
            if (array.Length <= 1) return;
            
            SortWithComparer(array, 0, array.Length - 1, comparer);
        }
        
        private static void SortWithComparer<T>(T[] array, int low, int high, IComparer<T> comparer)
        {
            if (low < high)
            {
                int pivotIndex = PartitionWithComparer(array, low, high, comparer);
                SortWithComparer(array, low, pivotIndex - 1, comparer);
                SortWithComparer(array, pivotIndex + 1, high, comparer);
            }
        }
        
        private static int PartitionWithComparer<T>(T[] array, int low, int high, IComparer<T> comparer)
        {
            T pivot = array[high];
            int i = low - 1;
            
            for (int j = low; j < high; j++)
            {
                if (comparer.Compare(array[j], pivot) <= 0)
                {
                    i++;
                    Swap(array, i, j);
                }
            }
            
            Swap(array, i + 1, high);
            return i + 1;
        }
        
        /// <summary>
        /// LINQ-style functional QuickSort
        /// </summary>
        public static IEnumerable<T> SortFunctional<T>(IEnumerable<T> source) where T : IComparable<T>
        {
            if (source == null) throw new ArgumentNullException(nameof(source));
            
            var array = source.ToArray();
            if (array.Length <= 1) return array;
            
            var pivot = array[array.Length / 2];
            var less = array.Where(x => x.CompareTo(pivot) < 0);
            var equal = array.Where(x => x.CompareTo(pivot) == 0);
            var greater = array.Where(x => x.CompareTo(pivot) > 0);
            
            return SortFunctional(less)
                .Concat(equal)
                .Concat(SortFunctional(greater));
        }
        
        /// <summary>
        /// Utility method to swap two elements in an array
        /// </summary>
        private static void Swap<T>(T[] array, int i, int j)
        {
            if (i != j)
            {
                T temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
        }
    }
    
    /// <summary>
    /// Extension methods for arrays and lists
    /// </summary>
    public static class QuickSortExtensions
    {
        /// <summary>
        /// Extension method to sort array using QuickSort
        /// </summary>
        public static T[] QuickSort<T>(this T[] array) where T : IComparable<T>
        {
            return QuickSort.Sort(array);
        }
        
        /// <summary>
        /// Extension method to sort array in-place using QuickSort
        /// </summary>
        public static void QuickSortInPlace<T>(this T[] array) where T : IComparable<T>
        {
            QuickSort.SortInPlace(array);
        }
        
        /// <summary>
        /// Extension method to sort list using QuickSort
        /// </summary>
        public static List<T> QuickSort<T>(this List<T> list) where T : IComparable<T>
        {
            var array = list.ToArray();
            QuickSort.SortInPlace(array);
            return array.ToList();
        }
        
        /// <summary>
        /// Check if array is sorted
        /// </summary>
        public static bool IsSorted<T>(this T[] array) where T : IComparable<T>
        {
            for (int i = 0; i < array.Length - 1; i++)
            {
                if (array[i].CompareTo(array[i + 1]) > 0)
                    return false;
            }
            return true;
        }
    }
    
    /// <summary>
    /// Performance testing and demonstration
    /// </summary>
    public class QuickSortDemo
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("🚀 C# QuickSort Implementation");
            Console.WriteLine(new string('=', 40));
            
            // Test various scenarios
            TestBasicSorting();
            TestAdvancedFeatures();
            PerformanceBenchmark();
            
            Console.WriteLine("\n✨ QuickSort demonstration complete!");
        }
        
        private static void TestBasicSorting()
        {
            Console.WriteLine("\n📋 Basic Sorting Tests");
            Console.WriteLine(new string('-', 30));
            
            var testArrays = new[]
            {
                new[] { 64, 34, 25, 12, 22, 11, 90 },
                new[] { 5, 2, 8, 6, 1, 9, 4 },
                new[] { 1 },
                new int[] { },
                new[] { 3, 3, 3, 3, 3 },
                new[] { 9, 8, 7, 6, 5, 4, 3, 2, 1 }
            };
            
            for (int i = 0; i < testArrays.Length; i++)
            {
                var original = testArrays[i];
                var sorted = QuickSort.Sort(original);
                
                Console.WriteLine($"\nTest {i + 1}:");
                Console.WriteLine($"Original: [{string.Join(", ", original)}]");
                Console.WriteLine($"Sorted:   [{string.Join(", ", sorted)}]");
                Console.WriteLine($"Correct:  {sorted.IsSorted()}");
            }
        }
        
        private static void TestAdvancedFeatures()
        {
            Console.WriteLine("\n🎯 Advanced Features");
            Console.WriteLine(new string('-', 25));
            
            // Test with strings
            var words = new[] { "banana", "apple", "cherry", "date", "elderberry" };
            Console.WriteLine($"\nOriginal words: [{string.Join(", ", words)}]");
            var sortedWords = QuickSort.Sort(words);
            Console.WriteLine($"Sorted words:   [{string.Join(", ", sortedWords)}]");
            
            // Test with custom comparer (reverse order)
            var numbers = new[] { 64, 34, 25, 12, 22, 11, 90 };
            var numbersCopy = new int[numbers.Length];
            Array.Copy(numbers, numbersCopy, numbers.Length);
            
            QuickSort.Sort(numbersCopy, Comparer<int>.Create((x, y) => y.CompareTo(x)));
            Console.WriteLine($"\nOriginal:     [{string.Join(", ", numbers)}]");
            Console.WriteLine($"Reverse sort: [{string.Join(", ", numbersCopy)}]");
            
            // Test LINQ functional approach
            var functionalResult = QuickSort.SortFunctional(numbers).ToArray();
            Console.WriteLine($"LINQ style:   [{string.Join(", ", functionalResult)}]");
            
            // Test extension methods
            var extArray = new[] { 9, 3, 7, 1, 5 };
            var extSorted = extArray.QuickSort();
            Console.WriteLine($"\nExtension method:");
            Console.WriteLine($"Original:  [{string.Join(", ", extArray)}]");
            Console.WriteLine($"Sorted:    [{string.Join(", ", extSorted)}]");
        }
        
        private static void PerformanceBenchmark()
        {
            Console.WriteLine("\n📊 Performance Benchmark");
            Console.WriteLine(new string('-', 30));
            
            var sizes = new[] { 1000, 10000, 100000 };
            var random = new Random(42); // Fixed seed for reproducible results
            
            foreach (int size in sizes)
            {
                Console.WriteLine($"\nTesting with {size:N0} elements:");
                
                // Generate random data
                var testData = Enumerable.Range(0, size)
                    .Select(_ => random.Next(1, 1000))
                    .ToArray();
                
                // Test different implementations
                BenchmarkImplementation("Standard", testData, (arr) => QuickSort.SortInPlace(arr));
                BenchmarkImplementation("Iterative", testData, (arr) => QuickSort.SortIterative(arr));
                BenchmarkImplementation("Randomized", testData, (arr) => QuickSort.SortRandomized(arr));
                BenchmarkImplementation("3-Way", testData, (arr) => QuickSort.Sort3Way(arr));
            }
        }
        
        private static void BenchmarkImplementation(string name, int[] originalData, Action<int[]> sortMethod)
        {
            var testData = new int[originalData.Length];
            Array.Copy(originalData, testData, originalData.Length);
            
            var stopwatch = Stopwatch.StartNew();
            sortMethod(testData);
            stopwatch.Stop();
            
            Console.WriteLine($"  {name,-12}: {stopwatch.ElapsedMilliseconds,6:N0} ms");
            
            // Verify correctness
            if (!testData.IsSorted())
            {
                Console.WriteLine($"    WARNING: {name} did not sort correctly!");
            }
        }
    }
    
    /// <summary>
    /// Custom comparer for demonstration
    /// </summary>
    public class CustomComparer<T> : IComparer<T> where T : IComparable<T>
    {
        private readonly Func<T, T, int> _compareFunction;
        
        public CustomComparer(Func<T, T, int> compareFunction)
        {
            _compareFunction = compareFunction ?? throw new ArgumentNullException(nameof(compareFunction));
        }
        
        public int Compare(T x, T y)
        {
            return _compareFunction(x, y);
        }
    }
}
