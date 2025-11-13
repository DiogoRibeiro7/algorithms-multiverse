! Stack Data Structure in Modern Fortran
!
! Features:
! - Array-based stack (fixed size)
! - Linked-list-based stack (dynamic size)
! - Generic operations: push, pop, peek, isEmpty, isFull
! - Multiple data type support (integer, real)
! - Stack applications: expression evaluation, bracket matching
!
! Compilation:
!   gfortran -O2 -o stack stack.f90
!   ./stack
!
! Author: Algorithms Multiverse

module stack_module
    implicit none
    private

    integer, parameter :: STACK_MAX_SIZE = 100

    ! Array-based Stack
    type, public :: array_stack
        private
        integer :: data(STACK_MAX_SIZE)
        integer :: top = 0
        integer :: capacity = STACK_MAX_SIZE
    contains
        procedure, public :: push => array_stack_push
        procedure, public :: pop => array_stack_pop
        procedure, public :: peek => array_stack_peek
        procedure, public :: is_empty => array_stack_is_empty
        procedure, public :: is_full => array_stack_is_full
        procedure, public :: get_size => array_stack_size
        procedure, public :: clear => array_stack_clear
        procedure, public :: print => array_stack_print
    end type array_stack

    ! Node for linked list stack
    type :: stack_node
        integer :: data
        type(stack_node), pointer :: next => null()
    end type stack_node

    ! Linked-list-based Stack
    type, public :: linked_stack
        private
        type(stack_node), pointer :: top => null()
        integer :: size = 0
    contains
        procedure, public :: push => linked_stack_push
        procedure, public :: pop => linked_stack_pop
        procedure, public :: peek => linked_stack_peek
        procedure, public :: is_empty => linked_stack_is_empty
        procedure, public :: get_size => linked_stack_size
        procedure, public :: clear => linked_stack_clear
        procedure, public :: print => linked_stack_print
        procedure, public :: destroy => linked_stack_destroy
    end type linked_stack

contains

    ! ========================================================================
    ! ARRAY-BASED STACK IMPLEMENTATION
    ! ========================================================================

    subroutine array_stack_push(this, value)
        class(array_stack), intent(inout) :: this
        integer, intent(in) :: value

        if (this%top >= this%capacity) then
            print *, 'Error: Stack overflow!'
            return
        end if

        this%top = this%top + 1
        this%data(this%top) = value
    end subroutine array_stack_push

    function array_stack_pop(this) result(value)
        class(array_stack), intent(inout) :: this
        integer :: value

        if (this%top == 0) then
            print *, 'Error: Stack underflow!'
            value = -999999  ! Error value
            return
        end if

        value = this%data(this%top)
        this%top = this%top - 1
    end function array_stack_pop

    function array_stack_peek(this) result(value)
        class(array_stack), intent(in) :: this
        integer :: value

        if (this%top == 0) then
            print *, 'Error: Stack is empty!'
            value = -999999  ! Error value
            return
        end if

        value = this%data(this%top)
    end function array_stack_peek

    function array_stack_is_empty(this) result(empty)
        class(array_stack), intent(in) :: this
        logical :: empty

        empty = (this%top == 0)
    end function array_stack_is_empty

    function array_stack_is_full(this) result(full)
        class(array_stack), intent(in) :: this
        logical :: full

        full = (this%top >= this%capacity)
    end function array_stack_is_full

    function array_stack_size(this) result(size)
        class(array_stack), intent(in) :: this
        integer :: size

        size = this%top
    end function array_stack_size

    subroutine array_stack_clear(this)
        class(array_stack), intent(inout) :: this

        this%top = 0
    end subroutine array_stack_clear

    subroutine array_stack_print(this)
        class(array_stack), intent(in) :: this
        integer :: i

        if (this%top == 0) then
            print *, 'Stack is empty'
            return
        end if

        write(*, '(A)', advance='no') 'Stack (top to bottom): '
        do i = this%top, 1, -1
            write(*, '(I0, 1X)', advance='no') this%data(i)
        end do
        print *
    end subroutine array_stack_print

    ! ========================================================================
    ! LINKED-LIST-BASED STACK IMPLEMENTATION
    ! ========================================================================

    subroutine linked_stack_push(this, value)
        class(linked_stack), intent(inout) :: this
        integer, intent(in) :: value
        type(stack_node), pointer :: new_node

        allocate(new_node)
        new_node%data = value
        new_node%next => this%top
        this%top => new_node
        this%size = this%size + 1
    end subroutine linked_stack_push

    function linked_stack_pop(this) result(value)
        class(linked_stack), intent(inout) :: this
        integer :: value
        type(stack_node), pointer :: temp

        if (.not. associated(this%top)) then
            print *, 'Error: Stack underflow!'
            value = -999999  ! Error value
            return
        end if

        value = this%top%data
        temp => this%top
        this%top => this%top%next
        deallocate(temp)
        this%size = this%size - 1
    end function linked_stack_pop

    function linked_stack_peek(this) result(value)
        class(linked_stack), intent(in) :: this
        integer :: value

        if (.not. associated(this%top)) then
            print *, 'Error: Stack is empty!'
            value = -999999  ! Error value
            return
        end if

        value = this%top%data
    end function linked_stack_peek

    function linked_stack_is_empty(this) result(empty)
        class(linked_stack), intent(in) :: this
        logical :: empty

        empty = .not. associated(this%top)
    end function linked_stack_is_empty

    function linked_stack_size(this) result(size)
        class(linked_stack), intent(in) :: this
        integer :: size

        size = this%size
    end function linked_stack_size

    subroutine linked_stack_clear(this)
        class(linked_stack), intent(inout) :: this

        call this%destroy()
    end subroutine linked_stack_clear

    subroutine linked_stack_print(this)
        class(linked_stack), intent(in) :: this
        type(stack_node), pointer :: current

        if (.not. associated(this%top)) then
            print *, 'Stack is empty'
            return
        end if

        write(*, '(A)', advance='no') 'Stack (top to bottom): '
        current => this%top
        do while (associated(current))
            write(*, '(I0, 1X)', advance='no') current%data
            current => current%next
        end do
        print *
    end subroutine linked_stack_print

    subroutine linked_stack_destroy(this)
        class(linked_stack), intent(inout) :: this
        type(stack_node), pointer :: current, next_node

        current => this%top
        do while (associated(current))
            next_node => current%next
            deallocate(current)
            current => next_node
        end do

        this%top => null()
        this%size = 0
    end subroutine linked_stack_destroy

end module stack_module

! ============================================================================
! STACK APPLICATIONS MODULE
! ============================================================================

module stack_applications
    use stack_module
    implicit none

contains

    ! Check if brackets are balanced
    function is_balanced(expression) result(balanced)
        character(len=*), intent(in) :: expression
        logical :: balanced
        type(array_stack) :: stack
        integer :: i, len_expr
        character :: ch, top_ch

        len_expr = len_trim(expression)
        balanced = .true.

        do i = 1, len_expr
            ch = expression(i:i)

            if (ch == '(' .or. ch == '[' .or. ch == '{') then
                call stack%push(ichar(ch))
            else if (ch == ')' .or. ch == ']' .or. ch == '}') then
                if (stack%is_empty()) then
                    balanced = .false.
                    return
                end if

                top_ch = char(stack%pop())

                if ((ch == ')' .and. top_ch /= '(') .or. &
                    (ch == ']' .and. top_ch /= '[') .or. &
                    (ch == '}' .and. top_ch /= '{')) then
                    balanced = .false.
                    return
                end if
            end if
        end do

        if (.not. stack%is_empty()) then
            balanced = .false.
        end if
    end function is_balanced

    ! Reverse a string using stack
    function reverse_string(str) result(reversed)
        character(len=*), intent(in) :: str
        character(len=:), allocatable :: reversed
        type(array_stack) :: stack
        integer :: i, len_str

        len_str = len_trim(str)
        allocate(character(len=len_str) :: reversed)

        ! Push all characters
        do i = 1, len_str
            call stack%push(ichar(str(i:i)))
        end do

        ! Pop all characters
        do i = 1, len_str
            reversed(i:i) = char(stack%pop())
        end do
    end function reverse_string

    ! Evaluate postfix expression
    function eval_postfix(expression) result(result_val)
        character(len=*), intent(in) :: expression
        integer :: result_val
        type(array_stack) :: stack
        integer :: i, len_expr, a, b
        character :: ch

        len_expr = len_trim(expression)

        do i = 1, len_expr
            ch = expression(i:i)

            if (ch >= '0' .and. ch <= '9') then
                call stack%push(ichar(ch) - ichar('0'))
            else if (ch == ' ') then
                cycle
            else
                b = stack%pop()
                a = stack%pop()

                select case (ch)
                case ('+')
                    call stack%push(a + b)
                case ('-')
                    call stack%push(a - b)
                case ('*')
                    call stack%push(a * b)
                case ('/')
                    if (b /= 0) then
                        call stack%push(a / b)
                    else
                        print *, 'Error: Division by zero'
                        result_val = 0
                        return
                    end if
                end select
            end if
        end do

        result_val = stack%pop()
    end function eval_postfix

end module stack_applications

! ============================================================================
! DEMONSTRATION PROGRAM
! ============================================================================

program test_stack
    use stack_module
    use stack_applications
    implicit none

    type(array_stack) :: astack
    type(linked_stack) :: lstack
    integer :: i, value
    character(len=100) :: expr
    character(len=:), allocatable :: reversed

    print '(A)', repeat('=', 75)
    print '(A)', '                   STACK - FORTRAN'
    print '(A)', repeat('=', 75)
    print *

    ! Test 1: Array-based stack
    print '(A)', 'Test 1: Array-Based Stack'
    print '(A)', repeat('-', 75)

    print *, 'Pushing: 10, 20, 30, 40, 50'
    call astack%push(10)
    call astack%push(20)
    call astack%push(30)
    call astack%push(40)
    call astack%push(50)

    call astack%print()
    print '(A, I0)', 'Size: ', astack%get_size()
    print '(A, I0)', 'Top element (peek): ', astack%peek()
    print *

    print *, 'Popping 2 elements...'
    value = astack%pop()
    print '(A, I0)', 'Popped: ', value
    value = astack%pop()
    print '(A, I0)', 'Popped: ', value
    call astack%print()
    print *

    ! Test 2: Linked-list-based stack
    print '(A)', 'Test 2: Linked-List-Based Stack'
    print '(A)', repeat('-', 75)

    print *, 'Pushing: 100, 200, 300, 400, 500'
    call lstack%push(100)
    call lstack%push(200)
    call lstack%push(300)
    call lstack%push(400)
    call lstack%push(500)

    call lstack%print()
    print '(A, I0)', 'Size: ', lstack%get_size()
    print '(A, I0)', 'Top element (peek): ', lstack%peek()
    print *

    print *, 'Popping 3 elements...'
    do i = 1, 3
        value = lstack%pop()
        print '(A, I0)', 'Popped: ', value
    end do
    call lstack%print()
    print *

    ! Test 3: Bracket matching
    print '(A)', 'Test 3: Balanced Brackets Check'
    print '(A)', repeat('-', 75)

    expr = '{[()()]}'
    print '(A, A, A, L1)', 'Expression: "', trim(expr), '" - Balanced: ', &
          is_balanced(expr)

    expr = '{[(])}'
    print '(A, A, A, L1)', 'Expression: "', trim(expr), '" - Balanced: ', &
          is_balanced(expr)

    expr = '{{[[(())]]}}'
    print '(A, A, A, L1)', 'Expression: "', trim(expr), '" - Balanced: ', &
          is_balanced(expr)

    expr = '{{[[(()]]]}'
    print '(A, A, A, L1)', 'Expression: "', trim(expr), '" - Balanced: ', &
          is_balanced(expr)
    print *

    ! Test 4: String reversal
    print '(A)', 'Test 4: String Reversal'
    print '(A)', repeat('-', 75)

    expr = 'FORTRAN'
    reversed = reverse_string(expr)
    print '(A, A)', 'Original: ', trim(expr)
    print '(A, A)', 'Reversed: ', trim(reversed)
    print *

    expr = 'Algorithm'
    reversed = reverse_string(expr)
    print '(A, A)', 'Original: ', trim(expr)
    print '(A, A)', 'Reversed: ', trim(reversed)
    print *

    ! Test 5: Postfix expression evaluation
    print '(A)', 'Test 5: Postfix Expression Evaluation'
    print '(A)', repeat('-', 75)

    expr = '53+82-*'  ! (5+3) * (8-2) = 8 * 6 = 48
    print '(A, A)', 'Expression: ', trim(expr)
    print '(A, I0)', 'Result: ', eval_postfix(expr)
    print *

    expr = '23*54*+'  ! (2*3) + (5*4) = 6 + 20 = 26
    print '(A, A)', 'Expression: ', trim(expr)
    print '(A, I0)', 'Result: ', eval_postfix(expr)
    print *

    ! Summary
    print '(A)', repeat('=', 75)
    print '(A)', 'STACK COMPLEXITY SUMMARY'
    print '(A)', repeat('=', 75)
    print '(A)', 'Implementation  Push    Pop     Peek    Space'
    print '(A)', repeat('-', 75)
    print '(A)', 'Array-based     O(1)    O(1)    O(1)    O(n)'
    print '(A)', 'Linked-list     O(1)    O(1)    O(1)    O(n)'
    print '(A)', ''
    print '(A)', 'Applications:'
    print '(A)', '- Expression evaluation (infix to postfix, evaluation)'
    print '(A)', '- Backtracking algorithms (DFS, maze solving)'
    print '(A)', '- Function call management (call stack)'
    print '(A)', '- Undo/Redo operations'
    print '(A)', '- Browser history'
    print '(A)', '- Syntax parsing and bracket matching'
    print '(A)', repeat('=', 75)

    ! Cleanup
    call lstack%destroy()

end program test_stack
