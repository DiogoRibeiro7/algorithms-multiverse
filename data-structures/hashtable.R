# ==============================================================================
# Hash Table Data Structure in R
#
# Implementation of hash table with collision handling.
#
# Features:
# - Separate chaining (linked lists) for collision resolution
# - Dynamic resizing (rehashing)
# - Common hash functions
# - Load factor monitoring
#
# Hash tables provide O(1) average-case lookup, insert, and delete!
#
# Run: Rscript hashtable.R
#
# @author Algorithms Multiverse
# @version 1.0
# ==============================================================================

# ==============================================================================
# Hash Table with Separate Chaining
# ==============================================================================

#' Create Hash Table
#'
#' @param size Initial size (number of buckets)
#' @return Hash table object
create_hashtable <- function(size = 16) {
  list(
    buckets = vector("list", size),
    size = size,
    count = 0,
    load_factor_threshold = 0.75
  )
}

#' Hash Function (Division Method)
#'
#' Time Complexity: O(1)
#'
#' @param key Key to hash
#' @param table_size Table size
#' @return Hash value (bucket index)
hash_function <- function(key, table_size) {
  if (is.character(key)) {
    # String hashing: sum of character codes
    hash_val <- sum(utf8ToInt(key))
  } else {
    hash_val <- key
  }

  (hash_val %% table_size) + 1  # R uses 1-based indexing
}

#' Insert into Hash Table
#'
#' Time Complexity: O(1) average, O(n) worst case
#'
#' @param ht Hash table object
#' @param key Key
#' @param value Value
#' @return Updated hash table
hashtable_insert <- function(ht, key, value) {
  # Check if resizing needed
  load_factor <- ht$count / ht$size
  if (load_factor > ht$load_factor_threshold) {
    ht <- hashtable_resize(ht, ht$size * 2)
  }

  # Compute hash
  hash_idx <- hash_function(key, ht$size)

  # Check if key exists (update)
  if (!is.null(ht$buckets[[hash_idx]])) {
    for (i in seq_along(ht$buckets[[hash_idx]])) {
      if (ht$buckets[[hash_idx]][[i]]$key == key) {
        ht$buckets[[hash_idx]][[i]]$value <- value
        return(ht)
      }
    }
  }

  # Insert new key-value pair
  entry <- list(key = key, value = value)
  ht$buckets[[hash_idx]] <- c(ht$buckets[[hash_idx]], list(entry))
  ht$count <- ht$count + 1

  ht
}

#' Get from Hash Table
#'
#' Time Complexity: O(1) average, O(n) worst case
#'
#' @param ht Hash table object
#' @param key Key to lookup
#' @return Value if found, NULL otherwise
hashtable_get <- function(ht, key) {
  hash_idx <- hash_function(key, ht$size)

  if (!is.null(ht$buckets[[hash_idx]])) {
    for (entry in ht$buckets[[hash_idx]]) {
      if (entry$key == key) {
        return(entry$value)
      }
    }
  }

  NULL  # Key not found
}

#' Delete from Hash Table
#'
#' Time Complexity: O(1) average, O(n) worst case
#'
#' @param ht Hash table object
#' @param key Key to delete
#' @return Updated hash table
hashtable_delete <- function(ht, key) {
  hash_idx <- hash_function(key, ht$size)

  if (!is.null(ht$buckets[[hash_idx]])) {
    for (i in seq_along(ht$buckets[[hash_idx]])) {
      if (ht$buckets[[hash_idx]][[i]]$key == key) {
        ht$buckets[[hash_idx]] <- ht$buckets[[hash_idx]][-i]
        ht$count <- ht$count - 1
        return(ht)
      }
    }
  }

  ht
}

#' Check if Key Exists
#'
#' @param ht Hash table object
#' @param key Key to check
#' @return TRUE if exists, FALSE otherwise
hashtable_contains <- function(ht, key) {
  !is.null(hashtable_get(ht, key))
}

#' Get All Keys
#'
#' @param ht Hash table object
#' @return Vector of all keys
hashtable_keys <- function(ht) {
  keys <- c()
  for (bucket in ht$buckets) {
    if (!is.null(bucket)) {
      for (entry in bucket) {
        keys <- c(keys, entry$key)
      }
    }
  }
  keys
}

#' Get All Values
#'
#' @param ht Hash table object
#' @return List of all values
hashtable_values <- function(ht) {
  values <- list()
  for (bucket in ht$buckets) {
    if (!is.null(bucket)) {
      for (entry in bucket) {
        values <- c(values, list(entry$value))
      }
    }
  }
  values
}

#' Resize Hash Table (Rehashing)
#'
#' Time Complexity: O(n) where n = number of entries
#'
#' @param ht Hash table object
#' @param new_size New table size
#' @return Resized hash table
hashtable_resize <- function(ht, new_size) {
  # Create new hash table
  new_ht <- create_hashtable(new_size)

  # Rehash all entries
  for (bucket in ht$buckets) {
    if (!is.null(bucket)) {
      for (entry in bucket) {
        new_ht <- hashtable_insert(new_ht, entry$key, entry$value)
        new_ht$count <- new_ht$count - 1  # Adjust count (insert increments it)
      }
    }
  }

  new_ht$count <- ht$count
  new_ht
}

#' Get Load Factor
#'
#' @param ht Hash table object
#' @return Load factor (entries / buckets)
hashtable_load_factor <- function(ht) {
  ht$count / ht$size
}

#' Print Hash Table Statistics
#'
#' @param ht Hash table object
hashtable_stats <- function(ht) {
  cat(sprintf("Size: %d buckets\n", ht$size))
  cat(sprintf("Count: %d entries\n", ht$count))
  cat(sprintf("Load factor: %.2f\n", hashtable_load_factor(ht)))

  # Collision statistics
  non_empty <- sum(sapply(ht$buckets, function(b) !is.null(b)))
  cat(sprintf("Non-empty buckets: %d\n", non_empty))

  chain_lengths <- sapply(ht$buckets, function(b) if(is.null(b)) 0 else length(b))
  max_chain <- max(chain_lengths)
  avg_chain <- mean(chain_lengths[chain_lengths > 0])

  cat(sprintf("Max chain length: %d\n", max_chain))
  if (!is.nan(avg_chain)) {
    cat(sprintf("Avg chain length: %.2f\n", avg_chain))
  }
}

# ==============================================================================
# Main Program - Examples and Tests
# ==============================================================================

cat("==============================================================================\n")
cat("                HASH TABLE DATA STRUCTURE IN R\n")
cat("           O(1) Average-Case Lookup Performance!\n")
cat("==============================================================================\n\n")

# Example 1: Basic Operations
cat("Example 1: Basic Hash Table Operations\n")
cat(strrep("=", 80), "\n")

ht <- create_hashtable(size = 8)

# Insert
cat("Inserting key-value pairs:\n")
ht <- hashtable_insert(ht, "name", "Alice")
ht <- hashtable_insert(ht, "age", 30)
ht <- hashtable_insert(ht, "city", "New York")
ht <- hashtable_insert(ht, "occupation", "Engineer")

cat(sprintf("  name -> %s\n", hashtable_get(ht, "name")))
cat(sprintf("  age -> %d\n", hashtable_get(ht, "age")))
cat(sprintf("  city -> %s\n", hashtable_get(ht, "city")))
cat(sprintf("  occupation -> %s\n", hashtable_get(ht, "occupation")))

# Update
cat("\nUpdating age to 31:\n")
ht <- hashtable_insert(ht, "age", 31)
cat(sprintf("  age -> %d\n", hashtable_get(ht, "age")))

# Contains
cat(sprintf("\nContains 'name': %s\n", hashtable_contains(ht, "name")))
cat(sprintf("Contains 'salary': %s\n", hashtable_contains(ht, "salary")))

# Delete
cat("\nDeleting 'city':\n")
ht <- hashtable_delete(ht, "city")
cat(sprintf("Contains 'city': %s\n\n", hashtable_contains(ht, "city")))

# Example 2: Hash Table Statistics
cat("Example 2: Hash Table Statistics\n")
cat(strrep("=", 80), "\n")
hashtable_stats(ht)
cat("\n")

# Example 3: Dynamic Resizing
cat("Example 3: Dynamic Resizing (Rehashing)\n")
cat(strrep("=", 80), "\n")

ht2 <- create_hashtable(size = 4)
cat("Initial table (size 4):\n")
hashtable_stats(ht2)

cat("\nInserting 10 items (triggers resize at load factor 0.75):\n")
for (i in 1:10) {
  ht2 <- hashtable_insert(ht2, paste0("key", i), i * 10)
}

hashtable_stats(ht2)
cat("\nTable automatically resized!\n\n")

# Example 4: Word Frequency Counter
cat("Example 4: Word Frequency Counter\n")
cat(strrep("=", 80), "\n")

text <- "the quick brown fox jumps over the lazy dog the fox was quick"
words <- strsplit(text, " ")[[1]]

freq_table <- create_hashtable()

cat(sprintf("Text: %s\n\n", text))
cat("Building frequency table:\n")

for (word in words) {
  current_count <- hashtable_get(freq_table, word)
  if (is.null(current_count)) {
    current_count <- 0
  }
  freq_table <- hashtable_insert(freq_table, word, current_count + 1)
}

cat("Word frequencies:\n")
for (word in hashtable_keys(freq_table)) {
  cat(sprintf("  %-10s: %d\n", word, hashtable_get(freq_table, word)))
}
cat("\n")

# Example 5: Collision Demonstration
cat("Example 5: Collision Handling\n")
cat(strrep("=", 80), "\n")

ht3 <- create_hashtable(size = 5)

# Insert keys that will likely collide
keys <- c("apple", "banana", "cherry", "date", "elderberry", "fig", "grape")
cat("Inserting keys (small table to force collisions):\n")
cat(sprintf("Keys: %s\n\n", paste(keys, collapse = ", ")))

for (i in seq_along(keys)) {
  ht3 <- hashtable_insert(ht3, keys[i], i)
}

hashtable_stats(ht3)
cat("\nCollisions handled via separate chaining!\n\n")

# Summary
cat(strrep("=", 80), "\n")
cat("Summary: Hash Table in R\n")
cat(strrep("=", 80), "\n")
cat("✓ Insert: O(1) average\n")
cat("✓ Lookup: O(1) average\n")
cat("✓ Delete: O(1) average\n")
cat("✓ Space: O(n) where n = entries\n")
cat("\nFeatures:\n")
cat("- Separate chaining for collisions\n")
cat("- Automatic resizing (rehashing)\n")
cat("- Load factor monitoring\n")
cat("\nApplications:\n")
cat("- Databases (indexing)\n")
cat("- Caching\n")
cat("- Symbol tables in compilers\n")
cat("- Duplicate detection\n")
cat("- Frequency counting\n")
cat(strrep("=", 80), "\n")
