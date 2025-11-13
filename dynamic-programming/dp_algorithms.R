# ==============================================================================
# Dynamic Programming Algorithms in R
#
# Comprehensive collection of classic DP problems.
# R's matrix operations make DP table management particularly efficient!
#
# Implementations:
# - 0/1 Knapsack Problem
# - Unbounded Knapsack
# - Longest Common Subsequence (LCS)
# - Edit Distance (Levenshtein)
# - Coin Change Problem
# - Matrix Chain Multiplication
# - Longest Increasing Subsequence (LIS)
# - Subset Sum Problem
#
# Run: Rscript dp_algorithms.R
#
# @author Algorithms Multiverse
# @version 1.0
# ==============================================================================

# ==============================================================================
# 0/1 Knapsack Problem
# ==============================================================================

#' 0/1 Knapsack Problem
#'
#' Maximize value of items in knapsack with weight capacity
#'
#' Time Complexity: O(n × W) where n = items, W = capacity
#' Space Complexity: O(n × W)
#'
#' Applications:
#' - Resource allocation
#' - Portfolio optimization
#' - Cargo loading
#'
#' @param values Item values (vector)
#' @param weights Item weights (vector)
#' @param capacity Knapsack capacity
#' @return List with max_value and selected items
knapsack_01 <- function(values, weights, capacity) {
  n <- length(values)

  # DP table: dp[i, w] = max value using first i items with capacity w
  dp <- matrix(0, nrow = n + 1, ncol = capacity + 1)

  # Fill DP table
  for (i in 1:n) {
    for (w in 0:capacity) {
      # Don't take item i
      dp[i + 1, w + 1] <- dp[i, w + 1]

      # Take item i (if it fits)
      if (weights[i] <= w) {
        dp[i + 1, w + 1] <- max(
          dp[i + 1, w + 1],
          dp[i, w - weights[i] + 1] + values[i]
        )
      }
    }
  }

  # Backtrack to find selected items
  selected <- logical(n)
  w <- capacity
  for (i in n:1) {
    if (dp[i + 1, w + 1] != dp[i, w + 1]) {
      selected[i] <- TRUE
      w <- w - weights[i]
    }
  }

  list(
    max_value = dp[n + 1, capacity + 1],
    selected_items = which(selected)
  )
}

# ==============================================================================
# Unbounded Knapsack
# ==============================================================================

#' Unbounded Knapsack Problem
#'
#' Items can be selected multiple times
#'
#' Time Complexity: O(n × W)
#' Space Complexity: O(W)
#'
#' @param values Item values
#' @param weights Item weights
#' @param capacity Knapsack capacity
#' @return Maximum value achievable
knapsack_unbounded <- function(values, weights, capacity) {
  n <- length(values)

  # DP array: dp[w] = max value with capacity w
  dp <- rep(0, capacity + 1)

  for (w in 1:capacity) {
    for (i in 1:n) {
      if (weights[i] <= w) {
        dp[w + 1] <- max(dp[w + 1], dp[w - weights[i] + 1] + values[i])
      }
    }
  }

  dp[capacity + 1]
}

# ==============================================================================
# Longest Common Subsequence (LCS)
# ==============================================================================

#' Longest Common Subsequence
#'
#' Find longest subsequence common to two sequences
#'
#' Time Complexity: O(m × n) where m, n = sequence lengths
#' Space Complexity: O(m × n)
#'
#' Applications:
#' - Diff utilities (git diff)
#' - Bioinformatics (DNA sequence alignment)
#' - Plagiarism detection
#'
#' @param x First sequence (character vector)
#' @param y Second sequence (character vector)
#' @return List with LCS length and the actual LCS
longest_common_subsequence <- function(x, y) {
  m <- length(x)
  n <- length(y)

  # DP table
  dp <- matrix(0, nrow = m + 1, ncol = n + 1)

  # Fill DP table
  for (i in 1:m) {
    for (j in 1:n) {
      if (x[i] == y[j]) {
        dp[i + 1, j + 1] <- dp[i, j] + 1
      } else {
        dp[i + 1, j + 1] <- max(dp[i, j + 1], dp[i + 1, j])
      }
    }
  }

  # Backtrack to find LCS
  lcs <- character(0)
  i <- m
  j <- n

  while (i > 0 && j > 0) {
    if (x[i] == y[j]) {
      lcs <- c(x[i], lcs)
      i <- i - 1
      j <- j - 1
    } else if (dp[i, j + 1] > dp[i + 1, j]) {
      i <- i - 1
    } else {
      j <- j - 1
    }
  }

  list(
    length = dp[m + 1, n + 1],
    sequence = lcs
  )
}

# ==============================================================================
# Edit Distance (Levenshtein Distance)
# ==============================================================================

#' Edit Distance (Levenshtein Distance)
#'
#' Minimum edits (insert, delete, substitute) to transform s1 to s2
#'
#' Time Complexity: O(m × n)
#' Space Complexity: O(m × n)
#'
#' Applications:
#' - Spell checking
#' - DNA sequence analysis
#' - Natural language processing
#' - Fuzzy string matching
#'
#' @param s1 First string
#' @param s2 Second string
#' @return Minimum edit distance
edit_distance <- function(s1, s2) {
  m <- nchar(s1)
  n <- nchar(s2)

  # Convert to character vectors
  chars1 <- strsplit(s1, "")[[1]]
  chars2 <- strsplit(s2, "")[[1]]

  # DP table: dp[i, j] = edit distance between s1[1:i] and s2[1:j]
  dp <- matrix(0, nrow = m + 1, ncol = n + 1)

  # Base cases
  dp[, 1] <- 0:m  # Delete all characters from s1
  dp[1, ] <- 0:n  # Insert all characters from s2

  # Fill DP table
  for (i in 1:m) {
    for (j in 1:n) {
      if (chars1[i] == chars2[j]) {
        dp[i + 1, j + 1] <- dp[i, j]  # No operation needed
      } else {
        dp[i + 1, j + 1] <- 1 + min(
          dp[i, j],      # Substitute
          dp[i + 1, j],  # Insert
          dp[i, j + 1]   # Delete
        )
      }
    }
  }

  dp[m + 1, n + 1]
}

# ==============================================================================
# Coin Change Problem
# ==============================================================================

#' Coin Change Problem
#'
#' Minimum coins needed to make amount
#'
#' Time Complexity: O(n × amount) where n = coin types
#' Space Complexity: O(amount)
#'
#' Applications:
#' - Making change
#' - Resource optimization
#' - Knapsack variants
#'
#' @param coins Available coin denominations
#' @param amount Target amount
#' @return Minimum number of coins needed
coin_change <- function(coins, amount) {
  # DP array: dp[i] = min coins needed for amount i
  dp <- rep(Inf, amount + 1)
  dp[1] <- 0  # Base case: 0 coins for amount 0

  for (i in 1:amount) {
    for (coin in coins) {
      if (i >= coin) {
        dp[i + 1] <- min(dp[i + 1], dp[i - coin + 1] + 1)
      }
    }
  }

  if (dp[amount + 1] == Inf) {
    return(-1)  # Cannot make amount
  }

  dp[amount + 1]
}

# ==============================================================================
# Matrix Chain Multiplication
# ==============================================================================

#' Matrix Chain Multiplication
#'
#' Find optimal parenthesization to minimize scalar multiplications
#'
#' Time Complexity: O(n³)
#' Space Complexity: O(n²)
#'
#' Example: (A₁ × A₂) × A₃ vs A₁ × (A₂ × A₃)
#' Different costs depending on matrix dimensions!
#'
#' Applications:
#' - Compiler optimization
#' - Computer graphics
#' - Query optimization in databases
#'
#' @param dims Dimensions vector [d₀, d₁, ..., dₙ]
#'        Matrix i has dimensions dᵢ₋₁ × dᵢ
#' @return Minimum scalar multiplications needed
matrix_chain_order <- function(dims) {
  n <- length(dims) - 1  # Number of matrices

  # DP table: m[i, j] = min cost to multiply matrices i..j
  m <- matrix(Inf, nrow = n, ncol = n)

  # Base case: single matrix has zero cost
  diag(m) <- 0

  # l = chain length
  for (l in 2:n) {
    for (i in 1:(n - l + 1)) {
      j <- i + l - 1

      # Try all split points
      for (k in i:(j - 1)) {
        # Cost = cost(i..k) + cost(k+1..j) + cost of multiplying results
        cost <- m[i, k] + m[k + 1, j] + dims[i] * dims[k + 1] * dims[j + 1]
        m[i, j] <- min(m[i, j], cost)
      }
    }
  }

  m[1, n]
}

# ==============================================================================
# Longest Increasing Subsequence (LIS)
# ==============================================================================

#' Longest Increasing Subsequence
#'
#' Find longest strictly increasing subsequence
#'
#' Time Complexity: O(n²) for DP, O(n log n) for binary search variant
#' Space Complexity: O(n)
#'
#' Applications:
#' - Patience sorting
#' - Stock market analysis
#' - Bioinformatics
#'
#' @param arr Input array
#' @return Length of LIS
longest_increasing_subsequence <- function(arr) {
  n <- length(arr)

  # DP array: lis[i] = length of LIS ending at index i
  lis <- rep(1, n)

  for (i in 2:n) {
    for (j in 1:(i - 1)) {
      if (arr[j] < arr[i]) {
        lis[i] <- max(lis[i], lis[j] + 1)
      }
    }
  }

  max(lis)
}

# ==============================================================================
# Subset Sum Problem
# ==============================================================================

#' Subset Sum Problem
#'
#' Determine if subset exists that sums to target
#'
#' Time Complexity: O(n × sum)
#' Space Complexity: O(n × sum)
#'
#' Applications:
#' - Partition problems
#' - Scheduling
#' - Cryptography
#'
#' @param arr Input array
#' @param target Target sum
#' @return TRUE if subset exists, FALSE otherwise
subset_sum <- function(arr, target) {
  n <- length(arr)

  # DP table: dp[i, s] = can we make sum s using first i elements?
  dp <- matrix(FALSE, nrow = n + 1, ncol = target + 1)
  dp[, 1] <- TRUE  # Can always make sum 0 (empty subset)

  for (i in 1:n) {
    for (s in 0:target) {
      # Don't include arr[i]
      dp[i + 1, s + 1] <- dp[i, s + 1]

      # Include arr[i]
      if (s >= arr[i]) {
        dp[i + 1, s + 1] <- dp[i + 1, s + 1] || dp[i, s - arr[i] + 1]
      }
    }
  }

  dp[n + 1, target + 1]
}

# ==============================================================================
# Main Program - Examples and Tests
# ==============================================================================

cat("==============================================================================\n")
cat("            DYNAMIC PROGRAMMING ALGORITHMS IN R\n")
cat("         Leveraging R's Efficient Matrix Operations\n")
cat("==============================================================================\n\n")

# Example 1: 0/1 Knapsack
cat("Example 1: 0/1 Knapsack Problem\n")
cat(strrep("=", 80), "\n")
values <- c(60, 100, 120)
weights <- c(10, 20, 30)
capacity <- 50
result <- knapsack_01(values, weights, capacity)
cat(sprintf("Values: %s\n", paste(values, collapse = ", ")))
cat(sprintf("Weights: %s\n", paste(weights, collapse = ", ")))
cat(sprintf("Capacity: %d\n", capacity))
cat(sprintf("Max value: %d\n", result$max_value))
cat(sprintf("Selected items: %s\n\n", paste(result$selected_items, collapse = ", ")))

# Example 2: Longest Common Subsequence
cat("Example 2: Longest Common Subsequence\n")
cat(strrep("=", 80), "\n")
x <- strsplit("AGGTAB", "")[[1]]
y <- strsplit("GXTXAYB", "")[[1]]
result <- longest_common_subsequence(x, y)
cat(sprintf("Sequence 1: %s\n", paste(x, collapse = "")))
cat(sprintf("Sequence 2: %s\n", paste(y, collapse = "")))
cat(sprintf("LCS length: %d\n", result$length))
cat(sprintf("LCS: %s\n\n", paste(result$sequence, collapse = "")))

# Example 3: Edit Distance
cat("Example 3: Edit Distance (Levenshtein)\n")
cat(strrep("=", 80), "\n")
s1 <- "kitten"
s2 <- "sitting"
distance <- edit_distance(s1, s2)
cat(sprintf("String 1: %s\n", s1))
cat(sprintf("String 2: %s\n", s2))
cat(sprintf("Edit distance: %d\n\n", distance))

# Example 4: Coin Change
cat("Example 4: Coin Change Problem\n")
cat(strrep("=", 80), "\n")
coins <- c(1, 5, 10, 25)
amount <- 63
min_coins <- coin_change(coins, amount)
cat(sprintf("Coins: %s\n", paste(coins, collapse = ", ")))
cat(sprintf("Amount: %d\n", amount))
cat(sprintf("Minimum coins needed: %d\n\n", min_coins))

# Example 5: Matrix Chain Multiplication
cat("Example 5: Matrix Chain Multiplication\n")
cat(strrep("=", 80), "\n")
dims <- c(10, 20, 30, 40, 30)
min_ops <- matrix_chain_order(dims)
cat(sprintf("Matrix dimensions: %s\n", paste(dims, collapse = " × ")))
cat(sprintf("Minimum scalar multiplications: %d\n\n", min_ops))

# Example 6: Longest Increasing Subsequence
cat("Example 6: Longest Increasing Subsequence\n")
cat(strrep("=", 80), "\n")
arr <- c(10, 9, 2, 5, 3, 7, 101, 18)
lis_length <- longest_increasing_subsequence(arr)
cat(sprintf("Array: %s\n", paste(arr, collapse = ", ")))
cat(sprintf("LIS length: %d\n\n", lis_length))

# Example 7: Subset Sum
cat("Example 7: Subset Sum Problem\n")
cat(strrep("=", 80), "\n")
arr <- c(3, 34, 4, 12, 5, 2)
target <- 9
exists <- subset_sum(arr, target)
cat(sprintf("Array: %s\n", paste(arr, collapse = ", ")))
cat(sprintf("Target sum: %d\n", target))
cat(sprintf("Subset exists: %s\n\n", exists))

# Summary
cat(strrep("=", 80), "\n")
cat("Summary: Dynamic Programming in R\n")
cat(strrep("=", 80), "\n")
cat("✓ R matrices make DP table management efficient\n")
cat("✓ Vectorized operations speed up computations\n")
cat("✓ Clear, readable implementations\n")
cat("\nApplications:\n")
cat("- Optimization problems (knapsack, coin change)\n")
cat("- Sequence analysis (LCS, edit distance)\n")
cat("- Bioinformatics (DNA alignment)\n")
cat("- NLP (text similarity, spell checking)\n")
cat(strrep("=", 80), "\n")
