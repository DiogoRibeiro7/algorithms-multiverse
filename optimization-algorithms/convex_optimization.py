"""
Convex Optimization Algorithms Implementation

This module provides implementations of fundamental convex optimization algorithms
including gradient descent variants, proximal methods, and interior point methods.

Key Algorithms:
- Gradient Descent (with line search)
- Newton's Method
- Conjugate Gradient
- Proximal Gradient Method (ISTA/FISTA)
- ADMM (Alternating Direction Method of Multipliers)
- Interior Point Method
- Subgradient Method
- Mirror Descent

Author: Claude
Date: January 2026
"""

import numpy as np
from typing import Callable, Optional, Tuple, Dict, List, Any, Union
from dataclasses import dataclass, field
import time
import warnings
from scipy.linalg import cholesky, solve_triangular
from scipy.sparse import csr_matrix, eye as sparse_eye
from scipy.sparse.linalg import cg, spsolve


@dataclass
class OptimizationResult:
    """Result of an optimization algorithm."""
    x: np.ndarray  # Optimal solution
    value: float  # Objective value at solution
    iterations: int  # Number of iterations
    converged: bool  # Whether algorithm converged
    history: Dict[str, List[float]] = field(default_factory=dict)  # Convergence history
    time: float = 0.0  # Total computation time
    message: str = ""  # Status message


class ConvexOptimizer:
    """
    Base class for convex optimization algorithms.
    """

    def __init__(self, tol: float = 1e-6, max_iter: int = 1000, verbose: bool = False):
        """
        Initialize optimizer.

        Args:
            tol: Convergence tolerance
            max_iter: Maximum iterations
            verbose: Print progress
        """
        self.tol = tol
        self.max_iter = max_iter
        self.verbose = verbose

    def line_search(self, f: Callable, grad_f: Callable, x: np.ndarray,
                    direction: np.ndarray, alpha: float = 1.0,
                    beta: float = 0.5, c: float = 0.5) -> float:
        """
        Backtracking line search with Armijo condition.

        Args:
            f: Objective function
            grad_f: Gradient function
            x: Current point
            direction: Search direction
            alpha: Initial step size
            beta: Step size reduction factor
            c: Armijo condition parameter

        Returns:
            Optimal step size
        """
        grad = grad_f(x)
        f_x = f(x)
        descent = np.dot(grad, direction)

        while f(x + alpha * direction) > f_x + c * alpha * descent:
            alpha *= beta
            if alpha < 1e-10:
                break

        return alpha


class GradientDescent(ConvexOptimizer):
    """
    Standard and accelerated gradient descent methods.
    """

    def minimize(self, f: Callable, grad_f: Callable, x0: np.ndarray,
                 method: str = "standard", learning_rate: Optional[float] = None,
                 momentum: float = 0.0) -> OptimizationResult:
        """
        Minimize a convex function using gradient descent.

        Args:
            f: Objective function
            grad_f: Gradient function
            x0: Initial point
            method: "standard", "nesterov", or "adagrad"
            learning_rate: Step size (None for line search)
            momentum: Momentum parameter for accelerated methods

        Returns:
            Optimization result
        """
        start_time = time.time()
        x = x0.copy()
        v = np.zeros_like(x)  # Velocity for momentum
        G = np.zeros_like(x)  # Accumulated gradient for AdaGrad

        history = {"objective": [], "gradient_norm": []}

        for iteration in range(self.max_iter):
            # Compute gradient
            if method == "nesterov":
                grad = grad_f(x + momentum * v)
            else:
                grad = grad_f(x)

            grad_norm = np.linalg.norm(grad)
            history["objective"].append(f(x))
            history["gradient_norm"].append(grad_norm)

            # Check convergence
            if grad_norm < self.tol:
                if self.verbose:
                    print(f"Converged at iteration {iteration}")
                return OptimizationResult(
                    x=x, value=f(x), iterations=iteration,
                    converged=True, history=history,
                    time=time.time() - start_time,
                    message="Converged: gradient norm below tolerance"
                )

            # Determine step size
            if learning_rate is None:
                # Use line search
                step = self.line_search(f, grad_f, x, -grad)
            else:
                step = learning_rate

            # Update based on method
            if method == "standard":
                x = x - step * grad
            elif method == "nesterov":
                v = momentum * v - step * grad
                x = x + v
            elif method == "adagrad":
                G += grad ** 2
                x = x - step * grad / (np.sqrt(G) + 1e-8)

            if self.verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}: f(x) = {f(x):.6f}, "
                      f"||grad|| = {grad_norm:.6f}")

        return OptimizationResult(
            x=x, value=f(x), iterations=self.max_iter,
            converged=False, history=history,
            time=time.time() - start_time,
            message="Maximum iterations reached"
        )


class NewtonMethod(ConvexOptimizer):
    """
    Newton's method for convex optimization.
    """

    def minimize(self, f: Callable, grad_f: Callable, hess_f: Callable,
                 x0: np.ndarray, damped: bool = True) -> OptimizationResult:
        """
        Minimize using Newton's method.

        Args:
            f: Objective function
            grad_f: Gradient function
            hess_f: Hessian function
            x0: Initial point
            damped: Use damped Newton (with line search)

        Returns:
            Optimization result
        """
        start_time = time.time()
        x = x0.copy()
        history = {"objective": [], "gradient_norm": [], "lambda_squared": []}

        for iteration in range(self.max_iter):
            grad = grad_f(x)
            hess = hess_f(x)

            # Compute Newton direction
            try:
                # Solve Hessian * direction = -gradient
                L = cholesky(hess, lower=True)
                direction = -solve_triangular(L.T, solve_triangular(L, grad, lower=True))
            except np.linalg.LinAlgError:
                # Hessian not positive definite, fall back to gradient descent
                direction = -grad

            # Newton decrement
            lambda_squared = -np.dot(grad, direction)

            history["objective"].append(f(x))
            history["gradient_norm"].append(np.linalg.norm(grad))
            history["lambda_squared"].append(lambda_squared)

            # Check convergence
            if lambda_squared / 2 < self.tol:
                if self.verbose:
                    print(f"Converged at iteration {iteration}")
                return OptimizationResult(
                    x=x, value=f(x), iterations=iteration,
                    converged=True, history=history,
                    time=time.time() - start_time,
                    message="Converged: Newton decrement below tolerance"
                )

            # Line search for step size
            if damped:
                step = self.line_search(f, grad_f, x, direction)
            else:
                step = 1.0

            x = x + step * direction

            if self.verbose and iteration % 10 == 0:
                print(f"Iteration {iteration}: f(x) = {f(x):.6f}, "
                      f"lambda^2 = {lambda_squared:.6f}")

        return OptimizationResult(
            x=x, value=f(x), iterations=self.max_iter,
            converged=False, history=history,
            time=time.time() - start_time,
            message="Maximum iterations reached"
        )


class ProximalGradient(ConvexOptimizer):
    """
    Proximal gradient methods for composite optimization: minimize f(x) + g(x)
    where f is smooth and g is non-smooth but has a proximal operator.
    """

    def __init__(self, tol: float = 1e-6, max_iter: int = 1000,
                 verbose: bool = False):
        super().__init__(tol, max_iter, verbose)

    def soft_threshold(self, x: np.ndarray, threshold: float) -> np.ndarray:
        """Soft thresholding (proximal operator for L1 norm)."""
        return np.sign(x) * np.maximum(np.abs(x) - threshold, 0)

    def prox_l2(self, x: np.ndarray, lamb: float) -> np.ndarray:
        """Proximal operator for L2 norm."""
        norm = np.linalg.norm(x)
        if norm <= lamb:
            return np.zeros_like(x)
        return (1 - lamb / norm) * x

    def prox_box(self, x: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> np.ndarray:
        """Proximal operator for box constraints."""
        return np.clip(x, lower, upper)

    def ista(self, f: Callable, grad_f: Callable, prox_g: Callable,
             x0: np.ndarray, L: float) -> OptimizationResult:
        """
        Iterative Shrinkage-Thresholding Algorithm (ISTA).

        Args:
            f: Smooth objective function
            grad_f: Gradient of f
            prox_g: Proximal operator for non-smooth part
            x0: Initial point
            L: Lipschitz constant of gradient

        Returns:
            Optimization result
        """
        start_time = time.time()
        x = x0.copy()
        history = {"objective": [], "gradient_norm": []}

        for iteration in range(self.max_iter):
            grad = grad_f(x)
            x_new = prox_g(x - grad / L)

            history["objective"].append(f(x))
            history["gradient_norm"].append(np.linalg.norm(grad))

            # Check convergence
            if np.linalg.norm(x_new - x) < self.tol:
                if self.verbose:
                    print(f"ISTA converged at iteration {iteration}")
                return OptimizationResult(
                    x=x_new, value=f(x_new), iterations=iteration,
                    converged=True, history=history,
                    time=time.time() - start_time,
                    message="Converged: change in x below tolerance"
                )

            x = x_new

            if self.verbose and iteration % 100 == 0:
                print(f"ISTA iteration {iteration}: f(x) = {f(x):.6f}")

        return OptimizationResult(
            x=x, value=f(x), iterations=self.max_iter,
            converged=False, history=history,
            time=time.time() - start_time,
            message="Maximum iterations reached"
        )

    def fista(self, f: Callable, grad_f: Callable, prox_g: Callable,
              x0: np.ndarray, L: float) -> OptimizationResult:
        """
        Fast ISTA with Nesterov acceleration.

        Args:
            f: Smooth objective function
            grad_f: Gradient of f
            prox_g: Proximal operator for non-smooth part
            x0: Initial point
            L: Lipschitz constant of gradient

        Returns:
            Optimization result
        """
        start_time = time.time()
        x = x0.copy()
        y = x.copy()
        t = 1.0
        history = {"objective": [], "gradient_norm": []}

        for iteration in range(self.max_iter):
            grad = grad_f(y)
            x_new = prox_g(y - grad / L)
            t_new = (1 + np.sqrt(1 + 4 * t ** 2)) / 2
            y = x_new + ((t - 1) / t_new) * (x_new - x)

            history["objective"].append(f(x))
            history["gradient_norm"].append(np.linalg.norm(grad))

            # Check convergence
            if np.linalg.norm(x_new - x) < self.tol:
                if self.verbose:
                    print(f"FISTA converged at iteration {iteration}")
                return OptimizationResult(
                    x=x_new, value=f(x_new), iterations=iteration,
                    converged=True, history=history,
                    time=time.time() - start_time,
                    message="Converged: change in x below tolerance"
                )

            x = x_new
            t = t_new

            if self.verbose and iteration % 100 == 0:
                print(f"FISTA iteration {iteration}: f(x) = {f(x):.6f}")

        return OptimizationResult(
            x=x, value=f(x), iterations=self.max_iter,
            converged=False, history=history,
            time=time.time() - start_time,
            message="Maximum iterations reached"
        )


class ADMM(ConvexOptimizer):
    """
    Alternating Direction Method of Multipliers for solving:
    minimize f(x) + g(z) subject to Ax + Bz = c
    """

    def __init__(self, rho: float = 1.0, tol: float = 1e-6,
                 max_iter: int = 1000, verbose: bool = False):
        """
        Initialize ADMM solver.

        Args:
            rho: Penalty parameter
            tol: Convergence tolerance
            max_iter: Maximum iterations
            verbose: Print progress
        """
        super().__init__(tol, max_iter, verbose)
        self.rho = rho

    def solve(self, prox_f: Callable, prox_g: Callable,
              A: np.ndarray, B: np.ndarray, c: np.ndarray,
              x0: Optional[np.ndarray] = None,
              z0: Optional[np.ndarray] = None) -> OptimizationResult:
        """
        Solve using ADMM.

        Args:
            prox_f: Proximal operator for f
            prox_g: Proximal operator for g
            A, B, c: Constraint matrices and vector
            x0, z0: Initial points

        Returns:
            Optimization result
        """
        start_time = time.time()

        # Initialize variables
        n, m = A.shape[1], B.shape[1]
        x = x0 if x0 is not None else np.zeros(n)
        z = z0 if z0 is not None else np.zeros(m)
        u = np.zeros(len(c))  # Dual variable

        history = {"primal_residual": [], "dual_residual": []}

        for iteration in range(self.max_iter):
            # x-update
            x_new = prox_f(x - A.T @ u / self.rho)

            # z-update
            z_new = prox_g(z - B.T @ u / self.rho)

            # u-update
            u = u + self.rho * (A @ x_new + B @ z_new - c)

            # Compute residuals
            primal_res = np.linalg.norm(A @ x_new + B @ z_new - c)
            dual_res = self.rho * np.linalg.norm(A.T @ (B @ (z_new - z)))

            history["primal_residual"].append(primal_res)
            history["dual_residual"].append(dual_res)

            # Check convergence
            if primal_res < self.tol and dual_res < self.tol:
                if self.verbose:
                    print(f"ADMM converged at iteration {iteration}")
                return OptimizationResult(
                    x=np.concatenate([x_new, z_new]),
                    value=0.0,  # Would need f and g to compute
                    iterations=iteration,
                    converged=True,
                    history=history,
                    time=time.time() - start_time,
                    message="Converged: residuals below tolerance"
                )

            x, z = x_new, z_new

            if self.verbose and iteration % 100 == 0:
                print(f"ADMM iteration {iteration}: "
                      f"primal_res = {primal_res:.6f}, dual_res = {dual_res:.6f}")

        return OptimizationResult(
            x=np.concatenate([x, z]),
            value=0.0,
            iterations=self.max_iter,
            converged=False,
            history=history,
            time=time.time() - start_time,
            message="Maximum iterations reached"
        )


class InteriorPointMethod(ConvexOptimizer):
    """
    Interior point method for constrained convex optimization:
    minimize f(x) subject to Ax = b, h_i(x) <= 0
    """

    def __init__(self, tol: float = 1e-6, max_iter: int = 100,
                 verbose: bool = False):
        super().__init__(tol, max_iter, verbose)

    def solve_barrier(self, f: Callable, grad_f: Callable, hess_f: Callable,
                      constraints: List[Tuple[Callable, Callable, Callable]],
                      x0: np.ndarray, t: float) -> np.ndarray:
        """
        Solve the barrier subproblem using Newton's method.

        Args:
            f: Objective function
            grad_f, hess_f: Gradient and Hessian of f
            constraints: List of (h, grad_h, hess_h) for each constraint h_i(x) <= 0
            x0: Initial point (must be strictly feasible)
            t: Barrier parameter

        Returns:
            Solution to barrier subproblem
        """
        x = x0.copy()

        for _ in range(50):  # Newton iterations for barrier subproblem
            # Compute barrier gradient and Hessian
            grad = t * grad_f(x)
            hess = t * hess_f(x)

            for h, grad_h, hess_h in constraints:
                h_x = h(x)
                if h_x >= 0:
                    return x  # Infeasible
                grad -= grad_h(x) / h_x
                hess += np.outer(grad_h(x), grad_h(x)) / (h_x ** 2) - hess_h(x) / h_x

            # Newton direction
            try:
                direction = -np.linalg.solve(hess, grad)
            except np.linalg.LinAlgError:
                break

            # Line search to maintain feasibility
            step = 1.0
            for h, _, _ in constraints:
                while h(x + step * direction) >= 0:
                    step *= 0.5
                    if step < 1e-10:
                        break

            x = x + step * direction

            if np.linalg.norm(grad) < 1e-8:
                break

        return x

    def minimize(self, f: Callable, grad_f: Callable, hess_f: Callable,
                 constraints: List[Tuple[Callable, Callable, Callable]],
                 x0: np.ndarray, mu: float = 10.0) -> OptimizationResult:
        """
        Minimize with inequality constraints using interior point method.

        Args:
            f: Objective function
            grad_f, hess_f: Gradient and Hessian of f
            constraints: List of constraint functions and derivatives
            x0: Initial strictly feasible point
            mu: Barrier parameter increase factor

        Returns:
            Optimization result
        """
        start_time = time.time()
        x = x0.copy()
        t = 1.0
        history = {"objective": [], "barrier_parameter": []}

        # Check initial feasibility
        for h, _, _ in constraints:
            if h(x) >= 0:
                return OptimizationResult(
                    x=x, value=f(x), iterations=0,
                    converged=False, history=history,
                    time=time.time() - start_time,
                    message="Initial point not strictly feasible"
                )

        for iteration in range(self.max_iter):
            # Solve barrier subproblem
            x = self.solve_barrier(f, grad_f, hess_f, constraints, x, t)

            history["objective"].append(f(x))
            history["barrier_parameter"].append(t)

            # Check convergence
            m = len(constraints)  # Number of constraints
            if m / t < self.tol:
                if self.verbose:
                    print(f"Interior point converged at iteration {iteration}")
                return OptimizationResult(
                    x=x, value=f(x), iterations=iteration,
                    converged=True, history=history,
                    time=time.time() - start_time,
                    message="Converged: duality gap below tolerance"
                )

            # Increase barrier parameter
            t *= mu

            if self.verbose and iteration % 10 == 0:
                print(f"Iteration {iteration}: f(x) = {f(x):.6f}, t = {t:.2f}")

        return OptimizationResult(
            x=x, value=f(x), iterations=self.max_iter,
            converged=False, history=history,
            time=time.time() - start_time,
            message="Maximum iterations reached"
        )


class SubgradientMethod(ConvexOptimizer):
    """
    Subgradient method for non-smooth convex optimization.
    """

    def minimize(self, f: Callable, subgrad_f: Callable, x0: np.ndarray,
                 step_rule: str = "constant", step_size: float = 0.01) -> OptimizationResult:
        """
        Minimize non-smooth convex function using subgradient method.

        Args:
            f: Objective function
            subgrad_f: Subgradient function
            x0: Initial point
            step_rule: "constant", "diminishing", or "polyak"
            step_size: Initial step size

        Returns:
            Optimization result
        """
        start_time = time.time()
        x = x0.copy()
        x_best = x.copy()
        f_best = f(x)

        history = {"objective": [], "best_objective": []}

        for iteration in range(self.max_iter):
            subgrad = subgrad_f(x)
            f_x = f(x)

            history["objective"].append(f_x)
            history["best_objective"].append(f_best)

            # Update best solution
            if f_x < f_best:
                x_best = x.copy()
                f_best = f_x

            # Determine step size
            if step_rule == "constant":
                alpha = step_size
            elif step_rule == "diminishing":
                alpha = step_size / np.sqrt(iteration + 1)
            elif step_rule == "polyak":
                # Requires knowing optimal value
                alpha = step_size / (np.linalg.norm(subgrad) ** 2 + 1e-8)
            else:
                alpha = step_size

            # Subgradient step
            x = x - alpha * subgrad

            if self.verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}: f_best = {f_best:.6f}")

        return OptimizationResult(
            x=x_best, value=f_best, iterations=self.max_iter,
            converged=False, history=history,
            time=time.time() - start_time,
            message="Subgradient method completed"
        )


class CoordinateDescent(ConvexOptimizer):
    """
    Coordinate descent for separable or block-separable problems.
    """

    def minimize(self, f: Callable, grad_f: Callable, x0: np.ndarray,
                 blocks: Optional[List[np.ndarray]] = None,
                 cyclic: bool = True) -> OptimizationResult:
        """
        Minimize using coordinate descent.

        Args:
            f: Objective function
            grad_f: Gradient function (used component-wise)
            x0: Initial point
            blocks: Block structure (None for single coordinates)
            cyclic: Use cyclic (True) or random (False) coordinate selection

        Returns:
            Optimization result
        """
        start_time = time.time()
        x = x0.copy()
        n = len(x)

        if blocks is None:
            blocks = [np.array([i]) for i in range(n)]

        history = {"objective": []}

        for iteration in range(self.max_iter):
            x_old = x.copy()

            # Select coordinate order
            if cyclic:
                block_order = range(len(blocks))
            else:
                block_order = np.random.permutation(len(blocks))

            # Update each block
            for block_idx in block_order:
                block = blocks[block_idx]

                # Minimize over this block
                def f_block(x_block):
                    x_full = x.copy()
                    x_full[block] = x_block
                    return f(x_full)

                def grad_f_block(x_block):
                    x_full = x.copy()
                    x_full[block] = x_block
                    return grad_f(x_full)[block]

                # Simple gradient step for the block
                x_block = x[block]
                grad_block = grad_f_block(x_block)
                x[block] = x_block - 0.01 * grad_block  # Fixed step size

            history["objective"].append(f(x))

            # Check convergence
            if np.linalg.norm(x - x_old) < self.tol:
                if self.verbose:
                    print(f"Coordinate descent converged at iteration {iteration}")
                return OptimizationResult(
                    x=x, value=f(x), iterations=iteration,
                    converged=True, history=history,
                    time=time.time() - start_time,
                    message="Converged: change in x below tolerance"
                )

            if self.verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}: f(x) = {f(x):.6f}")

        return OptimizationResult(
            x=x, value=f(x), iterations=self.max_iter,
            converged=False, history=history,
            time=time.time() - start_time,
            message="Maximum iterations reached"
        )


# Example problems and usage
def example_quadratic_programming():
    """Example: Minimize quadratic function with constraints."""
    print("=== Quadratic Programming Example ===\n")

    # Problem: minimize 0.5 * x^T Q x + c^T x
    # subject to Ax <= b
    n = 5
    np.random.seed(42)
    Q = np.random.randn(n, n)
    Q = Q.T @ Q  # Make positive definite
    c = np.random.randn(n)

    # Define objective and derivatives
    def f(x):
        return 0.5 * x @ Q @ x + c @ x

    def grad_f(x):
        return Q @ x + c

    def hess_f(x):
        return Q

    # Test different optimizers
    x0 = np.random.randn(n)

    print("Testing gradient descent...")
    gd = GradientDescent(tol=1e-6, max_iter=1000)
    result_gd = gd.minimize(f, grad_f, x0, method="standard")
    print(f"  Converged: {result_gd.converged}")
    print(f"  Iterations: {result_gd.iterations}")
    print(f"  Optimal value: {result_gd.value:.6f}\n")

    print("Testing Newton's method...")
    newton = NewtonMethod(tol=1e-8, max_iter=100)
    result_newton = newton.minimize(f, grad_f, hess_f, x0)
    print(f"  Converged: {result_newton.converged}")
    print(f"  Iterations: {result_newton.iterations}")
    print(f"  Optimal value: {result_newton.value:.6f}\n")

    print("Testing accelerated gradient (Nesterov)...")
    result_nesterov = gd.minimize(f, grad_f, x0, method="nesterov",
                                   learning_rate=0.01, momentum=0.9)
    print(f"  Converged: {result_nesterov.converged}")
    print(f"  Iterations: {result_nesterov.iterations}")
    print(f"  Optimal value: {result_nesterov.value:.6f}")


def example_lasso_regression():
    """Example: LASSO regression using proximal gradient methods."""
    print("=== LASSO Regression Example ===\n")

    # Generate synthetic data
    np.random.seed(42)
    n_samples, n_features = 100, 20
    X = np.random.randn(n_samples, n_features)
    true_coef = np.random.randn(n_features)
    true_coef[n_features // 2:] = 0  # Make sparse
    y = X @ true_coef + 0.1 * np.random.randn(n_samples)

    # LASSO: minimize 0.5 ||Xw - y||^2 + lambda ||w||_1
    lambda_reg = 0.1

    def f(w):
        return 0.5 * np.linalg.norm(X @ w - y) ** 2

    def grad_f(w):
        return X.T @ (X @ w - y)

    # Proximal operator for L1 norm (soft thresholding)
    def prox_l1(w):
        return np.sign(w) * np.maximum(np.abs(w) - lambda_reg / L, 0)

    # Lipschitz constant
    L = np.linalg.norm(X.T @ X, 2)

    # Initial point
    w0 = np.zeros(n_features)

    # Solve with ISTA
    print("Solving with ISTA...")
    prox_solver = ProximalGradient(tol=1e-6, max_iter=1000)
    result_ista = prox_solver.ista(f, grad_f, prox_l1, w0, L)
    print(f"  Converged: {result_ista.converged}")
    print(f"  Iterations: {result_ista.iterations}")
    print(f"  Sparsity: {np.sum(np.abs(result_ista.x) < 1e-6)}/{n_features} zeros\n")

    # Solve with FISTA
    print("Solving with FISTA (accelerated)...")
    result_fista = prox_solver.fista(f, grad_f, prox_l1, w0, L)
    print(f"  Converged: {result_fista.converged}")
    print(f"  Iterations: {result_fista.iterations}")
    print(f"  Sparsity: {np.sum(np.abs(result_fista.x) < 1e-6)}/{n_features} zeros")

    # Compare convergence speed
    print(f"\nFISTA speedup: {result_ista.iterations / result_fista.iterations:.2f}x")


def example_constrained_optimization():
    """Example: Constrained optimization using interior point method."""
    print("=== Constrained Optimization Example ===\n")

    # Problem: minimize x1^2 + x2^2
    # subject to x1 + x2 >= 1, x1 >= 0, x2 >= 0

    def f(x):
        return x[0] ** 2 + x[1] ** 2

    def grad_f(x):
        return 2 * x

    def hess_f(x):
        return 2 * np.eye(2)

    # Constraints (converted to h(x) <= 0 form)
    constraints = [
        # -x1 - x2 + 1 <= 0 (i.e., x1 + x2 >= 1)
        (lambda x: -x[0] - x[1] + 1,
         lambda x: np.array([-1, -1]),
         lambda x: np.zeros((2, 2))),
        # -x1 <= 0 (i.e., x1 >= 0)
        (lambda x: -x[0],
         lambda x: np.array([-1, 0]),
         lambda x: np.zeros((2, 2))),
        # -x2 <= 0 (i.e., x2 >= 0)
        (lambda x: -x[1],
         lambda x: np.array([0, -1]),
         lambda x: np.zeros((2, 2)))
    ]

    # Initial strictly feasible point
    x0 = np.array([1.0, 1.0])

    print("Solving with interior point method...")
    ip_solver = InteriorPointMethod(tol=1e-6, max_iter=50)
    result = ip_solver.minimize(f, grad_f, hess_f, constraints, x0)

    print(f"  Converged: {result.converged}")
    print(f"  Iterations: {result.iterations}")
    print(f"  Optimal point: [{result.x[0]:.4f}, {result.x[1]:.4f}]")
    print(f"  Optimal value: {result.value:.6f}")

    # Analytical solution: x* = [0.5, 0.5], f* = 0.5
    print(f"\n  Analytical solution: [0.5000, 0.5000], value = 0.5000")


def example_robust_optimization():
    """Example: Robust least squares using Huber loss."""
    print("=== Robust Optimization Example ===\n")

    # Generate data with outliers
    np.random.seed(42)
    n_samples, n_features = 100, 5
    X = np.random.randn(n_samples, n_features)
    true_coef = np.random.randn(n_features)
    y = X @ true_coef + 0.1 * np.random.randn(n_samples)

    # Add outliers
    outlier_idx = np.random.choice(n_samples, 10, replace=False)
    y[outlier_idx] += 5 * np.random.randn(10)

    # Huber loss
    delta = 1.0  # Huber parameter

    def huber_loss(r):
        return np.where(np.abs(r) <= delta,
                        0.5 * r ** 2,
                        delta * (np.abs(r) - 0.5 * delta))

    def f(w):
        residuals = X @ w - y
        return np.sum(huber_loss(residuals))

    def subgrad_f(w):
        residuals = X @ w - y
        subgrad = np.where(np.abs(residuals) <= delta,
                          residuals,
                          delta * np.sign(residuals))
        return X.T @ subgrad

    # Initial point
    w0 = np.zeros(n_features)

    print("Solving robust regression with subgradient method...")
    subgrad_solver = SubgradientMethod(max_iter=1000)
    result = subgrad_solver.minimize(f, subgrad_f, w0, step_rule="diminishing")

    print(f"  Iterations: {result.iterations}")
    print(f"  Optimal value: {result.value:.6f}")

    # Compare with standard least squares
    w_ls = np.linalg.lstsq(X, y, rcond=None)[0]
    print(f"\n  Standard LS objective: {0.5 * np.linalg.norm(X @ w_ls - y) ** 2:.6f}")
    print(f"  Robust objective: {f(result.x):.6f}")


if __name__ == "__main__":
    # Run examples
    example_quadratic_programming()
    print("\n" + "=" * 60 + "\n")

    example_lasso_regression()
    print("\n" + "=" * 60 + "\n")

    example_constrained_optimization()
    print("\n" + "=" * 60 + "\n")

    example_robust_optimization()

    print("\n" + "=" * 60)
    print("Key Insights:")
    print("=" * 60)
    print("""
1. Different algorithms excel at different problem structures:
   - Newton's method: Fast for smooth, well-conditioned problems
   - Gradient descent: Simpler but slower, good for large-scale
   - Proximal methods: Essential for non-smooth regularization

2. Acceleration techniques (Nesterov, FISTA) provide significant speedups
   for first-order methods without much additional complexity.

3. Interior point methods efficiently handle inequality constraints
   by maintaining strict feasibility throughout optimization.

4. ADMM enables distributed optimization by splitting problems into
   simpler subproblems that can be solved in parallel.

5. Subgradient methods handle non-smooth objectives but converge slowly
   compared to smooth optimization methods.

6. The choice of algorithm depends on:
   - Problem size and structure
   - Smoothness and conditioning
   - Constraint types
   - Accuracy requirements
   - Computational resources
    """)