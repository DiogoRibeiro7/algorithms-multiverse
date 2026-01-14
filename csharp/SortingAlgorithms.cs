using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Diagnostics;

namespace AlgorithmsMultiverse.CSharp
{
    /// <summary>
    /// Comprehensive sorting algorithms implementation with LINQ optimizations
    /// </summary>
    public static class SortingAlgorithms
    {
        #region Quick Sort

        /// <summary>
        /// Quick Sort implementation with generic type support
        /// </summary>
        public static void QuickSort<T>(T[] array) where T : IComparable<T>
        {
            QuickSort(array, 0, array.Length - 1);
        }

        private static void QuickSort<T>(T[] array, int low, int high) where T : IComparable<T>
        {
            if (low < high)
            {
                int pivot = Partition(array, low, high);
                QuickSort(array, low, pivot - 1);
                QuickSort(array, pivot + 1, high);
            }
        }

        private static int Partition<T>(T[] array, int low, int high) where T : IComparable<T>
        {
            T pivot = array[high];
            int i = low - 1;

            for (int j = low; j < high; j++)
            {
                if (array[j].CompareTo(pivot) <= 0)
                {
                    i++;
                    (array[i], array[j]) = (array[j], array[i]);
                }
            }

            (array[i + 1], array[high]) = (array[high], array[i + 1]);
            return i + 1;
        }

        /// <summary>
        /// Parallel Quick Sort for better performance on large datasets
        /// </summary>
        public static void ParallelQuickSort<T>(T[] array) where T : IComparable<T>
        {
            ParallelQuickSort(array, 0, array.Length - 1, Environment.ProcessorCount);
        }

        private static void ParallelQuickSort<T>(T[] array, int low, int high, int depthRemaining) where T : IComparable<T>
        {
            if (low < high)
            {
                int pivot = Partition(array, low, high);

                if (depthRemaining > 0)
                {
                    Parallel.Invoke(
                        () => ParallelQuickSort(array, low, pivot - 1, depthRemaining - 1),
                        () => ParallelQuickSort(array, pivot + 1, high, depthRemaining - 1)
                    );
                }
                else
                {
                    QuickSort(array, low, pivot - 1);
                    QuickSort(array, pivot + 1, high);
                }
            }
        }

        #endregion

        #region Merge Sort

        /// <summary>
        /// Merge Sort implementation with stability guarantee
        /// </summary>
        public static void MergeSort<T>(T[] array) where T : IComparable<T>
        {
            MergeSort(array, 0, array.Length - 1);
        }

        private static void MergeSort<T>(T[] array, int left, int right) where T : IComparable<T>
        {
            if (left < right)
            {
                int mid = left + (right - left) / 2;
                MergeSort(array, left, mid);
                MergeSort(array, mid + 1, right);
                Merge(array, left, mid, right);
            }
        }

        private static void Merge<T>(T[] array, int left, int mid, int right) where T : IComparable<T>
        {
            T[] temp = new T[right - left + 1];
            int i = left, j = mid + 1, k = 0;

            while (i <= mid && j <= right)
            {
                if (array[i].CompareTo(array[j]) <= 0)
                    temp[k++] = array[i++];
                else
                    temp[k++] = array[j++];
            }

            while (i <= mid)
                temp[k++] = array[i++];

            while (j <= right)
                temp[k++] = array[j++];

            Array.Copy(temp, 0, array, left, temp.Length);
        }

        #endregion

        #region Heap Sort

        /// <summary>
        /// Heap Sort implementation with in-place sorting
        /// </summary>
        public static void HeapSort<T>(T[] array) where T : IComparable<T>
        {
            int n = array.Length;

            // Build max heap
            for (int i = n / 2 - 1; i >= 0; i--)
                Heapify(array, n, i);

            // Extract elements from heap
            for (int i = n - 1; i > 0; i--)
            {
                (array[0], array[i]) = (array[i], array[0]);
                Heapify(array, i, 0);
            }
        }

        private static void Heapify<T>(T[] array, int n, int i) where T : IComparable<T>
        {
            int largest = i;
            int left = 2 * i + 1;
            int right = 2 * i + 2;

            if (left < n && array[left].CompareTo(array[largest]) > 0)
                largest = left;

            if (right < n && array[right].CompareTo(array[largest]) > 0)
                largest = right;

            if (largest != i)
            {
                (array[i], array[largest]) = (array[largest], array[i]);
                Heapify(array, n, largest);
            }
        }

        #endregion

        #region LINQ-Optimized Sorting

        /// <summary>
        /// LINQ-based sorting with custom comparers
        /// </summary>
        public static IEnumerable<T> LinqSort<T>(IEnumerable<T> collection, IComparer<T> comparer = null)
        {
            return comparer == null
                ? collection.OrderBy(x => x)
                : collection.OrderBy(x => x, comparer);
        }

        /// <summary>
        /// LINQ-based stable sort with multiple keys
        /// </summary>
        public static IEnumerable<T> MultiKeySort<T, TKey1, TKey2>(
            IEnumerable<T> collection,
            Func<T, TKey1> keySelector1,
            Func<T, TKey2> keySelector2)
        {
            return collection
                .OrderBy(keySelector1)
                .ThenBy(keySelector2);
        }

        /// <summary>
        /// Parallel LINQ sorting for large datasets
        /// </summary>
        public static IEnumerable<T> ParallelLinqSort<T>(IEnumerable<T> collection) where T : IComparable<T>
        {
            return collection
                .AsParallel()
                .OrderBy(x => x)
                .AsSequential();
        }

        #endregion

        #region Counting Sort

        /// <summary>
        /// Counting Sort for integers with known range
        /// </summary>
        public static void CountingSort(int[] array, int maxValue)
        {
            int[] count = new int[maxValue + 1];
            int[] output = new int[array.Length];

            // Count occurrences
            foreach (int num in array)
                count[num]++;

            // Cumulative count
            for (int i = 1; i <= maxValue; i++)
                count[i] += count[i - 1];

            // Build output array
            for (int i = array.Length - 1; i >= 0; i--)
            {
                output[count[array[i]] - 1] = array[i];
                count[array[i]]--;
            }

            Array.Copy(output, array, array.Length);
        }

        #endregion

        #region Radix Sort

        /// <summary>
        /// Radix Sort for non-negative integers
        /// </summary>
        public static void RadixSort(int[] array)
        {
            if (array.Length == 0) return;

            int max = array.Max();
            for (int exp = 1; max / exp > 0; exp *= 10)
                CountingSortByDigit(array, exp);
        }

        private static void CountingSortByDigit(int[] array, int exp)
        {
            int n = array.Length;
            int[] output = new int[n];
            int[] count = new int[10];

            for (int i = 0; i < n; i++)
                count[(array[i] / exp) % 10]++;

            for (int i = 1; i < 10; i++)
                count[i] += count[i - 1];

            for (int i = n - 1; i >= 0; i--)
            {
                int digit = (array[i] / exp) % 10;
                output[count[digit] - 1] = array[i];
                count[digit]--;
            }

            Array.Copy(output, array, n);
        }

        #endregion

        #region Tim Sort (Hybrid)

        /// <summary>
        /// Tim Sort - Hybrid stable sorting algorithm
        /// </summary>
        public static void TimSort<T>(T[] array) where T : IComparable<T>
        {
            const int MIN_MERGE = 32;
            int n = array.Length;

            // Sort individual runs using insertion sort
            for (int i = 0; i < n; i += MIN_MERGE)
            {
                int end = Math.Min(i + MIN_MERGE - 1, n - 1);
                InsertionSort(array, i, end);
            }

            // Merge the sorted runs
            for (int size = MIN_MERGE; size < n; size *= 2)
            {
                for (int start = 0; start < n; start += size * 2)
                {
                    int mid = start + size - 1;
                    int end = Math.Min(start + size * 2 - 1, n - 1);

                    if (mid < end)
                        Merge(array, start, mid, end);
                }
            }
        }

        private static void InsertionSort<T>(T[] array, int left, int right) where T : IComparable<T>
        {
            for (int i = left + 1; i <= right; i++)
            {
                T key = array[i];
                int j = i - 1;

                while (j >= left && array[j].CompareTo(key) > 0)
                {
                    array[j + 1] = array[j];
                    j--;
                }

                array[j + 1] = key;
            }
        }

        #endregion

        #region Bucket Sort

        /// <summary>
        /// Bucket Sort for uniformly distributed data
        /// </summary>
        public static void BucketSort(double[] array)
        {
            if (array.Length <= 1) return;

            int n = array.Length;
            List<double>[] buckets = new List<double>[n];

            for (int i = 0; i < n; i++)
                buckets[i] = new List<double>();

            // Distribute elements into buckets
            foreach (double num in array)
            {
                int bucketIndex = (int)(num * n);
                if (bucketIndex >= n) bucketIndex = n - 1;
                buckets[bucketIndex].Add(num);
            }

            // Sort individual buckets and combine
            int index = 0;
            foreach (var bucket in buckets)
            {
                var sorted = bucket.OrderBy(x => x).ToArray();
                foreach (double num in sorted)
                    array[index++] = num;
            }
        }

        #endregion

        #region Sorting Utilities

        /// <summary>
        /// Check if array is sorted
        /// </summary>
        public static bool IsSorted<T>(T[] array) where T : IComparable<T>
        {
            return array.Zip(array.Skip(1), (a, b) => a.CompareTo(b) <= 0).All(x => x);
        }

        /// <summary>
        /// Shuffle array using Fisher-Yates algorithm
        /// </summary>
        public static void Shuffle<T>(T[] array)
        {
            Random rand = new Random();
            for (int i = array.Length - 1; i > 0; i--)
            {
                int j = rand.Next(i + 1);
                (array[i], array[j]) = (array[j], array[i]);
            }
        }

        /// <summary>
        /// Get k smallest elements using partial sort
        /// </summary>
        public static IEnumerable<T> GetKSmallest<T>(IEnumerable<T> collection, int k) where T : IComparable<T>
        {
            return collection.OrderBy(x => x).Take(k);
        }

        /// <summary>
        /// Get k largest elements efficiently
        /// </summary>
        public static IEnumerable<T> GetKLargest<T>(IEnumerable<T> collection, int k) where T : IComparable<T>
        {
            return collection.OrderByDescending(x => x).Take(k);
        }

        #endregion

        #region Performance Benchmarking

        /// <summary>
        /// Benchmark sorting algorithm performance
        /// </summary>
        public static SortingBenchmark BenchmarkSort<T>(T[] array, Action<T[]> sortingAlgorithm) where T : IComparable<T>
        {
            T[] workingCopy = (T[])array.Clone();
            var stopwatch = Stopwatch.StartNew();

            sortingAlgorithm(workingCopy);

            stopwatch.Stop();

            return new SortingBenchmark
            {
                ElementCount = array.Length,
                ElapsedMilliseconds = stopwatch.ElapsedMilliseconds,
                IsSorted = IsSorted(workingCopy)
            };
        }

        public class SortingBenchmark
        {
            public int ElementCount { get; set; }
            public long ElapsedMilliseconds { get; set; }
            public bool IsSorted { get; set; }

            public override string ToString()
            {
                return $"Elements: {ElementCount}, Time: {ElapsedMilliseconds}ms, Sorted: {IsSorted}";
            }
        }

        #endregion
    }

    /// <summary>
    /// Extension methods for sorting operations
    /// </summary>
    public static class SortingExtensions
    {
        /// <summary>
        /// In-place quick sort extension method
        /// </summary>
        public static T[] QuickSorted<T>(this T[] array) where T : IComparable<T>
        {
            T[] result = (T[])array.Clone();
            SortingAlgorithms.QuickSort(result);
            return result;
        }

        /// <summary>
        /// Stable merge sort extension method
        /// </summary>
        public static T[] MergeSorted<T>(this T[] array) where T : IComparable<T>
        {
            T[] result = (T[])array.Clone();
            SortingAlgorithms.MergeSort(result);
            return result;
        }

        /// <summary>
        /// LINQ-style sorting with custom key selector
        /// </summary>
        public static IEnumerable<T> OrderByStable<T, TKey>(this IEnumerable<T> source, Func<T, TKey> keySelector)
        {
            return source.Select((item, index) => new { item, index })
                        .OrderBy(x => keySelector(x.item))
                        .ThenBy(x => x.index)
                        .Select(x => x.item);
        }

        /// <summary>
        /// Partition collection based on pivot
        /// </summary>
        public static (IEnumerable<T> less, IEnumerable<T> equal, IEnumerable<T> greater)
            Partition<T>(this IEnumerable<T> source, T pivot) where T : IComparable<T>
        {
            var groups = source.GroupBy(x => x.CompareTo(pivot) switch
            {
                < 0 => -1,
                0 => 0,
                > 0 => 1
            });

            return (
                groups.Where(g => g.Key == -1).SelectMany(g => g),
                groups.Where(g => g.Key == 0).SelectMany(g => g),
                groups.Where(g => g.Key == 1).SelectMany(g => g)
            );
        }
    }
}