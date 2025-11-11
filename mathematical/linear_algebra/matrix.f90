! ============================================================================
! Matrix Operations and Linear Algebra in Fortran 90
!
! Comprehensive collection of matrix operations optimized for numerical
! computing. Fortran has been the language of choice for scientific
! computing and linear algebra for over 60 years.
!
! Features:
! - Column-major storage (Fortran native)
! - BLAS-style interfaces
! - Numerical stability with pivoting
! - Efficient array operations
!
! Compile: gfortran -O3 -o matrix matrix.f90
! Run: ./matrix
!
! @author Algorithms Multiverse
! @version 1.0
! ============================================================================

module matrix_operations
    implicit none
    private
    public :: matrix_multiply, matrix_add, matrix_transpose
    public :: gaussian_elimination, lu_decomposition
    public :: matrix_inverse, determinant
    public :: power_iteration, qr_decomposition
    public :: print_matrix, print_vector

    real(8), parameter :: EPSILON = 1.0d-10

contains

    ! ========================================================================
    ! Basic Matrix Operations
    ! ========================================================================

    subroutine matrix_multiply(A, B, C, m, n, p)
        ! Standard matrix multiplication: C = A * B
        ! A is m×n, B is n×p, C is m×p
        !
        ! Time Complexity: O(mnp)
        !
        ! Applications:
        ! - Linear transformations
        ! - Scientific simulations
        ! - Computer graphics
        implicit none
        integer, intent(in) :: m, n, p
        real(8), intent(in) :: A(m,n), B(n,p)
        real(8), intent(out) :: C(m,p)
        integer :: i, j, k

        ! Initialize result
        C = 0.0d0

        ! Standard multiplication (ijk order for column-major)
        ! This order is cache-friendly in Fortran
        do j = 1, p
            do k = 1, n
                do i = 1, m
                    C(i,j) = C(i,j) + A(i,k) * B(k,j)
                end do
            end do
        end do
    end subroutine matrix_multiply

    subroutine matrix_add(A, B, C, m, n)
        ! Matrix addition: C = A + B
        implicit none
        integer, intent(in) :: m, n
        real(8), intent(in) :: A(m,n), B(m,n)
        real(8), intent(out) :: C(m,n)

        ! Fortran array notation - very efficient
        C = A + B
    end subroutine matrix_add

    subroutine matrix_transpose(A, AT, m, n)
        ! Matrix transpose: AT = A^T
        !
        ! Time Complexity: O(mn)
        implicit none
        integer, intent(in) :: m, n
        real(8), intent(in) :: A(m,n)
        real(8), intent(out) :: AT(n,m)

        ! Fortran intrinsic function
        AT = transpose(A)
    end subroutine matrix_transpose

    ! ========================================================================
    ! Gaussian Elimination
    ! ========================================================================

    subroutine gaussian_elimination(A, b, x, n, status)
        ! Solve Ax = b using Gaussian elimination with partial pivoting
        !
        ! Time Complexity: O(n³)
        !
        ! Arguments:
        !   A(n,n)  - coefficient matrix (destroyed)
        !   b(n)    - right-hand side (destroyed)
        !   x(n)    - solution vector (output)
        !   n       - system size
        !   status  - 0: success, -1: singular matrix
        !
        ! Applications:
        ! - Solving linear systems
        ! - Circuit analysis
        ! - Finite element analysis
        implicit none
        integer, intent(in) :: n
        real(8), intent(inout) :: A(n,n), b(n)
        real(8), intent(out) :: x(n)
        integer, intent(out) :: status
        integer :: i, j, k, max_row
        real(8) :: max_val, factor, temp

        status = 0

        ! Forward elimination with partial pivoting
        do k = 1, n-1
            ! Find pivot (maximum absolute value in column k)
            max_val = abs(A(k,k))
            max_row = k

            do i = k+1, n
                if (abs(A(i,k)) > max_val) then
                    max_val = abs(A(i,k))
                    max_row = i
                end if
            end do

            ! Check for singular matrix
            if (max_val < EPSILON) then
                status = -1
                return
            end if

            ! Swap rows if necessary
            if (max_row /= k) then
                do j = k, n
                    temp = A(k,j)
                    A(k,j) = A(max_row,j)
                    A(max_row,j) = temp
                end do
                temp = b(k)
                b(k) = b(max_row)
                b(max_row) = temp
            end if

            ! Eliminate column k below pivot
            do i = k+1, n
                factor = A(i,k) / A(k,k)
                do j = k+1, n
                    A(i,j) = A(i,j) - factor * A(k,j)
                end do
                b(i) = b(i) - factor * b(k)
                A(i,k) = 0.0d0
            end do
        end do

        ! Check last diagonal element
        if (abs(A(n,n)) < EPSILON) then
            status = -1
            return
        end if

        ! Backward substitution
        x(n) = b(n) / A(n,n)
        do i = n-1, 1, -1
            x(i) = b(i)
            do j = i+1, n
                x(i) = x(i) - A(i,j) * x(j)
            end do
            x(i) = x(i) / A(i,i)
        end do
    end subroutine gaussian_elimination

    ! ========================================================================
    ! LU Decomposition
    ! ========================================================================

    subroutine lu_decomposition(A, L, U, n, status)
        ! LU decomposition: A = LU (Doolittle's method)
        !
        ! Time Complexity: O(n³)
        !
        ! L is lower triangular with 1's on diagonal
        ! U is upper triangular
        !
        ! Applications:
        ! - Solving multiple systems with same A
        ! - Determinant calculation
        ! - Matrix inversion
        implicit none
        integer, intent(in) :: n
        real(8), intent(in) :: A(n,n)
        real(8), intent(out) :: L(n,n), U(n,n)
        integer, intent(out) :: status
        integer :: i, j, k
        real(8) :: sum_val

        status = 0
        L = 0.0d0
        U = 0.0d0

        do i = 1, n
            ! Upper triangular matrix U
            do k = i, n
                sum_val = 0.0d0
                do j = 1, i-1
                    sum_val = sum_val + L(i,j) * U(j,k)
                end do
                U(i,k) = A(i,k) - sum_val
            end do

            ! Lower triangular matrix L
            L(i,i) = 1.0d0  ! Diagonal elements
            do k = i+1, n
                sum_val = 0.0d0
                do j = 1, i-1
                    sum_val = sum_val + L(k,j) * U(j,i)
                end do
                if (abs(U(i,i)) < EPSILON) then
                    status = -1
                    return
                end if
                L(k,i) = (A(k,i) - sum_val) / U(i,i)
            end do
        end do
    end subroutine lu_decomposition

    ! ========================================================================
    ! QR Decomposition
    ! ========================================================================

    subroutine qr_decomposition(A, Q, R, m, n, status)
        ! QR decomposition using Gram-Schmidt orthogonalization
        !
        ! A = QR where Q is orthogonal, R is upper triangular
        !
        ! Time Complexity: O(mn²)
        !
        ! Applications:
        ! - Least squares problems
        ! - Eigenvalue computation
        implicit none
        integer, intent(in) :: m, n
        real(8), intent(in) :: A(m,n)
        real(8), intent(out) :: Q(m,n), R(n,n)
        integer, intent(out) :: status
        integer :: i, j, k
        real(8) :: norm_val, dot_val

        status = 0
        Q = A  ! Copy A to Q
        R = 0.0d0

        ! Modified Gram-Schmidt
        do j = 1, n
            ! Compute norm of column j
            norm_val = 0.0d0
            do i = 1, m
                norm_val = norm_val + Q(i,j)**2
            end do
            R(j,j) = sqrt(norm_val)

            if (R(j,j) < EPSILON) then
                status = -1
                return
            end if

            ! Normalize column j
            Q(:,j) = Q(:,j) / R(j,j)

            ! Orthogonalize remaining columns
            do k = j+1, n
                dot_val = 0.0d0
                do i = 1, m
                    dot_val = dot_val + Q(i,j) * Q(i,k)
                end do
                R(j,k) = dot_val
                Q(:,k) = Q(:,k) - R(j,k) * Q(:,j)
            end do
        end do
    end subroutine qr_decomposition

    ! ========================================================================
    ! Matrix Inversion
    ! ========================================================================

    subroutine matrix_inverse(A, A_inv, n, status)
        ! Matrix inversion using Gauss-Jordan elimination
        !
        ! Time Complexity: O(n³)
        !
        ! Applications:
        ! - Solving linear systems
        ! - Control systems
        ! - Statistics
        implicit none
        integer, intent(in) :: n
        real(8), intent(in) :: A(n,n)
        real(8), intent(out) :: A_inv(n,n)
        integer, intent(out) :: status
        real(8) :: augmented(n,2*n)
        integer :: i, j, k, max_row
        real(8) :: max_val, pivot, factor, temp

        status = 0

        ! Create augmented matrix [A|I]
        augmented(:,1:n) = A
        augmented(:,n+1:2*n) = 0.0d0
        do i = 1, n
            augmented(i,n+i) = 1.0d0
        end do

        ! Forward elimination
        do k = 1, n
            ! Find pivot
            max_val = abs(augmented(k,k))
            max_row = k
            do i = k+1, n
                if (abs(augmented(i,k)) > max_val) then
                    max_val = abs(augmented(i,k))
                    max_row = i
                end if
            end do

            ! Swap rows
            if (max_row /= k) then
                do j = 1, 2*n
                    temp = augmented(k,j)
                    augmented(k,j) = augmented(max_row,j)
                    augmented(max_row,j) = temp
                end do
            end if

            ! Check for singular matrix
            if (abs(augmented(k,k)) < EPSILON) then
                status = -1
                return
            end if

            ! Scale pivot row
            pivot = augmented(k,k)
            augmented(k,:) = augmented(k,:) / pivot

            ! Eliminate column
            do i = 1, n
                if (i /= k) then
                    factor = augmented(i,k)
                    augmented(i,:) = augmented(i,:) - factor * augmented(k,:)
                end if
            end do
        end do

        ! Extract inverse from right half
        A_inv = augmented(:,n+1:2*n)
    end subroutine matrix_inverse

    ! ========================================================================
    ! Determinant
    ! ========================================================================

    function determinant(A, n) result(det)
        ! Calculate determinant using LU decomposition
        !
        ! Time Complexity: O(n³)
        !
        ! det(A) = product of diagonal elements of U
        implicit none
        integer, intent(in) :: n
        real(8), intent(in) :: A(n,n)
        real(8) :: det
        real(8) :: L(n,n), U(n,n)
        integer :: i, status

        call lu_decomposition(A, L, U, n, status)

        if (status /= 0) then
            det = 0.0d0
            return
        end if

        ! Product of diagonal elements of U
        det = 1.0d0
        do i = 1, n
            det = det * U(i,i)
        end do
    end function determinant

    ! ========================================================================
    ! Eigenvalue Computation
    ! ========================================================================

    subroutine power_iteration(A, n, eigenvalue, eigenvector, max_iter)
        ! Find dominant eigenvalue and eigenvector using power iteration
        !
        ! Time Complexity: O(n² * iterations)
        !
        ! Applications:
        ! - Google PageRank
        ! - Principal Component Analysis
        ! - Markov chains
        implicit none
        integer, intent(in) :: n, max_iter
        real(8), intent(in) :: A(n,n)
        real(8), intent(out) :: eigenvalue
        real(8), intent(out) :: eigenvector(n)
        integer :: iter, i
        real(8) :: v_new(n), norm_val, Av(n)

        ! Initialize with random vector
        call random_number(eigenvector)

        ! Normalize
        norm_val = sqrt(sum(eigenvector**2))
        eigenvector = eigenvector / norm_val

        ! Power iteration
        do iter = 1, max_iter
            ! Multiply by matrix
            do i = 1, n
                v_new(i) = sum(A(i,:) * eigenvector)
            end do

            ! Normalize
            norm_val = sqrt(sum(v_new**2))
            v_new = v_new / norm_val

            ! Check convergence
            if (sum(abs(v_new - eigenvector)) < EPSILON) exit

            eigenvector = v_new
        end do

        ! Compute eigenvalue: λ = v^T * A * v
        do i = 1, n
            Av(i) = sum(A(i,:) * eigenvector)
        end do
        eigenvalue = sum(eigenvector * Av)
    end subroutine power_iteration

    ! ========================================================================
    ! Utility Functions
    ! ========================================================================

    subroutine print_matrix(A, m, n, name)
        ! Print matrix with formatting
        implicit none
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
        ! Print vector with formatting
        implicit none
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

end module matrix_operations

! ============================================================================
! Main Program - Examples and Tests
! ============================================================================

program matrix_demo
    use matrix_operations
    implicit none

    ! Example 1: Matrix multiplication
    call example_multiplication()

    ! Example 2: Gaussian elimination
    call example_gaussian_elimination()

    ! Example 3: LU decomposition
    call example_lu_decomposition()

    ! Example 4: Matrix inversion
    call example_matrix_inverse()

    ! Example 5: Eigenvalues
    call example_eigenvalues()

contains

    subroutine example_multiplication()
        ! Demonstrate matrix multiplication
        real(8) :: A(2,3), B(3,2), C(2,2)

        print *, ''
        print *, '======================================'
        print *, 'Example 1: Matrix Multiplication'
        print *, '======================================'

        ! Initialize matrices
        A = reshape([1.0d0, 4.0d0, 2.0d0, 5.0d0, 3.0d0, 6.0d0], [2,3])
        B = reshape([7.0d0, 9.0d0, 11.0d0, 8.0d0, 10.0d0, 12.0d0], [3,2])

        call matrix_multiply(A, B, C, 2, 3, 2)

        call print_matrix(A, 2, 3, 'A (2×3)')
        call print_matrix(B, 3, 2, 'B (3×2)')
        call print_matrix(C, 2, 2, 'C = A × B (2×2)')
    end subroutine example_multiplication

    subroutine example_gaussian_elimination()
        ! Solve linear system Ax = b
        real(8) :: A(3,3), b(3), x(3)
        integer :: status

        print *, ''
        print *, '======================================'
        print *, 'Example 2: Gaussian Elimination'
        print *, '======================================'

        ! System: 2x + y - z = 8
        !        -3x - y + 2z = -11
        !        -2x + y + 2z = -3
        A = reshape([2.0d0, -3.0d0, -2.0d0, &
                     1.0d0, -1.0d0,  1.0d0, &
                    -1.0d0,  2.0d0,  2.0d0], [3,3])
        b = [8.0d0, -11.0d0, -3.0d0]

        call gaussian_elimination(A, b, x, 3, status)

        if (status == 0) then
            call print_vector(x, 3, 'Solution x')
            print *, 'Expected: x=2, y=3, z=-1'
        else
            print *, 'Error: Singular matrix'
        end if
    end subroutine example_gaussian_elimination

    subroutine example_lu_decomposition()
        ! LU decomposition example
        real(8) :: A(3,3), L(3,3), U(3,3), product(3,3)
        integer :: status

        print *, ''
        print *, '======================================'
        print *, 'Example 3: LU Decomposition'
        print *, '======================================'

        A = reshape([2.0d0, -4.0d0, -4.0d0, &
                    -1.0d0,  6.0d0, -2.0d0, &
                    -2.0d0,  3.0d0,  8.0d0], [3,3])

        call lu_decomposition(A, L, U, 3, status)

        if (status == 0) then
            call print_matrix(A, 3, 3, 'A')
            call print_matrix(L, 3, 3, 'L (lower triangular)')
            call print_matrix(U, 3, 3, 'U (upper triangular)')

            ! Verify: L × U = A
            call matrix_multiply(L, U, product, 3, 3, 3)
            call print_matrix(product, 3, 3, 'L × U (should equal A)')
        else
            print *, 'Error: Singular matrix'
        end if
    end subroutine example_lu_decomposition

    subroutine example_matrix_inverse()
        ! Matrix inversion example
        real(8) :: A(2,2), A_inv(2,2), I(2,2)
        integer :: status

        print *, ''
        print *, '======================================'
        print *, 'Example 4: Matrix Inversion'
        print *, '======================================'

        A = reshape([4.0d0, 2.0d0, 7.0d0, 6.0d0], [2,2])

        call matrix_inverse(A, A_inv, 2, status)

        if (status == 0) then
            call print_matrix(A, 2, 2, 'A')
            call print_matrix(A_inv, 2, 2, 'A^(-1)')

            ! Verify: A × A^(-1) = I
            call matrix_multiply(A, A_inv, I, 2, 2, 2)
            call print_matrix(I, 2, 2, 'A × A^(-1) (should be identity)')
        else
            print *, 'Error: Singular matrix'
        end if
    end subroutine example_matrix_inverse

    subroutine example_eigenvalues()
        ! Eigenvalue computation
        real(8) :: A(2,2), eigenvalue, eigenvector(2)

        print *, ''
        print *, '======================================'
        print *, 'Example 5: Eigenvalue (Power Iteration)'
        print *, '======================================'

        A = reshape([2.0d0, 1.0d0, 1.0d0, 2.0d0], [2,2])

        call power_iteration(A, 2, eigenvalue, eigenvector, 100)

        call print_matrix(A, 2, 2, 'A')
        print *, ''
        print *, 'Dominant eigenvalue:', eigenvalue
        call print_vector(eigenvector, 2, 'Corresponding eigenvector')
    end subroutine example_eigenvalues

end program matrix_demo
