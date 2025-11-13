! Trie (Prefix Tree) Data Structure in Modern Fortran
!
! Features:
! - Array-based trie implementation
! - Insert, search, starts_with operations
! - Word counting and prefix matching
! - Dictionary applications
! - Auto-complete functionality
!
! Note: This is a simplified implementation using sorted arrays
! A full trie would use pointer-based tree structures which are
! complex in Fortran due to limited support for recursive data structures
!
! Compilation:
!   gfortran -O2 -o trie trie.f90
!   ./trie
!
! Author: Algorithms Multiverse

module trie_module
    implicit none
    private

    integer, parameter :: MAX_WORD_LENGTH = 100
    integer, parameter :: MAX_WORDS = 1000

    ! Trie using sorted array storage
    type, public :: trie
        private
        character(len=MAX_WORD_LENGTH) :: words(MAX_WORDS)
        integer :: word_count = 0
    contains
        procedure, public :: insert => trie_insert
        procedure, public :: search => trie_search
        procedure, public :: starts_with => trie_starts_with
        procedure, public :: delete => trie_delete
        procedure, public :: count_words => trie_count_words
        procedure, public :: count_prefix => trie_count_with_prefix
        procedure, public :: get_words_with_prefix => trie_get_words_with_prefix
        procedure, public :: print_all => trie_print_all
        procedure, public :: clear => trie_clear
    end type trie

contains

    ! ========================================================================
    ! INSERT
    ! ========================================================================

    subroutine trie_insert(this, word)
        class(trie), intent(inout) :: this
        character(len=*), intent(in) :: word
        character(len=MAX_WORD_LENGTH) :: normalized_word
        integer :: i, insert_pos

        ! Normalize word (convert to lowercase, trim)
        normalized_word = trim(adjustl(word))
        call to_lowercase(normalized_word)

        ! Check if word already exists
        do i = 1, this%word_count
            if (trim(this%words(i)) == trim(normalized_word)) then
                return  ! Word already exists
            end if
        end do

        ! Check capacity
        if (this%word_count >= MAX_WORDS) then
            print *, 'Error: Trie is full!'
            return
        end if

        ! Find insert position to keep sorted
        insert_pos = this%word_count + 1
        do i = 1, this%word_count
            if (trim(normalized_word) < trim(this%words(i))) then
                insert_pos = i
                exit
            end if
        end do

        ! Shift words to make room
        do i = this%word_count, insert_pos, -1
            this%words(i + 1) = this%words(i)
        end do

        ! Insert new word
        this%words(insert_pos) = normalized_word
        this%word_count = this%word_count + 1
    end subroutine trie_insert

    ! ========================================================================
    ! SEARCH
    ! ========================================================================

    function trie_search(this, word) result(found)
        class(trie), intent(in) :: this
        character(len=*), intent(in) :: word
        logical :: found
        character(len=MAX_WORD_LENGTH) :: normalized_word
        integer :: i

        normalized_word = trim(adjustl(word))
        call to_lowercase(normalized_word)

        found = .false.
        do i = 1, this%word_count
            if (trim(this%words(i)) == trim(normalized_word)) then
                found = .true.
                return
            end if
        end do
    end function trie_search

    ! ========================================================================
    ! STARTS WITH (PREFIX SEARCH)
    ! ========================================================================

    function trie_starts_with(this, prefix) result(found)
        class(trie), intent(in) :: this
        character(len=*), intent(in) :: prefix
        logical :: found
        character(len=MAX_WORD_LENGTH) :: normalized_prefix
        integer :: i, prefix_len

        normalized_prefix = trim(adjustl(prefix))
        call to_lowercase(normalized_prefix)
        prefix_len = len_trim(normalized_prefix)

        found = .false.
        do i = 1, this%word_count
            if (len_trim(this%words(i)) >= prefix_len) then
                if (this%words(i)(1:prefix_len) == normalized_prefix(1:prefix_len)) then
                    found = .true.
                    return
                end if
            end if
        end do
    end function trie_starts_with

    ! ========================================================================
    ! DELETE
    ! ========================================================================

    subroutine trie_delete(this, word)
        class(trie), intent(inout) :: this
        character(len=*), intent(in) :: word
        character(len=MAX_WORD_LENGTH) :: normalized_word
        integer :: i, delete_pos

        normalized_word = trim(adjustl(word))
        call to_lowercase(normalized_word)

        delete_pos = -1
        do i = 1, this%word_count
            if (trim(this%words(i)) == trim(normalized_word)) then
                delete_pos = i
                exit
            end if
        end do

        if (delete_pos == -1) then
            return  ! Word not found
        end if

        ! Shift words to fill gap
        do i = delete_pos, this%word_count - 1
            this%words(i) = this%words(i + 1)
        end do

        this%word_count = this%word_count - 1
    end subroutine trie_delete

    ! ========================================================================
    ! WORD COUNTING
    ! ========================================================================

    function trie_count_words(this) result(count)
        class(trie), intent(in) :: this
        integer :: count

        count = this%word_count
    end function trie_count_words

    function trie_count_with_prefix(this, prefix) result(count)
        class(trie), intent(in) :: this
        character(len=*), intent(in) :: prefix
        integer :: count
        character(len=MAX_WORD_LENGTH) :: normalized_prefix
        integer :: i, prefix_len

        normalized_prefix = trim(adjustl(prefix))
        call to_lowercase(normalized_prefix)
        prefix_len = len_trim(normalized_prefix)

        count = 0
        do i = 1, this%word_count
            if (len_trim(this%words(i)) >= prefix_len) then
                if (this%words(i)(1:prefix_len) == normalized_prefix(1:prefix_len)) then
                    count = count + 1
                end if
            end if
        end do
    end function trie_count_with_prefix

    ! ========================================================================
    ! GET WORDS WITH PREFIX
    ! ========================================================================

    subroutine trie_get_words_with_prefix(this, prefix)
        class(trie), intent(in) :: this
        character(len=*), intent(in) :: prefix
        character(len=MAX_WORD_LENGTH) :: normalized_prefix
        integer :: i, prefix_len, count

        normalized_prefix = trim(adjustl(prefix))
        call to_lowercase(normalized_prefix)
        prefix_len = len_trim(normalized_prefix)

        count = 0
        do i = 1, this%word_count
            if (len_trim(this%words(i)) >= prefix_len) then
                if (this%words(i)(1:prefix_len) == normalized_prefix(1:prefix_len)) then
                    print '(A)', '  ' // trim(this%words(i))
                    count = count + 1
                end if
            end if
        end do

        if (count == 0) then
            print '(A)', '  (none)'
        end if
    end subroutine trie_get_words_with_prefix

    ! ========================================================================
    ! PRINT ALL WORDS
    ! ========================================================================

    subroutine trie_print_all(this)
        class(trie), intent(in) :: this
        integer :: i

        if (this%word_count == 0) then
            print *, 'Trie is empty'
            return
        end if

        print '(A)', 'Words in trie:'
        do i = 1, this%word_count
            print '(A)', '  ' // trim(this%words(i))
        end do
    end subroutine trie_print_all

    ! ========================================================================
    ! CLEAR
    ! ========================================================================

    subroutine trie_clear(this)
        class(trie), intent(inout) :: this

        this%word_count = 0
    end subroutine trie_clear

    ! ========================================================================
    ! UTILITY FUNCTIONS
    ! ========================================================================

    subroutine to_lowercase(str)
        character(len=*), intent(inout) :: str
        integer :: i
        character :: ch

        do i = 1, len_trim(str)
            ch = str(i:i)
            if (ch >= 'A' .and. ch <= 'Z') then
                str(i:i) = char(ichar(ch) + 32)
            end if
        end do
    end subroutine to_lowercase

end module trie_module

! ============================================================================
! DEMONSTRATION PROGRAM
! ============================================================================

program test_trie
    use trie_module
    implicit none

    type(trie) :: dictionary
    integer :: count
    character(len=50) :: test_word

    print '(A)', repeat('=', 75)
    print '(A)', '                TRIE (PREFIX TREE) - FORTRAN'
    print '(A)', repeat('=', 75)
    print *

    ! Test 1: Basic insertions
    print '(A)', 'Test 1: Basic Insert and Search'
    print '(A)', repeat('-', 75)

    print *, 'Inserting words: the, there, their, answer, any, bye'
    call dictionary%insert('the')
    call dictionary%insert('there')
    call dictionary%insert('their')
    call dictionary%insert('answer')
    call dictionary%insert('any')
    call dictionary%insert('bye')

    print '(A, I0)', 'Total words in trie: ', dictionary%count_words()
    print *

    ! Test 2: Search operations
    print '(A)', 'Test 2: Search Operations'
    print '(A)', repeat('-', 75)

    test_word = 'the'
    print '(A, A, A, L1)', 'Search for "', trim(test_word), '": ', &
          dictionary%search(test_word)

    test_word = 'these'
    print '(A, A, A, L1)', 'Search for "', trim(test_word), '": ', &
          dictionary%search(test_word)

    test_word = 'answer'
    print '(A, A, A, L1)', 'Search for "', trim(test_word), '": ', &
          dictionary%search(test_word)

    test_word = 'ant'
    print '(A, A, A, L1)', 'Search for "', trim(test_word), '": ', &
          dictionary%search(test_word)
    print *

    ! Test 3: Prefix matching
    print '(A)', 'Test 3: Prefix Matching (startsWith)'
    print '(A)', repeat('-', 75)

    test_word = 'th'
    print '(A, A, A, L1)', 'Starts with "', trim(test_word), '": ', &
          dictionary%starts_with(test_word)
    count = dictionary%count_prefix(test_word)
    print '(A, I0)', '  Words with this prefix: ', count
    call dictionary%get_words_with_prefix(test_word)
    print *

    test_word = 'an'
    print '(A, A, A, L1)', 'Starts with "', trim(test_word), '": ', &
          dictionary%starts_with(test_word)
    count = dictionary%count_prefix(test_word)
    print '(A, I0)', '  Words with this prefix: ', count
    call dictionary%get_words_with_prefix(test_word)
    print *

    test_word = 'by'
    print '(A, A, A, L1)', 'Starts with "', trim(test_word), '": ', &
          dictionary%starts_with(test_word)
    print *

    test_word = 'cat'
    print '(A, A, A, L1)', 'Starts with "', trim(test_word), '": ', &
          dictionary%starts_with(test_word)
    print *

    ! Test 4: Print all words
    print '(A)', 'Test 4: All Words in Trie (sorted)'
    print '(A)', repeat('-', 75)
    call dictionary%print_all()
    print *

    ! Test 5: Deletion
    print '(A)', 'Test 5: Delete Operations'
    print '(A)', repeat('-', 75)

    print *, 'Deleting word: "their"'
    call dictionary%delete('their')
    print '(A, I0)', 'Total words after deletion: ', dictionary%count_words()
    print *

    print '(A)', 'Remaining words:'
    call dictionary%print_all()
    print *

    ! Test 6: Auto-complete scenario
    call dictionary%clear()

    print '(A)', 'Test 6: Auto-Complete Example'
    print '(A)', repeat('-', 75)

    print *, 'Building programming language dictionary...'
    call dictionary%insert('fortran')
    call dictionary%insert('forth')
    call dictionary%insert('python')
    call dictionary%insert('pascal')
    call dictionary%insert('perl')
    call dictionary%insert('php')
    call dictionary%insert('prolog')
    call dictionary%insert('povray')
    print *

    print '(A)', 'All programming languages in dictionary:'
    call dictionary%print_all()
    print *

    print '(A)', 'Words starting with "for":'
    call dictionary%get_words_with_prefix('for')
    print *

    print '(A)', 'Words starting with "p":'
    count = dictionary%count_prefix('p')
    print '(A, I0, A)', 'Count: ', count, ' words'
    call dictionary%get_words_with_prefix('p')
    print *

    print '(A)', 'Words starting with "py":'
    call dictionary%get_words_with_prefix('py')
    print *

    ! Test 7: Case insensitivity
    print '(A)', 'Test 7: Case Insensitivity'
    print '(A)', repeat('-', 75)

    call dictionary%clear()
    call dictionary%insert('Fortran')
    call dictionary%insert('PYTHON')
    call dictionary%insert('RuSt')

    print '(A)', 'Inserted: Fortran, PYTHON, RuSt'
    print '(A)', 'Stored words (normalized):'
    call dictionary%print_all()
    print *

    print '(A, L1)', 'Search for "fortran": ', dictionary%search('fortran')
    print '(A, L1)', 'Search for "PYTHON": ', dictionary%search('PYTHON')
    print '(A, L1)', 'Search for "rust": ', dictionary%search('rust')
    print *

    ! Summary
    print '(A)', repeat('=', 75)
    print '(A)', 'TRIE COMPLEXITY SUMMARY'
    print '(A)', repeat('=', 75)
    print '(A)', 'Operation       Time         Space'
    print '(A)', repeat('-', 75)
    print '(A)', 'Insert          O(n*m)       O(n*m)'
    print '(A)', 'Search          O(n*m)       O(1)'
    print '(A)', 'Delete          O(n*m)       O(1)'
    print '(A)', 'Prefix Match    O(n*m)       O(1)'
    print '(A)', ''
    print '(A)', 'where n = number of words, m = length of word/prefix'
    print '(A)', ''
    print '(A)', 'Note: This is a simplified array-based implementation'
    print '(A)', '      A pointer-based trie would have O(m) insert/search'
    print '(A)', ''
    print '(A)', 'Applications:'
    print '(A)', '- Auto-complete / Type-ahead search'
    print '(A)', '- Spell checking'
    print '(A)', '- IP routing (longest prefix matching)'
    print '(A)', '- Dictionary implementation'
    print '(A)', '- T9 predictive text'
    print '(A)', '- Genome sequence analysis'
    print '(A)', repeat('=', 75)

end program test_trie
