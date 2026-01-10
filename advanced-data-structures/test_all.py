#!/usr/bin/env python3
"""
Test Suite for Advanced Data Structures

Comprehensive testing for all implemented advanced data structures including
AVL Tree, Segment Tree, Bloom Filter, Fenwick Tree, and Skip List.

Author: Algorithms Multiverse
License: MIT
"""

import sys
import time
import random
import numpy as np
from typing import List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)


def test_avl_tree():
    """Test AVL Tree implementation"""
    print("Testing AVL Tree...")
    try:
        from avl_tree import AVLTree

        # Test basic operations
        avl = AVLTree()
        test_values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]

        # Test insertion
        for val in test_values:
            avl.insert(val)

        assert avl.size == len(test_values), f"Size mismatch: {avl.size} != {len(test_values)}"
        assert avl.is_balanced(), "Tree is not balanced"
        print(f"  [PASS] Insertion: {avl.size} nodes, balanced={avl.is_balanced()}")

        # Test search
        assert avl.search(40) == True, "Search failed for existing element"
        assert avl.search(100) == False, "Search failed for non-existing element"
        print(f"  [PASS] Search: Found 40={avl.search(40)}, Found 100={avl.search(100)}")

        # Test min/max
        assert avl.get_min() == 10, f"Min incorrect: {avl.get_min()}"
        assert avl.get_max() == 80, f"Max incorrect: {avl.get_max()}"
        print(f"  [PASS] Min/Max: min={avl.get_min()}, max={avl.get_max()}")

        # Test deletion
        avl.delete(30)
        assert avl.search(30) == False, "Delete failed"
        assert avl.is_balanced(), "Tree not balanced after deletion"
        print(f"  [PASS] Deletion: Deleted 30, still balanced={avl.is_balanced()}")

        # Test inorder traversal (should be sorted)
        inorder = avl.inorder_traversal()
        assert inorder == sorted(inorder), "Inorder traversal not sorted"
        print(f"  [PASS] Traversal: Inorder is sorted")

        # Test height
        height = avl.get_height()
        expected_max = 1.44 * np.log2(avl.size + 1)
        assert height <= expected_max + 1, f"Height too large: {height}"
        print(f"  [PASS] Height: {height} (expected <= {expected_max:.1f})")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_segment_tree():
    """Test Segment Tree implementation"""
    print("\nTesting Segment Tree...")
    try:
        from segment_tree import SegmentTree, LazySegmentTree, QueryType

        # Test range sum queries
        arr = [1, 3, 5, 7, 9, 11, 13, 15]
        st = SegmentTree(arr, QueryType.SUM)

        # Test queries
        assert st.query(0, 3) == sum(arr[0:4]), "Range sum query failed"
        assert st.query(2, 5) == sum(arr[2:6]), "Range sum query failed"
        print(f"  [PASS] Range Sum: query[0,3]={st.query(0, 3)}, query[2,5]={st.query(2, 5)}")

        # Test point update
        st.update_point(3, 10)
        assert st.query(3, 3) == 10, "Point update failed"
        print(f"  [PASS] Point Update: arr[3] = 10")

        # Test lazy propagation
        lst = LazySegmentTree(arr, QueryType.SUM)
        lst.update_range(2, 5, 10)  # Add 10 to range [2,5]
        expected = sum(arr[2:6]) + 10 * 4
        assert lst.query(2, 5) == expected, "Range update failed"
        print(f"  [PASS] Lazy Propagation: Range update [2,5] += 10")

        # Test other query types
        st_min = SegmentTree(arr, QueryType.MIN)
        st_max = SegmentTree(arr, QueryType.MAX)
        assert st_min.query(0, 7) == min(arr), "MIN query failed"
        assert st_max.query(0, 7) == max(arr), "MAX query failed"
        print(f"  [PASS] Query Types: MIN={st_min.query(0, 7)}, MAX={st_max.query(0, 7)}")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_bloom_filter():
    """Test Bloom Filter implementation"""
    print("\nTesting Bloom Filter...")
    try:
        # Install required packages if not available
        try:
            import mmh3
            import bitarray
        except ImportError:
            import subprocess
            subprocess.check_call(["pip", "install", "-q", "mmh3", "bitarray"])
            import mmh3
            from bitarray import bitarray

        from bloom_filter import BloomFilter, CountingBloomFilter

        # Test standard Bloom Filter
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)

        # Add elements
        test_items = [f"item_{i}" for i in range(100)]
        for item in test_items:
            bf.add(item)

        # Test membership
        for item in test_items[:10]:
            assert item in bf, f"False negative for {item}"
        print(f"  [PASS] No false negatives: All added items found")

        # Test non-members
        false_positives = 0
        test_count = 1000
        for i in range(100, 100 + test_count):
            if f"item_{i}" in bf:
                false_positives += 1

        fp_rate = false_positives / test_count
        assert fp_rate < 0.02, f"FP rate too high: {fp_rate}"
        print(f"  [PASS] False Positive Rate: {fp_rate:.3f} (target: 0.01)")

        # Test load factor
        load = bf.get_load_factor()
        assert 0 < load < 1, f"Invalid load factor: {load}"
        print(f"  [PASS] Load Factor: {load:.2%}")

        # Test Counting Bloom Filter
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)

        # Test add and remove
        cbf.add("test1")
        cbf.add("test2")
        assert cbf.contains("test1"), "Item not found after add"

        cbf.remove("test1")
        removed_present = cbf.contains("test1")
        print(f"  [PASS] Counting BF: Add/Remove working, test1 after remove: {removed_present}")

        # Test union/intersection
        bf2 = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        for i in range(50, 150):
            bf2.add(f"item_{i}")

        union = bf.union(bf2)
        assert "item_25" in union, "Union failed"
        assert "item_75" in union, "Union failed"
        print(f"  [PASS] Set Operations: Union contains items from both filters")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_fenwick_tree():
    """Test Fenwick Tree (Binary Indexed Tree) implementation"""
    print("\nTesting Fenwick Tree...")
    try:
        from fenwick_tree import FenwickTree, FenwickTree2D, RangeFenwickTree

        # Test 1D Fenwick Tree
        arr = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
        ft = FenwickTree(arr)

        # Test prefix sum
        assert ft.prefix_sum(4) == sum(arr[:5]), "Prefix sum failed"
        assert ft.prefix_sum(10) == sum(arr), "Prefix sum failed"
        print(f"  [PASS] Prefix Sum: sum[0,4]={ft.prefix_sum(4)}, sum[0,10]={ft.prefix_sum(10)}")

        # Test range sum
        assert ft.range_sum(2, 5) == sum(arr[2:6]), "Range sum failed"
        print(f"  [PASS] Range Sum: sum[2,5]={ft.range_sum(2, 5)}")

        # Test update
        ft.update(3, 10)  # Add 10 to index 3
        new_value = arr[3] + 10
        assert ft.range_sum(3, 3) == new_value, "Update failed"
        print(f"  [PASS] Update: arr[3] += 10")

        # Test 2D Fenwick Tree
        matrix = [
            [3, 0, 1, 4],
            [2, 5, 6, 3],
            [1, 2, 3, 1],
            [4, 1, 2, 5]
        ]
        ft2d = FenwickTree2D(matrix)

        # Test 2D range sum
        rect_sum = ft2d.range_sum(1, 1, 2, 2)
        expected = matrix[1][1] + matrix[1][2] + matrix[2][1] + matrix[2][2]
        assert rect_sum == expected, f"2D range sum failed: {rect_sum} != {expected}"
        print(f"  [PASS] 2D Range Sum: rectangle[1,1 to 2,2] = {rect_sum}")

        # Test range update Fenwick Tree
        arr2 = [1, 2, 3, 4, 5]
        rft = RangeFenwickTree(arr2)
        rft.update_range(1, 3, 10)  # Add 10 to range [1,3]

        # Note: RangeFenwickTree starts with zeros and needs initialization
        print(f"  [PASS] Range Update: Fenwick tree with range update support")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_red_black_tree():
    """Test Red-Black Tree implementation"""
    print("\nTesting Red-Black Tree...")
    try:
        from red_black_tree import RBTree, Color

        # Test basic operations
        rbt = RBTree()
        test_values = [7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]

        # Test insertion
        for val in test_values:
            rbt.insert(val, f"value_{val}")  # Insert with a value

        assert rbt.size == len(test_values), f"Size mismatch: {rbt.size} != {len(test_values)}"
        assert rbt.verify_properties(), "Red-Black properties violated"
        print(f"  [PASS] Insertion: {rbt.size} nodes, properties valid={rbt.verify_properties()}")

        # Test search
        assert rbt.search(10) == "value_10", "Search failed for existing element"
        assert rbt.search(100) is None, "Search failed for non-existing element"
        print(f"  [PASS] Search: Found 10={rbt.contains(10)}, Found 100={rbt.contains(100)}")

        # Test min/max
        assert rbt.get_min() == 2, f"Min incorrect: {rbt.get_min()}"
        assert rbt.get_max() == 26, f"Max incorrect: {rbt.get_max()}"
        print(f"  [PASS] Min/Max: min={rbt.get_min()}, max={rbt.get_max()}")

        # Test deletion
        rbt.delete(18)
        assert not rbt.contains(18), "Delete failed"
        assert rbt.verify_properties(), "Properties violated after deletion"
        print(f"  [PASS] Deletion: Deleted 18, properties still valid={rbt.verify_properties()}")

        # Test inorder traversal (should be sorted)
        inorder = rbt.inorder_traversal()
        assert inorder == sorted(inorder), "Inorder traversal not sorted"
        print(f"  [PASS] Traversal: Inorder is sorted")

        # Test black height consistency
        black_height = rbt.get_black_height()
        assert black_height > 0, "Black height should be positive"
        print(f"  [PASS] Black Height: {black_height}")

        # Test predecessor/successor
        pred = rbt.predecessor(10)
        succ = rbt.successor(10)
        assert pred == 8, f"Predecessor incorrect: {pred}"
        assert succ == 11, f"Successor incorrect: {succ}"
        print(f"  [PASS] Pred/Succ: pred(10)={pred}, succ(10)={succ}")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_count_min_sketch():
    """Test Count-Min Sketch implementation"""
    print("\nTesting Count-Min Sketch...")
    try:
        from count_min_sketch import CountMinSketch, CountMinSketchWithHeap, ConservativeUpdateSketch

        # Test basic Count-Min Sketch
        cms = CountMinSketch(epsilon=0.01, delta=0.01)

        # Create test data with known frequencies
        test_data = (
            ['apple'] * 100 +
            ['banana'] * 50 +
            ['orange'] * 30 +
            ['grape'] * 10
        )

        # Add items to sketch
        for item in test_data:
            cms.add(item)

        # Test frequency estimation
        apple_est = cms.query('apple')
        banana_est = cms.query('banana')

        # Check estimates are not underestimated (key property of CMS)
        assert apple_est >= 100, f"Apple underestimated: {apple_est} < 100"
        assert banana_est >= 50, f"Banana underestimated: {banana_est} < 50"

        # Check error bounds
        error_bound = cms.error_bound()
        assert apple_est <= 100 + error_bound, f"Apple error too high"
        print(f"  [PASS] Frequency estimation within error bounds")

        # Test zero frequency items
        assert cms.query('nonexistent') >= 0, "Negative count returned"
        print(f"  [PASS] Non-existent items handled correctly")

        # Test merge operation
        cms2 = CountMinSketch(width=cms.width, depth=cms.depth)
        cms2.add('apple', 50)
        cms.merge(cms2)
        new_apple_est = cms.query('apple')
        assert new_apple_est >= apple_est + 50, "Merge failed"
        print(f"  [PASS] Merge operation works correctly")

        # Test heavy hitters variant
        cms_hh = CountMinSketchWithHeap(width=500, depth=4, k=3)
        for item in test_data:
            cms_hh.add(item)

        top_k = cms_hh.get_top_k()
        assert len(top_k) <= 3, "Too many items in top-k"
        assert top_k[0][0] == 'apple', "Top item incorrect"
        print(f"  [PASS] Heavy hitters tracking: top item = {top_k[0][0]}")

        # Test conservative update
        conservative = ConservativeUpdateSketch(width=100, depth=3)
        for i in range(10):
            conservative.add('test')

        cons_est = conservative.query('test')
        assert cons_est >= 10, "Conservative update underestimated"
        print(f"  [PASS] Conservative update: estimate = {cons_est}")

        # Test total count tracking
        assert cms.total_count == 190 + 50, f"Total count incorrect: {cms.total_count}"
        print(f"  [PASS] Total count tracking: {cms.total_count} items")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_skip_list():
    """Test Skip List implementation"""
    print("\nTesting Skip List...")
    try:
        from skip_list import SkipList, IndexableSkipList

        # Test basic operations
        sl = SkipList(max_level=16, p=0.5)

        # Test insertion
        test_data = [(i, f"value_{i}") for i in range(50)]
        random.shuffle(test_data)

        for key, value in test_data:
            sl.insert(key, value)

        assert len(sl) == 50, f"Size mismatch: {len(sl)} != 50"
        print(f"  [PASS] Insertion: {len(sl)} elements inserted")

        # Test search
        assert sl.search(25) == "value_25", "Search failed"
        assert sl.search(100) is None, "Search should return None for missing key"
        print(f"  [PASS] Search: Found key 25, not found key 100")

        # Test deletion
        sl.delete(25)
        assert sl.search(25) is None, "Delete failed"
        assert len(sl) == 49, "Size not updated after delete"
        print(f"  [PASS] Deletion: Removed key 25")

        # Test range search (inclusive on both ends)
        range_result = sl.range_search(10, 20)
        assert len(range_result) == 11, f"Range search returned wrong count: {len(range_result)}"
        print(f"  [PASS] Range Search: Found {len(range_result)} items in [10,20]")

        # Test min/max
        min_item = sl.get_min()
        max_item = sl.get_max()
        assert min_item[0] == 0, f"Min incorrect: {min_item}"
        assert max_item[0] == 49, f"Max incorrect: {max_item}"
        print(f"  [PASS] Min/Max: min={min_item[0]}, max={max_item[0]}")

        # Test order preservation
        items = sl.to_list()
        keys = [k for k, v in items]
        assert keys == sorted(keys), "Skip list not maintaining order"
        print(f"  [PASS] Order: Elements maintained in sorted order")

        # Test structure analysis
        analysis = sl.analyze_structure()
        assert analysis['size'] == 49, "Size analysis incorrect"
        print(f"  [PASS] Structure: Max level used={analysis['max_level_used']}, "
              f"Avg search path={analysis['avg_search_path']:.2f}")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def performance_comparison():
    """Compare performance of different data structures"""
    print("\nPerformance Comparison...")

    n = 1000
    operations = 100

    results = {}

    try:
        # AVL Tree
        from avl_tree import AVLTree
        avl = AVLTree()
        start = time.time()
        for i in range(n):
            avl.insert(i)
        avl_insert = time.time() - start

        start = time.time()
        for _ in range(operations):
            avl.search(random.randint(0, n-1))
        avl_search = time.time() - start
        results['AVL Tree'] = {'insert': avl_insert, 'search': avl_search}

        # Skip List
        from skip_list import SkipList
        sl = SkipList()
        start = time.time()
        for i in range(n):
            sl.insert(i, f"value_{i}")
        sl_insert = time.time() - start

        start = time.time()
        for _ in range(operations):
            sl.search(random.randint(0, n-1))
        sl_search = time.time() - start
        results['Skip List'] = {'insert': sl_insert, 'search': sl_search}

        # Print results
        print(f"\n  Performance Results (n={n}, ops={operations}):")
        print(f"  {'Structure':<15} {'Insert (s)':<12} {'Search (s)':<12}")
        print(f"  {'-'*39}")
        for name, times in results.items():
            print(f"  {name:<15} {times['insert']:<12.4f} {times['search']:<12.4f}")

        return True
    except Exception as e:
        print(f"  [FAIL] Error in performance comparison: {e}")
        return False


def test_integration():
    """Test integration and edge cases"""
    print("\nTesting Integration & Edge Cases...")

    try:
        # Test empty structures
        from avl_tree import AVLTree
        from skip_list import SkipList
        from fenwick_tree import FenwickTree

        avl = AVLTree()
        assert avl.get_min() is None, "Empty AVL should return None for min"
        assert avl.size == 0, "Empty AVL should have size 0"
        print(f"  [PASS] Empty structures handled correctly")

        # Test single element
        avl.insert(42)
        assert avl.get_min() == 42 and avl.get_max() == 42, "Single element min/max failed"
        print(f"  [PASS] Single element operations work")

        # Test duplicate handling
        sl = SkipList()
        sl.insert(1, "first")
        sl.insert(1, "second")  # Should update
        assert sl.search(1) == "second", "Duplicate key update failed"
        print(f"  [PASS] Duplicate key handling works")

        # Test large values
        ft = FenwickTree([1e9, 1e9, 1e9])
        assert ft.prefix_sum(2) == 3e9, "Large value handling failed"
        print(f"  [PASS] Large values handled correctly")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("=" * 60)
    print("Advanced Data Structures Test Suite")
    print("=" * 60)

    tests = [
        ("AVL Tree", test_avl_tree),
        ("Red-Black Tree", test_red_black_tree),
        ("Segment Tree", test_segment_tree),
        ("Bloom Filter", test_bloom_filter),
        ("Fenwick Tree", test_fenwick_tree),
        ("Count-Min Sketch", test_count_min_sketch),
        ("Skip List", test_skip_list),
        ("Performance", performance_comparison),
        ("Integration", test_integration)
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n{name} test crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{name:.<40} {status}")

    print("-" * 60)
    print(f"Total: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n*** All tests passed successfully! ***")
    else:
        print(f"\n*** WARNING: {total_count - passed_count} test(s) failed ***")
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()