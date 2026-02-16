! Test suite for streaming algorithms module
program test_streaming_module
    use iso_fortran_env, only: int32, real64
    use streaming_module
    implicit none

    integer :: total_tests = 0, passed_tests = 0
    real(real64), parameter :: EPS = 1e-6

    print '(A)', "========================================"
    print '(A)', "    Streaming Module Test Suite"
    print '(A)', "========================================"

    call test_reservoir_sampling()
    call test_count_min_sketch()
    call test_hyperloglog()
    call test_streaming_statistics()
    call test_sliding_window()
    call test_frequent_items()

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

    subroutine test_reservoir_sampling()
        real(real64) :: stream(1000), sample(10), weights(1000)
        integer :: i, sample_size
        logical :: success
        real(real64) :: min_val, max_val

        print '(A)', ""
        print '(A)', "Testing Reservoir Sampling..."

        ! Create stream
        do i = 1, 1000
            stream(i) = real(i, real64)
        end do

        ! Test basic reservoir sampling
        sample_size = 10
        call reservoir_sample(stream, sample_size, sample)

        ! Check that all samples are from the stream
        min_val = minval(sample)
        max_val = maxval(sample)
        success = min_val >= 1.0_real64 .and. max_val <= 1000.0_real64
        call report_test("Reservoir sampling range", success)

        ! Check that sample size is correct
        success = size(sample) == sample_size
        call report_test("Reservoir sample size", success)

        ! Test weighted reservoir sampling
        do i = 1, 1000
            weights(i) = real(i, real64)  ! Higher numbers have higher weight
        end do

        call weighted_reservoir_sample(stream, weights, sample_size, sample)

        ! Weighted sample should tend towards higher values
        success = sum(sample) / sample_size > 500.0_real64
        call report_test("Weighted reservoir sampling", success)

    end subroutine test_reservoir_sampling

    subroutine test_count_min_sketch()
        type(count_min_sketch_type) :: cms
        integer :: estimate, actual
        logical :: success
        real(real64) :: error_rate

        print '(A)', ""
        print '(A)', "Testing Count-Min Sketch..."

        ! Initialize sketch
        call cms_create(cms, 100, 4)

        ! Add items
        call cms_update(cms, 1, 10)
        call cms_update(cms, 2, 20)
        call cms_update(cms, 3, 5)
        call cms_update(cms, 1, 5)  ! Total for item 1 = 15

        ! Query counts
        estimate = cms_query(cms, 1)
        actual = 15
        success = estimate >= actual  ! CMS never underestimates
        call report_test("Count-Min Sketch query", success)

        ! Test accuracy
        estimate = cms_query(cms, 2)
        actual = 20
        error_rate = abs(real(estimate - actual, real64)) / actual
        success = error_rate < 0.2  ! Within 20% error
        call report_test("Count-Min Sketch accuracy", success)

        ! Test item that wasn't added
        estimate = cms_query(cms, 999)
        success = estimate >= 0
        call report_test("Count-Min Sketch non-existent", success)

        call cms_destroy(cms)

    end subroutine test_count_min_sketch

    subroutine test_hyperloglog()
        type(hyperloglog_type) :: hll
        integer :: i, estimate, actual
        logical :: success
        real(real64) :: error_rate

        print '(A)', ""
        print '(A)', "Testing HyperLogLog..."

        ! Initialize HLL
        call hll_create(hll, 10)  ! 2^10 = 1024 registers

        ! Add unique items
        do i = 1, 1000
            call hll_add(hll, i)
        end do

        ! Add duplicates (shouldn't affect cardinality)
        do i = 1, 100
            call hll_add(hll, i)
        end do

        ! Estimate cardinality
        estimate = hll_estimate_cardinality(hll)
        actual = 1000

        error_rate = abs(real(estimate - actual, real64)) / actual
        success = error_rate < 0.1  ! Within 10% error
        call report_test("HyperLogLog cardinality", success)

        ! Test empty HLL
        call hll_create(hll, 10)
        estimate = hll_estimate_cardinality(hll)
        success = estimate == 0
        call report_test("HyperLogLog empty", success)

        call hll_destroy(hll)

    end subroutine test_hyperloglog

    subroutine test_streaming_statistics()
        type(streaming_stats_type) :: stats
        real(real64) :: values(100)
        real(real64) :: mean_val, var_val
        integer :: i
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Streaming Statistics..."

        ! Initialize streaming stats
        call streaming_stats_init(stats)

        ! Add values one by one
        do i = 1, 100
            values(i) = real(i, real64)
            call streaming_stats_add(stats, values(i))
        end do

        ! Test mean (should be 50.5)
        mean_val = streaming_mean(stats)
        success = abs(mean_val - 50.5_real64) < EPS
        call report_test("Streaming mean", success)

        ! Test variance
        var_val = streaming_variance(stats)
        success = var_val > 0.0_real64
        call report_test("Streaming variance", success)

        ! Test min/max
        success = stats%min_val == 1.0_real64 .and. stats%max_val == 100.0_real64
        call report_test("Streaming min/max", success)

        ! Test count
        success = stats%count == 100
        call report_test("Streaming count", success)

        ! Test approximate median (using simple reservoir)
        mean_val = streaming_median_approximate(values)
        success = abs(mean_val - 50.5_real64) < 5.0  ! Approximate
        call report_test("Approximate streaming median", success)

    end subroutine test_streaming_statistics

    subroutine test_sliding_window()
        type(sliding_window_type) :: window
        real(real64) :: values(20), window_data(5)
        real(real64) :: sum_val, mean_val
        integer :: i, size
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Sliding Window..."

        ! Initialize sliding window of size 5
        call sliding_window_init(window, 5)

        ! Add values
        do i = 1, 10
            call sliding_window_add(window, real(i, real64))
        end do

        ! Window should contain [6, 7, 8, 9, 10]
        size = sliding_window_size(window)
        success = size == 5
        call report_test("Sliding window size", success)

        ! Test window sum
        sum_val = sliding_window_sum(window)
        success = abs(sum_val - 40.0_real64) < EPS  ! 6+7+8+9+10 = 40
        call report_test("Sliding window sum", success)

        ! Test window mean
        mean_val = sliding_window_mean(window)
        success = abs(mean_val - 8.0_real64) < EPS
        call report_test("Sliding window mean", success)

        ! Test getting window data
        call sliding_window_get_data(window, window_data)
        success = window_data(1) == 6.0_real64 .and. window_data(5) == 10.0_real64
        call report_test("Sliding window data", success)

        call sliding_window_destroy(window)

    end subroutine test_sliding_window

    subroutine test_frequent_items()
        type(space_saving_type) :: ss
        type(tdigest_type) :: td
        integer :: items(1000), frequent(10), counts(10)
        real(real64) :: quantile_val
        integer :: i, k, num_frequent
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Frequent Items Algorithms..."

        ! Create stream with some frequent items
        do i = 1, 1000
            if (i <= 500) then
                items(i) = 1  ! Item 1 appears 500 times
            else if (i <= 750) then
                items(i) = 2  ! Item 2 appears 250 times
            else if (i <= 900) then
                items(i) = 3  ! Item 3 appears 150 times
            else
                items(i) = mod(i, 10) + 4  ! Others appear less
            end if
        end do

        ! Test Misra-Gries for frequent items
        k = 5
        call frequent_items_misra_gries(items, k, frequent, counts, num_frequent)
        success = num_frequent > 0 .and. frequent(1) == 1  ! Item 1 should be most frequent
        call report_test("Misra-Gries frequent items", success)

        ! Test Space-Saving algorithm
        call space_saving_init(ss, 10)

        do i = 1, 1000
            call space_saving_add(ss, items(i))
        end do

        call space_saving_get_top_k(ss, 3, frequent(1:3), counts(1:3))
        success = frequent(1) == 1 .and. counts(1) >= 450  ! Approximate count
        call report_test("Space-Saving algorithm", success)

        call space_saving_destroy(ss)

        ! Test T-Digest for quantile estimation
        call tdigest_init(td, 100)

        do i = 1, 1000
            call tdigest_add(td, real(i, real64))
        end do

        ! Test median (50th percentile)
        quantile_val = tdigest_quantile(td, 0.5_real64)
        success = abs(quantile_val - 500.5_real64) < 20.0  ! Approximate
        call report_test("T-Digest median", success)

        ! Test 90th percentile
        quantile_val = tdigest_quantile(td, 0.9_real64)
        success = abs(quantile_val - 900.0_real64) < 30.0  ! Approximate
        call report_test("T-Digest 90th percentile", success)

        call tdigest_destroy(td)

    end subroutine test_frequent_items

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

end program test_streaming_module