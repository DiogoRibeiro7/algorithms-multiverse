// Bubble Sort Algorithm Implementation in Rust
//
// Time Complexity:
// - Best Case: O(n) - when array is already sorted (optimized version)
// - Average Case: O(n²)
// - Worst Case: O(n²) - when array is reverse sorted
// Space Complexity: O(1) for in-place, O(n) for functional approach
//
// Bubble Sort works by repeatedly stepping through the list, comparing adjacent
// elements and swapping them if they are in the wrong order. The pass through
// the list is repeated until the list is sorted.
//
// Rust features:
// - Generic functions with trait bounds
// - Ownership and borrowing
// - Iterator patterns
// - Zero-cost abstractions
// - Type safety

use std::time::Instant;
use std::fmt::Debug;

/// Basic iterative bubble sort implementation.
///
/// This is the standard bubble sort algorithm that compares and swaps
/// adjacent elements until the entire slice is sorted.
///
/// # Arguments
/// * `arr` - Slice to be sorted
///
/// # Returns
/// New sorted vector
///
/// Time Complexity: O(n²) in all cases (no optimization)
/// Space Complexity: O(n) for the new vector
pub fn bubble_sort_iterative<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    let n = result.len();

    // Outer loop for number of passes
    for i in 0..n {
        // Inner loop for comparisons
        // After each pass, the largest element "bubbles up" to its position
        for j in 0..n - i - 1 {
            if result[j] > result[j + 1] {
                // Swap adjacent elements
                result.swap(j, j + 1);
            }
        }
    }

    result
}

/// Optimized bubble sort with early termination.
///
/// This version includes a flag to detect if any swaps were made during a pass.
/// If no swaps occur, the array is already sorted and we can terminate early.
///
/// # Arguments
/// * `arr` - Slice to be sorted
///
/// # Returns
/// New sorted vector
///
/// Time Complexity:
///   - Best Case: O(n) when already sorted
///   - Average/Worst: O(n²)
/// Space Complexity: O(n) for the new vector
pub fn bubble_sort_optimized<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    let n = result.len();

    for i in 0..n {
        // Flag to optimize for already sorted arrays
        let mut swapped = false;

        for j in 0..n - i - 1 {
            if result[j] > result[j + 1] {
                result.swap(j, j + 1);
                swapped = true;
            }
        }

        // If no swaps occurred, array is sorted
        if !swapped {
            break;
        }
    }

    result
}

/// In-place bubble sort implementation (optimized).
///
/// Sorts the slice in-place without creating a new vector,
/// minimizing space complexity.
///
/// # Arguments
/// * `arr` - Mutable slice to be sorted in-place
///
/// Time Complexity: O(n) best case, O(n²) average/worst
/// Space Complexity: O(1)
pub fn bubble_sort_in_place<T: Ord>(arr: &mut [T]) {
    let n = arr.len();

    for i in 0..n {
        let mut swapped = false;

        for j in 0..n - i - 1 {
            if arr[j] > arr[j + 1] {
                arr.swap(j, j + 1);
                swapped = true;
            }
        }

        if !swapped {
            break;
        }
    }
}

/// Recursive bubble sort implementation.
///
/// Each recursive call performs one pass through the array,
/// bubbling the largest element to the end.
///
/// # Arguments
/// * `arr` - Slice to be sorted
///
/// # Returns
/// New sorted vector
///
/// Time Complexity: O(n²)
/// Space Complexity: O(n) for recursion stack + O(n) for new vector
pub fn bubble_sort_recursive<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    let mut result = arr.to_vec();
    bubble_sort_recursive_helper(&mut result, result.len());
    result
}

fn bubble_sort_recursive_helper<T: Ord>(arr: &mut [T], n: usize) {
    // Base case: single element or empty
    if n <= 1 {
        return;
    }

    // One pass of bubble sort
    // After this pass, the largest element will be at the end
    for i in 0..n - 1 {
        if arr[i] > arr[i + 1] {
            arr.swap(i, i + 1);
        }
    }

    // Recursively sort the first n-1 elements
    bubble_sort_recursive_helper(arr, n - 1);
}

/// Functional-style bubble sort implementation.
///
/// This implementation uses functional programming principles,
/// creating new vectors for immutability.
///
/// # Arguments
/// * `arr` - Slice to be sorted
///
/// # Returns
/// New sorted vector
///
/// Time Complexity: O(n²)
/// Space Complexity: O(n)
pub fn bubble_sort_functional<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    let n = result.len();

    for i in 0..n {
        let mut swapped = false;

        for j in 0..n - i - 1 {
            if result[j] > result[j + 1] {
                result.swap(j, j + 1);
                swapped = true;
            }
        }

        if !swapped {
            break;
        }
    }

    result
}

/// Bubble sort with custom comparison function.
///
/// # Arguments
/// * `arr` - Slice to be sorted
/// * `compare` - Comparison function
///
/// # Returns
/// New sorted vector
pub fn bubble_sort_with_comparator<T: Clone, F>(arr: &[T], compare: F) -> Vec<T>
where
    F: Fn(&T, &T) -> std::cmp::Ordering,
{
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    let n = result.len();

    for i in 0..n {
        let mut swapped = false;

        for j in 0..n - i - 1 {
            if compare(&result[j], &result[j + 1]) == std::cmp::Ordering::Greater {
                result.swap(j, j + 1);
                swapped = true;
            }
        }

        if !swapped {
            break;
        }
    }

    result
}

/// Cocktail Shaker Sort (bidirectional bubble sort).
///
/// An optimized version of bubble sort that sorts in both directions
/// alternately, which can be more efficient for certain data patterns.
///
/// # Arguments
/// * `arr` - Slice to be sorted
///
/// # Returns
/// New sorted vector
///
/// Time Complexity: O(n²) worst case, but often faster than standard bubble sort
/// Space Complexity: O(n)
pub fn cocktail_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    let mut start = 0;
    let mut end = result.len() - 1;
    let mut swapped = true;

    while swapped {
        swapped = false;

        // Forward pass (like bubble sort)
        for i in start..end {
            if result[i] > result[i + 1] {
                result.swap(i, i + 1);
                swapped = true;
            }
        }

        if !swapped {
            break;
        }

        swapped = false;
        if end > 0 {
            end -= 1;
        }

        // Backward pass
        if end > start {
            for i in (start..end).rev() {
                if result[i] > result[i + 1] {
                    result.swap(i, i + 1);
                    swapped = true;
                }
            }
        }

        start += 1;
    }

    result
}

/// Check if a slice is sorted in ascending order.
///
/// # Arguments
/// * `arr` - Slice to check
///
/// # Returns
/// true if sorted, false otherwise
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
    pub iterations: usize,
}

impl SortStatistics {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn reset(&mut self) {
        self.comparisons = 0;
        self.swaps = 0;
        self.iterations = 0;
    }
}

impl std::fmt::Display for SortStatistics {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "Comparisons: {}, Swaps: {}, Iterations: {}",
            self.comparisons, self.swaps, self.iterations
        )
    }
}

/// Bubble sort with statistics tracking.
///
/// # Arguments
/// * `arr` - Slice to be sorted
/// * `stats` - Mutable reference to statistics struct
///
/// # Returns
/// New sorted vector
pub fn bubble_sort_with_stats<T: Ord + Clone>(
    arr: &[T],
    stats: &mut SortStatistics,
) -> Vec<T> {
    stats.reset();

    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    let n = result.len();

    for i in 0..n {
        stats.iterations += 1;
        let mut swapped = false;

        for j in 0..n - i - 1 {
            stats.comparisons += 1;
            if result[j] > result[j + 1] {
                result.swap(j, j + 1);
                stats.swaps += 1;
                swapped = true;
            }
        }

        if !swapped {
            break;
        }
    }

    result
}

/// BubbleSorter struct with state and statistics.
pub struct BubbleSorter {
    stats: SortStatistics,
}

impl BubbleSorter {
    pub fn new() -> Self {
        Self {
            stats: SortStatistics::new(),
        }
    }

    pub fn sort<T: Ord + Clone>(&mut self, arr: &[T]) -> Vec<T> {
        bubble_sort_with_stats(arr, &mut self.stats)
    }

    pub fn get_stats(&self) -> &SortStatistics {
        &self.stats
    }

    pub fn reset_stats(&mut self) {
        self.stats.reset();
    }
}

impl Default for BubbleSorter {
    fn default() -> Self {
        Self::new()
    }
}

/// Print a slice with a label.
fn print_slice<T: Debug>(arr: &[T], label: &str) {
    println!("{}: {:?}", label, arr);
}

/// Demonstrate various bubble sort implementations.
fn demonstrate_bubble_sort() {
    println!("🫧 Bubble Sort Implementation in Rust");
    println!("{}", "=".repeat(50));

    // Test data - comprehensive edge cases
    let test_cases = vec![
        (vec![64, 34, 25, 12, 22, 11, 90], "Random array"),
        (vec![5, 2, 8, 6, 1, 9, 4], "Small random array"),
        (vec![1], "Single element"),
        (vec![], "Empty array"),
        (vec![3, 3, 3, 3, 3], "All duplicates"),
        (vec![9, 8, 7, 6, 5, 4, 3, 2, 1], "Reverse sorted"),
        (vec![1, 2, 3, 4, 5], "Already sorted"),
        (vec![5, 1, 4, 2, 3], "Nearly sorted"),
    ];

    println!("\n📋 Basic Sorting Tests:");
    println!("{}", "-".repeat(50));

    for (arr, desc) in test_cases {
        let original = arr.clone();

        // Test different implementations
        let iterative_result = bubble_sort_iterative(&arr);
        let optimized_result = bubble_sort_optimized(&arr);
        let recursive_result = bubble_sort_recursive(&arr);
        let cocktail_result = cocktail_sort(&arr);

        // Test in-place
        let mut inplace_result = arr.clone();
        bubble_sort_in_place(&mut inplace_result);

        println!("\nTest: {}", desc);
        print_slice(&original, "Original");
        print_slice(&iterative_result, "Sorted  ");

        // Verify all results are correct and equal
        let all_correct = is_sorted(&iterative_result)
            && is_sorted(&optimized_result)
            && is_sorted(&recursive_result)
            && is_sorted(&cocktail_result)
            && is_sorted(&inplace_result);

        let all_equal = iterative_result == optimized_result
            && iterative_result == recursive_result
            && iterative_result == cocktail_result
            && iterative_result == inplace_result;

        let status = if all_correct && all_equal { "✓" } else { "✗" };
        println!("All implementations match: {}", status);
    }

    println!("\n{}", "-".repeat(50));

    // String sorting
    let words = vec!["banana", "apple", "cherry", "date", "elderberry"];
    let sorted_words = bubble_sort_optimized(&words);

    println!("\n🔤 Word sorting:");
    print_slice(&words, "Original    ");
    print_slice(&sorted_words, "Alphabetical");

    // Custom comparison (descending)
    let numbers = vec![3, 1, 4, 1, 5, 9, 2, 6];
    let desc_sorted = bubble_sort_with_comparator(&numbers, |a, b| b.cmp(a));

    println!("\n🔢 Custom comparison (descending):");
    print_slice(&numbers, "Original  ");
    print_slice(&desc_sorted, "Descending");
}

/// Benchmark different bubble sort implementations.
fn performance_benchmark() {
    println!("\n\n⚡ Performance Benchmark");
    println!("{}", "=".repeat(70));

    let sizes = vec![100, 500, 1000, 2000];

    // Test different data patterns
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
            "Sorted",
            Box::new(|n| (0..n as i32).collect()),
        ),
        (
            "Reversed",
            Box::new(|n| (0..n as i32).rev().collect()),
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
    ];

    let methods: Vec<(&str, Box<dyn Fn(&[i32]) -> Vec<i32>>)> = vec![
        ("Iterative", Box::new(bubble_sort_iterative)),
        ("Optimized", Box::new(bubble_sort_optimized)),
        ("Recursive", Box::new(bubble_sort_recursive)),
        ("Cocktail", Box::new(cocktail_sort)),
        (
            "slice.sort",
            Box::new(|arr: &[i32]| {
                let mut result = arr.to_vec();
                result.sort();
                result
            }),
        ),
    ];

    for (pattern_name, pattern_gen) in &patterns {
        println!("\n{} Data:", pattern_name);

        // Header
        print!("{:<8}", "Size");
        for (method_name, _) in &methods {
            print!("{:>12}", method_name);
        }
        println!();
        println!("{}", "-".repeat(8 + 12 * methods.len()));

        for &size in &sizes {
            let test_data = pattern_gen(size);
            print!("{:<8}", size);

            for (method_name, method_func) in &methods {
                // Skip recursive for large sizes
                if *method_name == "Recursive" && size > 1000 {
                    print!("{:>12}", "N/A");
                    continue;
                }

                // Warm-up
                let _ = method_func(&test_data);

                // Benchmark
                let start = Instant::now();
                let result = method_func(&test_data);
                let duration = start.elapsed();

                let elapsed_ms = duration.as_secs_f64() * 1000.0;
                print!("{:>11.2}ms", elapsed_ms);

                // Verify correctness
                if !is_sorted(&result) {
                    print!(" ✗");
                }
            }

            println!();
        }
    }
}

/// Analyze bubble sort behavior with different inputs.
fn analyze_algorithm() {
    println!("\n\n🔍 Algorithm Analysis");
    println!("{}", "=".repeat(50));

    let test_cases = vec![
        (vec![5, 2, 8, 6, 1], "Random"),
        (vec![1, 2, 3, 4, 5], "Already sorted"),
        (vec![5, 4, 3, 2, 1], "Reverse sorted"),
    ];

    for (arr, desc) in test_cases {
        let mut stats = SortStatistics::new();
        bubble_sort_with_stats(&arr, &mut stats);

        let n = arr.len();
        let theoretical_max = n * (n - 1) / 2;

        println!("\n{}: {:?}", desc, arr);
        println!("Array size (n): {}", n);
        println!(
            "Comparisons: {} (theoretical max: {})",
            stats.comparisons, theoretical_max
        );
        println!("Swaps: {}", stats.swaps);

        let efficiency = if stats.comparisons > 0 {
            (1.0 - stats.swaps as f64 / stats.comparisons as f64) * 100.0
        } else {
            0.0
        };
        println!("Efficiency: {:.1}% (fewer swaps is better)", efficiency);
    }
}

fn main() {
    demonstrate_bubble_sort();
    performance_benchmark();
    analyze_algorithm();

    // Demonstrate OOP approach
    println!("\n\n📊 Object-Oriented Approach");
    println!("{}", "=".repeat(50));

    let mut sorter = BubbleSorter::new();
    let test_array = vec![64, 34, 25, 12, 22, 11, 90];

    let sorted_array = sorter.sort(&test_array);
    let stats = sorter.get_stats();

    print_slice(&test_array, "Original");
    print_slice(&sorted_array, "Sorted  ");
    println!("Statistics: {}", stats);

    println!("\n✨ Bubble Sort demonstration complete!");
}

// Cargo.toml would include:
/*
[package]
name = "bubblesort"
version = "0.1.0"
edition = "2021"

[dependencies]
rand = "0.8"
*/

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_array() {
        let arr: Vec<i32> = vec![];
        assert_eq!(bubble_sort_optimized(&arr), vec![]);
    }

    #[test]
    fn test_single_element() {
        let arr = vec![1];
        assert_eq!(bubble_sort_optimized(&arr), vec![1]);
    }

    #[test]
    fn test_already_sorted() {
        let arr = vec![1, 2, 3, 4, 5];
        assert_eq!(bubble_sort_optimized(&arr), vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_reverse_sorted() {
        let arr = vec![5, 4, 3, 2, 1];
        assert_eq!(bubble_sort_optimized(&arr), vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_random_array() {
        let arr = vec![64, 34, 25, 12, 22, 11, 90];
        assert_eq!(
            bubble_sort_optimized(&arr),
            vec![11, 12, 22, 25, 34, 64, 90]
        );
    }

    #[test]
    fn test_duplicates() {
        let arr = vec![3, 3, 3, 3, 3];
        assert_eq!(bubble_sort_optimized(&arr), vec![3, 3, 3, 3, 3]);
    }

    #[test]
    fn test_all_implementations_match() {
        let arr = vec![5, 2, 8, 6, 1, 9, 4];

        let iter_result = bubble_sort_iterative(&arr);
        let opt_result = bubble_sort_optimized(&arr);
        let rec_result = bubble_sort_recursive(&arr);
        let cocktail_result = cocktail_sort(&arr);

        assert_eq!(iter_result, opt_result);
        assert_eq!(iter_result, rec_result);
        assert_eq!(iter_result, cocktail_result);
        assert!(is_sorted(&iter_result));
    }

    #[test]
    fn test_in_place() {
        let mut arr = vec![5, 2, 8, 6, 1];
        bubble_sort_in_place(&mut arr);
        assert_eq!(arr, vec![1, 2, 5, 6, 8]);
    }

    #[test]
    fn test_strings() {
        let arr = vec!["banana", "apple", "cherry"];
        assert_eq!(
            bubble_sort_optimized(&arr),
            vec!["apple", "banana", "cherry"]
        );
    }
}
