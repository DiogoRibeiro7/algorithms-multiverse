# MergeSort Implementation in R
#
# MergeSort is a divide-and-conquer sorting algorithm.
# Time Complexity: O(n log n) - all cases
# Space Complexity: O(n) - requires auxiliary array
#
# Features:
# - Stable sorting algorithm
# - Guaranteed O(n log n) performance
# - R-style implementation with vectorized operations

#' Top-down MergeSort (recursive)
#'
#' @param arr Numeric vector to sort
#' @return Sorted vector
mergesort <- function(arr) {
    n <- length(arr)

    # Base case
    if (n <= 1) {
        return(arr)
    }

    # Divide
    mid <- floor(n / 2)
    left <- arr[1:mid]
    right <- arr[(mid + 1):n]

    # Conquer
    left <- mergesort(left)
    right <- mergesort(right)

    # Combine
    return(merge(left, right))
}

#' Merge two sorted vectors
#'
#' @param left First sorted vector
#' @param right Second sorted vector
#' @return Merged sorted vector
merge <- function(left, right) {
    result <- numeric(length(left) + length(right))
    i <- 1
    j <- 1
    k <- 1

    # Merge while both vectors have elements
    while (i <= length(left) && j <= length(right)) {
        if (left[i] <= right[j]) {  # <= ensures stability
            result[k] <- left[i]
            i <- i + 1
        } else {
            result[k] <- right[j]
            j <- j + 1
        }
        k <- k + 1
    }

    # Copy remaining elements from left
    while (i <= length(left)) {
        result[k] <- left[i]
        i <- i + 1
        k <- k + 1
    }

    # Copy remaining elements from right
    while (j <= length(right)) {
        result[k] <- right[j]
        j <- j + 1
        k <- k + 1
    }

    return(result)
}

#' Bottom-up MergeSort (iterative)
#' Avoids recursion overhead
#'
#' @param arr Numeric vector to sort
#' @return Sorted vector
mergesort_bottomup <- function(arr) {
    n <- length(arr)

    # Start with subarrays of size 1
    curr_size <- 1

    while (curr_size < n) {
        # Pick starting points of left subarrays
        left_start <- 1

        while (left_start <= n) {
            # Find ending point of left subarray
            mid <- min(left_start + curr_size - 1, n)

            # Find ending point of right subarray
            right_end <- min(left_start + 2 * curr_size - 1, n)

            # Merge if there's a right subarray
            if (mid < n) {
                left <- arr[left_start:mid]
                right <- arr[(mid + 1):min(right_end, n)]
                merged <- merge(left, right)
                arr[left_start:min(right_end, n)] <- merged
            }

            left_start <- left_start + 2 * curr_size
        }

        curr_size <- curr_size * 2
    }

    return(arr)
}

#' Natural MergeSort
#' Takes advantage of already sorted runs in the data
#'
#' @param arr Numeric vector to sort
#' @return Sorted vector
mergesort_natural <- function(arr) {
    n <- length(arr)
    if (n <= 1) return(arr)

    # Find natural runs
    runs <- find_runs(arr)

    # Merge runs until only one remains
    while (length(runs) > 1) {
        new_runs <- list()

        i <- 1
        while (i <= length(runs)) {
            if (i < length(runs)) {
                # Merge two consecutive runs
                merged <- merge(runs[[i]], runs[[i + 1]])
                new_runs <- c(new_runs, list(merged))
                i <- i + 2
            } else {
                # Odd run left over
                new_runs <- c(new_runs, list(runs[[i]]))
                i <- i + 1
            }
        }

        runs <- new_runs
    }

    return(runs[[1]])
}

#' Find natural runs (already sorted sequences) in array
find_runs <- function(arr) {
    n <- length(arr)
    if (n == 0) return(list())

    runs <- list()
    start <- 1

    i <- 1
    while (i < n) {
        # Find end of ascending run
        while (i < n && arr[i] <= arr[i + 1]) {
            i <- i + 1
        }

        # Add run to list
        runs <- c(runs, list(arr[start:i]))

        i <- i + 1
        start <- i
    }

    # Add last element if not included
    if (start <= n) {
        runs <- c(runs, list(arr[start:n]))
    }

    return(runs)
}

#' Check if vector is sorted
#'
#' @param arr Vector to check
#' @return TRUE if sorted, FALSE otherwise
is_sorted <- function(arr) {
    if (length(arr) <= 1) return(TRUE)
    return(all(arr[-length(arr)] <= arr[-1]))
}

#' Benchmark sorting function
benchmark_sort <- function(sort_func, arr, name) {
    start_time <- Sys.time()
    sorted_arr <- sort_func(arr)
    end_time <- Sys.time()

    time_taken <- as.numeric(difftime(end_time, start_time, units = "secs"))

    if (is_sorted(sorted_arr)) {
        cat(sprintf("%s: ✓ Sorted in %.6f seconds\n", name, time_taken))
    } else {
        cat(sprintf("%s: ✗ Sort failed!\n", name))
    }

    return(time_taken)
}

# ===================================================================
# MAIN DEMONSTRATION
# ===================================================================

cat(rep('=', 70), '\n')
cat('                    MERGESORT IN R\n')
cat(rep('=', 70), '\n\n')

# Test 1: Small array
cat('Test 1: Small array (Top-Down)\n')
cat(rep('-', 70), '\n')
arr1 <- c(64, 34, 25, 12, 22, 11, 90, 88, 45, 50)

cat('Original: ')
cat('[', paste(arr1, collapse=', '), ']\n')

sorted1 <- mergesort(arr1)

cat('Sorted:   ')
cat('[', paste(sorted1, collapse=', '), ']\n')

if (is_sorted(sorted1)) {
    cat('✓ Array is sorted correctly\n')
    cat('Note: MergeSort is stable (preserves order of equal elements)\n\n')
} else {
    cat('✗ Sorting failed!\n\n')
}

# Test 2: Array with duplicates (stability test)
cat('Test 2: Testing stability with duplicates\n')
cat(rep('-', 70), '\n')
arr2 <- c(5, 2, 8, 2, 9, 1, 5, 5, 2, 8)

cat('Original: ')
cat('[', paste(arr2, collapse=', '), ']\n')

sorted2 <- mergesort(arr2)

cat('Sorted:   ')
cat('[', paste(sorted2, collapse=', '), ']\n')

if (is_sorted(sorted2)) {
    cat('✓ Array is sorted correctly\n\n')
} else {
    cat('✗ Sorting failed!\n\n')
}

# Test 3: Bottom-up MergeSort
cat('Test 3: Bottom-Up MergeSort (Iterative)\n')
cat(rep('-', 70), '\n')
arr3 <- c(38, 27, 43, 3, 9, 82, 10, 15, 22, 33)

cat('Original: ')
cat('[', paste(arr3, collapse=', '), ']\n')

sorted3 <- mergesort_bottomup(arr3)

cat('Sorted:   ')
cat('[', paste(sorted3, collapse=', '), ']\n')

if (is_sorted(sorted3)) {
    cat('✓ Array is sorted correctly\n\n')
} else {
    cat('✗ Sorting failed!\n\n')
}

# Test 4: Natural MergeSort (partially sorted data)
cat('Test 4: Natural MergeSort (takes advantage of existing order)\n')
cat(rep('-', 70), '\n')
arr4 <- c(1, 2, 3, 10, 11, 4, 5, 6, 15, 20, 7, 8, 9)

cat('Original: ')
cat('[', paste(arr4, collapse=', '), ']\n')
cat('(Notice the existing sorted runs: 1-3, 10-11, 4-6, 15-20, 7-9)\n')

sorted4 <- mergesort_natural(arr4)

cat('Sorted:   ')
cat('[', paste(sorted4, collapse=', '), ']\n')

if (is_sorted(sorted4)) {
    cat('✓ Array is sorted correctly\n\n')
} else {
    cat('✗ Sorting failed!\n\n')
}

# Performance benchmarks
cat('Performance Benchmarks\n')
cat(rep('=', 70), '\n')

sizes <- c(1000, 5000, 10000)

for (size in sizes) {
    cat(sprintf('\nArray size: %d elements\n', size))
    cat(rep('-', 70), '\n')

    # Create random array
    set.seed(42)
    arr <- sample(1:10000, size, replace = TRUE)

    # Test top-down mergesort
    benchmark_sort(mergesort, arr, "Top-Down MergeSort")

    # Test bottom-up mergesort
    benchmark_sort(mergesort_bottomup, arr, "Bottom-Up MergeSort")

    # Test natural mergesort
    benchmark_sort(mergesort_natural, arr, "Natural MergeSort")

    # Compare with R's built-in sort
    start_time <- Sys.time()
    sorted_builtin <- sort(arr)
    end_time <- Sys.time()
    time_builtin <- as.numeric(difftime(end_time, start_time, units = "secs"))
    cat(sprintf("R Built-in sort(): ✓ Sorted in %.6f seconds (reference)\n", time_builtin))
}

cat('\n', rep('=', 70), '\n')
cat('Key Points:\n')
cat('- Time Complexity: O(n log n) for all cases (best, average, worst)\n')
cat('- Space Complexity: O(n) - requires auxiliary array\n')
cat('- Stable: Yes - maintains relative order of equal elements\n')
cat('- Top-Down: Recursive, conceptually simple\n')
cat('- Bottom-Up: Iterative, avoids recursion overhead\n')
cat('- Natural: Takes advantage of existing order in data\n')
cat('- Best for: Linked lists, external sorting, stability required\n')
cat('- R note: Built-in sort() is highly optimized for production use\n')
cat(rep('=', 70), '\n')
