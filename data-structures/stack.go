// Stack Data Structure Implementation in Go
//
// Time Complexity:
// - Push: O(1)
// - Pop: O(1)
// - Peek: O(1)
// - Size: O(1)
// - IsEmpty: O(1)
// Space Complexity: O(n) where n is the number of elements
//
// A stack is a Last-In-First-Out (LIFO) data structure where elements are
// added and removed from the same end (top). Think of it like a stack of plates.
//
// Go features:
// - Generic implementation using type parameters (Go 1.18+)
// - Interface-based design for flexibility
// - Thread-safe implementation with mutex
// - Iterator pattern for traversal
// - Channel-based concurrent stack
// - Memory-efficient implementation

package main

import (
	"errors"
	"fmt"
	"strings"
	"sync"
)

// StackInterface defines the stack interface
type StackInterface[T any] interface {
	Push(item T)
	Pop() (T, error)
	Peek() (T, error)
	Size() int
	IsEmpty() bool
	Clear()
	ToSlice() []T
}

// Stack is a generic LIFO data structure
type Stack[T any] struct {
	items []T
}

// NewStack creates a new empty stack
func NewStack[T any]() *Stack[T] {
	return &Stack[T]{
		items: make([]T, 0),
	}
}

// NewStackWithCapacity creates a new stack with pre-allocated capacity
func NewStackWithCapacity[T any](capacity int) *Stack[T] {
	return &Stack[T]{
		items: make([]T, 0, capacity),
	}
}

// NewStackFrom creates a new stack from a slice
func NewStackFrom[T any](items []T) *Stack[T] {
	stack := &Stack[T]{
		items: make([]T, len(items)),
	}
	copy(stack.items, items)
	return stack
}

// Push adds an element to the top of the stack
//
// Time Complexity: O(1) amortized
func (s *Stack[T]) Push(item T) {
	s.items = append(s.items, item)
}

// Pop removes and returns the top element
//
// Time Complexity: O(1)
// Returns error if stack is empty
func (s *Stack[T]) Pop() (T, error) {
	var zero T
	if s.IsEmpty() {
		return zero, errors.New("pop from empty stack")
	}

	index := len(s.items) - 1
	item := s.items[index]
	s.items = s.items[:index]
	return item, nil
}

// Peek returns the top element without removing it
//
// Time Complexity: O(1)
// Returns error if stack is empty
func (s *Stack[T]) Peek() (T, error) {
	var zero T
	if s.IsEmpty() {
		return zero, errors.New("peek on empty stack")
	}

	return s.items[len(s.items)-1], nil
}

// Size returns the number of elements in the stack
//
// Time Complexity: O(1)
func (s *Stack[T]) Size() int {
	return len(s.items)
}

// IsEmpty checks if the stack is empty
//
// Time Complexity: O(1)
func (s *Stack[T]) IsEmpty() bool {
	return len(s.items) == 0
}

// Clear removes all elements from the stack
//
// Time Complexity: O(1)
func (s *Stack[T]) Clear() {
	s.items = make([]T, 0)
}

// ToSlice returns a copy of the stack as a slice (top to bottom)
//
// Time Complexity: O(n)
func (s *Stack[T]) ToSlice() []T {
	result := make([]T, len(s.items))
	for i := 0; i < len(s.items); i++ {
		result[i] = s.items[len(s.items)-1-i]
	}
	return result
}

// Contains checks if the stack contains an element
//
// Time Complexity: O(n)
func (s *Stack[T]) Contains(item T, equals func(a, b T) bool) bool {
	for _, element := range s.items {
		if equals(element, item) {
			return true
		}
	}
	return false
}

// Clone creates a deep copy of the stack
//
// Time Complexity: O(n)
func (s *Stack[T]) Clone() *Stack[T] {
	newStack := NewStack[T]()
	newStack.items = make([]T, len(s.items))
	copy(newStack.items, s.items)
	return newStack
}

// Reverse reverses the order of elements in the stack
//
// Time Complexity: O(n)
func (s *Stack[T]) Reverse() {
	for i, j := 0, len(s.items)-1; i < j; i, j = i+1, j-1 {
		s.items[i], s.items[j] = s.items[j], s.items[i]
	}
}

// String returns a string representation of the stack
func (s *Stack[T]) String() string {
	if s.IsEmpty() {
		return "Stack([])"
	}

	var sb strings.Builder
	sb.WriteString("Stack([")

	for i := len(s.items) - 1; i >= 0; i-- {
		sb.WriteString(fmt.Sprintf("%v", s.items[i]))
		if i > 0 {
			sb.WriteString(", ")
		}
	}

	sb.WriteString("])")
	return sb.String()
}

// ForEach applies a function to each element (top to bottom)
//
// Time Complexity: O(n)
func (s *Stack[T]) ForEach(fn func(item T)) {
	for i := len(s.items) - 1; i >= 0; i-- {
		fn(s.items[i])
	}
}

// Filter returns a new stack containing only elements that satisfy the predicate
//
// Time Complexity: O(n)
func (s *Stack[T]) Filter(predicate func(item T) bool) *Stack[T] {
	newStack := NewStack[T]()
	for _, item := range s.items {
		if predicate(item) {
			newStack.Push(item)
		}
	}
	return newStack
}

// Map applies a transformation function to each element
//
// Time Complexity: O(n)
func (s *Stack[T]) Map(transform func(item T) T) *Stack[T] {
	newStack := NewStack[T]()
	for _, item := range s.items {
		newStack.Push(transform(item))
	}
	return newStack
}

// ThreadSafeStack is a thread-safe stack implementation
type ThreadSafeStack[T any] struct {
	items []T
	mu    sync.RWMutex
}

// NewThreadSafeStack creates a new thread-safe stack
func NewThreadSafeStack[T any]() *ThreadSafeStack[T] {
	return &ThreadSafeStack[T]{
		items: make([]T, 0),
	}
}

// Push adds an element to the stack (thread-safe)
func (ts *ThreadSafeStack[T]) Push(item T) {
	ts.mu.Lock()
	defer ts.mu.Unlock()
	ts.items = append(ts.items, item)
}

// Pop removes and returns the top element (thread-safe)
func (ts *ThreadSafeStack[T]) Pop() (T, error) {
	ts.mu.Lock()
	defer ts.mu.Unlock()

	var zero T
	if len(ts.items) == 0 {
		return zero, errors.New("pop from empty stack")
	}

	index := len(ts.items) - 1
	item := ts.items[index]
	ts.items = ts.items[:index]
	return item, nil
}

// Peek returns the top element without removing it (thread-safe)
func (ts *ThreadSafeStack[T]) Peek() (T, error) {
	ts.mu.RLock()
	defer ts.mu.RUnlock()

	var zero T
	if len(ts.items) == 0 {
		return zero, errors.New("peek on empty stack")
	}

	return ts.items[len(ts.items)-1], nil
}

// Size returns the number of elements (thread-safe)
func (ts *ThreadSafeStack[T]) Size() int {
	ts.mu.RLock()
	defer ts.mu.RUnlock()
	return len(ts.items)
}

// IsEmpty checks if the stack is empty (thread-safe)
func (ts *ThreadSafeStack[T]) IsEmpty() bool {
	ts.mu.RLock()
	defer ts.mu.RUnlock()
	return len(ts.items) == 0
}

// Clear removes all elements (thread-safe)
func (ts *ThreadSafeStack[T]) Clear() {
	ts.mu.Lock()
	defer ts.mu.Unlock()
	ts.items = make([]T, 0)
}

// ChannelStack is a stack implementation using channels for concurrency
type ChannelStack[T any] struct {
	pushCh chan T
	popCh  chan T
	peekCh chan T
	sizeCh chan int
	quitCh chan struct{}
}

// NewChannelStack creates a new channel-based stack
func NewChannelStack[T any](bufferSize int) *ChannelStack[T] {
	cs := &ChannelStack[T]{
		pushCh: make(chan T, bufferSize),
		popCh:  make(chan T),
		peekCh: make(chan T),
		sizeCh: make(chan int),
		quitCh: make(chan struct{}),
	}

	go cs.run()
	return cs
}

// run is the goroutine that manages the stack operations
func (cs *ChannelStack[T]) run() {
	items := make([]T, 0)

	for {
		select {
		case item := <-cs.pushCh:
			items = append(items, item)

		case cs.popCh <- func() T {
			if len(items) == 0 {
				var zero T
				return zero
			}
			item := items[len(items)-1]
			items = items[:len(items)-1]
			return item
		}():

		case cs.peekCh <- func() T {
			if len(items) == 0 {
				var zero T
				return zero
			}
			return items[len(items)-1]
		}():

		case cs.sizeCh <- len(items):

		case <-cs.quitCh:
			return
		}
	}
}

// Push adds an element to the stack
func (cs *ChannelStack[T]) Push(item T) {
	cs.pushCh <- item
}

// Pop removes and returns the top element
func (cs *ChannelStack[T]) Pop() T {
	return <-cs.popCh
}

// Peek returns the top element without removing it
func (cs *ChannelStack[T]) Peek() T {
	return <-cs.peekCh
}

// Size returns the number of elements
func (cs *ChannelStack[T]) Size() int {
	return <-cs.sizeCh
}

// Close closes the channel stack
func (cs *ChannelStack[T]) Close() {
	close(cs.quitCh)
}

// MinStack maintains both elements and minimum values
type MinStack[T any] struct {
	items   []T
	minVals []T
	less    func(a, b T) bool
}

// NewMinStack creates a new MinStack that tracks minimum value
func NewMinStack[T any](less func(a, b T) bool) *MinStack[T] {
	return &MinStack[T]{
		items:   make([]T, 0),
		minVals: make([]T, 0),
		less:    less,
	}
}

// Push adds an element and updates minimum
func (ms *MinStack[T]) Push(item T) {
	ms.items = append(ms.items, item)

	if len(ms.minVals) == 0 || ms.less(item, ms.minVals[len(ms.minVals)-1]) {
		ms.minVals = append(ms.minVals, item)
	} else {
		ms.minVals = append(ms.minVals, ms.minVals[len(ms.minVals)-1])
	}
}

// Pop removes the top element
func (ms *MinStack[T]) Pop() (T, error) {
	var zero T
	if len(ms.items) == 0 {
		return zero, errors.New("pop from empty stack")
	}

	item := ms.items[len(ms.items)-1]
	ms.items = ms.items[:len(ms.items)-1]
	ms.minVals = ms.minVals[:len(ms.minVals)-1]
	return item, nil
}

// GetMin returns the current minimum value in O(1) time
func (ms *MinStack[T]) GetMin() (T, error) {
	var zero T
	if len(ms.minVals) == 0 {
		return zero, errors.New("getMin on empty stack")
	}
	return ms.minVals[len(ms.minVals)-1], nil
}

// Size returns the number of elements
func (ms *MinStack[T]) Size() int {
	return len(ms.items)
}

// IsEmpty checks if the stack is empty
func (ms *MinStack[T]) IsEmpty() bool {
	return len(ms.items) == 0
}

// Stack Applications and Utilities

// BalancedParentheses checks if parentheses are balanced
func BalancedParentheses(s string) bool {
	stack := NewStack[rune]()
	pairs := map[rune]rune{
		')': '(',
		']': '[',
		'}': '{',
	}

	for _, char := range s {
		switch char {
		case '(', '[', '{':
			stack.Push(char)
		case ')', ']', '}':
			if stack.IsEmpty() {
				return false
			}
			top, _ := stack.Pop()
			if top != pairs[char] {
				return false
			}
		}
	}

	return stack.IsEmpty()
}

// EvaluatePostfix evaluates a postfix expression
func EvaluatePostfix(expression []string) (int, error) {
	stack := NewStack[int]()

	for _, token := range expression {
		switch token {
		case "+", "-", "*", "/":
			if stack.Size() < 2 {
				return 0, errors.New("invalid expression")
			}

			b, _ := stack.Pop()
			a, _ := stack.Pop()

			var result int
			switch token {
			case "+":
				result = a + b
			case "-":
				result = a - b
			case "*":
				result = a * b
			case "/":
				if b == 0 {
					return 0, errors.New("division by zero")
				}
				result = a / b
			}

			stack.Push(result)
		default:
			var num int
			_, err := fmt.Sscanf(token, "%d", &num)
			if err != nil {
				return 0, fmt.Errorf("invalid token: %s", token)
			}
			stack.Push(num)
		}
	}

	if stack.Size() != 1 {
		return 0, errors.New("invalid expression")
	}

	return stack.Pop()
}

// ReverseString reverses a string using a stack
func ReverseString(s string) string {
	stack := NewStack[rune]()

	for _, char := range s {
		stack.Push(char)
	}

	var result strings.Builder
	for !stack.IsEmpty() {
		char, _ := stack.Pop()
		result.WriteRune(char)
	}

	return result.String()
}

// DemonstrateStack demonstrates stack operations
func DemonstrateStack() {
	fmt.Println("📚 Stack Data Structure Implementation in Go")
	fmt.Println(strings.Repeat("=", 70))

	// Basic operations
	fmt.Println("\n📋 Basic Stack Operations:")
	fmt.Println(strings.Repeat("-", 70))

	stack := NewStack[int]()
	fmt.Printf("Created new stack: %s\n", stack)
	fmt.Printf("Is empty: %v\n", stack.IsEmpty())

	// Push operations
	fmt.Println("\nPushing elements: 10, 20, 30, 40, 50")
	for _, val := range []int{10, 20, 30, 40, 50} {
		stack.Push(val)
		fmt.Printf("Pushed %d, Stack: %s\n", val, stack)
	}

	// Peek operation
	if top, err := stack.Peek(); err == nil {
		fmt.Printf("\nTop element (peek): %d\n", top)
	}

	fmt.Printf("Size: %d\n", stack.Size())

	// Pop operations
	fmt.Println("\nPopping elements:")
	for !stack.IsEmpty() {
		val, _ := stack.Pop()
		fmt.Printf("Popped %d, Stack: %s\n", val, stack)
	}

	// Error handling
	fmt.Println("\n🚨 Error Handling:")
	_, err := stack.Pop()
	if err != nil {
		fmt.Printf("Error: %v ✓\n", err)
	}

	// String stack
	fmt.Println("\n🔤 String Stack:")
	strStack := NewStack[string]()
	words := []string{"Hello", "World", "From", "Go"}

	for _, word := range words {
		strStack.Push(word)
	}

	fmt.Printf("Original: %v\n", words)
	fmt.Printf("Stack: %s\n", strStack)
	fmt.Printf("Reversed: %v\n", strStack.ToSlice())

	// Balanced parentheses
	fmt.Println("\n🔍 Balanced Parentheses Check:")
	testCases := []string{
		"()",
		"()[]{}",
		"(]",
		"([)]",
		"{[()]}",
		"((()))",
		"(()",
	}

	for _, test := range testCases {
		result := BalancedParentheses(test)
		status := "✓"
		if !result {
			status = "✗"
		}
		fmt.Printf("%s: %s\n", test, status)
	}

	// Postfix evaluation
	fmt.Println("\n🧮 Postfix Expression Evaluation:")
	expressions := [][]string{
		{"2", "3", "+"},           // 2 + 3 = 5
		{"2", "3", "+", "4", "*"}, // (2 + 3) * 4 = 20
		{"5", "1", "2", "+", "4", "*", "+", "3", "-"}, // 5 + ((1 + 2) * 4) - 3 = 14
	}

	for _, expr := range expressions {
		result, err := EvaluatePostfix(expr)
		if err == nil {
			fmt.Printf("%v = %d\n", expr, result)
		}
	}

	// String reversal
	fmt.Println("\n🔄 String Reversal:")
	original := "Hello, World!"
	reversed := ReverseString(original)
	fmt.Printf("Original: %s\n", original)
	fmt.Printf("Reversed: %s\n", reversed)

	// MinStack demonstration
	fmt.Println("\n📉 MinStack (Track Minimum):")
	minStack := NewMinStack[int](func(a, b int) bool { return a < b })

	operations := []int{5, 3, 7, 1, 9, 2}
	for _, val := range operations {
		minStack.Push(val)
		min, _ := minStack.GetMin()
		fmt.Printf("Pushed %d, Current min: %d\n", val, min)
	}

	// Thread-safe stack
	fmt.Println("\n🔒 Thread-Safe Stack:")
	tsStack := NewThreadSafeStack[int]()

	var wg sync.WaitGroup
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(val int) {
			defer wg.Done()
			tsStack.Push(val)
			fmt.Printf("Goroutine pushed: %d\n", val)
		}(i)
	}

	wg.Wait()
	fmt.Printf("Final size: %d\n", tsStack.Size())

	// Functional operations
	fmt.Println("\n🎨 Functional Operations:")
	numStack := NewStackFrom([]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10})

	evenStack := numStack.Filter(func(n int) bool { return n%2 == 0 })
	fmt.Printf("Original: %v\n", numStack.ToSlice())
	fmt.Printf("Even numbers: %v\n", evenStack.ToSlice())

	doubledStack := numStack.Map(func(n int) int { return n * 2 })
	fmt.Printf("Doubled: %v\n", doubledStack.ToSlice())
}

func main() {
	DemonstrateStack()
	fmt.Println("\n✨ Stack demonstration complete!")
}
