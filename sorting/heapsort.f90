! Heap Sort and Priority Queue Implementation in Modern Fortran
!
! Heap Sort: O(n log n) sorting algorithm using binary heap
! Priority Queue: Efficient data structure for priority-based operations
!
! Concepts:
! - Binary Heap: Complete binary tree satisfying heap property
! - Max Heap: Parent >= Children (for ascending sort)
! - Min Heap: Parent <= Children (for priority queue)
! - Heap Operations: Insert, Extract, Heapify
!
! Author: Algorithms Multiverse

program heapsort_demo
    implicit none

    ! Test arrays
    integer, parameter :: n1 = 10, n2 = 20, n3 = 1000
    integer :: arr1(n1), arr2(n2), arr3(n3)
    real(8) :: start_time, end_time
    integer :: i

    print '(A)', repeat('=', 75)
    print '(A)', '          HEAP SORT AND PRIORITY QUEUE IN FORTRAN'
    print '(A)', repeat('=', 75)
    print *

    ! Test 1: Basic heap sort
    call demo_basic_heapsort()

    ! Test 2: Priority queue operations
    call demo_priority_queue()

    ! Test 3: Performance benchmark
    call demo_performance()

    ! Summary
    print '(A)', repeat('=', 75)
    print '(A)', 'HEAP DATA STRUCTURE'
    print '(A)', repeat('=', 75)
    print '(A)', 'Properties:'
    print '(A)', '- Complete binary tree (all levels filled except possibly last)'
    print '(A)', '- Heap property: Parent-child relationship maintained'
    print '(A)', '- Max Heap: Parent >= Children'
    print '(A)', '- Min Heap: Parent <= Children'
    print '(A)', ''
    print '(A)', 'Operations:'
    print '(A)', '- Insert: O(log n) - Add element and bubble up'
    print '(A)', '- Extract Max/Min: O(log n) - Remove root and heapify'
    print '(A)', '- Peek: O(1) - View root without removing'
    print '(A)', '- Heapify: O(n) - Build heap from array'
    print '(A)', ''
    print '(A)', 'Heap Sort:'
    print '(A)', '- Time: O(n log n) for all cases (best, average, worst)'
    print '(A)', '- Space: O(1) - in-place sorting'
    print '(A)', '- Not stable: equal elements may be reordered'
    print '(A)', '- Good for: Large datasets, guaranteed O(n log n) performance'
    print '(A)', repeat('=', 75)

contains

    ! ===================================================================
    ! BASIC HEAP SORT DEMONSTRATION
    ! ===================================================================

    subroutine demo_basic_heapsort()
        integer :: test_arr(10)

        print '(A)', 'Test 1: Basic Heap Sort'
        print '(A)', repeat('-', 75)

        test_arr = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]

        print '(A)', 'Original array:'
        call print_array(test_arr, 10)

        call heap_sort(test_arr, 10)

        print '(A)', 'Sorted array:'
        call print_array(test_arr, 10)

        if (is_sorted(test_arr, 10)) then
            print '(A)', '✓ Array is sorted correctly'
        else
            print '(A)', '✗ Sorting failed!'
        end if
        print *
    end subroutine demo_basic_heapsort

    ! ===================================================================
    ! HEAP SORT ALGORITHM
    ! ===================================================================

    subroutine heap_sort(arr, n)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: n
        integer :: i, temp

        ! Build max heap
        do i = n / 2, 1, -1
            call heapify(arr, n, i)
        end do

        ! Extract elements from heap one by one
        do i = n, 2, -1
            ! Move current root to end
            temp = arr(1)
            arr(1) = arr(i)
            arr(i) = temp

            ! Heapify the reduced heap
            call heapify(arr, i - 1, 1)
        end do
    end subroutine heap_sort

    ! Heapify a subtree rooted at index i
    ! n is size of heap
    recursive subroutine heapify(arr, n, i)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: n, i
        integer :: largest, left, right, temp

        largest = i
        left = 2 * i
        right = 2 * i + 1

        ! If left child is larger than root
        if (left <= n .and. arr(left) > arr(largest)) then
            largest = left
        end if

        ! If right child is larger than largest so far
        if (right <= n .and. arr(right) > arr(largest)) then
            largest = right
        end if

        ! If largest is not root
        if (largest /= i) then
            temp = arr(i)
            arr(i) = arr(largest)
            arr(largest) = temp

            ! Recursively heapify the affected sub-tree
            call heapify(arr, n, largest)
        end if
    end subroutine heapify

    ! ===================================================================
    ! PRIORITY QUEUE IMPLEMENTATION (MIN HEAP)
    ! ===================================================================

    subroutine demo_priority_queue()
        integer, parameter :: capacity = 20
        integer :: pq(capacity)
        integer :: pq_size
        integer :: value

        print '(A)', 'Test 2: Priority Queue (Min Heap) Operations'
        print '(A)', repeat('-', 75)

        pq_size = 0

        ! Insert elements
        print '(A)', 'Inserting elements: 5, 3, 8, 1, 9, 2, 7'
        call pq_insert(pq, pq_size, capacity, 5)
        call pq_insert(pq, pq_size, capacity, 3)
        call pq_insert(pq, pq_size, capacity, 8)
        call pq_insert(pq, pq_size, capacity, 1)
        call pq_insert(pq, pq_size, capacity, 9)
        call pq_insert(pq, pq_size, capacity, 2)
        call pq_insert(pq, pq_size, capacity, 7)

        print '(A)', 'Priority Queue contents (min heap):'
        call print_array(pq, pq_size)

        ! Extract minimum elements
        print *
        print '(A)', 'Extracting elements in priority order:'

        do while (pq_size > 0)
            value = pq_extract_min(pq, pq_size)
            print '(A, I0)', '  Extracted: ', value
        end do

        print *
        print '(A)', 'Note: Elements extracted in ascending order (min heap property)'
        print *
    end subroutine demo_priority_queue

    ! Insert element into min-heap priority queue
    subroutine pq_insert(heap, size, capacity, value)
        integer, intent(inout) :: heap(:)
        integer, intent(inout) :: size
        integer, intent(in) :: capacity, value
        integer :: i, parent, temp

        if (size >= capacity) then
            print '(A)', 'Error: Priority queue is full!'
            return
        end if

        ! Insert new element at the end
        size = size + 1
        i = size
        heap(i) = value

        ! Bubble up to maintain heap property
        do while (i > 1)
            parent = i / 2
            if (heap(i) < heap(parent)) then
                temp = heap(i)
                heap(i) = heap(parent)
                heap(parent) = temp
                i = parent
            else
                exit
            end if
        end do
    end subroutine pq_insert

    ! Extract minimum element from min-heap
    function pq_extract_min(heap, size) result(min_val)
        integer, intent(inout) :: heap(:)
        integer, intent(inout) :: size
        integer :: min_val
        integer :: i, left, right, smallest, temp

        if (size < 1) then
            print '(A)', 'Error: Priority queue is empty!'
            min_val = -1
            return
        end if

        ! Get minimum (root)
        min_val = heap(1)

        ! Move last element to root
        heap(1) = heap(size)
        size = size - 1

        ! Heapify down
        i = 1
        do while (.true.)
            smallest = i
            left = 2 * i
            right = 2 * i + 1

            if (left <= size .and. heap(left) < heap(smallest)) then
                smallest = left
            end if

            if (right <= size .and. heap(right) < heap(smallest)) then
                smallest = right
            end if

            if (smallest /= i) then
                temp = heap(i)
                heap(i) = heap(smallest)
                heap(smallest) = temp
                i = smallest
            else
                exit
            end if
        end do
    end function pq_extract_min

    ! ===================================================================
    ! PERFORMANCE BENCHMARK
    ! ===================================================================

    subroutine demo_performance()
        integer :: test_sizes(3)
        integer, allocatable :: arr(:)
        integer :: i, j, size
        real(8) :: start, finish

        print '(A)', 'Test 3: Performance Benchmark'
        print '(A)', repeat('-', 75)

        test_sizes = [1000, 5000, 10000]

        print '(A)', 'Heap Sort Performance:'
        print '(A)', 'Size         Time (s)      Elements/sec'
        print '(A)', repeat('-', 50)

        do i = 1, 3
            size = test_sizes(i)
            allocate(arr(size))

            ! Fill with random data
            call random_seed()
            do j = 1, size
                call random_number(start)
                arr(j) = int(start * 10000)
            end do

            ! Benchmark heap sort
            call cpu_time(start)
            call heap_sort(arr, size)
            call cpu_time(finish)

            if (is_sorted(arr, size)) then
                print '(I8, 2X, F10.6, 2X, F12.0)', &
                      size, finish - start, real(size) / (finish - start)
            else
                print '(I8, A)', size, '  ✗ Sort failed!'
            end if

            deallocate(arr)
        end do

        print *
        print '(A)', 'Comparison with other O(n log n) sorts:'
        print '(A)', '- Heap Sort: Guaranteed O(n log n), but larger constant factor'
        print '(A)', '- Quick Sort: Average O(n log n), but O(n²) worst case'
        print '(A)', '- Merge Sort: O(n log n), but requires O(n) extra space'
        print *
    end subroutine demo_performance

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

end program heapsort_demo
