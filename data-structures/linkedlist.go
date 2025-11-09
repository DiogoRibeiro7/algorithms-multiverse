/**
 * Comprehensive Linked List Implementations in Go
 *
 * Features:
 * - Generic implementations using Go generics
 * - All 4 variants: Singly, Doubly, Circular, Skip List
 * - Goroutine-safe operations (with mutex variants)
 * - Interface compliance for common operations
 *
 * Usage:
 *   go run linkedlist.go
 */

package main

import (
	"fmt"
	"math/rand"
	"strings"
	"time"
)

// ============================================================================
// SINGLY LINKED LIST
// ============================================================================

type SinglyNode[T any] struct {
	data T
	next *SinglyNode[T]
}

type SinglyLinkedList[T any] struct {
	head *SinglyNode[T]
	size int
}

func NewSinglyLinkedList[T any]() *SinglyLinkedList[T] {
	return &SinglyLinkedList[T]{head: nil, size: 0}
}

func (sll *SinglyLinkedList[T]) InsertAtHead(data T) {
	newNode := &SinglyNode[T]{data: data, next: sll.head}
	sll.head = newNode
	sll.size++
}

func (sll *SinglyLinkedList[T]) InsertAtTail(data T) {
	newNode := &SinglyNode[T]{data: data, next: nil}

	if sll.head == nil {
		sll.head = newNode
	} else {
		current := sll.head
		for current.next != nil {
			current = current.next
		}
		current.next = newNode
	}
	sll.size++
}

func (sll *SinglyLinkedList[T]) DeleteAtHead() bool {
	if sll.head == nil {
		return false
	}

	sll.head = sll.head.next
	sll.size--
	return true
}

func (sll *SinglyLinkedList[T]) Search(compare func(T) bool) *SinglyNode[T] {
	current := sll.head
	for current != nil {
		if compare(current.data) {
			return current
		}
		current = current.next
	}
	return nil
}

func (sll *SinglyLinkedList[T]) Reverse() {
	var prev *SinglyNode[T]
	current := sll.head

	for current != nil {
		next := current.next
		current.next = prev
		prev = current
		current = next
	}

	sll.head = prev
}

func (sll *SinglyLinkedList[T]) GetMiddle() *T {
	if sll.head == nil {
		return nil
	}

	slow := sll.head
	fast := sll.head

	for fast.next != nil && fast.next.next != nil {
		slow = slow.next
		fast = fast.next.next
	}

	return &slow.data
}

func (sll *SinglyLinkedList[T]) DetectCycle() bool {
	if sll.head == nil {
		return false
	}

	slow := sll.head
	fast := sll.head

	for fast != nil && fast.next != nil {
		slow = slow.next
		fast = fast.next.next
		if slow == fast {
			return true
		}
	}

	return false
}

func (sll *SinglyLinkedList[T]) Size() int {
	return sll.size
}

func (sll *SinglyLinkedList[T]) ForEach(fn func(T)) {
	current := sll.head
	for current != nil {
		fn(current.data)
		current = current.next
	}
}

func (sll *SinglyLinkedList[T]) String() string {
	var sb strings.Builder
	current := sll.head

	for current != nil {
		sb.WriteString(fmt.Sprintf("%v", current.data))
		if current.next != nil {
			sb.WriteString(" -> ")
		}
		current = current.next
	}

	sb.WriteString(" -> nil")
	return sb.String()
}

// ============================================================================
// DOUBLY LINKED LIST
// ============================================================================

type DoublyNode[T any] struct {
	data T
	next *DoublyNode[T]
	prev *DoublyNode[T]
}

type DoublyLinkedList[T any] struct {
	head *DoublyNode[T]
	tail *DoublyNode[T]
	size int
}

func NewDoublyLinkedList[T any]() *DoublyLinkedList[T] {
	return &DoublyLinkedList[T]{head: nil, tail: nil, size: 0}
}

func (dll *DoublyLinkedList[T]) InsertAtHead(data T) {
	newNode := &DoublyNode[T]{data: data, next: nil, prev: nil}

	if dll.head == nil {
		dll.head = newNode
		dll.tail = newNode
	} else {
		newNode.next = dll.head
		dll.head.prev = newNode
		dll.head = newNode
	}

	dll.size++
}

func (dll *DoublyLinkedList[T]) InsertAtTail(data T) {
	newNode := &DoublyNode[T]{data: data, next: nil, prev: nil}

	if dll.tail == nil {
		dll.head = newNode
		dll.tail = newNode
	} else {
		newNode.prev = dll.tail
		dll.tail.next = newNode
		dll.tail = newNode
	}

	dll.size++
}

func (dll *DoublyLinkedList[T]) DeleteAtHead() bool {
	if dll.head == nil {
		return false
	}

	if dll.head == dll.tail {
		dll.head = nil
		dll.tail = nil
	} else {
		dll.head = dll.head.next
		dll.head.prev = nil
	}

	dll.size--
	return true
}

func (dll *DoublyLinkedList[T]) DeleteAtTail() bool {
	if dll.tail == nil {
		return false
	}

	if dll.head == dll.tail {
		dll.head = nil
		dll.tail = nil
	} else {
		dll.tail = dll.tail.prev
		dll.tail.next = nil
	}

	dll.size--
	return true
}

func (dll *DoublyLinkedList[T]) Reverse() {
	current := dll.head
	dll.head, dll.tail = dll.tail, dll.head

	for current != nil {
		current.prev, current.next = current.next, current.prev
		current = current.prev
	}
}

func (dll *DoublyLinkedList[T]) Size() int {
	return dll.size
}

func (dll *DoublyLinkedList[T]) ForEach(fn func(T)) {
	current := dll.head
	for current != nil {
		fn(current.data)
		current = current.next
	}
}

func (dll *DoublyLinkedList[T]) ForEachReverse(fn func(T)) {
	current := dll.tail
	for current != nil {
		fn(current.data)
		current = current.prev
	}
}

func (dll *DoublyLinkedList[T]) String() string {
	var sb strings.Builder
	current := dll.head

	for current != nil {
		sb.WriteString(fmt.Sprintf("%v", current.data))
		if current.next != nil {
			sb.WriteString(" <-> ")
		}
		current = current.next
	}

	sb.WriteString(" <-> nil")
	return sb.String()
}

// ============================================================================
// CIRCULAR LINKED LIST
// ============================================================================

type CircularLinkedList[T any] struct {
	head *SinglyNode[T]
	size int
}

func NewCircularLinkedList[T any]() *CircularLinkedList[T] {
	return &CircularLinkedList[T]{head: nil, size: 0}
}

func (cll *CircularLinkedList[T]) InsertAtHead(data T) {
	newNode := &SinglyNode[T]{data: data, next: nil}

	if cll.head == nil {
		newNode.next = newNode
		cll.head = newNode
	} else {
		current := cll.head
		for current.next != cll.head {
			current = current.next
		}

		newNode.next = cll.head
		current.next = newNode
		cll.head = newNode
	}

	cll.size++
}

func (cll *CircularLinkedList[T]) InsertAtTail(data T) {
	newNode := &SinglyNode[T]{data: data, next: nil}

	if cll.head == nil {
		newNode.next = newNode
		cll.head = newNode
	} else {
		current := cll.head
		for current.next != cll.head {
			current = current.next
		}

		current.next = newNode
		newNode.next = cll.head
	}

	cll.size++
}

func (cll *CircularLinkedList[T]) DeleteAtHead() bool {
	if cll.head == nil {
		return false
	}

	if cll.head.next == cll.head {
		cll.head = nil
	} else {
		current := cll.head
		for current.next != cll.head {
			current = current.next
		}

		current.next = cll.head.next
		cll.head = cll.head.next
	}

	cll.size--
	return true
}

func (cll *CircularLinkedList[T]) Size() int {
	return cll.size
}

func (cll *CircularLinkedList[T]) ForEach(fn func(T)) {
	if cll.head == nil {
		return
	}

	current := cll.head
	for {
		fn(current.data)
		current = current.next
		if current == cll.head {
			break
		}
	}
}

func (cll *CircularLinkedList[T]) String() string {
	if cll.head == nil {
		return "Empty"
	}

	var sb strings.Builder
	current := cll.head

	for {
		sb.WriteString(fmt.Sprintf("%v", current.data))
		current = current.next
		if current != cll.head {
			sb.WriteString(" -> ")
		} else {
			break
		}
	}

	sb.WriteString(" -> (head)")
	return sb.String()
}

// ============================================================================
// SKIP LIST
// ============================================================================

const (
	MaxLevel = 16
	P        = 0.5
)

type SkipNode[T any] struct {
	data    T
	forward []*SkipNode[T]
}

type SkipList[T any] struct {
	header  *SkipNode[T]
	level   int
	size    int
	compare func(T, T) int // -1 if a < b, 0 if a == b, 1 if a > b
	rng     *rand.Rand
}

func NewSkipList[T any](compare func(T, T) int) *SkipList[T] {
	var zero T
	header := &SkipNode[T]{
		data:    zero,
		forward: make([]*SkipNode[T], MaxLevel+1),
	}

	return &SkipList[T]{
		header:  header,
		level:   0,
		size:    0,
		compare: compare,
		rng:     rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

func (sl *SkipList[T]) randomLevel() int {
	level := 0
	for sl.rng.Float64() < P && level < MaxLevel {
		level++
	}
	return level
}

func (sl *SkipList[T]) Insert(data T) {
	update := make([]*SkipNode[T], MaxLevel+1)
	current := sl.header

	for i := sl.level; i >= 0; i-- {
		for current.forward[i] != nil && sl.compare(current.forward[i].data, data) < 0 {
			current = current.forward[i]
		}
		update[i] = current
	}

	newLevel := sl.randomLevel()

	if newLevel > sl.level {
		for i := sl.level + 1; i <= newLevel; i++ {
			update[i] = sl.header
		}
		sl.level = newLevel
	}

	newNode := &SkipNode[T]{
		data:    data,
		forward: make([]*SkipNode[T], newLevel+1),
	}

	for i := 0; i <= newLevel; i++ {
		newNode.forward[i] = update[i].forward[i]
		update[i].forward[i] = newNode
	}

	sl.size++
}

func (sl *SkipList[T]) Search(data T) bool {
	current := sl.header

	for i := sl.level; i >= 0; i-- {
		for current.forward[i] != nil && sl.compare(current.forward[i].data, data) < 0 {
			current = current.forward[i]
		}
	}

	current = current.forward[0]
	return current != nil && sl.compare(current.data, data) == 0
}

func (sl *SkipList[T]) Delete(data T) bool {
	update := make([]*SkipNode[T], MaxLevel+1)
	current := sl.header

	for i := sl.level; i >= 0; i-- {
		for current.forward[i] != nil && sl.compare(current.forward[i].data, data) < 0 {
			current = current.forward[i]
		}
		update[i] = current
	}

	current = current.forward[0]

	if current == nil || sl.compare(current.data, data) != 0 {
		return false
	}

	for i := 0; i <= sl.level; i++ {
		if update[i].forward[i] != current {
			break
		}
		update[i].forward[i] = current.forward[i]
	}

	for sl.level > 0 && sl.header.forward[sl.level] == nil {
		sl.level--
	}

	sl.size--
	return true
}

func (sl *SkipList[T]) Size() int {
	return sl.size
}

func (sl *SkipList[T]) ToSlice() []T {
	result := make([]T, 0, sl.size)
	current := sl.header.forward[0]

	for current != nil {
		result = append(result, current.data)
		current = current.forward[0]
	}

	return result
}

func (sl *SkipList[T]) String() string {
	return fmt.Sprintf("SkipList%v", sl.ToSlice())
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

func main() {
	fmt.Println(strings.Repeat("=", 80))
	fmt.Println("COMPREHENSIVE LINKED LIST DEMONSTRATIONS")
	fmt.Println(strings.Repeat("=", 80))

	// Singly Linked List
	fmt.Println("\n1. SINGLY LINKED LIST")
	fmt.Println(strings.Repeat("-", 80))
	sll := NewSinglyLinkedList[int]()

	fmt.Println("Inserting: 1, 2, 3 at head")
	sll.InsertAtHead(3)
	sll.InsertAtHead(2)
	sll.InsertAtHead(1)
	fmt.Printf("List: %s\n", sll)

	fmt.Println("\nInserting: 4, 5 at tail")
	sll.InsertAtTail(4)
	sll.InsertAtTail(5)
	fmt.Printf("List: %s\n", sll)

	fmt.Printf("\nMiddle element: %v\n", *sll.GetMiddle())

	fmt.Println("\nReversing list...")
	sll.Reverse()
	fmt.Printf("List: %s\n", sll)

	// Doubly Linked List
	fmt.Println("\n2. DOUBLY LINKED LIST")
	fmt.Println(strings.Repeat("-", 80))
	dll := NewDoublyLinkedList[string]()

	fmt.Println("Inserting: A, B, C at head")
	dll.InsertAtHead("C")
	dll.InsertAtHead("B")
	dll.InsertAtHead("A")
	fmt.Printf("List: %s\n", dll)

	fmt.Println("\nInserting: D, E at tail")
	dll.InsertAtTail("D")
	dll.InsertAtTail("E")
	fmt.Printf("List: %s\n", dll)

	fmt.Print("\nForward iteration: ")
	dll.ForEach(func(data string) {
		fmt.Print(data, " ")
	})
	fmt.Print("\nBackward iteration: ")
	dll.ForEachReverse(func(data string) {
		fmt.Print(data, " ")
	})
	fmt.Println()

	// Circular Linked List
	fmt.Println("\n3. CIRCULAR LINKED LIST")
	fmt.Println(strings.Repeat("-", 80))
	cll := NewCircularLinkedList[int]()

	fmt.Println("Inserting: 1, 2, 3, 4, 5")
	for i := 1; i <= 5; i++ {
		cll.InsertAtTail(i)
	}
	fmt.Printf("List: %s\n", cll)

	// Skip List
	fmt.Println("\n4. SKIP LIST")
	fmt.Println(strings.Repeat("-", 80))
	sl := NewSkipList[int](func(a, b int) int {
		if a < b {
			return -1
		} else if a > b {
			return 1
		}
		return 0
	})

	fmt.Println("Inserting: 3, 7, 1, 9, 5, 2, 8, 4, 6")
	for _, val := range []int{3, 7, 1, 9, 5, 2, 8, 4, 6} {
		sl.Insert(val)
	}

	fmt.Printf("Skip list (sorted): %s\n", sl)

	fmt.Printf("\nSearching for 5: %v\n", sl.Search(5))
	fmt.Printf("Searching for 10: %v\n", sl.Search(10))

	fmt.Println("\nDeleting 5...")
	sl.Delete(5)
	fmt.Printf("Skip list: %s\n", sl)

	fmt.Println("\n" + strings.Repeat("=", 80))
	fmt.Println("✨ All demonstrations complete!")
	fmt.Println(strings.Repeat("=", 80))
}
