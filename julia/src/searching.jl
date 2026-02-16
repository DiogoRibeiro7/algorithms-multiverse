"""
    Searching

Module containing various search algorithms implemented in Julia.
"""
module Searching

export binary_search, linear_search, jump_search, interpolation_search,
       exponential_search, ternary_search, fibonacci_search,
       find_first, find_last, count_occurrences,
       search_rotated, find_peak, find_min_rotated,
       search_matrix, kth_smallest_matrix

"""
    binary_search(arr::Vector{T}, target::T) where T

Search for target in sorted array using binary search.

# Returns
- Index of target if found, `nothing` otherwise

# Time Complexity
- O(log n)
- Space: O(1)
"""
function binary_search(arr::Vector{T}, target::T) where T
    left, right = 1, length(arr)

    while left <= right
        mid = left + (right - left) ÷ 2

        if arr[mid] == target
            return mid
        elseif arr[mid] < target
            left = mid + 1
        else
            right = mid - 1
        end
    end

    return nothing
end

"""
    binary_search_recursive(arr::Vector{T}, target::T, left::Int=1, right::Int=length(arr)) where T

Recursive binary search implementation.
"""
function binary_search_recursive(arr::Vector{T}, target::T, left::Int=1, right::Int=length(arr)) where T
    if left > right
        return nothing
    end

    mid = left + (right - left) ÷ 2

    if arr[mid] == target
        return mid
    elseif arr[mid] < target
        return binary_search_recursive(arr, target, mid + 1, right)
    else
        return binary_search_recursive(arr, target, left, mid - 1)
    end
end

"""
    linear_search(arr::Vector{T}, target::T) where T

Search for target using linear search.

# Time Complexity
- O(n)
- Space: O(1)
"""
function linear_search(arr::Vector{T}, target::T) where T
    for i in eachindex(arr)
        if arr[i] == target
            return i
        end
    end
    return nothing
end

"""
    jump_search(arr::Vector{T}, target::T) where T

Search for target in sorted array using jump search.

# Time Complexity
- O(√n)
- Space: O(1)
"""
function jump_search(arr::Vector{T}, target::T) where T
    n = length(arr)
    step = Int(floor(sqrt(n)))
    prev = 1

    # Jump to find the block where element is present
    while arr[min(step, n)] < target
        prev = step
        step += Int(floor(sqrt(n)))
        if prev >= n
            return nothing
        end
    end

    # Linear search in the identified block
    while arr[prev] < target
        prev += 1
        if prev == min(step + 1, n + 1)
            return nothing
        end
    end

    return arr[prev] == target ? prev : nothing
end

"""
    interpolation_search(arr::Vector{T}, target::T) where T <: Number

Search for target using interpolation search. Works best with uniformly distributed data.

# Time Complexity
- Average: O(log log n)
- Worst: O(n)
- Space: O(1)
"""
function interpolation_search(arr::Vector{T}, target::T) where T <: Number
    left, right = 1, length(arr)

    while left <= right && target >= arr[left] && target <= arr[right]
        if left == right
            return arr[left] == target ? left : nothing
        end

        # Interpolation formula
        pos = left + Int(floor((target - arr[left]) * (right - left) / (arr[right] - arr[left])))

        if arr[pos] == target
            return pos
        elseif arr[pos] < target
            left = pos + 1
        else
            right = pos - 1
        end
    end

    return nothing
end

"""
    exponential_search(arr::Vector{T}, target::T) where T

Search for target using exponential search.

# Time Complexity
- O(log n)
- Space: O(1)
"""
function exponential_search(arr::Vector{T}, target::T) where T
    if isempty(arr)
        return nothing
    end

    if arr[1] == target
        return 1
    end

    # Find range for binary search
    i = 1
    while i < length(arr) && arr[i] <= target
        i *= 2
    end

    # Binary search in the found range
    return binary_search_range(arr, target, i ÷ 2 + 1, min(i, length(arr)))
end

function binary_search_range(arr::Vector{T}, target::T, left::Int, right::Int) where T
    while left <= right
        mid = left + (right - left) ÷ 2

        if arr[mid] == target
            return mid
        elseif arr[mid] < target
            left = mid + 1
        else
            right = mid - 1
        end
    end

    return nothing
end

"""
    ternary_search(arr::Vector{T}, target::T) where T

Search for target using ternary search (dividing into three parts).

# Time Complexity
- O(log₃ n)
- Space: O(1)
"""
function ternary_search(arr::Vector{T}, target::T) where T
    left, right = 1, length(arr)

    while left <= right
        mid1 = left + (right - left) ÷ 3
        mid2 = right - (right - left) ÷ 3

        if arr[mid1] == target
            return mid1
        elseif arr[mid2] == target
            return mid2
        elseif target < arr[mid1]
            right = mid1 - 1
        elseif target > arr[mid2]
            left = mid2 + 1
        else
            left = mid1 + 1
            right = mid2 - 1
        end
    end

    return nothing
end

"""
    fibonacci_search(arr::Vector{T}, target::T) where T

Search for target using Fibonacci search.

# Time Complexity
- O(log n)
- Space: O(1)
"""
function fibonacci_search(arr::Vector{T}, target::T) where T
    n = length(arr)
    fib2 = 0  # (m-2)'th Fibonacci number
    fib1 = 1  # (m-1)'th Fibonacci number
    fib = fib2 + fib1  # m'th Fibonacci number

    # Find smallest Fibonacci number >= n
    while fib < n
        fib2 = fib1
        fib1 = fib
        fib = fib2 + fib1
    end

    offset = 0

    while fib > 1
        # Check if fib2 is valid index
        i = min(offset + fib2, n)

        if i > 0 && arr[i] < target
            fib = fib1
            fib1 = fib2
            fib2 = fib - fib1
            offset = i
        elseif i > 0 && arr[i] > target
            fib = fib2
            fib1 = fib1 - fib2
            fib2 = fib - fib1
        else
            return i > 0 ? i : nothing
        end
    end

    # Check last element
    if fib1 == 1 && offset + 1 <= n && arr[offset + 1] == target
        return offset + 1
    end

    return nothing
end

"""
    find_first(arr::Vector{T}, target::T) where T

Find the first occurrence of target in sorted array.

# Time Complexity
- O(log n)
"""
function find_first(arr::Vector{T}, target::T) where T
    left, right = 1, length(arr)
    result = nothing

    while left <= right
        mid = left + (right - left) ÷ 2

        if arr[mid] == target
            result = mid
            right = mid - 1  # Continue searching left
        elseif arr[mid] < target
            left = mid + 1
        else
            right = mid - 1
        end
    end

    return result
end

"""
    find_last(arr::Vector{T}, target::T) where T

Find the last occurrence of target in sorted array.

# Time Complexity
- O(log n)
"""
function find_last(arr::Vector{T}, target::T) where T
    left, right = 1, length(arr)
    result = nothing

    while left <= right
        mid = left + (right - left) ÷ 2

        if arr[mid] == target
            result = mid
            left = mid + 1  # Continue searching right
        elseif arr[mid] < target
            left = mid + 1
        else
            right = mid - 1
        end
    end

    return result
end

"""
    count_occurrences(arr::Vector{T}, target::T) where T

Count the number of occurrences of target in sorted array.

# Time Complexity
- O(log n)
"""
function count_occurrences(arr::Vector{T}, target::T) where T
    first = find_first(arr, target)
    if first === nothing
        return 0
    end

    last = find_last(arr, target)
    return last - first + 1
end

"""
    search_rotated(arr::Vector{T}, target::T) where T

Search for target in a rotated sorted array.

# Time Complexity
- O(log n)
"""
function search_rotated(arr::Vector{T}, target::T) where T
    left, right = 1, length(arr)

    while left <= right
        mid = left + (right - left) ÷ 2

        if arr[mid] == target
            return mid
        end

        # Check which half is sorted
        if arr[left] <= arr[mid]
            # Left half is sorted
            if arr[left] <= target < arr[mid]
                right = mid - 1
            else
                left = mid + 1
            end
        else
            # Right half is sorted
            if arr[mid] < target <= arr[right]
                left = mid + 1
            else
                right = mid - 1
            end
        end
    end

    return nothing
end

"""
    find_peak(arr::Vector{T}) where T

Find a peak element in the array (element greater than neighbors).

# Time Complexity
- O(log n)
"""
function find_peak(arr::Vector{T}) where T
    if isempty(arr)
        return nothing
    end

    if length(arr) == 1
        return 1
    end

    left, right = 1, length(arr)

    while left < right
        mid = left + (right - left) ÷ 2

        if arr[mid] > arr[mid + 1]
            right = mid
        else
            left = mid + 1
        end
    end

    return left
end

"""
    find_min_rotated(arr::Vector{T}) where T

Find the minimum element in a rotated sorted array.

# Time Complexity
- O(log n)
"""
function find_min_rotated(arr::Vector{T}) where T
    if isempty(arr)
        return nothing
    end

    left, right = 1, length(arr)

    # Array is not rotated
    if arr[left] < arr[right]
        return 1
    end

    while left < right
        mid = left + (right - left) ÷ 2

        if arr[mid] > arr[right]
            left = mid + 1
        else
            right = mid
        end
    end

    return left
end

"""
    search_matrix(matrix::Matrix{T}, target::T) where T

Search for target in a row-wise and column-wise sorted matrix.

# Time Complexity
- O(m + n) where m and n are dimensions
"""
function search_matrix(matrix::Matrix{T}, target::T) where T
    if isempty(matrix)
        return nothing
    end

    rows, cols = size(matrix)
    row, col = 1, cols

    while row <= rows && col >= 1
        if matrix[row, col] == target
            return (row, col)
        elseif matrix[row, col] > target
            col -= 1
        else
            row += 1
        end
    end

    return nothing
end

"""
    kth_smallest_matrix(matrix::Matrix{T}, k::Int) where T <: Number

Find the k-th smallest element in a sorted matrix.

# Time Complexity
- O((m+n) log(max-min))
"""
function kth_smallest_matrix(matrix::Matrix{T}, k::Int) where T <: Number
    if isempty(matrix) || k <= 0
        return nothing
    end

    rows, cols = size(matrix)
    left = matrix[1, 1]
    right = matrix[rows, cols]

    while left < right
        mid = left + (right - left) ÷ 2
        count = count_less_equal(matrix, mid)

        if count < k
            left = mid + 1
        else
            right = mid
        end
    end

    return left
end

function count_less_equal(matrix::Matrix{T}, target::T) where T <: Number
    count = 0
    rows, cols = size(matrix)
    row = rows
    col = 1

    while row >= 1 && col <= cols
        if matrix[row, col] <= target
            count += row
            col += 1
        else
            row -= 1
        end
    end

    return count
end

"""
    median_of_sorted_arrays(nums1::Vector{T}, nums2::Vector{T}) where T <: Number

Find the median of two sorted arrays.

# Time Complexity
- O(log(min(m, n)))
"""
function median_of_sorted_arrays(nums1::Vector{T}, nums2::Vector{T}) where T <: Number
    # Ensure nums1 is the smaller array
    if length(nums1) > length(nums2)
        nums1, nums2 = nums2, nums1
    end

    m, n = length(nums1), length(nums2)
    left, right = 0, m

    while left <= right
        partition1 = (left + right) ÷ 2
        partition2 = (m + n + 1) ÷ 2 - partition1

        max_left1 = partition1 == 0 ? -Inf : nums1[partition1]
        min_right1 = partition1 == m ? Inf : nums1[partition1 + 1]

        max_left2 = partition2 == 0 ? -Inf : nums2[partition2]
        min_right2 = partition2 == n ? Inf : nums2[partition2 + 1]

        if max_left1 <= min_right2 && max_left2 <= min_right1
            # Found the correct partition
            if (m + n) % 2 == 1
                return max(max_left1, max_left2)
            else
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2
            end
        elseif max_left1 > min_right2
            right = partition1 - 1
        else
            left = partition1 + 1
        end
    end

    error("Arrays are not sorted")
end

"""
    search_insert_position(arr::Vector{T}, target::T) where T

Find the index where target should be inserted to maintain sorted order.

# Time Complexity
- O(log n)
"""
function search_insert_position(arr::Vector{T}, target::T) where T
    left, right = 1, length(arr)

    while left <= right
        mid = left + (right - left) ÷ 2

        if arr[mid] == target
            return mid
        elseif arr[mid] < target
            left = mid + 1
        else
            right = mid - 1
        end
    end

    return left
end

end # module Searching