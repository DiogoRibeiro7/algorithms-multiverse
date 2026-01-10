#!/usr/bin/env python3
"""
Random Forest Implementation

Implements Random Forest for both classification and regression using
bootstrap aggregating (bagging) and random feature selection.

Builds on the Decision Tree implementation to create an ensemble of trees
that vote (classification) or average (regression) for final predictions.

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import List, Optional, Tuple, Union
from collections import Counter
import warnings
import multiprocessing

# Try to import joblib for parallel processing
try:
    from joblib import Parallel, delayed
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False

# Import our decision tree implementation
from decision_tree import DecisionTree, TreeNode


class RandomForest:
    """
    Random Forest classifier/regressor using ensemble of decision trees.

    Combines predictions from multiple trees trained on different
    subsets of data with random feature selection.
    """

    def __init__(self,
                 n_estimators: int = 100,
                 max_depth: Optional[int] = None,
                 min_samples_split: int = 2,
                 min_samples_leaf: int = 1,
                 max_features: Union[str, int, float] = 'sqrt',
                 bootstrap: bool = True,
                 oob_score: bool = False,
                 n_jobs: Optional[int] = None,
                 random_state: Optional[int] = None,
                 task: str = 'classification',
                 criterion: Optional[str] = None):
        """
        Initialize Random Forest.

        Args:
            n_estimators: Number of trees in the forest
            max_depth: Maximum depth of trees
            min_samples_split: Minimum samples required to split a node
            min_samples_leaf: Minimum samples required at a leaf node
            max_features: Number of features to consider for best split
                         ('sqrt', 'log2', int, or float fraction)
            bootstrap: Whether to use bootstrap samples
            oob_score: Whether to use out-of-bag samples to estimate accuracy
            n_jobs: Number of parallel jobs (-1 for all CPUs)
            random_state: Random seed for reproducibility
            task: 'classification' or 'regression'
            criterion: Split criterion (None for default based on task)
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.bootstrap = bootstrap
        self.oob_score = oob_score
        self.n_jobs = n_jobs if n_jobs is not None else 1
        self.random_state = random_state
        self.task = task

        # Set default criterion based on task
        if criterion is None:
            self.criterion = 'gini' if task == 'classification' else 'mse'
        else:
            self.criterion = criterion

        # Will be set during fit
        self.estimators_ = []
        self.feature_importances_ = None
        self.oob_score_ = None
        self.oob_decision_function_ = None
        self.classes_ = None
        self.n_classes_ = None
        self.n_features_ = None
        self.max_features_ = None

    def _get_max_features(self, n_features: int) -> int:
        """
        Calculate the actual number of features to consider.

        Args:
            n_features: Total number of features

        Returns:
            Number of features to use
        """
        if isinstance(self.max_features, str):
            if self.max_features == 'sqrt':
                return max(1, int(np.sqrt(n_features)))
            elif self.max_features == 'log2':
                return max(1, int(np.log2(n_features)))
            elif self.max_features == 'auto':
                return max(1, int(np.sqrt(n_features)))
            else:
                raise ValueError(f"Unknown max_features: {self.max_features}")
        elif isinstance(self.max_features, float):
            return max(1, int(self.max_features * n_features))
        elif isinstance(self.max_features, int):
            return min(self.max_features, n_features)
        elif self.max_features is None:
            return n_features
        else:
            raise ValueError(f"Invalid max_features: {self.max_features}")

    def _bootstrap_sample(self, X: np.ndarray, y: np.ndarray,
                         random_state: np.random.RandomState) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Create bootstrap sample with replacement.

        Args:
            X: Features
            y: Labels
            random_state: Random state for sampling

        Returns:
            Bootstrap sample X, y, and out-of-bag indices
        """
        n_samples = X.shape[0]

        if self.bootstrap:
            # Sample with replacement
            indices = random_state.choice(n_samples, n_samples, replace=True)
            oob_indices = np.array(list(set(range(n_samples)) - set(indices)))
        else:
            # Use all samples
            indices = np.arange(n_samples)
            oob_indices = np.array([])

        return X[indices], y[indices], oob_indices

    def _train_tree(self, tree_idx: int, X: np.ndarray, y: np.ndarray) -> Tuple[DecisionTree, np.ndarray, np.ndarray]:
        """
        Train a single decision tree.

        Args:
            tree_idx: Index of the tree (for random seed)
            X: Training features
            y: Training labels

        Returns:
            Trained tree, feature indices used, OOB indices
        """
        # Create random state for this tree
        if self.random_state is not None:
            seed = self.random_state + tree_idx
        else:
            seed = None
        random_state = np.random.RandomState(seed)

        # Bootstrap sample
        X_sample, y_sample, oob_indices = self._bootstrap_sample(X, y, random_state)

        # Random feature selection
        n_features = X.shape[1]
        feature_indices = np.arange(n_features)

        # Create decision tree with random feature selection
        tree = DecisionTreeWithRandomFeatures(
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            criterion=self.criterion,
            task=self.task,
            max_features=self.max_features_,
            random_state=seed
        )

        # Train tree
        tree.fit(X_sample, y_sample)

        return tree, feature_indices, oob_indices

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'RandomForest':
        """
        Train the Random Forest.

        Args:
            X: Training features of shape (n_samples, n_features)
            y: Training labels of shape (n_samples,)

        Returns:
            Self for method chaining
        """
        X = np.asarray(X)
        y = np.asarray(y)

        n_samples, n_features = X.shape
        self.n_features_ = n_features
        self.max_features_ = self._get_max_features(n_features)

        # Store classes for classification
        if self.task == 'classification':
            self.classes_ = np.unique(y)
            self.n_classes_ = len(self.classes_)

        # Initialize OOB score tracking
        if self.oob_score:
            if self.task == 'classification':
                self.oob_decision_function_ = np.zeros((n_samples, self.n_classes_))
            else:
                self.oob_decision_function_ = np.zeros(n_samples)
            oob_counts = np.zeros(n_samples)

        # Train trees in parallel
        if self.n_jobs == -1:
            n_jobs = multiprocessing.cpu_count()
        else:
            n_jobs = self.n_jobs

        # Train all trees
        if n_jobs > 1 and HAS_JOBLIB:
            # Parallel training with joblib
            results = Parallel(n_jobs=n_jobs)(
                delayed(self._train_tree)(i, X, y)
                for i in range(self.n_estimators)
            )
            self.estimators_ = [r[0] for r in results]
            oob_indices_list = [r[2] for r in results]
        else:
            # Sequential training
            self.estimators_ = []
            oob_indices_list = []

            for i in range(self.n_estimators):
                tree, _, oob_indices = self._train_tree(i, X, y)
                self.estimators_.append(tree)
                oob_indices_list.append(oob_indices)

        # Calculate OOB score if requested
        if self.oob_score and self.bootstrap:
            for tree, oob_indices in zip(self.estimators_, oob_indices_list):
                if len(oob_indices) > 0:
                    X_oob = X[oob_indices]

                    if self.task == 'classification':
                        # Get probability predictions for OOB samples
                        predictions = tree.predict_proba(X_oob)
                        for i, idx in enumerate(oob_indices):
                            self.oob_decision_function_[idx] += predictions[i]
                            oob_counts[idx] += 1
                    else:
                        # Get regression predictions for OOB samples
                        predictions = tree.predict(X_oob)
                        for i, idx in enumerate(oob_indices):
                            self.oob_decision_function_[idx] += predictions[i]
                            oob_counts[idx] += 1

            # Average OOB predictions
            mask = oob_counts > 0
            if self.task == 'classification':
                self.oob_decision_function_[mask] /= oob_counts[mask, np.newaxis]
                oob_predictions = self.classes_[np.argmax(self.oob_decision_function_[mask], axis=1)]
                self.oob_score_ = np.mean(oob_predictions == y[mask])
            else:
                self.oob_decision_function_[mask] /= oob_counts[mask]
                self.oob_score_ = 1 - np.mean((self.oob_decision_function_[mask] - y[mask]) ** 2) / np.var(y[mask])

        # Calculate feature importances
        self._calculate_feature_importances()

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels or values for samples.

        Args:
            X: Test samples of shape (n_samples, n_features)

        Returns:
            Predicted labels/values
        """
        X = np.asarray(X)

        if self.task == 'classification':
            # Get votes from all trees
            predictions = np.array([tree.predict(X) for tree in self.estimators_])

            # Majority voting
            n_samples = X.shape[0]
            final_predictions = np.zeros(n_samples)

            for i in range(n_samples):
                votes = predictions[:, i]
                final_predictions[i] = Counter(votes).most_common(1)[0][0]

            return final_predictions
        else:
            # Average predictions for regression
            predictions = np.array([tree.predict(X) for tree in self.estimators_])
            return np.mean(predictions, axis=0)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities for samples.

        Args:
            X: Test samples

        Returns:
            Class probabilities of shape (n_samples, n_classes)
        """
        if self.task != 'classification':
            raise ValueError("predict_proba is only available for classification")

        X = np.asarray(X)
        n_samples = X.shape[0]

        # Get probability predictions from all trees
        all_proba = np.zeros((self.n_estimators, n_samples, self.n_classes_))

        for i, tree in enumerate(self.estimators_):
            all_proba[i] = tree.predict_proba(X)

        # Average probabilities
        return np.mean(all_proba, axis=0)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate accuracy (classification) or R² score (regression).

        Args:
            X: Test features
            y: True labels

        Returns:
            Accuracy or R² score
        """
        predictions = self.predict(X)

        if self.task == 'classification':
            return np.mean(predictions == y)
        else:
            ss_res = np.sum((y - predictions) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0

    def _calculate_feature_importances(self):
        """Calculate feature importances as average over all trees."""
        if not self.estimators_:
            return

        # Collect importances from all trees
        all_importances = np.zeros((len(self.estimators_), self.n_features_))

        for i, tree in enumerate(self.estimators_):
            if hasattr(tree, 'feature_importances_') and tree.feature_importances_ is not None:
                all_importances[i] = tree.feature_importances_

        # Average across all trees
        self.feature_importances_ = np.mean(all_importances, axis=0)

        # Normalize
        total = np.sum(self.feature_importances_)
        if total > 0:
            self.feature_importances_ /= total


class DecisionTreeWithRandomFeatures(DecisionTree):
    """
    Decision Tree with random feature selection at each split.

    Extends the base DecisionTree to only consider a random subset
    of features at each split.
    """

    def __init__(self, max_features: int = None, **kwargs):
        """
        Initialize tree with random feature selection.

        Args:
            max_features: Number of features to consider at each split
            **kwargs: Other DecisionTree parameters
        """
        super().__init__(**kwargs)
        self.max_features = max_features
        self.rng = np.random.RandomState(kwargs.get('random_state'))

    def _best_split(self, X: np.ndarray, y: np.ndarray) -> Tuple[int, float]:
        """
        Find the best split considering only random subset of features.

        Args:
            X: Features
            y: Labels

        Returns:
            Best feature index and threshold
        """
        n_features = X.shape[1]

        # Select random features
        if self.max_features is not None and self.max_features < n_features:
            feature_indices = self.rng.choice(n_features, self.max_features, replace=False)
        else:
            feature_indices = np.arange(n_features)

        best_gain = -np.inf
        best_feature = None
        best_threshold = None

        current_impurity = self._calculate_impurity(y)

        for feature_idx in feature_indices:
            thresholds = np.unique(X[:, feature_idx])

            for threshold in thresholds:
                left_mask = X[:, feature_idx] <= threshold
                right_mask = ~left_mask

                if np.sum(left_mask) < self.min_samples_leaf or \
                   np.sum(right_mask) < self.min_samples_leaf:
                    continue

                # Calculate information gain
                left_impurity = self._calculate_impurity(y[left_mask])
                right_impurity = self._calculate_impurity(y[right_mask])

                n_left = np.sum(left_mask)
                n_right = np.sum(right_mask)
                n_total = n_left + n_right

                weighted_impurity = (n_left / n_total) * left_impurity + \
                                  (n_right / n_total) * right_impurity

                gain = current_impurity - weighted_impurity

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature_idx
                    best_threshold = threshold

        return best_feature, best_threshold


class ExtraTreesClassifier(RandomForest):
    """
    Extremely Randomized Trees (Extra Trees) classifier.

    Similar to Random Forest but with more randomization:
    - Uses the whole dataset (no bootstrap)
    - Randomly selects thresholds for splitting
    """

    def __init__(self, **kwargs):
        """Initialize Extra Trees with no bootstrap by default."""
        kwargs['bootstrap'] = False
        super().__init__(**kwargs)


def demonstrate_random_forest():
    """Demonstrate Random Forest capabilities"""
    print("=" * 60)
    print("Random Forest Demonstration")
    print("=" * 60)

    # Generate sample data
    np.random.seed(42)

    # Classification dataset
    from sklearn.datasets import make_classification
    X_class, y_class = make_classification(
        n_samples=200,
        n_features=10,
        n_informative=5,
        n_redundant=2,
        n_classes=3,
        random_state=42
    )

    # Split data
    n_train = 150
    X_train, X_test = X_class[:n_train], X_class[n_train:]
    y_train, y_test = y_class[:n_train], y_class[n_train:]

    # 1. Random Forest Classification
    print("\n1. Random Forest Classification")
    print("-" * 40)

    rf_classifier = RandomForest(
        n_estimators=100,
        max_depth=10,
        max_features='sqrt',
        oob_score=True,
        random_state=42,
        task='classification'
    )

    rf_classifier.fit(X_train, y_train)

    train_score = rf_classifier.score(X_train, y_train)
    test_score = rf_classifier.score(X_test, y_test)

    print(f"Training accuracy: {train_score:.3f}")
    print(f"Testing accuracy: {test_score:.3f}")

    if rf_classifier.oob_score_ is not None:
        print(f"OOB score: {rf_classifier.oob_score_:.3f}")

    # Feature importances
    importances = rf_classifier.feature_importances_
    top_features = np.argsort(importances)[-5:]
    print(f"Top 5 features: {top_features}")

    # Class probabilities
    proba = rf_classifier.predict_proba(X_test[:5])
    print(f"\nSample probability predictions shape: {proba.shape}")

    # 2. Random Forest Regression
    print("\n2. Random Forest Regression")
    print("-" * 40)

    # Generate regression data
    from sklearn.datasets import make_regression
    X_reg, y_reg = make_regression(
        n_samples=200,
        n_features=10,
        n_informative=5,
        noise=0.1,
        random_state=42
    )

    X_train_reg = X_reg[:150]
    X_test_reg = X_reg[150:]
    y_train_reg = y_reg[:150]
    y_test_reg = y_reg[150:]

    rf_regressor = RandomForest(
        n_estimators=50,
        max_depth=10,
        max_features='sqrt',
        oob_score=True,
        random_state=42,
        task='regression'
    )

    rf_regressor.fit(X_train_reg, y_train_reg)

    train_r2 = rf_regressor.score(X_train_reg, y_train_reg)
    test_r2 = rf_regressor.score(X_test_reg, y_test_reg)

    print(f"Training R² score: {train_r2:.3f}")
    print(f"Testing R² score: {test_r2:.3f}")

    if rf_regressor.oob_score_ is not None:
        print(f"OOB R² score: {rf_regressor.oob_score_:.3f}")

    # 3. Effect of number of estimators
    print("\n3. Effect of Number of Estimators")
    print("-" * 40)

    n_estimators_list = [10, 50, 100, 200]

    for n_est in n_estimators_list:
        rf = RandomForest(
            n_estimators=n_est,
            max_features='sqrt',
            random_state=42,
            task='classification'
        )
        rf.fit(X_train, y_train)
        score = rf.score(X_test, y_test)
        print(f"n_estimators={n_est:3d}: Accuracy = {score:.3f}")

    # 4. Compare with single decision tree
    print("\n4. Comparison with Single Decision Tree")
    print("-" * 40)

    # Single tree
    single_tree = DecisionTree(
        max_depth=10,
        task='classification'
    )
    single_tree.fit(X_train, y_train)
    single_score = single_tree.score(X_test, y_test)

    print(f"Single Decision Tree accuracy: {single_score:.3f}")
    print(f"Random Forest (100 trees) accuracy: {test_score:.3f}")
    print(f"Improvement: {(test_score - single_score):.3f}")

    # 5. Extra Trees comparison
    print("\n5. Extra Trees Classifier")
    print("-" * 40)

    extra_trees = ExtraTreesClassifier(
        n_estimators=100,
        max_depth=10,
        max_features='sqrt',
        random_state=42,
        task='classification'
    )

    extra_trees.fit(X_train, y_train)
    extra_score = extra_trees.score(X_test, y_test)

    print(f"Extra Trees accuracy: {extra_score:.3f}")
    print(f"Random Forest accuracy: {test_score:.3f}")


if __name__ == "__main__":
    # Check if scikit-learn is available for demo
    try:
        from sklearn.datasets import make_classification, make_regression
        demonstrate_random_forest()
    except ImportError:
        print("Note: scikit-learn is required for the demonstration.")
        print("Install with: pip install scikit-learn")

        # Simple demo without sklearn
        print("\nSimple Random Forest Demo (without sklearn)")
        print("-" * 40)

        # Generate simple data
        np.random.seed(42)
        X = np.random.randn(100, 4)
        y = (X[:, 0] + X[:, 1] > 0).astype(int)

        # Train Random Forest
        rf = RandomForest(
            n_estimators=10,
            max_depth=5,
            task='classification',
            random_state=42
        )

        rf.fit(X[:80], y[:80])
        score = rf.score(X[80:], y[80:])

        print(f"Random Forest accuracy: {score:.3f}")
        print(f"Number of trees: {len(rf.estimators_)}")
        print(f"Feature importances: {rf.feature_importances_}")