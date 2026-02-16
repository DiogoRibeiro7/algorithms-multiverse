/**
 * Machine Learning Examples
 * Demonstrates various ML algorithms for classification, regression, and clustering
 */

import * as ml from '../src/machineLearning.js';

console.log('=== MACHINE LEARNING EXAMPLES ===\n');

// ============================================
// Classification Example: Iris Dataset Simulation
// ============================================

console.log('--- CLASSIFICATION: FLOWER SPECIES PREDICTION ---\n');

// Generate synthetic iris-like dataset
function generateIrisData() {
    const data = [];
    const labels = [];

    // Setosa (class 0): small petals, small sepals
    for (let i = 0; i < 50; i++) {
        data.push([
            4.5 + Math.random() * 1.0,  // sepal length
            3.0 + Math.random() * 0.8,  // sepal width
            1.0 + Math.random() * 0.5,  // petal length
            0.1 + Math.random() * 0.3   // petal width
        ]);
        labels.push(0);
    }

    // Versicolor (class 1): medium petals, medium sepals
    for (let i = 0; i < 50; i++) {
        data.push([
            5.5 + Math.random() * 1.5,  // sepal length
            2.0 + Math.random() * 0.8,  // sepal width
            3.5 + Math.random() * 1.0,  // petal length
            1.0 + Math.random() * 0.5   // petal width
        ]);
        labels.push(1);
    }

    // Virginica (class 2): large petals, large sepals
    for (let i = 0; i < 50; i++) {
        data.push([
            6.0 + Math.random() * 1.5,  // sepal length
            2.5 + Math.random() * 0.8,  // sepal width
            5.0 + Math.random() * 1.0,  // petal length
            1.8 + Math.random() * 0.5   // petal width
        ]);
        labels.push(2);
    }

    return { data, labels };
}

const irisDataset = generateIrisData();
const normalizedData = ml.minMaxNormalize(irisDataset.data);

// Split data
const split = ml.trainTestSplit(normalizedData, irisDataset.labels, 0.3, 42);

console.log(`Dataset: ${irisDataset.data.length} samples, 4 features`);
console.log(`Training set: ${split.X_train.length} samples`);
console.log(`Test set: ${split.X_test.length} samples\n`);

// Test different classifiers
const classifiers = [
    { name: 'K-Nearest Neighbors', model: new ml.KNNClassifier(5) },
    { name: 'Naive Bayes', model: new ml.GaussianNaiveBayes() },
    { name: 'Decision Tree', model: new ml.DecisionTreeClassifier(5, 2) }
];

console.log('Classifier Performance:');
console.log('-'.repeat(40));

for (const { name, model } of classifiers) {
    // Train
    model.fit(split.X_train, split.y_train);

    // Test
    const predictions = model.predict(split.X_test);
    const accuracy = ml.accuracy(split.y_test, predictions);

    // Calculate confusion matrix
    const cm = ml.confusionMatrix(split.y_test, predictions);

    console.log(`${name}:`);
    console.log(`  Accuracy: ${(accuracy * 100).toFixed(2)}%`);
    console.log(`  Confusion Matrix:`);
    for (let i = 0; i < cm.matrix.length; i++) {
        console.log(`    Class ${i}: [${cm.matrix[i].join(', ')}]`);
    }
    console.log('');
}

// ============================================
// Binary Classification: Customer Churn Prediction
// ============================================

console.log('\n--- BINARY CLASSIFICATION: CUSTOMER CHURN ---\n');

// Generate synthetic customer data
function generateCustomerData() {
    const data = [];
    const labels = [];

    // Non-churned customers (class 0)
    for (let i = 0; i < 100; i++) {
        data.push([
            20 + Math.random() * 40,     // age
            12 + Math.random() * 48,     // tenure (months)
            30 + Math.random() * 70,     // monthly charges
            500 + Math.random() * 2000,  // total charges
            Math.random() < 0.7 ? 1 : 0  // has contract
        ]);
        labels.push(0);
    }

    // Churned customers (class 1)
    for (let i = 0; i < 50; i++) {
        data.push([
            18 + Math.random() * 30,     // age (younger)
            1 + Math.random() * 12,      // tenure (shorter)
            60 + Math.random() * 40,     // monthly charges (higher)
            100 + Math.random() * 500,   // total charges (lower)
            Math.random() < 0.3 ? 1 : 0  // has contract (less likely)
        ]);
        labels.push(1);
    }

    return { data, labels };
}

const churnDataset = generateCustomerData();
const churnNormalized = ml.standardize(churnDataset.data);
const churnSplit = ml.trainTestSplit(churnNormalized, churnDataset.labels, 0.3);

console.log(`Dataset: ${churnDataset.data.length} customers`);
console.log(`Features: Age, Tenure, Monthly Charges, Total Charges, Has Contract`);
console.log(`Class distribution: ${churnDataset.labels.filter(l => l === 0).length} retained, ${churnDataset.labels.filter(l => l === 1).length} churned\n`);

// Test binary classifiers
const binaryClassifiers = [
    { name: 'Logistic Regression', model: new ml.LogisticRegression(0.1, 500) },
    { name: 'Perceptron', model: new ml.Perceptron(0.01, 100) }
];

console.log('Binary Classifier Performance:');
console.log('-'.repeat(40));

for (const { name, model } of binaryClassifiers) {
    // Train
    model.fit(churnSplit.X_train, churnSplit.y_train);

    // Test
    const predictions = model.predict(churnSplit.X_test);

    // Calculate metrics
    const acc = ml.accuracy(churnSplit.y_test, predictions);
    const prec = ml.precision(churnSplit.y_test, predictions, 1);
    const rec = ml.recall(churnSplit.y_test, predictions, 1);
    const f1 = ml.f1Score(churnSplit.y_test, predictions, 1);

    console.log(`${name}:`);
    console.log(`  Accuracy: ${(acc * 100).toFixed(2)}%`);
    console.log(`  Precision: ${(prec * 100).toFixed(2)}%`);
    console.log(`  Recall: ${(rec * 100).toFixed(2)}%`);
    console.log(`  F1-Score: ${f1.toFixed(3)}`);
    console.log('');
}

// ============================================
// Regression Example: House Price Prediction
// ============================================

console.log('\n--- REGRESSION: HOUSE PRICE PREDICTION ---\n');

// Generate synthetic house data
function generateHouseData() {
    const data = [];
    const prices = [];

    for (let i = 0; i < 200; i++) {
        const sqft = 500 + Math.random() * 3000;
        const bedrooms = Math.floor(1 + Math.random() * 4);
        const bathrooms = Math.floor(1 + Math.random() * 3);
        const age = Math.floor(Math.random() * 50);

        // Price formula: base + sqft contribution + room contribution - age depreciation + noise
        const price = 50000 + sqft * 150 + bedrooms * 10000 + bathrooms * 5000 - age * 1000 + (Math.random() - 0.5) * 20000;

        data.push([sqft, bedrooms, bathrooms, age]);
        prices.push(price);
    }

    return { data, prices };
}

const houseDataset = generateHouseData();
const houseNormalized = ml.minMaxNormalize(houseDataset.data);
const houseSplit = ml.trainTestSplit(houseNormalized, houseDataset.prices, 0.2);

console.log(`Dataset: ${houseDataset.data.length} houses`);
console.log(`Features: Square Feet, Bedrooms, Bathrooms, Age`);
console.log(`Price range: $${Math.min(...houseDataset.prices).toFixed(0)} - $${Math.max(...houseDataset.prices).toFixed(0)}\n`);

// Train linear regression
const linearReg = new ml.LinearRegression(0.1, 1000);
linearReg.fit(houseSplit.X_train, houseSplit.y_train);

// Make predictions
const housePredictions = linearReg.predict(houseSplit.X_test);

// Calculate metrics
const mse = ml.meanSquaredError(houseSplit.y_test, housePredictions);
const mae = ml.meanAbsoluteError(houseSplit.y_test, housePredictions);
const r2 = ml.r2Score(houseSplit.y_test, housePredictions);

console.log('Linear Regression Results:');
console.log(`  MSE: ${mse.toFixed(2)}`);
console.log(`  MAE: $${mae.toFixed(2)}`);
console.log(`  R² Score: ${r2.toFixed(3)}`);

// Show sample predictions
console.log('\nSample Predictions:');
for (let i = 0; i < 5; i++) {
    console.log(`  House ${i + 1}: Actual=$${houseSplit.y_test[i].toFixed(0)}, Predicted=$${housePredictions[i].toFixed(0)}`);
}

// ============================================
// Clustering Example: Customer Segmentation
// ============================================

console.log('\n\n--- CLUSTERING: CUSTOMER SEGMENTATION ---\n');

// Generate synthetic customer behavior data
function generateCustomerBehaviorData() {
    const data = [];

    // Segment 1: High spenders, frequent buyers
    for (let i = 0; i < 50; i++) {
        data.push([
            500 + Math.random() * 300,  // average transaction
            20 + Math.random() * 10,    // frequency per month
            0.8 + Math.random() * 0.2   // loyalty score
        ]);
    }

    // Segment 2: Low spenders, occasional buyers
    for (let i = 0; i < 60; i++) {
        data.push([
            50 + Math.random() * 100,   // average transaction
            2 + Math.random() * 5,      // frequency per month
            0.3 + Math.random() * 0.3   // loyalty score
        ]);
    }

    // Segment 3: Medium spenders, regular buyers
    for (let i = 0; i < 40; i++) {
        data.push([
            200 + Math.random() * 150,  // average transaction
            8 + Math.random() * 7,      // frequency per month
            0.5 + Math.random() * 0.3   // loyalty score
        ]);
    }

    return data;
}

const customerData = generateCustomerBehaviorData();
const customerNormalized = ml.minMaxNormalize(customerData);

console.log(`Dataset: ${customerData.length} customers`);
console.log(`Features: Avg Transaction Value, Purchase Frequency, Loyalty Score\n`);

// K-Means clustering
console.log('K-Means Clustering (k=3):');
const kmeans = new ml.KMeans(3, 100);
kmeans.fit(customerNormalized);
const kmeansLabels = kmeans.labels;

// Count customers in each cluster
const clusterCounts = [0, 0, 0];
for (const label of kmeansLabels) {
    clusterCounts[label]++;
}

console.log(`  Cluster sizes: ${clusterCounts.join(', ')}`);

// Calculate silhouette score
const silhouetteKMeans = ml.silhouetteScore(customerNormalized, kmeansLabels);
console.log(`  Silhouette Score: ${silhouetteKMeans.toFixed(3)}`);

// Show cluster centers (denormalized for interpretation)
console.log('  Cluster Centers:');
for (let i = 0; i < 3; i++) {
    const center = kmeans.centroids[i];
    // Approximate denormalization
    console.log(`    Cluster ${i}: Avg Transaction=$${(center[0] * 750 + 50).toFixed(0)}, Frequency=${(center[1] * 28 + 2).toFixed(1)}, Loyalty=${center[2].toFixed(2)}`);
}

// DBSCAN clustering
console.log('\nDBSCAN Clustering:');
const dbscan = new ml.DBSCAN(0.15, 5);
dbscan.fit(customerNormalized);
const dbscanLabels = dbscan.labels;

// Count clusters and noise points
const uniqueLabels = [...new Set(dbscanLabels)];
const nClusters = uniqueLabels.filter(l => l !== -1).length;
const noisePoints = dbscanLabels.filter(l => l === -1).length;

console.log(`  Number of clusters: ${nClusters}`);
console.log(`  Noise points: ${noisePoints}`);

// Cluster sizes
const dbscanCounts = {};
for (const label of dbscanLabels) {
    dbscanCounts[label] = (dbscanCounts[label] || 0) + 1;
}
console.log('  Cluster sizes:');
for (const [label, count] of Object.entries(dbscanCounts)) {
    if (label !== '-1') {
        console.log(`    Cluster ${label}: ${count} customers`);
    }
}

// ============================================
// Dimensionality Reduction: PCA Visualization
// ============================================

console.log('\n\n--- DIMENSIONALITY REDUCTION: PCA ---\n');

// Use the iris dataset from earlier
console.log('Applying PCA to Iris dataset (4D → 2D):');

const pca = new ml.PCA(2);
const pcaTransformed = pca.fitTransform(normalizedData);

console.log(`Original dimensions: ${normalizedData[0].length}`);
console.log(`Reduced dimensions: ${pcaTransformed[0].length}`);

const varianceRatio = pca.getExplainedVarianceRatio();
console.log(`Explained variance ratio: [${varianceRatio.map(v => v.toFixed(3)).join(', ')}]`);
console.log(`Total variance preserved: ${(varianceRatio.reduce((sum, v) => sum + v, 0) * 100).toFixed(1)}%`);

// Show sample transformations
console.log('\nSample transformations (first 5 points):');
for (let i = 0; i < 5; i++) {
    console.log(`  Original: [${normalizedData[i].map(v => v.toFixed(2)).join(', ')}]`);
    console.log(`  → PCA: [${pcaTransformed[i].map(v => v.toFixed(2)).join(', ')}]`);
}

// ============================================
// Cross-Validation Example
// ============================================

console.log('\n\n--- MODEL SELECTION WITH CROSS-VALIDATION ---\n');

// Test different k values for KNN
console.log('Finding optimal k for KNN classifier:');

const kValues = [1, 3, 5, 7, 9, 11];
const knnScores = [];

for (const k of kValues) {
    const knn = new ml.KNNClassifier(k);

    // Simple 3-fold cross-validation
    const foldSize = Math.floor(normalizedData.length / 3);
    let totalScore = 0;

    for (let fold = 0; fold < 3; fold++) {
        const testStart = fold * foldSize;
        const testEnd = (fold + 1) * foldSize;

        const X_train = [
            ...normalizedData.slice(0, testStart),
            ...normalizedData.slice(testEnd)
        ];
        const y_train = [
            ...irisDataset.labels.slice(0, testStart),
            ...irisDataset.labels.slice(testEnd)
        ];
        const X_test = normalizedData.slice(testStart, testEnd);
        const y_test = irisDataset.labels.slice(testStart, testEnd);

        knn.fit(X_train, y_train);
        totalScore += knn.score(X_test, y_test);
    }

    const avgScore = totalScore / 3;
    knnScores.push(avgScore);
    console.log(`  k=${k}: Average accuracy = ${(avgScore * 100).toFixed(2)}%`);
}

const bestKIndex = knnScores.indexOf(Math.max(...knnScores));
console.log(`\nBest k value: ${kValues[bestKIndex]} with ${(knnScores[bestKIndex] * 100).toFixed(2)}% accuracy`);

// ============================================
// Feature Importance (from Decision Tree)
// ============================================

console.log('\n\n--- FEATURE IMPORTANCE ANALYSIS ---\n');

console.log('Training Decision Tree on house price data...');

const tree = new ml.DecisionTreeClassifier(10, 5);

// Convert regression to classification (price ranges)
const priceClasses = houseDataset.prices.map(price => {
    if (price < 200000) return 0;  // Low
    if (price < 400000) return 1;  // Medium
    return 2;  // High
});

tree.fit(houseNormalized, priceClasses);

console.log('\nDecision Tree Structure:');
function printTree(node, depth = 0, prefix = 'Root') {
    const indent = '  '.repeat(depth);

    if (node.type === 'leaf') {
        console.log(`${indent}${prefix} → Class ${node.label}`);
    } else {
        console.log(`${indent}${prefix} → Feature ${node.feature} ≤ ${node.threshold.toFixed(3)}`);
        printTree(node.left, depth + 1, 'Left');
        printTree(node.right, depth + 1, 'Right');
    }
}

// Print first few levels only
const maxDepth = 3;
function printTreeLimited(node, depth = 0, prefix = 'Root') {
    if (depth >= maxDepth) {
        console.log('  '.repeat(depth) + '...');
        return;
    }

    const indent = '  '.repeat(depth);

    if (node.type === 'leaf') {
        const className = ['Low', 'Medium', 'High'][node.label];
        console.log(`${indent}${prefix} → ${className} price`);
    } else {
        const featureNames = ['SqFt', 'Bedrooms', 'Bathrooms', 'Age'];
        console.log(`${indent}${prefix} → ${featureNames[node.feature]} ≤ ${node.threshold.toFixed(3)}`);
        printTreeLimited(node.left, depth + 1, 'Left');
        printTreeLimited(node.right, depth + 1, 'Right');
    }
}

printTreeLimited(tree.tree);

console.log('\n=== Machine Learning Examples Completed ===');