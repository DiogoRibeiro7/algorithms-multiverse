! Binary Search Algorithm Collection in Fortran
!
! Comprehensive implementation of binary search variants including:
! 1. Classic binary search (iterative & recursive)
! 2. First/last occurrence finding
! 3. Rotated array search
! 4. Exponential search
! 5. Interpolation search
! 6. Ternary search
! 7. Binary search on answer (optimization)
! 8. Advanced utilities
!
! Time Complexity: O(log n) for most variants
! Space Complexity: O(1) iterative, O(log n) recursive
!
! Fortran Features:
! - Array operations and intrinsic functions
! - Module-based organization
! - Explicit typing and interfaces
! - High performance numerical computing

module binary_search_module
    implicit none
    private
    public :: binary_search_iterative, binary_search_recursive
    public :: find_first_occurrence, find_last_occurrence, count_occurrences
    public :: search_rotated_array, find_rotation_point
    public :: exponential_search, interpolation_search, ternary_search
    public :: integer_square_root, find_closest, find_peak_element

contains

    ! ========================================================================
    ! 1. CLASSIC BINARY SEARCH
    ! ========================================================================

    ! Classic binary search - iterative implementation
    ! Returns index (1-based) or 0 if not found
    integer function binary_search_iterative(arr, n, target) result(idx)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: arr
        integer, intent(in) :: target
        integer :: left, right, mid

        idx = 0
        if (n <= 0) return

        left = 1
        right = n

        do while (left <= right)
            mid = left + (right - left) / 2

            if (arr(mid) == target) then
                idx = mid
                return
            else if (arr(mid) < target) then
                left = mid + 1
            else
                right = mid - 1
            end if
        end do
    end function binary_search_iterative

    ! Classic binary search - recursive implementation
    recursive function binary_search_recursive(arr, n, target) result(idx)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: arr
        integer, intent(in) :: target
        integer :: idx

        if (n <= 0) then
            idx = 0
        else
            idx = binary_search_helper(arr, target, 1, n)
        end if
    end function binary_search_recursive

    recursive function binary_search_helper(arr, target, left, right) result(idx)
        integer, dimension(:), intent(in) :: arr
        integer, intent(in) :: target, left, right
        integer :: idx, mid

        if (left > right) then
            idx = 0
            return
        end if

        mid = left + (right - left) / 2

        if (arr(mid) == target) then
            idx = mid
        else if (arr(mid) < target) then
            idx = binary_search_helper(arr, target, mid + 1, right)
        else
            idx = binary_search_helper(arr, target, left, mid - 1)
        end if
    end function binary_search_helper

    ! ========================================================================
    ! 2. FIRST/LAST OCCURRENCE
    ! ========================================================================

    ! Find first (leftmost) occurrence
    integer function find_first_occurrence(arr, n, target) result(idx)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: arr
        integer, intent(in) :: target
        integer :: left, right, mid

        idx = 0
        if (n <= 0) return

        left = 1
        right = n

        do while (left <= right)
            mid = left + (right - left) / 2

            if (arr(mid) == target) then
                idx = mid
                right = mid - 1  ! Continue searching left
            else if (arr(mid) < target) then
                left = mid + 1
            else
                right = mid - 1
            end if
        end do
    end function find_first_occurrence

    ! Find last (rightmost) occurrence
    integer function find_last_occurrence(arr, n, target) result(idx)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: arr
        integer, intent(in) :: target
        integer :: left, right, mid

        idx = 0
        if (n <= 0) return

        left = 1
        right = n

        do while (left <= right)
            mid = left + (right - left) / 2

            if (arr(mid) == target) then
                idx = mid
                left = mid + 1  ! Continue searching right
            else if (arr(mid) < target) then
                left = mid + 1
            else
                right = mid - 1
            end if
        end do
    end function find_last_occurrence

    ! Count occurrences
    integer function count_occurrences(arr, n, target) result(count)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: arr
        integer, intent(in) :: target
        integer :: first, last

        first = find_first_occurrence(arr, n, target)
        if (first == 0) then
            count = 0
            return
        end if

        last = find_last_occurrence(arr, n, target)
        count = last - first + 1
    end function count_occurrences

    ! ========================================================================
    ! 3. ROTATED SORTED ARRAY SEARCH
    ! ========================================================================

    ! Search in rotated sorted array
    integer function search_rotated_array(arr, n, target) result(idx)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: arr
        integer, intent(in) :: target
        integer :: left, right, mid

        idx = 0
        if (n <= 0) return

        left = 1
        right = n

        do while (left <= right)
            mid = left + (right - left) / 2

            if (arr(mid) == target) then
                idx = mid
                return
            end if

            ! Determine which half is sorted
            if (arr(left) <= arr(mid)) then
                ! Left half is sorted
                if (arr(left) <= target .and. target < arr(mid)) then
                    right = mid - 1
                else
                    left = mid + 1
                end if
            else
                ! Right half is sorted
                if (arr(mid) < target .and. target <= arr(right)) then
                    left = mid + 1
                else
                    right = mid - 1
                end if
            end if
        end do
    end function search_rotated_array

    ! Find rotation point (minimum element)
    integer function find_rotation_point(arr, n) result(idx)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: arr
        integer :: left, right, mid

        if (n <= 0) then
            idx = 0
            return
        end if

        left = 1
        right = n

        do while (left < right)
            mid = left + (right - left) / 2

            if (arr(mid) > arr(right)) then
                left = mid + 1
            else
                right = mid
            end if
        end do

        idx = left
    end function find_rotation_point

    ! ========================================================================
    ! 4. EXPONENTIAL SEARCH
    ! ========================================================================

    ! Exponential search
    integer function exponential_search(arr, n, target) result(idx)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: arr
        integer, intent(in) :: target
        integer :: i, left, right

        idx = 0
        if (n <= 0) return

        if (arr(1) == target) then
            idx = 1
            return
        end if

        ! Find range for binary search
        i = 1
        do while (i <= n .and. arr(i) <= target)
            i = i * 2
        end do

        ! Binary search in found range
        left = i / 2
        right = min(i, n)
        idx = binary_search_helper(arr, target, left, right)
    end function exponential_search

    ! ========================================================================
    ! 5. INTERPOLATION SEARCH
    ! ========================================================================

    ! Interpolation search
    integer function interpolation_search(arr, n, target) result(idx)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: arr
        integer, intent(in) :: target
        integer :: left, right, pos

        idx = 0
        if (n <= 0) return

        left = 1
        right = n

        do while (left <= right .and. target >= arr(left) .and. target <= arr(right))
            if (left == right) then
                if (arr(left) == target) idx = left
                return
            end if

            ! Interpolation formula
            pos = left + ((target - arr(left)) * (right - left)) / (arr(right) - arr(left))

            ! Ensure pos is within bounds
            pos = max(left, min(pos, right))

            if (arr(pos) == target) then
                idx = pos
                return
            else if (arr(pos) < target) then
                left = pos + 1
            else
                right = pos - 1
            end if
        end do
    end function interpolation_search

    ! ========================================================================
    ! 6. TERNARY SEARCH
    ! ========================================================================

    ! Ternary search
    integer function ternary_search(arr, n, target) result(idx)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: arr
        integer, intent(in) :: target
        integer :: left, right, mid1, mid2

        idx = 0
        if (n <= 0) return

        left = 1
        right = n

        do while (left <= right)
            mid1 = left + (right - left) / 3
            mid2 = right - (right - left) / 3

            if (arr(mid1) == target) then
                idx = mid1
                return
            end if
            if (arr(mid2) == target) then
                idx = mid2
                return
            end if

            if (target < arr(mid1)) then
                right = mid1 - 1
            else if (target > arr(mid2)) then
                left = mid2 + 1
            else
                left = mid1 + 1
                right = mid2 - 1
            end if
        end do
    end function ternary_search

    ! ========================================================================
    ! 7. BINARY SEARCH ON ANSWER
    ! ========================================================================

    ! Find integer square root
    integer function integer_square_root(n) result(sqrt_val)
        integer, intent(in) :: n
        integer :: left, right, mid
        integer(kind=8) :: square

        if (n < 0) then
            sqrt_val = -1
            return
        end if

        if (n == 0 .or. n == 1) then
            sqrt_val = n
            return
        end if

        left = 0
        right = n
        sqrt_val = 0

        do while (left <= right)
            mid = left + (right - left) / 2
            square = int(mid, kind=8) * int(mid, kind=8)

            if (square == n) then
                sqrt_val = mid
                return
            else if (square < n) then
                sqrt_val = mid
                left = mid + 1
            else
                right = mid - 1
            end if
        end do
    end function integer_square_root

    ! ========================================================================
    ! 8. ADVANCED UTILITIES
    ! ========================================================================

    ! Find closest element
    integer function find_closest(arr, n, target) result(idx)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: arr
        integer, intent(in) :: target
        integer :: left, right, mid

        if (n <= 0) then
            idx = 0
            return
        end if

        if (n == 1) then
            idx = 1
            return
        end if

        if (target <= arr(1)) then
            idx = 1
            return
        end if
        if (target >= arr(n)) then
            idx = n
            return
        end if

        left = 1
        right = n

        do while (left < right)
            mid = left + (right - left) / 2

            if (arr(mid) == target) then
                idx = mid
                return
            else if (arr(mid) < target) then
                left = mid + 1
            else
                right = mid
            end if
        end do

        if (left > 1) then
            if (abs(arr(left - 1) - target) < abs(arr(left) - target)) then
                idx = left - 1
                return
            end if
        end if

        idx = left
    end function find_closest

    ! Find peak element
    integer function find_peak_element(arr, n) result(idx)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: arr
        integer :: left, right, mid

        if (n <= 0) then
            idx = 0
            return
        end if

        if (n == 1) then
            idx = 1
            return
        end if

        left = 1
        right = n

        do while (left < right)
            mid = left + (right - left) / 2

            if (arr(mid) < arr(mid + 1)) then
                left = mid + 1
            else
                right = mid
            end if
        end do

        idx = left
    end function find_peak_element

end module binary_search_module

! ============================================================================
! DEMONSTRATION PROGRAM
! ============================================================================

program binary_search_demo
    use binary_search_module
    implicit none

    print *, '======================================================================'
    print *, 'BINARY SEARCH ALGORITHM COLLECTION - FORTRAN'
    print *, '======================================================================'

    call demonstrate_classic_binary_search()
    call demonstrate_first_last_occurrence()
    call demonstrate_rotated_array_search()
    call demonstrate_exponential_search()
    call demonstrate_interpolation_search()
    call demonstrate_ternary_search()
    call demonstrate_binary_search_on_answer()
    call demonstrate_advanced_utilities()

    print *, ''
    print *, '======================================================================'
    print *, 'DEMONSTRATION COMPLETE'
    print *, '======================================================================'

contains

    subroutine demonstrate_classic_binary_search()
        integer, dimension(10) :: arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        integer, dimension(4) :: targets = [7, 10, 1, 19]
        integer :: i, idx_iter, idx_rec

        print *, ''
        print *, '1. CLASSIC BINARY SEARCH'
        print *, '--------------------------------------------------'

        do i = 1, 4
            idx_iter = binary_search_iterative(arr, 10, targets(i))
            idx_rec = binary_search_recursive(arr, 10, targets(i))
            print '(A,I3,A,I3,A,I3)', 'Search', targets(i), &
                ': Iterative=', idx_iter, ', Recursive=', idx_rec
        end do
    end subroutine demonstrate_classic_binary_search

    subroutine demonstrate_first_last_occurrence()
        integer, dimension(10) :: arr = [1, 2, 2, 2, 3, 4, 4, 4, 4, 5]
        integer, dimension(3) :: targets = [2, 4, 6]
        integer :: i, first, last, count

        print *, ''
        print *, '2. FIRST/LAST OCCURRENCE'
        print *, '--------------------------------------------------'

        do i = 1, 3
            first = find_first_occurrence(arr, 10, targets(i))
            last = find_last_occurrence(arr, 10, targets(i))
            count = count_occurrences(arr, 10, targets(i))
            print '(A,I2,A,I3,A,I3,A,I2)', 'Target', targets(i), &
                ': First=', first, ', Last=', last, ', Count=', count
        end do
    end subroutine demonstrate_first_last_occurrence

    subroutine demonstrate_rotated_array_search()
        integer, dimension(7) :: rotated = [4, 5, 6, 7, 0, 1, 2]
        integer, dimension(3) :: targets = [0, 3, 6]
        integer :: i, rotation_point, idx

        print *, ''
        print *, '3. ROTATED ARRAY SEARCH'
        print *, '--------------------------------------------------'

        rotation_point = find_rotation_point(rotated, 7)
        print '(A,I2,A,I2)', 'Rotation point:', rotation_point, &
            ' (value:', rotated(rotation_point), ')'

        do i = 1, 3
            idx = search_rotated_array(rotated, 7, targets(i))
            print '(A,I2,A,I3)', 'Search', targets(i), ': Index=', idx
        end do
    end subroutine demonstrate_rotated_array_search

    subroutine demonstrate_exponential_search()
        integer, dimension(50) :: large_arr
        integer, dimension(3) :: targets = [15, 51, 99]
        integer :: i, idx

        print *, ''
        print *, '4. EXPONENTIAL SEARCH'
        print *, '--------------------------------------------------'

        do i = 1, 50
            large_arr(i) = i * 2 - 1
        end do

        do i = 1, 3
            idx = exponential_search(large_arr, 50, targets(i))
            print '(A,I3,A,I3)', 'Search', targets(i), ' in array of size 50: Index=', idx
        end do
    end subroutine demonstrate_exponential_search

    subroutine demonstrate_interpolation_search()
        integer, dimension(10) :: uniform_arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        integer, dimension(3) :: targets = [30, 75, 100]
        integer :: i, idx

        print *, ''
        print *, '5. INTERPOLATION SEARCH'
        print *, '--------------------------------------------------'

        do i = 1, 3
            idx = interpolation_search(uniform_arr, 10, targets(i))
            print '(A,I4,A,I3)', 'Search', targets(i), ': Index=', idx
        end do
    end subroutine demonstrate_interpolation_search

    subroutine demonstrate_ternary_search()
        integer, dimension(10) :: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        integer, dimension(4) :: targets = [5, 1, 10, 11]
        integer :: i, idx

        print *, ''
        print *, '6. TERNARY SEARCH'
        print *, '--------------------------------------------------'

        do i = 1, 4
            idx = ternary_search(arr, 10, targets(i))
            print '(A,I3,A,I3)', 'Search', targets(i), ': Index=', idx
        end do
    end subroutine demonstrate_ternary_search

    subroutine demonstrate_binary_search_on_answer()
        integer, dimension(4) :: test_numbers = [16, 25, 50, 100]
        integer :: i, sqrt_val

        print *, ''
        print *, '7. BINARY SEARCH ON ANSWER'
        print *, '--------------------------------------------------'

        do i = 1, 4
            sqrt_val = integer_square_root(test_numbers(i))
            print '(A,I4,A,I3)', 'sqrt(', test_numbers(i), ') =', sqrt_val
        end do
    end subroutine demonstrate_binary_search_on_answer

    subroutine demonstrate_advanced_utilities()
        integer, dimension(5) :: arr_closest = [1, 3, 5, 7, 9]
        integer, dimension(3) :: targets_closest = [4, 6, 8]
        integer, dimension(6) :: peak_arr = [1, 3, 20, 4, 1, 0]
        integer :: i, idx, peak

        print *, ''
        print *, '8. ADVANCED UTILITIES'
        print *, '--------------------------------------------------'

        do i = 1, 3
            idx = find_closest(arr_closest, 5, targets_closest(i))
            print '(A,I2,A,I2,A,I2)', 'Closest to', targets_closest(i), &
                ': Index=', idx, ', Value=', arr_closest(idx)
        end do

        peak = find_peak_element(peak_arr, 6)
        print '(A,I2,A,I3)', 'Peak element: Index=', peak, ', Value=', peak_arr(peak)
    end subroutine demonstrate_advanced_utilities

end program binary_search_demo
