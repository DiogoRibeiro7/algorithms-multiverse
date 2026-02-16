#!/usr/bin/env python3
"""
Linear Regression Implementation

Linear regression is a fundamental supervised learning algorithm that models
the relationship between a dependent variable and one or more independent variables
by fitting a linear equation to observed data.

The algorithm finds the best-fitting line through the data points by minimizing
the sum of squared differences between predicted and actual values (least squares).

Key Concepts:
- Hypothesis: h(x) = θ₀ + θ₁x₁ + θ₂x₂ + ... + θₙxₙ
- Cost Function: J(θ) = (1/2m) Σ(h(x) - y)²
- Optimization: Gradient Descent or Normal Equation

Time Complexity:
- Training: O(n*m*iterations) for gradient descent, O(n³) for normal equation
- Prediction: O(n) where n is number of features
Space Complexity: O(n*m) for storing training data

Applications:
- Predicting continuous values (prices, temperatures, scores)
- Trend analysis and forecasting
- Feature importance analysis
- Baseline model for regression tasks

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import Optional, Tuple, List, Union
import matplotlib.pyplot as plt


class LinearRegression:
    """
    Linear Regression using Gradient Descent and Normal Equation

    This implementation provides both gradient descent and normal equation
    methods for finding optimal parameters.

    Attributes:
        weights (np.ndarray): Model parameters (θ)
        bias (float): Intercept term (θ₀)
        cost_history (List[float]): Training cost over iterations
        learning_rate (float): Step size for gradient descent
        n_iterations (int): Number of training iterations
        regularization (float): L2 regularization parameter (lambda)
    """

    def __init__(self, learning_rate: float = 0.01,
                 n_iterations: int = 1000,
                 regularization: float = 0.0,
                 verbose: bool = False):
        """
        Initialize Linear Regression model

        Args:
            learning_rate: Learning rate for gradient descent (α)
            n_iterations: Number of gradient descent iterations
            regularization: L2 regularization strength (0 = no regularization)
            verbose: Print training progress
        """
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.regularization = regularization
        self.verbose = verbose
        self.weights = None
        self.bias = None
        self.cost_history = []

    def _add_intercept(self, X: np.ndarray) -> np.ndarray:
        """Add intercept term (column of ones) to feature matrix"""
        intercept = np.ones((X.shape[0], 1))
        return np.concatenate((intercept, X), axis=1)

    def _cost_function(self, X: np.ndarray, y: np.ndarray,
                       theta: np.ndarray) -> float:
        """
        Calculate Mean Squared Error cost with optional L2 regularization

        J(θ) = (1/2m) * Σ(h(x) - y)² + (λ/2m) * Σθⱼ²

        Args:
            X: Feature matrix with intercept (m x n+1)
            y: Target values (m x 1)
            theta: Model parameters (n+1 x 1)

        Returns:
            Cost value
        """
        m = len(y)
        predictions = X @ theta
        base_cost = (1/(2*m)) * np.sum((predictions - y)**2)

        # Add L2 regularization (exclude bias term)
        if self.regularization > 0:
            reg_cost = (self.regularization/(2*m)) * np.sum(theta[1:]**2)
            return base_cost + reg_cost

        return base_cost

    def _gradient_descent(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Perform gradient descent optimization

        θ = θ - α * ∇J(θ)

        Args:
            X: Feature matrix with intercept (m x n+1)
            y: Target values (m x 1)

        Returns:
            Optimized parameters theta
        """
        m = len(y)
        theta = np.zeros((X.shape[1], 1))

        for i in range(self.n_iterations):
            # Calculate predictions
            predictions = X @ theta

            # Calculate gradients
            gradients = (1/m) * X.T @ (predictions - y)

            # Add L2 regularization gradient (exclude bias)
            if self.regularization > 0:
                reg_term = (self.regularization/m) * theta
                reg_term[0] = 0  # Don't regularize bias
                gradients += reg_term

            # Update parameters
            theta -= self.learning_rate * gradients

            # Store cost
            cost = self._cost_function(X, y, theta)
            self.cost_history.append(cost)

            if self.verbose and i % 100 == 0:
                print(f"Iteration {i}, Cost: {cost:.6f}")

        return theta

    def _normal_equation(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Calculate parameters using Normal Equation (closed-form solution)

        θ = (X^T X)^(-1) X^T y

        With L2 regularization:
        θ = (X^T X + λI)^(-1) X^T y

        Args:
            X: Feature matrix with intercept (m x n+1)
            y: Target values (m x 1)

        Returns:
            Optimal parameters theta
        """
        # Create regularization matrix
        if self.regularization > 0:
            L = self.regularization * np.eye(X.shape[1])
            L[0, 0] = 0  # Don't regularize bias
        else:
            L = 0

        # Calculate using normal equation
        theta = np.linalg.inv(X.T @ X + L) @ X.T @ y
        return theta

    def fit(self, X: np.ndarray, y: np.ndarray,
            method: str = 'gradient_descent') -> 'LinearRegression':
        """
        Train the linear regression model

        Args:
            X: Training features (m x n)
            y: Training targets (m x 1)
            method: 'gradient_descent' or 'normal_equation'

        Returns:
            Self (for method chaining)
        """
        # Reshape y if necessary
        if len(y.shape) == 1:
            y = y.reshape(-1, 1)

        # Add intercept term
        X_with_intercept = self._add_intercept(X)

        # Choose optimization method
        if method == 'gradient_descent':
            theta = self._gradient_descent(X_with_intercept, y)
        elif method == 'normal_equation':
            theta = self._normal_equation(X_with_intercept, y)
        else:
            raise ValueError(f"Unknown method: {method}")

        # Store parameters
        self.bias = theta[0, 0]
        self.weights = theta[1:].flatten()

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions on new data

        Args:
            X: Feature matrix (m x n)

        Returns:
            Predictions (m x 1)
        """
        if self.weights is None:
            raise ValueError("Model must be trained before prediction")

        return X @ self.weights + self.bias

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate R² score (coefficient of determination)

        R² = 1 - (SS_res / SS_tot)

        Args:
            X: Feature matrix (m x n)
            y: True values (m x 1)

        Returns:
            R² score (1.0 = perfect fit, 0.0 = baseline)
        """
        predictions = self.predict(X)
        ss_res = np.sum((y - predictions)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        return 1 - (ss_res / ss_tot)

    def get_metrics(self, X: np.ndarray, y: np.ndarray) -> dict:
        """
        Calculate various regression metrics

        Args:
            X: Feature matrix
            y: True values

        Returns:
            Dictionary with MSE, RMSE, MAE, R² metrics
        """
        predictions = self.predict(X)
        n = len(y)

        mse = np.mean((y - predictions)**2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y - predictions))
        r2 = self.score(X, y)

        return {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2': r2
        }

    def plot_cost_history(self):
        """Plot training cost over iterations"""
        if not self.cost_history:
            print("No cost history available. Train with gradient descent first.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(self.cost_history)
        plt.title('Cost Function During Training')
        plt.xlabel('Iteration')
        plt.ylabel('Cost')
        plt.grid(True)
        plt.show()

    def plot_fit(self, X: np.ndarray, y: np.ndarray):
        """
        Plot data points and fitted line (for 1D features only)

        Args:
            X: Feature matrix (must be 1D)
            y: Target values
        """
        if X.shape[1] != 1:
            print("Plotting only works for single-feature datasets")
            return

        plt.figure(figsize=(10, 6))
        plt.scatter(X, y, alpha=0.5, label='Data points')

        # Create line points
        X_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
        y_line = self.predict(X_line)

        plt.plot(X_line, y_line, 'r-', label='Fitted line')
        plt.xlabel('X')
        plt.ylabel('y')
        plt.title('Linear Regression Fit')
        plt.legend()
        plt.grid(True)
        plt.show()


class MultipleLinearRegression(LinearRegression):
    """
    Extended Linear Regression with feature scaling and polynomial features

    Adds preprocessing capabilities for better convergence and non-linear fits.
    """

    def __init__(self, *args, feature_scaling: bool = True,
                 polynomial_degree: int = 1, **kwargs):
        """
        Initialize Multiple Linear Regression

        Args:
            feature_scaling: Normalize features to mean=0, std=1
            polynomial_degree: Degree of polynomial features (1 = linear)
            *args, **kwargs: Arguments for parent LinearRegression
        """
        super().__init__(*args, **kwargs)
        self.feature_scaling = feature_scaling
        self.polynomial_degree = polynomial_degree
        self.mean = None
        self.std = None

    def _normalize_features(self, X: np.ndarray,
                          fit: bool = False) -> np.ndarray:
        """
        Normalize features to zero mean and unit variance

        Args:
            X: Feature matrix
            fit: Whether to fit normalization parameters

        Returns:
            Normalized features
        """
        if fit:
            self.mean = np.mean(X, axis=0)
            self.std = np.std(X, axis=0)
            self.std[self.std == 0] = 1  # Avoid division by zero

        return (X - self.mean) / self.std

    def _polynomial_features(self, X: np.ndarray) -> np.ndarray:
        """
        Generate polynomial features up to specified degree

        For degree=2: [x₁, x₂] → [x₁, x₂, x₁², x₁x₂, x₂²]

        Args:
            X: Original features

        Returns:
            Polynomial features
        """
        if self.polynomial_degree == 1:
            return X

        n_samples, n_features = X.shape
        features = [X]

        for degree in range(2, self.polynomial_degree + 1):
            # Add powers of each feature
            for i in range(n_features):
                features.append(X[:, i:i+1] ** degree)

        return np.concatenate(features, axis=1)

    def fit(self, X: np.ndarray, y: np.ndarray,
            method: str = 'gradient_descent') -> 'MultipleLinearRegression':
        """
        Train with optional feature preprocessing

        Args:
            X: Training features
            y: Training targets
            method: Optimization method

        Returns:
            Self
        """
        # Generate polynomial features
        X_poly = self._polynomial_features(X)

        # Normalize if requested
        if self.feature_scaling:
            X_processed = self._normalize_features(X_poly, fit=True)
        else:
            X_processed = X_poly

        # Train model
        return super().fit(X_processed, y, method)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict with same preprocessing as training

        Args:
            X: Feature matrix

        Returns:
            Predictions
        """
        # Apply same preprocessing
        X_poly = self._polynomial_features(X)

        if self.feature_scaling:
            X_processed = self._normalize_features(X_poly, fit=False)
        else:
            X_processed = X_poly

        return super().predict(X_processed)


def example_simple_regression():
    """Example: Simple linear regression with synthetic data"""
    print("=" * 60)
    print("Simple Linear Regression Example")
    print("=" * 60)

    # Generate synthetic data
    np.random.seed(42)
    X = 2 * np.random.rand(100, 1)
    y = 4 + 3 * X + np.random.randn(100, 1)

    # Split data
    split_idx = 80
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Train model using gradient descent
    model_gd = LinearRegression(learning_rate=0.1, n_iterations=1000)
    model_gd.fit(X_train, y_train, method='gradient_descent')

    print(f"\nGradient Descent Results:")
    print(f"Weights: {model_gd.weights[0]:.4f}")
    print(f"Bias: {model_gd.bias:.4f}")
    print(f"Final cost: {model_gd.cost_history[-1]:.6f}")

    # Train using normal equation
    model_ne = LinearRegression()
    model_ne.fit(X_train, y_train, method='normal_equation')

    print(f"\nNormal Equation Results:")
    print(f"Weights: {model_ne.weights[0]:.4f}")
    print(f"Bias: {model_ne.bias:.4f}")

    # Evaluate on test set
    metrics = model_gd.get_metrics(X_test, y_test.flatten())
    print(f"\nTest Set Metrics:")
    for metric, value in metrics.items():
        print(f"  {metric.upper()}: {value:.4f}")

    # Plot results
    model_gd.plot_fit(X_train, y_train.flatten())
    model_gd.plot_cost_history()


def example_multiple_regression():
    """Example: Multiple linear regression with polynomial features"""
    print("\n" + "=" * 60)
    print("Multiple Linear Regression with Polynomial Features")
    print("=" * 60)

    # Generate non-linear synthetic data
    np.random.seed(42)
    X = 6 * np.random.rand(100, 1) - 3
    y = 0.5 * X**2 + X + 2 + np.random.randn(100, 1)

    # Train linear model
    linear_model = LinearRegression(learning_rate=0.01, n_iterations=1000)
    linear_model.fit(X, y)

    # Train polynomial model
    poly_model = MultipleLinearRegression(
        learning_rate=0.01,
        n_iterations=1000,
        polynomial_degree=2,
        feature_scaling=True
    )
    poly_model.fit(X, y)

    # Compare R² scores
    linear_r2 = linear_model.score(X, y.flatten())
    poly_r2 = poly_model.score(X, y.flatten())

    print(f"\nModel Comparison:")
    print(f"Linear Model R²: {linear_r2:.4f}")
    print(f"Polynomial Model R²: {poly_r2:.4f}")

    # Visualize fits
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.scatter(X, y, alpha=0.5)
    X_line = np.linspace(-3, 3, 100).reshape(-1, 1)
    y_linear = linear_model.predict(X_line)
    plt.plot(X_line, y_linear, 'r-', label='Linear fit')
    plt.xlabel('X')
    plt.ylabel('y')
    plt.title(f'Linear Model (R²={linear_r2:.3f})')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.scatter(X, y, alpha=0.5)
    y_poly = poly_model.predict(X_line)
    plt.plot(X_line, y_poly, 'g-', label='Polynomial fit')
    plt.xlabel('X')
    plt.ylabel('y')
    plt.title(f'Polynomial Model (R²={poly_r2:.3f})')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def example_regularization():
    """Example: Effect of L2 regularization on overfitting"""
    print("\n" + "=" * 60)
    print("L2 Regularization Example")
    print("=" * 60)

    # Generate data with outliers
    np.random.seed(42)
    X = np.random.rand(20, 1) * 10
    y = 2 * X + 1 + np.random.randn(20, 1) * 2

    # Add outliers
    X = np.vstack([X, [[2], [8]]])
    y = np.vstack([y, [[15], [-5]]])

    # Train models with different regularization
    lambdas = [0, 0.1, 1, 10]
    models = []

    for lambda_val in lambdas:
        model = LinearRegression(
            learning_rate=0.01,
            n_iterations=1000,
            regularization=lambda_val
        )
        model.fit(X, y)
        models.append(model)

    # Plot results
    plt.figure(figsize=(12, 3))
    X_line = np.linspace(0, 10, 100).reshape(-1, 1)

    for i, (model, lambda_val) in enumerate(zip(models, lambdas)):
        plt.subplot(1, 4, i+1)
        plt.scatter(X, y, alpha=0.5)
        y_pred = model.predict(X_line)
        plt.plot(X_line, y_pred, 'r-')
        plt.xlabel('X')
        plt.ylabel('y')
        plt.title(f'λ = {lambda_val}')
        plt.grid(True)

    plt.suptitle('Effect of L2 Regularization')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Run examples
    example_simple_regression()
    example_multiple_regression()
    example_regularization()

    print("\n" + "=" * 60)
    print("Linear Regression Implementation Complete!")
    print("=" * 60)