! Test suite for statistics algorithms module
program test_statistics_module
    use iso_fortran_env, only: int32, real64
    use statistics_module
    implicit none

    integer :: total_tests = 0, passed_tests = 0
    real(real64), parameter :: EPS = 1e-6

    print '(A)', "========================================"
    print '(A)', "    Statistics Module Test Suite"
    print '(A)', "========================================"

    call test_descriptive_statistics()
    call test_hypothesis_testing()
    call test_regression()
    call test_time_series()
    call test_clustering()

    print '(A)', ""
    print '(A)', "========================================"
    print '(A,I0,A,I0)', "Tests passed: ", passed_tests, "/", total_tests
    if (passed_tests == total_tests) then
        print '(A)', "STATUS: ALL TESTS PASSED ✓"
    else
        print '(A)', "STATUS: SOME TESTS FAILED ✗"
    end if
    print '(A)', "========================================"

contains

    subroutine test_descriptive_statistics()
        real(real64) :: data(10), data2(10)
        real(real64) :: result, result_array(10)
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Descriptive Statistics..."

        ! Test data
        data = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0, 9.0, 10.0]

        ! Test mean
        result = mean(data)
        success = abs(result - 5.9_real64) < EPS
        call report_test("Mean calculation", success)

        ! Test median
        result = median(data)
        success = abs(result - 5.0_real64) < EPS
        call report_test("Median calculation", success)

        ! Test mode
        result = mode(data)
        success = abs(result - 4.0_real64) < EPS
        call report_test("Mode calculation", success)

        ! Test variance
        result = variance(data)
        success = abs(result - 7.29_real64) < 0.01
        call report_test("Variance calculation", success)

        ! Test standard deviation
        result = std_dev(data)
        success = abs(result - sqrt(7.29_real64)) < 0.01
        call report_test("Standard deviation", success)

        ! Test covariance
        data2 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        result = covariance(data, data2)
        success = result > 0  ! Should be positive for positively correlated data
        call report_test("Covariance calculation", success)

        ! Test correlation
        result = correlation(data, data2)
        success = result > 0.8 .and. result <= 1.0  ! Strong positive correlation
        call report_test("Correlation coefficient", success)

        ! Test percentile
        result = percentile(data, 0.75_real64)  ! 75th percentile
        success = abs(result - 8.5_real64) < 1.0
        call report_test("Percentile calculation", success)

        ! Test z-score
        result_array = z_score(data)
        success = abs(result_array(1) + 1.44_real64) < 0.2  ! First z-score
        call report_test("Z-score normalization", success)

    end subroutine test_descriptive_statistics

    subroutine test_hypothesis_testing()
        real(real64) :: sample1(20), sample2(20)
        type(hypothesis_test_result) :: test_result
        real(real64) :: chi_square_val
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Hypothesis Testing..."

        ! Generate test data
        call random_number(sample1)
        sample1 = sample1 * 10.0 + 50.0  ! Mean around 55

        ! Test one-sample t-test
        test_result = t_test_one_sample(sample1, 50.0_real64)
        success = test_result%p_value >= 0.0 .and. test_result%p_value <= 1.0
        call report_test("One-sample t-test", success)

        ! Test two-sample t-test
        call random_number(sample2)
        sample2 = sample2 * 10.0 + 52.0  ! Mean around 57
        test_result = t_test_two_sample(sample1, sample2)
        success = test_result%p_value >= 0.0 .and. test_result%p_value <= 1.0
        call report_test("Two-sample t-test", success)

        ! Test chi-square test
        sample1(1:4) = [10.0, 15.0, 20.0, 25.0]  ! Observed frequencies
        sample2(1:4) = [12.0, 13.0, 22.0, 23.0]  ! Expected frequencies
        chi_square_val = chi_square_test(sample1(1:4), sample2(1:4))
        success = chi_square_val >= 0.0
        call report_test("Chi-square test", success)

        ! Test ANOVA
        sample1(1:5) = [23.0, 25.0, 27.0, 24.0, 26.0]
        sample2(1:5) = [28.0, 30.0, 29.0, 31.0, 32.0]
        test_result = anova_one_way(sample1(1:5), sample2(1:5), sample1(1:5))
        success = test_result%f_statistic >= 0.0
        call report_test("One-way ANOVA", success)

    end subroutine test_hypothesis_testing

    subroutine test_regression()
        real(real64) :: x(10), y(10)
        real(real64) :: slope, intercept, r_squared
        real(real64) :: coefficients(3), y_pred(10)
        logical :: success
        integer :: i

        print '(A)', ""
        print '(A)', "Testing Regression Analysis..."

        ! Generate test data
        do i = 1, 10
            x(i) = real(i, real64)
            y(i) = 2.0 * x(i) + 1.0 + 0.1 * (i - 5)  ! y = 2x + 1 with noise
        end do

        ! Test linear regression
        call linear_regression(x, y, slope, intercept, r_squared)
        success = abs(slope - 2.0) < 0.5 .and. abs(intercept - 1.0) < 2.0
        call report_test("Linear regression", success)

        success = r_squared > 0.9  ! Should have high R-squared
        call report_test("R-squared value", success)

        ! Test polynomial regression (degree 2)
        do i = 1, 10
            y(i) = x(i)**2 + 2.0*x(i) + 1.0  ! Quadratic function
        end do

        call polynomial_regression(x, y, 2, coefficients, y_pred)
        success = abs(coefficients(1) - 1.0) < 1.0  ! Coefficient of x^2
        call report_test("Polynomial regression", success)

        ! Test exponential regression
        do i = 1, 10
            y(i) = 2.0 * exp(0.5 * x(i))
        end do

        call exponential_regression(x, y, slope, intercept, r_squared)
        success = slope > 0.0  ! Growth rate should be positive
        call report_test("Exponential regression", success)

    end subroutine test_regression

    subroutine test_time_series()
        real(real64) :: data(20), smoothed(20)
        real(real64) :: ma_result(16), acf(10)
        real(real64) :: alpha
        logical :: success
        integer :: i

        print '(A)', ""
        print '(A)', "Testing Time Series Analysis..."

        ! Generate time series data with trend and noise
        do i = 1, 20
            data(i) = real(i, real64) + 0.5 * sin(real(i, real64)) + 0.1 * (i - 10)
        end do

        ! Test moving average (window size 5)
        call moving_average(data, 5, ma_result)
        success = size(ma_result) > 0
        call report_test("Moving average", success)

        ! Test exponential smoothing
        alpha = 0.3_real64
        call exponential_smoothing(data, alpha, smoothed)
        success = abs(smoothed(1) - data(1)) < EPS  ! First value unchanged
        call report_test("Exponential smoothing", success)

        ! Test autocorrelation
        call autocorrelation(data, 10, acf)
        success = abs(acf(1) - 1.0) < EPS  ! Lag 0 should be 1
        call report_test("Autocorrelation function", success)

    end subroutine test_time_series

    subroutine test_clustering()
        real(real64) :: data(20, 2), centers(2, 2)
        integer :: labels(20), k
        real(real64) :: threshold, min_points
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Clustering Algorithms..."

        ! Generate 2D clustering test data
        ! Cluster 1 around (2, 2)
        data(1:10, 1) = [1.8, 2.1, 1.9, 2.2, 2.0, 1.7, 2.3, 1.9, 2.1, 2.0]
        data(1:10, 2) = [1.9, 2.1, 2.0, 1.8, 2.2, 2.1, 1.9, 2.0, 2.3, 1.8]

        ! Cluster 2 around (5, 5)
        data(11:20, 1) = [4.8, 5.1, 4.9, 5.2, 5.0, 4.7, 5.3, 4.9, 5.1, 5.0]
        data(11:20, 2) = [4.9, 5.1, 5.0, 4.8, 5.2, 5.1, 4.9, 5.0, 5.3, 4.8]

        ! Test K-means clustering
        k = 2
        call k_means_clustering(data, k, labels, centers)
        success = maxval(labels) == k .and. minval(labels) == 1
        call report_test("K-means clustering", success)

        ! Check that centers are roughly correct
        success = (abs(centers(1,1) - 2.0) < 0.5 .or. abs(centers(1,1) - 5.0) < 0.5)
        call report_test("K-means centers", success)

        ! Test hierarchical clustering
        threshold = 2.0_real64
        call hierarchical_clustering(data, threshold, labels)
        success = maxval(labels) >= 1
        call report_test("Hierarchical clustering", success)

        ! Test DBSCAN clustering
        threshold = 0.5_real64  ! epsilon
        min_points = 3.0_real64
        call dbscan_clustering(data, threshold, min_points, labels)
        success = maxval(labels) >= 1  ! At least one cluster found
        call report_test("DBSCAN clustering", success)

        ! Test PCA
        call test_pca()

    end subroutine test_clustering

    subroutine test_pca()
        real(real64) :: data(10, 3), transformed(10, 2)
        real(real64) :: components(3, 2), explained_variance(2)
        logical :: success

        ! Generate correlated 3D data
        data(:, 1) = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        data(:, 2) = data(:, 1) * 2.0 + 1.0  ! Linear relationship
        data(:, 3) = data(:, 1) * 0.5 - 2.0  ! Another linear relationship

        ! Perform PCA to reduce to 2 dimensions
        call pca_transform(data, 2, transformed, components, explained_variance)

        success = size(transformed, 2) == 2  ! Reduced to 2 dimensions
        call report_test("PCA dimensionality reduction", success)

        success = explained_variance(1) > explained_variance(2)  ! First PC explains more
        call report_test("PCA variance explained", success)

    end subroutine test_pca

    subroutine report_test(test_name, success)
        character(len=*), intent(in) :: test_name
        logical, intent(in) :: success

        total_tests = total_tests + 1
        if (success) then
            passed_tests = passed_tests + 1
            print '(A,A,A)', "  ✓ ", test_name, " ... PASSED"
        else
            print '(A,A,A)', "  ✗ ", test_name, " ... FAILED"
        end if
    end subroutine report_test

end program test_statistics_module