! Queue Data Structure in Modern Fortran
!
! Features:
! - Circular array-based queue (fixed size)
! - Linked-list-based queue (dynamic size)
! - Priority queue (min-heap based)
! - Deque (double-ended queue)
! - Generic operations: enqueue, dequeue, front, isEmpty, isFull
!
! Compilation:
!   gfortran -O2 -o queue queue.f90
!   ./queue
!
! Author: Algorithms Multiverse

module queue_module
    implicit none
    private

    integer, parameter :: QUEUE_MAX_SIZE = 100

    ! Circular Array-based Queue
    type, public :: array_queue
        private
        integer :: data(QUEUE_MAX_SIZE)
        integer :: front = 1
        integer :: rear = 0
        integer :: size = 0
        integer :: capacity = QUEUE_MAX_SIZE
    contains
        procedure, public :: enqueue => array_queue_enqueue
        procedure, public :: dequeue => array_queue_dequeue
        procedure, public :: get_front => array_queue_front
        procedure, public :: is_empty => array_queue_is_empty
        procedure, public :: is_full => array_queue_is_full
        procedure, public :: get_size => array_queue_size
        procedure, public :: clear => array_queue_clear
        procedure, public :: print => array_queue_print
    end type array_queue

    ! Node for linked list queue
    type :: queue_node
        integer :: data
        type(queue_node), pointer :: next => null()
    end type queue_node

    ! Linked-list-based Queue
    type, public :: linked_queue
        private
        type(queue_node), pointer :: front => null()
        type(queue_node), pointer :: rear => null()
        integer :: size = 0
    contains
        procedure, public :: enqueue => linked_queue_enqueue
        procedure, public :: dequeue => linked_queue_dequeue
        procedure, public :: get_front => linked_queue_front
        procedure, public :: is_empty => linked_queue_is_empty
        procedure, public :: get_size => linked_queue_size
        procedure, public :: clear => linked_queue_clear
        procedure, public :: print => linked_queue_print
        procedure, public :: destroy => linked_queue_destroy
    end type linked_queue

    ! Priority Queue (Min-Heap)
    type, public :: priority_queue
        private
        integer :: data(QUEUE_MAX_SIZE)
        integer :: size = 0
        integer :: capacity = QUEUE_MAX_SIZE
    contains
        procedure, public :: insert => pq_insert
        procedure, public :: extract_min => pq_extract_min
        procedure, public :: get_min => pq_get_min
        procedure, public :: is_empty => pq_is_empty
        procedure, public :: is_full => pq_is_full
        procedure, public :: get_size => pq_size
        procedure, public :: clear => pq_clear
        procedure, public :: print => pq_print
    end type priority_queue

    ! Deque (Double-Ended Queue)
    type, public :: deque
        private
        integer :: data(QUEUE_MAX_SIZE)
        integer :: front = 1
        integer :: rear = 0
        integer :: size = 0
        integer :: capacity = QUEUE_MAX_SIZE
    contains
        procedure, public :: push_front => deque_push_front
        procedure, public :: push_back => deque_push_back
        procedure, public :: pop_front => deque_pop_front
        procedure, public :: pop_back => deque_pop_back
        procedure, public :: get_front => deque_get_front
        procedure, public :: get_back => deque_get_back
        procedure, public :: is_empty => deque_is_empty
        procedure, public :: is_full => deque_is_full
        procedure, public :: get_size => deque_size
        procedure, public :: print => deque_print
    end type deque

contains

    ! ========================================================================
    ! CIRCULAR ARRAY-BASED QUEUE IMPLEMENTATION
    ! ========================================================================

    subroutine array_queue_enqueue(this, value)
        class(array_queue), intent(inout) :: this
        integer, intent(in) :: value

        if (this%size >= this%capacity) then
            print *, 'Error: Queue overflow!'
            return
        end if

        this%rear = mod(this%rear, this%capacity) + 1
        this%data(this%rear) = value
        this%size = this%size + 1
    end subroutine array_queue_enqueue

    function array_queue_dequeue(this) result(value)
        class(array_queue), intent(inout) :: this
        integer :: value

        if (this%size == 0) then
            print *, 'Error: Queue underflow!'
            value = -999999
            return
        end if

        value = this%data(this%front)
        this%front = mod(this%front, this%capacity) + 1
        this%size = this%size - 1
    end function array_queue_dequeue

    function array_queue_front(this) result(value)
        class(array_queue), intent(in) :: this
        integer :: value

        if (this%size == 0) then
            print *, 'Error: Queue is empty!'
            value = -999999
            return
        end if

        value = this%data(this%front)
    end function array_queue_front

    function array_queue_is_empty(this) result(empty)
        class(array_queue), intent(in) :: this
        logical :: empty
        empty = (this%size == 0)
    end function array_queue_is_empty

    function array_queue_is_full(this) result(full)
        class(array_queue), intent(in) :: this
        logical :: full
        full = (this%size >= this%capacity)
    end function array_queue_is_full

    function array_queue_size(this) result(size)
        class(array_queue), intent(in) :: this
        integer :: size
        size = this%size
    end function array_queue_size

    subroutine array_queue_clear(this)
        class(array_queue), intent(inout) :: this
        this%front = 1
        this%rear = 0
        this%size = 0
    end subroutine array_queue_clear

    subroutine array_queue_print(this)
        class(array_queue), intent(in) :: this
        integer :: i, idx

        if (this%size == 0) then
            print *, 'Queue is empty'
            return
        end if

        write(*, '(A)', advance='no') 'Queue (front to rear): '
        idx = this%front
        do i = 1, this%size
            write(*, '(I0, 1X)', advance='no') this%data(idx)
            idx = mod(idx, this%capacity) + 1
        end do
        print *
    end subroutine array_queue_print

    ! ========================================================================
    ! LINKED-LIST-BASED QUEUE IMPLEMENTATION
    ! ========================================================================

    subroutine linked_queue_enqueue(this, value)
        class(linked_queue), intent(inout) :: this
        integer, intent(in) :: value
        type(queue_node), pointer :: new_node

        allocate(new_node)
        new_node%data = value
        new_node%next => null()

        if (.not. associated(this%rear)) then
            this%front => new_node
            this%rear => new_node
        else
            this%rear%next => new_node
            this%rear => new_node
        end if

        this%size = this%size + 1
    end subroutine linked_queue_enqueue

    function linked_queue_dequeue(this) result(value)
        class(linked_queue), intent(inout) :: this
        integer :: value
        type(queue_node), pointer :: temp

        if (.not. associated(this%front)) then
            print *, 'Error: Queue underflow!'
            value = -999999
            return
        end if

        value = this%front%data
        temp => this%front
        this%front => this%front%next

        if (.not. associated(this%front)) then
            this%rear => null()
        end if

        deallocate(temp)
        this%size = this%size - 1
    end function linked_queue_dequeue

    function linked_queue_front(this) result(value)
        class(linked_queue), intent(in) :: this
        integer :: value

        if (.not. associated(this%front)) then
            print *, 'Error: Queue is empty!'
            value = -999999
            return
        end if

        value = this%front%data
    end function linked_queue_front

    function linked_queue_is_empty(this) result(empty)
        class(linked_queue), intent(in) :: this
        logical :: empty
        empty = .not. associated(this%front)
    end function linked_queue_is_empty

    function linked_queue_size(this) result(size)
        class(linked_queue), intent(in) :: this
        integer :: size
        size = this%size
    end function linked_queue_size

    subroutine linked_queue_clear(this)
        class(linked_queue), intent(inout) :: this
        call this%destroy()
    end subroutine linked_queue_clear

    subroutine linked_queue_print(this)
        class(linked_queue), intent(in) :: this
        type(queue_node), pointer :: current

        if (.not. associated(this%front)) then
            print *, 'Queue is empty'
            return
        end if

        write(*, '(A)', advance='no') 'Queue (front to rear): '
        current => this%front
        do while (associated(current))
            write(*, '(I0, 1X)', advance='no') current%data
            current => current%next
        end do
        print *
    end subroutine linked_queue_print

    subroutine linked_queue_destroy(this)
        class(linked_queue), intent(inout) :: this
        type(queue_node), pointer :: current, next_node

        current => this%front
        do while (associated(current))
            next_node => current%next
            deallocate(current)
            current => next_node
        end do

        this%front => null()
        this%rear => null()
        this%size = 0
    end subroutine linked_queue_destroy

    ! ========================================================================
    ! PRIORITY QUEUE (MIN-HEAP) IMPLEMENTATION
    ! ========================================================================

    subroutine pq_insert(this, value)
        class(priority_queue), intent(inout) :: this
        integer, intent(in) :: value
        integer :: i, parent

        if (this%size >= this%capacity) then
            print *, 'Error: Priority queue is full!'
            return
        end if

        this%size = this%size + 1
        i = this%size
        this%data(i) = value

        ! Bubble up
        do while (i > 1)
            parent = i / 2
            if (this%data(i) < this%data(parent)) then
                call swap(this%data(i), this%data(parent))
                i = parent
            else
                exit
            end if
        end do
    end subroutine pq_insert

    function pq_extract_min(this) result(min_val)
        class(priority_queue), intent(inout) :: this
        integer :: min_val

        if (this%size == 0) then
            print *, 'Error: Priority queue is empty!'
            min_val = -999999
            return
        end if

        min_val = this%data(1)
        this%data(1) = this%data(this%size)
        this%size = this%size - 1

        call heapify_down(this%data, this%size, 1)
    end function pq_extract_min

    function pq_get_min(this) result(min_val)
        class(priority_queue), intent(in) :: this
        integer :: min_val

        if (this%size == 0) then
            print *, 'Error: Priority queue is empty!'
            min_val = -999999
            return
        end if

        min_val = this%data(1)
    end function pq_get_min

    function pq_is_empty(this) result(empty)
        class(priority_queue), intent(in) :: this
        logical :: empty
        empty = (this%size == 0)
    end function pq_is_empty

    function pq_is_full(this) result(full)
        class(priority_queue), intent(in) :: this
        logical :: full
        full = (this%size >= this%capacity)
    end function pq_is_full

    function pq_size(this) result(size)
        class(priority_queue), intent(in) :: this
        integer :: size
        size = this%size
    end function pq_size

    subroutine pq_clear(this)
        class(priority_queue), intent(inout) :: this
        this%size = 0
    end subroutine pq_clear

    subroutine pq_print(this)
        class(priority_queue), intent(in) :: this
        integer :: i

        if (this%size == 0) then
            print *, 'Priority queue is empty'
            return
        end if

        write(*, '(A)', advance='no') 'Priority Queue (heap): '
        do i = 1, this%size
            write(*, '(I0, 1X)', advance='no') this%data(i)
        end do
        print *
    end subroutine pq_print

    recursive subroutine heapify_down(arr, n, i)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: n, i
        integer :: smallest, left, right

        smallest = i
        left = 2 * i
        right = 2 * i + 1

        if (left <= n .and. arr(left) < arr(smallest)) then
            smallest = left
        end if

        if (right <= n .and. arr(right) < arr(smallest)) then
            smallest = right
        end if

        if (smallest /= i) then
            call swap(arr(i), arr(smallest))
            call heapify_down(arr, n, smallest)
        end if
    end subroutine heapify_down

    ! ========================================================================
    ! DEQUE (DOUBLE-ENDED QUEUE) IMPLEMENTATION
    ! ========================================================================

    subroutine deque_push_front(this, value)
        class(deque), intent(inout) :: this
        integer, intent(in) :: value

        if (this%size >= this%capacity) then
            print *, 'Error: Deque is full!'
            return
        end if

        this%front = this%front - 1
        if (this%front < 1) this%front = this%capacity
        this%data(this%front) = value
        this%size = this%size + 1
    end subroutine deque_push_front

    subroutine deque_push_back(this, value)
        class(deque), intent(inout) :: this
        integer, intent(in) :: value

        if (this%size >= this%capacity) then
            print *, 'Error: Deque is full!'
            return
        end if

        this%rear = mod(this%rear, this%capacity) + 1
        this%data(this%rear) = value
        this%size = this%size + 1
    end subroutine deque_push_back

    function deque_pop_front(this) result(value)
        class(deque), intent(inout) :: this
        integer :: value

        if (this%size == 0) then
            print *, 'Error: Deque is empty!'
            value = -999999
            return
        end if

        value = this%data(this%front)
        this%front = mod(this%front, this%capacity) + 1
        this%size = this%size - 1
    end function deque_pop_front

    function deque_pop_back(this) result(value)
        class(deque), intent(inout) :: this
        integer :: value

        if (this%size == 0) then
            print *, 'Error: Deque is empty!'
            value = -999999
            return
        end if

        value = this%data(this%rear)
        this%rear = this%rear - 1
        if (this%rear < 1) this%rear = this%capacity
        this%size = this%size - 1
    end function deque_pop_back

    function deque_get_front(this) result(value)
        class(deque), intent(in) :: this
        integer :: value

        if (this%size == 0) then
            print *, 'Error: Deque is empty!'
            value = -999999
            return
        end if

        value = this%data(this%front)
    end function deque_get_front

    function deque_get_back(this) result(value)
        class(deque), intent(in) :: this
        integer :: value

        if (this%size == 0) then
            print *, 'Error: Deque is empty!'
            value = -999999
            return
        end if

        value = this%data(this%rear)
    end function deque_get_back

    function deque_is_empty(this) result(empty)
        class(deque), intent(in) :: this
        logical :: empty
        empty = (this%size == 0)
    end function deque_is_empty

    function deque_is_full(this) result(full)
        class(deque), intent(in) :: this
        logical :: full
        full = (this%size >= this%capacity)
    end function deque_is_full

    function deque_size(this) result(size)
        class(deque), intent(in) :: this
        integer :: size
        size = this%size
    end function deque_size

    subroutine deque_print(this)
        class(deque), intent(in) :: this
        integer :: i, idx

        if (this%size == 0) then
            print *, 'Deque is empty'
            return
        end if

        write(*, '(A)', advance='no') 'Deque (front to back): '
        idx = this%front
        do i = 1, this%size
            write(*, '(I0, 1X)', advance='no') this%data(idx)
            idx = mod(idx, this%capacity) + 1
        end do
        print *
    end subroutine deque_print

    ! ========================================================================
    ! UTILITY FUNCTIONS
    ! ========================================================================

    subroutine swap(a, b)
        integer, intent(inout) :: a, b
        integer :: temp
        temp = a
        a = b
        b = temp
    end subroutine swap

end module queue_module

! ============================================================================
! DEMONSTRATION PROGRAM
! ============================================================================

program test_queue
    use queue_module
    implicit none

    type(array_queue) :: aqueue
    type(linked_queue) :: lqueue
    type(priority_queue) :: pqueue
    type(deque) :: dq
    integer :: i, value

    print '(A)', repeat('=', 75)
    print '(A)', '                   QUEUE - FORTRAN'
    print '(A)', repeat('=', 75)
    print *

    ! Test 1: Array-based queue
    print '(A)', 'Test 1: Circular Array-Based Queue'
    print '(A)', repeat('-', 75)

    print *, 'Enqueuing: 10, 20, 30, 40, 50'
    call aqueue%enqueue(10)
    call aqueue%enqueue(20)
    call aqueue%enqueue(30)
    call aqueue%enqueue(40)
    call aqueue%enqueue(50)

    call aqueue%print()
    print '(A, I0)', 'Size: ', aqueue%get_size()
    print '(A, I0)', 'Front element: ', aqueue%get_front()
    print *

    print *, 'Dequeuing 2 elements...'
    value = aqueue%dequeue()
    print '(A, I0)', 'Dequeued: ', value
    value = aqueue%dequeue()
    print '(A, I0)', 'Dequeued: ', value
    call aqueue%print()
    print *

    ! Test 2: Linked-list-based queue
    print '(A)', 'Test 2: Linked-List-Based Queue'
    print '(A)', repeat('-', 75)

    print *, 'Enqueuing: 100, 200, 300, 400, 500'
    call lqueue%enqueue(100)
    call lqueue%enqueue(200)
    call lqueue%enqueue(300)
    call lqueue%enqueue(400)
    call lqueue%enqueue(500)

    call lqueue%print()
    print '(A, I0)', 'Size: ', lqueue%get_size()
    print *

    print *, 'Dequeuing 3 elements...'
    do i = 1, 3
        value = lqueue%dequeue()
        print '(A, I0)', 'Dequeued: ', value
    end do
    call lqueue%print()
    print *

    ! Test 3: Priority queue
    print '(A)', 'Test 3: Priority Queue (Min-Heap)'
    print '(A)', repeat('-', 75)

    print *, 'Inserting: 50, 30, 70, 20, 40, 60, 10'
    call pqueue%insert(50)
    call pqueue%insert(30)
    call pqueue%insert(70)
    call pqueue%insert(20)
    call pqueue%insert(40)
    call pqueue%insert(60)
    call pqueue%insert(10)

    call pqueue%print()
    print '(A, I0)', 'Minimum element: ', pqueue%get_min()
    print *

    print *, 'Extracting minimum elements:'
    do i = 1, 3
        value = pqueue%extract_min()
        print '(A, I0)', 'Extracted: ', value
    end do
    call pqueue%print()
    print *

    ! Test 4: Deque
    print '(A)', 'Test 4: Deque (Double-Ended Queue)'
    print '(A)', repeat('-', 75)

    print *, 'Push front: 30, 20, 10'
    call dq%push_front(30)
    call dq%push_front(20)
    call dq%push_front(10)

    print *, 'Push back: 40, 50, 60'
    call dq%push_back(40)
    call dq%push_back(50)
    call dq%push_back(60)

    call dq%print()
    print '(A, I0)', 'Front: ', dq%get_front()
    print '(A, I0)', 'Back: ', dq%get_back()
    print *

    print *, 'Pop front twice, pop back once'
    value = dq%pop_front()
    print '(A, I0)', 'Popped from front: ', value
    value = dq%pop_front()
    print '(A, I0)', 'Popped from front: ', value
    value = dq%pop_back()
    print '(A, I0)', 'Popped from back: ', value
    call dq%print()
    print *

    ! Summary
    print '(A)', repeat('=', 75)
    print '(A)', 'QUEUE COMPLEXITY SUMMARY'
    print '(A)', repeat('=', 75)
    print '(A)', 'Type             Enqueue  Dequeue  Front   Space'
    print '(A)', repeat('-', 75)
    print '(A)', 'Array Queue      O(1)     O(1)     O(1)    O(n)'
    print '(A)', 'Linked Queue     O(1)     O(1)     O(1)    O(n)'
    print '(A)', 'Priority Queue   O(log n) O(log n) O(1)    O(n)'
    print '(A)', 'Deque            O(1)     O(1)     O(1)    O(n)'
    print '(A)', ''
    print '(A)', 'Applications:'
    print '(A)', '- Task scheduling (FIFO)'
    print '(A)', '- Breadth-First Search (BFS)'
    print '(A)', '- Print spooling'
    print '(A)', '- Request handling in servers'
    print '(A)', '- Priority Queue: Dijkstra''s algorithm, event simulation'
    print '(A)', '- Deque: Sliding window problems, palindrome checking'
    print '(A)', repeat('=', 75)

    ! Cleanup
    call lqueue%destroy()

end program test_queue
