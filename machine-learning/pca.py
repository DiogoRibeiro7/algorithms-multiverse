"""
Principal Component Analysis (PCA) Implementation

A dimensionality reduction technique that transforms data to a new coordinate system
where the greatest variance by any projection lies on the first coordinate (principal
component), the second greatest variance on the second coordinate, and so on.

Key Concepts:
- Finds orthogonal axes (principal components) that maximize variance
- Components are linear combinations of original features
- Preserves as much information as possible in fewer dimensions
- Based on eigendecomposition of covariance matrix or SVD

Mathematical Foundation:
1. Center the data: X_centered = X - mean(X)
2. Compute covariance matrix: C = (1/n) * X_centered^T * X_centered
3. Find eigenvalues and eigenvectors of C
4. Sort eigenvectors by eigenvalues (descending)
5. Transform data using top k eigenvectors

Applications:
- Dimensionality reduction
- Data visualization (2D/3D projections)
- Feature extraction
- Noise reduction
- Data compression
- Exploratory data analysis

Author: Algorithms Multiverse
Date: January 2026
"""

import numpy as np
from typing import Optional, Union, Literal, Tuple
import warnings


class PCA:
    """
    Principal Component Analysis for dimensionality reduction.

    Implements PCA using eigendecomposition of covariance matrix or SVD,
    with options for whitening, incremental PCA, and kernel PCA.

    Attributes:
        n_components: Number of components to keep
        whiten: Whether to whiten the components (unit variance)
        svd_solver: Algorithm to use ('auto', 'full', 'randomized')
        random_state: Random seed for reproducibility
    """

    def __init__(
        self,
        n_components: Optional[Union[int, float]] = None,
        whiten: bool = False,
        svd_solver: Literal['auto', 'full', 'randomized'] = 'auto',
        random_state: Optional[int] = None
    ):
        """
        Initialize PCA.

        Args:
            n_components: Number of components to keep.
                - If int: exact number of components
                - If float (0.0, 1.0]: percentage of variance to preserve
                - If None: keep all components
            whiten: Whiten components to have unit variance
            svd_solver: SVD solver to use
            random_state: Random seed
        """
        self.n_components = n_components
        self.whiten = whiten
        self.svd_solver = svd_solver
        self.random_state = random_state

        # Fitted parameters
        self.components_ = None  # Principal components
        self.explained_variance_ = None  # Variance explained by each component
        self.explained_variance_ratio_ = None  # Percentage of variance explained
        self.singular_values_ = None  # Singular values
        self.mean_ = None  # Mean of training data
        self.n_components_ = None  # Actual number of components
        self.n_features_ = None  # Number of input features
        self.n_samples_seen_ = 0  # Number of samples seen

        if random_state is not None:
            np.random.seed(random_state)

    def fit(self, X: np.ndarray) -> 'PCA':
        """
        Fit PCA model to data.

        Args:
            X: Training data of shape (n_samples, n_features)

        Returns:
            Self for method chaining
        """
        X = np.asarray(X, dtype=np.float64)
        n_samples, n_features = X.shape
        self.n_features_ = n_features
        self.n_samples_seen_ = n_samples

        # Center the data
        self.mean_ = np.mean(X, axis=0)
        X_centered = X - self.mean_

        # Determine number of components
        if self.n_components is None:
            n_components = min(n_samples, n_features)
        elif isinstance(self.n_components, float):
            # Will be determined after computing variance
            n_components = min(n_samples, n_features)
        else:
            n_components = min(self.n_components, n_samples, n_features)

        # Choose solver
        if self.svd_solver == 'auto':
            # Use full SVD for small datasets, randomized for large
            if max(n_samples, n_features) <= 500:
                solver = 'full'
            else:
                solver = 'randomized'
        else:
            solver = self.svd_solver

        # Perform SVD
        if solver == 'full':
            self._fit_full_svd(X_centered, n_components)
        elif solver == 'randomized':
            self._fit_randomized_svd(X_centered, n_components)

        # Handle variance-based component selection
        if isinstance(self.n_components, float):
            # Find number of components for desired variance
            ratio_cumsum = np.cumsum(self.explained_variance_ratio_)
            n_components = np.searchsorted(ratio_cumsum, self.n_components) + 1
            n_components = min(n_components, len(self.explained_variance_ratio_))

            # Truncate to selected components
            self.components_ = self.components_[:n_components]
            self.explained_variance_ = self.explained_variance_[:n_components]
            self.explained_variance_ratio_ = self.explained_variance_ratio_[:n_components]
            self.singular_values_ = self.singular_values_[:n_components]

        self.n_components_ = len(self.components_)

        return self

    def _fit_full_svd(self, X_centered: np.ndarray, n_components: int):
        """Fit using full SVD."""
        n_samples = X_centered.shape[0]

        # Perform SVD
        U, s, Vt = np.linalg.svd(X_centered, full_matrices=False)

        # Get components (principal axes)
        self.components_ = Vt[:n_components]

        # Compute explained variance
        self.singular_values_ = s[:n_components]
        self.explained_variance_ = (s[:n_components] ** 2) / (n_samples - 1)

        total_variance = np.sum((s ** 2) / (n_samples - 1))
        self.explained_variance_ratio_ = self.explained_variance_ / total_variance

    def _fit_randomized_svd(self, X_centered: np.ndarray, n_components: int):
        """Fit using randomized SVD (simplified version)."""
        # For simplicity, using standard SVD
        # Full implementation would use randomized algorithm
        self._fit_full_svd(X_centered, n_components)

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Apply dimensionality reduction to X.

        Args:
            X: Data to transform of shape (n_samples, n_features)

        Returns:
            Transformed data of shape (n_samples, n_components)
        """
        if self.components_ is None:
            raise ValueError("PCA must be fitted before transform")

        X = np.asarray(X, dtype=np.float64)

        # Center the data
        X_centered = X - self.mean_

        # Project onto principal components
        X_transformed = X_centered @ self.components_.T

        # Whiten if requested
        if self.whiten:
            X_transformed /= np.sqrt(self.explained_variance_)

        return X_transformed

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """
        Fit PCA and transform X.

        Args:
            X: Training data

        Returns:
            Transformed data
        """
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X_transformed: np.ndarray) -> np.ndarray:
        """
        Transform data back to original space.

        Args:
            X_transformed: Transformed data

        Returns:
            Data in original space
        """
        if self.components_ is None:
            raise ValueError("PCA must be fitted before inverse_transform")

        X_transformed = np.asarray(X_transformed)

        # Reverse whitening if applied
        if self.whiten:
            X_transformed = X_transformed * np.sqrt(self.explained_variance_)

        # Project back to original space
        X_original = X_transformed @ self.components_ + self.mean_

        return X_original

    def get_covariance(self) -> np.ndarray:
        """
        Compute data covariance with the generative model.

        Returns:
            Estimated covariance matrix
        """
        if self.components_ is None:
            raise ValueError("PCA must be fitted first")

        cov = self.components_.T @ np.diag(self.explained_variance_) @ self.components_

        # Add noise variance for non-selected components
        if self.n_components_ < self.n_features_:
            noise_variance = np.mean(self.explained_variance_)
            cov += noise_variance * np.eye(self.n_features_)

        return cov

    def get_precision(self) -> np.ndarray:
        """
        Compute data precision (inverse covariance) matrix.

        Returns:
            Estimated precision matrix
        """
        cov = self.get_covariance()
        return np.linalg.inv(cov)

    def score_samples(self, X: np.ndarray) -> np.ndarray:
        """
        Compute log-likelihood of samples.

        Args:
            X: Data samples

        Returns:
            Log-likelihood of each sample
        """
        X = np.asarray(X)
        n_features = X.shape[1]

        # Compute Mahalanobis distances
        X_centered = X - self.mean_
        precision = self.get_precision()

        # Log-likelihood (simplified)
        log_like = -0.5 * (n_features * np.log(2 * np.pi) +
                          np.sum((X_centered @ precision) * X_centered, axis=1))

        return log_like

    def score(self, X: np.ndarray) -> float:
        """
        Compute average log-likelihood of samples.

        Args:
            X: Data samples

        Returns:
            Average log-likelihood
        """
        return np.mean(self.score_samples(X))


class IncrementalPCA(PCA):
    """
    Incremental PCA for large datasets that don't fit in memory.

    Processes data in batches using incremental SVD.
    """

    def __init__(
        self,
        n_components: Optional[int] = None,
        whiten: bool = False,
        batch_size: Optional[int] = None
    ):
        super().__init__(n_components=n_components, whiten=whiten)
        self.batch_size = batch_size

        # Additional attributes for incremental computation
        self.n_samples_seen_ = 0
        self.var_ = None  # Running variance
        self.noise_variance_ = None

    def partial_fit(self, X: np.ndarray) -> 'IncrementalPCA':
        """
        Incrementally fit the model with batch of samples.

        Args:
            X: Training batch

        Returns:
            Self for method chaining
        """
        X = np.asarray(X, dtype=np.float64)
        n_samples, n_features = X.shape

        if self.n_components is None:
            self.n_components_ = n_features
        else:
            self.n_components_ = self.n_components

        # First batch
        if self.components_ is None:
            self.n_features_ = n_features
            self.components_ = np.zeros((self.n_components_, n_features))
            self.mean_ = np.zeros(n_features)
            self.var_ = np.zeros(n_features)

        # Update mean incrementally
        col_mean = np.mean(X, axis=0)
        col_var = np.var(X, axis=0)

        n_total = self.n_samples_seen_ + n_samples

        # Weighted average for mean
        self.mean_ = (self.n_samples_seen_ * self.mean_ + n_samples * col_mean) / n_total

        # Update variance
        self.var_ = (self.n_samples_seen_ * self.var_ + n_samples * col_var) / n_total

        # Center the batch
        X_centered = X - col_mean

        # Simple incremental SVD (simplified version)
        # Full implementation would use proper incremental SVD algorithm
        if self.n_samples_seen_ == 0:
            # First batch: standard SVD
            U, s, Vt = np.linalg.svd(X_centered, full_matrices=False)
            self.components_ = Vt[:self.n_components_]
            self.singular_values_ = s[:self.n_components_]
            self.explained_variance_ = (s[:self.n_components_] ** 2) / (n_samples - 1)
        else:
            # Subsequent batches: approximate update
            # This is simplified - proper implementation would merge SVDs
            U, s, Vt = np.linalg.svd(X_centered, full_matrices=False)

            # Weight by number of samples
            alpha = n_samples / n_total

            # Update components (simplified)
            self.components_ = (1 - alpha) * self.components_ + alpha * Vt[:self.n_components_]

            # Reorthogonalize
            Q, R = np.linalg.qr(self.components_.T)
            self.components_ = Q.T[:self.n_components_]

        self.n_samples_seen_ = n_total

        # Compute explained variance ratio
        total_var = np.sum(self.var_)
        self.explained_variance_ratio_ = self.explained_variance_ / total_var if total_var > 0 else self.explained_variance_

        return self


class KernelPCA:
    """
    Kernel PCA for non-linear dimensionality reduction.

    Projects data into higher dimensional space using kernel trick,
    then performs PCA in that space.
    """

    def __init__(
        self,
        n_components: Optional[int] = None,
        kernel: Literal['linear', 'rbf', 'poly', 'sigmoid'] = 'rbf',
        gamma: Optional[float] = None,
        degree: int = 3,
        coef0: float = 1.0,
        fit_inverse_transform: bool = False,
        random_state: Optional[int] = None
    ):
        """
        Initialize Kernel PCA.

        Args:
            n_components: Number of components
            kernel: Kernel type
            gamma: Kernel coefficient for rbf, poly, sigmoid
            degree: Degree for polynomial kernel
            coef0: Independent term in polynomial and sigmoid kernels
            fit_inverse_transform: Learn inverse transform
            random_state: Random seed
        """
        self.n_components = n_components
        self.kernel = kernel
        self.gamma = gamma
        self.degree = degree
        self.coef0 = coef0
        self.fit_inverse_transform = fit_inverse_transform
        self.random_state = random_state

        # Fitted parameters
        self.X_fit_ = None
        self.alphas_ = None  # Eigenvectors in kernel space
        self.lambdas_ = None  # Eigenvalues

        if random_state is not None:
            np.random.seed(random_state)

    def _compute_kernel(self, X: np.ndarray, Y: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Compute kernel matrix.

        Args:
            X: First data matrix
            Y: Second data matrix (if None, uses X)

        Returns:
            Kernel matrix
        """
        if Y is None:
            Y = X

        if self.kernel == 'linear':
            K = X @ Y.T

        elif self.kernel == 'rbf':
            # RBF (Gaussian) kernel
            if self.gamma is None:
                gamma = 1.0 / X.shape[1]
            else:
                gamma = self.gamma

            # Compute pairwise squared Euclidean distances
            XX = np.sum(X * X, axis=1)[:, np.newaxis]
            YY = np.sum(Y * Y, axis=1)[np.newaxis, :]
            distances_sq = XX + YY - 2 * (X @ Y.T)

            K = np.exp(-gamma * distances_sq)

        elif self.kernel == 'poly':
            # Polynomial kernel
            if self.gamma is None:
                gamma = 1.0 / X.shape[1]
            else:
                gamma = self.gamma

            K = (gamma * (X @ Y.T) + self.coef0) ** self.degree

        elif self.kernel == 'sigmoid':
            # Sigmoid kernel
            if self.gamma is None:
                gamma = 1.0 / X.shape[1]
            else:
                gamma = self.gamma

            K = np.tanh(gamma * (X @ Y.T) + self.coef0)

        else:
            raise ValueError(f"Unknown kernel: {self.kernel}")

        return K

    def _center_kernel(self, K: np.ndarray) -> np.ndarray:
        """Center kernel matrix."""
        n_samples = K.shape[0]

        # Centering matrix
        one_n = np.ones((n_samples, n_samples)) / n_samples

        # Center kernel matrix
        K_centered = K - one_n @ K - K @ one_n + one_n @ K @ one_n

        return K_centered

    def fit(self, X: np.ndarray) -> 'KernelPCA':
        """
        Fit Kernel PCA model.

        Args:
            X: Training data

        Returns:
            Self for method chaining
        """
        X = np.asarray(X, dtype=np.float64)
        self.X_fit_ = X
        n_samples = X.shape[0]

        # Compute kernel matrix
        K = self._compute_kernel(X)

        # Center kernel matrix
        K_centered = self._center_kernel(K)

        # Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(K_centered)

        # Sort by eigenvalues (descending)
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Remove negative eigenvalues
        positive_idx = eigenvalues > 0
        eigenvalues = eigenvalues[positive_idx]
        eigenvectors = eigenvectors[:, positive_idx]

        # Determine number of components
        if self.n_components is None:
            n_components = len(eigenvalues)
        else:
            n_components = min(self.n_components, len(eigenvalues))

        # Store results
        self.lambdas_ = eigenvalues[:n_components]
        self.alphas_ = eigenvectors[:, :n_components]

        # Normalize eigenvectors
        self.alphas_ = self.alphas_ / np.sqrt(self.lambdas_)

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform data to kernel PCA space.

        Args:
            X: Data to transform

        Returns:
            Transformed data
        """
        if self.X_fit_ is None:
            raise ValueError("KernelPCA must be fitted before transform")

        X = np.asarray(X, dtype=np.float64)

        # Compute kernel with training data
        K = self._compute_kernel(X, self.X_fit_)

        # Center kernel matrix
        n_samples = X.shape[0]
        n_samples_fit = self.X_fit_.shape[0]

        K_fit = self._compute_kernel(self.X_fit_)
        one_fit = np.ones((n_samples_fit, n_samples_fit)) / n_samples_fit
        one_transform = np.ones((n_samples, n_samples_fit)) / n_samples_fit

        K_centered = K - one_transform @ K_fit - K @ one_fit + one_transform @ K_fit @ one_fit

        # Project onto eigenvectors
        X_transformed = K_centered @ self.alphas_

        return X_transformed

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit and transform data."""
        self.fit(X)
        return self.transform(X)


def example_usage():
    """Demonstrate PCA usage with various examples."""
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_iris, make_swiss_roll

    print("PCA (Principal Component Analysis) Examples")
    print("=" * 50)

    # Example 1: Basic PCA on Iris dataset
    print("\n1. Basic PCA on Iris Dataset:")
    iris = load_iris()
    X_iris = iris.data
    y_iris = iris.target

    # Fit PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_iris)

    print(f"  Original dimensions: {X_iris.shape}")
    print(f"  Reduced dimensions: {X_pca.shape}")
    print(f"  Explained variance ratio: {pca.explained_variance_ratio_}")
    print(f"  Total variance preserved: {np.sum(pca.explained_variance_ratio_):.2%}")

    # Example 2: Choosing number of components by variance
    print("\n2. Selecting Components by Variance:")
    pca_var = PCA(n_components=0.95)  # Keep 95% variance
    X_pca_var = pca_var.fit_transform(X_iris)

    print(f"  Components needed for 95% variance: {pca_var.n_components_}")
    print(f"  Actual variance preserved: {np.sum(pca_var.explained_variance_ratio_):.2%}")

    # Example 3: Whitening
    print("\n3. PCA with Whitening:")
    pca_white = PCA(n_components=2, whiten=True)
    X_white = pca_white.fit_transform(X_iris)

    print(f"  Original data variance: {np.var(X_iris, axis=0)}")
    print(f"  Whitened data variance: {np.var(X_white, axis=0)}")

    # Example 4: Reconstruction error
    print("\n4. Reconstruction Error Analysis:")
    for n_comp in [1, 2, 3, 4]:
        pca_temp = PCA(n_components=n_comp)
        X_reduced = pca_temp.fit_transform(X_iris)
        X_reconstructed = pca_temp.inverse_transform(X_reduced)

        mse = np.mean((X_iris - X_reconstructed) ** 2)
        print(f"  {n_comp} components - MSE: {mse:.4f}, "
              f"Variance preserved: {np.sum(pca_temp.explained_variance_ratio_):.2%}")

    # Example 5: Incremental PCA
    print("\n5. Incremental PCA (for large datasets):")
    ipca = IncrementalPCA(n_components=2)

    # Process in batches
    batch_size = 50
    for i in range(0, len(X_iris), batch_size):
        batch = X_iris[i:i + batch_size]
        ipca.partial_fit(batch)

    X_ipca = ipca.transform(X_iris)
    print(f"  Incremental PCA shape: {X_ipca.shape}")
    print(f"  Explained variance ratio: {ipca.explained_variance_ratio_}")

    # Example 6: Kernel PCA for non-linear data
    print("\n6. Kernel PCA (Non-linear):")

    # Create Swiss roll dataset (non-linear manifold)
    X_swiss, color = make_swiss_roll(n_samples=500, random_state=42)

    # Standard PCA
    pca_linear = PCA(n_components=2)
    X_pca_linear = pca_linear.fit_transform(X_swiss)

    # Kernel PCA with RBF kernel
    kpca_rbf = KernelPCA(n_components=2, kernel='rbf', gamma=0.01)
    X_kpca = kpca_rbf.fit_transform(X_swiss)

    print(f"  Swiss roll original shape: {X_swiss.shape}")
    print(f"  Linear PCA result shape: {X_pca_linear.shape}")
    print(f"  Kernel PCA (RBF) result shape: {X_kpca.shape}")

    # Example 7: Feature importance
    print("\n7. Component Analysis:")
    pca_analysis = PCA()
    pca_analysis.fit(X_iris)

    print("  Principal Component Loadings (first 2 components):")
    feature_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    for i, component in enumerate(pca_analysis.components_[:2]):
        print(f"    PC{i+1}:")
        for j, loading in enumerate(component):
            print(f"      {feature_names[j]}: {loading:.3f}")

    # Example 8: Scree plot data
    print("\n8. Scree Plot Data (for visualization):")
    print("  Component | Variance | Cumulative")
    cumulative = np.cumsum(pca_analysis.explained_variance_ratio_)
    for i, (var, cum) in enumerate(zip(pca_analysis.explained_variance_ratio_, cumulative)):
        print(f"      {i+1}    |  {var:.3f}  |   {cum:.3f}")

    # Example 9: Noise reduction
    print("\n9. Noise Reduction with PCA:")
    # Add noise to data
    X_noisy = X_iris + np.random.normal(0, 0.5, X_iris.shape)

    # Denoise using PCA
    pca_denoise = PCA(n_components=0.99)
    X_denoised = pca_denoise.fit_transform(X_noisy)
    X_denoised = pca_denoise.inverse_transform(X_denoised)

    noise_before = np.mean((X_iris - X_noisy) ** 2)
    noise_after = np.mean((X_iris - X_denoised) ** 2)

    print(f"  MSE before denoising: {noise_before:.4f}")
    print(f"  MSE after denoising: {noise_after:.4f}")
    print(f"  Noise reduction: {(1 - noise_after/noise_before)*100:.1f}%")

    # Example 10: Performance comparison
    print("\n10. Algorithm Performance:")
    import time

    sizes = [100, 500, 1000]
    for size in sizes:
        X_test = np.random.randn(size, 50)

        # Standard PCA
        start = time.time()
        pca_test = PCA(n_components=10)
        pca_test.fit_transform(X_test)
        pca_time = time.time() - start

        # Kernel PCA (more expensive)
        start = time.time()
        kpca_test = KernelPCA(n_components=10, kernel='linear')
        kpca_test.fit_transform(X_test)
        kpca_time = time.time() - start

        print(f"  Size {size}x50 - PCA: {pca_time:.4f}s, KernelPCA: {kpca_time:.4f}s")


if __name__ == "__main__":
    example_usage()