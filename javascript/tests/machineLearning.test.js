/**
 * Test suite for Machine Learning algorithms
 */

import * as ml from '../src/machineLearning.js';

console.log('=== MACHINE LEARNING TESTS ===\n');

// Helper function to create simple test data
function createLinearData() {
    const X = [];
    const y = [];
    for (let i = 0; i < 100; i++) {
        const x = i / 10;
        X.push([x]);
        y.push(2 * x + 1 + (Math.random() - 0.5) * 0.1); // y = 2x + 1 + noise
    }
    return { X, y };
}

function createBinaryData() {
    const X = [];
    const y = [];
    // Class 0: centered around (0, 0)
    for (let i = 0; i < 50; i++) {
        X.push([Math.random() - 2, Math.random() - 2]);
        y.push(0);
    }
    // Class 1: centered around (2, 2)
    for (let i = 0; i < 50; i++) {
        X.push([Math.random() + 1, Math.random() + 1]);
        y.push(1);
    }
    return { X, y };
}

function createMulticlassData() {
    const X = [];
    const y = [];
    // Three clusters
    for (let c = 0; c < 3; c++) {
        for (let i = 0; i < 30; i++) {
            X.push([
                c * 3 + Math.random(),
                c * 2 + Math.random()
            ]);
            y.push(c);
        }
    }
    return { X, y };
}

// Test distance metrics
console.log('Testing Distance Metrics...');
const p1 = [0, 0];
const p2 = [3, 4];
console.assert(ml.euclideanDistance(p1, p2) === 5, 'Euclidean distance failed');
console.assert(ml.manhattanDistance(p1, p2) === 7, 'Manhattan distance failed');

const v1 = [1, 0];
const v2 = [0, 1];
console.assert(Math.abs(ml.cosineSimilarity(v1, v2)) < 0.001, 'Cosine similarity failed for orthogonal vectors');
console.log('✓ Distance metrics passed');

// Test data preprocessing
console.log('\nTesting Data Preprocessing...');
const testData = [[0, 100], [50, 200], [100, 300]];
const normalized = ml.minMaxNormalize(testData);
console.assert(normalized[0][0] === 0, 'Min-max normalization failed');
console.assert(normalized[2][0] === 1, 'Min-max normalization failed');

const standardized = ml.standardize([[1, 2], [2, 4], [3, 6]]);
console.assert(Math.abs(standardized[0][0] + 1.224) < 0.01, 'Standardization failed');
console.log('✓ Data preprocessing passed');

// Test train-test split
console.log('\nTesting Train-Test Split...');
const splitData = createBinaryData();
const split = ml.trainTestSplit(splitData.X, splitData.y, 0.2, 42);
console.assert(split.X_train.length === 80, 'Train-test split size failed');
console.assert(split.X_test.length === 20, 'Train-test split size failed');
console.assert(split.y_train.length === 80, 'Train-test split labels failed');
console.log('✓ Train-test split passed');

// Test KNN Classifier
console.log('\nTesting KNN Classifier...');
const knnData = createBinaryData();
const knn = new ml.KNNClassifier(3);
knn.fit(knnData.X, knnData.y);
const knnPred = knn.predict([[0, 0], [2, 2]]);
console.assert(knnPred[0] === 0, 'KNN prediction failed for class 0');
console.assert(knnPred[1] === 1, 'KNN prediction failed for class 1');
const knnScore = knn.score(knnData.X, knnData.y);
console.assert(knnScore > 0.8, 'KNN accuracy too low');
console.log('✓ KNN Classifier passed');

// Test Naive Bayes
console.log('\nTesting Gaussian Naive Bayes...');
const nbData = createBinaryData();
const nb = new ml.GaussianNaiveBayes();
nb.fit(nbData.X, nbData.y);
const nbPred = nb.predict([[-1, -1], [2, 2]]);
console.assert(nbPred[0] === 0, 'Naive Bayes prediction failed for class 0');
console.assert(nbPred[1] === 1, 'Naive Bayes prediction failed for class 1');
console.log('✓ Gaussian Naive Bayes passed');

// Test Decision Tree
console.log('\nTesting Decision Tree Classifier...');
const dtData = createMulticlassData();
const dt = new ml.DecisionTreeClassifier(5, 2);
dt.fit(dtData.X, dtData.y);
console.assert(dt.tree !== null, 'Decision tree not built');
console.assert(dt.tree.type === 'split' || dt.tree.type === 'leaf', 'Invalid tree structure');
const dtScore = dt.score(dtData.X, dtData.y);
console.assert(dtScore > 0.7, 'Decision tree accuracy too low');
console.log('✓ Decision Tree passed');

// Test Perceptron
console.log('\nTesting Perceptron...');
const percData = createBinaryData();
const perceptron = new ml.Perceptron(0.01, 100);
perceptron.fit(percData.X, percData.y);
console.assert(perceptron.weights !== null, 'Perceptron weights not initialized');
console.assert(perceptron.weights.length === 2, 'Perceptron weights dimension mismatch');
const percPred = perceptron.predict([[-1, -1], [2, 2]]);
console.assert(percPred[0] === 0, 'Perceptron prediction failed');
console.log('✓ Perceptron passed');

// Test Linear Regression
console.log('\nTesting Linear Regression...');
const linData = createLinearData();
const linReg = new ml.LinearRegression(0.1, 500);
linReg.fit(linData.X, linData.y);
console.assert(linReg.weights !== null, 'Linear regression weights not initialized');
const linPred = linReg.predict([[0], [1], [2]]);
console.assert(Math.abs(linPred[0] - 1) < 0.5, 'Linear regression prediction failed');
console.assert(Math.abs(linPred[1] - 3) < 0.5, 'Linear regression prediction failed');
const r2 = linReg.score(linData.X, linData.y);
console.assert(r2 > 0.95, 'Linear regression R² score too low');
console.log('✓ Linear Regression passed');

// Test Logistic Regression
console.log('\nTesting Logistic Regression...');
const logData = createBinaryData();
const logReg = new ml.LogisticRegression(0.1, 500);
logReg.fit(logData.X, logData.y);
const logProba = logReg.predictProba([[-2, -2], [2, 2]]);
console.assert(logProba[0] < 0.3, 'Logistic regression probability failed');
console.assert(logProba[1] > 0.7, 'Logistic regression probability failed');
const logScore = logReg.score(logData.X, logData.y);
console.assert(logScore > 0.7, 'Logistic regression accuracy too low');
console.log('✓ Logistic Regression passed');

// Test K-Means
console.log('\nTesting K-Means Clustering...');
const clusterData = createMulticlassData();
const kmeans = new ml.KMeans(3, 50);
kmeans.fit(clusterData.X);
console.assert(kmeans.centroids !== null, 'K-means centroids not initialized');
console.assert(kmeans.centroids.length === 3, 'K-means wrong number of centroids');
console.assert(kmeans.labels !== null, 'K-means labels not assigned');
const kmeansNewLabels = kmeans.predict([[0, 0], [3, 2], [6, 4]]);
console.assert(kmeansNewLabels.length === 3, 'K-means prediction failed');
console.log('✓ K-Means passed');

// Test DBSCAN
console.log('\nTesting DBSCAN Clustering...');
const dbscanData = createMulticlassData();
const dbscan = new ml.DBSCAN(1.5, 3);
dbscan.fit(dbscanData.X);
console.assert(dbscan.labels !== null, 'DBSCAN labels not assigned');
const nClusters = dbscan.getNClusters();
console.assert(nClusters >= 2 && nClusters <= 4, 'DBSCAN found unexpected number of clusters');
console.log('✓ DBSCAN passed');

// Test K-Medoids
console.log('\nTesting K-Medoids Clustering...');
const medoidData = createMulticlassData().X.slice(0, 30); // Smaller dataset for speed
const kmedoids = new ml.KMedoids(3, 20);
kmedoids.fit(medoidData);
console.assert(kmedoids.medoids !== null, 'K-medoids not initialized');
console.assert(kmedoids.medoids.length === 3, 'K-medoids wrong number of medoids');
console.assert(kmedoids.labels !== null, 'K-medoids labels not assigned');
console.log('✓ K-Medoids passed');

// Test PCA
console.log('\nTesting PCA...');
const pcaData = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]];
const pca = new ml.PCA(2);
const transformed = pca.fitTransform(pcaData);
console.assert(transformed.length === pcaData.length, 'PCA transformation length mismatch');
console.assert(transformed[0].length === 2, 'PCA dimension reduction failed');
console.assert(pca.components !== null, 'PCA components not computed');
const varianceRatio = pca.getExplainedVarianceRatio();
console.assert(varianceRatio !== null, 'PCA variance ratio not computed');
console.log('✓ PCA passed');

// Test Classification Metrics
console.log('\nTesting Classification Metrics...');
const yTrue = [0, 0, 1, 1, 0, 1];
const yPred = [0, 1, 1, 1, 0, 0];

const acc = ml.accuracy(yTrue, yPred);
console.assert(Math.abs(acc - 0.667) < 0.01, 'Accuracy calculation failed');

const cm = ml.confusionMatrix(yTrue, yPred);
console.assert(cm.matrix[0][0] === 2, 'Confusion matrix failed');
console.assert(cm.matrix[1][1] === 2, 'Confusion matrix failed');

const prec = ml.precision(yTrue, yPred, 1);
console.assert(Math.abs(prec - 0.667) < 0.01, 'Precision calculation failed');

const rec = ml.recall(yTrue, yPred, 1);
console.assert(Math.abs(rec - 0.667) < 0.01, 'Recall calculation failed');

const f1 = ml.f1Score(yTrue, yPred, 1);
console.assert(Math.abs(f1 - 0.667) < 0.01, 'F1 score calculation failed');

console.log('✓ Classification metrics passed');

// Test Regression Metrics
console.log('\nTesting Regression Metrics...');
const yTrueReg = [1, 2, 3, 4, 5];
const yPredReg = [1.1, 2.2, 2.9, 3.8, 5.1];

const mse = ml.meanSquaredError(yTrueReg, yPredReg);
console.assert(Math.abs(mse - 0.02) < 0.01, 'MSE calculation failed');

const mae = ml.meanAbsoluteError(yTrueReg, yPredReg);
console.assert(Math.abs(mae - 0.14) < 0.01, 'MAE calculation failed');

const r2Metric = ml.r2Score(yTrueReg, yPredReg);
console.assert(r2Metric > 0.98, 'R² score calculation failed');

console.log('✓ Regression metrics passed');

// Test Clustering Metrics
console.log('\nTesting Clustering Metrics...');
const clustData = [[0, 0], [0, 1], [5, 5], [5, 6]];
const clustLabels = [0, 0, 1, 1];
const silhouette = ml.silhouetteScore(clustData, clustLabels);
console.assert(silhouette > 0.5, 'Silhouette score too low for well-separated clusters');
console.log('✓ Clustering metrics passed');

console.log('\n=== All Machine Learning tests completed successfully ===');