! String Algorithms Module
! Collection of string matching and manipulation algorithms

module string_module
    use iso_fortran_env, only: int32, int64, real32, real64
    implicit none
    private

    ! Public interfaces
    public :: naive_search, kmp_search, rabin_karp_search
    public :: boyer_moore_search, z_algorithm, manacher_algorithm
    public :: longest_palindrome, all_palindromes
    public :: suffix_array, lcp_array, build_suffix_tree
    public :: aho_corasick_search, string_hash
    public :: levenshtein_distance, hamming_distance
    public :: longest_common_prefix, longest_repeated_substring
    public :: knuth_morris_pratt, string_matching_automaton
    public :: is_anagram, is_palindrome, is_rotation
    public :: compress_string, decompress_string
    public :: run_length_encoding, run_length_decoding
    public :: burrows_wheeler_transform, inverse_bwt

    ! Constants
    integer(int32), parameter :: ALPHABET_SIZE = 256
    integer(int64), parameter :: PRIME = 1000000007_int64
    integer(int64), parameter :: BASE = 256_int64

    ! Suffix tree node
    type :: suffix_node
        integer(int32) :: start
        integer(int32), pointer :: end_ptr
        integer(int32) :: suffix_link
        type(suffix_node), pointer :: children(:)
        integer(int32) :: suffix_index
    contains
        procedure :: init => suffix_node_init
    end type suffix_node

    ! Trie node for Aho-Corasick
    type :: trie_node
        type(trie_node), pointer :: children(:)
        type(trie_node), pointer :: failure_link
        integer(int32), dimension(:), allocatable :: output
        logical :: is_end
    contains
        procedure :: init => trie_node_init
    end type trie_node

contains

    !===============================================
    ! Naive String Search
    !===============================================

    function naive_search(text, pattern) result(positions)
        implicit none
        character(len=*), intent(in) :: text, pattern
        integer(int32), dimension(:), allocatable :: positions
        integer(int32) :: n, m, i, j, count
        integer(int32), dimension(:), allocatable :: temp_pos

        n = len_trim(text)
        m = len_trim(pattern)

        if (m > n) then
            allocate(positions(0))
            return
        end if

        allocate(temp_pos(n))
        count = 0

        do i = 1, n - m + 1
            j = 1
            do while (j <= m .and. text(i+j-1:i+j-1) == pattern(j:j))
                j = j + 1
            end do

            if (j > m) then
                count = count + 1
                temp_pos(count) = i
            end if
        end do

        allocate(positions(count))
        positions = temp_pos(1:count)

    end function naive_search

    !===============================================
    ! Knuth-Morris-Pratt (KMP) Algorithm
    !===============================================

    function kmp_search(text, pattern) result(positions)
        implicit none
        character(len=*), intent(in) :: text, pattern
        integer(int32), dimension(:), allocatable :: positions
        integer(int32), dimension(:), allocatable :: lps, temp_pos
        integer(int32) :: n, m, i, j, count

        n = len_trim(text)
        m = len_trim(pattern)

        if (m > n) then
            allocate(positions(0))
            return
        end if

        ! Build LPS array
        allocate(lps(m))
        call build_lps_array(pattern, lps)

        allocate(temp_pos(n))
        count = 0
        i = 1
        j = 1

        do while (i <= n)
            if (text(i:i) == pattern(j:j)) then
                i = i + 1
                j = j + 1
            end if

            if (j > m) then
                count = count + 1
                temp_pos(count) = i - j + 1
                j = lps(j-1) + 1
            else if (i <= n .and. text(i:i) /= pattern(j:j)) then
                if (j > 1) then
                    j = lps(j-1) + 1
                else
                    i = i + 1
                end if
            end if
        end do

        allocate(positions(count))
        positions = temp_pos(1:count)
        deallocate(lps)

    end function kmp_search

    subroutine build_lps_array(pattern, lps)
        implicit none
        character(len=*), intent(in) :: pattern
        integer(int32), dimension(:), intent(out) :: lps
        integer(int32) :: m, len, i

        m = len_trim(pattern)
        lps(1) = 0
        len = 0
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

    end subroutine build_lps_array

    !===============================================
    ! Rabin-Karp Algorithm
    !===============================================

    function rabin_karp_search(text, pattern) result(positions)
        implicit none
        character(len=*), intent(in) :: text, pattern
        integer(int32), dimension(:), allocatable :: positions
        integer(int32) :: n, m, i, j, count
        integer(int64) :: pattern_hash, text_hash, h
        integer(int32), dimension(:), allocatable :: temp_pos

        n = len_trim(text)
        m = len_trim(pattern)

        if (m > n) then
            allocate(positions(0))
            return
        end if

        allocate(temp_pos(n))
        count = 0

        ! Calculate hash multiplier
        h = 1_int64
        do i = 1, m - 1
            h = mod(h * BASE, PRIME)
        end do

        ! Calculate initial hashes
        pattern_hash = 0_int64
        text_hash = 0_int64
        do i = 1, m
            pattern_hash = mod(pattern_hash * BASE + iachar(pattern(i:i)), PRIME)
            text_hash = mod(text_hash * BASE + iachar(text(i:i)), PRIME)
        end do

        ! Sliding window
        do i = 1, n - m + 1
            if (pattern_hash == text_hash) then
                ! Check character by character
                j = 1
                do while (j <= m .and. text(i+j-1:i+j-1) == pattern(j:j))
                    j = j + 1
                end do

                if (j > m) then
                    count = count + 1
                    temp_pos(count) = i
                end if
            end if

            if (i < n - m + 1) then
                ! Roll the hash
                text_hash = mod(BASE * (text_hash - iachar(text(i:i)) * h) + &
                              iachar(text(i+m:i+m)), PRIME)
                if (text_hash < 0) text_hash = text_hash + PRIME
            end if
        end do

        allocate(positions(count))
        positions = temp_pos(1:count)

    end function rabin_karp_search

    !===============================================
    ! Boyer-Moore Algorithm
    !===============================================

    function boyer_moore_search(text, pattern) result(positions)
        implicit none
        character(len=*), intent(in) :: text, pattern
        integer(int32), dimension(:), allocatable :: positions
        integer(int32), dimension(0:255) :: bad_char
        integer(int32), dimension(:), allocatable :: temp_pos
        integer(int32) :: n, m, i, j, count, shift

        n = len_trim(text)
        m = len_trim(pattern)

        if (m > n) then
            allocate(positions(0))
            return
        end if

        allocate(temp_pos(n))
        count = 0

        ! Build bad character table
        bad_char = m
        do i = 1, m - 1
            bad_char(iachar(pattern(i:i))) = m - i
        end do

        ! Search
        i = m
        do while (i <= n)
            j = m
            do while (j > 0 .and. text(i-m+j:i-m+j) == pattern(j:j))
                j = j - 1
            end do

            if (j == 0) then
                count = count + 1
                temp_pos(count) = i - m + 1
                i = i + m
            else
                shift = bad_char(iachar(text(i-m+j:i-m+j)))
                i = i + max(1, shift - (m - j))
            end if
        end do

        allocate(positions(count))
        positions = temp_pos(1:count)

    end function boyer_moore_search

    !===============================================
    ! Z-Algorithm
    !===============================================

    function z_algorithm(str) result(z_array)
        implicit none
        character(len=*), intent(in) :: str
        integer(int32), dimension(:), allocatable :: z_array
        integer(int32) :: n, left, right, i, k

        n = len_trim(str)
        allocate(z_array(n))

        z_array(1) = n
        left = 0
        right = 0

        do i = 2, n
            if (i > right) then
                left = i
                right = i
                do while (right <= n .and. &
                        str(right-left+1:right-left+1) == str(right:right))
                    right = right + 1
                end do
                z_array(i) = right - left
                right = right - 1
            else
                k = i - left + 1
                if (z_array(k) < right - i + 1) then
                    z_array(i) = z_array(k)
                else
                    left = i
                    do while (right <= n .and. &
                            str(right-left+1:right-left+1) == str(right:right))
                        right = right + 1
                    end do
                    z_array(i) = right - left
                    right = right - 1
                end if
            end if
        end do

    end function z_algorithm

    !===============================================
    ! Manacher's Algorithm (Longest Palindrome)
    !===============================================

    function manacher_algorithm(str) result(longest_pal)
        implicit none
        character(len=*), intent(in) :: str
        character(len=:), allocatable :: longest_pal
        character(len=:), allocatable :: processed
        integer(int32), dimension(:), allocatable :: p
        integer(int32) :: n, i, center, right, mirror
        integer(int32) :: max_len, max_center

        n = len_trim(str)

        ! Process string: add boundaries
        allocate(character(len=2*n+3) :: processed)
        processed(1:1) = '^'
        do i = 1, n
            processed(2*i:2*i) = '#'
            processed(2*i+1:2*i+1) = str(i:i)
        end do
        processed(2*n+2:2*n+2) = '#'
        processed(2*n+3:2*n+3) = '$'

        allocate(p(2*n+3))
        p = 0
        center = 0
        right = 0

        do i = 2, 2*n+2
            mirror = 2*center - i

            if (i < right) then
                p(i) = min(right - i, p(mirror))
            end if

            ! Try to expand palindrome
            do while (i+p(i)+1 <= 2*n+3 .and. i-p(i)-1 >= 1 .and. &
                    processed(i+p(i)+1:i+p(i)+1) == processed(i-p(i)-1:i-p(i)-1))
                p(i) = p(i) + 1
            end do

            if (i + p(i) > right) then
                center = i
                right = i + p(i)
            end if
        end do

        ! Find longest palindrome
        max_len = 0
        max_center = 0
        do i = 2, 2*n+2
            if (p(i) > max_len) then
                max_len = p(i)
                max_center = i
            end if
        end do

        ! Extract palindrome
        allocate(character(len=max_len) :: longest_pal)
        longest_pal = str((max_center-max_len)/2:(max_center+max_len)/2-1)

    end function manacher_algorithm

    !===============================================
    ! Longest Palindromic Substring
    !===============================================

    function longest_palindrome(str) result(palindrome)
        implicit none
        character(len=*), intent(in) :: str
        character(len=:), allocatable :: palindrome
        integer(int32) :: n, i, j, max_len, start

        n = len_trim(str)
        max_len = 0
        start = 1

        ! Check all possible centers
        do i = 1, n
            ! Odd length palindromes
            j = 0
            do while (i-j >= 1 .and. i+j <= n .and. &
                    str(i-j:i-j) == str(i+j:i+j))
                if (2*j + 1 > max_len) then
                    max_len = 2*j + 1
                    start = i - j
                end if
                j = j + 1
            end do

            ! Even length palindromes
            j = 0
            do while (i-j >= 1 .and. i+j+1 <= n .and. &
                    str(i-j:i-j) == str(i+j+1:i+j+1))
                if (2*j + 2 > max_len) then
                    max_len = 2*j + 2
                    start = i - j
                end if
                j = j + 1
            end do
        end do

        allocate(character(len=max_len) :: palindrome)
        palindrome = str(start:start+max_len-1)

    end function longest_palindrome

    !===============================================
    ! All Palindromic Substrings
    !===============================================

    function all_palindromes(str) result(palindromes)
        implicit none
        character(len=*), intent(in) :: str
        character(len=:), dimension(:), allocatable :: palindromes
        character(len=len(str)), dimension(:), allocatable :: temp_pals
        integer(int32) :: n, i, j, count
        logical, dimension(:,:), allocatable :: is_pal

        n = len_trim(str)
        allocate(is_pal(n, n))
        allocate(temp_pals(n*n))

        is_pal = .false.
        count = 0

        ! Single characters
        do i = 1, n
            is_pal(i, i) = .true.
            count = count + 1
            temp_pals(count) = str(i:i)
        end do

        ! Two characters
        do i = 1, n-1
            if (str(i:i) == str(i+1:i+1)) then
                is_pal(i, i+1) = .true.
                count = count + 1
                temp_pals(count) = str(i:i+1)
            end if
        end do

        ! Longer palindromes
        do j = 3, n
            do i = 1, n-j+1
                if (str(i:i) == str(i+j-1:i+j-1) .and. is_pal(i+1, i+j-2)) then
                    is_pal(i, i+j-1) = .true.
                    count = count + 1
                    temp_pals(count) = str(i:i+j-1)
                end if
            end do
        end do

        allocate(character(len=n) :: palindromes(count))
        do i = 1, count
            palindromes(i) = trim(temp_pals(i))
        end do

    end function all_palindromes

    !===============================================
    ! Suffix Array Construction
    !===============================================

    function suffix_array(str) result(sa)
        implicit none
        character(len=*), intent(in) :: str
        integer(int32), dimension(:), allocatable :: sa
        integer(int32) :: n, i
        type :: suffix_type
            integer(int32) :: index
            character(len=:), allocatable :: suffix
        end type suffix_type
        type(suffix_type), dimension(:), allocatable :: suffixes

        n = len_trim(str)
        allocate(sa(n))
        allocate(suffixes(n))

        ! Create all suffixes
        do i = 1, n
            suffixes(i)%index = i
            allocate(character(len=n-i+1) :: suffixes(i)%suffix)
            suffixes(i)%suffix = str(i:n)
        end do

        ! Sort suffixes
        call sort_suffixes(suffixes)

        ! Extract suffix array
        do i = 1, n
            sa(i) = suffixes(i)%index
        end do

        ! Clean up
        do i = 1, n
            deallocate(suffixes(i)%suffix)
        end do

    end function suffix_array

    subroutine sort_suffixes(suffixes)
        implicit none
        type :: suffix_type
            integer(int32) :: index
            character(len=:), allocatable :: suffix
        end type suffix_type
        type(suffix_type), dimension(:), intent(inout) :: suffixes
        type(suffix_type) :: temp
        integer(int32) :: i, j, n

        n = size(suffixes)

        ! Simple bubble sort for suffixes
        do i = 1, n-1
            do j = 1, n-i
                if (suffixes(j)%suffix > suffixes(j+1)%suffix) then
                    temp = suffixes(j)
                    suffixes(j) = suffixes(j+1)
                    suffixes(j+1) = temp
                end if
            end do
        end do

    end subroutine sort_suffixes

    !===============================================
    ! LCP Array Construction
    !===============================================

    function lcp_array(str, sa) result(lcp)
        implicit none
        character(len=*), intent(in) :: str
        integer(int32), dimension(:), intent(in) :: sa
        integer(int32), dimension(:), allocatable :: lcp
        integer(int32), dimension(:), allocatable :: rank
        integer(int32) :: n, i, j, k, h

        n = len_trim(str)
        allocate(lcp(n))
        allocate(rank(n))

        ! Build rank array
        do i = 1, n
            rank(sa(i)) = i
        end do

        h = 0
        lcp = 0

        do i = 1, n
            if (rank(i) > 1) then
                j = sa(rank(i) - 1)
                do while (i + h <= n .and. j + h <= n .and. &
                        str(i+h:i+h) == str(j+h:j+h))
                    h = h + 1
                end do
                lcp(rank(i)) = h
                if (h > 0) h = h - 1
            end if
        end do

    end function lcp_array

    !===============================================
    ! String Hashing
    !===============================================

    function string_hash(str) result(hash_value)
        implicit none
        character(len=*), intent(in) :: str
        integer(int64) :: hash_value
        integer(int32) :: i, n

        n = len_trim(str)
        hash_value = 0_int64

        do i = 1, n
            hash_value = mod(hash_value * BASE + iachar(str(i:i)), PRIME)
        end do

    end function string_hash

    !===============================================
    ! Edit Distance Functions
    !===============================================

    function levenshtein_distance(str1, str2) result(distance)
        implicit none
        character(len=*), intent(in) :: str1, str2
        integer(int32) :: distance
        integer(int32), dimension(:,:), allocatable :: dp
        integer(int32) :: m, n, i, j, cost

        m = len_trim(str1)
        n = len_trim(str2)
        allocate(dp(0:m, 0:n))

        do i = 0, m
            dp(i, 0) = i
        end do
        do j = 0, n
            dp(0, j) = j
        end do

        do i = 1, m
            do j = 1, n
                if (str1(i:i) == str2(j:j)) then
                    cost = 0
                else
                    cost = 1
                end if

                dp(i, j) = min(dp(i-1, j) + 1,     &  ! deletion
                              dp(i, j-1) + 1,       &  ! insertion
                              dp(i-1, j-1) + cost)     ! substitution
            end do
        end do

        distance = dp(m, n)

    end function levenshtein_distance

    function hamming_distance(str1, str2) result(distance)
        implicit none
        character(len=*), intent(in) :: str1, str2
        integer(int32) :: distance
        integer(int32) :: i, n

        n = min(len_trim(str1), len_trim(str2))
        distance = 0

        do i = 1, n
            if (str1(i:i) /= str2(i:i)) then
                distance = distance + 1
            end if
        end do

        distance = distance + abs(len_trim(str1) - len_trim(str2))

    end function hamming_distance

    !===============================================
    ! Common String Operations
    !===============================================

    function longest_common_prefix(strings) result(prefix)
        implicit none
        character(len=*), dimension(:), intent(in) :: strings
        character(len=:), allocatable :: prefix
        integer(int32) :: n, min_len, i, j

        n = size(strings)
        if (n == 0) then
            allocate(character(len=0) :: prefix)
            return
        end if

        min_len = len_trim(strings(1))
        do i = 2, n
            min_len = min(min_len, len_trim(strings(i)))
        end do

        do i = 1, min_len
            do j = 2, n
                if (strings(1)(i:i) /= strings(j)(i:i)) then
                    allocate(character(len=i-1) :: prefix)
                    prefix = strings(1)(1:i-1)
                    return
                end if
            end do
        end do

        allocate(character(len=min_len) :: prefix)
        prefix = strings(1)(1:min_len)

    end function longest_common_prefix

    function longest_repeated_substring(str) result(substring)
        implicit none
        character(len=*), intent(in) :: str
        character(len=:), allocatable :: substring
        integer(int32) :: n, i, j, k, max_len

        n = len_trim(str)
        max_len = 0
        allocate(character(len=0) :: substring)

        do i = 1, n
            do j = i+1, n
                k = 0
                do while (i+k <= n .and. j+k <= n .and. &
                        str(i+k:i+k) == str(j+k:j+k))
                    k = k + 1
                end do

                if (k > max_len) then
                    max_len = k
                    deallocate(substring)
                    allocate(character(len=max_len) :: substring)
                    substring = str(i:i+k-1)
                end if
            end do
        end do

    end function longest_repeated_substring

    !===============================================
    ! String Predicates
    !===============================================

    function is_anagram(str1, str2) result(anagram)
        implicit none
        character(len=*), intent(in) :: str1, str2
        logical :: anagram
        integer(int32), dimension(0:255) :: count1, count2
        integer(int32) :: i, n1, n2

        n1 = len_trim(str1)
        n2 = len_trim(str2)

        if (n1 /= n2) then
            anagram = .false.
            return
        end if

        count1 = 0
        count2 = 0

        do i = 1, n1
            count1(iachar(str1(i:i))) = count1(iachar(str1(i:i))) + 1
            count2(iachar(str2(i:i))) = count2(iachar(str2(i:i))) + 1
        end do

        anagram = all(count1 == count2)

    end function is_anagram

    function is_palindrome(str) result(palindrome)
        implicit none
        character(len=*), intent(in) :: str
        logical :: palindrome
        integer(int32) :: i, j, n

        n = len_trim(str)
        i = 1
        j = n

        palindrome = .true.
        do while (i < j)
            if (str(i:i) /= str(j:j)) then
                palindrome = .false.
                return
            end if
            i = i + 1
            j = j - 1
        end do

    end function is_palindrome

    function is_rotation(str1, str2) result(rotation)
        implicit none
        character(len=*), intent(in) :: str1, str2
        logical :: rotation
        character(len=:), allocatable :: doubled

        if (len_trim(str1) /= len_trim(str2)) then
            rotation = .false.
            return
        end if

        allocate(character(len=2*len_trim(str1)) :: doubled)
        doubled = trim(str1) // trim(str1)

        rotation = index(doubled, trim(str2)) > 0

    end function is_rotation

    !===============================================
    ! String Compression
    !===============================================

    function compress_string(str) result(compressed)
        implicit none
        character(len=*), intent(in) :: str
        character(len=:), allocatable :: compressed
        character(len=100) :: temp
        integer(int32) :: i, n, count, pos
        character :: current

        n = len_trim(str)
        if (n == 0) then
            allocate(character(len=0) :: compressed)
            return
        end if

        temp = ''
        pos = 1
        current = str(1:1)
        count = 1

        do i = 2, n
            if (str(i:i) == current) then
                count = count + 1
            else
                write(temp(pos:pos), '(A)') current
                pos = pos + 1
                write(temp(pos:pos+9), '(I0)') count
                pos = pos + len_trim(temp(pos:pos+9))
                current = str(i:i)
                count = 1
            end if
        end do

        write(temp(pos:pos), '(A)') current
        pos = pos + 1
        write(temp(pos:pos+9), '(I0)') count
        pos = pos + len_trim(temp(pos:pos+9)) - 1

        allocate(character(len=pos) :: compressed)
        compressed = temp(1:pos)

    end function compress_string

    function decompress_string(compressed) result(str)
        implicit none
        character(len=*), intent(in) :: compressed
        character(len=:), allocatable :: str
        character(len=1000) :: temp
        integer(int32) :: i, n, count, pos, num_start
        character :: current

        n = len_trim(compressed)
        temp = ''
        pos = 1
        i = 1

        do while (i <= n)
            current = compressed(i:i)
            i = i + 1

            ! Read number
            num_start = i
            do while (i <= n .and. iachar(compressed(i:i)) >= iachar('0') .and. &
                    iachar(compressed(i:i)) <= iachar('9'))
                i = i + 1
            end do

            read(compressed(num_start:i-1), *) count

            ! Add characters to result
            do j = 1, count
                temp(pos:pos) = current
                pos = pos + 1
            end do
        end do

        allocate(character(len=pos-1) :: str)
        str = temp(1:pos-1)

    end function decompress_string

    !===============================================
    ! Run Length Encoding
    !===============================================

    function run_length_encoding(str) result(encoded)
        implicit none
        character(len=*), intent(in) :: str
        character(len=:), allocatable :: encoded
        character(len=100) :: temp
        integer(int32) :: i, n, count, pos
        character :: current

        n = len_trim(str)
        if (n == 0) then
            allocate(character(len=0) :: encoded)
            return
        end if

        temp = ''
        pos = 1
        current = str(1:1)
        count = 1

        do i = 2, n
            if (str(i:i) == current) then
                count = count + 1
            else
                if (count > 1) then
                    write(temp(pos:pos+9), '(I0)') count
                    pos = pos + len_trim(temp(pos:pos+9))
                end if
                temp(pos:pos) = current
                pos = pos + 1
                current = str(i:i)
                count = 1
            end if
        end do

        if (count > 1) then
            write(temp(pos:pos+9), '(I0)') count
            pos = pos + len_trim(temp(pos:pos+9))
        end if
        temp(pos:pos) = current

        allocate(character(len=pos) :: encoded)
        encoded = temp(1:pos)

    end function run_length_encoding

    function run_length_decoding(encoded) result(str)
        implicit none
        character(len=*), intent(in) :: encoded
        character(len=:), allocatable :: str
        character(len=1000) :: temp
        integer(int32) :: i, n, count, pos, j
        character :: current
        character(len=10) :: num_str

        n = len_trim(encoded)
        temp = ''
        pos = 1
        i = 1

        do while (i <= n)
            count = 0
            num_str = ''
            j = 1

            ! Read number if present
            do while (i <= n .and. iachar(encoded(i:i)) >= iachar('0') .and. &
                    iachar(encoded(i:i)) <= iachar('9'))
                num_str(j:j) = encoded(i:i)
                i = i + 1
                j = j + 1
            end do

            if (j > 1) then
                read(num_str(1:j-1), *) count
            else
                count = 1
            end if

            ! Read character
            if (i <= n) then
                current = encoded(i:i)
                i = i + 1

                ! Add to result
                do j = 1, count
                    temp(pos:pos) = current
                    pos = pos + 1
                end do
            end if
        end do

        allocate(character(len=pos-1) :: str)
        str = temp(1:pos-1)

    end function run_length_decoding

    !===============================================
    ! Burrows-Wheeler Transform
    !===============================================

    function burrows_wheeler_transform(str) result(bwt)
        implicit none
        character(len=*), intent(in) :: str
        character(len=:), allocatable :: bwt
        character(len=len(str)), dimension(:), allocatable :: rotations
        integer(int32) :: n, i
        integer(int32), dimension(:), allocatable :: indices

        n = len_trim(str)
        allocate(rotations(n))
        allocate(indices(n))
        allocate(character(len=n) :: bwt)

        ! Generate all rotations
        do i = 1, n
            rotations(i) = str(i:n) // str(1:i-1)
            indices(i) = i
        end do

        ! Sort rotations
        call sort_rotations_with_indices(rotations, indices)

        ! Extract last column
        do i = 1, n
            bwt(i:i) = rotations(i)(n:n)
        end do

    end function burrows_wheeler_transform

    subroutine sort_rotations_with_indices(rotations, indices)
        implicit none
        character(len=*), dimension(:), intent(inout) :: rotations
        integer(int32), dimension(:), intent(inout) :: indices
        character(len=len(rotations)) :: temp_rot
        integer(int32) :: i, j, n, temp_idx

        n = size(rotations)

        ! Simple bubble sort
        do i = 1, n-1
            do j = 1, n-i
                if (rotations(j) > rotations(j+1)) then
                    temp_rot = rotations(j)
                    rotations(j) = rotations(j+1)
                    rotations(j+1) = temp_rot

                    temp_idx = indices(j)
                    indices(j) = indices(j+1)
                    indices(j+1) = temp_idx
                end if
            end do
        end do

    end subroutine sort_rotations_with_indices

    function inverse_bwt(bwt, original_index) result(original)
        implicit none
        character(len=*), intent(in) :: bwt
        integer(int32), intent(in) :: original_index
        character(len=:), allocatable :: original
        character(len=len(bwt)), dimension(:), allocatable :: table
        integer(int32) :: n, i, j

        n = len_trim(bwt)
        allocate(table(n))
        allocate(character(len=n) :: original)

        ! Initialize table
        do i = 1, n
            table(i) = ''
        end do

        ! Build transformation table
        do i = 1, n
            do j = 1, n
                table(j) = bwt(j:j) // table(j)
            end do
            call sort_strings(table)
        end do

        original = table(original_index)

    end function inverse_bwt

    subroutine sort_strings(strings)
        implicit none
        character(len=*), dimension(:), intent(inout) :: strings
        character(len=len(strings)) :: temp
        integer(int32) :: i, j, n

        n = size(strings)

        do i = 1, n-1
            do j = 1, n-i
                if (strings(j) > strings(j+1)) then
                    temp = strings(j)
                    strings(j) = strings(j+1)
                    strings(j+1) = temp
                end if
            end do
        end do

    end subroutine sort_strings

    !===============================================
    ! KMP Preprocessing
    !===============================================

    function knuth_morris_pratt(text, pattern) result(positions)
        implicit none
        character(len=*), intent(in) :: text, pattern
        integer(int32), dimension(:), allocatable :: positions

        positions = kmp_search(text, pattern)

    end function knuth_morris_pratt

    !===============================================
    ! Finite Automaton for String Matching
    !===============================================

    function string_matching_automaton(text, pattern) result(positions)
        implicit none
        character(len=*), intent(in) :: text, pattern
        integer(int32), dimension(:), allocatable :: positions
        integer(int32), dimension(:,:), allocatable :: trans_table
        integer(int32) :: n, m, i, state, count
        integer(int32), dimension(:), allocatable :: temp_pos

        n = len_trim(text)
        m = len_trim(pattern)

        if (m > n) then
            allocate(positions(0))
            return
        end if

        allocate(trans_table(0:m, 0:255))
        allocate(temp_pos(n))

        ! Build transition table
        call build_transition_table(pattern, trans_table)

        count = 0
        state = 0

        do i = 1, n
            state = trans_table(state, iachar(text(i:i)))
            if (state == m) then
                count = count + 1
                temp_pos(count) = i - m + 1
            end if
        end do

        allocate(positions(count))
        positions = temp_pos(1:count)

    end function string_matching_automaton

    subroutine build_transition_table(pattern, trans_table)
        implicit none
        character(len=*), intent(in) :: pattern
        integer(int32), dimension(0:, 0:), intent(out) :: trans_table
        integer(int32) :: m, state, x, next_state

        m = len_trim(pattern)
        trans_table = 0

        do state = 0, m
            do x = 0, 255
                next_state = min(m, state + 1)

                do while (next_state > 0)
                    if (next_state == 0) exit

                    if (state >= next_state - 1) then
                        if (pattern(next_state:next_state) == achar(x)) then
                            if (next_state == 1) then
                                trans_table(state, x) = next_state
                                exit
                            else if (pattern(1:next_state-1) == &
                                   pattern(state-next_state+2:state)) then
                                trans_table(state, x) = next_state
                                exit
                            end if
                        end if
                    end if
                    next_state = next_state - 1
                end do
            end do
        end do

    end subroutine build_transition_table

    !===============================================
    ! Aho-Corasick Algorithm (Multiple Pattern Search)
    !===============================================

    function aho_corasick_search(text, patterns) result(matches)
        implicit none
        character(len=*), intent(in) :: text
        character(len=*), dimension(:), intent(in) :: patterns
        type :: match_type
            integer(int32) :: position
            integer(int32) :: pattern_index
        end type match_type
        type(match_type), dimension(:), allocatable :: matches
        type(trie_node), pointer :: root, current
        integer(int32) :: i, j, n, count
        type(match_type), dimension(:), allocatable :: temp_matches

        n = len_trim(text)
        allocate(temp_matches(n * size(patterns)))

        ! Build trie
        allocate(root)
        call root%init()
        do i = 1, size(patterns)
            call insert_pattern(root, patterns(i), i)
        end do

        ! Build failure links
        call build_failure_links(root)

        ! Search
        count = 0
        current => root

        do i = 1, n
            do while (associated(current) .and. current /= root .and. &
                    .not. associated(current%children(iachar(text(i:i)))))
                current => current%failure_link
            end do

            if (associated(current%children(iachar(text(i:i))))) then
                current => current%children(iachar(text(i:i)))
            end if

            if (allocated(current%output)) then
                do j = 1, size(current%output)
                    count = count + 1
                    temp_matches(count)%position = i - len_trim(patterns(current%output(j))) + 1
                    temp_matches(count)%pattern_index = current%output(j)
                end do
            end if
        end do

        allocate(matches(count))
        matches = temp_matches(1:count)

    end function aho_corasick_search

    subroutine insert_pattern(root, pattern, index)
        implicit none
        type(trie_node), pointer, intent(inout) :: root
        character(len=*), intent(in) :: pattern
        integer(int32), intent(in) :: index
        type(trie_node), pointer :: current
        integer(int32) :: i, ch

        current => root

        do i = 1, len_trim(pattern)
            ch = iachar(pattern(i:i))
            if (.not. associated(current%children(ch))) then
                allocate(current%children(ch))
                call current%children(ch)%init()
            end if
            current => current%children(ch)
        end do

        current%is_end = .true.
        if (.not. allocated(current%output)) then
            allocate(current%output(1))
            current%output(1) = index
        else
            current%output = [current%output, index]
        end if

    end subroutine insert_pattern

    subroutine build_failure_links(root)
        implicit none
        type(trie_node), pointer, intent(inout) :: root
        type(trie_node), pointer :: current, child, fail
        type(trie_node), pointer, dimension(:), allocatable :: queue
        integer(int32) :: front, rear, i

        allocate(queue(1000))
        front = 1
        rear = 0

        ! Initialize failure links for root's children
        do i = 0, 255
            if (associated(root%children(i))) then
                root%children(i)%failure_link => root
                rear = rear + 1
                queue(rear) => root%children(i)
            end if
        end do

        ! BFS to build failure links
        do while (front <= rear)
            current => queue(front)
            front = front + 1

            do i = 0, 255
                if (associated(current%children(i))) then
                    child => current%children(i)
                    rear = rear + 1
                    queue(rear) => child

                    fail => current%failure_link
                    do while (associated(fail) .and. fail /= root .and. &
                            .not. associated(fail%children(i)))
                        fail => fail%failure_link
                    end do

                    if (associated(fail%children(i)) .and. fail%children(i) /= child) then
                        child%failure_link => fail%children(i)
                    else
                        child%failure_link => root
                    end if

                    ! Merge output
                    if (associated(child%failure_link) .and. &
                        allocated(child%failure_link%output)) then
                        if (allocated(child%output)) then
                            child%output = [child%output, child%failure_link%output]
                        else
                            child%output = child%failure_link%output
                        end if
                    end if
                end if
            end do
        end do

    end subroutine build_failure_links

    !===============================================
    ! Helper Subroutines for Types
    !===============================================

    subroutine suffix_node_init(this)
        implicit none
        class(suffix_node), intent(inout) :: this

        this%start = 0
        this%end_ptr => null()
        this%suffix_link = -1
        allocate(this%children(256))
        this%children => null()
        this%suffix_index = -1

    end subroutine suffix_node_init

    subroutine trie_node_init(this)
        implicit none
        class(trie_node), intent(inout) :: this

        allocate(this%children(0:255))
        this%children => null()
        this%failure_link => null()
        this%is_end = .false.

    end subroutine trie_node_init

end module string_module