! ============================================================================
! Suffix Array and LCP Array Construction in Fortran
! ============================================================================
!
! Algorithms implemented:
! 1. Naive suffix array construction O(n² log n)
! 2. Kasai's algorithm for LCP array O(n)
!
! Applications:
! - Pattern matching
! - Finding longest repeated substring
! - Counting distinct substrings
!
! Compilation: gfortran -o suffix_array suffix_array.f90
! Usage: ./suffix_array
!
! ============================================================================

module suffix_array_module
    implicit none
    integer, parameter :: MAX_LENGTH = 200

contains

    ! ========================================================================
    ! Build suffix array using naive algorithm (sorting)
    ! Time: O(n² log n)
    ! ========================================================================
    subroutine build_suffix_array(text, n, sa)
        character(len=*), intent(in) :: text
        integer, intent(in) :: n
        integer, dimension(n), intent(out) :: sa
        integer :: i, j, temp
        logical :: swapped

        ! Initialize suffix array with indices
        do i = 1, n
            sa(i) = i
        end do

        ! Bubble sort based on lexicographic order of suffixes
        do i = 1, n - 1
            swapped = .false.
            do j = 1, n - i
                if (text(sa(j):n) > text(sa(j+1):n)) then
                    temp = sa(j)
                    sa(j) = sa(j+1)
                    sa(j+1) = temp
                    swapped = .true.
                end if
            end do
            if (.not. swapped) exit
        end do

    end subroutine build_suffix_array

    ! ========================================================================
    ! Build LCP array using Kasai's algorithm
    ! Time: O(n)
    ! ========================================================================
    subroutine build_lcp_array(text, n, sa, lcp)
        character(len=*), intent(in) :: text
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: sa
        integer, dimension(n), intent(out) :: lcp
        integer, dimension(n) :: rank
        integer :: i, j, h

        ! Initialize LCP array
        lcp = 0

        ! Build rank array (inverse of suffix array)
        do i = 1, n
            rank(sa(i)) = i
        end do

        ! Compute LCP values using Kasai's algorithm
        h = 0
        do i = 1, n
            if (rank(i) > 1) then
                j = sa(rank(i) - 1)

                ! Compute LCP between suffix at i and suffix at j
                do while (i + h <= n .and. j + h <= n)
                    if (text(i+h:i+h) == text(j+h:j+h)) then
                        h = h + 1
                    else
                        exit
                    end if
                end do

                lcp(rank(i)) = h

                ! Decrease h for next iteration
                if (h > 0) then
                    h = h - 1
                end if
            end if
        end do

    end subroutine build_lcp_array

    ! ========================================================================
    ! Pattern search using suffix array
    ! Returns number of matches
    ! ========================================================================
    function pattern_search(text, n, sa, pattern, m, matches) result(count)
        character(len=*), intent(in) :: text, pattern
        integer, intent(in) :: n, m
        integer, dimension(n), intent(in) :: sa
        integer, dimension(n), intent(out) :: matches
        integer :: count
        integer :: i, suffix_idx
        logical :: match_found

        count = 0

        do i = 1, n
            suffix_idx = sa(i)
            if (suffix_idx + m - 1 <= n) then
                match_found = .true.

                ! Check if pattern matches at this suffix
                if (text(suffix_idx:suffix_idx+m-1) == pattern(1:m)) then
                    count = count + 1
                    matches(count) = suffix_idx
                end if
            end if
        end do

    end function pattern_search

    ! ========================================================================
    ! Find longest repeated substring
    ! Returns length of longest repeated substring
    ! ========================================================================
    function longest_repeated_substring(text, n, sa, lcp, result_str) &
        result(max_len)
        character(len=*), intent(in) :: text
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: sa, lcp
        character(len=*), intent(out) :: result_str
        integer :: max_len
        integer :: i, max_idx

        max_len = 0
        max_idx = 0

        ! Find maximum LCP value
        do i = 2, n
            if (lcp(i) > max_len) then
                max_len = lcp(i)
                max_idx = i
            end if
        end do

        if (max_len == 0) then
            result_str = ""
        else
            result_str = text(sa(max_idx):sa(max_idx)+max_len-1)
        end if

    end function longest_repeated_substring

    ! ========================================================================
    ! Count distinct substrings
    ! Formula: n*(n+1)/2 - sum(LCP)
    ! ========================================================================
    function count_distinct_substrings(n, lcp) result(count)
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: lcp
        integer(kind=8) :: count
        integer(kind=8) :: total, duplicates
        integer :: i

        total = int(n, 8) * (int(n, 8) + 1) / 2

        duplicates = 0
        do i = 2, n
            duplicates = duplicates + lcp(i)
        end do

        count = total - duplicates

    end function count_distinct_substrings

    ! ========================================================================
    ! Visualize suffix array and LCP array
    ! ========================================================================
    subroutine visualize_suffix_array(text, n, sa, lcp)
        character(len=*), intent(in) :: text
        integer, intent(in) :: n
        integer, dimension(n), intent(in) :: sa, lcp
        integer :: i
        character(len=60) :: suffix_str

        print *, ""
        print *, "Suffix Array Visualization:"
        print *, "Text: '", trim(text), "'"
        print *, "Length:", n
        print *, ""
        print *, "  i  | SA[i] | LCP[i] | Suffix"
        print *, "-----+-------+--------+", &
                 "--------------------------------"

        do i = 1, n
            suffix_str = text(sa(i):n)
            if (len_trim(suffix_str) > 40) then
                suffix_str = text(sa(i):sa(i)+36) // "..."
            end if
            print '(I4, " |", I5, " |", I6, " | ", A)', &
                i, sa(i), lcp(i), trim(suffix_str)
        end do

        print *, ""

    end subroutine visualize_suffix_array

end module suffix_array_module

! ============================================================================
! MAIN PROGRAM - EXAMPLES AND TESTING
! ============================================================================

program main
    use suffix_array_module
    implicit none

    print *, repeat("=", 70)
    print *, "SUFFIX ARRAY AND LCP ARRAY IN FORTRAN"
    print *, repeat("=", 70)
    print *, ""

    call example_basic_construction()
    call example_pattern_search()
    call example_longest_repeated()
    call example_count_distinct()

    print *, repeat("=", 70)
    print *, "All examples completed successfully!"
    print *, repeat("=", 70)

contains

    ! ========================================================================
    ! Example 1: Basic suffix array construction
    ! ========================================================================
    subroutine example_basic_construction()
        character(len=20) :: text
        integer :: n
        integer, dimension(20) :: sa, lcp

        print *, repeat("=", 70)
        print *, "EXAMPLE 1: Basic Suffix Array Construction"
        print *, repeat("=", 70)

        text = "banana"
        n = 6

        call build_suffix_array(text, n, sa)
        call build_lcp_array(text, n, sa, lcp)
        call visualize_suffix_array(text, n, sa, lcp)

    end subroutine example_basic_construction

    ! ========================================================================
    ! Example 2: Pattern searching
    ! ========================================================================
    subroutine example_pattern_search()
        character(len=50) :: text
        character(len=10) :: pattern
        integer :: n, m, count, i
        integer, dimension(50) :: sa, matches

        print *, repeat("=", 70)
        print *, "EXAMPLE 2: Pattern Searching"
        print *, repeat("=", 70)

        text = "the quick brown fox jumps over the lazy dog"
        pattern = "the"
        n = 44
        m = 3

        call build_suffix_array(text, n, sa)
        count = pattern_search(text, n, sa, pattern, m, matches)

        print *, "Text: '", trim(text), "'"
        print *, "Pattern: '", trim(pattern), "'"
        print *, "Matches:"

        do i = 1, count
            print '(A, I3, A, A)', "  Position ", matches(i), ": '", &
                text(matches(i):matches(i)+m-1), "'"
        end do

        if (count == 0) then
            print *, "  No matches found"
        else
            print *, "Total matches:", count
        end if

        print *, ""

    end subroutine example_pattern_search

    ! ========================================================================
    ! Example 3: Longest repeated substring
    ! ========================================================================
    subroutine example_longest_repeated()
        character(len=20) :: text, result_str
        integer :: n, max_len
        integer, dimension(20) :: sa, lcp

        print *, repeat("=", 70)
        print *, "EXAMPLE 3: Longest Repeated Substring"
        print *, repeat("=", 70)

        text = "abracadabra"
        n = 11

        call build_suffix_array(text, n, sa)
        call build_lcp_array(text, n, sa, lcp)

        max_len = longest_repeated_substring(text, n, sa, lcp, result_str)

        print *, "Text: '", trim(text), "'"
        if (max_len == 0) then
            print *, "No repeated substring found"
        else
            print *, "Longest repeated substring: '", &
                trim(result_str), "' (length:", max_len, ")"
        end if

        print *, ""

    end subroutine example_longest_repeated

    ! ========================================================================
    ! Example 4: Count distinct substrings
    ! ========================================================================
    subroutine example_count_distinct()
        character(len=10) :: text
        integer :: n
        integer, dimension(10) :: sa, lcp
        integer(kind=8) :: count

        print *, repeat("=", 70)
        print *, "EXAMPLE 4: Count Distinct Substrings"
        print *, repeat("=", 70)

        text = "abab"
        n = 4

        call build_suffix_array(text, n, sa)
        call build_lcp_array(text, n, sa, lcp)

        count = count_distinct_substrings(n, lcp)

        print *, "Text: '", trim(text), "'"
        print *, "Number of distinct substrings:", count
        print *, ""

    end subroutine example_count_distinct

end program main
