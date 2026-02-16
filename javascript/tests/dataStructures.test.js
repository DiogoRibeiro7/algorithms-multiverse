/**
 * Test suite for data structures
 */

import * as ds from '../src/dataStructures.js';

console.log('=== DATA STRUCTURES TESTS ===\n');

// Test Stack
console.log('Testing Stack...');
const stack = new ds.Stack();
console.assert(stack.isEmpty(), 'Stack should be empty initially');
stack.push(1);
stack.push(2);
stack.push(3);
console.assert(stack.peek() === 3, 'Stack peek failed');
console.assert(stack.pop() === 3, 'Stack pop failed');
console.assert(stack.size() === 2, 'Stack size failed');
console.log('✓ Stack passed all tests');

// Test Queue
console.log('Testing Queue...');
const queue = new ds.Queue();
console.assert(queue.isEmpty(), 'Queue should be empty initially');
queue.enqueue(1);
queue.enqueue(2);
queue.enqueue(3);
console.assert(queue.peek() === 1, 'Queue peek failed');
console.assert(queue.dequeue() === 1, 'Queue dequeue failed');
console.assert(queue.size() === 2, 'Queue size failed');
console.log('✓ Queue passed all tests');

// Test LinkedList
console.log('Testing LinkedList...');
const linkedList = new ds.LinkedList();
linkedList.append(1);
linkedList.append(2);
linkedList.prepend(0);
console.assert(linkedList.size() === 3, 'LinkedList size failed');
console.assert(linkedList.get(0) === 0, 'LinkedList get failed');
console.assert(linkedList.get(1) === 1, 'LinkedList get failed');
linkedList.removeAt(1);
console.assert(linkedList.size() === 2, 'LinkedList removeAt failed');
console.log('✓ LinkedList passed all tests');

// Test DoublyLinkedList
console.log('Testing DoublyLinkedList...');
const dll = new ds.DoublyLinkedList();
dll.append(1);
dll.append(2);
dll.prepend(0);
console.assert(dll.size() === 3, 'DoublyLinkedList size failed');
console.assert(dll.get(0) === 0, 'DoublyLinkedList get failed');
dll.reverse();
console.assert(dll.get(0) === 2, 'DoublyLinkedList reverse failed');
console.log('✓ DoublyLinkedList passed all tests');

// Test BinarySearchTree
console.log('Testing BinarySearchTree...');
const bst = new ds.BinarySearchTree();
bst.insert(5);
bst.insert(3);
bst.insert(7);
bst.insert(1);
bst.insert(9);
console.assert(bst.search(7) === true, 'BST search failed');
console.assert(bst.search(10) === false, 'BST search failed for non-existent');
console.assert(bst.findMin() === 1, 'BST findMin failed');
console.assert(bst.findMax() === 9, 'BST findMax failed');
const inorder = bst.inorderTraversal();
console.assert(JSON.stringify(inorder) === '[1,3,5,7,9]', 'BST inorder traversal failed');
console.log('✓ BinarySearchTree passed all tests');

// Test AVLTree
console.log('Testing AVLTree...');
const avl = new ds.AVLTree();
avl.insert(10);
avl.insert(20);
avl.insert(30);
avl.insert(40);
avl.insert(50);
avl.insert(25);
console.assert(avl.isBalanced(), 'AVL tree should be balanced');
console.assert(avl.search(25) === true, 'AVL search failed');
console.log('✓ AVLTree passed all tests');

// Test RedBlackTree
console.log('Testing RedBlackTree...');
const rbt = new ds.RedBlackTree();
rbt.insert(7);
rbt.insert(3);
rbt.insert(18);
rbt.insert(10);
rbt.insert(22);
rbt.insert(8);
console.assert(rbt.search(10) === true, 'RedBlackTree search failed');
console.assert(rbt.search(15) === false, 'RedBlackTree search failed for non-existent');
console.log('✓ RedBlackTree passed all tests');

// Test MinHeap
console.log('Testing MinHeap...');
const minHeap = new ds.MinHeap();
minHeap.insert(5);
minHeap.insert(3);
minHeap.insert(7);
minHeap.insert(1);
console.assert(minHeap.extractMin() === 1, 'MinHeap extractMin failed');
console.assert(minHeap.peek() === 3, 'MinHeap peek failed');
console.log('✓ MinHeap passed all tests');

// Test MaxHeap
console.log('Testing MaxHeap...');
const maxHeap = new ds.MaxHeap();
maxHeap.insert(5);
maxHeap.insert(3);
maxHeap.insert(7);
maxHeap.insert(1);
console.assert(maxHeap.extractMax() === 7, 'MaxHeap extractMax failed');
console.assert(maxHeap.peek() === 5, 'MaxHeap peek failed');
console.log('✓ MaxHeap passed all tests');

// Test Trie
console.log('Testing Trie...');
const trie = new ds.Trie();
trie.insert('apple');
trie.insert('app');
trie.insert('apricot');
console.assert(trie.search('app') === true, 'Trie search failed');
console.assert(trie.search('application') === false, 'Trie search failed for non-existent');
console.assert(trie.startsWith('app') === true, 'Trie startsWith failed');
const words = trie.getAllWords();
console.assert(words.length === 3, 'Trie getAllWords failed');
console.log('✓ Trie passed all tests');

// Test DisjointSet
console.log('Testing DisjointSet...');
const dsu = new ds.DisjointSet(5);
dsu.union(0, 1);
dsu.union(2, 3);
dsu.union(1, 2);
console.assert(dsu.find(0) === dsu.find(3), 'DisjointSet union-find failed');
console.assert(dsu.find(0) !== dsu.find(4), 'DisjointSet should keep separate components');
console.log('✓ DisjointSet passed all tests');

// Test SegmentTree
console.log('Testing SegmentTree...');
const arr = [1, 3, 5, 7, 9, 11];
const segTree = new ds.SegmentTree(arr);
console.assert(segTree.query(1, 3) === 15, 'SegmentTree query failed'); // 3 + 5 + 7
segTree.update(2, 10);
console.assert(segTree.query(1, 3) === 20, 'SegmentTree update failed'); // 3 + 10 + 7
console.log('✓ SegmentTree passed all tests');

// Test FenwickTree
console.log('Testing FenwickTree...');
const fenwick = new ds.FenwickTree(6);
fenwick.update(0, 1);
fenwick.update(1, 3);
fenwick.update(2, 5);
fenwick.update(3, 7);
fenwick.update(4, 9);
fenwick.update(5, 11);
console.assert(fenwick.query(3) === 16, 'FenwickTree prefix sum failed'); // 1 + 3 + 5 + 7
console.assert(fenwick.rangeQuery(1, 3) === 15, 'FenwickTree range query failed'); // 3 + 5 + 7
console.log('✓ FenwickTree passed all tests');

console.log('\n=== All data structures tests completed ===');