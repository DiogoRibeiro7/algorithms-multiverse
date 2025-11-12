# QuickSort Implementation in R
#
# QuickSort is a divide-and-conquer sorting algorithm.
# Average Time Complexity: O(n log n)
# Worst Case: O(n²) - when pivot selection is poor
# Space Complexity: O(log n) - recursion stack
#
# Features:
# - In-place sorting
# - Randomized pivot selection
# - R-style vectorized operations where possible

#' Standard QuickSort using Lomuto partition scheme
#'
#' @param arr Numeric vector to sort
#' @param left Starting index (1-indexed)
#' @param right Ending index
#' @return Sorted vector
quicksort <- function(arr, left = 1, right = length(arr)) {
    if (left < right) {
        pivot_idx <- partition(arr, left, right)
        arr <- quicksort(arr, left, pivot_idx - 1)
        arr <- quicksort(arr, pivot_idx + 1, right)
    }
    return(arr)
}

#' Partition function using Lomuto scheme
partition <- function(arr, left, right) {
    pivot <- arr[right]
    i <- left - 1

    for (j in left:(right - 1)) {
        if (arr[j] <= pivot) {
            i <- i + 1
            # Swap arr[i] and arr[j]
            temp <- arr[i]
            arr[i] <- arr[j]
            arr[j] <- temp
        }
    }

    # Swap arr[i+1] and arr[right]
    temp <- arr[i + 1]
    arr[i + 1] <- arr[right]
    arr[right] <- temp

    return(i + 1)
}

#' Randomized QuickSort
#'
#' @param arr Numeric vector to sort
#' @param left Starting index
#' @param right Ending index
#' @return Sorted vector
quicksort_random <- function(arr, left = 1, right = length(arr)) {
    if (left < right) {
        pivot_idx <- partition_random(arr, left, right)
        arr <- quicksort_random(arr, left, pivot_idx - 1)
        arr <- quicksort_random(arr, pivot_idx + 1, right)
    }
    return(arr)
}

#' Partition with random pivot selection
partition_random <- function(arr, left, right) {
    # Choose random pivot and swap with rightmost element
    random_idx <- sample(left:right, 1)

    temp <- arr[random_idx]
    arr[random_idx] <- arr[right]
    arr[right] <- temp

    return(partition(arr, left, right))
}

#' Three-way QuickSort (Dutch National Flag algorithm)
#' Efficient for arrays with many duplicate elements
#'
#' @param arr Numeric vector to sort
#' @param left Starting index
#' @param right Ending index
#' @return Sorted vector
quicksort_3way <- function(arr, left = 1, right = length(arr)) {
    if (left >= right) return(arr)

    pivot <- arr[left]
    lt <- left      # arr[left..lt-1] < pivot
    gt <- right     # arr[gt+1..right] > pivot
    i <- left + 1   # arr[lt..i-1] == pivot

    while (i <= gt) {
        if (arr[i] < pivot) {
            temp <- arr[lt]
            arr[lt] <- arr[i]
            arr[i] <- temp
            lt <- lt + 1
            i <- i + 1
        } else if (arr[i] > pivot) {
            temp <- arr[i]
            arr[i] <- arr[gt]
            arr[gt] <- temp
            gt <- gt - 1
        } else {
            i <- i + 1
        }
    }

    # Recursively sort partitions
    arr <- quicksort_3way(arr, left, lt - 1)
    arr <- quicksort_3way(arr, gt + 1, right)

    return(arr)
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
#'
#' @param sort_func Sorting function to benchmark
#' @param arr Array to sort
#' @param name Name of the algorithm
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
cat('                    QUICKSORT IN R\n')
cat(rep('=', 70), '\n\n')

# Test 1: Small array
cat('Test 1: Small array\n')
cat(rep('-', 70), '\n')
arr1 <- c(64, 34, 25, 12, 22, 11, 90, 88, 45, 50)

cat('Original: ')
cat('[', paste(arr1, collapse=', '), ']\n')

sorted1 <- quicksort(arr1)

cat('Sorted:   ')
cat('[', paste(sorted1, collapse=', '), ']\n')

if (is_sorted(sorted1)) {
    cat('✓ Array is sorted correctly\n\n')
} else {
    cat('✗ Sorting failed!\n\n')
}

# Test 2: Array with duplicates (3-way partition)
cat('Test 2: Array with duplicates (3-way partition)\n')
cat(rep('-', 70), '\n')
arr2 <- c(5, 2, 8, 2, 9, 1, 5, 5, 2, 8, 3, 7, 4, 6, 1, 9, 3, 7, 4, 6)

cat('Original: ')
cat('[', paste(arr2, collapse=', '), ']\n')

sorted2 <- quicksort_3way(arr2)

cat('Sorted:   ')
cat('[', paste(sorted2, collapse=', '), ']\n')

if (is_sorted(sorted2)) {
    cat('✓ Array is sorted correctly\n\n')
} else {
    cat('✗ Sorting failed!\n\n')
}

# Test 3: Already sorted array (randomized pivot)
cat('Test 3: Already sorted array (randomized pivot)\n')
cat(rep('-', 70), '\n')
arr3 <- 1:20

cat('Original: ')
cat('[', paste(arr3, collapse=', '), ']\n')

sorted3 <- quicksort_random(arr3)

cat('Sorted:   ')
cat('[', paste(sorted3, collapse=', '), ']\n')

if (is_sorted(sorted3)) {
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
    set.seed(42)  # For reproducibility
    arr <- sample(1:10000, size, replace = TRUE)

    # Test standard quicksort
    benchmark_sort(quicksort, arr, "Standard QuickSort")

    # Test randomized quicksort
    benchmark_sort(quicksort_random, arr, "Randomized QuickSort")

    # Test 3-way quicksort
    benchmark_sort(quicksort_3way, arr, "3-Way QuickSort")

    # Compare with R's built-in sort
    start_time <- Sys.time()
    sorted_builtin <- sort(arr)
    end_time <- Sys.time()
    time_builtin <- as.numeric(difftime(end_time, start_time, units = "secs"))
    cat(sprintf("R Built-in sort(): ✓ Sorted in %.6f seconds (reference)\n", time_builtin))
}

cat('\n', rep('=', 70), '\n')
cat('Key Points:\n')
cat('- Standard QuickSort: Simple but O(n²) worst case\n')
cat('- Randomized QuickSort: Average O(n log n) even for sorted input\n')
cat('- 3-Way QuickSort: Excellent for arrays with many duplicates\n')
cat('- In-place sorting: Minimal extra memory\n')
cat('- Not stable: Equal elements may be reordered\n')
cat('- R note: Built-in sort() uses highly optimized algorithms\n')
cat(rep('=', 70), '\n')
