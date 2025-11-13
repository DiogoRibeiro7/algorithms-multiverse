! ============================================================================
! Numerical Integration Methods in Modern Fortran
!
! Comprehensive collection of numerical integration (quadrature) methods:
! - Trapezoidal Rule
! - Simpson's Rule
! - Simpson's 3/8 Rule
! - Romberg Integration
! - Gaussian Quadrature
! - Adaptive Simpson's Method
! - Monte Carlo Integration
!
! These methods numerically approximate definite integrals:
! ∫[a,b] f(x) dx
!
! Compile: gfortran -O3 -o integration integration.f90
! Run: ./integration
!
! @author Algorithms Multiverse
! @version 1.0
! ============================================================================

module integration_module
    implicit none
    private
    public :: trapezoidal_rule, simpsons_rule, simpsons_38_rule
    public :: romberg_integration, gaussian_quadrature
    public :: adaptive_simpson, monte_carlo_integration

    real(8), parameter :: PI = 3.141592653589793d0

    ! Abstract interface for functions to integrate
    abstract interface
        function func_1d(x) result(y)
            real(8), intent(in) :: x
            real(8) :: y
        end function func_1d
    end interface

contains

    ! ========================================================================
    ! TRAPEZOIDAL RULE
    ! ========================================================================

    function trapezoidal_rule(f, a, b, n) result(integral)
        ! Numerical integration using trapezoidal rule
        !
        ! Time Complexity: O(n)
        ! Error: O(h²) where h = (b-a)/n
        !
        ! Formula:
        ! ∫f(x)dx ≈ h/2 [f(a) + 2f(x₁) + 2f(x₂) + ... + 2f(xₙ₋₁) + f(b)]
        !
        ! Applications:
        ! - Simple, robust numerical integration
        ! - First-order approximation
        ! - Works well for smooth functions
        procedure(func_1d) :: f
        real(8), intent(in) :: a, b
        integer, intent(in) :: n
        real(8) :: integral
        real(8) :: h, x, sum_val
        integer :: i

        h = (b - a) / real(n, 8)
        sum_val = 0.5d0 * (f(a) + f(b))

        do i = 1, n-1
            x = a + i * h
            sum_val = sum_val + f(x)
        end do

        integral = h * sum_val
    end function trapezoidal_rule

    ! ========================================================================
    ! SIMPSON'S RULE
    ! ========================================================================

    function simpsons_rule(f, a, b, n) result(integral)
        ! Numerical integration using Simpson's 1/3 rule
        !
        ! Time Complexity: O(n)
        ! Error: O(h⁴) where h = (b-a)/n
        !
        ! Formula:
        ! ∫f(x)dx ≈ h/3 [f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + f(xₙ)]
        !
        ! Note: n must be even
        !
        ! Applications:
        ! - More accurate than trapezoidal rule
        ! - Good for smooth functions
        ! - Standard choice for many applications
        procedure(func_1d) :: f
        real(8), intent(in) :: a, b
        integer, intent(in) :: n
        real(8) :: integral
        real(8) :: h, x, sum_odd, sum_even
        integer :: i, n_adj

        ! Ensure n is even
        n_adj = n
        if (mod(n, 2) /= 0) n_adj = n + 1

        h = (b - a) / real(n_adj, 8)

        sum_odd = 0.0d0
        sum_even = 0.0d0

        ! Odd indices (multiply by 4)
        do i = 1, n_adj-1, 2
            x = a + i * h
            sum_odd = sum_odd + f(x)
        end do

        ! Even indices (multiply by 2)
        do i = 2, n_adj-2, 2
            x = a + i * h
            sum_even = sum_even + f(x)
        end do

        integral = (h / 3.0d0) * (f(a) + 4.0d0 * sum_odd + 2.0d0 * sum_even + f(b))
    end function simpsons_rule

    ! ========================================================================
    ! SIMPSON'S 3/8 RULE
    ! ========================================================================

    function simpsons_38_rule(f, a, b, n) result(integral)
        ! Numerical integration using Simpson's 3/8 rule
        !
        ! Time Complexity: O(n)
        ! Error: O(h⁴)
        !
        ! Formula:
        ! ∫f(x)dx ≈ 3h/8 [f(x₀) + 3f(x₁) + 3f(x₂) + 2f(x₃) + ... + f(xₙ)]
        !
        ! Note: n must be divisible by 3
        !
        ! Applications:
        ! - Alternative to Simpson's 1/3 rule
        ! - Useful when n is naturally divisible by 3
        procedure(func_1d) :: f
        real(8), intent(in) :: a, b
        integer, intent(in) :: n
        real(8) :: integral
        real(8) :: h, x, sum_val
        integer :: i, n_adj

        ! Ensure n is divisible by 3
        n_adj = 3 * (n / 3)
        if (n_adj == 0) n_adj = 3

        h = (b - a) / real(n_adj, 8)
        sum_val = f(a) + f(b)

        do i = 1, n_adj-1
            x = a + i * h
            if (mod(i, 3) == 0) then
                sum_val = sum_val + 2.0d0 * f(x)
            else
                sum_val = sum_val + 3.0d0 * f(x)
            end if
        end do

        integral = (3.0d0 * h / 8.0d0) * sum_val
    end function simpsons_38_rule

    ! ========================================================================
    ! ROMBERG INTEGRATION
    ! ========================================================================

    function romberg_integration(f, a, b, max_iter, tol) result(integral)
        ! Romberg integration using Richardson extrapolation
        !
        ! Time Complexity: O(2^k) where k is number of iterations
        ! Error: Exponentially decreasing with iterations
        !
        ! Algorithm:
        ! 1. Compute trapezoidal estimates with increasing refinement
        ! 2. Apply Richardson extrapolation to eliminate error terms
        ! 3. Continue until convergence
        !
        ! Applications:
        ! - High-accuracy integration
        ! - Adaptive error control
        ! - Smooth functions
        procedure(func_1d) :: f
        real(8), intent(in) :: a, b, tol
        integer, intent(in) :: max_iter
        real(8) :: integral
        real(8) :: R(max_iter, max_iter), h
        integer :: i, j, k, n

        ! R(1,1) = trapezoidal rule with h = b-a
        h = b - a
        R(1,1) = 0.5d0 * h * (f(a) + f(b))

        do i = 2, max_iter
            ! Trapezoidal rule with 2^(i-1) intervals
            n = 2**(i-2)
            h = (b - a) / (2.0d0 * n)

            ! Reuse previous computation
            R(i,1) = 0.5d0 * R(i-1,1)
            do k = 1, n
                R(i,1) = R(i,1) + h * f(a + (2*k - 1) * h)
            end do

            ! Richardson extrapolation
            do j = 2, i
                R(i,j) = R(i,j-1) + (R(i,j-1) - R(i-1,j-1)) / (4.0d0**(j-1) - 1.0d0)
            end do

            ! Check convergence
            if (i > 1) then
                if (abs(R(i,i) - R(i-1,i-1)) < tol) then
                    integral = R(i,i)
                    return
                end if
            end if
        end do

        integral = R(max_iter, max_iter)
    end function romberg_integration

    ! ========================================================================
    ! GAUSSIAN QUADRATURE
    ! ========================================================================

    function gaussian_quadrature(f, a, b, n) result(integral)
        ! Gaussian quadrature (Gauss-Legendre)
        !
        ! Time Complexity: O(n)
        ! Error: O(h^(2n)) - extremely accurate!
        !
        ! Uses optimal points (Gauss points) for maximum accuracy
        !
        ! Applications:
        ! - Highest accuracy per function evaluation
        ! - Polynomial integration (exact for degree ≤ 2n-1)
        ! - Finite element methods
        procedure(func_1d) :: f
        real(8), intent(in) :: a, b
        integer, intent(in) :: n
        real(8) :: integral
        real(8) :: nodes(n), weights(n), x
        integer :: i

        ! Get Gauss-Legendre nodes and weights
        call gauss_legendre_nodes_weights(n, nodes, weights)

        ! Transform from [-1,1] to [a,b]
        integral = 0.0d0
        do i = 1, n
            x = 0.5d0 * ((b - a) * nodes(i) + (b + a))
            integral = integral + weights(i) * f(x)
        end do
        integral = integral * 0.5d0 * (b - a)
    end function gaussian_quadrature

    subroutine gauss_legendre_nodes_weights(n, nodes, weights)
        ! Compute Gauss-Legendre nodes and weights
        ! (Simplified version for n ≤ 5)
        integer, intent(in) :: n
        real(8), intent(out) :: nodes(n), weights(n)

        select case(n)
        case(1)
            nodes(1) = 0.0d0
            weights(1) = 2.0d0
        case(2)
            nodes(1) = -sqrt(1.0d0/3.0d0)
            nodes(2) =  sqrt(1.0d0/3.0d0)
            weights(1) = 1.0d0
            weights(2) = 1.0d0
        case(3)
            nodes(1) = -sqrt(3.0d0/5.0d0)
            nodes(2) = 0.0d0
            nodes(3) =  sqrt(3.0d0/5.0d0)
            weights(1) = 5.0d0/9.0d0
            weights(2) = 8.0d0/9.0d0
            weights(3) = 5.0d0/9.0d0
        case(4)
            nodes(1) = -sqrt((3.0d0 + 2.0d0*sqrt(6.0d0/5.0d0))/7.0d0)
            nodes(2) = -sqrt((3.0d0 - 2.0d0*sqrt(6.0d0/5.0d0))/7.0d0)
            nodes(3) =  sqrt((3.0d0 - 2.0d0*sqrt(6.0d0/5.0d0))/7.0d0)
            nodes(4) =  sqrt((3.0d0 + 2.0d0*sqrt(6.0d0/5.0d0))/7.0d0)
            weights(1) = (18.0d0 - sqrt(30.0d0))/36.0d0
            weights(2) = (18.0d0 + sqrt(30.0d0))/36.0d0
            weights(3) = (18.0d0 + sqrt(30.0d0))/36.0d0
            weights(4) = (18.0d0 - sqrt(30.0d0))/36.0d0
        case default
            ! Use 2-point for n > 4
            nodes(1) = -sqrt(1.0d0/3.0d0)
            nodes(2) =  sqrt(1.0d0/3.0d0)
            weights(1) = 1.0d0
            weights(2) = 1.0d0
        end select
    end subroutine gauss_legendre_nodes_weights

    ! ========================================================================
    ! ADAPTIVE SIMPSON'S METHOD
    ! ========================================================================

    recursive function adaptive_simpson(f, a, b, tol, whole) result(integral)
        ! Adaptive Simpson's method with automatic refinement
        !
        ! Time Complexity: O(n log n) typically
        ! Error: Controlled by tolerance
        !
        ! Algorithm:
        ! 1. Compute Simpson's rule on [a,b]
        ! 2. Compute Simpson's rule on [a,m] and [m,b]
        ! 3. If difference < tolerance, accept; else subdivide
        !
        ! Applications:
        ! - Functions with varying smoothness
        ! - Automatic error control
        ! - Efficient for singular integrands
        procedure(func_1d) :: f
        real(8), intent(in) :: a, b, tol
        real(8), intent(in), optional :: whole
        real(8) :: integral
        real(8) :: m, left, right, S_whole, S_parts, delta
        real(8) :: fa, fb, fm, fleft, fright
        real(8) :: h

        m = (a + b) / 2.0d0
        h = b - a

        fa = f(a)
        fb = f(b)
        fm = f(m)

        if (present(whole)) then
            S_whole = whole
        else
            S_whole = (h / 6.0d0) * (fa + 4.0d0 * fm + fb)
        end if

        ! Compute Simpson's rule on subintervals
        fleft = f((a + m) / 2.0d0)
        fright = f((m + b) / 2.0d0)

        left = (h / 12.0d0) * (fa + 4.0d0 * fleft + fm)
        right = (h / 12.0d0) * (fm + 4.0d0 * fright + fb)
        S_parts = left + right

        delta = S_parts - S_whole

        if (abs(delta) <= 15.0d0 * tol) then
            ! Accept current approximation
            integral = S_parts + delta / 15.0d0
        else
            ! Recursively subdivide
            integral = adaptive_simpson(f, a, m, tol/2.0d0, left) + &
                      adaptive_simpson(f, m, b, tol/2.0d0, right)
        end if
    end function adaptive_simpson

    ! ========================================================================
    ! MONTE CARLO INTEGRATION
    ! ========================================================================

    function monte_carlo_integration(f, a, b, n_samples) result(integral)
        ! Monte Carlo integration using random sampling
        !
        ! Time Complexity: O(n)
        ! Error: O(1/√n) - probabilistic
        !
        ! Algorithm:
        ! 1. Generate random points in [a,b]
        ! 2. Evaluate f at random points
        ! 3. Average: (b-a) * mean(f(x))
        !
        ! Applications:
        ! - High-dimensional integration
        ! - Complex domains
        ! - When other methods fail
        procedure(func_1d) :: f
        real(8), intent(in) :: a, b
        integer, intent(in) :: n_samples
        real(8) :: integral
        real(8) :: x, sum_val
        integer :: i

        sum_val = 0.0d0

        do i = 1, n_samples
            call random_number(x)
            x = a + (b - a) * x
            sum_val = sum_val + f(x)
        end do

        integral = (b - a) * sum_val / real(n_samples, 8)
    end function monte_carlo_integration

end module integration_module

! ============================================================================
! Main Program - Examples and Tests
! ============================================================================

program integration_demo
    use integration_module
    implicit none

    print '(A)', repeat('=', 70)
    print '(A)', '        NUMERICAL INTEGRATION METHODS IN FORTRAN'
    print '(A)', repeat('=', 70)
    print *

    call test_all_methods()
    call compare_methods()

contains

    ! Test functions
    function f1(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = x**2  ! ∫x² dx from 0 to 1 = 1/3
    end function f1

    function f2(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = sin(x)  ! ∫sin(x) dx from 0 to π = 2
    end function f2

    function f3(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = exp(-x**2)  ! Gaussian
    end function f3

    subroutine test_all_methods()
        real(8) :: result
        real(8), parameter :: exact = 1.0d0/3.0d0

        print '(A)', 'Test Function: f(x) = x²'
        print '(A)', 'Exact integral from 0 to 1: 1/3 = 0.333333...'
        print '(A)', repeat('-', 70)

        result = trapezoidal_rule(f1, 0.0d0, 1.0d0, 100)
        print '(A, F12.8, A, E12.4)', 'Trapezoidal (n=100):   ', result, &
              '  Error: ', abs(result - exact)

        result = simpsons_rule(f1, 0.0d0, 1.0d0, 100)
        print '(A, F12.8, A, E12.4)', 'Simpsons 1/3 (n=100):  ', result, &
              '  Error: ', abs(result - exact)

        result = simpsons_38_rule(f1, 0.0d0, 1.0d0, 99)
        print '(A, F12.8, A, E12.4)', 'Simpsons 3/8 (n=99):   ', result, &
              '  Error: ', abs(result - exact)

        result = romberg_integration(f1, 0.0d0, 1.0d0, 10, 1.0d-10)
        print '(A, F12.8, A, E12.4)', 'Romberg:               ', result, &
              '  Error: ', abs(result - exact)

        result = gaussian_quadrature(f1, 0.0d0, 1.0d0, 3)
        print '(A, F12.8, A, E12.4)', 'Gaussian (n=3):        ', result, &
              '  Error: ', abs(result - exact)

        result = adaptive_simpson(f1, 0.0d0, 1.0d0, 1.0d-8)
        print '(A, F12.8, A, E12.4)', 'Adaptive Simpson:      ', result, &
              '  Error: ', abs(result - exact)

        result = monte_carlo_integration(f1, 0.0d0, 1.0d0, 100000)
        print '(A, F12.8, A, E12.4)', 'Monte Carlo (100k):    ', result, &
              '  Error: ', abs(result - exact)
    end subroutine test_all_methods

    subroutine compare_methods()
        real(8) :: result
        real(8), parameter :: exact = 2.0d0

        print *
        print *
        print '(A)', 'Test Function: f(x) = sin(x)'
        print '(A)', 'Exact integral from 0 to π: 2.0'
        print '(A)', repeat('-', 70)

        result = simpsons_rule(f2, 0.0d0, PI, 100)
        print '(A, F12.8, A, E12.4)', 'Simpsons (n=100):      ', result, &
              '  Error: ', abs(result - exact)

        result = gaussian_quadrature(f2, 0.0d0, PI, 3)
        print '(A, F12.8, A, E12.4)', 'Gaussian (n=3):        ', result, &
              '  Error: ', abs(result - exact)

        result = romberg_integration(f2, 0.0d0, PI, 10, 1.0d-10)
        print '(A, F12.8, A, E12.4)', 'Romberg:               ', result, &
              '  Error: ', abs(result - exact)

        print *
        print '(A)', repeat('=', 70)
        print '(A)', 'Summary:'
        print '(A)', '- Trapezoidal: O(h²) error, simple and robust'
        print '(A)', '- Simpsons: O(h⁴) error, good for smooth functions'
        print '(A)', '- Romberg: Exponential convergence, very accurate'
        print '(A)', '- Gaussian: Optimal accuracy per evaluation'
        print '(A)', '- Adaptive: Automatic error control'
        print '(A)', '- Monte Carlo: For high dimensions and complex domains'
        print '(A)', repeat('=', 70)
    end subroutine compare_methods

end program integration_demo
