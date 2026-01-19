/**
 * @file matrix.h
 * @brief Matrix operations interface
 */

#ifndef AM_MATRIX_H
#define AM_MATRIX_H

#include <stddef.h>
#include <stdbool.h>
#include <complex.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Matrix structure */
typedef struct {
    double* data;
    size_t rows;
    size_t cols;
} matrix_t;

typedef struct {
    double complex* data;
    size_t rows;
    size_t cols;
} complex_matrix_t;

/* Sparse matrix structures */
typedef struct {
    double* values;
    size_t* row_indices;
    size_t* col_indices;
    size_t nnz;  /* number of non-zero elements */
    size_t rows;
    size_t cols;
} sparse_matrix_coo_t;

typedef struct {
    double* values;
    size_t* col_indices;
    size_t* row_ptr;
    size_t nnz;
    size_t rows;
    size_t cols;
} sparse_matrix_csr_t;

/* Matrix creation and destruction */
matrix_t* matrix_create(size_t rows, size_t cols);
matrix_t* matrix_create_from_array(const double* data, size_t rows, size_t cols);
matrix_t* matrix_create_identity(size_t n);
matrix_t* matrix_create_zeros(size_t rows, size_t cols);
matrix_t* matrix_create_ones(size_t rows, size_t cols);
matrix_t* matrix_create_random(size_t rows, size_t cols, double min, double max);
matrix_t* matrix_copy(const matrix_t* mat);
void matrix_destroy(matrix_t* mat);

/* Basic matrix operations */
double matrix_get(const matrix_t* mat, size_t row, size_t col);
void matrix_set(matrix_t* mat, size_t row, size_t col, double value);
void matrix_fill(matrix_t* mat, double value);
void matrix_swap_rows(matrix_t* mat, size_t row1, size_t row2);
void matrix_swap_cols(matrix_t* mat, size_t col1, size_t col2);

/* Matrix arithmetic */
matrix_t* matrix_add(const matrix_t* a, const matrix_t* b);
matrix_t* matrix_subtract(const matrix_t* a, const matrix_t* b);
matrix_t* matrix_multiply(const matrix_t* a, const matrix_t* b);
matrix_t* matrix_multiply_scalar(const matrix_t* mat, double scalar);
matrix_t* matrix_divide_scalar(const matrix_t* mat, double scalar);
matrix_t* matrix_element_multiply(const matrix_t* a, const matrix_t* b);
matrix_t* matrix_element_divide(const matrix_t* a, const matrix_t* b);
matrix_t* matrix_power(const matrix_t* mat, int n);

/* Matrix transformations */
matrix_t* matrix_transpose(const matrix_t* mat);
matrix_t* matrix_reshape(const matrix_t* mat, size_t new_rows, size_t new_cols);
matrix_t* matrix_flatten(const matrix_t* mat);
matrix_t* matrix_slice(const matrix_t* mat, size_t row_start, size_t row_end,
                      size_t col_start, size_t col_end);
matrix_t* matrix_concatenate_horizontal(const matrix_t* a, const matrix_t* b);
matrix_t* matrix_concatenate_vertical(const matrix_t* a, const matrix_t* b);

/* Matrix properties */
double matrix_determinant(const matrix_t* mat);
double matrix_trace(const matrix_t* mat);
size_t matrix_rank(const matrix_t* mat);
double matrix_norm_frobenius(const matrix_t* mat);
double matrix_norm_1(const matrix_t* mat);
double matrix_norm_inf(const matrix_t* mat);
double matrix_condition_number(const matrix_t* mat);
bool matrix_is_symmetric(const matrix_t* mat);
bool matrix_is_diagonal(const matrix_t* mat);
bool matrix_is_upper_triangular(const matrix_t* mat);
bool matrix_is_lower_triangular(const matrix_t* mat);
bool matrix_is_orthogonal(const matrix_t* mat);
bool matrix_is_positive_definite(const matrix_t* mat);

/* Matrix decompositions */
bool matrix_lu_decomposition(const matrix_t* mat, matrix_t** L, matrix_t** U);
bool matrix_qr_decomposition(const matrix_t* mat, matrix_t** Q, matrix_t** R);
bool matrix_cholesky_decomposition(const matrix_t* mat, matrix_t** L);
bool matrix_svd(const matrix_t* mat, matrix_t** U, matrix_t** S, matrix_t** V);
bool matrix_eigenvalues(const matrix_t* mat, double complex* eigenvalues);
bool matrix_eigenvectors(const matrix_t* mat, matrix_t** eigenvectors,
                         double complex* eigenvalues);

/* Linear system solvers */
matrix_t* matrix_inverse(const matrix_t* mat);
matrix_t* matrix_pseudoinverse(const matrix_t* mat);
double* matrix_solve_linear_system(const matrix_t* A, const double* b);
double* matrix_solve_lu(const matrix_t* A, const double* b);
double* matrix_solve_qr(const matrix_t* A, const double* b);
double* matrix_solve_cholesky(const matrix_t* A, const double* b);
double* matrix_solve_gauss_elimination(const matrix_t* A, const double* b);
double* matrix_solve_gauss_seidel(const matrix_t* A, const double* b,
                                  int max_iter, double tolerance);
double* matrix_solve_jacobi(const matrix_t* A, const double* b,
                            int max_iter, double tolerance);

/* Vector operations */
double* vector_create(size_t n);
double* vector_create_from_array(const double* data, size_t n);
void vector_destroy(double* vec);
double vector_dot_product(const double* a, const double* b, size_t n);
double* vector_cross_product(const double* a, const double* b);
double vector_norm(const double* vec, size_t n);
double* vector_normalize(const double* vec, size_t n);
double* vector_add(const double* a, const double* b, size_t n);
double* vector_subtract(const double* a, const double* b, size_t n);
double* vector_multiply_scalar(const double* vec, size_t n, double scalar);

/* Special matrices */
matrix_t* matrix_hilbert(size_t n);
matrix_t* matrix_vandermonde(const double* x, size_t n, size_t m);
matrix_t* matrix_toeplitz(const double* c, const double* r, size_t n);
matrix_t* matrix_hankel(const double* c, const double* r, size_t n);
matrix_t* matrix_pascal(size_t n);

/* Sparse matrix operations */
sparse_matrix_csr_t* sparse_matrix_create_csr(size_t rows, size_t cols, size_t nnz);
void sparse_matrix_destroy_csr(sparse_matrix_csr_t* mat);
sparse_matrix_csr_t* sparse_from_dense(const matrix_t* mat);
matrix_t* sparse_to_dense(const sparse_matrix_csr_t* mat);
double* sparse_matrix_vector_multiply(const sparse_matrix_csr_t* mat,
                                      const double* vec);
sparse_matrix_csr_t* sparse_matrix_multiply(const sparse_matrix_csr_t* a,
                                            const sparse_matrix_csr_t* b);

/* Matrix utilities */
void matrix_print(const matrix_t* mat);
void matrix_save_to_file(const matrix_t* mat, const char* filename);
matrix_t* matrix_load_from_file(const char* filename);
bool matrix_equals(const matrix_t* a, const matrix_t* b, double tolerance);

#ifdef __cplusplus
}
#endif

#endif /* AM_MATRIX_H */