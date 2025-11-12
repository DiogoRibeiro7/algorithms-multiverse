// Stack Data Structure Implementation in Rust
//
// Time Complexity:
// - Push: O(1) amortized
// - Pop: O(1)
// - Peek: O(1)
// - Size: O(1)
// Space Complexity: O(n)
//
// A stack is a Last-In-First-Out (LIFO) data structure where elements are
// added and removed from the same end (top).
//
// Rust-specific features:
// - Ownership and move semantics for memory safety
// - Borrowing for non-consuming access
// - Option<T> for safe error handling
// - Interior mutability with RefCell where needed
// - Zero-cost abstractions with generics
// - Thread-safe variant with Arc and Mutex
// - Iterator implementation for idiomatic traversal

use std::fmt::{self, Debug, Display};
use std::iter::FromIterator;
use std::sync::{Arc, Mutex};

/// A generic LIFO stack implementation.
///
/// # Examples
/// ```
/// let mut stack = Stack::new();
/// stack.push(1);
/// stack.push(2);
/// assert_eq!(stack.pop(), Some(2));
/// assert_eq!(stack.peek(), Some(&1));
/// ```
#[derive(Debug, Clone)]
pub struct Stack<T> {
    items: Vec<T>,
}

impl<T> Stack<T> {
    /// Creates a new empty stack.
    ///
    /// # Examples
    /// ```
    /// let stack: Stack<i32> = Stack::new();
    /// assert!(stack.is_empty());
    /// ```
    pub fn new() -> Self {
        Self { items: Vec::new() }
    }

    /// Creates a new stack with the specified capacity.
    ///
    /// This pre-allocates memory, reducing reallocations for better performance.
    pub fn with_capacity(capacity: usize) -> Self {
        Self {
            items: Vec::with_capacity(capacity),
        }
    }

    /// Pushes an element onto the stack.
    ///
    /// # Time Complexity
    /// O(1) amortized
    ///
    /// # Examples
    /// ```
    /// let mut stack = Stack::new();
    /// stack.push(42);
    /// assert_eq!(stack.size(), 1);
    /// ```
    pub fn push(&mut self, item: T) {
        self.items.push(item);
    }

    /// Removes and returns the top element.
    ///
    /// Returns `None` if the stack is empty.
    ///
    /// # Time Complexity
    /// O(1)
    pub fn pop(&mut self) -> Option<T> {
        self.items.pop()
    }

    /// Returns a reference to the top element without removing it.
    ///
    /// Returns `None` if the stack is empty.
    ///
    /// # Time Complexity
    /// O(1)
    pub fn peek(&self) -> Option<&T> {
        self.items.last()
    }

    /// Returns a mutable reference to the top element.
    ///
    /// Returns `None` if the stack is empty.
    pub fn peek_mut(&mut self) -> Option<&mut T> {
        self.items.last_mut()
    }

    /// Returns the number of elements in the stack.
    pub fn size(&self) -> usize {
        self.items.len()
    }

    /// Returns `true` if the stack is empty.
    pub fn is_empty(&self) -> bool {
        self.items.is_empty()
    }

    /// Removes all elements from the stack.
    pub fn clear(&mut self) {
        self.items.clear();
    }

    /// Returns the capacity of the stack's internal buffer.
    pub fn capacity(&self) -> usize {
        self.items.capacity()
    }

    /// Reserves capacity for at least `additional` more elements.
    pub fn reserve(&mut self, additional: usize) {
        self.items.reserve(additional);
    }

    /// Shrinks the capacity to fit the current size.
    pub fn shrink_to_fit(&mut self) {
        self.items.shrink_to_fit();
    }

    /// Returns an iterator over the stack (top to bottom).
    pub fn iter(&self) -> impl Iterator<Item = &T> {
        self.items.iter().rev()
    }

    /// Returns a mutable iterator over the stack.
    pub fn iter_mut(&mut self) -> impl Iterator<Item = &mut T> {
        self.items.iter_mut().rev()
    }

    /// Consumes the stack and returns an iterator over its elements.
    pub fn into_iter_stack(self) -> impl Iterator<Item = T> {
        self.items.into_iter().rev()
    }

    /// Returns a slice of all elements (bottom to top).
    pub fn as_slice(&self) -> &[T] {
        &self.items
    }
}

impl<T: Clone> Stack<T> {
    /// Converts the stack to a Vec (top to bottom order).
    pub fn to_vec(&self) -> Vec<T> {
        self.items.iter().rev().cloned().collect()
    }

    /// Creates a stack from a slice.
    pub fn from_slice(slice: &[T]) -> Self {
        Self {
            items: slice.to_vec(),
        }
    }
}

impl<T: PartialEq> Stack<T> {
    /// Checks if the stack contains an element.
    ///
    /// # Time Complexity
    /// O(n)
    pub fn contains(&self, item: &T) -> bool {
        self.items.contains(item)
    }
}

// Trait implementations

impl<T> Default for Stack<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T> From<Vec<T>> for Stack<T> {
    fn from(vec: Vec<T>) -> Self {
        Self { items: vec }
    }
}

impl<T> FromIterator<T> for Stack<T> {
    fn from_iter<I: IntoIterator<Item = T>>(iter: I) -> Self {
        Self {
            items: iter.into_iter().collect(),
        }
    }
}

impl<T: Display> Display for Stack<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Stack[")?;
        for (i, item) in self.iter().enumerate() {
            if i > 0 {
                write!(f, ", ")?;
            }
            write!(f, "{}", item)?;
        }
        write!(f, "]")
    }
}

/// Thread-safe stack implementation using Arc and Mutex.
///
/// # Examples
/// ```
/// use std::sync::Arc;
/// use std::thread;
///
/// let stack = ThreadSafeStack::new();
/// let stack_clone = Arc::clone(&stack);
///
/// let handle = thread::spawn(move || {
///     stack_clone.push(42);
/// });
///
/// handle.join().unwrap();
/// assert_eq!(stack.pop(), Some(42));
/// ```
#[derive(Debug, Clone)]
pub struct ThreadSafeStack<T> {
    inner: Arc<Mutex<Vec<T>>>,
}

impl<T> ThreadSafeStack<T> {
    /// Creates a new thread-safe stack.
    pub fn new() -> Self {
        Self {
            inner: Arc::new(Mutex::new(Vec::new())),
        }
    }

    /// Pushes an element onto the stack.
    pub fn push(&self, item: T) {
        self.inner.lock().unwrap().push(item);
    }

    /// Pops an element from the stack.
    pub fn pop(&self) -> Option<T> {
        self.inner.lock().unwrap().pop()
    }

    /// Returns the size of the stack.
    pub fn size(&self) -> usize {
        self.inner.lock().unwrap().len()
    }

    /// Checks if the stack is empty.
    pub fn is_empty(&self) -> bool {
        self.inner.lock().unwrap().is_empty()
    }

    /// Clears all elements from the stack.
    pub fn clear(&self) {
        self.inner.lock().unwrap().clear();
    }
}

impl<T> Default for ThreadSafeStack<T> {
    fn default() -> Self {
        Self::new()
    }
}

/// MinStack tracks the minimum element efficiently.
///
/// # Examples
/// ```
/// let mut stack = MinStack::new();
/// stack.push(5);
/// stack.push(3);
/// stack.push(7);
/// assert_eq!(stack.get_min(), Some(&3));
/// stack.pop();
/// assert_eq!(stack.get_min(), Some(&3));
/// ```
#[derive(Debug, Clone)]
pub struct MinStack<T: Ord + Clone> {
    items: Vec<T>,
    min_stack: Vec<T>,
}

impl<T: Ord + Clone> MinStack<T> {
    /// Creates a new MinStack.
    pub fn new() -> Self {
        Self {
            items: Vec::new(),
            min_stack: Vec::new(),
        }
    }

    /// Pushes an element and updates the minimum.
    pub fn push(&mut self, item: T) {
        if let Some(min) = self.min_stack.last() {
            if item <= *min {
                self.min_stack.push(item.clone());
            } else {
                self.min_stack.push(min.clone());
            }
        } else {
            self.min_stack.push(item.clone());
        }

        self.items.push(item);
    }

    /// Pops the top element.
    pub fn pop(&mut self) -> Option<T> {
        self.min_stack.pop();
        self.items.pop()
    }

    /// Returns a reference to the top element.
    pub fn peek(&self) -> Option<&T> {
        self.items.last()
    }

    /// Returns a reference to the current minimum.
    ///
    /// # Time Complexity
    /// O(1)
    pub fn get_min(&self) -> Option<&T> {
        self.min_stack.last()
    }

    /// Returns the number of elements.
    pub fn size(&self) -> usize {
        self.items.len()
    }

    /// Checks if the stack is empty.
    pub fn is_empty(&self) -> bool {
        self.items.is_empty()
    }
}

impl<T: Ord + Clone> Default for MinStack<T> {
    fn default() -> Self {
        Self::new()
    }
}

/// Stack with a maximum capacity.
///
/// # Examples
/// ```
/// let mut stack = BoundedStack::new(3);
/// assert!(stack.push(1).is_ok());
/// assert!(stack.push(2).is_ok());
/// assert!(stack.push(3).is_ok());
/// assert!(stack.push(4).is_err()); // Stack full
/// ```
#[derive(Debug, Clone)]
pub struct BoundedStack<T> {
    items: Vec<T>,
    capacity: usize,
}

impl<T> BoundedStack<T> {
    /// Creates a bounded stack with the specified capacity.
    pub fn new(capacity: usize) -> Self {
        Self {
            items: Vec::with_capacity(capacity),
            capacity,
        }
    }

    /// Pushes an element if capacity allows.
    ///
    /// Returns `Ok(())` on success or `Err(item)` if stack is full.
    pub fn push(&mut self, item: T) -> Result<(), T> {
        if self.items.len() < self.capacity {
            self.items.push(item);
            Ok(())
        } else {
            Err(item)
        }
    }

    /// Pops the top element.
    pub fn pop(&mut self) -> Option<T> {
        self.items.pop()
    }

    /// Returns a reference to the top element.
    pub fn peek(&self) -> Option<&T> {
        self.items.last()
    }

    /// Returns the current size.
    pub fn size(&self) -> usize {
        self.items.len()
    }

    /// Returns the maximum capacity.
    pub fn capacity(&self) -> usize {
        self.capacity
    }

    /// Checks if the stack is full.
    pub fn is_full(&self) -> bool {
        self.items.len() >= self.capacity
    }

    /// Checks if the stack is empty.
    pub fn is_empty(&self) -> bool {
        self.items.is_empty()
    }
}

// Stack Applications

/// Checks if parentheses are balanced.
///
/// # Examples
/// ```
/// assert!(balanced_parentheses("()[]{}"));
/// assert!(balanced_parentheses("{[()]}"));
/// assert!(!balanced_parentheses("([)]"));
/// ```
pub fn balanced_parentheses(s: &str) -> bool {
    let mut stack = Stack::new();

    for ch in s.chars() {
        match ch {
            '(' | '[' | '{' => stack.push(ch),
            ')' => {
                if stack.pop() != Some('(') {
                    return false;
                }
            }
            ']' => {
                if stack.pop() != Some('[') {
                    return false;
                }
            }
            '}' => {
                if stack.pop() != Some('{') {
                    return false;
                }
            }
            _ => {}
        }
    }

    stack.is_empty()
}

/// Evaluates a postfix expression.
///
/// # Examples
/// ```
/// assert_eq!(evaluate_postfix(&["2", "3", "+"]), Ok(5));
/// assert_eq!(evaluate_postfix(&["2", "3", "+", "4", "*"]), Ok(20));
/// ```
pub fn evaluate_postfix(tokens: &[&str]) -> Result<i64, String> {
    let mut stack = Stack::new();

    for token in tokens {
        match *token {
            "+" | "-" | "*" | "/" => {
                let b = stack.pop().ok_or("Invalid expression")?;
                let a = stack.pop().ok_or("Invalid expression")?;

                let result = match *token {
                    "+" => a + b,
                    "-" => a - b,
                    "*" => a * b,
                    "/" => {
                        if b == 0 {
                            return Err("Division by zero".to_string());
                        }
                        a / b
                    }
                    _ => unreachable!(),
                };

                stack.push(result);
            }
            _ => {
                let num = token
                    .parse::<i64>()
                    .map_err(|_| format!("Invalid token: {}", token))?;
                stack.push(num);
            }
        }
    }

    if stack.size() == 1 {
        stack.pop().ok_or_else(|| "Empty stack".to_string())
    } else {
        Err("Invalid expression".to_string())
    }
}

/// Reverses a string using a stack.
pub fn reverse_string(s: &str) -> String {
    let stack: Stack<char> = s.chars().collect();
    stack.into_iter_stack().collect()
}

/// Converts infix to postfix notation.
pub fn infix_to_postfix(infix: &str) -> String {
    let mut stack = Stack::new();
    let mut output = Vec::new();

    let precedence = |op: char| match op {
        '+' | '-' => 1,
        '*' | '/' => 2,
        '^' => 3,
        _ => 0,
    };

    for ch in infix.chars() {
        match ch {
            ' ' => continue,
            '0'..='9' | 'a'..='z' | 'A'..='Z' => output.push(ch),
            '(' => stack.push(ch),
            ')' => {
                while let Some(&top) = stack.peek() {
                    if top == '(' {
                        break;
                    }
                    output.push(stack.pop().unwrap());
                }
                stack.pop(); // Remove '('
            }
            '+' | '-' | '*' | '/' | '^' => {
                while let Some(&top) = stack.peek() {
                    if top == '(' || precedence(top) < precedence(ch) {
                        break;
                    }
                    output.push(stack.pop().unwrap());
                }
                stack.push(ch);
            }
            _ => {}
        }
    }

    while let Some(op) = stack.pop() {
        output.push(op);
    }

    output.iter().collect()
}

fn main() {
    println!("📚 Stack Data Structure in Rust");
    println!("{}", "=".repeat(60));

    // Basic operations
    println!("\n📋 Basic Operations:");
    println!("{}", "-".repeat(60));

    let mut stack = Stack::new();
    println!("Created empty stack: {}", stack);
    println!("Is empty: {}", stack.is_empty());

    for i in 1..=5 {
        stack.push(i);
        println!("Pushed {}: {}", i, stack);
    }

    println!("\nPeek: {:?}", stack.peek());
    println!("Size: {}", stack.size());

    println!("\nPopping elements:");
    while let Some(val) = stack.pop() {
        println!("Popped {}: {}", val, stack);
    }

    // String stack
    println!("\n\n🔤 String Stack:");
    println!("{}", "-".repeat(60));

    let mut str_stack: Stack<&str> = Stack::new();
    let words = ["Hello", "World", "from", "Rust"];

    for word in &words {
        str_stack.push(word);
    }

    println!("Stack: {}", str_stack);
    println!("Reversed: {:?}", str_stack.to_vec());

    // Balanced parentheses
    println!("\n\n🔍 Balanced Parentheses:");
    println!("{}", "-".repeat(60));

    let test_cases = [
        "()",
        "()[]{}",
        "(]",
        "([)]",
        "{[()]}",
        "((()))",
        "(()",
    ];

    for test in &test_cases {
        let balanced = balanced_parentheses(test);
        let status = if balanced { "✓" } else { "✗" };
        println!("{:10} {}", test, status);
    }

    // Postfix evaluation
    println!("\n\n🧮 Postfix Expression Evaluation:");
    println!("{}", "-".repeat(60));

    let expressions = [
        vec!["2", "3", "+"],
        vec!["2", "3", "+", "4", "*"],
        vec!["5", "1", "2", "+", "4", "*", "+", "3", "-"],
    ];

    for expr in &expressions {
        match evaluate_postfix(expr) {
            Ok(result) => println!("{:?} = {}", expr, result),
            Err(e) => println!("{:?} Error: {}", expr, e),
        }
    }

    // String reversal
    println!("\n\n🔄 String Reversal:");
    println!("{}", "-".repeat(60));

    let text = "Hello, Rust!";
    let reversed = reverse_string(text);
    println!("Original: {}", text);
    println!("Reversed: {}", reversed);

    // Infix to postfix
    println!("\n\n📐 Infix to Postfix:");
    println!("{}", "-".repeat(60));

    let infix_exprs = ["a+b", "a+b*c", "(a+b)*c", "a+b*c-d"];

    for infix in &infix_exprs {
        let postfix = infix_to_postfix(infix);
        println!("{:15} -> {}", infix, postfix);
    }

    // MinStack
    println!("\n\n📉 MinStack (Track Minimum):");
    println!("{}", "-".repeat(60));

    let mut min_stack = MinStack::new();
    let values = [5, 3, 7, 1, 9, 2];

    for val in &values {
        min_stack.push(*val);
        println!(
            "Pushed {}, Min: {:?}",
            val,
            min_stack.get_min().unwrap()
        );
    }

    println!("\nPopping:");
    while !min_stack.is_empty() {
        let val = min_stack.pop().unwrap();
        let min = min_stack.get_min();
        println!("Popped {}, Min: {:?}", val, min);
    }

    // Bounded stack
    println!("\n\n📏 Bounded Stack (Fixed Capacity):");
    println!("{}", "-".repeat(60));

    let mut bounded = BoundedStack::new(3);
    println!("Capacity: {}", bounded.capacity());

    for i in 1..=5 {
        match bounded.push(i) {
            Ok(()) => println!("Pushed {}", i),
            Err(val) => println!("Failed to push {} (stack full)", val),
        }
    }

    // Thread-safe stack
    println!("\n\n🔒 Thread-Safe Stack:");
    println!("{}", "-".repeat(60));

    use std::thread;

    let ts_stack = ThreadSafeStack::new();
    let mut handles = vec![];

    for i in 0..5 {
        let stack_clone = ts_stack.clone();
        let handle = thread::spawn(move || {
            stack_clone.push(i);
            println!("Thread {} pushed {}", i, i);
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("\nFinal size: {}", ts_stack.size());
    println!("Elements:");
    while let Some(val) = ts_stack.pop() {
        println!("  {}", val);
    }

    // Iterator demonstration
    println!("\n\n🔁 Iterator Support:");
    println!("{}", "-".repeat(60));

    let stack: Stack<i32> = (1..=5).collect();
    println!("Stack from iterator: {}", stack);

    print!("Iteration (top to bottom): ");
    for val in stack.iter() {
        print!("{} ", val);
    }
    println!();

    // Performance metrics
    println!("\n\n⚡ Performance Metrics:");
    println!("{}", "-".repeat(60));

    let mut perf_stack = Stack::with_capacity(10000);
    let start = std::time::Instant::now();

    for i in 0..10000 {
        perf_stack.push(i);
    }

    let push_time = start.elapsed();

    let start = std::time::Instant::now();

    while perf_stack.pop().is_some() {}

    let pop_time = start.elapsed();

    println!("10,000 pushes: {:?}", push_time);
    println!("10,000 pops:   {:?}", pop_time);
}

// Cargo.toml (no external dependencies needed for basic implementation)
/*
[package]
name = "stack"
version = "0.1.0"
edition = "2021"
*/
