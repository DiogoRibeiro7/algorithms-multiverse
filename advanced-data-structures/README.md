# Advanced Data Structures

A comprehensive collection of advanced data structures implemented in Python, featuring self-balancing trees, probabilistic structures, and specialized trees for range operations.

## 📚 Table of Contents

- [Overview](#overview)
- [Implemented Data Structures](#implemented-data-structures)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Performance Comparisons](#performance-comparisons)
- [Applications](#applications)
- [Contributing](#contributing)

## 🎯 Overview

This module provides production-ready implementations of advanced data structures that go beyond basic arrays, linked lists, and simple trees. Each structure is optimized for specific use cases and includes:

- **Comprehensive Documentation**: Detailed explanations of algorithms and complexity
- **Visualization**: Built-in methods to visualize structure state
- **Benchmarking**: Performance comparison tools
- **Real-world Examples**: Practical applications demonstrated

## 📊 Implemented Data Structures

### Complete List (11 structures implemented - 100% COMPLETE):
1. AVL Tree - Self-balancing BST with strict height balance
2. Red-Black Tree - Self-balancing BST with relaxed balance
3. Segment Tree - Range queries and updates
4. Bloom Filter - Space-efficient membership testing
5. Fenwick Tree - Efficient prefix sums
6. Skip List - Probabilistic balanced structure
7. Count-Min Sketch - Frequency estimation in streams
8. B-Tree - Optimized for disk-based storage
9. B+ Tree - Enhanced B-Tree with linked leaves
10. Cuckoo Hashing - Worst-case O(1) lookup guarantee
11. Suffix Structures - Advanced string processing (Tree, Array, Automaton)

### 1. AVL Tree (`avl_tree.py`)

**Self-balancing binary search tree with strict height balance**

- **Properties**:
  - Height difference between subtrees ≤ 1
  - Guarantees O(log n) operations
  - More balanced than Red-Black trees
  - Automatic rebalancing through rotations

- **Operations**:
  - Insert: O(log n)
  - Delete: O(log n)
  - Search: O(log n)
  - Min/Max: O(log n)

- **Use Cases**:
  - Database indexing
  - Memory-constrained systems
  - Applications requiring guaranteed logarithmic operations
  - Scenarios where lookups outnumber insertions

```python
from avl_tree import AVLTree

# Create and populate tree
avl = AVLTree()
for value in [50, 30, 70, 20, 40, 60, 80]:
    avl.insert(value)

# Operations
print(avl.search(40))  # True
print(avl.get_height())  # Tree height
print(avl.is_balanced())  # True

# Visualization
avl.visualize()
avl.print_tree()
```

### 2. Red-Black Tree (`red_black_tree.py`)

**Self-balancing BST with relaxed balance constraints**

- **Properties**:
  - Color-based balancing (red/black nodes)
  - Less strict than AVL (better insertion/deletion performance)
  - Guaranteed O(log n) worst-case operations
  - All paths from root to leaf have same black node count

- **Operations**:
  - Insert: O(log n)
  - Delete: O(log n)
  - Search: O(log n)
  - Predecessor/Successor: O(log n)

- **Use Cases**:
  - C++ STL map/set implementations
  - Java TreeMap/TreeSet
  - Linux kernel (completely fair scheduler)
  - In-memory databases

```python
from red_black_tree import RBTree

# Create and use Red-Black Tree
rbt = RBTree()
for key, value in [(7, "seven"), (3, "three"), (18, "eighteen")]:
    rbt.insert(key, value)

# Operations
print(rbt.search(7))  # "seven"
print(rbt.verify_properties())  # True
print(rbt.get_black_height())  # Black height
print(rbt.predecessor(7))  # 3
print(rbt.successor(7))  # 18

# Visualization
print(rbt.visualize())
```

### 3. Segment Tree (`segment_tree.py`)

**Tree for efficient range queries and updates**

- **Properties**:
  - Stores intervals/segments
  - Supports various range operations (sum, min, max, GCD)
  - Lazy propagation for efficient range updates
  - Array-based implementation

- **Operations**:
  - Build: O(n)
  - Range Query: O(log n)
  - Point Update: O(log n)
  - Range Update: O(log n) with lazy propagation

- **Use Cases**:
  - Range sum/min/max queries
  - Computational geometry
  - Database range queries
  - Competitive programming
  - Time series analysis

```python
from segment_tree import SegmentTree, QueryType, LazySegmentTree

# Create segment tree for range sums
arr = [1, 3, 5, 7, 9, 11]
st = SegmentTree(arr, QueryType.SUM)

# Range queries
print(st.query(1, 4))  # Sum of arr[1:5]

# Point update
st.update_point(2, 10)

# Range update with lazy propagation
lst = LazySegmentTree(arr)
lst.update_range(2, 4, 5)  # Add 5 to range [2,4]
lst.set_range(1, 3, 100)  # Set range [1,3] to 100

# Visualization
st.visualize(highlight_range=(1, 4))
```

### 4. Bloom Filter (`bloom_filter.py`)

**Space-efficient probabilistic membership testing**

- **Properties**:
  - Uses bit array with multiple hash functions
  - No false negatives (if not found, definitely absent)
  - Possible false positives (configurable rate)
  - Extremely space-efficient
  - Counting variant supports deletion

- **Operations**:
  - Insert: O(k) where k = number of hash functions
  - Query: O(k)
  - Space: O(m) bits

- **Use Cases**:
  - Web crawlers (URL deduplication)
  - Database query optimization
  - Network routers
  - Distributed caching
  - Spell checkers
  - Blockchain/cryptocurrency

```python
from bloom_filter import BloomFilter, CountingBloomFilter

# Standard Bloom Filter
bf = BloomFilter(expected_elements=10000, false_positive_rate=0.01)

# Add elements
bf.add("apple")
bf.add("banana")

# Check membership
print("apple" in bf)  # True
print("orange" in bf)  # False (or rarely True - false positive)

# Statistics
print(f"Load factor: {bf.get_load_factor():.2%}")
print(f"Estimated FP rate: {bf.estimate_false_positive_rate():.4%}")

# Counting Bloom Filter (supports deletion)
cbf = CountingBloomFilter(expected_elements=1000)
cbf.add("item1")
cbf.remove("item1")

# Visualization
bf.visualize()
```

### 5. Fenwick Tree / Binary Indexed Tree (`fenwick_tree.py`)

**Efficient prefix sum queries and updates**

- **Properties**:
  - Space-efficient alternative to Segment Tree for specific operations
  - Uses clever bit manipulation for index calculations
  - Supports 2D variant for matrix operations
  - Range update variant available

- **Operations**:
  - Build: O(n)
  - Prefix Sum: O(log n)
  - Point Update: O(log n)
  - Range Sum: O(log n)

- **Use Cases**:
  - Cumulative frequency tables
  - Inversions count
  - Order statistics
  - Dynamic programming optimizations
  - 2D range sum queries

```python
from fenwick_tree import FenwickTree, FenwickTree2D, RangeFenwickTree

# 1D Fenwick Tree
arr = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
ft = FenwickTree(arr)

# Operations
print(ft.prefix_sum(4))  # Sum of first 5 elements
print(ft.range_sum(2, 5))  # Sum of range [2,5]
ft.update(3, 10)  # Add 10 to index 3

# 2D Fenwick Tree for matrices
matrix = [[3, 0, 1, 4],
          [2, 5, 6, 3],
          [1, 2, 3, 1]]
ft2d = FenwickTree2D(matrix)
print(ft2d.range_sum(0, 0, 1, 1))  # Rectangle sum

# Range updates
rft = RangeFenwickTree([1, 2, 3, 4, 5])
rft.update_range(1, 3, 10)  # Add 10 to range [1,3]
```

### 6. Skip List (`skip_list.py`)

**Probabilistic alternative to balanced trees**

- **Properties**:
  - Multiple levels of linked lists
  - Probabilistic balancing
  - Expected O(log n) operations
  - Simple implementation compared to trees
  - Supports indexable variant

- **Operations**:
  - Insert: O(log n) expected
  - Delete: O(log n) expected
  - Search: O(log n) expected
  - Range Search: O(log n + k) for k results

- **Use Cases**:
  - Redis sorted sets
  - Apache Lucene
  - Database indexes
  - Priority queues
  - Concurrent data structures

```python
from skip_list import SkipList, IndexableSkipList

# Standard Skip List
sl = SkipList(max_level=16, p=0.5)
sl.insert(10, "ten")
sl.insert(20, "twenty")
sl.insert(15, "fifteen")

# Operations
print(sl.search(15))  # "fifteen"
sl.delete(20)
range_items = sl.range_search(10, 20)  # Range query

# Indexable variant
isl = IndexableSkipList()
isl.insert(5, "five")
print(isl.get_by_index(0))  # Get by position
print(isl.get_rank(5))  # Get position of key

# Analysis
print(sl.analyze_structure())
```

### 7. Count-Min Sketch (`count_min_sketch.py`)

**Probabilistic frequency estimation in data streams**

- **Properties**:
  - Sublinear space complexity
  - Guaranteed overestimation (never underestimates)
  - Configurable error bounds
  - Supports merge operations
  - Conservative update variant available

- **Operations**:
  - Add: O(d) where d = depth
  - Query: O(d)
  - Space: O(w * d) where w = width

- **Use Cases**:
  - Stream processing
  - Network traffic analysis
  - Finding heavy hitters
  - Database query optimization
  - Natural language processing

```python
from count_min_sketch import CountMinSketch, CountMinSketchWithHeap

# Basic Count-Min Sketch
cms = CountMinSketch(epsilon=0.01, delta=0.01)

# Add items from stream
for item in data_stream:
    cms.add(item)

# Query frequencies
freq = cms.query("apple")
print(f"Frequency of 'apple': {freq}")
print(f"Error bound: {cms.error_bound()}")

# Heavy hitters tracking
cms_hh = CountMinSketchWithHeap(width=2000, depth=5, k=10)
for item in data_stream:
    cms_hh.add(item)

top_10 = cms_hh.get_top_k()
print(f"Top 10 items: {top_10}")
```

### 8. B-Tree (`btree.py`)

**Self-balancing tree optimized for disk-based storage**

- **Properties**:
  - All leaves at same level
  - Variable number of keys per node (based on order)
  - Keys and values stored in all nodes
  - Guaranteed O(log n) operations
  - Optimized for systems that read/write large blocks

- **Operations**:
  - Insert: O(log n)
  - Delete: O(log n)
  - Search: O(log n)
  - Range Query: O(log n + k)

- **Use Cases**:
  - Database indexing (PostgreSQL, MySQL)
  - File systems (HFS+, NTFS)
  - Key-value stores
  - B-Tree indexes in databases

```python
from btree import BTree

# Create B-Tree with order 5
btree = BTree(order=5)

# Insert key-value pairs
btree.insert(10, "ten")
btree.insert(20, "twenty")
btree.insert(5, "five")

# Search
value = btree.search(10)  # Returns "ten"

# Range query
results = btree.range_query(5, 15)  # [(5, "five"), (10, "ten")]

# Tree statistics
stats = btree.get_statistics()
print(f"Height: {stats['height']}")
print(f"Space utilization: {stats['space_utilization']:.2%}")

# Visualize tree structure
print(btree.visualize())
```

### 9. B+ Tree (`bplus_tree.py`)

**Enhanced B-Tree with all values in leaves**

- **Properties**:
  - All values stored only in leaf nodes
  - Internal nodes only contain keys for navigation
  - Leaf nodes are linked for sequential access
  - Better cache utilization than B-Tree
  - Optimized for range queries and sequential access

- **Operations**:
  - Insert: O(log n)
  - Delete: O(log n)
  - Search: O(log n)
  - Range Query: O(log n + k)
  - Sequential Scan: O(n)

- **Use Cases**:
  - Modern database systems (InnoDB, SQL Server)
  - File systems (btrfs, ZFS)
  - NoSQL databases
  - Time-series databases
  - Any application requiring efficient range scans

```python
from bplus_tree import BPlusTree

# Create B+ Tree with order 4
bplus = BPlusTree(order=4)

# Bulk load sorted data (optimized)
data = [(i, f"value_{i}") for i in range(100)]
bplus.bulk_load(data, sorted_input=True)

# Efficient range queries (linked leaves)
range_results = bplus.range_query(10, 50)

# Iterator support for sequential access
for key, value in bplus:
    if key > 10:
        break
    print(f"{key}: {value}")

# Get min/max efficiently
min_item = bplus.get_min()  # (0, "value_0")
max_item = bplus.get_max()  # (99, "value_99")

# Tree visualization
print(bplus.visualize())
```

### 10. Cuckoo Hashing (`cuckoo_hashing.py`)

**Hash table with worst-case O(1) lookup time**

- **Properties**:
  - Guaranteed worst-case O(1) lookup and delete
  - Uses two hash functions and displacement chain
  - No clustering or chaining needed
  - Load factor typically kept below 50%
  - Automatic rehashing when cycles detected

- **Operations**:
  - Lookup: O(1) worst-case
  - Delete: O(1) worst-case
  - Insert: O(1) expected, O(n) worst-case (rehashing)
  - Space: O(n)

- **Variants**:
  - **Standard Cuckoo Hash**: Basic implementation with two hash functions
  - **Cuckoo with Stash**: Small overflow area reduces rehashing
  - **Cuckoo Filter**: Probabilistic variant for membership testing

- **Use Cases**:
  - Network routers (IP lookup tables)
  - CPU caches
  - Database query optimization
  - Real-time systems requiring guaranteed lookup time
  - Hardware implementations (FPGAs)

```python
from cuckoo_hashing import CuckooHashTable, CuckooHashingWithStash, CuckooFilter

# Standard Cuckoo Hashing
ch = CuckooHashTable(initial_capacity=100)
ch.insert("key1", "value1")
ch["key2"] = "value2"  # Dict-style interface

# Guaranteed O(1) lookup
value = ch.lookup("key1")  # Always checks at most 2 locations
exists = "key1" in ch  # O(1) worst-case

# Cuckoo with Stash (reduces rehashing)
chs = CuckooHashingWithStash(initial_capacity=100, stash_size=4)
chs.insert("item", "data")

stats = chs.get_statistics()
print(f"Stash utilization: {stats['stash_utilization']:.0%}")
print(f"Rehash count: {stats['rehash_count']}")

# Cuckoo Filter (like Bloom filter but supports deletion)
cf = CuckooFilter(capacity=1000, fingerprint_size=8)
cf.insert("apple")
cf.insert("banana")

# Membership testing
if "apple" in cf:
    print("Apple might be present")

# Unlike Bloom filters, supports deletion
cf.delete("apple")

print(f"Load factor: {cf.get_load_factor():.2%}")
```

### 11. Suffix Structures (`suffix_structures.py`)

**Advanced string processing data structures**

Three implementations included:
- **Suffix Tree**: Compressed trie of all suffixes
- **Suffix Array**: Space-efficient sorted suffix indices
- **Suffix Automaton**: Minimal DFA for suffix recognition

- **Properties**:
  - O(n) suffix tree construction (Ukkonen's algorithm)
  - O(n log n) suffix array construction
  - O(m) pattern search where m is pattern length
  - Space-efficient alternatives to naive approaches
  - Support for complex string operations

- **Operations**:
  - Pattern search: O(m) for tree, O(m log n) for array
  - All occurrences: O(m + occ) where occ is occurrences
  - Longest repeated substring: O(n)
  - Longest common substring: O(n)
  - Count distinct substrings: O(n)

- **Use Cases**:
  - Bioinformatics (DNA/protein sequence analysis)
  - Text editors (search and replace)
  - Data compression algorithms
  - Plagiarism detection systems
  - Search engine indexing
  - Auto-complete/type-ahead features

```python
from suffix_structures import SuffixTree, SuffixArray, SuffixAutomaton

# Suffix Tree - O(n) construction, O(m) search
text = "banana"
st = SuffixTree(text)

# Find all occurrences of pattern
positions = st.search("ana")  # Returns [1, 3]

# Longest repeated substring
lrs = st.longest_repeated_substring()  # Returns "ana"

# Suffix Array - More space-efficient
sa = SuffixArray(text)
print(f"Suffix array: {sa.suffix_array}")  # Sorted suffix indices
print(f"LCP array: {sa.lcp_array}")  # Longest common prefixes

# Pattern search with binary search
occurrences = sa.search("nan")  # O(m log n)

# Count distinct substrings
distinct = sa.count_distinct_substrings()

# Longest common substring between two texts
text2 = "bandana"
lcs = sa.longest_common_substring(text2)  # Returns "ana"

# Suffix Automaton - Minimal DFA
automaton = SuffixAutomaton(text)
exists = automaton.contains("ana")  # O(m) membership test

# Bioinformatics application
dna = "ATCGATCGATCGTAGC"
st_dna = SuffixTree(dna)
motif = "ATCG"
gene_positions = st_dna.search(motif)  # Find gene sequences
tandem_repeat = st_dna.longest_repeated_substring()  # Find repeats
```

## 🚀 Installation

### Requirements

```bash
# Core requirements
python >= 3.7
numpy >= 1.19.0
matplotlib >= 3.3.0

# For Bloom Filter and Count-Min Sketch
pip install mmh3 bitarray

# Optional for better visualizations
pip install networkx
```

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/algorithms-multiverse.git
cd algorithms-multiverse/advanced-data-structures

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage Examples

### Example 1: Database Index Simulation with AVL Tree

```python
from avl_tree import AVLTree
import time
import random

# Simulate database index
class DatabaseIndex:
    def __init__(self):
        self.index = AVLTree()

    def insert_record(self, key, record):
        # In real DB, would store record pointer
        self.index.insert(key)

    def find_record(self, key):
        return self.index.search(key)

    def range_query(self, min_key, max_key):
        # Get all keys in range (inorder traversal)
        all_keys = self.index.inorder_traversal()
        return [k for k in all_keys if min_key <= k <= max_key]

# Usage
db = DatabaseIndex()

# Insert records
for i in range(10000):
    db.insert_record(random.randint(1, 100000), f"record_{i}")

# Query
print(db.find_record(50000))  # Fast O(log n) lookup
print(db.range_query(40000, 60000))  # Range query
```

### Example 2: Real-time Analytics with Segment Tree

```python
from segment_tree import SegmentTree, QueryType
import numpy as np

class TimeSeriesAnalyzer:
    def __init__(self, window_size=1000):
        self.data = np.zeros(window_size)
        self.min_tree = SegmentTree(self.data, QueryType.MIN)
        self.max_tree = SegmentTree(self.data, QueryType.MAX)
        self.sum_tree = SegmentTree(self.data, QueryType.SUM)

    def update_value(self, timestamp, value):
        """Update value at timestamp"""
        self.min_tree.update_point(timestamp, value)
        self.max_tree.update_point(timestamp, value)
        self.sum_tree.update_point(timestamp, value)

    def get_statistics(self, start_time, end_time):
        """Get statistics for time range"""
        return {
            'min': self.min_tree.query(start_time, end_time),
            'max': self.max_tree.query(start_time, end_time),
            'sum': self.sum_tree.query(start_time, end_time),
            'avg': self.sum_tree.query(start_time, end_time) / (end_time - start_time + 1)
        }

# Usage
analyzer = TimeSeriesAnalyzer()

# Simulate data updates
for t in range(100):
    analyzer.update_value(t, np.random.randn() * 10 + 50)

# Get statistics for any time range instantly
stats = analyzer.get_statistics(20, 80)
print(f"Stats for range [20,80]: {stats}")
```

### Example 3: Distributed Cache with Bloom Filter

```python
from bloom_filter import BloomFilter

class DistributedCache:
    def __init__(self, nodes=5):
        # Each node has a Bloom filter for its cache
        self.nodes = [
            BloomFilter(expected_elements=10000, false_positive_rate=0.01)
            for _ in range(nodes)
        ]
        self.cache_hits = 0
        self.cache_misses = 0

    def _hash_to_node(self, key):
        """Determine which node should handle this key"""
        return hash(key) % len(self.nodes)

    def cache_key(self, key):
        """Add key to appropriate node's cache"""
        node_id = self._hash_to_node(key)
        self.nodes[node_id].add(key)

    def might_have_key(self, key):
        """Check if key might be in cache"""
        node_id = self._hash_to_node(key)
        return key in self.nodes[node_id]

    def get(self, key):
        """Simulate cache get operation"""
        if self.might_have_key(key):
            # Would do actual cache lookup here
            self.cache_hits += 1
            return f"value_for_{key}"
        else:
            # Definitely not in cache, fetch from database
            self.cache_misses += 1
            return None

    def stats(self):
        """Get cache statistics"""
        total_memory = sum(node.size / 8 for node in self.nodes)
        return {
            'hits': self.cache_hits,
            'misses': self.cache_misses,
            'memory_bytes': total_memory,
            'false_positive_rate': np.mean([n.estimate_false_positive_rate() for n in self.nodes])
        }

# Usage
cache = DistributedCache()

# Cache some keys
for i in range(1000):
    cache.cache_key(f"user_{i}")

# Query cache
for i in range(1500):
    result = cache.get(f"user_{i}")

print(cache.stats())
```

## 📊 Performance Comparisons

### AVL Tree vs Red-Black Tree vs Regular BST

| Operation | AVL Tree | Red-Black Tree | Unbalanced BST | Notes |
|-----------|----------|----------------|----------------|-------|
| Insert (random) | O(log n) | O(log n) | O(log n) avg | RB faster in practice |
| Insert (sorted) | O(log n) | O(log n) | O(n) | Balanced trees win |
| Delete | O(log n) | O(log n) | O(n) worst | RB has simpler delete |
| Search | O(log n) | O(log n) | O(n) worst | AVL slightly faster |
| Height | ~1.44 log n | ~2 log n | n (worst) | AVL more balanced |

### Segment Tree vs Fenwick Tree

| Aspect | Segment Tree | Fenwick Tree | Winner |
|--------|--------------|--------------|--------|
| Space | 4n | n | Fenwick |
| Build Time | O(n) | O(n) | Tie |
| Range Sum | O(log n) | O(log n) | Tie |
| Range Min/Max | O(log n) | Not supported | Segment |
| Point Update | O(log n) | O(log n) | Tie |
| Range Update | O(log n) | O(log n)* | Segment |
| Implementation | Complex | Simple | Fenwick |

### Bloom Filter vs Count-Min Sketch

| Metric | Bloom Filter | Count-Min Sketch | Use Case |
|--------|--------------|------------------|----------|
| Purpose | Membership | Frequency | Different |
| Space (1M items) | ~1.2 MB | ~10 MB | Bloom wins |
| False Positives | Yes | N/A | Trade-off |
| Overestimation | N/A | Yes | Trade-off |
| Deletion | No* | No | Neither |
| Merge | Yes | Yes | Both |

### B-Tree vs B+ Tree

| Aspect | B-Tree | B+ Tree | Winner |
|--------|--------|---------|--------|
| Values Location | All nodes | Leaf nodes only | Depends |
| Internal Node Size | Smaller (has values) | Larger (keys only) | B+ Tree |
| Range Query | Good | Excellent (linked leaves) | B+ Tree |
| Point Query | Potentially faster | Always to leaf | B-Tree |
| Sequential Access | Slower | Fast (linked leaves) | B+ Tree |
| Space Efficiency | Better for point queries | Better for range queries | Depends |
| Cache Performance | Good | Better (more keys per node) | B+ Tree |
| Implementation | Simpler | More complex | B-Tree |

### Hash Table Comparison

| Operation | Cuckoo Hash | Chaining | Open Addressing | Use Case |
|-----------|-------------|----------|-----------------|----------|
| Lookup | O(1) worst | O(1) avg, O(n) worst | O(1) avg | Real-time systems |
| Insert | O(1) amortized | O(1) avg | O(1) avg | High-frequency ops |
| Delete | O(1) worst | O(1) avg | O(1) avg | Guaranteed timing |
| Load Factor | ~50% | >100% possible | ~75% | Memory constraints |
| Cache Misses | ≤2 always | Variable | 1 average | Cache-sensitive |
| Rehashing | Occasional | Rare | When full | Predictability |

## 🎯 Applications

### Real-World Use Cases

1. **AVL Trees**:
   - Database indexes (PostgreSQL, MySQL)
   - File systems (balanced directory trees)
   - Network routing tables
   - Priority queues with frequent updates

2. **Red-Black Trees**:
   - C++ STL (map, set, multimap, multiset)
   - Java Collections (TreeMap, TreeSet)
   - Linux kernel (completely fair scheduler, memory management)
   - Computational geometry algorithms

3. **Segment Trees**:
   - Stock market analysis (range queries on price data)
   - Geographic Information Systems (spatial queries)
   - Image processing (2D segment trees)
   - Competitive programming contests

4. **Bloom Filters**:
   - Google Bigtable (reducing disk seeks)
   - Bitcoin (SPV clients)
   - Web crawlers (URL deduplication)
   - Malware detection (signature matching)
   - Content Delivery Networks (cache optimization)

5. **Fenwick Trees**:
   - Competitive programming (range sum queries)
   - Statistics (running medians)
   - Inversion counting
   - 2D cumulative frequency tables

6. **Skip Lists**:
   - Redis (sorted sets implementation)
   - Apache Lucene (inverted indexes)
   - HBase (MemStore)
   - LevelDB/RocksDB (MemTable)

7. **Count-Min Sketch**:
   - Network monitoring (heavy hitters)
   - Database query optimization
   - Natural language processing (word frequency)
   - Streaming analytics

8. **B-Trees**:
   - Traditional database systems (PostgreSQL B-Tree indexes)
   - File systems (HFS+, NTFS MFT)
   - Key-value stores (Berkeley DB)
   - Search engines (inverted indexes)
   - Embedded databases (SQLite)

9. **B+ Trees**:
   - Modern database systems (MySQL InnoDB, Oracle, SQL Server)
   - File systems (btrfs, ZFS, ext4 with dir_index)
   - NoSQL databases (MongoDB WiredTiger)
   - Time-series databases (InfluxDB)
   - Graph databases (Neo4j)
   - In-memory databases with persistence

10. **Cuckoo Hashing**:
   - Network routers and switches (IP forwarding tables)
   - CPU cache implementations
   - Hardware hash tables (FPGAs, ASICs)
   - Real-time systems (guaranteed lookup time)
   - Content delivery networks (CDN routing)
   - High-frequency trading systems

11. **Suffix Structures**:
   - Bioinformatics (genome sequencing, protein analysis)
   - Search engines (Google, Elasticsearch)
   - Text editors (Sublime Text, VS Code search)
   - Plagiarism detection (Turnitin, Copyscape)
   - Data compression (LZ77, LZ78 algorithms)
   - Intrusion detection systems (pattern matching)

## 🧪 Testing

Run the test suite:

```bash
# Test individual structures
python avl_tree.py
python red_black_tree.py
python segment_tree.py
python bloom_filter.py
python fenwick_tree.py
python skip_list.py
python count_min_sketch.py
python btree.py
python bplus_tree.py
python cuckoo_hashing.py
python suffix_structures.py

# Test B-Trees and B+ Trees
python test_btrees.py

# Test Cuckoo Hashing
python test_cuckoo_hashing.py

# Test Suffix Structures
python test_suffix_structures.py

# Run all tests
python test_all.py

# Performance benchmarks
python benchmarks.py
```

## 📈 Benchmarks

```python
# Run performance comparisons
from test_all import performance_comparison

performance_comparison()
```

## 🤝 Contributing

Contributions are welcome! Priority areas:

1. **All core structures completed!** Next priorities:
   - Treap (Tree + Heap hybrid)
   - Splay Trees (self-adjusting BST)
   - Fibonacci Heaps (advanced priority queue)
   - Trie variations (Patricia, Radix)
   - Persistent data structures
   - Van Emde Boas Trees

2. **Add language implementations**:
   - Port to C++, Java, Go, Rust
   - Optimize for language-specific features

3. **Enhance existing structures**:
   - Add persistence (immutable versions)
   - Implement parallel versions
   - Add more visualization options

4. **Documentation**:
   - Add more real-world examples
   - Create tutorial notebooks
   - Add complexity proofs

## 📚 References

### Papers
- Adelson-Velsky, G.; Landis, E. M. (1962). "An algorithm for organization of information"
- Bloom, Burton H. (1970). "Space/Time Trade-offs in Hash Coding with Allowable Errors"
- Bentley, Jon Louis (1977). "Solutions to Klee's rectangle problems"
- Cormode, G.; Muthukrishnan, S. (2005). "An improved data stream summary: the count-min sketch"
- Pugh, William (1990). "Skip Lists: A Probabilistic Alternative to Balanced Trees"

### Books
- "Introduction to Algorithms" - Cormen, Leiserson, Rivest, Stein
- "Advanced Data Structures" - Peter Brass
- "The Art of Computer Programming" - Donald Knuth

### Online Resources
- [VisuAlgo](https://visualgo.net/) - Visualization of algorithms
- [CP-Algorithms](https://cp-algorithms.com/) - Competitive programming algorithms
- [GeeksforGeeks](https://www.geeksforgeeks.org/) - DS & Algo tutorials

## 📄 License

MIT License - See [LICENSE](../../LICENSE) file for details.

## 🌟 Acknowledgments

Part of the **Algorithms Multiverse** project - A comprehensive collection of algorithms and data structures across multiple programming languages.

---

**Author**: Algorithms Multiverse Contributors
**Last Updated**: January 2025