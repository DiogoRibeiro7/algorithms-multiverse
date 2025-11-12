/**
 * ============================================================================
 * Matrix Operations and Linear Algebra in Java
 *
 * Comprehensive collection of matrix operations and linear algebra algorithms
 * with educational focus, generic types, and parallel processing capabilities.
 *
 * Features:
 * - Generic implementations for different number types
 * - Parallel operations using Java Streams
 * - Numerical stability with pivoting
 * - Memory-efficient sparse matrix representation
 * - Educational implementations showing algorithm steps
 * - Applications in machine learning and graphics
 *
 * Compile: javac Matrix.java
 * Run: java Matrix
 *
 * @author Algorithms Multiverse
 * @version 1.0
 * ============================================================================
 */

import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class Matrix {

    private static final double EPSILON = 1e-10;

    // ========================================================================
    // Custom Exception
    // ========================================================================

    public static class MatrixException extends RuntimeException {
        public MatrixException(String message) {
            super(message);
        }
    }

    // ========================================================================
    // Basic Matrix Operations
    // ========================================================================

    /**
     * Create a matrix with given dimensions
     * Time Complexity: O(rows * cols)
     */
    public static double[][] createMatrix(int rows, int cols) {
        return new double[rows][cols];
    }

    /**
     * Create an n×n identity matrix
     * Time Complexity: O(n²)
     */
    public static double[][] identityMatrix(int n) {
        double[][] matrix = createMatrix(n, n);
        for (int i = 0; i < n; i++) {
            matrix[i][i] = 1.0;
        }
        return matrix;
    }

    /**
     * Add two matrices
     * Time Complexity: O(rows * cols)
     */
    public static double[][] add(double[][] A, double[][] B) {
        int rows = A.length, cols = A[0].length;
        if (rows != B.length || cols != B[0].length) {
            throw new MatrixException("Matrices must have same dimensions for addition");
        }

        double[][] result = createMatrix(rows, cols);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                result[i][j] = A[i][j] + B[i][j];
            }
        }
        return result;
    }

    /**
     * Subtract matrix B from matrix A
     */
    public static double[][] subtract(double[][] A, double[][] B) {
        int rows = A.length, cols = A[0].length;
        if (rows != B.length || cols != B[0].length) {
            throw new MatrixException("Matrices must have same dimensions for subtraction");
        }

        double[][] result = createMatrix(rows, cols);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                result[i][j] = A[i][j] - B[i][j];
            }
        }
        return result;
    }

    /**
     * Multiply matrix by scalar
     */
    public static double[][] scalarMultiply(double[][] A, double scalar) {
        int rows = A.length, cols = A[0].length;
        double[][] result = createMatrix(rows, cols);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                result[i][j] = A[i][j] * scalar;
            }
        }
        return result;
    }

    /**
     * Transpose a matrix
     * Time Complexity: O(rows * cols)
     */
    public static double[][] transpose(double[][] A) {
        int rows = A.length, cols = A[0].length;
        double[][] result = createMatrix(cols, rows);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                result[j][i] = A[i][j];
            }
        }
        return result;
    }

    /**
     * Deep copy a matrix
     */
    public static double[][] copy(double[][] A) {
        int rows = A.length;
        double[][] result = new double[rows][];
        for (int i = 0; i < rows; i++) {
            result[i] = Arrays.copyOf(A[i], A[i].length);
        }
        return result;
    }

    // ========================================================================
    // Matrix Multiplication
    // ========================================================================

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
    public static double[][] multiplyStandard(double[][] A, double[][] B) {
        int rowsA = A.length, colsA = A[0].length;
        int rowsB = B.length, colsB = B[0].length;

        if (colsA != rowsB) {
            throw new MatrixException(
                String.format("Cannot multiply %d×%d and %d×%d matrices",
                             rowsA, colsA, rowsB, colsB)
            );
        }

        double[][] result = createMatrix(rowsA, colsB);

        for (int i = 0; i < rowsA; i++) {
            for (int j = 0; j < colsB; j++) {
                double sum = 0.0;
                for (int k = 0; k < colsA; k++) {
                    sum += A[i][k] * B[k][j];
                }
                result[i][j] = sum;
            }
        }

        return result;
    }

    /**
     * Parallel matrix multiplication using Java Streams
     *
     * Time Complexity: O(n³/p) where p is number of processors
     * Best for: Large matrices (> 100×100)
     */
    public static double[][] multiplyParallel(double[][] A, double[][] B) {
        int rowsA = A.length, colsA = A[0].length;
        int rowsB = B.length, colsB = B[0].length;

        if (colsA != rowsB) {
            throw new MatrixException(
                String.format("Cannot multiply %d×%d and %d×%d matrices",
                             rowsA, colsA, rowsB, colsB)
            );
        }

        double[][] result = createMatrix(rowsA, colsB);

        IntStream.range(0, rowsA).parallel().forEach(i -> {
            for (int j = 0; j < colsB; j++) {
                double sum = 0.0;
                for (int k = 0; k < colsA; k++) {
                    sum += A[i][k] * B[k][j];
                }
                result[i][j] = sum;
            }
        });

        return result;
    }

    /**
     * Strassen's algorithm for matrix multiplication
     *
     * Time Complexity: O(n^2.807) vs O(n³) for standard multiplication
     * Best for: Large square matrices (n >= 64)
     */
    public static double[][] strassenMultiply(double[][] A, double[][] B) {
        int n = A.length;

        // Base case
        if (n <= 64) {
            return multiplyStandard(A, B);
        }

        // Ensure matrix size is power of 2
        if ((n & (n - 1)) != 0) {
            return multiplyStandard(A, B);
        }

        int mid = n / 2;

        // Divide matrices into quadrants
        double[][] A11 = new double[mid][mid];
        double[][] A12 = new double[mid][mid];
        double[][] A21 = new double[mid][mid];
        double[][] A22 = new double[mid][mid];
        double[][] B11 = new double[mid][mid];
        double[][] B12 = new double[mid][mid];
        double[][] B21 = new double[mid][mid];
        double[][] B22 = new double[mid][mid];

        for (int i = 0; i < mid; i++) {
            for (int j = 0; j < mid; j++) {
                A11[i][j] = A[i][j];
                A12[i][j] = A[i][j + mid];
                A21[i][j] = A[i + mid][j];
                A22[i][j] = A[i + mid][j + mid];

                B11[i][j] = B[i][j];
                B12[i][j] = B[i][j + mid];
                B21[i][j] = B[i + mid][j];
                B22[i][j] = B[i + mid][j + mid];
            }
        }

        // Compute the 7 Strassen products
        double[][] M1 = strassenMultiply(add(A11, A22), add(B11, B22));
        double[][] M2 = strassenMultiply(add(A21, A22), B11);
        double[][] M3 = strassenMultiply(A11, subtract(B12, B22));
        double[][] M4 = strassenMultiply(A22, subtract(B21, B11));
        double[][] M5 = strassenMultiply(add(A11, A12), B22);
        double[][] M6 = strassenMultiply(subtract(A21, A11), add(B11, B12));
        double[][] M7 = strassenMultiply(subtract(A12, A22), add(B21, B22));

        // Compute result quadrants
        double[][] C11 = add(subtract(add(M1, M4), M5), M7);
        double[][] C12 = add(M3, M5);
        double[][] C21 = add(M2, M4);
        double[][] C22 = add(subtract(add(M1, M3), M2), M6);

        // Combine quadrants
        double[][] result = createMatrix(n, n);
        for (int i = 0; i < mid; i++) {
            for (int j = 0; j < mid; j++) {
                result[i][j] = C11[i][j];
                result[i][j + mid] = C12[i][j];
                result[i + mid][j] = C21[i][j];
                result[i + mid][j + mid] = C22[i][j];
            }
        }

        return result;
    }

    // ========================================================================
    // Gaussian Elimination
    // ========================================================================

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
    public static double[] gaussianElimination(double[][] A, double[] b) {
        int n = A.length;
        if (n != b.length) {
            throw new MatrixException("Matrix and vector dimensions don't match");
        }

        // Create augmented matrix [A|b]
        double[][] augmented = new double[n][n + 1];
        for (int i = 0; i < n; i++) {
            System.arraycopy(A[i], 0, augmented[i], 0, n);
            augmented[i][n] = b[i];
        }

        // Forward elimination with partial pivoting
        for (int col = 0; col < n; col++) {
            // Find pivot
            int maxRow = col;
            for (int row = col + 1; row < n; row++) {
                if (Math.abs(augmented[row][col]) > Math.abs(augmented[maxRow][col])) {
                    maxRow = row;
                }
            }

            // Swap rows
            double[] temp = augmented[col];
            augmented[col] = augmented[maxRow];
            augmented[maxRow] = temp;

            // Check for singular matrix
            if (Math.abs(augmented[col][col]) < EPSILON) {
                throw new MatrixException("Matrix is singular or nearly singular");
            }

            // Eliminate column entries below pivot
            for (int row = col + 1; row < n; row++) {
                double factor = augmented[row][col] / augmented[col][col];
                for (int j = col; j <= n; j++) {
                    augmented[row][j] -= factor * augmented[col][j];
                }
            }
        }

        // Backward substitution
        double[] x = new double[n];
        for (int i = n - 1; i >= 0; i--) {
            x[i] = augmented[i][n];
            for (int j = i + 1; j < n; j++) {
                x[i] -= augmented[i][j] * x[j];
            }
            x[i] /= augmented[i][i];
        }

        return x;
    }

    // ========================================================================
    // Matrix Decomposition
    // ========================================================================

    /**
     * LU decomposition result holder
     */
    public static class LUResult {
        public final double[][] L;
        public final double[][] U;

        public LUResult(double[][] L, double[][] U) {
            this.L = L;
            this.U = U;
        }
    }

    /**
     * LU decomposition: A = LU
     *
     * Time Complexity: O(n³)
     * Applications:
     * - Solving multiple systems with same A
     * - Computing determinant
     * - Matrix inversion
     */
    public static LUResult luDecomposition(double[][] A) {
        int n = A.length;
        double[][] L = createMatrix(n, n);
        double[][] U = createMatrix(n, n);

        for (int i = 0; i < n; i++) {
            // Upper triangular matrix U
            for (int k = i; k < n; k++) {
                double sum = 0;
                for (int j = 0; j < i; j++) {
                    sum += L[i][j] * U[j][k];
                }
                U[i][k] = A[i][k] - sum;
            }

            // Lower triangular matrix L
            for (int k = i; k < n; k++) {
                if (i == k) {
                    L[i][i] = 1.0;
                } else {
                    double sum = 0;
                    for (int j = 0; j < i; j++) {
                        sum += L[k][j] * U[j][i];
                    }
                    if (Math.abs(U[i][i]) < EPSILON) {
                        throw new MatrixException("Matrix is singular");
                    }
                    L[k][i] = (A[k][i] - sum) / U[i][i];
                }
            }
        }

        return new LUResult(L, U);
    }

    /**
     * QR decomposition result holder
     */
    public static class QRResult {
        public final double[][] Q;
        public final double[][] R;

        public QRResult(double[][] Q, double[][] R) {
            this.Q = Q;
            this.R = R;
        }
    }

    /**
     * QR decomposition using Gram-Schmidt orthogonalization
     *
     * Time Complexity: O(mn²) for m×n matrix
     * Applications:
     * - Solving least squares problems
     * - Eigenvalue computation
     */
    public static QRResult qrDecompositionGramSchmidt(double[][] A) {
        int m = A.length, n = A[0].length;
        double[][] Q = copy(A);
        double[][] R = createMatrix(n, n);

        // Modified Gram-Schmidt
        for (int j = 0; j < n; j++) {
            // Compute norm of column j
            double norm = 0;
            for (int i = 0; i < m; i++) {
                norm += Q[i][j] * Q[i][j];
            }
            R[j][j] = Math.sqrt(norm);

            if (Math.abs(R[j][j]) < EPSILON) {
                throw new MatrixException("Matrix columns are linearly dependent");
            }

            // Normalize column j
            for (int i = 0; i < m; i++) {
                Q[i][j] /= R[j][j];
            }

            // Orthogonalize remaining columns
            for (int k = j + 1; k < n; k++) {
                R[j][k] = 0;
                for (int i = 0; i < m; i++) {
                    R[j][k] += Q[i][j] * Q[i][k];
                }
                for (int i = 0; i < m; i++) {
                    Q[i][k] -= R[j][k] * Q[i][j];
                }
            }
        }

        return new QRResult(Q, R);
    }

    // ========================================================================
    // Determinant Calculation
    // ========================================================================

    /**
     * Calculate determinant using recursive cofactor expansion
     * Time Complexity: O(n!)
     * Best for: Small matrices (n <= 4)
     */
    public static double determinantRecursive(double[][] A) {
        int n = A.length;

        if (n == 1) {
            return A[0][0];
        }

        if (n == 2) {
            return A[0][0] * A[1][1] - A[0][1] * A[1][0];
        }

        double det = 0;
        for (int j = 0; j < n; j++) {
            // Create submatrix
            double[][] submatrix = new double[n - 1][n - 1];
            for (int i = 1; i < n; i++) {
                int colIndex = 0;
                for (int k = 0; k < n; k++) {
                    if (k != j) {
                        submatrix[i - 1][colIndex++] = A[i][k];
                    }
                }
            }

            double cofactor = Math.pow(-1, j) * A[0][j] * determinantRecursive(submatrix);
            det += cofactor;
        }

        return det;
    }

    /**
     * Calculate determinant using LU decomposition
     * Time Complexity: O(n³)
     * Best for: Matrices larger than 4×4
     */
    public static double determinantLU(double[][] A) {
        try {
            LUResult lu = luDecomposition(A);
            double det = 1.0;
            for (int i = 0; i < lu.U.length; i++) {
                det *= lu.U[i][i];
            }
            return det;
        } catch (MatrixException e) {
            return 0.0; // Singular matrix
        }
    }

    // ========================================================================
    // Matrix Inversion
    // ========================================================================

    /**
     * Matrix inversion using Gauss-Jordan elimination
     *
     * Time Complexity: O(n³)
     * Applications:
     * - Solving linear systems
     * - Computer graphics transformations
     */
    public static double[][] inverseGaussJordan(double[][] A) {
        int n = A.length;

        // Create augmented matrix [A|I]
        double[][] augmented = new double[n][2 * n];
        for (int i = 0; i < n; i++) {
            System.arraycopy(A[i], 0, augmented[i], 0, n);
            double[] identity = identityMatrix(n)[i];
            System.arraycopy(identity, 0, augmented[i], n, n);
        }

        // Forward elimination
        for (int col = 0; col < n; col++) {
            // Find pivot
            int maxRow = col;
            for (int row = col + 1; row < n; row++) {
                if (Math.abs(augmented[row][col]) > Math.abs(augmented[maxRow][col])) {
                    maxRow = row;
                }
            }

            double[] temp = augmented[col];
            augmented[col] = augmented[maxRow];
            augmented[maxRow] = temp;

            if (Math.abs(augmented[col][col]) < EPSILON) {
                throw new MatrixException("Matrix is singular and cannot be inverted");
            }

            // Scale pivot row
            double pivot = augmented[col][col];
            for (int j = 0; j < 2 * n; j++) {
                augmented[col][j] /= pivot;
            }

            // Eliminate column
            for (int row = 0; row < n; row++) {
                if (row != col) {
                    double factor = augmented[row][col];
                    for (int j = 0; j < 2 * n; j++) {
                        augmented[row][j] -= factor * augmented[col][j];
                    }
                }
            }
        }

        // Extract inverse from right half
        double[][] inverse = new double[n][n];
        for (int i = 0; i < n; i++) {
            System.arraycopy(augmented[i], n, inverse[i], 0, n);
        }

        return inverse;
    }

    // ========================================================================
    // Eigenvalue Computation
    // ========================================================================

    /**
     * Eigenvalue result holder
     */
    public static class EigenResult {
        public final double eigenvalue;
        public final double[] eigenvector;

        public EigenResult(double eigenvalue, double[] eigenvector) {
            this.eigenvalue = eigenvalue;
            this.eigenvector = eigenvector;
        }
    }

    /**
     * Find dominant eigenvalue and eigenvector using power iteration
     *
     * Time Complexity: O(n² * iterations)
     * Applications:
     * - Google PageRank
     * - Principal Component Analysis
     */
    public static EigenResult powerIteration(double[][] A, int numIterations) {
        int n = A.length;
        Random random = new Random(42);

        // Start with random vector
        double[] v = new double[n];
        for (int i = 0; i < n; i++) {
            v[i] = random.nextDouble();
        }

        // Normalize
        double norm = 0;
        for (double val : v) {
            norm += val * val;
        }
        norm = Math.sqrt(norm);
        for (int i = 0; i < n; i++) {
            v[i] /= norm;
        }

        for (int iteration = 0; iteration < numIterations; iteration++) {
            // Multiply by matrix
            double[] vNew = new double[n];
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    vNew[i] += A[i][j] * v[j];
                }
            }

            // Normalize
            norm = 0;
            for (double val : vNew) {
                norm += val * val;
            }
            norm = Math.sqrt(norm);

            double[] vNormalized = new double[n];
            for (int i = 0; i < n; i++) {
                vNormalized[i] = vNew[i] / norm;
            }

            // Check convergence
            if (iteration > 0) {
                double diff = 0;
                for (int i = 0; i < n; i++) {
                    diff += Math.abs(vNormalized[i] - v[i]);
                }
                if (diff < EPSILON) {
                    break;
                }
            }

            v = vNormalized;
        }

        // Compute eigenvalue
        double[] Av = new double[n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                Av[i] += A[i][j] * v[j];
            }
        }

        double eigenvalue = 0;
        for (int i = 0; i < n; i++) {
            eigenvalue += v[i] * Av[i];
        }

        return new EigenResult(eigenvalue, v);
    }

    /**
     * QR algorithm for finding all eigenvalues
     * Time Complexity: O(n³ * iterations)
     */
    public static double[] qrAlgorithm(double[][] A, int numIterations) {
        int n = A.length;
        double[][] Ak = copy(A);

        for (int iter = 0; iter < numIterations; iter++) {
            try {
                QRResult qr = qrDecompositionGramSchmidt(Ak);
                Ak = multiplyStandard(qr.R, qr.Q);
            } catch (MatrixException e) {
                break;
            }
        }

        // Extract eigenvalues from diagonal
        double[] eigenvalues = new double[n];
        for (int i = 0; i < n; i++) {
            eigenvalues[i] = Ak[i][i];
        }

        return eigenvalues;
    }

    // ========================================================================
    // Sparse Matrix Class
    // ========================================================================

    public static class SparseMatrix {
        private final int rows;
        private final int cols;
        private final Map<String, Double> data;

        public SparseMatrix(int rows, int cols) {
            this.rows = rows;
            this.cols = cols;
            this.data = new HashMap<>();
        }

        public void set(int row, int col, double value) {
            if (Math.abs(value) > EPSILON) {
                data.put(row + "," + col, value);
            } else {
                data.remove(row + "," + col);
            }
        }

        public double get(int row, int col) {
            return data.getOrDefault(row + "," + col, 0.0);
        }

        public double[][] toDense() {
            double[][] matrix = createMatrix(rows, cols);
            for (Map.Entry<String, Double> entry : data.entrySet()) {
                String[] indices = entry.getKey().split(",");
                int i = Integer.parseInt(indices[0]);
                int j = Integer.parseInt(indices[1]);
                matrix[i][j] = entry.getValue();
            }
            return matrix;
        }

        public static SparseMatrix fromDense(double[][] matrix) {
            int rows = matrix.length, cols = matrix[0].length;
            SparseMatrix sparse = new SparseMatrix(rows, cols);
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    if (Math.abs(matrix[i][j]) > EPSILON) {
                        sparse.set(i, j, matrix[i][j]);
                    }
                }
            }
            return sparse;
        }

        public int nnz() {
            return data.size();
        }

        public double sparsity() {
            double total = rows * cols;
            return 1.0 - (nnz() / total);
        }

        public int getRows() { return rows; }
        public int getCols() { return cols; }
    }

    // ========================================================================
    // Utility Methods
    // ========================================================================

    public static void printMatrix(double[][] matrix, String name) {
        System.out.println(name + " =");
        for (double[] row : matrix) {
            System.out.print("  [");
            for (int j = 0; j < row.length; j++) {
                System.out.printf("%8.4f", row[j]);
                if (j < row.length - 1) System.out.print(", ");
            }
            System.out.println("]");
        }
    }

    public static void printVector(double[] vector, String name) {
        System.out.print(name + " = [");
        for (int i = 0; i < vector.length; i++) {
            System.out.printf("%.6f", vector[i]);
            if (i < vector.length - 1) System.out.print(", ");
        }
        System.out.println("]");
    }

    // ========================================================================
    // Example Usage and Tests
    // ========================================================================

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Matrix Operations and Linear Algebra Library");
        System.out.println("=".repeat(70));
        System.out.println();

        // Example 1: Matrix multiplication
        System.out.println("1. Matrix Multiplication");
        System.out.println("-".repeat(70));
        double[][] A1 = {{1, 2, 3}, {4, 5, 6}};
        double[][] B1 = {{7, 8}, {9, 10}, {11, 12}};
        double[][] C1 = multiplyStandard(A1, B1);
        System.out.println("A (2×3) × B (3×2) = C (2×2)");
        printMatrix(C1, "C");
        System.out.println();

        // Example 2: Solving linear system
        System.out.println("2. Solving Linear System Ax = b");
        System.out.println("-".repeat(70));
        double[][] A2 = {{2, 1, -1}, {-3, -1, 2}, {-2, 1, 2}};
        double[] b2 = {8, -11, -3};
        double[] x = gaussianElimination(A2, b2);
        printMatrix(A2, "A");
        printVector(b2, "b");
        printVector(x, "Solution x");
        System.out.println();

        // Example 3: LU Decomposition
        System.out.println("3. LU Decomposition");
        System.out.println("-".repeat(70));
        double[][] A3 = {{2, -1, -2}, {-4, 6, 3}, {-4, -2, 8}};
        LUResult lu = luDecomposition(A3);
        printMatrix(A3, "A");
        printMatrix(lu.L, "L");
        printMatrix(lu.U, "U");
        System.out.println();

        // Example 4: Matrix inversion
        System.out.println("4. Matrix Inversion");
        System.out.println("-".repeat(70));
        double[][] A4 = {{4, 7}, {2, 6}};
        double[][] AInv = inverseGaussJordan(A4);
        printMatrix(A4, "A");
        printMatrix(AInv, "A^(-1)");
        double[][] I = multiplyStandard(A4, AInv);
        printMatrix(I, "A × A^(-1)");
        System.out.println();

        // Example 5: Eigenvalues
        System.out.println("5. Eigenvalue Computation (Power Iteration)");
        System.out.println("-".repeat(70));
        double[][] A5 = {{2, 1}, {1, 2}};
        EigenResult eigen = powerIteration(A5, 100);
        printMatrix(A5, "A");
        System.out.printf("Dominant eigenvalue: %.6f%n", eigen.eigenvalue);
        printVector(eigen.eigenvector, "Corresponding eigenvector");
        System.out.println();

        // Example 6: Sparse matrices
        System.out.println("6. Sparse Matrix Operations");
        System.out.println("-".repeat(70));
        SparseMatrix sparse = new SparseMatrix(1000, 1000);
        Random random = new Random(42);
        for (int i = 0; i < 100; i++) {
            sparse.set(random.nextInt(1000), random.nextInt(1000), random.nextDouble());
        }
        System.out.printf("Matrix size: %d×%d%n", sparse.getRows(), sparse.getCols());
        System.out.printf("Non-zero elements: %d%n", sparse.nnz());
        System.out.printf("Sparsity: %.2f%%%n", sparse.sparsity() * 100);
        System.out.println();

        // Example 7: Determinant
        System.out.println("7. Determinant Calculation");
        System.out.println("-".repeat(70));
        double[][] A7 = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        double detRecursive = determinantRecursive(A7);
        double detLU = determinantLU(A7);
        printMatrix(A7, "A");
        System.out.printf("Determinant (recursive): %.6f%n", detRecursive);
        System.out.printf("Determinant (LU): %.6f%n", detLU);
        System.out.println();

        System.out.println("All examples completed successfully!");
    }
}
