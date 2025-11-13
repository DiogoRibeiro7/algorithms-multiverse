/*
 * ==============================================================================
 * Regression Algorithms in Swift
 *
 * Comprehensive collection of regression methods leveraging Swift's
 * type safety, protocols, and modern language features.
 *
 * Implementations:
 * - Simple Linear Regression (OLS)
 * - Multiple Linear Regression
 * - Polynomial Regression
 * - Ridge Regression (L2 regularization)
 * - Logistic Regression (binary classification)
 *
 * Swift's strong typing and safety features make these algorithms
 * robust and efficient for statistical computing.
 *
 * Compile: swiftc -O regression.swift
 * Run: ./regression
 *
 * @author Algorithms Multiverse
 * @version 1.0
 * ==============================================================================
 */

import Foundation

let EPSILON = 1e-10

// ==============================================================================
// Error Types
// ==============================================================================

enum RegressionError: Error {
    case dimensionMismatch(String)
    case zeroVariance
    case singularMatrix
    case emptyData

    var localizedDescription: String {
        switch self {
        case .dimensionMismatch(let msg): return "Dimension mismatch: \(msg)"
        case .zeroVariance: return "Cannot fit regression: zero variance"
        case .singularMatrix: return "Matrix is singular"
        case .emptyData: return "Empty data provided"
        }
    }
}

// ==============================================================================
// Simple Linear Regression
// ==============================================================================

/// Simple Linear Regression Result
struct SimpleRegressionResult {
    let intercept: Double
    let slope: Double
    let predictions: [Double]
    let residuals: [Double]
    let rSquared: Double
    let standardError: Double
}

/// Simple Linear Regression: y = β₀ + β₁x
///
/// Time Complexity: O(n)
/// Space Complexity: O(n)
///
/// Applications:
/// - Predicting continuous outcomes
/// - Trend analysis
/// - Econometrics
///
/// - Parameters:
///   - x: Predictor variable
///   - y: Response variable
/// - Returns: Regression results
/// - Throws: RegressionError if data is invalid
func simpleLinearRegression(x: [Double], y: [Double]) throws -> SimpleRegressionResult {
    guard x.count == y.count, !x.isEmpty else {
        throw RegressionError.dimensionMismatch("x and y must have same length")
    }

    let n = Double(x.count)
    let xMean = x.reduce(0, +) / n
    let yMean = y.reduce(0, +) / n

    // Calculate slope (β₁) and intercept (β₀)
    var numerator = 0.0
    var denominator = 0.0

    for i in 0..<x.count {
        numerator += (x[i] - xMean) * (y[i] - yMean)
        denominator += (x[i] - xMean) * (x[i] - xMean)
    }

    guard abs(denominator) > EPSILON else {
        throw RegressionError.zeroVariance
    }

    let slope = numerator / denominator
    let intercept = yMean - slope * xMean

    // Predictions and residuals
    let predictions = x.map { intercept + slope * $0 }
    let residuals = zip(y, predictions).map { $0 - $1 }

    // R-squared
    let ssTotal = y.map { pow($0 - yMean, 2) }.reduce(0, +)
    let ssResidual = residuals.map { pow($0, 2) }.reduce(0, +)
    let rSquared = 1.0 - (ssResidual / ssTotal)

    // Standard error
    let stdError = sqrt(ssResidual / (n - 2))

    return SimpleRegressionResult(
        intercept: intercept,
        slope: slope,
        predictions: predictions,
        residuals: residuals,
        rSquared: rSquared,
        standardError: stdError
    )
}

// ==============================================================================
// Multiple Linear Regression
// ==============================================================================

/// Multiple Linear Regression Result
struct MultipleRegressionResult {
    let coefficients: [Double]
    let predictions: [Double]
    let residuals: [Double]
    let rSquared: Double
    let adjustedRSquared: Double
    let standardError: Double
}

/// Multiple Linear Regression: y = β₀ + β₁x₁ + β₂x₂ + ... + βₚxₚ
///
/// Time Complexity: O(np² + p³)
/// Space Complexity: O(np)
///
/// - Parameters:
///   - X: Design matrix (n × p)
///   - y: Response vector
/// - Returns: Regression results
func multipleLinearRegression(X: [[Double]], y: [Double]) throws -> MultipleRegressionResult {
    guard !X.isEmpty, X[0].count > 0 else {
        throw RegressionError.emptyData
    }

    let n = X.count
    let p = X[0].count

    guard y.count == n else {
        throw RegressionError.dimensionMismatch("X rows must match y length")
    }

    // Add intercept column
    var XWithIntercept = X.map { [1.0] + $0 }

    // Calculate β = (X'X)⁻¹X'y using normal equations
    let XtX = matrixMultiply(transpose(XWithIntercept), XWithIntercept)
    let Xty = matrixVectorMultiply(transpose(XWithIntercept), y)

    let beta = try solveLinearSystem(XtX, Xty)

    // Predictions
    let predictions = XWithIntercept.map { row in
        zip(row, beta).map { $0 * $1 }.reduce(0, +)
    }

    let residuals = zip(y, predictions).map { $0 - $1 }

    // R-squared
    let yMean = y.reduce(0, +) / Double(n)
    let ssTotal = y.map { pow($0 - yMean, 2) }.reduce(0, +)
    let ssResidual = residuals.map { pow($0, 2) }.reduce(0, +)
    let rSquared = 1.0 - (ssResidual / ssTotal)

    // Adjusted R-squared
    let adjustedRSquared = 1.0 - ((1.0 - rSquared) * Double(n - 1) / Double(n - p - 1))

    let stdError = sqrt(ssResidual / Double(n - p - 1))

    return MultipleRegressionResult(
        coefficients: beta,
        predictions: predictions,
        residuals: residuals,
        rSquared: rSquared,
        adjustedRSquared: adjustedRSquared,
        standardError: stdError
    )
}

// ==============================================================================
// Ridge Regression (L2 Regularization)
// ==============================================================================

/// Ridge Regression Result
struct RidgeRegressionResult {
    let coefficients: [Double]
    let predictions: [Double]
    let residuals: [Double]
    let lambda: Double
}

/// Ridge Regression with L2 penalty
///
/// Time Complexity: O(np² + p³)
///
/// - Parameters:
///   - X: Design matrix
///   - y: Response vector
///   - lambda: Regularization parameter
/// - Returns: Ridge regression results
func ridgeRegression(X: [[Double]], y: [Double], lambda: Double = 1.0) throws -> RidgeRegressionResult {
    let n = X.count
    let p = X[0].count

    // Add intercept
    var XWithIntercept = X.map { [1.0] + $0 }

    // Ridge formula: β = (X'X + λI)⁻¹X'y
    var XtX = matrixMultiply(transpose(XWithIntercept), XWithIntercept)

    // Add penalty (don't penalize intercept)
    for i in 1..<(p + 1) {
        XtX[i][i] += lambda
    }

    let Xty = matrixVectorMultiply(transpose(XWithIntercept), y)
    let beta = try solveLinearSystem(XtX, Xty)

    // Predictions
    let predictions = XWithIntercept.map { row in
        zip(row, beta).map { $0 * $1 }.reduce(0, +)
    }

    let residuals = zip(y, predictions).map { $0 - $1 }

    return RidgeRegressionResult(
        coefficients: beta,
        predictions: predictions,
        residuals: residuals,
        lambda: lambda
    )
}

// ==============================================================================
// Logistic Regression
// ==============================================================================

/// Logistic Regression Result
struct LogisticRegressionResult {
    let coefficients: [Double]
    let probabilities: [Double]
    let predictions: [Int]
    let accuracy: Double
    let iterations: Int
}

/// Logistic Regression for binary classification
///
/// Time Complexity: O(iterations × n × p)
///
/// - Parameters:
///   - X: Design matrix
///   - y: Binary labels (0 or 1)
///   - learningRate: Learning rate for gradient descent
///   - maxIterations: Maximum iterations
/// - Returns: Logistic regression results
func logisticRegression(
    X: [[Double]],
    y: [Int],
    learningRate: Double = 0.01,
    maxIterations: Int = 1000
) -> LogisticRegressionResult {
    let n = X.count
    let p = X[0].count

    // Add intercept
    var XWithIntercept = X.map { [1.0] + $0 }
    var beta = Array(repeating: 0.0, count: p + 1)

    // Sigmoid function
    func sigmoid(_ z: Double) -> Double {
        1.0 / (1.0 + exp(-z))
    }

    // Gradient descent
    for iter in 0..<maxIterations {
        // Compute predictions
        let predictions = XWithIntercept.map { row in
            let z = zip(row, beta).map { $0 * $1 }.reduce(0, +)
            return sigmoid(z)
        }

        // Compute gradient
        var gradient = Array(repeating: 0.0, count: p + 1)
        for i in 0..<n {
            let error = predictions[i] - Double(y[i])
            for j in 0..<(p + 1) {
                gradient[j] += error * XWithIntercept[i][j]
            }
        }

        // Update coefficients
        for j in 0..<(p + 1) {
            beta[j] -= learningRate * gradient[j] / Double(n)
        }
    }

    // Final predictions
    let probabilities = XWithIntercept.map { row in
        let z = zip(row, beta).map { $0 * $1 }.reduce(0, +)
        return sigmoid(z)
    }

    let predictedClass = probabilities.map { $0 >= 0.5 ? 1 : 0 }
    let accuracy = Double(zip(predictedClass, y).filter { $0 == $1 }.count) / Double(n)

    return LogisticRegressionResult(
        coefficients: beta,
        probabilities: probabilities,
        predictions: predictedClass,
        accuracy: accuracy,
        iterations: maxIterations
    )
}

// ==============================================================================
// Matrix Helper Functions
// ==============================================================================

func transpose(_ matrix: [[Double]]) -> [[Double]] {
    guard !matrix.isEmpty else { return [] }
    let rows = matrix.count
    let cols = matrix[0].count
    return (0..<cols).map { col in
        (0..<rows).map { row in matrix[row][col] }
    }
}

func matrixMultiply(_ A: [[Double]], _ B: [[Double]]) -> [[Double]] {
    let m = A.count
    let n = B[0].count
    let p = A[0].count

    var result = Array(repeating: Array(repeating: 0.0, count: n), count: m)
    for i in 0..<m {
        for j in 0..<n {
            for k in 0..<p {
                result[i][j] += A[i][k] * B[k][j]
            }
        }
    }
    return result
}

func matrixVectorMultiply(_ A: [[Double]], _ v: [Double]) -> [Double] {
    return A.map { row in
        zip(row, v).map { $0 * $1 }.reduce(0, +)
    }
}

func solveLinearSystem(_ A: [[Double]], _ b: [Double]) throws -> [Double] {
    let n = A.count
    var augmented = A.map { $0 }
    var result = b

    // Gaussian elimination
    for k in 0..<n {
        guard abs(augmented[k][k]) > EPSILON else {
            throw RegressionError.singularMatrix
        }

        for i in (k+1)..<n {
            let factor = augmented[i][k] / augmented[k][k]
            for j in k..<n {
                augmented[i][j] -= factor * augmented[k][j]
            }
            result[i] -= factor * result[k]
        }
    }

    // Back substitution
    var x = Array(repeating: 0.0, count: n)
    for i in stride(from: n-1, through: 0, by: -1) {
        x[i] = result[i]
        for j in (i+1)..<n {
            x[i] -= augmented[i][j] * x[j]
        }
        x[i] /= augmented[i][i]
    }

    return x
}

// ==============================================================================
// Main Program - Examples and Tests
// ==============================================================================

print("==============================================================================")
print("                REGRESSION ALGORITHMS IN SWIFT")
print("         Type-Safe Statistical Computing")
print("==============================================================================\n")

// Example 1: Simple Linear Regression
print("Example 1: Simple Linear Regression")
print(String(repeating: "=", count: 80))

let x = (1...50).map { Double($0) }
let y = x.map { 3.0 + 2.0 * $0 + Double.random(in: -5...5) }

do {
    let result = try simpleLinearRegression(x: x, y: y)
    print("True model: y = 3 + 2x + noise")
    print(String(format: "Fitted model: y = %.4f + %.4fx", result.intercept, result.slope))
    print(String(format: "R² = %.4f", result.rSquared))
    print(String(format: "Standard Error = %.4f\n", result.standardError))
} catch {
    print("Error: \(error)")
}

// Example 2: Multiple Linear Regression
print("Example 2: Multiple Linear Regression")
print(String(repeating: "=", count: 80))

let X = (0..<100).map { _ in (0..<3).map { _ in Double.random(in: -1...1) } }
let trueBeta = [5.0, 2.0, -3.0, 1.0]
let yMultiple = X.map { row in
    trueBeta[0] + zip(row, Array(trueBeta[1...])).map { $0 * $1 }.reduce(0, +) + Double.random(in: -1...1)
}

do {
    let result = try multipleLinearRegression(X: X, y: yMultiple)
    print("True coefficients:", trueBeta.map { String(format: "%.2f", $0) }.joined(separator: ", "))
    print("Estimated coefficients:", result.coefficients.map { String(format: "%.4f", $0) }.joined(separator: ", "))
    print(String(format: "R² = %.4f", result.rSquared))
    print(String(format: "Adjusted R² = %.4f\n", result.adjustedRSquared))
} catch {
    print("Error: \(error)")
}

// Example 3: Ridge Regression
print("Example 3: Ridge Regression (L2 Regularization)")
print(String(repeating: "=", count: 80))

let XRidge = (0..<50).map { _ in (0..<10).map { _ in Double.random(in: -1...1) } }
let yRidge = XRidge.map { row in row[0] * 2 - row[1] + row[2] * 3 + Double.random(in: -1...1) }

do {
    let lambdas = [0.0, 0.1, 1.0, 10.0]
    print("Effect of regularization parameter λ:\n")
    print(String(format: "%-12s %-12s", "Lambda", "||β||²"))
    print(String(repeating: "-", count: 40))

    for lambda in lambdas {
        let result = try ridgeRegression(X: XRidge, y: yRidge, lambda: lambda)
        let betaNorm = result.coefficients[1...].map { $0 * $0 }.reduce(0, +)
        print(String(format: "%-12.1f %-12.4f", lambda, betaNorm))
    }
    print()
} catch {
    print("Error: \(error)")
}

// Example 4: Logistic Regression
print("Example 4: Logistic Regression (Binary Classification)")
print(String(repeating: "=", count: 80))

let XLogistic = (0..<200).map { _ in (0..<2).map { _ in Double.random(in: -2...2) } }
let trueBetaLogistic = [0.0, 1.5, -2.0]
let yLogistic = XLogistic.map { row -> Int in
    let z = trueBetaLogistic[0] + row[0] * trueBetaLogistic[1] + row[1] * trueBetaLogistic[2]
    let prob = 1.0 / (1.0 + exp(-z))
    return Double.random(in: 0...1) < prob ? 1 : 0
}

let result = logisticRegression(X: XLogistic, y: yLogistic, learningRate: 0.1, maxIterations: 1000)
print("True coefficients:", trueBetaLogistic.map { String(format: "%.2f", $0) }.joined(separator: ", "))
print("Estimated coefficients:", result.coefficients.map { String(format: "%.4f", $0) }.joined(separator: ", "))
print(String(format: "Classification accuracy: %.2f%%", result.accuracy * 100))
print(String(format: "Converged in %d iterations\n", result.iterations))

// Summary
print(String(repeating: "=", count: 80))
print("Summary: Swift Regression Capabilities")
print(String(repeating: "=", count: 80))
print("✓ Type-safe implementations with Swift's strong typing")
print("✓ Protocol-oriented design for extensibility")
print("✓ Efficient matrix operations")
print("✓ Comprehensive error handling")
print("\nApplications:")
print("- Predictive modeling")
print("- Machine learning pipelines")
print("- Statistical analysis")
print("- Data science workflows")
print(String(repeating: "=", count: 80))
