# Binary Search Algorithm Collection in R
#
# Comprehensive implementation of binary search variants including:
# 1. Classic binary search (iterative & recursive)
# 2. First/last occurrence finding
# 3. Rotated array search
# 4. Exponential search
# 5. Interpolation search
# 6. Ternary search
# 7. Binary search on answer (optimization)
# 8. Advanced utilities
#
# Time Complexity: O(log n) for most variants
# Space Complexity: O(1) iterative, O(log n) recursive
#
# R Features:
# - Vectorized operations
# - Functional programming with closures
# - List-based data structures
# - Statistical computing capabilities
# - Comprehensive visualization support

# ==============================================================================
# 1. CLASSIC BINARY SEARCH
# ==============================================================================

#' Classic binary search - iterative implementation
#'
#' @param arr Sorted vector of comparable elements
#' @param target Element to search for
#' @return Index of target if found, NA otherwise
#'
#' @examples
#' binary_search_iterative(c(1, 3, 5, 7, 9), 5)  # Returns 3
#' binary_search_iterative(c(1, 3, 5, 7, 9), 6)  # Returns NA
binary_search_iterative <- function(arr, target) {
  if (length(arr) == 0) {
    return(NA)
  }

  left <- 1
  right <- length(arr)

  while (left <= right) {
    mid <- left + floor((right - left) / 2)

    if (arr[mid] == target) {
      return(mid)
    } else if (arr[mid] < target) {
      left <- mid + 1
    } else {
      right <- mid - 1
    }
  }

  return(NA)
}

#' Classic binary search - recursive implementation
#'
#' @param arr Sorted vector
#' @param target Element to search for
#' @param left Left boundary (default: 1)
#' @param right Right boundary (default: length(arr))
#' @return Index of target if found, NA otherwise
binary_search_recursive <- function(arr, target, left = NULL, right = NULL) {
  if (length(arr) == 0) {
    return(NA)
  }

  if (is.null(left)) left <- 1
  if (is.null(right)) right <- length(arr)

  if (left > right) {
    return(NA)
  }

  mid <- left + floor((right - left) / 2)

  if (arr[mid] == target) {
    return(mid)
  } else if (arr[mid] < target) {
    return(binary_search_recursive(arr, target, mid + 1, right))
  } else {
    return(binary_search_recursive(arr, target, left, mid - 1))
  }
}

#' Generic binary search with custom comparator
#'
#' @param arr Sorted vector
#' @param target Element to search for
#' @param compare_fn Custom comparison function
#' @return Index of target if found, NA otherwise
binary_search_with_comparator <- function(arr, target, compare_fn = NULL) {
  if (is.null(compare_fn)) {
    compare_fn <- function(a, b) {
      if (a < b) return(-1)
      if (a > b) return(1)
      return(0)
    }
  }

  if (length(arr) == 0) {
    return(NA)
  }

  left <- 1
  right <- length(arr)

  while (left <= right) {
    mid <- left + floor((right - left) / 2)
    cmp <- compare_fn(arr[mid], target)

    if (cmp == 0) {
      return(mid)
    } else if (cmp < 0) {
      left <- mid + 1
    } else {
      right <- mid - 1
    }
  }

  return(NA)
}

# ==============================================================================
# 2. FIRST/LAST OCCURRENCE
# ==============================================================================

#' Find first (leftmost) occurrence of target
#'
#' @param arr Sorted vector (may contain duplicates)
#' @param target Element to search for
#' @return Index of first occurrence, NA if not found
find_first_occurrence <- function(arr, target) {
  if (length(arr) == 0) {
    return(NA)
  }

  left <- 1
  right <- length(arr)
  result <- NA

  while (left <= right) {
    mid <- left + floor((right - left) / 2)

    if (arr[mid] == target) {
      result <- mid
      right <- mid - 1  # Continue searching left
    } else if (arr[mid] < target) {
      left <- mid + 1
    } else {
      right <- mid - 1
    }
  }

  return(result)
}

#' Find last (rightmost) occurrence of target
#'
#' @param arr Sorted vector (may contain duplicates)
#' @param target Element to search for
#' @return Index of last occurrence, NA if not found
find_last_occurrence <- function(arr, target) {
  if (length(arr) == 0) {
    return(NA)
  }

  left <- 1
  right <- length(arr)
  result <- NA

  while (left <= right) {
    mid <- left + floor((right - left) / 2)

    if (arr[mid] == target) {
      result <- mid
      left <- mid + 1  # Continue searching right
    } else if (arr[mid] < target) {
      left <- mid + 1
    } else {
      right <- mid - 1
    }
  }

  return(result)
}

#' Count total occurrences of target
#'
#' @param arr Sorted vector
#' @param target Element to count
#' @return Number of occurrences
count_occurrences <- function(arr, target) {
  first <- find_first_occurrence(arr, target)
  if (is.na(first)) {
    return(0)
  }

  last <- find_last_occurrence(arr, target)
  return(last - first + 1)
}

#' Find range [start, end] of target
#'
#' @param arr Sorted vector
#' @param target Element to search for
#' @return List with first and last indices, or NULL if not found
search_range <- function(arr, target) {
  first <- find_first_occurrence(arr, target)
  if (is.na(first)) {
    return(NULL)
  }

  last <- find_last_occurrence(arr, target)
  return(list(first = first, last = last))
}

# ==============================================================================
# 3. ROTATED SORTED ARRAY SEARCH
# ==============================================================================

#' Search in rotated sorted array
#'
#' @param arr Rotated sorted vector (no duplicates)
#' @param target Element to search for
#' @return Index of target if found, NA otherwise
search_rotated_array <- function(arr, target) {
  if (length(arr) == 0) {
    return(NA)
  }

  left <- 1
  right <- length(arr)

  while (left <= right) {
    mid <- left + floor((right - left) / 2)

    if (arr[mid] == target) {
      return(mid)
    }

    # Determine which half is sorted
    if (arr[left] <= arr[mid]) {
      # Left half is sorted
      if (arr[left] <= target && target < arr[mid]) {
        right <- mid - 1
      } else {
        left <- mid + 1
      }
    } else {
      # Right half is sorted
      if (arr[mid] < target && target <= arr[right]) {
        left <- mid + 1
      } else {
        right <- mid - 1
      }
    }
  }

  return(NA)
}

#' Find rotation point (minimum element)
#'
#' @param arr Rotated sorted vector
#' @return Index of minimum element
find_rotation_point <- function(arr) {
  if (length(arr) == 0) {
    return(NA)
  }

  left <- 1
  right <- length(arr)

  while (left < right) {
    mid <- left + floor((right - left) / 2)

    if (arr[mid] > arr[right]) {
      left <- mid + 1
    } else {
      right <- mid
    }
  }

  return(left)
}

# ==============================================================================
# 4. EXPONENTIAL SEARCH
# ==============================================================================

#' Exponential search - efficient for unbounded arrays
#'
#' @param arr Sorted vector
#' @param target Element to search for
#' @return Index of target if found, NA otherwise
exponential_search <- function(arr, target) {
  if (length(arr) == 0) {
    return(NA)
  }

  if (arr[1] == target) {
    return(1)
  }

  # Find range for binary search
  i <- 1
  while (i <= length(arr) && arr[i] <= target) {
    i <- i * 2
  }

  # Binary search in found range
  left <- floor(i / 2)
  right <- min(i, length(arr))

  return(binary_search_recursive(arr, target, left, right))
}

# ==============================================================================
# 5. INTERPOLATION SEARCH
# ==============================================================================

#' Interpolation search - better for uniformly distributed data
#'
#' Time Complexity: O(log log n) average, O(n) worst
#'
#' @param arr Sorted vector of numeric values
#' @param target Numeric value to search for
#' @return Index of target if found, NA otherwise
interpolation_search <- function(arr, target) {
  if (length(arr) == 0) {
    return(NA)
  }

  left <- 1
  right <- length(arr)

  while (left <= right && target >= arr[left] && target <= arr[right]) {
    if (left == right) {
      return(if (arr[left] == target) left else NA)
    }

    # Interpolation formula
    pos <- left + floor(((target - arr[left]) * (right - left)) / (arr[right] - arr[left]))

    # Ensure pos is within bounds
    pos <- max(left, min(pos, right))

    if (arr[pos] == target) {
      return(pos)
    } else if (arr[pos] < target) {
      left <- pos + 1
    } else {
      right <- pos - 1
    }
  }

  return(NA)
}

# ==============================================================================
# 6. TERNARY SEARCH
# ==============================================================================

#' Ternary search - divides array into three parts
#'
#' @param arr Sorted vector
#' @param target Element to search for
#' @return Index of target if found, NA otherwise
ternary_search <- function(arr, target) {
  if (length(arr) == 0) {
    return(NA)
  }

  left <- 1
  right <- length(arr)

  while (left <= right) {
    mid1 <- left + floor((right - left) / 3)
    mid2 <- right - floor((right - left) / 3)

    if (arr[mid1] == target) {
      return(mid1)
    }
    if (arr[mid2] == target) {
      return(mid2)
    }

    if (target < arr[mid1]) {
      right <- mid1 - 1
    } else if (target > arr[mid2]) {
      left <- mid2 + 1
    } else {
      left <- mid1 + 1
      right <- mid2 - 1
    }
  }

  return(NA)
}

#' Ternary search for finding maximum of unimodal function
#'
#' @param fn Unimodal function (single peak)
#' @param left Left boundary
#' @param right Right boundary
#' @param epsilon Precision threshold
#' @return x value where function reaches maximum
ternary_search_maximum <- function(fn, left, right, epsilon = 1e-9) {
  while (right - left > epsilon) {
    mid1 <- left + (right - left) / 3
    mid2 <- right - (right - left) / 3

    if (fn(mid1) < fn(mid2)) {
      left <- mid1
    } else {
      right <- mid2
    }
  }

  return((left + right) / 2)
}

# ==============================================================================
# 7. BINARY SEARCH ON ANSWER
# ==============================================================================

#' Binary search on answer space for optimization problems
#'
#' @param predicate Function returning TRUE if answer is feasible
#' @param low Minimum possible answer
#' @param high Maximum possible answer
#' @return Minimum value where predicate is TRUE, NA if no solution
binary_search_on_answer <- function(predicate, low, high) {
  result <- NA

  while (low <= high) {
    mid <- low + floor((high - low) / 2)

    if (predicate(mid)) {
      result <- mid
      high <- mid - 1  # Try to find smaller answer
    } else {
      low <- mid + 1
    }
  }

  return(result)
}

#' Find integer square root using binary search
#'
#' @param n Number to find square root of (non-negative)
#' @return Integer square root of n
integer_square_root <- function(n) {
  if (n < 0) {
    stop("Cannot compute square root of negative number")
  }

  if (n == 0 || n == 1) {
    return(n)
  }

  left <- 0
  right <- n
  result <- 0

  while (left <= right) {
    mid <- left + floor((right - left) / 2)
    square <- mid * mid

    if (square == n) {
      return(mid)
    } else if (square < n) {
      result <- mid
      left <- mid + 1
    } else {
      right <- mid - 1
    }
  }

  return(result)
}

#' Find square root with decimal precision
#'
#' @param n Number to find square root of
#' @param precision Number of decimal places
#' @return Square root of n
square_root <- function(n, precision = 2) {
  if (n < 0) {
    stop("Cannot compute square root of negative number")
  }

  if (n == 0.0 || n == 1.0) {
    return(n)
  }

  left <- 0
  right <- n
  epsilon <- 10^(-precision)

  while (right - left > epsilon) {
    mid <- left + (right - left) / 2
    square <- mid * mid

    if (abs(square - n) < epsilon) {
      return(mid)
    } else if (square < n) {
      left <- mid
    } else {
      right <- mid
    }
  }

  return((left + right) / 2)
}

# ==============================================================================
# 8. ADVANCED UTILITIES
# ==============================================================================

#' Find insertion position to maintain sorted order
#'
#' @param arr Sorted vector
#' @param target Element to insert
#' @return Index where target should be inserted
search_insert_position <- function(arr, target) {
  if (length(arr) == 0) {
    return(1)
  }

  left <- 1
  right <- length(arr) + 1

  while (left < right) {
    mid <- left + floor((right - left) / 2)

    if (arr[mid] < target) {
      left <- mid + 1
    } else {
      right <- mid
    }
  }

  return(left)
}

#' Find element closest to target
#'
#' @param arr Sorted vector of numeric values
#' @param target Target value
#' @return Index of closest element
find_closest <- function(arr, target) {
  if (length(arr) == 0) {
    return(NA)
  }

  if (length(arr) == 1) {
    return(1)
  }

  if (target <= arr[1]) {
    return(1)
  }
  if (target >= arr[length(arr)]) {
    return(length(arr))
  }

  left <- 1
  right <- length(arr)

  while (left < right) {
    mid <- left + floor((right - left) / 2)

    if (arr[mid] == target) {
      return(mid)
    } else if (arr[mid] < target) {
      left <- mid + 1
    } else {
      right <- mid
    }
  }

  if (left > 1 && abs(arr[left - 1] - target) < abs(arr[left] - target)) {
    return(left - 1)
  }

  return(left)
}

#' Find peak element (element greater than neighbors)
#'
#' @param arr Vector of numeric values
#' @return Index of a peak element
find_peak_element <- function(arr) {
  if (length(arr) == 0) {
    return(NA)
  }

  if (length(arr) == 1) {
    return(1)
  }

  left <- 1
  right <- length(arr)

  while (left < right) {
    mid <- left + floor((right - left) / 2)

    if (arr[mid] < arr[mid + 1]) {
      left <- mid + 1
    } else {
      right <- mid
    }
  }

  return(left)
}

# ==============================================================================
# DEMONSTRATION AND TESTING
# ==============================================================================

demonstrate_all_variants <- function() {
  cat("======================================================================\n")
  cat("BINARY SEARCH ALGORITHM COLLECTION - R\n")
  cat("======================================================================\n")

  # 1. Classic Binary Search
  cat("\n1. CLASSIC BINARY SEARCH\n")
  cat("--------------------------------------------------\n")
  arr <- c(1, 3, 5, 7, 9, 11, 13, 15, 17, 19)
  targets <- c(7, 10, 1, 19)

  for (target in targets) {
    idx_iter <- binary_search_iterative(arr, target)
    idx_rec <- binary_search_recursive(arr, target)
    cat(sprintf("Search %2d: Iterative=%2s, Recursive=%2s\n",
                target, ifelse(is.na(idx_iter), "NA", idx_iter),
                ifelse(is.na(idx_rec), "NA", idx_rec)))
  }

  # 2. First/Last Occurrence
  cat("\n2. FIRST/LAST OCCURRENCE\n")
  cat("--------------------------------------------------\n")
  arr_dup <- c(1, 2, 2, 2, 3, 4, 4, 4, 4, 5)

  for (target in c(2, 4, 6)) {
    first <- find_first_occurrence(arr_dup, target)
    last <- find_last_occurrence(arr_dup, target)
    count <- count_occurrences(arr_dup, target)
    cat(sprintf("Target %d: First=%2s, Last=%2s, Count=%d\n",
                target, ifelse(is.na(first), "NA", first),
                ifelse(is.na(last), "NA", last), count))
  }

  # 3. Rotated Array Search
  cat("\n3. ROTATED ARRAY SEARCH\n")
  cat("--------------------------------------------------\n")
  rotated <- c(4, 5, 6, 7, 0, 1, 2)
  rotation_point <- find_rotation_point(rotated)
  cat(sprintf("Rotated array: %s\n", paste(rotated, collapse = ", ")))
  cat(sprintf("Rotation point: %d (value: %d)\n",
              rotation_point, rotated[rotation_point]))

  for (target in c(0, 3, 6)) {
    idx <- search_rotated_array(rotated, target)
    cat(sprintf("Search %d: Index=%s\n", target, ifelse(is.na(idx), "NA", idx)))
  }

  # 4. Exponential Search
  cat("\n4. EXPONENTIAL SEARCH\n")
  cat("--------------------------------------------------\n")
  large_arr <- seq(1, 99, by = 2)

  for (target in c(15, 51, 99)) {
    idx <- exponential_search(large_arr, target)
    cat(sprintf("Search %2d in array of size %d: Index=%s\n",
                target, length(large_arr), ifelse(is.na(idx), "NA", idx)))
  }

  # 5. Interpolation Search
  cat("\n5. INTERPOLATION SEARCH\n")
  cat("--------------------------------------------------\n")
  uniform_arr <- seq(10, 100, by = 10)

  for (target in c(30, 75, 100)) {
    idx <- interpolation_search(uniform_arr, target)
    cat(sprintf("Search %3d: Index=%s\n", target, ifelse(is.na(idx), "NA", idx)))
  }

  # 6. Ternary Search
  cat("\n6. TERNARY SEARCH\n")
  cat("--------------------------------------------------\n")
  arr <- 1:10

  for (target in c(5, 1, 10, 11)) {
    idx <- ternary_search(arr, target)
    cat(sprintf("Search %2d: Index=%s\n", target, ifelse(is.na(idx), "NA", idx)))
  }

  # Unimodal function
  fn <- function(x) -(x - 5)^2 + 25
  max_x <- ternary_search_maximum(fn, 0, 10)
  cat(sprintf("Maximum of -(x-5)² + 25 at x ≈ %.6f\n", max_x))

  # 7. Binary Search on Answer
  cat("\n7. BINARY SEARCH ON ANSWER\n")
  cat("--------------------------------------------------\n")

  for (n in c(16, 25, 50, 100)) {
    sqrt_int <- integer_square_root(n)
    sqrt_precise <- square_root(n, precision = 2)
    cat(sprintf("√%3d ≈ %d (integer), %.2f (precise)\n",
                n, sqrt_int, sqrt_precise))
  }

  # 8. Advanced Utilities
  cat("\n8. ADVANCED UTILITIES\n")
  cat("--------------------------------------------------\n")
  arr <- c(1, 3, 5, 6, 8, 10)

  for (target in c(2, 5, 11)) {
    pos <- search_insert_position(arr, target)
    cat(sprintf("Insert position for %2d: %d\n", target, pos))
  }

  arr_closest <- c(1, 3, 5, 7, 9)
  for (target in c(4, 6, 8)) {
    idx <- find_closest(arr_closest, target)
    cat(sprintf("Closest to %d: Index=%d, Value=%d\n",
                target, idx, arr_closest[idx]))
  }

  cat("\n======================================================================\n")
  cat("DEMONSTRATION COMPLETE\n")
  cat("======================================================================\n")
}

# Run demonstration if script is executed directly
if (!interactive()) {
  demonstrate_all_variants()
}

# Export functions for use as a package
if (FALSE) {  # Set to TRUE to export
  library(roxygen2)
  roxygenise()
}
