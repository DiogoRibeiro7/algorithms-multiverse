! Binary Search Tree (BST) Implementation in Modern Fortran
!
! Features:
! - Complete BST operations (insert, search, delete)
! - Tree traversals (inorder, preorder, postorder, level-order)
! - Min/Max/Height/Size operations
! - Parent pointer tracking
! - Balance factor checking
! - Pretty-print visualization
!
! Compilation:
!   gfortran -O2 -o bst bst.f90
!   ./bst
!
! Author: Algorithms Multiverse

module bst_module
    implicit none
    private

    ! BST Node Type
    type, public :: bst_node
        integer :: key
        real(8) :: value
        type(bst_node), pointer :: left => null()
        type(bst_node), pointer :: right => null()
        type(bst_node), pointer :: parent => null()
    end type bst_node

    ! Binary Search Tree Type
    type, public :: binary_search_tree
        private
        type(bst_node), pointer :: root => null()
        integer :: node_count = 0
    contains
        procedure, public :: insert => bst_insert
        procedure, public :: search => bst_search
        procedure, public :: delete => bst_delete
        procedure, public :: find_min => bst_find_min
        procedure, public :: find_max => bst_find_max
        procedure, public :: get_height => bst_height
        procedure, public :: get_size => bst_size
        procedure, public :: inorder_traversal => bst_inorder
        procedure, public :: preorder_traversal => bst_preorder
        procedure, public :: postorder_traversal => bst_postorder
        procedure, public :: level_order => bst_level_order
        procedure, public :: is_balanced => bst_is_balanced
        procedure, public :: print_tree => bst_print_tree
        procedure, public :: destroy => bst_destroy
    end type binary_search_tree

contains

    ! ========================================================================
    ! INSERTION
    ! ========================================================================

    subroutine bst_insert(this, key, value)
        class(binary_search_tree), intent(inout) :: this
        integer, intent(in) :: key
        real(8), intent(in) :: value

        if (.not. associated(this%root)) then
            allocate(this%root)
            this%root%key = key
            this%root%value = value
            this%root%left => null()
            this%root%right => null()
            this%root%parent => null()
            this%node_count = 1
        else
            call insert_recursive(this%root, key, value, this%node_count)
        end if
    end subroutine bst_insert

    recursive subroutine insert_recursive(node, key, value, count)
        type(bst_node), pointer, intent(inout) :: node
        integer, intent(in) :: key
        real(8), intent(in) :: value
        integer, intent(inout) :: count

        if (key < node%key) then
            if (.not. associated(node%left)) then
                allocate(node%left)
                node%left%key = key
                node%left%value = value
                node%left%left => null()
                node%left%right => null()
                node%left%parent => node
                count = count + 1
            else
                call insert_recursive(node%left, key, value, count)
            end if
        else if (key > node%key) then
            if (.not. associated(node%right)) then
                allocate(node%right)
                node%right%key = key
                node%right%value = value
                node%right%left => null()
                node%right%right => null()
                node%right%parent => node
                count = count + 1
            else
                call insert_recursive(node%right, key, value, count)
            end if
        else
            ! Key already exists, update value
            node%value = value
        end if
    end subroutine insert_recursive

    ! ========================================================================
    ! SEARCH
    ! ========================================================================

    function bst_search(this, key) result(found)
        class(binary_search_tree), intent(in) :: this
        integer, intent(in) :: key
        logical :: found
        type(bst_node), pointer :: result

        result => search_recursive(this%root, key)
        found = associated(result)
    end function bst_search

    recursive function search_recursive(node, key) result(result_node)
        type(bst_node), pointer, intent(in) :: node
        integer, intent(in) :: key
        type(bst_node), pointer :: result_node

        if (.not. associated(node)) then
            result_node => null()
        else if (key == node%key) then
            result_node => node
        else if (key < node%key) then
            result_node => search_recursive(node%left, key)
        else
            result_node => search_recursive(node%right, key)
        end if
    end function search_recursive

    ! ========================================================================
    ! DELETION
    ! ========================================================================

    subroutine bst_delete(this, key)
        class(binary_search_tree), intent(inout) :: this
        integer, intent(in) :: key

        this%root => delete_recursive(this%root, key, this%node_count)
    end subroutine bst_delete

    recursive function delete_recursive(node, key, count) result(new_node)
        type(bst_node), pointer, intent(inout) :: node
        integer, intent(in) :: key
        integer, intent(inout) :: count
        type(bst_node), pointer :: new_node, temp, min_node

        if (.not. associated(node)) then
            new_node => null()
            return
        end if

        if (key < node%key) then
            node%left => delete_recursive(node%left, key, count)
            new_node => node
        else if (key > node%key) then
            node%right => delete_recursive(node%right, key, count)
            new_node => node
        else
            ! Node found - delete it
            if (.not. associated(node%left)) then
                temp => node%right
                deallocate(node)
                new_node => temp
                count = count - 1
            else if (.not. associated(node%right)) then
                temp => node%left
                deallocate(node)
                new_node => temp
                count = count - 1
            else
                ! Node has two children - find inorder successor
                min_node => find_min_node(node%right)
                node%key = min_node%key
                node%value = min_node%value
                node%right => delete_recursive(node%right, min_node%key, count)
                new_node => node
                count = count + 1  ! Compensate for the extra decrement
            end if
        end if
    end function delete_recursive

    ! ========================================================================
    ! MIN/MAX OPERATIONS
    ! ========================================================================

    function bst_find_min(this) result(min_key)
        class(binary_search_tree), intent(in) :: this
        integer :: min_key
        type(bst_node), pointer :: min_node

        if (.not. associated(this%root)) then
            min_key = -999999  ! Error value
        else
            min_node => find_min_node(this%root)
            min_key = min_node%key
        end if
    end function bst_find_min

    recursive function find_min_node(node) result(min_node)
        type(bst_node), pointer, intent(in) :: node
        type(bst_node), pointer :: min_node

        if (.not. associated(node%left)) then
            min_node => node
        else
            min_node => find_min_node(node%left)
        end if
    end function find_min_node

    function bst_find_max(this) result(max_key)
        class(binary_search_tree), intent(in) :: this
        integer :: max_key
        type(bst_node), pointer :: max_node

        if (.not. associated(this%root)) then
            max_key = -999999  ! Error value
        else
            max_node => find_max_node(this%root)
            max_key = max_node%key
        end if
    end function bst_find_max

    recursive function find_max_node(node) result(max_node)
        type(bst_node), pointer, intent(in) :: node
        type(bst_node), pointer :: max_node

        if (.not. associated(node%right)) then
            max_node => node
        else
            max_node => find_max_node(node%right)
        end if
    end function find_max_node

    ! ========================================================================
    ! TREE PROPERTIES
    ! ========================================================================

    function bst_height(this) result(height)
        class(binary_search_tree), intent(in) :: this
        integer :: height

        height = height_recursive(this%root)
    end function bst_height

    recursive function height_recursive(node) result(h)
        type(bst_node), pointer, intent(in) :: node
        integer :: h, left_h, right_h

        if (.not. associated(node)) then
            h = -1
        else
            left_h = height_recursive(node%left)
            right_h = height_recursive(node%right)
            h = 1 + max(left_h, right_h)
        end if
    end function height_recursive

    function bst_size(this) result(size)
        class(binary_search_tree), intent(in) :: this
        integer :: size

        size = this%node_count
    end function bst_size

    function bst_is_balanced(this) result(balanced)
        class(binary_search_tree), intent(in) :: this
        logical :: balanced

        balanced = is_balanced_recursive(this%root)
    end function bst_is_balanced

    recursive function is_balanced_recursive(node) result(balanced)
        type(bst_node), pointer, intent(in) :: node
        logical :: balanced
        integer :: left_h, right_h

        if (.not. associated(node)) then
            balanced = .true.
        else
            left_h = height_recursive(node%left)
            right_h = height_recursive(node%right)

            if (abs(left_h - right_h) <= 1 .and. &
                is_balanced_recursive(node%left) .and. &
                is_balanced_recursive(node%right)) then
                balanced = .true.
            else
                balanced = .false.
            end if
        end if
    end function is_balanced_recursive

    ! ========================================================================
    ! TREE TRAVERSALS
    ! ========================================================================

    subroutine bst_inorder(this)
        class(binary_search_tree), intent(in) :: this

        write(*, '(A)', advance='no') 'Inorder: '
        call inorder_recursive(this%root)
        print *
    end subroutine bst_inorder

    recursive subroutine inorder_recursive(node)
        type(bst_node), pointer, intent(in) :: node

        if (associated(node)) then
            call inorder_recursive(node%left)
            write(*, '(I0, 1X)', advance='no') node%key
            call inorder_recursive(node%right)
        end if
    end subroutine inorder_recursive

    subroutine bst_preorder(this)
        class(binary_search_tree), intent(in) :: this

        write(*, '(A)', advance='no') 'Preorder: '
        call preorder_recursive(this%root)
        print *
    end subroutine bst_preorder

    recursive subroutine preorder_recursive(node)
        type(bst_node), pointer, intent(in) :: node

        if (associated(node)) then
            write(*, '(I0, 1X)', advance='no') node%key
            call preorder_recursive(node%left)
            call preorder_recursive(node%right)
        end if
    end subroutine preorder_recursive

    subroutine bst_postorder(this)
        class(binary_search_tree), intent(in) :: this

        write(*, '(A)', advance='no') 'Postorder: '
        call postorder_recursive(this%root)
        print *
    end subroutine bst_postorder

    recursive subroutine postorder_recursive(node)
        type(bst_node), pointer, intent(in) :: node

        if (associated(node)) then
            call postorder_recursive(node%left)
            call postorder_recursive(node%right)
            write(*, '(I0, 1X)', advance='no') node%key
        end if
    end subroutine postorder_recursive

    subroutine bst_level_order(this)
        class(binary_search_tree), intent(in) :: this
        integer :: current_level, max_level

        if (.not. associated(this%root)) return

        write(*, '(A)', advance='no') 'Level-order: '
        max_level = height_recursive(this%root)

        do current_level = 0, max_level
            call print_level(this%root, current_level)
        end do

        print *
    end subroutine bst_level_order

    recursive subroutine print_level(node, level)
        type(bst_node), pointer, intent(in) :: node
        integer, intent(in) :: level

        if (.not. associated(node)) return

        if (level == 0) then
            write(*, '(I0, 1X)', advance='no') node%key
        else
            call print_level(node%left, level - 1)
            call print_level(node%right, level - 1)
        end if
    end subroutine print_level

    ! ========================================================================
    ! TREE VISUALIZATION
    ! ========================================================================

    subroutine bst_print_tree(this)
        class(binary_search_tree), intent(in) :: this

        if (.not. associated(this%root)) then
            print *, 'Tree is empty'
        else
            print *, 'Tree structure:'
            call print_tree_recursive(this%root, 0)
        end if
    end subroutine bst_print_tree

    recursive subroutine print_tree_recursive(node, depth)
        type(bst_node), pointer, intent(in) :: node
        integer, intent(in) :: depth
        integer :: i

        if (associated(node)) then
            call print_tree_recursive(node%right, depth + 1)

            do i = 1, depth
                write(*, '(A)', advance='no') '    '
            end do
            print '(A, I0)', '└── ', node%key

            call print_tree_recursive(node%left, depth + 1)
        end if
    end subroutine print_tree_recursive

    ! ========================================================================
    ! CLEANUP
    ! ========================================================================

    subroutine bst_destroy(this)
        class(binary_search_tree), intent(inout) :: this

        call destroy_recursive(this%root)
        this%root => null()
        this%node_count = 0
    end subroutine bst_destroy

    recursive subroutine destroy_recursive(node)
        type(bst_node), pointer, intent(inout) :: node

        if (associated(node)) then
            call destroy_recursive(node%left)
            call destroy_recursive(node%right)
            deallocate(node)
        end if
    end subroutine destroy_recursive

end module bst_module

! ============================================================================
! DEMONSTRATION PROGRAM
! ============================================================================

program test_bst
    use bst_module
    implicit none

    type(binary_search_tree) :: tree
    integer :: i

    print '(A)', repeat('=', 75)
    print '(A)', '              BINARY SEARCH TREE - FORTRAN'
    print '(A)', repeat('=', 75)
    print *

    ! Test 1: Basic operations
    print '(A)', 'Test 1: Basic Insert and Traversals'
    print '(A)', repeat('-', 75)

    ! Insert values: 50, 30, 70, 20, 40, 60, 80
    call tree%insert(50, 50.0d0)
    call tree%insert(30, 30.0d0)
    call tree%insert(70, 70.0d0)
    call tree%insert(20, 20.0d0)
    call tree%insert(40, 40.0d0)
    call tree%insert(60, 60.0d0)
    call tree%insert(80, 80.0d0)

    print '(A, I0)', 'Inserted 7 nodes. Tree size: ', tree%get_size()
    print *

    call tree%inorder_traversal()
    call tree%preorder_traversal()
    call tree%postorder_traversal()
    call tree%level_order()
    print *

    ! Test 2: Tree properties
    print '(A)', 'Test 2: Tree Properties'
    print '(A)', repeat('-', 75)
    print '(A, I0)', 'Tree height: ', tree%get_height()
    print '(A, I0)', 'Minimum key: ', tree%find_min()
    print '(A, I0)', 'Maximum key: ', tree%find_max()
    print '(A, L1)', 'Is balanced: ', tree%is_balanced()
    print *

    ! Test 3: Search operations
    print '(A)', 'Test 3: Search Operations'
    print '(A)', repeat('-', 75)
    print '(A, I0, A, L1)', 'Search for 40: ', 40, ' - Found: ', tree%search(40)
    print '(A, I0, A, L1)', 'Search for 25: ', 25, ' - Found: ', tree%search(25)
    print '(A, I0, A, L1)', 'Search for 80: ', 80, ' - Found: ', tree%search(80)
    print *

    ! Test 4: Tree visualization
    print '(A)', 'Test 4: Tree Visualization'
    print '(A)', repeat('-', 75)
    call tree%print_tree()
    print *

    ! Test 5: Deletion
    print '(A)', 'Test 5: Delete Operations'
    print '(A)', repeat('-', 75)
    print '(A)', 'Deleting node with key 20 (leaf node)...'
    call tree%delete(20)
    call tree%inorder_traversal()
    print *

    print '(A)', 'Deleting node with key 30 (one child)...'
    call tree%delete(30)
    call tree%inorder_traversal()
    print *

    print '(A)', 'Deleting node with key 50 (two children - root)...'
    call tree%delete(50)
    call tree%inorder_traversal()
    print '(A, I0)', 'Tree size after deletions: ', tree%get_size()
    print *

    call tree%print_tree()
    print *

    ! Test 6: Building unbalanced tree
    call tree%destroy()

    print '(A)', 'Test 6: Unbalanced Tree (Sequential Insertion)'
    print '(A)', repeat('-', 75)
    print '(A)', 'Inserting 1, 2, 3, 4, 5, 6, 7 in order...'
    do i = 1, 7
        call tree%insert(i, real(i, 8))
    end do

    call tree%inorder_traversal()
    print '(A, I0)', 'Height: ', tree%get_height()
    print '(A, L1)', 'Is balanced: ', tree%is_balanced()
    print *

    call tree%print_tree()
    print *

    ! Summary
    print '(A)', repeat('=', 75)
    print '(A)', 'BST COMPLEXITY SUMMARY'
    print '(A)', repeat('=', 75)
    print '(A)', 'Operation       Average Case    Worst Case     Space'
    print '(A)', repeat('-', 75)
    print '(A)', 'Search          O(log n)        O(n)           O(1)'
    print '(A)', 'Insert          O(log n)        O(n)           O(1)'
    print '(A)', 'Delete          O(log n)        O(n)           O(1)'
    print '(A)', 'Min/Max         O(log n)        O(n)           O(1)'
    print '(A)', 'Traversal       O(n)            O(n)           O(h)'
    print '(A)', ''
    print '(A)', 'where n = number of nodes, h = tree height'
    print '(A)', ''
    print '(A)', 'Note: Worst case occurs with unbalanced trees'
    print '(A)', '      Use AVL or Red-Black trees for guaranteed O(log n)'
    print '(A)', repeat('=', 75)

    ! Cleanup
    call tree%destroy()

end program test_bst
