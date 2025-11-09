/**
 * Comprehensive Hash Table Implementation in Rust
 *
 * Features:
 * - Separate chaining for collision resolution
 * - Dynamic resizing with configurable load factor
 * - Generic implementation with trait bounds
 * - Memory-safe with Rust's ownership system
 * - Iterator support
 * - Performance statistics
 *
 * Time Complexity:
 * - Average: O(1) for insert, delete, search
 * - Worst:   O(n) for chaining with poor hash function
 *
 * Space Complexity: O(n) where n is the number of elements
 *
 * Compilation and Usage:
 *   rustc hashtable.rs -o hashtable
 *   ./hashtable
 *
 * Or with cargo:
 *   cargo build --release
 *   cargo run
 */

use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::fmt::Debug;

// ============================================================================
// HASH TABLE NODE
// ============================================================================

/// Node in the linked list (chain) for collision resolution
#[derive(Debug, Clone)]
struct Node<K, V> {
    key: K,
    value: V,
    next: Option<Box<Node<K, V>>>,
}

impl<K, V> Node<K, V> {
    fn new(key: K, value: V) -> Self {
        Node {
            key,
            value,
            next: None,
        }
    }
}

// ============================================================================
// HASH TABLE STRUCTURE
// ============================================================================

/// Hash table with separate chaining
pub struct HashTable<K, V> {
    buckets: Vec<Option<Box<Node<K, V>>>>,
    capacity: usize,
    size: usize,
    load_factor: f64,

    // Statistics
    collisions: usize,
    resizes: usize,
}

// ============================================================================
// HASH TABLE STATISTICS
// ============================================================================

#[derive(Debug)]
pub struct Stats {
    pub size: usize,
    pub capacity: usize,
    pub load_factor: f64,
    pub collisions: usize,
    pub resizes: usize,
    pub max_chain_length: usize,
    pub avg_chain_length: f64,
    pub number_of_chains: usize,
}

// ============================================================================
// HASH TABLE IMPLEMENTATION
// ============================================================================

impl<K, V> HashTable<K, V>
where
    K: Hash + Eq + Clone,
    V: Clone,
{
    /// Create a new hash table with initial capacity
    pub fn new(initial_capacity: usize) -> Self {
        let capacity = Self::next_power_of_2(initial_capacity.max(1));

        HashTable {
            buckets: (0..capacity).map(|_| None).collect(),
            capacity,
            size: 0,
            load_factor: 0.75,
            collisions: 0,
            resizes: 0,
        }
    }

    /// Create a new hash table with default capacity
    pub fn with_default_capacity() -> Self {
        Self::new(16)
    }

    /// Get next power of 2 >= n
    fn next_power_of_2(n: usize) -> usize {
        if n <= 1 {
            return 1;
        }
        let mut power = 1;
        while power < n {
            power *= 2;
        }
        power
    }

    /// Compute hash index for key
    fn hash_index(&self, key: &K) -> usize {
        let mut hasher = DefaultHasher::new();
        key.hash(&mut hasher);
        (hasher.finish() as usize) & (self.capacity - 1)
    }

    /// Check if table should be resized
    fn should_resize(&self) -> bool {
        (self.size as f64) / (self.capacity as f64) > self.load_factor
    }

    /// Resize and rehash all elements
    fn resize(&mut self) {
        self.resizes += 1;
        let old_buckets = std::mem::replace(
            &mut self.buckets,
            (0..self.capacity * 2).map(|_| None).collect(),
        );

        self.capacity *= 2;
        self.size = 0;
        self.collisions = 0;

        // Rehash all entries
        for bucket in old_buckets {
            let mut node = bucket;
            while let Some(mut n) = node {
                node = n.next.take();
                self.put(n.key, n.value);
            }
        }
    }

    /// Insert or update a key-value pair
    /// Returns the previous value if key existed
    pub fn put(&mut self, key: K, value: V) -> Option<V> {
        if self.should_resize() {
            self.resize();
        }

        let index = self.hash_index(&key);
        let mut node = &mut self.buckets[index];

        // Search for existing key
        while let Some(n) = node {
            if n.key == key {
                let old_value = n.value.clone();
                n.value = value;
                return Some(old_value);
            }
            node = &mut n.next;
        }

        // Key not found, insert at head
        if self.buckets[index].is_some() {
            self.collisions += 1;
        }

        let mut new_node = Box::new(Node::new(key, value));
        new_node.next = self.buckets[index].take();
        self.buckets[index] = Some(new_node);
        self.size += 1;

        None
    }

    /// Get value for key
    pub fn get(&self, key: &K) -> Option<&V> {
        let index = self.hash_index(key);
        let mut node = &self.buckets[index];

        while let Some(n) = node {
            if n.key == *key {
                return Some(&n.value);
            }
            node = &n.next;
        }

        None
    }

    /// Get mutable reference to value for key
    pub fn get_mut(&mut self, key: &K) -> Option<&mut V> {
        let index = self.hash_index(key);
        let mut node = &mut self.buckets[index];

        while let Some(n) = node {
            if n.key == *key {
                return Some(&mut n.value);
            }
            node = &mut n.next;
        }

        None
    }

    /// Remove key and return its value
    pub fn remove(&mut self, key: &K) -> Option<V> {
        let index = self.hash_index(key);
        let mut node = &mut self.buckets[index];
        let mut prev: Option<&mut Box<Node<K, V>>> = None;

        while let Some(n) = node {
            if n.key == *key {
                self.size -= 1;
                let removed = if let Some(p) = prev {
                    p.next.take()
                } else {
                    self.buckets[index].take()
                };

                if let Some(mut r) = removed {
                    if let Some(p) = prev {
                        p.next = r.next.take();
                    } else {
                        self.buckets[index] = r.next.take();
                    }
                    return Some(r.value);
                }
            }
            prev = Some(n);
            node = &mut n.next;
        }

        None
    }

    /// Check if key exists
    pub fn contains_key(&self, key: &K) -> bool {
        self.get(key).is_some()
    }

    /// Get number of elements
    pub fn len(&self) -> usize {
        self.size
    }

    /// Check if hash table is empty
    pub fn is_empty(&self) -> bool {
        self.size == 0
    }

    /// Clear all elements
    pub fn clear(&mut self) {
        self.buckets = (0..self.capacity).map(|_| None).collect();
        self.size = 0;
        self.collisions = 0;
    }

    /// Get all keys
    pub fn keys(&self) -> Vec<K> {
        let mut keys = Vec::with_capacity(self.size);
        for bucket in &self.buckets {
            let mut node = bucket;
            while let Some(n) = node {
                keys.push(n.key.clone());
                node = &n.next;
            }
        }
        keys
    }

    /// Get all values
    pub fn values(&self) -> Vec<V> {
        let mut values = Vec::with_capacity(self.size);
        for bucket in &self.buckets {
            let mut node = bucket;
            while let Some(n) = node {
                values.push(n.value.clone());
                node = &n.next;
            }
        }
        values
    }

    /// Iterate over key-value pairs
    pub fn iter(&self) -> impl Iterator<Item = (&K, &V)> {
        self.buckets.iter().flat_map(|bucket| {
            let mut items = Vec::new();
            let mut node = bucket;
            while let Some(n) = node {
                items.push((&n.key, &n.value));
                node = &n.next;
            }
            items
        })
    }

    /// Get performance statistics
    pub fn stats(&self) -> Stats {
        let mut max_chain = 0;
        let mut total_chain_length = 0;
        let mut num_chains = 0;

        for bucket in &self.buckets {
            let mut chain_length = 0;
            let mut node = bucket;

            while let Some(n) = node {
                chain_length += 1;
                node = &n.next;
            }

            if chain_length > 0 {
                num_chains += 1;
                total_chain_length += chain_length;
                max_chain = max_chain.max(chain_length);
            }
        }

        let avg_chain_length = if num_chains > 0 {
            total_chain_length as f64 / num_chains as f64
        } else {
            0.0
        };

        Stats {
            size: self.size,
            capacity: self.capacity,
            load_factor: self.size as f64 / self.capacity as f64,
            collisions: self.collisions,
            resizes: self.resizes,
            max_chain_length: max_chain,
            avg_chain_length,
            number_of_chains: num_chains,
        }
    }

    /// Print statistics
    pub fn print_stats(&self) {
        let stats = self.stats();
        println!("Hash Table Statistics:");
        println!("  Size:              {}", stats.size);
        println!("  Capacity:          {}", stats.capacity);
        println!("  Load Factor:       {:.2} / {:.2}", stats.load_factor, self.load_factor);
        println!("  Collisions:        {}", stats.collisions);
        println!("  Resizes:           {}", stats.resizes);
        println!("  Max Chain Length:  {}", stats.max_chain_length);
        println!("  Avg Chain Length:  {:.2}", stats.avg_chain_length);
        println!("  Number of Chains:  {}", stats.number_of_chains);
    }
}

impl<K, V> Default for HashTable<K, V>
where
    K: Hash + Eq + Clone,
    V: Clone,
{
    fn default() -> Self {
        Self::with_default_capacity()
    }
}

// ============================================================================
// DISPLAY TRAIT
// ============================================================================

impl<K, V> std::fmt::Debug for HashTable<K, V>
where
    K: Hash + Eq + Clone + Debug,
    V: Clone + Debug,
{
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_map().entries(self.iter()).finish()
    }
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

fn main() {
    println!("===========================================");
    println!("Hash Table Implementation in Rust");
    println!("===========================================");
    println!();

    // Create hash table
    let mut ht: HashTable<String, i32> = HashTable::new(16);

    println!("1. Inserting elements...");
    println!("-----------------------------------------");

    // Insert some data
    for i in 0..10 {
        let key = format!("key{}", i);
        let value = i * 10;
        ht.put(key.clone(), value);
        println!("  Inserted: {} -> {}", key, value);
    }
    println!("\nSize: {}\n", ht.len());

    println!("2. Retrieving elements...");
    println!("-----------------------------------------");

    let test_keys = vec!["key0", "key5", "key9", "nonexistent"];
    for key in test_keys {
        match ht.get(&key.to_string()) {
            Some(value) => println!("  Get '{}': {}", key, value),
            None => println!("  Get '{}': Not found", key),
        }
    }

    println!("\n3. Testing containment...");
    println!("-----------------------------------------");
    println!("  Contains 'key3': {}", ht.contains_key(&"key3".to_string()));
    println!("  Contains 'missing': {}", ht.contains_key(&"missing".to_string()));

    println!("\n4. Updating values...");
    println!("-----------------------------------------");

    if let Some(old_value) = ht.put("key5".to_string(), 999) {
        println!("  Updated 'key5': old value = {}, new value = 999", old_value);
    }

    println!("\n5. Removing elements...");
    println!("-----------------------------------------");

    if let Some(removed) = ht.remove(&"key7".to_string()) {
        println!("  Removed 'key7': {}", removed);
    }
    println!("  Size after removal: {}", ht.len());

    println!("\n6. Iterating over elements...");
    println!("-----------------------------------------");
    for (i, (key, value)) in ht.iter().enumerate() {
        if i < 5 {
            println!("  {}: {}", key, value);
        }
    }
    if ht.len() > 5 {
        println!("  ... and {} more elements", ht.len() - 5);
    }

    println!("\n7. Performance Statistics");
    println!("-----------------------------------------");
    ht.print_stats();

    println!("\n8. Testing with many elements...");
    println!("-----------------------------------------");

    // Insert many elements to trigger resizing
    for i in 100..200 {
        let key = format!("item{}", i);
        ht.put(key, i);
    }

    println!("  Added 100 more elements");
    println!("  New size: {}", ht.len());
    println!();
    ht.print_stats();

    println!("\n9. Testing with integer keys...");
    println!("-----------------------------------------");

    let mut int_table: HashTable<i32, String> = HashTable::new(8);
    for i in 1..=5 {
        int_table.put(i, format!("value{}", i));
    }

    if let Some(val) = int_table.get(&3) {
        println!("  int_table[3] = {}", val);
    }

    println!("\n10. Testing keys() and values()...");
    println!("-----------------------------------------");
    let keys = int_table.keys();
    let values = int_table.values();
    println!("  Keys: {:?}", keys);
    println!("  Values: {:?}", values);

    println!("\n11. Clearing hash table...");
    println!("-----------------------------------------");
    ht.clear();
    println!("  Size after clear: {}", ht.len());
    println!("  Is empty: {}", ht.is_empty());

    println!("\n===========================================");
    println!("✨ Hash table demonstration complete!");
    println!("===========================================");
}
