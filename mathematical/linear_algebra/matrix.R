# ==============================================================================
# Matrix Operations and Linear Algebra in R
#
# Comprehensive collection of matrix operations with focus on statistical
# applications and numerical computing in R.
#
# Features:
# - Leverages R's native matrix operations
# - Statistical applications (PCA, regression, etc.)
# - Efficient vectorized operations
# - Numerical stability considerations
# - Educational implementations showing algorithm steps
#
# Run: Rscript matrix.R
#
# @author Algorithms Multiverse
# @version 1.0
# ==============================================================================

EPSILON <- 1e-10

# ==============================================================================
# Basic Matrix Operations
# ==============================================================================

#' Create Identity Matrix
#'
#' Time Complexity: O(n^2)
#'
#' @param n Size of the identity matrix
#' @return n×n identity matrix
create_identity <- function(n) {
  diag(n)
}

#' Matrix Addition
#'
#' Time Complexity: O(rows * cols)
#'
#' Applications:
#' - Computer graphics transformations
#' - Neural network weight updates
#' - Image processing
#'
#' @param A First matrix
#' @param B Second matrix
#' @return A + B
matrix_add <- function(A, B) {
  if (!all(dim(A) == dim(B))) {
    stop("Matrix dimensions must match for addition")
  }
  return(A + B)
}

#' Matrix Subtraction
#'
#' Time Complexity: O(rows * cols)
#'
#' @param A First matrix
#' @param B Second matrix
#' @return A - B
matrix_subtract <- function(A, B) {
  if (!all(dim(A) == dim(B))) {
    stop("Matrix dimensions must match for subtraction")
  }
  return(A - B)
}

#' Scalar Multiplication
#'
#' Time Complexity: O(rows * cols)
#'
#' @param A Matrix
#' @param scalar Scalar value
#' @return scalar * A
scalar_multiply <- function(A, scalar) {
  return(scalar * A)
}

#' Matrix Transpose
#'
#' Time Complexity: O(rows * cols)
#'
#' Applications:
#' - Solving linear systems
#' - Covariance matrix computation
#' - Neural network backpropagation
#'
#' @param A Matrix
#' @return Transpose of A
matrix_transpose <- function(A) {
  return(t(A))
}

# ==============================================================================
# Matrix Multiplication
# ==============================================================================

#' Standard Matrix Multiplication
#'
#' Time Complexity: O(n^3) for n×n matrices
#' Space Complexity: O(n^2)
#'
#' Algorithm:
#' C[i,j] = Σ(A[i,k] * B[k,j]) for k from 1 to n
#'
#' Applications:
#' - Linear transformations
#' - Graph algorithms (adjacency matrices)
#' - Computer graphics transformations
#' - Neural network forward propagation
#'
#' @param A First matrix (m×n)
#' @param B Second matrix (n×p)
#' @return Product matrix (m×p)
matrix_multiply_standard <- function(A, B) {
  if (ncol(A) != nrow(B)) {
    stop(sprintf("Cannot multiply %dx%d and %dx%d matrices",
                 nrow(A), ncol(A), nrow(B), ncol(B)))
  }

  # Educational implementation showing the algorithm
  m <- nrow(A)
  n <- ncol(A)
  p <- ncol(B)

  C <- matrix(0, nrow = m, ncol = p)

  for (i in 1:m) {
    for (j in 1:p) {
      sum_val <- 0
      for (k in 1:n) {
        sum_val <- sum_val + A[i, k] * B[k, j]
      }
      C[i, j] <- sum_val
    }
  }

  return(C)
}

#' Efficient Matrix Multiplication (using R's built-in)
#'
#' Time Complexity: O(n^3) but highly optimized
#'
#' @param A First matrix
#' @param B Second matrix
#' @return Product matrix
matrix_multiply_fast <- function(A, B) {
  return(A %*% B)
}

# ==============================================================================
# Gaussian Elimination
# ==============================================================================

#' Solve Linear System using Gaussian Elimination
#'
#' Solve Ax = b using Gaussian elimination with partial pivoting
#'
#' Time Complexity: O(n^3)
#' Space Complexity: O(n^2)
#'
#' Algorithm:
#' 1. Forward elimination: Transform to upper triangular form
#' 2. Backward substitution: Solve for x
#'
#' Partial pivoting: Swap rows to avoid division by small numbers
#' This improves numerical stability
#'
#' Applications:
#' - Solving systems of linear equations
#' - Circuit analysis (Kirchhoff's laws)
#' - Structural engineering (finite element analysis)
#' - Economics (input-output models)
#' - Statistical regression
#'
#' @param A Coefficient matrix (n×n)
#' @param b Right-hand side vector (n×1)
#' @return Solution vector x
gaussian_elimination <- function(A, b) {
  n <- nrow(A)

  if (ncol(A) != n || length(b) != n) {
    stop("Invalid dimensions for Gaussian elimination")
  }

  # Make copies to avoid modifying originals
  A_work <- A
  b_work <- b

  # Forward elimination with partial pivoting
  for (col in 1:(n - 1)) {
    # Find pivot (maximum absolute value in column)
    max_row <- col
    max_val <- abs(A_work[col, col])

    for (row in (col + 1):n) {
      if (abs(A_work[row, col]) > max_val) {
        max_val <- abs(A_work[row, col])
        max_row <- row
      }
    }

    # Swap rows
    if (max_row != col) {
      temp_row <- A_work[col, ]
      A_work[col, ] <- A_work[max_row, ]
      A_work[max_row, ] <- temp_row

      temp_b <- b_work[col]
      b_work[col] <- b_work[max_row]
      b_work[max_row] <- temp_b
    }

    # Check for singular matrix
    if (abs(A_work[col, col]) < EPSILON) {
      stop("Matrix is singular or nearly singular")
    }

    # Eliminate column entries below pivot
    for (row in (col + 1):n) {
      factor <- A_work[row, col] / A_work[col, col]
      A_work[row, (col + 1):n] <- A_work[row, (col + 1):n] -
        factor * A_work[col, (col + 1):n]
      b_work[row] <- b_work[row] - factor * b_work[col]
      A_work[row, col] <- 0
    }
  }

  # Backward substitution
  x <- numeric(n)
  for (i in n:1) {
    x[i] <- b_work[i]
    if (i < n) {
      x[i] <- x[i] - sum(A_work[i, (i + 1):n] * x[(i + 1):n])
    }
    x[i] <- x[i] / A_work[i, i]
  }

  return(x)
}

# ==============================================================================
# Matrix Decomposition
# ==============================================================================

#' LU Decomposition
#'
#' LU decomposition: A = LU where L is lower triangular, U is upper triangular
#'
#' Time Complexity: O(n^3)
#' Space Complexity: O(n^2)
#'
#' Algorithm (Doolittle):
#' - L has 1's on diagonal
#' - U has calculated values on and above diagonal
#'
#' Applications:
#' - Solving multiple systems with same A but different b
#' - Computing determinant: det(A) = product of U's diagonal
#' - Matrix inversion
#'
#' @param A Square matrix (n×n)
#' @return List containing L and U matrices
lu_decomposition <- function(A) {
  n <- nrow(A)

  if (ncol(A) != n) {
    stop("LU decomposition requires square matrix")
  }

  L <- matrix(0, n, n)
  U <- matrix(0, n, n)

  for (i in 1:n) {
    # Upper triangular matrix U
    for (k in i:n) {
      sum_val <- 0
      if (i > 1) {
        sum_val <- sum(L[i, 1:(i - 1)] * U[1:(i - 1), k])
      }
      U[i, k] <- A[i, k] - sum_val
    }

    # Lower triangular matrix L
    L[i, i] <- 1  # Diagonal elements

    if (i < n) {
      for (k in (i + 1):n) {
        sum_val <- 0
        if (i > 1) {
          sum_val <- sum(L[k, 1:(i - 1)] * U[1:(i - 1), i])
        }

        if (abs(U[i, i]) < EPSILON) {
          stop("Matrix is singular")
        }

        L[k, i] <- (A[k, i] - sum_val) / U[i, i]
      }
    }
  }

  return(list(L = L, U = U))
}

#' QR Decomposition using Gram-Schmidt
#'
#' A = QR where:
#' - Q is orthogonal (Q^T * Q = I)
#' - R is upper triangular
#'
#' Time Complexity: O(mn^2) for m×n matrix
#' Space Complexity: O(mn)
#'
#' Applications:
#' - Solving least squares problems
#' - Eigenvalue computation (QR algorithm)
#' - Numerical stability in solving linear systems
#' - Linear regression
#'
#' @param A Matrix (m×n)
#' @return List containing Q and R matrices
qr_decomposition_gram_schmidt <- function(A) {
  m <- nrow(A)
  n <- ncol(A)

  Q <- A
  R <- matrix(0, n, n)

  # Modified Gram-Schmidt
  for (j in 1:n) {
    # Compute norm of column j
    R[j, j] <- sqrt(sum(Q[, j]^2))

    if (abs(R[j, j]) < EPSILON) {
      stop("Matrix columns are linearly dependent")
    }

    # Normalize column j
    Q[, j] <- Q[, j] / R[j, j]

    # Orthogonalize remaining columns
    if (j < n) {
      for (k in (j + 1):n) {
        R[j, k] <- sum(Q[, j] * Q[, k])
        Q[, k] <- Q[, k] - R[j, k] * Q[, j]
      }
    }
  }

  return(list(Q = Q, R = R))
}

#' Singular Value Decomposition (using R's built-in)
#'
#' A = U * Σ * V^T where:
#' - U: left singular vectors (m×m orthogonal)
#' - Σ: singular values (m×n diagonal)
#' - V^T: right singular vectors transposed (n×n orthogonal)
#'
#' Applications:
#' - Principal Component Analysis (PCA)
#' - Dimensionality reduction
#' - Image compression
#' - Recommender systems
#'
#' @param A Matrix (m×n)
#' @return List containing U, d (singular values), and V
svd_decomposition <- function(A) {
  return(svd(A))
}

# ==============================================================================
# Determinant Calculation
# ==============================================================================

#' Determinant using Recursive Cofactor Expansion
#'
#' Time Complexity: O(n!) - very slow for large matrices
#' Best for: Small matrices (n <= 4)
#'
#' @param A Square matrix
#' @return Determinant of A
determinant_recursive <- function(A) {
  n <- nrow(A)

  if (ncol(A) != n) {
    stop("Determinant requires square matrix")
  }

  if (n == 1) {
    return(A[1, 1])
  }

  if (n == 2) {
    return(A[1, 1] * A[2, 2] - A[1, 2] * A[2, 1])
  }

  det <- 0

  for (j in 1:n) {
    # Create submatrix (remove row 1, column j)
    submatrix <- A[2:n, -j, drop = FALSE]

    cofactor <- ((-1)^(1 + j)) * A[1, j] * determinant_recursive(submatrix)
    det <- det + cofactor
  }

  return(det)
}

#' Determinant using LU Decomposition
#'
#' Time Complexity: O(n^3)
#' Best for: Matrices larger than 4×4
#'
#' @param A Square matrix
#' @return Determinant of A
determinant_lu <- function(A) {
  n <- nrow(A)

  if (ncol(A) != n) {
    stop("Determinant requires square matrix")
  }

  tryCatch({
    decomp <- lu_decomposition(A)
    U <- decomp$U

    # Determinant is product of diagonal elements of U
    det <- prod(diag(U))
    return(det)
  }, error = function(e) {
    return(0)  # Singular matrix
  })
}

#' Determinant using R's built-in (most efficient)
#'
#' @param A Square matrix
#' @return Determinant of A
determinant_fast <- function(A) {
  return(det(A))
}

# ==============================================================================
# Matrix Inversion
# ==============================================================================

#' Matrix Inversion using Gauss-Jordan Elimination
#'
#' Time Complexity: O(n^3)
#' Space Complexity: O(n^2)
#'
#' Applications:
#' - Solving linear systems
#' - Computer graphics transformations
#' - Control systems
#' - Statistics (covariance matrix inversion)
#'
#' @param A Square matrix (n×n)
#' @return Inverse of A
matrix_inverse_gauss_jordan <- function(A) {
  n <- nrow(A)

  if (ncol(A) != n) {
    stop("Matrix inversion requires square matrix")
  }

  # Create augmented matrix [A|I]
  augmented <- cbind(A, diag(n))

  # Gauss-Jordan elimination
  for (col in 1:n) {
    # Find pivot
    max_row <- col
    max_val <- abs(augmented[col, col])

    if (col < n) {
      for (row in (col + 1):n) {
        if (abs(augmented[row, col]) > max_val) {
          max_val <- abs(augmented[row, col])
          max_row <- row
        }
      }
    }

    # Swap rows
    if (max_row != col) {
      temp_row <- augmented[col, ]
      augmented[col, ] <- augmented[max_row, ]
      augmented[max_row, ] <- temp_row
    }

    # Check for singular matrix
    if (abs(augmented[col, col]) < EPSILON) {
      stop("Matrix is singular and cannot be inverted")
    }

    # Scale pivot row
    pivot <- augmented[col, col]
    augmented[col, ] <- augmented[col, ] / pivot

    # Eliminate column
    for (row in 1:n) {
      if (row != col) {
        factor <- augmented[row, col]
        augmented[row, ] <- augmented[row, ] - factor * augmented[col, ]
      }
    }
  }

  # Extract inverse from right half
  inverse <- augmented[, (n + 1):(2 * n)]

  return(inverse)
}

#' Matrix Inversion using R's built-in (most efficient)
#'
#' @param A Square matrix
#' @return Inverse of A
matrix_inverse_fast <- function(A) {
  return(solve(A))
}

# ==============================================================================
# Eigenvalue Computation
# ==============================================================================

#' Power Iteration for Dominant Eigenvalue
#'
#' Time Complexity: O(n^2 * iterations)
#'
#' Applications:
#' - Google PageRank algorithm
#' - Principal Component Analysis (PCA)
#' - Markov chains (stationary distribution)
#'
#' @param A Square matrix (n×n)
#' @param max_iter Maximum number of iterations
#' @return List containing eigenvalue and eigenvector
power_iteration <- function(A, max_iter = 100) {
  n <- nrow(A)

  if (ncol(A) != n) {
    stop("Power iteration requires square matrix")
  }

  # Initialize with random vector
  v <- rnorm(n)

  # Normalize
  v <- v / sqrt(sum(v^2))

  # Power iteration
  for (iter in 1:max_iter) {
    # Multiply by matrix
    v_new <- A %*% v

    # Normalize
    v_new <- v_new / sqrt(sum(v_new^2))

    # Check convergence
    diff <- sum(abs(v_new - v))
    if (diff < EPSILON) {
      break
    }

    v <- v_new
  }

  # Compute eigenvalue: λ = v^T * A * v
  eigenvalue <- as.numeric(t(v) %*% A %*% v)

  return(list(eigenvalue = eigenvalue, eigenvector = as.vector(v)))
}

#' Eigenvalues using R's built-in (most efficient)
#'
#' @param A Square matrix
#' @return Eigenvalues and eigenvectors
eigenvalues_fast <- function(A) {
  return(eigen(A))
}

# ==============================================================================
# Statistical Applications
# ==============================================================================

#' Principal Component Analysis using SVD
#'
#' @param X Data matrix (samples × features)
#' @param n_components Number of principal components
#' @return List containing transformed data and components
pca_transform <- function(X, n_components) {
  # Center the data
  X_centered <- scale(X, center = TRUE, scale = FALSE)

  # Compute SVD
  svd_result <- svd(X_centered)

  # Extract principal components
  components <- svd_result$v[, 1:n_components, drop = FALSE]

  # Transform data
  X_transformed <- X_centered %*% components

  # Explained variance
  explained_variance <- svd_result$d[1:n_components]^2 / sum(svd_result$d^2)

  return(list(
    transformed = X_transformed,
    components = components,
    explained_variance = explained_variance
  ))
}

#' Linear Regression using Normal Equations
#'
#' Solves: β = (X^T * X)^(-1) * X^T * y
#'
#' @param X Design matrix (n × p)
#' @param y Response vector (n × 1)
#' @return Coefficient vector β
linear_regression <- function(X, y) {
  # Add intercept column
  X_design <- cbind(1, X)

  # Normal equations: β = (X^T * X)^(-1) * X^T * y
  XtX <- t(X_design) %*% X_design
  Xty <- t(X_design) %*% y

  beta <- solve(XtX) %*% Xty

  return(as.vector(beta))
}

# ==============================================================================
# Example Usage and Tests
# ==============================================================================

example_multiplication <- function() {
  cat("\n======================================\n")
  cat("Example 1: Matrix Multiplication\n")
  cat("======================================\n\n")

  A <- matrix(c(1, 4, 2, 5, 3, 6), nrow = 2, byrow = TRUE)
  B <- matrix(c(7, 9, 11, 8, 10, 12), nrow = 3, byrow = TRUE)

  C <- matrix_multiply_standard(A, B)

  cat("A (2x3):\n")
  print(A)
  cat("\nB (3x2):\n")
  print(B)
  cat("\nC = A × B (2x2):\n")
  print(C)
}

example_gaussian_elimination <- function() {
  cat("\n======================================\n")
  cat("Example 2: Gaussian Elimination\n")
  cat("======================================\n\n")

  A <- matrix(c(2, 1, -1, -3, -1, 2, -2, 1, 2), nrow = 3, byrow = TRUE)
  b <- c(8, -11, -3)

  x <- gaussian_elimination(A, b)

  cat("Solution x:\n")
  print(x)
  cat("\nExpected: x=2, y=3, z=-1\n")
}

example_lu_decomposition <- function() {
  cat("\n======================================\n")
  cat("Example 3: LU Decomposition\n")
  cat("======================================\n\n")

  A <- matrix(c(2, -1, -2, -4, 6, 3, -4, -2, 8), nrow = 3, byrow = TRUE)

  decomp <- lu_decomposition(A)

  cat("A:\n")
  print(A)
  cat("\nL (lower triangular):\n")
  print(decomp$L)
  cat("\nU (upper triangular):\n")
  print(decomp$U)
}

example_matrix_inverse <- function() {
  cat("\n======================================\n")
  cat("Example 4: Matrix Inversion\n")
  cat("======================================\n\n")

  A <- matrix(c(4, 7, 2, 6), nrow = 2, byrow = TRUE)

  A_inv <- matrix_inverse_gauss_jordan(A)

  cat("A:\n")
  print(A)
  cat("\nA^(-1):\n")
  print(A_inv)

  I <- A %*% A_inv
  cat("\nA × A^(-1) (should be identity):\n")
  print(I)
}

example_eigenvalues <- function() {
  cat("\n======================================\n")
  cat("Example 5: Eigenvalue Computation\n")
  cat("======================================\n\n")

  A <- matrix(c(2, 1, 1, 2), nrow = 2, byrow = TRUE)

  result <- power_iteration(A, max_iter = 100)

  cat("A:\n")
  print(A)
  cat(sprintf("\nDominant eigenvalue: %.6f\n", result$eigenvalue))
  cat("\nCorresponding eigenvector:\n")
  print(result$eigenvector)
}

example_determinant <- function() {
  cat("\n======================================\n")
  cat("Example 6: Determinant Calculation\n")
  cat("======================================\n\n")

  A <- matrix(c(1, 2, 3, 4, 5, 6, 7, 8, 9), nrow = 3, byrow = TRUE)

  det_lu <- determinant_lu(A)

  cat("A:\n")
  print(A)
  cat(sprintf("\nDeterminant (LU): %.6f\n", det_lu))
}

# Main execution
main <- function() {
  cat("======================================\n")
  cat("Matrix Operations and Linear Algebra\n")
  cat("======================================\n")

  example_multiplication()
  example_gaussian_elimination()
  example_lu_decomposition()
  example_matrix_inverse()
  example_eigenvalues()
  example_determinant()

  cat("\n======================================\n")
  cat("All examples completed successfully!\n")
  cat("======================================\n")
}

# Run main if script is executed directly
if (!interactive()) {
  main()
}
