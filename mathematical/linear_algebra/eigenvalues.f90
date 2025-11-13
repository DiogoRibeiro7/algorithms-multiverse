! ============================================================================
! Eigenvalue Algorithms in Modern Fortran
!
! Comprehensive eigenvalue/eigenvector computation methods:
! - Power Iteration (dominant eigenvalue)
! - Inverse Power Iteration (smallest eigenvalue)
! - QR Algorithm (all eigenvalues)
! - Jacobi Method (symmetric matrices)
! - Rayleigh Quotient Iteration
!
! Eigenvalue problem: Av = λv
! where λ is eigenvalue, v is eigenvector
!
! Compile: gfortran -O3 -o eigenvalues eigenvalues.f90
! Run: ./eigenvalues
!
! @author Algorithms Multiverse
! @version 1.0
! ============================================================================

module eigenvalue_module
    implicit none
    private
    public :: power_iteration, inverse_power_iteration
    public :: qr_algorithm, jacobi_eigensolve
    public :: rayleigh_quotient_iteration
    public :: print_matrix, print_vector

    real(8), parameter :: EPSILON = 1.0d-10
    integer, parameter :: MAX_ITER = 1000

contains

    ! ========================================================================
    ! POWER ITERATION
    ! ========================================================================

    subroutine power_iteration(A, n, eigenvalue, eigenvector, max_iter, tol)
        ! Find dominant eigenvalue (largest in magnitude) and eigenvector
        !
        ! Time Complexity: O(n² × iterations)
        ! Convergence rate: |λ₂/λ₁| per iteration
        !
        ! Algorithm:
        ! 1. Start with random vector v
        ! 2. Repeat: v = Av / ||Av||
        ! 3. λ = v^T A v (Rayleigh quotient)
        !
        ! Applications:
        ! - Google PageRank
        ! - Principal Component Analysis
        ! - Markov chain stationary distributions
        ! - Network centrality measures
        implicit none
        integer, intent(in) :: n, max_iter
        real(8), intent(in) :: A(n,n), tol
        real(8), intent(out) :: eigenvalue
        real(8), intent(out) :: eigenvector(n)
        integer :: iter, i
        real(8) :: v_new(n), Av(n), norm_val, lambda_old

        ! Initialize with random vector
        call random_number(eigenvector)
        norm_val = sqrt(sum(eigenvector**2))
        eigenvector = eigenvector / norm_val

        eigenvalue = 0.0d0

        do iter = 1, max_iter
            lambda_old = eigenvalue

            ! v_new = A * v
            do i = 1, n
                v_new(i) = sum(A(i,:) * eigenvector)
            end do

            ! Normalize
            norm_val = sqrt(sum(v_new**2))
            if (norm_val < EPSILON) then
                print *, 'Power iteration: zero vector encountered'
                return
            end if
            v_new = v_new / norm_val

            ! Compute Rayleigh quotient: λ = v^T A v
            do i = 1, n
                Av(i) = sum(A(i,:) * v_new)
            end do
            eigenvalue = sum(v_new * Av)

            ! Check convergence
            if (abs(eigenvalue - lambda_old) < tol) exit

            eigenvector = v_new
        end do
    end subroutine power_iteration

    ! ========================================================================
    ! INVERSE POWER ITERATION
    ! ========================================================================

    subroutine inverse_power_iteration(A, n, eigenvalue, eigenvector, max_iter, tol)
        ! Find smallest eigenvalue (in magnitude) and eigenvector
        !
        ! Time Complexity: O(n³) per iteration (solving linear system)
        !
        ! Algorithm:
        ! 1. Solve A x = v for x at each iteration
        ! 2. Normalize x
        ! 3. Eigenvalue of A⁻¹ is 1/λ
        !
        ! Applications:
        ! - Finding lowest energy states in quantum mechanics
        ! - Stability analysis
        ! - Vibration analysis
        implicit none
        integer, intent(in) :: n, max_iter
        real(8), intent(in) :: A(n,n), tol
        real(8), intent(out) :: eigenvalue
        real(8), intent(out) :: eigenvector(n)
        real(8) :: A_copy(n,n), v_new(n), norm_val, lambda_old, Av(n)
        integer :: iter, status, i

        ! Initialize
        call random_number(eigenvector)
        norm_val = sqrt(sum(eigenvector**2))
        eigenvector = eigenvector / norm_val

        eigenvalue = 0.0d0

        do iter = 1, max_iter
            lambda_old = eigenvalue

            ! Solve A * v_new = eigenvector
            A_copy = A
            v_new = eigenvector
            call gaussian_elimination(A_copy, v_new, v_new, n, status)

            if (status /= 0) then
                print *, 'Inverse power iteration: singular matrix'
                return
            end if

            ! Normalize
            norm_val = sqrt(sum(v_new**2))
            v_new = v_new / norm_val

            ! Compute Rayleigh quotient
            do i = 1, n
                Av(i) = sum(A(i,:) * v_new)
            end do
            eigenvalue = sum(v_new * Av)

            ! Check convergence
            if (abs(eigenvalue - lambda_old) < tol) exit

            eigenvector = v_new
        end do
    end subroutine inverse_power_iteration

    ! ========================================================================
    ! QR ALGORITHM
    ! ========================================================================

    subroutine qr_algorithm(A, n, eigenvalues, max_iter, tol)
        ! Find all eigenvalues using QR algorithm
        !
        ! Time Complexity: O(n³) per iteration
        !
        ! Algorithm:
        ! 1. Factor A = QR (QR decomposition)
        ! 2. Form A_new = RQ
        ! 3. Repeat until diagonal converges
        ! 4. Eigenvalues appear on diagonal
        !
        ! Applications:
        ! - Finding all eigenvalues simultaneously
        ! - Symmetric eigenvalue problems
        ! - Schur decomposition
        implicit none
        integer, intent(in) :: n, max_iter
        real(8), intent(in) :: A(n,n), tol
        real(8), intent(out) :: eigenvalues(n)
        real(8) :: B(n,n), Q(n,n), R(n,n), off_norm, prev_off_norm
        integer :: iter, status, i

        B = A
        prev_off_norm = huge(1.0d0)

        do iter = 1, max_iter
            ! QR decomposition of B
            call qr_decomposition(B, n, n, Q, R, status)

            if (status /= 0) then
                print *, 'QR algorithm: QR decomposition failed'
                return
            end if

            ! B = R * Q
            B = matmul(R, Q)

            ! Check convergence (off-diagonal elements → 0)
            off_norm = 0.0d0
            do i = 1, n-1
                off_norm = off_norm + sum(abs(B(i+1:n, i)))
            end do

            if (off_norm < tol) exit
            if (abs(off_norm - prev_off_norm) < tol * 0.1d0) exit

            prev_off_norm = off_norm
        end do

        ! Extract eigenvalues from diagonal
        do i = 1, n
            eigenvalues(i) = B(i,i)
        end do

        ! Sort eigenvalues
        call sort_eigenvalues(eigenvalues, n)
    end subroutine qr_algorithm

    ! ========================================================================
    ! JACOBI METHOD (for symmetric matrices)
    ! ========================================================================

    subroutine jacobi_eigensolve(A, n, eigenvalues, eigenvectors, status)
        ! Solve symmetric eigenvalue problem using Jacobi method
        !
        ! Time Complexity: O(n³) typically
        !
        ! Algorithm:
        ! 1. Find largest off-diagonal element
        ! 2. Apply Jacobi rotation to zero it out
        ! 3. Repeat until all off-diagonal elements are small
        !
        ! Applications:
        ! - Symmetric eigenvalue problems (quantum mechanics, vibrations)
        ! - Principal Component Analysis
        ! - Spectral clustering
        implicit none
        integer, intent(in) :: n
        real(8), intent(in) :: A(n,n)
        real(8), intent(out) :: eigenvalues(n), eigenvectors(n,n)
        integer, intent(out) :: status
        real(8) :: B(n,n), c, s, tau, t, off_diag
        integer :: iter, i, j, k, p, q

        status = 0
        B = A
        eigenvectors = 0.0d0
        do i = 1, n
            eigenvectors(i,i) = 1.0d0
        end do

        ! Jacobi iterations
        do iter = 1, MAX_ITER
            ! Find largest off-diagonal element
            p = 1
            q = 2
            do i = 1, n
                do j = i+1, n
                    if (abs(B(i,j)) > abs(B(p,q))) then
                        p = i
                        q = j
                    end if
                end do
            end do

            ! Check convergence
            off_diag = abs(B(p,q))
            if (off_diag < EPSILON) exit

            ! Compute rotation angle
            if (abs(B(p,p) - B(q,q)) < EPSILON) then
                t = 1.0d0
            else
                tau = (B(q,q) - B(p,p)) / (2.0d0 * B(p,q))
                if (tau >= 0.0d0) then
                    t = 1.0d0 / (tau + sqrt(1.0d0 + tau*tau))
                else
                    t = -1.0d0 / (-tau + sqrt(1.0d0 + tau*tau))
                end if
            end if

            c = 1.0d0 / sqrt(1.0d0 + t*t)
            s = t * c

            ! Update B
            do k = 1, n
                if (k /= p .and. k /= q) then
                    tau = B(p,k)
                    B(p,k) = c * tau - s * B(q,k)
                    B(k,p) = B(p,k)
                    B(q,k) = s * tau + c * B(q,k)
                    B(k,q) = B(q,k)
                end if
            end do

            tau = B(p,p)
            B(p,p) = c*c*tau - 2.0d0*s*c*B(p,q) + s*s*B(q,q)
            B(q,q) = s*s*tau + 2.0d0*s*c*B(p,q) + c*c*B(q,q)
            B(p,q) = 0.0d0
            B(q,p) = 0.0d0

            ! Update eigenvectors
            do k = 1, n
                tau = eigenvectors(k,p)
                eigenvectors(k,p) = c * tau - s * eigenvectors(k,q)
                eigenvectors(k,q) = s * tau + c * eigenvectors(k,q)
            end do
        end do

        ! Extract eigenvalues
        do i = 1, n
            eigenvalues(i) = B(i,i)
        end do

        ! Sort
        call sort_eigen_system(eigenvalues, eigenvectors, n)
    end subroutine jacobi_eigensolve

    ! ========================================================================
    ! RAYLEIGH QUOTIENT ITERATION
    ! ========================================================================

    subroutine rayleigh_quotient_iteration(A, n, eigenvalue, eigenvector, max_iter, tol)
        ! Rayleigh quotient iteration (cubic convergence!)
        !
        ! Time Complexity: O(n³) per iteration
        ! Convergence: Cubic (very fast near eigenvalue)
        !
        ! Algorithm:
        ! 1. Compute Rayleigh quotient: μ = v^T A v / v^T v
        ! 2. Solve (A - μI) x = v
        ! 3. Normalize x
        !
        ! Applications:
        ! - Fast eigenvalue refinement
        ! - When good initial guess is available
        implicit none
        integer, intent(in) :: n, max_iter
        real(8), intent(in) :: A(n,n), tol
        real(8), intent(inout) :: eigenvalue, eigenvector(n)
        real(8) :: A_shifted(n,n), v_new(n), Av(n), mu, mu_old, norm_val
        integer :: iter, i, status

        ! Normalize initial vector
        norm_val = sqrt(sum(eigenvector**2))
        eigenvector = eigenvector / norm_val

        do iter = 1, max_iter
            mu_old = eigenvalue

            ! Compute Rayleigh quotient
            do i = 1, n
                Av(i) = sum(A(i,:) * eigenvector)
            end do
            mu = sum(eigenvector * Av)

            ! Solve (A - μI) x = v
            A_shifted = A
            do i = 1, n
                A_shifted(i,i) = A_shifted(i,i) - mu
            end do

            v_new = eigenvector
            call gaussian_elimination(A_shifted, v_new, v_new, n, status)

            if (status /= 0) then
                ! Near exact eigenvalue - use current value
                eigenvalue = mu
                return
            end if

            ! Normalize
            norm_val = sqrt(sum(v_new**2))
            v_new = v_new / norm_val

            eigenvalue = mu

            ! Check convergence
            if (abs(eigenvalue - mu_old) < tol) exit

            eigenvector = v_new
        end do
    end subroutine rayleigh_quotient_iteration

    ! ========================================================================
    ! HELPER ROUTINES
    ! ========================================================================

    subroutine gaussian_elimination(A, b, x, n, status)
        ! Solve Ax = b (simplified version)
        integer, intent(in) :: n
        real(8), intent(inout) :: A(n,n), b(n)
        real(8), intent(out) :: x(n)
        integer, intent(out) :: status
        integer :: i, j, k
        real(8) :: factor

        status = 0

        ! Forward elimination
        do k = 1, n-1
            if (abs(A(k,k)) < EPSILON) then
                status = -1
                return
            end if

            do i = k+1, n
                factor = A(i,k) / A(k,k)
                A(i,k+1:n) = A(i,k+1:n) - factor * A(k,k+1:n)
                b(i) = b(i) - factor * b(k)
            end do
        end do

        if (abs(A(n,n)) < EPSILON) then
            status = -1
            return
        end if

        ! Back substitution
        x(n) = b(n) / A(n,n)
        do i = n-1, 1, -1
            x(i) = (b(i) - sum(A(i,i+1:n) * x(i+1:n))) / A(i,i)
        end do
    end subroutine gaussian_elimination

    subroutine qr_decomposition(A, m, n, Q, R, status)
        ! QR decomposition using Gram-Schmidt
        integer, intent(in) :: m, n
        real(8), intent(in) :: A(m,n)
        real(8), intent(out) :: Q(m,n), R(n,n)
        integer, intent(out) :: status
        integer :: i, j, k
        real(8) :: norm_val, dot_val

        status = 0
        Q = A
        R = 0.0d0

        do j = 1, n
            norm_val = sqrt(sum(Q(:,j)**2))
            R(j,j) = norm_val

            if (norm_val < EPSILON) then
                status = -1
                return
            end if

            Q(:,j) = Q(:,j) / norm_val

            do k = j+1, n
                dot_val = sum(Q(:,j) * Q(:,k))
                R(j,k) = dot_val
                Q(:,k) = Q(:,k) - dot_val * Q(:,j)
            end do
        end do
    end subroutine qr_decomposition

    subroutine sort_eigenvalues(eigenvalues, n)
        integer, intent(in) :: n
        real(8), intent(inout) :: eigenvalues(n)
        integer :: i, j
        real(8) :: temp

        do i = 1, n-1
            do j = i+1, n
                if (abs(eigenvalues(j)) > abs(eigenvalues(i))) then
                    temp = eigenvalues(i)
                    eigenvalues(i) = eigenvalues(j)
                    eigenvalues(j) = temp
                end if
            end do
        end do
    end subroutine sort_eigenvalues

    subroutine sort_eigen_system(eigenvalues, eigenvectors, n)
        integer, intent(in) :: n
        real(8), intent(inout) :: eigenvalues(n), eigenvectors(n,n)
        integer :: i, j
        real(8) :: temp, temp_vec(n)

        do i = 1, n-1
            do j = i+1, n
                if (abs(eigenvalues(j)) > abs(eigenvalues(i))) then
                    temp = eigenvalues(i)
                    eigenvalues(i) = eigenvalues(j)
                    eigenvalues(j) = temp

                    temp_vec = eigenvectors(:,i)
                    eigenvectors(:,i) = eigenvectors(:,j)
                    eigenvectors(:,j) = temp_vec
                end if
            end do
        end do
    end subroutine sort_eigen_system

    subroutine print_matrix(A, m, n, name)
        integer, intent(in) :: m, n
        real(8), intent(in) :: A(m,n)
        character(len=*), intent(in) :: name
        integer :: i, j

        print *, ''
        print *, trim(name), ':'
        do i = 1, m
            do j = 1, n
                write(*, '(F10.4)', advance='no') A(i,j)
            end do
            print *
        end do
    end subroutine print_matrix

    subroutine print_vector(v, n, name)
        integer, intent(in) :: n
        real(8), intent(in) :: v(n)
        character(len=*), intent(in) :: name
        integer :: i

        print *, ''
        print *, trim(name), ':'
        do i = 1, n
            write(*, '(F10.4)') v(i)
        end do
    end subroutine print_vector

end module eigenvalue_module

! ============================================================================
! Main Program - Examples and Tests
! ============================================================================

program eigenvalue_demo
    use eigenvalue_module
    implicit none

    call example_power_iteration()
    call example_qr_algorithm()
    call example_jacobi()

contains

    subroutine example_power_iteration()
        real(8) :: A(3,3), eigenvalue, eigenvector(3)

        print *, ''
        print *, '======================================'
        print *, 'Example 1: Power Iteration'
        print *, '======================================'

        A = reshape([2.0d0, 1.0d0, 0.0d0, &
                     1.0d0, 3.0d0, 1.0d0, &
                     0.0d0, 1.0d0, 2.0d0], [3,3])

        call power_iteration(A, 3, eigenvalue, eigenvector, 100, 1.0d-8)

        call print_matrix(A, 3, 3, 'A')
        print *, ''
        print *, 'Dominant eigenvalue:', eigenvalue
        call print_vector(eigenvector, 3, 'Eigenvector')
    end subroutine example_power_iteration

    subroutine example_qr_algorithm()
        real(8) :: A(3,3), eigenvalues(3)

        print *, ''
        print *, '======================================'
        print *, 'Example 2: QR Algorithm'
        print *, '======================================'

        A = reshape([4.0d0, 1.0d0, 0.0d0, &
                     1.0d0, 4.0d0, 1.0d0, &
                     0.0d0, 1.0d0, 4.0d0], [3,3])

        call qr_algorithm(A, 3, eigenvalues, 100, 1.0d-8)

        call print_matrix(A, 3, 3, 'A')
        call print_vector(eigenvalues, 3, 'All eigenvalues')
    end subroutine example_qr_algorithm

    subroutine example_jacobi()
        real(8) :: A(3,3), eigenvalues(3), eigenvectors(3,3)
        integer :: status

        print *, ''
        print *, '======================================'
        print *, 'Example 3: Jacobi Method'
        print *, '======================================'

        A = reshape([2.0d0, 1.0d0, 0.0d0, &
                     1.0d0, 2.0d0, 1.0d0, &
                     0.0d0, 1.0d0, 2.0d0], [3,3])

        call jacobi_eigensolve(A, 3, eigenvalues, eigenvectors, status)

        call print_matrix(A, 3, 3, 'A (symmetric)')
        call print_vector(eigenvalues, 3, 'Eigenvalues')
        call print_matrix(eigenvectors, 3, 3, 'Eigenvectors (columns)')
    end subroutine example_jacobi

end program eigenvalue_demo
