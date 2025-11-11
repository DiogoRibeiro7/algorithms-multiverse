"""
Dynamic Programming Classic Problems
=====================================

This module contains comprehensive implementations of classic DP problems
with multiple solution approaches: naive recursive, memoized (top-down),
tabulated (bottom-up), and space-optimized versions.

Each problem includes:
- Multiple solution approaches
- Detailed complexity analysis
- Real-world applications
- Example usage
"""

from typing import List, Tuple, Dict
from functools import lru_cache


# ============================================================================
# 1. LONGEST COMMON SUBSEQUENCE (LCS)
# ============================================================================

"""
Problem: Find the length of the longest subsequence common to two sequences.
A subsequence is a sequence that appears in the same relative order,
but not necessarily contiguous.

Real-world applications:
- Version control systems (diff algorithms)
- DNA sequence analysis in bioinformatics
- Plagiarism detection
- File comparison tools
"""

def lcs_naive(s1: str, s2: str) -> int:
    """
    Naive recursive solution.
    Time: O(2^(m+n)) - exponential due to overlapping subproblems
    Space: O(m+n) - recursion stack depth
    """
    def helper(i: int, j: int) -> int:
        if i == len(s1) or j == len(s2):
            return 0

        if s1[i] == s2[j]:
            return 1 + helper(i + 1, j + 1)
        else:
            return max(helper(i + 1, j), helper(i, j + 1))

    return helper(0, 0)


def lcs_memoized(s1: str, s2: str) -> int:
    """
    Memoized (top-down) DP solution.
    Time: O(m*n) - each state computed once
    Space: O(m*n) - memoization table + recursion stack
    """
    memo = {}

    def helper(i: int, j: int) -> int:
        if i == len(s1) or j == len(s2):
            return 0

        if (i, j) in memo:
            return memo[(i, j)]

        if s1[i] == s2[j]:
            result = 1 + helper(i + 1, j + 1)
        else:
            result = max(helper(i + 1, j), helper(i, j + 1))

        memo[(i, j)] = result
        return result

    return helper(0, 0)


def lcs_tabulated(s1: str, s2: str) -> int:
    """
    Tabulated (bottom-up) DP solution.
    Time: O(m*n)
    Space: O(m*n)

    State transition:
    dp[i][j] = length of LCS of s1[0...i-1] and s2[0...j-1]

    If s1[i-1] == s2[j-1]:
        dp[i][j] = 1 + dp[i-1][j-1]
    Else:
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]


def lcs_space_optimized(s1: str, s2: str) -> int:
    """
    Space-optimized solution using only two rows.
    Time: O(m*n)
    Space: O(min(m, n)) - only two rows needed
    """
    # Ensure s2 is the shorter string to optimize space
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    m, n = len(s1), len(s2)
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = 1 + prev[j-1]
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev, curr = curr, prev

    return prev[n]


# ============================================================================
# 2. LONGEST INCREASING SUBSEQUENCE (LIS)
# ============================================================================

"""
Problem: Find the length of the longest strictly increasing subsequence.

Real-world applications:
- Analyzing stock market trends
- Scheduling tasks with dependencies
- Box stacking problems
- Patience sorting algorithm
"""

def lis_naive(arr: List[int]) -> int:
    """
    Naive recursive solution.
    Time: O(2^n) - exponential
    Space: O(n) - recursion depth
    """
    def helper(idx: int, prev_val: float) -> int:
        if idx == len(arr):
            return 0

        # Option 1: Don't include current element
        exclude = helper(idx + 1, prev_val)

        # Option 2: Include current element if valid
        include = 0
        if arr[idx] > prev_val:
            include = 1 + helper(idx + 1, arr[idx])

        return max(include, exclude)

    return helper(0, float('-inf'))


def lis_memoized(arr: List[int]) -> int:
    """
    Memoized solution with coordinate compression.
    Time: O(n^2)
    Space: O(n^2)
    """
    n = len(arr)
    memo = {}

    def helper(idx: int, prev_idx: int) -> int:
        if idx == n:
            return 0

        if (idx, prev_idx) in memo:
            return memo[(idx, prev_idx)]

        # Don't include current
        exclude = helper(idx + 1, prev_idx)

        # Include current if valid
        include = 0
        if prev_idx == -1 or arr[idx] > arr[prev_idx]:
            include = 1 + helper(idx + 1, idx)

        result = max(include, exclude)
        memo[(idx, prev_idx)] = result
        return result

    return helper(0, -1)


def lis_tabulated(arr: List[int]) -> int:
    """
    Tabulated O(n^2) solution.
    Time: O(n^2)
    Space: O(n)

    State: dp[i] = length of LIS ending at index i
    """
    if not arr:
        return 0

    n = len(arr)
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def lis_optimized(arr: List[int]) -> int:
    """
    Optimized solution using binary search.
    Time: O(n log n) - optimal solution
    Space: O(n)

    Uses patience sorting concept: maintain smallest tail
    element for each increasing subsequence length.
    """
    from bisect import bisect_left

    if not arr:
        return 0

    # tails[i] = smallest tail element of all increasing subsequences of length i+1
    tails = []

    for num in arr:
        pos = bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num

    return len(tails)


# ============================================================================
# 3. EDIT DISTANCE (LEVENSHTEIN DISTANCE)
# ============================================================================

"""
Problem: Find minimum number of operations (insert, delete, replace) to
convert one string to another.

Real-world applications:
- Spell checkers
- DNA sequence alignment
- Natural language processing (fuzzy string matching)
- Autocorrect systems
"""

def edit_distance_naive(s1: str, s2: str) -> int:
    """
    Naive recursive solution.
    Time: O(3^max(m,n))
    Space: O(max(m, n))
    """
    def helper(i: int, j: int) -> int:
        # Base cases
        if i == 0:
            return j
        if j == 0:
            return i

        if s1[i-1] == s2[j-1]:
            return helper(i-1, j-1)

        # Try all three operations
        insert_op = 1 + helper(i, j-1)
        delete_op = 1 + helper(i-1, j)
        replace_op = 1 + helper(i-1, j-1)

        return min(insert_op, delete_op, replace_op)

    return helper(len(s1), len(s2))


def edit_distance_memoized(s1: str, s2: str) -> int:
    """
    Memoized solution.
    Time: O(m*n)
    Space: O(m*n)
    """
    memo = {}

    def helper(i: int, j: int) -> int:
        if i == 0:
            return j
        if j == 0:
            return i

        if (i, j) in memo:
            return memo[(i, j)]

        if s1[i-1] == s2[j-1]:
            result = helper(i-1, j-1)
        else:
            result = 1 + min(
                helper(i, j-1),    # insert
                helper(i-1, j),    # delete
                helper(i-1, j-1)   # replace
            )

        memo[(i, j)] = result
        return result

    return helper(len(s1), len(s2))


def edit_distance_tabulated(s1: str, s2: str) -> int:
    """
    Tabulated solution.
    Time: O(m*n)
    Space: O(m*n)

    State: dp[i][j] = edit distance between s1[0...i-1] and s2[0...j-1]
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i][j-1],    # insert
                    dp[i-1][j],    # delete
                    dp[i-1][j-1]   # replace
                )

    return dp[m][n]


def edit_distance_space_optimized(s1: str, s2: str) -> int:
    """
    Space-optimized solution.
    Time: O(m*n)
    Space: O(min(m, n))
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    m, n = len(s1), len(s2)
    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = 1 + min(curr[j-1], prev[j], prev[j-1])
        prev, curr = curr, prev

    return prev[n]


# ============================================================================
# 4. COIN CHANGE PROBLEM
# ============================================================================

"""
Problem: Find minimum number of coins needed to make a given amount,
or count the number of ways to make change.

Real-world applications:
- Making change in vending machines
- Currency exchange optimization
- Resource allocation problems
- Subset sum variations
"""

def coin_change_min_naive(coins: List[int], amount: int) -> int:
    """
    Naive recursive solution for minimum coins.
    Time: O(amount^len(coins))
    Space: O(amount)
    """
    def helper(remaining: int) -> int:
        if remaining == 0:
            return 0
        if remaining < 0:
            return float('inf')

        min_coins = float('inf')
        for coin in coins:
            result = helper(remaining - coin)
            if result != float('inf'):
                min_coins = min(min_coins, result + 1)

        return min_coins

    result = helper(amount)
    return result if result != float('inf') else -1


def coin_change_min_memoized(coins: List[int], amount: int) -> int:
    """
    Memoized solution for minimum coins.
    Time: O(amount * len(coins))
    Space: O(amount)
    """
    memo = {}

    def helper(remaining: int) -> int:
        if remaining == 0:
            return 0
        if remaining < 0:
            return float('inf')

        if remaining in memo:
            return memo[remaining]

        min_coins = float('inf')
        for coin in coins:
            result = helper(remaining - coin)
            if result != float('inf'):
                min_coins = min(min_coins, result + 1)

        memo[remaining] = min_coins
        return min_coins

    result = helper(amount)
    return result if result != float('inf') else -1


def coin_change_min_tabulated(coins: List[int], amount: int) -> int:
    """
    Tabulated solution for minimum coins.
    Time: O(amount * len(coins))
    Space: O(amount)

    State: dp[i] = minimum coins needed to make amount i
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_ways_tabulated(coins: List[int], amount: int) -> int:
    """
    Count number of ways to make change.
    Time: O(amount * len(coins))
    Space: O(amount)

    State: dp[i] = number of ways to make amount i
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    # Process each coin one at a time to avoid counting permutations
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]


# ============================================================================
# 5. KNAPSACK PROBLEMS
# ============================================================================

"""
Problem: Given items with weights and values, maximize value within
weight capacity.

Types:
- 0/1 Knapsack: Each item can be taken at most once
- Unbounded Knapsack: Unlimited quantity of each item

Real-world applications:
- Resource allocation with budget constraints
- Portfolio optimization
- Cargo loading
- Memory management
"""

def knapsack_01_naive(weights: List[int], values: List[int], capacity: int) -> int:
    """
    0/1 Knapsack - Naive recursive.
    Time: O(2^n)
    Space: O(n)
    """
    def helper(idx: int, remaining: int) -> int:
        if idx == len(weights) or remaining == 0:
            return 0

        # Don't take current item
        skip = helper(idx + 1, remaining)

        # Take current item if possible
        take = 0
        if weights[idx] <= remaining:
            take = values[idx] + helper(idx + 1, remaining - weights[idx])

        return max(skip, take)

    return helper(0, capacity)


def knapsack_01_memoized(weights: List[int], values: List[int], capacity: int) -> int:
    """
    0/1 Knapsack - Memoized.
    Time: O(n * capacity)
    Space: O(n * capacity)
    """
    memo = {}

    def helper(idx: int, remaining: int) -> int:
        if idx == len(weights) or remaining == 0:
            return 0

        if (idx, remaining) in memo:
            return memo[(idx, remaining)]

        skip = helper(idx + 1, remaining)
        take = 0
        if weights[idx] <= remaining:
            take = values[idx] + helper(idx + 1, remaining - weights[idx])

        result = max(skip, take)
        memo[(idx, remaining)] = result
        return result

    return helper(0, capacity)


def knapsack_01_tabulated(weights: List[int], values: List[int], capacity: int) -> int:
    """
    0/1 Knapsack - Tabulated.
    Time: O(n * capacity)
    Space: O(n * capacity)

    State: dp[i][w] = max value using items 0...i-1 with capacity w
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i-1
            dp[i][w] = dp[i-1][w]

            # Take item i-1 if possible
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])

    return dp[n][capacity]


def knapsack_01_space_optimized(weights: List[int], values: List[int], capacity: int) -> int:
    """
    0/1 Knapsack - Space optimized.
    Time: O(n * capacity)
    Space: O(capacity)
    """
    dp = [0] * (capacity + 1)

    for i in range(len(weights)):
        # Traverse backwards to avoid using updated values
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]


def knapsack_unbounded_tabulated(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Unbounded Knapsack - can take unlimited items.
    Time: O(n * capacity)
    Space: O(capacity)

    State: dp[w] = max value with capacity w
    """
    dp = [0] * (capacity + 1)

    for w in range(1, capacity + 1):
        for i in range(len(weights)):
            if weights[i] <= w:
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]


# ============================================================================
# 6. MATRIX CHAIN MULTIPLICATION
# ============================================================================

"""
Problem: Find optimal parenthesization of matrix chain to minimize
scalar multiplications.

Given chain A1 x A2 x ... x An where Ai has dimensions dims[i-1] x dims[i],
find minimum cost of multiplication.

Real-world applications:
- Compiler optimization
- Database query optimization
- Computer graphics transformations
- Expression evaluation order
"""

def matrix_chain_naive(dims: List[int]) -> int:
    """
    Naive recursive solution.
    Time: O(2^n) - Catalan number complexity
    Space: O(n)

    Cost of multiplying (p x q) and (q x r) matrices = p*q*r
    """
    def helper(i: int, j: int) -> int:
        if i == j:
            return 0

        min_cost = float('inf')
        # Try all split points
        for k in range(i, j):
            cost = (
                helper(i, k) +
                helper(k + 1, j) +
                dims[i-1] * dims[k] * dims[j]
            )
            min_cost = min(min_cost, cost)

        return min_cost

    n = len(dims)
    return helper(1, n - 1)


def matrix_chain_memoized(dims: List[int]) -> int:
    """
    Memoized solution.
    Time: O(n^3)
    Space: O(n^2)
    """
    memo = {}

    def helper(i: int, j: int) -> int:
        if i == j:
            return 0

        if (i, j) in memo:
            return memo[(i, j)]

        min_cost = float('inf')
        for k in range(i, j):
            cost = (
                helper(i, k) +
                helper(k + 1, j) +
                dims[i-1] * dims[k] * dims[j]
            )
            min_cost = min(min_cost, cost)

        memo[(i, j)] = min_cost
        return min_cost

    n = len(dims)
    return helper(1, n - 1)


def matrix_chain_tabulated(dims: List[int]) -> int:
    """
    Tabulated solution.
    Time: O(n^3)
    Space: O(n^2)

    State: dp[i][j] = min cost to multiply matrices from i to j
    Fill diagonally by chain length.
    """
    n = len(dims)
    dp = [[0] * n for _ in range(n)]

    # l is chain length
    for length in range(2, n):
        for i in range(1, n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')

            for k in range(i, j):
                cost = (
                    dp[i][k] +
                    dp[k + 1][j] +
                    dims[i-1] * dims[k] * dims[j]
                )
                dp[i][j] = min(dp[i][j], cost)

    return dp[1][n - 1]


# ============================================================================
# 7. PALINDROME PROBLEMS
# ============================================================================

"""
Problems:
- Longest Palindromic Subsequence
- Count of palindromic substrings
- Minimum insertions to make palindrome

Real-world applications:
- DNA sequence analysis
- Text processing and pattern recognition
- Data compression
- Error detection codes
"""

def longest_palindrome_subsequence_naive(s: str) -> int:
    """
    Naive recursive solution.
    Time: O(2^n)
    Space: O(n)
    """
    def helper(i: int, j: int) -> int:
        if i > j:
            return 0
        if i == j:
            return 1

        if s[i] == s[j]:
            return 2 + helper(i + 1, j - 1)
        else:
            return max(helper(i + 1, j), helper(i, j - 1))

    return helper(0, len(s) - 1)


def longest_palindrome_subsequence_tabulated(s: str) -> int:
    """
    Tabulated solution for longest palindromic subsequence.
    Time: O(n^2)
    Space: O(n^2)

    State: dp[i][j] = length of LPS in s[i...j]
    """
    n = len(s)
    dp = [[0] * n for _ in range(n)]

    # Base case: single characters
    for i in range(n):
        dp[i][i] = 1

    # Fill diagonally
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                dp[i][j] = 2 + (dp[i + 1][j - 1] if i + 1 <= j - 1 else 0)
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]


def count_palindromic_substrings(s: str) -> int:
    """
    Count all palindromic substrings.
    Time: O(n^2)
    Space: O(1)

    Uses expand-around-center approach.
    """
    def expand_around_center(left: int, right: int) -> int:
        count = 0
        while left >= 0 and right < len(s) and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
        return count

    total = 0
    for i in range(len(s)):
        # Odd length palindromes
        total += expand_around_center(i, i)
        # Even length palindromes
        total += expand_around_center(i, i + 1)

    return total


def min_insertions_palindrome(s: str) -> int:
    """
    Minimum insertions to make string a palindrome.
    Time: O(n^2)
    Space: O(n^2)

    Answer = n - LPS(s)
    """
    return len(s) - longest_palindrome_subsequence_tabulated(s)


def palindrome_partitioning_min_cuts(s: str) -> int:
    """
    Minimum cuts needed to partition string into palindromes.
    Time: O(n^2)
    Space: O(n^2)
    """
    n = len(s)

    # Build palindrome table
    is_palindrome = [[False] * n for _ in range(n)]
    for i in range(n):
        is_palindrome[i][i] = True

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                is_palindrome[i][j] = (length == 2) or is_palindrome[i + 1][j - 1]

    # DP for minimum cuts
    dp = [float('inf')] * n
    for i in range(n):
        if is_palindrome[0][i]:
            dp[i] = 0
        else:
            for j in range(i):
                if is_palindrome[j + 1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)

    return dp[n - 1]


# ============================================================================
# 8. MAXIMUM SUBARRAY SUM (KADANE'S ALGORITHM)
# ============================================================================

"""
Problem: Find contiguous subarray with maximum sum.

Real-world applications:
- Stock market analysis (best time to buy/sell)
- Signal processing
- Image processing
- Resource allocation over time
"""

def max_subarray_naive(arr: List[int]) -> int:
    """
    Naive solution - check all subarrays.
    Time: O(n^2) or O(n^3) depending on implementation
    Space: O(1)
    """
    if not arr:
        return 0

    max_sum = float('-inf')
    n = len(arr)

    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            max_sum = max(max_sum, current_sum)

    return max_sum


def max_subarray_kadane(arr: List[int]) -> int:
    """
    Kadane's Algorithm - optimal solution.
    Time: O(n)
    Space: O(1)

    Key insight: At each position, either extend current subarray
    or start fresh from current element.
    """
    if not arr:
        return 0

    max_sum = arr[0]
    current_sum = arr[0]

    for i in range(1, len(arr)):
        current_sum = max(arr[i], current_sum + arr[i])
        max_sum = max(max_sum, current_sum)

    return max_sum


def max_subarray_with_indices(arr: List[int]) -> Tuple[int, int, int]:
    """
    Kadane's with start and end indices.
    Time: O(n)
    Space: O(1)

    Returns: (max_sum, start_index, end_index)
    """
    if not arr:
        return (0, -1, -1)

    max_sum = arr[0]
    current_sum = arr[0]
    start = 0
    end = 0
    temp_start = 0

    for i in range(1, len(arr)):
        if arr[i] > current_sum + arr[i]:
            current_sum = arr[i]
            temp_start = i
        else:
            current_sum = current_sum + arr[i]

        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i

    return (max_sum, start, end)


def max_subarray_circular(arr: List[int]) -> int:
    """
    Maximum subarray sum in circular array.
    Time: O(n)
    Space: O(1)

    Key insight: Max circular sum = max(normal max, total - min subarray)
    """
    if not arr:
        return 0

    def kadane_min(arr: List[int]) -> int:
        """Find minimum subarray sum."""
        min_sum = arr[0]
        current_sum = arr[0]
        for i in range(1, len(arr)):
            current_sum = min(arr[i], current_sum + arr[i])
            min_sum = min(min_sum, current_sum)
        return min_sum

    max_normal = max_subarray_kadane(arr)

    # Handle all negative case
    if max_normal < 0:
        return max_normal

    total_sum = sum(arr)
    min_sum = kadane_min(arr)
    max_circular = total_sum - min_sum

    return max(max_normal, max_circular)


# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DYNAMIC PROGRAMMING CLASSIC PROBLEMS - EXAMPLES")
    print("=" * 70)

    # LCS Examples
    print("\n1. Longest Common Subsequence:")
    s1, s2 = "ABCDGH", "AEDFHR"
    print(f"   Strings: '{s1}', '{s2}'")
    print(f"   Naive: {lcs_naive(s1, s2)}")
    print(f"   Memoized: {lcs_memoized(s1, s2)}")
    print(f"   Tabulated: {lcs_tabulated(s1, s2)}")
    print(f"   Space-optimized: {lcs_space_optimized(s1, s2)}")

    # LIS Examples
    print("\n2. Longest Increasing Subsequence:")
    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"   Array: {arr}")
    print(f"   Naive: {lis_naive(arr)}")
    print(f"   Memoized: {lis_memoized(arr)}")
    print(f"   Tabulated O(n^2): {lis_tabulated(arr)}")
    print(f"   Optimized O(n log n): {lis_optimized(arr)}")

    # Edit Distance
    print("\n3. Edit Distance:")
    s1, s2 = "kitten", "sitting"
    print(f"   Strings: '{s1}', '{s2}'")
    print(f"   Naive: {edit_distance_naive(s1, s2)}")
    print(f"   Memoized: {edit_distance_memoized(s1, s2)}")
    print(f"   Tabulated: {edit_distance_tabulated(s1, s2)}")
    print(f"   Space-optimized: {edit_distance_space_optimized(s1, s2)}")

    # Coin Change
    print("\n4. Coin Change:")
    coins, amount = [1, 2, 5], 11
    print(f"   Coins: {coins}, Amount: {amount}")
    print(f"   Min coins (naive): {coin_change_min_naive(coins, amount)}")
    print(f"   Min coins (memoized): {coin_change_min_memoized(coins, amount)}")
    print(f"   Min coins (tabulated): {coin_change_min_tabulated(coins, amount)}")
    print(f"   Ways to make change: {coin_change_ways_tabulated(coins, amount)}")

    # Knapsack
    print("\n5. Knapsack Problem:")
    weights, values, capacity = [1, 3, 4, 5], [1, 4, 5, 7], 7
    print(f"   Weights: {weights}, Values: {values}, Capacity: {capacity}")
    print(f"   0/1 Naive: {knapsack_01_naive(weights, values, capacity)}")
    print(f"   0/1 Memoized: {knapsack_01_memoized(weights, values, capacity)}")
    print(f"   0/1 Tabulated: {knapsack_01_tabulated(weights, values, capacity)}")
    print(f"   0/1 Space-optimized: {knapsack_01_space_optimized(weights, values, capacity)}")
    print(f"   Unbounded: {knapsack_unbounded_tabulated(weights, values, capacity)}")

    # Matrix Chain
    print("\n6. Matrix Chain Multiplication:")
    dims = [10, 20, 30, 40, 30]
    print(f"   Dimensions: {dims}")
    print(f"   Naive: {matrix_chain_naive(dims)}")
    print(f"   Memoized: {matrix_chain_memoized(dims)}")
    print(f"   Tabulated: {matrix_chain_tabulated(dims)}")

    # Palindromes
    print("\n7. Palindrome Problems:")
    s = "bbbab"
    print(f"   String: '{s}'")
    print(f"   Longest palindromic subsequence: {longest_palindrome_subsequence_tabulated(s)}")
    print(f"   Count palindromic substrings: {count_palindromic_substrings(s)}")
    print(f"   Min insertions for palindrome: {min_insertions_palindrome(s)}")
    print(f"   Min cuts for palindrome partition: {palindrome_partitioning_min_cuts(s)}")

    # Maximum Subarray
    print("\n8. Maximum Subarray Sum:")
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"   Array: {arr}")
    print(f"   Naive: {max_subarray_naive(arr)}")
    print(f"   Kadane's: {max_subarray_kadane(arr)}")
    max_sum, start, end = max_subarray_with_indices(arr)
    print(f"   With indices: sum={max_sum}, range=[{start}:{end+1}]")

    arr_circular = [5, -3, 5]
    print(f"   Circular array: {arr_circular}")
    print(f"   Max circular sum: {max_subarray_circular(arr_circular)}")

    print("\n" + "=" * 70)
