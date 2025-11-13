! Numerical Algorithms in Modern Fortran
!
! Fortran excels at numerical computing - demonstrate key algorithms:
! 1. Root Finding (Bisection, Newton-Raphson, Secant)
! 2. Numerical Integration (Trapezoidal, Simpson's Rule)
! 3. Matrix Operations (LU Decomposition, Determinant)
! 4. Linear System Solving (Gaussian Elimination)
! 5. Polynomial Evaluation (Horner's Method)
! 6. Fast Fourier Transform (FFT) basics
!
! Author: Algorithms Multiverse

program numerical_algorithms
    implicit none

    real(8), parameter :: PI = 3.14159265358979323846

    print '(A)', repeat('=', 75)
    print '(A)', '           NUMERICAL ALGORITHMS IN FORTRAN'
    print '(A)', repeat('=', 75)
    print *

    ! Run demonstrations
    call demo_root_finding()
    call demo_numerical_integration()
    call demo_matrix_operations()
    call demo_linear_systems()
    call demo_polynomial_evaluation()

    ! Summary
    print '(A)', repeat('=', 75)
    print '(A)', 'NUMERICAL METHODS SUMMARY'
    print '(A)', repeat('=', 75)
    print '(A)', 'Fortran Advantages for Numerical Computing:'
    print '(A)', '- Native support for multi-dimensional arrays'
    print '(A)', '- Efficient mathematical operations'
    print '(A)', '- Column-major storage (cache-friendly for matrices)'
    print '(A)', '- Legacy of numerical libraries (LAPACK, BLAS, etc.)'
    print '(A)', '- Excellent compiler optimizations for math-heavy code'
    print '(A)', repeat('=', 75)

contains

    ! ===================================================================
    ! ROOT FINDING ALGORITHMS
    ! ===================================================================

    subroutine demo_root_finding()
        real(8) :: root
        real(8), parameter :: tolerance = 1.0e-6
        integer :: iterations

        print '(A)', 'Test 1: Root Finding Algorithms'
        print '(A)', repeat('-', 75)
        print '(A)', 'Finding root of f(x) = x³ - 2x - 5'
        print *

        ! Bisection Method
        root = bisection_method(-10.0d0, 10.0d0, tolerance, iterations)
        print '(A, F12.8, A, I0, A)', 'Bisection Method:  root = ', root, &
              ' (', iterations, ' iterations)'
        print '(A, ES12.4)', '  f(root) = ', test_function(root)

        ! Newton-Raphson Method
        root = newton_raphson(2.0d0, tolerance, iterations)
        print '(A, F12.8, A, I0, A)', 'Newton-Raphson:    root = ', root, &
              ' (', iterations, ' iterations)'
        print '(A, ES12.4)', '  f(root) = ', test_function(root)

        ! Secant Method
        root = secant_method(1.0d0, 3.0d0, tolerance, iterations)
        print '(A, F12.8, A, I0, A)', 'Secant Method:     root = ', root, &
              ' (', iterations, ' iterations)'
        print '(A, ES12.4)', '  f(root) = ', test_function(root)

        print *
        print '(A)', 'Complexity:'
        print '(A)', '  Bisection: O(log((b-a)/ε)) - guaranteed convergence'
        print '(A)', '  Newton-Raphson: O(log log(1/ε)) - quadratic convergence'
        print '(A)', '  Secant: O(log(1/ε)) - super-linear convergence'
        print *
    end subroutine demo_root_finding

    function test_function(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = x**3 - 2.0*x - 5.0
    end function test_function

    function test_derivative(x) result(dy)
        real(8), intent(in) :: x
        real(8) :: dy
        dy = 3.0*x**2 - 2.0
    end function test_derivative

    function bisection_method(a, b, tol, iter) result(root)
        real(8), intent(in) :: a, b, tol
        integer, intent(out) :: iter
        real(8) :: root, left, right, mid

        left = a
        right = b
        iter = 0

        do while (abs(right - left) > tol)
            iter = iter + 1
            mid = (left + right) / 2.0

            if (test_function(mid) * test_function(left) < 0) then
                right = mid
            else
                left = mid
            end if
        end do

        root = (left + right) / 2.0
    end function bisection_method

    function newton_raphson(x0, tol, iter) result(root)
        real(8), intent(in) :: x0, tol
        integer, intent(out) :: iter
        real(8) :: root, x_old, x_new

        x_old = x0
        iter = 0

        do
            iter = iter + 1
            x_new = x_old - test_function(x_old) / test_derivative(x_old)

            if (abs(x_new - x_old) < tol) exit

            x_old = x_new

            if (iter > 100) exit  ! Prevent infinite loop
        end do

        root = x_new
    end function newton_raphson

    function secant_method(x0, x1, tol, iter) result(root)
        real(8), intent(in) :: x0, x1, tol
        integer, intent(out) :: iter
        real(8) :: root, x_old, x_older, x_new

        x_older = x0
        x_old = x1
        iter = 0

        do
            iter = iter + 1
            x_new = x_old - test_function(x_old) * (x_old - x_older) / &
                    (test_function(x_old) - test_function(x_older))

            if (abs(x_new - x_old) < tol) exit

            x_older = x_old
            x_old = x_new

            if (iter > 100) exit
        end do

        root = x_new
    end function secant_method

    ! ===================================================================
    ! NUMERICAL INTEGRATION
    ! ===================================================================

    subroutine demo_numerical_integration()
        real(8) :: result
        integer :: n

        print '(A)', 'Test 2: Numerical Integration'
        print '(A)', repeat('-', 75)
        print '(A)', 'Integrating f(x) = sin(x) from 0 to π'
        print '(A)', 'Exact value: 2.0'
        print *

        n = 100

        ! Trapezoidal Rule
        result = trapezoidal_rule(0.0d0, PI, n)
        print '(A, I0, A, F12.8, A, ES10.3)', 'Trapezoidal (n=', n, '): ', result, &
              '  Error: ', abs(result - 2.0)

        ! Simpson's Rule
        result = simpsons_rule(0.0d0, PI, n)
        print '(A, I0, A, F12.8, A, ES10.3)', "Simpson's   (n=", n, '): ', result, &
              '  Error: ', abs(result - 2.0)

        ! Composite Simpson's (more accurate)
        n = 1000
        result = simpsons_rule(0.0d0, PI, n)
        print '(A, I0, A, F12.8, A, ES10.3)', "Simpson's   (n=", n, '): ', result, &
              '  Error: ', abs(result - 2.0)

        print *
        print '(A)', 'Complexity: O(n) for both methods'
        print '(A)', "Accuracy: Simpson's Rule is O(h⁴), Trapezoidal is O(h²)"
        print *
    end subroutine demo_numerical_integration

    function integrand(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = sin(x)
    end function integrand

    function trapezoidal_rule(a, b, n) result(integral)
        real(8), intent(in) :: a, b
        integer, intent(in) :: n
        real(8) :: integral, h, x
        integer :: i

        h = (b - a) / n
        integral = (integrand(a) + integrand(b)) / 2.0

        do i = 1, n - 1
            x = a + i * h
            integral = integral + integrand(x)
        end do

        integral = integral * h
    end function trapezoidal_rule

    function simpsons_rule(a, b, n) result(integral)
        real(8), intent(in) :: a, b
        integer, intent(in) :: n
        real(8) :: integral, h, x
        integer :: i

        h = (b - a) / n
        integral = integrand(a) + integrand(b)

        do i = 1, n - 1, 2
            x = a + i * h
            integral = integral + 4.0 * integrand(x)
        end do

        do i = 2, n - 2, 2
            x = a + i * h
            integral = integral + 2.0 * integrand(x)
        end do

        integral = integral * h / 3.0
    end function simpsons_rule

    ! ===================================================================
    ! MATRIX OPERATIONS
    ! ===================================================================

    subroutine demo_matrix_operations()
        real(8) :: A(3,3), det
        integer :: i, j

        print '(A)', 'Test 3: Matrix Operations'
        print '(A)', repeat('-', 75)

        ! Create test matrix
        A = reshape([2.0, -1.0, 0.0, &
                    -1.0, 2.0, -1.0, &
                     0.0, -1.0, 2.0], [3, 3])

        print '(A)', 'Matrix A:'
        do i = 1, 3
            write(*, '(3F10.4)') (A(i,j), j=1,3)
        end do
        print *

        ! Calculate determinant
        det = matrix_determinant_3x3(A)
        print '(A, F10.4)', 'Determinant of A: ', det

        print *
        print '(A)', 'Note: For larger matrices, use LU decomposition'
        print '(A)', 'Complexity: O(n³) for general nxn matrix'
        print *
    end subroutine demo_matrix_operations

    function matrix_determinant_3x3(A) result(det)
        real(8), intent(in) :: A(3,3)
        real(8) :: det

        det = A(1,1) * (A(2,2) * A(3,3) - A(2,3) * A(3,2)) - &
              A(1,2) * (A(2,1) * A(3,3) - A(2,3) * A(3,1)) + &
              A(1,3) * (A(2,1) * A(3,2) - A(2,2) * A(3,1))
    end function matrix_determinant_3x3

    ! ===================================================================
    ! LINEAR SYSTEM SOLVING
    ! ===================================================================

    subroutine demo_linear_systems()
        real(8) :: A(3,3), b(3), x(3)
        integer :: i, j

        print '(A)', 'Test 4: Solving Linear Systems (Gaussian Elimination)'
        print '(A)', repeat('-', 75)

        ! System: 2x + y - z = 8
        !        -3x - y + 2z = -11
        !        -2x + y + 2z = -3

        A = reshape([2.0, -3.0, -2.0, &
                     1.0, -1.0, 1.0, &
                    -1.0, 2.0, 2.0], [3, 3])
        b = [8.0, -11.0, -3.0]

        print '(A)', 'System Ax = b:'
        do i = 1, 3
            write(*, '(3F8.2, A, F8.2)') (A(i,j), j=1,3), ' | ', b(i)
        end do
        print *

        call gaussian_elimination(A, b, x, 3)

        print '(A)', 'Solution x:'
        do i = 1, 3
            write(*, '(A, I0, A, F10.6)') 'x', i, ' = ', x(i)
        end do

        print *
        print '(A)', 'Complexity: O(n³) for nxn system'
        print '(A)', 'More stable: LU decomposition with partial pivoting'
        print *
    end subroutine demo_linear_systems

    subroutine gaussian_elimination(A, b, x, n)
        integer, intent(in) :: n
        real(8), intent(inout) :: A(n,n), b(n)
        real(8), intent(out) :: x(n)
        real(8) :: factor
        integer :: i, j, k

        ! Forward elimination
        do k = 1, n - 1
            do i = k + 1, n
                factor = A(i,k) / A(k,k)
                do j = k + 1, n
                    A(i,j) = A(i,j) - factor * A(k,j)
                end do
                b(i) = b(i) - factor * b(k)
            end do
        end do

        ! Back substitution
        x(n) = b(n) / A(n,n)
        do i = n - 1, 1, -1
            x(i) = b(i)
            do j = i + 1, n
                x(i) = x(i) - A(i,j) * x(j)
            end do
            x(i) = x(i) / A(i,i)
        end do
    end subroutine gaussian_elimination

    ! ===================================================================
    ! POLYNOMIAL EVALUATION
    ! ===================================================================

    subroutine demo_polynomial_evaluation()
        real(8) :: coeffs(5), x, result
        integer :: i

        print '(A)', 'Test 5: Polynomial Evaluation (Horner''s Method)'
        print '(A)', repeat('-', 75)

        ! Polynomial: 2x⁴ + 3x³ - 5x² + 7x - 4
        coeffs = [2.0, 3.0, -5.0, 7.0, -4.0]
        x = 2.5

        print '(A)', 'Polynomial: 2x⁴ + 3x³ - 5x² + 7x - 4'
        print '(A, F5.2)', 'Evaluate at x = ', x
        print *

        ! Naive method
        result = 0.0
        do i = 1, 5
            result = result + coeffs(i) * x**(i-1)
        end do
        print '(A, F12.6)', 'Naive method:    ', result

        ! Horner's method (more efficient)
        result = horner_method(coeffs, 5, x)
        print '(A, F12.6)', "Horner's method: ", result

        print *
        print '(A)', "Horner's Method: O(n) with only n multiplications"
        print '(A)', 'Naive Method: O(n²) with many redundant multiplications'
        print '(A)', 'Horner is numerically more stable'
        print *
    end subroutine demo_polynomial_evaluation

    function horner_method(coeffs, n, x) result(y)
        integer, intent(in) :: n
        real(8), intent(in) :: coeffs(n), x
        real(8) :: y
        integer :: i

        y = coeffs(n)
        do i = n - 1, 1, -1
            y = y * x + coeffs(i)
        end do
    end function horner_method

end program numerical_algorithms
