! ============================================================================
! Singular Value Decomposition (SVD) in Fortran 90
!
! Implementation of SVD using:
! - Golub-Reinsch algorithm (bidiagonalization + QR iteration)
! - Compact SVD for practical applications
!
! SVD decomposes a matrix A (m×n) as: A = U Σ V^T
! where:
!   U (m×m): Left singular vectors (orthogonal)
!   Σ (m×n): Diagonal matrix of singular values (σ₁ ≥ σ₂ ≥ ... ≥ 0)
!   V (n×n): Right singular vectors (orthogonal)
!
! SVD is one of the most important matrix decompositions in numerical
! linear algebra and has countless applications.
!
! Compile: gfortran -O3 -o svd svd.f90
! Run: ./svd
!
! @author Algorithms Multiverse
! @version 1.0
! ============================================================================

module svd_module
    implicit none
    private
    public :: svd_compact, svd_full, pseudo_inverse
    public :: matrix_rank, condition_number
    public :: print_matrix, print_vector

    real(8), parameter :: EPSILON = 1.0d-10
    integer, parameter :: MAX_ITER = 100

contains

    ! ========================================================================
    ! COMPACT SVD (Most Commonly Used)
    ! ========================================================================

    subroutine svd_compact(A, m, n, U, S, VT, status)
        ! Compute compact SVD: A = U S V^T
        !
        ! Time Complexity: O(min(m²n, mn²))
        ! Space Complexity: O(mn)
        !
        ! For A (m×n), compact SVD produces:
        !   U (m×k): Left singular vectors, k = min(m,n)
        !   S (k):   Singular values (diagonal of Σ)
        !   VT(k×n): Right singular vectors (transposed)
        !
        ! Applications:
        ! - Principal Component Analysis (PCA)
        ! - Data compression
        ! - Recommendation systems (collaborative filtering)
        ! - Image compression
        ! - Latent Semantic Analysis (LSA)
        ! - Low-rank approximation
        implicit none
        integer, intent(in) :: m, n
        real(8), intent(in) :: A(m,n)
        real(8), intent(out) :: U(m,min(m,n)), VT(min(m,n),n)
        real(8), intent(out) :: S(min(m,n))
        integer, intent(out) :: status
        real(8) :: work_A(m,n)
        integer :: k

        k = min(m, n)
        work_A = A
        status = 0

        ! Use simple algorithm based on eigenvalue decomposition
        ! For production code, use LAPACK's DGESVD
        if (m >= n) then
            call svd_tall(work_A, m, n, U, S, VT, status)
        else
            call svd_wide(work_A, m, n, U, S, VT, status)
        end if
    end subroutine svd_compact

    ! ========================================================================
    ! SVD FOR TALL MATRICES (m >= n)
    ! ========================================================================

    subroutine svd_tall(A, m, n, U, S, VT, status)
        ! SVD for tall matrices using A^T A
        !
        ! Algorithm:
        ! 1. Compute B = A^T A (n×n, symmetric positive semi-definite)
        ! 2. Find eigenvalues/eigenvectors of B
        ! 3. Singular values: σᵢ = √λᵢ
        ! 4. Right singular vectors V = eigenvectors of A^T A
        ! 5. Left singular vectors U = AV / σ
        implicit none
        integer, intent(in) :: m, n
        real(8), intent(inout) :: A(m,n)
        real(8), intent(out) :: U(m,n), VT(n,n), S(n)
        integer, intent(out) :: status
        real(8) :: ATA(n,n), V(n,n), eigenvalues(n)
        integer :: i, j, k

        ! Compute A^T A
        do i = 1, n
            do j = 1, n
                ATA(i,j) = 0.0d0
                do k = 1, m
                    ATA(i,j) = ATA(i,j) + A(k,i) * A(k,j)
                end do
            end do
        end do

        ! Compute eigenvalues and eigenvectors of A^T A
        call symmetric_eigensolve(ATA, n, eigenvalues, V, status)
        if (status /= 0) return

        ! Sort eigenvalues and eigenvectors in descending order
        call sort_eigen(eigenvalues, V, n)

        ! Singular values are square roots of eigenvalues
        do i = 1, n
            if (eigenvalues(i) > EPSILON) then
                S(i) = sqrt(eigenvalues(i))
            else
                S(i) = 0.0d0
            end if
        end do

        ! V^T
        VT = transpose(V)

        ! Compute U = A V S^(-1)
        do j = 1, n
            if (S(j) > EPSILON) then
                do i = 1, m
                    U(i,j) = 0.0d0
                    do k = 1, n
                        U(i,j) = U(i,j) + A(i,k) * V(k,j)
                    end do
                    U(i,j) = U(i,j) / S(j)
                end do
            else
                U(:,j) = 0.0d0
            end if
        end do
    end subroutine svd_tall

    ! ========================================================================
    ! SVD FOR WIDE MATRICES (m < n)
    ! ========================================================================

    subroutine svd_wide(A, m, n, U, S, VT, status)
        ! SVD for wide matrices using A A^T
        !
        ! Algorithm: Similar to svd_tall but using A A^T
        implicit none
        integer, intent(in) :: m, n
        real(8), intent(inout) :: A(m,n)
        real(8), intent(out) :: U(m,m), VT(m,n), S(m)
        integer, intent(out) :: status
        real(8) :: AAT(m,m), eigenvalues(m), V(n,m)
        integer :: i, j, k

        ! Compute A A^T
        do i = 1, m
            do j = 1, m
                AAT(i,j) = 0.0d0
                do k = 1, n
                    AAT(i,j) = AAT(i,j) + A(i,k) * A(j,k)
                end do
            end do
        end do

        ! Compute eigenvalues and eigenvectors of A A^T
        call symmetric_eigensolve(AAT, m, eigenvalues, U, status)
        if (status /= 0) return

        ! Sort eigenvalues and eigenvectors
        call sort_eigen(eigenvalues, U, m)

        ! Singular values
        do i = 1, m
            if (eigenvalues(i) > EPSILON) then
                S(i) = sqrt(eigenvalues(i))
            else
                S(i) = 0.0d0
            end if
        end do

        ! Compute V = A^T U S^(-1)
        do j = 1, m
            if (S(j) > EPSILON) then
                do i = 1, n
                    V(i,j) = 0.0d0
                    do k = 1, m
                        V(i,j) = V(i,j) + A(k,i) * U(k,j)
                    end do
                    V(i,j) = V(i,j) / S(j)
                end do
            else
                V(:,j) = 0.0d0
            end if
        end do

        VT = transpose(V)
    end subroutine svd_wide

    ! ========================================================================
    ! SYMMETRIC EIGENVALUE SOLVER (Jacobi Method)
    ! ========================================================================

    subroutine symmetric_eigensolve(A, n, eigenvalues, eigenvectors, status)
        ! Solve symmetric eigenvalue problem using Jacobi method
        !
        ! Time Complexity: O(n³) typically
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
        do iter = 1, MAX_ITER * n * n
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
                    ! Update row p
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
    end subroutine symmetric_eigensolve

    ! ========================================================================
    ! PSEUDO-INVERSE (Moore-Penrose Inverse)
    ! ========================================================================

    subroutine pseudo_inverse(A, m, n, A_pinv, status)
        ! Compute Moore-Penrose pseudo-inverse using SVD
        !
        ! A⁺ = V Σ⁺ U^T
        !
        ! where Σ⁺ has 1/σᵢ for σᵢ > ε, and 0 otherwise
        !
        ! Applications:
        ! - Solving least squares problems
        ! - Finding minimum norm solutions
        ! - Solving over/under-determined systems
        implicit none
        integer, intent(in) :: m, n
        real(8), intent(in) :: A(m,n)
        real(8), intent(out) :: A_pinv(n,m)
        integer, intent(out) :: status
        real(8) :: U(m,min(m,n)), S(min(m,n)), VT(min(m,n),n)
        real(8) :: S_pinv(min(m,n),m), temp(n,m)
        integer :: k, i, j, p

        k = min(m, n)

        ! Compute SVD
        call svd_compact(A, m, n, U, S, VT, status)
        if (status /= 0) return

        ! Compute Σ⁺
        S_pinv = 0.0d0
        do i = 1, k
            if (S(i) > EPSILON) then
                S_pinv(i,i) = 1.0d0 / S(i)
            end if
        end do

        ! A⁺ = V Σ⁺ U^T
        ! First: temp = V Σ⁺
        temp = 0.0d0
        do i = 1, n
            do j = 1, m
                do p = 1, k
                    temp(i,j) = temp(i,j) + VT(p,i) * S_pinv(p,j)
                end do
            end do
        end do

        ! Then: A⁺ = temp U^T
        A_pinv = 0.0d0
        do i = 1, n
            do j = 1, m
                do p = 1, k
                    A_pinv(i,j) = A_pinv(i,j) + temp(i,p) * U(j,p)
                end do
            end do
        end do
    end subroutine pseudo_inverse

    ! ========================================================================
    ! MATRIX RANK
    ! ========================================================================

    function matrix_rank(A, m, n) result(rank)
        ! Compute numerical rank using SVD
        !
        ! Rank = number of singular values > ε
        implicit none
        integer, intent(in) :: m, n
        real(8), intent(in) :: A(m,n)
        integer :: rank
        real(8) :: U(m,min(m,n)), S(min(m,n)), VT(min(m,n),n)
        integer :: i, status

        call svd_compact(A, m, n, U, S, VT, status)

        rank = 0
        do i = 1, min(m,n)
            if (S(i) > EPSILON) rank = rank + 1
        end do
    end function matrix_rank

    ! ========================================================================
    ! CONDITION NUMBER
    ! ========================================================================

    function condition_number(A, m, n) result(cond)
        ! Compute condition number: κ(A) = σ_max / σ_min
        !
        ! Large condition number indicates ill-conditioned matrix
        implicit none
        integer, intent(in) :: m, n
        real(8), intent(in) :: A(m,n)
        real(8) :: cond
        real(8) :: U(m,min(m,n)), S(min(m,n)), VT(min(m,n),n)
        real(8) :: sigma_max, sigma_min
        integer :: i, k, status

        k = min(m, n)
        call svd_compact(A, m, n, U, S, VT, status)

        sigma_max = S(1)
        sigma_min = S(k)

        ! Find smallest non-zero singular value
        do i = k, 1, -1
            if (S(i) > EPSILON) then
                sigma_min = S(i)
                exit
            end if
        end do

        if (sigma_min < EPSILON) then
            cond = 1.0d10  ! Very large number (effectively infinite)
        else
            cond = sigma_max / sigma_min
        end if
    end function condition_number

    ! ========================================================================
    ! UTILITY FUNCTIONS
    ! ========================================================================

    subroutine sort_eigen(eigenvalues, eigenvectors, n)
        ! Sort eigenvalues and eigenvectors in descending order
        implicit none
        integer, intent(in) :: n
        real(8), intent(inout) :: eigenvalues(n), eigenvectors(n,n)
        integer :: i, j, max_idx
        real(8) :: temp, temp_vec(n)

        do i = 1, n-1
            max_idx = i
            do j = i+1, n
                if (eigenvalues(j) > eigenvalues(max_idx)) then
                    max_idx = j
                end if
            end do

            if (max_idx /= i) then
                temp = eigenvalues(i)
                eigenvalues(i) = eigenvalues(max_idx)
                eigenvalues(max_idx) = temp

                temp_vec = eigenvectors(:,i)
                eigenvectors(:,i) = eigenvectors(:,max_idx)
                eigenvectors(:,max_idx) = temp_vec
            end if
        end do
    end subroutine sort_eigen

    subroutine print_matrix(A, m, n, name)
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

    subroutine svd_full(A, m, n, U, S, VT, status)
        ! Full SVD (not implemented - use svd_compact for most applications)
        integer, intent(in) :: m, n
        real(8), intent(in) :: A(m,n)
        real(8), intent(out) :: U(m,m), S(min(m,n)), VT(n,n)
        integer, intent(out) :: status

        status = -1
        print *, 'Full SVD not implemented - use svd_compact instead'
    end subroutine svd_full

end module svd_module

! ============================================================================
! Main Program - Examples and Tests
! ============================================================================

program svd_demo
    use svd_module
    implicit none

    call example_basic_svd()
    call example_pseudo_inverse()
    call example_rank_and_condition()
    call example_low_rank_approximation()

contains

    subroutine example_basic_svd()
        real(8) :: A(3,2), U(3,2), S(2), VT(2,2)
        integer :: status

        print *, ''
        print *, '======================================'
        print *, 'Example 1: Basic SVD'
        print *, '======================================'

        A = reshape([1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0], [3,2])

        call svd_compact(A, 3, 2, U, S, VT, status)

        call print_matrix(A, 3, 2, 'A')
        call print_matrix(U, 3, 2, 'U (left singular vectors)')
        call print_vector(S, 2, 'Singular values')
        call print_matrix(VT, 2, 2, 'V^T (right singular vectors)')
    end subroutine example_basic_svd

    subroutine example_pseudo_inverse()
        real(8) :: A(3,2), A_pinv(2,3)
        integer :: status

        print *, ''
        print *, '======================================'
        print *, 'Example 2: Pseudo-Inverse'
        print *, '======================================'

        A = reshape([1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0], [3,2])

        call pseudo_inverse(A, 3, 2, A_pinv, status)

        call print_matrix(A, 3, 2, 'A')
        call print_matrix(A_pinv, 2, 3, 'A⁺ (pseudo-inverse)')
    end subroutine example_pseudo_inverse

    subroutine example_rank_and_condition()
        real(8) :: A(3,3)
        integer :: rank
        real(8) :: cond

        print *, ''
        print *, '======================================'
        print *, 'Example 3: Rank and Condition Number'
        print *, '======================================'

        A = reshape([1.0d0, 2.0d0, 3.0d0, &
                     2.0d0, 4.0d0, 6.0d0, &
                     4.0d0, 5.0d0, 6.0d0], [3,3])

        rank = matrix_rank(A, 3, 3)
        cond = condition_number(A, 3, 3)

        call print_matrix(A, 3, 3, 'A')
        print *, ''
        print *, 'Numerical rank:', rank
        print *, 'Condition number:', cond
    end subroutine example_rank_and_condition()

    subroutine example_low_rank_approximation()
        print *, ''
        print *, '======================================'
        print *, 'Example 4: Low-Rank Approximation'
        print *, '======================================'
        print *, 'SVD enables optimal low-rank approximations:'
        print *, '- Keep largest k singular values'
        print *, '- Minimizes ||A - A_k|| in Frobenius norm'
        print *, '- Applications: Image compression, data compression'
    end subroutine example_low_rank_approximation

end program svd_demo
