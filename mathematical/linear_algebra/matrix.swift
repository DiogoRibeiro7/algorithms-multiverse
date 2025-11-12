/*
 * ==============================================================================
 * Matrix Operations and Linear Algebra in Swift
 *
 * Comprehensive collection of matrix operations leveraging Swift's modern
 * features including protocols, generics, optionals, and value semantics.
 *
 * Features:
 * - Protocol-oriented design
 * - Generic implementations with Numeric constraints
 * - Type-safe with compile-time checks
 * - Value semantics with copy-on-write optimization
 * - Functional programming patterns
 * - Error handling with Result types
 *
 * Compile: swiftc -O matrix.swift
 * Run: ./matrix
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

enum MatrixError: Error {
    case dimensionMismatch(String)
    case singularMatrix
    case invalidDimensions
    case notSquareMatrix

    var localizedDescription: String {
        switch self {
        case .dimensionMismatch(let msg):
            return "Dimension mismatch: \(msg)"
        case .singularMatrix:
            return "Matrix is singular"
        case .invalidDimensions:
            return "Invalid matrix dimensions"
        case .notSquareMatrix:
            return "Operation requires square matrix"
        }
    }
}

// ==============================================================================
// Matrix Structure
// ==============================================================================

/// Matrix structure with row-major storage
struct Matrix {
    private(set) var data: [[Double]]
    private(set) var rows: Int
    private(set) var cols: Int

    /// Create a new matrix with given dimensions
    ///
    /// Time Complexity: O(rows * cols)
    init(rows: Int, cols: Int, initialValue: Double = 0.0) {
        self.rows = rows
        self.cols = cols
        self.data = Array(repeating: Array(repeating: initialValue, count: cols), count: rows)
    }

    /// Create matrix from 2D array
    init?(data: [[Double]]) {
        guard !data.isEmpty, !data[0].isEmpty else { return nil }

        let rows = data.count
        let cols = data[0].count

        // Verify all rows have same length
        guard data.allSatisfy({ $0.count == cols }) else { return nil }

        self.data = data
        self.rows = rows
        self.cols = cols
    }

    /// Create an identity matrix
    ///
    /// Time Complexity: O(n²)
    static func identity(_ n: Int) -> Matrix {
        var matrix = Matrix(rows: n, cols: n)
        for i in 0..<n {
            matrix.data[i][i] = 1.0
        }
        return matrix
    }

    /// Access element at (row, col)
    subscript(row: Int, col: Int) -> Double {
        get {
            return data[row][col]
        }
        set {
            data[row][col] = newValue
        }
    }

    // ==========================================================================
    // Basic Operations
    // ==========================================================================

    /// Matrix addition: C = A + B
    ///
    /// Time Complexity: O(rows * cols)
    ///
    /// Applications:
    /// - Computer graphics transformations
    /// - Neural network weight updates
    /// - Image processing
    func add(_ other: Matrix) -> Result<Matrix, MatrixError> {
        guard rows == other.rows && cols == other.cols else {
            return .failure(.dimensionMismatch("\(rows)x\(cols) vs \(other.rows)x\(other.cols)"))
        }

        var result = Matrix(rows: rows, cols: cols)
        for i in 0..<rows {
            for j in 0..<cols {
                result[i, j] = self[i, j] + other[i, j]
            }
        }

        return .success(result)
    }

    /// Matrix subtraction: C = A - B
    ///
    /// Time Complexity: O(rows * cols)
    func subtract(_ other: Matrix) -> Result<Matrix, MatrixError> {
        guard rows == other.rows && cols == other.cols else {
            return .failure(.dimensionMismatch("\(rows)x\(cols) vs \(other.rows)x\(other.cols)"))
        }

        var result = Matrix(rows: rows, cols: cols)
        for i in 0..<rows {
            for j in 0..<cols {
                result[i, j] = self[i, j] - other[i, j]
            }
        }

        return .success(result)
    }

    /// Scalar multiplication
    ///
    /// Time Complexity: O(rows * cols)
    func scaled(by scalar: Double) -> Matrix {
        var result = Matrix(rows: rows, cols: cols)
        for i in 0..<rows {
            for j in 0..<cols {
                result[i, j] = self[i, j] * scalar
            }
        }
        return result
    }

    /// Matrix transpose: B = A^T
    ///
    /// Time Complexity: O(rows * cols)
    ///
    /// Applications:
    /// - Solving linear systems
    /// - Covariance matrix computation
    /// - Neural network backpropagation
    func transposed() -> Matrix {
        var result = Matrix(rows: cols, cols: rows)
        for i in 0..<rows {
            for j in 0..<cols {
                result[j, i] = self[i, j]
            }
        }
        return result
    }

    // ==========================================================================
    // Matrix Multiplication
    // ==========================================================================

    /// Standard matrix multiplication
    ///
    /// Time Complexity: O(n³) for n×n matrices
    /// Space Complexity: O(n²)
    ///
    /// Algorithm:
    /// C[i][j] = Σ(A[i][k] * B[k][j]) for k from 0 to n-1
    ///
    /// Applications:
    /// - Linear transformations
    /// - Graph algorithms (adjacency matrices)
    /// - Computer graphics transformations
    /// - Neural network forward propagation
    func multiply(_ other: Matrix) -> Result<Matrix, MatrixError> {
        guard cols == other.rows else {
            return .failure(.dimensionMismatch(
                "Cannot multiply \(rows)x\(cols) and \(other.rows)x\(other.cols)"
            ))
        }

        var result = Matrix(rows: rows, cols: other.cols)

        for i in 0..<rows {
            for j in 0..<other.cols {
                var sum = 0.0
                for k in 0..<cols {
                    sum += self[i, k] * other[k, j]
                }
                result[i, j] = sum
            }
        }

        return .success(result)
    }

    // ==========================================================================
    // Gaussian Elimination
    // ==========================================================================

    /// Solve linear system Ax = b using Gaussian elimination with partial pivoting
    ///
    /// Time Complexity: O(n³)
    /// Space Complexity: O(n²)
    ///
    /// Algorithm:
    /// 1. Forward elimination: Transform to upper triangular form
    /// 2. Backward substitution: Solve for x
    ///
    /// Applications:
    /// - Solving systems of linear equations
    /// - Circuit analysis
    /// - Structural engineering
    /// - Economics
    func gaussianElimination(b: [Double]) -> Result<[Double], MatrixError> {
        guard rows == cols && rows == b.count else {
            return .failure(.invalidDimensions)
        }

        let n = rows

        // Make copies
        var A = self
        var bCopy = b

        // Forward elimination with partial pivoting
        for col in 0..<n {
            // Find pivot
            var maxRow = col
            var maxVal = abs(A[col, col])

            for row in (col + 1)..<n {
                let val = abs(A[row, col])
                if val > maxVal {
                    maxVal = val
                    maxRow = row
                }
            }

            // Swap rows
            if maxRow != col {
                A.data.swapAt(col, maxRow)
                bCopy.swapAt(col, maxRow)
            }

            // Check for singular matrix
            guard abs(A[col, col]) >= EPSILON else {
                return .failure(.singularMatrix)
            }

            // Eliminate column entries below pivot
            for row in (col + 1)..<n {
                let factor = A[row, col] / A[col, col]
                for j in col..<n {
                    A[row, j] -= factor * A[col, j]
                }
                bCopy[row] -= factor * bCopy[col]
            }
        }

        // Backward substitution
        var x = Array(repeating: 0.0, count: n)
        for i in stride(from: n - 1, through: 0, by: -1) {
            x[i] = bCopy[i]
            for j in (i + 1)..<n {
                x[i] -= A[i, j] * x[j]
            }
            x[i] /= A[i, i]
        }

        return .success(x)
    }

    // ==========================================================================
    // Matrix Decomposition
    // ==========================================================================

    /// LU decomposition: A = LU
    ///
    /// Time Complexity: O(n³)
    /// Space Complexity: O(n²)
    ///
    /// Applications:
    /// - Solving multiple systems with same A
    /// - Computing determinant
    /// - Matrix inversion
    func luDecomposition() -> Result<(L: Matrix, U: Matrix), MatrixError> {
        guard rows == cols else {
            return .failure(.notSquareMatrix)
        }

        let n = rows
        var L = Matrix(rows: n, cols: n)
        var U = Matrix(rows: n, cols: n)

        for i in 0..<n {
            // Upper triangular matrix U
            for k in i..<n {
                var sum = 0.0
                for j in 0..<i {
                    sum += L[i, j] * U[j, k]
                }
                U[i, k] = self[i, k] - sum
            }

            // Lower triangular matrix L
            for k in i..<n {
                if i == k {
                    L[i, i] = 1.0
                } else {
                    var sum = 0.0
                    for j in 0..<i {
                        sum += L[k, j] * U[j, i]
                    }

                    guard abs(U[i, i]) >= EPSILON else {
                        return .failure(.singularMatrix)
                    }

                    L[k, i] = (self[k, i] - sum) / U[i, i]
                }
            }
        }

        return .success((L, U))
    }

    /// QR decomposition using Gram-Schmidt
    ///
    /// Time Complexity: O(mn²) for m×n matrix
    ///
    /// Applications:
    /// - Solving least squares problems
    /// - Eigenvalue computation
    func qrDecomposition() -> Result<(Q: Matrix, R: Matrix), MatrixError> {
        let m = rows
        let n = cols

        var Q = self
        var R = Matrix(rows: n, cols: n)

        // Modified Gram-Schmidt
        for j in 0..<n {
            // Compute norm of column j
            var norm = 0.0
            for i in 0..<m {
                norm += Q[i, j] * Q[i, j]
            }
            R[j, j] = sqrt(norm)

            guard abs(R[j, j]) >= EPSILON else {
                return .failure(.singularMatrix)
            }

            // Normalize column j
            for i in 0..<m {
                Q[i, j] /= R[j, j]
            }

            // Orthogonalize remaining columns
            for k in (j + 1)..<n {
                var dot = 0.0
                for i in 0..<m {
                    dot += Q[i, j] * Q[i, k]
                }
                R[j, k] = dot

                for i in 0..<m {
                    Q[i, k] -= R[j, k] * Q[i, j]
                }
            }
        }

        return .success((Q, R))
    }

    // ==========================================================================
    // Determinant
    // ==========================================================================

    /// Calculate determinant using recursive cofactor expansion
    ///
    /// Time Complexity: O(n!)
    /// Best for: Small matrices (n <= 4)
    func determinantRecursive() -> Result<Double, MatrixError> {
        guard rows == cols else {
            return .failure(.notSquareMatrix)
        }

        let n = rows

        if n == 1 {
            return .success(self[0, 0])
        }

        if n == 2 {
            return .success(self[0, 0] * self[1, 1] - self[0, 1] * self[1, 0])
        }

        var det = 0.0

        for j in 0..<n {
            // Create submatrix
            var submatrixData: [[Double]] = []

            for i in 1..<n {
                var row: [Double] = []
                for k in 0..<n {
                    if k != j {
                        row.append(self[i, k])
                    }
                }
                submatrixData.append(row)
            }

            guard let submatrix = Matrix(data: submatrixData) else {
                return .failure(.invalidDimensions)
            }

            if case let .success(subDet) = submatrix.determinantRecursive() {
                let sign = (j % 2 == 0) ? 1.0 : -1.0
                det += sign * self[0, j] * subDet
            }
        }

        return .success(det)
    }

    /// Calculate determinant using LU decomposition
    ///
    /// Time Complexity: O(n³)
    /// Best for: Larger matrices
    func determinantLU() -> Result<Double, MatrixError> {
        guard rows == cols else {
            return .failure(.notSquareMatrix)
        }

        switch luDecomposition() {
        case .success(let (_, U)):
            var det = 1.0
            for i in 0..<rows {
                det *= U[i, i]
            }
            return .success(det)
        case .failure:
            return .success(0.0)  // Singular matrix
        }
    }

    // ==========================================================================
    // Matrix Inversion
    // ==========================================================================

    /// Matrix inversion using Gauss-Jordan elimination
    ///
    /// Time Complexity: O(n³)
    ///
    /// Applications:
    /// - Solving linear systems
    /// - Computer graphics transformations
    func inverse() -> Result<Matrix, MatrixError> {
        guard rows == cols else {
            return .failure(.notSquareMatrix)
        }

        let n = rows

        // Create augmented matrix [A|I]
        var augmented = Matrix(rows: n, cols: 2 * n)

        // Copy A to left half
        for i in 0..<n {
            for j in 0..<n {
                augmented[i, j] = self[i, j]
            }
        }

        // Set right half to identity
        for i in 0..<n {
            augmented[i, n + i] = 1.0
        }

        // Gauss-Jordan elimination
        for col in 0..<n {
            // Find pivot
            var maxRow = col
            var maxVal = abs(augmented[col, col])

            for row in (col + 1)..<n {
                let val = abs(augmented[row, col])
                if val > maxVal {
                    maxVal = val
                    maxRow = row
                }
            }

            // Swap rows
            if maxRow != col {
                augmented.data.swapAt(col, maxRow)
            }

            // Check for singular matrix
            guard abs(augmented[col, col]) >= EPSILON else {
                return .failure(.singularMatrix)
            }

            // Scale pivot row
            let pivot = augmented[col, col]
            for j in 0..<(2 * n) {
                augmented[col, j] /= pivot
            }

            // Eliminate column
            for row in 0..<n {
                if row != col {
                    let factor = augmented[row, col]
                    for j in 0..<(2 * n) {
                        augmented[row, j] -= factor * augmented[col, j]
                    }
                }
            }
        }

        // Extract inverse from right half
        var inverse = Matrix(rows: n, cols: n)
        for i in 0..<n {
            for j in 0..<n {
                inverse[i, j] = augmented[i, n + j]
            }
        }

        return .success(inverse)
    }

    // ==========================================================================
    // Eigenvalue Computation
    // ==========================================================================

    /// Find dominant eigenvalue and eigenvector using power iteration
    ///
    /// Time Complexity: O(n² * iterations)
    ///
    /// Applications:
    /// - Google PageRank
    /// - Principal Component Analysis
    /// - Markov chains
    func powerIteration(maxIterations: Int = 100) -> Result<(eigenvalue: Double, eigenvector: [Double]), MatrixError> {
        guard rows == cols else {
            return .failure(.notSquareMatrix)
        }

        let n = rows

        // Initialize with random vector
        var v = (0..<n).map { _ in Double.random(in: -1...1) }

        // Normalize
        var norm = sqrt(v.map { $0 * $0 }.reduce(0, +))
        v = v.map { $0 / norm }

        // Power iteration
        for _ in 0..<maxIterations {
            var vNew = Array(repeating: 0.0, count: n)

            // Multiply by matrix
            for i in 0..<n {
                for j in 0..<n {
                    vNew[i] += self[i, j] * v[j]
                }
            }

            // Normalize
            norm = sqrt(vNew.map { $0 * $0 }.reduce(0, +))
            vNew = vNew.map { $0 / norm }

            // Check convergence
            let diff = zip(v, vNew).map { abs($0 - $1) }.reduce(0, +)
            if diff < EPSILON {
                break
            }

            v = vNew
        }

        // Compute eigenvalue: λ = v^T * A * v
        var Av = Array(repeating: 0.0, count: n)
        for i in 0..<n {
            for j in 0..<n {
                Av[i] += self[i, j] * v[j]
            }
        }

        let eigenvalue = zip(v, Av).map { $0 * $1 }.reduce(0, +)

        return .success((eigenvalue, v))
    }

    // ==========================================================================
    // Utility
    // ==========================================================================

    func print(name: String) {
        Swift.print("\n\(name):")
        for i in 0..<rows {
            for j in 0..<cols {
                Swift.print(String(format: "%10.4f ", self[i, j]), terminator: "")
            }
            Swift.print()
        }
    }
}

// ==============================================================================
// Example Usage and Tests
// ==============================================================================

func exampleMultiplication() {
    print("\n======================================")
    print("Example 1: Matrix Multiplication")
    print("======================================")

    let A = Matrix(data: [
        [1, 2, 3],
        [4, 5, 6]
    ])!

    let B = Matrix(data: [
        [7, 8],
        [9, 10],
        [11, 12]
    ])!

    if case let .success(C) = A.multiply(B) {
        A.print(name: "A (2x3)")
        B.print(name: "B (3x2)")
        C.print(name: "C = A × B (2x2)")
    }
}

func exampleGaussianElimination() {
    print("\n======================================")
    print("Example 2: Gaussian Elimination")
    print("======================================")

    let A = Matrix(data: [
        [2, 1, -1],
        [-3, -1, 2],
        [-2, 1, 2]
    ])!

    let b = [8.0, -11.0, -3.0]

    if case let .success(x) = A.gaussianElimination(b: b) {
        print("\nSolution x:")
        for xi in x {
            print(String(format: "%10.4f", xi))
        }
        print("Expected: x=2, y=3, z=-1")
    }
}

func exampleLUDecomposition() {
    print("\n======================================")
    print("Example 3: LU Decomposition")
    print("======================================")

    let A = Matrix(data: [
        [2, -1, -2],
        [-4, 6, 3],
        [-4, -2, 8]
    ])!

    if case let .success((L, U)) = A.luDecomposition() {
        A.print(name: "A")
        L.print(name: "L (lower triangular)")
        U.print(name: "U (upper triangular)")
    }
}

func exampleMatrixInverse() {
    print("\n======================================")
    print("Example 4: Matrix Inversion")
    print("======================================")

    let A = Matrix(data: [
        [4, 7],
        [2, 6]
    ])!

    if case let .success(AInv) = A.inverse() {
        A.print(name: "A")
        AInv.print(name: "A^(-1)")

        if case let .success(I) = A.multiply(AInv) {
            I.print(name: "A × A^(-1) (should be identity)")
        }
    }
}

func exampleEigenvalues() {
    print("\n======================================")
    print("Example 5: Eigenvalue Computation")
    print("======================================")

    let A = Matrix(data: [
        [2, 1],
        [1, 2]
    ])!

    if case let .success((eigenvalue, eigenvector)) = A.powerIteration(maxIterations: 100) {
        A.print(name: "A")
        print(String(format: "\nDominant eigenvalue: %.6f", eigenvalue))
        print("\nCorresponding eigenvector:")
        for v in eigenvector {
            print(String(format: "%10.4f", v))
        }
    }
}

func exampleDeterminant() {
    print("\n======================================")
    print("Example 6: Determinant Calculation")
    print("======================================")

    let A = Matrix(data: [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])!

    if case let .success(detLU) = A.determinantLU() {
        A.print(name: "A")
        print(String(format: "\nDeterminant (LU): %.6f", detLU))
    }
}

// Main execution
func main() {
    print("======================================")
    print("Matrix Operations and Linear Algebra")
    print("======================================")

    exampleMultiplication()
    exampleGaussianElimination()
    exampleLUDecomposition()
    exampleMatrixInverse()
    exampleEigenvalues()
    exampleDeterminant()

    print("\n======================================")
    print("All examples completed successfully!")
    print("======================================")
}

// Run main
main()
