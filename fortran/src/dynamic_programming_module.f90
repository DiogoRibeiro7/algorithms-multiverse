! Dynamic Programming Algorithms Module
! Classic DP problems and solutions

module dynamic_programming_module
    use iso_fortran_env, only: int32, int64, real32, real64
    implicit none
    private

    ! Public interfaces
    public :: fibonacci_dp, knapsack, longest_common_subsequence
    public :: edit_distance, matrix_chain_multiplication
    public :: coin_change, longest_increasing_subsequence
    public :: maximum_subarray_sum, rod_cutting
    public :: subset_sum, palindrome_partitioning
    public :: optimal_binary_search_tree, word_break

    ! Type for knapsack items
    type, public :: item_type
        integer(int32) :: weight
        integer(int32) :: value
    end type item_type

    ! Type for matrix chain
    type, public :: matrix_dim
        integer(int32) :: rows
        integer(int32) :: cols
    end type matrix_dim

contains

    !===============================================
    ! Fibonacci with Dynamic Programming
    !===============================================

    function fibonacci_dp(n) result(fib)
        implicit none
        integer(int32), intent(in) :: n
        integer(int64) :: fib
        integer(int64), dimension(:), allocatable :: dp
        integer(int32) :: i

        if (n <= 0) then
            fib = 0
            return
        else if (n == 1) then
            fib = 1
            return
        end if

        allocate(dp(0:n))
        dp(0) = 0
        dp(1) = 1

        do i = 2, n
            dp(i) = dp(i-1) + dp(i-2)
        end do

        fib = dp(n)
        deallocate(dp)

    end function fibonacci_dp

    !===============================================
    ! 0/1 Knapsack Problem
    !===============================================

    function knapsack(items, capacity) result(max_value)
        implicit none
        type(item_type), dimension(:), intent(in) :: items
        integer(int32), intent(in) :: capacity
        integer(int32) :: max_value
        integer(int32), dimension(:,:), allocatable :: dp
        integer(int32) :: n, i, w

        n = size(items)
        allocate(dp(0:n, 0:capacity))

        ! Initialize base cases
        dp = 0

        ! Fill the DP table
        do i = 1, n
            do w = 0, capacity
                if (items(i)%weight <= w) then
                    dp(i, w) = max(dp(i-1, w), &
                                  dp(i-1, w - items(i)%weight) + items(i)%value)
                else
                    dp(i, w) = dp(i-1, w)
                end if
            end do
        end do

        max_value = dp(n, capacity)
        deallocate(dp)

    end function knapsack

    !===============================================
    ! Longest Common Subsequence
    !===============================================

    function longest_common_subsequence(str1, str2) result(lcs_length)
        implicit none
        character(len=*), intent(in) :: str1, str2
        integer(int32) :: lcs_length
        integer(int32), dimension(:,:), allocatable :: dp
        integer(int32) :: m, n, i, j

        m = len_trim(str1)
        n = len_trim(str2)
        allocate(dp(0:m, 0:n))

        ! Initialize base cases
        dp = 0

        ! Fill the DP table
        do i = 1, m
            do j = 1, n
                if (str1(i:i) == str2(j:j)) then
                    dp(i, j) = dp(i-1, j-1) + 1
                else
                    dp(i, j) = max(dp(i-1, j), dp(i, j-1))
                end if
            end do
        end do

        lcs_length = dp(m, n)
        deallocate(dp)

    end function longest_common_subsequence

    !===============================================
    ! Edit Distance (Levenshtein Distance)
    !===============================================

    function edit_distance(str1, str2) result(distance)
        implicit none
        character(len=*), intent(in) :: str1, str2
        integer(int32) :: distance
        integer(int32), dimension(:,:), allocatable :: dp
        integer(int32) :: m, n, i, j, cost

        m = len_trim(str1)
        n = len_trim(str2)
        allocate(dp(0:m, 0:n))

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

                dp(i, j) = min(dp(i-1, j) + 1,        &  ! deletion
                              dp(i, j-1) + 1,          &  ! insertion
                              dp(i-1, j-1) + cost)        ! substitution
            end do
        end do

        distance = dp(m, n)
        deallocate(dp)

    end function edit_distance

    !===============================================
    ! Matrix Chain Multiplication
    !===============================================

    function matrix_chain_multiplication(matrices) result(min_ops)
        implicit none
        type(matrix_dim), dimension(:), intent(in) :: matrices
        integer(int64) :: min_ops
        integer(int64), dimension(:,:), allocatable :: dp
        integer(int32) :: n, i, j, k, l
        integer(int64) :: cost

        n = size(matrices)
        allocate(dp(n, n))

        ! Initialize diagonal to 0
        dp = 0

        ! l is chain length
        do l = 2, n
            do i = 1, n - l + 1
                j = i + l - 1
                dp(i, j) = huge(min_ops)

                do k = i, j - 1
                    cost = dp(i, k) + dp(k+1, j) + &
                          int(matrices(i)%rows, int64) * &
                          int(matrices(k)%cols, int64) * &
                          int(matrices(j)%cols, int64)

                    if (cost < dp(i, j)) then
                        dp(i, j) = cost
                    end if
                end do
            end do
        end do

        min_ops = dp(1, n)
        deallocate(dp)

    end function matrix_chain_multiplication

    !===============================================
    ! Coin Change Problem
    !===============================================

    function coin_change(coins, amount) result(min_coins)
        implicit none
        integer(int32), dimension(:), intent(in) :: coins
        integer(int32), intent(in) :: amount
        integer(int32) :: min_coins
        integer(int32), dimension(:), allocatable :: dp
        integer(int32) :: i, j, n

        n = size(coins)
        allocate(dp(0:amount))

        ! Initialize DP array
        dp(0) = 0
        dp(1:) = huge(min_coins) / 2  ! Large value but avoid overflow

        ! Fill DP array
        do i = 1, amount
            do j = 1, n
                if (coins(j) <= i) then
                    dp(i) = min(dp(i), dp(i - coins(j)) + 1)
                end if
            end do
        end do

        if (dp(amount) >= huge(min_coins) / 2) then
            min_coins = -1  ! No solution
        else
            min_coins = dp(amount)
        end if

        deallocate(dp)

    end function coin_change

    !===============================================
    ! Longest Increasing Subsequence
    !===============================================

    function longest_increasing_subsequence(arr) result(lis_length)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32) :: lis_length
        integer(int32), dimension(:), allocatable :: dp
        integer(int32) :: n, i, j

        n = size(arr)
        if (n == 0) then
            lis_length = 0
            return
        end if

        allocate(dp(n))
        dp = 1  ! Every element is a subsequence of length 1

        do i = 2, n
            do j = 1, i - 1
                if (arr(j) < arr(i)) then
                    dp(i) = max(dp(i), dp(j) + 1)
                end if
            end do
        end do

        lis_length = maxval(dp)
        deallocate(dp)

    end function longest_increasing_subsequence

    !===============================================
    ! Maximum Subarray Sum (Kadane's Algorithm)
    !===============================================

    function maximum_subarray_sum(arr) result(max_sum)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int64) :: max_sum
        integer(int64) :: current_sum
        integer(int32) :: i, n

        n = size(arr)
        if (n == 0) then
            max_sum = 0
            return
        end if

        max_sum = arr(1)
        current_sum = arr(1)

        do i = 2, n
            current_sum = max(int(arr(i), int64), current_sum + int(arr(i), int64))
            max_sum = max(max_sum, current_sum)
        end do

    end function maximum_subarray_sum

    !===============================================
    ! Rod Cutting Problem
    !===============================================

    function rod_cutting(prices, length) result(max_value)
        implicit none
        integer(int32), dimension(:), intent(in) :: prices
        integer(int32), intent(in) :: length
        integer(int32) :: max_value
        integer(int32), dimension(:), allocatable :: dp
        integer(int32) :: i, j

        allocate(dp(0:length))
        dp(0) = 0

        do i = 1, length
            dp(i) = 0
            do j = 1, min(i, size(prices))
                dp(i) = max(dp(i), prices(j) + dp(i - j))
            end do
        end do

        max_value = dp(length)
        deallocate(dp)

    end function rod_cutting

    !===============================================
    ! Subset Sum Problem
    !===============================================

    function subset_sum(arr, target_sum) result(possible)
        implicit none
        integer(int32), dimension(:), intent(in) :: arr
        integer(int32), intent(in) :: target_sum
        logical :: possible
        logical, dimension(:,:), allocatable :: dp
        integer(int32) :: n, i, j

        n = size(arr)
        allocate(dp(0:n, 0:target_sum))

        ! Initialize base cases
        dp(:, 0) = .true.   ! Sum of 0 is always possible
        dp(0, 1:) = .false.  ! Non-zero sum with 0 elements is impossible

        ! Fill DP table
        do i = 1, n
            do j = 1, target_sum
                dp(i, j) = dp(i-1, j)  ! Exclude current element
                if (arr(i) <= j) then
                    dp(i, j) = dp(i, j) .or. dp(i-1, j - arr(i))  ! Include current element
                end if
            end do
        end do

        possible = dp(n, target_sum)
        deallocate(dp)

    end function subset_sum

    !===============================================
    ! Palindrome Partitioning (Minimum Cuts)
    !===============================================

    function palindrome_partitioning(str) result(min_cuts)
        implicit none
        character(len=*), intent(in) :: str
        integer(int32) :: min_cuts
        integer(int32) :: n, i, j, k
        logical, dimension(:,:), allocatable :: is_palindrome
        integer(int32), dimension(:), allocatable :: cuts

        n = len_trim(str)
        allocate(is_palindrome(n, n))
        allocate(cuts(n))

        ! Build palindrome table
        is_palindrome = .false.

        ! Single characters are palindromes
        do i = 1, n
            is_palindrome(i, i) = .true.
        end do

        ! Two character palindromes
        do i = 1, n - 1
            if (str(i:i) == str(i+1:i+1)) then
                is_palindrome(i, i+1) = .true.
            end if
        end do

        ! Longer palindromes
        do k = 3, n
            do i = 1, n - k + 1
                j = i + k - 1
                if (str(i:i) == str(j:j) .and. is_palindrome(i+1, j-1)) then
                    is_palindrome(i, j) = .true.
                end if
            end do
        end do

        ! Calculate minimum cuts
        do i = 1, n
            if (is_palindrome(1, i)) then
                cuts(i) = 0
            else
                cuts(i) = huge(min_cuts) / 2
                do j = 1, i - 1
                    if (is_palindrome(j+1, i)) then
                        cuts(i) = min(cuts(i), cuts(j) + 1)
                    end if
                end do
            end if
        end do

        min_cuts = cuts(n)
        deallocate(is_palindrome)
        deallocate(cuts)

    end function palindrome_partitioning

    !===============================================
    ! Optimal Binary Search Tree
    !===============================================

    function optimal_binary_search_tree(keys, freq) result(min_cost)
        implicit none
        integer(int32), dimension(:), intent(in) :: keys
        integer(int32), dimension(:), intent(in) :: freq
        integer(int32) :: min_cost
        integer(int32), dimension(:,:), allocatable :: cost
        integer(int32), dimension(:), allocatable :: prefix_sum
        integer(int32) :: n, i, j, k, l, temp_cost

        n = size(keys)
        allocate(cost(0:n, 0:n))
        allocate(prefix_sum(0:n))

        ! Calculate prefix sums
        prefix_sum(0) = 0
        do i = 1, n
            prefix_sum(i) = prefix_sum(i-1) + freq(i)
        end do

        ! Initialize cost matrix
        cost = 0

        ! Single keys
        do i = 1, n
            cost(i-1, i) = freq(i)
        end do

        ! Build cost matrix for all subtrees
        do l = 2, n
            do i = 0, n - l
                j = i + l
                cost(i, j) = huge(min_cost) / 2

                ! Try all roots
                do k = i + 1, j
                    temp_cost = cost(i, k-1) + cost(k, j)
                    if (temp_cost < cost(i, j)) then
                        cost(i, j) = temp_cost
                    end if
                end do

                ! Add sum of frequencies
                cost(i, j) = cost(i, j) + prefix_sum(j) - prefix_sum(i)
            end do
        end do

        min_cost = cost(0, n)
        deallocate(cost)
        deallocate(prefix_sum)

    end function optimal_binary_search_tree

    !===============================================
    ! Word Break Problem
    !===============================================

    function word_break(str, dictionary) result(can_break)
        implicit none
        character(len=*), intent(in) :: str
        character(len=*), dimension(:), intent(in) :: dictionary
        logical :: can_break
        logical, dimension(:), allocatable :: dp
        integer(int32) :: n, i, j, dict_size, k
        character(len=:), allocatable :: substr

        n = len_trim(str)
        dict_size = size(dictionary)
        allocate(dp(0:n))

        dp(0) = .true.
        dp(1:) = .false.

        do i = 1, n
            do j = 0, i - 1
                if (dp(j)) then
                    ! Check if substring is in dictionary
                    allocate(character(len=i-j) :: substr)
                    substr = str(j+1:i)

                    do k = 1, dict_size
                        if (trim(substr) == trim(dictionary(k))) then
                            dp(i) = .true.
                            exit
                        end if
                    end do

                    deallocate(substr)
                    if (dp(i)) exit
                end if
            end do
        end do

        can_break = dp(n)
        deallocate(dp)

    end function word_break

end module dynamic_programming_module