# Comprehensive Linked List Implementations in R
#
# Features:
# - Environment-based nodes for reference semantics
# - Functional programming approach
# - Statistical computing focus
# - Singly and Doubly linked lists
#
# Usage:
#   Rscript linkedlist.R

# ============================================================================
# SINGLY LINKED LIST
# ============================================================================

SinglyNode <- function(data) {
  node <- new.env(parent = emptyenv())
  node$data <- data
  node$next <- NULL
  node
}

SinglyLinkedList <- function() {
  list <- new.env(parent = emptyenv())
  list$head <- NULL
  list$size <- 0

  # Insert at head
  list$insert_at_head <- function(data) {
    new_node <- SinglyNode(data)
    new_node$next <- list$head
    list$head <- new_node
    list$size <- list$size + 1
  }

  # Insert at tail
  list$insert_at_tail <- function(data) {
    new_node <- SinglyNode(data)

    if (is.null(list$head)) {
      list$head <- new_node
    } else {
      current <- list$head
      while (!is.null(current$next)) {
        current <- current$next
      }
      current$next <- new_node
    }

    list$size <- list$size + 1
  }

  # Delete at head
  list$delete_at_head <- function() {
    if (is.null(list$head)) {
      return(NULL)
    }

    data <- list$head$data
    list$head <- list$head$next
    list$size <- list$size - 1
    data
  }

  # Search
  list$search <- function(predicate) {
    current <- list$head

    while (!is.null(current)) {
      if (predicate(current$data)) {
        return(current$data)
      }
      current <- current$next
    }

    NULL
  }

  # Reverse
  list$reverse <- function() {
    prev <- NULL
    current <- list$head

    while (!is.null(current)) {
      next_node <- current$next
      current$next <- prev
      prev <- current
      current <- next_node
    }

    list$head <- prev
  }

  # Get middle element
  list$get_middle <- function() {
    if (is.null(list$head)) {
      return(NULL)
    }

    slow <- list$head
    fast <- list$head

    while (!is.null(fast$next) && !is.null(fast$next$next)) {
      slow <- slow$next
      fast <- fast$next$next
    }

    slow$data
  }

  # Convert to vector
  list$to_vector <- function() {
    result <- c()
    current <- list$head

    while (!is.null(current)) {
      result <- c(result, current$data)
      current <- current$next
    }

    result
  }

  # Print
  list$print <- function() {
    elements <- list$to_vector()
    if (length(elements) == 0) {
      cat("NULL\n")
    } else {
      cat(paste(elements, collapse = " -> "), "-> NULL\n")
    }
  }

  list
}

# ============================================================================
# DOUBLY LINKED LIST
# ============================================================================

DoublyNode <- function(data) {
  node <- new.env(parent = emptyenv())
  node$data <- data
  node$next <- NULL
  node$prev <- NULL
  node
}

DoublyLinkedList <- function() {
  list <- new.env(parent = emptyenv())
  list$head <- NULL
  list$tail <- NULL
  list$size <- 0

  # Insert at head
  list$insert_at_head <- function(data) {
    new_node <- DoublyNode(data)

    if (is.null(list$head)) {
      list$head <- new_node
      list$tail <- new_node
    } else {
      new_node$next <- list$head
      list$head$prev <- new_node
      list$head <- new_node
    }

    list$size <- list$size + 1
  }

  # Insert at tail
  list$insert_at_tail <- function(data) {
    new_node <- DoublyNode(data)

    if (is.null(list$tail)) {
      list$head <- new_node
      list$tail <- new_node
    } else {
      new_node$prev <- list$tail
      list$tail$next <- new_node
      list$tail <- new_node
    }

    list$size <- list$size + 1
  }

  # Delete at head
  list$delete_at_head <- function() {
    if (is.null(list$head)) {
      return(NULL)
    }

    data <- list$head$data

    if (identical(list$head, list$tail)) {
      list$head <- NULL
      list$tail <- NULL
    } else {
      list$head <- list$head$next
      list$head$prev <- NULL
    }

    list$size <- list$size - 1
    data
  }

  # Delete at tail
  list$delete_at_tail <- function() {
    if (is.null(list$tail)) {
      return(NULL)
    }

    data <- list$tail$data

    if (identical(list$head, list$tail)) {
      list$head <- NULL
      list$tail <- NULL
    } else {
      list$tail <- list$tail$prev
      list$tail$next <- NULL
    }

    list$size <- list$size - 1
    data
  }

  # Convert to vector (forward)
  list$to_vector <- function() {
    result <- c()
    current <- list$head

    while (!is.null(current)) {
      result <- c(result, current$data)
      current <- current$next
    }

    result
  }

  # Convert to vector (backward)
  list$to_vector_reverse <- function() {
    result <- c()
    current <- list$tail

    while (!is.null(current)) {
      result <- c(result, current$data)
      current <- current$prev
    }

    result
  }

  # Print
  list$print <- function() {
    elements <- list$to_vector()
    if (length(elements) == 0) {
      cat("NULL\n")
    } else {
      cat(paste(elements, collapse = " <-> "), "<-> NULL\n")
    }
  }

  list
}

# ============================================================================
# STATISTICAL USE CASE: TIME SERIES DATA
# ============================================================================

TimeSeriesLinkedList <- function() {
  list <- DoublyLinkedList()

  # Add time-stamped observation
  list$add_observation <- function(value, timestamp = Sys.time()) {
    observation <- list(value = value, timestamp = timestamp)
    list$insert_at_tail(observation)
  }

  # Get observations within time range
  list$get_range <- function(start_time, end_time) {
    results <- c()
    current <- list$head

    while (!is.null(current)) {
      obs <- current$data
      if (obs$timestamp >= start_time && obs$timestamp <= end_time) {
        results <- c(results, obs$value)
      }
      current <- current$next
    }

    results
  }

  # Calculate rolling mean
  list$rolling_mean <- function(window_size = 5) {
    values <- sapply(list$to_vector(), function(x) x$value)

    if (length(values) < window_size) {
      return(mean(values))
    }

    means <- c()
    for (i in window_size:length(values)) {
      window <- values[(i - window_size + 1):i]
      means <- c(means, mean(window))
    }

    means
  }

  list
}

# ============================================================================
# DEMONSTRATION
# ============================================================================

cat(strrep("=", 80), "\n")
cat("LINKED LIST IMPLEMENTATIONS IN R\n")
cat(strrep("=", 80), "\n")

# Singly Linked List
cat("\n1. SINGLY LINKED LIST\n")
cat(strrep("-", 80), "\n")
sll <- SinglyLinkedList()

cat("Inserting: 1, 2, 3 at head\n")
sll$insert_at_head(3)
sll$insert_at_head(2)
sll$insert_at_head(1)
cat("List: ")
sll$print()

cat("\nInserting: 4, 5 at tail\n")
sll$insert_at_tail(4)
sll$insert_at_tail(5)
cat("List: ")
sll$print()

cat("\nMiddle element:", sll$get_middle(), "\n")

cat("\nReversing list...\n")
sll$reverse()
cat("List: ")
sll$print()

cat("\nAs vector:", paste(sll$to_vector(), collapse = ", "), "\n")

# Doubly Linked List
cat("\n2. DOUBLY LINKED LIST\n")
cat(strrep("-", 80), "\n")
dll <- DoublyLinkedList()

cat("Inserting: 10, 20, 30 at head\n")
dll$insert_at_head(30)
dll$insert_at_head(20)
dll$insert_at_head(10)
cat("List: ")
dll$print()

cat("\nInserting: 40, 50 at tail\n")
dll$insert_at_tail(40)
dll$insert_at_tail(50)
cat("List: ")
dll$print()

cat("\nForward iteration:", paste(dll$to_vector(), collapse = ", "), "\n")
cat("Backward iteration:", paste(dll$to_vector_reverse(), collapse = ", "), "\n")

# Statistical Use Case
cat("\n3. STATISTICAL USE CASE: TIME SERIES\n")
cat(strrep("-", 80), "\n")
ts_list <- TimeSeriesLinkedList()

cat("Adding time-series observations...\n")
set.seed(42)
for (i in 1:10) {
  ts_list$add_observation(rnorm(1, mean = 100, sd = 10))
  Sys.sleep(0.01)  # Small delay for timestamps
}

cat("All observations:",
    paste(sapply(ts_list$to_vector(), function(x) round(x$value, 2)),
          collapse = ", "), "\n")

cat("\nRolling mean (window=3):",
    paste(round(ts_list$rolling_mean(3), 2), collapse = ", "), "\n")

cat("\n", strrep("=", 80), "\n")
cat("✨ All demonstrations complete!\n")
cat(strrep("=", 80), "\n")
