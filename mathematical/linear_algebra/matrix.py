"""
Matrix Operations and Linear Algebra Algorithms

Comprehensive collection of matrix operations and linear algebra algorithms
with educational focus on algorithm clarity and numerical stability.

Algorithms included:
- Matrix multiplication (standard and Strassen's algorithm)
- Matrix decomposition (LU, QR, SVD basics)
- Gaussian elimination with partial pivoting
- Determinant calculation (multiple methods)
- Matrix inversion (Gauss-Jordan and LU decomposition)
- Eigenvalue computation (power iteration, QR algorithm)
- Sparse matrix operations
- Parallel matrix multiplication

Features:
- Educational implementations showing algorithm steps
- Numerical stability considerations
- Memory-efficient sparse matrix representation
- Performance benchmarking
- Applications in machine learning and graphics

@author Algorithms Multiverse
@version 1.0
"""

import math
import random
from typing import List, Tuple, Optional, Union, Callable
from dataclasses import dataclass
import copy
from collections import defaultdict
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing

# Type aliases
Matrix = List[List[float]]
Vector = List[float]

EPSILON = 1e-10


class MatrixError(Exception):
    """Custom exception for matrix operations"""
    pass


# ============================================================================
# Basic Matrix Operations
# ============================================================================

def create_matrix(rows: int, cols: int, fill_value: float = 0.0) -> Matrix:
    """
    Create a matrix with given dimensions

    Time Complexity: O(rows * cols)
    Space Complexity: O(rows * cols)
    """
    return [[fill_value for _ in range(cols)] for _ in range(rows)]


def identity_matrix(n: int) -> Matrix:
    """
    Create an n×n identity matrix

    Time Complexity: O(n²)
    """
    matrix = create_matrix(n, n)
    for i in range(n):
        matrix[i][i] = 1.0
    return matrix


def matrix_add(A: Matrix, B: Matrix) -> Matrix:
    """
    Add two matrices

    Time Complexity: O(rows * cols)

    Applications:
    - Computer graphics transformations
    - Neural network weight updates
    - Image processing
    """
    rows, cols = len(A), len(A[0])
    if rows != len(B) or cols != len(B[0]):
        raise MatrixError("Matrices must have same dimensions for addition")

    result = create_matrix(rows, cols)
    for i in range(rows):
        for j in range(cols):
            result[i][j] = A[i][j] + B[i][j]
    return result


def matrix_subtract(A: Matrix, B: Matrix) -> Matrix:
    """Subtract matrix B from matrix A"""
    rows, cols = len(A), len(A[0])
    if rows != len(B) or cols != len(B[0]):
        raise MatrixError("Matrices must have same dimensions for subtraction")

    result = create_matrix(rows, cols)
    for i in range(rows):
        for j in range(cols):
            result[i][j] = A[i][j] - B[i][j]
    return result


def scalar_multiply(A: Matrix, scalar: float) -> Matrix:
    """Multiply matrix by scalar"""
    rows, cols = len(A), len(A[0])
    result = create_matrix(rows, cols)
    for i in range(rows):
        for j in range(cols):
            result[i][j] = A[i][j] * scalar
    return result


def transpose(A: Matrix) -> Matrix:
    """
    Transpose a matrix

    Time Complexity: O(rows * cols)

    Applications:
    - Solving linear systems
    - Covariance matrix computation
    - Neural network backpropagation
    """
    rows, cols = len(A), len(A[0])
    result = create_matrix(cols, rows)
    for i in range(rows):
        for j in range(cols):
            result[j][i] = A[i][j]
    return result


# ============================================================================
# Matrix Multiplication
# ============================================================================

def matrix_multiply_standard(A: Matrix, B: Matrix) -> Matrix:
    """
    Standard matrix multiplication (naive algorithm)

    Time Complexity: O(n³) for n×n matrices
    Space Complexity: O(n²)

    Algorithm:
    C[i][j] = Σ(A[i][k] * B[k][j]) for k from 0 to n-1

    Applications:
    - Linear transformations
    - Graph algorithms (adjacency matrices)
    - Computer graphics transformations
    - Neural network forward propagation

    Example:
    >>> A = [[1, 2], [3, 4]]
    >>> B = [[5, 6], [7, 8]]
    >>> matrix_multiply_standard(A, B)
    [[19, 22], [43, 50]]
    """
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    if cols_A != rows_B:
        raise MatrixError(f"Cannot multiply {rows_A}×{cols_A} and {rows_B}×{cols_B} matrices")

    result = create_matrix(rows_A, cols_B)

    for i in range(rows_A):
        for j in range(cols_B):
            sum_val = 0.0
            for k in range(cols_A):
                sum_val += A[i][k] * B[k][j]
            result[i][j] = sum_val

    return result


def matrix_multiply_parallel(A: Matrix, B: Matrix, num_workers: int = None) -> Matrix:
    """
    Parallel matrix multiplication using multiprocessing

    Time Complexity: O(n³/p) where p is number of processors

    Best for: Large matrices (> 100×100)
    """
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    if cols_A != rows_B:
        raise MatrixError(f"Cannot multiply {rows_A}×{cols_A} and {rows_B}×{cols_B} matrices")

    if num_workers is None:
        num_workers = multiprocessing.cpu_count()

    def compute_row(i: int) -> Tuple[int, List[float]]:
        row = [0.0] * cols_B
        for j in range(cols_B):
            for k in range(cols_A):
                row[j] += A[i][k] * B[k][j]
        return i, row

    result = create_matrix(rows_A, cols_B)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(compute_row, i) for i in range(rows_A)]
        for future in futures:
            i, row = future.result()
            result[i] = row

    return result


def strassen_multiply(A: Matrix, B: Matrix) -> Matrix:
    """
    Strassen's algorithm for matrix multiplication

    Time Complexity: O(n^2.807) vs O(n³) for standard multiplication
    Space Complexity: O(n² log n) due to recursion

    Algorithm:
    Divides matrices into quadrants and uses 7 multiplications instead of 8

    M1 = (A11 + A22)(B11 + B22)
    M2 = (A21 + A22)B11
    M3 = A11(B12 - B22)
    M4 = A22(B21 - B11)
    M5 = (A11 + A12)B22
    M6 = (A21 - A11)(B11 + B12)
    M7 = (A12 - A22)(B21 + B22)

    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    Best for: Large square matrices (n >= 64)
    Worse for: Small matrices due to overhead

    Applications:
    - Large-scale scientific computing
    - Machine learning with large weight matrices
    - Graphics with many transformations
    """
    n = len(A)

    # Base case: use standard multiplication for small matrices
    if n <= 64:
        return matrix_multiply_standard(A, B)

    # Ensure matrix size is power of 2 (pad if necessary)
    if n & (n - 1) != 0:  # Not a power of 2
        return matrix_multiply_standard(A, B)

    # Divide matrices into quadrants
    mid = n // 2

    A11 = [[A[i][j] for j in range(mid)] for i in range(mid)]
    A12 = [[A[i][j] for j in range(mid, n)] for i in range(mid)]
    A21 = [[A[i][j] for j in range(mid)] for i in range(mid, n)]
    A22 = [[A[i][j] for j in range(mid, n)] for i in range(mid, n)]

    B11 = [[B[i][j] for j in range(mid)] for i in range(mid)]
    B12 = [[B[i][j] for j in range(mid, n)] for i in range(mid)]
    B21 = [[B[i][j] for j in range(mid)] for i in range(mid, n)]
    B22 = [[B[i][j] for j in range(mid, n)] for i in range(mid, n)]

    # Compute the 7 Strassen products
    M1 = strassen_multiply(matrix_add(A11, A22), matrix_add(B11, B22))
    M2 = strassen_multiply(matrix_add(A21, A22), B11)
    M3 = strassen_multiply(A11, matrix_subtract(B12, B22))
    M4 = strassen_multiply(A22, matrix_subtract(B21, B11))
    M5 = strassen_multiply(matrix_add(A11, A12), B22)
    M6 = strassen_multiply(matrix_subtract(A21, A11), matrix_add(B11, B12))
    M7 = strassen_multiply(matrix_subtract(A12, A22), matrix_add(B21, B22))

    # Compute result quadrants
    C11 = matrix_add(matrix_subtract(matrix_add(M1, M4), M5), M7)
    C12 = matrix_add(M3, M5)
    C21 = matrix_add(M2, M4)
    C22 = matrix_add(matrix_subtract(matrix_add(M1, M3), M2), M6)

    # Combine quadrants
    result = create_matrix(n, n)
    for i in range(mid):
        for j in range(mid):
            result[i][j] = C11[i][j]
            result[i][j + mid] = C12[i][j]
            result[i + mid][j] = C21[i][j]
            result[i + mid][j + mid] = C22[i][j]

    return result


# ============================================================================
# Gaussian Elimination
# ============================================================================

def gaussian_elimination(A: Matrix, b: Vector) -> Vector:
    """
    Solve linear system Ax = b using Gaussian elimination with partial pivoting

    Time Complexity: O(n³)
    Space Complexity: O(n²)

    Algorithm:
    1. Forward elimination: Transform to upper triangular form
    2. Backward substitution: Solve for x

    Partial pivoting: Swap rows to avoid division by small numbers
    This improves numerical stability

    Applications:
    - Solving systems of linear equations
    - Circuit analysis (Kirchhoff's laws)
    - Structural engineering (finite element analysis)
    - Economics (input-output models)

    Example:
    >>> A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
    >>> b = [8, -11, -3]
    >>> gaussian_elimination(A, b)
    [2.0, 3.0, -1.0]  # x = 2, y = 3, z = -1
    """
    n = len(A)
    if n != len(b):
        raise MatrixError("Matrix and vector dimensions don't match")

    # Create augmented matrix [A|b]
    augmented = [row[:] + [b[i]] for i, row in enumerate(A)]

    # Forward elimination with partial pivoting
    for col in range(n):
        # Find pivot (largest absolute value in column)
        max_row = col
        for row in range(col + 1, n):
            if abs(augmented[row][col]) > abs(augmented[max_row][col]):
                max_row = row

        # Swap rows
        augmented[col], augmented[max_row] = augmented[max_row], augmented[col]

        # Check for singular matrix
        if abs(augmented[col][col]) < EPSILON:
            raise MatrixError("Matrix is singular or nearly singular")

        # Eliminate column entries below pivot
        for row in range(col + 1, n):
            factor = augmented[row][col] / augmented[col][col]
            for j in range(col, n + 1):
                augmented[row][j] -= factor * augmented[col][j]

    # Backward substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = augmented[i][n]
        for j in range(i + 1, n):
            x[i] -= augmented[i][j] * x[j]
        x[i] /= augmented[i][i]

    return x


# ============================================================================
# Matrix Decomposition
# ============================================================================

def lu_decomposition(A: Matrix) -> Tuple[Matrix, Matrix]:
    """
    LU decomposition: A = LU where L is lower triangular, U is upper triangular

    Time Complexity: O(n³)
    Space Complexity: O(n²)

    Algorithm (Doolittle):
    - L has 1's on diagonal
    - U has calculated values on and above diagonal

    Applications:
    - Solving multiple systems with same A but different b
    - Computing determinant: det(A) = det(L) * det(U) = product of U's diagonal
    - Matrix inversion

    Example:
    >>> A = [[2, -1, -2], [-4, 6, 3], [-4, -2, 8]]
    >>> L, U = lu_decomposition(A)
    >>> # Verify: matrix_multiply_standard(L, U) ≈ A
    """
    n = len(A)
    L = create_matrix(n, n)
    U = create_matrix(n, n)

    for i in range(n):
        # Upper triangular matrix U
        for k in range(i, n):
            sum_val = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = A[i][k] - sum_val

        # Lower triangular matrix L
        for k in range(i, n):
            if i == k:
                L[i][i] = 1.0  # Diagonal as 1
            else:
                sum_val = sum(L[k][j] * U[j][i] for j in range(i))
                if abs(U[i][i]) < EPSILON:
                    raise MatrixError("Matrix is singular")
                L[k][i] = (A[k][i] - sum_val) / U[i][i]

    return L, U


def qr_decomposition_gram_schmidt(A: Matrix) -> Tuple[Matrix, Matrix]:
    """
    QR decomposition using Gram-Schmidt orthogonalization

    A = QR where:
    - Q is orthogonal (Q^T * Q = I)
    - R is upper triangular

    Time Complexity: O(mn²) for m×n matrix
    Space Complexity: O(mn)

    Algorithm (Modified Gram-Schmidt):
    1. Orthogonalize columns of A to get Q
    2. Compute R = Q^T * A

    Applications:
    - Solving least squares problems
    - Eigenvalue computation (QR algorithm)
    - Numerical stability in solving linear systems

    Example:
    >>> A = [[12, -51, 4], [6, 167, -68], [-4, 24, -41]]
    >>> Q, R = qr_decomposition_gram_schmidt(A)
    >>> # Q is orthogonal: Q^T * Q ≈ I
    >>> # A = Q * R
    """
    m, n = len(A), len(A[0])
    Q = create_matrix(m, n)
    R = create_matrix(n, n)

    # Copy A to Q
    for i in range(m):
        for j in range(n):
            Q[i][j] = A[i][j]

    # Modified Gram-Schmidt
    for j in range(n):
        # Compute norm of column j
        R[j][j] = math.sqrt(sum(Q[i][j] ** 2 for i in range(m)))

        if abs(R[j][j]) < EPSILON:
            raise MatrixError("Matrix columns are linearly dependent")

        # Normalize column j
        for i in range(m):
            Q[i][j] /= R[j][j]

        # Orthogonalize remaining columns
        for k in range(j + 1, n):
            R[j][k] = sum(Q[i][j] * Q[i][k] for i in range(m))
            for i in range(m):
                Q[i][k] -= R[j][k] * Q[i][j]

    return Q, R


def svd_power_iteration(A: Matrix, num_iterations: int = 100) -> Tuple[Matrix, Vector, Matrix]:
    """
    Simplified SVD using power iteration (computes dominant singular values)

    A = U * Σ * V^T where:
    - U: left singular vectors (m×m orthogonal)
    - Σ: singular values (m×n diagonal)
    - V^T: right singular vectors transposed (n×n orthogonal)

    Time Complexity: O(mn * k * iterations) for k singular values

    Note: This is a simplified educational implementation.
    For production, use optimized libraries (NumPy, LAPACK)

    Applications:
    - Principal Component Analysis (PCA)
    - Dimensionality reduction
    - Image compression
    - Recommender systems
    - Latent semantic analysis
    """
    m, n = len(A), len(A[0])

    # Compute A^T * A for right singular vectors
    ATA = matrix_multiply_standard(transpose(A), A)

    # Find dominant eigenvector using power iteration
    v = [random.random() for _ in range(n)]

    for _ in range(num_iterations):
        # Multiply by matrix
        v_new = [sum(ATA[i][j] * v[j] for j in range(n)) for i in range(n)]

        # Normalize
        norm = math.sqrt(sum(x ** 2 for x in v_new))
        v = [x / norm for x in v_new]

    # Compute singular value
    Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(m)]
    sigma = math.sqrt(sum(x ** 2 for x in Av))

    # Compute left singular vector
    u = [x / sigma if abs(sigma) > EPSILON else 0 for x in Av]

    # Note: This is simplified - full SVD requires computing all singular values
    # For educational purposes, we return the dominant components
    U = [[u[i] if j == 0 else 0 for j in range(m)] for i in range(m)]
    S = [sigma if i == 0 else 0 for i in range(min(m, n))]
    VT = [[v[j] if i == 0 else 0 for j in range(n)] for i in range(n)]

    return U, S, VT


# ============================================================================
# Determinant Calculation
# ============================================================================

def determinant_recursive(A: Matrix) -> float:
    """
    Calculate determinant using recursive cofactor expansion

    Time Complexity: O(n!) - very slow for large matrices
    Space Complexity: O(n²) for recursion

    Algorithm:
    det(A) = Σ((-1)^(i+j) * A[i][j] * det(submatrix))

    Best for: Small matrices (n <= 4)
    Use LU decomposition for larger matrices
    """
    n = len(A)

    if n == 1:
        return A[0][0]

    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]

    det = 0.0
    for j in range(n):
        # Create submatrix (remove row 0, column j)
        submatrix = [[A[i][k] for k in range(n) if k != j]
                     for i in range(1, n)]

        cofactor = ((-1) ** j) * A[0][j] * determinant_recursive(submatrix)
        det += cofactor

    return det


def determinant_lu(A: Matrix) -> float:
    """
    Calculate determinant using LU decomposition

    Time Complexity: O(n³)

    Algorithm:
    det(A) = det(L) * det(U) = product of diagonal elements of U
    (since L has 1's on diagonal)

    Best for: Matrices larger than 4×4

    Applications:
    - Testing if matrix is singular (det = 0)
    - Computing area/volume transformations
    - Characteristic polynomial in eigenvalue problems
    """
    try:
        L, U = lu_decomposition(A)
        # Determinant is product of diagonal elements of U
        det = 1.0
        for i in range(len(U)):
            det *= U[i][i]
        return det
    except MatrixError:
        return 0.0  # Singular matrix


# ============================================================================
# Matrix Inversion
# ============================================================================

def matrix_inverse_gauss_jordan(A: Matrix) -> Matrix:
    """
    Matrix inversion using Gauss-Jordan elimination

    Time Complexity: O(n³)
    Space Complexity: O(n²)

    Algorithm:
    1. Create augmented matrix [A|I]
    2. Transform to [I|A^(-1)] using row operations

    Applications:
    - Solving linear systems
    - Computer graphics transformations
    - Control systems
    - Statistics (covariance matrix inversion)

    Example:
    >>> A = [[4, 7], [2, 6]]
    >>> A_inv = matrix_inverse_gauss_jordan(A)
    >>> # Verify: matrix_multiply_standard(A, A_inv) ≈ I
    """
    n = len(A)

    # Create augmented matrix [A|I]
    augmented = [A[i][:] + identity_matrix(n)[i] for i in range(n)]

    # Forward elimination
    for col in range(n):
        # Find pivot
        max_row = col
        for row in range(col + 1, n):
            if abs(augmented[row][col]) > abs(augmented[max_row][col]):
                max_row = row

        augmented[col], augmented[max_row] = augmented[max_row], augmented[col]

        if abs(augmented[col][col]) < EPSILON:
            raise MatrixError("Matrix is singular and cannot be inverted")

        # Scale pivot row
        pivot = augmented[col][col]
        for j in range(2 * n):
            augmented[col][j] /= pivot

        # Eliminate column
        for row in range(n):
            if row != col:
                factor = augmented[row][col]
                for j in range(2 * n):
                    augmented[row][j] -= factor * augmented[col][j]

    # Extract inverse from right half
    inverse = [[augmented[i][j + n] for j in range(n)] for i in range(n)]
    return inverse


def matrix_inverse_lu(A: Matrix) -> Matrix:
    """
    Matrix inversion using LU decomposition

    Time Complexity: O(n³)

    Algorithm:
    1. Decompose A = LU
    2. For each column i of I:
       a. Solve Ly = e_i (forward substitution)
       b. Solve Ux = y (backward substitution)
       c. x is column i of A^(-1)

    More efficient when solving multiple systems with same A
    """
    n = len(A)
    L, U = lu_decomposition(A)

    inverse = create_matrix(n, n)

    for col in range(n):
        # Create unit vector e_col
        e = [1.0 if i == col else 0.0 for i in range(n)]

        # Forward substitution: Ly = e
        y = [0.0] * n
        for i in range(n):
            y[i] = e[i] - sum(L[i][j] * y[j] for j in range(i))

        # Backward substitution: Ux = y
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

        # Set column of inverse
        for i in range(n):
            inverse[i][col] = x[i]

    return inverse


# ============================================================================
# Eigenvalue Computation
# ============================================================================

def power_iteration(A: Matrix, num_iterations: int = 100) -> Tuple[float, Vector]:
    """
    Find dominant eigenvalue and eigenvector using power iteration

    Time Complexity: O(n² * iterations)

    Algorithm:
    1. Start with random vector v
    2. Repeatedly multiply by A and normalize
    3. Converges to eigenvector of largest eigenvalue

    Convergence rate depends on ratio of largest to second-largest eigenvalue

    Applications:
    - Google PageRank algorithm
    - Principal Component Analysis (PCA)
    - Markov chains (stationary distribution)
    - Vibration analysis (finding dominant frequency)

    Example:
    >>> A = [[2, 1], [1, 2]]
    >>> eigenvalue, eigenvector = power_iteration(A)
    >>> # Verify: A * v ≈ λ * v
    """
    n = len(A)

    # Start with random vector
    v = [random.random() for _ in range(n)]

    # Normalize
    norm = math.sqrt(sum(x ** 2 for x in v))
    v = [x / norm for x in v]

    for iteration in range(num_iterations):
        # Multiply by matrix
        v_new = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]

        # Normalize
        norm = math.sqrt(sum(x ** 2 for x in v_new))
        v_new = [x / norm for x in v_new]

        # Check convergence
        if iteration > 0:
            diff = sum(abs(v_new[i] - v[i]) for i in range(n))
            if diff < EPSILON:
                break

        v = v_new

    # Compute eigenvalue: λ = (v^T * A * v) / (v^T * v)
    Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
    eigenvalue = sum(v[i] * Av[i] for i in range(n))

    return eigenvalue, v


def qr_algorithm(A: Matrix, num_iterations: int = 100) -> List[float]:
    """
    QR algorithm for finding all eigenvalues

    Time Complexity: O(n³ * iterations)

    Algorithm:
    1. Start with A₀ = A
    2. For k = 0, 1, 2, ...:
       a. QR decomposition: Aₖ = QₖRₖ
       b. Form Aₖ₊₁ = RₖQₖ
    3. Aₖ converges to upper triangular (diagonal elements are eigenvalues)

    Applications:
    - Stability analysis
    - Control theory
    - Quantum mechanics
    - Vibration modes
    """
    n = len(A)
    Ak = [row[:] for row in A]  # Copy A

    for _ in range(num_iterations):
        try:
            Q, R = qr_decomposition_gram_schmidt(Ak)
            Ak = matrix_multiply_standard(R, Q)
        except MatrixError:
            break

    # Extract eigenvalues from diagonal
    eigenvalues = [Ak[i][i] for i in range(n)]
    return eigenvalues


# ============================================================================
# Sparse Matrix Operations
# ============================================================================

@dataclass
class SparseMatrix:
    """
    Sparse matrix representation using Dictionary of Keys (DOK)

    Memory efficient for matrices with mostly zeros

    Storage: O(nnz) where nnz = number of non-zero elements
    vs O(rows * cols) for dense matrix

    Applications:
    - Large graphs (adjacency matrices)
    - Finite element analysis
    - Natural language processing (term-document matrices)
    - Recommendation systems (user-item matrices)
    """
    rows: int
    cols: int
    data: dict = None  # (row, col) -> value

    def __post_init__(self):
        if self.data is None:
            self.data = {}

    def set(self, row: int, col: int, value: float):
        """Set value at (row, col)"""
        if abs(value) > EPSILON:
            self.data[(row, col)] = value
        elif (row, col) in self.data:
            del self.data[(row, col)]

    def get(self, row: int, col: int) -> float:
        """Get value at (row, col)"""
        return self.data.get((row, col), 0.0)

    def to_dense(self) -> Matrix:
        """Convert to dense matrix"""
        matrix = create_matrix(self.rows, self.cols)
        for (i, j), value in self.data.items():
            matrix[i][j] = value
        return matrix

    @staticmethod
    def from_dense(matrix: Matrix) -> 'SparseMatrix':
        """Create sparse matrix from dense matrix"""
        rows, cols = len(matrix), len(matrix[0])
        sparse = SparseMatrix(rows, cols)
        for i in range(rows):
            for j in range(cols):
                if abs(matrix[i][j]) > EPSILON:
                    sparse.set(i, j, matrix[i][j])
        return sparse

    def multiply(self, other: 'SparseMatrix') -> 'SparseMatrix':
        """
        Sparse matrix multiplication

        Time Complexity: O(nnz_A * nnz_B / cols_A) average case
        Much better than O(n³) for sparse matrices
        """
        if self.cols != other.rows:
            raise MatrixError("Matrix dimensions incompatible for multiplication")

        result = SparseMatrix(self.rows, other.cols)

        # Group data by row for efficient access
        A_by_row = defaultdict(dict)
        for (i, j), value in self.data.items():
            A_by_row[i][j] = value

        B_by_col = defaultdict(dict)
        for (i, j), value in other.data.items():
            B_by_col[j][i] = value

        # Multiply
        for i in A_by_row:
            for j in B_by_col:
                value = sum(A_by_row[i].get(k, 0) * B_by_col[j].get(k, 0)
                           for k in set(A_by_row[i].keys()) & set(B_by_col[j].keys()))
                if abs(value) > EPSILON:
                    result.set(i, j, value)

        return result

    def nnz(self) -> int:
        """Number of non-zero elements"""
        return len(self.data)

    def sparsity(self) -> float:
        """Sparsity: percentage of zero elements"""
        total = self.rows * self.cols
        return 1.0 - (self.nnz() / total)


# ============================================================================
# Applications
# ============================================================================

class LinearSystemSolver:
    """
    Utility class for solving various linear system problems
    """

    @staticmethod
    def solve_system(A: Matrix, b: Vector, method: str = 'gaussian') -> Vector:
        """
        Solve Ax = b using specified method

        Methods:
        - 'gaussian': Gaussian elimination (general)
        - 'lu': LU decomposition (multiple right-hand sides)
        - 'inverse': Matrix inversion (not recommended for large systems)
        """
        if method == 'gaussian':
            return gaussian_elimination(A, b)
        elif method == 'lu':
            n = len(A)
            L, U = lu_decomposition(A)

            # Forward substitution: Ly = b
            y = [0.0] * n
            for i in range(n):
                y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))

            # Backward substitution: Ux = y
            x = [0.0] * n
            for i in range(n - 1, -1, -1):
                x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

            return x
        elif method == 'inverse':
            A_inv = matrix_inverse_gauss_jordan(A)
            return [sum(A_inv[i][j] * b[j] for j in range(len(b))) for i in range(len(A))]
        else:
            raise ValueError(f"Unknown method: {method}")


class TransformationMatrix:
    """
    2D/3D transformation matrices for computer graphics
    """

    @staticmethod
    def rotation_2d(angle: float) -> Matrix:
        """2D rotation matrix"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [[cos_a, -sin_a], [sin_a, cos_a]]

    @staticmethod
    def scaling_2d(sx: float, sy: float) -> Matrix:
        """2D scaling matrix"""
        return [[sx, 0], [0, sy]]

    @staticmethod
    def rotation_3d_z(angle: float) -> Matrix:
        """3D rotation around Z-axis"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ]


# ============================================================================
# Performance Benchmarking
# ============================================================================

class MatrixBenchmark:
    """Benchmarking tools for comparing matrix algorithms"""

    @staticmethod
    def generate_random_matrix(rows: int, cols: int,
                               min_val: float = -10, max_val: float = 10) -> Matrix:
        """Generate random matrix"""
        return [[random.uniform(min_val, max_val) for _ in range(cols)]
                for _ in range(rows)]

    @staticmethod
    def generate_sparse_matrix(rows: int, cols: int, density: float = 0.1) -> SparseMatrix:
        """Generate sparse matrix with given density"""
        sparse = SparseMatrix(rows, cols)
        num_elements = int(rows * cols * density)
        for _ in range(num_elements):
            i = random.randint(0, rows - 1)
            j = random.randint(0, cols - 1)
            sparse.set(i, j, random.uniform(-10, 10))
        return sparse

    @staticmethod
    def benchmark_multiplication(sizes: List[int]):
        """Benchmark different multiplication algorithms"""
        print("Matrix Multiplication Benchmark")
        print("=" * 60)

        for n in sizes:
            A = MatrixBenchmark.generate_random_matrix(n, n)
            B = MatrixBenchmark.generate_random_matrix(n, n)

            # Standard multiplication
            start = time.time()
            C_standard = matrix_multiply_standard(A, B)
            time_standard = time.time() - start

            # Strassen (only for powers of 2)
            if n & (n - 1) == 0 and n >= 64:
                start = time.time()
                C_strassen = strassen_multiply(A, B)
                time_strassen = time.time() - start
                print(f"Size {n}×{n}:")
                print(f"  Standard: {time_standard:.4f}s")
                print(f"  Strassen: {time_strassen:.4f}s")
                print(f"  Speedup: {time_standard/time_strassen:.2f}x")
            else:
                print(f"Size {n}×{n}: Standard: {time_standard:.4f}s")
            print()

    @staticmethod
    def benchmark_sparse_vs_dense():
        """Compare sparse vs dense matrix operations"""
        print("Sparse vs Dense Matrix Benchmark")
        print("=" * 60)

        sizes = [100, 200, 500]
        densities = [0.01, 0.05, 0.1]

        for n in sizes:
            for density in densities:
                # Generate sparse matrices
                sparse_A = MatrixBenchmark.generate_sparse_matrix(n, n, density)
                sparse_B = MatrixBenchmark.generate_sparse_matrix(n, n, density)

                # Convert to dense
                dense_A = sparse_A.to_dense()
                dense_B = sparse_B.to_dense()

                # Sparse multiplication
                start = time.time()
                sparse_C = sparse_A.multiply(sparse_B)
                time_sparse = time.time() - start

                # Dense multiplication
                start = time.time()
                dense_C = matrix_multiply_standard(dense_A, dense_B)
                time_dense = time.time() - start

                print(f"Size {n}×{n}, Density {density:.2%}:")
                print(f"  Sparse: {time_sparse:.4f}s (nnz={sparse_C.nnz()})")
                print(f"  Dense:  {time_dense:.4f}s")
                print(f"  Speedup: {time_dense/time_sparse:.2f}x")
                print()


# ============================================================================
# Example Usage and Tests
# ============================================================================

def main():
    """Example usage and demonstrations"""
    print("=" * 70)
    print("Matrix Operations and Linear Algebra Library")
    print("=" * 70)
    print()

    # Example 1: Matrix multiplication
    print("1. Matrix Multiplication")
    print("-" * 70)
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]
    C = matrix_multiply_standard(A, B)
    print(f"A (2×3) × B (3×2) = C (2×2)")
    print(f"C = {C}")
    print()

    # Example 2: Solving linear system
    print("2. Solving Linear System Ax = b")
    print("-" * 70)
    A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
    b = [8, -11, -3]
    x = gaussian_elimination(A, b)
    print(f"A = {A}")
    print(f"b = {b}")
    print(f"Solution x = {x}")
    print()

    # Example 3: LU Decomposition
    print("3. LU Decomposition")
    print("-" * 70)
    A = [[2, -1, -2], [-4, 6, 3], [-4, -2, 8]]
    L, U = lu_decomposition(A)
    print(f"A = {A}")
    print(f"L = {L}")
    print(f"U = {U}")
    print()

    # Example 4: Matrix inversion
    print("4. Matrix Inversion")
    print("-" * 70)
    A = [[4, 7], [2, 6]]
    A_inv = matrix_inverse_gauss_jordan(A)
    print(f"A = {A}")
    print(f"A^(-1) = {A_inv}")
    # Verify
    I = matrix_multiply_standard(A, A_inv)
    print(f"A × A^(-1) = {[[round(I[i][j], 10) for j in range(len(I[0]))] for i in range(len(I))]}")
    print()

    # Example 5: Eigenvalues
    print("5. Eigenvalue Computation (Power Iteration)")
    print("-" * 70)
    A = [[2, 1], [1, 2]]
    eigenvalue, eigenvector = power_iteration(A)
    print(f"A = {A}")
    print(f"Dominant eigenvalue: {eigenvalue:.6f}")
    print(f"Corresponding eigenvector: {[f'{v:.6f}' for v in eigenvector]}")
    print()

    # Example 6: Sparse matrices
    print("6. Sparse Matrix Operations")
    print("-" * 70)
    sparse = SparseMatrix(1000, 1000)
    # Add some values
    for i in range(100):
        sparse.set(random.randint(0, 999), random.randint(0, 999), random.random())
    print(f"Matrix size: {sparse.rows}×{sparse.cols}")
    print(f"Non-zero elements: {sparse.nnz()}")
    print(f"Sparsity: {sparse.sparsity():.2%}")
    print()

    # Example 7: Determinant
    print("7. Determinant Calculation")
    print("-" * 70)
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    det_recursive = determinant_recursive(A)
    det_lu = determinant_lu(A)
    print(f"A = {A}")
    print(f"Determinant (recursive): {det_recursive:.6f}")
    print(f"Determinant (LU): {det_lu:.6f}")
    print()


if __name__ == "__main__":
    main()
