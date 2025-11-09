/**
 * Comprehensive Hash Table Implementation with Advanced Features (JavaScript/ES6+)
 *
 * Features:
 * - Multiple collision resolution strategies
 * - Dynamic resizing with load factor management
 * - Custom hash functions
 * - Iterator support (Symbol.iterator)
 * - Serialization/deserialization
 * - Consistent hashing for distributed systems
 * - Performance benchmarking
 *
 * Time Complexity:
 * - Average: O(1) for insert, delete, search
 * - Worst:   O(n) for chaining with poor hash function
 *
 * Space Complexity: O(n) where n is the number of elements
 */

// ============================================================================
// HASH FUNCTIONS
// ============================================================================

class HashFunction {
    /**
     * Collection of hash functions for different use cases.
     */

    /**
     * DJB2 hash function - classic string hashing.
     * Formula: hash = hash * 33 + char
     */
    static djb2(key) {
        let hash = 5381;
        const str = String(key);
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) + hash) + str.charCodeAt(i);
            hash = hash & 0xFFFFFFFF; // Keep 32-bit
        }
        return hash >>> 0; // Convert to unsigned
    }

    /**
     * FNV-1a hash function - excellent distribution.
     * Used in many production systems.
     */
    static fnv1a(key) {
        const FNV_PRIME = 0x01000193;
        const FNV_OFFSET = 0x811C9DC5;

        let hash = FNV_OFFSET;
        const str = String(key);

        for (let i = 0; i < str.length; i++) {
            hash ^= str.charCodeAt(i);
            hash = Math.imul(hash, FNV_PRIME);
            hash = hash >>> 0; // Keep unsigned 32-bit
        }

        return hash;
    }

    /**
     * Simplified MurmurHash3 - very fast with good distribution.
     */
    static murmur3(key, seed = 0) {
        const str = String(key);
        let h1 = seed;
        const c1 = 0xcc9e2d51;
        const c2 = 0x1b873593;

        for (let i = 0; i < str.length; i++) {
            let k1 = str.charCodeAt(i);
            k1 = Math.imul(k1, c1);
            k1 = (k1 << 15) | (k1 >>> 17);
            k1 = Math.imul(k1, c2);

            h1 ^= k1;
            h1 = (h1 << 13) | (h1 >>> 19);
            h1 = Math.imul(h1, 5) + 0xe6546b64;
        }

        h1 ^= str.length;
        h1 ^= h1 >>> 16;
        h1 = Math.imul(h1, 0x85ebca6b);
        h1 ^= h1 >>> 13;
        h1 = Math.imul(h1, 0xc2b2ae35);
        h1 ^= h1 >>> 16;

        return h1 >>> 0;
    }

    /**
     * Polynomial rolling hash - good for string matching.
     */
    static polynomialRolling(key, base = 31) {
        let hash = 0;
        const str = String(key);

        for (let i = 0; i < str.length; i++) {
            hash = (hash * base + str.charCodeAt(i)) >>> 0;
        }

        return hash;
    }
}

// ============================================================================
// SEPARATE CHAINING HASH TABLE
// ============================================================================

class ChainingHashTable {
    /**
     * Hash table using separate chaining for collision resolution.
     *
     * Collision Resolution: Each bucket contains a linked list of entries
     *
     * Advantages:
     * - Simple implementation
     * - Never fills up (only slows down)
     * - Deletion is straightforward
     *
     * Disadvantages:
     * - Extra memory for pointers
     * - Poor cache locality
     * - Performance degrades with long chains
     */

    constructor(initialCapacity = 16, loadFactor = 0.75, hashFunc = null) {
        this.capacity = this._nextPowerOf2(initialCapacity);
        this.size = 0;
        this.loadFactor = loadFactor;
        this.buckets = new Array(this.capacity).fill(null);
        this.hashFunc = hashFunc || HashFunction.fnv1a;

        // Statistics
        this.collisions = 0;
        this.resizes = 0;
    }

    /**
     * Node in the chain (linked list).
     */
    static Node = class {
        constructor(key, value) {
            this.key = key;
            this.value = value;
            this.next = null;
        }
    };

    _nextPowerOf2(n) {
        if (n <= 1) return 1;
        return 1 << (32 - Math.clz32(n - 1));
    }

    _hash(key) {
        return this.hashFunc(key) & (this.capacity - 1);
    }

    _shouldResize() {
        return this.size / this.capacity > this.loadFactor;
    }

    _resize() {
        this.resizes++;
        const oldBuckets = this.buckets;
        this.capacity *= 2;
        this.buckets = new Array(this.capacity).fill(null);
        this.size = 0;

        // Rehash all entries
        for (const bucket of oldBuckets) {
            let node = bucket;
            while (node) {
                this.put(node.key, node.value);
                node = node.next;
            }
        }
    }

    /**
     * Insert or update key-value pair.
     * @returns Previous value if key existed, undefined otherwise
     */
    put(key, value) {
        if (this._shouldResize()) {
            this._resize();
        }

        const index = this._hash(key);
        let node = this.buckets[index];

        // Search for existing key
        while (node) {
            if (node.key === key) {
                const oldValue = node.value;
                node.value = value;
                return oldValue;
            }
            node = node.next;
        }

        // Key not found, insert at head
        if (this.buckets[index] !== null) {
            this.collisions++;
        }

        const newNode = new ChainingHashTable.Node(key, value);
        newNode.next = this.buckets[index];
        this.buckets[index] = newNode;
        this.size++;
        return undefined;
    }

    /**
     * Retrieve value for key.
     */
    get(key) {
        const index = this._hash(key);
        let node = this.buckets[index];

        while (node) {
            if (node.key === key) {
                return node.value;
            }
            node = node.next;
        }

        return undefined;
    }

    /**
     * Remove key and return its value.
     */
    remove(key) {
        const index = this._hash(key);
        let node = this.buckets[index];
        let prev = null;

        while (node) {
            if (node.key === key) {
                if (prev) {
                    prev.next = node.next;
                } else {
                    this.buckets[index] = node.next;
                }
                this.size--;
                return node.value;
            }
            prev = node;
            node = node.next;
        }

        return undefined;
    }

    /**
     * Check if key exists.
     */
    has(key) {
        return this.get(key) !== undefined;
    }

    /**
     * Clear all elements.
     */
    clear() {
        this.buckets = new Array(this.capacity).fill(null);
        this.size = 0;
    }

    /**
     * Iterator support - enables for...of loops
     */
    *[Symbol.iterator]() {
        for (const bucket of this.buckets) {
            let node = bucket;
            while (node) {
                yield [node.key, node.value];
                node = node.next;
            }
        }
    }

    /**
     * Iterate over keys.
     */
    *keys() {
        for (const [key] of this) {
            yield key;
        }
    }

    /**
     * Iterate over values.
     */
    *values() {
        for (const [, value] of this) {
            yield value;
        }
    }

    /**
     * Iterate over key-value pairs.
     */
    *entries() {
        yield* this;
    }

    /**
     * Get performance statistics.
     */
    getStats() {
        const chainLengths = [];
        for (const bucket of this.buckets) {
            let length = 0;
            let node = bucket;
            while (node) {
                length++;
                node = node.next;
            }
            if (length > 0) {
                chainLengths.push(length);
            }
        }

        return {
            size: this.size,
            capacity: this.capacity,
            loadFactor: this.capacity > 0 ? this.size / this.capacity : 0,
            collisions: this.collisions,
            resizes: this.resizes,
            maxChainLength: chainLengths.length > 0 ? Math.max(...chainLengths) : 0,
            avgChainLength: chainLengths.length > 0 ?
                chainLengths.reduce((a, b) => a + b, 0) / chainLengths.length : 0,
            numChains: chainLengths.length
        };
    }

    /**
     * Serialize to JSON.
     */
    toJSON() {
        return Array.from(this);
    }

    /**
     * Deserialize from JSON.
     */
    static fromJSON(data) {
        const table = new ChainingHashTable();
        for (const [key, value] of data) {
            table.put(key, value);
        }
        return table;
    }
}

// ============================================================================
// OPEN ADDRESSING HASH TABLE (Linear Probing)
// ============================================================================

class OpenAddressingHashTable {
    /**
     * Hash table using open addressing with linear probing.
     *
     * Collision Resolution: Store all entries in the table array itself
     * When collision occurs, probe linearly: (hash + i) % capacity
     *
     * Advantages:
     * - Better cache locality
     * - No extra memory for pointers
     * - Simple implementation
     *
     * Disadvantages:
     * - Clustering can occur
     * - Must handle deletions carefully (tombstones)
     * - Can fill up (needs resizing before full)
     */

    constructor(initialCapacity = 16, loadFactor = 0.7, hashFunc = null) {
        this.capacity = this._nextPowerOf2(initialCapacity);
        this.size = 0;
        this.deletedCount = 0;
        this.loadFactor = loadFactor;
        this.table = new Array(this.capacity).fill(null);
        this.hashFunc = hashFunc || HashFunction.fnv1a;

        // Statistics
        this.probes = 0;
        this.resizes = 0;
    }

    static Entry = class {
        constructor(key, value) {
            this.key = key;
            this.value = value;
            this.isDeleted = false;
        }
    };

    _nextPowerOf2(n) {
        if (n <= 1) return 1;
        return 1 << (32 - Math.clz32(n - 1));
    }

    _hash(key) {
        return this.hashFunc(key) & (this.capacity - 1);
    }

    _shouldResize() {
        return (this.size + this.deletedCount) / this.capacity > this.loadFactor;
    }

    _resize() {
        this.resizes++;
        const oldTable = this.table;
        this.capacity *= 2;
        this.table = new Array(this.capacity).fill(null);
        this.size = 0;
        this.deletedCount = 0;

        // Rehash non-deleted entries
        for (const entry of oldTable) {
            if (entry && !entry.isDeleted) {
                this.put(entry.key, entry.value);
            }
        }
    }

    _findSlot(key) {
        const index = this._hash(key);
        let firstDeleted = -1;

        for (let i = 0; i < this.capacity; i++) {
            const probeIndex = (index + i) & (this.capacity - 1);
            this.probes++;

            const entry = this.table[probeIndex];

            if (entry === null) {
                return {
                    index: firstDeleted !== -1 ? firstDeleted : probeIndex,
                    found: false
                };
            }

            if (entry.isDeleted) {
                if (firstDeleted === -1) {
                    firstDeleted = probeIndex;
                }
            } else if (entry.key === key) {
                return { index: probeIndex, found: true };
            }
        }

        return { index: firstDeleted !== -1 ? firstDeleted : -1, found: false };
    }

    put(key, value) {
        if (this._shouldResize()) {
            this._resize();
        }

        const { index, found } = this._findSlot(key);

        if (index === -1) {
            throw new Error('Hash table is full');
        }

        let oldValue;
        if (found) {
            oldValue = this.table[index].value;
            this.table[index].value = value;
        } else {
            if (this.table[index] && this.table[index].isDeleted) {
                this.deletedCount--;
            }
            this.table[index] = new OpenAddressingHashTable.Entry(key, value);
            this.size++;
        }

        return oldValue;
    }

    get(key) {
        const { index, found } = this._findSlot(key);
        return found ? this.table[index].value : undefined;
    }

    remove(key) {
        const { index, found } = this._findSlot(key);
        if (found) {
            const value = this.table[index].value;
            this.table[index].isDeleted = true;
            this.size--;
            this.deletedCount++;
            return value;
        }
        return undefined;
    }

    has(key) {
        const { found } = this._findSlot(key);
        return found;
    }

    *[Symbol.iterator]() {
        for (const entry of this.table) {
            if (entry && !entry.isDeleted) {
                yield [entry.key, entry.value];
            }
        }
    }

    getStats() {
        return {
            size: this.size,
            capacity: this.capacity,
            deletedCount: this.deletedCount,
            loadFactor: this.capacity > 0 ? this.size / this.capacity : 0,
            totalProbes: this.probes,
            avgProbes: this.size > 0 ? this.probes / this.size : 0,
            resizes: this.resizes
        };
    }
}

// ============================================================================
// ROBIN HOOD HASHING
// ============================================================================

class RobinHoodHashTable {
    /**
     * Hash table using Robin Hood hashing.
     *
     * Key Idea: "Rob from the rich, give to the poor"
     * - Track probe sequence length (PSL) for each element
     * - When inserting, swap with elements that have lower PSL
     * - Results in more uniform distribution
     */

    constructor(initialCapacity = 16, loadFactor = 0.9, hashFunc = null) {
        this.capacity = this._nextPowerOf2(initialCapacity);
        this.size = 0;
        this.loadFactor = loadFactor;
        this.table = new Array(this.capacity).fill(null);
        this.hashFunc = hashFunc || HashFunction.fnv1a;

        // Statistics
        this.maxPsl = 0;
        this.totalPsl = 0;
        this.resizes = 0;
    }

    static Entry = class {
        constructor(key, value, psl = 0) {
            this.key = key;
            this.value = value;
            this.psl = psl;
            this.isDeleted = false;
        }
    };

    _nextPowerOf2(n) {
        if (n <= 1) return 1;
        return 1 << (32 - Math.clz32(n - 1));
    }

    _hash(key) {
        return this.hashFunc(key) & (this.capacity - 1);
    }

    _shouldResize() {
        return this.size / this.capacity > this.loadFactor;
    }

    _resize() {
        this.resizes++;
        const oldTable = this.table;
        this.capacity *= 2;
        this.table = new Array(this.capacity).fill(null);
        this.size = 0;
        this.maxPsl = 0;
        this.totalPsl = 0;

        for (const entry of oldTable) {
            if (entry && !entry.isDeleted) {
                this.put(entry.key, entry.value);
            }
        }
    }

    put(key, value) {
        if (this._shouldResize()) {
            this._resize();
        }

        const index = this._hash(key);
        let entry = new RobinHoodHashTable.Entry(key, value, 0);

        for (let i = 0; i < this.capacity; i++) {
            const probeIndex = (index + i) & (this.capacity - 1);
            const existing = this.table[probeIndex];

            if (existing === null || existing.isDeleted) {
                this.table[probeIndex] = entry;
                this.size++;
                this.totalPsl += entry.psl;
                this.maxPsl = Math.max(this.maxPsl, entry.psl);
                return undefined;
            }

            if (existing.key === key) {
                const oldValue = existing.value;
                existing.value = value;
                return oldValue;
            }

            // Robin Hood: swap if we've traveled further
            if (entry.psl > existing.psl) {
                [entry, this.table[probeIndex]] = [existing, entry];
            }

            entry.psl++;
        }

        throw new Error('Hash table is full');
    }

    get(key) {
        const index = this._hash(key);
        let psl = 0;

        for (let i = 0; i < this.capacity; i++) {
            const probeIndex = (index + i) & (this.capacity - 1);
            const entry = this.table[probeIndex];

            if (entry === null) {
                return undefined;
            }

            if (!entry.isDeleted && entry.key === key) {
                return entry.value;
            }

            // Early termination
            if (!entry.isDeleted && psl > entry.psl) {
                return undefined;
            }

            psl++;
        }

        return undefined;
    }

    remove(key) {
        const index = this._hash(key);

        for (let i = 0; i < this.capacity; i++) {
            const probeIndex = (index + i) & (this.capacity - 1);
            const entry = this.table[probeIndex];

            if (entry === null) {
                return undefined;
            }

            if (!entry.isDeleted && entry.key === key) {
                const value = entry.value;
                entry.isDeleted = true;
                this.size--;
                return value;
            }
        }

        return undefined;
    }

    *[Symbol.iterator]() {
        for (const entry of this.table) {
            if (entry && !entry.isDeleted) {
                yield [entry.key, entry.value];
            }
        }
    }

    getStats() {
        return {
            size: this.size,
            capacity: this.capacity,
            loadFactor: this.capacity > 0 ? this.size / this.capacity : 0,
            maxPsl: this.maxPsl,
            avgPsl: this.size > 0 ? this.totalPsl / this.size : 0,
            resizes: this.resizes
        };
    }
}

// ============================================================================
// CONSISTENT HASHING
// ============================================================================

class ConsistentHashRing {
    /**
     * Consistent Hashing for distributed systems.
     *
     * Use Case: Distribute keys across nodes with minimal redistribution
     * when nodes are added/removed.
     */

    constructor(nodes = [], virtualNodes = 150) {
        this.virtualNodes = virtualNodes;
        this.ring = new Map(); // hash -> node
        this.sortedKeys = [];
        this.nodes = new Set();

        for (const node of nodes) {
            this.addNode(node);
        }
    }

    _hash(key) {
        // Use simple hash for demonstration
        return HashFunction.murmur3(key);
    }

    addNode(node) {
        this.nodes.add(node);
        for (let i = 0; i < this.virtualNodes; i++) {
            const virtualKey = `${node}:${i}`;
            const hashVal = this._hash(virtualKey);
            this.ring.set(hashVal, node);
        }
        this.sortedKeys = Array.from(this.ring.keys()).sort((a, b) => a - b);
    }

    removeNode(node) {
        this.nodes.delete(node);
        const keysToRemove = [];
        for (const [k, v] of this.ring) {
            if (v === node) {
                keysToRemove.push(k);
            }
        }
        for (const key of keysToRemove) {
            this.ring.delete(key);
        }
        this.sortedKeys = Array.from(this.ring.keys()).sort((a, b) => a - b);
    }

    getNode(key) {
        if (this.ring.size === 0) {
            return null;
        }

        const hashVal = this._hash(key);
        const idx = this._binarySearchNext(hashVal);
        return this.ring.get(this.sortedKeys[idx]);
    }

    _binarySearchNext(hashVal) {
        if (hashVal > this.sortedKeys[this.sortedKeys.length - 1]) {
            return 0; // Wrap around
        }

        let left = 0, right = this.sortedKeys.length - 1;
        while (left < right) {
            const mid = Math.floor((left + right) / 2);
            if (this.sortedKeys[mid] < hashVal) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        return left;
    }

    getDistribution(keys) {
        const distribution = {};
        for (const node of this.nodes) {
            distribution[node] = 0;
        }
        for (const key of keys) {
            const node = this.getNode(key);
            if (node) {
                distribution[node]++;
            }
        }
        return distribution;
    }
}

// ============================================================================
// PERFORMANCE BENCHMARKING
// ============================================================================

function benchmarkHashTables() {
    console.log('='.repeat(80));
    console.log('HASH TABLE PERFORMANCE BENCHMARK');
    console.log('='.repeat(80));

    const sizes = [100, 1000, 10000, 50000];
    const implementations = {
        'Chaining': ChainingHashTable,
        'Open Addressing': OpenAddressingHashTable,
        'Robin Hood': RobinHoodHashTable
    };

    const results = {};
    for (const name of Object.keys(implementations)) {
        results[name] = { insert: [], lookup: [], delete: [] };
    }

    for (const size of sizes) {
        console.log(`\nBenchmarking with ${size} elements...`);

        // Generate test data
        const keys = Array.from({ length: size }, (_, i) => `key_${i}`);
        const values = Array.from({ length: size }, (_, i) => i);

        for (const [name, TableClass] of Object.entries(implementations)) {
            const table = new TableClass();

            // Benchmark insertion
            const insertStart = performance.now();
            for (let i = 0; i < keys.length; i++) {
                table.put(keys[i], values[i]);
            }
            const insertTime = (performance.now() - insertStart) / 1000;
            results[name].insert.push(insertTime);

            // Benchmark lookup
            const lookupStart = performance.now();
            for (const k of keys) {
                table.get(k);
            }
            const lookupTime = (performance.now() - lookupStart) / 1000;
            results[name].lookup.push(lookupTime);

            // Benchmark deletion
            const deleteStart = performance.now();
            for (let i = 0; i < keys.length / 2; i++) {
                table.remove(keys[i]);
            }
            const deleteTime = (performance.now() - deleteStart) / 1000;
            results[name].delete.push(deleteTime);

            console.log(`${name.padEnd(20)} - Insert: ${insertTime.toFixed(4)}s, ` +
                       `Lookup: ${lookupTime.toFixed(4)}s, Delete: ${deleteTime.toFixed(4)}s`);
        }
    }

    return results;
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        HashFunction,
        ChainingHashTable,
        OpenAddressingHashTable,
        RobinHoodHashTable,
        ConsistentHashRing,
        benchmarkHashTables
    };
}

// Run demo if executed directly
if (typeof require !== 'undefined' && require.main === module) {
    console.log('Hash Table Implementations - Comprehensive Demo\n');

    // Test chaining
    console.log('1. Separate Chaining Hash Table');
    console.log('-'.repeat(40));
    const htChain = new ChainingHashTable();
    for (let i = 0; i < 10; i++) {
        htChain.put(`key${i}`, i * 10);
    }
    console.log(`Size: ${htChain.size}`);
    console.log(`Get 'key5': ${htChain.get('key5')}`);
    console.log('Stats:', htChain.getStats(), '\n');

    // Test open addressing
    console.log('2. Open Addressing Hash Table');
    console.log('-'.repeat(40));
    const htOpen = new OpenAddressingHashTable();
    for (let i = 0; i < 10; i++) {
        htOpen.put(`key${i}`, i * 10);
    }
    console.log(`Size: ${htOpen.size}`);
    console.log('Stats:', htOpen.getStats(), '\n');

    // Test Robin Hood
    console.log('3. Robin Hood Hash Table');
    console.log('-'.repeat(40));
    const htRobin = new RobinHoodHashTable();
    for (let i = 0; i < 10; i++) {
        htRobin.put(`key${i}`, i * 10);
    }
    console.log(`Size: ${htRobin.size}`);
    console.log('Stats:', htRobin.getStats(), '\n');

    // Test consistent hashing
    console.log('4. Consistent Hashing');
    console.log('-'.repeat(40));
    const ring = new ConsistentHashRing(['server1', 'server2', 'server3']);
    const testKeys = Array.from({ length: 20 }, (_, i) => `user_${i}`);
    const distribution = ring.getDistribution(testKeys);
    console.log('Key distribution:', distribution, '\n');

    console.log('✨ Hash table demonstrations complete!');
}
