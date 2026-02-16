#!/usr/bin/env python3
"""
K-Means Clustering Algorithm with K-Means++ Initialization

This module implements the K-Means clustering algorithm with multiple initialization methods:
- Random initialization
- K-Means++ initialization (Arthur & Vassilvitskii, 2007)
- K-Means|| initialization (scalable K-Means++)

K-Means is an unsupervised learning algorithm that partitions n observations into k clusters
where each observation belongs to the cluster with the nearest mean (cluster center).

Features:
- Multiple initialization methods for better convergence
- Elbow method for optimal K selection
- Silhouette score for cluster quality assessment
- Mini-batch K-Means for large datasets
- Fuzzy C-Means for soft clustering

Applications:
- Customer segmentation
- Image compression
- Document clustering
- Anomaly detection
- Feature learning

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import Optional, Tuple, List, Dict, Union
from dataclasses import dataclass
import warnings
from scipy.spatial.distance import cdist
import time


@dataclass
class KMeansResult:
    """Results from K-Means clustering"""
    centroids: np.ndarray  # Final cluster centers
    labels: np.ndarray  # Cluster assignments
    inertia: float  # Within-cluster sum of squares
    n_iterations: int  # Number of iterations until convergence
    converged: bool  # Whether the algorithm converged


class KMeans:
    """
    K-Means Clustering Algorithm

    Parameters:
    -----------
    n_clusters : int
        Number of clusters to form
    init : str or np.ndarray, default='k-means++'
        Method for initialization:
        - 'random': Random selection of k points
        - 'k-means++': Smart initialization for faster convergence
        - 'k-means||': Scalable k-means++ for large datasets
        - array: Custom initial centroids
    n_init : int, default=10
        Number of times to run with different centroid seeds
    max_iter : int, default=300
        Maximum number of iterations
    tol : float, default=1e-4
        Tolerance for convergence
    random_state : int, optional
        Random seed for reproducibility
    verbose : bool, default=False
        Whether to print progress
    algorithm : str, default='lloyd'
        K-means algorithm to use ('lloyd' or 'elkan')
    """

    def __init__(
        self,
        n_clusters: int,
        init: Union[str, np.ndarray] = 'k-means++',
        n_init: int = 10,
        max_iter: int = 300,
        tol: float = 1e-4,
        random_state: Optional[int] = None,
        verbose: bool = False,
        algorithm: str = 'lloyd'
    ):
        self.n_clusters = n_clusters
        self.init = init
        self.n_init = n_init
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.verbose = verbose
        self.algorithm = algorithm

        self.centroids_ = None
        self.labels_ = None
        self.inertia_ = None
        self.n_iter_ = None

        if random_state is not None:
            np.random.seed(random_state)

    def fit(self, X: np.ndarray) -> 'KMeans':
        """
        Fit K-Means clustering

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Training data

        Returns:
        --------
        self : KMeans
            Fitted estimator
        """
        X = np.asarray(X)
        n_samples, n_features = X.shape

        if self.n_clusters > n_samples:
            raise ValueError(f"n_clusters ({self.n_clusters}) cannot be greater than n_samples ({n_samples})")

        best_result = None
        best_inertia = np.inf

        # Run multiple times with different initializations
        for run in range(self.n_init if isinstance(self.init, str) else 1):
            if self.verbose:
                print(f"Initialization {run + 1}/{self.n_init}")

            # Initialize centroids
            if isinstance(self.init, str):
                if self.init == 'random':
                    centroids = self._init_random(X)
                elif self.init == 'k-means++':
                    centroids = self._init_kmeans_plus_plus(X)
                elif self.init == 'k-means||':
                    centroids = self._init_kmeans_parallel(X)
                else:
                    raise ValueError(f"Unknown init method: {self.init}")
            else:
                centroids = np.asarray(self.init).copy()

            # Run K-Means
            if self.algorithm == 'lloyd':
                result = self._lloyd_algorithm(X, centroids)
            elif self.algorithm == 'elkan':
                result = self._elkan_algorithm(X, centroids)
            else:
                raise ValueError(f"Unknown algorithm: {self.algorithm}")

            # Keep best result
            if result.inertia < best_inertia:
                best_inertia = result.inertia
                best_result = result

        # Store best result
        self.centroids_ = best_result.centroids
        self.labels_ = best_result.labels
        self.inertia_ = best_result.inertia
        self.n_iter_ = best_result.n_iterations

        return self

    def _init_random(self, X: np.ndarray) -> np.ndarray:
        """Random initialization"""
        n_samples = X.shape[0]
        indices = np.random.choice(n_samples, self.n_clusters, replace=False)
        return X[indices].copy()

    def _init_kmeans_plus_plus(self, X: np.ndarray) -> np.ndarray:
        """
        K-Means++ initialization

        Algorithm:
        1. Choose first center randomly
        2. For each remaining center:
           - Compute distance from each point to nearest center
           - Choose next center with probability proportional to distance^2
        """
        n_samples = X.shape[0]
        centroids = []

        # Choose first center randomly
        first_idx = np.random.randint(n_samples)
        centroids.append(X[first_idx])

        # Choose remaining centers
        for _ in range(1, self.n_clusters):
            # Compute distances to nearest center
            distances = np.min(cdist(X, np.array(centroids), 'euclidean'), axis=1)

            # Choose next center with probability proportional to distance^2
            probabilities = distances ** 2
            probabilities /= probabilities.sum()

            # Sample next center
            next_idx = np.random.choice(n_samples, p=probabilities)
            centroids.append(X[next_idx])

        return np.array(centroids)

    def _init_kmeans_parallel(self, X: np.ndarray, oversampling_factor: int = 2) -> np.ndarray:
        """
        K-Means|| initialization (scalable K-Means++)

        Algorithm:
        1. Sample initial center
        2. For log(n) iterations:
           - Sample l = k * oversampling_factor points proportional to distance^2
        3. Run K-Means++ on sampled points to get final k centers
        """
        n_samples = X.shape[0]
        l = self.n_clusters * oversampling_factor

        # Initial center
        first_idx = np.random.randint(n_samples)
        centers = [X[first_idx]]

        # Oversampling phase
        n_iterations = int(np.log(n_samples))
        for _ in range(n_iterations):
            # Compute distances to nearest center
            distances = np.min(cdist(X, np.array(centers), 'euclidean'), axis=1)

            # Sample l points proportional to distance^2
            probabilities = distances ** 2
            if probabilities.sum() > 0:
                probabilities /= probabilities.sum()
                sampled_indices = np.random.choice(n_samples, min(l, n_samples),
                                                 replace=False, p=probabilities)
                centers.extend(X[sampled_indices])

        # Reduce to k centers using K-Means++
        centers = np.array(centers)
        if len(centers) > self.n_clusters:
            # Run K-Means on the oversampled centers
            temp_kmeans = KMeans(n_clusters=self.n_clusters, init='k-means++', n_init=1)
            temp_kmeans.fit(centers)
            return temp_kmeans.centroids_
        else:
            return centers

    def _lloyd_algorithm(self, X: np.ndarray, initial_centroids: np.ndarray) -> KMeansResult:
        """
        Lloyd's algorithm (standard K-Means)

        Algorithm:
        1. Assign each point to nearest centroid
        2. Update centroids as mean of assigned points
        3. Repeat until convergence
        """
        centroids = initial_centroids.copy()
        n_samples = X.shape[0]

        labels = np.zeros(n_samples, dtype=int)
        prev_labels = None

        for iteration in range(self.max_iter):
            # Assignment step: assign each point to nearest centroid
            distances = cdist(X, centroids, 'euclidean')
            labels = np.argmin(distances, axis=1)

            # Check for convergence
            if prev_labels is not None and np.array_equal(labels, prev_labels):
                converged = True
                break

            prev_labels = labels.copy()

            # Update step: compute new centroids
            for k in range(self.n_clusters):
                mask = labels == k
                if np.any(mask):
                    centroids[k] = X[mask].mean(axis=0)
                # If no points assigned, reinitialize centroid
                else:
                    centroids[k] = X[np.random.randint(n_samples)]

            if self.verbose and iteration % 10 == 0:
                inertia = self._compute_inertia(X, labels, centroids)
                print(f"  Iteration {iteration}: inertia = {inertia:.4f}")
        else:
            converged = False
            if self.verbose:
                print(f"  Warning: Did not converge in {self.max_iter} iterations")

        # Compute final inertia
        inertia = self._compute_inertia(X, labels, centroids)

        return KMeansResult(
            centroids=centroids,
            labels=labels,
            inertia=inertia,
            n_iterations=iteration + 1,
            converged=converged
        )

    def _elkan_algorithm(self, X: np.ndarray, initial_centroids: np.ndarray) -> KMeansResult:
        """
        Elkan's algorithm (accelerated K-Means using triangle inequality)

        More efficient for low-dimensional data by avoiding unnecessary distance calculations
        """
        # For simplicity, fallback to Lloyd's algorithm
        # Full Elkan implementation requires additional bookkeeping
        return self._lloyd_algorithm(X, initial_centroids)

    def _compute_inertia(self, X: np.ndarray, labels: np.ndarray, centroids: np.ndarray) -> float:
        """Compute within-cluster sum of squares"""
        inertia = 0.0
        for k in range(self.n_clusters):
            mask = labels == k
            if np.any(mask):
                cluster_points = X[mask]
                distances = np.linalg.norm(cluster_points - centroids[k], axis=1)
                inertia += np.sum(distances ** 2)
        return inertia

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict cluster labels for new data

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            New data to predict

        Returns:
        --------
        labels : np.ndarray of shape (n_samples,)
            Cluster labels
        """
        if self.centroids_ is None:
            raise ValueError("Model must be fitted before prediction")

        X = np.asarray(X)
        distances = cdist(X, self.centroids_, 'euclidean')
        return np.argmin(distances, axis=1)

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit and return cluster labels"""
        self.fit(X)
        return self.labels_

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform X to cluster-distance space

        Returns distance from each sample to each cluster center
        """
        if self.centroids_ is None:
            raise ValueError("Model must be fitted before transform")

        X = np.asarray(X)
        return cdist(X, self.centroids_, 'euclidean')

    def score(self, X: np.ndarray) -> float:
        """
        Return negative inertia (higher is better)

        Compatible with sklearn's scoring convention
        """
        labels = self.predict(X)
        inertia = self._compute_inertia(X, labels, self.centroids_)
        return -inertia


class MiniBatchKMeans:
    """
    Mini-Batch K-Means for large datasets

    Uses small random batches to update centroids, trading accuracy for speed

    Parameters:
    -----------
    n_clusters : int
        Number of clusters
    batch_size : int, default=100
        Size of mini-batches
    max_iter : int, default=100
        Maximum number of iterations
    n_init : int, default=3
        Number of initializations
    init : str, default='k-means++'
        Initialization method
    random_state : int, optional
        Random seed
    """

    def __init__(
        self,
        n_clusters: int,
        batch_size: int = 100,
        max_iter: int = 100,
        n_init: int = 3,
        init: str = 'k-means++',
        random_state: Optional[int] = None
    ):
        self.n_clusters = n_clusters
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.n_init = n_init
        self.init = init
        self.random_state = random_state

        self.centroids_ = None
        self.labels_ = None
        self.counts_ = None  # Number of points per cluster

        if random_state is not None:
            np.random.seed(random_state)

    def fit(self, X: np.ndarray) -> 'MiniBatchKMeans':
        """
        Fit Mini-Batch K-Means

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Training data

        Returns:
        --------
        self : MiniBatchKMeans
            Fitted estimator
        """
        X = np.asarray(X)
        n_samples, n_features = X.shape

        best_inertia = np.inf
        best_centroids = None

        for run in range(self.n_init):
            # Initialize using regular K-Means
            init_kmeans = KMeans(n_clusters=self.n_clusters, init=self.init, n_init=1)
            sample_size = min(n_samples, max(self.n_clusters * 10, 1000))
            sample_indices = np.random.choice(n_samples, sample_size, replace=False)
            init_kmeans.fit(X[sample_indices])

            centroids = init_kmeans.centroids_
            counts = np.ones(self.n_clusters)

            # Mini-batch updates
            for iteration in range(self.max_iter):
                # Sample mini-batch
                batch_indices = np.random.choice(n_samples, self.batch_size, replace=True)
                batch = X[batch_indices]

                # Assign batch to clusters
                distances = cdist(batch, centroids, 'euclidean')
                batch_labels = np.argmin(distances, axis=1)

                # Update centroids with learning rate
                for i, (point, label) in enumerate(zip(batch, batch_labels)):
                    counts[label] += 1
                    learning_rate = 1.0 / counts[label]
                    centroids[label] = (1 - learning_rate) * centroids[label] + learning_rate * point

            # Compute final inertia
            labels = np.argmin(cdist(X, centroids, 'euclidean'), axis=1)
            inertia = 0.0
            for k in range(self.n_clusters):
                mask = labels == k
                if np.any(mask):
                    cluster_points = X[mask]
                    distances = np.linalg.norm(cluster_points - centroids[k], axis=1)
                    inertia += np.sum(distances ** 2)

            if inertia < best_inertia:
                best_inertia = inertia
                best_centroids = centroids
                self.counts_ = counts

        self.centroids_ = best_centroids
        self.labels_ = np.argmin(cdist(X, self.centroids_, 'euclidean'), axis=1)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict cluster labels"""
        if self.centroids_ is None:
            raise ValueError("Model must be fitted before prediction")

        X = np.asarray(X)
        distances = cdist(X, self.centroids_, 'euclidean')
        return np.argmin(distances, axis=1)


class FuzzyCMeans:
    """
    Fuzzy C-Means Clustering (Soft Clustering)

    Each point has membership degree to each cluster rather than hard assignment

    Parameters:
    -----------
    n_clusters : int
        Number of clusters
    fuzziness : float, default=2.0
        Fuzziness parameter (m > 1). Higher values give fuzzier clusters
    max_iter : int, default=300
        Maximum iterations
    tol : float, default=1e-4
        Convergence tolerance
    random_state : int, optional
        Random seed
    """

    def __init__(
        self,
        n_clusters: int,
        fuzziness: float = 2.0,
        max_iter: int = 300,
        tol: float = 1e-4,
        random_state: Optional[int] = None
    ):
        if fuzziness <= 1:
            raise ValueError("Fuzziness parameter must be > 1")

        self.n_clusters = n_clusters
        self.fuzziness = fuzziness
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state

        self.centroids_ = None
        self.membership_ = None

        if random_state is not None:
            np.random.seed(random_state)

    def fit(self, X: np.ndarray) -> 'FuzzyCMeans':
        """
        Fit Fuzzy C-Means clustering

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Training data

        Returns:
        --------
        self : FuzzyCMeans
            Fitted estimator
        """
        X = np.asarray(X)
        n_samples, n_features = X.shape

        # Initialize membership matrix randomly
        membership = np.random.rand(n_samples, self.n_clusters)
        membership /= membership.sum(axis=1, keepdims=True)

        for iteration in range(self.max_iter):
            # Update centroids
            membership_weighted = membership ** self.fuzziness
            centroids = membership_weighted.T @ X / membership_weighted.sum(axis=0, keepdims=True).T

            # Update membership matrix
            distances = cdist(X, centroids, 'euclidean')

            # Handle zero distances
            zero_distances = distances == 0
            if np.any(zero_distances):
                # Points exactly at centroids get membership 1
                new_membership = np.zeros_like(membership)
                for i in range(n_samples):
                    zero_mask = zero_distances[i]
                    if np.any(zero_mask):
                        new_membership[i, zero_mask] = 1.0 / zero_mask.sum()
                    else:
                        # Standard FCM update
                        power = 2 / (self.fuzziness - 1)
                        new_membership[i] = 1 / np.sum((distances[i:i+1] / distances[i]) ** power, axis=1)
            else:
                # Standard FCM update
                power = 2 / (self.fuzziness - 1)
                new_membership = np.zeros_like(membership)
                for i in range(n_samples):
                    for j in range(self.n_clusters):
                        new_membership[i, j] = 1 / np.sum((distances[i, j] / distances[i]) ** power)

            # Check convergence
            if np.max(np.abs(new_membership - membership)) < self.tol:
                break

            membership = new_membership

        self.centroids_ = centroids
        self.membership_ = membership

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict crisp cluster labels (highest membership)

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Data to predict

        Returns:
        --------
        labels : np.ndarray of shape (n_samples,)
            Cluster labels
        """
        membership = self.predict_proba(X)
        return np.argmax(membership, axis=1)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict membership degrees for new data

        Parameters:
        -----------
        X : np.ndarray of shape (n_samples, n_features)
            Data to predict

        Returns:
        --------
        membership : np.ndarray of shape (n_samples, n_clusters)
            Membership degrees
        """
        if self.centroids_ is None:
            raise ValueError("Model must be fitted before prediction")

        X = np.asarray(X)
        n_samples = X.shape[0]

        distances = cdist(X, self.centroids_, 'euclidean')
        membership = np.zeros((n_samples, self.n_clusters))

        # Handle zero distances
        zero_distances = distances == 0

        for i in range(n_samples):
            zero_mask = zero_distances[i]
            if np.any(zero_mask):
                membership[i, zero_mask] = 1.0 / zero_mask.sum()
            else:
                power = 2 / (self.fuzziness - 1)
                for j in range(self.n_clusters):
                    membership[i, j] = 1 / np.sum((distances[i, j] / distances[i]) ** power)

        return membership


def elbow_method(X: np.ndarray, k_range: range, **kwargs) -> Dict[str, Union[List[int], List[float]]]:
    """
    Elbow method for determining optimal number of clusters

    Parameters:
    -----------
    X : np.ndarray
        Data to cluster
    k_range : range
        Range of k values to test
    **kwargs : dict
        Additional arguments for KMeans

    Returns:
    --------
    results : dict
        Dictionary with 'k_values' and 'inertias'
    """
    k_values = []
    inertias = []

    for k in k_range:
        kmeans = KMeans(n_clusters=k, **kwargs)
        kmeans.fit(X)
        k_values.append(k)
        inertias.append(kmeans.inertia_)

    return {'k_values': k_values, 'inertias': inertias}


def silhouette_score(X: np.ndarray, labels: np.ndarray) -> float:
    """
    Compute silhouette score for clustering quality

    Score ranges from -1 (worst) to 1 (best)

    Parameters:
    -----------
    X : np.ndarray of shape (n_samples, n_features)
        Data points
    labels : np.ndarray of shape (n_samples,)
        Cluster labels

    Returns:
    --------
    score : float
        Mean silhouette coefficient
    """
    n_samples = X.shape[0]
    unique_labels = np.unique(labels)

    if len(unique_labels) == 1:
        return 0.0

    silhouette_scores = []

    for i in range(n_samples):
        # Compute a(i): mean distance to points in same cluster
        same_cluster = labels == labels[i]
        if np.sum(same_cluster) > 1:
            a_i = np.mean(np.linalg.norm(X[same_cluster] - X[i], axis=1))
        else:
            a_i = 0

        # Compute b(i): min mean distance to points in other clusters
        b_i = np.inf
        for label in unique_labels:
            if label != labels[i]:
                other_cluster = labels == label
                if np.any(other_cluster):
                    mean_dist = np.mean(np.linalg.norm(X[other_cluster] - X[i], axis=1))
                    b_i = min(b_i, mean_dist)

        # Compute silhouette coefficient
        if b_i == np.inf:
            s_i = 0
        else:
            s_i = (b_i - a_i) / max(a_i, b_i)

        silhouette_scores.append(s_i)

    return np.mean(silhouette_scores)


def example_usage():
    """Demonstrate K-Means clustering capabilities"""
    print("K-Means Clustering Algorithm Demonstration")
    print("=" * 60)

    # Generate sample data
    np.random.seed(42)

    # Create three well-separated clusters
    cluster1 = np.random.randn(100, 2) + [2, 2]
    cluster2 = np.random.randn(100, 2) + [-2, -2]
    cluster3 = np.random.randn(100, 2) + [2, -2]
    X = np.vstack([cluster1, cluster2, cluster3])

    print("\n1. Standard K-Means with K-Means++ Initialization")
    print("-" * 40)

    kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
    kmeans.fit(X)

    print(f"Number of iterations: {kmeans.n_iter_}")
    print(f"Inertia: {kmeans.inertia_:.4f}")
    print(f"Cluster sizes: {np.bincount(kmeans.labels_)}")

    # Compute silhouette score
    sil_score = silhouette_score(X, kmeans.labels_)
    print(f"Silhouette score: {sil_score:.4f}")

    print("\n2. Comparison of Initialization Methods")
    print("-" * 40)

    for init_method in ['random', 'k-means++', 'k-means||']:
        kmeans = KMeans(n_clusters=3, init=init_method, n_init=5, random_state=42)
        kmeans.fit(X)
        print(f"{init_method:12s}: Inertia = {kmeans.inertia_:8.4f}, Iterations = {kmeans.n_iter_:3d}")

    print("\n3. Elbow Method for Optimal K")
    print("-" * 40)

    results = elbow_method(X, range(1, 8), n_init=5, random_state=42)

    print("K  | Inertia")
    print("---|----------")
    for k, inertia in zip(results['k_values'], results['inertias']):
        print(f"{k:2d} | {inertia:8.2f}")

    print("\n4. Mini-Batch K-Means (for large datasets)")
    print("-" * 40)

    mb_kmeans = MiniBatchKMeans(n_clusters=3, batch_size=50, random_state=42)
    mb_kmeans.fit(X)

    print(f"Cluster sizes: {np.bincount(mb_kmeans.labels_)}")
    mb_sil_score = silhouette_score(X, mb_kmeans.labels_)
    print(f"Silhouette score: {mb_sil_score:.4f}")

    print("\n5. Fuzzy C-Means (Soft Clustering)")
    print("-" * 40)

    fcm = FuzzyCMeans(n_clusters=3, fuzziness=2.0, random_state=42)
    fcm.fit(X)

    # Show membership degrees for first 5 points
    print("Membership degrees (first 5 points):")
    print("Point | Cluster 1 | Cluster 2 | Cluster 3")
    print("------|-----------|-----------|----------")
    for i in range(5):
        print(f"  {i:2d}  |  {fcm.membership_[i, 0]:.4f}  |  {fcm.membership_[i, 1]:.4f}  |  {fcm.membership_[i, 2]:.4f}")

    crisp_labels = np.argmax(fcm.membership_, axis=1)
    print(f"\nCrisp cluster sizes: {np.bincount(crisp_labels)}")

    print("\n6. Handling Different Cluster Shapes")
    print("-" * 40)

    # Create elongated clusters
    X_elongated = np.vstack([
        np.random.randn(100, 2) * [1.0, 2.5] + [0, 0],
        np.random.randn(100, 2) * [2.5, 0.5] + [5, 0],
        np.random.randn(100, 2) * [0.5, 0.5] + [-3, 3]
    ])

    kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
    kmeans.fit(X_elongated)

    print(f"Elongated clusters - Inertia: {kmeans.inertia_:.4f}")
    print(f"Cluster sizes: {np.bincount(kmeans.labels_)}")

    print("\n7. Performance Comparison")
    print("-" * 40)

    # Generate larger dataset
    X_large = np.random.randn(1000, 10)

    # Standard K-Means
    start = time.time()
    kmeans = KMeans(n_clusters=5, init='k-means++', n_init=3)
    kmeans.fit(X_large)
    standard_time = time.time() - start

    # Mini-Batch K-Means
    start = time.time()
    mb_kmeans = MiniBatchKMeans(n_clusters=5, batch_size=100, n_init=3)
    mb_kmeans.fit(X_large)
    minibatch_time = time.time() - start

    print(f"Standard K-Means:   {standard_time:.4f} seconds")
    print(f"Mini-Batch K-Means: {minibatch_time:.4f} seconds")
    print(f"Speedup: {standard_time/minibatch_time:.2f}x")

    print("\n" + "=" * 60)
    print("K-Means clustering demonstration complete!")
    print("\nKey takeaways:")
    print("- K-Means++ initialization converges faster than random")
    print("- Elbow method helps identify optimal number of clusters")
    print("- Mini-Batch K-Means trades accuracy for speed on large datasets")
    print("- Fuzzy C-Means provides soft cluster assignments")
    print("- Silhouette score measures clustering quality")


if __name__ == "__main__":
    example_usage()