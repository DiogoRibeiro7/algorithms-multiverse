import pytest

from bubblesort import (
    bubble_sort_iterative,
    bubble_sort_optimized,
    bubble_sort_in_place,
    bubble_sort_recursive,
    bubble_sort_functional,
    cocktail_sort
)

from heapsort import (
    heap_sort,
    heap_sort_in_place
)

from insertionsort import (
    insertion_sort,
    insertion_sort_in_place,
    insertion_sort_recursive,
    binary_insertion_sort,
    shell_sort,
    hybrid_insertion_sort
)

from mergesort import (
    merge_sort_recursive,
    merge_sort_in_place,
    merge_sort_iterative
)

from selectionsort import (
    selection_sort,
    selection_sort_in_place,
    bidirectional_selection_sort,
    selection_sort_recursive,
    stable_selection_sort
)

ALGORITHMS = [
    bubble_sort_iterative,
    bubble_sort_optimized,
    bubble_sort_in_place,
    bubble_sort_recursive,
    bubble_sort_functional,
    cocktail_sort,
    heap_sort,
    heap_sort_in_place,
    insertion_sort,
    insertion_sort_in_place,
    insertion_sort_recursive,
    binary_insertion_sort,
    shell_sort,
    hybrid_insertion_sort,
    merge_sort_recursive,
    merge_sort_in_place,
    merge_sort_iterative,
    selection_sort,
    selection_sort_in_place,
    bidirectional_selection_sort,
    selection_sort_recursive,
    stable_selection_sort
]

TEST_CASES = [
    [],
    [42],
    [1, 2, 3, 4, 5, 6],
    [9, 8, 7, 6, 5, 4],
    [3, 1, 4, 1, 5, 9, 2, 6, 5],
    [-5, 0, 5, -10, 20]
]

@pytest.mark.parametrize("algorithm", ALGORITHMS)
@pytest.mark.parametrize("test_case", TEST_CASES)

def test_sorting_algorithm(algorithm, test_case):
    # Copy the input test case
    arr = test_case.copy()
    # Run the algorithm
    result = algorithm(arr)

    # Some algorithms sort in-place and return None
    # otherwise they return the new sorted list.
    sorted_result = result if result is not None else arr
    
    # Validate against Python's built-in sorted function
    assert sorted_result == sorted(test_case)
