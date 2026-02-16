/**
 * @module dataStructures
 * @description Data structures implementation
 */

/**
 * Stack - LIFO data structure
 */
export class Stack {
    constructor() {
        this.items = [];
    }

    push(element) {
        this.items.push(element);
    }

    pop() {
        if (this.isEmpty()) return undefined;
        return this.items.pop();
    }

    peek() {
        if (this.isEmpty()) return undefined;
        return this.items[this.items.length - 1];
    }

    isEmpty() {
        return this.items.length === 0;
    }

    size() {
        return this.items.length;
    }

    clear() {
        this.items = [];
    }

    toArray() {
        return [...this.items];
    }
}

/**
 * Queue - FIFO data structure
 */
export class Queue {
    constructor() {
        this.items = [];
    }

    enqueue(element) {
        this.items.push(element);
    }

    dequeue() {
        if (this.isEmpty()) return undefined;
        return this.items.shift();
    }

    front() {
        if (this.isEmpty()) return undefined;
        return this.items[0];
    }

    isEmpty() {
        return this.items.length === 0;
    }

    size() {
        return this.items.length;
    }

    clear() {
        this.items = [];
    }

    toArray() {
        return [...this.items];
    }
}

/**
 * Deque - Double-ended queue
 */
export class Deque {
    constructor() {
        this.items = [];
    }

    addFront(element) {
        this.items.unshift(element);
    }

    addRear(element) {
        this.items.push(element);
    }

    removeFront() {
        if (this.isEmpty()) return undefined;
        return this.items.shift();
    }

    removeRear() {
        if (this.isEmpty()) return undefined;
        return this.items.pop();
    }

    peekFront() {
        if (this.isEmpty()) return undefined;
        return this.items[0];
    }

    peekRear() {
        if (this.isEmpty()) return undefined;
        return this.items[this.items.length - 1];
    }

    isEmpty() {
        return this.items.length === 0;
    }

    size() {
        return this.items.length;
    }

    clear() {
        this.items = [];
    }
}

/**
 * Priority Queue - Elements with priorities
 */
export class PriorityQueue {
    constructor(compareFunc = (a, b) => a.priority - b.priority) {
        this.items = [];
        this.compare = compareFunc;
    }

    enqueue(element, priority) {
        const queueElement = { element, priority };
        let added = false;

        for (let i = 0; i < this.items.length; i++) {
            if (this.compare(queueElement, this.items[i]) < 0) {
                this.items.splice(i, 0, queueElement);
                added = true;
                break;
            }
        }

        if (!added) {
            this.items.push(queueElement);
        }
    }

    dequeue() {
        if (this.isEmpty()) return undefined;
        return this.items.shift().element;
    }

    front() {
        if (this.isEmpty()) return undefined;
        return this.items[0].element;
    }

    isEmpty() {
        return this.items.length === 0;
    }

    size() {
        return this.items.length;
    }

    clear() {
        this.items = [];
    }
}

/**
 * Node for linked structures
 */
class Node {
    constructor(data) {
        this.data = data;
        this.next = null;
    }
}

/**
 * Singly Linked List
 */
export class LinkedList {
    constructor() {
        this.head = null;
        this.length = 0;
    }

    append(data) {
        const node = new Node(data);

        if (!this.head) {
            this.head = node;
        } else {
            let current = this.head;
            while (current.next) {
                current = current.next;
            }
            current.next = node;
        }

        this.length++;
    }

    prepend(data) {
        const node = new Node(data);
        node.next = this.head;
        this.head = node;
        this.length++;
    }

    insert(index, data) {
        if (index < 0 || index > this.length) return false;

        if (index === 0) {
            this.prepend(data);
            return true;
        }

        const node = new Node(data);
        let current = this.head;
        let previous;
        let i = 0;

        while (i < index) {
            previous = current;
            current = current.next;
            i++;
        }

        node.next = current;
        previous.next = node;
        this.length++;

        return true;
    }

    remove(index) {
        if (index < 0 || index >= this.length) return undefined;

        let current = this.head;

        if (index === 0) {
            this.head = current.next;
            this.length--;
            return current.data;
        }

        let previous;
        let i = 0;

        while (i < index) {
            previous = current;
            current = current.next;
            i++;
        }

        previous.next = current.next;
        this.length--;

        return current.data;
    }

    get(index) {
        if (index < 0 || index >= this.length) return undefined;

        let current = this.head;
        let i = 0;

        while (i < index) {
            current = current.next;
            i++;
        }

        return current.data;
    }

    indexOf(data) {
        let current = this.head;
        let index = 0;

        while (current) {
            if (current.data === data) {
                return index;
            }
            current = current.next;
            index++;
        }

        return -1;
    }

    isEmpty() {
        return this.length === 0;
    }

    size() {
        return this.length;
    }

    clear() {
        this.head = null;
        this.length = 0;
    }

    toArray() {
        const result = [];
        let current = this.head;

        while (current) {
            result.push(current.data);
            current = current.next;
        }

        return result;
    }

    reverse() {
        let prev = null;
        let current = this.head;
        let next = null;

        while (current) {
            next = current.next;
            current.next = prev;
            prev = current;
            current = next;
        }

        this.head = prev;
    }
}

/**
 * Doubly Linked List Node
 */
class DoublyNode {
    constructor(data) {
        this.data = data;
        this.next = null;
        this.prev = null;
    }
}

/**
 * Doubly Linked List
 */
export class DoublyLinkedList {
    constructor() {
        this.head = null;
        this.tail = null;
        this.length = 0;
    }

    append(data) {
        const node = new DoublyNode(data);

        if (!this.head) {
            this.head = node;
            this.tail = node;
        } else {
            node.prev = this.tail;
            this.tail.next = node;
            this.tail = node;
        }

        this.length++;
    }

    prepend(data) {
        const node = new DoublyNode(data);

        if (!this.head) {
            this.head = node;
            this.tail = node;
        } else {
            node.next = this.head;
            this.head.prev = node;
            this.head = node;
        }

        this.length++;
    }

    removeFirst() {
        if (!this.head) return undefined;

        const data = this.head.data;

        if (this.length === 1) {
            this.head = null;
            this.tail = null;
        } else {
            this.head = this.head.next;
            this.head.prev = null;
        }

        this.length--;
        return data;
    }

    removeLast() {
        if (!this.tail) return undefined;

        const data = this.tail.data;

        if (this.length === 1) {
            this.head = null;
            this.tail = null;
        } else {
            this.tail = this.tail.prev;
            this.tail.next = null;
        }

        this.length--;
        return data;
    }

    get(index) {
        if (index < 0 || index >= this.length) return undefined;

        let current;

        // Optimize by starting from head or tail
        if (index < this.length / 2) {
            current = this.head;
            for (let i = 0; i < index; i++) {
                current = current.next;
            }
        } else {
            current = this.tail;
            for (let i = this.length - 1; i > index; i--) {
                current = current.prev;
            }
        }

        return current.data;
    }

    isEmpty() {
        return this.length === 0;
    }

    size() {
        return this.length;
    }

    clear() {
        this.head = null;
        this.tail = null;
        this.length = 0;
    }

    toArray() {
        const result = [];
        let current = this.head;

        while (current) {
            result.push(current.data);
            current = current.next;
        }

        return result;
    }
}

/**
 * Binary Tree Node
 */
class TreeNode {
    constructor(data) {
        this.data = data;
        this.left = null;
        this.right = null;
    }
}

/**
 * Binary Search Tree
 */
export class BinarySearchTree {
    constructor() {
        this.root = null;
    }

    insert(data) {
        const node = new TreeNode(data);

        if (!this.root) {
            this.root = node;
        } else {
            this._insertNode(this.root, node);
        }
    }

    _insertNode(node, newNode) {
        if (newNode.data < node.data) {
            if (!node.left) {
                node.left = newNode;
            } else {
                this._insertNode(node.left, newNode);
            }
        } else {
            if (!node.right) {
                node.right = newNode;
            } else {
                this._insertNode(node.right, newNode);
            }
        }
    }

    search(data) {
        return this._searchNode(this.root, data);
    }

    _searchNode(node, data) {
        if (!node) return false;

        if (data < node.data) {
            return this._searchNode(node.left, data);
        } else if (data > node.data) {
            return this._searchNode(node.right, data);
        } else {
            return true;
        }
    }

    remove(data) {
        this.root = this._removeNode(this.root, data);
    }

    _removeNode(node, data) {
        if (!node) return null;

        if (data < node.data) {
            node.left = this._removeNode(node.left, data);
            return node;
        } else if (data > node.data) {
            node.right = this._removeNode(node.right, data);
            return node;
        } else {
            // Node to delete found

            // Case 1: Leaf node
            if (!node.left && !node.right) {
                return null;
            }

            // Case 2: Node with one child
            if (!node.left) {
                return node.right;
            }
            if (!node.right) {
                return node.left;
            }

            // Case 3: Node with two children
            const minRight = this._findMin(node.right);
            node.data = minRight.data;
            node.right = this._removeNode(node.right, minRight.data);
            return node;
        }
    }

    _findMin(node) {
        while (node.left) {
            node = node.left;
        }
        return node;
    }

    findMin() {
        if (!this.root) return null;
        return this._findMin(this.root).data;
    }

    findMax() {
        if (!this.root) return null;
        let node = this.root;
        while (node.right) {
            node = node.right;
        }
        return node.data;
    }

    inOrder(callback) {
        this._inOrderNode(this.root, callback);
    }

    _inOrderNode(node, callback) {
        if (node) {
            this._inOrderNode(node.left, callback);
            callback(node.data);
            this._inOrderNode(node.right, callback);
        }
    }

    preOrder(callback) {
        this._preOrderNode(this.root, callback);
    }

    _preOrderNode(node, callback) {
        if (node) {
            callback(node.data);
            this._preOrderNode(node.left, callback);
            this._preOrderNode(node.right, callback);
        }
    }

    postOrder(callback) {
        this._postOrderNode(this.root, callback);
    }

    _postOrderNode(node, callback) {
        if (node) {
            this._postOrderNode(node.left, callback);
            this._postOrderNode(node.right, callback);
            callback(node.data);
        }
    }

    levelOrder(callback) {
        if (!this.root) return;

        const queue = [this.root];

        while (queue.length > 0) {
            const node = queue.shift();
            callback(node.data);

            if (node.left) queue.push(node.left);
            if (node.right) queue.push(node.right);
        }
    }

    height(node = this.root) {
        if (!node) return -1;
        return 1 + Math.max(this.height(node.left), this.height(node.right));
    }

    isBalanced(node = this.root) {
        if (!node) return true;

        const leftHeight = this.height(node.left);
        const rightHeight = this.height(node.right);

        if (Math.abs(leftHeight - rightHeight) > 1) {
            return false;
        }

        return this.isBalanced(node.left) && this.isBalanced(node.right);
    }
}

/**
 * AVL Tree Node
 */
class AVLNode {
    constructor(data) {
        this.data = data;
        this.left = null;
        this.right = null;
        this.height = 1;
    }
}

/**
 * AVL Tree - Self-balancing BST
 */
export class AVLTree {
    constructor() {
        this.root = null;
    }

    getHeight(node) {
        return node ? node.height : 0;
    }

    getBalance(node) {
        return node ? this.getHeight(node.left) - this.getHeight(node.right) : 0;
    }

    updateHeight(node) {
        if (node) {
            node.height = 1 + Math.max(this.getHeight(node.left), this.getHeight(node.right));
        }
    }

    rotateRight(y) {
        const x = y.left;
        const T2 = x.right;

        x.right = y;
        y.left = T2;

        this.updateHeight(y);
        this.updateHeight(x);

        return x;
    }

    rotateLeft(x) {
        const y = x.right;
        const T2 = y.left;

        y.left = x;
        x.right = T2;

        this.updateHeight(x);
        this.updateHeight(y);

        return y;
    }

    insert(data) {
        this.root = this._insertNode(this.root, data);
    }

    _insertNode(node, data) {
        // Standard BST insertion
        if (!node) {
            return new AVLNode(data);
        }

        if (data < node.data) {
            node.left = this._insertNode(node.left, data);
        } else if (data > node.data) {
            node.right = this._insertNode(node.right, data);
        } else {
            return node; // Duplicate keys not allowed
        }

        // Update height
        this.updateHeight(node);

        // Get balance factor
        const balance = this.getBalance(node);

        // Left Left Case
        if (balance > 1 && data < node.left.data) {
            return this.rotateRight(node);
        }

        // Right Right Case
        if (balance < -1 && data > node.right.data) {
            return this.rotateLeft(node);
        }

        // Left Right Case
        if (balance > 1 && data > node.left.data) {
            node.left = this.rotateLeft(node.left);
            return this.rotateRight(node);
        }

        // Right Left Case
        if (balance < -1 && data < node.right.data) {
            node.right = this.rotateRight(node.right);
            return this.rotateLeft(node);
        }

        return node;
    }

    search(data) {
        return this._searchNode(this.root, data);
    }

    _searchNode(node, data) {
        if (!node) return false;

        if (data === node.data) return true;
        if (data < node.data) return this._searchNode(node.left, data);
        return this._searchNode(node.right, data);
    }

    inOrder(callback) {
        this._inOrderNode(this.root, callback);
    }

    _inOrderNode(node, callback) {
        if (node) {
            this._inOrderNode(node.left, callback);
            callback(node.data);
            this._inOrderNode(node.right, callback);
        }
    }
}

/**
 * Red-Black Tree Node
 */
class RBNode {
    constructor(data) {
        this.data = data;
        this.left = null;
        this.right = null;
        this.parent = null;
        this.color = 'RED';
    }
}

/**
 * Red-Black Tree - Self-balancing BST
 */
export class RedBlackTree {
    constructor() {
        this.root = null;
    }

    insert(data) {
        const node = new RBNode(data);

        if (!this.root) {
            node.color = 'BLACK';
            this.root = node;
        } else {
            this._insertNode(this.root, node);
            this._fixInsert(node);
        }
    }

    _insertNode(root, node) {
        if (node.data < root.data) {
            if (!root.left) {
                root.left = node;
                node.parent = root;
            } else {
                this._insertNode(root.left, node);
            }
        } else {
            if (!root.right) {
                root.right = node;
                node.parent = root;
            } else {
                this._insertNode(root.right, node);
            }
        }
    }

    _fixInsert(node) {
        while (node !== this.root && node.parent.color === 'RED') {
            const parent = node.parent;
            const grandParent = parent.parent;

            if (parent === grandParent.left) {
                const uncle = grandParent.right;

                if (uncle && uncle.color === 'RED') {
                    // Case 1: Uncle is red
                    parent.color = 'BLACK';
                    uncle.color = 'BLACK';
                    grandParent.color = 'RED';
                    node = grandParent;
                } else {
                    if (node === parent.right) {
                        // Case 2: Node is right child
                        this._rotateLeft(parent);
                        node = parent;
                    }
                    // Case 3: Node is left child
                    parent.color = 'BLACK';
                    grandParent.color = 'RED';
                    this._rotateRight(grandParent);
                }
            } else {
                const uncle = grandParent.left;

                if (uncle && uncle.color === 'RED') {
                    parent.color = 'BLACK';
                    uncle.color = 'BLACK';
                    grandParent.color = 'RED';
                    node = grandParent;
                } else {
                    if (node === parent.left) {
                        this._rotateRight(parent);
                        node = parent;
                    }
                    parent.color = 'BLACK';
                    grandParent.color = 'RED';
                    this._rotateLeft(grandParent);
                }
            }
        }

        this.root.color = 'BLACK';
    }

    _rotateLeft(node) {
        const rightChild = node.right;
        node.right = rightChild.left;

        if (rightChild.left) {
            rightChild.left.parent = node;
        }

        rightChild.parent = node.parent;

        if (!node.parent) {
            this.root = rightChild;
        } else if (node === node.parent.left) {
            node.parent.left = rightChild;
        } else {
            node.parent.right = rightChild;
        }

        rightChild.left = node;
        node.parent = rightChild;
    }

    _rotateRight(node) {
        const leftChild = node.left;
        node.left = leftChild.right;

        if (leftChild.right) {
            leftChild.right.parent = node;
        }

        leftChild.parent = node.parent;

        if (!node.parent) {
            this.root = leftChild;
        } else if (node === node.parent.right) {
            node.parent.right = leftChild;
        } else {
            node.parent.left = leftChild;
        }

        leftChild.right = node;
        node.parent = leftChild;
    }

    search(data) {
        return this._searchNode(this.root, data);
    }

    _searchNode(node, data) {
        if (!node) return false;

        if (data === node.data) return true;
        if (data < node.data) return this._searchNode(node.left, data);
        return this._searchNode(node.right, data);
    }
}

/**
 * Min Heap
 */
export class Heap {
    constructor(compareFunc = (a, b) => a - b) {
        this.items = [];
        this.compare = compareFunc;
    }

    getLeftChildIndex(parentIndex) {
        return 2 * parentIndex + 1;
    }

    getRightChildIndex(parentIndex) {
        return 2 * parentIndex + 2;
    }

    getParentIndex(childIndex) {
        return Math.floor((childIndex - 1) / 2);
    }

    hasLeftChild(index) {
        return this.getLeftChildIndex(index) < this.items.length;
    }

    hasRightChild(index) {
        return this.getRightChildIndex(index) < this.items.length;
    }

    hasParent(index) {
        return this.getParentIndex(index) >= 0;
    }

    leftChild(index) {
        return this.items[this.getLeftChildIndex(index)];
    }

    rightChild(index) {
        return this.items[this.getRightChildIndex(index)];
    }

    parent(index) {
        return this.items[this.getParentIndex(index)];
    }

    swap(indexOne, indexTwo) {
        [this.items[indexOne], this.items[indexTwo]] =
        [this.items[indexTwo], this.items[indexOne]];
    }

    peek() {
        if (this.items.length === 0) return undefined;
        return this.items[0];
    }

    poll() {
        if (this.items.length === 0) return undefined;

        const item = this.items[0];
        this.items[0] = this.items[this.items.length - 1];
        this.items.pop();
        this.heapifyDown();

        return item;
    }

    add(item) {
        this.items.push(item);
        this.heapifyUp();
    }

    heapifyUp() {
        let index = this.items.length - 1;

        while (this.hasParent(index) &&
               this.compare(this.parent(index), this.items[index]) > 0) {
            this.swap(this.getParentIndex(index), index);
            index = this.getParentIndex(index);
        }
    }

    heapifyDown() {
        let index = 0;

        while (this.hasLeftChild(index)) {
            let smallerChildIndex = this.getLeftChildIndex(index);

            if (this.hasRightChild(index) &&
                this.compare(this.rightChild(index), this.leftChild(index)) < 0) {
                smallerChildIndex = this.getRightChildIndex(index);
            }

            if (this.compare(this.items[index], this.items[smallerChildIndex]) < 0) {
                break;
            } else {
                this.swap(index, smallerChildIndex);
            }

            index = smallerChildIndex;
        }
    }

    isEmpty() {
        return this.items.length === 0;
    }

    size() {
        return this.items.length;
    }

    clear() {
        this.items = [];
    }
}

/**
 * Hash Table
 */
export class HashTable {
    constructor(size = 53) {
        this.keyMap = new Array(size);
        this.size = size;
    }

    _hash(key) {
        let total = 0;
        const PRIME = 31;

        for (let i = 0; i < Math.min(key.length, 100); i++) {
            const char = key[i];
            const value = char.charCodeAt(0) - 96;
            total = (total * PRIME + value) % this.size;
        }

        return total;
    }

    set(key, value) {
        const index = this._hash(key);

        if (!this.keyMap[index]) {
            this.keyMap[index] = [];
        }

        // Check if key already exists
        const existing = this.keyMap[index].find(item => item[0] === key);
        if (existing) {
            existing[1] = value;
        } else {
            this.keyMap[index].push([key, value]);
        }
    }

    get(key) {
        const index = this._hash(key);

        if (this.keyMap[index]) {
            const item = this.keyMap[index].find(item => item[0] === key);
            if (item) return item[1];
        }

        return undefined;
    }

    has(key) {
        const index = this._hash(key);

        if (this.keyMap[index]) {
            return this.keyMap[index].some(item => item[0] === key);
        }

        return false;
    }

    delete(key) {
        const index = this._hash(key);

        if (this.keyMap[index]) {
            const itemIndex = this.keyMap[index].findIndex(item => item[0] === key);
            if (itemIndex !== -1) {
                this.keyMap[index].splice(itemIndex, 1);
                return true;
            }
        }

        return false;
    }

    keys() {
        const keys = [];

        for (const slot of this.keyMap) {
            if (slot) {
                for (const [key] of slot) {
                    keys.push(key);
                }
            }
        }

        return keys;
    }

    values() {
        const values = [];
        const seen = new Set();

        for (const slot of this.keyMap) {
            if (slot) {
                for (const [, value] of slot) {
                    if (!seen.has(value)) {
                        values.push(value);
                        seen.add(value);
                    }
                }
            }
        }

        return values;
    }

    entries() {
        const entries = [];

        for (const slot of this.keyMap) {
            if (slot) {
                for (const entry of slot) {
                    entries.push(entry);
                }
            }
        }

        return entries;
    }

    clear() {
        this.keyMap = new Array(this.size);
    }
}

/**
 * Trie (Prefix Tree)
 */
class TrieNode {
    constructor() {
        this.children = {};
        this.isEndOfWord = false;
    }
}

export class Trie {
    constructor() {
        this.root = new TrieNode();
    }

    insert(word) {
        let current = this.root;

        for (const char of word) {
            if (!current.children[char]) {
                current.children[char] = new TrieNode();
            }
            current = current.children[char];
        }

        current.isEndOfWord = true;
    }

    search(word) {
        let current = this.root;

        for (const char of word) {
            if (!current.children[char]) {
                return false;
            }
            current = current.children[char];
        }

        return current.isEndOfWord;
    }

    startsWith(prefix) {
        let current = this.root;

        for (const char of prefix) {
            if (!current.children[char]) {
                return false;
            }
            current = current.children[char];
        }

        return true;
    }

    delete(word) {
        return this._deleteHelper(this.root, word, 0);
    }

    _deleteHelper(node, word, index) {
        if (index === word.length) {
            if (!node.isEndOfWord) {
                return false;
            }
            node.isEndOfWord = false;
            return Object.keys(node.children).length === 0;
        }

        const char = word[index];
        const childNode = node.children[char];

        if (!childNode) {
            return false;
        }

        const shouldDeleteChild = this._deleteHelper(childNode, word, index + 1);

        if (shouldDeleteChild) {
            delete node.children[char];
            return Object.keys(node.children).length === 0 && !node.isEndOfWord;
        }

        return false;
    }

    getAllWords(node = this.root, prefix = '', words = []) {
        if (node.isEndOfWord) {
            words.push(prefix);
        }

        for (const [char, childNode] of Object.entries(node.children)) {
            this.getAllWords(childNode, prefix + char, words);
        }

        return words;
    }

    autoComplete(prefix) {
        let current = this.root;

        for (const char of prefix) {
            if (!current.children[char]) {
                return [];
            }
            current = current.children[char];
        }

        return this.getAllWords(current, prefix);
    }
}

/**
 * Disjoint Set (Union-Find)
 */
export class DisjointSet {
    constructor(size) {
        this.parent = Array(size).fill(0).map((_, i) => i);
        this.rank = Array(size).fill(0);
        this.size = size;
    }

    find(x) {
        if (this.parent[x] !== x) {
            // Path compression
            this.parent[x] = this.find(this.parent[x]);
        }
        return this.parent[x];
    }

    union(x, y) {
        const rootX = this.find(x);
        const rootY = this.find(y);

        if (rootX === rootY) {
            return false;
        }

        // Union by rank
        if (this.rank[rootX] < this.rank[rootY]) {
            this.parent[rootX] = rootY;
        } else if (this.rank[rootX] > this.rank[rootY]) {
            this.parent[rootY] = rootX;
        } else {
            this.parent[rootY] = rootX;
            this.rank[rootX]++;
        }

        return true;
    }

    connected(x, y) {
        return this.find(x) === this.find(y);
    }

    getComponents() {
        const components = {};

        for (let i = 0; i < this.size; i++) {
            const root = this.find(i);
            if (!components[root]) {
                components[root] = [];
            }
            components[root].push(i);
        }

        return Object.values(components);
    }
}

/**
 * Segment Tree
 */
export class SegmentTree {
    constructor(arr, operation = (a, b) => a + b, identity = 0) {
        this.n = arr.length;
        this.tree = new Array(4 * this.n);
        this.operation = operation;
        this.identity = identity;

        if (this.n > 0) {
            this._build(arr, 0, 0, this.n - 1);
        }
    }

    _build(arr, node, start, end) {
        if (start === end) {
            this.tree[node] = arr[start];
        } else {
            const mid = Math.floor((start + end) / 2);
            const leftChild = 2 * node + 1;
            const rightChild = 2 * node + 2;

            this._build(arr, leftChild, start, mid);
            this._build(arr, rightChild, mid + 1, end);

            this.tree[node] = this.operation(
                this.tree[leftChild],
                this.tree[rightChild]
            );
        }
    }

    query(left, right) {
        if (left < 0 || right >= this.n || left > right) {
            return this.identity;
        }
        return this._query(0, 0, this.n - 1, left, right);
    }

    _query(node, start, end, left, right) {
        if (left > end || right < start) {
            return this.identity;
        }

        if (left <= start && end <= right) {
            return this.tree[node];
        }

        const mid = Math.floor((start + end) / 2);
        const leftChild = 2 * node + 1;
        const rightChild = 2 * node + 2;

        return this.operation(
            this._query(leftChild, start, mid, left, right),
            this._query(rightChild, mid + 1, end, left, right)
        );
    }

    update(index, value) {
        if (index < 0 || index >= this.n) return;
        this._update(0, 0, this.n - 1, index, value);
    }

    _update(node, start, end, index, value) {
        if (start === end) {
            this.tree[node] = value;
        } else {
            const mid = Math.floor((start + end) / 2);
            const leftChild = 2 * node + 1;
            const rightChild = 2 * node + 2;

            if (index <= mid) {
                this._update(leftChild, start, mid, index, value);
            } else {
                this._update(rightChild, mid + 1, end, index, value);
            }

            this.tree[node] = this.operation(
                this.tree[leftChild],
                this.tree[rightChild]
            );
        }
    }
}

/**
 * Fenwick Tree (Binary Indexed Tree)
 */
export class FenwickTree {
    constructor(size) {
        this.size = size;
        this.tree = new Array(size + 1).fill(0);
    }

    update(index, delta) {
        index++; // Convert to 1-indexed
        while (index <= this.size) {
            this.tree[index] += delta;
            index += index & (-index);
        }
    }

    query(index) {
        index++; // Convert to 1-indexed
        let sum = 0;
        while (index > 0) {
            sum += this.tree[index];
            index -= index & (-index);
        }
        return sum;
    }

    rangeQuery(left, right) {
        if (left > 0) {
            return this.query(right) - this.query(left - 1);
        }
        return this.query(right);
    }

    build(arr) {
        for (let i = 0; i < arr.length; i++) {
            this.update(i, arr[i]);
        }
    }
}

// Export all data structures
export default {
    Stack,
    Queue,
    Deque,
    PriorityQueue,
    LinkedList,
    DoublyLinkedList,
    BinarySearchTree,
    AVLTree,
    RedBlackTree,
    Heap,
    HashTable,
    Trie,
    DisjointSet,
    SegmentTree,
    FenwickTree
};