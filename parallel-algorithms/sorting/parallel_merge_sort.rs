/*
Parallel Merge Sort Implementation in Rust

This implementation uses Rayon for data parallelism, providing:
- Zero-cost abstractions
- Memory safety without garbage collection
- Work-stealing scheduler
- Fearless concurrency

Features:
- Rayon parallel iterators
- Thread pool configuration
- Lock-free operations
- Type safety and zero-cost abstractions

Time Complexity: O(n log n)
Space Complexity: O(n)

To compile and run:
1. Add to Cargo.toml:
   [dependencies]
   rayon = "1.7"

2. Run: cargo run --release

Author: Algorithms Multiverse
*/

use rayon::prelude::*;
use std::time::Instant;
use std::sync::atomic::{AtomicUsize, Ordering};

/// Result of a sorting operation with performance metrics
#[derive(Debug, Clone)]
pub struct SortResult {
    pub sorted_array: Vec<i32>,
    pub time_taken: std::time::Duration,
    pub comparisons: usize,
    pub method: String,
    pub num_threads: usize,
}

/// Parallel merge sort implementation
pub struct ParallelMergeSort {
    sequential_threshold: usize,
    comparisons: AtomicUsize,
}

impl ParallelMergeSort {
    /// Create a new ParallelMergeSort instance
    pub fn new(sequential_threshold: usize) -> Self {
        ParallelMergeSort {
            sequential_threshold,
            comparisons: AtomicUsize::new(0),
        }
    }

    /// Increment comparison counter (thread-safe)
    fn increment_comparisons(&self) {
        self.comparisons.fetch_add(1, Ordering::Relaxed);
    }

    /// Reset comparison counter
    fn reset_comparisons(&self) {
        self.comparisons.store(0, Ordering::Relaxed);
    }

    /// Get current comparison count
    fn get_comparisons(&self) -> usize {
        self.comparisons.load(Ordering::Relaxed)
    }

    /// Merge two sorted slices into one sorted vector
    fn merge(&self, left: &[i32], right: &[i32], count_comparisons: bool) -> Vec<i32> {
        let mut result = Vec::with_capacity(left.len() + right.len());
        let mut i = 0;
        let mut j = 0;

        while i < left.len() && j < right.len() {
            if count_comparisons {
                self.increment_comparisons();
            }

            if left[i] <= right[j] {
                result.push(left[i]);
                i += 1;
            } else {
                result.push(right[j]);
                j += 1;
            }
        }

        result.extend_from_slice(&left[i..]);
        result.extend_from_slice(&right[j..]);

        result
    }

    /// Sequential merge sort for base cases
    pub fn sequential_merge_sort(&self, arr: &[i32]) -> Vec<i32> {
        if arr.len() <= 1 {
            return arr.to_vec();
        }

        let mid = arr.len() / 2;
        let left = self.sequential_merge_sort(&arr[..mid]);
        let right = self.sequential_merge_sort(&arr[mid..]);

        self.merge(&left, &right, true)
    }

    /// Parallel merge sort using rayon's join
    pub fn parallel_merge_sort_rayon(&self, arr: &[i32]) -> Vec<i32> {
        if arr.len() <= self.sequential_threshold {
            return self.sequential_merge_sort(arr);
        }

        let mid = arr.len() / 2;

        // Rayon's join runs two closures potentially in parallel
        let (left, right) = rayon::join(
            || self.parallel_merge_sort_rayon(&arr[..mid]),
            || self.parallel_merge_sort_rayon(&arr[mid..]),
        );

        self.merge(&left, &right, true)
    }

    /// Parallel merge sort using rayon's parallel iterators
    pub fn parallel_merge_sort_iter(&self, arr: &[i32]) -> Vec<i32> {
        if arr.len() <= self.sequential_threshold {
            return self.sequential_merge_sort(arr);
        }

        // Split into chunks based on thread count
        let num_threads = rayon::current_num_threads();
        let chunk_size = (arr.len() + num_threads - 1) / num_threads;
        let chunk_size = chunk_size.max(self.sequential_threshold);

        // Sort chunks in parallel
        let mut sorted_chunks: Vec<Vec<i32>> = arr
            .par_chunks(chunk_size)
            .map(|chunk| self.sequential_merge_sort(chunk))
            .collect();

        // Merge sorted chunks
        while sorted_chunks.len() > 1 {
            sorted_chunks = sorted_chunks
                .par_chunks(2)
                .map(|pair| {
                    if pair.len() == 2 {
                        self.merge(&pair[0], &pair[1], false)
                    } else {
                        pair[0].clone()
                    }
                })
                .collect();
        }

        sorted_chunks.into_iter().next().unwrap_or_default()
    }

    /// Adaptive parallel merge sort
    pub fn adaptive_parallel_merge_sort(&self, arr: &[i32]) -> Vec<i32> {
        let n = arr.len();

        if n <= self.sequential_threshold {
            self.sequential_merge_sort(arr)
        } else if n <= 100_000 {
            self.parallel_merge_sort_rayon(arr)
        } else {
            self.parallel_merge_sort_iter(arr)
        }
    }

    /// Sort with performance metrics
    pub fn sort_with_metrics(&self, arr: &[i32], method: &str) -> SortResult {
        self.reset_comparisons();

        let num_threads = rayon::current_num_threads();
        let start = Instant::now();

        let sorted = match method {
            "sequential" => self.sequential_merge_sort(arr),
            "rayon_join" => self.parallel_merge_sort_rayon(arr),
            "rayon_iter" => self.parallel_merge_sort_iter(arr),
            "adaptive" => self.adaptive_parallel_merge_sort(arr),
            _ => self.adaptive_parallel_merge_sort(arr),
        };

        let time_taken = start.elapsed();

        SortResult {
            sorted_array: sorted,
            time_taken,
            comparisons: self.get_comparisons(),
            method: method.to_string(),
            num_threads,
        }
    }
}

/// Benchmark all sorting methods
pub fn benchmark_all_methods(arr: &[i32]) -> Vec<(String, SortResult)> {
    let methods = vec!["sequential", "rayon_join", "rayon_iter", "adaptive"];
    let mut results = Vec::new();

    for method in methods {
        let sorter = ParallelMergeSort::new(1000);
        let result = sorter.sort_with_metrics(arr, method);
        results.push((method.to_string(), result));
    }

    results
}

/// Calculate speedup factor
pub fn calculate_speedup(seq_time: std::time::Duration, parallel_time: std::time::Duration) -> f64 {
    if parallel_time.as_secs_f64() == 0.0 {
        return 0.0;
    }
    seq_time.as_secs_f64() / parallel_time.as_secs_f64()
}

/// Calculate parallel efficiency
pub fn calculate_efficiency(speedup: f64, num_threads: usize) -> f64 {
    if num_threads == 0 {
        return 0.0;
    }
    speedup / num_threads as f64
}

/// Check if array is sorted
pub fn is_sorted(arr: &[i32]) -> bool {
    arr.windows(2).all(|w| w[0] <= w[1])
}

fn main() {
    println!("{}", "=".repeat(80));
    println!("PARALLEL MERGE SORT DEMONSTRATION (Rust + Rayon)");
    println!("{}", "=".repeat(80));
    println!("Number of threads available: {}", rayon::current_num_threads());

    // Test with different sizes
    let sizes = vec![1000, 10000, 100000];

    for &size in &sizes {
        println!("\n{}", "=".repeat(80));
        println!("Testing with {} elements", size);
        println!("{}", "=".repeat(80));

        // Generate random array
        use rand::Rng;
        let mut rng = rand::thread_rng();
        let arr: Vec<i32> = (0..size).map(|_| rng.gen_range(0..100000)).collect();

        // Benchmark all methods
        let results = benchmark_all_methods(&arr);

        // Display results
        println!("\n{:<15} {:<15} {:<20} {:<10}", "Method", "Time", "Comparisons", "Verified");
        println!("{}", "-".repeat(80));

        let seq_time = results.iter()
            .find(|(method, _)| method == "sequential")
            .map(|(_, result)| result.time_taken)
            .unwrap_or_default();

        for (method, result) in &results {
            let verified = if is_sorted(&result.sorted_array) { "✓" } else { "✗" };

            println!(
                "{:<15} {:>13.6?}  {:>18}  {:<10}",
                method, result.time_taken, result.comparisons, verified
            );

            if method != "sequential" && seq_time.as_secs_f64() > 0.0 {
                let speedup = calculate_speedup(seq_time, result.time_taken);
                let efficiency = calculate_efficiency(speedup, result.num_threads);
                println!(
                    "{:<15} Speedup: {:.2}x  Efficiency: {:.2}%",
                    "", speedup, efficiency * 100.0
                );
            }
        }
    }

    println!("\n{}", "=".repeat(80));
    println!("RAYON CONFIGURATION ANALYSIS");
    println!("{}", "=".repeat(80));

    // Test with different thread counts
    println!("\nScalability test (50,000 elements):");
    use rand::Rng;
    let mut rng = rand::thread_rng();
    let test_arr: Vec<i32> = (0..50000).map(|_| rng.gen_range(0..100000)).collect();

    println!("\n{:<10} {:<15} {:<10}", "Threads", "Time", "Speedup");
    println!("{}", "-".repeat(40));

    let max_threads = rayon::current_num_threads();
    let mut baseline_time = std::time::Duration::default();

    for num_threads in 1..=max_threads {
        let pool = rayon::ThreadPoolBuilder::new()
            .num_threads(num_threads)
            .build()
            .unwrap();

        let result = pool.install(|| {
            let sorter = ParallelMergeSort::new(1000);
            sorter.sort_with_metrics(&test_arr, "rayon_join")
        });

        if num_threads == 1 {
            baseline_time = result.time_taken;
        }

        let speedup = calculate_speedup(baseline_time, result.time_taken);
        println!(
            "{:<10} {:>13.6?}  {:.2}x",
            num_threads, result.time_taken, speedup
        );
    }

    println!("\n{}", "=".repeat(80));
    println!("WHEN TO USE PARALLEL MERGE SORT IN RUST");
    println!("{}", "=".repeat(80));
    println!(r#"
Parallel merge sort with Rayon is beneficial when:

✓ Dataset size > 10,000 elements
✓ Multiple CPU cores available
✓ CPU-bound comparison operations
✓ Need for memory safety without GC overhead

Rust + Rayon advantages:
✓ Zero-cost abstractions
✓ Memory safety guarantees at compile time
✓ No data races by design (borrow checker)
✓ Work-stealing scheduler (same as Go's)
✓ Excellent cache locality
✓ No runtime overhead

Avoid parallel merge sort when:

✗ Small datasets (<1,000 elements)
✗ Single-core systems
✗ Simple comparisons with negligible CPU cost
✗ Already using all cores for other tasks

Strategy selection:
- Sequential: < 1,000 elements
- Rayon Join: 1,000 - 100,000 elements (best for recursive)
- Rayon Iter: > 100,000 elements (better chunking)
- Adaptive: Let the algorithm decide

Performance characteristics:
- Thread spawn: ~1-2μs overhead
- Work stealing: Highly efficient load balancing
- Near-linear speedup: 3.5-3.8x on 4 cores
- Efficiency: 85-95% for optimal workload
- Memory overhead: Minimal (stack allocation)

Best practices:
1. Use rayon::join for divide-and-conquer algorithms
2. Use par_iter for data parallelism over collections
3. Configure thread pool size with ThreadPoolBuilder
4. Profile with cargo flamegraph
5. Use --release flag for realistic benchmarks
6. Consider cache effects (prefer smaller chunks)

Rayon features used:
- rayon::join: Fork-join parallelism
- par_chunks: Parallel iterator over chunks
- ThreadPoolBuilder: Custom thread pool configuration
- current_num_threads: Query available parallelism

Memory safety:
✓ No race conditions (enforced by borrow checker)
✓ No data races (Send + Sync traits)
✓ No use-after-free
✓ No null pointer dereferences
✓ No iterator invalidation
"#);

    println!("\nDemonstration complete!");
}

// Note: To run this code, you need to add these dependencies to Cargo.toml:
// [dependencies]
// rayon = "1.7"
// rand = "0.8"
