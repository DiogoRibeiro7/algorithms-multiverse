# ==============================================================================
# Tree Data Structures in R
#
# Implementations of binary search trees and balanced variants.
#
# Implementations:
# - Binary Search Tree (BST)
# - AVL Tree (self-balancing)
# - Tree Traversals (inorder, preorder, postorder, level-order)
#
# Trees are fundamental data structures for hierarchical data storage
# and efficient searching, insertion, and deletion.
#
# Run: Rscript trees.R
#
# @author Algorithms Multiverse
# @version 1.0
# ==============================================================================

# ==============================================================================
# Binary Search Tree (BST) Node
# ==============================================================================

#' Create BST Node
#'
#' @param value Node value
#' @return List representing a BST node
create_node <- function(value) {
  list(
    value = value,
    left = NULL,
    right = NULL,
    height = 1  # For AVL trees
  )
}

# ==============================================================================
# Binary Search Tree Operations
# ==============================================================================

#' Insert into BST
#'
#' Time Complexity: O(h) where h = height (O(log n) balanced, O(n) worst)
#' Space Complexity: O(h) for recursion stack
#'
#' @param root Root node
#' @param value Value to insert
#' @return New root
bst_insert <- function(root, value) {
  if (is.null(root)) {
    return(create_node(value))
  }

  if (value < root$value) {
    root$left <- bst_insert(root$left, value)
  } else if (value > root$value) {
    root$right <- bst_insert(root$right, value)
  }

  root
}

#' Search in BST
#'
#' Time Complexity: O(h)
#'
#' @param root Root node
#' @param value Value to search
#' @return TRUE if found, FALSE otherwise
bst_search <- function(root, value) {
  if (is.null(root)) {
    return(FALSE)
  }

  if (root$value == value) {
    return(TRUE)
  } else if (value < root$value) {
    return(bst_search(root$left, value))
  } else {
    return(bst_search(root$right, value))
  }
}

#' Find Minimum Value in BST
#'
#' @param root Root node
#' @return Minimum value
bst_find_min <- function(root) {
  if (is.null(root)) return(NULL)

  current <- root
  while (!is.null(current$left)) {
    current <- current$left
  }

  current$value
}

#' Delete from BST
#'
#' Time Complexity: O(h)
#'
#' @param root Root node
#' @param value Value to delete
#' @return New root
bst_delete <- function(root, value) {
  if (is.null(root)) {
    return(NULL)
  }

  if (value < root$value) {
    root$left <- bst_delete(root$left, value)
  } else if (value > root$value) {
    root$right <- bst_delete(root$right, value)
  } else {
    # Node to delete found

    # Case 1: Leaf node or only one child
    if (is.null(root$left)) {
      return(root$right)
    } else if (is.null(root$right)) {
      return(root$left)
    }

    # Case 2: Two children
    # Find inorder successor (min in right subtree)
    root$value <- bst_find_min(root$right)
    root$right <- bst_delete(root$right, root$value)
  }

  root
}

# ==============================================================================
# Tree Traversals
# ==============================================================================

#' Inorder Traversal (Left, Root, Right)
#'
#' Produces sorted order for BST!
#'
#' Time Complexity: O(n)
#'
#' @param root Root node
#' @return Vector of values in inorder
inorder_traversal <- function(root) {
  if (is.null(root)) {
    return(integer(0))
  }

  c(
    inorder_traversal(root$left),
    root$value,
    inorder_traversal(root$right)
  )
}

#' Preorder Traversal (Root, Left, Right)
#'
#' @param root Root node
#' @return Vector of values in preorder
preorder_traversal <- function(root) {
  if (is.null(root)) {
    return(integer(0))
  }

  c(
    root$value,
    preorder_traversal(root$left),
    preorder_traversal(root$right)
  )
}

#' Postorder Traversal (Left, Right, Root)
#'
#' @param root Root node
#' @return Vector of values in postorder
postorder_traversal <- function(root) {
  if (is.null(root)) {
    return(integer(0))
  }

  c(
    postorder_traversal(root$left),
    postorder_traversal(root$right),
    root$value
  )
}

#' Level-order Traversal (BFS)
#'
#' @param root Root node
#' @return Vector of values in level order
levelorder_traversal <- function(root) {
  if (is.null(root)) {
    return(integer(0))
  }

  result <- integer(0)
  queue <- list(root)

  while (length(queue) > 0) {
    node <- queue[[1]]
    queue <- queue[-1]

    result <- c(result, node$value)

    if (!is.null(node$left)) {
      queue <- c(queue, list(node$left))
    }
    if (!is.null(node$right)) {
      queue <- c(queue, list(node$right))
    }
  }

  result
}

# ==============================================================================
# AVL Tree (Self-Balancing BST)
# ==============================================================================

#' Get Height of Node
#'
#' @param node Tree node
#' @return Height
get_height <- function(node) {
  if (is.null(node)) return(0)
  node$height
}

#' Get Balance Factor
#'
#' @param node Tree node
#' @return Balance factor (left height - right height)
get_balance <- function(node) {
  if (is.null(node)) return(0)
  get_height(node$left) - get_height(node$right)
}

#' Right Rotate
#'
#' @param y Node to rotate
#' @return New root after rotation
right_rotate <- function(y) {
  x <- y$left
  T2 <- x$right

  # Perform rotation
  x$right <- y
  y$left <- T2

  # Update heights
  y$height <- max(get_height(y$left), get_height(y$right)) + 1
  x$height <- max(get_height(x$left), get_height(x$right)) + 1

  x  # Return new root
}

#' Left Rotate
#'
#' @param x Node to rotate
#' @return New root after rotation
left_rotate <- function(x) {
  y <- x$right
  T2 <- y$left

  # Perform rotation
  y$left <- x
  x$right <- T2

  # Update heights
  x$height <- max(get_height(x$left), get_height(x$right)) + 1
  y$height <- max(get_height(y$left), get_height(y$right)) + 1

  y  # Return new root
}

#' Insert into AVL Tree
#'
#' Time Complexity: O(log n) - guaranteed balanced
#' Space Complexity: O(log n) for recursion
#'
#' @param root Root node
#' @param value Value to insert
#' @return New root (balanced)
avl_insert <- function(root, value) {
  # Standard BST insert
  if (is.null(root)) {
    return(create_node(value))
  }

  if (value < root$value) {
    root$left <- avl_insert(root$left, value)
  } else if (value > root$value) {
    root$right <- avl_insert(root$right, value)
  } else {
    return(root)  # Duplicates not allowed
  }

  # Update height
  root$height <- 1 + max(get_height(root$left), get_height(root$right))

  # Get balance factor
  balance <- get_balance(root)

  # Left Left Case
  if (balance > 1 && value < root$left$value) {
    return(right_rotate(root))
  }

  # Right Right Case
  if (balance < -1 && value > root$right$value) {
    return(left_rotate(root))
  }

  # Left Right Case
  if (balance > 1 && value > root$left$value) {
    root$left <- left_rotate(root$left)
    return(right_rotate(root))
  }

  # Right Left Case
  if (balance < -1 && value < root$right$value) {
    root$right <- right_rotate(root$right)
    return(left_rotate(root))
  }

  root
}

#' Get Tree Height
#'
#' @param root Root node
#' @return Height of tree
tree_height <- function(root) {
  if (is.null(root)) return(0)
  1 + max(tree_height(root$left), tree_height(root$right))
}

# ==============================================================================
# Main Program - Examples and Tests
# ==============================================================================

cat("==============================================================================\n")
cat("                TREE DATA STRUCTURES IN R\n")
cat("       Binary Search Trees & Self-Balancing AVL Trees\n")
cat("==============================================================================\n\n")

# Example 1: BST Operations
cat("Example 1: Binary Search Tree (BST)\n")
cat(strrep("=", 80), "\n")

bst_root <- NULL
values <- c(50, 30, 70, 20, 40, 60, 80)

cat(sprintf("Inserting: %s\n", paste(values, collapse = ", ")))
for (val in values) {
  bst_root <- bst_insert(bst_root, val)
}

cat(sprintf("Inorder (sorted): %s\n", paste(inorder_traversal(bst_root), collapse = ", ")))
cat(sprintf("Preorder: %s\n", paste(preorder_traversal(bst_root), collapse = ", ")))
cat(sprintf("Postorder: %s\n", paste(postorder_traversal(bst_root), collapse = ", ")))
cat(sprintf("Level-order: %s\n", paste(levelorder_traversal(bst_root), collapse = ", ")))
cat(sprintf("Tree height: %d\n", tree_height(bst_root)))

cat(sprintf("\nSearch 40: %s\n", bst_search(bst_root, 40)))
cat(sprintf("Search 100: %s\n", bst_search(bst_root, 100)))

cat("\nDeleting 30...\n")
bst_root <- bst_delete(bst_root, 30)
cat(sprintf("Inorder after delete: %s\n\n", paste(inorder_traversal(bst_root), collapse = ", ")))

# Example 2: AVL Tree (Self-Balancing)
cat("Example 2: AVL Tree (Self-Balancing BST)\n")
cat(strrep("=", 80), "\n")

avl_root <- NULL
values <- c(10, 20, 30, 40, 50, 25)

cat(sprintf("Inserting: %s\n", paste(values, collapse = ", ")))
for (val in values) {
  avl_root <- avl_insert(avl_root, val)
}

cat(sprintf("Inorder: %s\n", paste(inorder_traversal(avl_root), collapse = ", ")))
cat(sprintf("Tree height: %d (balanced!)\n", tree_height(avl_root)))
cat(sprintf("Balance factor at root: %d\n\n", get_balance(avl_root)))

# Example 3: Comparison BST vs AVL
cat("Example 3: Comparison - BST vs AVL (Worst Case)\n")
cat(strrep("=", 80), "\n")

# Insert sorted data (worst case for regular BST)
sorted_values <- 1:100

cat("Inserting sorted values 1-100:\n\n")

# Regular BST
bst_root2 <- NULL
for (val in sorted_values) {
  bst_root2 <- bst_insert(bst_root2, val)
}
cat(sprintf("Regular BST height: %d (degenerate - like linked list!)\n", tree_height(bst_root2)))

# AVL Tree
avl_root2 <- NULL
for (val in sorted_values) {
  avl_root2 <- avl_insert(avl_root2, val)
}
cat(sprintf("AVL Tree height: %d (balanced - O(log n))\n\n", tree_height(avl_root2)))

# Summary
cat(strrep("=", 80), "\n")
cat("Summary: Tree Data Structures in R\n")
cat(strrep("=", 80), "\n")
cat("✓ BST: O(log n) average, O(n) worst case\n")
cat("✓ AVL: O(log n) guaranteed (self-balancing)\n")
cat("✓ Traversals: Inorder, Preorder, Postorder, Level-order\n")
cat("\nApplications:\n")
cat("- Databases (indexing)\n")
cat("- File systems (directory structures)\n")
cat("- Priority queues\n")
cat("- Symbol tables in compilers\n")
cat(strrep("=", 80), "\n")
