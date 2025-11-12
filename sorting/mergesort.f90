! MergeSort Implementation in Modern Fortran
!
! MergeSort is a divide-and-conquer sorting algorithm.
! Time Complexity: O(n log n) - all cases
! Space Complexity: O(n) - requires auxiliary array
!
! Features:
! - Stable sorting algorithm
! - Guaranteed O(n log n) performance
! - Top-down recursive implementation

program mergesort_demo
    implicit none

    integer, parameter :: n1 = 10, n2 = 15, n3 = 5000
    integer :: arr1(n1), arr2(n2), arr3(n3)
    real(8) :: start_time, end_time
    integer :: i

    print '(A)', repeat('=', 70)
    print '(A)', '                MERGESORT IN FORTRAN'
    print '(A)', repeat('=', 70)
    print *

    ! Test 1: Small array
    print '(A)', 'Test 1: Small integer array'
    print '(A)', repeat('-', 70)
    arr1 = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]

    print '(A)', 'Original: '
    call print_array(arr1, n1)

    call mergesort(arr1, 1, n1)

    print '(A)', 'Sorted:   '
    call print_array(arr1, n1)

    if (is_sorted(arr1, n1)) then
        print '(A)', '✓ Array is sorted correctly'
    else
        print '(A)', '✗ Sorting failed!'
    end if
    print *

    ! Test 2: Array with duplicates (stability test)
    print '(A)', 'Test 2: Array with duplicates (stability test)'
    print '(A)', repeat('-', 70)
    arr2 = [5, 2, 8, 2, 9, 1, 5, 5, 2, 8, 3, 7, 4, 6, 1]

    print '(A)', 'Original: '
    call print_array(arr2, n2)

    call mergesort(arr2, 1, n2)

    print '(A)', 'Sorted:   '
    call print_array(arr2, n2)

    if (is_sorted(arr2, n2)) then
        print '(A)', '✓ Array is sorted correctly'
        print '(A)', 'Note: MergeSort is stable (preserves order of equal elements)'
    else
        print '(A)', '✗ Sorting failed!'
    end if
    print *

    ! Performance benchmark
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
    call mergesort(arr3, 1, n3)
    call cpu_time(end_time)

    if (is_sorted(arr3, n3)) then
        print '(A, F10.6, A)', '✓ Sorted correctly in ', end_time - start_time, ' seconds'
    else
        print '(A)', '✗ Sorting failed!'
    end if
    print *

    ! Summary
    print '(A)', repeat('=', 70)
    print '(A)', 'Key Points:'
    print '(A)', '- Time Complexity: O(n log n) for all cases'
    print '(A)', '- Space Complexity: O(n) - needs temporary array'
    print '(A)', '- Stable: maintains relative order of equal elements'
    print '(A)', '- Predictable performance (no worst case)'
    print '(A)', '- Excellent for linked lists'
    print '(A)', '- Used in external sorting (when data doesnt fit in memory)'
    print '(A)', repeat('=', 70)

contains

    ! ===================================================================
    ! MERGESORT - TOP-DOWN RECURSIVE
    ! ===================================================================

    recursive subroutine mergesort(arr, left, right)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: left, right
        integer :: mid

        if (left < right) then
            ! Find middle point
            mid = left + (right - left) / 2

            ! Sort first and second halves
            call mergesort(arr, left, mid)
            call mergesort(arr, mid + 1, right)

            ! Merge the sorted halves
            call merge(arr, left, mid, right)
        end if
    end subroutine mergesort

    ! ===================================================================
    ! MERGE - Combines two sorted subarrays
    ! ===================================================================

    subroutine merge(arr, left, mid, right)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: left, mid, right
        integer :: n1, n2, i, j, k
        integer, allocatable :: L(:), R(:)

        n1 = mid - left + 1
        n2 = right - mid

        ! Allocate temporary arrays
        allocate(L(n1), R(n2))

        ! Copy data to temporary arrays
        L = arr(left:mid)
        R = arr(mid+1:right)

        ! Merge the temporary arrays back into arr
        i = 1
        j = 1
        k = left

        do while (i <= n1 .and. j <= n2)
            if (L(i) <= R(j)) then  ! <= ensures stability
                arr(k) = L(i)
                i = i + 1
            else
                arr(k) = R(j)
                j = j + 1
            end if
            k = k + 1
        end do

        ! Copy remaining elements of L if any
        do while (i <= n1)
            arr(k) = L(i)
            i = i + 1
            k = k + 1
        end do

        ! Copy remaining elements of R if any
        do while (j <= n2)
            arr(k) = R(j)
            j = j + 1
            k = k + 1
        end do

        deallocate(L, R)
    end subroutine merge

    ! ===================================================================
    ! UTILITY FUNCTIONS
    ! ===================================================================

    subroutine print_array(arr, n)
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
    end subroutine print_array

    function is_sorted(arr, n) result(sorted)
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
    end function is_sorted

end program mergesort_demo
