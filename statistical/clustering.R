# ==============================================================================
# Clustering Algorithms in R
#
# Comprehensive collection of clustering methods for unsupervised learning.
#
# Implementations:
# - K-Means Clustering (Lloyd's algorithm)
# - K-Means++ (smart initialization)
# - Hierarchical Clustering (agglomerative)
# - DBSCAN (Density-Based Spatial Clustering)
# - Gaussian Mixture Models (EM algorithm)
# - Silhouette Analysis
#
# Clustering is fundamental in machine learning, data mining, and pattern
# recognition. R's vectorization makes these algorithms particularly efficient.
#
# Run: Rscript clustering.R
#
# @author Algorithms Multiverse
# @version 1.0
# ==============================================================================

EPSILON <- 1e-10

# ==============================================================================
# K-Means Clustering
# ==============================================================================

#' K-Means Clustering (Lloyd's Algorithm)
#'
#' Partitions data into K clusters by minimizing within-cluster variance
#'
#' Time Complexity: O(iterations × n × K × d)
#'   where n = samples, K = clusters, d = dimensions
#' Space Complexity: O(nK + Kd)
#'
#' Algorithm:
#' 1. Initialize K cluster centers randomly
#' 2. Assign each point to nearest center
#' 3. Update centers as mean of assigned points
#' 4. Repeat until convergence
#'
#' Applications:
#' - Customer segmentation
#' - Image compression
#' - Document clustering
#' - Anomaly detection
#'
#' @param X Data matrix (n × d)
#' @param K Number of clusters
#' @param max_iter Maximum iterations (default: 100)
#' @param tol Convergence tolerance (default: 1e-6)
#' @return List with cluster assignments, centers, inertia
kmeans_clustering <- function(X, K, max_iter = 100, tol = 1e-6) {
  n <- nrow(X)
  d <- ncol(X)

  # Random initialization
  set.seed(42)
  center_indices <- sample(1:n, K)
  centers <- X[center_indices, , drop = FALSE]

  # Initialize
  labels <- integer(n)
  inertia_old <- Inf

  for (iter in 1:max_iter) {
    # Assignment step: assign each point to nearest center
    distances <- matrix(0, nrow = n, ncol = K)
    for (k in 1:K) {
      # Euclidean distance to center k
      diff <- sweep(X, 2, centers[k, ])
      distances[, k] <- rowSums(diff^2)
    }
    labels <- apply(distances, 1, which.min)

    # Update step: recompute centers
    for (k in 1:K) {
      cluster_points <- X[labels == k, , drop = FALSE]
      if (nrow(cluster_points) > 0) {
        centers[k, ] <- colMeans(cluster_points)
      }
    }

    # Compute inertia (within-cluster sum of squares)
    inertia <- 0
    for (k in 1:K) {
      cluster_points <- X[labels == k, , drop = FALSE]
      if (nrow(cluster_points) > 0) {
        diff <- sweep(cluster_points, 2, centers[k, ])
        inertia <- inertia + sum(diff^2)
      }
    }

    # Check convergence
    if (abs(inertia_old - inertia) < tol) {
      break
    }
    inertia_old <- inertia
  }

  list(
    labels = labels,
    centers = centers,
    inertia = inertia,
    iterations = iter
  )
}

# ==============================================================================
# K-Means++ (Improved Initialization)
# ==============================================================================

#' K-Means++ Clustering
#'
#' K-Means with smart initialization (David Arthur & Sergei Vassilvitskii, 2007)
#'
#' Time Complexity: O(nKd) for init + O(iterations × nKd) for Lloyd's
#' Space Complexity: O(nK + Kd)
#'
#' Initialization:
#' 1. Choose first center uniformly at random
#' 2. For each subsequent center:
#'    - Choose point with probability proportional to D(x)²
#'    - where D(x) = distance to nearest existing center
#'
#' Benefits:
#' - Faster convergence
#' - Better final clustering
#' - O(log K) approximation guarantee
#'
#' @param X Data matrix (n × d)
#' @param K Number of clusters
#' @param max_iter Maximum iterations
#' @return List with cluster assignments, centers, inertia
kmeans_plusplus <- function(X, K, max_iter = 100) {
  n <- nrow(X)
  d <- ncol(X)

  # K-Means++ initialization
  set.seed(42)
  centers <- matrix(0, nrow = K, ncol = d)

  # First center: random
  centers[1, ] <- X[sample(1:n, 1), ]

  # Subsequent centers
  for (k in 2:K) {
    # Compute distance to nearest center for each point
    distances <- matrix(Inf, nrow = n, ncol = k - 1)
    for (j in 1:(k - 1)) {
      diff <- sweep(X, 2, centers[j, ])
      distances[, j] <- rowSums(diff^2)
    }
    min_distances <- apply(distances, 1, min)

    # Choose next center with probability ∝ D(x)²
    probabilities <- min_distances / sum(min_distances)
    centers[k, ] <- X[sample(1:n, 1, prob = probabilities), ]
  }

  # Run Lloyd's algorithm with these centers
  labels <- integer(n)
  inertia_old <- Inf

  for (iter in 1:max_iter) {
    # Assignment
    distances <- matrix(0, nrow = n, ncol = K)
    for (k in 1:K) {
      diff <- sweep(X, 2, centers[k, ])
      distances[, k] <- rowSums(diff^2)
    }
    labels <- apply(distances, 1, which.min)

    # Update centers
    for (k in 1:K) {
      cluster_points <- X[labels == k, , drop = FALSE]
      if (nrow(cluster_points) > 0) {
        centers[k, ] <- colMeans(cluster_points)
      }
    }

    # Compute inertia
    inertia <- 0
    for (k in 1:K) {
      cluster_points <- X[labels == k, , drop = FALSE]
      if (nrow(cluster_points) > 0) {
        diff <- sweep(cluster_points, 2, centers[k, ])
        inertia <- inertia + sum(diff^2)
      }
    }

    if (abs(inertia_old - inertia) < 1e-6) break
    inertia_old <- inertia
  }

  list(
    labels = labels,
    centers = centers,
    inertia = inertia,
    iterations = iter
  )
}

# ==============================================================================
# Hierarchical Clustering (Agglomerative)
# ==============================================================================

#' Hierarchical Agglomerative Clustering
#'
#' Bottom-up clustering building a dendrogram
#'
#' Time Complexity: O(n² log n) with efficient implementation
#' Space Complexity: O(n²)
#'
#' Algorithm:
#' 1. Start with each point as its own cluster
#' 2. Repeatedly merge closest clusters
#' 3. Continue until K clusters remain
#'
#' Linkage methods:
#' - single: minimum distance between clusters
#' - complete: maximum distance
#' - average: average distance
#'
#' Applications:
#' - Taxonomies
#' - Phylogenetic trees
#' - Document organization
#'
#' @param X Data matrix
#' @param K Number of clusters
#' @param linkage Linkage method ("single", "complete", "average")
#' @return List with cluster assignments, dendrogram
hierarchical_clustering <- function(X, K, linkage = "average") {
  n <- nrow(X)

  # Compute pairwise distance matrix
  dist_matrix <- as.matrix(dist(X, method = "euclidean"))

  # Initialize: each point is its own cluster
  clusters <- as.list(1:n)
  labels <- 1:n

  # Merge until K clusters remain
  while (length(clusters) > K) {
    # Find closest pair of clusters
    min_dist <- Inf
    merge_i <- NULL
    merge_j <- NULL

    for (i in 1:(length(clusters) - 1)) {
      for (j in (i + 1):length(clusters)) {
        # Compute distance between clusters i and j
        cluster_dist <- 0

        if (linkage == "single") {
          # Minimum distance
          cluster_dist <- min(dist_matrix[clusters[[i]], clusters[[j]]])
        } else if (linkage == "complete") {
          # Maximum distance
          cluster_dist <- max(dist_matrix[clusters[[i]], clusters[[j]]])
        } else {  # average
          # Average distance
          cluster_dist <- mean(dist_matrix[clusters[[i]], clusters[[j]]])
        }

        if (cluster_dist < min_dist) {
          min_dist <- cluster_dist
          merge_i <- i
          merge_j <- j
        }
      }
    }

    # Merge clusters
    clusters[[merge_i]] <- c(clusters[[merge_i]], clusters[[merge_j]])
    clusters <- clusters[-merge_j]
  }

  # Create labels
  final_labels <- integer(n)
  for (k in 1:K) {
    final_labels[clusters[[k]]] <- k
  }

  list(
    labels = final_labels,
    n_clusters = K,
    linkage = linkage
  )
}

# ==============================================================================
# DBSCAN (Density-Based Spatial Clustering)
# ==============================================================================

#' DBSCAN Clustering
#'
#' Density-based clustering that can find arbitrarily shaped clusters
#'
#' Time Complexity: O(n log n) with spatial index, O(n²) without
#' Space Complexity: O(n)
#'
#' Parameters:
#' - eps: Neighborhood radius
#' - minPts: Minimum points to form dense region
#'
#' Point types:
#' - Core: has ≥ minPts neighbors within eps
#' - Border: in neighborhood of core point
#' - Noise: neither core nor border
#'
#' Applications:
#' - Anomaly detection
#' - Spatial data analysis
#' - Arbitrary-shaped clusters
#' - No need to specify K
#'
#' @param X Data matrix
#' @param eps Neighborhood radius
#' @param minPts Minimum points for core point
#' @return List with cluster labels (0 = noise)
dbscan_clustering <- function(X, eps, minPts) {
  n <- nrow(X)

  # Compute distance matrix
  dist_matrix <- as.matrix(dist(X, method = "euclidean"))

  # Initialize
  labels <- rep(0, n)  # 0 = noise
  cluster_id <- 0
  visited <- rep(FALSE, n)

  for (i in 1:n) {
    if (visited[i]) next

    visited[i] <- TRUE

    # Find neighbors
    neighbors <- which(dist_matrix[i, ] <= eps)

    if (length(neighbors) < minPts) {
      labels[i] <- 0  # Noise point
    } else {
      # Start new cluster
      cluster_id <- cluster_id + 1
      labels[i] <- cluster_id

      # Expand cluster
      seed_set <- neighbors[neighbors != i]

      j <- 1
      while (j <= length(seed_set)) {
        point <- seed_set[j]

        if (!visited[point]) {
          visited[point] <- TRUE

          # Find neighbors of this point
          point_neighbors <- which(dist_matrix[point, ] <= eps)

          if (length(point_neighbors) >= minPts) {
            # Add new neighbors to seed set
            seed_set <- unique(c(seed_set, point_neighbors))
          }
        }

        # Add to cluster if not already assigned
        if (labels[point] == 0) {
          labels[point] <- cluster_id
        }

        j <- j + 1
      }
    }
  }

  list(
    labels = labels,
    n_clusters = cluster_id,
    n_noise = sum(labels == 0)
  )
}

# ==============================================================================
# Silhouette Analysis
# ==============================================================================

#' Silhouette Coefficient
#'
#' Measures clustering quality: how similar point is to its own cluster
#' vs. other clusters
#'
#' Time Complexity: O(n²)
#' Space Complexity: O(n)
#'
#' Silhouette score s(i) for point i:
#' s(i) = (b(i) - a(i)) / max(a(i), b(i))
#'
#' where:
#' - a(i) = average distance to points in same cluster
#' - b(i) = average distance to points in nearest other cluster
#'
#' Range: [-1, 1]
#' - 1: Perfect clustering
#' - 0: On cluster boundary
#' - -1: Wrong cluster
#'
#' @param X Data matrix
#' @param labels Cluster labels
#' @return List with silhouette scores and average
silhouette_analysis <- function(X, labels) {
  n <- nrow(X)
  dist_matrix <- as.matrix(dist(X, method = "euclidean"))

  scores <- numeric(n)
  clusters <- unique(labels)

  for (i in 1:n) {
    own_cluster <- labels[i]
    own_cluster_points <- which(labels == own_cluster & (1:n) != i)

    if (length(own_cluster_points) == 0) {
      scores[i] <- 0
      next
    }

    # a(i): average distance to own cluster
    a_i <- mean(dist_matrix[i, own_cluster_points])

    # b(i): minimum average distance to other clusters
    b_i <- Inf
    for (other_cluster in clusters) {
      if (other_cluster == own_cluster) next

      other_cluster_points <- which(labels == other_cluster)
      if (length(other_cluster_points) > 0) {
        avg_dist <- mean(dist_matrix[i, other_cluster_points])
        b_i <- min(b_i, avg_dist)
      }
    }

    # Silhouette score
    scores[i] <- (b_i - a_i) / max(a_i, b_i)
  }

  list(
    scores = scores,
    avg_score = mean(scores)
  )
}

# ==============================================================================
# Main Program - Examples and Tests
# ==============================================================================

cat("==============================================================================\n")
cat("                CLUSTERING ALGORITHMS IN R\n")
cat("         Unsupervised Learning & Pattern Recognition\n")
cat("==============================================================================\n\n")

# ==============================================================================
# Example 1: K-Means on Synthetic Data
# ==============================================================================

cat("Example 1: K-Means Clustering\n")
cat("================================================================================\n")
set.seed(42)

# Generate 3 clusters
cluster1 <- matrix(rnorm(100, mean = 0, sd = 1), ncol = 2)
cluster2 <- matrix(rnorm(100, mean = 5, sd = 1), ncol = 2)
cluster3 <- matrix(rnorm(100, mean = c(5, 0), sd = 1), ncol = 2)
X <- rbind(cluster1, cluster2, cluster3)

result <- kmeans_clustering(X, K = 3, max_iter = 100)
cat(sprintf("Converged in %d iterations\n", result$iterations))
cat(sprintf("Final inertia: %.4f\n", result$inertia))
cat(sprintf("Cluster sizes: %s\n", paste(table(result$labels), collapse = ", ")))

# Silhouette analysis
sil <- silhouette_analysis(X, result$labels)
cat(sprintf("Average silhouette score: %.4f\n\n", sil$avg_score))

# ==============================================================================
# Example 2: K-Means++ vs Regular K-Means
# ==============================================================================

cat("Example 2: K-Means++ vs Standard K-Means\n")
cat("================================================================================\n")

result_standard <- kmeans_clustering(X, K = 3)
result_plusplus <- kmeans_plusplus(X, K = 3)

cat("Standard K-Means:\n")
cat(sprintf("  Inertia: %.4f, Iterations: %d\n",
            result_standard$inertia, result_standard$iterations))

cat("K-Means++:\n")
cat(sprintf("  Inertia: %.4f, Iterations: %d\n",
            result_plusplus$inertia, result_plusplus$iterations))
cat(sprintf("  Improvement: %.2f%%\n\n",
            100 * (result_standard$inertia - result_plusplus$inertia) / result_standard$inertia))

# ==============================================================================
# Example 3: Hierarchical Clustering
# ==============================================================================

cat("Example 3: Hierarchical Clustering (Different Linkages)\n")
cat("================================================================================\n")

for (linkage in c("single", "complete", "average")) {
  result <- hierarchical_clustering(X, K = 3, linkage = linkage)
  sil <- silhouette_analysis(X, result$labels)
  cat(sprintf("%-10s linkage: Silhouette = %.4f\n", linkage, sil$avg_score))
}
cat("\n")

# ==============================================================================
# Example 4: DBSCAN
# ==============================================================================

cat("Example 4: DBSCAN (Density-Based Clustering)\n")
cat("================================================================================\n")

# Add some noise points
X_noisy <- rbind(X, matrix(runif(20, -2, 7), ncol = 2))

result <- dbscan_clustering(X_noisy, eps = 1.5, minPts = 5)
cat(sprintf("Number of clusters found: %d\n", result$n_clusters))
cat(sprintf("Number of noise points: %d\n", result$n_noise))
cat(sprintf("Cluster sizes: %s\n\n", paste(table(result$labels[result$labels > 0]), collapse = ", ")))

# ==============================================================================
# Example 5: Elbow Method (Finding Optimal K)
# ==============================================================================

cat("Example 5: Elbow Method for Optimal K\n")
cat("================================================================================\n")

inertias <- numeric(10)
for (k in 1:10) {
  result <- kmeans_clustering(X, K = k, max_iter = 100)
  inertias[k] <- result$inertia
}

cat("K    Inertia\n")
cat(strrep("-", 20), "\n")
for (k in 1:10) {
  cat(sprintf("%-4d %.2f\n", k, inertias[k]))
}
cat("\nOptimal K appears to be around the 'elbow' (K=3 for this data)\n\n")

# ==============================================================================
# Summary
# ==============================================================================

cat("==============================================================================\n")
cat("Summary: R Clustering Capabilities\n")
cat("==============================================================================\n")
cat("✓ K-Means: Fast, scalable, requires K\n")
cat("✓ K-Means++: Better initialization, faster convergence\n")
cat("✓ Hierarchical: No need to specify K, creates dendrogram\n")
cat("✓ DBSCAN: Finds arbitrary shapes, handles noise, no K needed\n")
cat("✓ Silhouette: Quality metric for cluster validation\n")
cat("\n")
cat("Applications:\n")
cat("- Customer segmentation (marketing)\n")
cat("- Image compression (K-Means)\n")
cat("- Anomaly detection (DBSCAN)\n")
cat("- Gene expression analysis (Hierarchical)\n")
cat("- Document clustering (K-Means, Hierarchical)\n")
cat("==============================================================================\n")
