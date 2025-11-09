/**
 * Comprehensive Hash Table Implementation in Kotlin
 *
 * Features:
 * - Separate chaining for collision resolution
 * - Dynamic resizing with configurable load factor
 * - Generic implementation with type constraints
 * - Iterator support with Kotlin sequences
 * - Operator overloading for subscript syntax
 * - Performance statistics
 * - Data classes for clean code
 *
 * Time Complexity:
 * - Average: O(1) for insert, delete, search
 * - Worst:   O(n) for chaining with poor hash function
 *
 * Space Complexity: O(n) where n is the number of elements
 *
 * Usage:
 *   kotlinc HashTable.kt -include-runtime -d HashTable.jar
 *   java -jar HashTable.jar
 *
 * Or with kotlin script:
 *   kotlin HashTable.kt
 */

import kotlin.math.max

// ============================================================================
// HASH TABLE NODE
// ============================================================================

/**
 * Node in the linked list (chain) for collision resolution
 */
private data class HashNode<K, V>(
    val key: K,
    var value: V,
    var next: HashNode<K, V>? = null
)

// ============================================================================
// HASH TABLE STATISTICS
// ============================================================================

/**
 * Performance statistics for hash table
 */
data class HashTableStats(
    val size: Int,
    val capacity: Int,
    val loadFactor: Double,
    val collisions: Int,
    val resizes: Int,
    val maxChainLength: Int,
    val avgChainLength: Double,
    val numberOfChains: Int
)

// ============================================================================
// HASH TABLE STRUCTURE
// ============================================================================

/**
 * Hash table with separate chaining
 */
class HashTable<K : Any, V>(
    initialCapacity: Int = 16,
    private val loadFactor: Double = 0.75
) : Iterable<Pair<K, V>> {

    private var buckets: Array<HashNode<K, V>?>
    private var capacity: Int
    private var count: Int = 0

    // Statistics
    private var collisions: Int = 0
    private var resizes: Int = 0

    init {
        capacity = nextPowerOf2(initialCapacity)
        @Suppress("UNCHECKED_CAST")
        buckets = arrayOfNulls<HashNode<K, V>?>(capacity) as Array<HashNode<K, V>?>
    }

    // ========================================================================
    // UTILITY FUNCTIONS
    // ========================================================================

    companion object {
        /**
         * Get next power of 2 >= n
         */
        private fun nextPowerOf2(n: Int): Int {
            if (n <= 1) return 1
            var power = 1
            while (power < n) {
                power *= 2
            }
            return power
        }
    }

    /**
     * Compute bucket index for key
     */
    private fun hashIndex(key: K): Int {
        return (key.hashCode() and Int.MAX_VALUE) and (capacity - 1)
    }

    /**
     * Check if table should be resized
     */
    private fun shouldResize(): Boolean {
        return count.toDouble() / capacity > loadFactor
    }

    /**
     * Resize and rehash all elements
     */
    private fun resize() {
        resizes++
        val oldBuckets = buckets
        capacity *= 2

        @Suppress("UNCHECKED_CAST")
        buckets = arrayOfNulls<HashNode<K, V>?>(capacity) as Array<HashNode<K, V>?>
        count = 0
        collisions = 0

        // Rehash all entries
        for (bucket in oldBuckets) {
            var node = bucket
            while (node != null) {
                put(node.key, node.value)
                node = node.next
            }
        }
    }

    // ========================================================================
    // CORE OPERATIONS
    // ========================================================================

    /**
     * Insert or update a key-value pair
     * Returns the previous value if key existed, null otherwise
     */
    fun put(key: K, value: V): V? {
        if (shouldResize()) {
            resize()
        }

        val index = hashIndex(key)
        var node = buckets[index]

        // Search for existing key
        while (node != null) {
            if (node.key == key) {
                val oldValue = node.value
                node.value = value
                return oldValue
            }
            node = node.next
        }

        // Key not found, insert at head
        if (buckets[index] != null) {
            collisions++
        }

        val newNode = HashNode(key, value, buckets[index])
        buckets[index] = newNode
        count++

        return null
    }

    /**
     * Get value for key
     * Returns value if found, null otherwise
     */
    fun get(key: K): V? {
        val index = hashIndex(key)
        var node = buckets[index]

        while (node != null) {
            if (node.key == key) {
                return node.value
            }
            node = node.next
        }

        return null
    }

    /**
     * Remove key and return its value
     * Returns value if found, null otherwise
     */
    fun remove(key: K): V? {
        val index = hashIndex(key)
        var node = buckets[index]
        var prev: HashNode<K, V>? = null

        while (node != null) {
            if (node.key == key) {
                if (prev != null) {
                    prev.next = node.next
                } else {
                    buckets[index] = node.next
                }
                count--
                return node.value
            }
            prev = node
            node = node.next
        }

        return null
    }

    /**
     * Check if key exists
     */
    fun contains(key: K): Boolean {
        return get(key) != null
    }

    /**
     * Get number of elements
     */
    val size: Int
        get() = count

    /**
     * Check if hash table is empty
     */
    val isEmpty: Boolean
        get() = count == 0

    /**
     * Clear all elements
     */
    fun clear() {
        @Suppress("UNCHECKED_CAST")
        buckets = arrayOfNulls<HashNode<K, V>?>(capacity) as Array<HashNode<K, V>?>
        count = 0
        collisions = 0
    }

    /**
     * Get all keys
     */
    fun keys(): List<K> {
        val result = mutableListOf<K>()
        for (bucket in buckets) {
            var node = bucket
            while (node != null) {
                result.add(node.key)
                node = node.next
            }
        }
        return result
    }

    /**
     * Get all values
     */
    fun values(): List<V> {
        val result = mutableListOf<V>()
        for (bucket in buckets) {
            var node = bucket
            while (node != null) {
                result.add(node.value)
                node = node.next
            }
        }
        return result
    }

    /**
     * Get all entries as pairs
     */
    fun entries(): List<Pair<K, V>> {
        val result = mutableListOf<Pair<K, V>>()
        for (bucket in buckets) {
            var node = bucket
            while (node != null) {
                result.add(Pair(node.key, node.value))
                node = node.next
            }
        }
        return result
    }

    /**
     * Operator overloading for subscript syntax
     */
    operator fun get(key: K): V? = get(key)

    operator fun set(key: K, value: V) {
        put(key, value)
    }

    // ========================================================================
    // ITERATION
    // ========================================================================

    /**
     * Iterator for hash table
     */
    override fun iterator(): Iterator<Pair<K, V>> {
        return entries().iterator()
    }

    /**
     * For each implementation
     */
    inline fun forEach(action: (K, V) -> Unit) {
        for (bucket in buckets) {
            var node = bucket
            while (node != null) {
                action(node.key, node.value)
                node = node.next
            }
        }
    }

    // ========================================================================
    // STATISTICS
    // ========================================================================

    /**
     * Get performance statistics
     */
    fun stats(): HashTableStats {
        var maxChain = 0
        var totalChainLength = 0
        var numChains = 0

        for (bucket in buckets) {
            var chainLength = 0
            var node = bucket

            while (node != null) {
                chainLength++
                node = node.next
            }

            if (chainLength > 0) {
                numChains++
                totalChainLength += chainLength
                maxChain = max(maxChain, chainLength)
            }
        }

        val avgChainLength = if (numChains > 0) {
            totalChainLength.toDouble() / numChains
        } else {
            0.0
        }

        return HashTableStats(
            size = count,
            capacity = capacity,
            loadFactor = count.toDouble() / capacity,
            collisions = collisions,
            resizes = resizes,
            maxChainLength = maxChain,
            avgChainLength = avgChainLength,
            numberOfChains = numChains
        )
    }

    /**
     * Print statistics
     */
    fun printStats() {
        val stats = stats()
        println("Hash Table Statistics:")
        println("  Size:              ${stats.size}")
        println("  Capacity:          ${stats.capacity}")
        println("  Load Factor:       ${"%.2f".format(stats.loadFactor)} / ${"%.2f".format(loadFactor)}")
        println("  Collisions:        ${stats.collisions}")
        println("  Resizes:           ${stats.resizes}")
        println("  Max Chain Length:  ${stats.maxChainLength}")
        println("  Avg Chain Length:  ${"%.2f".format(stats.avgChainLength)}")
        println("  Number of Chains:  ${stats.numberOfChains}")
    }

    /**
     * String representation
     */
    override fun toString(): String {
        val entries = entries().take(10).joinToString(", ") { "${it.first}: ${it.second}" }
        val more = if (count > 10) ", ... and ${count - 10} more" else ""
        return "HashTable($entries$more)"
    }
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

fun main() {
    println("===========================================")
    println("Hash Table Implementation in Kotlin")
    println("===========================================")
    println()

    // Create hash table
    val ht = HashTable<String, Int>(initialCapacity = 16)

    println("1. Inserting elements...")
    println("-----------------------------------------")

    // Insert some data
    for (i in 0 until 10) {
        val key = "key$i"
        val value = i * 10
        ht.put(key, value)
        println("  Inserted: $key -> $value")
    }
    println("\nSize: ${ht.size}\n")

    println("2. Retrieving elements...")
    println("-----------------------------------------")

    val testKeys = listOf("key0", "key5", "key9", "nonexistent")
    for (key in testKeys) {
        val value = ht.get(key)
        if (value != null) {
            println("  Get '$key': $value")
        } else {
            println("  Get '$key': Not found")
        }
    }

    println("\n3. Testing subscript syntax...")
    println("-----------------------------------------")
    println("  ht[\"key3\"] = ${ht["key3"]}")
    ht["key3"] = 333
    println("  After ht[\"key3\"] = 333: ${ht["key3"]}")

    println("\n4. Testing containment...")
    println("-----------------------------------------")
    println("  Contains 'key3': ${ht.contains("key3")}")
    println("  Contains 'missing': ${ht.contains("missing")}")

    println("\n5. Updating values...")
    println("-----------------------------------------")

    val oldValue = ht.put("key5", 999)
    if (oldValue != null) {
        println("  Updated 'key5': old value = $oldValue, new value = 999")
    }

    println("\n6. Removing elements...")
    println("-----------------------------------------")

    val removed = ht.remove("key7")
    if (removed != null) {
        println("  Removed 'key7': $removed")
    }
    println("  Size after removal: ${ht.size}")

    println("\n7. Iterating over elements...")
    println("-----------------------------------------")
    var itemCount = 0
    for ((key, value) in ht) {
        if (itemCount < 5) {
            println("  $key: $value")
        }
        itemCount++
    }
    if (itemCount > 5) {
        println("  ... and ${itemCount - 5} more elements")
    }

    println("\n8. Using forEach...")
    println("-----------------------------------------")
    var count = 0
    ht.forEach { key, value ->
        if (count < 3) {
            println("  $key -> $value")
        }
        count++
    }

    println("\n9. Performance Statistics")
    println("-----------------------------------------")
    ht.printStats()

    println("\n10. Testing with many elements...")
    println("-----------------------------------------")

    // Insert many elements to trigger resizing
    for (i in 100 until 200) {
        val key = "item$i"
        ht[key] = i
    }

    println("  Added 100 more elements")
    println("  New size: ${ht.size}")
    println()
    ht.printStats()

    println("\n11. Testing keys() and values()...")
    println("-----------------------------------------")
    val keys = ht.keys()
    val values = ht.values()
    println("  Total keys: ${keys.size}")
    println("  Total values: ${values.size}")
    println("  First 5 keys: ${keys.take(5)}")

    println("\n12. Testing with integer keys...")
    println("-----------------------------------------")

    val intTable = HashTable<Int, String>(initialCapacity = 8)
    for (i in 1..5) {
        intTable[i] = "value$i"
    }

    val val3 = intTable[3]
    if (val3 != null) {
        println("  intTable[3] = $val3")
    }

    println("\n13. Testing data classes as keys...")
    println("-----------------------------------------")

    data class Person(val name: String, val age: Int)

    val personTable = HashTable<Person, String>()
    val alice = Person("Alice", 30)
    val bob = Person("Bob", 25)

    personTable[alice] = "Engineer"
    personTable[bob] = "Designer"

    println("  personTable[alice] = ${personTable[alice]}")
    println("  personTable[bob] = ${personTable[bob]}")

    println("\n14. Clearing hash table...")
    println("-----------------------------------------")
    ht.clear()
    println("  Size after clear: ${ht.size}")
    println("  Is empty: ${ht.isEmpty}")

    println("\n===========================================")
    println("✨ Hash table demonstration complete!")
    println("===========================================")
}
