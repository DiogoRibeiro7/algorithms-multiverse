/**
 * @file numerical.c
 * @brief Implementation of numerical algorithms
 */

#include "numerical.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>
#include <time.h>

/* Basic arithmetic operations */

/* Greatest Common Divisor using Euclidean algorithm */
int64_t gcd(int64_t a, int64_t b) {
    a = llabs(a);
    b = llabs(b);

    while (b != 0) {
        int64_t temp = b;
        b = a % b;
        a = temp;
    }

    return a;
}

/* Least Common Multiple */
int64_t lcm(int64_t a, int64_t b) {
    if (a == 0 || b == 0) return 0;

    int64_t g = gcd(a, b);
    return llabs(a / g * b);  /* Avoid overflow by dividing first */
}

/* Extended Euclidean algorithm */
int64_t extended_gcd(int64_t a, int64_t b, int64_t* x, int64_t* y) {
    if (b == 0) {
        if (x) *x = 1;
        if (y) *y = 0;
        return a;
    }

    int64_t x1, y1;
    int64_t g = extended_gcd(b, a % b, &x1, &y1);

    if (x) *x = y1;
    if (y) *y = x1 - (a / b) * y1;

    return g;
}

/* Modular multiplicative inverse */
int64_t mod_inverse(int64_t a, int64_t m) {
    int64_t x, y;
    int64_t g = extended_gcd(a, m, &x, &y);

    if (g != 1) return -1;  /* Inverse doesn't exist */

    return ((x % m) + m) % m;
}

/* Modular exponentiation */
int64_t mod_exp(int64_t base, int64_t exp, int64_t mod) {
    if (mod == 1) return 0;

    int64_t result = 1;
    base %= mod;

    while (exp > 0) {
        if (exp & 1) {
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        exp >>= 1;
    }

    return result;
}

/* Fast power (integer) */
int64_t fast_power(int64_t base, int64_t exp) {
    int64_t result = 1;

    while (exp > 0) {
        if (exp & 1) {
            result *= base;
        }
        base *= base;
        exp >>= 1;
    }

    return result;
}

/* Prime number algorithms */

/* Simple primality test */
bool is_prime(int64_t n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;

    for (int64_t i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) {
            return false;
        }
    }

    return true;
}

/* Miller-Rabin primality test */
static bool miller_rabin_test(int64_t d, int64_t n) {
    int64_t a = 2 + rand() % (n - 4);
    int64_t x = mod_exp(a, d, n);

    if (x == 1 || x == n - 1) {
        return true;
    }

    while (d != n - 1) {
        x = (x * x) % n;
        d *= 2;

        if (x == 1) return false;
        if (x == n - 1) return true;
    }

    return false;
}

bool is_prime_miller_rabin(int64_t n, int iterations) {
    if (n <= 1 || n == 4) return false;
    if (n <= 3) return true;

    /* Find d such that n-1 = 2^r * d */
    int64_t d = n - 1;
    while (d % 2 == 0) {
        d /= 2;
    }

    for (int i = 0; i < iterations; i++) {
        if (!miller_rabin_test(d, n)) {
            return false;
        }
    }

    return true;
}

/* Find next prime after n */
int64_t next_prime(int64_t n) {
    if (n < 2) return 2;

    n++;
    if (n % 2 == 0 && n > 2) n++;  /* Make odd if not 2 */

    while (!is_prime(n)) {
        n += 2;
    }

    return n;
}

/* Sieve of Eratosthenes */
size_t* sieve_of_eratosthenes(size_t limit, size_t* count) {
    if (limit < 2) {
        if (count) *count = 0;
        return NULL;
    }

    bool* is_prime_arr = malloc((limit + 1) * sizeof(bool));
    memset(is_prime_arr, true, (limit + 1) * sizeof(bool));
    is_prime_arr[0] = is_prime_arr[1] = false;

    for (size_t i = 2; i * i <= limit; i++) {
        if (is_prime_arr[i]) {
            for (size_t j = i * i; j <= limit; j += i) {
                is_prime_arr[j] = false;
            }
        }
    }

    /* Count primes */
    size_t prime_count = 0;
    for (size_t i = 2; i <= limit; i++) {
        if (is_prime_arr[i]) prime_count++;
    }

    /* Collect primes */
    size_t* primes = malloc(prime_count * sizeof(size_t));
    size_t index = 0;

    for (size_t i = 2; i <= limit; i++) {
        if (is_prime_arr[i]) {
            primes[index++] = i;
        }
    }

    free(is_prime_arr);

    if (count) *count = prime_count;
    return primes;
}

/* Prime factorization */
int64_t* prime_factorization(int64_t n, size_t* count) {
    if (n <= 1) {
        if (count) *count = 0;
        return NULL;
    }

    size_t capacity = 64;
    int64_t* factors = malloc(capacity * sizeof(int64_t));
    size_t num_factors = 0;

    /* Factor out 2s */
    while (n % 2 == 0) {
        if (num_factors >= capacity) {
            capacity *= 2;
            factors = realloc(factors, capacity * sizeof(int64_t));
        }
        factors[num_factors++] = 2;
        n /= 2;
    }

    /* Factor out odd primes */
    for (int64_t i = 3; i * i <= n; i += 2) {
        while (n % i == 0) {
            if (num_factors >= capacity) {
                capacity *= 2;
                factors = realloc(factors, capacity * sizeof(int64_t));
            }
            factors[num_factors++] = i;
            n /= i;
        }
    }

    /* If n is still > 1, it's a prime factor */
    if (n > 1) {
        if (num_factors >= capacity) {
            capacity *= 2;
            factors = realloc(factors, capacity * sizeof(int64_t));
        }
        factors[num_factors++] = n;
    }

    /* Resize to actual size */
    factors = realloc(factors, num_factors * sizeof(int64_t));

    if (count) *count = num_factors;
    return factors;
}

/* Euler's totient function */
size_t euler_totient(int64_t n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;

    int64_t result = n;

    /* For every prime factor p of n */
    for (int64_t p = 2; p * p <= n; p++) {
        if (n % p == 0) {
            /* Remove all occurrences of p */
            while (n % p == 0) {
                n /= p;
            }
            /* Apply Euler's formula */
            result -= result / p;
        }
    }

    /* If n > 1, then it's a prime factor */
    if (n > 1) {
        result -= result / n;
    }

    return result;
}

/* Combinatorics */

/* Factorial (iterative) */
int64_t factorial(int n) {
    if (n < 0) return 0;
    if (n <= 1) return 1;

    int64_t result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }

    return result;
}

/* Factorial (double for large values) */
double factorial_double(int n) {
    if (n < 0) return 0.0;
    if (n <= 1) return 1.0;

    double result = 1.0;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }

    return result;
}

/* Binomial coefficient */
int64_t binomial_coefficient(int n, int k) {
    if (k < 0 || k > n) return 0;
    if (k == 0 || k == n) return 1;

    /* Optimize by using C(n,k) = C(n,n-k) */
    if (k > n - k) {
        k = n - k;
    }

    int64_t result = 1;
    for (int i = 0; i < k; i++) {
        result *= (n - i);
        result /= (i + 1);
    }

    return result;
}

/* Catalan number */
int64_t catalan_number(int n) {
    if (n <= 1) return 1;

    return binomial_coefficient(2 * n, n) / (n + 1);
}

/* Number sequences */

/* Fibonacci number (iterative) */
int64_t fibonacci(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;

    int64_t prev = 0, curr = 1;
    for (int i = 2; i <= n; i++) {
        int64_t next = prev + curr;
        prev = curr;
        curr = next;
    }

    return curr;
}

/* Fibonacci sequence */
int64_t* fibonacci_sequence(int n) {
    if (n <= 0) return NULL;

    int64_t* seq = malloc(n * sizeof(int64_t));

    if (n >= 1) seq[0] = 0;
    if (n >= 2) seq[1] = 1;

    for (int i = 2; i < n; i++) {
        seq[i] = seq[i - 1] + seq[i - 2];
    }

    return seq;
}

/* Lucas number */
int64_t lucas_number(int n) {
    if (n == 0) return 2;
    if (n == 1) return 1;

    int64_t prev = 2, curr = 1;
    for (int i = 2; i <= n; i++) {
        int64_t next = prev + curr;
        prev = curr;
        curr = next;
    }

    return curr;
}

/* Tribonacci number */
int64_t tribonacci(int n) {
    if (n == 0) return 0;
    if (n <= 2) return 1;

    int64_t a = 0, b = 1, c = 1;
    for (int i = 3; i <= n; i++) {
        int64_t next = a + b + c;
        a = b;
        b = c;
        c = next;
    }

    return c;
}

/* Collatz sequence */
int64_t* collatz_sequence(int64_t n, size_t* length) {
    if (n <= 0) {
        if (length) *length = 0;
        return NULL;
    }

    size_t capacity = 100;
    int64_t* seq = malloc(capacity * sizeof(int64_t));
    size_t len = 0;

    while (n != 1) {
        if (len >= capacity) {
            capacity *= 2;
            seq = realloc(seq, capacity * sizeof(int64_t));
        }

        seq[len++] = n;

        if (n % 2 == 0) {
            n /= 2;
        } else {
            n = 3 * n + 1;
        }
    }

    seq[len++] = 1;

    /* Resize to actual size */
    seq = realloc(seq, len * sizeof(int64_t));

    if (length) *length = len;
    return seq;
}

/* Numerical methods */

/* Newton-Raphson method */
double newton_raphson(double (*f)(double), double (*df)(double),
                      double x0, double tolerance, int max_iter) {
    if (!f || !df) return 0.0;

    double x = x0;
    for (int i = 0; i < max_iter; i++) {
        double fx = f(x);
        double dfx = df(x);

        if (fabs(dfx) < 1e-10) break;  /* Avoid division by zero */

        double x_new = x - fx / dfx;

        if (fabs(x_new - x) < tolerance) {
            return x_new;
        }

        x = x_new;
    }

    return x;
}

/* Bisection method */
double bisection_method(double (*f)(double), double a, double b,
                        double tolerance, int max_iter) {
    if (!f) return 0.0;

    double fa = f(a);
    double fb = f(b);

    if (fa * fb > 0) {
        return 0.0;  /* No root in interval */
    }

    for (int i = 0; i < max_iter; i++) {
        double c = (a + b) / 2;
        double fc = f(c);

        if (fabs(fc) < tolerance || (b - a) / 2 < tolerance) {
            return c;
        }

        if (fc * fa < 0) {
            b = c;
            fb = fc;
        } else {
            a = c;
            fa = fc;
        }
    }

    return (a + b) / 2;
}

/* Integration methods */

/* Trapezoidal rule */
double trapezoidal_rule(double (*f)(double), double a, double b, int n) {
    if (!f || n <= 0) return 0.0;

    double h = (b - a) / n;
    double sum = (f(a) + f(b)) / 2;

    for (int i = 1; i < n; i++) {
        sum += f(a + i * h);
    }

    return h * sum;
}

/* Simpson's rule */
double simpson_rule(double (*f)(double), double a, double b, int n) {
    if (!f || n <= 0 || n % 2 != 0) return 0.0;  /* n must be even */

    double h = (b - a) / n;
    double sum = f(a) + f(b);

    for (int i = 1; i < n; i++) {
        double x = a + i * h;
        if (i % 2 == 0) {
            sum += 2 * f(x);
        } else {
            sum += 4 * f(x);
        }
    }

    return h * sum / 3;
}

/* Monte Carlo integration */
double monte_carlo_integration(double (*f)(double), double a, double b,
                               int num_samples) {
    if (!f || num_samples <= 0) return 0.0;

    srand(time(NULL));
    double sum = 0.0;

    for (int i = 0; i < num_samples; i++) {
        double x = a + ((double)rand() / RAND_MAX) * (b - a);
        sum += f(x);
    }

    return (b - a) * sum / num_samples;
}

/* Interpolation */

/* Linear interpolation */
double linear_interpolation(double x0, double y0, double x1, double y1, double x) {
    if (x1 == x0) return y0;

    return y0 + (y1 - y0) * (x - x0) / (x1 - x0);
}

/* Lagrange interpolation */
double* lagrange_interpolation(const double* x, const double* y, size_t n,
                               const double* eval_points, size_t num_eval) {
    if (!x || !y || !eval_points || n == 0 || num_eval == 0) return NULL;

    double* result = malloc(num_eval * sizeof(double));

    for (size_t k = 0; k < num_eval; k++) {
        double sum = 0.0;

        for (size_t i = 0; i < n; i++) {
            double term = y[i];

            for (size_t j = 0; j < n; j++) {
                if (i != j) {
                    term *= (eval_points[k] - x[j]) / (x[i] - x[j]);
                }
            }

            sum += term;
        }

        result[k] = sum;
    }

    return result;
}

/* Random number generation */

static uint64_t random_state = 12345;

/* Set random seed */
void random_seed(uint64_t seed) {
    random_state = seed;
    srand(seed);
}

/* Random integer in range [min, max] */
int random_int(int min, int max) {
    if (min > max) {
        int temp = min;
        min = max;
        max = temp;
    }

    return min + rand() % (max - min + 1);
}

/* Random double in range [min, max) */
double random_double(double min, double max) {
    if (min > max) {
        double temp = min;
        min = max;
        max = temp;
    }

    return min + ((double)rand() / RAND_MAX) * (max - min);
}

/* Random normal distribution (Box-Muller transform) */
double random_normal(double mean, double stddev) {
    static bool has_spare = false;
    static double spare;

    if (has_spare) {
        has_spare = false;
        return spare * stddev + mean;
    }

    has_spare = true;

    double u = ((double)rand() / RAND_MAX);
    double v = ((double)rand() / RAND_MAX);

    double mag = sqrt(-2.0 * log(u));
    spare = mag * cos(2.0 * M_PI * v);
    return mag * sin(2.0 * M_PI * v) * stddev + mean;
}

/* Random permutation (Fisher-Yates shuffle) */
int* random_permutation(int n) {
    if (n <= 0) return NULL;

    int* perm = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        perm[i] = i;
    }

    for (int i = n - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int temp = perm[i];
        perm[i] = perm[j];
        perm[j] = temp;
    }

    return perm;
}

/* Special functions */

/* Gamma function (Stirling's approximation for large values) */
double gamma_function(double x) {
    if (x <= 0) return NAN;

    /* For small values, use recursion */
    if (x < 12) {
        double result = 1.0;
        while (x > 1) {
            x -= 1.0;
            result *= x;
        }
        return result;
    }

    /* Stirling's approximation for large values */
    double e = 2.71828182845904523536;
    return sqrt(2 * M_PI / x) * pow(x / e, x);
}

/* Error function (approximation) */
double erf_function(double x) {
    /* Abramowitz and Stegun approximation */
    double a1 =  0.254829592;
    double a2 = -0.284496736;
    double a3 =  1.421413741;
    double a4 = -1.453152027;
    double a5 =  1.061405429;
    double p  =  0.3275911;

    int sign = (x < 0) ? -1 : 1;
    x = fabs(x);

    double t = 1.0 / (1.0 + p * x);
    double t2 = t * t;
    double t3 = t2 * t;
    double t4 = t3 * t;
    double t5 = t4 * t;

    double y = 1.0 - ((a1 * t + a2 * t2 + a3 * t3 + a4 * t4 + a5 * t5) *
                      exp(-x * x));

    return sign * y;
}