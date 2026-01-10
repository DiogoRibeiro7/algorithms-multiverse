"""
Test suite for B-Tree and B+ Tree implementations.

Comprehensive tests including:
- Basic operations (insert, search, delete)
- Edge cases (empty tree, single element, duplicates)
- Large dataset handling
- Performance comparisons
- Property validation

Author: Algorithms Multiverse
Date: January 2026
"""

import time
import random
import string
from typing import List, Tuple, Any
from btree import BTree
from bplus_tree import BPlusTree


class TestBTrees:
    """Test suite for B-Tree and B+ Tree implementations."""

    @staticmethod
    def generate_random_data(n: int, key_type: str = 'int') -> List[Tuple[Any, str]]:
        """Generate random test data."""
        if key_type == 'int':
            keys = list(range(n))
            random.shuffle(keys)
        elif key_type == 'string':
            keys = [''.join(random.choices(string.ascii_letters, k=10)) for _ in range(n)]
        else:
            keys = [random.random() for _ in range(n)]

        return [(key, f"value_{key}") for key in keys]

    def test_basic_operations(self):
        """Test basic insert, search, and delete operations."""
        print("Testing Basic Operations")
        print("-" * 40)

        # Test both B-Tree and B+ Tree
        trees = [
            ("B-Tree", BTree(order=5)),
            ("B+ Tree", BPlusTree(order=5))
        ]

        for tree_name, tree in trees:
            print(f"\n{tree_name}:")

            # Insert
            test_data = [(10, "ten"), (20, "twenty"), (5, "five"),
                        (15, "fifteen"), (25, "twenty-five")]

            for key, value in test_data:
                tree.insert(key, value)

            print(f"  Inserted {len(test_data)} items")

            # Search
            successes = 0
            for key, expected_value in test_data:
                result = tree.search(key)
                if result == expected_value:
                    successes += 1

            print(f"  Search: {successes}/{len(test_data)} successful")

            # Search non-existent
            non_existent = [100, 200, 300]
            not_found = sum(1 for key in non_existent if tree.search(key) is None)
            print(f"  Non-existent keys: {not_found}/{len(non_existent)} correctly not found")

            # Delete
            delete_keys = [10, 15]
            delete_success = sum(1 for key in delete_keys if tree.delete(key))
            print(f"  Delete: {delete_success}/{len(delete_keys)} successful")

            # Verify deletion
            deleted_not_found = sum(1 for key in delete_keys if tree.search(key) is None)
            print(f"  Deleted keys: {deleted_not_found}/{len(delete_keys)} correctly not found")

            # Validate tree structure
            is_valid = tree.validate()
            print(f"  Tree valid after operations: {is_valid}")

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        print("\nTesting Edge Cases")
        print("-" * 40)

        trees = [
            ("B-Tree", BTree(order=3)),
            ("B+ Tree", BPlusTree(order=3))
        ]

        for tree_name, tree in trees:
            print(f"\n{tree_name}:")

            # Empty tree
            print(f"  Empty tree search: {tree.search(1)}")
            print(f"  Empty tree delete: {tree.delete(1)}")

            # Single element
            tree.insert(42, "answer")
            print(f"  Single element search: {tree.search(42) == 'answer'}")

            # Duplicate keys (update)
            tree.insert(42, "updated")
            print(f"  Duplicate key update: {tree.search(42) == 'updated'}")

            # Delete only element
            tree.delete(42)
            print(f"  After deleting only element: {tree.search(42) is None}")

            # Minimum order tree
            min_tree = BTree(order=3) if tree_name == "B-Tree" else BPlusTree(order=3)
            for i in range(10):
                min_tree.insert(i, f"val_{i}")
            print(f"  Minimum order tree valid: {min_tree.validate()}")

    def test_range_queries(self):
        """Test range query functionality."""
        print("\nTesting Range Queries")
        print("-" * 40)

        trees = [
            ("B-Tree", BTree(order=5)),
            ("B+ Tree", BPlusTree(order=5))
        ]

        # Insert test data
        test_data = list(range(0, 100, 5))
        for tree_name, tree in trees:
            for val in test_data:
                tree.insert(val, f"value_{val}")

            print(f"\n{tree_name}:")

            # Different range queries
            ranges = [
                (10, 30),
                (0, 15),
                (85, 100),
                (40, 40),  # Single value
                (100, 200)  # Out of range
            ]

            for min_key, max_key in ranges:
                result = tree.range_query(min_key, max_key)
                expected = [(k, f"value_{k}") for k in test_data
                           if min_key <= k <= max_key]
                matches = len(result) == len(expected)
                print(f"  Range [{min_key}, {max_key}]: {len(result)} items (correct: {matches})")

    def test_bulk_loading(self):
        """Test bulk loading functionality."""
        print("\nTesting Bulk Loading")
        print("-" * 40)

        n = 1000
        sorted_data = [(i, f"value_{i}") for i in range(n)]
        random_data = sorted_data.copy()
        random.shuffle(random_data)

        configs = [
            ("B-Tree sorted", BTree(order=10), sorted_data, True),
            ("B-Tree random", BTree(order=10), random_data, False),
            ("B+ Tree sorted", BPlusTree(order=10), sorted_data, True),
            ("B+ Tree random", BPlusTree(order=10), random_data, False)
        ]

        for name, tree, data, is_sorted in configs:
            start_time = time.time()
            tree.bulk_load(data, sorted_input=is_sorted)
            load_time = time.time() - start_time

            # Verify all data
            correct = sum(1 for key, expected_val in data
                         if tree.search(key) == expected_val)

            print(f"\n{name}:")
            print(f"  Load time: {load_time:.4f}s")
            print(f"  Verification: {correct}/{n} items correct")
            print(f"  Tree valid: {tree.validate()}")

            stats = tree.get_statistics()
            print(f"  Height: {stats['height']}")
            print(f"  Space utilization: {stats['space_utilization']:.2%}")

    def test_performance_comparison(self):
        """Compare performance between B-Tree and B+ Tree."""
        print("\nPerformance Comparison")
        print("-" * 40)

        sizes = [100, 1000, 5000]
        operations = ['insert', 'search', 'delete', 'range_query']

        for size in sizes:
            print(f"\nDataset size: {size}")
            data = self.generate_random_data(size)

            trees = [
                ("B-Tree", BTree(order=50)),
                ("B+ Tree", BPlusTree(order=50))
            ]

            for tree_name, tree in trees:
                times = {}

                # Insert
                start = time.time()
                for key, value in data:
                    tree.insert(key, value)
                times['insert'] = time.time() - start

                # Search
                start = time.time()
                for key, _ in data[:100]:  # Search first 100
                    tree.search(key)
                times['search'] = (time.time() - start) * (size / 100)

                # Range query
                start = time.time()
                tree.range_query(size // 4, size // 2)
                times['range_query'] = time.time() - start

                # Delete
                start = time.time()
                for key, _ in data[:100]:  # Delete first 100
                    tree.delete(key)
                times['delete'] = (time.time() - start) * (size / 100)

                print(f"\n  {tree_name}:")
                for op in operations:
                    if op in times:
                        print(f"    {op}: {times[op]:.6f}s")

    def test_ordered_operations(self):
        """Test operations with ordered data."""
        print("\nTesting Ordered Operations")
        print("-" * 40)

        trees = [
            ("B-Tree", BTree(order=5)),
            ("B+ Tree", BPlusTree(order=5))
        ]

        for tree_name, tree in trees:
            print(f"\n{tree_name}:")

            # Insert in ascending order
            ascending = list(range(50))
            for val in ascending:
                tree.insert(val, f"asc_{val}")

            print(f"  Ascending insert complete")
            print(f"  Tree valid: {tree.validate()}")
            print(f"  Height: {tree.get_height()}")

            # Clear and insert in descending order
            tree_desc = BTree(order=5) if tree_name == "B-Tree" else BPlusTree(order=5)
            descending = list(range(49, -1, -1))
            for val in descending:
                tree_desc.insert(val, f"desc_{val}")

            print(f"  Descending insert complete")
            print(f"  Tree valid: {tree_desc.validate()}")
            print(f"  Height: {tree_desc.get_height()}")

    def test_tree_properties(self):
        """Test and verify tree properties."""
        print("\nTesting Tree Properties")
        print("-" * 40)

        orders = [3, 5, 10, 50]
        n = 1000

        for order in orders:
            trees = [
                ("B-Tree", BTree(order=order)),
                ("B+ Tree", BPlusTree(order=order))
            ]

            for tree_name, tree in trees:
                # Insert data
                for i in range(n):
                    tree.insert(i, f"val_{i}")

                stats = tree.get_statistics()
                height = stats['height']

                # Theoretical bounds
                import math
                min_height = math.ceil(math.log(n + 1, order)) - 1
                max_height = math.floor(math.log((n + 1) / 2, math.ceil(order / 2)))

                print(f"\n{tree_name} (order={order}):")
                print(f"  Actual height: {height}")
                print(f"  Theoretical min: {min_height}")
                print(f"  Theoretical max: {max_height}")
                print(f"  Within bounds: {min_height <= height <= max_height}")
                print(f"  Space utilization: {stats['space_utilization']:.2%}")

    def test_iterator_bplus(self):
        """Test B+ Tree iterator functionality."""
        print("\nTesting B+ Tree Iterator")
        print("-" * 40)

        bplus = BPlusTree(order=5)
        data = [(i, f"val_{i}") for i in range(20)]
        random.shuffle(data)

        for key, value in data:
            bplus.insert(key, value)

        # Test iterator
        print("\nIterating through B+ Tree:")
        sorted_items = list(bplus)
        print(f"  Total items: {len(sorted_items)}")

        # Verify order
        is_sorted = all(sorted_items[i][0] <= sorted_items[i + 1][0]
                       for i in range(len(sorted_items) - 1))
        print(f"  Correctly sorted: {is_sorted}")

        # Test partial iteration
        first_five = []
        for i, (key, value) in enumerate(bplus):
            if i >= 5:
                break
            first_five.append(key)
        print(f"  First 5 keys: {first_five}")

    def run_all_tests(self):
        """Run all tests."""
        print("=" * 50)
        print("B-TREE AND B+ TREE TEST SUITE")
        print("=" * 50)

        tests = [
            self.test_basic_operations,
            self.test_edge_cases,
            self.test_range_queries,
            self.test_bulk_loading,
            self.test_ordered_operations,
            self.test_tree_properties,
            self.test_iterator_bplus,
            self.test_performance_comparison
        ]

        for test in tests:
            try:
                test()
                print(f"\n[PASS] {test.__name__} passed")
            except Exception as e:
                print(f"\n[FAIL] {test.__name__} failed: {e}")

        print("\n" + "=" * 50)
        print("TEST SUITE COMPLETE")
        print("=" * 50)


def benchmark_comparison():
    """Detailed performance benchmark between B-Tree and B+ Tree."""
    print("\nDETAILED PERFORMANCE BENCHMARK")
    print("=" * 50)

    sizes = [1000, 5000, 10000, 50000]
    order = 100  # Large order for database simulation

    results = []

    for size in sizes:
        print(f"\nTesting with {size} items (order={order})...")

        # Generate test data
        data = [(i, f"value_{i}") for i in range(size)]
        random_data = data.copy()
        random.shuffle(random_data)

        # B-Tree tests
        btree = BTree(order=order)
        btree_times = {}

        # Insert (random order)
        start = time.time()
        for key, value in random_data:
            btree.insert(key, value)
        btree_times['insert'] = time.time() - start

        # Sequential search
        start = time.time()
        for i in range(min(1000, size)):
            btree.search(i)
        btree_times['search'] = (time.time() - start) * (size / min(1000, size))

        # Range query (25% of data)
        start = time.time()
        btree.range_query(size // 4, size // 2)
        btree_times['range'] = time.time() - start

        # B+ Tree tests
        bplus = BPlusTree(order=order)
        bplus_times = {}

        # Insert (random order)
        start = time.time()
        for key, value in random_data:
            bplus.insert(key, value)
        bplus_times['insert'] = time.time() - start

        # Sequential search
        start = time.time()
        for i in range(min(1000, size)):
            bplus.search(i)
        bplus_times['search'] = (time.time() - start) * (size / min(1000, size))

        # Range query (25% of data)
        start = time.time()
        bplus.range_query(size // 4, size // 2)
        bplus_times['range'] = time.time() - start

        # Sequential scan (B+ Tree advantage)
        start = time.time()
        count = sum(1 for _ in bplus)
        bplus_times['sequential'] = time.time() - start

        # Results
        print(f"\nB-Tree:")
        print(f"  Insert: {btree_times['insert']:.4f}s")
        print(f"  Search: {btree_times['search']:.4f}s")
        print(f"  Range: {btree_times['range']:.4f}s")
        print(f"  Height: {btree.get_height()}")

        print(f"\nB+ Tree:")
        print(f"  Insert: {bplus_times['insert']:.4f}s")
        print(f"  Search: {bplus_times['search']:.4f}s")
        print(f"  Range: {bplus_times['range']:.4f}s ({bplus_times['range'] / btree_times['range']:.2f}x)")
        print(f"  Sequential: {bplus_times['sequential']:.4f}s")
        print(f"  Height: {bplus.get_height()}")

        # Memory efficiency (approximate)
        btree_stats = btree.get_statistics()
        bplus_stats = bplus.get_statistics()

        print(f"\nSpace Utilization:")
        print(f"  B-Tree: {btree_stats['space_utilization']:.2%}")
        print(f"  B+ Tree: {bplus_stats['space_utilization']:.2%}")

    print("\n" + "=" * 50)
    print("BENCHMARK COMPLETE")


if __name__ == "__main__":
    # Run test suite
    tester = TestBTrees()
    tester.run_all_tests()

    # Run detailed benchmark
    print("\n" * 2)
    benchmark_comparison()