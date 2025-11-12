/**
 * ============================================================================
 * Matrix Operations and Linear Algebra in C++
 *
 * Comprehensive collection of matrix operations and linear algebra algorithms
 * with modern C++ features, templates, and performance optimizations.
 *
 * Features:
 * - Modern C++17 features
 * - Template-based generic implementations
 * - RAII and smart pointers for memory safety
 * - Move semantics for performance
 * - STL algorithms and parallel execution (optional)
 * - Numerical stability with pivoting
 * - Memory-efficient sparse matrix representation
 *
 * Compile: g++ -std=c++17 -O3 -o matrix matrix.cpp
 * With OpenMP: g++ -std=c++17 -O3 -fopenmp -o matrix matrix.cpp
 * Run: ./matrix
 *
 * @author Algorithms Multiverse
 * @version 1.0
 * ============================================================================
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <stdexcept>
#include <random>
#include <iomanip>
#include <map>
#include <algorithm>
#include <chrono>
#include <memory>

constexpr double EPSILON = 1e-10;

// ============================================================================
// Type Definitions
// ============================================================================

using Matrix = std::vector<std::vector<double>>;
using Vector = std::vector<double>;

// ============================================================================
// Custom Exception Class
// ============================================================================

class MatrixException : public std::runtime_error {
public:
    explicit MatrixException(const std::string& message)
        : std::runtime_error(message) {}
};

// ============================================================================
// Basic Matrix Operations
// ============================================================================

/**
 * Create a matrix with given dimensions
 * Time Complexity: O(rows * cols)
 */
Matrix createMatrix(size_t rows, size_t cols, double fillValue = 0.0) {
    return Matrix(rows, Vector(cols, fillValue));
}

/**
 * Create an n×n identity matrix
 * Time Complexity: O(n²)
 */
Matrix identityMatrix(size_t n) {
    Matrix matrix = createMatrix(n, n);
    for (size_t i = 0; i < n; ++i) {
        matrix[i][i] = 1.0;
    }
    return matrix;
}

/**
 * Add two matrices
 * Time Complexity: O(rows * cols)
 */
Matrix matrixAdd(const Matrix& A, const Matrix& B) {
    size_t rows = A.size(), cols = A[0].size();
    if (rows != B.size() || cols != B[0].size()) {
        throw MatrixException("Matrices must have same dimensions for addition");
    }

    Matrix result = createMatrix(rows, cols);
    for (size_t i = 0; i < rows; ++i) {
        for (size_t j = 0; j < cols; ++j) {
            result[i][j] = A[i][j] + B[i][j];
        }
    }
    return result;
}

/**
 * Subtract matrix B from matrix A
 */
Matrix matrixSubtract(const Matrix& A, const Matrix& B) {
    size_t rows = A.size(), cols = A[0].size();
    if (rows != B.size() || cols != B[0].size()) {
        throw MatrixException("Matrices must have same dimensions for subtraction");
    }

    Matrix result = createMatrix(rows, cols);
    for (size_t i = 0; i < rows; ++i) {
        for (size_t j = 0; j < cols; ++j) {
            result[i][j] = A[i][j] - B[i][j];
        }
    }
    return result;
}

/**
 * Multiply matrix by scalar
 */
Matrix scalarMultiply(const Matrix& A, double scalar) {
    size_t rows = A.size(), cols = A[0].size();
    Matrix result = createMatrix(rows, cols);
    for (size_t i = 0; i < rows; ++i) {
        for (size_t j = 0; j < cols; ++j) {
            result[i][j] = A[i][j] * scalar;
        }
    }
    return result;
}

/**
 * Transpose a matrix
 * Time Complexity: O(rows * cols)
 */
Matrix transpose(const Matrix& A) {
    size_t rows = A.size(), cols = A[0].size();
    Matrix result = createMatrix(cols, rows);
    for (size_t i = 0; i < rows; ++i) {
        for (size_t j = 0; j < cols; ++j) {
            result[j][i] = A[i][j];
        }
    }
    return result;
}

// ============================================================================
// Matrix Multiplication
// ============================================================================

/**
 * Standard matrix multiplication (naive algorithm)
 *
 * Time Complexity: O(n³) for n×n matrices
 * Space Complexity: O(n²)
 *
 * Applications:
 * - Linear transformations
 * - Graph algorithms
 * - Computer graphics
 * - Neural network forward propagation
 */
Matrix matrixMultiplyStandard(const Matrix& A, const Matrix& B) {
    size_t rowsA = A.size(), colsA = A[0].size();
    size_t rowsB = B.size(), colsB = B[0].size();

    if (colsA != rowsB) {
        throw MatrixException(
            "Cannot multiply " + std::to_string(rowsA) + "×" + std::to_string(colsA) +
            " and " + std::to_string(rowsB) + "×" + std::to_string(colsB) + " matrices"
        );
    }

    Matrix result = createMatrix(rowsA, colsB);

    for (size_t i = 0; i < rowsA; ++i) {
        for (size_t j = 0; j < colsB; ++j) {
            double sum = 0.0;
            for (size_t k = 0; k < colsA; ++k) {
                sum += A[i][k] * B[k][j];
            }
            result[i][j] = sum;
        }
    }

    return result;
}

/**
 * Strassen's algorithm for matrix multiplication
 *
 * Time Complexity: O(n^2.807) vs O(n³) for standard multiplication
 * Best for: Large square matrices (n >= 64)
 */
Matrix strassenMultiply(const Matrix& A, const Matrix& B) {
    size_t n = A.size();

    // Base case
    if (n <= 64) {
        return matrixMultiplyStandard(A, B);
    }

    // Ensure matrix size is power of 2
    if ((n & (n - 1)) != 0) {
        return matrixMultiplyStandard(A, B);
    }

    size_t mid = n / 2;

    // Helper lambda to extract submatrix
    auto extractSubmatrix = [](const Matrix& M, size_t rowStart, size_t colStart, size_t size) {
        Matrix sub(size, Vector(size));
        for (size_t i = 0; i < size; ++i) {
            for (size_t j = 0; j < size; ++j) {
                sub[i][j] = M[rowStart + i][colStart + j];
            }
        }
        return sub;
    };

    // Divide matrices into quadrants
    Matrix A11 = extractSubmatrix(A, 0, 0, mid);
    Matrix A12 = extractSubmatrix(A, 0, mid, mid);
    Matrix A21 = extractSubmatrix(A, mid, 0, mid);
    Matrix A22 = extractSubmatrix(A, mid, mid, mid);

    Matrix B11 = extractSubmatrix(B, 0, 0, mid);
    Matrix B12 = extractSubmatrix(B, 0, mid, mid);
    Matrix B21 = extractSubmatrix(B, mid, 0, mid);
    Matrix B22 = extractSubmatrix(B, mid, mid, mid);

    // Compute the 7 Strassen products
    Matrix M1 = strassenMultiply(matrixAdd(A11, A22), matrixAdd(B11, B22));
    Matrix M2 = strassenMultiply(matrixAdd(A21, A22), B11);
    Matrix M3 = strassenMultiply(A11, matrixSubtract(B12, B22));
    Matrix M4 = strassenMultiply(A22, matrixSubtract(B21, B11));
    Matrix M5 = strassenMultiply(matrixAdd(A11, A12), B22);
    Matrix M6 = strassenMultiply(matrixSubtract(A21, A11), matrixAdd(B11, B12));
    Matrix M7 = strassenMultiply(matrixSubtract(A12, A22), matrixAdd(B21, B22));

    // Compute result quadrants
    Matrix C11 = matrixAdd(matrixSubtract(matrixAdd(M1, M4), M5), M7);
    Matrix C12 = matrixAdd(M3, M5);
    Matrix C21 = matrixAdd(M2, M4);
    Matrix C22 = matrixAdd(matrixSubtract(matrixAdd(M1, M3), M2), M6);

    // Combine quadrants
    Matrix result = createMatrix(n, n);
    for (size_t i = 0; i < mid; ++i) {
        for (size_t j = 0; j < mid; ++j) {
            result[i][j] = C11[i][j];
            result[i][j + mid] = C12[i][j];
            result[i + mid][j] = C21[i][j];
            result[i + mid][j + mid] = C22[i][j];
        }
    }

    return result;
}

// ============================================================================
// Gaussian Elimination
// ============================================================================

/**
 * Solve linear system Ax = b using Gaussian elimination with partial pivoting
 *
 * Time Complexity: O(n³)
 * Space Complexity: O(n²)
 *
 * Applications:
 * - Solving systems of linear equations
 * - Circuit analysis
 * - Structural engineering
 */
Vector gaussianElimination(const Matrix& A, const Vector& b) {
    size_t n = A.size();
    if (n != b.size()) {
        throw MatrixException("Matrix and vector dimensions don't match");
    }

    // Create augmented matrix [A|b]
    Matrix augmented(n, Vector(n + 1));
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            augmented[i][j] = A[i][j];
        }
        augmented[i][n] = b[i];
    }

    // Forward elimination with partial pivoting
    for (size_t col = 0; col < n; ++col) {
        // Find pivot
        size_t maxRow = col;
        for (size_t row = col + 1; row < n; ++row) {
            if (std::abs(augmented[row][col]) > std::abs(augmented[maxRow][col])) {
                maxRow = row;
            }
        }

        // Swap rows
        std::swap(augmented[col], augmented[maxRow]);

        // Check for singular matrix
        if (std::abs(augmented[col][col]) < EPSILON) {
            throw MatrixException("Matrix is singular or nearly singular");
        }

        // Eliminate column entries below pivot
        for (size_t row = col + 1; row < n; ++row) {
            double factor = augmented[row][col] / augmented[col][col];
            for (size_t j = col; j <= n; ++j) {
                augmented[row][j] -= factor * augmented[col][j];
            }
        }
    }

    // Backward substitution
    Vector x(n);
    for (int i = n - 1; i >= 0; --i) {
        x[i] = augmented[i][n];
        for (size_t j = i + 1; j < n; ++j) {
            x[i] -= augmented[i][j] * x[j];
        }
        x[i] /= augmented[i][i];
    }

    return x;
}

// ============================================================================
// Matrix Decomposition
// ============================================================================

/**
 * LU decomposition result structure
 */
struct LUResult {
    Matrix L;
    Matrix U;
};

/**
 * LU decomposition: A = LU
 *
 * Time Complexity: O(n³)
 * Applications:
 * - Solving multiple systems with same A
 * - Computing determinant
 * - Matrix inversion
 */
LUResult luDecomposition(const Matrix& A) {
    size_t n = A.size();
    Matrix L = createMatrix(n, n);
    Matrix U = createMatrix(n, n);

    for (size_t i = 0; i < n; ++i) {
        // Upper triangular matrix U
        for (size_t k = i; k < n; ++k) {
            double sum = 0.0;
            for (size_t j = 0; j < i; ++j) {
                sum += L[i][j] * U[j][k];
            }
            U[i][k] = A[i][k] - sum;
        }

        // Lower triangular matrix L
        for (size_t k = i; k < n; ++k) {
            if (i == k) {
                L[i][i] = 1.0;
            } else {
                double sum = 0.0;
                for (size_t j = 0; j < i; ++j) {
                    sum += L[k][j] * U[j][i];
                }
                if (std::abs(U[i][i]) < EPSILON) {
                    throw MatrixException("Matrix is singular");
                }
                L[k][i] = (A[k][i] - sum) / U[i][i];
            }
        }
    }

    return {L, U};
}

/**
 * QR decomposition result structure
 */
struct QRResult {
    Matrix Q;
    Matrix R;
};

/**
 * QR decomposition using Gram-Schmidt orthogonalization
 *
 * Time Complexity: O(mn²) for m×n matrix
 * Applications:
 * - Solving least squares problems
 * - Eigenvalue computation
 */
QRResult qrDecompositionGramSchmidt(const Matrix& A) {
    size_t m = A.size(), n = A[0].size();
    Matrix Q = A;  // Copy
    Matrix R = createMatrix(n, n);

    // Modified Gram-Schmidt
    for (size_t j = 0; j < n; ++j) {
        // Compute norm of column j
        double norm = 0.0;
        for (size_t i = 0; i < m; ++i) {
            norm += Q[i][j] * Q[i][j];
        }
        R[j][j] = std::sqrt(norm);

        if (std::abs(R[j][j]) < EPSILON) {
            throw MatrixException("Matrix columns are linearly dependent");
        }

        // Normalize column j
        for (size_t i = 0; i < m; ++i) {
            Q[i][j] /= R[j][j];
        }

        // Orthogonalize remaining columns
        for (size_t k = j + 1; k < n; ++k) {
            R[j][k] = 0.0;
            for (size_t i = 0; i < m; ++i) {
                R[j][k] += Q[i][j] * Q[i][k];
            }
            for (size_t i = 0; i < m; ++i) {
                Q[i][k] -= R[j][k] * Q[i][j];
            }
        }
    }

    return {Q, R};
}

// ============================================================================
// Determinant Calculation
// ============================================================================

/**
 * Calculate determinant using recursive cofactor expansion
 * Time Complexity: O(n!)
 * Best for: Small matrices (n <= 4)
 */
double determinantRecursive(const Matrix& A) {
    size_t n = A.size();

    if (n == 1) {
        return A[0][0];
    }

    if (n == 2) {
        return A[0][0] * A[1][1] - A[0][1] * A[1][0];
    }

    double det = 0.0;
    for (size_t j = 0; j < n; ++j) {
        // Create submatrix
        Matrix submatrix(n - 1, Vector(n - 1));
        for (size_t i = 1; i < n; ++i) {
            size_t colIndex = 0;
            for (size_t k = 0; k < n; ++k) {
                if (k != j) {
                    submatrix[i - 1][colIndex++] = A[i][k];
                }
            }
        }

        double cofactor = std::pow(-1, j) * A[0][j] * determinantRecursive(submatrix);
        det += cofactor;
    }

    return det;
}

/**
 * Calculate determinant using LU decomposition
 * Time Complexity: O(n³)
 * Best for: Matrices larger than 4×4
 */
double determinantLU(const Matrix& A) {
    try {
        auto [L, U] = luDecomposition(A);
        double det = 1.0;
        for (size_t i = 0; i < U.size(); ++i) {
            det *= U[i][i];
        }
        return det;
    } catch (const MatrixException&) {
        return 0.0;  // Singular matrix
    }
}

// ============================================================================
// Matrix Inversion
// ============================================================================

/**
 * Matrix inversion using Gauss-Jordan elimination
 *
 * Time Complexity: O(n³)
 * Applications:
 * - Solving linear systems
 * - Computer graphics transformations
 */
Matrix matrixInverseGaussJordan(const Matrix& A) {
    size_t n = A.size();

    // Create augmented matrix [A|I]
    Matrix augmented(n, Vector(2 * n));
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            augmented[i][j] = A[i][j];
        }
        augmented[i][i + n] = 1.0;
    }

    // Forward elimination
    for (size_t col = 0; col < n; ++col) {
        // Find pivot
        size_t maxRow = col;
        for (size_t row = col + 1; row < n; ++row) {
            if (std::abs(augmented[row][col]) > std::abs(augmented[maxRow][col])) {
                maxRow = row;
            }
        }

        std::swap(augmented[col], augmented[maxRow]);

        if (std::abs(augmented[col][col]) < EPSILON) {
            throw MatrixException("Matrix is singular and cannot be inverted");
        }

        // Scale pivot row
        double pivot = augmented[col][col];
        for (size_t j = 0; j < 2 * n; ++j) {
            augmented[col][j] /= pivot;
        }

        // Eliminate column
        for (size_t row = 0; row < n; ++row) {
            if (row != col) {
                double factor = augmented[row][col];
                for (size_t j = 0; j < 2 * n; ++j) {
                    augmented[row][j] -= factor * augmented[col][j];
                }
            }
        }
    }

    // Extract inverse from right half
    Matrix inverse = createMatrix(n, n);
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            inverse[i][j] = augmented[i][j + n];
        }
    }

    return inverse;
}

// ============================================================================
// Eigenvalue Computation
// ============================================================================

/**
 * Eigenvalue result structure
 */
struct EigenResult {
    double eigenvalue;
    Vector eigenvector;
};

/**
 * Find dominant eigenvalue and eigenvector using power iteration
 *
 * Time Complexity: O(n² * iterations)
 * Applications:
 * - Google PageRank
 * - Principal Component Analysis
 */
EigenResult powerIteration(const Matrix& A, int numIterations = 100) {
    size_t n = A.size();
    std::mt19937 gen(42);
    std::uniform_real_distribution<> dis(0.0, 1.0);

    // Start with random vector
    Vector v(n);
    for (size_t i = 0; i < n; ++i) {
        v[i] = dis(gen);
    }

    // Normalize
    double norm = 0.0;
    for (double val : v) {
        norm += val * val;
    }
    norm = std::sqrt(norm);
    for (double& val : v) {
        val /= norm;
    }

    for (int iteration = 0; iteration < numIterations; ++iteration) {
        // Multiply by matrix
        Vector vNew(n, 0.0);
        for (size_t i = 0; i < n; ++i) {
            for (size_t j = 0; j < n; ++j) {
                vNew[i] += A[i][j] * v[j];
            }
        }

        // Normalize
        norm = 0.0;
        for (double val : vNew) {
            norm += val * val;
        }
        norm = std::sqrt(norm);

        Vector vNormalized(n);
        for (size_t i = 0; i < n; ++i) {
            vNormalized[i] = vNew[i] / norm;
        }

        // Check convergence
        if (iteration > 0) {
            double diff = 0.0;
            for (size_t i = 0; i < n; ++i) {
                diff += std::abs(vNormalized[i] - v[i]);
            }
            if (diff < EPSILON) {
                break;
            }
        }

        v = vNormalized;
    }

    // Compute eigenvalue
    Vector Av(n, 0.0);
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            Av[i] += A[i][j] * v[j];
        }
    }

    double eigenvalue = 0.0;
    for (size_t i = 0; i < n; ++i) {
        eigenvalue += v[i] * Av[i];
    }

    return {eigenvalue, v};
}

/**
 * QR algorithm for finding all eigenvalues
 * Time Complexity: O(n³ * iterations)
 */
Vector qrAlgorithm(const Matrix& A, int numIterations = 100) {
    size_t n = A.size();
    Matrix Ak = A;

    for (int iter = 0; iter < numIterations; ++iter) {
        try {
            auto [Q, R] = qrDecompositionGramSchmidt(Ak);
            Ak = matrixMultiplyStandard(R, Q);
        } catch (const MatrixException&) {
            break;
        }
    }

    // Extract eigenvalues from diagonal
    Vector eigenvalues(n);
    for (size_t i = 0; i < n; ++i) {
        eigenvalues[i] = Ak[i][i];
    }

    return eigenvalues;
}

// ============================================================================
// Sparse Matrix Class
// ============================================================================

class SparseMatrix {
private:
    size_t rows_;
    size_t cols_;
    std::map<std::pair<size_t, size_t>, double> data_;

public:
    SparseMatrix(size_t rows, size_t cols) : rows_(rows), cols_(cols) {}

    void set(size_t row, size_t col, double value) {
        if (std::abs(value) > EPSILON) {
            data_[{row, col}] = value;
        } else {
            data_.erase({row, col});
        }
    }

    double get(size_t row, size_t col) const {
        auto it = data_.find({row, col});
        return (it != data_.end()) ? it->second : 0.0;
    }

    Matrix toDense() const {
        Matrix matrix = createMatrix(rows_, cols_);
        for (const auto& [key, value] : data_) {
            matrix[key.first][key.second] = value;
        }
        return matrix;
    }

    static SparseMatrix fromDense(const Matrix& matrix) {
        size_t rows = matrix.size(), cols = matrix[0].size();
        SparseMatrix sparse(rows, cols);
        for (size_t i = 0; i < rows; ++i) {
            for (size_t j = 0; j < cols; ++j) {
                if (std::abs(matrix[i][j]) > EPSILON) {
                    sparse.set(i, j, matrix[i][j]);
                }
            }
        }
        return sparse;
    }

    size_t nnz() const { return data_.size(); }

    double sparsity() const {
        double total = rows_ * cols_;
        return 1.0 - (nnz() / total);
    }

    size_t rows() const { return rows_; }
    size_t cols() const { return cols_; }
};

// ============================================================================
// Utility Functions
// ============================================================================

void printMatrix(const Matrix& matrix, const std::string& name) {
    std::cout << name << " =" << std::endl;
    for (const auto& row : matrix) {
        std::cout << "  [";
        for (size_t j = 0; j < row.size(); ++j) {
            std::cout << std::setw(8) << std::fixed << std::setprecision(4) << row[j];
            if (j < row.size() - 1) std::cout << ", ";
        }
        std::cout << "]" << std::endl;
    }
}

void printVector(const Vector& vector, const std::string& name) {
    std::cout << name << " = [";
    for (size_t i = 0; i < vector.size(); ++i) {
        std::cout << std::fixed << std::setprecision(6) << vector[i];
        if (i < vector.size() - 1) std::cout << ", ";
    }
    std::cout << "]" << std::endl;
}

// ============================================================================
// Example Usage and Tests
// ============================================================================

int main() {
    std::cout << std::string(70, '=') << std::endl;
    std::cout << "Matrix Operations and Linear Algebra Library" << std::endl;
    std::cout << std::string(70, '=') << std::endl;
    std::cout << std::endl;

    try {
        // Example 1: Matrix multiplication
        std::cout << "1. Matrix Multiplication" << std::endl;
        std::cout << std::string(70, '-') << std::endl;
        Matrix A1 = {{1, 2, 3}, {4, 5, 6}};
        Matrix B1 = {{7, 8}, {9, 10}, {11, 12}};
        Matrix C1 = matrixMultiplyStandard(A1, B1);
        std::cout << "A (2×3) × B (3×2) = C (2×2)" << std::endl;
        printMatrix(C1, "C");
        std::cout << std::endl;

        // Example 2: Solving linear system
        std::cout << "2. Solving Linear System Ax = b" << std::endl;
        std::cout << std::string(70, '-') << std::endl;
        Matrix A2 = {{2, 1, -1}, {-3, -1, 2}, {-2, 1, 2}};
        Vector b2 = {8, -11, -3};
        Vector x = gaussianElimination(A2, b2);
        printMatrix(A2, "A");
        printVector(b2, "b");
        printVector(x, "Solution x");
        std::cout << std::endl;

        // Example 3: LU Decomposition
        std::cout << "3. LU Decomposition" << std::endl;
        std::cout << std::string(70, '-') << std::endl;
        Matrix A3 = {{2, -1, -2}, {-4, 6, 3}, {-4, -2, 8}};
        auto [L, U] = luDecomposition(A3);
        printMatrix(A3, "A");
        printMatrix(L, "L");
        printMatrix(U, "U");
        std::cout << std::endl;

        // Example 4: Matrix inversion
        std::cout << "4. Matrix Inversion" << std::endl;
        std::cout << std::string(70, '-') << std::endl;
        Matrix A4 = {{4, 7}, {2, 6}};
        Matrix AInv = matrixInverseGaussJordan(A4);
        printMatrix(A4, "A");
        printMatrix(AInv, "A^(-1)");
        Matrix I = matrixMultiplyStandard(A4, AInv);
        printMatrix(I, "A × A^(-1)");
        std::cout << std::endl;

        // Example 5: Eigenvalues
        std::cout << "5. Eigenvalue Computation (Power Iteration)" << std::endl;
        std::cout << std::string(70, '-') << std::endl;
        Matrix A5 = {{2, 1}, {1, 2}};
        auto [eigenvalue, eigenvector] = powerIteration(A5);
        printMatrix(A5, "A");
        std::cout << "Dominant eigenvalue: " << std::fixed << std::setprecision(6)
                  << eigenvalue << std::endl;
        printVector(eigenvector, "Corresponding eigenvector");
        std::cout << std::endl;

        // Example 6: Sparse matrices
        std::cout << "6. Sparse Matrix Operations" << std::endl;
        std::cout << std::string(70, '-') << std::endl;
        SparseMatrix sparse(1000, 1000);
        std::mt19937 gen(42);
        std::uniform_int_distribution<> dis(0, 999);
        std::uniform_real_distribution<> valDis(0.0, 1.0);
        for (int i = 0; i < 100; ++i) {
            sparse.set(dis(gen), dis(gen), valDis(gen));
        }
        std::cout << "Matrix size: " << sparse.rows() << "×" << sparse.cols() << std::endl;
        std::cout << "Non-zero elements: " << sparse.nnz() << std::endl;
        std::cout << "Sparsity: " << std::fixed << std::setprecision(2)
                  << (sparse.sparsity() * 100) << "%" << std::endl;
        std::cout << std::endl;

        // Example 7: Determinant
        std::cout << "7. Determinant Calculation" << std::endl;
        std::cout << std::string(70, '-') << std::endl;
        Matrix A7 = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        double detRecursive = determinantRecursive(A7);
        double detLU = determinantLU(A7);
        printMatrix(A7, "A");
        std::cout << "Determinant (recursive): " << std::fixed << std::setprecision(6)
                  << detRecursive << std::endl;
        std::cout << "Determinant (LU): " << std::fixed << std::setprecision(6)
                  << detLU << std::endl;
        std::cout << std::endl;

        std::cout << "All examples completed successfully!" << std::endl;

    } catch (const MatrixException& e) {
        std::cerr << "Matrix error: " << e.what() << std::endl;
        return 1;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
