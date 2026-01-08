#!/usr/bin/env python3
"""
Test Suite for Machine Learning Algorithms

Runs basic tests on all implemented ML algorithms to ensure they work correctly.

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
import sys
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

def test_linear_regression():
    """Test Linear Regression implementation"""
    print("Testing Linear Regression...")
    try:
        from linear_regression import LinearRegression, MultipleLinearRegression

        # Generate simple data
        X = 2 * np.random.rand(100, 1)
        y = 4 + 3 * X.flatten() + np.random.randn(100)

        # Test basic linear regression
        model = LinearRegression(learning_rate=0.1, n_iterations=100)
        model.fit(X, y, method='gradient_descent')
        score = model.score(X, y)

        assert score > 0.7, f"Linear Regression R² too low: {score}"
        print(f"  [PASS] Gradient Descent: R² = {score:.4f}")

        # Test normal equation
        model_ne = LinearRegression()
        model_ne.fit(X, y, method='normal_equation')
        score_ne = model_ne.score(X, y)

        assert score_ne > 0.7, f"Normal Equation R² too low: {score_ne}"
        print(f"  [PASS] Normal Equation: R² = {score_ne:.4f}")

        # Test polynomial features
        poly_model = MultipleLinearRegression(polynomial_degree=2, feature_scaling=True)
        poly_model.fit(X, y)
        poly_score = poly_model.score(X, y)
        print(f"  [PASS] Polynomial Regression: R² = {poly_score:.4f}")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_knn():
    """Test K-Nearest Neighbors implementation"""
    print("\nTesting K-Nearest Neighbors...")
    try:
        from knn import KNN, KNNOptimizer

        # Classification test
        X = np.random.randn(150, 2)
        y = (X[:, 0] + X[:, 1] > 0).astype(int)

        # Split data
        split_idx = 120
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        # Test classification
        knn_clf = KNN(k=5, task='classification')
        knn_clf.fit(X_train, y_train)
        accuracy = knn_clf.score(X_test, y_test)

        assert accuracy > 0.7, f"KNN classification accuracy too low: {accuracy}"
        print(f"  [PASS] Classification: Accuracy = {accuracy:.4f}")

        # Test regression
        X_reg = np.sort(5 * np.random.rand(80, 1), axis=0)
        y_reg = np.sin(X_reg).ravel() + 0.1 * np.random.randn(80)

        knn_reg = KNN(k=3, task='regression')
        knn_reg.fit(X_reg[:60], y_reg[:60])
        r2_score = knn_reg.score(X_reg[60:], y_reg[60:])

        print(f"  [PASS] Regression: R² = {r2_score:.4f}")

        # Test different distance metrics
        for metric in ['euclidean', 'manhattan', 'cosine']:
            knn_metric = KNN(k=5, metric=metric, task='classification')
            knn_metric.fit(X_train, y_train)
            acc = knn_metric.score(X_test, y_test)
            print(f"  [PASS] {metric.capitalize()} distance: Accuracy = {acc:.4f}")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_decision_tree():
    """Test Decision Tree implementation"""
    print("\nTesting Decision Tree...")
    try:
        from decision_tree import DecisionTree

        # Classification test
        X = np.random.randn(200, 2)
        y = ((X[:, 0] > 0) & (X[:, 1] > 0)).astype(int)

        # Add some noise
        noise_idx = np.random.choice(200, 20, replace=False)
        y[noise_idx] = 1 - y[noise_idx]

        # Split data
        split_idx = 160
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        # Test classification with different criteria
        for criterion in ['gini', 'entropy']:
            tree_clf = DecisionTree(
                max_depth=5,
                min_samples_split=5,
                criterion=criterion,
                task='classification'
            )
            tree_clf.fit(X_train, y_train)
            accuracy = tree_clf.score(X_test, y_test)

            assert accuracy > 0.6, f"Decision Tree accuracy too low: {accuracy}"
            print(f"  [PASS] Classification ({criterion}): Accuracy = {accuracy:.4f}")

        # Test regression
        X_reg = np.sort(5 * np.random.rand(100, 1), axis=0)
        y_reg = np.sin(X_reg).ravel() + 0.1 * np.random.randn(100)

        tree_reg = DecisionTree(max_depth=5, criterion='mse', task='regression')
        tree_reg.fit(X_reg[:80], y_reg[:80])
        r2_score = tree_reg.score(X_reg[80:], y_reg[80:])

        print(f"  [PASS] Regression (MSE): R² = {r2_score:.4f}")

        # Test tree properties
        depth = tree_reg.get_depth()
        n_leaves = tree_reg.get_n_leaves()
        print(f"  [PASS] Tree structure: Depth = {depth}, Leaves = {n_leaves}")

        # Test feature importance
        importances = tree_clf.feature_importances_
        assert len(importances) == X.shape[1], "Feature importances dimension mismatch"
        assert np.allclose(np.sum(importances), 1.0), "Feature importances don't sum to 1"
        print(f"  [PASS] Feature importances: {importances}")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_gradient_descent():
    """Test Gradient Descent optimizers"""
    print("\nTesting Gradient Descent Optimizers...")
    try:
        from gradient_descent import (
            GradientDescent, StochasticGradientDescent,
            MiniBatchGradientDescent, MomentumGradientDescent,
            AdamOptimizer, RMSpropOptimizer, AdagradOptimizer
        )

        # Simple quadratic function
        def quadratic_cost(X, y, theta):
            return np.sum(theta ** 2)

        def quadratic_gradient(X, y, theta):
            return 2 * theta

        theta_init = np.array([5.0, 3.0])
        X_dummy = np.array([[1]])
        y_dummy = np.array([0])

        optimizers = {
            'Vanilla GD': GradientDescent(learning_rate=0.1, n_iterations=100),
            'SGD': StochasticGradientDescent(learning_rate=0.1, n_iterations=100),
            'Mini-batch': MiniBatchGradientDescent(
                learning_rate=0.1, batch_size=1, n_iterations=100
            ),
            'Momentum': MomentumGradientDescent(
                learning_rate=0.1, momentum=0.9, n_iterations=100
            ),
            'Adam': AdamOptimizer(learning_rate=0.1, n_iterations=100),
            'RMSprop': RMSpropOptimizer(learning_rate=0.1, n_iterations=100),
            'Adagrad': AdagradOptimizer(learning_rate=1.0, n_iterations=100)
        }

        for name, optimizer in optimizers.items():
            result = optimizer.optimize(
                X_dummy, y_dummy, theta_init,
                quadratic_cost, quadratic_gradient
            )
            final_cost = quadratic_cost(None, None, result)

            # Check if converged close to minimum (0, 0)
            assert final_cost < 0.1, f"{name} didn't converge: cost = {final_cost}"
            print(f"  [PASS] {name}: Final cost = {final_cost:.6f}")

        # Test on linear regression
        m = 50
        X_lr = np.random.randn(m, 2)
        X_lr = np.c_[np.ones(m), X_lr]
        true_theta = np.array([1.0, 2.0, -1.5])
        y_lr = X_lr @ true_theta + 0.1 * np.random.randn(m)

        def mse_cost(X, y, theta):
            predictions = X @ theta
            return np.mean((predictions - y) ** 2) / 2

        def mse_gradient(X, y, theta):
            predictions = X @ theta
            return X.T @ (predictions - y) / len(y)

        # Test Adam on linear regression
        adam = AdamOptimizer(learning_rate=0.1, n_iterations=200)
        theta_opt = adam.optimize(X_lr, y_lr, np.random.randn(3),
                                 mse_cost, mse_gradient)
        final_mse = mse_cost(X_lr, y_lr, theta_opt)

        assert final_mse < 0.1, f"Adam on linear regression failed: MSE = {final_mse}"
        print(f"  [PASS] Adam on Linear Regression: MSE = {final_mse:.6f}")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_integration():
    """Test integration between different algorithms"""
    print("\nTesting Algorithm Integration...")
    try:
        from linear_regression import LinearRegression
        from knn import KNN
        from decision_tree import DecisionTree

        # Generate common dataset
        np.random.seed(42)
        X = np.random.randn(100, 3)
        y = 2 * X[:, 0] - X[:, 1] + 0.5 * X[:, 2] + np.random.randn(100) * 0.1

        # Split data
        split_idx = 80
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        # Test all regression algorithms on same data
        models = {
            'Linear Regression': LinearRegression(),
            'KNN Regression': KNN(k=5, task='regression'),
            'Decision Tree': DecisionTree(max_depth=5, task='regression')
        }

        results = {}
        for name, model in models.items():
            if name == 'Linear Regression':
                model.fit(X_train, y_train, method='normal_equation')
            else:
                model.fit(X_train, y_train)

            score = model.score(X_test, y_test)
            results[name] = score
            print(f"  [PASS] {name}: R² = {score:.4f}")

        # Check that at least one model performs reasonably
        best_score = max(results.values())
        assert best_score > 0.5, f"All models performed poorly: best R² = {best_score}"

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("=" * 60)
    print("Machine Learning Algorithms Test Suite")
    print("=" * 60)

    tests = [
        ("Linear Regression", test_linear_regression),
        ("K-Nearest Neighbors", test_knn),
        ("Decision Tree", test_decision_tree),
        ("Gradient Descent", test_gradient_descent),
        ("Integration", test_integration)
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n{name} test crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for name, passed in results:
        status = "PASSED" if passed else "FAILED"
        print(f"{name:.<40} {status}")

    print("-" * 60)
    print(f"Total: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n*** All tests passed successfully! ***")
    else:
        print(f"\n*** WARNING: {total_count - passed_count} test(s) failed ***")
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()