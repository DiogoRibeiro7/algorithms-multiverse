/**
 * Dynamic Programming Classic Problems
 * =====================================
 *
 * Comprehensive implementations of classic DP problems with multiple
 * solution approaches: naive recursive, memoized (top-down),
 * tabulated (bottom-up), and space-optimized versions.
 *
 * Compile: rustc classic_problems.rs
 * Run: ./classic_problems
 */

use std::collections::HashMap;
use std::cmp::{max, min};

// ============================================================================
// 1. LONGEST COMMON SUBSEQUENCE (LCS)
// ============================================================================

/*
Problem: Find the length of the longest subsequence common to two sequences.

Real-world applications:
- Version control systems (diff algorithms)
- DNA sequence analysis
- Plagiarism detection
*/

/// Naive recursive solution
/// Time: O(2^(m+n)), Space: O(m+n)
pub fn lcs_naive(s1: &str, s2: &str) -> usize {
    lcs_naive_helper(s1.as_bytes(), s2.as_bytes(), 0, 0)
}

fn lcs_naive_helper(s1: &[u8], s2: &[u8], i: usize, j: usize) -> usize {
    if i == s1.len() || j == s2.len() {
        return 0;
    }

    if s1[i] == s2[j] {
        1 + lcs_naive_helper(s1, s2, i + 1, j + 1)
    } else {
        max(
            lcs_naive_helper(s1, s2, i + 1, j),
            lcs_naive_helper(s1, s2, i, j + 1),
        )
    }
}

/// Memoized solution
/// Time: O(m*n), Space: O(m*n)
pub fn lcs_memoized(s1: &str, s2: &str) -> usize {
    let mut memo = HashMap::new();
    lcs_memoized_helper(s1.as_bytes(), s2.as_bytes(), 0, 0, &mut memo)
}

fn lcs_memoized_helper(
    s1: &[u8],
    s2: &[u8],
    i: usize,
    j: usize,
    memo: &mut HashMap<(usize, usize), usize>,
) -> usize {
    if i == s1.len() || j == s2.len() {
        return 0;
    }

    if let Some(&result) = memo.get(&(i, j)) {
        return result;
    }

    let result = if s1[i] == s2[j] {
        1 + lcs_memoized_helper(s1, s2, i + 1, j + 1, memo)
    } else {
        max(
            lcs_memoized_helper(s1, s2, i + 1, j, memo),
            lcs_memoized_helper(s1, s2, i, j + 1, memo),
        )
    };

    memo.insert((i, j), result);
    result
}

/// Tabulated solution
/// Time: O(m*n), Space: O(m*n)
pub fn lcs_tabulated(s1: &str, s2: &str) -> usize {
    let s1 = s1.as_bytes();
    let s2 = s2.as_bytes();
    let m = s1.len();
    let n = s2.len();
    let mut dp = vec![vec![0; n + 1]; m + 1];

    for i in 1..=m {
        for j in 1..=n {
            if s1[i - 1] == s2[j - 1] {
                dp[i][j] = 1 + dp[i - 1][j - 1];
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    dp[m][n]
}

/// Space-optimized solution
/// Time: O(m*n), Space: O(min(m, n))
pub fn lcs_space_optimized(s1: &str, s2: &str) -> usize {
    let (s1, s2) = if s1.len() < s2.len() {
        (s2, s1)
    } else {
        (s1, s2)
    };

    let s1 = s1.as_bytes();
    let s2 = s2.as_bytes();
    let n = s2.len();
    let mut prev = vec![0; n + 1];
    let mut curr = vec![0; n + 1];

    for i in 1..=s1.len() {
        for j in 1..=n {
            if s1[i - 1] == s2[j - 1] {
                curr[j] = 1 + prev[j - 1];
            } else {
                curr[j] = max(prev[j], curr[j - 1]);
            }
        }
        std::mem::swap(&mut prev, &mut curr);
    }

    prev[n]
}

// ============================================================================
// 2. LONGEST INCREASING SUBSEQUENCE (LIS)
// ============================================================================

/*
Problem: Find the length of the longest strictly increasing subsequence.

Real-world applications:
- Stock market trend analysis
- Task scheduling
*/

/// Naive recursive solution
/// Time: O(2^n), Space: O(n)
pub fn lis_naive(arr: &[i32]) -> usize {
    lis_naive_helper(arr, 0, i32::MIN)
}

fn lis_naive_helper(arr: &[i32], idx: usize, prev: i32) -> usize {
    if idx == arr.len() {
        return 0;
    }

    let exclude = lis_naive_helper(arr, idx + 1, prev);
    let include = if arr[idx] > prev {
        1 + lis_naive_helper(arr, idx + 1, arr[idx])
    } else {
        0
    };

    max(exclude, include)
}

/// Tabulated O(n^2) solution
/// Time: O(n^2), Space: O(n)
pub fn lis_tabulated(arr: &[i32]) -> usize {
    if arr.is_empty() {
        return 0;
    }

    let n = arr.len();
    let mut dp = vec![1; n];

    for i in 1..n {
        for j in 0..i {
            if arr[j] < arr[i] {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
    }

    *dp.iter().max().unwrap()
}

/// Optimized solution using binary search
/// Time: O(n log n), Space: O(n)
pub fn lis_optimized(arr: &[i32]) -> usize {
    if arr.is_empty() {
        return 0;
    }

    let mut tails = Vec::new();

    for &num in arr {
        let pos = tails.binary_search(&num).unwrap_or_else(|e| e);
        if pos == tails.len() {
            tails.push(num);
        } else {
            tails[pos] = num;
        }
    }

    tails.len()
}

// ============================================================================
// 3. EDIT DISTANCE (LEVENSHTEIN DISTANCE)
// ============================================================================

/*
Problem: Minimum operations (insert, delete, replace) to convert s1 to s2.

Real-world applications:
- Spell checkers
- DNA sequence alignment
- Autocorrect systems
*/

/// Naive recursive solution
/// Time: O(3^max(m,n)), Space: O(max(m, n))
pub fn edit_distance_naive(s1: &str, s2: &str) -> usize {
    edit_distance_naive_helper(s1.as_bytes(), s2.as_bytes(), s1.len(), s2.len())
}

fn edit_distance_naive_helper(s1: &[u8], s2: &[u8], i: usize, j: usize) -> usize {
    if i == 0 {
        return j;
    }
    if j == 0 {
        return i;
    }

    if s1[i - 1] == s2[j - 1] {
        return edit_distance_naive_helper(s1, s2, i - 1, j - 1);
    }

    1 + min(
        min(
            edit_distance_naive_helper(s1, s2, i, j - 1),     // insert
            edit_distance_naive_helper(s1, s2, i - 1, j),     // delete
        ),
        edit_distance_naive_helper(s1, s2, i - 1, j - 1), // replace
    )
}

/// Memoized solution
/// Time: O(m*n), Space: O(m*n)
pub fn edit_distance_memoized(s1: &str, s2: &str) -> usize {
    let mut memo = HashMap::new();
    edit_distance_memoized_helper(
        s1.as_bytes(),
        s2.as_bytes(),
        s1.len(),
        s2.len(),
        &mut memo,
    )
}

fn edit_distance_memoized_helper(
    s1: &[u8],
    s2: &[u8],
    i: usize,
    j: usize,
    memo: &mut HashMap<(usize, usize), usize>,
) -> usize {
    if i == 0 {
        return j;
    }
    if j == 0 {
        return i;
    }

    if let Some(&result) = memo.get(&(i, j)) {
        return result;
    }

    let result = if s1[i - 1] == s2[j - 1] {
        edit_distance_memoized_helper(s1, s2, i - 1, j - 1, memo)
    } else {
        1 + min(
            min(
                edit_distance_memoized_helper(s1, s2, i, j - 1, memo),
                edit_distance_memoized_helper(s1, s2, i - 1, j, memo),
            ),
            edit_distance_memoized_helper(s1, s2, i - 1, j - 1, memo),
        )
    };

    memo.insert((i, j), result);
    result
}

/// Tabulated solution
/// Time: O(m*n), Space: O(m*n)
pub fn edit_distance_tabulated(s1: &str, s2: &str) -> usize {
    let s1 = s1.as_bytes();
    let s2 = s2.as_bytes();
    let m = s1.len();
    let n = s2.len();
    let mut dp = vec![vec![0; n + 1]; m + 1];

    for i in 0..=m {
        dp[i][0] = i;
    }
    for j in 0..=n {
        dp[0][j] = j;
    }

    for i in 1..=m {
        for j in 1..=n {
            if s1[i - 1] == s2[j - 1] {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + min(min(dp[i][j - 1], dp[i - 1][j]), dp[i - 1][j - 1]);
            }
        }
    }

    dp[m][n]
}

/// Space-optimized solution
/// Time: O(m*n), Space: O(min(m, n))
pub fn edit_distance_space_optimized(s1: &str, s2: &str) -> usize {
    let (s1, s2) = if s1.len() < s2.len() {
        (s2, s1)
    } else {
        (s1, s2)
    };

    let s1 = s1.as_bytes();
    let s2 = s2.as_bytes();
    let n = s2.len();
    let mut prev: Vec<usize> = (0..=n).collect();
    let mut curr = vec![0; n + 1];

    for i in 1..=s1.len() {
        curr[0] = i;
        for j in 1..=n {
            if s1[i - 1] == s2[j - 1] {
                curr[j] = prev[j - 1];
            } else {
                curr[j] = 1 + min(min(curr[j - 1], prev[j]), prev[j - 1]);
            }
        }
        std::mem::swap(&mut prev, &mut curr);
    }

    prev[n]
}

// ============================================================================
// 4. COIN CHANGE PROBLEM
// ============================================================================

/*
Problem: Find minimum coins needed or count ways to make change.

Real-world applications:
- Vending machines
- Currency exchange
*/

/// Naive recursive - minimum coins
/// Time: O(amount^len(coins)), Space: O(amount)
pub fn coin_change_min_naive(coins: &[i32], amount: i32) -> i32 {
    let result = coin_change_min_naive_helper(coins, amount);
    if result == i32::MAX {
        -1
    } else {
        result
    }
}

fn coin_change_min_naive_helper(coins: &[i32], remaining: i32) -> i32 {
    if remaining == 0 {
        return 0;
    }
    if remaining < 0 {
        return i32::MAX;
    }

    let mut min_coins = i32::MAX;
    for &coin in coins {
        let result = coin_change_min_naive_helper(coins, remaining - coin);
        if result != i32::MAX {
            min_coins = min(min_coins, result + 1);
        }
    }

    min_coins
}

/// Memoized - minimum coins
/// Time: O(amount * len(coins)), Space: O(amount)
pub fn coin_change_min_memoized(coins: &[i32], amount: i32) -> i32 {
    let mut memo = HashMap::new();
    let result = coin_change_min_memoized_helper(coins, amount, &mut memo);
    if result == i32::MAX {
        -1
    } else {
        result
    }
}

fn coin_change_min_memoized_helper(
    coins: &[i32],
    remaining: i32,
    memo: &mut HashMap<i32, i32>,
) -> i32 {
    if remaining == 0 {
        return 0;
    }
    if remaining < 0 {
        return i32::MAX;
    }

    if let Some(&result) = memo.get(&remaining) {
        return result;
    }

    let mut min_coins = i32::MAX;
    for &coin in coins {
        let result = coin_change_min_memoized_helper(coins, remaining - coin, memo);
        if result != i32::MAX {
            min_coins = min(min_coins, result + 1);
        }
    }

    memo.insert(remaining, min_coins);
    min_coins
}

/// Tabulated - minimum coins
/// Time: O(amount * len(coins)), Space: O(amount)
pub fn coin_change_min_tabulated(coins: &[i32], amount: i32) -> i32 {
    let amount = amount as usize;
    let mut dp = vec![i32::MAX; amount + 1];
    dp[0] = 0;

    for i in 1..=amount {
        for &coin in coins {
            let coin = coin as usize;
            if coin <= i && dp[i - coin] != i32::MAX {
                dp[i] = min(dp[i], dp[i - coin] + 1);
            }
        }
    }

    if dp[amount] == i32::MAX {
        -1
    } else {
        dp[amount]
    }
}

/// Count number of ways to make change
/// Time: O(amount * len(coins)), Space: O(amount)
pub fn coin_change_ways_tabulated(coins: &[i32], amount: i32) -> i32 {
    let amount = amount as usize;
    let mut dp = vec![0; amount + 1];
    dp[0] = 1;

    for &coin in coins {
        let coin = coin as usize;
        for i in coin..=amount {
            dp[i] += dp[i - coin];
        }
    }

    dp[amount]
}

// ============================================================================
// 5. KNAPSACK PROBLEMS
// ============================================================================

/*
Problem: Maximize value within weight capacity.

Real-world applications:
- Resource allocation
- Portfolio optimization
*/

/// 0/1 Knapsack - Naive recursive
/// Time: O(2^n), Space: O(n)
pub fn knapsack_01_naive(weights: &[i32], values: &[i32], capacity: i32) -> i32 {
    knapsack_01_naive_helper(weights, values, capacity, 0)
}

fn knapsack_01_naive_helper(weights: &[i32], values: &[i32], capacity: i32, idx: usize) -> i32 {
    if idx == weights.len() || capacity == 0 {
        return 0;
    }

    let skip = knapsack_01_naive_helper(weights, values, capacity, idx + 1);
    let take = if weights[idx] <= capacity {
        values[idx] + knapsack_01_naive_helper(weights, values, capacity - weights[idx], idx + 1)
    } else {
        0
    };

    max(skip, take)
}

/// 0/1 Knapsack - Tabulated
/// Time: O(n * capacity), Space: O(n * capacity)
pub fn knapsack_01_tabulated(weights: &[i32], values: &[i32], capacity: i32) -> i32 {
    let n = weights.len();
    let capacity = capacity as usize;
    let mut dp = vec![vec![0; capacity + 1]; n + 1];

    for i in 1..=n {
        for w in 0..=capacity {
            dp[i][w] = dp[i - 1][w];
            let weight = weights[i - 1] as usize;
            if weight <= w {
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weight] + values[i - 1]);
            }
        }
    }

    dp[n][capacity]
}

/// 0/1 Knapsack - Space optimized
/// Time: O(n * capacity), Space: O(capacity)
pub fn knapsack_01_space_optimized(weights: &[i32], values: &[i32], capacity: i32) -> i32 {
    let capacity = capacity as usize;
    let mut dp = vec![0; capacity + 1];

    for i in 0..weights.len() {
        let weight = weights[i] as usize;
        for w in (weight..=capacity).rev() {
            dp[w] = max(dp[w], dp[w - weight] + values[i]);
        }
    }

    dp[capacity]
}

/// Unbounded Knapsack
/// Time: O(n * capacity), Space: O(capacity)
pub fn knapsack_unbounded_tabulated(weights: &[i32], values: &[i32], capacity: i32) -> i32 {
    let capacity = capacity as usize;
    let mut dp = vec![0; capacity + 1];

    for w in 1..=capacity {
        for i in 0..weights.len() {
            let weight = weights[i] as usize;
            if weight <= w {
                dp[w] = max(dp[w], dp[w - weight] + values[i]);
            }
        }
    }

    dp[capacity]
}

// ============================================================================
// 6. MATRIX CHAIN MULTIPLICATION
// ============================================================================

/*
Problem: Find optimal parenthesization to minimize multiplications.

Real-world applications:
- Compiler optimization
- Database query optimization
*/

/// Naive recursive solution
/// Time: O(2^n), Space: O(n)
pub fn matrix_chain_naive(dims: &[i32]) -> i32 {
    matrix_chain_naive_helper(dims, 1, dims.len() - 1)
}

fn matrix_chain_naive_helper(dims: &[i32], i: usize, j: usize) -> i32 {
    if i == j {
        return 0;
    }

    let mut min_cost = i32::MAX;
    for k in i..j {
        let cost = matrix_chain_naive_helper(dims, i, k)
            + matrix_chain_naive_helper(dims, k + 1, j)
            + dims[i - 1] * dims[k] * dims[j];
        min_cost = min(min_cost, cost);
    }

    min_cost
}

/// Memoized solution
/// Time: O(n^3), Space: O(n^2)
pub fn matrix_chain_memoized(dims: &[i32]) -> i32 {
    let mut memo = HashMap::new();
    matrix_chain_memoized_helper(dims, 1, dims.len() - 1, &mut memo)
}

fn matrix_chain_memoized_helper(
    dims: &[i32],
    i: usize,
    j: usize,
    memo: &mut HashMap<(usize, usize), i32>,
) -> i32 {
    if i == j {
        return 0;
    }

    if let Some(&result) = memo.get(&(i, j)) {
        return result;
    }

    let mut min_cost = i32::MAX;
    for k in i..j {
        let cost = matrix_chain_memoized_helper(dims, i, k, memo)
            + matrix_chain_memoized_helper(dims, k + 1, j, memo)
            + dims[i - 1] * dims[k] * dims[j];
        min_cost = min(min_cost, cost);
    }

    memo.insert((i, j), min_cost);
    min_cost
}

/// Tabulated solution
/// Time: O(n^3), Space: O(n^2)
pub fn matrix_chain_tabulated(dims: &[i32]) -> i32 {
    let n = dims.len();
    let mut dp = vec![vec![0; n]; n];

    for length in 2..n {
        for i in 1..n - length + 1 {
            let j = i + length - 1;
            dp[i][j] = i32::MAX;

            for k in i..j {
                let cost = dp[i][k] + dp[k + 1][j] + dims[i - 1] * dims[k] * dims[j];
                dp[i][j] = min(dp[i][j], cost);
            }
        }
    }

    dp[1][n - 1]
}

// ============================================================================
// 7. PALINDROME PROBLEMS
// ============================================================================

/*
Real-world applications:
- DNA sequence analysis
- Text processing
*/

/// Longest palindromic subsequence - Tabulated
/// Time: O(n^2), Space: O(n^2)
pub fn longest_palindrome_subsequence_tabulated(s: &str) -> usize {
    let s = s.as_bytes();
    let n = s.len();
    let mut dp = vec![vec![0; n]; n];

    for i in 0..n {
        dp[i][i] = 1;
    }

    for length in 2..=n {
        for i in 0..n - length + 1 {
            let j = i + length - 1;

            if s[i] == s[j] {
                dp[i][j] = 2 + if i + 1 <= j - 1 { dp[i + 1][j - 1] } else { 0 };
            } else {
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1]);
            }
        }
    }

    dp[0][n - 1]
}

/// Count palindromic substrings
/// Time: O(n^2), Space: O(1)
pub fn count_palindromic_substrings(s: &str) -> usize {
    let s = s.as_bytes();
    let mut total = 0;

    for i in 0..s.len() {
        total += expand_around_center(s, i as i32, i as i32);      // odd length
        total += expand_around_center(s, i as i32, (i + 1) as i32); // even length
    }

    total
}

fn expand_around_center(s: &[u8], mut left: i32, mut right: i32) -> usize {
    let mut count = 0;
    while left >= 0 && (right as usize) < s.len() && s[left as usize] == s[right as usize] {
        count += 1;
        left -= 1;
        right += 1;
    }
    count
}

/// Minimum insertions to make palindrome
/// Time: O(n^2), Space: O(n^2)
pub fn min_insertions_palindrome(s: &str) -> usize {
    s.len() - longest_palindrome_subsequence_tabulated(s)
}

/// Minimum cuts for palindrome partitioning
/// Time: O(n^2), Space: O(n^2)
pub fn palindrome_partitioning_min_cuts(s: &str) -> usize {
    let s = s.as_bytes();
    let n = s.len();

    let mut is_palindrome = vec![vec![false; n]; n];
    for i in 0..n {
        is_palindrome[i][i] = true;
    }

    for length in 2..=n {
        for i in 0..n - length + 1 {
            let j = i + length - 1;
            if s[i] == s[j] {
                is_palindrome[i][j] = (length == 2) || is_palindrome[i + 1][j - 1];
            }
        }
    }

    let mut dp = vec![usize::MAX; n];
    for i in 0..n {
        if is_palindrome[0][i] {
            dp[i] = 0;
        } else {
            for j in 0..i {
                if is_palindrome[j + 1][i] {
                    dp[i] = min(dp[i], dp[j] + 1);
                }
            }
        }
    }

    dp[n - 1]
}

// ============================================================================
// 8. MAXIMUM SUBARRAY SUM (KADANE'S ALGORITHM)
// ============================================================================

/*
Problem: Find contiguous subarray with maximum sum.

Real-world applications:
- Stock market analysis
- Signal processing
*/

/// Naive solution - check all subarrays
/// Time: O(n^2), Space: O(1)
pub fn max_subarray_naive(arr: &[i32]) -> i32 {
    if arr.is_empty() {
        return 0;
    }

    let mut max_sum = i32::MIN;
    for i in 0..arr.len() {
        let mut current_sum = 0;
        for j in i..arr.len() {
            current_sum += arr[j];
            max_sum = max(max_sum, current_sum);
        }
    }

    max_sum
}

/// Kadane's Algorithm - optimal
/// Time: O(n), Space: O(1)
pub fn max_subarray_kadane(arr: &[i32]) -> i32 {
    if arr.is_empty() {
        return 0;
    }

    let mut max_sum = arr[0];
    let mut current_sum = arr[0];

    for &num in &arr[1..] {
        current_sum = max(num, current_sum + num);
        max_sum = max(max_sum, current_sum);
    }

    max_sum
}

/// Subarray result with indices
#[derive(Debug)]
pub struct SubarrayResult {
    pub max_sum: i32,
    pub start: usize,
    pub end: usize,
}

/// Kadane's with indices
/// Time: O(n), Space: O(1)
pub fn max_subarray_with_indices(arr: &[i32]) -> SubarrayResult {
    if arr.is_empty() {
        return SubarrayResult {
            max_sum: 0,
            start: 0,
            end: 0,
        };
    }

    let mut max_sum = arr[0];
    let mut current_sum = arr[0];
    let mut start = 0;
    let mut end = 0;
    let mut temp_start = 0;

    for i in 1..arr.len() {
        if arr[i] > current_sum + arr[i] {
            current_sum = arr[i];
            temp_start = i;
        } else {
            current_sum = current_sum + arr[i];
        }

        if current_sum > max_sum {
            max_sum = current_sum;
            start = temp_start;
            end = i;
        }
    }

    SubarrayResult {
        max_sum,
        start,
        end,
    }
}

/// Maximum subarray in circular array
/// Time: O(n), Space: O(1)
pub fn max_subarray_circular(arr: &[i32]) -> i32 {
    if arr.is_empty() {
        return 0;
    }

    let max_normal = max_subarray_kadane(arr);
    if max_normal < 0 {
        return max_normal;
    }

    let total_sum: i32 = arr.iter().sum();
    let min_sum = kadane_min(arr);
    let max_circular = total_sum - min_sum;

    max(max_normal, max_circular)
}

fn kadane_min(arr: &[i32]) -> i32 {
    let mut min_sum = arr[0];
    let mut current_sum = arr[0];
    for &num in &arr[1..] {
        current_sum = min(num, current_sum + num);
        min_sum = min(min_sum, current_sum);
    }
    min_sum
}

// ============================================================================
// MAIN - EXAMPLE USAGE AND TESTING
// ============================================================================

fn main() {
    println!("{}", "=".repeat(70));
    println!("DYNAMIC PROGRAMMING CLASSIC PROBLEMS - EXAMPLES");
    println!("{}", "=".repeat(70));

    // LCS Examples
    println!("\n1. Longest Common Subsequence:");
    let s1 = "ABCDGH";
    let s2 = "AEDFHR";
    println!("   Strings: '{}', '{}'", s1, s2);
    println!("   Naive: {}", lcs_naive(s1, s2));
    println!("   Memoized: {}", lcs_memoized(s1, s2));
    println!("   Tabulated: {}", lcs_tabulated(s1, s2));
    println!("   Space-optimized: {}", lcs_space_optimized(s1, s2));

    // LIS Examples
    println!("\n2. Longest Increasing Subsequence:");
    let arr1 = vec![10, 9, 2, 5, 3, 7, 101, 18];
    println!("   Array: {:?}", arr1);
    println!("   Naive: {}", lis_naive(&arr1));
    println!("   Tabulated O(n^2): {}", lis_tabulated(&arr1));
    println!("   Optimized O(n log n): {}", lis_optimized(&arr1));

    // Edit Distance
    println!("\n3. Edit Distance:");
    let str1 = "kitten";
    let str2 = "sitting";
    println!("   Strings: '{}', '{}'", str1, str2);
    println!("   Naive: {}", edit_distance_naive(str1, str2));
    println!("   Memoized: {}", edit_distance_memoized(str1, str2));
    println!("   Tabulated: {}", edit_distance_tabulated(str1, str2));
    println!("   Space-optimized: {}", edit_distance_space_optimized(str1, str2));

    // Coin Change
    println!("\n4. Coin Change:");
    let coins = vec![1, 2, 5];
    let amount = 11;
    println!("   Coins: {:?}, Amount: {}", coins, amount);
    println!("   Min coins (naive): {}", coin_change_min_naive(&coins, amount));
    println!("   Min coins (memoized): {}", coin_change_min_memoized(&coins, amount));
    println!("   Min coins (tabulated): {}", coin_change_min_tabulated(&coins, amount));
    println!("   Ways to make change: {}", coin_change_ways_tabulated(&coins, amount));

    // Knapsack
    println!("\n5. Knapsack Problem:");
    let weights = vec![1, 3, 4, 5];
    let values = vec![1, 4, 5, 7];
    let capacity = 7;
    println!("   Weights: {:?}, Values: {:?}, Capacity: {}", weights, values, capacity);
    println!("   0/1 Naive: {}", knapsack_01_naive(&weights, &values, capacity));
    println!("   0/1 Tabulated: {}", knapsack_01_tabulated(&weights, &values, capacity));
    println!("   0/1 Space-optimized: {}", knapsack_01_space_optimized(&weights, &values, capacity));
    println!("   Unbounded: {}", knapsack_unbounded_tabulated(&weights, &values, capacity));

    // Matrix Chain
    println!("\n6. Matrix Chain Multiplication:");
    let dims = vec![10, 20, 30, 40, 30];
    println!("   Dimensions: {:?}", dims);
    println!("   Naive: {}", matrix_chain_naive(&dims));
    println!("   Memoized: {}", matrix_chain_memoized(&dims));
    println!("   Tabulated: {}", matrix_chain_tabulated(&dims));

    // Palindromes
    println!("\n7. Palindrome Problems:");
    let p_str = "bbbab";
    println!("   String: '{}'", p_str);
    println!("   Longest palindromic subsequence: {}",
             longest_palindrome_subsequence_tabulated(p_str));
    println!("   Count palindromic substrings: {}",
             count_palindromic_substrings(p_str));
    println!("   Min insertions for palindrome: {}",
             min_insertions_palindrome(p_str));
    println!("   Min cuts for palindrome partition: {}",
             palindrome_partitioning_min_cuts(p_str));

    // Maximum Subarray
    println!("\n8. Maximum Subarray Sum:");
    let arr2 = vec![-2, 1, -3, 4, -1, 2, 1, -5, 4];
    println!("   Array: {:?}", arr2);
    println!("   Naive: {}", max_subarray_naive(&arr2));
    println!("   Kadane's: {}", max_subarray_kadane(&arr2));
    let result = max_subarray_with_indices(&arr2);
    println!("   With indices: sum={}, range=[{}:{}]",
             result.max_sum, result.start, result.end + 1);

    let arr_circular = vec![5, -3, 5];
    println!("   Circular array: {:?}", arr_circular);
    println!("   Max circular sum: {}", max_subarray_circular(&arr_circular));

    println!("\n{}", "=".repeat(70));
}
