// Selection Sort Algorithm - Educational Implementation (Rust)
//
// ALGORITHM OVERVIEW:
// ==================
// Selection Sort works by repeatedly finding the minimum element from the unsorted
// portion of the array and placing it at the beginning. It divides the array into
// two parts: a sorted portion (left) and an unsorted portion (right).
//
// Time Complexity:
// - Best Case: O(n²) - Even if array is already sorted, still searches for minimum
// - Average Case: O(n²)
// - Worst Case: O(n²)
// - IMPORTANT: Unlike bubble sort and insertion sort, selection sort ALWAYS performs
//   O(n²) comparisons, regardless of input
//
// Space Complexity: O(1) - Sorts in-place with only constant extra space
//
// Stability: NOT stable by default (can be made stable with modifications)
// In-place: YES
//
// KEY ADVANTAGE: Makes MINIMUM number of swaps - only O(n) swaps!

use std::cmp::Ordering;
use std::fmt::Display;
use std::time::Instant;

// ============================================================================
// STANDARD SELECTION SORT
// ============================================================================

/// Standard selection sort implementation.
///
/// ALGORITHM STEPS:
/// ===============
/// 1. Find the minimum element in the unsorted portion
/// 2. Swap it with the first element of the unsorted portion
/// 3. Move the boundary of sorted/unsorted portions one element to the right
/// 4. Repeat until the entire array is sorted
///
/// Visual Example:
/// ==============
/// Initial: [64, 25, 12, 22, 11]
///
/// Pass 1: Find min in [64, 25, 12, 22, 11] → 11
///         Swap 64 ↔ 11
///         Result: [11, 25, 12, 22, 64]
///                  ^^^ sorted portion
///
/// Pass 2: Find min in [25, 12, 22, 64] → 12
///         Swap 25 ↔ 12
///         Result: [11, 12, 25, 22, 64]
///                  ^^^^^^^ sorted portion
///
/// Time: O(n²), Space: O(n) for new vector
pub fn selection_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    selection_sort_in_place(&mut result);
    result
}

/// In-place selection sort implementation.
///
/// DETAILED STEP-BY-STEP:
/// ======================
/// For each position i from 0 to n-1:
///     - Assume arr[i] is the minimum
///     - Scan all elements from i+1 to n-1
///     - Track the index of the actual minimum element
///     - After scanning, swap arr[i] with the minimum element found
///
/// Time: O(n²), Space: O(1)
pub fn selection_sort_in_place<T: Ord>(arr: &mut [T]) {
    let n = arr.len();

    // Outer loop: Move boundary of unsorted subarray one by one
    for i in 0..n.saturating_sub(1) {
        // Find the minimum element in the remaining unsorted array
        // Start by assuming the first unsorted element is the minimum
        let mut min_idx = i;

        // Inner loop: Search for the minimum in arr[i+1...n-1]
        for j in (i + 1)..n {
            // If we find a smaller element, update min_idx
            if arr[j] < arr[min_idx] {
                min_idx = j;
            }
        }

        // Swap the found minimum element with the first element
        // of the unsorted portion
        if min_idx != i {
            arr.swap(i, min_idx);
        }
    }
}

// ============================================================================
// BIDIRECTIONAL SELECTION SORT
// ============================================================================

/// Bidirectional selection sort (also called "double selection sort").
///
/// OPTIMIZATION:
/// ============
/// Instead of finding just the minimum in each pass, we find BOTH the minimum
/// and maximum elements. We place the minimum at the beginning and the maximum
/// at the end, reducing the number of passes by approximately half.
///
/// Time: Still O(n²), but approximately 2x faster in practice
pub fn bidirectional_selection_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    let n = result.len();

    // Process from both ends toward the middle
    let mut left = 0;
    let mut right = n - 1;

    while left < right {
        // Find both minimum and maximum in the current range
        let mut min_idx = left;
        let mut max_idx = left;

        for i in left..=right {
            if result[i] < result[min_idx] {
                min_idx = i;
            }
            if result[i] > result[max_idx] {
                max_idx = i;
            }
        }

        // Handle special case: if min is at right position
        if min_idx == right {
            result.swap(left, right);
            if max_idx == left {
                max_idx = right;
            }
        } else {
            // Swap minimum to the left boundary
            if min_idx != left {
                result.swap(left, min_idx);
            }

            // If maximum was at left position, it's now at min_idx
            if max_idx == left {
                max_idx = min_idx;
            }

            // Swap maximum to the right boundary
            if max_idx != right {
                result.swap(right, max_idx);
            }
        }

        // Move boundaries inward
        left += 1;
        right = right.saturating_sub(1);
    }

    result
}

// ============================================================================
// RECURSIVE SELECTION SORT
// ============================================================================

/// Recursive implementation of selection sort.
///
/// RECURSIVE APPROACH:
/// ==================
/// Base case: Array of size 0 or 1 is already sorted
/// Recursive case:
///     1. Find the minimum element in the array
///     2. Swap it with the first element
///     3. Recursively sort the rest of the array (excluding the first element)
///
/// Time: O(n²), Space: O(n) for recursion stack
pub fn selection_sort_recursive<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    selection_sort_recursive_helper(&mut result, 0);
    result
}

fn selection_sort_recursive_helper<T: Ord>(arr: &mut [T], start_idx: usize) {
    // Base case: if we've reached the end, we're done
    if start_idx >= arr.len().saturating_sub(1) {
        return;
    }

    // Find the minimum element in arr[start_idx...n-1]
    let mut min_idx = start_idx;
    for i in (start_idx + 1)..arr.len() {
        if arr[i] < arr[min_idx] {
            min_idx = i;
        }
    }

    // Swap the minimum with the element at start_idx
    if min_idx != start_idx {
        arr.swap(start_idx, min_idx);
    }

    // Recursively sort the rest
    selection_sort_recursive_helper(arr, start_idx + 1);
}

// ============================================================================
// STABLE SELECTION SORT
// ============================================================================

/// Stable version of selection sort.
///
/// WHY STANDARD SELECTION SORT IS UNSTABLE:
/// ========================================
/// When we swap the minimum element with the first element of the unsorted
/// portion, we can change the relative order of equal elements.
///
/// MAKING IT STABLE:
/// ================
/// Instead of swapping, we shift all elements and insert the minimum
/// at the correct position. This preserves the relative order.
///
/// Time: O(n²) comparisons + O(n²) shifts
pub fn stable_selection_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    let n = result.len();

    for i in 0..n.saturating_sub(1) {
        // Find minimum in unsorted portion
        let mut min_idx = i;
        for j in (i + 1)..n {
            if result[j] < result[min_idx] {
                min_idx = j;
            }
        }

        // Instead of swapping, shift elements and insert
        if min_idx != i {
            let min_value = result[min_idx].clone();
            // Shift all elements between i and min_idx one position right
            for k in (i..min_idx).rev() {
                result[k + 1] = result[k].clone();
            }
            // Place minimum at position i
            result[i] = min_value;
        }
    }

    result
}

// ============================================================================
// VISUALIZATION AND STATISTICS
// ============================================================================

/// Tracks sorting operations
#[derive(Debug, Clone)]
pub struct SortStatistics {
    pub comparisons: usize,
    pub swaps: usize,
    pub array_accesses: usize,
}

impl SortStatistics {
    pub fn new() -> Self {
        Self {
            comparisons: 0,
            swaps: 0,
            array_accesses: 0,
        }
    }

    pub fn reset(&mut self) {
        self.comparisons = 0;
        self.swaps = 0;
        self.array_accesses = 0;
    }
}

impl Display for SortStatistics {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "Comparisons: {}, Swaps: {}, Array Accesses: {}",
            self.comparisons, self.swaps, self.array_accesses
        )
    }
}

/// Selection sort with operation counting
pub fn selection_sort_with_stats<T: Ord + Clone>(
    arr: &[T],
    stats: &mut SortStatistics,
) -> Vec<T> {
    stats.reset();

    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    let n = result.len();

    for i in 0..n.saturating_sub(1) {
        let mut min_idx = i;
        stats.array_accesses += 1;

        for j in (i + 1)..n {
            stats.comparisons += 1;
            stats.array_accesses += 2; // Read result[j] and result[min_idx]
            if result[j] < result[min_idx] {
                min_idx = j;
            }
        }

        if min_idx != i {
            stats.swaps += 1;
            stats.array_accesses += 4; // Two reads, two writes
            result.swap(i, min_idx);
        }
    }

    result
}

/// Creates a step-by-step visualization of selection sort
pub fn visualize_selection_sort(arr: &[i32]) -> Vec<String> {
    let mut steps = Vec::new();
    let mut result = arr.to_vec();

    steps.push("=".repeat(70));
    steps.push("SELECTION SORT VISUALIZATION".to_string());
    steps.push("=".repeat(70));
    steps.push(format!("Initial array: {:?}", result));
    steps.push(String::new());

    let n = result.len();
    for i in 0..n.saturating_sub(1) {
        steps.push(format!("Pass {}:", i + 1));
        steps.push(format!(
            "  Looking for minimum in unsorted portion: {:?}",
            &result[i..]
        ));

        let mut min_idx = i;
        let mut min_value = result[i];

        // Show the search process
        for j in (i + 1)..n {
            if result[j] < min_value {
                min_idx = j;
                min_value = result[j];
                steps.push(format!(
                    "    Found new minimum: {} at index {}",
                    min_value, min_idx
                ));
            }
        }

        // Show the swap
        if min_idx != i {
            steps.push(format!("  Swapping {} ↔ {}", result[i], result[min_idx]));
            result.swap(i, min_idx);
        } else {
            steps.push("  No swap needed (minimum already in place)".to_string());
        }

        // Show current state
        let sorted = &result[..=i];
        let unsorted = &result[i + 1..];
        steps.push(format!(
            "  Sorted: {:?} | Unsorted: {:?}",
            sorted, unsorted
        ));
        steps.push(String::new());
    }

    steps.push(format!("Final sorted array: {:?}", result));
    steps.push("=".repeat(70));

    steps
}

/// Check if a slice is sorted in ascending order
pub fn is_sorted<T: Ord>(arr: &[T]) -> bool {
    arr.windows(2).all(|w| w[0] <= w[1])
}

// ============================================================================
// DEMONSTRATION AND TESTING
// ============================================================================

fn demonstrate_selection_sort() {
    println!("📚 SELECTION SORT - EDUCATIONAL DEMONSTRATION");
    println!("{}", "=".repeat(80));

    // Test cases
    let test_cases = vec![
        (vec![64, 25, 12, 22, 11], "Random array"),
        (vec![5, 2, 8, 6, 1, 9, 4], "Small random array"),
        (vec![1], "Single element"),
        (vec![], "Empty array"),
        (vec![3, 3, 3, 3, 3], "All duplicates"),
        (vec![9, 8, 7, 6, 5, 4, 3, 2, 1], "Reverse sorted"),
        (vec![1, 2, 3, 4, 5], "Already sorted"),
        (vec![1, 3, 2, 4, 5], "Nearly sorted"),
    ];

    println!("\n📋 BASIC FUNCTIONALITY TESTS:");
    println!("{}", "-".repeat(80));

    for (arr, desc) in test_cases.iter() {
        let original = arr.clone();
        let standard = selection_sort(arr);
        let bidirectional = bidirectional_selection_sort(arr);
        let recursive = selection_sort_recursive(arr);
        let stable = stable_selection_sort(arr);

        println!("\nTest: {}", desc);
        println!("Original:      {:?}", original);
        println!("Standard:      {:?}", standard);
        println!("Bidirectional: {:?}", bidirectional);
        println!("Recursive:     {:?}", recursive);
        println!("Stable:        {:?}", stable);

        let all_correct =
            is_sorted(&standard) && is_sorted(&bidirectional) && is_sorted(&recursive) && is_sorted(&stable);

        let status = if all_correct { "✓" } else { "✗" };
        println!("All correct: {}", status);
    }

    // Visualization
    println!("\n\n🎬 STEP-BY-STEP VISUALIZATION:");
    println!("{}", "-".repeat(80));

    let demo_arr = vec![64, 25, 12, 22, 11];
    let steps = visualize_selection_sort(&demo_arr);
    for step in steps {
        println!("{}", step);
    }

    // Memory analysis
    println!("\n\n💾 MEMORY USAGE ANALYSIS:");
    println!("{}", "-".repeat(80));
    println!(
        r#"
Selection Sort Memory Characteristics:

1. In-Place Sorting:
   - Space Complexity: O(1) auxiliary space
   - Only uses constant extra memory (min_idx, loop variables)
   - Original array is modified in-place

2. Memory Writes:
   - Selection Sort: O(n) swaps (minimum writes)
   - Bubble Sort: O(n²) swaps in worst case
   - Insertion Sort: O(n²) shifts in worst case

   ⭐ This makes Selection Sort ideal when writing to memory is expensive!
      Examples: Flash memory, EEPROM, or distributed systems

3. Rust-Specific:
   - Uses swap() method for efficient swapping
   - Clone trait for creating copies
   - Ord trait for comparisons
"#
    );
}

fn performance_benchmark() {
    println!("\n\n⚡ PERFORMANCE BENCHMARK");
    println!("{}", "=".repeat(80));

    let sizes = vec![10, 20, 50, 100, 200];

    println!("\nRandom Data:");
    println!("{:<10}{:>15}{:>15}{:>15}", "Size", "Standard", "Bidirectional", "Recursive");
    println!("{}", "-".repeat(55));

    for &size in &sizes {
        let test_data: Vec<i32> = (0..size).map(|_| rand::random::<i32>() % 1000).collect();

        // Standard
        let start = Instant::now();
        let _ = selection_sort(&test_data);
        let time_standard = start.elapsed().as_secs_f64() * 1000.0;

        // Bidirectional
        let start = Instant::now();
        let _ = bidirectional_selection_sort(&test_data);
        let time_bidirectional = start.elapsed().as_secs_f64() * 1000.0;

        // Recursive
        let start = Instant::now();
        let _ = selection_sort_recursive(&test_data);
        let time_recursive = start.elapsed().as_secs_f64() * 1000.0;

        println!(
            "{:<10}{:>14.3}ms{:>14.3}ms{:>14.3}ms",
            size, time_standard, time_bidirectional, time_recursive
        );
    }
}

// ============================================================================
// UNIT TESTS
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_sorting() {
        let arr = vec![64, 25, 12, 22, 11];
        let sorted = selection_sort(&arr);
        assert_eq!(sorted, vec![11, 12, 22, 25, 64]);
    }

    #[test]
    fn test_empty_array() {
        let arr: Vec<i32> = vec![];
        let sorted = selection_sort(&arr);
        assert_eq!(sorted, vec![]);
    }

    #[test]
    fn test_single_element() {
        let arr = vec![1];
        let sorted = selection_sort(&arr);
        assert_eq!(sorted, vec![1]);
    }

    #[test]
    fn test_already_sorted() {
        let arr = vec![1, 2, 3, 4, 5];
        let sorted = selection_sort(&arr);
        assert_eq!(sorted, vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_reverse_sorted() {
        let arr = vec![5, 4, 3, 2, 1];
        let sorted = selection_sort(&arr);
        assert_eq!(sorted, vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_duplicates() {
        let arr = vec![3, 1, 4, 1, 5, 9, 2, 6];
        let sorted = selection_sort(&arr);
        assert!(is_sorted(&sorted));
    }

    #[test]
    fn test_all_implementations_match() {
        let arr = vec![64, 25, 12, 22, 11];
        let standard = selection_sort(&arr);
        let bidirectional = bidirectional_selection_sort(&arr);
        let recursive = selection_sort_recursive(&arr);
        let stable = stable_selection_sort(&arr);

        assert_eq!(standard, bidirectional);
        assert_eq!(standard, recursive);
        assert_eq!(standard, stable);
    }

    #[test]
    fn test_stability() {
        #[derive(Debug, Clone, PartialEq, Eq)]
        struct Item {
            value: i32,
            original_index: usize,
        }

        impl Ord for Item {
            fn cmp(&self, other: &Self) -> Ordering {
                self.value.cmp(&other.value)
            }
        }

        impl PartialOrd for Item {
            fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
                Some(self.cmp(other))
            }
        }

        let data = vec![
            Item { value: 3, original_index: 0 },
            Item { value: 1, original_index: 1 },
            Item { value: 3, original_index: 2 },
            Item { value: 2, original_index: 3 },
            Item { value: 3, original_index: 4 },
        ];

        let sorted = stable_selection_sort(&data);

        // Check that all 3's maintain their original order
        let threes: Vec<_> = sorted
            .iter()
            .filter(|item| item.value == 3)
            .map(|item| item.original_index)
            .collect();

        assert_eq!(threes, vec![0, 2, 4]);
    }
}

fn main() {
    demonstrate_selection_sort();
    performance_benchmark();

    println!("\n✨ Selection Sort demonstration complete!");
}
