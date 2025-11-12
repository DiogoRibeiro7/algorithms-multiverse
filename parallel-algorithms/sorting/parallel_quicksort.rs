/*
Parallel Quicksort Implementation in Rust

This implementation uses Rayon for data parallelism with:
- Zero-cost abstractions
- Memory safety without garbage collection
- Work-stealing scheduler
- Three-way partitioning for duplicates

Features:
- Rayon parallel sorting
- In-place partitioning
- Type safety and zero-cost abstractions
- Fearless concurrency

Time Complexity: O(n log n) average, O(n²) worst case
Space Complexity: O(log n) with in-place partitioning

To compile and run:
1. Add to Cargo.toml:
   [dependencies]
   rayon = "1.7"
   rand = "0.8"

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
    pub swaps: usize,
    pub method: String,
    pub num_threads: usize,
}

/// Parallel quicksort implementation
pub struct ParallelQuicksort {
    sequential_threshold: usize,
    comparisons: AtomicUsize,
    swaps: AtomicUsize,
}

impl ParallelQuicksort {
    /// Create a new ParallelQuicksort instance
    pub fn new(sequential_threshold: usize) -> Self {
        ParallelQuicksort {
            sequential_threshold,
            comparisons: AtomicUsize::new(0),
            swaps: AtomicUsize::new(0),
        }
    }

    /// Increment comparison counter (thread-safe)
    fn increment_comparisons(&self, count: usize) {
        self.comparisons.fetch_add(count, Ordering::Relaxed);
    }

    /// Increment swap counter (thread-safe)
    fn increment_swaps(&self, count: usize) {
        self.swaps.fetch_add(count, Ordering::Relaxed);
    }

    /// Reset counters
    fn reset_counters(&self) {
        self.comparisons.store(0, Ordering::Relaxed);
        self.swaps.store(0, Ordering::Relaxed);
    }

    /// Get current comparison count
    fn get_comparisons(&self) -> usize {
        self.comparisons.load(Ordering::Relaxed)
    }

    /// Get current swap count
    fn get_swaps(&self) -> usize {
        self.swaps.load(Ordering::Relaxed)
    }

    /// Three-way partitioning (Dutch National Flag algorithm)
    fn three_way_partition(&self, arr: &mut [i32]) -> (usize, usize) {
        if arr.is_empty() {
            return (0, 0);
        }

        // Choose random pivot
        let pivot_idx = rand::random::<usize>() % arr.len();
        let pivot = arr[pivot_idx];

        let mut lt = 0;
        let mut i = 0;
        let mut gt = arr.len() - 1;

        let mut comparisons = 0;
        let mut swaps = 0;

        while i <= gt {
            comparisons += 1;
            if arr[i] < pivot {
                arr.swap(lt, i);
                swaps += 1;
                lt += 1;
                i += 1;
            } else if arr[i] > pivot {
                comparisons += 1;
                arr.swap(i, gt);
                swaps += 1;
                if gt == 0 {
                    break;
                }
                gt -= 1;
            } else {
                i += 1;
            }
        }

        self.increment_comparisons(comparisons);
        self.increment_swaps(swaps);

        (lt, gt)
    }

    /// Sequential quicksort for base cases
    pub fn sequential_quicksort(&self, arr: &mut [i32]) {
        if arr.len() <= 1 {
            return;
        }

        let (lt, gt) = self.three_way_partition(arr);

        if lt > 0 {
            self.sequential_quicksort(&mut arr[..lt]);
        }
        if gt + 1 < arr.len() {
            self.sequential_quicksort(&mut arr[gt + 1..]);
        }
    }

    /// Parallel quicksort using rayon's join
    pub fn parallel_quicksort_rayon(&self, arr: &mut [i32]) {
        if arr.len() <= self.sequential_threshold {
            self.sequential_quicksort(arr);
            return;
        }

        let (lt, gt) = self.three_way_partition(arr);

        // Split array
        let (left, rest) = arr.split_at_mut(lt);
        let right = if gt + 1 < rest.len() {
            &mut rest[gt + 1 - lt..]
        } else {
            &mut []
        };

        // Rayon's join runs two closures potentially in parallel
        rayon::join(
            || self.parallel_quicksort_rayon(left),
            || self.parallel_quicksort_rayon(right),
        );
    }

    /// Parallel quicksort using rayon's par_iter (alternative approach)
    pub fn parallel_quicksort_chunks(&self, arr: &mut [i32]) {
        if arr.len() <= self.sequential_threshold {
            self.sequential_quicksort(arr);
            return;
        }

        // For very large arrays, partition into chunks first
        let num_threads = rayon::current_num_threads();
        let chunk_size = (arr.len() + num_threads - 1) / num_threads;

        if arr.len() > chunk_size * 2 {
            // Sort chunks in parallel first
            arr.par_chunks_mut(chunk_size)
                .for_each(|chunk| self.sequential_quicksort(chunk));

            // Then merge (simplified - could use better merging)
            arr.sort_unstable();
        } else {
            self.parallel_quicksort_rayon(arr);
        }
    }

    /// Sort with performance metrics
    pub fn sort_with_metrics(&self, arr: &[i32], method: &str) -> SortResult {
        self.reset_counters();

        let num_threads = rayon::current_num_threads();
        let mut arr_copy = arr.to_vec();
        let start = Instant::now();

        match method {
            "sequential" => self.sequential_quicksort(&mut arr_copy),
            "rayon_join" => self.parallel_quicksort_rayon(&mut arr_copy),
            "rayon_chunks" => self.parallel_quicksort_chunks(&mut arr_copy),
            _ => self.parallel_quicksort_rayon(&mut arr_copy),
        }

        let time_taken = start.elapsed();

        SortResult {
            sorted_array: arr_copy,
            time_taken,
            comparisons: self.get_comparisons(),
            swaps: self.get_swaps(),
            method: method.to_string(),
            num_threads,
        }
    }
}

/// Benchmark all sorting methods
pub fn benchmark_all_methods(arr: &[i32]) -> Vec<(String, SortResult)> {
    let methods = vec!["sequential", "rayon_join", "rayon_chunks"];
    let mut results = Vec::new();

    for method in methods {
        let sorter = ParallelQuicksort::new(1000);
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
    println!("PARALLEL QUICKSORT DEMONSTRATION (Rust + Rayon)");
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
        println!("\n{:<20} {:<15} {:<15} {:<15} {:<10}",
                "Method", "Time", "Comparisons", "Swaps", "Verified");
        println!("{}", "-".repeat(80));

        let seq_time = results.iter()
            .find(|(method, _)| method == "sequential")
            .map(|(_, result)| result.time_taken)
            .unwrap_or_default();

        for (method, result) in &results {
            let verified = if is_sorted(&result.sorted_array) { "✓" } else { "✗" };

            println!(
                "{:<20} {:>13.6?}  {:>13}  {:>13}  {:<10}",
                method, result.time_taken, result.comparisons, result.swaps, verified
            );

            if method != "sequential" && seq_time.as_secs_f64() > 0.0 {
                let speedup = calculate_speedup(seq_time, result.time_taken);
                let efficiency = calculate_efficiency(speedup, result.num_threads);
                println!(
                    "{:<20} Speedup: {:.2}x  Efficiency: {:.2}%",
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
            let sorter = ParallelQuicksort::new(1000);
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
    println!("WHEN TO USE PARALLEL QUICKSORT IN RUST");
    println!("{}", "=".repeat(80));
    println!(r#"
Parallel quicksort with Rayon is beneficial when:

✓ Large datasets (>10,000 elements)
✓ Random or uniformly distributed data
✓ Multiple CPU cores available
✓ In-place sorting preferred
✓ Need memory safety guarantees

Rust + Rayon advantages:
✓ Zero-cost abstractions
✓ Memory safety guarantees at compile time
✓ No data races by design (borrow checker)
✓ Work-stealing scheduler (same as Go's)
✓ Excellent cache locality
✓ No runtime overhead
✓ Three-way partitioning handles duplicates

Avoid parallel quicksort when:

✗ Small datasets (<1,000 elements)
✗ Nearly sorted or reverse-sorted data (O(n²) worst case)
✗ Single-core systems
✗ Worst-case guarantee needed (use merge sort)
✗ Stable sorting required

Strategy selection:
- Sequential: < 1,000 elements
- Rayon Join: 1,000 - 100,000 elements (best for recursive)
- Rayon Chunks: > 100,000 elements (hybrid approach)

Performance characteristics:
- Thread spawn: ~1-2μs overhead
- Work stealing: Highly efficient load balancing
- Three-way partitioning: O(n) with good duplicate handling
- Average case: O(n log n) with 3-4x speedup on 4 cores
- Worst case: O(n²) with sorted/reverse data
- Efficiency: 75-90% for random data

Best practices:
1. Use rayon::join for divide-and-conquer algorithms
2. Use three-way partitioning for duplicate handling
3. Configure thread pool size with ThreadPoolBuilder
4. Profile with cargo flamegraph
5. Use --release flag for realistic benchmarks
6. Consider input distribution (randomize if needed)

Rayon features used:
- rayon::join: Fork-join parallelism
- par_chunks_mut: Parallel iterator over mutable chunks
- ThreadPoolBuilder: Custom thread pool configuration
- current_num_threads: Query available parallelism

Memory safety:
✓ No race conditions (enforced by borrow checker)
✓ No data races (Send + Sync traits)
✓ No use-after-free
✓ No null pointer dereferences
✓ No iterator invalidation
✓ Compile-time ownership checks

vs. Parallel Merge Sort:
+ Quicksort: Better cache locality, in-place, faster average
- Quicksort: Worse worst case (O(n²)), unstable
+ Merge Sort: Guaranteed O(n log n), stable, predictable
- Merge Sort: Extra space (O(n)), more memory bandwidth

Optimization tips:
1. Use three-way partitioning for many duplicates
2. Randomize pivot selection to avoid worst case
3. Tune sequential threshold (typically 500-2000)
4. Consider parallel_sort_unstable for large datasets
5. Profile to identify actual bottlenecks

Debugging and profiling:
- cargo test -- --test-threads=1: Sequential tests
- RUST_BACKTRACE=1: Stack traces
- cargo flamegraph: Performance profiling
- cargo bench: Benchmarking framework
- ThreadSanitizer: Detect data races
"#);

    println!("\nDemonstration complete!");
}

// Note: To run this code, you need to add these dependencies to Cargo.toml:
// [dependencies]
// rayon = "1.7"
// rand = "0.8"
