! Advanced Search Algorithms in Modern Fortran
!
! Comprehensive collection of search algorithms:
! 1. Binary Search (iterative and recursive)
! 2. Interpolation Search
! 3. Jump Search
! 4. Exponential Search
! 5. Ternary Search
! 6. Fibonacci Search
!
! Author: Algorithms Multiverse

program advanced_search
    implicit none

    integer, parameter :: n = 1000
    integer :: arr(n), target, result
    integer :: i
    real(8) :: start_time, end_time

    print '(A)', repeat('=', 75)
    print '(A)', '            ADVANCED SEARCH ALGORITHMS IN FORTRAN'
    print '(A)', repeat('=', 75)
    print *

    ! Create sorted array
    do i = 1, n
        arr(i) = i * 2  ! Even numbers: 2, 4, 6, ..., 2000
    end do

    ! Run demonstrations
    call demo_binary_search(arr, n)
    call demo_interpolation_search(arr, n)
    call demo_jump_search(arr, n)
    call demo_exponential_search(arr, n)
    call demo_ternary_search()
    call demo_fibonacci_search(arr, n)

    ! Performance comparison
    call performance_comparison(arr, n)

    ! Summary
    print '(A)', repeat('=', 75)
    print '(A)', 'SEARCH ALGORITHM COMPLEXITY SUMMARY'
    print '(A)', repeat('=', 75)
    print '(A)', 'Algorithm           Best Case    Average      Worst Case   Space'
    print '(A)', repeat('-', 75)
    print '(A)', 'Binary Search       O(1)         O(log n)     O(log n)     O(1)'
    print '(A)', 'Interpolation       O(1)         O(log log n) O(n)         O(1)'
    print '(A)', 'Jump Search         O(1)         O(√n)        O(√n)        O(1)'
    print '(A)', 'Exponential         O(1)         O(log n)     O(log n)     O(1)'
    print '(A)', 'Ternary Search      O(1)         O(log₃ n)    O(log₃ n)    O(log n)'
    print '(A)', 'Fibonacci Search    O(1)         O(log n)     O(log n)     O(1)'
    print '(A)', repeat('=', 75)

contains

    ! ===================================================================
    ! BINARY SEARCH
    ! ===================================================================

    subroutine demo_binary_search(arr, n)
        integer, intent(in) :: arr(:), n
        integer :: target, result

        print '(A)', 'Test 1: Binary Search'
        print '(A)', repeat('-', 75)

        target = 500
        print '(A, I0)', 'Searching for: ', target

        ! Iterative version
        result = binary_search_iterative(arr, n, target)
        call print_result(result, target, "Iterative")

        ! Recursive version
        result = binary_search_recursive(arr, 1, n, target)
        call print_result(result, target, "Recursive")

        print *
        print '(A)', 'Complexity: O(log n)'
        print '(A)', 'Best for: Sorted arrays, most common search algorithm'
        print *
    end subroutine demo_binary_search

    function binary_search_iterative(arr, n, target) result(index)
        integer, intent(in) :: arr(:), n, target
        integer :: index, left, right, mid

        left = 1
        right = n

        do while (left <= right)
            mid = left + (right - left) / 2

            if (arr(mid) == target) then
                index = mid
                return
            else if (arr(mid) < target) then
                left = mid + 1
            else
                right = mid - 1
            end if
        end do

        index = -1  ! Not found
    end function binary_search_iterative

    recursive function binary_search_recursive(arr, left, right, target) result(index)
        integer, intent(in) :: arr(:), left, right, target
        integer :: index, mid

        if (right < left) then
            index = -1  ! Not found
            return
        end if

        mid = left + (right - left) / 2

        if (arr(mid) == target) then
            index = mid
        else if (arr(mid) < target) then
            index = binary_search_recursive(arr, mid + 1, right, target)
        else
            index = binary_search_recursive(arr, left, mid - 1, target)
        end if
    end function binary_search_recursive

    ! ===================================================================
    ! INTERPOLATION SEARCH
    ! ===================================================================

    subroutine demo_interpolation_search(arr, n)
        integer, intent(in) :: arr(:), n
        integer :: target, result

        print '(A)', 'Test 2: Interpolation Search'
        print '(A)', repeat('-', 75)

        target = 500
        print '(A, I0)', 'Searching for: ', target

        result = interpolation_search(arr, n, target)
        call print_result(result, target, "Interpolation")

        print *
        print '(A)', 'Complexity: O(log log n) for uniformly distributed data'
        print '(A)', 'Best for: Large sorted arrays with uniform distribution'
        print '(A)', 'Uses interpolation formula to estimate position'
        print *
    end subroutine demo_interpolation_search

    function interpolation_search(arr, n, target) result(index)
        integer, intent(in) :: arr(:), n, target
        integer :: index, low, high, pos

        low = 1
        high = n
        index = -1

        do while (low <= high .and. target >= arr(low) .and. target <= arr(high))
            if (low == high) then
                if (arr(low) == target) then
                    index = low
                end if
                return
            end if

            ! Interpolation formula
            pos = low + ((target - arr(low)) * (high - low)) / (arr(high) - arr(low))

            ! Ensure pos is within bounds
            if (pos < low) pos = low
            if (pos > high) pos = high

            if (arr(pos) == target) then
                index = pos
                return
            else if (arr(pos) < target) then
                low = pos + 1
            else
                high = pos - 1
            end if
        end do
    end function interpolation_search

    ! ===================================================================
    ! JUMP SEARCH
    ! ===================================================================

    subroutine demo_jump_search(arr, n)
        integer, intent(in) :: arr(:), n
        integer :: target, result

        print '(A)', 'Test 3: Jump Search'
        print '(A)', repeat('-', 75)

        target = 500
        print '(A, I0)', 'Searching for: ', target

        result = jump_search(arr, n, target)
        call print_result(result, target, "Jump")

        print *
        print '(A)', 'Complexity: O(√n)'
        print '(A)', 'Best for: Sorted arrays when binary search overhead is high'
        print '(A)', 'Jump size: √n for optimal performance'
        print *
    end subroutine demo_jump_search

    function jump_search(arr, n, target) result(index)
        integer, intent(in) :: arr(:), n, target
        integer :: index, step, prev, i

        step = int(sqrt(real(n)))
        prev = 1
        index = -1

        ! Find block where element may be present
        do while (arr(min(step, n)) < target)
            prev = step
            step = step + int(sqrt(real(n)))
            if (prev >= n) return
        end do

        ! Linear search in block
        do i = prev, min(step, n)
            if (arr(i) == target) then
                index = i
                return
            end if
        end do
    end function jump_search

    ! ===================================================================
    ! EXPONENTIAL SEARCH
    ! ===================================================================

    subroutine demo_exponential_search(arr, n)
        integer, intent(in) :: arr(:), n
        integer :: target, result

        print '(A)', 'Test 4: Exponential Search'
        print '(A)', repeat('-', 75)

        target = 500
        print '(A, I0)', 'Searching for: ', target

        result = exponential_search(arr, n, target)
        call print_result(result, target, "Exponential")

        print *
        print '(A)', 'Complexity: O(log n)'
        print '(A)', 'Best for: Unbounded/infinite arrays, unknown size'
        print '(A)', 'Strategy: Find range, then binary search'
        print *
    end subroutine demo_exponential_search

    function exponential_search(arr, n, target) result(index)
        integer, intent(in) :: arr(:), n, target
        integer :: index, bound

        ! If element is at first position
        if (arr(1) == target) then
            index = 1
            return
        end if

        ! Find range for binary search
        bound = 1
        do while (bound < n .and. arr(bound) < target)
            bound = bound * 2
        end do

        ! Binary search in found range
        index = binary_search_recursive(arr, bound / 2 + 1, min(bound, n), target)
    end function exponential_search

    ! ===================================================================
    ! TERNARY SEARCH (for unimodal functions)
    ! ===================================================================

    subroutine demo_ternary_search()
        real(8) :: left, right, max_val, max_pos

        print '(A)', 'Test 5: Ternary Search (for unimodal functions)'
        print '(A)', repeat('-', 75)

        left = -10.0
        right = 10.0

        max_pos = ternary_search(left, right)
        max_val = test_function(max_pos)

        print '(A, F10.6)', 'Maximum found at x = ', max_pos
        print '(A, F10.6)', 'Maximum value = ', max_val
        print *
        print '(A)', 'Complexity: O(log₃ n)'
        print '(A)', 'Best for: Finding maximum/minimum of unimodal function'
        print '(A)', 'Divides range into 3 parts instead of 2'
        print *
    end subroutine demo_ternary_search

    function ternary_search(left, right) result(max_pos)
        real(8), intent(in) :: left, right
        real(8) :: max_pos
        real(8) :: l, r, mid1, mid2
        real(8), parameter :: epsilon = 1.0e-6

        l = left
        r = right

        do while (r - l > epsilon)
            mid1 = l + (r - l) / 3.0
            mid2 = r - (r - l) / 3.0

            if (test_function(mid1) < test_function(mid2)) then
                l = mid1
            else
                r = mid2
            end if
        end do

        max_pos = (l + r) / 2.0
    end function ternary_search

    ! Test function: parabola with maximum at x=0
    function test_function(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = -x * x + 10.0
    end function test_function

    ! ===================================================================
    ! FIBONACCI SEARCH
    ! ===================================================================

    subroutine demo_fibonacci_search(arr, n)
        integer, intent(in) :: arr(:), n
        integer :: target, result

        print '(A)', 'Test 6: Fibonacci Search'
        print '(A)', repeat('-', 75)

        target = 500
        print '(A, I0)', 'Searching for: ', target

        result = fibonacci_search(arr, n, target)
        call print_result(result, target, "Fibonacci")

        print *
        print '(A)', 'Complexity: O(log n)'
        print '(A)', 'Best for: Systems where division is expensive'
        print '(A)', 'Uses Fibonacci numbers to divide array'
        print *
    end subroutine demo_fibonacci_search

    function fibonacci_search(arr, n, target) result(index)
        integer, intent(in) :: arr(:), n, target
        integer :: index
        integer :: fib_m2, fib_m1, fib_m, offset, i

        ! Initialize Fibonacci numbers
        fib_m2 = 0
        fib_m1 = 1
        fib_m = fib_m2 + fib_m1

        ! Find smallest Fibonacci >= n
        do while (fib_m < n)
            fib_m2 = fib_m1
            fib_m1 = fib_m
            fib_m = fib_m2 + fib_m1
        end do

        offset = 0
        index = -1

        do while (fib_m > 1)
            i = min(offset + fib_m2, n)

            if (arr(i) < target) then
                fib_m = fib_m1
                fib_m1 = fib_m2
                fib_m2 = fib_m - fib_m1
                offset = i
            else if (arr(i) > target) then
                fib_m = fib_m2
                fib_m1 = fib_m1 - fib_m2
                fib_m2 = fib_m - fib_m1
            else
                index = i
                return
            end if
        end do

        if (fib_m1 == 1 .and. offset + 1 <= n .and. arr(offset + 1) == target) then
            index = offset + 1
        end if
    end function fibonacci_search

    ! ===================================================================
    ! PERFORMANCE COMPARISON
    ! ===================================================================

    subroutine performance_comparison(arr, n)
        integer, intent(in) :: arr(:), n
        integer :: target, i, result
        real(8) :: start, finish
        real(8) :: time_binary, time_interpolation, time_jump, time_exponential
        integer, parameter :: num_searches = 10000

        print '(A)', 'Performance Comparison'
        print '(A)', repeat('=', 75)
        print '(A, I0, A)', 'Performing ', num_searches, ' searches...'
        print *

        target = n  ! Search for last element (worst case for many algorithms)

        ! Binary Search
        call cpu_time(start)
        do i = 1, num_searches
            result = binary_search_iterative(arr, n, target)
        end do
        call cpu_time(finish)
        time_binary = finish - start

        ! Interpolation Search
        call cpu_time(start)
        do i = 1, num_searches
            result = interpolation_search(arr, n, target)
        end do
        call cpu_time(finish)
        time_interpolation = finish - start

        ! Jump Search
        call cpu_time(start)
        do i = 1, num_searches
            result = jump_search(arr, n, target)
        end do
        call cpu_time(finish)
        time_jump = finish - start

        ! Exponential Search
        call cpu_time(start)
        do i = 1, num_searches
            result = exponential_search(arr, n, target)
        end do
        call cpu_time(finish)
        time_exponential = finish - start

        ! Print results
        print '(A)', 'Algorithm              Time (s)    Relative Speed'
        print '(A)', repeat('-', 55)
        print '(A, F10.6, A)', 'Binary Search          ', time_binary, '    1.00x (baseline)'
        print '(A, F10.6, A, F6.2, A)', 'Interpolation Search   ', time_interpolation, &
              '    ', time_binary / time_interpolation, 'x'
        print '(A, F10.6, A, F6.2, A)', 'Jump Search            ', time_jump, &
              '    ', time_binary / time_jump, 'x'
        print '(A, F10.6, A, F6.2, A)', 'Exponential Search     ', time_exponential, &
              '    ', time_binary / time_exponential, 'x'
        print *
    end subroutine performance_comparison

    ! ===================================================================
    ! UTILITY FUNCTIONS
    ! ===================================================================

    subroutine print_result(index, target, algorithm)
        integer, intent(in) :: index, target
        character(len=*), intent(in) :: algorithm

        if (index /= -1) then
            print '(A, A, I0, A, I0)', trim(algorithm), ' search: Found ', &
                  target, ' at index ', index
        else
            print '(A, A, I0, A)', trim(algorithm), ' search: ', target, ' not found'
        end if
    end subroutine print_result

end program advanced_search
