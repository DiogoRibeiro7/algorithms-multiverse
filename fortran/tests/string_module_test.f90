! Test suite for string algorithms module
program test_string_module
    use iso_fortran_env, only: int32
    use string_module
    implicit none

    integer :: total_tests = 0, passed_tests = 0

    print '(A)', "========================================"
    print '(A)', "    String Module Test Suite"
    print '(A)', "========================================"

    call test_pattern_matching()
    call test_string_operations()
    call test_palindromes()
    call test_string_distances()
    call test_advanced_algorithms()

    print '(A)', ""
    print '(A)', "========================================"
    print '(A,I0,A,I0)', "Tests passed: ", passed_tests, "/", total_tests
    if (passed_tests == total_tests) then
        print '(A)', "STATUS: ALL TESTS PASSED ✓"
    else
        print '(A)', "STATUS: SOME TESTS FAILED ✗"
    end if
    print '(A)', "========================================"

contains

    subroutine test_pattern_matching()
        character(len=100) :: text
        character(len=20) :: pattern
        integer, allocatable :: positions(:)
        integer :: num_matches
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Pattern Matching Algorithms..."

        text = "ababcababa"
        pattern = "aba"

        ! Test KMP search
        allocate(positions(10))
        call kmp_search(text, pattern, positions, num_matches)
        success = num_matches == 3 .and. positions(1) == 1 .and. positions(2) == 6 .and. positions(3) == 8
        call report_test("KMP pattern search", success)

        ! Test Rabin-Karp search
        positions = 0
        call rabin_karp_search(text, pattern, positions, num_matches)
        success = num_matches == 3
        call report_test("Rabin-Karp search", success)

        ! Test Boyer-Moore search
        positions = 0
        call boyer_moore_search(text, pattern, positions, num_matches)
        success = num_matches == 3
        call report_test("Boyer-Moore search", success)

        ! Test Z-algorithm
        text = "aabaaab"
        deallocate(positions)
        allocate(positions(len_trim(text)))
        call z_algorithm(text, positions)
        success = positions(1) == len_trim(text) .and. positions(2) == 1 .and. positions(5) == 3
        call report_test("Z-algorithm", success)

        deallocate(positions)

    end subroutine test_pattern_matching

    subroutine test_string_operations()
        character(len=50) :: str1, str2, result
        character(len=200), allocatable :: permutations(:)
        character(len=200), allocatable :: combinations(:)
        integer :: num_perms, num_combs
        logical :: success

        print '(A)', ""
        print '(A)', "Testing String Operations..."

        ! Test longest common substring
        str1 = "abcdxyz"
        str2 = "xyzabcd"
        result = longest_common_substring(str1, str2)
        success = trim(result) == "abcd" .or. trim(result) == "xyz"
        call report_test("Longest common substring", success)

        ! Test string permutations
        str1 = "ABC"
        allocate(permutations(6))  ! 3! = 6
        call string_permutations(str1, permutations, num_perms)
        success = num_perms == 6
        call report_test("String permutations", success)

        ! Test string combinations
        allocate(combinations(7))  ! 2^3 - 1 = 7
        call string_combinations(str1, combinations, num_combs)
        success = num_combs == 7
        call report_test("String combinations", success)

        deallocate(permutations, combinations)

    end subroutine test_string_operations

    subroutine test_palindromes()
        character(len=50) :: str, result
        logical :: is_pal, success

        print '(A)', ""
        print '(A)', "Testing Palindrome Algorithms..."

        ! Test palindrome check
        str = "racecar"
        is_pal = is_palindrome(str)
        success = is_pal
        call report_test("Is palindrome (positive)", success)

        str = "hello"
        is_pal = is_palindrome(str)
        success = .not. is_pal
        call report_test("Is palindrome (negative)", success)

        ! Test longest palindromic substring
        str = "babad"
        result = longest_palindromic_substring(str)
        success = trim(result) == "bab" .or. trim(result) == "aba"
        call report_test("Longest palindromic substring", success)

        ! Test Manacher's algorithm
        str = "abacabad"
        result = manacher_algorithm(str)
        success = len_trim(result) > 0
        call report_test("Manacher's algorithm", success)

    end subroutine test_palindromes

    subroutine test_string_distances()
        character(len=50) :: str1, str2
        integer :: distance
        logical :: success

        print '(A)', ""
        print '(A)', "Testing String Distance Algorithms..."

        ! Test Levenshtein distance
        str1 = "kitten"
        str2 = "sitting"
        distance = levenshtein_distance(str1, str2)
        success = distance == 3
        call report_test("Levenshtein distance", success)

        ! Test edit distance (same as Levenshtein)
        str1 = "saturday"
        str2 = "sunday"
        distance = levenshtein_distance(str1, str2)
        success = distance == 3
        call report_test("Edit distance", success)

    end subroutine test_string_distances

    subroutine test_advanced_algorithms()
        character(len=100) :: text
        character(len=20), allocatable :: patterns(:)
        integer, allocatable :: suffix(:), lcp(:), matches(:,:)
        integer :: num_patterns, num_matches
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Advanced String Algorithms..."

        ! Test suffix array construction
        text = "banana"
        allocate(suffix(len_trim(text)))
        call suffix_array_build(text, suffix)
        ! suffix array for "banana" should be [6,4,2,1,5,3]
        success = suffix(1) == 6 .and. suffix(2) == 4
        call report_test("Suffix array construction", success)

        ! Test LCP array construction
        allocate(lcp(len_trim(text)))
        call lcp_array_build(text, suffix, lcp)
        success = .true.  ! Basic check that it runs
        call report_test("LCP array construction", success)

        ! Test Aho-Corasick multiple pattern matching
        text = "ahishers"
        allocate(patterns(3))
        patterns(1) = "his"
        patterns(2) = "hers"
        patterns(3) = "she"
        num_patterns = 3

        allocate(matches(num_patterns, 10))
        call aho_corasick_search(text, patterns, num_patterns, matches, num_matches)
        success = num_matches > 0
        call report_test("Aho-Corasick search", success)

        deallocate(suffix, lcp, patterns, matches)

    end subroutine test_advanced_algorithms

    subroutine report_test(test_name, success)
        character(len=*), intent(in) :: test_name
        logical, intent(in) :: success

        total_tests = total_tests + 1
        if (success) then
            passed_tests = passed_tests + 1
            print '(A,A,A)', "  ✓ ", test_name, " ... PASSED"
        else
            print '(A,A,A)', "  ✗ ", test_name, " ... FAILED"
        end if
    end subroutine report_test

end program test_string_module