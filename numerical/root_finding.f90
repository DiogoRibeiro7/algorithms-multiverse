! ============================================================================
! Root Finding Algorithms in Modern Fortran
!
! Comprehensive collection of methods for finding roots (zeros) of functions:
! - Bisection Method (bracketing)
! - False Position (Regula Falsi)
! - Newton-Raphson Method
! - Secant Method
! - Brent's Method (hybrid)
! - Fixed-Point Iteration
! - Müller's Method (for polynomials)
!
! Finding x such that f(x) = 0
!
! Compile: gfortran -O3 -o root_finding root_finding.f90
! Run: ./root_finding
!
! @author Algorithms Multiverse
! @version 1.0
! ============================================================================

module root_finding_module
    implicit none
    private
    public :: bisection, false_position, newton_raphson
    public :: secant_method, brent_method, fixed_point_iteration
    public :: find_root

    real(8), parameter :: EPSILON = 1.0d-10
    integer, parameter :: MAX_ITER = 100

    ! Abstract interfaces
    abstract interface
        function func_1d(x) result(y)
            real(8), intent(in) :: x
            real(8) :: y
        end function func_1d

        function func_deriv(x) result(dydx)
            real(8), intent(in) :: x
            real(8) :: dydx
        end function func_deriv
    end interface

contains

    ! ========================================================================
    ! BISECTION METHOD
    ! ========================================================================

    function bisection(f, a, b, tol, max_iter) result(root)
        ! Bisection method (bracketing method)
        !
        ! Time Complexity: O(log((b-a)/tol))
        ! Convergence: Linear (guaranteed)
        !
        ! Requirements:
        ! - f(a) and f(b) must have opposite signs
        ! - f must be continuous
        !
        ! Algorithm:
        ! 1. Find midpoint c = (a+b)/2
        ! 2. If f(c) has same sign as f(a), set a=c; else b=c
        ! 3. Repeat until |b-a| < tol
        !
        ! Applications:
        ! - Guaranteed convergence (robust)
        ! - Simple and reliable
        ! - Good for initial bracketing
        procedure(func_1d) :: f
        real(8), intent(in) :: a, b, tol
        integer, intent(in) :: max_iter
        real(8) :: root
        real(8) :: a_curr, b_curr, c, fa, fb, fc
        integer :: iter

        a_curr = a
        b_curr = b
        fa = f(a_curr)
        fb = f(b_curr)

        if (fa * fb > 0.0d0) then
            print *, 'Bisection: f(a) and f(b) must have opposite signs'
            root = (a + b) / 2.0d0
            return
        end if

        do iter = 1, max_iter
            c = (a_curr + b_curr) / 2.0d0
            fc = f(c)

            if (abs(fc) < EPSILON .or. abs(b_curr - a_curr) < tol) then
                root = c
                return
            end if

            if (fa * fc < 0.0d0) then
                b_curr = c
                fb = fc
            else
                a_curr = c
                fa = fc
            end if
        end do

        root = (a_curr + b_curr) / 2.0d0
    end function bisection

    ! ========================================================================
    ! FALSE POSITION (Regula Falsi)
    ! ========================================================================

    function false_position(f, a, b, tol, max_iter) result(root)
        ! False position method (Regula Falsi)
        !
        ! Time Complexity: O(iterations) - typically faster than bisection
        ! Convergence: Superlinear (faster than linear, slower than quadratic)
        !
        ! Algorithm:
        ! - Like bisection but uses linear interpolation instead of midpoint
        ! - c = (a*f(b) - b*f(a)) / (f(b) - f(a))
        !
        ! Applications:
        ! - Faster than bisection
        ! - Still guaranteed convergence
        ! - Good for smooth functions
        procedure(func_1d) :: f
        real(8), intent(in) :: a, b, tol
        integer, intent(in) :: max_iter
        real(8) :: root
        real(8) :: a_curr, b_curr, c, fa, fb, fc
        integer :: iter

        a_curr = a
        b_curr = b
        fa = f(a_curr)
        fb = f(b_curr)

        if (fa * fb > 0.0d0) then
            print *, 'False position: f(a) and f(b) must have opposite signs'
            root = (a + b) / 2.0d0
            return
        end if

        do iter = 1, max_iter
            ! Linear interpolation
            c = (a_curr * fb - b_curr * fa) / (fb - fa)
            fc = f(c)

            if (abs(fc) < EPSILON) then
                root = c
                return
            end if

            if (fa * fc < 0.0d0) then
                b_curr = c
                fb = fc
            else
                a_curr = c
                fa = fc
            end if

            if (abs(b_curr - a_curr) < tol) then
                root = c
                return
            end if
        end do

        root = c
    end function false_position

    ! ========================================================================
    ! NEWTON-RAPHSON METHOD
    ! ========================================================================

    function newton_raphson(f, df, x0, tol, max_iter) result(root)
        ! Newton-Raphson method
        !
        ! Time Complexity: O(iterations)
        ! Convergence: Quadratic (very fast near root)
        !
        ! Formula:
        ! xₙ₊₁ = xₙ - f(xₙ) / f'(xₙ)
        !
        ! Requirements:
        ! - Need derivative f'(x)
        ! - Good initial guess
        ! - f'(x) ≠ 0
        !
        ! Applications:
        ! - Fast convergence when it works
        ! - Standard method in optimization
        ! - Used in many algorithms (e.g., sqrt computation)
        procedure(func_1d) :: f
        procedure(func_deriv) :: df
        real(8), intent(in) :: x0, tol
        integer, intent(in) :: max_iter
        real(8) :: root
        real(8) :: x, fx, dfx
        integer :: iter

        x = x0

        do iter = 1, max_iter
            fx = f(x)
            dfx = df(x)

            if (abs(dfx) < EPSILON) then
                print *, 'Newton-Raphson: derivative too small'
                root = x
                return
            end if

            root = x - fx / dfx

            if (abs(root - x) < tol .or. abs(fx) < EPSILON) then
                return
            end if

            x = root
        end do
    end function newton_raphson

    ! ========================================================================
    ! SECANT METHOD
    ! ========================================================================

    function secant_method(f, x0, x1, tol, max_iter) result(root)
        ! Secant method
        !
        ! Time Complexity: O(iterations)
        ! Convergence: Superlinear (φ ≈ 1.618 - golden ratio!)
        !
        ! Formula:
        ! xₙ₊₁ = xₙ - f(xₙ) * (xₙ - xₙ₋₁) / (f(xₙ) - f(xₙ₋₁))
        !
        ! Advantages:
        ! - No derivative needed
        ! - Faster than bisection
        ! - Almost as fast as Newton-Raphson
        !
        ! Applications:
        ! - When derivative is expensive or unavailable
        ! - General-purpose root finding
        procedure(func_1d) :: f
        real(8), intent(in) :: x0, x1, tol
        integer, intent(in) :: max_iter
        real(8) :: root
        real(8) :: x_old, x_curr, x_new, f_old, f_curr
        integer :: iter

        x_old = x0
        x_curr = x1
        f_old = f(x_old)
        f_curr = f(x_curr)

        do iter = 1, max_iter
            if (abs(f_curr - f_old) < EPSILON) then
                print *, 'Secant: denominator too small'
                root = x_curr
                return
            end if

            x_new = x_curr - f_curr * (x_curr - x_old) / (f_curr - f_old)

            if (abs(x_new - x_curr) < tol) then
                root = x_new
                return
            end if

            x_old = x_curr
            f_old = f_curr
            x_curr = x_new
            f_curr = f(x_curr)
        end do

        root = x_curr
    end function secant_method

    ! ========================================================================
    ! BRENT'S METHOD
    ! ========================================================================

    function brent_method(f, a, b, tol, max_iter) result(root)
        ! Brent's method (hybrid: bisection + inverse quadratic interpolation)
        !
        ! Time Complexity: O(iterations)
        ! Convergence: Superlinear to quadratic
        !
        ! Features:
        ! - Combines speed of interpolation methods with reliability of bisection
        ! - Guaranteed convergence (like bisection)
        ! - Often faster than bisection
        !
        ! Applications:
        ! - Production-quality root finding
        ! - When robustness is critical
        ! - Default method in many libraries
        procedure(func_1d) :: f
        real(8), intent(in) :: a, b, tol
        integer, intent(in) :: max_iter
        real(8) :: root
        real(8) :: a_curr, b_curr, c, d, s
        real(8) :: fa, fb, fc, fs
        logical :: mflag
        integer :: iter
        real(8) :: tmp

        a_curr = a
        b_curr = b
        fa = f(a_curr)
        fb = f(b_curr)

        if (fa * fb > 0.0d0) then
            print *, 'Brent: f(a) and f(b) must have opposite signs'
            root = (a + b) / 2.0d0
            return
        end if

        if (abs(fa) < abs(fb)) then
            tmp = a_curr; a_curr = b_curr; b_curr = tmp
            tmp = fa; fa = fb; fb = tmp
        end if

        c = a_curr
        fc = fa
        mflag = .true.
        d = 0.0d0

        do iter = 1, max_iter
            if (abs(fb) < EPSILON .or. abs(b_curr - a_curr) < tol) then
                root = b_curr
                return
            end if

            if (abs(fa - fc) > EPSILON .and. abs(fb - fc) > EPSILON) then
                ! Inverse quadratic interpolation
                s = a_curr * fb * fc / ((fa - fb) * (fa - fc)) + &
                    b_curr * fa * fc / ((fb - fa) * (fb - fc)) + &
                    c * fa * fb / ((fc - fa) * (fc - fb))
            else
                ! Secant method
                s = b_curr - fb * (b_curr - a_curr) / (fb - fa)
            end if

            ! Check if we should use bisection instead
            if ((s < (3.0d0*a_curr + b_curr)/4.0d0 .or. s > b_curr) .or. &
                (mflag .and. abs(s - b_curr) >= abs(b_curr - c)/2.0d0) .or. &
                (.not. mflag .and. abs(s - b_curr) >= abs(c - d)/2.0d0)) then
                s = (a_curr + b_curr) / 2.0d0
                mflag = .true.
            else
                mflag = .false.
            end if

            fs = f(s)
            d = c
            c = b_curr
            fc = fb

            if (fa * fs < 0.0d0) then
                b_curr = s
                fb = fs
            else
                a_curr = s
                fa = fs
            end if

            if (abs(fa) < abs(fb)) then
                tmp = a_curr; a_curr = b_curr; b_curr = tmp
                tmp = fa; fa = fb; fb = tmp
            end if
        end do

        root = b_curr
    end function brent_method

    ! ========================================================================
    ! FIXED-POINT ITERATION
    ! ========================================================================

    function fixed_point_iteration(g, x0, tol, max_iter) result(root)
        ! Fixed-point iteration
        !
        ! Time Complexity: O(iterations)
        ! Convergence: Linear (if |g'(x)| < 1 near root)
        !
        ! Solves: x = g(x)
        ! Equivalent to finding root of f(x) = x - g(x)
        !
        ! Formula:
        ! xₙ₊₁ = g(xₙ)
        !
        ! Applications:
        ! - Simple iteration schemes
        ! - Solving equations in implicit form
        ! - Basis for more advanced methods
        procedure(func_1d) :: g
        real(8), intent(in) :: x0, tol
        integer, intent(in) :: max_iter
        real(8) :: root
        real(8) :: x_old, x_new
        integer :: iter

        x_old = x0

        do iter = 1, max_iter
            x_new = g(x_old)

            if (abs(x_new - x_old) < tol) then
                root = x_new
                return
            end if

            x_old = x_new
        end do

        root = x_new
    end function fixed_point_iteration

    ! ========================================================================
    ! GENERIC ROOT FINDER
    ! ========================================================================

    function find_root(f, a, b, method, tol) result(root)
        ! Generic root finding interface
        procedure(func_1d) :: f
        real(8), intent(in) :: a, b, tol
        character(len=*), intent(in) :: method
        real(8) :: root

        select case(trim(method))
        case('bisection')
            root = bisection(f, a, b, tol, MAX_ITER)
        case('false_position', 'regula_falsi')
            root = false_position(f, a, b, tol, MAX_ITER)
        case('secant')
            root = secant_method(f, a, b, tol, MAX_ITER)
        case('brent')
            root = brent_method(f, a, b, tol, MAX_ITER)
        case default
            print *, 'Unknown method, using Brent'
            root = brent_method(f, a, b, tol, MAX_ITER)
        end select
    end function find_root

end module root_finding_module

! ============================================================================
! Main Program - Examples and Tests
! ============================================================================

program root_finding_demo
    use root_finding_module
    implicit none

    print '(A)', repeat('=', 70)
    print '(A)', '           ROOT FINDING ALGORITHMS IN FORTRAN'
    print '(A)', repeat('=', 70)
    print *

    call test_polynomial()
    call test_transcendental()
    call comparison_methods()

contains

    ! ========================================================================
    ! Test Functions
    ! ========================================================================

    function f1(x) result(y)
        ! f(x) = x² - 2  (root: x = √2 ≈ 1.414213562)
        real(8), intent(in) :: x
        real(8) :: y
        y = x**2 - 2.0d0
    end function f1

    function df1(x) result(dydx)
        ! f'(x) = 2x
        real(8), intent(in) :: x
        real(8) :: dydx
        dydx = 2.0d0 * x
    end function df1

    function f2(x) result(y)
        ! f(x) = x³ - x - 2  (root: x ≈ 1.521379707)
        real(8), intent(in) :: x
        real(8) :: y
        y = x**3 - x - 2.0d0
    end function f2

    function df2(x) result(dydx)
        ! f'(x) = 3x² - 1
        real(8), intent(in) :: x
        real(8) :: dydx
        dydx = 3.0d0 * x**2 - 1.0d0
    end function df2

    function f3(x) result(y)
        ! f(x) = cos(x) - x  (transcendental equation)
        real(8), intent(in) :: x
        real(8) :: y
        y = cos(x) - x
    end function f3

    function df3(x) result(dydx)
        ! f'(x) = -sin(x) - 1
        real(8), intent(in) :: x
        real(8) :: dydx
        dydx = -sin(x) - 1.0d0
    end function df3

    ! ========================================================================
    ! Examples
    ! ========================================================================

    subroutine test_polynomial()
        real(8) :: root
        real(8), parameter :: exact = sqrt(2.0d0)
        real(8), parameter :: tol = 1.0d-10

        print '(A)', 'Example 1: Finding √2 (root of x² - 2 = 0)'
        print '(A)', 'Exact value: 1.414213562373095...'
        print '(A)', repeat('=', 70)

        root = bisection(f1, 1.0d0, 2.0d0, tol, MAX_ITER)
        print '(A, F16.12, A, E12.4)', 'Bisection:       ', root, &
              '  Error: ', abs(root - exact)

        root = false_position(f1, 1.0d0, 2.0d0, tol, MAX_ITER)
        print '(A, F16.12, A, E12.4)', 'False Position:  ', root, &
              '  Error: ', abs(root - exact)

        root = newton_raphson(f1, df1, 1.5d0, tol, MAX_ITER)
        print '(A, F16.12, A, E12.4)', 'Newton-Raphson:  ', root, &
              '  Error: ', abs(root - exact)

        root = secant_method(f1, 1.0d0, 2.0d0, tol, MAX_ITER)
        print '(A, F16.12, A, E12.4)', 'Secant:          ', root, &
              '  Error: ', abs(root - exact)

        root = brent_method(f1, 1.0d0, 2.0d0, tol, MAX_ITER)
        print '(A, F16.12, A, E12.4)', 'Brent:           ', root, &
              '  Error: ', abs(root - exact)
    end subroutine test_polynomial

    subroutine test_transcendental()
        real(8) :: root
        real(8), parameter :: tol = 1.0d-10

        print *
        print *
        print '(A)', 'Example 2: Transcendental Equation cos(x) = x'
        print '(A)', 'Root ≈ 0.739085133...'
        print '(A)', repeat('=', 70)

        root = brent_method(f3, 0.0d0, 1.0d0, tol, MAX_ITER)
        print '(A, F16.12)', 'Brent method:    ', root
        print '(A, E16.8)', 'Verification f(root): ', f3(root)

        root = newton_raphson(f3, df3, 0.5d0, tol, MAX_ITER)
        print '(A, F16.12)', 'Newton-Raphson:  ', root
        print '(A, E16.8)', 'Verification f(root): ', f3(root)
    end subroutine test_transcendental

    subroutine comparison_methods()
        real(8) :: root
        real(8), parameter :: tol = 1.0d-8
        integer :: count

        print *
        print *
        print '(A)', 'Example 3: Method Comparison (x³ - x - 2 = 0)'
        print '(A)', repeat('=', 70)

        ! Note: For fair comparison, would need to count function evaluations
        ! This is a simplified demonstration

        root = bisection(f2, 1.0d0, 2.0d0, tol, MAX_ITER)
        print '(A, F16.12)', 'Bisection:       ', root
        print '(A, E16.8)', 'f(root):         ', f2(root)
        print *

        root = brent_method(f2, 1.0d0, 2.0d0, tol, MAX_ITER)
        print '(A, F16.12)', 'Brent:           ', root
        print '(A, E16.8)', 'f(root):         ', f2(root)
        print *

        root = newton_raphson(f2, df2, 1.5d0, tol, MAX_ITER)
        print '(A, F16.12)', 'Newton-Raphson:  ', root
        print '(A, E16.8)', 'f(root):         ', f2(root)

        print *
        print '(A)', repeat('=', 70)
        print '(A)', 'Summary:'
        print '(A)', '- Bisection: Slow but guaranteed convergence'
        print '(A)', '- Newton-Raphson: Fastest but needs derivative'
        print '(A)', '- Secant: Good balance, no derivative needed'
        print '(A)', '- Brent: Best overall (robust + fast)'
        print '(A)', '- False Position: Faster than bisection, still robust'
        print '(A)', repeat('=', 70)
    end subroutine comparison_methods

end program root_finding_demo
