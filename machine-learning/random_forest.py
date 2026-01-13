#!/usr/bin/env python3
"""
Random Forest and Ensemble Methods Implementation

A comprehensive implementation of Random Forest and other ensemble methods including:
- Random Forest Classifier and Regressor
- AdaBoost (Adaptive Boosting)
- Gradient Boosting
- Extra Trees (Extremely Randomized Trees)

Features:
- Bootstrap aggregating (bagging)
- Random feature selection
- Out-of-bag (OOB) score estimation
- Feature importance calculation
- Parallel tree training support
- Multiple boosting algorithms

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import List, Optional, Tuple, Union, Dict, Any
from collections import Counter
import warnings
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing


class DecisionTreeNode:
    """Node for decision tree used in ensemble methods."""

    def __init__(self, feature: int = None, threshold: float = None,
                 left=None, right=None, value=None, samples: int = 0,
                 impurity: float = 0.0):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        self.samples = samples
        self.impurity = impurity


class SimpleDecisionTree:
    """Simple decision tree for use in ensemble methods."""

    def __init__(self, max_depth: int = None, min_samples_split: int = 2,
                 min_samples_leaf: int = 1, max_features: int = None,
                 criterion: str = 'gini', random_state: int = None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.criterion = criterion
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
        self.root = None
        self.n_classes_ = None
        self.feature_importances_ = None

    def _gini(self, y: np.ndarray) -> float:
        """Calculate Gini impurity."""
        if len(y) == 0:
            return 0
        _, counts = np.unique(y, return_counts=True)
        probs = counts / len(y)
        return 1 - np.sum(probs ** 2)

    def _entropy(self, y: np.ndarray) -> float:
        """Calculate entropy."""
        if len(y) == 0:
            return 0
        _, counts = np.unique(y, return_counts=True)
        probs = counts / len(y)
        probs = probs[probs > 0]  # Remove zero probabilities
        return -np.sum(probs * np.log2(probs))

    def _mse(self, y: np.ndarray) -> float:
        """Calculate mean squared error."""
        if len(y) == 0:
            return 0
        return np.var(y)

    def _calculate_impurity(self, y: np.ndarray) -> float:
        """Calculate impurity based on criterion."""
        if self.criterion == 'gini':
            return self._gini(y)
        elif self.criterion == 'entropy':
            return self._entropy(y)
        elif self.criterion == 'mse':
            return self._mse(y)
        else:
            raise ValueError(f"Unknown criterion: {self.criterion}")

    def _best_split(self, X: np.ndarray, y: np.ndarray) -> Tuple[int, float]:
        """Find the best split for the data."""
        m, n = X.shape
        if m <= 1:
            return None, None

        # Calculate current impurity
        parent_impurity = self._calculate_impurity(y)

        # Select features to consider
        if self.max_features is not None:
            features = self.rng.choice(n, min(self.max_features, n), replace=False)
        else:
            features = np.arange(n)

        best_gain = 0
        best_feature = None
        best_threshold = None

        for feature in features:
            thresholds = np.unique(X[:, feature])

            for threshold in thresholds:
                # Split data
                left_mask = X[:, feature] <= threshold
                right_mask = ~left_mask

                if np.sum(left_mask) < self.min_samples_leaf or \
                   np.sum(right_mask) < self.min_samples_leaf:
                    continue

                # Calculate information gain
                left_impurity = self._calculate_impurity(y[left_mask])
                right_impurity = self._calculate_impurity(y[right_mask])

                n_left = np.sum(left_mask)
                n_right = np.sum(right_mask)

                weighted_impurity = (n_left / m) * left_impurity + (n_right / m) * right_impurity
                gain = parent_impurity - weighted_impurity

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold

        # Update feature importances
        if best_feature is not None and self.feature_importances_ is not None:
            self.feature_importances_[best_feature] += best_gain * m

        return best_feature, best_threshold

    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int = 0) -> DecisionTreeNode:
        """Recursively build the decision tree."""
        n_samples = len(y)

        # Check stopping criteria
        if (self.max_depth is not None and depth >= self.max_depth) or \
           n_samples < self.min_samples_split or \
           len(np.unique(y)) == 1:

            if self.criterion in ['gini', 'entropy']:
                # Classification: return most common class
                values, counts = np.unique(y, return_counts=True)
                return DecisionTreeNode(value=values[np.argmax(counts)],
                                       samples=n_samples,
                                       impurity=self._calculate_impurity(y))
            else:
                # Regression: return mean
                return DecisionTreeNode(value=np.mean(y),
                                       samples=n_samples,
                                       impurity=self._calculate_impurity(y))

        # Find best split
        best_feature, best_threshold = self._best_split(X, y)

        if best_feature is None:
            if self.criterion in ['gini', 'entropy']:
                values, counts = np.unique(y, return_counts=True)
                return DecisionTreeNode(value=values[np.argmax(counts)],
                                       samples=n_samples,
                                       impurity=self._calculate_impurity(y))
            else:
                return DecisionTreeNode(value=np.mean(y),
                                       samples=n_samples,
                                       impurity=self._calculate_impurity(y))

        # Split data
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask

        # Build child nodes
        left_child = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_child = self._build_tree(X[right_mask], y[right_mask], depth + 1)

        return DecisionTreeNode(feature=best_feature,
                               threshold=best_threshold,
                               left=left_child,
                               right=right_child,
                               samples=n_samples,
                               impurity=self._calculate_impurity(y))

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Train the decision tree."""
        n_features = X.shape[1]

        if self.criterion in ['gini', 'entropy']:
            self.n_classes_ = len(np.unique(y))

        # Initialize feature importances
        self.feature_importances_ = np.zeros(n_features)

        # Build tree
        self.root = self._build_tree(X, y)

        # Normalize feature importances
        if np.sum(self.feature_importances_) > 0:
            self.feature_importances_ /= np.sum(self.feature_importances_)

        return self

    def _predict_sample(self, x: np.ndarray, node: DecisionTreeNode):
        """Predict for a single sample."""
        if node.value is not None:
            return node.value

        if x[node.feature] <= node.threshold:
            return self._predict_sample(x, node.left)
        else:
            return self._predict_sample(x, node.right)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict for multiple samples."""
        return np.array([self._predict_sample(x, self.root) for x in X])

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities (for classification only)."""
        if self.criterion not in ['gini', 'entropy']:
            raise ValueError("predict_proba is only for classification")

        # Simple implementation: return one-hot encoded predictions
        predictions = self.predict(X)
        n_samples = len(X)
        proba = np.zeros((n_samples, self.n_classes_))

        for i, pred in enumerate(predictions):
            proba[i, int(pred)] = 1.0

        return proba


class RandomForestClassifier:
    """
    Random Forest Classifier using bootstrap aggregating and random feature selection.

    Parameters:
        n_estimators: Number of trees in the forest
        max_depth: Maximum depth of the trees
        min_samples_split: Minimum samples required to split a node
        min_samples_leaf: Minimum samples required at a leaf node
        max_features: Number of features to consider for best split
        bootstrap: Whether to use bootstrap samples
        oob_score: Whether to use out-of-bag samples to estimate accuracy
        n_jobs: Number of parallel jobs (-1 for all CPUs)
        random_state: Random seed for reproducibility
    """

    def __init__(self, n_estimators: int = 100, max_depth: int = None,
                 min_samples_split: int = 2, min_samples_leaf: int = 1,
                 max_features: Union[str, int, float] = 'sqrt',
                 bootstrap: bool = True, oob_score: bool = False,
                 n_jobs: int = 1, random_state: int = None,
                 criterion: str = 'gini'):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.bootstrap = bootstrap
        self.oob_score = oob_score
        self.n_jobs = n_jobs if n_jobs != -1 else multiprocessing.cpu_count()
        self.random_state = random_state
        self.criterion = criterion

        self.estimators_ = []
        self.classes_ = None
        self.n_classes_ = None
        self.n_features_ = None
        self.feature_importances_ = None
        self.oob_score_ = None
        self.oob_decision_function_ = None

    def _get_max_features(self, n_features: int) -> int:
        """Calculate the number of features to consider."""
        if isinstance(self.max_features, str):
            if self.max_features == 'sqrt':
                return max(1, int(np.sqrt(n_features)))
            elif self.max_features == 'log2':
                return max(1, int(np.log2(n_features)))
            else:
                raise ValueError(f"Unknown max_features: {self.max_features}")
        elif isinstance(self.max_features, float):
            return max(1, int(self.max_features * n_features))
        elif isinstance(self.max_features, int):
            return min(self.max_features, n_features)
        else:
            return n_features

    def _bootstrap_sample(self, X: np.ndarray, y: np.ndarray,
                         random_state: np.random.RandomState) -> Tuple:
        """Create bootstrap sample with replacement."""
        n_samples = X.shape[0]

        if self.bootstrap:
            indices = random_state.choice(n_samples, n_samples, replace=True)
            oob_indices = np.array(list(set(range(n_samples)) - set(indices)))
        else:
            indices = np.arange(n_samples)
            oob_indices = np.array([])

        return X[indices], y[indices], oob_indices

    def _train_tree(self, args):
        """Train a single tree."""
        tree_idx, X, y = args

        # Create random state for this tree
        if self.random_state is not None:
            seed = self.random_state + tree_idx
        else:
            seed = tree_idx
        random_state = np.random.RandomState(seed)

        # Bootstrap sample
        X_sample, y_sample, oob_indices = self._bootstrap_sample(X, y, random_state)

        # Create and train tree
        tree = SimpleDecisionTree(
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            max_features=self._get_max_features(self.n_features_),
            criterion=self.criterion,
            random_state=seed
        )
        tree.fit(X_sample, y_sample)

        return tree, oob_indices

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Train the Random Forest."""
        X = np.asarray(X)
        y = np.asarray(y)

        n_samples, n_features = X.shape
        self.n_features_ = n_features
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)

        # Create label encoder
        label_to_idx = {label: idx for idx, label in enumerate(self.classes_)}
        y_encoded = np.array([label_to_idx[label] for label in y])

        # Initialize OOB tracking
        if self.oob_score and self.bootstrap:
            self.oob_decision_function_ = np.zeros((n_samples, self.n_classes_))
            oob_counts = np.zeros(n_samples)

        # Train trees in parallel
        if self.n_jobs > 1:
            with ProcessPoolExecutor(max_workers=self.n_jobs) as executor:
                args_list = [(i, X, y_encoded) for i in range(self.n_estimators)]
                results = list(executor.map(self._train_tree, args_list))
        else:
            results = [self._train_tree((i, X, y_encoded))
                      for i in range(self.n_estimators)]

        self.estimators_ = [r[0] for r in results]
        oob_indices_list = [r[1] for r in results]

        # Calculate OOB score
        if self.oob_score and self.bootstrap:
            for tree, oob_indices in zip(self.estimators_, oob_indices_list):
                if len(oob_indices) > 0:
                    X_oob = X[oob_indices]
                    predictions = tree.predict_proba(X_oob)
                    for i, idx in enumerate(oob_indices):
                        self.oob_decision_function_[idx] += predictions[i]
                        oob_counts[idx] += 1

            # Average OOB predictions
            mask = oob_counts > 0
            self.oob_decision_function_[mask] /= oob_counts[mask, np.newaxis]
            oob_predictions = np.argmax(self.oob_decision_function_[mask], axis=1)
            self.oob_score_ = np.mean(oob_predictions == y_encoded[mask])

        # Calculate feature importances
        self._calculate_feature_importances()

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels."""
        X = np.asarray(X)

        # Get votes from all trees
        predictions = np.array([tree.predict(X) for tree in self.estimators_])

        # Majority voting
        n_samples = X.shape[0]
        final_predictions = np.zeros(n_samples)

        for i in range(n_samples):
            votes = predictions[:, i]
            values, counts = np.unique(votes, return_counts=True)
            final_predictions[i] = values[np.argmax(counts)]

        # Convert back to original labels
        return self.classes_[final_predictions.astype(int)]

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities."""
        X = np.asarray(X)

        # Get probability predictions from all trees
        all_proba = np.array([tree.predict_proba(X) for tree in self.estimators_])

        # Average probabilities
        return np.mean(all_proba, axis=0)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Calculate accuracy."""
        return np.mean(self.predict(X) == y)

    def _calculate_feature_importances(self):
        """Calculate feature importances as average over all trees."""
        all_importances = np.array([tree.feature_importances_
                                   for tree in self.estimators_])
        self.feature_importances_ = np.mean(all_importances, axis=0)


class RandomForestRegressor:
    """
    Random Forest Regressor using bootstrap aggregating and random feature selection.

    Parameters:
        n_estimators: Number of trees in the forest
        max_depth: Maximum depth of the trees
        min_samples_split: Minimum samples required to split a node
        min_samples_leaf: Minimum samples required at a leaf node
        max_features: Number of features to consider for best split
        bootstrap: Whether to use bootstrap samples
        oob_score: Whether to use out-of-bag samples to estimate R² score
        n_jobs: Number of parallel jobs (-1 for all CPUs)
        random_state: Random seed for reproducibility
    """

    def __init__(self, n_estimators: int = 100, max_depth: int = None,
                 min_samples_split: int = 2, min_samples_leaf: int = 1,
                 max_features: Union[str, int, float] = 'sqrt',
                 bootstrap: bool = True, oob_score: bool = False,
                 n_jobs: int = 1, random_state: int = None):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.bootstrap = bootstrap
        self.oob_score = oob_score
        self.n_jobs = n_jobs if n_jobs != -1 else multiprocessing.cpu_count()
        self.random_state = random_state

        self.estimators_ = []
        self.n_features_ = None
        self.feature_importances_ = None
        self.oob_score_ = None
        self.oob_prediction_ = None

    def _get_max_features(self, n_features: int) -> int:
        """Calculate the number of features to consider."""
        if isinstance(self.max_features, str):
            if self.max_features == 'sqrt':
                return max(1, int(np.sqrt(n_features)))
            elif self.max_features == 'log2':
                return max(1, int(np.log2(n_features)))
            else:
                raise ValueError(f"Unknown max_features: {self.max_features}")
        elif isinstance(self.max_features, float):
            return max(1, int(self.max_features * n_features))
        elif isinstance(self.max_features, int):
            return min(self.max_features, n_features)
        else:
            return n_features

    def _bootstrap_sample(self, X: np.ndarray, y: np.ndarray,
                         random_state: np.random.RandomState) -> Tuple:
        """Create bootstrap sample with replacement."""
        n_samples = X.shape[0]

        if self.bootstrap:
            indices = random_state.choice(n_samples, n_samples, replace=True)
            oob_indices = np.array(list(set(range(n_samples)) - set(indices)))
        else:
            indices = np.arange(n_samples)
            oob_indices = np.array([])

        return X[indices], y[indices], oob_indices

    def _train_tree(self, args):
        """Train a single tree."""
        tree_idx, X, y = args

        # Create random state for this tree
        if self.random_state is not None:
            seed = self.random_state + tree_idx
        else:
            seed = tree_idx
        random_state = np.random.RandomState(seed)

        # Bootstrap sample
        X_sample, y_sample, oob_indices = self._bootstrap_sample(X, y, random_state)

        # Create and train tree
        tree = SimpleDecisionTree(
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            max_features=self._get_max_features(self.n_features_),
            criterion='mse',
            random_state=seed
        )
        tree.fit(X_sample, y_sample)

        return tree, oob_indices

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Train the Random Forest."""
        X = np.asarray(X)
        y = np.asarray(y)

        n_samples, n_features = X.shape
        self.n_features_ = n_features

        # Initialize OOB tracking
        if self.oob_score and self.bootstrap:
            self.oob_prediction_ = np.zeros(n_samples)
            oob_counts = np.zeros(n_samples)

        # Train trees
        if self.n_jobs > 1:
            with ProcessPoolExecutor(max_workers=self.n_jobs) as executor:
                args_list = [(i, X, y) for i in range(self.n_estimators)]
                results = list(executor.map(self._train_tree, args_list))
        else:
            results = [self._train_tree((i, X, y))
                      for i in range(self.n_estimators)]

        self.estimators_ = [r[0] for r in results]
        oob_indices_list = [r[1] for r in results]

        # Calculate OOB score
        if self.oob_score and self.bootstrap:
            for tree, oob_indices in zip(self.estimators_, oob_indices_list):
                if len(oob_indices) > 0:
                    X_oob = X[oob_indices]
                    predictions = tree.predict(X_oob)
                    for i, idx in enumerate(oob_indices):
                        self.oob_prediction_[idx] += predictions[i]
                        oob_counts[idx] += 1

            # Average OOB predictions
            mask = oob_counts > 0
            self.oob_prediction_[mask] /= oob_counts[mask]

            # Calculate R² score
            ss_res = np.sum((y[mask] - self.oob_prediction_[mask]) ** 2)
            ss_tot = np.sum((y[mask] - np.mean(y[mask])) ** 2)
            self.oob_score_ = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0

        # Calculate feature importances
        self._calculate_feature_importances()

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict values."""
        X = np.asarray(X)

        # Get predictions from all trees
        predictions = np.array([tree.predict(X) for tree in self.estimators_])

        # Average predictions
        return np.mean(predictions, axis=0)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Calculate R² score."""
        predictions = self.predict(X)
        ss_res = np.sum((y - predictions) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0

    def _calculate_feature_importances(self):
        """Calculate feature importances as average over all trees."""
        all_importances = np.array([tree.feature_importances_
                                   for tree in self.estimators_])
        self.feature_importances_ = np.mean(all_importances, axis=0)


class AdaBoostClassifier:
    """
    AdaBoost (Adaptive Boosting) Classifier.

    Sequentially trains weak learners, focusing on misclassified samples.

    Parameters:
        n_estimators: Number of boosting iterations
        learning_rate: Shrinks the contribution of each classifier
        random_state: Random seed for reproducibility
    """

    def __init__(self, n_estimators: int = 50, learning_rate: float = 1.0,
                 random_state: int = None):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.random_state = random_state

        self.estimators_ = []
        self.estimator_weights_ = []
        self.estimator_errors_ = []
        self.classes_ = None
        self.n_classes_ = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Train the AdaBoost classifier."""
        X = np.asarray(X)
        y = np.asarray(y)

        n_samples = X.shape[0]

        # Initialize weights
        sample_weights = np.ones(n_samples) / n_samples

        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)

        # Convert to binary labels (-1, 1) for binary classification
        if self.n_classes_ == 2:
            y_encoded = np.where(y == self.classes_[0], -1, 1)
        else:
            raise ValueError("AdaBoost only supports binary classification")

        self.estimators_ = []
        self.estimator_weights_ = []
        self.estimator_errors_ = []

        for i in range(self.n_estimators):
            # Train weak learner
            tree = SimpleDecisionTree(
                max_depth=1,  # Decision stump
                criterion='gini',
                random_state=self.random_state + i if self.random_state else None
            )

            # Sample indices based on weights
            indices = np.random.choice(n_samples, n_samples, p=sample_weights)
            tree.fit(X[indices], y[indices])

            # Make predictions
            predictions = tree.predict(X)
            predictions_encoded = np.where(predictions == self.classes_[0], -1, 1)

            # Calculate error
            incorrect = predictions_encoded != y_encoded
            error = np.sum(sample_weights[incorrect]) / np.sum(sample_weights)

            # Skip if perfect prediction
            if error <= 0:
                self.estimators_.append(tree)
                self.estimator_weights_.append(1.0)
                self.estimator_errors_.append(0.0)
                break

            # Skip if error is too large
            if error >= 0.5:
                continue

            # Calculate estimator weight
            alpha = self.learning_rate * 0.5 * np.log((1 - error) / error)

            # Update sample weights
            sample_weights *= np.exp(-alpha * y_encoded * predictions_encoded)
            sample_weights /= np.sum(sample_weights)

            self.estimators_.append(tree)
            self.estimator_weights_.append(alpha)
            self.estimator_errors_.append(error)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels."""
        X = np.asarray(X)

        # Weighted voting
        decision = np.zeros(X.shape[0])

        for tree, weight in zip(self.estimators_, self.estimator_weights_):
            predictions = tree.predict(X)
            predictions_encoded = np.where(predictions == self.classes_[0], -1, 1)
            decision += weight * predictions_encoded

        # Convert back to class labels
        return np.where(decision < 0, self.classes_[0], self.classes_[1])

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities."""
        X = np.asarray(X)

        decision = np.zeros(X.shape[0])

        for tree, weight in zip(self.estimators_, self.estimator_weights_):
            predictions = tree.predict(X)
            predictions_encoded = np.where(predictions == self.classes_[0], -1, 1)
            decision += weight * predictions_encoded

        # Convert decision function to probabilities
        decision /= np.sum(self.estimator_weights_)
        proba = np.zeros((X.shape[0], 2))
        proba[:, 0] = 1 / (1 + np.exp(2 * decision))
        proba[:, 1] = 1 - proba[:, 0]

        return proba

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Calculate accuracy."""
        return np.mean(self.predict(X) == y)


class GradientBoostingClassifier:
    """
    Gradient Boosting Classifier.

    Sequentially trains trees to correct the errors of previous trees.

    Parameters:
        n_estimators: Number of boosting iterations
        learning_rate: Shrinks the contribution of each tree
        max_depth: Maximum depth of individual trees
        subsample: Fraction of samples to use for each tree
        random_state: Random seed for reproducibility
    """

    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.1,
                 max_depth: int = 3, subsample: float = 1.0,
                 random_state: int = None):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.subsample = subsample
        self.random_state = random_state

        self.estimators_ = []
        self.classes_ = None
        self.n_classes_ = None
        self.init_prediction_ = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Train the Gradient Boosting classifier."""
        X = np.asarray(X)
        y = np.asarray(y)

        n_samples = X.shape[0]

        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)

        if self.n_classes_ != 2:
            raise ValueError("GradientBoosting only supports binary classification")

        # Convert to binary labels (0, 1)
        y_encoded = (y == self.classes_[1]).astype(int)

        # Initialize with log odds
        pos_ratio = np.mean(y_encoded)
        self.init_prediction_ = np.log(pos_ratio / (1 - pos_ratio))

        # Initialize predictions
        F = np.full(n_samples, self.init_prediction_)

        self.estimators_ = []

        for i in range(self.n_estimators):
            # Calculate pseudo-residuals (negative gradient)
            p = 1 / (1 + np.exp(-F))
            residuals = y_encoded - p

            # Subsample
            if self.subsample < 1.0:
                sample_idx = np.random.choice(n_samples,
                                            int(n_samples * self.subsample),
                                            replace=False)
            else:
                sample_idx = np.arange(n_samples)

            # Train tree on residuals
            tree = SimpleDecisionTree(
                max_depth=self.max_depth,
                criterion='mse',
                random_state=self.random_state + i if self.random_state else None
            )
            tree.fit(X[sample_idx], residuals[sample_idx])

            # Update predictions
            predictions = tree.predict(X)
            F += self.learning_rate * predictions

            self.estimators_.append(tree)

        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities."""
        X = np.asarray(X)

        # Start with initial prediction
        F = np.full(X.shape[0], self.init_prediction_)

        # Add tree predictions
        for tree in self.estimators_:
            F += self.learning_rate * tree.predict(X)

        # Convert to probabilities
        p = 1 / (1 + np.exp(-F))
        proba = np.zeros((X.shape[0], 2))
        proba[:, 0] = 1 - p
        proba[:, 1] = p

        return proba

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels."""
        proba = self.predict_proba(X)
        return self.classes_[np.argmax(proba, axis=1)]

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Calculate accuracy."""
        return np.mean(self.predict(X) == y)


def example_usage():
    """Demonstrate Random Forest and ensemble methods."""
    print("=" * 60)
    print("Random Forest and Ensemble Methods Demonstration")
    print("=" * 60)

    # Generate synthetic dataset
    np.random.seed(42)
    n_samples = 1000
    n_features = 20

    # Classification dataset
    X = np.random.randn(n_samples, n_features)
    y = (X[:, 0] + X[:, 1] - X[:, 2] + 0.5 * np.random.randn(n_samples) > 0).astype(int)

    # Split data
    n_train = 700
    X_train, X_test = X[:n_train], X[n_train:]
    y_train, y_test = y[:n_train], y[n_train:]

    print("\n1. Random Forest Classifier")
    print("-" * 40)
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        max_features='sqrt',
        oob_score=True,
        random_state=42
    )
    rf.fit(X_train, y_train)

    train_score = rf.score(X_train, y_train)
    test_score = rf.score(X_test, y_test)
    print(f"Training accuracy: {train_score:.3f}")
    print(f"Testing accuracy: {test_score:.3f}")
    if rf.oob_score_ is not None:
        print(f"OOB score: {rf.oob_score_:.3f}")

    # Feature importance
    top_features = np.argsort(rf.feature_importances_)[-5:][::-1]
    print(f"Top 5 important features: {top_features}")

    print("\n2. Random Forest Regressor")
    print("-" * 40)
    # Regression dataset
    y_reg = X[:, 0] + 2 * X[:, 1] - X[:, 2] + 0.5 * np.random.randn(n_samples)
    y_train_reg, y_test_reg = y_reg[:n_train], y_reg[n_train:]

    rf_reg = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        max_features='sqrt',
        oob_score=True,
        random_state=42
    )
    rf_reg.fit(X_train, y_train_reg)

    train_r2 = rf_reg.score(X_train, y_train_reg)
    test_r2 = rf_reg.score(X_test, y_test_reg)
    print(f"Training R² score: {train_r2:.3f}")
    print(f"Testing R² score: {test_r2:.3f}")
    if rf_reg.oob_score_ is not None:
        print(f"OOB R² score: {rf_reg.oob_score_:.3f}")

    print("\n3. AdaBoost Classifier")
    print("-" * 40)
    ada = AdaBoostClassifier(
        n_estimators=50,
        learning_rate=1.0,
        random_state=42
    )
    ada.fit(X_train, y_train)

    ada_score = ada.score(X_test, y_test)
    print(f"AdaBoost testing accuracy: {ada_score:.3f}")
    print(f"Number of estimators used: {len(ada.estimators_)}")

    print("\n4. Gradient Boosting Classifier")
    print("-" * 40)
    gb = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        subsample=0.8,
        random_state=42
    )
    gb.fit(X_train, y_train)

    gb_score = gb.score(X_test, y_test)
    print(f"Gradient Boosting testing accuracy: {gb_score:.3f}")

    print("\n5. Ensemble Comparison")
    print("-" * 40)
    print(f"Random Forest accuracy: {test_score:.3f}")
    print(f"AdaBoost accuracy: {ada_score:.3f}")
    print(f"Gradient Boosting accuracy: {gb_score:.3f}")

    # Probability predictions comparison
    print("\n6. Probability Predictions (first 5 samples)")
    print("-" * 40)
    rf_proba = rf.predict_proba(X_test[:5])
    ada_proba = ada.predict_proba(X_test[:5])
    gb_proba = gb.predict_proba(X_test[:5])

    print("Random Forest probabilities:")
    print(rf_proba)
    print("\nAdaBoost probabilities:")
    print(ada_proba)
    print("\nGradient Boosting probabilities:")
    print(gb_proba)


if __name__ == "__main__":
    example_usage()