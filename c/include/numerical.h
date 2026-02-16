/**
 * @file numerical.h
 * @brief Numerical algorithms interface
 */

#ifndef AM_NUMERICAL_H
#define AM_NUMERICAL_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>
#include <complex.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Basic arithmetic operations */
int64_t gcd(int64_t a, int64_t b);
int64_t lcm(int64_t a, int64_t b);
int64_t extended_gcd(int64_t a, int64_t b, int64_t* x, int64_t* y);
int64_t mod_inverse(int64_t a, int64_t m);
int64_t mod_exp(int64_t base, int64_t exp, int64_t mod);
int64_t fast_power(int64_t base, int64_t exp);

/* Prime number algorithms */
bool is_prime(int64_t n);
bool is_prime_miller_rabin(int64_t n, int iterations);
int64_t next_prime(int64_t n);
int64_t nth_prime(size_t n);
size_t* sieve_of_eratosthenes(size_t limit, size_t* count);
size_t* segmented_sieve(int64_t low, int64_t high, size_t* count);
int64_t* prime_factorization(int64_t n, size_t* count);
size_t euler_totient(int64_t n);

/* Combinatorics */
int64_t factorial(int n);
double factorial_double(int n);
int64_t binomial_coefficient(int n, int k);
int64_t catalan_number(int n);
int64_t stirling_first_kind(int n, int k);
int64_t stirling_second_kind(int n, int k);
int64_t bell_number(int n);
int64_t* pascal_triangle_row(int n);

/* Number sequences */
int64_t fibonacci(int n);
int64_t* fibonacci_sequence(int n);
int64_t lucas_number(int n);
int64_t tribonacci(int n);
int64_t* collatz_sequence(int64_t n, size_t* length);

/* Numerical methods */
double newton_raphson(double (*f)(double), double (*df)(double),
                      double x0, double tolerance, int max_iter);
double bisection_method(double (*f)(double), double a, double b,
                        double tolerance, int max_iter);
double secant_method(double (*f)(double), double x0, double x1,
                     double tolerance, int max_iter);
double fixed_point_iteration(double (*g)(double), double x0,
                             double tolerance, int max_iter);

/* Integration methods */
double trapezoidal_rule(double (*f)(double), double a, double b, int n);
double simpson_rule(double (*f)(double), double a, double b, int n);
double romberg_integration(double (*f)(double), double a, double b,
                          double tolerance, int max_iter);
double monte_carlo_integration(double (*f)(double), double a, double b,
                               int num_samples);

/* Interpolation */
double linear_interpolation(double x0, double y0, double x1, double y1, double x);
double* lagrange_interpolation(const double* x, const double* y, size_t n,
                               const double* eval_points, size_t num_eval);
double* newton_divided_differences(const double* x, const double* y, size_t n);
double* cubic_spline_interpolation(const double* x, const double* y, size_t n,
                                   const double* eval_points, size_t num_eval);

/* Fast Fourier Transform */
void fft(double complex* x, size_t n);
void ifft(double complex* x, size_t n);
void real_fft(const double* x, size_t n, double complex* result);
double* convolution(const double* a, size_t len_a,
                    const double* b, size_t len_b);

/* Random number generation */
void random_seed(uint64_t seed);
int random_int(int min, int max);
double random_double(double min, double max);
double random_normal(double mean, double stddev);
double random_exponential(double lambda);
double random_poisson(double lambda);
int* random_permutation(int n);

/* Big integer operations (basic) */
typedef struct big_int big_int_t;

big_int_t* big_int_create(const char* str);
big_int_t* big_int_create_from_int(int64_t value);
void big_int_destroy(big_int_t* num);
big_int_t* big_int_add(const big_int_t* a, const big_int_t* b);
big_int_t* big_int_subtract(const big_int_t* a, const big_int_t* b);
big_int_t* big_int_multiply(const big_int_t* a, const big_int_t* b);
big_int_t* big_int_divide(const big_int_t* a, const big_int_t* b);
big_int_t* big_int_mod(const big_int_t* a, const big_int_t* b);
int big_int_compare(const big_int_t* a, const big_int_t* b);
char* big_int_to_string(const big_int_t* num);

/* Matrix decompositions (basic) */
bool lu_decomposition(const double* A, size_t n, double* L, double* U);
bool qr_decomposition(const double* A, size_t m, size_t n, double* Q, double* R);
bool cholesky_decomposition(const double* A, size_t n, double* L);

/* Special functions */
double gamma_function(double x);
double beta_function(double x, double y);
double erf_function(double x);
double bessel_j0(double x);
double bessel_j1(double x);

#ifdef __cplusplus
}
#endif

#endif /* AM_NUMERICAL_H */