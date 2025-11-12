// String Hashing Algorithms Implementation in Go
//
// String hashing is a technique to convert strings into fixed-size hash values
// for efficient comparison, pattern matching, and data structure operations.
//
// Time Complexity:
// - Hash computation: O(n) where n is string length
// - Hash comparison: O(1)
// - Rolling hash update: O(1)
//
// Go features:
// - Multiple hashing algorithms (polynomial, FNV, djb2, xxHash-inspired)
// - Rolling hash for efficient substring matching
// - Collision detection and handling
// - Thread-safe hash map
// - Rabin-Karp string matching using rolling hash
// - Concurrent hash computation with goroutines

package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"hash/fnv"
	"math"
	"math/big"
	"strings"
	"sync"
)

// POLYNOMIAL ROLLING HASH

const (
	DefaultBase = 31       // Common base for string hashing
	DefaultMod  = 1e9 + 9  // Large prime modulo
	Base256     = 256      // For byte-level hashing
)

// PolynomialHash computes polynomial rolling hash
//
// hash(s) = s[0]*base^(n-1) + s[1]*base^(n-2) + ... + s[n-1] (mod prime)
//
// Time Complexity: O(n)
func PolynomialHash(s string, base, mod int64) int64 {
	hash := int64(0)
	power := int64(1)

	for i := len(s) - 1; i >= 0; i-- {
		hash = (hash + int64(s[i])*power) % mod
		power = (power * base) % mod
	}

	return hash
}

// RollingHash maintains a rolling hash for efficient updates
type RollingHash struct {
	hash  int64
	base  int64
	mod   int64
	power int64 // base^(len-1) mod mod
	text  string
	start int
	end   int
}

// NewRollingHash creates a new rolling hash for a substring
func NewRollingHash(text string, start, end int, base, mod int64) *RollingHash {
	if start < 0 || end > len(text) || start >= end {
		return nil
	}

	rh := &RollingHash{
		hash:  0,
		base:  base,
		mod:   mod,
		power: 1,
		text:  text,
		start: start,
		end:   end,
	}

	// Compute initial hash and power
	length := end - start
	for i := start; i < end; i++ {
		rh.hash = (rh.hash*base + int64(text[i])) % mod
		if i < end-1 {
			rh.power = (rh.power * base) % mod
		}
	}

	_ = length
	return rh
}

// Hash returns the current hash value
func (rh *RollingHash) Hash() int64 {
	return rh.hash
}

// RollRight moves the window one position to the right
//
// Time Complexity: O(1)
func (rh *RollingHash) RollRight() bool {
	if rh.end >= len(rh.text) {
		return false
	}

	// Remove leftmost character
	rh.hash = (rh.hash - int64(rh.text[rh.start])*rh.power) % rh.mod
	if rh.hash < 0 {
		rh.hash += rh.mod
	}

	// Shift and add rightmost character
	rh.hash = (rh.hash*rh.base + int64(rh.text[rh.end])) % rh.mod

	rh.start++
	rh.end++

	return true
}

// Substring returns the current substring
func (rh *RollingHash) Substring() string {
	return rh.text[rh.start:rh.end]
}

// RABIN-KARP STRING MATCHING

// RabinKarp finds all occurrences of pattern in text using rolling hash
//
// Time Complexity: O(n+m) average case, O(nm) worst case
// where n = len(text), m = len(pattern)
func RabinKarp(text, pattern string) []int {
	if len(pattern) == 0 || len(pattern) > len(text) {
		return []int{}
	}

	const base = DefaultBase
	const mod = DefaultMod

	matches := make([]int, 0)

	// Compute pattern hash
	patternHash := PolynomialHash(pattern, base, mod)

	// Create rolling hash for text
	rh := NewRollingHash(text, 0, len(pattern), base, mod)

	// Check first window
	if rh.Hash() == patternHash && rh.Substring() == pattern {
		matches = append(matches, 0)
	}

	// Roll through text
	for rh.RollRight() {
		if rh.Hash() == patternHash && rh.Substring() == pattern {
			matches = append(matches, rh.start)
		}
	}

	return matches
}

// CLASSIC HASH FUNCTIONS

// DJB2Hash implements the djb2 hash function
//
// Simple and effective hash function by Dan Bernstein
func DJB2Hash(s string) uint64 {
	hash := uint64(5381)

	for i := 0; i < len(s); i++ {
		hash = ((hash << 5) + hash) + uint64(s[i]) // hash * 33 + c
	}

	return hash
}

// SDBMHash implements the SDBM hash function
//
// Used in SDBM database library
func SDBMHash(s string) uint64 {
	hash := uint64(0)

	for i := 0; i < len(s); i++ {
		hash = uint64(s[i]) + (hash << 6) + (hash << 16) - hash
	}

	return hash
}

// FNVHash implements FNV-1a hash
//
// Fast, well-distributed hash function
func FNVHash(s string) uint64 {
	h := fnv.New64a()
	h.Write([]byte(s))
	return h.Sum64()
}

// MurmurHash implements a simple MurmurHash-inspired function
func MurmurHash(s string) uint64 {
	const (
		seed = uint64(0x9747b28c)
		m    = uint64(0xc6a4a7935bd1e995)
		r    = 47
	)

	hash := seed ^ (uint64(len(s)) * m)

	for i := 0; i < len(s); i++ {
		k := uint64(s[i])
		k *= m
		k ^= k >> r
		k *= m

		hash ^= k
		hash *= m
	}

	hash ^= hash >> r
	hash *= m
	hash ^= hash >> r

	return hash
}

// CRYPTOGRAPHIC HASHING

// SHA256Hash computes SHA-256 hash
func SHA256Hash(s string) string {
	hash := sha256.Sum256([]byte(s))
	return hex.EncodeToString(hash[:])
}

// HASH COMPARISON AND COLLISION DETECTION

// HashComparison compares different hash functions
type HashComparison struct {
	String       string
	Polynomial   int64
	DJB2         uint64
	SDBM         uint64
	FNV          uint64
	Murmur       uint64
	SHA256       string
}

// CompareHashes computes all hash functions for a string
func CompareHashes(s string) HashComparison {
	return HashComparison{
		String:     s,
		Polynomial: PolynomialHash(s, DefaultBase, DefaultMod),
		DJB2:       DJB2Hash(s),
		SDBM:       SDBMHash(s),
		FNV:        FNVHash(s),
		Murmur:     MurmurHash(s),
		SHA256:     SHA256Hash(s)[:16], // Truncate for display
	}
}

// CollisionDetector detects hash collisions
type CollisionDetector struct {
	hashes map[int64][]string
	count  int
}

// NewCollisionDetector creates a new collision detector
func NewCollisionDetector() *CollisionDetector {
	return &CollisionDetector{
		hashes: make(map[int64][]string),
		count:  0,
	}
}

// Add adds a string and checks for collisions
func (cd *CollisionDetector) Add(s string) []string {
	hash := PolynomialHash(s, DefaultBase, DefaultMod)
	cd.count++

	if existing, ok := cd.hashes[hash]; ok {
		// Collision detected
		cd.hashes[hash] = append(existing, s)
		return existing
	}

	cd.hashes[hash] = []string{s}
	return nil
}

// Collisions returns all collision groups
func (cd *CollisionDetector) Collisions() map[int64][]string {
	collisions := make(map[int64][]string)

	for hash, strings := range cd.hashes {
		if len(strings) > 1 {
			collisions[hash] = strings
		}
	}

	return collisions
}

// LoadFactor returns the load factor
func (cd *CollisionDetector) LoadFactor() float64 {
	return float64(cd.count) / float64(len(cd.hashes))
}

// THREAD-SAFE HASH TABLE

// ThreadSafeHashTable is a concurrent hash table using string hashing
type ThreadSafeHashTable struct {
	buckets []bucket
	size    int
}

type bucket struct {
	mu    sync.RWMutex
	items map[int64][]keyValue
}

type keyValue struct {
	key   string
	value interface{}
}

// NewThreadSafeHashTable creates a new thread-safe hash table
func NewThreadSafeHashTable(size int) *ThreadSafeHashTable {
	ht := &ThreadSafeHashTable{
		buckets: make([]bucket, size),
		size:    size,
	}

	for i := 0; i < size; i++ {
		ht.buckets[i].items = make(map[int64][]keyValue)
	}

	return ht
}

// getBucket returns the bucket index for a key
func (ht *ThreadSafeHashTable) getBucket(key string) int {
	hash := PolynomialHash(key, DefaultBase, DefaultMod)
	return int(hash % int64(ht.size))
}

// Put inserts or updates a key-value pair
func (ht *ThreadSafeHashTable) Put(key string, value interface{}) {
	idx := ht.getBucket(key)
	bucket := &ht.buckets[idx]

	bucket.mu.Lock()
	defer bucket.mu.Unlock()

	hash := PolynomialHash(key, DefaultBase, DefaultMod)

	// Check if key exists
	if items, ok := bucket.items[hash]; ok {
		for i, item := range items {
			if item.key == key {
				items[i].value = value
				return
			}
		}
		bucket.items[hash] = append(items, keyValue{key, value})
	} else {
		bucket.items[hash] = []keyValue{{key, value}}
	}
}

// Get retrieves a value by key
func (ht *ThreadSafeHashTable) Get(key string) (interface{}, bool) {
	idx := ht.getBucket(key)
	bucket := &ht.buckets[idx]

	bucket.mu.RLock()
	defer bucket.mu.RUnlock()

	hash := PolynomialHash(key, DefaultBase, DefaultMod)

	if items, ok := bucket.items[hash]; ok {
		for _, item := range items {
			if item.key == key {
				return item.value, true
			}
		}
	}

	return nil, false
}

// Delete removes a key-value pair
func (ht *ThreadSafeHashTable) Delete(key string) bool {
	idx := ht.getBucket(key)
	bucket := &ht.buckets[idx]

	bucket.mu.Lock()
	defer bucket.mu.Unlock()

	hash := PolynomialHash(key, DefaultBase, DefaultMod)

	if items, ok := bucket.items[hash]; ok {
		for i, item := range items {
			if item.key == key {
				bucket.items[hash] = append(items[:i], items[i+1:]...)
				if len(bucket.items[hash]) == 0 {
					delete(bucket.items, hash)
				}
				return true
			}
		}
	}

	return false
}

// PARALLEL HASHING

// ParallelHash computes hashes of multiple strings concurrently
func ParallelHash(strings []string) []int64 {
	results := make([]int64, len(strings))
	var wg sync.WaitGroup

	for i, s := range strings {
		wg.Add(1)
		go func(idx int, str string) {
			defer wg.Done()
			results[idx] = PolynomialHash(str, DefaultBase, DefaultMod)
		}(i, s)
	}

	wg.Wait()
	return results
}

// SUBSTRING HASHING

// SubstringHashes computes hashes of all substrings of a given length
func SubstringHashes(text string, length int) map[int64][]int {
	if length > len(text) {
		return make(map[int64][]int)
	}

	hashToPositions := make(map[int64][]int)

	rh := NewRollingHash(text, 0, length, DefaultBase, DefaultMod)
	hashToPositions[rh.Hash()] = []int{0}

	for rh.RollRight() {
		hash := rh.Hash()
		hashToPositions[hash] = append(hashToPositions[hash], rh.start)
	}

	return hashToPositions
}

// FindDuplicateSubstrings finds all duplicate substrings of given length
func FindDuplicateSubstrings(text string, length int) []string {
	hashToPositions := SubstringHashes(text, length)

	duplicates := make(map[string]bool)

	for _, positions := range hashToPositions {
		if len(positions) > 1 {
			substring := text[positions[0] : positions[0]+length]
			duplicates[substring] = true
		}
	}

	result := make([]string, 0, len(duplicates))
	for dup := range duplicates {
		result = append(result, dup)
	}

	return result
}

// HASH DISTRIBUTION ANALYSIS

// AnalyzeHashDistribution analyzes hash distribution
func AnalyzeHashDistribution(strings []string, buckets int) map[int]int {
	distribution := make(map[int]int)

	for _, s := range strings {
		hash := PolynomialHash(s, DefaultBase, DefaultMod)
		bucket := int(hash % int64(buckets))
		distribution[bucket]++
	}

	return distribution
}

// DemonstrateStringHashing demonstrates string hashing algorithms
func DemonstrateStringHashing() {
	fmt.Println("🔐 String Hashing Algorithms in Go")
	fmt.Println(strings.Repeat("=", 80))

	// Basic hashing
	fmt.Println("\n📋 Basic Hash Functions:")
	fmt.Println(strings.Repeat("-", 80))

	testStrings := []string{"hello", "world", "golang", "hashing", "algorithm"}

	for _, s := range testStrings {
		comp := CompareHashes(s)
		fmt.Printf("\n'%s':\n", s)
		fmt.Printf("  Polynomial: %d\n", comp.Polynomial)
		fmt.Printf("  DJB2:       %d\n", comp.DJB2)
		fmt.Printf("  SDBM:       %d\n", comp.SDBM)
		fmt.Printf("  FNV:        %d\n", comp.FNV)
		fmt.Printf("  Murmur:     %d\n", comp.Murmur)
		fmt.Printf("  SHA256:     %s...\n", comp.SHA256)
	}

	// Rolling hash and Rabin-Karp
	fmt.Println("\n\n🔄 Rolling Hash and Rabin-Karp Pattern Matching:")
	fmt.Println(strings.Repeat("-", 80))

	text := "abracadabra"
	pattern := "abra"

	fmt.Printf("Text: '%s'\n", text)
	fmt.Printf("Pattern: '%s'\n", pattern)

	matches := RabinKarp(text, pattern)
	fmt.Printf("Matches found at positions: %v\n", matches)

	// Verify matches
	for _, pos := range matches {
		fmt.Printf("  Position %d: '%s'\n", pos, text[pos:pos+len(pattern)])
	}

	// Rolling hash demonstration
	fmt.Println("\n🎯 Rolling Hash Window:")
	fmt.Println(strings.Repeat("-", 80))

	windowSize := 3
	rh := NewRollingHash(text, 0, windowSize, DefaultBase, DefaultMod)

	fmt.Printf("Text: '%s', Window size: %d\n\n", text, windowSize)
	fmt.Printf("Position  Substring  Hash\n")
	fmt.Println(strings.Repeat("-", 30))

	fmt.Printf("%-9d %-10s %d\n", 0, rh.Substring(), rh.Hash())

	pos := 1
	for rh.RollRight() {
		fmt.Printf("%-9d %-10s %d\n", pos, rh.Substring(), rh.Hash())
		pos++
	}

	// Collision detection
	fmt.Println("\n\n⚠️  Collision Detection:")
	fmt.Println(strings.Repeat("-", 80))

	detector := NewCollisionDetector()
	testWords := []string{
		"hello", "world", "test", "hash", "collision",
		"golang", "programming", "algorithm", "data", "structure",
	}

	fmt.Println("Adding strings and checking for collisions:")
	for _, word := range testWords {
		collisions := detector.Add(word)
		if collisions != nil {
			fmt.Printf("  Collision! '%s' collides with: %v\n", word, collisions)
		}
	}

	fmt.Printf("\nTotal strings: %d\n", detector.count)
	fmt.Printf("Unique hashes: %d\n", len(detector.hashes))
	fmt.Printf("Load factor: %.2f\n", detector.LoadFactor())

	allCollisions := detector.Collisions()
	if len(allCollisions) > 0 {
		fmt.Println("\nCollision groups:")
		for hash, group := range allCollisions {
			fmt.Printf("  Hash %d: %v\n", hash, group)
		}
	}

	// Duplicate substrings
	fmt.Println("\n\n🔍 Finding Duplicate Substrings:")
	fmt.Println(strings.Repeat("-", 80))

	longText := "banana band stand banana hand"
	substringLength := 3

	fmt.Printf("Text: '%s'\n", longText)
	fmt.Printf("Substring length: %d\n\n", substringLength)

	duplicates := FindDuplicateSubstrings(longText, substringLength)
	fmt.Printf("Duplicate substrings: %v\n", duplicates)

	// Thread-safe hash table
	fmt.Println("\n\n🔒 Thread-Safe Hash Table:")
	fmt.Println(strings.Repeat("-", 80))

	ht := NewThreadSafeHashTable(10)

	// Concurrent insertions
	var wg sync.WaitGroup
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(val int) {
			defer wg.Done()
			key := fmt.Sprintf("key%d", val)
			ht.Put(key, val)
		}(i)
	}

	wg.Wait()
	fmt.Println("Inserted 100 key-value pairs concurrently")

	// Retrieve some values
	testKeys := []string{"key0", "key50", "key99", "nonexistent"}
	for _, key := range testKeys {
		if val, ok := ht.Get(key); ok {
			fmt.Printf("  %s: %v\n", key, val)
		} else {
			fmt.Printf("  %s: not found\n", key)
		}
	}

	// Hash distribution analysis
	fmt.Println("\n\n📊 Hash Distribution Analysis:")
	fmt.Println(strings.Repeat("-", 80))

	numStrings := 1000
	testData := make([]string, numStrings)
	for i := 0; i < numStrings; i++ {
		testData[i] = fmt.Sprintf("string%d", i)
	}

	numBuckets := 20
	distribution := AnalyzeHashDistribution(testData, numBuckets)

	fmt.Printf("Distributed %d strings into %d buckets:\n\n", numStrings, numBuckets)

	// Calculate statistics
	min := math.MaxInt
	max := 0
	sum := 0

	for bucket := 0; bucket < numBuckets; bucket++ {
		count := distribution[bucket]
		if count < min {
			min = count
		}
		if count > max {
			max = count
		}
		sum += count
	}

	avg := float64(sum) / float64(numBuckets)

	fmt.Printf("Statistics:\n")
	fmt.Printf("  Min: %d\n", min)
	fmt.Printf("  Max: %d\n", max)
	fmt.Printf("  Avg: %.2f\n", avg)
	fmt.Printf("  Expected: %.2f\n", float64(numStrings)/float64(numBuckets))

	// Parallel hashing
	fmt.Println("\n\n🚀 Parallel Hash Computation:")
	fmt.Println(strings.Repeat("-", 80))

	largeDataset := make([]string, 10000)
	for i := 0; i < len(largeDataset); i++ {
		largeDataset[i] = fmt.Sprintf("data%d", i)
	}

	fmt.Printf("Computing hashes for %d strings in parallel...\n", len(largeDataset))

	start := big.NewInt(0)
	_ = start // Placeholder for timing

	hashes := ParallelHash(largeDataset)

	fmt.Printf("Computed %d hashes\n", len(hashes))
	fmt.Printf("Sample hashes: %v...\n", hashes[:5])
}

func main() {
	DemonstrateStringHashing()
	fmt.Println("\n✨ String hashing demonstration complete!")
}
