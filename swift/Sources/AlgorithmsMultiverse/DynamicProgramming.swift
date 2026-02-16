import Foundation

// MARK: - Dynamic Programming Algorithms

public struct DynamicProgramming {

    // MARK: - Fibonacci

    /// Fibonacci number (memoized)
    /// - Complexity: O(n) time, O(n) space
    public static func fibonacci(_ n: Int) -> Int {
        var memo: [Int: Int] = [:]

        func fib(_ n: Int) -> Int {
            if n <= 1 { return n }

            if let cached = memo[n] {
                return cached
            }

            let result = fib(n - 1) + fib(n - 2)
            memo[n] = result
            return result
        }

        return fib(n)
    }

    /// Fibonacci number (iterative)
    /// - Complexity: O(n) time, O(1) space
    public static func fibonacciIterative(_ n: Int) -> Int {
        if n <= 1 { return n }

        var prev = 0
        var curr = 1

        for _ in 2...n {
            let next = prev + curr
            prev = curr
            curr = next
        }

        return curr
    }

    /// Generate Fibonacci sequence
    public static func fibonacciSequence(count: Int) -> [Int] {
        guard count > 0 else { return [] }
        if count == 1 { return [0] }

        var sequence = [0, 1]
        for i in 2..<count {
            sequence.append(sequence[i - 1] + sequence[i - 2])
        }

        return Array(sequence.prefix(count))
    }

    // MARK: - Longest Common Subsequence

    /// LCS with backtracking
    /// - Complexity: O(mn) time and space
    public static func longestCommonSubsequence(_ text1: String, _ text2: String) -> (length: Int, lcs: String) {
        let m = text1.count
        let n = text2.count
        let arr1 = Array(text1)
        let arr2 = Array(text2)

        var dp = Array(repeating: Array(repeating: 0, count: n + 1), count: m + 1)

        // Fill DP table
        for i in 1...m {
            for j in 1...n {
                if arr1[i - 1] == arr2[j - 1] {
                    dp[i][j] = dp[i - 1][j - 1] + 1
                } else {
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                }
            }
        }

        // Backtrack to find LCS
        var lcs = ""
        var i = m, j = n

        while i > 0 && j > 0 {
            if arr1[i - 1] == arr2[j - 1] {
                lcs = String(arr1[i - 1]) + lcs
                i -= 1
                j -= 1
            } else if dp[i - 1][j] > dp[i][j - 1] {
                i -= 1
            } else {
                j -= 1
            }
        }

        return (dp[m][n], lcs)
    }

    // MARK: - Longest Increasing Subsequence

    /// LIS using DP
    /// - Complexity: O(n²) time, O(n) space
    public static func longestIncreasingSubsequence<T: Comparable>(_ array: [T]) -> (length: Int, sequence: [T]) {
        guard !array.isEmpty else { return (0, []) }

        let n = array.count
        var dp = Array(repeating: 1, count: n)
        var parent = Array(repeating: -1, count: n)

        for i in 1..<n {
            for j in 0..<i {
                if array[j] < array[i] && dp[j] + 1 > dp[i] {
                    dp[i] = dp[j] + 1
                    parent[i] = j
                }
            }
        }

        // Find maximum length and its index
        var maxLength = 0
        var maxIndex = 0
        for i in 0..<n {
            if dp[i] > maxLength {
                maxLength = dp[i]
                maxIndex = i
            }
        }

        // Reconstruct sequence
        var sequence: [T] = []
        var current = maxIndex
        while current != -1 {
            sequence.append(array[current])
            current = parent[current]
        }

        return (maxLength, sequence.reversed())
    }

    /// LIS using binary search
    /// - Complexity: O(n log n) time, O(n) space
    public static func lisOptimized<T: Comparable>(_ array: [T]) -> Int {
        guard !array.isEmpty else { return 0 }

        var tails: [T] = []

        for num in array {
            if tails.isEmpty || num > tails.last! {
                tails.append(num)
            } else {
                // Binary search for insertion position
                var left = 0
                var right = tails.count - 1

                while left < right {
                    let mid = (left + right) / 2
                    if tails[mid] < num {
                        left = mid + 1
                    } else {
                        right = mid
                    }
                }

                tails[left] = num
            }
        }

        return tails.count
    }

    // MARK: - Edit Distance

    /// Levenshtein distance with operations
    /// - Complexity: O(mn) time and space
    public static func editDistance(_ word1: String, _ word2: String) -> (distance: Int, operations: [String]) {
        let m = word1.count
        let n = word2.count
        let arr1 = Array(word1)
        let arr2 = Array(word2)

        var dp = Array(repeating: Array(repeating: 0, count: n + 1), count: m + 1)

        // Initialize base cases
        for i in 0...m {
            dp[i][0] = i
        }
        for j in 0...n {
            dp[0][j] = j
        }

        // Fill DP table
        for i in 1...m {
            for j in 1...n {
                if arr1[i - 1] == arr2[j - 1] {
                    dp[i][j] = dp[i - 1][j - 1]
                } else {
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],     // Delete
                        dp[i][j - 1],     // Insert
                        dp[i - 1][j - 1]  // Replace
                    )
                }
            }
        }

        // Backtrack to find operations
        var operations: [String] = []
        var i = m, j = n

        while i > 0 || j > 0 {
            if i > 0 && j > 0 && arr1[i - 1] == arr2[j - 1] {
                i -= 1
                j -= 1
            } else if i > 0 && (j == 0 || dp[i - 1][j] <= dp[i][j - 1] && dp[i - 1][j] <= dp[i - 1][j - 1]) {
                operations.append("Delete '\(arr1[i - 1])' at position \(i)")
                i -= 1
            } else if j > 0 && (i == 0 || dp[i][j - 1] < dp[i - 1][j] && dp[i][j - 1] <= dp[i - 1][j - 1]) {
                operations.append("Insert '\(arr2[j - 1])' at position \(i + 1)")
                j -= 1
            } else if i > 0 && j > 0 {
                operations.append("Replace '\(arr1[i - 1])' with '\(arr2[j - 1])' at position \(i)")
                i -= 1
                j -= 1
            }
        }

        return (dp[m][n], operations.reversed())
    }

    // MARK: - Knapsack Problems

    /// 0/1 Knapsack with item tracking
    /// - Complexity: O(nW) time, O(W) space optimized
    public static func knapsack01(
        weights: [Int],
        values: [Int],
        capacity: Int
    ) -> (maxValue: Int, items: [Int]) {
        let n = weights.count
        var dp = Array(repeating: Array(repeating: 0, count: capacity + 1), count: n + 1)

        // Fill DP table
        for i in 1...n {
            for w in 1...capacity {
                if weights[i - 1] <= w {
                    dp[i][w] = max(
                        dp[i - 1][w],
                        values[i - 1] + dp[i - 1][w - weights[i - 1]]
                    )
                } else {
                    dp[i][w] = dp[i - 1][w]
                }
            }
        }

        // Backtrack to find selected items
        var items: [Int] = []
        var w = capacity

        for i in stride(from: n, through: 1, by: -1) {
            if dp[i][w] != dp[i - 1][w] {
                items.append(i - 1)
                w -= weights[i - 1]
            }
        }

        return (dp[n][capacity], items.reversed())
    }

    /// Unbounded knapsack
    /// - Complexity: O(nW) time, O(W) space
    public static func unboundedKnapsack(
        weights: [Int],
        values: [Int],
        capacity: Int
    ) -> Int {
        var dp = Array(repeating: 0, count: capacity + 1)

        for w in 1...capacity {
            for i in 0..<weights.count {
                if weights[i] <= w {
                    dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
                }
            }
        }

        return dp[capacity]
    }

    // MARK: - Coin Change

    /// Minimum coins for amount
    /// - Complexity: O(amount * n) time, O(amount) space
    public static func coinChange(_ coins: [Int], _ amount: Int) -> (minCoins: Int, combination: [Int: Int]?) {
        var dp = Array(repeating: amount + 1, count: amount + 1)
        var parent = Array(repeating: -1, count: amount + 1)
        dp[0] = 0

        for i in 1...amount {
            for j in 0..<coins.count {
                if coins[j] <= i && dp[i - coins[j]] + 1 < dp[i] {
                    dp[i] = dp[i - coins[j]] + 1
                    parent[i] = j
                }
            }
        }

        if dp[amount] > amount {
            return (-1, nil)
        }

        // Reconstruct coin combination
        var combination: [Int: Int] = [:]
        var current = amount

        while current > 0 {
            let coinIndex = parent[current]
            let coin = coins[coinIndex]
            combination[coin, default: 0] += 1
            current -= coin
        }

        return (dp[amount], combination)
    }

    /// Number of ways to make amount
    /// - Complexity: O(amount * n) time, O(amount) space
    public static func coinChangeWays(_ coins: [Int], _ amount: Int) -> Int {
        var dp = Array(repeating: 0, count: amount + 1)
        dp[0] = 1

        for coin in coins {
            for i in coin...amount {
                dp[i] += dp[i - coin]
            }
        }

        return dp[amount]
    }

    // MARK: - Maximum Subarray

    /// Kadane's algorithm with indices
    /// - Complexity: O(n) time, O(1) space
    public static func maxSubarray(_ array: [Int]) -> (sum: Int, start: Int, end: Int) {
        guard !array.isEmpty else { return (0, -1, -1) }

        var maxSum = array[0]
        var currentSum = array[0]
        var maxStart = 0
        var maxEnd = 0
        var currentStart = 0

        for i in 1..<array.count {
            if currentSum < 0 {
                currentSum = array[i]
                currentStart = i
            } else {
                currentSum += array[i]
            }

            if currentSum > maxSum {
                maxSum = currentSum
                maxStart = currentStart
                maxEnd = i
            }
        }

        return (maxSum, maxStart, maxEnd)
    }

    /// Maximum product subarray
    /// - Complexity: O(n) time, O(1) space
    public static func maxProductSubarray(_ array: [Int]) -> Int {
        guard !array.isEmpty else { return 0 }

        var maxProduct = array[0]
        var minSoFar = array[0]
        var maxSoFar = array[0]

        for i in 1..<array.count {
            let temp = maxSoFar
            maxSoFar = max(array[i], max(maxSoFar * array[i], minSoFar * array[i]))
            minSoFar = min(array[i], min(temp * array[i], minSoFar * array[i]))
            maxProduct = max(maxProduct, maxSoFar)
        }

        return maxProduct
    }

    // MARK: - Matrix Chain Multiplication

    /// Minimum scalar multiplications
    /// - Complexity: O(n³) time, O(n²) space
    public static func matrixChainMultiplication(_ dimensions: [Int]) -> (minOps: Int, order: String) {
        let n = dimensions.count - 1
        var dp = Array(repeating: Array(repeating: 0, count: n), count: n)
        var split = Array(repeating: Array(repeating: 0, count: n), count: n)

        // Length of chain
        for len in 2...n {
            for i in 0...(n - len) {
                let j = i + len - 1
                dp[i][j] = Int.max

                for k in i..<j {
                    let ops = dp[i][k] + dp[k + 1][j] +
                              dimensions[i] * dimensions[k + 1] * dimensions[j + 1]

                    if ops < dp[i][j] {
                        dp[i][j] = ops
                        split[i][j] = k
                    }
                }
            }
        }

        // Reconstruct parenthesization
        func buildOrder(_ i: Int, _ j: Int) -> String {
            if i == j {
                return "M\(i + 1)"
            }
            let k = split[i][j]
            return "(\(buildOrder(i, k)) × \(buildOrder(k + 1, j)))"
        }

        return (dp[0][n - 1], buildOrder(0, n - 1))
    }

    // MARK: - Longest Palindromic Substring

    /// Find longest palindrome in string
    /// - Complexity: O(n²) time and space
    public static func longestPalindromicSubstring(_ s: String) -> String {
        guard !s.isEmpty else { return "" }

        let chars = Array(s)
        let n = chars.count
        var dp = Array(repeating: Array(repeating: false, count: n), count: n)
        var maxLen = 1
        var start = 0

        // Single characters are palindromes
        for i in 0..<n {
            dp[i][i] = true
        }

        // Check for two-character palindromes
        for i in 0..<n - 1 {
            if chars[i] == chars[i + 1] {
                dp[i][i + 1] = true
                maxLen = 2
                start = i
            }
        }

        // Check for palindromes of length 3 or more
        for len in 3...n {
            for i in 0...(n - len) {
                let j = i + len - 1

                if chars[i] == chars[j] && dp[i + 1][j - 1] {
                    dp[i][j] = true
                    if len > maxLen {
                        maxLen = len
                        start = i
                    }
                }
            }
        }

        return String(chars[start..<(start + maxLen)])
    }

    /// Longest palindromic subsequence
    /// - Complexity: O(n²) time and space
    public static func longestPalindromicSubsequence(_ s: String) -> Int {
        let chars = Array(s)
        let n = chars.count
        var dp = Array(repeating: Array(repeating: 0, count: n), count: n)

        for i in 0..<n {
            dp[i][i] = 1
        }

        for len in 2...n {
            for i in 0...(n - len) {
                let j = i + len - 1

                if chars[i] == chars[j] {
                    dp[i][j] = dp[i + 1][j - 1] + 2
                } else {
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
                }
            }
        }

        return dp[0][n - 1]
    }

    // MARK: - House Robber

    /// Maximum money from non-adjacent houses
    /// - Complexity: O(n) time, O(1) space
    public static func houseRobber(_ houses: [Int]) -> Int {
        guard !houses.isEmpty else { return 0 }
        if houses.count == 1 { return houses[0] }

        var prev = houses[0]
        var curr = max(houses[0], houses[1])

        for i in 2..<houses.count {
            let temp = curr
            curr = max(curr, prev + houses[i])
            prev = temp
        }

        return curr
    }

    /// House robber in circle (first and last connected)
    public static func houseRobberCircle(_ houses: [Int]) -> Int {
        guard !houses.isEmpty else { return 0 }
        if houses.count == 1 { return houses[0] }
        if houses.count == 2 { return max(houses[0], houses[1]) }

        // Rob houses 0 to n-2
        let rob1 = robRange(houses, 0, houses.count - 2)
        // Rob houses 1 to n-1
        let rob2 = robRange(houses, 1, houses.count - 1)

        return max(rob1, rob2)
    }

    private static func robRange(_ houses: [Int], _ start: Int, _ end: Int) -> Int {
        var prev = 0
        var curr = 0

        for i in start...end {
            let temp = curr
            curr = max(curr, prev + houses[i])
            prev = temp
        }

        return curr
    }

    // MARK: - Partition Problems

    /// Check if array can be partitioned into equal sum subsets
    /// - Complexity: O(n * sum) time, O(sum) space
    public static func canPartition(_ nums: [Int]) -> Bool {
        let total = nums.reduce(0, +)
        if total % 2 != 0 { return false }

        let target = total / 2
        var dp = Array(repeating: false, count: target + 1)
        dp[0] = true

        for num in nums {
            for i in stride(from: target, through: num, by: -1) {
                dp[i] = dp[i] || dp[i - num]
            }
        }

        return dp[target]
    }

    // MARK: - Word Break

    /// Check if string can be segmented into dictionary words
    /// - Complexity: O(n² * m) where m is average word length
    public static func wordBreak(_ s: String, _ wordDict: Set<String>) -> Bool {
        let n = s.count
        var dp = Array(repeating: false, count: n + 1)
        dp[0] = true

        for i in 1...n {
            for j in 0..<i {
                if dp[j] {
                    let start = s.index(s.startIndex, offsetBy: j)
                    let end = s.index(s.startIndex, offsetBy: i)
                    let substring = String(s[start..<end])

                    if wordDict.contains(substring) {
                        dp[i] = true
                        break
                    }
                }
            }
        }

        return dp[n]
    }

    /// Get all possible word break solutions
    public static func wordBreakAll(_ s: String, _ wordDict: Set<String>) -> [String] {
        var memo: [String: [String]] = [:]

        func helper(_ s: String) -> [String] {
            if let cached = memo[s] {
                return cached
            }

            if s.isEmpty {
                return [""]
            }

            var result: [String] = []

            for word in wordDict {
                if s.hasPrefix(word) {
                    let suffix = String(s.dropFirst(word.count))
                    let suffixBreaks = helper(suffix)

                    for suffixBreak in suffixBreaks {
                        if suffixBreak.isEmpty {
                            result.append(word)
                        } else {
                            result.append("\(word) \(suffixBreak)")
                        }
                    }
                }
            }

            memo[s] = result
            return result
        }

        return helper(s)
    }

    // MARK: - Climbing Stairs

    /// Number of ways to climb n stairs (1 or 2 steps at a time)
    /// - Complexity: O(n) time, O(1) space
    public static func climbStairs(_ n: Int) -> Int {
        if n <= 2 { return n }

        var prev = 1
        var curr = 2

        for _ in 3...n {
            let next = prev + curr
            prev = curr
            curr = next
        }

        return curr
    }

    /// Number of ways with variable steps
    public static func climbStairsWithSteps(_ n: Int, steps: [Int]) -> Int {
        var dp = Array(repeating: 0, count: n + 1)
        dp[0] = 1

        for i in 1...n {
            for step in steps {
                if step <= i {
                    dp[i] += dp[i - step]
                }
            }
        }

        return dp[n]
    }

    // MARK: - Stock Trading

    /// Best time to buy and sell stock (single transaction)
    /// - Complexity: O(n) time, O(1) space
    public static func maxProfit(_ prices: [Int]) -> Int {
        guard !prices.isEmpty else { return 0 }

        var minPrice = prices[0]
        var maxProfit = 0

        for price in prices {
            minPrice = min(minPrice, price)
            maxProfit = max(maxProfit, price - minPrice)
        }

        return maxProfit
    }

    /// Best time with multiple transactions
    public static func maxProfitUnlimited(_ prices: [Int]) -> Int {
        var profit = 0

        for i in 1..<prices.count {
            if prices[i] > prices[i - 1] {
                profit += prices[i] - prices[i - 1]
            }
        }

        return profit
    }

    /// Best time with at most k transactions
    public static func maxProfitKTransactions(_ prices: [Int], _ k: Int) -> Int {
        guard !prices.isEmpty else { return 0 }

        let n = prices.count
        if k >= n / 2 {
            return maxProfitUnlimited(prices)
        }

        var buy = Array(repeating: -prices[0], count: k + 1)
        var sell = Array(repeating: 0, count: k + 1)

        for price in prices {
            for j in stride(from: k, through: 1, by: -1) {
                sell[j] = max(sell[j], buy[j] + price)
                buy[j] = max(buy[j], sell[j - 1] - price)
            }
        }

        return sell[k]
    }
}