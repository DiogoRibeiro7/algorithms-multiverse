// Insertion Sort Algorithm Implementation in Rust
//
// Time Complexity:
// - Best Case: O(n) - when array is already sorted
// - Average Case: O(n²)
// - Worst Case: O(n²) - when array is reverse sorted
// Space Complexity: O(1) for in-place, O(n) for functional approach
//
// Insertion Sort builds the final sorted array one item at a time.
//
// Rust features:
// - Generic functions with trait bounds
// - Ownership and borrowing
// - Zero-cost abstractions
// - Type safety
// - Comprehensive testing

use std::fmt::Debug;
use std::time::Instant;

/// Standard insertion sort implementation.
///
/// Time Complexity: O(n²) average and worst case, O(n) best case
/// Space Complexity: O(n) for the new vector
///
/// Example visualization:
///   Initial: [5, 2, 8, 6, 1]
///   Step 1:  [2, 5, 8, 6, 1]  // Insert 2
///   Step 2:  [2, 5, 8, 6, 1]  // 8 already in place
///   Step 3:  [2, 5, 6, 8, 1]  // Insert 6
///   Step 4:  [1, 2, 5, 6, 8]  // Insert 1
pub fn insertion_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    insertion_sort_in_place(&mut result);
    result
}

/// In-place insertion sort implementation.
///
/// Time Complexity: O(n²) average and worst case, O(n) best case
/// Space Complexity: O(1)
pub fn insertion_sort_in_place<T: Ord>(arr: &mut [T]) {
    for i in 1..arr.len() {
        let mut j = i;

        // Move elements greater than key one position ahead
        while j > 0 && arr[j - 1] > arr[j] {
            arr.swap(j - 1, j);
            j -= 1;
        }
    }
}

/// Recursive insertion sort implementation.
///
/// Time Complexity: O(n²)
/// Space Complexity: O(n) for recursion stack + O(n) for new vector
pub fn insertion_sort_recursive<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    let mut result = arr.to_vec();
    insertion_sort_recursive_helper(&mut result, result.len());
    result
}

fn insertion_sort_recursive_helper<T: Ord>(arr: &mut [T], n: usize) {
    // Base case
    if n <= 1 {
        return;
    }

    // Sort first n-1 elements
    insertion_sort_recursive_helper(arr, n - 1);

    // Insert last element at its correct position
    let mut j = n - 1;
    while j > 0 && arr[j - 1] > arr[j] {
        arr.swap(j - 1, j);
        j -= 1;
    }
}

/// Binary insertion sort - uses binary search to find insertion position.
///
/// Time Complexity: O(n²) for moves, O(n log n) for comparisons
/// Space Complexity: O(n)
pub fn binary_insertion_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();

    for i in 1..result.len() {
        let key = result[i].clone();

        // Find position using binary search
        let pos = binary_search_position(&result[..i], &key);

        // Rotate elements to make space
        result[pos..=i].rotate_right(1);
        result[pos] = key;
    }

    result
}

fn binary_search_position<T: Ord>(arr: &[T], key: &T) -> usize {
    let mut left = 0;
    let mut right = arr.len();

    while left < right {
        let mid = left + (right - left) / 2;

        if arr[mid] <= *key {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    left
}

/// Shell sort - a generalization of insertion sort.
///
/// Time Complexity: Depends on gap sequence (O(n log²n) for good sequences)
/// Space Complexity: O(n)
pub fn shell_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    let n = result.len();

    // Start with a large gap, then reduce (Knuth's sequence)
    let mut gap = 1;
    while gap < n / 3 {
        gap = 3 * gap + 1;
    }

    // Perform gapped insertion sort
    while gap > 0 {
        for i in gap..n {
            let mut j = i;

            // Insertion sort with gap
            while j >= gap && result[j - gap] > result[j] {
                result.swap(j - gap, j);
                j -= gap;
            }
        }

        gap /= 3;
    }

    result
}

/// Insertion sort with custom comparison function.
pub fn insertion_sort_by<T: Clone, F>(arr: &[T], mut compare: F) -> Vec<T>
where
    F: FnMut(&T, &T) -> std::cmp::Ordering,
{
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();

    for i in 1..result.len() {
        let mut j = i;

        while j > 0 && compare(&result[j - 1], &result[j]) == std::cmp::Ordering::Greater {
            result.swap(j - 1, j);
            j -= 1;
        }
    }

    result
}

/// Check if a slice is sorted in ascending order.
pub fn is_sorted<T: Ord>(arr: &[T]) -> bool {
    for i in 0..arr.len().saturating_sub(1) {
        if arr[i] > arr[i + 1] {
            return false;
        }
    }
    true
}

/// Statistics for tracking sort operations.
#[derive(Debug, Clone, Default)]
pub struct SortStatistics {
    pub comparisons: usize,
    pub swaps: usize,
}

impl SortStatistics {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn reset(&mut self) {
        self.comparisons = 0;
        self.swaps = 0;
    }
}

impl std::fmt::Display for SortStatistics {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Comparisons: {}, Swaps: {}", self.comparisons, self.swaps)
    }
}

/// Insertion sort with statistics tracking.
pub fn insertion_sort_with_stats<T: Ord + Clone>(
    arr: &[T],
    stats: &mut SortStatistics,
) -> Vec<T> {
    stats.reset();

    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();

    for i in 1..result.len() {
        let mut j = i;

        while j > 0 {
            stats.comparisons += 1;
            if result[j - 1] > result[j] {
                result.swap(j - 1, j);
                stats.swaps += 1;
                j -= 1;
            } else {
                break;
            }
        }
    }

    result
}

/// Create a step-by-step visualization of insertion sort.
pub fn visualize_insertion_sort(arr: &[i32]) -> Vec<String> {
    let mut steps = Vec::new();
    let mut result = arr.to_vec();

    steps.push(format!("Initial: {:?}", result));

    for i in 1..result.len() {
        let key = result[i];
        let mut j = i;

        steps.push(format!("\nStep {}: Inserting {}", i, key));
        steps.push(format!("  Before: {:?}", result));

        while j > 0 && result[j - 1] > key {
            result.swap(j - 1, j);
            j -= 1;
        }

        steps.push(format!("  After:  {:?}", result));
    }

    steps.push(format!("\nFinal: {:?}", result));
    steps
}

/// Demonstrate stability of insertion sort.
fn demonstrate_stability() {
    #[derive(Debug, Clone)]
    struct Pair {
        value: i32,
        original_index: usize,
    }

    impl PartialEq for Pair {
        fn eq(&self, other: &Self) -> bool {
            self.value == other.value
        }
    }

    impl Eq for Pair {}

    impl PartialOrd for Pair {
        fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
            Some(self.cmp(other))
        }
    }

    impl Ord for Pair {
        fn cmp(&self, other: &Self) -> std::cmp::Ordering {
            self.value.cmp(&other.value)
        }
    }

    let data = vec![
        Pair { value: 3, original_index: 0 },
        Pair { value: 1, original_index: 1 },
        Pair { value: 3, original_index: 2 },
        Pair { value: 2, original_index: 3 },
        Pair { value: 3, original_index: 4 },
    ];

    println!("Stability Demonstration:");
    print!("Original: ");
    for p in &data {
        print!("({},{}) ", p.value, p.original_index);
    }
    println!();

    let sorted = insertion_sort(&data);
    print!("Sorted:   ");
    for p in &sorted {
        print!("({},{}) ", p.value, p.original_index);
    }
    println!();

    // Check stability
    let three_indices: Vec<usize> = sorted
        .iter()
        .filter(|p| p.value == 3)
        .map(|p| p.original_index)
        .collect();

    let is_stable = three_indices == vec![0, 2, 4];
    println!("Stable: {} (indices of 3's: {:?})", is_stable, three_indices);
}

/// Print a slice with a label.
fn print_slice<T: Debug>(arr: &[T], label: &str) {
    println!("{}: {:?}", label, arr);
}

/// Demonstrate various insertion sort implementations.
fn demonstrate_insertion_sort() {
    println!("📝 Insertion Sort Implementation in Rust");
    println!("{}", "=".repeat(60));

    // Test data
    let test_cases = vec![
        (vec![64, 34, 25, 12, 22, 11, 90], "Random array"),
        (vec![5, 2, 8, 6, 1, 9, 4], "Small random array"),
        (vec![1], "Single element"),
        (vec![], "Empty array"),
        (vec![3, 3, 3, 3, 3], "All duplicates"),
        (vec![9, 8, 7, 6, 5, 4, 3, 2, 1], "Reverse sorted"),
        (vec![1, 2, 3, 4, 5], "Already sorted"),
        (vec![1, 3, 2, 4, 5], "Nearly sorted"),
    ];

    println!("\n📋 Basic Sorting Tests:");
    println!("{}", "-".repeat(60));

    for (arr, desc) in test_cases {
        let original = arr.clone();

        let standard_result = insertion_sort(&arr);
        let binary_result = binary_insertion_sort(&arr);
        let shell_result = shell_sort(&arr);
        let recursive_result = insertion_sort_recursive(&arr);

        println!("\nTest: {}", desc);
        print_slice(&original, "Original");
        print_slice(&standard_result, "Sorted  ");

        let all_correct = is_sorted(&standard_result)
            && is_sorted(&binary_result)
            && is_sorted(&shell_result)
            && is_sorted(&recursive_result);

        let all_equal = standard_result == binary_result
            && standard_result == shell_result
            && standard_result == recursive_result;

        let status = if all_correct && all_equal { "✓" } else { "✗" };
        println!("All implementations match: {}", status);
    }

    // Visualization demo
    println!("\n\n🎬 Step-by-Step Visualization:");
    println!("{}", "-".repeat(60));

    let demo_arr = vec![5, 2, 8, 6, 1];
    let steps = visualize_insertion_sort(&demo_arr);
    for step in steps {
        println!("{}", step);
    }

    // Stability demonstration
    println!("\n\n🔒 Stability Demonstration:");
    println!("{}", "-".repeat(60));
    demonstrate_stability();

    // Performance analysis
    println!("\n\n📊 Operation Counting:");
    println!("{}", "-".repeat(60));

    let stat_test_cases = vec![
        (vec![5, 2, 8, 6, 1], "Random"),
        (vec![1, 2, 3, 4, 5], "Already sorted"),
        (vec![5, 4, 3, 2, 1], "Reverse sorted"),
    ];

    for (arr, desc) in stat_test_cases {
        let mut stats = SortStatistics::new();
        insertion_sort_with_stats(&arr, &mut stats);

        let n = arr.len();
        println!("\n{}: {:?}", desc, arr);
        println!("Array size (n): {}", n);
        println!("Comparisons: {}", stats.comparisons);
        println!("Swaps: {}", stats.swaps);
        println!("Best case comparisons: {}", n - 1);
        println!("Worst case comparisons: {}", n * (n - 1) / 2);
    }
}

/// Benchmark insertion sort.
fn performance_benchmark() {
    println!("\n\n⚡ Performance Benchmark");
    println!("{}", "=".repeat(80));
    println!("\nInsertion sort is preferred for:");
    println!("  • Small arrays (typically n < 10-20)");
    println!("  • Nearly sorted arrays");
    println!("  • As part of hybrid sorting algorithms");
    println!();

    let sizes = vec![5, 10, 20, 50, 100, 500, 1000];

    let patterns: Vec<(&str, Box<dyn Fn(usize) -> Vec<i32>>)> = vec![
        (
            "Random",
            Box::new(|n| {
                use rand::Rng;
                let mut rng = rand::thread_rng();
                (0..n).map(|_| rng.gen_range(1..1001)).collect()
            }),
        ),
        (
            "Nearly Sorted",
            Box::new(|n| {
                use rand::Rng;
                let mut rng = rand::thread_rng();
                let mut arr: Vec<i32> = (0..n as i32).collect();
                for _ in 0..std::cmp::min(5, n / 10) {
                    let idx1 = rng.gen_range(0..n);
                    let idx2 = rng.gen_range(0..n);
                    arr.swap(idx1, idx2);
                }
                arr
            }),
        ),
        (
            "Reversed",
            Box::new(|n| (0..n as i32).rev().collect()),
        ),
    ];

    for (pattern_name, pattern_gen) in &patterns {
        println!("\n{} Data:", pattern_name);
        println!("{:<8}{:>15}{:>15}{:>15}{:>15}", "Size", "Insertion", "Binary", "Shell", "slice.sort");
        println!("{}", "-".repeat(68));

        for &size in &sizes {
            let test_data = pattern_gen(size);
            print!("{:<8}", size);

            // Insertion Sort
            let start = Instant::now();
            let _ = insertion_sort(&test_data);
            let duration = start.elapsed();
            print!("{:>14.3}ms", duration.as_secs_f64() * 1000.0);

            // Binary Insertion Sort
            let start = Instant::now();
            let _ = binary_insertion_sort(&test_data);
            let duration = start.elapsed();
            print!("{:>14.3}ms", duration.as_secs_f64() * 1000.0);

            // Shell Sort
            let start = Instant::now();
            let _ = shell_sort(&test_data);
            let duration = start.elapsed();
            print!("{:>14.3}ms", duration.as_secs_f64() * 1000.0);

            // slice.sort
            let mut test_data2 = test_data.clone();
            let start = Instant::now();
            test_data2.sort();
            let duration = start.elapsed();
            println!("{:>14.3}ms", duration.as_secs_f64() * 1000.0);
        }
    }
}

fn main() {
    demonstrate_insertion_sort();
    performance_benchmark();

    println!("\n✨ Insertion Sort demonstration complete!");
}

// Cargo.toml would include:
/*
[dependencies]
rand = "0.8"
*/

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_insertion_sort() {
        let arr = vec![64, 34, 25, 12, 22, 11, 90];
        let sorted = insertion_sort(&arr);
        assert_eq!(sorted, vec![11, 12, 22, 25, 34, 64, 90]);
    }

    #[test]
    fn test_empty_array() {
        let arr: Vec<i32> = vec![];
        let sorted = insertion_sort(&arr);
        assert_eq!(sorted, vec![]);
    }

    #[test]
    fn test_single_element() {
        let arr = vec![1];
        let sorted = insertion_sort(&arr);
        assert_eq!(sorted, vec![1]);
    }

    #[test]
    fn test_already_sorted() {
        let arr = vec![1, 2, 3, 4, 5];
        let sorted = insertion_sort(&arr);
        assert_eq!(sorted, vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_reverse_sorted() {
        let arr = vec![5, 4, 3, 2, 1];
        let sorted = insertion_sort(&arr);
        assert_eq!(sorted, vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_all_implementations_match() {
        let arr = vec![5, 2, 8, 6, 1, 9, 4];

        let standard = insertion_sort(&arr);
        let binary = binary_insertion_sort(&arr);
        let shell = shell_sort(&arr);
        let recursive = insertion_sort_recursive(&arr);

        assert_eq!(standard, binary);
        assert_eq!(standard, shell);
        assert_eq!(standard, recursive);
        assert!(is_sorted(&standard));
    }

    #[test]
    fn test_stability() {
        #[derive(Debug, Clone, PartialEq, Eq)]
        struct Item {
            key: i32,
            id: usize,
        }

        impl PartialOrd for Item {
            fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
                Some(self.cmp(other))
            }
        }

        impl Ord for Item {
            fn cmp(&self, other: &Self) -> std::cmp::Ordering {
                self.key.cmp(&other.key)
            }
        }

        let arr = vec![
            Item { key: 3, id: 0 },
            Item { key: 1, id: 1 },
            Item { key: 3, id: 2 },
        ];

        let sorted = insertion_sort(&arr);

        // Items with same key should maintain relative order
        assert_eq!(sorted[1].id, 0);
        assert_eq!(sorted[2].id, 2);
    }
}
