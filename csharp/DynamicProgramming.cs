using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace AlgorithmsMultiverse.CSharp
{
    /// <summary>
    /// Dynamic Programming algorithms with LINQ optimizations
    /// </summary>
    public static class DynamicProgramming
    {
        #region Classic DP Problems

        /// <summary>
        /// Fibonacci number with memoization
        /// </summary>
        public static long Fibonacci(int n, Dictionary<int, long> memo = null)
        {
            memo ??= new Dictionary<int, long>();

            if (n <= 1) return n;
            if (memo.ContainsKey(n)) return memo[n];

            memo[n] = Fibonacci(n - 1, memo) + Fibonacci(n - 2, memo);
            return memo[n];
        }

        /// <summary>
        /// Fibonacci with bottom-up approach
        /// </summary>
        public static long FibonacciIterative(int n)
        {
            if (n <= 1) return n;

            long prev = 0, curr = 1;
            for (int i = 2; i <= n; i++)
            {
                long temp = curr;
                curr = prev + curr;
                prev = temp;
            }

            return curr;
        }

        /// <summary>
        /// Generate Fibonacci sequence using LINQ
        /// </summary>
        public static IEnumerable<long> FibonacciSequence()
        {
            long prev = 0, curr = 1;
            yield return prev;
            yield return curr;

            while (true)
            {
                long next = prev + curr;
                yield return next;
                prev = curr;
                curr = next;
            }
        }

        #endregion

        #region Longest Common Subsequence

        /// <summary>
        /// Longest Common Subsequence length
        /// </summary>
        public static int LongestCommonSubsequence<T>(T[] seq1, T[] seq2) where T : IEquatable<T>
        {
            int m = seq1.Length;
            int n = seq2.Length;
            int[,] dp = new int[m + 1, n + 1];

            for (int i = 1; i <= m; i++)
            {
                for (int j = 1; j <= n; j++)
                {
                    if (seq1[i - 1].Equals(seq2[j - 1]))
                        dp[i, j] = dp[i - 1, j - 1] + 1;
                    else
                        dp[i, j] = Math.Max(dp[i - 1, j], dp[i, j - 1]);
                }
            }

            return dp[m, n];
        }

        /// <summary>
        /// Get the actual LCS
        /// </summary>
        public static T[] GetLCS<T>(T[] seq1, T[] seq2) where T : IEquatable<T>
        {
            int m = seq1.Length;
            int n = seq2.Length;
            int[,] dp = new int[m + 1, n + 1];

            // Fill DP table
            for (int i = 1; i <= m; i++)
            {
                for (int j = 1; j <= n; j++)
                {
                    if (seq1[i - 1].Equals(seq2[j - 1]))
                        dp[i, j] = dp[i - 1, j - 1] + 1;
                    else
                        dp[i, j] = Math.Max(dp[i - 1, j], dp[i, j - 1]);
                }
            }

            // Backtrack to find LCS
            List<T> lcs = new List<T>();
            int x = m, y = n;

            while (x > 0 && y > 0)
            {
                if (seq1[x - 1].Equals(seq2[y - 1]))
                {
                    lcs.Insert(0, seq1[x - 1]);
                    x--;
                    y--;
                }
                else if (dp[x - 1, y] > dp[x, y - 1])
                {
                    x--;
                }
                else
                {
                    y--;
                }
            }

            return lcs.ToArray();
        }

        #endregion

        #region Longest Increasing Subsequence

        /// <summary>
        /// Longest Increasing Subsequence length
        /// </summary>
        public static int LongestIncreasingSubsequence<T>(T[] sequence) where T : IComparable<T>
        {
            if (sequence.Length == 0) return 0;

            int[] dp = new int[sequence.Length];
            Array.Fill(dp, 1);

            for (int i = 1; i < sequence.Length; i++)
            {
                for (int j = 0; j < i; j++)
                {
                    if (sequence[j].CompareTo(sequence[i]) < 0)
                        dp[i] = Math.Max(dp[i], dp[j] + 1);
                }
            }

            return dp.Max();
        }

        /// <summary>
        /// LIS using binary search - O(n log n)
        /// </summary>
        public static int LISOptimized<T>(T[] sequence) where T : IComparable<T>
        {
            if (sequence.Length == 0) return 0;

            List<T> tails = new List<T>();

            foreach (T item in sequence)
            {
                int pos = tails.BinarySearch(item);

                if (pos < 0)
                    pos = ~pos; // Get insertion point

                if (pos == tails.Count)
                    tails.Add(item);
                else
                    tails[pos] = item;
            }

            return tails.Count;
        }

        /// <summary>
        /// Get all longest increasing subsequences using LINQ
        /// </summary>
        public static IEnumerable<T[]> GetAllLIS<T>(T[] sequence) where T : IComparable<T>
        {
            if (sequence.Length == 0)
                yield break;

            var dp = new List<List<T[]>>();

            for (int i = 0; i < sequence.Length; i++)
            {
                dp.Add(new List<T[]> { new[] { sequence[i] } });

                for (int j = 0; j < i; j++)
                {
                    if (sequence[j].CompareTo(sequence[i]) < 0)
                    {
                        var extended = dp[j]
                            .Select(seq => seq.Concat(new[] { sequence[i] }).ToArray())
                            .ToList();

                        if (extended.Any() && extended[0].Length > dp[i][0].Length)
                            dp[i] = extended;
                        else if (extended.Any() && extended[0].Length == dp[i][0].Length)
                            dp[i].AddRange(extended);
                    }
                }
            }

            int maxLength = dp.Max(list => list[0].Length);
            foreach (var subsequences in dp.Where(list => list[0].Length == maxLength))
                foreach (var seq in subsequences)
                    yield return seq;
        }

        #endregion

        #region Knapsack Problems

        /// <summary>
        /// 0/1 Knapsack problem
        /// </summary>
        public static (int MaxValue, List<int> Items) Knapsack01(
            int[] weights,
            int[] values,
            int capacity)
        {
            int n = weights.Length;
            int[,] dp = new int[n + 1, capacity + 1];

            // Fill DP table
            for (int i = 1; i <= n; i++)
            {
                for (int w = 0; w <= capacity; w++)
                {
                    if (weights[i - 1] <= w)
                    {
                        dp[i, w] = Math.Max(
                            dp[i - 1, w],
                            values[i - 1] + dp[i - 1, w - weights[i - 1]]
                        );
                    }
                    else
                    {
                        dp[i, w] = dp[i - 1, w];
                    }
                }
            }

            // Backtrack to find items
            List<int> items = new List<int>();
            int remainingCapacity = capacity;

            for (int i = n; i > 0 && remainingCapacity > 0; i--)
            {
                if (dp[i, remainingCapacity] != dp[i - 1, remainingCapacity])
                {
                    items.Add(i - 1);
                    remainingCapacity -= weights[i - 1];
                }
            }

            return (dp[n, capacity], items);
        }

        /// <summary>
        /// Unbounded Knapsack using LINQ
        /// </summary>
        public static int UnboundedKnapsack(
            IEnumerable<(int Weight, int Value)> items,
            int capacity)
        {
            int[] dp = new int[capacity + 1];

            for (int w = 1; w <= capacity; w++)
            {
                dp[w] = items
                    .Where(item => item.Weight <= w)
                    .Select(item => item.Value + dp[w - item.Weight])
                    .DefaultIfEmpty(0)
                    .Max();
            }

            return dp[capacity];
        }

        /// <summary>
        /// Fractional Knapsack (Greedy approach)
        /// </summary>
        public static double FractionalKnapsack(
            IEnumerable<(int Weight, int Value)> items,
            int capacity)
        {
            var sortedItems = items
                .Select(item => new
                {
                    item.Weight,
                    item.Value,
                    Ratio = (double)item.Value / item.Weight
                })
                .OrderByDescending(item => item.Ratio);

            double totalValue = 0;
            int remainingCapacity = capacity;

            foreach (var item in sortedItems)
            {
                if (remainingCapacity >= item.Weight)
                {
                    totalValue += item.Value;
                    remainingCapacity -= item.Weight;
                }
                else
                {
                    totalValue += item.Ratio * remainingCapacity;
                    break;
                }
            }

            return totalValue;
        }

        #endregion

        #region Coin Change

        /// <summary>
        /// Minimum coins needed to make change
        /// </summary>
        public static int CoinChangeMinCoins(int[] coins, int amount)
        {
            int[] dp = new int[amount + 1];
            Array.Fill(dp, int.MaxValue);
            dp[0] = 0;

            for (int i = 1; i <= amount; i++)
            {
                foreach (int coin in coins)
                {
                    if (coin <= i && dp[i - coin] != int.MaxValue)
                        dp[i] = Math.Min(dp[i], dp[i - coin] + 1);
                }
            }

            return dp[amount] == int.MaxValue ? -1 : dp[amount];
        }

        /// <summary>
        /// Number of ways to make change
        /// </summary>
        public static int CoinChangeWays(int[] coins, int amount)
        {
            int[] dp = new int[amount + 1];
            dp[0] = 1;

            foreach (int coin in coins)
            {
                for (int i = coin; i <= amount; i++)
                {
                    dp[i] += dp[i - coin];
                }
            }

            return dp[amount];
        }

        /// <summary>
        /// Get all combinations to make change using LINQ
        /// </summary>
        public static IEnumerable<List<int>> GetCoinCombinations(int[] coins, int amount)
        {
            if (amount == 0)
            {
                yield return new List<int>();
                yield break;
            }

            for (int i = 0; i < coins.Length; i++)
            {
                if (coins[i] <= amount)
                {
                    foreach (var combination in GetCoinCombinations(
                        coins.Skip(i).ToArray(),
                        amount - coins[i]))
                    {
                        combination.Insert(0, coins[i]);
                        yield return combination;
                    }
                }
            }
        }

        #endregion

        #region Edit Distance

        /// <summary>
        /// Levenshtein distance between two strings
        /// </summary>
        public static int EditDistance(string s1, string s2)
        {
            int m = s1.Length;
            int n = s2.Length;
            int[,] dp = new int[m + 1, n + 1];

            // Initialize base cases
            for (int i = 0; i <= m; i++)
                dp[i, 0] = i;
            for (int j = 0; j <= n; j++)
                dp[0, j] = j;

            // Fill DP table
            for (int i = 1; i <= m; i++)
            {
                for (int j = 1; j <= n; j++)
                {
                    if (s1[i - 1] == s2[j - 1])
                    {
                        dp[i, j] = dp[i - 1, j - 1];
                    }
                    else
                    {
                        dp[i, j] = 1 + Math.Min(
                            dp[i - 1, j],    // Delete
                            Math.Min(
                                dp[i, j - 1],    // Insert
                                dp[i - 1, j - 1] // Replace
                            )
                        );
                    }
                }
            }

            return dp[m, n];
        }

        /// <summary>
        /// Get edit operations to transform s1 to s2
        /// </summary>
        public static List<string> GetEditOperations(string s1, string s2)
        {
            int m = s1.Length;
            int n = s2.Length;
            int[,] dp = new int[m + 1, n + 1];

            // Fill DP table (same as EditDistance)
            for (int i = 0; i <= m; i++)
                dp[i, 0] = i;
            for (int j = 0; j <= n; j++)
                dp[0, j] = j;

            for (int i = 1; i <= m; i++)
            {
                for (int j = 1; j <= n; j++)
                {
                    if (s1[i - 1] == s2[j - 1])
                        dp[i, j] = dp[i - 1, j - 1];
                    else
                        dp[i, j] = 1 + Math.Min(dp[i - 1, j], Math.Min(dp[i, j - 1], dp[i - 1, j - 1]));
                }
            }

            // Backtrack to find operations
            List<string> operations = new List<string>();
            int x = m, y = n;

            while (x > 0 || y > 0)
            {
                if (x > 0 && y > 0 && s1[x - 1] == s2[y - 1])
                {
                    x--;
                    y--;
                }
                else if (y > 0 && (x == 0 || dp[x, y - 1] <= dp[x - 1, y - 1] && dp[x, y - 1] <= dp[x - 1, y]))
                {
                    operations.Insert(0, $"Insert '{s2[y - 1]}' at position {x}");
                    y--;
                }
                else if (x > 0 && (y == 0 || dp[x - 1, y] < dp[x - 1, y - 1] && dp[x - 1, y] < dp[x, y - 1]))
                {
                    operations.Insert(0, $"Delete '{s1[x - 1]}' at position {x - 1}");
                    x--;
                }
                else
                {
                    operations.Insert(0, $"Replace '{s1[x - 1]}' with '{s2[y - 1]}' at position {x - 1}");
                    x--;
                    y--;
                }
            }

            return operations;
        }

        #endregion

        #region Other DP Problems

        /// <summary>
        /// Maximum subarray sum (Kadane's algorithm)
        /// </summary>
        public static int MaxSubarraySum(int[] array)
        {
            int maxSoFar = array[0];
            int maxEndingHere = array[0];

            for (int i = 1; i < array.Length; i++)
            {
                maxEndingHere = Math.Max(array[i], maxEndingHere + array[i]);
                maxSoFar = Math.Max(maxSoFar, maxEndingHere);
            }

            return maxSoFar;
        }

        /// <summary>
        /// Get the actual maximum subarray
        /// </summary>
        public static int[] GetMaxSubarray(int[] array)
        {
            int maxSoFar = array[0];
            int maxEndingHere = array[0];
            int start = 0, end = 0, tempStart = 0;

            for (int i = 1; i < array.Length; i++)
            {
                if (array[i] > maxEndingHere + array[i])
                {
                    maxEndingHere = array[i];
                    tempStart = i;
                }
                else
                {
                    maxEndingHere = maxEndingHere + array[i];
                }

                if (maxEndingHere > maxSoFar)
                {
                    maxSoFar = maxEndingHere;
                    start = tempStart;
                    end = i;
                }
            }

            return array.Skip(start).Take(end - start + 1).ToArray();
        }

        /// <summary>
        /// Unique paths in a grid
        /// </summary>
        public static int UniquePaths(int m, int n)
        {
            int[] dp = new int[n];
            Array.Fill(dp, 1);

            for (int i = 1; i < m; i++)
            {
                for (int j = 1; j < n; j++)
                {
                    dp[j] += dp[j - 1];
                }
            }

            return dp[n - 1];
        }

        /// <summary>
        /// House Robber problem
        /// </summary>
        public static int HouseRobber(int[] houses)
        {
            if (houses.Length == 0) return 0;
            if (houses.Length == 1) return houses[0];

            int prev2 = 0;
            int prev1 = houses[0];

            for (int i = 1; i < houses.Length; i++)
            {
                int current = Math.Max(prev1, prev2 + houses[i]);
                prev2 = prev1;
                prev1 = current;
            }

            return prev1;
        }

        /// <summary>
        /// Longest palindromic substring
        /// </summary>
        public static string LongestPalindromicSubstring(string s)
        {
            if (string.IsNullOrEmpty(s)) return "";

            int start = 0;
            int maxLen = 0;

            void ExpandAroundCenter(int left, int right)
            {
                while (left >= 0 && right < s.Length && s[left] == s[right])
                {
                    int currentLen = right - left + 1;
                    if (currentLen > maxLen)
                    {
                        start = left;
                        maxLen = currentLen;
                    }
                    left--;
                    right++;
                }
            }

            for (int i = 0; i < s.Length; i++)
            {
                ExpandAroundCenter(i, i);     // Odd length
                ExpandAroundCenter(i, i + 1); // Even length
            }

            return s.Substring(start, maxLen);
        }

        /// <summary>
        /// Matrix chain multiplication
        /// </summary>
        public static int MatrixChainMultiplication(int[] dimensions)
        {
            int n = dimensions.Length - 1;
            int[,] dp = new int[n, n];

            for (int len = 2; len <= n; len++)
            {
                for (int i = 0; i < n - len + 1; i++)
                {
                    int j = i + len - 1;
                    dp[i, j] = int.MaxValue;

                    for (int k = i; k < j; k++)
                    {
                        int cost = dp[i, k] + dp[k + 1, j] +
                            dimensions[i] * dimensions[k + 1] * dimensions[j + 1];
                        dp[i, j] = Math.Min(dp[i, j], cost);
                    }
                }
            }

            return dp[0, n - 1];
        }

        /// <summary>
        /// Word break problem using LINQ
        /// </summary>
        public static bool WordBreak(string s, HashSet<string> wordDict)
        {
            bool[] dp = new bool[s.Length + 1];
            dp[0] = true;

            for (int i = 1; i <= s.Length; i++)
            {
                dp[i] = Enumerable.Range(0, i)
                    .Any(j => dp[j] && wordDict.Contains(s.Substring(j, i - j)));
            }

            return dp[s.Length];
        }

        /// <summary>
        /// Get all word break solutions
        /// </summary>
        public static IEnumerable<string> WordBreakSolutions(string s, HashSet<string> wordDict)
        {
            var memo = new Dictionary<string, List<string>>();

            List<string> Helper(string str)
            {
                if (memo.ContainsKey(str))
                    return memo[str];

                var result = new List<string>();

                if (string.IsNullOrEmpty(str))
                {
                    result.Add("");
                    return result;
                }

                foreach (var word in wordDict)
                {
                    if (str.StartsWith(word))
                    {
                        var subResults = Helper(str.Substring(word.Length));
                        foreach (var sub in subResults)
                        {
                            result.Add(word + (string.IsNullOrEmpty(sub) ? "" : " " + sub));
                        }
                    }
                }

                memo[str] = result;
                return result;
            }

            return Helper(s).Where(solution => !string.IsNullOrEmpty(solution));
        }

        #endregion
    }

    /// <summary>
    /// Extension methods for DP operations
    /// </summary>
    public static class DynamicProgrammingExtensions
    {
        /// <summary>
        /// Memoize a function
        /// </summary>
        public static Func<T, TResult> Memoize<T, TResult>(this Func<T, TResult> func)
        {
            var cache = new Dictionary<T, TResult>();
            return arg =>
            {
                if (cache.TryGetValue(arg, out TResult result))
                    return result;

                result = func(arg);
                cache[arg] = result;
                return result;
            };
        }

        /// <summary>
        /// Generate all subsets using dynamic programming
        /// </summary>
        public static IEnumerable<List<T>> GenerateSubsets<T>(this IEnumerable<T> items)
        {
            var itemList = items.ToList();
            int n = itemList.Count;

            for (int mask = 0; mask < (1 << n); mask++)
            {
                var subset = new List<T>();
                for (int i = 0; i < n; i++)
                {
                    if ((mask & (1 << i)) != 0)
                        subset.Add(itemList[i]);
                }
                yield return subset;
            }
        }

        /// <summary>
        /// Check if array can be partitioned into equal sum subsets
        /// </summary>
        public static bool CanPartition(this int[] nums)
        {
            int sum = nums.Sum();
            if (sum % 2 != 0) return false;

            int target = sum / 2;
            bool[] dp = new bool[target + 1];
            dp[0] = true;

            foreach (int num in nums)
            {
                for (int i = target; i >= num; i--)
                {
                    dp[i] = dp[i] || dp[i - num];
                }
            }

            return dp[target];
        }
    }
}