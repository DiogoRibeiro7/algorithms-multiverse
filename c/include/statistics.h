/**
 * @file statistics.h
 * @brief Statistical algorithms interface
 */

#ifndef AM_STATISTICS_H
#define AM_STATISTICS_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Descriptive statistics */
double stats_mean(const double* data, size_t n);
double stats_median(double* data, size_t n);
double stats_mode(const double* data, size_t n);
double stats_variance(const double* data, size_t n);
double stats_variance_sample(const double* data, size_t n);
double stats_std_dev(const double* data, size_t n);
double stats_std_dev_sample(const double* data, size_t n);
double stats_covariance(const double* x, const double* y, size_t n);
double stats_correlation(const double* x, const double* y, size_t n);
double stats_skewness(const double* data, size_t n);
double stats_kurtosis(const double* data, size_t n);
double stats_sem(const double* data, size_t n);  /* Standard error of mean */

/* Percentiles and quantiles */
double stats_percentile(double* data, size_t n, double p);
double stats_quartile(double* data, size_t n, int q);
double stats_iqr(double* data, size_t n);  /* Interquartile range */
void stats_five_number_summary(double* data, size_t n,
                               double* min, double* q1, double* median,
                               double* q3, double* max);

/* Range statistics */
double stats_range(const double* data, size_t n);
double stats_min(const double* data, size_t n);
double stats_max(const double* data, size_t n);
void stats_min_max(const double* data, size_t n, double* min, double* max);

/* Weighted statistics */
double stats_weighted_mean(const double* data, const double* weights, size_t n);
double stats_weighted_variance(const double* data, const double* weights, size_t n);
double stats_weighted_std_dev(const double* data, const double* weights, size_t n);

/* Moving statistics */
double* stats_moving_average(const double* data, size_t n, size_t window);
double* stats_cumulative_sum(const double* data, size_t n);
double* stats_cumulative_product(const double* data, size_t n);
double* stats_exponential_moving_average(const double* data, size_t n, double alpha);

/* Hypothesis testing structures */
typedef struct {
    double statistic;
    double p_value;
    double df;  /* degrees of freedom */
    bool reject_null;
    double confidence_level;
} hypothesis_test_t;

typedef struct {
    double lower;
    double upper;
    double confidence_level;
} confidence_interval_t;

/* T-tests */
hypothesis_test_t stats_t_test_one_sample(const double* data, size_t n,
                                          double population_mean);
hypothesis_test_t stats_t_test_two_sample(const double* data1, size_t n1,
                                          const double* data2, size_t n2,
                                          bool equal_variance);
hypothesis_test_t stats_t_test_paired(const double* data1,
                                      const double* data2, size_t n);

/* Other hypothesis tests */
hypothesis_test_t stats_z_test(const double* data, size_t n,
                               double population_mean, double population_std);
hypothesis_test_t stats_chi_square_test(const double* observed,
                                        const double* expected, size_t n);
hypothesis_test_t stats_anova_one_way(double** groups, size_t* group_sizes,
                                      size_t num_groups);
hypothesis_test_t stats_mann_whitney_u(const double* data1, size_t n1,
                                       const double* data2, size_t n2);
hypothesis_test_t stats_wilcoxon_signed_rank(const double* data1,
                                             const double* data2, size_t n);
hypothesis_test_t stats_kruskal_wallis(double** groups, size_t* group_sizes,
                                       size_t num_groups);

/* Confidence intervals */
confidence_interval_t stats_ci_mean(const double* data, size_t n,
                                    double confidence_level);
confidence_interval_t stats_ci_proportion(int successes, int trials,
                                          double confidence_level);
confidence_interval_t stats_ci_difference_means(const double* data1, size_t n1,
                                                const double* data2, size_t n2,
                                                double confidence_level);

/* Regression analysis */
typedef struct {
    double slope;
    double intercept;
    double r_squared;
    double std_error_slope;
    double std_error_intercept;
    double* residuals;
    size_t n;
} linear_regression_t;

typedef struct {
    double* coefficients;
    size_t degree;
    double r_squared;
    double* residuals;
    size_t n;
} polynomial_regression_t;

linear_regression_t* stats_linear_regression(const double* x, const double* y,
                                             size_t n);
void linear_regression_destroy(linear_regression_t* reg);
double linear_regression_predict(const linear_regression_t* reg, double x);

polynomial_regression_t* stats_polynomial_regression(const double* x,
                                                     const double* y,
                                                     size_t n, size_t degree);
void polynomial_regression_destroy(polynomial_regression_t* reg);
double polynomial_regression_predict(const polynomial_regression_t* reg, double x);

double* stats_multiple_regression(double** X, const double* y,
                                 size_t n, size_t m, double* r_squared);
double stats_logistic_regression_fit(double** X, const int* y,
                                     size_t n, size_t m, double* weights);

/* Correlation and association */
double stats_spearman_correlation(double* x, double* y, size_t n);
double stats_kendall_correlation(const double* x, const double* y, size_t n);
double stats_cramers_v(const int** contingency_table, size_t rows, size_t cols);

/* Time series analysis */
double* stats_autocorrelation(const double* data, size_t n, size_t max_lag);
double* stats_partial_autocorrelation(const double* data, size_t n, size_t max_lag);
void stats_decompose_additive(const double* data, size_t n, size_t period,
                              double** trend, double** seasonal,
                              double** residual);
double* stats_holt_winters(const double* data, size_t n,
                          double alpha, double beta, double gamma,
                          size_t period, size_t forecast_periods);

/* Distributions */
double stats_normal_pdf(double x, double mean, double std_dev);
double stats_normal_cdf(double x, double mean, double std_dev);
double stats_normal_quantile(double p, double mean, double std_dev);
double stats_t_pdf(double x, double df);
double stats_t_cdf(double x, double df);
double stats_chi_square_pdf(double x, double df);
double stats_chi_square_cdf(double x, double df);
double stats_f_pdf(double x, double df1, double df2);
double stats_f_cdf(double x, double df1, double df2);
double stats_poisson_pmf(int k, double lambda);
double stats_binomial_pmf(int k, int n, double p);
double stats_exponential_pdf(double x, double lambda);
double stats_exponential_cdf(double x, double lambda);

/* Clustering */
typedef struct {
    double** centers;
    int* labels;
    size_t k;
    size_t n;
    size_t dim;
    double inertia;
} kmeans_result_t;

kmeans_result_t* stats_kmeans(double** data, size_t n, size_t dim,
                              size_t k, int max_iter);
void kmeans_destroy(kmeans_result_t* result);

typedef struct {
    int* labels;
    size_t n;
    size_t num_clusters;
    double** linkage_matrix;
} hierarchical_result_t;

hierarchical_result_t* stats_hierarchical_clustering(double** data, size_t n,
                                                     size_t dim,
                                                     const char* method,
                                                     double threshold);
void hierarchical_destroy(hierarchical_result_t* result);

/* Principal Component Analysis */
typedef struct {
    double** components;
    double* explained_variance;
    double* explained_variance_ratio;
    size_t n_components;
    size_t n_features;
} pca_result_t;

pca_result_t* stats_pca(double** data, size_t n, size_t dim,
                        size_t n_components);
void pca_destroy(pca_result_t* result);
double** pca_transform(const pca_result_t* pca, double** data,
                      size_t n, size_t dim);

/* Outlier detection */
size_t* stats_outliers_iqr(double* data, size_t n, double k, size_t* num_outliers);
size_t* stats_outliers_zscore(const double* data, size_t n,
                              double threshold, size_t* num_outliers);
size_t* stats_outliers_mad(double* data, size_t n, double threshold,
                           size_t* num_outliers);
size_t* stats_outliers_isolation_forest(double** data, size_t n, size_t dim,
                                        double contamination, size_t* num_outliers);

/* Normality tests */
hypothesis_test_t stats_shapiro_wilk_test(const double* data, size_t n);
hypothesis_test_t stats_anderson_darling_test(const double* data, size_t n);
hypothesis_test_t stats_kolmogorov_smirnov_test(const double* data, size_t n);

/* Data transformation */
double* stats_normalize_zscore(const double* data, size_t n);
double* stats_normalize_minmax(const double* data, size_t n,
                               double new_min, double new_max);
double* stats_log_transform(const double* data, size_t n);
double* stats_box_cox_transform(const double* data, size_t n, double lambda);

/* Sampling */
void stats_sample_with_replacement(const double* data, size_t n,
                                   double* sample, size_t sample_size);
void stats_sample_without_replacement(const double* data, size_t n,
                                      double* sample, size_t sample_size);
double** stats_bootstrap(const double* data, size_t n,
                         size_t num_samples, size_t sample_size);

#ifdef __cplusplus
}
#endif

#endif /* AM_STATISTICS_H */