// Quick Sort Implementation in Rust
//
// Time Complexity:
// - Best/Average: O(n log n)
// - Worst: O(n²)
// Space Complexity: O(log n) - due to recursion stack
//
// Quick Sort is a divide-and-conquer algorithm that works by selecting a 'pivot'
// element and partitioning other elements into two sub-arrays according to whether
// they are less than or greater than the pivot.

use std::time::Instant;
use rand::Rng;

/// Sorts a vector using the QuickSort algorithm.
/// Returns a new sorted vector.
pub fn quick_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }
    
    let mut result = arr.to_vec();
    quick_sort_in_place(&mut result, 0, result.len() - 1);
    result
}

/// In-place QuickSort implementation for better space efficiency.
pub fn quick_sort_in_place<T: Ord>(arr: &mut [T], low: usize, high: usize) {
    if low < high {
        let pivot_index = partition(arr, low, high);
        if pivot_index > 0 {
            quick_sort_in_place(arr, low, pivot_index - 1);
        }
        quick_sort_in_place(arr, pivot_index + 1, high);
    }
}

/// Partitions the slice around a pivot element.
/// Returns the final position of the pivot.
fn partition<T: Ord>(arr: &mut [T], low: usize, high: usize) -> usize {
    let mut i = low;
    
    for j in low..high {
        if arr[j] <= arr[high] {
            arr.swap(i, j);
            i += 1;
        }
    }
    
    arr.swap(i, high);
    i
}

/// Iterative implementation of QuickSort to avoid recursion overhead.
pub fn quick_sort_iterative<T: Ord>(arr: &mut [T]) {
    if arr.len() <= 1 {
        return;
    }
    
    let mut stack = Vec::new();
    stack.push((0, arr.len() - 1));
    
    while let Some((low, high)) = stack.pop() {
        if low < high {
            let pivot_index = partition(arr, low, high);
            if pivot_index > 0 {
                stack.push((low, pivot_index - 1));
            }
            stack.push((pivot_index + 1, high));
        }
    }
}

/// QuickSort with random pivot selection for better average performance.
pub fn randomized_quick_sort<T: Ord>(arr: &mut [T], low: usize, high: usize) {
    if low < high {
        // Random pivot selection
        let mut rng = rand::thread_rng();
        let random_index = rng.gen_range(low..=high);
        arr.swap(random_index, high);
        
        let pivot_index = partition(arr, low, high);
        if pivot_index > 0 {
            randomized_quick_sort(arr, low, pivot_index - 1);
        }
        randomized_quick_sort(arr, pivot_index + 1, high);
    }
}

/// Three-way partitioning QuickSort for slices with many duplicate elements.
pub fn quick_sort_3way<T: Ord + Clone>(arr: &mut [T], low: usize, high: usize) {
    if low >= high {
        return;
    }
    
    let pivot = arr[low].clone();
    let mut lt = low;
    let mut gt = high;
    let mut i = low;
    
    while i <= gt {
        if arr[i] < pivot {
            arr.swap(lt, i);
            lt += 1;
            i += 1;
        } else if arr[i] > pivot {
            arr.swap(i, gt);
            if gt > 0 {
                gt -= 1;
            }
        } else {
            i += 1;
        }
    }
    
    if lt > 0 {
        quick_sort_3way(arr, low, lt - 1);
    }
    quick_sort_3way(arr, gt + 1, high);
}

/// Functional-style QuickSort implementation.
pub fn quick_sort_functional<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }
    
    let pivot = &arr[arr.len() / 2];
    let less: Vec<T> = arr.iter().filter(|&x| x < pivot).cloned().collect();
    let equal: Vec<T> = arr.iter().filter(|&x| x == pivot).cloned().collect();
    let greater: Vec<T> = arr.iter().filter(|&x| x > pivot).cloned().collect();
    
    [
        quick_sort_functional(&less),
        equal,
        quick_sort_functional(&greater),
    ]
    .concat()
}

/// Generic QuickSort with custom comparison function.
pub fn quick_sort_by<T, F>(arr: &mut [T], compare: F)
where
    F: Fn(&T, &T) -> std::cmp::Ordering,
{
    if arr.len() <= 1 {
        return;
    }
    quick_sort_by_helper(arr, 0, arr.len() - 1, &compare);
}

fn quick_sort_by_helper<T, F>(arr: &mut [T], low: usize, high: usize, compare: &F)
where
    F: Fn(&T, &T) -> std::cmp::Ordering,
{
    if low < high {
        let pivot_index = partition_by(arr, low, high, compare);
        if pivot_index > 0 {
            quick_sort_by_helper(arr, low, pivot_index - 1, compare);
        }
        quick_sort_by_helper(arr, pivot_index + 1, high, compare);
    }
}

fn partition_by<T, F>(arr: &mut [T], low: usize, high: usize, compare: &F) -> usize
where
    F: Fn(&T, &T) -> std::cmp::Ordering,
{
    let mut i = low;
    
    for j in low..high {
        if compare(&arr[j], &arr[high]) != std::cmp::Ordering::Greater {
            arr.swap(i, j);
            i += 1;
        }
    }
    
    arr.swap(i, high);
    i
}

/// Utility function to print a slice with a label.
fn print_slice<T: std::fmt::Debug>(arr: &[T], label: &str) {
    println!("{}: {:?}", label, arr);
}

/// Test function to verify the correctness of QuickSort implementations.
fn run_tests() {
    let test_arrays = vec![
        vec![64, 34, 25, 12, 22, 11, 90],
        vec![5, 2, 8, 6, 1, 9, 4],
        vec![1],
        vec![],
        vec![3, 3, 3, 3],
        vec![9, 8, 7, 6, 5, 4, 3, 2, 1],
    ];
    
    println!("QuickSort Implementation Tests");
    println!("{}", "=".repeat(40));
    
    for (i, arr) in test_arrays.iter().enumerate() {
        let original = arr.clone();
        let sorted = quick_sort(arr);
        let mut expected = original.clone();
        expected.sort();
        
        println!("Test {}:", i + 1);
        print_slice(&original, "Original");
        print_slice(&sorted, "Sorted  ");
        println!("Correct: {}", sorted == expected);
        println!("{}", "-".repeat(30));
    }
    
    // Performance test
    let mut rng = rand::thread_rng();
    let large_array: Vec<i32> = (0..100_000).map(|_| rng.gen_range(1..1000)).collect();
    
    let start = Instant::now();
    let _ = quick_sort(&large_array);
    let duration = start.elapsed();
    
    println!("\nPerformance Test (100,000 elements): {:?}", duration);
}

/// Demonstrate different QuickSort variants.
fn demonstrate_variants() {
    println!("\nDemonstrating QuickSort Variants:");
    println!("{}", "=".repeat(40));
    
    let test_array = vec![64, 34, 25, 12, 22, 11, 90];
    
    // Standard QuickSort
    let sorted1 = quick_sort(&test_array);
    println!("Standard QuickSort:");
    print_slice(&test_array, "Original");
    print_slice(&sorted1, "Sorted  ");
    
    // Functional QuickSort
    let sorted2 = quick_sort_functional(&test_array);
    println!("\nFunctional QuickSort:");
    print_slice(&test_array, "Original");
    print_slice(&sorted2, "Sorted  ");
    
    // Iterative QuickSort
    let mut arr3 = test_array.clone();
    quick_sort_iterative(&mut arr3);
    println!("\nIterative QuickSort:");
    print_slice(&test_array, "Original");
    print_slice(&arr3, "Sorted  ");
    
    // Custom comparison QuickSort
    let mut arr4 = test_array.clone();
    quick_sort_by(&mut arr4, |a, b| b.cmp(a)); // Reverse order
    println!("\nReverse Order QuickSort:");
    print_slice(&test_array, "Original");
    print_slice(&arr4, "Sorted  ");
}

/// Benchmark function for performance testing.
fn benchmark_quick_sort<T: Ord + Clone>(arr: &[T]) -> std::time::Duration {
    let start = Instant::now();
    let _ = quick_sort(arr);
    start.elapsed()
}

fn main() {
    run_tests();
    demonstrate_variants();
    
    // Additional benchmarking
    println!("\nBenchmarking different implementations:");
    let mut rng = rand::thread_rng();
    let test_data: Vec<i32> = (0..10_000).map(|_| rng.gen_range(1..1000)).collect();
    
    // Benchmark functional implementation
    let start = Instant::now();
    let _ = quick_sort_functional(&test_data);
    println!("Functional QuickSort: {:?}", start.elapsed());
    
    // Benchmark iterative implementation
    let mut test_data_iter = test_data.clone();
    let start = Instant::now();
    quick_sort_iterative(&mut test_data_iter);
    println!("Iterative QuickSort: {:?}", start.elapsed());
    
    // Benchmark 3-way implementation
    let mut test_data_3way = test_data.clone();
    let start = Instant::now();
    quick_sort_3way(&mut test_data_3way, 0, test_data_3way.len() - 1);
    println!("3-Way QuickSort: {:?}", start.elapsed());
}

// Cargo.toml would include:
/*
[dependencies]
rand = "0.8"
*/
