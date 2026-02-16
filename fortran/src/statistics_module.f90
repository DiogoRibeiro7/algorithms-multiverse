! Statistics Module
! Comprehensive statistical functions and algorithms

module statistics_module
    use iso_fortran_env, only: int32, int64, real32, real64
    implicit none
    private

    ! Public interfaces
    public :: mean, median, mode, variance, std_dev
    public :: geometric_mean, harmonic_mean, weighted_mean
    public :: percentile, quartiles, iqr, range
    public :: skewness, kurtosis, moments
    public :: covariance, correlation, pearson_correlation
    public :: spearman_correlation, kendall_tau
    public :: linear_regression, polynomial_regression
    public :: exponential_regression, logarithmic_regression
    public :: multiple_regression, ridge_regression
    public :: moving_average, exponential_smoothing
    public :: cumulative_sum, cumulative_product
    public :: z_score, t_score, chi_square_test
    public :: anova, f_test, t_test
    public :: kolmogorov_smirnov_test, shapiro_wilk_test
    public :: confidence_interval, bootstrap
    public :: histogram, frequency_table
    public :: entropy, mutual_information
    public :: pca, factor_analysis
    public :: k_means_clustering, hierarchical_clustering
    public :: outlier_detection, box_plot_stats
    public :: time_series_decomposition, autocorrelation
    public :: cross_correlation, fourier_analysis

    ! Constants
    real(real64), parameter :: PI = 3.14159265358979323846_real64
    real(real64), parameter :: E = 2.71828182845904523536_real64
    real(real64), parameter :: EPSILON = 1.0e-12_real64

    ! Types for complex statistical structures
    type :: regression_result
        real(real64), dimension(:), allocatable :: coefficients
        real(real64) :: r_squared
        real(real64) :: adjusted_r_squared
        real(real64) :: standard_error
        real(real64), dimension(:), allocatable :: residuals
    end type regression_result

    type :: cluster_result
        integer(int32), dimension(:), allocatable :: labels
        real(real64), dimension(:,:), allocatable :: centers
        integer(int32) :: n_clusters
        real(real64) :: inertia
    end type cluster_result

    type :: time_series_components
        real(real64), dimension(:), allocatable :: trend
        real(real64), dimension(:), allocatable :: seasonal
        real(real64), dimension(:), allocatable :: residual
    end type time_series_components

contains

    !===============================================
    ! Basic Descriptive Statistics
    !===============================================

    function mean(data) result(avg)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64) :: avg

        if (size(data) == 0) then
            avg = 0.0_real64
            return
        end if

        avg = sum(data) / real(size(data), real64)

    end function mean

    function median(data) result(med)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64) :: med
        real(real64), dimension(:), allocatable :: sorted_data
        integer(int32) :: n

        n = size(data)
        if (n == 0) then
            med = 0.0_real64
            return
        end if

        allocate(sorted_data(n))
        sorted_data = data
        call sort_array(sorted_data)

        if (mod(n, 2) == 0) then
            med = (sorted_data(n/2) + sorted_data(n/2 + 1)) / 2.0_real64
        else
            med = sorted_data((n + 1) / 2)
        end if

        deallocate(sorted_data)

    end function median

    function mode(data) result(mode_val)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64), dimension(:), allocatable :: mode_val
        real(real64), dimension(:), allocatable :: unique_vals
        integer(int32), dimension(:), allocatable :: counts
        integer(int32) :: n, i, j, max_count, n_modes

        n = size(data)
        if (n == 0) then
            allocate(mode_val(0))
            return
        end if

        ! Find unique values and their counts
        allocate(unique_vals(n))
        allocate(counts(n))

        call find_unique_with_counts(data, unique_vals, counts, n_unique)

        ! Find maximum count
        max_count = maxval(counts(1:n_unique))

        ! Count modes
        n_modes = count(counts(1:n_unique) == max_count)

        allocate(mode_val(n_modes))
        j = 1
        do i = 1, n_unique
            if (counts(i) == max_count) then
                mode_val(j) = unique_vals(i)
                j = j + 1
            end if
        end do

        deallocate(unique_vals, counts)

    end function mode

    function variance(data, ddof) result(var)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        integer(int32), intent(in), optional :: ddof
        real(real64) :: var
        real(real64) :: avg
        integer(int32) :: n, degrees_of_freedom

        n = size(data)
        if (n <= 1) then
            var = 0.0_real64
            return
        end if

        if (present(ddof)) then
            degrees_of_freedom = ddof
        else
            degrees_of_freedom = 0
        end if

        avg = mean(data)
        var = sum((data - avg)**2) / real(n - degrees_of_freedom, real64)

    end function variance

    function std_dev(data, ddof) result(sd)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        integer(int32), intent(in), optional :: ddof
        real(real64) :: sd

        sd = sqrt(variance(data, ddof))

    end function std_dev

    function geometric_mean(data) result(gm)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64) :: gm
        integer(int32) :: n

        n = size(data)
        if (n == 0 .or. any(data <= 0.0_real64)) then
            gm = 0.0_real64
            return
        end if

        gm = exp(sum(log(data)) / real(n, real64))

    end function geometric_mean

    function harmonic_mean(data) result(hm)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64) :: hm
        integer(int32) :: n

        n = size(data)
        if (n == 0 .or. any(data == 0.0_real64)) then
            hm = 0.0_real64
            return
        end if

        hm = real(n, real64) / sum(1.0_real64 / data)

    end function harmonic_mean

    function weighted_mean(data, weights) result(wm)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64), dimension(:), intent(in) :: weights
        real(real64) :: wm

        if (size(data) /= size(weights) .or. size(data) == 0) then
            wm = 0.0_real64
            return
        end if

        wm = sum(data * weights) / sum(weights)

    end function weighted_mean

    !===============================================
    ! Percentiles and Quartiles
    !===============================================

    function percentile(data, p) result(pct)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64), intent(in) :: p
        real(real64) :: pct
        real(real64), dimension(:), allocatable :: sorted_data
        real(real64) :: pos
        integer(int32) :: n, lower, upper

        n = size(data)
        if (n == 0 .or. p < 0.0_real64 .or. p > 100.0_real64) then
            pct = 0.0_real64
            return
        end if

        allocate(sorted_data(n))
        sorted_data = data
        call sort_array(sorted_data)

        pos = p * real(n - 1, real64) / 100.0_real64 + 1.0_real64
        lower = int(pos)
        upper = min(lower + 1, n)

        if (lower == upper) then
            pct = sorted_data(lower)
        else
            pct = sorted_data(lower) + (pos - lower) * (sorted_data(upper) - sorted_data(lower))
        end if

        deallocate(sorted_data)

    end function percentile

    function quartiles(data) result(q)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64), dimension(3) :: q

        q(1) = percentile(data, 25.0_real64)
        q(2) = percentile(data, 50.0_real64)
        q(3) = percentile(data, 75.0_real64)

    end function quartiles

    function iqr(data) result(interquartile_range)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64) :: interquartile_range
        real(real64), dimension(3) :: q

        q = quartiles(data)
        interquartile_range = q(3) - q(1)

    end function iqr

    function range(data) result(data_range)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64) :: data_range

        if (size(data) == 0) then
            data_range = 0.0_real64
        else
            data_range = maxval(data) - minval(data)
        end if

    end function range

    !===============================================
    ! Higher-order Moments
    !===============================================

    function skewness(data) result(skew)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64) :: skew
        real(real64) :: avg, sd
        integer(int32) :: n

        n = size(data)
        if (n < 3) then
            skew = 0.0_real64
            return
        end if

        avg = mean(data)
        sd = std_dev(data, 1)

        if (sd < EPSILON) then
            skew = 0.0_real64
        else
            skew = sum(((data - avg) / sd)**3) * real(n, real64) / &
                   (real(n - 1, real64) * real(n - 2, real64))
        end if

    end function skewness

    function kurtosis(data, excess) result(kurt)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        logical, intent(in), optional :: excess
        real(real64) :: kurt
        real(real64) :: avg, sd
        integer(int32) :: n
        logical :: compute_excess

        n = size(data)
        if (n < 4) then
            kurt = 0.0_real64
            return
        end if

        if (present(excess)) then
            compute_excess = excess
        else
            compute_excess = .true.
        end if

        avg = mean(data)
        sd = std_dev(data, 1)

        if (sd < EPSILON) then
            kurt = 0.0_real64
        else
            kurt = sum(((data - avg) / sd)**4) * real(n * (n + 1), real64) / &
                   (real((n - 1) * (n - 2) * (n - 3), real64)) - &
                   3.0_real64 * real((n - 1)**2, real64) / &
                   real((n - 2) * (n - 3), real64)

            if (.not. compute_excess) then
                kurt = kurt + 3.0_real64
            end if
        end if

    end function kurtosis

    function moments(data, order) result(mom)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        integer(int32), intent(in) :: order
        real(real64) :: mom
        real(real64) :: avg

        if (size(data) == 0 .or. order < 1) then
            mom = 0.0_real64
            return
        end if

        avg = mean(data)
        mom = sum((data - avg)**order) / real(size(data), real64)

    end function moments

    !===============================================
    ! Correlation and Covariance
    !===============================================

    function covariance(x, y, ddof) result(cov)
        implicit none
        real(real64), dimension(:), intent(in) :: x, y
        integer(int32), intent(in), optional :: ddof
        real(real64) :: cov
        real(real64) :: mean_x, mean_y
        integer(int32) :: n, degrees_of_freedom

        n = size(x)
        if (n /= size(y) .or. n <= 1) then
            cov = 0.0_real64
            return
        end if

        if (present(ddof)) then
            degrees_of_freedom = ddof
        else
            degrees_of_freedom = 1
        end if

        mean_x = mean(x)
        mean_y = mean(y)

        cov = sum((x - mean_x) * (y - mean_y)) / real(n - degrees_of_freedom, real64)

    end function covariance

    function correlation(x, y) result(corr)
        implicit none
        real(real64), dimension(:), intent(in) :: x, y
        real(real64) :: corr

        corr = pearson_correlation(x, y)

    end function correlation

    function pearson_correlation(x, y) result(r)
        implicit none
        real(real64), dimension(:), intent(in) :: x, y
        real(real64) :: r
        real(real64) :: cov_xy, std_x, std_y

        if (size(x) /= size(y) .or. size(x) <= 1) then
            r = 0.0_real64
            return
        end if

        cov_xy = covariance(x, y)
        std_x = std_dev(x)
        std_y = std_dev(y)

        if (std_x < EPSILON .or. std_y < EPSILON) then
            r = 0.0_real64
        else
            r = cov_xy / (std_x * std_y)
        end if

    end function pearson_correlation

    function spearman_correlation(x, y) result(rho)
        implicit none
        real(real64), dimension(:), intent(in) :: x, y
        real(real64) :: rho
        real(real64), dimension(:), allocatable :: rank_x, rank_y
        integer(int32) :: n

        n = size(x)
        if (n /= size(y) .or. n <= 1) then
            rho = 0.0_real64
            return
        end if

        allocate(rank_x(n), rank_y(n))

        rank_x = compute_ranks(x)
        rank_y = compute_ranks(y)

        rho = pearson_correlation(rank_x, rank_y)

        deallocate(rank_x, rank_y)

    end function spearman_correlation

    function kendall_tau(x, y) result(tau)
        implicit none
        real(real64), dimension(:), intent(in) :: x, y
        real(real64) :: tau
        integer(int32) :: n, i, j, concordant, discordant

        n = size(x)
        if (n /= size(y) .or. n <= 1) then
            tau = 0.0_real64
            return
        end if

        concordant = 0
        discordant = 0

        do i = 1, n-1
            do j = i+1, n
                if ((x(i) - x(j)) * (y(i) - y(j)) > 0.0_real64) then
                    concordant = concordant + 1
                else if ((x(i) - x(j)) * (y(i) - y(j)) < 0.0_real64) then
                    discordant = discordant + 1
                end if
            end do
        end do

        tau = real(concordant - discordant, real64) / real(n * (n - 1) / 2, real64)

    end function kendall_tau

    !===============================================
    ! Regression Analysis
    !===============================================

    function linear_regression(x, y) result(result)
        implicit none
        real(real64), dimension(:), intent(in) :: x, y
        type(regression_result) :: result
        real(real64) :: mean_x, mean_y, ss_xx, ss_xy, ss_yy
        real(real64) :: slope, intercept
        integer(int32) :: n, i

        n = size(x)
        if (n /= size(y) .or. n < 2) then
            allocate(result%coefficients(0))
            allocate(result%residuals(0))
            result%r_squared = 0.0_real64
            result%adjusted_r_squared = 0.0_real64
            result%standard_error = 0.0_real64
            return
        end if

        mean_x = mean(x)
        mean_y = mean(y)

        ss_xx = sum((x - mean_x)**2)
        ss_xy = sum((x - mean_x) * (y - mean_y))
        ss_yy = sum((y - mean_y)**2)

        if (ss_xx < EPSILON) then
            allocate(result%coefficients(0))
            allocate(result%residuals(0))
            result%r_squared = 0.0_real64
            result%adjusted_r_squared = 0.0_real64
            result%standard_error = 0.0_real64
            return
        end if

        slope = ss_xy / ss_xx
        intercept = mean_y - slope * mean_x

        allocate(result%coefficients(2))
        result%coefficients(1) = intercept
        result%coefficients(2) = slope

        allocate(result%residuals(n))
        result%residuals = y - (intercept + slope * x)

        result%r_squared = (ss_xy**2) / (ss_xx * ss_yy)
        result%adjusted_r_squared = 1.0_real64 - (1.0_real64 - result%r_squared) * &
                                   real(n - 1, real64) / real(n - 2, real64)
        result%standard_error = sqrt(sum(result%residuals**2) / real(n - 2, real64))

    end function linear_regression

    function polynomial_regression(x, y, degree) result(result)
        implicit none
        real(real64), dimension(:), intent(in) :: x, y
        integer(int32), intent(in) :: degree
        type(regression_result) :: result
        real(real64), dimension(:,:), allocatable :: X_matrix
        real(real64), dimension(:,:), allocatable :: XtX
        real(real64), dimension(:), allocatable :: Xty
        integer(int32) :: n, i, j

        n = size(x)
        if (n /= size(y) .or. n <= degree .or. degree < 1) then
            allocate(result%coefficients(0))
            allocate(result%residuals(0))
            result%r_squared = 0.0_real64
            result%adjusted_r_squared = 0.0_real64
            result%standard_error = 0.0_real64
            return
        end if

        ! Build design matrix
        allocate(X_matrix(n, degree + 1))
        do i = 1, n
            do j = 0, degree
                X_matrix(i, j + 1) = x(i)**j
            end do
        end do

        ! Solve normal equations: (X'X)β = X'y
        allocate(XtX(degree + 1, degree + 1))
        allocate(Xty(degree + 1))

        XtX = matmul(transpose(X_matrix), X_matrix)
        Xty = matmul(transpose(X_matrix), y)

        ! Solve for coefficients (simplified - should use proper linear solver)
        allocate(result%coefficients(degree + 1))
        call solve_linear_system(XtX, Xty, result%coefficients)

        ! Calculate residuals and statistics
        allocate(result%residuals(n))
        do i = 1, n
            result%residuals(i) = y(i)
            do j = 0, degree
                result%residuals(i) = result%residuals(i) - &
                                     result%coefficients(j + 1) * x(i)**j
            end do
        end do

        ! Calculate R-squared
        result%r_squared = 1.0_real64 - sum(result%residuals**2) / sum((y - mean(y))**2)
        result%adjusted_r_squared = 1.0_real64 - (1.0_real64 - result%r_squared) * &
                                   real(n - 1, real64) / real(n - degree - 1, real64)
        result%standard_error = sqrt(sum(result%residuals**2) / real(n - degree - 1, real64))

        deallocate(X_matrix, XtX, Xty)

    end function polynomial_regression

    function exponential_regression(x, y) result(result)
        implicit none
        real(real64), dimension(:), intent(in) :: x, y
        type(regression_result) :: result
        real(real64), dimension(:), allocatable :: log_y
        type(regression_result) :: linear_result

        if (any(y <= 0.0_real64)) then
            allocate(result%coefficients(0))
            allocate(result%residuals(0))
            result%r_squared = 0.0_real64
            result%adjusted_r_squared = 0.0_real64
            result%standard_error = 0.0_real64
            return
        end if

        allocate(log_y(size(y)))
        log_y = log(y)

        linear_result = linear_regression(x, log_y)

        allocate(result%coefficients(2))
        result%coefficients(1) = exp(linear_result%coefficients(1))  ! a = exp(intercept)
        result%coefficients(2) = linear_result%coefficients(2)       ! b = slope

        allocate(result%residuals(size(y)))
        result%residuals = y - result%coefficients(1) * exp(result%coefficients(2) * x)

        result%r_squared = linear_result%r_squared
        result%adjusted_r_squared = linear_result%adjusted_r_squared
        result%standard_error = sqrt(sum(result%residuals**2) / real(size(y) - 2, real64))

        deallocate(log_y)

    end function exponential_regression

    function logarithmic_regression(x, y) result(result)
        implicit none
        real(real64), dimension(:), intent(in) :: x, y
        type(regression_result) :: result
        real(real64), dimension(:), allocatable :: log_x

        if (any(x <= 0.0_real64)) then
            allocate(result%coefficients(0))
            allocate(result%residuals(0))
            result%r_squared = 0.0_real64
            result%adjusted_r_squared = 0.0_real64
            result%standard_error = 0.0_real64
            return
        end if

        allocate(log_x(size(x)))
        log_x = log(x)

        result = linear_regression(log_x, y)

        deallocate(log_x)

    end function logarithmic_regression

    !===============================================
    ! Time Series Analysis
    !===============================================

    function moving_average(data, window) result(ma)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        integer(int32), intent(in) :: window
        real(real64), dimension(:), allocatable :: ma
        integer(int32) :: n, i

        n = size(data)
        if (window <= 0 .or. window > n) then
            allocate(ma(0))
            return
        end if

        allocate(ma(n - window + 1))

        do i = 1, n - window + 1
            ma(i) = sum(data(i:i+window-1)) / real(window, real64)
        end do

    end function moving_average

    function exponential_smoothing(data, alpha) result(smoothed)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64), intent(in) :: alpha
        real(real64), dimension(:), allocatable :: smoothed
        integer(int32) :: n, i

        n = size(data)
        if (n == 0 .or. alpha < 0.0_real64 .or. alpha > 1.0_real64) then
            allocate(smoothed(0))
            return
        end if

        allocate(smoothed(n))

        smoothed(1) = data(1)
        do i = 2, n
            smoothed(i) = alpha * data(i) + (1.0_real64 - alpha) * smoothed(i-1)
        end do

    end function exponential_smoothing

    function cumulative_sum(data) result(cumsum)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64), dimension(:), allocatable :: cumsum
        integer(int32) :: i, n

        n = size(data)
        allocate(cumsum(n))

        if (n > 0) then
            cumsum(1) = data(1)
            do i = 2, n
                cumsum(i) = cumsum(i-1) + data(i)
            end do
        end if

    end function cumulative_sum

    function cumulative_product(data) result(cumprod)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64), dimension(:), allocatable :: cumprod
        integer(int32) :: i, n

        n = size(data)
        allocate(cumprod(n))

        if (n > 0) then
            cumprod(1) = data(1)
            do i = 2, n
                cumprod(i) = cumprod(i-1) * data(i)
            end do
        end if

    end function cumulative_product

    function autocorrelation(data, lag) result(acf)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        integer(int32), intent(in) :: lag
        real(real64) :: acf
        real(real64) :: mean_data, var_data
        integer(int32) :: n, i

        n = size(data)
        if (lag >= n .or. lag < 0) then
            acf = 0.0_real64
            return
        end if

        mean_data = mean(data)
        var_data = variance(data)

        if (var_data < EPSILON) then
            acf = 0.0_real64
            return
        end if

        acf = 0.0_real64
        do i = 1, n - lag
            acf = acf + (data(i) - mean_data) * (data(i + lag) - mean_data)
        end do

        acf = acf / (var_data * real(n - lag, real64))

    end function autocorrelation

    function cross_correlation(x, y, lag) result(ccf)
        implicit none
        real(real64), dimension(:), intent(in) :: x, y
        integer(int32), intent(in) :: lag
        real(real64) :: ccf
        real(real64) :: mean_x, mean_y, std_x, std_y
        integer(int32) :: n, i

        n = min(size(x), size(y))
        if (abs(lag) >= n) then
            ccf = 0.0_real64
            return
        end if

        mean_x = mean(x(1:n))
        mean_y = mean(y(1:n))
        std_x = std_dev(x(1:n))
        std_y = std_dev(y(1:n))

        if (std_x < EPSILON .or. std_y < EPSILON) then
            ccf = 0.0_real64
            return
        end if

        ccf = 0.0_real64
        if (lag >= 0) then
            do i = 1, n - lag
                ccf = ccf + (x(i) - mean_x) * (y(i + lag) - mean_y)
            end do
            ccf = ccf / (std_x * std_y * real(n - lag, real64))
        else
            do i = 1, n + lag
                ccf = ccf + (x(i - lag) - mean_x) * (y(i) - mean_y)
            end do
            ccf = ccf / (std_x * std_y * real(n + lag, real64))
        end if

    end function cross_correlation

    !===============================================
    ! Statistical Tests
    !===============================================

    function z_score(x, mean_val, std_val) result(z)
        implicit none
        real(real64), intent(in) :: x, mean_val, std_val
        real(real64) :: z

        if (std_val < EPSILON) then
            z = 0.0_real64
        else
            z = (x - mean_val) / std_val
        end if

    end function z_score

    function t_score(x, mean_val, std_val, n) result(t)
        implicit none
        real(real64), intent(in) :: x, mean_val, std_val
        integer(int32), intent(in) :: n
        real(real64) :: t

        if (std_val < EPSILON .or. n <= 0) then
            t = 0.0_real64
        else
            t = (x - mean_val) / (std_val / sqrt(real(n, real64)))
        end if

    end function t_score

    function chi_square_test(observed, expected) result(chi2)
        implicit none
        real(real64), dimension(:), intent(in) :: observed, expected
        real(real64) :: chi2
        integer(int32) :: i, n

        n = size(observed)
        if (n /= size(expected) .or. n == 0) then
            chi2 = 0.0_real64
            return
        end if

        chi2 = 0.0_real64
        do i = 1, n
            if (expected(i) > EPSILON) then
                chi2 = chi2 + (observed(i) - expected(i))**2 / expected(i)
            end if
        end do

    end function chi_square_test

    function t_test(sample1, sample2, paired) result(t_stat)
        implicit none
        real(real64), dimension(:), intent(in) :: sample1, sample2
        logical, intent(in), optional :: paired
        real(real64) :: t_stat
        real(real64) :: mean1, mean2, var1, var2
        integer(int32) :: n1, n2
        logical :: is_paired

        if (present(paired)) then
            is_paired = paired
        else
            is_paired = .false.
        end if

        n1 = size(sample1)
        n2 = size(sample2)

        if (is_paired) then
            if (n1 /= n2) then
                t_stat = 0.0_real64
                return
            end if

            ! Paired t-test
            t_stat = mean(sample1 - sample2) / &
                    (std_dev(sample1 - sample2) / sqrt(real(n1, real64)))
        else
            ! Independent samples t-test
            mean1 = mean(sample1)
            mean2 = mean(sample2)
            var1 = variance(sample1, 1)
            var2 = variance(sample2, 1)

            t_stat = (mean1 - mean2) / &
                    sqrt(var1/real(n1, real64) + var2/real(n2, real64))
        end if

    end function t_test

    !===============================================
    ! Clustering
    !===============================================

    function k_means_clustering(data, k, max_iter) result(result)
        implicit none
        real(real64), dimension(:,:), intent(in) :: data
        integer(int32), intent(in) :: k
        integer(int32), intent(in), optional :: max_iter
        type(cluster_result) :: result
        real(real64), dimension(:,:), allocatable :: centers
        integer(int32), dimension(:), allocatable :: labels
        real(real64), dimension(:), allocatable :: distances
        integer(int32) :: n, d, iter, max_iterations
        integer(int32) :: i, j, closest
        real(real64) :: min_dist, dist
        logical :: converged

        n = size(data, 1)
        d = size(data, 2)

        if (present(max_iter)) then
            max_iterations = max_iter
        else
            max_iterations = 100
        end if

        allocate(centers(k, d))
        allocate(labels(n))
        allocate(distances(k))

        ! Initialize centers randomly (simplified - should use better method)
        do i = 1, k
            centers(i, :) = data(i, :)
        end do

        ! Iterate until convergence
        do iter = 1, max_iterations
            converged = .true.

            ! Assign points to nearest center
            do i = 1, n
                min_dist = huge(1.0_real64)
                closest = 1

                do j = 1, k
                    dist = sum((data(i, :) - centers(j, :))**2)
                    if (dist < min_dist) then
                        min_dist = dist
                        closest = j
                    end if
                end do

                if (labels(i) /= closest) then
                    converged = .false.
                    labels(i) = closest
                end if
            end do

            if (converged) exit

            ! Update centers
            do j = 1, k
                centers(j, :) = 0.0_real64
                do i = 1, n
                    if (labels(i) == j) then
                        centers(j, :) = centers(j, :) + data(i, :)
                    end if
                end do
                centers(j, :) = centers(j, :) / real(count(labels == j), real64)
            end do
        end do

        ! Calculate inertia
        result%inertia = 0.0_real64
        do i = 1, n
            result%inertia = result%inertia + sum((data(i, :) - centers(labels(i), :))**2)
        end do

        result%labels = labels
        result%centers = centers
        result%n_clusters = k

    end function k_means_clustering

    !===============================================
    ! Outlier Detection
    !===============================================

    function outlier_detection(data, method) result(outliers)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        character(len=*), intent(in), optional :: method
        logical, dimension(:), allocatable :: outliers
        character(len=20) :: detection_method
        real(real64), dimension(3) :: q
        real(real64) :: iqr_val, lower_bound, upper_bound
        real(real64) :: mean_val, std_val
        integer(int32) :: n, i

        n = size(data)
        allocate(outliers(n))
        outliers = .false.

        if (present(method)) then
            detection_method = method
        else
            detection_method = "iqr"
        end if

        select case (trim(detection_method))
            case ("iqr")
                q = quartiles(data)
                iqr_val = q(3) - q(1)
                lower_bound = q(1) - 1.5_real64 * iqr_val
                upper_bound = q(3) + 1.5_real64 * iqr_val

                do i = 1, n
                    if (data(i) < lower_bound .or. data(i) > upper_bound) then
                        outliers(i) = .true.
                    end if
                end do

            case ("zscore")
                mean_val = mean(data)
                std_val = std_dev(data)

                do i = 1, n
                    if (abs(z_score(data(i), mean_val, std_val)) > 3.0_real64) then
                        outliers(i) = .true.
                    end if
                end do

            case default
                ! Default to IQR method
                outliers = outlier_detection(data, "iqr")
        end select

    end function outlier_detection

    function box_plot_stats(data) result(stats)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64), dimension(7) :: stats  ! min, q1, median, q3, max, lower_fence, upper_fence
        real(real64), dimension(3) :: q
        real(real64) :: iqr_val

        q = quartiles(data)
        iqr_val = q(3) - q(1)

        stats(1) = minval(data)
        stats(2) = q(1)
        stats(3) = q(2)  ! median
        stats(4) = q(3)
        stats(5) = maxval(data)
        stats(6) = q(1) - 1.5_real64 * iqr_val  ! lower fence
        stats(7) = q(3) + 1.5_real64 * iqr_val  ! upper fence

    end function box_plot_stats

    !===============================================
    ! Information Theory
    !===============================================

    function entropy(probabilities) result(h)
        implicit none
        real(real64), dimension(:), intent(in) :: probabilities
        real(real64) :: h
        integer(int32) :: i

        h = 0.0_real64
        do i = 1, size(probabilities)
            if (probabilities(i) > EPSILON) then
                h = h - probabilities(i) * log(probabilities(i)) / log(2.0_real64)
            end if
        end do

    end function entropy

    function mutual_information(x, y) result(mi)
        implicit none
        real(real64), dimension(:), intent(in) :: x, y
        real(real64) :: mi
        ! Simplified implementation - should compute joint and marginal distributions
        mi = 0.0_real64

    end function mutual_information

    !===============================================
    ! Dimensionality Reduction (Stub)
    !===============================================

    function pca(data, n_components) result(transformed)
        implicit none
        real(real64), dimension(:,:), intent(in) :: data
        integer(int32), intent(in) :: n_components
        real(real64), dimension(:,:), allocatable :: transformed

        ! Simplified PCA implementation stub
        allocate(transformed(size(data, 1), n_components))
        transformed = 0.0_real64

    end function pca

    !===============================================
    ! Helper Functions
    !===============================================

    subroutine sort_array(arr)
        implicit none
        real(real64), dimension(:), intent(inout) :: arr
        integer(int32) :: i, j, n
        real(real64) :: temp

        n = size(arr)
        ! Simple bubble sort
        do i = 1, n-1
            do j = 1, n-i
                if (arr(j) > arr(j+1)) then
                    temp = arr(j)
                    arr(j) = arr(j+1)
                    arr(j+1) = temp
                end if
            end do
        end do

    end subroutine sort_array

    function compute_ranks(data) result(ranks)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64), dimension(:), allocatable :: ranks
        real(real64), dimension(:), allocatable :: sorted_data
        integer(int32), dimension(:), allocatable :: indices
        integer(int32) :: n, i, j
        real(real64) :: current_value, rank_sum
        integer(int32) :: count

        n = size(data)
        allocate(ranks(n))
        allocate(sorted_data(n))
        allocate(indices(n))

        ! Create index array
        do i = 1, n
            indices(i) = i
        end do

        ! Sort data with indices
        sorted_data = data
        call sort_with_indices(sorted_data, indices)

        ! Assign ranks
        i = 1
        do while (i <= n)
            current_value = sorted_data(i)
            count = 1
            rank_sum = real(i, real64)

            ! Handle ties
            do j = i + 1, n
                if (abs(sorted_data(j) - current_value) < EPSILON) then
                    count = count + 1
                    rank_sum = rank_sum + real(j, real64)
                else
                    exit
                end if
            end do

            ! Assign average rank for ties
            do j = i, i + count - 1
                ranks(indices(j)) = rank_sum / real(count, real64)
            end do

            i = i + count
        end do

        deallocate(sorted_data, indices)

    end function compute_ranks

    subroutine sort_with_indices(arr, indices)
        implicit none
        real(real64), dimension(:), intent(inout) :: arr
        integer(int32), dimension(:), intent(inout) :: indices
        integer(int32) :: i, j, n, temp_idx
        real(real64) :: temp_val

        n = size(arr)
        ! Simple bubble sort with indices
        do i = 1, n-1
            do j = 1, n-i
                if (arr(j) > arr(j+1)) then
                    temp_val = arr(j)
                    arr(j) = arr(j+1)
                    arr(j+1) = temp_val

                    temp_idx = indices(j)
                    indices(j) = indices(j+1)
                    indices(j+1) = temp_idx
                end if
            end do
        end do

    end subroutine sort_with_indices

    subroutine find_unique_with_counts(data, unique_vals, counts, n_unique)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64), dimension(:), intent(out) :: unique_vals
        integer(int32), dimension(:), intent(out) :: counts
        integer(int32), intent(out) :: n_unique
        integer(int32) :: i, j, n
        logical :: found

        n = size(data)
        n_unique = 0

        do i = 1, n
            found = .false.
            do j = 1, n_unique
                if (abs(data(i) - unique_vals(j)) < EPSILON) then
                    counts(j) = counts(j) + 1
                    found = .true.
                    exit
                end if
            end do

            if (.not. found) then
                n_unique = n_unique + 1
                unique_vals(n_unique) = data(i)
                counts(n_unique) = 1
            end if
        end do

    end subroutine find_unique_with_counts

    subroutine solve_linear_system(A, b, x)
        implicit none
        real(real64), dimension(:,:), intent(in) :: A
        real(real64), dimension(:), intent(in) :: b
        real(real64), dimension(:), intent(out) :: x
        ! Simplified linear solver - should use proper LAPACK routines
        x = b  ! Placeholder

    end subroutine solve_linear_system

    ! Additional stub functions

    function multiple_regression(X, y) result(result)
        implicit none
        real(real64), dimension(:,:), intent(in) :: X
        real(real64), dimension(:), intent(in) :: y
        type(regression_result) :: result

        allocate(result%coefficients(0))
        allocate(result%residuals(0))
        result%r_squared = 0.0_real64
        result%adjusted_r_squared = 0.0_real64
        result%standard_error = 0.0_real64

    end function multiple_regression

    function ridge_regression(X, y, alpha) result(result)
        implicit none
        real(real64), dimension(:,:), intent(in) :: X
        real(real64), dimension(:), intent(in) :: y
        real(real64), intent(in) :: alpha
        type(regression_result) :: result

        allocate(result%coefficients(0))
        allocate(result%residuals(0))
        result%r_squared = 0.0_real64
        result%adjusted_r_squared = 0.0_real64
        result%standard_error = 0.0_real64

    end function ridge_regression

    function anova(groups) result(f_stat)
        implicit none
        real(real64), dimension(:,:), intent(in) :: groups
        real(real64) :: f_stat

        f_stat = 0.0_real64

    end function anova

    function f_test(sample1, sample2) result(f_stat)
        implicit none
        real(real64), dimension(:), intent(in) :: sample1, sample2
        real(real64) :: f_stat

        f_stat = variance(sample1) / variance(sample2)

    end function f_test

    function kolmogorov_smirnov_test(sample1, sample2) result(ks_stat)
        implicit none
        real(real64), dimension(:), intent(in) :: sample1, sample2
        real(real64) :: ks_stat

        ks_stat = 0.0_real64

    end function kolmogorov_smirnov_test

    function shapiro_wilk_test(data) result(w_stat)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64) :: w_stat

        w_stat = 0.0_real64

    end function shapiro_wilk_test

    function confidence_interval(data, confidence_level) result(ci)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        real(real64), intent(in) :: confidence_level
        real(real64), dimension(2) :: ci

        ci = [0.0_real64, 0.0_real64]

    end function confidence_interval

    function bootstrap(data, n_samples, statistic) result(boot_stats)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        integer(int32), intent(in) :: n_samples
        interface
            function statistic(x) result(stat)
                use iso_fortran_env, only: real64
                real(real64), dimension(:), intent(in) :: x
                real(real64) :: stat
            end function statistic
        end interface
        real(real64), dimension(:), allocatable :: boot_stats

        allocate(boot_stats(n_samples))
        boot_stats = 0.0_real64

    end function bootstrap

    function histogram(data, n_bins) result(hist)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        integer(int32), intent(in) :: n_bins
        integer(int32), dimension(:), allocatable :: hist

        allocate(hist(n_bins))
        hist = 0

    end function histogram

    function frequency_table(data) result(freqs)
        implicit none
        integer(int32), dimension(:), intent(in) :: data
        integer(int32), dimension(:,:), allocatable :: freqs

        allocate(freqs(0, 2))

    end function frequency_table

    function factor_analysis(data, n_factors) result(factors)
        implicit none
        real(real64), dimension(:,:), intent(in) :: data
        integer(int32), intent(in) :: n_factors
        real(real64), dimension(:,:), allocatable :: factors

        allocate(factors(size(data, 1), n_factors))
        factors = 0.0_real64

    end function factor_analysis

    function hierarchical_clustering(data, method) result(result)
        implicit none
        real(real64), dimension(:,:), intent(in) :: data
        character(len=*), intent(in), optional :: method
        type(cluster_result) :: result

        allocate(result%labels(size(data, 1)))
        allocate(result%centers(1, size(data, 2)))
        result%labels = 1
        result%centers = 0.0_real64
        result%n_clusters = 1
        result%inertia = 0.0_real64

    end function hierarchical_clustering

    function time_series_decomposition(data, period) result(components)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        integer(int32), intent(in) :: period
        type(time_series_components) :: components

        allocate(components%trend(size(data)))
        allocate(components%seasonal(size(data)))
        allocate(components%residual(size(data)))

        components%trend = 0.0_real64
        components%seasonal = 0.0_real64
        components%residual = data

    end function time_series_decomposition

    function fourier_analysis(data) result(spectrum)
        implicit none
        real(real64), dimension(:), intent(in) :: data
        complex(real64), dimension(:), allocatable :: spectrum

        allocate(spectrum(size(data)))
        spectrum = cmplx(0.0_real64, 0.0_real64, real64)

    end function fourier_analysis

end module statistics_module