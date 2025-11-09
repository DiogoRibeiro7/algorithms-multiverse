!==============================================================================
! Linked List Implementations in Fortran
!
! Features:
! - Singly and Doubly linked lists
! - Pointer-based implementation
! - Scientific computing focus
! - Modern Fortran (2003/2008)
!
! Compilation:
!   gfortran -o linkedlist linkedlist.f90
!   ./linkedlist
!==============================================================================

module linkedlist_module
    implicit none
    private

    ! Singly Linked List Node
    type, public :: singly_node
        real(8) :: data
        type(singly_node), pointer :: next => null()
    end type singly_node

    ! Doubly Linked List Node
    type, public :: doubly_node
        real(8) :: data
        type(doubly_node), pointer :: next => null()
        type(doubly_node), pointer :: prev => null()
    end type doubly_node

    ! Singly Linked List
    type, public :: singly_list
        private
        type(singly_node), pointer :: head => null()
        integer :: size = 0
    contains
        procedure, public :: insert_at_head => sll_insert_at_head
        procedure, public :: insert_at_tail => sll_insert_at_tail
        procedure, public :: delete_at_head => sll_delete_at_head
        procedure, public :: print => sll_print
        procedure, public :: reverse => sll_reverse
        procedure, public :: get_size => sll_get_size
        procedure, public :: destroy => sll_destroy
    end type singly_list

    ! Doubly Linked List
    type, public :: doubly_list
        private
        type(doubly_node), pointer :: head => null()
        type(doubly_node), pointer :: tail => null()
        integer :: size = 0
    contains
        procedure, public :: insert_at_head => dll_insert_at_head
        procedure, public :: insert_at_tail => dll_insert_at_tail
        procedure, public :: delete_at_head => dll_delete_at_head
        procedure, public :: delete_at_tail => dll_delete_at_tail
        procedure, public :: print => dll_print
        procedure, public :: print_reverse => dll_print_reverse
        procedure, public :: get_size => dll_get_size
        procedure, public :: destroy => dll_destroy
    end type doubly_list

contains

    !--------------------------------------------------------------------------
    ! SINGLY LINKED LIST PROCEDURES
    !--------------------------------------------------------------------------

    subroutine sll_insert_at_head(this, data)
        class(singly_list), intent(inout) :: this
        real(8), intent(in) :: data
        type(singly_node), pointer :: new_node

        allocate(new_node)
        new_node%data = data
        new_node%next => this%head
        this%head => new_node
        this%size = this%size + 1
    end subroutine sll_insert_at_head

    subroutine sll_insert_at_tail(this, data)
        class(singly_list), intent(inout) :: this
        real(8), intent(in) :: data
        type(singly_node), pointer :: new_node, current

        allocate(new_node)
        new_node%data = data
        new_node%next => null()

        if (.not. associated(this%head)) then
            this%head => new_node
        else
            current => this%head
            do while (associated(current%next))
                current => current%next
            end do
            current%next => new_node
        end if

        this%size = this%size + 1
    end subroutine sll_insert_at_tail

    function sll_delete_at_head(this) result(data)
        class(singly_list), intent(inout) :: this
        real(8) :: data
        type(singly_node), pointer :: temp

        data = 0.0d0

        if (.not. associated(this%head)) return

        temp => this%head
        data = temp%data
        this%head => this%head%next
        deallocate(temp)
        this%size = this%size - 1
    end function sll_delete_at_head

    subroutine sll_reverse(this)
        class(singly_list), intent(inout) :: this
        type(singly_node), pointer :: prev, current, next_node

        prev => null()
        current => this%head

        do while (associated(current))
            next_node => current%next
            current%next => prev
            prev => current
            current => next_node
        end do

        this%head => prev
    end subroutine sll_reverse

    subroutine sll_print(this)
        class(singly_list), intent(in) :: this
        type(singly_node), pointer :: current

        current => this%head

        do while (associated(current))
            write(*, '(F8.2)', advance='no') current%data
            if (associated(current%next)) then
                write(*, '(A)', advance='no') ' -> '
            end if
            current => current%next
        end do

        write(*, '(A)') ' -> NULL'
    end subroutine sll_print

    function sll_get_size(this) result(size)
        class(singly_list), intent(in) :: this
        integer :: size

        size = this%size
    end function sll_get_size

    subroutine sll_destroy(this)
        class(singly_list), intent(inout) :: this
        type(singly_node), pointer :: current, next_node

        current => this%head

        do while (associated(current))
            next_node => current%next
            deallocate(current)
            current => next_node
        end do

        this%head => null()
        this%size = 0
    end subroutine sll_destroy

    !--------------------------------------------------------------------------
    ! DOUBLY LINKED LIST PROCEDURES
    !--------------------------------------------------------------------------

    subroutine dll_insert_at_head(this, data)
        class(doubly_list), intent(inout) :: this
        real(8), intent(in) :: data
        type(doubly_node), pointer :: new_node

        allocate(new_node)
        new_node%data = data
        new_node%prev => null()

        if (.not. associated(this%head)) then
            new_node%next => null()
            this%head => new_node
            this%tail => new_node
        else
            new_node%next => this%head
            this%head%prev => new_node
            this%head => new_node
        end if

        this%size = this%size + 1
    end subroutine dll_insert_at_head

    subroutine dll_insert_at_tail(this, data)
        class(doubly_list), intent(inout) :: this
        real(8), intent(in) :: data
        type(doubly_node), pointer :: new_node

        allocate(new_node)
        new_node%data = data
        new_node%next => null()

        if (.not. associated(this%tail)) then
            new_node%prev => null()
            this%head => new_node
            this%tail => new_node
        else
            new_node%prev => this%tail
            this%tail%next => new_node
            this%tail => new_node
        end if

        this%size = this%size + 1
    end subroutine dll_insert_at_tail

    function dll_delete_at_head(this) result(data)
        class(doubly_list), intent(inout) :: this
        real(8) :: data
        type(doubly_node), pointer :: temp

        data = 0.0d0

        if (.not. associated(this%head)) return

        temp => this%head
        data = temp%data

        if (associated(this%head, this%tail)) then
            this%head => null()
            this%tail => null()
        else
            this%head => this%head%next
            this%head%prev => null()
        end if

        deallocate(temp)
        this%size = this%size - 1
    end function dll_delete_at_head

    function dll_delete_at_tail(this) result(data)
        class(doubly_list), intent(inout) :: this
        real(8) :: data
        type(doubly_node), pointer :: temp

        data = 0.0d0

        if (.not. associated(this%tail)) return

        temp => this%tail
        data = temp%data

        if (associated(this%head, this%tail)) then
            this%head => null()
            this%tail => null()
        else
            this%tail => this%tail%prev
            this%tail%next => null()
        end if

        deallocate(temp)
        this%size = this%size - 1
    end function dll_delete_at_tail

    subroutine dll_print(this)
        class(doubly_list), intent(in) :: this
        type(doubly_node), pointer :: current

        current => this%head

        do while (associated(current))
            write(*, '(F8.2)', advance='no') current%data
            if (associated(current%next)) then
                write(*, '(A)', advance='no') ' <-> '
            end if
            current => current%next
        end do

        write(*, '(A)') ' <-> NULL'
    end subroutine dll_print

    subroutine dll_print_reverse(this)
        class(doubly_list), intent(in) :: this
        type(doubly_node), pointer :: current

        current => this%tail

        do while (associated(current))
            write(*, '(F8.2)', advance='no') current%data
            if (associated(current%prev)) then
                write(*, '(A)', advance='no') ' <-> '
            end if
            current => current%prev
        end do

        write(*, '(A)') ' <-> NULL'
    end subroutine dll_print_reverse

    function dll_get_size(this) result(size)
        class(doubly_list), intent(in) :: this
        integer :: size

        size = this%size
    end function dll_get_size

    subroutine dll_destroy(this)
        class(doubly_list), intent(inout) :: this
        type(doubly_node), pointer :: current, next_node

        current => this%head

        do while (associated(current))
            next_node => current%next
            deallocate(current)
            current => next_node
        end do

        this%head => null()
        this%tail => null()
        this%size = 0
    end subroutine dll_destroy

end module linkedlist_module

!==============================================================================
! DEMONSTRATION PROGRAM
!==============================================================================

program linkedlist_demo
    use linkedlist_module
    implicit none

    type(singly_list) :: sll
    type(doubly_list) :: dll
    real(8) :: deleted_value
    integer :: i

    print *, repeat('=', 80)
    print *, 'LINKED LIST IMPLEMENTATIONS IN FORTRAN'
    print *, repeat('=', 80)

    ! Singly Linked List
    print *
    print *, '1. SINGLY LINKED LIST'
    print *, repeat('-', 80)

    print *, 'Inserting: 1.0, 2.0, 3.0 at head'
    call sll%insert_at_head(3.0d0)
    call sll%insert_at_head(2.0d0)
    call sll%insert_at_head(1.0d0)
    write(*, '(A)', advance='no') 'List: '
    call sll%print()

    print *
    print *, 'Inserting: 4.0, 5.0 at tail'
    call sll%insert_at_tail(4.0d0)
    call sll%insert_at_tail(5.0d0)
    write(*, '(A)', advance='no') 'List: '
    call sll%print()

    print *
    print *, 'Reversing list...'
    call sll%reverse()
    write(*, '(A)', advance='no') 'List: '
    call sll%print()

    print *
    deleted_value = sll%delete_at_head()
    write(*, '(A,F8.2)') 'Deleted head:', deleted_value
    write(*, '(A,I0)') 'Size: ', sll%get_size()

    ! Doubly Linked List
    print *
    print *, '2. DOUBLY LINKED LIST'
    print *, repeat('-', 80)

    print *, 'Inserting: 10.0, 20.0, 30.0 at head'
    call dll%insert_at_head(30.0d0)
    call dll%insert_at_head(20.0d0)
    call dll%insert_at_head(10.0d0)
    write(*, '(A)', advance='no') 'List: '
    call dll%print()

    print *
    print *, 'Inserting: 40.0, 50.0 at tail'
    call dll%insert_at_tail(40.0d0)
    call dll%insert_at_tail(50.0d0)
    write(*, '(A)', advance='no') 'List: '
    call dll%print()

    print *
    write(*, '(A)', advance='no') 'Forward iteration: '
    call dll%print()

    write(*, '(A)', advance='no') 'Backward iteration: '
    call dll%print_reverse()

    ! Cleanup
    call sll%destroy()
    call dll%destroy()

    print *
    print *, repeat('=', 80)
    print *, '✨ All demonstrations complete!'
    print *, repeat('=', 80)

end program linkedlist_demo
