! Numerical Algorithms Module
! Mathematical and numerical computation algorithms optimized for Fortran

module numerical_module
    use iso_fortran_env, only: int32, int64, real32, real64
    use, intrinsic :: ieee_arithmetic
    implicit none
    private

    ! Public interfaces
    public :: gcd, lcm, is_prime, sieve_of_eratosthenes, prime_factorization
    public :: factorial, binomial_coefficient, fast_power, modular_exponentiation
    public :: fibonacci, fibonacci_matrix, tribonacci
    public :: newton_raphson, bisection_method, secant_method, regula_falsi
    public :: trapezoidal_integration, simpson_integration, romberg_integration
    public :: euler_method, runge_kutta4, adams_bashforth
    public :: fft, ifft, convolution
    public :: polynomial_eval, polynomial_roots, horner_method

    ! Constants
    real(real64), parameter :: PI = 4.0_real64 * atan(1.0_real64)
    real(real64), parameter :: E = exp(1.0_real64)
    real(real64), parameter :: EPSILON = epsilon(1.0_real64)

    ! Abstract interface for functions
    abstract interface
        function real_function(x) result(y)
            import :: real64
            real(real64), intent(in) :: x
            real(real64) :: y
        end function real_function

        function ode_function(t, y) result(dydt)
            import :: real64
            real(real64), intent(in) :: t, y
            real(real64) :: dydt
        end function ode_function
    end interface

contains

    !===========================================================================
    ! Number Theory Algorithms
    !===========================================================================

    ! Greatest Common Divisor using Euclidean algorithm
    recursive function gcd(a, b) result(g)
        implicit none
        integer(int64), intent(in) :: a, b
        integer(int64) :: g

        if (b == 0) then
            g = abs(a)
        else
            g = gcd(b, mod(a, b))
        end if

    end function gcd

    ! Least Common Multiple
    function lcm(a, b) result(l)
        implicit none
        integer(int64), intent(in) :: a, b
        integer(int64) :: l

        if (a == 0 .or. b == 0) then
            l = 0
        else
            l = abs(a * b) / gcd(a, b)
        end if

    end function lcm

    ! Check if a number is prime
    function is_prime(n) result(prime)
        implicit none
        integer(int64), intent(in) :: n
        logical :: prime
        integer(int64) :: i, sqrt_n

        prime = .false.

        if (n <= 1) return
        if (n <= 3) then
            prime = .true.
            return
        end if
        if (mod(n, 2) == 0 .or. mod(n, 3) == 0) return

        sqrt_n = int(sqrt(real(n)))
        i = 5

        do while (i <= sqrt_n)
            if (mod(n, i) == 0 .or. mod(n, i + 2) == 0) return
            i = i + 6
        end do

        prime = .true.

    end function is_prime

    ! Sieve of Eratosthenes for finding all primes up to n
    function sieve_of_eratosthenes(n) result(primes)
        implicit none
        integer(int32), intent(in) :: n
        integer(int32), dimension(:), allocatable :: primes
        logical, dimension(:), allocatable :: is_prime_arr
        integer(int32) :: i, j, count, k

        allocate(is_prime_arr(2:n))
        is_prime_arr = .true.

        do i = 2, int(sqrt(real(n)))
            if (is_prime_arr(i)) then
                do j = i * i, n, i
                    is_prime_arr(j) = .false.
                end do
            end if
        end do

        ! Count primes
        count = count(is_prime_arr)
        allocate(primes(count))

        ! Collect primes
        k = 1
        do i = 2, n
            if (is_prime_arr(i)) then
                primes(k) = i
                k = k + 1
            end if
        end do

    end function sieve_of_eratosthenes

    ! Prime factorization
    function prime_factorization(n) result(factors)
        implicit none
        integer(int64), intent(in) :: n
        integer(int64), dimension(:, :), allocatable :: factors
        integer(int64) :: num, d, count, total_factors, i

        num = n
        total_factors = 0

        ! Count factors
        d = 2
        do while (d * d <= num)
            if (mod(num, d) == 0) then
                total_factors = total_factors + 1
                do while (mod(num, d) == 0)
                    num = num / d
                end do
            end if
            if (d == 2) then
                d = 3
            else
                d = d + 2
            end if
        end do

        if (num > 1) total_factors = total_factors + 1

        ! Allocate result array
        allocate(factors(total_factors, 2))

        ! Get factors
        num = n
        d = 2
        i = 1

        do while (d * d <= num)
            count = 0
            do while (mod(num, d) == 0)
                count = count + 1
                num = num / d
            end do

            if (count > 0) then
                factors(i, 1) = d
                factors(i, 2) = count
                i = i + 1
            end if

            if (d == 2) then
                d = 3
            else
                d = d + 2
            end if
        end do

        if (num > 1) then
            factors(i, 1) = num
            factors(i, 2) = 1
        end if

    end function prime_factorization

    !===========================================================================
    ! Combinatorial Functions
    !===========================================================================

    ! Factorial (iterative for efficiency)
    function factorial(n) result(fact)
        implicit none
        integer(int32), intent(in) :: n
        integer(int64) :: fact
        integer(int32) :: i

        fact = 1
        do i = 2, n
            fact = fact * i
        end do

    end function factorial

    ! Binomial coefficient (n choose k)
    function binomial_coefficient(n, k) result(coeff)
        implicit none
        integer(int32), intent(in) :: n, k
        integer(int64) :: coeff
        integer(int32) :: i, k_min

        if (k < 0 .or. k > n) then
            coeff = 0
            return
        end if

        k_min = min(k, n - k)
        coeff = 1

        do i = 0, k_min - 1
            coeff = coeff * (n - i) / (i + 1)
        end do

    end function binomial_coefficient

    ! Fast power using binary exponentiation
    function fast_power(base, exp) result(result_val)
        implicit none
        integer(int64), intent(in) :: base, exp
        integer(int64) :: result_val, b, e

        result_val = 1
        b = base
        e = exp

        do while (e > 0)
            if (mod(e, 2) == 1) then
                result_val = result_val * b
            end if
            b = b * b
            e = e / 2
        end do

    end function fast_power

    ! Modular exponentiation: (base^exp) mod m
    function modular_exponentiation(base, exp, m) result(result_val)
        implicit none
        integer(int64), intent(in) :: base, exp, m
        integer(int64) :: result_val, b, e

        result_val = 1
        b = mod(base, m)
        e = exp

        do while (e > 0)
            if (mod(e, 2) == 1) then
                result_val = mod(result_val * b, m)
            end if
            b = mod(b * b, m)
            e = e / 2
        end do

    end function modular_exponentiation

    !===========================================================================
    ! Fibonacci and Related Sequences
    !===========================================================================

    ! Fibonacci using iteration
    function fibonacci(n) result(fib)
        implicit none
        integer(int32), intent(in) :: n
        integer(int64) :: fib
        integer(int64) :: prev, curr
        integer(int32) :: i

        if (n <= 0) then
            fib = 0
        else if (n == 1) then
            fib = 1
        else
            prev = 0
            curr = 1
            do i = 2, n
                fib = prev + curr
                prev = curr
                curr = fib
            end do
        end if

    end function fibonacci

    ! Fibonacci using matrix exponentiation
    function fibonacci_matrix(n) result(fib)
        implicit none
        integer(int32), intent(in) :: n
        integer(int64) :: fib
        integer(int64), dimension(2, 2) :: mat, result_mat

        if (n <= 0) then
            fib = 0
        else if (n == 1) then
            fib = 1
        else
            mat = reshape([1_int64, 1_int64, 1_int64, 0_int64], [2, 2])
            result_mat = matrix_power(mat, n - 1)
            fib = result_mat(1, 1)
        end if

    end function fibonacci_matrix

    ! Matrix power for 2x2 matrices
    function matrix_power(mat, n) result(result_mat)
        implicit none
        integer(int64), dimension(2, 2), intent(in) :: mat
        integer(int32), intent(in) :: n
        integer(int64), dimension(2, 2) :: result_mat, base
        integer(int32) :: exp

        result_mat = reshape([1_int64, 0_int64, 0_int64, 1_int64], [2, 2])  ! Identity
        base = mat
        exp = n

        do while (exp > 0)
            if (mod(exp, 2) == 1) then
                result_mat = matmul(result_mat, base)
            end if
            base = matmul(base, base)
            exp = exp / 2
        end do

    end function matrix_power

    ! Tribonacci sequence
    function tribonacci(n) result(trib)
        implicit none
        integer(int32), intent(in) :: n
        integer(int64) :: trib
        integer(int64) :: a, b, c, temp
        integer(int32) :: i

        if (n == 0) then
            trib = 0
        else if (n == 1 .or. n == 2) then
            trib = 1
        else
            a = 0
            b = 1
            c = 1
            do i = 3, n
                trib = a + b + c
                a = b
                b = c
                c = trib
            end do
        end if

    end function tribonacci

    !===========================================================================
    ! Root Finding Methods
    !===========================================================================

    ! Newton-Raphson method
    function newton_raphson(f, df, x0, tol, max_iter) result(root)
        implicit none
        procedure(real_function) :: f, df
        real(real64), intent(in) :: x0, tol
        integer(int32), intent(in) :: max_iter
        real(real64) :: root
        real(real64) :: x, fx, dfx
        integer(int32) :: iter

        x = x0
        do iter = 1, max_iter
            fx = f(x)
            dfx = df(x)

            if (abs(fx) < tol) then
                root = x
                return
            end if

            if (abs(dfx) < EPSILON) then
                root = ieee_value(root, ieee_quiet_nan)
                return
            end if

            x = x - fx / dfx
        end do

        root = x

    end function newton_raphson

    ! Bisection method
    function bisection_method(f, a, b, tol) result(root)
        implicit none
        procedure(real_function) :: f
        real(real64), intent(in) :: a, b, tol
        real(real64) :: root
        real(real64) :: left, right, mid, fa, fb, fmid

        left = a
        right = b
        fa = f(a)
        fb = f(b)

        if (fa * fb > 0) then
            root = ieee_value(root, ieee_quiet_nan)
            return
        end if

        do while (abs(right - left) > tol)
            mid = (left + right) / 2.0_real64
            fmid = f(mid)

            if (abs(fmid) < tol) then
                root = mid
                return
            end if

            if (fa * fmid < 0) then
                right = mid
                fb = fmid
            else
                left = mid
                fa = fmid
            end if
        end do

        root = (left + right) / 2.0_real64

    end function bisection_method

    ! Secant method
    function secant_method(f, x0, x1, tol, max_iter) result(root)
        implicit none
        procedure(real_function) :: f
        real(real64), intent(in) :: x0, x1, tol
        integer(int32), intent(in) :: max_iter
        real(real64) :: root
        real(real64) :: xp, xc, xn, fp, fc
        integer(int32) :: iter

        xp = x0
        xc = x1
        fp = f(xp)
        fc = f(xc)

        do iter = 1, max_iter
            if (abs(fc) < tol) then
                root = xc
                return
            end if

            if (abs(fc - fp) < EPSILON) then
                root = ieee_value(root, ieee_quiet_nan)
                return
            end if

            xn = xc - fc * (xc - xp) / (fc - fp)
            xp = xc
            xc = xn
            fp = fc
            fc = f(xc)
        end do

        root = xc

    end function secant_method

    ! Regula Falsi (False Position) method
    function regula_falsi(f, a, b, tol, max_iter) result(root)
        implicit none
        procedure(real_function) :: f
        real(real64), intent(in) :: a, b, tol
        integer(int32), intent(in) :: max_iter
        real(real64) :: root
        real(real64) :: left, right, c, fa, fb, fc
        integer(int32) :: iter

        left = a
        right = b
        fa = f(a)
        fb = f(b)

        if (fa * fb > 0) then
            root = ieee_value(root, ieee_quiet_nan)
            return
        end if

        do iter = 1, max_iter
            c = (left * fb - right * fa) / (fb - fa)
            fc = f(c)

            if (abs(fc) < tol) then
                root = c
                return
            end if

            if (fa * fc < 0) then
                right = c
                fb = fc
            else
                left = c
                fa = fc
            end if
        end do

        root = c

    end function regula_falsi

    !===========================================================================
    ! Numerical Integration
    !===========================================================================

    ! Trapezoidal rule
    function trapezoidal_integration(f, a, b, n) result(integral)
        implicit none
        procedure(real_function) :: f
        real(real64), intent(in) :: a, b
        integer(int32), intent(in) :: n
        real(real64) :: integral
        real(real64) :: h, x
        integer(int32) :: i

        h = (b - a) / real(n, real64)
        integral = (f(a) + f(b)) / 2.0_real64

        do i = 1, n - 1
            x = a + i * h
            integral = integral + f(x)
        end do

        integral = integral * h

    end function trapezoidal_integration

    ! Simpson's 1/3 rule
    function simpson_integration(f, a, b, n) result(integral)
        implicit none
        procedure(real_function) :: f
        real(real64), intent(in) :: a, b
        integer(int32), intent(in) :: n
        real(real64) :: integral
        real(real64) :: h, x
        integer(int32) :: i, n_even

        ! Ensure n is even
        n_even = n
        if (mod(n_even, 2) == 1) n_even = n_even + 1

        h = (b - a) / real(n_even, real64)
        integral = f(a) + f(b)

        do i = 1, n_even - 1
            x = a + i * h
            if (mod(i, 2) == 1) then
                integral = integral + 4.0_real64 * f(x)
            else
                integral = integral + 2.0_real64 * f(x)
            end if
        end do

        integral = integral * h / 3.0_real64

    end function simpson_integration

    ! Romberg integration
    function romberg_integration(f, a, b, tol, max_iter) result(integral)
        implicit none
        procedure(real_function) :: f
        real(real64), intent(in) :: a, b, tol
        integer(int32), intent(in) :: max_iter
        real(real64) :: integral
        real(real64), dimension(:, :), allocatable :: R
        real(real64) :: h
        integer(int32) :: i, j, k, n

        allocate(R(max_iter, max_iter))

        ! First column using trapezoidal rule
        n = 1
        do i = 1, max_iter
            R(i, 1) = trapezoidal_integration(f, a, b, n)
            n = n * 2

            if (i > 1) then
                ! Richardson extrapolation
                do j = 2, i
                    R(i, j) = (4.0_real64**(j-1) * R(i, j-1) - R(i-1, j-1)) / (4.0_real64**(j-1) - 1.0_real64)
                end do

                ! Check convergence
                if (abs(R(i, i) - R(i-1, i-1)) < tol) then
                    integral = R(i, i)
                    deallocate(R)
                    return
                end if
            end if
        end do

        integral = R(max_iter, max_iter)
        deallocate(R)

    end function romberg_integration

    !===========================================================================
    ! Differential Equation Solvers
    !===========================================================================

    ! Euler's method for ODEs
    subroutine euler_method(f, y0, t0, tf, n, t_out, y_out)
        implicit none
        procedure(ode_function) :: f
        real(real64), intent(in) :: y0, t0, tf
        integer(int32), intent(in) :: n
        real(real64), dimension(n+1), intent(out) :: t_out, y_out
        real(real64) :: h, t, y
        integer(int32) :: i

        h = (tf - t0) / real(n, real64)
        t = t0
        y = y0

        t_out(1) = t
        y_out(1) = y

        do i = 1, n
            y = y + h * f(t, y)
            t = t + h
            t_out(i+1) = t
            y_out(i+1) = y
        end do

    end subroutine euler_method

    ! 4th-order Runge-Kutta method
    subroutine runge_kutta4(f, y0, t0, tf, n, t_out, y_out)
        implicit none
        procedure(ode_function) :: f
        real(real64), intent(in) :: y0, t0, tf
        integer(int32), intent(in) :: n
        real(real64), dimension(n+1), intent(out) :: t_out, y_out
        real(real64) :: h, t, y, k1, k2, k3, k4
        integer(int32) :: i

        h = (tf - t0) / real(n, real64)
        t = t0
        y = y0

        t_out(1) = t
        y_out(1) = y

        do i = 1, n
            k1 = h * f(t, y)
            k2 = h * f(t + h/2.0_real64, y + k1/2.0_real64)
            k3 = h * f(t + h/2.0_real64, y + k2/2.0_real64)
            k4 = h * f(t + h, y + k3)

            y = y + (k1 + 2.0_real64*k2 + 2.0_real64*k3 + k4) / 6.0_real64
            t = t + h

            t_out(i+1) = t
            y_out(i+1) = y
        end do

    end subroutine runge_kutta4

    ! Adams-Bashforth 4-step method
    subroutine adams_bashforth(f, y0, t0, tf, n, t_out, y_out)
        implicit none
        procedure(ode_function) :: f
        real(real64), intent(in) :: y0, t0, tf
        integer(int32), intent(in) :: n
        real(real64), dimension(n+1), intent(out) :: t_out, y_out
        real(real64) :: h, t, y
        real(real64), dimension(4) :: f_vals
        integer(int32) :: i

        h = (tf - t0) / real(n, real64)

        ! Use Runge-Kutta for first 4 steps
        call runge_kutta4(f, y0, t0, t0 + 3*h, 3, t_out(1:4), y_out(1:4))

        ! Store function values
        do i = 1, 4
            f_vals(i) = f(t_out(i), y_out(i))
        end do

        ! Adams-Bashforth for remaining steps
        do i = 4, n
            t = t_out(i)
            y = y_out(i)

            y = y + h * (55.0_real64*f_vals(4) - 59.0_real64*f_vals(3) + &
                        37.0_real64*f_vals(2) - 9.0_real64*f_vals(1)) / 24.0_real64

            t = t + h
            t_out(i+1) = t
            y_out(i+1) = y

            ! Shift function values
            f_vals(1:3) = f_vals(2:4)
            f_vals(4) = f(t, y)
        end do

    end subroutine adams_bashforth

    !===========================================================================
    ! Fast Fourier Transform (FFT)
    !===========================================================================

    ! Cooley-Tukey FFT (radix-2)
    recursive subroutine fft(x, n, inverse)
        implicit none
        complex(real64), dimension(:), intent(inout) :: x
        integer(int32), intent(in) :: n
        logical, intent(in), optional :: inverse
        complex(real64), dimension(:), allocatable :: even, odd
        complex(real64) :: w, wn, t
        integer(int32) :: i, half_n
        logical :: inv

        inv = .false.
        if (present(inverse)) inv = inverse

        if (n <= 1) return

        half_n = n / 2
        allocate(even(half_n), odd(half_n))

        ! Divide
        do i = 1, half_n
            even(i) = x(2*i - 1)
            odd(i) = x(2*i)
        end do

        ! Conquer
        call fft(even, half_n, inv)
        call fft(odd, half_n, inv)

        ! Combine
        if (inv) then
            wn = exp(cmplx(0.0_real64, 2.0_real64 * PI / real(n, real64)))
        else
            wn = exp(cmplx(0.0_real64, -2.0_real64 * PI / real(n, real64)))
        end if

        w = cmplx(1.0_real64, 0.0_real64)

        do i = 1, half_n
            t = w * odd(i)
            x(i) = even(i) + t
            x(i + half_n) = even(i) - t
            w = w * wn
        end do

        deallocate(even, odd)

    end subroutine fft

    ! Inverse FFT
    subroutine ifft(x, n)
        implicit none
        complex(real64), dimension(:), intent(inout) :: x
        integer(int32), intent(in) :: n
        integer(int32) :: i

        call fft(x, n, .true.)

        ! Normalize
        do i = 1, n
            x(i) = x(i) / real(n, real64)
        end do

    end subroutine ifft

    ! Convolution using FFT
    function convolution(a, b, n) result(c)
        implicit none
        real(real64), dimension(:), intent(in) :: a, b
        integer(int32), intent(in) :: n
        real(real64), dimension(n) :: c
        complex(real64), dimension(:), allocatable :: fa, fb, fc
        integer(int32) :: i, fft_size

        ! Find next power of 2
        fft_size = 1
        do while (fft_size < 2 * n - 1)
            fft_size = fft_size * 2
        end do

        allocate(fa(fft_size), fb(fft_size), fc(fft_size))

        ! Convert to complex and pad with zeros
        fa = cmplx(0.0_real64, 0.0_real64)
        fb = cmplx(0.0_real64, 0.0_real64)

        do i = 1, n
            fa(i) = cmplx(a(i), 0.0_real64)
            fb(i) = cmplx(b(i), 0.0_real64)
        end do

        ! FFT
        call fft(fa, fft_size)
        call fft(fb, fft_size)

        ! Multiply in frequency domain
        do i = 1, fft_size
            fc(i) = fa(i) * fb(i)
        end do

        ! Inverse FFT
        call ifft(fc, fft_size)

        ! Extract real part
        do i = 1, n
            c(i) = real(fc(i))
        end do

        deallocate(fa, fb, fc)

    end function convolution

    !===========================================================================
    ! Polynomial Operations
    !===========================================================================

    ! Evaluate polynomial using Horner's method
    function horner_method(coeffs, x) result(y)
        implicit none
        real(real64), dimension(:), intent(in) :: coeffs
        real(real64), intent(in) :: x
        real(real64) :: y
        integer(int32) :: i, n

        n = size(coeffs)
        y = coeffs(n)

        do i = n - 1, 1, -1
            y = y * x + coeffs(i)
        end do

    end function horner_method

    ! Evaluate polynomial (wrapper for Horner's method)
    function polynomial_eval(coeffs, x) result(y)
        implicit none
        real(real64), dimension(:), intent(in) :: coeffs
        real(real64), intent(in) :: x
        real(real64) :: y

        y = horner_method(coeffs, x)

    end function polynomial_eval

    ! Find polynomial roots using companion matrix eigenvalues
    function polynomial_roots(coeffs) result(roots)
        implicit none
        real(real64), dimension(:), intent(in) :: coeffs
        complex(real64), dimension(size(coeffs)-1) :: roots
        real(real64), dimension(:, :), allocatable :: companion
        integer(int32) :: n, i

        n = size(coeffs) - 1
        allocate(companion(n, n))

        ! Build companion matrix
        companion = 0.0_real64
        do i = 1, n - 1
            companion(i + 1, i) = 1.0_real64
        end do

        do i = 1, n
            companion(i, n) = -coeffs(i) / coeffs(n + 1)
        end do

        ! Find eigenvalues (simplified - would need LAPACK for real implementation)
        ! For now, returning placeholder values
        roots = cmplx(0.0_real64, 0.0_real64)

        deallocate(companion)

    end function polynomial_roots

end module numerical_module