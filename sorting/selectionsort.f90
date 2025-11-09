! Selection Sort Algorithm - Educational Implementation (Fortran 90+)
!
! ALGORITHM OVERVIEW:
! ==================
! Selection Sort works by repeatedly finding the minimum element from the unsorted
! portion of the array and placing it at the beginning. It divides the array into
! two parts: a sorted portion (left) and an unsorted portion (right).
!
! Time Complexity:
! - Best Case: O(n²) - Even if array is already sorted, still searches for minimum
! - Average Case: O(n²)
! - Worst Case: O(n²)
! - IMPORTANT: Unlike bubble sort and insertion sort, selection sort ALWAYS performs
!   O(n²) comparisons, regardless of input
!
! Space Complexity: O(1) - Sorts in-place with only constant extra space
!
! Stability: NOT stable by default (can be made stable with modifications)
! In-place: YES
!
! KEY ADVANTAGE: Makes MINIMUM number of swaps - only O(n) swaps!
! This is critical when writing to memory is expensive (flash, EEPROM, etc.)

program selection_sort_demo
    implicit none

    ! Test arrays
    integer, parameter :: N1 = 5, N2 = 7, N3 = 9
    integer :: test1(N1), test2(N2), test3(N3)
    integer :: i

    print *, '======================================================================'
    print *, 'SELECTION SORT - EDUCATIONAL DEMONSTRATION (Fortran)'
    print *, '======================================================================'

    ! Initialize test arrays
    test1 = (/ 64, 25, 12, 22, 11 /)
    test2 = (/ 5, 2, 8, 6, 1, 9, 4 /)
    test3 = (/ 9, 8, 7, 6, 5, 4, 3, 2, 1 /)

    ! Test 1: Random array
    print *, ''
    print *, 'Test 1: Random array'
    print *, 'Original:', test1
    call selection_sort(test1, N1)
    print *, 'Sorted:  ', test1
    print *, 'Status:  ', merge('PASS', 'FAIL', is_sorted(test1, N1))

    ! Test 2: Small random array
    print *, ''
    print *, 'Test 2: Small random array'
    print *, 'Original:', test2
    call selection_sort(test2, N2)
    print *, 'Sorted:  ', test2
    print *, 'Status:  ', merge('PASS', 'FAIL', is_sorted(test2, N2))

    ! Test 3: Reverse sorted
    print *, ''
    print *, 'Test 3: Reverse sorted'
    print *, 'Original:', test3
    call selection_sort(test3, N3)
    print *, 'Sorted:  ', test3
    print *, 'Status:  ', merge('PASS', 'FAIL', is_sorted(test3, N3))

    ! Detailed visualization
    print *, ''
    print *, ''
    print *, '======================================================================'
    print *, 'STEP-BY-STEP VISUALIZATION'
    print *, '======================================================================'
    call visualize_selection_sort()

    ! Memory analysis
    print *, ''
    print *, ''
    print *, '======================================================================'
    print *, 'MEMORY USAGE ANALYSIS'
    print *, '======================================================================'
    print *, ''
    print *, 'Selection Sort Memory Characteristics:'
    print *, ''
    print *, '1. In-Place Sorting:'
    print *, '   - Space Complexity: O(1) auxiliary space'
    print *, '   - Only uses constant extra memory (min_idx, temp, loop variables)'
    print *, '   - Original array is modified in-place'
    print *, ''
    print *, '2. Memory Writes:'
    print *, '   - Selection Sort: O(n) swaps (minimum writes)'
    print *, '   - Bubble Sort: O(n²) swaps in worst case'
    print *, '   - Insertion Sort: O(n²) shifts in worst case'
    print *, ''
    print *, '   ⭐ This makes Selection Sort ideal when writing to memory is expensive!'
    print *, '      Examples: Flash memory, EEPROM, or distributed systems'
    print *, ''
    print *, '3. Fortran-Specific:'
    print *, '   - Arrays are passed by reference (efficient)'
    print *, '   - Column-major ordering (affects cache performance)'
    print *, '   - No automatic bounds checking (use -fbounds-check for safety)'

    print *, ''
    print *, ''
    print *, '======================================================================'
    print *, 'WHEN TO USE SELECTION SORT'
    print *, '======================================================================'
    print *, ''
    print *, '✅ GOOD USE CASES:'
    print *, ''
    print *, '1. Minimal Memory Writes:'
    print *, '   - Flash memory or EEPROM (limited write cycles)'
    print *, '   - Distributed systems where network writes are expensive'
    print *, ''
    print *, '2. Small Datasets:'
    print *, '   - When simplicity matters more than efficiency'
    print *, '   - Scientific computing with small arrays'
    print *, ''
    print *, '3. Known Small Data:'
    print *, '   - Fortran scientific applications with fixed-size arrays'
    print *, '   - When n is guaranteed to be small (< 20 elements)'
    print *, ''
    print *, '❌ POOR USE CASES:'
    print *, ''
    print *, '1. Large Datasets:'
    print *, '   - Always O(n²) time, never adapts to input'
    print *, '   - Much slower than O(n log n) algorithms'
    print *, ''
    print *, '2. Nearly Sorted Data:'
    print *, '   - Unlike insertion sort, does not benefit from sorted input'
    print *, '   - Still performs all O(n²) comparisons'
    print *, ''
    print *, '3. Real-time Systems:'
    print *, '   - Non-adaptive nature means worst-case is always hit'
    print *, '   - Insertion sort or merge sort preferred'

    print *, ''
    print *, '✨ Selection Sort demonstration complete!'

contains

    ! ========================================================================
    ! STANDARD SELECTION SORT
    ! ========================================================================

    ! Standard selection sort implementation for integer arrays.
    !
    ! ALGORITHM STEPS:
    ! ===============
    ! 1. Find the minimum element in the unsorted portion
    ! 2. Swap it with the first element of the unsorted portion
    ! 3. Move the boundary of sorted/unsorted portions one element to the right
    ! 4. Repeat until the entire array is sorted
    !
    ! Visual Example:
    ! ==============
    ! Initial: [64, 25, 12, 22, 11]
    !
    ! Pass 1: Find min in [64, 25, 12, 22, 11] → 11
    !         Swap 64 ↔ 11
    !         Result: [11, 25, 12, 22, 64]
    !                  ^^^ sorted portion
    !
    ! Pass 2: Find min in [25, 12, 22, 64] → 12
    !         Swap 25 ↔ 12
    !         Result: [11, 12, 25, 22, 64]
    !                  ^^^^^^^ sorted portion
    !
    ! Time: O(n²), Space: O(1)
    !
    ! Arguments:
    !   arr - Array to sort (modified in-place)
    !   n   - Size of the array
    subroutine selection_sort(arr, n)
        implicit none
        integer, intent(in) :: n
        integer, intent(inout) :: arr(n)
        integer :: i, j, min_idx, temp

        ! Outer loop: Move boundary of unsorted subarray one by one
        do i = 1, n-1
            ! Find the minimum element in the remaining unsorted array
            ! Start by assuming the first unsorted element is the minimum
            min_idx = i

            ! Inner loop: Search for the minimum in arr(i+1:n)
            do j = i+1, n
                ! If we find a smaller element, update min_idx
                if (arr(j) < arr(min_idx)) then
                    min_idx = j
                end if
            end do

            ! Swap the found minimum element with the first element
            ! of the unsorted portion (only if different)
            if (min_idx /= i) then
                temp = arr(i)
                arr(i) = arr(min_idx)
                arr(min_idx) = temp
            end if
        end do
    end subroutine selection_sort

    ! ========================================================================
    ! BIDIRECTIONAL SELECTION SORT
    ! ========================================================================

    ! Bidirectional selection sort (also called "double selection sort").
    !
    ! OPTIMIZATION:
    ! ============
    ! Instead of finding just the minimum in each pass, we find BOTH the minimum
    ! and maximum elements. We place the minimum at the beginning and the maximum
    ! at the end, reducing the number of passes by approximately half.
    !
    ! Time: Still O(n²), but approximately 2x faster in practice
    subroutine bidirectional_selection_sort(arr, n)
        implicit none
        integer, intent(in) :: n
        integer, intent(inout) :: arr(n)
        integer :: left, right, i
        integer :: min_idx, max_idx, temp

        ! Process from both ends toward the middle
        left = 1
        right = n

        do while (left < right)
            ! Find both minimum and maximum in the current range
            min_idx = left
            max_idx = left

            do i = left, right
                if (arr(i) < arr(min_idx)) then
                    min_idx = i
                end if
                if (arr(i) > arr(max_idx)) then
                    max_idx = i
                end if
            end do

            ! Handle special case: if min is at right position
            if (min_idx == right) then
                temp = arr(left)
                arr(left) = arr(right)
                arr(right) = temp
                if (max_idx == left) then
                    max_idx = right
                end if
            else
                ! Swap minimum to the left boundary
                if (min_idx /= left) then
                    temp = arr(left)
                    arr(left) = arr(min_idx)
                    arr(min_idx) = temp
                end if

                ! If maximum was at left position, it's now at min_idx
                if (max_idx == left) then
                    max_idx = min_idx
                end if

                ! Swap maximum to the right boundary
                if (max_idx /= right) then
                    temp = arr(right)
                    arr(right) = arr(max_idx)
                    arr(max_idx) = temp
                end if
            end if

            ! Move boundaries inward
            left = left + 1
            right = right - 1
        end do
    end subroutine bidirectional_selection_sort

    ! ========================================================================
    ! RECURSIVE SELECTION SORT
    ! ========================================================================

    ! Recursive implementation of selection sort.
    !
    ! RECURSIVE APPROACH:
    ! ==================
    ! Base case: Array of size 0 or 1 is already sorted
    ! Recursive case:
    !     1. Find the minimum element in the array
    !     2. Swap it with the first element
    !     3. Recursively sort the rest of the array (excluding the first element)
    !
    ! Time: O(n²), Space: O(n) for recursion stack
    recursive subroutine selection_sort_recursive(arr, n, start_idx)
        implicit none
        integer, intent(in) :: n, start_idx
        integer, intent(inout) :: arr(n)
        integer :: i, min_idx, temp

        ! Base case: if we've reached the end, we're done
        if (start_idx >= n) return

        ! Find the minimum element in arr(start_idx:n)
        min_idx = start_idx
        do i = start_idx+1, n
            if (arr(i) < arr(min_idx)) then
                min_idx = i
            end if
        end do

        ! Swap the minimum with the element at start_idx
        if (min_idx /= start_idx) then
            temp = arr(start_idx)
            arr(start_idx) = arr(min_idx)
            arr(min_idx) = temp
        end if

        ! Recursively sort the rest
        call selection_sort_recursive(arr, n, start_idx + 1)
    end subroutine selection_sort_recursive

    ! ========================================================================
    ! STABLE SELECTION SORT
    ! ========================================================================

    ! Stable version of selection sort.
    !
    ! WHY STANDARD SELECTION SORT IS UNSTABLE:
    ! ========================================
    ! When we swap the minimum element with the first element of the unsorted
    ! portion, we can change the relative order of equal elements.
    !
    ! MAKING IT STABLE:
    ! ================
    ! Instead of swapping, we shift all elements and insert the minimum
    ! at the correct position. This preserves the relative order.
    !
    ! Time: O(n²) comparisons + O(n²) shifts
    subroutine stable_selection_sort(arr, n)
        implicit none
        integer, intent(in) :: n
        integer, intent(inout) :: arr(n)
        integer :: i, j, k, min_idx, min_value

        do i = 1, n-1
            ! Find minimum in unsorted portion
            min_idx = i
            do j = i+1, n
                if (arr(j) < arr(min_idx)) then
                    min_idx = j
                end if
            end do

            ! Instead of swapping, shift elements and insert
            if (min_idx /= i) then
                min_value = arr(min_idx)
                ! Shift all elements between i and min_idx one position right
                do k = min_idx, i+1, -1
                    arr(k) = arr(k-1)
                end do
                ! Place minimum at position i
                arr(i) = min_value
            end if
        end do
    end subroutine stable_selection_sort

    ! ========================================================================
    ! UTILITY FUNCTIONS
    ! ========================================================================

    ! Check if an array is sorted in ascending order
    logical function is_sorted(arr, n)
        implicit none
        integer, intent(in) :: n
        integer, intent(in) :: arr(n)
        integer :: i

        is_sorted = .true.
        do i = 1, n-1
            if (arr(i) > arr(i+1)) then
                is_sorted = .false.
                return
            end if
        end do
    end function is_sorted

    ! Print an array
    subroutine print_array(arr, n, label)
        implicit none
        integer, intent(in) :: n
        integer, intent(in) :: arr(n)
        character(len=*), intent(in) :: label
        integer :: i

        write(*, '(A)', advance='no') label
        write(*, '(A)', advance='no') ' ['
        do i = 1, n
            if (i < n) then
                write(*, '(I3, A)', advance='no') arr(i), ','
            else
                write(*, '(I3)', advance='no') arr(i)
            end if
        end do
        write(*, '(A)') ']'
    end subroutine print_array

    ! ========================================================================
    ! VISUALIZATION
    ! ========================================================================

    ! Create ASCII visualization of selection sort process
    subroutine visualize_selection_sort()
        implicit none
        integer, parameter :: N = 5
        integer :: arr(N)
        integer :: i, j, min_idx, temp

        ! Initialize array
        arr = (/ 64, 25, 12, 22, 11 /)

        print *, ''
        call print_array(arr, N, 'Initial array:')
        print *, ''

        ! Sort with visualization
        do i = 1, N-1
            print *, 'Pass ', i, ':'
            write(*, '(A)', advance='no') '  Looking for minimum in unsorted portion: ['
            do j = i, N
                if (j < N) then
                    write(*, '(I3, A)', advance='no') arr(j), ','
                else
                    write(*, '(I3)', advance='no') arr(j)
                end if
            end do
            print *, ']'

            min_idx = i
            do j = i+1, N
                if (arr(j) < arr(min_idx)) then
                    min_idx = j
                    print *, '    Found new minimum:', arr(min_idx), ' at index', min_idx
                end if
            end do

            if (min_idx /= i) then
                print *, '  Swapping', arr(i), '↔', arr(min_idx)
                temp = arr(i)
                arr(i) = arr(min_idx)
                arr(min_idx) = temp
            else
                print *, '  No swap needed (minimum already in place)'
            end if

            write(*, '(A)', advance='no') '  Sorted: ['
            do j = 1, i
                if (j < i) then
                    write(*, '(I3, A)', advance='no') arr(j), ','
                else
                    write(*, '(I3)', advance='no') arr(j)
                end if
            end do
            write(*, '(A)', advance='no') '] | Unsorted: ['
            if (i < N) then
                do j = i+1, N
                    if (j < N) then
                        write(*, '(I3, A)', advance='no') arr(j), ','
                    else
                        write(*, '(I3)', advance='no') arr(j)
                    end if
                end do
            end if
            print *, ']'
            print *, ''
        end do

        call print_array(arr, N, 'Final sorted array:')
    end subroutine visualize_selection_sort

end program selection_sort_demo
