! Example program demonstrating statistics algorithms
program statistics_example
    use iso_fortran_env, only: int32, real64
    use statistics_module
    implicit none

    real(real64), allocatable :: data(:), data2(:)
    real(real64) :: result, slope, intercept, r_squared
    type(hypothesis_test_result) :: test_result
    integer :: i

    print '(A)', "========================================"
    print '(A)', "    Statistics Algorithms Examples"
    print '(A)', "========================================"

    ! Example 1: Descriptive statistics
    print '(A)', ""
    print '(A)', "Example 1: Descriptive Statistics"
    print '(A)', "----------------------------------"

    ! Generate sample data
    allocate(data(20))
    data = [12.5, 14.2, 13.8, 15.1, 14.7, 13.3, 14.9, 15.5, &
            13.9, 14.4, 15.2, 14.0, 13.6, 14.8, 15.3, 14.1, &
            13.7, 14.6, 15.0, 14.3]

    print '(A)', "Data sample (n=20):"
    print '(5F8.2)', data

    result = mean(data)
    print '(A,F8.3)', "Mean: ", result

    result = median(data)
    print '(A,F8.3)', "Median: ", result

    result = std_dev(data)
    print '(A,F8.3)', "Standard deviation: ", result

    result = variance(data)
    print '(A,F8.3)', "Variance: ", result

    result = percentile(data, 0.25_real64)
    print '(A,F8.3)', "25th percentile: ", result

    result = percentile(data, 0.75_real64)
    print '(A,F8.3)', "75th percentile: ", result

    ! Example 2: Hypothesis testing
    print '(A)', ""
    print '(A)', "Example 2: Hypothesis Testing"
    print '(A)', "------------------------------"

    ! One-sample t-test (test if mean = 14.0)
    test_result = t_test_one_sample(data, 14.0_real64)
    print '(A)', "One-sample t-test (H0: μ = 14.0):"
    print '(A,F8.3)', "  t-statistic: ", test_result%t_statistic
    print '(A,F8.4)', "  p-value: ", test_result%p_value
    if (test_result%p_value < 0.05) then
        print '(A)', "  Result: Reject null hypothesis (p < 0.05)"
    else
        print '(A)', "  Result: Fail to reject null hypothesis (p >= 0.05)"
    end if

    ! Two-sample t-test
    allocate(data2(20))
    data2 = data + 0.5_real64  ! Slightly higher values

    test_result = t_test_two_sample(data, data2)
    print '(A)', ""
    print '(A)', "Two-sample t-test:"
    print '(A,F8.3)', "  t-statistic: ", test_result%t_statistic
    print '(A,F8.4)', "  p-value: ", test_result%p_value

    ! Example 3: Linear regression
    print '(A)', ""
    print '(A)', "Example 3: Linear Regression"
    print '(A)', "-----------------------------"

    ! Create data with linear relationship
    deallocate(data, data2)
    allocate(data(50), data2(50))

    ! X values: 1 to 50
    do i = 1, 50
        data(i) = real(i, real64)
        ! Y = 2X + 10 + noise
        data2(i) = 2.0 * data(i) + 10.0 + 0.5 * sin(real(i, real64))
    end do

    call linear_regression(data, data2, slope, intercept, r_squared)

    print '(A)', "Linear regression: Y = aX + b"
    print '(A,F8.3)', "  Slope (a): ", slope
    print '(A,F8.3)', "  Intercept (b): ", intercept
    print '(A,F8.4)', "  R-squared: ", r_squared

    ! Example 4: Correlation analysis
    print '(A)', ""
    print '(A)', "Example 4: Correlation Analysis"
    print '(A)', "--------------------------------"

    result = correlation(data, data2)
    print '(A,F8.4)', "Pearson correlation coefficient: ", result

    if (abs(result) > 0.8) then
        print '(A)', "Interpretation: Strong correlation"
    else if (abs(result) > 0.5) then
        print '(A)', "Interpretation: Moderate correlation"
    else if (abs(result) > 0.3) then
        print '(A)', "Interpretation: Weak correlation"
    else
        print '(A)', "Interpretation: Very weak or no correlation"
    end if

    ! Example 5: Time series analysis
    print '(A)', ""
    print '(A)', "Example 5: Time Series Analysis"
    print '(A)', "--------------------------------"

    ! Generate time series data
    deallocate(data)
    allocate(data(100))
    do i = 1, 100
        data(i) = 100.0 + 0.5 * i + 10.0 * sin(0.2 * i) + 2.0 * randn()
    end do

    ! Moving average
    call demonstrate_moving_average(data)

    ! Example 6: K-means clustering
    print '(A)', ""
    print '(A)', "Example 6: K-means Clustering"
    print '(A)', "------------------------------"

    call demonstrate_clustering()

    ! Clean up
    deallocate(data, data2)

    print '(A)', ""
    print '(A)', "========================================"
    print '(A)', "    Statistics Examples Complete"
    print '(A)', "========================================"

contains

    real(real64) function randn()
        ! Simple normal random number generator
        real(real64) :: u1, u2
        call random_number(u1)
        call random_number(u2)
        randn = sqrt(-2.0 * log(u1)) * cos(2.0 * 3.14159265359 * u2)
    end function randn

    subroutine demonstrate_moving_average(series)
        real(real64), intent(in) :: series(:)
        real(real64), allocatable :: ma(:)
        integer :: window_size

        window_size = 5
        allocate(ma(size(series) - window_size + 1))

        call moving_average(series, window_size, ma)

        print '(A,I0,A)', "Moving average (window=", window_size, "):"
        print '(A)', "First 10 original values:"
        print '(5F8.2)', series(1:10)
        print '(A)', "First 6 smoothed values:"
        print '(5F8.2)', ma(1:6)

        deallocate(ma)
    end subroutine demonstrate_moving_average

    subroutine demonstrate_clustering()
        real(real64), allocatable :: points(:,:), centers(:,:)
        integer, allocatable :: labels(:)
        integer :: n_points, n_clusters, i

        n_points = 30
        n_clusters = 3

        allocate(points(n_points, 2))
        allocate(centers(n_clusters, 2))
        allocate(labels(n_points))

        ! Generate clustered data
        ! Cluster 1 around (0, 0)
        do i = 1, 10
            points(i, 1) = randn() * 0.5
            points(i, 2) = randn() * 0.5
        end do

        ! Cluster 2 around (3, 3)
        do i = 11, 20
            points(i, 1) = 3.0 + randn() * 0.5
            points(i, 2) = 3.0 + randn() * 0.5
        end do

        ! Cluster 3 around (-2, 2)
        do i = 21, 30
            points(i, 1) = -2.0 + randn() * 0.5
            points(i, 2) = 2.0 + randn() * 0.5
        end do

        ! Perform k-means clustering
        call k_means_clustering(points, n_clusters, labels, centers)

        print '(A,I0,A)', "K-means clustering with ", n_clusters, " clusters:"
        print '(A)', "Cluster centers:"
        do i = 1, n_clusters
            print '(A,I0,A,2F8.3)', "  Cluster ", i, ": ", centers(i, :)
        end do

        print '(A)', "Sample point assignments (first 10):"
        print '(10I3)', labels(1:10)

        deallocate(points, centers, labels)
    end subroutine demonstrate_clustering

end program statistics_example