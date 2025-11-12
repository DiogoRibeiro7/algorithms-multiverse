/*
 * ============================================================================
 * Matrix Operations and Linear Algebra in Go
 *
 * Comprehensive collection of matrix operations leveraging Go's concurrency
 * features with goroutines and channels for efficient parallel computation.
 *
 * Features:
 * - Idiomatic Go with clear interfaces
 * - Concurrent operations using goroutines
 * - Efficient memory management
 * - Numerical stability with pivoting
 * - Educational implementations
 *
 * Run: go run matrix.go
 *
 * @author Algorithms Multiverse
 * @version 1.0
 * ============================================================================
 */

package main

import (
	"fmt"
	"math"
	"math/rand"
	"sync"
	"time"
)

const (
	// EPSILON is the tolerance for floating-point comparisons
	EPSILON = 1e-10
)

// ============================================================================
// Data Structures
// ============================================================================

// Matrix represents a 2D matrix with row-major storage
type Matrix struct {
	data [][]float64
	rows int
	cols int
}

// Vector represents a 1D vector
type Vector struct {
	data []float64
	size int
}

// SparseElement represents a non-zero element in a sparse matrix
type SparseElement struct {
	row, col int
	value    float64
}

// SparseMatrix represents a sparse matrix using map (similar to DOK format)
type SparseMatrix struct {
	data map[[2]int]float64
	rows int
	cols int
}

// ============================================================================
// Matrix Creation and Utilities
// ============================================================================

// NewMatrix creates a new matrix with given dimensions
// Time Complexity: O(rows * cols)
func NewMatrix(rows, cols int) *Matrix {
	data := make([][]float64, rows)
	for i := range data {
		data[i] = make([]float64, cols)
	}
	return &Matrix{
		data: data,
		rows: rows,
		cols: cols,
	}
}

// NewVector creates a new vector with given size
func NewVector(size int) *Vector {
	return &Vector{
		data: make([]float64, size),
		size: size,
	}
}

// NewIdentityMatrix creates an n×n identity matrix
// Time Complexity: O(n²)
func NewIdentityMatrix(n int) *Matrix {
	m := NewMatrix(n, n)
	for i := 0; i < n; i++ {
		m.data[i][i] = 1.0
	}
	return m
}

// Clone creates a deep copy of the matrix
func (m *Matrix) Clone() *Matrix {
	clone := NewMatrix(m.rows, m.cols)
	for i := 0; i < m.rows; i++ {
		copy(clone.data[i], m.data[i])
	}
	return clone
}

// ============================================================================
// Basic Matrix Operations
// ============================================================================

// Add performs matrix addition: C = A + B
//
// Time Complexity: O(rows * cols)
//
// Applications:
// - Computer graphics transformations
// - Neural network weight updates
// - Image processing
func (m *Matrix) Add(other *Matrix) (*Matrix, error) {
	if m.rows != other.rows || m.cols != other.cols {
		return nil, fmt.Errorf("matrix dimensions must match for addition: %dx%d vs %dx%d",
			m.rows, m.cols, other.rows, other.cols)
	}

	result := NewMatrix(m.rows, m.cols)
	for i := 0; i < m.rows; i++ {
		for j := 0; j < m.cols; j++ {
			result.data[i][j] = m.data[i][j] + other.data[i][j]
		}
	}

	return result, nil
}

// Subtract performs matrix subtraction: C = A - B
// Time Complexity: O(rows * cols)
func (m *Matrix) Subtract(other *Matrix) (*Matrix, error) {
	if m.rows != other.rows || m.cols != other.cols {
		return nil, fmt.Errorf("matrix dimensions must match for subtraction")
	}

	result := NewMatrix(m.rows, m.cols)
	for i := 0; i < m.rows; i++ {
		for j := 0; j < m.cols; j++ {
			result.data[i][j] = m.data[i][j] - other.data[i][j]
		}
	}

	return result, nil
}

// ScalarMultiply multiplies matrix by a scalar
// Time Complexity: O(rows * cols)
func (m *Matrix) ScalarMultiply(scalar float64) *Matrix {
	result := NewMatrix(m.rows, m.cols)
	for i := 0; i < m.rows; i++ {
		for j := 0; j < m.cols; j++ {
			result.data[i][j] = m.data[i][j] * scalar
		}
	}
	return result
}

// Transpose returns the transpose of the matrix
//
// Time Complexity: O(rows * cols)
//
// Applications:
// - Solving linear systems
// - Covariance matrix computation
// - Neural network backpropagation
func (m *Matrix) Transpose() *Matrix {
	result := NewMatrix(m.cols, m.rows)
	for i := 0; i < m.rows; i++ {
		for j := 0; j < m.cols; j++ {
			result.data[j][i] = m.data[i][j]
		}
	}
	return result
}

// ============================================================================
// Matrix Multiplication
// ============================================================================

// Multiply performs standard matrix multiplication
//
// Time Complexity: O(n³) for n×n matrices
// Space Complexity: O(n²)
//
// Algorithm:
// C[i][j] = Σ(A[i][k] * B[k][j]) for k from 0 to n-1
//
// Applications:
// - Linear transformations
// - Graph algorithms (adjacency matrices)
// - Computer graphics transformations
// - Neural network forward propagation
func (m *Matrix) Multiply(other *Matrix) (*Matrix, error) {
	if m.cols != other.rows {
		return nil, fmt.Errorf("cannot multiply %dx%d and %dx%d matrices",
			m.rows, m.cols, other.rows, other.cols)
	}

	result := NewMatrix(m.rows, other.cols)

	for i := 0; i < m.rows; i++ {
		for j := 0; j < other.cols; j++ {
			sum := 0.0
			for k := 0; k < m.cols; k++ {
				sum += m.data[i][k] * other.data[k][j]
			}
			result.data[i][j] = sum
		}
	}

	return result, nil
}

// MultiplyParallel performs parallel matrix multiplication using goroutines
//
// Time Complexity: O(n³/p) where p is number of goroutines
//
// Best for: Large matrices (> 100×100)
func (m *Matrix) MultiplyParallel(other *Matrix) (*Matrix, error) {
	if m.cols != other.rows {
		return nil, fmt.Errorf("cannot multiply %dx%d and %dx%d matrices",
			m.rows, m.cols, other.rows, other.cols)
	}

	result := NewMatrix(m.rows, other.cols)

	// Use goroutines to compute rows in parallel
	var wg sync.WaitGroup
	numWorkers := m.rows

	for i := 0; i < m.rows; i++ {
		wg.Add(1)
		go func(row int) {
			defer wg.Done()
			for j := 0; j < other.cols; j++ {
				sum := 0.0
				for k := 0; k < m.cols; k++ {
					sum += m.data[row][k] * other.data[k][j]
				}
				result.data[row][j] = sum
			}
		}(i)
	}

	wg.Wait()
	return result, nil
}

// ============================================================================
// Gaussian Elimination
// ============================================================================

// GaussianElimination solves the linear system Ax = b
//
// Time Complexity: O(n³)
// Space Complexity: O(1) - modifies A and b in place
//
// Algorithm:
// 1. Forward elimination: Transform to upper triangular form
// 2. Backward substitution: Solve for x
//
// Partial pivoting: Swap rows to avoid division by small numbers
// This improves numerical stability
//
// Applications:
// - Solving systems of linear equations
// - Circuit analysis (Kirchhoff's laws)
// - Structural engineering (finite element analysis)
// - Economics (input-output models)
func GaussianElimination(A *Matrix, b *Vector) (*Vector, error) {
	n := A.rows

	if A.rows != A.cols || A.rows != b.size {
		return nil, fmt.Errorf("invalid dimensions for Gaussian elimination")
	}

	// Make copies to avoid modifying originals
	ACopy := A.Clone()
	bCopy := &Vector{data: make([]float64, b.size), size: b.size}
	copy(bCopy.data, b.data)

	// Forward elimination with partial pivoting
	for col := 0; col < n; col++ {
		// Find pivot (largest absolute value in column)
		maxRow := col
		maxVal := math.Abs(ACopy.data[col][col])

		for row := col + 1; row < n; row++ {
			if val := math.Abs(ACopy.data[row][col]); val > maxVal {
				maxVal = val
				maxRow = row
			}
		}

		// Swap rows
		if maxRow != col {
			ACopy.data[col], ACopy.data[maxRow] = ACopy.data[maxRow], ACopy.data[col]
			bCopy.data[col], bCopy.data[maxRow] = bCopy.data[maxRow], bCopy.data[col]
		}

		// Check for singular matrix
		if math.Abs(ACopy.data[col][col]) < EPSILON {
			return nil, fmt.Errorf("matrix is singular or nearly singular")
		}

		// Eliminate column entries below pivot
		for row := col + 1; row < n; row++ {
			factor := ACopy.data[row][col] / ACopy.data[col][col]
			for j := col; j < n; j++ {
				ACopy.data[row][j] -= factor * ACopy.data[col][j]
			}
			bCopy.data[row] -= factor * bCopy.data[col]
		}
	}

	// Backward substitution
	x := NewVector(n)
	for i := n - 1; i >= 0; i-- {
		x.data[i] = bCopy.data[i]
		for j := i + 1; j < n; j++ {
			x.data[i] -= ACopy.data[i][j] * x.data[j]
		}
		x.data[i] /= ACopy.data[i][i]
	}

	return x, nil
}

// ============================================================================
// Matrix Decomposition
// ============================================================================

// LUDecomposition performs LU decomposition: A = LU
//
// Time Complexity: O(n³)
// Space Complexity: O(n²)
//
// Algorithm (Doolittle):
// - L has 1's on diagonal
// - U has calculated values on and above diagonal
//
// Applications:
// - Solving multiple systems with same A but different b
// - Computing determinant: det(A) = product of U's diagonal
// - Matrix inversion
func LUDecomposition(A *Matrix) (*Matrix, *Matrix, error) {
	n := A.rows

	if A.rows != A.cols {
		return nil, nil, fmt.Errorf("LU decomposition requires square matrix")
	}

	L := NewMatrix(n, n)
	U := NewMatrix(n, n)

	for i := 0; i < n; i++ {
		// Upper triangular matrix U
		for k := i; k < n; k++ {
			sum := 0.0
			for j := 0; j < i; j++ {
				sum += L.data[i][j] * U.data[j][k]
			}
			U.data[i][k] = A.data[i][k] - sum
		}

		// Lower triangular matrix L
		for k := i; k < n; k++ {
			if i == k {
				L.data[i][i] = 1.0
			} else {
				sum := 0.0
				for j := 0; j < i; j++ {
					sum += L.data[k][j] * U.data[j][i]
				}

				if math.Abs(U.data[i][i]) < EPSILON {
					return nil, nil, fmt.Errorf("matrix is singular")
				}

				L.data[k][i] = (A.data[k][i] - sum) / U.data[i][i]
			}
		}
	}

	return L, U, nil
}

// QRDecomposition performs QR decomposition using Gram-Schmidt
//
// A = QR where:
// - Q is orthogonal (Q^T * Q = I)
// - R is upper triangular
//
// Time Complexity: O(mn²) for m×n matrix
// Space Complexity: O(mn)
//
// Applications:
// - Solving least squares problems
// - Eigenvalue computation (QR algorithm)
// - Numerical stability in solving linear systems
func QRDecomposition(A *Matrix) (*Matrix, *Matrix, error) {
	m, n := A.rows, A.cols

	Q := A.Clone()
	R := NewMatrix(n, n)

	// Modified Gram-Schmidt
	for j := 0; j < n; j++ {
		// Compute norm of column j
		norm := 0.0
		for i := 0; i < m; i++ {
			norm += Q.data[i][j] * Q.data[i][j]
		}
		R.data[j][j] = math.Sqrt(norm)

		if math.Abs(R.data[j][j]) < EPSILON {
			return nil, nil, fmt.Errorf("matrix columns are linearly dependent")
		}

		// Normalize column j
		for i := 0; i < m; i++ {
			Q.data[i][j] /= R.data[j][j]
		}

		// Orthogonalize remaining columns
		for k := j + 1; k < n; k++ {
			dot := 0.0
			for i := 0; i < m; i++ {
				dot += Q.data[i][j] * Q.data[i][k]
			}
			R.data[j][k] = dot

			for i := 0; i < m; i++ {
				Q.data[i][k] -= R.data[j][k] * Q.data[i][j]
			}
		}
	}

	return Q, R, nil
}

// ============================================================================
// Determinant Calculation
// ============================================================================

// DeterminantRecursive calculates determinant using cofactor expansion
//
// Time Complexity: O(n!) - very slow for large matrices
// Best for: Small matrices (n <= 4)
func (m *Matrix) DeterminantRecursive() (float64, error) {
	if m.rows != m.cols {
		return 0, fmt.Errorf("determinant requires square matrix")
	}

	n := m.rows

	if n == 1 {
		return m.data[0][0], nil
	}

	if n == 2 {
		return m.data[0][0]*m.data[1][1] - m.data[0][1]*m.data[1][0], nil
	}

	det := 0.0

	for j := 0; j < n; j++ {
		// Create submatrix
		submatrix := NewMatrix(n-1, n-1)

		for i := 1; i < n; i++ {
			colIdx := 0
			for k := 0; k < n; k++ {
				if k != j {
					submatrix.data[i-1][colIdx] = m.data[i][k]
					colIdx++
				}
			}
		}

		subDet, _ := submatrix.DeterminantRecursive()
		sign := 1.0
		if j%2 == 1 {
			sign = -1.0
		}
		det += sign * m.data[0][j] * subDet
	}

	return det, nil
}

// DeterminantLU calculates determinant using LU decomposition
//
// Time Complexity: O(n³)
// Best for: Matrices larger than 4×4
func (m *Matrix) DeterminantLU() (float64, error) {
	if m.rows != m.cols {
		return 0, fmt.Errorf("determinant requires square matrix")
	}

	_, U, err := LUDecomposition(m)
	if err != nil {
		return 0, nil // Singular matrix
	}

	det := 1.0
	for i := 0; i < m.rows; i++ {
		det *= U.data[i][i]
	}

	return det, nil
}

// ============================================================================
// Matrix Inversion
// ============================================================================

// Inverse computes matrix inverse using Gauss-Jordan elimination
//
// Time Complexity: O(n³)
// Space Complexity: O(n²)
//
// Applications:
// - Solving linear systems
// - Computer graphics transformations
// - Control systems
func (m *Matrix) Inverse() (*Matrix, error) {
	n := m.rows

	if m.rows != m.cols {
		return nil, fmt.Errorf("matrix inversion requires square matrix")
	}

	// Create augmented matrix [A|I]
	augmented := NewMatrix(n, 2*n)

	// Copy A to left half
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			augmented.data[i][j] = m.data[i][j]
		}
	}

	// Set right half to identity
	for i := 0; i < n; i++ {
		augmented.data[i][n+i] = 1.0
	}

	// Gauss-Jordan elimination
	for col := 0; col < n; col++ {
		// Find pivot
		maxRow := col
		maxVal := math.Abs(augmented.data[col][col])

		for row := col + 1; row < n; row++ {
			if val := math.Abs(augmented.data[row][col]); val > maxVal {
				maxVal = val
				maxRow = row
			}
		}

		// Swap rows
		if maxRow != col {
			augmented.data[col], augmented.data[maxRow] = augmented.data[maxRow], augmented.data[col]
		}

		// Check for singular matrix
		if math.Abs(augmented.data[col][col]) < EPSILON {
			return nil, fmt.Errorf("matrix is singular and cannot be inverted")
		}

		// Scale pivot row
		pivot := augmented.data[col][col]
		for j := 0; j < 2*n; j++ {
			augmented.data[col][j] /= pivot
		}

		// Eliminate column
		for row := 0; row < n; row++ {
			if row != col {
				factor := augmented.data[row][col]
				for j := 0; j < 2*n; j++ {
					augmented.data[row][j] -= factor * augmented.data[col][j]
				}
			}
		}
	}

	// Extract inverse from right half
	inverse := NewMatrix(n, n)
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			inverse.data[i][j] = augmented.data[i][n+j]
		}
	}

	return inverse, nil
}

// ============================================================================
// Eigenvalue Computation
// ============================================================================

// PowerIteration finds dominant eigenvalue and eigenvector
//
// Time Complexity: O(n² * iterations)
//
// Applications:
// - Google PageRank algorithm
// - Principal Component Analysis (PCA)
// - Markov chains (stationary distribution)
func (m *Matrix) PowerIteration(maxIter int) (float64, *Vector, error) {
	n := m.rows

	if m.rows != m.cols {
		return 0, nil, fmt.Errorf("power iteration requires square matrix")
	}

	// Initialize with random vector
	rand.Seed(time.Now().UnixNano())
	v := NewVector(n)
	for i := 0; i < n; i++ {
		v.data[i] = rand.Float64()
	}

	// Normalize
	norm := 0.0
	for i := 0; i < n; i++ {
		norm += v.data[i] * v.data[i]
	}
	norm = math.Sqrt(norm)

	for i := 0; i < n; i++ {
		v.data[i] /= norm
	}

	// Power iteration
	for iter := 0; iter < maxIter; iter++ {
		vNew := NewVector(n)

		// Multiply by matrix
		for i := 0; i < n; i++ {
			for j := 0; j < n; j++ {
				vNew.data[i] += m.data[i][j] * v.data[j]
			}
		}

		// Normalize
		norm = 0.0
		for i := 0; i < n; i++ {
			norm += vNew.data[i] * vNew.data[i]
		}
		norm = math.Sqrt(norm)

		for i := 0; i < n; i++ {
			vNew.data[i] /= norm
		}

		// Check convergence
		diff := 0.0
		for i := 0; i < n; i++ {
			diff += math.Abs(vNew.data[i] - v.data[i])
		}

		if diff < EPSILON {
			break
		}

		v = vNew
	}

	// Compute eigenvalue: λ = v^T * A * v
	Av := NewVector(n)
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			Av.data[i] += m.data[i][j] * v.data[j]
		}
	}

	eigenvalue := 0.0
	for i := 0; i < n; i++ {
		eigenvalue += v.data[i] * Av.data[i]
	}

	return eigenvalue, v, nil
}

// ============================================================================
// Sparse Matrix Operations
// ============================================================================

// NewSparseMatrix creates a new sparse matrix
func NewSparseMatrix(rows, cols int) *SparseMatrix {
	return &SparseMatrix{
		data: make(map[[2]int]float64),
		rows: rows,
		cols: cols,
	}
}

// Set sets value at (row, col) in sparse matrix
func (sm *SparseMatrix) Set(row, col int, value float64) {
	if math.Abs(value) < EPSILON {
		delete(sm.data, [2]int{row, col})
	} else {
		sm.data[[2]int{row, col}] = value
	}
}

// Get gets value at (row, col) from sparse matrix
func (sm *SparseMatrix) Get(row, col int) float64 {
	return sm.data[[2]int{row, col}]
}

// NonZeroCount returns the number of non-zero elements
func (sm *SparseMatrix) NonZeroCount() int {
	return len(sm.data)
}

// Sparsity returns the percentage of zero elements
func (sm *SparseMatrix) Sparsity() float64 {
	total := sm.rows * sm.cols
	return 1.0 - float64(len(sm.data))/float64(total)
}

// ============================================================================
// Utility Functions
// ============================================================================

// Print prints the matrix with formatting
func (m *Matrix) Print(name string) {
	fmt.Printf("\n%s:\n", name)
	for i := 0; i < m.rows; i++ {
		for j := 0; j < m.cols; j++ {
			fmt.Printf("%10.4f ", m.data[i][j])
		}
		fmt.Println()
	}
}

// PrintVector prints the vector with formatting
func (v *Vector) Print(name string) {
	fmt.Printf("\n%s:\n", name)
	for i := 0; i < v.size; i++ {
		fmt.Printf("%10.4f\n", v.data[i])
	}
}

// ============================================================================
// Example Usage and Tests
// ============================================================================

func exampleMultiplication() {
	fmt.Println("\n======================================")
	fmt.Println("Example 1: Matrix Multiplication")
	fmt.Println("======================================")

	A := NewMatrix(2, 3)
	A.data[0] = []float64{1, 2, 3}
	A.data[1] = []float64{4, 5, 6}

	B := NewMatrix(3, 2)
	B.data[0] = []float64{7, 8}
	B.data[1] = []float64{9, 10}
	B.data[2] = []float64{11, 12}

	C, _ := A.Multiply(B)

	A.Print("A (2x3)")
	B.Print("B (3x2)")
	C.Print("C = A × B (2x2)")
}

func exampleGaussianElimination() {
	fmt.Println("\n======================================")
	fmt.Println("Example 2: Gaussian Elimination")
	fmt.Println("======================================")

	A := NewMatrix(3, 3)
	A.data[0] = []float64{2, 1, -1}
	A.data[1] = []float64{-3, -1, 2}
	A.data[2] = []float64{-2, 1, 2}

	b := NewVector(3)
	b.data = []float64{8, -11, -3}

	x, _ := GaussianElimination(A, b)

	x.Print("Solution x")
	fmt.Println("Expected: x=2, y=3, z=-1")
}

func exampleLUDecomposition() {
	fmt.Println("\n======================================")
	fmt.Println("Example 3: LU Decomposition")
	fmt.Println("======================================")

	A := NewMatrix(3, 3)
	A.data[0] = []float64{2, -1, -2}
	A.data[1] = []float64{-4, 6, 3}
	A.data[2] = []float64{-4, -2, 8}

	L, U, _ := LUDecomposition(A)

	A.Print("A")
	L.Print("L (lower triangular)")
	U.Print("U (upper triangular)")
}

func exampleMatrixInverse() {
	fmt.Println("\n======================================")
	fmt.Println("Example 4: Matrix Inversion")
	fmt.Println("======================================")

	A := NewMatrix(2, 2)
	A.data[0] = []float64{4, 7}
	A.data[1] = []float64{2, 6}

	AInv, _ := A.Inverse()

	A.Print("A")
	AInv.Print("A^(-1)")

	I, _ := A.Multiply(AInv)
	I.Print("A × A^(-1) (should be identity)")
}

func exampleEigenvalues() {
	fmt.Println("\n======================================")
	fmt.Println("Example 5: Eigenvalue Computation")
	fmt.Println("======================================")

	A := NewMatrix(2, 2)
	A.data[0] = []float64{2, 1}
	A.data[1] = []float64{1, 2}

	eigenvalue, eigenvector, _ := A.PowerIteration(100)

	A.Print("A")
	fmt.Printf("\nDominant eigenvalue: %.6f\n", eigenvalue)
	eigenvector.Print("Corresponding eigenvector")
}

func exampleDeterminant() {
	fmt.Println("\n======================================")
	fmt.Println("Example 6: Determinant Calculation")
	fmt.Println("======================================")

	A := NewMatrix(3, 3)
	A.data[0] = []float64{1, 2, 3}
	A.data[1] = []float64{4, 5, 6}
	A.data[2] = []float64{7, 8, 9}

	detLU, _ := A.DeterminantLU()

	A.Print("A")
	fmt.Printf("\nDeterminant (LU): %.6f\n", detLU)
}

func main() {
	fmt.Println("======================================")
	fmt.Println("Matrix Operations and Linear Algebra")
	fmt.Println("======================================")

	exampleMultiplication()
	exampleGaussianElimination()
	exampleLUDecomposition()
	exampleMatrixInverse()
	exampleEigenvalues()
	exampleDeterminant()

	fmt.Println("\n======================================")
	fmt.Println("All examples completed successfully!")
	fmt.Println("======================================")
}
