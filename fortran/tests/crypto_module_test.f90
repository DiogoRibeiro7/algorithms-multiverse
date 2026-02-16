! Test suite for cryptographic algorithms module
program test_crypto_module
    use iso_fortran_env, only: int32, int64
    use crypto_module
    implicit none

    integer :: total_tests = 0, passed_tests = 0

    print '(A)', "========================================"
    print '(A)', "    Crypto Module Test Suite"
    print '(A)', "========================================"

    call test_classical_ciphers()
    call test_hash_functions()
    call test_rsa_encryption()

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

    subroutine test_classical_ciphers()
        character(len=100) :: plaintext, ciphertext, decrypted
        character(len=26) :: key
        logical :: success
        integer :: i

        print '(A)', ""
        print '(A)', "Testing Classical Ciphers..."

        plaintext = "HELLO WORLD"

        ! Test Caesar cipher
        ciphertext = caesar_cipher_encrypt(plaintext, 3)
        decrypted = caesar_cipher_decrypt(ciphertext, 3)
        success = trim(adjustl(decrypted)) == trim(adjustl(plaintext))
        call report_test("Caesar cipher encrypt/decrypt", success)

        ! Test Vigenere cipher
        key = "KEY"
        ciphertext = vigenere_encrypt(plaintext, key)
        decrypted = vigenere_decrypt(ciphertext, key)
        success = trim(adjustl(decrypted)) == trim(adjustl(plaintext))
        call report_test("Vigenere cipher encrypt/decrypt", success)

        ! Test XOR cipher
        key = "SECRET"
        ciphertext = xor_cipher(plaintext, key)
        decrypted = xor_cipher(ciphertext, key)  ! XOR is its own inverse
        success = trim(adjustl(decrypted)) == trim(adjustl(plaintext))
        call report_test("XOR cipher encrypt/decrypt", success)

        ! Test Substitution cipher
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        ciphertext = substitution_cipher_encrypt(plaintext, key)
        decrypted = substitution_cipher_decrypt(ciphertext, key)
        success = trim(adjustl(decrypted)) == trim(adjustl(plaintext))
        call report_test("Substitution cipher encrypt/decrypt", success)

    end subroutine test_classical_ciphers

    subroutine test_hash_functions()
        character(len=100) :: input1, input2
        integer(int64) :: hash1, hash2
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Hash Functions..."

        input1 = "Hello World"
        input2 = "Hello World"

        ! Test simple hash - same input should give same hash
        hash1 = simple_hash(input1)
        hash2 = simple_hash(input2)
        success = hash1 == hash2
        call report_test("Simple hash consistency", success)

        ! Test simple hash - different input should give different hash
        input2 = "Hello World!"
        hash2 = simple_hash(input2)
        success = hash1 /= hash2
        call report_test("Simple hash uniqueness", success)

        ! Test DJB2 hash - same input should give same hash
        input1 = "test string"
        input2 = "test string"
        hash1 = djb2_hash(input1)
        hash2 = djb2_hash(input2)
        success = hash1 == hash2
        call report_test("DJB2 hash consistency", success)

        ! Test DJB2 hash - different input should give different hash
        input2 = "different string"
        hash2 = djb2_hash(input2)
        success = hash1 /= hash2
        call report_test("DJB2 hash uniqueness", success)

    end subroutine test_hash_functions

    subroutine test_rsa_encryption()
        integer(int64) :: public_key, private_key, modulus
        integer(int64) :: plaintext, ciphertext, decrypted
        logical :: success

        print '(A)', ""
        print '(A)', "Testing RSA Encryption..."

        ! Generate RSA keys (using small primes for testing)
        call generate_rsa_keys(public_key, private_key, modulus)

        ! Test key generation
        success = public_key > 0 .and. private_key > 0 .and. modulus > 0
        call report_test("RSA key generation", success)

        ! Test encryption and decryption
        plaintext = 42  ! Small number that fits within modulus

        ! Only test if plaintext is less than modulus
        if (plaintext < modulus) then
            ciphertext = rsa_encrypt(plaintext, public_key, modulus)
            success = ciphertext /= plaintext .and. ciphertext > 0
            call report_test("RSA encryption", success)

            decrypted = rsa_decrypt(ciphertext, private_key, modulus)
            success = decrypted == plaintext
            call report_test("RSA decryption", success)
        else
            print '(A)', "  ⚠ RSA encryption test skipped (modulus too small)"
            print '(A)', "  ⚠ RSA decryption test skipped (modulus too small)"
        end if

        ! Test with another plaintext value
        plaintext = 7
        if (plaintext < modulus) then
            ciphertext = rsa_encrypt(plaintext, public_key, modulus)
            decrypted = rsa_decrypt(ciphertext, private_key, modulus)
            success = decrypted == plaintext
            call report_test("RSA round-trip", success)
        else
            print '(A)', "  ⚠ RSA round-trip test skipped (modulus too small)"
        end if

    end subroutine test_rsa_encryption

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

end program test_crypto_module