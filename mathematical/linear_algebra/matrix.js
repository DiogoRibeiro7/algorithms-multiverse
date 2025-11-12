/**
 * ============================================================================
 * Matrix Operations and Linear Algebra in JavaScript
 *
 * Comprehensive collection of matrix operations and linear algebra algorithms
 * with educational focus on algorithm clarity and numerical stability.
 *
 * Features:
 * - Pure JavaScript with no dependencies
 * - Educational implementations showing algorithm steps
 * - Numerical stability considerations
 * - Memory-efficient sparse matrix representation
 * - Performance benchmarking
 * - Applications in machine learning and graphics
 *
 * Run: node matrix.js
 *
 * @author Algorithms Multiverse
 * @version 1.0
 * ============================================================================
 */

const EPSILON = 1e-10;

// ============================================================================
// Custom Error Class
// ============================================================================

class MatrixError extends Error {
    constructor(message) {
        super(message);
        this.name = 'MatrixError';
    }
}

// ============================================================================
// Basic Matrix Operations
// ============================================================================

/**
 * Create a matrix with given dimensions
 * Time Complexity: O(rows * cols)
 */
function createMatrix(rows, cols, fillValue = 0.0) {
    return Array.from({ length: rows }, () =>
        Array.from({ length: cols }, () => fillValue)
    );
}

/**
 * Create an n×n identity matrix
 * Time Complexity: O(n²)
 */
function identityMatrix(n) {
    const matrix = createMatrix(n, n);
    for (let i = 0; i < n; i++) {
        matrix[i][i] = 1.0;
    }
    return matrix;
}

/**
 * Add two matrices
 * Time Complexity: O(rows * cols)
 */
function matrixAdd(A, B) {
    const rows = A.length, cols = A[0].length;
    if (rows !== B.length || cols !== B[0].length) {
        throw new MatrixError('Matrices must have same dimensions for addition');
    }

    const result = createMatrix(rows, cols);
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            result[i][j] = A[i][j] + B[i][j];
        }
    }
    return result;
}

/**
 * Subtract matrix B from matrix A
 */
function matrixSubtract(A, B) {
    const rows = A.length, cols = A[0].length;
    if (rows !== B.length || cols !== B[0].length) {
        throw new MatrixError('Matrices must have same dimensions for subtraction');
    }

    const result = createMatrix(rows, cols);
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            result[i][j] = A[i][j] - B[i][j];
        }
    }
    return result;
}

/**
 * Multiply matrix by scalar
 */
function scalarMultiply(A, scalar) {
    const rows = A.length, cols = A[0].length;
    const result = createMatrix(rows, cols);
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            result[i][j] = A[i][j] * scalar;
        }
    }
    return result;
}

/**
 * Transpose a matrix
 * Time Complexity: O(rows * cols)
 */
function transpose(A) {
    const rows = A.length, cols = A[0].length;
    const result = createMatrix(cols, rows);
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
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
 * Algorithm:
 * C[i][j] = Σ(A[i][k] * B[k][j]) for k from 0 to n-1
 *
 * Applications:
 * - Linear transformations
 * - Graph algorithms
 * - Computer graphics
 * - Neural network forward propagation
 */
function matrixMultiplyStandard(A, B) {
    const rowsA = A.length, colsA = A[0].length;
    const rowsB = B.length, colsB = B[0].length;

    if (colsA !== rowsB) {
        throw new MatrixError(`Cannot multiply ${rowsA}×${colsA} and ${rowsB}×${colsB} matrices`);
    }

    const result = createMatrix(rowsA, colsB);

    for (let i = 0; i < rowsA; i++) {
        for (let j = 0; j < colsB; j++) {
            let sum = 0.0;
            for (let k = 0; k < colsA; k++) {
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
 * Space Complexity: O(n² log n) due to recursion
 *
 * Algorithm:
 * Divides matrices into quadrants and uses 7 multiplications instead of 8
 *
 * Best for: Large square matrices (n >= 64)
 */
function strassenMultiply(A, B) {
    const n = A.length;

    // Base case: use standard multiplication for small matrices
    if (n <= 64) {
        return matrixMultiplyStandard(A, B);
    }

    // Ensure matrix size is power of 2
    if ((n & (n - 1)) !== 0) {
        return matrixMultiplyStandard(A, B);
    }

    const mid = Math.floor(n / 2);

    // Divide matrices into quadrants
    const A11 = A.slice(0, mid).map(row => row.slice(0, mid));
    const A12 = A.slice(0, mid).map(row => row.slice(mid));
    const A21 = A.slice(mid).map(row => row.slice(0, mid));
    const A22 = A.slice(mid).map(row => row.slice(mid));

    const B11 = B.slice(0, mid).map(row => row.slice(0, mid));
    const B12 = B.slice(0, mid).map(row => row.slice(mid));
    const B21 = B.slice(mid).map(row => row.slice(0, mid));
    const B22 = B.slice(mid).map(row => row.slice(mid));

    // Compute the 7 Strassen products
    const M1 = strassenMultiply(matrixAdd(A11, A22), matrixAdd(B11, B22));
    const M2 = strassenMultiply(matrixAdd(A21, A22), B11);
    const M3 = strassenMultiply(A11, matrixSubtract(B12, B22));
    const M4 = strassenMultiply(A22, matrixSubtract(B21, B11));
    const M5 = strassenMultiply(matrixAdd(A11, A12), B22);
    const M6 = strassenMultiply(matrixSubtract(A21, A11), matrixAdd(B11, B12));
    const M7 = strassenMultiply(matrixSubtract(A12, A22), matrixAdd(B21, B22));

    // Compute result quadrants
    const C11 = matrixAdd(matrixSubtract(matrixAdd(M1, M4), M5), M7);
    const C12 = matrixAdd(M3, M5);
    const C21 = matrixAdd(M2, M4);
    const C22 = matrixAdd(matrixSubtract(matrixAdd(M1, M3), M2), M6);

    // Combine quadrants
    const result = createMatrix(n, n);
    for (let i = 0; i < mid; i++) {
        for (let j = 0; j < mid; j++) {
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
 * Algorithm:
 * 1. Forward elimination: Transform to upper triangular form
 * 2. Backward substitution: Solve for x
 *
 * Applications:
 * - Solving systems of linear equations
 * - Circuit analysis
 * - Structural engineering
 * - Economics models
 */
function gaussianElimination(A, b) {
    const n = A.length;
    if (n !== b.length) {
        throw new MatrixError("Matrix and vector dimensions don't match");
    }

    // Create augmented matrix [A|b]
    const augmented = A.map((row, i) => [...row, b[i]]);

    // Forward elimination with partial pivoting
    for (let col = 0; col < n; col++) {
        // Find pivot (largest absolute value in column)
        let maxRow = col;
        for (let row = col + 1; row < n; row++) {
            if (Math.abs(augmented[row][col]) > Math.abs(augmented[maxRow][col])) {
                maxRow = row;
            }
        }

        // Swap rows
        [augmented[col], augmented[maxRow]] = [augmented[maxRow], augmented[col]];

        // Check for singular matrix
        if (Math.abs(augmented[col][col]) < EPSILON) {
            throw new MatrixError('Matrix is singular or nearly singular');
        }

        // Eliminate column entries below pivot
        for (let row = col + 1; row < n; row++) {
            const factor = augmented[row][col] / augmented[col][col];
            for (let j = col; j <= n; j++) {
                augmented[row][j] -= factor * augmented[col][j];
            }
        }
    }

    // Backward substitution
    const x = new Array(n).fill(0);
    for (let i = n - 1; i >= 0; i--) {
        x[i] = augmented[i][n];
        for (let j = i + 1; j < n; j++) {
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
 * LU decomposition: A = LU where L is lower triangular, U is upper triangular
 *
 * Time Complexity: O(n³)
 * Space Complexity: O(n²)
 *
 * Applications:
 * - Solving multiple systems with same A but different b
 * - Computing determinant
 * - Matrix inversion
 */
function luDecomposition(A) {
    const n = A.length;
    const L = createMatrix(n, n);
    const U = createMatrix(n, n);

    for (let i = 0; i < n; i++) {
        // Upper triangular matrix U
        for (let k = i; k < n; k++) {
            let sum = 0;
            for (let j = 0; j < i; j++) {
                sum += L[i][j] * U[j][k];
            }
            U[i][k] = A[i][k] - sum;
        }

        // Lower triangular matrix L
        for (let k = i; k < n; k++) {
            if (i === k) {
                L[i][i] = 1.0;
            } else {
                let sum = 0;
                for (let j = 0; j < i; j++) {
                    sum += L[k][j] * U[j][i];
                }
                if (Math.abs(U[i][i]) < EPSILON) {
                    throw new MatrixError('Matrix is singular');
                }
                L[k][i] = (A[k][i] - sum) / U[i][i];
            }
        }
    }

    return { L, U };
}

/**
 * QR decomposition using Gram-Schmidt orthogonalization
 *
 * A = QR where:
 * - Q is orthogonal (Q^T * Q = I)
 * - R is upper triangular
 *
 * Time Complexity: O(mn²) for m×n matrix
 *
 * Applications:
 * - Solving least squares problems
 * - Eigenvalue computation
 */
function qrDecompositionGramSchmidt(A) {
    const m = A.length, n = A[0].length;
    const Q = A.map(row => [...row]);
    const R = createMatrix(n, n);

    // Modified Gram-Schmidt
    for (let j = 0; j < n; j++) {
        // Compute norm of column j
        let norm = 0;
        for (let i = 0; i < m; i++) {
            norm += Q[i][j] ** 2;
        }
        R[j][j] = Math.sqrt(norm);

        if (Math.abs(R[j][j]) < EPSILON) {
            throw new MatrixError('Matrix columns are linearly dependent');
        }

        // Normalize column j
        for (let i = 0; i < m; i++) {
            Q[i][j] /= R[j][j];
        }

        // Orthogonalize remaining columns
        for (let k = j + 1; k < n; k++) {
            R[j][k] = 0;
            for (let i = 0; i < m; i++) {
                R[j][k] += Q[i][j] * Q[i][k];
            }
            for (let i = 0; i < m; i++) {
                Q[i][k] -= R[j][k] * Q[i][j];
            }
        }
    }

    return { Q, R };
}

// ============================================================================
// Determinant Calculation
// ============================================================================

/**
 * Calculate determinant using recursive cofactor expansion
 *
 * Time Complexity: O(n!) - very slow for large matrices
 * Best for: Small matrices (n <= 4)
 */
function determinantRecursive(A) {
    const n = A.length;

    if (n === 1) {
        return A[0][0];
    }

    if (n === 2) {
        return A[0][0] * A[1][1] - A[0][1] * A[1][0];
    }

    let det = 0;
    for (let j = 0; j < n; j++) {
        // Create submatrix (remove row 0, column j)
        const submatrix = [];
        for (let i = 1; i < n; i++) {
            const row = [];
            for (let k = 0; k < n; k++) {
                if (k !== j) {
                    row.push(A[i][k]);
                }
            }
            submatrix.push(row);
        }

        const cofactor = ((-1) ** j) * A[0][j] * determinantRecursive(submatrix);
        det += cofactor;
    }

    return det;
}

/**
 * Calculate determinant using LU decomposition
 *
 * Time Complexity: O(n³)
 * Best for: Matrices larger than 4×4
 */
function determinantLU(A) {
    try {
        const { L, U } = luDecomposition(A);
        // Determinant is product of diagonal elements of U
        let det = 1.0;
        for (let i = 0; i < U.length; i++) {
            det *= U[i][i];
        }
        return det;
    } catch (error) {
        return 0.0; // Singular matrix
    }
}

// ============================================================================
// Matrix Inversion
// ============================================================================

/**
 * Matrix inversion using Gauss-Jordan elimination
 *
 * Time Complexity: O(n³)
 * Space Complexity: O(n²)
 *
 * Applications:
 * - Solving linear systems
 * - Computer graphics transformations
 * - Statistics
 */
function matrixInverseGaussJordan(A) {
    const n = A.length;

    // Create augmented matrix [A|I]
    const augmented = A.map((row, i) => [...row, ...identityMatrix(n)[i]]);

    // Forward elimination
    for (let col = 0; col < n; col++) {
        // Find pivot
        let maxRow = col;
        for (let row = col + 1; row < n; row++) {
            if (Math.abs(augmented[row][col]) > Math.abs(augmented[maxRow][col])) {
                maxRow = row;
            }
        }

        [augmented[col], augmented[maxRow]] = [augmented[maxRow], augmented[col]];

        if (Math.abs(augmented[col][col]) < EPSILON) {
            throw new MatrixError('Matrix is singular and cannot be inverted');
        }

        // Scale pivot row
        const pivot = augmented[col][col];
        for (let j = 0; j < 2 * n; j++) {
            augmented[col][j] /= pivot;
        }

        // Eliminate column
        for (let row = 0; row < n; row++) {
            if (row !== col) {
                const factor = augmented[row][col];
                for (let j = 0; j < 2 * n; j++) {
                    augmented[row][j] -= factor * augmented[col][j];
                }
            }
        }
    }

    // Extract inverse from right half
    const inverse = augmented.map(row => row.slice(n));
    return inverse;
}

// ============================================================================
// Eigenvalue Computation
// ============================================================================

/**
 * Find dominant eigenvalue and eigenvector using power iteration
 *
 * Time Complexity: O(n² * iterations)
 *
 * Applications:
 * - Google PageRank algorithm
 * - Principal Component Analysis
 * - Markov chains
 */
function powerIteration(A, numIterations = 100) {
    const n = A.length;

    // Start with random vector
    let v = Array.from({ length: n }, () => Math.random());

    // Normalize
    let norm = Math.sqrt(v.reduce((sum, x) => sum + x * x, 0));
    v = v.map(x => x / norm);

    for (let iteration = 0; iteration < numIterations; iteration++) {
        // Multiply by matrix
        const vNew = new Array(n);
        for (let i = 0; i < n; i++) {
            vNew[i] = 0;
            for (let j = 0; j < n; j++) {
                vNew[i] += A[i][j] * v[j];
            }
        }

        // Normalize
        norm = Math.sqrt(vNew.reduce((sum, x) => sum + x * x, 0));
        const vNormalized = vNew.map(x => x / norm);

        // Check convergence
        if (iteration > 0) {
            const diff = v.reduce((sum, val, i) => sum + Math.abs(vNormalized[i] - val), 0);
            if (diff < EPSILON) {
                break;
            }
        }

        v = vNormalized;
    }

    // Compute eigenvalue
    const Av = new Array(n);
    for (let i = 0; i < n; i++) {
        Av[i] = 0;
        for (let j = 0; j < n; j++) {
            Av[i] += A[i][j] * v[j];
        }
    }
    const eigenvalue = v.reduce((sum, val, i) => sum + val * Av[i], 0);

    return { eigenvalue, eigenvector: v };
}

/**
 * QR algorithm for finding all eigenvalues
 *
 * Time Complexity: O(n³ * iterations)
 */
function qrAlgorithm(A, numIterations = 100) {
    const n = A.length;
    let Ak = A.map(row => [...row]);

    for (let iter = 0; iter < numIterations; iter++) {
        try {
            const { Q, R } = qrDecompositionGramSchmidt(Ak);
            Ak = matrixMultiplyStandard(R, Q);
        } catch (error) {
            break;
        }
    }

    // Extract eigenvalues from diagonal
    const eigenvalues = Ak.map((row, i) => row[i]);
    return eigenvalues;
}

// ============================================================================
// Sparse Matrix Operations
// ============================================================================

class SparseMatrix {
    /**
     * Sparse matrix representation using Map (Dictionary of Keys)
     *
     * Memory efficient for matrices with mostly zeros
     * Storage: O(nnz) where nnz = number of non-zero elements
     */
    constructor(rows, cols) {
        this.rows = rows;
        this.cols = cols;
        this.data = new Map();
    }

    set(row, col, value) {
        if (Math.abs(value) > EPSILON) {
            this.data.set(`${row},${col}`, value);
        } else {
            this.data.delete(`${row},${col}`);
        }
    }

    get(row, col) {
        return this.data.get(`${row},${col}`) || 0.0;
    }

    toDense() {
        const matrix = createMatrix(this.rows, this.cols);
        for (const [key, value] of this.data.entries()) {
            const [i, j] = key.split(',').map(Number);
            matrix[i][j] = value;
        }
        return matrix;
    }

    static fromDense(matrix) {
        const rows = matrix.length, cols = matrix[0].length;
        const sparse = new SparseMatrix(rows, cols);
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                if (Math.abs(matrix[i][j]) > EPSILON) {
                    sparse.set(i, j, matrix[i][j]);
                }
            }
        }
        return sparse;
    }

    multiply(other) {
        if (this.cols !== other.rows) {
            throw new MatrixError('Matrix dimensions incompatible for multiplication');
        }

        const result = new SparseMatrix(this.rows, other.cols);

        // Group data by row and column for efficient access
        const AByRow = new Map();
        const BByCol = new Map();

        for (const [key, value] of this.data.entries()) {
            const [i, j] = key.split(',').map(Number);
            if (!AByRow.has(i)) AByRow.set(i, new Map());
            AByRow.get(i).set(j, value);
        }

        for (const [key, value] of other.data.entries()) {
            const [i, j] = key.split(',').map(Number);
            if (!BByCol.has(j)) BByCol.set(j, new Map());
            BByCol.get(j).set(i, value);
        }

        // Multiply
        for (const [i, rowA] of AByRow.entries()) {
            for (const [j, colB] of BByCol.entries()) {
                let sum = 0;
                for (const [k, aVal] of rowA.entries()) {
                    if (colB.has(k)) {
                        sum += aVal * colB.get(k);
                    }
                }
                if (Math.abs(sum) > EPSILON) {
                    result.set(i, j, sum);
                }
            }
        }

        return result;
    }

    nnz() {
        return this.data.size;
    }

    sparsity() {
        const total = this.rows * this.cols;
        return 1.0 - (this.nnz() / total);
    }
}

// ============================================================================
// Example Usage and Tests
// ============================================================================

function main() {
    console.log('='.repeat(70));
    console.log('Matrix Operations and Linear Algebra Library');
    console.log('='.repeat(70));
    console.log();

    // Example 1: Matrix multiplication
    console.log('1. Matrix Multiplication');
    console.log('-'.repeat(70));
    const A = [[1, 2, 3], [4, 5, 6]];
    const B = [[7, 8], [9, 10], [11, 12]];
    const C = matrixMultiplyStandard(A, B);
    console.log('A (2×3) × B (3×2) = C (2×2)');
    console.log('C =', C);
    console.log();

    // Example 2: Solving linear system
    console.log('2. Solving Linear System Ax = b');
    console.log('-'.repeat(70));
    const A2 = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]];
    const b2 = [8, -11, -3];
    const x = gaussianElimination(A2, b2);
    console.log('A =', A2);
    console.log('b =', b2);
    console.log('Solution x =', x);
    console.log();

    // Example 3: LU Decomposition
    console.log('3. LU Decomposition');
    console.log('-'.repeat(70));
    const A3 = [[2, -1, -2], [-4, 6, 3], [-4, -2, 8]];
    const { L, U } = luDecomposition(A3);
    console.log('A =', A3);
    console.log('L =', L);
    console.log('U =', U);
    console.log();

    // Example 4: Matrix inversion
    console.log('4. Matrix Inversion');
    console.log('-'.repeat(70));
    const A4 = [[4, 7], [2, 6]];
    const AInv = matrixInverseGaussJordan(A4);
    console.log('A =', A4);
    console.log('A^(-1) =', AInv);
    const I = matrixMultiplyStandard(A4, AInv);
    console.log('A × A^(-1) =', I.map(row => row.map(v => Math.round(v * 1e10) / 1e10)));
    console.log();

    // Example 5: Eigenvalues
    console.log('5. Eigenvalue Computation (Power Iteration)');
    console.log('-'.repeat(70));
    const A5 = [[2, 1], [1, 2]];
    const { eigenvalue, eigenvector } = powerIteration(A5);
    console.log('A =', A5);
    console.log('Dominant eigenvalue:', eigenvalue.toFixed(6));
    console.log('Corresponding eigenvector:', eigenvector.map(v => v.toFixed(6)));
    console.log();

    // Example 6: Sparse matrices
    console.log('6. Sparse Matrix Operations');
    console.log('-'.repeat(70));
    const sparse = new SparseMatrix(1000, 1000);
    for (let i = 0; i < 100; i++) {
        sparse.set(
            Math.floor(Math.random() * 1000),
            Math.floor(Math.random() * 1000),
            Math.random()
        );
    }
    console.log(`Matrix size: ${sparse.rows}×${sparse.cols}`);
    console.log(`Non-zero elements: ${sparse.nnz()}`);
    console.log(`Sparsity: ${(sparse.sparsity() * 100).toFixed(2)}%`);
    console.log();

    // Example 7: Determinant
    console.log('7. Determinant Calculation');
    console.log('-'.repeat(70));
    const A7 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
    const detRecursive = determinantRecursive(A7);
    const detLU = determinantLU(A7);
    console.log('A =', A7);
    console.log('Determinant (recursive):', detRecursive.toFixed(6));
    console.log('Determinant (LU):', detLU.toFixed(6));
    console.log();
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        createMatrix,
        identityMatrix,
        matrixAdd,
        matrixSubtract,
        scalarMultiply,
        transpose,
        matrixMultiplyStandard,
        strassenMultiply,
        gaussianElimination,
        luDecomposition,
        qrDecompositionGramSchmidt,
        determinantRecursive,
        determinantLU,
        matrixInverseGaussJordan,
        powerIteration,
        qrAlgorithm,
        SparseMatrix,
        MatrixError
    };
}

// Run if executed directly
if (typeof require !== 'undefined' && require.main === module) {
    main();
}
