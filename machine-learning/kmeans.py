#!/usr/bin/env python3
"""
K-Means Clustering Implementation

Implements K-Means clustering with various initialization methods:
- Random initialization
- K-Means++ for improved starting centroids
- Mini-batch K-Means for large datasets

Includes utilities for determining optimal K and cluster evaluation.

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import List, Tuple, Optional, Dict, Union
import matplotlib.pyplot as plt
import warnings
from scipy.spatial.distance import cdist


class KMeans:
    """
    K-Means clustering algorithm with multiple initialization methods.

    Partitions data into K clusters by minimizing within-cluster
    sum of squares (inertia).
    """

    def __init__(self,
                 n_clusters: int = 8,
                 init: str = 'k-means++',
                 n_init: int = 10,
                 max_iter: int = 300,
                 tol: float = 1e-4,
                 random_state: Optional[int] = None,
                 verbose: bool = False):
        """
        Initialize K-Means clusterer.

        Args:
            n_clusters: Number of clusters to form
            init: Method for initialization ('k-means++', 'random', or array of centers)
            n_init: Number of time k-means will be run with different seeds
            max_iter: Maximum number of iterations
            tol: Tolerance for convergence
            random_state: Random seed for reproducibility
            verbose: Verbosity mode
        """
        self.n_clusters = n_clusters
        self.init = init
        self.n_init = n_init
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.verbose = verbose

        # Will be set during fit
        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None
        self.n_iter_ = None

    def _init_random(self, X: np.ndarray) -> np.ndarray:
        """Initialize cluster centers randomly from data points"""
        n_samples = X.shape[0]
        indices = self.rng.choice(n_samples, self.n_clusters, replace=False)
        return X[indices].copy()

    def _init_kmeans_plus_plus(self, X: np.ndarray) -> np.ndarray:
        """
        Initialize cluster centers using K-Means++ algorithm.

        K-Means++ chooses initial centers that are far apart to improve
        convergence speed and solution quality.
        """
        n_samples, n_features = X.shape
        centers = np.empty((self.n_clusters, n_features))

        # Choose first center randomly
        center_idx = self.rng.choice(n_samples)
        centers[0] = X[center_idx]

        # Choose remaining centers
        for c in range(1, self.n_clusters):
            # Calculate squared distances to nearest center
            distances = np.array([
                min([np.linalg.norm(x - centers[j])**2 for j in range(c)])
                for x in X
            ])

            # Choose next center with probability proportional to squared distance
            probabilities = distances / distances.sum()
            cumulative_probs = probabilities.cumsum()
            r = self.rng.random()

            for i, p in enumerate(cumulative_probs):
                if r < p:
                    centers[c] = X[i]
                    break

        return centers

    def _assign_clusters(self, X: np.ndarray, centers: np.ndarray) -> np.ndarray:
        """Assign each sample to nearest cluster center"""
        # Calculate distances to all centers
        distances = cdist(X, centers, metric='euclidean')
        # Assign to nearest center
        return np.argmin(distances, axis=1)

    def _update_centers(self, X: np.ndarray, labels: np.ndarray) -> np.ndarray:
        """Update cluster centers as mean of assigned samples"""
        centers = np.zeros((self.n_clusters, X.shape[1]))
        for k in range(self.n_clusters):
            cluster_samples = X[labels == k]
            if len(cluster_samples) > 0:
                centers[k] = cluster_samples.mean(axis=0)
            else:
                # Handle empty cluster by reinitializing randomly
                centers[k] = X[self.rng.choice(X.shape[0])]
        return centers

    def _calculate_inertia(self, X: np.ndarray, labels: np.ndarray, centers: np.ndarray) -> float:
        """Calculate within-cluster sum of squares"""
        inertia = 0.0
        for k in range(self.n_clusters):
            cluster_samples = X[labels == k]
            if len(cluster_samples) > 0:
                inertia += np.sum((cluster_samples - centers[k])**2)
        return inertia

    def _kmeans_single(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float, int]:
        """Run a single K-Means clustering"""
        n_samples = X.shape[0]

        # Initialize centers
        if isinstance(self.init, str):
            if self.init == 'k-means++':
                centers = self._init_kmeans_plus_plus(X)
            elif self.init == 'random':
                centers = self._init_random(X)
            else:
                raise ValueError(f"Unknown init method: {self.init}")
        else:
            # Use provided centers
            centers = np.asarray(self.init).copy()

        # Main K-Means loop
        for iteration in range(self.max_iter):
            # Assign clusters
            labels = self._assign_clusters(X, centers)

            # Update centers
            new_centers = self._update_centers(X, labels)

            # Check convergence
            center_shift = np.linalg.norm(new_centers - centers)
            if self.verbose:
                print(f"Iteration {iteration}: center shift = {center_shift:.6f}")

            if center_shift < self.tol:
                if self.verbose:
                    print(f"Converged at iteration {iteration}")
                break

            centers = new_centers

        # Calculate final inertia
        inertia = self._calculate_inertia(X, labels, centers)

        return centers, labels, inertia, iteration + 1

    def fit(self, X: np.ndarray) -> 'KMeans':
        """
        Fit K-Means clustering to data.

        Args:
            X: Data to cluster of shape (n_samples, n_features)

        Returns:
            Self for method chaining
        """
        X = np.asarray(X)
        n_samples, n_features = X.shape

        if n_samples < self.n_clusters:
            raise ValueError(f"n_samples={n_samples} should be >= n_clusters={self.n_clusters}")

        # Set random state
        self.rng = np.random.RandomState(self.random_state)

        # Run K-Means multiple times and keep best result
        best_inertia = np.inf
        best_centers = None
        best_labels = None
        best_n_iter = None

        for run in range(self.n_init):
            if self.verbose and self.n_init > 1:
                print(f"\nRun {run + 1}/{self.n_init}")

            centers, labels, inertia, n_iter = self._kmeans_single(X)

            if inertia < best_inertia:
                best_inertia = inertia
                best_centers = centers
                best_labels = labels
                best_n_iter = n_iter

        self.cluster_centers_ = best_centers
        self.labels_ = best_labels
        self.inertia_ = best_inertia
        self.n_iter_ = best_n_iter

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict cluster labels for new samples.

        Args:
            X: New samples of shape (n_samples, n_features)

        Returns:
            Cluster labels for each sample
        """
        if self.cluster_centers_ is None:
            raise ValueError("Model must be fitted before predicting")

        X = np.asarray(X)
        return self._assign_clusters(X, self.cluster_centers_)

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """
        Fit model and predict cluster labels.

        Args:
            X: Data to cluster

        Returns:
            Cluster labels
        """
        self.fit(X)
        return self.labels_

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform X to cluster-distance space.

        Args:
            X: Data to transform

        Returns:
            Distances to cluster centers
        """
        if self.cluster_centers_ is None:
            raise ValueError("Model must be fitted before transforming")

        X = np.asarray(X)
        return cdist(X, self.cluster_centers_, metric='euclidean')


class MiniBatchKMeans:
    """
    Mini-Batch K-Means clustering for large datasets.

    Uses small random batches to update centers, trading accuracy
    for speed.
    """

    def __init__(self,
                 n_clusters: int = 8,
                 batch_size: int = 100,
                 max_iter: int = 100,
                 n_init: int = 3,
                 random_state: Optional[int] = None):
        """
        Initialize Mini-Batch K-Means.

        Args:
            n_clusters: Number of clusters
            batch_size: Size of mini batches
            max_iter: Maximum number of iterations
            n_init: Number of random initializations
            random_state: Random seed
        """
        self.n_clusters = n_clusters
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.n_init = n_init
        self.random_state = random_state

        # Will be set during fit
        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None
        self.counts_ = None  # Number of samples per center

    def fit(self, X: np.ndarray) -> 'MiniBatchKMeans':
        """
        Fit Mini-Batch K-Means to data.

        Args:
            X: Data to cluster

        Returns:
            Self for method chaining
        """
        X = np.asarray(X)
        n_samples, n_features = X.shape
        rng = np.random.RandomState(self.random_state)

        best_inertia = np.inf

        for init in range(self.n_init):
            # Initialize centers with K-Means++
            kmeans_init = KMeans(n_clusters=self.n_clusters,
                                 init='k-means++',
                                 n_init=1,
                                 max_iter=1,
                                 random_state=rng.randint(2**31))
            kmeans_init.fit(X[:min(1000, n_samples)])  # Use subset for initialization
            centers = kmeans_init.cluster_centers_.copy()
            counts = np.zeros(self.n_clusters)

            # Mini-batch iterations
            for iteration in range(self.max_iter):
                # Sample mini-batch
                batch_indices = rng.choice(n_samples, self.batch_size, replace=False)
                batch = X[batch_indices]

                # Assign clusters for batch
                batch_labels = cdist(batch, centers, metric='euclidean').argmin(axis=1)

                # Update centers with batch
                for i, (sample, label) in enumerate(zip(batch, batch_labels)):
                    counts[label] += 1
                    eta = 1.0 / counts[label]  # Learning rate
                    centers[label] = (1 - eta) * centers[label] + eta * sample

            # Calculate final assignments and inertia
            labels = cdist(X, centers, metric='euclidean').argmin(axis=1)
            inertia = 0.0
            for k in range(self.n_clusters):
                cluster_samples = X[labels == k]
                if len(cluster_samples) > 0:
                    inertia += np.sum((cluster_samples - centers[k])**2)

            if inertia < best_inertia:
                best_inertia = inertia
                self.cluster_centers_ = centers
                self.labels_ = labels
                self.inertia_ = inertia
                self.counts_ = counts

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict cluster labels for new samples"""
        if self.cluster_centers_ is None:
            raise ValueError("Model must be fitted before predicting")

        X = np.asarray(X)
        return cdist(X, self.cluster_centers_, metric='euclidean').argmin(axis=1)


def elbow_method(X: np.ndarray,
                 k_range: range = range(2, 11),
                 random_state: Optional[int] = None,
                 plot: bool = True) -> Dict[int, float]:
    """
    Find optimal number of clusters using elbow method.

    Args:
        X: Data to cluster
        k_range: Range of K values to test
        random_state: Random seed
        plot: Whether to plot the elbow curve

    Returns:
        Dictionary mapping K to inertia
    """
    inertias = {}

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=random_state)
        kmeans.fit(X)
        inertias[k] = kmeans.inertia_

    if plot:
        plt.figure(figsize=(10, 6))
        plt.plot(list(inertias.keys()), list(inertias.values()), 'bo-')
        plt.xlabel('Number of Clusters (K)')
        plt.ylabel('Within-cluster Sum of Squares (Inertia)')
        plt.title('Elbow Method for Optimal K')
        plt.grid(True, alpha=0.3)
        plt.show()

    return inertias


def silhouette_score(X: np.ndarray, labels: np.ndarray) -> float:
    """
    Calculate silhouette coefficient for clustering quality.

    The silhouette coefficient is a measure of how similar a sample is
    to its own cluster compared to other clusters.

    Args:
        X: Data samples
        labels: Cluster labels

    Returns:
        Mean silhouette coefficient (between -1 and 1, higher is better)
    """
    n_samples = X.shape[0]
    n_clusters = len(np.unique(labels))

    if n_clusters == 1:
        return 0.0

    silhouette_scores = np.zeros(n_samples)

    for i in range(n_samples):
        # a(i): mean distance to samples in same cluster
        same_cluster = X[labels == labels[i]]
        if len(same_cluster) > 1:
            a = np.mean([np.linalg.norm(X[i] - x) for x in same_cluster if not np.array_equal(X[i], x)])
        else:
            a = 0

        # b(i): mean distance to samples in nearest different cluster
        b = np.inf
        for k in range(n_clusters):
            if k != labels[i]:
                other_cluster = X[labels == k]
                if len(other_cluster) > 0:
                    mean_dist = np.mean([np.linalg.norm(X[i] - x) for x in other_cluster])
                    b = min(b, mean_dist)

        # Silhouette coefficient
        if max(a, b) == 0:
            silhouette_scores[i] = 0
        else:
            silhouette_scores[i] = (b - a) / max(a, b)

    return np.mean(silhouette_scores)


def generate_blob_data(n_samples: int = 300,
                      n_features: int = 2,
                      n_clusters: int = 3,
                      random_state: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate isotropic Gaussian blobs for clustering.

    Args:
        n_samples: Total number of samples
        n_features: Number of features
        n_clusters: Number of clusters
        random_state: Random seed

    Returns:
        X: Generated samples
        y: True cluster labels
    """
    rng = np.random.RandomState(random_state)

    # Generate cluster centers
    centers = rng.randn(n_clusters, n_features) * 3

    # Generate samples
    samples_per_cluster = n_samples // n_clusters
    X = []
    y = []

    for i in range(n_clusters):
        cluster_samples = rng.randn(samples_per_cluster, n_features) * 0.5 + centers[i]
        X.append(cluster_samples)
        y.extend([i] * samples_per_cluster)

    # Handle remaining samples
    remaining = n_samples - (samples_per_cluster * n_clusters)
    if remaining > 0:
        i = rng.choice(n_clusters)
        cluster_samples = rng.randn(remaining, n_features) * 0.5 + centers[i]
        X.append(cluster_samples)
        y.extend([i] * remaining)

    X = np.vstack(X)
    y = np.array(y)

    # Shuffle
    indices = rng.permutation(n_samples)
    return X[indices], y[indices]


def visualize_clusters(X: np.ndarray, labels: np.ndarray, centers: np.ndarray = None,
                      title: str = "K-Means Clustering"):
    """
    Visualize 2D clustering results.

    Args:
        X: Data samples (2D)
        labels: Cluster labels
        centers: Cluster centers
        title: Plot title
    """
    if X.shape[1] != 2:
        print("Visualization requires 2D data")
        return

    plt.figure(figsize=(10, 8))

    # Plot samples
    unique_labels = np.unique(labels)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))

    for k, col in zip(unique_labels, colors):
        cluster_samples = X[labels == k]
        plt.scatter(cluster_samples[:, 0], cluster_samples[:, 1],
                   c=[col], label=f'Cluster {k}', alpha=0.6, s=30)

    # Plot centers
    if centers is not None:
        plt.scatter(centers[:, 0], centers[:, 1],
                   c='black', marker='x', s=200, linewidths=3,
                   label='Centers')

    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def demonstrate_kmeans():
    """Demonstrate K-Means clustering"""
    print("=" * 60)
    print("K-Means Clustering Demonstration")
    print("=" * 60)

    # Generate sample data
    np.random.seed(42)
    X, y_true = generate_blob_data(n_samples=300, n_features=2,
                                   n_clusters=3, random_state=42)

    # 1. Standard K-Means
    print("\n1. Standard K-Means Clustering")
    print("-" * 40)

    kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
    kmeans.fit(X)

    print(f"Number of iterations: {kmeans.n_iter_}")
    print(f"Inertia: {kmeans.inertia_:.2f}")

    # Calculate metrics
    sil_score = silhouette_score(X, kmeans.labels_)
    print(f"Silhouette score: {sil_score:.3f}")

    # Visualize
    visualize_clusters(X, kmeans.labels_, kmeans.cluster_centers_,
                      "K-Means Clustering (K=3)")

    # 2. Compare initialization methods
    print("\n2. Comparison of Initialization Methods")
    print("-" * 40)

    methods = ['random', 'k-means++']
    for method in methods:
        km = KMeans(n_clusters=3, init=method, n_init=10, random_state=42)
        km.fit(X)
        print(f"{method:12s}: Inertia = {km.inertia_:.2f}, Iterations = {km.n_iter_}")

    # 3. Elbow Method
    print("\n3. Elbow Method for Optimal K")
    print("-" * 40)

    inertias = elbow_method(X, k_range=range(2, 9), random_state=42, plot=False)
    for k, inertia in inertias.items():
        print(f"K={k}: Inertia = {inertia:.2f}")

    # 4. Mini-Batch K-Means
    print("\n4. Mini-Batch K-Means (for large datasets)")
    print("-" * 40)

    mb_kmeans = MiniBatchKMeans(n_clusters=3, batch_size=50, random_state=42)
    mb_kmeans.fit(X)

    print(f"Mini-Batch Inertia: {mb_kmeans.inertia_:.2f}")
    mb_sil_score = silhouette_score(X, mb_kmeans.labels_)
    print(f"Mini-Batch Silhouette score: {mb_sil_score:.3f}")

    # 5. Different numbers of clusters
    print("\n5. Clustering Quality vs Number of Clusters")
    print("-" * 40)

    for k in range(2, 6):
        km = KMeans(n_clusters=k, random_state=42)
        km.fit(X)
        sil = silhouette_score(X, km.labels_)
        print(f"K={k}: Silhouette = {sil:.3f}, Inertia = {km.inertia_:.2f}")

    # 6. Prediction on new data
    print("\n6. Predicting Cluster for New Samples")
    print("-" * 40)

    new_samples = np.array([[0, 0], [5, 5], [-3, 2]])
    predictions = kmeans.predict(new_samples)
    distances = kmeans.transform(new_samples)

    for i, (sample, pred) in enumerate(zip(new_samples, predictions)):
        print(f"Sample {sample}: Cluster {pred}, "
              f"Distances = {distances[i].round(2)}")


if __name__ == "__main__":
    demonstrate_kmeans()