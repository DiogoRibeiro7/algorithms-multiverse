# ==============================================================================
# String Algorithms in R
#
# Pattern matching and text processing algorithms.
#
# Implementations:
# - Naive String Matching
# - Knuth-Morris-Pratt (KMP) Algorithm
# - Rabin-Karp Algorithm
# - Boyer-Moore Algorithm
# - Longest Palindromic Substring
# - String Hashing
#
# Run: Rscript string_algorithms.R
#
# @author Algorithms Multiverse
# @version 1.0
# ==============================================================================

# ==============================================================================
# Naive String Matching
# ==============================================================================

#' Naive String Matching
#'
#' Time Complexity: O((n-m+1) × m) where n = text length, m = pattern length
#' Space Complexity: O(1)
#'
#' @param text Input text
#' @param pattern Pattern to search
#' @return Vector of starting positions (1-indexed)
naive_search <- function(text, pattern) {
  n <- nchar(text)
  m <- nchar(pattern)
  positions <- integer(0)

  for (i in 1:(n - m + 1)) {
    if (substr(text, i, i + m - 1) == pattern) {
      positions <- c(positions, i)
    }
  }

  positions
}

# ==============================================================================
# Knuth-Morris-Pratt (KMP) Algorithm
# ==============================================================================

#' Compute KMP Failure Function
#'
#' @param pattern Pattern string
#' @return Failure function array
compute_lps <- function(pattern) {
  m <- nchar(pattern)
  lps <- rep(0, m)
  length <- 0
  i <- 2

  pattern_chars <- strsplit(pattern, "")[[1]]

  while (i <= m) {
    if (pattern_chars[i] == pattern_chars[length + 1]) {
      length <- length + 1
      lps[i] <- length
      i <- i + 1
    } else {
      if (length != 0) {
        length <- lps[length]
      } else {
        lps[i] <- 0
        i <- i + 1
      }
    }
  }

  lps
}

#' KMP String Matching
#'
#' Time Complexity: O(n + m)
#' Space Complexity: O(m)
#'
#' Applications:
#' - Text editors (find/replace)
#' - Intrusion detection systems
#' - Biological sequence matching
#'
#' @param text Input text
#' @param pattern Pattern to search
#' @return Vector of starting positions
kmp_search <- function(text, pattern) {
  n <- nchar(text)
  m <- nchar(pattern)

  lps <- compute_lps(pattern)
  positions <- integer(0)

  text_chars <- strsplit(text, "")[[1]]
  pattern_chars <- strsplit(pattern, "")[[1]]

  i <- 1  # Index for text
  j <- 1  # Index for pattern

  while (i <= n) {
    if (pattern_chars[j] == text_chars[i]) {
      i <- i + 1
      j <- j + 1
    }

    if (j > m) {
      positions <- c(positions, i - m)
      j <- lps[j - 1] + 1
    } else if (i <= n && pattern_chars[j] != text_chars[i]) {
      if (j != 1) {
        j <- lps[j - 1] + 1
      } else {
        i <- i + 1
      }
    }
  }

  positions
}

# ==============================================================================
# Rabin-Karp Algorithm (Rolling Hash)
# ==============================================================================

#' Rabin-Karp String Matching
#'
#' Time Complexity: O(n + m) average, O(nm) worst case
#' Space Complexity: O(1)
#'
#' Uses rolling hash for efficient pattern matching
#'
#' Applications:
#' - Plagiarism detection
#' - Multiple pattern search
#' - Document similarity
#'
#' @param text Input text
#' @param pattern Pattern to search
#' @param d Number of characters in alphabet (default: 256)
#' @param q Prime modulus (default: 101)
#' @return Vector of starting positions
rabin_karp_search <- function(text, pattern, d = 256, q = 101) {
  n <- nchar(text)
  m <- nchar(pattern)
  positions <- integer(0)

  # Convert to integer codes
  text_codes <- utf8ToInt(text)
  pattern_codes <- utf8ToInt(pattern)

  # Calculate hash value for pattern and first window
  h <- 1
  for (i in 1:(m - 1)) {
    h <- (h * d) %% q
  }

  p <- 0  # Hash value for pattern
  t <- 0  # Hash value for text window

  for (i in 1:m) {
    p <- (d * p + pattern_codes[i]) %% q
    t <- (d * t + text_codes[i]) %% q
  }

  # Slide pattern over text
  for (i in 0:(n - m)) {
    # Check if hash values match
    if (p == t) {
      # Verify character by character
      if (substr(text, i + 1, i + m) == pattern) {
        positions <- c(positions, i + 1)
      }
    }

    # Calculate hash for next window
    if (i < n - m) {
      t <- (d * (t - text_codes[i + 1] * h) + text_codes[i + m + 1]) %% q
      if (t < 0) {
        t <- t + q
      }
    }
  }

  positions
}

# ==============================================================================
# Longest Palindromic Substring (Manacher's Algorithm simplified)
# ==============================================================================

#' Longest Palindromic Substring
#'
#' Time Complexity: O(n²) for this DP version
#' Space Complexity: O(n²)
#'
#' Applications:
#' - Bioinformatics (DNA sequences)
#' - Text processing
#' - Pattern recognition
#'
#' @param s Input string
#' @return Longest palindromic substring
longest_palindrome <- function(s) {
  n <- nchar(s)
  if (n == 0) return("")

  # DP table: dp[i, j] = is substring s[i:j] a palindrome?
  dp <- matrix(FALSE, nrow = n, ncol = n)

  max_length <- 1
  start <- 1

  # All single characters are palindromes
  diag(dp) <- TRUE

  # Check for length 2
  for (i in 1:(n - 1)) {
    if (substr(s, i, i) == substr(s, i + 1, i + 1)) {
      dp[i, i + 1] <- TRUE
      start <- i
      max_length <- 2
    }
  }

  # Check for lengths > 2
  for (length in 3:n) {
    for (i in 1:(n - length + 1)) {
      j <- i + length - 1

      if (substr(s, i, i) == substr(s, j, j) && dp[i + 1, j - 1]) {
        dp[i, j] <- TRUE
        start <- i
        max_length <- length
      }
    }
  }

  substr(s, start, start + max_length - 1)
}

# ==============================================================================
# String Hashing (Polynomial Rolling Hash)
# ==============================================================================

#' Polynomial Rolling Hash
#'
#' Time Complexity: O(n)
#' Space Complexity: O(1)
#'
#' Applications:
#' - Hash tables for strings
#' - Fast string comparison
#' - Duplicate detection
#'
#' @param s Input string
#' @param p Base (default: 31 for lowercase letters)
#' @param m Modulus (default: 1e9 + 9)
#' @return Hash value
string_hash <- function(s, p = 31, m = 1e9 + 9) {
  n <- nchar(s)
  hash_value <- 0
  p_pow <- 1

  chars <- utf8ToInt(s)

  for (i in 1:n) {
    hash_value <- (hash_value + chars[i] * p_pow) %% m
    p_pow <- (p_pow * p) %% m
  }

  hash_value
}

# ==============================================================================
# String Distance Metrics
# ==============================================================================

#' Hamming Distance
#'
#' Number of positions where strings differ
#'
#' Time Complexity: O(n)
#'
#' @param s1 First string
#' @param s2 Second string
#' @return Hamming distance
hamming_distance <- function(s1, s2) {
  if (nchar(s1) != nchar(s2)) {
    stop("Strings must be same length for Hamming distance")
  }

  chars1 <- strsplit(s1, "")[[1]]
  chars2 <- strsplit(s2, "")[[1]]

  sum(chars1 != chars2)
}

# ==============================================================================
# Main Program - Examples and Tests
# ==============================================================================

cat("==============================================================================\n")
cat("                STRING ALGORITHMS IN R\n")
cat("           Pattern Matching & Text Processing\n")
cat("==============================================================================\n\n")

# Example 1: KMP vs Naive Search
cat("Example 1: Pattern Matching (KMP vs Naive)\n")
cat(strrep("=", 80), "\n")
text <- "ABABDABACDABABCABAB"
pattern <- "ABABCABAB"

positions_naive <- naive_search(text, pattern)
positions_kmp <- kmp_search(text, pattern)

cat(sprintf("Text: %s\n", text))
cat(sprintf("Pattern: %s\n", pattern))
cat(sprintf("Naive search found at: %s\n", paste(positions_naive, collapse = ", ")))
cat(sprintf("KMP search found at: %s\n\n", paste(positions_kmp, collapse = ", ")))

# Example 2: Rabin-Karp
cat("Example 2: Rabin-Karp (Rolling Hash)\n")
cat(strrep("=", 80), "\n")
text <- "GEEKS FOR GEEKS"
pattern <- "GEEKS"

positions <- rabin_karp_search(text, pattern)
cat(sprintf("Text: %s\n", text))
cat(sprintf("Pattern: %s\n", pattern))
cat(sprintf("Found at positions: %s\n\n", paste(positions, collapse = ", ")))

# Example 3: Longest Palindrome
cat("Example 3: Longest Palindromic Substring\n")
cat(strrep("=", 80), "\n")
s <- "babad"
palindrome <- longest_palindrome(s)
cat(sprintf("String: %s\n", s))
cat(sprintf("Longest palindrome: %s\n\n", palindrome))

# Example 4: String Hashing
cat("Example 4: String Hashing\n")
cat(strrep("=", 80), "\n")
strings <- c("hello", "world", "hello", "testing")
cat("String hashes:\n")
for (s in strings) {
  hash <- string_hash(s)
  cat(sprintf("  %-10s -> %d\n", s, hash))
}
cat("\nNote: 'hello' has same hash (duplicate detected)\n\n")

# Example 5: Hamming Distance
cat("Example 5: Hamming Distance\n")
cat(strrep("=", 80), "\n")
s1 <- "karolin"
s2 <- "kathrin"
distance <- hamming_distance(s1, s2)
cat(sprintf("String 1: %s\n", s1))
cat(sprintf("String 2: %s\n", s2))
cat(sprintf("Hamming distance: %d\n\n", distance))

# Summary
cat(strrep("=", 80), "\n")
cat("Summary: R String Algorithm Capabilities\n")
cat(strrep("=", 80), "\n")
cat("✓ Naive Search: O(nm) - Simple baseline\n")
cat("✓ KMP: O(n+m) - Optimal worst-case pattern matching\n")
cat("✓ Rabin-Karp: O(n+m) average - Rolling hash for efficiency\n")
cat("✓ Longest Palindrome: O(n²) - DP approach\n")
cat("✓ String Hashing: Fast comparison and duplicate detection\n")
cat("\nApplications:\n")
cat("- Text editors (search/replace)\n")
cat("- Bioinformatics (DNA/protein sequence analysis)\n")
cat("- Plagiarism detection\n")
cat("- Data deduplication\n")
cat(strrep("=", 80), "\n")
