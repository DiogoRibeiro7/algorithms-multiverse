#!/usr/bin/env python3
"""
Decision Tree Algorithm Implementation

Decision Trees are supervised learning algorithms used for classification
and regression. They work by recursively splitting the data based on feature
values to create a tree-like model of decisions.

Key Concepts:
- Recursive binary splitting
- Information gain (entropy) or Gini impurity for splits
- Pruning to prevent overfitting
- Feature importance calculation

Time Complexity:
- Training: O(n * m * log(n)) average, O(n² * m) worst case
- Prediction: O(depth) where depth is tree depth
Space Complexity: O(nodes) for storing the tree

Applications:
- Classification and regression tasks
- Feature importance analysis
- Foundation for Random Forests and Gradient Boosting
- Interpretable machine learning

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import Optional, Union, List, Tuple, Dict
import matplotlib.pyplot as plt
from collections import Counter


class TreeNode:
    """
    Node in the decision tree

    Attributes:
        feature (int): Feature index for splitting
        threshold (float): Threshold value for splitting
        left (TreeNode): Left child (values <= threshold)
        right (TreeNode): Right child (values > threshold)
        value: Prediction value for leaf nodes
        samples (int): Number of samples at this node
        impurity (float): Node impurity (entropy or gini)
        depth (int): Depth of node in tree
    """

    def __init__(self, feature: Optional[int] = None,
                 threshold: Optional[float] = None,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None,
                 value: Optional[Union[int, float]] = None,
                 samples: int = 0,
                 impurity: float = 0.0,
                 depth: int = 0):
        """Initialize tree node"""
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        self.samples = samples
        self.impurity = impurity
        self.depth = depth

    def is_leaf(self) -> bool:
        """Check if node is a leaf"""
        return self.value is not None

    def __str__(self) -> str:
        """String representation of node"""
        if self.is_leaf():
            return f"Leaf(value={self.value}, samples={self.samples})"
        return f"Node(feature={self.feature}, threshold={self.threshold:.3f}, samples={self.samples})"


class DecisionTree:
    """
    Decision Tree for Classification and Regression

    Implements CART (Classification and Regression Trees) algorithm
    with support for different splitting criteria and pruning.

    Attributes:
        max_depth (int): Maximum depth of tree
        min_samples_split (int): Minimum samples to split a node
        min_samples_leaf (int): Minimum samples in a leaf
        criterion (str): Splitting criterion
        task (str): 'classification' or 'regression'
        root (TreeNode): Root node of the tree
        n_features (int): Number of features
        feature_importances_ (np.ndarray): Feature importance scores
    """

    def __init__(self, max_depth: Optional[int] = None,
                 min_samples_split: int = 2,
                 min_samples_leaf: int = 1,
                 criterion: str = 'gini',
                 task: str = 'classification',
                 max_features: Optional[Union[int, str]] = None,
                 random_state: Optional[int] = None):
        """
        Initialize Decision Tree

        Args:
            max_depth: Maximum tree depth (None for unlimited)
            min_samples_split: Minimum samples required to split
            min_samples_leaf: Minimum samples required in leaf
            criterion: 'gini', 'entropy' (classification) or 'mse', 'mae' (regression)
            task: 'classification' or 'regression'
            max_features: Number of features to consider for best split
            random_state: Random seed for reproducibility
        """
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.task = task
        self.max_features = max_features
        self.random_state = random_state
        self.root = None
        self.n_features = None
        self.feature_importances_ = None
        self.classes_ = None

        if random_state is not None:
            np.random.seed(random_state)

    def _gini_impurity(self, y: np.ndarray) -> float:
        """
        Calculate Gini impurity for classification

        Gini = 1 - Σ(p_i)²

        Args:
            y: Class labels

        Returns:
            Gini impurity value
        """
        if len(y) == 0:
            return 0

        counts = Counter(y)
        n = len(y)
        gini = 1.0

        for count in counts.values():
            prob = count / n
            gini -= prob ** 2

        return gini

    def _entropy(self, y: np.ndarray) -> float:
        """
        Calculate entropy for classification

        Entropy = -Σ(p_i * log2(p_i))

        Args:
            y: Class labels

        Returns:
            Entropy value
        """
        if len(y) == 0:
            return 0

        counts = Counter(y)
        n = len(y)
        entropy = 0

        for count in counts.values():
            if count > 0:
                prob = count / n
                entropy -= prob * np.log2(prob)

        return entropy

    def _mse(self, y: np.ndarray) -> float:
        """
        Calculate mean squared error for regression

        MSE = Σ(y_i - mean(y))² / n

        Args:
            y: Target values

        Returns:
            MSE value
        """
        if len(y) == 0:
            return 0
        mean = np.mean(y)
        return np.mean((y - mean) ** 2)

    def _mae(self, y: np.ndarray) -> float:
        """
        Calculate mean absolute error for regression

        MAE = Σ|y_i - median(y)| / n

        Args:
            y: Target values

        Returns:
            MAE value
        """
        if len(y) == 0:
            return 0
        median = np.median(y)
        return np.mean(np.abs(y - median))

    def _get_impurity_function(self):
        """Get the appropriate impurity function"""
        impurity_functions = {
            'gini': self._gini_impurity,
            'entropy': self._entropy,
            'mse': self._mse,
            'mae': self._mae
        }

        if self.criterion not in impurity_functions:
            raise ValueError(f"Unknown criterion: {self.criterion}")

        return impurity_functions[self.criterion]

    def _information_gain(self, parent_impurity: float,
                         left_y: np.ndarray,
                         right_y: np.ndarray) -> float:
        """
        Calculate information gain from a split

        IG = parent_impurity - weighted_avg(child_impurities)

        Args:
            parent_impurity: Impurity of parent node
            left_y: Left child labels/values
            right_y: Right child labels/values

        Returns:
            Information gain
        """
        n = len(left_y) + len(right_y)
        if n == 0:
            return 0

        impurity_func = self._get_impurity_function()

        # Calculate weighted average of child impurities
        left_weight = len(left_y) / n
        right_weight = len(right_y) / n

        left_impurity = impurity_func(left_y)
        right_impurity = impurity_func(right_y)

        weighted_impurity = (left_weight * left_impurity +
                           right_weight * right_impurity)

        return parent_impurity - weighted_impurity

    def _get_feature_subset(self, n_features: int) -> np.ndarray:
        """
        Get subset of features to consider for splitting

        Args:
            n_features: Total number of features

        Returns:
            Array of feature indices
        """
        if self.max_features is None:
            return np.arange(n_features)

        if isinstance(self.max_features, int):
            n_select = min(self.max_features, n_features)
        elif self.max_features == 'sqrt':
            n_select = int(np.sqrt(n_features))
        elif self.max_features == 'log2':
            n_select = int(np.log2(n_features)) + 1
        else:
            return np.arange(n_features)

        return np.random.choice(n_features, n_select, replace=False)

    def _find_best_split(self, X: np.ndarray, y: np.ndarray) -> Tuple[int, float, float]:
        """
        Find the best feature and threshold to split on

        Args:
            X: Feature matrix
            y: Labels/values

        Returns:
            Tuple of (best_feature, best_threshold, best_gain)
        """
        best_feature = None
        best_threshold = None
        best_gain = -np.inf

        impurity_func = self._get_impurity_function()
        parent_impurity = impurity_func(y)

        # Consider subset of features
        features_to_try = self._get_feature_subset(X.shape[1])

        for feature_idx in features_to_try:
            feature_values = X[:, feature_idx]
            thresholds = np.unique(feature_values)

            for threshold in thresholds:
                # Split data
                left_mask = feature_values <= threshold
                right_mask = ~left_mask

                left_y = y[left_mask]
                right_y = y[right_mask]

                # Check minimum samples in leaves
                if (len(left_y) < self.min_samples_leaf or
                    len(right_y) < self.min_samples_leaf):
                    continue

                # Calculate information gain
                gain = self._information_gain(parent_impurity, left_y, right_y)

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature_idx
                    best_threshold = threshold

        return best_feature, best_threshold, best_gain

    def _build_tree(self, X: np.ndarray, y: np.ndarray,
                   depth: int = 0) -> TreeNode:
        """
        Recursively build the decision tree

        Args:
            X: Feature matrix
            y: Labels/values
            depth: Current depth in tree

        Returns:
            Root node of subtree
        """
        n_samples = len(y)
        impurity_func = self._get_impurity_function()
        node_impurity = impurity_func(y)

        # Create node
        node = TreeNode(samples=n_samples, impurity=node_impurity, depth=depth)

        # Check stopping criteria
        if (self.max_depth is not None and depth >= self.max_depth) or \
           (n_samples < self.min_samples_split) or \
           (len(np.unique(y)) == 1):
            # Create leaf node
            if self.task == 'classification':
                node.value = Counter(y).most_common(1)[0][0]
            else:
                node.value = np.mean(y)
            return node

        # Find best split
        best_feature, best_threshold, best_gain = self._find_best_split(X, y)

        if best_feature is None or best_gain <= 0:
            # No good split found, create leaf
            if self.task == 'classification':
                node.value = Counter(y).most_common(1)[0][0]
            else:
                node.value = np.mean(y)
            return node

        # Split data
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask

        # Store split information
        node.feature = best_feature
        node.threshold = best_threshold

        # Update feature importance
        self.feature_importances_[best_feature] += (
            best_gain * n_samples / self.n_samples_
        )

        # Recursively build child nodes
        node.left = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        node.right = self._build_tree(X[right_mask], y[right_mask], depth + 1)

        return node

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'DecisionTree':
        """
        Train the decision tree

        Args:
            X: Training features (n_samples x n_features)
            y: Training labels/values (n_samples,)

        Returns:
            Self (for method chaining)
        """
        self.n_features = X.shape[1]
        self.n_samples_ = X.shape[0]
        self.feature_importances_ = np.zeros(self.n_features)

        if self.task == 'classification':
            self.classes_ = np.unique(y)

        # Build tree
        self.root = self._build_tree(X, y)

        # Normalize feature importances
        if np.sum(self.feature_importances_) > 0:
            self.feature_importances_ /= np.sum(self.feature_importances_)

        return self

    def _predict_sample(self, x: np.ndarray, node: TreeNode) -> Union[int, float]:
        """
        Predict for a single sample

        Args:
            x: Feature vector
            node: Current node in tree

        Returns:
            Prediction
        """
        if node.is_leaf():
            return node.value

        if x[node.feature] <= node.threshold:
            return self._predict_sample(x, node.left)
        else:
            return self._predict_sample(x, node.right)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions for multiple samples

        Args:
            X: Feature matrix (n_samples x n_features)

        Returns:
            Predictions (n_samples,)
        """
        if self.root is None:
            raise ValueError("Tree must be fitted before prediction")

        predictions = []
        for x in X:
            pred = self._predict_sample(x, self.root)
            predictions.append(pred)

        return np.array(predictions)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities (classification only)

        Args:
            X: Feature matrix

        Returns:
            Class probabilities (n_samples x n_classes)
        """
        if self.task != 'classification':
            raise ValueError("predict_proba only works for classification")

        # For simplicity, return one-hot encoded predictions
        # A more sophisticated implementation would track class distributions in leaves
        predictions = self.predict(X)
        n_samples = X.shape[0]
        n_classes = len(self.classes_)
        proba = np.zeros((n_samples, n_classes))

        for i, pred in enumerate(predictions):
            class_idx = np.where(self.classes_ == pred)[0][0]
            proba[i, class_idx] = 1.0

        return proba

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate accuracy (classification) or R² (regression)

        Args:
            X: Feature matrix
            y: True labels/values

        Returns:
            Score
        """
        predictions = self.predict(X)

        if self.task == 'classification':
            return np.mean(predictions == y)
        else:
            ss_res = np.sum((y - predictions) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            return 1 - (ss_res / ss_tot)

    def get_depth(self, node: Optional[TreeNode] = None) -> int:
        """
        Get the depth of the tree

        Args:
            node: Starting node (default: root)

        Returns:
            Maximum depth
        """
        if node is None:
            node = self.root

        if node is None or node.is_leaf():
            return 0

        return 1 + max(self.get_depth(node.left), self.get_depth(node.right))

    def get_n_leaves(self, node: Optional[TreeNode] = None) -> int:
        """
        Count the number of leaves in the tree

        Args:
            node: Starting node (default: root)

        Returns:
            Number of leaves
        """
        if node is None:
            node = self.root

        if node is None:
            return 0

        if node.is_leaf():
            return 1

        return self.get_n_leaves(node.left) + self.get_n_leaves(node.right)

    def print_tree(self, node: Optional[TreeNode] = None,
                  depth: int = 0, prefix: str = ""):
        """
        Print text representation of the tree

        Args:
            node: Starting node
            depth: Current depth
            prefix: Prefix for printing
        """
        if node is None:
            node = self.root

        if node is None:
            return

        if node.is_leaf():
            print(f"{prefix}Predict: {node.value} (samples={node.samples})")
        else:
            print(f"{prefix}Feature_{node.feature} <= {node.threshold:.3f}?")
            print(f"{prefix}├─ True:")
            self.print_tree(node.left, depth + 1, prefix + "│  ")
            print(f"{prefix}└─ False:")
            self.print_tree(node.right, depth + 1, prefix + "   ")


def plot_feature_importances(tree: DecisionTree, feature_names: Optional[List[str]] = None):
    """
    Plot feature importances

    Args:
        tree: Trained decision tree
        feature_names: Optional names for features
    """
    if tree.feature_importances_ is None:
        print("Tree must be fitted first")
        return

    n_features = len(tree.feature_importances_)
    if feature_names is None:
        feature_names = [f"Feature {i}" for i in range(n_features)]

    # Sort by importance
    indices = np.argsort(tree.feature_importances_)[::-1]

    plt.figure(figsize=(10, 6))
    plt.title("Feature Importances")
    plt.bar(range(n_features), tree.feature_importances_[indices])
    plt.xticks(range(n_features), [feature_names[i] for i in indices], rotation=45)
    plt.xlabel("Feature")
    plt.ylabel("Importance")
    plt.tight_layout()
    plt.show()


def visualize_tree_boundary(tree: DecisionTree, X: np.ndarray, y: np.ndarray,
                           feature_names: Optional[List[str]] = None):
    """
    Visualize decision boundary for 2D features

    Args:
        tree: Trained decision tree
        X: Feature matrix (must be 2D)
        y: Labels
        feature_names: Optional feature names
    """
    if X.shape[1] != 2:
        print("Visualization only works for 2D features")
        return

    # Create mesh grid
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                        np.arange(y_min, y_max, h))

    # Predict for grid
    Z = tree.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Plot
    plt.figure(figsize=(10, 8))
    plt.contourf(xx, yy, Z, alpha=0.4, cmap='viridis')

    # Plot training points
    scatter = plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis',
                         edgecolor='black', s=50)
    plt.colorbar(scatter)

    if feature_names:
        plt.xlabel(feature_names[0])
        plt.ylabel(feature_names[1])
    else:
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')

    plt.title(f'Decision Tree Boundary (depth={tree.get_depth()})')
    plt.grid(True, alpha=0.3)
    plt.show()


def example_classification():
    """Example: Decision tree for classification"""
    print("=" * 60)
    print("Decision Tree Classification Example")
    print("=" * 60)

    # Generate synthetic data
    np.random.seed(42)
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=200, n_features=2, n_informative=2,
                              n_redundant=0, n_clusters_per_class=2,
                              random_state=42)

    # Split data
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Train trees with different max_depth
    depths = [1, 3, 5, None]
    for depth in depths:
        tree = DecisionTree(max_depth=depth, criterion='entropy',
                          task='classification')
        tree.fit(X_train, y_train)
        accuracy = tree.score(X_test, y_test)
        n_leaves = tree.get_n_leaves()
        print(f"Max depth={depth}: Accuracy={accuracy:.4f}, Leaves={n_leaves}")

    # Visualize best tree
    best_tree = DecisionTree(max_depth=3, criterion='entropy',
                            task='classification')
    best_tree.fit(X_train, y_train)

    print("\nTree structure:")
    best_tree.print_tree()

    visualize_tree_boundary(best_tree, X_train, y_train)
    plot_feature_importances(best_tree)


def example_regression():
    """Example: Decision tree for regression"""
    print("\n" + "=" * 60)
    print("Decision Tree Regression Example")
    print("=" * 60)

    # Generate synthetic regression data
    np.random.seed(42)
    X = np.sort(5 * np.random.rand(100, 1), axis=0)
    y = np.sin(X).ravel()
    y[::5] += 0.5 * (0.5 - np.random.rand(20))  # Add noise

    # Train trees with different max_depth
    depths = [2, 5, 10]
    plt.figure(figsize=(12, 4))

    for i, depth in enumerate(depths):
        tree = DecisionTree(max_depth=depth, criterion='mse',
                          task='regression')
        tree.fit(X, y)

        # Predict on dense grid
        X_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
        y_pred = tree.predict(X_test)

        plt.subplot(1, 3, i+1)
        plt.scatter(X, y, s=20, edgecolor="black", c="darkorange", label="data")
        plt.plot(X_test, y_pred, color="cornflowerblue",
                label=f"max_depth={depth}", linewidth=2)
        plt.xlabel("X")
        plt.ylabel("y")
        plt.title(f"Depth {depth}, Leaves: {tree.get_n_leaves()}")
        plt.legend()

    plt.suptitle("Decision Tree Regression with Different Depths")
    plt.tight_layout()
    plt.show()


def example_overfitting():
    """Example: Demonstrating overfitting with decision trees"""
    print("\n" + "=" * 60)
    print("Overfitting in Decision Trees")
    print("=" * 60)

    # Generate data with noise
    np.random.seed(42)
    n_samples = 100
    X = np.random.rand(n_samples, 2) * 10
    y = (X[:, 0] + X[:, 1] > 10).astype(int)
    # Add noise
    noise_indices = np.random.choice(n_samples, 10, replace=False)
    y[noise_indices] = 1 - y[noise_indices]

    # Split data
    split_idx = int(0.7 * n_samples)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Train with different parameters
    params = [
        {'max_depth': 2, 'min_samples_split': 10},
        {'max_depth': 5, 'min_samples_split': 5},
        {'max_depth': None, 'min_samples_split': 2}
    ]

    results = []
    for param in params:
        tree = DecisionTree(**param, task='classification')
        tree.fit(X_train, y_train)

        train_acc = tree.score(X_train, y_train)
        test_acc = tree.score(X_test, y_test)

        results.append({
            'params': param,
            'train_acc': train_acc,
            'test_acc': test_acc,
            'depth': tree.get_depth(),
            'leaves': tree.get_n_leaves()
        })

        print(f"Params: {param}")
        print(f"  Train Accuracy: {train_acc:.4f}")
        print(f"  Test Accuracy: {test_acc:.4f}")
        print(f"  Tree Depth: {tree.get_depth()}")
        print(f"  Number of Leaves: {tree.get_n_leaves()}")
        print()

    # Plot overfitting comparison
    plt.figure(figsize=(10, 6))
    x_pos = np.arange(len(params))
    width = 0.35

    train_accs = [r['train_acc'] for r in results]
    test_accs = [r['test_acc'] for r in results]

    plt.bar(x_pos - width/2, train_accs, width, label='Train Accuracy',
           color='blue', alpha=0.7)
    plt.bar(x_pos + width/2, test_accs, width, label='Test Accuracy',
           color='red', alpha=0.7)

    plt.xlabel('Model Complexity')
    plt.ylabel('Accuracy')
    plt.title('Overfitting in Decision Trees')
    plt.xticks(x_pos, ['Simple\n(depth=2)', 'Medium\n(depth=5)',
                       'Complex\n(unlimited)'])
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Run examples
    example_classification()
    example_regression()
    example_overfitting()

    print("\n" + "=" * 60)
    print("Decision Tree Implementation Complete!")
    print("=" * 60)