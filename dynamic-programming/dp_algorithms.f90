! Dynamic Programming Algorithms in Modern Fortran
!
! Classic DP problems demonstrating optimal substructure and overlapping subproblems:
! 1. Fibonacci Sequence (multiple approaches)
! 2. 0/1 Knapsack Problem
! 3. Longest Common Subsequence (LCS)
! 4. Coin Change Problem
! 5. Edit Distance (Levenshtein Distance)
! 6. Matrix Chain Multiplication
!
! Author: Algorithms Multiverse

program dp_algorithms
    implicit none

    ! Test parameters
    integer, parameter :: MAX_N = 100
    integer, parameter :: MAX_STR = 50

    print '(A)', repeat('=', 75)
    print '(A)', '          DYNAMIC PROGRAMMING ALGORITHMS IN FORTRAN'
    print '(A)', repeat('=', 75)
    print *

    ! Run all DP algorithm demonstrations
    call demo_fibonacci()
    call demo_knapsack()
    call demo_lcs()
    call demo_coin_change()
    call demo_edit_distance()
    call demo_matrix_chain()

    ! Summary
    print '(A)', repeat('=', 75)
    print '(A)', 'DYNAMIC PROGRAMMING PRINCIPLES'
    print '(A)', repeat('=', 75)
    print '(A)', 'Key Concepts:'
    print '(A)', '1. Optimal Substructure: Optimal solution contains optimal subsolutions'
    print '(A)', '2. Overlapping Subproblems: Same subproblems solved multiple times'
    print '(A)', '3. Memoization: Top-down approach storing computed results'
    print '(A)', '4. Tabulation: Bottom-up approach building table iteratively'
    print '(A)', ''
    print '(A)', 'When to Use DP:'
    print '(A)', '- Problem can be broken into overlapping subproblems'
    print '(A)', '- Optimal solution can be constructed from optimal subsolutions'
    print '(A)', '- Brute force would solve same subproblems repeatedly'
    print '(A)', repeat('=', 75)

contains

    ! ===================================================================
    ! FIBONACCI SEQUENCE
    ! ===================================================================

    subroutine demo_fibonacci()
        integer, parameter :: n = 40
        integer(8) :: result
        real(8) :: start_time, end_time
        integer(8) :: memo(0:MAX_N)

        print '(A)', 'Test 1: Fibonacci Sequence'
        print '(A)', repeat('-', 75)
        print '(A, I0)', 'Computing Fibonacci(', n, ') using different approaches:'
        print *

        ! Memoization approach
        memo = -1
        call cpu_time(start_time)
        result = fib_memo(n, memo)
        call cpu_time(end_time)
        print '(A, I0, A, I0, A, F10.6, A)', &
              'Memoization:     F(', n, ') = ', result, &
              ' (', end_time - start_time, ' seconds)'

        ! Tabulation approach
        call cpu_time(start_time)
        result = fib_tabulation(n)
        call cpu_time(end_time)
        print '(A, I0, A, I0, A, F10.6, A)', &
              'Tabulation:      F(', n, ') = ', result, &
              ' (', end_time - start_time, ' seconds)'

        ! Space-optimized approach
        call cpu_time(start_time)
        result = fib_optimized(n)
        call cpu_time(end_time)
        print '(A, I0, A, I0, A, F10.6, A)', &
              'Space-optimized: F(', n, ') = ', result, &
              ' (', end_time - start_time, ' seconds)'

        print *
        print '(A)', 'Complexity: O(n) time for all DP approaches'
        print '(A)', 'Space: O(n) for memoization/tabulation, O(1) for optimized'
        print *
    end subroutine demo_fibonacci

    recursive function fib_memo(n, memo) result(fib)
        integer, intent(in) :: n
        integer(8), intent(inout) :: memo(0:)
        integer(8) :: fib

        if (memo(n) /= -1) then
            fib = memo(n)
            return
        end if

        if (n <= 1) then
            fib = n
        else
            fib = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
        end if

        memo(n) = fib
    end function fib_memo

    function fib_tabulation(n) result(fib)
        integer, intent(in) :: n
        integer(8) :: fib
        integer(8) :: dp(0:MAX_N)
        integer :: i

        if (n <= 1) then
            fib = n
            return
        end if

        dp(0) = 0
        dp(1) = 1

        do i = 2, n
            dp(i) = dp(i - 1) + dp(i - 2)
        end do

        fib = dp(n)
    end function fib_tabulation

    function fib_optimized(n) result(fib)
        integer, intent(in) :: n
        integer(8) :: fib
        integer(8) :: prev2, prev1, curr
        integer :: i

        if (n <= 1) then
            fib = n
            return
        end if

        prev2 = 0
        prev1 = 1

        do i = 2, n
            curr = prev1 + prev2
            prev2 = prev1
            prev1 = curr
        end do

        fib = prev1
    end function fib_optimized

    ! ===================================================================
    ! 0/1 KNAPSACK PROBLEM
    ! ===================================================================

    subroutine demo_knapsack()
        integer, parameter :: n_items = 4
        integer, parameter :: capacity = 50
        integer :: weights(n_items), values(n_items)
        integer :: max_value, i

        print '(A)', 'Test 2: 0/1 Knapsack Problem'
        print '(A)', repeat('-', 75)

        ! Initialize items
        values = [60, 100, 120, 80]
        weights = [10, 20, 30, 25]

        print '(A)', 'Items: {value, weight}'
        do i = 1, n_items
            print '(A, I0, A, I0, A, I0, A)', &
                  '  Item ', i, ': {', values(i), ', ', weights(i), '}'
        end do
        print '(A, I0)', 'Knapsack capacity: ', capacity
        print *

        max_value = knapsack(capacity, weights, values, n_items)

        print '(A, I0)', 'Maximum value: ', max_value
        print *
        print '(A)', 'Complexity: O(nW) time, O(nW) space'
        print '(A)', 'where n = number of items, W = knapsack capacity'
        print *
    end subroutine demo_knapsack

    function knapsack(W, wt, val, n) result(max_val)
        integer, intent(in) :: W, n
        integer, intent(in) :: wt(:), val(:)
        integer :: max_val
        integer :: dp(0:n, 0:W)
        integer :: i, ww

        ! Build table bottom-up
        do i = 0, n
            do ww = 0, W
                if (i == 0 .or. ww == 0) then
                    dp(i, ww) = 0
                else if (wt(i) <= ww) then
                    dp(i, ww) = max(val(i) + dp(i - 1, ww - wt(i)), &
                                   dp(i - 1, ww))
                else
                    dp(i, ww) = dp(i - 1, ww)
                end if
            end do
        end do

        max_val = dp(n, W)
    end function knapsack

    ! ===================================================================
    ! LONGEST COMMON SUBSEQUENCE (LCS)
    ! ===================================================================

    subroutine demo_lcs()
        character(len=20) :: X = 'AGGTAB'
        character(len=20) :: Y = 'GXTXAYB'
        integer :: lcs_len, m, n

        print '(A)', 'Test 3: Longest Common Subsequence (LCS)'
        print '(A)', repeat('-', 75)

        m = len_trim(X)
        n = len_trim(Y)

        print '(A, A)', 'String X: ', trim(X)
        print '(A, A)', 'String Y: ', trim(Y)
        print *

        lcs_len = lcs(X, Y, m, n)

        print '(A, I0)', 'Length of LCS: ', lcs_len
        print '(A)', '(The LCS is "GTAB")'
        print *
        print '(A)', 'Complexity: O(mn) time, O(mn) space'
        print '(A)', 'Can be optimized to O(min(m,n)) space'
        print *
    end subroutine demo_lcs

    function lcs(X, Y, m, n) result(length)
        character(len=*), intent(in) :: X, Y
        integer, intent(in) :: m, n
        integer :: length
        integer :: dp(0:m, 0:n)
        integer :: i, j

        ! Build LCS table
        do i = 0, m
            do j = 0, n
                if (i == 0 .or. j == 0) then
                    dp(i, j) = 0
                else if (X(i:i) == Y(j:j)) then
                    dp(i, j) = dp(i - 1, j - 1) + 1
                else
                    dp(i, j) = max(dp(i - 1, j), dp(i, j - 1))
                end if
            end do
        end do

        length = dp(m, n)
    end function lcs

    ! ===================================================================
    ! COIN CHANGE PROBLEM
    ! ===================================================================

    subroutine demo_coin_change()
        integer, parameter :: n_coins = 4
        integer, parameter :: amount = 63
        integer :: coins(n_coins)
        integer :: min_coins, i

        print '(A)', 'Test 4: Coin Change Problem'
        print '(A)', repeat('-', 75)

        coins = [1, 5, 10, 25]

        print '(A)', 'Coins: {'
        do i = 1, n_coins
            if (i < n_coins) then
                print '(A, I0, A)', '  ', coins(i), ','
            else
                print '(A, I0)', '  ', coins(i)
            end if
        end do
        print '(A)', '}'
        print '(A, I0)', 'Amount: ', amount
        print *

        min_coins = coin_change(coins, n_coins, amount)

        if (min_coins == -1) then
            print '(A)', 'Cannot make change for this amount'
        else
            print '(A, I0)', 'Minimum coins needed: ', min_coins
            print '(A)', '(Solution: 2×25 + 1×10 + 3×1 = 6 coins)'
        end if

        print *
        print '(A)', 'Complexity: O(n×amount) time, O(amount) space'
        print *
    end subroutine demo_coin_change

    function coin_change(coins, n, amount) result(min_coins)
        integer, intent(in) :: n, amount
        integer, intent(in) :: coins(:)
        integer :: min_coins
        integer :: dp(0:amount)
        integer :: i, j

        ! Initialize with infinity (large value)
        dp = amount + 1
        dp(0) = 0

        ! Build up the dp array
        do i = 1, amount
            do j = 1, n
                if (coins(j) <= i) then
                    dp(i) = min(dp(i), dp(i - coins(j)) + 1)
                end if
            end do
        end do

        if (dp(amount) > amount) then
            min_coins = -1
        else
            min_coins = dp(amount)
        end if
    end function coin_change

    ! ===================================================================
    ! EDIT DISTANCE (Levenshtein Distance)
    ! ===================================================================

    subroutine demo_edit_distance()
        character(len=20) :: str1 = 'SUNDAY'
        character(len=20) :: str2 = 'SATURDAY'
        integer :: dist, m, n

        print '(A)', 'Test 5: Edit Distance (Levenshtein Distance)'
        print '(A)', repeat('-', 75)

        m = len_trim(str1)
        n = len_trim(str2)

        print '(A, A)', 'String 1: ', trim(str1)
        print '(A, A)', 'String 2: ', trim(str2)
        print *

        dist = edit_distance(str1, str2, m, n)

        print '(A, I0)', 'Minimum edit distance: ', dist
        print '(A)', 'Operations: Insert, Delete, Replace'
        print '(A)', 'Example transformation:'
        print '(A)', '  SUNDAY → SATURDAY'
        print '(A)', '  Insert "AT" after "S", Insert "R" before last "Y"'
        print *
        print '(A)', 'Complexity: O(mn) time, O(mn) space'
        print '(A)', 'Applications: Spell checking, DNA sequence alignment'
        print *
    end subroutine demo_edit_distance

    function edit_distance(str1, str2, m, n) result(dist)
        character(len=*), intent(in) :: str1, str2
        integer, intent(in) :: m, n
        integer :: dist
        integer :: dp(0:m, 0:n)
        integer :: i, j, cost

        ! Initialize base cases
        do i = 0, m
            dp(i, 0) = i
        end do

        do j = 0, n
            dp(0, j) = j
        end do

        ! Fill the DP table
        do i = 1, m
            do j = 1, n
                if (str1(i:i) == str2(j:j)) then
                    cost = 0
                else
                    cost = 1
                end if

                dp(i, j) = min(min(dp(i - 1, j) + 1,      & ! Delete
                                  dp(i, j - 1) + 1),      & ! Insert
                                  dp(i - 1, j - 1) + cost)  ! Replace
            end do
        end do

        dist = dp(m, n)
    end function edit_distance

    ! ===================================================================
    ! MATRIX CHAIN MULTIPLICATION
    ! ===================================================================

    subroutine demo_matrix_chain()
        integer, parameter :: n_matrices = 4
        integer :: dims(n_matrices + 1)
        integer :: min_ops

        print '(A)', 'Test 6: Matrix Chain Multiplication'
        print '(A)', repeat('-', 75)

        ! Matrix dimensions: A1(10×20), A2(20×30), A3(30×40), A4(40×30)
        dims = [10, 20, 30, 40, 30]

        print '(A)', 'Matrix dimensions:'
        print '(A)', '  A1: 10×20'
        print '(A)', '  A2: 20×30'
        print '(A)', '  A3: 30×40'
        print '(A)', '  A4: 40×30'
        print *

        min_ops = matrix_chain_order(dims, n_matrices)

        print '(A, I0)', 'Minimum scalar multiplications: ', min_ops
        print '(A)', 'Optimal parenthesization reduces operations significantly'
        print *
        print '(A)', 'Complexity: O(n³) time, O(n²) space'
        print '(A)', 'Classic example of optimal substructure'
        print *
    end subroutine demo_matrix_chain

    function matrix_chain_order(p, n) result(min_ops)
        integer, intent(in) :: n
        integer, intent(in) :: p(0:)
        integer :: min_ops
        integer :: dp(n, n)
        integer :: i, j, k, L, q

        ! dp[i,j] = minimum cost to multiply matrices i to j
        dp = 0

        ! L is chain length
        do L = 2, n
            do i = 1, n - L + 1
                j = i + L - 1
                dp(i, j) = huge(1)

                do k = i, j - 1
                    ! Cost of multiplying matrices i..k and k+1..j
                    ! plus cost of multiplying the two resulting matrices
                    q = dp(i, k) + dp(k + 1, j) + p(i - 1) * p(k) * p(j)

                    if (q < dp(i, j)) then
                        dp(i, j) = q
                    end if
                end do
            end do
        end do

        min_ops = dp(1, n)
    end function matrix_chain_order

end program dp_algorithms
