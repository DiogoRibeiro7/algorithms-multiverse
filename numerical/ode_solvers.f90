! ============================================================================
! Ordinary Differential Equation (ODE) Solvers in Modern Fortran
!
! Comprehensive collection of ODE solving methods:
! - Euler's Method (explicit, first-order)
! - Improved Euler (Heun's Method, second-order)
! - Runge-Kutta 2nd Order (RK2, Midpoint Method)
! - Classical Runge-Kutta 4th Order (RK4)
! - Adaptive Runge-Kutta-Fehlberg (RKF45)
!
! Solves Initial Value Problems (IVPs):
! dy/dt = f(t, y),  y(t₀) = y₀
!
! Fortran has been the language of choice for ODE solving in scientific
! computing for decades!
!
! Compile: gfortran -O3 -o ode_solvers ode_solvers.f90
! Run: ./ode_solvers
!
! @author Algorithms Multiverse
! @version 1.0
! ============================================================================

module ode_module
    implicit none
    private
    public :: euler_method, improved_euler, rk2_method, rk4_method
    public :: rkf45_method, solve_ode
    public :: print_solution

    real(8), parameter :: PI = 3.141592653589793d0

    ! Abstract interface for ODE right-hand side: dy/dt = f(t, y)
    abstract interface
        function ode_func(t, y) result(dydt)
            real(8), intent(in) :: t, y
            real(8) :: dydt
        end function ode_func
    end interface

contains

    ! ========================================================================
    ! EULER'S METHOD
    ! ========================================================================

    subroutine euler_method(f, t0, y0, t_final, n_steps, t, y)
        ! Euler's method (forward Euler, explicit Euler)
        !
        ! Time Complexity: O(n)
        ! Global Error: O(h) where h = step size
        ! Local Error: O(h²)
        !
        ! Formula:
        ! yₙ₊₁ = yₙ + h f(tₙ, yₙ)
        !
        ! Applications:
        ! - Simple, educational purposes
        ! - Quick rough estimates
        ! - Not recommended for production (low accuracy)
        procedure(ode_func) :: f
        real(8), intent(in) :: t0, y0, t_final
        integer, intent(in) :: n_steps
        real(8), intent(out) :: t(n_steps+1), y(n_steps+1)
        real(8) :: h
        integer :: i

        h = (t_final - t0) / real(n_steps, 8)

        t(1) = t0
        y(1) = y0

        do i = 1, n_steps
            t(i+1) = t(i) + h
            y(i+1) = y(i) + h * f(t(i), y(i))
        end do
    end subroutine euler_method

    ! ========================================================================
    ! IMPROVED EULER METHOD (Heun's Method)
    ! ========================================================================

    subroutine improved_euler(f, t0, y0, t_final, n_steps, t, y)
        ! Improved Euler method (Heun's method, RK2)
        !
        ! Time Complexity: O(n)
        ! Global Error: O(h²)
        ! Local Error: O(h³)
        !
        ! Formula:
        ! k₁ = f(tₙ, yₙ)
        ! k₂ = f(tₙ + h, yₙ + h k₁)
        ! yₙ₊₁ = yₙ + h/2 (k₁ + k₂)
        !
        ! Applications:
        ! - Better accuracy than Euler
        ! - Moderate computational cost
        ! - Good for non-stiff problems
        procedure(ode_func) :: f
        real(8), intent(in) :: t0, y0, t_final
        integer, intent(in) :: n_steps
        real(8), intent(out) :: t(n_steps+1), y(n_steps+1)
        real(8) :: h, k1, k2
        integer :: i

        h = (t_final - t0) / real(n_steps, 8)

        t(1) = t0
        y(1) = y0

        do i = 1, n_steps
            k1 = f(t(i), y(i))
            k2 = f(t(i) + h, y(i) + h * k1)

            t(i+1) = t(i) + h
            y(i+1) = y(i) + 0.5d0 * h * (k1 + k2)
        end do
    end subroutine improved_euler

    ! ========================================================================
    ! RUNGE-KUTTA 2ND ORDER (Midpoint Method)
    ! ========================================================================

    subroutine rk2_method(f, t0, y0, t_final, n_steps, t, y)
        ! Runge-Kutta 2nd order (midpoint method)
        !
        ! Time Complexity: O(n)
        ! Global Error: O(h²)
        ! Local Error: O(h³)
        !
        ! Formula:
        ! k₁ = f(tₙ, yₙ)
        ! k₂ = f(tₙ + h/2, yₙ + h/2 k₁)
        ! yₙ₊₁ = yₙ + h k₂
        !
        ! Applications:
        ! - Good balance of accuracy and efficiency
        ! - Standard choice for many applications
        procedure(ode_func) :: f
        real(8), intent(in) :: t0, y0, t_final
        integer, intent(in) :: n_steps
        real(8), intent(out) :: t(n_steps+1), y(n_steps+1)
        real(8) :: h, k1, k2
        integer :: i

        h = (t_final - t0) / real(n_steps, 8)

        t(1) = t0
        y(1) = y0

        do i = 1, n_steps
            k1 = f(t(i), y(i))
            k2 = f(t(i) + 0.5d0*h, y(i) + 0.5d0*h*k1)

            t(i+1) = t(i) + h
            y(i+1) = y(i) + h * k2
        end do
    end subroutine rk2_method

    ! ========================================================================
    ! CLASSICAL RUNGE-KUTTA 4TH ORDER (RK4)
    ! ========================================================================

    subroutine rk4_method(f, t0, y0, t_final, n_steps, t, y)
        ! Classical Runge-Kutta 4th order (RK4)
        !
        ! Time Complexity: O(n)
        ! Global Error: O(h⁴)
        ! Local Error: O(h⁵)
        !
        ! Formula:
        ! k₁ = f(tₙ, yₙ)
        ! k₂ = f(tₙ + h/2, yₙ + h/2 k₁)
        ! k₃ = f(tₙ + h/2, yₙ + h/2 k₂)
        ! k₄ = f(tₙ + h, yₙ + h k₃)
        ! yₙ₊₁ = yₙ + h/6 (k₁ + 2k₂ + 2k₃ + k₄)
        !
        ! Applications:
        ! - Most popular ODE solver
        ! - Excellent accuracy/efficiency tradeoff
        ! - Standard choice for non-stiff ODEs
        ! - Used in physics, engineering, biology
        procedure(ode_func) :: f
        real(8), intent(in) :: t0, y0, t_final
        integer, intent(in) :: n_steps
        real(8), intent(out) :: t(n_steps+1), y(n_steps+1)
        real(8) :: h, k1, k2, k3, k4
        integer :: i

        h = (t_final - t0) / real(n_steps, 8)

        t(1) = t0
        y(1) = y0

        do i = 1, n_steps
            k1 = f(t(i), y(i))
            k2 = f(t(i) + 0.5d0*h, y(i) + 0.5d0*h*k1)
            k3 = f(t(i) + 0.5d0*h, y(i) + 0.5d0*h*k2)
            k4 = f(t(i) + h, y(i) + h*k3)

            t(i+1) = t(i) + h
            y(i+1) = y(i) + (h/6.0d0) * (k1 + 2.0d0*k2 + 2.0d0*k3 + k4)
        end do
    end subroutine rk4_method

    ! ========================================================================
    ! RUNGE-KUTTA-FEHLBERG (RKF45) - ADAPTIVE STEP SIZE
    ! ========================================================================

    subroutine rkf45_method(f, t0, y0, t_final, tol, t, y, n_points)
        ! Runge-Kutta-Fehlberg adaptive method (RKF45)
        !
        ! Time Complexity: O(n) with adaptive n
        ! Global Error: O(h⁴) to O(h⁵)
        !
        ! Features:
        ! - Automatic step size control
        ! - Error estimation at each step
        ! - Adapts to function behavior
        !
        ! Applications:
        ! - When error control is critical
        ! - Functions with varying rates of change
        ! - Production-quality ODE solving
        procedure(ode_func) :: f
        real(8), intent(in) :: t0, y0, t_final, tol
        real(8), intent(out) :: t(:), y(:)
        integer, intent(out) :: n_points
        real(8) :: h, t_curr, y_curr, y_new_4, y_new_5, error
        real(8) :: k1, k2, k3, k4, k5, k6
        real(8), parameter :: h_min = 1.0d-10
        real(8), parameter :: h_max = 0.1d0
        real(8), parameter :: safety = 0.9d0
        integer :: max_size

        max_size = size(t)
        h = 0.01d0  ! Initial step size
        t_curr = t0
        y_curr = y0
        n_points = 1

        t(1) = t0
        y(1) = y0

        do while (t_curr < t_final .and. n_points < max_size)
            ! Ensure we don't overshoot
            if (t_curr + h > t_final) h = t_final - t_curr

            ! RKF45 coefficients
            k1 = h * f(t_curr, y_curr)
            k2 = h * f(t_curr + h/4.0d0, y_curr + k1/4.0d0)
            k3 = h * f(t_curr + 3.0d0*h/8.0d0, y_curr + 3.0d0*k1/32.0d0 + 9.0d0*k2/32.0d0)
            k4 = h * f(t_curr + 12.0d0*h/13.0d0, &
                      y_curr + 1932.0d0*k1/2197.0d0 - 7200.0d0*k2/2197.0d0 + 7296.0d0*k3/2197.0d0)
            k5 = h * f(t_curr + h, &
                      y_curr + 439.0d0*k1/216.0d0 - 8.0d0*k2 + 3680.0d0*k3/513.0d0 - 845.0d0*k4/4104.0d0)
            k6 = h * f(t_curr + h/2.0d0, &
                      y_curr - 8.0d0*k1/27.0d0 + 2.0d0*k2 - 3544.0d0*k3/2565.0d0 + 1859.0d0*k4/4104.0d0 - 11.0d0*k5/40.0d0)

            ! 4th order estimate
            y_new_4 = y_curr + 25.0d0*k1/216.0d0 + 1408.0d0*k3/2565.0d0 + 2197.0d0*k4/4104.0d0 - k5/5.0d0

            ! 5th order estimate
            y_new_5 = y_curr + 16.0d0*k1/135.0d0 + 6656.0d0*k3/12825.0d0 + 28561.0d0*k4/56430.0d0 - 9.0d0*k5/50.0d0 + 2.0d0*k6/55.0d0

            ! Error estimate
            error = abs(y_new_5 - y_new_4)

            if (error < tol .or. h < h_min) then
                ! Accept step
                t_curr = t_curr + h
                y_curr = y_new_5  ! Use more accurate estimate
                n_points = n_points + 1
                t(n_points) = t_curr
                y(n_points) = y_curr
            end if

            ! Adjust step size
            if (error > 0.0d0) then
                h = safety * h * (tol / error)**0.2d0
                h = max(h_min, min(h_max, h))
            end if
        end do
    end subroutine rkf45_method

    ! ========================================================================
    ! GENERIC ODE SOLVER
    ! ========================================================================

    subroutine solve_ode(f, t0, y0, t_final, method, n_steps, t, y)
        ! Generic ODE solver interface
        procedure(ode_func) :: f
        real(8), intent(in) :: t0, y0, t_final
        character(len=*), intent(in) :: method
        integer, intent(in) :: n_steps
        real(8), intent(out) :: t(n_steps+1), y(n_steps+1)

        select case(trim(method))
        case('euler')
            call euler_method(f, t0, y0, t_final, n_steps, t, y)
        case('heun', 'improved_euler')
            call improved_euler(f, t0, y0, t_final, n_steps, t, y)
        case('rk2', 'midpoint')
            call rk2_method(f, t0, y0, t_final, n_steps, t, y)
        case('rk4')
            call rk4_method(f, t0, y0, t_final, n_steps, t, y)
        case default
            print *, 'Unknown method, using RK4'
            call rk4_method(f, t0, y0, t_final, n_steps, t, y)
        end select
    end subroutine solve_ode

    ! ========================================================================
    ! UTILITY FUNCTIONS
    ! ========================================================================

    subroutine print_solution(t, y, n, name)
        ! Print solution in tabular format
        real(8), intent(in) :: t(:), y(:)
        integer, intent(in) :: n
        character(len=*), intent(in) :: name
        integer :: i, step

        print *, ''
        print '(A)', trim(name)
        print '(A)', repeat('-', 60)
        print '(A)', '    t          y(t)'
        print '(A)', repeat('-', 60)

        ! Print every nth point to avoid clutter
        step = max(1, n / 10)
        do i = 1, n, step
            write(*, '(F8.4, 4X, F12.6)') t(i), y(i)
        end do

        ! Always print final point
        if (mod(n-1, step) /= 0) then
            write(*, '(F8.4, 4X, F12.6)') t(n), y(n)
        end if
    end subroutine print_solution

end module ode_module

! ============================================================================
! Main Program - Examples and Tests
! ============================================================================

program ode_demo
    use ode_module
    implicit none

    print '(A)', repeat('=', 70)
    print '(A)', '           ODE SOLVERS IN FORTRAN'
    print '(A)', repeat('=', 70)
    print *

    call example_exponential_decay()
    call example_oscillator()
    call example_adaptive()
    call comparison_accuracy()

contains

    ! ========================================================================
    ! Example 1: Exponential Decay
    ! ========================================================================

    function exponential_decay(t, y) result(dydt)
        real(8), intent(in) :: t, y
        real(8) :: dydt
        real(8), parameter :: lambda = -0.5d0
        dydt = lambda * y
    end function exponential_decay

    subroutine example_exponential_decay()
        integer, parameter :: n = 100
        real(8) :: t(n+1), y(n+1)

        print '(A)', 'Example 1: Exponential Decay'
        print '(A)', 'ODE: dy/dt = -0.5 y,  y(0) = 1'
        print '(A)', 'Exact solution: y(t) = exp(-0.5 t)'
        print '(A)', repeat('=', 70)

        call rk4_method(exponential_decay, 0.0d0, 1.0d0, 10.0d0, n, t, y)
        call print_solution(t, y, n+1, 'RK4 Solution')

        print *, ''
        print '(A, F12.8)', 'RK4 at t=10:    ', y(n+1)
        print '(A, F12.8)', 'Exact at t=10:  ', exp(-0.5d0 * 10.0d0)
        print '(A, E12.4)', 'Error:          ', abs(y(n+1) - exp(-0.5d0 * 10.0d0))
    end subroutine example_exponential_decay

    ! ========================================================================
    ! Example 2: Harmonic Oscillator
    ! ========================================================================

    function harmonic_oscillator(t, y) result(dydt)
        ! This is a simplified 1D representation
        ! For full oscillator, need system of ODEs
        real(8), intent(in) :: t, y
        real(8) :: dydt
        dydt = cos(t)  ! Simplified
    end function harmonic_oscillator

    subroutine example_oscillator()
        integer, parameter :: n = 200
        real(8) :: t(n+1), y(n+1)

        print *
        print *
        print '(A)', 'Example 2: Oscillatory System'
        print '(A)', 'ODE: dy/dt = cos(t),  y(0) = 0'
        print '(A)', 'Exact solution: y(t) = sin(t)'
        print '(A)', repeat('=', 70)

        call rk4_method(harmonic_oscillator, 0.0d0, 0.0d0, 2.0d0*PI, n, t, y)
        call print_solution(t, y, n+1, 'RK4 Solution')

        print *, ''
        print '(A, F12.8)', 'RK4 at t=2π:    ', y(n+1)
        print '(A, F12.8)', 'Exact at t=2π:  ', sin(2.0d0 * PI)
        print '(A, E12.4)', 'Error:          ', abs(y(n+1) - sin(2.0d0 * PI))
    end subroutine example_oscillator

    ! ========================================================================
    ! Example 3: Adaptive Method
    ! ========================================================================

    function stiff_ode(t, y) result(dydt)
        real(8), intent(in) :: t, y
        real(8) :: dydt
        dydt = -100.0d0 * y + 100.0d0 * sin(t)
    end function stiff_ode

    subroutine example_adaptive()
        integer, parameter :: max_points = 1000
        real(8) :: t(max_points), y(max_points)
        integer :: n_points

        print *
        print *
        print '(A)', 'Example 3: Adaptive RKF45 Method'
        print '(A)', 'ODE: dy/dt = -100y + 100sin(t),  y(0) = 0'
        print '(A)', repeat('=', 70)

        call rkf45_method(stiff_ode, 0.0d0, 0.0d0, 1.0d0, 1.0d-6, t, y, n_points)

        print *, ''
        print '(A, I0)', 'Number of adaptive steps: ', n_points
        print '(A, F12.8)', 'Solution at t=1: ', y(n_points)
        call print_solution(t, y, n_points, 'RKF45 Solution (adaptive steps)')
    end subroutine example_adaptive

    ! ========================================================================
    ! Accuracy Comparison
    ! ========================================================================

    subroutine comparison_accuracy()
        integer, parameter :: n = 100
        real(8) :: t1(n+1), y1(n+1)
        real(8) :: t2(n+1), y2(n+1)
        real(8) :: t3(n+1), y3(n+1)
        real(8) :: t4(n+1), y4(n+1)
        real(8) :: exact

        print *
        print *
        print '(A)', 'Accuracy Comparison (dy/dt = -0.5y, y(0)=1, t=5)'
        print '(A)', repeat('=', 70)

        exact = exp(-0.5d0 * 5.0d0)

        call euler_method(exponential_decay, 0.0d0, 1.0d0, 5.0d0, n, t1, y1)
        call improved_euler(exponential_decay, 0.0d0, 1.0d0, 5.0d0, n, t2, y2)
        call rk2_method(exponential_decay, 0.0d0, 1.0d0, 5.0d0, n, t3, y3)
        call rk4_method(exponential_decay, 0.0d0, 1.0d0, 5.0d0, n, t4, y4)

        print *, ''
        print '(A)', 'Method              y(5)         Error       Order'
        print '(A)', repeat('-', 70)
        print '(A, F12.8, 2X, E12.4, 2X, A)', 'Exact:          ', exact, 0.0d0, '    -'
        print '(A, F12.8, 2X, E12.4, 2X, A)', 'Euler:          ', y1(n+1), abs(y1(n+1)-exact), '  O(h)'
        print '(A, F12.8, 2X, E12.4, 2X, A)', 'Improved Euler: ', y2(n+1), abs(y2(n+1)-exact), ' O(h²)'
        print '(A, F12.8, 2X, E12.4, 2X, A)', 'RK2:            ', y3(n+1), abs(y3(n+1)-exact), ' O(h²)'
        print '(A, F12.8, 2X, E12.4, 2X, A)', 'RK4:            ', y4(n+1), abs(y4(n+1)-exact), ' O(h⁴)'

        print *
        print '(A)', repeat('=', 70)
        print '(A)', 'Summary:'
        print '(A)', '- RK4 is the workhorse for most applications'
        print '(A)', '- RKF45 provides automatic error control (adaptive)'
        print '(A)', '- Euler is simple but inaccurate (educational only)'
        print '(A)', '- For stiff ODEs, use implicit methods (BDF, etc.)'
        print '(A)', repeat('=', 70)
    end subroutine comparison_accuracy

end program ode_demo
