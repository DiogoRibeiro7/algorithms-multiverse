! Comprehensive example demonstrating multiple algorithm modules
program comprehensive_example
    use iso_fortran_env, only: int32, real64
    use algorithms_multiverse
    implicit none

    print '(A)', ""
    print '(A)', "============================================"
    print '(A)', "   Algorithms Multiverse - Fortran"
    print '(A)', "      Comprehensive Examples"
    print '(A)', "============================================"
    print '(A)', ""

    ! Display module statistics
    call print_statistics()

    print '(A)', ""
    print '(A)', "Running comprehensive examples..."
    print '(A)', ""

    ! Example 1: Sorting and searching
    call sorting_searching_example()

    ! Example 2: Data structures
    call data_structures_example()

    ! Example 3: Numerical algorithms
    call numerical_example()

    ! Example 4: Matrix operations
    call matrix_example()

    ! Example 5: Cryptography
    call crypto_example()

    print '(A)', ""
    print '(A)', "============================================"
    print '(A)', "    All Examples Completed Successfully"
    print '(A)', "============================================"

contains

    subroutine sorting_searching_example()
        integer :: arr(10), sorted(10)
        integer :: target, position
        logical :: found

        print '(A)', "1. Sorting & Searching Example"
        print '(A)', "-------------------------------"

        ! Initialize array
        arr = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]
        print '(A,10I4)', "Original array: ", arr

        ! Sort using quicksort
        sorted = arr
        call quick_sort(sorted, 1, 10)
        print '(A,10I4)', "After quicksort: ", sorted

        ! Binary search
        target = 45
        call binary_search(sorted, target, position, found)
        if (found) then
            print '(A,I0,A,I0)', "Found ", target, " at position ", position
        else
            print '(A,I0,A)', "Value ", target, " not found"
        end if

        print '(A)', ""
    end subroutine sorting_searching_example

    subroutine data_structures_example()
        type(stack_type) :: stack
        type(queue_type) :: queue
        integer :: value

        print '(A)', "2. Data Structures Example"
        print '(A)', "--------------------------"

        ! Stack operations
        call stack_init(stack, 5)
        call stack_push(stack, 10)
        call stack_push(stack, 20)
        call stack_push(stack, 30)

        print '(A)', "Stack operations:"
        print '(A)', "  Pushed: 10, 20, 30"

        value = stack_pop(stack)
        print '(A,I0)', "  Popped: ", value

        ! Queue operations
        call queue_init(queue, 5)
        call queue_enqueue(queue, 100)
        call queue_enqueue(queue, 200)
        call queue_enqueue(queue, 300)

        print '(A)', "Queue operations:"
        print '(A)', "  Enqueued: 100, 200, 300"

        value = queue_dequeue(queue)
        print '(A,I0)', "  Dequeued: ", value

        call stack_destroy(stack)
        call queue_destroy(queue)

        print '(A)', ""
    end subroutine data_structures_example

    subroutine numerical_example()
        integer :: n, result
        integer, allocatable :: primes(:)
        logical :: is_prime_num

        print '(A)', "3. Numerical Algorithms Example"
        print '(A)', "--------------------------------"

        ! GCD and LCM
        print '(A,I0)', "GCD(48, 18) = ", gcd(48, 18)
        print '(A,I0)', "LCM(12, 15) = ", lcm(12, 15)

        ! Prime checking
        n = 97
        is_prime_num = is_prime(n)
        if (is_prime_num) then
            print '(A,I0,A)', n, " is prime"
        else
            print '(A,I0,A)', n, " is not prime"
        end if

        ! Sieve of Eratosthenes
        allocate(primes(25))
        call sieve_of_eratosthenes(100, primes, result)
        print '(A,I0,A)', "Found ", result, " primes below 100"
        print '(A,25I4)', "First 25 primes: ", primes

        ! Factorial
        print '(A,I0)', "10! = ", factorial(10)

        deallocate(primes)
        print '(A)', ""
    end subroutine numerical_example

    subroutine matrix_example()
        type(matrix_type) :: A, B, C
        real(real64) :: det

        print '(A)', "4. Matrix Operations Example"
        print '(A)', "-----------------------------"

        ! Create matrices
        A%rows = 3
        A%cols = 3
        allocate(A%data(3, 3))
        A%data = reshape([1.0, 2.0, 3.0, &
                          4.0, 5.0, 6.0, &
                          7.0, 8.0, 9.0], [3, 3])

        B%rows = 3
        B%cols = 3
        allocate(B%data(3, 3))
        B%data = reshape([9.0, 8.0, 7.0, &
                          6.0, 5.0, 4.0, &
                          3.0, 2.0, 1.0], [3, 3])

        ! Matrix multiplication
        call matrix_multiply(A, B, C)

        print '(A)', "Matrix A:"
        call print_matrix(A)
        print '(A)', "Matrix B:"
        call print_matrix(B)
        print '(A)', "A × B:"
        call print_matrix(C)

        deallocate(A%data, B%data, C%data)
        print '(A)', ""
    end subroutine matrix_example

    subroutine crypto_example()
        character(len=50) :: plaintext, ciphertext, decrypted

        print '(A)', "5. Cryptography Example"
        print '(A)', "-----------------------"

        plaintext = "HELLO FORTRAN WORLD"

        ! Caesar cipher
        ciphertext = caesar_cipher_encrypt(plaintext, 3)
        print '(A)', "Original: ", trim(plaintext)
        print '(A)', "Caesar encrypted (shift=3): ", trim(ciphertext)

        decrypted = caesar_cipher_decrypt(ciphertext, 3)
        print '(A)', "Decrypted: ", trim(decrypted)

        ! XOR cipher
        ciphertext = xor_cipher(plaintext, "KEY")
        print '(A)', "XOR encrypted: [binary data]"

        decrypted = xor_cipher(ciphertext, "KEY")
        print '(A)', "XOR decrypted: ", trim(decrypted)

        print '(A)', ""
    end subroutine crypto_example

    subroutine print_matrix(mat)
        type(matrix_type), intent(in) :: mat
        integer :: i

        do i = 1, mat%rows
            print '(3F8.2)', mat%data(i, :)
        end do
    end subroutine print_matrix

end program comprehensive_example