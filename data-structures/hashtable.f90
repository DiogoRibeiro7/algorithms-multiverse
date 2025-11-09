!==============================================================================
! Comprehensive Hash Table Implementation in Fortran
!
! Features:
! - Separate chaining for collision resolution
! - String keys and integer values (simplified for Fortran)
! - Dynamic resizing with configurable load factor
! - Performance statistics
! - Modern Fortran 2003/2008 features
!
! Time Complexity:
! - Average: O(1) for insert, delete, search
! - Worst:   O(n) for chaining with poor hash function
!
! Space Complexity: O(n) where n is the number of elements
!
! Compilation and Usage:
!   gfortran -o hashtable hashtable.f90
!   ./hashtable
!
! Or with Intel Fortran:
!   ifort -o hashtable hashtable.f90
!   ./hashtable
!==============================================================================

module hash_table_module
    implicit none
    private

    ! Maximum string length for keys
    integer, parameter :: MAX_KEY_LEN = 64
    integer, parameter :: INITIAL_CAPACITY = 16
    real(8), parameter :: LOAD_FACTOR = 0.75

    ! Node type for linked list (chain)
    type :: hash_node
        character(len=MAX_KEY_LEN) :: key
        integer :: value
        type(hash_node), pointer :: next => null()
    end type hash_node

    ! Hash table type
    type, public :: hash_table
        private
        type(hash_node), dimension(:), pointer :: buckets => null()
        integer :: capacity = INITIAL_CAPACITY
        integer :: size = 0
        real(8) :: load_factor = LOAD_FACTOR

        ! Statistics
        integer :: collisions = 0
        integer :: resizes = 0

    contains
        procedure, public :: init => ht_init
        procedure, public :: destroy => ht_destroy
        procedure, public :: put => ht_put
        procedure, public :: get => ht_get
        procedure, public :: remove => ht_remove
        procedure, public :: contains => ht_contains
        procedure, public :: get_size => ht_get_size
        procedure, public :: clear => ht_clear
        procedure, public :: print_stats => ht_print_stats
        procedure, private :: hash_index => ht_hash_index
        procedure, private :: should_resize => ht_should_resize
        procedure, private :: resize => ht_resize
    end type hash_table

contains

    !--------------------------------------------------------------------------
    ! Initialize hash table
    !--------------------------------------------------------------------------
    subroutine ht_init(this, initial_capacity)
        class(hash_table), intent(inout) :: this
        integer, intent(in), optional :: initial_capacity
        integer :: i, cap

        if (present(initial_capacity)) then
            cap = next_power_of_2(initial_capacity)
        else
            cap = INITIAL_CAPACITY
        end if

        this%capacity = cap
        this%size = 0
        this%collisions = 0
        this%resizes = 0

        allocate(this%buckets(0:this%capacity-1))

        ! Initialize all bucket pointers to null
        do i = 0, this%capacity - 1
            this%buckets(i)%next => null()
        end do

    end subroutine ht_init

    !--------------------------------------------------------------------------
    ! Destroy hash table and free memory
    !--------------------------------------------------------------------------
    subroutine ht_destroy(this)
        class(hash_table), intent(inout) :: this
        integer :: i
        type(hash_node), pointer :: node, next_node

        do i = 0, this%capacity - 1
            node => this%buckets(i)%next
            do while (associated(node))
                next_node => node%next
                deallocate(node)
                node => next_node
            end do
        end do

        if (associated(this%buckets)) then
            deallocate(this%buckets)
        end if

        this%size = 0

    end subroutine ht_destroy

    !--------------------------------------------------------------------------
    ! Compute hash index for key (FNV-1a hash function)
    !--------------------------------------------------------------------------
    function ht_hash_index(this, key) result(index)
        class(hash_table), intent(in) :: this
        character(len=*), intent(in) :: key
        integer :: index
        integer :: i, hash_val
        integer, parameter :: FNV_PRIME = 16777619
        integer, parameter :: FNV_OFFSET = -2128831035

        hash_val = FNV_OFFSET

        do i = 1, len_trim(key)
            hash_val = ieor(hash_val, ichar(key(i:i)))
            hash_val = hash_val * FNV_PRIME
        end do

        ! Ensure positive value and map to bucket range
        index = iand(abs(hash_val), this%capacity - 1)

    end function ht_hash_index

    !--------------------------------------------------------------------------
    ! Check if table should be resized
    !--------------------------------------------------------------------------
    function ht_should_resize(this) result(should)
        class(hash_table), intent(in) :: this
        logical :: should

        should = real(this%size, 8) / real(this%capacity, 8) > this%load_factor

    end function ht_should_resize

    !--------------------------------------------------------------------------
    ! Resize and rehash all elements
    !--------------------------------------------------------------------------
    subroutine ht_resize(this)
        class(hash_table), intent(inout) :: this
        type(hash_node), dimension(:), pointer :: old_buckets
        integer :: old_capacity, i
        type(hash_node), pointer :: node, next_node
        character(len=MAX_KEY_LEN) :: temp_key
        integer :: temp_value

        this%resizes = this%resizes + 1
        old_buckets => this%buckets
        old_capacity = this%capacity

        ! Double capacity
        this%capacity = this%capacity * 2

        ! Allocate new buckets
        allocate(this%buckets(0:this%capacity-1))

        do i = 0, this%capacity - 1
            this%buckets(i)%next => null()
        end do

        this%size = 0
        this%collisions = 0

        ! Rehash all entries
        do i = 0, old_capacity - 1
            node => old_buckets(i)%next
            do while (associated(node))
                next_node => node%next
                temp_key = node%key
                temp_value = node%value
                call this%put(temp_key, temp_value)
                deallocate(node)
                node => next_node
            end do
        end do

        deallocate(old_buckets)

    end subroutine ht_resize

    !--------------------------------------------------------------------------
    ! Insert or update a key-value pair
    !--------------------------------------------------------------------------
    subroutine ht_put(this, key, value)
        class(hash_table), intent(inout) :: this
        character(len=*), intent(in) :: key
        integer, intent(in) :: value
        integer :: index
        type(hash_node), pointer :: node, new_node

        if (this%should_resize()) then
            call this%resize()
        end if

        index = this%hash_index(key)
        node => this%buckets(index)%next

        ! Search for existing key
        do while (associated(node))
            if (trim(node%key) == trim(key)) then
                ! Key found, update value
                node%value = value
                return
            end if
            node => node%next
        end do

        ! Key not found, insert at head
        if (associated(this%buckets(index)%next)) then
            this%collisions = this%collisions + 1
        end if

        allocate(new_node)
        new_node%key = key
        new_node%value = value
        new_node%next => this%buckets(index)%next
        this%buckets(index)%next => new_node
        this%size = this%size + 1

    end subroutine ht_put

    !--------------------------------------------------------------------------
    ! Get value for key
    !--------------------------------------------------------------------------
    function ht_get(this, key, found) result(value)
        class(hash_table), intent(in) :: this
        character(len=*), intent(in) :: key
        logical, intent(out) :: found
        integer :: value
        integer :: index
        type(hash_node), pointer :: node

        found = .false.
        value = 0
        index = this%hash_index(key)
        node => this%buckets(index)%next

        do while (associated(node))
            if (trim(node%key) == trim(key)) then
                value = node%value
                found = .true.
                return
            end if
            node => node%next
        end do

    end function ht_get

    !--------------------------------------------------------------------------
    ! Remove key and return success
    !--------------------------------------------------------------------------
    function ht_remove(this, key) result(removed)
        class(hash_table), intent(inout) :: this
        character(len=*), intent(in) :: key
        logical :: removed
        integer :: index
        type(hash_node), pointer :: node, prev

        removed = .false.
        index = this%hash_index(key)
        node => this%buckets(index)%next
        prev => this%buckets(index)

        do while (associated(node))
            if (trim(node%key) == trim(key)) then
                ! Found key, remove node
                prev%next => node%next
                deallocate(node)
                this%size = this%size - 1
                removed = .true.
                return
            end if
            prev => node
            node => node%next
        end do

    end function ht_remove

    !--------------------------------------------------------------------------
    ! Check if key exists
    !--------------------------------------------------------------------------
    function ht_contains(this, key) result(exists)
        class(hash_table), intent(in) :: this
        character(len=*), intent(in) :: key
        logical :: exists, found
        integer :: dummy

        dummy = this%get(key, found)
        exists = found

    end function ht_contains

    !--------------------------------------------------------------------------
    ! Get number of elements
    !--------------------------------------------------------------------------
    function ht_get_size(this) result(size)
        class(hash_table), intent(in) :: this
        integer :: size

        size = this%size

    end function ht_get_size

    !--------------------------------------------------------------------------
    ! Clear all elements
    !--------------------------------------------------------------------------
    subroutine ht_clear(this)
        class(hash_table), intent(inout) :: this
        integer :: i
        type(hash_node), pointer :: node, next_node

        do i = 0, this%capacity - 1
            node => this%buckets(i)%next
            do while (associated(node))
                next_node => node%next
                deallocate(node)
                node => next_node
            end do
            this%buckets(i)%next => null()
        end do

        this%size = 0
        this%collisions = 0

    end subroutine ht_clear

    !--------------------------------------------------------------------------
    ! Print statistics
    !--------------------------------------------------------------------------
    subroutine ht_print_stats(this)
        class(hash_table), intent(in) :: this
        integer :: i, chain_length, max_chain, total_chain_length, num_chains
        real(8) :: avg_chain_length
        type(hash_node), pointer :: node

        max_chain = 0
        total_chain_length = 0
        num_chains = 0

        do i = 0, this%capacity - 1
            chain_length = 0
            node => this%buckets(i)%next

            do while (associated(node))
                chain_length = chain_length + 1
                node => node%next
            end do

            if (chain_length > 0) then
                num_chains = num_chains + 1
                total_chain_length = total_chain_length + chain_length
                max_chain = max(max_chain, chain_length)
            end if
        end do

        if (num_chains > 0) then
            avg_chain_length = real(total_chain_length, 8) / real(num_chains, 8)
        else
            avg_chain_length = 0.0
        end if

        print *, 'Hash Table Statistics:'
        print '(A,I0)', '  Size:              ', this%size
        print '(A,I0)', '  Capacity:          ', this%capacity
        print '(A,F0.2,A,F0.2)', '  Load Factor:       ', &
            real(this%size, 8) / real(this%capacity, 8), ' / ', this%load_factor
        print '(A,I0)', '  Collisions:        ', this%collisions
        print '(A,I0)', '  Resizes:           ', this%resizes
        print '(A,I0)', '  Max Chain Length:  ', max_chain
        print '(A,F0.2)', '  Avg Chain Length:  ', avg_chain_length
        print '(A,I0)', '  Number of Chains:  ', num_chains

    end subroutine ht_print_stats

    !--------------------------------------------------------------------------
    ! Get next power of 2 >= n
    !--------------------------------------------------------------------------
    function next_power_of_2(n) result(power)
        integer, intent(in) :: n
        integer :: power

        if (n <= 1) then
            power = 1
            return
        end if

        power = 1
        do while (power < n)
            power = power * 2
        end do

    end function next_power_of_2

end module hash_table_module

!==============================================================================
! DEMONSTRATION PROGRAM
!==============================================================================

program hashtable_demo
    use hash_table_module
    implicit none

    type(hash_table) :: ht
    character(len=64) :: key
    integer :: value, i
    logical :: found, removed

    print *, '==========================================='
    print *, 'Hash Table Implementation in Fortran'
    print *, '==========================================='
    print *

    ! Create hash table
    call ht%init(INITIAL_CAPACITY)

    print *, '1. Inserting elements...'
    print *, '-----------------------------------------'

    ! Insert some data
    do i = 0, 9
        write(key, '(A,I0)') 'key', i
        value = i * 10
        call ht%put(key, value)
        print '(A,A,A,I0)', '  Inserted: ', trim(key), ' -> ', value
    end do

    print *
    print '(A,I0)', 'Size: ', ht%get_size()
    print *

    print *, '2. Retrieving elements...'
    print *, '-----------------------------------------'

    ! Test retrieval
    key = 'key0'
    value = ht%get(key, found)
    if (found) then
        print '(A,A,A,I0)', "  Get '", trim(key), "': ", value
    else
        print '(A,A,A)', "  Get '", trim(key), "': Not found"
    end if

    key = 'key5'
    value = ht%get(key, found)
    if (found) then
        print '(A,A,A,I0)', "  Get '", trim(key), "': ", value
    else
        print '(A,A,A)', "  Get '", trim(key), "': Not found"
    end if

    key = 'nonexistent'
    value = ht%get(key, found)
    if (found) then
        print '(A,A,A,I0)', "  Get '", trim(key), "': ", value
    else
        print '(A,A,A)', "  Get '", trim(key), "': Not found"
    end if

    print *
    print *, '3. Testing containment...'
    print *, '-----------------------------------------'
    print '(A,L1)', "  Contains 'key3': ", ht%contains('key3')
    print '(A,L1)', "  Contains 'missing': ", ht%contains('missing')

    print *
    print *, '4. Updating values...'
    print *, '-----------------------------------------'

    call ht%put('key5', 999)
    value = ht%get('key5', found)
    print '(A,I0)', "  Updated 'key5' to: ", value

    print *
    print *, '5. Removing elements...'
    print *, '-----------------------------------------'

    removed = ht%remove('key7')
    if (removed) then
        print *, "  Removed 'key7': Success"
    else
        print *, "  Removed 'key7': Not found"
    end if
    print '(A,I0)', '  Size after removal: ', ht%get_size()

    print *
    print *, '6. Performance Statistics'
    print *, '-----------------------------------------'
    call ht%print_stats()

    print *
    print *, '7. Testing with many elements...'
    print *, '-----------------------------------------'

    ! Insert many elements to trigger resizing
    do i = 100, 199
        write(key, '(A,I0)') 'item', i
        call ht%put(key, i)
    end do

    print *, '  Added 100 more elements'
    print '(A,I0)', '  New size: ', ht%get_size()
    print *
    call ht%print_stats()

    print *
    print *, '8. Clearing hash table...'
    print *, '-----------------------------------------'
    call ht%clear()
    print '(A,I0)', '  Size after clear: ', ht%get_size()

    ! Cleanup
    call ht%destroy()

    print *
    print *, '==========================================='
    print *, '✨ Hash table demonstration complete!'
    print *, '==========================================='

end program hashtable_demo
