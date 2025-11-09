/**
 * Comprehensive Hash Table Implementation in C#
 *
 * Features:
 * - Separate chaining for collision resolution
 * - Dynamic resizing with configurable load factor
 * - Generic implementation with type constraints
 * - IEnumerable<T> interface for LINQ support
 * - Indexer syntax support
 * - Performance statistics
 * - Null-safe with nullable reference types
 *
 * Time Complexity:
 * - Average: O(1) for insert, delete, search
 * - Worst:   O(n) for chaining with poor hash function
 *
 * Space Complexity: O(n) where n is the number of elements
 *
 * Compilation and Usage:
 *   csc HashTable.cs
 *   ./HashTable.exe
 *
 * Or with dotnet:
 *   dotnet run
 */

using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

// ============================================================================
// HASH TABLE NODE
// ============================================================================

/// <summary>
/// Node in the linked list (chain) for collision resolution
/// </summary>
internal class HashNode<TKey, TValue>
{
    public TKey Key { get; set; }
    public TValue Value { get; set; }
    public HashNode<TKey, TValue>? Next { get; set; }

    public HashNode(TKey key, TValue value)
    {
        Key = key;
        Value = value;
        Next = null;
    }
}

// ============================================================================
// HASH TABLE STATISTICS
// ============================================================================

/// <summary>
/// Performance statistics for hash table
/// </summary>
public record HashTableStats
{
    public int Size { get; init; }
    public int Capacity { get; init; }
    public double LoadFactor { get; init; }
    public int Collisions { get; init; }
    public int Resizes { get; init; }
    public int MaxChainLength { get; init; }
    public double AvgChainLength { get; init; }
    public int NumberOfChains { get; init; }
}

// ============================================================================
// HASH TABLE STRUCTURE
// ============================================================================

/// <summary>
/// Hash table with separate chaining
/// </summary>
public class HashTable<TKey, TValue> : IEnumerable<KeyValuePair<TKey, TValue>>
    where TKey : notnull
{
    private HashNode<TKey, TValue>?[] _buckets;
    private int _capacity;
    private int _count;
    private readonly double _loadFactor;

    // Statistics
    private int _collisions;
    private int _resizes;

    // ========================================================================
    // CONSTRUCTORS
    // ========================================================================

    /// <summary>
    /// Create hash table with initial capacity
    /// </summary>
    public HashTable(int initialCapacity = 16, double loadFactor = 0.75)
    {
        _capacity = NextPowerOf2(initialCapacity);
        _count = 0;
        _loadFactor = loadFactor;
        _collisions = 0;
        _resizes = 0;
        _buckets = new HashNode<TKey, TValue>[_capacity];
    }

    // ========================================================================
    // UTILITY FUNCTIONS
    // ========================================================================

    /// <summary>
    /// Get next power of 2 >= n
    /// </summary>
    private static int NextPowerOf2(int n)
    {
        if (n <= 1) return 1;
        int power = 1;
        while (power < n)
        {
            power *= 2;
        }
        return power;
    }

    /// <summary>
    /// Compute bucket index for key
    /// </summary>
    private int GetHashIndex(TKey key)
    {
        int hashCode = key.GetHashCode();
        // Ensure positive value and map to bucket range
        return (hashCode & 0x7FFFFFFF) & (_capacity - 1);
    }

    /// <summary>
    /// Check if table should be resized
    /// </summary>
    private bool ShouldResize()
    {
        return (double)_count / _capacity > _loadFactor;
    }

    /// <summary>
    /// Resize and rehash all elements
    /// </summary>
    private void Resize()
    {
        _resizes++;
        var oldBuckets = _buckets;
        _capacity *= 2;
        _buckets = new HashNode<TKey, TValue>[_capacity];
        _count = 0;
        _collisions = 0;

        // Rehash all entries
        foreach (var bucket in oldBuckets)
        {
            var node = bucket;
            while (node != null)
            {
                Put(node.Key, node.Value);
                node = node.Next;
            }
        }
    }

    // ========================================================================
    // CORE OPERATIONS
    // ========================================================================

    /// <summary>
    /// Insert or update a key-value pair
    /// </summary>
    /// <returns>True if key existed (update), false if new key (insert)</returns>
    public bool Put(TKey key, TValue value)
    {
        if (ShouldResize())
        {
            Resize();
        }

        int index = GetHashIndex(key);
        var node = _buckets[index];

        // Search for existing key
        while (node != null)
        {
            if (EqualityComparer<TKey>.Default.Equals(node.Key, key))
            {
                node.Value = value;
                return true;
            }
            node = node.Next;
        }

        // Key not found, insert at head
        if (_buckets[index] != null)
        {
            _collisions++;
        }

        var newNode = new HashNode<TKey, TValue>(key, value)
        {
            Next = _buckets[index]
        };
        _buckets[index] = newNode;
        _count++;

        return false;
    }

    /// <summary>
    /// Get value for key
    /// </summary>
    public TValue? Get(TKey key)
    {
        int index = GetHashIndex(key);
        var node = _buckets[index];

        while (node != null)
        {
            if (EqualityComparer<TKey>.Default.Equals(node.Key, key))
            {
                return node.Value;
            }
            node = node.Next;
        }

        return default;
    }

    /// <summary>
    /// Try to get value for key
    /// </summary>
    public bool TryGetValue(TKey key, out TValue? value)
    {
        int index = GetHashIndex(key);
        var node = _buckets[index];

        while (node != null)
        {
            if (EqualityComparer<TKey>.Default.Equals(node.Key, key))
            {
                value = node.Value;
                return true;
            }
            node = node.Next;
        }

        value = default;
        return false;
    }

    /// <summary>
    /// Remove key and return success
    /// </summary>
    public bool Remove(TKey key)
    {
        int index = GetHashIndex(key);
        var node = _buckets[index];
        HashNode<TKey, TValue>? prev = null;

        while (node != null)
        {
            if (EqualityComparer<TKey>.Default.Equals(node.Key, key))
            {
                if (prev != null)
                {
                    prev.Next = node.Next;
                }
                else
                {
                    _buckets[index] = node.Next;
                }
                _count--;
                return true;
            }
            prev = node;
            node = node.Next;
        }

        return false;
    }

    /// <summary>
    /// Check if key exists
    /// </summary>
    public bool ContainsKey(TKey key)
    {
        return TryGetValue(key, out _);
    }

    /// <summary>
    /// Get number of elements
    /// </summary>
    public int Count => _count;

    /// <summary>
    /// Check if hash table is empty
    /// </summary>
    public bool IsEmpty => _count == 0;

    /// <summary>
    /// Clear all elements
    /// </summary>
    public void Clear()
    {
        _buckets = new HashNode<TKey, TValue>[_capacity];
        _count = 0;
        _collisions = 0;
    }

    /// <summary>
    /// Get all keys
    /// </summary>
    public IEnumerable<TKey> Keys
    {
        get
        {
            foreach (var bucket in _buckets)
            {
                var node = bucket;
                while (node != null)
                {
                    yield return node.Key;
                    node = node.Next;
                }
            }
        }
    }

    /// <summary>
    /// Get all values
    /// </summary>
    public IEnumerable<TValue> Values
    {
        get
        {
            foreach (var bucket in _buckets)
            {
                var node = bucket;
                while (node != null)
                {
                    yield return node.Value;
                    node = node.Next;
                }
            }
        }
    }

    /// <summary>
    /// Indexer syntax support
    /// </summary>
    public TValue? this[TKey key]
    {
        get => Get(key);
        set
        {
            if (value != null)
            {
                Put(key, value);
            }
        }
    }

    // ========================================================================
    // ITERATION
    // ========================================================================

    /// <summary>
    /// Get enumerator for iteration
    /// </summary>
    public IEnumerator<KeyValuePair<TKey, TValue>> GetEnumerator()
    {
        foreach (var bucket in _buckets)
        {
            var node = bucket;
            while (node != null)
            {
                yield return new KeyValuePair<TKey, TValue>(node.Key, node.Value);
                node = node.Next;
            }
        }
    }

    IEnumerator IEnumerable.GetEnumerator()
    {
        return GetEnumerator();
    }

    // ========================================================================
    // STATISTICS
    // ========================================================================

    /// <summary>
    /// Get performance statistics
    /// </summary>
    public HashTableStats GetStats()
    {
        int maxChain = 0;
        int totalChainLength = 0;
        int numChains = 0;

        foreach (var bucket in _buckets)
        {
            int chainLength = 0;
            var node = bucket;

            while (node != null)
            {
                chainLength++;
                node = node.Next;
            }

            if (chainLength > 0)
            {
                numChains++;
                totalChainLength += chainLength;
                maxChain = Math.Max(maxChain, chainLength);
            }
        }

        double avgChainLength = numChains > 0 ? (double)totalChainLength / numChains : 0.0;

        return new HashTableStats
        {
            Size = _count,
            Capacity = _capacity,
            LoadFactor = (double)_count / _capacity,
            Collisions = _collisions,
            Resizes = _resizes,
            MaxChainLength = maxChain,
            AvgChainLength = avgChainLength,
            NumberOfChains = numChains
        };
    }

    /// <summary>
    /// Print statistics
    /// </summary>
    public void PrintStats()
    {
        var stats = GetStats();
        Console.WriteLine("Hash Table Statistics:");
        Console.WriteLine($"  Size:              {stats.Size}");
        Console.WriteLine($"  Capacity:          {stats.Capacity}");
        Console.WriteLine($"  Load Factor:       {stats.LoadFactor:F2} / {_loadFactor:F2}");
        Console.WriteLine($"  Collisions:        {stats.Collisions}");
        Console.WriteLine($"  Resizes:           {stats.Resizes}");
        Console.WriteLine($"  Max Chain Length:  {stats.MaxChainLength}");
        Console.WriteLine($"  Avg Chain Length:  {stats.AvgChainLength:F2}");
        Console.WriteLine($"  Number of Chains:  {stats.NumberOfChains}");
    }

    /// <summary>
    /// String representation
    /// </summary>
    public override string ToString()
    {
        var entries = this.Take(10).Select(kvp => $"{kvp.Key}: {kvp.Value}");
        string entriesStr = string.Join(", ", entries);
        string more = _count > 10 ? $", ... and {_count - 10} more" : "";
        return $"HashTable({entriesStr}{more})";
    }
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

public class Program
{
    public static void Main()
    {
        Console.WriteLine("===========================================");
        Console.WriteLine("Hash Table Implementation in C#");
        Console.WriteLine("===========================================");
        Console.WriteLine();

        // Create hash table
        var ht = new HashTable<string, int>(initialCapacity: 16);

        Console.WriteLine("1. Inserting elements...");
        Console.WriteLine("-----------------------------------------");

        // Insert some data
        for (int i = 0; i < 10; i++)
        {
            string key = $"key{i}";
            int value = i * 10;
            ht.Put(key, value);
            Console.WriteLine($"  Inserted: {key} -> {value}");
        }
        Console.WriteLine($"\nSize: {ht.Count}\n");

        Console.WriteLine("2. Retrieving elements...");
        Console.WriteLine("-----------------------------------------");

        string[] testKeys = { "key0", "key5", "key9", "nonexistent" };
        foreach (var key in testKeys)
        {
            if (ht.TryGetValue(key, out var value))
            {
                Console.WriteLine($"  Get '{key}': {value}");
            }
            else
            {
                Console.WriteLine($"  Get '{key}': Not found");
            }
        }

        Console.WriteLine("\n3. Testing indexer syntax...");
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine($"  ht[\"key3\"] = {ht["key3"]}");
        ht["key3"] = 333;
        Console.WriteLine($"  After ht[\"key3\"] = 333: {ht["key3"]}");

        Console.WriteLine("\n4. Testing containment...");
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine($"  Contains 'key3': {ht.ContainsKey("key3")}");
        Console.WriteLine($"  Contains 'missing': {ht.ContainsKey("missing")}");

        Console.WriteLine("\n5. Updating values...");
        Console.WriteLine("-----------------------------------------");

        bool existed = ht.Put("key5", 999);
        Console.WriteLine($"  Updated 'key5': key existed = {existed}, new value = 999");

        Console.WriteLine("\n6. Removing elements...");
        Console.WriteLine("-----------------------------------------");

        bool removed = ht.Remove("key7");
        Console.WriteLine($"  Removed 'key7': {removed}");
        Console.WriteLine($"  Size after removal: {ht.Count}");

        Console.WriteLine("\n7. Iterating over elements...");
        Console.WriteLine("-----------------------------------------");
        int itemCount = 0;
        foreach (var kvp in ht)
        {
            if (itemCount < 5)
            {
                Console.WriteLine($"  {kvp.Key}: {kvp.Value}");
            }
            itemCount++;
        }
        if (itemCount > 5)
        {
            Console.WriteLine($"  ... and {itemCount - 5} more elements");
        }

        Console.WriteLine("\n8. Using LINQ...");
        Console.WriteLine("-----------------------------------------");
        var keysStartingWithK = ht.Keys.Where(k => k.StartsWith("key")).Take(3);
        Console.WriteLine($"  First 3 keys starting with 'key': {string.Join(", ", keysStartingWithK)}");

        Console.WriteLine("\n9. Performance Statistics");
        Console.WriteLine("-----------------------------------------");
        ht.PrintStats();

        Console.WriteLine("\n10. Testing with many elements...");
        Console.WriteLine("-----------------------------------------");

        // Insert many elements to trigger resizing
        for (int i = 100; i < 200; i++)
        {
            string key = $"item{i}";
            ht[key] = i;
        }

        Console.WriteLine("  Added 100 more elements");
        Console.WriteLine($"  New size: {ht.Count}");
        Console.WriteLine();
        ht.PrintStats();

        Console.WriteLine("\n11. Testing Keys and Values properties...");
        Console.WriteLine("-----------------------------------------");
        var keys = ht.Keys.ToList();
        var values = ht.Values.ToList();
        Console.WriteLine($"  Total keys: {keys.Count}");
        Console.WriteLine($"  Total values: {values.Count}");
        Console.WriteLine($"  First 5 keys: {string.Join(", ", keys.Take(5))}");

        Console.WriteLine("\n12. Testing with integer keys...");
        Console.WriteLine("-----------------------------------------");

        var intTable = new HashTable<int, string>(initialCapacity: 8);
        for (int i = 1; i <= 5; i++)
        {
            intTable[i] = $"value{i}";
        }

        if (intTable.TryGetValue(3, out var val3))
        {
            Console.WriteLine($"  intTable[3] = {val3}");
        }

        Console.WriteLine("\n13. Clearing hash table...");
        Console.WriteLine("-----------------------------------------");
        ht.Clear();
        Console.WriteLine($"  Size after clear: {ht.Count}");
        Console.WriteLine($"  Is empty: {ht.IsEmpty}");

        Console.WriteLine("\n===========================================");
        Console.WriteLine("✨ Hash table demonstration complete!");
        Console.WriteLine("===========================================");
    }
}
