! Matrix Operations Module
! High-performance linear algebra algorithms in Fortran

module matrix_module
    use iso_fortran_env, only: int32, int64, real32, real64
    use, intrinsic :: ieee_arithmetic
    implicit none
    private

    ! Public interfaces
    public :: matrix_multiply, matrix_transpose, matrix_inverse
    public :: lu_decomposition, qr_decomposition, cholesky_decomposition
    public :: gaussian_elimination, jacobi_iteration, gauss_seidel
    public :: eigenvalues_power_method, svd_simple
    public :: matrix_add, matrix_subtract, matrix_scalar_multiply
    public :: matrix_norm, matrix_determinant, matrix_trace
    public :: is_symmetric, is_positive_definite, matrix_rank
    public :: solve_linear_system

    ! Custom types
    public :: matrix_type, sparse_matrix_type

    ! Matrix type for convenient operations
    type :: matrix_type
        real(real64), dimension(:, :), allocatable :: data
        integer(int32) :: rows, cols
    contains
        procedure :: init => matrix_init
        procedure :: destroy => matrix_destroy
        procedure :: print => matrix_print
    end type matrix_type

    ! Sparse matrix type (CSR format)
    type :: sparse_matrix_type
        real(real64), dimension(:), allocatable :: values
        integer(int32), dimension(:), allocatable :: col_indices
        integer(int32), dimension(:), allocatable :: row_ptr
        integer(int32) :: rows, cols, nnz
    contains
        procedure :: init_sparse => sparse_matrix_init
        procedure :: destroy_sparse => sparse_matrix_destroy
    end type sparse_matrix_type

    ! Parameters
    real(real64), parameter :: TOLERANCE = 1.0e-10_real64

contains

    !===========================================================================
    ! Matrix Type Methods
    !===========================================================================

    subroutine matrix_init(this, rows, cols)
        implicit none
        class(matrix_type), intent(inout) :: this
        integer(int32), intent(in) :: rows, cols

        this%rows = rows
        this%cols = cols
        allocate(this%data(rows, cols))
        this%data = 0.0_real64

    end subroutine matrix_init

    subroutine matrix_destroy(this)
        implicit none
        class(matrix_type), intent(inout) :: this

        if (allocated(this%data)) deallocate(this%data)
        this%rows = 0
        this%cols = 0

    end subroutine matrix_destroy

    subroutine matrix_print(this)
        implicit none
        class(matrix_type), intent(in) :: this
        integer(int32) :: i, j

        print '(A, I0, A, I0)', 'Matrix (', this%rows, ' x ', this%cols, '):'
        do i = 1, this%rows
            do j = 1, this%cols
                write(*, '(F12.6, A)', advance='no') this%data(i, j), ' '
            end do
            print *
        end do

    end subroutine matrix_print

    subroutine sparse_matrix_init(this, rows, cols, nnz)
        implicit none
        class(sparse_matrix_type), intent(inout) :: this
        integer(int32), intent(in) :: rows, cols, nnz

        this%rows = rows
        this%cols = cols
        this%nnz = nnz
        allocate(this%values(nnz))
        allocate(this%col_indices(nnz))
        allocate(this%row_ptr(rows + 1))

    end subroutine sparse_matrix_init

    subroutine sparse_matrix_destroy(this)
        implicit none
        class(sparse_matrix_type), intent(inout) :: this

        if (allocated(this%values)) deallocate(this%values)
        if (allocated(this%col_indices)) deallocate(this%col_indices)
        if (allocated(this%row_ptr)) deallocate(this%row_ptr)
        this%rows = 0
        this%cols = 0
        this%nnz = 0

    end subroutine sparse_matrix_destroy

    !===========================================================================
    ! Basic Matrix Operations
    !===========================================================================

    ! Matrix multiplication C = A * B
    function matrix_multiply(A, B) result(C)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A, B
        real(real64), dimension(size(A, 1), size(B, 2)) :: C
        integer(int32) :: m, n, k
        integer(int32) :: i, j, l

        m = size(A, 1)
        k = size(A, 2)
        n = size(B, 2)

        if (size(B, 1) /= k) then
            print *, "Error: Matrix dimensions incompatible for multiplication"
            C = ieee_value(C(1, 1), ieee_quiet_nan)
            return
        end if

        ! Using explicit loops for clarity (BLAS would be faster)
        C = 0.0_real64
        do i = 1, m
            do j = 1, n
                do l = 1, k
                    C(i, j) = C(i, j) + A(i, l) * B(l, j)
                end do
            end do
        end do

    end function matrix_multiply

    ! Matrix transpose
    function matrix_transpose(A) result(AT)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64), dimension(size(A, 2), size(A, 1)) :: AT
        integer(int32) :: i, j

        do i = 1, size(A, 1)
            do j = 1, size(A, 2)
                AT(j, i) = A(i, j)
            end do
        end do

    end function matrix_transpose

    ! Matrix addition
    function matrix_add(A, B) result(C)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A, B
        real(real64), dimension(size(A, 1), size(A, 2)) :: C

        if (size(A, 1) /= size(B, 1) .or. size(A, 2) /= size(B, 2)) then
            print *, "Error: Matrix dimensions must match for addition"
            C = ieee_value(C(1, 1), ieee_quiet_nan)
            return
        end if

        C = A + B

    end function matrix_add

    ! Matrix subtraction
    function matrix_subtract(A, B) result(C)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A, B
        real(real64), dimension(size(A, 1), size(A, 2)) :: C

        if (size(A, 1) /= size(B, 1) .or. size(A, 2) /= size(B, 2)) then
            print *, "Error: Matrix dimensions must match for subtraction"
            C = ieee_value(C(1, 1), ieee_quiet_nan)
            return
        end if

        C = A - B

    end function matrix_subtract

    ! Scalar multiplication
    function matrix_scalar_multiply(A, scalar) result(B)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64), intent(in) :: scalar
        real(real64), dimension(size(A, 1), size(A, 2)) :: B

        B = scalar * A

    end function matrix_scalar_multiply

    !===========================================================================
    ! Matrix Properties
    !===========================================================================

    ! Matrix norm (Frobenius norm)
    function matrix_norm(A) result(norm_val)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64) :: norm_val
        integer(int32) :: i, j

        norm_val = 0.0_real64
        do i = 1, size(A, 1)
            do j = 1, size(A, 2)
                norm_val = norm_val + A(i, j) ** 2
            end do
        end do
        norm_val = sqrt(norm_val)

    end function matrix_norm

    ! Matrix determinant (using LU decomposition)
    function matrix_determinant(A) result(det)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64) :: det
        real(real64), dimension(size(A, 1), size(A, 2)) :: L, U
        integer(int32), dimension(size(A, 1)) :: P
        integer(int32) :: i, n, swaps

        n = size(A, 1)
        if (n /= size(A, 2)) then
            print *, "Error: Determinant requires square matrix"
            det = ieee_value(det, ieee_quiet_nan)
            return
        end if

        call lu_decomposition(A, L, U, P, swaps)

        det = 1.0_real64
        do i = 1, n
            det = det * U(i, i)
        end do

        ! Adjust sign based on permutations
        if (mod(swaps, 2) == 1) det = -det

    end function matrix_determinant

    ! Matrix trace
    function matrix_trace(A) result(trace_val)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64) :: trace_val
        integer(int32) :: i, n

        n = min(size(A, 1), size(A, 2))
        trace_val = 0.0_real64

        do i = 1, n
            trace_val = trace_val + A(i, i)
        end do

    end function matrix_trace

    ! Check if matrix is symmetric
    function is_symmetric(A) result(symmetric)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        logical :: symmetric
        integer(int32) :: i, j, n

        n = size(A, 1)
        symmetric = .true.

        if (n /= size(A, 2)) then
            symmetric = .false.
            return
        end if

        do i = 1, n
            do j = i + 1, n
                if (abs(A(i, j) - A(j, i)) > TOLERANCE) then
                    symmetric = .false.
                    return
                end if
            end do
        end do

    end function is_symmetric

    ! Check if matrix is positive definite (using Cholesky)
    function is_positive_definite(A) result(positive_def)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        logical :: positive_def
        real(real64), dimension(size(A, 1), size(A, 2)) :: L
        integer(int32) :: info

        if (.not. is_symmetric(A)) then
            positive_def = .false.
            return
        end if

        call cholesky_decomposition(A, L, info)
        positive_def = (info == 0)

    end function is_positive_definite

    ! Matrix rank (using SVD)
    function matrix_rank(A) result(rank_val)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        integer(int32) :: rank_val
        real(real64), dimension(min(size(A, 1), size(A, 2))) :: singular_values
        integer(int32) :: i

        ! Get singular values (simplified)
        call svd_simple(A, singular_values)

        rank_val = 0
        do i = 1, size(singular_values)
            if (abs(singular_values(i)) > TOLERANCE) then
                rank_val = rank_val + 1
            end if
        end do

    end function matrix_rank

    !===========================================================================
    ! Matrix Decompositions
    !===========================================================================

    ! LU decomposition with partial pivoting
    subroutine lu_decomposition(A, L, U, P, swaps)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64), dimension(:, :), intent(out) :: L, U
        integer(int32), dimension(:), intent(out) :: P
        integer(int32), intent(out) :: swaps
        integer(int32) :: i, j, k, n, max_row
        real(real64) :: max_val, temp

        n = size(A, 1)
        U = A
        L = 0.0_real64
        swaps = 0

        ! Initialize permutation vector
        do i = 1, n
            P(i) = i
        end do

        ! Initialize L diagonal
        do i = 1, n
            L(i, i) = 1.0_real64
        end do

        do k = 1, n - 1
            ! Find pivot
            max_val = abs(U(k, k))
            max_row = k

            do i = k + 1, n
                if (abs(U(i, k)) > max_val) then
                    max_val = abs(U(i, k))
                    max_row = i
                end if
            end do

            ! Swap rows if needed
            if (max_row /= k) then
                swaps = swaps + 1

                ! Swap in U
                do j = 1, n
                    temp = U(k, j)
                    U(k, j) = U(max_row, j)
                    U(max_row, j) = temp
                end do

                ! Swap in L (only computed part)
                do j = 1, k - 1
                    temp = L(k, j)
                    L(k, j) = L(max_row, j)
                    L(max_row, j) = temp
                end do

                ! Swap in P
                i = P(k)
                P(k) = P(max_row)
                P(max_row) = i
            end if

            ! Gaussian elimination
            do i = k + 1, n
                L(i, k) = U(i, k) / U(k, k)
                do j = k, n
                    U(i, j) = U(i, j) - L(i, k) * U(k, j)
                end do
            end do
        end do

    end subroutine lu_decomposition

    ! QR decomposition using Gram-Schmidt
    subroutine qr_decomposition(A, Q, R)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64), dimension(:, :), intent(out) :: Q, R
        integer(int32) :: i, j, k, m, n
        real(real64) :: norm_val

        m = size(A, 1)
        n = size(A, 2)

        Q = A
        R = 0.0_real64

        do j = 1, n
            ! Compute R(i,j) for i < j
            do i = 1, j - 1
                R(i, j) = 0.0_real64
                do k = 1, m
                    R(i, j) = R(i, j) + Q(k, i) * A(k, j)
                end do

                ! Orthogonalize
                do k = 1, m
                    Q(k, j) = Q(k, j) - R(i, j) * Q(k, i)
                end do
            end do

            ! Compute R(j,j) and normalize
            norm_val = 0.0_real64
            do k = 1, m
                norm_val = norm_val + Q(k, j) ** 2
            end do
            R(j, j) = sqrt(norm_val)

            if (R(j, j) > TOLERANCE) then
                do k = 1, m
                    Q(k, j) = Q(k, j) / R(j, j)
                end do
            end if
        end do

    end subroutine qr_decomposition

    ! Cholesky decomposition for positive definite matrices
    subroutine cholesky_decomposition(A, L, info)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64), dimension(:, :), intent(out) :: L
        integer(int32), intent(out) :: info
        integer(int32) :: i, j, k, n
        real(real64) :: sum_val

        n = size(A, 1)
        L = 0.0_real64
        info = 0

        do j = 1, n
            ! Diagonal element
            sum_val = A(j, j)
            do k = 1, j - 1
                sum_val = sum_val - L(j, k) ** 2
            end do

            if (sum_val <= 0.0_real64) then
                info = j  ! Not positive definite
                return
            end if

            L(j, j) = sqrt(sum_val)

            ! Off-diagonal elements
            do i = j + 1, n
                sum_val = A(i, j)
                do k = 1, j - 1
                    sum_val = sum_val - L(i, k) * L(j, k)
                end do
                L(i, j) = sum_val / L(j, j)
            end do
        end do

    end subroutine cholesky_decomposition

    !===========================================================================
    ! Linear System Solvers
    !===========================================================================

    ! Gaussian elimination with partial pivoting
    subroutine gaussian_elimination(A, b, x)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64), dimension(:), intent(in) :: b
        real(real64), dimension(:), intent(out) :: x
        real(real64), dimension(size(A, 1), size(A, 2) + 1) :: augmented
        integer(int32) :: i, j, k, n, max_row
        real(real64) :: max_val, temp, factor

        n = size(A, 1)

        ! Create augmented matrix
        augmented(:, 1:n) = A
        augmented(:, n + 1) = b

        ! Forward elimination
        do k = 1, n - 1
            ! Partial pivoting
            max_val = abs(augmented(k, k))
            max_row = k

            do i = k + 1, n
                if (abs(augmented(i, k)) > max_val) then
                    max_val = abs(augmented(i, k))
                    max_row = i
                end if
            end do

            ! Swap rows
            if (max_row /= k) then
                do j = k, n + 1
                    temp = augmented(k, j)
                    augmented(k, j) = augmented(max_row, j)
                    augmented(max_row, j) = temp
                end do
            end if

            ! Eliminate
            do i = k + 1, n
                factor = augmented(i, k) / augmented(k, k)
                do j = k, n + 1
                    augmented(i, j) = augmented(i, j) - factor * augmented(k, j)
                end do
            end do
        end do

        ! Back substitution
        x(n) = augmented(n, n + 1) / augmented(n, n)

        do i = n - 1, 1, -1
            x(i) = augmented(i, n + 1)
            do j = i + 1, n
                x(i) = x(i) - augmented(i, j) * x(j)
            end do
            x(i) = x(i) / augmented(i, i)
        end do

    end subroutine gaussian_elimination

    ! Jacobi iteration for linear systems
    subroutine jacobi_iteration(A, b, x, max_iter, tol)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64), dimension(:), intent(in) :: b
        real(real64), dimension(:), intent(inout) :: x
        integer(int32), intent(in) :: max_iter
        real(real64), intent(in) :: tol
        real(real64), dimension(size(x)) :: x_new
        real(real64) :: sum_val, error
        integer(int32) :: i, j, n, iter

        n = size(A, 1)

        do iter = 1, max_iter
            do i = 1, n
                sum_val = b(i)
                do j = 1, n
                    if (j /= i) then
                        sum_val = sum_val - A(i, j) * x(j)
                    end if
                end do
                x_new(i) = sum_val / A(i, i)
            end do

            ! Check convergence
            error = 0.0_real64
            do i = 1, n
                error = error + (x_new(i) - x(i)) ** 2
            end do
            error = sqrt(error)

            x = x_new

            if (error < tol) then
                print '(A, I0, A)', "Jacobi converged in ", iter, " iterations"
                return
            end if
        end do

        print '(A)', "Warning: Jacobi iteration did not converge"

    end subroutine jacobi_iteration

    ! Gauss-Seidel iteration
    subroutine gauss_seidel(A, b, x, max_iter, tol)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64), dimension(:), intent(in) :: b
        real(real64), dimension(:), intent(inout) :: x
        integer(int32), intent(in) :: max_iter
        real(real64), intent(in) :: tol
        real(real64), dimension(size(x)) :: x_old
        real(real64) :: sum_val, error
        integer(int32) :: i, j, n, iter

        n = size(A, 1)

        do iter = 1, max_iter
            x_old = x

            do i = 1, n
                sum_val = b(i)
                do j = 1, i - 1
                    sum_val = sum_val - A(i, j) * x(j)
                end do
                do j = i + 1, n
                    sum_val = sum_val - A(i, j) * x(j)
                end do
                x(i) = sum_val / A(i, i)
            end do

            ! Check convergence
            error = 0.0_real64
            do i = 1, n
                error = error + (x(i) - x_old(i)) ** 2
            end do
            error = sqrt(error)

            if (error < tol) then
                print '(A, I0, A)', "Gauss-Seidel converged in ", iter, " iterations"
                return
            end if
        end do

        print '(A)', "Warning: Gauss-Seidel iteration did not converge"

    end subroutine gauss_seidel

    ! General linear system solver
    subroutine solve_linear_system(A, b, x, method)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64), dimension(:), intent(in) :: b
        real(real64), dimension(:), intent(out) :: x
        character(len=*), intent(in), optional :: method
        character(len=20) :: solver_method

        solver_method = "gaussian"
        if (present(method)) solver_method = method

        select case(trim(solver_method))
            case("gaussian", "gauss")
                call gaussian_elimination(A, b, x)
            case("jacobi")
                x = 0.0_real64  ! Initial guess
                call jacobi_iteration(A, b, x, 1000, 1.0e-6_real64)
            case("gauss-seidel", "seidel")
                x = 0.0_real64  ! Initial guess
                call gauss_seidel(A, b, x, 1000, 1.0e-6_real64)
            case default
                print *, "Unknown method: ", solver_method
                call gaussian_elimination(A, b, x)
        end select

    end subroutine solve_linear_system

    !===========================================================================
    ! Matrix Inverse
    !===========================================================================

    ! Matrix inverse using Gauss-Jordan elimination
    function matrix_inverse(A) result(A_inv)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64), dimension(size(A, 1), size(A, 2)) :: A_inv
        real(real64), dimension(size(A, 1), 2 * size(A, 1)) :: augmented
        integer(int32) :: i, j, k, n, max_row
        real(real64) :: max_val, temp, factor

        n = size(A, 1)

        if (n /= size(A, 2)) then
            print *, "Error: Inverse requires square matrix"
            A_inv = ieee_value(A_inv(1, 1), ieee_quiet_nan)
            return
        end if

        ! Create augmented matrix [A | I]
        augmented(:, 1:n) = A
        augmented(:, n + 1:2 * n) = 0.0_real64
        do i = 1, n
            augmented(i, n + i) = 1.0_real64
        end do

        ! Gauss-Jordan elimination
        do k = 1, n
            ! Partial pivoting
            max_val = abs(augmented(k, k))
            max_row = k

            do i = k + 1, n
                if (abs(augmented(i, k)) > max_val) then
                    max_val = abs(augmented(i, k))
                    max_row = i
                end if
            end do

            ! Swap rows
            if (max_row /= k) then
                do j = 1, 2 * n
                    temp = augmented(k, j)
                    augmented(k, j) = augmented(max_row, j)
                    augmented(max_row, j) = temp
                end do
            end if

            ! Check for singularity
            if (abs(augmented(k, k)) < TOLERANCE) then
                print *, "Error: Matrix is singular"
                A_inv = ieee_value(A_inv(1, 1), ieee_quiet_nan)
                return
            end if

            ! Scale pivot row
            factor = augmented(k, k)
            do j = 1, 2 * n
                augmented(k, j) = augmented(k, j) / factor
            end do

            ! Eliminate column
            do i = 1, n
                if (i /= k) then
                    factor = augmented(i, k)
                    do j = 1, 2 * n
                        augmented(i, j) = augmented(i, j) - factor * augmented(k, j)
                    end do
                end if
            end do
        end do

        ! Extract inverse matrix
        A_inv = augmented(:, n + 1:2 * n)

    end function matrix_inverse

    !===========================================================================
    ! Eigenvalue Problems
    !===========================================================================

    ! Power method for dominant eigenvalue
    subroutine eigenvalues_power_method(A, eigenvalue, eigenvector, max_iter, tol)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64), intent(out) :: eigenvalue
        real(real64), dimension(:), intent(out) :: eigenvector
        integer(int32), intent(in) :: max_iter
        real(real64), intent(in) :: tol
        real(real64), dimension(size(A, 1)) :: v, v_new
        real(real64) :: norm_val, lambda_old
        integer(int32) :: i, n, iter

        n = size(A, 1)

        ! Initialize with random vector
        call random_number(v)
        norm_val = sqrt(sum(v ** 2))
        v = v / norm_val

        eigenvalue = 0.0_real64

        do iter = 1, max_iter
            lambda_old = eigenvalue

            ! Multiply by A
            v_new = matmul(A, v)

            ! Compute eigenvalue (Rayleigh quotient)
            eigenvalue = dot_product(v, v_new)

            ! Normalize
            norm_val = sqrt(sum(v_new ** 2))
            v_new = v_new / norm_val

            ! Check convergence
            if (abs(eigenvalue - lambda_old) < tol) then
                eigenvector = v_new
                print '(A, I0, A)', "Power method converged in ", iter, " iterations"
                return
            end if

            v = v_new
        end do

        eigenvector = v
        print '(A)', "Warning: Power method did not converge"

    end subroutine eigenvalues_power_method

    ! Simplified SVD (only singular values)
    subroutine svd_simple(A, singular_values)
        implicit none
        real(real64), dimension(:, :), intent(in) :: A
        real(real64), dimension(:), intent(out) :: singular_values
        real(real64), dimension(size(A, 2), size(A, 2)) :: ATA
        real(real64) :: eigenvalue
        real(real64), dimension(size(A, 2)) :: eigenvector
        integer(int32) :: i, n

        n = size(A, 2)

        ! Compute A^T * A
        ATA = matmul(transpose(A), A)

        ! Find eigenvalues of A^T * A (simplified - using power method)
        do i = 1, size(singular_values)
            call eigenvalues_power_method(ATA, eigenvalue, eigenvector, 100, 1.0e-6_real64)
            singular_values(i) = sqrt(abs(eigenvalue))

            ! Deflate matrix (simplified)
            ATA = ATA - eigenvalue * matmul(reshape(eigenvector, [n, 1]), &
                                           reshape(eigenvector, [1, n]))
        end do

    end subroutine svd_simple

end module matrix_module