/**
 * Matrix Operations Module
 * Comprehensive implementations of matrix operations and linear algebra
 */

/**
 * Matrix class for basic matrix operations
 */
export class Matrix {
    constructor(data) {
        if (Array.isArray(data)) {
            this.rows = data.length;
            this.cols = data[0] ? data[0].length : 0;
            this.data = data.map(row => [...row]); // Deep copy
        } else if (typeof data === 'object' && 'rows' in data && 'cols' in data) {
            this.rows = data.rows;
            this.cols = data.cols;
            this.data = Array(this.rows).fill().map(() => Array(this.cols).fill(0));
        } else {
            throw new Error("Invalid matrix initialization");
        }

        // Validate rectangular matrix
        for (let i = 0; i < this.rows; i++) {
            if (this.data[i].length !== this.cols) {
                throw new Error("Matrix must be rectangular");
            }
        }
    }

    // Get element at position (i, j)
    get(i, j) {
        if (i < 0 || i >= this.rows || j < 0 || j >= this.cols) {
            throw new Error("Index out of bounds");
        }
        return this.data[i][j];
    }

    // Set element at position (i, j)
    set(i, j, value) {
        if (i < 0 || i >= this.rows || j < 0 || j >= this.cols) {
            throw new Error("Index out of bounds");
        }
        this.data[i][j] = value;
    }

    // Get a row
    getRow(i) {
        if (i < 0 || i >= this.rows) {
            throw new Error("Row index out of bounds");
        }
        return [...this.data[i]];
    }

    // Get a column
    getColumn(j) {
        if (j < 0 || j >= this.cols) {
            throw new Error("Column index out of bounds");
        }
        return this.data.map(row => row[j]);
    }

    // Set a row
    setRow(i, row) {
        if (i < 0 || i >= this.rows) {
            throw new Error("Row index out of bounds");
        }
        if (row.length !== this.cols) {
            throw new Error("Row length mismatch");
        }
        this.data[i] = [...row];
    }

    // Set a column
    setColumn(j, column) {
        if (j < 0 || j >= this.cols) {
            throw new Error("Column index out of bounds");
        }
        if (column.length !== this.rows) {
            throw new Error("Column length mismatch");
        }
        for (let i = 0; i < this.rows; i++) {
            this.data[i][j] = column[i];
        }
    }

    // Create a copy of the matrix
    clone() {
        return new Matrix(this.data);
    }

    // Check if matrix is square
    isSquare() {
        return this.rows === this.cols;
    }

    // Check if matrix is symmetric
    isSymmetric() {
        if (!this.isSquare()) return false;
        for (let i = 0; i < this.rows; i++) {
            for (let j = i + 1; j < this.cols; j++) {
                if (Math.abs(this.data[i][j] - this.data[j][i]) > 1e-10) {
                    return false;
                }
            }
        }
        return true;
    }

    // Check if matrix is diagonal
    isDiagonal() {
        for (let i = 0; i < this.rows; i++) {
            for (let j = 0; j < this.cols; j++) {
                if (i !== j && Math.abs(this.data[i][j]) > 1e-10) {
                    return false;
                }
            }
        }
        return true;
    }

    // Check if matrix is upper triangular
    isUpperTriangular() {
        for (let i = 1; i < this.rows; i++) {
            for (let j = 0; j < Math.min(i, this.cols); j++) {
                if (Math.abs(this.data[i][j]) > 1e-10) {
                    return false;
                }
            }
        }
        return true;
    }

    // Check if matrix is lower triangular
    isLowerTriangular() {
        for (let i = 0; i < this.rows; i++) {
            for (let j = i + 1; j < this.cols; j++) {
                if (Math.abs(this.data[i][j]) > 1e-10) {
                    return false;
                }
            }
        }
        return true;
    }

    // Convert to array
    toArray() {
        return this.data.map(row => [...row]);
    }

    // String representation
    toString() {
        return this.data.map(row => row.map(val => val.toFixed(4)).join('\t')).join('\n');
    }
}

// Create identity matrix
export function identity(n) {
    const matrix = new Matrix({ rows: n, cols: n });
    for (let i = 0; i < n; i++) {
        matrix.set(i, i, 1);
    }
    return matrix;
}

// Create zero matrix
export function zeros(rows, cols = null) {
    if (cols === null) cols = rows;
    return new Matrix({ rows, cols });
}

// Create ones matrix
export function ones(rows, cols = null) {
    if (cols === null) cols = rows;
    const matrix = new Matrix({ rows, cols });
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            matrix.set(i, j, 1);
        }
    }
    return matrix;
}

// Create diagonal matrix from vector
export function diagonal(vector) {
    const n = vector.length;
    const matrix = new Matrix({ rows: n, cols: n });
    for (let i = 0; i < n; i++) {
        matrix.set(i, i, vector[i]);
    }
    return matrix;
}

// Create random matrix
export function random(rows, cols = null, min = 0, max = 1) {
    if (cols === null) cols = rows;
    const matrix = new Matrix({ rows, cols });
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            matrix.set(i, j, Math.random() * (max - min) + min);
        }
    }
    return matrix;
}

// Matrix addition
export function add(a, b) {
    if (a.rows !== b.rows || a.cols !== b.cols) {
        throw new Error("Matrix dimensions must match for addition");
    }
    const result = new Matrix({ rows: a.rows, cols: a.cols });
    for (let i = 0; i < a.rows; i++) {
        for (let j = 0; j < a.cols; j++) {
            result.set(i, j, a.get(i, j) + b.get(i, j));
        }
    }
    return result;
}

// Matrix subtraction
export function subtract(a, b) {
    if (a.rows !== b.rows || a.cols !== b.cols) {
        throw new Error("Matrix dimensions must match for subtraction");
    }
    const result = new Matrix({ rows: a.rows, cols: a.cols });
    for (let i = 0; i < a.rows; i++) {
        for (let j = 0; j < a.cols; j++) {
            result.set(i, j, a.get(i, j) - b.get(i, j));
        }
    }
    return result;
}

// Matrix multiplication
export function multiply(a, b) {
    if (a.cols !== b.rows) {
        throw new Error("Matrix dimensions incompatible for multiplication");
    }
    const result = new Matrix({ rows: a.rows, cols: b.cols });
    for (let i = 0; i < a.rows; i++) {
        for (let j = 0; j < b.cols; j++) {
            let sum = 0;
            for (let k = 0; k < a.cols; k++) {
                sum += a.get(i, k) * b.get(k, j);
            }
            result.set(i, j, sum);
        }
    }
    return result;
}

// Scalar multiplication
export function scalarMultiply(matrix, scalar) {
    const result = new Matrix({ rows: matrix.rows, cols: matrix.cols });
    for (let i = 0; i < matrix.rows; i++) {
        for (let j = 0; j < matrix.cols; j++) {
            result.set(i, j, matrix.get(i, j) * scalar);
        }
    }
    return result;
}

// Matrix transpose
export function transpose(matrix) {
    const result = new Matrix({ rows: matrix.cols, cols: matrix.rows });
    for (let i = 0; i < matrix.rows; i++) {
        for (let j = 0; j < matrix.cols; j++) {
            result.set(j, i, matrix.get(i, j));
        }
    }
    return result;
}

// Matrix trace (sum of diagonal elements)
export function trace(matrix) {
    if (!matrix.isSquare()) {
        throw new Error("Trace is only defined for square matrices");
    }
    let sum = 0;
    for (let i = 0; i < matrix.rows; i++) {
        sum += matrix.get(i, i);
    }
    return sum;
}

// Matrix determinant using LU decomposition
export function determinant(matrix) {
    if (!matrix.isSquare()) {
        throw new Error("Determinant is only defined for square matrices");
    }

    const n = matrix.rows;

    // Base cases
    if (n === 1) return matrix.get(0, 0);
    if (n === 2) {
        return matrix.get(0, 0) * matrix.get(1, 1) - matrix.get(0, 1) * matrix.get(1, 0);
    }

    // Use LU decomposition for larger matrices
    const { L, U, P, swaps } = luDecomposition(matrix);

    let det = swaps % 2 === 0 ? 1 : -1;
    for (let i = 0; i < n; i++) {
        det *= U.get(i, i);
    }

    return det;
}

// Matrix inverse using Gauss-Jordan elimination
export function inverse(matrix) {
    if (!matrix.isSquare()) {
        throw new Error("Only square matrices can be inverted");
    }

    const n = matrix.rows;
    const augmented = new Matrix({ rows: n, cols: 2 * n });

    // Create augmented matrix [A | I]
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            augmented.set(i, j, matrix.get(i, j));
            augmented.set(i, j + n, i === j ? 1 : 0);
        }
    }

    // Gauss-Jordan elimination
    for (let i = 0; i < n; i++) {
        // Find pivot
        let maxRow = i;
        for (let k = i + 1; k < n; k++) {
            if (Math.abs(augmented.get(k, i)) > Math.abs(augmented.get(maxRow, i))) {
                maxRow = k;
            }
        }

        // Swap rows
        if (maxRow !== i) {
            for (let j = 0; j < 2 * n; j++) {
                const temp = augmented.get(i, j);
                augmented.set(i, j, augmented.get(maxRow, j));
                augmented.set(maxRow, j, temp);
            }
        }

        // Check for singular matrix
        if (Math.abs(augmented.get(i, i)) < 1e-10) {
            throw new Error("Matrix is singular and cannot be inverted");
        }

        // Scale pivot row
        const pivot = augmented.get(i, i);
        for (let j = 0; j < 2 * n; j++) {
            augmented.set(i, j, augmented.get(i, j) / pivot);
        }

        // Eliminate column
        for (let k = 0; k < n; k++) {
            if (k !== i) {
                const factor = augmented.get(k, i);
                for (let j = 0; j < 2 * n; j++) {
                    augmented.set(k, j, augmented.get(k, j) - factor * augmented.get(i, j));
                }
            }
        }
    }

    // Extract inverse from augmented matrix
    const result = new Matrix({ rows: n, cols: n });
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            result.set(i, j, augmented.get(i, j + n));
        }
    }

    return result;
}

// Matrix rank
export function rank(matrix) {
    const m = matrix.rows;
    const n = matrix.cols;
    const copy = matrix.clone();
    let rank = 0;

    for (let col = 0; col < n && rank < m; col++) {
        // Find pivot
        let pivotRow = rank;
        for (let row = rank + 1; row < m; row++) {
            if (Math.abs(copy.get(row, col)) > Math.abs(copy.get(pivotRow, col))) {
                pivotRow = row;
            }
        }

        if (Math.abs(copy.get(pivotRow, col)) < 1e-10) {
            continue; // Skip this column
        }

        // Swap rows
        if (pivotRow !== rank) {
            for (let j = 0; j < n; j++) {
                const temp = copy.get(rank, j);
                copy.set(rank, j, copy.get(pivotRow, j));
                copy.set(pivotRow, j, temp);
            }
        }

        // Eliminate below
        for (let row = rank + 1; row < m; row++) {
            const factor = copy.get(row, col) / copy.get(rank, col);
            for (let j = col; j < n; j++) {
                copy.set(row, j, copy.get(row, j) - factor * copy.get(rank, j));
            }
        }

        rank++;
    }

    return rank;
}

// Frobenius norm
export function frobeniusNorm(matrix) {
    let sum = 0;
    for (let i = 0; i < matrix.rows; i++) {
        for (let j = 0; j < matrix.cols; j++) {
            sum += matrix.get(i, j) ** 2;
        }
    }
    return Math.sqrt(sum);
}

// Matrix power (for square matrices)
export function power(matrix, n) {
    if (!matrix.isSquare()) {
        throw new Error("Matrix power is only defined for square matrices");
    }

    if (n === 0) return identity(matrix.rows);
    if (n === 1) return matrix.clone();

    if (n < 0) {
        const inv = inverse(matrix);
        return power(inv, -n);
    }

    // Binary exponentiation
    let result = identity(matrix.rows);
    let base = matrix.clone();

    while (n > 0) {
        if (n % 2 === 1) {
            result = multiply(result, base);
        }
        base = multiply(base, base);
        n = Math.floor(n / 2);
    }

    return result;
}

// Dot product of two vectors
export function dotProduct(a, b) {
    if (a.length !== b.length) {
        throw new Error("Vectors must have the same length");
    }
    let sum = 0;
    for (let i = 0; i < a.length; i++) {
        sum += a[i] * b[i];
    }
    return sum;
}

// Cross product of two 3D vectors
export function crossProduct(a, b) {
    if (a.length !== 3 || b.length !== 3) {
        throw new Error("Cross product is only defined for 3D vectors");
    }
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    ];
}

// Vector norm
export function vectorNorm(vector, p = 2) {
    if (p === Infinity) {
        return Math.max(...vector.map(Math.abs));
    }
    if (p === 1) {
        return vector.reduce((sum, val) => sum + Math.abs(val), 0);
    }
    return Math.pow(
        vector.reduce((sum, val) => sum + Math.pow(Math.abs(val), p), 0),
        1 / p
    );
}

// LU decomposition
export function luDecomposition(matrix) {
    if (!matrix.isSquare()) {
        throw new Error("LU decomposition requires a square matrix");
    }

    const n = matrix.rows;
    const L = identity(n);
    const U = matrix.clone();
    const P = identity(n);
    let swaps = 0;

    for (let i = 0; i < n - 1; i++) {
        // Find pivot
        let maxRow = i;
        for (let k = i + 1; k < n; k++) {
            if (Math.abs(U.get(k, i)) > Math.abs(U.get(maxRow, i))) {
                maxRow = k;
            }
        }

        // Swap rows in U and P if needed
        if (maxRow !== i) {
            swaps++;
            for (let j = 0; j < n; j++) {
                // Swap in U
                const tempU = U.get(i, j);
                U.set(i, j, U.get(maxRow, j));
                U.set(maxRow, j, tempU);

                // Swap in P
                const tempP = P.get(i, j);
                P.set(i, j, P.get(maxRow, j));
                P.set(maxRow, j, tempP);
            }

            // Swap in L (only the already computed part)
            for (let j = 0; j < i; j++) {
                const tempL = L.get(i, j);
                L.set(i, j, L.get(maxRow, j));
                L.set(maxRow, j, tempL);
            }
        }

        // Gaussian elimination
        for (let j = i + 1; j < n; j++) {
            if (Math.abs(U.get(i, i)) < 1e-10) {
                throw new Error("Matrix is singular");
            }

            const factor = U.get(j, i) / U.get(i, i);
            L.set(j, i, factor);

            for (let k = i; k < n; k++) {
                U.set(j, k, U.get(j, k) - factor * U.get(i, k));
            }
        }
    }

    return { L, U, P, swaps };
}

// QR decomposition using Gram-Schmidt
export function qrDecomposition(matrix) {
    const m = matrix.rows;
    const n = matrix.cols;
    const Q = new Matrix({ rows: m, cols: n });
    const R = new Matrix({ rows: n, cols: n });

    // Gram-Schmidt orthogonalization
    for (let j = 0; j < n; j++) {
        // Get column j
        const v = matrix.getColumn(j);

        // Subtract projections of previous columns
        for (let i = 0; i < j; i++) {
            const q_i = Q.getColumn(i);
            const r_ij = dotProduct(q_i, v);
            R.set(i, j, r_ij);

            for (let k = 0; k < m; k++) {
                v[k] -= r_ij * q_i[k];
            }
        }

        // Compute norm
        const r_jj = vectorNorm(v);
        R.set(j, j, r_jj);

        // Normalize and set column in Q
        if (Math.abs(r_jj) > 1e-10) {
            for (let k = 0; k < m; k++) {
                Q.set(k, j, v[k] / r_jj);
            }
        }
    }

    return { Q, R };
}

// Cholesky decomposition (for positive definite matrices)
export function choleskyDecomposition(matrix) {
    if (!matrix.isSquare()) {
        throw new Error("Cholesky decomposition requires a square matrix");
    }
    if (!matrix.isSymmetric()) {
        throw new Error("Cholesky decomposition requires a symmetric matrix");
    }

    const n = matrix.rows;
    const L = new Matrix({ rows: n, cols: n });

    for (let i = 0; i < n; i++) {
        for (let j = 0; j <= i; j++) {
            let sum = 0;

            if (i === j) {
                // Diagonal elements
                for (let k = 0; k < j; k++) {
                    sum += L.get(j, k) ** 2;
                }
                const value = matrix.get(j, j) - sum;
                if (value <= 0) {
                    throw new Error("Matrix is not positive definite");
                }
                L.set(j, j, Math.sqrt(value));
            } else {
                // Off-diagonal elements
                for (let k = 0; k < j; k++) {
                    sum += L.get(i, k) * L.get(j, k);
                }
                L.set(i, j, (matrix.get(i, j) - sum) / L.get(j, j));
            }
        }
    }

    return L;
}

// Eigenvalues and eigenvectors using QR algorithm (simplified version)
export function eigenDecomposition(matrix, maxIterations = 100, tolerance = 1e-10) {
    if (!matrix.isSquare()) {
        throw new Error("Eigendecomposition requires a square matrix");
    }

    const n = matrix.rows;
    let A = matrix.clone();
    let V = identity(n);

    // QR algorithm
    for (let iter = 0; iter < maxIterations; iter++) {
        const { Q, R } = qrDecomposition(A);
        A = multiply(R, Q);
        V = multiply(V, Q);

        // Check convergence (simplified)
        let offDiagonalSum = 0;
        for (let i = 0; i < n; i++) {
            for (let j = 0; j < n; j++) {
                if (i !== j) {
                    offDiagonalSum += Math.abs(A.get(i, j));
                }
            }
        }

        if (offDiagonalSum < tolerance) break;
    }

    // Extract eigenvalues from diagonal
    const eigenvalues = [];
    for (let i = 0; i < n; i++) {
        eigenvalues.push(A.get(i, i));
    }

    return { eigenvalues, eigenvectors: V };
}

// Singular Value Decomposition (simplified version)
export function svd(matrix) {
    // Compute A^T * A
    const At = transpose(matrix);
    const AtA = multiply(At, matrix);

    // Get eigendecomposition of A^T * A
    const { eigenvalues, eigenvectors: V } = eigenDecomposition(AtA);

    // Compute singular values
    const singularValues = eigenvalues.map(val => Math.sqrt(Math.max(0, val)));

    // Sort singular values and corresponding vectors
    const sorted = singularValues.map((val, idx) => ({ val, idx }))
        .sort((a, b) => b.val - a.val);

    const S = diagonal(sorted.map(item => item.val));

    // Reorder V columns
    const Vreordered = new Matrix({ rows: V.rows, cols: V.cols });
    for (let i = 0; i < V.cols; i++) {
        const col = V.getColumn(sorted[i].idx);
        Vreordered.setColumn(i, col);
    }

    // Compute U = A * V * S^(-1)
    const U = new Matrix({ rows: matrix.rows, cols: Math.min(matrix.rows, matrix.cols) });
    for (let i = 0; i < U.cols; i++) {
        if (singularValues[sorted[i].idx] > 1e-10) {
            const v = Vreordered.getColumn(i);
            const u = [];
            for (let j = 0; j < matrix.rows; j++) {
                let sum = 0;
                for (let k = 0; k < matrix.cols; k++) {
                    sum += matrix.get(j, k) * v[k];
                }
                u.push(sum / singularValues[sorted[i].idx]);
            }
            U.setColumn(i, u);
        }
    }

    return { U, S, V: Vreordered };
}

// Solve linear system Ax = b using Gaussian elimination
export function solve(A, b) {
    if (!A.isSquare()) {
        throw new Error("Coefficient matrix must be square");
    }
    if (b.length !== A.rows) {
        throw new Error("Vector b length must match matrix dimensions");
    }

    const n = A.rows;
    const augmented = new Matrix({ rows: n, cols: n + 1 });

    // Create augmented matrix [A | b]
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            augmented.set(i, j, A.get(i, j));
        }
        augmented.set(i, n, b[i]);
    }

    // Forward elimination
    for (let i = 0; i < n; i++) {
        // Find pivot
        let maxRow = i;
        for (let k = i + 1; k < n; k++) {
            if (Math.abs(augmented.get(k, i)) > Math.abs(augmented.get(maxRow, i))) {
                maxRow = k;
            }
        }

        // Swap rows
        if (maxRow !== i) {
            for (let j = 0; j <= n; j++) {
                const temp = augmented.get(i, j);
                augmented.set(i, j, augmented.get(maxRow, j));
                augmented.set(maxRow, j, temp);
            }
        }

        // Check for singular matrix
        if (Math.abs(augmented.get(i, i)) < 1e-10) {
            throw new Error("Matrix is singular or nearly singular");
        }

        // Eliminate below
        for (let k = i + 1; k < n; k++) {
            const factor = augmented.get(k, i) / augmented.get(i, i);
            for (let j = i; j <= n; j++) {
                augmented.set(k, j, augmented.get(k, j) - factor * augmented.get(i, j));
            }
        }
    }

    // Back substitution
    const x = new Array(n);
    for (let i = n - 1; i >= 0; i--) {
        x[i] = augmented.get(i, n);
        for (let j = i + 1; j < n; j++) {
            x[i] -= augmented.get(i, j) * x[j];
        }
        x[i] /= augmented.get(i, i);
    }

    return x;
}

// Least squares solution using normal equations
export function leastSquares(A, b) {
    // Solve A^T * A * x = A^T * b
    const At = transpose(A);
    const AtA = multiply(At, A);
    const Atb = [];

    for (let i = 0; i < At.rows; i++) {
        let sum = 0;
        for (let j = 0; j < At.cols; j++) {
            sum += At.get(i, j) * b[j];
        }
        Atb.push(sum);
    }

    return solve(AtA, Atb);
}

// Pseudo-inverse using SVD
export function pseudoInverse(matrix, tolerance = 1e-10) {
    const { U, S, V } = svd(matrix);

    // Compute S+
    const Splus = new Matrix({ rows: S.cols, cols: S.rows });
    for (let i = 0; i < Math.min(S.rows, S.cols); i++) {
        const val = S.get(i, i);
        if (Math.abs(val) > tolerance) {
            Splus.set(i, i, 1 / val);
        }
    }

    // Compute A+ = V * S+ * U^T
    const VSplus = multiply(V, Splus);
    const Ut = transpose(U);
    return multiply(VSplus, Ut);
}

// Matrix condition number
export function conditionNumber(matrix) {
    const { S } = svd(matrix);
    const singularValues = [];
    for (let i = 0; i < Math.min(S.rows, S.cols); i++) {
        singularValues.push(S.get(i, i));
    }

    const maxSV = Math.max(...singularValues);
    const minSV = Math.min(...singularValues.filter(v => Math.abs(v) > 1e-10));

    return maxSV / minSV;
}

// Kronecker product
export function kroneckerProduct(A, B) {
    const result = new Matrix({
        rows: A.rows * B.rows,
        cols: A.cols * B.cols
    });

    for (let i = 0; i < A.rows; i++) {
        for (let j = 0; j < A.cols; j++) {
            const aij = A.get(i, j);
            for (let k = 0; k < B.rows; k++) {
                for (let l = 0; l < B.cols; l++) {
                    result.set(i * B.rows + k, j * B.cols + l, aij * B.get(k, l));
                }
            }
        }
    }

    return result;
}

// Hadamard product (element-wise multiplication)
export function hadamardProduct(A, B) {
    if (A.rows !== B.rows || A.cols !== B.cols) {
        throw new Error("Matrices must have the same dimensions for Hadamard product");
    }

    const result = new Matrix({ rows: A.rows, cols: A.cols });
    for (let i = 0; i < A.rows; i++) {
        for (let j = 0; j < A.cols; j++) {
            result.set(i, j, A.get(i, j) * B.get(i, j));
        }
    }

    return result;
}

// Matrix exponential using Taylor series
export function matrixExponential(matrix, terms = 20) {
    if (!matrix.isSquare()) {
        throw new Error("Matrix exponential requires a square matrix");
    }

    const n = matrix.rows;
    let result = identity(n);
    let term = identity(n);

    for (let k = 1; k <= terms; k++) {
        term = multiply(term, matrix);
        const scaledTerm = scalarMultiply(term, 1 / factorial(k));
        result = add(result, scaledTerm);
    }

    return result;
}

// Helper function for factorial
function factorial(n) {
    if (n <= 1) return 1;
    let result = 1;
    for (let i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// Export all functions as a default object for convenience
export default {
    Matrix,
    identity,
    zeros,
    ones,
    diagonal,
    random,
    add,
    subtract,
    multiply,
    scalarMultiply,
    transpose,
    trace,
    determinant,
    inverse,
    rank,
    frobeniusNorm,
    power,
    dotProduct,
    crossProduct,
    vectorNorm,
    luDecomposition,
    qrDecomposition,
    choleskyDecomposition,
    eigenDecomposition,
    svd,
    solve,
    leastSquares,
    pseudoInverse,
    conditionNumber,
    kroneckerProduct,
    hadamardProduct,
    matrixExponential
};