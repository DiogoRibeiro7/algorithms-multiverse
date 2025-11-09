/**
 * Comprehensive Hash Table Implementation in Swift
 *
 * Features:
 * - Separate chaining for collision resolution
 * - Dynamic resizing with configurable load factor
 * - Generic implementation with protocol constraints
 * - Sequence protocol conformance for iteration
 * - Performance statistics
 * - Subscript syntax support
 *
 * Time Complexity:
 * - Average: O(1) for insert, delete, search
 * - Worst:   O(n) for chaining with poor hash function
 *
 * Space Complexity: O(n) where n is the number of elements
 *
 * Usage:
 *   swift hashtable.swift
 *
 * Or compile:
 *   swiftc hashtable.swift -o hashtable
 *   ./hashtable
 */

import Foundation

// ============================================================================
// HASH TABLE NODE
// ============================================================================

/// Node in the linked list (chain) for collision resolution
private class HashNode<Key: Hashable, Value> {
    var key: Key
    var value: Value
    var next: HashNode?

    init(key: Key, value: Value) {
        self.key = key
        self.value = value
        self.next = nil
    }
}

// ============================================================================
// HASH TABLE STATISTICS
// ============================================================================

/// Performance statistics for hash table
struct HashTableStats {
    let size: Int
    let capacity: Int
    let loadFactor: Double
    let collisions: Int
    let resizes: Int
    let maxChainLength: Int
    let avgChainLength: Double
    let numberOfChains: Int
}

// ============================================================================
// HASH TABLE STRUCTURE
// ============================================================================

/// Hash table with separate chaining
class HashTable<Key: Hashable, Value> {
    private var buckets: [HashNode<Key, Value>?]
    private var capacity: Int
    private var count: Int
    private let loadFactor: Double

    // Statistics
    private var collisions: Int
    private var resizes: Int

    // ========================================================================
    // INITIALIZATION
    // ========================================================================

    /// Create hash table with initial capacity
    init(initialCapacity: Int = 16, loadFactor: Double = 0.75) {
        self.capacity = Self.nextPowerOf2(initialCapacity)
        self.count = 0
        self.loadFactor = loadFactor
        self.collisions = 0
        self.resizes = 0
        self.buckets = Array(repeating: nil, count: self.capacity)
    }

    /// Get next power of 2 >= n
    private static func nextPowerOf2(_ n: Int) -> Int {
        guard n > 1 else { return 1 }
        var power = 1
        while power < n {
            power *= 2
        }
        return power
    }

    // ========================================================================
    // HASH FUNCTIONS
    // ========================================================================

    /// Compute bucket index for key
    private func hashIndex(for key: Key) -> Int {
        var hasher = Hasher()
        key.hash(into: &hasher)
        let hashValue = abs(hasher.finalize())
        return hashValue & (capacity - 1)
    }

    /// Check if table should be resized
    private func shouldResize() -> Bool {
        return Double(count) / Double(capacity) > loadFactor
    }

    /// Resize and rehash all elements
    private func resize() {
        resizes += 1
        let oldBuckets = buckets
        capacity *= 2
        buckets = Array(repeating: nil, count: capacity)
        count = 0
        collisions = 0

        // Rehash all entries
        for bucket in oldBuckets {
            var node = bucket
            while let current = node {
                self[current.key] = current.value
                node = current.next
            }
        }
    }

    // ========================================================================
    // CORE OPERATIONS
    // ========================================================================

    /// Insert or update a key-value pair
    /// Returns the previous value if key existed
    @discardableResult
    func put(_ key: Key, _ value: Value) -> Value? {
        if shouldResize() {
            resize()
        }

        let index = hashIndex(for: key)
        var node = buckets[index]

        // Search for existing key
        while let current = node {
            if current.key == key {
                let oldValue = current.value
                current.value = value
                return oldValue
            }
            node = current.next
        }

        // Key not found, insert at head
        if buckets[index] != nil {
            collisions += 1
        }

        let newNode = HashNode(key: key, value: value)
        newNode.next = buckets[index]
        buckets[index] = newNode
        count += 1

        return nil
    }

    /// Get value for key
    func get(_ key: Key) -> Value? {
        let index = hashIndex(for: key)
        var node = buckets[index]

        while let current = node {
            if current.key == key {
                return current.value
            }
            node = current.next
        }

        return nil
    }

    /// Remove key and return its value
    @discardableResult
    func remove(_ key: Key) -> Value? {
        let index = hashIndex(for: key)
        var node = buckets[index]
        var prev: HashNode<Key, Value>? = nil

        while let current = node {
            if current.key == key {
                if let previous = prev {
                    previous.next = current.next
                } else {
                    buckets[index] = current.next
                }
                count -= 1
                return current.value
            }
            prev = current
            node = current.next
        }

        return nil
    }

    /// Check if key exists
    func contains(_ key: Key) -> Bool {
        return get(key) != nil
    }

    /// Get number of elements
    var size: Int {
        return count
    }

    /// Check if hash table is empty
    var isEmpty: Bool {
        return count == 0
    }

    /// Clear all elements
    func clear() {
        buckets = Array(repeating: nil, count: capacity)
        count = 0
        collisions = 0
    }

    /// Get all keys
    func keys() -> [Key] {
        var result: [Key] = []
        for bucket in buckets {
            var node = bucket
            while let current = node {
                result.append(current.key)
                node = current.next
            }
        }
        return result
    }

    /// Get all values
    func values() -> [Value] {
        var result: [Value] = []
        for bucket in buckets {
            var node = bucket
            while let current = node {
                result.append(current.value)
                node = current.next
            }
        }
        return result
    }

    /// Subscript syntax support
    subscript(key: Key) -> Value? {
        get {
            return get(key)
        }
        set {
            if let value = newValue {
                put(key, value)
            } else {
                remove(key)
            }
        }
    }

    // ========================================================================
    // STATISTICS
    // ========================================================================

    /// Get performance statistics
    func stats() -> HashTableStats {
        var maxChain = 0
        var totalChainLength = 0
        var numChains = 0

        for bucket in buckets {
            var chainLength = 0
            var node = bucket

            while let current = node {
                chainLength += 1
                node = current.next
            }

            if chainLength > 0 {
                numChains += 1
                totalChainLength += chainLength
                maxChain = max(maxChain, chainLength)
            }
        }

        let avgChainLength = numChains > 0 ? Double(totalChainLength) / Double(numChains) : 0.0

        return HashTableStats(
            size: count,
            capacity: capacity,
            loadFactor: Double(count) / Double(capacity),
            collisions: collisions,
            resizes: resizes,
            maxChainLength: maxChain,
            avgChainLength: avgChainLength,
            numberOfChains: numChains
        )
    }

    /// Print statistics
    func printStats() {
        let stats = self.stats()
        print("Hash Table Statistics:")
        print("  Size:              \(stats.size)")
        print("  Capacity:          \(stats.capacity)")
        print(String(format: "  Load Factor:       %.2f / %.2f", stats.loadFactor, loadFactor))
        print("  Collisions:        \(stats.collisions)")
        print("  Resizes:           \(stats.resizes)")
        print("  Max Chain Length:  \(stats.maxChainLength)")
        print(String(format: "  Avg Chain Length:  %.2f", stats.avgChainLength))
        print("  Number of Chains:  \(stats.numberOfChains)")
    }
}

// ============================================================================
// SEQUENCE PROTOCOL CONFORMANCE
// ============================================================================

extension HashTable: Sequence {
    /// Iterator for hash table
    func makeIterator() -> HashTableIterator<Key, Value> {
        return HashTableIterator(buckets: buckets)
    }
}

/// Iterator for hash table
struct HashTableIterator<Key: Hashable, Value>: IteratorProtocol {
    private let buckets: [HashNode<Key, Value>?]
    private var bucketIndex = 0
    private var currentNode: HashNode<Key, Value>?

    init(buckets: [HashNode<Key, Value>?]) {
        self.buckets = buckets
        advanceToNextNode()
    }

    private mutating func advanceToNextNode() {
        while bucketIndex < buckets.count {
            if let node = currentNode?.next {
                currentNode = node
                return
            }

            if let bucket = buckets[bucketIndex] {
                currentNode = bucket
                bucketIndex += 1
                return
            }

            bucketIndex += 1
        }
        currentNode = nil
    }

    mutating func next() -> (Key, Value)? {
        guard let node = currentNode else { return nil }
        let result = (node.key, node.value)
        advanceToNextNode()
        return result
    }
}

// ============================================================================
// CUSTOM STRING CONVERTIBLE
// ============================================================================

extension HashTable: CustomStringConvertible where Key: CustomStringConvertible, Value: CustomStringConvertible {
    var description: String {
        var result = "HashTable(["
        let items = self.map { "\($0.0): \($0.1)" }
        result += items.joined(separator: ", ")
        result += "])"
        return result
    }
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

func main() {
    print("===========================================")
    print("Hash Table Implementation in Swift")
    print("===========================================")
    print()

    // Create hash table
    let ht = HashTable<String, Int>(initialCapacity: 16)

    print("1. Inserting elements...")
    print("-----------------------------------------")

    // Insert some data
    for i in 0..<10 {
        let key = "key\(i)"
        let value = i * 10
        ht.put(key, value)
        print("  Inserted: \(key) -> \(value)")
    }
    print("\nSize: \(ht.size)\n")

    print("2. Retrieving elements...")
    print("-----------------------------------------")

    let testKeys = ["key0", "key5", "key9", "nonexistent"]
    for key in testKeys {
        if let value = ht.get(key) {
            print("  Get '\(key)': \(value)")
        } else {
            print("  Get '\(key)': Not found")
        }
    }

    print("\n3. Testing subscript syntax...")
    print("-----------------------------------------")
    print("  ht[\"key3\"] = \(ht["key3"] ?? -1)")
    ht["key3"] = 333
    print("  After ht[\"key3\"] = 333: \(ht["key3"] ?? -1)")

    print("\n4. Testing containment...")
    print("-----------------------------------------")
    print("  Contains 'key3': \(ht.contains("key3"))")
    print("  Contains 'missing': \(ht.contains("missing"))")

    print("\n5. Updating values...")
    print("-----------------------------------------")

    if let oldValue = ht.put("key5", 999) {
        print("  Updated 'key5': old value = \(oldValue), new value = 999")
    }

    print("\n6. Removing elements...")
    print("-----------------------------------------")

    if let removed = ht.remove("key7") {
        print("  Removed 'key7': \(removed)")
    }
    print("  Size after removal: \(ht.size)")

    print("\n7. Iterating over elements...")
    print("-----------------------------------------")
    var itemCount = 0
    for (key, value) in ht {
        if itemCount < 5 {
            print("  \(key): \(value)")
        }
        itemCount += 1
    }
    if itemCount > 5 {
        print("  ... and \(itemCount - 5) more elements")
    }

    print("\n8. Performance Statistics")
    print("-----------------------------------------")
    ht.printStats()

    print("\n9. Testing with many elements...")
    print("-----------------------------------------")

    // Insert many elements to trigger resizing
    for i in 100..<200 {
        let key = "item\(i)"
        ht.put(key, i)
    }

    print("  Added 100 more elements")
    print("  New size: \(ht.size)")
    print()
    ht.printStats()

    print("\n10. Testing keys() and values()...")
    print("-----------------------------------------")
    let keys = ht.keys()
    let values = ht.values()
    print("  Total keys: \(keys.count)")
    print("  Total values: \(values.count)")
    print("  First 5 keys: \(Array(keys.prefix(5)))")

    print("\n11. Testing with integer keys...")
    print("-----------------------------------------")

    let intTable = HashTable<Int, String>(initialCapacity: 8)
    for i in 1...5 {
        intTable[i] = "value\(i)"
    }

    if let val = intTable[3] {
        print("  intTable[3] = \(val)")
    }

    print("\n12. Clearing hash table...")
    print("-----------------------------------------")
    ht.clear()
    print("  Size after clear: \(ht.size)")
    print("  Is empty: \(ht.isEmpty)")

    print("\n===========================================")
    print("✨ Hash table demonstration complete!")
    print("===========================================")
}

// Run the demonstration
main()
