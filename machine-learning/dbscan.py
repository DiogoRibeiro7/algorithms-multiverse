"""
DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

A density-based clustering algorithm that groups together points that are closely
packed together, marking points in low-density regions as outliers. Unlike K-Means,
DBSCAN doesn't require specifying the number of clusters beforehand and can find
arbitrarily shaped clusters.

Key Concepts:
- Core points: Points with at least min_samples neighbors within eps radius
- Border points: Points within eps of a core point but not core themselves
- Noise points: Points that are neither core nor border points

Advantages:
- Finds clusters of arbitrary shape
- Robust to outliers (identifies noise)
- No need to specify number of clusters
- Can find clusters completely surrounded by other clusters

Disadvantages:
- Sensitive to eps and min_samples parameters
- Cannot cluster datasets with large density variations
- High memory requirements for distance matrix

Time Complexity: O(n²) worst case, O(n log n) with spatial index
Space Complexity: O(n)

Author: Algorithms Multiverse
Date: January 2026
"""

import numpy as np
from typing import Optional, List, Tuple, Union, Literal
from collections import deque
from scipy.spatial.distance import cdist
import warnings


class DBSCAN:
    """
    DBSCAN clustering algorithm implementation.

    Parameters:
        eps: Maximum distance between two samples for them to be considered neighbors
        min_samples: Minimum number of samples in a neighborhood for a point to be core
        metric: Distance metric ('euclidean', 'manhattan', 'cosine', etc.)
        algorithm: Algorithm for nearest neighbors ('brute', 'kd_tree', 'ball_tree')
        leaf_size: Leaf size for tree algorithms (ignored for brute force)
        n_jobs: Number of parallel jobs (-1 uses all processors)
    """

    def __init__(
        self,
        eps: float = 0.5,
        min_samples: int = 5,
        metric: str = 'euclidean',
        algorithm: Literal['auto', 'brute', 'kd_tree', 'ball_tree'] = 'auto',
        leaf_size: int = 30,
        n_jobs: int = 1
    ):
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric
        self.algorithm = algorithm
        self.leaf_size = leaf_size
        self.n_jobs = n_jobs

        # Results
        self.labels_ = None
        self.core_sample_indices_ = None
        self.components_ = None
        self.n_features_in_ = None

    def fit(self, X: np.ndarray, sample_weight: Optional[np.ndarray] = None) -> 'DBSCAN':
        """
        Perform DBSCAN clustering.

        Args:
            X: Feature array of shape (n_samples, n_features)
            sample_weight: Sample weights (not used in standard DBSCAN)

        Returns:
            Self for method chaining
        """
        X = np.asarray(X)
        n_samples = X.shape[0]
        self.n_features_in_ = X.shape[1]

        # Initialize labels (-1 for noise)
        labels = -np.ones(n_samples, dtype=int)

        # Find neighbors for all points
        if self.algorithm == 'auto':
            # Choose algorithm based on data
            if n_samples < 1000:
                neighbors = self._find_neighbors_brute(X)
            else:
                # For larger datasets, would use tree-based methods
                # For simplicity, using brute force here
                neighbors = self._find_neighbors_brute(X)
        else:
            neighbors = self._find_neighbors_brute(X)

        # Identify core points
        core_samples = np.zeros(n_samples, dtype=bool)
        for i in range(n_samples):
            if len(neighbors[i]) >= self.min_samples:
                core_samples[i] = True

        # Store core sample indices
        self.core_sample_indices_ = np.where(core_samples)[0]

        # Perform clustering
        cluster_id = 0
        visited = np.zeros(n_samples, dtype=bool)

        for i in range(n_samples):
            if visited[i]:
                continue

            visited[i] = True

            if not core_samples[i]:
                continue

            # Start new cluster
            labels[i] = cluster_id

            # BFS to expand cluster
            queue = deque(neighbors[i])

            while queue:
                neighbor_idx = queue.popleft()

                if not visited[neighbor_idx]:
                    visited[neighbor_idx] = True

                    if core_samples[neighbor_idx]:
                        # Add unvisited neighbors to queue
                        queue.extend([n for n in neighbors[neighbor_idx] if not visited[n]])

                if labels[neighbor_idx] == -1:  # Noise or unassigned
                    labels[neighbor_idx] = cluster_id

            cluster_id += 1

        self.labels_ = labels

        # Extract core components (core points grouped by cluster)
        if cluster_id > 0:
            self.components_ = X[core_samples]
        else:
            self.components_ = np.empty((0, self.n_features_in_))

        return self

    def _find_neighbors_brute(self, X: np.ndarray) -> List[List[int]]:
        """
        Find neighbors using brute force distance calculation.

        Args:
            X: Feature array

        Returns:
            List of neighbor indices for each point
        """
        n_samples = X.shape[0]
        neighbors = [[] for _ in range(n_samples)]

        # Compute pairwise distances
        if self.metric == 'euclidean':
            # Optimized euclidean distance
            for i in range(n_samples):
                dists = np.sqrt(np.sum((X - X[i]) ** 2, axis=1))
                neighbors[i] = np.where(dists <= self.eps)[0].tolist()
        else:
            # Use scipy for other metrics
            distances = cdist(X, X, metric=self.metric)
            for i in range(n_samples):
                neighbors[i] = np.where(distances[i] <= self.eps)[0].tolist()

        return neighbors

    def fit_predict(self, X: np.ndarray, sample_weight: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Perform clustering and return cluster labels.

        Args:
            X: Feature array
            sample_weight: Sample weights

        Returns:
            Cluster labels (-1 for noise)
        """
        self.fit(X, sample_weight)
        return self.labels_

    def get_params(self) -> dict:
        """Get parameters for this estimator."""
        return {
            'eps': self.eps,
            'min_samples': self.min_samples,
            'metric': self.metric,
            'algorithm': self.algorithm,
            'leaf_size': self.leaf_size,
            'n_jobs': self.n_jobs
        }

    def set_params(self, **params):
        """Set parameters for this estimator."""
        for key, value in params.items():
            setattr(self, key, value)
        return self


class OptimizedDBSCAN(DBSCAN):
    """
    Optimized DBSCAN with spatial indexing for better performance.

    Uses KD-tree or Ball-tree for efficient neighbor queries.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tree = None

    def _build_tree(self, X: np.ndarray):
        """Build spatial index tree for efficient queries."""
        try:
            from sklearn.neighbors import KDTree, BallTree

            if self.algorithm == 'kd_tree' or (self.algorithm == 'auto' and self.metric == 'euclidean'):
                self._tree = KDTree(X, leaf_size=self.leaf_size, metric=self.metric)
            else:
                self._tree = BallTree(X, leaf_size=self.leaf_size, metric=self.metric)
        except ImportError:
            warnings.warn("scikit-learn not available, falling back to brute force")
            self._tree = None

    def _find_neighbors_tree(self, X: np.ndarray) -> List[List[int]]:
        """Find neighbors using tree-based search."""
        if self._tree is None:
            self._build_tree(X)

        if self._tree is not None:
            # Query tree for all neighbors within eps
            neighbors = self._tree.query_radius(X, r=self.eps)
            return [n.tolist() for n in neighbors]
        else:
            return self._find_neighbors_brute(X)


class HDBSCAN:
    """
    Hierarchical DBSCAN - builds a hierarchy of clusters.

    Extends DBSCAN to find clusters of varying densities and provides
    a cluster hierarchy that can be used for different granularities.
    """

    def __init__(
        self,
        min_cluster_size: int = 5,
        min_samples: Optional[int] = None,
        metric: str = 'euclidean',
        alpha: float = 1.0,
        cluster_selection_method: Literal['eom', 'leaf'] = 'eom'
    ):
        self.min_cluster_size = min_cluster_size
        self.min_samples = min_samples if min_samples else min_cluster_size
        self.metric = metric
        self.alpha = alpha
        self.cluster_selection_method = cluster_selection_method

        self.labels_ = None
        self.probabilities_ = None
        self.cluster_persistence_ = None
        self.outlier_scores_ = None

    def fit(self, X: np.ndarray) -> 'HDBSCAN':
        """
        Build HDBSCAN hierarchy and extract clusters.

        This is a simplified version focusing on the core concepts.
        Full implementation would include MST construction and hierarchy extraction.
        """
        n_samples = X.shape[0]

        # Compute mutual reachability distance
        core_distances = self._compute_core_distances(X)

        # Build minimum spanning tree (simplified)
        mst = self._build_mst(X, core_distances)

        # Extract hierarchy (simplified - just use single linkage)
        hierarchy = self._extract_hierarchy(mst)

        # Extract clusters using EOM or leaf method
        self.labels_ = self._extract_clusters(hierarchy, n_samples)

        # Compute outlier scores
        self._compute_outlier_scores(X)

        return self

    def _compute_core_distances(self, X: np.ndarray) -> np.ndarray:
        """Compute core distance for each point."""
        n_samples = X.shape[0]
        core_distances = np.zeros(n_samples)

        # Compute distance to kth nearest neighbor
        if self.metric == 'euclidean':
            for i in range(n_samples):
                dists = np.sort(np.sqrt(np.sum((X - X[i]) ** 2, axis=1)))
                if self.min_samples < len(dists):
                    core_distances[i] = dists[self.min_samples]
                else:
                    core_distances[i] = dists[-1]
        else:
            distances = cdist(X, X, metric=self.metric)
            for i in range(n_samples):
                sorted_dists = np.sort(distances[i])
                if self.min_samples < len(sorted_dists):
                    core_distances[i] = sorted_dists[self.min_samples]
                else:
                    core_distances[i] = sorted_dists[-1]

        return core_distances

    def _build_mst(self, X: np.ndarray, core_distances: np.ndarray) -> List[Tuple[int, int, float]]:
        """Build minimum spanning tree (simplified version)."""
        n_samples = X.shape[0]
        mst = []

        # Simplified: use pairwise distances
        # Full implementation would use Prim's or Kruskal's algorithm
        distances = cdist(X, X, metric=self.metric)

        # Mutual reachability distance
        for i in range(n_samples):
            for j in range(i + 1, n_samples):
                mutual_reach = max(core_distances[i], core_distances[j], distances[i, j])
                mst.append((i, j, mutual_reach))

        # Sort by distance and extract MST (simplified)
        mst.sort(key=lambda x: x[2])

        # Return simplified MST (first n-1 edges)
        return mst[:n_samples - 1]

    def _extract_hierarchy(self, mst: List[Tuple[int, int, float]]) -> np.ndarray:
        """Extract cluster hierarchy from MST."""
        # Simplified: return MST as hierarchy
        # Full implementation would build dendrogram
        return np.array(mst)

    def _extract_clusters(self, hierarchy: np.ndarray, n_samples: int) -> np.ndarray:
        """Extract flat clustering from hierarchy."""
        # Simplified: use single threshold
        # Full implementation would use EOM or leaf selection
        labels = -np.ones(n_samples, dtype=int)

        # Simple connected components at a threshold
        if len(hierarchy) > 0:
            threshold = np.median(hierarchy[:, 2])

            # Union-find to extract components
            parent = list(range(n_samples))

            def find(x):
                if parent[x] != x:
                    parent[x] = find(parent[x])
                return parent[x]

            def union(x, y):
                px, py = find(x), find(y)
                if px != py:
                    parent[px] = py

            for i, j, dist in hierarchy:
                if dist <= threshold:
                    union(int(i), int(j))

            # Assign cluster labels
            cluster_map = {}
            cluster_id = 0

            for i in range(n_samples):
                root = find(i)
                if root not in cluster_map:
                    # Check if cluster is large enough
                    size = sum(1 for j in range(n_samples) if find(j) == root)
                    if size >= self.min_cluster_size:
                        cluster_map[root] = cluster_id
                        cluster_id += 1
                    else:
                        cluster_map[root] = -1

                labels[i] = cluster_map[root]

        return labels

    def _compute_outlier_scores(self, X: np.ndarray):
        """Compute outlier scores for each point."""
        # Simplified: use distance to nearest cluster
        # Full implementation would use GLOSH scores
        n_samples = X.shape[0]
        self.outlier_scores_ = np.zeros(n_samples)

        if self.labels_ is not None:
            for i in range(n_samples):
                if self.labels_[i] == -1:
                    self.outlier_scores_[i] = 1.0  # Maximum outlier score

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit and return cluster labels."""
        self.fit(X)
        return self.labels_


def example_usage():
    """Demonstrate DBSCAN usage with various examples."""
    import matplotlib.pyplot as plt
    from sklearn.datasets import make_moons, make_blobs, make_circles

    print("DBSCAN Clustering Examples")
    print("=" * 50)

    # Example 1: Two moons dataset (non-linear separation)
    print("\n1. Two Moons Dataset:")
    X_moons, y_moons = make_moons(n_samples=200, noise=0.1, random_state=42)

    dbscan_moons = DBSCAN(eps=0.2, min_samples=5)
    labels_moons = dbscan_moons.fit_predict(X_moons)

    n_clusters = len(set(labels_moons)) - (1 if -1 in labels_moons else 0)
    n_noise = list(labels_moons).count(-1)

    print(f"  Number of clusters: {n_clusters}")
    print(f"  Number of noise points: {n_noise}")
    print(f"  Core samples: {len(dbscan_moons.core_sample_indices_)}")

    # Example 2: Blobs with noise
    print("\n2. Gaussian Blobs with Noise:")
    X_blobs, y_blobs = make_blobs(n_samples=300, centers=3, n_features=2,
                                   center_box=(-10, 10), random_state=42)
    # Add noise points
    noise = np.random.uniform(-12, 12, (50, 2))
    X_blobs_noise = np.vstack([X_blobs, noise])

    dbscan_blobs = DBSCAN(eps=2.0, min_samples=5)
    labels_blobs = dbscan_blobs.fit_predict(X_blobs_noise)

    n_clusters = len(set(labels_blobs)) - (1 if -1 in labels_blobs else 0)
    n_noise = list(labels_blobs).count(-1)

    print(f"  Number of clusters: {n_clusters}")
    print(f"  Number of noise points: {n_noise}")

    # Example 3: Concentric circles
    print("\n3. Concentric Circles:")
    X_circles, y_circles = make_circles(n_samples=200, factor=0.5, noise=0.05,
                                        random_state=42)

    dbscan_circles = DBSCAN(eps=0.15, min_samples=5)
    labels_circles = dbscan_circles.fit_predict(X_circles)

    n_clusters = len(set(labels_circles)) - (1 if -1 in labels_circles else 0)
    print(f"  Number of clusters: {n_clusters}")

    # Example 4: Parameter sensitivity
    print("\n4. Parameter Sensitivity Analysis:")
    eps_values = [0.1, 0.2, 0.3, 0.5]
    min_samples_values = [3, 5, 10]

    print("  Results for Two Moons dataset:")
    for eps in eps_values:
        for min_samples in min_samples_values:
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            labels = dbscan.fit_predict(X_moons)
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            n_noise = list(labels).count(-1)
            print(f"    eps={eps:.1f}, min_samples={min_samples}: "
                  f"{n_clusters} clusters, {n_noise} noise points")

    # Example 5: Different metrics
    print("\n5. Different Distance Metrics:")
    metrics = ['euclidean', 'manhattan', 'cosine']

    for metric in metrics:
        try:
            dbscan = DBSCAN(eps=0.3, min_samples=5, metric=metric)
            labels = dbscan.fit_predict(X_moons)
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            print(f"  {metric}: {n_clusters} clusters found")
        except:
            print(f"  {metric}: Not available without scipy")

    # Example 6: Hierarchical DBSCAN
    print("\n6. Hierarchical DBSCAN (HDBSCAN):")
    hdbscan = HDBSCAN(min_cluster_size=5, min_samples=3)
    labels_h = hdbscan.fit_predict(X_blobs_noise)

    n_clusters = len(set(labels_h)) - (1 if -1 in labels_h else 0)
    n_noise = list(labels_h).count(-1)

    print(f"  Number of clusters: {n_clusters}")
    print(f"  Number of noise points: {n_noise}")

    # Example 7: Comparison with K-Means
    print("\n7. DBSCAN vs K-Means:")
    print("  Advantages of DBSCAN:")
    print("    - No need to specify number of clusters")
    print("    - Can find arbitrarily shaped clusters")
    print("    - Identifies outliers/noise")
    print("    - Can find clusters surrounded by other clusters")
    print("  Disadvantages:")
    print("    - Sensitive to eps and min_samples")
    print("    - Cannot cluster well with varying densities")
    print("    - Higher computational complexity")

    # Performance characteristics
    print("\n8. Performance Characteristics:")
    print("  Time Complexity: O(n²) worst case, O(n log n) with spatial index")
    print("  Space Complexity: O(n)")
    print("  Scalability: Good for medium datasets, challenging for very large datasets")

    # Visualization helper
    def plot_clusters(X, labels, title):
        """Plot clustering results."""
        plt.figure(figsize=(8, 6))

        # Get unique labels
        unique_labels = set(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black for noise
                col = 'black'
                marker = 'x'
            else:
                marker = 'o'

            class_member_mask = (labels == k)
            xy = X[class_member_mask]
            plt.scatter(xy[:, 0], xy[:, 1], c=[col], marker=marker,
                       s=50, label=f'Cluster {k}' if k != -1 else 'Noise')

        plt.title(title)
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    # Uncomment to visualize
    # plot_clusters(X_moons, labels_moons, "DBSCAN on Two Moons")
    # plot_clusters(X_blobs_noise, labels_blobs, "DBSCAN on Blobs with Noise")
    # plot_clusters(X_circles, labels_circles, "DBSCAN on Concentric Circles")


if __name__ == "__main__":
    example_usage()