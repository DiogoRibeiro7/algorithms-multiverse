"""
Test suite for Cuckoo Hashing implementations.

Tests:
- Basic operations (insert, lookup, delete)
- Collision handling and displacement
- Rehashing behavior
- Stash functionality
- Cuckoo filter operations
- Performance characteristics

Author: Algorithms Multiverse
Date: January 2026
"""

import random
import time
import string
from typing import List, Tuple, Any
from cuckoo_hashing import CuckooHashTable, CuckooHashingWithStash, CuckooFilter


class TestCuckooHashing:
    """Test suite for Cuckoo Hashing implementations."""

    def test_basic_operations(self):
        """Test basic insert, lookup, and delete operations."""
        print("Testing Basic Operations")
        print("-" * 40)

        ch = CuckooHashTable(initial_capacity=16)

        # Test insert
        test_data = [
            (1, "one"), (2, "two"), (3, "three"),
            (4, "four"), (5, "five"), (6, "six")
        ]

        for key, value in test_data:
            ch.insert(key, value)

        print(f"Inserted {len(test_data)} items")

        # Test lookup
        successes = 0
        for key, expected_value in test_data:
            result = ch.lookup(key)
            if result == expected_value:
                successes += 1

        print(f"Lookup: {successes}/{len(test_data)} successful")

        # Test non-existent keys
        non_existent = [100, 200, 300]
        not_found = sum(1 for key in non_existent if ch.lookup(key) is None)
        print(f"Non-existent keys: {not_found}/{len(non_existent)} correctly not found")

        # Test delete
        delete_keys = [2, 4]
        delete_success = sum(1 for key in delete_keys if ch.delete(key))
        print(f"Delete: {delete_success}/{len(delete_keys)} successful")

        # Verify deletion
        deleted_not_found = sum(1 for key in delete_keys if ch.lookup(key) is None)
        print(f"Deleted keys: {deleted_not_found}/{len(delete_keys)} correctly not found")

        # Test update
        ch.insert(1, "ONE")
        updated = ch.lookup(1) == "ONE"
        print(f"Update existing key: {updated}")

        return successes == len(test_data) and deleted_not_found == len(delete_keys)

    def test_collision_handling(self):
        """Test collision resolution and displacement."""
        print("\nTesting Collision Handling")
        print("-" * 40)

        ch = CuckooHashTable(initial_capacity=8)

        # Insert items to force collisions
        items_to_insert = 12  # More than half capacity
        for i in range(items_to_insert):
            ch.insert(i, f"value_{i}")

        # Check all items are present
        all_present = all(ch.lookup(i) == f"value_{i}" for i in range(items_to_insert))
        print(f"All items present after collisions: {all_present}")

        stats = ch.get_statistics()
        print(f"Load factor: {stats['load_factor']:.2%}")
        print(f"Rehash count: {stats['rehash_count']}")
        print(f"Avg displacements: {stats['avg_displacements_per_insert']:.2f}")

        return all_present

    def test_rehashing(self):
        """Test automatic rehashing when needed."""
        print("\nTesting Rehashing")
        print("-" * 40)

        ch = CuckooHashTable(initial_capacity=4)

        # Insert enough items to trigger rehashing
        n = 20
        for i in range(n):
            ch.insert(f"key_{i}", i)

        # Verify all items are still present
        all_present = all(ch.lookup(f"key_{i}") == i for i in range(n))
        print(f"All items present after rehashing: {all_present}")

        stats = ch.get_statistics()
        print(f"Final capacity: {stats['capacity']}")
        print(f"Rehash count: {stats['rehash_count']}")
        print(f"Load factor: {stats['load_factor']:.2%}")

        return all_present and stats['rehash_count'] > 0

    def test_stash_variant(self):
        """Test cuckoo hashing with stash."""
        print("\nTesting Cuckoo Hashing with Stash")
        print("-" * 40)

        chs = CuckooHashingWithStash(initial_capacity=8, stash_size=2)

        # Insert items
        n = 15
        for i in range(n):
            chs.insert(i, f"stash_value_{i}")

        # Check all items
        all_present = all(chs.lookup(i) == f"stash_value_{i}" for i in range(n))
        print(f"All items present: {all_present}")

        stats = chs.get_statistics()
        print(f"Stash utilization: {stats['stash_utilization']:.0%}")
        print(f"Rehash count: {stats['rehash_count']}")

        # Test delete from stash
        # Force an item into stash by filling main table
        for i in range(n, n + 10):
            chs.insert(i, f"extra_{i}")

        # Delete some items
        deleted = chs.delete(5) and chs.delete(10)
        print(f"Delete from stash successful: {deleted}")

        return all_present

    def test_cuckoo_filter(self):
        """Test cuckoo filter operations."""
        print("\nTesting Cuckoo Filter")
        print("-" * 40)

        cf = CuckooFilter(capacity=100)

        # Insert items
        items = list(range(50))
        insert_success = sum(1 for item in items if cf.insert(item))
        print(f"Insert success: {insert_success}/{len(items)}")

        # Test membership
        present_count = sum(1 for item in items if item in cf)
        print(f"Membership test: {present_count}/{len(items)} found")

        # Test false positives
        non_existent = list(range(1000, 1100))
        false_positives = sum(1 for item in non_existent if item in cf)
        print(f"False positive rate: {false_positives}/{len(non_existent)} ({false_positives/len(non_existent):.1%})")

        # Test deletion
        items_to_delete = items[:10]
        delete_success = sum(1 for item in items_to_delete if cf.delete(item))
        print(f"Delete success: {delete_success}/{len(items_to_delete)}")

        # Verify deletion
        still_present = sum(1 for item in items_to_delete if item in cf)
        print(f"Items still present after delete: {still_present}/{len(items_to_delete)}")

        return present_count == len(items) and still_present == 0

    def test_dictionary_interface(self):
        """Test dictionary-style interface."""
        print("\nTesting Dictionary Interface")
        print("-" * 40)

        ch = CuckooHashTable()

        # Test __setitem__ and __getitem__
        ch["name"] = "Alice"
        ch["age"] = 30

        get_success = ch["name"] == "Alice" and ch["age"] == 30
        print(f"Get/Set operations: {get_success}")

        # Test __contains__
        contains_success = "name" in ch and "city" not in ch
        print(f"Contains operation: {contains_success}")

        # Test __delitem__
        del ch["age"]
        del_success = "age" not in ch
        print(f"Delete operation: {del_success}")

        # Test KeyError
        try:
            _ = ch["nonexistent"]
            key_error_raised = False
        except KeyError:
            key_error_raised = True

        print(f"KeyError raised for missing key: {key_error_raised}")

        return get_success and contains_success and del_success and key_error_raised

    def test_string_keys(self):
        """Test with string keys."""
        print("\nTesting String Keys")
        print("-" * 40)

        ch = CuckooHashTable()

        # Generate random strings
        strings = [''.join(random.choices(string.ascii_letters, k=10))
                  for _ in range(20)]

        # Insert
        for s in strings:
            ch.insert(s, f"value_{s}")

        # Verify
        all_present = all(ch.lookup(s) == f"value_{s}" for s in strings)
        print(f"All string keys present: {all_present}")

        stats = ch.get_statistics()
        print(f"Load factor with strings: {stats['load_factor']:.2%}")

        return all_present

    def test_worst_case_lookup(self):
        """Verify O(1) worst-case lookup time."""
        print("\nTesting Worst-Case Lookup Time")
        print("-" * 40)

        ch = CuckooHashTable(initial_capacity=10000)

        # Insert many items
        n = 5000
        for i in range(n):
            ch.insert(i, i)

        # Measure lookup times
        lookup_times = []

        for _ in range(100):
            key = random.randint(0, n - 1)
            start = time.perf_counter()
            _ = ch.lookup(key)
            end = time.perf_counter()
            lookup_times.append(end - start)

        max_time = max(lookup_times)
        avg_time = sum(lookup_times) / len(lookup_times)

        # Check that max is not much worse than average (constant time)
        ratio = max_time / avg_time if avg_time > 0 else 1
        is_constant = ratio < 10  # Max should be within order of magnitude

        print(f"Avg lookup time: {avg_time*1000000:.2f} us")
        print(f"Max lookup time: {max_time*1000000:.2f} us")
        print(f"Max/Avg ratio: {ratio:.2f}")
        print(f"Appears constant time: {is_constant}")

        return is_constant

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        print("\nTesting Edge Cases")
        print("-" * 40)

        # Empty table
        ch = CuckooHashTable()
        empty_lookup = ch.lookup(1) is None
        empty_delete = not ch.delete(1)
        print(f"Empty table handled correctly: {empty_lookup and empty_delete}")

        # Single element
        ch.insert(42, "answer")
        single_lookup = ch.lookup(42) == "answer"
        print(f"Single element: {single_lookup}")

        # Delete only element
        ch.delete(42)
        after_delete = ch.lookup(42) is None
        print(f"After deleting only element: {after_delete}")

        # Duplicate keys
        ch.insert(1, "first")
        ch.insert(1, "second")
        duplicate_update = ch.lookup(1) == "second"
        print(f"Duplicate key updates value: {duplicate_update}")

        # None as value
        ch.insert("key", None)
        none_value = ch.lookup("key") is None
        print(f"None as value handled: {none_value}")

        return all([empty_lookup, empty_delete, single_lookup, after_delete,
                   duplicate_update, none_value])

    def test_performance_comparison(self):
        """Compare performance with Python dict."""
        print("\nPerformance Comparison with Python dict")
        print("-" * 40)

        sizes = [1000, 5000, 10000]

        for size in sizes:
            print(f"\nSize: {size}")

            # Generate data
            keys = list(range(size))
            random.shuffle(keys)

            # Cuckoo Hash
            ch = CuckooHashTable(initial_capacity=size * 2)
            start = time.time()
            for key in keys:
                ch.insert(key, key)
            ch_insert = time.time() - start

            start = time.time()
            for key in keys[:100]:
                _ = ch.lookup(key)
            ch_lookup = (time.time() - start) * (size / 100)

            # Python dict
            d = {}
            start = time.time()
            for key in keys:
                d[key] = key
            dict_insert = time.time() - start

            start = time.time()
            for key in keys[:100]:
                _ = d[key]
            dict_lookup = (time.time() - start) * (size / 100)

            print(f"  Cuckoo - Insert: {ch_insert:.4f}s, Lookup: {ch_lookup:.4f}s")
            print(f"  Dict   - Insert: {dict_insert:.4f}s, Lookup: {dict_lookup:.4f}s")
            print(f"  Ratio  - Insert: {ch_insert/dict_insert:.2f}x, Lookup: {ch_lookup/dict_lookup:.2f}x")

    def run_all_tests(self):
        """Run all tests."""
        print("=" * 50)
        print("CUCKOO HASHING TEST SUITE")
        print("=" * 50)

        tests = [
            self.test_basic_operations,
            self.test_collision_handling,
            self.test_rehashing,
            self.test_stash_variant,
            self.test_cuckoo_filter,
            self.test_dictionary_interface,
            self.test_string_keys,
            self.test_worst_case_lookup,
            self.test_edge_cases,
            self.test_performance_comparison
        ]

        passed = 0
        failed = 0

        for test in tests:
            try:
                result = test()
                if result is not False:
                    print(f"[PASS] {test.__name__}")
                    passed += 1
                else:
                    print(f"[FAIL] {test.__name__}")
                    failed += 1
            except Exception as e:
                print(f"[ERROR] {test.__name__}: {e}")
                failed += 1

        print("\n" + "=" * 50)
        print(f"TEST SUMMARY: {passed} passed, {failed} failed")
        print("=" * 50)


def verify_worst_case_guarantee():
    """Verify the O(1) worst-case lookup guarantee."""
    print("\nVerifying O(1) Worst-Case Guarantee")
    print("=" * 50)

    ch = CuckooHashTable(initial_capacity=100000)

    # Insert many items
    n = 50000
    print(f"Inserting {n} items...")
    for i in range(n):
        ch.insert(i, i)

    print(f"Load factor: {ch.get_load_factor():.2%}")
    print(f"Rehashes: {ch.get_statistics()['rehash_count']}")

    # Perform many lookups and track times
    print("\nPerforming 10000 random lookups...")
    times = []

    for _ in range(10000):
        key = random.randint(0, n - 1)
        start = time.perf_counter()
        _ = ch.lookup(key)
        end = time.perf_counter()
        times.append((end - start) * 1000000)  # Convert to microseconds

    # Analyze times
    avg_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)

    # Check variance
    variance = sum((t - avg_time) ** 2 for t in times) / len(times)
    std_dev = variance ** 0.5

    print(f"\nLookup Time Statistics (microseconds):")
    print(f"  Average: {avg_time:.2f}")
    print(f"  Minimum: {min_time:.2f}")
    print(f"  Maximum: {max_time:.2f}")
    print(f"  Std Dev: {std_dev:.2f}")
    print(f"  Max/Avg ratio: {max_time/avg_time:.2f}")

    # In true O(1) worst case, max should be close to average
    is_constant = (max_time / avg_time) < 5
    print(f"\nWorst-case appears O(1): {is_constant}")

    return is_constant


if __name__ == "__main__":
    # Run test suite
    tester = TestCuckooHashing()
    tester.run_all_tests()

    # Verify worst-case guarantee
    print("\n")
    verify_worst_case_guarantee()