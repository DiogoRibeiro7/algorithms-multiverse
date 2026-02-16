"""
    DynamicProgramming

Module containing dynamic programming algorithms implemented in Julia.
"""
module DynamicProgramming

export fibonacci, lcs, lis, knapsack, coin_change, edit_distance,
       max_subarray, matrix_chain_multiplication, longest_palindrome,
       word_break, egg_drop, house_robber

"""
    fibonacci(n::Int)

Calculate the n-th Fibonacci number using dynamic programming.
Time: O(n), Space: O(1)
"""
function fibonacci(n::Int)
    if n <= 1
        return n
    end

    prev, curr = 0, 1
    for _ in 2:n
        prev, curr = curr, prev + curr
    end

    return curr
end

"""
    lcs(s1::String, s2::String)

Find the longest common subsequence of two strings.
Time: O(mn), Space: O(mn)
"""
function lcs(s1::String, s2::String)
    m, n = length(s1), length(s2)
    dp = zeros(Int, m + 1, n + 1)

    for i in 1:m
        for j in 1:n
            if s1[i] == s2[j]
                dp[i + 1, j + 1] = dp[i, j] + 1
            else
                dp[i + 1, j + 1] = max(dp[i, j + 1], dp[i + 1, j])
            end
        end
    end

    # Reconstruct LCS
    lcs_str = ""
    i, j = m, n
    while i > 0 && j > 0
        if s1[i] == s2[j]
            lcs_str = s1[i] * lcs_str
            i -= 1
            j -= 1
        elseif dp[i, j + 1] > dp[i + 1, j]
            i -= 1
        else
            j -= 1
        end
    end

    return (length=dp[m + 1, n + 1], string=lcs_str)
end

"""
    lis(arr::Vector{T}) where T

Find the longest increasing subsequence.
Time: O(n²), Space: O(n)
"""
function lis(arr::Vector{T}) where T
    n = length(arr)
    if n == 0
        return (length=0, sequence=T[])
    end

    dp = ones(Int, n)
    parent = fill(-1, n)

    for i in 2:n
        for j in 1:i-1
            if arr[j] < arr[i] && dp[j] + 1 > dp[i]
                dp[i] = dp[j] + 1
                parent[i] = j
            end
        end
    end

    # Find maximum length and reconstruct
    max_length = maximum(dp)
    max_idx = findfirst(==(max_length), dp)

    # Reconstruct LIS
    lis_seq = T[]
    idx = max_idx
    while idx != -1
        pushfirst!(lis_seq, arr[idx])
        idx = parent[idx]
    end

    return (length=max_length, sequence=lis_seq)
end

"""
    knapsack(weights::Vector{Int}, values::Vector{Int}, capacity::Int)

Solve the 0/1 knapsack problem.
Time: O(nW), Space: O(nW)
"""
function knapsack(weights::Vector{Int}, values::Vector{Int}, capacity::Int)
    n = length(weights)
    dp = zeros(Int, n + 1, capacity + 1)

    for i in 1:n
        for w in 1:capacity
            if weights[i] <= w
                dp[i + 1, w + 1] = max(
                    dp[i, w + 1],
                    dp[i, w - weights[i] + 1] + values[i]
                )
            else
                dp[i + 1, w + 1] = dp[i, w + 1]
            end
        end
    end

    # Reconstruct selected items
    selected = Int[]
    w = capacity
    for i in n:-1:1
        if dp[i + 1, w + 1] != dp[i, w + 1]
            push!(selected, i)
            w -= weights[i]
        end
    end

    return (max_value=dp[n + 1, capacity + 1], items=reverse(selected))
end

"""
    coin_change(coins::Vector{Int}, amount::Int)

Find minimum coins needed to make the amount.
Time: O(n*amount), Space: O(amount)
"""
function coin_change(coins::Vector{Int}, amount::Int)
    dp = fill(amount + 1, amount + 1)
    dp[1] = 0  # 0 coins for amount 0

    for i in 1:amount
        for coin in coins
            if coin <= i
                dp[i + 1] = min(dp[i + 1], dp[i - coin + 1] + 1)
            end
        end
    end

    return dp[amount + 1] > amount ? -1 : dp[amount + 1]
end

"""
    edit_distance(s1::String, s2::String)

Calculate the edit distance (Levenshtein distance) between two strings.
Time: O(mn), Space: O(mn)
"""
function edit_distance(s1::String, s2::String)
    m, n = length(s1), length(s2)
    dp = zeros(Int, m + 1, n + 1)

    # Initialize base cases
    for i in 0:m
        dp[i + 1, 1] = i
    end
    for j in 0:n
        dp[1, j + 1] = j
    end

    # Fill DP table
    for i in 1:m
        for j in 1:n
            if s1[i] == s2[j]
                dp[i + 1, j + 1] = dp[i, j]
            else
                dp[i + 1, j + 1] = 1 + min(
                    dp[i, j + 1],      # Delete
                    dp[i + 1, j],      # Insert
                    dp[i, j]           # Replace
                )
            end
        end
    end

    return dp[m + 1, n + 1]
end

"""
    max_subarray(arr::Vector{T}) where T <: Number

Find maximum subarray sum using Kadane's algorithm.
Time: O(n), Space: O(1)
"""
function max_subarray(arr::Vector{T}) where T <: Number
    if isempty(arr)
        return (sum=zero(T), start=0, finish=0)
    end

    max_sum = current_sum = arr[1]
    start = temp_start = 1
    finish = 1

    for i in 2:length(arr)
        if current_sum < 0
            current_sum = arr[i]
            temp_start = i
        else
            current_sum += arr[i]
        end

        if current_sum > max_sum
            max_sum = current_sum
            start = temp_start
            finish = i
        end
    end

    return (sum=max_sum, start=start, finish=finish)
end

"""
    matrix_chain_multiplication(dimensions::Vector{Int})

Find minimum scalar multiplications needed for matrix chain.
Time: O(n³), Space: O(n²)
"""
function matrix_chain_multiplication(dimensions::Vector{Int})
    n = length(dimensions) - 1
    dp = zeros(Int, n, n)

    for length in 2:n
        for i in 1:n-length+1
            j = i + length - 1
            dp[i, j] = typemax(Int)

            for k in i:j-1
                cost = dp[i, k] + dp[k + 1, j] +
                       dimensions[i] * dimensions[k + 1] * dimensions[j + 1]

                if cost < dp[i, j]
                    dp[i, j] = cost
                end
            end
        end
    end

    return dp[1, n]
end

"""
    longest_palindrome(s::String)

Find the longest palindromic substring.
Time: O(n²), Space: O(n²)
"""
function longest_palindrome(s::String)
    n = length(s)
    if n == 0
        return ""
    end

    dp = falses(n, n)
    start = 1
    max_len = 1

    # Every single character is a palindrome
    for i in 1:n
        dp[i, i] = true
    end

    # Check for length 2
    for i in 1:n-1
        if s[i] == s[i + 1]
            dp[i, i + 1] = true
            start = i
            max_len = 2
        end
    end

    # Check for lengths greater than 2
    for length in 3:n
        for i in 1:n-length+1
            j = i + length - 1

            if s[i] == s[j] && dp[i + 1, j - 1]
                dp[i, j] = true
                start = i
                max_len = length
            end
        end
    end

    return s[start:start+max_len-1]
end

"""
    word_break(s::String, word_dict::Vector{String})

Check if string can be segmented into dictionary words.
Time: O(n²), Space: O(n)
"""
function word_break(s::String, word_dict::Vector{String})
    n = length(s)
    dp = falses(n + 1)
    dp[1] = true  # Empty string

    word_set = Set(word_dict)

    for i in 1:n
        for j in i:n
            if dp[i] && s[i:j] in word_set
                dp[j + 1] = true
            end
        end
    end

    return dp[n + 1]
end

"""
    egg_drop(eggs::Int, floors::Int)

Find minimum trials needed in worst case for egg drop problem.
Time: O(eggs * floors²), Space: O(eggs * floors)
"""
function egg_drop(eggs::Int, floors::Int)
    dp = zeros(Int, eggs + 1, floors + 1)

    # Base cases
    for j in 1:floors
        dp[2, j + 1] = j  # 1 egg, j floors
    end
    for i in 1:eggs
        dp[i + 1, 2] = 1  # i eggs, 1 floor
    end

    # Fill table
    for i in 2:eggs
        for j in 2:floors
            dp[i + 1, j + 1] = typemax(Int)

            for k in 1:j
                # If egg breaks, check floors below
                # If egg doesn't break, check floors above
                res = 1 + max(dp[i, k], dp[i + 1, j - k + 1])
                dp[i + 1, j + 1] = min(dp[i + 1, j + 1], res)
            end
        end
    end

    return dp[eggs + 1, floors + 1]
end

"""
    house_robber(houses::Vector{Int})

Find maximum money that can be robbed without robbing adjacent houses.
Time: O(n), Space: O(1)
"""
function house_robber(houses::Vector{Int})
    if isempty(houses)
        return 0
    elseif length(houses) == 1
        return houses[1]
    end

    prev = houses[1]
    curr = max(houses[1], houses[2])

    for i in 3:length(houses)
        prev, curr = curr, max(curr, prev + houses[i])
    end

    return curr
end

end # module DynamicProgramming