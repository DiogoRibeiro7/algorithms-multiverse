/**
 * Comprehensive Linked List Implementations in JavaScript
 *
 * Includes:
 * 1. Singly Linked List
 * 2. Doubly Linked List
 * 3. Circular Linked List
 * 4. Skip List (Probabilistic Data Structure)
 *
 * Features:
 * - ES6+ modern JavaScript
 * - Iterator protocol support
 * - Memory management considerations
 * - Performance comparisons
 * - Real-world use cases
 *
 * Usage:
 *   node linkedlist.js
 */

// ============================================================================
// SINGLY LINKED LIST
// ============================================================================

class SinglyNode {
    constructor(data) {
        this.data = data;
        this.next = null;
    }
}

class SinglyLinkedList {
    /**
     * Singly Linked List - unidirectional traversal
     *
     * Best for:
     * - Stack implementation
     * - Forward-only iteration
     * - Memory-constrained environments
     */

    constructor() {
        this.head = null;
        this.size = 0;
    }

    insertAtHead(data) {
        const newNode = new SinglyNode(data);
        newNode.next = this.head;
        this.head = newNode;
        this.size++;
    }

    insertAtTail(data) {
        const newNode = new SinglyNode(data);

        if (!this.head) {
            this.head = newNode;
        } else {
            let current = this.head;
            while (current.next) {
                current = current.next;
            }
            current.next = newNode;
        }

        this.size++;
    }

    insertAtPosition(data, position) {
        if (position < 0 || position > this.size) {
            throw new Error('Position out of bounds');
        }

        if (position === 0) {
            this.insertAtHead(data);
            return;
        }

        const newNode = new SinglyNode(data);
        let current = this.head;

        for (let i = 0; i < position - 1; i++) {
            current = current.next;
        }

        newNode.next = current.next;
        current.next = newNode;
        this.size++;
    }

    deleteAtHead() {
        if (!this.head) return null;

        const data = this.head.data;
        this.head = this.head.next;
        this.size--;
        return data;
    }

    deleteAtTail() {
        if (!this.head) return null;

        if (!this.head.next) {
            const data = this.head.data;
            this.head = null;
            this.size--;
            return data;
        }

        let current = this.head;
        while (current.next.next) {
            current = current.next;
        }

        const data = current.next.data;
        current.next = null;
        this.size--;
        return data;
    }

    deleteValue(value) {
        if (!this.head) return false;

        if (this.head.data === value) {
            this.head = this.head.next;
            this.size--;
            return true;
        }

        let current = this.head;
        while (current.next) {
            if (current.next.data === value) {
                current.next = current.next.next;
                this.size--;
                return true;
            }
            current = current.next;
        }

        return false;
    }

    search(value) {
        let current = this.head;
        while (current) {
            if (current.data === value) {
                return current;
            }
            current = current.next;
        }
        return null;
    }

    reverse() {
        let prev = null;
        let current = this.head;

        while (current) {
            const next = current.next;
            current.next = prev;
            prev = current;
            current = next;
        }

        this.head = prev;
    }

    getMiddle() {
        if (!this.head) return null;

        let slow = this.head;
        let fast = this.head;

        while (fast.next && fast.next.next) {
            slow = slow.next;
            fast = fast.next.next;
        }

        return slow.data;
    }

    detectCycle() {
        if (!this.head) return false;

        let slow = this.head;
        let fast = this.head;

        while (fast && fast.next) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow === fast) return true;
        }

        return false;
    }

    mergeSorted(other) {
        const result = new SinglyLinkedList();
        let current1 = this.head;
        let current2 = other.head;

        if (!current1) {
            result.head = current2;
            result.size = other.size;
            return result;
        }
        if (!current2) {
            result.head = current1;
            result.size = this.size;
            return result;
        }

        if (current1.data <= current2.data) {
            result.head = current1;
            current1 = current1.next;
        } else {
            result.head = current2;
            current2 = current2.next;
        }

        let current = result.head;

        while (current1 && current2) {
            if (current1.data <= current2.data) {
                current.next = current1;
                current1 = current1.next;
            } else {
                current.next = current2;
                current2 = current2.next;
            }
            current = current.next;
        }

        current.next = current1 || current2;
        result.size = this.size + other.size;

        return result;
    }

    *[Symbol.iterator]() {
        let current = this.head;
        while (current) {
            yield current.data;
            current = current.next;
        }
    }

    toArray() {
        return Array.from(this);
    }

    toString() {
        return this.toArray().join(' -> ') + ' -> null';
    }

    get length() {
        return this.size;
    }
}

// ============================================================================
// DOUBLY LINKED LIST
// ============================================================================

class DoublyNode {
    constructor(data) {
        this.data = data;
        this.next = null;
        this.prev = null;
    }
}

class DoublyLinkedList {
    /**
     * Doubly Linked List - bidirectional traversal
     *
     * Best for:
     * - Browser history
     * - LRU cache
     * - Deque implementation
     * - Undo/Redo functionality
     */

    constructor() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }

    insertAtHead(data) {
        const newNode = new DoublyNode(data);

        if (!this.head) {
            this.head = this.tail = newNode;
        } else {
            newNode.next = this.head;
            this.head.prev = newNode;
            this.head = newNode;
        }

        this.size++;
    }

    insertAtTail(data) {
        const newNode = new DoublyNode(data);

        if (!this.tail) {
            this.head = this.tail = newNode;
        } else {
            newNode.prev = this.tail;
            this.tail.next = newNode;
            this.tail = newNode;
        }

        this.size++;
    }

    deleteAtHead() {
        if (!this.head) return null;

        const data = this.head.data;

        if (this.head === this.tail) {
            this.head = this.tail = null;
        } else {
            this.head = this.head.next;
            this.head.prev = null;
        }

        this.size--;
        return data;
    }

    deleteAtTail() {
        if (!this.tail) return null;

        const data = this.tail.data;

        if (this.head === this.tail) {
            this.head = this.tail = null;
        } else {
            this.tail = this.tail.prev;
            this.tail.next = null;
        }

        this.size--;
        return data;
    }

    deleteNode(node) {
        if (node.prev) {
            node.prev.next = node.next;
        } else {
            this.head = node.next;
        }

        if (node.next) {
            node.next.prev = node.prev;
        } else {
            this.tail = node.prev;
        }

        this.size--;
    }

    reverse() {
        let current = this.head;
        [this.head, this.tail] = [this.tail, this.head];

        while (current) {
            [current.prev, current.next] = [current.next, current.prev];
            current = current.prev;
        }
    }

    *[Symbol.iterator]() {
        let current = this.head;
        while (current) {
            yield current.data;
            current = current.next;
        }
    }

    *reverseIterator() {
        let current = this.tail;
        while (current) {
            yield current.data;
            current = current.prev;
        }
    }

    toString() {
        return Array.from(this).join(' <-> ') + ' <-> null';
    }

    get length() {
        return this.size;
    }
}

// ============================================================================
// CIRCULAR LINKED LIST
// ============================================================================

class CircularLinkedList {
    /**
     * Circular Linked List - last node points to first
     *
     * Best for:
     * - Round-robin scheduling
     * - Circular buffers
     * - Music playlist on repeat
     * - Multiplayer game turns
     */

    constructor() {
        this.head = null;
        this.size = 0;
    }

    insertAtHead(data) {
        const newNode = new SinglyNode(data);

        if (!this.head) {
            newNode.next = newNode;
            this.head = newNode;
        } else {
            let current = this.head;
            while (current.next !== this.head) {
                current = current.next;
            }

            newNode.next = this.head;
            current.next = newNode;
            this.head = newNode;
        }

        this.size++;
    }

    insertAtTail(data) {
        const newNode = new SinglyNode(data);

        if (!this.head) {
            newNode.next = newNode;
            this.head = newNode;
        } else {
            let current = this.head;
            while (current.next !== this.head) {
                current = current.next;
            }

            current.next = newNode;
            newNode.next = this.head;
        }

        this.size++;
    }

    deleteAtHead() {
        if (!this.head) return null;

        const data = this.head.data;

        if (this.head.next === this.head) {
            this.head = null;
        } else {
            let current = this.head;
            while (current.next !== this.head) {
                current = current.next;
            }

            current.next = this.head.next;
            this.head = this.head.next;
        }

        this.size--;
        return data;
    }

    traverse(callback) {
        if (!this.head) return;

        let current = this.head;
        do {
            callback(current.data);
            current = current.next;
        } while (current !== this.head);
    }

    *[Symbol.iterator]() {
        if (!this.head) return;

        let current = this.head;
        do {
            yield current.data;
            current = current.next;
        } while (current !== this.head);
    }

    toString() {
        return Array.from(this).join(' -> ') + ' -> (head)';
    }

    get length() {
        return this.size;
    }
}

// ============================================================================
// SKIP LIST
// ============================================================================

class SkipNode {
    constructor(data, level) {
        this.data = data;
        this.forward = new Array(level + 1).fill(null);
    }
}

class SkipList {
    /**
     * Skip List - probabilistic data structure
     *
     * Best for:
     * - Fast search in sorted data
     * - In-memory databases
     * - Concurrent data structures
     * - Alternative to balanced trees
     *
     * Used by: Redis (sorted sets)
     */

    constructor() {
        this.MAX_LEVEL = 16;
        this.P = 0.5;
        this.level = 0;
        this.header = new SkipNode(null, this.MAX_LEVEL);
        this.size = 0;
    }

    randomLevel() {
        let level = 0;
        while (Math.random() < this.P && level < this.MAX_LEVEL) {
            level++;
        }
        return level;
    }

    insert(data) {
        const update = new Array(this.MAX_LEVEL + 1);
        let current = this.header;

        for (let i = this.level; i >= 0; i--) {
            while (current.forward[i] && current.forward[i].data < data) {
                current = current.forward[i];
            }
            update[i] = current;
        }

        const newLevel = this.randomLevel();

        if (newLevel > this.level) {
            for (let i = this.level + 1; i <= newLevel; i++) {
                update[i] = this.header;
            }
            this.level = newLevel;
        }

        const newNode = new SkipNode(data, newLevel);

        for (let i = 0; i <= newLevel; i++) {
            newNode.forward[i] = update[i].forward[i];
            update[i].forward[i] = newNode;
        }

        this.size++;
    }

    search(data) {
        let current = this.header;

        for (let i = this.level; i >= 0; i--) {
            while (current.forward[i] && current.forward[i].data < data) {
                current = current.forward[i];
            }
        }

        current = current.forward[0];
        return current !== null && current.data === data;
    }

    delete(data) {
        const update = new Array(this.MAX_LEVEL + 1);
        let current = this.header;

        for (let i = this.level; i >= 0; i--) {
            while (current.forward[i] && current.forward[i].data < data) {
                current = current.forward[i];
            }
            update[i] = current;
        }

        current = current.forward[0];

        if (!current || current.data !== data) {
            return false;
        }

        for (let i = 0; i <= this.level; i++) {
            if (update[i].forward[i] !== current) break;
            update[i].forward[i] = current.forward[i];
        }

        while (this.level > 0 && !this.header.forward[this.level]) {
            this.level--;
        }

        this.size--;
        return true;
    }

    *[Symbol.iterator]() {
        let current = this.header.forward[0];
        while (current) {
            yield current.data;
            current = current.forward[0];
        }
    }

    toArray() {
        return Array.from(this);
    }

    toString() {
        return `SkipList([${this.toArray().join(', ')}])`;
    }

    get length() {
        return this.size;
    }
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

function demonstrateLinkedLists() {
    console.log('='.repeat(80));
    console.log('COMPREHENSIVE LINKED LIST DEMONSTRATIONS');
    console.log('='.repeat(80));

    // Singly Linked List
    console.log('\n1. SINGLY LINKED LIST');
    console.log('-'.repeat(80));
    const sll = new SinglyLinkedList();

    console.log('Inserting: 1, 2, 3 at head');
    sll.insertAtHead(3);
    sll.insertAtHead(2);
    sll.insertAtHead(1);
    console.log(`List: ${sll}`);

    console.log('\nInserting: 4, 5 at tail');
    sll.insertAtTail(4);
    sll.insertAtTail(5);
    console.log(`List: ${sll}`);

    console.log(`\nMiddle element: ${sll.getMiddle()}`);

    console.log('\nReversing list...');
    sll.reverse();
    console.log(`List: ${sll}`);

    // Doubly Linked List
    console.log('\n2. DOUBLY LINKED LIST');
    console.log('-'.repeat(80));
    const dll = new DoublyLinkedList();

    console.log('Inserting: A, B, C at head');
    dll.insertAtHead('C');
    dll.insertAtHead('B');
    dll.insertAtHead('A');
    console.log(`List: ${dll}`);

    console.log('\nInserting: D, E at tail');
    dll.insertAtTail('D');
    dll.insertAtTail('E');
    console.log(`List: ${dll}`);

    console.log('\nForward iteration:', [...dll]);
    console.log('Backward iteration:', [...dll.reverseIterator()]);

    console.log('\nDeleting head and tail...');
    dll.deleteAtHead();
    dll.deleteAtTail();
    console.log(`List: ${dll}`);

    // Circular Linked List
    console.log('\n3. CIRCULAR LINKED LIST');
    console.log('-'.repeat(80));
    const cll = new CircularLinkedList();

    console.log('Inserting: 1, 2, 3, 4, 5');
    for (let i = 1; i <= 5; i++) {
        cll.insertAtTail(i);
    }
    console.log(`List: ${cll}`);

    // Skip List
    console.log('\n4. SKIP LIST');
    console.log('-'.repeat(80));
    const sl = new SkipList();

    console.log('Inserting: 3, 7, 1, 9, 5, 2, 8, 4, 6');
    [3, 7, 1, 9, 5, 2, 8, 4, 6].forEach(val => sl.insert(val));

    console.log(`Skip list (sorted): ${sl.toArray()}`);

    console.log('\nSearching for 5:', sl.search(5));
    console.log('Searching for 10:', sl.search(10));

    console.log('\nDeleting 5...');
    sl.delete(5);
    console.log(`Skip list: ${sl.toArray()}`);

    // Use Cases
    console.log('\n5. USE CASE EXAMPLES');
    console.log('-'.repeat(80));
    console.log(`
Singly Linked List:
✓ Stack implementation
✓ Simple queues
✓ Hash table chaining

Doubly Linked List:
✓ Browser history (back/forward)
✓ LRU cache
✓ Music player playlist
✓ Text editor cursor

Circular Linked List:
✓ Round-robin scheduling
✓ Circular buffers
✓ Multiplayer game turns

Skip List:
✓ Redis sorted sets
✓ In-memory databases
✓ Concurrent collections
    `);

    console.log('='.repeat(80));
    console.log('✨ All demonstrations complete!');
    console.log('='.repeat(80));
}

// Run demonstration
if (typeof module !== 'undefined' && require.main === module) {
    demonstrateLinkedLists();
}

// Export for use as module
if (typeof module !== 'undefined') {
    module.exports = {
        SinglyLinkedList,
        DoublyLinkedList,
        CircularLinkedList,
        SkipList
    };
}
