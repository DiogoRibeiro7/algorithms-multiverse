! QuickSort Implementation in Modern Fortran
!
! QuickSort is a divide-and-conquer sorting algorithm.
! Average Time Complexity: O(n log n)
! Worst Case: O(n²) - when pivot selection is poor
! Space Complexity: O(log n) - recursion stack
!
! Features:
! - In-place sorting
! - Randomized pivot selection
! - Handles integer and real arrays

program quicksort_demo
    implicit none

    ! Test arrays
    integer, parameter :: n1 = 10, n2 = 20, n3 = 1000
    integer :: arr1(n1), arr2(n2), arr3(n3)
    real(8) :: start_time, end_time
    integer :: i

    print '(A)', repeat('=', 70)
    print '(A)', '                QUICKSORT IN FORTRAN'
    print '(A)', repeat('=', 70)
    print *

    ! Test 1: Small integer array
    print '(A)', 'Test 1: Small integer array'
    print '(A)', repeat('-', 70)
    arr1 = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]

    print '(A)', 'Original: '
    call print_array_int(arr1, n1)

    call quicksort_int(arr1, 1, n1)

    print '(A)', 'Sorted:   '
    call print_array_int(arr1, n1)

    if (is_sorted_int(arr1, n1)) then
        print '(A)', '✓ Array is sorted correctly'
    else
        print '(A)', '✗ Sorting failed!'
    end if
    print *

    ! Test 2: Array with duplicates
    print '(A)', 'Test 2: Array with duplicates'
    print '(A)', repeat('-', 70)
    arr2 = [5, 2, 8, 2, 9, 1, 5, 5, 2, 8, 3, 7, 4, 6, 1, 9, 3, 7, 4, 6]

    print '(A)', 'Original: '
    call print_array_int(arr2, n2)

    call quicksort_random_int(arr2, 1, n2)

    print '(A)', 'Sorted:   '
    call print_array_int(arr2, n2)

    if (is_sorted_int(arr2, n2)) then
        print '(A)', '✓ Array is sorted correctly'
    else
        print '(A)', '✗ Sorting failed!'
    end if
    print *

    ! Benchmark with larger array
    print '(A)', 'Performance Benchmark'
    print '(A)', repeat('=', 70)
    print '(A, I0, A)', 'Array size: ', n3, ' elements'
    print '(A)', repeat('-', 70)

    ! Initialize random array
    call random_seed()
    do i = 1, n3
        call random_number(start_time)
        arr3(i) = int(start_time * 10000)
    end do

    ! Benchmark
    call cpu_time(start_time)
    call quicksort_random_int(arr3, 1, n3)
    call cpu_time(end_time)

    if (is_sorted_int(arr3, n3)) then
        print '(A, F10.6, A)', '✓ Sorted correctly in ', end_time - start_time, ' seconds'
    else
        print '(A)', '✗ Sorting failed!'
    end if
    print *

    ! Summary
    print '(A)', repeat('=', 70)
    print '(A)', 'Key Points:'
    print '(A)', '- Average Time: O(n log n)'
    print '(A)', '- Worst Case: O(n²) with poor pivot selection'
    print '(A)', '- Space: O(log n) for recursion stack'
    print '(A)', '- In-place sorting algorithm'
    print '(A)', '- Not stable: equal elements may be reordered'
    print '(A)', '- Randomized pivot prevents worst-case on sorted input'
    print '(A)', repeat('=', 70)

contains

    ! ===================================================================
    ! QUICKSORT FOR INTEGERS
    ! ===================================================================

    recursive subroutine quicksort_int(arr, left, right)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: left, right
        integer :: pivot_idx

        if (left < right) then
            pivot_idx = partition_int(arr, left, right)
            call quicksort_int(arr, left, pivot_idx - 1)
            call quicksort_int(arr, pivot_idx + 1, right)
        end if
    end subroutine quicksort_int

    function partition_int(arr, left, right) result(pivot_idx)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: left, right
        integer :: pivot_idx
        integer :: pivot, i, j, temp

        pivot = arr(right)
        i = left - 1

        do j = left, right - 1
            if (arr(j) <= pivot) then
                i = i + 1
                ! Swap arr(i) and arr(j)
                temp = arr(i)
                arr(i) = arr(j)
                arr(j) = temp
            end if
        end do

        ! Swap arr(i+1) and arr(right)
        temp = arr(i + 1)
        arr(i + 1) = arr(right)
        arr(right) = temp

        pivot_idx = i + 1
    end function partition_int

    ! ===================================================================
    ! RANDOMIZED QUICKSORT
    ! ===================================================================

    recursive subroutine quicksort_random_int(arr, left, right)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: left, right
        integer :: pivot_idx

        if (left < right) then
            pivot_idx = partition_random_int(arr, left, right)
            call quicksort_random_int(arr, left, pivot_idx - 1)
            call quicksort_random_int(arr, pivot_idx + 1, right)
        end if
    end subroutine quicksort_random_int

    function partition_random_int(arr, left, right) result(pivot_idx)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: left, right
        integer :: pivot_idx
        integer :: random_idx, temp
        real :: r

        ! Choose random pivot
        call random_number(r)
        random_idx = left + int(r * (right - left + 1))
        if (random_idx > right) random_idx = right

        ! Swap random element with rightmost
        temp = arr(random_idx)
        arr(random_idx) = arr(right)
        arr(right) = temp

        ! Use standard partition
        pivot_idx = partition_int(arr, left, right)
    end function partition_random_int

    ! ===================================================================
    ! UTILITY FUNCTIONS
    ! ===================================================================

    subroutine print_array_int(arr, n)
        integer, intent(in) :: arr(:), n
        integer :: i

        write(*, '(A)', advance='no') '['
        do i = 1, n
            if (i < n) then
                write(*, '(I0, A)', advance='no') arr(i), ', '
            else
                write(*, '(I0)', advance='no') arr(i)
            end if
        end do
        write(*, '(A)') ']'
    end subroutine print_array_int

    function is_sorted_int(arr, n) result(sorted)
        integer, intent(in) :: arr(:), n
        logical :: sorted
        integer :: i

        sorted = .true.
        do i = 1, n - 1
            if (arr(i) > arr(i + 1)) then
                sorted = .false.
                return
            end if
        end do
    end function is_sorted_int

end program quicksort_demo
