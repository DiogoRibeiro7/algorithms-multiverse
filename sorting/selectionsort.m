% Selection Sort Algorithm - Educational Implementation (MATLAB)
%
% ALGORITHM OVERVIEW:
% ==================
% Selection Sort works by repeatedly finding the minimum element from the unsorted
% portion of the array and placing it at the beginning. It divides the array into
% two parts: a sorted portion (left) and an unsorted portion (right).
%
% Time Complexity:
% - Best Case: O(n²) - Even if array is already sorted, still searches for minimum
% - Average Case: O(n²)
% - Worst Case: O(n²)
% - IMPORTANT: Unlike bubble sort and insertion sort, selection sort ALWAYS performs
%   O(n²) comparisons, regardless of input
%
% Space Complexity: O(1) for in-place, O(n) for functional approach
%
% Stability: NOT stable by default (can be made stable with modifications)
% In-place: YES (when modifying passed array)
%
% KEY ADVANTAGE: Makes MINIMUM number of swaps - only O(n) swaps!
% This is critical when writing to memory is expensive (flash, EEPROM, etc.)

%% ========================================================================
% STANDARD SELECTION SORT
% ========================================================================

function sorted_arr = selection_sort(arr)
    % SELECTION_SORT Standard selection sort implementation.
    %
    % ALGORITHM STEPS:
    % ===============
    % 1. Find the minimum element in the unsorted portion
    % 2. Swap it with the first element of the unsorted portion
    % 3. Move the boundary of sorted/unsorted portions one element to the right
    % 4. Repeat until the entire array is sorted
    %
    % Visual Example:
    % ==============
    % Initial: [64, 25, 12, 22, 11]
    %
    % Pass 1: Find min in [64, 25, 12, 22, 11] → 11
    %         Swap 64 ↔ 11
    %         Result: [11, 25, 12, 22, 64]
    %                  ^^^ sorted portion
    %
    % Pass 2: Find min in [25, 12, 22, 64] → 12
    %         Swap 25 ↔ 12
    %         Result: [11, 12, 25, 22, 64]
    %                  ^^^^^^^ sorted portion
    %
    % Time: O(n²), Space: O(n) for new array
    %
    % Args:
    %   arr - Array to sort
    %
    % Returns:
    %   sorted_arr - A new sorted array

    if isempty(arr) || length(arr) <= 1
        sorted_arr = arr;
        return;
    end

    sorted_arr = arr;
    n = length(sorted_arr);

    % Outer loop: Move boundary of unsorted subarray one by one
    for i = 1:n-1
        % Find the minimum element in the remaining unsorted array
        % Start by assuming the first unsorted element is the minimum
        min_idx = i;

        % Inner loop: Search for the minimum in arr(i+1:n)
        for j = i+1:n
            % If we find a smaller element, update min_idx
            if sorted_arr(j) < sorted_arr(min_idx)
                min_idx = j;
            end
        end

        % Swap the found minimum element with the first element
        % of the unsorted portion (only if different)
        if min_idx ~= i
            temp = sorted_arr(i);
            sorted_arr(i) = sorted_arr(min_idx);
            sorted_arr(min_idx) = temp;
        end
    end
end

%% ========================================================================
% BIDIRECTIONAL SELECTION SORT
% ========================================================================

function sorted_arr = bidirectional_selection_sort(arr)
    % BIDIRECTIONAL_SELECTION_SORT Bidirectional selection sort.
    %
    % OPTIMIZATION:
    % ============
    % Instead of finding just the minimum in each pass, we find BOTH the minimum
    % and maximum elements. We place the minimum at the beginning and the maximum
    % at the end, reducing the number of passes by approximately half.
    %
    % Time: Still O(n²), but approximately 2x faster in practice
    %
    % Args:
    %   arr - Array to sort
    %
    % Returns:
    %   sorted_arr - A new sorted array

    if isempty(arr) || length(arr) <= 1
        sorted_arr = arr;
        return;
    end

    sorted_arr = arr;
    n = length(sorted_arr);

    % Process from both ends toward the middle
    left = 1;
    right = n;

    while left < right
        % Find both minimum and maximum in the current range
        min_idx = left;
        max_idx = left;

        for i = left:right
            if sorted_arr(i) < sorted_arr(min_idx)
                min_idx = i;
            end
            if sorted_arr(i) > sorted_arr(max_idx)
                max_idx = i;
            end
        end

        % Handle special case: if min is at right position
        if min_idx == right
            temp = sorted_arr(left);
            sorted_arr(left) = sorted_arr(right);
            sorted_arr(right) = temp;
            if max_idx == left
                max_idx = right;
            end
        else
            % Swap minimum to the left boundary
            if min_idx ~= left
                temp = sorted_arr(left);
                sorted_arr(left) = sorted_arr(min_idx);
                sorted_arr(min_idx) = temp;
            end

            % If maximum was at left position, it's now at min_idx
            if max_idx == left
                max_idx = min_idx;
            end

            % Swap maximum to the right boundary
            if max_idx ~= right
                temp = sorted_arr(right);
                sorted_arr(right) = sorted_arr(max_idx);
                sorted_arr(max_idx) = temp;
            end
        end

        % Move boundaries inward
        left = left + 1;
        right = right - 1;
    end
end

%% ========================================================================
% RECURSIVE SELECTION SORT
% ========================================================================

function sorted_arr = selection_sort_recursive(arr, start_idx)
    % SELECTION_SORT_RECURSIVE Recursive selection sort.
    %
    % RECURSIVE APPROACH:
    % ==================
    % Base case: Array of size 0 or 1 is already sorted
    % Recursive case:
    %     1. Find the minimum element in the array
    %     2. Swap it with the first element
    %     3. Recursively sort the rest of the array (excluding the first element)
    %
    % Time: O(n²), Space: O(n) for recursion stack
    %
    % Args:
    %   arr - Array to sort
    %   start_idx - Starting index (default 1)
    %
    % Returns:
    %   sorted_arr - A new sorted array

    if nargin < 2
        start_idx = 1;
    end

    if isempty(arr)
        sorted_arr = arr;
        return;
    end

    n = length(arr);

    % Base case: if we've reached the end, we're done
    if start_idx >= n
        sorted_arr = arr;
        return;
    end

    % Find the minimum element in arr(start_idx:n)
    min_idx = start_idx;
    for i = start_idx+1:n
        if arr(i) < arr(min_idx)
            min_idx = i;
        end
    end

    % Swap the minimum with the element at start_idx
    if min_idx ~= start_idx
        temp = arr(start_idx);
        arr(start_idx) = arr(min_idx);
        arr(min_idx) = temp;
    end

    % Recursively sort the rest
    sorted_arr = selection_sort_recursive(arr, start_idx + 1);
end

%% ========================================================================
% STABLE SELECTION SORT
% ========================================================================

function sorted_arr = stable_selection_sort(arr)
    % STABLE_SELECTION_SORT Stable version of selection sort.
    %
    % WHY STANDARD SELECTION SORT IS UNSTABLE:
    % ========================================
    % When we swap the minimum element with the first element of the unsorted
    % portion, we can change the relative order of equal elements.
    %
    % MAKING IT STABLE:
    % ================
    % Instead of swapping, we shift all elements and insert the minimum
    % at the correct position. This preserves the relative order.
    %
    % Time: O(n²) comparisons + O(n²) shifts
    %
    % Args:
    %   arr - Array to sort
    %
    % Returns:
    %   sorted_arr - A new sorted array

    if isempty(arr) || length(arr) <= 1
        sorted_arr = arr;
        return;
    end

    sorted_arr = arr;
    n = length(sorted_arr);

    for i = 1:n-1
        % Find minimum in unsorted portion
        min_idx = i;
        for j = i+1:n
            if sorted_arr(j) < sorted_arr(min_idx)
                min_idx = j;
            end
        end

        % Instead of swapping, shift elements and insert
        if min_idx ~= i
            min_value = sorted_arr(min_idx);
            % Shift all elements between i and min_idx one position right
            for k = min_idx:-1:i+1
                sorted_arr(k) = sorted_arr(k-1);
            end
            % Place minimum at position i
            sorted_arr(i) = min_value;
        end
    end
end

%% ========================================================================
% VISUALIZATION AND UTILITIES
% ========================================================================

function steps = visualize_selection_sort(arr)
    % VISUALIZE_SELECTION_SORT Create ASCII visualization of selection sort.
    %
    % Args:
    %   arr - Array to visualize
    %
    % Returns:
    %   steps - Cell array of strings showing each step

    steps = {};
    result = arr;
    n = length(result);

    steps{end+1} = repmat('=', 1, 70);
    steps{end+1} = 'SELECTION SORT VISUALIZATION';
    steps{end+1} = repmat('=', 1, 70);
    steps{end+1} = sprintf('Initial array: %s', mat2str(result));
    steps{end+1} = '';

    for i = 1:n-1
        steps{end+1} = sprintf('Pass %d:', i);
        unsorted = result(i:n);
        steps{end+1} = sprintf('  Looking for minimum in unsorted portion: %s', mat2str(unsorted));

        min_idx = i;
        min_value = result(i);

        % Show the search process
        for j = i+1:n
            if result(j) < min_value
                min_idx = j;
                min_value = result(j);
                steps{end+1} = sprintf('    Found new minimum: %d at index %d', min_value, min_idx);
            end
        end

        % Show the swap
        if min_idx ~= i
            steps{end+1} = sprintf('  Swapping %d ↔ %d', result(i), result(min_idx));
            temp = result(i);
            result(i) = result(min_idx);
            result(min_idx) = temp;
        else
            steps{end+1} = '  No swap needed (minimum already in place)';
        end

        % Show current state
        sorted_part = result(1:i);
        unsorted_part = result(i+1:n);
        steps{end+1} = sprintf('  Sorted: %s | Unsorted: %s', mat2str(sorted_part), mat2str(unsorted_part));
        steps{end+1} = '';
    end

    steps{end+1} = sprintf('Final sorted array: %s', mat2str(result));
    steps{end+1} = repmat('=', 1, 70);
end

function result = is_sorted(arr)
    % IS_SORTED Check if an array is sorted in ascending order.
    %
    % Args:
    %   arr - Array to check
    %
    % Returns:
    %   result - true if sorted, false otherwise

    if isempty(arr) || length(arr) <= 1
        result = true;
        return;
    end

    result = all(diff(arr) >= 0);
end

%% ========================================================================
% DEMONSTRATION AND TESTING
% ========================================================================

function demonstrate_selection_sort()
    % DEMONSTRATE_SELECTION_SORT Comprehensive demonstration of selection sort.

    fprintf('📚 SELECTION SORT - EDUCATIONAL DEMONSTRATION\n');
    fprintf('%s\n\n', repmat('=', 1, 80));

    % Test cases
    test_cases = {
        struct('arr', [64, 25, 12, 22, 11], 'desc', 'Random array'), ...
        struct('arr', [5, 2, 8, 6, 1, 9, 4], 'desc', 'Small random array'), ...
        struct('arr', 1, 'desc', 'Single element'), ...
        struct('arr', [], 'desc', 'Empty array'), ...
        struct('arr', [3, 3, 3, 3, 3], 'desc', 'All duplicates'), ...
        struct('arr', [9, 8, 7, 6, 5, 4, 3, 2, 1], 'desc', 'Reverse sorted'), ...
        struct('arr', [1, 2, 3, 4, 5], 'desc', 'Already sorted'), ...
        struct('arr', [1, 3, 2, 4, 5], 'desc', 'Nearly sorted')
    };

    fprintf('📋 BASIC FUNCTIONALITY TESTS:\n');
    fprintf('%s\n\n', repmat('-', 1, 80));

    for i = 1:length(test_cases)
        tc = test_cases{i};
        original = tc.arr;
        standard = selection_sort(tc.arr);
        bidirectional = bidirectional_selection_sort(tc.arr);
        recursive = selection_sort_recursive(tc.arr);
        stable = stable_selection_sort(tc.arr);

        fprintf('\nTest: %s\n', tc.desc);
        fprintf('Original:      %s\n', mat2str(original));
        fprintf('Standard:      %s\n', mat2str(standard));
        fprintf('Bidirectional: %s\n', mat2str(bidirectional));
        fprintf('Recursive:     %s\n', mat2str(recursive));
        fprintf('Stable:        %s\n', mat2str(stable));

        all_correct = is_sorted(standard) && is_sorted(bidirectional) && ...
                     is_sorted(recursive) && is_sorted(stable);
        if all_correct
            status = '✓';
        else
            status = '✗';
        end
        fprintf('All correct: %s\n', status);
    end

    % Visualization
    fprintf('\n\n🎬 STEP-BY-STEP VISUALIZATION:\n');
    fprintf('%s\n\n', repmat('-', 1, 80));

    demo_arr = [64, 25, 12, 22, 11];
    steps = visualize_selection_sort(demo_arr);
    for i = 1:length(steps)
        fprintf('%s\n', steps{i});
    end

    % Memory analysis
    fprintf('\n\n💾 MEMORY USAGE ANALYSIS:\n');
    fprintf('%s\n', repmat('-', 1, 80));
    fprintf(['\n' ...
        'Selection Sort Memory Characteristics:\n' ...
        '\n' ...
        '1. In-Place Sorting:\n' ...
        '   - Space Complexity: O(1) auxiliary space\n' ...
        '   - Only uses constant extra memory (min_idx, temp, loop variables)\n' ...
        '   - MATLAB arrays are passed by value (creates copies)\n' ...
        '\n' ...
        '2. Memory Writes:\n' ...
        '   - Selection Sort: O(n) swaps (minimum writes)\n' ...
        '   - Bubble Sort: O(n²) swaps in worst case\n' ...
        '   - Insertion Sort: O(n²) shifts in worst case\n' ...
        '\n' ...
        '   ⭐ This makes Selection Sort ideal when writing to memory is expensive!\n' ...
        '      Examples: Flash memory, EEPROM, or distributed systems\n' ...
        '\n' ...
        '3. MATLAB-Specific:\n' ...
        '   - Arrays are column-major (affects cache performance)\n' ...
        '   - JIT compilation improves loop performance\n' ...
        '   - Vectorized operations preferred when possible\n' ...
        '\n']);

    fprintf('📌 WHEN TO USE SELECTION SORT:\n');
    fprintf('%s\n', repmat('-', 1, 80));
    fprintf(['\n' ...
        '✅ GOOD USE CASES:\n' ...
        '\n' ...
        '1. Minimal Memory Writes:\n' ...
        '   - Flash memory or EEPROM (limited write cycles)\n' ...
        '   - Distributed systems where network writes are expensive\n' ...
        '\n' ...
        '2. Small Datasets:\n' ...
        '   - When simplicity matters more than efficiency\n' ...
        '   - Scientific computing with small matrices/vectors\n' ...
        '\n' ...
        '3. Known Small Data:\n' ...
        '   - MATLAB applications with small arrays\n' ...
        '   - When n is guaranteed to be small (< 20 elements)\n' ...
        '\n' ...
        '❌ POOR USE CASES:\n' ...
        '\n' ...
        '1. Large Datasets:\n' ...
        '   - Always O(n²) time, never adapts to input\n' ...
        '   - Much slower than O(n log n) algorithms\n' ...
        '   - Use MATLAB''s built-in sort() function for large data\n' ...
        '\n' ...
        '2. Nearly Sorted Data:\n' ...
        '   - Unlike insertion sort, doesn''t benefit from sorted input\n' ...
        '   - Still performs all O(n²) comparisons\n' ...
        '\n' ...
        '3. Real-time Systems:\n' ...
        '   - Non-adaptive nature means worst-case is always hit\n' ...
        '   - Insertion sort or merge sort preferred\n' ...
        '\n']);
end

%% ========================================================================
% PERFORMANCE BENCHMARK
% ========================================================================

function performance_benchmark()
    % PERFORMANCE_BENCHMARK Benchmark selection sort performance.

    fprintf('\n\n⚡ PERFORMANCE BENCHMARK\n');
    fprintf('%s\n\n', repmat('=', 1, 80));

    sizes = [10, 20, 50, 100, 200];

    fprintf('Random Data:\n');
    fprintf('%-10s%15s%15s%15s%15s\n', 'Size', 'Standard', 'Bidirectional', 'Recursive', 'MATLAB sort');
    fprintf('%s\n', repmat('-', 1, 70));

    for i = 1:length(sizes)
        size_val = sizes(i);
        test_data = randi([1, 1000], 1, size_val);

        % Standard
        tic;
        selection_sort(test_data);
        time_standard = toc * 1000;

        % Bidirectional
        tic;
        bidirectional_selection_sort(test_data);
        time_bidirectional = toc * 1000;

        % Recursive
        tic;
        selection_sort_recursive(test_data);
        time_recursive = toc * 1000;

        % MATLAB built-in sort
        tic;
        sort(test_data);
        time_builtin = toc * 1000;

        fprintf('%-10d%14.3fms%14.3fms%14.3fms%14.3fms\n', ...
                size_val, time_standard, time_bidirectional, time_recursive, time_builtin);
    end
end

%% ========================================================================
% MAIN EXECUTION
% ========================================================================

% Run demonstration if this file is executed directly
if ~isdeployed
    demonstrate_selection_sort();
    performance_benchmark();
    fprintf('\n✨ Selection Sort demonstration complete!\n');
end
