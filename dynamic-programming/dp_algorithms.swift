/*
 * ==============================================================================
 * Dynamic Programming Algorithms in Swift
 *
 * Classic DP problems leveraging Swift's type safety and value semantics.
 *
 * Implementations:
 * - 0/1 Knapsack Problem
 * - Longest Common Subsequence (LCS)
 * - Edit Distance (Levenshtein)
 * - Coin Change Problem
 * - Longest Increasing Subsequence (LIS)
 *
 * Swift's arrays and tuples make DP state management elegant and efficient.
 *
 * Compile: swiftc -O dp_algorithms.swift
 * Run: ./dp_algorithms
 *
 * @author Algorithms Multiverse
 * @version 1.0
 * ==============================================================================
 */

import Foundation

// ==============================================================================
// 0/1 Knapsack Problem
// ==============================================================================

struct KnapsackResult {
    let maxValue: Int
    let selectedItems: [Int]
}

/// 0/1 Knapsack Problem
///
/// Time Complexity: O(n × W)
/// Space Complexity: O(n × W)
///
/// Applications:
/// - Resource allocation
/// - Portfolio optimization
/// - Cargo loading
func knapsack01(values: [Int], weights: [Int], capacity: Int) -> KnapsackResult {
    let n = values.count
    var dp = Array(repeating: Array(repeating: 0, count: capacity + 1), count: n + 1)

    // Fill DP table
    for i in 1...n {
        for w in 0...capacity {
            // Don't take item i-1
            dp[i][w] = dp[i-1][w]

            // Take item i-1 (if it fits)
            if weights[i-1] <= w {
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])
            }
        }
    }

    // Backtrack to find selected items
    var selectedItems = [Int]()
    var w = capacity
    for i in stride(from: n, to: 0, by: -1) {
        if dp[i][w] != dp[i-1][w] {
            selectedItems.append(i-1)
            w -= weights[i-1]
        }
    }

    return KnapsackResult(maxValue: dp[n][capacity], selectedItems: selectedItems.reversed())
}

// ==============================================================================
// Longest Common Subsequence (LCS)
// ==============================================================================

struct LCSResult {
    let length: Int
    let sequence: String
}

/// Longest Common Subsequence
///
/// Time Complexity: O(m × n)
/// Space Complexity: O(m × n)
///
/// Applications:
/// - Diff utilities (git diff)
/// - DNA sequence alignment
/// - Plagiarism detection
func longestCommonSubsequence(_ s1: String, _ s2: String) -> LCSResult {
    let m = s1.count
    let n = s2.count
    let chars1 = Array(s1)
    let chars2 = Array(s2)

    var dp = Array(repeating: Array(repeating: 0, count: n + 1), count: m + 1)

    // Fill DP table
    for i in 1...m {
        for j in 1...n {
            if chars1[i-1] == chars2[j-1] {
                dp[i][j] = dp[i-1][j-1] + 1
            } else {
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            }
        }
    }

    // Backtrack to find LCS
    var lcs = ""
    var i = m, j = n
    while i > 0 && j > 0 {
        if chars1[i-1] == chars2[j-1] {
            lcs = String(chars1[i-1]) + lcs
            i -= 1
            j -= 1
        } else if dp[i-1][j] > dp[i][j-1] {
            i -= 1
        } else {
            j -= 1
        }
    }

    return LCSResult(length: dp[m][n], sequence: lcs)
}

// ==============================================================================
// Edit Distance (Levenshtein Distance)
// ==============================================================================

/// Edit Distance (Levenshtein)
///
/// Time Complexity: O(m × n)
/// Space Complexity: O(m × n)
///
/// Applications:
/// - Spell checking
/// - DNA analysis
/// - Fuzzy string matching
func editDistance(_ s1: String, _ s2: String) -> Int {
    let m = s1.count
    let n = s2.count
    let chars1 = Array(s1)
    let chars2 = Array(s2)

    var dp = Array(repeating: Array(repeating: 0, count: n + 1), count: m + 1)

    // Base cases
    for i in 0...m { dp[i][0] = i }
    for j in 0...n { dp[0][j] = j }

    // Fill DP table
    for i in 1...m {
        for j in 1...n {
            if chars1[i-1] == chars2[j-1] {
                dp[i][j] = dp[i-1][j-1]
            } else {
                dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])
            }
        }
    }

    return dp[m][n]
}

// ==============================================================================
// Coin Change Problem
// ==============================================================================

/// Coin Change Problem
///
/// Time Complexity: O(n × amount)
/// Space Complexity: O(amount)
///
/// Applications:
/// - Making change
/// - Resource optimization
func coinChange(coins: [Int], amount: Int) -> Int {
    var dp = Array(repeating: Int.max, count: amount + 1)
    dp[0] = 0

    for i in 1...amount {
        for coin in coins where i >= coin {
            if dp[i - coin] != Int.max {
                dp[i] = min(dp[i], dp[i - coin] + 1)
            }
        }
    }

    return dp[amount] == Int.max ? -1 : dp[amount]
}

// ==============================================================================
// Longest Increasing Subsequence (LIS)
// ==============================================================================

/// Longest Increasing Subsequence
///
/// Time Complexity: O(n²)
/// Space Complexity: O(n)
///
/// Applications:
/// - Stock market analysis
/// - Patience sorting
func longestIncreasingSubsequence(_ arr: [Int]) -> Int {
    let n = arr.count
    guard n > 0 else { return 0 }

    var lis = Array(repeating: 1, count: n)

    for i in 1..<n {
        for j in 0..<i {
            if arr[j] < arr[i] {
                lis[i] = max(lis[i], lis[j] + 1)
            }
        }
    }

    return lis.max() ?? 0
}

// ==============================================================================
// Main Program - Examples and Tests
// ==============================================================================

print("==============================================================================")
print("            DYNAMIC PROGRAMMING ALGORITHMS IN SWIFT")
print("         Type-Safe DP with Swift's Modern Features")
print("==============================================================================\n")

// Example 1: 0/1 Knapsack
print("Example 1: 0/1 Knapsack Problem")
print(String(repeating: "=", count: 80))

let values = [60, 100, 120]
let weights = [10, 20, 30]
let capacity = 50

let knapsackResult = knapsack01(values: values, weights: weights, capacity: capacity)
print("Values:", values.map { String($0) }.joined(separator: ", "))
print("Weights:", weights.map { String($0) }.joined(separator: ", "))
print("Capacity:", capacity)
print("Max value:", knapsackResult.maxValue)
print("Selected items:", knapsackResult.selectedItems.map { String($0) }.joined(separator: ", "))
print()

// Example 2: Longest Common Subsequence
print("Example 2: Longest Common Subsequence")
print(String(repeating: "=", count: 80))

let s1 = "AGGTAB"
let s2 = "GXTXAYB"

let lcsResult = longestCommonSubsequence(s1, s2)
print("Sequence 1:", s1)
print("Sequence 2:", s2)
print("LCS length:", lcsResult.length)
print("LCS:", lcsResult.sequence)
print()

// Example 3: Edit Distance
print("Example 3: Edit Distance (Levenshtein)")
print(String(repeating: "=", count: 80))

let str1 = "kitten"
let str2 = "sitting"

let distance = editDistance(str1, str2)
print("String 1:", str1)
print("String 2:", str2)
print("Edit distance:", distance)
print()

// Example 4: Coin Change
print("Example 4: Coin Change Problem")
print(String(repeating: "=", count: 80))

let coins = [1, 5, 10, 25]
let targetAmount = 63

let minCoins = coinChange(coins: coins, amount: targetAmount)
print("Coins:", coins.map { String($0) }.joined(separator: ", "))
print("Amount:", targetAmount)
print("Minimum coins needed:", minCoins)
print()

// Example 5: Longest Increasing Subsequence
print("Example 5: Longest Increasing Subsequence")
print(String(repeating: "=", count: 80))

let arr = [10, 9, 2, 5, 3, 7, 101, 18]
let lisLength = longestIncreasingSubsequence(arr)

print("Array:", arr.map { String($0) }.joined(separator: ", "))
print("LIS length:", lisLength)
print()

// Summary
print(String(repeating: "=", count: 80))
print("Summary: Swift Dynamic Programming")
print(String(repeating: "=", count: 80))
print("✓ Type-safe DP table management")
print("✓ Value semantics for safety")
print("✓ Clean, idiomatic Swift code")
print("\nApplications:")
print("- Optimization problems")
print("- Sequence analysis")
print("- Bioinformatics")
print("- Text processing")
print(String(repeating: "=", count: 80))
