# Selection Sort Algorithm - Educational Implementation (R)
#
# ALGORITHM OVERVIEW:
# ==================
# Selection Sort works by repeatedly finding the minimum element from the unsorted
# portion of the array and placing it at the beginning. It divides the array into
# two parts: a sorted portion (left) and an unsorted portion (right).
#
# Time Complexity:
# - Best Case: O(n²) - Even if array is already sorted, still searches for minimum
# - Average Case: O(n²)
# - Worst Case: O(n²)
# - IMPORTANT: Unlike bubble sort and insertion sort, selection sort ALWAYS performs
#   O(n²) comparisons, regardless of input
#
# Space Complexity: O(1) for in-place, O(n) for functional approach
#
# Stability: NOT stable by default (can be made stable with modifications)
# In-place: YES (when modifying passed vector)
#
# KEY ADVANTAGE: Makes MINIMUM number of swaps - only O(n) swaps!
# This is critical when writing to memory is expensive (flash, EEPROM, etc.)

# ============================================================================
# STANDARD SELECTION SORT
# ============================================================================

#' Standard selection sort implementation.
#'
#' ALGORITHM STEPS:
#' ===============
#' 1. Find the minimum element in the unsorted portion
#' 2. Swap it with the first element of the unsorted portion
#' 3. Move the boundary of sorted/unsorted portions one element to the right
#' 4. Repeat until the entire array is sorted
#'
#' Visual Example:
#' ==============
#' Initial: [64, 25, 12, 22, 11]
#'
#' Pass 1: Find min in [64, 25, 12, 22, 11] → 11
#'         Swap 64 ↔ 11
#'         Result: [11, 25, 12, 22, 64]
#'                  ^^^ sorted portion
#'
#' Pass 2: Find min in [25, 12, 22, 64] → 12
#'         Swap 25 ↔ 12
#'         Result: [11, 12, 25, 22, 64]
#'                  ^^^^^^^ sorted portion
#'
#' Time: O(n²), Space: O(n) for new vector
#'
#' @param arr Vector to sort
#' @return A new sorted vector
selection_sort <- function(arr) {
  if (length(arr) <= 1) return(arr)

  result <- arr
  n <- length(result)

  # Outer loop: Move boundary of unsorted subarray one by one
  for (i in 1:(n-1)) {
    # Find the minimum element in the remaining unsorted array
    # Start by assuming the first unsorted element is the minimum
    min_idx <- i

    # Inner loop: Search for the minimum in arr[(i+1):n]
    if (i < n) {
      for (j in (i+1):n) {
        # If we find a smaller element, update min_idx
        if (result[j] < result[min_idx]) {
          min_idx <- j
        }
      }
    }

    # Swap the found minimum element with the first element
    # of the unsorted portion (only if different)
    if (min_idx != i) {
      temp <- result[i]
      result[i] <- result[min_idx]
      result[min_idx] <- temp
    }
  }

  return(result)
}

# ============================================================================
# BIDIRECTIONAL SELECTION SORT
# ============================================================================

#' Bidirectional selection sort (also called "double selection sort").
#'
#' OPTIMIZATION:
#' ============
#' Instead of finding just the minimum in each pass, we find BOTH the minimum
#' and maximum elements. We place the minimum at the beginning and the maximum
#' at the end, reducing the number of passes by approximately half.
#'
#' Time: Still O(n²), but approximately 2x faster in practice
#'
#' @param arr Vector to sort
#' @return A new sorted vector
bidirectional_selection_sort <- function(arr) {
  if (length(arr) <= 1) return(arr)

  result <- arr
  n <- length(result)

  # Process from both ends toward the middle
  left <- 1
  right <- n

  while (left < right) {
    # Find both minimum and maximum in the current range
    min_idx <- left
    max_idx <- left

    for (i in left:right) {
      if (result[i] < result[min_idx]) {
        min_idx <- i
      }
      if (result[i] > result[max_idx]) {
        max_idx <- i
      }
    }

    # Handle special case: if min is at right position
    if (min_idx == right) {
      temp <- result[left]
      result[left] <- result[right]
      result[right] <- temp
      if (max_idx == left) {
        max_idx <- right
      }
    } else {
      # Swap minimum to the left boundary
      if (min_idx != left) {
        temp <- result[left]
        result[left] <- result[min_idx]
        result[min_idx] <- temp
      }

      # If maximum was at left position, it's now at min_idx
      if (max_idx == left) {
        max_idx <- min_idx
      }

      # Swap maximum to the right boundary
      if (max_idx != right) {
        temp <- result[right]
        result[right] <- result[max_idx]
        result[max_idx] <- temp
      }
    }

    # Move boundaries inward
    left <- left + 1
    right <- right - 1
  }

  return(result)
}

# ============================================================================
# RECURSIVE SELECTION SORT
# ============================================================================

#' Recursive implementation of selection sort.
#'
#' RECURSIVE APPROACH:
#' ==================
#' Base case: Array of size 0 or 1 is already sorted
#' Recursive case:
#'     1. Find the minimum element in the array
#'     2. Swap it with the first element
#'     3. Recursively sort the rest of the array (excluding the first element)
#'
#' Time: O(n²), Space: O(n) for recursion stack
#'
#' @param arr Vector to sort
#' @param start_idx Starting index (default 1)
#' @return A new sorted vector
selection_sort_recursive <- function(arr, start_idx = 1) {
  n <- length(arr)

  # Base case: if we've reached the end, we're done
  if (start_idx >= n) return(arr)

  # Find the minimum element in arr[start_idx:n]
  min_idx <- start_idx
  if (start_idx < n) {
    for (i in (start_idx+1):n) {
      if (arr[i] < arr[min_idx]) {
        min_idx <- i
      }
    }
  }

  # Swap the minimum with the element at start_idx
  if (min_idx != start_idx) {
    temp <- arr[start_idx]
    arr[start_idx] <- arr[min_idx]
    arr[min_idx] <- temp
  }

  # Recursively sort the rest
  return(selection_sort_recursive(arr, start_idx + 1))
}

# ============================================================================
# STABLE SELECTION SORT
# ============================================================================

#' Stable version of selection sort.
#'
#' WHY STANDARD SELECTION SORT IS UNSTABLE:
#' ========================================
#' When we swap the minimum element with the first element of the unsorted
#' portion, we can change the relative order of equal elements.
#'
#' MAKING IT STABLE:
#' ================
#' Instead of swapping, we shift all elements and insert the minimum
#' at the correct position. This preserves the relative order.
#'
#' Time: O(n²) comparisons + O(n²) shifts
#'
#' @param arr Vector to sort
#' @return A new sorted vector
stable_selection_sort <- function(arr) {
  if (length(arr) <= 1) return(arr)

  result <- arr
  n <- length(result)

  for (i in 1:(n-1)) {
    # Find minimum in unsorted portion
    min_idx <- i
    if (i < n) {
      for (j in (i+1):n) {
        if (result[j] < result[min_idx]) {
          min_idx <- j
        }
      }
    }

    # Instead of swapping, shift elements and insert
    if (min_idx != i) {
      min_value <- result[min_idx]
      # Shift all elements between i and min_idx one position right
      if (min_idx > i) {
        for (k in min_idx:i) {
          if (k > i) {
            result[k] <- result[k-1]
          }
        }
      }
      # Place minimum at position i
      result[i] <- min_value
    }
  }

  return(result)
}

# ============================================================================
# VISUALIZATION AND STATISTICS
# ============================================================================

#' Create a visualization of selection sort process
#'
#' @param arr Vector to visualize
#' @return List of strings showing each step
visualize_selection_sort <- function(arr) {
  steps <- character()
  result <- arr
  n <- length(result)

  steps <- c(steps, paste(rep("=", 70), collapse=""))
  steps <- c(steps, "SELECTION SORT VISUALIZATION")
  steps <- c(steps, paste(rep("=", 70), collapse=""))
  steps <- c(steps, paste("Initial array:", paste(result, collapse=", ")))
  steps <- c(steps, "")

  for (i in 1:(n-1)) {
    steps <- c(steps, paste("Pass", i, ":"))
    unsorted <- result[i:n]
    steps <- c(steps, paste("  Looking for minimum in unsorted portion:",
                           paste(unsorted, collapse=", ")))

    min_idx <- i
    min_value <- result[i]

    # Show the search process
    if (i < n) {
      for (j in (i+1):n) {
        if (result[j] < min_value) {
          min_idx <- j
          min_value <- result[j]
          steps <- c(steps, paste("    Found new minimum:", min_value,
                                 "at index", min_idx))
        }
      }
    }

    # Show the swap
    if (min_idx != i) {
      steps <- c(steps, paste("  Swapping", result[i], "↔", result[min_idx]))
      temp <- result[i]
      result[i] <- result[min_idx]
      result[min_idx] <- temp
    } else {
      steps <- c(steps, "  No swap needed (minimum already in place)")
    }

    # Show current state
    sorted <- result[1:i]
    unsorted <- if (i < n) result[(i+1):n] else c()
    steps <- c(steps, paste("  Sorted:", paste(sorted, collapse=", "),
                           "| Unsorted:", paste(unsorted, collapse=", ")))
    steps <- c(steps, "")
  }

  steps <- c(steps, paste("Final sorted array:", paste(result, collapse=", ")))
  steps <- c(steps, paste(rep("=", 70), collapse=""))

  return(steps)
}

#' Check if a vector is sorted
#'
#' @param arr Vector to check
#' @return TRUE if sorted, FALSE otherwise
is_sorted <- function(arr) {
  if (length(arr) <= 1) return(TRUE)
  return(all(diff(arr) >= 0))
}

# ============================================================================
# DEMONSTRATION AND TESTING
# ============================================================================

demonstrate_selection_sort <- function() {
  cat("📚 SELECTION SORT - EDUCATIONAL DEMONSTRATION\n")
  cat(paste(rep("=", 80), collapse=""), "\n\n")

  # Test cases
  test_cases <- list(
    list(arr = c(64, 25, 12, 22, 11), desc = "Random array"),
    list(arr = c(5, 2, 8, 6, 1, 9, 4), desc = "Small random array"),
    list(arr = c(1), desc = "Single element"),
    list(arr = integer(0), desc = "Empty array"),
    list(arr = c(3, 3, 3, 3, 3), desc = "All duplicates"),
    list(arr = c(9, 8, 7, 6, 5, 4, 3, 2, 1), desc = "Reverse sorted"),
    list(arr = c(1, 2, 3, 4, 5), desc = "Already sorted"),
    list(arr = c(1, 3, 2, 4, 5), desc = "Nearly sorted")
  )

  cat("📋 BASIC FUNCTIONALITY TESTS:\n")
  cat(paste(rep("-", 80), collapse=""), "\n\n")

  for (tc in test_cases) {
    original <- tc$arr
    standard <- selection_sort(tc$arr)
    bidirectional <- bidirectional_selection_sort(tc$arr)
    recursive <- selection_sort_recursive(tc$arr)
    stable <- stable_selection_sort(tc$arr)

    cat(sprintf("\nTest: %s\n", tc$desc))
    cat("Original:     ", paste(original, collapse=", "), "\n")
    cat("Standard:     ", paste(standard, collapse=", "), "\n")
    cat("Bidirectional:", paste(bidirectional, collapse=", "), "\n")
    cat("Recursive:    ", paste(recursive, collapse=", "), "\n")
    cat("Stable:       ", paste(stable, collapse=", "), "\n")

    all_correct <- is_sorted(standard) && is_sorted(bidirectional) &&
                   is_sorted(recursive) && is_sorted(stable)
    status <- if (all_correct) "✓" else "✗"
    cat("All correct:", status, "\n")
  }

  # Visualization
  cat("\n\n🎬 STEP-BY-STEP VISUALIZATION:\n")
  cat(paste(rep("-", 80), collapse=""), "\n\n")

  demo_arr <- c(64, 25, 12, 22, 11)
  steps <- visualize_selection_sort(demo_arr)
  for (step in steps) {
    cat(step, "\n")
  }

  # Memory analysis
  cat("\n\n💾 MEMORY USAGE ANALYSIS:\n")
  cat(paste(rep("-", 80), collapse=""), "\n")
  cat("
Selection Sort Memory Characteristics:

1. In-Place Sorting:
   - Space Complexity: O(1) auxiliary space
   - Only uses constant extra memory (min_idx, temp, loop variables)
   - R vectors are copy-on-write (modifications create copies)

2. Memory Writes:
   - Selection Sort: O(n) swaps (minimum writes)
   - Bubble Sort: O(n²) swaps in worst case
   - Insertion Sort: O(n²) shifts in worst case

   ⭐ This makes Selection Sort ideal when writing to memory is expensive!
      Examples: Flash memory, EEPROM, or distributed systems

3. R-Specific:
   - Vectors are immutable (copy-on-write semantics)
   - Use lists for more complex data structures
   - Vectorized operations preferred for performance
\n")

  cat("📌 WHEN TO USE SELECTION SORT:\n")
  cat(paste(rep("-", 80), collapse=""), "\n")
  cat("
✅ GOOD USE CASES:

1. Minimal Memory Writes:
   - Flash memory or EEPROM (limited write cycles)
   - Distributed systems where network writes are expensive

2. Small Datasets:
   - When simplicity matters more than efficiency
   - Statistical analysis with small samples

3. Known Small Data:
   - R data frames with small number of rows
   - When n is guaranteed to be small (< 20 elements)

❌ POOR USE CASES:

1. Large Datasets:
   - Always O(n²) time, never adapts to input
   - Much slower than O(n log n) algorithms
   - Use R's built-in sort() function for large data

2. Nearly Sorted Data:
   - Unlike insertion sort, doesn't benefit from sorted input
   - Still performs all O(n²) comparisons

3. Real-time Systems:
   - Non-adaptive nature means worst-case is always hit
   - Insertion sort or merge sort preferred
\n")
}

# ============================================================================
# PERFORMANCE BENCHMARK
# ============================================================================

performance_benchmark <- function() {
  cat("\n\n⚡ PERFORMANCE BENCHMARK\n")
  cat(paste(rep("=", 80), collapse=""), "\n\n")

  sizes <- c(10, 20, 50, 100, 200)

  cat("Random Data:\n")
  cat(sprintf("%-10s%15s%15s%15s%15s\n", "Size", "Standard", "Bidirectional",
              "Recursive", "R sort()"))
  cat(paste(rep("-", 70), collapse=""), "\n")

  for (size in sizes) {
    test_data <- sample(1:1000, size, replace = TRUE)

    # Standard
    time_standard <- system.time(selection_sort(test_data))[3] * 1000

    # Bidirectional
    time_bidirectional <- system.time(bidirectional_selection_sort(test_data))[3] * 1000

    # Recursive
    time_recursive <- system.time(selection_sort_recursive(test_data))[3] * 1000

    # R built-in sort
    time_builtin <- system.time(sort(test_data))[3] * 1000

    cat(sprintf("%-10d%14.3fms%14.3fms%14.3fms%14.3fms\n",
                size, time_standard, time_bidirectional, time_recursive, time_builtin))
  }
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if (!interactive()) {
  demonstrate_selection_sort()
  performance_benchmark()
  cat("\n✨ Selection Sort demonstration complete!\n")
}

# Export functions
# (In R, all functions are automatically available in the environment)
