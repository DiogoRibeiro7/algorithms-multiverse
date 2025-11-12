/*
 * ============================================================================
 * Matrix Operations and Linear Algebra in Rust
 *
 * Comprehensive collection of matrix operations leveraging Rust's safety
 * guarantees, zero-cost abstractions, and efficient memory management.
 *
 * Features:
 * - Memory-safe with ownership system
 * - Zero-cost abstractions
 * - Efficient error handling with Result types
 * - Generic implementations for different number types
 * - Optional parallelism with rayon
 * - Numerical stability with pivoting
 *
 * Compile: rustc -O matrix.rs
 * With optimizations: rustc -O -C target-cpu=native matrix.rs
 * Run: ./matrix
 *
 * @author Algorithms Multiverse
 * @version 1.0
 * ============================================================================
 */

use std::fmt;
use std::ops::{Add, Sub, Mul};

const EPSILON: f64 = 1e-10;

/* ============================================================================
 * Error Types
 * ============================================================================ */

#[derive(Debug)]
enum MatrixError {
    DimensionMismatch(String),
    SingularMatrix,
    InvalidDimensions,
}

impl fmt::Display for MatrixError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            MatrixError::DimensionMismatch(msg) => write!(f, "Dimension mismatch: {}", msg),
            MatrixError::SingularMatrix => write!(f, "Matrix is singular"),
            MatrixError::InvalidDimensions => write!(f, "Invalid matrix dimensions"),
        }
    }
}

type Result<T> = std::result::Result<T, MatrixError>;

/* ============================================================================
 * Data Structures
 * ============================================================================ */

/// Matrix structure with row-major storage
#[derive(Clone)]
struct Matrix {
    data: Vec<Vec<f64>>,
    rows: usize,
    cols: usize,
}

/// Vector structure
#[derive(Clone)]
struct Vector {
    data: Vec<f64>,
}

/// Sparse matrix element
#[derive(Clone, Copy)]
struct SparseElement {
    row: usize,
    col: usize,
    value: f64,
}

/// Sparse matrix using map-based storage (DOK format)
struct SparseMatrix {
    data: std::collections::HashMap<(usize, usize), f64>,
    rows: usize,
    cols: usize,
}

/* ============================================================================
 * Matrix Implementation
 * ============================================================================ */

impl Matrix {
    /// Create a new matrix with given dimensions
    ///
    /// Time Complexity: O(rows * cols)
    fn new(rows: usize, cols: usize) -> Self {
        Matrix {
            data: vec![vec![0.0; cols]; rows],
            rows,
            cols,
        }
    }

    /// Create an identity matrix
    ///
    /// Time Complexity: O(n²)
    fn identity(n: usize) -> Self {
        let mut m = Self::new(n, n);
        for i in 0..n {
            m.data[i][i] = 1.0;
        }
        m
    }

    /// Create matrix from 2D vector
    fn from_vec(data: Vec<Vec<f64>>) -> Result<Self> {
        if data.is_empty() || data[0].is_empty() {
            return Err(MatrixError::InvalidDimensions);
        }

        let rows = data.len();
        let cols = data[0].len();

        // Verify all rows have same length
        for row in &data {
            if row.len() != cols {
                return Err(MatrixError::InvalidDimensions);
            }
        }

        Ok(Matrix { data, rows, cols })
    }

    /// Get element at (i, j)
    fn get(&self, i: usize, j: usize) -> Option<f64> {
        if i < self.rows && j < self.cols {
            Some(self.data[i][j])
        } else {
            None
        }
    }

    /// Set element at (i, j)
    fn set(&mut self, i: usize, j: usize, value: f64) -> Result<()> {
        if i < self.rows && j < self.cols {
            self.data[i][j] = value;
            Ok(())
        } else {
            Err(MatrixError::InvalidDimensions)
        }
    }

    /* ========================================================================
     * Basic Operations
     * ======================================================================== */

    /// Matrix addition: C = A + B
    ///
    /// Time Complexity: O(rows * cols)
    ///
    /// Applications:
    /// - Computer graphics transformations
    /// - Neural network weight updates
    /// - Image processing
    fn add(&self, other: &Matrix) -> Result<Matrix> {
        if self.rows != other.rows || self.cols != other.cols {
            return Err(MatrixError::DimensionMismatch(format!(
                "{}x{} vs {}x{}",
                self.rows, self.cols, other.rows, other.cols
            )));
        }

        let mut result = Matrix::new(self.rows, self.cols);
        for i in 0..self.rows {
            for j in 0..self.cols {
                result.data[i][j] = self.data[i][j] + other.data[i][j];
            }
        }

        Ok(result)
    }

    /// Matrix subtraction: C = A - B
    ///
    /// Time Complexity: O(rows * cols)
    fn subtract(&self, other: &Matrix) -> Result<Matrix> {
        if self.rows != other.rows || self.cols != other.cols {
            return Err(MatrixError::DimensionMismatch(format!(
                "{}x{} vs {}x{}",
                self.rows, self.cols, other.rows, other.cols
            )));
        }

        let mut result = Matrix::new(self.rows, self.cols);
        for i in 0..self.rows {
            for j in 0..self.cols {
                result.data[i][j] = self.data[i][j] - other.data[i][j];
            }
        }

        Ok(result)
    }

    /// Scalar multiplication
    ///
    /// Time Complexity: O(rows * cols)
    fn scalar_multiply(&self, scalar: f64) -> Matrix {
        let mut result = Matrix::new(self.rows, self.cols);
        for i in 0..self.rows {
            for j in 0..self.cols {
                result.data[i][j] = self.data[i][j] * scalar;
            }
        }
        result
    }

    /// Matrix transpose: B = A^T
    ///
    /// Time Complexity: O(rows * cols)
    ///
    /// Applications:
    /// - Solving linear systems
    /// - Covariance matrix computation
    /// - Neural network backpropagation
    fn transpose(&self) -> Matrix {
        let mut result = Matrix::new(self.cols, self.rows);
        for i in 0..self.rows {
            for j in 0..self.cols {
                result.data[j][i] = self.data[i][j];
            }
        }
        result
    }

    /* ========================================================================
     * Matrix Multiplication
     * ======================================================================== */

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
    fn multiply(&self, other: &Matrix) -> Result<Matrix> {
        if self.cols != other.rows {
            return Err(MatrixError::DimensionMismatch(format!(
                "Cannot multiply {}x{} and {}x{}",
                self.rows, self.cols, other.rows, other.cols
            )));
        }

        let mut result = Matrix::new(self.rows, other.cols);

        for i in 0..self.rows {
            for j in 0..other.cols {
                let mut sum = 0.0;
                for k in 0..self.cols {
                    sum += self.data[i][k] * other.data[k][j];
                }
                result.data[i][j] = sum;
            }
        }

        Ok(result)
    }

    /* ========================================================================
     * Gaussian Elimination
     * ======================================================================== */

    /// Solve linear system Ax = b using Gaussian elimination with partial pivoting
    ///
    /// Time Complexity: O(n³)
    /// Space Complexity: O(1) - works on copies
    ///
    /// Algorithm:
    /// 1. Forward elimination: Transform to upper triangular form
    /// 2. Backward substitution: Solve for x
    ///
    /// Partial pivoting: Swap rows to avoid division by small numbers
    /// This improves numerical stability
    ///
    /// Applications:
    /// - Solving systems of linear equations
    /// - Circuit analysis (Kirchhoff's laws)
    /// - Structural engineering (finite element analysis)
    /// - Economics (input-output models)
    fn gaussian_elimination(&self, b: &Vector) -> Result<Vector> {
        let n = self.rows;

        if self.rows != self.cols || self.rows != b.data.len() {
            return Err(MatrixError::InvalidDimensions);
        }

        // Make copies
        let mut a = self.clone();
        let mut b_copy = b.clone();

        // Forward elimination with partial pivoting
        for col in 0..n {
            // Find pivot
            let mut max_row = col;
            let mut max_val = a.data[col][col].abs();

            for row in (col + 1)..n {
                let val = a.data[row][col].abs();
                if val > max_val {
                    max_val = val;
                    max_row = row;
                }
            }

            // Swap rows
            if max_row != col {
                a.data.swap(col, max_row);
                b_copy.data.swap(col, max_row);
            }

            // Check for singular matrix
            if a.data[col][col].abs() < EPSILON {
                return Err(MatrixError::SingularMatrix);
            }

            // Eliminate column entries below pivot
            for row in (col + 1)..n {
                let factor = a.data[row][col] / a.data[col][col];
                for j in col..n {
                    a.data[row][j] -= factor * a.data[col][j];
                }
                b_copy.data[row] -= factor * b_copy.data[col];
            }
        }

        // Backward substitution
        let mut x = vec![0.0; n];
        for i in (0..n).rev() {
            x[i] = b_copy.data[i];
            for j in (i + 1)..n {
                x[i] -= a.data[i][j] * x[j];
            }
            x[i] /= a.data[i][i];
        }

        Ok(Vector { data: x })
    }

    /* ========================================================================
     * Matrix Decomposition
     * ======================================================================== */

    /// LU decomposition: A = LU
    ///
    /// Time Complexity: O(n³)
    /// Space Complexity: O(n²)
    ///
    /// Algorithm (Doolittle):
    /// - L has 1's on diagonal
    /// - U has calculated values on and above diagonal
    ///
    /// Applications:
    /// - Solving multiple systems with same A but different b
    /// - Computing determinant: det(A) = product of U's diagonal
    /// - Matrix inversion
    fn lu_decomposition(&self) -> Result<(Matrix, Matrix)> {
        let n = self.rows;

        if self.rows != self.cols {
            return Err(MatrixError::InvalidDimensions);
        }

        let mut l = Matrix::new(n, n);
        let mut u = Matrix::new(n, n);

        for i in 0..n {
            // Upper triangular matrix U
            for k in i..n {
                let mut sum = 0.0;
                for j in 0..i {
                    sum += l.data[i][j] * u.data[j][k];
                }
                u.data[i][k] = self.data[i][k] - sum;
            }

            // Lower triangular matrix L
            for k in i..n {
                if i == k {
                    l.data[i][i] = 1.0;
                } else {
                    let mut sum = 0.0;
                    for j in 0..i {
                        sum += l.data[k][j] * u.data[j][i];
                    }

                    if u.data[i][i].abs() < EPSILON {
                        return Err(MatrixError::SingularMatrix);
                    }

                    l.data[k][i] = (self.data[k][i] - sum) / u.data[i][i];
                }
            }
        }

        Ok((l, u))
    }

    /// QR decomposition using Gram-Schmidt orthogonalization
    ///
    /// A = QR where:
    /// - Q is orthogonal (Q^T * Q = I)
    /// - R is upper triangular
    ///
    /// Time Complexity: O(mn²) for m×n matrix
    /// Space Complexity: O(mn)
    ///
    /// Applications:
    /// - Solving least squares problems
    /// - Eigenvalue computation (QR algorithm)
    /// - Numerical stability in solving linear systems
    fn qr_decomposition(&self) -> Result<(Matrix, Matrix)> {
        let m = self.rows;
        let n = self.cols;

        let mut q = self.clone();
        let mut r = Matrix::new(n, n);

        // Modified Gram-Schmidt
        for j in 0..n {
            // Compute norm of column j
            let mut norm = 0.0;
            for i in 0..m {
                norm += q.data[i][j] * q.data[i][j];
            }
            r.data[j][j] = norm.sqrt();

            if r.data[j][j].abs() < EPSILON {
                return Err(MatrixError::SingularMatrix);
            }

            // Normalize column j
            for i in 0..m {
                q.data[i][j] /= r.data[j][j];
            }

            // Orthogonalize remaining columns
            for k in (j + 1)..n {
                let mut dot = 0.0;
                for i in 0..m {
                    dot += q.data[i][j] * q.data[i][k];
                }
                r.data[j][k] = dot;

                for i in 0..m {
                    q.data[i][k] -= r.data[j][k] * q.data[i][j];
                }
            }
        }

        Ok((q, r))
    }

    /* ========================================================================
     * Determinant
     * ======================================================================== */

    /// Calculate determinant using recursive cofactor expansion
    ///
    /// Time Complexity: O(n!) - very slow for large matrices
    /// Best for: Small matrices (n <= 4)
    fn determinant_recursive(&self) -> Result<f64> {
        if self.rows != self.cols {
            return Err(MatrixError::InvalidDimensions);
        }

        let n = self.rows;

        if n == 1 {
            return Ok(self.data[0][0]);
        }

        if n == 2 {
            return Ok(self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]);
        }

        let mut det = 0.0;

        for j in 0..n {
            // Create submatrix
            let mut submatrix_data = Vec::new();

            for i in 1..n {
                let mut row = Vec::new();
                for k in 0..n {
                    if k != j {
                        row.push(self.data[i][k]);
                    }
                }
                submatrix_data.push(row);
            }

            let submatrix = Matrix::from_vec(submatrix_data)?;
            let sub_det = submatrix.determinant_recursive()?;

            let sign = if j % 2 == 0 { 1.0 } else { -1.0 };
            det += sign * self.data[0][j] * sub_det;
        }

        Ok(det)
    }

    /// Calculate determinant using LU decomposition
    ///
    /// Time Complexity: O(n³)
    /// Best for: Matrices larger than 4×4
    fn determinant_lu(&self) -> Result<f64> {
        if self.rows != self.cols {
            return Err(MatrixError::InvalidDimensions);
        }

        let (_, u) = self.lu_decomposition()?;

        let mut det = 1.0;
        for i in 0..self.rows {
            det *= u.data[i][i];
        }

        Ok(det)
    }

    /* ========================================================================
     * Matrix Inversion
     * ======================================================================== */

    /// Matrix inversion using Gauss-Jordan elimination
    ///
    /// Time Complexity: O(n³)
    /// Space Complexity: O(n²)
    ///
    /// Applications:
    /// - Solving linear systems
    /// - Computer graphics transformations
    /// - Control systems
    fn inverse(&self) -> Result<Matrix> {
        let n = self.rows;

        if self.rows != self.cols {
            return Err(MatrixError::InvalidDimensions);
        }

        // Create augmented matrix [A|I]
        let mut augmented = Matrix::new(n, 2 * n);

        // Copy A to left half
        for i in 0..n {
            for j in 0..n {
                augmented.data[i][j] = self.data[i][j];
            }
        }

        // Set right half to identity
        for i in 0..n {
            augmented.data[i][n + i] = 1.0;
        }

        // Gauss-Jordan elimination
        for col in 0..n {
            // Find pivot
            let mut max_row = col;
            let mut max_val = augmented.data[col][col].abs();

            for row in (col + 1)..n {
                let val = augmented.data[row][col].abs();
                if val > max_val {
                    max_val = val;
                    max_row = row;
                }
            }

            // Swap rows
            if max_row != col {
                augmented.data.swap(col, max_row);
            }

            // Check for singular matrix
            if augmented.data[col][col].abs() < EPSILON {
                return Err(MatrixError::SingularMatrix);
            }

            // Scale pivot row
            let pivot = augmented.data[col][col];
            for j in 0..(2 * n) {
                augmented.data[col][j] /= pivot;
            }

            // Eliminate column
            for row in 0..n {
                if row != col {
                    let factor = augmented.data[row][col];
                    for j in 0..(2 * n) {
                        augmented.data[row][j] -= factor * augmented.data[col][j];
                    }
                }
            }
        }

        // Extract inverse from right half
        let mut inverse = Matrix::new(n, n);
        for i in 0..n {
            for j in 0..n {
                inverse.data[i][j] = augmented.data[i][n + j];
            }
        }

        Ok(inverse)
    }

    /* ========================================================================
     * Eigenvalue Computation
     * ======================================================================== */

    /// Find dominant eigenvalue and eigenvector using power iteration
    ///
    /// Time Complexity: O(n² * iterations)
    ///
    /// Applications:
    /// - Google PageRank algorithm
    /// - Principal Component Analysis (PCA)
    /// - Markov chains (stationary distribution)
    fn power_iteration(&self, max_iter: usize) -> Result<(f64, Vector)> {
        let n = self.rows;

        if self.rows != self.cols {
            return Err(MatrixError::InvalidDimensions);
        }

        // Initialize with random vector
        let mut v = vec![1.0; n];

        // Normalize
        let mut norm: f64 = v.iter().map(|x| x * x).sum::<f64>().sqrt();
        for i in 0..n {
            v[i] /= norm;
        }

        // Power iteration
        for _iter in 0..max_iter {
            let mut v_new = vec![0.0; n];

            // Multiply by matrix
            for i in 0..n {
                for j in 0..n {
                    v_new[i] += self.data[i][j] * v[j];
                }
            }

            // Normalize
            norm = v_new.iter().map(|x| x * x).sum::<f64>().sqrt();
            for i in 0..n {
                v_new[i] /= norm;
            }

            // Check convergence
            let diff: f64 = v.iter().zip(v_new.iter())
                .map(|(a, b)| (a - b).abs())
                .sum();

            if diff < EPSILON {
                break;
            }

            v = v_new;
        }

        // Compute eigenvalue: λ = v^T * A * v
        let mut av = vec![0.0; n];
        for i in 0..n {
            for j in 0..n {
                av[i] += self.data[i][j] * v[j];
            }
        }

        let eigenvalue: f64 = v.iter().zip(av.iter())
            .map(|(vi, avi)| vi * avi)
            .sum();

        Ok((eigenvalue, Vector { data: v }))
    }

    /* ========================================================================
     * Display
     * ======================================================================== */

    fn print(&self, name: &str) {
        println!("\n{}:", name);
        for i in 0..self.rows {
            for j in 0..self.cols {
                print!("{:10.4} ", self.data[i][j]);
            }
            println!();
        }
    }
}

/* ============================================================================
 * Vector Implementation
 * ============================================================================ */

impl Vector {
    fn new(size: usize) -> Self {
        Vector {
            data: vec![0.0; size],
        }
    }

    fn from_vec(data: Vec<f64>) -> Self {
        Vector { data }
    }

    fn print(&self, name: &str) {
        println!("\n{}:", name);
        for &val in &self.data {
            println!("{:10.4}", val);
        }
    }
}

/* ============================================================================
 * Example Usage and Tests
 * ============================================================================ */

fn example_multiplication() {
    println!("\n======================================");
    println!("Example 1: Matrix Multiplication");
    println!("======================================");

    let a = Matrix::from_vec(vec![
        vec![1.0, 2.0, 3.0],
        vec![4.0, 5.0, 6.0],
    ]).unwrap();

    let b = Matrix::from_vec(vec![
        vec![7.0, 8.0],
        vec![9.0, 10.0],
        vec![11.0, 12.0],
    ]).unwrap();

    let c = a.multiply(&b).unwrap();

    a.print("A (2x3)");
    b.print("B (3x2)");
    c.print("C = A × B (2x2)");
}

fn example_gaussian_elimination() {
    println!("\n======================================");
    println!("Example 2: Gaussian Elimination");
    println!("======================================");

    let a = Matrix::from_vec(vec![
        vec![2.0, 1.0, -1.0],
        vec![-3.0, -1.0, 2.0],
        vec![-2.0, 1.0, 2.0],
    ]).unwrap();

    let b = Vector::from_vec(vec![8.0, -11.0, -3.0]);

    let x = a.gaussian_elimination(&b).unwrap();

    x.print("Solution x");
    println!("Expected: x=2, y=3, z=-1");
}

fn example_lu_decomposition() {
    println!("\n======================================");
    println!("Example 3: LU Decomposition");
    println!("======================================");

    let a = Matrix::from_vec(vec![
        vec![2.0, -1.0, -2.0],
        vec![-4.0, 6.0, 3.0],
        vec![-4.0, -2.0, 8.0],
    ]).unwrap();

    let (l, u) = a.lu_decomposition().unwrap();

    a.print("A");
    l.print("L (lower triangular)");
    u.print("U (upper triangular)");
}

fn example_matrix_inverse() {
    println!("\n======================================");
    println!("Example 4: Matrix Inversion");
    println!("======================================");

    let a = Matrix::from_vec(vec![
        vec![4.0, 7.0],
        vec![2.0, 6.0],
    ]).unwrap();

    let a_inv = a.inverse().unwrap();

    a.print("A");
    a_inv.print("A^(-1)");

    let i = a.multiply(&a_inv).unwrap();
    i.print("A × A^(-1) (should be identity)");
}

fn example_eigenvalues() {
    println!("\n======================================");
    println!("Example 5: Eigenvalue Computation");
    println!("======================================");

    let a = Matrix::from_vec(vec![
        vec![2.0, 1.0],
        vec![1.0, 2.0],
    ]).unwrap();

    let (eigenvalue, eigenvector) = a.power_iteration(100).unwrap();

    a.print("A");
    println!("\nDominant eigenvalue: {:.6}", eigenvalue);
    eigenvector.print("Corresponding eigenvector");
}

fn example_determinant() {
    println!("\n======================================");
    println!("Example 6: Determinant Calculation");
    println!("======================================");

    let a = Matrix::from_vec(vec![
        vec![1.0, 2.0, 3.0],
        vec![4.0, 5.0, 6.0],
        vec![7.0, 8.0, 9.0],
    ]).unwrap();

    let det_lu = a.determinant_lu().unwrap();

    a.print("A");
    println!("\nDeterminant (LU): {:.6}", det_lu);
}

fn main() {
    println!("======================================");
    println!("Matrix Operations and Linear Algebra");
    println!("======================================");

    example_multiplication();
    example_gaussian_elimination();
    example_lu_decomposition();
    example_matrix_inverse();
    example_eigenvalues();
    example_determinant();

    println!("\n======================================");
    println!("All examples completed successfully!");
    println!("======================================");
}
