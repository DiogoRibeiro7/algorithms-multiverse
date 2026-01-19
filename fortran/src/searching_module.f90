! Searching Algorithms Module
! Comprehensive collection of search algorithms with generic interfaces

module searching_module
    use iso_fortran_env, only: int32, int64, real32, real64
    implicit none
    private

    ! Public interfaces for searching algorithms
    public :: binary_search, linear_search, jump_search
    public :: interpolation_search, exponential_search
    public :: ternary_search, fibonacci_search
    public :: find_kth_smallest, find_kth_largest
    public :: two_pointer_search, sliding_window_search

    ! Generic interfaces for different types
    interface binary_search
        module procedure binary_search_int32
        module procedure binary_search_int64
        module procedure binary_search_real32
        module procedure binary_search_real64
    end interface binary_search

    interface linear_search
        module procedure linear_search_int32
        module procedure linear_search_int64
        module procedure linear_search_real32
        module procedure linear_search_real64
    end interface linear_search

    interface jump_search
        module procedure jump_search_int32
        module procedure jump_search_int64
    end interface jump_search

    interface interpolation_search
        module procedure interpolation_search_int32
        module procedure interpolation_search_int64
    end interface interpolation_search

    interface exponential_search
        module procedure exponential_search_int32
        module procedure exponential_search_int64
    end interface exponential_search

    interface ternary_search
        module procedure ternary_search_real64
        module procedure ternary_search_int32
    end interface ternary_search

    interface fibonacci_search
        module procedure fibonacci_search_int32
        module procedure fibonacci_search_int64
    end interface fibonacci_search

contains

    !===============================================
    ! Binary Search Implementations
    !===============================================

    function binary_search_int32(arr, target) result(index)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: left, right, mid

        left = 1
        right = size(arr)
        index = -1

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

    end function binary_search_int32

    function binary_search_int64(arr, target) result(index)
        implicit none
        integer(int64), dimension(:), intent(in) :: arr
        integer(int64), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: left, right, mid

        left = 1
        right = size(arr)
        index = -1

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

    end function binary_search_int64

    function binary_search_real32(arr, target) result(index)
        implicit none
        real(real32), dimension(:), intent(in) :: arr
        real(real32), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: left, right, mid
        real(real32), parameter :: eps = 1.0e-6_real32

        left = 1
        right = size(arr)
        index = -1

        do while (left <= right)
            mid = left + (right - left) / 2

            if (abs(arr(mid) - target) < eps) then
                index = mid
                return
            else if (arr(mid) < target) then
                left = mid + 1
            else
                right = mid - 1
            end if
        end do

    end function binary_search_real32

    function binary_search_real64(arr, target) result(index)
        implicit none
        real(real64), dimension(:), intent(in) :: arr
        real(real64), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: left, right, mid
        real(real64), parameter :: eps = 1.0e-12_real64

        left = 1
        right = size(arr)
        index = -1

        do while (left <= right)
            mid = left + (right - left) / 2

            if (abs(arr(mid) - target) < eps) then
                index = mid
                return
            else if (arr(mid) < target) then
                left = mid + 1
            else
                right = mid - 1
            end if
        end do

    end function binary_search_real64

    !===============================================
    ! Linear Search Implementations
    !===============================================

    function linear_search_int32(arr, target) result(index)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: i

        index = -1
        do i = 1, size(arr)
            if (arr(i) == target) then
                index = i
                return
            end if
        end do

    end function linear_search_int32

    function linear_search_int64(arr, target) result(index)
        implicit none
        integer(int64), dimension(:), intent(in) :: arr
        integer(int64), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: i

        index = -1
        do i = 1, size(arr)
            if (arr(i) == target) then
                index = i
                return
            end if
        end do

    end function linear_search_int64

    function linear_search_real32(arr, target) result(index)
        implicit none
        real(real32), dimension(:), intent(in) :: arr
        real(real32), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: i
        real(real32), parameter :: eps = 1.0e-6_real32

        index = -1
        do i = 1, size(arr)
            if (abs(arr(i) - target) < eps) then
                index = i
                return
            end if
        end do

    end function linear_search_real32

    function linear_search_real64(arr, target) result(index)
        implicit none
        real(real64), dimension(:), intent(in) :: arr
        real(real64), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: i
        real(real64), parameter :: eps = 1.0e-12_real64

        index = -1
        do i = 1, size(arr)
            if (abs(arr(i) - target) < eps) then
                index = i
                return
            end if
        end do

    end function linear_search_real64

    !===============================================
    ! Jump Search Implementations
    !===============================================

    function jump_search_int32(arr, target) result(index)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: n, step, prev, i

        n = size(arr)
        step = int(sqrt(real(n)))
        prev = 0
        index = -1

        ! Jump to find the block where element is present
        do while (prev < n)
            if (arr(min(step, n)) >= target) then
                exit
            end if
            prev = step
            step = step + int(sqrt(real(n)))
            if (prev >= n) return
        end do

        ! Linear search in the identified block
        do i = prev + 1, min(step, n)
            if (arr(i) == target) then
                index = i
                return
            end if
        end do

    end function jump_search_int32

    function jump_search_int64(arr, target) result(index)
        implicit none
        integer(int64), dimension(:), intent(in) :: arr
        integer(int64), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: n, step, prev, i

        n = size(arr)
        step = int(sqrt(real(n)))
        prev = 0
        index = -1

        ! Jump to find the block where element is present
        do while (prev < n)
            if (arr(min(step, n)) >= target) then
                exit
            end if
            prev = step
            step = step + int(sqrt(real(n)))
            if (prev >= n) return
        end do

        ! Linear search in the identified block
        do i = prev + 1, min(step, n)
            if (arr(i) == target) then
                index = i
                return
            end if
        end do

    end function jump_search_int64

    !===============================================
    ! Interpolation Search Implementations
    !===============================================

    function interpolation_search_int32(arr, target) result(index)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: left, right, mid

        left = 1
        right = size(arr)
        index = -1

        do while (left <= right .and. target >= arr(left) .and. target <= arr(right))
            if (left == right) then
                if (arr(left) == target) then
                    index = left
                end if
                return
            end if

            ! Calculate position using interpolation formula
            mid = left + int((real(right - left) / real(arr(right) - arr(left))) * &
                           real(target - arr(left)))

            if (arr(mid) == target) then
                index = mid
                return
            else if (arr(mid) < target) then
                left = mid + 1
            else
                right = mid - 1
            end if
        end do

    end function interpolation_search_int32

    function interpolation_search_int64(arr, target) result(index)
        implicit none
        integer(int64), dimension(:), intent(in) :: arr
        integer(int64), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: left, right, mid

        left = 1
        right = size(arr)
        index = -1

        do while (left <= right .and. target >= arr(left) .and. target <= arr(right))
            if (left == right) then
                if (arr(left) == target) then
                    index = left
                end if
                return
            end if

            ! Calculate position using interpolation formula
            mid = left + int((real(right - left, real64) / real(arr(right) - arr(left), real64)) * &
                           real(target - arr(left), real64))

            if (arr(mid) == target) then
                index = mid
                return
            else if (arr(mid) < target) then
                left = mid + 1
            else
                right = mid - 1
            end if
        end do

    end function interpolation_search_int64

    !===============================================
    ! Exponential Search Implementations
    !===============================================

    function exponential_search_int32(arr, target) result(index)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: n, bound

        n = size(arr)
        index = -1

        ! If target is at first position
        if (arr(1) == target) then
            index = 1
            return
        end if

        ! Find range for binary search
        bound = 1
        do while (bound < n .and. arr(bound) < target)
            bound = bound * 2
        end do

        ! Binary search in the found range
        index = binary_search_range_int32(arr, target, bound/2 + 1, min(bound, n))

    end function exponential_search_int32

    function exponential_search_int64(arr, target) result(index)
        implicit none
        integer(int64), dimension(:), intent(in) :: arr
        integer(int64), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: n, bound

        n = size(arr)
        index = -1

        ! If target is at first position
        if (arr(1) == target) then
            index = 1
            return
        end if

        ! Find range for binary search
        bound = 1
        do while (bound < n .and. arr(bound) < target)
            bound = bound * 2
        end do

        ! Binary search in the found range
        index = binary_search_range_int64(arr, target, bound/2 + 1, min(bound, n))

    end function exponential_search_int64

    ! Helper function for binary search in a range
    function binary_search_range_int32(arr, target, left, right) result(index)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: target
        integer(int32), intent(in) :: left, right
        integer(int32) :: index
        integer(int32) :: l, r, mid

        l = left
        r = right
        index = -1

        do while (l <= r)
            mid = l + (r - l) / 2

            if (arr(mid) == target) then
                index = mid
                return
            else if (arr(mid) < target) then
                l = mid + 1
            else
                r = mid - 1
            end if
        end do

    end function binary_search_range_int32

    function binary_search_range_int64(arr, target, left, right) result(index)
        implicit none
        integer(int64), dimension(:), intent(in) :: arr
        integer(int64), intent(in) :: target
        integer(int32), intent(in) :: left, right
        integer(int32) :: index
        integer(int32) :: l, r, mid

        l = left
        r = right
        index = -1

        do while (l <= r)
            mid = l + (r - l) / 2

            if (arr(mid) == target) then
                index = mid
                return
            else if (arr(mid) < target) then
                l = mid + 1
            else
                r = mid - 1
            end if
        end do

    end function binary_search_range_int64

    !===============================================
    ! Ternary Search Implementations
    !===============================================

    function ternary_search_real64(func, left, right, eps) result(x_max)
        implicit none
        interface
            function func(x) result(y)
                use iso_fortran_env, only: real64
                real(real64), intent(in) :: x
                real(real64) :: y
            end function func
        end interface
        real(real64), intent(in) :: left, right
        real(real64), intent(in), optional :: eps
        real(real64) :: x_max
        real(real64) :: l, r, m1, m2, tolerance

        if (present(eps)) then
            tolerance = eps
        else
            tolerance = 1.0e-12_real64
        end if

        l = left
        r = right

        do while (r - l > tolerance)
            m1 = l + (r - l) / 3.0_real64
            m2 = r - (r - l) / 3.0_real64

            if (func(m1) < func(m2)) then
                l = m1
            else
                r = m2
            end if
        end do

        x_max = (l + r) / 2.0_real64

    end function ternary_search_real64

    function ternary_search_int32(arr, target) result(index)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: left, right, mid1, mid2

        left = 1
        right = size(arr)
        index = -1

        do while (left <= right)
            mid1 = left + (right - left) / 3
            mid2 = right - (right - left) / 3

            if (arr(mid1) == target) then
                index = mid1
                return
            else if (arr(mid2) == target) then
                index = mid2
                return
            else if (target < arr(mid1)) then
                right = mid1 - 1
            else if (target > arr(mid2)) then
                left = mid2 + 1
            else
                left = mid1 + 1
                right = mid2 - 1
            end if
        end do

    end function ternary_search_int32

    !===============================================
    ! Fibonacci Search Implementation
    !===============================================

    function fibonacci_search_int32(arr, target) result(index)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: n, fib_m2, fib_m1, fib_m, offset

        n = size(arr)
        index = -1

        ! Initialize Fibonacci numbers
        fib_m2 = 0   ! (m-2)'th Fibonacci number
        fib_m1 = 1   ! (m-1)'th Fibonacci number
        fib_m = fib_m2 + fib_m1  ! m'th Fibonacci number

        ! Find the smallest Fibonacci number >= n
        do while (fib_m < n)
            fib_m2 = fib_m1
            fib_m1 = fib_m
            fib_m = fib_m2 + fib_m1
        end do

        offset = 0

        do while (fib_m > 1)
            ! Check if fib_m2 is a valid location
            if (offset + fib_m2 <= n) then
                if (arr(offset + fib_m2) < target) then
                    fib_m = fib_m1
                    fib_m1 = fib_m2
                    fib_m2 = fib_m - fib_m1
                    offset = offset + fib_m2
                else if (arr(offset + fib_m2) > target) then
                    fib_m = fib_m2
                    fib_m1 = fib_m1 - fib_m2
                    fib_m2 = fib_m - fib_m1
                else
                    index = offset + fib_m2
                    return
                end if
            else
                fib_m = fib_m2
                fib_m1 = fib_m1 - fib_m2
                fib_m2 = fib_m - fib_m1
            end if
        end do

        ! Check the last element
        if (fib_m1 == 1 .and. offset + 1 <= n .and. arr(offset + 1) == target) then
            index = offset + 1
        end if

    end function fibonacci_search_int32

    function fibonacci_search_int64(arr, target) result(index)
        implicit none
        integer(int64), dimension(:), intent(in) :: arr
        integer(int64), intent(in) :: target
        integer(int32) :: index
        integer(int32) :: n, fib_m2, fib_m1, fib_m, offset

        n = size(arr)
        index = -1

        ! Initialize Fibonacci numbers
        fib_m2 = 0   ! (m-2)'th Fibonacci number
        fib_m1 = 1   ! (m-1)'th Fibonacci number
        fib_m = fib_m2 + fib_m1  ! m'th Fibonacci number

        ! Find the smallest Fibonacci number >= n
        do while (fib_m < n)
            fib_m2 = fib_m1
            fib_m1 = fib_m
            fib_m = fib_m2 + fib_m1
        end do

        offset = 0

        do while (fib_m > 1)
            ! Check if fib_m2 is a valid location
            if (offset + fib_m2 <= n) then
                if (arr(offset + fib_m2) < target) then
                    fib_m = fib_m1
                    fib_m1 = fib_m2
                    fib_m2 = fib_m - fib_m1
                    offset = offset + fib_m2
                else if (arr(offset + fib_m2) > target) then
                    fib_m = fib_m2
                    fib_m1 = fib_m1 - fib_m2
                    fib_m2 = fib_m - fib_m1
                else
                    index = offset + fib_m2
                    return
                end if
            else
                fib_m = fib_m2
                fib_m1 = fib_m1 - fib_m2
                fib_m2 = fib_m - fib_m1
            end if
        end do

        ! Check the last element
        if (fib_m1 == 1 .and. offset + 1 <= n .and. arr(offset + 1) == target) then
            index = offset + 1
        end if

    end function fibonacci_search_int64

    !===============================================
    ! K-th Element Search
    !===============================================

    function find_kth_smallest(arr, k) result(value)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: k
        integer(int32) :: value
        integer(int32), dimension(:), allocatable :: temp_arr
        integer(int32) :: n

        n = size(arr)
        allocate(temp_arr(n))
        temp_arr = arr

        ! Use quickselect algorithm
        value = quickselect(temp_arr, 1, n, k)

        deallocate(temp_arr)

    end function find_kth_smallest

    function find_kth_largest(arr, k) result(value)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: k
        integer(int32) :: value
        integer(int32) :: n

        n = size(arr)
        value = find_kth_smallest(arr, n - k + 1)

    end function find_kth_largest

    ! Quickselect algorithm for finding k-th smallest element
    recursive function quickselect(arr, left, right, k) result(value)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: left, right, k
        integer(int32) :: value
        integer(int32) :: pivot_index

        if (left == right) then
            value = arr(left)
            return
        end if

        pivot_index = partition_for_select(arr, left, right)

        if (k == pivot_index) then
            value = arr(k)
        else if (k < pivot_index) then
            value = quickselect(arr, left, pivot_index - 1, k)
        else
            value = quickselect(arr, pivot_index + 1, right, k)
        end if

    end function quickselect

    function partition_for_select(arr, left, right) result(pivot_index)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: left, right
        integer(int32) :: pivot_index
        integer(int32) :: pivot, i, j, temp

        pivot = arr(right)
        i = left - 1

        do j = left, right - 1
            if (arr(j) <= pivot) then
                i = i + 1
                temp = arr(i)
                arr(i) = arr(j)
                arr(j) = temp
            end if
        end do

        temp = arr(i + 1)
        arr(i + 1) = arr(right)
        arr(right) = temp

        pivot_index = i + 1

    end function partition_for_select

    !===============================================
    ! Two-Pointer Search
    !===============================================

    function two_pointer_search(arr, target_sum) result(indices)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: target_sum
        integer(int32), dimension(2) :: indices
        integer(int32) :: left, right, current_sum

        indices = [-1, -1]
        left = 1
        right = size(arr)

        do while (left < right)
            current_sum = arr(left) + arr(right)

            if (current_sum == target_sum) then
                indices = [left, right]
                return
            else if (current_sum < target_sum) then
                left = left + 1
            else
                right = right - 1
            end if
        end do

    end function two_pointer_search

    !===============================================
    ! Sliding Window Search
    !===============================================

    function sliding_window_search(arr, target_sum) result(indices)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: target_sum
        integer(int32), dimension(2) :: indices
        integer(int32) :: n, window_start, window_end, current_sum

        n = size(arr)
        indices = [-1, -1]
        window_start = 1
        current_sum = 0

        do window_end = 1, n
            current_sum = current_sum + arr(window_end)

            do while (current_sum > target_sum .and. window_start <= window_end)
                current_sum = current_sum - arr(window_start)
                window_start = window_start + 1
            end do

            if (current_sum == target_sum) then
                indices = [window_start, window_end]
                return
            end if
        end do

    end function sliding_window_search

end module searching_module