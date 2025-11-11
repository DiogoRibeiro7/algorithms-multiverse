/**
 * Binary Search Algorithm Collection in Rust
 *
 * Comprehensive implementation of binary search variants including:
 * 1. Classic binary search (iterative & recursive)
 * 2. First/last occurrence finding
 * 3. Rotated array search
 * 4. Exponential search
 * 5. Interpolation search
 * 6. Ternary search
 * 7. Binary search on answer (optimization)
 * 8. Advanced utilities
 *
 * Time Complexity: O(log n) for most variants
 * Space Complexity: O(1) iterative, O(log n) recursive
 *
 * Rust Features:
 * - Generic implementations with trait bounds
 * - Zero-cost abstractions
 * - Memory safety without garbage collection
 * - Pattern matching and Result types
 * - Comprehensive error handling
 */

use std::cmp::Ordering;
use std::time::Instant;

// ==============================================================================
// 1. CLASSIC BINARY SEARCH
// ==============================================================================

/// Classic binary search - iterative implementation
///
/// Time Complexity: O(log n)
/// Space Complexity: O(1)
pub fn binary_search_iterative<T: Ord>(arr: &[T], target: &T) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }

    let mut left = 0;
    let mut right = arr.len() - 1;

    while left <= right {
        let mid = left + (right - left) / 2; // Avoid overflow

        match arr[mid].cmp(target) {
            Ordering::Equal => return Some(mid),
            Ordering::Less => left = mid + 1,
            Ordering::Greater => {
                if mid == 0 {
                    break;
                }
                right = mid - 1;
            }
        }
    }

    None
}

/// Classic binary search - recursive implementation
///
/// Time Complexity: O(log n)
/// Space Complexity: O(log n) - recursion stack
pub fn binary_search_recursive<T: Ord>(arr: &[T], target: &T) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }
    binary_search_recursive_helper(arr, target, 0, arr.len() - 1)
}

fn binary_search_recursive_helper<T: Ord>(
    arr: &[T],
    target: &T,
    left: usize,
    right: usize,
) -> Option<usize> {
    if left > right {
        return None;
    }

    let mid = left + (right - left) / 2;

    match arr[mid].cmp(target) {
        Ordering::Equal => Some(mid),
        Ordering::Less => binary_search_recursive_helper(arr, target, mid + 1, right),
        Ordering::Greater => {
            if mid == 0 {
                None
            } else {
                binary_search_recursive_helper(arr, target, left, mid - 1)
            }
        }
    }
}

/// Generic binary search with custom comparator
pub fn binary_search_by<T, F>(arr: &[T], f: F) -> Option<usize>
where
    F: Fn(&T) -> Ordering,
{
    if arr.is_empty() {
        return None;
    }

    let mut left = 0;
    let mut right = arr.len() - 1;

    while left <= right {
        let mid = left + (right - left) / 2;

        match f(&arr[mid]) {
            Ordering::Equal => return Some(mid),
            Ordering::Less => left = mid + 1,
            Ordering::Greater => {
                if mid == 0 {
                    break;
                }
                right = mid - 1;
            }
        }
    }

    None
}

// ==============================================================================
// 2. FIRST/LAST OCCURRENCE
// ==============================================================================

/// Find first (leftmost) occurrence of target
pub fn find_first_occurrence<T: Ord>(arr: &[T], target: &T) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }

    let mut left = 0;
    let mut right = arr.len() - 1;
    let mut result = None;

    while left <= right {
        let mid = left + (right - left) / 2;

        match arr[mid].cmp(target) {
            Ordering::Equal => {
                result = Some(mid);
                if mid == 0 {
                    break;
                }
                right = mid - 1; // Continue searching left
            }
            Ordering::Less => left = mid + 1,
            Ordering::Greater => {
                if mid == 0 {
                    break;
                }
                right = mid - 1;
            }
        }
    }

    result
}

/// Find last (rightmost) occurrence of target
pub fn find_last_occurrence<T: Ord>(arr: &[T], target: &T) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }

    let mut left = 0;
    let mut right = arr.len() - 1;
    let mut result = None;

    while left <= right {
        let mid = left + (right - left) / 2;

        match arr[mid].cmp(target) {
            Ordering::Equal => {
                result = Some(mid);
                left = mid + 1; // Continue searching right
            }
            Ordering::Less => left = mid + 1,
            Ordering::Greater => {
                if mid == 0 {
                    break;
                }
                right = mid - 1;
            }
        }
    }

    result
}

/// Count total occurrences of target
pub fn count_occurrences<T: Ord>(arr: &[T], target: &T) -> usize {
    match find_first_occurrence(arr, target) {
        None => 0,
        Some(first) => {
            let last = find_last_occurrence(arr, target).unwrap();
            last - first + 1
        }
    }
}

/// Find range [start, end] of target
pub fn search_range<T: Ord>(arr: &[T], target: &T) -> Option<(usize, usize)> {
    find_first_occurrence(arr, target).map(|first| {
        let last = find_last_occurrence(arr, target).unwrap();
        (first, last)
    })
}

// ==============================================================================
// 3. ROTATED SORTED ARRAY SEARCH
// ==============================================================================

/// Search in rotated sorted array
pub fn search_rotated_array(arr: &[i32], target: i32) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }

    let mut left = 0;
    let mut right = arr.len() - 1;

    while left <= right {
        let mid = left + (right - left) / 2;

        if arr[mid] == target {
            return Some(mid);
        }

        // Determine which half is sorted
        if arr[left] <= arr[mid] {
            // Left half is sorted
            if arr[left] <= target && target < arr[mid] {
                if mid == 0 {
                    break;
                }
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        } else {
            // Right half is sorted
            if arr[mid] < target && target <= arr[right] {
                left = mid + 1;
            } else {
                if mid == 0 {
                    break;
                }
                right = mid - 1;
            }
        }
    }

    None
}

/// Find rotation point (minimum element)
pub fn find_rotation_point(arr: &[i32]) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }

    let mut left = 0;
    let mut right = arr.len() - 1;

    while left < right {
        let mid = left + (right - left) / 2;

        if arr[mid] > arr[right] {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    Some(left)
}

// ==============================================================================
// 4. EXPONENTIAL SEARCH
// ==============================================================================

/// Exponential search - efficient for unbounded arrays
pub fn exponential_search<T: Ord>(arr: &[T], target: &T) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }

    if &arr[0] == target {
        return Some(0);
    }

    // Find range for binary search
    let mut i = 1;
    while i < arr.len() && &arr[i] <= target {
        i *= 2;
    }

    // Binary search in found range
    let left = i / 2;
    let right = i.min(arr.len() - 1);

    binary_search_recursive_helper(arr, target, left, right)
}

// ==============================================================================
// 5. INTERPOLATION SEARCH
// ==============================================================================

/// Interpolation search - better for uniformly distributed data
///
/// Time Complexity: O(log log n) average, O(n) worst
pub fn interpolation_search(arr: &[i32], target: i32) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }

    let mut left = 0;
    let mut right = arr.len() - 1;

    while left <= right && target >= arr[left] && target <= arr[right] {
        if left == right {
            return if arr[left] == target { Some(left) } else { None };
        }

        // Interpolation formula
        let pos = left
            + ((target - arr[left]) as usize * (right - left))
                / (arr[right] - arr[left]) as usize;

        // Ensure pos is within bounds
        let pos = pos.max(left).min(right);

        match arr[pos].cmp(&target) {
            Ordering::Equal => return Some(pos),
            Ordering::Less => left = pos + 1,
            Ordering::Greater => {
                if pos == 0 {
                    break;
                }
                right = pos - 1;
            }
        }
    }

    None
}

// ==============================================================================
// 6. TERNARY SEARCH
// ==============================================================================

/// Ternary search - divides array into three parts
pub fn ternary_search<T: Ord>(arr: &[T], target: &T) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }

    let mut left = 0;
    let mut right = arr.len() - 1;

    while left <= right {
        let mid1 = left + (right - left) / 3;
        let mid2 = right - (right - left) / 3;

        if &arr[mid1] == target {
            return Some(mid1);
        }
        if &arr[mid2] == target {
            return Some(mid2);
        }

        if target < &arr[mid1] {
            if mid1 == 0 {
                break;
            }
            right = mid1 - 1;
        } else if target > &arr[mid2] {
            left = mid2 + 1;
        } else {
            left = mid1 + 1;
            if mid2 == 0 {
                break;
            }
            right = mid2 - 1;
        }
    }

    None
}

/// Ternary search for finding maximum of unimodal function
pub fn ternary_search_maximum<F>(mut f: F, mut left: f64, mut right: f64, epsilon: f64) -> f64
where
    F: FnMut(f64) -> f64,
{
    while right - left > epsilon {
        let mid1 = left + (right - left) / 3.0;
        let mid2 = right - (right - left) / 3.0;

        if f(mid1) < f(mid2) {
            left = mid1;
        } else {
            right = mid2;
        }
    }

    (left + right) / 2.0
}

// ==============================================================================
// 7. BINARY SEARCH ON ANSWER
// ==============================================================================

/// Binary search on answer space for optimization problems
pub fn binary_search_on_answer<F>(mut predicate: F, mut low: i32, mut high: i32) -> Option<i32>
where
    F: FnMut(i32) -> bool,
{
    let mut result = None;

    while low <= high {
        let mid = low + (high - low) / 2;

        if predicate(mid) {
            result = Some(mid);
            high = mid - 1; // Try to find smaller answer
        } else {
            low = mid + 1;
        }
    }

    result
}

/// Find integer square root using binary search
pub fn integer_square_root(n: i32) -> Option<i32> {
    if n < 0 {
        return None;
    }

    if n == 0 || n == 1 {
        return Some(n);
    }

    let mut left = 0;
    let mut right = n;
    let mut result = 0;

    while left <= right {
        let mid = left + (right - left) / 2;
        let square = (mid as i64) * (mid as i64);

        match square.cmp(&(n as i64)) {
            Ordering::Equal => return Some(mid),
            Ordering::Less => {
                result = mid;
                left = mid + 1;
            }
            Ordering::Greater => right = mid - 1,
        }
    }

    Some(result)
}

/// Find square root with decimal precision
pub fn square_root(n: f64, precision: i32) -> Option<f64> {
    if n < 0.0 {
        return None;
    }

    if n == 0.0 || n == 1.0 {
        return Some(n);
    }

    let mut left = 0.0;
    let mut right = n;
    let epsilon = 10_f64.powi(-precision);

    while right - left > epsilon {
        let mid = left + (right - left) / 2.0;
        let square = mid * mid;

        if (square - n).abs() < epsilon {
            return Some(mid);
        } else if square < n {
            left = mid;
        } else {
            right = mid;
        }
    }

    Some((left + right) / 2.0)
}

// ==============================================================================
// 8. ADVANCED UTILITIES
// ==============================================================================

/// Find insertion position to maintain sorted order
pub fn search_insert_position<T: Ord>(arr: &[T], target: &T) -> usize {
    let mut left = 0;
    let mut right = arr.len();

    while left < right {
        let mid = left + (right - left) / 2;

        if &arr[mid] < target {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    left
}

/// Find element closest to target
pub fn find_closest(arr: &[i32], target: i32) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }

    if arr.len() == 1 {
        return Some(0);
    }

    if target <= arr[0] {
        return Some(0);
    }
    if target >= arr[arr.len() - 1] {
        return Some(arr.len() - 1);
    }

    let mut left = 0;
    let mut right = arr.len() - 1;

    while left < right {
        let mid = left + (right - left) / 2;

        if arr[mid] == target {
            return Some(mid);
        } else if arr[mid] < target {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    if left > 0 && (arr[left - 1] - target).abs() < (arr[left] - target).abs() {
        Some(left - 1)
    } else {
        Some(left)
    }
}

/// Find peak element (element greater than neighbors)
pub fn find_peak_element(arr: &[i32]) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }

    if arr.len() == 1 {
        return Some(0);
    }

    let mut left = 0;
    let mut right = arr.len() - 1;

    while left < right {
        let mid = left + (right - left) / 2;

        if arr[mid] < arr[mid + 1] {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    Some(left)
}

// ==============================================================================
// DEMONSTRATION AND TESTING
// ==============================================================================

fn main() {
    println!("======================================================================");
    println!("BINARY SEARCH ALGORITHM COLLECTION - RUST");
    println!("======================================================================");

    demonstrate_classic_binary_search();
    demonstrate_first_last_occurrence();
    demonstrate_rotated_array_search();
    demonstrate_exponential_search();
    demonstrate_interpolation_search();
    demonstrate_ternary_search();
    demonstrate_binary_search_on_answer();
    demonstrate_advanced_utilities();
    run_performance_tests();

    println!("\n======================================================================");
    println!("DEMONSTRATION COMPLETE");
    println!("======================================================================");
}

fn demonstrate_classic_binary_search() {
    println!("\n1. CLASSIC BINARY SEARCH");
    println!("--------------------------------------------------");

    let arr = vec![1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
    let targets = vec![7, 10, 1, 19];

    for &target in &targets {
        let idx_iter = binary_search_iterative(&arr, &target);
        let idx_rec = binary_search_recursive(&arr, &target);
        println!(
            "Search {:2}: Iterative={:?}, Recursive={:?}",
            target, idx_iter, idx_rec
        );
    }
}

fn demonstrate_first_last_occurrence() {
    println!("\n2. FIRST/LAST OCCURRENCE");
    println!("--------------------------------------------------");

    let arr = vec![1, 2, 2, 2, 3, 4, 4, 4, 4, 5];
    let targets = vec![2, 4, 6];

    for &target in &targets {
        let first = find_first_occurrence(&arr, &target);
        let last = find_last_occurrence(&arr, &target);
        let count = count_occurrences(&arr, &target);
        println!(
            "Target {}: First={:?}, Last={:?}, Count={}",
            target, first, last, count
        );
    }
}

fn demonstrate_rotated_array_search() {
    println!("\n3. ROTATED ARRAY SEARCH");
    println!("--------------------------------------------------");

    let rotated = vec![4, 5, 6, 7, 0, 1, 2];
    let rotation_point = find_rotation_point(&rotated).unwrap();

    println!("Rotated array: {:?}", rotated);
    println!(
        "Rotation point: {} (value: {})",
        rotation_point, rotated[rotation_point]
    );

    let targets = vec![0, 3, 6];
    for &target in &targets {
        let idx = search_rotated_array(&rotated, target);
        println!("Search {}: Index={:?}", target, idx);
    }
}

fn demonstrate_exponential_search() {
    println!("\n4. EXPONENTIAL SEARCH");
    println!("--------------------------------------------------");

    let large_arr: Vec<i32> = (0..50).map(|i| i * 2 + 1).collect();
    let targets = vec![15, 51, 99];

    for &target in &targets {
        let idx = exponential_search(&large_arr, &target);
        println!("Search {:2} in array of size 50: Index={:?}", target, idx);
    }
}

fn demonstrate_interpolation_search() {
    println!("\n5. INTERPOLATION SEARCH");
    println!("--------------------------------------------------");

    let uniform_arr = vec![10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
    let targets = vec![30, 75, 100];

    for &target in &targets {
        let idx = interpolation_search(&uniform_arr, target);
        println!("Search {:3}: Index={:?}", target, idx);
    }
}

fn demonstrate_ternary_search() {
    println!("\n6. TERNARY SEARCH");
    println!("--------------------------------------------------");

    let arr = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let targets = vec![5, 1, 10, 11];

    for &target in &targets {
        let idx = ternary_search(&arr, &target);
        println!("Search {:2}: Index={:?}", target, idx);
    }

    // Unimodal function
    let func = |x: f64| -(x - 5.0) * (x - 5.0) + 25.0;
    let max_x = ternary_search_maximum(func, 0.0, 10.0, 1e-9);
    println!("Maximum of -(x-5)² + 25 at x ≈ {:.6}", max_x);
}

fn demonstrate_binary_search_on_answer() {
    println!("\n7. BINARY SEARCH ON ANSWER");
    println!("--------------------------------------------------");

    let test_numbers = vec![16, 25, 50, 100];
    for &n in &test_numbers {
        let sqrt_int = integer_square_root(n).unwrap();
        let sqrt_precise = square_root(n as f64, 2).unwrap();
        println!("√{:3} = {} (integer), {:.2} (precise)", n, sqrt_int, sqrt_precise);
    }
}

fn demonstrate_advanced_utilities() {
    println!("\n8. ADVANCED UTILITIES");
    println!("--------------------------------------------------");

    let arr = vec![1, 3, 5, 6, 8, 10];
    let targets = vec![2, 5, 11];

    for &target in &targets {
        let pos = search_insert_position(&arr, &target);
        println!("Insert position for {:2}: {}", target, pos);
    }

    let arr_closest = vec![1, 3, 5, 7, 9];
    let targets_closest = vec![4, 6, 8];

    for &target in &targets_closest {
        let idx = find_closest(&arr_closest, target).unwrap();
        println!(
            "Closest to {}: Index={}, Value={}",
            target, idx, arr_closest[idx]
        );
    }

    let peak_arr = vec![1, 3, 20, 4, 1, 0];
    let peak = find_peak_element(&peak_arr).unwrap();
    println!(
        "Peak element in {:?}: Index={}, Value={}",
        peak_arr, peak, peak_arr[peak]
    );
}

fn run_performance_tests() {
    println!("\n======================================================================");
    println!("PERFORMANCE BENCHMARKS");
    println!("======================================================================");

    let sizes = vec![1000, 10000, 100000];

    for &size in &sizes {
        println!("\nArray size: {}", size);
        println!("--------------------------------------------------");

        let arr: Vec<i32> = (0..size).map(|i| i * 2).collect();
        let targets: Vec<i32> = (0..100).map(|i| (i * size / 100) * 2).collect();

        let start = Instant::now();
        for &target in &targets {
            binary_search_iterative(&arr, &target);
        }
        let time_binary_iter = start.elapsed();

        let start = Instant::now();
        for &target in &targets {
            binary_search_recursive(&arr, &target);
        }
        let time_binary_rec = start.elapsed();

        let start = Instant::now();
        for &target in &targets {
            exponential_search(&arr, &target);
        }
        let time_exponential = start.elapsed();

        let start = Instant::now();
        for &target in &targets {
            interpolation_search(&arr, target);
        }
        let time_interpolation = start.elapsed();

        let start = Instant::now();
        for &target in &targets {
            ternary_search(&arr, &target);
        }
        let time_ternary = start.elapsed();

        println!("Binary (Iterative):    {:8.3} ms", time_binary_iter.as_secs_f64() * 1000.0);
        println!("Binary (Recursive):    {:8.3} ms", time_binary_rec.as_secs_f64() * 1000.0);
        println!("Exponential Search:    {:8.3} ms", time_exponential.as_secs_f64() * 1000.0);
        println!("Interpolation Search:  {:8.3} ms", time_interpolation.as_secs_f64() * 1000.0);
        println!("Ternary Search:        {:8.3} ms", time_ternary.as_secs_f64() * 1000.0);
    }
}
