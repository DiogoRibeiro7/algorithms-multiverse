/*
 * ==============================================================================
 * Clustering Algorithms in Swift
 *
 * Unsupervised learning algorithms for pattern discovery.
 *
 * Implementations:
 * - K-Means Clustering
 * - K-Means++ (smart initialization)
 * - DBSCAN (Density-Based Clustering)
 * - Silhouette Analysis
 *
 * Swift's value types and protocols make these algorithms
 * type-safe and efficient.
 *
 * Compile: swiftc -O clustering.swift
 * Run: ./clustering
 *
 * @author Algorithms Multiverse
 * @version 1.0
 * ==============================================================================
 */

import Foundation

typealias Point = [Double]

// ==============================================================================
// K-Means Clustering
// ==============================================================================

struct KMeansResult {
    let labels: [Int]
    let centers: [Point]
    let inertia: Double
    let iterations: Int
}

/// K-Means Clustering (Lloyd's Algorithm)
///
/// Time Complexity: O(iterations × n × K × d)
/// Space Complexity: O(nK + Kd)
///
/// - Parameters:
///   - data: Data points (n × d)
///   - K: Number of clusters
///   - maxIterations: Maximum iterations
///   - tolerance: Convergence tolerance
/// - Returns: Clustering result
func kMeansClustering(
    data: [Point],
    K: Int,
    maxIterations: Int = 100,
    tolerance: Double = 1e-6
) -> KMeansResult {
    let n = data.count
    let d = data[0].count

    // Random initialization
    var centers = (0..<K).map { _ in data.randomElement()! }
    var labels = Array(repeating: 0, count: n)
    var inertiaOld = Double.infinity

    var iter = 0
    for iteration in 0..<maxIterations {
        iter = iteration + 1

        // Assignment step
        for i in 0..<n {
            var minDist = Double.infinity
            var bestCluster = 0

            for k in 0..<K {
                let dist = euclideanDistance(data[i], centers[k])
                if dist < minDist {
                    minDist = dist
                    bestCluster = k
                }
            }
            labels[i] = bestCluster
        }

        // Update step
        for k in 0..<K {
            let clusterPoints = data.enumerated().filter { labels[$0.offset] == k }.map { $0.element }
            if !clusterPoints.isEmpty {
                centers[k] = (0..<d).map { dim in
                    clusterPoints.map { $0[dim] }.reduce(0, +) / Double(clusterPoints.count)
                }
            }
        }

        // Compute inertia
        var inertia = 0.0
        for i in 0..<n {
            inertia += euclideanDistance(data[i], centers[labels[i]])
        }

        if abs(inertiaOld - inertia) < tolerance {
            break
        }
        inertiaOld = inertia
    }

    return KMeansResult(labels: labels, centers: centers, inertia: inertiaOld, iterations: iter)
}

// ==============================================================================
// K-Means++
// ==============================================================================

/// K-Means++ with smart initialization
///
/// Time Complexity: O(nKd) for init + O(iterations × nKd)
func kMeansPlusPlus(data: [Point], K: Int, maxIterations: Int = 100) -> KMeansResult {
    let n = data.count
    let d = data[0].count

    // K-Means++ initialization
    var centers = [Point]()
    centers.append(data.randomElement()!)

    for _ in 1..<K {
        var distances = data.map { point in
            centers.map { euclideanDistance(point, $0) }.min()!
        }

        // Choose next center with probability proportional to distance²
        let distSquared = distances.map { $0 * $0 }
        let totalDist = distSquared.reduce(0, +)
        let probabilities = distSquared.map { $0 / totalDist }

        let rand = Double.random(in: 0...1)
        var cumulative = 0.0
        var nextCenter = 0

        for (i, prob) in probabilities.enumerated() {
            cumulative += prob
            if rand <= cumulative {
                nextCenter = i
                break
            }
        }

        centers.append(data[nextCenter])
    }

    // Run Lloyd's algorithm with these centers
    var labels = Array(repeating: 0, count: n)

    for _ in 0..<maxIterations {
        // Assignment
        for i in 0..<n {
            var minDist = Double.infinity
            var bestCluster = 0
            for k in 0..<K {
                let dist = euclideanDistance(data[i], centers[k])
                if dist < minDist {
                    minDist = dist
                    bestCluster = k
                }
            }
            labels[i] = bestCluster
        }

        // Update
        for k in 0..<K {
            let clusterPoints = data.enumerated().filter { labels[$0.offset] == k }.map { $0.element }
            if !clusterPoints.isEmpty {
                centers[k] = (0..<d).map { dim in
                    clusterPoints.map { $0[dim] }.reduce(0, +) / Double(clusterPoints.count)
                }
            }
        }
    }

    let inertia = (0..<n).map { euclideanDistance(data[$0], centers[labels[$0]]) }.reduce(0, +)
    return KMeansResult(labels: labels, centers: centers, inertia: inertia, iterations: maxIterations)
}

// ==============================================================================
// DBSCAN
// ==============================================================================

struct DBSCANResult {
    let labels: [Int]  // 0 = noise, >0 = cluster ID
    let numClusters: Int
    let numNoise: Int
}

/// DBSCAN Clustering
///
/// Time Complexity: O(n²) without spatial index
/// Space Complexity: O(n)
///
/// - Parameters:
///   - data: Data points
///   - eps: Neighborhood radius
///   - minPts: Minimum points for core point
/// - Returns: DBSCAN result
func dbscanClustering(data: [Point], eps: Double, minPts: Int) -> DBSCANResult {
    let n = data.count
    var labels = Array(repeating: 0, count: n)
    var visited = Array(repeating: false, count: n)
    var clusterID = 0

    for i in 0..<n {
        if visited[i] { continue }
        visited[i] = true

        // Find neighbors
        let neighbors = (0..<n).filter { euclideanDistance(data[i], data[$0]) <= eps }

        if neighbors.count < minPts {
            labels[i] = 0  // Noise
        } else {
            clusterID += 1
            labels[i] = clusterID

            // Expand cluster
            var seedSet = neighbors.filter { $0 != i }
            var j = 0

            while j < seedSet.count {
                let point = seedSet[j]

                if !visited[point] {
                    visited[point] = true
                    let pointNeighbors = (0..<n).filter { euclideanDistance(data[point], data[$0]) <= eps }

                    if pointNeighbors.count >= minPts {
                        seedSet.append(contentsOf: pointNeighbors.filter { !seedSet.contains($0) })
                    }
                }

                if labels[point] == 0 {
                    labels[point] = clusterID
                }

                j += 1
            }
        }
    }

    let numNoise = labels.filter { $0 == 0 }.count
    return DBSCANResult(labels: labels, numClusters: clusterID, numNoise: numNoise)
}

// ==============================================================================
// Silhouette Analysis
// ==============================================================================

struct SilhouetteResult {
    let scores: [Double]
    let averageScore: Double
}

/// Silhouette Coefficient
///
/// Time Complexity: O(n²)
/// Range: [-1, 1] where 1 = perfect, 0 = boundary, -1 = wrong cluster
func silhouetteAnalysis(data: [Point], labels: [Int]) -> SilhouetteResult {
    let n = data.count
    var scores = Array(repeating: 0.0, count: n)
    let clusters = Set(labels).sorted()

    for i in 0..<n {
        let ownCluster = labels[i]
        let ownClusterPoints = (0..<n).filter { labels[$0] == ownCluster && $0 != i }

        if ownClusterPoints.isEmpty {
            scores[i] = 0.0
            continue
        }

        // a(i): average distance to own cluster
        let a_i = ownClusterPoints.map { euclideanDistance(data[i], data[$0]) }.reduce(0, +) / Double(ownClusterPoints.count)

        // b(i): minimum average distance to other clusters
        var b_i = Double.infinity
        for otherCluster in clusters where otherCluster != ownCluster {
            let otherClusterPoints = (0..<n).filter { labels[$0] == otherCluster }
            if !otherClusterPoints.isEmpty {
                let avgDist = otherClusterPoints.map { euclideanDistance(data[i], data[$0]) }.reduce(0, +) / Double(otherClusterPoints.count)
                b_i = min(b_i, avgDist)
            }
        }

        scores[i] = (b_i - a_i) / max(a_i, b_i)
    }

    return SilhouetteResult(scores: scores, averageScore: scores.reduce(0, +) / Double(n))
}

// ==============================================================================
// Helper Functions
// ==============================================================================

func euclideanDistance(_ p1: Point, _ p2: Point) -> Double {
    sqrt(zip(p1, p2).map { pow($0 - $1, 2) }.reduce(0, +))
}

// ==============================================================================
// Main Program
// ==============================================================================

print("==============================================================================")
print("                CLUSTERING ALGORITHMS IN SWIFT")
print("         Unsupervised Learning & Pattern Recognition")
print("==============================================================================\n")

// Generate synthetic data
func generateClusters(centers: [[Double]], pointsPerCluster: Int, stdDev: Double) -> [Point] {
    var data = [Point]()
    for center in centers {
        for _ in 0..<pointsPerCluster {
            let point = center.map { $0 + Double.random(in: -stdDev...stdDev) }
            data.append(point)
        }
    }
    return data
}

let clusterCenters = [[0.0, 0.0], [5.0, 5.0], [5.0, 0.0]]
let data = generateClusters(centers: clusterCenters, pointsPerCluster: 50, stdDev: 1.0)

// Example 1: K-Means
print("Example 1: K-Means Clustering")
print(String(repeating: "=", count: 80))

let kmeansResult = kMeansClustering(data: data, K: 3)
print(String(format: "Converged in %d iterations", kmeansResult.iterations))
print(String(format: "Final inertia: %.4f", kmeansResult.inertia))

let clusterSizes = (0..<3).map { k in kmeansResult.labels.filter { $0 == k }.count }
print("Cluster sizes:", clusterSizes.map { String($0) }.joined(separator: ", "))

let silhouette = silhouetteAnalysis(data: data, labels: kmeansResult.labels)
print(String(format: "Average silhouette score: %.4f\n", silhouette.averageScore))

// Example 2: K-Means++ vs Standard
print("Example 2: K-Means++ vs Standard K-Means")
print(String(repeating: "=", count: 80))

let resultStandard = kMeansClustering(data: data, K: 3)
let resultPlusPlus = kMeansPlusPlus(data: data, K: 3)

print("Standard K-Means:")
print(String(format: "  Inertia: %.4f", resultStandard.inertia))
print("K-Means++:")
print(String(format: "  Inertia: %.4f", resultPlusPlus.inertia))
print(String(format: "  Improvement: %.2f%%\n", 100 * (resultStandard.inertia - resultPlusPlus.inertia) / resultStandard.inertia))

// Example 3: DBSCAN
print("Example 3: DBSCAN (Density-Based Clustering)")
print(String(repeating: "=", count: 80))

let dbscanResult = dbscanClustering(data: data, eps: 1.5, minPts: 5)
print(String(format: "Number of clusters found: %d", dbscanResult.numClusters))
print(String(format: "Number of noise points: %d\n", dbscanResult.numNoise))

// Summary
print(String(repeating: "=", count: 80))
print("Summary: Swift Clustering Capabilities")
print(String(repeating: "=", count: 80))
print("✓ K-Means: Fast, scalable, requires K")
print("✓ K-Means++: Better initialization, faster convergence")
print("✓ DBSCAN: Finds arbitrary shapes, handles noise")
print("✓ Silhouette: Quality metric for cluster validation")
print("\nApplications:")
print("- Customer segmentation")
print("- Image compression")
print("- Anomaly detection")
print("- Document clustering")
print(String(repeating: "=", count: 80))
