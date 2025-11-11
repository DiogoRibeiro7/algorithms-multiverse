/**
 * Jump Search Algorithm Implementation
 *
 * Time Complexity: O(√n)
 * Space Complexity: O(1)
 *
 * WHEN TO USE JUMP SEARCH OVER BINARY SEARCH:
 * 1. When backward jumping is costly (e.g., tape storage, linked lists with forward pointers)
 * 2. When data is in a system where jumping is cheaper than repeated divisions
 * 3. As a middle ground between linear search O(n) and binary search O(log n)
 * 4. When you need predictable jump patterns for cache optimization
 *
 * PERFORMANCE CHARACTERISTICS:
 * - Optimal block size: √n (square root of array length)
 * - Better cache performance than binary search in some cases (sequential jumps)
 * - Fewer comparisons than linear search, more than binary search
 * - Good for uniformly distributed data on sequential storage
 *
 * RUST-SPECIFIC OPTIMIZATIONS:
 * - Zero-cost abstractions with iterator chains
 * - Bounds checking eliminated by compiler in release mode
 * - Excellent cache locality with slice operations
 * - SIMD auto-vectorization opportunities in linear search phase
 */

use std::cmp::min;
use std::time::Instant;

/// Perform jump search on a sorted array
pub fn jump_search(arr: &[i32], target: i32) -> Option<usize> {
    let n = arr.len();
    if n == 0 {
        return None;
    }

    // Calculate optimal jump size: √n
    let jump = (n as f64).sqrt() as usize;
    let mut prev = 0;
    let mut curr = jump;

    // Jump through blocks until we find a block that might contain target
    while curr < n && arr[curr] < target {
        prev = curr;
        curr += jump;
    }

    // Linear search within the identified block
    let end = min(curr + 1, n);
    for i in prev..end {
        if arr[i] == target {
            return Some(i);
        } else if arr[i] > target {
            return None;
        }
    }

    None
}

/// Jump search with customizable block size for cache optimization
pub fn jump_search_optimized(arr: &[i32], target: i32, block_size: Option<usize>) -> Option<usize> {
    let n = arr.len();
    if n == 0 {
        return None;
    }

    // Use custom block size or default to √n
    let jump = block_size.unwrap_or_else(|| (n as f64).sqrt() as usize).max(1);
    let mut prev = 0;
    let mut curr = jump;

    // Jump through blocks
    while curr < n && arr[curr] < target {
        prev = curr;
        curr += jump;
    }

    // Linear search in the block
    let end = min(curr + 1, n);
    for i in prev..end {
        if arr[i] == target {
            return Some(i);
        } else if arr[i] > target {
            return None;
        }
    }

    None
}

/// Adaptive jump search that adjusts block size based on data distribution
pub fn adaptive_jump_search(arr: &[i32], target: i32) -> Option<usize> {
    let n = arr.len();
    if n == 0 {
        return None;
    }

    let initial_jump = (n as f64).sqrt() as usize;
    let mut jump = initial_jump;
    let mut prev = 0;

    // Adaptive jumping: adjust jump size based on value differences
    while prev < n && arr[min(prev + jump, n - 1)] < target {
        let next_idx = min(prev + jump, n - 1);

        // If we're getting close to target, reduce jump size
        if next_idx < n - 1 {
            let value_range = (arr[next_idx] - arr[prev]) as i64;
            let target_range = (target - arr[prev]) as i64;

            // Estimate where target might be and adjust jump
            if value_range > 0 {
                let estimated_position = (target_range as f64 / value_range as f64) * jump as f64;
                jump = ((estimated_position * 1.5) as usize).max(1);
            }
        }

        prev = next_idx;
        if prev >= n - 1 {
            break;
        }
    }

    // Linear search in the final block
    let start = prev.saturating_sub(initial_jump);
    let end = min(prev + initial_jump, n);

    for i in start..end {
        if arr[i] == target {
            return Some(i);
        } else if arr[i] > target {
            return None;
        }
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_jump_search() {
        let arr = vec![1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
        assert_eq!(jump_search(&arr, 7), Some(3));
        assert_eq!(jump_search(&arr, 20), None);
        assert_eq!(jump_search(&arr, 1), Some(0));
        assert_eq!(jump_search(&arr, 19), Some(9));
    }

    #[test]
    fn test_adaptive_jump_search() {
        let arr = vec![1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
        assert_eq!(adaptive_jump_search(&arr, 7), Some(3));
        assert_eq!(adaptive_jump_search(&arr, 20), None);
    }
}

fn main() {
    // Test correctness
    let test_arr = vec![1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29];
    println!("Test Array: {:?}", test_arr);
    println!("Jump Search for 15: {:?}", jump_search(&test_arr, 15));
    println!("Jump Search for 20: {:?}", jump_search(&test_arr, 20));
    println!("Jump Search for 1: {:?}", jump_search(&test_arr, 1));
    println!("Jump Search for 29: {:?}", jump_search(&test_arr, 29));

    // Performance comparison
    println!("\n--- Performance Comparison ---");
    let sizes = vec![1000, 10000, 100000, 1000000];

    for size in sizes {
        let arr: Vec<i32> = (0..size).map(|i| i * 2).collect();
        let target = arr[size / 2];

        // Warm-up
        for _ in 0..100 {
            jump_search(&arr, target);
            binary_search(&arr, target);
        }

        // Jump search
        let start = Instant::now();
        for _ in 0..10000 {
            jump_search(&arr, target);
        }
        let jump_time = start.elapsed();

        // Binary search
        let start = Instant::now();
        for _ in 0..10000 {
            binary_search(&arr, target);
        }
        let binary_time = start.elapsed();

        println!("\nArray size: {}", size);
        println!("Jump Search: {:.3}ms", jump_time.as_secs_f64() * 1000.0);
        println!("Binary Search: {:.3}ms", binary_time.as_secs_f64() * 1000.0);
        println!("Ratio (Jump/Binary): {:.2}x",
                 jump_time.as_secs_f64() / binary_time.as_secs_f64());
    }

    // Cache-friendly block size analysis
    println!("\n--- Cache-Friendly Block Size Analysis ---");
    let large_arr: Vec<i32> = (0..100000).map(|i| i * 2).collect();
    let target = large_arr[50000];

    let block_sizes = vec![32, 64, 128, 256, 512, 1024,
                           (large_arr.len() as f64).sqrt() as usize];

    for block_size in block_sizes {
        // Warm-up
        for _ in 0..100 {
            jump_search_optimized(&large_arr, target, Some(block_size));
        }

        let start = Instant::now();
        for _ in 0..10000 {
            jump_search_optimized(&large_arr, target, Some(block_size));
        }
        let elapsed = start.elapsed();

        println!("Block size {:5}: {:.3}ms",
                 block_size, elapsed.as_secs_f64() * 1000.0);
    }
}
