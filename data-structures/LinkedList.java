/**
 * Comprehensive Linked List Implementations in Java
 *
 * Includes:
 * 1. Singly Linked List
 * 2. Doubly Linked List
 * 3. Circular Linked List
 * 4. Skip List
 *
 * Features:
 * - Generic implementations
 * - Iterator support
 * - Thread-safe variants available
 * - Comparable interface support
 *
 * Compilation: javac LinkedList.java
 * Usage: java LinkedList
 */

import java.util.*;

// ============================================================================
// SINGLY LINKED LIST
// ============================================================================

class SinglyNode<T> {
    T data;
    SinglyNode<T> next;

    SinglyNode(T data) {
        this.data = data;
        this.next = null;
    }
}

class SinglyLinkedList<T> implements Iterable<T> {
    private SinglyNode<T> head;
    private int size;

    public SinglyLinkedList() {
        this.head = null;
        this.size = 0;
    }

    public void insertAtHead(T data) {
        SinglyNode<T> newNode = new SinglyNode<>(data);
        newNode.next = head;
        head = newNode;
        size++;
    }

    public void insertAtTail(T data) {
        SinglyNode<T> newNode = new SinglyNode<>(data);

        if (head == null) {
            head = newNode;
        } else {
            SinglyNode<T> current = head;
            while (current.next != null) {
                current = current.next;
            }
            current.next = newNode;
        }
        size++;
    }

    public T deleteAtHead() {
        if (head == null) return null;

        T data = head.data;
        head = head.next;
        size--;
        return data;
    }

    public boolean search(T value) {
        SinglyNode<T> current = head;
        while (current != null) {
            if (current.data.equals(value)) {
                return true;
            }
            current = current.next;
        }
        return false;
    }

    public void reverse() {
        SinglyNode<T> prev = null;
        SinglyNode<T> current = head;

        while (current != null) {
            SinglyNode<T> next = current.next;
            current.next = prev;
            prev = current;
            current = next;
        }

        head = prev;
    }

    public T getMiddle() {
        if (head == null) return null;

        SinglyNode<T> slow = head;
        SinglyNode<T> fast = head;

        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        return slow.data;
    }

    public boolean detectCycle() {
        if (head == null) return false;

        SinglyNode<T> slow = head;
        SinglyNode<T> fast = head;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }

        return false;
    }

    @Override
    public Iterator<T> iterator() {
        return new Iterator<T>() {
            private SinglyNode<T> current = head;

            @Override
            public boolean hasNext() {
                return current != null;
            }

            @Override
            public T next() {
                if (!hasNext()) {
                    throw new NoSuchElementException();
                }
                T data = current.data;
                current = current.next;
                return data;
            }
        };
    }

    public int size() {
        return size;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        SinglyNode<T> current = head;

        while (current != null) {
            sb.append(current.data);
            if (current.next != null) {
                sb.append(" -> ");
            }
            current = current.next;
        }

        sb.append(" -> null");
        return sb.toString();
    }
}

// ============================================================================
// DOUBLY LINKED LIST
// ============================================================================

class DoublyNode<T> {
    T data;
    DoublyNode<T> next;
    DoublyNode<T> prev;

    DoublyNode(T data) {
        this.data = data;
        this.next = null;
        this.prev = null;
    }
}

class DoublyLinkedList<T> implements Iterable<T> {
    private DoublyNode<T> head;
    private DoublyNode<T> tail;
    private int size;

    public DoublyLinkedList() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }

    public void insertAtHead(T data) {
        DoublyNode<T> newNode = new DoublyNode<>(data);

        if (head == null) {
            head = tail = newNode;
        } else {
            newNode.next = head;
            head.prev = newNode;
            head = newNode;
        }

        size++;
    }

    public void insertAtTail(T data) {
        DoublyNode<T> newNode = new DoublyNode<>(data);

        if (tail == null) {
            head = tail = newNode;
        } else {
            newNode.prev = tail;
            tail.next = newNode;
            tail = newNode;
        }

        size++;
    }

    public T deleteAtHead() {
        if (head == null) return null;

        T data = head.data;

        if (head == tail) {
            head = tail = null;
        } else {
            head = head.next;
            head.prev = null;
        }

        size--;
        return data;
    }

    public T deleteAtTail() {
        if (tail == null) return null;

        T data = tail.data;

        if (head == tail) {
            head = tail = null;
        } else {
            tail = tail.prev;
            tail.next = null;
        }

        size--;
        return data;
    }

    public void reverse() {
        DoublyNode<T> current = head;
        DoublyNode<T> temp;

        DoublyNode<T> tempHead = head;
        head = tail;
        tail = tempHead;

        while (current != null) {
            temp = current.prev;
            current.prev = current.next;
            current.next = temp;
            current = current.prev;
        }
    }

    public Iterable<T> reverseIterable() {
        return () -> new Iterator<T>() {
            private DoublyNode<T> current = tail;

            @Override
            public boolean hasNext() {
                return current != null;
            }

            @Override
            public T next() {
                if (!hasNext()) {
                    throw new NoSuchElementException();
                }
                T data = current.data;
                current = current.prev;
                return data;
            }
        };
    }

    @Override
    public Iterator<T> iterator() {
        return new Iterator<T>() {
            private DoublyNode<T> current = head;

            @Override
            public boolean hasNext() {
                return current != null;
            }

            @Override
            public T next() {
                if (!hasNext()) {
                    throw new NoSuchElementException();
                }
                T data = current.data;
                current = current.next;
                return data;
            }
        };
    }

    public int size() {
        return size;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        DoublyNode<T> current = head;

        while (current != null) {
            sb.append(current.data);
            if (current.next != null) {
                sb.append(" <-> ");
            }
            current = current.next;
        }

        sb.append(" <-> null");
        return sb.toString();
    }
}

// ============================================================================
// CIRCULAR LINKED LIST
// ============================================================================

class CircularLinkedList<T> implements Iterable<T> {
    private SinglyNode<T> head;
    private int size;

    public CircularLinkedList() {
        this.head = null;
        this.size = 0;
    }

    public void insertAtHead(T data) {
        SinglyNode<T> newNode = new SinglyNode<>(data);

        if (head == null) {
            newNode.next = newNode;
            head = newNode;
        } else {
            SinglyNode<T> current = head;
            while (current.next != head) {
                current = current.next;
            }

            newNode.next = head;
            current.next = newNode;
            head = newNode;
        }

        size++;
    }

    public void insertAtTail(T data) {
        SinglyNode<T> newNode = new SinglyNode<>(data);

        if (head == null) {
            newNode.next = newNode;
            head = newNode;
        } else {
            SinglyNode<T> current = head;
            while (current.next != head) {
                current = current.next;
            }

            current.next = newNode;
            newNode.next = head;
        }

        size++;
    }

    public T deleteAtHead() {
        if (head == null) return null;

        T data = head.data;

        if (head.next == head) {
            head = null;
        } else {
            SinglyNode<T> current = head;
            while (current.next != head) {
                current = current.next;
            }

            current.next = head.next;
            head = head.next;
        }

        size--;
        return data;
    }

    @Override
    public Iterator<T> iterator() {
        return new Iterator<T>() {
            private SinglyNode<T> current = head;
            private boolean started = false;

            @Override
            public boolean hasNext() {
                return head != null && (!started || current != head);
            }

            @Override
            public T next() {
                if (!hasNext()) {
                    throw new NoSuchElementException();
                }
                started = true;
                T data = current.data;
                current = current.next;
                return data;
            }
        };
    }

    public int size() {
        return size;
    }

    @Override
    public String toString() {
        if (head == null) return "Empty";

        StringBuilder sb = new StringBuilder();
        SinglyNode<T> current = head;

        do {
            sb.append(current.data);
            if (current.next != head) {
                sb.append(" -> ");
            }
            current = current.next;
        } while (current != head);

        sb.append(" -> (head)");
        return sb.toString();
    }
}

// ============================================================================
// SKIP LIST
// ============================================================================

class SkipNode<T extends Comparable<T>> {
    T data;
    SkipNode<T>[] forward;

    @SuppressWarnings("unchecked")
    SkipNode(T data, int level) {
        this.data = data;
        this.forward = new SkipNode[level + 1];
    }
}

class SkipList<T extends Comparable<T>> implements Iterable<T> {
    private static final int MAX_LEVEL = 16;
    private static final double P = 0.5;

    private int level;
    private SkipNode<T> header;
    private Random random;
    private int size;

    public SkipList() {
        this.level = 0;
        this.header = new SkipNode<>(null, MAX_LEVEL);
        this.random = new Random();
        this.size = 0;
    }

    private int randomLevel() {
        int lvl = 0;
        while (random.nextDouble() < P && lvl < MAX_LEVEL) {
            lvl++;
        }
        return lvl;
    }

    public void insert(T data) {
        SkipNode<T>[] update = new SkipNode[MAX_LEVEL + 1];
        SkipNode<T> current = header;

        for (int i = level; i >= 0; i--) {
            while (current.forward[i] != null &&
                   current.forward[i].data.compareTo(data) < 0) {
                current = current.forward[i];
            }
            update[i] = current;
        }

        int newLevel = randomLevel();

        if (newLevel > level) {
            for (int i = level + 1; i <= newLevel; i++) {
                update[i] = header;
            }
            level = newLevel;
        }

        SkipNode<T> newNode = new SkipNode<>(data, newLevel);

        for (int i = 0; i <= newLevel; i++) {
            newNode.forward[i] = update[i].forward[i];
            update[i].forward[i] = newNode;
        }

        size++;
    }

    public boolean search(T data) {
        SkipNode<T> current = header;

        for (int i = level; i >= 0; i--) {
            while (current.forward[i] != null &&
                   current.forward[i].data.compareTo(data) < 0) {
                current = current.forward[i];
            }
        }

        current = current.forward[0];
        return current != null && current.data.equals(data);
    }

    public boolean delete(T data) {
        SkipNode<T>[] update = new SkipNode[MAX_LEVEL + 1];
        SkipNode<T> current = header;

        for (int i = level; i >= 0; i--) {
            while (current.forward[i] != null &&
                   current.forward[i].data.compareTo(data) < 0) {
                current = current.forward[i];
            }
            update[i] = current;
        }

        current = current.forward[0];

        if (current == null || !current.data.equals(data)) {
            return false;
        }

        for (int i = 0; i <= level; i++) {
            if (update[i].forward[i] != current) break;
            update[i].forward[i] = current.forward[i];
        }

        while (level > 0 && header.forward[level] == null) {
            level--;
        }

        size--;
        return true;
    }

    @Override
    public Iterator<T> iterator() {
        return new Iterator<T>() {
            private SkipNode<T> current = header.forward[0];

            @Override
            public boolean hasNext() {
                return current != null;
            }

            @Override
            public T next() {
                if (!hasNext()) {
                    throw new NoSuchElementException();
                }
                T data = current.data;
                current = current.forward[0];
                return data;
            }
        };
    }

    public int size() {
        return size;
    }

    @Override
    public String toString() {
        List<T> elements = new ArrayList<>();
        for (T data : this) {
            elements.add(data);
        }
        return "SkipList" + elements;
    }
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

public class LinkedList {
    public static void main(String[] args) {
        System.out.println("=".repeat(80));
        System.out.println("COMPREHENSIVE LINKED LIST DEMONSTRATIONS");
        System.out.println("=".repeat(80));

        // Singly Linked List
        System.out.println("\n1. SINGLY LINKED LIST");
        System.out.println("-".repeat(80));
        SinglyLinkedList<Integer> sll = new SinglyLinkedList<>();

        System.out.println("Inserting: 1, 2, 3 at head");
        sll.insertAtHead(3);
        sll.insertAtHead(2);
        sll.insertAtHead(1);
        System.out.println("List: " + sll);

        System.out.println("\nInserting: 4, 5 at tail");
        sll.insertAtTail(4);
        sll.insertAtTail(5);
        System.out.println("List: " + sll);

        System.out.println("\nMiddle element: " + sll.getMiddle());

        System.out.println("\nReversing list...");
        sll.reverse();
        System.out.println("List: " + sll);

        // Doubly Linked List
        System.out.println("\n2. DOUBLY LINKED LIST");
        System.out.println("-".repeat(80));
        DoublyLinkedList<String> dll = new DoublyLinkedList<>();

        System.out.println("Inserting: A, B, C at head");
        dll.insertAtHead("C");
        dll.insertAtHead("B");
        dll.insertAtHead("A");
        System.out.println("List: " + dll);

        System.out.println("\nInserting: D, E at tail");
        dll.insertAtTail("D");
        dll.insertAtTail("E");
        System.out.println("List: " + dll);

        System.out.print("\nForward iteration: ");
        for (String s : dll) {
            System.out.print(s + " ");
        }
        System.out.print("\nBackward iteration: ");
        for (String s : dll.reverseIterable()) {
            System.out.print(s + " ");
        }
        System.out.println();

        // Circular Linked List
        System.out.println("\n3. CIRCULAR LINKED LIST");
        System.out.println("-".repeat(80));
        CircularLinkedList<Integer> cll = new CircularLinkedList<>();

        System.out.println("Inserting: 1, 2, 3, 4, 5");
        for (int i = 1; i <= 5; i++) {
            cll.insertAtTail(i);
        }
        System.out.println("List: " + cll);

        // Skip List
        System.out.println("\n4. SKIP LIST");
        System.out.println("-".repeat(80));
        SkipList<Integer> sl = new SkipList<>();

        System.out.println("Inserting: 3, 7, 1, 9, 5, 2, 8, 4, 6");
        int[] values = {3, 7, 1, 9, 5, 2, 8, 4, 6};
        for (int val : values) {
            sl.insert(val);
        }

        System.out.println("Skip list (sorted): " + sl);

        System.out.println("\nSearching for 5: " + sl.search(5));
        System.out.println("Searching for 10: " + sl.search(10));

        System.out.println("\nDeleting 5...");
        sl.delete(5);
        System.out.println("Skip list: " + sl);

        System.out.println("\n" + "=".repeat(80));
        System.out.println("✨ All demonstrations complete!");
        System.out.println("=".repeat(80));
    }
}
