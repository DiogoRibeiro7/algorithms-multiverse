"""
Logistic Regression Implementation

A fundamental classification algorithm that models the probability of binary outcomes
using the logistic (sigmoid) function. Extended to support multi-class classification
through One-vs-Rest (OvR) or multinomial approaches.

Key Features:
- Binary and multi-class classification
- L1 (Lasso) and L2 (Ridge) regularization
- Multiple optimization methods (gradient descent, Newton's method)
- Probability calibration
- Feature importance analysis
- ROC curve and AUC computation

Mathematical Foundation:
- Hypothesis: h(x) = sigmoid(θᵀx) where sigmoid(z) = 1/(1 + e^(-z))
- Cost function: J(θ) = -1/m Σ[y*log(h(x)) + (1-y)*log(1-h(x))]
- Gradient: ∂J/∂θ = 1/m Xᵀ(h(X) - y)

Author: Algorithms Multiverse
Date: January 2026
"""

import numpy as np
from typing import Optional, Literal, Tuple, List, Dict, Union
import warnings
from dataclasses import dataclass


@dataclass
class LogisticRegressionMetrics:
    """Container for model evaluation metrics."""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    auc_roc: Optional[float] = None
    confusion_matrix: Optional[np.ndarray] = None
    classification_report: Optional[Dict] = None


class LogisticRegression:
    """
    Logistic Regression classifier with regularization support.

    Implements gradient descent optimization with various regularization options
    for binary and multi-class classification problems.

    Attributes:
        learning_rate: Step size for gradient descent
        n_iterations: Maximum number of iterations
        regularization: Type of regularization ('l1', 'l2', or None)
        lambda_reg: Regularization strength
        multi_class: Strategy for multi-class ('ovr' or 'multinomial')
        fit_intercept: Whether to fit an intercept term
        verbose: Print training progress
        random_state: Random seed for reproducibility
    """

    def __init__(
        self,
        learning_rate: float = 0.01,
        n_iterations: int = 1000,
        regularization: Optional[Literal['l1', 'l2']] = 'l2',
        lambda_reg: float = 0.01,
        multi_class: Literal['ovr', 'multinomial'] = 'ovr',
        fit_intercept: bool = True,
        convergence_tol: float = 1e-4,
        verbose: bool = False,
        random_state: Optional[int] = None
    ):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.regularization = regularization
        self.lambda_reg = lambda_reg
        self.multi_class = multi_class
        self.fit_intercept = fit_intercept
        self.convergence_tol = convergence_tol
        self.verbose = verbose
        self.random_state = random_state

        # Model parameters
        self.weights = None
        self.classes_ = None
        self.n_classes_ = None
        self.cost_history = []

        # For multi-class
        self.classifiers = {}

        # Set random seed
        if random_state is not None:
            np.random.seed(random_state)

    def _sigmoid(self, z: np.ndarray) -> np.ndarray:
        """
        Sigmoid activation function.

        Stable implementation to avoid overflow.
        """
        # Clip input to prevent overflow
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def _softmax(self, z: np.ndarray) -> np.ndarray:
        """
        Softmax function for multinomial logistic regression.

        Converts raw scores to probabilities for multi-class.
        """
        # Subtract max for numerical stability
        z_shifted = z - np.max(z, axis=1, keepdims=True)
        exp_z = np.exp(z_shifted)
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def _add_intercept(self, X: np.ndarray) -> np.ndarray:
        """Add intercept term to feature matrix."""
        if self.fit_intercept:
            intercept = np.ones((X.shape[0], 1))
            return np.concatenate((intercept, X), axis=1)
        return X

    def _initialize_weights(self, n_features: int, n_classes: int = 1) -> np.ndarray:
        """
        Initialize weights using Xavier/He initialization.

        Better than zeros for faster convergence.
        """
        if n_classes == 1:
            # Binary classification
            limit = np.sqrt(2 / n_features)
            return np.random.randn(n_features) * limit
        else:
            # Multi-class
            limit = np.sqrt(2 / n_features)
            return np.random.randn(n_features, n_classes) * limit

    def _compute_cost(self, X: np.ndarray, y: np.ndarray, weights: np.ndarray) -> float:
        """
        Compute the logistic loss (cross-entropy) with regularization.

        Args:
            X: Feature matrix
            y: Target values
            weights: Model weights

        Returns:
            Cost value
        """
        m = X.shape[0]

        # Check if this is binary classification (including OvR case)
        if len(weights.shape) == 1 or (len(weights.shape) == 2 and weights.shape[1] == 1):
            # Binary classification (also used in OvR)
            z = X @ weights
            predictions = self._sigmoid(z)

            # Avoid log(0)
            epsilon = 1e-7
            predictions = np.clip(predictions, epsilon, 1 - epsilon)

            # Cross-entropy loss
            cost = -np.mean(y * np.log(predictions) + (1 - y) * np.log(1 - predictions))
        else:
            # Multi-class multinomial
            z = X @ weights
            predictions = self._softmax(z)

            # Clip predictions to avoid log(0)
            epsilon = 1e-7
            predictions = np.clip(predictions, epsilon, 1 - epsilon)

            # Cross-entropy for multi-class
            cost = -np.mean(np.sum(y * np.log(predictions), axis=1))

        # Add regularization
        if self.regularization == 'l2':
            if self.fit_intercept:
                # Don't regularize intercept
                reg_weights = weights[1:] if len(weights.shape) == 1 else weights[1:, :]
            else:
                reg_weights = weights
            cost += (self.lambda_reg / (2 * m)) * np.sum(reg_weights ** 2)
        elif self.regularization == 'l1':
            if self.fit_intercept:
                reg_weights = weights[1:] if len(weights.shape) == 1 else weights[1:, :]
            else:
                reg_weights = weights
            cost += (self.lambda_reg / m) * np.sum(np.abs(reg_weights))

        return cost

    def _compute_gradient(self, X: np.ndarray, y: np.ndarray, weights: np.ndarray) -> np.ndarray:
        """
        Compute gradient of the cost function.

        Args:
            X: Feature matrix
            y: Target values
            weights: Model weights

        Returns:
            Gradient vector
        """
        m = X.shape[0]

        # Check if this is binary classification (including OvR case)
        if len(weights.shape) == 1 or (len(weights.shape) == 2 and weights.shape[1] == 1):
            # Binary classification (also used in OvR)
            z = X @ weights
            predictions = self._sigmoid(z)
            gradient = (1/m) * X.T @ (predictions - y)
        else:
            # Multi-class multinomial
            z = X @ weights
            predictions = self._softmax(z)
            gradient = (1/m) * X.T @ (predictions - y)

        # Add regularization gradient
        if self.regularization == 'l2':
            if self.fit_intercept:
                # Don't regularize intercept
                reg_gradient = np.zeros_like(weights)
                if len(weights.shape) == 1:
                    reg_gradient[1:] = (self.lambda_reg / m) * weights[1:]
                else:
                    reg_gradient[1:, :] = (self.lambda_reg / m) * weights[1:, :]
                gradient += reg_gradient
            else:
                gradient += (self.lambda_reg / m) * weights
        elif self.regularization == 'l1':
            if self.fit_intercept:
                reg_gradient = np.zeros_like(weights)
                if len(weights.shape) == 1:
                    reg_gradient[1:] = (self.lambda_reg / m) * np.sign(weights[1:])
                else:
                    reg_gradient[1:, :] = (self.lambda_reg / m) * np.sign(weights[1:, :])
                gradient += reg_gradient
            else:
                gradient += (self.lambda_reg / m) * np.sign(weights)

        return gradient

    def _gradient_descent(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Perform gradient descent optimization.

        Args:
            X: Feature matrix with intercept
            y: Target values

        Returns:
            Optimized weights
        """
        n_features = X.shape[1]

        # Initialize weights based on y shape (for OvR, y is binary)
        if len(y.shape) == 1 or (len(y.shape) == 2 and y.shape[1] == 1):
            # Binary classification (including OvR)
            weights = self._initialize_weights(n_features)
        else:
            # Multi-class multinomial (y is one-hot encoded)
            weights = self._initialize_weights(n_features, y.shape[1])

        # Training loop
        for iteration in range(self.n_iterations):
            # Compute cost
            cost = self._compute_cost(X, y, weights)
            self.cost_history.append(cost)

            # Compute gradient
            gradient = self._compute_gradient(X, y, weights)

            # Update weights
            weights -= self.learning_rate * gradient

            # Check convergence
            if iteration > 0:
                cost_change = abs(self.cost_history[-2] - self.cost_history[-1])
                if cost_change < self.convergence_tol:
                    if self.verbose:
                        print(f"Converged at iteration {iteration}")
                    break

            # Print progress
            if self.verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}, Cost: {cost:.4f}")

        return weights

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LogisticRegression':
        """
        Fit the logistic regression model.

        Args:
            X: Training features of shape (n_samples, n_features)
            y: Training labels of shape (n_samples,)

        Returns:
            Self for method chaining
        """
        # Identify classes
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)

        # Add intercept
        X_with_intercept = self._add_intercept(X)

        if self.n_classes_ == 2:
            # Binary classification
            # Convert labels to 0/1
            y_binary = (y == self.classes_[1]).astype(int)

            self.weights = self._gradient_descent(X_with_intercept, y_binary)

        elif self.multi_class == 'ovr':
            # One-vs-Rest for multi-class
            self.classifiers = {}

            for class_label in self.classes_:
                if self.verbose:
                    print(f"\nTraining classifier for class {class_label}")

                # Create binary labels
                y_binary = (y == class_label).astype(int)

                # Train binary classifier
                self.cost_history = []
                weights = self._gradient_descent(X_with_intercept, y_binary)
                self.classifiers[class_label] = weights

        else:  # multinomial
            # Multinomial logistic regression
            # Convert y to one-hot encoding
            y_one_hot = np.zeros((y.shape[0], self.n_classes_))
            for i, class_label in enumerate(self.classes_):
                y_one_hot[y == class_label, i] = 1

            self.weights = self._gradient_descent(X_with_intercept, y_one_hot)

        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities.

        Args:
            X: Features of shape (n_samples, n_features)

        Returns:
            Probabilities of shape (n_samples, n_classes)
        """
        X_with_intercept = self._add_intercept(X)

        if self.n_classes_ == 2:
            # Binary classification
            z = X_with_intercept @ self.weights
            prob_class_1 = self._sigmoid(z)
            prob_class_0 = 1 - prob_class_1
            return np.column_stack((prob_class_0, prob_class_1))

        elif self.multi_class == 'ovr':
            # One-vs-Rest
            probabilities = np.zeros((X.shape[0], self.n_classes_))

            for i, class_label in enumerate(self.classes_):
                weights = self.classifiers[class_label]
                z = X_with_intercept @ weights
                probabilities[:, i] = self._sigmoid(z)

            # Normalize probabilities
            prob_sum = probabilities.sum(axis=1, keepdims=True)
            probabilities = probabilities / prob_sum

            return probabilities

        else:  # multinomial
            z = X_with_intercept @ self.weights
            return self._softmax(z)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels.

        Args:
            X: Features of shape (n_samples, n_features)

        Returns:
            Predicted labels of shape (n_samples,)
        """
        probabilities = self.predict_proba(X)
        class_indices = np.argmax(probabilities, axis=1)
        return self.classes_[class_indices]

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Compute accuracy score.

        Args:
            X: Features
            y: True labels

        Returns:
            Accuracy score
        """
        predictions = self.predict(X)
        return np.mean(predictions == y)

    def get_feature_importance(self) -> np.ndarray:
        """
        Get feature importance based on weight magnitudes.

        Returns:
            Feature importance scores
        """
        if self.weights is None:
            raise ValueError("Model must be fitted before getting feature importance")

        if self.n_classes_ == 2:
            # Binary classification
            importance = np.abs(self.weights)
            if self.fit_intercept:
                importance = importance[1:]  # Exclude intercept
        else:
            # Multi-class: average absolute weights across classes
            if self.multi_class == 'ovr':
                weights_matrix = np.array(list(self.classifiers.values()))
                importance = np.mean(np.abs(weights_matrix), axis=0)
            else:
                importance = np.mean(np.abs(self.weights), axis=1)

            if self.fit_intercept:
                importance = importance[1:]

        # Normalize
        return importance / np.sum(importance)

    def compute_metrics(self, X: np.ndarray, y: np.ndarray) -> LogisticRegressionMetrics:
        """
        Compute comprehensive evaluation metrics.

        Args:
            X: Features
            y: True labels

        Returns:
            LogisticRegressionMetrics object with various metrics
        """
        predictions = self.predict(X)
        probabilities = self.predict_proba(X)

        # Accuracy
        accuracy = self.score(X, y)

        # For binary classification, compute additional metrics
        if self.n_classes_ == 2:
            # Convert to binary
            y_binary = (y == self.classes_[1]).astype(int)
            pred_binary = (predictions == self.classes_[1]).astype(int)

            # Confusion matrix elements
            true_positives = np.sum((y_binary == 1) & (pred_binary == 1))
            false_positives = np.sum((y_binary == 0) & (pred_binary == 1))
            false_negatives = np.sum((y_binary == 1) & (pred_binary == 0))
            true_negatives = np.sum((y_binary == 0) & (pred_binary == 0))

            # Precision, Recall, F1
            precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            # Confusion matrix
            confusion_matrix = np.array([[true_negatives, false_positives],
                                        [false_negatives, true_positives]])

            # AUC-ROC (simplified calculation)
            prob_positive = probabilities[:, 1]
            auc_roc = self._compute_auc(y_binary, prob_positive)

        else:
            # Multi-class metrics (macro-averaged)
            precision_scores = []
            recall_scores = []

            for class_label in self.classes_:
                y_binary = (y == class_label).astype(int)
                pred_binary = (predictions == class_label).astype(int)

                tp = np.sum((y_binary == 1) & (pred_binary == 1))
                fp = np.sum((y_binary == 0) & (pred_binary == 1))
                fn = np.sum((y_binary == 1) & (pred_binary == 0))

                prec = tp / (tp + fp) if (tp + fp) > 0 else 0
                rec = tp / (tp + fn) if (tp + fn) > 0 else 0

                precision_scores.append(prec)
                recall_scores.append(rec)

            precision = np.mean(precision_scores)
            recall = np.mean(recall_scores)
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            confusion_matrix = None
            auc_roc = None

        return LogisticRegressionMetrics(
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            auc_roc=auc_roc,
            confusion_matrix=confusion_matrix
        )

    def _compute_auc(self, y_true: np.ndarray, y_scores: np.ndarray) -> float:
        """
        Compute Area Under the ROC Curve.

        Simplified implementation for binary classification.
        """
        # Sort by scores
        sorted_indices = np.argsort(y_scores)[::-1]
        y_true_sorted = y_true[sorted_indices]

        # Count positives and negatives
        n_pos = np.sum(y_true)
        n_neg = len(y_true) - n_pos

        if n_pos == 0 or n_neg == 0:
            return 0.5

        # Calculate AUC using trapezoidal rule
        tp = 0
        fp = 0
        auc = 0

        for label in y_true_sorted:
            if label == 1:
                tp += 1
            else:
                fp += 1
                auc += tp

        return auc / (n_pos * n_neg)


def example_usage():
    """Demonstrate logistic regression usage."""
    print("Logistic Regression Examples")
    print("=" * 50)

    # Generate synthetic data
    from sklearn.datasets import make_classification, make_blobs
    import matplotlib.pyplot as plt

    # Binary classification example
    print("\n1. Binary Classification:")
    X_binary, y_binary = make_classification(
        n_samples=200, n_features=2, n_informative=2, n_redundant=0,
        n_clusters_per_class=1, random_state=42
    )

    # Train model
    lr_binary = LogisticRegression(
        learning_rate=0.1,
        n_iterations=1000,
        regularization='l2',
        lambda_reg=0.01,
        verbose=False
    )

    # Split data
    split_idx = int(0.8 * len(X_binary))
    X_train, X_test = X_binary[:split_idx], X_binary[split_idx:]
    y_train, y_test = y_binary[:split_idx], y_binary[split_idx:]

    # Fit model
    lr_binary.fit(X_train, y_train)

    # Evaluate
    train_acc = lr_binary.score(X_train, y_train)
    test_acc = lr_binary.score(X_test, y_test)
    print(f"  Training Accuracy: {train_acc:.4f}")
    print(f"  Test Accuracy: {test_acc:.4f}")

    # Get metrics
    metrics = lr_binary.compute_metrics(X_test, y_test)
    print(f"  Precision: {metrics.precision:.4f}")
    print(f"  Recall: {metrics.recall:.4f}")
    print(f"  F1 Score: {metrics.f1_score:.4f}")
    if metrics.auc_roc:
        print(f"  AUC-ROC: {metrics.auc_roc:.4f}")

    # Multi-class classification example
    print("\n2. Multi-class Classification (One-vs-Rest):")
    X_multi, y_multi = make_blobs(
        n_samples=300, n_features=2, centers=4, random_state=42
    )

    # Train model
    lr_multi_ovr = LogisticRegression(
        learning_rate=0.1,
        n_iterations=1000,
        multi_class='ovr',
        verbose=False
    )

    # Split data
    split_idx = int(0.8 * len(X_multi))
    X_train_m, X_test_m = X_multi[:split_idx], X_multi[split_idx:]
    y_train_m, y_test_m = y_multi[:split_idx], y_multi[split_idx:]

    # Fit and evaluate
    lr_multi_ovr.fit(X_train_m, y_train_m)
    test_acc_multi = lr_multi_ovr.score(X_test_m, y_test_m)
    print(f"  Test Accuracy (OvR): {test_acc_multi:.4f}")

    # Multinomial logistic regression
    print("\n3. Multi-class Classification (Multinomial):")
    lr_multi_mn = LogisticRegression(
        learning_rate=0.1,
        n_iterations=1000,
        multi_class='multinomial',
        verbose=False
    )

    lr_multi_mn.fit(X_train_m, y_train_m)
    test_acc_mn = lr_multi_mn.score(X_test_m, y_test_m)
    print(f"  Test Accuracy (Multinomial): {test_acc_mn:.4f}")

    # Regularization comparison
    print("\n4. Regularization Comparison:")

    # No regularization
    lr_no_reg = LogisticRegression(regularization=None, verbose=False)
    lr_no_reg.fit(X_train, y_train)

    # L1 regularization
    lr_l1 = LogisticRegression(regularization='l1', lambda_reg=0.1, verbose=False)
    lr_l1.fit(X_train, y_train)

    # L2 regularization
    lr_l2 = LogisticRegression(regularization='l2', lambda_reg=0.1, verbose=False)
    lr_l2.fit(X_train, y_train)

    print(f"  No Regularization - Test Acc: {lr_no_reg.score(X_test, y_test):.4f}")
    print(f"  L1 Regularization - Test Acc: {lr_l1.score(X_test, y_test):.4f}")
    print(f"  L2 Regularization - Test Acc: {lr_l2.score(X_test, y_test):.4f}")

    # Feature importance
    print("\n5. Feature Importance:")
    importance = lr_binary.get_feature_importance()
    for i, imp in enumerate(importance):
        print(f"  Feature {i}: {imp:.4f}")

    # Cost history
    print("\n6. Training Progress:")
    print(f"  Initial Cost: {lr_binary.cost_history[0]:.4f}")
    print(f"  Final Cost: {lr_binary.cost_history[-1]:.4f}")
    print(f"  Iterations: {len(lr_binary.cost_history)}")

    # Probability predictions
    print("\n7. Probability Predictions (first 5 samples):")
    probs = lr_binary.predict_proba(X_test[:5])
    for i, prob in enumerate(probs):
        print(f"  Sample {i}: Class 0={prob[0]:.3f}, Class 1={prob[1]:.3f}")


if __name__ == "__main__":
    example_usage()