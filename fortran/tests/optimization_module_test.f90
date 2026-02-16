! Test suite for optimization algorithms module
program test_optimization_module
    use iso_fortran_env, only: int32, real64
    use optimization_module
    implicit none

    integer :: total_tests = 0, passed_tests = 0
    real(real64), parameter :: EPS = 1e-4

    print '(A)', "========================================"
    print '(A)', "    Optimization Module Test Suite"
    print '(A)', "========================================"

    call test_univariate_optimization()
    call test_gradient_based()
    call test_derivative_free()
    call test_metaheuristics()
    call test_linear_programming()

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

    subroutine test_univariate_optimization()
        real(real64) :: x_min, f_min
        real(real64) :: a, b, tol
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Univariate Optimization..."

        ! Test golden section search on f(x) = (x-2)^2
        a = 0.0_real64
        b = 5.0_real64
        tol = 1e-6_real64

        call golden_section_search(quadratic_1d, a, b, tol, x_min, f_min)
        success = abs(x_min - 2.0_real64) < 0.01
        call report_test("Golden section search", success)

        ! Test Newton's method on same function
        x_min = 0.0_real64  ! Starting point
        call newton_method_optimization(quadratic_1d_grad, quadratic_1d_hess, x_min, f_min)
        success = abs(x_min - 2.0_real64) < EPS
        call report_test("Newton's method (1D)", success)

    end subroutine test_univariate_optimization

    subroutine test_gradient_based()
        real(real64) :: x(2), f_min
        real(real64) :: learning_rate
        integer :: max_iter
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Gradient-Based Optimization..."

        ! Test gradient descent on Rosenbrock function
        x = [-1.0_real64, 1.0_real64]
        learning_rate = 0.001_real64
        max_iter = 10000

        call gradient_descent(rosenbrock, rosenbrock_grad, x, learning_rate, max_iter, f_min)
        success = abs(x(1) - 1.0_real64) < 0.1 .and. abs(x(2) - 1.0_real64) < 0.1
        call report_test("Gradient descent", success)

        ! Test conjugate gradient
        x = [-1.0_real64, 1.0_real64]
        call conjugate_gradient_minimize(rosenbrock, rosenbrock_grad, x, f_min)
        success = abs(f_min) < 0.1  ! Rosenbrock minimum is 0
        call report_test("Conjugate gradient", success)

        ! Test BFGS
        x = [-1.0_real64, 1.0_real64]
        call bfgs_minimize(rosenbrock, rosenbrock_grad, x, f_min)
        success = abs(x(1) - 1.0_real64) < 0.01 .and. abs(x(2) - 1.0_real64) < 0.01
        call report_test("BFGS optimization", success)

    end subroutine test_gradient_based

    subroutine test_derivative_free()
        real(real64) :: x(2), f_min
        real(real64) :: simplex(3, 2)
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Derivative-Free Optimization..."

        ! Test Nelder-Mead on Rosenbrock
        x = [0.0_real64, 0.0_real64]
        call nelder_mead_simplex(rosenbrock, x, f_min)
        success = f_min < 0.1
        call report_test("Nelder-Mead simplex", success)

        ! Test on a simpler quadratic function
        x = [3.0_real64, -2.0_real64]
        call nelder_mead_simplex(quadratic_2d, x, f_min)
        success = abs(x(1)) < 0.1 .and. abs(x(2)) < 0.1  ! Minimum at origin
        call report_test("Nelder-Mead (quadratic)", success)

    end subroutine test_derivative_free

    subroutine test_metaheuristics()
        real(real64) :: best_solution(10), best_fitness
        real(real64) :: bounds(10, 2)
        integer :: pop_size, max_iter, i
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Metaheuristic Algorithms..."

        ! Set bounds for all variables
        do i = 1, 10
            bounds(i, 1) = -5.0_real64  ! Lower bound
            bounds(i, 2) = 5.0_real64   ! Upper bound
        end do

        pop_size = 50
        max_iter = 100

        ! Test Differential Evolution
        call differential_evolution(sphere_function, bounds, pop_size, max_iter, &
                                   best_solution, best_fitness)
        success = best_fitness < 1.0  ! Should find near-optimal solution
        call report_test("Differential evolution", success)

        ! Test Particle Swarm Optimization
        call particle_swarm_optimization(sphere_function, bounds, pop_size, max_iter, &
                                         best_solution, best_fitness)
        success = best_fitness < 1.0
        call report_test("Particle swarm optimization", success)

        ! Test Genetic Algorithm
        call genetic_algorithm(sphere_function, bounds, pop_size, max_iter, &
                              best_solution, best_fitness)
        success = best_fitness < 2.0  ! GA might need more iterations
        call report_test("Genetic algorithm", success)

        ! Test Simulated Annealing (single solution)
        best_solution = 2.0_real64  ! Start away from optimum
        call simulated_annealing(sphere_function, best_solution, bounds, &
                                best_fitness)
        success = best_fitness < 5.0
        call report_test("Simulated annealing", success)

        ! Test Tabu Search
        call tabu_search(discrete_function, 100, 20, best_solution(1:1), best_fitness)
        success = best_fitness < 10.0
        call report_test("Tabu search", success)

        ! Test Ant Colony Optimization (for discrete problems)
        call test_aco()

    end subroutine test_metaheuristics

    subroutine test_aco()
        real(real64) :: distances(5, 5), best_tour(5), best_length
        integer :: num_ants, max_iter
        logical :: success

        ! Create a small TSP instance
        distances = 0.0_real64
        distances(1, 2) = 10.0_real64
        distances(1, 3) = 15.0_real64
        distances(1, 4) = 20.0_real64
        distances(1, 5) = 25.0_real64
        distances(2, 3) = 35.0_real64
        distances(2, 4) = 25.0_real64
        distances(2, 5) = 30.0_real64
        distances(3, 4) = 30.0_real64
        distances(3, 5) = 20.0_real64
        distances(4, 5) = 15.0_real64

        ! Make symmetric
        distances = distances + transpose(distances)

        num_ants = 10
        max_iter = 50

        call ant_colony_optimization(distances, num_ants, max_iter, best_tour, best_length)
        success = best_length > 0.0 .and. best_length < 200.0
        call report_test("Ant colony optimization", success)

    end subroutine test_aco

    subroutine test_linear_programming()
        real(real64) :: c(3), A(2, 3), b(2)
        real(real64) :: solution(3), optimal_value
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Linear Programming..."

        ! Maximize: 3x + 2y + z
        ! Subject to:
        !   x + y + z <= 10
        !   2x + y <= 8
        !   x, y, z >= 0

        c = [3.0_real64, 2.0_real64, 1.0_real64]  ! Objective coefficients
        A(1, :) = [1.0_real64, 1.0_real64, 1.0_real64]
        A(2, :) = [2.0_real64, 1.0_real64, 0.0_real64]
        b = [10.0_real64, 8.0_real64]

        call linear_programming_simplex(c, A, b, solution, optimal_value)
        success = optimal_value > 0.0
        call report_test("Simplex method", success)

        ! Test Branch and Bound (for integer programming)
        call test_branch_and_bound()

    end subroutine test_linear_programming

    subroutine test_branch_and_bound()
        real(real64) :: solution(5), value
        logical :: success

        ! Simple knapsack-like problem
        call branch_and_bound(knapsack_objective, 5, solution, value)
        success = value > 0.0
        call report_test("Branch and bound", success)

    end subroutine test_branch_and_bound

    ! Test objective functions
    real(real64) function quadratic_1d(x)
        real(real64), intent(in) :: x
        quadratic_1d = (x - 2.0_real64)**2
    end function quadratic_1d

    real(real64) function quadratic_1d_grad(x)
        real(real64), intent(in) :: x
        quadratic_1d_grad = 2.0_real64 * (x - 2.0_real64)
    end function quadratic_1d_grad

    real(real64) function quadratic_1d_hess(x)
        real(real64), intent(in) :: x
        quadratic_1d_hess = 2.0_real64
    end function quadratic_1d_hess

    real(real64) function quadratic_2d(x)
        real(real64), intent(in) :: x(2)
        quadratic_2d = x(1)**2 + x(2)**2
    end function quadratic_2d

    real(real64) function rosenbrock(x)
        real(real64), intent(in) :: x(:)
        rosenbrock = 100.0 * (x(2) - x(1)**2)**2 + (1.0 - x(1))**2
    end function rosenbrock

    function rosenbrock_grad(x) result(grad)
        real(real64), intent(in) :: x(:)
        real(real64) :: grad(size(x))
        grad(1) = -400.0 * x(1) * (x(2) - x(1)**2) - 2.0 * (1.0 - x(1))
        grad(2) = 200.0 * (x(2) - x(1)**2)
    end function rosenbrock_grad

    real(real64) function sphere_function(x)
        real(real64), intent(in) :: x(:)
        sphere_function = sum(x**2)
    end function sphere_function

    real(real64) function discrete_function(x)
        real(real64), intent(in) :: x(:)
        discrete_function = abs(x(1) - 50.0)
    end function discrete_function

    real(real64) function knapsack_objective(x)
        real(real64), intent(in) :: x(:)
        real(real64) :: weights(5), values(5)
        weights = [2.0, 1.0, 3.0, 2.0, 1.0]
        values = [12.0, 10.0, 20.0, 15.0, 8.0]
        knapsack_objective = sum(x * values) - 1000.0 * max(0.0_real64, sum(x * weights) - 10.0)
    end function knapsack_objective

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

end program test_optimization_module