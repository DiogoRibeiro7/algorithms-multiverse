#!/usr/bin/env python3
"""
Support Vector Machine (SVM) Implementation

Implements SVM for classification with various kernels:
- Linear kernel
- Polynomial kernel
- RBF (Gaussian) kernel
- Sigmoid kernel

Uses simplified SMO (Sequential Minimal Optimization) algorithm for training.

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import Callable, Optional, Tuple, List
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist


class SVM:
    """
    Support Vector Machine classifier using SMO algorithm.

    Supports both linear and non-linear classification through kernel functions.
    """

    def __init__(self,
                 C: float = 1.0,
                 kernel: str = 'linear',
                 gamma: float = 'scale',
                 degree: int = 3,
                 coef0: float = 0.0,
                 tol: float = 1e-3,
                 max_iter: int = 1000,
                 random_state: Optional[int] = None):
        """
        Initialize SVM classifier.

        Args:
            C: Regularization parameter (soft margin)
            kernel: Kernel type ('linear', 'poly', 'rbf', 'sigmoid')
            gamma: Kernel coefficient for 'rbf', 'poly', 'sigmoid'
            degree: Degree for polynomial kernel
            coef0: Independent term in kernel function
            tol: Tolerance for stopping criterion
            max_iter: Maximum number of iterations
            random_state: Random seed for reproducibility
        """
        self.C = C
        self.kernel = kernel
        self.gamma = gamma
        self.degree = degree
        self.coef0 = coef0
        self.tol = tol
        self.max_iter = max_iter
        self.random_state = random_state

        # Will be set during fit
        self.alphas = None
        self.b = 0
        self.X = None
        self.y = None
        self.kernel_matrix = None
        self.support_vectors_ = None
        self.support_vector_indices_ = None
        self.dual_coef_ = None
        self.n_support_ = None

    def _kernel_function(self, X1: np.ndarray, X2: np.ndarray) -> np.ndarray:
        """
        Compute kernel matrix between X1 and X2.

        Args:
            X1: First set of samples
            X2: Second set of samples

        Returns:
            Kernel matrix
        """
        if self.kernel == 'linear':
            return np.dot(X1, X2.T)

        elif self.kernel == 'poly':
            return (self.gamma * np.dot(X1, X2.T) + self.coef0) ** self.degree

        elif self.kernel == 'rbf':
            # Compute pairwise squared Euclidean distances
            distances = cdist(X1, X2, metric='sqeuclidean')
            return np.exp(-self.gamma * distances)

        elif self.kernel == 'sigmoid':
            return np.tanh(self.gamma * np.dot(X1, X2.T) + self.coef0)

        else:
            raise ValueError(f"Unknown kernel: {self.kernel}")

    def _compute_kernel_matrix(self, X: np.ndarray) -> np.ndarray:
        """Compute the kernel matrix for training data"""
        n_samples = X.shape[0]
        K = self._kernel_function(X, X)
        # Ensure symmetry
        K = (K + K.T) / 2
        return K

    def _objective_function(self, alphas: np.ndarray) -> float:
        """
        Calculate the SVM objective function value.

        The dual objective to maximize:
        W(α) = Σα_i - 0.5 * ΣΣ α_i * α_j * y_i * y_j * K(x_i, x_j)
        """
        return np.sum(alphas) - 0.5 * np.sum(
            alphas[:, np.newaxis] * alphas[np.newaxis, :] *
            self.y[:, np.newaxis] * self.y[np.newaxis, :] *
            self.kernel_matrix
        )

    def _decision_function(self, X_test: np.ndarray) -> np.ndarray:
        """
        Compute decision function values.

        Args:
            X_test: Test samples

        Returns:
            Decision function values
        """
        if self.support_vector_indices_ is None or len(self.support_vector_indices_) == 0:
            # Fallback: use all training samples during training
            K = self._kernel_function(X_test, self.X)
            return np.dot(K, self.alphas * self.y) + self.b
        else:
            # Use support vectors after training
            K = self._kernel_function(X_test, self.X[self.support_vector_indices_])
            # Decision function: f(x) = Σ α_i * y_i * K(x, x_i) + b
            return np.dot(K, self.dual_coef_) + self.b

    def _select_alpha_pair(self, i1: int) -> Optional[int]:
        """
        Select second alpha using heuristic (maximum step size).

        Args:
            i1: Index of first alpha

        Returns:
            Index of second alpha or None
        """
        # Calculate error for i1
        decision = np.dot(self.kernel_matrix[i1], self.alphas * self.y) + self.b
        E1 = decision - self.y[i1]

        # Find non-bound alphas (0 < alpha < C)
        non_bound = np.logical_and(self.alphas > 0, self.alphas < self.C)
        non_bound_indices = np.where(non_bound)[0]

        if len(non_bound_indices) > 1:
            # Choose alpha with maximum |E1 - E2|
            errors = np.array([
                np.dot(self.kernel_matrix[i], self.alphas * self.y) + self.b - self.y[i]
                for i in non_bound_indices
            ])
            i2 = non_bound_indices[np.argmax(np.abs(E1 - errors))]
            if i2 != i1:
                return i2

        # Fallback to random selection
        candidates = list(range(len(self.alphas)))
        candidates.remove(i1)
        if candidates:
            return self.rng.choice(candidates)

        return None

    def _update_alpha_pair(self, i1: int, i2: int) -> bool:
        """
        Update a pair of alphas using SMO algorithm.

        Args:
            i1: Index of first alpha
            i2: Index of second alpha

        Returns:
            True if alphas were updated
        """
        if i1 == i2:
            return False

        alpha1_old = self.alphas[i1]
        alpha2_old = self.alphas[i2]
        y1 = self.y[i1]
        y2 = self.y[i2]

        # Calculate errors
        E1 = np.dot(self.kernel_matrix[i1], self.alphas * self.y) + self.b - y1
        E2 = np.dot(self.kernel_matrix[i2], self.alphas * self.y) + self.b - y2

        # Calculate bounds for alpha2
        if y1 != y2:
            L = max(0, alpha2_old - alpha1_old)
            H = min(self.C, self.C + alpha2_old - alpha1_old)
        else:
            L = max(0, alpha1_old + alpha2_old - self.C)
            H = min(self.C, alpha1_old + alpha2_old)

        if L == H:
            return False

        # Calculate eta (second derivative of objective)
        K11 = self.kernel_matrix[i1, i1]
        K12 = self.kernel_matrix[i1, i2]
        K22 = self.kernel_matrix[i2, i2]
        eta = K11 + K22 - 2 * K12

        if eta <= 0:
            # Kernel matrix is not positive definite
            return False

        # Calculate new alpha2
        alpha2_new = alpha2_old + y2 * (E1 - E2) / eta

        # Clip alpha2
        if alpha2_new > H:
            alpha2_new = H
        elif alpha2_new < L:
            alpha2_new = L

        # Check for significant change
        if abs(alpha2_new - alpha2_old) < 1e-5:
            return False

        # Calculate new alpha1
        alpha1_new = alpha1_old + y1 * y2 * (alpha2_old - alpha2_new)

        # Update alphas
        self.alphas[i1] = alpha1_new
        self.alphas[i2] = alpha2_new

        # Update bias term
        b1 = self.b - E1 - y1 * (alpha1_new - alpha1_old) * K11 - \
             y2 * (alpha2_new - alpha2_old) * K12
        b2 = self.b - E2 - y1 * (alpha1_new - alpha1_old) * K12 - \
             y2 * (alpha2_new - alpha2_old) * K22

        if 0 < alpha1_new < self.C:
            self.b = b1
        elif 0 < alpha2_new < self.C:
            self.b = b2
        else:
            self.b = (b1 + b2) / 2

        return True

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'SVM':
        """
        Fit the SVM model using SMO algorithm.

        Args:
            X: Training features of shape (n_samples, n_features)
            y: Training labels of shape (n_samples,) with values in {-1, 1}

        Returns:
            Self for method chaining
        """
        X = np.asarray(X)
        y = np.asarray(y)

        # Convert labels to {-1, 1}
        unique_labels = np.unique(y)
        if len(unique_labels) != 2:
            raise ValueError("SVM supports only binary classification")

        self.classes_ = unique_labels
        y = np.where(y == unique_labels[0], -1, 1)

        n_samples, n_features = X.shape

        # Set gamma for RBF/poly/sigmoid kernels
        if self.gamma == 'scale':
            self.gamma = 1 / (n_features * X.var())
        elif self.gamma == 'auto':
            self.gamma = 1 / n_features

        # Initialize
        self.X = X
        self.y = y
        self.alphas = np.zeros(n_samples)
        self.b = 0
        self.rng = np.random.RandomState(self.random_state)

        # Compute kernel matrix
        self.kernel_matrix = self._compute_kernel_matrix(X)

        # SMO main loop
        n_iter = 0
        while n_iter < self.max_iter:
            n_changed = 0

            # Loop over all samples
            for i1 in range(n_samples):
                # Check KKT conditions
                E1 = np.dot(self.kernel_matrix[i1], self.alphas * y) + self.b - y[i1]
                r1 = E1 * y[i1]

                if ((r1 < -self.tol and self.alphas[i1] < self.C) or
                    (r1 > self.tol and self.alphas[i1] > 0)):

                    # Select second alpha
                    i2 = self._select_alpha_pair(i1)
                    if i2 is not None:
                        if self._update_alpha_pair(i1, i2):
                            n_changed += 1

            # Check convergence
            if n_changed == 0:
                break

            n_iter += 1

        # Store support vectors
        sv_indices = self.alphas > 1e-5
        self.support_vector_indices_ = np.where(sv_indices)[0]
        self.support_vectors_ = X[sv_indices]
        self.dual_coef_ = (self.alphas * y)[sv_indices]
        self.n_support_ = len(self.support_vector_indices_)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels for samples in X.

        Args:
            X: Test samples of shape (n_samples, n_features)

        Returns:
            Predicted class labels
        """
        X = np.asarray(X)
        decision = self._decision_function(X)
        predictions = np.where(decision >= 0, 1, -1)
        # Convert back to original labels
        return np.where(predictions == -1, self.classes_[0], self.classes_[1])

    def decision_function(self, X: np.ndarray) -> np.ndarray:
        """
        Get decision function values for samples.

        Args:
            X: Test samples

        Returns:
            Decision function values (distance to hyperplane)
        """
        return self._decision_function(X)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate accuracy score.

        Args:
            X: Test features
            y: True labels

        Returns:
            Accuracy score between 0 and 1
        """
        predictions = self.predict(X)
        return np.mean(predictions == y)


class MultiClassSVM:
    """
    Multi-class SVM using One-vs-Rest (OvR) strategy.
    """

    def __init__(self, **svm_params):
        """
        Initialize multi-class SVM.

        Args:
            **svm_params: Parameters to pass to binary SVM classifiers
        """
        self.svm_params = svm_params
        self.classifiers = {}
        self.classes_ = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'MultiClassSVM':
        """
        Fit multi-class SVM using One-vs-Rest strategy.

        Args:
            X: Training features
            y: Training labels (can have more than 2 classes)

        Returns:
            Self for method chaining
        """
        X = np.asarray(X)
        y = np.asarray(y)

        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)

        if n_classes == 2:
            # Binary classification
            self.classifiers[0] = SVM(**self.svm_params)
            self.classifiers[0].fit(X, y)
        else:
            # One-vs-Rest for multi-class
            for i, class_label in enumerate(self.classes_):
                # Create binary labels: current class vs rest
                binary_y = np.where(y == class_label, 1, -1)

                # Train binary classifier
                clf = SVM(**self.svm_params)
                clf.fit(X, binary_y)
                self.classifiers[i] = clf

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels for samples.

        Args:
            X: Test samples

        Returns:
            Predicted class labels
        """
        X = np.asarray(X)

        if len(self.classes_) == 2:
            # Binary classification
            return self.classifiers[0].predict(X)

        # Multi-class: get decision values from all classifiers
        n_samples = X.shape[0]
        decision_values = np.zeros((n_samples, len(self.classes_)))

        for i, clf in self.classifiers.items():
            decision_values[:, i] = clf.decision_function(X)

        # Predict class with highest decision value
        predictions_idx = np.argmax(decision_values, axis=1)
        return self.classes_[predictions_idx]

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Calculate accuracy score"""
        predictions = self.predict(X)
        return np.mean(predictions == y)


def create_toy_dataset(n_samples: int = 200,
                       n_features: int = 2,
                       noise: float = 0.1,
                       random_state: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create a toy dataset for SVM demonstration.

    Args:
        n_samples: Number of samples
        n_features: Number of features
        noise: Noise level
        random_state: Random seed

    Returns:
        X: Features
        y: Labels
    """
    rng = np.random.RandomState(random_state)

    # Create two classes with some overlap
    n_samples_per_class = n_samples // 2

    # Class 1: centered around (-2, -2)
    X1 = rng.randn(n_samples_per_class, n_features) + [-2, -2]

    # Class 2: centered around (2, 2)
    X2 = rng.randn(n_samples_per_class, n_features) + [2, 2]

    # Add noise
    X1 += rng.randn(n_samples_per_class, n_features) * noise
    X2 += rng.randn(n_samples_per_class, n_features) * noise

    X = np.vstack([X1, X2])
    y = np.array([0] * n_samples_per_class + [1] * n_samples_per_class)

    # Shuffle
    indices = rng.permutation(n_samples)
    return X[indices], y[indices]


def create_nonlinear_dataset(n_samples: int = 200,
                            random_state: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create a non-linearly separable dataset (circles).

    Args:
        n_samples: Number of samples
        random_state: Random seed

    Returns:
        X: Features
        y: Labels
    """
    rng = np.random.RandomState(random_state)

    n_samples_per_class = n_samples // 2

    # Inner circle (class 0)
    theta_inner = rng.uniform(0, 2*np.pi, n_samples_per_class)
    r_inner = rng.uniform(0, 2, n_samples_per_class)
    X_inner = np.column_stack([r_inner * np.cos(theta_inner),
                               r_inner * np.sin(theta_inner)])

    # Outer circle (class 1)
    theta_outer = rng.uniform(0, 2*np.pi, n_samples_per_class)
    r_outer = rng.uniform(3, 5, n_samples_per_class)
    X_outer = np.column_stack([r_outer * np.cos(theta_outer),
                               r_outer * np.sin(theta_outer)])

    X = np.vstack([X_inner, X_outer])
    y = np.array([0] * n_samples_per_class + [1] * n_samples_per_class)

    # Shuffle
    indices = rng.permutation(n_samples)
    return X[indices], y[indices]


def plot_decision_boundary(svm_model, X: np.ndarray, y: np.ndarray,
                          title: str = "SVM Decision Boundary"):
    """
    Plot SVM decision boundary for 2D data.

    Args:
        svm_model: Trained SVM model
        X: Features (2D)
        y: Labels
        title: Plot title
    """
    if X.shape[1] != 2:
        print("Plotting requires 2D data")
        return

    plt.figure(figsize=(10, 8))

    # Create mesh
    h = 0.02  # Step size
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    # Get predictions for mesh
    Z = svm_model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Plot decision boundary
    plt.contourf(xx, yy, Z, alpha=0.4, cmap=plt.cm.RdYlBu)

    # Plot data points
    scatter = plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu,
                         edgecolors='black', s=50)

    # Highlight support vectors if available
    if hasattr(svm_model, 'support_vectors_') and svm_model.support_vectors_ is not None:
        plt.scatter(svm_model.support_vectors_[:, 0],
                   svm_model.support_vectors_[:, 1],
                   s=200, linewidth=1, facecolors='none',
                   edgecolors='green', label='Support Vectors')

    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def demonstrate_svm():
    """Demonstrate SVM with various kernels"""
    print("=" * 60)
    print("Support Vector Machine Demonstration")
    print("=" * 60)

    # 1. Linear SVM on linearly separable data
    print("\n1. Linear SVM on Linearly Separable Data")
    print("-" * 40)

    X_linear, y_linear = create_toy_dataset(n_samples=100, random_state=42)

    # Split data
    n_train = 80
    X_train, X_test = X_linear[:n_train], X_linear[n_train:]
    y_train, y_test = y_linear[:n_train], y_linear[n_train:]

    # Train linear SVM
    svm_linear = SVM(C=1.0, kernel='linear', random_state=42)
    svm_linear.fit(X_train, y_train)

    train_score = svm_linear.score(X_train, y_train)
    test_score = svm_linear.score(X_test, y_test)

    print(f"Training accuracy: {train_score:.3f}")
    print(f"Testing accuracy: {test_score:.3f}")
    print(f"Number of support vectors: {svm_linear.n_support_}")

    # Visualize
    plot_decision_boundary(svm_linear, X_train, y_train,
                          "Linear SVM Decision Boundary")

    # 2. RBF kernel on non-linear data
    print("\n2. RBF Kernel SVM on Non-linear Data")
    print("-" * 40)

    X_nonlinear, y_nonlinear = create_nonlinear_dataset(n_samples=200, random_state=42)

    # Split data
    X_train, X_test = X_nonlinear[:160], X_nonlinear[160:]
    y_train, y_test = y_nonlinear[:160], y_nonlinear[160:]

    # Try different kernels
    kernels = ['linear', 'rbf', 'poly']

    for kernel in kernels:
        if kernel == 'poly':
            svm = SVM(C=1.0, kernel=kernel, degree=3, random_state=42)
        else:
            svm = SVM(C=1.0, kernel=kernel, random_state=42)

        svm.fit(X_train, y_train)
        score = svm.score(X_test, y_test)

        print(f"{kernel:8s} kernel: Accuracy = {score:.3f}, "
              f"Support vectors = {svm.n_support_}")

        if kernel == 'rbf':
            plot_decision_boundary(svm, X_train, y_train,
                                  f"RBF Kernel SVM Decision Boundary")

    # 3. Effect of regularization parameter C
    print("\n3. Effect of Regularization Parameter C")
    print("-" * 40)

    C_values = [0.01, 0.1, 1.0, 10.0, 100.0]

    for C in C_values:
        svm = SVM(C=C, kernel='rbf', random_state=42)
        svm.fit(X_train, y_train)

        train_acc = svm.score(X_train, y_train)
        test_acc = svm.score(X_test, y_test)

        print(f"C = {C:6.2f}: Train = {train_acc:.3f}, "
              f"Test = {test_acc:.3f}, SVs = {svm.n_support_}")

    # 4. Multi-class classification
    print("\n4. Multi-class Classification")
    print("-" * 40)

    # Create 3-class dataset
    np.random.seed(42)
    X_multi = np.vstack([
        np.random.randn(30, 2) + [0, 0],
        np.random.randn(30, 2) + [3, 3],
        np.random.randn(30, 2) + [-3, 3]
    ])
    y_multi = np.array([0] * 30 + [1] * 30 + [2] * 30)

    # Shuffle
    indices = np.random.permutation(90)
    X_multi, y_multi = X_multi[indices], y_multi[indices]

    # Train multi-class SVM
    mc_svm = MultiClassSVM(C=1.0, kernel='rbf', random_state=42)
    mc_svm.fit(X_multi[:70], y_multi[:70])

    score = mc_svm.score(X_multi[70:], y_multi[70:])
    print(f"Multi-class SVM accuracy: {score:.3f}")

    # 5. Decision function values
    print("\n5. Decision Function Analysis")
    print("-" * 40)

    # Get decision values for some test points
    test_points = np.array([[0, 0], [2, 2], [-2, -2]])
    decisions = svm_linear.decision_function(test_points)
    predictions = svm_linear.predict(test_points)

    for i, (point, decision, pred) in enumerate(zip(test_points, decisions, predictions)):
        print(f"Point {point}: Decision = {decision:.3f}, Prediction = {pred}")


if __name__ == "__main__":
    demonstrate_svm()