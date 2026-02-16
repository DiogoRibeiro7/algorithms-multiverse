#!/usr/bin/env python3
"""
K-Nearest Neighbors (KNN) Algorithm Implementation

KNN is a simple, non-parametric, lazy learning algorithm used for both
classification and regression. It makes predictions based on the k nearest
training examples in the feature space.

Key Concepts:
- No training phase (lazy learning) - stores all training data
- Prediction by majority vote (classification) or average (regression)
- Distance metrics: Euclidean, Manhattan, Minkowski
- Choice of k affects bias-variance tradeoff

Time Complexity:
- Training: O(1) - just stores the data
- Prediction: O(n*m*k) where n=samples, m=features, k=neighbors
- Can be improved with KD-trees or Ball trees to O(log n)

Space Complexity: O(n*m) - stores all training data

Applications:
- Pattern recognition
- Recommendation systems
- Missing value imputation
- Anomaly detection

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import List, Tuple, Optional, Union, Callable
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


class KNN:
    """
    K-Nearest Neighbors for Classification and Regression

    This implementation supports multiple distance metrics and both
    uniform and distance-weighted voting.

    Attributes:
        k (int): Number of neighbors to consider
        metric (str): Distance metric to use
        weights (str): Weighting scheme for neighbors
        X_train (np.ndarray): Stored training features
        y_train (np.ndarray): Stored training labels
        task (str): 'classification' or 'regression'
    """

    def __init__(self, k: int = 5, metric: str = 'euclidean',
                 weights: str = 'uniform', task: str = 'classification'):
        """
        Initialize KNN model

        Args:
            k: Number of neighbors
            metric: Distance metric ('euclidean', 'manhattan', 'minkowski', 'cosine')
            weights: 'uniform' or 'distance' weighted voting
            task: 'classification' or 'regression'
        """
        self.k = k
        self.metric = metric
        self.weights = weights
        self.task = task
        self.X_train = None
        self.y_train = None
        self.classes_ = None

    def _euclidean_distance(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """Calculate Euclidean distance between two points"""
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def _manhattan_distance(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """Calculate Manhattan distance between two points"""
        return np.sum(np.abs(x1 - x2))

    def _minkowski_distance(self, x1: np.ndarray, x2: np.ndarray,
                          p: int = 3) -> float:
        """Calculate Minkowski distance between two points"""
        return np.sum(np.abs(x1 - x2) ** p) ** (1/p)

    def _cosine_distance(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """Calculate Cosine distance (1 - cosine similarity)"""
        dot_product = np.dot(x1, x2)
        norm_x1 = np.linalg.norm(x1)
        norm_x2 = np.linalg.norm(x2)

        if norm_x1 == 0 or norm_x2 == 0:
            return 1.0

        similarity = dot_product / (norm_x1 * norm_x2)
        return 1 - similarity

    def _get_distance_function(self) -> Callable:
        """Return the appropriate distance function based on metric"""
        distance_functions = {
            'euclidean': self._euclidean_distance,
            'manhattan': self._manhattan_distance,
            'minkowski': self._minkowski_distance,
            'cosine': self._cosine_distance
        }

        if self.metric not in distance_functions:
            raise ValueError(f"Unknown metric: {self.metric}")

        return distance_functions[self.metric]

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'KNN':
        """
        Fit the KNN model (store training data)

        Args:
            X: Training features (n_samples x n_features)
            y: Training labels/targets (n_samples,)

        Returns:
            Self (for method chaining)
        """
        self.X_train = X
        self.y_train = y

        # Store unique classes for classification
        if self.task == 'classification':
            self.classes_ = np.unique(y)

        return self

    def _get_neighbors(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Find k nearest neighbors for a single sample

        Args:
            x: Query point (n_features,)

        Returns:
            Tuple of (neighbor_indices, distances)
        """
        distance_func = self._get_distance_function()

        # Calculate distances to all training points
        distances = []
        for i, x_train in enumerate(self.X_train):
            dist = distance_func(x, x_train)
            distances.append((dist, i))

        # Sort by distance and get k nearest
        distances.sort(key=lambda x: x[0])
        k_nearest = distances[:self.k]

        # Extract indices and distances
        neighbor_distances = np.array([d for d, _ in k_nearest])
        neighbor_indices = np.array([i for _, i in k_nearest])

        return neighbor_indices, neighbor_distances

    def _predict_classification(self, x: np.ndarray) -> int:
        """
        Predict class for a single sample

        Args:
            x: Query point

        Returns:
            Predicted class label
        """
        neighbor_indices, neighbor_distances = self._get_neighbors(x)
        neighbor_labels = self.y_train[neighbor_indices]

        if self.weights == 'uniform':
            # Simple majority vote
            vote_counts = Counter(neighbor_labels)
            return vote_counts.most_common(1)[0][0]

        elif self.weights == 'distance':
            # Weighted vote based on inverse distance
            vote_weights = {}
            for label, dist in zip(neighbor_labels, neighbor_distances):
                if dist == 0:
                    # Handle exact match
                    return label
                weight = 1 / dist
                vote_weights[label] = vote_weights.get(label, 0) + weight

            return max(vote_weights, key=vote_weights.get)

    def _predict_regression(self, x: np.ndarray) -> float:
        """
        Predict value for a single sample (regression)

        Args:
            x: Query point

        Returns:
            Predicted value
        """
        neighbor_indices, neighbor_distances = self._get_neighbors(x)
        neighbor_values = self.y_train[neighbor_indices]

        if self.weights == 'uniform':
            # Simple average
            return np.mean(neighbor_values)

        elif self.weights == 'distance':
            # Weighted average based on inverse distance
            if np.any(neighbor_distances == 0):
                # Handle exact match
                zero_idx = np.where(neighbor_distances == 0)[0][0]
                return neighbor_values[zero_idx]

            weights = 1 / neighbor_distances
            weighted_sum = np.sum(neighbor_values * weights)
            weight_sum = np.sum(weights)
            return weighted_sum / weight_sum

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions for multiple samples

        Args:
            X: Query points (n_samples x n_features)

        Returns:
            Predictions (n_samples,)
        """
        if self.X_train is None:
            raise ValueError("Model must be fitted before prediction")

        predictions = []
        for x in X:
            if self.task == 'classification':
                pred = self._predict_classification(x)
            else:
                pred = self._predict_regression(x)
            predictions.append(pred)

        return np.array(predictions)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities (classification only)

        Args:
            X: Query points (n_samples x n_features)

        Returns:
            Class probabilities (n_samples x n_classes)
        """
        if self.task != 'classification':
            raise ValueError("predict_proba only works for classification")

        if self.X_train is None:
            raise ValueError("Model must be fitted before prediction")

        n_samples = X.shape[0]
        n_classes = len(self.classes_)
        probabilities = np.zeros((n_samples, n_classes))

        for i, x in enumerate(X):
            neighbor_indices, neighbor_distances = self._get_neighbors(x)
            neighbor_labels = self.y_train[neighbor_indices]

            if self.weights == 'uniform':
                # Count votes for each class
                for class_idx, class_label in enumerate(self.classes_):
                    count = np.sum(neighbor_labels == class_label)
                    probabilities[i, class_idx] = count / self.k

            elif self.weights == 'distance':
                # Weighted votes
                for class_idx, class_label in enumerate(self.classes_):
                    mask = neighbor_labels == class_label
                    if np.any(mask):
                        distances = neighbor_distances[mask]
                        if np.any(distances == 0):
                            probabilities[i, class_idx] = 1.0
                            break
                        else:
                            weights = 1 / distances
                            probabilities[i, class_idx] = np.sum(weights)

                # Normalize to get probabilities
                row_sum = np.sum(probabilities[i, :])
                if row_sum > 0:
                    probabilities[i, :] /= row_sum

        return probabilities

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate accuracy (classification) or R² (regression)

        Args:
            X: Test features
            y: True labels/values

        Returns:
            Score (accuracy or R²)
        """
        predictions = self.predict(X)

        if self.task == 'classification':
            return np.mean(predictions == y)
        else:
            ss_res = np.sum((y - predictions) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            return 1 - (ss_res / ss_tot)

    def get_params(self) -> dict:
        """Get model parameters"""
        return {
            'k': self.k,
            'metric': self.metric,
            'weights': self.weights,
            'task': self.task
        }

    def set_params(self, **params):
        """Set model parameters"""
        for param, value in params.items():
            setattr(self, param, value)
        return self


class KNNOptimizer:
    """
    Optimizer for finding the best k value using cross-validation

    Implements elbow method and cross-validation for hyperparameter tuning.
    """

    def __init__(self, k_range: Tuple[int, int] = (1, 20),
                 cv_folds: int = 5):
        """
        Initialize KNN optimizer

        Args:
            k_range: Range of k values to test (min, max)
            cv_folds: Number of cross-validation folds
        """
        self.k_range = k_range
        self.cv_folds = cv_folds
        self.scores = {}
        self.best_k = None

    def _cross_validate(self, X: np.ndarray, y: np.ndarray,
                       k: int, **knn_params) -> float:
        """
        Perform k-fold cross-validation for a specific k value

        Args:
            X: Features
            y: Labels
            k: Number of neighbors
            **knn_params: Additional KNN parameters

        Returns:
            Mean cross-validation score
        """
        n_samples = X.shape[0]
        fold_size = n_samples // self.cv_folds
        scores = []

        for fold in range(self.cv_folds):
            # Create validation fold
            val_start = fold * fold_size
            val_end = val_start + fold_size if fold < self.cv_folds - 1 else n_samples

            val_indices = np.arange(val_start, val_end)
            train_indices = np.concatenate([
                np.arange(0, val_start),
                np.arange(val_end, n_samples)
            ])

            X_train_fold = X[train_indices]
            y_train_fold = y[train_indices]
            X_val_fold = X[val_indices]
            y_val_fold = y[val_indices]

            # Train and evaluate
            knn = KNN(k=k, **knn_params)
            knn.fit(X_train_fold, y_train_fold)
            score = knn.score(X_val_fold, y_val_fold)
            scores.append(score)

        return np.mean(scores)

    def find_best_k(self, X: np.ndarray, y: np.ndarray,
                   **knn_params) -> int:
        """
        Find the best k value using cross-validation

        Args:
            X: Training features
            y: Training labels
            **knn_params: Additional KNN parameters

        Returns:
            Best k value
        """
        k_values = range(self.k_range[0], self.k_range[1] + 1)

        for k in k_values:
            score = self._cross_validate(X, y, k, **knn_params)
            self.scores[k] = score

        # Find best k
        self.best_k = max(self.scores, key=self.scores.get)
        return self.best_k

    def plot_elbow_curve(self):
        """Plot the elbow curve for k selection"""
        if not self.scores:
            print("Run find_best_k first to generate scores")
            return

        plt.figure(figsize=(10, 6))
        k_values = list(self.scores.keys())
        score_values = list(self.scores.values())

        plt.plot(k_values, score_values, 'b-o')
        plt.axvline(x=self.best_k, color='r', linestyle='--',
                   label=f'Best k = {self.best_k}')
        plt.xlabel('k (Number of Neighbors)')
        plt.ylabel('Cross-Validation Score')
        plt.title('KNN Elbow Curve - Finding Optimal k')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()


def visualize_knn_classification(X: np.ndarray, y: np.ndarray,
                                k: int = 5, test_point: Optional[np.ndarray] = None):
    """
    Visualize KNN classification decision boundaries (2D only)

    Args:
        X: Training features (must be 2D)
        y: Training labels
        k: Number of neighbors
        test_point: Optional test point to highlight
    """
    if X.shape[1] != 2:
        print("Visualization only works for 2D features")
        return

    # Train KNN
    knn = KNN(k=k, task='classification')
    knn.fit(X, y)

    # Create mesh grid
    h = 0.02  # step size
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                        np.arange(y_min, y_max, h))

    # Predict for entire grid
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Plot
    plt.figure(figsize=(10, 8))
    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
    cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

    plt.contourf(xx, yy, Z, alpha=0.4, cmap=cmap_light)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold, edgecolor='k', s=50)

    if test_point is not None:
        prediction = knn.predict(test_point.reshape(1, -1))[0]
        plt.scatter(test_point[0], test_point[1], c='yellow',
                   marker='*', s=300, edgecolor='k', linewidth=2,
                   label=f'Test point (pred={prediction})')

        # Show k nearest neighbors
        neighbor_indices, _ = knn._get_neighbors(test_point)
        neighbors = X[neighbor_indices]
        plt.scatter(neighbors[:, 0], neighbors[:, 1],
                   facecolors='none', edgecolors='orange',
                   s=100, linewidth=2, label=f'{k} nearest neighbors')

        # Draw lines to neighbors
        for neighbor in neighbors:
            plt.plot([test_point[0], neighbor[0]],
                    [test_point[1], neighbor[1]],
                    'orange', alpha=0.3, linewidth=1)

        plt.legend()

    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title(f'KNN Classification (k={k})')
    plt.grid(True, alpha=0.3)
    plt.show()


def example_classification():
    """Example: KNN for classification with iris-like data"""
    print("=" * 60)
    print("KNN Classification Example")
    print("=" * 60)

    # Generate synthetic classification data
    np.random.seed(42)
    n_samples = 150
    n_features = 2
    n_classes = 3

    # Create clustered data
    X = []
    y = []
    for class_id in range(n_classes):
        center = np.random.randn(n_features) * 2
        samples = np.random.randn(n_samples // n_classes, n_features) + center
        X.extend(samples)
        y.extend([class_id] * (n_samples // n_classes))

    X = np.array(X)
    y = np.array(y)

    # Shuffle data
    indices = np.random.permutation(n_samples)
    X = X[indices]
    y = y[indices]

    # Split data
    split_idx = int(0.8 * n_samples)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Train KNN with different k values
    k_values = [1, 3, 5, 9]
    for k in k_values:
        knn = KNN(k=k, task='classification')
        knn.fit(X_train, y_train)
        accuracy = knn.score(X_test, y_test)
        print(f"k={k}: Accuracy = {accuracy:.4f}")

    # Find optimal k
    print("\nFinding optimal k using cross-validation...")
    optimizer = KNNOptimizer(k_range=(1, 15), cv_folds=5)
    best_k = optimizer.find_best_k(X_train, y_train, task='classification')
    print(f"Best k found: {best_k}")
    optimizer.plot_elbow_curve()

    # Visualize classification
    test_point = X_test[0]
    visualize_knn_classification(X_train, y_train, k=best_k, test_point=test_point)


def example_regression():
    """Example: KNN for regression"""
    print("\n" + "=" * 60)
    print("KNN Regression Example")
    print("=" * 60)

    # Generate synthetic regression data
    np.random.seed(42)
    X = np.sort(5 * np.random.rand(100, 1), axis=0)
    y = np.sin(X).ravel()
    y += 0.1 * np.random.randn(100)

    # Split data
    split_idx = 80
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Try different k values
    k_values = [1, 3, 5, 10]
    plt.figure(figsize=(12, 8))

    for i, k in enumerate(k_values):
        knn = KNN(k=k, task='regression')
        knn.fit(X_train, y_train)

        # Create smooth line for predictions
        X_line = np.linspace(0, 5, 200).reshape(-1, 1)
        y_pred = knn.predict(X_line)

        # Calculate R² score
        r2_score = knn.score(X_test, y_test)

        # Plot
        plt.subplot(2, 2, i+1)
        plt.scatter(X_train, y_train, color='blue', alpha=0.5, label='Training')
        plt.scatter(X_test, y_test, color='red', alpha=0.5, label='Test')
        plt.plot(X_line, y_pred, color='green', linewidth=2, label='Prediction')
        plt.xlabel('X')
        plt.ylabel('y')
        plt.title(f'k={k}, R²={r2_score:.3f}')
        plt.legend()
        plt.grid(True, alpha=0.3)

    plt.suptitle('KNN Regression with Different k Values')
    plt.tight_layout()
    plt.show()


def example_distance_metrics():
    """Example: Effect of different distance metrics"""
    print("\n" + "=" * 60)
    print("Distance Metrics Comparison")
    print("=" * 60)

    # Generate data
    np.random.seed(42)
    X = np.random.randn(100, 5)  # 5D features
    y = (X[:, 0] + X[:, 1] > 0).astype(int)  # Simple linear boundary

    # Split data
    split_idx = 80
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Test different metrics
    metrics = ['euclidean', 'manhattan', 'minkowski', 'cosine']
    results = {}

    for metric in metrics:
        knn = KNN(k=5, metric=metric, task='classification')
        knn.fit(X_train, y_train)
        accuracy = knn.score(X_test, y_test)
        results[metric] = accuracy
        print(f"{metric.capitalize()} distance: Accuracy = {accuracy:.4f}")

    # Plot comparison
    plt.figure(figsize=(10, 6))
    metrics_list = list(results.keys())
    accuracies = list(results.values())

    plt.bar(metrics_list, accuracies, color=['blue', 'green', 'red', 'orange'])
    plt.xlabel('Distance Metric')
    plt.ylabel('Accuracy')
    plt.title('KNN Performance with Different Distance Metrics')
    plt.ylim([0, 1])
    plt.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for i, (metric, acc) in enumerate(results.items()):
        plt.text(i, acc + 0.01, f'{acc:.3f}', ha='center')

    plt.show()


if __name__ == "__main__":
    # Run examples
    example_classification()
    example_regression()
    example_distance_metrics()

    print("\n" + "=" * 60)
    print("KNN Implementation Complete!")
    print("=" * 60)