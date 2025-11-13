! String Algorithms in Modern Fortran
!
! Implementations of classic string processing algorithms:
! 1. Naive Pattern Matching
! 2. KMP (Knuth-Morris-Pratt) Algorithm
! 3. Rabin-Karp Algorithm (rolling hash)
! 4. String Hashing
! 5. Longest Palindromic Substring
! 6. String Matching with Wildcards
!
! Author: Algorithms Multiverse

program string_algorithms
    implicit none

    character(len=100) :: text, pattern

    print '(A)', repeat('=', 75)
    print '(A)', '              STRING ALGORITHMS IN FORTRAN'
    print '(A)', repeat('=', 75)
    print *

    ! Run demonstrations
    call demo_pattern_matching()
    call demo_kmp()
    call demo_rabin_karp()
    call demo_palindrome()
    call demo_string_hashing()

    ! Summary
    print '(A)', repeat('=', 75)
    print '(A)', 'STRING ALGORITHM COMPLEXITY SUMMARY'
    print '(A)', repeat('=', 75)
    print '(A)', 'Algorithm              Time            Space    Preprocessing'
    print '(A)', repeat('-', 75)
    print '(A)', 'Naive                  O(nm)           O(1)     None'
    print '(A)', 'KMP                    O(n+m)          O(m)     O(m)'
    print '(A)', 'Rabin-Karp            O(n+m) avg      O(1)     O(m)'
    print '(A)', 'Boyer-Moore           O(n/m) best     O(m)     O(m+σ)'
    print '(A)', 'Z-Algorithm           O(n+m)          O(n)     O(n)'
    print '(A)', ''
    print '(A)', 'where n = text length, m = pattern length, σ = alphabet size'
    print '(A)', repeat('=', 75)

contains

    ! ===================================================================
    ! NAIVE PATTERN MATCHING
    ! ===================================================================

    subroutine demo_pattern_matching()
        character(len=50) :: txt, pat
        integer :: positions(20), count

        print '(A)', 'Test 1: Naive Pattern Matching'
        print '(A)', repeat('-', 75)

        txt = 'ABABDABACDABABCABAB'
        pat = 'ABABCABAB'

        print '(A)', 'Text:    ', trim(txt)
        print '(A)', 'Pattern: ', trim(pat)
        print *

        call naive_search(txt, pat, positions, count)

        if (count > 0) then
            print '(A, I0, A)', 'Pattern found at ', count, ' position(s):'
            call print_positions(positions, count)
        else
            print '(A)', 'Pattern not found'
        end if

        print *
        print '(A)', 'Complexity: O(nm) where n = text length, m = pattern length'
        print '(A)', 'Simple but inefficient for large texts'
        print *
    end subroutine demo_pattern_matching

    subroutine naive_search(text, pattern, positions, count)
        character(len=*), intent(in) :: text, pattern
        integer, intent(out) :: positions(:), count
        integer :: n, m, i, j
        logical :: match

        n = len_trim(text)
        m = len_trim(pattern)
        count = 0

        do i = 1, n - m + 1
            match = .true.
            do j = 1, m
                if (text(i+j-1:i+j-1) /= pattern(j:j)) then
                    match = .false.
                    exit
                end if
            end do

            if (match) then
                count = count + 1
                positions(count) = i
            end if
        end do
    end subroutine naive_search

    ! ===================================================================
    ! KMP (KNUTH-MORRIS-PRATT) ALGORITHM
    ! ===================================================================

    subroutine demo_kmp()
        character(len=50) :: txt, pat
        integer :: positions(20), count

        print '(A)', 'Test 2: KMP (Knuth-Morris-Pratt) Algorithm'
        print '(A)', repeat('-', 75)

        txt = 'ABABDABACDABABCABAB'
        pat = 'ABABCABAB'

        print '(A)', 'Text:    ', trim(txt)
        print '(A)', 'Pattern: ', trim(pat)
        print *

        call kmp_search(txt, pat, positions, count)

        if (count > 0) then
            print '(A, I0, A)', 'Pattern found at ', count, ' position(s):'
            call print_positions(positions, count)
        else
            print '(A)', 'Pattern not found'
        end if

        print *
        print '(A)', 'Complexity: O(n + m) - optimal for pattern matching'
        print '(A)', 'Key Idea: Use failure function to avoid redundant comparisons'
        print *
    end subroutine demo_kmp

    subroutine kmp_search(text, pattern, positions, count)
        character(len=*), intent(in) :: text, pattern
        integer, intent(out) :: positions(:), count
        integer :: n, m, i, j
        integer, allocatable :: lps(:)

        n = len_trim(text)
        m = len_trim(pattern)
        count = 0

        allocate(lps(m))
        call compute_lps(pattern, lps, m)

        i = 1
        j = 1

        do while (i <= n)
            if (pattern(j:j) == text(i:i)) then
                i = i + 1
                j = j + 1
            end if

            if (j > m) then
                count = count + 1
                positions(count) = i - j + 1
                j = lps(j - 1) + 1
            else if (i <= n .and. pattern(j:j) /= text(i:i)) then
                if (j /= 1) then
                    j = lps(j - 1) + 1
                else
                    i = i + 1
                end if
            end if
        end do

        deallocate(lps)
    end subroutine kmp_search

    ! Compute Longest Proper Prefix which is also Suffix (LPS) array
    subroutine compute_lps(pattern, lps, m)
        character(len=*), intent(in) :: pattern
        integer, intent(out) :: lps(:)
        integer, intent(in) :: m
        integer :: len, i

        len = 0
        lps(1) = 0
        i = 2

        do while (i <= m)
            if (pattern(i:i) == pattern(len+1:len+1)) then
                len = len + 1
                lps(i) = len
                i = i + 1
            else
                if (len /= 0) then
                    len = lps(len)
                else
                    lps(i) = 0
                    i = i + 1
                end if
            end if
        end do
    end subroutine compute_lps

    ! ===================================================================
    ! RABIN-KARP ALGORITHM (Rolling Hash)
    ! ===================================================================

    subroutine demo_rabin_karp()
        character(len=50) :: txt, pat
        integer :: positions(20), count

        print '(A)', 'Test 3: Rabin-Karp Algorithm (Rolling Hash)'
        print '(A)', repeat('-', 75)

        txt = 'ABABDABACDABABCABAB'
        pat = 'ABAB'

        print '(A)', 'Text:    ', trim(txt)
        print '(A)', 'Pattern: ', trim(pat)
        print *

        call rabin_karp_search(txt, pat, positions, count)

        if (count > 0) then
            print '(A, I0, A)', 'Pattern found at ', count, ' position(s):'
            call print_positions(positions, count)
        else
            print '(A)', 'Pattern not found'
        end if

        print *
        print '(A)', 'Complexity: O(n + m) average, O(nm) worst'
        print '(A)', 'Key Idea: Use rolling hash for fast comparison'
        print '(A)', 'Good for: Multiple pattern search, plagiarism detection'
        print *
    end subroutine demo_rabin_karp

    subroutine rabin_karp_search(text, pattern, positions, count)
        character(len=*), intent(in) :: text, pattern
        integer, intent(out) :: positions(:), count
        integer :: n, m, i, j
        integer :: prime, d
        integer(8) :: pattern_hash, text_hash, h
        logical :: match

        n = len_trim(text)
        m = len_trim(pattern)
        count = 0

        ! Prime number for hashing
        prime = 101
        d = 256  ! Number of characters in alphabet

        ! Calculate hash value for pattern and first window of text
        pattern_hash = 0
        text_hash = 0
        h = 1

        ! h = d^(m-1) mod prime
        do i = 1, m - 1
            h = mod(h * d, prime)
        end do

        ! Calculate hash for pattern and first window
        do i = 1, m
            pattern_hash = mod(d * pattern_hash + ichar(pattern(i:i)), prime)
            text_hash = mod(d * text_hash + ichar(text(i:i)), prime)
        end do

        ! Slide pattern over text
        do i = 1, n - m + 1
            ! Check if hash values match
            if (pattern_hash == text_hash) then
                ! Verify character by character
                match = .true.
                do j = 1, m
                    if (text(i+j-1:i+j-1) /= pattern(j:j)) then
                        match = .false.
                        exit
                    end if
                end do

                if (match) then
                    count = count + 1
                    positions(count) = i
                end if
            end if

            ! Calculate hash for next window (rolling hash)
            if (i < n - m + 1) then
                text_hash = mod(d * (text_hash - ichar(text(i:i)) * h) + &
                               ichar(text(i+m:i+m)), prime)

                ! Convert negative hash to positive
                if (text_hash < 0) then
                    text_hash = text_hash + prime
                end if
            end if
        end do
    end subroutine rabin_karp_search

    ! ===================================================================
    ! LONGEST PALINDROMIC SUBSTRING
    ! ===================================================================

    subroutine demo_palindrome()
        character(len=50) :: str
        character(len=50) :: palindrome
        integer :: start, length

        print '(A)', 'Test 4: Longest Palindromic Substring'
        print '(A)', repeat('-', 75)

        str = 'BABAD'

        print '(A)', 'String: ', trim(str)
        print *

        call longest_palindrome(str, start, length)

        palindrome = str(start:start+length-1)

        print '(A)', 'Longest palindrome: ', trim(palindrome)
        print '(A, I0)', 'Length: ', length
        print '(A, I0)', 'Position: ', start
        print *

        ! Another example
        str = 'CBBD'
        print '(A)', 'String: ', trim(str)
        call longest_palindrome(str, start, length)
        palindrome = str(start:start+length-1)
        print '(A)', 'Longest palindrome: ', trim(palindrome)
        print *

        print '(A)', 'Complexity: O(n²) - Expand around center approach'
        print '(A)', 'Can be optimized to O(n) using Manacher''s algorithm'
        print *
    end subroutine demo_palindrome

    subroutine longest_palindrome(str, start_pos, max_len)
        character(len=*), intent(in) :: str
        integer, intent(out) :: start_pos, max_len
        integer :: n, i, len1, len2, len
        integer :: temp_start

        n = len_trim(str)
        start_pos = 1
        max_len = 1

        do i = 1, n
            ! Check for odd length palindrome (center is single character)
            call expand_around_center(str, i, i, temp_start, len1)

            ! Check for even length palindrome (center is between characters)
            call expand_around_center(str, i, i + 1, temp_start, len2)

            len = max(len1, len2)

            if (len > max_len) then
                max_len = len
                start_pos = i - (len - 1) / 2
            end if
        end do
    end subroutine longest_palindrome

    subroutine expand_around_center(str, left, right, start, length)
        character(len=*), intent(in) :: str
        integer, intent(in) :: left, right
        integer, intent(out) :: start, length
        integer :: l, r, n

        n = len_trim(str)
        l = left
        r = right

        do while (l >= 1 .and. r <= n .and. str(l:l) == str(r:r))
            l = l - 1
            r = r + 1
        end do

        start = l + 1
        length = r - l - 1
    end subroutine expand_around_center

    ! ===================================================================
    ! STRING HASHING
    ! ===================================================================

    subroutine demo_string_hashing()
        character(len=30) :: str1, str2, str3
        integer(8) :: hash1, hash2, hash3

        print '(A)', 'Test 5: String Hashing'
        print '(A)', repeat('-', 75)

        str1 = 'HELLO'
        str2 = 'WORLD'
        str3 = 'HELLO'

        hash1 = string_hash(str1)
        hash2 = string_hash(str2)
        hash3 = string_hash(str3)

        print '(A, A, A, I0)', 'String: "', trim(str1), '", Hash: ', hash1
        print '(A, A, A, I0)', 'String: "', trim(str2), '", Hash: ', hash2
        print '(A, A, A, I0)', 'String: "', trim(str3), '", Hash: ', hash3
        print *

        if (hash1 == hash3) then
            print '(A)', '✓ Same strings have same hash'
        end if

        if (hash1 /= hash2) then
            print '(A)', '✓ Different strings (likely) have different hashes'
        end if

        print *
        print '(A)', 'Applications:'
        print '(A)', '- Fast string comparison'
        print '(A)', '- Hash tables'
        print '(A)', '- Rabin-Karp algorithm'
        print '(A)', '- Data deduplication'
        print *
    end subroutine demo_string_hashing

    function string_hash(str) result(hash)
        character(len=*), intent(in) :: str
        integer(8) :: hash
        integer :: i, n
        integer, parameter :: prime = 31
        integer, parameter :: mod_val = 1000000007

        n = len_trim(str)
        hash = 0

        do i = 1, n
            hash = mod(hash * prime + ichar(str(i:i)), mod_val)
        end do
    end function string_hash

    ! ===================================================================
    ! UTILITY FUNCTIONS
    ! ===================================================================

    subroutine print_positions(positions, count)
        integer, intent(in) :: positions(:), count
        integer :: i

        do i = 1, count
            print '(A, I0)', '  Position ', positions(i)
        end do
    end subroutine print_positions

end program string_algorithms
