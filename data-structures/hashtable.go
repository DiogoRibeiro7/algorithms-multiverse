/**
 * Comprehensive Hash Table Implementation in Go
 *
 * Features:
 * - Separate chaining for collision resolution
 * - Dynamic resizing with configurable load factor
 * - FNV-1a hash function
 * - Generic implementation using Go generics
 * - Iterator support
 * - Thread-safe variant available
 * - Performance statistics
 *
 * Time Complexity:
 * - Average: O(1) for insert, delete, search
 * - Worst:   O(n) for chaining with poor hash function
 *
 * Space Complexity: O(n) where n is the number of elements
 *
 * Usage:
 *   go run hashtable.go
 */

package main

import (
	"fmt"
	"hash/fnv"
	"sync"
)

// ============================================================================
// HASH TABLE NODE
// ============================================================================

// Node represents a key-value pair in the chain
type node[K comparable, V any] struct {
	key   K
	value V
	next  *node[K, V]
}

// ============================================================================
// HASH TABLE STRUCTURE
// ============================================================================

// HashTable implements a hash table with separate chaining
type HashTable[K comparable, V any] struct {
	buckets    []*node[K, V] // Array of linked list heads
	capacity   int           // Number of buckets
	size       int           // Number of elements
	loadFactor float64       // Resize threshold

	// Statistics
	collisions int
	resizes    int
}

// ============================================================================
// HASH FUNCTIONS
// ============================================================================

// hashString computes FNV-1a hash for string
func hashString(s string) uint32 {
	h := fnv.New32a()
	h.Write([]byte(s))
	return h.Sum32()
}

// hashInt computes hash for integer
func hashInt(i int) uint32 {
	// Simple integer hashing
	x := uint32(i)
	x = ((x >> 16) ^ x) * 0x45d9f3b
	x = ((x >> 16) ^ x) * 0x45d9f3b
	x = (x >> 16) ^ x
	return x
}

// getHash returns hash value for key
func getHash[K comparable](key K) uint32 {
	switch v := any(key).(type) {
	case string:
		return hashString(v)
	case int:
		return hashInt(v)
	default:
		// Fallback to fmt.Sprint for other types
		return hashString(fmt.Sprint(v))
	}
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

// nextPowerOf2 returns the next power of 2 >= n
func nextPowerOf2(n int) int {
	if n <= 1 {
		return 1
	}
	n--
	n |= n >> 1
	n |= n >> 2
	n |= n >> 4
	n |= n >> 8
	n |= n >> 16
	n |= n >> 32
	n++
	return n
}

// ============================================================================
// HASH TABLE OPERATIONS
// ============================================================================

// NewHashTable creates a new hash table
func NewHashTable[K comparable, V any](initialCapacity int) *HashTable[K, V] {
	if initialCapacity < 1 {
		initialCapacity = 16
	}

	capacity := nextPowerOf2(initialCapacity)

	return &HashTable[K, V]{
		buckets:    make([]*node[K, V], capacity),
		capacity:   capacity,
		size:       0,
		loadFactor: 0.75,
		collisions: 0,
		resizes:    0,
	}
}

// hashIndex computes bucket index for key
func (ht *HashTable[K, V]) hashIndex(key K) int {
	return int(getHash(key)) & (ht.capacity - 1)
}

// shouldResize checks if table should be resized
func (ht *HashTable[K, V]) shouldResize() bool {
	return float64(ht.size)/float64(ht.capacity) > ht.loadFactor
}

// resize doubles capacity and rehashes all elements
func (ht *HashTable[K, V]) resize() {
	ht.resizes++
	oldBuckets := ht.buckets
	ht.capacity *= 2
	ht.buckets = make([]*node[K, V], ht.capacity)
	ht.size = 0
	ht.collisions = 0

	// Rehash all entries
	for _, bucket := range oldBuckets {
		for n := bucket; n != nil; n = n.next {
			ht.Put(n.key, n.value)
		}
	}
}

// Put inserts or updates a key-value pair
// Returns the previous value if key existed, or zero value and false otherwise
func (ht *HashTable[K, V]) Put(key K, value V) (V, bool) {
	if ht.shouldResize() {
		ht.resize()
	}

	index := ht.hashIndex(key)
	n := ht.buckets[index]

	// Search for existing key
	for n != nil {
		if n.key == key {
			oldValue := n.value
			n.value = value
			return oldValue, true
		}
		n = n.next
	}

	// Key not found, insert at head
	if ht.buckets[index] != nil {
		ht.collisions++
	}

	newNode := &node[K, V]{
		key:   key,
		value: value,
		next:  ht.buckets[index],
	}
	ht.buckets[index] = newNode
	ht.size++

	var zero V
	return zero, false
}

// Get retrieves value for key
// Returns value and true if found, zero value and false otherwise
func (ht *HashTable[K, V]) Get(key K) (V, bool) {
	index := ht.hashIndex(key)
	n := ht.buckets[index]

	for n != nil {
		if n.key == key {
			return n.value, true
		}
		n = n.next
	}

	var zero V
	return zero, false
}

// Remove deletes key and returns its value
// Returns value and true if found, zero value and false otherwise
func (ht *HashTable[K, V]) Remove(key K) (V, bool) {
	index := ht.hashIndex(key)
	n := ht.buckets[index]
	var prev *node[K, V]

	for n != nil {
		if n.key == key {
			// Found key, remove node
			if prev != nil {
				prev.next = n.next
			} else {
				ht.buckets[index] = n.next
			}
			ht.size--
			return n.value, true
		}
		prev = n
		n = n.next
	}

	var zero V
	return zero, false
}

// Contains checks if key exists
func (ht *HashTable[K, V]) Contains(key K) bool {
	_, found := ht.Get(key)
	return found
}

// Size returns number of elements
func (ht *HashTable[K, V]) Size() int {
	return ht.size
}

// Clear removes all elements
func (ht *HashTable[K, V]) Clear() {
	ht.buckets = make([]*node[K, V], ht.capacity)
	ht.size = 0
	ht.collisions = 0
}

// Keys returns all keys as a slice
func (ht *HashTable[K, V]) Keys() []K {
	keys := make([]K, 0, ht.size)
	for _, bucket := range ht.buckets {
		for n := bucket; n != nil; n = n.next {
			keys = append(keys, n.key)
		}
	}
	return keys
}

// Values returns all values as a slice
func (ht *HashTable[K, V]) Values() []V {
	values := make([]V, 0, ht.size)
	for _, bucket := range ht.buckets {
		for n := bucket; n != nil; n = n.next {
			values = append(values, n.value)
		}
	}
	return values
}

// ForEach iterates over all key-value pairs
func (ht *HashTable[K, V]) ForEach(fn func(K, V)) {
	for _, bucket := range ht.buckets {
		for n := bucket; n != nil; n = n.next {
			fn(n.key, n.value)
		}
	}
}

// Stats represents hash table statistics
type Stats struct {
	Size            int
	Capacity        int
	LoadFactor      float64
	Collisions      int
	Resizes         int
	MaxChainLength  int
	AvgChainLength  float64
	NumberOfChains  int
}

// GetStats returns performance statistics
func (ht *HashTable[K, V]) GetStats() Stats {
	maxChain := 0
	totalChainLength := 0
	numChains := 0

	for _, bucket := range ht.buckets {
		chainLength := 0
		for n := bucket; n != nil; n = n.next {
			chainLength++
		}

		if chainLength > 0 {
			numChains++
			totalChainLength += chainLength
			if chainLength > maxChain {
				maxChain = chainLength
			}
		}
	}

	avgChainLength := 0.0
	if numChains > 0 {
		avgChainLength = float64(totalChainLength) / float64(numChains)
	}

	return Stats{
		Size:            ht.size,
		Capacity:        ht.capacity,
		LoadFactor:      float64(ht.size) / float64(ht.capacity),
		Collisions:      ht.collisions,
		Resizes:         ht.resizes,
		MaxChainLength:  maxChain,
		AvgChainLength:  avgChainLength,
		NumberOfChains:  numChains,
	}
}

// PrintStats displays hash table statistics
func (ht *HashTable[K, V]) PrintStats() {
	stats := ht.GetStats()
	fmt.Println("Hash Table Statistics:")
	fmt.Printf("  Size:              %d\n", stats.Size)
	fmt.Printf("  Capacity:          %d\n", stats.Capacity)
	fmt.Printf("  Load Factor:       %.2f / %.2f\n", stats.LoadFactor, ht.loadFactor)
	fmt.Printf("  Collisions:        %d\n", stats.Collisions)
	fmt.Printf("  Resizes:           %d\n", stats.Resizes)
	fmt.Printf("  Max Chain Length:  %d\n", stats.MaxChainLength)
	fmt.Printf("  Avg Chain Length:  %.2f\n", stats.AvgChainLength)
	fmt.Printf("  Number of Chains:  %d\n", stats.NumberOfChains)
}

// ============================================================================
// THREAD-SAFE HASH TABLE
// ============================================================================

// ThreadSafeHashTable wraps HashTable with mutex for thread safety
type ThreadSafeHashTable[K comparable, V any] struct {
	ht *HashTable[K, V]
	mu sync.RWMutex
}

// NewThreadSafeHashTable creates a thread-safe hash table
func NewThreadSafeHashTable[K comparable, V any](initialCapacity int) *ThreadSafeHashTable[K, V] {
	return &ThreadSafeHashTable[K, V]{
		ht: NewHashTable[K, V](initialCapacity),
	}
}

// Put inserts or updates a key-value pair (thread-safe)
func (tsht *ThreadSafeHashTable[K, V]) Put(key K, value V) (V, bool) {
	tsht.mu.Lock()
	defer tsht.mu.Unlock()
	return tsht.ht.Put(key, value)
}

// Get retrieves value for key (thread-safe)
func (tsht *ThreadSafeHashTable[K, V]) Get(key K) (V, bool) {
	tsht.mu.RLock()
	defer tsht.mu.RUnlock()
	return tsht.ht.Get(key)
}

// Remove deletes key (thread-safe)
func (tsht *ThreadSafeHashTable[K, V]) Remove(key K) (V, bool) {
	tsht.mu.Lock()
	defer tsht.mu.Unlock()
	return tsht.ht.Remove(key)
}

// Size returns number of elements (thread-safe)
func (tsht *ThreadSafeHashTable[K, V]) Size() int {
	tsht.mu.RLock()
	defer tsht.mu.RUnlock()
	return tsht.ht.Size()
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

func main() {
	fmt.Println("===========================================")
	fmt.Println("Hash Table Implementation in Go")
	fmt.Println("===========================================")
	fmt.Println()

	// Create hash table
	ht := NewHashTable[string, int](16)

	fmt.Println("1. Inserting elements...")
	fmt.Println("-----------------------------------------")

	// Insert some data
	for i := 0; i < 10; i++ {
		key := fmt.Sprintf("key%d", i)
		value := i * 10
		ht.Put(key, value)
		fmt.Printf("  Inserted: %s -> %d\n", key, value)
	}
	fmt.Printf("\nSize: %d\n\n", ht.Size())

	fmt.Println("2. Retrieving elements...")
	fmt.Println("-----------------------------------------")

	testKeys := []string{"key0", "key5", "key9", "nonexistent"}
	for _, key := range testKeys {
		if value, found := ht.Get(key); found {
			fmt.Printf("  Get '%s': %d\n", key, value)
		} else {
			fmt.Printf("  Get '%s': Not found\n", key)
		}
	}

	fmt.Println("\n3. Testing containment...")
	fmt.Println("-----------------------------------------")
	fmt.Printf("  Contains 'key3': %v\n", ht.Contains("key3"))
	fmt.Printf("  Contains 'missing': %v\n", ht.Contains("missing"))

	fmt.Println("\n4. Updating values...")
	fmt.Println("-----------------------------------------")

	oldValue, existed := ht.Put("key5", 999)
	if existed {
		fmt.Printf("  Updated 'key5': old value = %d, new value = %d\n", oldValue, 999)
	}

	fmt.Println("\n5. Removing elements...")
	fmt.Println("-----------------------------------------")

	if removed, found := ht.Remove("key7"); found {
		fmt.Printf("  Removed 'key7': %d\n", removed)
	}
	fmt.Printf("  Size after removal: %d\n", ht.Size())

	fmt.Println("\n6. Iterating over elements...")
	fmt.Println("-----------------------------------------")
	count := 0
	ht.ForEach(func(key string, value int) {
		if count < 5 {
			fmt.Printf("  %s: %d\n", key, value)
		}
		count++
	})
	if count > 5 {
		fmt.Printf("  ... and %d more elements\n", count-5)
	}

	fmt.Println("\n7. Performance Statistics")
	fmt.Println("-----------------------------------------")
	ht.PrintStats()

	fmt.Println("\n8. Testing with many elements...")
	fmt.Println("-----------------------------------------")

	// Insert many elements to trigger resizing
	for i := 100; i < 200; i++ {
		key := fmt.Sprintf("item%d", i)
		ht.Put(key, i)
	}

	fmt.Printf("  Added 100 more elements\n")
	fmt.Printf("  New size: %d\n", ht.Size())
	fmt.Println()
	ht.PrintStats()

	fmt.Println("\n9. Testing integer keys...")
	fmt.Println("-----------------------------------------")

	intTable := NewHashTable[int, string](8)
	for i := 1; i <= 5; i++ {
		intTable.Put(i, fmt.Sprintf("value%d", i))
	}

	if val, found := intTable.Get(3); found {
		fmt.Printf("  intTable[3] = %s\n", val)
	}

	fmt.Println("\n10. Thread-safe variant...")
	fmt.Println("-----------------------------------------")

	tsht := NewThreadSafeHashTable[string, int](16)
	tsht.Put("thread-safe", 42)
	if val, found := tsht.Get("thread-safe"); found {
		fmt.Printf("  Thread-safe get: %d\n", val)
	}
	fmt.Printf("  Thread-safe size: %d\n", tsht.Size())

	fmt.Println("\n11. Clearing hash table...")
	fmt.Println("-----------------------------------------")
	ht.Clear()
	fmt.Printf("  Size after clear: %d\n", ht.Size())

	fmt.Println("\n===========================================")
	fmt.Println("✨ Hash table demonstration complete!")
	fmt.Println("===========================================")
}
