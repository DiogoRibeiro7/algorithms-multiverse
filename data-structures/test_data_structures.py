"""
Comprehensive Test Suite for Data Structures

Tests all Python data structure implementations:
- BinaryTree (binary_tree.py)
- Hash Tables: Chaining, Open Addressing, Robin Hood, ThreadSafe, ConsistentHashRing (hashtable.py)
- Linked Lists: Singly, Doubly, Circular, SkipList (linkedlist.py)
- Tries: Trie, PatriciaTrie, SuffixTrie, SpellChecker, AutoComplete, Dictionary (trie.py)

Run with:
    python -m pytest test_data_structures.py -v
    or
    python test_data_structures.py
"""

import sys
import os
import unittest
import json
import random
import threading

sys.path.insert(0, os.path.dirname(__file__))

from binary_tree import BinaryTree, TreeNode
from hashtable import (
    ChainingHashTable,
    OpenAddressingHashTable,
    RobinHoodHashTable,
    ThreadSafeHashTable,
    ConsistentHashRing,
    HashFunction,
)
from linkedlist import (
    SinglyLinkedList,
    DoublyLinkedList,
    CircularLinkedList,
    SkipList,
)
from trie import (
    Trie,
    PatriciaTrie,
    SuffixTrie,
    SpellChecker,
    AutoComplete,
    Dictionary,
)


# ============================================================================
# BINARY TREE TESTS
# ============================================================================


class TestBinaryTreeEmpty(unittest.TestCase):
    """Test BinaryTree edge cases with empty tree."""

    def setUp(self):
        self.tree = BinaryTree()

    def test_empty_tree_size(self):
        self.assertEqual(len(self.tree), 0)

    def test_empty_tree_bool(self):
        self.assertFalse(bool(self.tree))

    def test_empty_tree_height(self):
        self.assertEqual(self.tree.height(), -1)

    def test_empty_tree_search(self):
        self.assertFalse(self.tree.search(42))

    def test_empty_tree_contains(self):
        self.assertNotIn(42, self.tree)

    def test_empty_tree_delete(self):
        self.assertFalse(self.tree.delete(42))

    def test_empty_tree_traversals(self):
        self.assertEqual(list(self.tree.inorder_traversal()), [])
        self.assertEqual(list(self.tree.preorder_traversal()), [])
        self.assertEqual(list(self.tree.postorder_traversal()), [])
        self.assertEqual(list(self.tree.level_order_traversal()), [])

    def test_empty_tree_to_list(self):
        self.assertEqual(self.tree.to_list(), [])

    def test_empty_tree_count_leaves(self):
        self.assertEqual(self.tree.count_leaves(), 0)

    def test_empty_tree_iterator(self):
        self.assertEqual(list(self.tree), [])


class TestBinaryTreeSingleElement(unittest.TestCase):
    """Test BinaryTree with a single element."""

    def setUp(self):
        self.tree = BinaryTree()
        self.tree.insert(42)

    def test_single_size(self):
        self.assertEqual(len(self.tree), 1)

    def test_single_bool(self):
        self.assertTrue(bool(self.tree))

    def test_single_height(self):
        self.assertEqual(self.tree.height(), 0)

    def test_single_search(self):
        self.assertTrue(self.tree.search(42))
        self.assertFalse(self.tree.search(99))

    def test_single_is_balanced(self):
        self.assertTrue(self.tree.is_balanced())

    def test_single_count_leaves(self):
        self.assertEqual(self.tree.count_leaves(), 1)

    def test_single_delete(self):
        self.assertTrue(self.tree.delete(42))
        self.assertEqual(len(self.tree), 0)
        self.assertFalse(self.tree.search(42))

    def test_single_depth(self):
        self.assertEqual(self.tree.depth(42), 0)


class TestBinaryTreeCRUD(unittest.TestCase):
    """Test BinaryTree CRUD operations."""

    def setUp(self):
        self.tree = BinaryTree()
        self.values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
        for v in self.values:
            self.tree.insert(v)

    def test_insert_and_size(self):
        self.assertEqual(len(self.tree), len(self.values))

    def test_search_existing(self):
        for v in self.values:
            self.assertTrue(self.tree.search(v), f"Failed to find {v}")

    def test_search_nonexistent(self):
        self.assertFalse(self.tree.search(99))
        self.assertFalse(self.tree.search(-1))
        self.assertFalse(self.tree.search(0))

    def test_contains_operator(self):
        self.assertIn(50, self.tree)
        self.assertNotIn(99, self.tree)

    def test_delete_leaf(self):
        self.assertTrue(self.tree.delete(10))
        self.assertEqual(len(self.tree), len(self.values) - 1)
        self.assertFalse(self.tree.search(10))

    def test_delete_node_one_child(self):
        self.assertTrue(self.tree.delete(20))
        self.assertFalse(self.tree.search(20))
        self.assertTrue(self.tree.search(10))
        self.assertTrue(self.tree.search(25))

    def test_delete_node_two_children(self):
        self.assertTrue(self.tree.delete(30))
        self.assertFalse(self.tree.search(30))
        # Children should still be accessible
        self.assertTrue(self.tree.search(20))
        self.assertTrue(self.tree.search(40))

    def test_delete_root(self):
        self.assertTrue(self.tree.delete(50))
        self.assertFalse(self.tree.search(50))
        self.assertEqual(len(self.tree), len(self.values) - 1)
        # Other nodes still accessible
        self.assertTrue(self.tree.search(30))
        self.assertTrue(self.tree.search(70))

    def test_delete_nonexistent(self):
        self.assertFalse(self.tree.delete(99))
        self.assertEqual(len(self.tree), len(self.values))

    def test_insert_duplicates(self):
        self.tree.insert(50)
        self.assertEqual(len(self.tree), len(self.values) + 1)


class TestBinaryTreeTraversals(unittest.TestCase):
    """Test BinaryTree traversal methods."""

    def setUp(self):
        self.tree = BinaryTree()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            self.tree.insert(v)

    def test_inorder_is_sorted(self):
        result = list(self.tree.inorder_traversal())
        self.assertEqual(result, sorted(result))

    def test_preorder_root_first(self):
        result = list(self.tree.preorder_traversal())
        self.assertEqual(result[0], 50)

    def test_postorder_root_last(self):
        result = list(self.tree.postorder_traversal())
        self.assertEqual(result[-1], 50)

    def test_level_order(self):
        result = list(self.tree.level_order_traversal())
        self.assertEqual(result[0], 50)
        # Level 1 should contain 30 and 70
        self.assertIn(30, result[1:3])
        self.assertIn(70, result[1:3])

    def test_iterator_is_inorder(self):
        self.assertEqual(list(self.tree), list(self.tree.inorder_traversal()))

    def test_to_list_sorted(self):
        self.assertEqual(self.tree.to_list(), [20, 30, 40, 50, 60, 70, 80])


class TestBinaryTreeUtilities(unittest.TestCase):
    """Test BinaryTree utility methods."""

    def setUp(self):
        self.tree = BinaryTree()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            self.tree.insert(v)

    def test_height(self):
        self.assertEqual(self.tree.height(), 2)

    def test_depth_root(self):
        self.assertEqual(self.tree.depth(50), 0)

    def test_depth_leaves(self):
        self.assertEqual(self.tree.depth(20), 2)
        self.assertEqual(self.tree.depth(80), 2)

    def test_depth_nonexistent(self):
        self.assertEqual(self.tree.depth(99), -1)

    def test_is_balanced(self):
        self.assertTrue(self.tree.is_balanced())

    def test_count_nodes(self):
        self.assertEqual(self.tree.count_nodes(), 7)

    def test_count_leaves(self):
        self.assertEqual(self.tree.count_leaves(), 4)

    def test_get_level_nodes(self):
        self.assertEqual(self.tree.get_level_nodes(0), [50])
        self.assertEqual(sorted(self.tree.get_level_nodes(1)), [30, 70])
        self.assertEqual(sorted(self.tree.get_level_nodes(2)), [20, 40, 60, 80])

    def test_to_json(self):
        json_str = self.tree.to_json()
        data = json.loads(json_str)
        self.assertEqual(data["data"], 50)
        self.assertIn("left", data)
        self.assertIn("right", data)

    def test_str_repr(self):
        s = str(self.tree)
        r = repr(self.tree)
        self.assertIn("20", s)
        self.assertIn("BinaryTree", r)


class TestBinaryTreePropertyInvariants(unittest.TestCase):
    """Test BST property: left < root <= right after operations."""

    def test_bst_invariant_after_insertions(self):
        tree = BinaryTree()
        random.seed(42)
        values = random.sample(range(1000), 100)
        for v in values:
            tree.insert(v)
        result = list(tree.inorder_traversal())
        self.assertEqual(result, sorted(result))

    def test_bst_invariant_after_deletions(self):
        tree = BinaryTree()
        random.seed(42)
        values = random.sample(range(1000), 100)
        for v in values:
            tree.insert(v)

        to_delete = random.sample(values, 50)
        for v in to_delete:
            tree.delete(v)

        result = list(tree.inorder_traversal())
        self.assertEqual(result, sorted(result))


# ============================================================================
# HASH TABLE TESTS
# ============================================================================


class TestHashFunction(unittest.TestCase):
    """Test hash function implementations."""

    def test_djb2_deterministic(self):
        self.assertEqual(HashFunction.djb2("hello"), HashFunction.djb2("hello"))

    def test_fnv1a_deterministic(self):
        self.assertEqual(HashFunction.fnv1a("hello"), HashFunction.fnv1a("hello"))

    def test_murmur3_deterministic(self):
        self.assertEqual(HashFunction.murmur3("hello"), HashFunction.murmur3("hello"))

    def test_polynomial_rolling_deterministic(self):
        self.assertEqual(
            HashFunction.polynomial_rolling("hello"),
            HashFunction.polynomial_rolling("hello"),
        )

    def test_different_keys_different_hashes(self):
        h1 = HashFunction.fnv1a("hello")
        h2 = HashFunction.fnv1a("world")
        self.assertNotEqual(h1, h2)


class _HashTableTestMixin:
    """Shared tests for all hash table implementations."""

    def create_table(self):
        raise NotImplementedError

    def setUp(self):
        self.table = self.create_table()

    def test_empty_table(self):
        self.assertEqual(len(self.table), 0)

    def test_put_and_get(self):
        self.table.put("key1", "value1")
        self.assertEqual(self.table.get("key1"), "value1")

    def test_put_returns_none_for_new(self):
        result = self.table.put("key1", "value1")
        self.assertIsNone(result)

    def test_put_returns_old_value_on_update(self):
        self.table.put("key1", "value1")
        old = self.table.put("key1", "value2")
        self.assertEqual(old, "value1")
        self.assertEqual(self.table.get("key1"), "value2")

    def test_get_nonexistent(self):
        self.assertIsNone(self.table.get("missing"))

    def test_remove(self):
        self.table.put("key1", "value1")
        removed = self.table.remove("key1")
        self.assertEqual(removed, "value1")
        self.assertIsNone(self.table.get("key1"))
        self.assertEqual(len(self.table), 0)

    def test_remove_nonexistent(self):
        self.assertIsNone(self.table.remove("missing"))

    def test_len(self):
        for i in range(10):
            self.table.put(f"key{i}", i)
        self.assertEqual(len(self.table), 10)

    def test_many_insertions_trigger_resize(self):
        for i in range(100):
            self.table.put(f"key{i}", i)
        self.assertEqual(len(self.table), 100)
        for i in range(100):
            self.assertEqual(self.table.get(f"key{i}"), i)

    def test_iteration(self):
        for i in range(5):
            self.table.put(f"key{i}", i)
        items = list(self.table)
        self.assertEqual(len(items), 5)
        keys = {k for k, v in items}
        self.assertEqual(keys, {f"key{i}" for i in range(5)})

    def test_insert_remove_insert(self):
        self.table.put("key", "v1")
        self.table.remove("key")
        self.table.put("key", "v2")
        self.assertEqual(self.table.get("key"), "v2")


class TestChainingHashTable(_HashTableTestMixin, unittest.TestCase):
    def create_table(self):
        return ChainingHashTable()

    def test_contains(self):
        self.table.put("key1", "value1")
        self.assertTrue(self.table.contains("key1"))
        self.assertFalse(self.table.contains("key2"))

    def test_keys_values_items(self):
        for i in range(5):
            self.table.put(f"k{i}", i)
        keys = set(self.table.keys())
        values = set(self.table.values())
        self.assertEqual(keys, {f"k{i}" for i in range(5)})
        self.assertEqual(values, set(range(5)))

    def test_clear(self):
        for i in range(10):
            self.table.put(f"key{i}", i)
        self.table.clear()
        self.assertEqual(len(self.table), 0)
        self.assertIsNone(self.table.get("key0"))

    def test_get_stats(self):
        for i in range(10):
            self.table.put(f"key{i}", i)
        stats = self.table.get_stats()
        self.assertEqual(stats["size"], 10)
        self.assertIn("capacity", stats)
        self.assertIn("collisions", stats)

    def test_custom_hash_function(self):
        table = ChainingHashTable(hash_func=HashFunction.djb2)
        table.put("test", 123)
        self.assertEqual(table.get("test"), 123)


class TestOpenAddressingHashTable(_HashTableTestMixin, unittest.TestCase):
    def create_table(self):
        return OpenAddressingHashTable()

    def test_contains(self):
        self.table.put("key1", "value1")
        self.assertTrue(self.table.contains("key1"))
        self.assertFalse(self.table.contains("key2"))

    def test_tombstone_handling(self):
        """Verify that deletion with tombstones doesn't break lookups."""
        self.table.put("a", 1)
        self.table.put("b", 2)
        self.table.put("c", 3)
        self.table.remove("b")
        self.assertEqual(self.table.get("c"), 3)
        self.assertIsNone(self.table.get("b"))

    def test_get_stats(self):
        stats = self.table.get_stats()
        self.assertIn("size", stats)
        self.assertIn("deleted_count", stats)


class TestRobinHoodHashTable(_HashTableTestMixin, unittest.TestCase):
    def create_table(self):
        return RobinHoodHashTable()

    def test_get_stats(self):
        for i in range(20):
            self.table.put(f"key{i}", i)
        stats = self.table.get_stats()
        self.assertEqual(stats["size"], 20)
        self.assertIn("max_psl", stats)
        self.assertIn("avg_psl", stats)


class TestThreadSafeHashTable(unittest.TestCase):
    """Test thread-safe hash table variant."""

    def setUp(self):
        self.table = ThreadSafeHashTable()

    def test_basic_operations(self):
        self.table.put("key", "value")
        self.assertEqual(self.table.get("key"), "value")
        self.table.remove("key")
        self.assertIsNone(self.table.get("key"))

    def test_concurrent_puts(self):
        errors = []

        def writer(start):
            try:
                for i in range(100):
                    self.table.put(f"key_{start}_{i}", i)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=writer, args=(t,)) for t in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(self.table), 400)

    def test_concurrent_reads_and_writes(self):
        for i in range(100):
            self.table.put(f"key{i}", i)

        errors = []

        def reader():
            try:
                for i in range(100):
                    self.table.get(f"key{i}")
            except Exception as e:
                errors.append(e)

        def writer():
            try:
                for i in range(100, 200):
                    self.table.put(f"key{i}", i)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=reader) for _ in range(3)]
        threads.append(threading.Thread(target=writer))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0)


class TestConsistentHashRing(unittest.TestCase):
    """Test consistent hash ring for distributed systems."""

    def test_empty_ring(self):
        ring = ConsistentHashRing()
        self.assertIsNone(ring.get_node("key"))

    def test_single_node(self):
        ring = ConsistentHashRing(["server1"])
        self.assertEqual(ring.get_node("any_key"), "server1")

    def test_multiple_nodes(self):
        ring = ConsistentHashRing(["s1", "s2", "s3"])
        node = ring.get_node("test_key")
        self.assertIn(node, ["s1", "s2", "s3"])

    def test_add_remove_node(self):
        ring = ConsistentHashRing(["s1", "s2"])
        ring.add_node("s3")
        self.assertIn("s3", ring.nodes)

        ring.remove_node("s1")
        self.assertNotIn("s1", ring.nodes)
        # All keys should still map to existing nodes
        node = ring.get_node("test")
        self.assertIn(node, ["s2", "s3"])

    def test_deterministic_mapping(self):
        ring = ConsistentHashRing(["s1", "s2", "s3"])
        node1 = ring.get_node("key1")
        node2 = ring.get_node("key1")
        self.assertEqual(node1, node2)

    def test_distribution(self):
        ring = ConsistentHashRing(["s1", "s2", "s3"])
        keys = [f"key_{i}" for i in range(300)]
        dist = ring.get_distribution(keys)
        # Each server should get at least some keys
        for count in dist.values():
            self.assertGreater(count, 0)

    def test_minimal_redistribution_on_add(self):
        ring = ConsistentHashRing(["s1", "s2"])
        keys = [f"key_{i}" for i in range(100)]
        before = {k: ring.get_node(k) for k in keys}

        ring.add_node("s3")
        after = {k: ring.get_node(k) for k in keys}

        # Some keys should have moved, but not all
        changed = sum(1 for k in keys if before[k] != after[k])
        self.assertLess(changed, len(keys))


# ============================================================================
# LINKED LIST TESTS
# ============================================================================


class TestSinglyLinkedListEmpty(unittest.TestCase):
    """Test SinglyLinkedList edge cases."""

    def setUp(self):
        self.ll = SinglyLinkedList()

    def test_empty_size(self):
        self.assertEqual(len(self.ll), 0)

    def test_empty_delete_head(self):
        self.assertIsNone(self.ll.delete_at_head())

    def test_empty_delete_tail(self):
        self.assertIsNone(self.ll.delete_at_tail())

    def test_empty_search(self):
        self.assertIsNone(self.ll.search(42))

    def test_empty_get_middle(self):
        self.assertIsNone(self.ll.get_middle())

    def test_empty_detect_cycle(self):
        self.assertFalse(self.ll.detect_cycle())

    def test_empty_iterator(self):
        self.assertEqual(list(self.ll), [])


class TestSinglyLinkedListCRUD(unittest.TestCase):
    """Test SinglyLinkedList CRUD operations."""

    def test_insert_at_head(self):
        ll = SinglyLinkedList()
        ll.insert_at_head(3)
        ll.insert_at_head(2)
        ll.insert_at_head(1)
        self.assertEqual(list(ll), [1, 2, 3])
        self.assertEqual(len(ll), 3)

    def test_insert_at_tail(self):
        ll = SinglyLinkedList()
        ll.insert_at_tail(1)
        ll.insert_at_tail(2)
        ll.insert_at_tail(3)
        self.assertEqual(list(ll), [1, 2, 3])

    def test_insert_at_position(self):
        ll = SinglyLinkedList()
        ll.insert_at_tail(1)
        ll.insert_at_tail(3)
        ll.insert_at_position(2, 1)
        self.assertEqual(list(ll), [1, 2, 3])

    def test_insert_at_position_head(self):
        ll = SinglyLinkedList()
        ll.insert_at_tail(2)
        ll.insert_at_position(1, 0)
        self.assertEqual(list(ll), [1, 2])

    def test_insert_at_position_out_of_bounds(self):
        ll = SinglyLinkedList()
        with self.assertRaises(IndexError):
            ll.insert_at_position(1, 5)
        with self.assertRaises(IndexError):
            ll.insert_at_position(1, -1)

    def test_delete_at_head(self):
        ll = SinglyLinkedList()
        ll.insert_at_tail(1)
        ll.insert_at_tail(2)
        self.assertEqual(ll.delete_at_head(), 1)
        self.assertEqual(list(ll), [2])

    def test_delete_at_tail(self):
        ll = SinglyLinkedList()
        ll.insert_at_tail(1)
        ll.insert_at_tail(2)
        self.assertEqual(ll.delete_at_tail(), 2)
        self.assertEqual(list(ll), [1])

    def test_delete_single_element_tail(self):
        ll = SinglyLinkedList()
        ll.insert_at_head(1)
        self.assertEqual(ll.delete_at_tail(), 1)
        self.assertEqual(len(ll), 0)

    def test_delete_value(self):
        ll = SinglyLinkedList()
        for v in [1, 2, 3, 4]:
            ll.insert_at_tail(v)
        self.assertTrue(ll.delete_value(2))
        self.assertEqual(list(ll), [1, 3, 4])

    def test_delete_value_head(self):
        ll = SinglyLinkedList()
        for v in [1, 2, 3]:
            ll.insert_at_tail(v)
        self.assertTrue(ll.delete_value(1))
        self.assertEqual(list(ll), [2, 3])

    def test_delete_value_nonexistent(self):
        ll = SinglyLinkedList()
        ll.insert_at_tail(1)
        self.assertFalse(ll.delete_value(99))

    def test_search(self):
        ll = SinglyLinkedList()
        for v in [1, 2, 3]:
            ll.insert_at_tail(v)
        node = ll.search(2)
        self.assertIsNotNone(node)
        self.assertEqual(node.data, 2)

    def test_search_not_found(self):
        ll = SinglyLinkedList()
        ll.insert_at_tail(1)
        self.assertIsNone(ll.search(99))


class TestSinglyLinkedListAdvanced(unittest.TestCase):
    """Test advanced SinglyLinkedList operations."""

    def test_reverse(self):
        ll = SinglyLinkedList()
        for v in [1, 2, 3, 4, 5]:
            ll.insert_at_tail(v)
        ll.reverse()
        self.assertEqual(list(ll), [5, 4, 3, 2, 1])

    def test_reverse_single(self):
        ll = SinglyLinkedList()
        ll.insert_at_head(1)
        ll.reverse()
        self.assertEqual(list(ll), [1])

    def test_reverse_empty(self):
        ll = SinglyLinkedList()
        ll.reverse()
        self.assertEqual(list(ll), [])

    def test_get_middle_odd(self):
        ll = SinglyLinkedList()
        for v in [1, 2, 3, 4, 5]:
            ll.insert_at_tail(v)
        self.assertEqual(ll.get_middle(), 3)

    def test_get_middle_even(self):
        ll = SinglyLinkedList()
        for v in [1, 2, 3, 4]:
            ll.insert_at_tail(v)
        self.assertEqual(ll.get_middle(), 2)

    def test_get_middle_single(self):
        ll = SinglyLinkedList()
        ll.insert_at_head(42)
        self.assertEqual(ll.get_middle(), 42)

    def test_detect_cycle_no_cycle(self):
        ll = SinglyLinkedList()
        for v in [1, 2, 3]:
            ll.insert_at_tail(v)
        self.assertFalse(ll.detect_cycle())

    def test_detect_cycle_with_cycle(self):
        ll = SinglyLinkedList()
        for v in [1, 2, 3, 4]:
            ll.insert_at_tail(v)
        # Manually create a cycle: tail -> head
        current = ll.head
        while current.next:
            current = current.next
        current.next = ll.head
        self.assertTrue(ll.detect_cycle())

    def test_merge_sorted(self):
        ll1 = SinglyLinkedList()
        for v in [1, 3, 5]:
            ll1.insert_at_tail(v)

        ll2 = SinglyLinkedList()
        for v in [2, 4, 6]:
            ll2.insert_at_tail(v)

        merged = ll1.merge_sorted(ll2)
        self.assertEqual(list(merged), [1, 2, 3, 4, 5, 6])

    def test_merge_sorted_one_empty(self):
        ll1 = SinglyLinkedList()
        for v in [1, 2, 3]:
            ll1.insert_at_tail(v)

        ll2 = SinglyLinkedList()

        merged = ll1.merge_sorted(ll2)
        self.assertEqual(list(merged), [1, 2, 3])

    def test_merge_sorted_both_empty(self):
        ll1 = SinglyLinkedList()
        ll2 = SinglyLinkedList()
        merged = ll1.merge_sorted(ll2)
        self.assertEqual(list(merged), [])

    def test_str(self):
        ll = SinglyLinkedList()
        for v in [1, 2, 3]:
            ll.insert_at_tail(v)
        s = str(ll)
        self.assertIn("1", s)
        self.assertIn("->", s)


class TestDoublyLinkedListEmpty(unittest.TestCase):
    """Test DoublyLinkedList edge cases."""

    def setUp(self):
        self.dll = DoublyLinkedList()

    def test_empty_size(self):
        self.assertEqual(len(self.dll), 0)

    def test_empty_delete_head(self):
        self.assertIsNone(self.dll.delete_at_head())

    def test_empty_delete_tail(self):
        self.assertIsNone(self.dll.delete_at_tail())

    def test_empty_iterator(self):
        self.assertEqual(list(self.dll), [])

    def test_empty_reverse_iter(self):
        self.assertEqual(list(self.dll.reverse_iter()), [])


class TestDoublyLinkedListCRUD(unittest.TestCase):
    """Test DoublyLinkedList CRUD operations."""

    def test_insert_at_head(self):
        dll = DoublyLinkedList()
        dll.insert_at_head(3)
        dll.insert_at_head(2)
        dll.insert_at_head(1)
        self.assertEqual(list(dll), [1, 2, 3])

    def test_insert_at_tail(self):
        dll = DoublyLinkedList()
        dll.insert_at_tail(1)
        dll.insert_at_tail(2)
        dll.insert_at_tail(3)
        self.assertEqual(list(dll), [1, 2, 3])

    def test_delete_at_head(self):
        dll = DoublyLinkedList()
        dll.insert_at_tail(1)
        dll.insert_at_tail(2)
        dll.insert_at_tail(3)
        self.assertEqual(dll.delete_at_head(), 1)
        self.assertEqual(list(dll), [2, 3])

    def test_delete_at_tail(self):
        dll = DoublyLinkedList()
        dll.insert_at_tail(1)
        dll.insert_at_tail(2)
        dll.insert_at_tail(3)
        self.assertEqual(dll.delete_at_tail(), 3)
        self.assertEqual(list(dll), [1, 2])

    def test_delete_single_element(self):
        dll = DoublyLinkedList()
        dll.insert_at_head(1)
        self.assertEqual(dll.delete_at_head(), 1)
        self.assertEqual(len(dll), 0)
        self.assertIsNone(dll.head)
        self.assertIsNone(dll.tail)

    def test_delete_node(self):
        dll = DoublyLinkedList()
        dll.insert_at_tail(1)
        dll.insert_at_tail(2)
        dll.insert_at_tail(3)
        # Delete middle node
        middle = dll.head.next
        dll.delete_node(middle)
        self.assertEqual(list(dll), [1, 3])

    def test_delete_node_head(self):
        dll = DoublyLinkedList()
        dll.insert_at_tail(1)
        dll.insert_at_tail(2)
        dll.delete_node(dll.head)
        self.assertEqual(list(dll), [2])

    def test_delete_node_tail(self):
        dll = DoublyLinkedList()
        dll.insert_at_tail(1)
        dll.insert_at_tail(2)
        dll.delete_node(dll.tail)
        self.assertEqual(list(dll), [1])


class TestDoublyLinkedListAdvanced(unittest.TestCase):
    """Test DoublyLinkedList advanced operations."""

    def test_reverse(self):
        dll = DoublyLinkedList()
        for v in [1, 2, 3, 4, 5]:
            dll.insert_at_tail(v)
        dll.reverse()
        self.assertEqual(list(dll), [5, 4, 3, 2, 1])

    def test_reverse_iter(self):
        dll = DoublyLinkedList()
        for v in [1, 2, 3]:
            dll.insert_at_tail(v)
        self.assertEqual(list(dll.reverse_iter()), [3, 2, 1])

    def test_bidirectional_consistency(self):
        dll = DoublyLinkedList()
        for v in [1, 2, 3, 4, 5]:
            dll.insert_at_tail(v)
        forward = list(dll)
        backward = list(dll.reverse_iter())
        self.assertEqual(forward, backward[::-1])

    def test_head_tail_pointers(self):
        dll = DoublyLinkedList()
        dll.insert_at_tail(1)
        dll.insert_at_tail(2)
        dll.insert_at_tail(3)
        self.assertEqual(dll.head.data, 1)
        self.assertEqual(dll.tail.data, 3)
        self.assertIsNone(dll.head.prev)
        self.assertIsNone(dll.tail.next)


class TestCircularLinkedListEmpty(unittest.TestCase):
    """Test CircularLinkedList edge cases."""

    def setUp(self):
        self.cll = CircularLinkedList()

    def test_empty_size(self):
        self.assertEqual(len(self.cll), 0)

    def test_empty_delete_head(self):
        self.assertIsNone(self.cll.delete_at_head())

    def test_empty_iterator(self):
        self.assertEqual(list(self.cll), [])

    def test_empty_str(self):
        self.assertEqual(str(self.cll), "Empty")


class TestCircularLinkedListCRUD(unittest.TestCase):
    """Test CircularLinkedList CRUD operations."""

    def test_insert_at_head(self):
        cll = CircularLinkedList()
        cll.insert_at_head(3)
        cll.insert_at_head(2)
        cll.insert_at_head(1)
        self.assertEqual(list(cll), [1, 2, 3])

    def test_insert_at_tail(self):
        cll = CircularLinkedList()
        cll.insert_at_tail(1)
        cll.insert_at_tail(2)
        cll.insert_at_tail(3)
        self.assertEqual(list(cll), [1, 2, 3])

    def test_single_element_is_circular(self):
        cll = CircularLinkedList()
        cll.insert_at_head(1)
        self.assertEqual(cll.head.next, cll.head)

    def test_circularity(self):
        cll = CircularLinkedList()
        for v in [1, 2, 3]:
            cll.insert_at_tail(v)
        # Last node should point back to head
        current = cll.head
        while current.next != cll.head:
            current = current.next
        self.assertEqual(current.next, cll.head)

    def test_delete_at_head(self):
        cll = CircularLinkedList()
        for v in [1, 2, 3]:
            cll.insert_at_tail(v)
        self.assertEqual(cll.delete_at_head(), 1)
        self.assertEqual(list(cll), [2, 3])

    def test_delete_single_element(self):
        cll = CircularLinkedList()
        cll.insert_at_head(1)
        self.assertEqual(cll.delete_at_head(), 1)
        self.assertEqual(len(cll), 0)
        self.assertIsNone(cll.head)

    def test_traverse(self):
        cll = CircularLinkedList()
        for v in [1, 2, 3]:
            cll.insert_at_tail(v)
        result = []
        cll.traverse(lambda x: result.append(x))
        self.assertEqual(result, [1, 2, 3])


class TestSkipListEmpty(unittest.TestCase):
    """Test SkipList edge cases."""

    def setUp(self):
        self.sl = SkipList()

    def test_empty_size(self):
        self.assertEqual(len(self.sl), 0)

    def test_empty_search(self):
        self.assertFalse(self.sl.search(42))

    def test_empty_delete(self):
        self.assertFalse(self.sl.delete(42))

    def test_empty_iterator(self):
        self.assertEqual(list(self.sl), [])


class TestSkipListCRUD(unittest.TestCase):
    """Test SkipList CRUD operations."""

    def test_insert_and_search(self):
        sl = SkipList()
        random.seed(42)
        for v in [3, 7, 1, 9, 5]:
            sl.insert(v)
        self.assertEqual(len(sl), 5)
        for v in [3, 7, 1, 9, 5]:
            self.assertTrue(sl.search(v))
        self.assertFalse(sl.search(99))

    def test_sorted_order(self):
        sl = SkipList()
        random.seed(42)
        values = [5, 3, 8, 1, 9, 2, 7, 4, 6]
        for v in values:
            sl.insert(v)
        self.assertEqual(list(sl), sorted(values))

    def test_delete(self):
        sl = SkipList()
        random.seed(42)
        for v in [1, 2, 3, 4, 5]:
            sl.insert(v)
        self.assertTrue(sl.delete(3))
        self.assertFalse(sl.search(3))
        self.assertEqual(len(sl), 4)
        self.assertEqual(list(sl), [1, 2, 4, 5])

    def test_delete_nonexistent(self):
        sl = SkipList()
        random.seed(42)
        sl.insert(1)
        self.assertFalse(sl.delete(99))

    def test_many_elements(self):
        sl = SkipList()
        random.seed(42)
        values = random.sample(range(1000), 200)
        for v in values:
            sl.insert(v)
        self.assertEqual(len(sl), 200)
        self.assertEqual(list(sl), sorted(values))

    def test_sorted_invariant_after_deletions(self):
        sl = SkipList()
        random.seed(42)
        values = random.sample(range(500), 100)
        for v in values:
            sl.insert(v)

        to_delete = random.sample(values, 30)
        for v in to_delete:
            sl.delete(v)

        result = list(sl)
        self.assertEqual(result, sorted(result))


# ============================================================================
# TRIE TESTS
# ============================================================================


class TestTrieEmpty(unittest.TestCase):
    """Test Trie edge cases."""

    def setUp(self):
        self.trie = Trie()

    def test_empty_word_count(self):
        self.assertEqual(self.trie.word_count, 0)

    def test_search_empty(self):
        self.assertFalse(self.trie.search("anything"))

    def test_starts_with_empty(self):
        self.assertFalse(self.trie.starts_with("a"))

    def test_autocomplete_empty(self):
        self.assertEqual(self.trie.autocomplete("a"), [])

    def test_get_all_words_empty(self):
        self.assertEqual(self.trie.get_all_words(), [])

    def test_longest_common_prefix_empty(self):
        self.assertEqual(self.trie.longest_common_prefix(), "")


class TestTrieCRUD(unittest.TestCase):
    """Test Trie CRUD operations."""

    def setUp(self):
        self.trie = Trie()
        self.words = ["the", "there", "their", "answer", "any", "bye"]
        for w in self.words:
            self.trie.insert(w)

    def test_insert_and_count(self):
        self.assertEqual(self.trie.word_count, len(self.words))

    def test_search_existing(self):
        for w in self.words:
            self.assertTrue(self.trie.search(w), f"Failed to find '{w}'")

    def test_search_nonexistent(self):
        self.assertFalse(self.trie.search("the_"))
        self.assertFalse(self.trie.search("an"))
        self.assertFalse(self.trie.search("by"))

    def test_search_prefix_is_not_word(self):
        self.assertFalse(self.trie.search("th"))

    def test_starts_with(self):
        self.assertTrue(self.trie.starts_with("th"))
        self.assertTrue(self.trie.starts_with("the"))
        self.assertTrue(self.trie.starts_with("an"))
        self.assertFalse(self.trie.starts_with("xyz"))

    def test_delete_existing(self):
        self.trie.delete("the")
        self.assertFalse(self.trie.search("the"))
        self.assertEqual(self.trie.word_count, len(self.words) - 1)
        # "there" and "their" should still work
        self.assertTrue(self.trie.search("there"))
        self.assertTrue(self.trie.search("their"))

    def test_delete_nonexistent(self):
        result = self.trie.delete("xyz")
        self.assertFalse(result)
        self.assertEqual(self.trie.word_count, len(self.words))

    def test_delete_prefix_not_word(self):
        result = self.trie.delete("th")
        self.assertFalse(result)

    def test_insert_duplicate(self):
        self.trie.insert("the")
        # word_count should not increase for duplicates
        self.assertEqual(self.trie.word_count, len(self.words))

    def test_insert_with_frequency(self):
        self.trie.insert("popular", 100)
        self.assertTrue(self.trie.search("popular"))

    def test_get_all_words(self):
        all_words = self.trie.get_all_words()
        self.assertEqual(sorted(all_words), sorted(self.words))


class TestTrieAdvanced(unittest.TestCase):
    """Test Trie advanced features."""

    def test_autocomplete(self):
        trie = Trie()
        trie.insert("apple", 10)
        trie.insert("application", 5)
        trie.insert("apply", 8)
        trie.insert("banana", 3)

        results = trie.autocomplete("app")
        words = [w for w, f in results]
        self.assertIn("apple", words)
        self.assertIn("application", words)
        self.assertIn("apply", words)
        self.assertNotIn("banana", words)

    def test_autocomplete_with_limit(self):
        trie = Trie()
        for i in range(20):
            trie.insert(f"word{i:02d}")

        results = trie.autocomplete("word", limit=5)
        self.assertEqual(len(results), 5)

    def test_longest_common_prefix(self):
        trie = Trie()
        trie.insert("flower")
        trie.insert("flow")
        trie.insert("flight")
        self.assertEqual(trie.longest_common_prefix(), "fl")

    def test_longest_common_prefix_all_same(self):
        trie = Trie()
        trie.insert("aaa")
        trie.insert("aaab")
        trie.insert("aaac")
        self.assertEqual(trie.longest_common_prefix(), "aaa")

    def test_count_words_with_prefix(self):
        trie = Trie()
        trie.insert("the")
        trie.insert("there")
        trie.insert("their")
        trie.insert("answer")
        self.assertEqual(trie.count_words_with_prefix("the"), 3)
        self.assertEqual(trie.count_words_with_prefix("ans"), 1)
        self.assertEqual(trie.count_words_with_prefix("xyz"), 0)

    def test_serialize_deserialize(self):
        trie = Trie()
        words = ["apple", "banana", "cherry"]
        for w in words:
            trie.insert(w)

        serialized = trie.serialize()
        restored = Trie.deserialize(serialized)

        for w in words:
            self.assertTrue(restored.search(w))
        self.assertEqual(restored.word_count, len(words))

    def test_empty_string(self):
        trie = Trie()
        trie.insert("")
        self.assertTrue(trie.search(""))
        self.assertEqual(trie.word_count, 1)

    def test_single_character_words(self):
        trie = Trie()
        for c in "abcdef":
            trie.insert(c)
        self.assertEqual(trie.word_count, 6)
        for c in "abcdef":
            self.assertTrue(trie.search(c))


class TestPatriciaTrie(unittest.TestCase):
    """Test Patricia (compressed) trie."""

    def test_insert_and_search(self):
        pt = PatriciaTrie()
        pt.insert("test")
        pt.insert("testing")
        pt.insert("team")
        self.assertTrue(pt.search("test"))
        self.assertTrue(pt.search("testing"))
        self.assertTrue(pt.search("team"))

    def test_search_nonexistent(self):
        pt = PatriciaTrie()
        pt.insert("test")
        self.assertFalse(pt.search("tes"))
        self.assertFalse(pt.search("tester"))
        self.assertFalse(pt.search("xyz"))

    def test_shared_prefix(self):
        pt = PatriciaTrie()
        pt.insert("romane")
        pt.insert("romanus")
        pt.insert("romulus")
        self.assertTrue(pt.search("romane"))
        self.assertTrue(pt.search("romanus"))
        self.assertTrue(pt.search("romulus"))
        self.assertFalse(pt.search("rom"))

    def test_insert_empty_string(self):
        pt = PatriciaTrie()
        pt.insert("")
        # Empty string insert returns early, so search should be False
        self.assertFalse(pt.search(""))

    def test_single_word(self):
        pt = PatriciaTrie()
        pt.insert("hello")
        self.assertTrue(pt.search("hello"))
        self.assertFalse(pt.search("hell"))


class TestSuffixTrie(unittest.TestCase):
    """Test SuffixTrie for pattern matching."""

    def setUp(self):
        self.st = SuffixTrie("banana")

    def test_contains_substring(self):
        self.assertTrue(self.st.contains_substring("ana"))
        self.assertTrue(self.st.contains_substring("ban"))
        self.assertTrue(self.st.contains_substring("banana"))
        self.assertTrue(self.st.contains_substring("a"))
        self.assertFalse(self.st.contains_substring("xyz"))
        self.assertFalse(self.st.contains_substring("banan_"))

    def test_find_all_occurrences(self):
        positions = self.st.find_all_occurrences("ana")
        self.assertEqual(sorted(positions), [1, 3])

    def test_find_occurrences_not_found(self):
        positions = self.st.find_all_occurrences("xyz")
        self.assertEqual(positions, [])

    def test_find_single_char(self):
        positions = self.st.find_all_occurrences("a")
        self.assertEqual(sorted(positions), [1, 3, 5])


class TestSpellChecker(unittest.TestCase):
    """Test SpellChecker application."""

    def setUp(self):
        self.checker = SpellChecker(
            ["hello", "world", "python", "programming", "algorithm"]
        )

    def test_correct_words(self):
        self.assertTrue(self.checker.is_correct("hello"))
        self.assertTrue(self.checker.is_correct("python"))
        self.assertTrue(self.checker.is_correct("HELLO"))  # case insensitive

    def test_incorrect_words(self):
        self.assertFalse(self.checker.is_correct("helo"))
        self.assertFalse(self.checker.is_correct("xyz"))

    def test_suggest_correct_word(self):
        suggestions = self.checker.suggest("hello")
        self.assertEqual(suggestions, ["hello"])

    def test_suggest_misspelled(self):
        suggestions = self.checker.suggest("helo")
        self.assertIn("hello", suggestions)

    def test_suggest_returns_list(self):
        suggestions = self.checker.suggest("pythn")
        self.assertIsInstance(suggestions, list)


class TestAutoComplete(unittest.TestCase):
    """Test AutoComplete application."""

    def setUp(self):
        self.ac = AutoComplete()
        self.ac.add_word("python", 100)
        self.ac.add_word("programming", 80)
        self.ac.add_word("program", 60)
        self.ac.add_word("java", 90)
        self.ac.add_word("javascript", 85)

    def test_search_prefix(self):
        results = self.ac.search("pro")
        self.assertIn("programming", results)
        self.assertIn("program", results)
        self.assertNotIn("python", results)

    def test_search_no_match(self):
        results = self.ac.search("xyz")
        self.assertEqual(results, [])

    def test_record_search_boost(self):
        self.ac.record_search("program")
        results = self.ac.search("pro")
        # "program" should be boosted to top
        self.assertEqual(results[0], "program")

    def test_case_insensitive(self):
        results = self.ac.search("PRO")
        self.assertGreater(len(results), 0)


class TestDictionary(unittest.TestCase):
    """Test Dictionary application."""

    def setUp(self):
        self.dictionary = Dictionary()
        self.dictionary.add("algorithm", "A step-by-step procedure")
        self.dictionary.add("trie", "A tree data structure for strings")

    def test_lookup_existing(self):
        result = self.dictionary.lookup("algorithm")
        self.assertEqual(result, "A step-by-step procedure")

    def test_lookup_nonexistent(self):
        self.assertIsNone(self.dictionary.lookup("missing"))

    def test_case_insensitive_lookup(self):
        result = self.dictionary.lookup("Algorithm")
        self.assertEqual(result, "A step-by-step procedure")

    def test_words_starting_with(self):
        self.dictionary.add("also", "In addition")
        self.dictionary.add("banana", "A fruit")
        words = self.dictionary.words_starting_with("al")
        self.assertIn("algorithm", words)
        self.assertIn("also", words)
        self.assertNotIn("banana", words)


# ============================================================================
# RUN TESTS
# ============================================================================


if __name__ == "__main__":
    unittest.main(verbosity=2)
