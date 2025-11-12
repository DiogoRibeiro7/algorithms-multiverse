// Queue Data Structure Implementation in Go
//
// Time Complexity:
// - Enqueue: O(1)
// - Dequeue: O(1)
// - Peek: O(1)
// - Size: O(1)
// - IsEmpty: O(1)
// Space Complexity: O(n) where n is the number of elements
//
// A queue is a First-In-First-Out (FIFO) data structure where elements are
// added at the rear and removed from the front. Think of it like a line of people.
//
// Go features:
// - Generic implementation using type parameters (Go 1.18+)
// - Multiple implementations (slice-based, linked-list-based, circular)
// - Thread-safe implementation with mutex
// - Channel-based concurrent queue
// - Priority queue implementation
// - Circular queue with fixed capacity
// - Double-ended queue (deque)

package main

import (
	"errors"
	"fmt"
	"strings"
	"sync"
)

// QueueInterface defines the queue interface
type QueueInterface[T any] interface {
	Enqueue(item T)
	Dequeue() (T, error)
	Peek() (T, error)
	Size() int
	IsEmpty() bool
	Clear()
}

// Queue is a generic FIFO data structure (slice-based)
type Queue[T any] struct {
	items []T
}

// NewQueue creates a new empty queue
func NewQueue[T any]() *Queue[T] {
	return &Queue[T]{
		items: make([]T, 0),
	}
}

// NewQueueWithCapacity creates a new queue with pre-allocated capacity
func NewQueueWithCapacity[T any](capacity int) *Queue[T] {
	return &Queue[T]{
		items: make([]T, 0, capacity),
	}
}

// NewQueueFrom creates a new queue from a slice
func NewQueueFrom[T any](items []T) *Queue[T] {
	queue := &Queue[T]{
		items: make([]T, len(items)),
	}
	copy(queue.items, items)
	return queue
}

// Enqueue adds an element to the rear of the queue
//
// Time Complexity: O(1) amortized
func (q *Queue[T]) Enqueue(item T) {
	q.items = append(q.items, item)
}

// Dequeue removes and returns the front element
//
// Time Complexity: O(n) due to slice reallocation (can be optimized)
// Returns error if queue is empty
func (q *Queue[T]) Dequeue() (T, error) {
	var zero T
	if q.IsEmpty() {
		return zero, errors.New("dequeue from empty queue")
	}

	item := q.items[0]
	q.items = q.items[1:]
	return item, nil
}

// Peek returns the front element without removing it
//
// Time Complexity: O(1)
// Returns error if queue is empty
func (q *Queue[T]) Peek() (T, error) {
	var zero T
	if q.IsEmpty() {
		return zero, errors.New("peek on empty queue")
	}

	return q.items[0], nil
}

// Size returns the number of elements in the queue
//
// Time Complexity: O(1)
func (q *Queue[T]) Size() int {
	return len(q.items)
}

// IsEmpty checks if the queue is empty
//
// Time Complexity: O(1)
func (q *Queue[T]) IsEmpty() bool {
	return len(q.items) == 0
}

// Clear removes all elements from the queue
//
// Time Complexity: O(1)
func (q *Queue[T]) Clear() {
	q.items = make([]T, 0)
}

// ToSlice returns a copy of the queue as a slice (front to rear)
//
// Time Complexity: O(n)
func (q *Queue[T]) ToSlice() []T {
	result := make([]T, len(q.items))
	copy(result, q.items)
	return result
}

// String returns a string representation of the queue
func (q *Queue[T]) String() string {
	if q.IsEmpty() {
		return "Queue([])"
	}

	var sb strings.Builder
	sb.WriteString("Queue([")

	for i, item := range q.items {
		sb.WriteString(fmt.Sprintf("%v", item))
		if i < len(q.items)-1 {
			sb.WriteString(", ")
		}
	}

	sb.WriteString("])")
	return sb.String()
}

// LinkedQueue is a linked-list-based queue (O(1) dequeue)
type LinkedQueue[T any] struct {
	front *queueNode[T]
	rear  *queueNode[T]
	size  int
}

type queueNode[T any] struct {
	data T
	next *queueNode[T]
}

// NewLinkedQueue creates a new linked-list-based queue
func NewLinkedQueue[T any]() *LinkedQueue[T] {
	return &LinkedQueue[T]{
		front: nil,
		rear:  nil,
		size:  0,
	}
}

// Enqueue adds an element to the rear
//
// Time Complexity: O(1)
func (lq *LinkedQueue[T]) Enqueue(item T) {
	newNode := &queueNode[T]{data: item, next: nil}

	if lq.rear == nil {
		lq.front = newNode
		lq.rear = newNode
	} else {
		lq.rear.next = newNode
		lq.rear = newNode
	}

	lq.size++
}

// Dequeue removes and returns the front element
//
// Time Complexity: O(1)
func (lq *LinkedQueue[T]) Dequeue() (T, error) {
	var zero T
	if lq.IsEmpty() {
		return zero, errors.New("dequeue from empty queue")
	}

	item := lq.front.data
	lq.front = lq.front.next

	if lq.front == nil {
		lq.rear = nil
	}

	lq.size--
	return item, nil
}

// Peek returns the front element
//
// Time Complexity: O(1)
func (lq *LinkedQueue[T]) Peek() (T, error) {
	var zero T
	if lq.IsEmpty() {
		return zero, errors.New("peek on empty queue")
	}

	return lq.front.data, nil
}

// Size returns the number of elements
func (lq *LinkedQueue[T]) Size() int {
	return lq.size
}

// IsEmpty checks if the queue is empty
func (lq *LinkedQueue[T]) IsEmpty() bool {
	return lq.size == 0
}

// Clear removes all elements
func (lq *LinkedQueue[T]) Clear() {
	lq.front = nil
	lq.rear = nil
	lq.size = 0
}

// CircularQueue is a fixed-size circular queue
type CircularQueue[T any] struct {
	items    []T
	front    int
	rear     int
	size     int
	capacity int
}

// NewCircularQueue creates a new circular queue with fixed capacity
func NewCircularQueue[T any](capacity int) *CircularQueue[T] {
	return &CircularQueue[T]{
		items:    make([]T, capacity),
		front:    0,
		rear:     -1,
		size:     0,
		capacity: capacity,
	}
}

// Enqueue adds an element (returns error if full)
//
// Time Complexity: O(1)
func (cq *CircularQueue[T]) Enqueue(item T) error {
	if cq.IsFull() {
		return errors.New("queue is full")
	}

	cq.rear = (cq.rear + 1) % cq.capacity
	cq.items[cq.rear] = item
	cq.size++
	return nil
}

// Dequeue removes and returns the front element
//
// Time Complexity: O(1)
func (cq *CircularQueue[T]) Dequeue() (T, error) {
	var zero T
	if cq.IsEmpty() {
		return zero, errors.New("dequeue from empty queue")
	}

	item := cq.items[cq.front]
	cq.front = (cq.front + 1) % cq.capacity
	cq.size--
	return item, nil
}

// Peek returns the front element
func (cq *CircularQueue[T]) Peek() (T, error) {
	var zero T
	if cq.IsEmpty() {
		return zero, errors.New("peek on empty queue")
	}

	return cq.items[cq.front], nil
}

// Size returns the number of elements
func (cq *CircularQueue[T]) Size() int {
	return cq.size
}

// IsEmpty checks if the queue is empty
func (cq *CircularQueue[T]) IsEmpty() bool {
	return cq.size == 0
}

// IsFull checks if the queue is full
func (cq *CircularQueue[T]) IsFull() bool {
	return cq.size == cq.capacity
}

// Clear removes all elements
func (cq *CircularQueue[T]) Clear() {
	cq.front = 0
	cq.rear = -1
	cq.size = 0
}

// Deque (Double-Ended Queue) allows insertion/deletion at both ends
type Deque[T any] struct {
	items []T
}

// NewDeque creates a new deque
func NewDeque[T any]() *Deque[T] {
	return &Deque[T]{
		items: make([]T, 0),
	}
}

// PushFront adds an element to the front
//
// Time Complexity: O(n) due to slice reallocation
func (dq *Deque[T]) PushFront(item T) {
	dq.items = append([]T{item}, dq.items...)
}

// PushBack adds an element to the back
//
// Time Complexity: O(1) amortized
func (dq *Deque[T]) PushBack(item T) {
	dq.items = append(dq.items, item)
}

// PopFront removes and returns the front element
//
// Time Complexity: O(n)
func (dq *Deque[T]) PopFront() (T, error) {
	var zero T
	if dq.IsEmpty() {
		return zero, errors.New("popFront from empty deque")
	}

	item := dq.items[0]
	dq.items = dq.items[1:]
	return item, nil
}

// PopBack removes and returns the back element
//
// Time Complexity: O(1)
func (dq *Deque[T]) PopBack() (T, error) {
	var zero T
	if dq.IsEmpty() {
		return zero, errors.New("popBack from empty deque")
	}

	item := dq.items[len(dq.items)-1]
	dq.items = dq.items[:len(dq.items)-1]
	return item, nil
}

// PeekFront returns the front element
func (dq *Deque[T]) PeekFront() (T, error) {
	var zero T
	if dq.IsEmpty() {
		return zero, errors.New("peekFront on empty deque")
	}

	return dq.items[0], nil
}

// PeekBack returns the back element
func (dq *Deque[T]) PeekBack() (T, error) {
	var zero T
	if dq.IsEmpty() {
		return zero, errors.New("peekBack on empty deque")
	}

	return dq.items[len(dq.items)-1], nil
}

// Size returns the number of elements
func (dq *Deque[T]) Size() int {
	return len(dq.items)
}

// IsEmpty checks if the deque is empty
func (dq *Deque[T]) IsEmpty() bool {
	return len(dq.items) == 0
}

// ThreadSafeQueue is a thread-safe queue implementation
type ThreadSafeQueue[T any] struct {
	items []T
	mu    sync.RWMutex
}

// NewThreadSafeQueue creates a new thread-safe queue
func NewThreadSafeQueue[T any]() *ThreadSafeQueue[T] {
	return &ThreadSafeQueue[T]{
		items: make([]T, 0),
	}
}

// Enqueue adds an element (thread-safe)
func (tsq *ThreadSafeQueue[T]) Enqueue(item T) {
	tsq.mu.Lock()
	defer tsq.mu.Unlock()
	tsq.items = append(tsq.items, item)
}

// Dequeue removes and returns the front element (thread-safe)
func (tsq *ThreadSafeQueue[T]) Dequeue() (T, error) {
	tsq.mu.Lock()
	defer tsq.mu.Unlock()

	var zero T
	if len(tsq.items) == 0 {
		return zero, errors.New("dequeue from empty queue")
	}

	item := tsq.items[0]
	tsq.items = tsq.items[1:]
	return item, nil
}

// Size returns the number of elements (thread-safe)
func (tsq *ThreadSafeQueue[T]) Size() int {
	tsq.mu.RLock()
	defer tsq.mu.RUnlock()
	return len(tsq.items)
}

// IsEmpty checks if the queue is empty (thread-safe)
func (tsq *ThreadSafeQueue[T]) IsEmpty() bool {
	tsq.mu.RLock()
	defer tsq.mu.RUnlock()
	return len(tsq.items) == 0
}

// PriorityQueue is a priority queue implementation
type PriorityQueue[T any] struct {
	items []priorityItem[T]
	less  func(a, b T) bool
}

type priorityItem[T any] struct {
	value    T
	priority int
}

// NewPriorityQueue creates a new priority queue
func NewPriorityQueue[T any]() *PriorityQueue[T] {
	return &PriorityQueue[T]{
		items: make([]priorityItem[T], 0),
	}
}

// Enqueue adds an element with priority
//
// Time Complexity: O(n) - maintains sorted order
func (pq *PriorityQueue[T]) Enqueue(item T, priority int) {
	newItem := priorityItem[T]{value: item, priority: priority}

	// Insert in sorted order (higher priority first)
	inserted := false
	for i, existing := range pq.items {
		if priority > existing.priority {
			pq.items = append(pq.items[:i], append([]priorityItem[T]{newItem}, pq.items[i:]...)...)
			inserted = true
			break
		}
	}

	if !inserted {
		pq.items = append(pq.items, newItem)
	}
}

// Dequeue removes and returns the highest priority element
//
// Time Complexity: O(1)
func (pq *PriorityQueue[T]) Dequeue() (T, int, error) {
	var zero T
	if pq.IsEmpty() {
		return zero, 0, errors.New("dequeue from empty priority queue")
	}

	item := pq.items[0]
	pq.items = pq.items[1:]
	return item.value, item.priority, nil
}

// Peek returns the highest priority element
func (pq *PriorityQueue[T]) Peek() (T, int, error) {
	var zero T
	if pq.IsEmpty() {
		return zero, 0, errors.New("peek on empty priority queue")
	}

	return pq.items[0].value, pq.items[0].priority, nil
}

// Size returns the number of elements
func (pq *PriorityQueue[T]) Size() int {
	return len(pq.items)
}

// IsEmpty checks if the queue is empty
func (pq *PriorityQueue[T]) IsEmpty() bool {
	return len(pq.items) == 0
}

// Queue Applications

// BreadthFirstSearch demonstrates BFS using a queue
func BreadthFirstSearch(graph map[int][]int, start int) []int {
	visited := make(map[int]bool)
	result := make([]int, 0)
	queue := NewQueue[int]()

	queue.Enqueue(start)
	visited[start] = true

	for !queue.IsEmpty() {
		node, _ := queue.Dequeue()
		result = append(result, node)

		for _, neighbor := range graph[node] {
			if !visited[neighbor] {
				visited[neighbor] = true
				queue.Enqueue(neighbor)
			}
		}
	}

	return result
}

// HotPotato simulates the hot potato game
func HotPotato(names []string, num int) string {
	queue := NewQueueFrom(names)

	for queue.Size() > 1 {
		// Pass the potato num times
		for i := 0; i < num; i++ {
			name, _ := queue.Dequeue()
			queue.Enqueue(name)
		}

		// Remove the person holding the potato
		eliminated, _ := queue.Dequeue()
		fmt.Printf("%s is eliminated\n", eliminated)
	}

	winner, _ := queue.Peek()
	return winner
}

// DemonstrateQueue demonstrates queue operations
func DemonstrateQueue() {
	fmt.Println("🎯 Queue Data Structure Implementation in Go")
	fmt.Println(strings.Repeat("=", 70))

	// Basic queue operations
	fmt.Println("\n📋 Basic Queue Operations (Slice-based):")
	fmt.Println(strings.Repeat("-", 70))

	queue := NewQueue[int]()
	fmt.Printf("Created new queue: %s\n", queue)
	fmt.Printf("Is empty: %v\n", queue.IsEmpty())

	// Enqueue operations
	fmt.Println("\nEnqueuing elements: 10, 20, 30, 40, 50")
	for _, val := range []int{10, 20, 30, 40, 50} {
		queue.Enqueue(val)
		fmt.Printf("Enqueued %d, Queue: %s\n", val, queue)
	}

	// Peek operation
	if front, err := queue.Peek(); err == nil {
		fmt.Printf("\nFront element (peek): %d\n", front)
	}

	fmt.Printf("Size: %d\n", queue.Size())

	// Dequeue operations
	fmt.Println("\nDequeuing elements:")
	for !queue.IsEmpty() {
		val, _ := queue.Dequeue()
		fmt.Printf("Dequeued %d, Queue: %s\n", val, queue)
	}

	// Linked queue
	fmt.Println("\n🔗 Linked Queue (O(1) Dequeue):")
	fmt.Println(strings.Repeat("-", 70))

	linkedQueue := NewLinkedQueue[string]()
	words := []string{"First", "Second", "Third", "Fourth"}

	for _, word := range words {
		linkedQueue.Enqueue(word)
		fmt.Printf("Enqueued: %s, Size: %d\n", word, linkedQueue.Size())
	}

	fmt.Println("\nDequeuing:")
	for !linkedQueue.IsEmpty() {
		word, _ := linkedQueue.Dequeue()
		fmt.Printf("Dequeued: %s, Remaining: %d\n", word, linkedQueue.Size())
	}

	// Circular queue
	fmt.Println("\n⭕ Circular Queue (Fixed Capacity):")
	fmt.Println(strings.Repeat("-", 70))

	circQueue := NewCircularQueue[int](5)
	fmt.Printf("Created circular queue with capacity: 5\n")

	for i := 1; i <= 5; i++ {
		circQueue.Enqueue(i)
		fmt.Printf("Enqueued %d, Size: %d, Full: %v\n", i, circQueue.Size(), circQueue.IsFull())
	}

	// Try to enqueue when full
	err := circQueue.Enqueue(6)
	if err != nil {
		fmt.Printf("Error: %v ✓\n", err)
	}

	// Dequeue and enqueue
	val, _ := circQueue.Dequeue()
	fmt.Printf("Dequeued %d\n", val)
	circQueue.Enqueue(6)
	fmt.Printf("Enqueued 6 after dequeue\n")

	// Deque (Double-Ended Queue)
	fmt.Println("\n↔️  Deque (Double-Ended Queue):")
	fmt.Println(strings.Repeat("-", 70))

	deque := NewDeque[int]()

	fmt.Println("Operations:")
	deque.PushBack(1)
	fmt.Printf("PushBack(1): [%v]\n", deque.items)

	deque.PushBack(2)
	fmt.Printf("PushBack(2): [%v]\n", deque.items)

	deque.PushFront(0)
	fmt.Printf("PushFront(0): [%v]\n", deque.items)

	deque.PushFront(-1)
	fmt.Printf("PushFront(-1): [%v]\n", deque.items)

	front, _ := deque.PopFront()
	fmt.Printf("PopFront(): %d, Remaining: [%v]\n", front, deque.items)

	back, _ := deque.PopBack()
	fmt.Printf("PopBack(): %d, Remaining: [%v]\n", back, deque.items)

	// Priority queue
	fmt.Println("\n⭐ Priority Queue:")
	fmt.Println(strings.Repeat("-", 70))

	pq := NewPriorityQueue[string]()

	tasks := []struct {
		name     string
		priority int
	}{
		{"Low priority task", 1},
		{"High priority task", 5},
		{"Medium priority task", 3},
		{"Critical task", 10},
		{"Normal task", 2},
	}

	for _, task := range tasks {
		pq.Enqueue(task.name, task.priority)
		fmt.Printf("Enqueued: %s (priority %d)\n", task.name, task.priority)
	}

	fmt.Println("\nProcessing tasks by priority:")
	for !pq.IsEmpty() {
		task, priority, _ := pq.Dequeue()
		fmt.Printf("Priority %d: %s\n", priority, task)
	}

	// BFS demonstration
	fmt.Println("\n🔍 Breadth-First Search:")
	fmt.Println(strings.Repeat("-", 70))

	graph := map[int][]int{
		0: {1, 2},
		1: {0, 3, 4},
		2: {0, 5, 6},
		3: {1},
		4: {1},
		5: {2},
		6: {2},
	}

	bfsResult := BreadthFirstSearch(graph, 0)
	fmt.Printf("BFS traversal from node 0: %v\n", bfsResult)

	// Hot Potato game
	fmt.Println("\n🔥 Hot Potato Game:")
	fmt.Println(strings.Repeat("-", 70))

	players := []string{"Alice", "Bob", "Charlie", "David", "Eve"}
	fmt.Printf("Players: %v\n", players)
	fmt.Printf("Passing the potato 3 times each round\n\n")

	winner := HotPotato(players, 3)
	fmt.Printf("\nWinner: %s 🎉\n", winner)

	// Thread-safe queue
	fmt.Println("\n🔒 Thread-Safe Queue:")
	fmt.Println(strings.Repeat("-", 70))

	tsQueue := NewThreadSafeQueue[int]()

	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(val int) {
			defer wg.Done()
			tsQueue.Enqueue(val)
		}(i)
	}

	wg.Wait()
	fmt.Printf("Enqueued 10 elements concurrently, Size: %d\n", tsQueue.Size())

	fmt.Println("Dequeuing:")
	for i := 0; i < 5; i++ {
		val, _ := tsQueue.Dequeue()
		fmt.Printf("Dequeued: %d\n", val)
	}
}

func main() {
	DemonstrateQueue()
	fmt.Println("\n✨ Queue demonstration complete!")
}
