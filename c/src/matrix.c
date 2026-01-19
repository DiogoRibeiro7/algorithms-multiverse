/**
 * @file matrix.c
 * @brief Implementation of matrix operations
 */

#include "matrix.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <float.h>

#define EPSILON 1e-10
#define MIN(a,b) ((a) < (b) ? (a) : (b))
#define MAX(a,b) ((a) > (b) ? (a) : (b))
#define ABS(x) ((x) < 0 ? -(x) : (x))

/* =========================== */
/*  Matrix Creation/Destroy    */
/* =========================== */

matrix_t* matrix_create(size_t rows, size_t cols) {
    if (rows == 0 || cols == 0) return NULL;

    matrix_t* mat = malloc(sizeof(matrix_t));
    if (!mat) return NULL;

    mat->rows = rows;
    mat->cols = cols;
    mat->data = calloc(rows * cols, sizeof(double));

    if (!mat->data) {
        free(mat);
        return NULL;
    }

    return mat;
}

matrix_t* matrix_create_from_array(const double* data, size_t rows, size_t cols) {
    if (!data || rows == 0 || cols == 0) return NULL;

    matrix_t* mat = matrix_create(rows, cols);
    if (!mat) return NULL;

    memcpy(mat->data, data, rows * cols * sizeof(double));
    return mat;
}

matrix_t* matrix_create_identity(size_t n) {
    matrix_t* mat = matrix_create(n, n);
    if (!mat) return NULL;

    for (size_t i = 0; i < n; i++) {
        mat->data[i * n + i] = 1.0;
    }

    return mat;
}

matrix_t* matrix_create_zeros(size_t rows, size_t cols) {
    return matrix_create(rows, cols);  /* Already zero-initialized by calloc */
}

matrix_t* matrix_create_ones(size_t rows, size_t cols) {
    matrix_t* mat = matrix_create(rows, cols);
    if (!mat) return NULL;

    for (size_t i = 0; i < rows * cols; i++) {
        mat->data[i] = 1.0;
    }

    return mat;
}

matrix_t* matrix_create_random(size_t rows, size_t cols, double min, double max) {
    matrix_t* mat = matrix_create(rows, cols);
    if (!mat) return NULL;

    double range = max - min;
    for (size_t i = 0; i < rows * cols; i++) {
        mat->data[i] = min + ((double)rand() / RAND_MAX) * range;
    }

    return mat;
}

matrix_t* matrix_copy(const matrix_t* mat) {
    if (!mat) return NULL;
    return matrix_create_from_array(mat->data, mat->rows, mat->cols);
}

void matrix_destroy(matrix_t* mat) {
    if (mat) {
        free(mat->data);
        free(mat);
    }
}

/* =========================== */
/*   Basic Matrix Operations   */
/* =========================== */

double matrix_get(const matrix_t* mat, size_t row, size_t col) {
    if (!mat || row >= mat->rows || col >= mat->cols) return NAN;
    return mat->data[row * mat->cols + col];
}

void matrix_set(matrix_t* mat, size_t row, size_t col, double value) {
    if (!mat || row >= mat->rows || col >= mat->cols) return;
    mat->data[row * mat->cols + col] = value;
}

void matrix_fill(matrix_t* mat, double value) {
    if (!mat) return;
    for (size_t i = 0; i < mat->rows * mat->cols; i++) {
        mat->data[i] = value;
    }
}

void matrix_swap_rows(matrix_t* mat, size_t row1, size_t row2) {
    if (!mat || row1 >= mat->rows || row2 >= mat->rows) return;

    size_t cols = mat->cols;
    for (size_t j = 0; j < cols; j++) {
        double temp = mat->data[row1 * cols + j];
        mat->data[row1 * cols + j] = mat->data[row2 * cols + j];
        mat->data[row2 * cols + j] = temp;
    }
}

void matrix_swap_cols(matrix_t* mat, size_t col1, size_t col2) {
    if (!mat || col1 >= mat->cols || col2 >= mat->cols) return;

    size_t cols = mat->cols;
    for (size_t i = 0; i < mat->rows; i++) {
        double temp = mat->data[i * cols + col1];
        mat->data[i * cols + col1] = mat->data[i * cols + col2];
        mat->data[i * cols + col2] = temp;
    }
}

/* =========================== */
/*     Matrix Arithmetic       */
/* =========================== */

matrix_t* matrix_add(const matrix_t* a, const matrix_t* b) {
    if (!a || !b || a->rows != b->rows || a->cols != b->cols) return NULL;

    matrix_t* result = matrix_create(a->rows, a->cols);
    if (!result) return NULL;

    size_t n = a->rows * a->cols;
    for (size_t i = 0; i < n; i++) {
        result->data[i] = a->data[i] + b->data[i];
    }

    return result;
}

matrix_t* matrix_subtract(const matrix_t* a, const matrix_t* b) {
    if (!a || !b || a->rows != b->rows || a->cols != b->cols) return NULL;

    matrix_t* result = matrix_create(a->rows, a->cols);
    if (!result) return NULL;

    size_t n = a->rows * a->cols;
    for (size_t i = 0; i < n; i++) {
        result->data[i] = a->data[i] - b->data[i];
    }

    return result;
}

matrix_t* matrix_multiply(const matrix_t* a, const matrix_t* b) {
    if (!a || !b || a->cols != b->rows) return NULL;

    matrix_t* result = matrix_create(a->rows, b->cols);
    if (!result) return NULL;

    for (size_t i = 0; i < a->rows; i++) {
        for (size_t j = 0; j < b->cols; j++) {
            double sum = 0.0;
            for (size_t k = 0; k < a->cols; k++) {
                sum += a->data[i * a->cols + k] * b->data[k * b->cols + j];
            }
            result->data[i * b->cols + j] = sum;
        }
    }

    return result;
}

matrix_t* matrix_multiply_scalar(const matrix_t* mat, double scalar) {
    if (!mat) return NULL;

    matrix_t* result = matrix_create(mat->rows, mat->cols);
    if (!result) return NULL;

    size_t n = mat->rows * mat->cols;
    for (size_t i = 0; i < n; i++) {
        result->data[i] = mat->data[i] * scalar;
    }

    return result;
}

matrix_t* matrix_divide_scalar(const matrix_t* mat, double scalar) {
    if (!mat || scalar == 0.0) return NULL;
    return matrix_multiply_scalar(mat, 1.0 / scalar);
}

matrix_t* matrix_element_multiply(const matrix_t* a, const matrix_t* b) {
    if (!a || !b || a->rows != b->rows || a->cols != b->cols) return NULL;

    matrix_t* result = matrix_create(a->rows, a->cols);
    if (!result) return NULL;

    size_t n = a->rows * a->cols;
    for (size_t i = 0; i < n; i++) {
        result->data[i] = a->data[i] * b->data[i];
    }

    return result;
}

matrix_t* matrix_element_divide(const matrix_t* a, const matrix_t* b) {
    if (!a || !b || a->rows != b->rows || a->cols != b->cols) return NULL;

    matrix_t* result = matrix_create(a->rows, a->cols);
    if (!result) return NULL;

    size_t n = a->rows * a->cols;
    for (size_t i = 0; i < n; i++) {
        if (b->data[i] == 0.0) {
            result->data[i] = (a->data[i] >= 0) ? INFINITY : -INFINITY;
        } else {
            result->data[i] = a->data[i] / b->data[i];
        }
    }

    return result;
}

matrix_t* matrix_power(const matrix_t* mat, int n) {
    if (!mat || mat->rows != mat->cols) return NULL;

    if (n == 0) {
        return matrix_create_identity(mat->rows);
    }

    if (n == 1) {
        return matrix_copy(mat);
    }

    if (n < 0) {
        matrix_t* inv = matrix_inverse(mat);
        if (!inv) return NULL;
        matrix_t* result = matrix_power(inv, -n);
        matrix_destroy(inv);
        return result;
    }

    /* Positive power - use repeated squaring */
    matrix_t* result = matrix_create_identity(mat->rows);
    matrix_t* base = matrix_copy(mat);

    while (n > 0) {
        if (n % 2 == 1) {
            matrix_t* temp = matrix_multiply(result, base);
            matrix_destroy(result);
            result = temp;
        }
        matrix_t* temp = matrix_multiply(base, base);
        matrix_destroy(base);
        base = temp;
        n /= 2;
    }

    matrix_destroy(base);
    return result;
}

/* =========================== */
/*   Matrix Transformations    */
/* =========================== */

matrix_t* matrix_transpose(const matrix_t* mat) {
    if (!mat) return NULL;

    matrix_t* result = matrix_create(mat->cols, mat->rows);
    if (!result) return NULL;

    for (size_t i = 0; i < mat->rows; i++) {
        for (size_t j = 0; j < mat->cols; j++) {
            result->data[j * mat->rows + i] = mat->data[i * mat->cols + j];
        }
    }

    return result;
}

matrix_t* matrix_reshape(const matrix_t* mat, size_t new_rows, size_t new_cols) {
    if (!mat || new_rows * new_cols != mat->rows * mat->cols) return NULL;

    matrix_t* result = matrix_create(new_rows, new_cols);
    if (!result) return NULL;

    memcpy(result->data, mat->data, mat->rows * mat->cols * sizeof(double));
    return result;
}

matrix_t* matrix_flatten(const matrix_t* mat) {
    if (!mat) return NULL;
    return matrix_reshape(mat, 1, mat->rows * mat->cols);
}

matrix_t* matrix_slice(const matrix_t* mat, size_t row_start, size_t row_end,
                      size_t col_start, size_t col_end) {
    if (!mat || row_start > row_end || col_start > col_end ||
        row_end > mat->rows || col_end > mat->cols) return NULL;

    size_t new_rows = row_end - row_start;
    size_t new_cols = col_end - col_start;

    matrix_t* result = matrix_create(new_rows, new_cols);
    if (!result) return NULL;

    for (size_t i = 0; i < new_rows; i++) {
        for (size_t j = 0; j < new_cols; j++) {
            result->data[i * new_cols + j] =
                mat->data[(row_start + i) * mat->cols + (col_start + j)];
        }
    }

    return result;
}

/* =========================== */
/*     Matrix Properties       */
/* =========================== */

double matrix_determinant(const matrix_t* mat) {
    if (!mat || mat->rows != mat->cols) return NAN;

    size_t n = mat->rows;

    if (n == 1) {
        return mat->data[0];
    }

    if (n == 2) {
        return mat->data[0] * mat->data[3] - mat->data[1] * mat->data[2];
    }

    /* Use LU decomposition for larger matrices */
    matrix_t* L = NULL;
    matrix_t* U = NULL;

    if (!matrix_lu_decomposition(mat, &L, &U)) {
        return 0.0;  /* Singular matrix */
    }

    double det = 1.0;
    for (size_t i = 0; i < n; i++) {
        det *= U->data[i * n + i];
    }

    matrix_destroy(L);
    matrix_destroy(U);

    return det;
}

double matrix_trace(const matrix_t* mat) {
    if (!mat || mat->rows != mat->cols) return NAN;

    double trace = 0.0;
    for (size_t i = 0; i < mat->rows; i++) {
        trace += mat->data[i * mat->cols + i];
    }

    return trace;
}

double matrix_norm_frobenius(const matrix_t* mat) {
    if (!mat) return NAN;

    double sum = 0.0;
    size_t n = mat->rows * mat->cols;

    for (size_t i = 0; i < n; i++) {
        sum += mat->data[i] * mat->data[i];
    }

    return sqrt(sum);
}

double matrix_norm_1(const matrix_t* mat) {
    if (!mat) return NAN;

    double max_sum = 0.0;

    for (size_t j = 0; j < mat->cols; j++) {
        double col_sum = 0.0;
        for (size_t i = 0; i < mat->rows; i++) {
            col_sum += ABS(mat->data[i * mat->cols + j]);
        }
        max_sum = MAX(max_sum, col_sum);
    }

    return max_sum;
}

double matrix_norm_inf(const matrix_t* mat) {
    if (!mat) return NAN;

    double max_sum = 0.0;

    for (size_t i = 0; i < mat->rows; i++) {
        double row_sum = 0.0;
        for (size_t j = 0; j < mat->cols; j++) {
            row_sum += ABS(mat->data[i * mat->cols + j]);
        }
        max_sum = MAX(max_sum, row_sum);
    }

    return max_sum;
}

bool matrix_is_symmetric(const matrix_t* mat) {
    if (!mat || mat->rows != mat->cols) return false;

    size_t n = mat->rows;
    for (size_t i = 0; i < n; i++) {
        for (size_t j = i + 1; j < n; j++) {
            if (ABS(mat->data[i * n + j] - mat->data[j * n + i]) > EPSILON) {
                return false;
            }
        }
    }

    return true;
}

bool matrix_is_diagonal(const matrix_t* mat) {
    if (!mat || mat->rows != mat->cols) return false;

    size_t n = mat->rows;
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            if (i != j && ABS(mat->data[i * n + j]) > EPSILON) {
                return false;
            }
        }
    }

    return true;
}

bool matrix_is_upper_triangular(const matrix_t* mat) {
    if (!mat || mat->rows != mat->cols) return false;

    size_t n = mat->rows;
    for (size_t i = 1; i < n; i++) {
        for (size_t j = 0; j < i; j++) {
            if (ABS(mat->data[i * n + j]) > EPSILON) {
                return false;
            }
        }
    }

    return true;
}

bool matrix_is_lower_triangular(const matrix_t* mat) {
    if (!mat || mat->rows != mat->cols) return false;

    size_t n = mat->rows;
    for (size_t i = 0; i < n - 1; i++) {
        for (size_t j = i + 1; j < n; j++) {
            if (ABS(mat->data[i * n + j]) > EPSILON) {
                return false;
            }
        }
    }

    return true;
}

/* =========================== */
/*    Matrix Decompositions    */
/* =========================== */

bool matrix_lu_decomposition(const matrix_t* mat, matrix_t** L, matrix_t** U) {
    if (!mat || !L || !U || mat->rows != mat->cols) return false;

    size_t n = mat->rows;
    *L = matrix_create_identity(n);
    *U = matrix_copy(mat);

    if (!*L || !*U) {
        matrix_destroy(*L);
        matrix_destroy(*U);
        *L = NULL;
        *U = NULL;
        return false;
    }

    for (size_t k = 0; k < n - 1; k++) {
        /* Check for zero pivot */
        if (ABS((*U)->data[k * n + k]) < EPSILON) {
            matrix_destroy(*L);
            matrix_destroy(*U);
            *L = NULL;
            *U = NULL;
            return false;
        }

        for (size_t i = k + 1; i < n; i++) {
            double factor = (*U)->data[i * n + k] / (*U)->data[k * n + k];
            (*L)->data[i * n + k] = factor;

            for (size_t j = k; j < n; j++) {
                (*U)->data[i * n + j] -= factor * (*U)->data[k * n + j];
            }
        }
    }

    /* Zero out lower triangle of U */
    for (size_t i = 1; i < n; i++) {
        for (size_t j = 0; j < i; j++) {
            (*U)->data[i * n + j] = 0.0;
        }
    }

    return true;
}

bool matrix_qr_decomposition(const matrix_t* mat, matrix_t** Q, matrix_t** R) {
    if (!mat || !Q || !R) return false;

    size_t m = mat->rows;
    size_t n = mat->cols;

    *Q = matrix_copy(mat);
    *R = matrix_create(n, n);

    if (!*Q || !*R) {
        matrix_destroy(*Q);
        matrix_destroy(*R);
        *Q = NULL;
        *R = NULL;
        return false;
    }

    /* Gram-Schmidt orthogonalization */
    for (size_t j = 0; j < n; j++) {
        /* Compute R[i][j] for i < j */
        for (size_t i = 0; i < j; i++) {
            double dot = 0.0;
            for (size_t k = 0; k < m; k++) {
                dot += (*Q)->data[k * n + i] * mat->data[k * n + j];
            }
            (*R)->data[i * n + j] = dot;

            /* Orthogonalize */
            for (size_t k = 0; k < m; k++) {
                (*Q)->data[k * n + j] -= dot * (*Q)->data[k * n + i];
            }
        }

        /* Compute R[j][j] and normalize */
        double norm = 0.0;
        for (size_t k = 0; k < m; k++) {
            norm += (*Q)->data[k * n + j] * (*Q)->data[k * n + j];
        }
        norm = sqrt(norm);

        if (norm < EPSILON) {
            matrix_destroy(*Q);
            matrix_destroy(*R);
            *Q = NULL;
            *R = NULL;
            return false;
        }

        (*R)->data[j * n + j] = norm;

        /* Normalize column j of Q */
        for (size_t k = 0; k < m; k++) {
            (*Q)->data[k * n + j] /= norm;
        }
    }

    return true;
}

bool matrix_cholesky_decomposition(const matrix_t* mat, matrix_t** L) {
    if (!mat || !L || mat->rows != mat->cols) return false;

    size_t n = mat->rows;

    /* Check if matrix is symmetric */
    if (!matrix_is_symmetric(mat)) return false;

    *L = matrix_create(n, n);
    if (!*L) return false;

    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j <= i; j++) {
            double sum = mat->data[i * n + j];

            for (size_t k = 0; k < j; k++) {
                sum -= (*L)->data[i * n + k] * (*L)->data[j * n + k];
            }

            if (i == j) {
                if (sum <= 0) {
                    /* Not positive definite */
                    matrix_destroy(*L);
                    *L = NULL;
                    return false;
                }
                (*L)->data[i * n + j] = sqrt(sum);
            } else {
                (*L)->data[i * n + j] = sum / (*L)->data[j * n + j];
            }
        }
    }

    return true;
}

/* =========================== */
/*   Linear System Solvers     */
/* =========================== */

matrix_t* matrix_inverse(const matrix_t* mat) {
    if (!mat || mat->rows != mat->cols) return NULL;

    size_t n = mat->rows;
    matrix_t* aug = matrix_create(n, 2 * n);
    if (!aug) return NULL;

    /* Create augmented matrix [A | I] */
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            aug->data[i * 2 * n + j] = mat->data[i * n + j];
        }
        aug->data[i * 2 * n + n + i] = 1.0;
    }

    /* Gauss-Jordan elimination */
    for (size_t i = 0; i < n; i++) {
        /* Find pivot */
        size_t pivot = i;
        double max_val = ABS(aug->data[i * 2 * n + i]);

        for (size_t k = i + 1; k < n; k++) {
            if (ABS(aug->data[k * 2 * n + i]) > max_val) {
                max_val = ABS(aug->data[k * 2 * n + i]);
                pivot = k;
            }
        }

        if (max_val < EPSILON) {
            /* Matrix is singular */
            matrix_destroy(aug);
            return NULL;
        }

        /* Swap rows if needed */
        if (pivot != i) {
            matrix_swap_rows(aug, i, pivot);
        }

        /* Scale pivot row */
        double pivot_val = aug->data[i * 2 * n + i];
        for (size_t j = 0; j < 2 * n; j++) {
            aug->data[i * 2 * n + j] /= pivot_val;
        }

        /* Eliminate column */
        for (size_t k = 0; k < n; k++) {
            if (k == i) continue;

            double factor = aug->data[k * 2 * n + i];
            for (size_t j = 0; j < 2 * n; j++) {
                aug->data[k * 2 * n + j] -= factor * aug->data[i * 2 * n + j];
            }
        }
    }

    /* Extract inverse from augmented matrix */
    matrix_t* inv = matrix_create(n, n);
    if (!inv) {
        matrix_destroy(aug);
        return NULL;
    }

    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            inv->data[i * n + j] = aug->data[i * 2 * n + n + j];
        }
    }

    matrix_destroy(aug);
    return inv;
}

double* matrix_solve_linear_system(const matrix_t* A, const double* b) {
    if (!A || !b || A->rows != A->cols) return NULL;

    return matrix_solve_gauss_elimination(A, b);
}

double* matrix_solve_gauss_elimination(const matrix_t* A, const double* b) {
    if (!A || !b || A->rows != A->cols) return NULL;

    size_t n = A->rows;

    /* Create augmented matrix */
    matrix_t* aug = matrix_create(n, n + 1);
    if (!aug) return NULL;

    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            aug->data[i * (n + 1) + j] = A->data[i * n + j];
        }
        aug->data[i * (n + 1) + n] = b[i];
    }

    /* Forward elimination */
    for (size_t i = 0; i < n - 1; i++) {
        /* Find pivot */
        size_t pivot = i;
        double max_val = ABS(aug->data[i * (n + 1) + i]);

        for (size_t k = i + 1; k < n; k++) {
            if (ABS(aug->data[k * (n + 1) + i]) > max_val) {
                max_val = ABS(aug->data[k * (n + 1) + i]);
                pivot = k;
            }
        }

        if (max_val < EPSILON) {
            /* Matrix is singular */
            matrix_destroy(aug);
            return NULL;
        }

        /* Swap rows if needed */
        if (pivot != i) {
            matrix_swap_rows(aug, i, pivot);
        }

        /* Eliminate column */
        for (size_t k = i + 1; k < n; k++) {
            double factor = aug->data[k * (n + 1) + i] / aug->data[i * (n + 1) + i];
            for (size_t j = i; j <= n; j++) {
                aug->data[k * (n + 1) + j] -= factor * aug->data[i * (n + 1) + j];
            }
        }
    }

    /* Back substitution */
    double* x = malloc(n * sizeof(double));
    if (!x) {
        matrix_destroy(aug);
        return NULL;
    }

    for (int i = n - 1; i >= 0; i--) {
        x[i] = aug->data[i * (n + 1) + n];
        for (size_t j = i + 1; j < n; j++) {
            x[i] -= aug->data[i * (n + 1) + j] * x[j];
        }
        x[i] /= aug->data[i * (n + 1) + i];
    }

    matrix_destroy(aug);
    return x;
}

/* =========================== */
/*      Vector Operations      */
/* =========================== */

double* vector_create(size_t n) {
    return calloc(n, sizeof(double));
}

double* vector_create_from_array(const double* data, size_t n) {
    if (!data || n == 0) return NULL;

    double* vec = malloc(n * sizeof(double));
    if (!vec) return NULL;

    memcpy(vec, data, n * sizeof(double));
    return vec;
}

void vector_destroy(double* vec) {
    free(vec);
}

double vector_dot_product(const double* a, const double* b, size_t n) {
    if (!a || !b) return NAN;

    double dot = 0.0;
    for (size_t i = 0; i < n; i++) {
        dot += a[i] * b[i];
    }

    return dot;
}

double* vector_cross_product(const double* a, const double* b) {
    if (!a || !b) return NULL;

    double* result = malloc(3 * sizeof(double));
    if (!result) return NULL;

    result[0] = a[1] * b[2] - a[2] * b[1];
    result[1] = a[2] * b[0] - a[0] * b[2];
    result[2] = a[0] * b[1] - a[1] * b[0];

    return result;
}

double vector_norm(const double* vec, size_t n) {
    if (!vec) return NAN;

    double sum = 0.0;
    for (size_t i = 0; i < n; i++) {
        sum += vec[i] * vec[i];
    }

    return sqrt(sum);
}

double* vector_normalize(const double* vec, size_t n) {
    if (!vec) return NULL;

    double norm = vector_norm(vec, n);
    if (norm < EPSILON) return NULL;

    double* result = malloc(n * sizeof(double));
    if (!result) return NULL;

    for (size_t i = 0; i < n; i++) {
        result[i] = vec[i] / norm;
    }

    return result;
}

/* =========================== */
/*     Special Matrices        */
/* =========================== */

matrix_t* matrix_hilbert(size_t n) {
    matrix_t* mat = matrix_create(n, n);
    if (!mat) return NULL;

    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            mat->data[i * n + j] = 1.0 / (i + j + 1);
        }
    }

    return mat;
}

matrix_t* matrix_vandermonde(const double* x, size_t n, size_t m) {
    if (!x) return NULL;

    matrix_t* mat = matrix_create(n, m);
    if (!mat) return NULL;

    for (size_t i = 0; i < n; i++) {
        double xi = x[i];
        double power = 1.0;
        for (size_t j = 0; j < m; j++) {
            mat->data[i * m + j] = power;
            power *= xi;
        }
    }

    return mat;
}

/* =========================== */
/*      Matrix Utilities       */
/* =========================== */

void matrix_print(const matrix_t* mat) {
    if (!mat) {
        printf("Matrix is NULL\n");
        return;
    }

    printf("Matrix (%zu x %zu):\n", mat->rows, mat->cols);
    for (size_t i = 0; i < mat->rows; i++) {
        for (size_t j = 0; j < mat->cols; j++) {
            printf("%10.4f ", mat->data[i * mat->cols + j]);
        }
        printf("\n");
    }
}

bool matrix_equals(const matrix_t* a, const matrix_t* b, double tolerance) {
    if (!a || !b) return false;
    if (a->rows != b->rows || a->cols != b->cols) return false;

    size_t n = a->rows * a->cols;
    for (size_t i = 0; i < n; i++) {
        if (ABS(a->data[i] - b->data[i]) > tolerance) {
            return false;
        }
    }

    return true;
}