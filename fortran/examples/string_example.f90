! Example program demonstrating string algorithms
program string_example
    use iso_fortran_env, only: int32
    use string_module
    implicit none

    character(len=100) :: text, pattern, result
    character(len=50) :: str1, str2
    integer, allocatable :: positions(:), suffix(:)
    integer :: num_matches, distance
    logical :: is_pal

    print '(A)', "========================================"
    print '(A)', "    String Algorithms Examples"
    print '(A)', "========================================"

    ! Example 1: Pattern matching
    print '(A)', ""
    print '(A)', "Example 1: Pattern Matching"
    print '(A)', "----------------------------"

    text = "The quick brown fox jumps over the lazy dog. The fox is quick."
    pattern = "fox"

    allocate(positions(10))

    ! KMP search
    call kmp_search(text, pattern, positions, num_matches)
    print '(A)', "Text: ", trim(text)
    print '(A)', "Pattern: ", trim(pattern)
    print '(A,I0)', "Number of matches found: ", num_matches
    print '(A)', "Match positions: ", positions(1:num_matches)

    ! Rabin-Karp search
    pattern = "quick"
    call rabin_karp_search(text, pattern, positions, num_matches)
    print '(A)', ""
    print '(A)', "Pattern: ", trim(pattern)
    print '(A,I0)', "Rabin-Karp matches: ", num_matches
    print '(A)', "Positions: ", positions(1:num_matches)

    ! Example 2: String operations
    print '(A)', ""
    print '(A)', "Example 2: String Operations"
    print '(A)', "-----------------------------"

    str1 = "ABCDEFG"
    str2 = "BCDEFGH"

    ! Longest common substring
    result = longest_common_substring(str1, str2)
    print '(A)', "String 1: ", trim(str1)
    print '(A)', "String 2: ", trim(str2)
    print '(A)', "Longest common substring: ", trim(result)

    ! Levenshtein distance
    str1 = "kitten"
    str2 = "sitting"
    distance = levenshtein_distance(str1, str2)
    print '(A)', ""
    print '(A)', "String 1: ", trim(str1)
    print '(A)', "String 2: ", trim(str2)
    print '(A,I0)', "Levenshtein distance: ", distance

    ! Example 3: Palindrome algorithms
    print '(A)', ""
    print '(A)', "Example 3: Palindrome Detection"
    print '(A)', "--------------------------------"

    str1 = "racecar"
    is_pal = is_palindrome(str1)
    print '(A,A,L1)', "Is '", trim(str1), "' a palindrome? ", is_pal

    str1 = "A man a plan a canal Panama"
    ! Remove spaces for palindrome check
    str2 = str1
    call remove_spaces(str2)
    is_pal = is_palindrome(str2)
    print '(A,A,L1)', "Is '", trim(str1), "' a palindrome (ignoring spaces)? ", is_pal

    ! Longest palindromic substring
    str1 = "babad"
    result = longest_palindromic_substring(str1)
    print '(A)', ""
    print '(A)', "String: ", trim(str1)
    print '(A)', "Longest palindromic substring: ", trim(result)

    ! Example 4: Advanced string algorithms
    print '(A)', ""
    print '(A)', "Example 4: Suffix Array"
    print '(A)', "------------------------"

    text = "banana"
    allocate(suffix(len_trim(text)))

    call suffix_array_build(text, suffix)
    print '(A)', "Text: ", trim(text)
    print '(A)', "Suffix array: ", suffix

    print '(A)', "Sorted suffixes:"
    do i = 1, len_trim(text)
        print '(A,I0,A,A)', "  ", i, ": ", text(suffix(i):len_trim(text))
    end do

    ! Example 5: String permutations
    print '(A)', ""
    print '(A)', "Example 5: String Permutations"
    print '(A)', "-------------------------------"

    str1 = "ABC"
    call demonstrate_permutations(str1)

    ! Clean up
    deallocate(positions, suffix)

    print '(A)', ""
    print '(A)', "========================================"
    print '(A)', "    String Examples Complete"
    print '(A)', "========================================"

contains

    subroutine remove_spaces(str)
        character(len=*), intent(inout) :: str
        character(len=len(str)) :: temp
        integer :: i, j

        j = 0
        do i = 1, len_trim(str)
            if (str(i:i) /= ' ') then
                j = j + 1
                temp(j:j) = str(i:i)
            end if
        end do
        str = temp(1:j)
    end subroutine remove_spaces

    subroutine demonstrate_permutations(str)
        character(len=*), intent(in) :: str
        character(len=200), allocatable :: perms(:)
        integer :: num_perms, i

        allocate(perms(6))  ! 3! = 6 permutations
        call string_permutations(str, perms, num_perms)

        print '(A,A)', "Permutations of '", trim(str), "':"
        do i = 1, num_perms
            print '(A,A)', "  ", trim(perms(i))
        end do

        deallocate(perms)
    end subroutine demonstrate_permutations

    integer :: i  ! Loop variable

end program string_example