"""
    Sorting

Module containing various sorting algorithms implemented in Julia.
"""
module Sorting

export quicksort, quicksort!, mergesort, mergesort!,
       heapsort!, insertionsort!, selectionsort!, bubblesort!,
       shellsort!, countingsort, radixsort, bucketsort,
       timsort!, introsort!, quickselect

"""
    quicksort(arr::Vector{T}) where T

Return a sorted copy of the array using quicksort algorithm.

# Time Complexity
- Best/Average: O(n log n)
- Worst: O(n²)
- Space: O(log n)
"""
function quicksort(arr::Vector{T}) where T
    result = copy(arr)
    quicksort!(result)
    return result
end

"""
    quicksort!(arr::Vector{T}, lo::Int=1, hi::Int=length(arr)) where T

Sort array in-place using quicksort algorithm.
"""
function quicksort!(arr::Vector{T}, lo::Int=1, hi::Int=length(arr)) where T
    if lo < hi
        p = partition!(arr, lo, hi)
        quicksort!(arr, lo, p - 1)
        quicksort!(arr, p + 1, hi)
    end
    return arr
end

function partition!(arr::Vector{T}, lo::Int, hi::Int) where T
    pivot = arr[hi]
    i = lo - 1

    for j in lo:hi-1
        if arr[j] <= pivot
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
        end
    end

    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1
end

"""
    mergesort(arr::Vector{T}) where T

Return a sorted copy of the array using mergesort algorithm.

# Time Complexity
- All cases: O(n log n)
- Space: O(n)
"""
function mergesort(arr::Vector{T}) where T
    if length(arr) <= 1
        return copy(arr)
    end

    mid = length(arr) ÷ 2
    left = mergesort(arr[1:mid])
    right = mergesort(arr[mid+1:end])

    return merge(left, right)
end

"""
    mergesort!(arr::Vector{T}) where T

Sort array in-place using mergesort algorithm (with auxiliary space).
"""
function mergesort!(arr::Vector{T}) where T
    n = length(arr)
    aux = similar(arr)
    mergesort_helper!(arr, aux, 1, n)
    return arr
end

function mergesort_helper!(arr::Vector{T}, aux::Vector{T}, lo::Int, hi::Int) where T
    if lo >= hi
        return
    end

    mid = lo + (hi - lo) ÷ 2
    mergesort_helper!(arr, aux, lo, mid)
    mergesort_helper!(arr, aux, mid + 1, hi)
    merge!(arr, aux, lo, mid, hi)
end

function merge!(arr::Vector{T}, aux::Vector{T}, lo::Int, mid::Int, hi::Int) where T
    # Copy to auxiliary array
    for k in lo:hi
        aux[k] = arr[k]
    end

    i = lo
    j = mid + 1

    for k in lo:hi
        if i > mid
            arr[k] = aux[j]
            j += 1
        elseif j > hi
            arr[k] = aux[i]
            i += 1
        elseif aux[j] < aux[i]
            arr[k] = aux[j]
            j += 1
        else
            arr[k] = aux[i]
            i += 1
        end
    end
end

function merge(left::Vector{T}, right::Vector{T}) where T
    result = T[]
    i = j = 1

    while i <= length(left) && j <= length(right)
        if left[i] <= right[j]
            push!(result, left[i])
            i += 1
        else
            push!(result, right[j])
            j += 1
        end
    end

    append!(result, left[i:end])
    append!(result, right[j:end])

    return result
end

"""
    heapsort!(arr::Vector{T}) where T

Sort array in-place using heapsort algorithm.

# Time Complexity
- All cases: O(n log n)
- Space: O(1)
"""
function heapsort!(arr::Vector{T}) where T
    n = length(arr)

    # Build max heap
    for i in n÷2:-1:1
        heapify!(arr, n, i)
    end

    # Extract elements from heap
    for i in n:-1:2
        arr[1], arr[i] = arr[i], arr[1]
        heapify!(arr, i - 1, 1)
    end

    return arr
end

function heapify!(arr::Vector{T}, n::Int, i::Int) where T
    largest = i
    left = 2 * i
    right = 2 * i + 1

    if left <= n && arr[left] > arr[largest]
        largest = left
    end

    if right <= n && arr[right] > arr[largest]
        largest = right
    end

    if largest != i
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify!(arr, n, largest)
    end
end

"""
    insertionsort!(arr::Vector{T}, lo::Int=1, hi::Int=length(arr)) where T

Sort array in-place using insertion sort algorithm.

# Time Complexity
- Best: O(n)
- Average/Worst: O(n²)
- Space: O(1)
"""
function insertionsort!(arr::Vector{T}, lo::Int=1, hi::Int=length(arr)) where T
    for i in lo+1:hi
        key = arr[i]
        j = i - 1

        while j >= lo && arr[j] > key
            arr[j + 1] = arr[j]
            j -= 1
        end

        arr[j + 1] = key
    end

    return arr
end

"""
    selectionsort!(arr::Vector{T}) where T

Sort array in-place using selection sort algorithm.

# Time Complexity
- All cases: O(n²)
- Space: O(1)
"""
function selectionsort!(arr::Vector{T}) where T
    n = length(arr)

    for i in 1:n-1
        min_idx = i

        for j in i+1:n
            if arr[j] < arr[min_idx]
                min_idx = j
            end
        end

        if min_idx != i
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        end
    end

    return arr
end

"""
    bubblesort!(arr::Vector{T}) where T

Sort array in-place using bubble sort algorithm.

# Time Complexity
- Best: O(n)
- Average/Worst: O(n²)
- Space: O(1)
"""
function bubblesort!(arr::Vector{T}) where T
    n = length(arr)

    for i in 1:n-1
        swapped = false

        for j in 1:n-i
            if arr[j] > arr[j + 1]
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = true
            end
        end

        if !swapped
            break
        end
    end

    return arr
end

"""
    shellsort!(arr::Vector{T}) where T

Sort array in-place using shell sort algorithm.

# Time Complexity
- Best: O(n log n)
- Average: O(n^1.5)
- Worst: O(n²)
- Space: O(1)
"""
function shellsort!(arr::Vector{T}) where T
    n = length(arr)
    gap = n ÷ 2

    while gap > 0
        for i in gap+1:n
            temp = arr[i]
            j = i

            while j > gap && arr[j - gap] > temp
                arr[j] = arr[j - gap]
                j -= gap
            end

            arr[j] = temp
        end

        gap ÷= 2
    end

    return arr
end

"""
    countingsort(arr::Vector{Int}, max_val::Int=maximum(arr))

Sort array of non-negative integers using counting sort.

# Time Complexity
- O(n + k) where k is the range
- Space: O(k)
"""
function countingsort(arr::Vector{Int}, max_val::Int=maximum(arr))
    if isempty(arr)
        return Int[]
    end

    min_val = minimum(arr)
    range_size = max_val - min_val + 1
    count = zeros(Int, range_size)
    output = similar(arr)

    # Count occurrences
    for num in arr
        count[num - min_val + 1] += 1
    end

    # Cumulative count
    for i in 2:range_size
        count[i] += count[i - 1]
    end

    # Build output array
    for i in length(arr):-1:1
        idx = arr[i] - min_val + 1
        output[count[idx]] = arr[i]
        count[idx] -= 1
    end

    return output
end

"""
    radixsort(arr::Vector{Int})

Sort array of non-negative integers using radix sort.

# Time Complexity
- O(nk) where k is the number of digits
- Space: O(n)
"""
function radixsort(arr::Vector{Int})
    if isempty(arr)
        return Int[]
    end

    result = copy(arr)
    max_num = maximum(arr)
    exp = 1

    while max_num ÷ exp > 0
        counting_sort_by_digit!(result, exp)
        exp *= 10
    end

    return result
end

function counting_sort_by_digit!(arr::Vector{Int}, exp::Int)
    n = length(arr)
    output = similar(arr)
    count = zeros(Int, 10)

    # Count occurrences of each digit
    for num in arr
        digit = (num ÷ exp) % 10
        count[digit + 1] += 1
    end

    # Cumulative count
    for i in 2:10
        count[i] += count[i - 1]
    end

    # Build output array
    for i in n:-1:1
        digit = (arr[i] ÷ exp) % 10
        output[count[digit + 1]] = arr[i]
        count[digit + 1] -= 1
    end

    # Copy back
    copyto!(arr, output)
end

"""
    bucketsort(arr::Vector{Float64}, n_buckets::Int=10)

Sort array of floats in range [0, 1) using bucket sort.

# Time Complexity
- Average: O(n + k)
- Worst: O(n²)
- Space: O(n)
"""
function bucketsort(arr::Vector{Float64}, n_buckets::Int=10)
    if isempty(arr)
        return Float64[]
    end

    # Initialize buckets
    buckets = [Float64[] for _ in 1:n_buckets]

    # Distribute elements into buckets
    for num in arr
        # Scale number to bucket range
        idx = min(Int(floor(num * n_buckets)) + 1, n_buckets)
        push!(buckets[idx], num)
    end

    # Sort individual buckets and concatenate
    result = Float64[]
    for bucket in buckets
        if !isempty(bucket)
            sort!(bucket)
            append!(result, bucket)
        end
    end

    return result
end

"""
    timsort!(arr::Vector{T}) where T

Sort array using TimSort algorithm (hybrid stable sort).

# Time Complexity
- Best: O(n)
- Average/Worst: O(n log n)
- Space: O(n)
"""
function timsort!(arr::Vector{T}) where T
    MIN_MERGE = 32
    n = length(arr)

    # Sort individual runs using insertion sort
    for start in 1:MIN_MERGE:n
        finish = min(start + MIN_MERGE - 1, n)
        insertionsort!(arr, start, finish)
    end

    # Start merging from MIN_MERGE
    size = MIN_MERGE
    while size < n
        for start in 1:2*size:n
            mid = start + size - 1
            finish = min(start + 2*size - 1, n)

            if mid < finish
                # Create auxiliary array for merge
                aux = similar(arr, finish - start + 1)
                merge_tim!(arr, aux, start, mid, finish)
            end
        end
        size *= 2
    end

    return arr
end

function merge_tim!(arr::Vector{T}, aux::Vector{T}, lo::Int, mid::Int, hi::Int) where T
    # Copy to auxiliary array
    k = 1
    for idx in lo:hi
        aux[k] = arr[idx]
        k += 1
    end

    i = 1
    j = mid - lo + 2

    for idx in lo:hi
        if i > mid - lo + 1
            arr[idx] = aux[j]
            j += 1
        elseif j > hi - lo + 1
            arr[idx] = aux[i]
            i += 1
        elseif aux[j] < aux[i]
            arr[idx] = aux[j]
            j += 1
        else
            arr[idx] = aux[i]
            i += 1
        end
    end
end

"""
    introsort!(arr::Vector{T}) where T

Sort array using IntroSort algorithm (hybrid of quicksort, heapsort, and insertion sort).

# Time Complexity
- All cases: O(n log n)
- Space: O(log n)
"""
function introsort!(arr::Vector{T}) where T
    max_depth = 2 * Int(floor(log2(length(arr))))
    introsort_helper!(arr, 1, length(arr), max_depth)
    return arr
end

function introsort_helper!(arr::Vector{T}, lo::Int, hi::Int, max_depth::Int) where T
    if hi - lo < 16
        insertionsort!(arr, lo, hi)
    elseif max_depth == 0
        heapsort_range!(arr, lo, hi)
    else
        p = partition!(arr, lo, hi)
        introsort_helper!(arr, lo, p - 1, max_depth - 1)
        introsort_helper!(arr, p + 1, hi, max_depth - 1)
    end
end

function heapsort_range!(arr::Vector{T}, lo::Int, hi::Int) where T
    # Build max heap for the range
    n = hi - lo + 1
    offset = lo - 1

    for i in n÷2:-1:1
        heapify_range!(arr, n, i, offset)
    end

    # Extract elements
    for i in n:-1:2
        arr[offset + 1], arr[offset + i] = arr[offset + i], arr[offset + 1]
        heapify_range!(arr, i - 1, 1, offset)
    end
end

function heapify_range!(arr::Vector{T}, n::Int, i::Int, offset::Int) where T
    largest = i
    left = 2 * i
    right = 2 * i + 1

    if left <= n && arr[offset + left] > arr[offset + largest]
        largest = left
    end

    if right <= n && arr[offset + right] > arr[offset + largest]
        largest = right
    end

    if largest != i
        arr[offset + i], arr[offset + largest] = arr[offset + largest], arr[offset + i]
        heapify_range!(arr, n, largest, offset)
    end
end

"""
    quickselect(arr::Vector{T}, k::Int) where T

Find the k-th smallest element in the array (1-indexed).

# Time Complexity
- Average: O(n)
- Worst: O(n²)
- Space: O(1)
"""
function quickselect(arr::Vector{T}, k::Int) where T
    if k < 1 || k > length(arr)
        throw(ArgumentError("k must be between 1 and length(arr)"))
    end

    arr_copy = copy(arr)
    return quickselect!(arr_copy, k, 1, length(arr_copy))
end

function quickselect!(arr::Vector{T}, k::Int, lo::Int, hi::Int) where T
    if lo == hi
        return arr[lo]
    end

    p = partition!(arr, lo, hi)

    if k == p
        return arr[k]
    elseif k < p
        return quickselect!(arr, k, lo, p - 1)
    else
        return quickselect!(arr, k, p + 1, hi)
    end
end

"""
    parallel_quicksort(arr::Vector{T}, threshold::Int=10000) where T

Sort array using parallel quicksort for large arrays.

# Time Complexity
- Average: O(n log n) with parallelism
- Space: O(log n)
"""
function parallel_quicksort(arr::Vector{T}, threshold::Int=10000) where T
    if length(arr) <= threshold
        return quicksort(arr)
    end

    result = copy(arr)
    parallel_quicksort!(result, 1, length(result), threshold)
    return result
end

function parallel_quicksort!(arr::Vector{T}, lo::Int, hi::Int, threshold::Int) where T
    if hi - lo < threshold
        quicksort!(arr, lo, hi)
        return
    end

    p = partition!(arr, lo, hi)

    # Parallel execution of left and right parts
    @sync begin
        Threads.@spawn parallel_quicksort!(arr, lo, p - 1, threshold)
        Threads.@spawn parallel_quicksort!(arr, p + 1, hi, threshold)
    end
end

end # module Sorting