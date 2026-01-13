#!/usr/bin/env python3
"""
Naive Bayes Classifiers

This module implements various Naive Bayes classifiers for different types of data:
- Gaussian Naive Bayes: For continuous features with Gaussian distribution
- Multinomial Naive Bayes: For discrete count data (e.g., text classification)
- Bernoulli Naive Bayes: For binary/boolean features
- Complement Naive Bayes: For imbalanced datasets

Naive Bayes classifiers are based on Bayes' theorem with the "naive" assumption
of conditional independence between features.

Features:
- Fast training and prediction
- Works well with high-dimensional data
- Probabilistic predictions
- Online learning support
- Minimal hyperparameter tuning

Applications:
- Text classification (spam filtering, sentiment analysis)
- Document categorization
- Medical diagnosis
- Real-time prediction
- Multi-class classification

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import Optional, Tuple, List, Dict, Union
from dataclasses import dataclass
import warnings
from scipy.special import logsumexp


@dataclass
class NaiveBayesResult:
    """Results from Naive Bayes training"""
    class_priors: np.ndarray  # Prior probabilities for each class
    feature_stats: Dict  # Feature statistics (varies by model type)
    classes: np.ndarray  # Unique class labels
    n_features: int  # Number of features


class GaussianNB:
    """
    Gaussian Naive Bayes classifier

    Assumes features follow Gaussian (normal) distribution within each class.
    Suitable for continuous features.

    Parameters:
    -----------
    var_smoothing : float, default=1e-9
        Portion of largest variance added to variances for stability
    priors : np.ndarray, optional
        Prior probabilities of the classes
    """

    def __init__(self, var_smoothing: float = 1e-9, priors: Optional[np.ndarray] = None):
        self.var_smoothing = var_smoothing
        self.priors = priors

        # Will be set during fit
        self.classes_ = None
        self.class_priors_ = None
        self.theta_ = None  # Mean of each feature per class
        self.sigma_ = None  # Variance of each feature per class
        self.n_features_ = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'GaussianNB':
        """
        Fit Gaussian Naive Bayes

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Training features
        y : np.ndarray of shape (n_samples,)
            Target values

        Returns:
        --------
        self : GaussianNB
            Fitted estimator
        """
        X = np.asarray(X)
        y = np.asarray(y)

        n_samples, n_features = X.shape
        self.n_features_ = n_features

        # Get unique classes
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)

        # Initialize parameters
        self.theta_ = np.zeros((n_classes, n_features))
        self.sigma_ = np.zeros((n_classes, n_features))
        self.class_priors_ = np.zeros(n_classes)

        # Calculate statistics for each class
        for idx, class_val in enumerate(self.classes_):
            mask = y == class_val
            X_class = X[mask]

            # Calculate prior
            if self.priors is not None:
                self.class_priors_[idx] = self.priors[idx]
            else:
                self.class_priors_[idx] = np.sum(mask) / n_samples

            # Calculate mean and variance
            self.theta_[idx] = X_class.mean(axis=0)
            self.sigma_[idx] = X_class.var(axis=0) + self.var_smoothing

        return self

    def _joint_log_likelihood(self, X: np.ndarray) -> np.ndarray:
        """
        Compute joint log-likelihood P(X, y) for each class

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        log_likelihood : np.ndarray of shape (n_samples, n_classes)
            Log-likelihood for each sample and class
        """
        n_samples = X.shape[0]
        n_classes = len(self.classes_)
        log_likelihood = np.zeros((n_samples, n_classes))

        for idx in range(n_classes):
            # Log prior
            log_prior = np.log(self.class_priors_[idx])

            # Log likelihood of features given class
            # Using Gaussian PDF: -0.5 * log(2π * σ²) - 0.5 * (x - μ)² / σ²
            variance = self.sigma_[idx]
            mean = self.theta_[idx]

            log_likelihood[:, idx] = log_prior - 0.5 * np.sum(
                np.log(2 * np.pi * variance) + ((X - mean) ** 2) / variance,
                axis=1
            )

        return log_likelihood

    def predict_log_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Compute log probabilities of samples for each class

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        log_proba : np.ndarray of shape (n_samples, n_classes)
            Log probabilities
        """
        if self.classes_ is None:
            raise ValueError("Model must be fitted before prediction")

        X = np.asarray(X)

        # Compute joint log-likelihood
        log_likelihood = self._joint_log_likelihood(X)

        # Normalize to get posterior probabilities
        # log P(y|X) = log P(X, y) - log P(X)
        log_proba = log_likelihood - logsumexp(log_likelihood, axis=1, keepdims=True)

        return log_proba

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Compute probabilities of samples for each class

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        proba : np.ndarray of shape (n_samples, n_classes)
            Probabilities
        """
        return np.exp(self.predict_log_proba(X))

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        y_pred : np.ndarray of shape (n_samples,)
            Predicted class labels
        """
        log_proba = self.predict_log_proba(X)
        return self.classes_[np.argmax(log_proba, axis=1)]

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute accuracy score"""
        y_pred = self.predict(X)
        return np.mean(y_pred == y)


class MultinomialNB:
    """
    Multinomial Naive Bayes classifier

    Suitable for discrete features (e.g., word counts for text classification).

    Parameters:
    -----------
    alpha : float, default=1.0
        Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing)
    fit_prior : bool, default=True
        Whether to learn class prior probabilities
    class_prior : np.ndarray, optional
        Prior probabilities of the classes
    """

    def __init__(
        self,
        alpha: float = 1.0,
        fit_prior: bool = True,
        class_prior: Optional[np.ndarray] = None
    ):
        self.alpha = alpha
        self.fit_prior = fit_prior
        self.class_prior = class_prior

        # Will be set during fit
        self.classes_ = None
        self.class_priors_ = None
        self.feature_log_prob_ = None
        self.feature_count_ = None
        self.n_features_ = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'MultinomialNB':
        """
        Fit Multinomial Naive Bayes

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Training features (should be non-negative integers)
        y : np.ndarray of shape (n_samples,)
            Target values

        Returns:
        --------
        self : MultinomialNB
            Fitted estimator
        """
        X = np.asarray(X)
        y = np.asarray(y)

        # Check for negative values
        if np.any(X < 0):
            raise ValueError("Multinomial NB requires non-negative features")

        n_samples, n_features = X.shape
        self.n_features_ = n_features

        # Get unique classes
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)

        # Initialize feature counts
        self.feature_count_ = np.zeros((n_classes, n_features))
        self.class_priors_ = np.zeros(n_classes)

        # Count features for each class
        for idx, class_val in enumerate(self.classes_):
            mask = y == class_val
            X_class = X[mask]

            # Sum feature counts
            self.feature_count_[idx] = X_class.sum(axis=0)

            # Calculate prior
            if self.fit_prior:
                if self.class_prior is not None:
                    self.class_priors_[idx] = self.class_prior[idx]
                else:
                    self.class_priors_[idx] = np.sum(mask) / n_samples
            else:
                self.class_priors_[idx] = 1.0 / n_classes

        # Apply smoothing and calculate log probabilities
        smoothed_fc = self.feature_count_ + self.alpha
        smoothed_cc = smoothed_fc.sum(axis=1, keepdims=True)

        # Log probabilities of features given class
        self.feature_log_prob_ = np.log(smoothed_fc) - np.log(smoothed_cc)

        return self

    def _joint_log_likelihood(self, X: np.ndarray) -> np.ndarray:
        """
        Compute joint log-likelihood P(X, y) for each class

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        log_likelihood : np.ndarray of shape (n_samples, n_classes)
            Log-likelihood for each sample and class
        """
        # Log likelihood = log prior + sum(feature_count * log feature_prob)
        log_likelihood = np.log(self.class_priors_) + X @ self.feature_log_prob_.T
        return log_likelihood

    def predict_log_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Compute log probabilities of samples for each class

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        log_proba : np.ndarray of shape (n_samples, n_classes)
            Log probabilities
        """
        if self.classes_ is None:
            raise ValueError("Model must be fitted before prediction")

        X = np.asarray(X)

        # Compute joint log-likelihood
        log_likelihood = self._joint_log_likelihood(X)

        # Normalize to get posterior probabilities
        log_proba = log_likelihood - logsumexp(log_likelihood, axis=1, keepdims=True)

        return log_proba

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Compute probabilities of samples for each class

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        proba : np.ndarray of shape (n_samples, n_classes)
            Probabilities
        """
        return np.exp(self.predict_log_proba(X))

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        y_pred : np.ndarray of shape (n_samples,)
            Predicted class labels
        """
        log_proba = self.predict_log_proba(X)
        return self.classes_[np.argmax(log_proba, axis=1)]

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute accuracy score"""
        y_pred = self.predict(X)
        return np.mean(y_pred == y)


class BernoulliNB:
    """
    Bernoulli Naive Bayes classifier

    Suitable for binary/boolean features (e.g., word presence/absence).

    Parameters:
    -----------
    alpha : float, default=1.0
        Additive (Laplace/Lidstone) smoothing parameter
    binarize : float or None, default=0.0
        Threshold for binarizing features (None to assume already binary)
    fit_prior : bool, default=True
        Whether to learn class prior probabilities
    class_prior : np.ndarray, optional
        Prior probabilities of the classes
    """

    def __init__(
        self,
        alpha: float = 1.0,
        binarize: Optional[float] = 0.0,
        fit_prior: bool = True,
        class_prior: Optional[np.ndarray] = None
    ):
        self.alpha = alpha
        self.binarize = binarize
        self.fit_prior = fit_prior
        self.class_prior = class_prior

        # Will be set during fit
        self.classes_ = None
        self.class_priors_ = None
        self.feature_log_prob_ = None
        self.n_features_ = None

    def _binarize_X(self, X: np.ndarray) -> np.ndarray:
        """Binarize features if needed"""
        if self.binarize is not None:
            return (X > self.binarize).astype(np.float64)
        return X

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BernoulliNB':
        """
        Fit Bernoulli Naive Bayes

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Training features
        y : np.ndarray of shape (n_samples,)
            Target values

        Returns:
        --------
        self : BernoulliNB
            Fitted estimator
        """
        X = np.asarray(X)
        y = np.asarray(y)

        # Binarize features
        X = self._binarize_X(X)

        n_samples, n_features = X.shape
        self.n_features_ = n_features

        # Get unique classes
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)

        # Initialize parameters
        self.feature_log_prob_ = np.zeros((n_classes, n_features))
        self.class_priors_ = np.zeros(n_classes)

        # Calculate statistics for each class
        for idx, class_val in enumerate(self.classes_):
            mask = y == class_val
            X_class = X[mask]
            n_class_samples = np.sum(mask)

            # Calculate prior
            if self.fit_prior:
                if self.class_prior is not None:
                    self.class_priors_[idx] = self.class_prior[idx]
                else:
                    self.class_priors_[idx] = n_class_samples / n_samples
            else:
                self.class_priors_[idx] = 1.0 / n_classes

            # Calculate feature probabilities with smoothing
            feature_count = X_class.sum(axis=0)
            smoothed_fc = feature_count + self.alpha
            smoothed_cc = n_class_samples + 2 * self.alpha

            # Log probabilities of features being 1 given class
            self.feature_log_prob_[idx] = np.log(smoothed_fc / smoothed_cc)

        return self

    def _joint_log_likelihood(self, X: np.ndarray) -> np.ndarray:
        """
        Compute joint log-likelihood P(X, y) for each class

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        log_likelihood : np.ndarray of shape (n_samples, n_classes)
            Log-likelihood for each sample and class
        """
        X = self._binarize_X(X)
        n_classes = len(self.classes_)

        # Compute log probabilities
        # P(x_i=1|y) when x_i=1 and P(x_i=0|y) = 1 - P(x_i=1|y) when x_i=0
        neg_prob = np.log(1 - np.exp(self.feature_log_prob_))

        # Joint log-likelihood
        log_likelihood = np.log(self.class_priors_) + X @ self.feature_log_prob_.T
        log_likelihood += (1 - X) @ neg_prob.T

        return log_likelihood

    def predict_log_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Compute log probabilities of samples for each class

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        log_proba : np.ndarray of shape (n_samples, n_classes)
            Log probabilities
        """
        if self.classes_ is None:
            raise ValueError("Model must be fitted before prediction")

        X = np.asarray(X)

        # Compute joint log-likelihood
        log_likelihood = self._joint_log_likelihood(X)

        # Normalize to get posterior probabilities
        log_proba = log_likelihood - logsumexp(log_likelihood, axis=1, keepdims=True)

        return log_proba

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Compute probabilities of samples for each class

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        proba : np.ndarray of shape (n_samples, n_classes)
            Probabilities
        """
        return np.exp(self.predict_log_proba(X))

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        y_pred : np.ndarray of shape (n_samples,)
            Predicted class labels
        """
        log_proba = self.predict_log_proba(X)
        return self.classes_[np.argmax(log_proba, axis=1)]

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute accuracy score"""
        y_pred = self.predict(X)
        return np.mean(y_pred == y)


class ComplementNB:
    """
    Complement Naive Bayes classifier

    Designed to correct the "severe assumptions" made by standard Multinomial NB.
    Particularly effective for imbalanced datasets.

    Parameters:
    -----------
    alpha : float, default=1.0
        Additive (Laplace/Lidstone) smoothing parameter
    fit_prior : bool, default=True
        Whether to learn class prior probabilities
    norm : bool, default=False
        Whether to perform weight normalization
    """

    def __init__(
        self,
        alpha: float = 1.0,
        fit_prior: bool = True,
        norm: bool = False
    ):
        self.alpha = alpha
        self.fit_prior = fit_prior
        self.norm = norm

        # Will be set during fit
        self.classes_ = None
        self.class_priors_ = None
        self.feature_log_prob_ = None
        self.n_features_ = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'ComplementNB':
        """
        Fit Complement Naive Bayes

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Training features (should be non-negative)
        y : np.ndarray of shape (n_samples,)
            Target values

        Returns:
        --------
        self : ComplementNB
            Fitted estimator
        """
        X = np.asarray(X)
        y = np.asarray(y)

        # Check for negative values
        if np.any(X < 0):
            raise ValueError("Complement NB requires non-negative features")

        n_samples, n_features = X.shape
        self.n_features_ = n_features

        # Get unique classes
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)

        # Initialize parameters
        self.feature_log_prob_ = np.zeros((n_classes, n_features))
        self.class_priors_ = np.zeros(n_classes)

        # Calculate complement counts
        for idx, class_val in enumerate(self.classes_):
            mask = y == class_val

            # Calculate prior
            if self.fit_prior:
                self.class_priors_[idx] = np.sum(mask) / n_samples
            else:
                self.class_priors_[idx] = 1.0 / n_classes

            # Complement: sum features NOT in this class
            complement_mask = ~mask
            complement_count = X[complement_mask].sum(axis=0)

            # Apply smoothing
            smoothed_cc = complement_count + self.alpha
            smoothed_sum = smoothed_cc.sum()

            # Weight calculation (negative because we use complement)
            weights = np.log(smoothed_cc / smoothed_sum)

            # Normalization
            if self.norm:
                weights = weights / np.abs(weights).sum()

            self.feature_log_prob_[idx] = -weights

        return self

    def _joint_log_likelihood(self, X: np.ndarray) -> np.ndarray:
        """
        Compute joint log-likelihood P(X, y) for each class

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        log_likelihood : np.ndarray of shape (n_samples, n_classes)
            Log-likelihood for each sample and class
        """
        # Complement NB decision rule
        log_likelihood = np.log(self.class_priors_) + X @ self.feature_log_prob_.T
        return log_likelihood

    def predict_log_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Compute log probabilities of samples for each class

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        log_proba : np.ndarray of shape (n_samples, n_classes)
            Log probabilities
        """
        if self.classes_ is None:
            raise ValueError("Model must be fitted before prediction")

        X = np.asarray(X)

        # Compute joint log-likelihood
        log_likelihood = self._joint_log_likelihood(X)

        # Normalize to get posterior probabilities
        log_proba = log_likelihood - logsumexp(log_likelihood, axis=1, keepdims=True)

        return log_proba

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Compute probabilities of samples for each class

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        proba : np.ndarray of shape (n_samples, n_classes)
            Probabilities
        """
        return np.exp(self.predict_log_proba(X))

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        Returns:
        --------
        y_pred : np.ndarray of shape (n_samples,)
            Predicted class labels
        """
        log_proba = self.predict_log_proba(X)
        return self.classes_[np.argmax(log_proba, axis=1)]

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute accuracy score"""
        y_pred = self.predict(X)
        return np.mean(y_pred == y)


def generate_classification_data(
    n_samples: int = 300,
    n_features: int = 20,
    n_informative: int = 10,
    n_classes: int = 3,
    random_state: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic classification data

    Parameters:
    -----------
    n_samples : int
        Number of samples
    n_features : int
        Total number of features
    n_informative : int
        Number of informative features
    n_classes : int
        Number of classes
    random_state : int, optional
        Random seed

    Returns:
    --------
    X : np.ndarray
        Features
    y : np.ndarray
        Target labels
    """
    np.random.seed(random_state)

    # Generate informative features
    X = np.random.randn(n_samples, n_features)

    # Create class centers for informative features
    centers = np.random.randn(n_classes, n_informative) * 2

    # Generate labels
    y = np.random.randint(0, n_classes, n_samples)

    # Make features informative
    for i in range(n_samples):
        X[i, :n_informative] += centers[y[i]]

    # Add noise to non-informative features
    X[:, n_informative:] = np.random.randn(n_samples, n_features - n_informative) * 0.1

    return X, y


def generate_text_data(
    n_samples: int = 200,
    n_features: int = 100,
    n_classes: int = 2,
    random_state: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic text-like data (word counts)

    Parameters:
    -----------
    n_samples : int
        Number of documents
    n_features : int
        Vocabulary size
    n_classes : int
        Number of document classes
    random_state : int, optional
        Random seed

    Returns:
    --------
    X : np.ndarray
        Document-term matrix (counts)
    y : np.ndarray
        Document labels
    """
    np.random.seed(random_state)

    # Generate class-specific word distributions
    word_probs = np.random.dirichlet(np.ones(n_features), n_classes)

    X = np.zeros((n_samples, n_features), dtype=int)
    y = np.random.randint(0, n_classes, n_samples)

    for i in range(n_samples):
        # Sample word counts based on class
        doc_length = np.random.poisson(50) + 10
        words = np.random.choice(n_features, doc_length, p=word_probs[y[i]])
        for word in words:
            X[i, word] += 1

    return X, y


def example_usage():
    """Demonstrate Naive Bayes classifiers"""
    print("Naive Bayes Classifiers Demonstration")
    print("=" * 60)

    np.random.seed(42)

    print("\n1. Gaussian Naive Bayes (Continuous Features)")
    print("-" * 40)

    # Generate continuous data
    X_cont, y_cont = generate_classification_data(
        n_samples=300, n_features=10, n_informative=5, n_classes=3, random_state=42
    )

    # Split data
    n_train = 200
    X_train, X_test = X_cont[:n_train], X_cont[n_train:]
    y_train, y_test = y_cont[:n_train], y_cont[n_train:]

    # Train Gaussian NB
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)

    # Evaluate
    train_acc = gnb.score(X_train, y_train)
    test_acc = gnb.score(X_test, y_test)

    print(f"Training accuracy: {train_acc:.4f}")
    print(f"Testing accuracy: {test_acc:.4f}")

    # Show predictions with probabilities
    sample_idx = 0
    proba = gnb.predict_proba(X_test[sample_idx:sample_idx+1])
    pred = gnb.predict(X_test[sample_idx:sample_idx+1])
    print(f"\nSample prediction:")
    print(f"  True class: {y_test[sample_idx]}")
    print(f"  Predicted class: {pred[0]}")
    print(f"  Class probabilities: {proba[0].round(3)}")

    print("\n2. Multinomial Naive Bayes (Count Features)")
    print("-" * 40)

    # Generate text-like data
    X_text, y_text = generate_text_data(
        n_samples=200, n_features=50, n_classes=2, random_state=42
    )

    # Split data
    n_train = 150
    X_train, X_test = X_text[:n_train], X_text[n_train:]
    y_train, y_test = y_text[:n_train], y_text[n_train:]

    # Train Multinomial NB
    mnb = MultinomialNB(alpha=1.0)
    mnb.fit(X_train, y_train)

    # Evaluate
    train_acc = mnb.score(X_train, y_train)
    test_acc = mnb.score(X_test, y_test)

    print(f"Training accuracy: {train_acc:.4f}")
    print(f"Testing accuracy: {test_acc:.4f}")

    # Feature importance (most predictive words)
    feature_log_prob_diff = mnb.feature_log_prob_[1] - mnb.feature_log_prob_[0]
    top_features = np.argsort(np.abs(feature_log_prob_diff))[-5:]
    print(f"Most discriminative features: {top_features}")

    print("\n3. Bernoulli Naive Bayes (Binary Features)")
    print("-" * 40)

    # Convert to binary features
    X_binary = (X_text > 0).astype(int)
    X_train, X_test = X_binary[:n_train], X_binary[n_train:]

    # Train Bernoulli NB
    bnb = BernoulliNB(alpha=1.0)
    bnb.fit(X_train, y_train)

    # Evaluate
    train_acc = bnb.score(X_train, y_train)
    test_acc = bnb.score(X_test, y_test)

    print(f"Training accuracy: {train_acc:.4f}")
    print(f"Testing accuracy: {test_acc:.4f}")

    print("\n4. Complement Naive Bayes (Imbalanced Data)")
    print("-" * 40)

    # Create imbalanced dataset
    imbalanced_mask = np.concatenate([
        np.ones(140, dtype=bool),  # Keep most of class 0
        np.random.choice([True, False], 60, p=[0.2, 0.8])  # Keep few of class 1
    ])
    X_imbalanced = X_text[imbalanced_mask]
    y_imbalanced = y_text[imbalanced_mask]

    n_train = int(0.75 * len(X_imbalanced))
    X_train, X_test = X_imbalanced[:n_train], X_imbalanced[n_train:]
    y_train, y_test = y_imbalanced[:n_train], y_imbalanced[n_train:]

    print(f"Class distribution in training: {np.bincount(y_train)}")

    # Compare Multinomial and Complement NB
    mnb = MultinomialNB(alpha=1.0)
    mnb.fit(X_train, y_train)

    cnb = ComplementNB(alpha=1.0)
    cnb.fit(X_train, y_train)

    print(f"Multinomial NB test accuracy: {mnb.score(X_test, y_test):.4f}")
    print(f"Complement NB test accuracy: {cnb.score(X_test, y_test):.4f}")

    print("\n5. Comparison of Smoothing Parameters")
    print("-" * 40)

    alphas = [0.001, 0.01, 0.1, 1.0, 10.0]

    print("Alpha | Gaussian | Multinomial | Bernoulli")
    print("------|----------|-------------|----------")

    for alpha in alphas:
        # Note: GaussianNB uses var_smoothing, not alpha
        gnb = GaussianNB(var_smoothing=alpha)
        gnb.fit(X_cont[:200], y_cont[:200])
        g_score = gnb.score(X_cont[200:], y_cont[200:])

        mnb = MultinomialNB(alpha=alpha)
        mnb.fit(X_text[:150], y_text[:150])
        m_score = mnb.score(X_text[150:], y_text[150:])

        bnb = BernoulliNB(alpha=alpha)
        bnb.fit(X_binary[:150], y_text[:150])
        b_score = bnb.score(X_binary[150:], y_text[150:])

        print(f"{alpha:5.3f} |  {g_score:.4f}  |   {m_score:.4f}   |  {b_score:.4f}")

    print("\n6. Online Learning (Incremental Training)")
    print("-" * 40)

    # Simulate streaming data
    batch_size = 50
    n_batches = 4

    gnb = GaussianNB()

    for batch in range(n_batches):
        start_idx = batch * batch_size
        end_idx = start_idx + batch_size

        X_batch = X_cont[start_idx:end_idx]
        y_batch = y_cont[start_idx:end_idx]

        if batch == 0:
            gnb.fit(X_batch, y_batch)
        else:
            # Partial fit (simplified - real implementation would update incrementally)
            # Here we refit on accumulated data
            X_accumulated = X_cont[:end_idx]
            y_accumulated = y_cont[:end_idx]
            gnb.fit(X_accumulated, y_accumulated)

        acc = gnb.score(X_cont[200:], y_cont[200:])
        print(f"Batch {batch + 1}: Test accuracy = {acc:.4f}")

    print("\n" + "=" * 60)
    print("Naive Bayes demonstration complete!")
    print("\nKey takeaways:")
    print("- Gaussian NB: Best for continuous, normally distributed features")
    print("- Multinomial NB: Ideal for count data (text classification)")
    print("- Bernoulli NB: Suitable for binary/boolean features")
    print("- Complement NB: Better for imbalanced datasets")
    print("- Simple, fast, and effective for high-dimensional data")


if __name__ == "__main__":
    example_usage()