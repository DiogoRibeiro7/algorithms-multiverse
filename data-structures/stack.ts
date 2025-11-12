/**
 * Stack Data Structure Implementation in TypeScript
 *
 * Time Complexity:
 * - Push: O(1) amortized
 * - Pop: O(1)
 * - Peek: O(1)
 * - Size: O(1)
 *
 * Space Complexity: O(n)
 *
 * Features advanced TypeScript patterns:
 * - Generic type constraints and variance
 * - Conditional types for method return values
 * - Mapped types for transformation operations
 * - Template literal types for error messages
 * - Builder pattern with type-safe chaining
 * - Iterator protocol implementation
 * - Symbol-based private fields
 *
 * @packageDocumentation
 */

// ============================================================================
// Type Definitions and Constraints
// ============================================================================

/**
 * Base constraint for stack elements.
 * Using a branded type for additional type safety.
 */
export type StackElement = string | number | boolean | object | symbol | bigint;

/**
 * Error types for stack operations using template literal types.
 */
export type StackErrorType =
    | 'EMPTY_STACK'
    | 'OVERFLOW'
    | 'UNDERFLOW'
    | 'INVALID_OPERATION';

/**
 * Type-safe error messages using template literals.
 */
export type StackErrorMessage<T extends StackErrorType> =
    T extends 'EMPTY_STACK' ? 'Cannot perform operation on empty stack'
    : T extends 'OVERFLOW' ? 'Stack capacity exceeded'
    : T extends 'UNDERFLOW' ? 'Stack is empty'
    : T extends 'INVALID_OPERATION' ? 'Invalid operation for current stack state'
    : never;

/**
 * Custom error class for stack operations.
 */
export class StackError<T extends StackErrorType> extends Error {
    constructor(
        public readonly type: T,
        message?: string
    ) {
        super(message || (`Stack error: ${type}` as StackErrorMessage<T>));
        this.name = 'StackError';
    }
}

/**
 * Result type for operations that might fail.
 * Implements a Result/Either monad pattern.
 */
export type StackResult<T, E = StackError<StackErrorType>> =
    | { ok: true; value: T }
    | { ok: false; error: E };

/**
 * Helper to create success results.
 */
export const Ok = <T>(value: T): StackResult<T> => ({ ok: true, value });

/**
 * Helper to create error results.
 */
export const Err = <E>(error: E): StackResult<never, E> => ({ ok: false, error });

/**
 * Options for stack creation using mapped types.
 */
export interface StackOptions {
    readonly capacity?: number;
    readonly initialItems?: readonly StackElement[];
}

/**
 * Conditional type that determines if a stack operation can fail.
 */
export type MayFail<T, CanFail extends boolean> =
    CanFail extends true ? StackResult<T> : T;

// ============================================================================
// Core Stack Implementation
// ============================================================================

/**
 * Generic LIFO stack implementation with advanced TypeScript features.
 *
 * @template T - Type of elements stored in the stack
 *
 * @example
 * ```typescript
 * const stack = new Stack<number>();
 * stack.push(1);
 * stack.push(2);
 * console.log(stack.pop()); // 2
 * console.log(stack.peek()); // 1
 * ```
 */
export class Stack<T extends StackElement> implements Iterable<T> {
    private readonly items: T[] = [];
    private readonly maxCapacity?: number;

    /**
     * Symbol-based private field for internal state.
     */
    private readonly [Symbol.toStringTag] = 'Stack';

    constructor(options: StackOptions = {}) {
        this.maxCapacity = options.capacity;
        if (options.initialItems) {
            this.items.push(...(options.initialItems as T[]));
        }
    }

    /**
     * Pushes an element onto the stack.
     *
     * @param item - Element to push
     * @returns Result indicating success or capacity error
     *
     * @throws {StackError} When stack capacity is exceeded
     */
    push(item: T): StackResult<void> {
        if (this.maxCapacity && this.items.length >= this.maxCapacity) {
            return Err(new StackError('OVERFLOW', 'Stack capacity exceeded'));
        }

        this.items.push(item);
        return Ok(undefined);
    }

    /**
     * Removes and returns the top element.
     *
     * @returns Result containing the popped element or error
     */
    pop(): StackResult<T> {
        if (this.isEmpty()) {
            return Err(new StackError('UNDERFLOW', 'Cannot pop from empty stack'));
        }

        const item = this.items.pop()!;
        return Ok(item);
    }

    /**
     * Returns the top element without removing it.
     *
     * @returns Result containing the top element or error
     */
    peek(): StackResult<T> {
        if (this.isEmpty()) {
            return Err(new StackError('EMPTY_STACK'));
        }

        return Ok(this.items[this.items.length - 1]);
    }

    /**
     * Returns the number of elements in the stack.
     */
    size(): number {
        return this.items.length;
    }

    /**
     * Checks if the stack is empty.
     */
    isEmpty(): boolean {
        return this.items.length === 0;
    }

    /**
     * Checks if the stack is at capacity.
     */
    isFull(): boolean {
        return this.maxCapacity !== undefined && this.items.length >= this.maxCapacity;
    }

    /**
     * Clears all elements from the stack.
     */
    clear(): void {
        this.items.length = 0;
    }

    /**
     * Returns an array copy of stack elements (top to bottom).
     */
    toArray(): readonly T[] {
        return [...this.items].reverse();
    }

    /**
     * Returns a readonly view of the internal array.
     */
    asReadonly(): readonly T[] {
        return this.items;
    }

    /**
     * Implements the iterator protocol.
     * Iterates from top to bottom.
     */
    *[Symbol.iterator](): Iterator<T> {
        for (let i = this.items.length - 1; i >= 0; i--) {
            yield this.items[i];
        }
    }

    /**
     * Creates a new stack with transformed elements.
     *
     * @template U - Type of transformed elements
     * @param fn - Transformation function
     * @returns New stack with transformed elements
     */
    map<U extends StackElement>(fn: (item: T, index: number) => U): Stack<U> {
        const newStack = new Stack<U>({ capacity: this.maxCapacity });
        this.items.forEach((item, index) => {
            newStack.push(fn(item, index));
        });
        return newStack;
    }

    /**
     * Creates a new stack with elements that satisfy the predicate.
     *
     * @param predicate - Filter function
     * @returns New filtered stack
     */
    filter(predicate: (item: T, index: number) => boolean): Stack<T> {
        const newStack = new Stack<T>({ capacity: this.maxCapacity });
        this.items.forEach((item, index) => {
            if (predicate(item, index)) {
                newStack.push(item);
            }
        });
        return newStack;
    }

    /**
     * Reduces the stack to a single value.
     *
     * @template U - Type of accumulated value
     * @param reducer - Reducer function
     * @param initialValue - Initial accumulator value
     * @returns Reduced value
     */
    reduce<U>(reducer: (acc: U, item: T, index: number) => U, initialValue: U): U {
        return this.items.reduce(reducer, initialValue);
    }

    /**
     * Executes a function for each element (top to bottom).
     *
     * @param fn - Function to execute
     */
    forEach(fn: (item: T, index: number) => void): void {
        for (let i = this.items.length - 1; i >= 0; i--) {
            fn(this.items[i], this.items.length - 1 - i);
        }
    }

    /**
     * Checks if any element satisfies the predicate.
     */
    some(predicate: (item: T) => boolean): boolean {
        return this.items.some(predicate);
    }

    /**
     * Checks if all elements satisfy the predicate.
     */
    every(predicate: (item: T) => boolean): boolean {
        return this.items.every(predicate);
    }

    /**
     * Finds the first element matching the predicate (from top).
     */
    find(predicate: (item: T) => boolean): T | undefined {
        for (let i = this.items.length - 1; i >= 0; i--) {
            if (predicate(this.items[i])) {
                return this.items[i];
            }
        }
        return undefined;
    }

    /**
     * Custom JSON serialization.
     */
    toJSON(): { type: string; items: T[]; capacity?: number } {
        return {
            type: 'Stack',
            items: [...this.items].reverse(),
            capacity: this.maxCapacity,
        };
    }

    /**
     * String representation of the stack.
     */
    toString(): string {
        return `Stack[${this.toArray().join(', ')}]`;
    }
}

// ============================================================================
// MinStack - Tracks Minimum Element
// ============================================================================

/**
 * Stack that tracks the minimum element in O(1) time.
 *
 * @template T - Numeric type
 */
export class MinStack<T extends number> extends Stack<T> {
    private readonly minStack: T[] = [];

    /**
     * Pushes an element and updates minimum tracking.
     */
    override push(item: T): StackResult<void> {
        const result = super.push(item);

        if (result.ok) {
            if (this.minStack.length === 0) {
                this.minStack.push(item);
            } else {
                const currentMin = this.minStack[this.minStack.length - 1];
                this.minStack.push(Math.min(currentMin, item) as T);
            }
        }

        return result;
    }

    /**
     * Pops an element and updates minimum tracking.
     */
    override pop(): StackResult<T> {
        const result = super.pop();

        if (result.ok) {
            this.minStack.pop();
        }

        return result;
    }

    /**
     * Gets the current minimum in O(1) time.
     */
    getMin(): StackResult<T> {
        if (this.minStack.length === 0) {
            return Err(new StackError('EMPTY_STACK'));
        }

        return Ok(this.minStack[this.minStack.length - 1]);
    }

    /**
     * Clears both stacks.
     */
    override clear(): void {
        super.clear();
        this.minStack.length = 0;
    }
}

// ============================================================================
// Type-Safe Builder Pattern
// ============================================================================

/**
 * Builder for creating stacks with fluent API.
 *
 * @template T - Type of stack elements
 */
export class StackBuilder<T extends StackElement> {
    private capacity?: number;
    private items: T[] = [];

    /**
     * Sets the maximum capacity.
     */
    withCapacity(capacity: number): this {
        if (capacity < 0) {
            throw new Error('Capacity must be non-negative');
        }
        this.capacity = capacity;
        return this;
    }

    /**
     * Adds initial items.
     */
    withItems(...items: T[]): this {
        this.items.push(...items);
        return this;
    }

    /**
     * Builds the stack instance.
     */
    build(): Stack<T> {
        if (this.capacity && this.items.length > this.capacity) {
            throw new Error('Initial items exceed capacity');
        }

        return new Stack<T>({
            capacity: this.capacity,
            initialItems: this.items,
        });
    }

    /**
     * Builds a MinStack instance (only for numeric types).
     */
    buildMinStack<U extends T & number>(): MinStack<U> {
        if (this.capacity && this.items.length > this.capacity) {
            throw new Error('Initial items exceed capacity');
        }

        const minStack = new MinStack<U>({
            capacity: this.capacity,
        });

        this.items.forEach(item => {
            minStack.push(item as U);
        });

        return minStack;
    }
}

// ============================================================================
// Utility Functions and Type Guards
// ============================================================================

/**
 * Type guard to check if a result is successful.
 */
export function isOk<T>(result: StackResult<T>): result is { ok: true; value: T } {
    return result.ok === true;
}

/**
 * Type guard to check if a result is an error.
 */
export function isErr<T>(result: StackResult<T>): result is { ok: false; error: StackError<StackErrorType> } {
    return result.ok === false;
}

/**
 * Unwraps a result or throws an error.
 */
export function unwrap<T>(result: StackResult<T>): T {
    if (isOk(result)) {
        return result.value;
    }
    throw result.error;
}

/**
 * Unwraps a result or returns a default value.
 */
export function unwrapOr<T>(result: StackResult<T>, defaultValue: T): T {
    return isOk(result) ? result.value : defaultValue;
}

// ============================================================================
// Stack Applications
// ============================================================================

/**
 * Checks if parentheses/brackets are balanced.
 *
 * @param input - String to check
 * @returns True if balanced
 */
export function balancedParentheses(input: string): boolean {
    const stack = new Stack<string>();
    const pairs: Record<string, string> = {
        ')': '(',
        ']': '[',
        '}': '{',
    };

    for (const char of input) {
        if ('([{'.includes(char)) {
            stack.push(char);
        } else if (')]}'.includes(char)) {
            const result = stack.pop();
            if (isErr(result) || result.value !== pairs[char]) {
                return false;
            }
        }
    }

    return stack.isEmpty();
}

/**
 * Evaluates a postfix expression.
 *
 * @param tokens - Array of tokens
 * @returns Result of evaluation
 */
export function evaluatePostfix(tokens: string[]): StackResult<number> {
    const stack = new Stack<number>();
    const operators = new Set(['+', '-', '*', '/']);

    for (const token of tokens) {
        if (operators.has(token)) {
            const b = stack.pop();
            const a = stack.pop();

            if (isErr(a) || isErr(b)) {
                return Err(new StackError('INVALID_OPERATION', 'Insufficient operands'));
            }

            let result: number;
            switch (token) {
                case '+':
                    result = a.value + b.value;
                    break;
                case '-':
                    result = a.value - b.value;
                    break;
                case '*':
                    result = a.value * b.value;
                    break;
                case '/':
                    if (b.value === 0) {
                        return Err(new StackError('INVALID_OPERATION', 'Division by zero'));
                    }
                    result = a.value / b.value;
                    break;
                default:
                    return Err(new StackError('INVALID_OPERATION', `Unknown operator: ${token}`));
            }

            stack.push(result);
        } else {
            const num = parseFloat(token);
            if (isNaN(num)) {
                return Err(new StackError('INVALID_OPERATION', `Invalid number: ${token}`));
            }
            stack.push(num);
        }
    }

    if (stack.size() !== 1) {
        return Err(new StackError('INVALID_OPERATION', 'Invalid expression'));
    }

    return stack.pop();
}

/**
 * Reverses a string using a stack.
 */
export function reverseString(input: string): string {
    const stack = new Stack<string>();

    for (const char of input) {
        stack.push(char);
    }

    let result = '';
    for (const char of stack) {
        result += char;
    }

    return result;
}

/**
 * Converts infix to postfix notation.
 */
export function infixToPostfix(infix: string): string {
    const stack = new Stack<string>();
    const output: string[] = [];

    const precedence: Record<string, number> = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3,
    };

    const tokens = infix.split(/\s+/).filter(t => t);

    for (const token of tokens) {
        if (/^[a-zA-Z0-9]+$/.test(token)) {
            output.push(token);
        } else if (token === '(') {
            stack.push(token);
        } else if (token === ')') {
            while (!stack.isEmpty()) {
                const result = stack.pop();
                if (isErr(result)) break;

                if (result.value === '(') break;
                output.push(result.value);
            }
        } else if (token in precedence) {
            while (!stack.isEmpty()) {
                const result = stack.peek();
                if (isErr(result)) break;

                const top = result.value;
                if (top === '(' || precedence[top] < precedence[token]) {
                    break;
                }

                const popped = stack.pop();
                if (isOk(popped)) {
                    output.push(popped.value);
                }
            }
            stack.push(token);
        }
    }

    while (!stack.isEmpty()) {
        const result = stack.pop();
        if (isOk(result)) {
            output.push(result.value);
        }
    }

    return output.join(' ');
}

// ============================================================================
// Demonstration and Examples
// ============================================================================

/**
 * Demonstrates TypeScript-specific stack features.
 */
export function demonstrateStack(): void {
    console.log('📚 Stack - TypeScript Implementation');
    console.log('='.repeat(60));

    // Basic operations with type safety
    console.log('\n📋 Basic Operations:');
    const stack = new Stack<number>();
    console.log('Created empty stack');

    [1, 2, 3, 4, 5].forEach(n => {
        const result = stack.push(n);
        if (isOk(result)) {
            console.log(`Pushed ${n}: ${stack.toString()}`);
        }
    });

    // Pop with Result type
    console.log('\nPopping:');
    const popResult = stack.pop();
    if (isOk(popResult)) {
        console.log(`Popped: ${popResult.value}`);
    }

    // Peek without modifying
    const peekResult = stack.peek();
    if (isOk(peekResult)) {
        console.log(`Peek: ${peekResult.value}`);
    }

    // Iterator protocol
    console.log('\n🔁 Iterator (top to bottom):');
    for (const item of stack) {
        console.log(`  ${item}`);
    }

    // Functional operations
    console.log('\n🎨 Functional Operations:');
    const doubled = stack.map(x => x * 2);
    console.log('Original:', stack.toString());
    console.log('Doubled: ', doubled.toString());

    const evens = stack.filter(x => x % 2 === 0);
    console.log('Evens:   ', evens.toString());

    // Builder pattern
    console.log('\n🏗️  Builder Pattern:');
    const builtStack = new StackBuilder<string>()
        .withCapacity(5)
        .withItems('a', 'b', 'c')
        .build();

    console.log('Built stack:', builtStack.toString());

    // MinStack
    console.log('\n📉 MinStack:');
    const minStack = new MinStack<number>();

    [5, 3, 7, 1, 9, 2].forEach(n => {
        minStack.push(n);
        const min = minStack.getMin();
        if (isOk(min)) {
            console.log(`Pushed ${n}, Min: ${min.value}`);
        }
    });

    // Balanced parentheses
    console.log('\n🔍 Balanced Parentheses:');
    const testCases = ['()', '()[]{}', '(]', '([)]', '{[()]}'];
    testCases.forEach(test => {
        const balanced = balancedParentheses(test);
        console.log(`${test.padEnd(10)} ${balanced ? '✓' : '✗'}`);
    });

    // Postfix evaluation
    console.log('\n🧮 Postfix Evaluation:');
    const expressions = [
        ['2', '3', '+'],
        ['2', '3', '+', '4', '*'],
        ['5', '1', '2', '+', '4', '*', '+', '3', '-'],
    ];

    expressions.forEach(expr => {
        const result = evaluatePostfix(expr);
        if (isOk(result)) {
            console.log(`${expr.join(' ')} = ${result.value}`);
        }
    });

    // String reversal
    console.log('\n🔄 String Reversal:');
    const text = 'TypeScript';
    const reversed = reverseString(text);
    console.log(`Original: ${text}`);
    console.log(`Reversed: ${reversed}`);

    // Error handling
    console.log('\n❌ Error Handling:');
    const emptyStack = new Stack<number>();
    const popEmpty = emptyStack.pop();

    if (isErr(popEmpty)) {
        console.log(`Error type: ${popEmpty.error.type}`);
        console.log(`Error message: ${popEmpty.error.message}`);
    }

    // JSON serialization
    console.log('\n📄 JSON Serialization:');
    console.log(JSON.stringify(stack.toJSON(), null, 2));
}

// Run demonstration if executed directly
if (typeof require !== 'undefined' && require.main === module) {
    demonstrateStack();
}

// Export all public API
export default {
    Stack,
    MinStack,
    StackBuilder,
    StackError,
    Ok,
    Err,
    isOk,
    isErr,
    unwrap,
    unwrapOr,
    balancedParentheses,
    evaluatePostfix,
    reverseString,
    infixToPostfix,
};
