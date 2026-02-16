/**
 * Data Structures in TypeScript
 * ==============================
 *
 * Advanced data structures with TypeScript features:
 * - Generic types for type safety
 * - Iterator support
 * - Method chaining
 * - Comprehensive error handling
 *
 * @module dataStructures
 * @author Algorithms Multiverse
 */

/**
 * Generic node class for linked structures
 */
class Node<T> {
    constructor(
        public data: T,
        public next: Node<T> | null = null
    ) {}
}

/**
 * Generic tree node class
 */
class TreeNode<T> {
    constructor(
        public data: T,
        public left: TreeNode<T> | null = null,
        public right: TreeNode<T> | null = null
    ) {}
}

/**
 * Linked List Implementation
 */
export class LinkedList<T> implements Iterable<T> {
    private head: Node<T> | null = null;
    private tail: Node<T> | null = null;
    private size = 0;

    /**
     * Add element to the end of the list
     */
    append(data: T): LinkedList<T> {
        const node = new Node(data);

        if (!this.head) {
            this.head = this.tail = node;
        } else {
            this.tail!.next = node;
            this.tail = node;
        }

        this.size++;
        return this;
    }

    /**
     * Add element to the beginning of the list
     */
    prepend(data: T): LinkedList<T> {
        const node = new Node(data, this.head);
        this.head = node;

        if (!this.tail) {
            this.tail = node;
        }

        this.size++;
        return this;
    }

    /**
     * Insert at specific index
     */
    insertAt(index: number, data: T): boolean {
        if (index < 0 || index > this.size) {
            throw new RangeError(`Index ${index} out of bounds`);
        }

        if (index === 0) {
            this.prepend(data);
            return true;
        }

        if (index === this.size) {
            this.append(data);
            return true;
        }

        const node = new Node(data);
        let current = this.head;
        let prev: Node<T> | null = null;
        let i = 0;

        while (i < index && current) {
            prev = current;
            current = current.next;
            i++;
        }

        node.next = current;
        prev!.next = node;
        this.size++;

        return true;
    }

    /**
     * Remove first occurrence of value
     */
    remove(data: T): boolean {
        if (!this.head) return false;

        if (this.head.data === data) {
            this.head = this.head.next;
            if (!this.head) {
                this.tail = null;
            }
            this.size--;
            return true;
        }

        let current = this.head;
        let prev: Node<T> | null = null;

        while (current) {
            if (current.data === data) {
                prev!.next = current.next;
                if (current === this.tail) {
                    this.tail = prev;
                }
                this.size--;
                return true;
            }
            prev = current;
            current = current.next;
        }

        return false;
    }

    /**
     * Find element in the list
     */
    find(predicate: (value: T) => boolean): T | undefined {
        let current = this.head;

        while (current) {
            if (predicate(current.data)) {
                return current.data;
            }
            current = current.next;
        }

        return undefined;
    }

    /**
     * Convert to array
     */
    toArray(): T[] {
        const result: T[] = [];
        let current = this.head;

        while (current) {
            result.push(current.data);
            current = current.next;
        }

        return result;
    }

    /**
     * Iterator implementation
     */
    *[Symbol.iterator](): Iterator<T> {
        let current = this.head;

        while (current) {
            yield current.data;
            current = current.next;
        }
    }

    get length(): number {
        return this.size;
    }

    clear(): void {
        this.head = this.tail = null;
        this.size = 0;
    }
}

/**
 * Stack Implementation (LIFO)
 */
export class Stack<T> {
    private items: T[] = [];

    push(...elements: T[]): number {
        this.items.push(...elements);
        return this.items.length;
    }

    pop(): T | undefined {
        return this.items.pop();
    }

    peek(): T | undefined {
        return this.items[this.items.length - 1];
    }

    isEmpty(): boolean {
        return this.items.length === 0;
    }

    clear(): void {
        this.items = [];
    }

    get size(): number {
        return this.items.length;
    }

    toArray(): T[] {
        return [...this.items];
    }
}

/**
 * Queue Implementation (FIFO)
 */
export class Queue<T> {
    private items: T[] = [];

    enqueue(...elements: T[]): number {
        this.items.push(...elements);
        return this.items.length;
    }

    dequeue(): T | undefined {
        return this.items.shift();
    }

    front(): T | undefined {
        return this.items[0];
    }

    rear(): T | undefined {
        return this.items[this.items.length - 1];
    }

    isEmpty(): boolean {
        return this.items.length === 0;
    }

    clear(): void {
        this.items = [];
    }

    get size(): number {
        return this.items.length;
    }

    toArray(): T[] {
        return [...this.items];
    }
}

/**
 * Priority Queue Implementation (Min Heap)
 */
export class PriorityQueue<T> {
    private heap: Array<{ priority: number; value: T }> = [];

    enqueue(value: T, priority: number): void {
        const node = { priority, value };
        this.heap.push(node);
        this.bubbleUp(this.heap.length - 1);
    }

    dequeue(): T | undefined {
        if (this.isEmpty()) return undefined;

        if (this.heap.length === 1) {
            return this.heap.pop()!.value;
        }

        const min = this.heap[0];
        this.heap[0] = this.heap.pop()!;
        this.bubbleDown(0);

        return min.value;
    }

    private bubbleUp(index: number): void {
        while (index > 0) {
            const parentIndex = Math.floor((index - 1) / 2);

            if (this.heap[index].priority >= this.heap[parentIndex].priority) {
                break;
            }

            [this.heap[index], this.heap[parentIndex]] = [this.heap[parentIndex], this.heap[index]];
            index = parentIndex;
        }
    }

    private bubbleDown(index: number): void {
        while (true) {
            const leftChild = 2 * index + 1;
            const rightChild = 2 * index + 2;
            let smallest = index;

            if (leftChild < this.heap.length &&
                this.heap[leftChild].priority < this.heap[smallest].priority) {
                smallest = leftChild;
            }

            if (rightChild < this.heap.length &&
                this.heap[rightChild].priority < this.heap[smallest].priority) {
                smallest = rightChild;
            }

            if (smallest === index) break;

            [this.heap[index], this.heap[smallest]] = [this.heap[smallest], this.heap[index]];
            index = smallest;
        }
    }

    peek(): T | undefined {
        return this.isEmpty() ? undefined : this.heap[0].value;
    }

    isEmpty(): boolean {
        return this.heap.length === 0;
    }

    get size(): number {
        return this.heap.length;
    }

    clear(): void {
        this.heap = [];
    }
}

/**
 * Binary Search Tree Implementation
 */
export class BinarySearchTree<T> {
    private root: TreeNode<T> | null = null;
    private compareFn: (a: T, b: T) => number;
    private size = 0;

    constructor(compareFn?: (a: T, b: T) => number) {
        this.compareFn = compareFn || ((a: T, b: T) => {
            if (a < b) return -1;
            if (a > b) return 1;
            return 0;
        });
    }

    /**
     * Insert value into the tree
     */
    insert(data: T): boolean {
        const node = new TreeNode(data);

        if (!this.root) {
            this.root = node;
            this.size++;
            return true;
        }

        let current = this.root;

        while (true) {
            const cmp = this.compareFn(data, current.data);

            if (cmp === 0) {
                return false; // Duplicate
            }

            if (cmp < 0) {
                if (!current.left) {
                    current.left = node;
                    this.size++;
                    return true;
                }
                current = current.left;
            } else {
                if (!current.right) {
                    current.right = node;
                    this.size++;
                    return true;
                }
                current = current.right;
            }
        }
    }

    /**
     * Search for a value
     */
    search(data: T): boolean {
        let current = this.root;

        while (current) {
            const cmp = this.compareFn(data, current.data);

            if (cmp === 0) return true;
            current = cmp < 0 ? current.left : current.right;
        }

        return false;
    }

    /**
     * Find minimum value
     */
    findMin(): T | undefined {
        if (!this.root) return undefined;

        let current = this.root;
        while (current.left) {
            current = current.left;
        }

        return current.data;
    }

    /**
     * Find maximum value
     */
    findMax(): T | undefined {
        if (!this.root) return undefined;

        let current = this.root;
        while (current.right) {
            current = current.right;
        }

        return current.data;
    }

    /**
     * Delete a value from the tree
     */
    delete(data: T): boolean {
        const deleteNode = (node: TreeNode<T> | null, data: T): TreeNode<T> | null => {
            if (!node) return null;

            const cmp = this.compareFn(data, node.data);

            if (cmp < 0) {
                node.left = deleteNode(node.left, data);
            } else if (cmp > 0) {
                node.right = deleteNode(node.right, data);
            } else {
                // Node found
                if (!node.left) return node.right;
                if (!node.right) return node.left;

                // Node with two children
                let minRight = node.right;
                while (minRight.left) {
                    minRight = minRight.left;
                }

                node.data = minRight.data;
                node.right = deleteNode(node.right, minRight.data);
            }

            return node;
        };

        const initialSize = this.size;
        this.root = deleteNode(this.root, data);

        if (this.getSize() < initialSize) {
            this.size--;
            return true;
        }

        return false;
    }

    /**
     * In-order traversal
     */
    inOrder(): T[] {
        const result: T[] = [];

        const traverse = (node: TreeNode<T> | null): void => {
            if (!node) return;
            traverse(node.left);
            result.push(node.data);
            traverse(node.right);
        };

        traverse(this.root);
        return result;
    }

    /**
     * Pre-order traversal
     */
    preOrder(): T[] {
        const result: T[] = [];

        const traverse = (node: TreeNode<T> | null): void => {
            if (!node) return;
            result.push(node.data);
            traverse(node.left);
            traverse(node.right);
        };

        traverse(this.root);
        return result;
    }

    /**
     * Post-order traversal
     */
    postOrder(): T[] {
        const result: T[] = [];

        const traverse = (node: TreeNode<T> | null): void => {
            if (!node) return;
            traverse(node.left);
            traverse(node.right);
            result.push(node.data);
        };

        traverse(this.root);
        return result;
    }

    /**
     * Level-order traversal (BFS)
     */
    levelOrder(): T[][] {
        if (!this.root) return [];

        const result: T[][] = [];
        const queue: TreeNode<T>[] = [this.root];

        while (queue.length > 0) {
            const levelSize = queue.length;
            const level: T[] = [];

            for (let i = 0; i < levelSize; i++) {
                const node = queue.shift()!;
                level.push(node.data);

                if (node.left) queue.push(node.left);
                if (node.right) queue.push(node.right);
            }

            result.push(level);
        }

        return result;
    }

    getSize(): number {
        const countNodes = (node: TreeNode<T> | null): number => {
            if (!node) return 0;
            return 1 + countNodes(node.left) + countNodes(node.right);
        };

        return countNodes(this.root);
    }

    getHeight(): number {
        const height = (node: TreeNode<T> | null): number => {
            if (!node) return -1;
            return 1 + Math.max(height(node.left), height(node.right));
        };

        return height(this.root);
    }

    clear(): void {
        this.root = null;
        this.size = 0;
    }
}

/**
 * Hash Table Implementation
 */
export class HashTable<K, V> {
    private buckets: Array<Array<[K, V]>>;
    private size = 0;
    private capacity: number;
    private loadFactor = 0.75;

    constructor(initialCapacity = 16) {
        this.capacity = initialCapacity;
        this.buckets = new Array(this.capacity).fill(null).map(() => []);
    }

    private hash(key: K): number {
        const str = String(key);
        let hash = 0;

        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }

        return Math.abs(hash) % this.capacity;
    }

    set(key: K, value: V): void {
        const index = this.hash(key);
        const bucket = this.buckets[index];

        const existing = bucket.find(([k]) => k === key);
        if (existing) {
            existing[1] = value;
        } else {
            bucket.push([key, value]);
            this.size++;

            if (this.size > this.capacity * this.loadFactor) {
                this.resize();
            }
        }
    }

    get(key: K): V | undefined {
        const index = this.hash(key);
        const bucket = this.buckets[index];
        const pair = bucket.find(([k]) => k === key);

        return pair ? pair[1] : undefined;
    }

    has(key: K): boolean {
        return this.get(key) !== undefined;
    }

    delete(key: K): boolean {
        const index = this.hash(key);
        const bucket = this.buckets[index];
        const pairIndex = bucket.findIndex(([k]) => k === key);

        if (pairIndex !== -1) {
            bucket.splice(pairIndex, 1);
            this.size--;
            return true;
        }

        return false;
    }

    private resize(): void {
        const oldBuckets = this.buckets;
        this.capacity *= 2;
        this.size = 0;
        this.buckets = new Array(this.capacity).fill(null).map(() => []);

        for (const bucket of oldBuckets) {
            for (const [key, value] of bucket) {
                this.set(key, value);
            }
        }
    }

    clear(): void {
        this.buckets = new Array(this.capacity).fill(null).map(() => []);
        this.size = 0;
    }

    keys(): K[] {
        const keys: K[] = [];
        for (const bucket of this.buckets) {
            for (const [key] of bucket) {
                keys.push(key);
            }
        }
        return keys;
    }

    values(): V[] {
        const values: V[] = [];
        for (const bucket of this.buckets) {
            for (const [, value] of bucket) {
                values.push(value);
            }
        }
        return values;
    }

    entries(): Array<[K, V]> {
        const entries: Array<[K, V]> = [];
        for (const bucket of this.buckets) {
            entries.push(...bucket);
        }
        return entries;
    }

    getSize(): number {
        return this.size;
    }
}

/**
 * Trie (Prefix Tree) Implementation
 */
class TrieNode {
    children: Map<string, TrieNode> = new Map();
    isEndOfWord = false;
}

export class Trie {
    private root = new TrieNode();
    private size = 0;

    /**
     * Insert a word into the trie
     */
    insert(word: string): void {
        let current = this.root;

        for (const char of word) {
            if (!current.children.has(char)) {
                current.children.set(char, new TrieNode());
            }
            current = current.children.get(char)!;
        }

        if (!current.isEndOfWord) {
            current.isEndOfWord = true;
            this.size++;
        }
    }

    /**
     * Search for a word
     */
    search(word: string): boolean {
        let current = this.root;

        for (const char of word) {
            if (!current.children.has(char)) {
                return false;
            }
            current = current.children.get(char)!;
        }

        return current.isEndOfWord;
    }

    /**
     * Check if any word starts with prefix
     */
    startsWith(prefix: string): boolean {
        let current = this.root;

        for (const char of prefix) {
            if (!current.children.has(char)) {
                return false;
            }
            current = current.children.get(char)!;
        }

        return true;
    }

    /**
     * Get all words with given prefix
     */
    getWordsWithPrefix(prefix: string): string[] {
        const results: string[] = [];
        let current = this.root;

        // Navigate to prefix node
        for (const char of prefix) {
            if (!current.children.has(char)) {
                return results;
            }
            current = current.children.get(char)!;
        }

        // DFS to find all words
        const dfs = (node: TrieNode, path: string): void => {
            if (node.isEndOfWord) {
                results.push(prefix + path);
            }

            for (const [char, child] of node.children) {
                dfs(child, path + char);
            }
        };

        dfs(current, '');
        return results;
    }

    /**
     * Delete a word from the trie
     */
    delete(word: string): boolean {
        const deleteHelper = (node: TrieNode, word: string, index: number): boolean => {
            if (index === word.length) {
                if (!node.isEndOfWord) {
                    return false;
                }
                node.isEndOfWord = false;
                this.size--;
                return node.children.size === 0;
            }

            const char = word[index];
            const child = node.children.get(char);

            if (!child) {
                return false;
            }

            const shouldDeleteChild = deleteHelper(child, word, index + 1);

            if (shouldDeleteChild) {
                node.children.delete(char);
                return node.children.size === 0 && !node.isEndOfWord;
            }

            return false;
        };

        return deleteHelper(this.root, word, 0);
    }

    getSize(): number {
        return this.size;
    }

    clear(): void {
        this.root = new TrieNode();
        this.size = 0;
    }
}

// Example usage and tests
if (require.main === module) {
    console.log("TypeScript Data Structures Demonstration");
    console.log("=" .repeat(50));

    // Linked List
    console.log("\n1. Linked List:");
    const list = new LinkedList<number>();
    list.append(1).append(2).append(3).prepend(0);
    console.log("List:", list.toArray());
    console.log("Length:", list.length);
    console.log("Iterating:", [...list]);

    // Stack
    console.log("\n2. Stack:");
    const stack = new Stack<string>();
    stack.push("first", "second", "third");
    console.log("Pop:", stack.pop());
    console.log("Peek:", stack.peek());
    console.log("Stack:", stack.toArray());

    // Queue
    console.log("\n3. Queue:");
    const queue = new Queue<number>();
    queue.enqueue(1, 2, 3);
    console.log("Dequeue:", queue.dequeue());
    console.log("Front:", queue.front());
    console.log("Queue:", queue.toArray());

    // Priority Queue
    console.log("\n4. Priority Queue:");
    const pq = new PriorityQueue<string>();
    pq.enqueue("low priority", 3);
    pq.enqueue("high priority", 1);
    pq.enqueue("medium priority", 2);
    console.log("Dequeue (highest priority):", pq.dequeue());
    console.log("Peek:", pq.peek());

    // Binary Search Tree
    console.log("\n5. Binary Search Tree:");
    const bst = new BinarySearchTree<number>();
    [50, 30, 70, 20, 40, 60, 80].forEach(val => bst.insert(val));
    console.log("In-order:", bst.inOrder());
    console.log("Level-order:", bst.levelOrder());
    console.log("Height:", bst.getHeight());
    console.log("Search 40:", bst.search(40));
    console.log("Min:", bst.findMin(), "Max:", bst.findMax());

    // Hash Table
    console.log("\n6. Hash Table:");
    const hashTable = new HashTable<string, number>();
    hashTable.set("apple", 5);
    hashTable.set("banana", 3);
    hashTable.set("orange", 7);
    console.log("Get 'banana':", hashTable.get("banana"));
    console.log("Has 'grape':", hashTable.has("grape"));
    console.log("Keys:", hashTable.keys());
    console.log("Values:", hashTable.values());

    // Trie
    console.log("\n7. Trie:");
    const trie = new Trie();
    ["apple", "app", "apricot", "banana", "band", "bandana"].forEach(word => trie.insert(word));
    console.log("Search 'app':", trie.search("app"));
    console.log("Starts with 'ban':", trie.startsWith("ban"));
    console.log("Words with prefix 'app':", trie.getWordsWithPrefix("app"));
    console.log("Size:", trie.getSize());
}