# ==============================================================================
# Heap Data Structures in R
#
# Binary heap implementation for priority queues.
#
# Implementations:
# - Min Heap
# - Max Heap
# - Priority Queue
# - Heap Sort
#
# Heaps are complete binary trees stored as arrays, providing efficient
# priority queue operations.
#
# Run: Rscript heap.R
#
# @author Algorithms Multiverse
# @version 1.0
# ==============================================================================

# ==============================================================================
# Min Heap
# ==============================================================================

#' Create Min Heap
#'
#' @return Empty min heap (list with heap vector)
create_min_heap <- function() {
  list(heap = integer(0), size = 0)
}

#' Get Parent Index
parent_idx <- function(i) {
  floor(i / 2)
}

#' Get Left Child Index
left_child_idx <- function(i) {
  2 * i
}

#' Get Right Child Index
right_child_idx <- function(i) {
  2 * i + 1
}

#' Heapify Up (Bubble Up)
#'
#' @param heap_obj Heap object
#' @param i Index to heapify from
heapify_up_min <- function(heap_obj, i) {
  while (i > 1 && heap_obj$heap[parent_idx(i)] > heap_obj$heap[i]) {
    # Swap with parent
    temp <- heap_obj$heap[i]
    heap_obj$heap[i] <- heap_obj$heap[parent_idx(i)]
    heap_obj$heap[parent_idx(i)] <- temp

    i <- parent_idx(i)
  }
  heap_obj
}

#' Heapify Down (Bubble Down)
#'
#' @param heap_obj Heap object
#' @param i Index to heapify from
heapify_down_min <- function(heap_obj, i) {
  while (TRUE) {
    smallest <- i
    left <- left_child_idx(i)
    right <- right_child_idx(i)

    if (left <= heap_obj$size && heap_obj$heap[left] < heap_obj$heap[smallest]) {
      smallest <- left
    }
    if (right <= heap_obj$size && heap_obj$heap[right] < heap_obj$heap[smallest]) {
      smallest <- right
    }

    if (smallest == i) break

    # Swap
    temp <- heap_obj$heap[i]
    heap_obj$heap[i] <- heap_obj$heap[smallest]
    heap_obj$heap[smallest] <- temp

    i <- smallest
  }
  heap_obj
}

#' Insert into Min Heap
#'
#' Time Complexity: O(log n)
#'
#' @param heap_obj Heap object
#' @param value Value to insert
#' @return Updated heap
min_heap_insert <- function(heap_obj, value) {
  heap_obj$size <- heap_obj$size + 1
  heap_obj$heap[heap_obj$size] <- value
  heapify_up_min(heap_obj, heap_obj$size)
}

#' Extract Minimum
#'
#' Time Complexity: O(log n)
#'
#' @param heap_obj Heap object
#' @return List with min value and updated heap
min_heap_extract_min <- function(heap_obj) {
  if (heap_obj$size == 0) {
    stop("Heap is empty")
  }

  min_val <- heap_obj$heap[1]

  # Move last element to root
  heap_obj$heap[1] <- heap_obj$heap[heap_obj$size]
  heap_obj$size <- heap_obj$size - 1

  if (heap_obj$size > 0) {
    heap_obj <- heapify_down_min(heap_obj, 1)
  }

  list(value = min_val, heap = heap_obj)
}

#' Peek Minimum
#'
#' Time Complexity: O(1)
#'
#' @param heap_obj Heap object
#' @return Minimum value
min_heap_peek <- function(heap_obj) {
  if (heap_obj$size == 0) {
    stop("Heap is empty")
  }
  heap_obj$heap[1]
}

# ==============================================================================
# Max Heap
# ==============================================================================

#' Heapify Up for Max Heap
heapify_up_max <- function(heap_obj, i) {
  while (i > 1 && heap_obj$heap[parent_idx(i)] < heap_obj$heap[i]) {
    temp <- heap_obj$heap[i]
    heap_obj$heap[i] <- heap_obj$heap[parent_idx(i)]
    heap_obj$heap[parent_idx(i)] <- temp
    i <- parent_idx(i)
  }
  heap_obj
}

#' Heapify Down for Max Heap
heapify_down_max <- function(heap_obj, i) {
  while (TRUE) {
    largest <- i
    left <- left_child_idx(i)
    right <- right_child_idx(i)

    if (left <= heap_obj$size && heap_obj$heap[left] > heap_obj$heap[largest]) {
      largest <- left
    }
    if (right <= heap_obj$size && heap_obj$heap[right] > heap_obj$heap[largest]) {
      largest <- right
    }

    if (largest == i) break

    temp <- heap_obj$heap[i]
    heap_obj$heap[i] <- heap_obj$heap[largest]
    heap_obj$heap[largest] <- temp
    i <- largest
  }
  heap_obj
}

#' Insert into Max Heap
max_heap_insert <- function(heap_obj, value) {
  heap_obj$size <- heap_obj$size + 1
  heap_obj$heap[heap_obj$size] <- value
  heapify_up_max(heap_obj, heap_obj$size)
}

#' Extract Maximum
max_heap_extract_max <- function(heap_obj) {
  if (heap_obj$size == 0) {
    stop("Heap is empty")
  }

  max_val <- heap_obj$heap[1]
  heap_obj$heap[1] <- heap_obj$heap[heap_obj$size]
  heap_obj$size <- heap_obj$size - 1

  if (heap_obj$size > 0) {
    heap_obj <- heapify_down_max(heap_obj, 1)
  }

  list(value = max_val, heap = heap_obj)
}

# ==============================================================================
# Heap Sort
# ==============================================================================

#' Heap Sort
#'
#' Sorts array using heap data structure
#'
#' Time Complexity: O(n log n)
#' Space Complexity: O(1) - in-place
#'
#' Applications:
#' - Guaranteed O(n log n) worst case
#' - In-place sorting
#' - Not stable
#'
#' @param arr Array to sort
#' @return Sorted array
heap_sort <- function(arr) {
  n <- length(arr)

  # Build max heap
  for (i in floor(n/2):1) {
    arr <- heapify_array(arr, n, i)
  }

  # Extract elements one by one
  for (i in n:2) {
    # Move current root to end
    temp <- arr[1]
    arr[1] <- arr[i]
    arr[i] <- temp

    # Heapify reduced heap
    arr <- heapify_array(arr, i - 1, 1)
  }

  arr
}

#' Heapify Array (for heap sort)
heapify_array <- function(arr, heap_size, i) {
  largest <- i
  left <- 2 * i
  right <- 2 * i + 1

  if (left <= heap_size && arr[left] > arr[largest]) {
    largest <- left
  }
  if (right <= heap_size && arr[right] > arr[largest]) {
    largest <- right
  }

  if (largest != i) {
    temp <- arr[i]
    arr[i] <- arr[largest]
    arr[largest] <- temp
    arr <- heapify_array(arr, heap_size, largest)
  }

  arr
}

# ==============================================================================
# Build Heap from Array
# ==============================================================================

#' Build Min Heap from Array
#'
#' Time Complexity: O(n) - surprisingly, not O(n log n)!
#'
#' @param arr Input array
#' @return Min heap object
build_min_heap <- function(arr) {
  heap_obj <- list(heap = arr, size = length(arr))

  # Start from last non-leaf node
  for (i in floor(heap_obj$size / 2):1) {
    heap_obj <- heapify_down_min(heap_obj, i)
  }

  heap_obj
}

# ==============================================================================
# Main Program - Examples and Tests
# ==============================================================================

cat("==============================================================================\n")
cat("                HEAP DATA STRUCTURES IN R\n")
cat("            Priority Queues & Heap Sort\n")
cat("==============================================================================\n\n")

# Example 1: Min Heap
cat("Example 1: Min Heap (Priority Queue)\n")
cat(strrep("=", 80), "\n")

min_heap <- create_min_heap()
values <- c(15, 10, 20, 8, 21, 5)

cat(sprintf("Inserting: %s\n", paste(values, collapse = ", ")))
for (val in values) {
  min_heap <- min_heap_insert(min_heap, val)
}

cat(sprintf("Heap array: %s\n", paste(min_heap$heap[1:min_heap$size], collapse = ", ")))
cat(sprintf("Minimum (peek): %d\n", min_heap_peek(min_heap)))

cat("\nExtracting minimum elements:\n")
while (min_heap$size > 0) {
  result <- min_heap_extract_min(min_heap)
  cat(sprintf("  Extracted: %d\n", result$value))
  min_heap <- result$heap
}
cat("\n")

# Example 2: Max Heap
cat("Example 2: Max Heap\n")
cat(strrep("=", 80), "\n")

max_heap <- list(heap = integer(0), size = 0)
values <- c(15, 10, 20, 8, 21, 5)

cat(sprintf("Inserting: %s\n", paste(values, collapse = ", ")))
for (val in values) {
  max_heap <- max_heap_insert(max_heap, val)
}

cat(sprintf("Heap array: %s\n", paste(max_heap$heap[1:max_heap$size], collapse = ", ")))
cat(sprintf("Maximum: %d\n\n", max_heap$heap[1]))

# Example 3: Heap Sort
cat("Example 3: Heap Sort\n")
cat(strrep("=", 80), "\n")

arr <- c(12, 11, 13, 5, 6, 7)
cat(sprintf("Original: %s\n", paste(arr, collapse = ", ")))

sorted_arr <- heap_sort(arr)
cat(sprintf("Sorted:   %s\n\n", paste(sorted_arr, collapse = ", ")))

# Example 4: Build Heap from Array
cat("Example 4: Build Min Heap from Array\n")
cat(strrep("=", 80), "\n")

arr <- c(9, 5, 6, 2, 3, 7, 1, 4, 8)
cat(sprintf("Array: %s\n", paste(arr, collapse = ", ")))

heap <- build_min_heap(arr)
cat(sprintf("Min heap: %s\n", paste(heap$heap[1:heap$size], collapse = ", ")))
cat(sprintf("Minimum: %d\n\n", heap$heap[1]))

# Example 5: Priority Queue Application
cat("Example 5: Priority Queue (Task Scheduling)\n")
cat(strrep("=", 80), "\n")

# Simulate task scheduling with priorities (lower = higher priority)
tasks <- data.frame(
  task = c("Email", "Meeting", "Code Review", "Bug Fix", "Documentation"),
  priority = c(3, 1, 2, 1, 4)
)

pq <- create_min_heap()
cat("Adding tasks:\n")
for (i in 1:nrow(tasks)) {
  cat(sprintf("  %s (priority %d)\n", tasks$task[i], tasks$priority[i]))
  pq <- min_heap_insert(pq, tasks$priority[i])
}

cat("\nProcessing tasks by priority:\n")
task_idx <- 1
while (pq$size > 0) {
  result <- min_heap_extract_min(pq)
  # Find task with this priority
  task_row <- which(tasks$priority == result$value)[1]
  cat(sprintf("  Processing: %s (priority %d)\n", tasks$task[task_row], result$value))
  pq <- result$heap
}
cat("\n")

# Summary
cat(strrep("=", 80), "\n")
cat("Summary: Heap Data Structures in R\n")
cat(strrep("=", 80), "\n")
cat("✓ Min/Max Heap: O(log n) insert/extract\n")
cat("✓ Peek: O(1) to get min/max\n")
cat("✓ Build heap: O(n) from array\n")
cat("✓ Heap sort: O(n log n) guaranteed, in-place\n")
cat("\nApplications:\n")
cat("- Priority queues (task scheduling)\n")
cat("- Dijkstra's shortest path algorithm\n")
cat("- Heap sort (guaranteed O(n log n))\n")
cat("- Finding k largest/smallest elements\n")
cat("- Event-driven simulation\n")
cat(strrep("=", 80), "\n")
