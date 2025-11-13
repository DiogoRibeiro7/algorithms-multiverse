# ==============================================================================
# Regression Algorithms in R
#
# Comprehensive collection of regression methods - R's statistical strength!
#
# Implementations:
# - Simple Linear Regression (OLS)
# - Multiple Linear Regression
# - Polynomial Regression
# - Ridge Regression (L2 regularization)
# - Lasso Regression (L1 regularization)
# - Logistic Regression (binary classification)
# - Weighted Least Squares
#
# R excels at regression analysis with efficient matrix operations and
# built-in statistical functions. These implementations showcase both
# the algorithmic foundations and R's vectorization capabilities.
#
# Run: Rscript regression.R
#
# @author Algorithms Multiverse
# @version 1.0
# ==============================================================================

EPSILON <- 1e-10

# ==============================================================================
# Simple Linear Regression
# ==============================================================================

#' Simple Linear Regression
#'
#' Fits y = β₀ + β₁x using Ordinary Least Squares (OLS)
#'
#' Time Complexity: O(n)
#' Space Complexity: O(1)
#'
#' Formula:
#' β₁ = Cov(x,y) / Var(x)
#' β₀ = mean(y) - β₁ * mean(x)
#'
#' Applications:
#' - Predicting continuous outcomes
#' - Trend analysis
#' - Econometrics
#' - Scientific data analysis
#'
#' @param x Predictor variable (vector)
#' @param y Response variable (vector)
#' @return List with coefficients, predictions, R², residuals
simple_linear_regression <- function(x, y) {
  n <- length(x)

  # Calculate means
  x_mean <- mean(x)
  y_mean <- mean(y)

  # Calculate slope (β₁) and intercept (β₀)
  numerator <- sum((x - x_mean) * (y - y_mean))
  denominator <- sum((x - x_mean)^2)

  if (abs(denominator) < EPSILON) {
    stop("Cannot fit regression: x has zero variance")
  }

  beta_1 <- numerator / denominator
  beta_0 <- y_mean - beta_1 * x_mean

  # Predictions and residuals
  y_pred <- beta_0 + beta_1 * x
  residuals <- y - y_pred

  # R-squared (coefficient of determination)
  ss_total <- sum((y - y_mean)^2)
  ss_residual <- sum(residuals^2)
  r_squared <- 1 - (ss_residual / ss_total)

  # Standard error
  std_error <- sqrt(ss_residual / (n - 2))

  list(
    coefficients = c(intercept = beta_0, slope = beta_1),
    predictions = y_pred,
    residuals = residuals,
    r_squared = r_squared,
    std_error = std_error
  )
}

# ==============================================================================
# Multiple Linear Regression
# ==============================================================================

#' Multiple Linear Regression
#'
#' Fits y = β₀ + β₁x₁ + β₂x₂ + ... + βₚxₚ using matrix algebra
#'
#' Time Complexity: O(np² + p³) where n = samples, p = features
#' Space Complexity: O(np)
#'
#' Formula: β = (X'X)⁻¹X'y
#'
#' Applications:
#' - Multivariate prediction
#' - Feature importance analysis
#' - Econometric modeling
#' - Machine learning baselines
#'
#' @param X Design matrix (n × p)
#' @param y Response vector (n × 1)
#' @return List with coefficients, predictions, R², residuals
multiple_linear_regression <- function(X, y) {
  # Add intercept column
  X <- cbind(1, X)
  n <- nrow(X)
  p <- ncol(X)

  # Calculate coefficients: β = (X'X)⁻¹X'y
  XtX <- t(X) %*% X
  Xty <- t(X) %*% y

  # Solve system (more stable than explicit inverse)
  beta <- solve(XtX, Xty)

  # Predictions
  y_pred <- X %*% beta
  residuals <- y - y_pred

  # Statistics
  y_mean <- mean(y)
  ss_total <- sum((y - y_mean)^2)
  ss_residual <- sum(residuals^2)
  r_squared <- 1 - (ss_residual / ss_total)

  # Adjusted R²
  adj_r_squared <- 1 - ((1 - r_squared) * (n - 1) / (n - p))

  # Standard errors
  std_error <- sqrt(ss_residual / (n - p))

  list(
    coefficients = as.vector(beta),
    predictions = as.vector(y_pred),
    residuals = as.vector(residuals),
    r_squared = r_squared,
    adj_r_squared = adj_r_squared,
    std_error = std_error
  )
}

# ==============================================================================
# Polynomial Regression
# ==============================================================================

#' Polynomial Regression
#'
#' Fits y = β₀ + β₁x + β₂x² + ... + βₚxᵖ
#'
#' Time Complexity: O(np² + p³)
#' Space Complexity: O(np)
#'
#' Applications:
#' - Non-linear trend modeling
#' - Curve fitting
#' - Growth curves
#'
#' @param x Predictor variable
#' @param y Response variable
#' @param degree Polynomial degree (default: 2)
#' @return List with coefficients, predictions, R²
polynomial_regression <- function(x, y, degree = 2) {
  # Create polynomial features
  X <- matrix(0, nrow = length(x), ncol = degree)
  for (i in 1:degree) {
    X[, i] <- x^i
  }

  # Use multiple linear regression
  result <- multiple_linear_regression(X, y)
  result$degree <- degree
  result
}

# ==============================================================================
# Ridge Regression (L2 Regularization)
# ==============================================================================

#' Ridge Regression
#'
#' Fits y = Xβ with L2 penalty: min ||y - Xβ||² + λ||β||²
#'
#' Time Complexity: O(np² + p³)
#' Space Complexity: O(np)
#'
#' Formula: β = (X'X + λI)⁻¹X'y
#'
#' Applications:
#' - Preventing overfitting
#' - Multicollinearity handling
#' - High-dimensional regression
#' - Machine learning regularization
#'
#' @param X Design matrix
#' @param y Response vector
#' @param lambda Regularization parameter (default: 1.0)
#' @return List with coefficients, predictions
ridge_regression <- function(X, y, lambda = 1.0) {
  # Add intercept
  X <- cbind(1, X)
  p <- ncol(X)

  # Ridge formula: β = (X'X + λI)⁻¹X'y
  XtX <- t(X) %*% X

  # Add penalty (don't penalize intercept)
  penalty <- diag(c(0, rep(lambda, p - 1)))

  beta <- solve(XtX + penalty, t(X) %*% y)

  # Predictions
  y_pred <- X %*% beta
  residuals <- y - y_pred

  list(
    coefficients = as.vector(beta),
    predictions = as.vector(y_pred),
    residuals = as.vector(residuals),
    lambda = lambda
  )
}

# ==============================================================================
# Lasso Regression (L1 Regularization)
# ==============================================================================

#' Lasso Regression (Coordinate Descent)
#'
#' Fits y = Xβ with L1 penalty: min ||y - Xβ||² + λ||β||₁
#'
#' Time Complexity: O(iterations × n × p)
#' Space Complexity: O(np)
#'
#' Features:
#' - Sparse solutions (feature selection)
#' - Sets irrelevant coefficients to zero
#'
#' Applications:
#' - Feature selection
#' - High-dimensional data
#' - Compressed sensing
#'
#' @param X Design matrix
#' @param y Response vector
#' @param lambda Regularization parameter
#' @param max_iter Maximum iterations (default: 1000)
#' @param tol Convergence tolerance (default: 1e-6)
#' @return List with coefficients, predictions
lasso_regression <- function(X, y, lambda = 1.0, max_iter = 1000, tol = 1e-6) {
  # Standardize features
  X <- scale(X)
  y <- y - mean(y)

  n <- nrow(X)
  p <- ncol(X)
  beta <- rep(0, p)

  # Coordinate descent
  for (iter in 1:max_iter) {
    beta_old <- beta

    for (j in 1:p) {
      # Partial residual
      r <- y - X %*% beta + X[, j] * beta[j]

      # Correlation
      rho <- sum(X[, j] * r) / n

      # Soft thresholding
      if (rho < -lambda) {
        beta[j] <- rho + lambda
      } else if (rho > lambda) {
        beta[j] <- rho - lambda
      } else {
        beta[j] <- 0
      }
    }

    # Check convergence
    if (max(abs(beta - beta_old)) < tol) {
      break
    }
  }

  # Predictions
  y_pred <- X %*% beta

  list(
    coefficients = as.vector(beta),
    predictions = as.vector(y_pred),
    lambda = lambda,
    iterations = iter
  )
}

# ==============================================================================
# Logistic Regression
# ==============================================================================

#' Logistic Regression (Binary Classification)
#'
#' Fits P(y=1|x) = 1 / (1 + exp(-Xβ)) using gradient descent
#'
#' Time Complexity: O(iterations × n × p)
#' Space Complexity: O(np)
#'
#' Applications:
#' - Binary classification
#' - Probability prediction
#' - Credit scoring
#' - Medical diagnosis
#'
#' @param X Design matrix
#' @param y Binary response (0 or 1)
#' @param learning_rate Learning rate (default: 0.01)
#' @param max_iter Maximum iterations (default: 1000)
#' @param tol Convergence tolerance (default: 1e-6)
#' @return List with coefficients, predictions, probabilities
logistic_regression <- function(X, y, learning_rate = 0.01, max_iter = 1000, tol = 1e-6) {
  # Add intercept
  X <- cbind(1, X)
  n <- nrow(X)
  p <- ncol(X)
  beta <- rep(0, p)

  # Sigmoid function
  sigmoid <- function(z) {
    1 / (1 + exp(-z))
  }

  # Gradient descent
  for (iter in 1:max_iter) {
    # Predictions
    z <- X %*% beta
    predictions <- sigmoid(z)

    # Gradient
    gradient <- t(X) %*% (predictions - y) / n

    # Update
    beta_new <- beta - learning_rate * gradient

    # Check convergence
    if (max(abs(beta_new - beta)) < tol) {
      beta <- beta_new
      break
    }

    beta <- beta_new
  }

  # Final predictions
  probabilities <- sigmoid(X %*% beta)
  predicted_class <- ifelse(probabilities >= 0.5, 1, 0)

  # Accuracy
  accuracy <- mean(predicted_class == y)

  list(
    coefficients = as.vector(beta),
    probabilities = as.vector(probabilities),
    predictions = predicted_class,
    accuracy = accuracy,
    iterations = iter
  )
}

# ==============================================================================
# Weighted Least Squares
# ==============================================================================

#' Weighted Least Squares Regression
#'
#' Fits y = Xβ with weights: min Σwᵢ(yᵢ - xᵢβ)²
#'
#' Time Complexity: O(np² + p³)
#' Space Complexity: O(np)
#'
#' Applications:
#' - Heteroscedastic data
#' - Handling outliers
#' - Precision weighting
#'
#' @param X Design matrix
#' @param y Response vector
#' @param weights Weight vector (default: equal weights)
#' @return List with coefficients, predictions
weighted_least_squares <- function(X, y, weights = NULL) {
  if (is.null(weights)) {
    weights <- rep(1, length(y))
  }

  # Add intercept
  X <- cbind(1, X)

  # Create weight matrix
  W <- diag(weights)

  # Weighted formula: β = (X'WX)⁻¹X'Wy
  XtWX <- t(X) %*% W %*% X
  XtWy <- t(X) %*% W %*% y

  beta <- solve(XtWX, XtWy)

  # Predictions
  y_pred <- X %*% beta

  list(
    coefficients = as.vector(beta),
    predictions = as.vector(y_pred),
    weights = weights
  )
}

# ==============================================================================
# Main Program - Examples and Tests
# ==============================================================================

cat("==============================================================================\n")
cat("                REGRESSION ALGORITHMS IN R\n")
cat("         Showcasing R's Statistical Computing Strength!\n")
cat("==============================================================================\n\n")

# ==============================================================================
# Example 1: Simple Linear Regression
# ==============================================================================

cat("Example 1: Simple Linear Regression\n")
cat("================================================================================\n")
set.seed(42)
x <- 1:50
y <- 3 + 2 * x + rnorm(50, 0, 5)

result <- simple_linear_regression(x, y)
cat(sprintf("True model: y = 3 + 2x + noise\n"))
cat(sprintf("Fitted model: y = %.4f + %.4f*x\n",
            result$coefficients["intercept"],
            result$coefficients["slope"]))
cat(sprintf("R² = %.4f\n", result$r_squared))
cat(sprintf("Standard Error = %.4f\n\n", result$std_error))

# ==============================================================================
# Example 2: Multiple Linear Regression
# ==============================================================================

cat("Example 2: Multiple Linear Regression\n")
cat("================================================================================\n")
set.seed(42)
n <- 100
X <- matrix(rnorm(n * 3), ncol = 3)
true_beta <- c(5, 2, -3, 1)  # intercept + 3 coefficients
y <- true_beta[1] + X %*% true_beta[-1] + rnorm(n, 0, 1)

result <- multiple_linear_regression(X, y)
cat("True coefficients: ", true_beta, "\n")
cat("Estimated coefficients: ", round(result$coefficients, 4), "\n")
cat(sprintf("R² = %.4f\n", result$r_squared))
cat(sprintf("Adjusted R² = %.4f\n\n", result$adj_r_squared))

# ==============================================================================
# Example 3: Polynomial Regression
# ==============================================================================

cat("Example 3: Polynomial Regression (Degree 2)\n")
cat("================================================================================\n")
set.seed(42)
x <- seq(0, 10, length.out = 50)
y <- 2 + 3*x - 0.5*x^2 + rnorm(50, 0, 2)

result <- polynomial_regression(x, y, degree = 2)
cat(sprintf("Polynomial degree: %d\n", result$degree))
cat(sprintf("R² = %.4f\n\n", result$r_squared))

# ==============================================================================
# Example 4: Ridge Regression
# ==============================================================================

cat("Example 4: Ridge Regression (L2 Regularization)\n")
cat("================================================================================\n")
set.seed(42)
n <- 50
p <- 10
X <- matrix(rnorm(n * p), ncol = p)
true_beta <- c(2, -1, 3, 0, 0, 0, 0, 0, 0, 0)
y <- X %*% true_beta + rnorm(n, 0, 1)

# Compare different lambda values
lambdas <- c(0, 0.1, 1, 10)
cat("Effect of regularization parameter λ:\n\n")
cat(sprintf("%-12s %-12s %-12s\n", "Lambda", "||β||²", "MSE"))
cat(strrep("-", 40), "\n")

for (lambda in lambdas) {
  result <- ridge_regression(X, y, lambda = lambda)
  beta_norm <- sum(result$coefficients[-1]^2)  # Exclude intercept
  mse <- mean(result$residuals^2)
  cat(sprintf("%-12.1f %-12.4f %-12.4f\n", lambda, beta_norm, mse))
}
cat("\n")

# ==============================================================================
# Example 5: Logistic Regression
# ==============================================================================

cat("Example 5: Logistic Regression (Binary Classification)\n")
cat("================================================================================\n")
set.seed(42)
n <- 200
X <- matrix(rnorm(n * 2), ncol = 2)
true_beta <- c(0, 1.5, -2)
prob <- 1 / (1 + exp(-(cbind(1, X) %*% true_beta)))
y <- rbinom(n, 1, prob)

result <- logistic_regression(X, y, learning_rate = 0.1, max_iter = 1000)
cat("True coefficients: ", true_beta, "\n")
cat("Estimated coefficients: ", round(result$coefficients, 4), "\n")
cat(sprintf("Classification accuracy: %.2f%%\n", result$accuracy * 100))
cat(sprintf("Converged in %d iterations\n\n", result$iterations))

# ==============================================================================
# Summary
# ==============================================================================

cat("==============================================================================\n")
cat("Summary: R Regression Capabilities\n")
cat("==============================================================================\n")
cat("✓ Simple Linear: O(n) - Fast, interpretable baseline\n")
cat("✓ Multiple Linear: O(np² + p³) - Multivariate predictions\n")
cat("✓ Polynomial: Captures non-linear relationships\n")
cat("✓ Ridge: L2 regularization prevents overfitting\n")
cat("✓ Lasso: L1 regularization for feature selection\n")
cat("✓ Logistic: Binary classification with probabilities\n")
cat("✓ Weighted LS: Handles heteroscedasticity\n")
cat("\n")
cat("R's Advantages:\n")
cat("- Efficient matrix operations\n")
cat("- Built-in statistical functions\n")
cat("- Vectorized computations\n")
cat("- Natural integration with data frames\n")
cat("==============================================================================\n")
