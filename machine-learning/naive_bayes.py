#!/usr/bin/env python3
"""
Naive Bayes Classifier Implementation

Implements three variants of Naive Bayes:
1. Gaussian Naive Bayes - for continuous features
2. Multinomial Naive Bayes - for discrete count features
3. Bernoulli Naive Bayes - for binary/boolean features

Based on Bayes' theorem with the "naive" assumption of conditional independence
between features.

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import List, Tuple, Optional, Dict, Union
from collections import defaultdict
import warnings
from scipy.stats import norm
from abc import ABC, abstractmethod


class BaseNaiveBayes(ABC):
    """Abstract base class for Naive Bayes classifiers"""

    def __init__(self):
        """Initialize base Naive Bayes classifier"""
        self.classes = None
        self.class_priors = None
        self.n_features = None
        self.n_samples = None

    @abstractmethod
    def _calculate_likelihood(self, X: np.ndarray, class_idx: int) -> np.ndarray:
        """Calculate likelihood P(X|class)"""
        pass

    @abstractmethod
    def _fit_class_parameters(self, X: np.ndarray, y: np.ndarray):
        """Fit parameters for each class"""
        pass

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BaseNaiveBayes':
        """
        Fit the Naive Bayes model.

        Args:
            X: Training features of shape (n_samples, n_features)
            y: Training labels of shape (n_samples,)

        Returns:
            Self for method chaining
        """
        X = np.asarray(X)
        y = np.asarray(y)

        self.n_samples, self.n_features = X.shape
        self.classes = np.unique(y)
        n_classes = len(self.classes)

        # Calculate class priors P(y)
        self.class_priors = np.zeros(n_classes)
        for idx, c in enumerate(self.classes):
            self.class_priors[idx] = np.sum(y == c) / self.n_samples

        # Fit class-specific parameters
        self._fit_class_parameters(X, y)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels for samples in X.

        Args:
            X: Features of shape (n_samples, n_features)

        Returns:
            Predicted class labels
        """
        X = np.asarray(X)
        posteriors = self.predict_proba(X)
        return self.classes[np.argmax(posteriors, axis=1)]

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities for samples in X.

        Args:
            X: Features of shape (n_samples, n_features)

        Returns:
            Class probabilities of shape (n_samples, n_classes)
        """
        X = np.asarray(X)
        n_samples = X.shape[0]
        n_classes = len(self.classes)

        # Calculate posterior probabilities for each class
        posteriors = np.zeros((n_samples, n_classes))

        for idx in range(n_classes):
            # Prior probability P(y)
            prior = np.log(self.class_priors[idx])

            # Likelihood P(X|y)
            likelihood = self._calculate_likelihood(X, idx)

            # Posterior P(y|X) = P(X|y) * P(y) (in log space)
            posteriors[:, idx] = likelihood + prior

        # Normalize to get probabilities (convert from log space)
        # Use log-sum-exp trick for numerical stability
        max_posterior = np.max(posteriors, axis=1, keepdims=True)
        posteriors = posteriors - max_posterior
        posteriors = np.exp(posteriors)
        posteriors = posteriors / np.sum(posteriors, axis=1, keepdims=True)

        return posteriors

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate accuracy score.

        Args:
            X: Features of shape (n_samples, n_features)
            y: True labels of shape (n_samples,)

        Returns:
            Accuracy score between 0 and 1
        """
        predictions = self.predict(X)
        return np.mean(predictions == y)


class GaussianNB(BaseNaiveBayes):
    """
    Gaussian Naive Bayes for continuous features.

    Assumes features follow a Gaussian distribution within each class.
    """

    def __init__(self, var_smoothing: float = 1e-9):
        """
        Initialize Gaussian Naive Bayes.

        Args:
            var_smoothing: Portion of largest variance added to variances
                          for calculation stability
        """
        super().__init__()
        self.var_smoothing = var_smoothing
        self.theta = None  # Mean of each feature per class
        self.sigma = None  # Variance of each feature per class

    def _fit_class_parameters(self, X: np.ndarray, y: np.ndarray):
        """Fit Gaussian parameters (mean and variance) for each class"""
        n_classes = len(self.classes)

        self.theta = np.zeros((n_classes, self.n_features))
        self.sigma = np.zeros((n_classes, self.n_features))

        for idx, c in enumerate(self.classes):
            X_c = X[y == c]
            self.theta[idx, :] = np.mean(X_c, axis=0)
            self.sigma[idx, :] = np.var(X_c, axis=0) + self.var_smoothing

    def _calculate_likelihood(self, X: np.ndarray, class_idx: int) -> np.ndarray:
        """Calculate Gaussian likelihood for each sample"""
        mean = self.theta[class_idx]
        var = self.sigma[class_idx]

        # Calculate Gaussian PDF in log space for numerical stability
        # log P(x|y) = -0.5 * log(2*pi*var) - 0.5 * (x-mean)^2 / var
        log_likelihood = -0.5 * np.sum(np.log(2 * np.pi * var))
        log_likelihood -= 0.5 * np.sum(((X - mean) ** 2) / var, axis=1)

        return log_likelihood


class MultinomialNB(BaseNaiveBayes):
    """
    Multinomial Naive Bayes for discrete count features.

    Commonly used for text classification with word count features.
    """

    def __init__(self, alpha: float = 1.0):
        """
        Initialize Multinomial Naive Bayes.

        Args:
            alpha: Laplace smoothing parameter (0 for no smoothing)
        """
        super().__init__()
        self.alpha = alpha
        self.feature_log_prob = None  # Log probability of each feature per class
        self.feature_count = None  # Count of each feature per class
        self.class_count = None  # Total count per class

    def _fit_class_parameters(self, X: np.ndarray, y: np.ndarray):
        """Fit multinomial parameters for each class"""
        n_classes = len(self.classes)

        self.feature_count = np.zeros((n_classes, self.n_features))
        self.class_count = np.zeros(n_classes)

        for idx, c in enumerate(self.classes):
            X_c = X[y == c]
            self.feature_count[idx, :] = np.sum(X_c, axis=0) + self.alpha
            self.class_count[idx] = np.sum(self.feature_count[idx, :])

        # Calculate log probabilities
        self.feature_log_prob = (np.log(self.feature_count) -
                                 np.log(self.class_count[:, np.newaxis]))

    def _calculate_likelihood(self, X: np.ndarray, class_idx: int) -> np.ndarray:
        """Calculate multinomial likelihood for each sample"""
        # P(X|y) = product of P(xi|y)^xi for all features
        # In log space: log P(X|y) = sum of xi * log P(xi|y)
        return np.dot(X, self.feature_log_prob[class_idx])


class BernoulliNB(BaseNaiveBayes):
    """
    Bernoulli Naive Bayes for binary/boolean features.

    Useful for binary feature vectors (e.g., word presence/absence).
    """

    def __init__(self, alpha: float = 1.0, binarize: float = 0.0):
        """
        Initialize Bernoulli Naive Bayes.

        Args:
            alpha: Laplace smoothing parameter
            binarize: Threshold for binarizing features (None to assume already binary)
        """
        super().__init__()
        self.alpha = alpha
        self.binarize = binarize
        self.feature_log_prob_pos = None  # Log P(xi=1|y)
        self.feature_log_prob_neg = None  # Log P(xi=0|y)

    def _binarize_X(self, X: np.ndarray) -> np.ndarray:
        """Binarize features based on threshold"""
        if self.binarize is not None:
            return (X > self.binarize).astype(np.float64)
        return X

    def _fit_class_parameters(self, X: np.ndarray, y: np.ndarray):
        """Fit Bernoulli parameters for each class"""
        X = self._binarize_X(X)
        n_classes = len(self.classes)

        feature_count = np.zeros((n_classes, self.n_features))
        class_count = np.zeros(n_classes)

        for idx, c in enumerate(self.classes):
            X_c = X[y == c]
            feature_count[idx] = np.sum(X_c, axis=0) + self.alpha
            class_count[idx] = X_c.shape[0] + 2 * self.alpha

        # Calculate log probabilities
        smoothed_prob = feature_count / class_count[:, np.newaxis]
        self.feature_log_prob_pos = np.log(smoothed_prob)
        self.feature_log_prob_neg = np.log(1 - smoothed_prob)

    def _calculate_likelihood(self, X: np.ndarray, class_idx: int) -> np.ndarray:
        """Calculate Bernoulli likelihood for each sample"""
        X = self._binarize_X(X)

        # P(X|y) = product of P(xi|y) for xi=1 and (1-P(xi|y)) for xi=0
        # In log space: sum of xi*log(P(xi|y)) + (1-xi)*log(1-P(xi|y))
        pos_part = np.dot(X, self.feature_log_prob_pos[class_idx])
        neg_part = np.dot(1 - X, self.feature_log_prob_neg[class_idx])

        return pos_part + neg_part


class ComplementNB(MultinomialNB):
    """
    Complement Naive Bayes for imbalanced datasets.

    Particularly effective for imbalanced text classification tasks.
    """

    def __init__(self, alpha: float = 1.0, norm: bool = False):
        """
        Initialize Complement Naive Bayes.

        Args:
            alpha: Laplace smoothing parameter
            norm: Whether to perform second normalization
        """
        super().__init__(alpha=alpha)
        self.norm = norm

    def _fit_class_parameters(self, X: np.ndarray, y: np.ndarray):
        """Fit complement parameters for each class"""
        n_classes = len(self.classes)

        self.feature_count = np.zeros((n_classes, self.n_features))
        self.class_count = np.zeros(n_classes)

        # Calculate complement counts (all samples NOT in class c)
        for idx, c in enumerate(self.classes):
            X_c_complement = X[y != c]
            self.feature_count[idx, :] = np.sum(X_c_complement, axis=0) + self.alpha
            self.class_count[idx] = np.sum(self.feature_count[idx, :])

        # Calculate log probabilities of complement
        self.feature_log_prob = (np.log(self.feature_count) -
                                 np.log(self.class_count[:, np.newaxis]))

        # Weight normalization if requested
        if self.norm:
            self.feature_log_prob = self.feature_log_prob / np.sum(np.abs(self.feature_log_prob), axis=1)[:, np.newaxis]

    def _calculate_likelihood(self, X: np.ndarray, class_idx: int) -> np.ndarray:
        """Calculate complement likelihood (actually negative of complement)"""
        # Use negative of complement class log probability
        return -np.dot(X, self.feature_log_prob[class_idx])


def create_toy_dataset() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Create a toy dataset for demonstration"""
    np.random.seed(42)

    # Generate Gaussian data for GaussianNB
    n_samples = 150
    n_features = 4

    # Class 0: centered around (0, 0, 0, 0)
    X0 = np.random.randn(50, n_features) * 0.5

    # Class 1: centered around (2, 2, 2, 2)
    X1 = np.random.randn(50, n_features) * 0.5 + 2

    # Class 2: centered around (-2, -2, -2, -2)
    X2 = np.random.randn(50, n_features) * 0.5 - 2

    X = np.vstack([X0, X1, X2])
    y = np.array([0] * 50 + [1] * 50 + [2] * 50)

    # Shuffle the data
    indices = np.random.permutation(n_samples)
    X = X[indices]
    y = y[indices]

    # Split into train and test
    train_size = int(0.8 * n_samples)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    return X_train, X_test, y_train, y_test


def create_text_dataset() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Create a simple text classification dataset (word counts)"""
    # Simulate word count features for document classification
    # Features represent counts of different words

    # Sports documents (high counts for sports-related words)
    sports_docs = np.array([
        [5, 3, 0, 0, 2, 1, 0, 0],  # [game, team, movie, actor, ball, play, film, scene]
        [4, 4, 0, 0, 3, 2, 0, 0],
        [6, 2, 0, 0, 4, 3, 0, 0],
        [3, 5, 0, 1, 2, 4, 0, 0],
        [4, 3, 0, 0, 5, 2, 0, 0],
    ])

    # Movie documents (high counts for movie-related words)
    movie_docs = np.array([
        [0, 0, 5, 4, 0, 2, 3, 2],
        [0, 1, 4, 3, 0, 1, 4, 3],
        [0, 0, 6, 5, 0, 0, 2, 4],
        [1, 0, 3, 4, 0, 1, 5, 2],
        [0, 0, 4, 3, 0, 2, 3, 5],
    ])

    X = np.vstack([sports_docs, movie_docs])
    y = np.array([0] * 5 + [1] * 5)  # 0: sports, 1: movies

    # Simple train/test split
    X_train = np.vstack([sports_docs[:4], movie_docs[:4]])
    y_train = np.array([0] * 4 + [1] * 4)
    X_test = np.vstack([sports_docs[4:], movie_docs[4:]])
    y_test = np.array([0] * 1 + [1] * 1)

    return X_train, X_test, y_train, y_test


def demonstrate_naive_bayes():
    """Demonstrate all Naive Bayes variants"""
    print("=" * 60)
    print("Naive Bayes Classifier Demonstration")
    print("=" * 60)

    # 1. Gaussian Naive Bayes
    print("\n1. Gaussian Naive Bayes (Continuous Features)")
    print("-" * 40)

    X_train, X_test, y_train, y_test = create_toy_dataset()

    gnb = GaussianNB()
    gnb.fit(X_train, y_train)

    train_score = gnb.score(X_train, y_train)
    test_score = gnb.score(X_test, y_test)

    print(f"Training accuracy: {train_score:.3f}")
    print(f"Testing accuracy: {test_score:.3f}")

    # Show predictions with probabilities
    sample = X_test[:3]
    predictions = gnb.predict(sample)
    probabilities = gnb.predict_proba(sample)

    print("\nSample predictions:")
    for i in range(len(sample)):
        print(f"  Sample {i+1}: Predicted={predictions[i]}, "
              f"Probabilities={probabilities[i].round(3)}")

    # 2. Multinomial Naive Bayes
    print("\n2. Multinomial Naive Bayes (Count Features)")
    print("-" * 40)

    X_train, X_test, y_train, y_test = create_text_dataset()

    mnb = MultinomialNB(alpha=1.0)
    mnb.fit(X_train, y_train)

    train_score = mnb.score(X_train, y_train)
    test_score = mnb.score(X_test, y_test)

    print(f"Training accuracy: {train_score:.3f}")
    print(f"Testing accuracy: {test_score:.3f}")

    # 3. Bernoulli Naive Bayes
    print("\n3. Bernoulli Naive Bayes (Binary Features)")
    print("-" * 40)

    # Convert to binary features (presence/absence)
    X_train_binary = (X_train > 0).astype(int)
    X_test_binary = (X_test > 0).astype(int)

    bnb = BernoulliNB(alpha=1.0)
    bnb.fit(X_train_binary, y_train)

    train_score = bnb.score(X_train_binary, y_train)
    test_score = bnb.score(X_test_binary, y_test)

    print(f"Training accuracy: {train_score:.3f}")
    print(f"Testing accuracy: {test_score:.3f}")

    # 4. Complement Naive Bayes
    print("\n4. Complement Naive Bayes (Imbalanced Data)")
    print("-" * 40)

    cnb = ComplementNB(alpha=1.0)
    cnb.fit(X_train, y_train)

    train_score = cnb.score(X_train, y_train)
    test_score = cnb.score(X_test, y_test)

    print(f"Training accuracy: {train_score:.3f}")
    print(f"Testing accuracy: {test_score:.3f}")

    # Comparison
    print("\n" + "=" * 60)
    print("Classifier Comparison on Text Data")
    print("=" * 60)

    classifiers = [
        ("Multinomial NB", MultinomialNB()),
        ("Bernoulli NB", BernoulliNB(binarize=0.0)),
        ("Complement NB", ComplementNB()),
    ]

    for name, clf in classifiers:
        if name == "Bernoulli NB":
            clf.fit(X_train_binary, y_train)
            score = clf.score(X_test_binary, y_test)
        else:
            clf.fit(X_train, y_train)
            score = clf.score(X_test, y_test)
        print(f"{name:15s}: Test accuracy = {score:.3f}")


if __name__ == "__main__":
    demonstrate_naive_bayes()