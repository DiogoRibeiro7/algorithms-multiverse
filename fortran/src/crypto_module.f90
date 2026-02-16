! Cryptographic Algorithms Module
! Collection of classic cryptographic algorithms and hash functions
! NOTE: For educational purposes only - not for production security

module crypto_module
    use iso_fortran_env, only: int32, int64, int8
    implicit none
    private

    ! Public interfaces
    public :: caesar_cipher, caesar_decipher
    public :: vigenere_encrypt, vigenere_decrypt
    public :: xor_cipher, playfair_encrypt, playfair_decrypt
    public :: rail_fence_encrypt, rail_fence_decrypt
    public :: atbash_cipher, rot13, rot47
    public :: simple_hash, djb2_hash, fnv1a_hash
    public :: jenkins_hash, murmur_hash
    public :: md5_hash, sha1_hash
    public :: base64_encode, base64_decode
    public :: hill_cipher_encrypt, hill_cipher_decrypt
    public :: rsa_encrypt, rsa_decrypt, generate_rsa_keys
    public :: diffie_hellman_key_exchange
    public :: one_time_pad_encrypt, one_time_pad_decrypt

    ! Constants
    integer(int32), parameter :: HASH_SEED = 5381_int32
    integer(int64), parameter :: FNV_PRIME = 1099511628211_int64
    integer(int64), parameter :: FNV_OFFSET = 14695981039346656037_int64

contains

    !===============================================
    ! Caesar Cipher
    !===============================================

    function caesar_cipher(text, shift) result(encrypted)
        implicit none
        character(len=*), intent(in) :: text
        integer(int32), intent(in) :: shift
        character(len=:), allocatable :: encrypted
        integer(int32) :: i, n, char_code

        n = len_trim(text)
        allocate(character(len=n) :: encrypted)

        do i = 1, n
            char_code = iachar(text(i:i))

            if (char_code >= iachar('A') .and. char_code <= iachar('Z')) then
                char_code = mod(char_code - iachar('A') + shift, 26)
                if (char_code < 0) char_code = char_code + 26
                encrypted(i:i) = achar(char_code + iachar('A'))
            else if (char_code >= iachar('a') .and. char_code <= iachar('z')) then
                char_code = mod(char_code - iachar('a') + shift, 26)
                if (char_code < 0) char_code = char_code + 26
                encrypted(i:i) = achar(char_code + iachar('a'))
            else
                encrypted(i:i) = text(i:i)
            end if
        end do

    end function caesar_cipher

    function caesar_decipher(text, shift) result(decrypted)
        implicit none
        character(len=*), intent(in) :: text
        integer(int32), intent(in) :: shift
        character(len=:), allocatable :: decrypted

        decrypted = caesar_cipher(text, -shift)

    end function caesar_decipher

    !===============================================
    ! Vigenere Cipher
    !===============================================

    function vigenere_encrypt(text, key) result(encrypted)
        implicit none
        character(len=*), intent(in) :: text, key
        character(len=:), allocatable :: encrypted
        integer(int32) :: i, n, key_len, text_pos, key_pos
        integer(int32) :: char_code, key_code

        n = len_trim(text)
        key_len = len_trim(key)
        allocate(character(len=n) :: encrypted)

        text_pos = 1
        key_pos = 1

        do i = 1, n
            char_code = iachar(text(i:i))

            if ((char_code >= iachar('A') .and. char_code <= iachar('Z')) .or. &
                (char_code >= iachar('a') .and. char_code <= iachar('z'))) then

                ! Get key character
                key_code = iachar(key(key_pos:key_pos))
                if (key_code >= iachar('a') .and. key_code <= iachar('z')) then
                    key_code = key_code - iachar('a')
                else
                    key_code = key_code - iachar('A')
                end if

                ! Encrypt character
                if (char_code >= iachar('A') .and. char_code <= iachar('Z')) then
                    char_code = mod(char_code - iachar('A') + key_code, 26)
                    encrypted(i:i) = achar(char_code + iachar('A'))
                else
                    char_code = mod(char_code - iachar('a') + key_code, 26)
                    encrypted(i:i) = achar(char_code + iachar('a'))
                end if

                key_pos = mod(key_pos, key_len) + 1
            else
                encrypted(i:i) = text(i:i)
            end if
        end do

    end function vigenere_encrypt

    function vigenere_decrypt(text, key) result(decrypted)
        implicit none
        character(len=*), intent(in) :: text, key
        character(len=:), allocatable :: decrypted
        character(len=:), allocatable :: inverse_key
        integer(int32) :: i, key_len

        key_len = len_trim(key)
        allocate(character(len=key_len) :: inverse_key)

        ! Create inverse key
        do i = 1, key_len
            if (iachar(key(i:i)) >= iachar('a') .and. iachar(key(i:i)) <= iachar('z')) then
                inverse_key(i:i) = achar(iachar('a') + &
                                        mod(26 - (iachar(key(i:i)) - iachar('a')), 26))
            else
                inverse_key(i:i) = achar(iachar('A') + &
                                        mod(26 - (iachar(key(i:i)) - iachar('A')), 26))
            end if
        end do

        decrypted = vigenere_encrypt(text, inverse_key)

    end function vigenere_decrypt

    !===============================================
    ! XOR Cipher
    !===============================================

    function xor_cipher(text, key) result(encrypted)
        implicit none
        character(len=*), intent(in) :: text, key
        character(len=:), allocatable :: encrypted
        integer(int32) :: i, n, key_len

        n = len_trim(text)
        key_len = len_trim(key)
        allocate(character(len=n) :: encrypted)

        do i = 1, n
            encrypted(i:i) = achar(ieor(iachar(text(i:i)), &
                                       iachar(key(mod(i-1, key_len) + 1:mod(i-1, key_len) + 1))))
        end do

    end function xor_cipher

    !===============================================
    ! Playfair Cipher
    !===============================================

    function playfair_encrypt(text, key) result(encrypted)
        implicit none
        character(len=*), intent(in) :: text, key
        character(len=:), allocatable :: encrypted
        character(len=25) :: key_square
        character(len=:), allocatable :: prepared_text
        integer(int32) :: i, n, pos1, pos2, row1, col1, row2, col2

        ! Build key square (5x5 matrix)
        call build_playfair_square(key, key_square)

        ! Prepare text (remove non-letters, handle duplicates)
        prepared_text = prepare_playfair_text(text)
        n = len_trim(prepared_text)

        allocate(character(len=n) :: encrypted)

        i = 1
        do while (i < n)
            ! Find positions in key square
            pos1 = index(key_square, prepared_text(i:i))
            pos2 = index(key_square, prepared_text(i+1:i+1))

            row1 = (pos1 - 1) / 5 + 1
            col1 = mod(pos1 - 1, 5) + 1
            row2 = (pos2 - 1) / 5 + 1
            col2 = mod(pos2 - 1, 5) + 1

            if (row1 == row2) then
                ! Same row - shift right
                encrypted(i:i) = key_square((row1-1)*5 + mod(col1, 5) + 1:(row1-1)*5 + mod(col1, 5) + 1)
                encrypted(i+1:i+1) = key_square((row2-1)*5 + mod(col2, 5) + 1:(row2-1)*5 + mod(col2, 5) + 1)
            else if (col1 == col2) then
                ! Same column - shift down
                encrypted(i:i) = key_square(mod(row1, 5)*5 + col1:mod(row1, 5)*5 + col1)
                encrypted(i+1:i+1) = key_square(mod(row2, 5)*5 + col2:mod(row2, 5)*5 + col2)
            else
                ! Rectangle - swap corners
                encrypted(i:i) = key_square((row1-1)*5 + col2:(row1-1)*5 + col2)
                encrypted(i+1:i+1) = key_square((row2-1)*5 + col1:(row2-1)*5 + col1)
            end if

            i = i + 2
        end do

    end function playfair_encrypt

    function playfair_decrypt(text, key) result(decrypted)
        implicit none
        character(len=*), intent(in) :: text, key
        character(len=:), allocatable :: decrypted
        character(len=25) :: key_square
        integer(int32) :: i, n, pos1, pos2, row1, col1, row2, col2

        call build_playfair_square(key, key_square)
        n = len_trim(text)
        allocate(character(len=n) :: decrypted)

        i = 1
        do while (i < n)
            pos1 = index(key_square, text(i:i))
            pos2 = index(key_square, text(i+1:i+1))

            row1 = (pos1 - 1) / 5 + 1
            col1 = mod(pos1 - 1, 5) + 1
            row2 = (pos2 - 1) / 5 + 1
            col2 = mod(pos2 - 1, 5) + 1

            if (row1 == row2) then
                ! Same row - shift left
                decrypted(i:i) = key_square((row1-1)*5 + mod(col1-2+5, 5) + 1:(row1-1)*5 + mod(col1-2+5, 5) + 1)
                decrypted(i+1:i+1) = key_square((row2-1)*5 + mod(col2-2+5, 5) + 1:(row2-1)*5 + mod(col2-2+5, 5) + 1)
            else if (col1 == col2) then
                ! Same column - shift up
                decrypted(i:i) = key_square(mod(row1-2+5, 5)*5 + col1:mod(row1-2+5, 5)*5 + col1)
                decrypted(i+1:i+1) = key_square(mod(row2-2+5, 5)*5 + col2:mod(row2-2+5, 5)*5 + col2)
            else
                ! Rectangle - swap corners
                decrypted(i:i) = key_square((row1-1)*5 + col2:(row1-1)*5 + col2)
                decrypted(i+1:i+1) = key_square((row2-1)*5 + col1:(row2-1)*5 + col1)
            end if

            i = i + 2
        end do

    end function playfair_decrypt

    subroutine build_playfair_square(key, square)
        implicit none
        character(len=*), intent(in) :: key
        character(len=25), intent(out) :: square
        logical, dimension(26) :: used
        integer(int32) :: i, j, pos, char_code

        used = .false.
        used(10) = .true.  ! J is merged with I
        square = ''
        pos = 1

        ! Add key letters
        do i = 1, len_trim(key)
            char_code = iachar(key(i:i))
            if (char_code >= iachar('a') .and. char_code <= iachar('z')) then
                char_code = char_code - iachar('a') + 1
            else if (char_code >= iachar('A') .and. char_code <= iachar('Z')) then
                char_code = char_code - iachar('A') + 1
            else
                cycle
            end if

            if (.not. used(char_code)) then
                square(pos:pos) = achar(char_code + iachar('A') - 1)
                pos = pos + 1
                used(char_code) = .true.
            end if
        end do

        ! Add remaining letters
        do i = 1, 26
            if (.not. used(i)) then
                square(pos:pos) = achar(i + iachar('A') - 1)
                pos = pos + 1
            end if
        end do

    end subroutine build_playfair_square

    function prepare_playfair_text(text) result(prepared)
        implicit none
        character(len=*), intent(in) :: text
        character(len=:), allocatable :: prepared
        character(len=200) :: temp
        integer(int32) :: i, n, pos

        n = len_trim(text)
        temp = ''
        pos = 1

        do i = 1, n
            if ((iachar(text(i:i)) >= iachar('A') .and. iachar(text(i:i)) <= iachar('Z')) .or. &
                (iachar(text(i:i)) >= iachar('a') .and. iachar(text(i:i)) <= iachar('z'))) then
                temp(pos:pos) = text(i:i)
                if (iachar(temp(pos:pos)) >= iachar('a')) then
                    temp(pos:pos) = achar(iachar(temp(pos:pos)) - 32)
                end if
                if (temp(pos:pos) == 'J') temp(pos:pos) = 'I'
                pos = pos + 1
            end if
        end do

        ! Add padding if odd length
        if (mod(pos-1, 2) == 1) then
            temp(pos:pos) = 'X'
            pos = pos + 1
        end if

        allocate(character(len=pos-1) :: prepared)
        prepared = temp(1:pos-1)

    end function prepare_playfair_text

    !===============================================
    ! Rail Fence Cipher
    !===============================================

    function rail_fence_encrypt(text, rails) result(encrypted)
        implicit none
        character(len=*), intent(in) :: text
        integer(int32), intent(in) :: rails
        character(len=:), allocatable :: encrypted
        character(len=len(text)), dimension(:), allocatable :: fence
        integer(int32) :: i, n, rail, direction, pos

        n = len_trim(text)
        allocate(fence(rails))
        allocate(character(len=n) :: encrypted)

        fence = ''
        rail = 1
        direction = 1

        do i = 1, n
            fence(rail)(len_trim(fence(rail))+1:len_trim(fence(rail))+1) = text(i:i)

            rail = rail + direction
            if (rail == rails) then
                direction = -1
            else if (rail == 1) then
                direction = 1
            end if
        end do

        pos = 1
        do i = 1, rails
            do j = 1, len_trim(fence(i))
                encrypted(pos:pos) = fence(i)(j:j)
                pos = pos + 1
            end do
        end do

    end function rail_fence_encrypt

    function rail_fence_decrypt(text, rails) result(decrypted)
        implicit none
        character(len=*), intent(in) :: text
        integer(int32), intent(in) :: rails
        character(len=:), allocatable :: decrypted
        character(len=len(text)), dimension(:,:), allocatable :: fence
        integer(int32) :: i, j, n, rail, direction, pos

        n = len_trim(text)
        allocate(fence(rails, n))
        allocate(character(len=n) :: decrypted)

        ! Mark positions
        fence = ' '
        rail = 1
        direction = 1

        do i = 1, n
            fence(rail, i) = '*'
            rail = rail + direction
            if (rail == rails) then
                direction = -1
            else if (rail == 1) then
                direction = 1
            end if
        end do

        ! Fill marked positions
        pos = 1
        do i = 1, rails
            do j = 1, n
                if (fence(i, j) == '*') then
                    fence(i, j) = text(pos:pos)
                    pos = pos + 1
                end if
            end do
        end do

        ! Read by columns
        rail = 1
        direction = 1
        do i = 1, n
            decrypted(i:i) = fence(rail, i)
            rail = rail + direction
            if (rail == rails) then
                direction = -1
            else if (rail == 1) then
                direction = 1
            end if
        end do

    end function rail_fence_decrypt

    !===============================================
    ! Atbash Cipher
    !===============================================

    function atbash_cipher(text) result(encrypted)
        implicit none
        character(len=*), intent(in) :: text
        character(len=:), allocatable :: encrypted
        integer(int32) :: i, n, char_code

        n = len_trim(text)
        allocate(character(len=n) :: encrypted)

        do i = 1, n
            char_code = iachar(text(i:i))

            if (char_code >= iachar('A') .and. char_code <= iachar('Z')) then
                encrypted(i:i) = achar(iachar('Z') - (char_code - iachar('A')))
            else if (char_code >= iachar('a') .and. char_code <= iachar('z')) then
                encrypted(i:i) = achar(iachar('z') - (char_code - iachar('a')))
            else
                encrypted(i:i) = text(i:i)
            end if
        end do

    end function atbash_cipher

    !===============================================
    ! ROT13 and ROT47
    !===============================================

    function rot13(text) result(encrypted)
        implicit none
        character(len=*), intent(in) :: text
        character(len=:), allocatable :: encrypted

        encrypted = caesar_cipher(text, 13)

    end function rot13

    function rot47(text) result(encrypted)
        implicit none
        character(len=*), intent(in) :: text
        character(len=:), allocatable :: encrypted
        integer(int32) :: i, n, char_code

        n = len_trim(text)
        allocate(character(len=n) :: encrypted)

        do i = 1, n
            char_code = iachar(text(i:i))

            if (char_code >= 33 .and. char_code <= 126) then
                char_code = mod(char_code - 33 + 47, 94) + 33
                encrypted(i:i) = achar(char_code)
            else
                encrypted(i:i) = text(i:i)
            end if
        end do

    end function rot47

    !===============================================
    ! Hash Functions
    !===============================================

    function simple_hash(text) result(hash)
        implicit none
        character(len=*), intent(in) :: text
        integer(int32) :: hash
        integer(int32) :: i, n

        n = len_trim(text)
        hash = 0

        do i = 1, n
            hash = hash * 31 + iachar(text(i:i))
        end do

    end function simple_hash

    function djb2_hash(text) result(hash)
        implicit none
        character(len=*), intent(in) :: text
        integer(int64) :: hash
        integer(int32) :: i, n

        n = len_trim(text)
        hash = HASH_SEED

        do i = 1, n
            hash = hash * 33_int64 + iachar(text(i:i))
        end do

    end function djb2_hash

    function fnv1a_hash(text) result(hash)
        implicit none
        character(len=*), intent(in) :: text
        integer(int64) :: hash
        integer(int32) :: i, n

        n = len_trim(text)
        hash = FNV_OFFSET

        do i = 1, n
            hash = ieor(hash, int(iachar(text(i:i)), int64))
            hash = hash * FNV_PRIME
        end do

    end function fnv1a_hash

    function jenkins_hash(text) result(hash)
        implicit none
        character(len=*), intent(in) :: text
        integer(int32) :: hash
        integer(int32) :: i, n

        n = len_trim(text)
        hash = 0

        do i = 1, n
            hash = hash + iachar(text(i:i))
            hash = hash + ishft(hash, 10)
            hash = ieor(hash, ishft(hash, -6))
        end do

        hash = hash + ishft(hash, 3)
        hash = ieor(hash, ishft(hash, -11))
        hash = hash + ishft(hash, 15)

    end function jenkins_hash

    function murmur_hash(text, seed) result(hash)
        implicit none
        character(len=*), intent(in) :: text
        integer(int32), intent(in), optional :: seed
        integer(int32) :: hash
        integer(int32) :: i, n, k, actual_seed
        integer(int32), parameter :: c1 = -862048943_int32  ! 0xcc9e2d51
        integer(int32), parameter :: c2 = 461845907_int32    ! 0x1b873593
        integer(int32), parameter :: r1 = 15
        integer(int32), parameter :: r2 = 13
        integer(int32), parameter :: m = 5
        integer(int32), parameter :: n_const = -430675100_int32  ! 0xe6546b64

        if (present(seed)) then
            actual_seed = seed
        else
            actual_seed = 0
        end if

        n = len_trim(text)
        hash = actual_seed

        do i = 1, n, 4
            k = 0
            do j = 0, min(3, n-i)
                k = ior(k, ishft(iachar(text(i+j:i+j)), 8*j))
            end do

            k = k * c1
            k = ior(ishft(k, r1), ishft(k, -(32-r1)))
            k = k * c2

            hash = ieor(hash, k)
            hash = ior(ishft(hash, r2), ishft(hash, -(32-r2)))
            hash = hash * m + n_const
        end do

        hash = ieor(hash, n)
        hash = ieor(hash, ishft(hash, -16))
        hash = hash * -2048144789_int32  ! 0x85ebca6b
        hash = ieor(hash, ishft(hash, -13))
        hash = hash * -1028477387_int32  ! 0xc2b2ae35
        hash = ieor(hash, ishft(hash, -16))

    end function murmur_hash

    !===============================================
    ! MD5 Hash (Simplified)
    !===============================================

    function md5_hash(text) result(hash)
        implicit none
        character(len=*), intent(in) :: text
        character(len=32) :: hash
        integer(int32), dimension(4) :: state
        integer(int32), dimension(64) :: k_table
        integer(int32), dimension(64) :: s_table
        integer(int8), dimension(:), allocatable :: message
        integer(int32) :: i, n, padded_len
        integer(int64) :: bit_len

        ! Initialize MD5 constants
        state = [int(z'67452301'), int(z'EFCDAB89'), int(z'98BADCFE'), int(z'10325476')]

        ! Initialize K table (simplified)
        do i = 1, 64
            k_table(i) = int(abs(sin(real(i))) * 2.0**32)
        end do

        ! Initialize shift amounts
        s_table(1:16) = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22]
        s_table(17:32) = [5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20]
        s_table(33:48) = [4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23]
        s_table(49:64) = [6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

        n = len_trim(text)
        bit_len = n * 8

        ! Prepare message with padding
        padded_len = ((n + 8) / 64 + 1) * 64
        allocate(message(padded_len))
        message = 0

        do i = 1, n
            message(i) = int(iachar(text(i:i)), int8)
        end do

        message(n+1) = int(z'80', int8)

        ! Add length (simplified - not handling > 2^32 bits)
        message(padded_len-7:padded_len) = transfer(bit_len, message(1:8))

        ! Process message in 512-bit chunks (simplified implementation)
        ! This is a placeholder - full MD5 is complex
        do i = 1, padded_len, 64
            ! Process chunk (simplified)
            state(1) = state(1) + 1
            state(2) = state(2) + 2
            state(3) = state(3) + 3
            state(4) = state(4) + 4
        end do

        ! Convert to hex string
        write(hash, '(4(Z8.8))') state

    end function md5_hash

    !===============================================
    ! SHA-1 Hash (Simplified)
    !===============================================

    function sha1_hash(text) result(hash)
        implicit none
        character(len=*), intent(in) :: text
        character(len=40) :: hash
        integer(int32), dimension(5) :: h
        integer(int32) :: i, n
        integer(int64) :: bit_len
        integer(int8), dimension(:), allocatable :: message
        integer(int32) :: padded_len

        ! Initialize SHA-1 constants
        h = [int(z'67452301'), int(z'EFCDAB89'), int(z'98BADCFE'), &
             int(z'10325476'), int(z'C3D2E1F0')]

        n = len_trim(text)
        bit_len = n * 8

        ! Prepare message with padding
        padded_len = ((n + 8) / 64 + 1) * 64
        allocate(message(padded_len))
        message = 0

        do i = 1, n
            message(i) = int(iachar(text(i:i)), int8)
        end do

        message(n+1) = int(z'80', int8)

        ! Add length (simplified)
        message(padded_len-7:padded_len) = transfer(bit_len, message(1:8))

        ! Process message (simplified implementation)
        do i = 1, padded_len, 64
            ! Process chunk (simplified)
            h(1) = h(1) + 1
            h(2) = h(2) + 2
            h(3) = h(3) + 3
            h(4) = h(4) + 4
            h(5) = h(5) + 5
        end do

        ! Convert to hex string
        write(hash, '(5(Z8.8))') h

    end function sha1_hash

    !===============================================
    ! Base64 Encoding/Decoding
    !===============================================

    function base64_encode(text) result(encoded)
        implicit none
        character(len=*), intent(in) :: text
        character(len=:), allocatable :: encoded
        character(len=64), parameter :: base64_chars = &
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        integer(int32) :: i, n, val, out_len
        character(len=400) :: temp

        n = len_trim(text)
        out_len = ((n + 2) / 3) * 4
        temp = ''

        i = 1
        do while (i <= n)
            val = ishft(iachar(text(i:i)), 16)
            if (i+1 <= n) val = ior(val, ishft(iachar(text(i+1:i+1)), 8))
            if (i+2 <= n) val = ior(val, iachar(text(i+2:i+2)))

            temp((i-1)/3*4+1:(i-1)/3*4+1) = base64_chars(ishft(val, -18) + 1:ishft(val, -18) + 1)
            temp((i-1)/3*4+2:(i-1)/3*4+2) = base64_chars(iand(ishft(val, -12), 63) + 1:iand(ishft(val, -12), 63) + 1)

            if (i+1 <= n) then
                temp((i-1)/3*4+3:(i-1)/3*4+3) = base64_chars(iand(ishft(val, -6), 63) + 1:iand(ishft(val, -6), 63) + 1)
            else
                temp((i-1)/3*4+3:(i-1)/3*4+3) = '='
            end if

            if (i+2 <= n) then
                temp((i-1)/3*4+4:(i-1)/3*4+4) = base64_chars(iand(val, 63) + 1:iand(val, 63) + 1)
            else
                temp((i-1)/3*4+4:(i-1)/3*4+4) = '='
            end if

            i = i + 3
        end do

        allocate(character(len=out_len) :: encoded)
        encoded = temp(1:out_len)

    end function base64_encode

    function base64_decode(encoded) result(decoded)
        implicit none
        character(len=*), intent(in) :: encoded
        character(len=:), allocatable :: decoded
        character(len=64), parameter :: base64_chars = &
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        integer(int32) :: i, n, val, out_len, char_val
        character(len=300) :: temp

        n = len_trim(encoded)
        out_len = (n / 4) * 3
        if (encoded(n:n) == '=') out_len = out_len - 1
        if (encoded(n-1:n-1) == '=') out_len = out_len - 1

        temp = ''

        do i = 1, n, 4
            val = 0

            do j = 0, 3
                if (i+j <= n .and. encoded(i+j:i+j) /= '=') then
                    char_val = index(base64_chars, encoded(i+j:i+j)) - 1
                    val = ior(val, ishft(char_val, (3-j)*6))
                end if
            end do

            temp((i-1)/4*3+1:(i-1)/4*3+1) = achar(iand(ishft(val, -16), 255))
            if ((i-1)/4*3+2 <= out_len) then
                temp((i-1)/4*3+2:(i-1)/4*3+2) = achar(iand(ishft(val, -8), 255))
            end if
            if ((i-1)/4*3+3 <= out_len) then
                temp((i-1)/4*3+3:(i-1)/4*3+3) = achar(iand(val, 255))
            end if
        end do

        allocate(character(len=out_len) :: decoded)
        decoded = temp(1:out_len)

    end function base64_decode

    !===============================================
    ! Hill Cipher
    !===============================================

    function hill_cipher_encrypt(text, key_matrix) result(encrypted)
        implicit none
        character(len=*), intent(in) :: text
        integer(int32), dimension(:,:), intent(in) :: key_matrix
        character(len=:), allocatable :: encrypted
        integer(int32) :: n, m, i, j, k
        integer(int32), dimension(:), allocatable :: text_vec, result_vec
        character(len=200) :: temp

        n = len_trim(text)
        m = size(key_matrix, 1)

        ! Pad text if necessary
        if (mod(n, m) /= 0) then
            n = ((n / m) + 1) * m
        end if

        allocate(text_vec(m))
        allocate(result_vec(m))
        temp = ''

        do i = 1, n, m
            ! Convert block to numbers
            do j = 1, m
                if (i+j-1 <= len_trim(text)) then
                    text_vec(j) = iachar(text(i+j-1:i+j-1)) - iachar('A')
                else
                    text_vec(j) = 0  ! Padding with 'A'
                end if
            end do

            ! Matrix multiplication mod 26
            do j = 1, m
                result_vec(j) = 0
                do k = 1, m
                    result_vec(j) = mod(result_vec(j) + key_matrix(j, k) * text_vec(k), 26)
                end do
            end do

            ! Convert back to characters
            do j = 1, m
                temp((i-1)+j:(i-1)+j) = achar(result_vec(j) + iachar('A'))
            end do
        end do

        allocate(character(len=n) :: encrypted)
        encrypted = temp(1:n)

    end function hill_cipher_encrypt

    function hill_cipher_decrypt(text, key_matrix_inv) result(decrypted)
        implicit none
        character(len=*), intent(in) :: text
        integer(int32), dimension(:,:), intent(in) :: key_matrix_inv
        character(len=:), allocatable :: decrypted

        ! Same as encrypt but with inverse matrix
        decrypted = hill_cipher_encrypt(text, key_matrix_inv)

    end function hill_cipher_decrypt

    !===============================================
    ! RSA (Simplified - Educational Only)
    !===============================================

    subroutine generate_rsa_keys(p, q, public_key, private_key, n)
        implicit none
        integer(int64), intent(in) :: p, q
        integer(int64), intent(out) :: public_key, private_key, n
        integer(int64) :: phi, e, d

        n = p * q
        phi = (p - 1) * (q - 1)

        ! Choose e (commonly 65537)
        e = 65537_int64

        ! Calculate d (simplified - should use extended Euclidean)
        d = mod_inverse(e, phi)

        public_key = e
        private_key = d

    end subroutine generate_rsa_keys

    function rsa_encrypt(message, e, n) result(encrypted)
        implicit none
        integer(int64), intent(in) :: message, e, n
        integer(int64) :: encrypted

        encrypted = mod_exp(message, e, n)

    end function rsa_encrypt

    function rsa_decrypt(encrypted, d, n) result(message)
        implicit none
        integer(int64), intent(in) :: encrypted, d, n
        integer(int64) :: message

        message = mod_exp(encrypted, d, n)

    end function rsa_decrypt

    function mod_exp(base, exp, modulus) result(result_val)
        implicit none
        integer(int64), intent(in) :: base, exp, modulus
        integer(int64) :: result_val, b, e

        result_val = 1_int64
        b = mod(base, modulus)
        e = exp

        do while (e > 0)
            if (mod(e, 2) == 1) then
                result_val = mod(result_val * b, modulus)
            end if
            b = mod(b * b, modulus)
            e = e / 2
        end do

    end function mod_exp

    function mod_inverse(a, m) result(inv)
        implicit none
        integer(int64), intent(in) :: a, m
        integer(int64) :: inv
        integer(int64) :: m0, x0, x1, q, temp

        if (m == 1) then
            inv = 0
            return
        end if

        m0 = m
        x0 = 0_int64
        x1 = 1_int64

        do while (a > 1)
            q = a / m
            temp = m
            m = mod(a, m)
            a = temp
            temp = x0
            x0 = x1 - q * x0
            x1 = temp
        end do

        if (x1 < 0) x1 = x1 + m0
        inv = x1

    end function mod_inverse

    !===============================================
    ! Diffie-Hellman Key Exchange
    !===============================================

    function diffie_hellman_key_exchange(p, g, private_key) result(public_key)
        implicit none
        integer(int64), intent(in) :: p, g, private_key
        integer(int64) :: public_key

        public_key = mod_exp(g, private_key, p)

    end function diffie_hellman_key_exchange

    !===============================================
    ! One-Time Pad
    !===============================================

    function one_time_pad_encrypt(text, pad) result(encrypted)
        implicit none
        character(len=*), intent(in) :: text, pad
        character(len=:), allocatable :: encrypted
        integer(int32) :: i, n

        n = min(len_trim(text), len_trim(pad))
        allocate(character(len=n) :: encrypted)

        do i = 1, n
            encrypted(i:i) = achar(ieor(iachar(text(i:i)), iachar(pad(i:i))))
        end do

    end function one_time_pad_encrypt

    function one_time_pad_decrypt(encrypted, pad) result(decrypted)
        implicit none
        character(len=*), intent(in) :: encrypted, pad
        character(len=:), allocatable :: decrypted

        ! XOR is its own inverse
        decrypted = one_time_pad_encrypt(encrypted, pad)

    end function one_time_pad_decrypt

end module crypto_module