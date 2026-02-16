! Sorting Algorithms Module
! High-performance sorting implementations in modern Fortran

module sorting_module
    use iso_fortran_env, only: int32, int64, real32, real64
    implicit none
    private

    ! Public interfaces
    public :: quick_sort, merge_sort, heap_sort, insertion_sort, bubble_sort
    public :: shell_sort, radix_sort, counting_sort, bucket_sort, tim_sort
    public :: intro_sort, parallel_quick_sort
    public :: is_sorted, shuffle_array

    ! Generic interfaces for different types
    interface quick_sort
        module procedure quick_sort_int32, quick_sort_real64
    end interface quick_sort

    interface merge_sort
        module procedure merge_sort_int32, merge_sort_real64
    end interface merge_sort

    interface heap_sort
        module procedure heap_sort_int32, heap_sort_real64
    end interface heap_sort

contains

    !===========================================================================
    ! Quick Sort - O(n log n) average, O(n²) worst case
    !===========================================================================

    recursive subroutine quick_sort_int32(arr, low, high)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in), optional :: low, high
        integer(int32) :: lo, hi, pivot_index

        lo = 1
        hi = size(arr)
        if (present(low)) lo = low
        if (present(high)) hi = high

        if (lo < hi) then
            pivot_index = partition_int32(arr, lo, hi)
            call quick_sort_int32(arr, lo, pivot_index - 1)
            call quick_sort_int32(arr, pivot_index + 1, hi)
        end if

    end subroutine quick_sort_int32

    function partition_int32(arr, low, high) result(pivot_index)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: low, high
        integer(int32) :: pivot_index, i, j, pivot, temp

        ! Choose pivot as median of three
        call median_of_three_int32(arr, low, high)

        pivot = arr(high)
        i = low - 1

        do j = low, high - 1
            if (arr(j) <= pivot) then
                i = i + 1
                temp = arr(i)
                arr(i) = arr(j)
                arr(j) = temp
            end if
        end do

        temp = arr(i + 1)
        arr(i + 1) = arr(high)
        arr(high) = temp

        pivot_index = i + 1

    end function partition_int32

    subroutine median_of_three_int32(arr, low, high)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: low, high
        integer(int32) :: mid, temp

        mid = (low + high) / 2

        ! Sort low, mid, high
        if (arr(mid) < arr(low)) then
            temp = arr(low)
            arr(low) = arr(mid)
            arr(mid) = temp
        end if

        if (arr(high) < arr(low)) then
            temp = arr(low)
            arr(low) = arr(high)
            arr(high) = temp
        end if

        if (arr(high) < arr(mid)) then
            temp = arr(mid)
            arr(mid) = arr(high)
            arr(high) = temp
        end if

        ! Place median at high-1
        temp = arr(mid)
        arr(mid) = arr(high)
        arr(high) = temp

    end subroutine median_of_three_int32

    recursive subroutine quick_sort_real64(arr, low, high)
        implicit none
        real(real64), dimension(:), intent(inout) :: arr
        integer(int32), intent(in), optional :: low, high
        integer(int32) :: lo, hi, pivot_index

        lo = 1
        hi = size(arr)
        if (present(low)) lo = low
        if (present(high)) hi = high

        if (lo < hi) then
            pivot_index = partition_real64(arr, lo, hi)
            call quick_sort_real64(arr, lo, pivot_index - 1)
            call quick_sort_real64(arr, pivot_index + 1, hi)
        end if

    end subroutine quick_sort_real64

    function partition_real64(arr, low, high) result(pivot_index)
        implicit none
        real(real64), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: low, high
        integer(int32) :: pivot_index, i, j
        real(real64) :: pivot, temp

        pivot = arr(high)
        i = low - 1

        do j = low, high - 1
            if (arr(j) <= pivot) then
                i = i + 1
                temp = arr(i)
                arr(i) = arr(j)
                arr(j) = temp
            end if
        end do

        temp = arr(i + 1)
        arr(i + 1) = arr(high)
        arr(high) = temp

        pivot_index = i + 1

    end function partition_real64

    !===========================================================================
    ! Merge Sort - O(n log n) guaranteed
    !===========================================================================

    recursive subroutine merge_sort_int32(arr, low, high)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in), optional :: low, high
        integer(int32) :: lo, hi, mid

        lo = 1
        hi = size(arr)
        if (present(low)) lo = low
        if (present(high)) hi = high

        if (lo < hi) then
            mid = lo + (hi - lo) / 2
            call merge_sort_int32(arr, lo, mid)
            call merge_sort_int32(arr, mid + 1, hi)
            call merge_int32(arr, lo, mid, hi)
        end if

    end subroutine merge_sort_int32

    subroutine merge_int32(arr, low, mid, high)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: low, mid, high
        integer(int32), dimension(:), allocatable :: left, right
        integer(int32) :: n1, n2, i, j, k

        n1 = mid - low + 1
        n2 = high - mid

        allocate(left(n1), right(n2))

        ! Copy data to temporary arrays
        do i = 1, n1
            left(i) = arr(low + i - 1)
        end do

        do j = 1, n2
            right(j) = arr(mid + j)
        end do

        ! Merge temporary arrays back
        i = 1
        j = 1
        k = low

        do while (i <= n1 .and. j <= n2)
            if (left(i) <= right(j)) then
                arr(k) = left(i)
                i = i + 1
            else
                arr(k) = right(j)
                j = j + 1
            end if
            k = k + 1
        end do

        ! Copy remaining elements
        do while (i <= n1)
            arr(k) = left(i)
            i = i + 1
            k = k + 1
        end do

        do while (j <= n2)
            arr(k) = right(j)
            j = j + 1
            k = k + 1
        end do

        deallocate(left, right)

    end subroutine merge_int32

    recursive subroutine merge_sort_real64(arr, low, high)
        implicit none
        real(real64), dimension(:), intent(inout) :: arr
        integer(int32), intent(in), optional :: low, high
        integer(int32) :: lo, hi, mid

        lo = 1
        hi = size(arr)
        if (present(low)) lo = low
        if (present(high)) hi = high

        if (lo < hi) then
            mid = lo + (hi - lo) / 2
            call merge_sort_real64(arr, lo, mid)
            call merge_sort_real64(arr, mid + 1, hi)
            call merge_real64(arr, lo, mid, hi)
        end if

    end subroutine merge_sort_real64

    subroutine merge_real64(arr, low, mid, high)
        implicit none
        real(real64), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: low, mid, high
        real(real64), dimension(:), allocatable :: left, right
        integer(int32) :: n1, n2, i, j, k

        n1 = mid - low + 1
        n2 = high - mid

        allocate(left(n1), right(n2))

        do i = 1, n1
            left(i) = arr(low + i - 1)
        end do

        do j = 1, n2
            right(j) = arr(mid + j)
        end do

        i = 1
        j = 1
        k = low

        do while (i <= n1 .and. j <= n2)
            if (left(i) <= right(j)) then
                arr(k) = left(i)
                i = i + 1
            else
                arr(k) = right(j)
                j = j + 1
            end if
            k = k + 1
        end do

        do while (i <= n1)
            arr(k) = left(i)
            i = i + 1
            k = k + 1
        end do

        do while (j <= n2)
            arr(k) = right(j)
            j = j + 1
            k = k + 1
        end do

        deallocate(left, right)

    end subroutine merge_real64

    !===========================================================================
    ! Heap Sort - O(n log n) guaranteed, in-place
    !===========================================================================

    subroutine heap_sort_int32(arr)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32) :: n, i, temp

        n = size(arr)

        ! Build max heap
        do i = n / 2, 1, -1
            call heapify_int32(arr, n, i)
        end do

        ! Extract elements from heap
        do i = n, 2, -1
            temp = arr(1)
            arr(1) = arr(i)
            arr(i) = temp
            call heapify_int32(arr, i - 1, 1)
        end do

    end subroutine heap_sort_int32

    recursive subroutine heapify_int32(arr, n, i)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: n, i
        integer(int32) :: largest, left, right, temp

        largest = i
        left = 2 * i
        right = 2 * i + 1

        if (left <= n .and. arr(left) > arr(largest)) then
            largest = left
        end if

        if (right <= n .and. arr(right) > arr(largest)) then
            largest = right
        end if

        if (largest /= i) then
            temp = arr(i)
            arr(i) = arr(largest)
            arr(largest) = temp
            call heapify_int32(arr, n, largest)
        end if

    end subroutine heapify_int32

    subroutine heap_sort_real64(arr)
        implicit none
        real(real64), dimension(:), intent(inout) :: arr
        integer(int32) :: n, i
        real(real64) :: temp

        n = size(arr)

        do i = n / 2, 1, -1
            call heapify_real64(arr, n, i)
        end do

        do i = n, 2, -1
            temp = arr(1)
            arr(1) = arr(i)
            arr(i) = temp
            call heapify_real64(arr, i - 1, 1)
        end do

    end subroutine heap_sort_real64

    recursive subroutine heapify_real64(arr, n, i)
        implicit none
        real(real64), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: n, i
        integer(int32) :: largest, left, right
        real(real64) :: temp

        largest = i
        left = 2 * i
        right = 2 * i + 1

        if (left <= n .and. arr(left) > arr(largest)) then
            largest = left
        end if

        if (right <= n .and. arr(right) > arr(largest)) then
            largest = right
        end if

        if (largest /= i) then
            temp = arr(i)
            arr(i) = arr(largest)
            arr(largest) = temp
            call heapify_real64(arr, n, largest)
        end if

    end subroutine heapify_real64

    !===========================================================================
    ! Insertion Sort - O(n²) but efficient for small arrays
    !===========================================================================

    subroutine insertion_sort(arr)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32) :: i, j, key, n

        n = size(arr)

        do i = 2, n
            key = arr(i)
            j = i - 1

            do while (j >= 1 .and. arr(j) > key)
                arr(j + 1) = arr(j)
                j = j - 1
            end do

            arr(j + 1) = key
        end do

    end subroutine insertion_sort

    !===========================================================================
    ! Bubble Sort - O(n²) - Educational purposes
    !===========================================================================

    subroutine bubble_sort(arr)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32) :: i, j, n, temp
        logical :: swapped

        n = size(arr)

        do i = 1, n - 1
            swapped = .false.

            do j = 1, n - i
                if (arr(j) > arr(j + 1)) then
                    temp = arr(j)
                    arr(j) = arr(j + 1)
                    arr(j + 1) = temp
                    swapped = .true.
                end if
            end do

            if (.not. swapped) exit
        end do

    end subroutine bubble_sort

    !===========================================================================
    ! Shell Sort - O(n log n) to O(n²) depending on gap sequence
    !===========================================================================

    subroutine shell_sort(arr)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32) :: n, gap, i, j, temp

        n = size(arr)
        gap = n / 2

        do while (gap > 0)
            do i = gap + 1, n
                temp = arr(i)
                j = i

                do while (j > gap .and. arr(j - gap) > temp)
                    arr(j) = arr(j - gap)
                    j = j - gap
                end do

                arr(j) = temp
            end do

            gap = gap / 2
        end do

    end subroutine shell_sort

    !===========================================================================
    ! Radix Sort - O(d(n+k)) for integers
    !===========================================================================

    subroutine radix_sort(arr)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32) :: n, max_val, exp

        n = size(arr)
        max_val = maxval(arr)
        exp = 1

        do while (max_val / exp > 0)
            call counting_sort_by_digit(arr, exp)
            exp = exp * 10
        end do

    end subroutine radix_sort

    subroutine counting_sort_by_digit(arr, exp)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: exp
        integer(int32), dimension(:), allocatable :: output, count
        integer(int32) :: n, i, digit

        n = size(arr)
        allocate(output(n), count(0:9))

        count = 0

        ! Count occurrences
        do i = 1, n
            digit = mod(arr(i) / exp, 10)
            count(digit) = count(digit) + 1
        end do

        ! Cumulative count
        do i = 1, 9
            count(i) = count(i) + count(i - 1)
        end do

        ! Build output array
        do i = n, 1, -1
            digit = mod(arr(i) / exp, 10)
            output(count(digit)) = arr(i)
            count(digit) = count(digit) - 1
        end do

        ! Copy output to arr
        arr = output

        deallocate(output, count)

    end subroutine counting_sort_by_digit

    !===========================================================================
    ! Counting Sort - O(n+k) for small range integers
    !===========================================================================

    subroutine counting_sort(arr, max_value)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in), optional :: max_value
        integer(int32), dimension(:), allocatable :: count, output
        integer(int32) :: n, k, i

        n = size(arr)
        k = maxval(arr)
        if (present(max_value)) k = max_value

        allocate(count(0:k), output(n))

        count = 0

        ! Count occurrences
        do i = 1, n
            count(arr(i)) = count(arr(i)) + 1
        end do

        ! Cumulative count
        do i = 1, k
            count(i) = count(i) + count(i - 1)
        end do

        ! Build output
        do i = n, 1, -1
            output(count(arr(i))) = arr(i)
            count(arr(i)) = count(arr(i)) - 1
        end do

        arr = output

        deallocate(count, output)

    end subroutine counting_sort

    !===========================================================================
    ! Bucket Sort - O(n) average for uniformly distributed data
    !===========================================================================

    subroutine bucket_sort(arr)
        implicit none
        real(real64), dimension(:), intent(inout) :: arr
        type bucket_type
            real(real64), dimension(:), allocatable :: values
            integer(int32) :: count = 0
        end type bucket_type

        type(bucket_type), dimension(:), allocatable :: buckets
        integer(int32) :: n, num_buckets, i, j, k, bucket_index
        real(real64) :: min_val, max_val, range

        n = size(arr)
        num_buckets = int(sqrt(real(n)))

        allocate(buckets(num_buckets))

        ! Allocate bucket arrays
        do i = 1, num_buckets
            allocate(buckets(i)%values(n))
        end do

        min_val = minval(arr)
        max_val = maxval(arr)
        range = max_val - min_val

        ! Distribute elements into buckets
        do i = 1, n
            bucket_index = min(int((arr(i) - min_val) / range * num_buckets) + 1, num_buckets)
            buckets(bucket_index)%count = buckets(bucket_index)%count + 1
            buckets(bucket_index)%values(buckets(bucket_index)%count) = arr(i)
        end do

        ! Sort individual buckets and concatenate
        k = 1
        do i = 1, num_buckets
            if (buckets(i)%count > 0) then
                call insertion_sort_real64(buckets(i)%values(1:buckets(i)%count))
                do j = 1, buckets(i)%count
                    arr(k) = buckets(i)%values(j)
                    k = k + 1
                end do
            end if
        end do

        ! Clean up
        do i = 1, num_buckets
            deallocate(buckets(i)%values)
        end do
        deallocate(buckets)

    end subroutine bucket_sort

    subroutine insertion_sort_real64(arr)
        implicit none
        real(real64), dimension(:), intent(inout) :: arr
        integer(int32) :: i, j, n
        real(real64) :: key

        n = size(arr)

        do i = 2, n
            key = arr(i)
            j = i - 1

            do while (j >= 1 .and. arr(j) > key)
                arr(j + 1) = arr(j)
                j = j - 1
            end do

            arr(j + 1) = key
        end do

    end subroutine insertion_sort_real64

    !===========================================================================
    ! Tim Sort - Hybrid stable sort (simplified version)
    !===========================================================================

    subroutine tim_sort(arr)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), parameter :: MIN_MERGE = 32
        integer(int32) :: n, i, size, start, mid, endpoint

        n = size(arr)

        ! Sort individual runs using insertion sort
        do i = 1, n, MIN_MERGE
            call insertion_sort_range(arr, i, min(i + MIN_MERGE - 1, n))
        end do

        ! Merge sorted runs
        size = MIN_MERGE
        do while (size < n)
            do start = 1, n, size * 2
                mid = start + size - 1
                endpoint = min(start + size * 2 - 1, n)

                if (mid < endpoint) then
                    call merge_int32(arr, start, mid, endpoint)
                end if
            end do
            size = size * 2
        end do

    end subroutine tim_sort

    subroutine insertion_sort_range(arr, low, high)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: low, high
        integer(int32) :: i, j, key

        do i = low + 1, high
            key = arr(i)
            j = i - 1

            do while (j >= low .and. arr(j) > key)
                arr(j + 1) = arr(j)
                j = j - 1
            end do

            arr(j + 1) = key
        end do

    end subroutine insertion_sort_range

    !===========================================================================
    ! Intro Sort - Hybrid of quicksort, heapsort, and insertion sort
    !===========================================================================

    subroutine intro_sort(arr)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32) :: n, max_depth

        n = size(arr)
        max_depth = 2 * int(log(real(n)) / log(2.0))

        call intro_sort_recursive(arr, 1, n, max_depth)

    end subroutine intro_sort

    recursive subroutine intro_sort_recursive(arr, low, high, depth_limit)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: low, high, depth_limit
        integer(int32) :: n, pivot_index

        n = high - low + 1

        if (n <= 16) then
            call insertion_sort_range(arr, low, high)
        else if (depth_limit == 0) then
            call heap_sort_range(arr, low, high)
        else
            pivot_index = partition_int32(arr, low, high)
            call intro_sort_recursive(arr, low, pivot_index - 1, depth_limit - 1)
            call intro_sort_recursive(arr, pivot_index + 1, high, depth_limit - 1)
        end if

    end subroutine intro_sort_recursive

    subroutine heap_sort_range(arr, low, high)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: low, high
        ! Implementation similar to heap_sort but on a range
        ! For brevity, calling standard heap_sort on sub-array
        call heap_sort_int32(arr(low:high))

    end subroutine heap_sort_range

    !===========================================================================
    ! Parallel Quick Sort - Using OpenMP
    !===========================================================================

    subroutine parallel_quick_sort(arr)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr

        !$OMP PARALLEL
        !$OMP SINGLE
        call parallel_quick_sort_recursive(arr, 1, size(arr))
        !$OMP END SINGLE
        !$OMP END PARALLEL

    end subroutine parallel_quick_sort

    recursive subroutine parallel_quick_sort_recursive(arr, low, high)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32), intent(in) :: low, high
        integer(int32) :: pivot_index

        if (low < high) then
            pivot_index = partition_int32(arr, low, high)

            !$OMP TASK SHARED(arr) IF(high - low > 1000)
            call parallel_quick_sort_recursive(arr, low, pivot_index - 1)
            !$OMP END TASK

            !$OMP TASK SHARED(arr) IF(high - low > 1000)
            call parallel_quick_sort_recursive(arr, pivot_index + 1, high)
            !$OMP END TASK

            !$OMP TASKWAIT
        end if

    end subroutine parallel_quick_sort_recursive

    !===========================================================================
    ! Utility Functions
    !===========================================================================

    function is_sorted(arr) result(sorted)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        logical :: sorted
        integer(int32) :: i, n

        n = size(arr)
        sorted = .true.

        do i = 1, n - 1
            if (arr(i) > arr(i + 1)) then
                sorted = .false.
                exit
            end if
        end do

    end function is_sorted

    subroutine shuffle_array(arr)
        implicit none
        integer(int32), dimension(:), intent(inout) :: arr
        integer(int32) :: i, j, n, temp
        real :: r

        n = size(arr)

        do i = n, 2, -1
            call random_number(r)
            j = int(r * i) + 1
            temp = arr(i)
            arr(i) = arr(j)
            arr(j) = temp
        end do

    end subroutine shuffle_array

end module sorting_module