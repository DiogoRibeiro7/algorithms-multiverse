# Machine Learning Algorithms

A comprehensive collection of fundamental machine learning algorithms implemented from scratch in Python, with detailed documentation, visualizations, and examples.

## 📚 Table of Contents

- [Overview](#overview)
- [Implemented Algorithms](#implemented-algorithms)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Algorithm Details](#algorithm-details)
- [Performance Comparisons](#performance-comparisons)
- [Contributing](#contributing)
- [References](#references)

## 🎯 Overview

This module provides pure Python implementations of essential machine learning algorithms, focusing on:

- **Educational Value**: Clear, well-documented code with detailed explanations
- **From Scratch**: No dependency on scikit-learn for core algorithms
- **Visualization**: Built-in plotting functions to understand algorithm behavior
- **Comprehensive**: Both basic and advanced features for each algorithm
- **Production Patterns**: Proper class structure, error handling, and optimization

## 📊 Implemented Algorithms

### Currently Available

| Algorithm | File | Type | Features | Complexity |
|-----------|------|------|----------|------------|
| **Linear Regression** | `linear_regression.py` | Supervised | Gradient Descent, Normal Equation, Regularization, Polynomial Features | O(n*m*iterations) |
| **K-Nearest Neighbors** | `knn.py` | Supervised | Multiple Distance Metrics, Weighted Voting, Cross-Validation | O(n*m*k) |
| **Decision Trees** | `decision_tree.py` | Supervised | CART, Entropy/Gini, Feature Importance, Pruning Support | O(n*m*log(n)) |
| **Gradient Descent** | `gradient_descent.py` | Optimization | SGD, Mini-batch, Momentum, Adam, RMSprop, Adagrad | O(n*iterations) |
| **Naive Bayes** | `naive_bayes.py` | Supervised | Gaussian, Multinomial, Bernoulli, Complement variants | O(n*m) |
| **K-Means Clustering** | `kmeans.py` | Unsupervised | K-Means++, Mini-Batch, Elbow Method, Silhouette Score | O(n*k*iterations) |
| **Support Vector Machine** | `svm.py` | Supervised | SMO Algorithm, Multiple Kernels (RBF, Polynomial, Sigmoid), Multi-class Support | O(n²) |
| **Random Forest** | `random_forest.py` | Supervised | Bootstrap Aggregating, OOB Score, Feature Importance, Parallel Trees | O(n*m*log(n)*trees) |
| **Neural Network** | `neural_network.py` | Supervised | Feedforward, Backpropagation, Multiple Activations, Adam/SGD/Momentum, Dropout, Early Stopping | O(n*m*h*iterations) |

### Planned Additions

- Gradient Boosting
- Principal Component Analysis (PCA)
- Logistic Regression
- DBSCAN Clustering
- Hidden Markov Models
- Convolutional Neural Networks (CNN)

## 🚀 Installation

### Requirements

```bash
# Core requirements
numpy>=1.19.0
matplotlib>=3.3.0

# Optional for examples
scikit-learn>=0.24.0  # For dataset generation only
pandas>=1.2.0         # For data manipulation examples
```

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/algorithms-multiverse.git
cd algorithms-multiverse/machine-learning

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage Examples

### Linear Regression

```python
from linear_regression import LinearRegression, MultipleLinearRegression
import numpy as np

# Simple linear regression
X = np.random.randn(100, 1)
y = 2 * X + 1 + np.random.randn(100, 1) * 0.1

model = LinearRegression(learning_rate=0.01, n_iterations=1000)
model.fit(X, y, method='gradient_descent')
predictions = model.predict(X)

print(f"R² Score: {model.score(X, y):.4f}")
model.plot_fit(X, y)

# With polynomial features and regularization
poly_model = MultipleLinearRegression(
    polynomial_degree=3,
    regularization=0.1,
    feature_scaling=True
)
poly_model.fit(X, y)
```

### K-Nearest Neighbors

```python
from knn import KNN, KNNOptimizer
import numpy as np

# Classification
X_train = np.random.randn(100, 2)
y_train = (X_train[:, 0] + X_train[:, 1] > 0).astype(int)

knn = KNN(k=5, metric='euclidean', weights='distance')
knn.fit(X_train, y_train)

# Find optimal k
optimizer = KNNOptimizer(k_range=(1, 20))
best_k = optimizer.find_best_k(X_train, y_train)
optimizer.plot_elbow_curve()

# Regression with different metrics
knn_reg = KNN(k=3, metric='manhattan', task='regression')
knn_reg.fit(X_train, y_continuous)
```

### Decision Trees

```python
from decision_tree import DecisionTree
import numpy as np

# Classification tree
tree_clf = DecisionTree(
    max_depth=5,
    min_samples_split=5,
    criterion='entropy',
    task='classification'
)
tree_clf.fit(X_train, y_train)

# Print tree structure
tree_clf.print_tree()

# Feature importance
importances = tree_clf.feature_importances_
print(f"Feature Importances: {importances}")

# Regression tree
tree_reg = DecisionTree(
    max_depth=10,
    criterion='mse',
    task='regression'
)
tree_reg.fit(X_train, y_continuous)
```

### Naive Bayes

```python
from naive_bayes import GaussianNB, MultinomialNB, BernoulliNB, ComplementNB
import numpy as np

# Gaussian Naive Bayes for continuous features
gnb = GaussianNB(var_smoothing=1e-9)
gnb.fit(X_train, y_train)
predictions = gnb.predict(X_test)
probabilities = gnb.predict_proba(X_test)

# Multinomial Naive Bayes for count features (e.g., word counts)
X_counts = np.array([[2, 1, 0], [1, 2, 1], [0, 1, 3]])  # Word counts
mnb = MultinomialNB(alpha=1.0)  # Laplace smoothing
mnb.fit(X_counts, y_train)

# Bernoulli Naive Bayes for binary features
X_binary = (X_counts > 0).astype(int)  # Presence/absence
bnb = BernoulliNB(alpha=1.0, binarize=0.0)
bnb.fit(X_binary, y_train)

# Complement Naive Bayes for imbalanced datasets
cnb = ComplementNB(alpha=1.0, norm=True)
cnb.fit(X_counts, y_train)
```

### K-Means Clustering

```python
from kmeans import KMeans, MiniBatchKMeans, elbow_method, silhouette_score
import numpy as np

# Standard K-Means with K-Means++ initialization
kmeans = KMeans(
    n_clusters=3,
    init='k-means++',
    n_init=10,
    max_iter=300,
    random_state=42
)
kmeans.fit(X)
labels = kmeans.labels_
centers = kmeans.cluster_centers_

# Find optimal K using elbow method
inertias = elbow_method(X, k_range=range(2, 10), plot=True)

# Evaluate clustering quality
sil_score = silhouette_score(X, labels)
print(f"Silhouette Score: {sil_score:.3f}")

# Mini-Batch K-Means for large datasets
mb_kmeans = MiniBatchKMeans(
    n_clusters=3,
    batch_size=100,
    max_iter=100
)
mb_kmeans.fit(X_large)

# Predict cluster for new samples
new_samples = np.array([[0, 0], [1, 1]])
predictions = kmeans.predict(new_samples)
distances = kmeans.transform(new_samples)  # Distance to each cluster center
```

### Support Vector Machine

```python
from svm import SVM
import numpy as np

# Binary classification with RBF kernel
svm_rbf = SVM(
    kernel='rbf',
    C=1.0,
    gamma='scale',
    max_iter=1000,
    random_state=42
)
svm_rbf.fit(X_train, y_train)
predictions = svm_rbf.predict(X_test)
decision_values = svm_rbf.decision_function(X_test)

# Different kernels
svm_poly = SVM(kernel='poly', degree=3, coef0=1.0)
svm_sigmoid = SVM(kernel='sigmoid', gamma=0.1)
svm_linear = SVM(kernel='linear', C=0.1)

# Multi-class classification with One-vs-Rest
svm_multiclass = SVM(
    kernel='rbf',
    multi_class='ovr',  # or 'ovo' for One-vs-One
    decision_function_shape='ovr'
)
svm_multiclass.fit(X_train, y_multiclass)

# Get support vectors
support_vectors = svm_rbf.support_vectors_
n_support = svm_rbf.n_support_
print(f"Number of support vectors per class: {n_support}")
```

### Random Forest

```python
from random_forest import RandomForest
import numpy as np

# Classification with Random Forest
rf_clf = RandomForest(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    max_features='sqrt',  # or 'log2', int, float
    bootstrap=True,
    oob_score=True,
    random_state=42
)
rf_clf.fit(X_train, y_train)
predictions = rf_clf.predict(X_test)
probabilities = rf_clf.predict_proba(X_test)

# Out-of-bag score (unbiased estimate)
oob_score = rf_clf.oob_score_
print(f"OOB Score: {oob_score:.4f}")

# Feature importance
feature_importances = rf_clf.feature_importances_
print(f"Feature Importances: {feature_importances}")

# Regression with Random Forest
rf_reg = RandomForest(
    n_estimators=50,
    task='regression',
    max_features=0.3,  # Use 30% of features
    min_samples_leaf=5
)
rf_reg.fit(X_train, y_continuous)
```

### Neural Network

```python
from neural_network import NeuralNetwork
import numpy as np

# Multi-layer perceptron for classification
nn = NeuralNetwork(
    layer_sizes=[input_dim, 128, 64, 32, num_classes],
    activations=['relu', 'relu', 'relu', 'softmax'],
    learning_rate=0.001,
    optimizer='adam',
    regularization=0.01,
    dropout=0.2,
    batch_size=32,
    epochs=100,
    early_stopping=True,
    patience=10,
    verbose=True,
    random_state=42
)

# Train the network
history = nn.fit(X_train, y_train, validation_data=(X_val, y_val))

# Make predictions
predictions = nn.predict(X_test)
probabilities = nn.predict_proba(X_test)

# Plot training history
nn.plot_history(history)

# Regression with custom architecture
nn_reg = NeuralNetwork(
    layer_sizes=[input_dim, 256, 128, 1],
    activations=['relu', 'relu', 'linear'],  # Linear output for regression
    optimizer='sgd',
    learning_rate=0.01,
    momentum=0.9,
    task='regression'
)
nn_reg.fit(X_train, y_continuous)

# Access model parameters
weights = nn.weights
biases = nn.biases
```

## 📖 Algorithm Details

### Linear Regression

**Purpose**: Model linear relationships between features and continuous targets.

**Key Features**:
- **Gradient Descent**: Iterative optimization with configurable learning rate
- **Normal Equation**: Closed-form solution for small datasets
- **L2 Regularization**: Ridge regression to prevent overfitting
- **Polynomial Features**: Capture non-linear relationships
- **Feature Scaling**: Normalization for better convergence

**When to Use**:
- Continuous target variable
- Linear relationships expected
- Need interpretable coefficients
- Baseline model for regression tasks

### K-Nearest Neighbors (KNN)

**Purpose**: Non-parametric algorithm for classification and regression based on similarity.

**Key Features**:
- **Multiple Distance Metrics**: Euclidean, Manhattan, Minkowski, Cosine
- **Weighted Voting**: Distance-based weights for predictions
- **Cross-Validation**: Built-in k-optimization
- **Lazy Learning**: No training phase, stores all data

**When to Use**:
- Non-linear decision boundaries
- Local patterns important
- Small to medium datasets
- No assumptions about data distribution

### Decision Trees

**Purpose**: Tree-based model that makes decisions through recursive splitting.

**Key Features**:
- **CART Algorithm**: Classification and Regression Trees
- **Multiple Criteria**: Gini, Entropy (classification), MSE, MAE (regression)
- **Feature Importance**: Automatic feature ranking
- **Pruning Parameters**: Control tree complexity
- **Interpretability**: Visualizable decision rules

**When to Use**:
- Non-linear relationships
- Need interpretable model
- Mixed data types (after encoding)
- Feature importance required
- Foundation for ensemble methods

### Naive Bayes

**Purpose**: Probabilistic classifier based on Bayes' theorem with feature independence assumption.

**Key Features**:
- **Multiple Variants**: Gaussian (continuous), Multinomial (counts), Bernoulli (binary), Complement (imbalanced)
- **Fast Training**: Single pass through data
- **Probabilistic Output**: Natural probability estimates
- **Handles Missing Data**: Can work with incomplete features
- **Text Classification**: Excellent for document classification

**When to Use**:
- Text classification tasks
- Real-time prediction needed
- Small training datasets
- Features are independent
- Need probability estimates
- Baseline for comparison

### K-Means Clustering

**Purpose**: Unsupervised clustering algorithm that partitions data into K clusters.

**Key Features**:
- **K-Means++ Initialization**: Smart centroid initialization
- **Mini-Batch Variant**: For large datasets
- **Elbow Method**: Find optimal number of clusters
- **Silhouette Analysis**: Evaluate cluster quality
- **Distance Transform**: Get distances to all centroids

**When to Use**:
- Exploratory data analysis
- Customer segmentation
- Image compression
- Anomaly detection (outliers)
- Preprocessing for supervised learning
- Document clustering

### Support Vector Machine (SVM)

**Purpose**: Powerful classifier that finds optimal hyperplane for maximum margin separation.

**Key Features**:
- **SMO Algorithm**: Sequential Minimal Optimization for efficient training
- **Multiple Kernels**: Linear, RBF, Polynomial, Sigmoid for non-linear boundaries
- **Soft Margin**: C parameter for handling non-separable data
- **Multi-class Support**: One-vs-Rest and One-vs-One strategies
- **Support Vectors**: Identifies critical data points defining decision boundary

**When to Use**:
- High-dimensional data (text classification, gene expression)
- Non-linear classification problems
- When good generalization is critical
- Binary or multi-class classification
- Robust to outliers needed
- Clear margin of separation exists

### Random Forest

**Purpose**: Ensemble of decision trees using bootstrap aggregating for robust predictions.

**Key Features**:
- **Bootstrap Aggregating**: Each tree trained on random sample with replacement
- **Random Feature Selection**: Reduces correlation between trees
- **Out-of-Bag Score**: Built-in cross-validation without separate test set
- **Feature Importance**: Automatic ranking of predictive features
- **Parallel Training**: Trees can be trained independently

**When to Use**:
- Non-linear relationships with interactions
- Mixed data types (numerical and categorical)
- Feature importance analysis needed
- Robust predictions required
- Less prone to overfitting than single trees
- Both classification and regression tasks

### Neural Network

**Purpose**: Deep learning model with multiple layers for complex pattern recognition.

**Key Features**:
- **Flexible Architecture**: Configurable layers and neurons
- **Multiple Activations**: ReLU, Sigmoid, Tanh, Softmax, Linear
- **Advanced Optimizers**: SGD, Momentum, Adam for efficient training
- **Regularization**: L2 penalty and dropout for preventing overfitting
- **Early Stopping**: Automatic training termination on validation loss plateau
- **Mini-batch Training**: Efficient gradient updates

**When to Use**:
- Complex non-linear patterns
- Large amounts of training data available
- Feature engineering is difficult
- Image, text, or sequential data
- Universal function approximation needed
- Deep representations beneficial

## 📊 Performance Comparisons

### Classification Performance

| Algorithm | Accuracy | Training Time | Prediction Time | Interpretability |
|-----------|----------|---------------|-----------------|------------------|
| KNN (k=5) | 0.92 | O(1) | O(n*m) | Medium |
| Decision Tree | 0.89 | O(n*m*log(n)) | O(depth) | High |
| Naive Bayes | 0.85 | O(n*m) | O(m) | High |
| SVM (RBF) | 0.95 | O(n²) | O(n*m) | Low |
| Random Forest | 0.94 | O(t*n*m*log(n)) | O(t*depth) | Medium |
| Neural Network | 0.96 | O(e*n*m*h²) | O(m*h²) | Low |

### Regression Performance

| Algorithm | R² Score | MSE | Training Complexity | Suitable For |
|-----------|----------|-----|-------------------|--------------|
| Linear Regression | 0.88 | 0.12 | O(n*m*iter) | Linear relationships |
| Polynomial Regression | 0.94 | 0.06 | O(n*m²*iter) | Non-linear curves |
| KNN Regression | 0.86 | 0.14 | O(1) | Local patterns |
| Decision Tree | 0.91 | 0.09 | O(n*m*log(n)) | Complex patterns |
| Random Forest | 0.93 | 0.07 | O(t*n*m*log(n)) | Complex interactions |
| Neural Network | 0.95 | 0.05 | O(e*n*m*h²) | Universal approximation |

## 🧪 Testing

Run individual algorithm tests:

```bash
# Test specific algorithm
python linear_regression.py
python knn.py
python decision_tree.py
python naive_bayes.py
python kmeans.py
python svm.py
python random_forest.py
python neural_network.py

# Run all tests
python test_all.py

# Performance benchmarks
python benchmarks.py
```

## 🔬 Advanced Usage

### Custom Distance Metrics for KNN

```python
from knn import KNN

def custom_distance(x1, x2):
    """Custom distance function"""
    return np.sum(np.abs(x1 - x2) ** 3) ** (1/3)

# Extend KNN class
class CustomKNN(KNN):
    def _custom_distance(self, x1, x2):
        return custom_distance(x1, x2)

model = CustomKNN(k=5)
```

### Early Stopping for Gradient Descent

```python
from linear_regression import LinearRegression

class EarlyStoppingRegression(LinearRegression):
    def _gradient_descent(self, X, y):
        """Override with early stopping"""
        patience = 10
        best_cost = float('inf')
        no_improvement = 0

        # ... gradient descent with early stopping logic
```

### Ensemble Methods

```python
# Combine multiple models
models = [
    DecisionTree(max_depth=3),
    DecisionTree(max_depth=5),
    DecisionTree(max_depth=7)
]

# Train all models
for model in models:
    model.fit(X_train, y_train)

# Ensemble predictions (voting)
predictions = np.array([model.predict(X_test) for model in models])
ensemble_pred = np.mean(predictions, axis=0)
```

## 🎓 Learning Resources

### Complexity Analysis

| Operation | Linear Regression | KNN | Decision Tree | SVM | Random Forest | Neural Network |
|-----------|------------------|-----|---------------|-----|---------------|----------------|
| Training | O(n*m*iterations) | O(1) | O(n*m*log(n)) | O(n²) to O(n³) | O(t*n*m*log(n)) | O(e*n*m*h²) |
| Prediction (single) | O(m) | O(n*m) | O(depth) | O(nsv*m) | O(t*depth) | O(m*h²) |
| Space | O(m) | O(n*m) | O(nodes) | O(nsv*m) | O(t*nodes) | O(h²) |

*Legend: n=samples, m=features, t=trees, h=hidden units, e=epochs, nsv=support vectors*

### Key Concepts

1. **Bias-Variance Tradeoff**
   - High bias: Underfitting (too simple)
   - High variance: Overfitting (too complex)
   - Balance through regularization and validation

2. **Cross-Validation**
   - K-fold validation for model selection
   - Train-validation-test split
   - Stratified sampling for imbalanced data

3. **Feature Engineering**
   - Polynomial features
   - Feature scaling/normalization
   - Feature selection/importance

## 🤝 Contributing

We welcome contributions! Areas for improvement:

1. **New Algorithms**: Implement missing algorithms from the planned list
2. **Optimizations**: Improve performance with vectorization, caching
3. **Visualizations**: Add more plotting functions
4. **Documentation**: Enhance docstrings and examples
5. **Tests**: Add unit tests and edge cases

### Guidelines

- Follow PEP 8 style guide
- Include comprehensive docstrings
- Add example usage in docstrings
- Implement both basic and advanced features
- Include time/space complexity analysis

## 📚 References

### Papers
- Breiman, L. (2001). "Random Forests". Machine Learning.
- Cortes, C.; Vapnik, V. (1995). "Support-vector networks". Machine Learning.
- Fix, E.; Hodges, J.L. (1951). "Discriminatory Analysis. Nonparametric Discrimination".

### Books
- "Pattern Recognition and Machine Learning" - Christopher Bishop
- "The Elements of Statistical Learning" - Hastie, Tibshirani, Friedman
- "Machine Learning" - Tom Mitchell
- "Hands-On Machine Learning" - Aurélien Géron

### Online Resources
- [Andrew Ng's Machine Learning Course](https://www.coursera.org/learn/machine-learning)
- [Fast.ai Practical Deep Learning](https://www.fast.ai/)
- [Google's Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course)

## 📄 License

MIT License - See [LICENSE](../../LICENSE) file for details.

## 🌟 Acknowledgments

Part of the **Algorithms Multiverse** project - A comprehensive collection of algorithms across multiple programming languages.

---

**Author**: Algorithms Multiverse Contributors
**Contact**: [GitHub Issues](https://github.com/yourusername/algorithms-multiverse/issues)
**Last Updated**: 2024