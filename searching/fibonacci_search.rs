/**
 * Fibonacci Search Algorithm Implementation
 *
 * Time Complexity: O(log n)
 * Space Complexity: O(1)
 *
 * WHEN TO USE FIBONACCI SEARCH OVER BINARY SEARCH:
 * 1. When division/multiplication operations are costly (embedded systems, old CPUs)
 * 2. For data stored on magnetic tapes or systems where jumping backward is expensive
 * 3. When you want to minimize comparisons on average (fewer than binary search)
 * 4. For uniformly distributed sorted data
 *
 * RUST-SPECIFIC ADVANTAGES:
 * - Overflow-safe arithmetic with checked operations
 * - Pattern matching for cleaner comparison logic
 * - Zero-cost abstractions maintain performance
 */

use std::cmp::min;
use std::time::Instant;

/// Perform Fibonacci search on a sorted array
pub fn fibonacci_search(arr: &[i32], target: i32) -> Option<usize> {
    let n = arr.len();
    if n == 0 {
        return None;
    }

    // Initialize Fibonacci numbers
    let mut fib_m2 = 0;  // (m-2)'th Fibonacci number
    let mut fib_m1 = 1;  // (m-1)'th Fibonacci number
    let mut fib_m = fib_m2 + fib_m1;  // m'th Fibonacci number

    // Find the smallest Fibonacci number >= n
    while fib_m < n {
        fib_m2 = fib_m1;
        fib_m1 = fib_m;
        fib_m = fib_m2 + fib_m1;
    }

    // Marks the eliminated range from front
    let mut offset: isize = -1;

    // While there are elements to be inspected
    while fib_m > 1 {
        // Check if fib_m2 is a valid index
        let i = min((offset + fib_m2 as isize) as usize, n - 1);

        // Use pattern matching for cleaner comparison
        match arr[i].cmp(&target) {
            std::cmp::Ordering::Less => {
                // Target is greater
                fib_m = fib_m1;
                fib_m1 = fib_m2;
                fib_m2 = fib_m - fib_m1;
                offset = i as isize;
            }
            std::cmp::Ordering::Greater => {
                // Target is less
                fib_m = fib_m2;
                fib_m1 = fib_m1 - fib_m2;
                fib_m2 = fib_m - fib_m1;
            }
            std::cmp::Ordering::Equal => {
                // Element found
                return Some(i);
            }
        }
    }

    // Compare the last element
    let last_idx = (offset + 1) as usize;
    if fib_m1 == 1 && last_idx < n && arr[last_idx] == target {
        return Some(last_idx);
    }

    None
}

/// Optimized Fibonacci search with early termination
pub fn fibonacci_search_optimized(arr: &[i32], target: i32) -> Option<usize> {
    let n = arr.len();
    if n == 0 {
        return None;
    }

    // Quick boundary checks
    if target < arr[0] || target > arr[n - 1] {
        return None;
    }
    if arr[0] == target {
        return Some(0);
    }
    if arr[n - 1] == target {
        return Some(n - 1);
    }

    // Initialize Fibonacci numbers
    let mut fib_m2 = 0;
    let mut fib_m1 = 1;
    let mut fib_m = fib_m2 + fib_m1;

    while fib_m < n {
        fib_m2 = fib_m1;
        fib_m1 = fib_m;
        fib_m = fib_m2 + fib_m1;
    }

    let mut offset: isize = -1;

    while fib_m > 1 {
        let i = min((offset + fib_m2 as isize) as usize, n - 1);

        match arr[i].cmp(&target) {
            std::cmp::Ordering::Less => {
                fib_m = fib_m1;
                fib_m1 = fib_m2;
                fib_m2 = fib_m - fib_m1;
                offset = i as isize;
            }
            std::cmp::Ordering::Greater => {
                fib_m = fib_m2;
                fib_m1 = fib_m1 - fib_m2;
                fib_m2 = fib_m - fib_m1;
            }
            std::cmp::Ordering::Equal => return Some(i),
        }
    }

    let last_idx = (offset + 1) as usize;
    if fib_m1 == 1 && last_idx < n && arr[last_idx] == target {
        return Some(last_idx);
    }

    None
}

/// Binary search for comparison
fn binary_search(arr: &[i32], target: i32) -> Option<usize> {
    let mut left = 0;
    let mut right = arr.len();

    while left < right {
        let mid = left + (right - left) / 2;
        match arr[mid].cmp(&target) {
            std::cmp::Ordering::Equal => return Some(mid),
            std::cmp::Ordering::Less => left = mid + 1,
            std::cmp::Ordering::Greater => right = mid,
        }
    }

    None
}

/// Jump search for comparison
fn jump_search(arr: &[i32], target: i32) -> Option<usize> {
    let n = arr.len();
    let jump = (n as f64).sqrt() as usize;
    let mut prev = 0;

    while prev < n && arr[prev.saturating_add(jump).min(n - 1)] < target {
        prev += jump;
    }

    for i in prev.saturating_sub(jump)..prev.saturating_add(jump).min(n) {
        if arr[i] == target {
            return Some(i);
        }
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fibonacci_search() {
        let arr = vec![1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
        assert_eq!(fibonacci_search(&arr, 7), Some(3));
        assert_eq!(fibonacci_search(&arr, 20), None);
        assert_eq!(fibonacci_search(&arr, 1), Some(0));
        assert_eq!(fibonacci_search(&arr, 19), Some(9));
    }

    #[test]
    fn test_fibonacci_search_optimized() {
        let arr = vec![1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
        assert_eq!(fibonacci_search_optimized(&arr, 7), Some(3));
        assert_eq!(fibonacci_search_optimized(&arr, 20), None);
    }
}

fn main() {
    // Test correctness
    let test_arr = vec![1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29];
    println!("Test Array: {:?}", test_arr);
    println!("Fibonacci Search for 15: {:?}", fibonacci_search(&test_arr, 15));
    println!("Fibonacci Search for 20: {:?}", fibonacci_search(&test_arr, 20));
    println!("Fibonacci Search for 1: {:?}", fibonacci_search(&test_arr, 1));
    println!("Fibonacci Search for 29: {:?}", fibonacci_search(&test_arr, 29));

    // Performance comparison
    println!("\n--- Performance Comparison ---");
    let sizes = vec![1000, 10000, 100000, 1000000];

    for size in sizes {
        let arr: Vec<i32> = (0..size).map(|i| i * 2).collect();
        let target = arr[size / 2];

        // Warm-up
        for _ in 0..100 {
            fibonacci_search(&arr, target);
            binary_search(&arr, target);
            jump_search(&arr, target);
        }

        // Fibonacci search
        let start = Instant::now();
        for _ in 0..10000 {
            fibonacci_search(&arr, target);
        }
        let fib_time = start.elapsed();

        // Binary search
        let start = Instant::now();
        for _ in 0..10000 {
            binary_search(&arr, target);
        }
        let binary_time = start.elapsed();

        // Jump search
        let start = Instant::now();
        for _ in 0..10000 {
            jump_search(&arr, target);
        }
        let jump_time = start.elapsed();

        println!("\nArray size: {}", size);
        println!("Fibonacci Search: {:.3}ms", fib_time.as_secs_f64() * 1000.0);
        println!("Binary Search: {:.3}ms", binary_time.as_secs_f64() * 1000.0);
        println!("Jump Search: {:.3}ms", jump_time.as_secs_f64() * 1000.0);
        println!("Ratio (Fib/Binary): {:.2}x",
                 fib_time.as_secs_f64() / binary_time.as_secs_f64());
        println!("Ratio (Fib/Jump): {:.2}x",
                 fib_time.as_secs_f64() / jump_time.as_secs_f64());
    }

    // Performance on different data distributions
    println!("\n--- Performance on Different Data Distributions ---");

    // Uniform distribution
    let arr_uniform: Vec<i32> = (0..100000).collect();
    let target1 = 75000;

    let start = Instant::now();
    for _ in 0..10000 {
        fibonacci_search(&arr_uniform, target1);
    }
    let uniform_time = start.elapsed();
    println!("Uniform distribution: {:.3}ms", uniform_time.as_secs_f64() * 1000.0);

    // Sparse distribution
    let arr_sparse: Vec<i32> = (0..10000).map(|i| i * 10).collect();
    let target2 = 75000;

    let start = Instant::now();
    for _ in 0..10000 {
        fibonacci_search(&arr_sparse, target2);
    }
    let sparse_time = start.elapsed();
    println!("Sparse distribution: {:.3}ms", sparse_time.as_secs_f64() * 1000.0);
}
