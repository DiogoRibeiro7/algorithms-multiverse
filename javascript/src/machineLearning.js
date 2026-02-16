/**
 * Machine Learning Algorithms Module
 * Comprehensive implementations of fundamental ML algorithms
 */

// ============================================
// Utility Functions
// ============================================

/**
 * Calculate Euclidean distance between two points
 */
export function euclideanDistance(point1, point2) {
    if (point1.length !== point2.length) {
        throw new Error('Points must have the same dimensionality');
    }
    let sum = 0;
    for (let i = 0; i < point1.length; i++) {
        sum += Math.pow(point1[i] - point2[i], 2);
    }
    return Math.sqrt(sum);
}

/**
 * Calculate Manhattan distance
 */
export function manhattanDistance(point1, point2) {
    if (point1.length !== point2.length) {
        throw new Error('Points must have the same dimensionality');
    }
    let sum = 0;
    for (let i = 0; i < point1.length; i++) {
        sum += Math.abs(point1[i] - point2[i]);
    }
    return sum;
}

/**
 * Calculate cosine similarity
 */
export function cosineSimilarity(vec1, vec2) {
    if (vec1.length !== vec2.length) {
        throw new Error('Vectors must have the same dimensionality');
    }
    let dotProduct = 0;
    let norm1 = 0;
    let norm2 = 0;

    for (let i = 0; i < vec1.length; i++) {
        dotProduct += vec1[i] * vec2[i];
        norm1 += vec1[i] * vec1[i];
        norm2 += vec2[i] * vec2[i];
    }

    return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
}

/**
 * Normalize features to [0, 1] range
 */
export function minMaxNormalize(data) {
    if (data.length === 0) return [];

    const features = data[0].length;
    const normalized = data.map(row => [...row]);

    for (let j = 0; j < features; j++) {
        let min = Infinity;
        let max = -Infinity;

        // Find min and max for this feature
        for (let i = 0; i < data.length; i++) {
            if (data[i][j] < min) min = data[i][j];
            if (data[i][j] > max) max = data[i][j];
        }

        // Normalize
        const range = max - min;
        if (range > 0) {
            for (let i = 0; i < data.length; i++) {
                normalized[i][j] = (data[i][j] - min) / range;
            }
        }
    }

    return normalized;
}

/**
 * Standardize features (z-score normalization)
 */
export function standardize(data) {
    if (data.length === 0) return [];

    const features = data[0].length;
    const standardized = data.map(row => [...row]);

    for (let j = 0; j < features; j++) {
        // Calculate mean
        let mean = 0;
        for (let i = 0; i < data.length; i++) {
            mean += data[i][j];
        }
        mean /= data.length;

        // Calculate standard deviation
        let variance = 0;
        for (let i = 0; i < data.length; i++) {
            variance += Math.pow(data[i][j] - mean, 2);
        }
        const stdDev = Math.sqrt(variance / data.length);

        // Standardize
        if (stdDev > 0) {
            for (let i = 0; i < data.length; i++) {
                standardized[i][j] = (data[i][j] - mean) / stdDev;
            }
        }
    }

    return standardized;
}

/**
 * Split data into training and testing sets
 */
export function trainTestSplit(X, y, testSize = 0.2, randomSeed = null) {
    const n = X.length;
    const testCount = Math.floor(n * testSize);

    // Create indices array and shuffle
    const indices = Array.from({length: n}, (_, i) => i);

    // Simple shuffle (use seed for reproducibility if provided)
    if (randomSeed !== null) {
        // Simple seeded random for reproducibility
        let seed = randomSeed;
        for (let i = n - 1; i > 0; i--) {
            seed = (seed * 9301 + 49297) % 233280;
            const j = Math.floor((seed / 233280) * (i + 1));
            [indices[i], indices[j]] = [indices[j], indices[i]];
        }
    } else {
        for (let i = n - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [indices[i], indices[j]] = [indices[j], indices[i]];
        }
    }

    const testIndices = indices.slice(0, testCount);
    const trainIndices = indices.slice(testCount);

    const X_train = trainIndices.map(i => X[i]);
    const X_test = testIndices.map(i => X[i]);
    const y_train = trainIndices.map(i => y[i]);
    const y_test = testIndices.map(i => y[i]);

    return { X_train, X_test, y_train, y_test };
}

// ============================================
// Classification Algorithms
// ============================================

/**
 * K-Nearest Neighbors Classifier
 */
export class KNNClassifier {
    constructor(k = 3, distanceMetric = euclideanDistance) {
        this.k = k;
        this.distanceMetric = distanceMetric;
        this.X_train = null;
        this.y_train = null;
    }

    fit(X, y) {
        this.X_train = X;
        this.y_train = y;
    }

    predict(X) {
        return X.map(sample => this.predictSingle(sample));
    }

    predictSingle(sample) {
        // Calculate distances to all training samples
        const distances = this.X_train.map((trainSample, idx) => ({
            distance: this.distanceMetric(sample, trainSample),
            label: this.y_train[idx]
        }));

        // Sort by distance and get k nearest
        distances.sort((a, b) => a.distance - b.distance);
        const kNearest = distances.slice(0, this.k);

        // Vote for the most common label
        const votes = new Map();
        for (const neighbor of kNearest) {
            votes.set(neighbor.label, (votes.get(neighbor.label) || 0) + 1);
        }

        // Return label with most votes
        let maxVotes = 0;
        let prediction = null;
        for (const [label, count] of votes) {
            if (count > maxVotes) {
                maxVotes = count;
                prediction = label;
            }
        }

        return prediction;
    }

    score(X, y) {
        const predictions = this.predict(X);
        let correct = 0;
        for (let i = 0; i < predictions.length; i++) {
            if (predictions[i] === y[i]) correct++;
        }
        return correct / y.length;
    }
}

/**
 * Naive Bayes Classifier (Gaussian)
 */
export class GaussianNaiveBayes {
    constructor() {
        this.classes = [];
        this.classPriors = {};
        this.featureMeans = {};
        this.featureVars = {};
    }

    fit(X, y) {
        const n = X.length;
        const nFeatures = X[0].length;

        // Get unique classes
        this.classes = [...new Set(y)];

        // Calculate class priors and feature statistics
        for (const cls of this.classes) {
            // Get samples for this class
            const classIndices = y.map((label, idx) => label === cls ? idx : -1)
                                  .filter(idx => idx !== -1);
            const classSamples = classIndices.map(idx => X[idx]);

            // Prior probability
            this.classPriors[cls] = classIndices.length / n;

            // Calculate mean and variance for each feature
            this.featureMeans[cls] = [];
            this.featureVars[cls] = [];

            for (let j = 0; j < nFeatures; j++) {
                const featureValues = classSamples.map(sample => sample[j]);

                // Mean
                const mean = featureValues.reduce((sum, val) => sum + val, 0) / featureValues.length;
                this.featureMeans[cls].push(mean);

                // Variance
                const variance = featureValues.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / featureValues.length;
                this.featureVars[cls].push(variance + 1e-9); // Add small value to avoid division by zero
            }
        }
    }

    gaussianPdf(x, mean, variance) {
        const exponent = -Math.pow(x - mean, 2) / (2 * variance);
        return (1 / Math.sqrt(2 * Math.PI * variance)) * Math.exp(exponent);
    }

    predict(X) {
        return X.map(sample => this.predictSingle(sample));
    }

    predictSingle(sample) {
        const posteriors = {};

        for (const cls of this.classes) {
            let posterior = Math.log(this.classPriors[cls]); // Use log to avoid underflow

            for (let j = 0; j < sample.length; j++) {
                const likelihood = this.gaussianPdf(
                    sample[j],
                    this.featureMeans[cls][j],
                    this.featureVars[cls][j]
                );
                posterior += Math.log(likelihood + 1e-10); // Add small value to avoid log(0)
            }

            posteriors[cls] = posterior;
        }

        // Return class with highest posterior
        let maxPosterior = -Infinity;
        let prediction = null;
        for (const cls of this.classes) {
            if (posteriors[cls] > maxPosterior) {
                maxPosterior = posteriors[cls];
                prediction = cls;
            }
        }

        return prediction;
    }

    score(X, y) {
        const predictions = this.predict(X);
        let correct = 0;
        for (let i = 0; i < predictions.length; i++) {
            if (predictions[i] === y[i]) correct++;
        }
        return correct / y.length;
    }
}

/**
 * Decision Tree Classifier (ID3 algorithm)
 */
export class DecisionTreeClassifier {
    constructor(maxDepth = 5, minSamplesSplit = 2) {
        this.maxDepth = maxDepth;
        this.minSamplesSplit = minSamplesSplit;
        this.tree = null;
    }

    entropy(y) {
        const counts = new Map();
        for (const label of y) {
            counts.set(label, (counts.get(label) || 0) + 1);
        }

        let entropy = 0;
        const total = y.length;
        for (const count of counts.values()) {
            if (count > 0) {
                const p = count / total;
                entropy -= p * Math.log2(p);
            }
        }

        return entropy;
    }

    informationGain(X, y, featureIdx, threshold) {
        const parentEntropy = this.entropy(y);

        // Split data
        const leftIndices = [];
        const rightIndices = [];

        for (let i = 0; i < X.length; i++) {
            if (X[i][featureIdx] <= threshold) {
                leftIndices.push(i);
            } else {
                rightIndices.push(i);
            }
        }

        if (leftIndices.length === 0 || rightIndices.length === 0) {
            return 0;
        }

        // Calculate weighted average entropy of children
        const n = y.length;
        const leftY = leftIndices.map(i => y[i]);
        const rightY = rightIndices.map(i => y[i]);

        const weightedEntropy = (leftIndices.length / n) * this.entropy(leftY) +
                               (rightIndices.length / n) * this.entropy(rightY);

        return parentEntropy - weightedEntropy;
    }

    findBestSplit(X, y) {
        let bestGain = 0;
        let bestFeature = null;
        let bestThreshold = null;

        const nFeatures = X[0].length;

        for (let featureIdx = 0; featureIdx < nFeatures; featureIdx++) {
            // Get unique values for this feature
            const values = [...new Set(X.map(sample => sample[featureIdx]))].sort((a, b) => a - b);

            // Try different thresholds
            for (let i = 0; i < values.length - 1; i++) {
                const threshold = (values[i] + values[i + 1]) / 2;
                const gain = this.informationGain(X, y, featureIdx, threshold);

                if (gain > bestGain) {
                    bestGain = gain;
                    bestFeature = featureIdx;
                    bestThreshold = threshold;
                }
            }
        }

        return { feature: bestFeature, threshold: bestThreshold, gain: bestGain };
    }

    buildTree(X, y, depth = 0) {
        // Check stopping conditions
        const uniqueLabels = [...new Set(y)];

        if (uniqueLabels.length === 1) {
            return { type: 'leaf', label: uniqueLabels[0] };
        }

        if (depth >= this.maxDepth || y.length < this.minSamplesSplit) {
            // Return most common label
            const counts = new Map();
            for (const label of y) {
                counts.set(label, (counts.get(label) || 0) + 1);
            }

            let maxCount = 0;
            let majorityLabel = null;
            for (const [label, count] of counts) {
                if (count > maxCount) {
                    maxCount = count;
                    majorityLabel = label;
                }
            }

            return { type: 'leaf', label: majorityLabel };
        }

        // Find best split
        const split = this.findBestSplit(X, y);

        if (split.gain === 0) {
            // No information gain, return majority label
            const counts = new Map();
            for (const label of y) {
                counts.set(label, (counts.get(label) || 0) + 1);
            }

            let maxCount = 0;
            let majorityLabel = null;
            for (const [label, count] of counts) {
                if (count > maxCount) {
                    maxCount = count;
                    majorityLabel = label;
                }
            }

            return { type: 'leaf', label: majorityLabel };
        }

        // Split data
        const leftIndices = [];
        const rightIndices = [];

        for (let i = 0; i < X.length; i++) {
            if (X[i][split.feature] <= split.threshold) {
                leftIndices.push(i);
            } else {
                rightIndices.push(i);
            }
        }

        const leftX = leftIndices.map(i => X[i]);
        const leftY = leftIndices.map(i => y[i]);
        const rightX = rightIndices.map(i => X[i]);
        const rightY = rightIndices.map(i => y[i]);

        // Recursively build subtrees
        return {
            type: 'split',
            feature: split.feature,
            threshold: split.threshold,
            left: this.buildTree(leftX, leftY, depth + 1),
            right: this.buildTree(rightX, rightY, depth + 1)
        };
    }

    fit(X, y) {
        this.tree = this.buildTree(X, y);
    }

    predictSingle(sample) {
        let node = this.tree;

        while (node.type !== 'leaf') {
            if (sample[node.feature] <= node.threshold) {
                node = node.left;
            } else {
                node = node.right;
            }
        }

        return node.label;
    }

    predict(X) {
        return X.map(sample => this.predictSingle(sample));
    }

    score(X, y) {
        const predictions = this.predict(X);
        let correct = 0;
        for (let i = 0; i < predictions.length; i++) {
            if (predictions[i] === y[i]) correct++;
        }
        return correct / y.length;
    }
}

/**
 * Perceptron Classifier
 */
export class Perceptron {
    constructor(learningRate = 0.01, maxIterations = 1000) {
        this.learningRate = learningRate;
        this.maxIterations = maxIterations;
        this.weights = null;
        this.bias = 0;
    }

    fit(X, y) {
        const nFeatures = X[0].length;
        this.weights = Array(nFeatures).fill(0);
        this.bias = 0;

        // Convert labels to -1 and 1
        const labels = y.map(label => label === 1 ? 1 : -1);

        for (let iter = 0; iter < this.maxIterations; iter++) {
            let errors = 0;

            for (let i = 0; i < X.length; i++) {
                const prediction = this.predictRaw(X[i]);
                const error = labels[i] - prediction;

                if (error !== 0) {
                    errors++;
                    // Update weights
                    for (let j = 0; j < nFeatures; j++) {
                        this.weights[j] += this.learningRate * labels[i] * X[i][j];
                    }
                    this.bias += this.learningRate * labels[i];
                }
            }

            if (errors === 0) break; // Converged
        }
    }

    predictRaw(sample) {
        let sum = this.bias;
        for (let j = 0; j < sample.length; j++) {
            sum += this.weights[j] * sample[j];
        }
        return sum >= 0 ? 1 : -1;
    }

    predict(X) {
        return X.map(sample => {
            const pred = this.predictRaw(sample);
            return pred === 1 ? 1 : 0;
        });
    }

    score(X, y) {
        const predictions = this.predict(X);
        let correct = 0;
        for (let i = 0; i < predictions.length; i++) {
            if (predictions[i] === y[i]) correct++;
        }
        return correct / y.length;
    }
}

// ============================================
// Regression Algorithms
// ============================================

/**
 * Linear Regression
 */
export class LinearRegression {
    constructor(learningRate = 0.01, iterations = 1000) {
        this.learningRate = learningRate;
        this.iterations = iterations;
        this.weights = null;
        this.bias = 0;
    }

    fit(X, y) {
        const nSamples = X.length;
        const nFeatures = X[0].length;

        // Initialize weights
        this.weights = Array(nFeatures).fill(0);
        this.bias = 0;

        // Gradient descent
        for (let iter = 0; iter < this.iterations; iter++) {
            // Calculate predictions
            const predictions = this.predict(X);

            // Calculate gradients
            const dw = Array(nFeatures).fill(0);
            let db = 0;

            for (let i = 0; i < nSamples; i++) {
                const error = predictions[i] - y[i];

                for (let j = 0; j < nFeatures; j++) {
                    dw[j] += error * X[i][j];
                }
                db += error;
            }

            // Update weights
            for (let j = 0; j < nFeatures; j++) {
                this.weights[j] -= this.learningRate * (dw[j] / nSamples);
            }
            this.bias -= this.learningRate * (db / nSamples);
        }
    }

    predict(X) {
        return X.map(sample => {
            let prediction = this.bias;
            for (let j = 0; j < sample.length; j++) {
                prediction += this.weights[j] * sample[j];
            }
            return prediction;
        });
    }

    score(X, y) {
        const predictions = this.predict(X);

        // Calculate R² score
        const yMean = y.reduce((sum, val) => sum + val, 0) / y.length;

        let ssRes = 0; // Residual sum of squares
        let ssTot = 0; // Total sum of squares

        for (let i = 0; i < y.length; i++) {
            ssRes += Math.pow(y[i] - predictions[i], 2);
            ssTot += Math.pow(y[i] - yMean, 2);
        }

        return 1 - (ssRes / ssTot);
    }
}

/**
 * Logistic Regression
 */
export class LogisticRegression {
    constructor(learningRate = 0.01, iterations = 1000) {
        this.learningRate = learningRate;
        this.iterations = iterations;
        this.weights = null;
        this.bias = 0;
    }

    sigmoid(z) {
        return 1 / (1 + Math.exp(-z));
    }

    fit(X, y) {
        const nSamples = X.length;
        const nFeatures = X[0].length;

        // Initialize weights
        this.weights = Array(nFeatures).fill(0);
        this.bias = 0;

        // Gradient descent
        for (let iter = 0; iter < this.iterations; iter++) {
            // Calculate predictions
            const z = X.map(sample => {
                let sum = this.bias;
                for (let j = 0; j < sample.length; j++) {
                    sum += this.weights[j] * sample[j];
                }
                return sum;
            });

            const predictions = z.map(val => this.sigmoid(val));

            // Calculate gradients
            const dw = Array(nFeatures).fill(0);
            let db = 0;

            for (let i = 0; i < nSamples; i++) {
                const error = predictions[i] - y[i];

                for (let j = 0; j < nFeatures; j++) {
                    dw[j] += error * X[i][j];
                }
                db += error;
            }

            // Update weights
            for (let j = 0; j < nFeatures; j++) {
                this.weights[j] -= this.learningRate * (dw[j] / nSamples);
            }
            this.bias -= this.learningRate * (db / nSamples);
        }
    }

    predictProba(X) {
        return X.map(sample => {
            let z = this.bias;
            for (let j = 0; j < sample.length; j++) {
                z += this.weights[j] * sample[j];
            }
            return this.sigmoid(z);
        });
    }

    predict(X) {
        const probas = this.predictProba(X);
        return probas.map(p => p >= 0.5 ? 1 : 0);
    }

    score(X, y) {
        const predictions = this.predict(X);
        let correct = 0;
        for (let i = 0; i < predictions.length; i++) {
            if (predictions[i] === y[i]) correct++;
        }
        return correct / y.length;
    }
}

// ============================================
// Clustering Algorithms
// ============================================

/**
 * K-Means Clustering
 */
export class KMeans {
    constructor(k = 3, maxIterations = 100, tolerance = 1e-4) {
        this.k = k;
        this.maxIterations = maxIterations;
        this.tolerance = tolerance;
        this.centroids = null;
        this.labels = null;
    }

    initializeCentroids(X) {
        const n = X.length;
        const indices = [];

        // K-means++ initialization
        // Choose first centroid randomly
        indices.push(Math.floor(Math.random() * n));

        for (let i = 1; i < this.k; i++) {
            const distances = X.map((point, idx) => {
                if (indices.includes(idx)) return 0;

                // Find minimum distance to existing centroids
                let minDist = Infinity;
                for (const centroidIdx of indices) {
                    const dist = euclideanDistance(point, X[centroidIdx]);
                    if (dist < minDist) minDist = dist;
                }
                return minDist;
            });

            // Choose next centroid with probability proportional to squared distance
            const sumDistances = distances.reduce((sum, d) => sum + d * d, 0);
            let target = Math.random() * sumDistances;
            let cumSum = 0;

            for (let j = 0; j < n; j++) {
                cumSum += distances[j] * distances[j];
                if (cumSum >= target) {
                    indices.push(j);
                    break;
                }
            }
        }

        return indices.map(idx => [...X[idx]]);
    }

    assignClusters(X, centroids) {
        return X.map(point => {
            let minDist = Infinity;
            let label = -1;

            for (let i = 0; i < centroids.length; i++) {
                const dist = euclideanDistance(point, centroids[i]);
                if (dist < minDist) {
                    minDist = dist;
                    label = i;
                }
            }

            return label;
        });
    }

    updateCentroids(X, labels) {
        const nFeatures = X[0].length;
        const newCentroids = [];

        for (let k = 0; k < this.k; k++) {
            const clusterPoints = X.filter((_, idx) => labels[idx] === k);

            if (clusterPoints.length === 0) {
                // No points assigned to this cluster, keep old centroid
                newCentroids.push(this.centroids[k]);
            } else {
                // Calculate mean of cluster points
                const centroid = Array(nFeatures).fill(0);

                for (const point of clusterPoints) {
                    for (let j = 0; j < nFeatures; j++) {
                        centroid[j] += point[j];
                    }
                }

                for (let j = 0; j < nFeatures; j++) {
                    centroid[j] /= clusterPoints.length;
                }

                newCentroids.push(centroid);
            }
        }

        return newCentroids;
    }

    fit(X) {
        // Initialize centroids
        this.centroids = this.initializeCentroids(X);

        for (let iter = 0; iter < this.maxIterations; iter++) {
            // Assign clusters
            const labels = this.assignClusters(X, this.centroids);

            // Update centroids
            const newCentroids = this.updateCentroids(X, labels);

            // Check convergence
            let maxChange = 0;
            for (let i = 0; i < this.k; i++) {
                const change = euclideanDistance(this.centroids[i], newCentroids[i]);
                if (change > maxChange) maxChange = change;
            }

            this.centroids = newCentroids;
            this.labels = labels;

            if (maxChange < this.tolerance) break;
        }

        return this;
    }

    predict(X) {
        return this.assignClusters(X, this.centroids);
    }

    fitPredict(X) {
        this.fit(X);
        return this.labels;
    }

    getInertia() {
        // Sum of squared distances from samples to their closest cluster center
        let inertia = 0;

        for (let i = 0; i < this.labels.length; i++) {
            const dist = euclideanDistance(X[i], this.centroids[this.labels[i]]);
            inertia += dist * dist;
        }

        return inertia;
    }
}

/**
 * DBSCAN Clustering (Density-Based Spatial Clustering)
 */
export class DBSCAN {
    constructor(epsilon = 0.5, minSamples = 5, distanceMetric = euclideanDistance) {
        this.epsilon = epsilon;
        this.minSamples = minSamples;
        this.distanceMetric = distanceMetric;
        this.labels = null;
    }

    getNeighbors(X, pointIdx) {
        const neighbors = [];
        const point = X[pointIdx];

        for (let i = 0; i < X.length; i++) {
            if (i !== pointIdx) {
                const dist = this.distanceMetric(point, X[i]);
                if (dist <= this.epsilon) {
                    neighbors.push(i);
                }
            }
        }

        return neighbors;
    }

    expandCluster(X, labels, pointIdx, neighbors, clusterId) {
        labels[pointIdx] = clusterId;

        let i = 0;
        while (i < neighbors.length) {
            const neighborIdx = neighbors[i];

            if (labels[neighborIdx] === -1) {
                // Noise point, add to cluster
                labels[neighborIdx] = clusterId;
            }

            if (labels[neighborIdx] === undefined) {
                // Unvisited point
                labels[neighborIdx] = clusterId;

                const newNeighbors = this.getNeighbors(X, neighborIdx);
                if (newNeighbors.length >= this.minSamples) {
                    // Add new neighbors to the list
                    neighbors.push(...newNeighbors.filter(n => !neighbors.includes(n)));
                }
            }

            i++;
        }
    }

    fit(X) {
        const n = X.length;
        this.labels = new Array(n);
        let clusterId = 0;

        for (let i = 0; i < n; i++) {
            if (this.labels[i] !== undefined) continue; // Already visited

            const neighbors = this.getNeighbors(X, i);

            if (neighbors.length < this.minSamples) {
                // Mark as noise
                this.labels[i] = -1;
            } else {
                // Start a new cluster
                this.expandCluster(X, this.labels, i, neighbors, clusterId);
                clusterId++;
            }
        }

        return this;
    }

    fitPredict(X) {
        this.fit(X);
        return this.labels;
    }

    getNClusters() {
        if (!this.labels) return 0;
        const uniqueLabels = [...new Set(this.labels)];
        return uniqueLabels.filter(label => label !== -1).length;
    }
}

/**
 * K-Medoids Clustering (PAM - Partitioning Around Medoids)
 */
export class KMedoids {
    constructor(k = 3, maxIterations = 100, distanceMetric = euclideanDistance) {
        this.k = k;
        this.maxIterations = maxIterations;
        this.distanceMetric = distanceMetric;
        this.medoids = null;
        this.labels = null;
    }

    initializeMedoids(X) {
        const n = X.length;
        const indices = new Set();

        // Random initialization
        while (indices.size < this.k) {
            indices.add(Math.floor(Math.random() * n));
        }

        return Array.from(indices);
    }

    assignClusters(X, medoidIndices) {
        return X.map((point, idx) => {
            let minDist = Infinity;
            let label = -1;

            for (let i = 0; i < medoidIndices.length; i++) {
                const dist = this.distanceMetric(point, X[medoidIndices[i]]);
                if (dist < minDist) {
                    minDist = dist;
                    label = i;
                }
            }

            return label;
        });
    }

    calculateCost(X, labels, medoidIndices) {
        let cost = 0;

        for (let i = 0; i < X.length; i++) {
            const medoidIdx = medoidIndices[labels[i]];
            cost += this.distanceMetric(X[i], X[medoidIdx]);
        }

        return cost;
    }

    fit(X) {
        const n = X.length;

        // Initialize medoids
        this.medoids = this.initializeMedoids(X);
        this.labels = this.assignClusters(X, this.medoids);
        let currentCost = this.calculateCost(X, this.labels, this.medoids);

        for (let iter = 0; iter < this.maxIterations; iter++) {
            let improved = false;

            // Try swapping each medoid with each non-medoid
            for (let k = 0; k < this.k; k++) {
                let bestSwap = -1;
                let bestCost = currentCost;

                for (let i = 0; i < n; i++) {
                    if (this.medoids.includes(i)) continue;

                    // Try swapping
                    const newMedoids = [...this.medoids];
                    newMedoids[k] = i;

                    const newLabels = this.assignClusters(X, newMedoids);
                    const newCost = this.calculateCost(X, newLabels, newMedoids);

                    if (newCost < bestCost) {
                        bestCost = newCost;
                        bestSwap = i;
                    }
                }

                if (bestSwap !== -1) {
                    this.medoids[k] = bestSwap;
                    currentCost = bestCost;
                    improved = true;
                }
            }

            this.labels = this.assignClusters(X, this.medoids);

            if (!improved) break;
        }

        return this;
    }

    predict(X) {
        // For new data, assign to nearest medoid
        // Note: This assumes the original training data is available
        throw new Error('Prediction requires access to original training data');
    }

    fitPredict(X) {
        this.fit(X);
        return this.labels;
    }
}

// ============================================
// Dimensionality Reduction
// ============================================

/**
 * Principal Component Analysis (PCA)
 */
export class PCA {
    constructor(nComponents = 2) {
        this.nComponents = nComponents;
        this.mean = null;
        this.components = null;
        this.explainedVariance = null;
    }

    fit(X) {
        const n = X.length;
        const nFeatures = X[0].length;

        // Calculate mean
        this.mean = Array(nFeatures).fill(0);
        for (const sample of X) {
            for (let j = 0; j < nFeatures; j++) {
                this.mean[j] += sample[j];
            }
        }
        for (let j = 0; j < nFeatures; j++) {
            this.mean[j] /= n;
        }

        // Center the data
        const centered = X.map(sample =>
            sample.map((val, j) => val - this.mean[j])
        );

        // Calculate covariance matrix
        const covariance = Array(nFeatures).fill().map(() => Array(nFeatures).fill(0));

        for (let i = 0; i < nFeatures; i++) {
            for (let j = i; j < nFeatures; j++) {
                let sum = 0;
                for (const sample of centered) {
                    sum += sample[i] * sample[j];
                }
                covariance[i][j] = sum / (n - 1);
                covariance[j][i] = covariance[i][j]; // Symmetric
            }
        }

        // Compute eigenvalues and eigenvectors using power iteration
        // Simplified version - for production use, use a proper eigendecomposition
        this.components = [];
        this.explainedVariance = [];

        for (let comp = 0; comp < Math.min(this.nComponents, nFeatures); comp++) {
            // Power iteration to find dominant eigenvector
            let vector = Array(nFeatures).fill().map(() => Math.random());
            let eigenvalue = 0;

            for (let iter = 0; iter < 100; iter++) {
                // Multiply by covariance matrix
                const newVector = Array(nFeatures).fill(0);
                for (let i = 0; i < nFeatures; i++) {
                    for (let j = 0; j < nFeatures; j++) {
                        newVector[i] += covariance[i][j] * vector[j];
                    }
                }

                // Normalize
                eigenvalue = Math.sqrt(newVector.reduce((sum, val) => sum + val * val, 0));
                vector = newVector.map(val => val / eigenvalue);
            }

            this.components.push(vector);
            this.explainedVariance.push(eigenvalue);

            // Deflate the covariance matrix
            for (let i = 0; i < nFeatures; i++) {
                for (let j = 0; j < nFeatures; j++) {
                    covariance[i][j] -= eigenvalue * vector[i] * vector[j];
                }
            }
        }

        return this;
    }

    transform(X) {
        if (!this.components) {
            throw new Error('PCA must be fitted before transform');
        }

        return X.map(sample => {
            // Center the sample
            const centered = sample.map((val, j) => val - this.mean[j]);

            // Project onto components
            const transformed = [];
            for (const component of this.components) {
                let projection = 0;
                for (let j = 0; j < centered.length; j++) {
                    projection += centered[j] * component[j];
                }
                transformed.push(projection);
            }

            return transformed;
        });
    }

    fitTransform(X) {
        this.fit(X);
        return this.transform(X);
    }

    inverseTransform(X) {
        if (!this.components) {
            throw new Error('PCA must be fitted before inverse transform');
        }

        const nFeatures = this.mean.length;

        return X.map(sample => {
            const reconstructed = Array(nFeatures).fill(0);

            // Add contribution from each component
            for (let i = 0; i < sample.length; i++) {
                for (let j = 0; j < nFeatures; j++) {
                    reconstructed[j] += sample[i] * this.components[i][j];
                }
            }

            // Add back the mean
            return reconstructed.map((val, j) => val + this.mean[j]);
        });
    }

    getExplainedVarianceRatio() {
        if (!this.explainedVariance) return null;

        const totalVariance = this.explainedVariance.reduce((sum, val) => sum + val, 0);
        return this.explainedVariance.map(val => val / totalVariance);
    }
}

// ============================================
// Evaluation Metrics
// ============================================

/**
 * Classification metrics
 */
export function accuracy(yTrue, yPred) {
    let correct = 0;
    for (let i = 0; i < yTrue.length; i++) {
        if (yTrue[i] === yPred[i]) correct++;
    }
    return correct / yTrue.length;
}

export function confusionMatrix(yTrue, yPred) {
    const classes = [...new Set([...yTrue, ...yPred])].sort();
    const n = classes.length;
    const matrix = Array(n).fill().map(() => Array(n).fill(0));

    const classToIndex = new Map();
    classes.forEach((cls, idx) => classToIndex.set(cls, idx));

    for (let i = 0; i < yTrue.length; i++) {
        const trueIdx = classToIndex.get(yTrue[i]);
        const predIdx = classToIndex.get(yPred[i]);
        matrix[trueIdx][predIdx]++;
    }

    return { matrix, classes };
}

export function precision(yTrue, yPred, positiveClass = 1) {
    let truePositives = 0;
    let falsePositives = 0;

    for (let i = 0; i < yTrue.length; i++) {
        if (yPred[i] === positiveClass) {
            if (yTrue[i] === positiveClass) {
                truePositives++;
            } else {
                falsePositives++;
            }
        }
    }

    return truePositives / (truePositives + falsePositives);
}

export function recall(yTrue, yPred, positiveClass = 1) {
    let truePositives = 0;
    let falseNegatives = 0;

    for (let i = 0; i < yTrue.length; i++) {
        if (yTrue[i] === positiveClass) {
            if (yPred[i] === positiveClass) {
                truePositives++;
            } else {
                falseNegatives++;
            }
        }
    }

    return truePositives / (truePositives + falseNegatives);
}

export function f1Score(yTrue, yPred, positiveClass = 1) {
    const p = precision(yTrue, yPred, positiveClass);
    const r = recall(yTrue, yPred, positiveClass);

    if (p + r === 0) return 0;
    return 2 * (p * r) / (p + r);
}

/**
 * Regression metrics
 */
export function meanSquaredError(yTrue, yPred) {
    let sum = 0;
    for (let i = 0; i < yTrue.length; i++) {
        sum += Math.pow(yTrue[i] - yPred[i], 2);
    }
    return sum / yTrue.length;
}

export function meanAbsoluteError(yTrue, yPred) {
    let sum = 0;
    for (let i = 0; i < yTrue.length; i++) {
        sum += Math.abs(yTrue[i] - yPred[i]);
    }
    return sum / yTrue.length;
}

export function r2Score(yTrue, yPred) {
    const mean = yTrue.reduce((sum, val) => sum + val, 0) / yTrue.length;

    let ssRes = 0;
    let ssTot = 0;

    for (let i = 0; i < yTrue.length; i++) {
        ssRes += Math.pow(yTrue[i] - yPred[i], 2);
        ssTot += Math.pow(yTrue[i] - mean, 2);
    }

    return 1 - (ssRes / ssTot);
}

/**
 * Clustering metrics
 */
export function silhouetteScore(X, labels) {
    const n = X.length;
    const uniqueLabels = [...new Set(labels)];

    if (uniqueLabels.length === 1) return 0;

    const silhouettes = [];

    for (let i = 0; i < n; i++) {
        const clusterLabel = labels[i];

        // Calculate a(i) - mean distance to points in same cluster
        const sameCluster = [];
        for (let j = 0; j < n; j++) {
            if (i !== j && labels[j] === clusterLabel) {
                sameCluster.push(euclideanDistance(X[i], X[j]));
            }
        }

        if (sameCluster.length === 0) {
            silhouettes.push(0);
            continue;
        }

        const a = sameCluster.reduce((sum, d) => sum + d, 0) / sameCluster.length;

        // Calculate b(i) - min mean distance to points in other clusters
        let b = Infinity;

        for (const otherLabel of uniqueLabels) {
            if (otherLabel === clusterLabel) continue;

            const otherCluster = [];
            for (let j = 0; j < n; j++) {
                if (labels[j] === otherLabel) {
                    otherCluster.push(euclideanDistance(X[i], X[j]));
                }
            }

            if (otherCluster.length > 0) {
                const meanDist = otherCluster.reduce((sum, d) => sum + d, 0) / otherCluster.length;
                if (meanDist < b) b = meanDist;
            }
        }

        const s = (b - a) / Math.max(a, b);
        silhouettes.push(s);
    }

    return silhouettes.reduce((sum, s) => sum + s, 0) / n;
}

// Export all classes and functions as default
export default {
    // Distance metrics
    euclideanDistance,
    manhattanDistance,
    cosineSimilarity,

    // Data preprocessing
    minMaxNormalize,
    standardize,
    trainTestSplit,

    // Classification
    KNNClassifier,
    GaussianNaiveBayes,
    DecisionTreeClassifier,
    Perceptron,
    LogisticRegression,

    // Regression
    LinearRegression,

    // Clustering
    KMeans,
    DBSCAN,
    KMedoids,

    // Dimensionality Reduction
    PCA,

    // Metrics
    accuracy,
    confusionMatrix,
    precision,
    recall,
    f1Score,
    meanSquaredError,
    meanAbsoluteError,
    r2Score,
    silhouetteScore
};