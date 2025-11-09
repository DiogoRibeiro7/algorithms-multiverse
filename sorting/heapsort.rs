// Heap Sort Algorithm Implementation in Rust
//
// Time Complexity: O(n log n) - consistently across all cases
// Space Complexity: O(1) for in-place sorting, O(n) for auxiliary heap
//
// Heap Sort is a comparison-based sorting algorithm that uses a binary heap data
// structure. It divides its input into a sorted and an unsorted region, and it
// iteratively shrinks the unsorted region by extracting the largest element and
// inserting it into the sorted region.
//
// Rust features:
// - Generic functions with trait bounds
// - Ownership and borrowing
// - Error handling with Result types
// - Complete heap data structure
// - Zero-cost abstractions

use std::fmt::{Debug, Display};
use std::time::Instant;

/// Maintain the max-heap property for a subtree rooted at index i.
///
/// Time Complexity: O(log n)
pub fn heapify_max<T: Ord>(arr: &mut [T], n: usize, i: usize) {
    let mut largest = i;
    let left = 2 * i + 1;
    let right = 2 * i + 2;

    // Check if left child exists and is greater than root
    if left < n && arr[left] > arr[largest] {
        largest = left;
    }

    // Check if right child exists and is greater than largest so far
    if right < n && arr[right] > arr[largest] {
        largest = right;
    }

    // If largest is not root, swap and recursively heapify
    if largest != i {
        arr.swap(i, largest);
        heapify_max(arr, n, largest);
    }
}

/// Maintain the min-heap property for a subtree rooted at index i.
///
/// Time Complexity: O(log n)
pub fn heapify_min<T: Ord>(arr: &mut [T], n: usize, i: usize) {
    let mut smallest = i;
    let left = 2 * i + 1;
    let right = 2 * i + 2;

    if left < n && arr[left] < arr[smallest] {
        smallest = left;
    }

    if right < n && arr[right] < arr[smallest] {
        smallest = right;
    }

    if smallest != i {
        arr.swap(i, smallest);
        heapify_min(arr, n, smallest);
    }
}

/// Build a max-heap from an unordered array.
///
/// Time Complexity: O(n)
pub fn build_max_heap<T: Ord>(arr: &mut [T]) {
    let n = arr.len();
    // Start from the last non-leaf node and heapify each node
    if n > 0 {
        for i in (0..=n / 2 - 1).rev() {
            heapify_max(arr, n, i);
        }
    }
}

/// Build a min-heap from an unordered array.
///
/// Time Complexity: O(n)
pub fn build_min_heap<T: Ord>(arr: &mut [T]) {
    let n = arr.len();
    if n > 0 {
        for i in (0..=n / 2 - 1).rev() {
            heapify_min(arr, n, i);
        }
    }
}

/// Sort a slice using heap sort algorithm.
///
/// Time Complexity: O(n log n)
pub fn heap_sort<T: Ord + Clone>(arr: &[T]) -> Vec<T> {
    if arr.len() <= 1 {
        return arr.to_vec();
    }

    let mut result = arr.to_vec();
    heap_sort_in_place(&mut result);
    result
}

/// Sort a slice in-place using heap sort algorithm.
///
/// Time Complexity: O(n log n)
/// Space Complexity: O(1)
pub fn heap_sort_in_place<T: Ord>(arr: &mut [T]) {
    let n = arr.len();

    // Build a max heap
    build_max_heap(arr);

    // Extract elements from heap one by one
    for i in (1..n).rev() {
        // Move current root to end
        arr.swap(0, i);
        // Call heapify on the reduced heap
        heapify_max(arr, i, 0);
    }
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

/// Max-Heap data structure implementation.
pub struct MaxHeap<T: Ord> {
    heap: Vec<T>,
}

impl<T: Ord> MaxHeap<T> {
    /// Create a new empty max-heap.
    pub fn new() -> Self {
        Self { heap: Vec::new() }
    }

    /// Create a max-heap from initial data.
    pub fn from_vec(data: Vec<T>) -> Self {
        let mut heap = Self { heap: data };
        heap.build_heap();
        heap
    }

    fn parent(&self, i: usize) -> usize {
        (i - 1) / 2
    }

    fn left(&self, i: usize) -> usize {
        2 * i + 1
    }

    fn right(&self, i: usize) -> usize {
        2 * i + 2
    }

    fn build_heap(&mut self) {
        let n = self.heap.len();
        if n > 0 {
            for i in (0..=n / 2 - 1).rev() {
                self.heapify_down(i);
            }
        }
    }

    fn bubble_up(&mut self, mut i: usize) {
        while i > 0 && self.heap[self.parent(i)] < self.heap[i] {
            let parent_idx = self.parent(i);
            self.heap.swap(i, parent_idx);
            i = parent_idx;
        }
    }

    fn heapify_down(&mut self, i: usize) {
        let mut largest = i;
        let left = self.left(i);
        let right = self.right(i);

        if left < self.heap.len() && self.heap[left] > self.heap[largest] {
            largest = left;
        }

        if right < self.heap.len() && self.heap[right] > self.heap[largest] {
            largest = right;
        }

        if largest != i {
            self.heap.swap(i, largest);
            self.heapify_down(largest);
        }
    }

    /// Insert a new key into the heap.
    ///
    /// Time Complexity: O(log n)
    pub fn insert(&mut self, key: T) {
        self.heap.push(key);
        self.bubble_up(self.heap.len() - 1);
    }

    /// Remove and return the maximum element (root) from the heap.
    ///
    /// Time Complexity: O(log n)
    pub fn extract_max(&mut self) -> Option<T> {
        if self.heap.is_empty() {
            return None;
        }

        if self.heap.len() == 1 {
            return self.heap.pop();
        }

        let max = self.heap.swap_remove(0);
        self.heapify_down(0);
        Some(max)
    }

    /// Get the maximum element without removing it.
    pub fn get_max(&self) -> Option<&T> {
        self.heap.first()
    }

    /// Increase the value of a key at index i.
    ///
    /// Time Complexity: O(log n)
    pub fn increase_key(&mut self, i: usize, new_key: T) -> Result<(), String> {
        if i >= self.heap.len() {
            return Err(format!("Index {} out of bounds", i));
        }

        if new_key < self.heap[i] {
            return Err("New key is smaller than current key".to_string());
        }

        self.heap[i] = new_key;
        self.bubble_up(i);
        Ok(())
    }

    /// Decrease the value of a key at index i.
    ///
    /// Time Complexity: O(log n)
    pub fn decrease_key(&mut self, i: usize, new_key: T) -> Result<(), String> {
        if i >= self.heap.len() {
            return Err(format!("Index {} out of bounds", i));
        }

        if new_key > self.heap[i] {
            return Err("New key is greater than current key".to_string());
        }

        self.heap[i] = new_key;
        self.heapify_down(i);
        Ok(())
    }

    /// Return the size of the heap.
    pub fn size(&self) -> usize {
        self.heap.len()
    }

    /// Check if the heap is empty.
    pub fn is_empty(&self) -> bool {
        self.heap.is_empty()
    }

    /// Return a reference to the internal vector.
    pub fn as_slice(&self) -> &[T] {
        &self.heap
    }

    /// Create ASCII art visualization of the heap.
    pub fn visualize(&self) -> String
    where
        T: Display,
    {
        if self.heap.is_empty() {
            return "Empty heap".to_string();
        }

        let mut lines = Vec::new();
        self.visualize_helper(0, "", "", &mut lines);
        lines.join("\n")
    }

    fn visualize_helper(&self, i: usize, prefix: &str, child_prefix: &str, lines: &mut Vec<String>)
    where
        T: Display,
    {
        if i >= self.heap.len() {
            return;
        }

        lines.push(format!("{}{}", prefix, self.heap[i]));

        let left_idx = self.left(i);
        let right_idx = self.right(i);

        if left_idx < self.heap.len() || right_idx < self.heap.len() {
            if left_idx < self.heap.len() {
                if right_idx < self.heap.len() {
                    self.visualize_helper(left_idx, &format!("{}├── ", child_prefix), &format!("{}│   ", child_prefix), lines);
                } else {
                    self.visualize_helper(left_idx, &format!("{}└── ", child_prefix), &format!("{}    ", child_prefix), lines);
                }
            }

            if right_idx < self.heap.len() {
                self.visualize_helper(right_idx, &format!("{}└── ", child_prefix), &format!("{}    ", child_prefix), lines);
            }
        }
    }
}

impl<T: Ord> Default for MaxHeap<T> {
    fn default() -> Self {
        Self::new()
    }
}

/// Min-Heap data structure implementation.
pub struct MinHeap<T: Ord> {
    heap: Vec<T>,
}

impl<T: Ord> MinHeap<T> {
    pub fn new() -> Self {
        Self { heap: Vec::new() }
    }

    pub fn from_vec(data: Vec<T>) -> Self {
        let mut heap = Self { heap: data };
        heap.build_heap();
        heap
    }

    fn parent(&self, i: usize) -> usize {
        (i - 1) / 2
    }

    fn left(&self, i: usize) -> usize {
        2 * i + 1
    }

    fn right(&self, i: usize) -> usize {
        2 * i + 2
    }

    fn build_heap(&mut self) {
        let n = self.heap.len();
        if n > 0 {
            for i in (0..=n / 2 - 1).rev() {
                self.heapify_down(i);
            }
        }
    }

    fn bubble_up(&mut self, mut i: usize) {
        while i > 0 && self.heap[self.parent(i)] > self.heap[i] {
            let parent_idx = self.parent(i);
            self.heap.swap(i, parent_idx);
            i = parent_idx;
        }
    }

    fn heapify_down(&mut self, i: usize) {
        let mut smallest = i;
        let left = self.left(i);
        let right = self.right(i);

        if left < self.heap.len() && self.heap[left] < self.heap[smallest] {
            smallest = left;
        }

        if right < self.heap.len() && self.heap[right] < self.heap[smallest] {
            smallest = right;
        }

        if smallest != i {
            self.heap.swap(i, smallest);
            self.heapify_down(smallest);
        }
    }

    pub fn insert(&mut self, key: T) {
        self.heap.push(key);
        self.bubble_up(self.heap.len() - 1);
    }

    pub fn extract_min(&mut self) -> Option<T> {
        if self.heap.is_empty() {
            return None;
        }

        if self.heap.len() == 1 {
            return self.heap.pop();
        }

        let min = self.heap.swap_remove(0);
        self.heapify_down(0);
        Some(min)
    }

    pub fn get_min(&self) -> Option<&T> {
        self.heap.first()
    }

    pub fn size(&self) -> usize {
        self.heap.len()
    }

    pub fn is_empty(&self) -> bool {
        self.heap.is_empty()
    }

    pub fn visualize(&self) -> String
    where
        T: Display,
    {
        if self.heap.is_empty() {
            return "Empty heap".to_string();
        }

        let mut lines = Vec::new();
        self.visualize_helper(0, "", "", &mut lines);
        lines.join("\n")
    }

    fn visualize_helper(&self, i: usize, prefix: &str, child_prefix: &str, lines: &mut Vec<String>)
    where
        T: Display,
    {
        if i >= self.heap.len() {
            return;
        }

        lines.push(format!("{}{}", prefix, self.heap[i]));

        let left_idx = self.left(i);
        let right_idx = self.right(i);

        if left_idx < self.heap.len() || right_idx < self.heap.len() {
            if left_idx < self.heap.len() {
                if right_idx < self.heap.len() {
                    self.visualize_helper(left_idx, &format!("{}├── ", child_prefix), &format!("{}│   ", child_prefix), lines);
                } else {
                    self.visualize_helper(left_idx, &format!("{}└── ", child_prefix), &format!("{}    ", child_prefix), lines);
                }
            }

            if right_idx < self.heap.len() {
                self.visualize_helper(right_idx, &format!("{}└── ", child_prefix), &format!("{}    ", child_prefix), lines);
            }
        }
    }
}

impl<T: Ord> Default for MinHeap<T> {
    fn default() -> Self {
        Self::new()
    }
}

/// Priority Queue implementation using a max-heap.
pub struct PriorityQueue<T: Ord> {
    heap: MaxHeap<T>,
}

impl<T: Ord> PriorityQueue<T> {
    pub fn new() -> Self {
        Self {
            heap: MaxHeap::new(),
        }
    }

    pub fn enqueue(&mut self, item: T) {
        self.heap.insert(item);
    }

    pub fn dequeue(&mut self) -> Option<T> {
        self.heap.extract_max()
    }

    pub fn peek(&self) -> Option<&T> {
        self.heap.get_max()
    }

    pub fn is_empty(&self) -> bool {
        self.heap.is_empty()
    }

    pub fn size(&self) -> usize {
        self.heap.size()
    }
}

impl<T: Ord> Default for PriorityQueue<T> {
    fn default() -> Self {
        Self::new()
    }
}

/// Print a slice with a label.
fn print_slice<T: Debug>(arr: &[T], label: &str) {
    println!("{}: {:?}", label, arr);
}

/// Demonstrate heap sort and heap data structure.
fn demonstrate_heap_sort() {
    println!("🏔️  Heap Sort Implementation in Rust");
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
    ];

    println!("\n📋 Basic Sorting Tests:");
    println!("{}", "-".repeat(60));

    for (arr, desc) in test_cases {
        let original = arr.clone();
        let sorted_arr = heap_sort(&arr);

        println!("\nTest: {}", desc);
        print_slice(&original, "Original");
        print_slice(&sorted_arr, "Sorted  ");
        println!("Correct:  {}", if is_sorted(&sorted_arr) { "✓" } else { "✗" });
    }

    println!("\n{}", "-".repeat(60));

    // Demonstrate heap visualization
    println!("\n🌲 Heap Visualization:");
    println!("{}", "-".repeat(60));

    let data = vec![64, 34, 25, 12, 22, 11, 90];
    let max_heap = MaxHeap::from_vec(data.clone());

    println!("\nMax-Heap built from: {:?}", data);
    println!("{}", max_heap.visualize());

    println!("\nMin-Heap built from: {:?}", data);
    let min_heap = MinHeap::from_vec(data);
    println!("{}", min_heap.visualize());

    // Demonstrate heap operations
    println!("\n🔧 Heap Operations:");
    println!("{}", "-".repeat(60));

    let mut heap = MaxHeap::new();
    let operations = vec![50, 30, 70, 20, 40, 60, 80];

    println!("\nInserting elements: {:?}", operations);
    for val in operations {
        heap.insert(val);
        println!("Inserted {}, Max: {:?}", val, heap.get_max().unwrap());
    }

    println!("\nHeap structure:");
    println!("{}", heap.visualize());

    println!("\nExtracting elements:");
    let mut extracted = Vec::new();
    while !heap.is_empty() {
        let val = heap.extract_max().unwrap();
        extracted.push(val);
        println!("Extracted: {}", val);
    }

    print_slice(&extracted, "Extraction order");

    // Demonstrate priority queue
    println!("\n📬 Priority Queue Demo:");
    println!("{}", "-".repeat(60));

    let mut pq = PriorityQueue::new();
    let tasks = vec![5, 1, 9, 3, 7];

    println!("\nEnqueuing tasks with priorities: {:?}", tasks);
    for priority in tasks {
        pq.enqueue(priority);
        println!("Enqueued priority {}, Top priority: {:?}", priority, pq.peek().unwrap());
    }

    println!("\nProcessing tasks by priority:");
    while !pq.is_empty() {
        let priority = pq.dequeue().unwrap();
        println!("Processing task with priority: {}", priority);
    }
}

/// Benchmark heap sort.
fn performance_benchmark() {
    println!("\n\n⚡ Performance Benchmark");
    println!("{}", "=".repeat(80));

    let sizes = vec![100, 500, 1000, 5000, 10000];

    let patterns: Vec<(&str, Box<dyn Fn(usize) -> Vec<i32>>)> = vec![
        (
            "Random",
            Box::new(|n| {
                use rand::Rng;
                let mut rng = rand::thread_rng();
                (0..n).map(|_| rng.gen_range(1..1001)).collect()
            }),
        ),
        ("Sorted", Box::new(|n| (0..n as i32).collect())),
        ("Reversed", Box::new(|n| (0..n as i32).rev().collect())),
    ];

    for (pattern_name, pattern_gen) in &patterns {
        println!("\n{} Data:", pattern_name);
        println!("{:<8}{:>15}{:>15}", "Size", "Heap Sort", "slice.sort");
        println!("{}", "-".repeat(38));

        for &size in &sizes {
            let test_data = pattern_gen(size);
            print!("{:<8}", size);

            // Heap Sort
            let start = Instant::now();
            let _ = heap_sort(&test_data);
            let duration = start.elapsed();
            print!("{:>14.2}ms", duration.as_secs_f64() * 1000.0);

            // slice.sort
            let mut test_data2 = test_data.clone();
            let start = Instant::now();
            test_data2.sort();
            let duration = start.elapsed();
            println!("{:>14.2}ms", duration.as_secs_f64() * 1000.0);
        }
    }
}

/// Test edge cases.
fn test_edge_cases() {
    println!("\n\n🧪 Edge Cases and Error Handling");
    println!("{}", "=".repeat(60));

    println!("\n1. Testing empty heap operations:");
    let mut heap: MaxHeap<i32> = MaxHeap::new();
    match heap.extract_max() {
        None => println!("   ✓ Correctly returned None"),
        Some(_) => println!("   ✗ Should have returned None"),
    }

    println!("\n2. Testing increaseKey with smaller value:");
    let mut heap2 = MaxHeap::from_vec(vec![10, 20, 30]);
    match heap2.increase_key(0, 5) {
        Err(e) => println!("   ✓ Correctly returned error: {}", e),
        Ok(_) => println!("   ✗ Should have returned error"),
    }

    println!("\n3. Testing with duplicates:");
    let arr = vec![5, 5, 5, 5, 5];
    let sorted = heap_sort(&arr);
    print_slice(&arr, "   Original");
    print_slice(&sorted, "   Sorted  ");
    println!("   Correct:  {}", if sorted == arr { "✓" } else { "✗" });
}

fn main() {
    demonstrate_heap_sort();
    performance_benchmark();
    test_edge_cases();

    println!("\n✨ Heap Sort demonstration complete!");
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
    fn test_heap_sort() {
        let arr = vec![64, 34, 25, 12, 22, 11, 90];
        let sorted = heap_sort(&arr);
        assert_eq!(sorted, vec![11, 12, 22, 25, 34, 64, 90]);
    }

    #[test]
    fn test_empty_array() {
        let arr: Vec<i32> = vec![];
        let sorted = heap_sort(&arr);
        assert_eq!(sorted, vec![]);
    }

    #[test]
    fn test_max_heap_operations() {
        let mut heap = MaxHeap::new();
        heap.insert(5);
        heap.insert(3);
        heap.insert(7);

        assert_eq!(heap.get_max(), Some(&7));
        assert_eq!(heap.extract_max(), Some(7));
        assert_eq!(heap.get_max(), Some(&5));
    }

    #[test]
    fn test_priority_queue() {
        let mut pq = PriorityQueue::new();
        pq.enqueue(5);
        pq.enqueue(10);
        pq.enqueue(3);

        assert_eq!(pq.dequeue(), Some(10));
        assert_eq!(pq.dequeue(), Some(5));
        assert_eq!(pq.dequeue(), Some(3));
        assert_eq!(pq.dequeue(), None);
    }
}
