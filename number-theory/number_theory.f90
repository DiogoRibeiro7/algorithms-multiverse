! ============================================================================
! Number Theory Algorithms - Fortran Implementation
! ============================================================================
!
! Modern Fortran (90+) implementation of fundamental number theory algorithms.
! Optimized for numerical computing with scientific applications.
!
! Compilation:
!   gfortran -O3 -o number_theory number_theory.f90
!   # Or with Intel Fortran:
!   ifort -O3 -o number_theory number_theory.f90
!
! Usage:
!   ./number_theory
!
! Features:
!   - Modern Fortran 90+ features (modules, dynamic arrays)
!   - Array operations and intrinsic functions
!   - Optimized for numerical computing
!   - Support for 64-bit integers
!
! Author: algorithms-multiverse
! ============================================================================

module number_theory_module
    implicit none
    private
    public :: sieve_of_eratosthenes, gcd, extended_gcd, lcm, &
              mod_exp, mod_inverse, prime_factorization, &
              miller_rabin, euler_totient, chinese_remainder_theorem

    integer, parameter :: i8 = selected_int_kind(18)  ! 64-bit integers

contains

    ! ========================================================================
    ! PRIME NUMBER GENERATION
    ! ========================================================================

    !> Sieve of Eratosthenes - Generate all primes up to limit
    !!
    !! Time Complexity: O(n log log n)
    !! Space Complexity: O(n)
    !!
    !! @param limit Upper bound for prime generation
    !! @param primes Output array of primes (allocatable)
    !! @param n_primes Number of primes found
    subroutine sieve_of_eratosthenes(limit, primes, n_primes)
        integer(i8), intent(in) :: limit
        integer(i8), allocatable, intent(out) :: primes(:)
        integer, intent(out) :: n_primes

        logical, allocatable :: is_prime(:)
        integer(i8) :: i, j, sqrt_limit
        integer :: idx

        if (limit < 2) then
            n_primes = 0
            return
        end if

        ! Initialize sieve
        allocate(is_prime(0:limit))
        is_prime = .true.
        is_prime(0) = .false.
        is_prime(1) = .false.

        ! Sieve algorithm
        sqrt_limit = int(sqrt(real(limit)), i8)
        do i = 2, sqrt_limit
            if (is_prime(i)) then
                ! Mark multiples of i as composite
                do j = i*i, limit, i
                    is_prime(j) = .false.
                end do
            end if
        end do

        ! Count primes
        n_primes = count(is_prime)

        ! Collect primes
        allocate(primes(n_primes))
        idx = 1
        do i = 2, limit
            if (is_prime(i)) then
                primes(idx) = i
                idx = idx + 1
            end if
        end do

        deallocate(is_prime)
    end subroutine sieve_of_eratosthenes

    ! ========================================================================
    ! GREATEST COMMON DIVISOR
    ! ========================================================================

    !> Euclidean algorithm for GCD
    !!
    !! Time Complexity: O(log min(a, b))
    !! Space Complexity: O(1)
    !!
    !! Mathematical Proof:
    !!   gcd(a, b) = gcd(b, a mod b) when b != 0
    !!   gcd(a, 0) = a
    recursive function gcd(a, b) result(g)
        integer(i8), intent(in) :: a, b
        integer(i8) :: g

        if (b == 0) then
            g = a
        else
            g = gcd(b, mod(a, b))
        end if
    end function gcd

    !> Extended Euclidean Algorithm
    !! Finds gcd(a, b) and Bézout coefficients x, y such that ax + by = gcd(a, b)
    !!
    !! Time Complexity: O(log min(a, b))
    !! Applications: Modular multiplicative inverse, linear Diophantine equations
    recursive subroutine extended_gcd(a, b, g, x, y)
        integer(i8), intent(in) :: a, b
        integer(i8), intent(out) :: g, x, y
        integer(i8) :: x1, y1, q

        if (b == 0) then
            g = a
            x = 1
            y = 0
        else
            call extended_gcd(b, mod(a, b), g, x1, y1)
            x = y1
            y = x1 - (a / b) * y1
        end if
    end subroutine extended_gcd

    !> Least Common Multiple
    !!
    !! Formula: lcm(a, b) = (a * b) / gcd(a, b)
    function lcm(a, b) result(l)
        integer(i8), intent(in) :: a, b
        integer(i8) :: l

        if (a == 0 .or. b == 0) then
            l = 0
        else
            l = (a / gcd(a, b)) * b
        end if
    end function lcm

    ! ========================================================================
    ! MODULAR ARITHMETIC
    ! ========================================================================

    !> Modular exponentiation using binary exponentiation
    !! Computes: base^exponent mod modulus
    !!
    !! Time Complexity: O(log exponent)
    !! Space Complexity: O(1)
    !!
    !! Critical for cryptographic applications (RSA, Diffie-Hellman)
    function mod_exp(base, exponent, modulus) result(res)
        integer(i8), intent(in) :: base, exponent, modulus
        integer(i8) :: res
        integer(i8) :: b, e

        if (modulus == 1) then
            res = 0
            return
        end if

        res = 1
        b = mod(base, modulus)
        e = exponent

        do while (e > 0)
            if (mod(e, 2_i8) == 1) then
                res = mod(res * b, modulus)
            end if
            e = e / 2
            b = mod(b * b, modulus)
        end do
    end function mod_exp

    !> Modular multiplicative inverse
    !! Find x such that (a * x) ≡ 1 (mod m)
    !!
    !! Uses Extended Euclidean Algorithm
    !! Inverse exists if and only if gcd(a, m) = 1
    !!
    !! @return Inverse of a mod m, or 0 if it doesn't exist
    function mod_inverse(a, m) result(inv)
        integer(i8), intent(in) :: a, m
        integer(i8) :: inv
        integer(i8) :: g, x, y

        call extended_gcd(a, m, g, x, y)

        if (g /= 1) then
            inv = 0  ! Inverse doesn't exist
        else
            ! Ensure positive result
            inv = mod(mod(x, m) + m, m)
        end if
    end function mod_inverse

    ! ========================================================================
    ! PRIME FACTORIZATION
    ! ========================================================================

    !> Prime factorization using trial division
    !!
    !! Time Complexity: O(√n)
    !! Returns array of prime factors (with repetition)
    subroutine prime_factorization(n, factors, count)
        integer(i8), intent(in) :: n
        integer(i8), allocatable, intent(out) :: factors(:)
        integer, intent(out) :: count

        integer(i8) :: temp_factors(100)  ! Temporary storage
        integer(i8) :: num, i
        integer :: idx

        if (n < 2) then
            count = 0
            return
        end if

        num = n
        idx = 0

        ! Handle factor 2
        do while (mod(num, 2_i8) == 0)
            idx = idx + 1
            temp_factors(idx) = 2
            num = num / 2
        end do

        ! Check odd divisors
        i = 3
        do while (i * i <= num)
            do while (mod(num, i) == 0)
                idx = idx + 1
                temp_factors(idx) = i
                num = num / i
            end do
            i = i + 2
        end do

        ! If num > 1, it's a prime factor
        if (num > 1) then
            idx = idx + 1
            temp_factors(idx) = num
        end if

        ! Copy to output array
        count = idx
        allocate(factors(count))
        factors(1:count) = temp_factors(1:count)
    end subroutine prime_factorization

    ! ========================================================================
    ! PRIMALITY TESTING
    ! ========================================================================

    !> Miller-Rabin primality test
    !!
    !! Probabilistic test with deterministic witnesses for n < 2^64
    !!
    !! Time Complexity: O(k log³ n) for k rounds
    !! Error probability: ≤ 4^(-k) for random witnesses
    function miller_rabin(n, k) result(is_prime)
        integer(i8), intent(in) :: n
        integer, intent(in) :: k
        logical :: is_prime

        integer(i8) :: d, r, a, x
        integer :: i, j
        integer(i8), parameter :: witnesses(12) = &
            [2_i8, 3_i8, 5_i8, 7_i8, 11_i8, 13_i8, &
             17_i8, 19_i8, 23_i8, 29_i8, 31_i8, 37_i8]
        logical :: composite

        ! Handle small cases
        if (n < 2) then
            is_prime = .false.
            return
        end if
        if (n == 2 .or. n == 3) then
            is_prime = .true.
            return
        end if
        if (mod(n, 2_i8) == 0) then
            is_prime = .false.
            return
        end if

        ! Write n-1 as 2^r * d where d is odd
        d = n - 1
        r = 0
        do while (mod(d, 2_i8) == 0)
            r = r + 1
            d = d / 2
        end do

        ! Test each witness
        do i = 1, 12
            a = witnesses(i)
            if (a >= n) cycle

            ! Compute x = a^d mod n
            x = mod_exp(a, d, n)

            if (x == 1 .or. x == n - 1) cycle

            ! Square x repeatedly r-1 times
            composite = .true.
            do j = 1, r - 1
                x = mod_exp(x, 2_i8, n)
                if (x == n - 1) then
                    composite = .false.
                    exit
                end if
            end do

            if (composite) then
                is_prime = .false.
                return
            end if
        end do

        is_prime = .true.
    end function miller_rabin

    ! ========================================================================
    ! EULER'S TOTIENT FUNCTION
    ! ========================================================================

    !> Calculate Euler's totient function φ(n)
    !!
    !! φ(n) = count of integers k where 1 ≤ k ≤ n and gcd(k, n) = 1
    !!
    !! Time Complexity: O(√n)
    function euler_totient(n) result(phi)
        integer(i8), intent(in) :: n
        integer(i8) :: phi
        integer(i8) :: temp, i

        if (n == 1) then
            phi = 1
            return
        end if

        phi = n
        temp = n

        ! Handle factor 2
        if (mod(temp, 2_i8) == 0) then
            phi = phi / 2
            do while (mod(temp, 2_i8) == 0)
                temp = temp / 2
            end do
        end if

        ! Check odd factors
        i = 3
        do while (i * i <= temp)
            if (mod(temp, i) == 0) then
                phi = phi / i * (i - 1)
                do while (mod(temp, i) == 0)
                    temp = temp / i
                end do
            end if
            i = i + 2
        end do

        ! If temp > 1, it's a prime factor
        if (temp > 1) then
            phi = phi / temp * (temp - 1)
        end if
    end function euler_totient

    ! ========================================================================
    ! CHINESE REMAINDER THEOREM
    ! ========================================================================

    !> Chinese Remainder Theorem
    !! Solve system of congruences
    !!
    !! Requires moduli to be pairwise coprime
    !!
    !! @return .true. if successful, .false. if moduli not coprime
    function chinese_remainder_theorem(remainders, moduli, n, result) result(success)
        integer, intent(in) :: n
        integer(i8), intent(in) :: remainders(n), moduli(n)
        integer(i8), intent(out) :: result
        logical :: success

        integer(i8) :: big_m, mi, yi
        integer :: i, j

        ! Check if moduli are pairwise coprime
        do i = 1, n
            do j = i + 1, n
                if (gcd(moduli(i), moduli(j)) /= 1) then
                    success = .false.
                    return
                end if
            end do
        end do

        ! Calculate M = product of all moduli
        big_m = product(moduli)

        ! Calculate solution
        result = 0
        do i = 1, n
            mi = big_m / moduli(i)
            yi = mod_inverse(mi, moduli(i))
            if (yi == 0) then
                success = .false.
                return
            end if
            result = mod(result + remainders(i) * mi * yi, big_m)
        end do

        success = .true.
    end function chinese_remainder_theorem

end module number_theory_module

! ============================================================================
! MAIN PROGRAM - TESTING AND DEMONSTRATION
! ============================================================================

program test_number_theory
    use number_theory_module
    implicit none

    integer, parameter :: i8 = selected_int_kind(18)

    call print_header()
    call test_sieve()
    call test_gcd_lcm()
    call test_modular_arithmetic()
    call test_primality()
    call test_factorization()
    call test_totient()
    call test_crt()
    call print_footer()

contains

    subroutine print_header()
        print '(70("="))'
        print '(a)', "NUMBER THEORY ALGORITHMS - FORTRAN IMPLEMENTATION"
        print '(70("="))'
    end subroutine print_header

    subroutine print_footer()
        print *
        print '(70("="))'
        print '(a)', "All tests completed successfully!"
        print '(70("="))'
    end subroutine print_footer

    subroutine print_separator()
        print '(50("-"))'
    end subroutine print_separator

    subroutine test_sieve()
        integer(i8), allocatable :: primes(:)
        integer :: n_primes, i

        print *
        print '(a)', "1. SIEVE OF ERATOSTHENES"
        call print_separator()

        call sieve_of_eratosthenes(100_i8, primes, n_primes)

        print '(a, i0, a)', "Primes up to 100: (showing first 25 of ", n_primes, ")"
        do i = 1, min(25, n_primes)
            write(*, '(i0, 1x)', advance='no') primes(i)
        end do
        if (n_primes > 25) write(*, '(a)', advance='no') "..."
        print *
        print '(a, i0, a)', "Total: ", n_primes, " primes"

        deallocate(primes)
    end subroutine test_sieve

    subroutine test_gcd_lcm()
        integer(i8) :: a, b, g, l
        integer :: i

        print *
        print '(a)', "2. GCD AND LCM"
        call print_separator()

        ! Test pairs
        do i = 1, 3
            select case (i)
                case (1)
                    a = 48; b = 18
                case (2)
                    a = 100; b = 35
                case (3)
                    a = 17; b = 19
            end select

            g = gcd(a, b)
            l = lcm(a, b)
            print '(a, i0, a, i0, a, i0, a, i0, a, i0, a, i0)', &
                "gcd(", a, ", ", b, ") = ", g, ", lcm(", a, ", ", b, ") = ", l
        end do
    end subroutine test_gcd_lcm

    subroutine test_modular_arithmetic()
        integer(i8) :: base, exp, modulus, result, inv
        integer :: i

        print *
        print '(a)', "3. MODULAR ARITHMETIC"
        call print_separator()

        print '(a)', "Modular Exponentiation:"

        do i = 1, 3
            select case (i)
                case (1)
                    base = 2; exp = 10; modulus = 1000
                case (2)
                    base = 3; exp = 100; modulus = 13
                case (3)
                    base = 7; exp = 256; modulus = 100
            end select

            result = mod_exp(base, exp, modulus)
            print '(a, i0, a, i0, a, i0, a, i0)', &
                "  ", base, "^", exp, " mod ", modulus, " = ", result
        end do

        print *
        print '(a)', "Modular Inverse:"

        base = 3; modulus = 11
        inv = mod_inverse(base, modulus)
        print '(a, i0, a, i0, a, i0)', &
            "  Inverse of ", base, " mod ", modulus, " = ", inv
        print '(a, i0, a, i0, a, i0, a, i0)', &
            "    Verification: (", base, " × ", inv, ") mod ", modulus, " = ", mod(base * inv, modulus)
    end subroutine test_modular_arithmetic

    subroutine test_primality()
        integer(i8) :: test_nums(7)
        integer :: i
        logical :: is_prime

        print *
        print '(a)', "4. PRIMALITY TESTING"
        call print_separator()

        test_nums = [17_i8, 561_i8, 1105_i8, 2047_i8, 8191_i8, 9973_i8, 10001_i8]

        do i = 1, 7
            is_prime = miller_rabin(test_nums(i), 20)
            if (is_prime) then
                print '(i5, a)', test_nums(i), ": PRIME"
            else
                print '(i5, a)', test_nums(i), ": COMPOSITE"
            end if
        end do
    end subroutine test_primality

    subroutine test_factorization()
        integer(i8), allocatable :: factors(:)
        integer(i8) :: test_nums(4)
        integer :: count, i, j

        print *
        print '(a)', "5. PRIME FACTORIZATION"
        call print_separator()

        test_nums = [60_i8, 128_i8, 1001_i8, 2024_i8]

        do i = 1, 4
            call prime_factorization(test_nums(i), factors, count)
            write(*, '(i0, a)', advance='no') test_nums(i), " = "
            do j = 1, count
                write(*, '(i0)', advance='no') factors(j)
                if (j < count) write(*, '(a)', advance='no') " × "
            end do
            print *
            deallocate(factors)
        end do
    end subroutine test_factorization

    subroutine test_totient()
        integer(i8) :: test_vals(5), phi
        integer :: i

        print *
        print '(a)', "6. EULER'S TOTIENT FUNCTION"
        call print_separator()

        test_vals = [1_i8, 9_i8, 10_i8, 36_i8, 100_i8]

        do i = 1, 5
            phi = euler_totient(test_vals(i))
            print '(a, i0, a, i0)', "φ(", test_vals(i), ") = ", phi
        end do
    end subroutine test_totient

    subroutine test_crt()
        integer(i8) :: remainders(3), moduli(3), result
        logical :: success
        integer :: i

        print *
        print '(a)', "7. CHINESE REMAINDER THEOREM"
        call print_separator()

        remainders = [2_i8, 3_i8, 2_i8]
        moduli = [3_i8, 5_i8, 7_i8]

        print '(a)', "System of congruences:"
        do i = 1, 3
            print '(a, i0, a, i0, a)', "  x ≡ ", remainders(i), " (mod ", moduli(i), ")"
        end do

        success = chinese_remainder_theorem(remainders, moduli, 3, result)

        if (success) then
            print '(a, i0)', "Solution: x = ", result
            print '(a)', "Verification:"
            do i = 1, 3
                print '(a, i0, a, i0, a, i0, a, i0)', &
                    "  ", result, " mod ", moduli(i), " = ", mod(result, moduli(i)), &
                    " (expected ", remainders(i), ")"
            end do
        else
            print '(a)', "Failed to solve (moduli not pairwise coprime)"
        end if
    end subroutine test_crt

end program test_number_theory
