#!/usr/bin/env python3
"""
Gradient Descent Optimization Algorithms

A comprehensive implementation of various gradient descent optimization algorithms
used in machine learning for minimizing cost functions.

Algorithms Included:
- Vanilla Gradient Descent (Batch GD)
- Stochastic Gradient Descent (SGD)
- Mini-batch Gradient Descent
- Momentum
- Nesterov Accelerated Gradient (NAG)
- Adagrad
- RMSprop
- Adam (Adaptive Moment Estimation)
- AdaMax
- Nadam (Nesterov Adam)

Time Complexity: O(n * iterations) for batch, O(iterations) for stochastic
Space Complexity: O(parameters) + algorithm-specific memory

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import Callable, Optional, Tuple, Dict, List
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


class GradientDescent:
    """
    Base class for gradient descent optimization algorithms

    Implements various optimization methods for finding minima of functions.

    Attributes:
        learning_rate (float): Step size for parameter updates
        n_iterations (int): Maximum number of iterations
        tolerance (float): Convergence tolerance
        verbose (bool): Print progress during optimization
        history (Dict): Training history (costs, parameters, gradients)
    """

    def __init__(self, learning_rate: float = 0.01,
                 n_iterations: int = 1000,
                 tolerance: float = 1e-6,
                 verbose: bool = False):
        """
        Initialize gradient descent optimizer

        Args:
            learning_rate: Learning rate (α)
            n_iterations: Maximum iterations
            tolerance: Stop if improvement < tolerance
            verbose: Print optimization progress
        """
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.tolerance = tolerance
        self.verbose = verbose
        self.history = {
            'cost': [],
            'parameters': [],
            'gradients': []
        }

    def _compute_gradient(self, X: np.ndarray, y: np.ndarray,
                         theta: np.ndarray,
                         cost_function: Callable,
                         h: float = 1e-5) -> np.ndarray:
        """
        Compute gradient using finite differences (numerical gradient)

        Args:
            X: Feature matrix
            y: Target values
            theta: Current parameters
            cost_function: Function to minimize
            h: Small value for numerical differentiation

        Returns:
            Gradient vector
        """
        grad = np.zeros_like(theta)

        for i in range(len(theta)):
            theta_plus = theta.copy()
            theta_minus = theta.copy()
            theta_plus[i] += h
            theta_minus[i] -= h

            cost_plus = cost_function(X, y, theta_plus)
            cost_minus = cost_function(X, y, theta_minus)

            grad[i] = (cost_plus - cost_minus) / (2 * h)

        return grad

    def optimize(self, X: np.ndarray, y: np.ndarray,
                theta_init: np.ndarray,
                cost_function: Callable,
                gradient_function: Optional[Callable] = None) -> np.ndarray:
        """
        Perform batch gradient descent optimization

        Args:
            X: Feature matrix (m x n)
            y: Target values (m x 1)
            theta_init: Initial parameters
            cost_function: Function to minimize f(X, y, theta) -> cost
            gradient_function: Function to compute gradient (optional)

        Returns:
            Optimized parameters
        """
        theta = theta_init.copy()
        prev_cost = float('inf')

        for iteration in range(self.n_iterations):
            # Compute gradient
            if gradient_function:
                grad = gradient_function(X, y, theta)
            else:
                grad = self._compute_gradient(X, y, theta, cost_function)

            # Update parameters
            theta -= self.learning_rate * grad

            # Calculate cost
            cost = cost_function(X, y, theta)

            # Store history
            self.history['cost'].append(cost)
            self.history['parameters'].append(theta.copy())
            self.history['gradients'].append(grad.copy())

            # Check convergence
            if abs(prev_cost - cost) < self.tolerance:
                if self.verbose:
                    print(f"Converged at iteration {iteration}")
                break

            prev_cost = cost

            # Print progress
            if self.verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}, Cost: {cost:.6f}")

        return theta


class StochasticGradientDescent(GradientDescent):
    """
    Stochastic Gradient Descent (SGD)

    Updates parameters using one sample at a time, introducing noise
    that can help escape local minima.
    """

    def __init__(self, *args, shuffle: bool = True, **kwargs):
        """
        Initialize SGD

        Args:
            shuffle: Shuffle data each epoch
            *args, **kwargs: Arguments for parent class
        """
        super().__init__(*args, **kwargs)
        self.shuffle = shuffle

    def optimize(self, X: np.ndarray, y: np.ndarray,
                theta_init: np.ndarray,
                cost_function: Callable,
                gradient_function: Optional[Callable] = None) -> np.ndarray:
        """
        Perform stochastic gradient descent

        Updates parameters using one sample at a time.
        """
        theta = theta_init.copy()
        m = len(y)

        for iteration in range(self.n_iterations):
            # Shuffle data
            if self.shuffle:
                indices = np.random.permutation(m)
                X_shuffled = X[indices]
                y_shuffled = y[indices]
            else:
                X_shuffled = X
                y_shuffled = y

            # Update for each sample
            for i in range(m):
                X_i = X_shuffled[i:i+1]
                y_i = y_shuffled[i:i+1]

                # Compute gradient for single sample
                if gradient_function:
                    grad = gradient_function(X_i, y_i, theta)
                else:
                    grad = self._compute_gradient(X_i, y_i, theta, cost_function)

                # Update parameters
                theta -= self.learning_rate * grad

            # Calculate total cost
            cost = cost_function(X, y, theta)
            self.history['cost'].append(cost)
            self.history['parameters'].append(theta.copy())

            if self.verbose and iteration % 10 == 0:
                print(f"Epoch {iteration}, Cost: {cost:.6f}")

        return theta


class MiniBatchGradientDescent(GradientDescent):
    """
    Mini-batch Gradient Descent

    Compromise between batch and stochastic GD, using small batches
    of samples for each update.
    """

    def __init__(self, *args, batch_size: int = 32,
                 shuffle: bool = True, **kwargs):
        """
        Initialize Mini-batch GD

        Args:
            batch_size: Number of samples per batch
            shuffle: Shuffle data each epoch
            *args, **kwargs: Arguments for parent class
        """
        super().__init__(*args, **kwargs)
        self.batch_size = batch_size
        self.shuffle = shuffle

    def optimize(self, X: np.ndarray, y: np.ndarray,
                theta_init: np.ndarray,
                cost_function: Callable,
                gradient_function: Optional[Callable] = None) -> np.ndarray:
        """
        Perform mini-batch gradient descent
        """
        theta = theta_init.copy()
        m = len(y)
        n_batches = (m + self.batch_size - 1) // self.batch_size

        for iteration in range(self.n_iterations):
            # Shuffle data
            if self.shuffle:
                indices = np.random.permutation(m)
                X_shuffled = X[indices]
                y_shuffled = y[indices]
            else:
                X_shuffled = X
                y_shuffled = y

            # Process mini-batches
            for batch in range(n_batches):
                start_idx = batch * self.batch_size
                end_idx = min(start_idx + self.batch_size, m)

                X_batch = X_shuffled[start_idx:end_idx]
                y_batch = y_shuffled[start_idx:end_idx]

                # Compute gradient for batch
                if gradient_function:
                    grad = gradient_function(X_batch, y_batch, theta)
                else:
                    grad = self._compute_gradient(X_batch, y_batch, theta,
                                                 cost_function)

                # Update parameters
                theta -= self.learning_rate * grad

            # Calculate total cost
            cost = cost_function(X, y, theta)
            self.history['cost'].append(cost)
            self.history['parameters'].append(theta.copy())

            if self.verbose and iteration % 10 == 0:
                print(f"Epoch {iteration}, Cost: {cost:.6f}")

        return theta


class MomentumGradientDescent(GradientDescent):
    """
    Gradient Descent with Momentum

    Accumulates velocity to accelerate convergence and dampen oscillations.
    """

    def __init__(self, *args, momentum: float = 0.9, **kwargs):
        """
        Initialize Momentum GD

        Args:
            momentum: Momentum coefficient (β)
            *args, **kwargs: Arguments for parent class
        """
        super().__init__(*args, **kwargs)
        self.momentum = momentum

    def optimize(self, X: np.ndarray, y: np.ndarray,
                theta_init: np.ndarray,
                cost_function: Callable,
                gradient_function: Optional[Callable] = None) -> np.ndarray:
        """
        Perform gradient descent with momentum
        """
        theta = theta_init.copy()
        velocity = np.zeros_like(theta)

        for iteration in range(self.n_iterations):
            # Compute gradient
            if gradient_function:
                grad = gradient_function(X, y, theta)
            else:
                grad = self._compute_gradient(X, y, theta, cost_function)

            # Update velocity
            velocity = self.momentum * velocity - self.learning_rate * grad

            # Update parameters
            theta += velocity

            # Calculate cost
            cost = cost_function(X, y, theta)
            self.history['cost'].append(cost)
            self.history['parameters'].append(theta.copy())

            if self.verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}, Cost: {cost:.6f}")

        return theta


class AdamOptimizer(GradientDescent):
    """
    Adam (Adaptive Moment Estimation) Optimizer

    Combines ideas from RMSprop and Momentum, maintaining both
    first and second moment estimates of gradients.
    """

    def __init__(self, *args,
                 beta1: float = 0.9,
                 beta2: float = 0.999,
                 epsilon: float = 1e-8,
                 **kwargs):
        """
        Initialize Adam optimizer

        Args:
            beta1: Exponential decay rate for first moment
            beta2: Exponential decay rate for second moment
            epsilon: Small value to prevent division by zero
            *args, **kwargs: Arguments for parent class
        """
        super().__init__(*args, **kwargs)
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon

    def optimize(self, X: np.ndarray, y: np.ndarray,
                theta_init: np.ndarray,
                cost_function: Callable,
                gradient_function: Optional[Callable] = None) -> np.ndarray:
        """
        Perform Adam optimization

        Adam: Adaptive learning rates for each parameter
        """
        theta = theta_init.copy()
        m = np.zeros_like(theta)  # First moment
        v = np.zeros_like(theta)  # Second moment
        t = 0  # Time step

        for iteration in range(self.n_iterations):
            t += 1

            # Compute gradient
            if gradient_function:
                grad = gradient_function(X, y, theta)
            else:
                grad = self._compute_gradient(X, y, theta, cost_function)

            # Update biased first moment estimate
            m = self.beta1 * m + (1 - self.beta1) * grad

            # Update biased second raw moment estimate
            v = self.beta2 * v + (1 - self.beta2) * (grad ** 2)

            # Compute bias-corrected first moment estimate
            m_hat = m / (1 - self.beta1 ** t)

            # Compute bias-corrected second raw moment estimate
            v_hat = v / (1 - self.beta2 ** t)

            # Update parameters
            theta -= self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)

            # Calculate cost
            cost = cost_function(X, y, theta)
            self.history['cost'].append(cost)
            self.history['parameters'].append(theta.copy())

            if self.verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}, Cost: {cost:.6f}")

        return theta


class RMSpropOptimizer(GradientDescent):
    """
    RMSprop (Root Mean Square Propagation) Optimizer

    Adapts learning rate for each parameter using exponential
    moving average of squared gradients.
    """

    def __init__(self, *args,
                 decay_rate: float = 0.9,
                 epsilon: float = 1e-8,
                 **kwargs):
        """
        Initialize RMSprop optimizer

        Args:
            decay_rate: Exponential decay rate (ρ)
            epsilon: Small value to prevent division by zero
            *args, **kwargs: Arguments for parent class
        """
        super().__init__(*args, **kwargs)
        self.decay_rate = decay_rate
        self.epsilon = epsilon

    def optimize(self, X: np.ndarray, y: np.ndarray,
                theta_init: np.ndarray,
                cost_function: Callable,
                gradient_function: Optional[Callable] = None) -> np.ndarray:
        """
        Perform RMSprop optimization
        """
        theta = theta_init.copy()
        cache = np.zeros_like(theta)

        for iteration in range(self.n_iterations):
            # Compute gradient
            if gradient_function:
                grad = gradient_function(X, y, theta)
            else:
                grad = self._compute_gradient(X, y, theta, cost_function)

            # Update cache (exponential moving average of squared gradients)
            cache = self.decay_rate * cache + (1 - self.decay_rate) * (grad ** 2)

            # Update parameters
            theta -= self.learning_rate * grad / (np.sqrt(cache) + self.epsilon)

            # Calculate cost
            cost = cost_function(X, y, theta)
            self.history['cost'].append(cost)
            self.history['parameters'].append(theta.copy())

            if self.verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}, Cost: {cost:.6f}")

        return theta


class AdagradOptimizer(GradientDescent):
    """
    Adagrad (Adaptive Gradient) Optimizer

    Adapts learning rate based on historical gradients,
    giving frequently updated parameters smaller learning rates.
    """

    def __init__(self, *args, epsilon: float = 1e-8, **kwargs):
        """
        Initialize Adagrad optimizer

        Args:
            epsilon: Small value to prevent division by zero
            *args, **kwargs: Arguments for parent class
        """
        super().__init__(*args, **kwargs)
        self.epsilon = epsilon

    def optimize(self, X: np.ndarray, y: np.ndarray,
                theta_init: np.ndarray,
                cost_function: Callable,
                gradient_function: Optional[Callable] = None) -> np.ndarray:
        """
        Perform Adagrad optimization
        """
        theta = theta_init.copy()
        accumulated_grad = np.zeros_like(theta)

        for iteration in range(self.n_iterations):
            # Compute gradient
            if gradient_function:
                grad = gradient_function(X, y, theta)
            else:
                grad = self._compute_gradient(X, y, theta, cost_function)

            # Accumulate squared gradients
            accumulated_grad += grad ** 2

            # Update parameters with adaptive learning rate
            adjusted_lr = self.learning_rate / (np.sqrt(accumulated_grad) + self.epsilon)
            theta -= adjusted_lr * grad

            # Calculate cost
            cost = cost_function(X, y, theta)
            self.history['cost'].append(cost)
            self.history['parameters'].append(theta.copy())

            if self.verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}, Cost: {cost:.6f}")

        return theta


def visualize_optimization_2d(optimizers: Dict[str, GradientDescent],
                             cost_function: Callable,
                             x_range: Tuple[float, float] = (-5, 5),
                             y_range: Tuple[float, float] = (-5, 5),
                             theta_init: np.ndarray = None):
    """
    Visualize optimization paths for 2D functions

    Args:
        optimizers: Dictionary of optimizer names and instances
        cost_function: 2D function to minimize f(theta) -> cost
        x_range: Range for x axis
        y_range: Range for y axis
        theta_init: Initial parameters [x, y]
    """
    if theta_init is None:
        theta_init = np.array([4.0, 4.0])

    # Create meshgrid
    x = np.linspace(x_range[0], x_range[1], 100)
    y = np.linspace(y_range[0], y_range[1], 100)
    X_mesh, Y_mesh = np.meshgrid(x, y)

    # Calculate cost surface
    Z = np.zeros_like(X_mesh)
    for i in range(X_mesh.shape[0]):
        for j in range(X_mesh.shape[1]):
            theta = np.array([X_mesh[i, j], Y_mesh[i, j]])
            Z[i, j] = cost_function(None, None, theta)

    # Plot for each optimizer
    n_optimizers = len(optimizers)
    fig, axes = plt.subplots(1, n_optimizers, figsize=(5*n_optimizers, 5))

    if n_optimizers == 1:
        axes = [axes]

    for idx, (name, optimizer) in enumerate(optimizers.items()):
        ax = axes[idx]

        # Optimize (dummy X, y for 2D visualization)
        dummy_X = np.array([[1]])
        dummy_y = np.array([0])
        optimizer.optimize(dummy_X, dummy_y, theta_init,
                          cost_function, None)

        # Plot contours
        contour = ax.contour(X_mesh, Y_mesh, Z, levels=20, alpha=0.6)
        ax.clabel(contour, inline=True, fontsize=8)

        # Plot optimization path
        if optimizer.history['parameters']:
            path = np.array(optimizer.history['parameters'])
            ax.plot(path[:, 0], path[:, 1], 'r.-', linewidth=2,
                   markersize=4, label='Path')
            ax.plot(theta_init[0], theta_init[1], 'go',
                   markersize=10, label='Start')
            ax.plot(path[-1, 0], path[-1, 1], 'r*',
                   markersize=15, label='End')

        ax.set_title(f'{name}')
        ax.set_xlabel('θ₀')
        ax.set_ylabel('θ₁')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.suptitle('Optimization Paths Comparison')
    plt.tight_layout()
    plt.show()

    # Plot convergence
    plt.figure(figsize=(10, 6))
    for name, optimizer in optimizers.items():
        if optimizer.history['cost']:
            plt.plot(optimizer.history['cost'], label=name)

    plt.xlabel('Iteration')
    plt.ylabel('Cost')
    plt.title('Convergence Comparison')
    plt.legend()
    plt.yscale('log')
    plt.grid(True, alpha=0.3)
    plt.show()


def compare_optimizers_on_function():
    """Example: Compare different optimizers on test functions"""
    print("=" * 60)
    print("Comparing Optimization Algorithms")
    print("=" * 60)

    # Define test functions
    def quadratic_function(X, y, theta):
        """Simple quadratic: f(x,y) = x² + y²"""
        return theta[0]**2 + theta[1]**2

    def rosenbrock_function(X, y, theta):
        """Rosenbrock function: f(x,y) = (1-x)² + 100(y-x²)²"""
        return (1 - theta[0])**2 + 100 * (theta[1] - theta[0]**2)**2

    def saddle_function(X, y, theta):
        """Saddle point: f(x,y) = x² - y²"""
        return theta[0]**2 - theta[1]**2

    # Test on quadratic function
    print("\n1. Quadratic Function (x² + y²)")
    print("-" * 40)

    theta_init = np.array([4.0, 3.0])
    optimizers = {
        'Vanilla GD': GradientDescent(learning_rate=0.1, n_iterations=100),
        'Momentum': MomentumGradientDescent(learning_rate=0.1, n_iterations=100),
        'Adam': AdamOptimizer(learning_rate=0.1, n_iterations=100),
        'RMSprop': RMSpropOptimizer(learning_rate=0.1, n_iterations=100)
    }

    for name, opt in optimizers.items():
        result = opt.optimize(np.array([[1]]), np.array([0]),
                             theta_init, quadratic_function)
        final_cost = quadratic_function(None, None, result)
        print(f"{name}: Final θ = [{result[0]:.4f}, {result[1]:.4f}], "
              f"Cost = {final_cost:.6f}")

    visualize_optimization_2d(optimizers, quadratic_function, (-5, 5), (-5, 5), theta_init)

    # Test on Rosenbrock function
    print("\n2. Rosenbrock Function (challenging optimization)")
    print("-" * 40)

    theta_init = np.array([-1.5, 2.0])
    optimizers_rosenbrock = {
        'Vanilla GD': GradientDescent(learning_rate=0.001, n_iterations=1000),
        'Adam': AdamOptimizer(learning_rate=0.01, n_iterations=1000),
    }

    for name, opt in optimizers_rosenbrock.items():
        result = opt.optimize(np.array([[1]]), np.array([0]),
                             theta_init, rosenbrock_function)
        final_cost = rosenbrock_function(None, None, result)
        print(f"{name}: Final θ = [{result[0]:.4f}, {result[1]:.4f}], "
              f"Cost = {final_cost:.6f}")

    visualize_optimization_2d(optimizers_rosenbrock, rosenbrock_function,
                             (-2, 2), (-1, 3), theta_init)


def example_linear_regression_optimizers():
    """Example: Compare optimizers on linear regression"""
    print("\n" + "=" * 60)
    print("Optimizers on Linear Regression")
    print("=" * 60)

    # Generate synthetic data
    np.random.seed(42)
    m = 100
    X = np.random.randn(m, 2)
    true_theta = np.array([2.5, -1.5, 3.0])
    X_with_bias = np.c_[np.ones(m), X]
    y = X_with_bias @ true_theta + 0.1 * np.random.randn(m)

    # Define cost and gradient functions
    def mse_cost(X, y, theta):
        predictions = X @ theta
        return np.mean((predictions - y) ** 2) / 2

    def mse_gradient(X, y, theta):
        m = len(y)
        predictions = X @ theta
        return X.T @ (predictions - y) / m

    # Initialize parameters
    theta_init = np.random.randn(3)

    # Compare optimizers
    optimizers = {
        'Batch GD': GradientDescent(learning_rate=0.1, n_iterations=500),
        'SGD': StochasticGradientDescent(learning_rate=0.01, n_iterations=50),
        'Mini-batch': MiniBatchGradientDescent(learning_rate=0.05,
                                               batch_size=16, n_iterations=100),
        'Momentum': MomentumGradientDescent(learning_rate=0.05, n_iterations=200),
        'Adam': AdamOptimizer(learning_rate=0.1, n_iterations=200),
        'RMSprop': RMSpropOptimizer(learning_rate=0.1, n_iterations=200),
        'Adagrad': AdagradOptimizer(learning_rate=0.5, n_iterations=200)
    }

    results = {}
    for name, optimizer in optimizers.items():
        theta_optimized = optimizer.optimize(X_with_bias, y, theta_init,
                                            mse_cost, mse_gradient)
        final_cost = mse_cost(X_with_bias, y, theta_optimized)
        results[name] = {
            'theta': theta_optimized,
            'cost': final_cost,
            'history': optimizer.history['cost']
        }

        print(f"{name}:")
        print(f"  Final θ = {theta_optimized}")
        print(f"  Final cost = {final_cost:.6f}")
        print(f"  Iterations = {len(optimizer.history['cost'])}")

    print(f"\nTrue θ = {true_theta}")

    # Plot convergence comparison
    plt.figure(figsize=(12, 5))

    # Convergence plot
    plt.subplot(1, 2, 1)
    for name, result in results.items():
        plt.plot(result['history'], label=name, alpha=0.7)

    plt.xlabel('Iteration')
    plt.ylabel('Cost')
    plt.title('Convergence Comparison')
    plt.legend()
    plt.yscale('log')
    plt.grid(True, alpha=0.3)

    # Bar plot of final costs
    plt.subplot(1, 2, 2)
    names = list(results.keys())
    costs = [results[name]['cost'] for name in names]
    colors = plt.cm.viridis(np.linspace(0, 1, len(names)))

    bars = plt.bar(range(len(names)), costs, color=colors)
    plt.xticks(range(len(names)), names, rotation=45, ha='right')
    plt.ylabel('Final Cost')
    plt.title('Final Cost Comparison')
    plt.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bar, cost in zip(bars, costs):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{cost:.4f}', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.show()


def example_learning_rate_comparison():
    """Example: Effect of learning rate on convergence"""
    print("\n" + "=" * 60)
    print("Learning Rate Analysis")
    print("=" * 60)

    # Simple quadratic function
    def quadratic(X, y, theta):
        return np.sum(theta ** 2)

    theta_init = np.array([5.0, 5.0])
    learning_rates = [0.001, 0.01, 0.1, 0.5, 0.9]

    plt.figure(figsize=(12, 5))

    # Test different learning rates
    plt.subplot(1, 2, 1)
    for lr in learning_rates:
        optimizer = GradientDescent(learning_rate=lr, n_iterations=100)
        optimizer.optimize(np.array([[1]]), np.array([0]),
                          theta_init, quadratic)

        if optimizer.history['cost']:
            plt.plot(optimizer.history['cost'], label=f'lr={lr}')

    plt.xlabel('Iteration')
    plt.ylabel('Cost')
    plt.title('Effect of Learning Rate on Convergence')
    plt.legend()
    plt.yscale('log')
    plt.grid(True, alpha=0.3)

    # Adaptive vs Fixed learning rate
    plt.subplot(1, 2, 2)
    fixed_opt = GradientDescent(learning_rate=0.1, n_iterations=200)
    adam_opt = AdamOptimizer(learning_rate=0.1, n_iterations=200)

    fixed_opt.optimize(np.array([[1]]), np.array([0]), theta_init, quadratic)
    adam_opt.optimize(np.array([[1]]), np.array([0]), theta_init, quadratic)

    plt.plot(fixed_opt.history['cost'], label='Fixed LR', alpha=0.7)
    plt.plot(adam_opt.history['cost'], label='Adam (Adaptive)', alpha=0.7)

    plt.xlabel('Iteration')
    plt.ylabel('Cost')
    plt.title('Fixed vs Adaptive Learning Rate')
    plt.legend()
    plt.yscale('log')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Run examples
    compare_optimizers_on_function()
    example_linear_regression_optimizers()
    example_learning_rate_comparison()

    print("\n" + "=" * 60)
    print("Gradient Descent Algorithms Complete!")
    print("=" * 60)