/**
 * Comprehensive Linked List Implementations in C++
 *
 * Features:
 * - Template-based generic implementations
 * - RAII and smart pointers for memory safety
 * - STL-compliant iterators
 * - Move semantics for efficiency
 * - All 4 variants: Singly, Doubly, Circular, Skip List
 *
 * Compilation:
 *   g++ -std=c++17 -O2 -o linkedlist linkedlist.cpp
 *   ./linkedlist
 */

#include <iostream>
#include <memory>
#include <random>
#include <vector>
#include <stdexcept>
#include <iterator>

// ============================================================================
// SINGLY LINKED LIST
// ============================================================================

template<typename T>
class SinglyLinkedList {
private:
    struct Node {
        T data;
        std::unique_ptr<Node> next;

        Node(const T& value) : data(value), next(nullptr) {}
        Node(T&& value) : data(std::move(value)), next(nullptr) {}
    };

    std::unique_ptr<Node> head;
    size_t list_size;

public:
    SinglyLinkedList() : head(nullptr), list_size(0) {}

    // Iterator
    class Iterator {
    private:
        Node* current;

    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        using pointer = T*;
        using reference = T&;

        Iterator(Node* node) : current(node) {}

        reference operator*() const { return current->data; }
        pointer operator->() const { return &current->data; }

        Iterator& operator++() {
            if (current) current = current->next.get();
            return *this;
        }

        Iterator operator++(int) {
            Iterator tmp = *this;
            ++(*this);
            return tmp;
        }

        bool operator==(const Iterator& other) const {
            return current == other.current;
        }

        bool operator!=(const Iterator& other) const {
            return !(*this == other);
        }
    };

    Iterator begin() { return Iterator(head.get()); }
    Iterator end() { return Iterator(nullptr); }

    void insertAtHead(const T& value) {
        auto newNode = std::make_unique<Node>(value);
        newNode->next = std::move(head);
        head = std::move(newNode);
        ++list_size;
    }

    void insertAtHead(T&& value) {
        auto newNode = std::make_unique<Node>(std::move(value));
        newNode->next = std::move(head);
        head = std::move(newNode);
        ++list_size;
    }

    void insertAtTail(const T& value) {
        auto newNode = std::make_unique<Node>(value);

        if (!head) {
            head = std::move(newNode);
        } else {
            Node* current = head.get();
            while (current->next) {
                current = current->next.get();
            }
            current->next = std::move(newNode);
        }
        ++list_size;
    }

    bool deleteAtHead() {
        if (!head) return false;

        head = std::move(head->next);
        --list_size;
        return true;
    }

    bool search(const T& value) const {
        Node* current = head.get();
        while (current) {
            if (current->data == value) return true;
            current = current->next.get();
        }
        return false;
    }

    void reverse() {
        std::unique_ptr<Node> prev = nullptr;
        std::unique_ptr<Node> current = std::move(head);

        while (current) {
            std::unique_ptr<Node> next = std::move(current->next);
            current->next = std::move(prev);
            prev = std::move(current);
            current = std::move(next);
        }

        head = std::move(prev);
    }

    T getMiddle() const {
        if (!head) throw std::runtime_error("Empty list");

        Node* slow = head.get();
        Node* fast = head.get();

        while (fast->next && fast->next->next) {
            slow = slow->next.get();
            fast = fast->next->next.get();
        }

        return slow->data;
    }

    size_t size() const { return list_size; }
    bool empty() const { return head == nullptr; }

    friend std::ostream& operator<<(std::ostream& os, const SinglyLinkedList& list) {
        Node* current = list.head.get();
        while (current) {
            os << current->data;
            if (current->next) os << " -> ";
            current = current->next.get();
        }
        os << " -> null";
        return os;
    }
};

// ============================================================================
// DOUBLY LINKED LIST
// ============================================================================

template<typename T>
class DoublyLinkedList {
private:
    struct Node {
        T data;
        std::unique_ptr<Node> next;
        Node* prev;

        Node(const T& value) : data(value), next(nullptr), prev(nullptr) {}
        Node(T&& value) : data(std::move(value)), next(nullptr), prev(nullptr) {}
    };

    std::unique_ptr<Node> head;
    Node* tail;
    size_t list_size;

public:
    DoublyLinkedList() : head(nullptr), tail(nullptr), list_size(0) {}

    class Iterator {
    private:
        Node* current;

    public:
        using iterator_category = std::bidirectional_iterator_tag;
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        using pointer = T*;
        using reference = T&;

        Iterator(Node* node) : current(node) {}

        reference operator*() const { return current->data; }
        pointer operator->() const { return &current->data; }

        Iterator& operator++() {
            if (current) current = current->next.get();
            return *this;
        }

        Iterator& operator--() {
            if (current) current = current->prev;
            return *this;
        }

        bool operator==(const Iterator& other) const {
            return current == other.current;
        }

        bool operator!=(const Iterator& other) const {
            return !(*this == other);
        }
    };

    Iterator begin() { return Iterator(head.get()); }
    Iterator end() { return Iterator(nullptr); }

    void insertAtHead(const T& value) {
        auto newNode = std::make_unique<Node>(value);

        if (!head) {
            tail = newNode.get();
            head = std::move(newNode);
        } else {
            newNode->next = std::move(head);
            newNode->next->prev = newNode.get();
            head = std::move(newNode);
        }
        ++list_size;
    }

    void insertAtTail(const T& value) {
        auto newNode = std::make_unique<Node>(value);

        if (!tail) {
            head = std::move(newNode);
            tail = head.get();
        } else {
            newNode->prev = tail;
            tail->next = std::move(newNode);
            tail = tail->next.get();
        }
        ++list_size;
    }

    bool deleteAtHead() {
        if (!head) return false;

        if (head.get() == tail) {
            head = nullptr;
            tail = nullptr;
        } else {
            head = std::move(head->next);
            head->prev = nullptr;
        }
        --list_size;
        return true;
    }

    bool deleteAtTail() {
        if (!tail) return false;

        if (head.get() == tail) {
            head = nullptr;
            tail = nullptr;
        } else {
            tail = tail->prev;
            tail->next = nullptr;
        }
        --list_size;
        return true;
    }

    void reverse() {
        if (!head) return;

        Node* current = head.get();
        std::unique_ptr<Node> temp;

        std::swap(head.get(), tail);

        while (current) {
            // Swap next and prev
            Node* prev = current->prev;
            current->prev = current->next.get();

            if (current->next) {
                temp = std::move(current->next);
                current->next = std::move(temp);
            }

            if (prev) {
                current = prev;
            } else {
                break;
            }
        }
    }

    size_t size() const { return list_size; }
    bool empty() const { return head == nullptr; }

    friend std::ostream& operator<<(std::ostream& os, const DoublyLinkedList& list) {
        Node* current = list.head.get();
        while (current) {
            os << current->data;
            if (current->next) os << " <-> ";
            current = current->next.get();
        }
        os << " <-> null";
        return os;
    }
};

// ============================================================================
// CIRCULAR LINKED LIST
// ============================================================================

template<typename T>
class CircularLinkedList {
private:
    struct Node {
        T data;
        std::shared_ptr<Node> next;

        Node(const T& value) : data(value), next(nullptr) {}
    };

    std::shared_ptr<Node> head;
    size_t list_size;

public:
    CircularLinkedList() : head(nullptr), list_size(0) {}

    void insertAtHead(const T& value) {
        auto newNode = std::make_shared<Node>(value);

        if (!head) {
            newNode->next = newNode;
            head = newNode;
        } else {
            auto current = head;
            while (current->next != head) {
                current = current->next;
            }
            newNode->next = head;
            current->next = newNode;
            head = newNode;
        }
        ++list_size;
    }

    void insertAtTail(const T& value) {
        auto newNode = std::make_shared<Node>(value);

        if (!head) {
            newNode->next = newNode;
            head = newNode;
        } else {
            auto current = head;
            while (current->next != head) {
                current = current->next;
            }
            current->next = newNode;
            newNode->next = head;
        }
        ++list_size;
    }

    bool deleteAtHead() {
        if (!head) return false;

        if (head->next == head) {
            head = nullptr;
        } else {
            auto current = head;
            while (current->next != head) {
                current = current->next;
            }
            current->next = head->next;
            head = head->next;
        }
        --list_size;
        return true;
    }

    size_t size() const { return list_size; }
    bool empty() const { return head == nullptr; }

    friend std::ostream& operator<<(std::ostream& os, const CircularLinkedList& list) {
        if (!list.head) {
            os << "Empty";
            return os;
        }

        auto current = list.head;
        do {
            os << current->data;
            current = current->next;
            if (current != list.head) os << " -> ";
        } while (current != list.head);
        os << " -> (head)";
        return os;
    }
};

// ============================================================================
// SKIP LIST
// ============================================================================

template<typename T>
class SkipList {
private:
    static constexpr int MAX_LEVEL = 16;
    static constexpr double P = 0.5;

    struct Node {
        T data;
        std::vector<std::shared_ptr<Node>> forward;

        Node(const T& value, int level)
            : data(value), forward(level + 1, nullptr) {}
    };

    std::shared_ptr<Node> header;
    int level;
    size_t list_size;
    std::mt19937 rng;
    std::uniform_real_distribution<double> dist;

    int randomLevel() {
        int lvl = 0;
        while (dist(rng) < P && lvl < MAX_LEVEL) {
            ++lvl;
        }
        return lvl;
    }

public:
    SkipList() : header(std::make_shared<Node>(T(), MAX_LEVEL)),
                 level(0), list_size(0), rng(std::random_device{}()), dist(0.0, 1.0) {}

    void insert(const T& value) {
        std::vector<std::shared_ptr<Node>> update(MAX_LEVEL + 1);
        auto current = header;

        for (int i = level; i >= 0; --i) {
            while (current->forward[i] && current->forward[i]->data < value) {
                current = current->forward[i];
            }
            update[i] = current;
        }

        int newLevel = randomLevel();

        if (newLevel > level) {
            for (int i = level + 1; i <= newLevel; ++i) {
                update[i] = header;
            }
            level = newLevel;
        }

        auto newNode = std::make_shared<Node>(value, newLevel);

        for (int i = 0; i <= newLevel; ++i) {
            newNode->forward[i] = update[i]->forward[i];
            update[i]->forward[i] = newNode;
        }

        ++list_size;
    }

    bool search(const T& value) const {
        auto current = header;

        for (int i = level; i >= 0; --i) {
            while (current->forward[i] && current->forward[i]->data < value) {
                current = current->forward[i];
            }
        }

        current = current->forward[0];
        return current && current->data == value;
    }

    bool remove(const T& value) {
        std::vector<std::shared_ptr<Node>> update(MAX_LEVEL + 1);
        auto current = header;

        for (int i = level; i >= 0; --i) {
            while (current->forward[i] && current->forward[i]->data < value) {
                current = current->forward[i];
            }
            update[i] = current;
        }

        current = current->forward[0];

        if (!current || current->data != value) {
            return false;
        }

        for (int i = 0; i <= level; ++i) {
            if (update[i]->forward[i] != current) break;
            update[i]->forward[i] = current->forward[i];
        }

        while (level > 0 && !header->forward[level]) {
            --level;
        }

        --list_size;
        return true;
    }

    size_t size() const { return list_size; }
    bool empty() const { return list_size == 0; }

    std::vector<T> toVector() const {
        std::vector<T> result;
        auto current = header->forward[0];
        while (current) {
            result.push_back(current->data);
            current = current->forward[0];
        }
        return result;
    }

    friend std::ostream& operator<<(std::ostream& os, const SkipList& list) {
        os << "SkipList[";
        auto vec = list.toVector();
        for (size_t i = 0; i < vec.size(); ++i) {
            os << vec[i];
            if (i < vec.size() - 1) os << ", ";
        }
        os << "]";
        return os;
    }
};

// ============================================================================
// DEMONSTRATION
// ============================================================================

int main() {
    std::cout << std::string(80, '=') << "\n";
    std::cout << "COMPREHENSIVE LINKED LIST DEMONSTRATIONS\n";
    std::cout << std::string(80, '=') << "\n";

    // Singly Linked List
    std::cout << "\n1. SINGLY LINKED LIST\n";
    std::cout << std::string(80, '-') << "\n";
    SinglyLinkedList<int> sll;

    std::cout << "Inserting: 1, 2, 3 at head\n";
    sll.insertAtHead(3);
    sll.insertAtHead(2);
    sll.insertAtHead(1);
    std::cout << "List: " << sll << "\n";

    std::cout << "\nInserting: 4, 5 at tail\n";
    sll.insertAtTail(4);
    sll.insertAtTail(5);
    std::cout << "List: " << sll << "\n";

    std::cout << "\nMiddle element: " << sll.getMiddle() << "\n";

    std::cout << "\nReversing list...\n";
    sll.reverse();
    std::cout << "List: " << sll << "\n";

    // Doubly Linked List
    std::cout << "\n2. DOUBLY LINKED LIST\n";
    std::cout << std::string(80, '-') << "\n";
    DoublyLinkedList<std::string> dll;

    std::cout << "Inserting: A, B, C at head\n";
    dll.insertAtHead("C");
    dll.insertAtHead("B");
    dll.insertAtHead("A");
    std::cout << "List: " << dll << "\n";

    std::cout << "\nInserting: D, E at tail\n";
    dll.insertAtTail("D");
    dll.insertAtTail("E");
    std::cout << "List: " << dll << "\n";

    std::cout << "\nDeleting head and tail...\n";
    dll.deleteAtHead();
    dll.deleteAtTail();
    std::cout << "List: " << dll << "\n";

    // Circular Linked List
    std::cout << "\n3. CIRCULAR LINKED LIST\n";
    std::cout << std::string(80, '-') << "\n";
    CircularLinkedList<int> cll;

    std::cout << "Inserting: 1, 2, 3, 4, 5\n";
    for (int i = 1; i <= 5; ++i) {
        cll.insertAtTail(i);
    }
    std::cout << "List: " << cll << "\n";

    // Skip List
    std::cout << "\n4. SKIP LIST\n";
    std::cout << std::string(80, '-') << "\n";
    SkipList<int> sl;

    std::cout << "Inserting: 3, 7, 1, 9, 5, 2, 8, 4, 6\n";
    for (int val : {3, 7, 1, 9, 5, 2, 8, 4, 6}) {
        sl.insert(val);
    }

    std::cout << "Skip list (sorted): " << sl << "\n";

    std::cout << "\nSearching for 5: " << (sl.search(5) ? "found" : "not found") << "\n";
    std::cout << "Searching for 10: " << (sl.search(10) ? "found" : "not found") << "\n";

    std::cout << "\nDeleting 5...\n";
    sl.remove(5);
    std::cout << "Skip list: " << sl << "\n";

    std::cout << "\n" << std::string(80, '=') << "\n";
    std::cout << "✨ All demonstrations complete!\n";
    std::cout << std::string(80, '=') << "\n";

    return 0;
}
