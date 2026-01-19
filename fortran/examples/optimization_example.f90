! Example program demonstrating optimization algorithms
program optimization_example
    use iso_fortran_env, only: int32, real64
    use optimization_module
    implicit none

    real(real64) :: x(2), x_min, f_min
    real(real64) :: bounds(2, 2), best_solution(2), best_fitness
    integer :: i

    print '(A)', "========================================"
    print '(A)', "    Optimization Algorithms Examples"
    print '(A)', "========================================"

    ! Example 1: Golden section search (1D optimization)
    print '(A)', ""
    print '(A)', "Example 1: Golden Section Search"
    print '(A)', "---------------------------------"
    print '(A)', "Finding minimum of f(x) = (x-3)^2 + 2"

    call golden_section_search(quadratic_function, 0.0_real64, 10.0_real64, &
                               1e-6_real64, x_min, f_min)

    print '(A,F8.4)', "Minimum at x = ", x_min
    print '(A,F8.4)', "Function value = ", f_min

    ! Example 2: Gradient descent
    print '(A)', ""
    print '(A)', "Example 2: Gradient Descent"
    print '(A)', "----------------------------"
    print '(A)', "Minimizing Rosenbrock function"

    x = [-1.5_real64, 2.5_real64]  ! Starting point
    print '(A,2F8.4)', "Starting point: ", x

    call gradient_descent(rosenbrock_function, rosenbrock_gradient, x, &
                          0.001_real64, 10000, f_min)

    print '(A,2F8.4)', "Minimum found at: ", x
    print '(A,F8.6)', "Function value: ", f_min
    print '(A)', "True minimum is at (1, 1) with f = 0"

    ! Example 3: Nelder-Mead simplex
    print '(A)', ""
    print '(A)', "Example 3: Nelder-Mead Simplex"
    print '(A)', "-------------------------------"
    print '(A)', "Derivative-free optimization of Rosenbrock"

    x = [-1.5_real64, 2.5_real64]  ! Starting point
    call nelder_mead_simplex(rosenbrock_function, x, f_min)

    print '(A,2F8.4)', "Minimum found at: ", x
    print '(A,F8.6)', "Function value: ", f_min

    ! Example 4: Differential Evolution
    print '(A)', ""
    print '(A)', "Example 4: Differential Evolution"
    print '(A)', "----------------------------------"
    print '(A)', "Global optimization of Rastrigin function"

    ! Set bounds for variables
    bounds(:, 1) = -5.12_real64  ! Lower bounds
    bounds(:, 2) = 5.12_real64   ! Upper bounds

    call differential_evolution(rastrigin_function, bounds, 50, 100, &
                                best_solution, best_fitness)

    print '(A,2F8.4)', "Best solution: ", best_solution
    print '(A,F8.6)', "Function value: ", best_fitness
    print '(A)', "Global minimum is at (0, 0) with f = 0"

    ! Example 5: Particle Swarm Optimization
    print '(A)', ""
    print '(A)', "Example 5: Particle Swarm Optimization"
    print '(A)', "---------------------------------------"
    print '(A)', "Another approach to Rastrigin function"

    call particle_swarm_optimization(rastrigin_function, bounds, 30, 100, &
                                      best_solution, best_fitness)

    print '(A,2F8.4)', "Best solution: ", best_solution
    print '(A,F8.6)', "Function value: ", best_fitness

    ! Example 6: Simulated Annealing
    print '(A)', ""
    print '(A)', "Example 6: Simulated Annealing"
    print '(A)', "-------------------------------"
    print '(A)', "Probabilistic optimization"

    best_solution = [2.0_real64, 2.0_real64]  ! Starting point
    call simulated_annealing(sphere_function, best_solution, bounds, best_fitness)

    print '(A,2F8.4)', "Best solution: ", best_solution
    print '(A,F8.6)', "Function value: ", best_fitness

    ! Example 7: Linear Programming
    print '(A)', ""
    print '(A)', "Example 7: Linear Programming (Simplex)"
    print '(A)', "----------------------------------------"
    call demonstrate_linear_programming()

    print '(A)', ""
    print '(A)', "========================================"
    print '(A)', "    Optimization Examples Complete"
    print '(A)', "========================================"

contains

    ! Test functions
    real(real64) function quadratic_function(x)
        real(real64), intent(in) :: x
        quadratic_function = (x - 3.0_real64)**2 + 2.0_real64
    end function quadratic_function

    real(real64) function rosenbrock_function(x)
        real(real64), intent(in) :: x(:)
        rosenbrock_function = 100.0 * (x(2) - x(1)**2)**2 + (1.0 - x(1))**2
    end function rosenbrock_function

    function rosenbrock_gradient(x) result(grad)
        real(real64), intent(in) :: x(:)
        real(real64) :: grad(size(x))
        grad(1) = -400.0 * x(1) * (x(2) - x(1)**2) - 2.0 * (1.0 - x(1))
        grad(2) = 200.0 * (x(2) - x(1)**2)
    end function rosenbrock_gradient

    real(real64) function rastrigin_function(x)
        real(real64), intent(in) :: x(:)
        real(real64), parameter :: PI = 3.14159265359_real64
        integer :: n, i
        n = size(x)
        rastrigin_function = 10.0 * n
        do i = 1, n
            rastrigin_function = rastrigin_function + &
                                  x(i)**2 - 10.0 * cos(2.0 * PI * x(i))
        end do
    end function rastrigin_function

    real(real64) function sphere_function(x)
        real(real64), intent(in) :: x(:)
        sphere_function = sum(x**2)
    end function sphere_function

    subroutine demonstrate_linear_programming()
        real(real64) :: c(3), A(3, 3), b(3)
        real(real64) :: solution(3), optimal_value

        print '(A)', "Maximize: 3x + 5y + 2z"
        print '(A)', "Subject to:"
        print '(A)', "  x + 2y + z <= 10"
        print '(A)', "  2x + y + 3z <= 15"
        print '(A)', "  x + y + z <= 8"
        print '(A)', "  x, y, z >= 0"

        ! Objective function coefficients
        c = [3.0_real64, 5.0_real64, 2.0_real64]

        ! Constraint matrix
        A(1, :) = [1.0_real64, 2.0_real64, 1.0_real64]
        A(2, :) = [2.0_real64, 1.0_real64, 3.0_real64]
        A(3, :) = [1.0_real64, 1.0_real64, 1.0_real64]

        ! Right-hand side
        b = [10.0_real64, 15.0_real64, 8.0_real64]

        call linear_programming_simplex(c, A, b, solution, optimal_value)

        print '(A)', ""
        print '(A)', "Solution:"
        print '(A,F8.4)', "  x = ", solution(1)
        print '(A,F8.4)', "  y = ", solution(2)
        print '(A,F8.4)', "  z = ", solution(3)
        print '(A,F8.4)', "Optimal value: ", optimal_value
    end subroutine demonstrate_linear_programming

end program optimization_example