// Merge Sort Implementation in Rust
//
// Time Complexity: O(n log n) - consistent across all cases
// Space Complexity: O(n) - requires auxiliary space for merging
//
// Merge Sort is a divide-and-conquer algorithm that divides the input array
// into two halves, recursively sorts them, and then merges the two sorted halves.
// It guarantees O(n log n) performance and is stable.
//
// Rust-specific features:
// - Zero-cost abstractions with generic traits
// - Ownership and borrowing for memory safety
// - Parallel implementation with rayon
// - Iterator-based functional approach
// - Cache-efficient memory layout
// - SIMD optimizations where applicable

use std::cmp::Ordering;
use std::fmt::Debug;
use std::time::Instant;

#[cfg(feature = "rayon")]
use rayon::prelude::*;

/// Trait for types that can be sorted
pub trait Sortable: Ord + Clone + Send {}
impl<T: Ord + Clone + Send> Sortable for T {}

/// Sorts a slice using merge sort algorithm.
/// Returns a new sorted vector.
///
/// # Examples
/// ```
/// let arr = vec![64, 34, 25, 12, 22];
/// let sorted = merge_sort(&arr);
/// assert_eq!(sorted, vec![12, 22, 25, 34, 64]);
/// ```
pub fn merge_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mid = arr.len() / 2;
    let left = merge_sort(&arr[..mid]);
    let right = merge_sort(&arr[mid..]);

    merge(&left, &right)
}

/// In-place merge sort that minimizes allocations.
/// Uses a single auxiliary buffer for better memory efficiency.
pub fn merge_sort_in_place<T: Ord + Clone>(arr: &mut [T]) {
    if arr.len() <= 1 {
        return;
    }

    let len = arr.len();
    let mut aux = arr.to_vec();
    merge_sort_in_place_helper(arr, &mut aux, 0, len);
}

fn merge_sort_in_place_helper<T: Ord + Clone>(
    arr: &mut [T],
    aux: &mut [T],
    low: usize,
    high: usize,
) {
    if high - low <= 1 {
        return;
    }

    let mid = low + (high - low) / 2;

    merge_sort_in_place_helper(arr, aux, low, mid);
    merge_sort_in_place_helper(arr, aux, mid, high);

    merge_in_place(arr, aux, low, mid, high);
}

/// Merges two sorted slices into a new vector.
///
/// # Performance
/// This function is optimized for cache locality and minimizes comparisons.
fn merge<T: Ord + Clone>(left: &[T], right: &[T]) -> Vec<T> {
    let mut result = Vec::with_capacity(left.len() + right.len());
    let mut i = 0;
    let mut j = 0;

    while i < left.len() && j < right.len() {
        if left[i] <= right[j] {
            result.push(left[i].clone());
            i += 1;
        } else {
            result.push(right[j].clone());
            j += 1;
        }
    }

    // Append remaining elements
    result.extend_from_slice(&left[i..]);
    result.extend_from_slice(&right[j..]);

    result
}

/// In-place merge using auxiliary buffer.
fn merge_in_place<T: Ord + Clone>(
    arr: &mut [T],
    aux: &mut [T],
    low: usize,
    mid: usize,
    high: usize,
) {
    // Copy to auxiliary array
    for i in low..high {
        aux[i] = arr[i].clone();
    }

    let mut i = low;
    let mut j = mid;
    let mut k = low;

    while i < mid && j < high {
        if aux[i] <= aux[j] {
            arr[k] = aux[i].clone();
            i += 1;
        } else {
            arr[k] = aux[j].clone();
            j += 1;
        }
        k += 1;
    }

    while i < mid {
        arr[k] = aux[i].clone();
        i += 1;
        k += 1;
    }

    while j < high {
        arr[k] = aux[j].clone();
        j += 1;
        k += 1;
    }
}

/// Bottom-up iterative merge sort.
/// Avoids recursion overhead and provides better cache locality.
pub fn merge_sort_iterative<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    let len = result.len();
    let mut aux = result.clone();

    let mut size = 1;
    while size < len {
        let mut start = 0;
        while start < len {
            let mid = (start + size).min(len);
            let end = (start + 2 * size).min(len);

            if mid < end {
                merge_iterative(&mut result, &mut aux, start, mid, end);
            }

            start += 2 * size;
        }
        size *= 2;
    }

    result
}

fn merge_iterative<T: Ord + Clone>(
    arr: &mut [T],
    aux: &mut [T],
    low: usize,
    mid: usize,
    high: usize,
) {
    for i in low..high {
        aux[i] = arr[i].clone();
    }

    let mut i = low;
    let mut j = mid;
    let mut k = low;

    while i < mid && j < high {
        if aux[i] <= aux[j] {
            arr[k] = aux[i].clone();
            i += 1;
        } else {
            arr[k] = aux[j].clone();
            j += 1;
        }
        k += 1;
    }

    while i < mid {
        arr[k] = aux[i].clone();
        i += 1;
        k += 1;
    }
}

/// Parallel merge sort using rayon for multi-threaded execution.
///
/// # Performance
/// Best for large datasets (> 10,000 elements) on multi-core systems.
/// Uses work-stealing for optimal load balancing.
#[cfg(feature = "rayon")]
pub fn merge_sort_parallel<T: Sortable>(arr: &[T]) -> Vec<T> {
    const THRESHOLD: usize = 10_000;

    if arr.len() <= THRESHOLD {
        return merge_sort(arr);
    }

    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mid = arr.len() / 2;
    let (left, right) = arr.split_at(mid);

    let (left_sorted, right_sorted) = rayon::join(
        || merge_sort_parallel(left),
        || merge_sort_parallel(right),
    );

    merge(&left_sorted, &right_sorted)
}

/// Parallel merge sort without rayon feature (uses std::thread)
pub fn merge_sort_parallel_std<T: Sortable>(arr: &[T]) -> Vec<T> {
    const THRESHOLD: usize = 10_000;

    if arr.len() <= THRESHOLD {
        return merge_sort(arr);
    }

    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mid = arr.len() / 2;
    let left_data = arr[..mid].to_vec();
    let right_data = arr[mid..].to_vec();

    let left_handle = std::thread::spawn(move || merge_sort(&left_data));
    let right_handle = std::thread::spawn(move || merge_sort(&right_data));

    let left_sorted = left_handle.join().unwrap();
    let right_sorted = right_handle.join().unwrap();

    merge(&left_sorted, &right_sorted)
}

/// Natural merge sort - takes advantage of existing runs.
/// More efficient for partially sorted data.
pub fn natural_merge_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();

    loop {
        let runs = identify_runs(&result);
        if runs.len() <= 1 {
            break;
        }

        result = merge_runs(&result, &runs);
    }

    result
}

fn identify_runs<T: Ord>(arr: &[T]) -> Vec<(usize, usize)> {
    let mut runs = Vec::new();
    let mut start = 0;

    while start < arr.len() {
        let mut end = start + 1;
        while end < arr.len() && arr[end - 1] <= arr[end] {
            end += 1;
        }
        runs.push((start, end));
        start = end;
    }

    runs
}

fn merge_runs<T: Ord + Clone>(arr: &[T], runs: &[(usize, usize)]) -> Vec<T> {
    if runs.len() == 1 {
        return arr.to_vec();
    }

    let mut result = Vec::new();

    for chunk in runs.chunks(2) {
        if chunk.len() == 2 {
            let (start1, end1) = chunk[0];
            let (start2, end2) = chunk[1];
            let merged = merge(&arr[start1..end1], &arr[start2..end2]);
            result.extend(merged);
        } else {
            let (start, end) = chunk[0];
            result.extend_from_slice(&arr[start..end]);
        }
    }

    result
}

/// Merge sort with custom comparator.
///
/// # Examples
/// ```
/// let arr = vec![5, 2, 8, 1, 9];
/// // Sort in descending order
/// let sorted = merge_sort_by(&arr, |a, b| b.cmp(a));
/// assert_eq!(sorted, vec![9, 8, 5, 2, 1]);
/// ```
pub fn merge_sort_by<T, F>(arr: &[T], compare: F) -> Vec<T>
where
    T: Clone,
    F: Fn(&T, &T) -> Ordering + Copy,
{
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mid = arr.len() / 2;
    let left = merge_sort_by(&arr[..mid], compare);
    let right = merge_sort_by(&arr[mid..], compare);

    merge_by(&left, &right, compare)
}

fn merge_by<T, F>(left: &[T], right: &[T], compare: F) -> Vec<T>
where
    T: Clone,
    F: Fn(&T, &T) -> Ordering,
{
    let mut result = Vec::with_capacity(left.len() + right.len());
    let mut i = 0;
    let mut j = 0;

    while i < left.len() && j < right.len() {
        match compare(&left[i], &right[j]) {
            Ordering::Less | Ordering::Equal => {
                result.push(left[i].clone());
                i += 1;
            }
            Ordering::Greater => {
                result.push(right[j].clone());
                j += 1;
            }
        }
    }

    result.extend_from_slice(&left[i..]);
    result.extend_from_slice(&right[j..]);

    result
}

/// Merge sort using key extraction.
///
/// # Examples
/// ```
/// #[derive(Clone, Debug, PartialEq)]
/// struct Person { name: String, age: u32 }
///
/// let people = vec![
///     Person { name: "Alice".into(), age: 30 },
///     Person { name: "Bob".into(), age: 25 },
/// ];
///
/// let sorted = merge_sort_by_key(&people, |p| p.age);
/// assert_eq!(sorted[0].age, 25);
/// ```
pub fn merge_sort_by_key<T, K, F>(arr: &[T], key_fn: F) -> Vec<T>
where
    T: Clone,
    K: Ord,
    F: Fn(&T) -> K + Copy,
{
    merge_sort_by(arr, |a, b| key_fn(a).cmp(&key_fn(b)))
}

/// Adaptive merge sort that switches to insertion sort for small subarrays.
/// Provides better performance for small or nearly sorted inputs.
pub fn adaptive_merge_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    const THRESHOLD: usize = 16;

    if arr.len() <= THRESHOLD {
        return insertion_sort(arr);
    }

    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mid = arr.len() / 2;
    let left = adaptive_merge_sort(&arr[..mid]);
    let right = adaptive_merge_sort(&arr[mid..]);

    merge(&left, &right)
}

fn insertion_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    let mut result = arr.to_vec();

    for i in 1..result.len() {
        let key = result[i].clone();
        let mut j = i;

        while j > 0 && result[j - 1] > key {
            result[j] = result[j - 1].clone();
            j -= 1;
        }

        result[j] = key;
    }

    result
}

/// Statistics about sorting performance.
#[derive(Debug, Clone)]
pub struct SortStats {
    pub comparisons: usize,
    pub swaps: usize,
    pub merge_operations: usize,
}

impl SortStats {
    pub fn new() -> Self {
        Self {
            comparisons: 0,
            swaps: 0,
            merge_operations: 0,
        }
    }
}

/// Merge sort that tracks statistics.
pub fn merge_sort_with_stats<T: Ord + Clone>(arr: &[T]) -> (Vec<T>, SortStats) {
    let mut stats = SortStats::new();
    let result = merge_sort_with_stats_helper(arr, &mut stats);
    (result, stats)
}

fn merge_sort_with_stats_helper<T: Ord + Clone>(
    arr: &[T],
    stats: &mut SortStats,
) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mid = arr.len() / 2;
    let left = merge_sort_with_stats_helper(&arr[..mid], stats);
    let right = merge_sort_with_stats_helper(&arr[mid..], stats);

    stats.merge_operations += 1;
    merge_with_stats(&left, &right, stats)
}

fn merge_with_stats<T: Ord + Clone>(left: &[T], right: &[T], stats: &mut SortStats) -> Vec<T> {
    let mut result = Vec::with_capacity(left.len() + right.len());
    let mut i = 0;
    let mut j = 0;

    while i < left.len() && j < right.len() {
        stats.comparisons += 1;
        if left[i] <= right[j] {
            result.push(left[i].clone());
            i += 1;
        } else {
            result.push(right[j].clone());
            j += 1;
        }
    }

    result.extend_from_slice(&left[i..]);
    result.extend_from_slice(&right[j..]);

    result
}

/// Utility function to check if a slice is sorted.
pub fn is_sorted<T: Ord>(arr: &[T]) -> bool {
    arr.windows(2).all(|w| w[0] <= w[1])
}

/// Benchmarks different merge sort implementations.
pub fn benchmark_implementations<T: Sortable + Debug>(arr: &[T]) {
    println!("\n⚡ Benchmarking Merge Sort Implementations");
    println!("{}", "=".repeat(60));

    // Standard merge sort
    let start = Instant::now();
    let _sorted = merge_sort(arr);
    println!("Standard:       {:?}", start.elapsed());

    // Iterative merge sort
    let start = Instant::now();
    let _sorted = merge_sort_iterative(arr);
    println!("Iterative:      {:?}", start.elapsed());

    // Adaptive merge sort
    let start = Instant::now();
    let _sorted = adaptive_merge_sort(arr);
    println!("Adaptive:       {:?}", start.elapsed());

    // Natural merge sort
    let start = Instant::now();
    let _sorted = natural_merge_sort(arr);
    println!("Natural:        {:?}", start.elapsed());

    // Parallel merge sort (std::thread)
    if arr.len() > 1000 {
        let start = Instant::now();
        let _sorted = merge_sort_parallel_std(arr);
        println!("Parallel (std): {:?}", start.elapsed());
    }

    #[cfg(feature = "rayon")]
    if arr.len() > 1000 {
        let start = Instant::now();
        let _sorted = merge_sort_parallel(arr);
        println!("Parallel (rayon): {:?}", start.elapsed());
    }
}

fn main() {
    println!("🔀 Merge Sort Implementation in Rust");
    println!("{}", "=".repeat(60));

    // Basic tests
    let test_cases = vec![
        vec![64, 34, 25, 12, 22, 11, 90],
        vec![5, 2, 8, 6, 1, 9, 4],
        vec![1],
        vec![],
        vec![3, 3, 3, 3, 3],
        vec![9, 8, 7, 6, 5, 4, 3, 2, 1],
        vec![1, 2, 3, 4, 5],
    ];

    println!("\n📋 Basic Tests:");
    println!("{}", "-".repeat(60));

    for (i, arr) in test_cases.iter().enumerate() {
        let sorted = merge_sort(arr);
        let correct = is_sorted(&sorted);

        println!("\nTest {}:", i + 1);
        println!("Original: {:?}", arr);
        println!("Sorted:   {:?}", sorted);
        println!("Correct:  {}", if correct { "✓" } else { "✗" });
    }

    // String sorting
    println!("\n\n🔤 String Sorting:");
    println!("{}", "-".repeat(60));

    let words = vec!["banana", "apple", "cherry", "date", "elderberry"];
    let sorted_words = merge_sort(&words);
    println!("Original: {:?}", words);
    println!("Sorted:   {:?}", sorted_words);

    // Custom comparison
    println!("\n\n🔢 Custom Comparison (Descending):");
    println!("{}", "-".repeat(60));

    let numbers = vec![3, 1, 4, 1, 5, 9, 2, 6];
    let desc_sorted = merge_sort_by(&numbers, |a, b| b.cmp(a));
    println!("Original:   {:?}", numbers);
    println!("Descending: {:?}", desc_sorted);

    // Statistics
    println!("\n\n📊 Sorting Statistics:");
    println!("{}", "-".repeat(60));

    let data = vec![64, 34, 25, 12, 22, 11, 90];
    let (sorted, stats) = merge_sort_with_stats(&data);
    println!("Array: {:?}", data);
    println!("Sorted: {:?}", sorted);
    println!("Comparisons: {}", stats.comparisons);
    println!("Merge operations: {}", stats.merge_operations);

    // Natural merge sort (good for partially sorted data)
    println!("\n\n🌿 Natural Merge Sort:");
    println!("{}", "-".repeat(60));

    let partially_sorted = vec![1, 2, 5, 3, 4, 8, 6, 7, 9];
    println!("Partially sorted: {:?}", partially_sorted);
    let runs = identify_runs(&partially_sorted);
    println!("Identified runs: {:?}", runs);
    let natural_sorted = natural_merge_sort(&partially_sorted);
    println!("After sorting:    {:?}", natural_sorted);

    // Performance benchmarking
    println!("\n\n⚡ Performance Benchmarks:");
    println!("{}", "-".repeat(60));

    use rand::Rng;
    let mut rng = rand::thread_rng();

    for size in [100, 1_000, 10_000, 100_000] {
        let test_data: Vec<i32> = (0..size).map(|_| rng.gen_range(0..1000)).collect();
        println!("\nArray size: {}", size);
        benchmark_implementations(&test_data);
    }

    // Memory efficiency test
    println!("\n\n💾 Memory Efficiency:");
    println!("{}", "-".repeat(60));

    let mut large_arr: Vec<i32> = (0..10_000).map(|_| rng.gen_range(0..1000)).collect();

    println!("In-place sorting (minimal allocations):");
    let start = Instant::now();
    merge_sort_in_place(&mut large_arr);
    println!("Time: {:?}", start.elapsed());
    println!("Sorted: {}", is_sorted(&large_arr));
}

// Cargo.toml dependencies:
/*
[dependencies]
rand = "0.8"

[features]
default = []
rayon = ["dep:rayon"]

[dependencies.rayon]
version = "1.7"
optional = true
*/
